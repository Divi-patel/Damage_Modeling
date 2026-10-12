"""Reference evaluator for the noncanonical flood × real estate model-v0.1 proposal.

Evaluates one request against the proposed bundle-v3 artifact and returns a damage-emit-v2 object.
Physics only: failure-unit damage ratio (fraction of structure replacement cost new). No dollars,
no frequency, no annual or tail metrics. Standard library only. Not a stable src API.

Request contract (canonical field names):
    pathway_id                       required, "flood_inundation_contact"
    failure_unit_id                  optional; defaults to the single numeric unit
    reference_building_id            required selector
    flood_water_type                 required conditioner
    flood_depth_above_grade_ft       axis mode A (preferred): water depth above ground at the building
    first_floor_height_ft            optional with mode A; reference-building default otherwise
    flood_depth_above_first_floor_ft axis mode B: depth already referenced to the first floor

Rules (decision log D-FRE-05, -20, -21, -22, -24):
    - unknown water type withholds; freshwater uses Hazus, coastal surge uses NACCS;
    - straight lines between published points;
    - mode A: depth above grade <= 0 is not inundated and returns 0 (D-FRE-24);
    - below a record's lowest published depth returns 0; above its highest published depth withholds;
    - coastal records also emit the NACCS Min / Max building-variant bounds (not a probability spread).

Usage:
    python flood_real_estate_curve_eval.py <artifact.json> '<request json>'
"""
from __future__ import annotations

import json
import math
import sys
from typing import Any, Mapping

PATHWAY_ID = "flood_inundation_contact"
AXIS_DIRECT = "flood_depth_above_first_floor_ft"
AXIS_GRADE = "flood_depth_above_grade_ft"
FFH_FIELD = "first_floor_height_ft"


