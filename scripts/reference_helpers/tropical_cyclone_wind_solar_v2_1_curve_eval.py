#!/usr/bin/env python3
"""Coverage-complete screening evaluator for TC-wind x solar model v2.1.

Model v2.1 preserves the v2.0 architecture-specific array curves, adds
explicit Tier-4 site-facility proxy curves, and assembles a named replacement-
value profile into plant physical DR and scenario loss.  It remains a
screening proxy; annual frequency and tail metrics remain consumer-owned.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

import tropical_cyclone_wind_solar_v2_curve_eval as v20


PATHWAY = v20.PATHWAY
FIXED = v20.FIXED
TRACKER = v20.TRACKER
PERRY = v20.PERRY
REFERENCE_PROFILE_ID = "NLR_Q1_2025_UPV_PV_ONLY_2024_USD_PHYSICAL_V1"
COMMON_CURVE_UNITS = (
    "PV_FOUNDATION",
    "PV_POWER_CONVERSION_AND_COLLECTION",
    "PV_GSU_SUBSTATION",
    "PV_SCADA_COMMUNICATIONS",
    "PV_CIVIL_INFRA",
)
SUPPORT_UNIT = "PV_REPLACEMENT_SUPPORT"
SITE_AXIS_FIELDS = frozenset(
    {
        "tc_site_event_to_design_wind_pressure_ratio",
        "tc_peak_gust_3s_10m_mps",
        "qualified_site_design_3s_gust_mps",
        "site_facility_demand_bridge_id",
    }
)
ASSEMBLY_FIELDS = frozenset(
    {
        "output_mode",
        "value_profile_id",
        "capacity_kwdc",
        "array_exposure_basis",
    }
)
REFERENCE_VALUES_PER_KWDC = {
    "PV_FIXED_TILT_MODULE_FIELD": 291.21485143992487,
    "PV_TRACKER_MODULE_FIELD": 291.21485143992487,
    "PV_FIXED_TILT_SUPPORT_STRUCTURE": 109.98972602739727,
    "PV_TRACKER_SBOS_ASSEMBLY": 109.98972602739727,
    "PV_FOUNDATION": 31.12448715327472,
    "PV_POWER_CONVERSION_AND_COLLECTION": 116.83772835067089,
    "PV_GSU_SUBSTATION": 106.50466417910448,
    "PV_SCADA_COMMUNICATIONS": 1.31,
    "PV_CIVIL_INFRA": 31.223744292237445,
    SUPPORT_UNIT: 189.59050092005714,
}
PHYSICAL_REPLACEMENT_VALUE_PER_KWDC = 877.7957023626668
INSTALLED_CAPEX_PER_KWDC = 1120.0
EXCLUDED_SOFT_NONPHYSICAL_VALUE_PER_KWDC = 242.20429763733296
STALE_LIMITATION_FLAGS = {
    "SCENARIO_DOLLAR_LOSS_WITHHELD",
    "FULL_PLANT_PHYSICAL_LOSS_INCOMPLETE",
    "NO_CANONICAL_OR_HAZARD_CUTOVER",
}


class TropicalCycloneWindSolarV21EvaluationError(ValueError):
    """Fail-closed v2.1 error with a stable code."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def load_artifact(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def _number(value: Any, code: str, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TropicalCycloneWindSolarV21EvaluationError(code, f"{field} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise TropicalCycloneWindSolarV21EvaluationError(code, f"{field} must be finite")
    return result


