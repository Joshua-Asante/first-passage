"""Independent working-order evidence and literal emulator semantics."""
from datetime import datetime, timedelta, timezone
from dataclasses import replace

import pytest

from c1_signal_daemon.book_protocol import Bracket, BracketAmend, OrderIntent, Side
from c1_rail.book_account_owner import BrokerCommand, BrokerResult

NOW = datetime(2026, 9, 16, 14, tzinfo=timezone.utc)


def api():
    from c1_rail import book_protection as p
    from c1_rail.book_synthetic_protection import SyntheticProtectionBroker
    return p, SyntheticProtectionBroker


def command(action, operation='entry', change=None):
    p, _ = api()
    return BrokerCommand('attempt:' + operation, operation, 'leg', action.kind if isinstance(action, OrderIntent) else 'amend',
                         'buy', 2, 'MNQ', 'RUNNING', 1, action,
                         occurrence=p.ActionOccurrence('account', 'epoch', 'session', 'direct', operation, 0),
                         protection_change=change)


def setup_broker(bracket=None):
    p, cls = api()
    broker = cls([BrokerResult('accepted')] * 8, account='account', account_epoch='epoch', at=NOW)
    broker.send(command(OrderIntent('entry', 'leg', 'entry', Side.BUY, 2, bracket=bracket)))
    return p, broker


def read(broker):
    p, _ = api()
    return broker.read_protection(p.ProtectionRead(p.ActionOccurrence('account', 'epoch', 'session', 'direct', 'read', 0), ('leg',), NOW))


def test_clock_and_receipt_cannot_manufacture_working_protection():
    p, broker = setup_broker(Bracket(stop=98.13))
    assert read(broker) is None
    broker.advance(NOW + timedelta(seconds=1))
    assert read(broker).orders == ()
    broker.execute_entry('entry', fill_id='f1', quantity=1, price=100, at=NOW + timedelta(seconds=2))
    state = read(broker)
    assert state.positions == (('f1', 1),)
    assert state.orders[0].effective == Bracket(stop=98)
    assert state.orders[0].quantity == 1
    with pytest.raises(ValueError):
        broker.advance(NOW)


@pytest.mark.parametrize('side, expected', [(Side.BUY, Bracket(stop=98, limit=102.25)), (Side.SELL, Bracket(stop=98.25, limit=102))])
def test_directional_levels_match_emulator(side, expected):
    p, _ = api()
    from c1_signal_daemon.tv_broker_emulator import TVBrokerEmulator
    emulator = TVBrokerEmulator('leg', .25, 2, 0, 0)
    raw = Bracket(stop=98.13, limit=102.13)
    assert p.normalize_bracket(raw, side, .25) == expected == emulator._rounded(raw, long=side is Side.BUY)


def test_fifo_trigger_keeps_live_original_owner_and_consumed_tombstone():
    p, broker = setup_broker(Bracket(stop=98))
    broker.execute_entry('entry', fill_id='old', quantity=1, price=100, at=NOW + timedelta(seconds=1))
    broker.execute_entry('entry', fill_id='new', quantity=1, price=100, at=NOW + timedelta(seconds=2))
    state = read(broker)
    old, new = state.orders
    event = broker.execute_protection(new.owner_id, quantity=1, price=98, terminal=True, at=NOW + timedelta(seconds=3))
    assert event.allocations == (('old', 1),)
    assert event.snapshot.positions == (('new', 1),)
    assert tuple(o.owner_id for o in event.snapshot.orders) == (old.owner_id,)
    target = p.ProtectionTarget(new.owner_id, 'new', 'leg', 'MNQ', Side.BUY, 1, 'attach')
    change = p.ProtectionChange(target, Bracket(stop=99), Bracket(stop=99), ('stop',))
    broker.send(command(BracketAmend('leg', change.desired), 'resurrect', change))
    with pytest.raises(ValueError, match='consumed'):
        broker.apply('resurrect', outcome='applied', at=NOW + timedelta(seconds=4))


def test_rejected_apply_preserves_independent_state_and_outcome():
    p, broker = setup_broker(Bracket(stop=98))
    broker.execute_entry('entry', fill_id='f', quantity=2, price=100, at=NOW + timedelta(seconds=1))
    old = read(broker).orders[0]
    target = p.ProtectionTarget(old.owner_id, 'f', 'leg', 'MNQ', Side.BUY, 2, 'amend')
    change = p.ProtectionChange(target, Bracket(stop=99), Bracket(stop=99), ('stop',))
    broker.send(command(BracketAmend('leg', change.desired), 'amend', change))
    broker.apply('amend', outcome='rejected', at=NOW + timedelta(seconds=2))
    state = read(broker)
    assert state.orders[0] == old
    assert ('amend', 'rejected') in state.resolved_operations


