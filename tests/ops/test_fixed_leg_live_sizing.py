"""Fixed-leg source quantities are signals, not live policy overrides.

Public synthetic consumers only; this is never FG or accepted-port evidence.
"""
from dataclasses import replace
from datetime import timedelta
from enum import IntEnum

import pytest

from c1_rail.book_account_owner import BookAccountOwner, BrokerFact
from c1_rail.book_policy import entry_quantities, validate_size_vector
from c1_rail.qualification.model import ET, PathBar, SessionSchedule
from c1_rail.qualification.replay import BookReplay, Instrument
from c1_signal_daemon.book_adapters import ADAPTER_BY_LEG, synthetic_adapter_registry
from c1_signal_daemon.book_bundle_execution import (
    BundleExecution, SizingInputs, run_sized_adapter,
)
from c1_signal_daemon.book_protocol import Mode
from c1_signal_daemon.book_runtime import FourLegRuntime
from c1_signal_daemon.feed import Bar
from c1_signal_daemon.tv_broker_emulator import TVBrokerEmulator
from mc.simulation import EvaluationState
from book_bootstrap_fixtures import activate_fresh
from test_four_leg_runtime import NOW, binding, entry
from test_personal_replay_live_parity import LEGS, POLICY, REASONS, VECTOR, OwnerBroker, Script


class OneEntry(Script):
    """One source intent; preserve it separately from the consumer's sized copy."""

    def __init__(self, leg_id, action=None):
        super().__init__(leg_id, action is not None)
        self.action = action

    def on_bar(self, bar):
        self.index += 1
        return [self.action] if self.index == 1 and self.active else []


def exercise(tmp_path, route, leg_id, source_qty, *, vector=None, protected=False,
             tier="AUTHORIZED"):
    action = replace(entry(leg_id, source_qty, stop=24), qty=source_qty)
    sources = {k: OneEntry(k, action if k == leg_id else None) for k in LEGS}
    source = sources[leg_id]
    spec = ADAPTER_BY_LEG[leg_id]
    mode = Mode.PROTECTED if protected else Mode.NORMAL
    admitted, outcomes = [], []
    if route == "adapter":
        consumer = BundleExecution(source, SizingInputs(
            leg_id, mode, tier, 80, 100, spec.pointvalue,
            None if vector is None else vector.leg(leg_id)), policy=POLICY)
        broker = TVBrokerEmulator(leg_id, spec.mintick, spec.pointvalue, 0, 0)
    elif route == "replay":
        # Independent producer matching personal replay: only Vanguard consumes
        # its port ladder; fixed legs omit normal_base and Striker consumes risk.
        def sizing(k, intent, pb):
            values = {"lifecycle_tier": tier}
            if k == "vanguard_mgc":
                values["normal_base"] = intent.qty
            elif k == "dj30_mym_p250":
                values.update(risk_dollars=100,
                              per_contract_risk=intent.stop_dist_pts * ADAPTER_BY_LEG[k].pointvalue,
                              cap_alloc=80)
            return values

        equity = 98500 if protected else 100000
        consumer = BookReplay(sources, {k: Instrument(ADAPTER_BY_LEG[k].mintick,
            ADAPTER_BY_LEG[k].pointvalue, 0, 0) for k in LEGS}, policy=POLICY,
            initial_state=EvaluationState(original_basis=100000, current_equity=equity,
                historical_eod_peak=100000, prior_trade_days=1 if protected else 0,
                prior_max_day_profit=0),
            sizing_inputs=sizing, schedule_quotes=lambda *args: 100,
            **({} if vector is None else {"size_vector": vector}))
    else:
        data = binding(protected=protected)
        data.update(valid_until=NOW + timedelta(hours=2), max_evidence_age=timedelta(hours=2))
        data["lifecycle_tiers"][leg_id] = tier
        if vector is not None:
            data["size_vector"] = vector
        broker = OwnerBroker(False)
        consumer = BookAccountOwner.boot(tmp_path / "owner.sqlite", "synthetic-account",
                                         binding=data, synthetic_broker=broker)
        activate_fresh(consumer)
        runtime = FourLegRuntime(consumer, synthetic_adapter_registry(sources))
    for index in range(2):
        instant = NOW + timedelta(minutes=15 * index)
        bar = Bar(instant, 100, 100, 100, 100)
        if route == "adapter":
            actions = consumer.on_bar(bar)
            admitted.extend(a.qty for a in actions)
            for event in broker.submit(actions, bar):
                consumer.on_execution(event)
        elif route == "replay":
            pb = PathBar(instant, instant, instant.date(), instant.astimezone(ET),
                         tuple((k, bar) for k in LEGS))
            schedule = SessionSchedule(NOW + timedelta(hours=1), NOW + timedelta(hours=1, minutes=10),
                                       NOW + timedelta(hours=1, minutes=15))
            consumer._index, consumer._path_time = index, instant
            for intent in source.on_bar(bar):
                sized = consumer._admit(intent, pb, mode, schedule)
                if sized is not None:
                    admitted.append(sized.qty)
                    consumer._submit(leg_id, [sized], bar)
        else:
            broker.advance(instant)
            for k in LEGS:
                result = runtime.on_completed_bar(k, bar, now=instant)
                if result is not None:
                    outcomes.extend(result)
            for command in broker.commands[len(admitted):]:
                observed = instant + timedelta(microseconds=1)
                runtime.observe_fact(BrokerFact.terminal(command.operation_id, "filled",
                    command.quantity, observed), now=observed)
            admitted = [c.quantity for c in broker.commands]
    return admitted, source, consumer, outcomes


