"""Read-only station Wildfire binding/source/accounting and installed-byte proof."""
from decimal import Decimal
import hashlib
import json
from pathlib import Path


def validate():
    root = Path(__file__).resolve().parents[2]
    folder = root / "docs/contracts/hazard_handoff/substation_wildfire_screening_v1"
    bpath = folder / "binding.json"
    binding = json.loads(bpath.read_bytes())
    source = root / "docs/cells/wildfire_solar/current/wildfire_solar__model_v1_0__docs_r3__curve_artifact.json"
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    artifact = json.loads(source.read_bytes())
    assert sha(source) == binding["source_pin"]["artifact_sha256"]
    assert artifact["canonical_runtime_artifact"]
    rows = binding["value"]["ledger"]
    assert len(rows) == len({r["row_id"] for r in rows}) == 31
    selected = [r for r in rows if r["role"] == "modeled_electrical_assembly"]
    modeled = sum(Decimal(r["amount_usd"]) for r in selected)
    withheld = sum(Decimal(r["amount_usd"]) for r in rows if r["role"] == "withheld_fenced_value")
    assert len(selected) == 8 and modeled == Decimal("13025357")
    assert modeled + withheld == Decimal("27353236.37")
    assert modeled == Decimal(binding["annual_aggregate_cap_usd"])
    hazard = root.parent / "Hazard_modeling"
    assert sha(hazard / binding["physical_profile"]["path"]) == binding["physical_profile"]["sha256"]
    res = hazard / "perils/wildfire/src/wildfire/resources/substation_screening"
    assert (res / "binding.json").read_bytes() == bpath.read_bytes()
    assert (res / "curve_artifact.json").read_bytes() == source.read_bytes()
    expected = {"binding_sha256": sha(bpath), "artifact_sha256": sha(source)}
    assert json.loads((res / "consumption_pin.json").read_bytes()) == expected
    return {"status": "passed", **expected, "value_rows":31, "modeled_rows":8,
            "modeled_value_usd":str(modeled), "withheld_fenced_value_usd":str(withheld),
            "canonical_curve_changed":False, "new_cell_created":False,
            "hazard_resource_bytes_identical":True,
            "scope":"source/accounting/packaging; Hazard owns numerical and annual proof"}


if __name__ == "__main__":
    print(json.dumps(validate(), indent=2, sort_keys=True))
