"""Card A P4/P8: explicit personal identity and resolved capacity; synthetic only."""
from dataclasses import replace
from datetime import datetime, timedelta, timezone

import pytest

from c1_rail import book_policy as bp
from c1_rail import book_capacity as capacity
from c1_signal_daemon.book_protocol import Mode


def personal():
    assert hasattr(bp, "PersonalP0Policy"), "P0 policy is not implemented"
    return bp.PersonalP0Policy()


def test_p0_is_distinct_and_cannot_enter_tradeify_clock():
    policy = personal()
    assert bp.require_personal_p0(policy) is policy
    assert policy.tier == "Personal_Tradovate"
    with pytest.raises(bp.PolicyAbsent):
        bp.require_policy(policy)
    with pytest.raises(bp.PolicyAbsent):
        bp.BookProtectionClock(policy, 100000, 100000)
    for invalid in (None, bp.candidate_book_protection_policy(), object(),
                    replace(policy, tier=bp.TIER)):
        with pytest.raises((bp.PolicyAbsent, bp.PolicyMismatch, ValueError)):
            bp.require_personal_p0(invalid)


@pytest.mark.parametrize("leg,values,want", [
    ("aegis_6j", {}, (8, 0)),
    ("orb_mnq_v7", {}, (1, 1)),
    ("vanguard_mgc", {"normal_base": 2}, (2, 2)),
    ("dj30_mym_p250", {"risk_dollars": 700, "per_contract_risk": 35, "cap_alloc": 80}, (20, 50)),
])
def test_p0_uses_normal_sizing_and_refuses_protected(leg, values, want):
    policy = personal()
    assert bp.entry_quantities(leg, mode=Mode.NORMAL, policy=policy,
                              lifecycle_tier="AUTHORIZED", **values) == want
    with pytest.raises((bp.PolicyMismatch, ValueError)):
        bp.entry_quantities(leg, mode=Mode.PROTECTED, policy=policy,
                            lifecycle_tier="AUTHORIZED", **values)


@pytest.mark.parametrize("cap", [None, 0, -1, True, 1.5, "80"])
def test_invalid_resolved_cap_refuses(cap, monkeypatch):
    policy = personal()
    monkeypatch.setitem(bp.FIRM_RULES[policy.tier], "micro_contract_cap", cap)
    with pytest.raises(ValueError):
        bp.account_micro_cap(policy.tier)


def test_resolved_cap_default_and_personal_limits(monkeypatch):
    policy = personal()
    assert bp.account_micro_cap(policy.tier) == 80
    monkeypatch.setitem(bp.FIRM_RULES[policy.tier], "micro_contract_cap", 20)
    now = datetime(2026, 1, 5, 14, tzinfo=timezone.utc)
    state = capacity.CapacityState("synthetic", "epoch")

    def step(state, qty, *, instance=None):
        seq = state.sequence + 1
        event = capacity.Event(str(seq), seq, now, "synthetic", "epoch",
                               capacity.Reserve(str(seq), "orb_mnq_v7", "SYNTHETIC", qty))
        return capacity.apply_event(state, event, now=now, max_age=timedelta(seconds=1),
                                    instance=instance)

    default = step(state, 21)
    assert default.operations[-1].status == "active"
    over = step(state, 21, instance=policy)
    assert over.operations[-1].status == "refused" and capacity.used_micro(over) == 0
    full = step(state, 20, instance=policy)
    assert capacity.used_micro(full) == 20
    assert step(full, 1, instance=policy).operations[-1].status == "refused"
    assert bp.ACCOUNT_MICRO_CAP == 80


def test_personal_cap_bounds_risk_allocation(monkeypatch):
    policy = personal()
    monkeypatch.setitem(bp.FIRM_RULES[policy.tier], "micro_contract_cap", 20)
    with pytest.raises(ValueError, match="cap"):
        bp.entry_quantities("dj30_mym_p250", mode=Mode.NORMAL, policy=policy,
                            lifecycle_tier="AUTHORIZED", risk_dollars=700,
                            per_contract_risk=35, cap_alloc=21)

