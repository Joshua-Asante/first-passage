"""Synthetic TB-S1 vectors; these do not discharge private export parity."""
from fractions import Fraction

import pytest

import c1_rail.book_policy as policy
from c1_signal_daemon.book_protocol import Mode


POLICY = policy.candidate_book_protection_policy()
STRIKER = "dj30_mym_p250"
MODE_ROWS = [
    (Mode.NORMAL, "AUTHORIZED", (8, 0), (1, 1), (2, 2), (1, 1), (22, 55)),
    (Mode.PROTECTED, "AUTHORIZED", (3, 0), (0, 0), (0, 0), (1, 0), (22, 55)),
    (Mode.NORMAL, "WATCH-1", (4, 0), (0, 0), (0, 0), (0, 0), (22, 55)),
    (Mode.PROTECTED, "WATCH-1", (1, 0), (0, 0), (0, 0), (0, 0), (14, 35)),
    (Mode.NORMAL, "WATCH-2", (2, 0), (0, 0), (0, 0), (0, 0), (17, 42)),
    (Mode.PROTECTED, "WATCH-2", (0, 0), (0, 0), (0, 0), (0, 0), (7, 17)),
    (Mode.NORMAL, "RETIRED", (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)),
    (Mode.PROTECTED, "RETIRED", (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)),
]
ADDS = (0, 2, 5, 7, 10, 12, 15, 17, 20, 22, 25, 27, 30,
        32, 35, 37, 40, 42, 45, 47, 50, 52, 55)


def striker(**overrides):
    args = dict(policy=POLICY, mode=Mode.PROTECTED, lifecycle_tier="AUTHORIZED",
                risk_dollars=700, per_contract_risk=10, cap_alloc=80)
    args.update(overrides)
    return policy.entry_quantities(STRIKER, **args)


@pytest.mark.parametrize("mode,tier,aegis,v1,v2,orb,s", MODE_ROWS)
def test_literal_mode_lifecycle_rows(mode, tier, aegis, v1, v2, orb, s):
    args = dict(policy=POLICY, mode=mode, lifecycle_tier=tier)
    assert policy.entry_quantities("aegis_6j", **args) == aegis
    assert policy.entry_quantities("vanguard_mgc", normal_base=1, **args) == v1
    assert policy.entry_quantities("vanguard_mgc", normal_base=2, **args) == v2
    assert policy.entry_quantities("orb_mnq_v7", **args) == orb
    assert striker(mode=mode, lifecycle_tier=tier) == s


@pytest.mark.parametrize("mode,tier,m", [
    (Mode.NORMAL, "AUTHORIZED", Fraction(1)),
    (Mode.PROTECTED, "AUTHORIZED", Fraction(2, 5)),
    (Mode.NORMAL, "WATCH-1", Fraction(1, 2)),
    (Mode.PROTECTED, "WATCH-1", Fraction(1, 5)),
    (Mode.NORMAL, "WATCH-2", Fraction(1, 4)),
    (Mode.PROTECTED, "WATCH-2", Fraction(1, 10)),
])
@pytest.mark.parametrize("base", range(1, 23))
def test_every_striker_integer_boundary(mode, tier, m, base):
    risk = Fraction(base) / m
    args = dict(mode=mode, lifecycle_tier=tier, per_contract_risk=1)
    assert striker(risk_dollars=risk, **args) == (base, ADDS[base])
    assert striker(risk_dollars=risk - Fraction(1, 10000), **args) == (
        base - 1, ADDS[base - 1])


def test_noncap_law_b_and_inert_allocation():
    assert striker(risk_dollars=Fraction(5, 2), per_contract_risk=1) == (1, 2)
    assert striker(cap_alloc=0) == (0, 0)
    assert striker(cap_alloc=35) == (10, 25)


@pytest.mark.parametrize("base,add", enumerate(ADDS))
def test_add_uses_confirmed_base_without_second_haircut(base, add):
    assert policy.add_quantity(STRIKER, base, policy=POLICY,
                               mode=Mode.PROTECTED, lifecycle_tier="WATCH-2") == add


