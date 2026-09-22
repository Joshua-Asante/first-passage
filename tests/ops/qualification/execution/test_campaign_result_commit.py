"""S6 authenticated full-result construction and atomic commit.

Real SQLite journals and real admitted campaigns (the S3 scene, imported --
never edited); the F3 successors are the fixture's synthetic-predecessor rows,
labelled ``synthetic_predecessor=True`` (result_fixture). Windows exercises
the modules through the F1 service double; the Linux unit/separation evidence
lives in tests/integration/qualification_boundary/test_campaign_result_seal_linux.py.

Ported legacy regressions are cited by their legacy test names (PR415):
test_partial_and_nonpass_results_never_seal, test_void_before_seal_survives_restart,
test_seal_retry_and_history_survive_restart_and_void, test_historical_complete_pass_
signatures_inspect_but_active_authority_is_retired, test_later_stage_evidence_after_
failure_is_refused, test_n1_terminal_prefix_needs_no_later_draws.
"""
import base64
import json
from dataclasses import replace
from datetime import datetime, timezone

import pytest
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution import campaign_result
from c1_rail.qualification.execution import campaign_supervisor as supervisor
from c1_rail.qualification.execution.campaign_result import ResultStore
from c1_rail.qualification.execution.campaign_store import CampaignStore
from c1_rail.qualification.execution.g5_result import _authentication_core, _sign_authentication
from c1_rail.qualification.execution.protocol import sha256

from result_fixture import (G5_UID, build_candidate, commit_request,
                            complete_phase_work, scene, settle_phase_work,
                            sign_candidate, stage_authentication)

NOW = datetime(2026, 9, 21, tzinfo=timezone.utc)


def altered(candidate, **changes):
    """A canonical, still-legal aggregate that differs from the original."""
    document = json.loads(candidate)
    document.update(changes)
    return encoded(document)


def prepared(tmp_path, monkeypatch, **options):
    """The scene plus a staged aggregate: snapshot, candidate, authentication,
    private staging and the COMMIT request."""
    instance, double = scene(tmp_path, monkeypatch, **options)
    attempt = instance.attempt
    snapshot = double.results.result_snapshot(attempt)
    candidate = build_candidate(double, snapshot)
    revision = json.loads(snapshot)['campaign_revision']
    authentication = sign_candidate(double, candidate, revision=revision,
                                    snapshot_sha256=sha256(snapshot))
    stage_authentication(double, authentication)
    request = commit_request(attempt, 'rwork', candidate, authentication, revision=revision)
    return instance, double, snapshot, candidate, authentication, request


def test_all_stage_pass_commits_result_committed_pass(tmp_path, monkeypatch):
    instance, double, snapshot, candidate, authentication, request = prepared(
        tmp_path, monkeypatch, n1_decision='CONTINUE', through='PART_A')
    response = json.loads(double.handle_result_request(G5_UID, request))
    receipt = response['receipt']
    assert response['historical'] is False and response['validity'] == 'VALID'
    assert receipt['outcome'] == 'PASS'
    assert receipt['campaign_state'] == 'RESULT_COMMITTED_PASS'
    assert receipt['accepted_prefix'] == list(campaign_result.STAGE_ORDER)
    state = json.loads(double.results.result_state_bytes(instance.attempt))
    assert state['checkpoints']['N1']['state'] == 'COMMITTED'
    family = json.loads(double.results.result_snapshot(instance.attempt))['result']
    assert family == dict(state='COMMITTED', outcome='PASS')
    assert double.results.seal_eligibility(instance.attempt)['eligible'] is True


def test_fail_after_n1_commits_from_real_custody_only(tmp_path, monkeypatch):
    """Legacy: test_n1_terminal_prefix_needs_no_later_draws -- a terminal N1
    failure is a complete legal aggregate with no successor custody."""
    instance, double, snapshot, candidate, authentication, request = prepared(
        tmp_path, monkeypatch, n1_decision='FAILURE')
    response = json.loads(double.handle_result_request(G5_UID, request))
    receipt = response['receipt']
    assert receipt['outcome'] == 'FAIL'
    assert receipt['campaign_state'] == 'RESULT_COMMITTED_FAIL'
    assert receipt['accepted_prefix'] == ['LEGALITY', 'N1']
    assert double.results.seal_eligibility(instance.attempt)['eligible'] is False


