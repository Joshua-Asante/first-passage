"""Q-R2AGRUN-1 G2 — unit tests. Must ALL PASS before the runner reads real TBBO."""
from __future__ import annotations

from research_utils.camp_import import load_camp_sibling

from datetime import date, datetime
from zoneinfo import ZoneInfo

import numpy as np
import pytest

al = load_camp_sibling("agrun_lib", __file__)

ET = ZoneInfo("America/New_York")


def test_frozen_constants():
    assert al.SEED == 20260808
    assert al.N_BOOT == 10_000
    assert al.N_PLACEBO == 1_000
    assert al.N_MIN == 2_000
    assert al.COV_MIN == 0.90
    assert al.MAG_FLOOR == 0.02
    assert al.RUN_N_MIN == 2
    assert al.HORIZON_S == 60
    assert date(2026, 2, 16) in al.EXCLUDED_SESSION_DATES


def test_mid_price():
    assert al.mid_price(100.0, 102.0) == pytest.approx(101.0)


def test_rth_session_gate():
    assert al.is_rth_session(date(2026, 2, 16)) is False  # holiday
    assert al.is_rth_session(date(2026, 2, 14)) is False  # Saturday
    assert al.is_rth_session(date(2026, 2, 9)) is True


def test_pearson_perfect():
    a = np.array([1.0, 2.0, 3.0, 4.0])
    r = np.array([2.0, 4.0, 6.0, 8.0])
    assert al.pearson_rho(a, r) == pytest.approx(1.0)


def test_void_power_precedes():
    v = al.verdict_g2(
        (-1, 1), 0.0, np.zeros(10), coverage=1.0, n_retained=1999, h1_rho=0.1, h2_rho=0.1
    )
    assert v == "VOID-POWER"
    assert al.candidate_list(v) == []


def test_void_coverage():
    v = al.verdict_g2(
        (-1, 1), 0.0, np.zeros(10), coverage=0.89, n_retained=5000, h1_rho=0.1, h2_rho=0.1
    )
    assert v == "VOID-COVERAGE"


def test_falsified_ci_and_placebo():
    placebo = np.full(100, 0.05)
    assert al.verdict_g2((-0.01, 0.01), 0.005, placebo, 1.0, 5000, 0.1, 0.1) == "FALSIFIED"
    assert al.verdict_g2((0.01, 0.04), 0.03, placebo, 1.0, 5000, 0.1, 0.1) == "FALSIFIED"


def test_ambiguous_halves_and_magnitude():
    placebo = np.full(100, 0.001)
    assert (
        al.verdict_g2((0.03, 0.05), 0.04, placebo, 1.0, 5000, 0.04, -0.03) == "AMBIGUOUS-HOLD"
    )
    assert (
        al.verdict_g2((0.005, 0.015), 0.01, placebo, 1.0, 5000, 0.01, 0.01) == "AMBIGUOUS-HOLD"
    )


def test_promote():
    placebo = np.full(100, 0.001)
    v = al.verdict_g2((0.03, 0.05), 0.04, placebo, 1.0, 5000, 0.04, 0.03)
    assert v == "PROMOTE"
    assert al.candidate_list(v) == ["C1"]


def test_suff_stats_match_corrcoef():
    rng = np.random.default_rng(0)
    a = rng.normal(size=500)
    r = 0.4 * a + rng.normal(scale=0.5, size=500)
    assert al.pearson_rho_from_suff(*al.session_suff_stats(a, r)) == pytest.approx(
        al.pearson_rho(a, r), rel=1e-12, abs=1e-12
    )


