"""Delayed observations cannot reuse already-consumed residual evidence."""
from dataclasses import replace
from datetime import timedelta

import pytest

from c1_rail.book_account_owner import BrokerFact, BrokerResult
from c1_signal_daemon.book_protocol import Bracket, Mode
from book_protection_fixtures import ProtectionScenario
from test_book_close_reconciliation import close, status
from test_book_account_owner import NOW, intent, owner


def test_duplicate_snapshot_cannot_reconcile_a_later_arriving_close_fact(tmp_path):
    case = ProtectionScenario(tmp_path)
    case.enter(bracket=Bracket(stop=98))
    case.broker.queue(BrokerResult('accepted'))
    case.dispatch(close('close', quantity=1), case.occurrence('close'))
    fill_time = case.now + timedelta(milliseconds=50)
    before_fill = case.observe()
    assert before_fill.positions == (('base', 3),)
    facts = case.broker.execute_close('close', execution_id='delayed', quantity=1,
                                     price=100, terminal=True, at=case.advance())
    for fact in facts:
        assert case.owner.observe(replace(fact, as_of=fill_time), now=case.now) == ()
    assert case.owner.exposure('dj30_mym_p250') == (2, 0)
    assert status(case.owner, 'close') == 'awaiting_protection'
    feedback = case.owner.all_feedback

    assert case.owner.observe_protection(before_fill, now=case.now) == ()
    assert case.owner.all_feedback == feedback
    assert status(case.owner, 'close') == 'awaiting_protection'

    # A new complete read reflects the reduction and can release the fill.
    case.observe()
    assert status(case.owner, 'close') == 'terminal'
    assert case.protection('base').quantity == 2
    assert len(case.owner.all_feedback) == len(feedback) + 1


def test_new_close_cannot_jump_an_older_queued_demand(tmp_path):
    account, broker = owner(tmp_path, [BrokerResult('accepted'), BrokerResult('accepted')])
    account.dispatch(intent(), occurrence=account.make_occurrence('direct', 'entry'), now=NOW)
    account.observe(BrokerFact.fill('base-fill', 'base', 'dj30_mym_p250', 'entry', 3, 100, NOW), now=NOW)
    account.dispatch(close('first', quantity=1), occurrence=account.make_occurrence('direct', 'first'), now=NOW)
    second = account.dispatch(close('second', quantity=1),
                              occurrence=account.make_occurrence('direct', 'second'), now=NOW)
    assert second.refusal_reason == 'close_pending'
    at = NOW + timedelta(seconds=1)
    account.observe(BrokerFact.terminal('first', 'cancelled', 0, at), now=at)
    third = account.dispatch(close('third', quantity=1),
                             occurrence=account.make_occurrence('direct', 'third'), now=at)
    assert third.refusal_reason == 'close_pending'
    assert len(broker.commands) == 2
    broker.queue(BrokerResult('accepted'))
    resumed = account.resume_closes(now=at)
    assert resumed[0].operation_id == 'second'
    assert resumed[0].transport_state == 'accepted'
    assert resumed[1].refusal_reason == 'close_pending'
    assert broker.commands[-1].operation_id == 'second'


def test_partial_close_cancel_feedback_follows_fill_after_residual_read(tmp_path):
    case = ProtectionScenario(tmp_path)
    case.enter(bracket=Bracket(stop=98))
    case.broker.queue(BrokerResult('accepted'))
    case.dispatch(close('close'), case.occurrence('close'))
    before = case.owner.all_feedback
    facts = case.broker.execute_close('close', execution_id='partial', quantity=1,
                                     price=100, terminal=True, at=case.advance())
    for fact in facts:
        assert case.owner.observe(fact, now=case.now) == ()
    assert case.owner.all_feedback == before
    assert status(case.owner, 'close') == 'awaiting_protection'
    case.observe()
    released = case.owner.all_feedback[len(before):]
    assert [row['body']['event'] for row in released] == ['fill', 'cancel']
    assert status(case.owner, 'close') == 'terminal'
    assert case.owner.exposure('dj30_mym_p250') == (2, 0)


