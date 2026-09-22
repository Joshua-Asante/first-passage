"""S3 genuine N1 capture and committed G5 decision: real SQLite journals, real
admitted campaigns and plans; simulated trusted clocks/identities. No Linux
enforcement is claimed here -- the host-side cases live in
tests/integration/qualification_boundary/test_campaign_n1_linux.py.
"""

import base64
import json
import threading
from contextlib import nullcontext
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest
from bundle_fixture import build_bundle
from test_campaign_admission import running
from test_contract import NOW
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution import campaign_funding as funding
from c1_rail.qualification.execution import campaign_supervisor as supervisor
from c1_rail.qualification.execution.campaign_store import CampaignStore
from c1_rail.qualification.execution.plan import derive_campaign_plan_from_context
from c1_rail.qualification.execution.protocol import sha256
from c1_rail.qualification.execution.service import ExecutionService
from c1_rail.qualification.execution.store import ExecutionStore

CLIENT, G5, OPERATOR, SERVICE_UID = 1001, 1002, 1003, 1004
ADMISSION_CHARGE = 20_000_000_000


class Runtime:
    started = []

    def __init__(self, context):
        Runtime.started.append('guardian')

    def start(self, state, work, enrollment):
        pass


def campaign(tmp_path, monkeypatch, *, t=11):
    """A warm dispatch-capable service (release/v5, budget profile/v3) with a
    fully admitted campaign: real bundle, real plan, retained receipt."""
    instance, case = running(tmp_path, monkeypatch, dispatch=True)
    instance.config = {'host_run_id': 'host1', 'service_uid': SERVICE_UID}
    instance.recovery_issues = {}
    instance.schedule_eligible = True
    instance.dispatch_eligible = True
    monkeypatch.setattr(supervisor, 'controller_cpu_guard', nullcontext)
    monkeypatch.setattr(supervisor, 'LinuxCampaignRuntime', Runtime)
    state = {'t': t}
    monkeypatch.setattr(supervisor, 'observe_campaign_clock', lambda: encoded(clock(state)))
    instance.clocks = state
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
    return instance, case


def clock(state):
    return {
        'schema': 'qualification_campaign_clock/v1',
        'boot_id': 'boot-1',
        'boottime_ns': state['t'],
        'utc': '2026-09-21T00:00:00Z',
    }


def submit(instance, case):
    raw = encoded(
        {
            'schema': 'qualification_campaign_request/v2',
            'operation': 'SUBMIT_E1',
            'attempt_id': case['attempt_id'],
            'bundle_sha256': sha256(case['index']),
            'request_id': 'dispatch-1',
        }
    )
    first = json.loads(instance.handle_request(CLIENT, raw))
    assert first['state'] == 'METERED_INSPECTION_REQUIRED' or first['receipt'] is None
    return raw


def verified_context(instance, case):
    from c1_rail.qualification.execution.admission import verify_bundle

    return verify_bundle(
        instance.root / 'bundles' / sha256(case['index']), case['release'], case['keys'], NOW
    )


def admission_observation(case, state):
    scopes = supervisor.work_enrollment('host1', case['attempt_id'], 'admission')
    return encoded(
        {
            'schema': 'qualification_campaign_observation/v2',
            'attempt_id': case['attempt_id'],
            'work_id': 'admission',
            'clock': clock(state),
            'campaign_scope_id': scopes['campaign_slice'],
            'work_scope_id': scopes['payload_slice'],
            'cpu_ns': 0,
            'memory_peak_bytes': 0,
            'oom_events': 0,
            'termination_known': True,
            'orchestration_charge_cpu_ns': ADMISSION_CHARGE,
        }
    )


def store(instance):
    return CampaignStore(instance.store)


def snap(instance):
    attempt = instance.attempt
    return json.loads(store(instance).budget_snapshot(attempt))


def schedule_document(instance, role='n1_worker', work='n1work', probe='noop', fault=None):
    return encoded(
        {
            'schema': 'qualification_campaign_schedule_request/v1',
            'attempt_id': instance.attempt,
            'work_id': work,
            'role': role,
            'probe': probe,
            'signing_retry_of': None,
            'fault': fault,
        }
    )


def claim(instance, raw=None):
    return store(instance).claim_scheduler_bootstrap(
        raw or schedule_document(instance), supervisor.observe_campaign_clock()
    )


def materialized(instance, raw=None):
    token, status = claim(instance, raw)
    assert token is not None, 'claim refused: ' + json.loads(
        status.decode() if isinstance(status, bytes) else status
    ).get('state', '?')
    document = funding.parse_request(raw or schedule_document(instance))
    return store(instance).materialize_scheduler_bootstrap(
        instance.attempt, document['work_id'], token, 'host1'
    )


def transition(instance, work, state, data=None):
    return store(instance).record_work_transition(
        instance.attempt,
        work,
        encoded(
            {
                'schema': 'qualification_campaign_work_transition/v1',
                'attempt_id': instance.attempt,
                'work_id': work,
                'state': state,
                'clock': json.loads(supervisor.observe_campaign_clock()),
                'data': data or {},
            }
        ),
        expected_revision=snap(instance)['authority_revision'],
    )


def settle(instance, work, cpu=20):
    scopes = supervisor.work_enrollment('host1', instance.attempt, work)
    profile = snap(instance)['profile']
    observation = encoded(
        {
            'schema': 'qualification_campaign_observation/v2',
            'attempt_id': instance.attempt,
            'work_id': work,
            'clock': json.loads(supervisor.observe_campaign_clock()),
            'campaign_scope_id': scopes['campaign_slice'],
            'work_scope_id': scopes['payload_slice'],
            'cpu_ns': cpu,
            'memory_peak_bytes': 50,
            'oom_events': 0,
            'termination_known': True,
            'orchestration_charge_cpu_ns': profile['orchestration_cpu_ns'][
                next(w['phase'] for w in snap(instance)['works'] if w['work_id'] == work)
            ],
        }
    )
    return store(instance).settle_work(instance.attempt, work, observation)


def retained_identity(instance, work):
    """S2-G5 R1: a retained alive-verified identity inside the enrolled slice."""
    scopes = supervisor.work_enrollment('host1', instance.attempt, work)
    event = encoded(
        {
            'schema': 'qualification_campaign_supervision_event/v2',
            'attempt_id': instance.attempt,
            'work_id': work,
            'kind': 'PROCESS',
            'clock': json.loads(supervisor.observe_campaign_clock()),
            'data': {
                'pid': 4242,
                'start_ticks': 99,
                'uid': 7,
                'cgroup': '/fpq/' + scopes['payload_slice'] + '/payload-scope',
                'comm': 'fpq-armed',
                'exe': '',
            },
        }
    )
    store(instance).retain_supervision_event(event)


