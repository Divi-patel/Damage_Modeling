"""Build and validate the owner-selected, noncanonical BESS Hurricane proposal."""
from copy import deepcopy
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[7]
HERE = Path(__file__).resolve().parent
HOME = ROOT / "docs/cells/tropical_cyclone_wind_bess/proposed/local_candidate_v0_1"
CELL = "tropical_cyclone_wind_bess"
PATHWAY = "tropical_cyclone_wind"
ENC = "BESS_INTEGRATED_ENCLOSURE"
PCS = "BESS_SEPARATE_PCS"
T4 = "T4_placeholder_or_expert_judgment"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read_csv(p):
    with p.open(newline="") as f:
        return list(csv.DictReader(f))


def csv_write(name, rows):
    with (HOME / name).open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)


def dump(name, value):
    (HOME / name).write_text(json.dumps(value, indent=2) + "\n")


def main():
    HOME.mkdir(parents=True, exist_ok=True)
    spec_path = HERE / "experiment_spec.json"
    spec = json.loads(spec_path.read_text())
    assert spec["owner_ruling"]["words"] == "Test full replacement; retain repair as a sensitivity (Recommended)"
    assert spec["owner_ruling"]["scope"] == "local testing only"
    index = ROOT / "docs/contracts/machine_readable_artifact_index.json"
    index_before = index.read_bytes()
    source_path = ROOT / spec["source_response"]["path"]
    assert sha(source_path) == spec["source_response"]["sha256"]
    source_before = source_path.read_bytes()
    source_artifact = json.loads(source_before)
    original = next(r for r in source_artifact["pathways"][0]["curve_records"] if r["curve_id"] == spec["source_response"]["curve_id"])
    state_rows = read_csv(HERE / "state_costs.csv")
    costs = {p: [float(r["cabinet_cost_fraction"]) for r in state_rows if r["repair_policy"] == p] for p in spec["repair_policies"]}
    records = []
    mappings = {"approved_replacement": {}, "repair_sensitivity": {}}
    for name, hypothesis, policy in [("BESS_ENCLOSURE_TC_REPLACE_MAJOR_V0_1", "approved_replacement", "replace_at_major_compromise"), ("BESS_ENCLOSURE_TC_REPAIR_SENSITIVITY_V0_1", "repair_sensitivity", "repair_if_contained_hardware_serviceable")]:
        record = deepcopy(original)
        record.update(curve_id=name, failure_unit_id=ENC, x_axis="bess_tc_event_to_reference_pressure_ratio")
        for i, state in enumerate(record["parameters"]["damage_states"]):
            state.update(state_id=f"{name}_DS{i}", cost_ratio=costs[policy][i], affected_subsystems=[] if i == 0 else ["integrated_battery_enclosure"], description=f"{spec['states'][i]}; {policy}; selected engineering policy, not measured damage", tier=T4, source_ids=["BW-S02", "BW-S11", "BW-S12"])
        records.append(record); mappings[hypothesis][ENC] = name
    pcs_record = deepcopy(original)
    pcs_record.update(curve_id="BESS_SEPARATE_PCS_TC_PROXY_V0_1", failure_unit_id=PCS, x_axis="bess_tc_event_to_reference_pressure_ratio")
    for i, state in enumerate(pcs_record["parameters"]["damage_states"]):
        state.update(state_id=f"BESS_PCS_TC_DS{i}", affected_subsystems=[] if i == 0 else ["separate_pcs"], description="Related electrical-equipment T4 transfer; not matched OEM fragility", source_ids=["BW-S02", "BW-S03"])
    records.append(pcs_record)
    for record in records:
        for scenario in record["parameters"]["capacity_scenarios"]:
            scenario["source_ids"] = ["BW-S02"]
    for hypothesis in mappings:
        mappings[hypothesis][PCS] = pcs_record["curve_id"]
    units = [{"id": ENC, "subsystem": "battery_enclosures", "component": "integrated cabinet and included internal hardware", "treatment": "primary_nonzero", "y_axis": "failure_unit_damage_ratio", "denominator": "same integrated enclosure pre-event physical replacement proxy"}, {"id": PCS, "subsystem": "pcs", "component": "separate PCS group", "treatment": "primary_nonzero", "y_axis": "failure_unit_damage_ratio", "denominator": "same separate PCS pre-event physical replacement proxy"}]
    withheld = ["BESS_MV_AND_SHARED_ELECTRICAL", "BESS_CIVIL", "BESS_FIELDWORK"]
    for unit in withheld:
        units.append({"id": unit, "subsystem": unit, "component": "unbound reference property", "treatment": "withheld", "y_axis": "failure_unit_damage_ratio", "denominator": "retained reference budget row", "withheld_reason_codes": ["NO_QUALIFIED_WIND_RESPONSE_OR_ALLOCATION"]})
    flags = ["LOCAL_TEST_ONLY_NOT_CANONICAL", "T4_PROBABILITY_TRANSFER_NOT_CALIBRATED", "BW_Q01_CONSERVATIVE_REPLACEMENT_POLICY", "REPAIR_AND_RESISTANCE_SENSITIVITIES_NOT_CONFIDENCE_INTERVALS", "BESS_WIND_REFERENCE_NOT_YET_QUALIFIED", "PARTIAL_PROPERTY_SCOPE", "WIND_ONLY_DEBRIS_RAIN_INGRESS_AND_SPREAD_UNQUANTIFIED", "UNKNOWN_TC_DURATION_CLASS", "UNKNOWN_TC_DIRECTION_EVOLUTION_CLASS"]
    capability = {"schema_version": "capability_declaration.v3", "cell_id": CELL, "canonical_runtime_artifact": False, "pathway_capabilities": [{"pathway_id": PATHWAY, "failure_unit_scalar_dr": "conditional", "scenario_loss_given_value_basis": "conditional", "curve_intrinsic_spread": "not_carried", "populated_emit_modes": ["scalar_mean"], "conditions": ["Exact artifact/value/capability pins", "Explicit local-test opt-in", "Explicit response hypothesis and unweighted resistance scenario", "Declared comparable normalized-demand basis and valid source domain", "Unique physical unit and same-unit value"], "limitation_flags": flags, "withheld_failure_units": [{"failure_unit_id": u, "reason_codes": ["NO_QUALIFIED_WIND_RESPONSE_OR_ALLOCATION"]} for u in withheld]}], "consumer_annual_metrics": {"computation_owner": "downstream_consumer", "status_before_promotion": "withheld_noncanonical_proposal", "status_after_promotion": "withheld", "prerequisites": ["Separate local Hazard source/reference bridge and coupling proof", "Separate annual loss, physical cap and fixed-mass tail qualification", "Governed canonical promotion before production use"], "limitation_flags": flags}, "cap_binding": {"policy": "consumer_enforced_fail_closed", "enforcement_owner": "downstream_consumer", "checks_required": ["One integrated value per unique enclosure; do not add its internals again", "One separate PCS value per unit", "No renormalization of94.4M candidate hardware to109.8M full TIV", "No within-year replacement assumptions inferred from occurrence response"], "action_if_fail": "withhold affected response"}, "promotion_gate": {"status": "blocked", "required_before_canonical_use": ["Hazard local target/reference bridge qualification", "Scientific and capability review beyond local-test approval", "Separate annual qualification before EAL/PML/VaR/TVaR"]}}
    dump("capability.json", capability)
    values = {"full_tiv_usd": 109_800_000, "candidate_hardware_usd": 94_400_000, "unbound_property_usd": 15_400_000, "currency_basis": "fixed_2024_USD", "units": {ENC: {"count": 80, "value_usd_each": 1_050_000}, PCS: {"count": 20, "value_usd_each": 520_000}}, "profile_sha256": sha(ROOT.parent / "Hazard_modeling/docs/plans/_cross_cutting/bess_conus/asset_model.json"), "allocation_source_sha256": sha(ROOT / spec["cost_allocation"]["path"]), "complete_plant_loss_supported": False}
    dump("value_binding.json", values)
    budget = read_csv(ROOT.parent / "Hazard_modeling/docs/plans/_cross_cutting/bess_conus/reference_budget.csv")
    value_rows = [{"source_row": r["row_id"], "target_group": r["target_group"], "included_usd": r["included_usd"], "excluded_source_usd": r["excluded_usd"], "candidate_failure_unit": ENC if r["target_group"] == "battery_enclosures" else PCS if r["target_group"] == "pcs" else "UNBOUND_OR_EXCLUDED", "status": "local_candidate" if r["target_group"] in ["battery_enclosures", "pcs"] else "unbound_not_zero" if float(r["included_usd"]) > 0 else "outside_physical_scope"} for r in budget]
    csv_write("value_crosswalk.csv", value_rows)
    csv_write("source_register.csv", read_csv(HERE.parent / "sources.csv") + read_csv(HERE / "sources.csv"))
    claims = read_csv(HERE.parent / "claims.csv")
    # The first pass uses numerical_status rather than status; snapshot one explicit convention.
    claims = [{"claim_id": r["claim_id"], "claim_type": r["claim_type"], "source_ids": r["source_ids"], "exact_locator": r["exact_locator"], "statement": r["statement"], "status": r["numerical_status"], "prohibited_inference": r["prohibited_inference"], "update_trigger": r["update_trigger"]} for r in claims]
    claims += read_csv(HERE / "claims.csv")
    claims.append({"claim_id": "BW-C16", "claim_type": "owner_ruling", "source_ids": "BW-S01", "exact_locator": "BW-Q01 owner reply2026-10-19; experiment_spec.json owner_ruling", "statement": spec["owner_ruling"]["words"], "status": "approved_local_testing_only", "prohibited_inference": "Annual admission or empirical calibration", "update_trigger": "Later qualification or matched evidence"})
    csv_write("claim_parameter_register.csv", claims)
    params = read_csv(HERE / "parameter_register.csv")
    csv_write("parameter_register.csv", params)
    home = str(HOME.relative_to(ROOT))
    artifact = {"schema_version": "damage_curve_record_bundle.v3", "schema_status": "proposed_draft", "cell_id": CELL, "damage_code_id": "BESS_TC_WIND_LOCAL_CANDIDATE_V0_1", "semantic_damage_model_version": "model v0.1", "documentation_revision": "docs r1", "lifecycle_state": "local_test_candidate", "promotion_status": "not_canonical_not_in_runtime_index", "package_release": "unreleased", "package_baseline": "library v2.5", "package_inclusion_status": "not_included", "canonical_runtime_artifact": False, "source_dossier": home + "/derivation.md", "source_workbook": home + "/value_crosswalk.csv", "known_answer_tests": home + "/known_answers.json", "source_register": home + "/source_register.csv", "claim_parameter_register": home + "/claim_parameter_register.csv", "value_crosswalk": home + "/value_crosswalk.csv", "failure_units": units, "pathways": [{"pathway_id": PATHWAY, "hazard_scope": {"included": "conditional direct TC wind", "deferred": ["debris", "wind_driven_rain", "triggered_propagation"], "neighboring": ["flood", "strong_wind", "tornado"], "autonomous_failure": "outside_scope"}, "hazard_axis": {"id": "bess_tc_event_to_reference_pressure_ratio", "preferred_input_field": "pressure_ratio", "unit": "dimensionless comparable pressure-demand/reference ratio", "valid_range": [0, 2], "extrapolation_policy": "withhold outside range; no clamp"}, "selector_logic": [{"reference": "standalone_outdoor_liquid_cooled_LFP_r1"}], "conditioner_logic": [], "exposure_contract": {"scope": "one physical unit at declared local demand", "unknown_demand": "withhold", "height_or_protection_credit": "none"}, "failure_unit_coverage": [{"failure_unit_id": u["id"], "status": "conditional_local_test" if u["treatment"] == "primary_nonzero" else "withheld"} for u in units], "curve_records": records}], "value_linkage": {"value_binding_path": home + "/value_binding.json", "value_binding_sha256": sha(HOME / "value_binding.json"), "full_tiv_usd": values["full_tiv_usd"], "candidate_hardware_usd": values["candidate_hardware_usd"], "unbound_property_usd": values["unbound_property_usd"]}, "parameter_tier_table": params, "evaluation_contract": {"production_runtime_authorized": False, "explicit_local_test_opt_in_required": True, "approved_policy_id": "BW_Q01_LOCAL_MAJOR_REPLACEMENT", "curve_selection_by_response_hypothesis": mappings, "default_response_hypothesis": None, "national_reference_selected": False, "required_local_demand_basis_id": "BESS_TC_LOCAL_PRESSURE_RATIO_RESEARCH_V1", "limitation_flags": flags}, "emit_contract": {"schema_version": "damage_emit.v2", "populated_emit_modes_for_this_cell": ["scalar_mean"]}, "capability_declaration": capability, "derivation_rationale": {"source_artifact_path": str(source_path.relative_to(ROOT)), "source_artifact_sha256": sha(source_path), "owner_local_policy": spec["owner_ruling"], "research_spec_sha256": sha(spec_path), "shape": "T4 transfer, no fitted BESS observations", "costs": "Cabinet-specific projected composite costs; full replacement at approved major state", "consumer_boundary": "No annual or complete-plant result"}}
    dump("curve_artifact.json", artifact)
    known = []
    probes = read_csv(HERE / "response_probes.csv")
    for p in probes:
        if p["resistance_scenario"] == "central_screening" and float(p["pressure_ratio"]) in (0.0, 0.5, 1.0, 1.5, 2.0):
            for unit, field in [(ENC, "enclosure_mean_dr"), (PCS, "pcs_proxy_mean_dr")]:
                known.append({"failure_unit_id": unit, "pressure_ratio": float(p["pressure_ratio"]), "response_hypothesis_id": "approved_replacement" if p["repair_policy"] == "replace_at_major_compromise" else "repair_sensitivity", "resistance_scenario": p["resistance_scenario"], "expected_dr": float(p[field]), "expected_basis": "Independent research state-cost expectation; not measured"})
    dump("known_answers.json", {"cases": known, "not_field_calibration": True})
    pinned = ["curve_artifact.json", "capability.json", "value_binding.json", "value_crosswalk.csv", "source_register.csv", "claim_parameter_register.csv", "parameter_register.csv", "known_answers.json", "evaluate_local.py"]
    dependency = "scripts/reference_helpers/tropical_cyclone_wind_solar_v2_curve_eval.py"
    dump("consumption_pin.json", {"cell_id": CELL, "model": "model v0.1", "docs": "docs r1", "sha256": {n: sha(HOME / n) for n in pinned}, "dependency_sha256": {dependency: sha(ROOT / dependency)}, "canonical_runtime_artifact": False})
    schema_dir = ROOT / "docs/contracts/schemas"
    schema = json.loads((schema_dir / "curve_artifact_bundle.v3.schema.json").read_text())
    cap_schema = json.loads((schema_dir / "capability_declaration.v3.schema.json").read_text())
    registry = Registry().with_resource(cap_schema["$id"], Resource.from_contents(cap_schema))
    Draft202012Validator(schema, registry=registry).validate(artifact)
    Draft202012Validator(cap_schema).validate(capability)
    module_spec = importlib.util.spec_from_file_location("bess_wind_local", HOME / "evaluate_local.py")
    evaluator = importlib.util.module_from_spec(module_spec); module_spec.loader.exec_module(evaluator)
    try:
        evaluator.load_candidate()
    except ValueError as exc:
        assert "OPT_IN_REQUIRED" in str(exc)
    else:
        raise AssertionError("local opt-in bypass")
    loaded = evaluator.load_candidate(allow_local_test=True)
    def call(unit, x, hypothesis, scenario="central_screening", **updates):
        request = dict(failure_unit_id=unit, pressure_ratio=x, pathway_id=PATHWAY, demand_basis_id="BESS_TC_LOCAL_PRESSURE_RATIO_RESEARCH_V1", response_hypothesis_id=hypothesis, resistance_scenario=scenario)
        request.update(updates); return evaluator.evaluate(loaded, **request)
    checked = 0; max_delta = 0
    for p in probes:
        hypothesis = "approved_replacement" if p["repair_policy"] == "replace_at_major_compromise" else "repair_sensitivity"
        for unit, field in [(ENC, "enclosure_mean_dr"), (PCS, "pcs_proxy_mean_dr")]:
            result = call(unit, float(p["pressure_ratio"]), hypothesis, p["resistance_scenario"])
            delta = abs(result["dr"] - float(p[field])); max_delta = max(max_delta, delta)
            assert delta < 1e-14 and result["complete_plant_loss_usd"] is None
            checked += 1
    negatives = [dict(x=-1), dict(x=2.001), dict(x=True), dict(x=float("nan")), dict(x=float("inf")), dict(x=None), dict(x="1.0"), dict(pathway_id="tornado"), dict(demand_basis_id="unbridged_10m_gust"), dict(hypothesis=None), dict(resistance_scenario="probabilistic_p90"), dict(resistance_scenario=None), dict(unit="BESS_MV_AND_SHARED_ELECTRICAL"), dict(unit=None)]
    for update in negatives:
        args = dict(unit=ENC, x=1.0, hypothesis="approved_replacement"); args.update(update)
        result = call(**args)
        assert result["dr"] is None and result["unit_candidate_loss_usd"] is None
    assert sum(float(r["included_usd"]) for r in value_rows) == 109_800_000
    assert source_path.read_bytes() == source_before
    assert index.read_bytes() == index_before
    sources = {r["source_id"] for r in read_csv(HOME / "source_register.csv")}
    for row in claims + params:
        assert set(row["source_ids"].split(";")) <= sources
    for record in records:
        for row in record["parameters"]["damage_states"] + record["parameters"]["capacity_scenarios"]:
            assert set(row["source_ids"]) <= sources
    for name in ("source_dossier", "source_workbook", "known_answer_tests", "source_register", "claim_parameter_register", "value_crosswalk"):
        assert (ROOT / artifact[name]).is_file(), name
    for name in ("curve_artifact.json", "value_binding.json", "capability.json"):
        with tempfile.TemporaryDirectory() as temporary:
            copy = Path(temporary) / "proposal"
            shutil.copytree(HOME, copy)
            with (copy / name).open("a") as stream:
                stream.write("\n")
            try:
                evaluator.load_candidate(copy, allow_local_test=True)
            except ValueError as exc:
                assert "CANDIDATE_SHA_MISMATCH" in str(exc)
            else:
                raise AssertionError(f"tampered candidate admitted: {name}")
    with tempfile.TemporaryDirectory() as temporary:
        copy = Path(temporary) / "proposal"
        shutil.copytree(HOME, copy)
        copied_pin = json.loads((copy / "consumption_pin.json").read_text())
        copied_pin["dependency_sha256"][dependency] = "0" * 64
        (copy / "consumption_pin.json").write_text(json.dumps(copied_pin))
        try:
            evaluator.load_candidate(copy, allow_local_test=True)
        except ValueError as exc:
            assert "NUMERICAL_DEPENDENCY_SHA_MISMATCH" in str(exc)
        else:
            raise AssertionError("unmatched numerical dependency admitted")
    validation = {"status": "PASS", "classification": "NEW_CELL_SCAFFOLD", "candidate_state": "owner_selected_local_test", "schemas": "existing bundle_v3 and capability_v3; unchanged", "exact_parity_evaluations": checked, "negative_response_controls": len(negatives), "explicit_optin_control": 1, "tampered_payload_controls": 3, "dependency_pin_control": 1, "source_records": len(sources), "claim_records": len(claims), "max_dr_abs_delta": max_delta, "known_answer_cases": len(known), "value_rows_reconciled": len(value_rows), "canonical_runtime_artifact": False, "runtime_index_changed": False, "annual_metrics_qualified": False, "artifact_sha256": sha(HOME / "curve_artifact.json")}
    dump("validation.json", validation); print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