def test_fail_after_joint_batch_and_after_all_stages_commit(tmp_path, monkeypatch):
    for through, fail_at, prefix in (('N2', 'N2', ['LEGALITY', 'N1', 'N2', 'PART_B']),
                                     ('PART_A', 'PART_A', list(campaign_result.STAGE_ORDER))):
        instance, double, snapshot, candidate, authentication, request = prepared(
            tmp_path / (through + fail_at), monkeypatch, n1_decision='CONTINUE',
            through=through, fail_at=fail_at)
        response = json.loads(double.handle_result_request(G5_UID, request))
        assert response['receipt']['outcome'] == 'FAIL'
        assert response['receipt']['accepted_prefix'] == prefix


def test_missing_extra_or_out_of_order_stages_refuse(tmp_path, monkeypatch):
    instance, double = scene(tmp_path, monkeypatch, n1_decision='CONTINUE',
                             through='PART_A')
    rows, _, _ = double.custody(instance.attempt)
    cutoffs = {row['checkpoint']: row['cutoff_bytes'] for row in rows}
    from result_fixture import result_context
    context = result_context(double, instance.attempt)
    kwargs = dict(cutoffs=cutoffs, budget_digest='0' * 64,
                  release=double.instance.release, policy=context.policy)
    # Missing the PART_A successor: a passing incomplete prefix.
    with pytest.raises(ValueError, match='incomplete passing prefix refuses a result'):
        campaign_result.build_campaign_result(checkpoint_receipts=rows[:2], **kwargs)
    # Extra: a duplicated joint-batch row.
    with pytest.raises(ValueError, match='checkpoint custody order differs'):
        campaign_result.build_campaign_result(checkpoint_receipts=[rows[0], rows[1], rows[1]],
                                               **kwargs)
    # Out of order: PART_A before the joint batch.
    with pytest.raises(ValueError, match='checkpoint custody order differs'):
        campaign_result.build_campaign_result(checkpoint_receipts=[rows[0], rows[2], rows[1]],
                                               **kwargs)
    # Legacy: test_later_stage_evidence_after_failure_is_refused -- a successor
    # row after a failing N1 refuses (the failing prefix is terminal).
    failing_cutoff = encoded(dict(
        schema='qualification_campaign_cutoff_receipt/v1',
        attempt_id=instance.attempt, checkpoint='N1',
        assessment_sha256=rows[0]['assessment_sha256'], decision='FAILURE'))
    failing_n1 = dict(rows[0], decision='FAILURE', cutoff_bytes=failing_cutoff,
                      stages=[dict(stage='LEGALITY', status='PASS'),
                              dict(stage='N1', status='FAIL')])
    with pytest.raises(ValueError, match='only the last stage of a complete prefix may fail'):
        campaign_result.build_campaign_result(
            checkpoint_receipts=[failing_n1, rows[1]],
            cutoffs={**cutoffs, 'N1': failing_cutoff},
            budget_digest='0' * 64, release=double.instance.release, policy=context.policy)


