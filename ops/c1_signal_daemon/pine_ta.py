"""Incremental Pine-equivalent primitives for the fixed-book adapters (Track B).

Generic indicator arithmetic only — no strategy parameters, no edge. Each
class consumes one value per bar and returns the Pine built-in's value for
that bar (``None`` while Pine would return ``na``), matching:

* ``ta.sma`` — simple mean of the last ``length`` values.
* ``ta.ema`` — ``alpha = 2/(length+1)``, seeded with the first value.
* ``ta.rma`` — ``alpha = 1/length``, seeded with the SMA of the first ``length`` values.
* ``ta.stdev`` — population standard deviation (``biased = true`` default).
* ``ta.bb``   — SMA basis +/- mult x population stdev.
* ``ta.atr``  — RMA of true range; the first bar's TR is ``high - low``.
* ``ta.highest`` / ``ta.lowest`` — window extremes.
* ``math.round`` — half away from zero (Python's ``round`` is banker's).

Session helpers convert bar-open UTC timestamps to the filter clock the Pine
scripts use (``America/New_York`` inputs; exchange-timezone built-ins where a
script left the argument out).
"""
from __future__ import annotations

import math
from collections import deque
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
CT = ZoneInfo("America/Chicago")
UTC = ZoneInfo("UTC")


def pine_round(x: float) -> int:
    """Pine math.round: nearest integer, ties away from zero."""
    if x >= 0:
        return int(math.floor(x + 0.5))
    return -int(math.floor(-x + 0.5))


def tick_round(price: float, mintick: float) -> float:
    """Pine ``math.round(p / mintick) * mintick``."""
    return pine_round(price / mintick) * mintick


class Sma:
    def __init__(self, length: int) -> None:
        self.length = length
        self._win: deque[float] = deque(maxlen=length)
        self._sum = 0.0

    def update(self, value: float | None) -> float | None:
        if value is None:
            return None
        if len(self._win) == self.length:
            self._sum -= self._win[0]
        self._win.append(value)
        self._sum += value
        if len(self._win) < self.length:
            return None
        return self._sum / self.length


class Ema:
    def __init__(self, length: int) -> None:
        self.alpha = 2.0 / (length + 1)
        self.value: float | None = None

    def update(self, value: float | None) -> float | None:
        if value is None:
            return self.value
        if self.value is None:
            self.value = value
        else:
            self.value = self.alpha * value + (1.0 - self.alpha) * self.value
        return self.value


class Rma:
    def __init__(self, length: int) -> None:
        self.length = length
        self.alpha = 1.0 / length
        self.value: float | None = None
        self._seed = Sma(length)

    def update(self, value: float | None) -> float | None:
        if value is None:
            return self.value
        if self.value is None:
            self.value = self._seed.update(value)
        else:
            self.value = self.alpha * value + (1.0 - self.alpha) * self.value
        return self.value


class Stdev:
    """Population stdev over a window (Pine ta.stdev default biased=true)."""

    def __init__(self, length: int) -> None:
        self.length = length
        self._win: deque[float] = deque(maxlen=length)

    def update(self, value: float | None) -> float | None:
        if value is None:
            return None
        self._win.append(value)
        if len(self._win) < self.length:
            return None
        mean = sum(self._win) / self.length
        var = sum((v - mean) ** 2 for v in self._win) / self.length
        return math.sqrt(var) if var > 0 else 0.0


class BollingerBands:
    def __init__(self, length: int, mult: float) -> None:
        self.mult = mult
        self._sma = Sma(length)
        self._sd = Stdev(length)

    def update(self, value: float | None) -> tuple[float | None, float | None, float | None]:
        basis = self._sma.update(value)
        sd = self._sd.update(value)
        if basis is None or sd is None:
            return None, None, None
        return basis, basis + self.mult * sd, basis - self.mult * sd


class Atr:
    def __init__(self, length: int) -> None:
        self._rma = Rma(length)
        self._prev_close: float | None = None

    def update(self, high: float, low: float, close: float) -> float | None:
        if self._prev_close is None:
            tr = high - low
        else:
            tr = max(high - low, abs(high - self._prev_close), abs(low - self._prev_close))
        self._prev_close = close
        return self._rma.update(tr)


class Highest:
    def __init__(self, length: int) -> None:
        self.length = length
        self._win: deque[float] = deque(maxlen=length)

    def update(self, value: float) -> float | None:
        self._win.append(value)
        if len(self._win) < self.length:
            return None
        return max(self._win)


class Lowest:
    def __init__(self, length: int) -> None:
        self.length = length
        self._win: deque[float] = deque(maxlen=length)

    def update(self, value: float) -> float | None:
        self._win.append(value)
        if len(self._win) < self.length:
            return None
        return min(self._win)


