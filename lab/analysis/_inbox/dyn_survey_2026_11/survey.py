"""DYN-SURVEY-1 engine: frozen protocol v5 sections 3 and 4 (private; see DESIGN.md).

Prices are 15m bars by open timestamp, America/New_York. Times are minutes after midnight on
the session date. A session date's bars used here all fall in [07:30, 16:45], inside that
date's session day, so a session is one date's bars before 17:00.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Mapping

import numpy as np
import pandas as pd

from builder import gates
from builder.gates import Costs
from builder.instruments import INSTRUMENTS, minutes

K = 80
CELLS = tuple(f"C{i}" for i in range(1, 9))
DIRECTIONS = {"cont": 1, "rev": -1}
DEV_START = "2022-01-03"
H = minutes("16:30")
DAY_END = minutes("17:00")
C_PREV_FIRST, C_PREV_LAST = minutes("16:00"), minutes("16:45")
EXIT_TIME = {"MNQ": "15:45", "MYM": "15:45", "M2K": "15:45", "MGC": "14:00", "MCL": "14:30"}
SPLIT_DATE = "2024-04-30"
MIN_TRADES, MIN_SHARPE, MIN_DSR, MIN_COMMON, MIN_RISE = 200, 0.12, 0.95, 500, 0.03
BASE_TICKS, ADVERSE_TICKS = 1.0, 2.0

Day = Mapping[int, tuple[float, float, float, float]]  # bar open minute -> (open, high, low, close)
Plan = tuple[float | None, int, int]                   # (X, entry boundary, exit boundary)


def clock(symbol: str) -> tuple[int, int]:
    """(O, E) in minutes. O is the builder's session open."""
    return minutes(INSTRUMENTS[symbol].session_open), minutes(EXIT_TIME[symbol])


def session_days(bars: pd.DataFrame) -> dict[str, dict[int, tuple[float, float, float, float]]]:
    """{date: {open minute: OHLC}} for bars opening before 17:00 ET."""
    idx = bars.index
    mins = idx.hour * 60 + idx.minute
    keep = mins < DAY_END
    rows = bars.loc[keep, ["open", "high", "low", "close"]].to_numpy()
    out: dict[str, dict] = {}
    for d, t, r in zip(idx[keep].strftime("%Y-%m-%d"), mins[keep], rows):
        out.setdefault(d, {})[int(t)] = tuple(float(x) for x in r)
    return out


def ref(day: Day, t: int) -> float | None:
    """R(T): close of the latest real bar opening in [T - 60m, T - 15m]."""
    for b in range(t - 15, t - 75, -15):
        if b in day:
            return day[b][3]
    return None


def fill(day: Day, t: int, limit: int) -> float | None:
    """F(T, L): open of the first real bar opening in [T, min(T + 30m, L))."""
    for b in range(t, min(t + 30, limit), 15):
        if b in day:
            return day[b][0]
    return None


def diff(a: float | None, b: float | None) -> float | None:
    return None if a is None or b is None else a - b


def c_prev(day: Day | None) -> float | None:
    """Close of the latest real bar of the previous session day opening 16:00-16:45."""
    if day is None:
        return None
    for b in range(C_PREV_LAST, C_PREV_FIRST - 15, -15):
        if b in day:
            return day[b][3]
    return None


def first_hours(sessions: list[str], days: Mapping[str, Day], symbol: str) -> dict[str, tuple | None]:
    """{date: (H1, L1, narrow)}; None without a complete first hour. Narrow: W is at or below the
    7th smallest of the 20 most recent earlier complete first hours; False with fewer than 20."""
    o, tick = clock(symbol)[0], INSTRUMENTS[symbol].tick
    seen: list[int] = []
    out: dict[str, tuple | None] = {}
    for d in sessions:
        bars = [days[d].get(o + 15 * i) for i in range(4)]
        if any(b is None for b in bars):
            out[d] = None
            continue
        hi, lo = max(b[1] for b in bars), min(b[2] for b in bars)
        w = round((hi - lo) / tick)  # whole ticks, so ties are exact
        out[d] = (hi, lo, len(seen) >= 20 and w <= sorted(seen[-20:])[6])
        seen.append(w)
    return out


def window_valid(cell: str, symbol: str, s: int | None) -> bool:
    """False for both C6 and C7 when S is missing or off the 15m grid, or either window is invalid."""
    if cell not in ("C6", "C7"):
        return True
    return s is not None and s % 15 == 0 and s - 30 >= clock(symbol)[0] + 60 and s + 30 <= H


