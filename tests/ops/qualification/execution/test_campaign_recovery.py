"""Real SQLite recovery/races with simulated trusted observations only."""
import base64
import json
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from threading import Event

import pytest
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution.campaign_store import CampaignStore
from c1_rail.qualification.execution.store import ExecutionStore
from test_campaign_budget import (ATTEMPT, NOW, clock, contract_budget, observation,
    opened, profile, request, reserve, snap, start, transition)


def void_request():
    return encoded(dict(schema='qualification_campaign_request/v1', operation='VOID',
        attempt_id=ATTEMPT, reason='stop', operator_approval_bytes='eA=='))


def capture(store, work='admission', t=12):
    return transition(store, work, 'CAPTURED', t,
        dict(capture_bytes_b64=base64.b64encode(b'persisted exact bytes').decode()))


def test_reserved_recovery_reuses_reservation_and_elapsed_deadline(tmp_path):
    store = opened(tmp_path)
    before = snap(store)
    store = CampaignStore(ExecutionStore(store.store.path))
    store.recover_work(ATTEMPT, 'admission', encoded(clock(100)))
    after = snap(store)
    assert after['reserved_cpu_ns'] == before['reserved_cpu_ns'] == 60
    assert after['deadline_boottime_ns'] == before['deadline_boottime_ns']
    assert after['authority_revision'] == before['authority_revision']
    store.recover_work(ATTEMPT, 'admission', encoded(clock(20_000_000_010)))
    assert snap(store)['state'] == 'BUDGET_EXHAUSTED'
    with pytest.raises(ValueError): start(store)


@pytest.mark.parametrize('running', [False, True])
def test_uncertainty_is_durable_before_cleanup_and_prevents_redraw(tmp_path, running):
    store = opened(tmp_path)
    start(store)
    if running: transition(store, 'admission', 'RUNNING', 11)
    store.recover_work(ATTEMPT, 'admission', observation(cpu=None, t=12))
    try:
        raise OSError('simulated cleanup failure after durable recovery')
    except OSError:
        pass
    recovered = CampaignStore(ExecutionStore(store.store.path))
    result = snap(recovered)
    assert result['works'][0]['state'] == 'IN_DOUBT'
    assert result['settled_cpu_ns'] == 60
    assert result['state'] == 'BUDGET_UNCERTAIN'
    with pytest.raises(ValueError): reserve(recovered)
    assert json.loads(start(recovered))['works'][0]['state'] == 'IN_DOUBT'


def test_captured_recovery_retains_bytes_and_cannot_restart(tmp_path):
    store = opened(tmp_path)
    start(store)
    capture(store)
    store.recover_work(ATTEMPT, 'admission', observation(t=13))
    before = store.budget_snapshot(ATTEMPT)
    store = CampaignStore(ExecutionStore(store.store.path))
    assert store.budget_snapshot(ATTEMPT) == before
    work = snap(store)['works'][0]
    assert work['state'] == 'CAPTURED'
    saved = json.loads(base64.b64decode(work['transitions'][-1]))
    assert base64.b64decode(saved['data']['capture_bytes_b64']) == b'persisted exact bytes'
    with pytest.raises(ValueError): start(store, t=14)


def test_accounting_settlement_and_finalization_share_authority_revision(tmp_path):
    store = opened(tmp_path)
    start(store)
    capture(store)
    snapshot = snap(store)
    with store.store.transaction():
        store.settle_work(ATTEMPT, 'admission', observation(t=13))
        charged = snap(store)
        assert charged['authority_revision'] == snapshot['authority_revision']
        assert charged['authority_head'] == snapshot['authority_head']
        assert charged['event_head'] != snapshot['event_head']
        transition(store, 'admission', 'COMPLETED', 14)
    assert snap(store)['works'][0]['state'] == 'COMPLETED'
    assert snap(store)['settled_cpu_ns'] == 20


def test_settlement_and_finalization_rollback_together(tmp_path):
    store = opened(tmp_path)
    start(store)
    capture(store)
    before = store.budget_snapshot(ATTEMPT)
    with pytest.raises(RuntimeError):
        with store.store.transaction():
            store.settle_work(ATTEMPT, 'admission', observation(t=13))
            transition(store, 'admission', 'COMPLETED', 14)
            raise RuntimeError('publication failed before commit')
    assert CampaignStore(ExecutionStore(store.store.path)).budget_snapshot(ATTEMPT) == before


