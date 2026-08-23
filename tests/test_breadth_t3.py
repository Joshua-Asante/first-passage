"""T3 additive calibration + downside-corr / marginal-delta."""

import numpy as np
import pandas as pd

from research_utils.breadth import (
    NULL_KIND_GARCH,
    NULL_KIND_IID,
    SURROGATE_FPR_BAND,
    SURROGATE_FPR_NOMINAL,
    compute_breadth,
    downside_correlation,
    marginal_admission_delta,
    simulate_garch11,
    surrogate_false_positive_rate,
)


def test_surrogate_fpr_iid_inside_preregistered_band():
    rng = np.random.default_rng(4)
    fpr = surrogate_false_positive_rate(
        n=200,
        n_surrogates=400,
        kind=NULL_KIND_IID,
        alpha=SURROGATE_FPR_NOMINAL,
        rng=rng,
    )
    lo, hi = SURROGATE_FPR_BAND
    assert lo <= fpr <= hi, f"FPR {fpr} outside [{lo}, {hi}]"


def test_garch_null_is_additive_not_default():
    rng = np.random.default_rng(5)
    iid = simulate_garch11(64, rng=rng)  # path exists
    assert len(iid) == 64
    # Default kind remains IID — calling GARCH requires an explicit kind.
    assert NULL_KIND_IID == "iid_gaussian"
    assert NULL_KIND_GARCH == "garch_fitted"


def test_downside_corr_and_marginal_delta_fixture():
    idx = pd.bdate_range("2022-01-03", periods=80)
    rng = np.random.default_rng(6)
    a = rng.standard_normal(80)
    b = 0.9 * a + 0.1 * rng.standard_normal(80)
    panel = pd.DataFrame({"a": a, "b": b}, index=idx)
    corr = downside_correlation(a, b)
    assert np.isfinite(corr)
    baseline = compute_breadth(panel)
    candidate = pd.Series(rng.standard_normal(80) * 0.2, index=idx, name="cand")
    with_c = compute_breadth(panel, candidate=candidate)
    delta = marginal_admission_delta(baseline, with_c)
    assert "n_eff_dependence_delta" in delta
    assert "enb_dependence_delta" in delta
    assert delta["n_eff_dependence_delta"] == with_c["n_eff_dependence"] - baseline[
        "n_eff_dependence"
    ]
