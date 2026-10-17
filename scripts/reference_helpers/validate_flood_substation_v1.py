"""Read-only standalone Substation Flood release validation."""
from pathlib import Path
import hashlib,json,csv
from decimal import Decimal
from jsonschema import Draft202012Validator
from referencing import Registry,Resource
D=Path(__file__).resolve().parents[2];o=D/'docs/cells/flood_substation/current'
p=o/'flood_substation__model_v1_0__docs_r1__curve_artifact.json';c=o/'flood_substation__model_v1_0__docs_r1__capability.json';a=json.loads(p.read_text());cap=json.loads(c.read_text())
schemas=D/'docs/contracts/schemas';bs=json.loads((schemas/'curve_artifact_bundle.v3.schema.json').read_text());cs=json.loads((schemas/'capability_declaration.v3.schema.json').read_text());reg=Registry().with_resource(cs['$id'],Resource.from_contents(cs))
Draft202012Validator(bs,registry=reg).validate(a);Draft202012Validator(cs).validate(cap)
source=D/a['derivation_rationale']['source_artifact_path'];assert hashlib.sha256(source.read_bytes()).hexdigest()==a['derivation_rationale']['source_artifact_sha256']
assert a['pathways'][0]['curve_records'][0]['parameters']['points']==json.loads(source.read_text())['pathways'][0]['curve_records'][0]['parameters']['points']
bp=D/a['value_linkage']['value_binding_path'];assert hashlib.sha256(bp.read_bytes()).hexdigest()==a['value_linkage']['value_binding_sha256'];b=json.loads(bp.read_text());roles={}
for r in b['value']['ledger']:roles[r['role']]=roles.get(r['role'],Decimal(0))+Decimal(r['amount_usd'])
assert roles['assembly_denominator']==Decimal('27353236.37')
for key in ['source_dossier','source_workbook','known_answer_tests','source_register','claim_parameter_register','value_crosswalk']:assert (D/a[key]).exists(),key
assert (o/'value_crosswalk.csv').read_bytes()==(bp.parent/'value_crosswalk.csv').read_bytes()

assert len(b["value"]["ledger"]) == 31
print("PASS: bundle/capability schemas, source parity, value partition and evidence paths")
