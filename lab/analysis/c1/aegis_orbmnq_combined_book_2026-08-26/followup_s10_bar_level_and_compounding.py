"""S10 follow-up (2026-08-26c, local session): Task 2 (genuine intraday-honest
remeasure, superseding S9.3's trade-level MAE proxy) and Task 3 (compounding
checks S9 did not run).

Task 2 methodology -- why timestamp-sequencing, not a bar-panel match
----------------------------------------------------------------------
S9.4 asked for a bar-level (M15 OHLC) remeasure. Two paths were evaluated:

  1. Match each trade's own [entry, exit] window against the real 6J_M15/
     MNQ_M15 bar panels and read the excursion off the bars directly.
  2. Use the raw (un-reduced) TradingView "List of Trades" exports -- which,
     unlike the committed derived CSVs, carry each trade's own real ENTRY
     timestamp, not just exit_date -- to sequence trades within a day and
     derive a timestamp-precise (not bar-precise) worst-case equity walk.

Path 1 was attempted first (see recover_6j_bars.py -- 6J's own committed
M15 panel is 51.4% degenerate/flat-bar due to a 5dp-rounding artifact on its
fine mintick; recovered via the documented Price-USD+MFE/MAE method from the
raw BAR_EXPORT harness export, 0% degenerate post-recovery, 0 bracket
violations, median 9-tick range -- externally consistent with this repo's
own independently-measured figure for the same instrument). But a direct
cross-check against Aegis-6J1's OWN reported entry price at a matching
timestamp showed a ~9-tick discrepancy between the two independently-exported
6J feeds (the strategy's own chart feed vs. the synthetic bar-harness feed)
-- comparable in size to this trade's ENTIRE mae_usd (5.5 ticks). Aegis-6J1's
risk profile is tight enough (median trade MAE a handful of ticks) that
cross-feed alignment noise of that size would swamp the signal being
measured. Using the bar panel for tick-level magnitude matching was
therefore rejected as LESS trustworthy than the strategy's own TV-computed
mae_usd, not more.

Path 2 avoids this: it uses only each leg's OWN reported numbers (already
TV-precise, no cross-feed risk) plus real entry/exit TIMESTAMPS (the one
genuinely new ingredient available locally that the original S9.3 proxy
lacked) to correctly sequence and overlap-test trades within a day, instead
of S9.3's coarser "any two trades sharing an exit_date get summed
conservatively" rule. Confirmed first: EVERY Aegis-6J1 and all but 3/1,503
ORB-MNQ-1 trades have entry_date == exit_date (both legs are almost entirely
same-session intraday) -- so the gap this section closes is mostly about
INTRADAY sequencing/overlap. The 3 genuinely multi-day ORB-MNQ trades (2 in
the tested 3yr window) are handled by carrying the trade across every day it
spans, not dismissed as absent (see build_intraday_low_sequenced).

Per-day construction (sweep-line, exact given each trade's own timestamps,
mae and net_pnl, conservative only where timing WITHIN a trade's own hold
is still unknown -- i.e. concurrently-open trades are assumed capable of
hitting their own worst point simultaneously, which real price paths need
not do):
  - Process each day's trades (both legs, contract-scaled to the target
    sizing) as timestamped open/close events; a multi-day trade contributes
    its own MAE to every day it spans, with open/close events only on its
    own entry/exit day.
  - At EVERY event (open OR close), the candidate day floor = (realized P&L
    of all trades ALREADY CLOSED so far that day) + (sum of MAE of every
    trade currently open, INCLUDING the one in this event) -- realized P&L
    from already-closed trades carries forward (a real effect S9.3's "just
    take one MAE" missed: a losing trade earlier in the day lowers the floor
    for a later trade even if their windows never overlap). Checking at
    CLOSE events too (not just opens) catches a trade whose own net_pnl
    realizes worse than its own recorded mae -- TradingView's Adverse
    Excursion field excludes exit-side commission, Net PnL does not,
    observed on 6-11% of trades across both legs; an earlier version of
    this function checked opens only and was caught by adversarial review
    before this section was finalized (understated 8.4% of 3yr days by up
    to $16.53 -- moved no bootstrap figure at 2dp precision, but was a real
    gap, not a cosmetic one).
  - The day's intraday_low = the minimum candidate floor across all the
    day's events (0 if the day has no trades).
  - Consistency check: summed net_pnl over a day's CLOSING trades must equal
    the flat daily_pnl series' own value for that day (verifies this
    script's trade parsing agrees with the already-committed, adversarially
    spot-checked derived data) -- asserted, not just eyeballed.

Reuses combined_sim.py (core/mc/simulation.py::simulate_path/run_seed,
core/mc/preflight.py::firm_kwargs/summarize_outcomes) throughout, exactly as
followup_h7_h8_regime.py and followup_intraday_mae_proxy.py did. Task 3
reuses followup_h7_h8_regime.py's own H7-derived sizing ratios (already
computed, not re-derived) and its own both-halves split dates.
"""
from __future__ import annotations

