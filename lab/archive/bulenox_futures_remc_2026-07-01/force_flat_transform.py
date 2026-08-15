"""DJ30 force-flat-at-17:00-ET transform (Bulenox futures-prop pivot, 2026-07-01).

Bulenox (and every US futures-prop firm researched — see
docs/adr/2026-06-30-no-manual-trading-cfd-retirement.md and
lab/analysis/futures_prop_hold_compat_2026-06-30/RESULTS.md) mandatory-flattens
open positions at 17:00 ET; no overnight/weekend carry. DJ30's locked Pine
strategy has no such constraint (~3.7% of its trades hold past that boundary
per the 2026-06-30 hold-compat analysis). This module re-derives what each
of those trades would have realized if force-closed at the boundary instead
of its actual (later) exit, so the Bulenox re-MC panel reflects the venue's
actual constraint rather than the strategy's unconstrained backtest.

ZERO fork of locked core/portfolio_mc — reuses its `_ROLLOVER_HOUR_ET`
convention (the same 17:00 ET boundary already used for swap-cost rollover
counting) rather than re-deriving it.

Status (2026-07-03): the core truncation math AND the raw-CSV wrapper
(`force_flat_csv`) are unit-tested (test_force_flat_transform.py). The wrapper
was validated against the real Pepperstone DJ30 export (2026-05-24 vintage)
on 2026-07-03: the export's price column is "Price USD" (NOT "Price") —
corrected here; the "Trade #" / "Date and time" / "Net P&L USD" assumptions
matched real exports as-is (`_normalize_tv_columns` maps v5.6-vintage
"Net PnL USD" back to "Net P&L USD").
"""

from __future__ import annotations

import sys
from datetime import timedelta
from pathlib import Path
from typing import Tuple

import pandas as pd

_CORE = Path(__file__).resolve().parents[3] / "core"
if str(_CORE) not in sys.path:
    sys.path.insert(0, str(_CORE))

from portfolio_mc import _ROLLOVER_HOUR_ET, _normalize_tv_columns  # noqa: E402

# CME/CFD index futures have a daily settlement break 17:00-18:00 ET, so no bar
# is ever stamped exactly at the 17:00 force-flat boundary (empirically: 0 bars
# in the 17:xx hour across the full US30 panel; last pre-break bar is 16:45,
# whose close IS the 17:00 price). The fill uses the last bar at or before the
# boundary — normally 16:45, up to ~4h earlier on a half-day close. A prior bar
# farther than this is a genuine data gap, not a session break, and must raise
# rather than truncate at a stale price.
_MAX_BOUNDARY_GAP_H = 12


def bars_utc_to_et(bars_df: pd.DataFrame, time_col: str = "time") -> pd.DataFrame:
    """Convert a BAR_EXPORT bars DataFrame's UTC `time` column to tz-naive
    US/Eastern wall-clock time, DST-aware. The BAR_EXPORT epoch is always
    UTC even on an ET chart (memory: reference_bar_export_epoch_utc), while
    `portfolio_mc.load_trades`'s "Date and time" column is tz-naive chart-TZ
    ET. `force_flat_trade`'s bars_df lookup is a naive `==` comparison, so
    bars MUST be pre-converted with this function before being passed in —
    otherwise every lookup silently misses (or worse, hits the wrong bar) by
    the UTC-ET offset. Returns a copy; does not mutate the input.
    """
    out = bars_df.copy()
    out[time_col] = (
        pd.to_datetime(out[time_col], utc=True)
        .dt.tz_convert("America/New_York")
        .dt.tz_localize(None)
    )
    return out


def first_boundary_crossing(entry_dt, exit_dt, hour_et: int = _ROLLOVER_HOUR_ET):
    """First `hour_et`:00 ET timestamp strictly after entry_dt and <= exit_dt,
    or None if the trade never reaches one.

    Mirrors `portfolio_mc._count_rollovers`'s boundary-finding convention
    exactly (same replace/compare/advance-a-day bootstrapping) but returns
    the first crossing timestamp instead of a count — force-flat only cares
    about the FIRST boundary a trade is still open at; it closes there, so
    it can never reach a second one.
    """
    if hasattr(entry_dt, "to_pydatetime"):
        entry_dt = entry_dt.to_pydatetime()
    if hasattr(exit_dt, "to_pydatetime"):
        exit_dt = exit_dt.to_pydatetime()
    cur = entry_dt.replace(hour=hour_et, minute=0, second=0, microsecond=0)
    if cur <= entry_dt:
        cur += timedelta(days=1)
    return cur if cur <= exit_dt else None