class DamageCallError(ValueError):
    """Raised for malformed or contract-violating requests; .code holds the reason code."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def _finite(value: Any, code: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise DamageCallError(code)
    number = float(value)
    if not math.isfinite(number):
        raise DamageCallError(code)
    return number


def interpolate(points: list[list[float]], x: float) -> float:
    """Straight line between the two published points around x (x inside the published range)."""
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        if x0 <= x <= x1:
            return y0 if x1 == x0 else y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    raise DamageCallError("AXIS_OUTSIDE_RECORD_POINTS")


def _record_value(record: Mapping[str, Any], x: float) -> tuple[str, float | None, str | None]:
    """Return (status, DR, reason/flag) for one record at depth-above-floor x."""
    lo, hi = record["valid_range"]
    if x > hi:
        return "withheld", None, "ABOVE_SOURCE_VALID_RANGE"
    if x < lo:
        return "conditional", 0.0, "BELOW_SOURCE_RANGE_ZERO"
    return "conditional", interpolate(record["parameters"]["points"], x), None


def evaluate_damage_call(artifact: Mapping[str, Any], request: Mapping[str, Any]) -> dict[str, Any]:
    if artifact.get("schema_version") != "damage_curve_record_bundle.v3":
        raise DamageCallError("V3_ARTIFACT_REQUIRED")
    pathway_id = request.get("pathway_id")
    if not pathway_id:
        raise DamageCallError("PATHWAY_ID_REQUIRED")
    pathways = {p["pathway_id"]: p for p in artifact["pathways"]}
    if pathway_id not in pathways:
        raise DamageCallError("PATHWAY_ID_UNKNOWN")
    pathway = pathways[pathway_id]
    units = {u["id"]: u for u in artifact["failure_units"]}

    # selector: reference building (fixed identity)
    selector = {s["field"]: s for s in pathway["selector_logic"]}["reference_building_id"]
    building = request.get("reference_building_id")
    if building in (None, ""):
        raise DamageCallError("REFERENCE_BUILDING_ID_REQUIRED")
    if building not in selector["allowed"]:
        raise DamageCallError("REFERENCE_BUILDING_ID_UNKNOWN")

    # conditioner: water type (event state); routes the record, withholds when unknown
    conditioner = {c["field"]: c for c in pathway["conditioner_logic"]}["flood_water_type"]
    water = request.get("flood_water_type")
    if water in (None, ""):
        raise DamageCallError("FLOOD_WATER_TYPE_REQUIRED")
    if water not in conditioner["allowed"]:
        raise DamageCallError("FLOOD_WATER_TYPE_UNKNOWN_VALUE")

    # axis: exactly one payload mode
    has_direct = AXIS_DIRECT in request
    has_grade = AXIS_GRADE in request
    if has_direct and (has_grade or FFH_FIELD in request):
        raise DamageCallError("AXIS_PAYLOAD_AMBIGUOUS")
    if not has_direct and not has_grade:
        raise DamageCallError("AXIS_PAYLOAD_REQUIRED")
    flags: list[str] = list(artifact["evaluation_contract"]["metadata_flags_always"])
    hazard_input: dict[str, Any] = {}
    inundated = True
    if has_grade:
        depth_grade = _finite(request[AXIS_GRADE], "AXIS_VALUE_INVALID")
        if depth_grade < 0:
            raise DamageCallError("NEGATIVE_DEPTH_ABOVE_GRADE")
        if FFH_FIELD in request:
            ffh = _finite(request[FFH_FIELD], "FIRST_FLOOR_HEIGHT_INVALID")
            if ffh < 0:
                raise DamageCallError("FIRST_FLOOR_HEIGHT_INVALID")
        else:
            ffh = float(pathway["reference_first_floor_height_ft"][building])
            flags.append("REFERENCE_FIRST_FLOOR_HEIGHT_DEFAULT_USED")
        x = depth_grade - ffh
        inundated = depth_grade > 0
        hazard_input = {AXIS_GRADE: depth_grade, FFH_FIELD: ffh, AXIS_DIRECT: x}
    else:
        x = _finite(request[AXIS_DIRECT], "AXIS_VALUE_INVALID")
        hazard_input = {AXIS_DIRECT: x}
        flags.append("DEPTH_ABOVE_FLOOR_SUPPLIED_DIRECTLY")

    unit_id = request.get("failure_unit_id") or artifact["evaluation_contract"]["supported_failure_unit_id"]
    if unit_id not in units:
        raise DamageCallError("FAILURE_UNIT_ID_UNKNOWN")
    unit = units[unit_id]
    base = {
        "schema_version": "damage_emit.v2",
        "cell_id": artifact["cell_id"],
        "damage_code_id": artifact["damage_code_id"],
        "model_version": artifact["semantic_damage_model_version"],
        "pathway_id": pathway_id,
        "emit_mode": "scalar_mean",
        "hazard_input_used": hazard_input,
        "selectors_used": {"reference_building_id": building},
        "conditioners_used": {"flood_water_type": water},
        "capability_declaration_ref": artifact["capability_declaration"]["cell_id"],
    }

    def withheld(codes: list[str], curve_id: str | None = None) -> dict[str, Any]:
        return {**base, "failure_unit_results": [{
            "pathway_id": pathway_id, "failure_unit_id": unit_id, "curve_id": curve_id,
            "subsystem": unit["subsystem"], "component": unit["component"], "status": "withheld",
            "scalar_central_dr": None, "withheld_reason_codes": codes,
            "metadata_flags": list(dict.fromkeys(flags))}]}

    coverage = {c["failure_unit_id"]: c for c in pathway["failure_unit_coverage"]}[unit_id]
    if coverage["status"].startswith("withheld"):
        return withheld(list(coverage["reason_codes"]))
    if water not in conditioner["numeric_support_when"]:
        return withheld([conditioner["withhold_otherwise"]])

    def pick(band: str) -> Mapping[str, Any] | None:
        hits = [r for r in pathway["curve_records"]
                if r["failure_unit_id"] == unit_id
                and r["selector_match"]["reference_building_id"] == building
                and r["selector_match"]["flood_water_type"] == water
                and r["selector_match"]["band"] == band]
        if len(hits) > 1:
            raise DamageCallError("CURVE_SELECTOR_MATCH_NOT_UNIQUE")
        return hits[0] if hits else None

    record = pick("point")
    if record is None:
        raise DamageCallError("CURVE_SELECTOR_MATCH_NOT_FOUND")
    flags += record["metadata_flags"]
    lower, upper = pick("lower_bound"), pick("upper_bound")

    if not inundated:
        flags.append("NOT_INUNDATED_ABOVE_GRADE")
        status, dr, note = "conditional", 0.0, None
    else:
        status, dr, note = _record_value(record, x)
    if status == "withheld":
        return withheld([note], record["curve_id"])
    if note:
        flags.append(note)

    result: dict[str, Any] = {
        "pathway_id": pathway_id, "failure_unit_id": unit_id, "curve_id": record["curve_id"],
        "subsystem": unit["subsystem"], "component": unit["component"], "status": "conditional",
        "scalar_central_dr": dr, "withheld_reason_codes": [],
    }
    if lower is not None and upper is not None:
        base["emit_mode"] = "scalar_mean_plus_bounds"
        if inundated:
            lo_dr, hi_dr = _record_value(lower, x)[1], _record_value(upper, x)[1]
        else:
            lo_dr = hi_dr = 0.0
        result["scenario_drs"] = {"naccs_min_building_variant": lo_dr, "naccs_max_building_variant": hi_dr}
        flags.append("BOUNDS_ARE_BUILDING_VARIANT_ENVELOPE_NOT_PROBABILITY")
    result["metadata_flags"] = list(dict.fromkeys(flags))
    return {**base, "failure_unit_results": [result]}


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__)
        return 2
    with open(argv[1]) as fh:
        artifact = json.load(fh)
    try:
        print(json.dumps(evaluate_damage_call(artifact, json.loads(argv[2])), indent=2))
    except DamageCallError as err:
        print(json.dumps({"error_code": err.code}))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
