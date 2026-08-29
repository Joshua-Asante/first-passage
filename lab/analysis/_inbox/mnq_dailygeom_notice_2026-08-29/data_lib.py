"""Shared data prep for the 2026-08-29 MNQ Notice-phase 5-candidate screen.

Panel: core/data/bar_data/MNQ_M15.csv (BAR EXPORT v0.2, CME_MINI:MNQ1!), UTC time,
columns time,open,high,low,close,volume. No instrument_id column (TV continuous
front-month "1!" splice -- the TV analogue of databento's .v.0 volume-lead per
ops/instruments/MNQ.md W1) -- unlike GC/CL's raw databento continuous panels, no
roll-day exclusion is performed here; there is no per-bar roll marker to key it on.

RTH convention pinned to this repo's own standing use on MNQ M15/1m native-bar
campaigns (lab/analysis/c1/mnq_tnec_con4_pdh_pdl_break_2026-08/construct_lib.py):
RTH = [09:30, 16:00) America/New_York, tz-aware conversion (handles DST).

Trading-day (session) boundary: CME's own convention -- the Globex day for a given
trading date opens 18:00 ET the evening before and closes 17:00 ET on the date
itself. Bars from 18:00-23:59 ET belong to the NEXT calendar trading day. This
naturally absorbs the Sun-18:00-ET reopen into Monday's trading day and produces
no phantom Saturday session -- unlike databento's ohlcv-1d UTC-calendar-day
bucketing (MNQ.md W2), so no explicit weekend-row filter is needed here (disclosed
in the write-up as a by-construction difference from the GC/CL daily panels, not
an oversight).
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CSV = HERE.parent.parent.parent.parent / "core" / "data" / "bar_data" / "MNQ_M15.csv"

RTH_OPEN_MIN = 9 * 60 + 30   # 09:30 ET
RTH_CLOSE_MIN = 16 * 60      # 16:00 ET
TRADING_DAY_CUTOVER_MIN = 18 * 60  # 18:00 ET -> next trading day


def load_raw() -> pd.DataFrame:
    df = pd.read_csv(CSV)
    assert list(df.columns) == ["time", "open", "high", "low", "close", "volume"], df.columns
    df["time"] = pd.to_datetime(df["time"], utc=True)
    df = df.sort_values("time").drop_duplicates(subset="time", keep="last").reset_index(drop=True)
    et = df["time"].dt.tz_convert("America/New_York")
    df["et"] = et
    df["et_minute"] = et.dt.hour * 60 + et.dt.minute
    # trading-day: et date, +1 day if et_minute >= 18:00 cutover
    et_date = et.dt.normalize()
    bump = (df["et_minute"] >= TRADING_DAY_CUTOVER_MIN)
    df["trading_day"] = (et_date + pd.to_timedelta(bump.astype(int), unit="D")).dt.date
    df["is_rth"] = (df["et_minute"] >= RTH_OPEN_MIN) & (df["et_minute"] < RTH_CLOSE_MIN)
    return df


def daily_ohlc(df: pd.DataFrame) -> pd.DataFrame:
    """One row per trading_day: full-session (all bars, RTH+overnight) OHLC + bar count."""
    g = df.groupby("trading_day", sort=True)
    out = pd.DataFrame({
        "open": g["open"].first(),
        "high": g["high"].max(),
        "low": g["low"].min(),
        "close": g["close"].last(),
        "n_bars": g.size(),
        "volume": g["volume"].sum(),
    })
    out.index = pd.to_datetime(out.index)
    return out.sort_index()


def rth_ohlc(df: pd.DataFrame) -> pd.DataFrame:
    """One row per trading_day: RTH-only [09:30,16:00) ET OHLC + bar count."""
    r = df[df["is_rth"]]
    g = r.groupby("trading_day", sort=True)
    out = pd.DataFrame({
        "open": g["open"].first(),
        "high": g["high"].max(),
        "low": g["low"].min(),
        "close": g["close"].last(),
        "n_bars": g.size(),
    })
    out.index = pd.to_datetime(out.index)
    return out.sort_index()


def overnight_ohlc(df: pd.DataFrame) -> pd.DataFrame:
    """One row per trading_day: the pre-RTH (Globex overnight) segment of that
    SAME trading day -- i.e. all bars with is_rth==False belonging to trading_day
    d (which spans 18:00 ET d-1 through 09:30 ET d)."""
    o = df[~df["is_rth"]]
    g = o.groupby("trading_day", sort=True)
    out = pd.DataFrame({
        "open": g["open"].first(),
        "high": g["high"].max(),
        "low": g["low"].min(),
        "close": g["close"].last(),
        "n_bars": g.size(),
    })
    out.index = pd.to_datetime(out.index)
    return out.sort_index()


def wilders_tr(ohlc: pd.DataFrame) -> pd.Series:
    """Wilder's TR using the immediately preceding row's close in THIS frame
    (no roll exclusion -- see module docstring)."""
    h, l, c = ohlc["high"].to_numpy(), ohlc["low"].to_numpy(), ohlc["close"].to_numpy()
    prev_c = np.empty(len(ohlc))
    prev_c[0] = np.nan
    prev_c[1:] = c[:-1]
    tr = np.maximum.reduce([h - l, np.abs(h - prev_c), np.abs(l - prev_c)])
    return pd.Series(tr, index=ohlc.index, name="TR")


def range_series(ohlc: pd.DataFrame) -> pd.Series:
    """Plain high-low range (no prior-close term) -- used for the overnight and
    RTH sub-session ranges, where a Wilder gap-term against the OTHER
    sub-session's close would mix the two segments' price levels."""
    return (ohlc["high"] - ohlc["low"]).rename("range")


if __name__ == "__main__":
    df = load_raw()
    print(f"rows: {len(df)}  span: {df['time'].min()} -> {df['time'].max()}")
    print(f"trading days: {df['trading_day'].nunique()}")
    daily = daily_ohlc(df)
    print(f"daily bar-count distribution:\n{daily['n_bars'].describe()}")
    print(f"days with n_bars < 20: {(daily['n_bars'] < 20).sum()}")
    rth = rth_ohlc(df)
    print(f"\nRTH sessions: {len(rth)}")
    print(f"RTH bar-count distribution:\n{rth['n_bars'].describe()}")
    on = overnight_ohlc(df)
    print(f"\novernight sessions: {len(on)}")
    print(f"overnight bar-count distribution:\n{on['n_bars'].describe()}")
    print(f"\nH==L degenerate bars (full panel): {(df['high'] == df['low']).sum()} / {len(df)}")
