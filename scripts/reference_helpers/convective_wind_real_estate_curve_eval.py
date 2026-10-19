"""Reference evaluator for the noncanonical convective wind × real estate model-v0.1 proposal.

Evaluates one request against the proposed bundle-v3 artifact and returns a damage-emit-v2 object.
Physics only: failure-unit damage ratio (fraction of structure replacement cost new). No dollars,
no frequency, no annual or tail metrics. Standard library only. Not a stable src API.

Request contract (canonical field names):
    pathway_id                              required: straight_line_convective | tornado_direct_hit
    failure_unit_id                         required: CWRE_BUILDING_STRUCTURE (CWRE_BUILDING_CONTENTS is withheld)
    reference_building_id                   required selector
    convective_gust_3s_10m_mph              axis of straight_line_convective (3-s gust, 10 m, open terrain)
    tornado_gust_3s_10m_mph                 axis of tornado_direct_hit (3-s gust; Hazard's EF band midpoint accepted)

Rules (decision log D-CWRE-02, -05, -14, -15):
    - each pathway reads only its own axis field; an EF rating is not a gust and is never evaluated;
    - straight lines between the tabulated 1-mph points; 0 to 255 mph evaluates;
    - above 255 mph withholds (ABOVE_SOURCE_VALID_RANGE); a negative gust is an error (AXIS_OUTSIDE_VALID_RANGE).

Usage:
    python convective_wind_real_estate_curve_eval.py <artifact.json> '<request json>'
"""
from __future__ import annotations

import json
import math
import sys
from typing import Any, Mapping

BUILDING = "reference_building_id"


class DamageCallError(ValueError):
    """Raised for malformed or contract-violating requests; .code holds the reason code."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def interpolate(points: list[list[float]], x: float) -> float:
    """Straight line between the two tabulated points around x (x inside the tabulated range)."""
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        if x0 <= x <= x1:
            return y0 if x1 == x0 else y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    raise DamageCallError("AXIS_OUTSIDE_RECORD_POINTS")


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
    selectors = {s["field"]: s for s in pathway["selector_logic"]}

    building = request.get(BUILDING)
    if building in (None, ""):
        raise DamageCallError("REFERENCE_BUILDING_ID_REQUIRED")
    if building not in selectors[BUILDING]["allowed"]:
        raise DamageCallError("REFERENCE_BUILDING_ID_UNKNOWN")

    axis = pathway["hazard_axis"]["preferred_input_field"]
    if axis not in request:
        raise DamageCallError("AXIS_PAYLOAD_REQUIRED")
    gust = request[axis]
    if isinstance(gust, bool) or not isinstance(gust, (int, float)) or not math.isfinite(float(gust)):
        raise DamageCallError("AXIS_VALUE_INVALID")
    gust = float(gust)
    lo, hi = pathway["hazard_axis"]["valid_range"]
    if gust < lo:
        raise DamageCallError("AXIS_OUTSIDE_VALID_RANGE")

    unit_id = request.get("failure_unit_id")
    if unit_id in (None, ""):
        raise DamageCallError("FAILURE_UNIT_ID_REQUIRED")
    if unit_id not in units:
        raise DamageCallError("FAILURE_UNIT_ID_UNKNOWN")
    unit = units[unit_id]
    flags: list[str] = list(artifact["evaluation_contract"]["metadata_flags_always"])
    base = {
        "schema_version": "damage_emit.v2",
        "cell_id": artifact["cell_id"],
        "damage_code_id": artifact["damage_code_id"],
        "model_version": artifact["semantic_damage_model_version"],
        "pathway_id": pathway_id,
        "emit_mode": "scalar_mean",
        "hazard_input_used": {axis: gust},
        "selectors_used": {BUILDING: building},
        "conditioners_used": {},
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

    hits = [r for r in pathway["curve_records"]
            if r["failure_unit_id"] == unit_id and r["selector_match"][BUILDING] == building]
    if len(hits) != 1:
        raise DamageCallError("CURVE_SELECTOR_MATCH_NOT_UNIQUE" if hits else "CURVE_SELECTOR_MATCH_NOT_FOUND")
    record = hits[0]
    flags += record["metadata_flags"]
    if gust > hi:
        return withheld(["ABOVE_SOURCE_VALID_RANGE"], record["curve_id"])
    dr = interpolate(record["parameters"]["points"], gust)
    return {**base, "failure_unit_results": [{
        "pathway_id": pathway_id, "failure_unit_id": unit_id, "curve_id": record["curve_id"],
        "subsystem": unit["subsystem"], "component": unit["component"], "status": "conditional",
        "scalar_central_dr": dr, "withheld_reason_codes": [],
        "metadata_flags": list(dict.fromkeys(flags))}]}


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
