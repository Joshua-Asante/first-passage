"""DL-1 (MGC-ORC) — frozen volume-lead stitch, TRAIN partition only.

Implements prereg Sec3 "Frozen stitch rule (both partitions, imported verbatim
from the family's own frozen precedent, DISC-CAMP-0 manifest params)":
front month = per-UTC-day ohlcv-1d volume leader, outrights only; a roll day
= the day the leader changes (excluded from entries per Sec1).

The leader-selection and reindex/ffill logic below is the DISC-CAMP-0
`series.py` implementation (git show c783533:lab/analysis/disccamp0_gc_2010_18/series.py),
adapted from 1h to 1m bars and re-pointed at the DL-1 cache-tag/window. No
back-adjustment anywhere (prereg Sec3): all levels are the actual contract's
own prices.

Hard scope guard: this module only ever loads GC.FUT (TRAIN). It has no
MGC.FUT / confirm-window code path -- Sec5 forbids touching confirm during
iteration.
"""
from __future__ import annotations

import re
from types import SimpleNamespace

import databento as db
import pandas as pd

from databento_fetch.db_fetch import _cache_path

CAMPAIGN_ID = "DL1-MGC-ORC"
TRAIN_SYMBOLS = "GC.FUT"
TRAIN_START, TRAIN_END = "2010-06-06", "2019-01-01"  # --end exclusive (prereg Sec3)
GC_OUTRIGHT_RE = re.compile(r"^GC[FGHJKMNQUVXZ]\d{1,2}$")


def _cached_df(schema: str, *, phase: str = "discovery") -> pd.DataFrame:
    """Load the era-tagged DL-1 TRAIN cache entry (GC.FUT only), outrights only."""
    args = SimpleNamespace(
        symbols=TRAIN_SYMBOLS, stype="parent", schema=schema,
        start=TRAIN_START, end=TRAIN_END,
        campaign_id=CAMPAIGN_ID, phase=phase,
    )
    path = _cache_path(args)
    if not path.exists():
        raise FileNotFoundError(
            f"Cache miss for {TRAIN_SYMBOLS}/{schema}/{phase}: {path} -- run the pull first."
        )
    df = db.DBNStore.from_file(path).to_df()
    return df[df["symbol"].str.match(GC_OUTRIGHT_RE)]


def daily_volume_leader(daily: pd.DataFrame) -> pd.Series:
    """Per-UTC-day volume leader (index = date, value = symbol).

    `sort_values("volume").groupby("day")["symbol"].last()` picks the
    max-volume symbol per day (ascending sort -> last row is the argmax).
    """
    d = daily.assign(day=daily.index.date)
    return d.sort_values("volume").groupby("day")["symbol"].last().sort_index()


def volume_lead_stitch(minute: pd.DataFrame, daily: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """1m bars of each UTC day's volume leader, plus the per-day leader map.

    The leader series is reindexed onto the SET OF DAYS PRESENT IN THE MINUTE
    TABLE (not the daily table) before ffill -- this is what makes phantom
    ohlcv-1d weekend/holiday rows harmless (memory: databento ohlcv-1d
    weekend-bar trap): a day with no minute bars never enters `by_day`.
    """
    leader = daily_volume_leader(daily)
    m = minute.assign(day=minute.index.date)
    days_present = sorted(set(m["day"]))
    by_day = leader.reindex(days_present).ffill()
    stitched = m[m["symbol"] == m["day"].map(by_day)].sort_index()
    return stitched, by_day


def roll_days(by_day: pd.Series) -> set:
    """Days where the leader differs from the immediately preceding day in
    `by_day` (itself already restricted to days with minute bars) -- prereg
    Sec1: "a roll day = the day the leader changes ... sessions containing a
    front-month volume-roll are excluded from entries." The first day in the
    series is never a roll day (no prior leader to compare against)."""
    prev = by_day.shift(1)
    changed = by_day[(prev.notna()) & (by_day != prev)]
    return set(changed.index)


def load_train_stitched() -> tuple[pd.DataFrame, set]:
    """Public entry point: (stitched 1m TRAIN bars, roll-day set)."""
    daily = _cached_df("ohlcv-1d")
    minute = _cached_df("ohlcv-1m")
    stitched, by_day = volume_lead_stitch(minute, daily)
    rolls = roll_days(by_day)
    return stitched, rolls