def dispatched(instance, work):
    campaigns = store(instance)
    with campaigns.launch_gate(
        instance.attempt, work, supervisor.observe_campaign_clock, role='payload'
    ) as permit:
        pass
    campaigns.acknowledge_dispatch(
        instance.attempt, work, 'payload', permit['token'], supervisor.observe_campaign_clock
    )


def n1_plan(instance):
    from c1_rail.qualification.checkpoint_plan import derive_checkpoint_plan

    return derive_checkpoint_plan(
        store(instance).retained_object(instance.attempt, 'plan'), 'N1', None
    )


def result_document(instance, work='n1work', payload=b'archived-worker-frame'):
    scopes = supervisor.work_enrollment('host1', instance.attempt, work)
    state = snap(instance)
    return encoded(
        {
            'schema': 'qualification_campaign_checkpoint_result/v1',
            'attempt_id': instance.attempt,
            'checkpoint': 'N1',
            'work_id': work,
            'campaign_id': 'campaign-1',
            'plan_sha256': sha256(n1_plan(instance)),
            'plan_byte_length': len(n1_plan(instance)),
            'payload_sha256': sha256(payload),
            'payload_byte_length': len(payload),
            'worker_execution_id': work,
            'container_id': '9' * 64,
            'worker_image_digest': 'sha256:' + '8' * 64,
            'runtime_manifest_sha256': '7' * 64,
            'capture': {
                'exit_code': 0,
                'oom_killed': False,
                'started_utc': '2026-09-21T00:00:01Z',
                'completed_utc': '2026-09-21T00:00:02Z',
                'authorized_at_utc': '2026-09-21T00:00:00Z',
                'campaign_scope_id': scopes['campaign_slice'],
                'work_scope_id': scopes['payload_slice'],
                'payload_slice': scopes['payload_slice'],
            },
            'limits': {
                'cpu_ns': state['profile']['phases']['N1']['cpu_ns'],
                'wall_ns': state['profile']['phases']['N1']['wall_ns'],
                'memory_bytes': state['profile']['phases']['N1']['memory_bytes'],
                'orchestration_cpu_ns': state['profile']['orchestration_cpu_ns']['N1'],
            },
            'observations': {
                'exit_code': 0,
                'oom_killed': False,
                'worker_compute_wall_ns': 1,
                'worker_cpu_ns': 1,
                'worker_peak_memory_bytes': 1,
            },
            'created_utc': '2026-09-21T00:00:03Z',
        }
    )


def enrolled_capture(tmp_path, monkeypatch):
    """The N1 worker scene: dispatched, identity-retained, captured, attested."""
    instance, case = campaign(tmp_path, monkeypatch)
    materialized(instance)
    retained_identity(instance, 'n1work')
    transition(instance, 'n1work', 'RUNNING')
    dispatched(instance, 'n1work')
    payload = b'archived-worker-frame'
    result = result_document(instance, payload=payload)
    capture_transition = encoded(
        {
            'schema': 'qualification_campaign_work_transition/v1',
            'attempt_id': instance.attempt,
            'work_id': 'n1work',
            'state': 'CAPTURED',
            'clock': json.loads(supervisor.observe_campaign_clock()),
            'data': {'capture_bytes_b64': base64.b64encode(result).decode('ascii')},
        }
    )
    store(instance).retain_checkpoint_capture(
        instance.attempt, 'n1work', result, payload, capture_transition
    )
    attestation = attestation_document(instance, result, payload)
    store(instance).retain_checkpoint_attestation(
        instance.attempt, attestation, verify=lambda *args, **kwargs: None
    )
    return instance, result, payload, attestation


def attestation_document(instance, result, payload):
    parsed = json.loads(result)
    release = json.loads(instance.release)
    return encoded(
        {
            'schema': 'qualification_campaign_checkpoint_attestation/v1',
            'payload': {
                'schema': 'qualification_campaign_checkpoint_attestation_payload/v1',
                'scope': 'ATTEST_CAMPAIGN_CHECKPOINT',
                'attempt_id': instance.attempt,
                'checkpoint': 'N1',
                'work_id': 'n1work',
                'result_sha256': sha256(result),
                'payload_sha256': sha256(payload),
                'payload_byte_length': len(payload),
                'plan_sha256': parsed['plan_sha256'],
                'execution_release_sha256': sha256(instance.release),
                'profile_sha256': instance.profile.sha256,
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
                'observations': {'exit_code': 0, 'oom_killed': False},
                'authorized_at_utc': '2026-09-21T00:00:00Z',
                'started_utc': '2026-09-21T00:00:01Z',
                'completed_utc': '2026-09-21T00:00:02Z',
                'campaign_revision': 2,
            },
            'signature': {
                'algorithm': 'Ed25519',
                'key_id': 'test-execution',
                'value_b64': base64.b64encode(b's' * 64).decode(),
            },
        }
    )


def g5_claimed(tmp_path, monkeypatch):
    instance, result, payload, attestation = enrolled_capture(tmp_path, monkeypatch)
    settle(instance, 'n1work')
    transition(instance, 'n1work', 'COMPLETED')
    materialized(instance, schedule_document(instance, role='n1_g5', work='g5work'))
    retained_identity(instance, 'g5work')
    transition(instance, 'g5work', 'RUNNING')
    dispatched(instance, 'g5work')
    return instance


def candidate_document(instance, decision='CONTINUE', revision=None):
    raw = store(instance).checkpoint_snapshot(instance.attempt)
    snapshot = json.loads(raw)
    capture = snapshot['capture']
    return encoded(
        {
            'schema': 'qualification_campaign_checkpoint_assessment/v1',
            'attempt_id': instance.attempt,
            'checkpoint': 'N1',
            'work_id': 'n1work',
            'binding': {
                'contract_sha256': '1' * 64,
                'trust_domain_sha256': '2' * 64,
                'policy_sha256': '5' * 64,
                'execution_release_sha256': '3' * 64,
            },
            'snapshot': {
                'campaign_revision': revision or snapshot['campaign_revision'],
                'authority_head': snapshot['authority_head'],
                'snapshot_sha256': sha256(raw),
            },
            'capture': {
                'result_sha256': capture['result_sha256'],
                'payload_sha256': capture['payload_sha256'],
                'attestation_sha256': capture['attestation_sha256'],
            },
            'stages': [
                {
                    'stage': 'LEGALITY',
                    'status': 'PASS',
                    'input_sha256': 'b' * 64,
                    'output_sha256': 'c' * 64,
                    'population_counts': {},
                },
                {
                    'stage': 'N1',
                    'status': 'FAIL' if decision == 'FAILURE' else 'PASS',
                    'input_sha256': 'd' * 64,
                    'output_sha256': 'e' * 64,
                    'population_counts': {'FULL': 2, 'H1': 2, 'H2': 2},
                },
            ],
            'decision': decision,
            'n1_decision': 'FAIL' if decision == 'FAILURE' else 'PASS',
            'cutoff': {'checkpoint': 'N1', 'n1_cutoffs': {'FULL': 0, 'H1': 0, 'H2': 0}},
            'n2_thresholds': {
                'bound_to': '1' * 64,
                'stages': [{'stage': 'N2', 'exact_depth': 2, 'max_failures_per_population': 0}],
            },
            'artifacts': [{'role': 'attempt_journal', 'sha256': 'f' * 64, 'byte_length': 10}],
            'signature': {
                'algorithm': 'Ed25519',
                'key_id': 'test-producer',
                'value_b64': base64.b64encode(b'x' * 64).decode(),
            },
        }
    )