@pytest.mark.parametrize('void_first', [True, False])
def test_void_and_finalization_both_sqlite_orderings(tmp_path, void_first):
    store = opened(tmp_path)
    start(store)
    capture(store)
    old_revision = snap(store)['authority_revision']
    entered, release, contender = Event(), Event(), Event()
    def finalize(target):
        target.settle_work(ATTEMPT, 'admission', observation(t=13))
        return target.record_work_transition(ATTEMPT, 'admission', encoded(dict(
            schema='qualification_campaign_work_transition/v1', attempt_id=ATTEMPT,
            work_id='admission', state='COMPLETED', clock=clock(14), data={})),
            expected_revision=old_revision)
    def first():
        with store.store.transaction():
            result = store.void(void_request(), now=NOW) if void_first else finalize(store)
            entered.set()
            assert release.wait(10)
            return result
    def second():
        contender.set()
        other = CampaignStore(ExecutionStore(store.store.path))
        return finalize(other) if void_first else other.void(void_request(), now=NOW)
    with ThreadPoolExecutor(max_workers=2) as pool:
        a = pool.submit(first)
        assert entered.wait(10)
        b = pool.submit(second)
        assert contender.wait(10)
        release.set()
        first_result = a.result()
        if void_first:
            with pytest.raises(ValueError): b.result()
        else:
            b.result()
            assert json.loads(first_result)['works'][0]['state'] == 'COMPLETED'
    result = snap(CampaignStore(ExecutionStore(store.store.path)))
    assert result['validity'] == 'VOID'
    assert result['works'][0]['state'] == ('CAPTURED' if void_first else 'COMPLETED')
    assert store.void(void_request(), now=NOW) == store.void_retry(void_request())


def test_signing_intent_is_fixed_and_serializes_authority_not_accounting(tmp_path):
    store = opened(tmp_path)
    start(store)
    capture(store)
    intent = dict(intent_id='intent-1', payload_bytes_b64='eA==', key_id='test-key',
                  signing_at_utc='2026-09-19T00:00:00Z')
    transition(store, 'admission', 'SIGNING_INTENT', 13, intent)
    revision = snap(store)['authority_revision']
    store.settle_work(ATTEMPT, 'admission', observation(t=14))
    assert snap(store)['authority_revision'] == revision
    with pytest.raises(ValueError): reserve(store, t=14)
    with pytest.raises(ValueError): transition(store, 'admission', 'SIGNING_INTENT', 13, dict(intent, key_id='other'))
    candidate = dict(candidate_bytes_b64='c2F2ZWQ=')
    transition(store, 'admission', 'SIGNED', 15, candidate)
    before = store.budget_snapshot(ATTEMPT)
    assert CampaignStore(ExecutionStore(store.store.path)).budget_snapshot(ATTEMPT) == before
    assert transition(store, 'admission', 'SIGNED', 15, candidate) == before


def test_phase_wall_overrun_is_terminal_even_below_campaign_deadline(tmp_path):
    store = opened(tmp_path)
    start(store)
    store.settle_work(ATTEMPT, 'admission', observation(t=1_000_000_010))
    assert snap(store)['state'] == 'BUDGET_EXHAUSTED'


def test_compute_finalization_requires_saved_capture(tmp_path):
    store = opened(tmp_path)
    reserve(store)
    start(store, 'n1', 11)
    store.settle_work(ATTEMPT, 'n1', observation('n1', t=12))
    with pytest.raises(ValueError): transition(store, 'n1', 'COMPLETED', 13)


