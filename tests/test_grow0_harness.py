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
