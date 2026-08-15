"""Phase 6a — wire planted controls to Gen-2 DSR (stdlib; no arch/skfolio).

Pre-registered threshold: DSR_PASS_THRESHOLD = 0.95 (LdP default used by the
deflated_sharpe CLI). Negative control must FAIL; positive control must PASS.
"""

from __future__ import annotations

from research_utils.deflated_sharpe import (
    deflated_sharpe,
    expected_max_sharpe,
    moments_from_returns,
)
from validation_selftest import generate_negative_control, generate_positive_control

# Pre-registered before computing DSR on these controls (2026-07-11 bridge B).
DSR_PASS_THRESHOLD = 0.95


def _per_trial_sharpe(returns) -> float:
    sr, *_ = moments_from_returns([float(x) for x in returns])
    return sr


def _dsr_for_control(ctrl) -> float:
    srs = [_per_trial_sharpe(t) for t in ctrl.trial_returns]
    mean = sum(srs) / len(srs)
    var_trials = sum((x - mean) ** 2 for x in srs) / len(srs)
    if var_trials <= 0:
        var_trials = 1e-12
    sr, n, skew, kurt = moments_from_returns(
        [float(x) for x in ctrl.best_returns]
    )
    sr0 = expected_max_sharpe(ctrl.n_trials, var_trials)
    return deflated_sharpe(sr, n, skew, kurt, sr0)


def test_negative_control_fails_dsr_gate():
    """Planted-overfit (noise + IS-best) must not clear the DSR threshold."""
    dsr = _dsr_for_control(generate_negative_control())
    assert dsr < DSR_PASS_THRESHOLD, (
        f"negative control DSR={dsr:.4f} unexpectedly cleared {DSR_PASS_THRESHOLD}"
    )


def test_positive_control_passes_dsr_gate():
    """Planted-real (heterogeneous injected edge) must clear the DSR threshold."""
    dsr = _dsr_for_control(generate_positive_control())
    assert dsr >= DSR_PASS_THRESHOLD, (
        f"positive control DSR={dsr:.4f} failed to clear {DSR_PASS_THRESHOLD}"
    )


def test_deflated_sharpe_importable_from_research_utils():
    from research_utils.deflated_sharpe import deflated_sharpe as dsr_fn

    assert callable(dsr_fn)
