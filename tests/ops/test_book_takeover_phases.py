"""Takeover must be justified by independent broker effects, not receipts."""
from dataclasses import asdict, replace
from datetime import timedelta

import pytest

from c1_rail.book_account_owner import BrokerFact, BrokerResult
from c1_rail.book_synthetic_protection import SyntheticProtectionBroker
from c1_signal_daemon.book_protocol import Cancel
from test_four_leg_runtime import owner, entry
from test_book_account_owner import NOW


class TakeoverScenario:
    def __init__(self, path, *, leg='vanguard_mgc', qty=2, fill=1, root_cut=None, bracket=None, runtime_body=None):
        from c1_signal_daemon.book_runtime import FourLegRuntime
        from c1_signal_daemon.book_protocol import Mode
        from test_four_leg_runtime import inert_adapters
        self.owner = owner(path, [])
        occurrence = self.owner.make_occurrence('direct', 'initial')
        self.broker = SyntheticProtectionBroker([BrokerResult('accepted')] * 12,
            account=occurrence.account, account_epoch=occurrence.account_epoch, at=NOW)
        self.owner.synthetic_broker = self.broker
        self.runtime = FourLegRuntime(self.owner, inert_adapters())
        self.runtime._mode_actions(Mode.NORMAL)
        self.now = NOW
        self.leg = leg
        self.target = 'entry:' + leg
        result = self.owner.dispatch(replace(entry(leg, qty), bracket=bracket), occurrence=occurrence, now=self.now)
        self.runtime.deliver_confirmed(result)
        fact = self.broker.execute_entry(self.target, fill_id='initial-fill', quantity=fill, price=100, at=self.tick())
        self.runtime.observe_fact(fact, now=self.now)
        self.root = entry('aegis_6j', 8)
        self.owner.crash_at = root_cut
        root_occurrence = self.owner.make_occurrence('direct', 'root')
        if runtime_body is not None:
            root_occurrence = self.owner.make_occurrence('runtime', NOW.isoformat())
            for leg_id, bar_body in runtime_body.items():
                self.owner.record_partial_bar(leg_id, NOW, bar_body, acquired_at=self.now)
            self.owner.record_barrier(NOW, runtime_body, session_id=self.owner.binding['session'].session_id, mode=Mode.NORMAL)
            self.owner.record_barrier_actions(NOW, [dict(type='OrderIntent', value=asdict(self.root), occurrence=asdict(root_occurrence))])
        result = self.owner.dispatch(self.root, occurrence=root_occurrence, now=self.now)
        assert result.refusal_reason == 'takeover_pending'

    def tick(self):
        self.now += timedelta(milliseconds=100)
        self.broker.advance(self.now)
        return self.now

    def snapshot(self):
        request = self.owner.prepare_takeover_inventory(now=self.now)
        assert request is not None
        self.tick()
        return self.broker.read_inventory(request)

    def poll(self):
        from c1_rail.c1_rail_listener import handle_book_takeover_inventory
        snapshot = self.snapshot()
        handle_book_takeover_inventory(snapshot, self.runtime, now=self.now)
        return snapshot

    def cancel(self):
        self.poll()
        command = next(c for c in self.broker.commands if c.kind == 'cancel')
        self.broker.apply_cancel(command.operation_id, at=self.tick())
        self.poll()
        return next(c for c in self.broker.commands if c.kind == 'flat')


def test_complete_producer_runtime_trace_and_duplicate_inventory(tmp_path):
    s = TakeoverScenario(tmp_path)
    s.poll()
    assert [c.kind for c in s.broker.commands] == ['entry', 'cancel']
    s.poll()  # receipt and another complete inventory are not cancellation
    assert [c.kind for c in s.broker.commands] == ['entry', 'cancel']
    late = s.broker.execute_entry(s.target, fill_id='late', quantity=1, price=101, at=s.tick())
    cancel = s.broker.commands[-1]
    s.broker.apply_cancel(cancel.operation_id, at=s.tick())
    s.poll()  # late fill/terminal reach owner through inventory, before the close
    flat = s.broker.commands[-1]
    assert flat.kind == 'flat' and flat.quantity == 2, s.owner.incidents
    assert s.owner.exposure(s.leg) == (2, 0)
    s.broker.execute_close(flat.operation_id, execution_id='close', quantity=2, price=101, terminal=True, at=s.tick())
    snapshot = s.poll()
    assert [c.kind for c in s.broker.commands] == ['entry', 'cancel', 'flat', 'entry']
    assert s.broker.commands[-1].operation_id == s.root.order_id
    s.runtime.observe_takeover_inventory(snapshot, now=s.tick())
    s.owner.resume_takeover(now=s.now)
    assert len(s.broker.commands) == 4
    assert s.owner.exposure(s.leg) == (0, 0)
    assert s.owner.exposure('aegis_6j') == (0, 8)
    assert s.owner.pending_feedback == ()
    assert s.owner.authority == 'NORMAL'


