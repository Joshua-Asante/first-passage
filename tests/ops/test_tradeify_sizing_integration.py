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


def test_verified_fingerprints_feed_host_and_operation_capacity(host):
    """Synthetic artifact owners, real serializer/verifier/host/reducer chain."""
    from pathlib import Path
    from book_capacity import CapacityState, Event, Fill, Reserve, Terminal, apply_event, project_capacity
    from policy_fingerprint import (
        REQUIRED_COMPONENTS, build_shared_manifest, canonical_config_bytes,
        sha256_bytes, verify_shared_manifest,
    )

    root = Path(__file__).resolve().parents[2]
    row = {"instance_key": "tradeify_portfolio@Tradeify_Select_100K",
           "reference_mode": POLICY.reference_mode, "scale": str(POLICY.scale),
           "trigger": str(POLICY.trigger)}
    components = {name: (root / name).read_bytes() for name in REQUIRED_COMPONENTS}
    components["config/synthetic.json"] = canonical_config_bytes({"dry_run": True, "armed_until": None})
    artifacts = dict(policy_row=row, geometry_source=(root / "core/dd_geometry.py").read_bytes(),
                     registry_rows={}, components=components,
                     tool_source=(root / "ops/c1_rail/policy_fingerprint.py").read_bytes(),
                     dependency_artifacts={"runtime/synthetic": b"synthetic runtime artifact"})
    frozen = build_shared_manifest(**artifacts)
    verify_shared_manifest(frozen, **artifacts)
    policy_digest = frozen["shared_components"]["policy_row"]["sha256"]
    request, context, binding = inputs()
    context, binding = (replace(item, policy_digest=policy_digest) for item in (context, binding))
    state = CapacityState(context.account_id, context.owner_epoch)
    demand = decide(host, request, project_capacity(state, context), binding)
    assert not demand.halt and (demand.qty_out, demand.prospective_add) == (22, 55)
    assert demand.policy_digest == policy_digest and demand.submit is False
    facts = [Reserve(request.operation_id, request.leg_id, request.order_symbol, demand.qty_out),
             Fill("fill-base", request.operation_id, 22), Terminal(request.operation_id, "filled", 22),
             Reserve("aegis-entry", "aegis_6j", "SYNTHETIC-6J", 3)]
    for sequence, fact in enumerate(facts, 1):
        event = Event(f"event-{sequence}", sequence, NOW, context.account_id, context.owner_epoch, fact)
        state = apply_event(state, event, now=NOW, max_age=timedelta(seconds=30))
    add_request = replace(request, operation_id="add-operation", kind="add")
    add_context = replace(context, operation_id="add-operation", intended_base=22,
                          confirmed_base=22, base_operation_id=request.operation_id)
    refusal = decide(host, add_request, project_capacity(state, add_context), binding)
    assert refusal.halt_reason == "insufficient_observed_capacity" and not refusal.submit
    assert not decide(host, request, context, replace(binding, policy_digest="f" * 64)).submit
    assert decide(host, request, context, replace(binding, policy_digest="f" * 64)).halt
    # A changed input is refused by the real verifier before an owner binds it.
    changed = {**artifacts, "components": {**components, "config/synthetic.json": b"{}"}}
    with pytest.raises(ValueError, match="manifest mismatch"):
        verify_shared_manifest(frozen, **changed)
    assert sha256_bytes(components["config/synthetic.json"]) == frozen["shared_components"]["config/synthetic.json"]["sha256"]


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


@pytest.mark.parametrize("equity,expected", [(99000, Mode.PROTECTED),
                                         (99000.04, Mode.PROTECTED),
                                         (99000.06, Mode.NORMAL)])
