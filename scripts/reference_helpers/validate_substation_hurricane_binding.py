"""Read-only exact source, installed resource and station-accounting validation."""

from decimal import Decimal
import hashlib
import json
from pathlib import Path


def validate():
    root = Path(__file__).resolve().parents[2]
    folder = root / "docs/contracts/hazard_handoff/substation_hurricane_screening_v1"
    binding_path = folder / "binding.json"
    binding = json.loads(binding_path.read_bytes())
    source = root / "docs/cells/tropical_cyclone_wind_solar/current/tropical_cyclone_wind_solar__model_v2_1__docs_r2__curve_artifact.json"
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    assert sha(source) == binding["source_pin"]["artifact_sha256"]
    artifact = json.loads(source.read_bytes())
    assert artifact["canonical_runtime_artifact"]
    assert artifact["capability_declaration"]["consumer_annual_metrics"]["status_after_promotion"] == binding["annual_metrics"]
    value = binding["value"]
    ledger = value["ledger"]
    assert len(ledger) == len({r["row_id"] for r in ledger}) == 31
    selected = [r for r in ledger if r["role"] == "assembly_denominator"]
    assert len(selected) == 27
    total = sum(Decimal(r["amount_usd"]) for r in ledger)
    modeled = sum(Decimal(r["amount_usd"]) for r in selected)
    assert modeled == Decimal(value["assembly_usd"]) == Decimal(binding["annual_aggregate_cap_usd"])
    assert total == Decimal(value["full_reference_budget_usd"])
    assert total-modeled == Decimal(value["unmodeled_budget_usd"])
    hazard = root.parent / "Hazard_modeling"
    assert sha(hazard / binding["physical_profile"]["path"]) == binding["physical_profile"]["sha256"]
    resource = hazard / "perils/hurricane/src/hurricane/resources/substation_screening"
    assert (resource / "curve_artifact.json").read_bytes() == source.read_bytes()
    assert (resource / "binding.json").read_bytes() == binding_path.read_bytes()
    expected = {"binding_sha256":sha(binding_path), "artifact_sha256":sha(source)}
    assert json.loads((resource / "consumption_pin.json").read_bytes()) == expected
    return {"status":"passed", **expected, "value_rows":31, "assembly_rows":27,
            "assembly_usd":str(modeled), "unmodeled_usd":str(total-modeled),
            "canonical_curve_changed":False, "new_cell_created":False,
            "hazard_resource_bytes_identical":True,
            "scope":"source/accounting/packaging; Hazard owns numerical and annual proof"}


if __name__ == "__main__":
    print(json.dumps(validate(), indent=2, sort_keys=True))
