"""MSL P2 W-B — msl_score TV→N-SURV adapter acceptance tests."""
from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pytest

from discovery.prop_survivor_scoring import load_scoring_thresholds
from research_utils import msl_score as ms
from research_utils import nsurv_channel as ns

REPO = Path(__file__).resolve().parents[1]
PREREG = REPO / "docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md"
FIXTURES = REPO / "lab/research_utils/fixtures/msl_score"
W1_RESULTS_MD = (
    REPO / "lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS_INTRADAY_W1.md"
)

_TEST_SIMS = 40
_TEST_HORIZON = 400


def _thr():
    return replace(load_scoring_thresholds(PREREG), horizon=_TEST_HORIZON)


def _synthetic_frame(n: int = 80, *, seed: int = 7) -> pd.DataFrame:
    """Identical shape to tests/test_nsurv_channel._synthetic_frame."""
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2020-01-06", periods=n)
    pnl = rng.normal(20.0, 180.0, size=n)
    deep = pnl - np.abs(rng.normal(350.0, 150.0, size=n))
    low = np.minimum(0.0, deep)
    return pd.DataFrame(
        {
            "date": dates,
            "pnl_usd": pnl.astype(float),
            "intraday_low": low.astype(float),
        }
    )


def _fake_remc_factory(bust: float = 0.01, pass_rate: float = 0.80):
    def _fake_remc(
        firm_key,
        blocks,
        thresholds,
        *,
        n_sims=None,
        consistency=None,
        intraday_blocks=None,
    ):
        return {
            "firm_key": firm_key,
            "consistency": consistency,
            "n_sims": n_sims or thresholds.sims_per_seed,
            "headline_bust": bust,
            "pass_rate": pass_rate,
            "intraday_low": intraday_blocks is not None,
        }

    return _fake_remc


# ── firm geometry verify (as-is; never patch) ─────────────────────────────────


def test_verify_firm_geometry_select_100k_unreachable_lock():
    offset = ms.verify_firm_geometry("Tradeify_Select_100K")
    assert offset == pytest.approx(1_000_000.0)


# ── primary: adapter scoring path matches nsurv_channel ───────────────────────


def test_score_daily_panel_matches_channel_output(monkeypatch):
    """Primary anchor: identical daily panel → identical channel report."""
    frame = _synthetic_frame(60)
    boundary = frame["date"].iloc[30]
    monkeypatch.setattr(ns, "run_tier_remc", _fake_remc_factory(0.01, 0.80))

    via_adapter = ms.score_daily_panel(
        frame,
        half_boundary_date=boundary,
        thresholds=_thr(),
        n_sims=_TEST_SIMS,
    )
    via_channel = ns.score_nsurv(
        frame,
        half_boundary_date=boundary,
        thresholds=_thr(),
        n_sims=_TEST_SIMS,
    )
    assert via_adapter.to_dict() == via_channel.to_dict()
    assert via_adapter.nsurv == "PASS"
    assert via_adapter.nsurv_line == "N-SURV PASS"


def test_w1_headline_bust_pins_still_quoted():
    """Reuse channel pin numbers from test_nsurv_channel / RESULTS_INTRADAY_W1."""
    assert W1_RESULTS_MD.is_file()
    text = W1_RESULTS_MD.read_text(encoding="utf-8")
    assert "Tradeify_Select_100K" in text
    assert "0.72%" in text and "99.20%" in text
    pins = ns.w1_published_pins("Tradeify_Select_100K")
    assert pins["full"]["headline_bust"] == pytest.approx(0.007233333333333334)
    assert pins["full"]["pass_rate"] == pytest.approx(0.992)
    assert pins["H1"]["headline_bust"] == pytest.approx(0.0177)
    assert pins["H1"]["pass_rate"] == pytest.approx(0.9507666666666666)
    assert pins["H2"]["headline_bust"] == pytest.approx(0.0028333333333333335)
    assert pins["H2"]["pass_rate"] == pytest.approx(0.9971666666666666)


# ── hand-paired TV fixture round-trips ────────────────────────────────────────


def _assert_panel_matches(result: ms.DailyPanelResult, expected_path: Path) -> None:
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    assert result.honesty == expected["honesty"]
    assert result.lower_bound is expected["lower_bound"]
    assert result.n_trades == expected["n_trades"]
    if "excursion_columns_used" in expected:
        assert list(result.excursion_columns_used) == expected["excursion_columns_used"]
    rows = expected["rows"]
    assert len(result.frame) == len(rows)
    for i, row in enumerate(rows):
        got = result.frame.iloc[i]
        assert got["date"].date().isoformat() == row["date"]
        assert float(got["pnl_usd"]) == pytest.approx(row["pnl_usd"])
        assert float(got["intraday_low"]) == pytest.approx(row["intraday_low"])


