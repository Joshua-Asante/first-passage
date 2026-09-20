"""S2-G2: funded post-admission cancellation authentication and safe admission retry.

Real SQLite journal, real signed TEST_ONLY bundles and approvals; the trusted
clock, the controller CPU guard and the OS runtime are simulated. Nothing here
is Linux enforcement evidence; test_campaign_service_linux.py holds that.
"""
import base64
import json
from contextlib import nullcontext

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution import campaign_supervisor as supervisor
from c1_rail.qualification.execution import service as service_module
from c1_rail.qualification.execution.campaign_store import (
    CANCELLATION_PENDING, VOID_AUTHENTICATION_PREFIX, VOID_REFUSAL_PREFIX,
    VOID_TERMINAL_REFUSAL_PREFIX, CampaignStore)
from c1_rail.qualification.execution.protocol import sha256
from c1_rail.qualification.execution.store import ExecutionStore
from composition_fixture import signed_approval
from test_campaign_admission import running
from test_campaign_budget import clock
from test_contract import NOW

CLIENT, G5, OPERATOR = 1001, 1002, 1003
CHARGE = 2_000_000_000            # control_cpu_seconds + cpu_granularity_seconds
ADMISSION_CHARGE = 20_000_000_000  # installed orchestration bound, measured cpu 0
PHASE = 120_000_000_000


class Runtime:
    """Simulated guardian launcher: records starts and never touches the OS."""
    started = []

    def __init__(self, context):
        pass

    def start(self, state, work, enrollment):
        Runtime.started.append(work['work_id'])

    def observation(self, state, work, enrollment):
        """Known, terminated, zero-usage counters: matches the settled admission exactly."""
        return encoded(dict(schema='qualification_campaign_observation/v2', attempt_id=state['attempt_id'],
            work_id=work['work_id'], clock=json.loads(supervisor.observe_campaign_clock()),
            campaign_scope_id=enrollment['scopes']['campaign_slice'],
            work_scope_id=enrollment['scopes']['payload_slice'], cpu_ns=0, memory_peak_bytes=0,
            oom_events=0, termination_known=True,
            orchestration_charge_cpu_ns=state['profile']['orchestration_cpu_ns'][work['phase']]))

    def cleanup(self, enrollment):
        pass


def funded_service(tmp_path, monkeypatch, *, t=11, budget_seconds=None, **options):
    """A warm execution-capable service (release/v4, funded budget profile v3)."""
    if budget_seconds is not None:
        import test_contract
        original = test_contract._document

        def small():
            doc = original()
            doc['replay']['budget']['maximum_cpu_seconds'] = budget_seconds
            return doc
        monkeypatch.setattr(test_contract, '_document', small)
    instance, case = running(tmp_path, monkeypatch, funded=True, **options)
    instance.config = {'host_run_id': 'host1', 'service_uid': 1004}
    instance.recovery_issues = {}
    Runtime.started = []
    monkeypatch.setattr(supervisor, 'controller_cpu_guard', nullcontext)
    monkeypatch.setattr(supervisor, 'observe_campaign_clock', lambda: encoded(clock(t)))
    monkeypatch.setattr(supervisor, 'LinuxCampaignRuntime', Runtime)
    return instance, case


def fresh_service(instance):
    """A restarted process over the same journal: no in-memory delegation memory."""
    restarted = object.__new__(service_module.ExecutionService)
    restarted.__dict__.update({k: v for k, v in instance.__dict__.items() if k not in ('store', 'delegated_admissions', 'recovery_issues')})
    restarted.store = ExecutionStore(instance.store.path)
    restarted.recovery_issues = {}
    return restarted


def request(case, operation='SUBMIT_E1', **values):
    doc = dict(schema='qualification_campaign_request/v2', operation=operation, attempt_id=case['attempt_id'])
    if operation == 'SUBMIT_E1':
        doc.update(bundle_sha256=sha256(case['index']), request_id='diagnostic')
    doc.update(values)
    return encoded(doc)


def void_request(case, context, *, reason='stop', private=None, key_id='test-freeze'):
    subject = encoded(dict(attempt_id=case['attempt_id'], reason=reason, contract_sha256=context.contract.contract_sha256))
    approval = signed_approval(subject, private or case['private'][key_id], key_id=key_id,
                               scope='VOID_QUALIFICATION_ATTEMPT', contract_sha256=context.contract.contract_sha256)
    return request(case, 'VOID', reason=reason, operator_approval_bytes=base64.b64encode(approval).decode('ascii'))


def verified_context(instance, case):
    from c1_rail.qualification.execution.admission import verify_bundle
    return verify_bundle(instance.root / 'bundles' / sha256(case['index']), case['release'], case['keys'], NOW)


def admission_observation(case, *, t=12):
    scopes = supervisor.work_enrollment('host1', case['attempt_id'], 'admission')
    return encoded(dict(schema='qualification_campaign_observation/v2', attempt_id=case['attempt_id'], work_id='admission',
        clock=clock(t), campaign_scope_id=scopes['campaign_slice'], work_scope_id=scopes['payload_slice'],
        cpu_ns=0, memory_peak_bytes=0, oom_events=0, termination_known=True, orchestration_charge_cpu_ns=ADMISSION_CHARGE))


def admit(instance, case):
    """Submit, then play the admission guardian's charged tail up to the receipt."""
    from c1_rail.qualification.execution.plan import derive_campaign_plan_from_context
    raw = request(case)
    first = json.loads(instance.handle_request(CLIENT, raw))
    assert first['state'] == 'PROVISIONAL' and first['receipt'] is None and Runtime.started == ['admission']
    context = verified_context(instance, case)
    plan = derive_campaign_plan_from_context(context)
    status = CampaignStore(instance.store).finish_diagnostic_admission(
        raw, context, plan, admission_observation(case), now=NOW, trusted_keys=case['keys'])
    assert status['receipt'] is not None and status['state'] == 'BOUND' and status['validity'] == 'VALID'
    assert status['settled_cpu_ns'] == ADMISSION_CHARGE
    return raw, context


def status(instance, case, peer=CLIENT):
    return json.loads(instance.handle_request(peer, request(case, 'STATUS')))


def funding(instance, case):
    return json.loads(CampaignStore(instance.store).scheduler_status(case['attempt_id']))


def objects(instance, case, prefix):
    return sorted(role for role in CampaignStore(instance.store).objects(case['attempt_id']) if role.startswith(prefix))


def snapshot(instance, case):
    return json.loads(CampaignStore(instance.store).budget_snapshot(case['attempt_id']))


# --- Gap 3: funded post-admission VOID authentication ------------------------