def test_settlement_clock_to_session_host_and_invalid_ordering(host, equity, expected):
    from datetime import date
    from book_policy import BookProtectionClock

    clock = BookProtectionClock(POLICY, 100000, 100000)
    assert clock.mode_for(date(2026, 9, 11)) is Mode.NORMAL
    clock.settle(date(2026, 9, 11), equity)
    snapshot = clock.snapshot()
    for duplicate_or_old in (date(2026, 9, 11), date(2026, 9, 10)):
        with pytest.raises(ValueError):
            clock.settle(duplicate_or_old, 101000)
        assert clock.snapshot() == snapshot
    with pytest.raises(ValueError):
        clock.mode_for(date(2026, 9, 11))
    assert clock.mode_for(date(2026, 9, 14)) is expected
    request, context, binding = inputs("aegis_6j")
    settled = replace(context.settled, equity=equity, peak=clock.peak)
    context = replace(context, settled=settled, mode=expected)
    result = decide(host, request, context, replace(binding, settlement=settled))
    assert not result.halt and result.qty_out == (3 if expected is Mode.PROTECTED else 8)


@pytest.mark.parametrize("field,value", [("owner_epoch", "old-boot"),
    ("account_id", "other-account"), ("session_id", "old-session"),
    ("policy_digest", "e" * 64), ("snapshot_digest", "e" * 64)])
def test_fresh_host_rejects_mismatched_restored_context(tmp_path, field, value):
    request, context, binding = inputs()
    restarted = C1SizingHostReference(tmp_path / "lifecycle", tmp_path / "dd", tmp_path / "config")
    result = decide(restarted, request, replace(context, **{field: value}), binding)
    assert result.halt and not result.submit


def transition_fixture():
    from book_capacity import CapacityState, Event, Reserve, Fill, Terminal, apply_event

    state = CapacityState("synthetic-account", "boot-2")
    facts = (Reserve("orb-base", "orb_mnq_v7", "SYNTHETIC-MNQ", 1),
             Fill("orb-fill", "orb-base", 1), Terminal("orb-base", "filled", 1),
             Reserve("orb-add", "orb_mnq_v7", "SYNTHETIC-MNQ", 1))
    for seq, fact in enumerate(facts, 1):
        state = apply_event(state, Event(str(seq), seq, NOW, state.account_id, state.owner_epoch, fact),
                            now=NOW, max_age=timedelta(seconds=30))
    return state


def test_transition_blocks_until_terminal_and_never_resizes_carried_position(host):
    from book_capacity import (Event, Terminal, apply_event, exposures,
                               ProtectionTransition, project_transition)
    state = transition_fixture()
    request, context, binding = inputs()
    transition = ProtectionTransition(state.account_id, state.owner_epoch, context.session_id,
                                      Mode.NORMAL, Mode.PROTECTED, ("orb-add",))
    projected = project_transition(transition, state, context)
    assert projected.blocks and decide(host, request, projected, binding).halt
    # An acknowledgement is not terminal proof and must not release the reservation.
    ack = Event("ack", 5, NOW, state.account_id, state.owner_epoch,
                Terminal("orb-add", "cancel_ack", 0))
    invalid = apply_event(state, ack, now=NOW, max_age=timedelta(seconds=30))
    assert project_transition(transition, invalid, context).blocks
    terminal = replace(ack, event_id="terminal", fact=Terminal("orb-add", "cancelled", 0))
    done = apply_event(state, terminal, now=NOW, max_age=timedelta(seconds=30))
    completed = project_transition(transition, done, context)
    assert not completed.blocks and not decide(host, request, completed, binding).halt
    orb = next(row for row in exposures(done) if row.leg_id == "orb_mnq_v7")
    assert (orb.confirmed, orb.reserved) == (1, 0)
    assert transition.operation_ids == ("orb-add",)  # descriptor retained for reconciliation
    assert project_transition(transition, done, replace(context, blocks=("other",))).blocks == ("other",)
    orb_request, orb_context, orb_binding = inputs("orb_mnq_v7")
    orb_context = replace(orb_context, intended_base=1, confirmed_base=1, base_operation_id="orb-base")
    orb_request = replace(orb_request, kind="add")
    assert decide(host, orb_request, project_transition(transition, state, orb_context), orb_binding).halt
    refused_add = decide(host, orb_request, project_transition(transition, done, orb_context), orb_binding)
    assert not refused_add.halt and refused_add.qty_out == 0 and not refused_add.submit


