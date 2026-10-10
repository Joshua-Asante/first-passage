"""Exact protection / capacity / sizing rules of the accepted Tradeify book (Track B).

Owner of the values: docs/notes/2026-09-10-tradeify-protection-selection.md and the
Track B umbrella (TB-S1 (A)-(F), D-B7/D-B8/D-B10/D-B11/D-B14). Every number below
is derivable from those two sources; nothing here reads or edits the frozen
core/dd_protection.py constants or lands a POLICY_REGISTRY row.
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal
from fractions import Fraction

import pytest

from c1_rail import book_policy as bp
from c1_rail.book_policy import (
    ACCOUNT_MICRO_CAP,
    BOOK_LEGS,
    BookProtectionClock,
    CapacityError,
    CapacityLedger,
    PolicyAbsent,
    ProtectedRule,
    StrikerRiskInputs,
    add_quantity,
    candidate_book_protection_policy,
    entry_quantities,
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


def test_floor_is_exact_rational_not_float():
    for n in (5, 10, 15, 25, 35, 55, 65):
        assert scaled_quantity(n, mode=Mode.PROTECTED, policy=POLICY) == n * 2 // 5
    assert scaled_quantity(3, mode=Mode.PROTECTED, policy=POLICY, lifecycle_tier="WATCH-1") == 0
    with pytest.raises(ValueError):
        scaled_quantity(-1, mode=Mode.NORMAL, policy=POLICY)
    with pytest.raises(ValueError):
        leg_quantities("dj30_mym_p250", 23, mode=Mode.NORMAL, policy=POLICY)   # outside the ladder


def test_quantity_table_and_reachable_menu():
    samples = [StrikerRiskInputs(Fraction(i, 2), Fraction(1), 80)
               for i in range(1, 444, 2)]
    rows = quantity_table(POLICY, striker_inputs=samples)
    assert len(rows) == (1 + len(samples) + 2 + 1) * 3 * 2
    menu = reachable_quantity_menu(POLICY, striker_inputs=samples)
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
    assert led.confirmed["dj30_mym_p250"] == 5                  # broker truth kept even though refused
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


# ── P-S1 size vector (successor build card 2026-10-10 §2.3, rows Z1-Z6, Z8) ──
# Row names are read through ``bp`` inside each test so a base without them
# fails the row, never the module's collection (T00 card F7).

TIERS = ("AUTHORIZED", "WATCH-1", "WATCH-2", "RETIRED")
MODES = (Mode.NORMAL, Mode.PROTECTED)
IDENTITY_MAPPING = {
    "aegis_6j": {"base": 8, "adds": "UNCHANGED"},
    "dj30_mym_p250": {"risk_multiplier": "1/1", "cap_reserve_multiplier": "1/1", "adds": "UNCHANGED"},
    "vanguard_mgc": {"base_by_port": {"1": 1, "2": 2}, "adds": "UNCHANGED"},
    "orb_mnq_v7": {"base": 1, "adds": "UNCHANGED"},
}


def vector(**legs):
    """A validated vector: the identity mapping with the named legs replaced."""
    return bp.validate_size_vector({**IDENTITY_MAPPING, **legs})


def ladder(leg_id):
    """Every ladder input of a leg: Striker risk ratio 1..23 x allocation 0..80."""
    if leg_id == "dj30_mym_p250":
        return [dict(risk_dollars=r, per_contract_risk=1, cap_alloc=a)
                for r in range(1, 24) for a in range(81)]
    if leg_id == "vanguard_mgc":
        return [dict(normal_base=1), dict(normal_base=2)]
    return [{}]


def quantities(leg_id, size=None, **inputs):
    return {(mode, tier): entry_quantities(leg_id, mode=mode, policy=POLICY, lifecycle_tier=tier,
                                           size=size, **inputs)
            for mode in MODES for tier in TIERS}


def test_Z1_no_size_and_identity_vector_give_todays_quantities():
    identity = bp.IDENTITY_SIZE_VECTOR
    assert identity == bp.validate_size_vector(IDENTITY_MAPPING) and identity.is_identity
    for spec in BOOK_LEGS:
        size = identity.leg(spec.leg_id)
        for inputs in ladder(spec.leg_id):
            for mode in MODES:
                for tier in TIERS:
                    today = entry_quantities(spec.leg_id, mode=mode, policy=POLICY,
                                             lifecycle_tier=tier, **inputs)          # twin
                    assert entry_quantities(spec.leg_id, mode=mode, policy=POLICY, lifecycle_tier=tier,
                                            size=None, **inputs) == today
                    assert entry_quantities(spec.leg_id, mode=mode, policy=POLICY, lifecycle_tier=tier,
                                            size=size, **inputs) == today
        for base in range(max(spec.normal_base_values) + 1):
            for mode in MODES:
                for tier in TIERS:
                    today = add_quantity(spec.leg_id, base, mode=mode, policy=POLICY, lifecycle_tier=tier)
                    assert add_quantity(spec.leg_id, base, mode=mode, policy=POLICY,
                                        lifecycle_tier=tier, size=size) == today
    # The pinned integer table is unchanged under the identity vector.
    assert entry_quantities("aegis_6j", mode=Mode.PROTECTED, policy=POLICY, lifecycle_tier="AUTHORIZED",
                            size=identity.leg("aegis_6j")) == (3, 0)


def test_Z2_aegis_base():
    for b in range(9):
        got = quantities("aegis_6j", size=vector(aegis_6j={"base": b, "adds": "UNCHANGED"}).leg("aegis_6j"))
        assert got[(Mode.NORMAL, "AUTHORIZED")] == (b, 0)
        assert got[(Mode.PROTECTED, "AUTHORIZED")] == (b * 2 // 5, 0)
        assert got[(Mode.NORMAL, "WATCH-1")] == (b // 2, 0)
        assert got[(Mode.PROTECTED, "RETIRED")] == (0, 0)
    assert quantities("aegis_6j", size=vector().leg("aegis_6j")) == quantities("aegis_6j")   # twin: b = 8


def test_Z3_striker_multipliers_max_base_and_cap_term_exact():
    cases = [("1/2", "1/1", None), ("1/3", "1/2", None), ("3/5", "2/7", 3), ("1/1", "1/2", 7),
             ("0/1", "0/1", None)]
    risks = [(Fraction(700), Fraction(35)), (Fraction(125), Fraction(10)), (Decimal("124.9"), Decimal("10")),
             (Fraction(7, 3), Fraction(1, 3)), (Fraction(10**6), Fraction(1))]
    for m, c, cap in cases:
        size = bp.LegSize("dj30_mym_p250", risk_multiplier=m, cap_reserve_multiplier=c, max_base=cap)
        for risk, pcr in risks:
            for alloc in (0, 7, 40, 80):
                got = quantities("dj30_mym_p250", size=size, risk_dollars=risk,
                                 per_contract_risk=pcr, cap_alloc=alloc)
                for (mode, tier), (base, add) in got.items():
                    scale = Fraction(2, 5) if mode is Mode.PROTECTED else Fraction(1)
                    life = Fraction(str(bp.TIER_MULTIPLIER[tier]))
                    terms = [Fraction(risk) * scale * life * Fraction(m) / Fraction(pcr) // 1,
                             Fraction(alloc) * Fraction(c) / Fraction(7, 2) // 1]
                    assert base == min(terms + ([cap] if cap is not None else []))
                    assert add == (base * 5 // 2 if tier != "RETIRED" else 0)
    half = bp.LegSize("dj30_mym_p250", risk_multiplier="1/2", cap_reserve_multiplier="1/2")

    def eq(**kw):
        return entry_quantities("dj30_mym_p250", policy=POLICY, lifecycle_tier="AUTHORIZED", size=half, **kw)
    assert eq(mode=Mode.NORMAL, risk_dollars=700, per_contract_risk=35, cap_alloc=80) == (10, 25)
    assert eq(mode=Mode.NORMAL, risk_dollars=700, per_contract_risk=4, cap_alloc=80) == (11, 27)  # cap term
    assert eq(mode=Mode.PROTECTED, risk_dollars=125, per_contract_risk=10, cap_alloc=80) == (2, 5)
    assert entry_quantities("dj30_mym_p250", mode=Mode.NORMAL, policy=POLICY, lifecycle_tier="AUTHORIZED",
                            risk_dollars=700, per_contract_risk=35, cap_alloc=80) == (20, 50)   # twin


def test_Z4_vanguard_base_by_port():
    one = vector(vanguard_mgc={"base_by_port": {"1": 1, "2": 1}, "adds": "UNCHANGED"}).leg("vanguard_mgc")
    off_low = vector(vanguard_mgc={"base_by_port": {"1": 0, "2": 2}, "adds": "UNCHANGED"}).leg("vanguard_mgc")

    def q(size, nb, mode=Mode.NORMAL, tier="AUTHORIZED"):
        return entry_quantities("vanguard_mgc", normal_base=nb, mode=mode, policy=POLICY,
                                lifecycle_tier=tier, size=size)
    assert (q(one, 2), q(one, 1), q(one, 2, Mode.PROTECTED), q(one, 2, tier="WATCH-1")) == (
        (1, 1), (1, 1), (0, 0), (0, 0))
    assert (q(off_low, 1), q(off_low, 2)) == ((0, 0), (2, 2))
    assert (q(None, 1), q(None, 2)) == ((1, 1), (2, 2))                                           # twin
    with pytest.raises(ValueError):
        q(one, 3)


def test_Z5_orb_base_zero_and_one_unscaled_when_protected():
    for b, normal, protected in ((0, (0, 0), (0, 0)), (1, (1, 1), (1, 0))):
        got = quantities("orb_mnq_v7", size=vector(orb_mnq_v7={"base": b, "adds": "UNCHANGED"}).leg("orb_mnq_v7"))
        assert got[(Mode.NORMAL, "AUTHORIZED")] == normal
        assert got[(Mode.PROTECTED, "AUTHORIZED")] == protected
        assert got[(Mode.NORMAL, "WATCH-1")] == (0, 0)
    assert quantities("orb_mnq_v7") == quantities("orb_mnq_v7", size=vector().leg("orb_mnq_v7"))   # twin


@pytest.mark.parametrize("leg_id,base,rule,normal,protected", [
    ("dj30_mym_p250", 10, "UNCHANGED", 25, 25),
    ("dj30_mym_p250", 10, "OFF_WHEN_PROTECTED", 25, 0),
    ("dj30_mym_p250", 10, "OFF", 0, 0),
    ("vanguard_mgc", 2, "UNCHANGED", 2, 0),
    ("vanguard_mgc", 2, "OFF", 0, 0),
    ("orb_mnq_v7", 1, "UNCHANGED", 1, 0),
    ("orb_mnq_v7", 1, "OFF", 0, 0),
    ("aegis_6j", 8, "UNCHANGED", 0, 0),
])
def test_Z6_adds_rule_against_add_quantity(leg_id, base, rule, normal, protected):
    fields = {k: v for k, v in IDENTITY_MAPPING[leg_id].items() if k != "adds"}
    size = vector(**{leg_id: {**fields, "adds": rule}}).leg(leg_id)

    def add(mode, s, tier="AUTHORIZED"):
        return add_quantity(leg_id, base, mode=mode, policy=POLICY, lifecycle_tier=tier, size=s)
    assert (add(Mode.NORMAL, size), add(Mode.PROTECTED, size)) == (normal, protected)
    assert add(Mode.NORMAL, None) == add_quantity(leg_id, base, mode=Mode.NORMAL, policy=POLICY,
                                                  lifecycle_tier="AUTHORIZED")                  # twin
    assert add(Mode.NORMAL, size, "WATCH-1") == (25 if (leg_id, rule) == ("dj30_mym_p250", "UNCHANGED")
                                                 or (leg_id, rule) == ("dj30_mym_p250", "OFF_WHEN_PROTECTED")
                                                 else 0)


def _with(leg_id, **fields):
    return {**IDENTITY_MAPPING, leg_id: {**IDENTITY_MAPPING[leg_id], **fields}}


def _without(leg_id, field_name):
    return {**IDENTITY_MAPPING, leg_id: {k: v for k, v in IDENTITY_MAPPING[leg_id].items() if k != field_name}}


Z8_REFUSALS = {
    "not_a_mapping": lambda: [("aegis_6j", {})],
    "missing_leg": lambda: {k: v for k, v in IDENTITY_MAPPING.items() if k != "orb_mnq_v7"},
    "unknown_leg": lambda: {**IDENTITY_MAPPING, "dj30_mym": {"base": 1, "adds": "UNCHANGED"}},
    "retired_leg_replaces": lambda: {**{k: v for k, v in IDENTITY_MAPPING.items() if k != "orb_mnq_v7"},
                                     "nas100_mnq": {"base": 1, "adds": "UNCHANGED"}},
    "leg_not_mapping": lambda: {**IDENTITY_MAPPING, "orb_mnq_v7": 1},
    "extra_field": lambda: _with("aegis_6j", note="x"),
    "missing_field": lambda: _without("orb_mnq_v7", "adds"),
    "missing_multiplier": lambda: _without("dj30_mym_p250", "cap_reserve_multiplier"),
    "foreign_field": lambda: _with("aegis_6j", max_base=1),
    "string_int": lambda: _with("aegis_6j", base="8"),
    "float_int": lambda: _with("aegis_6j", base=8.0),
    "bool_int": lambda: _with("orb_mnq_v7", base=True),
    "aegis_above_today": lambda: _with("aegis_6j", base=9),
    "orb_above_today": lambda: _with("orb_mnq_v7", base=2),
    "vanguard_above_today": lambda: _with("vanguard_mgc", base_by_port={"1": 2, "2": 2}),
    "vanguard_port_extra": lambda: _with("vanguard_mgc", base_by_port={"1": 1, "2": 2, "3": 1}),
    "vanguard_port_float": lambda: _with("vanguard_mgc", base_by_port={"1": 1, "2": 1.0}),
    "max_base_above_today": lambda: _with("dj30_mym_p250", max_base=23),
    "max_base_float": lambda: _with("dj30_mym_p250", max_base=5.0),
    "negative_base": lambda: _with("aegis_6j", base=-1),
    "negative_max_base": lambda: _with("dj30_mym_p250", max_base=-1),
    "multiplier_above_one": lambda: _with("dj30_mym_p250", risk_multiplier="3/2"),
    "multiplier_negative": lambda: _with("dj30_mym_p250", cap_reserve_multiplier="-1/2"),
    "multiplier_float": lambda: _with("dj30_mym_p250", risk_multiplier=0.5),
    "multiplier_decimal_text": lambda: _with("dj30_mym_p250", risk_multiplier="0.5"),
    "multiplier_bare_int": lambda: _with("dj30_mym_p250", risk_multiplier="1"),
    "multiplier_padded": lambda: _with("dj30_mym_p250", risk_multiplier=" 1/2"),
    "multiplier_zero_denominator": lambda: _with("dj30_mym_p250", risk_multiplier="1/0"),
    "unknown_adds": lambda: _with("orb_mnq_v7", adds="ON"),
    # S-5 canonical encoding: one vector, one encoding.
    "unreduced_fraction": lambda: _with("dj30_mym_p250", risk_multiplier="2/4"),
    "unreduced_one": lambda: _with("dj30_mym_p250", cap_reserve_multiplier="2/2"),
    "leading_zero": lambda: _with("dj30_mym_p250", risk_multiplier="01/2"),
    "aegis_adds_not_unchanged": lambda: _with("aegis_6j", adds="OFF"),
    "vanguard_off_when_protected": lambda: _with("vanguard_mgc", adds="OFF_WHEN_PROTECTED"),
    "orb_off_when_protected": lambda: _with("orb_mnq_v7", adds="OFF_WHEN_PROTECTED"),
    "max_base_22": lambda: _with("dj30_mym_p250", max_base=22),
    "max_base_at_cap_term": lambda: _with("dj30_mym_p250", cap_reserve_multiplier="1/2", max_base=11),
    "max_base_none": lambda: _with("dj30_mym_p250", max_base=None),
    "off_leg_adds_rule": lambda: _with("orb_mnq_v7", base=0, adds="OFF"),
    "off_vanguard_adds_rule": lambda: _with("vanguard_mgc", base_by_port={"1": 0, "2": 0}, adds="OFF"),
    "striker_off_by_risk_only": lambda: _with("dj30_mym_p250", risk_multiplier="0/1"),
    "striker_off_by_cap_only": lambda: _with("dj30_mym_p250", cap_reserve_multiplier="0/1"),
    "striker_off_by_max_base": lambda: _with("dj30_mym_p250", max_base=0),
    "striker_off_with_adds_rule": lambda: _with("dj30_mym_p250", risk_multiplier="0/1",
                                                cap_reserve_multiplier="0/1", adds="OFF"),
}


@pytest.mark.parametrize("case", sorted(Z8_REFUSALS))
def test_Z8_validate_size_vector_refusals(case):
    with pytest.raises(ValueError):
        bp.validate_size_vector(Z8_REFUSALS[case]())


def test_Z8_canonical_twins_and_is_identity_over_the_quantity_table():
    accepted = [_with("dj30_mym_p250", cap_reserve_multiplier="1/2", max_base=10),       # twins of refusals
                _with("dj30_mym_p250", max_base=21),
                _with("dj30_mym_p250", risk_multiplier="0/1", cap_reserve_multiplier="0/1"),
                _with("orb_mnq_v7", base=0), _with("orb_mnq_v7", adds="OFF"),
                _with("vanguard_mgc", adds="OFF"), _with("dj30_mym_p250", adds="OFF_WHEN_PROTECTED")]
    for mapping in accepted:
        validated = bp.validate_size_vector(mapping)
        assert not validated.is_identity
        assert validated.as_mapping() == mapping                                            # round trip
    assert bp.validate_size_vector(IDENTITY_MAPPING).as_mapping() == IDENTITY_MAPPING
    legs = {spec.leg_id: bp.IDENTITY_SIZE_VECTOR.leg(spec.leg_id) for spec in BOOK_LEGS}

    def direct(**replaced):
        merged = {**legs, **replaced}
        return bp.SizeVector(tuple(merged[s.leg_id] for s in BOOK_LEGS))
    # Non-canonical encodings that still give today's quantities.
    assert direct(dj30_mym_p250=bp.LegSize("dj30_mym_p250", risk_multiplier="2/2",
                                           cap_reserve_multiplier="3/3", max_base=22)).is_identity
    assert direct(aegis_6j=bp.LegSize("aegis_6j", base=8, adds=bp.AddsRule.OFF)).is_identity
    assert direct(orb_mnq_v7=bp.LegSize("orb_mnq_v7", base=1, adds=bp.AddsRule.OFF_WHEN_PROTECTED)).is_identity
    assert not direct(dj30_mym_p250=bp.LegSize("dj30_mym_p250", risk_multiplier="1/1",
                                               cap_reserve_multiplier="1/1", max_base=21)).is_identity  # twin
    for m, c in (("99/100", "1/1"), ("1/1", "79/80")):         # each multiplier alone, just below one
        assert not direct(dj30_mym_p250=bp.LegSize("dj30_mym_p250", risk_multiplier=m,
                                                   cap_reserve_multiplier=c)).is_identity
    with pytest.raises(ValueError):
        bp.LegSize("aegis_6j", base=9)                         # direct construction can only lower too
    with pytest.raises(ValueError):
        bp.LegSize("dj30_mym_p250", risk_multiplier="3/2", cap_reserve_multiplier="1/1")
    with pytest.raises(ValueError):
        bp.SizeVector(tuple(legs[s.leg_id] for s in reversed(BOOK_LEGS)))
    with pytest.raises(ValueError):
        entry_quantities("orb_mnq_v7", mode=Mode.NORMAL, policy=POLICY, lifecycle_tier="AUTHORIZED",
                         size=legs["aegis_6j"])                # a leg's size is never another leg's
