"""5e placebo diagnostic, T1 and T2 (zero K, synthetic data only; DESIGN.md is frozen before any run).

Production code is called, never changed: ``compile.days``/``simulate_day`` make the card's trades,
``gates.net`` prices them and ``frozen_placebo.placebo_beaten_share`` is the production 5e statistic
as it stood before #1074 (engine ``10f0eb19…``; #1074 replaced it with the window slide). The only
re-implementation is ``beaten_shares``, which repeats the production placebo's draw sequence
exactly (validated path by path against the production function, V1) so that two diagnostic side
rules can share the same entry-bar and hold draws:

- ``realised``: the trade's realised side (production behaviour);
- ``causal``: the side of the range midpoint the drawn bar opens on, known at that bar's open;
- ``coin``: a fair coin, independent of the path.

Bars are path-consistent: each 15m bar is the open, high, low and close of 15 one-minute steps of
a Gaussian random walk, so a stop that a bar's high or low reaches is reached by the path itself.
That removes #1067's short-wick fill artefact (its V2 miss). The card, firm and costs are #1067's.
"""
from __future__ import annotations

import math

import numpy as np
import pandas as pd

from builder import cards, gates
from builder import compile as C
from builder.instruments import INSTRUMENTS
from research_utils.camp_import import load_camp_sibling

FROZEN = load_camp_sibling("frozen_placebo", __file__)

FIRM = "Tradeify_Select_100K"
CARD_TEXT = """
id: diag-mnq-orb
family: orb
instrument: MNQ
entry: {type: breakout, range: first_n_bars, side: both, order: stop}
exit: {stop: range_opposite, target: none, flat_at: "15:45"}
time: {entry_cutoff: "12:00"}
params: {n_bars: {value: 2, step: 1}}
"""
CARD = cards.parse(CARD_TEXT)
COSTS = gates.Costs.for_firm(FIRM, "MNQ")
BAR_SD = 10.0          # points per 15m bar, as #1067
MIN_PER_BAR = 15
SLOTS = [f"{m // 60:02d}:{m % 60:02d}" for m in range(9 * 60 + 30, 17 * 60, 15)]  # 09:30 .. 16:45
RANGE_BARS = 2         # the card's n_bars: the 09:30-10:00 range
PY = 252
SIDE_MODES = ("realised", "causal", "coin")


def bar_panel(rng: np.random.Generator, n_days: int, drift: float, start: str = "2000-01-03"):
    """Weekday 15m MNQ bars 09:30-16:45 ET built from a one-minute Gaussian walk (per-minute sd
    BAR_SD/sqrt(15)). From the bar after the first 15m close outside the 09:30-10:00 range, every
    minute drifts ``drift``/15 points in the breakout's direction (``drift`` points per bar).
    OHLC are the minute path's open, max, min and close, rounded to the 0.25 grid."""
    nb = len(SLOTS)
    sd = BAR_SD / math.sqrt(MIN_PER_BAR)
    o = np.empty((n_days, nb)); h = np.empty((n_days, nb)); l = np.empty((n_days, nb)); c = np.empty((n_days, nb))
    px = np.full(n_days, 20000.0)
    hi = np.full(n_days, -np.inf); lo = np.full(n_days, np.inf)
    side = np.zeros(n_days)
    for j in range(nb):
        steps = rng.standard_normal((n_days, MIN_PER_BAR)) * sd + (side * drift / MIN_PER_BAR)[:, None]
        path = px[:, None] + np.cumsum(steps, axis=1)
        o[:, j] = px
        h[:, j] = np.maximum(px, path.max(axis=1))
        l[:, j] = np.minimum(px, path.min(axis=1))
        px = path[:, -1]
        c[:, j] = px
        if j < RANGE_BARS:
            hi, lo = np.maximum(hi, h[:, j]), np.minimum(lo, l[:, j])
        else:
            brk = (side == 0) & ((px > hi) | (px < lo))
            side = np.where(brk, np.where(px > hi, 1.0, -1.0), side)
    r = lambda a: np.round(a * 4) / 4  # noqa: E731
    o, h, l, c = r(o), r(h), r(l), r(c)
    days = pd.bdate_range(start, periods=n_days)
    off = pd.to_timedelta([int(t[:2]) * 60 + int(t[3:]) for t in SLOTS], unit="min")
    idx = pd.DatetimeIndex((days.values[:, None] + off.values[None, :]).ravel()).tz_localize("America/New_York")
    b = pd.DataFrame({"open": o.ravel(), "high": h.ravel(), "low": l.ravel(), "close": c.ravel()}, index=idx)
    return b, [str(d.date()) for d in days]