import csv
import glob
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
DOWNLOADS = r"C:\Users\joshu\Downloads"

FIRM_KEY = "Tradeify_Select_100K"
CONSISTENCY = 0.40
SEEDS = (1, 2, 3, 4, 5)
N_SIMS = 2000

RAW_FILES = {
    "aegis_3yr": os.path.join(DOWNLOADS, "Aegis_6J1_CME_6J1!_2026-08-26_06813.csv"),
    "aegis_1yr": os.path.join(DOWNLOADS, "Aegis_6J1_CME_6J1!_2026-08-26_073cd.csv"),
    "orbmnq_6yr": os.path.join(DOWNLOADS, "ORB-MNQ-1_recon_v2_CME_MINI_MNQ1!_2026-08-26_857de.csv"),
}


# ---------------------------------------------------------------------------
# Raw "List of Trades" loader (Entry+Exit row pairs -> one record per trade)
# ---------------------------------------------------------------------------

def load_raw_trades(path):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    by_trade = {}
    for r in rows:
        tn = r["Trade number"]
        by_trade.setdefault(tn, {})[r["Type"].split()[0]] = r  # "Entry"/"Exit" -> row
    trades = []
    for tn, sides in by_trade.items():
        entry, exit_ = sides.get("Entry"), sides.get("Exit")
        if entry is None or exit_ is None:
            raise ValueError(f"{path} trade {tn}: missing Entry or Exit row")
        qty = float(entry["Size (qty)"])
        entry_time = pd.Timestamp(entry["Date and time"])
        exit_time = pd.Timestamp(exit_["Date and time"])
        net_pnl_pc = float(exit_["Net PnL USD"]) / qty
        mae_pc = float(exit_["Adverse excursion USD"]) / qty
        mfe_pc = float(exit_["Favorable excursion USD"]) / qty
        trades.append({
            "trade_number": tn, "entry_time": entry_time, "exit_time": exit_time,
            "entry_date": pd.Timestamp(entry_time.date()),
            "exit_date": pd.Timestamp(exit_time.date()), "qty": qty,
            "net_pnl_per_contract": net_pnl_pc, "mae_per_contract": mae_pc,
            "mfe_per_contract": mfe_pc,
        })
    trades.sort(key=lambda t: t["entry_time"])
    return trades


def slice_by_window(trades, start, end):
    start, end = pd.Timestamp(start), pd.Timestamp(end)
    return [t for t in trades if start <= t["exit_date"] <= end]


# ---------------------------------------------------------------------------
# Timestamp-sequenced per-day worst-case walk
# ---------------------------------------------------------------------------

