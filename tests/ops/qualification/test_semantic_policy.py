import hashlib
import json
from pathlib import Path

import pytest

from c1_rail.qualification.contract import canonical_json_bytes
from semantic_fixture import semantic_case


def validate(document, policy, workload):
    from c1_rail.qualification.policy import validate_contract_semantics
    validate_contract_semantics(document, policy, workload_policy=workload)


def test_pristine_50k_cannot_describe_fixed_100k_product():
    document, policy, workload = semantic_case()
    for field in ('original_basis', 'current_equity', 'historical_eod_peak'):
        document['initial_state'][field] = '50000'
    with pytest.raises(ValueError, match='PRODUCT_BASIS_MISMATCH'):
        validate(document, policy, workload)


def test_valid_product_and_installed_owner_bytes():
    from c1_rail import book_policy, policy_fingerprint
    import firm_rules
    from c1_rail.qualification.policy_sources import build_qualification_policy, require_installed_policy
    document, policy, workload = semantic_case()
    validate(document, policy, workload)
    require_installed_policy(policy)
    assert build_qualification_policy() == policy.canonical_bytes
    raw = json.loads(policy.canonical_bytes)
    assert raw['product'] == {'tier': book_policy.TIER, 'original_basis': '100000', 'state_class': 'PRISTINE'}
    assert raw['source_owner_sha256'] == {
        name: hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()
        for name, module in [('book_policy', book_policy), ('firm_rules', firm_rules), ('policy_fingerprint', policy_fingerprint)]}


@pytest.mark.parametrize('field,value', [
    ('original_basis', '0'), ('original_basis', '-1'), ('original_basis', True),
    ('original_basis', 'NaN'), ('original_basis', 'Infinity'), ('original_basis', {}),
    ('current_equity', '99999'), ('historical_eod_peak', '100001'),
    ('class', 'USED'), ('prior_trade_days', 1), ('prior_trade_days', False),
    ('prior_max_day_profit', '1'), ('prior_max_day_profit', False)])
def test_invalid_initial_state(field, value):
    document, policy, workload = semantic_case()
    document['initial_state'][field] = value
    with pytest.raises(ValueError):
        validate(document, policy, workload)


@pytest.mark.parametrize('change', ['order', 'remove_part_b', 'population', 'joint_depth', 'n3_seal', 'bool_depth', 'horizon', 'panels'])
def test_stage_and_workload_substitution(change):
    document, policy, workload = semantic_case()
    replay = document['replay']
    stages = replay['stages']
    if change == 'order': stages[2], stages[3] = stages[3], stages[2]
    elif change == 'remove_part_b': stages.pop(3)
    elif change == 'population': stages[1]['population_counts'].pop('H2')
    elif change == 'joint_depth': stages[3]['exact_depth'] += 1
    elif change == 'n3_seal': stages[-1]['included_in_e1_seal'] = True
    elif change == 'bool_depth': stages[1]['population_counts']['FULL'] = [True]
    elif change == 'horizon': replay['horizon_sessions'] += 5
    elif change == 'panels': replay['part_a']['initial_panels'] += 1
    with pytest.raises(ValueError): validate(document, policy, workload)


@pytest.mark.parametrize('change', ['contract_hash', 'plan_hash', 'roles', 'optional', 'unknown'])
def test_policy_and_result_plan_binding(change):
    document, policy, workload = semantic_case()
    if change == 'contract_hash': document['policy_sha256'] = 'a' * 64
    elif change == 'plan_hash': document['result_plan']['policy_sha256'] = 'a' * 64
    else: document['result_plan'][{'roles': 'required_output_roles', 'optional': 'permitted_optional_output_roles', 'unknown': 'unknown'}[change]] = ['placeholder']
    with pytest.raises(ValueError): validate(document, policy, workload)


def test_rehashed_alternate_product_policy_is_not_installed_policy():
    from c1_rail.qualification.policy import parse_policy
    from c1_rail.qualification.policy_sources import require_installed_policy
    _, policy, _ = semantic_case()
    doc = json.loads(policy.canonical_bytes)
    doc['product']['original_basis'] = '50000'
    alternate = parse_policy(canonical_json_bytes(doc))
    with pytest.raises(ValueError, match='INSTALLED_POLICY_MISMATCH'):
        require_installed_policy(alternate)


