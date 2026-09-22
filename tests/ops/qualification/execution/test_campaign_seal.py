"""S7 separate seal authority and atomic publication -- tests-first draft.

Defines S7's Windows acceptance against the frozen §1 interfaces BEFORE the
modules exist (the coordinator's tests-first ruling): every case carries a
reason string. Until campaign_seal.py / seal_service.py land, this file fails
at collection (the S6 fail-on-base pattern). The qseal IPC is doubled on
Windows exactly as the F1 double stands in for the service seam; the real
Unix-socket process separation is the Linux acceptance file's evidence.

The seal intent schema frozen by these tests:
qualification_campaign_seal_intent/v1 = {schema, attempt_id, intent_id,
result_sha256, authentication_sha256, result_receipt_sha256, release_sha256,
domain_sha256, key_id, signing_at_utc}.
"""
import base64
import json
from datetime import datetime, timezone

import pytest
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution import campaign_result
from c1_rail.qualification.execution import campaign_seal
from c1_rail.qualification.execution import seal_service
from c1_rail.qualification.execution.campaign_seal import SEAL_OPERATIONS
from c1_rail.qualification.execution.protocol import sha256

from result_fixture import G5_UID, scene, sign_candidate
from test_campaign_result_commit import prepared

NOW = datetime(2026, 9, 21, tzinfo=timezone.utc)
SEAL_KEY = 'test-seal'


def committed_pass(tmp_path, monkeypatch):
    """The seal-eligible base: a committed five-stage PASS with its bytes."""
    instance, double, snapshot, candidate, authentication, request = prepared(
        tmp_path, monkeypatch, n1_decision='CONTINUE', through='PART_A')
    response = json.loads(double.handle_result_request(G5_UID, request))
    assert response['receipt']['outcome'] == 'PASS'
    receipt_bytes, _, validity = double.results.result_receipt(instance.attempt)
    assert validity == 'VALID'
    return instance, double, candidate, authentication, receipt_bytes


def seal_intent(attempt, *, result_bytes, authentication_bytes, receipt_bytes,
                key_id=SEAL_KEY, signing_at='2026-09-21T03:00:00Z',
                release_sha256='3' * 64, domain_sha256='2' * 64):
    return encoded(dict(schema='qualification_campaign_seal_intent/v1',
        attempt_id=attempt, intent_id=attempt + '-seal',
        result_sha256=sha256(result_bytes),
        authentication_sha256=sha256(authentication_bytes),
        result_receipt_sha256=sha256(receipt_bytes),
        release_sha256=release_sha256, domain_sha256=domain_sha256, key_id=key_id,
        signing_at_utc=signing_at))


def seal_eligible_scene(tmp_path, monkeypatch):
    """committed_pass plus the SEAL reservation (with the guardian's real
    start transition) driven to RUNNING, and the durable T1 intent (the
    intent binds the live release/domain digests, as request_seal builds it)."""
    from result_fixture import result_context
    instance, double, result_bytes, authentication, receipt_bytes = committed_pass(
        tmp_path, monkeypatch)
    seals = campaign_seal.SealStore(double.campaigns)
    state = json.loads(double.results.result_state_bytes(instance.attempt))
    from c1_rail.qualification.execution import campaign_supervisor as supervisor
    clock_doc = json.loads(supervisor.observe_campaign_clock())
    reservation = encoded(dict(limits=state['profile']['phases']['SEAL'],
                               clock=clock_doc, input_sha256=sha256(b'seal-input')))
    scopes = supervisor.work_enrollment('host1', instance.attempt, 'swork')
    start = encoded(dict(schema='qualification_campaign_work_transition/v1',
        attempt_id=instance.attempt, work_id='swork', state='START_INTENT',
        clock=clock_doc, data=dict(campaign_scope_id=scopes['campaign_slice'],
                                   work_scope_id=scopes['payload_slice'])))
    seals.reserve_seal_work(instance.attempt, 'swork', reservation,
                            expected_revision=state['authority_revision'],
                            start_transition_bytes=start)
    state = json.loads(seals.result_state_bytes(instance.attempt))
    running = encoded(dict(schema='qualification_campaign_work_transition/v1',
        attempt_id=instance.attempt, work_id='swork', state='RUNNING',
        clock=clock_doc, data={}))
    seals.record_result_transition(instance.attempt, 'swork', running,
                                   expected_revision=state['authority_revision'])
    context = result_context(double, instance.attempt)
    intent = seal_intent(instance.attempt, result_bytes=result_bytes,
                         authentication_bytes=authentication,
                         receipt_bytes=receipt_bytes,
                         release_sha256=sha256(double.instance.release),
                         domain_sha256=context.domain.sha256)
    return instance, double, seals, intent, result_bytes, authentication, receipt_bytes


