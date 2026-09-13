"""Real host -> explicit synthetic account context -> shared quantity laws."""
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from fractions import Fraction

import pytest

from book_policy import BOOK_LEGS, candidate_book_protection_policy
from c1_sizing_host_reference import C1SizingHostReference
from c1_signal_daemon.book_protocol import Mode
from book_sizing_context import (
    BookAccountContext, BookExposure, BookSession, BookSizingBinding,
    BookSizingRequest, SettledClose,
)


NOW = datetime(2026, 9, 14, 15, tzinfo=timezone.utc)
POLICY = candidate_book_protection_policy()


def inputs(leg_id="dj30_mym_p250", *, protected=True, tier="AUTHORIZED"):
    spec = next(item for item in BOOK_LEGS if item.leg_id == leg_id)
    session = BookSession("session-2", "session-1", NOW - timedelta(hours=1),
                          NOW + timedelta(hours=1), NOW + timedelta(hours=2), "a" * 64)
    settled = SettledClose("session-1", NOW - timedelta(days=1),
                           99000 if protected else 100000, 100000, "d" * 64)
    binding = BookSizingBinding("synthetic-account", "boot-2", "b" * 64,
                                "c" * 64, settled, session, timedelta(seconds=30),
                                leg_id, "SYNTHETIC-" + spec.symbol, 80, Fraction(700))
    context = BookAccountContext(
        "synthetic-account", "boot-2", "op-2", leg_id, binding.order_symbol,
        "session-2", Mode.PROTECTED if protected else Mode.NORMAL,
        "b" * 64, "c" * 64, "a" * 64, settled, spec.lifecycle_key, tier,
        NOW, NOW + timedelta(seconds=30), 0, 0, None,
        tuple(BookExposure(item.leg_id, 0, 0) for item in BOOK_LEGS), (), ())
    request = BookSizingRequest("op-2", leg_id, binding.order_symbol, "entry",
                                2 if leg_id == "vanguard_mgc" else None, Fraction(10))
    return request, context, binding


@pytest.fixture
def host(tmp_path):
    # Book sizing must not read historical files or intraday equity.
    return C1SizingHostReference(tmp_path / "absent-lifecycle",
                                 tmp_path / "absent-dd", tmp_path / "absent-constants")


def decide(host, request, context, binding, **kwargs):
    return host.process_book_signal(request, context=context, binding=binding,
                                    policy=kwargs.get("policy", POLICY),
                                    now=kwargs.get("now", NOW))


def test_capacity_projection_preserves_evidence_and_blocks_real_host(host):
    from book_capacity import CapacityState, Event, Reserve, apply_event, project_capacity

    request, context, binding = inputs()
    state = CapacityState(context.account_id, context.owner_epoch)
    event = Event("reserve", 1, NOW, context.account_id, context.owner_epoch,
                  Reserve("other", "aegis_6j", "SYNTHETIC-6J", 8))
    state = apply_event(state, event, now=NOW, max_age=timedelta(seconds=30))
    projected = project_capacity(state, context)
    assert projected.as_of == context.as_of and projected.snapshot_digest == context.snapshot_digest
    assert projected.pending_operation_ids == ("other",)
    result = decide(host, request, projected, binding)
    assert result.halt and result.submit is False
    with pytest.raises(ValueError, match="identity"):
        project_capacity(replace(state, owner_epoch="wrong"), context)


def test_capacity_projection_does_not_erase_existing_obligations(host):
    from book_capacity import CapacityState, project_capacity

    request, context, binding = inputs()
    context = replace(context, blocks=("transition",), pending_operation_ids=("existing",))
    projected = project_capacity(CapacityState(context.account_id, context.owner_epoch), context)
    assert projected.blocks == ("transition",) and projected.pending_operation_ids == ("existing",)
    assert decide(host, request, projected, binding).halt


def test_empty_capacity_projection_reaches_shared_sizing_laws(host):
    from book_capacity import CapacityState, project_capacity

    request, context, binding = inputs()
    projected = project_capacity(CapacityState(context.account_id, context.owner_epoch), context)
    result = decide(host, request, projected, binding)
    assert not result.halt and (result.qty_out, result.prospective_add) == (22, 55)
    assert result.submit is False


@pytest.mark.parametrize("leg_id,normal,protected", [
    ("aegis_6j", (8, 0), (3, 0)),
    ("dj30_mym_p250", (22, 55), (22, 55)),
    ("vanguard_mgc", (2, 2), (0, 0)),
    ("orb_mnq_v7", (1, 1), (1, 0)),
])
@pytest.mark.parametrize("protected_mode", [False, True])
def test_host_uses_shared_quantity_laws(host, leg_id, normal, protected, protected_mode):
    request, context, binding = inputs(leg_id, protected=protected_mode)
    result = decide(host, request, context, binding)
    assert not result.halt
    assert (result.qty_out, result.prospective_add) == (protected if protected_mode else normal)
    assert result.submit is False
    assert result.operation_id == request.operation_id


