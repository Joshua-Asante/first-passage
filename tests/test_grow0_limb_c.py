"""Tests for GROW-0 Limb C (lab/discovery/grow0_limb_c.py) and the additive edge_dollars
extension to grow0_dgp.py / grow0_scoring.py it depends on.

Style mirrors tests/test_grow0_scoring.py / test_grow0_harness.py: plain pytest functions, direct
assertions, no test classes. Per the design note's own known-error-class guidance (v1/v2/v3
history), this file specifically covers: determinism, edge-shape SR verification via the same
brentq-solve-then-check pattern GROW-0 used, a seeding-uniqueness spot-check (Limb C's new root
vs GROW-0's own untouched root), and the population-scoping arithmetic in _aggregate_condition
against hand-built fixtures (the exact class of mistake v1's gate-(a) mislabeling was).
"""
from __future__ import annotations

import math

import numpy as np
import pytest
from scipy.optimize import brentq

from discovery import grow0_dgp, grow0_limb_c
from discovery.grow0_dgp import EDGE_DOLLARS, GROW0_ROOT_SEED, draw_daily_pnl
from discovery.grow0_limb_c import (
    AS_RUN,
    BOUNDARY,
    LIMB_C_ROOT_SEED,
    ConditionSpec,
    _aggregate_condition,
    append_retry_ledger,
    run_condition,
    run_limb_c,
    wilson_ci,
)
from discovery.grow0_scoring import PanelResult, _score_all_variants, annualized_sharpe

FLOOR = 1.265  # floor_at_k(10, years=6.5) -- pinned literal, matches test_grow0_scoring.py


# --- Additive edge_dollars kwarg: default-preserving, doesn't disturb existing call sites ---


def test_draw_daily_pnl_default_edge_dollars_matches_module_constant():
    """Calling draw_daily_pnl(seed, edge=True) with no edge_dollars kwarg must draw byte-identical
    output to calling it with edge_dollars=EDGE_DOLLARS explicitly -- the additive-extension
    contract (design note §9 item 1, §5 forbidden-move "no existing call site's behavior altered")."""
    seed_a = np.random.SeedSequence(12345)
    seed_b = np.random.SeedSequence(12345)
    default_draw = draw_daily_pnl(seed_a, edge=True)
    explicit_draw = draw_daily_pnl(seed_b, edge=True, edge_dollars=EDGE_DOLLARS)
    np.testing.assert_array_equal(default_draw, explicit_draw)


def test_draw_daily_pnl_smaller_edge_dollars_shifts_mean_down():
    """A smaller edge_dollars (Limb C's own marginal shifts) must produce a smaller planted mean
    shift than the frozen EDGE_DOLLARS=64.4412 Limb A uses -- sanity that the kwarg actually
    threads through, not silently ignored."""
    seed = np.random.SeedSequence(777)
    null_draw = draw_daily_pnl(np.random.SeedSequence(777), edge=False)
    small_edge_draw = draw_daily_pnl(seed, edge=True, edge_dollars=19.9857)
    large_edge_draw = draw_daily_pnl(np.random.SeedSequence(777), edge=True, edge_dollars=64.4412)
    assert null_draw.mean() < small_edge_draw.mean() < large_edge_draw.mean()


def test_score_all_variants_edge_dollars_passthrough_reaches_draw_daily_pnl():
    """_score_all_variants' own additive edge_dollars kwarg (design note §9 item 2) must reach
    draw_daily_pnl -- verified by comparing the edge variant's realized mean against a small vs.
    large edge_dollars value on identical seeds."""
    root = np.random.SeedSequence(999)
    train_children = root.spawn(10)
    root2 = np.random.SeedSequence(999)
    train_children2 = root2.spawn(10)

    pnls_small, stats_small = _score_all_variants(train_children, 5, edge_dollars=19.9857)
    pnls_large, stats_large = _score_all_variants(train_children2, 5, edge_dollars=64.4412)

    # Same seed tree -> null variants (0-4, 6-9) are byte-identical regardless of edge_dollars
    for i in range(10):
        if i != 5:
            np.testing.assert_array_equal(pnls_small[i], pnls_large[i])
    # Variant 5 (the edge variant) differs -- the larger edge_dollars produces a larger mean shift
    assert pnls_small[5].mean() < pnls_large[5].mean()
    assert stats_small[5] < stats_large[5]  # larger planted edge -> higher TRAIN Sharpe