def plans(cell: str, symbol: str, day: Day, prev: Day | None, fh: tuple | None, s: int | None) -> list[Plan]:
    """The session's candidate trades, in order."""
    o, e = clock(symbol)
    if cell == "C1":
        return [(diff(ref(day, o), c_prev(prev)), o, o + 60)]
    if cell == "C2":
        return [(diff(ref(day, o), c_prev(prev)), o + 60, e)]
    if cell == "C3":
        return [(diff(ref(day, o + 60), ref(day, o)), o + 60, e)]
    if cell == "C4":
        return [(diff(ref(day, e - 60), ref(day, o)), e - 60, e)]
    if cell == "C5":
        b = [o + 60 * j for j in range((e - o) // 60 + 1)]  # b[j] is B_{j+1}
        return [(diff(ref(day, b[k]), ref(day, b[k - 1])), b[k], b[k + 1]) for k in range(1, len(b) - 1)]
    if cell == "C6":
        return [(diff(ref(day, s - 30), ref(day, o)), s - 30, s)]
    if cell == "C7":
        return [(diff(ref(day, s), ref(day, s - 30)), s, s + 30)]
    if cell == "C8":
        if fh is None or not fh[2]:
            return []
        for t in range(o + 60, e - 75 + 1, 15):
            if t in day and (day[t][3] > fh[0] or day[t][3] < fh[1]):
                return [(1.0 if day[t][3] > fh[0] else -1.0, t + 15, e)]
        return []
    raise ValueError(f"unknown cell {cell}")


@dataclass(frozen=True)
class Trade:
    date: str
    side: int
    entry_t: int
    exit_t: int
    entry_px: float
    exit_px: float | None  # None: unresolved

    @property
    def unresolved(self) -> bool:
        return self.exit_px is None


def session_trades(date: str, day: Day, todo: list[Plan], d: int) -> list[Trade]:
    out = []
    for x, t_in, t_out in todo:
        if x is None or x == 0:
            continue
        entry = fill(day, t_in, t_out)
        if entry is None:
            continue
        exit_px = fill(day, t_out, H + 15)
        out.append(Trade(date, d * (1 if x > 0 else -1), t_in, t_out, entry, exit_px))
        if exit_px is None:
            break
    return out


def cell_trades(cell: str, symbol: str, d: int, sessions: list[str], dev: list[str],
                days: Mapping[str, Day], closed: frozenset[str], s: int | None) -> list[Trade]:
    """All trades on development sessions. ``sessions`` is every export session, in order; earlier
    ones feed C8's warm-up only, so the first development session has no C_prev. A closed calendar
    date stays a session with no trade."""
    prev = dict(zip(dev[1:], dev[:-1]))
    fhs = first_hours(sessions, days, symbol) if cell == "C8" else {}
    out: list[Trade] = []
    for date in dev:
        if date not in closed:
            todo = plans(cell, symbol, days[date], days.get(prev.get(date)), fhs.get(date), s)
            out += session_trades(date, days[date], todo, d)
    return out


def series(trades: list[Trade], dev: list[str], symbol: str, commission: float, ticks: float) -> np.ndarray:
    """Net P&L of one contract per development session; zero on no-trade sessions."""
    pv = INSTRUMENTS[symbol].point_value
    cost = Costs(commission, ticks).per_trade(symbol)
    pos = {d: i for i, d in enumerate(dev)}
    x = np.zeros(len(dev))
    for t in trades:
        x[pos[t.date]] += t.side * (t.exit_px - t.entry_px) * pv - cost
    return x


def safe_dsr(x: np.ndarray) -> float | None:
    try:
        v = gates.dsr(x, K)[0]
    except (ValueError, ZeroDivisionError):
        return None
    return v if math.isfinite(v) else None


def statistics(trades: list[Trade], dev: list[str], symbol: str, commission: float,
               book: dict[str, float] | None) -> dict:
    """Protocol 4.2 for a cell with no unresolved development trade."""
    x = series(trades, dev, symbol, commission, BASE_TICKS)
    adverse = series(trades, dev, symbol, commission, ADVERSE_TICKS)
    half = len(x) // 2
    years = pd.Series(x, index=[d[:4] for d in dev]).groupby(level=0).mean()
    before = np.array([d <= SPLIT_DATE for d in dev])
    mean = lambda v: float(v.mean()) if len(v) else None  # noqa: E731
    return {"trades": len(trades), "sessions_traded": len({t.date for t in trades}), "sessions": len(dev),
            "sharpe_base": gates.sharpe(x), "sharpe_adverse": gates.sharpe(adverse), "dsr": safe_dsr(x),
            "zero_variance": not x.std() > 0, "mean_first_half": mean(x[:half]), "mean_second_half": mean(x[half:]),
            "mean_by_year": {k: float(v) for k, v in years.items()},
            "mean_to_split": mean(x[before]), "mean_after_split": mean(x[~before]),
            "book": gates._book(dev, x, book)}


def failures(st: dict) -> list[str]:
    """Why a resolved cell is INELIGIBLE (protocol 4.3); empty when ELIGIBLE."""
    out = []
    if st["trades"] < MIN_TRADES:
        out.append("fewer than 200 trades")
    if st["zero_variance"]:
        out.append("zero series variance")
    if st["dsr"] is None:
        out.append("undefined DSR")
    elif st["dsr"] < MIN_DSR:
        out.append("DSR below 0.95")
    if st["sharpe_base"] < MIN_SHARPE:
        out.append("base Sharpe below 0.12")
    if not st["sharpe_adverse"] > 0:
        out.append("adverse Sharpe not above 0")
    if not ((st["mean_first_half"] or 0) > 0 and (st["mean_second_half"] or 0) > 0):
        out.append("mean not above 0 in each half")
    if st["book"]["sessions"] < MIN_COMMON:
        out.append("fewer than 500 sessions in common with the book")
    return out


def cell_id(symbol: str, cell: str, direction: str) -> str:
    return f"{symbol}-{cell}-{direction}"


def evaluate_cell(cell: str, direction: str, symbol: str, sessions: list[str], dev: list[str],
                  days: Mapping[str, Day], closed: frozenset[str], s: int | None, commission: float,
                  book: dict[str, float] | None) -> dict:
    row = {"id": cell_id(symbol, cell, direction)}
    if not window_valid(cell, symbol, s):
        return {**row, "status": "NOT EVALUATED", "reason": "settlement time missing, off grid or window invalid"}
    trades = cell_trades(cell, symbol, DIRECTIONS[direction], sessions, dev, days, closed, s)
    unresolved = sorted({t.date for t in trades if t.unresolved})
    if unresolved:
        return {**row, "status": "UNRESOLVED", "trades": len(trades), "sessions_traded": len({t.date for t in trades}),
                "unresolved": sum(t.unresolved for t in trades), "unresolved_dates": unresolved}
    st = statistics(trades, dev, symbol, commission, book)
    bad = failures(st)
    row.update(st, status="INELIGIBLE" if bad else "ELIGIBLE", failed=bad, unresolved=0, unresolved_dates=[])
    if not bad:
        row["rise"] = st["book"]["book_s_with_card"] - st["book"]["book_s"]
    return row


def select(rows: list[dict]) -> dict | None:
    """Protocol 4.4: the largest rise, then higher DSR, then lower id; advances at +0.03 or more."""
    eligible = [r for r in rows if r["status"] == "ELIGIBLE"]
    if not eligible:
        return None
    best = min(eligible, key=lambda r: (-r["rise"], -r["dsr"], r["id"]))
    return best if best["rise"] >= MIN_RISE else None


def outcome(rows: list[dict], chosen: dict | None) -> str:
    """The survey's stage of protocol 6. An advance is not an outcome until parity, look and 5h."""
    if chosen is not None:
        return "ADVANCED"
    return "PARTIAL NULL" if any(r["status"] == "NOT EVALUATED" for r in rows) else "NULL"


def quality(bars: pd.DataFrame, volume: pd.Series, dev: list[str], symbol: str, cost: float) -> list[dict]:
    """Per-slot table: missing-bar share, median range and volume, cost / median range."""
    o, e = clock(symbol)
    idx = bars.index
    frame = pd.DataFrame({"date": idx.strftime("%Y-%m-%d"), "slot": idx.hour * 60 + idx.minute,
                          "range": (bars["high"] - bars["low"]).to_numpy(), "volume": volume.to_numpy()})
    frame = frame[frame["date"].isin(set(dev))]
    pv, out = INSTRUMENTS[symbol].point_value, []
    for slot in range(o, e + 15, 15):
        f = frame[frame["slot"] == slot]
        rng = float(f["range"].median()) if len(f) else None
        out.append({"slot": f"{slot // 60:02d}:{slot % 60:02d}", "missing_share": 1 - len(f) / len(dev),
                    "median_range": rng, "median_volume": float(f["volume"].median()) if len(f) else None,
                    "cost_over_median_range": cost / (rng * pv) if rng else None})
    return out
