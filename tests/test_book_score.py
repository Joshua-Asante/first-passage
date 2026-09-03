"""Tests for lab/research_utils/book_score.py (TNEC-AU-1 step-3 tooling).

Computes composed N-SURV blocks; does not admit. Known-answer path reproduces
Q-TXG-1 striker×MNQ PANEL_SCORE.json when the committed daily panel is present.
"""
from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pytest

from discovery.prop_survivor_scoring import load_scoring_thresholds
from research_utils import book_score as bs
from research_utils import nsurv_channel as ns

REPO = Path(__file__).resolve().parents[1]
# v1 — CLOSED 2026-08-26 (its own head banner), superseded by
# 2026-08-26-prop-survivor-scoring-prereg-v2.md: the LIVE Part A eval bust
# ceiling is 5.0%, not the 3.0% pinned below. This fixture deliberately stays on
# v1 so the loader keeps regression-testing v1's frozen 3.0% text forever,
# independent of whichever file DEFAULT_PREREG points at (Trap #12 — v1's own
# numbers are never edited in place, so this pin never needs to change). The
# StaleGateWarning these calls emit is expected and is the point.
PREREG_V1 = REPO / "docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md"
TXG_CELL = (
    REPO
    / "lab/archive/transfer_expression_grid_2026-08/cells/striker_mnq"
)
TXG_DAILY = TXG_CELL / "daily_pnl_nsurv.csv"
TXG_PANEL_SCORE = TXG_CELL / "PANEL_SCORE.json"

_TEST_SIMS = 40
_TEST_HORIZON = 400


def _thr():
    return replace(load_scoring_thresholds(PREREG_V1), horizon=_TEST_HORIZON)


def _leg_frame(
    dates: pd.DatetimeIndex,
    pnl: np.ndarray,
    low: np.ndarray,
) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": dates,
            "pnl_usd": np.asarray(pnl, dtype=float),
            "intraday_low": np.asarray(low, dtype=float),
        }
    )


# ── composition: alignment, missing-day zero-fill, sign conventions ───────────


def test_compose_date_aligned_sum_and_missing_day_zero_fill():
    """Union of dates; absent leg-days fill 0 for pnl and intraday_low."""
    a = _leg_frame(
        pd.to_datetime(["2020-01-06", "2020-01-07", "2020-01-09"]),
        pnl=[100.0, 50.0, -20.0],
        low=[-10.0, -5.0, -30.0],
    )
    b = _leg_frame(
        pd.to_datetime(["2020-01-07", "2020-01-08", "2020-01-09"]),
        pnl=[10.0, 40.0, 5.0],
        low=[-2.0, -8.0, -1.0],
    )
    composed = bs.compose_book({"leg_a": a, "leg_b": b})
    assert list(composed["date"].dt.strftime("%Y-%m-%d")) == [
        "2020-01-06",
        "2020-01-07",
        "2020-01-08",
        "2020-01-09",
    ]
    assert composed["pnl_usd"].tolist() == pytest.approx([100.0, 60.0, 40.0, -15.0])
    # Missing days contribute 0 excursion; present days sum (conservative book low).
    assert composed["intraday_low"].tolist() == pytest.approx([-10.0, -7.0, -8.0, -31.0])
    assert (composed["intraday_low"] <= 0.0).all()


def test_compose_single_leg_is_identity():
    frame = _leg_frame(
        pd.bdate_range("2020-01-06", periods=5),
        pnl=[1.0, -2.0, 3.0, -4.0, 5.0],
        low=[-1.0, -2.0, -3.0, -4.0, -5.0],
    )
    composed = bs.compose_book({"only": frame})
    assert len(composed) == 5
    assert np.allclose(composed["pnl_usd"], frame["pnl_usd"])
    assert np.allclose(composed["intraday_low"], frame["intraday_low"])


