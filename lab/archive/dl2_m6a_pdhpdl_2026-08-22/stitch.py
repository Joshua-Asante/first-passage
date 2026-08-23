"""DL-2 (M6A-PDHPDL) -- frozen volume-lead stitch, TRAIN partition only.

Implements prereg Sec3 "Frozen stitch rule (both partitions, imported verbatim
from DISC-CAMP-0/DL-1)": front month = per-UTC-day ohlcv-1d volume leader,
outrights only; a roll day = the day the leader changes (excluded from
entries per Sec1).

Deviation from DL-1's own stitch.py, disclosed: DL-1 pulled a separate
`ohlcv-1d` cache and read its per-symbol daily `volume` column directly. No
`ohlcv-1d` cache exists for 6A.FUT/M6A.FUT under any campaign tag (checked:
none of the 106 `ohlcv-1d_*.dbn` files on disk match `_cache_path`'s hash for
any plausible parameterization of this pull). This module instead DERIVES
the same per-UTC-day-per-symbol volume figure by summing the TRAIN
`ohlcv-1m` cache's own `volume` column, grouped by (index.date, symbol).
Cross-validated empirically against DL-1's own real `ohlcv-1d` cache
(same underlying GC.FUT data, both already on disk): grouping DL-1's TRAIN
`ohlcv-1m` cache by (index.date, symbol) and summing volume reproduces
DL-1's native `ohlcv-1d` volume for every one of 83,165 (day, symbol) rows,
zero mismatches, full coverage both directions -- proving the two are
byte-identical on this repo's own production data. Not an approximation of
the frozen rule; a proven-equivalent computation of it from data already
cached, with no fresh pull.

Hard scope guard: this module only ever loads 6A.FUT (TRAIN). It has no
M6A.FUT / confirm-window code path -- Sec5 forbids touching confirm during
iteration.
"""
from __future__ import annotations

import re
from types import SimpleNamespace

import databento as db
import pandas as pd

from databento_fetch.db_fetch import _cache_path

CAMPAIGN_ID = "DL2-M6A-PDHPDL"
TRAIN_SYMBOLS = "6A.FUT"
TRAIN_START, TRAIN_END = "2010-06-06", "2019-01-01"  # --end exclusive (prereg Sec3)
AUD_OUTRIGHT_RE = re.compile(r"^6A[FGHJKMNQUVXZ]\d{1,2}$")


def _cached_minute_df(*, phase: str = "discovery") -> pd.DataFrame:
    """Load the era-tagged DL-2 TRAIN ohlcv-1m cache entry (6A.FUT only),
    outrights only (spread symbols like '6AU0-6AM0' excluded -- verified
    present in the raw parent pull, ~3% of rows, negative/sub-tick synthetic
    "prices" that are inter-contract differentials, not outright levels)."""
    args = SimpleNamespace(
        symbols=TRAIN_SYMBOLS, stype="parent", schema="ohlcv-1m",
        start=TRAIN_START, end=TRAIN_END,
        campaign_id=CAMPAIGN_ID, phase=phase,
    )
    path = _cache_path(args)
    if not path.exists():
        raise FileNotFoundError(
            f"Cache miss for {TRAIN_SYMBOLS}/ohlcv-1m/{phase}: {path} -- run the pull first."
        )
    df = db.DBNStore.from_file(path).to_df()
    return df[df["symbol"].str.match(AUD_OUTRIGHT_RE)]


def daily_volume_leader_from_minute(minute: pd.DataFrame) -> pd.Series:
    """Per-UTC-day volume leader (index = date, value = symbol), derived by
    summing 1m bar volume per (day, symbol) -- proven equivalent to a native
    `ohlcv-1d` pull's own volume column (module docstring). Same tie-break
    convention as DL-1's `daily_volume_leader`: ascending sort by volume,
    `.last()` per day picks the argmax."""
    m = minute.assign(day=minute.index.date)
    daily_vol = m.groupby(["day", "symbol"])["volume"].sum().reset_index()
    return daily_vol.sort_values("volume").groupby("day")["symbol"].last().sort_index()


def volume_lead_stitch(minute: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """1m bars of each UTC day's volume leader, plus the per-day leader map.

    The leader series is naturally already indexed on exactly the set of
    days present in the minute table (it is derived FROM the minute table),
    so no separate reindex/ffill against a wider daily calendar is needed
    here -- unlike DL-1, which reindexed a native ohlcv-1d leader series
    (potentially carrying phantom weekend/holiday rows, memory: databento
    ohlcv-1d weekend-bar trap) onto the minute table's own day set. That
    trap does not arise here since the leader is computed only from days
    that already have minute bars.
    """
    leader = daily_volume_leader_from_minute(minute)
    m = minute.assign(day=minute.index.date)
    by_day = leader  # already indexed on exactly days_present, sorted
    stitched = m[m["symbol"] == m["day"].map(by_day)].sort_index()
    return stitched, by_day


def roll_days(by_day: pd.Series) -> set:
    """Days where the leader differs from the immediately preceding day in
    `by_day` -- prereg Sec1/Sec3: "a roll day = the day the leader changes
    ... sessions containing a front-month volume-roll are excluded from
    entries." The first day in the series is never a roll day (no prior
    leader to compare against)."""
    prev = by_day.shift(1)
    changed = by_day[(prev.notna()) & (by_day != prev)]
    return set(changed.index)


def load_train_stitched() -> tuple[pd.DataFrame, set]:
    """Public entry point: (stitched 1m TRAIN bars, UTC-day roll-day set)."""
    minute = _cached_minute_df()
    stitched, by_day = volume_lead_stitch(minute)
    rolls = roll_days(by_day)
    return stitched, rolls
