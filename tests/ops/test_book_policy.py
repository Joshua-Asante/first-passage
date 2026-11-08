"""Exact protection and sizing rules of the accepted Tradeify book (Track B).

Owner of the values: docs/notes/2026-09-10-tradeify-protection-selection.md and the
Track B umbrella (TB-S1 (A)-(F), D-B7/D-B8/D-B10/D-B11/D-B14). Every number below
is derivable from those two sources; nothing here reads or edits the frozen
core/dd_protection.py constants or lands a POLICY_REGISTRY row.
"""
from __future__ import annotations

from datetime import date

import pytest

from c1_rail.book_policy import (
    ACCOUNT_MICRO_CAP,
    BOOK_LEGS,
    BookProtectionClock,
    PolicyAbsent,
    ProtectedRule,
    candidate_book_protection_policy,
    frozen_surfaces_untouched,
    is_protected,
    leg,
    leg_quantities,
)
from c1_signal_daemon.book_protocol import Mode, Side

POLICY = candidate_book_protection_policy()


# ── governance ───────────────────────────────────────────────────────────

def test_candidate_policy_is_the_selected_instance_and_not_admitted():
    assert POLICY.trigger == 0.01 and POLICY.scale == 0.40
    assert POLICY.reference_mode == "trailing"
    assert "CANDIDATE" in POLICY.provenance and "D-B11" in POLICY.provenance
    pins = frozen_surfaces_untouched()
    assert pins == {"DD_TRIGGER": 0.015, "DD_SCALE": 0.40, "registry_empty": True}


def test_no_policy_halts_never_defaults():
    with pytest.raises(PolicyAbsent):
        is_protected(99_000.0, 100_000.0, None)
    with pytest.raises(PolicyAbsent):
        leg_quantities("aegis_6j", 8, mode=Mode.NORMAL, policy=None)
    with pytest.raises(PolicyAbsent):
        BookProtectionClock(None, 100_000.0, 100_000.0)


def test_fixed_book_legs_priority_and_sides():
    ids = [l.leg_id for l in BOOK_LEGS]
    assert ids == ["aegis_6j", "dj30_mym_p250", "vanguard_mgc", "orb_mnq_v7"]   # D-B8 order
    assert [l.priority for l in BOOK_LEGS] == [1, 2, 3, 4]
    assert leg("aegis_6j").entry_side is Side.SELL                              # D-B7
    assert all(leg(i).entry_side is Side.BUY for i in ids[1:])
    assert leg("aegis_6j").micro_equiv == 10 and leg("orb_mnq_v7").micro_equiv == 1
    assert leg("orb_mnq_v7").protected_rule is ProtectedRule.BASE_FIXED_ADDS_OFF
    assert ACCOUNT_MICRO_CAP == 80
    for retired in ("dj30_mym", "nas100_mnq"):
        with pytest.raises(KeyError):
            leg(retired)


# ── trigger ──────────────────────────────────────────────────────────────

@pytest.mark.parametrize("equity,peak,expected", [
    (99_000.0, 100_000.0, True),        # exactly 1.000000 %
    (99_000.5, 100_000.0, False),       # 0.999995 % -> rounds to 0.999995 < 0.01
    (98_999.99, 100_000.0, True),
    (100_000.0, 100_000.0, False),
    (101_000.0, 100_000.0, False),      # above peak: dd 0
    (99_000.0 + 4e-5, 100_000.0, True),  # 0.0099999996 -> round(.., 6) == 0.01 (ULP rule)
])
def test_trigger_formula_with_ulp_rounding(equity, peak, expected):
    assert is_protected(equity, peak, POLICY) is expected


# ── quantities (D-B10 floor, TB-S1 (C), D-B14 (a)) ──────────────────────

@pytest.mark.parametrize("leg_id,normal,tier,mode,expected", [
    ("aegis_6j", 8, "AUTHORIZED", Mode.NORMAL, (8, 0)),
    ("aegis_6j", 8, "AUTHORIZED", Mode.PROTECTED, (3, 0)),
    ("aegis_6j", 8, "WATCH-1", Mode.NORMAL, (4, 0)),
    ("aegis_6j", 8, "WATCH-1", Mode.PROTECTED, (1, 0)),
    ("aegis_6j", 8, "WATCH-2", Mode.NORMAL, (2, 0)),
    ("aegis_6j", 8, "WATCH-2", Mode.PROTECTED, (0, 0)),
    ("vanguard_mgc", 2, "AUTHORIZED", Mode.NORMAL, (2, 2)),
    ("vanguard_mgc", 2, "AUTHORIZED", Mode.PROTECTED, (0, 0)),       # D-B10 accepted consequence
    ("vanguard_mgc", 1, "AUTHORIZED", Mode.NORMAL, (1, 1)),
    ("vanguard_mgc", 1, "AUTHORIZED", Mode.PROTECTED, (0, 0)),
    ("vanguard_mgc", 2, "WATCH-1", Mode.NORMAL, (0, 0)),
    ("orb_mnq_v7", 1, "AUTHORIZED", Mode.NORMAL, (1, 1)),
    ("orb_mnq_v7", 1, "AUTHORIZED", Mode.PROTECTED, (1, 0)),         # base unchanged, adds off
    ("orb_mnq_v7", 1, "WATCH-1", Mode.NORMAL, (0, 0)),               # ladder retained (D-B14 (a))
])
def test_protected_and_lifecycle_integer_table(leg_id, normal, tier, mode, expected):
    assert leg_quantities(leg_id, normal, mode=mode, policy=POLICY, lifecycle_tier=tier) == expected


def test_normal_base_outside_the_ladder_refuses():
    with pytest.raises(ValueError):
        leg_quantities("dj30_mym_p250", 23, mode=Mode.NORMAL, policy=POLICY)


# ── timing (TB-S1 (B)) ──────────────────────────────────────────────────

def test_mode_from_prior_close_no_latch_and_peak_ratchet():
    clock = BookProtectionClock(POLICY, 100_000.0, 100_000.0)
    d1, d2, d3, d4, d5 = (date(2026, 9, 14 + i) for i in range(5))
    assert clock.mode_for(d1) is Mode.NORMAL
    assert clock.settle(d1, 99_000.0) is Mode.PROTECTED          # exactly 1 % -> next session protected
    with pytest.raises(ValueError):
        clock.mode_for(d1)                                       # intraday equity never changes today's mode
    assert clock.mode_for(d2) is Mode.PROTECTED
    assert clock.settle(d2, 99_500.0) is Mode.NORMAL             # no latch: back under the trigger
    assert clock.settle(d3, 101_000.0) is Mode.NORMAL and clock.peak == 101_000.0
    assert clock.settle(d4, 99_990.0) is Mode.PROTECTED          # (101000-99990)/101000 = 1.0 %
    with pytest.raises(ValueError):
        clock.settle(d4, 100_000.0)                              # settles must advance
    assert clock.snapshot()["mode_next"] == "protected"
    assert clock.mode_for(d5) is Mode.PROTECTED


def test_frozen_initial_state_is_required_and_honoured():
    with pytest.raises(ValueError):
        BookProtectionClock(POLICY, 100_500.0, 100_000.0)        # peak below equity
    snapshot = BookProtectionClock(POLICY, 100_500.0, 101_600.0)  # B7-style seed, already in drawdown
    assert snapshot.mode_for(date(2026, 10, 1)) is Mode.PROTECTED
