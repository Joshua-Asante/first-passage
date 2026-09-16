"""Daemon side of the TB-S3 kernel model: emission gates by action class, source health,
feed-loss flat intents and control reads (spec §1 ``emit``, R-N, S6).

The daemon never writes listener state; it reads the control endpoint (which stamps the
listener's ``last_control_read``) and emits intents. Risk-adding emissions need a fresh
control read and no kill; risk-reducing emissions need only the daemon's own config and a
matching active-leg digest (spec rev 5.4 ``emit_risk_add`` / ``emit_risk_reducing``).
"""
from __future__ import annotations

from dataclasses import dataclass, field
import copy
from datetime import datetime

from c1_rail.book_policy import leg as leg_spec
from book_protocol import Bracket

from .broker import BAR, STALENESS_WINDOW, Clock
from .kernel import bracket_dict, components_of, Store, KernelRefusal
from .account import AccountKernel as Kernel

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
    store: Store = field(default_factory=Store)
    reports: dict = field(default_factory=dict)
    report_seq: dict = field(default_factory=dict)
    started_at: datetime | None = None
    episode_boundaries: dict = field(default_factory=dict)

    def __post_init__(self):
        self.started_at = self.started_at or self.clock.now
        if self.store.data is not None:
            required = {"source_last_bar", "feed_loss_ops", "reports", "report_seq", "started_at",
                        "episode_boundaries"}
            if self.store.data.get("schema") != 1 or not required <= self.store.data.keys():
                raise KernelRefusal("incompatible daemon snapshot")
            for key in required:
                value = self.store.data[key]
                setattr(self, key, copy.deepcopy(value))

    def persist(self):
        self.store.data = {"schema": 1, **{key: copy.deepcopy(getattr(self, key)) for key in
                          ("source_last_bar", "feed_loss_ops", "reports", "report_seq", "started_at",
                           "episode_boundaries")}}

    def deliver_reports(self):
        for seq, report in sorted(list(self.reports.items())):
            if self.kernel.source_report(report):
                self.reports.pop(seq)
                self.persist()
            else:
                break

    def _report(self, kind, leg_id, episode, now):
        seq = self.report_seq.get(leg_id, 0) + 1
        self.report_seq[leg_id] = seq
        self.reports[leg_id, seq] = dict(kind=kind, leg_id=leg_id, episode=episode,
                                        at=now, seq=seq,
                                        source_at=self.source_last_bar.get(leg_spec(leg_id).symbol,
                                                                          self.started_at))
        self.persist()
        self.deliver_reports()

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
                and not self.reports
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
    def reissue(self, leg_id: str, fill_id: str, bracket: Bracket | dict, bar_close: float,
                now: datetime) -> str:
        """S3 (d): for an ``orders_on_close`` leg a newly issued fixed level already crossed
        by the generating close is a market exit at the signal (the emulator's
        ``_evaluate_at_close`` rule); otherwise the re-issue is an ``AMEND``/``ATTACH``."""
        cases = self.kernel.protection_cases.get(leg_id, set())
        lot = self.kernel.lots.get(fill_id)
        if lot is None or lot.leg_id != leg_id:
            return "invalid_owner"
        try:
            components_of(bracket)
        except (ValueError, TypeError):
            return "invalid_bracket"
        long = lot.side == "buy"
        raw = bracket_dict(bracket)
        stop, limit = raw.get("stop"), raw.get("limit")
        crossed = ((stop is not None and (bar_close <= stop if long else bar_close >= stop))
                   or (limit is not None and (bar_close >= limit if long else bar_close <= limit)))
        if "orders_on_close" in cases and crossed and self.emit_risk_reducing():
            ev = self.kernel.coherent_evidence(lot.sym, now)
            if ev is None or ev.protection_owners.get(fill_id, {}).get("consumed"):
                return "amend_deferred"
            qty = ev.protection_owners[fill_id]["qty"] or lot.qty
            component = "stop" if stop is not None and (
                bar_close <= stop if long else bar_close >= stop) else "limit"
            self.kernel.close("fill", fill_id, now, "exit", qty=qty,
                              transition="triggered_protection",
                              trigger_bracket={component: raw[component]})
            return "close_time_exit"
        action = self.kernel.amend_action(fill_id, bracket, now)
        if action is None:
            return "amend_deferred"
        if not self.may_emit(action, now):
            return "suppressed"
        return self.kernel.amend(fill_id, bracket, now).reason

    # ── source health and the feed-loss flat (S6) ──────────────────────────
    def on_bar(self, sym: str, now: datetime) -> None:
        """A bar arrived from ``sym``'s source: the source is healthy and any episode ends."""
        if sym in self.source_last_bar and now <= self.source_last_bar[sym]:
            return
        self.source_last_bar[sym] = now
        recovered = set()
        for leg_id in [l for l, _ in self.feed_loss_ops.items() if leg_spec(l).symbol == sym]:
            if (now < self.episode_boundaries[leg_id]
                    or self.clock.now - now > STALENESS_WINDOW):
                continue
            episode = self.feed_loss_ops.pop(leg_id)
            self._report("recovery", leg_id, episode, now)
            recovered.add(leg_id)
        for leg_id in list(self.report_seq):
            if (leg_spec(leg_id).symbol == sym and leg_id not in self.feed_loss_ops
                    and leg_id not in recovered):
                self._report("health", leg_id, "", now)
        self.persist()

    def source_unhealthy(self, sym: str, now: datetime) -> bool:
        """S2b staleness formula: ``2 × bar_period + 30 s`` without a bar."""
        last = self.source_last_bar.get(sym, self.started_at)
        return now - last > STALENESS_WINDOW

    def feed_loss_check(self, leg_id: str, now: datetime) -> str | None:
        """Emit one ``flat`` intent per feed-loss episode for a leg whose symbol is not
        confirmed flat; redelivery reuses the episode's operation identity."""
        sym = leg_spec(leg_id).symbol
        if not self.source_unhealthy(sym, now) or not self.emit_risk_reducing():
            return None
        episode = self.source_last_bar.get(sym)
        op_id = self.feed_loss_ops.get(leg_id) or (
            f"feedloss:{leg_id}:{episode.isoformat() if episode else 'never'}")
        if leg_id not in self.feed_loss_ops:
            self.feed_loss_ops[leg_id] = op_id
            self.episode_boundaries[leg_id] = now
            self._report("open", leg_id, op_id, now)
        else:
            self.deliver_reports()
        return op_id
