"""C2 R4: release-bound operations and closed, authenticated joint batches."""

import base64
import copy
import json

import pytest
from test_campaign_n1 import campaign, settle, store, transition
from test_campaign_n2 import (
    G5, _committed_assessment, attestation_document, capture_checkpoint,
    committed_n1, committed_receipt, keys_map, n1_plan, n2_plan,
    result_document, run_work, sign_candidate, worker_payload,
)
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution import g5
from c1_rail.qualification.execution.protocol import sha256


def wire(instance, operation, **values):
    return instance.handle_request(G5, encoded({
        'schema': 'qualification_campaign_request/v2', 'operation': operation,
        'attempt_id': instance.attempt, 'checkpoint': 'N2', **values,
    }))


@pytest.mark.parametrize('operation,values', [
    ('CHECKPOINT_SNAPSHOT', {}),
    ('FETCH_CHECKPOINT_MEMBER', {'object_sha256': 'a' * 64, 'offset': 0, 'length': 1}),
    ('STAGE_CHECKPOINT_ARTIFACT', {'role': 'attempt_journal', 'bytes_b64': 'eA=='}),
    ('COMMIT_CHECKPOINT_ASSESSMENT', {
        'work_id': 'n2g5', 'candidate_bytes_b64': 'e30=', 'artifacts': [],
    }),
])
def test_v5_rejects_every_n2_checkpoint_operation(tmp_path, monkeypatch, operation, values):
    instance, _ = campaign(tmp_path, monkeypatch)
    with pytest.raises(ValueError, match='installed N2 dispatch release required'):
        wire(instance, operation, **values)


def joint_capture(tmp_path, monkeypatch, *, full_fail=False, halves_fail=False):
    instance = committed_n1(tmp_path, monkeypatch)
    plan = n2_plan(instance, committed_receipt(instance))
    run_work(instance, 'n2work', 'n2_worker')
    payload = worker_payload(instance, plan=plan, checkpoint='N2', work='n2work',
                             full_fail=full_fail, halves_fail=halves_fail)
    capture_checkpoint(instance, 'n2work', 'N2', payload)
    settle(instance, 'n2work')
    transition(instance, 'n2work', 'COMPLETED')
    run_work(instance, 'n2g5', 'n2_g5')
    capture = store(instance).checkpoint_capture(instance.attempt, 'N2')
    args = {
        'checkpoint': 'N2', 'plan_bytes': plan,
        'attestation_bytes': capture['attestation_bytes'],
        'snapshot_bytes': store(instance).checkpoint_snapshot(instance.attempt, 'N2'),
        'current_keys': keys_map(instance.case),
        'artifacts': {
            'result': capture['result_bytes'], 'worker_result': payload,
            'predecessor_receipt': committed_receipt(instance),
            'predecessor_assessment': _committed_assessment(instance),
            'predecessor_plan': n1_plan(instance),
            'predecessor_payload': store(instance).checkpoint_capture(
                instance.attempt, 'N1')['payload_bytes'],
        },
    }
    return instance, args


@pytest.mark.parametrize('full_fail,halves_fail,expected', [
    (False, False, 'PART_A_READY'), (True, False, 'N2_FAILED'),
    (False, True, 'N2_FAILED'),
])
def test_joint_assessment_commits_through_service(
    tmp_path, monkeypatch, full_fail, halves_fail, expected,
):
    instance, args = joint_capture(tmp_path, monkeypatch,
                                  full_fail=full_fail, halves_fail=halves_fail)
    evidence = g5.validate_campaign_checkpoint(instance.verified, **args)
    for role, raw in evidence.output_bytes_by_role.items():
        wire(instance, 'STAGE_CHECKPOINT_ARTIFACT', role=role,
             bytes_b64=base64.b64encode(raw).decode('ascii'))
    response = json.loads(wire(
        instance, 'COMMIT_CHECKPOINT_ASSESSMENT', work_id='n2g5',
        candidate_bytes_b64=base64.b64encode(sign_candidate(instance, evidence)).decode('ascii'),
        artifacts=[{'role': role, 'sha256': sha256(raw)}
                   for role, raw in sorted(evidence.output_bytes_by_role.items())],
    ))
    assert response['receipt']['campaign_state'] == expected
    settle(instance, 'n2g5')
    transition(instance, 'n2g5', 'COMPLETED')
    state = json.loads(store(instance).budget_snapshot(instance.attempt))
    assert state['state'] == expected
    assert next(w for w in state['works'] if w['work_id'] == 'n2g5')['state'] == 'COMPLETED'