@pytest.mark.parametrize("changes", [{"owner_epoch": "old"}, {"session_id": "old"},
    {"operation_ids": ("unknown",)}, {"operation_ids": ("orb-add", "orb-add")},
    {"mode": Mode.NORMAL}])
def test_transition_invalid_binding_fails_closed(changes):
    from book_capacity import ProtectionTransition, project_transition
    state = transition_fixture()
    _, context, _ = inputs()
    transition = ProtectionTransition(state.account_id, state.owner_epoch, context.session_id,
                                      Mode.NORMAL, Mode.PROTECTED, ("orb-add",))
    with pytest.raises(ValueError):
        project_transition(replace(transition, **changes), state, context)


@pytest.mark.parametrize("terminal_status", ["filled", "cancelled", "rejected"])
def test_transition_fill_race_retains_carried_quantity_and_unknown_blocks(terminal_status):
    from book_capacity import (Event, Fill, Terminal, apply_event, exposures,
                               ProtectionTransition, project_transition)
    state = transition_fixture()
    _, context, _ = inputs()
    transition = ProtectionTransition(state.account_id, state.owner_epoch, context.session_id,
                                      Mode.NORMAL, Mode.PROTECTED, ("orb-add",))
    fill = Event("late-fill", 5, NOW, state.account_id, state.owner_epoch,
                 Fill("add-fill", "orb-add", 1))
    state = apply_event(state, fill, now=NOW, max_age=timedelta(seconds=30))
    assert project_transition(transition, state, context).blocks  # full fill still needs terminal
    terminal = replace(fill, event_id="terminal", sequence=6,
                       fact=Terminal("orb-add", terminal_status, 1))
    state = apply_event(state, terminal, now=NOW, max_age=timedelta(seconds=30))
    assert not project_transition(transition, state, context).blocks
    orb = next(e for e in exposures(state) if e.leg_id == "orb_mnq_v7")
    assert (orb.confirmed, orb.reserved) == (2, 0)
    unknown = replace(fill, event_id="unknown", sequence=7, fact=Fill("unknown", "missing", 1))
    state = apply_event(state, unknown, now=NOW, max_age=timedelta(seconds=30))
    assert project_transition(transition, state, context).blocks


def test_transition_requires_every_captured_add_to_be_terminal():
    from book_capacity import (Event, Reserve, Terminal, apply_event,
                               ProtectionTransition, project_transition)
    state = transition_fixture()
    _, context, _ = inputs()
    event = Event("second", 5, NOW, state.account_id, state.owner_epoch,
                  Reserve("orb-add-2", "orb_mnq_v7", "SYNTHETIC-MNQ", 1))
    state = apply_event(state, event, now=NOW, max_age=timedelta(seconds=30))
    transition = ProtectionTransition(state.account_id, state.owner_epoch, context.session_id,
                                      Mode.NORMAL, Mode.PROTECTED, ("orb-add", "orb-add-2"))
    state = apply_event(state, replace(event, event_id="terminal-1", sequence=6,
                        fact=Terminal("orb-add", "cancelled", 0)),
                        now=NOW, max_age=timedelta(seconds=30))
    assert project_transition(transition, state, context).blocks
    state = apply_event(state, replace(event, event_id="terminal-2", sequence=7,
                        fact=Terminal("orb-add-2", "cancelled", 0)),
                        now=NOW, max_age=timedelta(seconds=30))
    assert not project_transition(transition, state, context).blocks


@pytest.mark.parametrize("leg_id,adapter_normal", [("aegis_6j", 8),
    ("dj30_mym_p250", 2), ("vanguard_mgc", 2), ("orb_mnq_v7", 1)])
