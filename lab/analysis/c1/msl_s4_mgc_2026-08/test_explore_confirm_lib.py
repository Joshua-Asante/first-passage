"""Unit tests for explore_confirm_lib.py -- synthetic fixtures only, no
vendor data or DATABENTO_API_KEY required. Run standalone:
    python -m pytest lab/analysis/c1/msl_s4_mgc_2026-08/test_explore_confirm_lib.py -q
"""
from __future__ import annotations

import numpy as np
import pytest

from research_utils.camp_import import load_camp_sibling

lib = load_camp_sibling("explore_confirm_lib", __file__)


# ============================================================================
# IAAFT core
# ============================================================================

def test_iaaft_surrogate_preserves_exact_value_multiset():
    rng = np.random.default_rng(42)
    x = rng.normal(size=300).cumsum() * 0.01
    y = lib.iaaft_surrogate(x, n_iter=50, rng=np.random.default_rng(1))
    assert np.allclose(np.sort(x), np.sort(y))


def test_iaaft_surrogate_beats_naive_shuffle_on_autocorrelation():
    rng = np.random.default_rng(7)
    # AR(1)-like trending series -- real financial log-returns have
    # meaningfully more autocorrelation than white noise.
    innov = rng.normal(size=400)
    x = np.cumsum(innov * 0.3 + np.roll(innov, 1) * 0.7)
    surrogate = lib.iaaft_surrogate(x, n_iter=100, rng=np.random.default_rng(2))
    shuffled = rng.permutation(x)
    real_acf1 = lib.rank_acf(x, 1)
    surr_acf1 = lib.rank_acf(surrogate, 1)
    shuf_acf1 = lib.rank_acf(shuffled, 1)
    assert abs(surr_acf1 - real_acf1) < abs(shuf_acf1 - real_acf1)


def test_generate_surrogate_returns_normal_scores_preserves_multiset():
    rng = np.random.default_rng(11)
    returns = rng.standard_t(df=5, size=250) * 0.01  # fat-tailed, like real returns
    surrogate = lib.generate_surrogate_returns(returns, np.random.default_rng(3), n_iter=50)
    assert np.allclose(np.sort(returns), np.sort(surrogate))


def test_van_der_waerden_scores_monotonic_in_input_rank():
    x = np.array([5.0, 1.0, 3.0, 2.0, 4.0])
    scores = lib.van_der_waerden_scores(x)
    # rank order of scores must match rank order of x
    assert np.array_equal(np.argsort(x), np.argsort(scores))


def test_surrogate_diagnostic_reports_exact_multiset_and_small_delta():
    rng = np.random.default_rng(5)
    x = rng.standard_normal(400).cumsum() * 0.005
    surrogate = lib.iaaft_surrogate(x, n_iter=100, rng=np.random.default_rng(6))
    diag = lib.surrogate_diagnostic(x, surrogate)
    assert diag["multiset_exact"] is True
    assert diag["max_abs_delta"] < 0.25  # generous -- real tolerance is a pilot-calibration item


# ============================================================================
# Convergence statistic -- hand-computed fixtures
# ============================================================================

def _price_series():
    # index:      0     1     2     3     4     5
    return np.array([100.0, 102.0, 98.0, 101.0, 99.5, 100.2])


def test_displacement_reduction_hand_computed_converging():
    price = _price_series()
    cycle = lib.Cycle(contract="X1", expiry="2099-01-01", strike_star=100.0,
                       arm_start_idx=1, arm_end_idx=3)  # |102-100|=2 -> |101-100|=1
    disp_start, disp_end, converged = lib.displacement_reduction(price, cycle)
    assert disp_start == pytest.approx(2.0)
    assert disp_end == pytest.approx(1.0)
    assert converged is True


