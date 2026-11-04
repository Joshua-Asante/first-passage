"""Whole-stack power harness for the strategy builder (zero K, synthetic data only).

Synthetic cards with a known true annual Sharpe go through the builder's own gate code on
``main`` (``lab/builder/gates.py``); nothing here re-implements a gate. DESIGN.md fixes the grid,
path counts, seeds and success criteria before any run.

Series layer (exact): per-session net P&L is built as trades whose net value after the engine's
own per-trade cost is a draw with a known distribution, so the true per-session Sharpe of the
daily series (zero on no-trade days, as ``gates.daily`` builds it) is exact. The gates called are
5a (``THRESHOLDS['5a_min_trades']``), 5c (``gates._halves``), 5f (``gates._dsr_gate``), the
stage-8 look (``gates.holdout_look``) and, after a holdout pass, 5g placement (inside
``holdout_look``). 5b always passes (``COSTS_LABEL``: "not a gate"). 5d and 5e need bars and
are calibrated only in the bar layer.

Bar layer: synthetic 15m MNQ bars with a planted opening-range breakout drift, run through
``gates.evaluate`` (``compile.py`` included) and ``gates.holdout_look``.
"""
from __future__ import annotations

import math
import tempfile
from contextlib import contextmanager
from pathlib import Path
from statistics import NormalDist
from unittest import mock

import numpy as np
import pandas as pd

from builder import cards, gates, ledger
from builder import compile as C

ND = NormalDist()
PY = 252  # sessions per year, as gates.REACH
FIRM = "Tradeify_Select_100K"
CARD_TEXT = """
id: power-mnq-orb
family: orb
instrument: MNQ
entry: {type: breakout, range: first_n_bars, side: both, order: stop}
exit: {stop: range_opposite, target: none, flat_at: "15:45"}
time: {entry_cutoff: "12:00"}
params: {n_bars: {value: 2, step: 1}}
"""
CARD = cards.parse(CARD_TEXT)
COSTS = gates.Costs.for_firm(FIRM, "MNQ")
PV = 2.0  # MNQ point value (builder.instruments)
TRADE_SD_USD = 100.0  # scale of one trade's net P&L; every gate statistic is scale-free

# ---------------------------------------------------------------- payoff shapes (standardised)
# orb_skew: a stopped loser of -1 with probability P_STOP, else a runner THETA * Exp(1).
P_STOP, THETA = 0.6, 1.5
_M0 = -P_STOP + (1 - P_STOP) * THETA
_V0 = P_STOP + (1 - P_STOP) * 2 * THETA ** 2 - _M0 ** 2


def shape_quantile(shape: str, u: np.ndarray) -> np.ndarray:
    """Standardised (mean 0, variance 1) draw from ``shape`` at uniforms ``u`` (exact quantile)."""
    if shape == "normal":
        return np.array([ND.inv_cdf(min(max(x, 1e-15), 1 - 1e-15)) for x in u])
    if shape == "orb_skew":
        z0 = np.where(u < P_STOP, -1.0, -THETA * np.log1p(-np.clip((u - P_STOP) / (1 - P_STOP), 0, 1 - 1e-15)))
        return (z0 - _M0) / math.sqrt(_V0)
    raise ValueError(shape)


def trade_mean(s_session: float, q: float) -> float:
    """Mean of one trade's standardised net P&L so that the daily series x = I*Y (I ~ Bern(q),
    Y = mu + Z, Var Z = 1) has per-session Sharpe s: E x = q mu, Var x = q(1 + mu^2) - q^2 mu^2."""
    d = q - s_session ** 2 * (1 - q)
    if d <= 0:
        raise ValueError(f"Sharpe {s_session} per session unreachable at trade rate {q}")
    return math.copysign(abs(s_session) / math.sqrt(d), s_session)


# ---------------------------------------------------------------- series layer
def dates(n: int) -> list[str]:
    return [str(d.date()) for d in pd.bdate_range("2000-01-03", periods=n)]