def test_protective_execution_releases_earlier_close_before_protective_feedback(tmp_path):
    from c1_signal_daemon.book_runtime import FourLegRuntime
    from test_four_leg_runtime import inert_adapters
    case = ProtectionScenario(tmp_path)
    case.enter(bracket=Bracket(stop=98))
    runtime = FourLegRuntime(case.owner, inert_adapters())
    for adapter in runtime.adapters.values():
        adapter.set_mode(Mode.NORMAL)
    case.broker.queue(BrokerResult('accepted'))
    case.dispatch(close('close', quantity=1), case.occurrence('close'))
    facts = case.broker.execute_close('close', execution_id='ordinary', quantity=1,
                                     price=100, terminal=True, at=case.advance())
    for fact in facts:
        assert runtime.observe_fact(fact, now=case.now) == ()
    event = case.broker.execute_protection('protection:base', quantity=2,
                                          price=98, terminal=True, at=case.advance())
    events = runtime.observe_protection_execution(event, now=case.now)
    assert len(events) == 2
    assert events[0].fill.order_id == 'close'
    assert events[1].fill.order_id != 'close'
    assert [item.fill.qty for item in events] == [1, 2]
    assert [item[2] for item in runtime.adapters['dj30_mym_p250'].events] == [
        item.fill.fill_id for item in events]
    assert status(case.owner, 'close') == 'terminal'
    assert case.owner.exposure('dj30_mym_p250') == (0, 0)
    delivered = [row for row in case.owner.all_feedback if row['body']['order_id'] == 'close'
                 or row['body'].get('fill', {}).get('price') == 98]
    assert len(delivered) == 2 and all(row['delivered'] for row in delivered)


def test_unresolved_attachment_queues_close_until_confirmation(tmp_path):
    case = ProtectionScenario(tmp_path)
    case.broker.queue(BrokerResult('accepted'))
    case.dispatch(replace(intent(), bracket=Bracket(stop=98)), case.occurrence('entry'))
    fill = case.broker.execute_entry('base', fill_id='base', quantity=3,
                                    price=100, at=case.advance())
    case.owner.observe(fill, now=case.now)
    pending = case.dispatch(close('close'), case.occurrence('close'))
    assert pending.refusal_reason == 'close_pending'
    assert len(case.broker.commands) == 1
    assert case.protection('base').pending_operation is not None
    case.observe()
    assert case.protection('base').pending_operation is None
    case.broker.queue(BrokerResult('accepted'))
    resumed = case.owner.resume_closes(now=case.now)
    assert len(resumed) == 1 and resumed[0].transport_state == 'accepted'
    assert resumed[0].quantity == 3
    assert len(case.broker.commands) == 2


def test_queued_close_that_becomes_empty_retains_one_local_rejection(tmp_path):
    account, broker = owner(tmp_path, [BrokerResult('accepted'), BrokerResult('accepted')])
    account.dispatch(intent(), occurrence=account.make_occurrence('direct', 'entry'), now=NOW)
    account.observe(BrokerFact.fill('base-fill', 'base', 'dj30_mym_p250', 'entry', 3, 100, NOW), now=NOW)
    account.dispatch(close('first'), occurrence=account.make_occurrence('direct', 'first'), now=NOW)
    queued = account.make_occurrence('direct', 'queued')
    assert account.dispatch(close('queued'), occurrence=queued, now=NOW).refusal_reason == 'close_pending'
    at = NOW + timedelta(seconds=1)
    account.observe(BrokerFact.fill('closed', 'first', 'dj30_mym_p250', 'exit', 3, 100, at,
                                   entry_execution_id='base-fill'), now=at)
    before = account.all_feedback
    resumed = account.resume_closes(now=at)
    assert len(resumed) == 1 and resumed[0].refusal_reason == 'zero_exposure'
    assert len(resumed[0].confirmed_events) == 1
    assert resumed[0].confirmed_events[0].event == 'reject'
    assert account.occurrence_state(queued)['state'] == 'complete'
    assert len(account.all_feedback) == len(before) + 1
    assert account.resume_closes(now=at) == ()
    assert len(account.all_feedback) == len(before) + 1
    assert len(broker.commands) == 2


