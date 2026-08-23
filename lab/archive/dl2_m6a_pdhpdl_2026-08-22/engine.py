"""DL-2 prereg Sec1 + Sec3 -- frozen full-Globex-session prior-session
breakout-continuation engine, M6A-rescaled, TRAIN partition only.

Every function below cites the prereg clause it implements so the parent-
session review (handoff Sec7 Pass 1) can check function-by-function against
the frozen text.

Interpretive fills (spec silent on the exact micro-convention; disclosed
here, mirroring DL-1's own engine.py I1-I5 disclosure discipline, NOT
amendments to Sec1-Sec3 since fixed before any train number was computed):
  I1. A stray bar timestamped inside the (17:00, 18:00) ET maintenance-break
      gap (feed artifact; none expected) is assigned to the CURRENT-day
      session rather than dropped or raising -- disclosed, not expected to
      fire (checked: zero such bars in the actual TRAIN stitched series).
  I2. The entry bar itself is checked for stop/target touch (not just bars
      strictly after it) -- same convention as DL-1's own I3 (bar-based
      fill-engine, not intrabar-position-based).
  I3. Retest-limit fills require the touch bar to be STRICTLY AFTER the
      close-confirm (arming) bar -- DL-1's own I5, adopted for the same
      reason (Sec2's own text already sequences it this way: "after the
      close-confirm trigger fires, rest a limit order").
  I4. Close-confirm's tick buffer and "gaps through" carve-out (Sec3 item 4)
      apply only to close-confirm entries; retest-limit fills exactly at
      the broken level (Sec2's own text names no tick adjustment for it,
      and DL-1's own retest fill precedent is likewise exact-at-level).
  I5. No same-bar double-trigger case exists for close-confirm entries
      (unlike DL-1's OR-breakout, which triggers on intrabar high/low
      touch): the trigger is BAR CLOSE beyond level.high or level.low, and
      level.high >= level.low always (both derived from the same
      session-range object(s)), so a single bar's close cannot satisfy
      both directions at once.
"""
from __future__ import annotations

from bisect import bisect_left
from dataclasses import dataclass
from datetime import date as Date

import numpy as np
import pandas as pd

from variants import Variant

TICK = 0.0001                  # 6A/M6A minimum price fluctuation, USD per AUD
DOLLAR_PER_POINT = 10000.0     # M6A (10,000 AUD micro) -- prereg Sec3 proxy: tick 0.0001 = $1
RT_COST = 2.60                 # prereg Sec3 item 3, frozen cost pin (both partitions)

ET = "America/New_York"
SESSION_OPEN_MIN = 18 * 60           # 18:00 ET, prereg Sec1 session boundary (start)
FORCE_FLAT_HOUR, FORCE_FLAT_MINUTE = 16, 55  # 16:55 ET, prereg Sec1 force-flat


@dataclass
class Trade:
    session_date: Date
    variant: int
    direction: str          # "long" | "short"
    entry_style: str
    entry_price: float
    exit_price: float
    exit_reason: str        # "stop" | "target" | "force_flat"
    risk_price: float
    stop_ticks: float
    gross_dollars: float
    net_dollars: float


@dataclass
class SessionSlice:
    session_date: Date
    utc_days: frozenset
    et_idx: pd.DatetimeIndex   # tz-aware (ET), ascending, one per bar
    o: np.ndarray
    h: np.ndarray
    l: np.ndarray
    c: np.ndarray
    open_: float
    close_: float
    high: float
    low: float


def _session_label(et_index: pd.DatetimeIndex) -> np.ndarray:
    """prereg Sec1: 18:00 ET (previous calendar day) -> 17:00 ET (current
    calendar day). A bar at/after 18:00 ET belongs to the NEXT calendar
    day's session; a bar at/before 17:00 ET belongs to the current day's
    session (I1 covers the empty maintenance-break gap between them)."""
    tmin = et_index.hour * 60 + et_index.minute
    shifted = tmin >= SESSION_OPEN_MIN
    return np.where(shifted, (et_index + pd.Timedelta(days=1)).date, et_index.date)


