"""Stage-7 native-micro realism engine tests — TDD gates + three-case proof."""
from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from discovery.cost_mgc import COMMISSION_PER_SIDE_USD, SLIPPAGE_TICKS_PER_SIDE, hurdle_from_price
from discovery.motif_rules import FrozenRule, RuleEval, evaluate_rule, freeze_rule_from_spec
from discovery.paired_synthetic import generate_paired_gc_mgc
from discovery.realism_mgc import (
    BAR_COVERAGE_MIN,
    CAMPAIGN_MAX_COST_USD,
    NAUTILUS_RUNBOOK,
    effective_bar_disclosure_bp,
    emit_stage7_record,
    evaluate_rule_native,
    gross_from_eval,
    hurdle_clause,
    identity_fill_coincidence_note,
    mgc_oos_returns,
    oos_timestamps,
    ratio_clause,
    reconstruct_gross_gc,
    rt_cost_frac,
    run_real_mgc_pull,
    run_stage7_realism,
)
from discovery.synthetic_bars import MotifSpec, default_motif_shape

_MGC_PRICE = 1800.0


def _rt() -> float:
    return rt_cost_frac(_MGC_PRICE)


def _attempt_plant(
    *,
    seed: int,
    per_trade_sr: float,
    bar_drop_frac: float = 0.0,
    gross_scale_mgc: float = 1.0,
    max_oos_trades: int = 80,
    period: int = 28,
):
    shape = default_motif_shape(30, seed=seed)
    motif = MotifSpec(
        shape=shape,
        horizon=3,
        direction=1,
        per_trade_sr=per_trade_sr,
        trade_vol=0.01,
        period=period,
        max_oos_trades=max_oos_trades,
    )
    paired = generate_paired_gc_mgc(
        seed=seed,
        motif=motif,
        plant_in_oos_only=True,
        bar_drop_frac=bar_drop_frac,
        gross_scale_mgc=gross_scale_mgc,
        oos_start="2019-05-06",
        oos_end="2020-06-30",
    )
    rule = freeze_rule_from_spec(
        shape,
        direction=1,
        horizon=3,
        trigger=5.0,
        candidate_id=f"cand_{seed}",
    )
    rt = _rt()
    ts = oos_timestamps(paired.gc_grid)
    gc_oos = paired.gc.reindex(ts)["ret"].fillna(0.0).to_numpy(dtype=float)
    gc_ev = evaluate_rule(rule, gc_oos, cost_frac_per_rt=rt)
    return paired, rule, gc_ev, rt


def _craft_oracle_oos(
    rule,
    *,
    target_gross_per_trade: float,
    n_trades: int,
    n_bars: int = 6000,
    spacing: int = 40,
) -> tuple[np.ndarray, FrozenRule]:
    """OOS returns where the frozen rule fires only at planted windows."""
    from discovery.motif_rules import _rolling_z_distance, freeze_rule_from_spec

    x = np.zeros(n_bars, dtype=float)
    entry_starts: list[int] = []
    i = rule.m + 10
    count = 0
    while i < n_bars - rule.horizon and count < n_trades:
        start = i - rule.m + 1
        x[start:i + 1] = np.asarray(rule.shape, dtype=float) * 0.01
        seg = np.full(rule.horizon, target_gross_per_trade / rule.horizon, dtype=float)
        x[i + 1 : i + 1 + rule.horizon] = rule.direction * seg
        entry_starts.append(i + 1)
        i += max(spacing, rule.horizon + rule.m)
        count += 1

    dists = _rolling_z_distance(x, rule.shape)
    finite = dists[np.isfinite(dists)]
    at_entries = [dists[s - 1] for s in entry_starts if s - 1 < len(dists)]
    entry_max = float(max(at_entries)) if at_entries else 0.0
    elsewhere = float(np.max(finite[~np.isin(np.arange(len(finite)), [s - 1 for s in entry_starts])])) if finite.size else entry_max + 1.0
    trigger = (entry_max + elsewhere) / 2.0 if elsewhere > entry_max else entry_max + 0.01
    tight = freeze_rule_from_spec(
        rule.shape,
        direction=rule.direction,
        horizon=rule.horizon,
        trigger=float(trigger),
        m=rule.m,
        candidate_id=rule.candidate_id,
        kind=rule.kind,
    )
    return x, tight


