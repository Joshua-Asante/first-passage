"""MSL-S4 Explore-confirm -- `expiry-oi-strike-convergence` (MGC).

Corrects the informal 2026-08-21 cheap falsifier's naive fixed-offset control
window, which turned out to be trend-confounded (same cycles converged/
diverged in BOTH arm and control -- see the falsifier LOG's addendum). This
is the pre-registered PRIMARY significance test: an IAAFT-surrogate null,
following the same methodology this repo already proved out for an
analogous autocorrelation-confound problem
(docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md) --
adapted here from a TR-persistence conditional-hit-rate statistic to a
strike-convergence statistic on GC price levels.

Frozen geometry: EXPLORE_GO.DRAFT.md. Pulling logic (definition/statistics/
ohlcv-1d schema use, cycle discovery from live Databento definition
snapshots) extends the proven pattern from
_cheap_falsifier_expiry_oi_strike_convergence_2026-08-21.py to also cover
weekly OG expiries, not just monthlies.

Everything in this file is unit-testable on synthetic fixtures (no vendor
data required) -- see test_explore_confirm_lib.py. Functions that pull from
Databento live in a separate runner module so the statistical core can be
tested without DATABENTO_API_KEY.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

import numpy as np

# ---- FROZEN (EXPLORE_GO.DRAFT.md) --------------------------------------------
K_INTRINSIC = 1
DSR_FLOOR = 0.650
RT_USD_MGC = 4.12
FOUR_X_RT_USD_MGC = 16.48

ARM_WINDOW_BDAYS = 3          # sessions before expiry (PREREG_G0.md Sec1 default N=3)
DISPLACEMENT_THRESHOLD_PTS = 3.0

# Partitions -- see EXPLORE_GO.DRAFT.md for the full accounting of what the
# 2026-08-21 TV backtest + cheap falsifier already viewed.
IS_START = np.datetime64("2024-01-01")
IS_END = np.datetime64("2025-03-31")
CONFIRM_START = np.datetime64("2025-04-01")
CONFIRM_END = np.datetime64("2025-09-29")
ALREADY_VIEWED_START = np.datetime64("2025-09-30")  # excluded from IS and CONFIRM
ALREADY_VIEWED_END = np.datetime64("2026-08-21")

# IAAFT null -- generation domain, seed provenance, escalation ladder mirror
# the corrected-null-battery precedent's conventions (not its calibrated
# tolerance NUMBERS, which were fit to a different series -- see
# EXPLORE_GO.DRAFT.md Sec "Diagnostic gate" for why those aren't reused
# verbatim and what pilot-calibration step is owed before the official run).
IAAFT_ITER_DEFAULT = 100
IAAFT_ITER_ESCALATED = 500
IAAFT_M = 1000
IAAFT_SEED_BLOCK = 20260821  # official block: default_rng([IAAFT_SEED_BLOCK, i]), i=0..M-1
IAAFT_PILOT_SEED_BLOCK = 990000  # disjoint from the official block, verification only


# ============================================================================
# IAAFT surrogate generation
# ============================================================================

def van_der_waerden_scores(x: np.ndarray) -> np.ndarray:
    """Rank-Gaussianize x (normal-scores transform). Ties broken by stable
    ordinal rank (temporal order), matching the corrected-null-battery's
    ratified tie convention (A10-i) -- not averaged mid-rank."""
    n = len(x)
    order = np.argsort(x, kind="stable")
    ranks = np.empty(n, dtype=float)
    ranks[order] = np.arange(1, n + 1)
    from scipy import stats as _stats
    return _stats.norm.ppf(ranks / (n + 1))


def iaaft_surrogate(x: np.ndarray, n_iter: int, rng: np.random.Generator) -> np.ndarray:
    """Schreiber-Schmitz IAAFT surrogate of x: exact value multiset of x
    (bitwise-exact marginal), power spectrum iteratively matched to x's own
    (approximate linear-ACF fidelity). Caller supplies n_iter and rng --
    this function does not itself decide the generation domain (raw vs
    normal-scores); see generate_surrogate_returns for that decision.
    """
    x = np.asarray(x, dtype=float)
    n = len(x)
    target_spec = np.abs(np.fft.rfft(x))
    sorted_x = np.sort(x)
    y = rng.permutation(x)
    for _ in range(n_iter):
        f = np.fft.rfft(y)
        phases = np.angle(f)
        y_spec = np.fft.irfft(target_spec * np.exp(1j * phases), n=n)
        ranks = np.argsort(np.argsort(y_spec, kind="stable"), kind="stable")
        y = sorted_x[ranks]
    return y


def generate_surrogate_returns(
    real_returns: np.ndarray,
    rng: np.random.Generator,
    *,
    n_iter: int = IAAFT_ITER_DEFAULT,
    domain: str = "normal_scores",
) -> np.ndarray:
    """One IAAFT surrogate of a log-return series, in the frozen-default
    normal-scores domain (per the corrected-null-battery's own finding that
    raw-domain IAAFT is empirically disqualified for spike/skew-inflated
    series -- returns are less skewed than True Range, but normal-scores is
    adopted as the safe default here too, consistent with precedent, rather
    than re-deriving the raw-vs-normal-scores question from scratch without
    real data to test it on).

    Returns a surrogate series in the SAME units as real_returns (the
    normal-scores transform is inverted via rank-remap onto the real
    sorted returns, exactly as van_der_waerden_scores + iaaft_surrogate's
    own rank-remap step already does for the raw-domain case -- so this
    function's output is directly usable as a return series, never scores).
    """
    if domain == "raw":
        return iaaft_surrogate(real_returns, n_iter, rng)
    if domain != "normal_scores":
        raise ValueError(f"unknown domain: {domain}")
    scores = van_der_waerden_scores(real_returns)
    surrogate_scores = iaaft_surrogate(scores, n_iter, rng)
    # Rank-remap the surrogate SCORES back onto the real RETURNS' own sorted
    # values -- final output has the real returns' exact value multiset,
    # normal-scores-domain spectral matching.
    order = np.argsort(surrogate_scores, kind="stable")
    ranks = np.empty(len(surrogate_scores), dtype=int)
    ranks[order] = np.arange(len(surrogate_scores))
    return np.sort(real_returns)[ranks]


def rank_acf(x: np.ndarray, lag: int) -> float:
    """Spearman-style rank autocorrelation at `lag` (diagnostic domain per
    the corrected-null-battery's A10-ii ratification: gate on rank-ACF, not
    raw-value ACF)."""
    n = len(x)
    if lag >= n:
        return float("nan")
    r = np.argsort(np.argsort(x, kind="stable"), kind="stable").astype(float)
    r = r - r.mean()
    denom = np.dot(r, r)
    if denom == 0:
        return float("nan")
    return float(np.dot(r[:-lag], r[lag:]) / denom)


def surrogate_diagnostic(
    real_returns: np.ndarray,
    surrogate_returns: np.ndarray,
    lags: Sequence[int] = (1, 2, 3, 5, 10, 20),
) -> dict:
    """Per-surrogate rank-ACF fidelity table. Does NOT itself gate -- the
    EXPLORE_GO token names the tolerance (pilot-calibration owed, see
    EXPLORE_GO.DRAFT.md) that consumes this output."""
    real_r = {lag: rank_acf(real_returns, lag) for lag in lags}
    surr_r = {lag: rank_acf(surrogate_returns, lag) for lag in lags}
    delta = {lag: abs(real_r[lag] - surr_r[lag]) for lag in lags}
    return {
        "real_rank_acf": real_r,
        "surrogate_rank_acf": surr_r,
        "abs_delta": delta,
        "max_abs_delta": max(delta.values()),
        "multiset_exact": bool(np.array_equal(np.sort(real_returns), np.sort(surrogate_returns))),
    }


# ============================================================================
# Convergence statistic (arm-window displacement reduction)
# ============================================================================

@dataclass(frozen=True)
class Cycle:
    """One options-expiry cycle's frozen covariates -- real, never surrogated."""
    contract: str
    expiry: str  # ISO date
    strike_star: float  # highest-OI strike, real
    arm_start_idx: int  # index into the shared price-series array
    arm_end_idx: int
    sham_reference: float = field(default=float("nan"))  # DELETE-test level


def displacement_reduction(price: np.ndarray, cycle: Cycle, *, reference: float | None = None) -> tuple[float, float, bool]:
    """(disp_start, disp_end, converged) for one cycle against a price series
    (real or surrogate) and a reference level (defaults to the cycle's real
    strike; pass `reference=cycle.sham_reference` for the DELETE test)."""
    ref = cycle.strike_star if reference is None else reference
    disp_start = abs(float(price[cycle.arm_start_idx]) - ref)
    disp_end = abs(float(price[cycle.arm_end_idx]) - ref)
    return disp_start, disp_end, disp_end < disp_start


def mean_displacement_reduction(price: np.ndarray, cycles: Sequence[Cycle], *, reference: str = "strike") -> float:
    """Mean(start - end) across cycles -- positive = net convergence."""
    vals = []
    for c in cycles:
        ref = c.sham_reference if reference == "sham" else None
        start, end, _ = displacement_reduction(price, c, reference=ref)
        vals.append(start - end)
    return float(np.mean(vals)) if vals else float("nan")


def convergence_rate(price: np.ndarray, cycles: Sequence[Cycle], *, reference: str = "strike") -> float:
    hits = []
    for c in cycles:
        ref = c.sham_reference if reference == "sham" else None
        _, _, converged = displacement_reduction(price, c, reference=ref)
        hits.append(converged)
    return float(np.mean(hits)) if hits else float("nan")


# ============================================================================
# IAAFT-surrogate significance test (PRIMARY gate)
# ============================================================================

@dataclass(frozen=True)
class SurrogateTestResult:
    real_stat: float
    null_stats: np.ndarray
    p_upper: float
    p_lower: float
    percentile: float


def iaaft_significance_test(
    real_returns: np.ndarray,
    start_price: float,
    cycles: Sequence[Cycle],
    *,
    m: int = IAAFT_M,
    n_iter: int = IAAFT_ITER_DEFAULT,
    seed_block: int = IAAFT_SEED_BLOCK,
    statistic: str = "mean_displacement_reduction",
) -> SurrogateTestResult:
    """Real statistic vs M IAAFT-surrogate-implied nulls, real strikes/dates
    held fixed (only the price PATH is surrogated -- see EXPLORE_GO.DRAFT.md
    for why this isolates the right variable). Reconstructs a surrogate
    price path by cumsum-ing surrogate log-returns from the real starting
    price, so displacement-from-strike stays in real price units.
    """
    stat_fn = {
        "mean_displacement_reduction": mean_displacement_reduction,
        "convergence_rate": convergence_rate,
    }[statistic]

    real_price = start_price * np.exp(np.concatenate([[0.0], np.cumsum(real_returns)]))
    real_stat = stat_fn(real_price, cycles)

    null_stats = np.empty(m, dtype=float)
    for i in range(m):
        rng = np.random.default_rng([seed_block, i])
        surr_returns = generate_surrogate_returns(real_returns, rng, n_iter=n_iter)
        surr_price = start_price * np.exp(np.concatenate([[0.0], np.cumsum(surr_returns)]))
        null_stats[i] = stat_fn(surr_price, cycles)

    p_upper = (1 + np.sum(null_stats >= real_stat)) / (m + 1)
    p_lower = (1 + np.sum(null_stats <= real_stat)) / (m + 1)
    percentile = float(np.mean(null_stats <= real_stat) * 100)
    return SurrogateTestResult(real_stat, null_stats, float(p_upper), float(p_lower), percentile)


# ============================================================================
# Req 1a delete/flip (distinct from the IAAFT null -- tests whether the
# STRIKE SELECTION matters, not whether the effect is statistically real)
# ============================================================================

def delete_pass(constrained_stat: float, sham_stat: float) -> bool:
    """PASS iff the true-strike statistic beats the sham-reference statistic
    (strict). NaN -> not PASS. Mirrors MSL-C2's own delete_pass convention."""
    if not (np.isfinite(constrained_stat) and np.isfinite(sham_stat)):
        return False
    return constrained_stat > sham_stat


def flip_pass(converge_stat: float, diverge_stat: float) -> bool:
    """PASS iff betting on convergence beats betting on divergence (strict)."""
    if not (np.isfinite(converge_stat) and np.isfinite(diverge_stat)):
        return False
    return converge_stat > diverge_stat


# ============================================================================
# Gate vocabulary
# ============================================================================

def explore_verdict(
    *,
    iaaft_p_upper: float,
    delete_passed: bool,
    flip_passed: bool,
    diagnostic_ok: bool,
    n_cycles_is: int,
    n_floor: int = 20,
) -> str:
    """FALSIFIED / SHAPE-CLEAR / AMBIGUOUS-HOLD / VOID -- mirrors MSL-C2's
    gate vocabulary and precedence (diagnostic/coverage failures VOID before
    anything else is read; a real p can't rescue an n-floor miss)."""
    if not diagnostic_ok:
        return "VOID"
    if n_cycles_is < n_floor:
        return "VOID"
    if iaaft_p_upper > 0.95:
        # real stat sits BELOW almost the whole null -- convergence is no
        # better than generic autocorrelated price dynamics
        return "FALSIFIED"
    if iaaft_p_upper <= 0.05 and delete_passed and flip_passed:
        return "SHAPE-CLEAR"
    return "AMBIGUOUS-HOLD"
