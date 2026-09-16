"""Offline broker with independent positions, orders and explicit synthetic time."""
from dataclasses import dataclass, replace
from datetime import datetime
import math

from c1_signal_daemon.book_protocol import Bracket, OrderIntent, Side
from c1_signal_daemon.book_adapters import ADAPTER_BY_LEG
from c1_rail.book_account_owner import BrokerCommand, BrokerFact, BrokerResult, SyntheticBroker
from c1_rail.book_protection import (
    ObservedProtection, ProtectionExecution, ProtectionRead, ProtectionSnapshot,
    changed_components, has_components, normalize_bracket,
)
from c1_rail.book_takeover import (
    AccountInventory, InventoryPosition, InventoryRead, RequestOutcome, WorkingOrder,
)


@dataclass
class _Lot:
    fill_id: str
    leg_id: str
    symbol: str
    side: Side
    remaining: int
    price: float
    consumed: bool = False


class SyntheticProtectionBroker(SyntheticBroker):
    """Receipt never applies a command. Only explicit synthetic stimuli mutate state."""

    def __init__(self, results=(), *, account, account_epoch, mintick=.25,
                 stream_id='synthetic-protection', at=None):
        super().__init__(results)
        self.account, self.account_epoch = account, account_epoch
        self.stream_id, self.mintick = stream_id, mintick
        self._clock = None
        self._sequence = 0
        self._pending = {}
        self._outcomes = {}
        self._lots = {}
        self._orders = {}
        self._filled = {}
        self._facts = {}
        self._prices = {}
        self._working = {}
        self._entry_operations = {}
        self._terminals = {}
        self._inventory_sequence = 0
        self._history = {}
        self._close_execution_ids = set()
        self.drop_reads = False
        if at is not None:
            self.advance(at)

    @property
    def now(self):
        return self._clock

    def advance(self, at: datetime):
        if not isinstance(at, datetime) or at.tzinfo is None or at.utcoffset() is None:
            raise ValueError('aware synthetic time required')
        if self._clock is not None and at < self._clock:
            raise ValueError('synthetic clock cannot move backward')
        self._clock = at

    def _tick(self, leg):
        adapter = ADAPTER_BY_LEG.get(leg)
        if adapter is not None:
            return adapter.mintick
        return self.mintick[leg] if isinstance(self.mintick, dict) else self.mintick

    def send(self, command: BrokerCommand) -> BrokerResult:
        if command.operation_id in self._pending:
            raise ValueError('duplicate operation send')
        occurrence = command.occurrence
        if occurrence is not None and (occurrence.account != self.account or
                                        occurrence.account_epoch != self.account_epoch):
            raise ValueError('foreign occurrence')
        result = super().send(command)
        self._pending[command.operation_id] = command
        if result.state == 'rejected':
            self._outcomes[command.operation_id] = 'rejected'
            if command.kind in ('entry', 'add', 'exit', 'flat'):
                self._terminal(command.operation_id, 'rejected', self._clock)
        return result

    def apply(self, operation_id: str, *, outcome: str, at: datetime):
        if outcome not in ('applied', 'rejected'):
            raise ValueError('invalid application outcome')
        command = self._pending[operation_id]
        if operation_id in self._outcomes:
            if self._outcomes[operation_id] != outcome:
                raise ValueError('conflicting application outcome')
            self.advance(at)
            return
        self.advance(at)
        if outcome == 'rejected':
            self._outcomes[operation_id] = outcome
            if command.kind in ('entry', 'add', 'exit', 'flat'):
                self._working.pop(operation_id, None)
                self._terminal(operation_id, 'rejected', at)
            return
        change = command.protection_change
        if change is not None:
            target = change.target
            lot = self._lots[target.entry_fill_id]
            if target.owner_id != 'protection:' + lot.fill_id or (target.leg_id, target.order_symbol, target.side) != (lot.leg_id, lot.symbol, lot.side):
                raise ValueError('foreign protection target')
            if lot.consumed:
                raise ValueError('consumed protection cannot be attached')
            old = self._orders.get(target.owner_id)
            expected = changed_components(old.effective if old else None, change.effective)
            if expected != change.changed_components:
                raise ValueError('component mutation does not match actual state')
            coverage = self._coverage(lot)
            if type(target.quantity) is not int or target.quantity <= 0 or target.quantity > coverage:
                raise ValueError('invalid protection coverage')
            if old is None and (target.primitive != 'attach' or target.quantity != lot.remaining):
                raise ValueError('attachment requires surviving bare lot')
            if old is not None and (target.primitive != 'amend' or target.quantity != old.quantity):
                raise ValueError('amendment cannot invent quantity reduction')
            if has_components(change.effective):
                self._orders[target.owner_id] = ObservedProtection(
                    target.owner_id, lot.fill_id, lot.leg_id, lot.symbol,
                    old.broker_order_ids if old else ('synthetic:' + target.owner_id,),
                    operation_id, old.revision + 1 if old else 1, target.quantity,
                    change.effective, old.trail_active if old else False,
                    old.trail_anchor if old else None)
            else:
                self._orders.pop(target.owner_id, None)
        elif isinstance(command.action, OrderIntent) and command.kind in ('exit', 'flat'):
            self._close(command, at)
            self._terminal(operation_id, 'filled', at)
        elif command.kind in ('entry', 'add'):
            self._set_working(command)
        elif command.kind == 'cancel':
            self.apply_cancel(operation_id, at=at)
        self._outcomes[operation_id] = outcome

    def execute_entry(self, operation_id, *, fill_id, quantity, price, at):
        command = self._pending[operation_id]
        if (command.kind not in ('entry', 'add') or self._outcomes.get(operation_id) == 'rejected'
                or operation_id in self._terminals):
            raise ValueError('entry is not executable')
        self._validate_fill(quantity, price)
        if fill_id in self._lots or quantity + self._filled.get(operation_id, 0) > command.quantity:
            raise ValueError('duplicate or excessive entry fill')
        self.advance(at)
        lot = _Lot(fill_id, command.leg_id, command.order_symbol, Side(command.side), quantity, price)
        self._lots[fill_id] = lot
        self._entry_operations[fill_id] = operation_id
        self._filled[operation_id] = self._filled.get(operation_id, 0) + quantity
        bracket = normalize_bracket(command.action.bracket, lot.side, self._tick(lot.leg_id))
        if has_components(bracket):
            owner_id = 'protection:' + fill_id
            self._orders[owner_id] = ObservedProtection(owner_id, fill_id, lot.leg_id, lot.symbol,
                ('synthetic:' + owner_id,), operation_id, 1, quantity, bracket, False, None)
        self._outcomes[operation_id] = 'applied'
        fact = BrokerFact.fill(fill_id, operation_id, lot.leg_id, command.kind, quantity, price, at)
        self._history[fact.fact_id] = fact
        self._set_working(command)
        if self._filled[operation_id] == command.quantity:
            self._terminal(operation_id, 'filled', at)
        return fact

    def _set_working(self, command):
        remaining = command.quantity - self._filled.get(command.operation_id, 0)
        if remaining:
            self._working[command.operation_id] = WorkingOrder('synthetic:' + command.operation_id,
                command.operation_id, command.leg_id, command.order_symbol, command.kind, remaining)
        else:
            self._working.pop(command.operation_id, None)

    def _terminal(self, operation_id, status, at):
        if operation_id not in self._terminals:
            fact = BrokerFact.terminal(operation_id, status, self._filled.get(operation_id, 0), at)
            self._terminals[operation_id] = fact
            self._history[fact.fact_id] = fact
        return self._terminals[operation_id]

    def apply_cancel(self, operation_id, *, at):
        command = self._pending[operation_id]
        if command.kind != 'cancel' or self._outcomes.get(operation_id) == 'rejected':
            raise ValueError('cancel is not applicable')
        self.advance(at)
        target = command.target_operation_id
        if target not in self._pending or self._pending[target].kind not in ('entry', 'add'):
            raise ValueError('unknown cancel target')
        self._working.pop(target, None)
        fact = self._terminal(target, 'cancelled', at)
        self._outcomes[operation_id] = 'applied'
        return (fact,)

    def read_bootstrap_inventory(self, request: InventoryRead):
        """Synchronous offline read at the current synthetic clock, without a send."""
        return self._read_inventory(request, bootstrap=True)

    def read_inventory(self, request: InventoryRead):
        return self._read_inventory(request, bootstrap=False)

    def _read_inventory(self, request: InventoryRead, *, bootstrap):
        if (request.occurrence.account, request.occurrence.account_epoch) != (self.account, self.account_epoch):
            raise ValueError('foreign inventory read')
        if (self.drop_reads or self._clock is None or self._clock < request.prepared_at
                or not bootstrap and self._clock == request.prepared_at):
            return None
        self._inventory_sequence += 1
        legs = request.scope_legs
        requests = []
        for op, command in self._pending.items():
            if command.leg_id not in legs:
                continue
            target = command.target_operation_id if command.kind == 'cancel' else op
            terminal = self._terminals.get(target)
            requests.append(RequestOutcome(op, command.attempt_id, command.target_operation_id,
                self._outcomes.get(op, 'pending'), terminal.fact_id if terminal else None))
        return AccountInventory(f'{self.stream_id}:inventory:{self._inventory_sequence}',
            self.account, self.account_epoch, self.stream_id + ':inventory', self._inventory_sequence,
            request.read_id, self._clock, legs, True,
            tuple(InventoryPosition(lot.fill_id, self._entry_operations[lot.fill_id], lot.leg_id,
                  lot.symbol, lot.side.value, lot.remaining) for lot in self._lots.values()
                  if lot.leg_id in legs and lot.remaining),
            tuple(order for order in self._working.values() if order.leg_id in legs),
            self._snapshot(legs), tuple(requests),
            tuple(fact for fact in self._history.values()
                  if self._pending[fact.operation_id].leg_id in legs))

    def execute_close(self, operation_id, *, execution_id, quantity, price, terminal, at):
        command = self._pending[operation_id]
        if (command.kind not in ('exit', 'flat') or operation_id in self._terminals
                or self._outcomes.get(operation_id) == 'rejected'):
            raise ValueError('close is not executable')
        self._validate_fill(quantity, price)
        if (type(terminal) is not bool or not isinstance(execution_id, str) or not execution_id
                or execution_id in self._close_execution_ids
                or self._filled.get(operation_id, 0) + quantity > command.quantity):
            raise ValueError('invalid close execution')
        self.advance(at)
        self._prices[command.leg_id] = price
        self._close(replace(command, quantity=quantity), at, execution_id=execution_id)
        self._close_execution_ids.add(execution_id)
        self._outcomes[operation_id] = 'applied'
        self._set_working(command)
        facts = self._facts[operation_id]
        if terminal:
            self._working.pop(operation_id, None)
            status = 'filled' if self._filled[operation_id] == command.quantity else 'cancelled'
            facts += (self._terminal(operation_id, status, at),)
        return facts

    @staticmethod
    def _validate_fill(quantity, price):
        if type(quantity) is not int or quantity <= 0 or type(price) not in (int, float) or not math.isfinite(price):
            raise ValueError('invalid fill')

    def _coverage(self, lot):
        return sum(other.remaining for other in self._lots.values()
                   if (other.leg_id, other.symbol, other.side) == (lot.leg_id, lot.symbol, lot.side))

    def _snapshot(self, legs):
        self._sequence += 1
        return ProtectionSnapshot(f'{self.stream_id}:{self._sequence}', self.account, self.account_epoch,
            self.stream_id, self._sequence, self._clock, tuple(legs), True,
            tuple(order for order in self._orders.values() if order.leg_id in legs),
            tuple((lot.fill_id, lot.remaining) for lot in self._lots.values() if lot.leg_id in legs and lot.remaining),
            tuple((op, result) for op, result in self._outcomes.items() if self._pending[op].leg_id in legs))

    def read_protection(self, request: ProtectionRead):
        if (request.occurrence.account, request.occurrence.account_epoch) != (self.account, self.account_epoch):
            raise ValueError('foreign protection read')
        if self.drop_reads or self._clock is None or self._clock <= request.prepared_at:
            return None
        return self._snapshot(request.scope_legs)

    def execute_protection(self, owner_id, *, quantity, price, terminal, at):
        self._validate_fill(quantity, price)
        order = self._orders[owner_id]
        lot = self._lots[order.entry_fill_id]
        if type(terminal) is not bool or quantity > order.quantity or quantity > self._coverage(lot):
            raise ValueError('invalid protection execution coverage')
        if not terminal and quantity == order.quantity:
            raise ValueError('exhausted order must be terminal')
        self.advance(at)
        remaining, allocations = quantity, []
        for other in self._lots.values():
            if (other.leg_id, other.symbol, other.side) != (lot.leg_id, lot.symbol, lot.side):
                continue
            take = min(other.remaining, remaining)
            if take:
                other.remaining -= take
                remaining -= take
                allocations.append((other.fill_id, take))
        if terminal:
            del self._orders[owner_id]
            lot.consumed = True
        else:
            self._orders[owner_id] = replace(order, quantity=order.quantity - quantity)
        self._cap_orders()
        snapshot = self._snapshot((lot.leg_id,))
        return ProtectionExecution('execution:' + snapshot.fact_id, self.account, self.account_epoch,
            owner_id, order.broker_order_ids[0], at, quantity, price, tuple(allocations), terminal, snapshot)

    def _cap_orders(self):
        for owner_id, order in tuple(self._orders.items()):
            coverage = self._coverage(self._lots[order.entry_fill_id])
            if not coverage:
                del self._orders[owner_id]
                self._lots[order.entry_fill_id].consumed = True
            elif order.quantity > coverage:
                self._orders[owner_id] = replace(order, quantity=coverage)

    def _close(self, command, at, execution_id=None):
        if command.leg_id not in self._prices:
            raise ValueError('explicit market price required for close')
        price = self._prices[command.leg_id]
        selected = [lot for lot in self._lots.values() if lot.leg_id == command.leg_id and
                    (command.action.scope_fill_ids is None or lot.fill_id in command.action.scope_fill_ids)]
        remaining = command.quantity if command.quantity is not None else sum(lot.remaining for lot in selected)
        if sum(lot.remaining for lot in selected) < remaining:
            raise ValueError('close exceeds surviving inventory')
        if any(f'{execution_id or "close:" + command.operation_id}:{lot.fill_id}' in self._history
               for lot in selected if lot.remaining):
            raise ValueError('duplicate close execution')
        facts = []
        for lot in selected:
            take = min(lot.remaining, remaining)
            if not take:
                continue
            lot.remaining -= take
            remaining -= take
            identity = f'{execution_id or "close:" + command.operation_id}:{lot.fill_id}'
            facts.append(BrokerFact.fill(identity, command.operation_id,
                lot.leg_id, command.kind, take, price, at, entry_execution_id=lot.fill_id))
            if not lot.remaining:
                self._orders.pop('protection:' + lot.fill_id, None)
                lot.consumed = True
        self._cap_orders()
        self._facts[command.operation_id] = tuple(facts)
        self._filled[command.operation_id] = self._filled.get(command.operation_id, 0) + sum(f.quantity for f in facts)
        self._history.update((f.fact_id, f) for f in facts)

    def result_facts(self, operation_id):
        return self._facts.get(operation_id, ())

    def mark_price(self, leg_id, price, *, at):
        """Advance trailing state using an explicit market-price observation."""
        self._validate_fill(1, price)
        self.advance(at)
        self._prices[leg_id] = price
        for owner_id, order in tuple(self._orders.items()):
            if order.leg_id != leg_id or order.effective.trail_activation_ticks is None:
                continue
            lot = self._lots[order.entry_fill_id]
            direction = 1 if lot.side == Side.BUY else -1
            active = order.trail_active or direction * (price - lot.price) >= order.effective.trail_activation_ticks * self._tick(leg_id)
            if active:
                anchor = price if order.trail_anchor is None else (max(order.trail_anchor, price) if direction == 1 else min(order.trail_anchor, price))
                self._orders[owner_id] = replace(order, trail_active=True, trail_anchor=anchor)