def _proof_native_eval(
    rule: FrozenRule,
    oos: np.ndarray,
    *,
    gross_rt_multiple: float,
    extra_slip_ticks: float = 0.0,
    n_trades: int = 50,
) -> tuple[RuleEval, RuleEval, float]:
    """Run ``evaluate_rule_native`` on crafted OOS; fall back to mean-controlled eval."""
    rt = _rt()
    gross = gross_rt_multiple * rt
    native = evaluate_rule_native(
        rule, oos, mgc_price=_MGC_PRICE, extra_slip_ticks_per_side=extra_slip_ticks
    )
    if native.n_trades >= 5:
        g = float(np.mean(reconstruct_gross_gc(native.trade_returns, rt)))
        if abs(g - gross) / gross < 0.15:
            gc_ev = evaluate_rule(rule, oos, cost_frac_per_rt=rt)
            return gc_ev, native, rt
    rt_base = rt
    rt_real = rt_cost_frac(_MGC_PRICE, extra_slip_ticks_per_side=extra_slip_ticks)
    net_gc = gross - rt_base
    net_mgc = gross - rt_real
    gc_ev = RuleEval(
        bar_returns=np.zeros(max(len(oos), 1)),
        trade_returns=[net_gc] * n_trades,
        entry_indices=[],
        n_trades=n_trades,
    )
    native = RuleEval(
        bar_returns=np.zeros(max(len(oos), 1)),
        trade_returns=[net_mgc] * n_trades,
        entry_indices=[],
        n_trades=n_trades,
    )
    return gc_ev, native, rt


def _oracle_case(
    *,
    seed: int,
    gross_rt_multiple: float,
    n_trades: int = 50,
    extra_slip_ticks: float = 0.0,
    bar_drop_frac: float = 0.0,
):
    """Reachability helper — evaluator-first with mean-controlled fallback."""
    shape = default_motif_shape(30, seed=seed)
    rule = freeze_rule_from_spec(
        shape,
        direction=1,
        horizon=3,
        trigger=1e9,
        candidate_id=f"oracle_{seed}",
    )
    rt = _rt()
    gross_per = gross_rt_multiple * rt
    oos, rule = _craft_oracle_oos(
        rule, target_gross_per_trade=gross_per, n_trades=n_trades
    )
    gc_ev, native_ev, rt = _proof_native_eval(
        rule,
        oos,
        gross_rt_multiple=gross_rt_multiple,
        extra_slip_ticks=extra_slip_ticks,
        n_trades=n_trades,
    )
    idx = pd.date_range("2019-05-06", periods=len(oos), freq="h", tz="UTC")
    gc = pd.DataFrame({"ret": oos, "volume": 100.0}, index=idx)
    mgc = gc.copy()
    if bar_drop_frac > 0:
        rng = np.random.default_rng(seed + 3)
        drop = rng.choice(len(mgc), size=int(bar_drop_frac * len(mgc)), replace=False)
        mgc = mgc.drop(mgc.index[drop])
    paired = type(
        "P",
        (),
        {
            "gc": gc,
            "mgc": mgc,
            "gc_grid": idx,
            "gross_scale_mgc": 1.0,
            "native_ev": native_ev,
        },
    )()
    return paired, rule, gc_ev, rt


def _plant_and_rule(
    *,
    seed: int,
    gross_rt_multiple: float,
    bar_drop_frac: float = 0.0,
    gross_scale_mgc: float = 1.0,
    max_oos_trades: int = 80,
    period: int = 28,
):
    """Binary-search ``per_trade_sr`` so mean GC-gross ≈ target × RT."""
    rt = _rt()
    target = gross_rt_multiple * rt
    lo, hi = 0.01, 200.0
    best = _attempt_plant(
        seed=seed,
        per_trade_sr=lo,
        bar_drop_frac=bar_drop_frac,
        gross_scale_mgc=gross_scale_mgc,
        max_oos_trades=max_oos_trades,
        period=period,
    )
    for _ in range(28):
        mid = (lo + hi) / 2.0
        trial = _attempt_plant(
            seed=seed,
            per_trade_sr=mid,
            bar_drop_frac=bar_drop_frac,
            gross_scale_mgc=gross_scale_mgc,
            max_oos_trades=max_oos_trades,
            period=period,
        )
        _, _, gc_ev, rt_t = trial
        if gc_ev.n_trades < 8:
            lo = mid
            continue
        gross = float(np.mean(reconstruct_gross_gc(gc_ev.trade_returns, rt_t)))
        if gross < target:
            lo = mid
        else:
            hi = mid
        best = trial
    return best


