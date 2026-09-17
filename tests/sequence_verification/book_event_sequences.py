"""Opt-in generated sequences over real owners and the offline broker producer."""
from dataclasses import replace
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

from hypothesis import given, settings, strategies as st
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tests' / 'ops'))
from c1_rail.book_account_owner import BookAccountOwner, BrokerResult
from c1_signal_daemon.book_protocol import Bracket, Cancel, OrderIntent, Side
from book_protection_fixtures import ProtectionScenario
from test_book_takeover_phases import TakeoverScenario
from test_book_account_owner import NOW, SESSION, intent, owner

GENERATED = settings(max_examples=20, deadline=None, derandomize=True, database=None)
noise = st.lists(st.sampled_from(['poll', 'replay']), min_size=0, max_size=4)


def delayed(scenario, events, snapshot):
    for event in events:
        if event == 'poll':
            snapshot = scenario.poll()
        else:
            scenario.runtime.observe_takeover_inventory(snapshot, now=scenario.tick())
    return snapshot


@GENERATED
@given(before=noise, after=noise, late=st.booleans())
def test_takeover_waits_for_terminal_and_closes_late_fills(before, after, late):
    with TemporaryDirectory() as directory:
        s = TakeoverScenario(Path(directory))
        snapshot = s.poll()
        delayed(s, before, snapshot)
        assert [c.kind for c in s.broker.commands] == ['entry', 'cancel']
        cancel = s.broker.commands[-1]
        if late:
            s.broker.execute_entry(s.target, fill_id='late', quantity=1, price=101, at=s.tick())
        s.broker.apply_cancel(cancel.operation_id, at=s.tick())
        # A real broker effect is still not an observed proof.
        assert not any(c.kind == 'flat' for c in s.broker.commands)
        snapshot = s.poll()
        flat = s.broker.commands[-1]
        assert flat.kind == 'flat' and flat.quantity == 1 + int(late)
        delayed(s, after, snapshot)
        assert len([c for c in s.broker.commands if c.kind == 'flat']) == 1
        s.broker.execute_close(flat.operation_id, execution_id='finish', quantity=flat.quantity,
                               price=101, terminal=True, at=s.tick())
        snapshot = s.poll()
        s.runtime.observe_takeover_inventory(snapshot, now=s.tick())
        assert s.owner.exposure(s.leg) == (0, 0)
        assert len([c for c in s.broker.commands if c.operation_id == s.root.order_id]) == 1


@GENERATED
@given(wait=noise, terminal=st.booleans())
def test_partial_close_and_duplicate_inventory_never_send_a_second_close(wait, terminal):
    with TemporaryDirectory() as directory:
        s = TakeoverScenario(Path(directory), fill=2)
        s.poll()
        flat = next(c for c in s.broker.commands if c.kind == 'flat')
        s.broker.execute_close(flat.operation_id, execution_id='partial', quantity=1,
                               price=101, terminal=terminal, at=s.tick())
        snapshot = s.poll()
        if not terminal:
            delayed(s, wait, snapshot)
        else:
            for _ in wait:
                s.owner.resume_takeover(now=s.tick())
            assert s.owner.authority == 'INTERVENTION'
        assert s.owner.exposure(s.leg)[0] == 1
        assert len([c for c in s.broker.commands if c.kind == 'flat']) == 1
        assert not any(c.operation_id == s.root.order_id for c in s.broker.commands)


@GENERATED
@given(stage=st.sampled_from(['cancel_sent', 'cancel_applied', 'close_sent', 'undelivered_close']),
       repeats=st.integers(min_value=1, max_value=4))
def test_restart_never_replays_unresolved_commands(stage, repeats):
    with TemporaryDirectory() as directory:
        s = TakeoverScenario(Path(directory))
        s.poll()
        if stage != 'cancel_sent':
            s.broker.apply_cancel(s.broker.commands[-1].operation_id, at=s.tick())
        if stage in ('close_sent', 'undelivered_close'):
            s.poll()
        if stage == 'undelivered_close':
            flat = s.broker.commands[-1]
            s.broker.execute_close(flat.operation_id, execution_id='undelivered', quantity=1,
                                   price=101, terminal=True, at=s.tick())
        count = len(s.broker.commands)
        restarted = BookAccountOwner.boot(s.owner.path, s.owner.account,
                                          binding=s.owner.binding, synthetic_broker=s.broker)
        for _ in range(repeats):
            restarted.resume_takeover(now=s.tick())
            restarted.advance_schedule(now=s.now)
        assert restarted.authority == 'INTERVENTION'
        assert len(s.broker.commands) == count


