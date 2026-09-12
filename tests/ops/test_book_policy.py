"""Exact protection / capacity / sizing rules of the accepted Tradeify book (Track B).

Owner of the values: docs/notes/2026-09-10-tradeify-protection-selection.md and the
Track B umbrella (TB-S1 (A)-(F), D-B7/D-B8/D-B10/D-B11/D-B14). Every number below
is derivable from those two sources; nothing here reads or edits the frozen
core/dd_protection.py constants or lands a POLICY_REGISTRY row.
"""
from __future__ import annotations

from datetime import date

import pytest

from book_policy import (
    ACCOUNT_MICRO_CAP,
    BOOK_LEGS,
    BookProtectionClock,
    CapacityError,
    CapacityLedger,
    PolicyAbsent,
    ProtectedRule,
    candidate_book_protection_policy,
    frozen_surfaces_untouched,
    is_protected,
    leg,
    leg_quantities,
    quantity_table,
    reachable_quantity_menu,
    scaled_quantity,
    transition_cancels,
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
        scaled_quantity(8, mode=Mode.PROTECTED, policy=None)
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
    ("dj30_mym_p250", 22, "AUTHORIZED", Mode.NORMAL, (22, 55)),
    ("dj30_mym_p250", 22, "AUTHORIZED", Mode.PROTECTED, (8, 22)),   # every tier floored from its own normal
    ("dj30_mym_p250", 22, "WATCH-1", Mode.NORMAL, (11, 27)),
    ("dj30_mym_p250", 5, "AUTHORIZED", Mode.PROTECTED, (2, 4)),      # 5 x 0.4 = 2 exactly (no binary64 floor slip)
    ("vanguard_mgc", 2, "AUTHORIZED", Mode.NORMAL, (2, 2)),
    ("vanguard_mgc", 2, "AUTHORIZED", Mode.PROTECTED, (0, 0)),       # D-B10 accepted consequence
    ("vanguard_mgc", 1, "AUTHORIZED", Mode.NORMAL, (1, 1)),
    ("vanguard_mgc", 1, "AUTHORIZED", Mode.PROTECTED, (0, 0)),
    ("vanguard_mgc", 2, "WATCH-1", Mode.NORMAL, (1, 1)),
    ("orb_mnq_v7", 1, "AUTHORIZED", Mode.NORMAL, (1, 1)),
    ("orb_mnq_v7", 1, "AUTHORIZED", Mode.PROTECTED, (1, 0)),         # base unchanged, adds off
    ("orb_mnq_v7", 1, "WATCH-1", Mode.NORMAL, (0, 0)),               # ladder retained (D-B14 (a))
])
def test_protected_and_lifecycle_integer_table(leg_id, normal, tier, mode, expected):
    assert leg_quantities(leg_id, normal, mode=mode, policy=POLICY, lifecycle_tier=tier) == expected


def test_floor_is_exact_rational_not_float():
    for n in (5, 10, 15, 25, 35, 55, 65):
        assert scaled_quantity(n, mode=Mode.PROTECTED, policy=POLICY) == n * 2 // 5
    assert scaled_quantity(3, mode=Mode.PROTECTED, policy=POLICY, lifecycle_tier="WATCH-1") == 0
    with pytest.raises(ValueError):
        scaled_quantity(-1, mode=Mode.NORMAL, policy=POLICY)
    with pytest.raises(ValueError):
        leg_quantities("dj30_mym_p250", 23, mode=Mode.NORMAL, policy=POLICY)   # outside the ladder


def test_quantity_table_and_reachable_menu():
    rows = quantity_table(POLICY)
    assert len(rows) == (1 + 22 + 2 + 1) * 3 * 2
    menu = reachable_quantity_menu(POLICY)
    assert menu["aegis_6j"]["base"] == {8, 3, 4, 1, 2}
    assert menu["aegis_6j"]["add"] == set()
    assert menu["orb_mnq_v7"] == {"base": {1}, "add": {1}}
    assert menu["vanguard_mgc"]["base"] == {2, 1}
    assert max(menu["dj30_mym_p250"]["base"]) == 22 and max(menu["dj30_mym_p250"]["add"]) == 55
    assert leg("orb_mnq_v7").protected_rule is ProtectedRule.BASE_FIXED_ADDS_OFF


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


# ── carried positions (TB-S1 (D)) ────────────────────────────────────────

def test_transition_cancels_only_resting_orb_adds_on_activation():
    assert transition_cancels(Mode.NORMAL, Mode.PROTECTED, ["orb:add:1", "orb:add:2"]) == ["orb:add:1", "orb:add:2"]
    assert transition_cancels(Mode.PROTECTED, Mode.NORMAL, ["orb:add:1"]) == []
    assert transition_cancels(Mode.PROTECTED, Mode.PROTECTED, ["orb:add:1"]) == []


# ── capacity (TB-S1 (E), D-B8) ───────────────────────────────────────────