def test_run_panel_default_edge_dollars_unchanged_for_limb_a_shaped_call():
    """A Limb-A-shaped run_panel call with no edge_dollars kwarg must remain byte-identical to
    before the kwarg existed -- reproduces the exact seed tree GROW-0's own RESOLVED closure used
    (branches['limb_a']) and checks the nominee/clears shape, not the literal historical numbers
    (which are re-derived from the real, unmodified run in the results doc, not asserted here)."""
    from discovery.grow0_dgp import build_root_branches, spawn_panel_streams
    from discovery.grow0_scoring import run_panel

    branches = build_root_branches()
    train_children, confirm_children = spawn_panel_streams(branches["limb_a"], 10)
    result = run_panel(train_children, confirm_children, edge_variant_index=5, floor=FLOOR)
    assert result.nominee == 5
    assert result.abandoned is False
    assert result.clears is True


# --- Edge-shape SR verification via brentq-solve-then-check (GROW-0's own §3/§10 pattern) ---

_YEARS = 6.5
_P_ACTIVE = 0.60
_P_WIN = 0.45
_WIN_MEAN, _WIN_SD, _LOSS_MEAN, _LOSS_SD = 200.0, 80.0, -163.60, 60.0


def _ann_sr_closed_form(edge_dollars: float) -> float:
    """Identical closed-form annualization the design note's own §3/§10 uses (and GROW-0's own
    §10 audit hook): daily_mean = p_active*edge; daily_var = p_active*var_y +
    p_active*(1-p_active)*edge^2; ann_sr = daily_mean/sqrt(daily_var)*sqrt(252)."""
    mu_y = _P_WIN * _WIN_MEAN + (1 - _P_WIN) * _LOSS_MEAN
    e_y2 = _P_WIN * (_WIN_SD**2 + _WIN_MEAN**2) + (1 - _P_WIN) * (_LOSS_SD**2 + _LOSS_MEAN**2)
    var_y = e_y2 - mu_y**2
    daily_mean = _P_ACTIVE * edge_dollars
    daily_var = _P_ACTIVE * var_y + _P_ACTIVE * (1 - _P_ACTIVE) * edge_dollars**2
    return daily_mean / math.sqrt(daily_var) * math.sqrt(252)


def test_closed_form_reproduces_limb_a_own_frozen_edge_dollars():
    """Sanity check (design note §10): the same closed-form formula, solved via brentq for
    target_sr=4.0, must reproduce Limb A's own frozen EDGE_DOLLARS=64.4412 -- confirms this test
    file's formula is the identical one GROW-0's own harness/prereg used, not a divergent
    reimplementation."""
    solved = brentq(lambda e: _ann_sr_closed_form(e) - 4.0, 1e-6, 10000.0, xtol=1e-12, rtol=1e-14)
    assert round(solved, 4) == pytest.approx(64.4412, abs=1e-3)
    assert _ann_sr_closed_form(EDGE_DOLLARS) == pytest.approx(4.0, abs=1e-3)


@pytest.mark.parametrize(
    "target_sr,frozen_edge_dollars",
    [(1.8, grow0_limb_c.AS_RUN_EDGE_DOLLARS), (1.265, grow0_limb_c.BOUNDARY_EDGE_DOLLARS)],
)
def test_limb_c_frozen_edge_dollars_round_trips_to_target_sr(target_sr, frozen_edge_dollars):
    """Each Limb C condition's frozen edge_dollars literal (design note §3) must, run back through
    the identical closed-form formula, reproduce its own target_sr to within the same immaterial
    rounding artifact class the design note discloses (<1e-4 SR) -- the brentq-solve-then-check
    pattern GROW-0's own Limb A construction used, applied to Limb C's own two frozen literals."""
    resolved_sr = _ann_sr_closed_form(frozen_edge_dollars)
    assert resolved_sr == pytest.approx(target_sr, abs=5e-6)
    # Independently re-solve via brentq and confirm it recovers the same frozen literal (to 4dp):
    resolved_edge = brentq(
        lambda e: _ann_sr_closed_form(e) - target_sr, 1e-6, 10000.0, xtol=1e-12, rtol=1e-14
    )
    assert round(resolved_edge, 4) == pytest.approx(frozen_edge_dollars, abs=1e-3)