def test_bootstrap_suff_matches_concat_on_tiny():
    """Same seed + tiny sessions: suff-stat bootstrap equals concat bootstrap."""
    rng = np.random.default_rng(1)
    sessions = []
    for _ in range(5):
        a = rng.normal(size=30)
        r = 0.3 * a + rng.normal(scale=0.2, size=30)
        sessions.append((a, r))

    # Reference: old concat path (inline, one-shot)
    ref_rng = np.random.default_rng(al.SEED)
    n_s = len(sessions)
    ref = np.empty(200)
    for i in range(200):
        idx = ref_rng.integers(0, n_s, n_s)
        a = np.concatenate([sessions[j][0] for j in idx])
        r = np.concatenate([sessions[j][1] for j in idx])
        ref[i] = al.pearson_rho(a, r)
    lo_ref, hi_ref = float(np.nanpercentile(ref, 2.5)), float(np.nanpercentile(ref, 97.5))
    lo, hi = al.session_block_bootstrap_rho(sessions, n=200, seed=al.SEED)
    assert lo == pytest.approx(lo_ref, rel=0, abs=1e-12)
    assert hi == pytest.approx(hi_ref, rel=0, abs=1e-12)


def test_bootstrap_and_placebo_shapes():
    rng = np.random.default_rng(0)
    sessions = []
    for _ in range(8):
        a = rng.normal(size=40)
        r = 0.5 * a + rng.normal(scale=0.1, size=40)
        sessions.append((a, r))
    lo, hi = al.session_block_bootstrap_rho(sessions, n=200, seed=al.SEED)
    assert lo < hi
    placebo = al.within_session_r_shuffle_placebo(sessions, n=50, seed=al.SEED)
    assert placebo.shape == (50,)
    dates = [date(2026, 2, d) for d in range(9, 17)]
    h1, h2 = al.halves_rho(sessions, dates)
    assert np.isfinite(h1) and np.isfinite(h2)


def test_close_runs_side_flip_and_n_break():
    """BBB then AAA → two runs (+3, −3); singleton discarded; N breaks."""
    ts = np.array([10, 20, 30, 40, 50, 60, 70, 80], dtype=np.int64)
    side = np.array(["B", "B", "B", "A", "A", "A", "B", "N"])
    ends, feats = al.close_aggressor_runs(ts, side, n_min=2)
    assert list(ends) == [30, 60]
    assert list(feats) == [3.0, -3.0]


def test_singleton_run_dropped():
    ts = np.array([1, 2, 3], dtype=np.int64)
    side = np.array(["B", "A", "B"])
    ends, feats = al.close_aggressor_runs(ts, side, n_min=2)
    assert len(ends) == 0
    assert len(feats) == 0


def test_n_break_flushes_prior_run():
    ts = np.array([1, 2, 3, 4], dtype=np.int64)
    side = np.array(["A", "A", "N", "B"])
    ends, feats = al.close_aggressor_runs(ts, side, n_min=2)
    assert list(ends) == [2]
    assert list(feats) == [-2.0]


def test_sample_pairs_synthetic_day():
    day = date(2026, 2, 9)
    start = datetime(2026, 2, 9, 9, 30, tzinfo=ET)
    end = datetime(2026, 2, 9, 16, 1, tzinfo=ET)
    t0 = int(start.astimezone(ZoneInfo("UTC")).timestamp() * 1e9)
    t1 = int(end.astimezone(ZoneInfo("UTC")).timestamp() * 1e9)
    step = 1_000_000_000
    ts_ns = np.arange(t0, t1, step, dtype=np.int64)
    n = len(ts_ns)
    # pairs of same-side then flip → many length-2 runs
    side = np.array(["B", "B", "A", "A"] * ((n // 4) + 1))[:n]
    mid_ramp = np.linspace(0, 2.0, n)
    bid_px = 100.0 + mid_ramp
    ask_px = 100.5 + mid_ramp
    a, r, n_ret, n_elig = al.sample_pairs_for_day(ts_ns, side, bid_px, ask_px, day)
    assert n_elig > 100
    assert n_ret > 100
    assert a.shape == r.shape
    assert n_ret <= n_elig
    assert np.all(np.isfinite(a)) and np.all(np.isfinite(r))
    assert n_ret / n_elig >= 0.9
    assert set(np.unique(np.abs(a)).tolist()).issubset({2.0})