def test_passing_incomplete_prefix_refuses_fail_on_base(tmp_path, monkeypatch):
    """Fail-on-base regression 1: a passing incomplete prefix is refused at
    BOTH layers -- the store never reserves the RESULT work for it, and the
    canonical builder refuses it outright (absent at 71732aa: the module does
    not exist there, so this file fails to import on the base revision)."""
    from result_fixture import (ResultServiceDouble, committed_n1, result_context,
                                synthetic_predecessors)
    instance, _ = committed_n1(tmp_path, monkeypatch, decision='CONTINUE')
    campaign_id = CampaignStore(instance.store).row(instance.attempt)['campaign_id']
    rows, artifacts, attestations = synthetic_predecessors(instance.attempt, campaign_id,
                                                           through='N2')
    double = ResultServiceDouble(instance, synthetic_rows=rows,
                                 synthetic_artifacts=artifacts,
                                 synthetic_attestations=attestations)
    state = json.loads(double.results.result_state_bytes(instance.attempt))
    clock_doc = json.loads(supervisor.observe_campaign_clock())
    reservation = encoded(dict(limits=state['profile']['phases']['RESULT'], clock=clock_doc,
                               input_sha256=sha256(b'incomplete-prefix-input')))
    with pytest.raises(ValueError,
                       match='result predecessor refuses: incomplete passing prefix'):
        double.results.reserve_result_work(instance.attempt, 'rwork', reservation,
                                           expected_revision=state['authority_revision'])
    custody = double.results.checkpoint_receipts(instance.attempt)
    context = result_context(double, instance.attempt)
    with pytest.raises(ValueError, match='incomplete passing prefix refuses a result'):
        campaign_result.build_campaign_result(
            checkpoint_receipts=custody,
            cutoffs={row['checkpoint']: row['cutoff_bytes'] for row in custody},
            budget_digest='0' * 64, release=double.instance.release, policy=context.policy)
    # The same custody with a FAIL at the joint batch is the legal shape.
    failing_cutoff = encoded(dict(schema='qualification_campaign_cutoff_receipt/v1',
        attempt_id=instance.attempt, checkpoint='N2',
        assessment_sha256=custody[1]['assessment_sha256'], decision='FAIL'))
    failing = [custody[0], dict(custody[1], decision='FAIL', cutoff_bytes=failing_cutoff,
                                stages=[dict(stage='N2', status='PASS'),
                                        dict(stage='PART_B', status='FAIL')])]
    raw = campaign_result.build_campaign_result(
        checkpoint_receipts=failing,
        cutoffs={row['checkpoint']: row['cutoff_bytes'] for row in failing},
        budget_digest='0' * 64, release=double.instance.release, policy=context.policy)
    assert json.loads(raw)['outcome'] == 'FAIL'


def test_exact_intent_and_candidate_retention(tmp_path, monkeypatch):
    instance, double, snapshot, candidate, authentication, request = prepared(
        tmp_path, monkeypatch, n1_decision='FAILURE')
    from c1_rail.qualification.execution.store import instant
    intent = encoded(dict(schema=campaign_result.RESULT_INTENT_SCHEMA,
        attempt_id=instance.attempt, work_id='rwork', key_id='test-producer',
        signing_at_utc=instant(NOW), candidate_sha256=sha256(candidate),
        snapshot_sha256=sha256(snapshot)))
    revision = json.loads(snapshot)['campaign_revision']
    double.results.persist_result_intent(instance.attempt, 'rwork', snapshot, intent,
                                         candidate, expected_revision=revision)
    # Exact retry is idempotent; a different candidate always refuses.
    double.results.persist_result_intent(instance.attempt, 'rwork', snapshot, intent,
                                         candidate, expected_revision=revision)
    different = altered(candidate, binding=dict(json.loads(candidate)['binding'],
                                                budget_digest='c' * 64))
    rebound = encoded(dict(json.loads(intent), candidate_sha256=sha256(different)))
    with pytest.raises(ValueError, match='immutable result signing candidate differs'):
        double.results.persist_result_intent(instance.attempt, 'rwork', snapshot, rebound,
                                             different, expected_revision=revision)
    with pytest.raises(ValueError, match='exact result candidate retry required'):
        double.handle_result_request(G5_UID, commit_request(
            instance.attempt, 'rwork', different, authentication, revision=revision))


def test_void_during_signing_window_refuses_the_commit(tmp_path, monkeypatch):
    """Spec 2.8's single observable ordering, VOID first: a VOID landing in
    the re-validation window between T1 and T2 leaves no authority for the
    publication (the wrapper below marks and forces that exact point)."""
    instance, double, snapshot, candidate, authentication, request = prepared(
        tmp_path, monkeypatch, n1_decision='CONTINUE', through='PART_A')
    from c1_rail.qualification.execution import g5_result
    original = g5_result.verify_result_authentication

    def void_then_verify(raw, *, context, current_keys):
        with instance.store.transaction() as connection:
            connection.execute("UPDATE full_campaigns SET validity='VOID' WHERE attempt_id=?",
                               (instance.attempt,))
        return original(raw, context=context, current_keys=current_keys)

    monkeypatch.setattr(g5_result, 'verify_result_authentication', void_then_verify)
    with pytest.raises(ValueError, match='VOID campaign'):
        double.handle_result_request(G5_UID, request)
    monkeypatch.setattr(g5_result, 'verify_result_authentication', original)
    # Legacy: test_void_before_seal_survives_restart -- no receipt was written.
    with pytest.raises(ValueError, match='no committed campaign result'):
        double.results.result_receipt(instance.attempt)
    assert double.results.seal_eligibility(instance.attempt)['eligible'] is False


