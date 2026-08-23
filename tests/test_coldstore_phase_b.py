"""Phase B axis-separation: catalog disposition is not a lifecycle write."""

from pathlib import Path

import dd_protection
from lifecycle import (
    STATE_FILE,
    STRATEGY_KEYS,
    TIER_MULTIPLIER,
    get_lifecycle_multipliers,
    load_lifecycle_state,
)

ADR = Path(__file__).resolve().parents[1] / "docs" / "adr" / "2026-08-23-strategy-coldstore-phase-b.md"


def test_b_does_not_mutate_protection_or_ladder_pins():
    assert dd_protection.DD_TRIGGER == 0.015
    assert dd_protection.DD_SCALE == 0.40
    assert TIER_MULTIPLIER == {
        "AUTHORIZED": 1.00,
        "WATCH-1": 0.50,
        "WATCH-2": 0.25,
        "RETIRED": 0.00,
    }


def test_striker_stays_authorized_by_default():
    assert load_lifecycle_state() == {}
    assert not STATE_FILE.exists()
    mult = get_lifecycle_multipliers(STRATEGY_KEYS)
    assert mult["Striker"] == 1.0
    assert mult["Striker NAS100"] == 1.0
    assert set(STRATEGY_KEYS) == {
        "Guardian",
        "Striker",
        "Aegis",
        "Striker NAS100",
    }


def test_disposition_table_none_for_venue_withdrawn():
    text = ADR.read_text(encoding="utf-8")
    assert "VENUE_WITHDRAWN" in text
    assert "**none** — Tradeify de-scope is edition-level" in text
    assert "lifecycle_state.json" in text
