"""Shared MYM M15 -> session-level loader for the mymdd_1_2026_08_29 Notice batch.

Panel: core/data/bar_data/MYM_M15.csv (BAR EXPORT v0.2, CBOT_MINI:MYM1!), epoch UTC
(reference/bar_export_epoch_utc.md). No instrument_id column (this is a single
continuous TV front-month export, not a Databento .c.0/.v.0 continuous roll series) --
roll contamination is detected empirically (large overnight jump near a 3rd-Friday
quarterly roll month), not read off a column.

Session convention: CME/Globex trading day D = [D-1 18:00 ET, D 17:00 ET) -- the
standard futures-trading-day bucketing, NOT UTC-calendar-day (which the W2 standing
warning flags as producing phantom weekend bars). RTH sub-window = [09:30, 15:59] ET,
overnight sub-window = same trading-day's bars strictly before 09:30 ET -- both pinned
to the convention already used on this exact panel by four MSL campaigns
(lab/archive/msl_c1_mym_2026-08/construct_lib.py RTH_OPEN_MIN/RTH_CLOSE_MIN/
OVERNIGHT_CLOSE_MIN), not invented here.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[4]
PANEL = REPO / "core" / "data" / "bar_data" / "MYM_M15.csv"

RTH_OPEN_MIN = 9 * 60 + 30
RTH_CLOSE_MIN = 15 * 60 + 59
OVERNIGHT_CLOSE_MIN = 9 * 60 + 29


def load_bars() -> pd.DataFrame:
    df = pd.read_csv(PANEL)
    ts = pd.to_datetime(df["time"], utc=True)
    et = ts.dt.tz_convert("America/New_York")
    out = pd.DataFrame({
        "ts_et": et,
        "open": df["open"].astype(float),
        "high": df["high"].astype(float),
        "low": df["low"].astype(float),
        "close": df["close"].astype(float),
        "volume": df["volume"].astype(float),
    })
    out = out.sort_values("ts_et").reset_index(drop=True)
    # trading-day bucket: a wall-clock rule (bar hour >= 18 -> next calendar date),
    # not a fixed-Timedelta shift -- a Timedelta subtraction on a tz-aware series
    # follows absolute elapsed time, which mis-buckets the 4 bars right after the
    # Sunday 18:00 reopen in the one week/year that crosses the US spring-forward
    # transition (verified: 6 spurious dayofweek==5 "sessions" of n_bars=4 each
    # before this fix, one per year 2021-2026, all on the Mar 2nd-Sunday reopen).
    hour = out["ts_et"].dt.hour
    date = out["ts_et"].dt.date
    out["session"] = np.where(hour >= 18, pd.DatetimeIndex(date) + pd.Timedelta(days=1), pd.DatetimeIndex(date))
    out["session"] = pd.to_datetime(out["session"]).dt.date
    out["minute"] = out["ts_et"].dt.hour * 60 + out["ts_et"].dt.minute
    return out


def session_ohlc(bars: pd.DataFrame) -> pd.DataFrame:
    """Full trading-day OHLC (overnight + RTH), one row per session -- the GC/CL
    ohlcv-1d analogue."""
    g = bars.groupby("session", sort=True)
    rec = g.agg(
        open=("open", "first"),
        high=("high", "max"),
        low=("low", "min"),
        close=("close", "last"),
        volume=("volume", "sum"),
        n_bars=("open", "size"),
    )
    rec.index = pd.to_datetime(rec.index)
    return rec


def rth_ohlc(bars: pd.DataFrame) -> pd.DataFrame:
    m = (bars["minute"] >= RTH_OPEN_MIN) & (bars["minute"] <= RTH_CLOSE_MIN)
    g = bars[m].groupby("session", sort=True)
    rec = g.agg(
        open=("open", "first"), high=("high", "max"), low=("low", "min"),
        close=("close", "last"), volume=("volume", "sum"), n_bars=("open", "size"),
    )
    rec.index = pd.to_datetime(rec.index)
    return rec


def overnight_ohlc(bars: pd.DataFrame) -> pd.DataFrame:
    m = bars["minute"] <= OVERNIGHT_CLOSE_MIN
    g = bars[m].groupby("session", sort=True)
    rec = g.agg(
        open=("open", "first"), high=("high", "max"), low=("low", "min"),
        close=("close", "last"), volume=("volume", "sum"), n_bars=("open", "size"),
    )
    rec.index = pd.to_datetime(rec.index)
    return rec


def wilder_tr(o: pd.DataFrame) -> pd.Series:
    h, l, c = o["high"].to_numpy(), o["low"].to_numpy(), o["close"].to_numpy()
    prev_c = np.empty(len(o)); prev_c[0] = np.nan; prev_c[1:] = c[:-1]
    tr = np.maximum.reduce([h - l, np.abs(h - prev_c), np.abs(l - prev_c)])
    tr[0] = np.nan
    return pd.Series(tr, index=o.index, name="TR")


def flag_roll_days(o: pd.DataFrame, tr: pd.Series, mult: float = 8.0) -> pd.Series:
    """Empirical roll-day detector: TR >= mult x the trailing-60 median AND the
    session falls in a quarterly roll month (Mar/Jun/Sep/Dec, day-of-month 13-19,
    the 3rd-Friday window) -- mirrors W1's named roll-date convention rather than
    flagging every large-range day (a real vol spike is not a roll)."""
    med60 = tr.rolling(60, min_periods=30).median().shift(1)
    big = tr >= (mult * med60)
    roll_month = o.index.month.isin([3, 6, 9, 12])
    roll_window = (o.index.day >= 13) & (o.index.day <= 19)
    return big & roll_month & roll_window


if __name__ == "__main__":
    bars = load_bars()
    print(f"bars: {len(bars)}  span {bars['ts_et'].min()} .. {bars['ts_et'].max()}")
    full = session_ohlc(bars)
    print(f"sessions (full): {len(full)}  span {full.index.min()} .. {full.index.max()}")
    rth = rth_ohlc(bars)
    print(f"sessions (RTH):  {len(rth)}")
    on = overnight_ohlc(bars)
    print(f"sessions (overnight): {len(on)}")
    print("\nfull-session n_bars distribution:")
    print(full["n_bars"].describe())
    print("low-bar-count sessions (<20):", int((full["n_bars"] < 20).sum()))
    print(full.index[full["n_bars"] < 20].tolist())

    tr = wilder_tr(full)
    print(f"TR valid: {tr.notna().sum()} / {len(tr)}")
    roll = flag_roll_days(full, tr)
    print(f"roll-day candidates flagged: {int(roll.sum())}")
    print(full.index[roll][:20].tolist())
    print(tr[roll].describe())
    print("\nTR describe (all):")
    print(tr.describe())
    # sanity: day-of-week census on full-session index
    print("\ndow census:", pd.Series(full.index.dayofweek).value_counts().sort_index().to_dict())
