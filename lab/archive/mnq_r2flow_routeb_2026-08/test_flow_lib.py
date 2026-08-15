"""Q-R2FLOW-1 G2 — unit tests. Must ALL PASS before the runner reads real TBBO."""
from __future__ import annotations

from research_utils.camp_import import load_camp_sibling

from datetime import date, datetime
from zoneinfo import ZoneInfo

import numpy as np
import pytest

fl = load_camp_sibling("flow_lib", __file__)

ET = ZoneInfo("America/New_York")


def test_frozen_constants():
    assert fl.SEED == 20260808
    assert fl.N_BOOT == 10_000
    assert fl.N_PLACEBO == 1_000
    assert fl.N_MIN == 2_000
    assert fl.COV_MIN == 0.90
    assert fl.MAG_FLOOR == 0.02
    assert fl.HORIZON_S == 60
    assert date(2026, 2, 16) in fl.EXCLUDED_SESSION_DATES
    assert len(fl.rth_minute_starts_ns(date(2026, 2, 9))) == 390


def test_mid_price():
    assert fl.mid_price(100.0, 102.0) == pytest.approx(101.0)


def test_rth_session_gate():
    assert fl.is_rth_session(date(2026, 2, 16)) is False  # holiday
    assert fl.is_rth_session(date(2026, 2, 14)) is False  # Saturday
    assert fl.is_rth_session(date(2026, 2, 9)) is True


def test_pearson_perfect():
    a = np.array([1.0, 2.0, 3.0, 4.0])
    r = np.array([2.0, 4.0, 6.0, 8.0])
    assert fl.pearson_rho(a, r) == pytest.approx(1.0)


def test_void_power_precedes():
    v = fl.verdict_g2(
        (-1, 1), 0.0, np.zeros(10), coverage=1.0, n_retained=1999, h1_rho=0.1, h2_rho=0.1
    )
    assert v == "VOID-POWER"
    assert fl.candidate_list(v) == []


def test_void_coverage():
    v = fl.verdict_g2(
        (-1, 1), 0.0, np.zeros(10), coverage=0.89, n_retained=5000, h1_rho=0.1, h2_rho=0.1
    )
    assert v == "VOID-COVERAGE"


def test_falsified_ci_and_placebo():
    placebo = np.full(100, 0.05)
    assert fl.verdict_g2((-0.01, 0.01), 0.005, placebo, 1.0, 5000, 0.1, 0.1) == "FALSIFIED"
    assert fl.verdict_g2((0.01, 0.04), 0.03, placebo, 1.0, 5000, 0.1, 0.1) == "FALSIFIED"


def test_ambiguous_halves_and_magnitude():
    placebo = np.full(100, 0.001)
    assert (
        fl.verdict_g2((0.03, 0.05), 0.04, placebo, 1.0, 5000, 0.04, -0.03) == "AMBIGUOUS-HOLD"
    )
    assert (
        fl.verdict_g2((0.005, 0.015), 0.01, placebo, 1.0, 5000, 0.01, 0.01) == "AMBIGUOUS-HOLD"
    )


def test_promote():
    placebo = np.full(100, 0.001)
    v = fl.verdict_g2((0.03, 0.05), 0.04, placebo, 1.0, 5000, 0.04, 0.03)
    assert v == "PROMOTE"
    assert fl.candidate_list(v) == ["C1"]


def test_suff_stats_match_corrcoef():
    rng = np.random.default_rng(0)
    a = rng.normal(size=500)
    r = 0.4 * a + rng.normal(scale=0.5, size=500)
    assert fl.pearson_rho_from_suff(*fl.session_suff_stats(a, r)) == pytest.approx(
        fl.pearson_rho(a, r), rel=1e-12, abs=1e-12
    )


def test_bootstrap_and_placebo_shapes():
    rng = np.random.default_rng(0)
    sessions = []
    for _ in range(8):
        a = rng.normal(size=40)
        r = 0.5 * a + rng.normal(scale=0.1, size=40)
        sessions.append((a, r))
    lo, hi = fl.session_block_bootstrap_rho(sessions, n=200, seed=fl.SEED)
    assert lo < hi
    placebo = fl.within_session_r_shuffle_placebo(sessions, n=50, seed=fl.SEED)
    assert placebo.shape == (50,)
    dates = [date(2026, 2, d) for d in range(9, 17)]
    h1, h2 = fl.halves_rho(sessions, dates)
    assert np.isfinite(h1) and np.isfinite(h2)


def test_aggregate_signed_size_and_zero_print_ineligible():
    """Minute 0: +10B −3A → A=+7; minute 1: only N → ineligible; minute 2: −5A → A=−5."""
    day = date(2026, 2, 9)
    starts = fl.rth_minute_starts_ns(day)[:3]
    t0, t1, t2 = int(starts[0]), int(starts[1]), int(starts[2])
    ts = np.array(
        [t0 + 1_000_000, t0 + 2_000_000, t1 + 1_000_000, t2 + 1_000_000],
        dtype=np.int64,
    )
    size = np.array([10.0, 3.0, 99.0, 5.0])
    side = np.array(["B", "A", "N", "A"])
    out_t, out_a = fl.aggregate_clock_minute_flow(ts, size, side, starts)
    assert list(out_t) == [t0, t2]
    assert list(out_a) == [7.0, -5.0]


def test_sample_pairs_mid_from_t_end():
    """r uses mid at t_end and t_end+60s, not at minute start."""
    day = date(2026, 2, 9)
    open_ns = int(datetime(2026, 2, 9, 9, 30, tzinfo=ET).timestamp() * 1e9)
    # Quotes every second from 09:30 through 09:33 so first minute retains.
    ts_ns = np.arange(open_ns, open_ns + 4 * 60_000_000_000, 1_000_000_000, dtype=np.int64)
    n = len(ts_ns)
    size = np.ones(n, dtype=float)
    side = np.array(["B"] * n)
    # Mid ramps: at t_end=09:31 mid=101; at 09:32 mid=102 → r ≈ 1/101
    mid = 100.0 + (ts_ns - open_ns) / 60_000_000_000.0
    bid_px = mid - 0.25
    ask_px = mid + 0.25
    a, r, n_ret, n_elig = fl.sample_pairs_for_day(ts_ns, size, side, bid_px, ask_px, day)
    assert n_elig >= 1
    assert n_ret >= 1
    # First minute: all B size=1 for 60 prints → A=60
    assert a[0] == pytest.approx(60.0)
    assert r[0] == pytest.approx((102.0 - 101.0) / 101.0, rel=1e-9)


def test_sample_pairs_synthetic_day_coverage():
    day = date(2026, 2, 9)
    start = datetime(2026, 2, 9, 9, 30, tzinfo=ET)
    end = datetime(2026, 2, 9, 16, 1, tzinfo=ET)
    t0 = int(start.timestamp() * 1e9)
    t1 = int(end.timestamp() * 1e9)
    step = 1_000_000_000
    ts_ns = np.arange(t0, t1, step, dtype=np.int64)
    n = len(ts_ns)
    size = np.full(n, 2.0)
    side = np.array(["B", "A"] * ((n // 2) + 1))[:n]
    mid_ramp = np.linspace(0, 2.0, n)
    bid_px = 100.0 + mid_ramp
    ask_px = 100.5 + mid_ramp
    a, r, n_ret, n_elig = fl.sample_pairs_for_day(ts_ns, size, side, bid_px, ask_px, day)
    assert n_elig == 390
    assert n_ret == 390
    assert a.shape == r.shape
    assert np.all(np.isfinite(a)) and np.all(np.isfinite(r))
    assert n_ret / n_elig >= 0.9
