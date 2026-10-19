"""Author and audit a proposed BESS Wildfire candidate; no current release.

The class-response transfer is an analyst T4 hypothesis. The owner selected
only the consequence policy. Existing source/runtime files remain unchanged.
"""
from copy import deepcopy
import csv
from decimal import Decimal
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[7]
HERE = Path(__file__).resolve().parent
HOME = ROOT / "docs/cells/wildfire_bess/proposed/local_candidate_v0_1"
CELL, PATHWAY = "wildfire_bess", "wildfire_thermal_attack"
ENC, PCS = "BESS_INTEGRATED_ENCLOSURE", "BESS_SEPARATE_PCS"
SELECTOR = "BESS_LFP_R1_WILDFIRE_ORDINAL_LOCAL_V0_1"
T4 = "T4_placeholder_or_expert_judgment"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def csv_rows(path):
    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert all(None not in r and None not in r.values() for r in rows), path
    return rows


def dump(name, data):
    (HOME / name).write_text(json.dumps(data, indent=2) + "\n")


def write_csv(name, rows):
    with (HOME / name).open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main():
    spec_path = HERE / "experiment_spec.json"
    spec = json.loads(spec_path.read_text())
    assert spec["owner_ruling"]["words"] == "Test full replacement; retain repair sensitivities (Recommended)"
    index = ROOT / "docs/contracts/machine_readable_artifact_index.json"
    before = index.read_bytes()
    assert not any(x["cell_id"] == CELL for x in json.loads(before)["artifacts"])
    source = ROOT / spec["source_response"]["path"]
    assert sha(source) == spec["source_response"]["sha256"]
    source_bytes = source.read_bytes()
    source_artifact = json.loads(source_bytes)
    records = {r["curve_id"]: r for r in source_artifact["curve_records"]}
    weights = {
        "electronics_ordinal": records[spec["source_response"]["baseline_record"]]["parameters"]["points"],
        "heavy_electrical_ordinal": records[spec["source_response"]["sensitivity_record"]]["parameters"]["points"],
    }
    allocation_path = ROOT / spec["cost_allocation"]["path"]
    assert sha(allocation_path) == spec["cost_allocation"]["sha256"]
    cost = {r["cost_group"]: Decimal(r["projected_usd_per_enclosure"])
            for r in csv_rows(allocation_path)
            if r["allocation_case"] == spec["cost_allocation"]["case"]}
    assert abs(sum(cost.values()) - Decimal(1050000)) < Decimal("1e-8")
    end_costs = {
        "approved_replacement": Decimal(1050000),
        "noncell_repair_sensitivity": sum(v for k, v in cost.items() if k != "cells"),
        "limited_repair_sensitivity": cost["thermal_management"] + cost["enclosure_racks_fire_suppression"],
    }
    flags = ["LOCAL_TEST_ONLY_NOT_CANONICAL", "BESS_CLASS_RESPONSE_TRANSFER_T4_NOT_CALIBRATED",
             "SOURCE_DR_IS_NOT_IGNITION_PROBABILITY", "FSIM_CLASS_IS_NOT_LOCAL_HEAT_FLUX",
             "BWF_Q01_FULL_REPLACEMENT_AFTER_BATTERY_COMPROMISE", "PARTIAL_PROPERTY_SCOPE",
             "REPAIR_AND_SHAPE_SENSITIVITIES_ARE_UNWEIGHTED_HYPOTHESES",
             "NO_GENERIC_MITIGATION_CREDIT", "CROSS_UNIT_PROPAGATION_UNQUANTIFIED",
             "CURVE_INTRINSIC_SPREAD_NOT_CARRIED", "ANNUAL_SOURCE_COUPLING_NOT_QUALIFIED"]
    params = [
        dict(parameter_id="BWF-P07", scope="enclosure ordinal mean-response transfer", value=weights,
             tier=T4, source_ids=["BWF-S03", "BWF-S04", "BWF-S05"],
             reasoning="Electronics response is the simple reference for enclosed electronic/cooling/battery hardware; heavy electrical is a contrasting lower-response shape. Both are new T4 target transfers, not physical or probabilistic conversion of the donor DR.",
             update_trigger="Matched local attack, construction, inspected damage and same-unit repair costs"),
        dict(parameter_id="BWF-P08", scope="same-unit consequence policy", value={k: float(v) for k,v in end_costs.items()},
             tier=T4, source_ids=["BWF-S01", "BWF-S09", "BWF-S12"],
             reasoning="Owner selects full replacement for compromised battery contents; cheaper outcomes require the explicit retained-hardware serviceability counterfactual.",
             update_trigger="OEM disposition, actual repair BOM/costs or revised owner policy"),
        dict(parameter_id="BWF-P09", scope="PCS adjacent electrical transfer", value=weights["electronics_ordinal"],
             tier=T4, source_ids=["BWF-S01", "BWF-S03"],
             reasoning="Separate PCS has related enclosed power-electronic hardware; it is not battery contents or a whole GSU. Source response is retained without target calibration.",
             update_trigger="Matched PCS thermal exposure and repair evidence"),
        dict(parameter_id="BWF-P10", scope="site/cost/uncertainty controls", value="No blanket protection, no exposed-share default, no stochastic Damage-state draw, no residual zero",
             tier=T4, source_ids=["BWF-S01", "BWF-S02", "BWF-S08", "BWF-S10"],
             reasoning="Keep reference/context limits explicit; use per-unit conditional means only. Source BP, joint events and annual caps stay with Hazard.",
             update_trigger="Qualified consumer coupling or matched protection/propagation/value evidence"),
    ]
    curve_records, selection, answers = [], {}, []
    for hypothesis, dollars in end_costs.items():
        selection[hypothesis] = {}
        for shape, points in weights.items():
            cid = f"BWF01_ENC_{hypothesis}_{shape}"
            ratio = dollars / Decimal(1050000)
            ordinates = [[s, float(Decimal(str(w)) * ratio)] for s, w in points]
            curve_records.append(dict(curve_id=cid, pathway_id=PATHWAY, failure_unit_id=ENC,
                curve_form="piecewise_linear", x_axis="fsim_class_state_exact_integer_only",
                y_axis="failure_unit_damage_ratio", parameters={"points": ordinates},
                valid_range=[0,6], interpolation_policy="linear_between_source_knots",
                extrapolation_policy="reject every noninteger or unknown state; exact lookup only; no interpolation executed",
                selector_match={"reference_id": SELECTOR, "response_hypothesis_id": hypothesis, "shape_scenario": shape},
                source_parameter_refs=["BWF-P07", "BWF-P08", "BWF-P10"], metadata_flags=flags))
            selection[hypothesis][shape] = {ENC: cid, PCS: "BWF01_PCS_ELECTRONICS"}
            for state, w in points:
                answers.append(dict(failure_unit_id=ENC, class_state=state, response_hypothesis_id=hypothesis,
                    shape_scenario=shape, expected_dr=float(Decimal(str(w))*dollars/Decimal(1050000)),
                    expected_loss_usd=float(Decimal(str(w))*dollars)))
    curve_records.append(dict(curve_id="BWF01_PCS_ELECTRONICS", pathway_id=PATHWAY, failure_unit_id=PCS,
        curve_form="piecewise_linear", x_axis="fsim_class_state_exact_integer_only", y_axis="failure_unit_damage_ratio",
        parameters={"points": weights["electronics_ordinal"]}, valid_range=[0,6],
        interpolation_policy="linear_between_source_knots",
        extrapolation_policy="reject every noninteger or unknown state; exact lookup only; no interpolation executed",
        selector_match={"reference_id": SELECTOR}, source_parameter_refs=["BWF-P09", "BWF-P10"], metadata_flags=flags))
    for h in end_costs:
        for sh in weights:
            for state, w in weights["electronics_ordinal"]:
                answers.append(dict(failure_unit_id=PCS, class_state=state, response_hypothesis_id=h,
                    shape_scenario=sh, expected_dr=w, expected_loss_usd=float(Decimal(str(w))*Decimal(520000))))
    withheld = ["BESS_MV_AND_SHARED_ELECTRICAL", "BESS_CIVIL", "BESS_FIELDWORK"]
    units = [dict(id=ENC, subsystem="battery_enclosures", component="integrated battery/cooling/BMS/enclosure/safety",
                  treatment="primary_nonzero", y_axis="failure_unit_damage_ratio", denominator="same integrated enclosure physical hardware value"),
             dict(id=PCS, subsystem="pcs", component="separate bidirectional PCS",
                  treatment="primary_nonzero", y_axis="failure_unit_damage_ratio", denominator="same separate PCS physical hardware value")]
    units += [dict(id=u, subsystem=u, component="unbound reference property", treatment="withheld",
                   y_axis="failure_unit_damage_ratio", denominator="retained physical value row",
                   withheld_reason_codes=["NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT", "VALUE_ALLOCATION_OR_RESPONSE_UNQUALIFIED"]) for u in withheld]
    capability = dict(schema_version="capability_declaration.v3", cell_id=CELL, canonical_runtime_artifact=False,
        pathway_capabilities=[dict(pathway_id=PATHWAY, failure_unit_scalar_dr="conditional",
            scenario_loss_given_value_basis="conditional", curve_intrinsic_spread="not_carried",
            populated_emit_modes=["scalar_mean"], conditions=["Exact content pins and explicit local-test opt-in",
                "Exact class0..6 and explicit BESS reference, policy and shape",
                "Repair requires explicit serviceability counterfactual", "Same physical unit/value; no blanket exposure or protection multiplier"],
            limitation_flags=flags, withheld_failure_units=[dict(failure_unit_id=u, reason_codes=["NO_RUNTIME_CURVE_FOR_PATHWAY_UNIT"]) for u in withheld])],
        consumer_annual_metrics=dict(computation_owner="downstream_consumer", status_before_promotion="withheld_noncanonical_proposal",
            status_after_promotion="withheld", prerequisites=["Local source/footprint bridge qualification",
                "Annual joint coupling, original mass, per-unit caps and fixed-mass tail proof", "Separate canonical admission before production use"], limitation_flags=flags),
        cap_binding=dict(policy="consumer_enforced_fail_closed", enforcement_owner="downstream_consumer",
            checks_required=["One value per physical unit; enclosures already include their internals", "94.4M hardware does not become109.8M modeled value",
                             "No within-year restoration inferred; qualify annual per-unit caps separately"], action_if_fail="withhold affected response"),
        promotion_gate=dict(status="blocked", required_before_canonical_use=["Local Hazard exposure and consumer proof",
            "Scientific/capability review; owner cost choice is not response calibration", "Separate annual qualification"]))
    values = {**spec["value"], "units": {ENC:dict(count=80, value_usd_each=1050000), PCS:dict(count=20, value_usd_each=520000)},
              "reference_hashes":spec["reference_hashes"], "known_battery_compromise_cost_usd":1050000,
              "counterfactual_repair_costs_usd":{k:float(v) for k,v in end_costs.items() if k != "approved_replacement"},
              "complete_plant_loss_supported":False}
    dump("capability.json", capability)
    dump("value_binding.json", values)
    write_csv("value_crosswalk.csv", csv_rows(HERE.parent / "value_crosswalk.csv"))
    sources = csv_rows(HERE.parent / "sources.csv")
    sources.append(dict(source_id="BWF-S12", citation="Owner BWF-Q01 ruling2026-10-19",
        url_or_repo_path="docs/extra/discussion/bess_damage/09_wildfire_damage_intake.md", locator="BWF-Q01; experiment_spec.json owner_ruling",
        role="boundary_or_cap", tier=T4, measured_endpoint="Owner-selected local cost policy; not scientific calibration",
        permitted_inference="Test integrated replacement with repair sensitivities", prohibited_inference="Approved curve probabilities or annual/national release", disposition="adopt local policy"))
    write_csv("source_register.csv", sources)
    claims = csv_rows(HERE.parent / "claims.csv")
    common = dict(locator="experiment_spec.json; derivation.md; BWF-Q01", update_trigger="Matched evidence or later qualified version")
    claims += [dict(claim_id="BWF-C12", type="owner_ruling", source_ids="BWF-S12",
                    claim=spec["owner_ruling"]["words"], adopted_rule="Full replacement for compromised battery state, repair sensitivities retained",
                    reasoning="Local policy only; no class calibration approval", **common),
               dict(claim_id="BWF-C13", type="engineering_hypothesis", source_ids="BWF-S03;BWF-S04;BWF-S05",
                    claim="Related electrical ordinates are an ordinal mean-response template for the new BESS proxy",
                    adopted_rule="Reference electronics shape; heavy electrical alternative; no inferred ignition probability or Damage-state sampling",
                    reasoning="Minimal categorical hypothesis uses existing source axis and physical mechanism limits; absolute BESS transfer remains T4", **common),
               dict(claim_id="BWF-C14", type="engineering_hypothesis", source_ids="BWF-S01;BWF-S09;BWF-S12",
                    claim="Repair cases compare distinct retained-serviceable-hardware interpretations",
                    adopted_rule="Explicit serviceability counterfactual required; do not use repair on known compromised cells",
                    reasoning="Same severity weight is held for a controlled economic sensitivity; alternatives are not confidence bounds", **common)]
    write_csv("claim_parameter_register.csv", claims)
    write_csv("parameter_register.csv", [dict(parameter_id=p["parameter_id"],scope=p["scope"],value=json.dumps(p["value"]),tier=p["tier"],source_ids=";".join(p["source_ids"]),reasoning=p["reasoning"],update_trigger=p["update_trigger"]) for p in params])
    home = str(HOME.relative_to(ROOT))
    artifact = dict(schema_version="damage_curve_record_bundle.v3", schema_status="proposed_draft", cell_id=CELL,
        damage_code_id="BESS_WILDFIRE_LOCAL_CANDIDATE_V0_1", semantic_damage_model_version="model v0.1", documentation_revision="docs r1",
        lifecycle_state="local_test_candidate", promotion_status="not_canonical_not_in_runtime_index", model_grade="screening_engineering_hypothesis_t4",
        package_release="unreleased",package_baseline="library v2.5",package_inclusion_status="not_included",canonical_runtime_artifact=False,
        source_dossier=home+"/derivation.md",source_workbook=home+"/value_crosswalk.csv",known_answer_tests=home+"/known_answers.json",
        source_register=home+"/source_register.csv",claim_parameter_register=home+"/claim_parameter_register.csv",value_crosswalk=home+"/value_crosswalk.csv",
        failure_units=units, pathways=[dict(pathway_id=PATHWAY,
            hazard_scope=dict(included="exogenous wildfire unit thermal response proxy",deferred=["cross_unit_propagation","postfire_erosion","remediation"],
                              excluded=["autonomous_equipment_fire","BI","performance","collector_station_export"]),
            hazard_axis=dict(id="FSIM_CLASS_EXACT",preferred_input_field="class_state",unit="source_native_categorical_class",valid_range=[0,6],
                             extrapolation_policy="exact integer state0..6 only; no midpoint, heat-flux conversion, interpolation or extrapolation"),
            selector_logic=[dict(reference_id=SELECTOR)],conditioner_logic=[],
            exposure_contract=dict(unit="one physical enclosure or PCS",required_support="declared local native class; geometry coupling separately qualified",
                                   unknown="withhold; no default zero or at-risk share",mitigation_credit="none",frequency="BP excluded from Damage call"),
            failure_unit_coverage=[dict(failure_unit_id=u["id"],status="conditional_local_test" if u["treatment"]=="primary_nonzero" else "withheld") for u in units],curve_records=curve_records)],
        value_linkage=dict(value_binding_path=home+"/value_binding.json",value_binding_sha256=sha(HOME/"value_binding.json"),
                           full_tiv_usd=109800000,candidate_hardware_usd=94400000,unbound_property_usd=15400000),
        parameter_tier_table=params, evaluation_contract=dict(production_runtime_authorized=False,explicit_local_test_opt_in_required=True,
            pathway_id=PATHWAY,reference_id=SELECTOR,response_hypotheses=list(end_costs),shape_scenarios=list(weights),
            record_selection=selection,default_response_hypothesis=None,default_shape_scenario=None,
            exact_state_only=True,repair_serviceability_counterfactual_required=True,limitation_flags=flags),
        emit_contract=dict(schema_version="damage_emit.v2",populated_emit_modes_for_this_cell=["scalar_mean"]),
        capability_declaration=capability,derivation_rationale=dict(source_artifact_sha256=sha(source),source_artifact_path=str(source.relative_to(ROOT)),
            experiment_spec_sha256=sha(spec_path),owner_local_policy=spec["owner_ruling"],
            interpretation=spec["source_response"]["interpretation"],not_a_damage_probability_distribution=True))
    dump("curve_artifact.json", artifact)
    dump("known_answers.json", dict(cases=answers,independent_basis="Decimal arithmetic on pinned donor ordinates and cost allocations; not measured BESS data"))
    pinned=["curve_artifact.json","capability.json","value_binding.json","value_crosswalk.csv","source_register.csv",
            "claim_parameter_register.csv","parameter_register.csv","known_answers.json","evaluate_local.py"]
    dump("consumption_pin.json",dict(cell_id=CELL,model="model v0.1",docs="docs r1",canonical_runtime_artifact=False,
                                     sha256={n:sha(HOME/n) for n in pinned}))
    schema_dir=ROOT/"docs/contracts/schemas"
    cap_schema=json.loads((schema_dir/"capability_declaration.v3.schema.json").read_text())
    registry=Registry().with_resource(cap_schema["$id"],Resource.from_contents(cap_schema))
    Draft202012Validator(json.loads((schema_dir/"curve_artifact_bundle.v3.schema.json").read_text()),registry=registry).validate(artifact)
    Draft202012Validator(cap_schema).validate(capability)
    module_spec=importlib.util.spec_from_file_location("wildfire_bess_candidate",HOME/"evaluate_local.py")
    evaluator=importlib.util.module_from_spec(module_spec);module_spec.loader.exec_module(evaluator)
    try:evaluator.load_candidate()
    except ValueError as exc:assert "OPT_IN_REQUIRED" in str(exc)
    else:raise AssertionError("opt-in bypass")
    loaded=evaluator.load_candidate(allow_local_test=True)
    def call(**updates):
        request=dict(failure_unit_id=ENC,class_state=4,pathway_id=PATHWAY,selector_id=SELECTOR,
                     response_hypothesis_id="approved_replacement",shape_scenario="electronics_ordinal")
        request.update(updates)
        return evaluator.evaluate(loaded,**request)
    comparison=[]
    for case in answers:
        request={k:v for k,v in case.items() if not k.startswith("expected_")}
        actual=call(**request,assume_retained_hardware_serviceable_for_sensitivity=True)
        assert abs(actual["dr"]-case["expected_dr"])<1e-14
        assert abs(actual["unit_conditional_mean_loss_usd"]-case["expected_loss_usd"])<1e-8
        comparison.append({**case,"actual_dr":actual["dr"],"actual_loss_usd":actual["unit_conditional_mean_loss_usd"]})
    negatives=[dict(class_state=s) for s in [-1,7,1.5,True,None,"3",float("nan"),float("inf")]]
    negatives += [dict(pathway_id="autonomous_battery_fire"),dict(pathway_id=None),dict(selector_id=None),dict(response_hypothesis_id=None),
                  dict(shape_scenario=None),dict(shape_scenario="p90"),dict(failure_unit_id=withheld[0]),dict(burn_probability=.1),
                  dict(response_hypothesis_id="limited_repair_sensitivity"),dict(response_hypothesis_id="noncell_repair_sensitivity",assume_retained_hardware_serviceable_for_sensitivity="yes"),dict(failure_unit_id=[])]
    for n in negatives:
        actual=call(**n);assert actual["dr"] is None and actual["unit_conditional_mean_loss_usd"] is None
    for name in ["curve_artifact.json","capability.json","value_binding.json"]:
        with tempfile.TemporaryDirectory() as d:
            copy=Path(d)/"candidate";shutil.copytree(HOME,copy)
            with (copy/name).open("a") as f:f.write("\n")
            try:evaluator.load_candidate(copy,allow_local_test=True)
            except ValueError as exc:assert "CANDIDATE_SHA_MISMATCH" in str(exc)
            else:raise AssertionError("tampered payload admitted")
    src_ids={s["source_id"] for s in sources};assert len(src_ids)==len(sources)
    for c in claims:assert set(c["source_ids"].split(";"))<=src_ids
    for p in params:assert set(p["source_ids"])<=src_ids
    for name in ["source_dossier","source_workbook","known_answer_tests","source_register","claim_parameter_register","value_crosswalk"]:
        assert (ROOT/artifact[name]).is_file(),name
    assert index.read_bytes()==before and source.read_bytes()==source_bytes
    assert sum(Decimal(r["included_usd"]) for r in csv_rows(HOME/"value_crosswalk.csv"))==Decimal(109800000)
    write_csv("conditional_comparisons.csv",comparison)
    uniform = []
    for h in end_costs:
        for sh in weights:
            for state in range(7):
                amounts = {u: call(failure_unit_id=u, class_state=state, response_hypothesis_id=h,
                                  shape_scenario=sh, assume_retained_hardware_serviceable_for_sensitivity=True)
                           for u in (ENC, PCS)}
                total = 80*amounts[ENC]["unit_conditional_mean_loss_usd"] + 20*amounts[PCS]["unit_conditional_mean_loss_usd"]
                assert 0 <= total <= 94400000
                uniform.append(dict(response_hypothesis_id=h, shape_scenario=sh, class_state=state,
                    one_enclosure_mean_usd=amounts[ENC]["unit_conditional_mean_loss_usd"],
                    one_pcs_mean_usd=amounts[PCS]["unit_conditional_mean_loss_usd"],
                    uniform_class_hardware_mean_usd=total, uniform_class_percent_full_tiv=100*total/109800000,
                    annual_result=False, complete_property_result=False))
    write_csv("uniform_class_pressure_test.csv", uniform)
    validation=dict(status="PASS",classification="NEW_CELL_SCAFFOLD",scope="owner-selected local conditional testing; no canonical or annual admission",
        schemas="existing bundle_v3/capability_v3 unchanged",exact_conditional_comparisons=len(answers),negative_response_controls=len(negatives),
        opt_in_controls=1,tampered_payload_controls=3,known_answer_cases=len(answers),value_rows_reconciled=10,
        source_records=len(sources),claim_records=len(claims),curve_records=len(curve_records),
        artifact_sha256=sha(HOME/"curve_artifact.json"),canonical_runtime_artifact=False,runtime_index_changed=False,
        annual_metrics_qualified=False,curve_intrinsic_spread_carried=False)
    dump("validation.json",validation)
    (HERE/"validation.json").write_text(json.dumps(validation,indent=2)+"\n")
    print(json.dumps(validation,indent=2))


if __name__ == "__main__":
    main()
