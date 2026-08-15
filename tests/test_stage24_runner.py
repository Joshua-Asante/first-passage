"""Stage-2/4 runner tests — TDD gates for Mine→Score→emit + campaign-K e2e.

Research-venv deps (stumpy/arch/skfolio) are importorskip'd so ops/CI skips cleanly.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

pytest.importorskip("arch")
pytest.importorskip("skfolio")
pytest.importorskip("stumpy")
pytest.importorskip("ruptures")

from discovery.k_count import compute_k_bracket
from discovery.matrix_emit import emit_stage4, trade_matrix_for_gate
from discovery.miner import best_hit_distance_to_shape, mine_series
from discovery.motif_rules import evaluate_rule, freeze_rule_from_spec
from discovery.scorer import DSR_UNREACHABLE_N, score_rules
from discovery.stage24_runner import (
    CAMPAIGN_SCALE_T,
    run_gate_on_survivors,
    run_synthetic_stage24,
    synthetic_e2e_report,
)
from discovery.synthetic_bars import (
    MotifSpec,
    default_motif_shape,
    generate_synthetic_bars,
)
from research_utils.prereg_paths import DISC_CAMP_0_PREREG
from research_utils.universe_gate import load_returns_matrix, load_thresholds_from_prereg

_PREREG = DISC_CAMP_0_PREREG


# ---------------------------------------------------------------- 2.1 already in test_stage24_k_count


# ---------------------------------------------------------------- 2.2 miner recovers planted motif

def test_miner_surfaces_injected_motif():
    m = 30
    shape = default_motif_shape(m, seed=2)
    motif = MotifSpec(
        shape=shape,
        horizon=3,
        direction=1,
        per_trade_sr=0.30,
        trade_vol=0.01,
        period=35,
        max_oos_trades=80,
    )
    synth = generate_synthetic_bars(
        seed=7,
        motif=motif,
        is_start="2016-01-01",
        is_end="2016-04-30",
        oos_start="2019-05-06",
        oos_end="2019-08-31",
    )
    is_ret = synth.bars["ret"].to_numpy()[synth.is_mask]
    hours = synth.bars.index.hour.to_numpy()[synth.is_mask]
    mine = mine_series(is_ret, hours=hours, windows=(30,), run_catch22=False)
    assert mine.hits, "expected motif/discord hits"
    # catch22 covariates present or explicitly unavailable — never scored columns
    assert isinstance(mine.catch22_covariates, dict)
    best, dist = best_hit_distance_to_shape(
        [h for h in mine.hits if h.m == m], shape
    )
    assert best is not None
    assert dist < 3.0, f"planted motif not recovered (dist={dist})"


# ---------------------------------------------------------------- 2.3 frozen rules — no OOS refit

def test_rule_params_frozen_from_is_only():
    shape = default_motif_shape(30, seed=3)
    rule = freeze_rule_from_spec(
        shape, direction=1, horizon=3, trigger=1.2, candidate_id="r0"
    )
    # Provenance is immutable fields on the frozen dataclass.
    assert rule.trigger == 1.2
    assert rule.direction == 1
    assert rule.horizon == 3
    rng = np.random.default_rng(0)
    series = rng.normal(0, 0.001, size=500)
    ev = evaluate_rule(rule, series)
    # Evaluating must not mutate the rule.
    assert rule.trigger == 1.2
    assert isinstance(ev.n_trades, int)


# ---------------------------------------------------------------- 2.4 low-n flag

def test_low_n_flag_set_not_dropped(tmp_path):
    shape = default_motif_shape(30, seed=4)
    rule = freeze_rule_from_spec(
        shape, direction=1, horizon=2, trigger=10.0, candidate_id="rare"
    )
    # Huge trigger → almost never fires → low n_trades on OOS.
    rng = np.random.default_rng(1)
    is_s = rng.normal(0, 0.001, 400)
    oos_s = rng.normal(0, 0.001, 400)
    bundle = score_rules([rule], is_s, oos_s, cost_frac_per_rt=0.0)
    # Cost-law may kill; force a survivor path via direct flag check on eval.
    from discovery.scorer import ScoredCandidate
    from discovery.motif_rules import RuleEval

    low = ScoredCandidate(
        rule=rule,
        is_eval=RuleEval(np.zeros(1), [0.01] * 20, [], 20),
        oos_eval=RuleEval(np.zeros(1), [0.01] * 150, [], 150),
        is_pvalue=0.1,
        cost_law_pass=True,
        dsr_unreachable_low_n=150 <= DSR_UNREACHABLE_N,
        mean_is_trade=0.01,
    )
    assert low.dsr_unreachable_low_n is True
    bracket = compute_k_bracket(1000)
    art = emit_stage4(
        [low],
        __import__("pandas").date_range("2019-01-01", periods=1, freq="h", tz="UTC"),
        bracket,
        out_dir=tmp_path,
        run_id="low_n_flag",
        zero_benchmark=True,
    )
    meta = json.loads(art.meta_json.read_text())
    assert meta["candidates"][0]["dsr_unreachable_low_n"] is True
    assert meta["v_rule"] == "1/n"


# ---------------------------------------------------------------- 2.5 matrix contract

def test_emit_matrix_loads_in_universe_gate(tmp_path):
    shape = default_motif_shape(30, seed=5)
    motif = MotifSpec(
        shape=shape,
        horizon=3,
        direction=1,
        per_trade_sr=0.30,
        trade_vol=0.01,
        period=40,
        max_oos_trades=100,
    )
    res = run_synthetic_stage24(
        seed=5,
        max_oos_trades=100,
        out_dir=tmp_path,
        run_id="emit_contract",
        include_oracle_rule=True,
        use_miner_rule=False,
        n_noise=2,
        campaign_t_for_k=CAMPAIGN_SCALE_T,
    )
    assert res.artifacts.matrix_csv.exists()
    rm = load_returns_matrix(res.artifacts.matrix_csv)
    assert "benchmark" not in rm.candidate_ids
    assert rm.benchmark is not None
    meta = json.loads(res.artifacts.meta_json.read_text())
    assert meta["k_dsr"] == res.bracket.k_dsr
    assert meta["k_spa"] == len(res.survivors)
    assert meta["k_dsr"] != meta["k_spa"]
    assert meta["v_rule"] == "1/n"
    assert meta["k_bracket"]["floor_binding"] == meta["k_dsr"]
    assert meta["k_bracket"]["raw_overlapping"] == meta["k_raw"]


# ---------------------------------------------------------------- 2.6 campaign-K e2e

def test_campaign_k_e2e_pos_low_n_neg():
    """Positive promotes; low-n expected-fails DSR; noise rejects — at K_DSR≈3200."""
    rep = synthetic_e2e_report(seed=0)
    assert 3000 <= rep["k_dsr"] <= 3400
    assert rep["positive_promote"] is True, rep
    assert rep["positive_battery"] == "PASS"
    assert rep["low_n_flag"] is True
    assert rep["low_n_promote"] is False
    assert rep["low_n_dsr_pass"] is False, "low-n must fail DSR by construction"
    assert rep["negative_promote"] is False, rep


def test_oracle_path_emit_then_gate_wires_real_modules(tmp_path):
    """Miner-skipped oracle rule → emit → load_returns_matrix → gate(var_trials=1/n)."""
    res = run_synthetic_stage24(
        seed=11,
        max_oos_trades=120,
        period=25,
        out_dir=tmp_path,
        run_id="oracle_wire",
        include_oracle_rule=True,
        use_miner_rule=False,
        n_noise=3,
        campaign_t_for_k=CAMPAIGN_SCALE_T,
    )
    assert res.survivors, "oracle should clear cost-law on planted edge"
    rm = load_returns_matrix(res.artifacts.matrix_csv)
    assert rm.returns.shape[1] == len(res.survivors)
    thr = load_thresholds_from_prereg(_PREREG)
    # Wire gate on trade matrix (DSR n = trade count); may or may not promote at
    # this short-series n — the load-bearing assert is that the call succeeds
    # with the pinned V rule and campaign-scale K_DSR.
    v = run_gate_on_survivors(res.survivors, res.bracket, thresholds=thr, seed=3)
    assert v.detail["cumulative_k"] == res.bracket.k_dsr
    assert v.detail["var_trials"] == pytest.approx(
        1.0 / max(max(s.oos_eval.n_trades for s in res.survivors), 1)
    )
    assert "dsr" in v.gate_results


def test_bind_real_k_refused():
    with pytest.raises(RuntimeError, match="operator go"):
        run_synthetic_stage24(bind_real_k=True)


def test_mine_series_stage_flags():
    """Real-campaign split: STUMPY-only on hourly (no ruptures blowup), ruptures-only
    on daily (no off-K-budget STUMPY hits). Defaults stay byte-identical legacy."""
    rng = np.random.default_rng(0)
    x = rng.normal(0, 0.001, size=400)
    stumpy_only = mine_series(x, windows=(30,), run_ruptures=False)
    assert stumpy_only.hits, "STUMPY hits expected"
    assert stumpy_only.regime_labels.max() == 0, "ruptures skipped => single label"
    ruptures_only = mine_series(x, windows=(30,), run_stumpy=False)
    assert ruptures_only.hits == [], "STUMPY skipped => no candidate hits"
    assert ruptures_only.regime_labels.shape == (400,)


def test_no_ops_import_in_discovery_runner():
    root = Path(__file__).resolve().parent.parent / "lab" / "discovery"
    for p in root.glob("*.py"):
        text = p.read_text(encoding="utf-8")
        assert "import ops" not in text
        assert "from ops" not in text
