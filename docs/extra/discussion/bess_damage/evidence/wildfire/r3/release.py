"""Author/validate the first conditional BESS Wildfire screening release.

Damage emits severity only. Hazard owns every annual calculation. This evidence
utility is not a Hazard production dependency and never changes prior proposals.
"""
from copy import deepcopy
import csv
import hashlib
import json
from pathlib import Path
import shutil

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[7]
HERE = Path(__file__).resolve().parent
CELL = ROOT / "docs/cells/wildfire_bess"
OLD = CELL / "proposed/local_candidate_v0_1"
CURRENT = CELL / "current"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read(p):
    return json.loads(p.read_text())


def write(p, data):
    p.write_text(json.dumps(data, indent=2)+"\n")


def build():
    if CURRENT.exists():
        raise FileExistsError(CURRENT)
    proof = read(HERE/"annual_qualification.json")
    assert proof["status"] == "passed" and proof["physical_unit_caps_passed"]
    assert proof["max_marginal_rate_delta"] < 1e-14
    assert proof["max_metric_replay_delta_usd"] <= 1e-5
    assert proof["max_aep_array_replay_delta_usd"] == 0
    assert proof["max_oep_array_replay_delta_usd"] == 0
    CURRENT.mkdir()
    for name in ("value_crosswalk.csv", "source_register.csv", "claim_parameter_register.csv",
                 "parameter_register.csv", "known_answers.json"):
        shutil.copyfile(OLD/name, CURRENT/name)
    a, c, v = [deepcopy(read(OLD/n)) for n in
               ("curve_artifact.json", "capability.json", "value_binding.json")]
    flags = [f for f in c["consumer_annual_metrics"]["limitation_flags"] if f not in
             ("LOCAL_TEST_ONLY_NOT_CANONICAL", "ANNUAL_SOURCE_COUPLING_NOT_QUALIFIED")]
    flags += ["COMMON_RATE_AND_CLASS_RANK_SCREENING_DEPENDENCE",
        "ORIGINAL_SOURCE_AND_UNKNOWN_CLOCKS_RETAINED",
        "PER_PHYSICAL_UNIT_ANNUAL_CAP_NO_RESTORATION", "LOCAL_PROOF_NOT_NATIONAL_ADMISSION"]
    c["canonical_runtime_artifact"] = True
    for p in c["pathway_capabilities"]:
        p["conditions"][0] = "Exact model v1.0/docs r1 content pins and compatible declared reference"
        p["limitation_flags"] = flags
    annual = c["consumer_annual_metrics"]
    annual["status_after_promotion"] = "consumer_computable_from_validated_frequency_intensity_coupling_value_and_cap_model"
    annual["prerequisites"] = [
        "Exact artifact/capability/value/profile pins and exact class0..6 lookup",
        "Explicit consequence policy and unweighted shape; serviceability counterfactual for repairs",
        "Qualified native source demand; no fire frequency or heat-flux bridge inside Damage",
        "Declared common-event screening dependence preserving every unit rate/class marginal",
        "Original source support, unknown clocks and positive-BP/no-FLP exclusions retained",
        "Unique physical units; separate cumulative annual caps; no within-year restoration",
        "Qualified annual AEP/OEP arrays and independent mean, cap and fixed-mass-tail checks",
        "Mean Damage response only; no inferred intrinsic severity spread",
        "Partial property; national support, publication and recipient admission remain separate"]
    annual["limitation_flags"] = flags
    c["cap_binding"]["checks_required"] += [
        "Cap each physical unit before summing plant annual loss; dry units cannot lend value",
        "AEP and OEP retain the same declared events and original source weights"]
    c["promotion_gate"] = {"status": "passed", "required_before_canonical_use": [
        "Every consumer must satisfy all conditional-use prerequisites for its exact support and run"]}
    v.update(annual_cap_policy="per_physical_unit_no_within_year_restoration",
             use="partial_scope_annual_screening", intrinsic_damage_spread="not_carried")
    write(CURRENT/"value_binding.json", v)
    write(CURRENT/"capability.json", c)
    a.update(schema_status="released", damage_code_id="BESS_WILDFIRE_SCREENING_V1",
        semantic_damage_model_version="model v1.0", documentation_revision="docs r1",
        lifecycle_state="repository_canonical_conditional_screening",
        promotion_status="conditional_consumer_annual_use_qualified", canonical_runtime_artifact=True,
        package_inclusion_status="repository_canonical_not_in_portable_package",
        model_grade="screening_T4_not_calibrated", review_status="same_author_with_independent_numerical_methods")
    for key in ("source_dossier", "source_workbook", "known_answer_tests", "source_register",
                "claim_parameter_register", "value_crosswalk"):
        a[key] = str((CURRENT/Path(a[key]).name).relative_to(ROOT))
    a["value_linkage"]["value_binding_path"] = str((CURRENT/"value_binding.json").relative_to(ROOT))
    a["value_linkage"]["value_binding_sha256"] = sha(CURRENT/"value_binding.json")
    a["evaluation_contract"].update(production_runtime_authorized=True,
        explicit_local_test_opt_in_required=False, reference_id="BESS_LFP_R1_WILDFIRE_ORDINAL_V1",
        annual_qualification_evidence=str((HERE/"annual_qualification.json").relative_to(ROOT)),
        limitation_flags=flags)
    a["capability_declaration"] = c
    a["derivation_rationale"]["predecessor_candidate_sha256"] = sha(OLD/"curve_artifact.json")
    a["derivation_rationale"]["consumer_boundary"] = "Conditional annual screening after exact frequency/coupling/value/cap/distribution prerequisites; complete property withheld"
    for unit in a["pathways"][0]["failure_unit_coverage"]:
        if unit["status"] == "conditional_local_test":
            unit["status"] = "conditional_screening"
    write(CURRENT/"curve_artifact.json", a)
    write(CURRENT/"validation.json", {"status":"passed_conditional_annual_screening",
        "classification":"NEW_CELL_MODEL_RELEASE", "schema_change":False,
        "conditional_records_and_unit_values":"exactly_unchanged_from_v0_1",
        "qualification":proof, "portable_package_issued":False,"national_admission":False})
    names = ("curve_artifact.json", "capability.json", "value_binding.json", "value_crosswalk.csv",
        "source_register.csv", "claim_parameter_register.csv", "parameter_register.csv",
        "known_answers.json", "validation.json")
    write(CURRENT/"consumption_pin.json", {"cell_id":a["cell_id"], "semantic_damage_model_version":"model v1.0",
        "documentation_revision":"docs r1", "canonical_runtime_artifact":True,
        "sha256":{n:sha(CURRENT/n) for n in names}})
    index = read(ROOT/"docs/contracts/machine_readable_artifact_index.json")
    assert not any(r["cell_id"]==a["cell_id"] for r in index["artifacts"])
    index["repository_contract_revision"] = "2026-10-19.bess-wildfire-screening-v1"
    index["artifacts"].append({"cell_id":a["cell_id"],"damage_code_id":a["damage_code_id"],
        "semantic_damage_model_version":"model v1.0","documentation_revision":"docs r1",
        "consumer_pin":"wildfire_bess@model_v1_0__docs_r1",
        "artifact_schema_version":"damage_curve_record_bundle.v3","capability_schema_version":"capability_declaration.v3",
        "publication_status":"repository_canonical_not_in_portable_package",
        "path":str((CURRENT/"curve_artifact.json").relative_to(ROOT)),"sha256":sha(CURRENT/"curve_artifact.json"),
        "changelog_path":str((CELL/"CHANGELOG.json").relative_to(ROOT)),
        "known_answer_tests_path":str((CURRENT/"known_answers.json").relative_to(ROOT))})
    write(ROOT/"docs/contracts/machine_readable_artifact_index.json", index)
    write(CELL/"CHANGELOG.json", {"cell_id":a["cell_id"],
        "current_pin":"wildfire_bess@model_v1_0__docs_r1","changes":[{"date":"2026-10-19",
        "model":"model v1.0","docs":"docs r1","classification":"NEW_CELL_MODEL_RELEASE",
        "reason":"Independent local annual proof; conditional response and unit values unchanged",
        "schema_change":False,"portable_package_release":"unreleased","other_cells_changed":False}]})