@pytest.mark.parametrize('change', ['incomplete', 'foreign', 'future', 'positions'])
def test_bad_inventory_never_authorizes_controls(tmp_path, change):
    s = TakeoverScenario(tmp_path)
    snap = s.snapshot()
    values = {'incomplete': {'complete': False}, 'foreign': {'account_epoch': 'foreign'},
              'future': {'as_of': s.now + timedelta(seconds=1)}, 'positions': {'positions': ()}}
    s.runtime.observe_takeover_inventory(replace(snap, **values[change]), now=s.now)
    assert len(s.broker.commands) == 1


def test_partial_terminal_close_intervenes_without_second_close(tmp_path):
    s = TakeoverScenario(tmp_path, fill=2)
    s.poll()  # already filled terminal: no cancellation needed
    flat = next(c for c in s.broker.commands if c.kind == 'flat')
    assert s.owner.authority == 'NORMAL'
    s.broker.execute_close(flat.operation_id, execution_id='partial', quantity=1, price=101, terminal=True, at=s.tick())
    s.poll()
    assert s.owner.authority == 'INTERVENTION'
    assert s.owner.exposure(s.leg) == (1, 0)
    s.owner.resume_takeover(now=s.tick())
    assert len([c for c in s.broker.commands if c.kind == 'flat']) == 1


def test_restart_after_cancel_never_resends(tmp_path):
    from c1_rail.book_account_owner import BookAccountOwner
    s = TakeoverScenario(tmp_path)
    s.poll()
    count = len(s.broker.commands)
    restarted = BookAccountOwner.boot(s.owner.path, s.owner.account, binding=s.owner.binding, synthetic_broker=s.broker)
    restarted.resume_takeover(now=s.tick())
    assert restarted.authority == 'INTERVENTION'
    assert len(s.broker.commands) == count


def ready_without_attempt(s):
    flat = s.cancel()
    s.broker.execute_close(flat.operation_id, execution_id='complete', quantity=flat.quantity,
                           price=101, terminal=True, at=s.tick())
    snap = s.snapshot()
    events = s.owner.observe_takeover_inventory(snap, now=s.now)
    s.runtime.deliver_confirmed_events(events)
    controls, done = s.owner.advance_takeover(now=s.now)
    assert done and not controls
    return snap


@pytest.mark.parametrize('invalid', ['policy', 'lifecycle', 'settlement', 'allocation', 'source', 'proof_age'])
def test_final_admission_rechecks_retained_request(tmp_path, invalid):
    s = TakeoverScenario(tmp_path)
    ready_without_attempt(s)
    if invalid == 'policy':
        s.owner.binding['policy_digest'] = 'e' * 64
    elif invalid == 'lifecycle':
        s.owner.binding['lifecycle_tiers']['aegis_6j'] = 'WATCH-1'
    elif invalid == 'settlement':
        s.owner.binding['settlement'] = replace(s.owner.binding['settlement'], equity=98500)
    elif invalid == 'allocation':
        s.owner.binding['cap_allocations']['aegis_6j'] = 70
    elif invalid == 'source':
        s.now += timedelta(minutes=16)
        s.owner.binding['max_evidence_age'] = timedelta(hours=2)
        s.owner.binding['valid_until'] = s.now + timedelta(minutes=1)
    else:
        s.now += timedelta(seconds=31)
        s.owner.binding['as_of'] = s.now  # cannot refresh proof through account metadata
    s.owner.resume_takeover(now=s.now)
    assert not any(c.operation_id == s.root.order_id for c in s.broker.commands)
    assert s.owner.exposure('aegis_6j') == (0, 0)


