"""Fixing-reversal cost pre-screen — library (2026-06-22).

Cheapest falsifier for the FX intraday fixing-reversal 5th-leg mechanism
(Krohn, Mueller & Whelan, *Journal of Finance* 2024): does a London 16:00 fix
fade on EURUSD clear the after-cost hurdle, or does it die on cost as the paper
predicts (edge survives at half-spread, NEGATIVE at full retail spread)?

This measures, on the canonical Pepperstone 5m feed, the post-fix reversal, the
realized cost-in-R (the USDCAD cost law: cost/R = round-trip-cost / stop), and
the BREAK-EVEN spread — compared to FXIFY-realistic EURUSD spreads. It does NOT
claim an edge; a PASS graduates to a separate, pre-registered edge validation.

RESEARCH (lab/). Zero core/ touch: reuses the canonical BAR_EXPORT decode
primitive (``core/bar_export_loader.decode_bar_signal`` + ``price_tolerance``)
without modifying it, and does not register EURUSD in the core price-column map
(promotion to core happens only at admission).

Run from this directory:  python -m pytest test_fixrev_costscreen.py -q
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Sequence

import numpy as np
import pandas as pd

# ── wire in the canonical (locked) BAR_EXPORT decode primitive, zero fork ──────
_CORE = Path(__file__).resolve().parents[3] / "core"
if str(_CORE) not in sys.path:
    sys.path.insert(0, str(_CORE))
from bar_export_loader import decode_bar_signal, price_tolerance  # noqa: E402

PIP = 0.0001            # EURUSD pip
FIX_TZ = "Europe/London"


# ── DST-aware fix-time resolution ─────────────────────────────────────────────
def london_fix_utc(date, *, hour: int = 16, minute: int = 0, tz: str = FIX_TZ) -> pd.Timestamp:
    """The WM/Reuters 4pm London fix for ``date``, resolved to a UTC instant.

    16:00 *London local* is 16:00 UTC in winter (GMT) and 15:00 UTC in summer
    (BST). Resolving via the zone (not a hardcoded UTC hour) is the DST trap this
    guards against — distinct from the BAR_EXPORT epoch (already UTC).
    """
    local = pd.Timestamp(
        year=date.year, month=date.month, day=date.day, hour=hour, minute=minute, tz=tz
    )
    return local.tz_convert("UTC")


# ── BAR_EXPORT v0.1 loader (lab-local; reuses core decode_bar_signal) ─────────
def decode_bars(
    paths: Sequence[str | Path], *, price_col: str = "Price USD", symbol: str = "EURUSD"
) -> pd.DataFrame:
    """Decode one or more BAR_EXPORT v0.1 page CSVs into a UTC OHLCV bar frame.

    Mirrors ``core.bar_export_loader.parse_bar_export`` semantics (epoch_ms is
    bar-open UTC and authoritative; Entry price must equal the encoded close =
    format-drift detector; pages deduped on ``time`` keep='last', sorted) but
    takes the price column explicitly so EURUSD need not be registered in core.
    """
    frames: list[pd.DataFrame] = []
    for p in paths:
        raw = pd.read_csv(p, encoding="utf-8-sig")
        raw.columns = [str(c).strip() for c in raw.columns]
        if price_col not in raw.columns:
            raise ValueError(f"BAR_EXPORT missing price column {price_col!r}: {p}")
        entries = raw[raw["Type"].astype(str).str.startswith("Entry")]
        rows: list[dict] = []
        for _, row in entries.iterrows():
            enc = decode_bar_signal(row.get("Signal", ""))
            if "epoch_ms" not in enc:
                raise ValueError(f"BAR_EXPORT signal missing epoch (legacy comment fmt?): {p}")
            entry_px = float(row[price_col])
            tol = price_tolerance(symbol, enc["c"])
            if abs(entry_px - enc["c"]) > tol:
                raise ValueError(
                    f"Cross-check fail {p}: entry px {entry_px} vs encoded close {enc['c']}"
                )
            rows.append({
                "time": pd.to_datetime(int(enc["epoch_ms"]), unit="ms", utc=True),
                "open": enc["o"], "high": enc["h"], "low": enc["l"],
                "close": enc["c"], "volume": int(enc["v"]),
            })
        if not rows:
            raise ValueError(f"No decodable Entry bars in {p}")
        frames.append(pd.DataFrame(rows))
    df = pd.concat(frames, ignore_index=True)
    return (
        df.sort_values("time")
        .drop_duplicates(subset="time", keep="last")
        .reset_index(drop=True)
    )


def fix_bar_index(bars: pd.DataFrame, fix_ts: pd.Timestamp):
    """Positional index of the bar whose open == ``fix_ts``; None if absent (skip)."""
    pos = np.flatnonzero((bars["time"] == fix_ts).to_numpy())
    return int(pos[0]) if len(pos) else None


# ── signal magnitude (paper bps frame) ───────────────────────────────────────
def fix_window_return_bps(bars: pd.DataFrame, fix_idx: int, post_bars: int) -> float:
    """Post-fix EURUSD return from the fix bar's close over ``post_bars``, in bps."""
    c = bars["close"].to_numpy()
    return float((c[fix_idx + post_bars] - c[fix_idx]) / c[fix_idx] * 1e4)