def validate():
    a,c,v,pin=[read(CURRENT/n) for n in ("curve_artifact.json","capability.json","value_binding.json","consumption_pin.json")]
    old,ov=read(OLD/"curve_artifact.json"),read(OLD/"value_binding.json")
    schemas=ROOT/"docs/contracts/schemas"
    cs=read(schemas/"capability_declaration.v3.schema.json")
    registry=Registry().with_resource(cs["$id"],Resource.from_contents(cs))
    Draft202012Validator(read(schemas/"curve_artifact_bundle.v3.schema.json"),registry=registry).validate(a)
    Draft202012Validator(cs).validate(c)
    assert a["pathways"][0]["curve_records"]==old["pathways"][0]["curve_records"]
    assert a["evaluation_contract"]["record_selection"]==old["evaluation_contract"]["record_selection"]
    for key in ov:
        assert v[key]==ov[key],key
    for name,digest in pin["sha256"].items():
        assert sha(CURRENT/name)==digest,name
    assert a["capability_declaration"]==c and a["canonical_runtime_artifact"] is True
    for key in ("source_dossier","source_workbook","known_answer_tests","source_register","claim_parameter_register","value_crosswalk"):
        assert (ROOT/a[key]).is_file(),key
    with (CURRENT/"value_crosswalk.csv").open() as f:
        rows=list(csv.DictReader(f))
    assert sum(float(r["included_usd"]) for r in rows)==109800000
    index=read(ROOT/"docs/contracts/machine_readable_artifact_index.json")
    current=[r for r in index["artifacts"] if r["cell_id"]==a["cell_id"]]
    assert len(current)==1 and current[0]["sha256"]==sha(CURRENT/"curve_artifact.json")
    print("PASS: existing v3 schemas, exact conditional/value parity, pins, provenance, index and conditional capability")


if __name__ == "__main__":
    import sys
    if "--build" in sys.argv:
        build()
    validate()