def test_halt_after_proof_preserves_displaced_history(tmp_path):
    s = TakeoverScenario(tmp_path)
    ready_without_attempt(s)
    before = s.owner.observable_accounting()
    s.owner.halt('operator', 'operator', now=s.now)
    s.owner.resume_takeover(now=s.now)
    assert not any(c.operation_id == s.root.order_id for c in s.broker.commands)
    assert s.owner.observable_accounting()['operations'] == before['operations']


def test_old_inventory_cannot_qualify_after_new_cancel_attempt(tmp_path):
    s = TakeoverScenario(tmp_path)
    old = s.poll()
    s.runtime.observe_takeover_inventory(old, now=s.tick())
    assert [c.kind for c in s.broker.commands] == ['entry', 'cancel']


@pytest.mark.parametrize('outcome', ['unknown', 'rejected'])
def test_cancel_failure_fences_and_retains_exposure(tmp_path, outcome):
    s = TakeoverScenario(tmp_path)
    s.broker._results[:] = [BrokerResult(outcome)]
    s.poll()
    assert s.owner.authority == 'INTERVENTION'
    assert s.owner.exposure(s.leg) == (1, 1)
    s.owner.resume_takeover(now=s.tick())
    assert not any(c.kind == 'flat' for c in s.broker.commands)


def test_missing_phase_table_fails_without_repair(tmp_path):
    import sqlite3
    from c1_rail.book_account_owner import BookAccountOwner, AccountOwnerError
    s = TakeoverScenario(tmp_path)
    with sqlite3.connect(s.owner.path) as db:
        db.execute('DROP TABLE takeover_reads')
    with pytest.raises(AccountOwnerError):
        BookAccountOwner.boot(s.owner.path, s.owner.account, binding=s.owner.binding, synthetic_broker=s.broker)
    with sqlite3.connect(s.owner.path) as db:
        assert db.execute("SELECT 1 FROM sqlite_master WHERE name='takeover_reads'").fetchone() is None


@pytest.mark.parametrize('table', ['takeover_children', 'takeover_events', 'takeover_streams', 'takeover_inventory', 'takeover_plans'])
def test_missing_durable_record_is_corruption(tmp_path, table):
    import sqlite3
    from c1_rail.book_account_owner import BookAccountOwner, AccountOwnerError
    s = TakeoverScenario(tmp_path)
    s.poll()
    with sqlite3.connect(s.owner.path) as db:
        db.execute('DELETE FROM ' + table)
    with pytest.raises(AccountOwnerError):
        BookAccountOwner.boot(s.owner.path, s.owner.account, binding=s.owner.binding, synthetic_broker=s.broker)


@pytest.mark.parametrize('cut', ['PLAN', 'CONFIRM_CANCELLATIONS', 'CLOSE_DISPLACED', 'REVALIDATE', 'ATTEMPTED'])
def test_durable_phase_crash_has_no_restart_authority(tmp_path, cut):
    from c1_rail.book_account_owner import BookAccountOwner, SimulatedOwnerCrash
    if cut == 'PLAN':
        s = TakeoverScenario.__new__(TakeoverScenario)
        with pytest.raises(SimulatedOwnerCrash):
            s.__init__(tmp_path, root_cut='takeover:PLAN')
    else:
        s = TakeoverScenario(tmp_path)
        s.owner.crash_at = 'takeover:' + cut
        with pytest.raises(SimulatedOwnerCrash):
            s.poll()
            cancel = next(c for c in s.broker.commands if c.kind == 'cancel')
            s.broker.apply_cancel(cancel.operation_id, at=s.tick())
            s.poll()
            flat = next(c for c in s.broker.commands if c.kind == 'flat')
            s.broker.execute_close(flat.operation_id, execution_id='finish', quantity=flat.quantity, price=101, terminal=True, at=s.tick())
            s.poll()
    count = len(s.broker.commands)
    restarted = BookAccountOwner.boot(s.owner.path, s.owner.account, binding=s.owner.binding, synthetic_broker=s.broker)
    restarted.resume_takeover(now=s.tick())
    assert restarted.authority == 'INTERVENTION'
    assert len(s.broker.commands) == count


def test_duplicate_partial_close_cannot_mutate_producer(tmp_path):
    s = TakeoverScenario(tmp_path, fill=2)
    s.poll()
    flat = s.broker.commands[-1]
    s.broker.execute_close(flat.operation_id, execution_id='dup', quantity=1, price=100, terminal=False, at=s.tick())
    before = s.snapshot()
    with pytest.raises(ValueError):
        s.broker.execute_close(flat.operation_id, execution_id='dup', quantity=1, price=100, terminal=False, at=s.tick())
    after = s.snapshot()
    assert after.positions == before.positions
    assert after.facts == before.facts
    assert after.working_orders == before.working_orders


