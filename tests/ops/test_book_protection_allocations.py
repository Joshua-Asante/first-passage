"""Scoped market reductions and protective FIFO have distinct owner lifecycles."""
from dataclasses import replace
from datetime import timedelta

import pytest

from book_protection_fixtures import ProtectionScenario
from c1_rail.book_account_owner import BrokerResult
from c1_rail.book_protection import ProtectionRead
from c1_signal_daemon.book_protocol import Bracket, OrderIntent, Side

LEG = 'dj30_mym_p250'


def close_new(s, quantity):
    action = OrderIntent('close-new', LEG, 'exit', Side.SELL, quantity,
                         scope_fill_ids=('new',), bar_time=s.now)
    s.broker.queue(BrokerResult('accepted'))
    result = s.dispatch(action, s.occurrence('close-new'))
    assert result.transport_state == 'accepted'
    facts = s.broker.execute_close(result.operation_id, execution_id='close-fill',
                                  quantity=quantity, price=101, terminal=True, at=s.advance())
    for fact in facts:
        s.owner.observe(fact, now=s.now)
    s.advance()
    return s.broker.read_protection(ProtectionRead(s.occurrence('read'), (LEG,),
                                                  s.now - timedelta(milliseconds=1)))


@pytest.mark.parametrize('quantity', [1, 2])
def test_scoped_close_adjusts_only_target_owner(tmp_path, quantity):
    s = ProtectionScenario(tmp_path)
    s.enter(('old', 'new'), quantities=(1, 2), bracket=Bracket(stop=98))
    snapshot = close_new(s, quantity)
    assert {r.entry_fill_id: r.quantity for r in snapshot.orders} == (
        {'old': 1, 'new': 1} if quantity == 1 else {'old': 1})
    s.owner.observe_protection(snapshot, now=s.now)
    assert s.owner.authority == 'NORMAL'
    assert s.protection('old').quantity == 1
    assert s.protection('new').quantity == 2 - quantity
    assert s.protection('new').consumed == (quantity == 2)
    s.observe()
    assert s.owner.authority == 'NORMAL'


def test_valid_partial_scoped_snapshot_is_accepted_independent_of_producer(tmp_path):
    s = ProtectionScenario(tmp_path)
    s.enter(('old', 'new'), quantities=(1, 2), bracket=Bracket(stop=98))
    snapshot = close_new(s, 1)
    snapshot = replace(snapshot, orders=tuple(replace(r, quantity=1) for r in snapshot.orders))
    s.owner.observe_protection(snapshot, now=s.now)
    assert s.owner.authority == 'NORMAL'
    assert s.protection('new').quantity == 1


@pytest.mark.parametrize('fault', ['oversize', 'orphan', 'sibling_removed'])
def test_scoped_snapshot_rejects_invalid_owner_coverage(tmp_path, fault):
    s = ProtectionScenario(tmp_path)
    s.enter(('old', 'new'), quantities=(1, 2), bracket=Bracket(stop=98))
    snapshot = close_new(s, 1)
    rows = tuple(replace(r, quantity=1) for r in snapshot.orders)
    if fault == 'oversize':
        rows = tuple(replace(r, quantity=2) if r.entry_fill_id == 'new' else r for r in rows)
    elif fault == 'orphan':
        rows = tuple(replace(r, owner_id='protection:foreign', entry_fill_id='foreign')
                     if r.entry_fill_id == 'new' else r for r in rows)
    else:
        rows = tuple(r for r in rows if r.entry_fill_id == 'new')
    s.owner.observe_protection(replace(snapshot, orders=rows), now=s.now)
    assert s.owner.authority == 'INTERVENTION'
    assert s.protection('old').quantity == 1
    assert s.protection('new').quantity == 2