def test_commit_first_then_void_flips_validity_only(tmp_path, monkeypatch):
    """Publication first, VOID second: the receipt stays byte-identical and
    historical; the current validity flips; no new authority appears."""
    instance, double, snapshot, candidate, authentication, request = prepared(
        tmp_path, monkeypatch, n1_decision='CONTINUE', through='PART_A')
    first = json.loads(double.handle_result_request(G5_UID, request))
    with instance.store.transaction() as connection:
        connection.execute("UPDATE full_campaigns SET validity='VOID' WHERE attempt_id=?",
                           (instance.attempt,))
    receipt_bytes, historical, validity = double.results.result_receipt(instance.attempt)
    assert historical is True and validity == 'VOID'
    assert receipt_bytes == encoded(first['receipt'])
    retry = json.loads(double.handle_result_request(G5_UID, request))
    assert retry['receipt'] == first['receipt'] and retry['historical'] is True
    assert retry['validity'] == 'VOID'
    # Legacy: test_historical_complete_pass_signatures_inspect_but_active_
    # authority_is_retired -- the historical PASS never re-opens sealing.
    assert double.results.seal_eligibility(instance.attempt) == dict(
        eligible=False, reason='VOID campaign', state='RESULT_COMMITTED_PASS')


def test_lost_response_after_commit_returns_identical_receipt(tmp_path, monkeypatch):
    """Legacy: test_seal_retry_and_history_survive_restart_and_void (the
    result side): the retry after a lost reply is byte-identical, with no
    fresh time, key or signature."""
    instance, double, snapshot, candidate, authentication, request = prepared(
        tmp_path, monkeypatch, n1_decision='CONTINUE', through='PART_A')
    first = json.loads(double.handle_result_request(G5_UID, request))
    second = json.loads(double.handle_result_request(G5_UID, request))
    assert second['receipt'] == first['receipt']
    assert second['historical'] is True and first['historical'] is False
    assert second['receipt']['committed_at_utc'] == first['receipt']['committed_at_utc']


def test_revoked_or_absent_key_before_commit_refuses(tmp_path, monkeypatch):
    instance, double, snapshot, candidate, authentication, request = prepared(
        tmp_path, monkeypatch, n1_decision='CONTINUE', through='PART_A')
    keys = dict(double.keys())
    revoked = dict(keys)
    revoked['test-producer'] = replace(keys['test-producer'],
                                       revoked_at=datetime(2026, 9, 20, tzinfo=timezone.utc))
    monkeypatch.setattr(double, 'keys', lambda: revoked)
    with pytest.raises(ValueError, match='result key is revoked'):
        double.handle_result_request(G5_UID, request)
    # A key absent from the registry fails closed even earlier: the enrollment
    # context cannot be re-established without it (defense in depth below the
    # validator's own missing-key refusal).
    missing = dict(keys)
    del missing['test-producer']
    monkeypatch.setattr(double, 'keys', lambda: missing)
    with pytest.raises(ValueError, match='release key authority or identity differs'):
        double.handle_result_request(G5_UID, request)


def test_authentication_binding_mismatches_refuse(tmp_path, monkeypatch):
    instance, double, snapshot, candidate, authentication, request = prepared(
        tmp_path, monkeypatch, n1_decision='CONTINUE', through='PART_A')
    revision = json.loads(snapshot)['campaign_revision']
    # A mismatched staged digest refuses before any state change.
    wrong_request = encoded(dict(json.loads(request), authentication_sha256='e' * 64))
    with pytest.raises(ValueError, match='staged result authentication membership differs'):
        double.handle_result_request(G5_UID, wrong_request)
    # A signature over the wrong revision refuses at T2's binding check.
    bad = _sign_authentication(
        _authentication_core(attempt_id=instance.attempt, aggregate_sha256=sha256(candidate),
                             campaign_revision=revision + 1,
                             snapshot_sha256=sha256(snapshot)), 'test-producer',
        instance.case['private']['test-producer'])
    stage_authentication(double, bad)
    with pytest.raises(ValueError, match='result authentication binding differs'):
        double.handle_result_request(G5_UID, commit_request(
            instance.attempt, 'rwork', candidate, bad, revision=revision))