def test_incomplete_causal_envelope_cannot_change_identity(tmp_path):
    s = TakeoverScenario(tmp_path)
    s.poll()
    s.broker.execute_entry(s.target, fill_id='late', quantity=1, price=100, at=s.tick())
    s.broker.apply_cancel(s.broker.commands[-1].operation_id, at=s.tick())
    complete = s.snapshot()
    incomplete = replace(complete, facts=tuple(f for f in complete.facts if f.fact_id != 'late'))
    s.owner.observe_takeover_inventory(incomplete, now=s.now)
    assert s.owner.authority == 'NORMAL'
    s.runtime.observe_takeover_inventory(complete, now=s.now)
    assert s.owner.authority == 'INTERVENTION'
    assert not any(c.kind == 'flat' for c in s.broker.commands)


def test_ordinary_cancel_history_is_not_foreign_to_takeover(tmp_path):
    account = owner(tmp_path, [])
    occurrence = account.make_occurrence('direct', 'start')
    broker = SyntheticProtectionBroker([BrokerResult('accepted')] * 10, account=occurrence.account,
                                       account_epoch=occurrence.account_epoch, at=NOW)
    account.synthetic_broker = broker
    account.dispatch(entry('vanguard_mgc', 2), occurrence=occurrence, now=NOW)
    fact = broker.execute_entry('entry:vanguard_mgc', fill_id='f', quantity=1, price=100, at=NOW)
    account.observe(fact, now=NOW)
    result = account.dispatch(Cancel('vanguard_mgc', 'entry:vanguard_mgc'),
        occurrence=account.make_occurrence('direct', 'ordinary-cancel'), now=NOW)
    for fact in broker.apply_cancel(result.operation_id, at=NOW):
        account.observe(fact, now=NOW)
    account.dispatch(entry('aegis_6j', 8), occurrence=account.make_occurrence('direct', 'root'), now=NOW)
    request = account.prepare_takeover_inventory(now=NOW)
    broker.advance(NOW + timedelta(seconds=1))
    account.observe_takeover_inventory(broker.read_inventory(request), now=broker.now)
    account.resume_takeover(now=broker.now)
    assert account.authority == 'NORMAL', account.incidents
    assert broker.commands[-1].kind == 'flat'


def test_failed_phase_storage_suppresses_later_sends(tmp_path):
    import sqlite3
    from c1_rail.book_account_owner import AccountOwnerError
    s = TakeoverScenario(tmp_path)
    snap = s.snapshot()
    s.owner.observe_takeover_inventory(snap, now=s.now)
    with sqlite3.connect(s.owner.path) as db:
        db.execute("CREATE TRIGGER fail_phase BEFORE INSERT ON takeover_events BEGIN SELECT RAISE(ABORT, 'storage unavailable'); END")
    with pytest.raises(AccountOwnerError):
        s.owner.resume_takeover(now=s.now)
    with sqlite3.connect(s.owner.path) as db:
        db.execute('DROP TRIGGER fail_phase')
    s.owner.resume_takeover(now=s.tick())
    assert len(s.broker.commands) == 1


def test_failed_inventory_incident_storage_suppresses_later_sends(tmp_path):
    import sqlite3
    from c1_rail.book_account_owner import AccountOwnerError
    s = TakeoverScenario(tmp_path)
    snapshot = s.snapshot()
    with sqlite3.connect(s.owner.path) as db:
        db.execute("CREATE TRIGGER fail_incident BEFORE INSERT ON incidents BEGIN SELECT RAISE(ABORT, 'storage unavailable'); END")
    with pytest.raises(AccountOwnerError):
        s.owner.observe_takeover_inventory(replace(snapshot, account_epoch='foreign'), now=s.now)
    with sqlite3.connect(s.owner.path) as db:
        db.execute('DROP TRIGGER fail_incident')
    s.owner.observe_takeover_inventory(snapshot, now=s.now)
    s.owner.resume_takeover(now=s.tick())
    assert len(s.broker.commands) == 1