def build_sessions(stitched: pd.DataFrame) -> dict[Date, SessionSlice]:
    """One SessionSlice per ET-labeled Globex session (prereg Sec1), holding
    the FULL 18:00-ET(prev)->17:00-ET(current) window -- callers trim to
    [start, 16:55 ET] separately for the tradable/force-flat window
    (mirrors DL-1's own full-slice/trading-window split)."""
    et_idx = stitched.index.tz_convert(ET)
    utc_days = stitched.index.date
    session_dates = _session_label(et_idx)

    o = stitched["open"].to_numpy(dtype=float)
    h = stitched["high"].to_numpy(dtype=float)
    l = stitched["low"].to_numpy(dtype=float)
    c = stitched["close"].to_numpy(dtype=float)

    order = np.lexsort((et_idx.asi8, session_dates))
    sd_sorted = session_dates[order]

    out: dict[Date, SessionSlice] = {}
    boundaries = np.flatnonzero(sd_sorted[1:] != sd_sorted[:-1]) + 1
    starts = np.concatenate(([0], boundaries))
    ends = np.concatenate((boundaries, [len(sd_sorted)]))
    for s, e in zip(starts, ends):
        idx = order[s:e]
        d = sd_sorted[s]
        out[d] = SessionSlice(
            session_date=d,
            utc_days=frozenset(utc_days[idx]),
            et_idx=et_idx[idx],
            o=o[idx], h=h[idx], l=l[idx], c=c[idx],
            open_=float(o[idx][0]), close_=float(c[idx][-1]),
            high=float(h[idx].max()), low=float(l[idx].min()),
        )
    return out


def is_roll_session_map(sessions: dict[Date, SessionSlice], roll_days_utc: set) -> dict[Date, bool]:
    """prereg Sec1: 'sessions containing a front-month volume-roll are
    excluded from entries' -- a session is a roll session if any of the
    (up to 2) UTC calendar days its bars are drawn from is itself a UTC
    roll day (Sec3's frozen per-UTC-day rule)."""
    return {d: bool(s.utc_days & roll_days_utc) for d, s in sessions.items()}


def trading_calendar(sessions: dict[Date, SessionSlice]) -> list[Date]:
    """prereg Sec3 item 1 (CME trading calendar, flat days included as
    zeros): every ET-labeled Globex session present in the stitched TRAIN
    data. DL-2's session unit IS the full Globex day (unlike DL-1's RTH
    sub-window), so every session date with any bars is a genuine trading
    session -- no Sunday-reopen-style narrowing needed."""
    return sorted(sessions)


def _lookback_reference(nonroll_dates_sorted: list[Date], target: Date, n_sessions: int) -> list[Date] | None:
    """prereg Sec1 roll-day lookback rule: walk back through NON-roll
    sessions strictly before `target`, skipping roll sessions entirely (a
    roll session never seeds a PDH/PDL level, only its own entries are
    suppressed). Returns the `n_sessions` most recent such dates, oldest
    first, or None if fewer than `n_sessions` exist before `target`."""
    pos = bisect_left(nonroll_dates_sorted, target)
    if pos < n_sessions:
        return None
    return nonroll_dates_sorted[pos - n_sessions:pos]


def lookback_level(sessions: dict[Date, SessionSlice], refs: list[Date]) -> tuple[float, float]:
    """PDH/PDL over the reference session(s) -- prereg Sec2: 1-session
    (canonical PDH/PDL) or 2-session (wider structural level, still 'prior
    extreme')."""
    highs = [sessions[r].high for r in refs]
    lows = [sessions[r].low for r in refs]
    return max(highs), min(lows)


def drift_sign(sessions: dict[Date, SessionSlice], refs: list[Date]) -> int:
    """prereg Sec2: sign(lookback-window's last session close - lookback-
    window's first session open). `refs` is chronological, oldest first."""
    first_open = sessions[refs[0]].open_
    last_close = sessions[refs[-1]].close_
    if last_close == first_open:
        return 0
    return 1 if last_close > first_open else -1


def _trim_to_force_flat(ss: SessionSlice):
    """Bars from session-start through the 16:55 ET force-flat bar
    (inclusive) -- entries and resolution are both scanned only within this
    window (mirrors DL-1's own `_trading_window` restriction, applied here
    to the full Globex session rather than an RTH sub-window)."""
    cutoff = pd.Timestamp(ss.session_date, tz=ET) + pd.Timedelta(hours=FORCE_FLAT_HOUR, minutes=FORCE_FLAT_MINUTE)
    mask = ss.et_idx <= cutoff
    return ss.o[mask], ss.h[mask], ss.l[mask], ss.c[mask]


def _find_close_confirm_trigger(c: np.ndarray, level_high: float, level_low: float, directions: set[str]):
    """First bar whose CLOSE breaks beyond the level, eligible direction --
    prereg Sec1 ('a break ... confirmed by a subsequent session close
    beyond the level'). See module docstring I5: no same-bar double-trigger
    case exists here."""
    for i in range(len(c)):
        if "long" in directions and c[i] > level_high:
            return i, "long"
        if "short" in directions and c[i] < level_low:
            return i, "short"
    return None