def to_trades(day_idx: np.ndarray, net_usd: np.ndarray, ds: list[str]) -> list[C.Trade]:
    """compile.Trade objects whose engine net (points * PV - cost) equals ``net_usd``."""
    c = COSTS.per_trade("MNQ")
    return [C.Trade(ds[i], 1, 0, 1, 1000.0, 1000.0 + (v + c) / PV, "flat") for i, v in zip(day_idx, net_usd)]


@contextmanager
def series_holdout(trades: list[C.Trade]):
    """Let the real ``gates.holdout_look`` read synthetic trades instead of simulating bars: only
    the bar-reading calls are replaced; the ledger, the pass rule and 5g placement are the engine's."""
    with mock.patch.object(gates, "check_dates", lambda *a, **k: None), \
            mock.patch.object(gates.C, "simulate", lambda *a, **k: trades):
        yield


def series_path(rng: np.random.Generator, S: float, n: int, h: int, q: float, shape: str,
                ks: tuple[int, ...], rho: float, book_sharpe: float, book_active: float) -> dict:
    """One synthetic card through 5a, 5c, 5f (each K), the stage-8 look and 5g placement."""
    s = S / math.sqrt(PY)
    mu = trade_mean(s, q)
    N = n + h
    ds = dates(N)
    # book: active with probability book_active, normal per active day, annual Sharpe book_sharpe
    sb = book_sharpe / math.sqrt(PY)
    mub = trade_mean(sb, book_active)
    zb = rng.standard_normal(N)
    book_on = rng.random(N) < book_active
    book_x = np.where(book_on, (mub + zb) * TRADE_SD_USD, 0.0)
    # card: trade days, latent correlated with the book's latent (Gaussian copula)
    on = rng.random(N) < q
    lat = rho * zb + math.sqrt(1 - rho ** 2) * rng.standard_normal(N)
    u = np.array([ND.cdf(v) for v in lat[on]])
    y = (mu + shape_quantile(shape, u)) * TRADE_SD_USD
    idx = np.flatnonzero(on)
    dev_d, hold_d = ds[:n], ds[n:]
    dev_trades = to_trades(idx[idx < n], y[idx < n], ds)
    hold_trades = to_trades(idx[idx >= n], y[idx >= n], ds)
    out = {"trades": len(dev_trades)}
    T = gates.THRESHOLDS
    out["5a"] = len(dev_trades) >= T["5a_min_trades"]
    g: list = []
    half = n // 2
    out["5c"] = gates._halves(g, CARD, dev_trades, COSTS, set(dev_d[:half]), set(dev_d[half:]))
    x = gates.daily(CARD, dev_trades, dev_d, COSTS)
    out["5f"] = {}
    for k in ks:
        gk: list = []
        out["5f"][k] = gates._dsr_gate(gk, x, k)
    book = gates._book(dev_d, x, dict(zip(dev_d, book_x[:n])))
    with tempfile.TemporaryDirectory() as td, series_holdout(hold_trades):
        lp = Path(td) / "ledger.jsonl"
        ledger.append_cards(lp, "power", [CARD])
        look = gates.holdout_look(CARD, None, hold_d, lp, "power", COSTS, closed=frozenset(), book=book)
    out["holdout"] = bool(look["pass"])
    out["placement"] = look["placement"]  # None unless the look passed
    out["placement_any"] = gates.placement(book)["placement"]  # same rule on every path, for 5g's own rate
    return out


def closed_form_5f(S: float, k: int, n: int) -> float:
    """``gates.reachability``'s normal-approximation P(5f pass) at any true annual Sharpe S."""
    from research_utils.deflated_sharpe import expected_max_sharpe
    floor = expected_max_sharpe(k, 1.0 / (n - 1)) + ND.inv_cdf(gates.THRESHOLDS["5f_min_dsr"]) / math.sqrt(n - 1)
    return ND.cdf((S - floor * math.sqrt(PY)) * math.sqrt((n - 1) / PY))


# ---------------------------------------------------------------- bar layer
BAR_SD = 10.0  # points per 15m bar (MNQ-like)
SLOTS = [f"{m // 60:02d}:{m % 60:02d}" for m in range(9 * 60 + 30, 17 * 60, 15)]  # 09:30 .. 16:45