def test_boundary_target_sr_equals_floor_exactly():
    """The boundary condition's target_sr must equal FLOOR exactly (z=0 by construction, design
    note §2(b)) -- not merely close."""
    from discovery.grow0_harness import FLOOR as harness_floor

    assert grow0_limb_c.BOUNDARY_TARGET_SR == harness_floor


# --- Seeding: new/separate root, hierarchical spawn pattern reused verbatim, no collision ---


def test_limb_c_root_is_new_and_separate_from_grow0_root():
    assert LIMB_C_ROOT_SEED == 20260824
    assert GROW0_ROOT_SEED == 20260822
    assert LIMB_C_ROOT_SEED != GROW0_ROOT_SEED


def test_limb_c_root_spawn_order_is_fixed_as_run_then_boundary():
    """design note §7: 'fixed order: (a) as-run, then (b) boundary' -- spawning the root twice
    with the same seed must deterministically reproduce the same two child sequences in the same
    order (SeedSequence.spawn is deterministic given the parent's state)."""
    root1 = np.random.SeedSequence(LIMB_C_ROOT_SEED)
    as_run_1, boundary_1 = root1.spawn(2)
    root2 = np.random.SeedSequence(LIMB_C_ROOT_SEED)
    as_run_2, boundary_2 = root2.spawn(2)
    assert as_run_1.generate_state(4).tolist() == as_run_2.generate_state(4).tolist()
    assert boundary_1.generate_state(4).tolist() == boundary_2.generate_state(4).tolist()
    assert as_run_1.generate_state(4).tolist() != boundary_1.generate_state(4).tolist()


def test_limb_c_leaves_do_not_collide_with_grow0_own_root_leaves():
    """Spot-check (design note §7's own claim: 'no shared lineage, no possibility of the two
    roots' spawn trees colliding, by SeedSequence's own construction'). Draws a representative
    slice of leaves from both roots and confirms zero overlap in generated state -- mirrors
    GROW-0's own v3 §10 diversity spot-check, applied across the two roots rather than within
    one."""
    grow0_root = np.random.SeedSequence(GROW0_ROOT_SEED)
    grow0_branches = grow0_root.spawn(5)
    grow0_leaves = []
    for branch in grow0_branches[:2]:  # limb_a, limb_b top branches -- representative sample
        panel_seqs = branch.spawn(20)
        for p in panel_seqs:
            tr, co = p.spawn(2)
            grow0_leaves.extend(tr.spawn(10))
            grow0_leaves.extend(co.spawn(10))

    limb_c_root = np.random.SeedSequence(LIMB_C_ROOT_SEED)
    as_run_seq, boundary_seq = limb_c_root.spawn(2)
    limb_c_leaves = []
    for branch in (as_run_seq, boundary_seq):
        panel_seqs = branch.spawn(20)
        for p in panel_seqs:
            tr, co = p.spawn(2)
            limb_c_leaves.extend(tr.spawn(10))
            limb_c_leaves.extend(co.spawn(10))

    grow0_states = {tuple(s.generate_state(4)) for s in grow0_leaves}
    limb_c_states = {tuple(s.generate_state(4)) for s in limb_c_leaves}
    assert grow0_states.isdisjoint(limb_c_states)
    # Also no internal collisions within each root's own sampled slice (sanity, mirrors §7):
    assert len(grow0_states) == len(grow0_leaves)
    assert len(limb_c_states) == len(limb_c_leaves)


def test_run_condition_is_deterministic_given_same_seed_sequence():
    """Same root seed, same condition spec, small N -> byte-identical aggregate result on repeat
    (determinism check named explicitly in the dispatch)."""
    tiny_spec = ConditionSpec(
        label="tiny_test", target_sr=1.8, edge_dollars=28.5002, n=25, composite_estimate=0.9095
    )
    root1 = np.random.SeedSequence(424242)
    (seq1,) = root1.spawn(1)
    result1 = run_condition(tiny_spec, seq1)

    root2 = np.random.SeedSequence(424242)
    (seq2,) = root2.spawn(1)
    result2 = run_condition(tiny_spec, seq2)

    assert result1 == result2


# --- wilson_ci: known-value + edge-case checks ---