def seal_unit_scene(tmp_path, monkeypatch):
    """seal_eligible_scene with the qseal work's supervision facts: the
    enrollment and one alive payload-scope PROCESS identity, exactly as the
    guardian retains them for the unit."""
    instance, double, seals, intent, result_bytes, authentication, receipt = (
        seal_eligible_scene(tmp_path, monkeypatch))
    from c1_rail.qualification.execution import campaign_supervisor as supervisor
    scopes = supervisor.work_enrollment('host1', instance.attempt, 'swork')
    seals.retain_result_enrollment(encoded(dict(
        schema='qualification_campaign_supervision/v1', host_run_id='host1',
        attempt_id=instance.attempt, work_id='swork',
        manifest_bytes_b64=base64.b64encode(encoded(dict(
            # The manifest role WORK_ROLES knows at this revision for the
            # qseal unit; the seam registers 'seal' beside it.
            schema='qualification_campaign_work_manifest/v1',
            attempt_id=instance.attempt, work_id='swork', role='probe_seal',
            probe='noop'))).decode('ascii'),
        scopes=scopes)))
    seals.retain_result_supervision_event(encoded(dict(
        schema='qualification_campaign_supervision_event/v2',
        attempt_id=instance.attempt, work_id='swork', kind='PROCESS',
        clock=json.loads(supervisor.observe_campaign_clock()),
        data=dict(pid=4243, start_ticks=99, uid=7,
                  cgroup='/fpq/' + scopes['payload_slice'] + '/payload-scope',
                  comm='fpq-armed', exe=''))))
    return instance, double, seals, intent, result_bytes, authentication, receipt


def sign_like_qseal(double, intent, result_bytes, authentication, receipt_bytes):
    """The Windows stand-in for the qseal process body: the REAL signer over a
    fixture credential (the module's Linux-only credential loader doubled)."""
    keys = double.keys()
    private = double.instance.case['private'][SEAL_KEY]
    return seal_service.sign_committed_pass(
        intent, result_bytes, authentication, receipt_bytes,
        credential_root='fixture://test-seal', current_keys=keys,
        _loader=lambda reference: (SEAL_KEY, 'TEST_ONLY', private))


def test_pass_only_eligibility(tmp_path, monkeypatch):
    """Only a committed PASS with current validity reaches qseal; a FAIL, an
    uncommitted result and VOID campaigns refuse with reason strings."""
    instance, double, snapshot, candidate, authentication, request = prepared(
        tmp_path, monkeypatch, n1_decision='FAILURE')
    json.loads(double.handle_result_request(G5_UID, request))
    assert double.results.seal_eligibility(instance.attempt)['reason'] ==         'committed FAIL outcome is never sealed'
    with pytest.raises(ValueError, match='committed FAIL outcome is never sealed'):
        campaign_seal.request_seal(double, instance.attempt)
    instance2, double2, result_bytes, authentication, receipt = committed_pass(
        tmp_path / 'second', monkeypatch)
    seals = campaign_seal.SealStore(double2.campaigns)
    intent = seal_intent(instance2.attempt, result_bytes=result_bytes,
                         authentication_bytes=authentication, receipt_bytes=receipt)
    with pytest.raises(ValueError, match='SEAL reservation required'):
        seals.prepare_seal_intent(instance2.attempt, intent,
                                  expected_revision=json.loads(
                                      double2.results.result_state_bytes(instance2.attempt)
                                  )['authority_revision'])