def test_occurrence_and_component_contracts():
    p, _ = api()
    occurrence = p.ActionOccurrence('account', 'epoch', 'session', 'direct', 'event', 0)
    assert p.validate_occurrence(occurrence)
    assert not p.validate_occurrence(replace(occurrence, ordinal=True))
    assert p.occurrence_key(occurrence) != p.occurrence_key(replace(occurrence, ordinal=1))
    old = Bracket(stop=98, trail_activation_ticks=4, trail_offset_ticks=2)
    assert p.changed_components(old, replace(old, stop=99)) == ('stop',)
    assert not p.is_loosening(old, replace(old, stop=99), Side.BUY)
    assert p.is_loosening(old, replace(old, stop=None), Side.BUY)
    assert p.is_loosening(old, replace(old, trail_offset_ticks=3), Side.BUY)


def test_close_requires_market_price_and_preserves_scoped_sibling():
    p, broker = setup_broker(Bracket(stop=98))
    broker.execute_entry('entry', fill_id='old', quantity=1, price=100, at=NOW + timedelta(seconds=1))
    broker.execute_entry('entry', fill_id='new', quantity=1, price=100, at=NOW + timedelta(seconds=2))
    close = OrderIntent('close', 'leg', 'exit', Side.SELL, 1, scope_fill_ids=('new',))
    broker.send(replace(command(close, 'close'), side='sell', quantity=1))
    with pytest.raises(ValueError, match='market price'):
        broker.apply('close', outcome='applied', at=NOW + timedelta(seconds=3))
    assert read(broker).positions == (('old', 1), ('new', 1))
    broker.mark_price('leg', 101, at=NOW + timedelta(seconds=4))
    broker.apply('close', outcome='applied', at=NOW + timedelta(seconds=4))
    fact, = broker.result_facts('close')
    assert (fact.price, fact.entry_execution_id) == (101, 'new')
    assert read(broker).positions == (('old', 1),)
    assert read(broker).orders[0].entry_fill_id == 'old'
    from c1_signal_daemon.tv_broker_emulator import TVBrokerEmulator
    from c1_signal_daemon.book_protocol import FillTiming
    from c1_signal_daemon.feed import Bar
    emulator = TVBrokerEmulator('leg', .25, 2, 0, 0)
    ids = []
    for name in ('old', 'new'):
        event, = emulator.submit([OrderIntent(name, 'leg', 'entry', Side.BUY, 1,
            bracket=Bracket(stop=98), timing=FillTiming.THIS_CLOSE)], Bar(NOW, 100, 100, 100, 100, 1))
        ids.append(event.fill.fill_id)
    close_event, = emulator.submit([replace(close, scope_fill_ids=(ids[1],), timing=FillTiming.THIS_CLOSE)],
                                  Bar(NOW + timedelta(seconds=4), 101, 101, 101, 101, 1))
    assert close_event.fill.price == fact.price
    assert emulator._open[ids[0]].lot_qty == read(broker).positions[0][1]
    assert emulator._open[ids[0]].bracket == read(broker).orders[0].effective
    assert ids[1] not in emulator._open


@pytest.mark.parametrize('side', [Side.BUY, Side.SELL])
def test_producer_emulator_fifo_anchor_and_component_trace(side):
    p, cls = api()
    from c1_signal_daemon.tv_broker_emulator import TVBrokerEmulator
    from c1_signal_daemon.book_protocol import FillTiming
    from c1_signal_daemon.feed import Bar
    broker = cls([BrokerResult('accepted')] * 5, account='account', account_epoch='epoch', at=NOW)
    emulator = TVBrokerEmulator('leg', .25, 2, 0, 0)
    direction = 1 if side is Side.BUY else -1
    bracket = Bracket(stop=90 if direction == 1 else 110, trail_activation_ticks=4, trail_offset_ticks=8)
    ids = []
    for i, name in enumerate(('old', 'new')):
        intent = OrderIntent(name, 'leg', 'entry', side, 1, bracket=bracket, timing=FillTiming.THIS_CLOSE)
        broker.send(replace(command(intent, name), side=side.value, quantity=1))
        at = NOW + timedelta(seconds=i + 1)
        event, = emulator.submit([intent], Bar(at, 100, 100, 100, 100, 1))
        ids.append(event.fill.fill_id)
        broker.execute_entry(name, fill_id=event.fill.fill_id, quantity=1, price=100, at=at)
    at = NOW + timedelta(seconds=3)
    favorable = 100 + direction * 2
    broker.mark_price('leg', favorable, at=at)
    emulator.process_bar(Bar(at, 100, max(100, favorable), min(100, favorable), favorable, 1))
    for observed in read(broker).orders:
        oracle = emulator._open[observed.entry_fill_id]
        assert (observed.trail_active, observed.trail_anchor) == (oracle.trail_active, oracle.trail_extreme) == (True, favorable)
    old = read(broker).orders[0]
    desired = replace(bracket, stop=91 if direction == 1 else 109)
    target = p.ProtectionTarget(old.owner_id, old.entry_fill_id, 'leg', 'MNQ', side, 1, 'amend')
    change = p.ProtectionChange(target, desired, desired, ('stop',))
    broker.send(command(BracketAmend('leg', desired, (ids[0],)), 'change', change))
    broker.apply('change', outcome='applied', at=NOW + timedelta(seconds=4))
    emulator._amend(BracketAmend('leg', desired, (ids[0],)))
    assert read(broker).orders[0].trail_anchor == emulator._open[ids[0]].trail_extreme == favorable
    trigger = read(broker).orders[1]
    executed = broker.execute_protection(trigger.owner_id, quantity=1, price=100, terminal=True, at=NOW + timedelta(seconds=5))
    emulator._fill_exit(emulator._open[ids[1]], 100, NOW + timedelta(seconds=5), slip=False, reason='synthetic')
    assert executed.allocations == ((ids[0], 1),)
    assert executed.snapshot.positions == tuple((fid, o.lot_qty) for fid, o in emulator._open.items() if o.lot_qty)
    live, = executed.snapshot.orders
    oracle = emulator._open[live.entry_fill_id]
    assert (live.quantity, live.effective, live.trail_anchor) == (oracle.bracket_qty, oracle.bracket, oracle.trail_extreme)
    assert oracle.lot_qty == 0


