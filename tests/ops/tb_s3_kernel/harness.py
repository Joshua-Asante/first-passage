"""Shared harness for the kernel-model tests: a world (clock, broker, kernel, daemon) and
helpers that read like the spec's acceptance cases."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

from book_policy import leg as leg_spec
from book_protocol import Bracket, OrderIntent

from .broker import BAR, SUPPORTED, Clock, FakeBroker
from .daemon import Daemon
from .kernel import OWNED_SYMBOLS, Kernel, Store

T0 = datetime(2026, 9, 14, 9, 45)
MIN = timedelta(minutes=1)

DEFAULT_CASES = {
    "dj30_mym_p250": {"bare_entry", "orders_on_close"},   # emulator evidence (Striker)
    "orb_mnq_v7": {"bracket_at_entry", "trailing"},        # ORB export evidence
    "aegis_6j": {"bracket_at_entry"},
    "vanguard_mgc": {"bracket_at_entry"},
}


@dataclass
class World:
    """Everything one scenario needs."""

    clock: Clock
    broker: FakeBroker
    kernel: Kernel
    daemon: Daemon

    @property
    def now(self) -> datetime:
        """The scenario clock."""
        return self.clock.now

    def advance(self, delta: timedelta) -> datetime:
        """Move the clock."""
        return self.clock.advance(delta)

    def snap(self, *syms: str, at: datetime | None = None) -> None:
        """Feed the kernel a broker read of each symbol (default: every owned symbol, now)."""
        for sym in syms or OWNED_SYMBOLS:
            self.kernel.apply_evidence(self.broker.snapshot(sym, at))

    def bars(self, at: datetime | None = None) -> None:
        """Every source delivered a bar (all healthy)."""
        for sym in OWNED_SYMBOLS:
            self.daemon.on_bar(sym, at or self.now)


def make_world(caps: dict[str, str] | None = None, cases: dict | None = None,
               start: datetime = T0, **kernel_kwargs) -> World:
    """A fresh world with fresh evidence for every symbol and every source healthy."""
    clock = Clock(start)
    broker = FakeBroker(clock)
    if caps:
        broker.caps.update(caps)
    kernel = Kernel(broker, clock, store=Store(),
                    protection_cases=dict(cases if cases is not None else DEFAULT_CASES),
                    **kernel_kwargs)
    daemon = Daemon(kernel, clock)
    world = World(clock, broker, kernel, daemon)
    world.snap()
    world.bars()
    daemon.control_read(start)
    return world


def entry(leg_id: str, qty: int, bracket: Bracket | None = None, kind: str = "entry",
          order_type: str = "market", price: float | None = None) -> OrderIntent:
    """An adapter intent in the delivered protocol shape (qty = adapter-normal, R-P)."""
    spec = leg_spec(leg_id)
    return OrderIntent(order_id=f"{leg_id}-{kind}", leg_id=leg_id, kind=kind,
                       side=spec.entry_side, qty=qty, order_type=order_type, price=price,
                       bracket=bracket)


def fill_lot(world: World, leg_id: str, qty: int, bracket: Bracket | None = None,
             **kw) -> str:
    """Admit, fill and evidence one entry/add; return its lot id."""
    decision = world.kernel.admit_entry(entry(leg_id, qty, bracket, **kw), world.now)
    assert decision.ok, decision.reason
    world.broker.fill(decision.ref)
    world.advance(MIN)
    world.snap()
    lot_id = world.broker.lot_id(decision.ref)
    assert world.kernel.lots[lot_id].qty == qty
    return lot_id


def all_supported() -> dict[str, str]:
    """Every L-2 item recorded as supported."""
    return {i: SUPPORTED for i in "abcdefg"}


__all__ = ["BAR", "MIN", "T0", "World", "all_supported", "entry", "fill_lot", "make_world"]