def test_invalid_signature_is_charged_every_attempt_and_never_sets_void(tmp_path, monkeypatch):
    instance, case = funded_service(tmp_path, monkeypatch)
    _, context = admit(instance, case)
    before = funding(instance, case)
    frozen = snapshot(instance, case)
    forged = void_request(case, context, private=Ed25519PrivateKey.generate())
    for attempt in range(1, 4):
        with pytest.raises(ValueError):
            instance.handle_request(OPERATOR, forged)
        after = funding(instance, case)
        assert after['settled_cpu_ns'] == before['settled_cpu_ns'] + attempt * CHARGE
        assert after['remaining_cpu_ns'] == before['remaining_cpu_ns'] - attempt * CHARGE
        assert after['validity'] == 'VALID'
        current = status(instance, case)
        assert current['validity'] == 'VALID' and current['void_pending'] is False
        assert current['void_authentication_attempts'] == attempt and current['settled_cpu_ns'] == after['settled_cpu_ns']
        assert current['void_refusal']
        assert len(objects(instance, case, VOID_AUTHENTICATION_PREFIX)) == attempt
        assert len(objects(instance, case, VOID_REFUSAL_PREFIX)) == attempt
        assert objects(instance, case, 'pending_void') == []
    # The snapshot's per-work totals are untouched: the charge lives in the
    # funding projection, which is the only post-admission intent gate.
    assert snapshot(instance, case) == frozen
    reopened = CampaignStore(ExecutionStore(instance.store.path))
    assert json.loads(reopened.scheduler_status(case['attempt_id'])) == funding(instance, case)
    assert reopened.void_retry(forged) is None


def test_valid_approval_is_charged_once_and_the_exact_retry_is_free(tmp_path, monkeypatch):
    instance, case = funded_service(tmp_path, monkeypatch)
    _, context = admit(instance, case)
    before = funding(instance, case)
    valid = void_request(case, context)
    receipt = instance.handle_request(OPERATOR, valid)
    assert json.loads(receipt)['validity'] == 'VOID'
    after = funding(instance, case)
    assert after['settled_cpu_ns'] == before['settled_cpu_ns'] + CHARGE and after['validity'] == 'VOID'
    current = status(instance, case)
    assert current['validity'] == 'VOID' and current['void_authentication_attempts'] == 1 and current['void_refusal'] is None
    assert current['void_pending'] is False and objects(instance, case, 'pending_void') == []
    assert objects(instance, case, VOID_REFUSAL_PREFIX) == []
    # Exact historical retry: identical receipt, no claim, no charge.
    monkeypatch.setattr(service_module, 'verify_detached_approval',
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError('unmetered verification')))
    assert instance.handle_request(OPERATOR, valid) == receipt
    assert funding(instance, case) == after and status(instance, case)['void_authentication_attempts'] == 1
    with pytest.raises(ValueError, match='conflict'):
        instance.handle_request(OPERATOR, void_request(case, context, reason='another'))
    restarted = fresh_service(instance)
    assert restarted.handle_request(OPERATOR, valid) == receipt
    assert json.loads(restarted.handle_request(CLIENT, request(case)))['validity'] == 'VOID'


def test_unenrolled_trusted_key_is_refused_charged_and_retained(tmp_path, monkeypatch):
    instance, case = funded_service(tmp_path, monkeypatch)
    _, context = admit(instance, case)
    before = funding(instance, case)
    with pytest.raises(ValueError, match='not enrolled'):
        instance.handle_request(OPERATOR, void_request(case, context, key_id='test-producer'))
    current = status(instance, case)
    assert current['validity'] == 'VALID' and current['void_authentication_attempts'] == 1
    assert current['void_refusal'] == 'VOID authority is not enrolled'
    assert funding(instance, case)['settled_cpu_ns'] == before['settled_cpu_ns'] + CHARGE
    refusal = json.loads(CampaignStore(instance.store).retained_object(case['attempt_id'], VOID_REFUSAL_PREFIX + '000001'))
    assert refusal['reason'] == 'VOID authority is not enrolled' and refusal['sequence'] == 1
    ExecutionStore(instance.store.path)


@pytest.mark.parametrize('peer', [CLIENT, G5, 1004, 7])
def test_non_operator_peers_are_refused_before_any_cost(tmp_path, monkeypatch, peer):
    instance, case = funded_service(tmp_path, monkeypatch)
    _, context = admit(instance, case)
    before = funding(instance, case)
    monkeypatch.setattr(service_module, 'verify_detached_approval',
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError('verification for a foreign peer')))
    with pytest.raises(ValueError, match='PEER_NOT_AUTHORIZED'):
        instance.handle_request(peer, void_request(case, context))
    assert funding(instance, case) == before
    assert status(instance, case)['void_authentication_attempts'] == 0 and objects(instance, case, 'pending_void') == []


def drain(instance, case, *, keep_ns):
    """Reserve whole installed phases until fewer than keep_ns + one phase remain."""
    campaigns = CampaignStore(instance.store)
    index = 0
    while snapshot(instance, case)['remaining_cpu_ns'] - PHASE >= keep_ns:
        campaigns.reserve_work(case['attempt_id'], 'drain-%02d' % index, 'N1_G5',
            encoded(dict(limits=snapshot(instance, case)['profile']['phases']['N1_G5'], clock=clock(13), input_sha256='d' * 64)),
            expected_revision=snapshot(instance, case)['authority_revision'])
        index += 1
    return snapshot(instance, case)['remaining_cpu_ns']


def test_exhaustion_refuses_the_claim_and_keeps_the_body_pending_without_authentication(tmp_path, monkeypatch):
    # Contract budget 1500 s: twelve 120 s phases bind, 40 s remain after admission
    # and the drain, i.e. exactly twenty charged attempts.
    instance, case = funded_service(tmp_path, monkeypatch, budget_seconds=1500)
    _, context = admit(instance, case)
    remaining = drain(instance, case, keep_ns=40 * 10**9)
    assert remaining == 40 * 10**9 and funding(instance, case)['remaining_cpu_ns'] == remaining
    forged = void_request(case, context, private=Ed25519PrivateKey.generate())
    for attempt in range(1, 21):
        with pytest.raises(ValueError):
            instance.handle_request(OPERATOR, forged)
        assert funding(instance, case)['remaining_cpu_ns'] == remaining - attempt * CHARGE
    assert funding(instance, case)['remaining_cpu_ns'] == 0
    monkeypatch.setattr(service_module, 'verify_detached_approval',
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError('authentication without allowance')))
    refused = json.loads(instance.handle_request(OPERATOR, forged))
    assert refused['schema'] == 'qualification_campaign_status/v2'
    assert refused['void_pending'] is True and refused['validity'] == 'VALID'
    assert refused['void_authentication_attempts'] == 20 and refused['remaining_cpu_ns'] == 0
    assert objects(instance, case, 'pending_void') == ['pending_void']
    # A byte-different body while one is pending is a cheap refusal; a valid
    # approval cannot be funded either, so validity stays VALID and no route
    # forges VOID.
    with pytest.raises(ValueError, match='pending cancellation differs'):
        instance.handle_request(OPERATOR, void_request(case, context))
    assert funding(instance, case)['settled_cpu_ns'] == refused['settled_cpu_ns']
    # Restart preserves the queued body; the exact retry is refused again for free.
    # (The restart's bounded per-work recovery samples a later clock.)
    monkeypatch.setattr(supervisor, 'observe_campaign_clock', lambda: encoded(clock(40)))
    restarted = fresh_service(instance)
    restarted.recover_service()
    assert snapshot(restarted, case)['state'] == 'BOUND'
    again = json.loads(restarted.handle_request(OPERATOR, forged))
    assert again['void_pending'] is True and again['void_authentication_attempts'] == 20
    assert again['validity'] == 'VALID'
    # New positive authority is barred while the body is pending: settlement is not.
    campaigns = CampaignStore(restarted.store)
    with pytest.raises(ValueError, match='cancellation pending'):
        campaigns.reserve_work(case['attempt_id'], 'late', 'N1_G5',
            encoded(dict(limits=snapshot(restarted, case)['profile']['phases']['N1_G5'], clock=clock(14), input_sha256='d' * 64)),
            expected_revision=snapshot(restarted, case)['authority_revision'])
    ExecutionStore(instance.store.path)