@pytest.mark.parametrize('version', [1, 2])
def test_legacy_schema_refusal_is_nonmutating(tmp_path, version):
    import sqlite3
    from c1_rail.book_account_owner import AccountOwnerError, BookAccountOwner
    s = TakeoverScenario(tmp_path)
    with sqlite3.connect(s.owner.path) as db:
        db.execute('UPDATE owner_state SET schema=?', (version,))
    before = s.owner.path.read_bytes()
    with pytest.raises(AccountOwnerError, match='legacy schema requires explicit migration'):
        BookAccountOwner.boot(s.owner.path, s.owner.account, binding=s.owner.binding, synthetic_broker=s.broker)
    assert s.owner.path.read_bytes() == before
    assert len(s.broker.commands) == 1


def test_fresh_complete_envelope_resolves_prior_missing_fill(tmp_path):
    s = TakeoverScenario(tmp_path)
    s.poll()
    s.broker.execute_entry(s.target, fill_id='late', quantity=1, price=100, at=s.tick())
    s.broker.apply_cancel(s.broker.commands[-1].operation_id, at=s.tick())
    complete = s.snapshot()
    s.runtime.observe_takeover_inventory(replace(complete, facts=tuple(f for f in complete.facts if f.fact_id != 'late')), now=s.now)
    assert s.owner.authority == 'NORMAL'
    assert not any(c.kind == 'flat' for c in s.broker.commands)
    s.poll()
    assert s.broker.commands[-1].kind == 'flat'
    assert s.broker.commands[-1].quantity == 2


def test_invalid_final_inventory_member_rolls_back_late_fill(tmp_path):
    s = TakeoverScenario(tmp_path)
    s.poll()
    s.broker.execute_entry(s.target, fill_id='late', quantity=1, price=100, at=s.tick())
    s.broker.apply_cancel(s.broker.commands[-1].operation_id, at=s.tick())
    snapshot = s.snapshot()
    s.runtime.observe_takeover_inventory(replace(snapshot, positions=()), now=s.now)
    assert s.owner.exposure(s.leg) == (1, 1)
    assert not any(r['fact_id'] == 'late' for r in s.owner.all_feedback)
    assert s.owner.authority == 'INTERVENTION'


@pytest.mark.parametrize('cut', ['after_reservation', 'before_send', 'after_send'])
def test_takeover_control_attempt_crash_never_retries(tmp_path, cut):
    from c1_rail.book_account_owner import BookAccountOwner, SimulatedOwnerCrash
    s = TakeoverScenario(tmp_path)
    s.owner.crash_at = cut
    with pytest.raises(SimulatedOwnerCrash):
        s.poll()
    count = len(s.broker.commands)
    restarted = BookAccountOwner.boot(s.owner.path, s.owner.account, binding=s.owner.binding, synthetic_broker=s.broker)
    restarted.resume_takeover(now=s.tick())
    assert len(s.broker.commands) == count


def test_new_pending_inventory_invalidates_ready_proof(tmp_path):
    s = TakeoverScenario(tmp_path)
    ready_without_attempt(s)
    snap = s.snapshot()
    request = replace(snap.requests[-1], status='pending', terminal_fact_id=None)
    s.owner.observe_takeover_inventory(replace(snap, requests=snap.requests[:-1] + (request,)), now=s.now)
    s.owner.resume_takeover(now=s.now)
    assert not any(c.operation_id == s.root.order_id for c in s.broker.commands)


def test_mixed_legs_close_in_priority_order(tmp_path):
    # Start with ORB, then add Vanguard before requesting the Aegis takeover.
    account = owner(tmp_path, [])
    occurrence = account.make_occurrence('direct', 'initial')
    broker = SyntheticProtectionBroker([BrokerResult('accepted')] * 20, account=occurrence.account,
                                       account_epoch=occurrence.account_epoch, at=NOW)
    account.synthetic_broker = broker
    for leg_id, qty in [('orb_mnq_v7', 1), ('vanguard_mgc', 2)]:
        action = entry(leg_id, qty)
        account.dispatch(action, occurrence=account.make_occurrence('direct', leg_id), now=NOW)
        account.observe(broker.execute_entry(action.order_id, fill_id=leg_id, quantity=qty, price=100, at=NOW), now=NOW)
    account.dispatch(entry('aegis_6j', 8), occurrence=account.make_occurrence('direct', 'root'), now=NOW)
    now = NOW
    for expected in ['orb_mnq_v7', 'vanguard_mgc']:
        request = account.prepare_takeover_inventory(now=now)
        now += timedelta(seconds=1)
        broker.advance(now)
        account.observe_takeover_inventory(broker.read_inventory(request), now=now)
        account.resume_takeover(now=now)
        flat = broker.commands[-1]
        assert (flat.kind, flat.leg_id) == ('flat', expected)
        broker.execute_close(flat.operation_id, execution_id='close:' + expected, quantity=flat.quantity,
                             price=100, terminal=True, at=now)
    request = account.prepare_takeover_inventory(now=now)
    now += timedelta(seconds=1)
    broker.advance(now)
    account.observe_takeover_inventory(broker.read_inventory(request), now=now)
    account.resume_takeover(now=now)
    assert broker.commands[-1].operation_id == 'entry:aegis_6j'


