"""MNQ-SIZEDIV-1 statistic + calendar + slot-return library.

Frozen with DESIGN_FREEZE.md (same commit) BEFORE any trades data was pulled.
Quarantine rule embodied here: Stage-1 code paths read the panel's `time`
column only (calendar); price columns are touched exclusively by the Stage-2+
slot-return path.
"""
from __future__ import annotations

from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

ET = ZoneInfo("America/New_York")
RTH_BARS = 26  # 09:30 .. 15:45 M15 bar-open stamps
RTH_START = (9, 30)
RTH_END = (16, 0)  # exclusive


# ---------------------------------------------------------------- panel side

def _panel_times_et(path: str | Path) -> pd.Series:
    """Panel `time` column only (Stage-1-safe: no price columns loaded)."""
    t = pd.read_csv(path, usecols=["time"])["time"]
    return pd.to_datetime(t, utc=True).dt.tz_convert(ET)


def load_calendar(path: str | Path) -> pd.DataFrame:
    """Per-date RTH bar count from the panel. Full session == RTH_BARS bars."""
    et = _panel_times_et(path)
    tod = et.dt.hour * 60 + et.dt.minute
    rth = (tod >= RTH_START[0] * 60 + RTH_START[1]) & (tod < RTH_END[0] * 60 + RTH_END[1])
    dates = et.dt.date[rth]
    counts = dates.value_counts().sort_index()
    out = pd.DataFrame({"date": counts.index, "rth_bars": counts.values})
    out["full"] = out["rth_bars"] == RTH_BARS
    return out


def load_slot_returns(path: str | Path) -> pd.DataFrame:
    """Stage-2+ ONLY. Per full session: r1 = ln(open12:45/open09:30),
    r2 = ln(close15:45bar/open12:45), in bp."""
    df = pd.read_csv(path, usecols=["time", "open", "close"])
    et = pd.to_datetime(df["time"], utc=True).dt.tz_convert(ET)
    df = df.assign(et=et, date=et.dt.date, hm=et.dt.hour * 100 + et.dt.minute)
    o930 = df[df["hm"] == 930].set_index("date")["open"]
    o1245 = df[df["hm"] == 1245].set_index("date")["open"]
    c1545 = df[df["hm"] == 1545].set_index("date")["close"]
    cal = load_calendar(path).set_index("date")
    full = cal.index[cal["full"]]
    idx = full.intersection(o930.index).intersection(o1245.index).intersection(c1545.index)
    r1 = (np.log(o1245.loc[idx] / o930.loc[idx]) * 1e4).rename("r1_bp")
    r2 = (np.log(c1545.loc[idx] / o1245.loc[idx]) * 1e4).rename("r2_bp")
    return pd.concat([r1, r2], axis=1).reset_index().rename(columns={"index": "date"})


# --------------------------------------------------------------- trades side

def _to_et_index(df: pd.DataFrame) -> pd.Series:
    """Event timestamps as tz-aware ET, from `ts_event` column or the index."""
    if "ts_event" in df.columns:
        ts = pd.to_datetime(df["ts_event"], utc=True)
    else:
        ts = pd.to_datetime(df.index, utc=True).to_series(index=df.index)
    return ts.dt.tz_convert(ET) if hasattr(ts, "dt") else ts.tz_convert(ET)


def rth_mask(et: pd.Series) -> pd.Series:
    tod = et.dt.hour * 60 + et.dt.minute
    return (tod >= RTH_START[0] * 60 + RTH_START[1]) & (tod < RTH_END[0] * 60 + RTH_END[1])


def session_stats(trades: pd.DataFrame) -> pd.DataFrame:
    """Per-session aggregates from a trades chunk (RTH prints only).

    Expects columns: price, size, side (values 'A'/'B'/'N'). Returns one row per
    date: V_B/V_A/N_B/N_A, n_prints (all RTH), n_signable, span_h, plus the
    tick-rule tallies agree/disagree (zero-change prints dropped).
    """
    et = _to_et_index(trades)
    m = rth_mask(et)
    df = trades.loc[m.values if hasattr(m, "values") else m].copy()
    df["date"] = et[m].dt.date.values
    df["side"] = df["side"].astype(str)
    df["price"] = df["price"].astype(float)
    df["size"] = df["size"].astype("int64")

    rows = []
    for date, g in df.groupby("date", sort=True):
        sig = g[g["side"].isin(("A", "B"))]
        buy = sig["side"].to_numpy() == "B"
        v_b = int(sig["size"].to_numpy()[buy].sum())
        v_a = int(sig["size"].to_numpy()[~buy].sum())
        # tick rule vs side, zero-changes dropped (within-session only)
        p = sig["price"].to_numpy()
        s = np.where(buy, 1, -1)
        dp = np.sign(np.diff(p))
        nz = dp != 0
        agree = int((dp[nz] == s[1:][nz]).sum())
        disagree = int(nz.sum()) - agree
        rows.append(
            dict(date=date, V_B=v_b, V_A=v_a, N_B=int(buy.sum()), N_A=int((~buy).sum()),
                 n_prints=len(g), n_signable=len(sig), tick_agree=agree, tick_disagree=disagree)
        )
    out = pd.DataFrame(rows)
    # per-date print span in hours (first..last RTH print)
    span = (
        pd.DataFrame({"date": df["date"].values, "et": et[m].values})
        .groupby("date")["et"].agg(["min", "max"])
    )
    span_h = (span["max"] - span["min"]).dt.total_seconds() / 3600.0
    out = out.merge(span_h.rename("span_h").reset_index(), on="date", how="left")
    return out


def combine_stats(parts: list[pd.DataFrame]) -> pd.DataFrame:
    """Sum per-session aggregates across chunk/file boundaries."""
    allp = pd.concat(parts, ignore_index=True)
    agg = allp.groupby("date", sort=True).agg(
        V_B=("V_B", "sum"), V_A=("V_A", "sum"), N_B=("N_B", "sum"), N_A=("N_A", "sum"),
        n_prints=("n_prints", "sum"), n_signable=("n_signable", "sum"),
        tick_agree=("tick_agree", "sum"), tick_disagree=("tick_disagree", "sum"),
        span_h=("span_h", "max"),
    ).reset_index()
    return agg


def sizediv(stats: pd.DataFrame) -> pd.DataFrame:
    """I_vw, I_cw and A = I_vw − I_cw per session (guarding zero denominators)."""
    s = stats.copy()
    vden = (s["V_B"] + s["V_A"]).replace(0, np.nan)
    nden = (s["N_B"] + s["N_A"]).replace(0, np.nan)
    s["I_vw"] = (s["V_B"] - s["V_A"]) / vden
    s["I_cw"] = (s["N_B"] - s["N_A"]) / nden
    s["A"] = s["I_vw"] - s["I_cw"]
    return s
