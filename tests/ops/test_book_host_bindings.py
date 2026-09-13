"""Inert fixed-book identities must never enter the historical sizing path."""
import json

import pytest

import lifecycle
import c1_sizing_host_reference as host_module
from book_policy import BOOK_LEGS


EXPECTED = {
    "aegis_6j": "Aegis 6J",
    "dj30_mym_p250": "Striker MYM p250",
    "vanguard_mgc": "Vanguard MGC",
    "orb_mnq_v7": "ORB MNQ v7",
}


def test_book_bindings_are_inert_and_match_policy():
    bindings = host_module.generate_book_bindings()
    assert {key: row["leg_key"] for key, row in bindings.items()} == EXPECTED
    assert set(bindings).isdisjoint(host_module.LEG_MAP)
    assert set(EXPECTED.values()) <= lifecycle.STRATEGY_KEYS
    for spec in BOOK_LEGS:
        row = bindings[spec.leg_id]
        assert row == {"leg_key": spec.lifecycle_key, "symbol": spec.symbol,
                       "cap_alloc": 0, "order_symbol": None}
    # Returning configuration must not expose mutable shared allocation state.
    bindings["aegis_6j"]["cap_alloc"] = 80
    assert host_module.generate_book_bindings()["aegis_6j"]["cap_alloc"] == 0


def test_lifecycle_loader_accepts_explicit_book_states(tmp_path, monkeypatch):
    state_file = tmp_path / "lifecycle.json"
    state = dict(zip(EXPECTED.values(), lifecycle.TIER_MULTIPLIER))
    state_file.write_text(json.dumps(state), encoding="utf-8")
    monkeypatch.setattr(lifecycle, "STATE_FILE", state_file)
    assert lifecycle.load_lifecycle_state() == state


@pytest.mark.parametrize("leg_id", EXPECTED)
@pytest.mark.parametrize("signal_type", ["entry", "add", "exit", "flat"])
def test_book_signal_cannot_use_legacy_host_even_with_injected_map(
        tmp_path, monkeypatch, leg_id, signal_type):
    monkeypatch.setitem(host_module.LEG_MAP, leg_id,
                        {"leg_key": EXPECTED[leg_id], "cap_alloc": 80})
    host = host_module.C1SizingHostReference(
        lifecycle_state_path=tmp_path / "missing-lifecycle.json",
        dd_state_path=tmp_path / "missing-dd.json",
        constants_path=tmp_path / "missing-constants.json")
    decision = host.process_signal(
        {"leg_id": leg_id, "signal_type": signal_type, "bar_time": 1,
         "close": 100, "stop_dist_pts": 10}, current_equity=100000)
    assert decision.halt and not decision.submit and decision.qty_out == 0
    assert decision.halt_reason == "book_requires_session_policy_and_account_owner"
