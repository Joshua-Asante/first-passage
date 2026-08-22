import pytest

from discovery.grow0_harness import FLOOR, check_cost_wiring


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