def _close_confirm_fill(o: np.ndarray, i: int, direction: str, level_high: float, level_low: float):
    """prereg Sec2 ('enter next 1m bar's open (+1 tick, mirrored for
    shorts)') + Sec3 item 4 ('or bar open if the bar gaps through, for
    close-confirm variants'): fill at the worse of {next bar's open,
    level +- 1 tick}. None if there is no next bar within the session."""
    if i + 1 >= len(o):
        return None
    nxt_open = o[i + 1]
    if direction == "long":
        return i + 1, max(nxt_open, level_high + TICK)
    return i + 1, min(nxt_open, level_low - TICK)


def _retest_limit_fill(h: np.ndarray, l: np.ndarray, i: int, direction: str, level_high: float, level_low: float):
    """prereg Sec2 ('rest a limit order at the broken level itself ...
    filled if price returns to the level before session flat'): scan bars
    STRICTLY AFTER the confirming bar `i` (I3) for the first touch; fills
    EXACTLY at the level (I4). None if never touched."""
    for j in range(i + 1, len(h)):
        if direction == "long" and l[j] <= level_high:
            return j, level_high
        if direction == "short" and h[j] >= level_low:
            return j, level_low
    return None


def _resolve_trade(h: np.ndarray, l: np.ndarray, c: np.ndarray, entry_idx: int, direction: str,
                    stop_price: float, target_price: float, extra_slip_ticks: int):
    """prereg Sec3 item 4: adverse-first same-bar resolution; stop exits at
    stop price -+ 1 tick slip (mirrored for shorts); target exits at target
    price exactly; else force-flat at the last (16:55 ET) bar's close.
    Entry bar itself is checked too (I2)."""
    slip = TICK * (1 + extra_slip_ticks)
    for i in range(entry_idx, len(h)):
        if direction == "long":
            if l[i] <= stop_price:
                return stop_price - slip, "stop"
            if h[i] >= target_price:
                return target_price, "target"
        else:
            if h[i] >= stop_price:
                return stop_price + slip, "stop"
            if l[i] <= target_price:
                return target_price, "target"
    return float(c[-1]), "force_flat"


def simulate_variant(
    sessions: dict[Date, SessionSlice],
    session_dates_sorted: list[Date],
    nonroll_dates_sorted: list[Date],
    is_roll: dict[Date, bool],
    variant: Variant,
    extra_slip_ticks: int = 0,
) -> list[Trade]:
    """One full TRAIN pass for a single frozen variant (prereg Sec1-Sec3)."""
    trades: list[Trade] = []
    for d in session_dates_sorted:
        if is_roll[d]:
            continue  # prereg Sec1: roll sessions excluded from entries

        refs = _lookback_reference(nonroll_dates_sorted, d, variant.lookback)
        if refs is None:
            continue  # insufficient non-roll history yet

        level_high, level_low = lookback_level(sessions, refs)

        if variant.drift == "aligned":
            drift = drift_sign(sessions, refs)
            if drift == 0:
                continue
            directions = {"long"} if drift > 0 else {"short"}
        else:
            directions = {"long", "short"}

        o, h, l, c = _trim_to_force_flat(sessions[d])
        if len(c) == 0:
            continue

        trig = _find_close_confirm_trigger(c, level_high, level_low, directions)
        if trig is None:
            continue
        confirm_idx, direction = trig

        if variant.entry_style == "close_confirm":
            fill = _close_confirm_fill(o, confirm_idx, direction, level_high, level_low)
        else:
            fill = _retest_limit_fill(h, l, confirm_idx, direction, level_high, level_low)
        if fill is None:
            continue
        entry_idx, entry_price = fill

        if direction == "long":
            entry_price += TICK * extra_slip_ticks
            stop_price = level_low
            risk_price = entry_price - stop_price
            target_price = entry_price + variant.target_r * risk_price
        else:
            entry_price -= TICK * extra_slip_ticks
            stop_price = level_high
            risk_price = stop_price - entry_price
            target_price = entry_price - variant.target_r * risk_price

        if risk_price <= 0:
            continue  # degenerate reference (entry beyond opposite extreme already) -- no valid trade

        exit_price, reason = _resolve_trade(h, l, c, entry_idx, direction, stop_price, target_price, extra_slip_ticks)
        gross_price = (exit_price - entry_price) if direction == "long" else (entry_price - exit_price)
        gross_dollars = gross_price * DOLLAR_PER_POINT
        net_dollars = gross_dollars - RT_COST

        trades.append(Trade(
            session_date=d, variant=variant.v, direction=direction, entry_style=variant.entry_style,
            entry_price=entry_price, exit_price=exit_price, exit_reason=reason,
            risk_price=risk_price, stop_ticks=risk_price / TICK,
            gross_dollars=gross_dollars, net_dollars=net_dollars,
        ))
    return trades