def test_additive_migration_rolls_back_and_validates_exact_layout(tmp_path, monkeypatch):
    from c1_rail.qualification.execution import campaign_store as module
    store = CampaignStore(ExecutionStore(tmp_path / 'journal.sqlite'))
    with monkeypatch.context() as patch:
        patch.setattr(module, 'BUDGET_SCHEMA', module.BUDGET_SCHEMA + ' invalid migration;')
        with pytest.raises(sqlite3.OperationalError):
            store.begin_admission(request(), encoded(profile()), encoded(clock()))
    with sqlite3.connect(store.store.path) as connection:
        assert connection.execute('PRAGMA user_version').fetchone()[0] == 5
        assert connection.execute("SELECT 1 FROM sqlite_master WHERE name='full_campaign_budgets'").fetchone() is None
    store.begin_admission(request(), encoded(profile()), encoded(clock()))
    assert CampaignStore(ExecutionStore(store.store.path)).budget_snapshot(ATTEMPT) == store.budget_snapshot(ATTEMPT)
    with sqlite3.connect(store.store.path) as connection:
        connection.execute('ALTER TABLE full_campaign_budgets ADD COLUMN unexpected TEXT')
    with pytest.raises(ValueError, match='layout'): ExecutionStore(store.store.path)


def test_tampered_projection_or_event_is_rejected_on_reopen(tmp_path):
    store = opened(tmp_path)
    with sqlite3.connect(store.store.path) as connection:
        state = snap(store)
        state['remaining_cpu_ns'] = 10**12
        connection.execute('UPDATE full_campaign_budgets SET snapshot_bytes=?', (encoded(state),))
    with pytest.raises(ValueError, match='integrity'): ExecutionStore(store.store.path)


@pytest.mark.parametrize('actions', [
    ('reopen', 'recover', 'intent', 'running', 'capture', 'recover', 'reopen'),
    ('intent', 'recover', 'reopen', 'running'),
    ('intent', 'running', 'void', 'recover', 'capture'),
    ('void', 'intent'),
])
def test_sqlite_recovery_matches_independent_lifecycle_model(tmp_path, actions):
    from lifecycle_model import CampaignBudgetModel
    model = CampaignBudgetModel(1_000_000_000, 60)
    store = opened(tmp_path)
    t = 10
    for action in actions:
        t += 1
        expected = model.apply(action, charge=20)
        def invoke():
            nonlocal store
            if action == 'reopen':
                store = CampaignStore(ExecutionStore(store.store.path))
            elif action == 'recover':
                raw = encoded(clock(t)) if snap(store)['works'][0]['state'] == 'RESERVED' else observation(t=t)
                store.recover_work(ATTEMPT, 'admission', raw)
            elif action == 'void': store.void(void_request(), now=NOW)
            elif action == 'intent': start(store, t=t)
            elif action == 'running': transition(store, 'admission', 'RUNNING', t)
            elif action == 'capture': capture(store, t=t)
        if expected:
            invoke()
        else:
            with pytest.raises(ValueError): invoke()
        actual = snap(store)
        assert actual['works'][0]['state'] == model.state
        assert actual['validity'] == model.validity
        assert actual['remaining_cpu_ns'] == model.remaining


def test_candidate_custody_does_not_stale_its_own_signing_snapshot(tmp_path):
    store = opened(tmp_path)
    start(store)
    capture(store)
    intent = dict(intent_id='intent-1', payload_bytes_b64='eA==', key_id='test-key',
                  signing_at_utc='2026-09-19T00:00:00Z')
    transition(store, 'admission', 'SIGNING_INTENT', 13, intent)
    signing = snap(store)
    transition(store, 'admission', 'SIGNED', 14, dict(candidate_bytes_b64='c2F2ZWQ='))
    assert snap(store)['authority_revision'] == signing['authority_revision']
    assert snap(store)['authority_head'] == signing['authority_head']
    with pytest.raises(ValueError): reserve(store, t=14)
    with store.store.transaction():
        store.settle_work(ATTEMPT, 'admission', observation(t=15))
        doc = encoded(dict(schema='qualification_campaign_work_transition/v1', attempt_id=ATTEMPT,
            work_id='admission', state='COMPLETED', clock=clock(16), data={}))
        store.record_work_transition(ATTEMPT, 'admission', doc,
                                     expected_revision=signing['authority_revision'])
    assert snap(store)['authority_revision'] == signing['authority_revision'] + 1


def test_abort_is_irreversible_campaign_terminal(tmp_path):
    store = opened(tmp_path)
    transition(store, 'admission', 'ABORTED', 11)
    with pytest.raises(ValueError): reserve(store, t=12)
    assert snap(store)['state'] == 'ABORTED'


