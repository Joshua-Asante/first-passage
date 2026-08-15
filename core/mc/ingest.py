"""TradingView ingestion and panel construction for portfolio MC."""

from __future__ import annotations

from datetime import timedelta
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import pandas as pd

try:
    from ..historical_challenge import STARTING_EQUITY
    from ..lib.mvd import assert_min_rows, assert_window
    from ..tv_schema import (
        TV_COLUMN_ALIASES,
        normalize_tv_columns as _canonical_normalize_tv_columns,
    )
except ImportError:
    from historical_challenge import STARTING_EQUITY
    from lib.mvd import assert_min_rows, assert_window
    from tv_schema import (
        TV_COLUMN_ALIASES,
        normalize_tv_columns as _canonical_normalize_tv_columns,
    )

SWAP_RATES_PER_UNIT_PER_NIGHT: Dict[str, Dict[str, float]] = {
    "guardian":       {"long": -57.49 / 100.0,           "short":  43.84 / 100.0},
    "striker":        {"long":  -0.969 / 10.0,           "short":   0.194 / 10.0},
    "aegis":          {"long":   0.005 * 0.001 / 150.0,  "short":  -0.01 * 0.001 / 150.0},
    "striker_nas100": {"long":  -0.523 / 10.0,           "short":   0.105 / 10.0},
}
ROLLOVER_HOUR_ET = 17
ROLLOVER_TIMEZONE = "America/New_York"
TV_COLUMN_NORMALIZATION: Dict[str, str] = TV_COLUMN_ALIASES


def _as_eastern(value):
    """Interpret naive TV timestamps as ET and convert aware timestamps to ET."""
    timestamp = pd.Timestamp(value)
    if timestamp.tzinfo is None:
        timestamp = timestamp.tz_localize(ROLLOVER_TIMEZONE)
    else:
        timestamp = timestamp.tz_convert(ROLLOVER_TIMEZONE)
    return timestamp.to_pydatetime()


def count_rollovers(entry_dt, exit_dt) -> int:
    """Count 17:00 ET rollover crossings strictly after entry and through exit."""
    entry_dt = _as_eastern(entry_dt)
    exit_dt = _as_eastern(exit_dt)
    cur = entry_dt.replace(
        hour=ROLLOVER_HOUR_ET, minute=0, second=0, microsecond=0
    )
    if cur <= entry_dt:
        cur += timedelta(days=1)
    nights = 0
    while cur <= exit_dt:
        nights += 1
        cur += timedelta(days=1)
    return nights


def compute_per_trade_swap(df: pd.DataFrame, strategy: str) -> pd.DataFrame:
    """Return per-trade FXIFY overnight swap costs."""
    if strategy not in SWAP_RATES_PER_UNIT_PER_NIGHT:
        raise ValueError(
            f"No swap rate registered for strategy={strategy!r}. "
            f"Known: {list(SWAP_RATES_PER_UNIT_PER_NIGHT.keys())}"
        )
    rates = SWAP_RATES_PER_UNIT_PER_NIGHT[strategy]
    work = df.copy()
    work["_dt"] = pd.to_datetime(work["Date and time"])
    entries = work[work["Type"].astype(str).str.startswith("Entry")]
    exits = work[work["Type"].astype(str).str.startswith("Exit")]

    rows = []
    for trade_number in entries["Trade #"].unique():
        entry_rows = entries[entries["Trade #"] == trade_number]
        exit_rows = exits[exits["Trade #"] == trade_number]
        if entry_rows.empty or exit_rows.empty:
            continue
        entry_dt = entry_rows["_dt"].min()
        exit_dt = exit_rows["_dt"].max()
        quantity = float(entry_rows["Size (qty)"].iloc[0])
        is_long = str(entry_rows["Type"].iloc[0]).endswith("long")
        rate = rates["long"] if is_long else rates["short"]
        nights = count_rollovers(entry_dt, exit_dt)
        rows.append(
            {"Trade #": trade_number, "swap_cost": quantity * rate * nights}
        )

    return pd.DataFrame(rows, columns=["Trade #", "swap_cost"])


