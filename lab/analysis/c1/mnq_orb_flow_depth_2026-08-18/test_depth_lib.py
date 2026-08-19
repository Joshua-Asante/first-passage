"""MNQFLOW-1-DEPTH — hand-computed unit tests for the statistic core.

PREREG §9 step 4: these must ALL PASS before the runner reads a real quote.
Synthetic / fake quote data only — no MBP-10, no Databento, no pull.

Every expected value below is computed BY HAND in the test's own comment, never by
running the code and pasting its output. Adversarial guards (empty/NaN/vacuous
placebo) mirror the parent MNQFLOW-1 suite.

Run:
  .venv-research/Scripts/python.exe -m pytest \\
    lab/analysis/c1/mnq_orb_flow_depth_2026-08-18/test_depth_lib.py -q
"""
from __future__ import annotations

import numpy as np
import pytest
from research_utils.camp_import import load_camp_sibling

dl = load_camp_sibling("depth_lib", __file__)


# --------------------------------------------------------------- frozen constants
def test_frozen_constants():
    """Pin harness constants to the FROZEN PREREG table (no silent drift)."""
    assert dl.SEED == 20260818
    assert dl.N_BOOT == 10_000
    assert dl.N_PLACEBO == 1_000
    assert dl.EPS_RATIO == 0.001
    assert dl.COV_MIN == 0.90
    assert dl.N_LEVELS == 10
    assert dl.PARENT_N == 255
    assert dl.SAMPLE_K == 30
    assert dl.SAMPLE_SPAN == 254


# --------------------------------------------------------------- S3 / S3': features
def test_a_depth_hand_computed():
    # bid [10,5,3,2,1,1,1,1,1,1] sum=26; ask [2]*10 sum=20
    # A_depth = (26-20)/(26+20) = 6/46 = 3/23
    bid = [10, 5, 3, 2, 1, 1, 1, 1, 1, 1]
    ask = [2] * 10
    assert dl.a_depth(bid_sizes=bid, ask_sizes=ask) == pytest.approx(3 / 23)


def test_a_l1_hand_computed_matches_parent_formula():
    # level-0 only: (10-2)/(10+2) = 8/12 = 2/3
    bid = [10, 5, 3, 2, 1, 1, 1, 1, 1, 1]
    ask = [2] * 10
    assert dl.a_l1(bid_sizes=bid, ask_sizes=ask) == pytest.approx(2 / 3)
    # parent asym(bid0, ask0) identity
    assert dl.a_l1(bid_sizes=bid, ask_sizes=ask) == pytest.approx(
        dl.book_imbalance([10], [2])
    )


def test_a_depth_from_databento_shaped_mapping():
    # same book as above, via bid_sz_00..09 / ask_sz_00..09
    quote = {f"bid_sz_{i:02d}": v for i, v in enumerate([10, 5, 3, 2, 1, 1, 1, 1, 1, 1])}
    quote.update({f"ask_sz_{i:02d}": 2.0 for i in range(10)})
    assert dl.a_depth(quote) == pytest.approx(3 / 23)
    assert dl.a_l1(quote) == pytest.approx(2 / 3)


def test_empty_book_is_nan_not_zero():
    # bid+ask == 0 carries no information. Returning 0.0 would fabricate "balanced".
    assert np.isnan(dl.book_imbalance([0] * 10, [0] * 10))
    assert np.isnan(dl.a_depth(bid_sizes=[0] * 10, ask_sizes=[0] * 10))
    assert np.isnan(dl.a_l1(bid_sizes=[0] * 10, ask_sizes=[0] * 10))


def test_missing_deeper_levels_count_as_zero():
    # Only levels 0..2 populated; rest missing → treated as size 0 (§2.3).
    # bid: 4+3+2+0*7 = 9; ask: 1+1+1+0*7 = 3; A = (9-3)/(9+3) = 6/12 = 0.5
    quote = {
        "bid_sz_00": 4.0,
        "bid_sz_01": 3.0,
        "bid_sz_02": 2.0,
        "ask_sz_00": 1.0,
        "ask_sz_01": 1.0,
        "ask_sz_02": 1.0,
        # levels 3..9 absent
    }
    assert dl.a_depth(quote) == pytest.approx(0.5)


def test_signed_imbalance_long_and_short():
    # long : +A -> 0.5 ; short : -A on the same book -> -0.5
    assert dl.signed_imbalance(0.5, "long") == pytest.approx(0.5)
    assert dl.signed_imbalance(0.5, "short") == pytest.approx(-0.5)