def test_closes_only_fixture_roundtrip_panel_and_lower_bound():
    panel = ms.load_tv_daily_panel(FIXTURES / "closes_only_tv.csv")
    _assert_panel_matches(panel, FIXTURES / "expected_panel_closes_only.json")
    assert panel.honesty_label == "LOWER BOUND"
    assert panel.lower_bound is True


def test_excursion_fixture_roundtrip_no_lower_bound_label():
    panel = ms.load_tv_daily_panel(FIXTURES / "excursion_tv.csv")
    _assert_panel_matches(panel, FIXTURES / "expected_panel_excursion.json")
    assert panel.honesty_label is None
    assert panel.lower_bound is False
    assert "Adverse excursion USD" in panel.excursion_columns_used


def test_closes_only_flag_forces_lower_bound_even_with_mae_cols():
    panel = ms.load_tv_daily_panel(
        FIXTURES / "excursion_tv.csv",
        use_excursion_columns=False,
    )
    assert panel.lower_bound is True
    assert panel.honesty == "LOWER BOUND"
    # Close-only lows match the closes-only fixture on the shared P&L path.
    expected = json.loads(
        (FIXTURES / "expected_panel_closes_only.json").read_text(encoding="utf-8")
    )
    for i, row in enumerate(expected["rows"]):
        got = panel.frame.iloc[i]
        assert float(got["pnl_usd"]) == pytest.approx(row["pnl_usd"])
        assert float(got["intraday_low"]) == pytest.approx(row["intraday_low"])


# ── TNEC JSON envelope ────────────────────────────────────────────────────────


def test_score_tv_export_json_keys_and_lower_bound(monkeypatch):
    monkeypatch.setattr(ns, "run_tier_remc", _fake_remc_factory())
    # 5 exit-days → enough for week-blocks under tiny horizon override.
    payload = ms.score_tv_export(
        FIXTURES / "closes_only_tv.csv",
        half_boundary_date="2020-01-13",
        thresholds=_thr(),
        n_sims=_TEST_SIMS,
    )
    assert payload["honesty"] == "LOWER BOUND"
    assert payload["honesty_label"] == "LOWER BOUND"
    assert payload["LOWER BOUND"] is True
    assert payload["disclaimer"] == "computes, does not admit"
    assert "nsurv" in payload
    assert set(payload["nsurv"]) >= {
        "firm_key",
        "full",
        "H1",
        "H2",
        "nsurv",
        "nsurv_line",
        "eval_bust_ceiling",
        "pass_floor",
    }
    assert payload["nsurv_line"] == payload["nsurv"]["nsurv_line"]
    assert payload["tnec_nsurv"] in ("PASS", "FAIL")
    assert payload["panel"]["n_trades"] == 12
    assert payload["panel"]["n_days"] == 10


def test_score_tv_export_excursion_omits_lower_bound_key(monkeypatch):
    monkeypatch.setattr(ns, "run_tier_remc", _fake_remc_factory())
    payload = ms.score_tv_export(
        FIXTURES / "excursion_tv.csv",
        half_boundary_date="2020-01-13",
        thresholds=_thr(),
        n_sims=_TEST_SIMS,
    )
    assert payload["honesty"] == "excursion-bounded"
    assert "LOWER BOUND" not in payload
    assert "honesty_label" not in payload
    assert payload["panel"]["excursion_columns_used"]


def test_score_tv_book_composed_path(monkeypatch):
    monkeypatch.setattr(ns, "run_tier_remc", _fake_remc_factory())
    payload = ms.score_tv_book(
        {"leg_a": FIXTURES / "excursion_tv.csv"},
        half_boundary_date="2020-01-13",
        thresholds=_thr(),
        n_sims=_TEST_SIMS,
    )
    assert "book" in payload
    assert payload["book"]["composed"]["nsurv_line"].startswith("N-SURV")
    assert payload["nsurv_line"] == payload["book"]["composed"]["nsurv_line"]
    assert payload["honesty"] == "excursion-bounded"


def test_no_remc_reimplementation_in_module_source():
    src = (REPO / "lab/research_utils/msl_score.py").read_text(encoding="utf-8")
    assert "score_nsurv" in src and "score_book" in src
    assert "run_tier_remc" not in src
    assert "simulate_path" not in src