def persisted_intent(instance, candidate=None):
    candidate = candidate or candidate_document(instance)
    campaigns = store(instance)
    snapshot = campaigns.checkpoint_snapshot(instance.attempt)
    intent = encoded(
        {
            'schema': 'qualification_campaign_checkpoint_intent/v1',
            'attempt_id': instance.attempt,
            'checkpoint': 'N1',
            'work_id': 'g5work',
            'key_id': 'test-producer',
            'signing_at_utc': '2026-09-21T01:00:00Z',
            'candidate_sha256': sha256(candidate),
            'snapshot_sha256': sha256(snapshot),
        }
    )
    capture = encoded(
        {
            'schema': 'qualification_campaign_g5_capture/v1',
            'attempt_id': instance.attempt,
            'checkpoint': 'N1',
            'work_id': 'g5work',
            'candidate_sha256': sha256(candidate),
            'staged': [],
        }
    )
    capture_transition = encoded(
        {
            'schema': 'qualification_campaign_work_transition/v1',
            'attempt_id': instance.attempt,
            'work_id': 'g5work',
            'state': 'CAPTURED',
            'clock': json.loads(supervisor.observe_campaign_clock()),
            'data': {'capture_bytes_b64': base64.b64encode(capture).decode('ascii')},
        }
    )
    signing_transition = encoded(
        {
            'schema': 'qualification_campaign_work_transition/v1',
            'attempt_id': instance.attempt,
            'work_id': 'g5work',
            'state': 'SIGNING_INTENT',
            'clock': json.loads(supervisor.observe_campaign_clock()),
            'data': {
                'intent_id': 'g5work-intent',
                'payload_bytes_b64': base64.b64encode(candidate).decode('ascii'),
                'key_id': 'test-producer',
                'signing_at_utc': '2026-09-21T01:00:00Z',
            },
        }
    )
    campaigns.persist_checkpoint_intent(
        instance.attempt,
        'g5work',
        snapshot,
        intent,
        candidate,
        capture_transition,
        signing_transition,
    )
    return candidate


def cutoff_document(instance, candidate):
    return encoded(
        {
            'schema': 'qualification_campaign_cutoff_receipt/v1',
            'attempt_id': instance.attempt,
            'checkpoint': 'N1',
            'assessment_sha256': sha256(candidate),
            'decision': json.loads(candidate)['decision'],
            'n1_cutoffs': {'FULL': 0, 'H1': 0, 'H2': 0},
            'n2_thresholds': [{'stage': 'N2', 'exact_depth': 2, 'max_failures_per_population': 0}],
            'n2_bound_to': sha256(candidate),
            'created_utc': '2026-09-21T02:00:00Z',
        }
    )


def commit(instance, candidate, cutoff=None):
    cutoff = cutoff or cutoff_document(instance, candidate)
    return store(instance).commit_checkpoint_assessment(
        instance.attempt,
        'g5work',
        candidate,
        cutoff,
        now=datetime(2026, 9, 21, tzinfo=timezone.utc),
        clock_bytes=supervisor.observe_campaign_clock(),
    )


def test_dispatch_roles_require_completed_admission_and_noop_probe(tmp_path, monkeypatch):
    instance, case = campaign(tmp_path, monkeypatch)
    # An admitted campaign with its receipt removed loses dispatch eligibility.
    with instance.store.transaction() as connection:
        connection.execute(
            "DELETE FROM full_campaign_objects WHERE attempt_id=? AND role='diagnostic_receipt'",
            (instance.attempt,),
        )
    with pytest.raises(ValueError, match='completed campaign admission required'):
        claim(instance)
    # A fresh campaign with the receipt retains it: the claim funds the work.
    instance2, case2 = campaign(tmp_path / 'second', monkeypatch)
    token, _ = claim(instance2)
    assert token is not None
    document = funding.parse_request(schedule_document(instance2))
    store(instance2).materialize_scheduler_bootstrap(
        instance2.attempt, document['work_id'], token, 'host1'
    )
    with pytest.raises(ValueError, match='compute phase already reserved'):
        claim(instance2, schedule_document(instance2, work='n1work2'))
    with pytest.raises(ValueError, match='fixed noop probe'):
        claim(instance2, schedule_document(instance2, role='n1_g5', work='g5work', probe='cpu'))


def test_capture_retains_bytes_and_migrates_the_v6_family(tmp_path, monkeypatch):
    instance, result, payload, attestation = enrolled_capture(tmp_path, monkeypatch)
    state = snap(instance)
    assert state['schema'] == 'qualification_campaign_budget_snapshot/v6'
    family = state['checkpoints']['N1']
    assert family['state'] == 'ATTESTED' and family['work_id'] == 'n1work'
    assert family['payload_sha256'] == sha256(payload)
    assert family['attestation_sha256'] == sha256(attestation)
    reopened = CampaignStore(ExecutionStore(instance.store.path))
    assert json.loads(reopened.budget_snapshot(instance.attempt)) == state
    assert reopened.checkpoint_capture(instance.attempt)['payload_bytes'] == payload
    import re as _re

    with pytest.raises(
        ValueError,
        match=_re.compile('immutable checkpoint capture differs|archived payload differs'),
    ):
        reopened.retain_checkpoint_capture(
            instance.attempt,
            'n1work',
            result,
            b'substituted',
            encoded(
                {
                    'schema': 'qualification_campaign_work_transition/v1',
                    'attempt_id': instance.attempt,
                    'work_id': 'n1work',
                    'state': 'CAPTURED',
                    'clock': json.loads(supervisor.observe_campaign_clock()),
                    'data': {'capture_bytes_b64': base64.b64encode(result).decode('ascii')},
                }
            ),
        )


