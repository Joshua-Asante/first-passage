"""Magdon-Ismail et al. (2004) closed forms for Brownian MDD.

Reference: J. Appl. Prob. 41:147-161
PDF: https://www.cs.rpi.edu/~magdon/ps/journal/drawdown_journal.pdf

G_D(h) = P[max drawdown >= h] on [0, T] for X(t) = sigma W(t) + mu t.
Appendix B Q_p / Q_n tables sanity-check E[MDD] recovered by integrating G_D.
Static barrier G_H is the lower first-passage probability (Appendix A limb).
"""

from __future__ import annotations

import json
import math
from functools import lru_cache
from pathlib import Path
from typing import Iterable

import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm

GAMMA = math.sqrt(math.pi / 8.0)  # ≈ 0.626657
_FIXTURES = Path(__file__).resolve().parent / "fixtures"
_EPS = 1e-12
_N_THETA_DEFAULT = 200


@lru_cache(maxsize=4096)
def _theta_roots_cached(beta: float, n_roots: int) -> tuple[float, ...]:
    """Positive solutions of tan(theta) = beta * theta (beta = sigma^2/(mu h))."""
    roots: list[float] = []
    if beta > 0:
        k = 0 if beta > 1.0 + 1e-14 else 1
    else:
        k = 0
    guard = 0
    while len(roots) < n_roots and guard < n_roots * 4:
        guard += 1
        if beta > 0:
            left = k * math.pi + 1e-9
            right = k * math.pi + math.pi / 2.0 - 1e-9
        else:
            left = k * math.pi + math.pi / 2.0 + 1e-9
            right = (k + 1) * math.pi - 1e-9
        k += 1
        if right <= left:
            continue

        def f(theta: float, b: float = beta) -> float:
            return math.tan(theta) - b * theta

        try:
            fl, fr = f(left), f(right)
        except ValueError:
            continue
        if fl * fr > 0:
            continue
        try:
            root = float(brentq(f, left, right))
        except ValueError:
            continue
        if root > 1e-8:
            roots.append(root)
    return tuple(roots)


def _theta_roots(mu: float, sigma: float, h: float, n_roots: int) -> list[float]:
    """Positive solutions of tan(theta) = (sigma^2 / (mu h)) * theta."""
    if abs(mu) < _EPS:
        return [(n - 0.5) * math.pi for n in range(1, n_roots + 1)]
    beta = (sigma * sigma) / (mu * h)
    return list(_theta_roots_cached(round(beta, 12), n_roots))


def _eta_root(mu: float, sigma: float, h: float) -> float:
    """Unique positive solution of tanh(eta) = (sigma^2/(mu h)) * eta when 0 < beta < 1."""
    beta = (sigma * sigma) / (mu * h)
    if not (0.0 < beta < 1.0):
        raise ValueError(f"eta undefined for beta={beta}")

    def f(eta: float) -> float:
        return math.tanh(eta) - beta * eta

    # root in (0, artanh-region); for beta in (0,1) exists in (0, ~pi-ish)
    hi = 20.0
    while f(hi) > 0 and hi < 1e4:
        hi *= 2.0
    return float(brentq(f, _EPS, hi))


def _L_term(h: float, mu: float, sigma: float, T: float) -> float:
    """Additive L in Magdon-Ismail eq. (2)/(4)."""
    s2 = sigma * sigma
    s4 = s2 * s2
    thresh = s2 / h
    if mu < thresh - 1e-14:
        return 0.0
    if abs(mu - thresh) <= 1e-14:
        return (3.0 / math.e) * (1.0 - math.exp(-mu * mu * T / (2.0 * s2)))

    # mu > sigma^2 / h
    eta = _eta_root(mu, sigma, h)
    denom = s4 * eta * eta - mu * mu * h * h + s2 * mu * h
    if abs(denom) < _EPS:
        return 0.0
    pref = (
        2.0
        * s4
        * eta
        * math.sinh(eta)
        * math.exp(-mu * h / s2)
        / denom
    )
    inside = 1.0 - math.exp(
        -mu * mu * T / (2.0 * s2) + s2 * eta * eta * T / (2.0 * h * h)
    )
    return pref * inside