def test_consumed_owner_pending_amendment_blocks_quiescence(tmp_path):
    from c1_signal_daemon.book_protocol import Bracket, BracketAmend
    s = TakeoverScenario(tmp_path, fill=2, bracket=Bracket(stop=98))
    snapshot = s.snapshot()
    s.runtime.deliver_confirmed_events(s.owner.observe_takeover_inventory(snapshot, now=s.now))
    occurrence = s.owner.make_occurrence('direct', 'tighten')
    amend = BracketAmend(s.leg, Bracket(stop=99), ('initial-fill',))
    waiting = s.owner.dispatch(amend, occurrence=occurrence, now=s.now)
    assert waiting.refusal_reason == 'awaiting_evidence'
    s.tick()
    pending = s.owner.dispatch(amend, occurrence=occurrence, now=s.now)
    assert pending.transport_state == 'accepted'
    before = s.owner.protection_owners[0]
    event = s.broker.execute_protection('protection:initial-fill', quantity=2, price=98, terminal=True, at=s.tick())
    s.runtime.observe_protection_execution(event, now=s.now)
    after = s.owner.protection_owners[0]
    assert after.consumed and after.pending_operation == before.pending_operation
    assert after.deadline == before.deadline
    s.poll()
    assert not any(c.operation_id == s.root.order_id for c in s.broker.commands)
    assert s.owner.protection_owners[0].pending_operation == before.pending_operation


def test_unknown_working_order_prevents_quiescence(tmp_path):
    from c1_rail.book_takeover import WorkingOrder
    s = TakeoverScenario(tmp_path)
    flat = s.cancel()
    s.broker.execute_close(flat.operation_id, execution_id='close', quantity=flat.quantity, price=100, terminal=True, at=s.tick())
    # Fault injection into the independent broker, not a hand-authored zero proof.
    s.broker._working['external'] = WorkingOrder('external-order', 'external', s.leg, 'MGC1!', 'entry', 1)
    s.poll()
    assert s.owner.authority == 'INTERVENTION'
    assert not any(c.operation_id == s.root.order_id for c in s.broker.commands)


def test_inventory_cannot_predate_its_close_facts(tmp_path):
    s = TakeoverScenario(tmp_path)
    flat = s.cancel()
    request = s.owner.prepare_takeover_inventory(now=s.now)
    old = s.tick()
    s.broker.execute_close(flat.operation_id, execution_id='close', quantity=flat.quantity, price=100, terminal=True, at=s.tick())
    snap = s.broker.read_inventory(request)
    snap = replace(snap, as_of=old, protection=replace(snap.protection, as_of=old))
    s.runtime.observe_takeover_inventory(snap, now=s.now)
    assert not any(c.operation_id == s.root.order_id for c in s.broker.commands)
    assert s.owner.authority == 'INTERVENTION'


def test_inventory_cannot_predate_already_delivered_close(tmp_path):
    s = TakeoverScenario(tmp_path)
    flat = s.cancel()
    old = s.tick()
    facts = s.broker.execute_close(flat.operation_id, execution_id='close', quantity=flat.quantity,
                                   price=100, terminal=True, at=s.tick())
    for fact in facts:
        s.runtime.observe_fact(fact, now=s.now)
    request = s.owner.prepare_takeover_inventory(now=old - timedelta(milliseconds=1))
    snap = s.broker.read_inventory(request)
    snap = replace(snap, facts=(), as_of=old, protection=replace(snap.protection, as_of=old))
    s.runtime.observe_takeover_inventory(snap, now=s.now)
    assert not any(c.operation_id == s.root.order_id for c in s.broker.commands)


