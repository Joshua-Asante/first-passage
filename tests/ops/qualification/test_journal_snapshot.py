import json
import pytest
from c1_rail.qualification.contract import canonical_json_bytes


def snapshot_case():
    return dict(attempt_id='attempt-1', contract_sha256='a'*64, trust_domain_sha256='b'*64,
                policy_sha256='c'*64, validity='VALID', campaign_revision=0, event_head='d'*64, executions=())


def test_fixed_empty_snapshot_vector():
    from c1_rail.qualification.journal_snapshot import encode_assessment_snapshot, parse_assessment_snapshot
    raw = encode_assessment_snapshot(**snapshot_case())
    expected = ('{"attempt_id":"attempt-1","campaign_revision":0,"contract_sha256":"' + 'a'*64 +
                '","event_head":"' + 'd'*64 + '","executions":[],"policy_sha256":"' + 'c'*64 +
                '","schema":"qualification_journal_snapshot/v1","trust_domain_sha256":"' + 'b'*64 +
                '","validity":"VALID"}').encode()
    assert raw == expected
    assert parse_assessment_snapshot(raw)['executions'] == []


def test_void_is_a_snapshot_fact_not_erased_history():
    from c1_rail.qualification.journal_snapshot import encode_assessment_snapshot, parse_assessment_snapshot
    args = snapshot_case()
    args.update(validity='VOID', campaign_revision=3, executions=(dict(checkpoint='N1', execution_id='exec-1',
        execution_revision=2, state='ATTESTED', plan_sha256='e'*64, attestation_sha256='f'*64),))
    doc = parse_assessment_snapshot(encode_assessment_snapshot(**args))
    assert doc['validity'] == 'VOID'
    assert doc['executions'][0]['attestation_sha256'] == 'f'*64


@pytest.mark.parametrize('change', ['duplicate','missing_attestation','premature_attestation','unknown_state','bool_revision','bad_attempt','future_digest'])
def test_invalid_snapshot_relationships(change):
    from c1_rail.qualification.journal_snapshot import encode_assessment_snapshot, parse_assessment_snapshot
    args = snapshot_case()
    row = dict(checkpoint='N1', execution_id='exec-1', execution_revision=2,state='ATTESTED',plan_sha256='e'*64,attestation_sha256='f'*64)
    args['campaign_revision'] = 3
    args['executions'] = (row,)
    if change == 'duplicate': args['executions'] = (row,row)
    elif change == 'missing_attestation': row['attestation_sha256'] = None
    elif change == 'premature_attestation': row['state'] = 'RUNNING'
    elif change == 'unknown_state': row['state'] = 'COMPLETE'
    elif change == 'bool_revision': args['campaign_revision'] = True
    elif change == 'bad_attempt': args['attempt_id'] = ''
    if change == 'future_digest':
        doc = json.loads(encode_assessment_snapshot(**args))
        doc['result_sha256'] = '1'*64
        with pytest.raises(ValueError): parse_assessment_snapshot(canonical_json_bytes(doc))
    else:
        with pytest.raises(ValueError): encode_assessment_snapshot(**args)


@pytest.mark.parametrize('validity', ['VALID', 'VOID'])
def test_fixed_populated_snapshot_vector(validity):
    from c1_rail.qualification.journal_snapshot import encode_assessment_snapshot, parse_assessment_snapshot
    args = snapshot_case()
    args.update(validity=validity, campaign_revision=3, executions=(dict(checkpoint='N1', execution_id='exec-1',
        execution_revision=2, state='ATTESTED', plan_sha256='e'*64, attestation_sha256='f'*64),))
    expected = ('{"attempt_id":"attempt-1","campaign_revision":3,"contract_sha256":"' + 'a'*64 +
        '","event_head":"' + 'd'*64 + '","executions":[{"attestation_sha256":"' + 'f'*64 +
        '","checkpoint":"N1","execution_id":"exec-1","execution_revision":2,"plan_sha256":"' + 'e'*64 +
        '","state":"ATTESTED"}],"policy_sha256":"' + 'c'*64 +
        '","schema":"qualification_journal_snapshot/v1","trust_domain_sha256":"' + 'b'*64 +
        '","validity":"' + validity + '"}').encode()
    assert encode_assessment_snapshot(**args) == expected
    assert parse_assessment_snapshot(expected)['executions'][0]['execution_revision'] == 2


def test_execution_revision_cannot_exceed_campaign_revision():
    from c1_rail.qualification.journal_snapshot import encode_assessment_snapshot
    args = snapshot_case()
    args.update(campaign_revision=3, executions=(dict(checkpoint='N1', execution_id='exec-1',
        execution_revision=4, state='ATTESTED', plan_sha256='e'*64, attestation_sha256='f'*64),))
    with pytest.raises(ValueError, match='SNAPSHOT_REVISION_MISMATCH'):
        encode_assessment_snapshot(**args)


@pytest.mark.parametrize('change', ['reorder', 'duplicate_checkpoint'])
def test_snapshot_checkpoint_order_is_canonical_and_unique(change):
    from c1_rail.qualification.journal_snapshot import encode_assessment_snapshot, parse_assessment_snapshot
    args = snapshot_case()
    rows = tuple(dict(checkpoint=checkpoint, execution_id='exec-'+checkpoint, execution_revision=index+1,
        state='ATTESTED', plan_sha256='e'*64, attestation_sha256='f'*64)
        for index,checkpoint in enumerate(('N1','N2','PART_A')))
    args.update(campaign_revision=3, executions=tuple(reversed(rows)))
    doc = parse_assessment_snapshot(encode_assessment_snapshot(**args))
    assert [row['checkpoint'] for row in doc['executions']] == ['N1','N2','PART_A']
    if change == 'reorder': doc['executions'].reverse()
    else: doc['executions'][1]['checkpoint']='N1'
    with pytest.raises(ValueError, match='SNAPSHOT_CHECKPOINT_ORDER_MISMATCH'):
        parse_assessment_snapshot(canonical_json_bytes(doc))