def g_d_zero_drift(h: float, sigma: float, T: float, n_terms: int = _N_THETA_DEFAULT) -> float:
    """Eq. (14): mu = 0."""
    if h <= 0 or T <= 0 or sigma <= 0:
        return 1.0 if h <= 0 else 0.0
    total = 0.0
    for n in range(1, n_terms + 1):
        half = n - 0.5
        theta = half * math.pi
        weight = math.sin(theta) / theta
        expo = -((sigma * theta) ** 2) * T / (2.0 * h * h)
        term = weight * (1.0 - math.exp(expo))
        if abs(term) < 1e-16 and n > 20:
            break
        total += term
    return float(min(1.0, max(0.0, 2.0 * total)))


def g_d(
    h: float,
    mu: float,
    sigma: float,
    T: float,
    n_terms: int = _N_THETA_DEFAULT,
) -> float:
    """G_D(h) = P[max drawdown >= h] on [0, T] (Magdon-Ismail eqs. 2 / 14)."""
    if h <= 0:
        return 1.0
    if T <= 0 or sigma <= 0:
        return 0.0
    if abs(mu) < _EPS:
        return g_d_zero_drift(h, sigma, T, n_terms)

    s2 = sigma * sigma
    s4 = s2 * s2
    thetas = _theta_roots(mu, sigma, h, n_terms)
    series = 0.0
    for theta in thetas:
        denom = s4 * theta * theta + (mu * h) ** 2 - s2 * mu * h
        if abs(denom) < _EPS:
            continue
        decay = math.exp(
            -(s2 * theta * theta * T) / (2.0 * h * h) - (mu * mu * T) / (2.0 * s2)
        )
        term = (theta * math.sin(theta) / denom) * (1.0 - decay)
        series += term
        if abs(term) < 1e-16 and abs(series) > 0:
            # keep going through reserved roots; cheap
            pass

    val = 2.0 * s4 * math.exp(-mu * h / s2) * series + _L_term(h, mu, sigma, T)
    return float(min(1.0, max(0.0, val)))


def g_h_static(h: float, mu: float, sigma: float, T: float) -> float:
    """P(tau_{-h} <= T) for BM — static lower barrier at -h (Appendix A / IG FP).

    Starting at 0: P(min_{t<=T} X(t) <= -h).
    """
    if h <= 0:
        return 1.0
    if T <= 0 or sigma <= 0:
        return 0.0
    srt = sigma * math.sqrt(T)
    a = -h
    # Standard formula for hitting a < 0:
    # Phi((a - mu T)/(sig sqrt T)) + exp(2 mu a / sig^2) Phi((a + mu T)/(sig sqrt T))
    term1 = norm.cdf((a - mu * T) / srt)
    term2 = math.exp(2.0 * mu * a / (sigma * sigma)) * norm.cdf((a + mu * T) / srt)
    return float(min(1.0, max(0.0, term1 + term2)))


def expected_mdd_zero_drift(sigma: float, T: float) -> float:
    """E[D_bar] = 2 * gamma * sigma * sqrt(T) for mu=0."""
    return 2.0 * GAMMA * sigma * math.sqrt(T)


def integrate_expected_mdd(
    mu: float,
    sigma: float,
    T: float,
    h_max: float | None = None,
    n_grid: int = 400,
    n_terms: int = 120,
) -> float:
    """E[D_bar] = integral_0^inf G_D(h) dh via trapezoid on [0, h_max]."""
    if abs(mu) < _EPS:
        return expected_mdd_zero_drift(sigma, T)
    if h_max is None:
        # generous tail: several expected scales
        h_max = max(20.0 * sigma * math.sqrt(T), 20.0 * abs(sigma * sigma / mu))
    hs = np.linspace(_EPS, h_max, n_grid)
    gs = np.array([g_d(float(h), mu, sigma, T, n_terms=n_terms) for h in hs])
    return float(np.trapezoid(gs, hs))


def q_from_expected_mdd(e_mdd: float, mu: float, sigma: float) -> float:
    """Invert E[D]= (2 sigma^2 / |mu|) Q  (sign conventions of eqs. 6 / 18)."""
    return e_mdd * abs(mu) / (2.0 * sigma * sigma)


