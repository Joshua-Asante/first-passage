#!/usr/bin/env python3
"""Standalone idle-clock (M-B) monitor logic for Q-MONSURF-1.

Frozen semantics per docs/briefs/pre-registration/Q-MONSURF-1-verdict-preregistration.md §3-5.
Deliberately has NO import of ops/c1_rail/c1_rail_telemetry.py or any live EventLedger schema
(parent brief §5 forbidden move) -- this module is wired to the live account only at Phase 5,
after F3 registers a successor venue. Input here is a plain list of per-day activity booleans;
the eventual Phase-5 adapter is responsible for turning live fills into that same shape.
"""

from dataclasses import dataclass, field


@dataclass
class DayAlert:
    week_index: int
    day_position: int  # 1-indexed within the week
    kind: str  # "T-2" or "T-1"


@dataclass
class WeekResult:
    week_index: int
    n_days: int
    active_days: list  # 1-indexed positions with activity
    alerts: list = field(default_factory=list)
    breached: bool = False


def _default_lookback(day_active_flags: list, position: int) -> bool:
    """True iff any day strictly before `position` (1-indexed) was active. The frozen,
    no-look-ahead rule (pre-reg §4)."""
    return any(day_active_flags[: position - 1])


def evaluate_week(week_index: int, day_active_flags: list, lookback=_default_lookback) -> WeekResult:
    """Evaluate one week's T-2/T-1 alerts against its own day_active_flags.

    day_active_flags: list of bool, one per business day in the week, in order.
    `lookback` is injectable so the acceptance battery can plant a defective lookback rule
    and confirm the scoring catches it (mutation testing), without touching the frozen
    day_active_flags input itself.
    """
    n = len(day_active_flags)
    active_days = [i + 1 for i, flag in enumerate(day_active_flags) if flag]
    result = WeekResult(week_index=week_index, n_days=n, active_days=active_days)

    if n >= 2:
        t2_position = n - 1
        if not lookback(day_active_flags, t2_position):
            result.alerts.append(DayAlert(week_index, t2_position, "T-2"))

    if n >= 1:
        t1_position = n
        if not lookback(day_active_flags, t1_position):
            result.alerts.append(DayAlert(week_index, t1_position, "T-1"))

    result.breached = len(active_days) == 0
    return result


def evaluate_panel(weeks: list, lookback=_default_lookback) -> list:
    """weeks: list of list[bool] (one inner list per week, chronological). Returns list[WeekResult]."""
    return [evaluate_week(i, week, lookback=lookback) for i, week in enumerate(weeks)]


def score_battery(results: list) -> dict:
    """Apply the frozen missed/spurious definitions (pre-reg §5) against evaluated weeks."""
    missed = []
    spurious = []

    for r in results:
        if r.breached:
            kinds_fired = {a.kind for a in r.alerts}
            if r.n_days >= 2 and "T-2" not in kinds_fired:
                missed.append((r.week_index, "T-2"))
            if r.n_days >= 1 and "T-1" not in kinds_fired:
                missed.append((r.week_index, "T-1"))

        for a in r.alerts:
            active_before = any(pos <= a.day_position - 1 for pos in r.active_days)
            if active_before:
                spurious.append((r.week_index, a.kind, a.day_position, r.active_days))

    return {
        "n_weeks": len(results),
        "n_breached": sum(1 for r in results if r.breached),
        "n_missed": len(missed),
        "missed": missed,
        "n_spurious": len(spurious),
        "spurious": spurious,
        "pass": (len(missed) == 0 and len(spurious) == 0),
    }
