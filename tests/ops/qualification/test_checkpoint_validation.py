"""Coherent substitutions must fail even after all dependent hashes change."""
import json
from types import SimpleNamespace
import pytest
from test_orchestration import contract
from c1_rail.qualification.orchestration import _stage_seeds, _part_a_seeds, canonical_bytes
from c1_rail.qualification.seal import _validate_checkpoint_plan_inputs, ResultValidationError
import hashlib

def case(checkpoint):
    c=contract()
    seeds=(_part_a_seeds(c,True) if checkpoint=='PART_A' else
           _stage_seeds(c,'n1' if checkpoint=='N1' else 'n2',True))
    plan=dict(schema='e1_checkpoint_plan/v1',checkpoint=checkpoint,
        contract_sha256=c.contract_sha256,trust_domain_sha256=c.trust_domain_sha256,
        synthetic=True,exact_depth_approval_sha256='c'*64,horizon_sessions=500,
        seed_inputs=[json.loads(s.canonical_bytes) for s in seeds],
        extra={'initial_panels':2,'expanded_panels':4} if checkpoint=='PART_A' else None)
    return c,plan

def validate(c,plan):
    # Rehash every path after mutation, reproducing coherent caller evidence.
    records=[]
    for row in plan['seed_inputs']:
        if row['purpose']!='path': continue
        stage=('PART_A' if plan['checkpoint']=='PART_A' else 'N1' if plan['checkpoint']=='N1'
               else 'N2' if row['population']=='FULL' else 'PART_B')
        records.append(dict(stage=stage,seed_input_sha256=hashlib.sha256(canonical_bytes(row)).hexdigest()))
    _validate_checkpoint_plan_inputs(canonical_bytes(plan),checkpoint=plan['checkpoint'],contract=c,
        exact_depth_approval_sha256='c'*64,synthetic=True,inventory_records=records)

@pytest.mark.parametrize('checkpoint',['N1','N2','PART_A'])
@pytest.mark.parametrize('field,value',[
    ('root_rng_namespace','foreign'),('stage','n3'),('population','H2'),
    ('panel_index',13),('path_index',101),('seed',0),
    ('source_session_ids_sha256','0'*64),
])
def test_consistently_substituted_seed_is_rejected(checkpoint,field,value):
    c,p=case(checkpoint);p['seed_inputs'][0][field]=value
    with pytest.raises(ResultValidationError): validate(c,p)

@pytest.mark.parametrize('mutation',['reverse','missing','duplicate','outer_missing'])
def test_ordered_complete_plan_required(mutation):
    c,p=case('PART_A')
    if mutation=='reverse':p['seed_inputs'].reverse()
    elif mutation=='missing':p['seed_inputs'].pop()
    elif mutation=='duplicate':p['seed_inputs'].append(p['seed_inputs'][-1])
    else:p['seed_inputs']=[r for r in p['seed_inputs'] if r['purpose']!='outer']
    with pytest.raises(ResultValidationError):validate(c,p)

@pytest.mark.parametrize('checkpoint',['N1','N2','PART_A'])
def test_canonical_frozen_plan_accepts(checkpoint):
    validate(*case(checkpoint))

@pytest.mark.parametrize('mutation',['source','identity','index','missing','order'])
def test_part_a_panel_source_binding_required(mutation):
    from c1_rail.qualification.seal import _validate_part_a_panels
    from c1_rail.qualification.orchestration import panel_identity
    c=contract();panels=[];records=[]
    for i in range(2):
        ids=list(c.populations['FULL'])
        if mutation=='source' and i==0:ids[0]='foreign-session'
        identity=panel_identity(c,SimpleNamespace(index=i,source_session_ids=tuple(ids)))
        panels.append(dict(panel_index=i,panel_id=identity,source_session_ids=ids))
        records.extend(dict(stage='PART_A',population='REGIME',panel_id=identity,path_index=j)
                       for j in range(2))
    if mutation=='identity':panels[0]['panel_id']='f'*64
    elif mutation=='index':panels[0]['panel_index']=3
    elif mutation=='missing':panels.pop()
    elif mutation=='order':panels.reverse()
    with pytest.raises(ResultValidationError):_validate_part_a_panels(c,{'panels':panels},records)

def test_canonical_seed_vector_preserves_existing_stream():
    c,p=case('N1')
    first=p['seed_inputs'][0]
    assert first['seed']==10869960941191221317
    assert first['source_session_ids_sha256']=='0473ef2dc0d324ab659d3580c1134e9d812035905c4781fdd6d529b0c6860e13'

@pytest.mark.parametrize('count',[2,4])
def test_panel_binding_allows_bootstrap_repetitions_and_expansion(count):
    from c1_rail.qualification.seal import _validate_part_a_panels
    from c1_rail.qualification.orchestration import panel_identity
    c=contract();panels=[];records=[]
    for i in range(count):
        ids=['a','a']
        identity=panel_identity(c,SimpleNamespace(index=i,source_session_ids=tuple(ids)))
        panels.append(dict(panel_index=i,panel_id=identity,source_session_ids=ids))
        records.extend(dict(stage='PART_A',population='REGIME',panel_id=identity,path_index=j) for j in range(2))
    _validate_part_a_panels(c,{'panels':panels},records)
