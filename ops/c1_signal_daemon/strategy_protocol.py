"""Pluggable strategy evaluate hook — no Striker redeploy under S2b build ADR."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from c1_signal_daemon.feed import Bar


@dataclass(frozen=True)
class Signal:
    """Strategy intent before B1 packing / fail-closed gate."""

    leg_id: str
    signal_type: str
    close: float
    stop_dist_pts: float
    bar_time: str | int | float


class Strategy(Protocol):
    def on_bar(self, bar: Bar) -> Signal | None:
        """Return a Signal to emit, or None for no-fire."""


class NullStrategy:
    """Default: never emits (warm daemon until a strategy GO)."""

    def on_bar(self, bar: Bar) -> Signal | None:
        return None
