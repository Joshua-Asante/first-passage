"""H4 (2026-08-26d, local session): native TradingView re-export at exactly 4
Aegis-6J1 contracts -- the one item that remained open after S10.

Operator-supplied `Aegis_6J1_CME_6J1!_2026-08-26_c59e9.csv`: a genuine flat
max_contracts=4 backtest (every trade's own Size (qty)==4, not the variable
4-8 cap-8-style sizing behind the committed data), 2020-02-24 -> 2026-08-05,
154 trades.

Sliced to the SAME 3yr window used throughout this campaign
(2022-09-07 -> 2025-08-20) and run through the identical bootstrap
methodology that produced the original 2.77% linear-rescale figure
(data/aegis_solo_supplementary_bootstrap.json "c4": n_sims=2000, seeds
1-5, weekly blocks, Tradeify_Select_100K, consistency=0.40, solo Aegis
leg only) -- reused verbatim via combined_sim.bootstrap_block_sweep, no
barrier logic reimplemented. The only difference from that prior run:
the trade data itself is a native 4-contract export, not a linear rescale
of the 8-contract backtest.
"""
from __future__ import annotations

import csv
import json
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combined_sim as cs  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
RAW_PATH = r"C:\Users\joshu\Downloads\Aegis_6J1_CME_6J1!_2026-08-26_c59e9.csv"

FIRM_KEY = "Tradeify_Select_100K"
CONSISTENCY = 0.40
SEEDS = (1, 2, 3, 4, 5)
N_SIMS = 2000

WINDOW_3YR_START = pd.Timestamp("2022-09-07")
WINDOW_3YR_END = pd.Timestamp("2025-08-20")


def load_native_daily_series(path):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    exits = [r for r in rows if r["Type"].startswith("Exit")]
    qtys = set(r["Size (qty)"] for r in exits)
    if qtys != {"4"}:
        raise ValueError(f"expected a flat qty=4 export, got qty values {qtys}")
    by_day = {}
    for r in exits:
        day = pd.Timestamp(pd.Timestamp(r["Date and time"]).date())
        by_day[day] = by_day.get(day, 0.0) + float(r["Net PnL USD"])
    dates = pd.to_datetime(sorted(by_day))
    series = pd.Series([by_day[d] for d in dates], index=dates, dtype=float).sort_index()
    series.name = "native_4contract_pnl"
    return series


if __name__ == "__main__":
    full_series = load_native_daily_series(RAW_PATH)
    print(f"full native export: {len(full_series)} trading days, "
          f"{full_series.index.min().date()} -> {full_series.index.max().date()}")

    window_series = full_series.loc[WINDOW_3YR_START:WINDOW_3YR_END]
    print(f"sliced to campaign 3yr window: {len(window_series)} trading days with a trade, "
          f"{window_series.index.min().date()} -> {window_series.index.max().date()}")

    sweep = cs.bootstrap_block_sweep(
        {"aegis": window_series}, {"aegis": 1.0},
        firm_key=FIRM_KEY, consistency=CONSISTENCY, n_sims=N_SIMS, seeds=SEEDS,
        start=WINDOW_3YR_START, end=WINDOW_3YR_END,
    )
    single = cs.replay_flat(
        cs.build_combined_path({"aegis": window_series}, {"aegis": 1.0},
                                start=WINDOW_3YR_START, end=WINDOW_3YR_END)[0],
        firm_key=FIRM_KEY, consistency=CONSISTENCY,
    )

    original_linear_rescale_bust_pct = 2.77  # data/aegis_solo_supplementary_bootstrap.json "c4"
    native_bust_pct = round(sweep["headline_bust"] * 100, 4)

    result = {
        "source_file": RAW_PATH,
        "n_trading_days_full_export": len(full_series),
        "n_trading_days_in_window": len(window_series),
        "window_start": str(WINDOW_3YR_START), "window_end": str(WINDOW_3YR_END),
        "n_weeks_available": sweep["n_weeks_available"],
        "single_path": {"outcome": single["outcome"], "day": single["day"], "max_dd_pct": single["max_dd_pct"]},
        "native_4contract_bootstrap_bust_pct": native_bust_pct,
        "native_4contract_pass_rate_pct": round(sweep["pass_rate"] * 100, 4),
        "original_linear_rescale_bust_pct": original_linear_rescale_bust_pct,
        "delta_pp_native_minus_linear": round(native_bust_pct - original_linear_rescale_bust_pct, 4),
        "ceiling_pct": 3.0,
        "margin_pp_vs_ceiling": round(3.0 - native_bust_pct, 4),
        "clears_3pct_ceiling": bool(native_bust_pct <= 3.0),
    }
    print(json.dumps(result, indent=2, default=str))
    with open(os.path.join(DATA, "followup_h4_native_4contract_results.json"), "w") as fh:
        json.dump(result, fh, indent=2, default=str)
    print("\nwrote data/followup_h4_native_4contract_results.json")
