"""Card -> trades on closed 15m bars (spec stage 4, backtest side).

Fill model, conservative where 15m bars hide the order of events:
- The range is the card's n bars from the session open (offset for time_window). Orders are
  stop entries one tick beyond the range, live from the first bar after the range until the
  entry cutoff. A bar that opens beyond a level fills at its open (gap); otherwise at the level.
- If one bar touches both levels, the side whose level is nearer the bar's open fills.
- In the entry bar, the stop counts if the bar reaches it; the target never does.
- Later bars: a gap through the stop exits at the open; if a bar reaches both the stop and the
  target, the stop counts first.
- At the first bar opening at or after flat_at the position exits at that open; if the day has
  no such bar (an early halt), at the close of its last bar before DAY_END.
Costs are applied by the gate engine, not here. ATR is the 14-bar mean true range of the 15m
series through the last range bar, defined only when those bars and the close before them are
contiguous; it is never computed across a gap.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from builder.cards import Card
from builder.instruments import DAY_END, INSTRUMENTS

ATR_LEN = 14
BAR_MIN = 15


@dataclass(frozen=True)
class Day:
    date: str
    times: tuple[str, ...]
    o: np.ndarray
    h: np.ndarray
    l: np.ndarray
    c: np.ndarray
    first: int       # first bar index where entries are live
    cutoff: int      # entries live while index < cutoff
    flat: int        # index of the flat_at bar, or len(times) when the day has none
    hi: float
    lo: float
    atr: float


@dataclass(frozen=True)
class Trade:
    date: str
    side: int        # +1 long, -1 short
    entry_i: int
    exit_i: int
    entry_px: float
    exit_px: float
    reason: str      # stop | target | flat

    @property
    def points(self) -> float:
        return self.side * (self.exit_px - self.entry_px)


def days(card: Card, bars: pd.DataFrame, dates: list[str], skipped: dict | None = None) -> list[Day]:
    """The card's tradable days among ``dates`` (sessions of ``bars``). A day's bars run from the
    session open to the last bar before DAY_END; ``data`` guarantees they are contiguous. Days left
    out are counted in ``skipped`` by reason: day_of_week (card filter), short_session (the day
    ends before entries go live) and atr_window_gap (the card uses ATR and there are
    no 15 contiguous bars for it)."""
    inst = INSTRUMENTS[card.instrument]
    tr = np.maximum(bars["high"], bars["close"].shift()) - np.minimum(bars["low"], bars["close"].shift())
    step_ok = pd.Series((pd.Series(bars.index).diff() == pd.Timedelta(minutes=BAR_MIN)).to_numpy(), index=bars.index)
    atr = tr.rolling(ATR_LEN).mean().where(step_ok.rolling(ATR_LEN).sum() == ATR_LEN).to_numpy()
    off, n = int(card.p("offset_bars", 0)), int(card.p("n_bars"))
    uses_atr = "atr_multiple" in (card.stop, card.target) or "min_range_atr" in card.filters
    hhmm = bars.index.strftime("%H:%M")
    win = np.flatnonzero((hhmm >= inst.session_open) & (hhmm < DAY_END))
    by_day = pd.Series(win).groupby(bars.index[win].strftime("%Y-%m-%d")).agg(list)
    skipped = {} if skipped is None else skipped
    out = []
    for d in dates:
        if card.days and pd.Timestamp(d).weekday() not in card.days:
            reason = "day_of_week"
        else:
            ix = np.array(by_day[d])
            t = tuple(hhmm[ix])
            flat = next((j for j, s in enumerate(t) if s >= card.flat_at), len(t))
            t, ix = t[:flat + 1], ix[:flat + 1]
            first = off + n
            cutoff = min(next((j for j, s in enumerate(t) if s >= card.entry_cutoff), len(t)), flat)
            a = atr[ix[first - 1]] if first < cutoff else np.nan
            if first >= cutoff:
                reason = "short_session"
            elif uses_atr and (not np.isfinite(a) or a <= 0):
                reason = "atr_window_gap"
            else:
                o, h, l, c = (bars[k].to_numpy()[ix] for k in ("open", "high", "low", "close"))
                out.append(Day(d, t, o, h, l, c, first, cutoff, flat,
                               float(h[off:first].max()), float(l[off:first].min()), float(a)))
                continue
        skipped[reason] = skipped.get(reason, 0) + 1
    return out


def _on_tick(x: float, tick: float) -> float:
    return round(round(x / tick) * tick, 10)


def _levels(card: Card, day: Day, side: int, entry: float, tick: float) -> tuple[float, float | None]:
    if card.stop == "range_opposite":
        stop = _on_tick(day.lo - tick if side > 0 else day.hi + tick, tick)
    elif card.stop == "atr_multiple":
        stop = entry - side * card.p("stop_atr") * day.atr
    else:
        stop = entry - side * card.p("stop_ticks") * tick
    risk = side * (entry - stop)
    if card.target == "r_multiple":
        target = entry + side * card.p("target_r") * risk
    elif card.target == "atr_multiple":
        target = entry + side * card.p("target_atr") * day.atr
    else:
        target = None
    return _on_tick(stop, tick), (None if target is None else _on_tick(target, tick))


def simulate_day(card: Card, day: Day) -> list[Trade]:
    tick = INSTRUMENTS[card.instrument].tick
    if "min_range_atr" in card.filters and (day.hi - day.lo) / day.atr < card.p("min_range_atr"):
        return []
    max_trades = int(card.p("max_trades_per_day", 1))
    up, dn = _on_tick(day.hi + tick, tick), _on_tick(day.lo - tick, tick)
    allow = {1: card.side in ("long", "both"), -1: card.side in ("short", "both")}
    trades, j, n = [], day.first, len(day.times)
    while j < day.cutoff and len(trades) < max_trades:
        hit = [s for s, lvl in ((1, up), (-1, dn)) if allow[s] and (day.h[j] >= lvl if s > 0 else day.l[j] <= lvl)]
        if not hit:
            j += 1
            continue
        side = min(hit, key=lambda s: abs((up if s > 0 else dn) - day.o[j]))
        lvl = up if side > 0 else dn
        entry = max(lvl, day.o[j]) if side > 0 else min(lvl, day.o[j])
        stop, target = _levels(card, day, side, entry, tick)
        k, px, why = j, None, "flat"
        if (day.l[j] <= stop) if side > 0 else (day.h[j] >= stop):
            px, why = stop, "stop"
        while px is None:
            k += 1
            if k >= day.flat or k >= n:
                k = min(day.flat, n - 1)
                px = day.o[k] if day.flat < n else day.c[n - 1]
                break
            o, h, l = day.o[k], day.h[k], day.l[k]
            if (o <= stop) if side > 0 else (o >= stop):
                px, why = o, "stop"
            elif (l <= stop) if side > 0 else (h >= stop):
                px, why = stop, "stop"
            elif target is not None and ((o >= target) if side > 0 else (o <= target)):
                px, why = o, "target"
            elif target is not None and ((h >= target) if side > 0 else (l <= target)):
                px, why = target, "target"
        trades.append(Trade(day.date, side, j, k, float(entry), float(px), why))
        j = k + 1 if why != "flat" else day.cutoff
    return trades


def simulate(card: Card, bars: pd.DataFrame, dates: list[str]) -> list[Trade]:
    return [t for d in days(card, bars, dates) for t in simulate_day(card, d)]
