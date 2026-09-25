"""S4 joint N2/Part B batch: one capture, one attestation, one assessment with
two stage decisions, bound to the committed N1 receipt. Real SQLite journals,
real admitted campaigns and plans; synthesized trusted clocks/identities and
outcome batches. No Linux enforcement is claimed here -- the host-side cases
live in tests/integration/qualification_boundary/test_campaign_n2_linux.py.
"""

import base64
import json
from contextlib import contextmanager
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest
from bundle_fixture import build_bundle
from test_campaign_admission import running
from test_campaign_n1 import (
    NOW,
    clock,
    dispatched,
    materialized,
    retained_identity,
    schedule_document,
    settle,
    snap,
    store,
    transition,
)
from c1_rail.qualification.checkpoint_plan import derive_checkpoint_plan
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution import campaign_supervisor as supervisor
from c1_rail.qualification.execution import g5 as g5_module
from c1_rail.qualification.execution.campaign_funding import DISPATCH_ROLES
from c1_rail.qualification.execution.campaign_store import CampaignStore
from c1_rail.qualification.execution.compute import stage_request
from c1_rail.qualification.execution.evidence import encode_worker_result
from c1_rail.qualification.execution.plan import derive_campaign_plan_from_context
from c1_rail.qualification.execution.protocol import sha256
from c1_rail.qualification.model import PathOutcome
from c1_rail.qualification.source_admission import admit_source

CLIENT, G5, OPERATOR, SERVICE_UID = 1001, 1002, 1003, 1004


def keys_map(case):
    return {
        key.key_id: SimpleNamespace(public_key=key.public_key)
        for key in case['keys'].values()
    }


def n2_campaign(tmp_path, monkeypatch, *, t=21):
    """A warm joint-dispatch service (release/v6, budget profile/v3) with a
    fully admitted campaign: the S3 scene over the /v6 installation."""
    from contextlib import nullcontext
    from test_campaign_n1 import Runtime, submit, verified_context

    instance, case = running(tmp_path, monkeypatch, dispatch=True, joint=True)
    instance.config = {'host_run_id': 'host1', 'service_uid': SERVICE_UID}
    instance.recovery_issues = {}
    instance.schedule_eligible = True
    instance.dispatch_eligible = True
    instance.joint_dispatch_eligible = True
    monkeypatch.setattr(supervisor, 'controller_cpu_guard', nullcontext)
    monkeypatch.setattr(supervisor, 'LinuxCampaignRuntime', Runtime)
    state = {'t': t}
    monkeypatch.setattr(supervisor, 'observe_campaign_clock', lambda: encoded(clock(state)))
    instance.clocks = state
    from test_campaign_n1 import admission_observation

    request_bytes = submit(instance, case)
    context = verified_context(instance, case)
    plan = derive_campaign_plan_from_context(context)
    status = CampaignStore(instance.store).finish_diagnostic_admission(
        request_bytes,
        context,
        plan,
        admission_observation(case, state),
        now=NOW,
        trusted_keys=case['keys'],
    )
    assert status['receipt'] is not None and status['state'] == 'BOUND'
    instance.attempt = case['attempt_id']
    instance.case = case
    instance.verified = context
    instance.campaign_plan = plan
    instance.admitted = admit_source(
        context.contract, artifact_root=context.bundle_dir, policy=context.policy
    )
    return instance, case


def n1_plan(instance):
    return derive_checkpoint_plan(instance.campaign_plan, 'N1', None)


def n2_plan(instance, receipt):
    return derive_checkpoint_plan(instance.campaign_plan, 'N2', receipt)


def committed_receipt(instance, checkpoint='N1'):
    with instance.store.transaction() as connection:
        row = connection.execute(
            'SELECT receipt_bytes FROM full_campaign_checkpoint_intents '
            'WHERE attempt_id=? AND checkpoint=?',
            (instance.attempt, checkpoint),
        ).fetchone()
    assert row is not None, 'committed ' + checkpoint + ' receipt required'
    return bytes(row[0])


def _outcomes(count, *, fail):
    return [
        PathOutcome(
            'FAILURE' if fail else 'PASS',
            None if fail else 1,
            'fixture-failure' if fail else None,
            (),
        )
        for _ in range(count)
    ]


def worker_payload(instance, *, plan, checkpoint, work, n1_pass=True, full_fail=False, halves_fail=False):
    """The synthesized captured batch through the production serializer.

    N1: 2x(FULL,H1,H2); N2 joint: FULL at the frozen N2 depth (stage N2) plus
    H1/H2 at the frozen PART_B depth (stage PART_B) in one framed result."""
    depths = json.loads(plan)['depths']
    if checkpoint == 'N1':
        sections = [
            (row['population'], 'N1', _outcomes(row['depth'], fail=not n1_pass))
            for row in depths
        ]
        stage = 'n1'
    else:
        sections = [
            (
                row['population'],
                row['statistics_stage'],
                _outcomes(
                    row['depth'],
                    fail=full_fail if row['statistics_stage'] == 'N2' else halves_fail,
                ),
            )
            for row in depths
        ]
        stage = 'n2'
    run = SimpleNamespace(
        stage=stage,
        populations=tuple(
            (population, tuple(rows)) for population, _, rows in sections
        ),
        synthetic=instance.verified.domain.permits_synthetic,
    )
    return encode_worker_result(
        instance.verified,
        work,
        plan,
        run,
        {'worker_compute_wall_ns': 1, 'worker_cpu_ns': 1, 'worker_peak_memory_bytes': 1},
        admitted=instance.admitted,
    )


def _work_phase(instance, work):
    return next(
        row['phase'] for row in snap(instance)['works'] if row['work_id'] == work
    )


