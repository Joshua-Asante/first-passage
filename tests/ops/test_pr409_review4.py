"""Regression cases from the post-Slice-D PR409 review."""
from dataclasses import replace
from datetime import timedelta

import pytest

from c1_rail.book_account_owner import BookAccountOwner, BrokerFact, BrokerResult
from c1_rail.book_protection import ProtectionRead
from c1_signal_daemon.book_protocol import Bracket, Side
from book_bootstrap_fixtures import BootstrapBroker, activate_fresh
from book_protection_fixtures import ProtectionScenario
from test_book_account_owner import NOW, SESSION, binding, intent, owner


def test_overlapping_protection_owners_cannot_each_cover_same_remaining_contract(tmp_path):
    case = ProtectionScenario(tmp_path)
    case.enter(('first', 'second'), quantities=(1, 2), bracket=Bracket(stop=98))
    snapshot = case.observe()
    close = replace(intent('reduce'), kind='exit', side=Side.SELL, qty=2)
    case.broker.queue(BrokerResult('accepted'))
    result = case.dispatch(close, case.occurrence('reduce'))
    assert result.quantity == 2
    for fill_id in ('first', 'second'):
        case.owner.observe(BrokerFact.fill('reduction-' + fill_id, 'reduce', close.leg_id, 'exit', 1, 99,
                                          case.now, entry_execution_id=fill_id), now=case.now)
    assert case.owner.authority == 'NORMAL', case.owner.incidents
    at = case.advance()
    corrupt = replace(snapshot, fact_id='overlapping', sequence=snapshot.sequence+1, as_of=at,
                      positions=(('second', 1),),
                      orders=tuple(replace(row, quantity=1) for row in snapshot.orders))
    case.owner.observe_protection(corrupt, now=at)
    assert case.owner.authority == 'INTERVENTION'


@pytest.mark.parametrize('first_phase', [SESSION.risk_add_cutoff, SESSION.flatten_start])
def test_scheduled_flat_waits_for_terminal_and_reconciled_late_fills(tmp_path, first_phase):
    account, broker = owner(tmp_path, [BrokerResult('accepted'), BrokerResult('accepted')])
    account.dispatch(intent(), occurrence=account.make_occurrence('direct', 'entry'), now=NOW)
    account.observe(BrokerFact.fill('early', 'base', 'dj30_mym_p250', 'entry', 1, 100, NOW), now=NOW)
    account.advance_schedule(now=first_phase)
    account.advance_schedule(now=SESSION.flatten_start)
    assert [c.kind for c in broker.commands] == ['entry', 'cancel']
    at = SESSION.flatten_start + timedelta(seconds=1)
    account.observe(BrokerFact.fill('late', 'base', 'dj30_mym_p250', 'entry', 1, 100, at), now=at)
    account.observe(BrokerFact.terminal('base', 'cancelled', 2, at), now=at)
    broker.queue(BrokerResult('accepted'))
    result = account.advance_schedule(now=at)
    assert len(result) == 1 and result[0].quantity == 2
    assert broker.commands[-1].kind == 'flat'


@pytest.mark.parametrize('outcome,elapsed', [('unknown', 1), ('accepted', 901)])
def test_unresolved_ordinary_order_blocks_other_leg_until_postdating_terminal(tmp_path, outcome, elapsed):
    bound = binding()
    bound.update(valid_until=NOW+timedelta(hours=2), max_evidence_age=timedelta(hours=2))
    broker = BootstrapBroker([BrokerResult(outcome), BrokerResult('accepted')])
    account = BookAccountOwner.boot(tmp_path/'owner.sqlite', 'synthetic-account', binding=bound, synthetic_broker=broker)
    activate_fresh(account)
    account.dispatch(intent(), occurrence=account.make_occurrence('direct', 'base'), now=NOW)
    at = NOW + timedelta(seconds=elapsed)
    other = replace(intent('other'), leg_id='orb_mnq_v7', qty=1, bar_time=at)
    refusal = account.dispatch(other, occurrence=account.make_occurrence('direct', 'blocked'), now=at)
    assert refusal.refusal_reason == 'unknown_order'
    assert len(broker.commands) == 1 and account.exposure('dj30_mym_p250') == (0, 3)
    account.observe(BrokerFact.terminal('base', 'cancelled', 0, at), now=at)
    result = account.dispatch(replace(other, order_id='after'), occurrence=account.make_occurrence('direct', 'after'), now=at)
    assert result.transport_state == 'accepted'