def test_barrier_blocks_new_authority_but_not_settlement_recovery_or_negative_facts(tmp_path, monkeypatch):
    from scheduler_fixture import schedule
    instance, case = funded_service(tmp_path, monkeypatch)
    _, context = admit(instance, case)
    attempt = case['attempt_id']
    campaigns = CampaignStore(instance.store)
    limits = snapshot(instance, case)['profile']['phases']['N1_G5']
    # Two works prepared before the body arrives: one started, one merely reserved.
    campaigns.reserve_work(attempt, 'started', 'N1_G5', encoded(dict(limits=limits, clock=clock(13), input_sha256='d' * 64)),
                           expected_revision=snapshot(instance, case)['authority_revision'])
    campaigns.reserve_work(attempt, 'reserved', 'N1_G5', encoded(dict(limits=limits, clock=clock(13), input_sha256='e' * 64)),
                           expected_revision=snapshot(instance, case)['authority_revision'])
    scopes = supervisor.work_enrollment('host1', attempt, 'started')
    campaigns.record_work_transition(attempt, 'started', encoded(dict(schema='qualification_campaign_work_transition/v1',
        attempt_id=attempt, work_id='started', state='START_INTENT', clock=clock(14),
        data=dict(campaign_scope_id=scopes['campaign_slice'], work_scope_id=scopes['payload_slice']))),
        expected_revision=snapshot(instance, case)['authority_revision'])
    valid = void_request(case, context)
    pending = json.loads(campaigns.queue_diagnostic_void(valid))  # transport only: nothing charged, nothing verified
    assert pending['void_pending'] is True and pending['void_authentication_attempts'] == 0
    before = snapshot(instance, case)
    revision = before['authority_revision']
    # New positive authority refuses at every chokepoint.
    with pytest.raises(ValueError, match=CANCELLATION_PENDING):
        campaigns.claim_scheduler_bootstrap(schedule(attempt_id=attempt, work_id='probe'), encoded(clock(15)))
    with pytest.raises(ValueError, match=CANCELLATION_PENDING):
        campaigns.reserve_work(attempt, 'new', 'N1_G5', encoded(dict(limits=limits, clock=clock(15), input_sha256='f' * 64)),
                               expected_revision=revision)
    with pytest.raises(ValueError, match=CANCELLATION_PENDING):
        campaigns.claim_supervision_control(attempt, 'reserved', 'START_OWNER', encoded(clock(15)))
    with pytest.raises(ValueError, match=CANCELLATION_PENDING):
        with campaigns.launch_gate(attempt, 'started', lambda: encoded(clock(15))):
            raise AssertionError('gate opened under a pending cancellation')
    for target in ('RUNNING', 'COMPLETED'):
        with pytest.raises(ValueError, match=CANCELLATION_PENDING):
            campaigns.record_work_transition(attempt, 'started', encoded(dict(schema='qualification_campaign_work_transition/v1',
                attempt_id=attempt, work_id='started', state=target, clock=clock(15), data={})), expected_revision=revision)
    with pytest.raises(ValueError, match=CANCELLATION_PENDING):
        campaigns.bind_budget(attempt, encoded(before['budget']), expected_revision=revision, clock_bytes=encoded(clock(15)))
    assert snapshot(instance, case) == before
    # Settlement, negative facts, recovery and reads continue.
    observed = encoded(dict(schema='qualification_campaign_observation/v2', attempt_id=attempt, work_id='started',
        clock=clock(16), campaign_scope_id=scopes['campaign_slice'], work_scope_id=scopes['payload_slice'],
        cpu_ns=5, memory_peak_bytes=1, oom_events=0, termination_known=True, orchestration_charge_cpu_ns=ADMISSION_CHARGE))
    settled = json.loads(campaigns.settle_work(attempt, 'started', observed))
    assert next(w for w in settled['works'] if w['work_id'] == 'started')['charge_cpu_ns'] == 5 + ADMISSION_CHARGE
    assert settled['validity'] == 'VALID' and settled['state'] == 'BOUND'
    assert json.loads(campaigns.budget_snapshot(attempt)) == settled  # the read stays open to the guardian's polls
    # The same request through the operator route authenticates immediately:
    # the barrier is transient in the fundable case and never itself sets VOID.
    receipt = json.loads(instance.handle_request(OPERATOR, valid))
    assert receipt['validity'] == 'VOID'
    assert status(instance, case)['void_authentication_attempts'] == 1 and objects(instance, case, 'pending_void') == []
    ExecutionStore(instance.store.path)


def test_negative_transition_proceeds_under_the_barrier_and_leaves_the_body_pending_on_a_terminal_campaign(tmp_path, monkeypatch):
    instance, case = funded_service(tmp_path, monkeypatch)
    _, context = admit(instance, case)
    attempt = case['attempt_id']
    campaigns = CampaignStore(instance.store)
    limits = snapshot(instance, case)['profile']['phases']['N1_G5']
    campaigns.reserve_work(attempt, 'reserved', 'N1_G5', encoded(dict(limits=limits, clock=clock(13), input_sha256='e' * 64)),
                           expected_revision=snapshot(instance, case)['authority_revision'])
    valid = void_request(case, context)
    campaigns.queue_diagnostic_void(valid)
    # Recovery of the reserved work proceeds under the barrier (a clock fact).
    campaigns.recover_work(attempt, 'reserved', encoded(clock(16)))
    assert snapshot(instance, case)['state'] == 'BOUND'
    # ABORTED is a negative fact: it commits under the barrier and, being a
    # campaign terminal, makes the queued body unfundable -- but never
    # unrecordable (S2-G4 A1): the terminal-but-VALID campaign authenticates the
    # body once, uncharged, so the operator's VOID intent is answered instead of
    # pending forever, and no charge object exists for it.
    state = json.loads(campaigns.record_work_transition(attempt, 'reserved', encoded(dict(
        schema='qualification_campaign_work_transition/v1', attempt_id=attempt, work_id='reserved',
        state='ABORTED', clock=clock(17), data={})), expected_revision=snapshot(instance, case)['authority_revision']))
    assert state['state'] == 'ABORTED'
    receipt = json.loads(instance.handle_request(OPERATOR, valid))
    assert receipt['validity'] == 'VOID'
    current = status(instance, case)
    assert current['state'] == 'ABORTED' and current['void_pending'] is False
    assert current['void_authentication_attempts'] == 0  # uncharged: no charge object was minted
    assert objects(instance, case, VOID_AUTHENTICATION_PREFIX) == []
    assert funding(instance, case)['settled_cpu_ns'] == ADMISSION_CHARGE  # the terminal attempt costs nothing
    assert campaigns.void_retry(valid) is not None
    ExecutionStore(instance.store.path)