def test_displacement_reduction_hand_computed_diverging():
    price = _price_series()
    cycle = lib.Cycle(contract="X2", expiry="2099-01-01", strike_star=100.0,
                       arm_start_idx=3, arm_end_idx=2)  # |101-100|=1 -> |98-100|=2
    disp_start, disp_end, converged = lib.displacement_reduction(price, cycle)
    assert disp_start == pytest.approx(1.0)
    assert disp_end == pytest.approx(2.0)
    assert converged is False


def test_mean_displacement_reduction_and_convergence_rate_two_cycles():
    price = _price_series()
    c1 = lib.Cycle(contract="X1", expiry="2099-01-01", strike_star=100.0, arm_start_idx=1, arm_end_idx=3)  # reduction +1, converged
    c2 = lib.Cycle(contract="X2", expiry="2099-01-01", strike_star=100.0, arm_start_idx=3, arm_end_idx=2)  # reduction -1, diverged
    mean_red = lib.mean_displacement_reduction(price, [c1, c2])
    rate = lib.convergence_rate(price, [c1, c2])
    assert mean_red == pytest.approx(0.0)  # (+1 + -1) / 2
    assert rate == pytest.approx(0.5)


def test_displacement_reduction_sham_reference():
    price = _price_series()
    cycle = lib.Cycle(contract="X1", expiry="2099-01-01", strike_star=100.0,
                       arm_start_idx=1, arm_end_idx=3, sham_reference=90.0)
    # against the real strike (100): converges (2 -> 1)
    _, _, converged_real = lib.displacement_reduction(price, cycle)
    # against the sham (90): |102-90|=12 -> |101-90|=11, also "converges" numerically
    _, _, converged_sham = lib.displacement_reduction(price, cycle, reference=cycle.sham_reference)
    assert converged_real is True
    assert converged_sham is True  # illustrates why delete_pass compares MAGNITUDES, not just booleans


# ============================================================================
# Delete / flip
# ============================================================================

def test_delete_pass_true_when_constrained_beats_sham():
    assert lib.delete_pass(constrained_stat=1.2, sham_stat=0.3) is True


def test_delete_pass_false_when_sham_beats_constrained():
    assert lib.delete_pass(constrained_stat=0.1, sham_stat=0.9) is False


def test_delete_pass_false_on_nan():
    assert lib.delete_pass(constrained_stat=float("nan"), sham_stat=0.3) is False


def test_flip_pass_true_when_convergence_beats_divergence():
    assert lib.flip_pass(converge_stat=0.8, diverge_stat=0.1) is True


def test_flip_pass_false_when_divergence_beats_convergence():
    assert lib.flip_pass(converge_stat=0.1, diverge_stat=0.8) is False


# ============================================================================
# IAAFT significance test -- power + false-positive control (the
# corrected-null-battery's own "positive control" discipline, adapted)
# ============================================================================

def _synthetic_cycles(n_cycles, series_len, rng, spacing=15, window=3):
    cycles = []
    starts = rng.choice(np.arange(window, series_len - window - spacing, spacing),
                         size=n_cycles, replace=False)
    for i, s in enumerate(sorted(starts)):
        cycles.append(lib.Cycle(
            contract=f"SYN{i}", expiry="2099-01-01", strike_star=0.0,  # set per-test
            arm_start_idx=int(s), arm_end_idx=int(s) + window,
        ))
    return cycles


def test_iaaft_significance_test_null_scenario_does_not_false_positive():
    """No injected mechanism: pure autocorrelated noise, strikes at the
    series' own trailing mean (no real pull). p_upper should NOT be tiny."""
    rng = np.random.default_rng(100)
    n = 500
    innov = rng.normal(size=n) * 0.01
    returns = innov * 0.4 + np.roll(innov, 1) * 0.6  # autocorrelated, no expiry effect
    start_price = 4000.0
    price = start_price * np.exp(np.concatenate([[0.0], np.cumsum(returns)]))

    cycles_raw = _synthetic_cycles(8, n, rng)
    cycles = [lib.Cycle(contract=c.contract, expiry=c.expiry,
                         strike_star=float(price[max(c.arm_start_idx - 20, 0)]),
                         arm_start_idx=c.arm_start_idx, arm_end_idx=c.arm_end_idx)
              for c in cycles_raw]

    result = lib.iaaft_significance_test(returns, start_price, cycles, m=80, n_iter=40)
    assert 0.05 < result.p_upper < 1.0  # not falsely "significant"


