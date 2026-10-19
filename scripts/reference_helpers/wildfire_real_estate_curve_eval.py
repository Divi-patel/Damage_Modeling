"""Reference evaluator for the noncanonical wildfire × real estate model-v0.1 proposal.

Evaluates one request against the proposed bundle-v3 artifact and returns a damage-emit-v2 object.
Physics only: failure-unit damage ratio (fraction of structure replacement cost new). No dollars,
no frequency, no annual or tail metrics. Standard library only. Not a stable src API.

Request contract (canonical field names):
    pathway_id                              required: wildfire_building_exposure
    failure_unit_id                         required: WFRE_BUILDING_STRUCTURE (WFRE_BUILDING_CONTENTS is withheld)
    reference_building_id                   required selector
    source_wildfire_product_id              required selector: USFS_RDS_2016_0034_3_270M
    conditional_flame_length_class_state    exact integer FSim class state 0..6 (0 = no event)

Rules (decision log D-WFRE-02, -04, -10):
    - exact integer states only; a fractional, boolean, non-numeric or out-of-range state is INVALID_CLASS_STATE;
    - nothing is interpolated between classes; state 0 returns 0;
    - a burn probability in the damage call is an error (FREQUENCY_FIELD_NOT_ALLOWED_IN_DAMAGE_CALL);
    - a flame length in feet or a class label is not the axis field.

Usage:
    python wildfire_real_estate_curve_eval.py <artifact.json> '<request json>'
"""
from __future__ import annotations

import json
import math
import sys
from typing import Any, Mapping

BUILDING = "reference_building_id"
PRODUCT = "source_wildfire_product_id"
FREQUENCY_FIELDS = ("burn_probability", "annual_burn_probability", "lambda_burnable", "bp")


class DamageCallError(ValueError):
    """Raised for malformed or contract-violating requests; .code holds the reason code."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def evaluate_damage_call(artifact: Mapping[str, Any], request: Mapping[str, Any]) -> dict[str, Any]:
    if artifact.get("schema_version") != "damage_curve_record_bundle.v3":
        raise DamageCallError("V3_ARTIFACT_REQUIRED")
    if any(f in request for f in FREQUENCY_FIELDS):
        raise DamageCallError("FREQUENCY_FIELD_NOT_ALLOWED_IN_DAMAGE_CALL")
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
    product = request.get(PRODUCT)
    if product in (None, ""):
        raise DamageCallError("SOURCE_WILDFIRE_PRODUCT_ID_REQUIRED")
    if product not in selectors[PRODUCT]["allowed"]:
        raise DamageCallError("SOURCE_WILDFIRE_PRODUCT_ID_UNSUPPORTED")

    axis = pathway["hazard_axis"]["preferred_input_field"]
    if axis not in request:
        raise DamageCallError("AXIS_PAYLOAD_REQUIRED")
    state = request[axis]
    if isinstance(state, bool) or not isinstance(state, (int, float)) or not math.isfinite(float(state)) \
            or not float(state).is_integer():
        raise DamageCallError("INVALID_CLASS_STATE")
    lo, hi = pathway["hazard_axis"]["valid_range"]
    if not lo <= float(state) <= hi:
        raise DamageCallError("INVALID_CLASS_STATE")
    state = int(state)

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
        "hazard_input_used": {axis: state},
        "selectors_used": {BUILDING: building, PRODUCT: product},
        "conditioners_used": {},
        "capability_declaration_ref": artifact["capability_declaration"]["cell_id"],
    }

    coverage = {c["failure_unit_id"]: c for c in pathway["failure_unit_coverage"]}[unit_id]
    if coverage["status"].startswith("withheld"):
        return {**base, "failure_unit_results": [{
            "pathway_id": pathway_id, "failure_unit_id": unit_id, "curve_id": None,
            "subsystem": unit["subsystem"], "component": unit["component"], "status": "withheld",
            "scalar_central_dr": None, "withheld_reason_codes": list(coverage["reason_codes"]),
            "metadata_flags": list(dict.fromkeys(flags))}]}

    hits = [r for r in pathway["curve_records"]
            if r["failure_unit_id"] == unit_id and r["selector_match"][BUILDING] == building
            and r["selector_match"][PRODUCT] == product]
    if len(hits) != 1:
        raise DamageCallError("CURVE_SELECTOR_MATCH_NOT_UNIQUE" if hits else "CURVE_SELECTOR_MATCH_NOT_FOUND")
    record = hits[0]
    flags += record["metadata_flags"]
    points = {int(x): y for x, y in record["parameters"]["points"]}
    if state not in points:
        raise DamageCallError("INVALID_CLASS_STATE")
    return {**base, "failure_unit_results": [{
        "pathway_id": pathway_id, "failure_unit_id": unit_id, "curve_id": record["curve_id"],
        "subsystem": unit["subsystem"], "component": unit["component"], "status": "conditional",
        "scalar_central_dr": points[state], "withheld_reason_codes": [],
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