def test_short_side_is_exactly_the_negation_of_long():
    """ADVERSARIAL: a regression that dropped the direction flip would pass every
    other test in this file. This one pins the flip itself."""
    v = 0.37
    assert dl.signed_imbalance(v, "short") == pytest.approx(
        -dl.signed_imbalance(v, "long")
    )


def test_bad_side_raises():
    with pytest.raises(ValueError):
        dl.signed_imbalance(0.1, "up")


def test_window_mean_hand_computed():
    # (0.5 + 0.0) / 2 = 0.25
    assert dl.window_mean([0.5, 0.0]) == pytest.approx(0.25)


def test_empty_window_is_none_not_zero():
    """ADVERSARIAL / silent-bias guard. A window with no usable quote is NO-DATA."""
    assert dl.window_mean([]) is None
    assert dl.window_mean([float("nan"), float("nan")]) is None


# --------------------------------------------------------------- S8: agreement
def test_agreement_stats_happy_path():
    # depth_diff = -0.02, l1_diff = -0.01 → ratio = 2.0, same sign
    ratio, agree = dl.agreement_stats(-0.02, -0.01)
    assert ratio == pytest.approx(2.0)
    assert agree is True


def test_agreement_near_zero_l1_denominator_is_undefined():
    """PREREG W5 / S8 — expected-to-occur given L1 tie-saturation, not an edge skip.
    abs(l1_diff) = 0.0005 < EPS_RATIO = 0.001 → ratio is None by design."""
    ratio, agree = dl.agreement_stats(0.02, 0.0005)
    assert ratio is None
    assert agree is True  # both positive


def test_agreement_at_eps_ratio_boundary_is_defined():
    # abs(l1_diff) == 0.001 is NOT < EPS_RATIO → ratio is computed
    ratio, agree = dl.agreement_stats(0.002, 0.001)
    assert ratio == pytest.approx(2.0)
    assert agree is True


def test_agreement_sign_disagree():
    ratio, agree = dl.agreement_stats(0.02, -0.01)
    assert ratio == pytest.approx(2.0)
    assert agree is False


# --------------------------------------------------------------- S2: systematic sample
EXPECTED_S2_INDICES = (
    0, 9, 18, 26, 35, 44, 53, 61, 70, 79,
    88, 96, 105, 114, 123, 131, 140, 149, 158, 166,
    175, 184, 193, 201, 210, 219, 228, 236, 245, 254,
)


def test_systematic_sample_indices_pin_frozen_formula():
    # round(i * 254/29) for i = 0..29 — hand-checked against Python builtin round
    idxs = dl.systematic_sample_indices()
    assert idxs == EXPECTED_S2_INDICES
    assert idxs[0] == 0
    assert idxs[-1] == 254
    assert len(idxs) == 30


def test_systematic_sample_includes_last_not_stride8_endpoint():
    """The rejected stride-8-from-0 scheme ends at 232; full-range includes 254."""
    idxs = dl.systematic_sample_indices()
    assert 254 in idxs
    assert idxs[-1] != 232


def test_take_systematic_sample_on_chrono_range():
    chrono = list(range(255))
    sample = dl.take_systematic_sample(chrono)
    assert sample == EXPECTED_S2_INDICES


# --------------------------------------------------------------- S5: bootstrap
def test_observed_stat_hand_computed():
    # session 0: trigger 1.0, controls 0.0, 0.0
    # session 1: trigger 0.0, controls 0.0, 0.0
    # trigger mean = 0.5; control mean = 0.0; stat = 0.5
    s = [np.array([1.0, 0.0, 0.0]), np.array([0.0, 0.0, 0.0])]
    assert dl.observed_stat(s) == pytest.approx(0.5)
    assert dl.means(s) == (pytest.approx(0.5), pytest.approx(0.0))


def test_ragged_sessions_weight_controls_by_real_count():
    # trigger mean = 1.0; control mean = (0.5+0.5+0.2)/3 = 0.4; stat = 0.6
    s = [np.array([1.0, 0.5, 0.5]), np.array([1.0, 0.2])]
    assert dl.means(s) == (pytest.approx(1.0), pytest.approx(0.4))
    assert dl.observed_stat(s) == pytest.approx(0.6)


def test_bootstrap_on_identical_sessions_is_a_point():
    s = [np.array([1.0, 0.0]) for _ in range(4)]
    lo, hi = dl.session_block_bootstrap(s, n=200)
    assert lo == pytest.approx(1.0) and hi == pytest.approx(1.0)