def result_document(instance, work, checkpoint, payload, plan):
    phase = 'N1' if checkpoint == 'N1' else 'N2'
    scopes = supervisor.work_enrollment('host1', instance.attempt, work)
    state = snap(instance)
    release = json.loads(instance.release)
    return encoded(
        {
            'schema': 'qualification_campaign_checkpoint_result/v1',
            'attempt_id': instance.attempt,
            'checkpoint': checkpoint,
            'work_id': work,
            'campaign_id': 'campaign-1',
            'plan_sha256': sha256(plan),
            'plan_byte_length': len(plan),
            'payload_sha256': sha256(payload),
            'payload_byte_length': len(payload),
            'worker_execution_id': work,
            'container_id': '9' * 64,
            'worker_image_digest': release['worker_image_digest'],
            'runtime_manifest_sha256': sha256(
                encoded(release['runtime_manifests']['worker'])
            ),
            'capture': {
                'exit_code': 0,
                'oom_killed': False,
                'started_utc': '2026-09-22T00:00:01Z',
                'completed_utc': '2026-09-22T00:00:02Z',
                'authorized_at_utc': '2026-09-22T00:00:00Z',
                'campaign_scope_id': scopes['campaign_slice'],
                'work_scope_id': scopes['payload_slice'],
                'payload_slice': scopes['payload_slice'],
            },
            'limits': {
                'cpu_ns': state['profile']['phases'][phase]['cpu_ns'],
                'wall_ns': state['profile']['phases'][phase]['wall_ns'],
                'memory_bytes': state['profile']['phases'][phase]['memory_bytes'],
                'orchestration_cpu_ns': state['profile']['orchestration_cpu_ns'][phase],
            },
            'observations': {
                'exit_code': 0,
                'oom_killed': False,
                'worker_compute_wall_ns': 1,
                'worker_cpu_ns': 1,
                'worker_peak_memory_bytes': 1,
            },
            'created_utc': '2026-09-22T00:00:03Z',
        }
    )


def attestation_document(instance, work, checkpoint, result, payload, plan):
    release = json.loads(instance.release)
    parsed = json.loads(result)
    core = {
        'schema': 'qualification_campaign_checkpoint_attestation_payload/v1',
        'scope': 'ATTEST_CAMPAIGN_CHECKPOINT',
        'attempt_id': instance.attempt,
        'checkpoint': checkpoint,
        'work_id': work,
        'result_sha256': sha256(result),
        'payload_sha256': sha256(payload),
        'payload_byte_length': len(payload),
        'plan_sha256': sha256(plan),
        'execution_release_sha256': sha256(instance.release),
        'profile_sha256': release['profile_sha256'],
        'service_id': release['service_id'],
        'worker_image_digest': parsed['worker_image_digest'],
        'runtime_manifest_sha256': parsed['runtime_manifest_sha256'],
        'container_id': parsed['container_id'],
        'capture': {
            'exit_code': 0,
            'oom_killed': False,
            'campaign_scope_id': parsed['capture']['campaign_scope_id'],
            'work_scope_id': parsed['capture']['work_scope_id'],
            'payload_slice': parsed['capture']['payload_slice'],
        },
        'observations': dict(parsed['observations']),
        'authorized_at_utc': '2026-09-22T00:00:00Z',
        'started_utc': '2026-09-22T00:00:01Z',
        'completed_utc': '2026-09-22T00:00:02Z',
        'campaign_revision': snap(instance)['authority_revision'],
    }
    signature = instance.case['private']['test-execution'].sign(encoded(core))
    return encoded(
        {
            'schema': 'qualification_campaign_checkpoint_attestation/v1',
            'payload': core,
            'signature': {
                'algorithm': 'Ed25519',
                'key_id': 'test-execution',
                'value_b64': base64.b64encode(signature).decode('ascii'),
            },
        }
    )


def capture_checkpoint(instance, work, checkpoint, payload):
    plan = (
        n1_plan(instance)
        if checkpoint == 'N1'
        else n2_plan(instance, committed_receipt(instance))
    )
    result = result_document(instance, work, checkpoint, payload, plan)
    transition_bytes = encoded(
        {
            'schema': 'qualification_campaign_work_transition/v1',
            'attempt_id': instance.attempt,
            'work_id': work,
            'state': 'CAPTURED',
            'clock': json.loads(supervisor.observe_campaign_clock()),
            'data': {'capture_bytes_b64': base64.b64encode(result).decode('ascii')},
        }
    )
    store(instance).retain_checkpoint_capture(
        instance.attempt, work, result, payload, transition_bytes, checkpoint=checkpoint
    )
    attestation = attestation_document(instance, work, checkpoint, result, payload, plan)
    store(instance).retain_checkpoint_attestation(
        instance.attempt, attestation, checkpoint=checkpoint, verify=lambda *a, **k: None
    )
    return result, attestation


def run_work(instance, work, role):
    materialized(instance, schedule_document(instance, role=role, work=work))
    retained_identity(instance, work)
    transition(instance, work, 'RUNNING')
    dispatched(instance, work)


def committed_n1(tmp_path, monkeypatch):
    """The genuine N1 prefix: real reconstruction, real signatures, committed
    receipt, campaign N2_READY -- the S4 scene's predecessor state."""
    instance, case = n2_campaign(tmp_path, monkeypatch)
    run_work(instance, 'n1work', 'n1_worker')
    payload = worker_payload(
        instance, plan=n1_plan(instance), checkpoint='N1', work='n1work'
    )
    capture_checkpoint(instance, 'n1work', 'N1', payload)
    settle(instance, 'n1work')
    transition(instance, 'n1work', 'COMPLETED')
    run_work(instance, 'g5work', 'n1_g5')
    evidence = g5_module.validate_campaign_checkpoint(
        instance.verified,
        checkpoint='N1',
        plan_bytes=n1_plan(instance),
        attestation_bytes=store(instance).checkpoint_capture(instance.attempt, 'N1')[
            'attestation_bytes'
        ],
        artifacts={
            'result': store(instance).checkpoint_capture(instance.attempt, 'N1')['result_bytes'],
            'worker_result': payload,
        },
        snapshot_bytes=store(instance).checkpoint_snapshot(instance.attempt, 'N1'),
        current_keys=keys_map(case),
    )
    candidate = sign_candidate(instance, evidence)
    persist_intent(instance, 'g5work', 'N1', candidate)
    reply = json.loads(commit(instance, 'g5work', 'N1', candidate))
    assert reply['receipt']['campaign_state'] == 'N2_READY'
    assert snap(instance)['state'] == 'N2_READY'
    settle(instance, 'g5work')
    transition(instance, 'g5work', 'COMPLETED')
    return instance


def sign_candidate(instance, evidence):
    core = json.loads(evidence.assessment_bytes.decode())
    value = instance.case['private']['test-producer'].sign(evidence.assessment_bytes)
    return encoded(
        dict(
            core,
            signature={
                'algorithm': 'Ed25519',
                'key_id': 'test-producer',
                'value_b64': base64.b64encode(value).decode('ascii'),
            },
        )
    )