def build_intraday_low_sequenced(trades_by_leg, leg_contracts, date_index):
    """-> (intraday_low ndarray aligned to date_index, per-day realized totals
    ndarray for the consistency check, n_sequencing_effect_days).

    Checks the candidate floor at BOTH open AND close events. A trade's own
    net_pnl can be WORSE than its own recorded mae (observed directly on the
    raw exports: 9/90 aegis_3yr, 2/32 aegis_1yr, 168/1503 orbmnq_6yr trades --
    consistent with TradingView's Adverse Excursion field excluding exit-side
    commission while Net PnL includes it), so the floor must be re-checked
    immediately after a trade realizes, not only while it is still open.

    Multi-day trades (entry_date != exit_date -- confirmed rare: 3 of 1,503
    ORB-MNQ-1 trades across the whole 6yr history, 0 Aegis-6J1 trades, 2 of
    the 3 falling inside the tested 3yr window) are carried across every
    calendar day they span: they contribute their own `mae` to each
    intervening day's floor (no event needed that day, since the position is
    already open at that day's start and still open at its end) in addition
    to their own open-day and close-day events.
    """
    day_opens, day_closes, day_carries = {}, {}, {}
    for leg, trades in trades_by_leg.items():
        contracts = leg_contracts[leg]
        for t in trades:
            scaled = dict(t)
            scaled["net_pnl"] = t["net_pnl_per_contract"] * contracts
            scaled["mae"] = t["mae_per_contract"] * contracts
            day_opens.setdefault(t["entry_date"], []).append(scaled)
            day_closes.setdefault(t["exit_date"], []).append(scaled)
            for day in pd.date_range(t["entry_date"], t["exit_date"], freq="D")[1:-1]:
                day_carries.setdefault(day, []).append(scaled)

    all_days = set(day_opens) | set(day_closes) | set(day_carries)
    low_by_day = {}
    realized_by_day = {}
    naive_worst_single_mae_by_day = {}
    for day in all_days:
        opens = day_opens.get(day, [])
        closes = day_closes.get(day, [])
        carries = day_carries.get(day, [])

        events = [(t["entry_time"], 0, id(t), t) for t in opens]
        events += [(t["exit_time"], 1, id(t), t) for t in closes]
        events.sort(key=lambda e: (e[0], e[1]))

        open_trades = {id(t): t for t in carries}
        realized = 0.0
        min_floor = realized + sum(o["mae"] for o in open_trades.values())
        for _time, kind, tid, t in events:
            if kind == 0:
                open_trades[tid] = t
            else:
                realized += t["net_pnl"]
                open_trades.pop(tid, None)
            candidate = realized + sum(o["mae"] for o in open_trades.values())
            min_floor = min(min_floor, candidate)

        low_by_day[day] = min_floor
        # The day's own REALIZED contribution to the flat path is only
        # trades CLOSING that day, matching the already-committed daily_pnl
        # convention (a multi-day trade's whole net_pnl books on exit_date) --
        # carries/opens-not-yet-closed realize nothing today.
        realized_by_day[day] = sum(t["net_pnl"] for t in closes)
        today_trades = opens + closes + carries
        if today_trades:
            naive_worst_single_mae_by_day[day] = min(t["mae"] for t in today_trades)

    n = len(date_index)
    low = np.zeros(n, dtype=float)
    realized_arr = np.zeros(n, dtype=float)
    naive_arr = np.zeros(n, dtype=float)
    for i, day in enumerate(date_index):
        if day in low_by_day:
            low[i] = low_by_day[day]
            realized_arr[i] = realized_by_day[day]
            naive_arr[i] = naive_worst_single_mae_by_day.get(day, 0.0)
    low = np.minimum(low, 0.0)
    n_sequencing_effect_days = int(((low < naive_arr - 1e-6) & (naive_arr < 0)).sum())
    return low, realized_arr, n_sequencing_effect_days


def assert_consistent_with_flat_path(realized_arr, flat_path_sum, label):
    diff = np.abs(realized_arr - flat_path_sum)
    worst = diff.max()
    if worst > 0.02:  # 2 cents, float rounding only
        bad = np.argmax(diff)
        raise AssertionError(
            f"{label}: raw-trade reconstruction disagrees with committed daily_pnl "
            f"by ${worst:.4f} at index {bad} (reconstructed={realized_arr[bad]:.4f}, "
            f"committed={flat_path_sum[bad]:.4f}) -- parsing bug, do not trust output"
        )
    print(f"  [OK] {label}: raw-trade reconstruction matches committed daily_pnl to ${worst:.6f} max diff")


# ---------------------------------------------------------------------------
# Task 2 -- flat vs. timestamp-sequenced intraday-honest sweep
# ---------------------------------------------------------------------------

def sweep_flat_and_intraday_v2(label, pnl_by_leg, trades_by_leg, leg_contracts, start, end):
    path, date_index, leg_order = cs.build_combined_path(pnl_by_leg, leg_contracts, start=start, end=end)
    n_days, n_legs = path.shape
    n_weeks = n_days // 5
    usable = n_weeks * 5
    blocks = path[:usable].reshape(n_weeks, 5, n_legs)

    intraday_low, realized_arr, n_sequencing_effect_days = build_intraday_low_sequenced(trades_by_leg, leg_contracts, date_index)
    flat_sum = path.sum(axis=1)
    assert_consistent_with_flat_path(realized_arr, flat_sum, label)
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
        "n_days_with_overlap_or_sequencing_effect": n_sequencing_effect_days,
    }


