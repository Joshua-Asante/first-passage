"""Unit tests for CON-1 Stage-0 harness — synthetic fixtures only; no real path PnL."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from research_utils.camp_import import load_camp_sibling

C = load_camp_sibling("construct_lib", __file__)


def test_frozen_constants():
    assert C.GATE_G == 10.0
    assert C.RT_PT == 1.41
    assert C.LOOKBACK_MIN == 5
    assert C.THETA_SESSIONS == 20
    assert C.K_INTRINSIC == 1
    assert C.DSR_FLOOR == 0.650
    assert C.RANDOM_SEED == 20260808
    assert C.PLACEBO_REPS == 1000


def test_arithmetic_bars():
    b = C.arithmetic_bars()
    assert b["em1_pred_pt"] == pytest.approx(5.41)
    assert b["nedge_pred_pt"] == pytest.approx(1.41)
    assert b["em1_wr_bar"] == pytest.approx(0.7705)
    assert b["nedge_wr_bar"] == pytest.approx(0.5705)


def test_cheap_falsifier_ok_without_prior_art():
    r = C.cheap_falsifier(prior_art_effect_pt=None, entry_named=True, sign_relative_contrarian=True)
    assert r.verdict == "CHEAP_FALSIFIER_OK"
    assert r.falsified_by_arithmetic is False


def test_cheap_falsifier_arithmetic_trip():
    # Prior-art effect tiny vs EM1 bar/2 (= 2.705)
    r = C.cheap_falsifier(prior_art_effect_pt=1.0, entry_named=True, sign_relative_contrarian=True)
    assert r.verdict == "FALSIFIED-BY-ARITHMETIC"
    assert r.arithmetic_bar_hit == "EM1"


def test_cheap_falsifier_rejects_inverted_sign():
    r = C.cheap_falsifier(sign_relative_contrarian=False)
    assert r.verdict == "FALSIFIED"
    assert "C5" in r.detail or "momentum" in r.detail.lower()


def test_tnec_verdict_template_all_U():
    s = C.g0_freeze_verdict_template()
    assert s == "U U U U U | U | U | U"


def test_tnec_verdict_partial_limbs():
    s = C.format_tnec_verdict({"N-SHAPE": "P", "N-EDGE": "U"}, bust="U", p_pass="U", mu_disclosed="12.3")
    assert s == "U U U P U | U | U | 12.3"


def test_r_math():
    assert C.r_from_pts(10.0) == pytest.approx(0.859)
    assert C.r_from_pts(-10.0) == pytest.approx(-1.141)


def test_path_stop_before_flat():
    o = 100.0
    h = np.array([101.0, 102.0])
    l = np.array([89.0, 90.0])  # stop on bar 0 for long G=10
    c = np.array([100.0, 105.0])
    pts, kind = C.path_pts_session_flat(o, +1, h, l, c, 0, stop_pt=10.0)
    assert kind == "stop"
    assert pts == pytest.approx(-10.0)


def test_path_session_flat_no_stop():
    o = 100.0
    h = np.array([101.0, 102.0, 103.0])
    l = np.array([99.0, 98.0, 97.0])
    c = np.array([100.5, 101.0, 104.0])
    pts, kind = C.path_pts_session_flat(o, +1, h, l, c, 0, stop_pt=10.0)
    assert kind == "flat"
    assert pts == pytest.approx(4.0)


def test_log_return_lookback_and_divergence_sign():
    # ES rose more than NQ over last 5 completed closes → d > 0 → LONG (contrarian: NQ lagged)
    es = np.array([100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 101.0, 102.0], dtype=float)
    nq = np.array([100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.2, 100.4], dtype=float)
    # at t=7: close[6]/close[1] = 101/100 vs 100.2/100
    d = C.divergence_series(es, nq)
    assert np.isnan(d[5])
    assert d[7] > 0.0
    assert C.entry_side_at(d[7], theta_t=1e-6) == +1
    # negative divergence → SHORT
    assert C.entry_side_at(-0.01, theta_t=1e-6) == -1
    # below threshold → flat
    assert C.entry_side_at(0.001, theta_t=0.01) == 0


def test_em3_one_position_ignores_further_signals():
    n = 20
    o = np.full(n, 100.0)
    h = np.full(n, 101.0)
    l = np.full(n, 99.0)
    c = np.linspace(100.0, 105.0, n)
    # Force long signal every bar
    d = np.full(n, 1.0)
    trades = C.simulate_session_trades(o, h, l, c, d, theta=0.1, stop_pt=10.0)
    assert len(trades) == 1
    assert trades[0]["side"] == +1
    assert trades[0]["kind"] == "flat"


def test_session_theta_needs_20_prior():
    abs_d = [np.array([0.01, 0.02])] * 19
    assert np.isnan(C.session_theta(abs_d, 19, window=20))
    abs_d = [np.array([0.01, 0.03])] * 20 + [np.array([0.5])]
    th = C.session_theta(abs_d, 20, window=20)
    assert th == pytest.approx(0.02)


def test_explore_go_absent_by_default(tmp_path):
    assert C.explore_go_present(tmp_path) is False
    (tmp_path / "EXPLORE_GO.md").write_text("GO\n", encoding="utf-8")
    assert C.explore_go_present(tmp_path) is True


def test_divergence_series_vec_matches_loop():
    rng = np.random.default_rng(0)
    es = 100 + np.cumsum(rng.normal(0, 0.1, 40))
    nq = 100 + np.cumsum(rng.normal(0, 0.1, 40))
    a = C.divergence_series(es, nq)
    b = C.divergence_series_vec(es, nq)
    mask = np.isfinite(a) | np.isfinite(b)
    np.testing.assert_allclose(a[mask], b[mask], rtol=0, atol=1e-12)


def test_session_block_bootstrap_mean_deterministic():
    sessions = [np.array([0.1, 0.2]), np.array([-0.05]), np.array([0.3, 0.0, 0.1])]
    a = C.session_block_bootstrap_mean(sessions, n=200, seed=20260808)
    b = C.session_block_bootstrap_mean(sessions, n=200, seed=20260808)
    assert a == b
    assert a[0] <= a[1]


def test_halves_mean_sign_agree_and_disagree():
    trades_ok = [
        {"session": __import__("datetime").date(2020, 1, 1), "R": 0.2},
        {"session": __import__("datetime").date(2020, 1, 2), "R": 0.1},
        {"session": __import__("datetime").date(2024, 1, 1), "R": 0.3},
        {"session": __import__("datetime").date(2024, 1, 2), "R": 0.05},
    ]
    _, _, agree = C.halves_mean_sign(trades_ok)
    assert agree is True
    trades_bad = [
        {"session": __import__("datetime").date(2020, 1, 1), "R": 0.2},
        {"session": __import__("datetime").date(2020, 1, 2), "R": 0.1},
        {"session": __import__("datetime").date(2024, 1, 1), "R": -0.3},
        {"session": __import__("datetime").date(2024, 1, 2), "R": -0.05},
    ]
    _, _, agree2 = C.halves_mean_sign(trades_bad)
    assert agree2 is False


def test_verdict_arm_void_on_thin_n():
    v = C.verdict_arm(
        n=5,
        mean_r=0.5,
        ci=(0.1, 0.9),
        placebo_means=np.array([-0.1, 0.0]),
        halves_agree=True,
        ann_sr=1.0,
        dsr=0.99,
    )
    assert v == "VOID"


def test_verdict_arm_falsified_ci_straddles_zero():
    v = C.verdict_arm(
        n=100,
        mean_r=0.05,
        ci=(-0.01, 0.12),
        placebo_means=np.full(100, -0.1),
        halves_agree=True,
        ann_sr=1.0,
        dsr=0.99,
    )
    assert v == "FALSIFIED"


def test_overall_explore_verdict():
    assert C.overall_explore_verdict("SHAPE-CLEAR", "FALSIFIED") == "SHAPE-CLEAR"
    assert C.overall_explore_verdict("FALSIFIED", "FALSIFIED") == "FALSIFIED"
    assert C.overall_explore_verdict("VOID", "FALSIFIED") == "VOID"


def test_within_session_placebo_changes_when_pool_varies():
    # Two clocks with different path R; one entry at index 0 in the pool.
    pack = {
        "entry_clocks": np.array([0]),
        "path_r_all_clocks": np.array([1.0, -1.0, 0.5]),
    }
    means = C.within_session_r_shuffle_placebo_means([pack], n=50, seed=1)
    assert len(means) == 50
    assert np.isfinite(means).all()
    # With a varied pool, shuffled means are not all identical to 1.0
    assert np.unique(np.round(means, 6)).size >= 2