@pytest.mark.parametrize('field', ['quantity', 'scope_operations', 'admission_binding', 'request', 'generation'])
def test_missing_plan_field_fails_boot(tmp_path, field):
    import json
    import sqlite3
    from c1_rail.book_account_owner import BookAccountOwner, AccountOwnerError
    s = TakeoverScenario(tmp_path)
    with sqlite3.connect(s.owner.path) as db:
        plan = json.loads(db.execute('SELECT body FROM takeover_plans').fetchone()[0])
        del plan[field]
        db.execute('UPDATE takeover_plans SET body=?', (json.dumps(plan),))
    with pytest.raises(AccountOwnerError):
        BookAccountOwner.boot(s.owner.path, s.owner.account, binding=s.owner.binding, synthetic_broker=s.broker)


@pytest.mark.parametrize('complete', [False, True])
def test_runtime_takeover_requires_complete_source_boundary(tmp_path, complete):
    from test_four_leg_runtime import bars
    body = {leg_id: asdict(bar) for leg_id, bar in bars().items()} if complete else {}
    s = TakeoverScenario(tmp_path, runtime_body=body)
    ready_without_attempt(s)
    s.owner.resume_takeover(now=s.now)
    assert any(c.operation_id == s.root.order_id for c in s.broker.commands) is complete


def test_halt_is_retained_in_takeover_phase_history(tmp_path):
    import sqlite3
    s = TakeoverScenario(tmp_path)
    s.poll()
    s.owner.halt('operator', 'operator', now=s.now)
    s.owner.halt('operator', 'operator', now=s.now)
    with sqlite3.connect(s.owner.path) as db:
        kinds = [r[0] for r in db.execute('SELECT kind FROM takeover_events ORDER BY ordinal')]
    assert kinds == ['PLAN', 'CANCEL', 'CONFIRM_CANCELLATIONS', 'HALT']


@pytest.mark.parametrize('cut', ['after_reservation', 'before_send', 'after_send'])
def test_retained_aegis_attempt_crash_never_retries(tmp_path, cut):
    from c1_rail.book_account_owner import BookAccountOwner, SimulatedOwnerCrash
    s = TakeoverScenario(tmp_path)
    ready_without_attempt(s)
    s.owner.crash_at = cut
    with pytest.raises(SimulatedOwnerCrash):
        s.owner.resume_takeover(now=s.now)
    count = len(s.broker.commands)
    restarted = BookAccountOwner.boot(s.owner.path, s.owner.account, binding=s.owner.binding, synthetic_broker=s.broker)
    restarted.resume_takeover(now=s.tick())
    assert len(s.broker.commands) == count


@pytest.mark.parametrize('displaced', [False, True])
def test_cutoff_retires_only_root_and_retains_effects(tmp_path, displaced):
    s = TakeoverScenario(tmp_path)
    if displaced:
        ready_without_attempt(s)
    s.owner.resume_takeover(now=s.owner.binding['session'].risk_add_cutoff)
    assert not any(c.operation_id == s.root.order_id for c in s.broker.commands)
    assert s.owner.exposure(s.leg) == ((0, 0) if displaced else (1, 1))
    assert s.owner.exposure('aegis_6j') == (0, 0)
    assert s.owner.authority == 'SCHEDULED_EXIT'


def test_late_inventory_after_halt_updates_accounting_without_send(tmp_path):
    s = TakeoverScenario(tmp_path)
    flat = s.cancel()
    s.broker.execute_close(flat.operation_id, execution_id='late-close', quantity=flat.quantity,
                           price=100, terminal=True, at=s.tick())
    snapshot = s.snapshot()
    s.owner.halt('operator', 'operator', now=s.now)
    count = len(s.broker.commands)
    s.runtime.observe_takeover_inventory(snapshot, now=s.now)
    assert s.owner.exposure(s.leg) == (0, 0)
    assert s.owner.authority == 'INTERVENTION'
    assert len(s.broker.commands) == count