def persist_intent(instance, work, checkpoint, candidate):
    campaigns = store(instance)
    snapshot = campaigns.checkpoint_snapshot(instance.attempt, checkpoint)
    intent = encoded(
        {
            'schema': 'qualification_campaign_checkpoint_intent/v1',
            'attempt_id': instance.attempt,
            'checkpoint': checkpoint,
            'work_id': work,
            'key_id': 'test-producer',
            'signing_at_utc': '2026-09-22T01:00:00Z',
            'candidate_sha256': sha256(candidate),
            'snapshot_sha256': sha256(snapshot),
        }
    )
    capture = encoded(
        {
            'schema': 'qualification_campaign_g5_capture/v1',
            'attempt_id': instance.attempt,
            'checkpoint': checkpoint,
            'work_id': work,
            'candidate_sha256': sha256(candidate),
            'staged': [],
        }
    )
    capture_transition = encoded(
        {
            'schema': 'qualification_campaign_work_transition/v1',
            'attempt_id': instance.attempt,
            'work_id': work,
            'state': 'CAPTURED',
            'clock': json.loads(supervisor.observe_campaign_clock()),
            'data': {'capture_bytes_b64': base64.b64encode(capture).decode('ascii')},
        }
    )
    signing_transition = encoded(
        {
            'schema': 'qualification_campaign_work_transition/v1',
            'attempt_id': instance.attempt,
            'work_id': work,
            'state': 'SIGNING_INTENT',
            'clock': json.loads(supervisor.observe_campaign_clock()),
            'data': {
                'intent_id': work + '-intent',
                'payload_bytes_b64': base64.b64encode(candidate).decode('ascii'),
                'key_id': 'test-producer',
                'signing_at_utc': '2026-09-22T01:00:00Z',
            },
        }
    )
    campaigns.persist_checkpoint_intent(
        instance.attempt,
        work,
        snapshot,
        intent,
        candidate,
        capture_transition,
        signing_transition,
        checkpoint=checkpoint,
    )
    return candidate


def cutoff_document(instance, checkpoint, candidate):
    core = json.loads(candidate)
    if checkpoint == 'N1':
        return encoded(
            {
                'schema': 'qualification_campaign_cutoff_receipt/v1',
                'attempt_id': instance.attempt,
                'checkpoint': 'N1',
                'assessment_sha256': sha256(candidate),
                'decision': core['decision'],
                'n1_cutoffs': core['cutoff']['n1_cutoffs'],
                'n2_thresholds': core['n2_thresholds']['stages'],
                'n2_bound_to': sha256(candidate),
                'created_utc': '2026-09-22T02:00:00Z',
            }
        )
    return encoded(
        {
            'schema': 'qualification_campaign_cutoff_receipt/v1',
            'attempt_id': instance.attempt,
            'checkpoint': 'N2',
            'assessment_sha256': sha256(candidate),
            'decision': core['decision'],
            'stage_decisions': core['stage_decisions'],
            'stage_thresholds': core['cutoff']['stage_thresholds'],
            'predecessor_receipt_sha256': sha256(committed_receipt(instance)),
            'created_utc': '2026-09-22T02:00:00Z',
        }
    )


def commit(instance, work, checkpoint, candidate):
    return store(instance).commit_checkpoint_assessment(
        instance.attempt,
        work,
        candidate,
        cutoff_document(instance, checkpoint, candidate),
        now=datetime(2026, 9, 22, tzinfo=timezone.utc),
        clock_bytes=supervisor.observe_campaign_clock(),
        checkpoint=checkpoint,
    )


def committed_n2(tmp_path, monkeypatch, *, full_fail=False, halves_fail=False):
    """The joint batch scene: one n2_worker capture, one assessment carrying
    both stage decisions, committed by the n2 g5 work."""
    instance = committed_n1(tmp_path, monkeypatch)
    run_work(instance, 'n2work', 'n2_worker')
    payload = worker_payload(
        instance,
        plan=n2_plan(instance, committed_receipt(instance)),
        checkpoint='N2',
        work='n2work',
        full_fail=full_fail,
        halves_fail=halves_fail,
    )
    capture_checkpoint(instance, 'n2work', 'N2', payload)
    settle(instance, 'n2work')
    transition(instance, 'n2work', 'COMPLETED')
    run_work(instance, 'n2g5', 'n2_g5')
    capture = store(instance).checkpoint_capture(instance.attempt, 'N2')
    predecessor = store(instance).checkpoint_capture(instance.attempt, 'N1')
    evidence = g5_module.validate_campaign_checkpoint(
        instance.verified,
        checkpoint='N2',
        plan_bytes=n2_plan(instance, committed_receipt(instance)),
        attestation_bytes=capture['attestation_bytes'],
        artifacts={
            'result': capture['result_bytes'],
            'worker_result': payload,
            'predecessor_receipt': committed_receipt(instance),
            'predecessor_assessment': _committed_assessment(instance),
            'predecessor_plan': n1_plan(instance),
            'predecessor_payload': predecessor['payload_bytes'],
        },
        snapshot_bytes=store(instance).checkpoint_snapshot(instance.attempt, 'N2'),
        current_keys=keys_map(instance.case),
    )
    candidate = sign_candidate(instance, evidence)
    persist_intent(instance, 'n2g5', 'N2', candidate)
    reply = json.loads(commit(instance, 'n2g5', 'N2', candidate))
    return instance, evidence, reply


def _committed_assessment(instance):
    with instance.store.transaction() as connection:
        row = connection.execute(
            'SELECT candidate_bytes FROM full_campaign_checkpoint_intents '
            'WHERE attempt_id=? AND checkpoint=?',
            (instance.attempt, 'N1'),
        ).fetchone()
    assert row is not None
    return bytes(row[0])


# ---- The two discriminating cases (the slice's first checkbox) ---------------


def test_full_fails_while_halves_pass_is_one_failure_decision(tmp_path, monkeypatch):
    """FULL fails while halves pass: one batch, both decisions, N2_FAILED, and
    no Part A work may ever follow."""
    instance, evidence, reply = committed_n2(
        tmp_path, monkeypatch, full_fail=True, halves_fail=False
    )
    decisions = json.loads(evidence.assessment_bytes)['stage_decisions']
    assert decisions == {'N2': 'FAIL', 'PART_B': 'PASS'}
    assert reply['receipt']['decision'] == 'FAILURE'
    assert reply['receipt']['campaign_state'] == 'N2_FAILED'
    state = snap(instance)
    assert state['state'] == 'N2_FAILED'
    assert state['schema'] == 'qualification_campaign_budget_snapshot/v7'
    assert state['checkpoints']['N2']['stage_decisions'] == decisions
    with pytest.raises(
        ValueError, match='bound budget and installed phase required|terminal campaign budget'
    ):
        store(instance).reserve_work(
            instance.attempt,
            'partawork',
            'PART_A',
            encoded(
                {
                    'limits': state['profile']['phases']['PART_A'],
                    'clock': json.loads(supervisor.observe_campaign_clock()),
                    'input_sha256': '0' * 64,
                }
            ),
            expected_revision=state['authority_revision'],
        )