def test_bootstrap_is_deterministic_under_seed():
    s = [np.array([1.0, 0.0, 0.3]), np.array([0.2, 0.1, 0.0]), np.array([-0.4, 0.2, 0.1])]
    assert dl.session_block_bootstrap(s, n=500, seed=1) == dl.session_block_bootstrap(
        s, n=500, seed=1
    )
    assert dl.session_block_bootstrap(s, n=500, seed=1) != dl.session_block_bootstrap(
        s, n=500, seed=2
    )


def test_bootstrap_ci_is_ordered():
    s = [np.array([1.0, 0.0, 0.3]), np.array([0.2, 0.1, 0.0]), np.array([-0.4, 0.2, 0.1])]
    lo, hi = dl.session_block_bootstrap(s, n=500)
    assert lo <= hi


def test_bootstrap_default_seed_is_prereg_seed():
    """Default seed must be 20260818 (S5), not the parent's 20260805."""
    s = [np.array([1.0, 0.0, 0.3]), np.array([0.2, 0.1, 0.0]), np.array([-0.4, 0.2, 0.1])]
    assert dl.session_block_bootstrap(s, n=300) == dl.session_block_bootstrap(
        s, n=300, seed=20260818
    )


# --------------------------------------------------------------- S6: placebo
def test_placebo_j_zero_reproduces_observed():
    """NON-VACUITY: j=0 must reduce to the observed statistic."""
    s = [np.array([1.0, 0.5, 0.5]), np.array([1.0, 0.2, -0.3])]
    M, lens = dl._pad(s)
    j0 = np.zeros(len(s), int)
    assert dl._stat_from_choice(M, lens, j0) == pytest.approx(dl.observed_stat(s))


def test_placebo_actually_permutes():
    """ADVERSARIAL: a placebo that returned the observed value every rep would be a
    rubber stamp. Assert it produces genuine spread."""
    s = [np.array([1.0, 0.0]), np.array([1.0, 0.0]), np.array([1.0, 0.0])]
    p = dl.within_session_placebo(s, n=200)
    assert len(np.unique(p)) > 1


def test_placebo_deterministic_under_seed():
    s = [np.array([1.0, 0.5, 0.5]), np.array([1.0, 0.2, -0.3])]
    assert np.array_equal(
        dl.within_session_placebo(s, n=100, seed=3),
        dl.within_session_placebo(s, n=100, seed=3),
    )


# --------------------------------------------------------- assemble (NaN trap)
def test_assemble_drops_nan_not_just_none():
    """REGRESSION from parent: NaN controls must be dropped, never zeroed."""
    pairs = [(1.0, [0.5, float("nan"), 0.3])]
    sessions, no_t, no_c = dl.assemble_sessions(pairs)
    assert len(sessions) == 1
    assert sessions[0].tolist() == [1.0, 0.5, 0.3]
    assert (no_t, no_c) == (0, 0)
    assert dl.means(sessions) == (pytest.approx(1.0), pytest.approx(0.4))


def test_assemble_drops_sessions_with_nan_trigger():
    pairs = [(float("nan"), [0.5, 0.3]), (None, [0.2]), (1.0, [0.0])]
    sessions, no_t, no_c = dl.assemble_sessions(pairs)
    assert len(sessions) == 1 and no_t == 2 and no_c == 0


def test_assemble_drops_sessions_left_without_controls():
    pairs = [(1.0, [float("nan"), None]), (1.0, [0.0])]
    sessions, no_t, no_c = dl.assemble_sessions(pairs)
    assert len(sessions) == 1 and no_t == 0 and no_c == 1


def test_pad_refuses_a_nonfinite_row():
    with pytest.raises(ValueError):
        dl.observed_stat([np.array([1.0, float("nan")]), np.array([1.0, 0.0])])


def test_empty_and_degenerate_inputs_raise():
    with pytest.raises(ValueError):
        dl.observed_stat([])
    with pytest.raises(ValueError):
        dl.observed_stat([np.array([1.0])])


# --------------------------------------------------------------- §2.3 controls
def test_select_controls_takes_five_closest():
    # trigger at tod=120; candidates every 5 min from 60..180
    # eligible: |d| in [15, 30] → tod in [90,105] U [135,150]
    trigger = 120.0
    cands = list(range(60, 185, 5))  # 60,65,...,180
    chosen = dl.select_controls(trigger, cands)
    assert chosen is not None
    assert len(chosen) == 5
    # closest eligible by abs distance, ties → earlier clock
    # distances: 105→15, 100→20, 95→25, 90→30, 135→15, 140→20, 145→25, 150→30
    # sorted: (15,105), (15,135), (20,100), (20,140), (25,95) → first five
    picked_tods = [cands[i] for i in chosen]
    assert picked_tods == [105, 135, 100, 140, 95]


