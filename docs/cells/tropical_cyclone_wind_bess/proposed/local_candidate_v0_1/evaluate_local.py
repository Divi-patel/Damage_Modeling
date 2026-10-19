"""Explicit-opt-in local test reader. Not a production Damage API."""
import hashlib
import json
import math
from numbers import Real
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "scripts/reference_helpers"))
from tropical_cyclone_wind_solar_v2_curve_eval import evaluate_ordered_damage_state_record


def load_candidate(folder=None, *, allow_local_test=False):
    if allow_local_test is not True:
        raise ValueError("LOCAL_TEST_OPT_IN_REQUIRED")
    folder = Path(folder or Path(__file__).resolve().parent)
    pin = json.loads((folder / "consumption_pin.json").read_text())
    for name, expected in pin["sha256"].items():
        if hashlib.sha256((folder / name).read_bytes()).hexdigest() != expected:
            raise ValueError("CANDIDATE_SHA_MISMATCH")
    for name, expected in pin["dependency_sha256"].items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected:
            raise ValueError("NUMERICAL_DEPENDENCY_SHA_MISMATCH")
    artifact = json.loads((folder / "curve_artifact.json").read_text())
    if (artifact["cell_id"], artifact["semantic_damage_model_version"], artifact["documentation_revision"], artifact["canonical_runtime_artifact"]) != ("tropical_cyclone_wind_bess", "model v0.1", "docs r1", False):
        raise ValueError("CANDIDATE_IDENTITY_MISMATCH")
    return {"artifact": artifact, "values": json.loads((folder / "value_binding.json").read_text())}


def evaluate(candidate, *, failure_unit_id, pressure_ratio, pathway_id, demand_basis_id, response_hypothesis_id, resistance_scenario):
    def withheld(reason):
        return {"status": "unavailable", "reason": reason, "dr": None, "unit_candidate_loss_usd": None, "complete_plant_loss_usd": None}
    if pathway_id != "tropical_cyclone_wind":
        return withheld("PATHWAY_NOT_SUPPORTED")
    if demand_basis_id != "BESS_TC_LOCAL_PRESSURE_RATIO_RESEARCH_V1":
        return withheld("DEMAND_BASIS_NOT_QUALIFIED_FOR_LOCAL_TEST")
    if isinstance(pressure_ratio, bool) or not isinstance(pressure_ratio, Real) or not math.isfinite(pressure_ratio) or not 0 <= pressure_ratio <= 2:
        return withheld("PRESSURE_RATIO_INVALID_OR_OUTSIDE_SOURCE_DOMAIN")
    artifact = candidate["artifact"]
    selected = artifact["evaluation_contract"]["curve_selection_by_response_hypothesis"].get(response_hypothesis_id)
    if selected is None:
        return withheld("RESPONSE_HYPOTHESIS_REQUIRED_OR_UNKNOWN")
    curve_id = selected.get(failure_unit_id)
    if curve_id is None:
        return withheld("NO_RESPONSE_FOR_FAILURE_UNIT")
    record = next(r for r in artifact["pathways"][0]["curve_records"] if r["curve_id"] == curve_id)
    if resistance_scenario not in {r["scenario_id"] for r in record["parameters"]["capacity_scenarios"]}:
        return withheld("RESISTANCE_SCENARIO_REQUIRED_OR_UNKNOWN")
    response = evaluate_ordered_damage_state_record(record, float(pressure_ratio))[resistance_scenario]
    value = candidate["values"]["units"][failure_unit_id]["value_usd_each"]
    dr = response["damage_ratio"]
    loss = dr * value
    if not 0 <= dr <= 1 or not 0 <= loss <= value:
        raise ValueError("SAME_UNIT_PHYSICAL_CAP_FAILED")
    return {"status": "local_candidate_only", "reason": "BW_Q01_SELECTED_LOCAL_TEST_NOT_CANONICAL", "dr": dr, "unit_candidate_loss_usd": loss, "complete_plant_loss_usd": None, "curve_id": curve_id, "limitation_flags": artifact["evaluation_contract"]["limitation_flags"]}