def bar_panel(rng: np.random.Generator, n_days: int, drift: float, start: str = "2000-01-03"):
    """Weekday 15m MNQ bars 09:30-16:45 ET. A random walk with per-bar sd BAR_SD; from the bar
    after the first close outside the 09:30-10:00 range (the card's n_bars=2 range), each bar
    drifts ``drift`` points in the breakout's direction (the planted edge). Prices on the 0.25 grid."""
    days = pd.bdate_range(start, periods=n_days)
    nb = len(SLOTS)
    inc = rng.standard_normal((n_days, nb)) * BAR_SD
    wick = np.abs(rng.standard_normal((n_days, nb, 2))) * BAR_SD * 0.3
    o = np.empty((n_days, nb)); c = np.empty((n_days, nb))
    for d in range(n_days):
        px, hi, lo, side = 20000.0, -np.inf, np.inf, 0
        for j in range(nb):
            o[d, j] = px
            px = px + inc[d, j] + side * drift
            c[d, j] = px
            if j < 2:
                hi, lo = max(hi, o[d, j], px), min(lo, o[d, j], px)
            elif side == 0 and (px > hi or px < lo):
                side = 1 if px > hi else -1
    h = np.maximum(o, c) + wick[..., 0]
    l = np.minimum(o, c) - wick[..., 1]
    r = lambda a: np.round(a * 4) / 4  # noqa: E731
    o, h, l, c = r(o), r(h), r(l), r(c)
    off = pd.to_timedelta([int(t[:2]) * 60 + int(t[3:]) for t in SLOTS], unit="min")
    idx = pd.DatetimeIndex((days.values[:, None] + off.values[None, :]).ravel()).tz_localize("America/New_York")
    b = pd.DataFrame({"open": o.ravel(), "high": h.ravel(), "low": l.ravel(), "close": c.ravel()}, index=idx)
    return b, [str(d.date()) for d in days]


def bar_true_sharpe(rng: np.random.Generator, drift: float, n_days: int) -> tuple[float, float, int]:
    """Population-estimate of the card's annual net Sharpe at ``drift`` from one long panel
    (compile.py + gates.daily). Returns (annual Sharpe, its standard error, trades)."""
    b, ds = bar_panel(rng, n_days, drift)
    tr = C.simulate(CARD, b, ds)
    x = gates.daily(CARD, gates.resolved(tr, "calibration"), ds, COSTS)
    s = gates.sharpe(x)
    return s * math.sqrt(PY), math.sqrt((1 + s * s / 2) / len(x)) * math.sqrt(PY), len(tr)


def bar_path(rng: np.random.Generator, drift: float, n: int, h: int, ks: tuple[int, ...]) -> dict:
    """One synthetic bar panel through gates.evaluate (5a-5f at K = ks[0]) and the stage-8 look,
    plus 5f at the other K on the same development series."""
    b, ds = bar_panel(rng, n + h, drift)
    dev, hold = ds[:n], ds[n:]
    with tempfile.TemporaryDirectory() as td:
        lp = Path(td) / "ledger.jsonl"
        ledger.append_cards(lp, "power", [CARD])
        rep = gates.evaluate(CARD, b, dev, lp, COSTS, "synthetic", None, closed=frozenset(), k_scope="instrument")
        out = {"verdict": rep["verdict"], "trades": rep["trades"],
               "gates": {gg["gate"].split()[0]: bool(gg["pass"]) for gg in rep["gates"]}}
        if rep["verdict"] == "unresolved":
            return out
        x = gates.daily(CARD, C.simulate(CARD, b, dev), dev, COSTS)
        out["5f_k"] = {k: gates._dsr_gate([], x, k) for k in ks}
        # the look is taken for every path so the holdout's own rate is measured; the stack
        # counts it only where 5a-5f passed
        look = gates.holdout_look(CARD, b, hold, lp, "power", COSTS, closed=frozenset(), book=rep["book"])
        out["holdout"] = bool(look["pass"])
    return out
