"""Roll-seam flagging for unadjusted continuous-contract bar panels.

Spec: docs/superpowers/specs/2026-07-01-cfd-to-futures-conversion-design.md §2.1.
A seam = an overnight gap large enough AND falling in the symbol's roll window.

SCOPE (R5): this makes PER-BAR derivations (ATR, single-bar stats) safe by
letting callers exclude seam bars. It does NOT make an unadjusted panel safe
for multi-day drawdown/return path reconstruction — deleting a seam bar does
not remove the price-path discontinuity. Path-spanning work needs a
back-adjusted series or explicit gap-splicing, not this mask.
"""
from __future__ import annotations

import datetime as _dt

import pandas as pd

QUARTERLY = "quarterly"   # Mar/Jun/Sep/Dec — equity index + FX (NQ/YM/J7)
BIMONTHLY = "bimonthly"   # gold even-month listing (QO): rolls out of odd months

ROLL_CYCLE_BY_SYMBOL = {
    "NQ": QUARTERLY,
    "MNQ": QUARTERLY,  # Micro NQ — same Mar/Jun/Sep/Dec cycle as NQ
    "YM": QUARTERLY,
    "MYM": QUARTERLY,  # Micro YM — same Mar/Jun/Sep/Dec cycle as YM
    "J7": QUARTERLY,
    "QO": BIMONTHLY,
    "GC": BIMONTHLY,   # COMEX gold (even-month active: Feb/Apr/Jun/Aug/Oct/Dec)
    "MGC": BIMONTHLY,  # Micro gold — same roll cycle as GC (2026-07 Guardian self-funded floor)
}


def _in_roll_window(ts: pd.Timestamp, cycle: str) -> bool:
    if cycle == BIMONTHLY:
        # Gold is listed in even months; the continuous series rolls out of the
        # non-listed odd month. Window = last ~week of an odd month into the
        # first few days of the even month it rolls into.
        return (ts.month % 2 == 1 and ts.day >= 22) or (ts.month % 2 == 0 and ts.day <= 3)
    # Quarterly: ~8-10 sessions before the 3rd Friday of Mar/Jun/Sep/Dec.
    return ts.month in (3, 6, 9, 12) and 5 <= ts.day <= 18


def flag_roll_seams(bars: pd.DataFrame, *, symbol: str,
                    threshold_pct: float = 0.5) -> pd.DataFrame:
    """Return a copy of `bars` with a boolean `roll_seam` column.

    Requires columns `time` (UTC-parseable), `open`, `close`. The first row is
    never a seam (no prior close to gap from).
    """
    if symbol not in ROLL_CYCLE_BY_SYMBOL:
        raise KeyError(
            f"no roll cycle registered for {symbol!r}; add it to ROLL_CYCLE_BY_SYMBOL"
        )
    out = bars.copy()
    t = pd.to_datetime(out["time"], utc=True)
    gap_pct = (out["open"] / out["close"].shift(1) - 1.0).abs() * 100.0
    cycle = ROLL_CYCLE_BY_SYMBOL[symbol]
    in_win = t.apply(lambda x: _in_roll_window(x, cycle))
    out["roll_seam"] = (gap_pct > threshold_pct).fillna(False) & in_win.to_numpy()
    return out


def roll_seam_dates(bars: pd.DataFrame, *, symbol: str,
                    threshold_pct: float = 0.5) -> list[_dt.date]:
    flagged = flag_roll_seams(bars, symbol=symbol, threshold_pct=threshold_pct)
    t = pd.to_datetime(flagged.loc[flagged["roll_seam"], "time"], utc=True)
    return sorted(set(t.dt.date.tolist()))