def test_phase_wall_checked_before_capture_authority(tmp_path):
    store = opened(tmp_path)
    start(store)
    capture(store, t=1_000_000_010)
    assert snap(store)['state'] == 'BUDGET_EXHAUSTED'
    assert snap(store)['works'][0]['state'] == 'START_INTENT'


def test_migration_revalidates_layout_inside_its_transaction(tmp_path):
    store = CampaignStore(ExecutionStore(tmp_path / 'journal.sqlite'))
    with sqlite3.connect(store.store.path) as connection:
        connection.execute('ALTER TABLE full_campaigns ADD COLUMN unexpected TEXT')
    with pytest.raises(ValueError, match='layout'):
        store.begin_admission(request(), encoded(profile()), encoded(clock()))
    with sqlite3.connect(store.store.path) as connection:
        assert connection.execute('PRAGMA user_version').fetchone()[0] == 5


def test_recovery_cannot_claim_durability_inside_uncommitted_outer_transaction(tmp_path):
    store = opened(tmp_path)
    start(store)
    with store.store.transaction():
        with pytest.raises(ValueError, match='outer transaction'):
            store.recover_work(ATTEMPT, 'admission', observation(cpu=None))


def test_snapshot_transition_parser_rejects_unknown_fields(tmp_path):
    from c1_rail.qualification.journal_snapshot import parse_campaign_budget_snapshot
    store = opened(tmp_path)
    start(store)
    state = snap(store)
    transition_doc = json.loads(base64.b64decode(state['works'][0]['transitions'][0]))
    transition_doc['data']['untrusted_extra'] = 1
    state['works'][0]['transitions'][0] = base64.b64encode(encoded(transition_doc)).decode()
    with pytest.raises(ValueError): parse_campaign_budget_snapshot(encoded(state))


@pytest.mark.parametrize('boot,t', [('boot-1', None), (None, 12)])
def test_unavailable_trusted_clock_is_durable_uncertainty(tmp_path, boot, t):
    store = opened(tmp_path)
    start(store)
    store.settle_work(ATTEMPT, 'admission', observation(boot=boot, t=t))
    assert snap(store)['state'] == 'BUDGET_UNCERTAIN'
    assert snap(CampaignStore(ExecutionStore(store.store.path)))['state'] == 'BUDGET_UNCERTAIN'


def test_exact_retry_still_rejects_boolean_expected_revision(tmp_path):
    store = opened(tmp_path)
    with pytest.raises(ValueError): store.bind_budget(ATTEMPT, contract_budget(), expected_revision=True)


def test_late_settlement_after_unavailable_clock_retains_charges(tmp_path):
    store = opened(tmp_path)
    reserve(store)
    start(store, t=11)
    start(store, 'n1', 11)
    store.settle_work(ATTEMPT, 'admission', observation(t=None))
    store.settle_work(ATTEMPT, 'n1', observation('n1', cpu=30, t=12))
    result = snap(store)
    assert result['state'] == 'BUDGET_UNCERTAIN'
    assert result['settled_cpu_ns'] == 50 and result['reserved_cpu_ns'] == 0


@pytest.mark.parametrize('field,value', [('dispatch_enabled', True),
    ('request_sha256', '0' * 64), ('attempt_id', 'other'), ('unexpected', 1)])
def test_provisional_receipt_is_exactly_validated_on_reopen(tmp_path, field, value):
    store = opened(tmp_path)
    with sqlite3.connect(store.store.path) as connection:
        raw = connection.execute('SELECT receipt_bytes FROM full_campaigns').fetchone()[0]
        receipt = json.loads(raw)
        receipt[field] = value
        connection.execute('UPDATE full_campaigns SET receipt_bytes=?', (encoded(receipt),))
    with pytest.raises(ValueError, match='integrity'): ExecutionStore(store.store.path)


@pytest.mark.parametrize('boundary', ['START_INTENT', 'RUNNING', 'CAPTURED'])
@pytest.mark.parametrize('boot,t,want', [('boot-1', 20, 'BOUND'),
    ('boot-2', 20, 'BUDGET_UNCERTAIN'), ('boot-1', 20_000_000_010, 'BUDGET_EXHAUSTED')])