def test_select_controls_shortfall_below_floor_is_none():
    # only one eligible candidate → below floor of 2 → None
    trigger = 100.0
    cands = [100.0, 101.0, 118.0]  # 118 is |d|=18, inside [15,30]; others too close
    assert dl.select_controls(trigger, cands) is None


def test_select_controls_keeps_shortfall_at_or_above_floor():
    # two eligible → keep both (floor=2)
    trigger = 100.0
    cands = [80.0, 120.0, 200.0]  # |20|, |20|; 200 is |100| > 30 → out
    chosen = dl.select_controls(trigger, cands)
    assert chosen == (0, 1)


def test_select_controls_rejects_inside_min_sep():
    trigger = 100.0
    cands = [110.0, 112.0]  # |10|, |12| — both < 15 min sep
    assert dl.select_controls(trigger, cands) is None


# --------------------------------------------------------------- §7 verdict table
def test_verdict_w6_void_coverage():
    # coverage 0.89 outranks an otherwise-RESOLVED world
    assert (
        dl.verdict(0.89, 0.03, 0.03, (0.02, 0.04)) == "VOID-COVERAGE"
    )


def test_verdict_coverage_at_floor_is_not_w6():
    # coverage == 0.90 is NOT < 0.90 → fall through
    assert (
        dl.verdict(0.90, 0.03, 0.03, (0.02, 0.04)) == "RESOLVED-CONSISTENT"
    )


def test_verdict_w5_void_ratio_undefined():
    # abs(l1_diff)=0.0005 < 0.001; depth CI would otherwise look fine
    assert (
        dl.verdict(1.0, 0.0005, 0.02, (0.01, 0.03)) == "VOID-RATIO-UNDEFINED"
    )


def test_verdict_w5_does_not_fire_at_eps_boundary():
    # abs(l1_diff)==0.001 is defined → not W5; ratio=2.0 → W2
    assert (
        dl.verdict(1.0, 0.001, 0.002, (0.001, 0.003)) == "RESOLVED-CONSISTENT"
    )


def test_verdict_w4_falsified_sign_disagree():
    # l1 +0.02, depth −0.02; CI excludes 0 on the depth side
    assert (
        dl.verdict(1.0, 0.02, -0.02, (-0.03, -0.01))
        == "FALSIFIED-DEPTH-DILUTES-OR-REVERSES"
    )


def test_verdict_w3_ambiguous_underpowered():
    # same sign, but CI includes 0
    assert (
        dl.verdict(1.0, 0.03, 0.03, (-0.01, 0.01)) == "AMBIGUOUS-UNDERPOWERED"
    )


def test_verdict_w3_ci_touching_zero():
    # boundary: CI touching exactly 0 still counts as including 0
    assert (
        dl.verdict(1.0, 0.03, 0.03, (0.0, 0.04)) == "AMBIGUOUS-UNDERPOWERED"
    )


def test_verdict_w2_resolved_consistent():
    # depth=0.03, l1=0.03 → ratio=1.0 ∈ [0.5, 2.0]
    assert (
        dl.verdict(1.0, 0.03, 0.03, (0.02, 0.04)) == "RESOLVED-CONSISTENT"
    )


def test_verdict_w2_at_ratio_half_and_double():
    assert (
        dl.verdict(1.0, 0.04, 0.02, (0.01, 0.03)) == "RESOLVED-CONSISTENT"
    )  # ratio = 0.5
    assert (
        dl.verdict(1.0, 0.02, 0.04, (0.03, 0.05)) == "RESOLVED-CONSISTENT"
    )  # ratio = 2.0


def test_verdict_w1a_depth_amplified():
    # depth=0.05, l1=0.02 → ratio=2.5 > 2.0
    assert (
        dl.verdict(1.0, 0.02, 0.05, (0.03, 0.07)) == "RESOLVED-DEPTH-AMPLIFIED"
    )


def test_verdict_w1b_depth_attenuated():
    # depth=0.01, l1=0.03 → ratio=1/3 < 0.5
    assert (
        dl.verdict(1.0, 0.03, 0.01, (0.005, 0.015)) == "RESOLVED-DEPTH-ATTENUATED"
    )


def test_verdict_precedence_w6_before_w5():
    """W6 outranks W5 even when the L1 denom is also undefined."""
    assert (
        dl.verdict(0.5, 0.0001, 0.02, (0.01, 0.03)) == "VOID-COVERAGE"
    )


def test_verdict_does_not_consume_placebo():
    """DEPTH §7 has no placebo limb — placebo is reported, not gated.
    Signature must not require a placebo argument."""
    import inspect

    params = inspect.signature(dl.verdict).parameters
    assert "placebo" not in params