def test_deadline_exhaustion_refuses_the_result_work(tmp_path, monkeypatch):
    """RESULT exhaustion: a reservation whose trusted clock observation lands
    past the campaign deadline terminalizes the budget and refuses (reason
    string); nothing is reserved."""
    from result_fixture import ResultServiceDouble, committed_n1
    instance, _ = committed_n1(tmp_path, monkeypatch, decision='FAILURE')
    double = ResultServiceDouble(instance)
    state = json.loads(double.results.result_state_bytes(instance.attempt))
    instance.clocks['t'] = state['deadline_boottime_ns'] + 1
    clock_doc = json.loads(supervisor.observe_campaign_clock())
    reservation = encoded(dict(limits=state['profile']['phases']['RESULT'], clock=clock_doc,
                               input_sha256=sha256(b'another-result-input')))
    with pytest.raises(ValueError,
                       match='result reservation refused by campaign budget: BUDGET_EXHAUSTED'):
        double.results.reserve_result_work(instance.attempt, 'rwork', reservation,
                                           expected_revision=state['authority_revision'])
    state_after = json.loads(double.results.result_state_bytes(instance.attempt))
    # The refusal is the observable; the snapshot's state field keeps its
    # canonical predecessor (the enum seam carries BUDGET_EXHAUSTED flips for
    # terminal campaigns post-integration).
    assert state_after['state'] == 'N1_FAILED'
    assert not any(w['phase'] == 'RESULT' for w in state_after['works'])


