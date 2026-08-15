"""Canonical TradingView column and row-pairing contracts."""
from __future__ import annotations

from collections.abc import Iterator

import pandas as pd


TV_COLUMN_ALIASES: dict[str, str] = {
    "Trade number": "Trade #",
    "Net PnL USD": "Net P&L USD",
    "Net PnL %": "Net P&L %",
    "Return %": "Net P&L %",
    "Cumulative PnL USD": "Cumulative P&L USD",
    "Cumulative PnL %": "Cumulative P&L %",
}

COL_TRADE_NO = "Trade #"
COL_TYPE = "Type"
COL_DATETIME = "Date and time"
COL_SIGNAL = "Signal"
COL_QTY = "Size (qty)"
COL_NET_PNL_USD = "Net P&L USD"


def normalize_tv_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Return a frame exposing canonical TradingView column names."""
    renames = {
        alias: canonical
        for alias, canonical in TV_COLUMN_ALIASES.items()
        if alias in df.columns and canonical not in df.columns
    }
    return df.rename(columns=renames) if renames else df


def split_aligned_tv_rows(
    raw: pd.DataFrame,
    *,
    source_label: str = "TV-export",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return strictly aligned entry and exit rows indexed by trade number."""
    normalized = normalize_tv_columns(raw)
    entries = normalized[normalized[COL_TYPE].str.startswith("Entry")].copy()
    exits = normalized[normalized[COL_TYPE].str.startswith("Exit")].copy()
    if len(entries) != len(exits):
        raise AssertionError(
            f"TV-export pairing fail [{source_label}]: "
            f"{len(entries)} entries vs {len(exits)} exits"
        )

    entries = entries.set_index(COL_TRADE_NO)
    exits = exits.set_index(COL_TRADE_NO)
    if not entries.index.equals(exits.index):
        raise AssertionError(
            f"TV-export pairing fail [{source_label}]: "
            "Trade # index mismatch between entry and exit rows"
        )
    return entries, exits


def iter_tv_trade_pairs(
    raw: pd.DataFrame,
) -> Iterator[tuple[object, pd.Series, pd.Series]]:
    """Yield the first entry/exit row for each TradingView trade group."""
    normalized = normalize_tv_columns(raw)
    for trade_no, group in normalized.groupby(COL_TRADE_NO):
        types = group[COL_TYPE].str.lower()
        entry = group[types.str.startswith("entry")].iloc[0]
        exit_ = group[types.str.startswith("exit")].iloc[0]
        yield trade_no, entry, exit_
