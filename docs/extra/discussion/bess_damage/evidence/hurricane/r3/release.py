"""Author and validate the first repository-canonical BESS wind screening cell.

No Hazard production consumer imports this authoring/evidence script.
"""
from copy import deepcopy
import csv, hashlib, json
from pathlib import Path
import shutil
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT=Path(__file__).resolve().parents[7]
HERE=Path(__file__).resolve().parent
CELL=ROOT/'docs/cells/tropical_cyclone_wind_bess'
OLD=CELL/'proposed/local_candidate_v0_1'
CURRENT=CELL/'current'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())

def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')

def build():
    if CURRENT.exists():raise FileExistsError(CURRENT)
    proof=load(HERE/'annual_qualification.json')
    assert proof['status']=='passed' and proof['physical_cap_all_passed']
    assert proof['max_rate_band_refinement_pgf_eal_relative']<proof['rate_band_mean_relative_gate']
    CURRENT.mkdir()
    for name in ['value_crosswalk.csv','source_register.csv','claim_parameter_register.csv','parameter_register.csv','known_answers.json']:
        shutil.copyfile(OLD/name,CURRENT/name)
    art=deepcopy(load(OLD/'curve_artifact.json'));cap=deepcopy(load(OLD/'capability.json'));value=deepcopy(load(OLD/'value_binding.json'))
    flags=[f for f in cap['consumer_annual_metrics']['limitation_flags'] if f not in ['LOCAL_TEST_ONLY_NOT_CANONICAL','BESS_WIND_REFERENCE_NOT_YET_QUALIFIED']]
    flags+=['COMMON_RATE_RANK_SCREENING_DEPENDENCE','SOURCE_UNKNOWN_MASS_RETAINED','NO_INTRINSIC_DAMAGE_SPREAD','PER_PHYSICAL_UNIT_ANNUAL_CAP_NO_RESTORATION','LOCAL_PROOF_NOT_NATIONAL_ADMISSION']
    cap['canonical_runtime_artifact']=True
    for pathway in cap['pathway_capabilities']:
        pathway['conditions']=[x for x in pathway['conditions'] if x!='Explicit local-test opt-in']
        pathway['conditions'].append('Qualified reference/coupling and annual-cap prerequisites when used downstream')
        pathway['limitation_flags']=flags
    cap['consumer_annual_metrics']['status_after_promotion']='consumer_computable_from_validated_frequency_intensity_coupling_value_and_cap_model'
    cap['consumer_annual_metrics']['prerequisites']=[
        'Exact model v1.0/docs r1 artifact/value/capability and profile pins',
        'Explicit replacement or repair hypothesis and unweighted resistance scenario',
        'Comparable pressure demand/reference and valid 0-to-2 response domain',
        'Declared frequency and common-event spatial coupling; marginal rates are not joint events',
        'Unique physical units; cap cumulative annual cost separately at each unit value; no within-year restoration',
        'Retain original source/rank weights and unknown intervals, clocks, source floor and unbound property',
        'Validated annual AEP/OEP distribution and independent fixed-mass tail/mean checks',
        'Annual projection uses conditional mean severity; no intrinsic Damage uncertainty inferred',
        'Local qualification is not national support, publication, complete property or recipient admission']
    cap['consumer_annual_metrics']['limitation_flags']=flags
    cap['cap_binding']['checks_required']+=['Per-physical-unit annual cap before plant sum','AEP/OEP from same storms and fixed plant; no assembly cap borrowing undamaged stock']
    cap['promotion_gate']={'status':'passed','required_before_canonical_use':['Consumer must satisfy all conditional-use prerequisites for its exact run; no automatic national/recipient admission']}
    value.update(annual_cap_policy='per_physical_unit_no_within_year_restoration',use='partial_scope_annual_screening',intrinsic_damage_spread='not_carried')
    write(CURRENT/'value_binding.json',value);write(CURRENT/'capability.json',cap)
    art.update(schema_status='released',damage_code_id='BESS_TC_WIND_SCREENING_V1',semantic_damage_model_version='model v1.0',documentation_revision='docs r1',lifecycle_state='repository_canonical_conditional_screening',promotion_status='conditional_consumer_annual_use_qualified',canonical_runtime_artifact=True,package_inclusion_status='repository_canonical_not_in_portable_package',model_grade='screening_T4_not_calibrated',review_status='same_author_with_independent_numerical_methods')
    for key in ['source_dossier','source_workbook','known_answer_tests','source_register','claim_parameter_register','value_crosswalk']:
        art[key]=str((CURRENT/Path(art[key]).name).relative_to(ROOT))
    art['source_dossier']=str((CURRENT/'derivation.md').relative_to(ROOT))
    art['value_linkage']['value_binding_path']=str((CURRENT/'value_binding.json').relative_to(ROOT))
    art['value_linkage']['value_binding_sha256']=sha(CURRENT/'value_binding.json')
    art['evaluation_contract'].update(production_runtime_authorized=True,explicit_local_test_opt_in_required=False,annual_qualification_evidence=str((HERE/'annual_qualification.json').relative_to(ROOT)),limitation_flags=flags)
    art['evaluation_contract']['required_local_demand_basis_id']='qualified_comparable_pressure_reference_declared_by_consumer'
    art['capability_declaration']=cap
    art['derivation_rationale']['consumer_boundary']='Conditional partial-scope annual metrics only after frequency/coupling/value/cap/distribution prerequisites; complete-plant metrics withheld'
    art['derivation_rationale']['predecessor_candidate_sha256']=sha(OLD/'curve_artifact.json')
    for unit in art['pathways'][0]['failure_unit_coverage']:
        if unit['status']=='conditional_local_test':unit['status']='conditional_screening'
    # Parameter values and tier are frozen; source rows retain research provenance.
    write(CURRENT/'curve_artifact.json',art)
    write(CURRENT/'validation.json',{'status':'passed_conditional_annual_screening','classification':'NEW_CELL_MODEL_RELEASE','response_and_unit_values_vs_v0_1':'exactly_unchanged','qualification':proof,'portable_package_issued':False,'national_spatial_qualification':False})
    names=['curve_artifact.json','capability.json','value_binding.json','value_crosswalk.csv','source_register.csv','claim_parameter_register.csv','parameter_register.csv','known_answers.json','validation.json']
    write(CURRENT/'consumption_pin.json',{'cell_id':art['cell_id'],'semantic_damage_model_version':'model v1.0','documentation_revision':'docs r1','canonical_runtime_artifact':True,'sha256':{n:sha(CURRENT/n) for n in names}})
    index=load(ROOT/'docs/contracts/machine_readable_artifact_index.json')
    assert not any(x['cell_id']==art['cell_id'] for x in index['artifacts'])
    index['artifacts'].append({'cell_id':art['cell_id'],'damage_code_id':art['damage_code_id'],'semantic_damage_model_version':'model v1.0','documentation_revision':'docs r1','consumer_pin':'tropical_cyclone_wind_bess@model_v1_0__docs_r1','artifact_schema_version':'damage_curve_record_bundle.v3','capability_schema_version':'capability_declaration.v3','publication_status':'repository_canonical_not_in_portable_package','path':str((CURRENT/'curve_artifact.json').relative_to(ROOT)),'sha256':sha(CURRENT/'curve_artifact.json'),'changelog_path':str((CELL/'CHANGELOG.json').relative_to(ROOT)),'known_answer_tests_path':str((CURRENT/'known_answers.json').relative_to(ROOT))})
    write(ROOT/'docs/contracts/machine_readable_artifact_index.json',index)
    write(CELL/'CHANGELOG.json',{'cell_id':art['cell_id'],'changes':[{'date':'2026-10-19','model':'model v1.0','docs':'docs r1','classification':'NEW_CELL_MODEL_RELEASE','reason':'Owner-directed local annual proof passes; same conditional response and value, conditional consumer admission','schema_change':False,'other_cells_changed':False,'portable_package_release':'unreleased'}]})

