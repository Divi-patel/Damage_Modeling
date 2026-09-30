#!/usr/bin/env python3
"""Reference evaluator for the TC-wind × wind model-v1 curve records.

The helper implements the current and preserved-proposal bundle-v3
``thresholded_weibull_expected_damage`` record exactly.  It emits only a
conditional scalar damage ratio for the quarantined Jaimes source-native
exposure atom.  It never assembles dollar, whole-plant, annual, or financial
loss. This remains an authoring/review helper; production Hazard uses the
registry-fed common loader.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Mapping


SUPPORTED_PATHWAY = "tropical_cyclone_wind"
SUPPORTED_FAILURE_UNIT = "WT_JAIMES_TURBINE_TOWER_EXPOSURE_UNIT"
PROXY_FAILURE_UNIT = "WT_TURBINE_EQUIPMENT_ASSEMBLY"
SUPPORTED_ASSUMPTION_SET = (
    "JAIMES_2020_GENERIC_FIXED_BASE_STEEL_PARKED_ROTOR_AS_DOCUMENTED"
)
PROXY_ARCHETYPE_ID = "CONUS_WIND_FARM_5MW_HH100_PROXY_V1"
PROXY_POLICY_ID = "TCWW_OWNER_APPROVED_3P3MW_FOR_CANONICAL_5MW_V1"
PROXY_ASSET_PROFILE_ID = "CONUS_WIND_FARM_REFERENCE_V1"
PROXY_VALUE_BASIS_ID = "CONUS_WIND_FARM_ROTOR_NACELLE_TOWER_63PCT_V1"
PROXY_COVERED_VALUE_SHARE = 0.63
TOWER_PROXY_FAILURE_UNIT = SUPPORTED_FAILURE_UNIT
TOWER_PROXY_ARCHETYPE_ID = "CONUS_WIND_FARM_5MW_HH100_TOWER_PROXY_V1"
TOWER_PROXY_POLICY_ID = "TCWW_OWNER_APPROVED_3P3MW_FOR_CANONICAL_5MW_TOWER_ONLY_V1"
TOWER_PROXY_ASSET_PROFILE_ID = PROXY_ASSET_PROFILE_ID
TOWER_PROXY_VALUE_BASIS_ID = "CONUS_WIND_FARM_TOWER_16PCT_V1"
TOWER_PROXY_COVERED_VALUE_SHARE = 0.16
PROXY_TRANSITION_ZERO_UPPER_KMH = 108.0
PROXY_SOURCE_CEILING_KMH = 252.0
AXIS_ID = "TC_PEAK_GUST_3S_10M_KMH_JAIMES"
AXIS_FIELD = "tc_peak_gust_3s_10m_kmh"
INCOMPATIBLE_AXIS_FIELDS = frozenset(
    {
        "saffir_simpson_category",
        "nhc_maximum_sustained_surface_wind_mps",
        "hub_height_3s_gust_mps",
        "tc_peak_gust_3s_10m_mps",
        "maximum_sustained_wind_mph",
        "maximum_sustained_wind_knots",
    }
)


class TropicalCycloneWindEvaluationError(ValueError):
    """Fail-closed error carrying a stable machine reason code."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def load_artifact(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def artifact_sha256(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify_artifact_pin(
    artifact: Mapping[str, Any],
    pin: Mapping[str, Any],
    *,
    artifact_sha256_hex: str,
) -> None:
    expected = {
        "cell_id": artifact["cell_id"],
        "semantic_damage_model_version": artifact["semantic_damage_model_version"],
        "documentation_revision": artifact["documentation_revision"],
        "schema_version": artifact["schema_version"],
        "artifact_sha256": artifact_sha256_hex,
    }
    if set(pin) != set(expected):
        raise TropicalCycloneWindEvaluationError(
            "ARTIFACT_PIN_INCOMPLETE",
            "pin must contain exactly cell, model, docs, schema, and SHA",
        )
    mismatches = [key for key, value in expected.items() if pin[key] != value]
    if mismatches:
        raise TropicalCycloneWindEvaluationError(
            "ARTIFACT_PIN_MISMATCH",
            "pin mismatch for " + ", ".join(sorted(mismatches)),
        )