def test_settled_recovery_records_current_facts_without_recharging(tmp_path, boundary, boot, t, want):
    store = opened(tmp_path)
    start(store)
    if boundary == 'RUNNING': transition(store, 'admission', 'RUNNING', 11)
    if boundary == 'CAPTURED': capture(store, t=11)
    store.settle_work(ATTEMPT, 'admission', observation(t=12))
    saved = snap(store)['works'][0]['observation_bytes_b64']
    store = CampaignStore(ExecutionStore(store.store.path))
    raw = observation(t=t, boot=boot)
    store.recover_work(ATTEMPT, 'admission', raw)
    result = snap(CampaignStore(ExecutionStore(store.store.path)))
    assert result['state'] == ('IN_DOUBT' if want == 'BOUND' and boundary != 'CAPTURED' else want)
    assert result['works'][0]['state'] == ('CAPTURED' if boundary == 'CAPTURED' else 'IN_DOUBT')
    assert result['works'][0]['observation_bytes_b64'] == saved
    assert result['settled_cpu_ns'] == 20
    assert result['last_clock'] == clock(t, boot)
    before = store.budget_snapshot(ATTEMPT)
    assert store.recover_work(ATTEMPT, 'admission', raw) == before


def signing_parent(tmp_path):
    store = opened(tmp_path)
    start(store)
    store.settle_work(ATTEMPT, 'admission', observation(t=11))
    transition(store, 'admission', 'COMPLETED', 12)
    reserve(store, 'seal', 'SEAL', 13)
    start(store, 'seal', 14)
    capture(store, 'seal', 15)
    transition(store, 'seal', 'SIGNING_INTENT', 16, dict(intent_id='fixed',
        payload_bytes_b64='eA==', key_id='key', signing_at_utc='2026-09-19T00:00:00Z'))
    store.recover_work(ATTEMPT, 'seal', observation('seal', t=17))
    return store


def signing_retry(store, name='retry', t=18):
    from c1_rail.qualification.execution.protocol import sha256
    raw = encoded(dict(limits=profile()['phases']['SEAL'], clock=clock(t),
                       input_sha256=sha256(b'x'), signing_retry_of='seal'))
    return store.reserve_work(ATTEMPT, name, 'SEAL', raw,
        expected_revision=snap(store)['authority_revision'])


def test_signing_retry_preserves_intent_and_charges_new_scope(tmp_path):
    store = signing_parent(tmp_path)
    original = snap(store)
    signing_retry(store)
    assert snap(store)['reserved_cpu_ns'] == 60
    assert snap(store)['remaining_cpu_ns'] == 999_999_900
    assert signing_retry(store) == store.budget_snapshot(ATTEMPT)
    start(store, 'retry', 19)
    transition(store, 'retry', 'RUNNING', 20)
    with pytest.raises(ValueError):
        transition(store, 'seal', 'SIGNED', 20, dict(candidate_bytes_b64='eA=='))
    store.settle_work(ATTEMPT, 'retry', observation('retry', cpu=30, t=21))
    transition(store, 'retry', 'COMPLETED', 22)
    transition(store, 'seal', 'SIGNED', 23, dict(candidate_bytes_b64='eA=='))
    result = snap(CampaignStore(ExecutionStore(store.store.path)))
    assert result['settled_cpu_ns'] == 70 and result['reserved_cpu_ns'] == 0
    assert result['authority_revision'] == original['authority_revision']
    assert result['authority_head'] == original['authority_head']
    parent = next(w for w in result['works'] if w['work_id'] == 'seal')
    old_parent = next(w for w in original['works'] if w['work_id'] == 'seal')
    assert parent['transitions'][:-1] == old_parent['transitions']
    transition(store, 'seal', 'COMPLETED', 24)


@pytest.mark.parametrize('cpu,want', [(20, 'BOUND'), (None, 'BUDGET_UNCERTAIN')])
def test_signing_retry_crash_recovery_never_refunds_usage(tmp_path, cpu, want):
    store = signing_parent(tmp_path)
    signing_retry(store)
    start(store, 'retry', 19)
    store.recover_work(ATTEMPT, 'retry', observation('retry', cpu=cpu, t=20))
    store = CampaignStore(ExecutionStore(store.store.path))
    assert snap(store)['state'] == want
    assert snap(store)['settled_cpu_ns'] == (60 if cpu is not None else 100)
    if cpu is not None:
        signing_retry(store, 'retry2', 21)
        assert snap(store)['reserved_cpu_ns'] == 60
    else:
        with pytest.raises(ValueError): signing_retry(store, 'retry2', 21)


