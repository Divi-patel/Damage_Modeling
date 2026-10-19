"""Opt-in conditional candidate audit reader; never a Hazard production import."""
import hashlib
import json
import math
from numbers import Real
from pathlib import Path

CELL = "wildfire_bess"
PATHWAY = "wildfire_thermal_attack"
SELECTOR = "BESS_LFP_R1_WILDFIRE_ORDINAL_LOCAL_V0_1"


def load_candidate(folder=None, *, allow_local_test=False):
    if allow_local_test is not True:
        raise ValueError("LOCAL_TEST_OPT_IN_REQUIRED")
    folder = Path(folder or Path(__file__).resolve().parent)
    pin = json.loads((folder / "consumption_pin.json").read_text())
    for name, expected in pin["sha256"].items():
        if Path(name).name != name:
            raise ValueError("LOCAL_PIN_FILENAME_REQUIRED")
        if hashlib.sha256((folder / name).read_bytes()).hexdigest() != expected:
            raise ValueError("CANDIDATE_SHA_MISMATCH")
    artifact = json.loads((folder / "curve_artifact.json").read_text())
    values = json.loads((folder / "value_binding.json").read_text())
    cap = json.loads((folder / "capability.json").read_text())
    if (artifact["cell_id"], artifact["semantic_damage_model_version"],
        artifact["documentation_revision"], artifact["canonical_runtime_artifact"]
        ) != (CELL, "model v0.1", "docs r1", False):
        raise ValueError("CANDIDATE_IDENTITY_MISMATCH")
    if artifact["capability_declaration"] != cap:
        raise ValueError("CAPABILITY_MISMATCH")
    if any(cap["consumer_annual_metrics"][k] != "withheld" for k in
           ("status_after_promotion",)):
        raise ValueError("LOCAL_ANNUAL_CAPABILITY_REQUIRED_WITHHELD")
    return {"artifact": artifact, "values": values}


def evaluate(candidate, *, failure_unit_id, class_state, pathway_id,
             selector_id, response_hypothesis_id, shape_scenario,
             assume_retained_hardware_serviceable_for_sensitivity=False,
             **unsupported_fields):
    def withheld(reason):
        return {"status": "unavailable", "reason": reason, "dr": None,
                "unit_conditional_mean_loss_usd": None,
                "complete_plant_loss_usd": None, "annual_metrics_authorized": False}
    if unsupported_fields:
        return withheld("UNSUPPORTED_INPUT_OR_FREQUENCY_FIELD")
    if pathway_id != PATHWAY:
        return withheld("PATHWAY_NOT_SUPPORTED")
    if selector_id != SELECTOR:
        return withheld("EXPLICIT_LOCAL_REFERENCE_SELECTOR_REQUIRED")
    if (isinstance(class_state, bool) or not isinstance(class_state, Real)
        or not math.isfinite(class_state) or int(class_state) != class_state
        or not 0 <= class_state <= 6):
        return withheld("EXACT_FSIM_CLASS_STATE_REQUIRED")
    contract = candidate["artifact"]["evaluation_contract"]
    if response_hypothesis_id not in contract["response_hypotheses"]:
        return withheld("RESPONSE_HYPOTHESIS_REQUIRED_OR_UNKNOWN")
    if shape_scenario not in contract["shape_scenarios"]:
        return withheld("SHAPE_SCENARIO_REQUIRED_OR_UNKNOWN")
    if (response_hypothesis_id != "approved_replacement"
        and assume_retained_hardware_serviceable_for_sensitivity is not True):
        return withheld("SERVICEABILITY_COUNTERFACTUAL_REQUIRED_FOR_REPAIR_SENSITIVITY")
    if not isinstance(failure_unit_id, str):
        return withheld("NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT")
    selected = contract["record_selection"][response_hypothesis_id][shape_scenario]
    record_id = selected.get(failure_unit_id)
    if record_id is None:
        return withheld("NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT")
    record = next(r for r in candidate["artifact"]["pathways"][0]["curve_records"]
                  if r["curve_id"] == record_id)
    # This source-native domain contains seven exact states. No interpolation,
    # extrapolation, thermal conversion or assumed ignition odds are executed.
    dr = dict(record["parameters"]["points"])[int(class_state)]
    value = candidate["values"]["units"][failure_unit_id]["value_usd_each"]
    loss = dr * value
    if not 0 <= dr <= 1 or not 0 <= loss <= value:
        raise ValueError("SAME_UNIT_CAP_FAILED")
    return {"status": "local_candidate_only", "reason": "BWF_Q01_LOCAL_TEST_NOT_CANONICAL",
            "dr": dr, "unit_conditional_mean_loss_usd": loss,
            "complete_plant_loss_usd": None, "annual_metrics_authorized": False,
            "curve_id": record_id,
            "limitation_flags": contract["limitation_flags"]}
