"""Follow-up analysis (2026-08-26b): H2/H3/H10 -- trade-level MAE-proxy
intraday-honest remeasure.

NOT a true bar-level intraday reconstruction. The real 6J_M15/MNQ_M15 M15
OHLC panels exist in this repo's provenance (core/data/bar_data/SHA256SUMS)
but the bytes are gitignored vendor data and are not present in this
container -- see core/data/bar_data/README.md ("usable but not
regenerable"). A genuine tick/bar-level intraday reconstruction needs those
bytes (or a fresh CME BAR EXPORT) and is handed off as follow-up work
outside this container.

What this script does instead is a disclosed, conservative approximation
using ONLY data already committed to this repo: each trade's own recorded
`mae_usd` (TradingView's own per-trade adverse-excursion figure, already in
data/*_trades.csv). Construction:

  - Per leg, per day: group that leg's trades by exit_date, take the MOST
    NEGATIVE per-contract mae_usd/qty among that day's trades. This handles
    ORB-MNQ's same-day pyramid scale-ins (see `is_scalein` in the 6yr trades
    CSV) without fabricating a "sum of sequential legs' worst moments" story
    the data can't support -- each scale-in's MAE is measured from its own
    entry, and we don't have the intraday timestamps to sequence them.
  - Cross-leg, on days BOTH legs trade: conservative -- sum both legs' own
    (contract-scaled) worst-day MAE, i.e. assume their worst moments COULD
    have coincided (unknown without intraday timestamps). Per the session's
    own mutual-exclusion finding, this touches only ~9-10% of days, so it
    cannot be the dominant source of any resulting delta.
  - Fed into core.mc.simulation.simulate_path's `intraday_low` argument
    (single path) and core.mc.simulation.run_seed's `intraday_blocks`
    argument (bootstrap) -- reused verbatim, the same mechanism ORB-MNQ-1's
    own W1/T2 studies used, just built from a trade-level proxy instead of
    real bars.

Uses the CORRECTED ORB-MNQ series/trades throughout (sliced from the 6-year
export), matching followup_h7_h8_regime.py.
"""
from __future__ import annotations

import csv
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combined_sim as cs  # noqa: E402
from mc.simulation import simulate_path, run_seed, HORIZON_CAP  # noqa: E402
from mc.preflight import firm_kwargs as _firm_kwargs, summarize_outcomes  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
DAILY = os.path.join(DATA, "daily_pnl")

FIRM_KEY = "Tradeify_Select_100K"
CONSISTENCY = 0.40
SEEDS = (1, 2, 3, 4, 5)
N_SIMS = 2000


def load_day_mae(csv_path, date_lo=None, date_hi=None):
    """-> pd.Series indexed by date, worst (most negative) per-contract MAE that day."""
    rows = list(csv.DictReader(open(csv_path)))
    by_day = {}
    for r in rows:
        d = pd.Timestamp(r["exit_date"])
        if date_lo is not None and d < date_lo:
            continue
        if date_hi is not None and d > date_hi:
            continue
        qty = float(r["qty"])
        mae_pc = float(r["mae_usd"]) / qty
        by_day[d] = min(by_day.get(d, 0.0), mae_pc)
    if not by_day:
        raise ValueError(f"{csv_path}: no rows in window")
    s = pd.Series(by_day).sort_index()
    assert (s <= 0.0).all(), "found a positive MAE -- data error"
    return s


def build_intraday_low(mae_series_by_leg, leg_contracts, date_index):
    """Day-level intraday_low aligned to date_index, in COMBINED dollars
    (already contract-scaled), for the sizing used to build the P&L path."""
    n = len(date_index)
    low = np.zeros(n, dtype=float)
    for leg, contracts in leg_contracts.items():
        mae = mae_series_by_leg[leg].reindex(date_index, fill_value=0.0).to_numpy(dtype=float)
        low += mae * contracts
    return np.minimum(low, 0.0)  # simulate_path requires intraday_low <= 0.0


