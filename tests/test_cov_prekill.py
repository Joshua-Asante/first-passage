"""Tests for lab/research_utils/cov_prekill.py (TNEC-AU-1 kill-order step 2).

Known-answer fixture source when Q-COMPOSE-1 panel inputs are absent:
``docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md`` (quoted daily-$-std
and N_eff risk-vs-correlation split). Synthetic cases cover delta sign only.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from research_utils import cov_prekill as cp


# Source: docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md
# PHASE0 smoke corroborates risk 1.9593 -> 1.9628 (~1.96 flat).
Q_COMPOSE_1_FIXTURE_SOURCE = (
    "docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md"
)
Q_COMPOSE_1_LEG_DAILY_STD = 438.0
Q_COMPOSE_1_BOOK_DAILY_STD = 273.0
Q_COMPOSE_1_STD_RATIO = 438.0 / 273.0
Q_COMPOSE_1_N_EFF_RISK_BEFORE = 1.96
Q_COMPOSE_1_N_EFF_RISK_AFTER = 1.96
# Documentary split only — tool emits PR(cov), never PR(corr):
Q_COMPOSE_1_N_EFF_CORR_BEFORE = 1.9948
Q_COMPOSE_1_N_EFF_CORR_AFTER = 2.9502


def test_q_compose_1_fixture_constants_match_closure_quotes():
    """Absent committed inputs -> encode closure figures as fixture expectations."""
    assert cp.Q_COMPOSE_1_FIXTURE_SOURCE == Q_COMPOSE_1_FIXTURE_SOURCE
    assert cp.Q_COMPOSE_1_LEG_DAILY_STD == Q_COMPOSE_1_LEG_DAILY_STD
    assert cp.Q_COMPOSE_1_BOOK_DAILY_STD == Q_COMPOSE_1_BOOK_DAILY_STD
    assert cp.Q_COMPOSE_1_STD_RATIO == pytest.approx(Q_COMPOSE_1_STD_RATIO)
    assert cp.Q_COMPOSE_1_N_EFF_RISK_BEFORE == pytest.approx(
        Q_COMPOSE_1_N_EFF_RISK_BEFORE
    )
    assert cp.Q_COMPOSE_1_N_EFF_RISK_AFTER == pytest.approx(
        Q_COMPOSE_1_N_EFF_RISK_AFTER
    )
    assert cp.Q_COMPOSE_1_N_EFF_CORR_BEFORE == pytest.approx(
        Q_COMPOSE_1_N_EFF_CORR_BEFORE
    )
    assert cp.Q_COMPOSE_1_N_EFF_CORR_AFTER == pytest.approx(
        Q_COMPOSE_1_N_EFF_CORR_AFTER
    )
    assert cp.Q_COMPOSE_1_N_EFF_RISK_AFTER == pytest.approx(
        cp.Q_COMPOSE_1_N_EFF_RISK_BEFORE
    )
    assert cp.Q_COMPOSE_1_N_EFF_CORR_AFTER > cp.Q_COMPOSE_1_N_EFF_CORR_BEFORE


def test_q_compose_1_std_ratio_formula_from_quoted_stds():
    """rho = leg daily-$-std / book daily-$-std from the closure's published stds."""
    dates = pd.bdate_range("2022-01-03", periods=260)  # Mon-start, ~52 weeks
    rng = np.random.default_rng(0)
    book = pd.Series(rng.normal(0, 1.0, size=len(dates)), index=dates, name="book")
    leg = pd.Series(rng.normal(0, 1.0, size=len(dates)), index=dates, name="leg")
    book = book * (Q_COMPOSE_1_BOOK_DAILY_STD / book.std(ddof=1))
    leg = leg * (Q_COMPOSE_1_LEG_DAILY_STD / leg.std(ddof=1))
    report = cp.cov_prekill(leg=leg, book=book)
    assert report.leg_daily_std == pytest.approx(Q_COMPOSE_1_LEG_DAILY_STD, rel=1e-9)
    assert report.book_daily_std == pytest.approx(Q_COMPOSE_1_BOOK_DAILY_STD, rel=1e-9)
    assert report.std_ratio == pytest.approx(Q_COMPOSE_1_STD_RATIO, rel=1e-9)


def test_participation_ratio_matches_stage8_adr_formula():
    """PR(M) = (sum eigvals)^2 / sum(eigvals^2) — Stage-8 ADR / breadth.py."""
    matrix = np.diag([2.0, 1.0, 1.0, 0.0])
    assert cp.participation_ratio(matrix) == pytest.approx(16.0 / 6.0, abs=1e-9)


def _panel(n_weeks: int, n_cols: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2022-01-03", periods=n_weeks * 5)
    data = rng.normal(0, 1.0, size=(len(dates), n_cols))
    cols = [f"leg{i}" for i in range(n_cols)]
    return pd.DataFrame(data, index=dates, columns=cols)


def test_zero_covariance_insertion_delta_positive_pass_to_mc():
    """Independent equal-scale leg lifts risk N_eff -> PASS-TO-MC."""
    book = _panel(n_weeks=80, n_cols=1, seed=11)["leg0"].rename("book")
    leg = _panel(n_weeks=80, n_cols=1, seed=99)["leg0"].rename("orb")
    report = cp.cov_prekill(leg=leg, book=book)
    assert report.n_eff_risk_delta > 0
    assert report.verdict == "PASS-TO-MC"
    assert report.verdict_line == (
        "PASS-TO-MC — necessary-never-sufficient — composed MC still binds (M-21)"
    )


def test_high_covariance_high_variance_delta_nonpositive_prekill():
    """Variance-dominant perfect clone of the book -> PRE-KILL (delta <= 0)."""
    book = _panel(n_weeks=80, n_cols=1, seed=7)["leg0"].rename("book")
    leg = (book * 2.0).rename("dominant")
    report = cp.cov_prekill(leg=leg, book=book)
    assert report.n_eff_risk_delta <= 0
    assert report.std_ratio > 1.0
    assert report.verdict == "PRE-KILL"
    assert report.verdict_line == (
        "PRE-KILL — necessary-never-sufficient — composed MC still binds (M-21)"
    )


def test_book_dataframe_uses_summed_composite_for_daily_std():
    """Multi-column book: daily-$-std is std of the caller's summed composite."""
    panel = _panel(n_weeks=40, n_cols=2, seed=3)
    leg = _panel(n_weeks=40, n_cols=1, seed=4)["leg0"].rename("cand")
    report = cp.cov_prekill(leg=leg, book=panel)
    expected_book_std = float(panel.sum(axis=1).std(ddof=1))
    assert report.book_daily_std == pytest.approx(expected_book_std, rel=1e-12)
    assert report.sizing_basis_usd == 100_000.0