def test_snapshot_serves_members_and_bounded_chunks(tmp_path, monkeypatch):
    instance, result, payload, attestation = enrolled_capture(tmp_path, monkeypatch)
    snapshot = json.loads(store(instance).checkpoint_snapshot(instance.attempt))
    members = {row['role']: row['sha256'] for row in snapshot['members']}
    assert {'plan', 'result', 'payload', 'attestation', 'retained_bundle_index'} <= set(members)
    assert sha256(n1_plan(instance)) == members['plan']
    whole = json.loads(
        store(instance).fetch_checkpoint_member(
            instance.attempt, members['payload'], 0, 1024 * 1024
        )
    )
    assert whole['total_byte_length'] == len(payload)
    part = json.loads(
        store(instance).fetch_checkpoint_member(instance.attempt, members['payload'], 2, 4)
    )
    assert base64.b64decode(part['bytes_b64']) == payload[2:6]
    with pytest.raises(ValueError, match='membership differs'):
        store(instance).fetch_checkpoint_member(instance.attempt, 'deadbeef' + '0' * 56, 0, 16)
    with pytest.raises(ValueError, match='outside member'):
        store(instance).fetch_checkpoint_member(
            instance.attempt, members['payload'], len(payload) + 10, 4
        )
    staged = store(instance).stage_checkpoint_artifact(
        instance.attempt, 'attempt_journal', b'staged-bytes'
    )
    assert staged == sha256(b'staged-bytes')


def test_commit_pass_reaches_n2_ready_and_exact_retry_is_identical(tmp_path, monkeypatch):
    instance = g5_claimed(tmp_path, monkeypatch)
    candidate = persisted_intent(instance)
    response = json.loads(commit(instance, candidate))
    receipt = response['receipt']
    assert receipt['decision'] == 'CONTINUE' and receipt['campaign_state'] == 'N2_READY'
    state = snap(instance)
    assert state['state'] == 'N2_READY'
    assert state['checkpoints']['N1']['state'] == 'COMMITTED'
    assert state['checkpoints']['N1']['assessment_sha256'] == sha256(candidate)
    work = next(w for w in state['works'] if w['work_id'] == 'g5work')
    assert work['state'] == 'SIGNED'
    retry = json.loads(commit(instance, candidate))
    assert retry['receipt'] == receipt and retry['historical'] is True
    with pytest.raises(ValueError, match='exact checkpoint candidate retry required'):
        commit(instance, candidate_document(instance, decision='FAILURE'))


def test_commit_fail_reaches_the_terminal_statistical_prefix(tmp_path, monkeypatch):
    instance = g5_claimed(tmp_path, monkeypatch)
    candidate = persisted_intent(instance, candidate_document(instance, decision='FAILURE'))
    json.loads(commit(instance, candidate))
    state = snap(instance)
    assert state['state'] == 'N1_FAILED'
    assert state['checkpoints']['N1']['decision'] == 'FAILURE'


@pytest.mark.parametrize('decision,terminal', [('CONTINUE', 'N2_READY'), ('FAILURE', 'N1_FAILED')])
def test_committed_g5_settles_within_budget_and_completes(tmp_path, monkeypatch, decision, terminal):
    """The committing G5 work settles after T2 and must still complete in the
    progression state its own commit produced (PR #455 review, Codex P2)."""
    instance = g5_claimed(tmp_path, monkeypatch)
    commit(instance, persisted_intent(instance, candidate_document(instance, decision=decision)))
    settle(instance, 'g5work')
    transition(instance, 'g5work', 'COMPLETED')
    state = snap(instance)
    assert state['state'] == terminal
    assert next(w for w in state['works'] if w['work_id'] == 'g5work')['state'] == 'COMPLETED'


@pytest.mark.parametrize('decision', ['CONTINUE', 'FAILURE'])
def test_committed_g5_overrun_blocks_the_progression(tmp_path, monkeypatch, decision):
    """An overrun observed when the G5 work settles after T2 permanently blocks
    authority (spec 2.5): the progression becomes BUDGET_EXHAUSTED, the work
    cannot complete, and the receipt survives only as history (Codex P1)."""
    instance = g5_claimed(tmp_path, monkeypatch)
    candidate = persisted_intent(instance, candidate_document(instance, decision=decision))
    receipt = json.loads(commit(instance, candidate))['receipt']
    limit = next(w for w in snap(instance)['works'] if w['work_id'] == 'g5work')['limits']['cpu_ns']
    settle(instance, 'g5work', cpu=limit + 1)
    assert snap(instance)['state'] == 'BUDGET_EXHAUSTED'
    with pytest.raises(ValueError, match='terminal campaign budget'):
        transition(instance, 'g5work', 'COMPLETED')
    retry = json.loads(commit(instance, candidate))
    assert retry['receipt'] == receipt and retry['historical'] is True


def test_stale_revision_or_void_refuses_the_commit(tmp_path, monkeypatch):
    instance = g5_claimed(tmp_path, monkeypatch)
    # A candidate whose snapshot revision is not the persisted T1 revision is
    # refused even though its bytes are the persisted ones.
    stale = persisted_intent(instance, candidate_document(instance, revision=999))
    with pytest.raises(ValueError, match='snapshot identity differs'):
        commit(instance, stale)
    with pytest.raises(ValueError, match='exact checkpoint candidate retry required'):
        commit(instance, candidate_document(instance))


def test_void_before_commit_refuses_the_commit(tmp_path, monkeypatch):
    # Spec 2.8's single observable ordering: a VOID that commits first leaves
    # no authority for the assessment commit.
    instance = g5_claimed(tmp_path, monkeypatch)
    candidate = persisted_intent(instance)
    cutoff = cutoff_document(instance, candidate)
    with instance.store.transaction() as connection:
        connection.execute(
            "UPDATE full_campaigns SET validity='VOID' WHERE attempt_id=?", (instance.attempt,)
        )
    with pytest.raises(ValueError, match='VOID campaign'):
        store(instance).commit_checkpoint_assessment(
            instance.attempt,
            'g5work',
            candidate,
            cutoff,
            now=datetime(2026, 9, 21, tzinfo=timezone.utc),
            clock_bytes=supervisor.observe_campaign_clock(),
        )


def test_intent_survives_restart_and_exact_retry_completes(tmp_path, monkeypatch):
    instance = g5_claimed(tmp_path, monkeypatch)
    candidate = persisted_intent(instance)
    reopened = CampaignStore(ExecutionStore(instance.store.path))
    assert (
        json.loads(reopened.budget_snapshot(instance.attempt))['checkpoints']['N1']['state']
        == 'ASSESSING'
    )
    reopened.commit_checkpoint_assessment(
        instance.attempt,
        'g5work',
        candidate,
        cutoff_document(instance, candidate),
        now=datetime(2026, 9, 21, tzinfo=timezone.utc),
        clock_bytes=supervisor.observe_campaign_clock(),
    )
    final = json.loads(reopened.budget_snapshot(instance.attempt))
    assert final['state'] == 'N2_READY'


