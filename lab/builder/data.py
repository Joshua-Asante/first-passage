"""Strict BAR EXPORT v0.2 reader, the book file, the frozen calendar and the date-pinned split.

The builder reads raw TradingView BAR EXPORT v0.2 List-of-Trades files only, with its own
parser. It does not use ``core/bar_export_loader``, which skips undecodable rows and keeps the
last of duplicate bars; derived ``bar_data`` panels come from that producer and are refused.
Every rule below aborts the load; none skips, defaults or warns (invariants I-B1..I-B13).

- Header has ``Trade number``, ``Type``, ``Signal``, ``Price USD``; every row's Type is one of
  the four List-of-Trades types. Exit rows carry no bar of their own and are otherwise ignored.
- Every Entry Signal matches the full 17-field v0.2 grammar
  ``epoch|O|H|L|C|V|time_close|dow|sess|ticker|type|qCcy|bCcy|mintick|pointvalue|tz|tf``.
- Entry price equals the encoded close; low <= open, close <= high; prices on the mintick grid.
- Instrument constants equal ``builder.instruments`` on every row, with timeframe ``15``, and each
  bar's time_close is its open + 15 minutes.
- Bar opens are on the 15m grid, unique, and strictly increase with trade number.
- Missing 15m bars are not refused: TradingView omits a bar in which nothing traded. The
  summary counts weekdays with day-window bars ([session open, 17:00) ET) but no open bar
  (``days_without_open_bar``; not sessions), session days with a gap inside the window
  (``gap_sessions``), early-closing sessions and every gap between bars. ``builder.compile``
  treats a missing bar as a no-trade interval (W1 contract v5 §3).

The TV ``1!`` continuous series is used as exported; no roll is reconstructed.

The split is pinned by date per instrument: development = dev_start <= sessions <= dev_end,
holdout = dev_end < sessions <= holdout_end; other sessions are in neither. Every given end must
be a session date of the loaded export, so a refreshed export cannot move a session across a
boundary. ``dev_start`` is optional (R1's specs predate it); bars before it may feed indicator
warm-up only.

The calendar (``ops/calendars/cme_holiday_calendar_2022_2026.json``) is read for exactly
``CALENDAR_FIELDS``: the schema, the coverage window, every ``entries[].date`` and every entry's
``*_status`` fields. An entry date is closed (not traded) only when at least one recorded status
is not ``NORMAL``; a row whose every status is ``NORMAL`` is informational and leaves the session
in place (operator decision 2026-11-03, option B on PR #1045). An entry with no ``*_status``
field, or a status outside ``CALENDAR_STATUSES``, aborts the load. Every evaluated session must
lie inside the coverage window.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

from builder.instruments import DAY_END, EXPORT_TZ, INSTRUMENTS

NY = "America/New_York"
CALENDAR_SCHEMA = "cme_holiday_calendar/v1"
CALENDAR_FIELDS = ("schema", "coverage_start", "coverage_end", "entries[].date", "entries[].*_status")
# the status values the admitted calendar uses (cme_holiday_calendar_2022_2026.json); nothing else loads
CALENDAR_STATUSES = frozenset({"EARLY_CLOSE", "FULL_CLOSURE", "NORMAL"})
BAR_MS = 15 * 60 * 1000
COLUMNS = ("Trade number", "Type", "Signal", "Price USD")
TYPES = {"Entry long", "Entry short", "Exit long", "Exit short"}
_NUM = r"-?\d+(?:\.\d+)?"
SIGNAL = re.compile(
    rf"^(?P<epoch>\d+)\|(?P<o>{_NUM})\|(?P<h>{_NUM})\|(?P<l>{_NUM})\|(?P<c>{_NUM})\|(?P<v>\d+)"
    r"\|(?P<time_close>\d+)\|(?P<dow>[1-7])\|(?P<sess>M|PRE|POST|X)"
    r"\|(?P<ticker>[^|]*)\|(?P<type>[^|]*)\|(?P<qccy>[^|]*)\|(?P<bccy>[^|]*)"
    r"\|(?P<mintick>\d+(?:\.\d+)?)\|(?P<pointvalue>\d+(?:\.\d+)?)\|(?P<tz>[^|]*)\|(?P<tf>[^|]*)$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class DataError(ValueError):
    pass


class BookError(DataError):
    pass


def file_sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def check_sha256(path: Path, expected: str) -> str:
    got = file_sha256(path)
    if got != expected:
        raise DataError(f"{path}: sha256 {got} does not match the pinned {expected}")
    return got


def _on_grid(x: float, tick: float) -> bool:
    return abs(x / tick - round(x / tick)) < 1e-6


def read_bar_export(path: Path, symbol: str) -> tuple[pd.DataFrame, dict]:
    """Return (OHLC bars indexed by America/New_York bar open, load summary)."""
    inst = INSTRUMENTS[symbol]
    with open(path, encoding="utf-8-sig", newline="") as fh:
        rd = csv.DictReader(fh)
        missing = set(COLUMNS) - set(rd.fieldnames or ())
        if missing:
            raise DataError(f"{path}: header lacks {sorted(missing)}; only raw BAR EXPORT v0.2 files are accepted")
        rows = []
        for r in rd:
            line = rd.line_num
            if r["Type"] not in TYPES:
                raise DataError(f"{path}:{line}: unknown Type {r['Type']!r}")
            if not r["Type"].startswith("Entry"):
                continue
            m = SIGNAL.match(r["Signal"] or "")
            if not m:
                raise DataError(f"{path}:{line}: Signal does not match BAR EXPORT v0.2: {r['Signal']!r}")
            tn = r["Trade number"] or ""
            if not tn.isdigit():
                raise DataError(f"{path}:{line}: Trade number {tn!r} is not an integer")
            try:
                price = float(r["Price USD"])
            except (TypeError, ValueError):
                raise DataError(f"{path}:{line}: Price USD {r['Price USD']!r} is not a number") from None
            o, h, l, c = (float(m[k]) for k in "ohlc")
            e = int(m["epoch"])
            if not all(math.isfinite(x) for x in (o, h, l, c, price)):
                raise DataError(f"{path}:{line}: non-finite price")
            if (m["ticker"], m["tz"], m["tf"]) != (inst.ticker, EXPORT_TZ, "15") \
                    or not math.isclose(float(m["mintick"]), inst.tick) \
                    or not math.isclose(float(m["pointvalue"]), inst.point_value):
                raise DataError(f"{path}:{line}: instrument constants {m['ticker']}|{m['mintick']}|{m['pointvalue']}|"
                                f"{m['tz']}|{m['tf']} do not match builder.instruments[{symbol}] at 15m")
            if int(m["time_close"]) != e + BAR_MS:
                raise DataError(f"{path}:{line}: bar is not 15 minutes long (time_close - open != 900000 ms)")
            if e % BAR_MS:
                raise DataError(f"{path}:{line}: bar open {e} is off the 15m grid")
            if not math.isclose(price, c, rel_tol=0, abs_tol=inst.tick * 1e-6):
                raise DataError(f"{path}:{line}: Entry price {price} != encoded close {c}")
            if not (l <= min(o, c) and max(o, c) <= h) or not all(_on_grid(x, inst.tick) for x in (o, h, l, c)):
                raise DataError(f"{path}:{line}: OHLC {o}/{h}/{l}/{c} fails low <= open,close <= high or the tick grid")
            rows.append((int(tn), e, o, h, l, c, line))
    if not rows:
        raise DataError(f"{path}: no Entry rows")
    rows.sort()
    tns = [r[0] for r in rows]
    if len(set(tns)) != len(tns):
        raise DataError(f"{path}: duplicate Entry trade numbers")
    eps = np.array([r[1] for r in rows], dtype=np.int64)
    if len(np.unique(eps)) != len(eps):
        raise DataError(f"{path}: duplicate bar timestamps")
    bad = np.flatnonzero(np.diff(eps) <= 0)
    if len(bad):
        raise DataError(f"{path}:{rows[bad[0] + 1][6]}: bar opens do not increase with trade number")
    idx = pd.to_datetime(eps, unit="ms", utc=True).as_unit("ns").tz_convert(NY)
    bars = pd.DataFrame([r[2:6] for r in rows], columns=["open", "high", "low", "close"], index=idx)
    return bars, _check_sessions(bars, symbol, path)


def _check_sessions(bars: pd.DataFrame, symbol: str, path) -> dict:
    so = INSTRUMENTS[symbol].session_open
    hm, day = bars.index.strftime("%H:%M"), bars.index.strftime("%Y-%m-%d")
    inwin = (hm >= so) & (hm < DAY_END) & (bars.index.weekday < 5)
    short = no_open = gappy = 0
    for _, t in pd.Series(bars.index[inwin]).groupby(day[inwin]):
        if t.iloc[0].strftime("%H:%M") != so:
            no_open += 1
            continue
        gappy += bool((t.diff().iloc[1:] != pd.Timedelta(minutes=15)).any())
        short += t.iloc[-1].strftime("%H:%M") < f"{int(DAY_END[:2]) - 1:02d}:45"
    steps = pd.Series(bars.index).diff().iloc[1:]
    return {"bars": len(bars), "first": str(bars.index[0]), "last": str(bars.index[-1]),
            "early_close_sessions": int(short), "days_without_open_bar": no_open, "gap_sessions": gappy,
            "gaps_between_bars": int((steps != pd.Timedelta(minutes=15)).sum())}


def load_bars(path: Path, symbol: str, sha256: str) -> tuple[pd.DataFrame, dict]:
    check_sha256(path, sha256)
    bars, summary = read_bar_export(path, symbol)
    return bars, {**summary, "sha256": sha256}


def session_dates(bars: pd.DataFrame, symbol: str) -> list[str]:
    """Weekdays with a bar opening exactly at the instrument's session open."""
    so = INSTRUMENTS[symbol].session_open
    idx = bars.index
    m = (idx.strftime("%H:%M") == so) & (idx.weekday < 5)
    return sorted(set(idx[m].strftime("%Y-%m-%d")))