def test_halves_fail_while_full_passes_is_one_failure_decision(tmp_path, monkeypatch):
    """Halves fail while FULL passes: the mirror discriminator -- N2 PASS,
    PART_B FAIL, the same single FAILURE decision and terminal N2_FAILED."""
    instance, evidence, reply = committed_n2(
        tmp_path, monkeypatch, full_fail=False, halves_fail=True
    )
    decisions = json.loads(evidence.assessment_bytes)['stage_decisions']
    assert decisions == {'N2': 'PASS', 'PART_B': 'FAIL'}
    assert reply['receipt']['campaign_state'] == 'N2_FAILED'
    assert snap(instance)['state'] == 'N2_FAILED'


def test_joint_pass_reaches_part_a_ready(tmp_path, monkeypatch):
    """Both stages PASS: CONTINUE, PART_A_READY, the committed N1 rows frozen,
    and the committing n2 g5 work completes in the state it produced."""
    instance, evidence, reply = committed_n2(tmp_path, monkeypatch)
    decisions = json.loads(evidence.assessment_bytes)['stage_decisions']
    assert decisions == {'N2': 'PASS', 'PART_B': 'PASS'}
    assert reply['receipt']['decision'] == 'CONTINUE'
    assert reply['receipt']['campaign_state'] == 'PART_A_READY'
    state = snap(instance)
    assert state['state'] == 'PART_A_READY'
    assert state['checkpoints']['N1']['state'] == 'COMMITTED'
    assert state['checkpoints']['N1']['decision'] == 'CONTINUE'
    settle(instance, 'n2g5')
    transition(instance, 'n2g5', 'COMPLETED')
    state = snap(instance)
    assert state['state'] == 'PART_A_READY'
    assert next(w for w in state['works'] if w['work_id'] == 'n2g5')['state'] == 'COMPLETED'


def test_committed_n2_g5_overrun_ends_authority(tmp_path, monkeypatch):
    """A post-commit overrun of the committing N2_G5 work ends authority from
    PART_A_READY; the receipt survives as history only."""
    instance = committed_n2(tmp_path, monkeypatch)[0]
    limit = next(w for w in snap(instance)['works'] if w['work_id'] == 'n2g5')['limits'][
        'cpu_ns'
    ]
    settle(instance, 'n2g5', cpu=limit + 1)
    assert snap(instance)['state'] == 'BUDGET_EXHAUSTED'
    with pytest.raises(ValueError, match='terminal campaign budget'):
        transition(instance, 'n2g5', 'COMPLETED')


def test_n2_snapshot_serves_the_predecessor_family(tmp_path, monkeypatch):
    instance = committed_n1(tmp_path, monkeypatch)
    run_work(instance, 'n2work', 'n2_worker')
    payload = worker_payload(
        instance,
        plan=n2_plan(instance, committed_receipt(instance)),
        checkpoint='N2',
        work='n2work',
    )
    capture_checkpoint(instance, 'n2work', 'N2', payload)
    snapshot = json.loads(store(instance).checkpoint_snapshot(instance.attempt, 'N2'))
    members = {row['role']: row['sha256'] for row in snapshot['members']}
    assert {
        'plan',
        'result',
        'payload',
        'attestation',
        'retained_bundle_index',
        'predecessor_receipt',
        'predecessor_assessment',
        'predecessor_plan',
        'predecessor_payload',
    } <= set(members)
    assert members['predecessor_receipt'] == sha256(committed_receipt(instance))
    assert snapshot['predecessor'] == {
        'checkpoint': 'N1',
        'assessment_sha256': sha256(_committed_assessment(instance)),
        'receipt_sha256': sha256(committed_receipt(instance)),
    }
    assert snapshot['capture']['payload_sha256'] == sha256(payload)


def test_foreign_or_missing_predecessor_refuses(tmp_path, monkeypatch):
    """A missing, foreign or stale predecessor receipt refuses with a closed
    reason at derivation and at the committed boundary."""
    instance = committed_n1(tmp_path, monkeypatch)
    campaign = instance.campaign_plan
    with pytest.raises(ValueError, match='predecessor receipt required'):
        derive_checkpoint_plan(campaign, 'N2', None)
    foreign = encoded(
        dict(
            json.loads(committed_receipt(instance)),
            attempt_id='foreign-attempt',
        )
    )
    with pytest.raises(ValueError, match='predecessor receipt binding differs'):
        derive_checkpoint_plan(campaign, 'N2', foreign)
    stale = encoded(
        dict(
            json.loads(committed_receipt(instance)),
            decision='FAILURE',
            campaign_state='N1_FAILED',
        )
    )
    with pytest.raises(ValueError, match='committed predecessor decision differs'):
        derive_checkpoint_plan(campaign, 'N2', stale)
    run_work(instance, 'n2work', 'n2_worker')
    payload = worker_payload(
        instance,
        plan=n2_plan(instance, committed_receipt(instance)),
        checkpoint='N2',
        work='n2work',
    )
    capture_checkpoint(instance, 'n2work', 'N2', payload)
    capture = store(instance).checkpoint_capture(instance.attempt, 'N2')
    plan_bytes = n2_plan(instance, committed_receipt(instance))
    tampered = derive_checkpoint_plan(
        campaign, 'N2', encoded(dict(json.loads(committed_receipt(instance))))
    )
    assert tampered == plan_bytes
    run_work(instance, 'n2g5', 'n2_g5')
    with pytest.raises(
        ValueError,
        match='predecessor receipt binding differs|checkpoint capture membership differs',
    ):
        g5_module.validate_campaign_checkpoint(
            instance.verified,
            checkpoint='N2',
            plan_bytes=derive_checkpoint_plan(
                campaign,
                'N2',
                encoded(dict(json.loads(committed_receipt(instance)), work_id='other')),
            ),
            attestation_bytes=capture['attestation_bytes'],
            artifacts={
                'result': capture['result_bytes'],
                'worker_result': payload,
                'predecessor_receipt': committed_receipt(instance),
                'predecessor_assessment': _committed_assessment(instance),
                'predecessor_plan': n1_plan(instance),
                'predecessor_payload': store(instance).checkpoint_capture(
                    instance.attempt, 'N1'
                )['payload_bytes'],
            },
            snapshot_bytes=store(instance).checkpoint_snapshot(instance.attempt, 'N2'),
            current_keys=keys_map(instance.case),
        )


