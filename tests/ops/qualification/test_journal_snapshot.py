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


# ---- S3 /v6 campaign budget snapshot vectors (beside the unchanged /v5) ------

PHASES_V3 = ('ADMISSION', 'N1', 'N1_CAPTURE', 'N1_G5', 'N2', 'N2_CAPTURE',
             'N2_G5', 'PART_A', 'PART_A_CAPTURE', 'PART_A_G5', 'RESULT', 'SEAL')


def funded_profile_v3():
    return dict(schema='qualification_campaign_budget_profile/v3',
        installed_profile_sha256='a' * 64, record_byte_limit=131072,
        funding_intents='qualification_campaign_funding/v1',
        phases={name: dict(cpu_ns=120_000_000_000, wall_ns=300_000_000_000, memory_bytes=256_000_000)
                for name in PHASES_V3},
        orchestration_cpu_ns={name: 20_000_000_000 for name in PHASES_V3})


def v5_snapshot():
    import base64
    import json
    return dict(schema='qualification_campaign_budget_snapshot/v5',
        attempt_id='vector-attempt', request_sha256='b' * 64, profile=funded_profile_v3(),
        budget=dict(identity_sha256='9' * 64, maximum_cpu_seconds=1500,
            maximum_wall_seconds=4000, maximum_memory_bytes=256_000_000, n1_paths=6, n2_paths=6,
            part_a_initial_paths=4, part_a_expanded_paths=8, n3_paths=6),
        start_clock=dict(schema='qualification_campaign_clock/v1', boot_id='boot-1',
            boottime_ns=10, utc='2026-09-21T00:00:00Z'),
        last_clock=dict(schema='qualification_campaign_clock/v1', boot_id='boot-1',
            boottime_ns=10, utc='2026-09-21T00:00:00Z'),
        deadline_boottime_ns=10_000_000_010, state='BOUND', validity='VALID',
        authority_revision=1, accounting_revision=1, authority_head='c' * 64, event_head='d' * 64,
        campaign_scope_id='fpq-scope', memory_peak_bytes=0, oom_events=0,
        works=[dict(work_id='admission', phase='ADMISSION',
            limits=funded_profile_v3()['phases']['ADMISSION'], input_sha256='e' * 64,
            reservation_bytes_b64=base64.b64encode(canonical_json_bytes(dict(
                limits=funded_profile_v3()['phases']['ADMISSION'],
                clock=dict(schema='qualification_campaign_clock/v1', boot_id='boot-1', boottime_ns=10,
                           utc='2026-09-21T00:00:00Z'), input_sha256='e' * 64))).decode('ascii'),
            state='COMPLETED', transitions=[base64.b64encode(canonical_json_bytes(dict(
                schema='qualification_campaign_work_transition/v1', attempt_id='vector-attempt',
                work_id='admission', state='COMPLETED',
                clock=dict(schema='qualification_campaign_clock/v1', boot_id='boot-1', boottime_ns=11,
                           utc='2026-09-21T00:00:01Z'), data={}))).decode('ascii')],
            observation_bytes_b64=base64.b64encode(canonical_json_bytes(dict(
                schema='qualification_campaign_observation/v2', attempt_id='vector-attempt',
                work_id='admission', clock=dict(schema='qualification_campaign_clock/v1', boot_id='boot-1',
                    boottime_ns=11, utc='2026-09-21T00:00:01Z'), campaign_scope_id='fpq-campaign',
                work_scope_id='fpq-payload', cpu_ns=0, memory_peak_bytes=0, oom_events=0,
                termination_known=True, orchestration_charge_cpu_ns=20_000_000_000))).decode('ascii'),
            charge_cpu_ns=20_000_000_000)],
        settled_cpu_ns=20_000_000_000, reserved_cpu_ns=0, remaining_cpu_ns=1_480_000_000_000,
        recoveries=[], dispatches=[dict(work_id='admission', role='guardian', owner_sha256='f' * 64,
            started_clock=dict(schema='qualification_campaign_clock/v1', boot_id='boot-1', boottime_ns=10,
                               utc='2026-09-21T00:00:00Z'), acknowledged_clock=dict(
                schema='qualification_campaign_clock/v1', boot_id='boot-1', boottime_ns=10,
                utc='2026-09-21T00:00:00Z'))])


def test_v5_budget_snapshot_bytes_are_pinned_unchanged():
    from c1_rail.qualification.journal_snapshot import parse_campaign_budget_snapshot
    raw = canonical_json_bytes(v5_snapshot())
    parse_campaign_budget_snapshot(raw)
    assert raw == V5_PINNED_BYTES


def test_v6_budget_snapshot_vector_beside_v5():
    import json
    from c1_rail.qualification.journal_snapshot import (encode_campaign_budget_snapshot,
        parse_campaign_budget_snapshot)
    doc = v5_snapshot()
    doc['schema'] = 'qualification_campaign_budget_snapshot/v6'
    doc['checkpoints'] = {'N1': dict(state='ATTESTED', work_id='n1work', payload_sha256='1' * 64,
                                     result_sha256='2' * 64, attestation_sha256='3' * 64)}
    raw = encode_campaign_budget_snapshot(doc)
    parsed = parse_campaign_budget_snapshot(raw)
    assert parsed['schema'] == 'qualification_campaign_budget_snapshot/v6'
    assert parsed['checkpoints']['N1']['state'] == 'ATTESTED'
    # The same v5 document with a checkpoints field is not a valid v5.
    with_checkpoints = v5_snapshot()
    with_checkpoints['checkpoints'] = doc['checkpoints']
    with pytest.raises(ValueError):
        parse_campaign_budget_snapshot(canonical_json_bytes(with_checkpoints))
    # A v6 without the checkpoints field refuses, and an uncommitted decision too.
    missing = v5_snapshot()
    missing['schema'] = 'qualification_campaign_budget_snapshot/v6'
    with pytest.raises(ValueError):
        parse_campaign_budget_snapshot(canonical_json_bytes(missing))
    premature = json.loads(json.dumps(doc))
    premature['checkpoints']['N1']['decision'] = 'CONTINUE'
    with pytest.raises(ValueError):
        parse_campaign_budget_snapshot(canonical_json_bytes(premature))


V5_PINNED_BYTES = canonical_json_bytes(v5_snapshot())