def warm(tmp_path, monkeypatch, *, eligible=True, dispatch=True):
    service = object.__new__(ExecutionService)
    service.store = ExecutionStore(tmp_path / 'journal.sqlite')
    service.config = {'host_run_id': 'host1', 'service_uid': SERVICE_UID}
    service.profile = SimpleNamespace(values={'schema': 'qualification_execution_profile/v5'})
    service.dispatch_lock = threading.Lock()
    service.recovery_issues = {}
    service.schedule_eligible = eligible
    service.dispatch_eligible = dispatch
    monkeypatch.setattr(supervisor, 'controller_cpu_guard', nullcontext)
    return service


def test_v4_service_route_refuses_the_dispatch_roles(tmp_path, monkeypatch):
    """Fail-on-base capability + guard: on a v4 installation the schedule route
    refuses n1_worker with the dispatch-release refusal (and on the S2 base the
    same request cannot even parse the role)."""
    service = warm(tmp_path, monkeypatch, dispatch=False)
    document = encoded(
        {
            'schema': 'qualification_campaign_schedule_request/v1',
            'attempt_id': 'a1',
            'work_id': 'n1work',
            'role': 'n1_worker',
            'probe': 'noop',
            'signing_retry_of': None,
            'fault': None,
        }
    )
    with pytest.raises(ValueError, match='installed N1 dispatch release required'):
        service._schedule_request(SERVICE_UID, document)
    service.dispatch_eligible = True
    service.schedule_eligible = False
    probe = encoded(
        {
            'schema': 'qualification_campaign_schedule_request/v1',
            'attempt_id': 'a1',
            'work_id': 'probe1',
            'role': 'probe_worker',
            'probe': 'noop',
            'signing_retry_of': None,
            'fault': None,
        }
    )
    with pytest.raises(ValueError, match='execution-capable diagnostic release'):
        service._schedule_request(SERVICE_UID, probe)


def test_v5_installation_keeps_the_funded_probe_route(tmp_path, monkeypatch):
    """The /v5 dispatch revision is a superset of /v4: the funded private route
    stays open for harmless probe work while dispatch roles need the v5 gate."""
    service = warm(tmp_path, monkeypatch, eligible=True, dispatch=True)
    probe = encoded(
        {
            'schema': 'qualification_campaign_schedule_request/v1',
            'attempt_id': 'a1',
            'work_id': 'probe1',
            'role': 'probe_worker',
            'probe': 'noop',
            'signing_retry_of': None,
            'fault': None,
        }
    )
    try:
        service._schedule_request(SERVICE_UID, probe)
    except ValueError as exc:
        # The route opened (no release refusal); the empty journal refuses.
        assert 'execution-capable diagnostic release' not in str(exc), exc
        assert 'installed N1 dispatch release required' not in str(exc), exc
    service.dispatch_eligible = False
    with pytest.raises(ValueError, match='installed N1 dispatch release required'):
        service._schedule_request(
            SERVICE_UID,
            (
                schedule_document(instance=None)
                if False
                else encoded(
                    {
                        'schema': 'qualification_campaign_schedule_request/v1',
                        'attempt_id': 'a1',
                        'work_id': 'n1work',
                        'role': 'n1_worker',
                        'probe': 'noop',
                        'signing_retry_of': None,
                        'fault': None,
                    }
                )
            ),
        )


def test_full_e1_assessment_family_exists_and_is_closed():
    """Fail-on-base capability: the FULL_E1 assessment builder and comparator
    exist only on this branch (AttributeError on the S2 base) and refuse any
    value outside the closed evidence shape."""
    from c1_rail.qualification import evidence

    assert hasattr(evidence, 'build_checkpoint_evidence')
    assert hasattr(evidence, 'compare_checkpoint_evidence')
    with pytest.raises(ValueError, match='EVIDENCE_SEMANTIC_MISMATCH'):
        evidence.compare_checkpoint_evidence('not-inspected', expected='also-not-inspected')


# ---- The five §4 negatives (C1 GO condition a) -------------------------------


def _keys_and_context(tmp_path):
    """A minimal verified-path context: enrolled keys, a fake domain, attempt."""
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives import serialization
    from types import SimpleNamespace

    private = {
        name: Ed25519PrivateKey.generate()
        for name in ('test-execution', 'test-producer', 'wrong-key')
    }
    keys = {
        name: SimpleNamespace(
            public_key=key.public_key().public_bytes(
                serialization.Encoding.Raw, serialization.PublicFormat.Raw
            )
        )
        for name, key in private.items()
    }
    domain = SimpleNamespace(
        execution_key_ids=['test-execution'],
        result_key_ids=['test-producer'],
        trusted_key_sha256={
            name: __import__('hashlib').sha256(key.public_key).hexdigest()
            for name, key in keys.items()
        },
    )
    context = SimpleNamespace(attempt_id='neg-attempt', domain=domain)
    return private, keys, context