def test_substituted_joint_batch_refuses_at_validation(tmp_path, monkeypatch):
    """A batch whose FULL rows were substituted for the speed sample, or whose
    order/count/seed changed, refuses in the closed reconstruction."""
    instance = committed_n1(tmp_path, monkeypatch)
    run_work(instance, 'n2work', 'n2_worker')
    payload = worker_payload(
        instance,
        plan=n2_plan(instance, committed_receipt(instance)),
        checkpoint='N2',
        work='n2work',
    )
    capture_checkpoint(instance, 'n2work', 'N2', payload)
    capture = store(instance).checkpoint_capture(instance.attempt, 'N2')
    base = {
        'result': capture['result_bytes'],
        'worker_result': payload,
        'predecessor_receipt': committed_receipt(instance),
        'predecessor_assessment': _committed_assessment(instance),
        'predecessor_plan': n1_plan(instance),
        'predecessor_payload': store(instance).checkpoint_capture(instance.attempt, 'N1')[
            'payload_bytes'
        ],
    }
    doc = json.loads(payload)
    doc['populations'][0]['outcomes'][0]['sessions_to_pass'] = 3
    reordered = encoded(doc)
    with pytest.raises(ValueError, match='checkpoint capture membership differs'):
        g5_module.validate_campaign_checkpoint(
            instance.verified,
            checkpoint='N2',
            plan_bytes=n2_plan(instance, committed_receipt(instance)),
            attestation_bytes=capture['attestation_bytes'],
            artifacts=dict(base, worker_result=reordered),
            snapshot_bytes=store(instance).checkpoint_snapshot(instance.attempt, 'N2'),
            current_keys=keys_map(instance.case),
        )


def test_crash_after_n2_intent_recovers_the_exact_candidate(tmp_path, monkeypatch):
    """Crash after START_INTENT without capture is IN_DOUBT; after the capture
    the retained bytes recover and an altered retry refuses."""
    instance = committed_n1(tmp_path, monkeypatch)
    run_work(instance, 'n2work', 'n2_worker')
    transition(instance, 'n2work', 'IN_DOUBT')
    assert snap(instance)['state'] == 'IN_DOUBT'
    instance2 = committed_n1(tmp_path / 'second', monkeypatch)
    run_work(instance2, 'n2work', 'n2_worker')
    payload = worker_payload(
        instance2,
        plan=n2_plan(instance2, committed_receipt(instance2)),
        checkpoint='N2',
        work='n2work',
    )
    capture_checkpoint(instance2, 'n2work', 'N2', payload)
    campaigns = store(instance2)
    with pytest.raises(
        ValueError,
        match='immutable checkpoint capture differs|archived payload differs',
    ):
        campaigns.retain_checkpoint_capture(
            instance2.attempt,
            'n2work',
            campaigns.checkpoint_capture(instance2.attempt, 'N2')['result_bytes'],
            b'substituted',
            encoded(
                {
                    'schema': 'qualification_campaign_work_transition/v1',
                    'attempt_id': instance2.attempt,
                    'work_id': 'n2work',
                    'state': 'CAPTURED',
                    'clock': json.loads(supervisor.observe_campaign_clock()),
                    'data': {
                        'capture_bytes_b64': base64.b64encode(
                            campaigns.checkpoint_capture(instance2.attempt, 'N2')['result_bytes']
                        ).decode('ascii')
                    },
                }
            ),
            checkpoint='N2',
        )


# ---- Producer-level and fail-on-base regressions ------------------------------


def test_joint_depths_are_from_the_frozen_contract(tmp_path):
    """The slice's mandatory producer-level regression, verbatim."""
    contract = build_bundle(tmp_path)['contract']
    request = stage_request(contract, 'n2', 1.0)
    assert request.depths == (
        ('FULL', contract.stage_specs['N2'].exact_depth),
        ('H1', contract.stage_specs['PART_B'].exact_depth),
        ('H2', contract.stage_specs['PART_B'].exact_depth),
    )


def test_v5_route_refuses_the_n2_dispatch_roles(tmp_path, monkeypatch):
    """Fail-on-base: on the /v5 N1-only dispatch installation the joint roles
    refuse with the joint-release gate (the roles do not parse on the base)."""
    import threading
    from contextlib import nullcontext

    from c1_rail.qualification.execution.service import ExecutionService
    from c1_rail.qualification.execution.store import ExecutionStore

    service = object.__new__(ExecutionService)
    service.store = ExecutionStore(tmp_path / 'journal.sqlite')
    service.config = {'host_run_id': 'host1', 'service_uid': SERVICE_UID}
    service.dispatch_lock = threading.Lock()
    service.recovery_issues = {}
    service.schedule_eligible = True
    service.dispatch_eligible = True
    service.joint_dispatch_eligible = False
    monkeypatch.setattr(supervisor, 'controller_cpu_guard', nullcontext)
    document = encoded(
        {
            'schema': 'qualification_campaign_schedule_request/v1',
            'attempt_id': 'a1',
            'work_id': 'n2work',
            'role': 'n2_worker',
            'probe': 'noop',
            'signing_retry_of': None,
            'fault': None,
        }
    )
    with pytest.raises(ValueError, match='installed N2 dispatch release required'):
        service._schedule_request(SERVICE_UID, document)


def test_joint_continuation_prefix_requires_the_versioned_policy():
    """Fail-on-base: order[:4] with (PARTIAL, NONE) is legal only under the
    versioned FULL_E1 policy identity; the pre-S4 document keeps refusing it."""
    from c1_rail.qualification.evidence import required_output_roles
    from c1_rail.qualification.policy import parse_policy
    from c1_rail.qualification.policy_sources import build_qualification_policy

    policy = parse_policy(build_qualification_policy())
    order = tuple(json.loads(policy.canonical_bytes)['stage_order'])
    roles = required_output_roles(
        policy, stages=order[:4], completion='PARTIAL', verdict='NONE'
    )
    assert roles == tuple(
        sorted(
            json.loads(policy.canonical_bytes)['base_artifact_roles']
            + [
                json.loads(policy.canonical_bytes)['stage_artifact_roles'][stage]
                for stage in order[:4]
            ]
        )
    )
    legacy = dict(
        json.loads(policy.canonical_bytes),
        policy_id='tradeify-e1-pristine/v1',
    )
    legacy.pop('joint_continuation')
    with pytest.raises(ValueError, match='POLICY_SCHEMA_MISMATCH'):
        parse_policy(encoded(legacy))


