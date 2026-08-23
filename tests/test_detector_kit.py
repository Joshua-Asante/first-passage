"""T2 cheap detector kit — synthetic pins."""

import numpy as np

from research_utils.detector_kit import (
    detector_report,
    hac_t_mean,
    lo_mackinlay_vr,
    n_eff_autocorr,
)


def test_white_noise_vr_near_one():
    rng = np.random.default_rng(0)
    x = rng.standard_normal(4000)
    vr = lo_mackinlay_vr(x, q=2)
    assert abs(vr - 1.0) < 0.12


def test_known_ar_n_eff_lt_n():
    rng = np.random.default_rng(1)
    n = 800
    e = rng.standard_normal(n)
    x = np.empty(n)
    x[0] = e[0]
    phi = 0.8
    for t in range(1, n):
        x[t] = phi * x[t - 1] + e[t]
    n_eff = n_eff_autocorr(x)
    assert n_eff < n * 0.5


def test_detector_report_has_no_lock_decision():
    rng = np.random.default_rng(2)
    report = detector_report(rng.standard_normal(200))
    assert report["lock_decision"] is None
    assert report["n"] == 200
    assert "tstat" in report["hac_t"]
    _ = hac_t_mean(rng.standard_normal(80))