def _text(value: Any, code: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise TropicalCycloneWindSolarV21EvaluationError(code, f"{field} must be non-empty")
    return value


def _capability_ref(
    artifact: Mapping[str, Any], verified_artifact_sha256_hex: str | None
) -> dict[str, Any]:
    docs_stem = str(artifact["documentation_revision"]).replace(" ", "_")
    return {
        "path": f"tropical_cyclone_wind_solar__model_v2_1__{docs_stem}__capability.json",
        "semantic_damage_model_version": artifact["semantic_damage_model_version"],
        "documentation_revision": artifact["documentation_revision"],
        "artifact_schema_version": artifact["schema_version"],
        "artifact_sha256": verified_artifact_sha256_hex,
        "pin_status": (
            "verified_by_caller"
            if verified_artifact_sha256_hex is not None
            else "unbound_reference_evaluation"
        ),
    }


def _site_axis(request: Mapping[str, Any]) -> tuple[float, dict[str, Any], list[str]]:
    bridge_id = _text(
        request.get("site_facility_demand_bridge_id"),
        "SITE_FACILITY_DEMAND_BRIDGE_REQUIRED",
        "site_facility_demand_bridge_id",
    )
    direct_present = "tc_site_event_to_design_wind_pressure_ratio" in request
    speed_fields = {
        "tc_peak_gust_3s_10m_mps",
        "qualified_site_design_3s_gust_mps",
    }
    speed_present = speed_fields.intersection(request)
    if direct_present and speed_present:
        raise TropicalCycloneWindSolarV21EvaluationError(
            "SITE_AXIS_PAYLOAD_AMBIGUOUS",
            "supply a direct site pressure ratio or the complete speed proxy, not both",
        )
    flags = ["SITE_FACILITY_T4_DEMAND_BRIDGE"]
    if direct_present:
        ratio = _number(
            request["tc_site_event_to_design_wind_pressure_ratio"],
            "SITE_AXIS_VALUE_INVALID",
            "tc_site_event_to_design_wind_pressure_ratio",
        )
        basis = {
            "input_field": "tc_site_event_to_design_wind_pressure_ratio",
            "site_facility_demand_bridge_id": bridge_id,
        }
    else:
        if speed_present != speed_fields:
            raise TropicalCycloneWindSolarV21EvaluationError(
                "SITE_AXIS_PAYLOAD_REQUIRED",
                "the speed proxy requires event and qualified design 10 m 3-second gusts",
            )
        event_speed = _number(
            request.get("tc_peak_gust_3s_10m_mps"),
            "SITE_AXIS_VALUE_INVALID",
            "tc_peak_gust_3s_10m_mps",
        )
        design_speed = _number(
            request.get("qualified_site_design_3s_gust_mps"),
            "SITE_AXIS_VALUE_INVALID",
            "qualified_site_design_3s_gust_mps",
        )
        if event_speed < 0 or design_speed <= 0:
            raise TropicalCycloneWindSolarV21EvaluationError(
                "SITE_AXIS_VALUE_INVALID",
                "event gust must be nonnegative and design gust positive",
            )
        ratio = (event_speed / design_speed) ** 2
        basis = {
            "input_field": "tc_peak_gust_3s_10m_mps",
            "event_speed_mps": event_speed,
            "qualified_design_speed_mps": design_speed,
            "conversion": "(event/design)^2",
            "site_facility_demand_bridge_id": bridge_id,
        }
        flags.append("SITE_GUST_SQUARED_PRESSURE_PROXY_USED")
    if ratio < 0 or ratio > 2:
        raise TropicalCycloneWindSolarV21EvaluationError(
            "SITE_AXIS_OUTSIDE_VALID_RANGE",
            "site facility demand ratio must be within [0,2]",
        )
    basis.update(
        {
            "axis_id": "site_facility_tropical_cyclone_wind_demand_ratio",
            "axis_value": ratio,
            "valid_range": [0.0, 2.0],
        }
    )
    return ratio, basis, flags


def _common_result(
    artifact: Mapping[str, Any],
    failure_unit_id: str,
    axis: float,
    flags: list[str],
) -> dict[str, Any]:
    pathway = v20._pathway(artifact)
    record = v20._record(pathway, failure_unit_id)
    if record is None:
        raise TropicalCycloneWindSolarV21EvaluationError(
            "CURVE_PAYLOAD_INVALID", f"missing v2.1 common-unit record for {failure_unit_id}"
        )
    unit = next(item for item in artifact["failure_units"] if item["id"] == failure_unit_id)
    evaluated = v20.evaluate_ordered_damage_state_record(record, axis)
    return {
        "pathway_id": PATHWAY,
        "failure_unit_id": failure_unit_id,
        "curve_id": record["curve_id"],
        "subsystem": unit["subsystem"],
        "component": unit["component"],
        "status": "conditional",
        "scalar_central_dr": evaluated["central_screening"]["damage_ratio"],
        "scenario_drs": {
            scenario_id: values["damage_ratio"]
            for scenario_id, values in evaluated.items()
        },
        "state_probabilities_by_scenario": {
            scenario_id: values["state_probabilities"]
            for scenario_id, values in evaluated.items()
        },
        "withheld_reason_codes": [],
        "metadata_flags": list(dict.fromkeys(flags)),
    }


def _clean_v20_emit(
    artifact: Mapping[str, Any],
    emit: dict[str, Any],
    verified_artifact_sha256_hex: str | None,
) -> dict[str, Any]:
    cleaned = deepcopy(emit)
    cleaned["damage_code_id"] = artifact["damage_code_id"]
    cleaned["model_version"] = artifact["semantic_damage_model_version"]
    cleaned["capability_declaration_ref"] = _capability_ref(
        artifact, verified_artifact_sha256_hex
    )
    quality_flags = [
        flag
        for flag in cleaned.get("input_quality", {}).get("limitation_flags", [])
        if flag not in STALE_LIMITATION_FLAGS
    ]
    release_flag = (
        "CANONICAL_SCREENING_RELEASE"
        if artifact.get("canonical_runtime_artifact") is True
        and artifact.get("documentation_revision") == "docs r2"
        else "NONCANONICAL_MODEL_V2_1"
    )
    quality_flags.extend(
        [
            "SCREENING_ENGINEERING_PROXY",
            "TC_NUMERICAL_RESPONSE_NOT_CALIBRATED",
            release_flag,
        ]
    )
    quality_flags = list(dict.fromkeys(quality_flags))
    cleaned["input_quality"] = {"limitation_flags": quality_flags}
    for result in cleaned["failure_unit_results"]:
        result["metadata_flags"] = list(
            dict.fromkeys(
                [
                    flag
                    for flag in result.get("metadata_flags", [])
                    if flag not in STALE_LIMITATION_FLAGS
                ]
                + quality_flags
            )
        )
    return cleaned


def _array_unit_results(
    artifact: Mapping[str, Any],
    request: Mapping[str, Any],
    verified_artifact_sha256_hex: str | None,
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any], dict[str, Any]]:
    architecture = request.get("array_architecture")
    if architecture not in {FIXED, TRACKER}:
        raise TropicalCycloneWindSolarV21EvaluationError(
            "FULL_PLANT_ARCHITECTURE_UNSUPPORTED",
            "full-plant screening supports fixed tilt or qualified tracker, not Perry",
        )
    stripped = {
        key: value
        for key, value in request.items()
        if key not in SITE_AXIS_FIELDS | ASSEMBLY_FIELDS
    }
    results: list[dict[str, Any]] = []
    representative_emit: dict[str, Any] | None = None
    for unit_id in v20.ARCHITECTURE_UNITS[architecture]:
        unit_request = dict(stripped)
        unit_request["failure_unit_id"] = unit_id
        raw = v20.evaluate_damage_call(
            artifact,
            unit_request,
            verified_artifact_sha256_hex=verified_artifact_sha256_hex,
            allow_canonical_runtime_artifact=True,
        )
        cleaned = _clean_v20_emit(artifact, raw, verified_artifact_sha256_hex)
        results.extend(cleaned["failure_unit_results"])
        representative_emit = cleaned
    if representative_emit is None:
        raise AssertionError("architecture has no active array units")
    return (
        results,
        representative_emit["hazard_input_used"],
        representative_emit["selectors_used"],
        representative_emit["conditioners_used"],
    )