def test_reservation_accounting_refuses_not_clips():
    led = CapacityLedger()
    assert led.request("dj30_mym_p250", 77).admitted
    assert led.request("orb_mnq_v7", 3).admitted and led.micro_used() == 80
    d = led.request("vanguard_mgc", 1)
    assert not d.admitted and d.takeover is None and "refused" in d.reason
    assert led.reserved.get("vanguard_mgc", 0) == 0
    led.confirm_fill("dj30_mym_p250", 77)
    assert led.confirmed["dj30_mym_p250"] == 77 and led.reserved["dj30_mym_p250"] == 0
    with pytest.raises(CapacityError):
        led.confirm_fill("dj30_mym_p250", 1)                    # nothing reserved


def test_aegis_takeover_atomic_lowest_priority_first_and_admits_only_on_confirmations():
    led = CapacityLedger()
    led.request("dj30_mym_p250", 77); led.confirm_fill("dj30_mym_p250", 77)
    led.request("orb_mnq_v7", 3); led.confirm_fill("orb_mnq_v7", 3)
    d = led.request("aegis_6j", 3)                              # 30 micro-equivalents
    assert not d.admitted and d.takeover is not None
    assert d.takeover.displaced == ("orb_mnq_v7", "dj30_mym_p250")   # lowest first; Vanguard holds nothing
    t = led.begin_takeover(d.takeover)
    assert not led.request("vanguard_mgc", 1).admitted          # nothing admitted while a takeover is pending
    with pytest.raises(CapacityError):
        t.confirm_close("vanguard_mgc", 0)                      # not a displaced leg
    t.ack_cancel("orb_mnq_v7"); t.confirm_close("orb_mnq_v7", 0)
    t.ack_cancel("dj30_mym_p250"); t.confirm_close("dj30_mym_p250", 0)
    assert t.complete()
    res = led.settle_takeover()
    assert res.admitted and led.reserved["aegis_6j"] == 3
    assert led.confirmed.get("dj30_mym_p250", 0) == 0 and led.confirmed.get("orb_mnq_v7", 0) == 0
    kinds = [e["kind"] for e in led.events]
    assert "capacity_takeover_admitted" in kinds and "capacity_takeover_close_confirmed" in kinds


def test_takeover_fails_closed_on_partial_close_or_missing_ack():
    led = CapacityLedger()
    led.request("dj30_mym_p250", 60); led.confirm_fill("dj30_mym_p250", 60)
    led.request("orb_mnq_v7", 3); led.confirm_fill("orb_mnq_v7", 3)
    d = led.request("aegis_6j", 3)
    t = led.begin_takeover(d.takeover)
    t.ack_cancel("orb_mnq_v7"); t.confirm_close("orb_mnq_v7", 0)
    t.ack_cancel("dj30_mym_p250"); t.confirm_close("dj30_mym_p250", 5)   # partial: 5 still open
    assert t.state == "refused"
    res = led.settle_takeover()
    assert not res.admitted and led.reserved.get("aegis_6j", 0) == 0
    assert led.confirmed["dj30_mym_p250"] == 60                 # ledger untouched until confirmed flat
    assert any(e["kind"] == "capacity_takeover_refused" for e in led.events)

    led2 = CapacityLedger()
    led2.request("orb_mnq_v7", 80); led2.confirm_fill("orb_mnq_v7", 80)
    d2 = led2.request("aegis_6j", 1)
    t2 = led2.begin_takeover(d2.takeover)
    t2.confirm_close("orb_mnq_v7", 0)                            # close reported before the cancel ack
    assert t2.state == "refused"
    assert not led2.settle_takeover().admitted

    led3 = CapacityLedger()
    led3.request("orb_mnq_v7", 75); led3.confirm_fill("orb_mnq_v7", 75)
    d3 = led3.request("aegis_6j", 1)                            # 85 > 80 -> takeover planned
    assert d3.takeover is not None
    led3.begin_takeover(d3.takeover)
    assert not led3.settle_takeover().admitted                   # settle before confirmations -> refused


def test_only_the_top_priority_leg_may_displace_and_cap_can_be_unreachable():
    led = CapacityLedger()
    led.request("aegis_6j", 8); led.confirm_fill("aegis_6j", 8)   # 80 micro
    assert not led.request("dj30_mym_p250", 1).admitted           # Striker never displaces Aegis
    d = led.request("aegis_6j", 1)
    assert not d.admitted and d.takeover is None                  # nothing lower-priority to displace
    led2 = CapacityLedger()
    led2.request("orb_mnq_v7", 5); led2.confirm_fill("orb_mnq_v7", 5)
    d2 = led2.request("aegis_6j", 9)                              # 90 > 80 even when flat
    assert not d2.admitted and d2.takeover is None and "unreachable" in d2.reason


def test_broker_truth_reconciliation():
    led = CapacityLedger()
    led.request("vanguard_mgc", 2)
    led.release_reservation("vanguard_mgc", 1)
    assert led.reserved["vanguard_mgc"] == 1
    led.confirm_fill("vanguard_mgc", 1)
    led.confirm_position("vanguard_mgc", 0)                       # broker-confirmed flat
    assert led.micro_used() == 0
    with pytest.raises(CapacityError):
        led.confirm_position("vanguard_mgc", -1)