def test_signing_retry_does_not_unlock_unrelated_or_nested_work(tmp_path):
    store = signing_parent(tmp_path)
    signing_retry(store)
    with pytest.raises(ValueError): signing_retry(store, 'parallel')
    with pytest.raises(ValueError): reserve(store, 'other', 'N1_G5', 18)
    start(store, 'retry', 19)
    with pytest.raises(ValueError):
        transition(store, 'retry', 'SIGNING_INTENT', 20, dict(intent_id='new',
            payload_bytes_b64='eA==', key_id='key', signing_at_utc='2026-09-19T00:00:00Z'))
    store.void(void_request(), now=NOW)
    with pytest.raises(ValueError): transition(store, 'retry', 'RUNNING', 20)
    store.settle_work(ATTEMPT, 'retry', observation('retry', t=21))
    assert snap(CampaignStore(ExecutionStore(store.store.path)))['validity'] == 'VOID'


def test_settled_recovery_cannot_replace_usage_with_new_counter(tmp_path):
    store = opened(tmp_path)
    start(store)
    capture(store)
    store.settle_work(ATTEMPT, 'admission', observation(t=13))
    store.recover_work(ATTEMPT, 'admission', observation(cpu=30, t=14))
    assert snap(store)['state'] == 'BUDGET_UNCERTAIN'
    assert snap(store)['settled_cpu_ns'] == 20



@pytest.mark.parametrize('field,value,want', [('memory_peak_bytes', None, 'BUDGET_UNCERTAIN'),
    ('oom_events', None, 'BUDGET_UNCERTAIN'), ('oom_events', 1, 'BUDGET_EXHAUSTED'),
    ('memory_peak_bytes', 101, 'BUDGET_EXHAUSTED')])
def test_settled_recovery_checks_current_parent_resources(tmp_path, field, value, want):
    store = opened(tmp_path)
    start(store)
    capture(store)
    store.settle_work(ATTEMPT, 'admission', observation(t=13))
    current = json.loads(observation(t=14))
    current[field] = value
    store.recover_work(ATTEMPT, 'admission', encoded(current))
    assert snap(CampaignStore(ExecutionStore(store.store.path)))['state'] == want
    assert snap(store)['settled_cpu_ns'] == 20


def test_settled_work_cannot_resume_running(tmp_path):
    store = signing_parent(tmp_path)
    signing_retry(store)
    start(store, 'retry', 19)
    store.settle_work(ATTEMPT, 'retry', observation('retry', t=20))
    with pytest.raises(ValueError): transition(store, 'retry', 'RUNNING', 21)


@pytest.mark.parametrize('change', ['payload', 'phase', 'parent', 'null', 'extra'])
def test_signing_retry_rejects_unbound_reservations(tmp_path, change):
    from c1_rail.qualification.execution.protocol import sha256
    store = signing_parent(tmp_path)
    raw = dict(limits=profile()['phases']['SEAL'], clock=clock(18),
               input_sha256=sha256(b'x'), signing_retry_of='seal')
    phase = 'SEAL'
    if change == 'payload': raw['input_sha256'] = 'f' * 64
    if change == 'phase': phase = 'N1'
    if change == 'parent': raw['signing_retry_of'] = 'admission'
    if change == 'null': raw['signing_retry_of'] = None
    if change == 'extra': raw['other'] = 1
    before = store.budget_snapshot(ATTEMPT)
    with pytest.raises(ValueError):
        store.reserve_work(ATTEMPT, 'retry', phase, encoded(raw),
            expected_revision=snap(store)['authority_revision'])
    assert store.budget_snapshot(ATTEMPT) == before