def _assemble_reference_profile(
    artifact: Mapping[str, Any],
    damage_emit: Mapping[str, Any],
    *,
    capacity_kwdc: float | None,
    verified_artifact_sha256_hex: str | None,
) -> dict[str, Any]:
    architecture = damage_emit["selectors_used"]["array_architecture"]
    active_module, active_structure = v20.ARCHITECTURE_UNITS[architecture]
    active_values = {
        active_module: REFERENCE_VALUES_PER_KWDC[active_module],
        active_structure: REFERENCE_VALUES_PER_KWDC[active_structure],
        **{unit: REFERENCE_VALUES_PER_KWDC[unit] for unit in COMMON_CURVE_UNITS},
    }
    result_map = {
        item["failure_unit_id"]: item for item in damage_emit["failure_unit_results"]
    }
    if set(result_map) != set(active_values):
        raise TropicalCycloneWindSolarV21EvaluationError(
            "ASSEMBLY_COVERAGE_INCOMPLETE",
            "full-plant assembly requires every direct/civil reference unit exactly once",
        )
    scenario_ids = set.intersection(
        *(set(item["scenario_drs"]) for item in result_map.values())
    )
    if scenario_ids != {"lower_resistance", "central_screening", "upper_resistance"}:
        raise TropicalCycloneWindSolarV21EvaluationError(
            "ASSEMBLY_SCENARIOS_MISMATCH", "unit scenario sets do not reconcile"
        )
    direct_reference_value = sum(active_values.values())
    support_value = REFERENCE_VALUES_PER_KWDC[SUPPORT_UNIT]
    if not math.isclose(
        direct_reference_value + support_value,
        PHYSICAL_REPLACEMENT_VALUE_PER_KWDC,
        rel_tol=0,
        abs_tol=1e-9,
    ):
        raise AssertionError("reference physical-value profile does not reconcile")
    scenario_results: dict[str, Any] = {}
    for scenario_id in sorted(scenario_ids):
        unit_losses = {
            unit: value * result_map[unit]["scenario_drs"][scenario_id]
            for unit, value in active_values.items()
        }
        direct_loss_per_kwdc = sum(unit_losses.values())
        support_dr = direct_loss_per_kwdc / direct_reference_value
        support_loss_per_kwdc = support_value * support_dr
        physical_loss_per_kwdc = direct_loss_per_kwdc + support_loss_per_kwdc
        scenario_result: dict[str, Any] = {
            "unit_loss_2024_usd_per_kwdc": unit_losses,
            "direct_and_civil_loss_2024_usd_per_kwdc": direct_loss_per_kwdc,
            "replacement_support_dr": support_dr,
            "replacement_support_loss_2024_usd_per_kwdc": support_loss_per_kwdc,
            "physical_loss_2024_usd_per_kwdc": physical_loss_per_kwdc,
            "physical_replacement_dr": (
                physical_loss_per_kwdc / PHYSICAL_REPLACEMENT_VALUE_PER_KWDC
            ),
            "installed_capex_physical_loss_fraction": (
                physical_loss_per_kwdc / INSTALLED_CAPEX_PER_KWDC
            ),
        }
        if capacity_kwdc is not None:
            scenario_result["scenario_physical_loss_2024_usd"] = (
                physical_loss_per_kwdc * capacity_kwdc
            )
        scenario_results[scenario_id] = scenario_result
    return {
        "schema_version": "physical_damage_assembly.v1",
        "cell_id": artifact["cell_id"],
        "damage_code_id": artifact["damage_code_id"],
        "model_version": artifact["semantic_damage_model_version"],
        "documentation_revision": artifact["documentation_revision"],
        "artifact_schema_version": artifact["schema_version"],
        "artifact_sha256": verified_artifact_sha256_hex,
        "pathway_id": PATHWAY,
        "array_architecture": architecture,
        "value_profile": {
            "value_profile_id": REFERENCE_PROFILE_ID,
            "currency_basis": "2024 USD",
            "value_unit": "USD_per_kWdc",
            "unit_values": active_values,
            "replacement_support_value": support_value,
            "physical_replacement_value": PHYSICAL_REPLACEMENT_VALUE_PER_KWDC,
            "installed_capex": INSTALLED_CAPEX_PER_KWDC,
            "capacity_kwdc": capacity_kwdc,
        },
        "coverage": {
            "physical_replacement_value_fraction": 1.0,
            "intrinsic_curve_value_fraction": (
                direct_reference_value / PHYSICAL_REPLACEMENT_VALUE_PER_KWDC
            ),
            "derived_support_value_fraction": (
                support_value / PHYSICAL_REPLACEMENT_VALUE_PER_KWDC
            ),
            "excluded_soft_nonphysical_value_2024_usd_per_kwdc": (
                EXCLUDED_SOFT_NONPHYSICAL_VALUE_PER_KWDC
            ),
        },
        "support_allocation_rule": (
            "replacement-support DR equals the value-weighted direct-and-civil DR once; "
            "support is not independently damaged or double-counted"
        ),
        "scenario_results": scenario_results,
        "limitation_flags": [
            "SCREENING_ENGINEERING_PROXY",
            "NAMED_REFERENCE_VALUE_PROFILE_USED",
            "T4_COMMON_UNIT_CURVES_NOT_CALIBRATED",
            "REPRESENTATIVE_ARRAY_ZONE_APPLIED_TO_FULL_ARRAY_VALUE",
            "WIND_ONLY_RAIN_DEBRIS_SURGE_AND_TORNADO_EXCLUDED",
            "ANNUAL_AND_TAIL_METRICS_CONSUMER_OWNED",
        ],
    }


