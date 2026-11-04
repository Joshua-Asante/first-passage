"""Generator, config and lookup tests for the firm feasibility atlas (synthetic only)."""
from __future__ import annotations

import math

import numpy as np
import pytest

from firm_rules import AUTOMATION_FRIENDLY_PROP_FIRMS, FIRM_RULES
from mc import preflight
from research_utils.camp_import import load_camp_sibling

A = load_camp_sibling("atlas", __file__)


def test_grid_matches_design():
    assert len(A.shapes()) == 540
    assert A.shapes()[0] == A.Shape(0.05, 0.0, 0.35, 0.25, "tight")


@pytest.mark.parametrize("e,p", [(0.0, 0.35), (0.1, 0.5), (0.2, 0.65)])
def test_payoff_gives_expectancy(e, p):
    s = A.Shape(0.1, e, p, 1.0, "mid")
    assert math.isclose(p * s.payoff - (1 - p), e, abs_tol=1e-12)


def test_generator_moments_and_zero_days():
    pnl, low = A.generate(0.1, 0.5, 1.0, "mid", 200, 500, seed=7)
    assert pnl.shape == low.shape == (200, 500)
    assert np.all(low <= 0.0)
    assert np.all(low <= np.minimum(pnl, 0.0))  # the low is never above the close
    # zero-trade share ~ e^-1, mean daily R ~ lam * e
    assert abs((pnl == 0).mean() - math.exp(-1)) < 0.01
    assert abs(pnl.mean() - 0.1) < 0.02


def test_generator_sequences_a_known_day():
    pnl, low = A.generate(0.05, 0.5, 3.0, "deep", 1, 2000, seed=11)
    # recompute by replaying the same RNG stream
    b = (0.05 + 1 - 0.5) / 0.5
    r2 = np.random.default_rng(11)
    c = r2.poisson(3.0, size=2000)
    t = int(c.sum())
    win = r2.random(t) < 0.5
    rr = np.where(win, b, -1.0)
    ex = np.where(win, r2.uniform(0.5, 0.95, t), 1.0)
    k = 0
    for d in range(2000):
        cum, lo = 0.0, 0.0
        for _ in range(c[d]):
            lo = min(lo, cum - ex[k])
            cum += rr[k]
            k += 1
        assert pnl[0, d] == cum
        assert low[0, d] == lo


def test_generator_is_seeded():
    a = A.generate(0.1, 0.35, 0.25, "tight", 5, 50, seed=1)
    b = A.generate(0.1, 0.35, 0.25, "tight", 5, 50, seed=1)
    assert all(np.array_equal(x, y) for x, y in zip(a, b))


def test_configs_cover_every_listed_tier():
    cfgs = A.configs(FIRM_RULES, AUTOMATION_FRIENDLY_PROP_FIRMS)
    listed = {t for ts in AUTOMATION_FRIENDLY_PROP_FIRMS.values() for t in ts}
    assert {c.tier for c in cfgs} == listed
    assert len(cfgs) == len(listed) + 4
    for c in cfgs:
        kw = A.engine_kwargs(c, preflight.firm_kwargs)
        assert A.dd_allowance(kw) > 0
        if c.fixed_dollar_trail:
            assert kw["dd_type"] == "trailing_locking"
            assert kw["dd_lock_offset_usd"] == A.UNREACHABLE_LOCK


def _rows():
    rows = []
    for s in A.shapes():
        for tier, mark in (("T_HIGH", "HIGH"), ("T_EX", "EXCLUDED")):
            rows.append({"tier": tier, "config": tier, "mark": mark, "f": s.f, "e": s.e,
                         "p": s.p, "lam": s.lam, "mae": s.mae,
                         "pass": 0.5 + s.e - s.f, "bust": s.f / 4, "unresolved": 0.01,
                         "ttp_p50": 100 * s.f, "ttp_p90": 200.0, "p_pass_22": 0.1,
                         "p_pass_63": 0.3, "se_pass": 0.0, "se_bust": 0.0})
    return rows


def test_lookup_exact_and_bracketed_worst_case():
    rows = _rows()
    exact = A.lookup("T_HIGH", expectancy_r=0.1, win_rate=0.5, trades_per_session=1.0,
                     risk_frac=0.10, mae="mid", rows=rows)
    assert exact["corners_read"] == 1 and math.isclose(exact["bust"], 0.025)
    mid = A.lookup("T_HIGH", expectancy_r=0.07, win_rate=0.5, trades_per_session=1.0,
                   risk_frac=0.12, mae=0.3, rows=rows)
    assert mid["corners_read"] == 2 * 2 * 2  # e, f and mae bracketed
    assert math.isclose(mid["bust"], 0.15 / 4)          # worst = higher f
    assert math.isclose(mid["pass"], 0.5 + 0.05 - 0.15)  # worst = lower e, higher f


def test_lookup_refuses_off_grid_and_excluded():
    rows = _rows()
    with pytest.raises(A.Refused, match="outside"):
        A.lookup("T_HIGH", expectancy_r=0.5, win_rate=0.5, trades_per_session=1.0,
                 risk_frac=0.1, rows=rows)
    with pytest.raises(A.Refused, match="EXCLUDED"):
        A.lookup("T_EX", expectancy_r=0.1, win_rate=0.5, trades_per_session=1.0,
                 risk_frac=0.1, rows=rows)
    lb = A.lookup("T_EX", expectancy_r=0.1, win_rate=0.5, trades_per_session=1.0,
                  risk_frac=0.1, rows=rows, include_lower_bound=True)
    assert lb["bust_is_lower_bound"] is True


def test_smoke_run_refuses_the_atlas_directory():
    run = load_camp_sibling("run_atlas", __file__)
    with pytest.raises(SystemExit):
        run.main(["--smoke"])
    with pytest.raises(SystemExit):
        run.main(["--smoke", "--out", str(run.HERE)])


def test_report_worst_takes_min_of_both_pass_windows():
    rep = load_camp_sibling("report", __file__)
    base = {"tier": "T", "f": 0.1, "e": 0.1, "p": 0.5, "lam": 1.0, "mae": "mid", "pass": 0.6,
            "bust": 0.1, "unresolved": 0.0, "ttp_p50": 50.0, "ttp_p90": 90.0,
            "p_pass_22": 0.2, "p_pass_63": 0.4}
    w = rep.worst_by_shape([base, {**base, "p_pass_22": 0.3, "p_pass_63": 0.3}])
    r = w["T"][(0.1, 0.1, 0.5, 1.0, "mid")]
    assert (r["p_pass_22"], r["p_pass_63"]) == (0.2, 0.3)