def pinned_split(sessions: list[str], dev_end: str, holdout_end: str,
                 dev_start: str | None = None) -> tuple[list[str], list[str]]:
    """Development = dev_start <= sessions <= dev_end; holdout = dev_end < sessions <= holdout_end.
    Every given end must be a session of the export; development needs two sessions (one per 5c
    half), the holdout one."""
    for name, d in (("dev_start", dev_start), ("dev_end", dev_end), ("holdout_end", holdout_end)):
        if d is not None and d not in sessions:
            raise DataError(f"split {name} {d} is not a session date of the loaded export")
    dev = [d for d in sessions if (dev_start is None or dev_start <= d) and d <= dev_end]
    hold = [d for d in sessions if dev_end < d <= holdout_end]
    if len(dev) < 2 or not hold:
        raise DataError(f"split dev_end {dev_end} / holdout_end {holdout_end} gives {len(dev)} development "
                        f"and {len(hold)} holdout sessions; need >= 2 and >= 1")
    return dev, hold


def _iso(v) -> bool:
    try:
        return isinstance(v, str) and bool(DATE.match(v)) and date.fromisoformat(v).isoformat() == v
    except ValueError:
        return False


@dataclass(frozen=True)
class Calendar:
    closed: frozenset[str]   # entry dates with a non-NORMAL status: sessions on these dates are not traded
    start: str
    end: str
    sha256: str

    def check_covers(self, sessions: list[str], what: str) -> None:
        out = [d for d in sessions if not self.start <= d <= self.end]
        if out:
            raise DataError(f"{what}: sessions outside the calendar coverage {self.start}..{self.end}: {out[:5]}")


