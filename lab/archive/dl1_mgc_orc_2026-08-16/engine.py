"""DL-1 prereg Sec1 + Sec3 -- frozen NY-session opening-range continuation
engine, MGC-rescaled, TRAIN partition only.

Every function below cites the prereg clause it implements so the
adversarial verification pass can check function-by-function against the
frozen text.

Interpretive fills (spec silent on the exact micro-convention; disclosed
here, NOT amendments to Sec1/Sec3 since fixed before any train number was
computed):
  I1. "08:30 ET" / "17:00 CT reopen" anchor prices use the OPEN of the first
      bar at-or-after each anchor time.
  I2. ET and CT observe US DST on the same calendar day every year, so
      CT = ET - 1h with NO seasonal edge case: 17:00 CT is always exactly
      18:00 ET. The drift lookup is therefore done entirely in ET-minutes,
      no separate CT zone conversion needed.
  I3. The entry bar is itself checked for stop/target touch (not just bars
      strictly after it) -- the fill-engine text is bar-based, not
      intrabar-position-based.
  I4. A bar that would trigger BOTH entry directions at once (possible only
      on a single 1m bar spanning the full OR range) is treated as "no
      entry" that day for that variant -- Sec1's "first triggered side only"
      presumes a resolvable time order, which OHLC data cannot give for a
      same-bar double-trigger. Counted and reported (expected ~0 occurrences).
  I5. Retest fills require the pullback bar to be STRICTLY AFTER the break
      (arming) bar -- same-bar break+retest is not allowed. Tried the
      same-bar-allowed reading first; rejected after testing showed it made
      "retest" entries degenerate to near-identical behavior with
      "breakout" entries (a typical breakout bar's own low already sits
      below the OR level while its high pokes above the trigger, so an
      any-bar retest check kept firing on the break bar itself).
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date as Date, time

import numpy as np
import pandas as pd

from variants import Variant

TICK = 0.10                    # GC/MGC minimum price tick, $/oz
DOLLAR_PER_POINT = 10.0        # MGC (10oz) -- prereg Sec3 proxy discipline: tick 0.1 = $1
RT_COST = 4.12                 # prereg Sec3 item 3, frozen cost pin (both partitions)

OR_ANCHOR_MIN = 8 * 60 + 30    # 08:30 ET, prereg Sec1 session anchor
FORCE_FLAT_MIN = 15 * 60 + 55  # 15:55 ET, prereg Sec1 force-flat
REOPEN_ET_MIN = 18 * 60        # 17:00 CT == 18:00 ET (I2), prereg Sec1 drift anchor
ET = "America/New_York"


@dataclass
class Trade:
    session_date: Date
    variant: int
    direction: str          # "long" | "short"
    entry_style: str
    entry_price: float
    exit_price: float
    exit_reason: str        # "stop" | "target" | "force_flat"
    risk_price: float       # |entry - opposite OR extreme|
    stop_ticks: float
    gross_dollars: float
    net_dollars: float


@dataclass
class DaySlice:
    session_date: Date
    et_min: np.ndarray      # minutes since ET midnight, one per bar, sorted ascending
    o: np.ndarray
    h: np.ndarray
    l: np.ndarray
    c: np.ndarray


def build_day_slices(stitched: pd.DataFrame) -> dict[Date, DaySlice]:
    """One DaySlice per ET calendar date, holding that date's full set of
    stitched bars (spans the whole 24h session, not just 08:30-15:55, so the
    same structure serves both the OR/trading window and the drift lookup
    to the same-labeled-date's evening reopen -- I2)."""
    et_idx = stitched.index.tz_convert(ET)
    days = et_idx.date
    o = stitched["open"].to_numpy(dtype=float)
    h = stitched["high"].to_numpy(dtype=float)
    l = stitched["low"].to_numpy(dtype=float)
    c = stitched["close"].to_numpy(dtype=float)
    et_min = (et_idx.hour * 60 + et_idx.minute).to_numpy()

    order = np.lexsort((et_min, days))
    days_sorted = days[order]
    boundaries = np.flatnonzero(np.diff(days_sorted.astype("datetime64[D]").astype(np.int64))) + 1
    starts = np.concatenate(([0], boundaries))
    ends = np.concatenate((boundaries, [len(days_sorted)]))

    out: dict[Date, DaySlice] = {}
    for s, e in zip(starts, ends):
        idx = order[s:e]
        d = days_sorted[s]
        out[d] = DaySlice(d, et_min[idx], o[idx], h[idx], l[idx], c[idx])
    return out


def compute_or(slices: dict[Date, DaySlice], or_minutes: int) -> dict[Date, tuple[float, float]]:
    """OR high/low over [08:30, 08:30+or_minutes) ET -- prereg Sec1. A day
    with no bars in the window is absent from the result (no trade)."""
    end_min = OR_ANCHOR_MIN + or_minutes
    out = {}
    for d, ds in slices.items():
        mask = (ds.et_min >= OR_ANCHOR_MIN) & (ds.et_min < end_min)
        if not mask.any():
            continue
        out[d] = (float(ds.h[mask].max()), float(ds.l[mask].min()))
    return out


def compute_drift(slices: dict[Date, DaySlice]) -> dict[Date, int]:
    """sign(P_0830_today - P_reopen_prior_evening), prereg Sec1 drift filter.
    P_0830 = open of first bar at/after 08:30 ET today (I1). P_reopen = open
    of first bar at/after 18:00 ET (== 17:00 CT, I2) on the SAME date's own
    slice, read for the PRIOR calendar date (the evening session-open that
    precedes today's NY morning) -- prereg: "prior 17:00 CT reopen". A day
    missing either anchor bar, or with drift == 0, is absent from the result
    (I: aligned variants get no eligible direction that day)."""
    out: dict[Date, int] = {}
    for d, ds in slices.items():
        mask_0830 = ds.et_min >= OR_ANCHOR_MIN
        if not mask_0830.any():
            continue
        p_0830 = float(ds.o[mask_0830][0])  # et_min sorted ascending -> first hit is earliest

        prior_date = d - pd.Timedelta(days=1)
        prior = slices.get(prior_date)
        if prior is None:
            continue
        mask_reopen = prior.et_min >= REOPEN_ET_MIN
        if not mask_reopen.any():
            continue
        p_reopen = float(prior.o[mask_reopen][0])

        if p_0830 == p_reopen:
            continue
        out[d] = 1 if p_0830 > p_reopen else -1
    return out


def _trading_window(ds: DaySlice) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Bars in [08:30, 15:55] ET -- the tradable window, force-flat inclusive
    of the 15:55 bar itself (its close is the force-flat price if reached)."""
    mask = (ds.et_min >= OR_ANCHOR_MIN) & (ds.et_min <= FORCE_FLAT_MIN)
    return ds.et_min[mask], ds.o[mask], ds.h[mask], ds.l[mask], ds.c[mask]


def trading_calendar(slices: dict[Date, DaySlice]) -> list[Date]:
    """The CME trading calendar for this NY-session strategy -- prereg Sec3
    item 1 ("CME trading calendar, flat days included as zeros"): dates that
    actually have bars inside the [08:30, 15:55] ET tradable window.

    NOT every raw ET-calendar-date present in `slices`: Globex's Sunday-
    evening reopen produces bars on a "Sunday" ET date that has no 08:30 ET
    session at all -- bucketing daily P&L by raw ET date (as an earlier
    version of this module did) folds in ~16% of spurious always-zero
    "Sunday" observations, diluting net annSR and mismatching the sqrt(252)
    annualization's implied ~252-obs/year assumption (found by adversarial
    verification). A date present here but with no OR-window bars for a
    given variant's or_minutes still correctly contributes a flat zero via
    daily_pnl_series -- it's a real trading day, just one with no entry."""
    return sorted(d for d, ds in slices.items() if _trading_window(ds)[0].size > 0)