@pytest.mark.parametrize("field,value", [
    ("account_id", "wrong"), ("owner_epoch", "boot-old"),
    ("operation_id", "wrong"), ("leg_id", "aegis_6j"),
    ("order_symbol", "wrong"), ("session_id", "old-session"),
    ("policy_digest", "e" * 64), ("snapshot_digest", "e" * 64),
    ("calendar_digest", "e" * 64), ("lifecycle_key", "Striker"),
    ("lifecycle_tier", "unknown"), ("mode", Mode.NORMAL),
    ("as_of", NOW - timedelta(seconds=31)), ("as_of", NOW + timedelta(seconds=1)),
    ("valid_until", NOW), ("confirmed_base", True),
    ("pending_operation_ids", ("op-2",)), ("blocks", ("orb-cancel-pending",)),
    ("exposures", ()), ("settled", None),
])
def test_context_defects_halt(host, field, value):
    request, context, binding = inputs()
    result = decide(host, request, replace(context, **{field: value}), binding)
    assert result.halt and result.qty_out == 0 and not result.submit


@pytest.mark.parametrize("field,value", [
    ("session_id", "session-2"), ("seal_digest", ""),
    ("seal_digest", "e" * 64), ("as_of", NOW),
    ("equity", float("nan")), ("peak", 98000),
])
def test_bad_settlement_halts(host, field, value):
    request, context, binding = inputs()
    context = replace(context, settled=replace(context.settled, **{field: value}))
    assert decide(host, request, context, binding).halt


def test_explicit_policy_context_and_session_required(host):
    request, context, binding = inputs()
    assert decide(host, request, context, binding, policy=None).halt
    assert decide(host, request, None, binding).halt
    assert decide(host, request, context, None).halt
    assert decide(host, request, context, binding, now=NOW.replace(tzinfo=None)).halt
    assert decide(host, request, context, binding, now=binding.session.risk_add_cutoff).halt


def test_partial_confirmed_base_sizes_add_without_second_haircut(host):
    request, context, binding = inputs()
    context = replace(context, intended_base=22, confirmed_base=7, base_operation_id="base-1",
                      exposures=tuple(replace(row, confirmed=7) if row.leg_id == request.leg_id
                                      else row for row in context.exposures))
    result = decide(host, replace(request, kind="add"), context, binding)
    assert not result.halt and result.qty_out == 17 and not result.submit
    # The host never changes the carried base or the in-memory historical map.
    assert context.confirmed_base == 7 and host.open_leg_state == {}
    assert decide(host, replace(request, kind="add"),
                  replace(context, confirmed_base=23), binding).halt


def test_zero_allocation_cannot_size_even_fixed_leg(host):
    request, context, binding = inputs("aegis_6j")
    result = decide(host, request, context, replace(binding, cap_alloc=0))
    assert result.qty_out == 0 and not result.submit


def test_capacity_observation_is_all_or_refuse(host):
    request, context, binding = inputs("dj30_mym_p250")
    context = replace(context, exposures=tuple(
        replace(row, confirmed=3, reserved=3) if row.leg_id == "aegis_6j" else row
        for row in context.exposures))
    result = decide(host, request, context, binding)
    assert result.halt and result.qty_out == 0
    assert result.halt_reason == "insufficient_observed_capacity"
    assert context.exposures[0].reserved == 3


@pytest.mark.parametrize("equity,mode", [(99000.06, Mode.NORMAL), (99000.04, Mode.PROTECTED)])
def test_prior_close_ulp_boundary(host, equity, mode):
    request, context, binding = inputs("aegis_6j")
    context = replace(context, mode=mode, settled=replace(context.settled, equity=equity))
    binding = replace(binding, settlement=context.settled)
    result = decide(host, request, context, binding)
    assert not result.halt and result.qty_out == (8 if mode is Mode.NORMAL else 3)


@pytest.mark.parametrize("leg_id,tier,normal,protected", [
    ("aegis_6j", "WATCH-1", 4, 1), ("aegis_6j", "WATCH-2", 2, 0),
    ("aegis_6j", "RETIRED", 0, 0),
    ("dj30_mym_p250", "WATCH-1", 22, 14),
    ("dj30_mym_p250", "WATCH-2", 17, 7),
    ("dj30_mym_p250", "RETIRED", 0, 0),
    ("vanguard_mgc", "WATCH-1", 0, 0), ("vanguard_mgc", "WATCH-2", 0, 0),
    ("vanguard_mgc", "RETIRED", 0, 0),
    ("orb_mnq_v7", "WATCH-1", 0, 0), ("orb_mnq_v7", "WATCH-2", 0, 0),
    ("orb_mnq_v7", "RETIRED", 0, 0),
])
@pytest.mark.parametrize("protected_mode", [False, True])
def test_lifecycle_is_threaded_without_call4(host, leg_id, tier, normal, protected, protected_mode):
    request, context, binding = inputs(leg_id, protected=protected_mode, tier=tier)
    result = decide(host, request, context, binding)
    assert not result.halt and not result.submit
    assert result.qty_out == (protected if protected_mode else normal)


