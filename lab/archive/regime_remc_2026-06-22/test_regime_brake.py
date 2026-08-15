"""Self-tests for the exogenous regime brake (Q-REGIME-ADAPT-1.T2b, 2026-06-22).

Run:  python -m pytest test_regime_brake.py -q

Pure-synthetic — no vendor data, no VIX, no decompound import needed. Tests the
NEW glue only (the locked MC machinery is REG-tested in decompound): lag-honest
factor derivation, threshold semantics, panel alignment (ffill + calm default),
and the multiplicative brake.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import regime_brake as R  # noqa: E402


def _sig(dates, vals):
    return pd.Series(vals, index=pd.to_datetime(dates), dtype=float)


def test_regime_factor_lag_honest_uses_prior_day():
    s = _sig(["2021-01-04", "2021-01-05", "2021-01-06", "2021-01-07"], [10, 30, 30, 10])
    f = R.regime_factor_series(s, threshold=20, k_derisk=0.5, lag_days=1)
    # day t uses signal[t-1]: nan→calm, 10→calm, 30→stressed, 30→stressed
    assert list(f.values) == [1.0, 1.0, 0.5, 0.5]


def test_regime_factor_threshold_strict_gt():
    s = _sig(["2021-01-04", "2021-01-05", "2021-01-06"], [20, 21, 19])
    f = R.regime_factor_series(s, threshold=20, k_derisk=0.5, lag_days=0)
    assert list(f.values) == [1.0, 0.5, 1.0]  # 20 NOT >20 (strict)


def test_align_factor_ffills_and_defaults_calm_before_first():
    f = _sig(["2021-01-05", "2021-01-07"], [0.5, 1.0])
    panel_idx = pd.to_datetime(["2021-01-04", "2021-01-05", "2021-01-06", "2021-01-07", "2021-01-08"])
    a = R.align_factor_to_panel(f, panel_idx)
    # d04 before first→calm 1.0; d05→0.5; d06 ffill 0.5; d07→1.0; d08 ffill 1.0
    assert list(a.values) == [1.0, 0.5, 0.5, 1.0, 1.0]


def test_apply_regime_brake_scales_each_row_by_its_factor():
    idx = pd.to_datetime(["2021-01-04", "2021-01-05"])
    panel = pd.DataFrame({"g": [100.0, 200.0], "a": [10.0, 20.0]}, index=idx)
    out = R.apply_regime_brake(panel, pd.Series([0.5, 1.0], index=idx))
    assert out.loc[idx[0], "g"] == 50.0 and out.loc[idx[0], "a"] == 5.0
    assert out.loc[idx[1], "g"] == 200.0 and out.loc[idx[1], "a"] == 20.0


def test_calm_factor_is_identity():
    idx = pd.to_datetime(["2021-01-04", "2021-01-05"])
    panel = pd.DataFrame({"g": [100.0, 200.0]}, index=idx)
    out = R.apply_regime_brake(panel, pd.Series([1.0, 1.0], index=idx))
    pd.testing.assert_frame_equal(out, panel)


def test_factor_only_two_values_and_never_boosts():
    s = _sig(pd.bdate_range("2021-01-01", periods=10),
             [10, 30, 15, 40, 5, 25, 18, 22, 12, 35])
    f = R.regime_factor_series(s, threshold=20, k_derisk=0.4, lag_days=1)
    assert set(np.unique(f.values)).issubset({0.4, 1.0})
    assert f.max() <= 1.0  # a brake never increases size