def assert_fill(result, expected, source_qty):
    admitted, source, _, outcomes = result
    assert admitted == [expected], outcomes
    assert source.action.qty == source_qty
    assert [(e.event, e.fill.qty if e.fill else None) for e in source.events] == [("fill", expected)]


@pytest.mark.parametrize("route", REASONS)
@pytest.mark.parametrize("source_qty", range(1, 9))
def test_f1_aegis_source_ladder_does_not_override_fixed_size(tmp_path, route, source_qty):
    assert_fill(exercise(tmp_path, route, "aegis_6j", source_qty,
                         vector=validate_size_vector(VECTOR)), 3, source_qty)


@pytest.mark.parametrize("route", REASONS)
@pytest.mark.parametrize("protected", [False, True])
def test_f2_orb_conflicting_source_quantity_keeps_fixed_size(tmp_path, route, protected):
    assert_fill(exercise(tmp_path, route, "orb_mnq_v7", 2,
                         vector=validate_size_vector(VECTOR), protected=protected), 1, 2)


@pytest.mark.parametrize("route", REASONS)
@pytest.mark.parametrize("leg_id,source_qty,expected", [("aegis_6j", 1, 8), ("orb_mnq_v7", 2, 1)])
def test_f2_absent_size_vector_preserves_default_quantities(tmp_path, route, leg_id, source_qty, expected):
    assert_fill(exercise(tmp_path, route, leg_id, source_qty), expected, source_qty)


@pytest.mark.parametrize("route", REASONS)
@pytest.mark.parametrize("tier", ["AUTHORIZED", "RETIRED"])
def test_f3_f5_zero_refusal_has_feedback_without_fill_or_reservation(tmp_path, route, tier):
    vector = validate_size_vector({**VECTOR, "aegis_6j": {
        "base": 0 if tier == "AUTHORIZED" else 3, "adds": "UNCHANGED"}})
    admitted, source, consumer, outcomes = exercise(tmp_path, route, "aegis_6j", 1,
                                                   vector=vector, tier=tier)
    assert admitted == []
    assert source.action.qty == 1
    assert [(e.event, e.detail, e.fill) for e in source.events] == [("reject", REASONS[route], None)]
    if route == "owner":
        assert consumer.synthetic_broker.commands == []
        assert consumer.exposure("aegis_6j") == (0, 0)
        assert len(outcomes) == 1
        assert outcomes[0].quantity == 0 and outcomes[0].attempt_id is None


@pytest.mark.parametrize("route", REASONS)
@pytest.mark.parametrize("source_qty", [1, 2])
def test_f4_vanguard_still_consumes_its_source_ladder(tmp_path, route, source_qty):
    vector = validate_size_vector({**VECTOR, "vanguard_mgc": {
        "base_by_port": {"1": 1, "2": 2}, "adds": "OFF"}})
    assert_fill(exercise(tmp_path, route, "vanguard_mgc", source_qty, vector=vector),
                source_qty, source_qty)