@pytest.mark.parametrize("leg,base,mode,tier,want", [
    (STRIKER, 3, Mode.NORMAL, "AUTHORIZED", 7),
    (STRIKER, 22, Mode.NORMAL, "RETIRED", 0),
    ("vanguard_mgc", 1, Mode.NORMAL, "AUTHORIZED", 1),
    ("vanguard_mgc", 2, Mode.NORMAL, "AUTHORIZED", 2),
    ("vanguard_mgc", 2, Mode.PROTECTED, "AUTHORIZED", 0),
    ("vanguard_mgc", 2, Mode.NORMAL, "WATCH-1", 0),
    ("orb_mnq_v7", 1, Mode.PROTECTED, "AUTHORIZED", 0),
    ("orb_mnq_v7", 1, Mode.NORMAL, "WATCH-1", 0),
])
def test_partial_and_carried_base_add_admission(leg, base, mode, tier, want):
    assert policy.add_quantity(leg, base, policy=POLICY,
                               mode=mode, lifecycle_tier=tier) == want


@pytest.mark.parametrize("field,bad", [
    ("risk_dollars", None), ("risk_dollars", True), ("risk_dollars", "700"),
    ("risk_dollars", float("nan")), ("risk_dollars", float("inf")),
    ("risk_dollars", -1), ("risk_dollars", 0),
    ("per_contract_risk", None), ("per_contract_risk", 0),
    ("per_contract_risk", -1), ("per_contract_risk", float("inf")),
    ("cap_alloc", None), ("cap_alloc", True), ("cap_alloc", 80.0),
    ("cap_alloc", -1), ("cap_alloc", 81),
    ("mode", None), ("lifecycle_tier", None), ("lifecycle_tier", "unknown"),
])
def test_invalid_inputs_refuse_even_with_retired_or_zero_output(field, bad):
    with pytest.raises((ValueError, TypeError)):
        striker(**{field: bad})


def test_missing_policy_and_authorization_fail_closed():
    with pytest.raises(policy.PolicyAbsent):
        striker(policy=None)
    with pytest.raises(TypeError):
        policy.entry_quantities("aegis_6j", policy=POLICY, mode=Mode.NORMAL)  # pylint: disable=missing-kwoa
    with pytest.raises(ValueError, match="risk"):
        policy.leg_quantities(STRIKER, 22, policy=POLICY, mode=Mode.NORMAL)


@pytest.mark.parametrize("normal", [True, -1, 23, 1.5, float("nan")])
def test_invalid_normal_diagnostic_is_rejected(normal):
    with pytest.raises(ValueError):
        striker(normal_base=normal)


@pytest.mark.parametrize("base", [True, 1.5, -1, 23])
def test_bad_confirmed_base_is_not_an_add(base):
    with pytest.raises(ValueError):
        policy.add_quantity(STRIKER, base, policy=POLICY,
                            mode=Mode.NORMAL, lifecycle_tier="AUTHORIZED")


def test_table_requires_explicit_risk_samples_and_retains_them():
    samples = [policy.StrikerRiskInputs(Fraction(i, 2), Fraction(1), 80)
               for i in range(1, 444, 2)]
    rows = policy.quantity_table(POLICY, striker_inputs=samples)
    for mode, tier, *_ in MODE_ROWS[:6]:
        selected = [r for r in rows if r.leg_id == STRIKER
                    and r.mode == mode and r.lifecycle_tier == tier]
        assert {r.base for r in selected} == set(range(23))
        for row in selected:
            assert row.risk_inputs in samples
            assert (row.base, row.add) == striker(
                mode=mode, lifecycle_tier=tier,
                risk_dollars=row.risk_inputs.risk_dollars, per_contract_risk=1)
    with pytest.raises(TypeError):
        policy.quantity_table(POLICY)  # pylint: disable=missing-kwoa
    with pytest.raises(ValueError):
        policy.quantity_table(POLICY, striker_inputs=[])
    with pytest.raises(ValueError):
        policy.quantity_table(POLICY, striker_inputs=[(700, 10, 80)])
    with pytest.raises(ValueError):
        policy.quantity_table(POLICY, lifecycle_tiers=[], striker_inputs=samples)
    menu = policy.reachable_quantity_menu(POLICY, striker_inputs=samples)
    assert menu[STRIKER] == {"base": set(range(1, 23)), "add": set(ADDS[1:])}