def test_wilson_ci_matches_hand_computed_value():
    # count=5, n=5500, z=1.96 -- textbook Wilson interval, computed independently here
    p_hat, lo, hi = wilson_ci(5, 5500)
    assert p_hat == pytest.approx(5 / 5500)
    z = 1.96
    n = 5500
    expected_center = (p_hat + z * z / (2 * n)) / (1 + z * z / n)
    expected_half = (z / (1 + z * z / n)) * math.sqrt(
        p_hat * (1 - p_hat) / n + z * z / (4 * n * n)
    )
    assert lo == pytest.approx(expected_center - expected_half, abs=1e-12)
    assert hi == pytest.approx(expected_center + expected_half, abs=1e-12)
    assert 0.0 <= lo <= p_hat <= hi <= 1.0


def test_wilson_ci_zero_denominator_returns_nan():
    p_hat, lo, hi = wilson_ci(0, 0)
    assert math.isnan(p_hat) and math.isnan(lo) and math.isnan(hi)


def test_wilson_ci_clips_to_unit_interval_at_extremes():
    p_hat, lo, hi = wilson_ci(0, 1150)
    assert lo == 0.0
    assert 0.0 <= hi <= 1.0
    p_hat2, lo2, hi2 = wilson_ci(1150, 1150)
    assert hi2 == pytest.approx(1.0, abs=1e-9)  # floating-point cancellation can land just under
    # 1.0 (e.g. 0.9999999999999999) even at p_hat=1 -- the clamp's job is capping values that
    # would otherwise legitimately exceed 1.0, not forcing exact-1.0 in every boundary case.
    assert 0.0 <= lo2 <= 1.0


# --- Population-scoping arithmetic: hand-built fixtures (the v1 mislabeling-class defect) ---


def _fake_result(nominee, abandoned, clears):
    return PanelResult(
        nominee=nominee,
        train_stat=1.0,
        gate_a=not abandoned,
        gate_b=not abandoned,
        abandoned=abandoned,
        confirm_stat=None if abandoned else (2.0 if clears else 0.5),
        clears=clears,
    )


def test_aggregate_condition_population_scoping_hand_built():
    """Hand-built 10-panel fixture exercising every branch of §8's population-scoped definitions:
    - 3 panels: nominee=5, not abandoned, clears -> counts toward nominee5, gatespass, clears, accept
    - 2 panels: nominee=5, not abandoned, does NOT clear -> counts toward nominee5, gatespass; NOT accept
    - 1 panel: nominee=5, abandoned -> counts toward nominee5 AND false-abandonment; NOT gatespass
    - 2 panels: nominee=2 (a null variant), abandoned -> counts toward false-abandonment ONLY
      (unconditional on nominee, per §8) -- NOT nominee5, NOT gatespass
    - 2 panels: nominee=3 (a null variant), not abandoned, does not clear -> none of the four
      numerators (correctly excluded: wrong nominee, not abandoned)
    """
    results = (
        [_fake_result(5, False, True)] * 3
        + [_fake_result(5, False, False)] * 2
        + [_fake_result(5, True, False)] * 1
        + [_fake_result(2, True, False)] * 2
        + [_fake_result(3, False, False)] * 2
    )
    spec = ConditionSpec(
        label="fixture", target_sr=1.8, edge_dollars=28.5002, n=10, composite_estimate=0.30
    )
    agg = _aggregate_condition(spec, results)

    assert agg["n"] == 10
    assert agg["nominee_5_count"] == 6  # 3+2+1 -- every panel where variant 5 won the argmax
    assert agg["gates_pass_given_nominee5_count"] == 5  # 3+2 -- nominee=5 AND not abandoned
    assert agg["confirm_clears_given_nominee5_gatespass_count"] == 3  # the 3 that also cleared
    assert agg["accept_count"] == 3  # identical to clears_count (three-conjunct definition)
    # False-abandonment: unconditional on nominee -- the nominee=5-abandoned panel (1) PLUS the
    # two nominee=2-abandoned panels (2) = 3, NOT just the nominee=5 abandonment:
    assert agg["abandoned_count"] == 3
    assert agg["p_nominee5"]["point"] == pytest.approx(0.6)
    assert agg["p_gatespass_given_nominee5"]["point"] == pytest.approx(5 / 6)
    assert agg["p_clears_given_nominee5_gatespass"]["point"] == pytest.approx(3 / 5)
    assert agg["p_accept"]["point"] == pytest.approx(0.3)
    assert agg["p_false_abandonment"]["point"] == pytest.approx(0.3)