def test_compose_rejects_positive_intraday_low():
    bad = _leg_frame(
        pd.bdate_range("2020-01-06", periods=3),
        pnl=[1.0, 2.0, 3.0],
        low=[-1.0, 0.5, -2.0],
    )
    with pytest.raises(ValueError, match="intraday_low"):
        bs.compose_book({"bad": bad})


# ── threshold edges (frozen prereg inequality directions) ─────────────────────


def test_threshold_edges_non_strict_bust_le_and_pass_ge():
    """**v1**'s frozen Part A: bust ≤ 3.0% ∧ P(pass) ≥ 50% — both bounds
    inclusive. 3.0% is v1's HISTORICAL ceiling; the live Part A ceiling is **5.0%**
    (prereg v2, 2026-08-26). What this test pins is the inequality *direction* and
    inclusivity, which v2 did not change — not the number itself."""
    thr = load_scoring_thresholds(PREREG_V1)
    assert thr.eval_bust_ceiling == pytest.approx(0.03)
    assert thr.pass_floor == pytest.approx(0.50)
    assert bs.clears_bust_ceiling(0.03, thr) is True
    assert bs.clears_bust_ceiling(0.0300001, thr) is False
    assert bs.clears_pass_floor(0.50, thr) is True
    assert bs.clears_pass_floor(0.499999, thr) is False
    assert ns.clears_nsurv_floor(0.03, 0.50, thr) is True


# ── score_book wires score_nsurv (no engine fork) ─────────────────────────────


def test_score_book_of_one_delegates_to_score_nsurv(monkeypatch):
    dates = pd.bdate_range("2020-01-06", periods=40)
    frame = _leg_frame(
        dates,
        pnl=np.full(40, 25.0),
        low=np.full(40, -100.0),
    )
    boundary = dates[20]
    seen: list[Any] = []

    def _fake_score(frame_in, *, half_boundary_date, **kwargs):
        seen.append({"n": len(frame_in), "boundary": half_boundary_date})
        return ns.NSurvReport(
            firm_key=ns.DEFAULT_FIRM_KEY,
            sizing_basis_usd=ns.SIZING_BASIS_USD,
            half_boundary_date=pd.Timestamp(half_boundary_date).date().isoformat(),
            thresholds_source=str(PREREG_V1),
            eval_bust_ceiling=0.03,  # v1's historical value; fixture only (live: 0.05)
            pass_floor=0.5,
            full=ns.PartitionScore(
                "full", 0.01, 0.8, True, len(frame_in), 40, 0.4, "run2", True
            ),
            h1=ns.PartitionScore("H1", 0.01, 0.8, True, 20, 40, 0.4, "run2", True),
            h2=ns.PartitionScore("H2", 0.01, 0.8, True, 20, 40, 0.4, "run2", True),
            nsurv="PASS",
        )

    monkeypatch.setattr(bs, "score_nsurv", _fake_score)
    report = bs.score_book(
        {"leg1": frame},
        half_boundary_date=boundary,
        thresholds=_thr(),
        n_sims=_TEST_SIMS,
    )
    assert len(seen) == 1
    assert seen[0]["n"] == 40
    assert report.composed.nsurv == "PASS"
    assert report.without_marginal is None
    assert "computes, does not admit" in report.format_block().lower()


