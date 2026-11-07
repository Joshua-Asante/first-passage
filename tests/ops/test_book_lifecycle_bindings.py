"""Fixed-book lifecycle keys, and their separation from the historical call-4 keys."""
import json

import lifecycle
from c1_rail.book_policy import BOOK_LEGS


EXPECTED = {
    "aegis_6j": "Aegis 6J",
    "dj30_mym_p250": "Striker MYM p250",
    "vanguard_mgc": "Vanguard MGC",
    "orb_mnq_v7": "ORB MNQ v7",
}


def test_book_lifecycle_keys_match_policy():
    assert {spec.leg_id: spec.lifecycle_key for spec in BOOK_LEGS} == EXPECTED
    assert set(EXPECTED.values()) == lifecycle.BOOK_STRATEGY_KEYS


def test_lifecycle_loader_accepts_explicit_book_states(tmp_path, monkeypatch):
    state_file = tmp_path / "lifecycle.json"
    state = dict(zip(EXPECTED.values(), lifecycle.TIER_MULTIPLIER))
    state_file.write_text(json.dumps(state), encoding="utf-8")
    monkeypatch.setattr(lifecycle, "STATE_FILE", state_file)
    assert lifecycle.load_lifecycle_state() == state


def test_book_demotions_do_not_change_historical_call4(tmp_path, monkeypatch):
    state_file = tmp_path / "lifecycle.json"
    state_file.write_text(json.dumps(dict.fromkeys(EXPECTED.values(), "RETIRED")),
                          encoding="utf-8")
    monkeypatch.setattr(lifecycle, "STATE_FILE", state_file)
    assert lifecycle.get_effective_multipliers(lifecycle.STRATEGY_KEYS) == {
        "Guardian": 1.0, "Striker": 1.0, "Aegis": 1.0, "Striker NAS100": 1.0}