def test_wrong_signer_is_refused_on_the_verified_paths():
    """Wrong signer: an attestation under a non-execution key and an assessment
    under a non-result key refuse in the g5 verifiers with closed reasons."""
    from c1_rail.qualification.execution import g5
    from c1_rail.qualification.contract import canonical_json_bytes as enc
    import base64

    private, keys, context = _keys_and_context(None)
    payload = {
        'schema': 'qualification_campaign_checkpoint_attestation_payload/v1',
        'scope': 'ATTEST_CAMPAIGN_CHECKPOINT',
        'attempt_id': 'neg-attempt',
        'checkpoint': 'N1',
        'work_id': 'n1work',
        'result_sha256': '0' * 64,
        'payload_sha256': '1' * 64,
        'payload_byte_length': 8,
        'plan_sha256': '2' * 64,
        'execution_release_sha256': '3' * 64,
        'profile_sha256': '4' * 64,
        'service_id': 's',
        'worker_image_digest': 'sha256:' + '5' * 64,
        'runtime_manifest_sha256': '6' * 64,
        'container_id': '7' * 64,
        'capture': {
            'exit_code': 0,
            'oom_killed': False,
            'campaign_scope_id': 'c1',
            'work_scope_id': 'w1',
            'payload_slice': 'p1',
        },
        'observations': {'exit_code': 0, 'oom_killed': False},
        'authorized_at_utc': '2026-09-21T00:00:00Z',
        'started_utc': '2026-09-21T00:00:01Z',
        'completed_utc': '2026-09-21T00:00:02Z',
        'campaign_revision': 1,
    }
    raw_payload = enc(payload)

    def envelope(key_id, sign_with):
        return enc(
            {
                'schema': 'qualification_campaign_checkpoint_attestation/v1',
                'payload': payload,
                'signature': {
                    'algorithm': 'Ed25519',
                    'key_id': key_id,
                    'value_b64': base64.b64encode(sign_with.sign(raw_payload)).decode('ascii'),
                },
            }
        )

    g5.verify_checkpoint_attestation(
        envelope('test-execution', private['test-execution']), context=context, current_keys=keys
    )
    with pytest.raises(
        ValueError, match='checkpoint attestation key is not enrolled for execution'
    ):
        g5.verify_checkpoint_attestation(
            envelope('wrong-key', private['wrong-key']), context=context, current_keys=keys
        )
    with pytest.raises(ValueError, match='checkpoint attestation signature differs'):
        g5.verify_checkpoint_attestation(
            envelope('test-execution', private['wrong-key']), context=context, current_keys=keys
        )
    core = {
        'schema': 'qualification_campaign_checkpoint_assessment/v1',
        'attempt_id': 'neg-attempt',
        'checkpoint': 'N1',
        'work_id': 'n1work',
        'binding': {
            'contract_sha256': '1' * 64,
            'trust_domain_sha256': '2' * 64,
            'policy_sha256': '5' * 64,
            'execution_release_sha256': '3' * 64,
        },
        'snapshot': {
            'campaign_revision': 2,
            'authority_head': '4' * 64,
            'snapshot_sha256': '8' * 64,
        },
        'capture': {
            'result_sha256': '9' * 64,
            'payload_sha256': 'a' * 64,
            'attestation_sha256': 'b' * 64,
        },
        'stages': [
            {
                'stage': 'LEGALITY',
                'status': 'PASS',
                'input_sha256': 'c' * 64,
                'output_sha256': 'd' * 64,
                'population_counts': {},
            },
            {
                'stage': 'N1',
                'status': 'PASS',
                'input_sha256': 'e' * 64,
                'output_sha256': 'f' * 64,
                'population_counts': {'FULL': 2},
            },
        ],
        'decision': 'CONTINUE',
        'n1_decision': 'PASS',
        'cutoff': {'checkpoint': 'N1', 'n1_cutoffs': {'FULL': 0}},
        'n2_thresholds': {
            'bound_to': '1' * 64,
            'stages': [{'stage': 'N2', 'exact_depth': 2, 'max_failures_per_population': 0}],
        },
        'artifacts': [{'role': 'attempt_journal', 'sha256': '0' * 64, 'byte_length': 4}],
    }

    def candidate(key_id, sign_with):
        signature = {
            'algorithm': 'Ed25519',
            'key_id': key_id,
            'value_b64': base64.b64encode(sign_with.sign(enc(core))).decode('ascii'),
        }
        return enc(dict(core, signature=signature))

    g5.verify_checkpoint_assessment(
        candidate('test-producer', private['test-producer']), context=context, current_keys=keys
    )
    with pytest.raises(ValueError, match='checkpoint assessment key is not enrolled for results'):
        g5.verify_checkpoint_assessment(
            candidate('test-execution', private['test-execution']),
            context=context,
            current_keys=keys,
        )


def test_source_substitution_refuses_at_validation():
    """Source substitution: validated members are the archived bytes; anything
    else refuses with the closed membership reason before reconstruction."""
    from c1_rail.qualification.execution import g5
    from c1_rail.qualification.contract import canonical_json_bytes as enc
    import base64

    private, keys, context = _keys_and_context(None)
    payload_bytes = b'archived-worker-frame'
    result_bytes = b'checkpoint-result-document'
    payload = {
        'schema': 'qualification_campaign_checkpoint_attestation_payload/v1',
        'scope': 'ATTEST_CAMPAIGN_CHECKPOINT',
        'attempt_id': 'neg-attempt',
        'checkpoint': 'N1',
        'work_id': 'n1work',
        'result_sha256': __import__('hashlib').sha256(result_bytes).hexdigest(),
        'payload_sha256': __import__('hashlib').sha256(payload_bytes).hexdigest(),
        'payload_byte_length': len(payload_bytes),
        'plan_sha256': '2' * 64,
        'execution_release_sha256': '3' * 64,
        'profile_sha256': '4' * 64,
        'service_id': 's',
        'worker_image_digest': 'sha256:' + '5' * 64,
        'runtime_manifest_sha256': '6' * 64,
        'container_id': '7' * 64,
        'capture': {
            'exit_code': 0,
            'oom_killed': False,
            'campaign_scope_id': 'c1',
            'work_scope_id': 'w1',
            'payload_slice': 'p1',
        },
        'observations': {'exit_code': 0, 'oom_killed': False},
        'authorized_at_utc': '2026-09-21T00:00:00Z',
        'started_utc': '2026-09-21T00:00:01Z',
        'completed_utc': '2026-09-21T00:00:02Z',
        'campaign_revision': 1,
    }
    attestation = enc(
        {
            'schema': 'qualification_campaign_checkpoint_attestation/v1',
            'payload': payload,
            'signature': {
                'algorithm': 'Ed25519',
                'key_id': 'test-execution',
                'value_b64': base64.b64encode(private['test-execution'].sign(enc(payload))).decode(
                    'ascii'
                ),
            },
        }
    )
    substituted = b'substituted-worker-frame'
    with pytest.raises(ValueError, match='checkpoint capture membership differs'):
        g5.validate_campaign_checkpoint(
            context,
            checkpoint='N1',
            plan_bytes=b'plan',
            attestation_bytes=attestation,
            artifacts={'result': result_bytes, 'worker_result': substituted},
            snapshot_bytes=b'snapshot',
            current_keys=keys,
        )
    with pytest.raises(ValueError, match='checkpoint capture membership differs'):
        g5.validate_campaign_checkpoint(
            context,
            checkpoint='N1',
            plan_bytes=b'other-plan',
            attestation_bytes=attestation,
            artifacts={'result': result_bytes, 'worker_result': payload_bytes},
            snapshot_bytes=b'snapshot',
            current_keys=keys,
        )


def test_altered_outcome_candidate_is_refused(tmp_path, monkeypatch):
    """Altered outcomes: a coherently re-signed candidate whose decision flips
    the captured facts is never authority -- the persisted candidate is the only
    one the window accepts, and its cutoff binding refuses the stranger."""
    instance = g5_claimed(tmp_path, monkeypatch)
    candidate = persisted_intent(instance)
    tampered = json.loads(candidate)
    for stage in tampered['stages']:
        if stage['stage'] == 'N1':
            stage['status'] = 'PASS' if stage['status'] == 'FAIL' else 'FAIL'
    tampered['n1_decision'] = tampered['stages'][1]['status']
    tampered['decision'] = 'CONTINUE' if tampered['n1_decision'] == 'PASS' else 'FAILURE'
    tampered['cutoff']['n1_cutoffs'] = {'FULL': 9, 'H1': 9, 'H2': 9}
    tampered_bytes = encoded(tampered)
    cutoff = cutoff_document(instance, tampered_bytes)
    with pytest.raises(ValueError, match='exact checkpoint candidate retry required'):
        store(instance).commit_checkpoint_assessment(
            instance.attempt,
            'g5work',
            tampered_bytes,
            cutoff,
            now=datetime(2026, 9, 21, tzinfo=timezone.utc),
            clock_bytes=supervisor.observe_campaign_clock(),
        )