# ---------------------------------------------------------------------------
# Task 3 -- compounding checks not run in S9
# ---------------------------------------------------------------------------

def regime_both_halves_intraday(label, pnl_by_leg, trades_by_leg, sizing, start, end, mid):
    """3yr both-halves under H7 sizing + intraday-honesty TOGETHER (Task 3a),
    or 1yr h1/h2 under EITHER correction alone (Task 3b) -- same helper,
    caller passes the sizing/pnl/trades combination it wants tested."""
    def run(s, e):
        path, date_index, leg_order = cs.build_combined_path(pnl_by_leg, sizing, start=s, end=e)
        n_days, n_legs = path.shape
        n_weeks = n_days // 5
        usable = n_weeks * 5
        blocks = path[:usable].reshape(n_weeks, 5, n_legs)
        fkw = _firm_kwargs(FIRM_KEY, consistency=CONSISTENCY)
        if trades_by_leg is None:
            boot = summarize_outcomes(
                [run_seed(sd, N_SIMS, blocks, 1.0, 1.0, horizon=HORIZON_CAP, strats=tuple(leg_order), firm_kwargs=fkw) for sd in SEEDS], N_SIMS)
        else:
            intraday_low, realized_arr, _n_seq = build_intraday_low_sequenced(trades_by_leg, sizing, date_index)
            flat_sum = path.sum(axis=1)
            assert_consistent_with_flat_path(realized_arr, flat_sum, f"{label} [{s}:{e}]")
            intraday_blocks = intraday_low[:usable].reshape(n_weeks, 5, 1)
            boot = summarize_outcomes(
                [run_seed(sd, N_SIMS, blocks, 1.0, 1.0, horizon=HORIZON_CAP, strats=tuple(leg_order), firm_kwargs=fkw,
                           intraday_blocks=intraday_blocks) for sd in SEEDS], N_SIMS)
        return round(boot["headline_bust"] * 100, 4), n_weeks

    full_bust, full_weeks = run(start, end)
    h1_bust, h1_weeks = run(start, mid)
    h2_bust, h2_weeks = run(mid, end)
    return {
        "sizing": sizing,
        "full_window_bust_pct": full_bust, "full_n_weeks": full_weeks,
        "h1_start": str(start), "h1_end": str(mid), "h1_bust_pct": h1_bust, "h1_n_weeks": h1_weeks,
        "h2_start": str(mid), "h2_end": str(end), "h2_bust_pct": h2_bust, "h2_n_weeks": h2_weeks,
        "both_halves_clear_3pct": bool(h1_bust <= 3.0 and h2_bust <= 3.0),
    }


