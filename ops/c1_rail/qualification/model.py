"""Immutable source/path contracts. These records never represent live settlement."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from math import isfinite
from zoneinfo import ZoneInfo

from c1_signal_daemon.feed import Bar

LEG_IDS = ('aegis_6j', 'dj30_mym_p250', 'vanguard_mgc', 'orb_mnq_v7')
ET = ZoneInfo('America/New_York')


def aware(value: datetime) -> None:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError('aware timestamp required')


def positive_int(value: int, label: str) -> None:
    if type(value) is not int or value <= 0:
        raise ValueError(f'{label} must be a positive integer')


def _bars(instant, bars):
    if type(bars) is not tuple or not bars:
        raise ValueError('nonempty immutable bar tuple required')
    if any(type(row) is not tuple or len(row) != 2 for row in bars):
        raise ValueError('immutable bar pairs required')
    keys = [leg for leg, _ in bars]
    if len(keys) != len(set(keys)) or not set(keys) <= set(LEG_IDS):
        raise ValueError('unknown or duplicate leg')
    for _, bar in bars:
        if not isinstance(bar, Bar) or bar.ts != instant:
            raise ValueError('bar/source time mismatch')
        if not all(isfinite(x) for x in (bar.open, bar.high, bar.low, bar.close, bar.volume)):
            raise ValueError('nonfinite bar')
        if not 0 < bar.low <= min(bar.open, bar.close) <= max(bar.open, bar.close) <= bar.high:
            raise ValueError('invalid OHLC')


@dataclass(frozen=True)
class SessionSchedule:
    cutoff: datetime
    flatten_start: datetime
    own_flat_deadline: datetime

    def __post_init__(self):
        for instant in (self.cutoff, self.flatten_start, self.own_flat_deadline):
            aware(instant)
        if not self.cutoff < self.flatten_start < self.own_flat_deadline:
            raise ValueError('schedule order')
        if self.own_flat_deadline - self.cutoff != timedelta(minutes=15) or self.own_flat_deadline - self.flatten_start != timedelta(minutes=5):
            raise ValueError('schedule differs from accepted buffers')


@dataclass(frozen=True)
class SourceBar:
    source_bar_time: datetime
    bars: tuple[tuple[str, Bar], ...]

    def __post_init__(self):
        aware(self.source_bar_time)
        if self.source_bar_time.minute % 15 or self.source_bar_time.second or self.source_bar_time.microsecond:
            raise ValueError('source must be on M15 grid')
        _bars(self.source_bar_time, self.bars)


@dataclass(frozen=True)
class SourceSession:
    session_id: str
    source_session_date: date
    bars: tuple[SourceBar, ...]
    schedule: SessionSchedule

    def __post_init__(self):
        if not self.session_id or not self.bars or type(self.bars) is not tuple:
            raise ValueError('session requires identity and immutable bars')
        times = [bar.source_bar_time for bar in self.bars]
        if any(a >= b for a, b in zip(times, times[1:])):
            raise ValueError('source bars not strictly ordered')
        if self.schedule.own_flat_deadline.astimezone(ET).date() != self.source_session_date:
            raise ValueError('schedule/source session mismatch')
        for instant in times:
            local = instant.astimezone(ET)
            session_date = local.date() + timedelta(days=int(local.hour >= 18))
            if session_date != self.source_session_date:
                raise ValueError('bar/source session mismatch')


@dataclass(frozen=True)
class PathBar:
    path_time: datetime
    source_bar_time: datetime
    source_session_date: date
    source_time_et: datetime
    bars: tuple[tuple[str, Bar], ...]

    def __post_init__(self):
        aware(self.path_time)
        aware(self.source_bar_time)
        aware(self.source_time_et)
        if self.source_time_et != self.source_bar_time.astimezone(ET):
            raise ValueError('source ET identity mismatch')
        _bars(self.source_bar_time, self.bars)


@dataclass(frozen=True)
class PathSession:
    occurrence: int
    path_session_date: date
    source: SourceSession
    bars: tuple[PathBar, ...]
    block_start: bool
    block_end: bool

    def __post_init__(self):
        if type(self.bars) is not tuple or type(self.occurrence) is not int or self.occurrence < 0 or not self.bars:
            raise ValueError('path occurrence requires bars')
        if len(self.bars) != len(self.source.bars):
            raise ValueError('source bars must not be dropped or imputed')
        for mapped, original in zip(self.bars, self.source.bars):
            if (mapped.source_bar_time != original.source_bar_time or mapped.bars != original.bars
                    or mapped.source_session_date != self.source.source_session_date):
                raise ValueError('source metadata changed')
        if any(a.path_time >= b.path_time for a, b in zip(self.bars, self.bars[1:])):
            raise ValueError('path times must increase')


@dataclass(frozen=True)
class EdgeState:
    positions: tuple[tuple[str, int], ...]
    working_orders: tuple[tuple[str, int], ...]
    reservations: tuple[tuple[str, int], ...]

    def __post_init__(self):
        for rows in (self.positions, self.working_orders, self.reservations):
            if type(rows) is not tuple or any(type(row) is not tuple or len(row)!=2 for row in rows) or len(rows) != 4 or {k for k, _ in rows} != set(LEG_IDS):
                raise ValueError('edge proof must enumerate exactly four legs')
            if any(type(v) is not int or v < 0 for _, v in rows):
                raise ValueError('gross nonnegative counts required')

    @property
    def is_flat(self):
        return all(value == 0 for rows in (self.positions, self.working_orders, self.reservations) for _, value in rows)


@dataclass(frozen=True)
class SessionRecord:
    occurrence: int
    path_session_date: date
    source_session_id: str
    pnl: float
    intraday_low: float
    fills: int
    flat_before_deadline: bool
    start_edge: EdgeState
    end_edge: EdgeState

    def __post_init__(self):
        if not isfinite(self.pnl) or not isfinite(self.intraday_low) or self.intraday_low > 0:
            raise ValueError('finite P&L and nonpositive excursion required')
        if type(self.fills) is not int or self.fills < 0:
            raise ValueError('fills must be nonnegative')


@dataclass(frozen=True)
class ReplayEvent:
    path_time: datetime
    kind: str
    leg_id: str
    detail: str = ''


@dataclass(frozen=True)
class ReplayResult:
    sessions: tuple[SessionRecord, ...]
    events: tuple[ReplayEvent, ...]

    def __post_init__(self):
        if type(self.sessions) is not tuple or any(type(row) is not SessionRecord for row in self.sessions):
            raise ValueError('immutable typed session records required')
        if type(self.events) is not tuple or any(type(row) is not ReplayEvent for row in self.events):
            raise ValueError('immutable typed replay events required')


@dataclass(frozen=True)
class PathOutcome:
    status: str
    sessions_to_pass: int | None
    failure_reason: str | None
    diagnostics: tuple[tuple[str, str], ...]

    def __post_init__(self):
        if self.status not in ('PASS', 'FAILURE', 'UNRESOLVED'):
            raise ValueError('unknown outcome status')
        if self.status == 'PASS':
            if type(self.sessions_to_pass) is not int or self.sessions_to_pass < 0 or self.failure_reason is not None:
                raise ValueError('PASS requires finite nonnegative session count and no failure')
        elif self.sessions_to_pass is not None or not self.failure_reason:
            raise ValueError('nonpass is T=infinity with reason')
        if type(self.diagnostics) is not tuple or any(type(row) is not tuple or len(row)!=2 for row in self.diagnostics) or any(type(k) is not str or type(v) is not str for k, v in self.diagnostics):
            raise ValueError('immutable string diagnostics required')