def test_expired_deadline_refuses_the_commit_without_receipt(tmp_path, monkeypatch):
    """Expiry at T2: the deadline passed between the intent and the commit; the
    commit returns no receipt, the campaign is terminal and the family window
    stays uncommitted."""
    instance = g5_claimed(tmp_path, monkeypatch)
    candidate = persisted_intent(instance)
    state = snap(instance)
    expired = dict(
        json.loads(supervisor.observe_campaign_clock()),
        boottime_ns=state['deadline_boottime_ns'] + 10**9,
    )
    response = store(instance).commit_checkpoint_assessment(
        instance.attempt,
        'g5work',
        candidate,
        cutoff_document(instance, candidate),
        now=datetime(2026, 9, 21, tzinfo=timezone.utc),
        clock_bytes=encoded(expired),
    )
    assert b'receipt' not in response or json.loads(response).get('receipt') is None
    final = snap(instance)
    assert final['state'] == 'BUDGET_EXHAUSTED'
    assert final['checkpoints']['N1']['state'] == 'ASSESSING'
    with instance.store.transaction() as connection:
        row = connection.execute(
            'SELECT receipt_bytes FROM full_campaign_checkpoint_intents ' 'WHERE attempt_id=?',
            (instance.attempt,),
        ).fetchone()
    assert row[0] is None, 'no receipt may exist for an expired commit'


def test_n1_g5_exhaustion_grants_no_credit(tmp_path, monkeypatch):
    """N1_G5 exhaustion: a measured overrun of the N1_G5 reservation consumes it
    whole and terminalises the budget; the assessment window then grants no
    credit and no commit, and the work settles with the facts retained."""
    instance = g5_claimed(tmp_path, monkeypatch)
    ceiling = snap(instance)['profile']['phases']['N1_G5']['cpu_ns']
    scopes = supervisor.work_enrollment('host1', instance.attempt, 'g5work')
    overrun = encoded(
        {
            'schema': 'qualification_campaign_observation/v2',
            'attempt_id': instance.attempt,
            'work_id': 'g5work',
            'clock': json.loads(supervisor.observe_campaign_clock()),
            'campaign_scope_id': scopes['campaign_slice'],
            'work_scope_id': scopes['payload_slice'],
            'cpu_ns': ceiling,
            'memory_peak_bytes': 50,
            'oom_events': 0,
            'termination_known': True,
            'orchestration_charge_cpu_ns': snap(instance)['profile']['orchestration_cpu_ns'][
                'N1_G5'
            ],
        }
    )
    store(instance).settle_work(instance.attempt, 'g5work', overrun)
    final = snap(instance)
    assert final['state'] == 'BUDGET_EXHAUSTED'
    work = next(w for w in final['works'] if w['work_id'] == 'g5work')
    assert (
        work['charge_cpu_ns'] > work['limits']['cpu_ns']
    ), 'an overrun consumes the whole reservation'
    candidate = candidate_document(instance)
    with pytest.raises(ValueError, match='terminal campaign budget'):
        persisted_intent(instance, candidate)
    assert final['checkpoints']['N1']['state'] == 'ATTESTED', 'no assessment credit was granted'
    with pytest.raises(ValueError, match='exact checkpoint candidate retry required'):
        commit(instance, candidate)