def test_signing_retry_reservation_cannot_exceed_remaining_cap(tmp_path):
    from c1_rail.qualification.execution.protocol import sha256
    p = profile()
    for limit in p['phases'].values(): limit['cpu_ns'] = 60_000_000
    store = CampaignStore(ExecutionStore(tmp_path / 'journal.sqlite'))
    store.begin_admission(request(), encoded(p), encoded(clock()))
    start(store)
    store.settle_work(ATTEMPT, 'admission', observation(cpu=20_000_000, t=11))
    store.bind_budget(ATTEMPT, contract_budget(), expected_revision=snap(store)['authority_revision'])
    for i in range(15):
        store.reserve_work(ATTEMPT, 'pending-' + str(i), 'N1_G5', encoded(dict(
            limits=p['phases']['N1_G5'], clock=clock(12), input_sha256='d'*64)),
            expected_revision=snap(store)['authority_revision'])
    store.reserve_work(ATTEMPT, 'seal', 'SEAL', encoded(dict(limits=p['phases']['SEAL'],
        clock=clock(13), input_sha256='d'*64)), expected_revision=snap(store)['authority_revision'])
    start(store, 'seal', 14)
    capture(store, 'seal', 15)
    transition(store, 'seal', 'SIGNING_INTENT', 16, dict(intent_id='fixed',
        payload_bytes_b64='eA==', key_id='key', signing_at_utc='2026-09-19T00:00:00Z'))
    store.recover_work(ATTEMPT, 'seal', observation('seal', cpu=60_000_000, t=17))
    assert snap(store)['remaining_cpu_ns'] == 20_000_000
    store.reserve_work(ATTEMPT, 'retry', 'SEAL', encoded(dict(limits=p['phases']['SEAL'],
        clock=clock(18), input_sha256=sha256(b'x'), signing_retry_of='seal')),
        expected_revision=snap(store)['authority_revision'])
    result = snap(CampaignStore(ExecutionStore(store.store.path)))
    assert result['state'] == 'BUDGET_EXHAUSTED'
    assert not any(w['work_id'] == 'retry' for w in result['works'])


def test_snapshot_rejects_changed_signing_retry_link(tmp_path):
    from c1_rail.qualification.journal_snapshot import parse_campaign_budget_snapshot
    store = signing_parent(tmp_path)
    signing_retry(store)
    state = snap(store)
    work = next(w for w in state['works'] if w['work_id'] == 'retry')
    reservation = json.loads(base64.b64decode(work['reservation_bytes_b64']))
    reservation['signing_retry_of'] = 'admission'
    work['reservation_bytes_b64'] = base64.b64encode(encoded(reservation)).decode()
    with pytest.raises(ValueError): parse_campaign_budget_snapshot(encoded(state))



def test_linked_retry_versions_snapshot_without_rewriting_v1_history(tmp_path):
    from c1_rail.qualification.journal_snapshot import parse_campaign_budget_snapshot
    store = signing_parent(tmp_path)
    before = store.budget_snapshot(ATTEMPT)
    assert json.loads(before)['schema'] == 'qualification_campaign_budget_snapshot/v1'
    with sqlite3.connect(store.store.path) as connection:
        history = connection.execute('SELECT sequence,body,sha256 FROM full_campaign_budget_events ORDER BY sequence').fetchall()
    signing_retry(store)
    result = snap(CampaignStore(ExecutionStore(store.store.path)))
    assert result['schema'] == 'qualification_campaign_budget_snapshot/v2'
    with sqlite3.connect(store.store.path) as connection:
        assert connection.execute('SELECT sequence,body,sha256 FROM full_campaign_budget_events WHERE sequence<=? ORDER BY sequence', (len(history),)).fetchall() == history
    result['schema'] = 'qualification_campaign_budget_snapshot/v1'
    with pytest.raises(ValueError): parse_campaign_budget_snapshot(encoded(result))
    assert parse_campaign_budget_snapshot(before)['schema'] == 'qualification_campaign_budget_snapshot/v1'


@pytest.mark.parametrize('void_first', [True, False])
def test_signing_retry_reservation_and_void_both_sqlite_orderings(tmp_path, void_first):
    store = signing_parent(tmp_path)
    entered, release = Event(), Event()
    def first():
        with store.store.transaction():
            if void_first: store.void(void_request(), now=NOW)
            else: signing_retry(store)
            entered.set()
            assert release.wait(10)
    def second():
        other = CampaignStore(ExecutionStore(store.store.path))
        if void_first: signing_retry(other)
        else: other.void(void_request(), now=NOW)
    with ThreadPoolExecutor(max_workers=2) as pool:
        a = pool.submit(first)
        assert entered.wait(10)
        b = pool.submit(second)
        release.set()
        a.result()
        if void_first:
            with pytest.raises(ValueError): b.result()
        else:
            b.result()
    result = snap(CampaignStore(ExecutionStore(store.store.path)))
    assert result['validity'] == 'VOID'
    assert any(w['work_id'] == 'retry' for w in result['works']) is (not void_first)
    if not void_first:
        with pytest.raises(ValueError): start(store, 'retry', 19)