@pytest.mark.parametrize("leg_id,base,normal,protected", [
    ("dj30_mym_p250", 3, 7, 7), ("vanguard_mgc", 2, 2, 0),
    ("orb_mnq_v7", 1, 1, 0),
])
@pytest.mark.parametrize("protected_mode", [False, True])
def test_confirmed_adds_and_carried_positions(host, leg_id, base, normal, protected, protected_mode):
    request, context, binding = inputs(leg_id, protected=protected_mode)
    context = replace(context, intended_base=base, confirmed_base=base, base_operation_id="base-1",
                      exposures=tuple(replace(row, confirmed=base) if row.leg_id == leg_id
                                      else row for row in context.exposures))
    result = decide(host, replace(request, kind="add"), context, binding)
    assert not result.halt and result.qty_out == (protected if protected_mode else normal)
    assert context.confirmed_base == base and result.prospective_add == 0


@pytest.mark.parametrize("field,value", [
    ("cap_alloc", True), ("cap_alloc", -1), ("cap_alloc", 81),
    ("policy_digest", ""), ("snapshot_digest", ""), ("order_symbol", None),
    ("max_evidence_age", timedelta(0)), ("risk_dollars", None),
    ("risk_dollars", float("inf")), ("session", None),
])
def test_invalid_binding_halts(host, field, value):
    request, context, binding = inputs()
    assert decide(host, request, context, replace(binding, **{field: value})).halt


@pytest.mark.parametrize("field,value", [
    ("operation_id", ""), ("leg_id", "dj30_mym"), ("order_symbol", "wrong"),
    ("kind", "exit"), ("kind", "flat"), ("kind", "unknown"),
    ("per_contract_risk", 0), ("per_contract_risk", True),
    ("per_contract_risk", float("nan")), ("normal_base", 99),
])
def test_invalid_request_halts(host, field, value):
    request, context, binding = inputs()
    assert decide(host, replace(request, **{field: value}), context, binding).halt


def test_exposures_are_complete_gross_counts(host):
    request, context, binding = inputs("orb_mnq_v7", protected=False)
    rows = context.exposures
    for bad_rows in (rows + (rows[0],), (rows[0],) * 4,
                     (replace(rows[0], confirmed=-1),) + rows[1:],
                     (replace(rows[0], reserved=True),) + rows[1:]):
        assert decide(host, request, replace(context, exposures=bad_rows), binding).halt
    # 70 equivalents in 6J plus 9 in MYM leaves exactly one for ORB.
    context = replace(context, exposures=tuple(
        replace(row, confirmed=7) if row.leg_id == "aegis_6j" else
        replace(row, reserved=9) if row.leg_id == "dj30_mym_p250" else row
        for row in rows))
    result = decide(host, request, context, binding)
    assert not result.halt and result.observed_used_micro == 79 and result.requested_micro == 1
    assert result.submit is False


def test_session_identity_comes_from_calendar_not_weekday_arithmetic(host):
    request, context, binding = inputs()
    friday = NOW - timedelta(days=3)
    context = replace(context, settled=replace(context.settled, as_of=friday))
    binding = replace(binding, settlement=context.settled)
    assert not decide(host, request, context, binding).halt
    # Even a fresh close cannot substitute a different calendar session identity.
    context = replace(context, settled=replace(context.settled, session_id="skipped-session"))
    assert decide(host, request, context, binding).halt


def test_no_in_memory_dedupe_or_account_mutation_is_claimed(host):
    request, context, binding = inputs()
    first = decide(host, request, context, binding)
    assert first == decide(host, request, context, binding)
    assert not first.submit
    assert decide(host, request, replace(context, pending_operation_ids=(request.operation_id,)),
                  binding).halt


def test_changed_settlement_cannot_reuse_a_verified_seal(host):
    request, context, binding = inputs("aegis_6j")
    # Mode and digest still agree, but the evidence contents have changed.
    changed = replace(context, settled=replace(context.settled, equity=98000))
    assert decide(host, request, changed, binding).halt


def test_host_threads_risk_before_floor_instead_of_normal_integer(host):
    request, context, binding = inputs()
    request = replace(request, normal_base=2, per_contract_risk=Fraction(2))
    binding = replace(binding, risk_dollars=Fraction(5))
    result = decide(host, request, context, binding)
    assert not result.halt and (result.qty_out, result.prospective_add) == (1, 2)


def test_host_threads_vanguard_normal_ladder(host):
    request, context, binding = inputs("vanguard_mgc", protected=False)
    result = decide(host, replace(request, normal_base=1), context, binding)
    assert not result.halt and (result.qty_out, result.prospective_add) == (1, 1)