def test_n2_work_start_claim_is_live_from_n2_ready(tmp_path, monkeypatch):
    """The launch's START_CLIENT control claim (campaign_supervisor._control)
    for a reserved N2 work runs from N2_READY, the progression state S4 opens;
    it must see the campaign as live exactly as the reservation and launch gate
    do, not as a terminal budget. The Linux joint cases refused here ('terminal
    campaign budget') once the N1 G5 settlement wait let them reach the launch."""
    instance = committed_n1(tmp_path, monkeypatch)
    materialized(instance, schedule_document(instance, role='n2_worker', work='n2work'))
    assert snap(instance)['state'] == 'N2_READY'
    store(instance).claim_supervision_control(
        instance.attempt, 'n2work', 'START_CLIENT', supervisor.observe_campaign_clock()
    )


def test_n1_work_start_claim_stays_refused_from_n2_ready(tmp_path, monkeypatch):
    """The progression allowance is phase-scoped: a phase outside the state's
    PROGRESSION_PHASES still meets the terminal-budget refusal."""
    instance = committed_n1(tmp_path, monkeypatch)
    with pytest.raises(ValueError, match='terminal campaign budget'):
        store(instance).claim_supervision_control(
            instance.attempt, 'g5work', 'START_CLIENT', supervisor.observe_campaign_clock()
        )


# ---- The N2 guardian fix regressions (S4-R1b) ---------------------------------
#
# Ported from the HEAD-vs-patched scratch pair in .cache/n2fix-reference to run
# once against the real supervisor: the N2 guardians' dispatch-ack wait and
# authority check treat N2_READY as live for their own phases, the n2 dispatch
# roles get the campaign-control task bound, the N2 worker container runs as the
# worker uid, the N2 compute work completes after its settlement, the N2 g5 unit
# is supervised/resumed, and the signing-retry finalize reaches the N2 commit --
# with the N1 g5 commit detection unchanged.

WORKER_UID = 65532


def _supervision_context():
    """The supervisor's own context surface for a container-body derivation."""
    return SimpleNamespace(
        config={'g5_uid': G5, 'seal_probe_uid': OPERATOR},
        profile=SimpleNamespace(
            worker_uid=WORKER_UID,
            pids_limit=64,
            memory_bytes=256000000,
            scratch_bytes=10000000,
        ),
        release=encoded({'worker_image_digest': 'sha256:' + '0' * 64}),
    )


def _enrollment(work_id='n2work'):
    """A real enrolled scope family over the installed host/attempt identity."""
    return {
        'schema': 'qualification_campaign_supervision/v1',
        'host_run_id': 'host1',
        'attempt_id': 'a1',
        'work_id': work_id,
        'manifest_bytes_b64': '',
        'scopes': supervisor.work_enrollment('host1', 'a1', work_id),
    }


def test_n2_guardian_dispatch_ack_and_authority_are_live_from_n2_ready(
    tmp_path, monkeypatch
):
    """The N2 guardian's own wait and authority check against the real journal:
    a dispatched N2 work acknowledges and returns live from N2_READY, phase
    scoped -- a foreign phase and a phase-less check still refuse."""
    instance = committed_n1(tmp_path, monkeypatch)
    materialized(instance, schedule_document(instance, role='n2_worker', work='n2work'))
    campaigns = store(instance)
    with campaigns.launch_gate(
        instance.attempt, 'n2work', supervisor.observe_campaign_clock, role='guardian'
    ) as permit:
        pass
    campaigns.acknowledge_dispatch(
        instance.attempt, 'n2work', 'guardian', permit['token'], supervisor.observe_campaign_clock
    )
    state = supervisor._await_dispatch_ack(campaigns, instance.attempt, 'n2work', 10**18)
    assert state['state'] == 'N2_READY'
    supervisor._assert_authority(state, 'N2')
    with pytest.raises(ValueError, match='campaign is terminal or invalidated'):
        supervisor._assert_authority(state, 'N1_G5')
    with pytest.raises(ValueError, match='campaign is terminal or invalidated'):
        supervisor._assert_authority(state)


def test_n2_dispatch_roles_get_the_campaign_control_task_bound():
    """Every dispatch-work guardian spawns its own campaign_control children, n2
    included; harmless probes and the admission stay single-task."""
    roles = ('n1_worker', 'n1_g5', 'n2_worker', 'n2_g5', 'probe_worker', 'admission')
    bound = {role: supervisor.guardian_task_bound({'role': role}) for role in roles}
    control = 1 + supervisor.CAMPAIGN_CONTROL_TASKS
    assert bound == {
        'n1_worker': control,
        'n1_g5': control,
        'n2_worker': control,
        'n2_g5': control,
        'probe_worker': 1,
        'admission': 1,
    }
    assert {'n2_worker', 'n2_g5'} <= set(DISPATCH_ROLES)


def test_n2_worker_container_body_has_the_worker_uid():
    """The joint worker's container body carries the worker uid entry (the probe
    body's fixed role map) and the N2 checkpoint argument."""
    manifest = {'work_id': 'n2work', 'role': 'n2_worker', 'probe': 'noop'}
    body = supervisor.worker_container_body(
        _supervision_context(), _enrollment(), manifest, checkpoint='N2'
    )
    assert body['User'] == str(WORKER_UID) + ':' + str(WORKER_UID)
    assert body['Cmd'][-2:] == ['--checkpoint', 'N2']
    assert body['Labels']['fp.s2.role'] == 'n2_worker'


