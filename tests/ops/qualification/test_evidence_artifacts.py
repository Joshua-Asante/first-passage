"""Role/content consistency only; no capture or authentication authority."""
import hashlib
import json
import pytest

from c1_rail.qualification.contract import canonical_json_bytes
from semantic_fixture import stage_case


def build(stage='N1', passing=True):
    from c1_rail.qualification.evidence import build_stage_artifact
    c, p, raw, inventory = stage_case(stage, passing=passing)
    predecessors = {'N1': (), 'N2': ('N1',), 'PART_B': ('N1','N2'), 'PART_A': ('N1','N2','PART_B')}[stage]
    prior = {name: stage_case(name)[2] for name in predecessors}
    return build_stage_artifact(contract=c, policy=p, stage=stage, input_plan_sha256='e'*64,
        outcome_bytes=raw, path_inventory_bytes=inventory, prior_stage_outcomes=prior)


@pytest.mark.parametrize('stage,passing,decision,counts', [
    ('N1', True, 'PASS', {'FULL':10,'H1':10,'H2':10}),
    ('N1', False, 'FAIL', {'FULL':10,'H1':10,'H2':10}),
    ('N2', True, 'PASS', {'FULL':100}), ('N2', False, 'FAIL', {'FULL':100}),
    ('PART_B', True, 'PASS', {'H1':100,'H2':100}), ('PART_B', False, 'FAIL', {'H1':100,'H2':100}),
    ('PART_A', True, 'PASS', {'REGIME':2}), ('PART_A', False, 'FAIL', {'REGIME':2}),
])
def test_artifact_decision_and_counts_derive_from_observations(stage, passing, decision, counts):
    artifact = json.loads(build(stage, passing))
    assert artifact['schema'] == 'qualification_stage_result/v1'
    assert artifact['decision'] == decision
    assert artifact['population_counts'] == counts
    assert artifact['outcome_array_sha256'] == hashlib.sha256(stage_case(stage, passing=passing)[2]).hexdigest()


@pytest.mark.parametrize('change', ['population_order','outcome','path_order','seed','stage','missing','extra','bool_index'])
def test_changed_evidence_relationship_rejected(change):
    from c1_rail.qualification.evidence import build_stage_artifact
    c,p,raw,inventory = stage_case()
    outcomes = json.loads(raw)
    paths = json.loads(inventory)
    if change == 'population_order': outcomes.reverse()
    elif change == 'outcome': outcomes[0]['outcomes'][0]['diagnostics'] = []
    elif change == 'path_order': paths['records'].reverse()
    elif change == 'seed': paths['records'][0]['seed_input_sha256'] = 'f'*64
    elif change == 'stage': paths['records'][0]['stage'] = 'N2'
    elif change == 'missing': paths['records'].pop()
    elif change == 'extra': paths['records'].append(paths['records'][0])
    elif change == 'bool_index': paths['records'][0]['path_index'] = False
    with pytest.raises(ValueError):
        build_stage_artifact(contract=c, policy=p, stage='N1', input_plan_sha256='e'*64,
            outcome_bytes=canonical_json_bytes(outcomes), path_inventory_bytes=canonical_json_bytes(paths), prior_stage_outcomes={})


def test_later_stage_requires_actual_passing_prerequisite():
    from c1_rail.qualification.evidence import build_stage_artifact
    c,p,raw,inventory = stage_case('N2')
    for prior in ({}, {'N1':stage_case(passing=False)[2]}):
        with pytest.raises(ValueError):
            build_stage_artifact(contract=c, policy=p, stage='N2', input_plan_sha256='e'*64,
                outcome_bytes=raw,path_inventory_bytes=inventory,prior_stage_outcomes=prior)


@pytest.mark.parametrize('role', ['attempt_journal','legality_result','n1_result','path_inventory','runtime_load_trace'])
def test_every_n1_role_is_mandatory(role):
    from c1_rail.qualification.evidence import validate_output_roles
    _,p,_,_ = stage_case()
    roles = ['attempt_journal','legality_result','n1_result','path_inventory','runtime_load_trace']
    roles.remove(role)
    with pytest.raises(ValueError, match='OUTPUT_ROLE_MISMATCH'):
        validate_output_roles(p, roles, stages=('LEGALITY','N1'), completion='COMPLETE', verdict='FAIL')


@pytest.mark.parametrize('role', ['n2_result','part_b_result','part_a_result','private-result','n1_result'])
def test_surplus_or_duplicate_n1_role_rejected(role):
    from c1_rail.qualification.evidence import validate_output_roles
    _,p,_,_ = stage_case()
    roles = ['attempt_journal','legality_result','n1_result','path_inventory','runtime_load_trace',role]
    with pytest.raises(ValueError, match='OUTPUT_ROLE_MISMATCH'):
        validate_output_roles(p, roles, stages=('LEGALITY','N1'),completion='PARTIAL',verdict='NONE')