@pytest.mark.parametrize('path', ['exit', 'flat', 'schedule'])
@GENERATED
@given(polls=st.integers(min_value=1, max_value=4), late=st.booleans())
def test_close_entrypoints_wait_for_cancel_confirmation(path, polls, late):
    with TemporaryDirectory() as directory:
        account, broker = owner(Path(directory), [BrokerResult('accepted')] * 20)
        occurrence = account.make_occurrence('direct', 'entry')
        account.dispatch(intent(), occurrence=occurrence, now=NOW)
        fact = broker.execute_entry('base', fill_id='first', quantity=1, price=100, at=NOW)
        account.observe(fact, now=NOW)
        now = SESSION.flatten_start if path == 'schedule' else NOW
        action = OrderIntent('close', 'dj30_mym_p250', path if path != 'schedule' else 'flat',
                             Side.SELL, None, bar_time=now)
        close_occurrence = account.make_occurrence('direct', 'close')
        def request_close():
            if path == 'schedule':
                return account.advance_schedule(now=now)
            return account.dispatch(action, occurrence=close_occurrence, now=now)
        initial = request_close()
        if path != 'schedule':
            assert initial.refusal_reason == 'entry_remainder_pending'
            # Ordinary closes refuse; their caller owns the separate cancel.
            account.dispatch(Cancel('dj30_mym_p250', 'base'),
                             occurrence=account.make_occurrence('direct', 'cancel'), now=now)
        for _ in range(polls):
            request_close()
        assert not any(c.kind in ('flat', 'exit') for c in broker.commands)
        cancel = next(c for c in broker.commands if c.kind == 'cancel')
        if late:
            account.observe(broker.execute_entry('base', fill_id='late', quantity=1,
                                                price=101, at=now), now=now)
        for terminal_fact in broker.apply_cancel(cancel.operation_id, at=now):
            account.observe(terminal_fact, now=now)
        if path != 'schedule':
            # A refused occurrence is immutable; retry as a new input event.
            action = replace(action, order_id='close-after-terminal')
            close_occurrence = account.make_occurrence('direct', 'close-after-terminal')
        request_close()
        closes = [c for c in broker.commands if c.kind in ('flat', 'exit')]
        assert len(closes) == 1
        assert closes[0].quantity == 1 + int(late)


@GENERATED
@given(quantity=st.integers(min_value=1, max_value=3), replays=st.integers(min_value=0, max_value=3),
       restart=st.booleans())
def test_close_feedback_waits_for_fresh_residual_protection(quantity, replays, restart):
    with TemporaryDirectory() as directory:
        case = ProtectionScenario(Path(directory))
        case.enter(bracket=Bracket(stop=98))
        stale = case.observe()
        action = replace(intent('protected-close'), kind='exit', side=Side.SELL, qty=quantity)
        case.broker.queue(BrokerResult('accepted'))
        case.dispatch(action, case.occurrence('protected-close'))
        before = case.owner.all_feedback
        for fact in case.broker.execute_close(action.order_id, execution_id='closed', quantity=quantity,
                                               price=101, terminal=True, at=case.advance()):
            assert case.owner.observe(fact, now=case.now) == ()
        for _ in range(replays):
            assert case.owner.observe_protection(stale, now=case.advance()) == ()
            assert case.owner.all_feedback == before
        assert case.owner.exposure('dj30_mym_p250') == (3 - quantity, 0)
        if restart:
            count = len(case.broker.commands)
            restarted = BookAccountOwner.boot(case.owner.path, case.owner.account,
                binding=case.owner.binding, synthetic_broker=case.broker)
            restarted.resume_closes(now=case.now)
            assert len(case.broker.commands) == count
            assert restarted.all_feedback == before
            assert restarted.permission == 'HALTED'
        else:
            snapshot = case.observe()
            assert len(case.owner.all_feedback) == len(before) + 1
            assert case.owner.observe_protection(snapshot, now=case.advance()) == ()
            assert len(case.owner.all_feedback) == len(before) + 1