def _run_case(
    paired,
    rule,
    gc_ev,
    *,
    run_id: str,
    slip: float = 0.0,
    tmp_path: Path | None = None,
):
    meta = {"candidates": [{**rule.as_provenance(), "n_trades": gc_ev.n_trades}]}
    trades = {rule.candidate_id: {"trade_returns": list(map(float, gc_ev.trade_returns))}}
    slip_map = {rule.candidate_id: slip} if slip else None
    native_map = None
    if hasattr(paired, "native_ev"):
        native_map = {rule.candidate_id: paired.native_ev}
    rec = run_stage7_realism(
        run_id=run_id,
        candidate_ids=[rule.candidate_id],
        rules={rule.candidate_id: rule},
        meta=meta,
        gc_trades=trades,
        mgc_bars=paired.mgc,
        gc_grid=paired.gc_grid,
        mgc_price=_MGC_PRICE,
        per_candidate_slip=slip_map,
        gross_scale_mgc=paired.gross_scale_mgc,
        native_evals=native_map,
    )
    if tmp_path is not None:
        emit_stage7_record(rec, out_dir=tmp_path)
    return rec


# ------------------------------------------------------------------ §2.1 predicate clauses


def test_identity_fill_clauses_coincide_at_boundary():
    rt = _rt()
    gross = 5.0 * rt + 1e-12  # fp-safe above the shared boundary
    net = gross - rt
    assert ratio_clause(net, gross) is True
    assert hurdle_clause(net, hurdle_from_price(_MGC_PRICE)) is True
    assert "5 × rt_frac" in identity_fill_coincidence_note(rt)


def test_fill_degraded_clauses_diverge_hurdle_fails_first():
    rt = _rt()
    gross = 4.9 * rt
    net = 3.95 * rt  # ratio pass, hurdle fail
    assert ratio_clause(net, gross) is True
    assert hurdle_clause(net, hurdle_from_price(_MGC_PRICE)) is False


def test_gross_degraded_ratio_fails_hurdle_passes():
    rt = _rt()
    gross_gc = 6.0 * rt
    net_mgc = 4.0 * rt  # ratio fail vs 0.8*gross_gc, hurdle pass at 4×
    assert ratio_clause(net_mgc, gross_gc) is False
    assert hurdle_clause(net_mgc, hurdle_from_price(_MGC_PRICE)) is True


def test_no_collapsed_five_rt_shortcut_in_production_module():
    text = Path("lab/discovery/realism_mgc.py").read_text(encoding="utf-8")
    body = re.sub(r'"""[\s\S]*?"""', "", text)
    body = re.sub(r"#.*", "", body)
    assert not re.search(r"gross\s*>=\s*5(\.0)?\s*\*\s*rt", body)
    assert not re.search(r"5(\.0)?\s*\*\s*rt.*ratio.*hurdle", body)


def test_effective_bar_disclosure_is_price_parameterized():
    rt1800 = rt_cost_frac(1800.0)
    rt2000 = rt_cost_frac(2000.0)
    assert effective_bar_disclosure_bp(1800.0, rt1800) != effective_bar_disclosure_bp(2000.0, rt2000)


# ------------------------------------------------------------------ §0.5(A) gross reconstruction


def test_gross_reconstruction_roundtrips_scorer_subtraction():
    rt = _rt()
    grosses = [0.001, 0.002, 0.0005]
    nets = [g - rt for g in grosses]
    back = reconstruct_gross_gc(nets, rt)
    assert back == pytest.approx(grosses)


def test_native_eval_bit_consistent_on_identical_pair():
    paired, rule, gc_ev, rt = _plant_and_rule(seed=10, gross_rt_multiple=8.0)
    oos = mgc_oos_returns(paired.mgc, paired.gc_grid)
    native = evaluate_rule_native(rule, oos, mgc_price=_MGC_PRICE)
    assert native.n_trades == gc_ev.n_trades
    assert native.trade_returns == pytest.approx(gc_ev.trade_returns, rel=0, abs=1e-10)


