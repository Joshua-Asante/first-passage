"""Fixed-book adapter protocol — Track B offline surface (umbrella TB-S3 (C)/(D)/(M)).

`strategy_protocol.Signal` carries one leg-less intent per bar. The accepted
four-strategy book needs more: an explicit order side (D-B7), an integer
quantity, per-fill exit brackets (TradingView attaches one exit per entry
fill — the captured exports show base and add fills leaving on different
bars), and an execution-feedback path so an adapter advances its
position-dependent state ONLY from confirmed fills, never from its own
emitted intent (TB-S3 (M)).

Nothing here emits, sizes for the account, or touches the rail. The daemon
registry / bar-time barrier / listener wiring is TB-I3; this module is the
contract the four private adapters (TB-A1..A4) implement and the offline
broker emulator (`tv_broker_emulator.py`) executes.

Timing vocabulary mirrors TradingView's broker emulator:

* ``FillTiming.THIS_CLOSE`` — ``process_orders_on_close=true`` scripts (ORB,
  Striker MYM): a market order generated at a bar's close fills at that same
  close.
* ``FillTiming.NEXT_OPEN`` — default scripts (Aegis, Vanguard): a market order
  generated at a bar's close fills at the next bar's open.
* ``order_type="stop"`` — a price-triggered entry (ORB's breakout stop); fills
  intrabar at the level (plus slippage) or at the open after a gap.

Exit levels live in a :class:`Bracket` attached to each fill; the adapter may
re-issue (amend) the bracket every bar exactly as Pine re-calls
``strategy.exit`` — trailing activation state persists in the emulator.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Protocol, Union

from c1_signal_daemon.feed import Bar


class Side(str, Enum):
    BUY = "buy"
    SELL = "sell"


class FillTiming(str, Enum):
    NEXT_OPEN = "next_open"
    THIS_CLOSE = "this_close"


class Mode(str, Enum):
    """Book protection mode for the day (set from the prior settled close)."""

    NORMAL = "normal"
    PROTECTED = "protected"


SIGNAL_KINDS = frozenset({"entry", "add", "exit", "flat"})


@dataclass(frozen=True)
class Bracket:
    """Per-fill exit levels (price units; trailing in ticks, TV semantics)."""

    stop: float | None = None
    limit: float | None = None
    trail_activation_ticks: int | None = None
    trail_offset_ticks: int | None = None


@dataclass(frozen=True)
class OrderIntent:
    """One order the adapter wants placed. Quantity is an integer contract count."""

    order_id: str
    leg_id: str
    kind: str                     # entry | add | exit | flat
    side: Side                    # side of THIS order (an exit of a short is BUY)
    qty: int | None               # None on exit/flat = every open fill in scope
    order_type: str = "market"    # market | stop
    price: float | None = None    # trigger level for order_type == "stop"
    timing: FillTiming = FillTiming.NEXT_OPEN
    bracket: Bracket | None = None            # entries/adds: attached to the resulting fill
    scope_fill_ids: tuple[str, ...] | None = None  # exits: fills to close (None = all)
    oca_group: str | None = None
    stop_dist_pts: float = 0.0    # B1 payload field (listener contract)
    bar_time: datetime | None = None
    reason: str = ""

    def __post_init__(self) -> None:
        if self.kind not in SIGNAL_KINDS:
            raise ValueError(f"unknown kind {self.kind!r}; valid: {sorted(SIGNAL_KINDS)}")
        if self.order_type not in ("market", "stop"):
            raise ValueError(f"unknown order_type {self.order_type!r}")
        if self.kind in ("entry", "add"):
            if not isinstance(self.qty, int) or self.qty <= 0:
                raise ValueError(f"{self.kind} qty must be a positive int, got {self.qty!r}")
        elif self.qty is not None and (not isinstance(self.qty, int) or isinstance(self.qty, bool)
                                       or self.qty <= 0):
            raise ValueError(f"{self.kind} qty must be None (all in scope) or a positive int, got {self.qty!r}")
        if self.order_type == "stop" and self.price is None:
            raise ValueError("stop order needs a trigger price")


@dataclass(frozen=True)
class BracketAmend:
    """Re-issue exit levels for open fills (Pine: strategy.exit called again)."""

    leg_id: str
    bracket: Bracket
    scope_fill_ids: tuple[str, ...] | None = None  # None = every open fill of the leg


@dataclass(frozen=True)
class Cancel:
    """Cancel pending (unfilled) entry/add orders; None = every pending order of the leg."""

    leg_id: str
    order_id: str | None = None


Action = Union[OrderIntent, BracketAmend, Cancel]


@dataclass(frozen=True)
class Fill:
    fill_id: str
    order_id: str
    leg_id: str
    kind: str                 # entry | add | exit | flat
    side: Side
    qty: int
    price: float              # includes slippage where TV applies it
    bar_time: datetime        # open time of the bar the fill is recorded on
    entry_fill_id: str | None = None   # exits: the entry fill closed
    commission: float = 0.0            # cash charged on this side (per contract x qty)
    reason: str = ""


@dataclass(frozen=True)
class ExecutionEvent:
    """Broker-confirmed outcome delivered to the adapter (TB-S3 (M))."""

    event: str                # fill | cancel | reject
    leg_id: str
    bar_time: datetime
    fill: Fill | None = None
    order_id: str | None = None
    detail: str = ""


class BookStrategy(Protocol):
    """What every fixed-book adapter implements."""

    leg_id: str

    def on_bar(self, bar: Bar) -> list[Action]:
        """Evaluate one completed bar; return the orders/amends/cancels it wants."""

    def on_execution(self, event: ExecutionEvent) -> None:
        """Advance position-dependent state from a confirmed outcome only."""

    def set_mode(self, mode: Mode) -> list[Action]:
        """Apply the day's protection mode; may return cancels (ORB resting adds)."""

    def checkpoint(self) -> dict:
        """Durable per-bar state for warm restart (TB-S3 (H))."""