if __name__ == "__main__":
    aegis_1yr_pnl = cs.load_daily_pnl_per_contract(os.path.join(DAILY, "aegis_1yr.json"))
    aegis_3yr_pnl = cs.load_daily_pnl_per_contract(os.path.join(DAILY, "aegis_3yr.json"))
    orbmnq_6yr_pnl = cs.load_daily_pnl_per_contract(os.path.join(DAILY, "orbmnq_6yr.json"))
    orbmnq_1yr_pnl = orbmnq_6yr_pnl.loc[aegis_1yr_pnl.index.min():aegis_1yr_pnl.index.max()]
    orbmnq_3yr_pnl = orbmnq_6yr_pnl.loc[aegis_3yr_pnl.index.min():aegis_3yr_pnl.index.max()]

    aegis_3yr_raw = load_raw_trades(RAW_FILES["aegis_3yr"])
    aegis_1yr_raw = load_raw_trades(RAW_FILES["aegis_1yr"])
    orbmnq_6yr_raw = load_raw_trades(RAW_FILES["orbmnq_6yr"])
    orbmnq_3yr_raw = slice_by_window(orbmnq_6yr_raw, aegis_3yr_pnl.index.min(), aegis_3yr_pnl.index.max())
    orbmnq_1yr_raw = slice_by_window(orbmnq_6yr_raw, aegis_1yr_pnl.index.min(), aegis_1yr_pnl.index.max())

    print(f"aegis_3yr_raw n={len(aegis_3yr_raw)} (committed=90)")
    print(f"aegis_1yr_raw n={len(aegis_1yr_raw)} (committed=32)")
    print(f"orbmnq_3yr_raw (sliced) n={len(orbmnq_3yr_raw)} (committed corrected slice ~ same as followup h7/h8)")
    print(f"orbmnq_1yr_raw (sliced) n={len(orbmnq_1yr_raw)}")

    results = {}

    print("\n=== TASK 2: flat vs. timestamp-sequenced intraday-honest ===")
    results["task2_1yr_flagship"] = sweep_flat_and_intraday_v2(
        "1yr", {"aegis": aegis_1yr_pnl, "orbmnq": orbmnq_1yr_pnl},
        {"aegis": aegis_1yr_raw, "orbmnq": orbmnq_1yr_raw},
        {"aegis": 5.333333, "orbmnq": 0.18}, aegis_1yr_pnl.index.min(), aegis_1yr_pnl.index.max())
    results["task2_3yr_flagship"] = sweep_flat_and_intraday_v2(
        "3yr", {"aegis": aegis_3yr_pnl, "orbmnq": orbmnq_3yr_pnl},
        {"aegis": aegis_3yr_raw, "orbmnq": orbmnq_3yr_raw},
        {"aegis": 5.333333, "orbmnq": 0.40}, aegis_3yr_pnl.index.min(), aegis_3yr_pnl.index.max())
    results["task2_3yr_H7_sizing"] = sweep_flat_and_intraday_v2(
        "3yr_H7", {"aegis": aegis_3yr_pnl, "orbmnq": orbmnq_3yr_pnl},
        {"aegis": aegis_3yr_raw, "orbmnq": orbmnq_3yr_raw},
        {"aegis": 5.333333, "orbmnq": 0.5708}, aegis_3yr_pnl.index.min(), aegis_3yr_pnl.index.max())

    print(json.dumps(results, indent=2, default=str))

    print("\n=== TASK 3a: 3yr both-halves under H7 sizing + intraday-honesty TOGETHER ===")
    mid_3yr = pd.Timestamp("2024-02-28")
    task3a = regime_both_halves_intraday(
        "3yr_H7_plus_intraday", {"aegis": aegis_3yr_pnl, "orbmnq": orbmnq_3yr_pnl},
        {"aegis": aegis_3yr_raw, "orbmnq": orbmnq_3yr_raw},
        {"aegis": 5.333333, "orbmnq": 0.5708}, aegis_3yr_pnl.index.min(), aegis_3yr_pnl.index.max(), mid_3yr)
    print(json.dumps(task3a, indent=2, default=str))

    print("\n=== TASK 3b: 1yr h1/h2 under H7 sizing ALONE (flat/EOD basis) ===")
    mid_1yr = pd.Timestamp("2026-02-13")
    task3b_h7_only = regime_both_halves_intraday(
        "1yr_H7_only", {"aegis": aegis_1yr_pnl, "orbmnq": orbmnq_1yr_pnl}, None,
        {"aegis": 5.333333, "orbmnq": 0.1812}, aegis_1yr_pnl.index.min(), aegis_1yr_pnl.index.max(), mid_1yr)
    print(json.dumps(task3b_h7_only, indent=2, default=str))

    print("\n=== TASK 3b: 1yr h1/h2 under intraday-honesty ALONE (original sizing) ===")
    task3b_intraday_only = regime_both_halves_intraday(
        "1yr_intraday_only", {"aegis": aegis_1yr_pnl, "orbmnq": orbmnq_1yr_pnl},
        {"aegis": aegis_1yr_raw, "orbmnq": orbmnq_1yr_raw},
        {"aegis": 5.333333, "orbmnq": 0.18}, aegis_1yr_pnl.index.min(), aegis_1yr_pnl.index.max(), mid_1yr)
    print(json.dumps(task3b_intraday_only, indent=2, default=str))

    out = {
        "task2": results,
        "task3a_3yr_both_halves_H7_plus_intraday": task3a,
        "task3b_1yr_both_halves_H7_only": task3b_h7_only,
        "task3b_1yr_both_halves_intraday_only": task3b_intraday_only,
    }
    with open(os.path.join(DATA, "followup_s10_bar_level_and_compounding_results.json"), "w") as fh:
        json.dump(out, fh, indent=2, default=str)
    print("\nwrote data/followup_s10_bar_level_and_compounding_results.json")