def force_flat_trade(entry_dt, exit_dt, *, entry_price: float, exit_price: float,
                      pnl: float, bars_df: pd.DataFrame,
                      hour_et: int = _ROLLOVER_HOUR_ET) -> Tuple[object, float, bool]:
    """If the trade is still open at the first `hour_et`:00 ET boundary it
    crosses, truncate it there. Returns (new_exit_dt, new_pnl, was_truncated).

    Truncated pnl is the original pnl scaled by the ratio of the boundary
    bar's close-price move to the original full price move — proportional
    to the price move actually realized by the force-flat moment, holding
    position size/direction fixed (constant for the life of one Trade #, per
    the same per-Trade#-is-one-leg convention `_count_rollovers`/`load_trades`
    already assume). Robust to point-value/contract-multiplier drift since it
    only uses the CSV's own recorded prices and P&L, never an external
    contract-spec lookup — no risk of a stale DXTrade contractValue table.

    The fill price is the close of the last bar at or before the boundary: the
    17:00 ET force-flat instant falls in the CME/CFD 17:00-18:00 ET settlement
    break, so no bar is ever stamped exactly 17:00 — the 16:45 bar's close is
    the 17:00 price. Raises KeyError if the nearest prior bar is more than
    `_MAX_BOUNDARY_GAP_H` hours before the boundary — that is a genuine data
    gap, not a session break, and truncating at a stale price would corrupt
    the re-MC.
    """
    boundary_dt = first_boundary_crossing(entry_dt, exit_dt, hour_et)
    if boundary_dt is None:
        return exit_dt, pnl, False

    prior = bars_df.loc[bars_df["time"] <= boundary_dt]
    if prior.empty:
        raise KeyError(f"no bar at or before boundary {boundary_dt} in bars_df")
    last_idx = prior["time"].idxmax()  # robust to unsorted input
    last_time = prior.at[last_idx, "time"]
    if pd.Timedelta(boundary_dt - last_time) > pd.Timedelta(hours=_MAX_BOUNDARY_GAP_H):
        raise KeyError(
            f"nearest bar to boundary {boundary_dt} is {last_time} "
            f"(> {_MAX_BOUNDARY_GAP_H}h earlier) — data gap, not a session break"
        )
    boundary_close = float(prior.at[last_idx, "close"])

    price_range = exit_price - entry_price
    new_pnl = 0.0 if price_range == 0 else pnl * (boundary_close - entry_price) / price_range
    return boundary_dt, new_pnl, True


def force_flat_csv(raw_df: pd.DataFrame, bars_df: pd.DataFrame,
                    hour_et: int = _ROLLOVER_HOUR_ET) -> pd.DataFrame:
    """Raw-CSV-level wrapper, validated against a real Pepperstone DJ30 export
    on 2026-07-03. Expects `raw_df` in `portfolio_mc.load_trades`'s input
    shape (Entry/Exit rows keyed by "Trade #", "Date and time", "Price USD",
    "Net P&L USD"/normalized equivalent) and `bars_df` in
    `bar_export_loader.parse_bar_export`'s output shape ("time", "close").
    Returns a copy of `raw_df` with force-flatted Exit rows' "Date and time"
    and P&L column adjusted in place; Entry rows and untruncated Exit rows
    are unchanged.
    """
    df = _normalize_tv_columns(raw_df).copy()
    df["_dt"] = pd.to_datetime(df["Date and time"])
    entries = df[df["Type"].astype(str).str.startswith("Entry")]
    exits = df[df["Type"].astype(str).str.startswith("Exit")]

    for tnum in entries["Trade #"].unique():
        e = entries[entries["Trade #"] == tnum]
        x = exits[exits["Trade #"] == tnum]
        if len(e) != 1 or len(x) != 1:
            # Multi-leg pyramid adds get their own Trade #s in this export
            # convention (per portfolio_mc's swap-cost pairing); a 1:1
            # Entry:Exit mismatch here means that assumption doesn't hold
            # for this row and needs a human look, not a silent guess.
            raise ValueError(f"Trade #{tnum}: expected 1 Entry + 1 Exit row, "
                              f"got {len(e)} + {len(x)}")
        e_row, x_row = e.iloc[0], x.iloc[0]
        new_exit_dt, new_pnl, truncated = force_flat_trade(
            e_row["_dt"], x_row["_dt"],
            entry_price=float(e_row["Price USD"]), exit_price=float(x_row["Price USD"]),
            pnl=float(x_row["Net P&L USD"]), bars_df=bars_df, hour_et=hour_et,
        )
        if truncated:
            idx = x_row.name
            # Write the boundary time back in the CSV's own "%Y-%m-%d %H:%M"
            # string form, not a datetime object: "Date and time" is
            # string-dtype on modern pandas, so assigning a datetime raises
            # TypeError, and load_trades re-parses this column with
            # pd.to_datetime anyway (boundaries are always HH:00).
            df.loc[idx, "Date and time"] = new_exit_dt.strftime("%Y-%m-%d %H:%M")
            df.loc[idx, "Net P&L USD"] = new_pnl

    return df.drop(columns=["_dt"])