@pytest.mark.parametrize('field,value', [('stage_order', ['N1']), ('base_artifact_roles', ['placeholder']), ('pre_admission_registry', 'ANY'), ('unknown', None)])
def test_closed_policy_rejects_changed_requirements(field, value):
    from c1_rail.qualification.policy import parse_policy
    _, policy, _ = semantic_case()
    doc = json.loads(policy.canonical_bytes)
    doc[field] = value
    with pytest.raises(ValueError): parse_policy(canonical_json_bytes(doc))


@pytest.mark.parametrize('stages,completion,verdict,roles', [
    (('LEGALITY','N1'), 'COMPLETE','FAIL', ('attempt_journal','legality_result','n1_result','path_inventory','runtime_load_trace')),
    (('LEGALITY','N1'), 'PARTIAL','NONE', ('attempt_journal','legality_result','n1_result','path_inventory','runtime_load_trace')),
    (('LEGALITY','N1','N2','PART_B'), 'COMPLETE','FAIL', ('attempt_journal','legality_result','n1_result','n2_result','part_b_result','path_inventory','runtime_load_trace')),
    (('LEGALITY','N1','N2','PART_B'), 'PARTIAL','NONE', ('attempt_journal','legality_result','n1_result','n2_result','part_b_result','path_inventory','runtime_load_trace')),
    (('LEGALITY','N1','N2','PART_B','PART_A'), 'COMPLETE','PASS', ('attempt_journal','legality_result','n1_result','n2_result','part_a_result','part_b_result','path_inventory','runtime_load_trace')),
    (('LEGALITY','N1','N2','PART_B','PART_A'), 'COMPLETE','FAIL', ('attempt_journal','legality_result','n1_result','n2_result','part_a_result','part_b_result','path_inventory','runtime_load_trace')),
])
def test_exact_prefix_role_vectors(stages, completion, verdict, roles):
    from c1_rail.qualification.policy import required_output_roles
    _, policy, _ = semantic_case()
    assert required_output_roles(policy, stages=stages, completion=completion, verdict=verdict) == roles


@pytest.mark.parametrize('stages,completion,verdict', [
    (('LEGALITY','N1'), 'COMPLETE','PASS'), (('LEGALITY',),'COMPLETE','FAIL'),
    (('LEGALITY','N1','N2'),'COMPLETE','FAIL'),
    (('LEGALITY','N1','N2','PART_B','PART_A'), 'PARTIAL','NONE'),
    (('N1','LEGALITY'),'COMPLETE','FAIL')],
    ids=['n1-pass-incomplete', 'legality-only', 'missing-part-b', 'full-prefix-incomplete', 'reordered'])
def test_unsupported_prefix_decision(stages, completion, verdict):
    from c1_rail.qualification.policy import required_output_roles
    _, policy, _ = semantic_case()
    with pytest.raises(ValueError, match='UNSUPPORTED_STAGE_ASSESSMENT'):
        required_output_roles(policy, stages=stages, completion=completion, verdict=verdict)


def test_joint_continuation_is_the_versioned_policy_identity():
    """S4-D4: the joint PARTIAL/NONE prefix is legal only under the versioned
    FULL_E1 identity (policy_id /v2 with joint_continuation); the pre-S4
    document no longer parses as installed policy at all."""
    import hashlib
    from pathlib import Path
    from c1_rail import book_policy, policy_fingerprint
    import firm_rules
    from c1_rail.qualification.policy import parse_policy
    from c1_rail.qualification.policy_sources import build_qualification_policy

    _, policy, _ = semantic_case()
    document = json.loads(policy.canonical_bytes)
    assert document['policy_id'] == 'tradeify-e1-pristine/v2'
    assert document['joint_continuation'] is True
    legacy = dict(document, policy_id='tradeify-e1-pristine/v1')
    legacy.pop('joint_continuation')
    with pytest.raises(ValueError, match='POLICY_SCHEMA_MISMATCH'):
        parse_policy(json.dumps(legacy, separators=(',', ':')).encode())
    assert build_qualification_policy() == policy.canonical_bytes