def sweep_flat_and_intraday(label, pnl_by_leg, mae_by_leg, leg_contracts, start, end):
    path, date_index, leg_order = cs.build_combined_path(pnl_by_leg, leg_contracts, start=start, end=end)
    n_days, n_legs = path.shape
    n_weeks = n_days // 5
    usable = n_weeks * 5
    blocks = path[:usable].reshape(n_weeks, 5, n_legs)

    intraday_low = build_intraday_low(mae_by_leg, leg_contracts, date_index)
    intraday_blocks = intraday_low[:usable].reshape(n_weeks, 5, 1)

    fkw = _firm_kwargs(FIRM_KEY, consistency=CONSISTENCY)
    horizon = n_days

    flat_single = simulate_path(path, 1.0, 1.0, horizon, **fkw)
    intraday_single = simulate_path(path, 1.0, 1.0, horizon, intraday_low=intraday_low, **fkw)

    flat_boot = summarize_outcomes(
        [run_seed(s, N_SIMS, blocks, 1.0, 1.0, horizon=HORIZON_CAP, strats=tuple(leg_order), firm_kwargs=fkw) for s in SEEDS], N_SIMS)
    intraday_boot = summarize_outcomes(
        [run_seed(s, N_SIMS, blocks, 1.0, 1.0, horizon=HORIZON_CAP, strats=tuple(leg_order), firm_kwargs=fkw,
                   intraday_blocks=intraday_blocks) for s in SEEDS], N_SIMS)

    return {
        "label": label, "leg_contracts": leg_contracts, "n_days": n_days,
        "flat_single_path": {"outcome": flat_single[0], "day": flat_single[1], "max_dd_pct": round(flat_single[2] * 100, 3)},
        "intraday_single_path": {"outcome": intraday_single[0], "day": intraday_single[1], "max_dd_pct": round(intraday_single[2] * 100, 3)},
        "flat_bootstrap_bust_pct": round(flat_boot["headline_bust"] * 100, 4),
        "intraday_bootstrap_bust_pct": round(intraday_boot["headline_bust"] * 100, 4),
        "worst_intraday_low_day_usd": round(float(intraday_low.min()), 2),
        "n_days_intraday_low_nonzero": int((intraday_low < 0).sum()),
    }


if __name__ == "__main__":
    aegis_1yr_pnl = cs.load_daily_pnl_per_contract(os.path.join(DAILY, "aegis_1yr.json"))
    aegis_3yr_pnl = cs.load_daily_pnl_per_contract(os.path.join(DAILY, "aegis_3yr.json"))
    orbmnq_6yr_pnl = cs.load_daily_pnl_per_contract(os.path.join(DAILY, "orbmnq_6yr.json"))
    orbmnq_1yr_pnl = orbmnq_6yr_pnl.loc[aegis_1yr_pnl.index.min():aegis_1yr_pnl.index.max()]
    orbmnq_3yr_pnl = orbmnq_6yr_pnl.loc[aegis_3yr_pnl.index.min():aegis_3yr_pnl.index.max()]

    aegis_1yr_mae = load_day_mae(os.path.join(DATA, "aegis_1yr_trades.csv"))
    aegis_3yr_mae = load_day_mae(os.path.join(DATA, "aegis_3yr_trades.csv"))
    orbmnq_6yr_mae_full = load_day_mae(os.path.join(DATA, "orbmnq_6yr_trades.csv"))
    orbmnq_1yr_mae = orbmnq_6yr_mae_full.loc[
        (orbmnq_6yr_mae_full.index >= aegis_1yr_pnl.index.min()) & (orbmnq_6yr_mae_full.index <= aegis_1yr_pnl.index.max())]
    orbmnq_3yr_mae = orbmnq_6yr_mae_full.loc[
        (orbmnq_6yr_mae_full.index >= aegis_3yr_pnl.index.min()) & (orbmnq_6yr_mae_full.index <= aegis_3yr_pnl.index.max())]

    results = {}
    results["1yr_flagship"] = sweep_flat_and_intraday(
        "1yr", {"aegis": aegis_1yr_pnl, "orbmnq": orbmnq_1yr_pnl}, {"aegis": aegis_1yr_mae, "orbmnq": orbmnq_1yr_mae},
        {"aegis": 5.333333, "orbmnq": 0.18}, aegis_1yr_pnl.index.min(), aegis_1yr_pnl.index.max())
    results["3yr_flagship"] = sweep_flat_and_intraday(
        "3yr", {"aegis": aegis_3yr_pnl, "orbmnq": orbmnq_3yr_pnl}, {"aegis": aegis_3yr_mae, "orbmnq": orbmnq_3yr_mae},
        {"aegis": 5.333333, "orbmnq": 0.40}, aegis_3yr_pnl.index.min(), aegis_3yr_pnl.index.max())
    results["3yr_H7_sizing"] = sweep_flat_and_intraday(
        "3yr_H7", {"aegis": aegis_3yr_pnl, "orbmnq": orbmnq_3yr_pnl}, {"aegis": aegis_3yr_mae, "orbmnq": orbmnq_3yr_mae},
        {"aegis": 5.333333, "orbmnq": 0.5708}, aegis_3yr_pnl.index.min(), aegis_3yr_pnl.index.max())

    print(json.dumps(results, indent=2))
    with open(os.path.join(DATA, "followup_intraday_mae_proxy_results.json"), "w") as fh:
        json.dump(results, fh, separators=(",", ":"))