def test_partial_protection_execution_retains_order_until_terminal():
    p, broker = setup_broker(Bracket(stop=98))
    broker.execute_entry('entry', fill_id='f', quantity=2, price=100, at=NOW + timedelta(seconds=1))
    owner = read(broker).orders[0].owner_id
    first = broker.execute_protection(owner, quantity=1, price=98, terminal=False, at=NOW + timedelta(seconds=2))
    assert first.snapshot.orders[0].quantity == 1
    assert first.snapshot.positions == (('f', 1),)
    second = broker.execute_protection(owner, quantity=1, price=98, terminal=True, at=NOW + timedelta(seconds=3))
    assert second.snapshot.orders == second.snapshot.positions == ()


def test_transport_rejection_is_reported_by_later_independent_read():
    p, cls = api()
    broker = cls(account='account', account_epoch='epoch', at=NOW)
    broker.queue(BrokerResult('rejected'))
    broker.send(command(OrderIntent('denied', 'leg', 'entry', Side.BUY, 1), 'denied'))
    broker.advance(NOW + timedelta(seconds=1))
    assert ('denied', 'rejected') in read(broker).resolved_operations
    with pytest.raises(ValueError, match='not executable'):
        broker.execute_entry('denied', fill_id='no', quantity=1, price=100, at=NOW + timedelta(seconds=2))


def test_bare_attachment_matches_emulator_and_receipt_does_not_apply():
    p, broker = setup_broker()
    from c1_signal_daemon.tv_broker_emulator import TVBrokerEmulator
    from c1_signal_daemon.book_protocol import FillTiming
    from c1_signal_daemon.feed import Bar
    emulator = TVBrokerEmulator('leg', .25, 2, 0, 0)
    event, = emulator.submit([OrderIntent('entry', 'leg', 'entry', Side.BUY, 2, timing=FillTiming.THIS_CLOSE)],
                             Bar(NOW, 100, 100, 100, 100, 1))
    fid = event.fill.fill_id
    broker.execute_entry('entry', fill_id=fid, quantity=2, price=100, at=NOW + timedelta(seconds=1))
    target = p.ProtectionTarget('protection:' + fid, fid, 'leg', 'MNQ', Side.BUY, 2, 'attach')
    change = p.ProtectionChange(target, Bracket(stop=98.13), Bracket(stop=98), ('stop',))
    broker.send(command(BracketAmend('leg', change.desired, (fid,)), 'attach', change))
    assert read(broker).orders == ()
    broker.apply('attach', outcome='applied', at=NOW + timedelta(seconds=2))
    emulator._amend(BracketAmend('leg', change.desired, (fid,)))
    observed, = read(broker).orders
    oracle = emulator._open[fid]
    assert (observed.quantity, observed.effective, observed.trail_active, observed.trail_anchor) == (
        oracle.bracket_qty, oracle.bracket, oracle.trail_active, oracle.trail_extreme)


def test_wrong_component_mask_cannot_partially_mutate_working_state():
    p, broker = setup_broker(Bracket(stop=98, limit=104))
    broker.execute_entry('entry', fill_id='f', quantity=2, price=100, at=NOW + timedelta(seconds=1))
    old = read(broker).orders[0]
    target = p.ProtectionTarget(old.owner_id, 'f', 'leg', 'MNQ', Side.BUY, 2, 'amend')
    change = p.ProtectionChange(target, Bracket(stop=99, limit=105), Bracket(stop=99, limit=105), ('stop',))
    broker.send(command(BracketAmend('leg', change.desired), 'bad', change))
    with pytest.raises(ValueError, match='component'):
        broker.apply('bad', outcome='applied', at=NOW + timedelta(seconds=2))
    assert read(broker).orders == (old,)
    assert ('bad', 'applied') not in read(broker).resolved_operations