def load_appendix_b(kind: str) -> list[tuple[float, float]]:
    path = _FIXTURES / (f"appendix_b_{kind}.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    return [(float(p["x"]), float(p["Q"])) for p in data["points"]]


def interpolate_table(x: float, table: list[tuple[float, float]]) -> float:
    xs = [t[0] for t in table]
    qs = [t[1] for t in table]
    if x <= xs[0]:
        return qs[0]
    if x >= xs[-1]:
        return qs[-1]
    return float(np.interp(x, xs, qs))


def check_appendix_b(
    kind: str,
    sample_x: Iterable[float] | None = None,
    sigma: float = 1.0,
    tol: float = 5e-3,
    n_grid: int = 120,
    include_integral: bool = False,
) -> list[dict]:
    """Sanity-check Appendix B tables (role A).

    Primary: paper asymptotics vs transcribed values.
      x→0: Q ≈ gamma * sqrt(2x)
      Qp x→∞: (1/4) log x + 0.49088
      Qn x→∞: x + 1/2
    Optional: one mid-x integral of G_D → Q (expensive; coarse grid).
    """
    table = load_appendix_b(kind)
    rows: list[dict] = []

    # Small-x asymptotics on the first few table rows
    for x, q_tab in table[:5]:
        q_asym = GAMMA * math.sqrt(2.0 * x)
        err = abs(q_tab - q_asym)
        # tables are approximate; small-x agreement loosens slightly
        rows.append(
            {
                "kind": kind,
                "check": "asym_small",
                "x": x,
                "Q_impl": q_asym,
                "Q_table": q_tab,
                "abs_err": err,
                "pass": err <= max(tol, 0.01),
                "tol": max(tol, 0.01),
            }
        )

    # Large-x asymptotics on the last table row
    x_big, q_tab_big = table[-1]
    if kind == "qp":
        q_asym_big = 0.25 * math.log(x_big) + 0.49088
    else:
        q_asym_big = x_big + 0.5
    err_big = abs(q_tab_big - q_asym_big)
    rows.append(
        {
            "kind": kind,
            "check": "asym_large",
            "x": x_big,
            "Q_impl": q_asym_big,
            "Q_table": q_tab_big,
            "abs_err": err_big,
            "pass": err_big <= max(tol, 0.02),
            "tol": max(tol, 0.02),
        }
    )

    if include_integral:
        # Single mid-range integral recovery (one x only — G_D integrate is O(n_grid * n_terms))
        xs = list(sample_x) if sample_x is not None else ([0.5] if kind == "qp" else [0.5])
        x = xs[0]
        mu = 1.0 if kind == "qp" else -1.0
        T = 2.0 * x * (sigma**2) / (mu * mu)
        e_mdd = integrate_expected_mdd(mu, sigma, T, n_grid=n_grid, n_terms=60)
        q_impl = q_from_expected_mdd(e_mdd, mu, sigma)
        q_tab = interpolate_table(x, table)
        err = abs(q_impl - q_tab)
        # Integration truncation is coarse; allow wider band than pure table tol
        int_tol = max(tol, 0.05)
        rows.append(
            {
                "kind": kind,
                "check": "integral_G_D",
                "x": x,
                "Q_impl": q_impl,
                "Q_table": q_tab,
                "abs_err": err,
                "pass": err <= int_tol,
                "tol": int_tol,
            }
        )
    return rows


def solve_h_static_equiv(
    h_trail: float,
    mu: float,
    sigma: float,
    T: float,
    n_terms: int = 120,
) -> tuple[float, float]:
    """Solve G_D(h_trail) = G_H(h_static) for h_static > 0. Returns (h_static, G)."""
    g_target = g_d(h_trail, mu, sigma, T, n_terms=n_terms)
    if g_target <= 0.0:
        return float("inf"), 0.0
    if g_target >= 1.0 - 1e-12:
        return 0.0, 1.0

    def f(h_s: float) -> float:
        return g_h_static(h_s, mu, sigma, T) - g_target

    # G_H decreases in h_static; bracket
    lo, hi = _EPS, max(h_trail * 20.0, 50.0 * sigma * math.sqrt(T))
    while f(hi) > 0 and hi < 1e8:
        hi *= 2.0
    if f(lo) * f(hi) > 0:
        # target may sit outside bracket; fall back to lo/hi extremes
        return float(hi if abs(f(hi)) < abs(f(lo)) else lo), g_target
    h_s = float(brentq(f, lo, hi))
    return h_s, g_target


if __name__ == "__main__":
    for kind in ("qp", "qn"):
        for row in check_appendix_b(kind, include_integral=False):
            flag = "PASS" if row["pass"] else "FAIL"
            print(
                f"{flag} {row['kind']} {row['check']} x={row['x']}: "
                f"Q_impl={row['Q_impl']:.6f} Q_tab={row['Q_table']:.6f} "
                f"err={row['abs_err']:.6f}"
            )
    print("mu0 G_D(h=2,sig=1,T=1)=", g_d(2.0, 0.0, 1.0, 1.0))
    print("E[MDD] mu0=", expected_mdd_zero_drift(1.0, 1.0))