def normalize_tv_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Compatibility wrapper for the canonical TradingView normalizer."""
    return _canonical_normalize_tv_columns(df)


def load_trades(
    path: Path, *, strategy: str | None = None, apply_swap: bool = False
) -> pd.DataFrame:
    """Load a TV List-of-Trades CSV as normalized exit-date P&L rows."""
    df = pd.read_csv(path, encoding="utf-8-sig")
    df = normalize_tv_columns(df)
    assert_min_rows(len(df), 100, label=f"MC input panel {path.name}")
    exits = df[df["Type"].astype(str).str.startswith("Exit")].copy()
    exits["exit_date"] = pd.to_datetime(exits["Date and time"]).dt.normalize()
    exits = exits.rename(columns={"Net P&L USD": "pnl"})

    if apply_swap:
        if strategy is None:
            raise ValueError("apply_swap=True requires strategy argument")
        swap_df = compute_per_trade_swap(df, strategy)
        exits = exits.merge(swap_df, on="Trade #", how="left")
        exits["swap_cost"] = exits["swap_cost"].fillna(0.0)
        exits["pnl"] = exits["pnl"] + exits["swap_cost"]

    out = exits[["exit_date", "pnl"]].sort_values("exit_date").reset_index(drop=True)
    if not out.empty:
        assert_window(
            out["exit_date"].iloc[0].to_pydatetime(),
            out["exit_date"].iloc[-1].to_pydatetime(),
            expected_min_days=4 * 365,
            label=f"MC input panel {path.name}",
            tolerance_days=100,
        )
    return out


def implied_1r(
    pnl: pd.Series, strategy: str, account: float | None = None
) -> Tuple[float, bool]:
    """Return the implied dollar 1R and whether median fallback was used.

    ``account`` resolves at call time (not def time) so an explicit basis or a
    monkeypatched ``STARTING_EQUITY`` is honored. Default ``None`` keeps the
    historical $200K path byte-identical. The 0.01 * account threshold is a
    cohort selector for full-stop losses, not a scale factor — a wrong basis
    reclassifies the 1R sample.
    """
    account = STARTING_EQUITY if account is None else account
    abs_losses = pnl[pnl < 0].abs()
    if strategy == "guardian":
        return float(abs_losses.median()), False
    full_stops = abs_losses[abs_losses > 0.01 * account]
    if len(full_stops) < 5:
        return float(abs_losses.median()), True
    return float(full_stops.mean()), False


def build_daily_panel(
    trades_by_strat: Dict[str, pd.DataFrame],
    allocations: Dict[str, float],
    fixed_1r_reference: Dict[str, float] | None = None,
    *,
    account_basis: float | None = None,
) -> Tuple[pd.DataFrame, Dict[str, dict]]:
    """Risk-normalize strategy P&L and aggregate it to business days.

    ``account_basis`` (keyword-only) defaults to the historical challenge
    ``STARTING_EQUITY``. Explicit threading is the Phase-1 decoupling seam
    (ADR 2026-07-22 §7); the default path must stay byte-identical.
    """
    basis = STARTING_EQUITY if account_basis is None else account_basis
    scale_info: Dict[str, dict] = {}
    series = []
    for strategy, trades in trades_by_strat.items():
        if fixed_1r_reference is not None:
            r1 = float(fixed_1r_reference[strategy])
            fell_back = False
        else:
            r1, fell_back = implied_1r(trades["pnl"], strategy, account=basis)
        target_dollars = allocations[strategy] * basis
        scale = target_dollars / r1 if r1 > 0 else 1.0
        scale_info[strategy] = {
            "implied_1r": r1,
            "scale": scale,
            "n_trades": len(trades),
            "fell_back": fell_back,
        }
        pnl_by_day = trades.groupby("exit_date")["pnl"].sum() * scale
        pnl_by_day.name = strategy
        series.append(pnl_by_day)
    panel = pd.concat(series, axis=1, sort=True).fillna(0.0)
    business_days = pd.bdate_range(panel.index.min(), panel.index.max())
    return panel.reindex(business_days).fillna(0.0), scale_info


def build_week_blocks(panel: pd.DataFrame) -> np.ndarray:
    """Return Mon-anchored non-overlapping five-business-day blocks."""
    values = panel.values
    blocks = []
    for index, day in enumerate(panel.index):
        if day.weekday() == 0 and index + 5 <= len(panel):
            blocks.append(values[index:index + 5])
    return np.array(blocks)