class History:
    """Pine ``x[n]`` access for a series (``None`` before enough bars)."""

    def __init__(self, depth: int) -> None:
        self._win: deque = deque(maxlen=depth + 1)

    def push(self, value) -> None:
        self._win.append(value)

    def get(self, n: int = 0):
        if n >= len(self._win):
            return None
        return self._win[-1 - n]


# ── clocks ───────────────────────────────────────────────────────────────

def as_utc(ts: datetime) -> datetime:
    return ts if ts.tzinfo is not None else ts.replace(tzinfo=UTC)


def in_tz(ts: datetime, tz: ZoneInfo) -> datetime:
    return as_utc(ts).astimezone(tz)


def minute_of_day(ts: datetime, tz: ZoneInfo = ET) -> int:
    local = in_tz(ts, tz)
    return local.hour * 60 + local.minute


def date_key(ts: datetime, tz: ZoneInfo = ET) -> int:
    local = in_tz(ts, tz)
    return local.year * 10000 + local.month * 100 + local.day


def trading_day(ts: datetime, tz: ZoneInfo = ET, session_open_hour: int = 18) -> date:
    """CME ``time("D")`` day: the session that opens at 18:00 ET carries the NEXT date."""
    local = in_tz(ts, tz)
    shifted = local + timedelta(hours=24 - session_open_hour)
    return shifted.date()


US_MARKET_HOLIDAYS_2022_2027 = frozenset({
    # NYSE full-closure holidays (CME Globex runs a shortened session but publishes
    # no daily bar for the date on TradingView). Source: NYSE holiday calendar.
    20220117, 20220221, 20220415, 20220530, 20220620, 20220704, 20220905, 20221124, 20221226,
    20230102, 20230116, 20230220, 20230407, 20230529, 20230619, 20230704, 20230904, 20231123, 20231225,
    20240101, 20240115, 20240219, 20240329, 20240527, 20240619, 20240704, 20240902, 20241128, 20241225,
    20250101, 20250109, 20250120, 20250217, 20250418, 20250526, 20250619, 20250704, 20250901, 20251127, 20251225,
    20260101, 20260119, 20260216, 20260403, 20260525, 20260619, 20260703, 20260907, 20261126, 20261225,
    20270101, 20270118, 20270215, 20270326, 20270531, 20270618, 20270705, 20270906, 20271125, 20271224,
})


def tv_daily_key(ts: datetime, holidays: frozenset[int] = US_MARKET_HOLIDAYS_2022_2027,
                 tz: ZoneInfo = ET, session_open_hour: int = 18) -> date:
    """The daily bar a 15-minute bar belongs to on TradingView (``time("D")``).

    A CME session opens at 18:00 ET and carries the next calendar date. A US
    market holiday has NO daily bar on TradingView: the holiday's shortened
    session belongs to the next trading day's daily bar, so
    ``ta.change(time("D"))`` is 0 at the holiday-evening reopen. Evidence: the
    captured Vanguard export has no trade on the session after MLK,
    Presidents', Memorial, Labor Day and the 2026-07-03 observed holiday
    although the entry rule fires (its EOD flat latch resets only on a new
    daily bar), while it does trade on 2023-07-04, 2024-07-04 and 2024-12-26,
    whose daily bars begin at the prior evening's reopen.
    """
    key = trading_day(ts, tz, session_open_hour)
    while (key.year * 10000 + key.month * 100 + key.day) in holidays or key.weekday() >= 5:
        key = key + timedelta(days=1)
    return key


def pine_dayofweek(ts: datetime, tz: ZoneInfo) -> int:
    """Pine dayofweek: Sunday=1 ... Saturday=7."""
    local = in_tz(ts, tz)
    return (local.weekday() + 1) % 7 + 1


def parse_early_close_dates(text: str) -> frozenset[int]:
    cleaned = text.replace(" ", "").replace("\n", "")
    out = set()
    for tok in cleaned.split(","):
        if tok:
            out.add(int(tok))
    return frozenset(out)


# The early-close / holiday list every fixed-book Pine ships as its input default
# (derived from ops/calendars/cme_holiday_calendar_2022_2026.json; 2027 rows are
# unverified carry-over per the Pine tooltips).
EARLY_CLOSE_DATES_DEFAULT = parse_early_close_dates(
    "20220117,20220221,20220415,20220530,20220620,20220704,20220905,20221124,20221125,20221225,20221226,"
    "20230101,20230102,20230116,20230220,20230407,20230529,20230619,20230703,20230704,20230904,20231123,20231124,20231224,20231225,20231231,"
    "20240101,20240115,20240219,20240329,20240527,20240619,20240703,20240704,20240902,20241128,20241129,20241224,20241225,"
    "20250101,20250109,20250120,20250217,20250418,20250526,20250619,20250703,20250704,20250901,20251127,20251128,20251224,20251225,"
    "20260101,20260119,20260216,20260403,20260525,20260619,20260703,20260907,20261126,20261127,20261224,20261225,"
    "20270118,20270215,20270531,20270618,20270705,20270906,20271125,20271126,20271223,20271224"
)