def test_one_immutable_receipt_and_v9_custody_freezes_the_s3_store(tmp_path, monkeypatch):
    instance, double, snapshot, candidate, authentication, request = prepared(
        tmp_path, monkeypatch, n1_decision='FAILURE')
    json.loads(double.handle_result_request(G5_UID, request))
    with instance.store.transaction() as connection:
        version = connection.execute('PRAGMA user_version').fetchone()[0]
        tables = {row[0] for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")}
        double.results.result_integrity(connection)
    assert version == 9
    assert {'full_campaign_result_intents', 'full_campaign_seal_intents'} <= tables
    # The S3 budget reader is frozen at v9 (the store.py version seam).
    campaigns = CampaignStore(instance.store)
    with pytest.raises(ValueError, match='no metered campaign'):
        campaigns.budget_snapshot(instance.attempt)
    receipt_bytes, historical, validity = double.results.result_receipt(instance.attempt)
    assert historical is True and validity == 'VALID'
    with pytest.raises(ValueError, match='no committed campaign result'):
        ResultStore(campaigns).result_receipt('missing-attempt')


def test_result_operations_shape_and_authorization(tmp_path, monkeypatch):
    instance, double = scene(tmp_path, monkeypatch, n1_decision='FAILURE')
    snapshot = double.results.result_snapshot(instance.attempt)
    candidate = build_candidate(double, snapshot)
    revision = json.loads(snapshot)['campaign_revision']
    good = commit_request(instance.attempt, 'rwork', candidate, b'x' * 32, revision=revision)
    parsed = campaign_result.parse_result_operation(good)
    assert parsed['operation'] == 'COMMIT_E1_RESULT'
    unknown = encoded(dict(schema='qualification_campaign_request/v2',
                           operation='COMMIT_E1_RESULT_EXTRA', attempt_id=instance.attempt))
    with pytest.raises(ValueError, match='UNKNOWN_OPERATION'):
        campaign_result.parse_result_operation(unknown)
    oversized = encoded(dict(json.loads(good), candidate_bytes_b64=base64.b64encode(
        b'x' * 262145).decode('ascii')))
    with pytest.raises(ValueError, match='bounded result candidate required'):
        campaign_result.parse_result_operation(oversized)
    with pytest.raises(ValueError, match='PEER_NOT_AUTHORIZED'):
        double.handle_result_request(1001, good)


def test_result_snapshot_excludes_its_own_receipt(tmp_path, monkeypatch):
    instance, double, snapshot, candidate, authentication, request = prepared(
        tmp_path, monkeypatch, n1_decision='CONTINUE', through='PART_A')
    parsed = json.loads(snapshot)
    assert parsed['result'] == dict(state='ABSENT', outcome=None)
    assert 'receipt' not in parsed['result'] and 'receipt_bytes_b64' not in parsed
    json.loads(double.handle_result_request(G5_UID, request))
    later = json.loads(double.results.result_snapshot(instance.attempt))
    assert later['result'] == dict(state='COMMITTED', outcome='PASS')
    assert 'receipt_bytes_b64' not in later


def test_run_result_g5_signature_matches_the_n1_g5_body():
    """F4: the guardian body has _run_n1_g5's exact signature (the seam maps
    manifest role 'result_g5' to it); the launch itself is Linux evidence."""
    import inspect
    from c1_rail.qualification.execution.campaign_supervisor import _run_n1_g5
    assert inspect.signature(campaign_result.run_result_g5) == inspect.signature(_run_n1_g5)
    spec = campaign_result.run_result_g5
    assert spec.__module__ == 'c1_rail.qualification.execution.campaign_result'


@pytest.mark.parametrize('n1_decision,through,frozen', [
    ('CONTINUE', 'PART_A', 'N2_READY'), ('FAILURE', None, 'N1_FAILED')])
def test_committed_result_settles_within_budget_and_completes(tmp_path, monkeypatch,
                                                              n1_decision, through, frozen):
    """The committing RESULT work settles after T2 and completes in the state
    its own commit produced (S3's a8a983e rule, PR #455 review, carried to
    T05): on frozen bytes the budget snapshot keeps the statistical
    predecessor -- N2_READY/N1_FAILED here, the F3 terminal names once S4/S5
    land, RESULT_COMMITTED_{PASS,FAIL} after the enum seam."""
    instance, double, snapshot, candidate, authentication, request = prepared(
        tmp_path, monkeypatch, n1_decision=n1_decision, through=through)
    json.loads(double.handle_result_request(G5_UID, request))
    state = settle_phase_work(double.results, instance.attempt, 'rwork', 'RESULT')
    assert state['state'] == frozen
    state = complete_phase_work(double.results, instance.attempt, 'rwork')
    assert state['state'] == frozen
    assert next(w for w in state['works'] if w['work_id'] == 'rwork')['state'] == 'COMPLETED'


@pytest.mark.parametrize('n1_decision,through', [
    ('CONTINUE', 'PART_A'), ('FAILURE', None)])
def test_committed_result_overrun_blocks_the_outcome(tmp_path, monkeypatch,
                                                     n1_decision, through):
    """An overrun observed when the RESULT work settles after T2 permanently
    blocks authority (spec 2.5 via S3's a8a983e): the commit's state becomes
    BUDGET_EXHAUSTED, the committing work cannot complete, the ended
    authority never reaches the seal, and the receipt survives as history."""
    instance, double, snapshot, candidate, authentication, request = prepared(
        tmp_path, monkeypatch, n1_decision=n1_decision, through=through)
    first = json.loads(double.handle_result_request(G5_UID, request))
    limit = next(w for w in json.loads(
        double.results.result_state_bytes(instance.attempt))['works']
        if w['work_id'] == 'rwork')['limits']['cpu_ns']
    state = settle_phase_work(double.results, instance.attempt, 'rwork', 'RESULT',
                              cpu=limit + 1)
    assert state['state'] == 'BUDGET_EXHAUSTED'
    with pytest.raises(ValueError, match='terminal campaign budget'):
        complete_phase_work(double.results, instance.attempt, 'rwork')
    retry = json.loads(double.handle_result_request(G5_UID, request))
    assert retry['receipt'] == first['receipt'] and retry['historical'] is True
    assert double.results.seal_eligibility(instance.attempt)['eligible'] is False


def test_synthetic_predecessors_are_labelled_in_every_record(tmp_path, monkeypatch):
    instance, double = scene(tmp_path, monkeypatch, n1_decision='CONTINUE',
                             through='PART_A')
    rows = double.results.checkpoint_receipts(instance.attempt)
    labels = {row['checkpoint']: row['synthetic_predecessor'] for row in rows}
    assert labels == {'N1': False, 'N2': True, 'PART_A': True}
    for row in rows[1:]:
        for name in ('assessment_bytes', 'cutoff_bytes', 'receipt_bytes'):
            assert json.loads(row[name])['synthetic_predecessor'] is True
