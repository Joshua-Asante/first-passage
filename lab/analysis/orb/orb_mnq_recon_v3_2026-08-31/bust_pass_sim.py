"""Bust/pass rope walk for orb_mnq_recon_v3.pine at Tradeify_Select_100K,
reusing core/mc/simulation.py verbatim (same engine, same firm_kwargs
convention as the 2026-08-03 T2 payability measurement and the
2026-08-26 combined-book study).

k grid {1,2,3} matches the T2 ADR's own admissible-contract sweep
(docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md Sec 4).
Consistency=0.40 (Run-2, Tradeify's real consistency rule) is the
deployable-expression reading the live pre-registration (v2) scores against;
Run-1 (consistency=None) reported alongside for continuity with anything
that quoted Run-1 numbers historically.

EOD-clock reading uses daily_pnl.json alone (closed-trade net PnL per day --
a lower bound per this repo's own standing posture, since it cannot see an
intraday breach that recovers by the close). Intraday-honest reading adds
daily_mae.json via simulate_path's intraday_low -- a disclosed trade-level
MAE proxy (see reduce_trades.py docstring), not a true bar-level
reconstruction.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
import pandas as pd

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "core"))

from mc.simulation import HORIZON_CAP, run_seed, simulate_path  # noqa: E402
from mc.preflight import firm_kwargs as _firm_kwargs, summarize_outcomes  # noqa: E402

FIRM_KEY = "Tradeify_Select_100K"
K_GRID = (1, 2, 3)
SEEDS = (1, 2, 3)
N_SIMS = 10_000  # matches the T2 ADR's own "10,000 sims/seed x 3 seeds"
CEILING_LIVE = 5.0   # prereg v2 Sec 3, live since 2026-08-26
CEILING_ORIGINAL = 3.0  # prereg v1, historical -- ADR table used this
PASS_FLOOR = 50.0


def load_series(path: str, value_key: str) -> pd.Series:
    with open(path) as fh:
        records = json.load(fh)
    dates = pd.to_datetime([r["date"] for r in records])
    values = np.asarray([float(r[value_key]) for r in records], dtype=float)
    return pd.Series(values, index=dates).sort_index()


def build_path(pnl: pd.Series, mae: pd.Series, k: int):
    date_index = pd.bdate_range(start=pnl.index.min(), end=pnl.index.max())
    pnl_aligned = pnl.reindex(date_index, fill_value=0.0).to_numpy(dtype=float) * k
    mae_aligned = mae.reindex(date_index, fill_value=0.0).to_numpy(dtype=float) * k
    mae_aligned = np.minimum(mae_aligned, 0.0)
    path = pnl_aligned.reshape(-1, 1)
    return path, mae_aligned, date_index


def sweep(pnl: pd.Series, mae: pd.Series, consistency, label: str) -> dict:
    fkw = _firm_kwargs(FIRM_KEY, consistency=consistency)
    out = {}
    for k in K_GRID:
        path, intraday_low, date_index = build_path(pnl, mae, k)
        n_days = path.shape[0]
        n_weeks = n_days // 5
        usable = n_weeks * 5
        blocks = path[:usable].reshape(n_weeks, 5, 1)
        intraday_blocks = intraday_low[:usable].reshape(n_weeks, 5, 1)

        eod_single = simulate_path(path, 1.0, 1.0, n_days, **fkw)
        intraday_single = simulate_path(path, 1.0, 1.0, n_days, intraday_low=intraday_low, **fkw)

        eod_boot = summarize_outcomes(
            [run_seed(s, N_SIMS, blocks, 1.0, 1.0, horizon=HORIZON_CAP, firm_kwargs=fkw) for s in SEEDS],
            N_SIMS)
        intraday_boot = summarize_outcomes(
            [run_seed(s, N_SIMS, blocks, 1.0, 1.0, horizon=HORIZON_CAP, firm_kwargs=fkw,
                       intraday_blocks=intraday_blocks) for s in SEEDS],
            N_SIMS)

        out[f"k={k}"] = {
            "n_days_realized_panel": int(n_days),
            "realized_path": {
                "eod_clock": {"outcome": eod_single[0], "day": eod_single[1], "max_dd_pct": round(eod_single[2] * 100, 3)},
                "intraday_honest": {"outcome": intraday_single[0], "day": intraday_single[1], "max_dd_pct": round(intraday_single[2] * 100, 3)},
            },
            "bootstrap_bust_pct": {
                "eod_clock": round(eod_boot["headline_bust"] * 100, 3),
                "intraday_honest": round(intraday_boot["headline_bust"] * 100, 3),
            },
            "bootstrap_pass_pct": {
                "eod_clock": round(eod_boot["pass_rate"] * 100, 3),
                "intraday_honest": round(intraday_boot["pass_rate"] * 100, 3),
            },
        }
    return {"label": label, "consistency": consistency, "k_results": out}


def main() -> None:
    pnl = load_series("data/daily_pnl.json", "pnl_per_contract")
    mae = load_series("data/daily_mae.json", "mae_per_contract")

    results = {
        "run2_consistency_040": sweep(pnl, mae, 0.40, "Run-2 (consistency=0.40, deployable expression)"),
        "run1_consistency_off": sweep(pnl, mae, None, "Run-1 (consistency off, historical continuity)"),
    }

    print(json.dumps(results, indent=2))
    with open("data/bust_pass_sim_results.json", "w") as fh:
        json.dump(results, fh, indent=2)

    print("\n=== headline (Run-2, intraday-honest bootstrap bust %, vs ceilings) ===")
    for k in K_GRID:
        r = results["run2_consistency_040"]["k_results"][f"k={k}"]
        bust = r["bootstrap_bust_pct"]["intraday_honest"]
        passp = r["bootstrap_pass_pct"]["intraday_honest"]
        print(f"k={k}: bust={bust}%  (live ceiling {CEILING_LIVE}%, original {CEILING_ORIGINAL}%)  "
              f"pass={passp}%  (floor {PASS_FLOOR}%)  "
              f"-> {'CLEARS' if bust <= CEILING_LIVE and passp >= PASS_FLOOR else 'FAILS'} live gate")


if __name__ == "__main__":
    main()
