#!/usr/bin/env python3
"""Reference evaluator for the proposed TC-wind x solar model-v2 package.

The generic fixed-tilt and tracker records are an explicitly synthetic Tier-4
coverage experiment.  They are not calibrated hurricane fragilities and this
helper is not a promoted runtime API.  The Perry compatibility route preserves
the source-specific model-v1 curve without relabelling it as generic.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any, Mapping, Sequence


PATHWAY = "tropical_cyclone_wind"
PERRY = "perry_ground_nontracking_source_cohort_v1_compat"
FIXED = "fixed_tilt_ground_mount_tc_synthetic_t4_v1"
TRACKER = "single_axis_tracker_tc_qualified_synthetic_t4_v1"
PERRY_UNIT = "PV_PERRY_GROUND_FIXED_VISIBLE_MODULE_HARDWARE_SOURCE_UNIT"
ARCHITECTURE_UNITS = {
    PERRY: (PERRY_UNIT,),
    FIXED: ("PV_FIXED_TILT_MODULE_FIELD", "PV_FIXED_TILT_SUPPORT_STRUCTURE"),
    TRACKER: ("PV_TRACKER_MODULE_FIELD", "PV_TRACKER_SBOS_ASSEMBLY"),
}
COMMON_WITHHELD_UNITS = (
    "PV_FOUNDATION",
    "PV_POWER_CONVERSION_AND_COLLECTION",
    "PV_GSU_SUBSTATION",
    "PV_SCADA_COMMUNICATIONS",
    "PV_CIVIL_INFRA",
    "PV_REPLACEMENT_SUPPORT",
)
PERRY_SELECTORS = {
    "array_architecture_id": "PERRY_GROUND_NONTRACKING_SOURCE_COHORT_V1",
    "source_population_match_id": "PERRY_MANUAL_GROUND_NONTRACKING_MIXED_SCALE_V1",
    "module_value_distribution_assumption_id": "UNIFORM_MODULE_HARDWARE_VALUE",
    "visible_damage_disposition_assumption_id": "FULL_REPLACEMENT_IF_VISIBLE_OR_MISSING",
    "source_wind_product_id": "PERRY_DATASET_REPORTED_EVENT_MAX_GUST",
    "causal_scope_acknowledgement_id": "SOURCE_COMPOSITE_HURRICANE_MODULE_LOSS",
}
VALUE_FIELDS = frozenset(
    {
        "value_basis",
        "direct_replacement_value_usd",
        "module_value",
        "structure_value",
        "full_tiv_usd",
        "installed_cost_usd",
        "replacement_value_usd",
        "site_replacement_value_usd",
        "value_usd",
        "tiv_usd",
        "scenario_loss_requested",
        "exposure_fraction",
        "at_risk_fraction",
        "array_exposure_fraction",
        "exposed_fraction",
    }
)
COMMON_REQUEST_FIELDS = frozenset(
    {
        "event_id",
        "event_family_id",
        "pathway_id",
        "array_architecture",
        "failure_unit_id",
        "tc_duration_class",
        "tc_direction_evolution_class",
        "rain_ingress_indicator",
        "windborne_debris_indicator",
        "flood_or_surge_indicator",
        "tc_tornado_indicator",
        "compound_reconciliation_acknowledgement_id",
    }
)
FIXED_REQUEST_FIELDS = COMMON_REQUEST_FIELDS | {
    "tc_fixed_event_to_design_net_pressure_ratio",
    "tc_array_height_3s_gust_mps",
    "qualified_design_array_height_3s_gust_mps",
    "tc_peak_gust_3s_10m_mps",
    "tc_wind_field_bridge_id",
    "tc_directional_history_bridge_id",
    "tc_duration_cycling_bridge_id",
    "aerodynamic_demand_bridge_id",
    "array_zone",
    "array_spatial_object_id",
}
TRACKER_REQUEST_FIELDS = COMMON_REQUEST_FIELDS | {
    "tc_tracker_normal_3s_gust_mps",
    "critical_instability_3s_gust_mps",
    "aeroelastic_qualification_id",
    "aeroelastic_qualification_sha256",
    "tracker_system_id",
    "tracker_module_configuration",
    "tracker_layout_id",
    "tracker_angle_deg",
    "tracker_position_state",
    "stow_confirmation_basis",
    "tracker_drive_lock_state",
    "array_zone",
    "array_spatial_object_id",
    "tc_wind_field_bridge_id",
    "tc_directional_history_bridge_id",
    "tc_duration_cycling_bridge_id",
    "qualification_tracker_system_id",
    "qualification_tracker_module_configuration",
    "qualification_tracker_layout_id",
    "qualification_tracker_angle_deg",
    "qualification_tracker_position_state",
    "qualification_array_zone",
    "qualification_drive_lock_state",
    "qualification_speed_averaging_s",
    "qualification_speed_reference",
    "qualification_tc_wind_field_bridge_id",
    "qualification_direction_basis_id",
    "qualification_duration_basis_id",
}
PERRY_REQUEST_FIELDS = COMMON_REQUEST_FIELDS | {
    "perry_event_max_gust_mps",
    *PERRY_SELECTORS,
}
WITHHELD_DIRECT_REQUEST_FIELDS = (
    COMMON_REQUEST_FIELDS - {"array_architecture"}
)
FAILURE_CODES = frozenset(
    {
        "AERODYNAMIC_DEMAND_BRIDGE_REQUIRED",
        "ARCHITECTURE_AXIS_MISMATCH",
        "ARRAY_ARCHITECTURE_REQUIRED",
        "ARRAY_ARCHITECTURE_UNSUPPORTED",
        "ARRAY_SPATIAL_OBJECT_ID_REQUIRED",
        "ARRAY_ZONE_REQUIRED",
        "ARTIFACT_PIN_INCOMPLETE",
        "ARTIFACT_PIN_MISMATCH",
        "AXIS_OUTSIDE_VALID_RANGE",
        "AXIS_PAYLOAD_REQUIRED",
        "AXIS_VALUE_INVALID",
        "COMPOUND_RECONCILIATION_REQUIRED",
        "CONDITIONER_VALUE_UNSUPPORTED",
        "CURVE_FORM_UNSUPPORTED",
        "CURVE_PAYLOAD_INVALID",
        "CURVE_RECORD_NOT_UNIQUE",
        "EVENT_FAMILY_ID_REQUIRED",
        "EVENT_ID_REQUIRED",
        "FAILURE_UNIT_ID_UNKNOWN",
        "FAILURE_UNIT_NOT_APPLICABLE_TO_ARCHITECTURE",
        "PATHWAY_ID_REQUIRED",
        "PATHWAY_ID_UNKNOWN",
        "PERRY_COMPOSITE_PATHWAY_OVERLAP_UNRESOLVED",
        "PRESSURE_INDEX_REQUIRED",
        "QUALIFIED_DESIGN_GUST_REQUIRED",
        "REQUEST_FIELD_UNSUPPORTED",
        "SCENARIO_LOSS_WITHHELD_SYNTHETIC_T4_PROPOSAL",
        "SELECTOR_MISMATCH",
        "SELECTOR_REQUIRED",
        "TC_WIND_BRIDGE_REQUIRED",
        "TRACKER_QUALIFICATION_BASIS_MISMATCH",
        "UNBRIDGED_TEN_METER_GUST_PROHIBITED",
    }
)


class TropicalCycloneWindSolarV2EvaluationError(ValueError):
    """Fail-closed error carrying a stable reason code."""

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
    if re.fullmatch(r"[0-9a-f]{64}", artifact_sha256_hex) is None:
        raise TropicalCycloneWindSolarV2EvaluationError(
            "ARTIFACT_PIN_MISMATCH", "verified artifact SHA must be 64 lowercase hexadecimal characters"
        )
    expected = {
        "cell_id": artifact["cell_id"],
        "semantic_damage_model_version": artifact["semantic_damage_model_version"],
        "documentation_revision": artifact["documentation_revision"],
        "schema_version": artifact["schema_version"],
        "artifact_sha256": artifact_sha256_hex,
    }
    if set(pin) != set(expected):
        raise TropicalCycloneWindSolarV2EvaluationError(
            "ARTIFACT_PIN_INCOMPLETE",
            "pin must contain exactly cell, model, docs, schema, and SHA",
        )
    mismatches = [key for key, value in expected.items() if pin[key] != value]
    if mismatches:
        raise TropicalCycloneWindSolarV2EvaluationError(
            "ARTIFACT_PIN_MISMATCH", "pin mismatch for " + ", ".join(mismatches)
        )


def _number(value: Any, code: str, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TropicalCycloneWindSolarV2EvaluationError(code, f"{field} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise TropicalCycloneWindSolarV2EvaluationError(code, f"{field} must be finite")
    return result


def _text(value: Any, code: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise TropicalCycloneWindSolarV2EvaluationError(code, f"{field} must be non-empty")
    return value


def _reject_unknown_fields(request: Mapping[str, Any], allowed: frozenset[str] | set[str]) -> None:
    unknown = sorted(set(request) - set(allowed) - set(VALUE_FIELDS))
    if unknown:
        raise TropicalCycloneWindSolarV2EvaluationError(
            "REQUEST_FIELD_UNSUPPORTED",
            "undeclared or foreign-route request fields: " + ", ".join(unknown),
        )


def _normal_cdf(value: float) -> float:
    return 0.5 * math.erfc(-value / math.sqrt(2.0))


def _state_probabilities(
    x: float,
    *,
    beta_ln: float,
    medians: Sequence[float],
    state_ids: Sequence[str],
) -> dict[str, float]:
    if x < 0:
        raise TropicalCycloneWindSolarV2EvaluationError(
            "AXIS_OUTSIDE_VALID_RANGE", "demand index cannot be negative"
        )
    if x == 0:
        return {
            state_id: 1.0 if index == 0 else 0.0
            for index, state_id in enumerate(state_ids)
        }
    exceedance = [_normal_cdf(math.log(x / median) / beta_ln) for median in medians]
    exact = [1.0 - exceedance[0]]
    exact.extend(
        exceedance[index] - exceedance[index + 1]
        for index in range(len(exceedance) - 1)
    )
    exact.append(exceedance[-1])
    if any(value < -1e-14 for value in exact):
        raise TropicalCycloneWindSolarV2EvaluationError(
            "CURVE_PAYLOAD_INVALID", "ordered-state probability became negative"
        )
    exact = [min(1.0, max(0.0, value)) for value in exact]
    total = sum(exact)
    if not math.isclose(total, 1.0, rel_tol=0, abs_tol=1e-12):
        raise TropicalCycloneWindSolarV2EvaluationError(
            "CURVE_PAYLOAD_INVALID", "state probabilities do not sum to one"
        )
    exact[0] += 1.0 - total
    return dict(zip(state_ids, exact, strict=True))


def evaluate_ordered_damage_state_record(
    record: Mapping[str, Any], x: float
) -> dict[str, dict[str, Any]]:
    if record.get("curve_form") != "ordered_damage_state_lognormal":
        raise TropicalCycloneWindSolarV2EvaluationError(
            "CURVE_FORM_UNSUPPORTED", "record is not ordered_damage_state_lognormal"
        )
    parameters = record["parameters"]
    if "zero_below" in parameters:
        raise TropicalCycloneWindSolarV2EvaluationError(
            "CURVE_PAYLOAD_INVALID",
            "v2 prohibits a synthetic hard-zero threshold; only x=0 is exact zero",
        )
    beta = _number(parameters.get("beta_ln"), "CURVE_PAYLOAD_INVALID", "beta_ln")
    if beta <= 0:
        raise TropicalCycloneWindSolarV2EvaluationError(
            "CURVE_PAYLOAD_INVALID", "beta_ln must be positive"
        )
    states = parameters["damage_states"]
    state_ids = [state["state_id"] for state in states]
    costs = [
        _number(state["cost_ratio"], "CURVE_PAYLOAD_INVALID", "cost_ratio")
        for state in states
    ]
    output: dict[str, dict[str, Any]] = {}
    for scenario in parameters["capacity_scenarios"]:
        medians = [
            _number(value, "CURVE_PAYLOAD_INVALID", "state median")
            for value in scenario["state_medians"]
        ]
        if len(medians) != len(states) - 1 or any(
            left >= right for left, right in zip(medians, medians[1:])
        ):
            raise TropicalCycloneWindSolarV2EvaluationError(
                "CURVE_PAYLOAD_INVALID", "state medians are incomplete or unordered"
            )
        probabilities = _state_probabilities(
            x, beta_ln=beta, medians=medians, state_ids=state_ids
        )
        dr = sum(
            probabilities[state_id] * cost
            for state_id, cost in zip(state_ids, costs, strict=True)
        )
        output[scenario["scenario_id"]] = {
            "damage_ratio": min(1.0, max(0.0, dr)),
            "state_probabilities": probabilities,
        }
    return output


def _piecewise_points(record: Mapping[str, Any]) -> list[tuple[float, float]]:
    if record.get("curve_form") != "piecewise_linear":
        raise TropicalCycloneWindSolarV2EvaluationError(
            "CURVE_FORM_UNSUPPORTED", "Perry record must be piecewise_linear"
        )
    raw = record.get("parameters", {}).get("points")
    if not isinstance(raw, list) or len(raw) != 13:
        raise TropicalCycloneWindSolarV2EvaluationError(
            "CURVE_PAYLOAD_INVALID", "Perry compatibility route must retain 13 knots"
        )
    points: list[tuple[float, float]] = []
    for index, point in enumerate(raw):
        if not isinstance(point, list) or len(point) != 2:
            raise TropicalCycloneWindSolarV2EvaluationError(
                "CURVE_PAYLOAD_INVALID", f"Perry point {index} is malformed"
            )
        x = _number(point[0], "CURVE_PAYLOAD_INVALID", f"point[{index}].x")
        y = _number(point[1], "CURVE_PAYLOAD_INVALID", f"point[{index}].y")
        if not 0 <= y <= 1 or (points and (x <= points[-1][0] or y < points[-1][1])):
            raise TropicalCycloneWindSolarV2EvaluationError(
                "CURVE_PAYLOAD_INVALID", "Perry knots must be increasing and monotone"
            )
        points.append((x, y))
    if points[0][0] != 17.4 or points[-1][0] != 39.1:
        raise TropicalCycloneWindSolarV2EvaluationError(
            "CURVE_PAYLOAD_INVALID", "Perry range changed"
        )
    return points


def evaluate_piecewise_linear_record(record: Mapping[str, Any], x: float) -> float:
    points = _piecewise_points(record)
    if x < points[0][0] or x > points[-1][0]:
        raise TropicalCycloneWindSolarV2EvaluationError(
            "AXIS_OUTSIDE_VALID_RANGE", "Perry gust is outside 17.4 through 39.1 m/s"
        )
    for knot_x, knot_y in points:
        if x == knot_x:
            return knot_y
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        if x0 < x < x1:
            return y0 + (x - x0) / (x1 - x0) * (y1 - y0)
    raise TropicalCycloneWindSolarV2EvaluationError(
        "CURVE_PAYLOAD_INVALID", "in-range Perry input did not resolve"
    )


def _pathway(artifact: Mapping[str, Any]) -> Mapping[str, Any]:
    matches = [item for item in artifact["pathways"] if item["pathway_id"] == PATHWAY]
    if len(matches) != 1:
        raise TropicalCycloneWindSolarV2EvaluationError(
            "CURVE_PAYLOAD_INVALID", "artifact must declare one TC-wind pathway"
        )
    return matches[0]


def _record(pathway: Mapping[str, Any], failure_unit_id: str) -> Mapping[str, Any] | None:
    matches = [
        item for item in pathway["curve_records"] if item["failure_unit_id"] == failure_unit_id
    ]
    if len(matches) > 1:
        raise TropicalCycloneWindSolarV2EvaluationError(
            "CURVE_RECORD_NOT_UNIQUE", f"multiple records for {failure_unit_id}"
        )
    return matches[0] if matches else None


def _require_event_identity(request: Mapping[str, Any]) -> None:
    _text(request.get("event_id"), "EVENT_ID_REQUIRED", "event_id")
    _text(request.get("event_family_id"), "EVENT_FAMILY_ID_REQUIRED", "event_family_id")


def _compound_conditioners(
    request: Mapping[str, Any], flags: list[str], *, architecture: str | None
) -> dict[str, Any]:
    used: dict[str, Any] = {}
    for field in (
        "rain_ingress_indicator",
        "windborne_debris_indicator",
        "flood_or_surge_indicator",
        "tc_tornado_indicator",
    ):
        value = request.get(field, "unknown")
        if not (isinstance(value, bool) or value == "unknown"):
            raise TropicalCycloneWindSolarV2EvaluationError(
                "CONDITIONER_VALUE_UNSUPPORTED", f"{field} must be true, false, or unknown"
            )
        used[field] = value
    if any(value is True for value in used.values()):
        if architecture == PERRY:
            raise TropicalCycloneWindSolarV2EvaluationError(
                "PERRY_COMPOSITE_PATHWAY_OVERLAP_UNRESOLVED",
                "Perry's source-composite endpoint cannot be partitioned from an identified compound pathway",
            )
        if request.get("compound_reconciliation_acknowledgement_id") != (
            "SEPARATE_PATHWAYS_AND_NO_DOUBLE_COUNT"
        ):
            raise TropicalCycloneWindSolarV2EvaluationError(
                "COMPOUND_RECONCILIATION_REQUIRED",
                "identified compound pathways require explicit separate-pathway acknowledgement",
            )
        flags.append("COMPOUND_PATHWAY_PRESENT_NOT_INCLUDED_IN_WIND_DR")
        used["compound_reconciliation_acknowledgement_id"] = request[
            "compound_reconciliation_acknowledgement_id"
        ]
    for field, allowed in {
        "tc_duration_class": {
            "short_lt_1h",
            "sustained_1_to_6h",
            "extended_gt_6h",
            "unknown",
        },
        "tc_direction_evolution_class": {
            "approximately_unidirectional",
            "evolving",
            "multi_peak_or_eye_passage",
            "unknown",
        },
    }.items():
        value = request.get(field, "unknown")
        if value not in allowed:
            raise TropicalCycloneWindSolarV2EvaluationError(
                "CONDITIONER_VALUE_UNSUPPORTED", f"{field}={value!r} is unsupported"
            )
        if value == "unknown":
            flags.append(f"UNKNOWN_{field.upper()}")
        used[field] = value
    return used


def _axis_limits(x: float, *, architecture: str, flags: list[str]) -> float:
    if x < 0 or x > 2.0:
        raise TropicalCycloneWindSolarV2EvaluationError(
            "AXIS_OUTSIDE_VALID_RANGE", "normalized demand index must be within [0, 2]"
        )
    return x


def _required_tc_bridges(request: Mapping[str, Any]) -> dict[str, str]:
    return {
        field: _text(request.get(field), "TC_WIND_BRIDGE_REQUIRED", field)
        for field in (
            "tc_wind_field_bridge_id",
            "tc_directional_history_bridge_id",
            "tc_duration_cycling_bridge_id",
        )
    }


def _fixed_axis(request: Mapping[str, Any], flags: list[str]) -> tuple[float, dict[str, Any]]:
    if any(
        field in request
        for field in ("tc_tracker_normal_3s_gust_mps", "critical_instability_3s_gust_mps")
    ):
        raise TropicalCycloneWindSolarV2EvaluationError(
            "ARCHITECTURE_AXIS_MISMATCH", "tracker fields cannot route a fixed-tilt call"
        )
    bridges = _required_tc_bridges(request)
    aerodynamic = _text(
        request.get("aerodynamic_demand_bridge_id"),
        "AERODYNAMIC_DEMAND_BRIDGE_REQUIRED",
        "aerodynamic_demand_bridge_id",
    )
    zone = request.get("array_zone")
    if zone not in {"interior", "edge", "corner_or_end_row"}:
        raise TropicalCycloneWindSolarV2EvaluationError(
            "ARRAY_ZONE_REQUIRED", "fixed-tilt array zone must be interior, edge, or corner_or_end_row"
        )
    spatial_object_id = _text(
        request.get("array_spatial_object_id"),
        "ARRAY_SPATIAL_OBJECT_ID_REQUIRED",
        "array_spatial_object_id",
    )
    direct = "tc_fixed_event_to_design_net_pressure_ratio" in request
    proxy = "tc_array_height_3s_gust_mps" in request
    if direct == proxy:
        raise TropicalCycloneWindSolarV2EvaluationError(
            "PRESSURE_INDEX_REQUIRED",
            "provide exactly one qualified pressure ratio or TC array-height gust proxy",
        )
    proxy_companions = {
        "qualified_design_array_height_3s_gust_mps",
        "tc_peak_gust_3s_10m_mps",
    }
    if direct and proxy_companions.intersection(request):
        raise TropicalCycloneWindSolarV2EvaluationError(
            "PRESSURE_INDEX_REQUIRED",
            "direct pressure-ratio mode cannot carry speed-proxy-only companion fields",
        )
    if direct:
        x = _number(
            request["tc_fixed_event_to_design_net_pressure_ratio"],
            "PRESSURE_INDEX_REQUIRED",
            "tc_fixed_event_to_design_net_pressure_ratio",
        )
        basis: dict[str, Any] = {
            "input_field": "tc_fixed_event_to_design_net_pressure_ratio",
            "aerodynamic_demand_bridge_id": aerodynamic,
            **bridges,
            "array_zone": zone,
            "array_spatial_object_id": spatial_object_id,
        }
    else:
        speed = _number(
            request["tc_array_height_3s_gust_mps"],
            "TC_WIND_BRIDGE_REQUIRED",
            "tc_array_height_3s_gust_mps",
        )
        design = _number(
            request.get("qualified_design_array_height_3s_gust_mps"),
            "QUALIFIED_DESIGN_GUST_REQUIRED",
            "qualified_design_array_height_3s_gust_mps",
        )
        if speed < 0 or design <= 0:
            raise TropicalCycloneWindSolarV2EvaluationError(
                "QUALIFIED_DESIGN_GUST_REQUIRED",
                "event gust must be nonnegative and design gust positive",
            )
        x = (speed / design) ** 2
        flags.append("TC_QUASI_STEADY_GUST_SQUARED_PROXY_USED")
        basis = {
            "input_field": "tc_array_height_3s_gust_mps",
            "input_speed_mps": speed,
            "qualified_design_array_height_3s_gust_mps": design,
            "aerodynamic_demand_bridge_id": aerodynamic,
            **bridges,
            "array_zone": zone,
            "array_spatial_object_id": spatial_object_id,
        }
    if "tc_peak_gust_3s_10m_mps" in request:
        source = _number(
            request["tc_peak_gust_3s_10m_mps"],
            "TC_WIND_BRIDGE_REQUIRED",
            "tc_peak_gust_3s_10m_mps",
        )
        if source < 0 or not proxy:
            raise TropicalCycloneWindSolarV2EvaluationError(
                "UNBRIDGED_TEN_METER_GUST_PROHIBITED",
                "10 m gust is context only and requires a separately delivered array-height proxy",
            )
        basis["source_tc_peak_gust_3s_10m_mps"] = source
    return _axis_limits(x, architecture=FIXED, flags=flags), basis


def _tracker_axis(request: Mapping[str, Any], flags: list[str]) -> tuple[float, dict[str, Any]]:
    if any(
        field in request
        for field in (
            "tc_fixed_event_to_design_net_pressure_ratio",
            "qualified_design_array_height_3s_gust_mps",
        )
    ):
        raise TropicalCycloneWindSolarV2EvaluationError(
            "ARCHITECTURE_AXIS_MISMATCH", "fixed fields cannot route a tracker call"
        )
    bridges = _required_tc_bridges(request)
    speed = _number(
        request.get("tc_tracker_normal_3s_gust_mps"),
        "TRACKER_QUALIFICATION_BASIS_MISMATCH",
        "tc_tracker_normal_3s_gust_mps",
    )
    critical = _number(
        request.get("critical_instability_3s_gust_mps"),
        "TRACKER_QUALIFICATION_BASIS_MISMATCH",
        "critical_instability_3s_gust_mps",
    )
    if speed < 0 or critical <= 0:
        raise TropicalCycloneWindSolarV2EvaluationError(
            "TRACKER_QUALIFICATION_BASIS_MISMATCH",
            "tracker-normal gust must be nonnegative and Ucrit positive",
        )
    qualification_id = _text(
        request.get("aeroelastic_qualification_id"),
        "TRACKER_QUALIFICATION_BASIS_MISMATCH",
        "aeroelastic_qualification_id",
    )
    qualification_sha256 = _text(
        request.get("aeroelastic_qualification_sha256"),
        "TRACKER_QUALIFICATION_BASIS_MISMATCH",
        "aeroelastic_qualification_sha256",
    )
    if re.fullmatch(r"[0-9a-f]{64}", qualification_sha256) is None:
        raise TropicalCycloneWindSolarV2EvaluationError(
            "TRACKER_QUALIFICATION_BASIS_MISMATCH",
            "aeroelastic_qualification_sha256 must be 64 lowercase hexadecimal characters",
        )
    system_id = _text(
        request.get("tracker_system_id"),
        "TRACKER_QUALIFICATION_BASIS_MISMATCH",
        "tracker_system_id",
    )
    layout_id = _text(
        request.get("tracker_layout_id"),
        "TRACKER_QUALIFICATION_BASIS_MISMATCH",
        "tracker_layout_id",
    )
    configuration = request.get("tracker_module_configuration")
    if configuration not in {"1P", "2P"}:
        raise TropicalCycloneWindSolarV2EvaluationError(
            "TRACKER_QUALIFICATION_BASIS_MISMATCH",
            "tracker_module_configuration must be 1P or 2P",
        )
    angle = _number(
        request.get("tracker_angle_deg"),
        "TRACKER_QUALIFICATION_BASIS_MISMATCH",
        "tracker_angle_deg",
    )
    position = request.get("tracker_position_state")
    if position not in {"confirmed_wind_stow", "normal_tracking", "drive_or_power_fault"}:
        raise TropicalCycloneWindSolarV2EvaluationError(
            "TRACKER_QUALIFICATION_BASIS_MISMATCH",
            "tracker position must be attained and known; commanded stow is insufficient",
        )
    stow_basis = request.get("stow_confirmation_basis")
    if stow_basis not in {"position_sensor_and_scada", "field_observation"}:
        raise TropicalCycloneWindSolarV2EvaluationError(
            "TRACKER_QUALIFICATION_BASIS_MISMATCH",
            "attained position requires sensor/SCADA or field observation",
        )
    drive = request.get("tracker_drive_lock_state")
    if drive not in {"drive_engaged", "mechanically_locked", "unlocked_or_free"}:
        raise TropicalCycloneWindSolarV2EvaluationError(
            "TRACKER_QUALIFICATION_BASIS_MISMATCH", "tracker drive/lock state must be known"
        )
    zone = request.get("array_zone")
    if zone not in {"interior", "edge", "corner_or_end_row"}:
        raise TropicalCycloneWindSolarV2EvaluationError(
            "TRACKER_QUALIFICATION_BASIS_MISMATCH", "tracker array zone must be known"
        )
    spatial_object_id = _text(
        request.get("array_spatial_object_id"),
        "ARRAY_SPATIAL_OBJECT_ID_REQUIRED",
        "array_spatial_object_id",
    )
    expected = {
        "qualification_tracker_system_id": system_id,
        "qualification_tracker_module_configuration": configuration,
        "qualification_tracker_layout_id": layout_id,
        "qualification_tracker_position_state": position,
        "qualification_array_zone": zone,
        "qualification_drive_lock_state": drive,
        "qualification_speed_reference": "array_height_tracker_normal_3s_gust",
        "qualification_tc_wind_field_bridge_id": bridges["tc_wind_field_bridge_id"],
        "qualification_direction_basis_id": bridges["tc_directional_history_bridge_id"],
        "qualification_duration_basis_id": bridges["tc_duration_cycling_bridge_id"],
    }
    mismatches = [field for field, value in expected.items() if request.get(field) != value]
    qualification_angle = _number(
        request.get("qualification_tracker_angle_deg"),
        "TRACKER_QUALIFICATION_BASIS_MISMATCH",
        "qualification_tracker_angle_deg",
    )
    averaging = _number(
        request.get("qualification_speed_averaging_s"),
        "TRACKER_QUALIFICATION_BASIS_MISMATCH",
        "qualification_speed_averaging_s",
    )
    if not math.isclose(angle, qualification_angle, rel_tol=0, abs_tol=1e-9):
        mismatches.append("qualification_tracker_angle_deg")
    if not math.isclose(averaging, 3.0, rel_tol=0, abs_tol=1e-12):
        mismatches.append("qualification_speed_averaging_s")
    if mismatches:
        raise TropicalCycloneWindSolarV2EvaluationError(
            "TRACKER_QUALIFICATION_BASIS_MISMATCH",
            "qualification mismatch for " + ", ".join(sorted(mismatches)),
        )
    x = speed / critical
    if x >= 0.75:
        flags.append("STOW_ACTION_THRESHOLD_EXCEEDED_NOT_DAMAGE_ONSET")
    flags.append("QUALIFIED_TRACKER_INSTABILITY_AXIS")
    flags.append("QUALIFICATION_CONTENT_NOT_RESOLVED_BY_REFERENCE_EVALUATOR")
    return _axis_limits(x, architecture=TRACKER, flags=flags), {
        "input_field": "tc_tracker_normal_3s_gust_mps",
        "input_speed_mps": speed,
        "critical_instability_3s_gust_mps": critical,
        "aeroelastic_qualification_id": qualification_id,
        "aeroelastic_qualification_sha256": qualification_sha256,
        "tracker_system_id": system_id,
        "tracker_layout_id": layout_id,
        "tracker_module_configuration": configuration,
        "tracker_angle_deg": angle,
        "tracker_position_state": position,
        "stow_confirmation_basis": stow_basis,
        "tracker_drive_lock_state": drive,
        "array_zone": zone,
        "array_spatial_object_id": spatial_object_id,
        "qualification_basis_match": True,
        **bridges,
    }


def _perry_axis(
    request: Mapping[str, Any], record: Mapping[str, Any]
) -> tuple[float, dict[str, Any], float]:
    for field, expected in PERRY_SELECTORS.items():
        if request.get(field) != expected:
            code = "SELECTOR_REQUIRED" if field not in request else "SELECTOR_MISMATCH"
            raise TropicalCycloneWindSolarV2EvaluationError(code, f"{field} must equal {expected}")
    if "perry_event_max_gust_mps" not in request:
        raise TropicalCycloneWindSolarV2EvaluationError(
            "AXIS_PAYLOAD_REQUIRED", "perry_event_max_gust_mps is required"
        )
    x = _number(
        request["perry_event_max_gust_mps"],
        "AXIS_VALUE_INVALID",
        "perry_event_max_gust_mps",
    )
    dr = evaluate_piecewise_linear_record(record, x)
    return x, {
        "input_field": "perry_event_max_gust_mps",
        "axis_id": "PERRY_DATASET_REPORTED_EVENT_MAX_GUST_MPS",
        "unit": "m/s",
        "source_height_and_averaging_period": "unresolved_in_source_release",
    }, dr


def evaluate_damage_call(
    artifact: Mapping[str, Any],
    request: Mapping[str, Any],
    *,
    verified_artifact_sha256_hex: str | None = None,
    allow_canonical_runtime_artifact: bool = False,
) -> dict[str, Any]:
    canonical = artifact.get("canonical_runtime_artifact")
    if canonical is not False and not (
        allow_canonical_runtime_artifact and canonical is True
    ):
        raise TropicalCycloneWindSolarV2EvaluationError(
            "CURVE_PAYLOAD_INVALID", "reference evaluator requires a noncanonical proposal"
        )
    if verified_artifact_sha256_hex is not None and re.fullmatch(
        r"[0-9a-f]{64}", verified_artifact_sha256_hex
    ) is None:
        raise TropicalCycloneWindSolarV2EvaluationError(
            "ARTIFACT_PIN_MISMATCH", "verified artifact SHA must be 64 lowercase hexadecimal characters"
        )
    if request.get("pathway_id") in (None, ""):
        raise TropicalCycloneWindSolarV2EvaluationError(
            "PATHWAY_ID_REQUIRED", "pathway_id is required"
        )
    if request.get("pathway_id") != PATHWAY:
        raise TropicalCycloneWindSolarV2EvaluationError(
            "PATHWAY_ID_UNKNOWN", "no neighboring-wind fallback is permitted"
        )
    present_values = sorted(VALUE_FIELDS.intersection(request))
    if present_values:
        raise TropicalCycloneWindSolarV2EvaluationError(
            "SCENARIO_LOSS_WITHHELD_SYNTHETIC_T4_PROPOSAL",
            "value inputs are prohibited: " + ", ".join(present_values),
        )
    _require_event_identity(request)
    pathway = _pathway(artifact)
    units = {item["id"]: item for item in artifact["failure_units"]}
    requested = request.get("failure_unit_id")
    if requested is not None and requested not in units:
        raise TropicalCycloneWindSolarV2EvaluationError(
            "FAILURE_UNIT_ID_UNKNOWN", f"unknown failure unit {requested!r}"
        )
    capability = artifact["capability_declaration"]["pathway_capabilities"][0]
    withheld = {
        item["failure_unit_id"]: item["reason_codes"]
        for item in capability["withheld_failure_units"]
    }

    def capability_ref() -> dict[str, Any]:
        return {
            "path": "tropical_cyclone_wind_solar__model_v2_0__docs_r1__capability.json",
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

    common_flags = [
        "NO_CANONICAL_OR_HAZARD_CUTOVER",
        "SCENARIO_DOLLAR_LOSS_WITHHELD",
        "FULL_PLANT_PHYSICAL_LOSS_INCOMPLETE",
    ]
    if requested in COMMON_WITHHELD_UNITS:
        _reject_unknown_fields(request, WITHHELD_DIRECT_REQUEST_FIELDS)
        flags = [
            *common_flags,
            "WITHHELD_UNIT_NO_ARRAY_AXIS_EVALUATED",
        ]
        if requested == "PV_GSU_SUBSTATION":
            flags.append("GSU_SEPARATE_YARD_POINT_ROUTE_REQUIRED")
        conditioners = _compound_conditioners(request, flags, architecture=None)
        unit = units[requested]
        result_flags = list(dict.fromkeys(flags))
        result_item = {
            "pathway_id": PATHWAY,
            "failure_unit_id": requested,
            "curve_id": None,
            "subsystem": unit["subsystem"],
            "component": unit["component"],
            "status": "withheld",
            "scalar_central_dr": None,
            "scenario_drs": {},
            "state_probabilities_by_scenario": {},
            "withheld_reason_codes": list(
                dict.fromkeys(
                    ["NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT", *withheld.get(requested, [])]
                )
            ),
            "metadata_flags": result_flags,
        }
        return {
            "schema_version": "damage_emit.v2",
            "cell_id": artifact["cell_id"],
            "damage_code_id": artifact["damage_code_id"],
            "model_version": artifact["semantic_damage_model_version"],
            "pathway_id": PATHWAY,
            "emit_mode": "scalar_mean",
            "hazard_input_used": {
                "event_id": request["event_id"],
                "event_family_id": request["event_family_id"],
                "requested_failure_unit_id": requested,
                "array_axis_applied": False,
            },
            "input_quality": {"limitation_flags": result_flags},
            "selectors_used": {"failure_unit_id": requested},
            "conditioners_used": conditioners,
            "failure_unit_results": [result_item],
            "capability_declaration_ref": capability_ref(),
        }

    architecture = request.get("array_architecture")
    if architecture is None:
        raise TropicalCycloneWindSolarV2EvaluationError(
            "ARRAY_ARCHITECTURE_REQUIRED", "array_architecture has no default"
        )
    if architecture not in ARCHITECTURE_UNITS:
        raise TropicalCycloneWindSolarV2EvaluationError(
            "ARRAY_ARCHITECTURE_UNSUPPORTED", f"unsupported architecture {architecture!r}"
        )
    allowed_fields = {
        PERRY: PERRY_REQUEST_FIELDS,
        FIXED: FIXED_REQUEST_FIELDS,
        TRACKER: TRACKER_REQUEST_FIELDS,
    }[architecture]
    _reject_unknown_fields(request, allowed_fields)
    active = ARCHITECTURE_UNITS[architecture]
    other_active = set().union(*ARCHITECTURE_UNITS.values()) - set(active)
    if requested in other_active:
        raise TropicalCycloneWindSolarV2EvaluationError(
            "FAILURE_UNIT_NOT_APPLICABLE_TO_ARCHITECTURE",
            f"{requested} is not applicable to {architecture}",
        )
    flags = list(common_flags)
    conditioners = _compound_conditioners(request, flags, architecture=architecture)
    if architecture == PERRY:
        record = _record(pathway, PERRY_UNIT)
        if record is None:
            raise TropicalCycloneWindSolarV2EvaluationError(
                "CURVE_PAYLOAD_INVALID", "Perry compatibility record is missing"
            )
        axis, hazard_basis, perry_dr = _perry_axis(request, record)
        flags.extend(
            [
                "PERRY_SOURCE_COMPATIBILITY_ROUTE",
                "SOURCE_SPECIFIC_VISIBLE_MODULE_MATERIAL_PROXY",
                "SOURCE_COMPOSITE_HURRICANE_MODULE_LOSS",
                "SOURCE_AXIS_PRODUCT_QUERY_SEMANTICS_UNRESOLVED",
                "PREDICTIVE_RELATIONSHIP_NOT_VALIDATED",
            ]
        )
    elif architecture == FIXED:
        flags.extend(
            [
                "EXPERIMENTAL_SYNTHETIC_T4_SCENARIO",
                "TC_NUMERICAL_RESPONSE_NOT_CALIBRATED",
                "CELL_LOCAL_SYNTHETIC_PARAMETER_DECISION",
                "NONPROBABILISTIC_EPISTEMIC_ENVELOPE",
                "TC_BRIDGE_CONTENT_NOT_RESOLVED_BY_REFERENCE_EVALUATOR",
                "TC_DURATION_DIRECTION_AND_CYCLING_NOT_NUMERICALLY_MODELED",
                "NO_HARD_ZERO_EXCEPT_ZERO_DEMAND",
            ]
        )
        axis, hazard_basis = _fixed_axis(request, flags)
        perry_dr = None
    else:
        flags.extend(
            [
                "EXPERIMENTAL_SYNTHETIC_T4_SCENARIO",
                "TC_NUMERICAL_RESPONSE_NOT_CALIBRATED",
                "CELL_LOCAL_SYNTHETIC_PARAMETER_DECISION",
                "NONPROBABILISTIC_EPISTEMIC_ENVELOPE",
                "TC_BRIDGE_CONTENT_NOT_RESOLVED_BY_REFERENCE_EVALUATOR",
                "TC_DURATION_DIRECTION_AND_CYCLING_NOT_NUMERICALLY_MODELED",
                "NO_HARD_ZERO_EXCEPT_ZERO_DEMAND",
            ]
        )
        axis, hazard_basis = _tracker_axis(request, flags)
        perry_dr = None
    flags = list(dict.fromkeys(flags))
    hazard_basis.update(
        {
            "event_id": request["event_id"],
            "event_family_id": request["event_family_id"],
            "axis_value": axis,
            "array_architecture": architecture,
            "axis_id": (
                hazard_basis.get("axis_id")
                or pathway["hazard_axis"]["id"]
            ),
        }
    )
    selectors_used: dict[str, Any] = {"array_architecture": architecture}
    if architecture == PERRY:
        selectors_used.update(
            {field: request[field] for field in PERRY_SELECTORS}
        )
    elif architecture == FIXED:
        selectors_used.update(
            {
                "array_zone": request["array_zone"],
                "array_spatial_object_id": request["array_spatial_object_id"],
            }
        )
    else:
        tracker_selector_fields = (
            "aeroelastic_qualification_id",
            "aeroelastic_qualification_sha256",
            "tracker_system_id",
            "tracker_module_configuration",
            "tracker_layout_id",
            "tracker_angle_deg",
            "tracker_position_state",
            "stow_confirmation_basis",
            "tracker_drive_lock_state",
            "array_zone",
            "array_spatial_object_id",
            "qualification_tracker_system_id",
            "qualification_tracker_module_configuration",
            "qualification_tracker_layout_id",
            "qualification_tracker_angle_deg",
            "qualification_tracker_position_state",
            "qualification_array_zone",
            "qualification_drive_lock_state",
            "qualification_speed_averaging_s",
            "qualification_speed_reference",
            "qualification_tc_wind_field_bridge_id",
            "qualification_direction_basis_id",
            "qualification_duration_basis_id",
        )
        selectors_used.update({field: request[field] for field in tracker_selector_fields})
    unit_ids = [requested] if requested else [*active, *COMMON_WITHHELD_UNITS]
    results: list[dict[str, Any]] = []
    for unit_id in unit_ids:
        unit = units[unit_id]
        record = _record(pathway, unit_id)
        if record is None:
            result_flags = [*flags, "ARRAY_AXIS_NOT_APPLIED_TO_WITHHELD_UNIT"]
            if unit_id == "PV_GSU_SUBSTATION":
                result_flags.append("GSU_SEPARATE_YARD_POINT_ROUTE_REQUIRED")
            results.append(
                {
                    "pathway_id": PATHWAY,
                    "failure_unit_id": unit_id,
                    "curve_id": None,
                    "subsystem": unit["subsystem"],
                    "component": unit["component"],
                    "status": "withheld",
                    "scalar_central_dr": None,
                    "scenario_drs": {},
                    "state_probabilities_by_scenario": {},
                    "withheld_reason_codes": list(
                        dict.fromkeys(
                            ["NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT", *withheld.get(unit_id, [])]
                        )
                    ),
                    "metadata_flags": list(dict.fromkeys(result_flags)),
                }
            )
            continue
        if architecture == PERRY:
            results.append(
                {
                    "pathway_id": PATHWAY,
                    "failure_unit_id": unit_id,
                    "curve_id": record["curve_id"],
                    "subsystem": unit["subsystem"],
                    "component": unit["component"],
                    "status": "conditional",
                    "scalar_central_dr": perry_dr,
                    "scenario_drs": {"source_compatibility": perry_dr},
                    "state_probabilities_by_scenario": {},
                    "withheld_reason_codes": [],
                    "metadata_flags": flags,
                }
            )
            continue
        evaluated = evaluate_ordered_damage_state_record(record, axis)
        results.append(
            {
                "pathway_id": PATHWAY,
                "failure_unit_id": unit_id,
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
                "metadata_flags": flags,
            }
        )
    return {
        "schema_version": "damage_emit.v2",
        "cell_id": artifact["cell_id"],
        "damage_code_id": artifact["damage_code_id"],
        "model_version": artifact["semantic_damage_model_version"],
        "pathway_id": PATHWAY,
        "emit_mode": "state_ensemble" if architecture != PERRY else "scalar_mean",
        "hazard_input_used": hazard_basis,
        "input_quality": {"limitation_flags": flags},
        "selectors_used": selectors_used,
        "conditioners_used": conditioners,
        "failure_unit_results": results,
        "capability_declaration_ref": capability_ref(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact")
    parser.add_argument("request_json")
    args = parser.parse_args()
    artifact = load_artifact(args.artifact)
    request = json.loads(args.request_json)
    pin = request.pop("artifact_pin", None)
    if not isinstance(pin, Mapping):
        raise TropicalCycloneWindSolarV2EvaluationError(
            "ARTIFACT_PIN_INCOMPLETE", "CLI request must carry an exact artifact_pin"
        )
    digest = artifact_sha256(args.artifact)
    verify_artifact_pin(artifact, pin, artifact_sha256_hex=digest)
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
