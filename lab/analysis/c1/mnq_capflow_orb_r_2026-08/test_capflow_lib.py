"""Q-CAPFLOW-1 — unit tests. Must ALL PASS before the runner reads TBBO."""
from __future__ import annotations

from research_utils.camp_import import load_camp_sibling

from datetime import date, datetime
from zoneinfo import ZoneInfo

import numpy as np
import pytest

cl = load_camp_sibling("capflow_lib", __file__)

ET = ZoneInfo("America/New_York")


def test_frozen_constants():
    assert cl.SEED == 20260808
    assert cl.N_BOOT == 10_000
    assert cl.N_PLACEBO == 1_000
    assert cl.N_MIN == 30
    assert cl.COV_MIN == 0.90
    assert cl.MAG_FLOOR == 0.02
    assert cl.OR_OPEN.hour == 9 and cl.OR_OPEN.minute == 30


def test_or_start_ns_is_0930_et():
    ns = cl.or_start_ns(date(2026, 2, 9))
    expect = int(datetime(2026, 2, 9, 9, 30, tzinfo=ET).timestamp() * 1e9)
    assert ns == expect


def test_signed_aggressor_sum_ba_window():
    day = date(2026, 2, 9)
    t0 = cl.or_start_ns(day)
    t1 = t0 + 60_000_000_000
    ts = np.array([t0 + 1, t0 + 2, t1, t1 + 1], dtype=np.int64)
    size = np.array([10.0, 3.0, 99.0, 5.0])
    side = np.array(["B", "A", "B", "A"])
    # [t0, t1): +10 −3 = 7; print at t1 excluded
    assert cl.signed_aggressor_sum(ts, size, side, t0, t1) == pytest.approx(7.0)


def test_signed_aggressor_empty_is_none_not_zero():
    day = date(2026, 2, 9)
    t0 = cl.or_start_ns(day)
    t1 = t0 + 60_000_000_000
    ts = np.array([t0 + 1], dtype=np.int64)
    size = np.array([10.0])
    side = np.array(["N"])
    assert cl.signed_aggressor_sum(ts, size, side, t0, t1) is None


def test_pearson_perfect():
    a = np.array([1.0, 2.0, 3.0, 4.0])
    r = np.array([2.0, 4.0, 6.0, 8.0])
    assert cl.pearson_rho(a, r) == pytest.approx(1.0)


def test_mean_split_disclosure_twin():
    a = np.array([1.0, 2.0, 10.0, 20.0])
    r = np.array([0.0, 1.0, 2.0, 3.0])
    # median R = 1.5 → hi={10,20} lo={1,2} → Δ = 15 − 1.5 = 13.5
    assert cl.mean_split_delta(a, r) == pytest.approx(13.5)


def test_void_power_precedes_coverage():
    v = cl.verdict_capflow((-1, 1), 0.0, np.array([0.0]), coverage=1.0,
                           n_covered=29, h1_rho=0.1, h2_rho=0.1)
    assert v == "VOID-POWER"


def test_void_coverage():
    v = cl.verdict_capflow((-1, 1), 0.0, np.array([0.0]), coverage=0.89,
                           n_covered=100, h1_rho=0.1, h2_rho=0.1)
    assert v == "VOID-COVERAGE"


def test_falsified_ci_includes_zero():
    placebo = np.zeros(100)
    v = cl.verdict_capflow((-0.01, 0.01), 0.005, placebo, coverage=1.0,
                           n_covered=100, h1_rho=0.1, h2_rho=0.1)
    assert v == "FALSIFIED"


def test_falsified_below_placebo():
    placebo = np.full(100, 0.05)
    v = cl.verdict_capflow((0.01, 0.04), 0.03, placebo, coverage=1.0,
                           n_covered=100, h1_rho=0.1, h2_rho=0.1)
    assert v == "FALSIFIED"


def test_ambiguous_hold_magnitude():
    placebo = np.full(100, 0.001)
    obs = 0.015  # |obs| > p95, |obs| < 0.02
    v = cl.verdict_capflow((0.01, 0.02), obs, placebo, coverage=1.0,
                           n_covered=100, h1_rho=0.015, h2_rho=0.014)
    assert v == "AMBIGUOUS-HOLD"
    assert not cl.cap_spent(v)


def test_ambiguous_hold_halves_disagree():
    placebo = np.full(100, 0.001)
    obs = 0.05
    v = cl.verdict_capflow((0.03, 0.07), obs, placebo, coverage=1.0,
                           n_covered=100, h1_rho=0.05, h2_rho=-0.02)
    assert v == "AMBIGUOUS-HOLD"


def test_resolved_accept():
    placebo = np.full(100, 0.001)
    obs = 0.05
    v = cl.verdict_capflow((0.03, 0.07), obs, placebo, coverage=1.0,
                           n_covered=100, h1_rho=0.05, h2_rho=0.04)
    assert v == "RESOLVED"
    assert cl.cap_spent(v)


def test_assemble_sessions_drops_uncovered():
    pairs = [
        (1.0, 0.5, date(2026, 2, 9)),
        (None, 0.5, date(2026, 2, 9)),
        (2.0, 1.0, date(2026, 2, 10)),
    ]
    sessions, dates, dropped = cl.assemble_trigger_sessions(pairs)
    assert dropped == 1
    assert dates == [date(2026, 2, 9), date(2026, 2, 10)]
    assert sessions[0][0].tolist() == [1.0]
    assert sessions[1][0].tolist() == [2.0]


def test_bootstrap_deterministic():
    rng = np.random.default_rng(0)
    sessions = []
    for _ in range(6):
        a = rng.normal(size=8)
        r = 0.4 * a + rng.normal(scale=0.2, size=8)
        sessions.append((a, r))
    a = cl.session_block_bootstrap_rho(sessions, n=200, seed=cl.SEED)
    b = cl.session_block_bootstrap_rho(sessions, n=200, seed=cl.SEED)
    assert a == b
