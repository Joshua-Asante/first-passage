"""Synthetic payoff-shape trade-generating process for the A2 feasibility map.

Not a strategy, not a candidate, not a mechanism. Generates a long synthetic
(daily_pnl, intraday_low) panel for one (win_rate, shape, trades_per_week,
risk_usd) tuple, deterministically seeded, purely as an input to the production
survivor-MC engine (core/mc/simulation.py::simulate_path via
lab/discovery/prop_survivor_scoring.py). See RESULTS.md "Shape generative
process" for the full disclosed parametric form, provenance, and limitations.

Axes are coverage, not selection (task brief, Phase A Task A2). Per-trade risk
levels are EM2's edge-indexed frontier cells, verbatim ($250/$275/$325 --
docs/spec/2026-08-05-eval-mechanism-shape-screen.md EM2 row), used only as
dollar risk-per-trade coverage levels -- never as a claim that any real
candidate achieves the R multiples EM2 originally indexed them to (that
provenance is void per docs/adr/2026-08-08-edge-cohort-correction-and-
necessity-retarget.md; EM2's arithmetic/interpolate-down principle stands).
"""
from __future__ import annotations

from collections import Counter
from typing import Dict, List, Tuple

import numpy as np

N_WEEKS = 520  # ~10 synthetic years -> 520 week-blocks for the engine's block
               # bootstrap to draw from (comparable order of magnitude to real
               # multi-year campaign panels; not calibrated to any real history).
DGP_MASTER_SEED = 20260823  # Seeds ONLY the synthetic trade generator below --
               # orthogonal to, and never a substitute for, the engine's own
               # frozen block-bootstrap seeds (42/123/2026 via
               # load_scoring_thresholds()), which this harness never touches.

WIN_RATES: Tuple[float, ...] = (0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70)
SHAPES: Tuple[str, ...] = ("symmetric", "mild_right_skew", "bounded_clustered")
CADENCES: Tuple[int, ...] = (1, 2, 3, 5, 8)
# EM2 frontier, verbatim. "Interpolate down, never up" is honored by never
# testing a risk level above the top published cell ($325).
RISK_USD: Tuple[float, ...] = (250.0, 275.0, 325.0)

# Deterministic weekday placement (0=Mon..4=Fri), repeats allowed (cadence=8).
# Guarantees every calendar week has >=1 trade for every cadence tested here --
# activity is satisfied STRUCTURALLY by construction, never via the operator
# token-trade path (see RESULTS.md "Activity floor" section).
WEEKDAY_PATTERN: Dict[int, Tuple[int, ...]] = {
    1: (0,),
    2: (0, 2),
    3: (0, 2, 4),
    5: (0, 1, 2, 3, 4),
    8: (0, 0, 1, 1, 2, 2, 3, 4),
}

# Intraday MAE band for WINNING trades only, as a fraction of one stop (1R),
# shape-dependent. Losing trades are modeled as reaching (not slipping past)
# their hard stop -- MAE == the realized loss itself. See module docstring /
# RESULTS.md for the disclosed rationale and limitation (no gap-through-stop
# tail is modeled; that tail is explicitly out of EM3's scope too).
_MAE_BAND: Dict[str, Tuple[float, float]] = {
    "symmetric": (0.20, 0.60),
    "mild_right_skew": (0.30, 0.80),
    "bounded_clustered": (0.10, 0.30),
}

_AXIS_SIZES = (len(SHAPES), len(CADENCES), len(RISK_USD))


def tuple_index(win_rate: float, shape: str, cadence: int, risk: float) -> int:
    """Deterministic enumeration index for one grid tuple -- drives the DGP seed.

    Pure function of the tuple's own coordinates (never of any prior result),
    so re-running this module reproduces byte-identical panels.
    """
    wr_i = WIN_RATES.index(win_rate)
    sh_i = SHAPES.index(shape)
    cd_i = CADENCES.index(cadence)
    rk_i = RISK_USD.index(risk)
    n_sh, n_cd, n_rk = _AXIS_SIZES
    return ((wr_i * n_sh + sh_i) * n_cd + cd_i) * n_rk + rk_i


def all_tuples() -> List[Tuple[float, str, int, float]]:
    """Full 7x3x5x3 = 315 coverage grid, in a fixed, documented enumeration order."""
    out = []
    for wr in WIN_RATES:
        for sh in SHAPES:
            for cd in CADENCES:
                for rk in RISK_USD:
                    out.append((wr, sh, cd, rk))
    return out