@pytest.mark.parametrize('producer', ['runtime', 'direct'])
def test_cutoff_retires_queued_close_without_touching_inflight_close(tmp_path, producer):
    account, broker = owner(tmp_path, [BrokerResult('accepted'), BrokerResult('accepted')])
    account.dispatch(intent(), occurrence=account.make_occurrence('direct', 'entry'), now=NOW)
    account.observe(BrokerFact.fill('base-fill', 'base', 'dj30_mym_p250', 'entry', 3, 100, NOW), now=NOW)
    account.observe(BrokerFact.terminal('base', 'filled', 3, NOW), now=NOW)
    account.dispatch(close('first'), occurrence=account.make_occurrence('direct', 'first'), now=NOW)
    queued = account.make_occurrence(producer, NOW.isoformat(), 0)
    assert account.dispatch(close('queued'), occurrence=queued, now=NOW).refusal_reason == 'close_pending'
    first_status = status(account, 'first')
    before = account.all_feedback
    cutoff = account.binding['session'].risk_add_cutoff
    results = account.advance_schedule(now=cutoff)
    assert any(row.operation_id == 'queued' and row.refusal_reason == 'scheduled_operation_required'
               for row in results)
    assert account.occurrence_state(queued)['state'] == 'complete'
    assert status(account, 'first') == first_status
    assert len(broker.commands) == 2
    added = account.all_feedback[len(before):]
    assert len(added) == 1
    assert added[0]['body']['event'] == 'reject'
    assert added[0]['body']['order_id'] == 'queued'
    assert added[0]['body']['detail'] == 'scheduled_operation_required'
    assert account.advance_schedule(now=cutoff) == ()
    assert account.resume_closes(now=cutoff) == ()
    assert len(account.all_feedback) == len(before) + 1


def test_protective_execution_drains_queued_close_to_checkpointed_rejection(tmp_path):
    from c1_signal_daemon.book_runtime import FourLegRuntime
    from test_four_leg_runtime import inert_adapters
    case = ProtectionScenario(tmp_path)
    case.enter(bracket=Bracket(stop=98))
    runtime = FourLegRuntime(case.owner, inert_adapters())
    for adapter in runtime.adapters.values():
        adapter.set_mode(Mode.NORMAL)
    case.broker.queue(BrokerResult('accepted'))
    case.dispatch(close('first', quantity=1), case.occurrence('first'))
    for fact in case.broker.execute_close('first', execution_id='ordinary', quantity=1,
                                         price=100, terminal=True, at=case.advance()):
        assert runtime.observe_fact(fact, now=case.now) == ()
    queued = case.occurrence('queued')
    assert case.dispatch(close('queued'), queued).refusal_reason == 'close_pending'
    commands = len(case.broker.commands)
    event = case.broker.execute_protection('protection:base', quantity=2, price=98,
                                          terminal=True, at=case.advance())
    events = runtime.observe_protection_execution(event, now=case.now)
    assert [item.fill.qty for item in events] == [1, 2]
    assert status(case.owner, 'first') == 'terminal'
    assert case.owner.occurrence_state(queued)['state'] == 'complete'
    rejection = [row for row in case.owner.all_feedback
                 if row['body']['order_id'] == 'queued']
    assert len(rejection) == 1
    assert rejection[0]['body']['event'] == 'reject'
    assert rejection[0]['body']['detail'] == 'zero_exposure'
    assert rejection[0]['delivered'] and rejection[0]['checkpoint'] is not None
    assert runtime.adapters['dj30_mym_p250'].events[-1] == ('reject', 'queued', None)
    assert len(case.broker.commands) == commands
    assert runtime.observe_protection_execution(event, now=case.now) == ()
    assert len([row for row in case.owner.all_feedback
                if row['body']['order_id'] == 'queued']) == 1