@pytest.mark.parametrize('path', ['settlement', 'recovery'])
@pytest.mark.parametrize('peak,want', [(49, 'BUDGET_UNCERTAIN'), (50, 'BOUND'), (51, 'BOUND')])
def test_parent_peak_continuity_survives_restart(tmp_path, path, peak, want):
    store = opened(tmp_path)
    start(store)
    capture(store)
    store.settle_work(ATTEMPT, 'admission', observation(t=13))
    store = CampaignStore(ExecutionStore(store.store.path))
    if path == 'settlement':
        transition(store, 'admission', 'COMPLETED', 14)
        reserve(store, t=15)
        start(store, 'n1', 16)
        current = json.loads(observation('n1', t=17))
        current['memory_peak_bytes'] = peak
        store.settle_work(ATTEMPT, 'n1', encoded(current))
    else:
        current = json.loads(observation(t=14))
        current['memory_peak_bytes'] = peak
        store.recover_work(ATTEMPT, 'admission', encoded(current))
    result = snap(CampaignStore(ExecutionStore(store.store.path)))
    assert result['state'] == want
    assert result['memory_peak_bytes'] == max(50, peak)
    if want == 'BUDGET_UNCERTAIN':
        with pytest.raises(ValueError):
            reserve(store, work='later', t=18)


@pytest.mark.parametrize('bind', [False, True])
def test_plan_fetch_without_admitted_plan_is_bounded_rejection(tmp_path, bind):
    store = opened(tmp_path, bind=bind)
    store = CampaignStore(ExecutionStore(store.store.path))
    before = store.budget_snapshot(ATTEMPT)
    with pytest.raises(ValueError, match='plan'):
        store.chunk(dict(attempt_id=ATTEMPT, object_sha256='a' * 64, offset=0, length=1))
    assert store.budget_snapshot(ATTEMPT) == before


def test_queued_cancellation_bars_new_reservation_but_settlement_and_negative_facts_continue(tmp_path):
    """S2-G2: reserve_work refuses a queued operator body even before any receipt; nothing negative is barred."""
    from test_campaign_budget import profile, request
    config = profile()
    config.update(schema='qualification_campaign_budget_profile/v2', orchestration_cpu_ns={p: 10 for p in config['phases']})
    store = CampaignStore(ExecutionStore(tmp_path / 'journal.sqlite'))
    store.begin_admission(request(), encoded(config), encoded(clock()))
    store.bind_budget(ATTEMPT, contract_budget(), expected_revision=snap(store)['authority_revision'])
    start(store)
    cancel = encoded(dict(schema='qualification_campaign_request/v2', operation='VOID', attempt_id=ATTEMPT,
                          reason='stop', operator_approval_bytes='eA=='))
    store.queue_diagnostic_void(cancel)
    before = snap(store)
    with pytest.raises(ValueError, match='cancellation pending'):
        reserve(store)
    assert snap(store) == before
    measured = json.loads(observation(t=12))
    measured.update(schema='qualification_campaign_observation/v2', orchestration_charge_cpu_ns=10, termination_known=True)
    settled = json.loads(store.settle_work(ATTEMPT, 'admission', encoded(measured)))
    assert settled['works'][0]['charge_cpu_ns'] == 30 and settled['validity'] == 'VALID' and settled['state'] == 'BOUND'
    # Recovery of a started, unfinished work is a negative fact (IN_DOUBT): it commits under the barrier.
    recovered = json.loads(store.recover_work(ATTEMPT, 'admission', encoded(measured)))
    assert recovered['state'] == 'IN_DOUBT' and recovered['validity'] == 'VALID'
    assert recovered['works'][0]['charge_cpu_ns'] == 30
    assert json.loads(store.void(cancel, now=NOW))['validity'] == 'VOID'
    with pytest.raises(ValueError, match='VOID'):
        reserve(store, t=14)
    ExecutionStore(store.store.path)