def _find_entry(
    et_min: np.ndarray, o: np.ndarray, h: np.ndarray, l: np.ndarray,
    or_end_min: int, or_high: float, or_low: float,
    directions: set[str], style: str,
) -> tuple[int, str, float] | None:
    """Scan post-OR bars for the first triggered entry. Returns
    (bar_index, direction, entry_price) or None. I3/I4/I5 govern the tie
    breaks documented in the module docstring."""
    # compute_or's OR window is [start, or_end_min) -- exclusive of or_end_min
    # itself -- so the entry scan must START at or_end_min (>=), not after it
    # (>), else the bar exactly at the boundary belongs to neither the OR
    # calc nor the entry scan (found by adversarial verification: a 1-minute
    # dead zone on every session, every variant).
    post_mask = et_min >= or_end_min
    idx = np.flatnonzero(post_mask)
    if idx.size == 0:
        return None

    long_trigger = or_high + TICK
    short_trigger = or_low - TICK

    if style == "breakout":
        for i in idx:
            hit_long = ("long" in directions) and (h[i] >= long_trigger)
            hit_short = ("short" in directions) and (l[i] <= short_trigger)
            if hit_long and hit_short:
                return None  # I4: same-bar double trigger -> no entry
            if hit_long:
                price = o[i] if o[i] >= long_trigger else long_trigger
                return i, "long", float(price)
            if hit_short:
                price = o[i] if o[i] <= short_trigger else short_trigger
                return i, "short", float(price)
        return None

    if style == "retest":
        # I5 (revised): retest must fill on a bar STRICTLY AFTER the arming
        # (break) bar. Allowing a same-bar break+retest was tried first and
        # rejected after testing: a typical breakout bar's low still sits
        # below or_high while its high pokes above long_trigger, so an
        # any-bar retest check degenerated to firing on the break bar itself
        # almost every time -- making "retest" behaviorally indistinguishable
        # from "breakout" instead of testing the genuinely later, sometimes-
        # never-filling pullback entry the variant axis is meant to probe.
        long_armed_at = None
        short_armed_at = None
        for pos, i in enumerate(idx):
            if long_armed_at is None and ("long" in directions) and (h[i] >= long_trigger):
                long_armed_at = pos
            if short_armed_at is None and ("short" in directions) and (l[i] <= short_trigger):
                short_armed_at = pos
            retest_long = long_armed_at is not None and pos > long_armed_at and l[i] <= or_high
            retest_short = short_armed_at is not None and pos > short_armed_at and h[i] >= or_low
            if retest_long and retest_short:
                return None  # I4 analogue: both complete on the same bar
            if retest_long:
                return i, "long", float(or_high)
            if retest_short:
                return i, "short", float(or_low)
        return None

    raise ValueError(f"unknown entry style {style!r}")