def test_accepted_timeout_fence_clears_only_after_every_owner_resolves(tmp_path):
    bound = binding()
    bound.update(valid_until=NOW+timedelta(hours=2), max_evidence_age=timedelta(hours=2))
    broker = BootstrapBroker([BrokerResult('accepted')]*3)
    account = BookAccountOwner.boot(tmp_path/'owner.sqlite', 'synthetic-account', binding=bound, synthetic_broker=broker)
    activate_fresh(account)
    for index, leg in enumerate(('dj30_mym_p250', 'orb_mnq_v7')):
        action = replace(intent('pending-'+str(index)), leg_id=leg, qty=1 if index else 5)
        account.dispatch(action, occurrence=account.make_occurrence('direct', action.order_id), now=NOW)
    at = NOW+timedelta(minutes=15)
    def try_risk(identity):
        action = replace(intent(identity), bar_time=at)
        return account.dispatch(action, occurrence=account.make_occurrence('direct', identity), now=at)
    assert try_risk('blocked-both').refusal_reason == 'unknown_order'
    account.observe(BrokerFact.terminal('pending-0', 'cancelled', 0, at), now=at)
    assert try_risk('blocked-one').refusal_reason == 'unknown_order'
    account.observe(BrokerFact.terminal('pending-1', 'cancelled', 0, at), now=at)
    cleared = try_risk('clear')
    assert cleared.transport_state == 'accepted', cleared


def test_unknown_order_equal_time_terminal_does_not_clear_and_restart_retains_attempt(tmp_path):
    account, broker = owner(tmp_path, [BrokerResult('unknown')])
    account.dispatch(intent(), occurrence=account.make_occurrence('direct', 'entry'), now=NOW)
    account.observe(BrokerFact.terminal('base', 'cancelled', 0, NOW), now=NOW)
    refusal = account.dispatch(replace(intent('other'), leg_id='orb_mnq_v7', qty=1),
        occurrence=account.make_occurrence('direct', 'other'), now=NOW+timedelta(seconds=1))
    assert refusal.refusal_reason == 'unknown_order'
    restarted = BookAccountOwner.boot(account.path, account.account, binding=account.binding, synthetic_broker=broker)
    assert restarted.permission == 'HALTED'
    result = restarted.dispatch(intent('restart'), occurrence=restarted.make_occurrence('direct', 'restart'), now=NOW)
    assert result.transport_state == 'not_attempted' and len(broker.commands) == 1


def test_pending_scheduled_cancellation_past_deadline_never_sends_flat(tmp_path):
    account, broker = owner(tmp_path, [BrokerResult('accepted'), BrokerResult('unknown')])
    account.dispatch(intent(), occurrence=account.make_occurrence('direct', 'entry'), now=NOW)
    account.observe(BrokerFact.fill('early', 'base', 'dj30_mym_p250', 'entry', 1, 100, NOW), now=NOW)
    account.advance_schedule(now=SESSION.flatten_start)
    account.advance_schedule(now=SESSION.own_flat_deadline)
    assert [c.kind for c in broker.commands] == ['entry', 'cancel']
    assert account.authority == 'INTERVENTION' and account.exposure('dj30_mym_p250') == (1, 2)

@pytest.mark.parametrize('offset', [-1, 0])
def test_aged_accepted_order_cannot_resolve_with_nonpostdating_terminal(tmp_path, offset):
    bound = binding()
    bound.update(valid_until=NOW+timedelta(hours=2), max_evidence_age=timedelta(hours=2))
    broker = BootstrapBroker([BrokerResult('accepted')]*2)
    account = BookAccountOwner.boot(tmp_path/'owner.sqlite', 'synthetic-account', binding=bound, synthetic_broker=broker)
    activate_fresh(account)
    account.dispatch(intent(), occurrence=account.make_occurrence('direct', 'base'), now=NOW)
    account.observe(BrokerFact.terminal('base', 'cancelled', 0, NOW+timedelta(seconds=offset)), now=NOW)
    at = NOW+timedelta(minutes=15)
    result = account.dispatch(replace(intent('after'), leg_id='orb_mnq_v7', qty=1, bar_time=at),
        occurrence=account.make_occurrence('direct', 'after'), now=at)
    assert result.refusal_reason == 'unknown_order'
    assert len(broker.commands) == 1
