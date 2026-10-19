"""Validate the proposed BESS cell without admitting it to runtime."""
from pathlib import Path
import csv
import hashlib
import json

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[2]
FOLDER = ROOT / "docs/cells/flood_bess/proposed/local_candidate_v0_1"


def main():
    artifact = json.loads((FOLDER / "curve_artifact.json").read_text())
    capability = json.loads((FOLDER / "capability.json").read_text())
    schema_dir = ROOT / "docs/contracts/schemas"
    schema = json.loads((schema_dir / "curve_artifact_bundle.v2.schema.json").read_text())
    cap_schema = json.loads((schema_dir / "capability_declaration.v2.schema.json").read_text())
    registry = Registry().with_resource(cap_schema["$id"], Resource.from_contents(cap_schema))
    Draft202012Validator(schema, registry=registry).validate(artifact)
    Draft202012Validator(cap_schema).validate(capability)
    assert capability == artifact["capability_declaration"]
    assert artifact["canonical_runtime_artifact"] is False
    assert artifact["evaluation_contract"]["production_runtime_authorized"] is False
    assert all(capability["consumer_annual_metrics"][k] == "withheld" for k in ["eal", "pml", "var", "tvar"])
    pin = json.loads((FOLDER / "consumption_pin.json").read_text())
    for name, digest in pin["sha256"].items():
        assert hashlib.sha256((FOLDER / name).read_bytes()).hexdigest() == digest, name
    assert hashlib.sha256((FOLDER / "value_binding.json").read_bytes()).hexdigest() == artifact["value_linkage"]["value_binding_sha256"]
    source = ROOT / artifact["derivation_rationale"]["source_artifact_path"]
    assert hashlib.sha256(source.read_bytes()).hexdigest() == artifact["derivation_rationale"]["source_artifact_sha256"]
    source_pcs = next(r for r in json.loads(source.read_text())["curve_records"] if r["curve_id"] == "FS_INV")
    assert artifact["curve_records"][1]["parameters"] == source_pcs["parameters"]
    assert artifact["curve_records"][0]["parameters"]["points"] == [[0, 0], [1, 1]]
    assert "only binary" in artifact["evaluation_contract"]["battery_state"]
    for name in ["source_dossier", "known_answer_tests"]:
        assert (ROOT / artifact[name]).is_file()
    rows = list(csv.DictReader((FOLDER / "value_crosswalk.csv").open()))
    assert abs(sum(float(r["value_usd"]) for r in rows) - 109800000) < 1e-6
    print("PASS: schemas, exact pins, unchanged PCS source, binary-state contract, evidence paths, value reconciliation and non-admission")


if __name__ == "__main__":
    main()
