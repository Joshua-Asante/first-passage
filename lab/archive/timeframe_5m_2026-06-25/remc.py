"""Descriptive portfolio re-MC for the 5m prototypes. Reuses the core MC kernel
(build_daily_panel / build_week_blocks / _run_seeds) but loads trades with a
window-RELAXED loader: the canonical load_trades enforces a ~4yr window that a
short 5m export cannot satisfy. The achieved window + any implied_1r fallback
are returned for disclosure. NOT a lock gate."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd

import portfolio_mc as pmc
import io_tv

def to_mc_trades(exits: pd.DataFrame) -> pd.DataFrame:
    """Map io_tv.load_exits output to the load_trades shape build_daily_panel
    expects: ['exit_date','pnl'] using the as-reported $ column (the MC kernel
    re-normalizes per-strategy via implied_1r internally)."""
    return pd.DataFrame({
        "exit_date": pd.to_datetime(exits["exit_date"]),
        "pnl": exits["net_pnl_usd"].astype(float),
    }).sort_values("exit_date").reset_index(drop=True)

def aggregate(seeds_results: list) -> dict:
    per = pmc.SIMS_PER_SEED
    pass_r = [r["outcomes"]["pass"] / per for r in seeds_results]
    bust_r = [(r["outcomes"]["bust_daily"] + r["outcomes"]["bust_static"]) / per
              for r in seeds_results]
    dds = [d for r in seeds_results for d in r["max_dds"]]
    return {
        "pass_rate": float(np.mean(pass_r)),
        "bust_rate": float(np.mean(bust_r)),
        "p99_dd": float(np.percentile(dds, 99)),
    }

def run_5m_remc(proto_csvs: dict) -> dict:
    trades = {s: to_mc_trades(io_tv.load_exits(p)) for s, p in proto_csvs.items()}
    empty = [s for s, t in trades.items() if len(t) == 0]
    if empty:
        raise ValueError(
            f"5m re-MC: strategies with 0 exit rows: {empty}. "
            f"Re-export or check the 5m proto's session/vol filters before running the re-MC."
        )
    spans = {s: {"first": str(t["exit_date"].iloc[0].date()),
                 "last": str(t["exit_date"].iloc[-1].date()),
                 "n": int(len(t))} for s, t in trades.items()}
    panel, scale_info = pmc.build_daily_panel(trades, pmc.ALLOCATIONS)
    fell_back = {s: bool(info["fell_back"]) for s, info in scale_info.items()}
    blocks = pmc.build_week_blocks(panel)
    seeds = pmc._run_seeds(blocks, pmc.DD_TRIGGER, pmc.DD_SCALE,
                           strats=tuple(trades.keys()))
    agg = aggregate(seeds)
    return {**agg, "spans": spans, "fell_back": fell_back,
            "panel_start": str(panel.index.min().date()),
            "panel_end": str(panel.index.max().date()),
            "n_bdays": int(len(panel)), "n_blocks": int(len(blocks))}
