"""DL-1 prereg Sec3 (frozen scoring conventions) + Sec6 step-2 (nomination
gates), TRAIN partition only. SPA is NOT reimplemented here -- delegates to
the repo's vetted primitive `research_utils.universe_gate.run_spa` (arch
SPA/Hansen), per that module's own "do not reimplement" rule. Requires `lab`
on PYTHONPATH for this import.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date as Date

import numpy as np
import pandas as pd

from research_utils.universe_gate import run_spa

from engine import RT_COST, Trade

ANNUALIZATION = np.sqrt(252)  # prereg Sec3 item 1: annualized by sqrt(252)
SPA_BLOCK_SIZE = 20           # prereg Sec6 step 2b: expected block length 20 days
SPA_REPS = 10_000             # prereg Sec6 step 2b: B = 10,000
SPA_SEED = 7                  # prereg Sec6 step 2b: RNG seed 7
SPA_ALPHA = 0.10              # prereg Sec6 step 2b: p <= 0.10
COST_LAW_DESIGN_R = 0.40      # prereg Sec6 step 2a: gross expectancy 0.40R at the design point
COST_LAW_MIN_RATIO = 4.0      # prereg Sec6 step 2a: ratio >= 4x
N_ACT_MIN_PER_WEEK = 1.0      # prereg Sec6 step 2c


def daily_pnl_series(trades: list[Trade], trading_dates: list[Date]) -> pd.Series:
    """Daily net P&L over the CME calendar (trading_dates = every date the
    stitched TRAIN series has bars on), flat days included as zeros --
    prereg Sec3 item 1."""
    by_day: dict[Date, float] = {d: 0.0 for d in trading_dates}
    for t in trades:
        by_day[t.session_date] = by_day.get(t.session_date, 0.0) + t.net_dollars
    idx = sorted(by_day)
    return pd.Series([by_day[d] for d in idx], index=pd.DatetimeIndex(idx))


def net_annsr(daily_pnl: pd.Series) -> float:
    """Sharpe of the daily net P&L series, annualized by sqrt(252) -- prereg
    Sec3 item 1. ddof=1 (sample std); returns 0.0 on a degenerate (zero-
    variance) series rather than inf/nan."""
    sd = daily_pnl.std(ddof=1)
    if not np.isfinite(sd) or sd == 0.0:
        return 0.0
    return float(daily_pnl.mean() / sd * ANNUALIZATION)


def halves_split(daily_pnl: pd.Series, split_date: str) -> tuple[float, float]:
    """Per-half net annSR around a frozen split date (confirm-side use;
    exposed here for reuse, not invoked on TRAIN by this driver)."""
    split = pd.Timestamp(split_date, tz=daily_pnl.index.tz)
    h1 = daily_pnl[daily_pnl.index < split]
    h2 = daily_pnl[daily_pnl.index >= split]
    return net_annsr(h1), net_annsr(h2)


def cadence_per_week(n_trades: int, trading_dates: list[Date]) -> float:
    """prereg Sec6 step 2c (N-ACT): measured trades/week on train, over the
    TRAIN window's calendar span (not the count of active trading days)."""
    if not trading_dates:
        return 0.0
    span_days = (max(trading_dates) - min(trading_dates)).days + 1
    weeks = span_days / 7.0
    return n_trades / weeks if weeks > 0 else 0.0


def cost_law_gate(trades: list[Trade]) -> dict:
    """prereg Sec6 step 2a stop-width sub-check: ratio = 0.40 x
    median_stop_ticks x $1/tick / $4.12 (design-point gross-R yardstick,
    stop width is the realized-train-geometry variable) >= 4x, equivalently
    median stop >= ~41.2 ticks (the prereg's own worked number)."""
    if not trades:
        return {"median_stop_ticks": 0.0, "ratio": 0.0, "passed": False}
    stop_ticks = np.array([t.stop_ticks for t in trades], dtype=float)
    median_stop = float(np.median(stop_ticks))
    ratio = COST_LAW_DESIGN_R * median_stop * 1.0 / RT_COST
    return {"median_stop_ticks": median_stop, "ratio": ratio, "passed": ratio >= COST_LAW_MIN_RATIO}


@dataclass
class VariantResult:
    variant: int
    n_trades: int
    net_annsr: float
    cadence_per_week: float
    cost_law: dict
    daily_pnl: pd.Series


def score_variant(trades: list[Trade], trading_dates: list[Date]) -> VariantResult:
    daily = daily_pnl_series(trades, trading_dates)
    return VariantResult(
        variant=trades[0].variant if trades else -1,
        n_trades=len(trades),
        net_annsr=net_annsr(daily),
        cadence_per_week=cadence_per_week(len(trades), trading_dates),
        cost_law=cost_law_gate(trades),
        daily_pnl=daily,
    )


def spa_universe(daily_pnl_by_variant: dict[int, pd.Series]) -> dict:
    """prereg Sec6 step 2b: SPA (Hansen) consistent p <= 0.10 against the
    full 10-variant universe. benchmark = zero-return series (verbatim);
    block_size=20, reps=10000, seed=7 (pinned, NOT ACF-derived -- this
    overrides universe_gate's own ACF default by passing block_size
    explicitly)."""
    idx = None
    cols = []
    order = sorted(daily_pnl_by_variant)
    for v in order:
        s = daily_pnl_by_variant[v]
        idx = s.index if idx is None else idx.union(s.index)
    aligned = []
    for v in order:
        aligned.append(daily_pnl_by_variant[v].reindex(idx, fill_value=0.0).to_numpy())
    matrix = np.column_stack(aligned)
    benchmark = np.zeros(matrix.shape[0])
    p, better = run_spa(
        benchmark, matrix, block_size=SPA_BLOCK_SIZE,
        better_cutoff=SPA_ALPHA, reps=SPA_REPS, seed=SPA_SEED,
    )
    better_variants = [order[i] for i in better if 0 <= i < len(order)]
    return {"p_value": p, "passed": p <= SPA_ALPHA, "better_variants": better_variants, "order": order}


def m16_slip_gate(trades_at_extra_slip: list[Trade], trading_dates: list[Date]) -> dict:
    """prereg Sec6 step 2d (M-16): nominee's train net annSR stays > 0 at
    +1 tick/side additional slip. Caller re-simulates the nominee with
    engine.simulate_variant(..., extra_slip_ticks=1) and passes the result
    here."""
    daily = daily_pnl_series(trades_at_extra_slip, trading_dates)
    sr = net_annsr(daily)
    return {"net_annsr_plus1tick": sr, "passed": sr > 0.0}