def _finite_number(value: Any, code: str, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TropicalCycloneWindEvaluationError(code, f"{field} must be numeric")
    numeric = float(value)
    if not math.isfinite(numeric):
        raise TropicalCycloneWindEvaluationError(code, f"{field} must be finite")
    return numeric


def evaluate_thresholded_weibull_expected_damage_record(
    record: Mapping[str, Any], speed_kmh: float
) -> float:
    """Evaluate one exact source-fitted expected-damage record."""

    if record.get("curve_form") != "thresholded_weibull_expected_damage":
        raise TropicalCycloneWindEvaluationError(
            "CURVE_FORM_UNSUPPORTED",
            f"unsupported curve form {record.get('curve_form')!r}",
        )
    parameters = record["parameters"]
    v_zero = _finite_number(
        parameters.get("V_zero_kmh"), "CURVE_PAYLOAD_INVALID", "V_zero_kmh"
    )
    delta_v50 = _finite_number(
        parameters.get("delta_V50_kmh"),
        "CURVE_PAYLOAD_INVALID",
        "delta_V50_kmh",
    )
    rho = _finite_number(parameters.get("rho"), "CURVE_PAYLOAD_INVALID", "rho")
    v_at_dr50 = _finite_number(
        parameters.get("V_at_DR50_kmh"),
        "CURVE_PAYLOAD_INVALID",
        "V_at_DR50_kmh",
    )
    max_dr = _finite_number(
        parameters.get("max_dr"), "CURVE_PAYLOAD_INVALID", "max_dr"
    )
    if v_zero < 0 or delta_v50 <= 0 or rho <= 0 or not 0 <= max_dr <= 1:
        raise TropicalCycloneWindEvaluationError(
            "CURVE_PAYLOAD_INVALID", "curve parameters violate their bounds"
        )
    if not math.isclose(
        v_at_dr50, v_zero + delta_v50, rel_tol=0.0, abs_tol=1e-12
    ):
        raise TropicalCycloneWindEvaluationError(
            "CURVE_PAYLOAD_INVALID", "V_at_DR50 must equal V_zero + delta_V50"
        )
    if speed_kmh <= v_zero:
        return 0.0
    damage_ratio = max_dr * (
        1.0
        - math.exp(
            -math.log(2.0)
            * math.pow((speed_kmh - v_zero) / delta_v50, rho)
        )
    )
    if not math.isfinite(damage_ratio):
        raise TropicalCycloneWindEvaluationError(
            "CURVE_PAYLOAD_INVALID", "curve evaluation is not finite"
        )
    return min(1.0, max(0.0, damage_ratio))


def evaluate_proxy_screening_completion(
    record: Mapping[str, Any], speed_kmh: float
) -> tuple[float, str | None]:
    """Complete the named proxy outside the source-supported simulation band.

    The source curve itself is not rewritten: the named canonical-5-MW proxy
    alone assigns zero in the 90–108 km/h transition and caps DR at ``max_dr``
    above 252 km/h.  The second return value is the disclosure flag.
    """
    if 90.0 < speed_kmh < PROXY_TRANSITION_ZERO_UPPER_KMH:
        return 0.0, "SCREENING_TRANSITION_BAND_ASSIGNED_ZERO"
    if speed_kmh > PROXY_SOURCE_CEILING_KMH:
        max_dr = _finite_number(
            record["parameters"].get("max_dr"),
            "CURVE_PAYLOAD_INVALID",
            "max_dr",
        )
        return max_dr, "SCREENING_ABOVE_SOURCE_RANGE_CAPPED_AT_MAX_DR"
    return evaluate_thresholded_weibull_expected_damage_record(record, speed_kmh), None


def _pathway(artifact: Mapping[str, Any]) -> Mapping[str, Any]:
    matches = [
        item
        for item in artifact["pathways"]
        if item["pathway_id"] == SUPPORTED_PATHWAY
    ]
    if len(matches) != 1:
        raise TropicalCycloneWindEvaluationError(
            "CURVE_PAYLOAD_INVALID", "TC pathway is not uniquely declared"
        )
    pathway = matches[0]
    axis = pathway.get("hazard_axis", {})
    if axis.get("id") != AXIS_ID or axis.get("preferred_input_field") != AXIS_FIELD:
        raise TropicalCycloneWindEvaluationError(
            "CURVE_PAYLOAD_INVALID",
            "TC source-native axis identity or preferred input field changed",
        )
    return pathway


def _select_record(
    pathway: Mapping[str, Any], archetype_id: str
) -> Mapping[str, Any]:
    matches = [
        record
        for record in pathway["curve_records"]
        if record["selector_match"]["turbine_archetype_id"] == archetype_id
    ]
    if len(matches) != 1:
        raise TropicalCycloneWindEvaluationError(
            "TURBINE_ARCHETYPE_UNSUPPORTED",
            "archetype must match exactly one Jaimes record",
        )
    return matches[0]


def _validate_proxy_request(
    artifact: Mapping[str, Any],
    request: Mapping[str, Any],
    record: Mapping[str, Any],
) -> Mapping[str, Any] | None:
    """Validate an exact named bridge; never infer a nearest neighbour.

    Model v1.1 is retained for archived reproduction.  Model v1.2 corrects
    the value/failure-unit binding while preserving the numerical curve.
    """

    selector = record.get("selector_match", {})
    archetype_id = selector.get("turbine_archetype_id")
    model_version = artifact.get("semantic_damage_model_version")
    configs = {
        ("model v1.1", PROXY_ARCHETYPE_ID): {
            "failure_unit_id": PROXY_FAILURE_UNIT,
            "proxy_policy_id": PROXY_POLICY_ID,
            "canonical_asset_profile_id": PROXY_ASSET_PROFILE_ID,
            "covered_value_basis_id": PROXY_VALUE_BASIS_ID,
            "covered_value_share": PROXY_COVERED_VALUE_SHARE,
            "covered_subsystems": ["rotor", "nacelle", "tower"],
            "coverage_flag": "PARTIAL_STRUCTURAL_VALUE_COVERAGE_63PCT",
            "uncovered_flag": "UNCOVERED_PROJECT_VALUE_37PCT_WITHHELD_NOT_ZERO",
            "scenario_loss_status": "consumer_computable_with_explicit_0p63_covered_value_cap",
        },
        ("model v1.2", TOWER_PROXY_ARCHETYPE_ID): {
            "failure_unit_id": TOWER_PROXY_FAILURE_UNIT,
            "proxy_policy_id": TOWER_PROXY_POLICY_ID,
            "canonical_asset_profile_id": TOWER_PROXY_ASSET_PROFILE_ID,
            "covered_value_basis_id": TOWER_PROXY_VALUE_BASIS_ID,
            "covered_value_share": TOWER_PROXY_COVERED_VALUE_SHARE,
            "covered_subsystems": ["tower"],
            "coverage_flag": "PARTIAL_TOWER_VALUE_COVERAGE_16PCT",
            "uncovered_flag": "UNCOVERED_PROJECT_VALUE_84PCT_WITHHELD_NOT_ZERO",
            "scenario_loss_status": "consumer_computable_with_explicit_0p16_tower_value_cap",
        },
        ("model v1.3", TOWER_PROXY_ARCHETYPE_ID): {
            "failure_unit_id": TOWER_PROXY_FAILURE_UNIT,
            "proxy_policy_id": "TCWW_OWNER_APPROVED_3P3MW_FOR_CANONICAL_5MW_PHYSICAL_TOWER_V1",
            "canonical_asset_profile_id": "CONUS_WIND_FARM_REFERENCE_V2",
            "covered_value_basis_id": "CONUS_WIND_FARM_SOURCE_TOWER_VALUE_V1",
            "covered_value_share": 276 / 1623,
            "covered_subsystems": ["tower"],
            "coverage_flag": "PARTIAL_SOURCE_COST_TOWER_VALUE_COVERAGE",
            "uncovered_flag": "NON_TOWER_PHYSICAL_VALUE_WITHHELD_NOT_ZERO",
            "scenario_loss_status": "consumer_computable_with_exact_source_tower_value_cap",
        },
    }
    config = configs.get((model_version, archetype_id))
    if config is None:
        if archetype_id in {PROXY_ARCHETYPE_ID, TOWER_PROXY_ARCHETYPE_ID}:
            raise TropicalCycloneWindEvaluationError(
                "TURBINE_ARCHETYPE_UNSUPPORTED",
                "the requested canonical 5 MW proxy is not part of this model version",
            )
        return None
    required = {
        "proxy_policy_id": config["proxy_policy_id"],
        "canonical_asset_profile_id": config["canonical_asset_profile_id"],
        "covered_value_basis_id": config["covered_value_basis_id"],
    }
    missing = [field for field in required if not request.get(field)]
    if missing:
        raise TropicalCycloneWindEvaluationError(
            "OWNER_APPROVED_PROXY_OPT_IN_REQUIRED",
            "explicit proxy fields are required: " + ", ".join(missing),
        )
    mismatches = [
        field for field, expected in required.items() if request.get(field) != expected
    ]
    if mismatches:
        raise TropicalCycloneWindEvaluationError(
            "OWNER_APPROVED_PROXY_IDENTITY_MISMATCH",
            "proxy identity mismatch for " + ", ".join(mismatches),
        )
    if record.get("failure_unit_id") != config["failure_unit_id"]:
        raise TropicalCycloneWindEvaluationError(
            "CURVE_PAYLOAD_INVALID", "proxy record failure unit changed"
        )
    return config


def _withheld_by_unit(
    artifact: Mapping[str, Any]
) -> dict[str, list[str]]:
    capability = artifact["capability_declaration"]["pathway_capabilities"]
    matches = [item for item in capability if item["pathway_id"] == SUPPORTED_PATHWAY]
    if len(matches) != 1:
        raise TropicalCycloneWindEvaluationError(
            "CURVE_PAYLOAD_INVALID", "TC capability is not uniquely declared"
        )
    return {
        item["failure_unit_id"]: list(item["reason_codes"])
        for item in matches[0]["withheld_failure_units"]
    }


def _withheld_result(
    *,
    pathway_id: str,
    unit: Mapping[str, Any],
    reason_codes: list[str],
    flags: list[str],
) -> dict[str, Any]:
    return {
        "pathway_id": pathway_id,
        "failure_unit_id": unit["id"],
        "curve_id": None,
        "subsystem": unit["subsystem"],
        "component": unit["component"],
        "status": "withheld",
        "scalar_central_dr": None,
        "withheld_reason_codes": list(dict.fromkeys(reason_codes)),
        "metadata_flags": list(dict.fromkeys(flags)),
    }


def evaluate_damage_call(
    artifact: Mapping[str, Any], request: Mapping[str, Any]
) -> dict[str, Any]:
    """Evaluate one governed TC-wind request and return damage-emit-v2."""

    pathway_id = request.get("pathway_id")
    if pathway_id is None or pathway_id == "":
        raise TropicalCycloneWindEvaluationError(
            "PATHWAY_ID_REQUIRED", "pathway_id is required and has no default"
        )
    if pathway_id != SUPPORTED_PATHWAY:
        raise TropicalCycloneWindEvaluationError(
            "PATHWAY_ID_UNKNOWN", f"unsupported pathway_id {pathway_id!r}"
        )
    pathway = _pathway(artifact)

    archetype_id = request.get("turbine_archetype_id")
    if archetype_id is None or archetype_id == "":
        raise TropicalCycloneWindEvaluationError(
            "TURBINE_ARCHETYPE_REQUIRED",
            "an exact Jaimes turbine_archetype_id is required",
        )
    if not isinstance(archetype_id, str):
        raise TropicalCycloneWindEvaluationError(
            "TURBINE_ARCHETYPE_UNSUPPORTED", "archetype ID must be a string"
        )
    record = _select_record(pathway, archetype_id)
    proxy_config = _validate_proxy_request(artifact, request, record)
    proxy_route = proxy_config is not None

    assumption_set = request.get("source_model_assumption_set_id")
    if assumption_set is None or assumption_set == "":
        raise TropicalCycloneWindEvaluationError(
            "SOURCE_MODEL_ASSUMPTION_SET_REQUIRED",
            "source model assumption acknowledgement is required",
        )
    if assumption_set != SUPPORTED_ASSUMPTION_SET:
        raise TropicalCycloneWindEvaluationError(
            "SOURCE_MODEL_ASSUMPTION_SET_UNSUPPORTED",
            "only the documented Jaimes source-model state is supported",
        )

    if AXIS_FIELD not in request:
        present_incompatible = sorted(INCOMPATIBLE_AXIS_FIELDS.intersection(request))
        detail = (
            f"; incompatible fields present: {', '.join(present_incompatible)}"
            if present_incompatible
            else ""
        )
        raise TropicalCycloneWindEvaluationError(
            "TC_SOURCE_NATIVE_AXIS_REQUIRED",
            f"{AXIS_FIELD} is required{detail}",
        )
    if INCOMPATIBLE_AXIS_FIELDS.intersection(request):
        raise TropicalCycloneWindEvaluationError(
            "TC_SOURCE_NATIVE_AXIS_REQUIRED",
            "source-native input cannot be combined with category, NHC, hub, or alternate-unit fields",
        )
    speed = _finite_number(
        request[AXIS_FIELD], "TC_SOURCE_NATIVE_AXIS_REQUIRED", AXIS_FIELD
    )
    if speed < 0:
        raise TropicalCycloneWindEvaluationError(
            "AXIS_OUTSIDE_VALID_RANGE", "TC source-native gust cannot be negative"
        )

    failure_units = {item["id"]: item for item in artifact["failure_units"]}
    requested_unit = request.get("failure_unit_id")
    if requested_unit is not None and requested_unit not in failure_units:
        raise TropicalCycloneWindEvaluationError(
            "FAILURE_UNIT_ID_UNKNOWN", f"unknown failure_unit_id {requested_unit!r}"
        )
    unit_ids = [requested_unit] if requested_unit is not None else list(failure_units)
    withheld_by_unit = _withheld_by_unit(artifact)

    base_flags = list(artifact["evaluation_contract"]["metadata_flags_always"])
    base_flags.append("SOURCE_MODEL_ASSUMPTION_SET_ACKNOWLEDGED")
    if proxy_route:
        assert proxy_config is not None
        base_flags.extend(
            [
                "OWNER_APPROVED_SCREENING_PROXY",
                "REQUESTED_5MW_EVALUATED_WITH_3P3MW_SOURCE_CURVE",
                "NO_CAPACITY_RATIO_SCALING",
                proxy_config["coverage_flag"],
                proxy_config["uncovered_flag"],
            ]
        )
    if archetype_id == "TCWW_JAIMES_GENERIC_1MW_HH44_V1":
        base_flags.append("SOURCE_1MW_HUB_HEIGHT_TABLE_44M_FIGURE_CAPTION_40M")
    control_state = request.get("actual_operating_control_state")
    if control_state == "unknown":
        base_flags.append("SOURCE_MODEL_CONTROL_STATE_UNKNOWN")
    elif control_state not in {
        None,
        "known_consistent_with_source_assumption",
        "known_inconsistent_with_source_assumption",
    }:
        raise TropicalCycloneWindEvaluationError(
            "CONDITIONER_VALUE_UNSUPPORTED",
            f"unsupported actual_operating_control_state {control_state!r}",
        )
    control_mismatch = control_state == "known_inconsistent_with_source_assumption"

    results: list[dict[str, Any]] = []
    for failure_unit_id in unit_ids:
        unit = failure_units[failure_unit_id]
        if failure_unit_id != record["failure_unit_id"]:
            results.append(
                _withheld_result(
                    pathway_id=pathway_id,
                    unit=unit,
                    reason_codes=[
                        "NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT",
                        *withheld_by_unit.get(failure_unit_id, []),
                    ],
                    flags=base_flags,
                )
            )
            continue
        if control_mismatch:
            results.append(
                _withheld_result(
                    pathway_id=pathway_id,
                    unit=unit,
                    reason_codes=["SOURCE_MODEL_CONTROL_STATE_MISMATCH"],
                    flags=base_flags,
                )
            )
            continue
        if 90 < speed < 108 and not proxy_route:
            results.append(
                _withheld_result(
                    pathway_id=pathway_id,
                    unit=unit,
                    reason_codes=["BELOW_SOURCE_SIMULATION_RANGE"],
                    flags=base_flags,
                )
            )
            continue
        if speed > 252 and not proxy_route:
            results.append(
                _withheld_result(
                    pathway_id=pathway_id,
                    unit=unit,
                    reason_codes=["ABOVE_SOURCE_SIMULATION_RANGE"],
                    flags=base_flags,
                )
            )
            continue
        result_flags = list(base_flags)
        if speed <= 90:
            result_flags.append("SOURCE_ASSUMED_NO_DAMAGE_THRESHOLD_NOT_EMPIRICAL")
        if proxy_route:
            damage_ratio, completion_flag = evaluate_proxy_screening_completion(
                record, speed
            )
            if completion_flag:
                result_flags.append(completion_flag)
        else:
            damage_ratio = evaluate_thresholded_weibull_expected_damage_record(
                record, speed
            )
        results.append(
            {
                "pathway_id": pathway_id,
                "failure_unit_id": failure_unit_id,
                "curve_id": record["curve_id"],
                "subsystem": unit["subsystem"],
                "component": unit["component"],
                "status": "supported",
                "scalar_central_dr": damage_ratio,
                "withheld_reason_codes": [],
                "metadata_flags": list(dict.fromkeys(result_flags)),
            }
        )

    return {
        "schema_version": "damage_emit.v2",
        "cell_id": artifact["cell_id"],
        "damage_code_id": artifact["damage_code_id"],
        "model_version": artifact["semantic_damage_model_version"],
        "pathway_id": pathway_id,
        "emit_mode": "scalar_mean",
        "hazard_input_used": {
            "axis_id": pathway["hazard_axis"]["id"],
            "input_field": AXIS_FIELD,
            "value": speed,
            "unit": "km/h",
        },
        "input_quality": {
            "source_simulation_range_kmh": [108, 252],
            "source_assumed_zero_branch_kmh": [0, 90],
            "proxy_screening_completion": (
                {
                    "transition_band_kmh": [90, 108],
                    "transition_treatment": "zero_with_explicit_flag",
                    "above_source_ceiling_kmh": 252,
                    "above_ceiling_treatment": "cap_at_max_dr_with_explicit_flag",
                }
                if proxy_route
                else None
            ),
            "scenario_loss_status": (
                proxy_config["scenario_loss_status"]
                if proxy_route
                else "withheld"
            ),
        },
        "selectors_used": {
            "turbine_archetype_id": archetype_id,
            "source_model_assumption_set_id": assumption_set,
            **(
                {
                    "proxy_policy_id": proxy_config["proxy_policy_id"],
                    "canonical_asset_profile_id": proxy_config["canonical_asset_profile_id"],
                    "covered_value_basis_id": proxy_config["covered_value_basis_id"],
                }
                if proxy_route
                else {}
            ),
        },
        "conditioners_used": {
            "actual_operating_control_state": control_state
        },
        "exposure_used": (
            {
                "covered_value_share_of_project_tiv": proxy_config["covered_value_share"],
                "uncovered_value_share_of_project_tiv": 1.0
                - proxy_config["covered_value_share"],
                "covered_subsystems": proxy_config["covered_subsystems"],
                "uncovered_treatment": "withheld_not_zero",
            }
            if proxy_route
            else {}
        ),
        "failure_unit_results": results,
        "capability_declaration_ref": (
            "tropical_cyclone_wind_wind__"
            + artifact["semantic_damage_model_version"].replace(" ", "_").replace(".", "_")
            + "__"
            + artifact["documentation_revision"].replace(" ", "_")
            + "__capability.json"
        ),
        "cap_binding_preflight_ref": None,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("request", help="JSON object or path to a JSON file")
    args = parser.parse_args()
    request_text = args.request
    if request_text.lstrip().startswith("{"):
        request = json.loads(request_text)
    else:
        request_path = Path(request_text)
        if request_path.exists():
            request = json.loads(request_path.read_text())
        else:
            request = json.loads(request_text)
    artifact = load_artifact(args.artifact)
    print(json.dumps(evaluate_damage_call(artifact, request), indent=2))


if __name__ == "__main__":
    main()