def evaluate_damage_call(
    artifact: Mapping[str, Any],
    request: Mapping[str, Any],
    *,
    verified_artifact_sha256_hex: str | None = None,
) -> dict[str, Any]:
    if artifact.get("semantic_damage_model_version") != "model v2.1":
        raise TropicalCycloneWindSolarV21EvaluationError(
            "MODEL_VERSION_MISMATCH", "v2.1 evaluator requires model v2.1"
        )
    canonical = artifact.get("canonical_runtime_artifact")
    expected_damage_code_id = (
        "TROPICAL_CYCLONE_WIND_SOLAR_SCREENING_COMPLETE_V2_1"
        if canonical is True
        else "TROPICAL_CYCLONE_WIND_SOLAR_SCREENING_COMPLETE_V2_1_PROPOSED"
    )
    if canonical not in {False, True} or artifact.get("damage_code_id") != expected_damage_code_id:
        raise TropicalCycloneWindSolarV21EvaluationError(
            "CURVE_PAYLOAD_INVALID",
            "v2.1 evaluator requires the exact proposed or canonical artifact identity",
        )
    if request.get("pathway_id") != PATHWAY:
        code = "PATHWAY_ID_REQUIRED" if not request.get("pathway_id") else "PATHWAY_ID_UNKNOWN"
        raise TropicalCycloneWindSolarV21EvaluationError(code, f"pathway_id must be {PATHWAY}")
    requested = request.get("failure_unit_id")
    output_mode = request.get("output_mode")
    if output_mode == "full_plant_screening":
        if requested is not None:
            raise TropicalCycloneWindSolarV21EvaluationError(
                "REQUEST_FIELD_UNSUPPORTED", "omit failure_unit_id for full-plant screening"
            )
        if request.get("value_profile_id") != REFERENCE_PROFILE_ID:
            raise TropicalCycloneWindSolarV21EvaluationError(
                "VALUE_PROFILE_UNSUPPORTED", f"value_profile_id must be {REFERENCE_PROFILE_ID}"
            )
        if request.get("array_exposure_basis") != "representative_site_array_zone":
            raise TropicalCycloneWindSolarV21EvaluationError(
                "ARRAY_EXPOSURE_BASIS_REQUIRED",
                "array_exposure_basis must be representative_site_array_zone",
            )
        capacity_kwdc: float | None = None
        if "capacity_kwdc" in request:
            capacity_kwdc = _number(
                request["capacity_kwdc"], "CAPACITY_VALUE_INVALID", "capacity_kwdc"
            )
            if capacity_kwdc <= 0:
                raise TropicalCycloneWindSolarV21EvaluationError(
                    "CAPACITY_VALUE_INVALID", "capacity_kwdc must be positive"
                )
        array_results, array_basis, selectors, conditioners = _array_unit_results(
            artifact, request, verified_artifact_sha256_hex
        )
        site_axis, site_basis, site_flags = _site_axis(request)
        common_flags = [
            "SCREENING_ENGINEERING_PROXY",
            "TC_NUMERICAL_RESPONSE_NOT_CALIBRATED",
            "T4_COMMON_UNIT_CURVES_NOT_CALIBRATED",
            *site_flags,
        ]
        common_results = [
            _common_result(artifact, unit, site_axis, common_flags)
            for unit in COMMON_CURVE_UNITS
        ]
        limitation_flags = list(
            dict.fromkeys(
                [
                    *next(iter(array_results))["metadata_flags"],
                    *common_flags,
                    "NAMED_REFERENCE_VALUE_PROFILE_USED",
                    "REPRESENTATIVE_ARRAY_ZONE_APPLIED_TO_FULL_ARRAY_VALUE",
                    "WIND_ONLY_RAIN_DEBRIS_SURGE_AND_TORNADO_EXCLUDED",
                ]
            )
        )
        damage_emit = {
            "schema_version": "damage_emit.v2",
            "cell_id": artifact["cell_id"],
            "damage_code_id": artifact["damage_code_id"],
            "model_version": artifact["semantic_damage_model_version"],
            "pathway_id": PATHWAY,
            "emit_mode": "state_ensemble",
            "hazard_input_used": {
                "event_id": request["event_id"],
                "event_family_id": request["event_family_id"],
                "array_axis": array_basis,
                "site_facility_axis": site_basis,
            },
            "input_quality": {"limitation_flags": limitation_flags},
            "selectors_used": selectors,
            "conditioners_used": conditioners,
            "exposure_used": {
                "array_exposure_basis": request["array_exposure_basis"],
                "value_profile_id": request["value_profile_id"],
            },
            "failure_unit_results": [*array_results, *common_results],
            "capability_declaration_ref": _capability_ref(
                artifact, verified_artifact_sha256_hex
            ),
        }
        assembly = _assemble_reference_profile(
            artifact,
            damage_emit,
            capacity_kwdc=capacity_kwdc,
            verified_artifact_sha256_hex=verified_artifact_sha256_hex,
        )
        return {
            "output_mode": "full_plant_screening",
            "damage_emit": damage_emit,
            "physical_damage_assembly": assembly,
        }
    if output_mode is not None:
        raise TropicalCycloneWindSolarV21EvaluationError(
            "OUTPUT_MODE_UNSUPPORTED", "output_mode must be full_plant_screening or omitted"
        )
    if requested in COMMON_CURVE_UNITS:
        allowed = (
            v20.WITHHELD_DIRECT_REQUEST_FIELDS
            | SITE_AXIS_FIELDS
        )
        v20._reject_unknown_fields(request, allowed)
        v20._require_event_identity(request)
        site_axis, site_basis, site_flags = _site_axis(request)
        flags = [
            "SCREENING_ENGINEERING_PROXY",
            "TC_NUMERICAL_RESPONSE_NOT_CALIBRATED",
            "T4_COMMON_UNIT_CURVES_NOT_CALIBRATED",
            *site_flags,
        ]
        conditioners = v20._compound_conditioners(request, flags, architecture=None)
        result = _common_result(artifact, requested, site_axis, flags)
        return {
            "schema_version": "damage_emit.v2",
            "cell_id": artifact["cell_id"],
            "damage_code_id": artifact["damage_code_id"],
            "model_version": artifact["semantic_damage_model_version"],
            "pathway_id": PATHWAY,
            "emit_mode": "state_ensemble",
            "hazard_input_used": {
                "event_id": request["event_id"],
                "event_family_id": request["event_family_id"],
                **site_basis,
            },
            "input_quality": {"limitation_flags": flags},
            "selectors_used": {"failure_unit_id": requested},
            "conditioners_used": conditioners,
            "failure_unit_results": [result],
            "capability_declaration_ref": _capability_ref(
                artifact, verified_artifact_sha256_hex
            ),
        }
    if requested == SUPPORT_UNIT:
        raise TropicalCycloneWindSolarV21EvaluationError(
            "DERIVED_ASSEMBLY_RULE_ONLY",
            "replacement support is emitted only through full_plant_screening assembly",
        )
    if requested is None:
        raise TropicalCycloneWindSolarV21EvaluationError(
            "OUTPUT_MODE_REQUIRED",
            "supply one failure_unit_id or output_mode=full_plant_screening",
        )
    stripped = {
        key: value
        for key, value in request.items()
        if key not in SITE_AXIS_FIELDS | ASSEMBLY_FIELDS
    }
    raw = v20.evaluate_damage_call(
        artifact,
        stripped,
        verified_artifact_sha256_hex=verified_artifact_sha256_hex,
        allow_canonical_runtime_artifact=True,
    )
    return _clean_v20_emit(artifact, raw, verified_artifact_sha256_hex)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact")
    parser.add_argument("request_json")
    args = parser.parse_args()
    artifact = load_artifact(args.artifact)
    request = json.loads(args.request_json)
    pin = request.pop("artifact_pin", None)
    if not isinstance(pin, Mapping):
        raise TropicalCycloneWindSolarV21EvaluationError(
            "ARTIFACT_PIN_INCOMPLETE", "CLI request must carry an exact artifact_pin"
        )
    digest = v20.artifact_sha256(args.artifact)
    v20.verify_artifact_pin(artifact, pin, artifact_sha256_hex=digest)
    print(
        json.dumps(
            evaluate_damage_call(
                artifact, request, verified_artifact_sha256_hex=digest
            ),
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