def test_qseal_recomputes_pass_and_binds_every_digest(tmp_path, monkeypatch):
    """sign_committed_pass independently re-parses the result (outcome PASS,
    all five stages PASS), verifies the G5 authentication and the service
    receipt, and binds exactly the intent's digests -- a caller-supplied PASS
    is never accepted and there is no publication path in the module."""
    instance, double, seals, intent, result_bytes, authentication, receipt = seal_eligible_scene(
        tmp_path, monkeypatch)
    signature = sign_like_qseal(double, intent, result_bytes, authentication, receipt)
    assert json.loads(signature)['schema'] == 'qualification_campaign_seal/v1'
    tampered = json.loads(result_bytes)
    tampered['outcome'] = 'FAIL'
    tampered['stages'][-1]['status'] = 'FAIL'
    tampered['checkpoints'][-1]['decision'] = 'FAIL'
    with pytest.raises(ValueError, match='committed PASS result required'):
        sign_like_qseal(double, intent, encoded(tampered), authentication, receipt)
    with pytest.raises(ValueError, match='seal intent binding differs'):
        sign_like_qseal(double, seal_intent(instance.attempt, result_bytes=result_bytes,
                                            authentication_bytes=authentication,
                                            receipt_bytes=receipt + b' '),
                        result_bytes, authentication, receipt)


def test_wrong_role_result_or_domain_refuses(tmp_path, monkeypatch):
    instance, double, seals, intent, result_bytes, authentication, receipt = seal_eligible_scene(
        tmp_path, monkeypatch)
    # The domain reference lives with the service's enrollment context (seam
    # #19), so the wrong-domain intent is refused by the service-side
    # enrollment check the signing phase rechecks before publication.
    from result_fixture import result_context
    other_domain = json.loads(seal_intent(instance.attempt, result_bytes=result_bytes,
        authentication_bytes=authentication, receipt_bytes=receipt))
    other_domain['domain_sha256'] = '9' * 64
    with pytest.raises(ValueError, match='seal intent domain differs'):
        campaign_seal.verify_seal_intent(encoded(other_domain),
                                         result_context(double, instance.attempt),
                                         double.instance.release)
    wrong_key = json.loads(intent)
    wrong_key['key_id'] = 'test-producer'
    with pytest.raises(ValueError, match='seal key is not enrolled for sealing'):
        sign_like_qseal(double, encoded(wrong_key), result_bytes, authentication, receipt)


def test_altered_intent_after_t1_refuses_the_commit(tmp_path, monkeypatch):
    instance, double, seals, intent, result_bytes, authentication, receipt = seal_eligible_scene(
        tmp_path, monkeypatch)
    revision = json.loads(double.results.result_state_bytes(instance.attempt))['authority_revision']
    seals.prepare_seal_intent(instance.attempt, intent, expected_revision=revision)
    altered = json.loads(intent)
    altered['signing_at_utc'] = '2026-09-21T04:00:00Z'
    signature = sign_like_qseal(double, intent, result_bytes, authentication, receipt)
    with pytest.raises(ValueError, match='exact seal intent retry required'):
        seals.commit_campaign_seal(instance.attempt, encoded(altered), signature, now=NOW)


def test_expired_or_revoked_seal_key_refuses(tmp_path, monkeypatch):
    instance, double, seals, intent, result_bytes, authentication, receipt = seal_eligible_scene(
        tmp_path, monkeypatch)
    from dataclasses import replace
    keys = dict(double.keys())
    revoked = dict(keys)
    revoked[SEAL_KEY] = replace(keys[SEAL_KEY], revoked_at=datetime(2026, 9, 20, tzinfo=timezone.utc))
    monkeypatch.setattr(double, 'keys', lambda: revoked)
    with pytest.raises(ValueError, match='seal key is revoked'):
        seal_service.sign_committed_pass(
            intent, result_bytes, authentication, receipt,
            credential_root='fixture://test-seal', current_keys=revoked,
            _loader=lambda reference: (SEAL_KEY, 'TEST_ONLY',
                                       double.instance.case['private'][SEAL_KEY]))


def test_lost_signing_response_recovers_exactly(tmp_path, monkeypatch):
    instance, double, seals, intent, result_bytes, authentication, receipt = seal_eligible_scene(
        tmp_path, monkeypatch)
    revision = json.loads(double.results.result_state_bytes(instance.attempt))['authority_revision']
    seals.prepare_seal_intent(instance.attempt, intent, expected_revision=revision)
    signature = sign_like_qseal(double, intent, result_bytes, authentication, receipt)
    first = json.loads(seals.commit_campaign_seal(instance.attempt, intent, signature, now=NOW))
    again = json.loads(seals.commit_campaign_seal(instance.attempt, intent, signature, now=NOW))
    assert again['receipt'] == first['receipt'] and again['historical'] is True
    assert again['receipt']['signing_at_utc'] == json.loads(intent)['signing_at_utc']