def _resolve_trade(
    et_min: np.ndarray, h: np.ndarray, l: np.ndarray, c: np.ndarray,
    entry_idx: int, direction: str, stop_price: float, target_price: float,
    extra_slip_ticks: int,
) -> tuple[float, str]:
    """From the entry bar (inclusive, I3) through the last tradable bar:
    adverse-first same-bar resolution (stop wins a same-bar double-touch);
    stop exits at stop_price -+ (1 + extra_slip_ticks) ticks of slippage
    (mirrored by direction); target exits at target_price exactly; else
    force-flat at the 15:55 ET bar's close."""
    slip = TICK * (1 + extra_slip_ticks)
    n = len(et_min)
    for i in range(entry_idx, n):
        if direction == "long":
            stop_hit = l[i] <= stop_price
            target_hit = h[i] >= target_price
            if stop_hit:
                return stop_price - slip, "stop"
            if target_hit:
                return target_price, "target"
        else:
            stop_hit = h[i] >= stop_price
            target_hit = l[i] <= target_price
            if stop_hit:
                return stop_price + slip, "stop"
            if target_hit:
                return target_price, "target"
    return float(c[-1]), "force_flat"


def simulate_variant(
    slices: dict[Date, DaySlice],
    or_by_date_30: dict[Date, tuple[float, float]],
    or_by_date_60: dict[Date, tuple[float, float]],
    drift_by_date: dict[Date, int],
    roll_dates: set[Date],
    variant: Variant,
    extra_slip_ticks: int = 0,
) -> list[Trade]:
    """One full TRAIN pass for a single frozen variant (prereg Sec1-Sec3)."""
    or_by_date = or_by_date_30 if variant.or_minutes == 30 else or_by_date_60
    or_end_min = OR_ANCHOR_MIN + variant.or_minutes

    trades: list[Trade] = []
    for d, (or_high, or_low) in or_by_date.items():
        if d in roll_dates:
            continue  # prereg Sec1: roll sessions excluded from entries

        if variant.drift == "aligned":
            drift = drift_by_date.get(d)
            if not drift:
                continue
            directions = {"long"} if drift > 0 else {"short"}
        else:
            directions = {"long", "short"}

        ds = slices[d]
        et_min, o, h, l, c = _trading_window(ds)
        found = _find_entry(et_min, o, h, l, or_end_min, or_high, or_low, directions, variant.entry_style)
        if found is None:
            continue
        entry_idx, direction, entry_price = found

        if direction == "long":
            entry_price += TICK * extra_slip_ticks
            stop_price = or_low
            risk_price = entry_price - stop_price
            target_price = entry_price + variant.target_r * risk_price
        else:
            entry_price -= TICK * extra_slip_ticks
            stop_price = or_high
            risk_price = stop_price - entry_price
            target_price = entry_price - variant.target_r * risk_price

        if risk_price <= 0:
            continue  # degenerate OR (entry beyond opposite extreme already) -- no valid trade

        exit_price, reason = _resolve_trade(
            et_min, h, l, c, entry_idx, direction, stop_price, target_price, extra_slip_ticks,
        )
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