@pytest.mark.parametrize('terminal, quantity, remaining', [(False, 1, 1), (True, 2, 0)])
def test_protective_fifo_keeps_exhausted_origin_sibling(tmp_path, terminal, quantity, remaining):
    s = ProtectionScenario(tmp_path)
    s.enter(('old', 'new'), quantities=(1, 2), bracket=Bracket(stop=98))
    event = s.broker.execute_protection('protection:new', quantity=quantity, price=98,
                                        terminal=terminal, at=s.advance())
    feedback = s.owner.observe_protection_execution(event, now=s.now)
    assert feedback
    assert s.owner.authority == 'NORMAL'
    assert s.protection('old').quantity == 1
    assert not s.protection('old').consumed
    assert s.protection('new').quantity == remaining
    s.observe()
    assert s.owner.authority == 'NORMAL'

@pytest.mark.parametrize('remove_survivor', [False, True])
def test_historical_scoped_close_does_not_consume_fifo_survivor(tmp_path, remove_survivor):
    s = ProtectionScenario(tmp_path)
    s.enter(('new', 'old'), quantities=(2, 1), bracket=Bracket(stop=98))
    snapshot = close_new(s, 1)
    s.owner.observe_protection(snapshot, now=s.now)
    assert s.owner.authority == 'NORMAL'
    event = s.broker.execute_protection('protection:old', quantity=1, price=98,
                                        terminal=True, at=s.advance())
    assert event.allocations == (('new', 1),)
    if remove_survivor:
        event = replace(event, snapshot=replace(event.snapshot, orders=()))
    feedback = s.owner.observe_protection_execution(event, now=s.now)
    if remove_survivor:
        assert feedback == ()
        assert s.owner.authority == 'INTERVENTION'
        assert s.owner.exposure(LEG) == (2, 0)
    else:
        assert feedback
        assert s.owner.authority == 'NORMAL'
        assert s.owner.exposure(LEG) == (1, 0)
        s.observe()
        assert s.owner.authority == 'NORMAL'
    assert s.protection('new').quantity == 1
    assert not s.protection('new').consumed

@pytest.mark.parametrize('legacy_cursor', [False, True])
def test_restart_reconciles_scoped_close_with_retained_or_legacy_evidence(tmp_path, legacy_cursor):
    import json
    import sqlite3
    from c1_rail.book_account_owner import BookAccountOwner
    from test_book_account_owner import binding

    s = ProtectionScenario(tmp_path)
    s.enter(('old', 'new'), quantities=(1, 2), bracket=Bracket(stop=98))
    snapshot = close_new(s, 1)
    if legacy_cursor:
        # Model a pre-cursor journal without changing authority or broker facts.
        with sqlite3.connect(s.owner.path) as db:
            rows = db.execute('SELECT owner_id,body FROM protection_owners').fetchall()
            for identity, body in rows:
                row = json.loads(body)
                row.pop('close_evidence_sequence', None)
                db.execute('UPDATE protection_owners SET body=? WHERE owner_id=?',
                           (json.dumps(row), identity))
    s.owner = BookAccountOwner.boot(s.owner.path, s.owner.account,
                                    binding=binding(), synthetic_broker=s.broker)
    before = s.owner.incidents
    s.owner.observe_protection(snapshot, now=s.now)
    assert s.protection('new').quantity == 1
    assert s.protection('old').quantity == 1
    assert s.owner.incidents == before
    s.observe()
    assert s.owner.incidents == before


def test_fifo_execution_can_reconcile_preceding_unobserved_scoped_close(tmp_path):
    s = ProtectionScenario(tmp_path)
    s.enter(('new', 'old'), quantities=(2, 1), bracket=Bracket(stop=98))
    close_new(s, 1)  # Broker/ledger reduced, but its protection snapshot is delayed.
    event = s.broker.execute_protection('protection:old', quantity=1, price=98,
                                        terminal=True, at=s.advance())
    assert event.allocations == (('new', 1),)
    feedback = s.owner.observe_protection_execution(event, now=s.now)
    assert feedback
    assert s.owner.authority == 'NORMAL'
    assert s.owner.exposure(LEG) == (1, 0)
    assert s.protection('new').quantity == 1
    assert not s.protection('new').consumed