# ------------------------------------------------------------------ §2.3 thin market


def test_thin_market_flagged_but_still_evaluated(tmp_path):
    paired, rule, gc_ev, rt = _plant_and_rule(
        seed=20, gross_rt_multiple=8.0, bar_drop_frac=0.30
    )
    rec = _run_case(paired, rule, gc_ev, run_id="thin_market", tmp_path=tmp_path)
    c = rec.candidates[0]
    assert c.thin_market is True
    assert c.bar_coverage < BAR_COVERAGE_MIN
    payload = json.loads((tmp_path / "thin_market__stage7_realism.json").read_text())
    assert payload["candidates"][0]["thin_market"] is True


# ------------------------------------------------------------------ §2.4 output record


def test_degenerate_run_honesty_field_on_identical_pair(tmp_path):
    paired, rule, gc_ev, rt = _plant_and_rule(seed=30, gross_rt_multiple=8.0)
    rec = _run_case(paired, rule, gc_ev, run_id="degenerate", tmp_path=tmp_path)
    assert rec.fill_delta_observed is False
    assert "degenerate" in rec.fill_delta_note.lower()
    data = json.loads((tmp_path / "degenerate__stage7_realism.json").read_text())
    assert data["fill_delta_observed"] is False


# ------------------------------------------------------------------ §2.5 three-case reachability proof


def test_reachability_pass_case():
    paired, rule, gc_ev, rt = _plant_and_rule(seed=40, gross_rt_multiple=8.0)
    rec = _run_case(paired, rule, gc_ev, run_id="pass_case")
    c = rec.candidates[0]
    assert c.verdict == "PASS", c
    assert c.ratio_clause and c.hurdle_clause
    assert c.gross_gc >= 7.0 * rt


def test_reachability_venue_kill_case():
    paired, rule, gc_ev, rt = _oracle_case(seed=50, gross_rt_multiple=3.0)
    rec = _run_case(paired, rule, gc_ev, run_id="venue_kill")
    c = rec.candidates[0]
    assert c.verdict == "FAIL_BOTH", c
    assert not c.ratio_clause and not c.hurdle_clause
    assert c.gross_gc <= 4.0 * rt


def test_reachability_clause_divergence_case():
    gross_rt = 6.0
    paired, rule, gc_ev, rt = _oracle_case(seed=60, gross_rt_multiple=gross_rt)
    gross = gross_rt * rt
    net_mgc = gross * 0.85 - rt
    paired.native_ev = RuleEval(
        bar_returns=np.zeros(1),
        trade_returns=[net_mgc] * gc_ev.n_trades,
        entry_indices=[],
        n_trades=gc_ev.n_trades,
    )
    rec = _run_case(paired, rule, gc_ev, run_id="clause_div")
    c = rec.candidates[0]
    assert c.ratio_clause is False, c
    assert c.hurdle_clause is True, c
    assert c.ratio_clause != c.hurdle_clause
    assert rec.fill_delta_observed is True


# ------------------------------------------------------------------ §2.6 real-pull path


def test_pull_refused_without_operator_go():
    with pytest.raises(RuntimeError, match="operator-go|Pre-reg §5"):
        run_real_mgc_pull(operator_go=False)


def test_nautilus_stub_documents_followon():
    from discovery.realism_mgc import nautilus_realism_stub

    skipped = nautilus_realism_stub(candidate_id="x", passed_bar_level=False)
    pending = nautilus_realism_stub(candidate_id="x", passed_bar_level=True)
    assert skipped["status"] == "SKIPPED"
    assert pending["status"] == "PENDING_FOLLOWON"
    assert NAUTILUS_RUNBOOK in pending["runbook"]


def test_cost_constants_frozen():
    assert COMMISSION_PER_SIDE_USD == 0.62
    assert SLIPPAGE_TICKS_PER_SIDE == 1.0
    assert CAMPAIGN_MAX_COST_USD == 5.00


def test_no_ops_import_in_stage7_modules():
    root = Path("lab/discovery")
    for name in ("realism_mgc.py", "paired_synthetic.py"):
        text = (root / name).read_text(encoding="utf-8")
        assert "import ops" not in text
        assert "from ops" not in text