def test_iaaft_significance_test_detects_injected_convergence_signal():
    """Injected mechanism: near each cycle's arm window, nudge returns to
    pull price toward a MEANINGFULLY DISPLACED strike (40-100pt gap, same
    order as the real construct's own displacement threshold). The surrogate
    null (which preserves generic autocorrelation but not this specific
    pull) should NOT explain it away -- p_upper should land low.

    Direction is recomputed from the LIVE, incrementally-injected price at
    each bar (not a stale pre-injection snapshot) -- an earlier draft of
    this test computed direction from a fixed snapshot, which let earlier
    cycles' compounding pulls silently invalidate later cycles' gap sign
    and caused net divergence instead of convergence. Caught by this test
    failing, not assumed correct.
    """
    rng = np.random.default_rng(101)
    n = 500
    innov = rng.normal(size=n) * 0.01
    returns = innov * 0.4 + np.roll(innov, 1) * 0.6
    start_price = 4000.0
    window = 5
    nudge = 0.010  # per-bar directional log-return nudge toward the strike

    cycles_raw = _synthetic_cycles(14, n, rng, window=window)
    returns_injected = returns.copy()
    strikes: dict[str, float] = {}
    for c in cycles_raw:
        price_now = start_price * np.exp(np.sum(returns_injected[:c.arm_start_idx]))
        displaced = rng.choice([-1, 1]) * rng.uniform(40, 100)
        strikes[c.contract] = float(price_now + displaced)
        for t in range(c.arm_start_idx, c.arm_end_idx):
            price_t = start_price * np.exp(np.sum(returns_injected[:t]))
            direction = 1.0 if strikes[c.contract] > price_t else -1.0
            returns_injected[t] += direction * nudge

    price_final = start_price * np.exp(np.concatenate([[0.0], np.cumsum(returns_injected)]))
    cycles = [lib.Cycle(contract=c.contract, expiry=c.expiry, strike_star=strikes[c.contract],
                         arm_start_idx=c.arm_start_idx, arm_end_idx=c.arm_end_idx)
              for c in cycles_raw]

    real_stat = lib.mean_displacement_reduction(price_final, cycles)
    result = lib.iaaft_significance_test(returns_injected, start_price, cycles, m=150, n_iter=40)
    assert real_stat > 0  # sanity: the injected pull actually produced net convergence
    assert result.p_upper < 0.05  # the null (autocorrelation alone) should not explain it away


# ============================================================================
# Verdict gate
# ============================================================================

@pytest.mark.parametrize("p_upper,delete_ok,flip_ok,diag_ok,n,expected", [
    (0.5, True, True, False, 50, "VOID"),          # diagnostic fail
    (0.5, True, True, True, 5, "VOID"),            # n-floor miss
    (0.99, True, True, True, 50, "FALSIFIED"),     # real stat below the whole null
    (0.02, True, True, True, 50, "SHAPE-CLEAR"),   # significant + delete + flip PASS
    (0.02, False, True, True, 50, "AMBIGUOUS-HOLD"),  # significant but delete FAILs
    (0.02, True, False, True, 50, "AMBIGUOUS-HOLD"),  # significant but flip FAILs
    (0.5, True, True, True, 50, "AMBIGUOUS-HOLD"), # not significant either way
])
def test_explore_verdict_gate_table(p_upper, delete_ok, flip_ok, diag_ok, n, expected):
    verdict = lib.explore_verdict(
        iaaft_p_upper=p_upper, delete_passed=delete_ok, flip_passed=flip_ok,
        diagnostic_ok=diag_ok, n_cycles_is=n,
    )
    assert verdict == expected
