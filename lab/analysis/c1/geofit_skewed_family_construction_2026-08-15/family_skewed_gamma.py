"""The skew-aware i.i.d. family for a Q-GEOFIT-1 successor -- construction, not a test.

STATUS: scoping construction, follow-up to `geofit_skew_probe_2026-07-25` (confirmed skew is the
dominant missing dimension) and `geofit_iid_sufficiency_power_2026-08-15` (confirmed the true
marginals, i.i.d., are sufficient -- no block structure needed). **Not** part of Q-GEOFIT-1 and not
a re-open of it. No envelope, no grid, no cells, no candidate claim. $0.00 spend, zero K.

===============================================================================
DESIGN DECISION (operator-directed, 2026-08-15 -- record the reasoning, not just the choice)
===============================================================================

The win branch's heavy right tail is a MEASURED feature of the real book, not a fitting artifact:
n=150 real win-days, mean $463.08, median $84.63, max $4,971.88 (10.7x the mean). The
method-of-moments Gamma fit to (mean, sd) forces shape k = mean^2/var = 0.359 -- a distribution
whose own coefficient of variation exceeds 1 (sd 1.67x its mean). That is what threw "monster
realizations" in the original skewed_gamma arm (bust-rate sd 10.85% at N=5), not a defect in the
family choice.

Operator decision: PRESERVE the tail, do not cap it. Capping at any multiple of the observed
max, or deriving a structural bound from position-sizing/pyramid math, would understate exactly the
risk a trailing-DD survival gate exists to price -- a book whose real max win is already 10.7x its
mean is not obviously bounded at 1.5x or 2x that figure, and no Pine source is available in this
worktree to derive a structural cap even if one were wanted. Consequence: this family's win branch
stays an UNCAPPED Gamma(k=0.359-ish, matched per-fit). A future grid scoring cells with this family
must report the SPREAD of bust rate across realizations, not a single point estimate -- the spread
IS the finding, not noise to average away.

The loss branch is not capped either (for symmetry and because nothing forced it), but it does not
need to be: fitted k = 0.920 (near-exponential, CV~1.04), no comparable instability observed.

===============================================================================
WHAT THIS MODULE IS AND IS NOT
===============================================================================

IS: a reusable, documented (fit, draw) pair for the family class validated by the two prior probes
    -- win-rate + separately-parameterized win/loss scales, Gamma-shaped, uncapped, i.i.d. across
    active days, uniform zero-day placement (R4's measured effect was -0.29pp / 0.21 sigma,
    indistinguishable from zero -- clustering is not adopted here for lack of a measured reason to).

IS NOT: a re-derivation of Q-GEOFIT-1's closed 288-cell grid, a new gate, or a candidate-generating
    construct. It exists so a FUTURE successor brief has a validated family to grid, not to grid one
    itself -- that step needs its own pre-registration (z-range, cell count, N-per-cell, scoring
    rule for a spread rather than a point) per brief-authoring / Trap #12 discipline. See this
    directory's README "Open for the successor brief" for what stays undecided here.
"""
from __future__ import annotations

import numpy as np


def fit_family(active: np.ndarray) -> dict:
    """Method-of-moments fit: win-rate + separately-scaled win/loss branches. No cap."""
    a = np.asarray(active, dtype=float).reshape(-1)
    a = a[a != 0.0]
    win, loss = a[a > 0], a[a < 0]
    return {
        "n_active": int(a.size),
        "p_win": float((a > 0).mean()),
        "win_mean": float(win.mean()),
        "win_sd": float(win.std(ddof=1)),
        "win_max": float(win.max()),
        "loss_mean": float(loss.mean()),
        "loss_sd": float(loss.std(ddof=1)),
        "loss_min": float(loss.min()),
        "k_win": float(win.mean() ** 2 / win.var(ddof=1)),
        "k_loss": float(loss.mean() ** 2 / loss.var(ddof=1)),
    }


def _gamma_matched(rng: np.random.Generator, mean: float, sd: float, n: int) -> np.ndarray:
    """Gamma matched to (mean, sd) by method of moments: k = mean^2/var, theta = var/mean.
    UNCAPPED -- see module docstring "Design decision"."""
    var = sd * sd
    k = mean * mean / var
    theta = var / mean
    return rng.gamma(shape=k, scale=theta, size=n)


def draw_series(params: dict, seed: int, n_bdays: int, z: float | None = None) -> np.ndarray:
    """One realization of the family. `z` overrides the fitted n_active/n_bdays ratio (needed to
    extend past the closed family's 0.40 ceiling -- see README item 2); default reuses the fit's
    own active-day count."""
    rng = np.random.default_rng(seed)
    n_active = params["n_active"] if z is None else int(round(n_bdays * (1.0 - z)))
    is_win = rng.random(n_active) < params["p_win"]
    vals = np.empty(n_active, dtype=float)
    n_w, n_l = int(is_win.sum()), int((~is_win).sum())
    if n_w:
        vals[is_win] = _gamma_matched(rng, params["win_mean"], params["win_sd"], n_w)
    if n_l:
        vals[~is_win] = -_gamma_matched(rng, abs(params["loss_mean"]), params["loss_sd"], n_l)
    out = np.zeros(n_bdays, dtype=float)
    idx = np.sort(rng.permutation(n_bdays)[:n_active])  # uniform placement (R4, see docstring)
    out[idx] = vals
    return out