def test_aggregate_condition_verdict_corroborated_when_ci_contains_estimate():
    # 100/100 accept -> p_accept point=1.0, CI is narrow but nonzero-width; pick a composite
    # estimate inside a wide-enough CI by using a smaller, non-degenerate count instead.
    results = [_fake_result(5, False, True)] * 91 + [_fake_result(5, False, False)] * 9
    spec = ConditionSpec(
        label="fixture_corrob", target_sr=1.8, edge_dollars=28.5002, n=100, composite_estimate=0.91
    )
    agg = _aggregate_condition(spec, results)
    assert agg["p_accept"]["point"] == pytest.approx(0.91)
    assert agg["p_accept"]["lo"] <= 0.91 <= agg["p_accept"]["hi"]
    assert agg["verdict"] == "CORROBORATED"


def test_aggregate_condition_verdict_diverged_when_ci_excludes_estimate():
    # All panels miss -> p_accept point=0.0, CI upper bound is small but nonzero; a composite
    # estimate far outside (e.g. 0.90) must DIVERGE.
    results = [_fake_result(2, False, False)] * 50
    spec = ConditionSpec(
        label="fixture_diverged", target_sr=1.8, edge_dollars=28.5002, n=50, composite_estimate=0.90
    )
    agg = _aggregate_condition(spec, results)
    assert agg["p_accept"]["point"] == pytest.approx(0.0)
    assert agg["p_accept"]["hi"] < 0.90
    assert agg["verdict"] == "DIVERGED"


def test_aggregate_condition_gatespass_denominator_zero_is_nan_not_crash():
    """If no panel ever nominates variant 5 (pathological, but must not crash): gatespass and
    clears CIs both degrade to NaN gracefully (n=0 denominator), and the verdict still resolves
    (via p_accept, whose own denominator is N, never zero at real N)."""
    results = [_fake_result(2, False, False)] * 5
    spec = ConditionSpec(
        label="fixture_zero_nominee5", target_sr=1.8, edge_dollars=28.5002, n=5,
        composite_estimate=0.5,
    )
    agg = _aggregate_condition(spec, results)
    assert agg["nominee_5_count"] == 0
    assert math.isnan(agg["p_gatespass_given_nominee5"]["point"])
    assert math.isnan(agg["p_clears_given_nominee5_gatespass"]["point"])
    assert agg["p_accept"]["point"] == pytest.approx(0.0)  # N=5 denominator, not nominee5-count
    assert agg["verdict"] == "DIVERGED"


# --- Retry ledger: append-only, separate file from GROW-0's own ---


def test_append_retry_ledger_is_append_only(tmp_path):
    path = tmp_path / "grow0_limb_c_retry_ledger_test.jsonl"
    append_retry_ledger({"run_id": "a"}, path=path)
    append_retry_ledger({"run_id": "b"}, path=path)
    lines = path.read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 2
    assert '"run_id": "a"' in lines[0]
    assert '"run_id": "b"' in lines[1]


def test_run_limb_c_smoke_tiny_conditions(tmp_path, monkeypatch):
    """End-to-end smoke test at drastically reduced N (not the frozen 1,150) -- verifies run_limb_c
    wires both conditions, writes one ledger line covering both, and returns well-shaped dicts.
    Does NOT assert on the frozen N=1,150 literals (that's the real run, done separately at full
    scale and reported in the results doc, not re-run inside the test suite)."""
    tiny_as_run = ConditionSpec(
        label="as_run", target_sr=1.8, edge_dollars=28.5002, n=15, composite_estimate=0.9095
    )
    tiny_boundary = ConditionSpec(
        label="boundary", target_sr=1.265, edge_dollars=19.9857, n=15, composite_estimate=0.4656
    )
    monkeypatch.setattr(grow0_limb_c, "AS_RUN", tiny_as_run)
    monkeypatch.setattr(grow0_limb_c, "BOUNDARY", tiny_boundary)

    ledger_path = tmp_path / "smoke_ledger.jsonl"
    result = run_limb_c(
        run_id="test-smoke",
        started_at_arg="2026-08-24T00:00:00Z",
        prereg_commit="deadbeef",
        ledger_path=ledger_path,
    )
    assert result["as_run"]["n"] == 15
    assert result["boundary"]["n"] == 15
    assert result["as_run"]["verdict"] in ("CORROBORATED", "DIVERGED")
    assert result["boundary"]["verdict"] in ("CORROBORATED", "DIVERGED")
    lines = ledger_path.read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 1  # one line covering BOTH conditions, per design note §7
