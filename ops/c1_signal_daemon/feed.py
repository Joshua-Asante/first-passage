"""Feed health + staleness (build ADR: 2× bar_period + 30s)."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Protocol

STALENESS_SLACK_S = 30.0


@dataclass(frozen=True)
class Bar:
    """One OHLCV bar from the live evaluate feed."""

    ts: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0


class BarSource(Protocol):
    """Live CME bar feed (Databento Live ohlcv-1m in production)."""

    def poll(self) -> Bar | None:
        """Return the newest bar, or None if none yet / disconnected."""

    @property
    def connected(self) -> bool:
        """True while the transport session is up."""


def staleness_limit_s(bar_period_s: float) -> float:
    """Canonical unhealthy age: 2 × bar_period + 30s."""
    if bar_period_s <= 0:
        raise ValueError(f"bar_period_s must be > 0, got {bar_period_s}")
    return 2.0 * float(bar_period_s) + STALENESS_SLACK_S


def feed_healthy(
    *,
    connected: bool,
    last_bar_ts: datetime | None,
    now: datetime,
    bar_period_s: float,
) -> bool:
    """False when disconnected, missing bars, or last bar older than limit."""
    if not connected:
        return False
    if last_bar_ts is None:
        return False
    if last_bar_ts.tzinfo is None:
        last_bar_ts = last_bar_ts.replace(tzinfo=timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    age_s = (now - last_bar_ts).total_seconds()
    return age_s <= staleness_limit_s(bar_period_s)


def last_bar_age_s(last_bar_ts: datetime | None, now: datetime) -> float | None:
    """Seconds since last bar, or None if never received."""
    if last_bar_ts is None:
        return None
    if last_bar_ts.tzinfo is None:
        last_bar_ts = last_bar_ts.replace(tzinfo=timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    return max(0.0, (now - last_bar_ts).total_seconds())