class _WorkerCampaigns:
    """The store surface ``_run_n1_worker`` uses, over a frozen progression."""

    def __init__(self, progression):
        self.progression = progression
        self.transitions = []
        self.events = []

    def state(self):
        return {
            'attempt_id': 'a1',
            'state': self.progression,
            'validity': 'VALID',
            'authority_revision': 3,
            'profile': {'orchestration_cpu_ns': {'N2': 20 * 10**9}},
            'works': [
                {
                    'work_id': 'n2work',
                    'phase': 'N2',
                    'state': 'RUNNING',
                    'limits': {
                        'cpu_ns': 120 * 10**9,
                        'wall_ns': 300 * 10**9,
                        'memory_bytes': 256000000,
                    },
                }
            ],
        }

    def budget_snapshot(self, attempt):
        return encoded(self.state())

    def _work(self, state, work_id):
        return next(work for work in state['works'] if work['work_id'] == work_id)

    @contextmanager
    def launch_gate(self, *args, **kwargs):
        yield {'token': b'x' * 32}

    def acknowledge_dispatch(self, *args, **kwargs):
        pass

    def retain_supervision_event(self, raw):
        self.events.append(json.loads(raw)['kind'])

    def row(self, attempt):
        return {'request_bytes': encoded({'bundle_sha256': 'b' * 64}), 'campaign_id': 'c1'}

    def retain_checkpoint_capture(self, *args, **kwargs):
        pass

    def retain_checkpoint_attestation(self, *args, **kwargs):
        pass

    def settle_work(self, attempt, work_id, observed):
        return encoded(self.state())

    def record_work_transition(self, attempt, work_id, raw, expected_revision):
        self.transitions.append(json.loads(raw)['state'])
        return encoded(self.state())


class _WorkerDocker:
    """One fixed container: created, inspected, seen running once, then exit 0."""

    def __init__(self, body):
        self.body = body
        self.polls = 0

    def call(self, method, path, body=None, raw=False):
        if path == '/info':
            return {'CgroupDriver': 'systemd'}
        if path.startswith('/containers/create'):
            return {'Id': 'c' * 64}
        if path.endswith('/json'):
            self.polls += 1
            running = self.polls == 2
            return {
                'Image': self.body['Image'],
                'Config': {key: self.body[key] for key in ('User', 'Entrypoint', 'Cmd')},
                'HostConfig': {
                    'CgroupParent': self.body['HostConfig']['CgroupParent'],
                    'Binds': self.body['HostConfig']['Binds'],
                },
                'State': {
                    'Running': running,
                    'Pid': 4242 if running else 0,
                    'ExitCode': 0,
                    'OOMKilled': False,
                    'StartedAt': '2026-09-23T00:00:01Z',
                    'FinishedAt': '2026-09-23T00:00:02Z',
                },
            }
        return {}


@pytest.mark.parametrize(
    'progression,completed',
    [('N2_READY', ['COMPLETED']), ('BUDGET_EXHAUSTED', [])],
    ids=['N2_READY', 'BUDGET_EXHAUSTED'],
)
def test_n2_compute_work_completes_in_n2_ready_after_settlement(
    tmp_path, monkeypatch, progression, completed
):
    """The joint compute work's COMPLETED gate follows its settlement: live for
    its own N2 phase in N2_READY (the state the N1 commit produced), refused
    once the campaign budget is terminal."""
    from c1_rail.qualification.execution import files, protocol, signing

    enrollment = _enrollment()
    payload_slice = enrollment['scopes']['payload_slice']
    body = {
        'Image': 'img',
        'User': str(WORKER_UID) + ':' + str(WORKER_UID),
        'Entrypoint': ['e'],
        'Cmd': ['c'],
        'HostConfig': {'CgroupParent': payload_slice, 'Binds': ['a:/input:ro']},
    }
    docker = _WorkerDocker(body)
    clock_bytes = encoded(
        {
            'schema': 'qualification_campaign_clock/v1',
            'boot_id': 'b',
            'boottime_ns': 10**12,
            'utc': '2026-09-23T00:00:00Z',
        }
    )
    monkeypatch.setattr(supervisor, 'observe_campaign_clock', lambda: clock_bytes)
    monkeypatch.setattr(supervisor, 'DockerControl', lambda: docker)
    monkeypatch.setattr(supervisor, '_worker_input_files', lambda *a, **k: ([], b'plan'))
    monkeypatch.setattr(supervisor, '_guardian_bus_call', lambda *a, **k: None)
    monkeypatch.setattr(supervisor, '_write_worker_input', lambda *a, **k: 0)
    monkeypatch.setattr(supervisor, 'worker_container_body', lambda *a, **k: body)
    monkeypatch.setattr(
        supervisor, '_process_cgroup', lambda pid='self': '/' + payload_slice + '/c'
    )
    monkeypatch.setattr(supervisor, '_payload_processes', lambda group: ['4242'])
    monkeypatch.setattr(
        supervisor,
        '_process_identity',
        lambda pid: (99, WORKER_UID, '/' + payload_slice + '/c', 'python3', '/x'),
    )
    monkeypatch.setattr(supervisor, '_pre_exec_init', lambda comm: False)
    monkeypatch.setattr(supervisor, '_interpreter_image', lambda *a: False)
    monkeypatch.setattr(
        supervisor,
        '_read_counter',
        lambda path: (b'usage_usec 0\n' if path.name == 'cpu.stat' else b'oom 0\noom_kill 0\n'),
    )
    monkeypatch.setattr(supervisor.time, 'sleep', lambda seconds: None)
    monkeypatch.setattr(files, 'read_regular', lambda *a, **k: b'frame')
    monkeypatch.setattr(protocol, 'decode_frame', lambda raw, limit: b'payload')
    result = encoded(
        {
            'payload_sha256': 'p' * 64,
            'payload_byte_length': 7,
            'plan_sha256': 'q' * 64,
            'worker_image_digest': 'img',
            'runtime_manifest_sha256': 'r' * 64,
            'container_id': 'c' * 64,
        }
    )
    monkeypatch.setattr(
        supervisor,
        '_capture_result_document',
        lambda *a, **k: (result, SimpleNamespace(document={'observations': {}})),
    )
    monkeypatch.setattr(signing, 'sign_checkpoint_attestation', lambda *a, **k: b'attestation')
    verified = SimpleNamespace(profile=SimpleNamespace(sha256='s' * 64))
    context = SimpleNamespace(
        profile=SimpleNamespace(output_byte_limit=10**7, worker_uid=WORKER_UID),
        config={'execution_credential': 'cred', 'service_uid': SERVICE_UID},
        release=encoded({'service_id': 'svc'}),
        keys=lambda: {},
        _context=lambda digest, at: verified,
    )
    runtime = SimpleNamespace(
        parent=tmp_path / (payload_slice[:-6].split('-')[0] + '.slice'),
        observation=lambda *a: b'{}',
    )
    campaigns = _WorkerCampaigns(progression)
    state = campaigns.state()
    supervisor._run_n1_worker(
        context,
        campaigns,
        runtime,
        state,
        state['works'][0],
        enrollment,
        {'work_id': 'n2work', 'role': 'n2_worker'},
        checkpoint='N2',
    )
    assert 'PROCESS' in campaigns.events and 'PAYLOAD_EXIT' in campaigns.events
    assert campaigns.transitions == completed