def card_trades(bars, ds):
    """The card's trades exactly as gates.evaluate builds them (compile.days + simulate_day)."""
    days = C.days(CARD, bars, ds, {}, frozenset())
    return days, [t for d in days for t in C.simulate_day(CARD, d)]


def beaten_shares(days, trades, runs: int, seed: int, aux: np.random.Generator) -> dict[str, float]:
    """Beaten share under each side rule. The production draw sequence (rng = default_rng(seed),
    one ``integers(first, cutoff, size=runs)`` call per trade in trade order) is repeated exactly,
    so ``realised`` equals frozen_placebo.placebo_beaten_share. ``aux`` supplies coin flips and midpoint
    ties only, so it never perturbs the shared entry-bar draws."""
    pv, cost = INSTRUMENTS[CARD.instrument].point_value, COSTS.per_trade(CARD.instrument)
    by = {d.date: d for d in days}
    rng = np.random.default_rng(seed)
    tot = {m: np.zeros(runs) for m in SIDE_MODES}
    for t in trades:
        d = by[t.date]
        e = rng.integers(d.first, d.cutoff, size=runs)
        x = np.minimum(e + (t.exit_i - t.entry_i), d.flat)
        n = len(d.times)
        exit_px = np.where(x < n, d.o[np.minimum(x, n - 1)], d.c[n - 1])
        exit_px = np.where(x == e, d.c[e], exit_px)
        move = exit_px - d.o[e]
        mid = (d.hi + d.lo) / 2
        coin = np.where(aux.random(runs) < 0.5, 1.0, -1.0)
        causal = np.where(d.o[e] > mid, 1.0, np.where(d.o[e] < mid, -1.0, coin))
        tot["realised"] += t.side * move * pv - cost
        tot["causal"] += causal * move * pv - cost
        tot["coin"] += coin * move * pv - cost
    real = gates.net(CARD, trades, COSTS).sum()
    return {m: float((tot[m] < real).mean()) for m in SIDE_MODES}


def path_result(rng: np.random.Generator, aux: np.random.Generator, drift: float, n: int) -> dict:
    """One synthetic development window: the card's trades, the production 5e beaten share and the
    three diagnostic side rules on the same draws."""
    b, ds = bar_panel(rng, n, drift)
    days, trades = card_trades(b, ds)
    if any(t.unresolved for t in trades):
        return {"unresolved": True}
    T = gates.THRESHOLDS
    prod = FROZEN.placebo_beaten_share(CARD, days, trades, COSTS, T["5e_placebo_runs"], T["5e_seed"])
    sh = beaten_shares(days, trades, T["5e_placebo_runs"], T["5e_seed"], aux)
    x = gates.daily(CARD, trades, ds, COSTS)
    gross = sum(t.points for t in trades) * INSTRUMENTS["MNQ"].point_value
    return {"unresolved": False, "trades": len(trades), "v1_equal": prod == sh["realised"], "production": prod,
            **{f"share_{m}": v for m, v in sh.items()}, "net_usd": float(gates.net(CARD, trades, COSTS).sum()),
            "gross_usd": float(gross), "net_annual_sharpe": gates.sharpe(x) * math.sqrt(PY)}


def daily_net_gross(rng: np.random.Generator, drift: float, n_days: int) -> tuple[np.ndarray, np.ndarray]:
    """The card's daily net and gross P&L series (zero on no-trade days) on one long panel."""
    b, ds = bar_panel(rng, n_days, drift)
    _, tr = card_trades(b, ds)
    x = gates.daily(CARD, gates.resolved(tr, "calibration"), ds, COSTS)
    pos = {d: i for i, d in enumerate(ds)}
    g = x + COSTS.per_trade("MNQ") * np.bincount([pos[t.date] for t in tr], minlength=len(ds))
    return x, g
