"""A close is complete only after its execution and residual protection agree."""
from dataclasses import replace
from datetime import timedelta
import sqlite3

import pytest

from c1_rail.book_account_owner import BookAccountOwner, BrokerFact, BrokerResult
from c1_rail.book_protection import ProtectionRead
from c1_signal_daemon.book_protocol import Bracket, Side
from book_protection_fixtures import ProtectionScenario
from test_book_account_owner import NOW, binding, intent, owner


def close(identity, *, quantity=None, scope=None):
    return replace(intent(identity), kind='exit', side=Side.SELL, qty=quantity, scope_fill_ids=scope)


def status(account, identity):
    with sqlite3.connect(account.path) as db:
        return db.execute('SELECT status FROM operations WHERE operation_id=?', (identity,)).fetchone()[0]


def test_filled_terminal_is_journal_evidence_not_cancellation(tmp_path):
    account, _ = owner(tmp_path, [BrokerResult('unknown')])
    account.dispatch(intent(), occurrence=account.make_occurrence('direct', 'entry'), now=NOW)
    at = NOW + timedelta(seconds=1)
    account.observe(BrokerFact.fill('filled', 'base', 'dj30_mym_p250', 'entry', 3, 100, at), now=at)
    before = account.all_feedback
    terminal = BrokerFact.terminal('base', 'filled', 3, at)
    assert account.observe(terminal, now=at) == ()
    assert account.all_feedback == before
    with account._transaction() as db:
        assert account._ordinary_unknown_orders_db(db, now=at) == ()
    restarted = BookAccountOwner.boot(account.path, account.account, binding=binding())
    assert restarted.all_feedback == before


@pytest.mark.parametrize('outcome', ['accepted', 'unknown'])
def test_close_demands_queue_per_symbol_without_reserving_or_sending_twice(tmp_path, outcome):
    account, broker = owner(tmp_path, [BrokerResult('accepted'), BrokerResult(outcome)])
    account.dispatch(intent(), occurrence=account.make_occurrence('direct', 'entry'), now=NOW)
    for fid, qty in [('a', 1), ('b', 2)]:
        account.observe(BrokerFact.fill(fid, 'base', 'dj30_mym_p250', 'entry', qty, 100, NOW), now=NOW)
    account.dispatch(close('first', scope=('a',)), occurrence=account.make_occurrence('direct', 'first'), now=NOW)
    occurrence = account.make_occurrence('direct', 'second')
    queued = account.dispatch(close('second', scope=('b',)), occurrence=occurrence, now=NOW)
    assert queued.refusal_reason == 'close_pending'
    assert account.occurrence_state(occurrence)['state'] == 'close_pending'
    assert len(broker.commands) == 2
    at = NOW + timedelta(seconds=1)
    account.observe(BrokerFact.terminal('first', 'cancelled', 0, at), now=at)
    broker.queue(BrokerResult('accepted'))
    results = account.resume_closes(now=at)
    assert results[0].transport_state == 'accepted' and results[0].quantity == 2
    assert len(broker.commands) == 3
    account.resume_closes(now=at)
    assert len(broker.commands) == 3


@pytest.mark.parametrize('quantity', [1, 3])
def test_protected_close_withholds_completion_and_feedback_until_snapshot(tmp_path, quantity):
    case = ProtectionScenario(tmp_path)
    case.enter(bracket=Bracket(stop=98))
    case.broker.queue(BrokerResult('accepted'))
    case.dispatch(close('close', quantity=quantity), case.occurrence('close'))
    before = case.owner.all_feedback
    facts = case.broker.execute_close('close', execution_id='closed', quantity=quantity,
                                      price=100, terminal=True, at=case.advance())
    for fact in facts:
        assert case.owner.observe(fact, now=case.now) == ()
    assert case.owner.exposure('dj30_mym_p250') == (3-quantity, 0)
    assert case.owner.all_feedback == before
    assert status(case.owner, 'close') == 'awaiting_protection'
    other = replace(intent('orb'), leg_id='orb_mnq_v7', qty=1)
    assert case.dispatch(other, case.occurrence('orb')).refusal_reason == 'close_unreconciled'
    # Snapshot after the fill, including its complete residual inventory.
    prepared = case.now
    case.advance()
    snapshot = case.broker.read_protection(ProtectionRead(
        case.occurrence('snapshot'), ('dj30_mym_p250',), prepared))
    events = case.owner.observe_protection(snapshot, now=case.now)
    assert len(events) == 1 and events[0].event == 'fill'
    assert status(case.owner, 'close') == 'terminal'
    assert case.protection('base').quantity == 3-quantity
    assert case.protection('base').consumed == (quantity == 3)
    assert case.owner.observe_protection(snapshot, now=case.now) == ()


def test_orphaned_protection_snapshot_halts_without_releasing_feedback(tmp_path):
    case = ProtectionScenario(tmp_path)
    case.enter(bracket=Bracket(stop=98))
    original = case.observe()
    case.broker.queue(BrokerResult('accepted'))
    case.dispatch(close('close'), case.occurrence('close'))
    for fact in case.broker.execute_close('close', execution_id='closed', quantity=3,
                                         price=100, terminal=True, at=case.advance()):
        case.owner.observe(fact, now=case.now)
    before = case.owner.all_feedback
    invalid = replace(original, fact_id='orphan', sequence=original.sequence+10,
                      as_of=case.advance(), positions=())
    assert case.owner.observe_protection(invalid, now=case.now) == ()
    assert case.owner.authority == 'INTERVENTION'
    assert case.owner.all_feedback == before
    assert status(case.owner, 'close') == 'awaiting_protection'


def test_protection_obligation_and_close_queue_survive_restart_without_sends(tmp_path):
    case = ProtectionScenario(tmp_path)
    case.enter(bracket=Bracket(stop=98))
    case.broker.queue(BrokerResult('accepted'))
    case.dispatch(close('close', quantity=1), case.occurrence('close'))
    for fact in case.broker.execute_close('close', execution_id='closed', quantity=1,
                                         price=100, terminal=True, at=case.advance()):
        case.owner.observe(fact, now=case.now)
    assert case.dispatch(close('queued'), case.occurrence('queued')).refusal_reason == 'close_pending'
    restarted = BookAccountOwner.boot(case.owner.path, case.owner.account, binding=binding(), synthetic_broker=case.broker)
    sends = len(case.broker.commands)
    assert restarted.resume_closes(now=case.now) == ()
    assert len(case.broker.commands) == sends
    assert status(restarted, 'close') == 'awaiting_protection'
    assert restarted.permission == 'HALTED'


def test_missing_residual_protection_evidence_expires_to_intervention(tmp_path):
    case = ProtectionScenario(tmp_path)
    case.enter(bracket=Bracket(stop=98))
    case.broker.queue(BrokerResult('accepted'))
    case.dispatch(close('close'), case.occurrence('close'))
    for fact in case.broker.execute_close('close', execution_id='closed', quantity=3,
                                         price=100, terminal=True, at=case.advance()):
        case.owner.observe(fact, now=case.now)
    case.owner.check_protection_deadlines(now=case.now+timedelta(minutes=15))
    assert case.owner.authority == 'INTERVENTION'
