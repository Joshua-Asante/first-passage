"""Build the WTI futures curve-state panel for the Helios F1 probe.

Pulls CME crude daily bars (CL.c.0 front, CL.c.1 second; calendar continuous)
from Databento, builds a daily panel with the curve-state label, and caches it.

Curve state (day T close): backwardation == close(CL.c.0) > close(CL.c.1).
This is a same-day calendar spread, so it is robust to contract rolls. The
roll itself (CL.c.0's underlying contract changing) is recorded via the
``iid_c0`` (instrument_id) column so the F1 return builder can drop
roll-spanning windows.

LEAK DISCIPLINE (brief forbidden move #1): this module only builds the panel.
The one-bar lag between the curve-state signal and the forward-return window is
applied in ``f1_mechanism.py`` (``state.shift(1)``), never here.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd

from .databento_client import fetch_ohlcv_1d

_PKG = Path(__file__).resolve().parent
_DATA = _PKG / "data"
_CACHE = _DATA / "cl_curve_daily.csv"
_MANIFEST = _DATA / "SHA256SUMS"

# Panel window narrowed to 2020-01 per Joshua (2026-06-06): covers the 2020
# super-contango crash, the 2021-22 backwardation, and the 2025-26 Hormuz
# backwardation. The 2014-15 contango glut is intentionally out of scope.
# End is exclusive per the API.
DEFAULT_START = "2020-01-01"
DEFAULT_END = "2026-06-06"


def _to_date(ts: pd.Series) -> pd.Series:
    return pd.to_datetime(ts).dt.tz_localize(None).dt.normalize()


def build_curve_panel(start: str = DEFAULT_START, end: str = DEFAULT_END) -> pd.DataFrame:
    """Fetch and assemble the daily curve panel (no caching)."""
    raw = fetch_ohlcv_1d(["CL.c.0", "CL.c.1"], start, end)
    raw = raw.copy()
    raw["date"] = _to_date(raw["ts_event"])

    c0 = raw[raw["symbol"] == "CL.c.0"][["date", "close", "instrument_id"]]
    c0 = c0.rename(columns={"close": "close_c0", "instrument_id": "iid_c0"})
    c1 = raw[raw["symbol"] == "CL.c.1"][["date", "close"]]
    c1 = c1.rename(columns={"close": "close_c1"})

    df = c0.merge(c1, on="date", how="inner").sort_values("date").reset_index(drop=True)
    df["spread"] = df["close_c0"] - df["close_c1"]
    # state: 1 = backwardation (front > second), 0 = contango. Ties (spread==0)
    # are rare and counted as contango (not backwardation) — conservative for a
    # concept that must SHOW a backwardation effect.
    df["state"] = (df["spread"] > 0).astype(int)
    df["roll"] = (df["iid_c0"] != df["iid_c0"].shift(1)).astype(int)
    df.loc[0, "roll"] = 0
    return df


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def load_curve_panel(
    *, rebuild: bool = False, start: str = DEFAULT_START, end: str = DEFAULT_END
) -> pd.DataFrame:
    """Load the cached panel, fetching + caching on first use or ``rebuild``."""
    if _CACHE.exists() and not rebuild:
        df = pd.read_csv(_CACHE, parse_dates=["date"])
        return df
    df = build_curve_panel(start, end)
    _DATA.mkdir(exist_ok=True)
    df.to_csv(_CACHE, index=False)
    # Tracked-manifest hygiene (house pattern): hash the gitignored cache.
    _MANIFEST.write_text(f"{_sha256(_CACHE)}  {_CACHE.name}\n", encoding="utf-8")
    return df


def regime_report(df: pd.DataFrame, min_episode_len: int = 10) -> str:
    """Per-year backwardation/contango day counts + major contiguous episodes."""
    out: list[str] = []
    n = len(df)
    nb = int(df["state"].sum())
    nc = n - nb
    out.append(
        f"Panel: {n} trading days  {df['date'].min().date()} -> {df['date'].max().date()}"
    )
    out.append(f"  Backwardation days: {nb} ({nb/n*100:.1f}%)   Contango days: {nc} ({nc/n*100:.1f}%)")
    out.append("")
    out.append("Per-year day counts (backw / contango):")
    yr = df.assign(year=df["date"].dt.year).groupby("year")["state"].agg(["sum", "count"])
    for year, row in yr.iterrows():
        b = int(row["sum"]); tot = int(row["count"]); c = tot - b
        out.append(f"  {year}: backw {b:>4} / contango {c:>4}  (n={tot})")
    out.append("")
    out.append(f"Major contiguous episodes (>= {min_episode_len} days):")
    # run-length encode the state series
    state = df["state"].to_numpy()
    dates = df["date"].to_numpy()
    i = 0
    while i < n:
        j = i
        while j + 1 < n and state[j + 1] == state[i]:
            j += 1
        run = j - i + 1
        if run >= min_episode_len:
            lbl = "BACKWARDATION" if state[i] == 1 else "contango"
            out.append(
                f"  {pd.Timestamp(dates[i]).date()} -> {pd.Timestamp(dates[j]).date()}  "
                f"{lbl:<13} ({run} days)"
            )
        i = j + 1
    return "\n".join(out)


if __name__ == "__main__":
    panel = load_curve_panel(rebuild=True)
    print(regime_report(panel))