def _draw_trade_r(rng: np.random.Generator, shape: str, is_win: bool) -> float:
    """One trade's realized R-multiple (signed; wins > 0, losses < 0)."""
    if shape == "symmetric":
        return float(rng.uniform(0.7, 1.3)) if is_win else -float(rng.uniform(0.7, 1.3))
    if shape == "mild_right_skew":
        return float(1.0 + rng.exponential(0.5)) if is_win else -float(rng.uniform(0.7, 1.3))
    if shape == "bounded_clustered":
        return float(rng.uniform(0.9, 1.1)) if is_win else -1.0
    raise ValueError(f"unknown shape {shape!r}")


def _draw_trade_mae_r(
    rng: np.random.Generator, shape: str, is_win: bool, realized_r: float
) -> float:
    """Worst intraday mark-against before this trade's close, in R-units, <= 0.

    This is the limb that makes the process intraday-honest rather than
    close-only: a day that CLOSES flat or positive can still have touched a
    materially lower point during the session, which is exactly what
    `intraday_low` exists to expose to the trailing-DD barrier (W1 pattern,
    docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md).
    """
    if not is_win:
        return realized_r  # hard-stop reached, not slipped past (disclosed limitation)
    lo, hi = _MAE_BAND[shape]
    return -min(0.95, float(rng.uniform(lo, hi)))


def build_panel(
    win_rate: float, shape: str, cadence: int, risk: float
) -> Tuple[np.ndarray, np.ndarray]:
    """Return (daily_pnl, intraday_low) arrays, N_WEEKS*5 business days long.

    `intraday_low[d]` is the day's worst mark-to-market excursion below that
    day's OPENING equity (<=0, dollars), composed sequentially across however
    many trades land on that day (correct for cadence=8, where two trades can
    share a business day) -- never a naive sum-of-independent-lows.
    """
    if cadence not in WEEKDAY_PATTERN:
        raise ValueError(f"no weekday pattern registered for cadence={cadence}")
    seed = DGP_MASTER_SEED + tuple_index(win_rate, shape, cadence, risk)
    rng = np.random.default_rng(seed)
    counts = Counter(WEEKDAY_PATTERN[cadence])

    n_days = N_WEEKS * 5
    daily = np.zeros(n_days, dtype=float)
    intraday = np.zeros(n_days, dtype=float)

    for w in range(N_WEEKS):
        for wd, n_trades in counts.items():
            cum = 0.0
            day_low = 0.0
            for _ in range(n_trades):
                is_win = bool(rng.random() < win_rate)
                r = _draw_trade_r(rng, shape, is_win)
                mae_r = _draw_trade_mae_r(rng, shape, is_win, r)
                trade_low = cum + mae_r * risk
                if trade_low < day_low:
                    day_low = trade_low
                cum += r * risk
            idx = w * 5 + wd
            daily[idx] = cum
            intraday[idx] = min(0.0, day_low)
    return daily, intraday


def expectancy_r(win_rate: float, shape: str, *, n_draw: int = 200_000, seed: int = 777) -> float:
    """Monte-Carlo expectancy in R-units for a (win_rate, shape) pair -- disclosure only.

    Independent of `build_panel`'s own seeding (fixed diagnostic seed) so this
    is stable regardless of which tuple calls it. Not used by the scoring
    path; exists to annotate RESULTS.md tables with each row's approximate
    per-trade edge.
    """
    rng = np.random.default_rng(seed)
    is_win = rng.random(n_draw) < win_rate
    r = np.empty(n_draw, dtype=float)
    n_win = int(is_win.sum())
    n_loss = n_draw - n_win
    if shape == "symmetric":
        r[is_win] = rng.uniform(0.7, 1.3, n_win)
        r[~is_win] = -rng.uniform(0.7, 1.3, n_loss)
    elif shape == "mild_right_skew":
        r[is_win] = 1.0 + rng.exponential(0.5, n_win)
        r[~is_win] = -rng.uniform(0.7, 1.3, n_loss)
    elif shape == "bounded_clustered":
        r[is_win] = rng.uniform(0.9, 1.1, n_win)
        r[~is_win] = -1.0
    else:
        raise ValueError(f"unknown shape {shape!r}")
    return float(r.mean())


__all__ = [
    "N_WEEKS",
    "DGP_MASTER_SEED",
    "WIN_RATES",
    "SHAPES",
    "CADENCES",
    "RISK_USD",
    "WEEKDAY_PATTERN",
    "all_tuples",
    "tuple_index",
    "build_panel",
    "expectancy_r",
]