def test_service_commit_checkpoint_on_a_funded_campaign(tmp_path, monkeypatch):
    """The coordinator's heads-up regression, at wire level: the funded route's
    T2 calls CampaignStore.context(), which reads the campaign row's receipt --
    after the admission finish that column must carry the admitted diagnostic
    receipt, not the provisional intent, or every COMMIT_CHECKPOINT_ASSESSMENT
    refuses. The full G5 sequence runs through handle_request on a funded
    campaign with a real worker capture."""
    import base64
    import importlib
    from bundle_fixture import build_bundle
    from test_campaign_admission import running
    from c1_rail.qualification.execution import g5 as g5_module
    from c1_rail.qualification.execution.admission import verify_bundle
    from c1_rail.qualification.execution.plan import derive_campaign_plan_from_context
    from c1_rail.qualification.execution.protocol import decode_frame
    from c1_rail.qualification.checkpoint_plan import derive_checkpoint_plan

    # A dispatch campaign whose capture is a REAL worker frame over its own bundle.
    worker_module = importlib.import_module('c1_rail.qualification.execution.worker')
    monkeypatch.setattr(worker_module, 'utc_now', lambda: NOW)
    instance, case = campaign(tmp_path, monkeypatch)
    context = verified_context(instance, case)
    staged = tmp_path / 'worker-input'
    (staged / 'installation').mkdir(parents=True)
    (staged / 'bundle').mkdir()
    from c1_rail.qualification.checkpoint_plan import derive_n1_plan

    plan_for_worker = derive_n1_plan(
        context.contract,
        policy=context.policy,
        execution_release_sha256=context.domain.execution_release_sha256,
        attempt_id=context.attempt_id,
        exact_depth_approval_sha256=context.exact_depth_approval.approval_sha256,
    )
    (staged / 'plan.json').write_bytes(plan_for_worker)
    (staged / 'installation' / 'release.json').write_bytes(case['release'])
    (staged / 'installation' / 'keys.json').write_bytes(
        encoded(
            {
                'schema': 'qualification_trusted_keys/v1',
                'keys': [
                    {
                        'key_id': key.key_id,
                        'public_key_b64': base64.b64encode(key.public_key).decode(),
                        'authority_class': key.authority_class,
                        'revoked_at': None,
                    }
                    for key in case['keys'].values()
                ],
            }
        )
    )
    (staged / 'bundle' / 'index.json').write_bytes(context.retained_bundle_index)
    for row in json.loads(context.retained_bundle_index)['entries']:
        target = staged / 'bundle' / row['path']
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(context.retained_bytes[row['role']])
    frame = worker_module.run_worker(staged, execution_id='n1work')
    payload = decode_frame(frame, limit=context.profile.output_byte_limit)
    document = json.loads(payload)

    materialized(instance)
    retained_identity(instance, 'n1work')
    transition(instance, 'n1work', 'RUNNING')
    dispatched(instance, 'n1work')
    release = json.loads(case['release'])
    scopes = supervisor.work_enrollment('host1', instance.attempt, 'n1work')
    plan_bytes = derive_checkpoint_plan(
        store(instance).retained_object(instance.attempt, 'plan'), 'N1', None
    )
    result = encoded(
        {
            'schema': 'qualification_campaign_checkpoint_result/v1',
            'attempt_id': instance.attempt,
            'checkpoint': 'N1',
            'work_id': 'n1work',
            'campaign_id': 'campaign-1',
            'plan_sha256': sha256(plan_bytes),
            'plan_byte_length': len(plan_bytes),
            'payload_sha256': sha256(payload),
            'payload_byte_length': len(payload),
            'worker_execution_id': 'n1work',
            'container_id': '9' * 64,
            'worker_image_digest': release['worker_image_digest'],
            'runtime_manifest_sha256': sha256(encoded(release['runtime_manifests']['worker'])),
            'capture': {
                'exit_code': 0,
                'oom_killed': False,
                'started_utc': '2026-09-21T00:00:01Z',
                'completed_utc': '2026-09-21T00:00:02Z',
                'authorized_at_utc': '2026-09-21T00:00:00Z',
                'campaign_scope_id': scopes['campaign_slice'],
                'work_scope_id': scopes['payload_slice'],
                'payload_slice': scopes['payload_slice'],
            },
            'limits': {
                'cpu_ns': snap(instance)['profile']['phases']['N1']['cpu_ns'],
                'wall_ns': snap(instance)['profile']['phases']['N1']['wall_ns'],
                'memory_bytes': snap(instance)['profile']['phases']['N1']['memory_bytes'],
                'orchestration_cpu_ns': snap(instance)['profile']['orchestration_cpu_ns']['N1'],
            },
            'observations': dict(exit_code=0, oom_killed=False, **document['observations']),
            'created_utc': '2026-09-21T00:00:03Z',
        }
    )
    capture_transition = encoded(
        {
            'schema': 'qualification_campaign_work_transition/v1',
            'attempt_id': instance.attempt,
            'work_id': 'n1work',
            'state': 'CAPTURED',
            'clock': json.loads(supervisor.observe_campaign_clock()),
            'data': {'capture_bytes_b64': base64.b64encode(result).decode('ascii')},
        }
    )
    store(instance).retain_checkpoint_capture(
        instance.attempt, 'n1work', result, payload, capture_transition
    )
    attestation_payload = {
        'schema': 'qualification_campaign_checkpoint_attestation_payload/v1',
        'scope': 'ATTEST_CAMPAIGN_CHECKPOINT',
        'attempt_id': instance.attempt,
        'checkpoint': 'N1',
        'work_id': 'n1work',
        'result_sha256': sha256(result),
        'payload_sha256': sha256(payload),
        'payload_byte_length': len(payload),
        'plan_sha256': sha256(plan_bytes),
        'execution_release_sha256': sha256(case['release']),
        'profile_sha256': release['profile_sha256'],
        'service_id': release['service_id'],
        'worker_image_digest': release['worker_image_digest'],
        'runtime_manifest_sha256': sha256(encoded(release['runtime_manifests']['worker'])),
        'container_id': '9' * 64,
        'capture': {
            'exit_code': 0,
            'oom_killed': False,
            'campaign_scope_id': scopes['campaign_slice'],
            'work_scope_id': scopes['payload_slice'],
            'payload_slice': scopes['payload_slice'],
        },
        'observations': dict(exit_code=0, oom_killed=False, **document['observations']),
        'authorized_at_utc': '2026-09-21T00:00:00Z',
        'started_utc': '2026-09-21T00:00:01Z',
        'completed_utc': '2026-09-21T00:00:02Z',
        'campaign_revision': 2,
    }
    attestation = encoded(
        {
            'schema': 'qualification_campaign_checkpoint_attestation/v1',
            'payload': attestation_payload,
            'signature': {
                'algorithm': 'Ed25519',
                'key_id': 'test-execution',
                'value_b64': base64.b64encode(
                    case['private']['test-execution'].sign(encoded(attestation_payload))
                ).decode('ascii'),
            },
        }
    )
    store(instance).retain_checkpoint_attestation(
        instance.attempt, attestation, verify=lambda *args, **kwargs: None
    )
    settle(instance, 'n1work')
    transition(instance, 'n1work', 'COMPLETED')
    materialized(instance, schedule_document(instance, role='n1_g5', work='g5work'))
    retained_identity(instance, 'g5work')
    transition(instance, 'g5work', 'RUNNING')
    dispatched(instance, 'g5work')

    def wire(operation, **values):
        return instance.handle_request(
            G5,
            encoded(
                dict(
                    schema='qualification_campaign_request/v2',
                    operation=operation,
                    attempt_id=instance.attempt,
                    **values,
                )
            ),
        )

    snapshot_reply = wire('CHECKPOINT_SNAPSHOT', checkpoint='N1')
    verified = verified_context(instance, case)
    evidence = g5_module.validate_campaign_checkpoint(
        context=verified,
        checkpoint='N1',
        plan_bytes=plan_bytes,
        attestation_bytes=attestation,
        artifacts={'result': result, 'worker_result': payload},
        snapshot_bytes=snapshot_reply,
        current_keys=case['keys'],
    )
    for role, raw in evidence.output_bytes_by_role.items():
        staged_reply = json.loads(
            wire(
                'STAGE_CHECKPOINT_ARTIFACT',
                checkpoint='N1',
                role=role,
                bytes_b64=base64.b64encode(raw).decode('ascii'),
            )
        )
        assert staged_reply == {'artifact_sha256': sha256(raw)}
    core = json.loads(evidence.assessment_bytes)
    core['signature'] = {
        'algorithm': 'Ed25519',
        'key_id': 'test-producer',
        'value_b64': base64.b64encode(
            case['private']['test-producer'].sign(evidence.assessment_bytes)
        ).decode('ascii'),
    }
    candidate = encoded(core)
    g5_module.verify_checkpoint_assessment(candidate, context=verified, current_keys=case['keys'])
    commit_reply = json.loads(
        wire(
            'COMMIT_CHECKPOINT_ASSESSMENT',
            checkpoint='N1',
            work_id='g5work',
            candidate_bytes_b64=base64.b64encode(candidate).decode('ascii'),
            artifacts=[
                {'role': role, 'sha256': sha256(raw)}
                for role, raw in sorted(evidence.output_bytes_by_role.items())
            ],
        )
    )
    receipt = commit_reply['receipt']
    assert receipt['decision'] == 'CONTINUE' and receipt['campaign_state'] == 'N2_READY'
    final = snap(instance)
    assert final['state'] == 'N2_READY'
    assert final['checkpoints']['N1']['state'] == 'COMMITTED'