def test_marginal_excludes_named_leg_and_emits_step3_lines(monkeypatch):
    dates = pd.bdate_range("2020-01-06", periods=40)
    leg_a = _leg_frame(dates, np.full(40, 10.0), np.full(40, -50.0))
    leg_b = _leg_frame(dates, np.full(40, 20.0), np.full(40, -80.0))
    composed_pnls: list[float] = []

    def _fake_score(frame_in, *, half_boundary_date, **kwargs):
        composed_pnls.append(float(frame_in["pnl_usd"].iloc[0]))
        # First call = full book (30); second = without leg_b (10).
        bust = 0.01 if frame_in["pnl_usd"].iloc[0] == 30.0 else 0.02
        pass_rate = 0.70 if frame_in["pnl_usd"].iloc[0] == 30.0 else 0.55
        return ns.NSurvReport(
            firm_key=ns.DEFAULT_FIRM_KEY,
            sizing_basis_usd=ns.SIZING_BASIS_USD,
            half_boundary_date=pd.Timestamp(half_boundary_date).date().isoformat(),
            thresholds_source=str(PREREG_V1),
            eval_bust_ceiling=0.03,  # v1's historical value; fixture only (live: 0.05)
            pass_floor=0.5,
            full=ns.PartitionScore(
                "full", bust, pass_rate, True, len(frame_in), 40, 0.4, "run2", True
            ),
            h1=ns.PartitionScore(
                "H1", bust, pass_rate, True, 20, 40, 0.4, "run2", True
            ),
            h2=ns.PartitionScore(
                "H2", bust, pass_rate, True, 20, 40, 0.4, "run2", True
            ),
            nsurv="PASS",
        )

    monkeypatch.setattr(bs, "score_nsurv", _fake_score)
    report = bs.score_book(
        {"leg_a": leg_a, "leg_b": leg_b},
        half_boundary_date=dates[20],
        marginal="leg_b",
        thresholds=_thr(),
        n_sims=_TEST_SIMS,
    )
    assert composed_pnls == pytest.approx([30.0, 10.0])
    assert report.without_marginal is not None
    assert report.marginal_leg == "leg_b"
    block = report.format_block()
    assert "computes, does not admit" in block.lower()
    assert "book-without:leg_b" in block or "without leg_b" in block.lower()
    # Step-3: composed bust vs ceiling; composed pass vs book-without.
    assert "composed bust" in block.lower()
    assert "composed p(pass)" in block.lower() or "composed pass" in block.lower()
    # Composed pass 0.70 ≥ without 0.55 → comparison clears on the pass limb.
    assert report.step3_pass_vs_without is True
    assert report.step3_bust_vs_ceiling is True


def test_marginal_requires_n_ge_2():
    dates = pd.bdate_range("2020-01-06", periods=20)
    frame = _leg_frame(dates, np.ones(20), np.full(20, -1.0))
    with pytest.raises(ValueError, match="marginal"):
        bs.score_book(
            {"only": frame},
            half_boundary_date=dates[10],
            marginal="only",
            thresholds=_thr(),
            n_sims=_TEST_SIMS,
        )


# ── known-answer: Q-TXG-1 striker×MNQ book-of-1 ───────────────────────────────


def test_q_txg1_striker_mnq_book_of_1_reproduces_panel_score():
    """Reproduce PANEL_SCORE.json N-SURV numbers as a book of one.

    Skip only when the committed daily panel or score artifact is absent.
    """
    if not TXG_DAILY.is_file() or not TXG_PANEL_SCORE.is_file():
        pytest.skip(
            "Q-TXG-1 striker_mnq daily_pnl_nsurv.csv / PANEL_SCORE.json absent; "
            "known-answer reproduction not executed."
        )

    expected = json.loads(TXG_PANEL_SCORE.read_text(encoding="utf-8"))["nsurv"]
    thr = load_scoring_thresholds(PREREG_V1)
    report = bs.score_book_from_paths(
        {"striker_mnq": TXG_DAILY},
        half_boundary_date=expected["half_boundary_date"],
        thresholds=thr,
        n_sims=None,
    )
    composed = report.composed
    assert composed.full.headline_bust == expected["full"]["headline_bust"]
    assert composed.full.pass_rate == expected["full"]["pass_rate"]
    assert composed.h1.headline_bust == expected["H1"]["headline_bust"]
    assert composed.h1.pass_rate == expected["H1"]["pass_rate"]
    assert composed.h2.headline_bust == expected["H2"]["headline_bust"]
    assert composed.h2.pass_rate == expected["H2"]["pass_rate"]
    assert composed.nsurv == expected["nsurv"]
