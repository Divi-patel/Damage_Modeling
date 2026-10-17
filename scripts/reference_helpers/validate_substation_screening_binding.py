#!/usr/bin/env python3
"""Validate a consumer binding without changing or promoting a Damage cell."""
import csv
from decimal import Decimal
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def validate():
    hazard = ROOT.parent/'Hazard_modeling'
    folder = ROOT/'docs/contracts/hazard_handoff/substation_flood_screening_v1'
    raw = (folder/'binding.json').read_bytes(); binding = json.loads(raw)
    source = binding['source_inputs']
    for pin in source.values():
        repo = ROOT if pin['repository'] == 'damage_modeling' else hazard
        assert hashlib.sha256((repo/pin['path']).read_bytes()).hexdigest() == pin['sha256'], pin['path']
    artifact = json.loads((ROOT/source['damage_artifact']['path']).read_text())
    capability = json.loads((ROOT/source['damage_capability']['path']).read_text())
    assert artifact['capability_declaration'] == capability
    assert capability['consumer_annual_metrics']['status_after_promotion'] == 'withheld'
    assert artifact['canonical_runtime_artifact'] is True
    assert binding['annual_metrics'] == 'withheld_by_source_capability'
    budget = list(csv.DictReader((hazard/source['hazard_budget']['path']).open()))
    summary = json.loads((hazard/source['hazard_budget_summary']['path']).read_text())
    ledger = binding['value']['ledger']; assert len(ledger) == 31
    by_id = {row['row_id']:row for row in ledger}; assert len(by_id) == 31
    for row in budget:
        selected = by_id.pop(row['row_id'])
        assert Decimal(selected['amount_usd']) == Decimal(row['amount_usd'])
        expected = 'outside_response_boundary' if row['row_id'] == 'road' else 'assembly_denominator'
        assert selected['role'] == expected and selected['component_dr_assigned'] is False
    assert set(by_id) == set(summary['separate_support_allowances_usd'])
    for row_id, row in by_id.items():
        assert Decimal(row['amount_usd']) == Decimal(str(summary['separate_support_allowances_usd'][row_id]))
        assert row['role'] == 'repair_support_not_modeled' and row['component_dr_assigned'] is False
    crosswalk = list(csv.DictReader((folder/'value_crosswalk.csv').open()))
    assert len(crosswalk) == len(ledger)
    for a, b in zip(crosswalk,ledger):
        assert a == {key:str(value) for key,value in b.items()}
    installed = hazard/'perils/flood/src/flood/resources/damage/substation_screening'
    assert raw == (installed/'binding.json').read_bytes()
    assert (installed/'curve_artifact.json').read_bytes() == (ROOT/source['damage_artifact']['path']).read_bytes()
    pin = json.loads((installed/'consumption_pin.json').read_text())
    assert pin['binding_sha256'] == hashlib.sha256(raw).hexdigest()
    return {'status':'pass','date':'2026-10-16','binding_sha256':pin['binding_sha256'],
            'source_artifact_sha256':pin['artifact_sha256'],'value_rows':len(ledger),
            'exact_hazard_resource_copies':True,'existing_source_pins_unchanged':True,
            'damage_cell_model_or_capability_changed':False,'annual_metrics':'withheld'}


if __name__ == '__main__':
    receipt = validate()
    path = ROOT/'docs/contracts/hazard_handoff/substation_flood_screening_v1/validation.json'
    path.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
