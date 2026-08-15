"""Side-agnostic TV List-of-Trades exit-row loader for the 5m harness.

Unlike core.tv_export_loader.pair_tv_export_dataframe, this does NOT require
long-only entries or a symbol price column — it only needs the P&L + timestamp
columns shared by every TV strategy export. Reuses core's column normalization
and the MVD min-rows floor."""
from __future__ import annotations
from pathlib import Path
import pandas as pd

import portfolio_mc as pmc          # core, via conftest sys.path
from lib.mvd import assert_min_rows

def load_exits(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    df = pd.read_csv(path, encoding="utf-8-sig")
    df = pmc._normalize_tv_columns(df)
    assert_min_rows(len(df), 100, label=f"5m harness panel {path.name}")
    ex = df[df["Type"].astype(str).str.startswith("Exit")].copy()
    ts = pd.to_datetime(ex["Date and time"])
    out = pd.DataFrame({
        "exit_ts":     ts.values,
        "exit_date":   ts.dt.normalize().values,
        "net_pnl_usd": ex["Net P&L USD"].astype(float).values,
        "net_pnl_pct": ex["Net P&L %"].astype(float).values,
    })
    return out.sort_values("exit_ts").reset_index(drop=True)
