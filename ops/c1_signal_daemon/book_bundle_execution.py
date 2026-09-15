"""Offline single-bundle shared sizing and confirmed feedback.

This is an emulator integration component, not a source-admission authority,
durable account owner or live sender. Mode/lifecycle are fixed comparison inputs.
The four-leg owner, settlement-derived mode changes and account reservations
remain separate integration requirements. Private port bodies are not modified.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction

from c1_rail.book_policy import (
    ACCOUNT_MICRO_CAP, add_quantity, entry_quantities, leg, require_policy,
)
from c1_signal_daemon.book_protocol import ExecutionEvent, Mode, OrderIntent, Side


@dataclass(frozen=True)
class SizingInputs:
    leg_id: str
    mode: Mode
    lifecycle_tier: str
    cap_alloc: int
    risk_dollars: object
    pointvalue: float


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def check_margin_phase(emulator, bar, new_actions):
    """Sufficient long-only ORB margin bound for one enumerated emulator phase.

    Call before process_bar with all queued orders, before submit with its whole
    action batch, and after submit with no new orders. No intrabar recalculation,
    at most three new contracts per phase, no more than three existing contracts.
    Refusal means the proof failed, not necessarily that a margin call occurred.
    Affordability remains implemented by the emulator and is never disabled.
    """
    exact = lambda value: Fraction(str(value))
    try:
        lo, hi, opening, close = map(exact, (bar.low, bar.high, bar.open, bar.close))
        point, tick, fee, margin = map(exact, (emulator.pointvalue, emulator.mintick,
                                             emulator.commission_per_side, emulator.margin_pct))
        require(emulator.leg_id == "orb_mnq_v7" and point == 2 and tick == Fraction(1, 4),
                "margin_domain_instrument")
        require(0 < lo <= min(opening, close) <= max(opening, close) <= hi,
                "margin_domain_prices")
        require(type(emulator.slippage_ticks) is int and emulator.slippage_ticks >= 0
                and fee >= 0 and margin > 0, "margin_domain_costs")
        slip = tick * emulator.slippage_ticks
        entries = [a for a in new_actions if isinstance(a, OrderIntent) and a.kind in ("entry", "add")]
        require(all(a.leg_id == emulator.leg_id and a.side is Side.BUY and
                    type(a.qty) is int and a.qty > 0 for a in entries), "margin_domain_orders")
        require(sum(a.qty for a in entries) <= 3, "margin_domain_new_quantity")
        # Exact remaining lot quantities, including emulator FIFO partial exits.
        lots = [lot for lot in emulator._open.values() if lot.lot_qty > 0]
        require(all(lot.is_long and type(lot.lot_qty) is int for lot in lots), "margin_domain_side")
        existing = sum(lot.lot_qty for lot in lots)
        require(existing <= 3, "margin_domain_existing_quantity")
        lower = exact(emulator.initial_capital) + exact(emulator.realized_net())
        for lot in lots:
            # Do not count unrealized gains. Charge even the full original entry
            # fee on a partly closed lot; this only lowers the sufficient bound.
            loss = max(Fraction(0), exact(lot.fill.price) - (lo - slip))
            lower -= loss * point * lot.lot_qty + exact(lot.fill.commission) + fee * lot.lot_qty
        # Permit three replacements EVEN IF all three old lots are present.
        lower -= 3 * ((hi + slip - (lo - slip)) * point + 2 * fee)
        required_margin = (existing + 3) * (hi + slip) * point * margin / 100
        require(lower > required_margin, "margin_envelope_failed")
    except (TypeError, ZeroDivisionError, OverflowError) as exc:
        raise ValueError("margin_domain_invalid_number") from exc


def run_sized_adapter(execution, bars, emulator):
    """Run the complete feedback path, checking every finite-margin phase.

    Queue enumeration is owned here, not provided by a caller's assertion.
    This does not select files or grant source admission. The caller must bind
    the panel, source settings and inputs before treating results as evidence.
    """
    require(isinstance(execution, BundleExecution) and execution.leg_id == emulator.leg_id,
            "execution_identity_mismatch")
    count = checks = 0
    previous = None
    for bar in bars:
        require(bar.ts.tzinfo is not None and (previous is None or bar.ts > previous),
                "invalid_bar_sequence")
        previous = bar.ts
        if emulator.margin_pct:
            queued = [*emulator._pending_market, *emulator._pending_stop.values()]
            check_margin_phase(emulator, bar, queued)
            checks += 1
        for event in emulator.process_bar(bar):
            execution.on_execution(event)
        actions = execution.on_bar(bar)
        if emulator.margin_pct:
            check_margin_phase(emulator, bar, actions)
            checks += 1
        for event in emulator.submit(actions, bar):
            execution.on_execution(event)
        if emulator.margin_pct:
            check_margin_phase(emulator, bar, [])
            checks += 1
        count += 1
    require(count > 0, "empty_panel")
    return {"bars": count, "margin_phase_checks": checks}


class BundleExecution:
    """Resize a copy of source intents; deliver actual outcomes exactly once."""

    def __init__(self, adapter, inputs: SizingInputs, *, policy):
        require_policy(policy)
        require(adapter.leg_id == inputs.leg_id, "adapter_identity_mismatch")
        require(type(inputs.cap_alloc) is int and 0 < inputs.cap_alloc <= ACCOUNT_MICRO_CAP,
                "invalid_allocation")
        require(Fraction(str(inputs.pointvalue)) > 0, "invalid_pointvalue")
        self.adapter = adapter
        self.inputs = inputs
        self.policy = policy
        self.leg_id = inputs.leg_id
        self.confirmed_base = 0
        self._base_order = None
        self._pending = {}
        self._lots = {}
        self._seen_fills = set()

    @property
    def open_quantity(self):
        return sum(self._lots.values())

    def on_bar(self, bar):
        return self.admit(self.adapter.on_bar(bar), bar)

    def admit(self, actions, bar):
        out = []
        cfg = self.inputs
        for action in actions:
            require(action.leg_id == self.leg_id, "action_identity_mismatch")
            if not isinstance(action, OrderIntent) or action.kind not in ("entry", "add"):
                out.append(action)
                continue
            if action.kind == "entry":
                require(self.open_quantity == 0, "entry_requires_empty_leg")
                qty, _ = entry_quantities(
                    self.leg_id, mode=cfg.mode, lifecycle_tier=cfg.lifecycle_tier,
                    policy=self.policy, normal_base=action.qty,
                    risk_dollars=cfg.risk_dollars,
                    per_contract_risk=Fraction(str(action.stop_dist_pts)) * Fraction(str(cfg.pointvalue)),
                    cap_alloc=cfg.cap_alloc)
            else:
                require(not any(kind == "entry" for kind, _ in self._pending.values()), "pending_base")
                require(self.confirmed_base > 0 and self.open_quantity > 0, "add_requires_confirmed_base")
                qty = add_quantity(self.leg_id, self.confirmed_base, mode=cfg.mode,
                                   lifecycle_tier=cfg.lifecycle_tier, policy=self.policy)
            if qty == 0:
                self.adapter.on_execution(ExecutionEvent(
                    "reject", self.leg_id, bar.ts, order_id=action.order_id,
                    detail="shared_sizing_zero"))
                continue
            previous = self._pending.get(action.order_id)
            require(previous is None or previous == (action.kind, qty), "pending_order_redefinition")
            reserved = sum(n for oid, (_, n) in self._pending.items() if oid != action.order_id)
            require((self.open_quantity + reserved + qty) * leg(self.leg_id).micro_equiv <= cfg.cap_alloc,
                    "allocation_refusal")
            self._pending[action.order_id] = (action.kind, qty)
            out.append(replace(action, qty=qty))
        return out

    def on_execution(self, event):
        require(event.leg_id == self.leg_id, "event_identity_mismatch")
        if event.event in ("cancel", "reject"):
            require(event.order_id in self._pending, "unknown_terminal_order")
            del self._pending[event.order_id]
        elif event.event == "fill":
            fill = event.fill
            require(fill is not None and fill.leg_id == self.leg_id, "missing_or_wrong_fill")
            require(fill.fill_id not in self._seen_fills, "duplicate_fill")
            require(type(fill.qty) is int and fill.qty > 0, "invalid_fill_quantity")
            if fill.kind in ("entry", "add"):
                require(fill.order_id in self._pending, "unknown_entry")
                kind, remaining = self._pending[fill.order_id]
                require(kind == fill.kind and fill.qty <= remaining, "fill_exceeds_request")
                if fill.kind == "entry":
                    require(self._base_order in (None, fill.order_id), "multiple_base_orders")
                    self._base_order = fill.order_id
                    self.confirmed_base += fill.qty
                if remaining == fill.qty:
                    del self._pending[fill.order_id]
                else:
                    self._pending[fill.order_id] = (kind, remaining - fill.qty)
                self._lots[fill.fill_id] = fill.qty
            else:
                require(fill.kind in ("exit", "flat") and fill.entry_fill_id in self._lots,
                        "unknown_exit_lot")
                remaining = self._lots[fill.entry_fill_id]
                require(fill.qty <= remaining, "exit_exceeds_lot")
                if fill.qty == remaining:
                    del self._lots[fill.entry_fill_id]
                else:
                    self._lots[fill.entry_fill_id] = remaining - fill.qty
            self._seen_fills.add(fill.fill_id)
        else:
            raise ValueError("unsupported_execution_event")
        if not self._lots and not self._pending:
            self.confirmed_base = 0
            self._base_order = None
        # This is the original broker event, including actual size/fees/PnL inputs.
        self.adapter.on_execution(event)

    def checkpoint(self):
        return {"source": self.adapter.checkpoint(), "confirmed_base": self.confirmed_base,
                "base_order": self._base_order, "open_quantity": self.open_quantity,
                "pending": dict(self._pending)}