@pytest.mark.parametrize("protected", [False, True])
@pytest.mark.parametrize("tier", ["AUTHORIZED", "WATCH-1", "WATCH-2", "RETIRED"])
def test_rp_adapter_normal_entry_shared_admission_matches_host(host, leg_id, adapter_normal,
                                                              protected, tier):
    from book_policy import entry_quantities, leg
    from c1_signal_daemon.book_protocol import OrderIntent, Bracket

    bracket = Bracket(stop=90, limit=110, trail_activation_ticks=8, trail_offset_ticks=4)
    intent = OrderIntent("adapter-entry", leg_id, "entry", leg(leg_id).entry_side,
                         adapter_normal, bracket=bracket, stop_dist_pts=2)
    request, context, binding = inputs(leg_id, protected=protected, tier=tier)
    # Explicit normalized owner inputs; production payload conversion is TB-I3.
    dollars_per_point = Fraction(1)
    risk = Fraction(intent.stop_dist_pts) * dollars_per_point
    binding = replace(binding, risk_dollars=Fraction(5))
    request = replace(request, normal_base=intent.qty, per_contract_risk=risk)
    shared = entry_quantities(leg_id, policy=POLICY, mode=context.mode, lifecycle_tier=tier,
                              normal_base=intent.qty, risk_dollars=binding.risk_dollars,
                              per_contract_risk=risk, cap_alloc=binding.cap_alloc)
    result = decide(host, request, context, binding)
    assert not result.halt and (result.qty_out, result.prospective_add) == shared
    assert intent.qty == adapter_normal and intent.bracket == bracket
    if result.qty_out:
        admitted = replace(intent, qty=result.qty_out)
        assert admitted.bracket == bracket and admitted.stop_dist_pts == intent.stop_dist_pts
    assert result.submit is False


@pytest.mark.parametrize("leg_id,normal_add,confirmed", [
    ("dj30_mym_p250", 55, 3), ("vanguard_mgc", 2, 1), ("orb_mnq_v7", 1, 1)])
@pytest.mark.parametrize("protected", [False, True])
def test_rp_add_uses_confirmed_base_not_adapter_add(host, leg_id, normal_add, confirmed, protected):
    from book_policy import add_quantity, leg
    from c1_signal_daemon.book_protocol import OrderIntent

    intent = OrderIntent("adapter-add", leg_id, "add", leg(leg_id).entry_side, normal_add)
    request, context, binding = inputs(leg_id, protected=protected)
    context = replace(context, intended_base=max(leg(leg_id).normal_base_values),
                      confirmed_base=confirmed, base_operation_id="confirmed-base",
                      exposures=tuple(replace(row, confirmed=confirmed) if row.leg_id == leg_id
                                      else row for row in context.exposures))
    # The adapter add is intentionally not substituted for confirmed-base evidence.
    result = decide(host, replace(request, kind="add"), context, binding)
    assert not result.halt and result.qty_out == add_quantity(
        leg_id, confirmed, mode=context.mode, policy=POLICY, lifecycle_tier="AUTHORIZED")
    assert intent.qty == normal_add
    if leg_id == "dj30_mym_p250":
        assert result.qty_out == 7 and result.qty_out != intent.qty


def test_rp_normal_integer_cannot_supply_missing_risk_or_fill_evidence(host):
    request, context, binding = inputs()
    request = replace(request, normal_base=22)
    assert decide(host, request, context, replace(binding, risk_dollars=None)).halt
    assert decide(host, replace(request, per_contract_risk=None), context, binding).halt
    assert decide(host, replace(request, kind="add"), context, binding).halt


@pytest.mark.parametrize("kind", ["exit", "flat"])
@pytest.mark.parametrize("qty", [None, 3])
def test_rp_exit_scope_and_bracket_semantics_unchanged(kind, qty):
    from c1_signal_daemon.book_protocol import OrderIntent, Bracket, BracketAmend, Side

    intent = OrderIntent("exit", "aegis_6j", kind, Side.BUY, qty, scope_fill_ids=("confirmed-fill",))
    bracket = Bracket(stop=90, limit=110, trail_activation_ticks=8, trail_offset_ticks=4)
    amend = BracketAmend(intent.leg_id, bracket, intent.scope_fill_ids)
    assert intent.qty == qty and intent.scope_fill_ids == ("confirmed-fill",)
    assert amend.bracket is bracket and amend.scope_fill_ids == intent.scope_fill_ids


def test_host_threads_vanguard_normal_ladder(host):
    request, context, binding = inputs("vanguard_mgc", protected=False)
    result = decide(host, replace(request, normal_base=1), context, binding)
    assert not result.halt and (result.qty_out, result.prospective_add) == (1, 1)
