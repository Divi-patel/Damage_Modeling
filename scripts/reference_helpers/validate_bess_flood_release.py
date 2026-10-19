"""Validate BESS canonical response, capability, provenance and predecessor parity."""
from pathlib import Path
import csv
import hashlib
import json

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[2]


def validate():
    folder = ROOT/'docs/cells/flood_bess/current'
    old = ROOT/'docs/cells/flood_bess/proposed/local_candidate_v0_2'
    load = lambda path: json.loads(path.read_text())
    sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    artifact, cap, value, pin = [load(folder/n) for n in ['curve_artifact.json','capability.json','value_binding.json','consumption_pin.json']]
    schemas = ROOT/'docs/contracts/schemas'
    cap_schema = load(schemas/'capability_declaration.v2.schema.json')
    registry = Registry().with_resource(cap_schema['$id'], Resource.from_contents(cap_schema))
    Draft202012Validator(load(schemas/'curve_artifact_bundle.v2.schema.json'), registry=registry).validate(artifact)
    Draft202012Validator(cap_schema).validate(cap)
    assert artifact['capability_declaration'] == cap
    assert artifact['canonical_runtime_artifact'] is True
    assert artifact['semantic_damage_model_version'] == pin['semantic_damage_model_version'] == 'model v1.0'
    assert artifact['evaluation_contract']['required_policy_id'] == value['policy_id'] == 'BESS_FLOOD_SCREENING_V1'
    assert artifact['emit_contract']['populated_emit_modes_for_this_cell'] == cap['vulnerability_emit']['populated_emit_modes']
    for name, digest in pin['sha256'].items(): assert sha(folder/name) == digest, name
    prior, prior_value = load(old/'curve_artifact.json'), load(old/'value_binding.json')
    assert artifact['curve_records'] == prior['curve_records']
    assert artifact['evaluation_contract']['curve_selection_by_water_condition'] == prior['evaluation_contract']['curve_selection_by_water_condition']
    for key in ['units','unmodeled_value_usd','unmodeled_buckets','reference_tiv_usd','reference_sha256']:
        assert value[key] == prior_value[key], key
    assert abs(sum(u['count']*u['same_unit_value_usd'] for u in value['units'].values()) - value['modeled_value_usd']) < 1e-6
    assert abs(value['modeled_value_usd']+value['unmodeled_value_usd']-value['reference_tiv_usd']) < 1e-6
    assert value['annual_cap_policy'] == 'per_physical_unit_no_within_year_restoration'
    for name in ['source_dossier','source_workbook','known_answer_tests']:
        assert (ROOT/artifact[name]).is_file(), name
    assert sha(ROOT/artifact['value_linkage']['value_binding_path']) == artifact['value_linkage']['value_binding_sha256']
    source = artifact['derivation_rationale']
    assert sha(ROOT/source['source_artifact_path']) == source['source_artifact_sha256']
    with (ROOT/source['evidence_sources']).open() as f: sources={r['source_id'] for r in csv.DictReader(f)}
    with (ROOT/source['evidence_claims']).open() as f: claims={r['claim_id'] for r in csv.DictReader(f)}
    for parameter in artifact['parameter_tier_table']:
        assert set(parameter['source_ids']) <= sources
        assert set(parameter['claim_ids']) <= claims
    with (folder/'value_crosswalk.csv').open() as f: rows=list(csv.DictReader(f))
    assert all(None not in row and all(v is not None for v in row.values()) for row in rows)
    assert abs(sum(float(r['value_usd']) for r in rows)-value['reference_tiv_usd']) < 1e-6
    index=load(ROOT/'docs/contracts/machine_readable_artifact_index.json')
    entries=[r for r in index['artifacts'] if r['cell_id']=='flood_bess']
    assert len(entries)==1 and entries[0]['sha256']==sha(folder/'curve_artifact.json')
    print('PASS: v1.0 schemas/pins/index, complete response and value parity to v0.2, source/claim paths, disjoint value and annual capability.')


if __name__=='__main__':
    validate()
