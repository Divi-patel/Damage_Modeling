"""Reference evaluator for the noncanonical tropical-cyclone wind × real estate model-v0.1 proposal.

Evaluates one request against the proposed bundle-v3 artifact and returns a damage-emit-v2 object.
Physics only: failure-unit damage ratio (fraction of structure replacement cost new). No dollars,
no frequency, no annual or tail metrics. Standard library only. Not a stable src API.

Request contract (canonical field names):
    pathway_id                 required, "tropical_cyclone_wind"
    failure_unit_id            optional; defaults to the single numeric unit
    reference_building_id      required selector
    hazus_terrain_class        required selector: open | light_suburban | suburban | light_trees | trees
    tc_peak_gust_3s_10m_mph    required axis: peak 3-second gust at 10 m, open terrain, mph
    hazus_<characteristic>     optional wind building characteristics (roof shape, shutters, ...); only the
                               reference value of each is published in v0.1

Rules (decision log D-TCRE-06, -07, -17, -18, -19):
    - terrain is required, never defaulted, never interpolated;
    - straight lines between the published 5-mph points;
    - 0 <= gust < 50 mph returns 0 (the source's own zero); gust > 250 mph withholds; negative gust is an error;
    - a characteristic omitted uses the reference value (flagged); a different, valid value withholds
      (WIND_CHARACTERISTIC_VARIANT_NOT_PUBLISHED); a value or field the building does not have is an error.

Usage:
    python tropical_cyclone_wind_real_estate_curve_eval.py <artifact.json> '<request json>'
"""
from __future__ import annotations

import json
import math
import sys
from typing import Any, Mapping

AXIS = "tc_peak_gust_3s_10m_mph"
BUILDING = "reference_building_id"
TERRAIN = "hazus_terrain_class"
CHAR_PREFIX = "hazus_"


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

    # selectors: reference building (fixed identity) and terrain class (fixed site attribute)
    building = request.get(BUILDING)
    if building in (None, ""):
        raise DamageCallError("REFERENCE_BUILDING_ID_REQUIRED")
    if building not in selectors[BUILDING]["allowed"]:
        raise DamageCallError("REFERENCE_BUILDING_ID_UNKNOWN")
    terrain = request.get(TERRAIN)
    if terrain in (None, ""):
        raise DamageCallError("TERRAIN_CLASS_REQUIRED")
    if terrain not in selectors[TERRAIN]["allowed"]:
        raise DamageCallError("TERRAIN_CLASS_UNKNOWN")

    # wind building characteristics: reference value only (D-TCRE-19)
    contract = pathway["wind_characteristic_contract"][building]
    known_fields = {f for b in pathway["wind_characteristic_contract"].values() for f in b}
    supplied = {k: v for k, v in request.items() if k.startswith(CHAR_PREFIX) and k != TERRAIN}
    for field, value in supplied.items():
        if field not in known_fields:
            raise DamageCallError("WIND_CHARACTERISTIC_FIELD_UNKNOWN")
        if field not in contract:
            raise DamageCallError("WIND_CHARACTERISTIC_NOT_APPLICABLE")
        if value not in contract[field]["allowed"]:
            raise DamageCallError("WIND_CHARACTERISTIC_VALUE_UNKNOWN")
    variant = [f for f, v in supplied.items() if v != contract[f]["reference"]]
    characteristics = {f: supplied.get(f, c["reference"]) for f, c in contract.items()}

    # axis
    if AXIS not in request:
        raise DamageCallError("AXIS_PAYLOAD_REQUIRED")
    gust = _finite(request[AXIS], "AXIS_VALUE_INVALID")
    if gust < 0:
        raise DamageCallError("NEGATIVE_GUST")

    unit_id = request.get("failure_unit_id") or artifact["evaluation_contract"]["supported_failure_unit_id"]
    if unit_id not in units:
        raise DamageCallError("FAILURE_UNIT_ID_UNKNOWN")
    unit = units[unit_id]
    flags: list[str] = list(artifact["evaluation_contract"]["metadata_flags_always"])
    if len(supplied) < len(contract):
        flags.append("REFERENCE_WIND_CHARACTERISTICS_DEFAULT_USED")
    base = {
        "schema_version": "damage_emit.v2",
        "cell_id": artifact["cell_id"],
        "damage_code_id": artifact["damage_code_id"],
        "model_version": artifact["semantic_damage_model_version"],
        "pathway_id": pathway_id,
        "emit_mode": "scalar_mean",
        "hazard_input_used": {AXIS: gust},
        "selectors_used": {BUILDING: building, TERRAIN: terrain, "wind_building_characteristics": characteristics},
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
    if variant:
        return withheld(["WIND_CHARACTERISTIC_VARIANT_NOT_PUBLISHED"])

    hits = [r for r in pathway["curve_records"]
            if r["failure_unit_id"] == unit_id
            and r["selector_match"][BUILDING] == building and r["selector_match"][TERRAIN] == terrain]
    if len(hits) != 1:
        raise DamageCallError("CURVE_SELECTOR_MATCH_NOT_UNIQUE" if hits else "CURVE_SELECTOR_MATCH_NOT_FOUND")
    record = hits[0]
    flags += record["metadata_flags"]
    lo, hi = record["valid_range"]
    if gust > hi:
        return withheld(["ABOVE_SOURCE_VALID_RANGE"], record["curve_id"])
    if gust < lo:
        dr = 0.0
        flags.append("BELOW_SOURCE_RANGE_ZERO")
    else:
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