@pytest.mark.parametrize('mutation', [
    'missing_half', 'extra_population', 'stage_label', 'population_order',
    'extra_record', 'unknown_stage', 'seed', 'count', 'unused_record', 'record_order',
    'separate_speed_sample',
])
def test_authenticated_malformed_joint_batch_refuses_reconstruction(tmp_path, monkeypatch, mutation):
    instance, args = joint_capture(tmp_path, monkeypatch)
    doc = json.loads(args['artifacts']['worker_result'])
    if mutation == 'missing_half':
        doc['populations'].pop()
    elif mutation == 'extra_population':
        doc['populations'].append(copy.deepcopy(doc['populations'][0]))
    elif mutation == 'stage_label':
        doc['populations'][1]['stage'] = 'N2'
    elif mutation == 'population_order':
        doc['populations'][1:3] = reversed(doc['populations'][1:3])
    elif mutation == 'extra_record':
        doc['path_inventory']['records'].append(copy.deepcopy(doc['path_inventory']['records'][0]))
    elif mutation == 'unknown_stage':
        doc['path_inventory']['records'][0]['stage'] = 'IGNORED'
    elif mutation == 'unused_record':
        extra = dict(doc['path_inventory']['records'][0], stage='IGNORED')
        doc['path_inventory']['records'].append(extra)
    elif mutation == 'record_order':
        records = doc['path_inventory']['records']
        records.insert(0, records.pop())
    elif mutation == 'separate_speed_sample':
        sample = copy.deepcopy(doc['populations'][0]['outcomes'])
        sample[0]['sessions_to_pass'] = 2
        doc['populations'][0]['speed_outcomes'] = sample
    elif mutation == 'seed':
        doc['path_inventory']['records'][0]['seed_input_sha256'] = 'a' * 64
    else:
        doc['populations'][0]['outcomes'].pop()
    payload = encoded(doc)
    result = result_document(instance, 'n2work', 'N2', payload, args['plan_bytes'])
    attestation = attestation_document(instance, 'n2work', 'N2', result, payload, args['plan_bytes'])
    snapshot = json.loads(args['snapshot_bytes'])
    snapshot['capture'].update(payload_sha256=sha256(payload), result_sha256=sha256(result),
                               attestation_sha256=sha256(attestation))
    args.update(snapshot_bytes=encoded(snapshot), attestation_bytes=attestation)
    args['artifacts'].update(result=result, worker_result=payload)
    # Hashes and execution signature are coherent. Failure must come from
    # reconstruction, not the outer capture-membership rejection.
    with pytest.raises(ValueError) as exc:
        g5.validate_campaign_checkpoint(instance.verified, **args)
    assert 'membership differs' not in str(exc.value)


def test_unset_joint_failure_thresholds_remain_null(tmp_path, monkeypatch):
    instance, args = joint_capture(tmp_path, monkeypatch)
    thresholds = json.loads(args['plan_bytes'])['thresholds']
    expected = {row['stage']: row['max_failures_per_population'] for row in thresholds}
    assert any(value is None for value in expected.values()), 'exercise an unset frozen cap'
    evidence = g5.validate_campaign_checkpoint(instance.verified, **args)
    assert json.loads(evidence.assessment_bytes)['cutoff']['stage_thresholds'] == expected


@pytest.mark.parametrize('mutation', ['foreign', 'stale', 'uncommitted'])
def test_predecessor_refusal_reaches_joint_reconstruction(tmp_path, monkeypatch, mutation):
    instance, args = joint_capture(tmp_path, monkeypatch)
    receipt = json.loads(args['artifacts']['predecessor_receipt'])
    if mutation == 'foreign':
        receipt['attempt_id'] = 'another-attempt'
    elif mutation == 'stale':
        receipt.update(decision='FAILURE', campaign_state='N1_FAILED')
    else:
        receipt['work_id'] = 'uncommitted-work'
    # The actual N2 capture and its signature stay valid; only the alleged
    # predecessor changes. G5's outer capture-membership checks all pass.
    args['artifacts']['predecessor_receipt'] = encoded(receipt)
    with pytest.raises(ValueError, match='predecessor receipt binding differs'):
        g5.validate_campaign_checkpoint(instance.verified, **args)