def _run_g5_work(tmp_path, monkeypatch, *, progression, parent=None, procs='', checkpoint='N2'):
    """Drive ``_run_n1_g5`` over the g5 settlement kernel and store fakes.

    ``parent`` names a signing retry's parent work, so the persisted candidate
    exists and the caller-finalizes-after-retry tail runs.
    """
    from pathlib import PurePosixPath

    from c1_rail.qualification.execution import runtime as runtime_module
    from test_g5_settlement_wait import (
        LINUX_CODE_ROOT,
        LINUX_INTERPRETER,
        PAYLOAD_SLICE,
        START_NS,
        WALL_NS,
        Kernel,
    )

    phase = checkpoint + '_G5'
    parent_path = tmp_path / 'fpq.slice'
    kernel = Kernel(parent_path, exit_after=3)
    (kernel.group / 'cgroup.procs').write_text(procs)
    events, signals, commits, transitions = [], [], [], []
    candidate = encoded(
        {'artifacts': [{'role': 'n2_result', 'sha256': 'a' * 64, 'byte_length': 1}]}
    )

    class Campaigns:
        def state(self):
            return {
                'attempt_id': 'att1',
                'state': progression,
                'validity': 'VALID',
                'authority_revision': 7,
                'works': [],
            }

        def budget_snapshot(self, attempt_id):
            return encoded(self.state())

        @contextmanager
        def launch_gate(self, *args, **kwargs):
            yield {'token': 'tok'}

        def acknowledge_dispatch(self, *args):
            pass

        def _work(self, state, work_id):
            return {
                'work_id': work_id,
                'phase': phase,
                'state': 'RUNNING' if parent else 'SIGNED',
            }

        def _retry_parent(self, work):
            return parent

        def settle_work(self, attempt_id, work_id, observed):
            return encoded(self.state())

        def record_work_transition(self, attempt_id, work_id, raw, expected_revision):
            transitions.append(json.loads(raw)['state'])
            return encoded(self.state())

        def retain_supervision_event(self, raw):
            events.append(json.loads(raw)['kind'])

    class IntentStore:
        @contextmanager
        def transaction(self):
            yield SimpleNamespace(
                execute=lambda *a: SimpleNamespace(
                    fetchone=lambda: (candidate,) if parent else None
                )
            )

    class Runtime:
        def __init__(self):
            self.parent = parent_path

        def observation(self, state, work, enrollment):
            return b'{}'

    monkeypatch.setattr(supervisor, 'observe_campaign_clock', kernel.clock)
    monkeypatch.setattr(supervisor.time, 'sleep', kernel.sleep)
    monkeypatch.setattr(supervisor, '_guardian_bus_call', lambda *a: None)
    monkeypatch.setattr(supervisor.sys, 'executable', LINUX_INTERPRETER)
    monkeypatch.setattr(
        runtime_module, 'installed_code_root', lambda: PurePosixPath(LINUX_CODE_ROOT)
    )
    monkeypatch.setattr(
        supervisor,
        '_process_identity',
        lambda pid: (
            99,
            G5,
            '/fpq.slice/' + PAYLOAD_SLICE + '/unit',
            supervisor.READINESS_TOKEN,
            LINUX_INTERPRETER,
        ),
    )
    monkeypatch.setattr(supervisor, '_interpreter_image', lambda *a: True)
    monkeypatch.setattr(supervisor, '_signal_state', lambda pid: (1, 512, 512))
    monkeypatch.setattr(
        supervisor, '_guardian_signal_unit', lambda unit, name: signals.append(name)
    )
    reservation = base64.b64encode(encoded({'clock': json.loads(kernel.clock())})).decode()
    state = {
        'attempt_id': 'att1',
        'deadline_boottime_ns': START_NS + WALL_NS,
        'profile': {'orchestration_cpu_ns': {phase: 10**9}},
    }
    work = {
        'work_id': 'n2g5retry' if parent else 'n2g5',
        'phase': phase,
        'reservation_bytes_b64': reservation,
        'limits': {'cpu_ns': 30 * 10**9, 'wall_ns': WALL_NS},
    }
    enrollment = {
        'scopes': {'payload_slice': PAYLOAD_SLICE, 'guardian_unit': 'fpq-guardian.service'}
    }
    context = SimpleNamespace(
        config={'g5_uid': G5},
        store=IntentStore(),
        _commit_checkpoint=lambda campaigns, attempt, request: commits.append(request),
    )
    supervisor._run_n1_g5(
        context,
        Campaigns(),
        Runtime(),
        state,
        work,
        enrollment,
        manifest={},
        checkpoint=checkpoint,
    )
    return events, signals, commits, transitions


def test_n2_g5_unit_is_supervised_and_resumed_from_n2_ready(tmp_path, monkeypatch):
    """The N2 g5 unit is supervised from N2_READY: its identity is retained
    (PROCESS) and the readiness handshake sends the resume signal (SIGUSR1)."""
    events, signals, _, _ = _run_g5_work(
        tmp_path, monkeypatch, progression='N2_READY', procs='4242'
    )
    assert 'PROCESS' in events and 'RESUMED' in events
    assert signals[:1] == ['SIGUSR1']


def test_n2_signing_retry_finalizes_the_n2_commit(tmp_path, monkeypatch):
    """The redelivered N2 signing retry settles, completes, and finalizes the
    interrupted signing from N2_READY through the service's own commit path:
    the N2 checkpoint and its parent work, never the N1 pair."""
    _, _, commits, transitions = _run_g5_work(
        tmp_path, monkeypatch, progression='N2_READY', parent='n2g5'
    )
    assert transitions == ['COMPLETED']
    assert len(commits) == 1
    assert commits[0]['checkpoint'] == 'N2' and commits[0]['work_id'] == 'n2g5'


@pytest.mark.parametrize('progression,supervised', [('N2_READY', False), ('BOUND', True)])
def test_n1_g5_commit_detection_unchanged_by_the_n2_fix(
    tmp_path, monkeypatch, progression, supervised
):
    """Guard: an N1 g5 in N2_READY is still its own commit's progression (its
    unit is no longer supervised), and from BOUND it is still supervised and
    resumed."""
    events, signals, _, _ = _run_g5_work(
        tmp_path, monkeypatch, progression=progression, procs='4242', checkpoint='N1'
    )
    assert ('PROCESS' in events) is supervised
    assert bool(signals) is supervised
