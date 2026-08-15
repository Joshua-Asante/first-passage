"""Prop survivor-scoring harness — G0–G8 + F1/F2 load-bearing regressions."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from discovery.prop_survivor_scoring import (
    DEFAULT_PREREG,
    ScoringThresholds,
    TierScore,
    blocks_from_daily_pnl,
    cost_law_kill,
    discharges_falsifier,
    load_scoring_thresholds,
    naive_daily_static_bust,
    reduce_to_deployable,
    score_candidate,
    score_part_a,
)
from firm_rules import FIRM_RULES
from mc.preflight import summarize_outcomes

REPO = Path(__file__).resolve().parents[1]
PREREG = REPO / "docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md"

# Tiny sim count for wall-clock; production default stays at pre-reg 10k.
_TEST_SIMS = 40


def _thr() -> ScoringThresholds:
    return load_scoring_thresholds(PREREG)


# ── Step 2.1 — pre-reg loader ────────────────────────────────────────────────


def test_loader_parses_live_prereg():
    t = _thr()
    assert t.eval_bust_ceiling == pytest.approx(0.03)
    assert t.funded_bust_ceiling == pytest.approx(0.01)
    assert t.pass_floor == pytest.approx(0.50)
    assert t.tier_keys == (
        "Bulenox_100K",
        "Tradeify_Select_100K",
        "MFFU_Rapid_100K",
        "BluSky_Premium_100K",
    )
    assert t.seeds == (42, 123, 2026)
    assert t.sims_per_seed == 10_000
    assert t.horizon == 1500
    assert t.cost_law_multiple == pytest.approx(4.0)
    assert t.trailing_locking_tiers == frozenset(
        {"Tradeify_Select_100K", "MFFU_Rapid_100K"}
    )
    assert Path(t.source_path) == PREREG
    assert DEFAULT_PREREG.name == PREREG.name


def test_loader_refuses_missing_ceiling(tmp_path: Path):
    bad = tmp_path / "bad.md"
    bad.write_text("# no numbers here\n", encoding="utf-8")
    with pytest.raises(ValueError, match="refusing to guess"):
        load_scoring_thresholds(bad)


def test_no_ceiling_literals_outside_loader_and_tests():
    """§10 audit: gate logic must not hardcode 3.0 / 1.0 / 50 / 10000."""
    src = (REPO / "lab/discovery/prop_survivor_scoring.py").read_text(encoding="utf-8")
    # Strip the loader function body (it may mention the patterns in comments/regex).
    # Assert production gate helpers after load_scoring_thresholds do not embed ceilings.
    after = src.split("def reduce_to_deployable", 1)[1]
    for forbidden in ("0.03", "0.01", "0.50", "0.5)", "10000", "10_000", "3.0%", "50%"):
        assert forbidden not in after, f"forbidden literal {forbidden!r} outside loader"


# ── Step 2.2 — G1 / G2 ───────────────────────────────────────────────────────


def test_g1_yes_records_r_deploy_and_ratio():
    g1 = reduce_to_deployable(
        [10.0, 20.0, -5.0],
        np.array([1.0, 2.0, 0.0]),
        envelope_verdict="YES",
    )
    assert g1.r_deploy == 3
    assert g1.halted is False
    assert g1.deployable_default_envelope == "YES"
    assert g1.expectancy_ratio == pytest.approx(np.mean([1.0, 2.0, 0.0]) / np.mean([10.0, 20.0, -5.0]))


def test_g1_no_halts_before_g2(monkeypatch):
    called = {"g2": False}

    def _boom(*_a, **_k):
        called["g2"] = True
        raise AssertionError("G2 must not run after G1 NO")

    monkeypatch.setattr(
        "discovery.prop_survivor_scoring.cost_law_kill", _boom
    )
    report = score_candidate(
        strategy_label="halt-fixture",
        candidate_daily_pnl=np.ones(60) * 50.0,
        full_res_trades=[1.0, 2.0],
        envelope_verdict="NO",
        thresholds=_thr(),
        n_sims=_TEST_SIMS,
    )
    assert report.halted_at == "G1"
    assert report.discharges_falsifier is False
    assert report.tiers == {}
    assert called["g2"] is False


def test_g2_kills_sub_hurdle_and_passes_clear_edge():
    t = _thr()
    # Tradeify $0.91/side → RT $1.82; 4× × 10 RTs = $72.80
    kill = cost_law_kill(
        "Tradeify_Select_100K",
        r_deploy=10,
        gross_edge_usd=10.0,
        thresholds=t,
    )
    assert kill.passed is False
    assert kill.hurdle_usd == pytest.approx(4.0 * 1.82 * 10)

    clear = cost_law_kill(
        "Tradeify_Select_100K",
        r_deploy=10,
        gross_edge_usd=1_000.0,
        thresholds=t,
    )
    assert clear.passed is True


# ── Step 2.3 — G3 ────────────────────────────────────────────────────────────


def test_g3_all_four_frozen_tiers_engine_ready():
    from mc.preflight import assert_engine_ready

    for key in _thr().tier_keys:
        kw = assert_engine_ready(key)
        assert "starting_equity" in kw
        assert FIRM_RULES[key]["daily_loss_pct"] is None
        assert kw["daily_loss_pct"] is None


# ── Blocks + F1 regression ───────────────────────────────────────────────────


def test_blocks_from_daily_pnl_shape():
    pnl = np.arange(20, dtype=float)
    blocks = blocks_from_daily_pnl(pnl)
    assert blocks.ndim == 3
    assert blocks.shape[1:] == (5, 1)
    assert blocks.shape[0] >= 1


def test_f1_headline_includes_trailing_naive_omits():
    """Load-bearing: trailing-only busts must surface via summarize_outcomes."""
    seeds = [
        {
            "outcomes": {
                "pass": 0,
                "bust_daily": 0,
                "bust_static": 0,
                "bust_trailing": 40,
                "bust_inactivity": 0,
                "horizon_cap": 0,
            }
        }
        for _ in range(3)
    ]
    summary = summarize_outcomes(seeds, 40)
    assert summary["headline_bust"] == pytest.approx(1.0)
    assert naive_daily_static_bust(summary["rates"]) == pytest.approx(0.0)
    # Bust-side trap: naive daily+static reads 0% (clears 3% ceiling); faithful does not.
    assert naive_daily_static_bust(summary["rates"]) <= _thr().eval_bust_ceiling
    assert summary["headline_bust"] > _thr().eval_bust_ceiling
    faithful_ok = score_part_a(
        {"headline_bust": summary["headline_bust"], "pass_rate": summary["pass_rate"]},
        _thr(),
    )
    assert faithful_ok is False


# ── Step 2.6 — discharge rule (F2 geometry requirement) ──────────────────────


def _tier(firm_key: str, clears: bool) -> TierScore:
    return TierScore(
        firm_key=firm_key,
        dd_type=str(FIRM_RULES[firm_key]["dd_type"]),
        f2_label="optimistic-lower-bound"
        if FIRM_RULES[firm_key]["dd_type"] == "trailing"
        else None,
        g3_ok=True,
        run1={},
        run2={},
        clears_part_a=clears,
        clears_funded=False,
        gated_on="run2",
    )


def test_discharge_requires_trailing_locking():
    t = _thr()
    # Bulenox + BluSky only — both trailing — MUST NOT discharge.
    only_trailing = {
        "Bulenox_100K": _tier("Bulenox_100K", True),
        "BluSky_Premium_100K": _tier("BluSky_Premium_100K", True),
        "Tradeify_Select_100K": _tier("Tradeify_Select_100K", False),
        "MFFU_Rapid_100K": _tier("MFFU_Rapid_100K", False),
    }
    assert discharges_falsifier(only_trailing, t) is False

    # Tradeify + Bulenox — includes trailing_locking — discharges.
    with_locking = {
        "Bulenox_100K": _tier("Bulenox_100K", True),
        "BluSky_Premium_100K": _tier("BluSky_Premium_100K", False),
        "Tradeify_Select_100K": _tier("Tradeify_Select_100K", True),
        "MFFU_Rapid_100K": _tier("MFFU_Rapid_100K", False),
    }
    assert discharges_falsifier(with_locking, t) is True


def test_discharge_needs_two_firms():
    t = _thr()
    one = {
        "Tradeify_Select_100K": _tier("Tradeify_Select_100K", True),
        "MFFU_Rapid_100K": _tier("MFFU_Rapid_100K", False),
        "Bulenox_100K": _tier("Bulenox_100K", False),
        "BluSky_Premium_100K": _tier("BluSky_Premium_100K", False),
    }
    assert discharges_falsifier(one, t) is False


# ── End-to-end synthetic paths ───────────────────────────────────────────────


def _steady_edge_daily(n: int = 260, daily: float = 80.0) -> np.ndarray:
    """Gentle positive EOD P&L — tends to clear trailing_locking evals at $100K."""
    return np.full(n, daily, dtype=float)


def _catastrophic_daily(n: int = 260) -> np.ndarray:
    """Large red days — should fail Part A on every tier."""
    rng = np.random.default_rng(0)
    return rng.normal(-500.0, 50.0, size=n)


def test_e2e_edge_candidate_runs_four_tiers_and_routes_standalone():
    t = _thr()
    trades = [80.0] * 120  # R_deploy large; gross edge clears G2
    report = score_candidate(
        strategy_label="synthetic-edge",
        candidate_daily_pnl=_steady_edge_daily(),
        full_res_trades=trades,
        envelope_verdict="YES",
        thresholds=t,
        n_sims=_TEST_SIMS,
        gross_edge_usd=50_000.0,
    )
    assert report.halted_at is None
    assert report.routing == "STANDALONE"
    assert set(report.tiers) == set(t.tier_keys)
    assert "TODO" in report.regime_robustness_gate
    # Every tier should have gotten past G3
    assert all(s.g3_ok for s in report.tiers.values())
    # F2 labels on trailing firms
    assert report.tiers["Bulenox_100K"].f2_label == "optimistic-lower-bound"
    assert report.tiers["BluSky_Premium_100K"].f2_label == "optimistic-lower-bound"
    assert report.tiers["Tradeify_Select_100K"].f2_label is None
    # Consistency gating: Bulenox has no rule → degenerate; Tradeify gates on run2
    assert report.tiers["Bulenox_100K"].gated_on == "run1_degenerate"
    assert report.tiers["Tradeify_Select_100K"].gated_on == "run2"
    # Serialization
    d = report.to_dict()
    assert "discharges_falsifier" in d
    assert d["g1"]["r_deploy"] == 120


def test_e2e_fail_candidate_does_not_discharge():
    t = _thr()
    report = score_candidate(
        strategy_label="synthetic-fail",
        candidate_daily_pnl=_catastrophic_daily(),
        full_res_trades=[-500.0] * 50,
        envelope_verdict="YES",
        thresholds=t,
        n_sims=_TEST_SIMS,
        gross_edge_usd=50_000.0,  # clear G2 so we exercise remc failure path
    )
    assert report.discharges_falsifier is False
    assert all(not s.clears_part_a for s in report.tiers.values())


def test_e2e_f1_exposed_on_trailing_tier_rates():
    """A trailing-heavy fail path must show bust_trailing in reported rates."""
    t = _thr()
    report = score_candidate(
        strategy_label="trailing-bust-probe",
        candidate_daily_pnl=_catastrophic_daily(),
        full_res_trades=[-500.0] * 50,
        envelope_verdict="YES",
        thresholds=t,
        n_sims=_TEST_SIMS,
        gross_edge_usd=50_000.0,
        tiers=("Bulenox_100K",),
    )
    rates = report.tiers["Bulenox_100K"].run2["rates"]
    headline = report.tiers["Bulenox_100K"].run2["headline_bust"]
    naive = naive_daily_static_bust(rates)
    # On a pure trailing geometry, most busts land in bust_trailing.
    assert rates["bust_trailing"] > 0.0
    assert headline > naive
    assert headline == pytest.approx(
        rates["bust_daily"] + rates["bust_static"] + rates["bust_trailing"]
    )


def test_production_default_sims_is_prereg_10k():
    t = _thr()
    assert t.sims_per_seed == 10_000
