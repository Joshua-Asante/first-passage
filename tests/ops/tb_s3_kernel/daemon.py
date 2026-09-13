"""Daemon side of the TB-S3 kernel model: emission gates by action class, source health,
feed-loss flat intents and control reads (spec §1 ``emit``, R-N, S6).

The daemon never writes listener state; it reads the control endpoint (which stamps the
listener's ``last_control_read``) and emits intents. Risk-adding emissions need a fresh
control read and no kill; risk-reducing emissions need only the daemon's own config and a
matching active-leg digest (spec rev 5.4 ``emit_risk_add`` / ``emit_risk_reducing``).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from book_policy import leg as leg_spec

from .broker import BAR, STALENESS_WINDOW, Clock
from .kernel import Kernel

RISK_ADDING = frozenset({"entry", "add", "loosening_amend", "protective_cancel"})
RISK_REDUCING = frozenset({"exit", "flat", "cancel_resting", "tightening_amend", "attach",
                           "feed_loss_flat"})


@dataclass
class Daemon:
    """The signal daemon's emission control surface."""

    kernel: Kernel
    clock: Clock
    emit_enabled: bool = True
    digest_ok: bool = True
    last_control: dict | None = None
    last_control_at: datetime | None = None
    source_last_bar: dict[str, datetime] = field(default_factory=dict)
    feed_loss_ops: dict[str, str] = field(default_factory=dict)   # leg -> op id of the episode

    # ── control read (R-N) ──────────────────────────────────────────────────
    def control_read(self, now: datetime, reachable: bool = True) -> dict | None:
        """Read the listener's control state; the listener records the read time."""
        if not reachable:
            return None
        self.kernel.record_control_read(now)
        self.last_control = {"kill": "kill" in self.kernel.blocks,
                             "blocks": sorted(self.kernel.blocks)}
        self.last_control_at = now
        return self.last_control

    def control_fresh(self, now: datetime) -> bool:
        """A control read older than one bar is stale."""
        return self.last_control_at is not None and now - self.last_control_at <= BAR

    # ── emission gates (spec §1 ``emit``) ──────────────────────────────────
    def emit_risk_add(self, now: datetime) -> bool:
        """config ∧ fresh control read ∧ ¬kill ∧ digest."""
        return (self.emit_enabled and self.digest_ok and self.control_fresh(now)
                and not (self.last_control or {}).get("kill", False))

    def emit_risk_reducing(self) -> bool:
        """config ∧ digest — kill and a stale control read never suppress risk reduction."""
        return self.emit_enabled and self.digest_ok

    def may_emit(self, action: str, now: datetime) -> bool:
        """Whether an action of the given class may leave the daemon now."""
        if action in RISK_ADDING:
            return self.emit_risk_add(now)
        if action in RISK_REDUCING:
            return self.emit_risk_reducing()
        raise ValueError(f"unclassified action {action!r}")

    # ── the port re-issued its bracket (S3 (c)/(d)) ────────────────────────
    def reissue(self, leg_id: str, fill_id: str, bracket: dict, bar_close: float,
                now: datetime) -> str:
        """S3 (d): for an ``orders_on_close`` leg a newly issued fixed level already crossed
        by the generating close is a market exit at the signal (the emulator's
        ``_evaluate_at_close`` rule); otherwise the re-issue is an ``AMEND``/``ATTACH``."""
        cases = self.kernel.protection_cases.get(leg_id, set())
        lot = self.kernel.lots[fill_id]
        long = lot.side == "buy"
        stop, limit = bracket.get("stop"), bracket.get("limit")
        crossed = ((stop is not None and (bar_close <= stop if long else bar_close >= stop))
                   or (limit is not None and (bar_close >= limit if long else bar_close <= limit)))
        if "orders_on_close" in cases and crossed and self.emit_risk_reducing():
            self.kernel.handle_exit(leg_id, now, fill_id=fill_id, qty=lot.qty)
            return "close_time_exit"
        if not self.may_emit("tightening_amend", now):
            return "suppressed"
        return self.kernel.amend(fill_id, bracket, now).reason

    # ── source health and the feed-loss flat (S6) ──────────────────────────
    def on_bar(self, sym: str, now: datetime) -> None:
        """A bar arrived from ``sym``'s source: the source is healthy and any episode ends."""
        self.source_last_bar[sym] = now
        for leg_id in [l for l, _ in self.feed_loss_ops.items() if leg_spec(l).symbol == sym]:
            self.feed_loss_ops.pop(leg_id, None)

    def source_unhealthy(self, sym: str, now: datetime) -> bool:
        """S2b staleness formula: ``2 × bar_period + 30 s`` without a bar."""
        last = self.source_last_bar.get(sym)
        return last is None or now - last > STALENESS_WINDOW

    def feed_loss_check(self, leg_id: str, now: datetime) -> str | None:
        """Emit one ``flat`` intent per feed-loss episode for a leg whose symbol is not
        confirmed flat; redelivery reuses the episode's operation identity."""
        sym = leg_spec(leg_id).symbol
        if not self.source_unhealthy(sym, now) or not self.emit_risk_reducing():
            return None
        state, qty = self.kernel.position(sym, now)
        if state == "CONFIRMED" and qty == 0:
            return None
        episode = self.source_last_bar.get(sym)
        op_id = self.feed_loss_ops.get(leg_id) or (
            f"feedloss:{leg_id}:{episode.isoformat() if episode else 'never'}")
        self.feed_loss_ops[leg_id] = op_id
        self.kernel.on_flat_intent(op_id, leg_id, now)
        return op_id