def test_serialized_halt_wins_race_with_ready_takeover(tmp_path, monkeypatch):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Event
    s = TakeoverScenario(tmp_path)
    ready_without_attempt(s)
    locked, release, started = Event(), Event(), Event()
    original = s.owner._halt_db
    def paused_halt(*args):
        locked.set()
        assert release.wait(5)
        return original(*args)
    monkeypatch.setattr(s.owner, '_halt_db', paused_halt)
    def resume():
        started.set()
        return s.owner.resume_takeover(now=s.now)
    count = len(s.broker.commands)
    with ThreadPoolExecutor(max_workers=2) as pool:
        halt = pool.submit(s.owner.halt, 'race', 'operator', now=s.now)
        assert locked.wait(5)
        sender = pool.submit(resume)
        try:
            assert started.wait(5)
        finally:
            release.set()
        halt.result(timeout=5)
        sender.result(timeout=5)
    assert len(s.broker.commands) == count
    assert s.owner.authority == 'INTERVENTION'


@pytest.mark.parametrize('cumulative', [-1, False, 0, 3])
def test_impossible_terminal_cumulative_is_an_incident(tmp_path, cumulative):
    s = TakeoverScenario(tmp_path)
    s.poll()
    s.broker.apply_cancel(s.broker.commands[-1].operation_id, at=s.tick())
    snapshot = s.snapshot()
    snapshot = replace(snapshot, facts=tuple(replace(f, cumulative_filled=cumulative)
                       if f.kind == 'terminal' else f for f in snapshot.facts))
    s.runtime.observe_takeover_inventory(snapshot, now=s.now)
    assert s.owner.authority == 'INTERVENTION'
    assert s.owner.exposure(s.leg) == (1, 1)


def test_known_terminal_conflict_cannot_hide_as_missing_fill(tmp_path):
    s = TakeoverScenario(tmp_path)
    s.cancel()
    snapshot = s.snapshot()
    snapshot = replace(snapshot, facts=tuple(replace(f, cumulative_filled=2)
                       if f.kind == 'terminal' else f for f in snapshot.facts))
    s.runtime.observe_takeover_inventory(snapshot, now=s.now)
    assert s.owner.authority == 'INTERVENTION'


def test_no_close_before_displaced_entry_terminal(tmp_path):
    account = owner(tmp_path, [])
    account.dispatch(entry('orb_mnq_v7', 1), occurrence=account.make_occurrence('direct', 'orb'), now=NOW)
    account.observe(BrokerFact.fill('orb-fill', 'entry:orb_mnq_v7', 'orb_mnq_v7', 'entry', 1, 100, NOW), now=NOW)
    account.dispatch(entry('aegis_6j', 8), occurrence=account.make_occurrence('direct', 'aegis'), now=NOW)
    account.advance_takeover(now=NOW)
    assert not any(c.kind == 'flat' for c in account.synthetic_broker.commands)


def test_producer_cancel_removes_remainder_and_retains_late_fill(tmp_path):
    from c1_rail import book_takeover as t
    account = owner(tmp_path, [])
    occurrence = account.make_occurrence('direct', 'base')
    broker = SyntheticProtectionBroker(account=occurrence.account, account_epoch=occurrence.account_epoch, at=NOW)
    account.synthetic_broker = broker
    account.dispatch(entry('vanguard_mgc', 2), occurrence=occurrence, now=NOW)
    broker.execute_entry('entry:vanguard_mgc', fill_id='f1', quantity=1, price=100, at=NOW)
    account.dispatch(Cancel('vanguard_mgc', 'entry:vanguard_mgc'), occurrence=account.make_occurrence('direct', 'cancel'), now=NOW)
    cancel = broker.commands[-1]
    request = t.InventoryRead('read', occurrence, ('vanguard_mgc',), NOW, 0)
    broker.advance(NOW + timedelta(seconds=1))
    pending = broker.read_inventory(request)
    assert pending.working_orders[0].remaining == 1
    assert next(r for r in pending.requests if r.operation_id == cancel.operation_id).status == 'pending'
    broker.execute_entry('entry:vanguard_mgc', fill_id='f2', quantity=1, price=100, at=broker.now)
    facts = broker.apply_cancel(cancel.operation_id, at=broker.now)
    assert facts[-1].status == 'filled'
    assert facts[-1].cumulative_filled == 2
    snapshot = broker.read_inventory(request)
    assert snapshot.working_orders == ()
    assert sum(p.remaining for p in snapshot.positions) == 2
    assert broker.apply_cancel(cancel.operation_id, at=broker.now) == facts
    with pytest.raises(ValueError):
        broker.execute_entry('entry:vanguard_mgc', fill_id='f3', quantity=1, price=100, at=broker.now)