# ── one fade trade (the cost-law unit) ───────────────────────────────────────
def simulate_fade(
    bars: pd.DataFrame, entry_idx: int, hold_bars: int, stop_pips: float, *,
    spread_pips: float, commission_pips: float, side: int = +1, pip: float = PIP,
) -> dict:
    """Long(+1)/short(-1) fade entered at the fix bar's close, protective stop at
    ``stop_pips``, time-exit ``hold_bars`` later. R = stop distance; cost-in-R is
    the round-trip cost / stop. gross/net reported in R."""
    close = bars["close"].to_numpy()
    high = bars["high"].to_numpy()
    low = bars["low"].to_numpy()
    entry_price = float(close[entry_idx])
    R = stop_pips * pip
    stop_price = entry_price - side * R

    exit_price = None
    exit_reason = "time"
    last = entry_idx + hold_bars
    for j in range(entry_idx + 1, last + 1):
        if j >= len(close):
            break
        if side > 0 and low[j] <= stop_price:
            exit_price, exit_reason = stop_price, "stop"
            break
        if side < 0 and high[j] >= stop_price:
            exit_price, exit_reason = stop_price, "stop"
            break
    if exit_price is None:
        exit_price = float(close[min(last, len(close) - 1)])

    gross_R = side * (exit_price - entry_price) / R
    cost_R = (spread_pips + commission_pips) / stop_pips
    return {
        "entry_price": entry_price, "exit_price": float(exit_price),
        "gross_R": float(gross_R), "cost_R": float(cost_R),
        "net_R": float(gross_R - cost_R), "exit_reason": exit_reason,
    }


def breakeven_spread_pips(mean_gross_R: float, stop_pips: float, commission_pips: float) -> float:
    """Spread at which mean net_R = 0:  (spread+comm)/stop = mean_gross  ⇒
    spread = mean_gross*stop - comm. Above this spread the cell is net-negative."""
    return mean_gross_R * stop_pips - commission_pips


# ── the screen ───────────────────────────────────────────────────────────────
def run_screen(
    bars: pd.DataFrame, *, hold_grid_bars: Sequence[int], stop_grid_pips: Sequence[float],
    spread_grid_pips: Sequence[float], commission_pips: float, side: int = +1, pip: float = PIP,
) -> dict:
    """One trade per fix-day (long EURUSD at the fix, protective stop, time-exit),
    aggregated over a (hold × stop) grid; net derived per spread by subtracting
    the constant cost-in-R. Reports per-cell n, mean gross R, win rate, stop-out
    share, break-even spread, and net at each spread."""
    bars = bars.sort_values("time").reset_index(drop=True)
    dates = sorted(set(pd.DatetimeIndex(bars["time"]).date))

    entries: list[int] = []
    skipped = 0
    for d in dates:
        idx = fix_bar_index(bars, london_fix_utc(d))
        if idx is None:
            skipped += 1
        else:
            entries.append(idx)

    cells = []
    for hold in hold_grid_bars:
        for stop in stop_grid_pips:
            gross, reasons = [], []
            for idx in entries:
                if idx + hold >= len(bars):
                    continue
                tr = simulate_fade(bars, idx, hold, stop, spread_pips=0.0,
                                   commission_pips=0.0, side=side, pip=pip)
                gross.append(tr["gross_R"])
                reasons.append(tr["exit_reason"])
            g = np.asarray(gross, float)
            n = len(g)
            mean_gross = float(g.mean()) if n else float("nan")
            per_spread = []
            for s in spread_grid_pips:
                cost_R = (s + commission_pips) / stop
                net = g - cost_R
                per_spread.append({
                    "spread_pips": s, "cost_R": cost_R,
                    "mean_net_R": float(net.mean()) if n else float("nan"),
                    "pct_net_positive": float((net > 0).mean()) if n else float("nan"),
                })
            cells.append({
                "hold_bars": hold, "hold_min": hold * 5, "stop_pips": stop,
                "n_trades": n, "mean_gross_R": mean_gross,
                "win_rate": float((g > 0).mean()) if n else float("nan"),
                "stop_out_share": float(np.mean([r == "stop" for r in reasons])) if n else float("nan"),
                "breakeven_spread_pips": breakeven_spread_pips(mean_gross, stop, commission_pips) if n else float("nan"),
                "per_spread": per_spread,
            })
    return {
        "cells": cells,
        "n_fix_days": len(entries),
        "n_skipped_days": skipped,
        "date_min": str(min(dates)) if dates else None,
        "date_max": str(max(dates)) if dates else None,
    }


def classify_verdict(
    *, best_breakeven_pips: float, fxify_spread_pips: float, n_trades: int, n_floor: int
) -> str:
    """Pre-stated gate. ``best_breakeven_pips`` is the MAX break-even spread across
    the grid (best-of-grid = an optimistic upper bound, multiplicity-aware).

    - ``INSUFFICIENT-DATA`` if n < floor.
    - ``FAIL-COST`` if even the best cell's break-even spread ≤ FXIFY's realistic
      EURUSD spread (cost eats the edge — the paper's own prediction).
    - ``PASS-PROVISIONAL`` if the best cell clears FXIFY cost → graduates to a
      separate, pre-registered edge validation (this pre-screen claims no edge).
    """
    if n_trades < n_floor:
        return "INSUFFICIENT-DATA"
    return "PASS-PROVISIONAL" if best_breakeven_pips > fxify_spread_pips else "FAIL-COST"


def find_input_csvs(directory, *, pattern: str = "BAR_EXPORT_*_EURUSD_*.csv") -> list[str]:
    """Sorted matching CSVs in ``directory`` (empty list if absent → graceful skip)."""
    d = Path(directory)
    if not d.exists():
        return []
    return sorted(str(p) for p in d.glob(pattern))
