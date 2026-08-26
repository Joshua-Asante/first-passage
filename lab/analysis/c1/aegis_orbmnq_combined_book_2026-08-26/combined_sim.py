"""Reusable simulator: does a combined "Aegis 6J1 + ORB-MNQ" book pass a
Tradeify Select 100K futures-prop evaluation?

This module deliberately does NOT reimplement barrier/bust logic. It:

  * reuses ``core/mc/simulation.py``'s ``simulate_path`` (deterministic single-
    path barrier test) and ``run_seed`` (block-bootstrap over weekly blocks)
    verbatim, via ``sys.path`` import exactly as the task specifies;
  * reuses ``core/mc/preflight.py``'s ``firm_kwargs`` (turns a
    ``core/firm_rules.FIRM_RULES`` tier into ``simulate_path`` kwargs,
    None-safely) and ``summarize_outcomes`` (aggregates ``run_seed`` results
    with the F1 bucket-sum assertion) verbatim;
  * ports, as a faithful *parallel* implementation (not a reuse -- required
    because ``simulate_path`` only accepts a fixed, pre-sized path and cannot
    itself re-size contracts day-by-day), the cushion-proportional dynamic
    sizing formula already tested in
    ``lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20/
    run_evalseq_orb_intraday.py`` (function ``pol_cushion``), extended from a
    single leg to the combined 2-leg book.

The ``replay_cushion`` day-loop mirrors ``simulate_path``'s loop body
statement-for-statement (same variable names, same order of operations:
compute this-day's DD-throttle scale from *last* day's peak/equity, apply it,
test the barrier against the *pre-update* peak/floor, THEN advance
equity/peak/trade_days/max_day_profit, THEN test the profit-target +
min-trading-days + consistency exit) -- the only two differences are (a) the
per-leg dollar P&L for the day is built from ``base_leg_contracts * that
day's cushion multiplier`` instead of being read off a fixed path, and (b)
the floor/profit-target constants come from ``firm_kwargs`` instead of being
hardcoded.

Live-book posture (see repo CLAUDE.md): this is exploratory research tooling
only. Aegis 6J1 and ORB-MNQ are NOT the c1 book (Striker legs only, barred
since 2026-08-04); nothing here places or authorizes a trade.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

# Portable path fix (2026-08-26, on landing this module in-repo): the
# original scratchpad session hardcoded this session's own absolute
# container path. Resolved relative to this file's own location instead
# (lab/analysis/c1/<slug>/combined_sim.py -> repo_root/core), so it runs
# unmodified from a fresh clone.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "core"))

from mc.simulation import HORIZON_CAP, run_seed, simulate_path  # noqa: E402
from mc.preflight import firm_kwargs as _firm_kwargs, summarize_outcomes  # noqa: E402
from firm_rules import FIRM_RULES  # noqa: E402

__all__ = [
    "load_daily_pnl_per_contract",
    "build_combined_path",
    "replay_flat",
    "replay_cushion",
    "bootstrap_block_sweep",
]


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_daily_pnl_per_contract(json_path: str) -> pd.Series:
    """Load one daily_pnl JSON (list of {"date": "YYYY-MM-DD",
    "pnl_per_contract": float}) into a pandas Series indexed by date
    (DatetimeIndex, sorted, no duplicate dates), float $/contract/day.

    Matches the on-disk schema produced upstream at
    scratchpad/combined_book/daily_pnl/{aegis_1yr,aegis_3yr,orbmnq_1yr,
    orbmnq_3yr}.json (bdate_range-indexed, 0.0 on no-exit business days,
    summed pnl_per_contract on exit business days).
    """
    with open(json_path, "r") as fh:
        records = json.load(fh)
    if not records:
        raise ValueError(f"{json_path}: empty daily_pnl JSON")
    dates = pd.to_datetime([r["date"] for r in records])
    values = np.asarray([float(r["pnl_per_contract"]) for r in records], dtype=float)
    series = pd.Series(values, index=dates, dtype=float).sort_index()
    if series.index.has_duplicates:
        # Upstream schema promises one row per business day; fail loudly
        # rather than silently summing/overwriting if that promise breaks.
        dupes = series.index[series.index.duplicated()].unique()
        raise ValueError(f"{json_path}: duplicate dates in daily_pnl JSON: {list(dupes)}")
    series.name = "pnl_per_contract"
    return series


# ---------------------------------------------------------------------------
# Path assembly
# ---------------------------------------------------------------------------

def build_combined_path(
    leg_series: Dict[str, pd.Series],
    leg_contracts: Dict[str, float],
    start: Optional[str] = None,
    end: Optional[str] = None,
) -> Tuple[np.ndarray, pd.DatetimeIndex, List[str]]:
    """Align named legs on a shared business-day index and scale each by its
    target contract count.

    Parameters
    ----------
    leg_series : {leg_name: per-contract daily $ Series}, e.g. as returned by
        ``load_daily_pnl_per_contract``.
    leg_contracts : {leg_name: target contract count}. Must have the same
        keys as ``leg_series`` (checked).
    start, end : optional date bounds (anything ``pd.Timestamp`` accepts).
        Default to the union of the legs' own [min, max] date range when
        omitted, so a caller can pass either explicit overlap-window bounds
        (per the Parse-phase overlap_1yr / overlap_3yr windows) or nothing.

    Returns
    -------
    (path, date_index, leg_name_order)
      path : np.ndarray, shape (n_days, n_legs), dollar P&L per leg per day
             (leg_series[name] * leg_contracts[name]), 0.0 on days a leg has
             no row in its own series (no trade that day, or day outside
             that leg's own backtest window).
      date_index : the shared pd.DatetimeIndex (business days, start..end).
      leg_name_order : list[str], the column order of ``path`` -- the
             insertion order of ``leg_series`` (stable, since Python dicts
             preserve insertion order).
    """
    missing = set(leg_series) ^ set(leg_contracts)
    if missing:
        raise KeyError(
            f"leg_series and leg_contracts must share the same keys; "
            f"symmetric difference = {sorted(missing)}"
        )
    leg_name_order = list(leg_series.keys())

    if start is None:
        start = min(s.index.min() for s in leg_series.values())
    if end is None:
        end = max(s.index.max() for s in leg_series.values())
    date_index = pd.bdate_range(start=start, end=end)

    n_days = len(date_index)
    n_legs = len(leg_name_order)
    path = np.zeros((n_days, n_legs), dtype=float)
    for col, name in enumerate(leg_name_order):
        aligned = leg_series[name].reindex(date_index, fill_value=0.0)
        path[:, col] = aligned.to_numpy(dtype=float) * float(leg_contracts[name])

    return path, date_index, leg_name_order


# ---------------------------------------------------------------------------
# Flat (constant-contract) replay -- pure reuse of simulate_path
# ---------------------------------------------------------------------------

def replay_flat(
    path_array: np.ndarray,
    firm_key: str = "Tradeify_Select_100K",
    consistency: Optional[float] = 0.40,
    dd_trigger: float = 1.0,
    dd_scale: float = 1.0,
    leg_names: Optional[Sequence[str]] = None,
) -> dict:
    """Replay a fixed (already contract-sized) combined path through the
    repo's own ``simulate_path`` barrier engine, with constant sizing
    throughout (no cushion adjustment).

    ``dd_trigger=1.0, dd_scale=1.0`` (the defaults) disable this repo's
    separate 1.5%/0.40x portfolio DD-throttle -- per task framing that
    throttle was calibrated for a different, older locked 4-strategy book
    and is only an optional exploratory sensitivity for this new candidate
    book, not authoritative for it. A 100% DD threshold can never be
    reached, so it is a true no-op at these defaults.

    ``leg_names`` is optional: when supplied (e.g. the ``leg_name_order``
    ``build_combined_path`` returned), ``culprit_leg`` resolves to the leg's
    name instead of its raw column index.

    Returns
    -------
    dict with keys: outcome, day, max_dd_pct, max_dd_usd, culprit_leg.
    ``max_dd_pct``/``max_dd_usd`` read simulate_path's own ``max_dd`` return
    (a peak-relative fraction, EOD-denominated); ``max_dd_usd`` multiplies
    that fraction by the tier's starting_equity as a readable dollar
    approximation -- NOT peak-exact when the running peak has drifted from
    starting_equity (see the aegis_3yr max-DD-% artifact note in this
    project's Parse-phase output for why peak-relative and equity-relative
    percentages can diverge).
    """
    path_array = np.asarray(path_array, dtype=float)
    horizon = path_array.shape[0]
    kwargs = _firm_kwargs(firm_key, consistency=consistency)
    starting_equity = kwargs["starting_equity"]

    outcome, day, max_dd, culprit = simulate_path(
        path_array, dd_trigger, dd_scale, horizon, **kwargs
    )

    culprit_leg = None
    if culprit is not None:
        culprit_leg = leg_names[culprit] if leg_names is not None else culprit

    return {
        "outcome": outcome,
        "day": day,
        "max_dd_pct": max_dd * 100.0,
        "max_dd_usd": max_dd * starting_equity,
        "culprit_leg": culprit_leg,
    }


# ---------------------------------------------------------------------------
# Cushion-proportional replay -- faithful parallel day-loop
# ---------------------------------------------------------------------------

def replay_cushion(
    leg_series: Dict[str, pd.Series],
    base_leg_contracts: Dict[str, float],
    firm_key: str = "Tradeify_Select_100K",
    consistency: Optional[float] = 0.40,
    start: Optional[str] = None,
    end: Optional[str] = None,
    dd_trigger: float = 1.0,
    dd_scale: float = 1.0,
) -> dict:
    """Day-by-day cushion-proportional sizing replay of the combined book.

    At each day, computes the multiplier from the CURRENT combined
    balance/peak (exactly the formula tested and found effective at
    eliminating ORB-MNQ-1-solo busts in
    ``lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20/
    run_evalseq_orb_intraday.py::pol_cushion``, ported from one leg to
    ``len(leg_series)`` legs):

        cushion    = bal - (peak - DD)
        multiplier = 0.75 * min(1.0, max(cushion, 0.0) / DD)

    where DD is the firm's dollar drawdown allowance
    (``-trailing_dd_pct * starting_equity`` from ``firm_kwargs`` --
    $3,000 for Tradeify_Select_100K). The SAME multiplier is applied to
    every leg's ``base_leg_contracts`` that day before that day's per-leg
    dollar P&L is computed from ``leg_series``.

    Everything downstream of that per-day contract count -- the DD-throttle
    scale, the trailing_locking floor test
    (``floor = min(peak - max_dd_usd, starting_equity + dd_lock_offset_usd)``),
    the daily-loss test, the inactivity counter, and the profit_target +
    min_trading_days + consistency_frac exit -- is a faithful, line-by-line
    parallel of ``simulate_path``'s own loop body (core/mc/simulation.py),
    read in full before writing this function per this repo's Rule 0. This
    duplication is necessary, not a shortcut: ``simulate_path`` only accepts
    a fixed path and has no notion of a per-day-reweighable position size.

    Returns
    -------
    dict with keys: outcome, day, max_dd_pct, max_dd_usd, culprit_leg.
    Same outcome vocabulary as ``simulate_path``:
    {'pass','bust_daily','bust_static','bust_trailing','bust_inactivity',
    'horizon_cap'}. Tradeify_Select_100K is dd_type='trailing_locking', so
    in practice only 'bust_trailing' (or 'bust_inactivity'/'pass'/
    'horizon_cap') will occur -- 'bust_static' is unreachable here (its check
    lives on a different dd_type branch) and is asserted unreachable.
    """
    missing = set(leg_series) ^ set(base_leg_contracts)
    if missing:
        raise KeyError(
            f"leg_series and base_leg_contracts must share the same keys; "
            f"symmetric difference = {sorted(missing)}"
        )

    # Reuse build_combined_path for the alignment step (per-contract, i.e.
    # contracts=1.0 for every leg) so the date-index / fill-with-0.0 /
    # column-order logic is not duplicated.
    percontract_path, date_index, leg_order = build_combined_path(
        leg_series, {name: 1.0 for name in leg_series}, start=start, end=end
    )
    base_contracts_vec = np.asarray(
        [float(base_leg_contracts[name]) for name in leg_order], dtype=float
    )
    horizon = percontract_path.shape[0]

    kwargs = _firm_kwargs(firm_key, consistency=consistency)
    starting_equity = float(kwargs["starting_equity"])
    daily_loss_pct = kwargs["daily_loss_pct"]
    dd_type = kwargs["dd_type"]
    if dd_type != "trailing_locking":
        raise ValueError(
            f"replay_cushion is written against dd_type='trailing_locking' "
            f"(Tradeify's fixed-$ EOD trail); {firm_key!r} has dd_type="
            f"{dd_type!r}. Extend this function before using it on that tier."
        )
    trailing_dd_pct = kwargs["trailing_dd_pct"]
    dd_lock_offset_usd = kwargs["dd_lock_offset_usd"]
    profit_target = float(kwargs["profit_target"])
    min_trading_days = int(kwargs["min_trading_days"])
    inactivity_limit = int(kwargs["inactivity_limit"])
    consistency_frac = kwargs["consistency_frac"]

    max_dd_usd_allow = -trailing_dd_pct * starting_equity  # e.g. $3,000

    equity = peak = starting_equity
    trade_days = 0
    consecutive_idle = 0
    max_dd = 0.0
    max_day_profit = 0.0

    outcome = "horizon_cap"
    result_day = horizon
    culprit = None

    for day in range(horizon):
        # --- this repo's own separate DD-throttle (off by default: dd_trigger=1.0) ---
        dd_from_peak = (equity - peak) / peak if peak > 0 else 0.0
        throttle = dd_scale if round(dd_from_peak, 6) <= -dd_trigger else 1.0

        # --- cushion-proportional contract sizing, from *start-of-day* bal/peak ---
        cushion = equity - (peak - max_dd_usd_allow)
        multiplier = 0.75 * min(1.0, max(cushion, 0.0) / max_dd_usd_allow)
        contracts_today = base_contracts_vec * multiplier

        strategy_pnls = percontract_path[day] * contracts_today * throttle
        pnl = float(strategy_pnls.sum())
        equity_new = equity + pnl

        dd_new = (peak - equity_new) / peak if peak > 0 else 0.0
        if dd_new > max_dd:
            max_dd = dd_new

        equity_test = equity_new  # no intraday-low series available here

        if (
            daily_loss_pct is not None
            and round(pnl / starting_equity, 6) <= daily_loss_pct
        ):
            outcome, result_day = "bust_daily", day + 1
            culprit = leg_order[int(np.argmin(strategy_pnls))]
            break

        floor = min(peak - max_dd_usd_allow, starting_equity + dd_lock_offset_usd)
        if round((equity_test - floor) / starting_equity, 6) <= 0.0:
            outcome, result_day = "bust_trailing", day + 1
            culprit = leg_order[int(np.argmin(strategy_pnls))]
            break

        had_activity = bool(np.any(strategy_pnls != 0.0))
        if not had_activity:
            consecutive_idle += 1
        else:
            consecutive_idle = 0
        if consecutive_idle >= inactivity_limit:
            outcome, result_day = "bust_inactivity", day + 1
            culprit = None
            break

        equity = equity_new
        if equity > peak:
            peak = equity
        if had_activity:
            trade_days += 1
        if pnl > max_day_profit:
            max_day_profit = pnl

        if round(equity, 2) >= profit_target and trade_days >= min_trading_days:
            if consistency_frac is None:
                outcome, result_day = "pass", day + 1
                break
            total_profit = equity - starting_equity
            if (
                total_profit <= 0.0
                or round(max_day_profit - consistency_frac * total_profit, 2) <= 0.0
            ):
                outcome, result_day = "pass", day + 1
                break

    return {
        "outcome": outcome,
        "day": result_day,
        "max_dd_pct": max_dd * 100.0,
        "max_dd_usd": max_dd * starting_equity,
        "culprit_leg": culprit,
    }


# ---------------------------------------------------------------------------
# Block-bootstrap sweep -- pure reuse of run_seed + summarize_outcomes
# ---------------------------------------------------------------------------

def bootstrap_block_sweep(
    leg_series: Dict[str, pd.Series],
    leg_contracts: Dict[str, float],
    firm_key: str = "Tradeify_Select_100K",
    consistency: Optional[float] = 0.40,
    n_sims: int = 2000,
    seeds: Sequence[int] = (1, 2, 3, 4, 5),
    start: Optional[str] = None,
    end: Optional[str] = None,
    dd_trigger: float = 1.0,
    dd_scale: float = 1.0,
    horizon: int = HORIZON_CAP,
) -> dict:
    """Aggregate pass/bust rates for the flat (constant-contract) combined
    book via the engine's OWN block-bootstrap (``run_seed``, 5-day/weekly
    blocks) and OWN aggregator (``summarize_outcomes`` -- reused verbatim,
    not hand-rolled).

    ``seeds`` must be the fixed ints given (never a wall-clock-derived seed)
    for reproducibility, per task instruction.

    Returns the dict ``summarize_outcomes`` returns (rates per outcome
    bucket, headline_bust = mean(bust_daily+bust_static+bust_trailing),
    pass_rate, n_seeds, sims_per_seed), augmented with ``leg_order`` and
    ``n_weeks_available`` (how many whole 5-day blocks the aligned history
    supplied -- the block-bootstrap resamples *from* these, WITH
    replacement, out to ``horizon`` days per simulated path, so this is a
    data-richness diagnostic, not a cap on the simulated horizon).
    """
    path, date_index, leg_order = build_combined_path(
        leg_series, leg_contracts, start=start, end=end
    )
    n_days, n_legs = path.shape
    n_weeks = n_days // 5
    if n_weeks < 1:
        raise ValueError(
            f"combined path only has {n_days} aligned business day(s); need "
            f"at least 5 (one weekly block) for the block-bootstrap."
        )
    usable_days = n_weeks * 5
    blocks = path[:usable_days].reshape(n_weeks, 5, n_legs)

    fkw = _firm_kwargs(firm_key, consistency=consistency)

    seeds_results = [
        run_seed(
            seed,
            n_sims,
            blocks,
            dd_trigger,
            dd_scale,
            horizon=horizon,
            strats=tuple(leg_order),
            firm_kwargs=fkw,
        )
        for seed in seeds
    ]
    summary = summarize_outcomes(seeds_results, n_sims)
    summary["leg_order"] = leg_order
    summary["n_weeks_available"] = n_weeks
    return summary
