"""A delayed scoped reduction must precede the same owner's protective fill."""
from dataclasses import replace

import pytest

from book_protection_fixtures import ProtectionScenario
from c1_rail.book_account_owner import BrokerResult
from c1_signal_daemon.book_protocol import Bracket
from test_book_close_reconciliation import close


def pending_close(case):
    case.enter(bracket=Bracket(stop=98))
    case.broker.queue(BrokerResult('accepted'))
    case.dispatch(close('ordinary', quantity=1), case.occurrence('ordinary'))
    for fact in case.broker.execute_close('ordinary', execution_id='ordinary-fill',
                                         quantity=1, price=100, terminal=True, at=case.advance()):
        assert case.owner.observe(fact, now=case.now) == ()
    assert case.protection('base').quantity == 3
    assert case.owner.exposure('dj30_mym_p250') == (2, 0)


@pytest.mark.parametrize('terminal,quantity', [(False, 1), (True, 2)])
def test_same_owner_protective_fill_reconciles_prior_unobserved_close(tmp_path, terminal, quantity):
    case = ProtectionScenario(tmp_path)
    pending_close(case)
    event = case.broker.execute_protection('protection:base', quantity=quantity,
                                          price=98, terminal=terminal, at=case.advance())
    feedback = case.owner.observe_protection_execution(event, now=case.now)
    assert [item.fill.qty for item in feedback] == [1, quantity]
    assert feedback[0].fill.order_id == 'ordinary'
    assert case.owner.authority == 'NORMAL'
    assert case.owner.exposure('dj30_mym_p250') == (2 - quantity, 0)
    assert case.protection('base').quantity == 2 - quantity
    assert case.protection('base').consumed == terminal
    case.observe()
    assert case.owner.authority == 'NORMAL'


def test_overstated_protective_execution_cannot_use_preclose_quantity(tmp_path):
    case = ProtectionScenario(tmp_path)
    pending_close(case)
    event = case.broker.execute_protection('protection:base', quantity=2,
                                          price=98, terminal=True, at=case.advance())
    event = replace(event, quantity=3, allocations=(('base', 3),))
    before = case.owner.all_feedback
    assert case.owner.observe_protection_execution(event, now=case.now) == ()
    assert case.owner.authority == 'INTERVENTION'
    assert case.owner.exposure('dj30_mym_p250') == (2, 0)
    assert case.owner.all_feedback == before


def test_scoped_close_after_fifo_reconciles_exhausted_origin_sibling(tmp_path):
    from test_book_protection_allocations import close_new
    case = ProtectionScenario(tmp_path)
    case.enter(('old', 'new'), quantities=(1, 2), bracket=Bracket(stop=98))
    event = case.broker.execute_protection('protection:new', quantity=1,
                                          price=98, terminal=False, at=case.advance())
    assert event.allocations == (('old', 1),)
    assert case.owner.observe_protection_execution(event, now=case.now)
    assert case.protection('old').quantity == 1
    assert case.protection('new').quantity == 1
    assert case.owner.exposure('dj30_mym_p250') == (2, 0)
    snapshot = close_new(case, 1)
    assert {row.entry_fill_id: row.quantity for row in snapshot.orders} == {'new': 1}
    assert case.owner.observe_protection(snapshot, now=case.now)
    assert case.owner.authority == 'NORMAL'
    assert case.protection('old').consumed
    assert case.protection('new').quantity == 1
    assert case.owner.exposure('dj30_mym_p250') == (1, 0)


@pytest.mark.parametrize('scope', [('new',), ('old',)])
def test_scoped_close_refuses_unsupported_coverage_but_full_flat_remains_valid(tmp_path, monkeypatch, scope):
    import sqlite3
    import test_book_account_owner
    bound = test_book_account_owner.binding()
    bound['risk_dollars']['dj30_mym_p250'] = 128
    monkeypatch.setattr(test_book_account_owner, 'binding', lambda: bound)
    case = ProtectionScenario(tmp_path)
    case.enter(('old', 'new'), quantities=(2, 2), bracket=Bracket(stop=98))
    event = case.broker.execute_protection('protection:new', quantity=1,
                                          price=98, terminal=False, at=case.advance())
    assert event.allocations == (('old', 1),)
    assert case.owner.observe_protection_execution(event, now=case.now)
    assert case.owner.exposure('dj30_mym_p250') == (3, 0)
    commands = len(case.broker.commands)
    rejected = case.dispatch(close('unsafe', quantity=1, scope=scope), case.occurrence('unsafe'))
    assert rejected.refusal_reason == 'close_capability_problem'
    assert len(case.broker.commands) == commands
    assert case.owner.exposure('dj30_mym_p250') == (3, 0)
    with sqlite3.connect(case.owner.path) as db:
        assert db.execute('SELECT count(*) FROM close_reservations').fetchone()[0] == 0
        assert db.execute("SELECT count(*) FROM operations WHERE operation_id='unsafe'").fetchone()[0] == 0
    case.broker.queue(BrokerResult('accepted'))
    admitted = case.dispatch(replace(close('full'), kind='flat'), case.occurrence('full'))
    assert admitted.transport_state == 'accepted' and admitted.quantity == 3
    for fact in case.broker.execute_close('full', execution_id='full-fill', quantity=3,
                                         price=100, terminal=True, at=case.advance()):
        case.owner.observe(fact, now=case.now)
    case.observe()
    assert case.owner.authority == 'NORMAL'
    assert case.owner.exposure('dj30_mym_p250') == (0, 0)
    assert case.protection('old').consumed and case.protection('new').consumed
