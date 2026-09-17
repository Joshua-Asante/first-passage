"""Exact-byte source loading and explicit active-window coverage, before sampling."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timedelta
import hashlib
import io
from pathlib import Path

from c1_signal_daemon.feed import Bar
from .model import ET, LEG_IDS, SourceBar, SourceSession, aware


class PanelError(ValueError):
    pass


@dataclass(frozen=True)
class Exclusion:
    session_date: object
    reason: str
    detail: str


@dataclass(frozen=True)
class CoverageReport:
    sessions: tuple[SourceSession, ...]
    exclusions: tuple[Exclusion, ...]
    adjacent: tuple[bool, ...]


def load_bar_csv(path, expected_sha256, *, strip_crlf=False):
    """Read/hash/parse one byte snapshot; normalization is an explicit manifest rule."""
    raw = Path(path).read_bytes()
    digest_bytes = raw.replace(b'\r\n', b'\n') if strip_crlf else raw
    if hashlib.sha256(digest_bytes).hexdigest() != expected_sha256:
        raise PanelError('source digest mismatch')
    rows = csv.DictReader(io.StringIO(raw.decode('utf-8-sig')))
    if rows.fieldnames not in (['time','open','high','low','close','volume'], ['timestamp','open','high','low','close','volume']):
        raise PanelError('explicit time,OHLC,volume columns required')
    time_key = rows.fieldnames[0]
    result = []
    for row in rows:
        ts = datetime.fromisoformat(row[time_key].replace('Z', '+00:00'))
        aware(ts)
        bar = Bar(ts, *(float(row[key]) for key in ('open','high','low','close','volume')))
        SourceBar(ts, ((LEG_IDS[0], bar),))  # common OHLC/time validation
        if result and result[-1].ts >= ts:
            raise PanelError('duplicate or unordered source timestamp')
        result.append(bar)
    if not result:
        raise PanelError('empty source panel')
    return tuple(result)


def source_session_date(instant):
    aware(instant)
    local = instant.astimezone(ET)
    return local.date() + timedelta(days=int(local.hour >= 18))


def build_panel(panels, *, schedules, expected_dates, active, excluded_dates=()):
    """The source calendar supplies *all* expected dates, including all-flat days.

    ``active(leg, source_time)`` must be the evidence-bound Pine window predicate.
    Missing inactive observations are absent, never last-close filled. An omitted
    calendar date or a provider-wide gap cannot silently become a closure.
    """
    if set(panels) != set(LEG_IDS):
        raise PanelError('exact four-leg panels required')
    expected_dates = tuple(expected_dates)
    if not expected_dates or tuple(sorted(set(expected_dates))) != expected_dates:
        raise PanelError('unique ordered expected calendar dates required')
    denied = set(excluded_dates)
    if not denied <= set(expected_dates):
        raise PanelError('closure dates outside expected calendar')
    if any(day not in schedules for day in expected_dates if day not in denied):
        raise PanelError('source calendar coverage missing')
    lookup = {}
    grids = {day: set() for day in expected_dates}
    for leg, bars in panels.items():
        previous = None
        lookup[leg] = {}
        for bar in bars:
            SourceBar(bar.ts, ((leg, bar),))
            if previous is not None and previous >= bar.ts:
                raise PanelError('duplicate or unordered panel')
            previous = bar.ts
            day = source_session_date(bar.ts)
            if day not in grids:
                raise PanelError('bar outside declared source calendar')
            lookup[leg][bar.ts] = bar
            grids[day].add(bar.ts)
    accepted, exclusions, indices = [], [], []
    for index, day in enumerate(expected_dates):
        if day in denied:
            exclusions.append(Exclusion(day, 'source_calendar_closure', 'explicit typed source overlay'))
            continue
        grid = sorted(grids[day])
        if not grid:
            exclusions.append(Exclusion(day, 'missing_entire_session', 'all providers absent'))
            continue
        missing = [(leg, ts) for ts in grid for leg in LEG_IDS if active(leg, ts) and ts not in lookup[leg]]
        if missing:
            exclusions.append(Exclusion(day, 'missing_active_bar', ';'.join(f'{leg}@{ts.isoformat()}' for leg, ts in missing)))
            continue
        rows = tuple(SourceBar(ts, tuple((leg, lookup[leg][ts]) for leg in LEG_IDS if ts in lookup[leg])) for ts in grid)
        accepted.append(SourceSession(day.isoformat(), day, rows, schedules[day]))
        indices.append(index)
    # An exclusion is not compressed into adjacent bootstrap sessions.
    return CoverageReport(tuple(accepted), tuple(exclusions), tuple(b == a + 1 for a, b in zip(indices, indices[1:])))
