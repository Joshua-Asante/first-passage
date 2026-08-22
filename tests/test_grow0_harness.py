import pytest

from discovery.grow0_dgp import TRUE_EDGE_VARIANT_INDEX
from discovery.grow0_harness import FLOOR, check_cost_wiring, run_limb_a


def test_floor_matches_prereg():
    assert round(FLOOR, 3) == 1.265


def test_check_cost_wiring_passes():
    check_cost_wiring()  # must not raise


def test_check_cost_wiring_catches_a_broken_mnq_resolution(monkeypatch):
    import discovery.grow0_harness

    def _broken_resolve(firm_key, instrument):
        raise ValueError("simulated breakage")

    monkeypatch.setattr(discovery.grow0_harness, "resolve_commission", _broken_resolve)
    with pytest.raises(AssertionError):
        check_cost_wiring()


def test_run_limb_a_passes_with_frozen_seed():
    verdict, result = run_limb_a()
    # SR=4.0 planted edge is deterministic-in-practice per the prereg's own power
    # derivation (confirm-clear probability 1.00000000 at this target) -- a fresh,
    # frozen-tree run should PASS; a FAIL here means the harness code has a bug,
    # not that the design is underpowered (see prereg §3 "Why SR=4.0")
    assert verdict == "PASS"
    assert result.nominee == TRUE_EDGE_VARIANT_INDEX
    assert result.clears is True


def test_limb_b_constants_match_prereg_section_4():
    from discovery.grow0_harness import LIMB_B_C, LIMB_B_N

    assert LIMB_B_N == 5500
    assert LIMB_B_C == 7


def test_assert_seed_diversity_passes_on_distinct_leaves():
    from discovery.grow0_dgp import build_root_branches, spawn_panel_streams
    from discovery.grow0_harness import assert_seed_diversity

    branches = build_root_branches()
    panels = branches["limb_b"].spawn(20)
    leaves = []
    for p in panels:
        tr, co = spawn_panel_streams(p, 10)
        leaves.extend(tr)
        leaves.extend(co)
    assert_seed_diversity(leaves, min_distinct=400)  # 20 panels x 20 leaves = 400, all distinct


def test_assert_seed_diversity_catches_a_collapsed_run():
    from discovery.grow0_dgp import build_root_branches
    from discovery.grow0_harness import assert_seed_diversity

    branches = build_root_branches()
    one_panel = branches["limb_b"].spawn(1)[0]
    collapsed_leaves = [one_panel] * 400  # simulates a broadcast/closure bug: every
    # "panel" resolves to the SAME underlying SeedSequence
    with pytest.raises(AssertionError):
        assert_seed_diversity(collapsed_leaves, min_distinct=400)


def test_run_limb_b_small_n_returns_consistent_shape():
    """Uses a small N for speed (this plan's local-compute-budget constraint) --
    the frozen N=5,500/c=7 pair is exercised only by the manual full-scale
    invocation documented in Task 13, never by the automated test suite."""
    from discovery.grow0_harness import run_limb_b

    small_n, small_c = 100, 3  # not the frozen pair -- structural test only
    verdict, sum_clears, results = run_limb_b(n=small_n, c=small_c)
    assert verdict in ("PASS", "FAIL")
    assert len(results) == small_n
    assert sum_clears == sum(1 for r in results if r.clears)
    assert (verdict == "FAIL") == (sum_clears >= small_c)


def test_run_red_leak_fails_as_expected_at_frozen_scale():
    """RED-LEAK's own expected clear rate (~0.59%, per RED-BLIND's empirical measurement)
    is low enough that even c=1 requires a large N to be deterministic-in-practice.
    n=500 had P(zero clears) ≈ 0.0521 (~5.2%), causing ~5.2% spurious failures.
    n=2000 gives P(zero clears) ≈ 0.0000066 (~0.00066%), rendering the test
    deterministic for all practical purposes (standard used elsewhere for SR=4.0 edges).
    2000 panels x ~0.0059 ≈ 12 expected clears; c=1 makes FAIL verdict reliable."""
    from discovery.grow0_harness import run_red_leak

    verdict = run_red_leak(n=2000, c=1)
    assert verdict == "FAILED_AS_EXPECTED"