def test_pre_admission_body_never_blocks_the_admission_guardian_and_is_authenticated_at_the_receipt(tmp_path, monkeypatch):
    from scheduler_fixture import schedule
    from c1_rail.qualification.execution.plan import derive_campaign_plan_from_context
    instance, case = funded_service(tmp_path, monkeypatch)
    attempt = case['attempt_id']
    raw = request(case)
    assert json.loads(instance.handle_request(CLIENT, raw))['state'] == 'PROVISIONAL'
    context = verified_context(instance, case)
    valid = void_request(case, context)
    monkeypatch.setattr(service_module, 'verify_detached_approval',
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError('verification before the receipt')))
    queued = json.loads(instance.handle_request(OPERATOR, valid))
    assert queued['void_pending'] is True and queued['void_authentication_attempts'] == 0 and queued['receipt'] is None
    assert funding(instance, case)['settled_cpu_ns'] == 0
    campaigns = CampaignStore(instance.store)
    # A new work grant refuses even before the receipt ...
    with pytest.raises(ValueError, match=CANCELLATION_PENDING):
        campaigns.claim_scheduler_bootstrap(schedule(attempt_id=attempt, work_id='probe'), encoded(clock(12)))
    # ... while the admission guardian's own progress (RUNNING, binding) is not barred.
    state = json.loads(campaigns.record_work_transition(attempt, 'admission', encoded(dict(
        schema='qualification_campaign_work_transition/v1', attempt_id=attempt, work_id='admission',
        state='RUNNING', clock=clock(12), data={})), expected_revision=snapshot(instance, case)['authority_revision']))
    contract = json.loads(context.contract.canonical_bytes)
    state = json.loads(campaigns.bind_budget(attempt, encoded(contract['replay']['budget']),
                                             expected_revision=state['authority_revision'], clock_bytes=encoded(clock(13))))
    assert state['state'] == 'BOUND'
    plan = derive_campaign_plan_from_context(context)
    result = campaigns.finish_diagnostic_admission(raw, context, plan, admission_observation(case, t=14), now=NOW, trusted_keys=case['keys'])
    assert result['validity'] == 'VOID' and result['receipt'] is None and result['settled_cpu_ns'] == ADMISSION_CHARGE
    assert result['void_authentication_attempts'] == 0 and result['void_pending'] is False
    assert campaigns.void_retry(valid) is not None
    ExecutionStore(instance.store.path)


@pytest.mark.parametrize('kind', ['forged', 'unenrolled'])
def test_refused_pre_admission_body_is_retained_cleared_and_admission_still_completes(tmp_path, monkeypatch, kind):
    """Coordinator addendum (1): a pre-admission refusal is a retained fact under the admission's own charge, never an admission failure."""
    from c1_rail.qualification.execution.campaign_store import VOID_ADMISSION_REFUSAL_PREFIX
    from c1_rail.qualification.execution.plan import derive_campaign_plan_from_context
    instance, case = funded_service(tmp_path, monkeypatch)
    attempt = case['attempt_id']
    raw = request(case)
    assert json.loads(instance.handle_request(CLIENT, raw))['state'] == 'PROVISIONAL'
    context = verified_context(instance, case)
    body = (void_request(case, context, private=Ed25519PrivateKey.generate()) if kind == 'forged'
            else void_request(case, context, key_id='test-producer'))
    queued = json.loads(instance.handle_request(OPERATOR, body))
    assert queued['void_pending'] is True and queued['receipt'] is None
    campaigns = CampaignStore(instance.store)
    plan = derive_campaign_plan_from_context(context)
    result = campaigns.finish_diagnostic_admission(raw, context, plan, admission_observation(case), now=NOW, trusted_keys=case['keys'])
    # Admission completed normally: receipt, BOUND, VALID, the admission charge only.
    assert result['receipt'] is not None and result['state'] == 'BOUND' and result['validity'] == 'VALID'
    assert result['settled_cpu_ns'] == ADMISSION_CHARGE and result['void_authentication_attempts'] == 0
    assert result['void_pending'] is False and result['void_refusal']
    if kind == 'unenrolled':
        assert result['void_refusal'] == 'pending cancellation authority is not enrolled'
    assert objects(instance, case, 'pending_void') == []
    assert objects(instance, case, VOID_AUTHENTICATION_PREFIX) == [] and objects(instance, case, VOID_REFUSAL_PREFIX) == []
    assert objects(instance, case, VOID_ADMISSION_REFUSAL_PREFIX) == [VOID_ADMISSION_REFUSAL_PREFIX + '000001']
    refusal = json.loads(campaigns.retained_object(attempt, VOID_ADMISSION_REFUSAL_PREFIX + '000001'))
    assert refusal['request_sha256'] == sha256(body) and refusal['sequence'] == 1
    assert campaigns.void_retry(body) is None
    # The route is open again and the same body, now post-admission, is charged and refused.
    with pytest.raises(ValueError):
        instance.handle_request(OPERATOR, body)
    current = status(instance, case)
    assert current['validity'] == 'VALID' and current['void_authentication_attempts'] == 1
    assert current['settled_cpu_ns'] == ADMISSION_CHARGE + CHARGE
    assert objects(instance, case, VOID_REFUSAL_PREFIX) == [VOID_REFUSAL_PREFIX + '000001']
    # A valid approval still ends it.
    assert json.loads(instance.handle_request(OPERATOR, void_request(case, context)))['validity'] == 'VOID'
    ExecutionStore(instance.store.path)


def test_persistence_only_release_queues_and_never_authenticates(tmp_path, monkeypatch):
    """release/v3 has no funding projection to charge: fail-closed, the body waits."""
    instance, case = running(tmp_path, monkeypatch, diagnostic=True)
    instance.config = {'host_run_id': 'host1', 'service_uid': 1004}
    instance.recovery_issues = {}
    Runtime.started = []
    monkeypatch.setattr(supervisor, 'controller_cpu_guard', nullcontext)
    monkeypatch.setattr(supervisor, 'observe_campaign_clock', lambda: encoded(clock(11)))
    monkeypatch.setattr(supervisor, 'LinuxCampaignRuntime', Runtime)
    _, context = admit(instance, case)
    monkeypatch.setattr(service_module, 'verify_detached_approval',
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError('unfunded verification')))
    reply = json.loads(instance.handle_request(OPERATOR, void_request(case, context)))
    assert reply['validity'] == 'VALID' and reply['void_pending'] is True and reply['void_authentication_attempts'] == 0
    assert objects(instance, case, VOID_AUTHENTICATION_PREFIX) == []
    ExecutionStore(instance.store.path)


