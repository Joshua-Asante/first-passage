"""Bar loading and the development/holdout split (spec: Data and holdout, per the 10-30 direction).

Input is a CME BAR EXPORT v0.2 file (decoded by ``core/bar_export_loader``) or a derived
``bar_data/<SYMBOL>_M15.csv`` panel. The TV ``1!`` continuous series is used as exported; no roll
is reconstructed. Times become America/New_York bar opens. Duplicate or malformed bars abort.
"""
from __future__ import annotations

import hashlib
import math
from pathlib import Path

import pandas as pd

from builder.instruments import INSTRUMENTS

NY = "America/New_York"
HOLDOUT_SHARE = 0.30


def file_sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_bars(path: Path, symbol: str) -> pd.DataFrame:
    inst = INSTRUMENTS[symbol]
    head = Path(path).open(encoding="utf-8-sig").readline()
    if "Signal" in head:
        from bar_export_loader import parse_bar_export_with_meta
        raw = pd.read_csv(path, usecols=["Type", "Signal"], encoding="utf-8-sig")
        epochs = raw.loc[raw["Type"].str.startswith("Entry"), "Signal"].str.split("|").str[0]
        if epochs.duplicated().any():  # the shared parser keeps the last duplicate; the builder aborts
            raise ValueError(f"{path}: duplicate bar timestamps in the export")
        df, meta = parse_bar_export_with_meta(path, symbol=symbol)
        if meta is None or meta["ticker"] != inst.ticker or not math.isclose(meta["mintick"], inst.tick) \
                or not math.isclose(meta["pointvalue"], inst.point_value) or str(meta["timeframe"]) != "15":
            raise ValueError(f"{path}: export metadata does not match builder.instruments[{symbol}] / 15m")
    else:
        df = pd.read_csv(path)
    if df["time"].duplicated().any():
        raise ValueError(f"{path}: duplicate bar timestamps")
    t = pd.to_datetime(df["time"], utc=True).dt.tz_convert(NY)
    out = pd.DataFrame({c: df[c].astype(float).to_numpy() for c in ("open", "high", "low", "close")}, index=t)
    out = out.sort_index()
    if ((out.index.minute % 15) != 0).any() or (out.index.second != 0).any():
        raise ValueError(f"{path}: bar opens are not on the 15m grid")
    lo, hi = out[["open", "close"]].min(axis=1), out[["open", "close"]].max(axis=1)
    if not ((out["low"] <= lo) & (hi <= out["high"])).all():
        raise ValueError(f"{path}: OHLC fails low <= open,close <= high")
    return out


def session_dates(bars: pd.DataFrame, symbol: str) -> list[str]:
    """Weekdays with a bar opening exactly at the instrument's session open."""
    so = INSTRUMENTS[symbol].session_open
    idx = bars.index
    m = (idx.strftime("%H:%M") == so) & (idx.weekday < 5)
    return sorted(set(idx[m].strftime("%Y-%m-%d")))


def split(dates: list[str], holdout_share: float = HOLDOUT_SHARE) -> tuple[list[str], list[str]]:
    """Development = first (1 - share) of sessions by date; holdout = the rest."""
    cut = int(round(len(dates) * (1 - holdout_share)))
    return dates[:cut], dates[cut:]
