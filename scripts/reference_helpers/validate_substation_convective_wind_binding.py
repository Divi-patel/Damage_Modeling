"""Read-only source, accounting and installed-byte proof for the CW station binding."""
from decimal import Decimal
import hashlib
import json
from pathlib import Path


def validate():
    root=Path(__file__).resolve().parents[2]
    folder=root/'docs/contracts/hazard_handoff/substation_convective_wind_screening_v1'
    binding=json.loads((folder/'binding.json').read_bytes())
    source=next((root/'docs/cells/tropical_cyclone_wind_solar/current').glob('*model_v2_1*docs_r2*curve_artifact.json'))
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    artifact=json.loads(source.read_bytes())
    assert sha(source)==binding['source_pin']['artifact_sha256'] and artifact['canonical_runtime_artifact']
    assert binding['qualified_target_pathways']==['strong_wind','tornado_direct_wind_loading']
    record=next(r for p in artifact['pathways'] for r in p['curve_records'] if r.get('failure_unit_id')==binding['failure_unit_id'])
    assert record['curve_id']==binding['curve_id']
    rows=binding['value']['ledger'];assert len(rows)==len({r['row_id'] for r in rows})==31
    selected=sum(Decimal(r['amount_usd']) for r in rows if r['role']=='assembly_denominator')
    assert selected==Decimal('27353236.37')==Decimal(binding['annual_aggregate_cap_usd'])
    assert sum(Decimal(r['amount_usd']) for r in rows)==Decimal('30415059.81')
    hazard=root.parent/'Hazard_modeling'
    assert sha(hazard/binding['physical_profile']['path'])==binding['physical_profile']['sha256']
    resource=hazard/'perils/convective_wind/src/convective_wind/resources/substation_screening'
    assert (resource/'binding.json').read_bytes()==(folder/'binding.json').read_bytes()
    assert (resource/'curve_artifact.json').read_bytes()==source.read_bytes()
    pins=dict(binding_sha256=sha(folder/'binding.json'),artifact_sha256=sha(source))
    assert json.loads((resource/'consumption_pin.json').read_text())==pins
    return dict(status='passed',**pins,value_rows=31,station_value_usd=str(selected),canonical_curve_changed=False,new_cell_created=False,hazard_resource_bytes_identical=True,scope='source/accounting/packaging; Hazard owns applicability, numerical and annual proof')


if __name__=='__main__':print(json.dumps(validate(),indent=2))