def test_interrupted_attempt_keeps_the_charge_and_the_body_and_the_retry_is_charged_again(tmp_path, monkeypatch):
    instance, case = funded_service(tmp_path, monkeypatch)
    _, context = admit(instance, case)
    valid = void_request(case, context)
    original = service_module.verify_detached_approval
    monkeypatch.setattr(service_module, 'verify_detached_approval',
                        lambda *a, **k: (_ for _ in ()).throw(RuntimeError('service died during verification')))
    with pytest.raises(RuntimeError):
        instance.handle_request(OPERATOR, valid)
    current = status(instance, case)
    assert current['void_authentication_attempts'] == 1 and current['void_pending'] is True
    assert current['void_refusal'] is None and objects(instance, case, VOID_REFUSAL_PREFIX) == []
    assert funding(instance, case)['settled_cpu_ns'] == ADMISSION_CHARGE + CHARGE
    monkeypatch.setattr(service_module, 'verify_detached_approval', original)
    monkeypatch.setattr(supervisor, 'observe_campaign_clock', lambda: encoded(clock(40)))
    restarted = fresh_service(instance)
    restarted.recover_service()
    assert snapshot(restarted, case)['state'] == 'BOUND'
    assert json.loads(restarted.handle_request(OPERATOR, valid))['validity'] == 'VOID'
    final = json.loads(restarted.handle_request(CLIENT, request(case, 'STATUS')))
    assert final['void_authentication_attempts'] == 2 and final['settled_cpu_ns'] == ADMISSION_CHARGE + 2 * CHARGE
    ExecutionStore(instance.store.path)


@pytest.mark.parametrize('damage', ['charge_amount', 'refusal_orphan', 'funding_total', 'pre_receipt_charge'])
def test_reopen_rejects_tampered_cancellation_accounting(tmp_path, monkeypatch, damage):
    import sqlite3
    instance, case = funded_service(tmp_path, monkeypatch)
    _, context = admit(instance, case)
    attempt = case['attempt_id']
    with pytest.raises(ValueError):
        instance.handle_request(OPERATOR, void_request(case, context, private=Ed25519PrivateKey.generate()))
    with sqlite3.connect(instance.store.path) as connection:
        role = VOID_AUTHENTICATION_PREFIX + '000001'
        body = json.loads(connection.execute('SELECT body FROM full_campaign_objects WHERE attempt_id=? AND role=?', (attempt, role)).fetchone()[0])
        if damage == 'charge_amount':
            body['charge_cpu_ns'] = 1
            raw = encoded(body)
            connection.execute('UPDATE full_campaign_objects SET body=?,sha256=?,byte_length=? WHERE attempt_id=? AND role=?',
                               (raw, sha256(raw), len(raw), attempt, role))
        elif damage == 'refusal_orphan':
            connection.execute('DELETE FROM full_campaign_objects WHERE attempt_id=? AND role=?', (attempt, role))
        elif damage == 'funding_total':
            doc = json.loads(connection.execute('SELECT body FROM full_campaign_funding WHERE attempt_id=?', (attempt,)).fetchone()[0])
            doc['settled_cpu_ns'] -= CHARGE
            connection.execute('UPDATE full_campaign_funding SET body=? WHERE attempt_id=?', (encoded(doc), attempt))
        else:
            connection.execute("DELETE FROM full_campaign_objects WHERE attempt_id=? AND role='diagnostic_receipt'", (attempt,))
    with pytest.raises(ValueError):
        ExecutionStore(instance.store.path)


# --- Gap 4: safe exact-retry resume of a structurally absent RESERVED admission


def crash_after_begin_admission(instance, case, monkeypatch):
    """The service dies after begin_admission commits and before any start intent."""
    original = supervisor.run_campaign_work
    calls = []

    def dies(context, reservation, manifest):
        calls.append(manifest)
        raise RuntimeError('service died before the start intent')
    monkeypatch.setattr(supervisor, 'run_campaign_work', dies)
    with pytest.raises(RuntimeError):
        instance.handle_request(CLIENT, request(case))
    monkeypatch.setattr(supervisor, 'run_campaign_work', original)
    work = snapshot(instance, case)['works'][0]
    assert work['work_id'] == 'admission' and work['state'] == 'RESERVED' and work['transitions'] == []
    assert Runtime.started == [] and calls
    return work


def control_slots(instance, case):
    return objects(instance, case, 'supervision_control_')


def test_exact_retry_resumes_the_unstarted_admission_exactly_once(tmp_path, monkeypatch):
    instance, case = funded_service(tmp_path, monkeypatch)
    crash_after_begin_admission(instance, case, monkeypatch)
    assert control_slots(instance, case) == []
    resumed = json.loads(instance.handle_request(CLIENT, request(case)))
    assert resumed['schema'] == 'qualification_campaign_status/v2' and resumed['state'] == 'PROVISIONAL'
    assert Runtime.started == ['admission']
    work = snapshot(instance, case)['works'][0]
    assert work['state'] == 'START_INTENT'
    assert control_slots(instance, case) == ['supervision_control_' + sha256(encoded(['admission', 'START_OWNER']))]
    # A second identical retry is status only; changed bytes are refused.
    monkeypatch.setattr(supervisor, 'observe_campaign_clock', lambda: (_ for _ in ()).throw(AssertionError('resampled retry')))
    assert json.loads(instance.handle_request(CLIENT, request(case))) == resumed
    assert Runtime.started == ['admission']
    with pytest.raises(ValueError, match='differs'):
        instance.handle_request(CLIENT, request(case, request_id='other'))
    ExecutionStore(instance.store.path)


def test_restart_never_spends_the_recovery_slot_on_the_unstarted_admission(tmp_path, monkeypatch):
    instance, case = funded_service(tmp_path, monkeypatch)
    crash_after_begin_admission(instance, case, monkeypatch)
    attempt = case['attempt_id']
    for restart in range(2):
        restarted = fresh_service(instance)
        restarted.campaign_runtime = Runtime(restarted)
        restarted.recover_service()
        assert restarted.recovery_issues == {attempt + ':admission': 'ADMISSION_RESUMABLE'}
        state = snapshot(restarted, case)
        assert state['works'][0]['state'] == 'RESERVED' and state['recoveries'] == [] and state['state'] == 'PROVISIONAL'
        assert control_slots(restarted, case) == []
    # Base bytes: the first restart spent RECOVERY_OWNER, the second left a
    # permanent RECOVERY_PENDING barrier; here the exact retry still launches.
    resumed = json.loads(restarted.handle_request(CLIENT, request(case)))
    assert resumed['state'] == 'PROVISIONAL' and Runtime.started == ['admission']
    assert snapshot(restarted, case)['works'][0]['state'] == 'START_INTENT'
    ExecutionStore(instance.store.path)