def test_void_orderings_against_the_seal(tmp_path, monkeypatch):
    instance, double, seals, intent, result_bytes, authentication, receipt = seal_eligible_scene(
        tmp_path, monkeypatch)
    revision = json.loads(double.results.result_state_bytes(instance.attempt))['authority_revision']
    seals.prepare_seal_intent(instance.attempt, intent, expected_revision=revision)
    with instance.store.transaction() as connection:
        connection.execute("UPDATE full_campaigns SET validity='VOID' WHERE attempt_id=?",
                           (instance.attempt,))
    signature = sign_like_qseal(double, intent, result_bytes, authentication, receipt)
    with pytest.raises(ValueError, match='VOID campaign'):
        seals.commit_campaign_seal(instance.attempt, intent, signature, now=NOW)
    # Publication first, VOID second: exact receipt recovery with flipped
    # current validity and truthful eligibility.
    instance2, double2, seals2, intent2, rb2, ab2, rec2 = seal_eligible_scene(
        tmp_path / 'second', monkeypatch)
    rev2 = json.loads(double2.results.result_state_bytes(instance2.attempt))['authority_revision']
    seals2.prepare_seal_intent(instance2.attempt, intent2, expected_revision=rev2)
    signature2 = sign_like_qseal(double2, intent2, rb2, ab2, rec2)
    json.loads(seals2.commit_campaign_seal(instance2.attempt, intent2, signature2, now=NOW))
    with instance2.store.transaction() as connection:
        connection.execute("UPDATE full_campaigns SET validity='VOID' WHERE attempt_id=?",
                           (instance2.attempt,))
    receipt_bytes, historical, validity, eligibility = seals2.seal_receipt(instance2.attempt)
    assert historical is True and validity == 'VOID' and eligibility['eligible'] is False


def test_no_alternate_candidate_publication_path(tmp_path, monkeypatch):
    """Only commit_campaign_seal publishes; a different signature under the
    persisted intent refuses, and inspect_seal never confers authority."""
    instance, double, seals, intent, result_bytes, authentication, receipt = seal_eligible_scene(
        tmp_path, monkeypatch)
    revision = json.loads(double.results.result_state_bytes(instance.attempt))['authority_revision']
    seals.prepare_seal_intent(instance.attempt, intent, expected_revision=revision)
    signature = sign_like_qseal(double, intent, result_bytes, authentication, receipt)
    json.loads(seals.commit_campaign_seal(instance.attempt, intent, signature, now=NOW))
    forged = encoded(dict(json.loads(signature), signature=dict(
        algorithm='Ed25519', key_id=SEAL_KEY, value_b64=base64.b64encode(b'x' * 64).decode())))
    with pytest.raises(ValueError, match='exact seal signature retry required'):
        seals.commit_campaign_seal(instance.attempt, intent, forged, now=NOW)
    view = json.loads(campaign_seal.inspect_seal(double.campaigns, instance.attempt))
    assert view['receipt']['schema'] == 'qualification_campaign_seal_receipt/v1'
    assert view['current_validity'] == 'VALID'


def test_signing_failure_rolls_back_publication_not_the_intent(tmp_path, monkeypatch):
    instance, double, seals, intent, result_bytes, authentication, receipt = seal_eligible_scene(
        tmp_path, monkeypatch)
    revision = json.loads(double.results.result_state_bytes(instance.attempt))['authority_revision']
    seals.prepare_seal_intent(instance.attempt, intent, expected_revision=revision)
    def broken_loader(reference):
        raise ValueError('qseal credential unavailable')
    with pytest.raises(ValueError, match='qseal credential unavailable'):
        seal_service.sign_committed_pass(intent, result_bytes, authentication, receipt,
            credential_root='fixture://test-seal', current_keys=double.keys(),
            _loader=broken_loader)
    with pytest.raises(ValueError, match='no committed campaign seal'):
        seals.seal_receipt(instance.attempt)
    # The durable intent survives for the exact retry.
    signature = sign_like_qseal(double, intent, result_bytes, authentication, receipt)
    json.loads(seals.commit_campaign_seal(instance.attempt, intent, signature, now=NOW))


