"""Minimal, repo-self-contained TradingView List-of-Trades loader.

Extracted from `.claude/skills/trade-csv-reconcile/scripts/reconcile.py::load_csv`
(BOM handling + the current/legacy column-alias map only — the R-pinning and
Pine-header-baseline machinery in that skill is for the four LOCKED strategies
and does not apply to this candidate). Kept local so this campaign's scripts
are runnable from a fresh checkout without depending on the operator's
personal `.claude/skills/` directory.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

COLUMN_ALIASES = {
    "Trade number": "Trade #",
    "Net PnL USD": "Net P&L USD",
    "Net PnL %": "Net P&L %",
    "Return %": "Net P&L %",
    "Cumulative PnL USD": "Cumulative P&L USD",
    "Cumulative PnL %": "Cumulative P&L %",
}


def load_csv(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="utf-8-sig")
    df.columns = [c.strip().replace("﻿", "") for c in df.columns]

    rename_map = {
        src: dst
        for src, dst in COLUMN_ALIASES.items()
        if src in df.columns and dst not in df.columns
    }
    if rename_map:
        df = df.rename(columns=rename_map)

    required = {"Trade #", "Type", "Date and time", "Net P&L USD"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(
            f"CSV missing required columns: {missing}. Available: {list(df.columns)}"
        )

    df["dt"] = pd.to_datetime(df["Date and time"], errors="coerce")
    return df