def _entry_closed(path: Path, e: dict) -> bool:
    """True when any recorded ``*_status`` is not NORMAL; refuses a row with none or an unknown one."""
    statuses = [v for k, v in e.items() if isinstance(k, str) and k.endswith("_status")]
    if not statuses:
        raise DataError(f"{path}: entry {e['date']} has no *_status field")
    bad = sorted({repr(v) for v in statuses if not isinstance(v, str) or v not in CALENDAR_STATUSES})
    if bad:
        raise DataError(f"{path}: entry {e['date']} has status {bad}; allowed {sorted(CALENDAR_STATUSES)}")
    return any(v != "NORMAL" for v in statuses)


def load_calendar(path: Path, sha256: str) -> Calendar:
    check_sha256(path, sha256)
    try:
        d = json.loads(Path(path).read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise DataError(f"{path}: not JSON ({e})") from None
    if not isinstance(d, dict) or d.get("schema") != CALENDAR_SCHEMA:
        raise DataError(f"{path}: calendar schema must be {CALENDAR_SCHEMA}")
    if not (_iso(d.get("coverage_start")) and _iso(d.get("coverage_end")) and d["coverage_start"] <= d["coverage_end"]):
        raise DataError(f"{path}: coverage_start/coverage_end must be ordered YYYY-MM-DD dates")
    entries = d.get("entries")
    if not isinstance(entries, list) or not entries or any(not isinstance(e, dict) or not _iso(e.get("date"))
                                                           for e in entries):
        raise DataError(f"{path}: entries must be a non-empty list of objects with a YYYY-MM-DD date")
    if any(not d["coverage_start"] <= e["date"] <= d["coverage_end"] for e in entries):
        raise DataError(f"{path}: an entry date lies outside the coverage window")
    closed = frozenset(e["date"] for e in entries if _entry_closed(path, e))
    return Calendar(closed, d["coverage_start"], d["coverage_end"], sha256)


def _unique_pairs(pairs):
    keys = [k for k, _ in pairs]
    if len(set(keys)) != len(keys):
        raise BookError(f"book has duplicate dates: {sorted({k for k in keys if keys.count(k) > 1})[:5]}")
    return dict(pairs)


def load_book(path: Path, sha256: str) -> dict[str, float]:
    """{YYYY-MM-DD: book P&L per session}; unique valid dates, finite numbers, not empty."""
    check_sha256(path, sha256)
    try:
        book = json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=_unique_pairs)
    except json.JSONDecodeError as e:
        raise BookError(f"{path}: not JSON ({e})") from None
    if not isinstance(book, dict) or not book:
        raise BookError(f"{path}: book must be a non-empty object; declare an empty book with book: null")
    for k, v in book.items():
        if not _iso(k) or isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
            raise BookError(f"{path}: bad book entry {k!r}: {v!r}")
    return {k: float(v) for k, v in book.items()}