@pytest.mark.parametrize('condition', ['void', 'deadline', 'boot', 'recovery_pending'])
def test_retry_never_launches_unless_the_admission_is_resumable(tmp_path, monkeypatch, condition):
    instance, case = funded_service(tmp_path, monkeypatch)
    crash_after_begin_admission(instance, case, monkeypatch)
    attempt = case['attempt_id']
    campaigns = CampaignStore(instance.store)
    if condition == 'void':
        campaigns.void(encoded(dict(schema='qualification_campaign_request/v2', operation='VOID', attempt_id=attempt,
                                    reason='stop', operator_approval_bytes='eA==')), now=NOW)
    elif condition == 'deadline':
        deadline = snapshot(instance, case)['deadline_boottime_ns']
        monkeypatch.setattr(supervisor, 'observe_campaign_clock', lambda: encoded(clock(deadline)))
    elif condition == 'boot':
        monkeypatch.setattr(supervisor, 'observe_campaign_clock', lambda: encoded(clock(12, boot='boot-2')))
    else:
        campaigns.claim_supervision_control(attempt, 'admission', 'RECOVERY_OWNER', encoded(clock(12)), recovery_owner_token=b'r' * 32)
    reply = json.loads(instance.handle_request(CLIENT, request(case)))
    assert reply['schema'] == 'qualification_campaign_status/v2'
    assert Runtime.started == [] and snapshot(instance, case)['works'][0]['state'] == 'RESERVED'
    assert 'supervision_control_' + sha256(encoded(['admission', 'START_OWNER'])) not in control_slots(instance, case)
    restarted = fresh_service(instance)
    restarted.campaign_runtime = Runtime(restarted)
    restarted.recover_service()
    label = restarted.recovery_issues.get(attempt + ':admission')
    if condition == 'recovery_pending':
        assert label == 'RECOVERY_PENDING'  # a legacy claim is not structurally absent; today's path
    else:
        assert label == 'ADMISSION_UNSTARTED'
        assert snapshot(restarted, case)['recoveries'] == []
    ExecutionStore(instance.store.path)


@pytest.mark.parametrize('condition', ['deadline', 'boot'])
def test_restart_terminalises_an_expired_unstarted_admission_without_a_slot(tmp_path, monkeypatch, condition):
    """Coordinator addendum (2): past the deadline or on another boot the budget ends honestly, ownerless and effect-free."""
    instance, case = funded_service(tmp_path, monkeypatch)
    crash_after_begin_admission(instance, case, monkeypatch)
    attempt = case['attempt_id']
    before = snapshot(instance, case)
    if condition == 'deadline':
        monkeypatch.setattr(supervisor, 'observe_campaign_clock', lambda: encoded(clock(before['deadline_boottime_ns'])))
    else:
        monkeypatch.setattr(supervisor, 'observe_campaign_clock', lambda: encoded(clock(12, boot='boot-2')))
    restarted = fresh_service(instance)
    restarted.campaign_runtime = Runtime(restarted)
    restarted.recover_service()
    assert restarted.recovery_issues == {attempt + ':admission': 'ADMISSION_UNSTARTED'}
    state = snapshot(restarted, case)
    assert state['state'] == ('BUDGET_EXHAUSTED' if condition == 'deadline' else 'BUDGET_UNCERTAIN')
    assert state['validity'] == 'VALID' and state['works'][0]['state'] == 'RESERVED' and state['works'][0]['transitions'] == []
    assert state['recoveries'] == [] and state['dispatches'] == [] and control_slots(restarted, case) == []
    assert state['settled_cpu_ns'] == before['settled_cpu_ns'] and state['reserved_cpu_ns'] == before['reserved_cpu_ns']
    assert Runtime.started == []
    # The exact retry is status only, and a second restart changes nothing further.
    reply = json.loads(restarted.handle_request(CLIENT, request(case)))
    assert reply['state'] == state['state'] and Runtime.started == []
    again = fresh_service(instance)
    again.campaign_runtime = Runtime(again)
    again.recover_service()
    assert again.recovery_issues == {attempt + ':admission': 'ADMISSION_UNSTARTED'}
    assert snapshot(again, case)['accounting_revision'] == state['accounting_revision']
    ExecutionStore(instance.store.path)


def test_concurrent_identical_retries_launch_once(tmp_path, monkeypatch):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier
    instance, case = funded_service(tmp_path, monkeypatch)
    crash_after_begin_admission(instance, case, monkeypatch)
    barrier = Barrier(2)

    def contender():
        barrier.wait()
        return json.loads(instance.handle_request(CLIENT, request(case)))
    with ThreadPoolExecutor(max_workers=2) as pool:
        replies = list(pool.map(lambda _: contender(), range(2)))
    assert all(reply['schema'] == 'qualification_campaign_status/v2' for reply in replies)
    assert Runtime.started == ['admission']
    assert snapshot(instance, case)['works'][0]['state'] == 'START_INTENT'
    assert len(control_slots(instance, case)) == 1


def test_resumed_launch_failure_takes_recovery_with_an_unspent_slot(tmp_path, monkeypatch):
    instance, case = funded_service(tmp_path, monkeypatch)
    crash_after_begin_admission(instance, case, monkeypatch)
    monkeypatch.setattr(Runtime, 'start', lambda self, state, work, enrollment: (_ for _ in ()).throw(OSError('launch failed')))
    with pytest.raises(OSError):
        instance.handle_request(CLIENT, request(case))
    state = snapshot(instance, case)
    assert state['works'][0]['state'] == 'IN_DOUBT' and state['state'] == 'IN_DOUBT'
    assert 'supervision_control_' + sha256(encoded(['admission', 'RECOVERY_OWNER'])) in control_slots(instance, case)
    assert json.loads(instance.handle_request(CLIENT, request(case)))['state'] == 'IN_DOUBT'
    ExecutionStore(instance.store.path)


# --- S2-G4: store-side invariants (A1, A5, A7) --------------------------------


def _retained_process_event(campaigns, attempt, work_id, pid, cgroup, *, t=14):
    """One retained alive-verified PROCESS identity, in whichever shape the
    installed parser accepts: G3 adds and requires the process image fields
    (comm/exe); a pre-G3 parser whitelists them away. The A5 store rule reads
    only the cgroup, so either shape proves the same thing."""
    base = dict(pid=pid, start_ticks=1, uid=1001, cgroup=cgroup)
    for image in (dict(comm='python', exe='/opt/ops/bin/python'), {}):
        try:
            campaigns.retain_supervision_event(encoded(dict(
                schema='qualification_campaign_supervision_event/v1', attempt_id=attempt,
                work_id=work_id, kind='PROCESS', clock=clock(t), data=dict(base, **image))))
            return
        except ValueError:
            continue
    raise AssertionError('no accepted PROCESS event shape on this tree')


def _reserve_and_start(campaigns, attempt, work_id, limits):
    campaigns.reserve_work(attempt, work_id, 'N1_G5',
        encoded(dict(limits=limits, clock=clock(13), input_sha256='e' * 64)),
        expected_revision=json.loads(campaigns.budget_snapshot(attempt))['authority_revision'])
    scopes = supervisor.work_enrollment('host1', attempt, work_id)
    campaigns.record_work_transition(attempt, work_id, encoded(dict(
        schema='qualification_campaign_work_transition/v1', attempt_id=attempt, work_id=work_id,
        state='START_INTENT', clock=clock(14),
        data=dict(campaign_scope_id=scopes['campaign_slice'], work_scope_id=scopes['payload_slice']))),
        expected_revision=json.loads(campaigns.budget_snapshot(attempt))['authority_revision'])
    return scopes