def validate():
    art,cap,value,pin=[load(CURRENT/n) for n in ['curve_artifact.json','capability.json','value_binding.json','consumption_pin.json']]
    old=load(OLD/'curve_artifact.json');oldvalue=load(OLD/'value_binding.json')
    schemas=ROOT/'docs/contracts/schemas';cs=load(schemas/'capability_declaration.v3.schema.json')
    registry=Registry().with_resource(cs['$id'],Resource.from_contents(cs))
    Draft202012Validator(load(schemas/'curve_artifact_bundle.v3.schema.json'),registry=registry).validate(art)
    Draft202012Validator(cs).validate(cap)
    assert art['pathways'][0]['curve_records']==old['pathways'][0]['curve_records']
    assert art['evaluation_contract']['curve_selection_by_response_hypothesis']==old['evaluation_contract']['curve_selection_by_response_hypothesis']
    for key in oldvalue:assert value[key]==oldvalue[key],key
    assert art['capability_declaration']==cap and art['canonical_runtime_artifact'] is True
    for name,digest in pin['sha256'].items():assert sha(CURRENT/name)==digest,name
    for key in ['source_dossier','source_workbook','known_answer_tests','source_register','claim_parameter_register','value_crosswalk']:
        assert (ROOT/art[key]).is_file(),key
    with (CURRENT/'value_crosswalk.csv').open() as f:rows=list(csv.DictReader(f))
    assert sum(float(r['included_usd']) for r in rows)==109800000
    index=load(ROOT/'docs/contracts/machine_readable_artifact_index.json')
    entries=[x for x in index['artifacts'] if x['cell_id']==art['cell_id']]
    assert len(entries)==1 and entries[0]['sha256']==sha(CURRENT/'curve_artifact.json')
    print('PASS: existing v3 schemas, exact response/unit-value parity, pins, provenance, index and conditional annual capability')

if __name__=='__main__':
    import sys
    if '--build' in sys.argv:build()
    validate()
