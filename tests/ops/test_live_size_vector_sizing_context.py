"""P-L1: the binding's per-leg LegSize reaches both shared quantity laws (card §4 LS1-LS7).

Synthetic sizes only, chosen off the k=0.5 floor-half rule; no screened vector value appears here.
"""
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from fractions import Fraction

import pytest

from c1_rail.book_policy import (
    BOOK_LEGS, TIER_MULTIPLIER, AddsRule, LegSize, _identity_ladder, add_quantity,
    candidate_book_protection_policy, entry_quantities, leg, validate_size_vector,
)
from c1_rail.book_sizing_context import (
    BookAccountContext, BookExposure, BookSession, BookSizingBinding,
    BookSizingRequest, SettledClose, size_book_request,
)
from c1_signal_daemon.book_protocol import Mode

NOW = datetime(2026, 9, 14, 15, tzinfo=timezone.utc)
POLICY = candidate_book_protection_policy()
LEGS = [spec.leg_id for spec in BOOK_LEGS]
MODES = (Mode.NORMAL, Mode.PROTECTED)
SYNTHETIC = validate_size_vector({
    "aegis_6j": {"base": 3, "adds": "UNCHANGED"},
    "dj30_mym_p250": {"risk_multiplier": "1/3", "cap_reserve_multiplier": "1/1", "adds": "UNCHANGED"},
    "vanguard_mgc": {"base_by_port": {"1": 1, "2": 0}, "adds": "UNCHANGED"},
    "orb_mnq_v7": {"base": 1, "adds": "OFF"},
})


def case(leg_id, *, size, mode=Mode.NORMAL, tier="AUTHORIZED", kind="entry", inputs=None,
         base=0, cap_alloc=80):
    inputs = inputs or {}
    spec = leg(leg_id)
    session = BookSession("session-2", "session-1", NOW - timedelta(hours=1),
                          NOW + timedelta(hours=1), NOW + timedelta(hours=2), "a" * 64)
    settled = SettledClose("session-1", NOW - timedelta(days=1),
                           99000 if mode is Mode.PROTECTED else 100000, 100000, "d" * 64)
    binding = BookSizingBinding("synthetic-account", "boot-2", "b" * 64, "c" * 64, settled,
                                session, timedelta(seconds=30), leg_id, "SYNTHETIC-" + spec.symbol,
                                inputs.get("cap_alloc", cap_alloc),
                                Fraction(inputs.get("risk_dollars", 700)), size=size)
    exposures = tuple(BookExposure(item.leg_id, base if item.leg_id == leg_id else 0, 0)
                      for item in BOOK_LEGS)
    context = BookAccountContext(
        "synthetic-account", "boot-2", "op-2", leg_id, binding.order_symbol, "session-2", mode,
        "b" * 64, "c" * 64, "a" * 64, settled, spec.lifecycle_key, tier,
        NOW, NOW + timedelta(seconds=30), base, base, "base-1" if kind == "add" else None,
        exposures, (), ())
    request = BookSizingRequest("op-2", leg_id, binding.order_symbol, kind,
                                inputs.get("normal_base"),
                                Fraction(inputs.get("per_contract_risk", 10)))
    return request, context, binding


def decide(request, context, binding):
    return size_book_request(request, context=context, binding=binding, policy=POLICY, now=NOW)


def expected_entry(request, context, binding, size):
    return entry_quantities(request.leg_id, mode=context.mode, policy=POLICY,
                            lifecycle_tier=context.lifecycle_tier, normal_base=request.normal_base,
                            risk_dollars=binding.risk_dollars,
                            per_contract_risk=request.per_contract_risk,
                            cap_alloc=binding.cap_alloc, size=size)


def entry_outcomes(leg_id, size):
    for tier in TIER_MULTIPLIER:
        for mode in MODES:
            for inputs in _identity_ladder(leg_id):
                request, context, binding = case(leg_id, size=size, mode=mode, tier=tier, inputs=inputs)
                yield (tier, mode, tuple(sorted(inputs.items()))), decide(request, context, binding), \
                    expected_entry(request, context, binding, size)


@pytest.mark.parametrize("leg_id", LEGS)
def test_ls1_explicit_none_is_todays_entry_and_add(leg_id):
    for _, decision, expected in entry_outcomes(leg_id, None):
        assert not decision.halt and decision.halt_reason is None
        assert (decision.qty_out, decision.prospective_add) == expected
    for tier in TIER_MULTIPLIER:
        for mode in MODES:
            for base in range(1, max(leg(leg_id).normal_base_values) + 1):
                decision = decide(*case(leg_id, size=None, mode=mode, tier=tier, kind="add", base=base))
                assert not decision.halt and decision.prospective_add == 0
                assert decision.qty_out == add_quantity(leg_id, base, mode=mode, policy=POLICY,
                                                        lifecycle_tier=tier)


@pytest.mark.parametrize("leg_id", LEGS)
def test_ls2_size_reaches_entry_law(leg_id):
    size = SYNTHETIC.leg(leg_id)
    unsized = {key: (d.qty_out, d.prospective_add) for key, d, _ in entry_outcomes(leg_id, None)}
    differs = False
    for key, decision, expected in entry_outcomes(leg_id, size):
        assert not decision.halt and (decision.qty_out, decision.prospective_add) == expected
        differs |= expected != unsized[key]
    assert differs, f"{leg_id}: synthetic size never changes an entry quantity"


@pytest.mark.parametrize("mode", MODES)
def test_ls3_size_reaches_add_law(mode):
    unchanged = SYNTHETIC.leg("dj30_mym_p250")
    off = replace(unchanged, adds=AddsRule.OFF)
    for base in (1, 3, 22):
        refused = decide(*case("dj30_mym_p250", size=off, mode=mode, kind="add", base=base))
        assert not refused.halt and refused.qty_out == 0
        sized = decide(*case("dj30_mym_p250", size=unchanged, mode=mode, kind="add", base=base))
        assert not sized.halt and sized.qty_out == add_quantity(
            "dj30_mym_p250", base, mode=mode, policy=POLICY, lifecycle_tier="AUTHORIZED",
            size=unchanged) > 0


@pytest.mark.parametrize("mode", MODES)
def test_ls4_leg_at_zero_sizes_zero_without_halt(mode):
    decision = decide(*case("aegis_6j", size=LegSize("aegis_6j", base=0), mode=mode))
    assert not decision.halt and (decision.qty_out, decision.prospective_add) == (0, 0)


def test_ls5_other_legs_size_halts():
    decision = decide(*case("dj30_mym_p250", size=SYNTHETIC.leg("aegis_6j")))
    assert decision.halt and decision.halt_reason == "size_binding_mismatch"
    assert decision.qty_out == 0


def test_ls6_untyped_size_halts():
    decision = decide(*case("aegis_6j", size={"base": 3, "adds": "UNCHANGED"}))
    assert decision.halt and decision.halt_reason == "size_binding_mismatch"
    assert decision.qty_out == 0


def test_ls7_capacity_checks_the_sized_quantity():
    cap = 3 * leg("aegis_6j").micro_equiv
    refused = decide(*case("aegis_6j", size=None, cap_alloc=cap))
    assert refused.halt and refused.halt_reason == "leg_allocation_refusal"
    sized = decide(*case("aegis_6j", size=SYNTHETIC.leg("aegis_6j"), cap_alloc=cap))
    assert not sized.halt and sized.qty_out == 3 and sized.requested_micro == cap