def test_void_queued_in_the_dispatch_window_is_refused_then_recorded_after_terminalisation(tmp_path, monkeypatch):
    """PR #436 review A1, end to end: a legitimate VOID that lands while a dispatch
    row is unacknowledged is refused (the window closes), the pending-cancellation
    barrier terminalises the started work, and the exact retry authenticates once
    uncharged on the terminal-but-VALID campaign and records the VOID."""
    instance, case = funded_service(tmp_path, monkeypatch)
    _, context = admit(instance, case)
    attempt = case['attempt_id']
    campaigns = CampaignStore(instance.store)
    limits = snapshot(instance, case)['profile']['phases']['N1_G5']
    _reserve_and_start(campaigns, attempt, 'work', limits)
    valid = void_request(case, context)
    with campaigns.launch_gate(attempt, 'work', lambda: encoded(clock(15))) as gate:
        refused = json.loads(instance.handle_request(OPERATOR, valid))
        assert refused['void_pending'] is True and refused['validity'] == 'VALID'
        assert refused['void_authentication_attempts'] == 0
        assert funding(instance, case)['settled_cpu_ns'] == ADMISSION_CHARGE  # nothing charged in the window
    campaigns.acknowledge_dispatch(attempt, 'work', 'payload', gate['token'], lambda: encoded(clock(16)))
    # The queued body's barrier fails the started work's next positive step; the
    # guardian's failure shape is the negative IN_DOUBT transition.
    state = json.loads(campaigns.record_work_transition(attempt, 'work', encoded(dict(
        schema='qualification_campaign_work_transition/v1', attempt_id=attempt, work_id='work',
        state='IN_DOUBT', clock=clock(17), data={})),
        expected_revision=json.loads(campaigns.budget_snapshot(attempt))['authority_revision']))
    assert state['state'] == 'IN_DOUBT' and state['validity'] == 'VALID'
    receipt = json.loads(instance.handle_request(OPERATOR, valid))
    assert receipt['validity'] == 'VOID'
    current = status(instance, case)
    assert current['void_pending'] is False and current['void_authentication_attempts'] == 0
    assert objects(instance, case, VOID_AUTHENTICATION_PREFIX) == []       # the terminal attempt is uncharged
    assert objects(instance, case, VOID_TERMINAL_REFUSAL_PREFIX) == []     # and it verified
    assert objects(instance, case, 'pending_void') == []
    assert funding(instance, case)['settled_cpu_ns'] == ADMISSION_CHARGE
    assert campaigns.void_retry(valid) is not None
    ExecutionStore(instance.store.path)


def test_forged_body_on_a_terminal_campaign_is_refused_once_uncharged_and_never_requeued(tmp_path, monkeypatch):
    """A forged body queued on a terminal-but-VALID campaign gets exactly one
    uncharged attempt: the refusal is retained by body digest, the body is
    cleared, the campaign stays VALID, and the same digest can never be queued
    again -- while a distinct body gets its own single attempt."""
    instance, case = funded_service(tmp_path, monkeypatch)
    _, context = admit(instance, case)
    attempt = case['attempt_id']
    campaigns = CampaignStore(instance.store)
    limits = snapshot(instance, case)['profile']['phases']['N1_G5']
    campaigns.reserve_work(attempt, 'reserved', 'N1_G5',
        encoded(dict(limits=limits, clock=clock(13), input_sha256='e' * 64)),
        expected_revision=snapshot(instance, case)['authority_revision'])
    forged = void_request(case, context, private=Ed25519PrivateKey.generate())
    campaigns.queue_diagnostic_void(forged)
    state = json.loads(campaigns.record_work_transition(attempt, 'reserved', encoded(dict(
        schema='qualification_campaign_work_transition/v1', attempt_id=attempt, work_id='reserved',
        state='ABORTED', clock=clock(16), data={})),
        expected_revision=snapshot(instance, case)['authority_revision']))
    assert state['state'] == 'ABORTED' and state['validity'] == 'VALID'
    with pytest.raises(ValueError):  # one uncharged attempt: verified, refused, retained, cleared
        instance.handle_request(OPERATOR, forged)
    current = status(instance, case)
    assert current['validity'] == 'VALID' and current['void_pending'] is False
    assert objects(instance, case, VOID_AUTHENTICATION_PREFIX) == []
    assert objects(instance, case, VOID_TERMINAL_REFUSAL_PREFIX) == [
        VOID_TERMINAL_REFUSAL_PREFIX + sha256(forged)]
    refusal = json.loads(campaigns.retained_object(attempt, VOID_TERMINAL_REFUSAL_PREFIX + sha256(forged)))
    assert refusal['sequence'] == 1 and refusal['request_sha256'] == sha256(forged)
    assert funding(instance, case)['settled_cpu_ns'] == ADMISSION_CHARGE
    # The same digest is never re-queued on this campaign ...
    with pytest.raises(ValueError, match='already refused on the terminal campaign'):
        instance.handle_request(OPERATOR, forged)
    # ... a distinct body gets its own single uncharged attempt (a valid one).
    other = json.loads(instance.handle_request(OPERATOR, void_request(case, context, reason='other')))
    assert other['validity'] == 'VOID'
    assert len(objects(instance, case, VOID_TERMINAL_REFUSAL_PREFIX)) == 1
    ExecutionStore(instance.store.path)  # the digest-keyed refusal reopens clean


def test_terminal_refusal_tampering_is_rejected_on_reopen(tmp_path, monkeypatch):
    """The digest-keyed terminal refusals are integrity-checked: a body whose
    request digest no longer matches its role, or a broken sequence, is refused
    when the journal reopens."""
    import sqlite3
    instance, case = funded_service(tmp_path, monkeypatch)
    _, context = admit(instance, case)
    attempt = case['attempt_id']
    campaigns = CampaignStore(instance.store)
    limits = snapshot(instance, case)['profile']['phases']['N1_G5']
    campaigns.reserve_work(attempt, 'reserved', 'N1_G5',
        encoded(dict(limits=limits, clock=clock(13), input_sha256='e' * 64)),
        expected_revision=snapshot(instance, case)['authority_revision'])
    forged = void_request(case, context, private=Ed25519PrivateKey.generate())
    campaigns.queue_diagnostic_void(forged)
    campaigns.record_work_transition(attempt, 'reserved', encoded(dict(
        schema='qualification_campaign_work_transition/v1', attempt_id=attempt, work_id='reserved',
        state='ABORTED', clock=clock(16), data={})),
        expected_revision=snapshot(instance, case)['authority_revision'])
    with pytest.raises(ValueError):
        instance.handle_request(OPERATOR, forged)
    role = VOID_TERMINAL_REFUSAL_PREFIX + sha256(forged)
    saved = json.loads(campaigns.retained_object(attempt, role))
    tampered = encoded(dict(saved, request_sha256='f' * 64))
    connection = sqlite3.connect(instance.store.path)
    connection.execute('UPDATE full_campaign_objects SET body=? WHERE attempt_id=? AND role=?',
                       (tampered, attempt, role))
    connection.commit()
    connection.close()
    with pytest.raises(ValueError, match='terminal cancellation refusal binding differs'):
        CampaignStore(ExecutionStore(instance.store.path))