@pytest.mark.parametrize("route", ["adapter", "owner"])
@pytest.mark.parametrize("leg_id,source_qty,reason", [
    ("vanguard_mgc", 3, "vanguard_mgc requires normal_base"),
    ("dj30_mym_p250", 23, "Striker normal_base diagnostic"),
])
def test_f4_invalid_variable_leg_diagnostics_remain_enforced(tmp_path, route, leg_id, source_qty, reason):
    if route == "adapter":
        with pytest.raises(ValueError, match=reason):
            exercise(tmp_path, route, leg_id, source_qty, vector=validate_size_vector(VECTOR))
    else:
        admitted, source, consumer, outcomes = exercise(
            tmp_path, route, leg_id, source_qty, vector=validate_size_vector(VECTOR))
        assert admitted == [] and consumer.exposure(leg_id) == (0, 0)
        assert len(outcomes) == 1 and reason in outcomes[0].refusal_reason
        assert len(source.events) == 1 and source.events[0].event == "reject"


@pytest.mark.parametrize("route", REASONS)
def test_f4_striker_uses_risk_before_floor(tmp_path, route):
    # floor(100 / (24 * .5) * .5) = 4; scaling source qty 5 would give 2.
    assert_fill(exercise(tmp_path, route, "dj30_mym_p250", 5,
                         vector=validate_size_vector(VECTOR)), 4, 5)


@pytest.mark.parametrize("route", REASONS)
def test_f5_protected_aegis_keeps_policy_scaling(tmp_path, route):
    assert_fill(exercise(tmp_path, route, "aegis_6j", 1,
                         vector=validate_size_vector(VECTOR), protected=True), 1, 1)


@pytest.mark.parametrize("leg_id,source_qty", [("aegis_6j", 1), ("orb_mnq_v7", 2)])
def test_f6_explicit_fixed_leg_overrides_still_fail_closed(leg_id, source_qty):
    with pytest.raises(ValueError, match="normal_base must equal fixed quantity"):
        entry_quantities(leg_id, mode=Mode.NORMAL, policy=POLICY, lifecycle_tier="AUTHORIZED",
                         normal_base=source_qty, size=validate_size_vector(VECTOR).leg(leg_id))

class PositiveInt(int):
    """A source-shaped positive integer whose exact type is not int."""


class FixedQuantity(IntEnum):
    ONE = 1
    EIGHT = 8


@pytest.mark.parametrize("leg_id,source_qty", [
    ("aegis_6j", True),
    ("orb_mnq_v7", True),
    ("aegis_6j", PositiveInt(8)),
    ("orb_mnq_v7", PositiveInt(1)),
    ("aegis_6j", FixedQuantity.EIGHT),
    ("orb_mnq_v7", FixedQuantity.ONE),
], ids=["aegis-bool", "orb-bool", "aegis-subclass", "orb-subclass", "aegis-enum", "orb-enum"])
def test_non_exact_fixed_leg_source_is_rejected_before_submission(leg_id, source_qty):
    source = OneEntry(leg_id, entry(leg_id, source_qty, stop=24))
    original = source.action
    spec = ADAPTER_BY_LEG[leg_id]
    consumer = BundleExecution(source, SizingInputs(
        leg_id, Mode.NORMAL, "AUTHORIZED", 80, 100, spec.pointvalue,
        validate_size_vector(VECTOR).leg(leg_id)), policy=POLICY)
    broker = TVBrokerEmulator(leg_id, spec.mintick, spec.pointvalue, 0, 0)
    bar = Bar(NOW, 100, 100, 100, 100)
    with pytest.raises(ValueError, match="normal_base must equal fixed quantity"):
        run_sized_adapter(consumer, [bar], broker)
    assert source.action is original and original.qty is source_qty
    assert consumer.checkpoint()["pending"] == {}
    assert consumer.open_quantity == consumer.confirmed_base == 0
    assert source.events == []
    assert broker.events == []
    assert broker.pending_order_ids() == []
    assert broker.position() == 0