def test_seal_operations_shape():
    assert SEAL_OPERATIONS == ('REQUEST_SEAL', 'INSPECT_SEAL')
    good = encoded(dict(schema='qualification_campaign_request/v2',
                        operation='REQUEST_SEAL', attempt_id='a1'))
    assert campaign_seal.parse_seal_operation(good)['operation'] == 'REQUEST_SEAL'
    with pytest.raises(ValueError, match='UNKNOWN_OPERATION'):
        campaign_seal.parse_seal_operation(encoded(dict(
            schema='qualification_campaign_request/v2', operation='SIGN_COMMITTED_PASS',
            attempt_id='a1')))


def test_committed_seal_work_settles_within_budget_and_completes(tmp_path, monkeypatch):
    """The committing SEAL work settles after T2 and completes in the state
    its own commit produced (S3's a8a983e rule, PR #455 review, carried to
    T05): SEALED_PASS once the enum seam lands; on frozen bytes the budget
    snapshot keeps the statistical predecessor N2_READY."""
    from result_fixture import complete_phase_work, settle_phase_work
    instance, double, seals, intent, result_bytes, authentication, receipt = (
        seal_unit_scene(tmp_path, monkeypatch))
    revision = json.loads(seals.result_state_bytes(instance.attempt))['authority_revision']
    seals.prepare_seal_intent(instance.attempt, intent, expected_revision=revision)
    signature = sign_like_qseal(double, intent, result_bytes, authentication, receipt)
    json.loads(seals.commit_campaign_seal(instance.attempt, intent, signature, now=NOW))
    state = settle_phase_work(seals, instance.attempt, 'swork', 'SEAL')
    assert state['state'] == 'N2_READY'
    state = complete_phase_work(seals, instance.attempt, 'swork')
    assert state['state'] == 'N2_READY'
    assert next(w for w in state['works'] if w['work_id'] == 'swork')['state'] == 'COMPLETED'
    view = json.loads(campaign_seal.inspect_seal(double.campaigns, instance.attempt))
    assert view['seal_state'] == 'SEALED' and view['receipt'] is not None


def test_committed_seal_overrun_blocks_the_sealed_pass(tmp_path, monkeypatch):
    """An overrun observed when the qseal work settles after T2 permanently
    blocks authority (spec 2.5 via S3's a8a983e): SEALED_PASS becomes
    BUDGET_EXHAUSTED, the committing work cannot complete, no new SEAL
    reservation is granted, and the seal receipt survives as history."""
    from c1_rail.qualification.execution import campaign_supervisor as supervisor
    from result_fixture import complete_phase_work, settle_phase_work
    instance, double, seals, intent, result_bytes, authentication, receipt = (
        seal_unit_scene(tmp_path, monkeypatch))
    revision = json.loads(seals.result_state_bytes(instance.attempt))['authority_revision']
    seals.prepare_seal_intent(instance.attempt, intent, expected_revision=revision)
    signature = sign_like_qseal(double, intent, result_bytes, authentication, receipt)
    first = json.loads(seals.commit_campaign_seal(instance.attempt, intent, signature,
                                                  now=NOW))
    limit = next(w for w in json.loads(
        seals.result_state_bytes(instance.attempt))['works']
        if w['work_id'] == 'swork')['limits']['cpu_ns']
    state = settle_phase_work(seals, instance.attempt, 'swork', 'SEAL', cpu=limit + 1)
    assert state['state'] == 'BUDGET_EXHAUSTED'
    with pytest.raises(ValueError, match='terminal campaign budget'):
        complete_phase_work(seals, instance.attempt, 'swork')
    retry = json.loads(seals.commit_campaign_seal(instance.attempt, intent, signature,
                                                  now=NOW))
    assert retry['receipt'] == first['receipt'] and retry['historical'] is True
    assert seals.seal_eligibility(instance.attempt) == dict(
        eligible=False, reason='BUDGET_EXHAUSTED', state='BUDGET_EXHAUSTED')
    # The ended authority grants no new SEAL reservation.
    state = json.loads(seals.result_state_bytes(instance.attempt))
    reservation = encoded(dict(limits=state['profile']['phases']['SEAL'],
                               clock=json.loads(supervisor.observe_campaign_clock()),
                               input_sha256=sha256(b'seal-input-2')))
    with pytest.raises(ValueError, match='seal predecessor refuses: BUDGET_EXHAUSTED'):
        seals.reserve_seal_work(instance.attempt, 'swork2', reservation,
                                expected_revision=state['authority_revision'])