def test_charged_authentications_bound_reserve_work_to_one_allowance_view(tmp_path, monkeypatch):
    """S2-G4 A7: the snapshot's remaining is pre-charge; after N charged
    authentication attempts a reservation that still fits the snapshot but not
    the projection's remaining is refused and terminalises the campaign."""
    # Contract budget 1345 s: admission 20 s, ten 120 s drain phases, 125 s left.
    instance, case = funded_service(tmp_path, monkeypatch, budget_seconds=1345)
    _, context = admit(instance, case)
    assert drain(instance, case, keep_ns=125 * 10**9) == 125 * 10**9
    forged = void_request(case, context, private=Ed25519PrivateKey.generate())
    for _ in range(3):  # 3 x 2 s charged: the projection holds 119 s, the snapshot 125 s
        with pytest.raises(ValueError):
            instance.handle_request(OPERATOR, forged)
    campaigns = CampaignStore(instance.store)
    limits = snapshot(instance, case)['profile']['phases']['N1_G5']
    assert snapshot(instance, case)['remaining_cpu_ns'] == 125 * 10**9  # pre-charge view
    state = json.loads(campaigns.reserve_work(case['attempt_id'], 'overdraft', 'N1_G5',
        encoded(dict(limits=limits, clock=clock(14), input_sha256='f' * 64)),
        expected_revision=snapshot(instance, case)['authority_revision']))
    # A 120 s phase fits the snapshot's 125 s but not the projection's 119 s:
    # refused (terminal), and the reservation was not granted.
    assert state['state'] == 'BUDGET_EXHAUSTED'
    assert all(w['work_id'] != 'overdraft' for w in state['works'])
    assert funding(instance, case)['remaining_cpu_ns'] == 119 * 10**9  # the authoritative view
    ExecutionStore(instance.store.path)


def test_credit_requires_a_retained_payload_scope_identity_store_side(tmp_path, monkeypatch):
    """S2-G4 A5: on a funded campaign, CAPTURED/SIGNING_INTENT/COMPLETED require
    a retained alive-verified PROCESS identity inside the work's enrolled
    payload slice; the guardian's own identity (outside it) never counts."""
    instance, case = funded_service(tmp_path, monkeypatch)
    _, context = admit(instance, case)
    attempt = case['attempt_id']
    campaigns = CampaignStore(instance.store)
    limits = snapshot(instance, case)['profile']['phases']['N1_G5']
    scopes = _reserve_and_start(campaigns, attempt, 'probe', limits)
    campaigns.record_work_transition(attempt, 'probe', encoded(dict(
        schema='qualification_campaign_work_transition/v1', attempt_id=attempt, work_id='probe',
        state='RUNNING', clock=clock(15), data={})),
        expected_revision=json.loads(campaigns.budget_snapshot(attempt))['authority_revision'])
    manifest = encoded(dict(schema='qualification_campaign_work_manifest/v1', attempt_id=attempt,
        work_id='probe', role='probe_g5', probe='noop'))
    campaigns.retain_supervision(attempt, 'probe', encoded(dict(
        schema='qualification_campaign_supervision/v1', host_run_id='host1', attempt_id=attempt,
        work_id='probe', manifest_bytes_b64=base64.b64encode(manifest).decode('ascii'), scopes=scopes)))
    revision = json.loads(campaigns.budget_snapshot(attempt))['authority_revision']

    def capture():
        return campaigns.record_work_transition(attempt, 'probe', encoded(dict(
            schema='qualification_campaign_work_transition/v1', attempt_id=attempt, work_id='probe',
            state='CAPTURED', clock=clock(16), data={})), expected_revision=revision)
    # No identity at all: refused.
    with pytest.raises(ValueError, match='alive-verified payload identity required'):
        capture()
    # The guardian's own PROCESS identity is outside the payload slice: refused.
    _retained_process_event(campaigns, attempt, 'probe', 9999, scopes['guardian_unit'])
    with pytest.raises(ValueError, match='alive-verified payload identity required'):
        capture()
    # A payload-scope identity opens the credit path, and the journal reopens clean.
    _retained_process_event(campaigns, attempt, 'probe', 4242,
        scopes['payload_slice'] + '/docker-' + 'f' * 64 + '.scope')
    state = json.loads(capture())
    assert next(w for w in state['works'] if w['work_id'] == 'probe')['state'] == 'CAPTURED'
    ExecutionStore(instance.store.path)


def test_integrity_refuses_credited_work_whose_payload_identity_was_removed(tmp_path, monkeypatch):
    """S2-G4 A5 walk: a credited work whose payload-scope PROCESS events are gone
    (a tampered journal) is refused when the journal reopens."""
    import sqlite3
    instance, case = funded_service(tmp_path, monkeypatch)
    _, context = admit(instance, case)
    attempt = case['attempt_id']
    campaigns = CampaignStore(instance.store)
    limits = snapshot(instance, case)['profile']['phases']['N1_G5']
    scopes = _reserve_and_start(campaigns, attempt, 'probe', limits)
    campaigns.record_work_transition(attempt, 'probe', encoded(dict(
        schema='qualification_campaign_work_transition/v1', attempt_id=attempt, work_id='probe',
        state='RUNNING', clock=clock(15), data={})),
        expected_revision=json.loads(campaigns.budget_snapshot(attempt))['authority_revision'])
    manifest = encoded(dict(schema='qualification_campaign_work_manifest/v1', attempt_id=attempt,
        work_id='probe', role='probe_g5', probe='noop'))
    campaigns.retain_supervision(attempt, 'probe', encoded(dict(
        schema='qualification_campaign_supervision/v1', host_run_id='host1', attempt_id=attempt,
        work_id='probe', manifest_bytes_b64=base64.b64encode(manifest).decode('ascii'), scopes=scopes)))
    _retained_process_event(campaigns, attempt, 'probe', 4242,
        scopes['payload_slice'] + '/docker-' + 'f' * 64 + '.scope')
    state = json.loads(campaigns.record_work_transition(attempt, 'probe', encoded(dict(
        schema='qualification_campaign_work_transition/v1', attempt_id=attempt, work_id='probe',
        state='CAPTURED', clock=clock(16), data={})),
        expected_revision=json.loads(campaigns.budget_snapshot(attempt))['authority_revision']))
    assert next(w for w in state['works'] if w['work_id'] == 'probe')['state'] == 'CAPTURED'
    ExecutionStore(instance.store.path)  # clean while the identity is retained
    connection = sqlite3.connect(instance.store.path)
    connection.execute("DELETE FROM full_campaign_objects WHERE attempt_id=? AND role GLOB 'supervision_event_*'",
                       (attempt,))
    connection.commit()
    connection.close()
    with pytest.raises(ValueError, match='credited work lacks alive-verified payload identity'):
        CampaignStore(ExecutionStore(instance.store.path))