@pytest.mark.parametrize('stage,predecessors', [('N2',('N1',)),('PART_B',('N1','N2')),('PART_A',('N1','N2','PART_B'))])
def test_later_stage_adapter_requires_each_predecessor(stage,predecessors):
    from c1_rail.qualification.evidence import build_stage_artifact
    c,p,raw,inventory=stage_case(stage)
    for missing in predecessors:
        prior={name:stage_case(name)[2] for name in predecessors if name!=missing}
        with pytest.raises(ValueError,match='STAGE_PREREQUISITE_MISMATCH'):
            build_stage_artifact(contract=c,policy=p,stage=stage,input_plan_sha256='e'*64,
                outcome_bytes=raw,path_inventory_bytes=inventory,prior_stage_outcomes=prior)


@pytest.mark.parametrize('stage,failed', [('PART_B','N1'),('PART_A','N1'),('PART_A','N2'),('PART_A','PART_B')])
def test_later_stage_adapter_rejects_failed_prerequisite(stage,failed):
    from c1_rail.qualification.evidence import build_stage_artifact
    c,p,raw,inventory=stage_case(stage)
    names=('N1','N2') if stage=='PART_B' else ('N1','N2','PART_B')
    prior={name:stage_case(name,passing=name!=failed)[2] for name in names}
    with pytest.raises(ValueError,match='failed'):
        build_stage_artifact(contract=c,policy=p,stage=stage,input_plan_sha256='e'*64,
            outcome_bytes=raw,path_inventory_bytes=inventory,prior_stage_outcomes=prior)


@pytest.mark.parametrize('role', ['attempt_journal','legality_result','n1_result','n2_result','part_b_result',
    'part_a_result','path_inventory','runtime_load_trace'])
def test_each_complete_prefix_role_is_mandatory(role):
    from c1_rail.qualification.evidence import validate_output_roles
    _,p,_,_=stage_case()
    roles=['attempt_journal','legality_result','n1_result','n2_result','part_b_result','part_a_result','path_inventory','runtime_load_trace']
    roles.remove(role)
    with pytest.raises(ValueError,match='OUTPUT_ROLE_MISMATCH'):
        validate_output_roles(p,roles,stages=('LEGALITY','N1','N2','PART_B','PART_A'),completion='COMPLETE',verdict='PASS')


def _panel_adapter_case(passes):
    from c1_rail.qualification.seed_identity import seed_input
    c,p,_,_=stage_case('PART_A')
    c.stage_specs['PART_A'].exact_depth=20
    c.replay.part_a.paths_per_population_per_panel=20
    rows,records=[],[]
    for panel,count in enumerate(passes):
        for index in range(20):
            row=dict(status='PASS' if index<count else 'UNRESOLVED',sessions_to_pass=1 if index<count else None,
                     failure_reason=None if index<count else 'horizon_cap',diagnostics=[])
            rows.append(row)
            seed=seed_input(c,stage='n2',population='FULL',panel_index=panel,path_index=index,synthetic=True)
            records.append(dict(stage='PART_A',population='REGIME',panel_id=hashlib.sha256(str(panel).encode()).hexdigest(),
                path_index=index,seed_input_sha256=seed.sha256,outcome_sha256=hashlib.sha256(canonical_json_bytes(row)).hexdigest()))
    return c,p,canonical_json_bytes([dict(population='REGIME',outcomes=rows)]),dict(
        schema='qualification_path_inventory/v1',trust_domain_sha256=c.trust_domain_sha256,records=records)


@pytest.mark.parametrize('passes,expected', [([19,20],None),([19,20,19,20],'PASS'),([20,20],'PASS'),([20,20,20,20],None)])
def test_part_a_adapter_enforces_original_prefix_expansion(passes,expected):
    from c1_rail.qualification.evidence import build_stage_artifact
    c,p,raw,inventory=_panel_adapter_case(passes)
    def run():
        return build_stage_artifact(contract=c,policy=p,stage='PART_A',input_plan_sha256='e'*64,
            outcome_bytes=raw,path_inventory_bytes=canonical_json_bytes(inventory),
            prior_stage_outcomes={name:stage_case(name)[2] for name in ('N1','N2','PART_B')})
    if expected is None:
        with pytest.raises(ValueError,match='expansion'): run()
    else: assert json.loads(run())['decision']==expected


def test_part_a_adapter_rejects_reordered_panels():
    from c1_rail.qualification.evidence import build_stage_artifact
    c,p,raw,inventory=_panel_adapter_case([19,20,19,20])
    inventory['records']=inventory['records'][20:40]+inventory['records'][:20]+inventory['records'][40:]
    with pytest.raises(ValueError,match='PATH_'):
        build_stage_artifact(contract=c,policy=p,stage='PART_A',input_plan_sha256='e'*64,outcome_bytes=raw,
            path_inventory_bytes=canonical_json_bytes(inventory),
            prior_stage_outcomes={name:stage_case(name)[2] for name in ('N1','N2','PART_B')})
