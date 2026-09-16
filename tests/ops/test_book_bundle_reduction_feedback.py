"""Strict sized adapters retire refused reductions through the durable runtime."""
from dataclasses import replace
from datetime import timedelta

import pytest

from c1_rail.book_account_owner import BookAccountOwner
from c1_rail.book_policy import candidate_book_protection_policy
from c1_signal_daemon.book_adapters import synthetic_adapter_registry
from c1_signal_daemon.book_bundle_execution import SizingInputs
from c1_signal_daemon.book_protocol import ExecutionEvent, Mode, Side
from c1_signal_daemon.book_runtime import FourLegRuntime, SimulatedRuntimeCrash
from test_book_runtime_close_feedback import LEG, PlannedAdapter, RuntimeExecution, complete
from test_four_leg_runtime import Adapter, LEGS, NOW, binding, entry, owner
from book_bootstrap_fixtures import BootstrapBroker


class RefusalTrackingAdapter(PlannedAdapter):
    """ORB-style source tracks outstanding entries by their actual identity."""
    def __init__(self, plan):
        super().__init__(plan)
        self.pending_entries = set()

    def on_bar(self, bar):
        from c1_signal_daemon.book_protocol import OrderIntent
        actions = super().on_bar(bar)
        self.pending_entries.update(action.order_id for action in actions
            if isinstance(action, OrderIntent) and action.kind in ("entry", "add"))
        return actions

    def on_execution(self, event):
        if event.event in ("cancel", "reject"):
            self.pending_entries.discard(event.order_id)
        super().on_execution(event)


def registry(action):
    source = RefusalTrackingAdapter({NOW: [action]})
    execution = RuntimeExecution(source, SizingInputs(
        LEG, Mode.PROTECTED, "AUTHORIZED", 80, 100, .5),
        policy=candidate_book_protection_policy())
    values = {leg: Adapter(leg) for leg in LEGS}
    values[LEG] = execution
    return synthetic_adapter_registry(values), source, execution


@pytest.mark.parametrize("kind,qty,scope,reason", [
    ("flat", None, None, "zero_exposure"),
    ("exit", 1, None, "close_exceeds_confirmed_exposure"),
    ("exit", 1, ("missing",), "unknown_close_scope"),
])
@pytest.mark.parametrize("crash", [False, True])
def test_local_reduction_refusal_reaches_strict_adapter_and_replays(
        tmp_path, kind, qty, scope, reason, crash):
    action = replace(entry(LEG, 1), order_id="reduce", kind=kind,
                     side=Side.SELL, qty=qty, scope_fill_ids=scope)
    account = owner(tmp_path, [], protected=True)
    adapters, source, execution = registry(action)
    runtime = FourLegRuntime(account, adapters, crash_after_dispatch=crash)
    if crash:
        with pytest.raises(SimulatedRuntimeCrash):
            complete(runtime, NOW)
    else:
        assert complete(runtime, NOW)[0].refusal_reason == reason
        assert source.events == [("reject", "reduce", None)]
        assert account.pending_feedback == ()
        assert account.retained_barriers[0]["completed"]
        with pytest.raises(ValueError, match="unknown_terminal_order"):
            execution.on_execution(ExecutionEvent("reject", LEG, NOW, order_id="reduce"))
    restarted = BookAccountOwner.boot(
        tmp_path / "owner.sqlite", "synthetic-account", binding=binding(protected=True),
        synthetic_broker=BootstrapBroker([]))
    fresh, recovered_source, recovered_execution = registry(action)
    FourLegRuntime.recover(restarted, fresh)
    assert recovered_source.events == [("reject", "reduce", None)]
    assert restarted.pending_feedback == ()
    assert restarted.synthetic_broker.commands == []
    assert recovered_execution.open_quantity == recovered_execution.confirmed_base == 0
    with pytest.raises(ValueError, match="unknown_terminal_order"):
        recovered_execution.on_execution(ExecutionEvent("reject", LEG, NOW, order_id="unseen"))


@pytest.mark.parametrize("terminal", ["reject", "cancel"])
def test_partial_reduction_terminal_preserves_confirmed_exposure(terminal):
    from test_book_bundle_execution import Source, owner as sized, intent, event
    from c1_signal_daemon.feed import Bar
    source = Source()
    execution = sized(source)
    bar = Bar(NOW, 100, 101, 99, 100)
    execution.admit([intent()], bar)
    execution.on_execution(event("base-fill", "base", "entry", 3))
    execution.admit([replace(intent("exit", 2, "reduce"), side=Side.SELL)], bar)
    execution.on_execution(event("partial", "reduce", "exit", 1, "base-fill"))
    execution.on_execution(ExecutionEvent(terminal, LEG, NOW, order_id="reduce"))
    assert execution.open_quantity == 2
    assert execution.confirmed_base == 3
    assert source.events[-1].event == terminal
    with pytest.raises(ValueError, match="unknown_terminal_order"):
        execution.on_execution(ExecutionEvent(terminal, LEG, NOW, order_id="reduce"))


def test_fully_filled_reduction_cannot_receive_another_terminal():
    from test_book_bundle_execution import Source, owner as sized, intent, event
    from c1_signal_daemon.feed import Bar
    execution = sized(Source())
    bar = Bar(NOW, 100, 101, 99, 100)
    execution.admit([intent()], bar)
    execution.on_execution(event("base-fill", "base", "entry", 3))
    execution.admit([replace(intent("flat", None, "reduce"), side=Side.SELL)], bar)
    execution.on_execution(event("full", "reduce", "flat", 3, "base-fill"))
    assert execution.confirmed_base == execution.open_quantity == 0
    with pytest.raises(ValueError, match="unknown_terminal_order"):
        execution.on_execution(ExecutionEvent("reject", LEG, NOW, order_id="reduce"))


@pytest.mark.parametrize("scoped", [True, False])
def test_queued_quantityless_flat_retires_when_actual_scope_is_exhausted(scoped):
    from test_book_bundle_execution import Source, owner as sized, intent, event
    from c1_signal_daemon.feed import Bar
    execution = sized(Source())
    bar = Bar(NOW, 100, 101, 99, 100)
    execution.admit([intent()], bar)
    execution.on_execution(event("first-lot", "base", "entry", 2))
    execution.on_execution(event("sibling-lot", "base", "entry", 1))
    flat = replace(intent("flat", None, "flat"), side=Side.SELL,
                   scope_fill_ids=("first-lot",) if scoped else None)
    earlier = replace(intent("exit", 1, "earlier"), side=Side.SELL,
                      scope_fill_ids=("first-lot",))
    later = replace(flat, order_id="queued")
    execution.admit([earlier, flat, later], bar)
    execution.on_execution(event("earlier-fill", "earlier", "exit", 1, "first-lot"))
    execution.on_execution(event("flat-fill", "flat", "flat", 1, "first-lot"))
    if not scoped:
        execution.on_execution(event("sibling-flat", "flat", "flat", 1, "sibling-lot"))
    assert execution.open_quantity == (1 if scoped else 0)
    with pytest.raises(ValueError, match="unknown_terminal_order"):
        execution.on_execution(ExecutionEvent("reject", LEG, NOW, order_id="flat"))
    # Exhausting another operation's scope does not acknowledge this queued ID.
    execution.on_execution(ExecutionEvent("reject", LEG, NOW, order_id="queued"))
    with pytest.raises(ValueError, match="unknown_terminal_order"):
        execution.on_execution(ExecutionEvent("reject", LEG, NOW, order_id="queued"))


@pytest.mark.parametrize("control", ["cancel", "cancel_all", "amend"])
@pytest.mark.parametrize("strict", [True, False])
def test_control_refusal_preserves_live_entry_and_replays(tmp_path, control, strict):
    from c1_rail.book_account_owner import BrokerResult
    from c1_signal_daemon.book_protocol import Bracket, BracketAmend, Cancel
    later = NOW + timedelta(minutes=15)
    opening = entry(LEG, 5, stop=24)
    action = (BracketAmend(LEG, Bracket(stop=98)) if control == "amend"
              else Cancel(LEG, opening.order_id if control == "cancel" else None))
    def fresh():
        values, source, execution = registry(opening)
        source.plan[later] = [action, action]
        if not strict:
            values = synthetic_adapter_registry({leg: source if leg == LEG else values[leg]
                                                 for leg in LEGS})
        return values, source, execution
    account = owner(tmp_path, [BrokerResult("accepted")], protected=True)
    values, source, execution = fresh()
    runtime = FourLegRuntime(account, values)
    complete(runtime, NOW)
    pending = execution.checkpoint()["pending"]
    assert pending == ({opening.order_id: ("entry", 3)} if strict else {})
    account.halt("test-control", "operator", now=later)
    results = complete(runtime, later)
    assert all(result.refusal_reason == "intervention_fence" for result in results)
    assert execution.checkpoint()["pending"] == pending
    assert source.pending_entries == {opening.order_id}
    assert source.events and all(event[0] == "reject" for event in source.events)
    assert account.pending_feedback == ()
    assert account.retained_barriers[-1]["completed"]
    count = len(source.events)
    restarted = BookAccountOwner.boot(account.path, account.account,
        binding=binding(protected=True), synthetic_broker=BootstrapBroker([]))
    values, recovered_source, recovered_execution = fresh()
    FourLegRuntime.recover(restarted, values)
    assert len(recovered_source.events) == count
    assert recovered_execution.checkpoint()["pending"] == pending
    assert recovered_source.pending_entries == {opening.order_id}
    assert restarted.pending_feedback == ()
    assert restarted.synthetic_broker.commands == []


@pytest.mark.parametrize("delivery", ["transport", "async", "crash"])
def test_broker_cancel_refusal_preserves_target_and_replays(tmp_path, delivery):
    from c1_rail.book_account_owner import BrokerFact, BrokerResult
    from c1_signal_daemon.book_protocol import Cancel
    later = NOW + timedelta(minutes=15)
    opening = entry(LEG, 5, stop=24)
    def fresh():
        values, source, execution = registry(opening)
        source.plan[later] = [Cancel(LEG, opening.order_id)]
        return values, source, execution
    account = owner(tmp_path, [BrokerResult("accepted"), BrokerResult(
        "accepted" if delivery == "async" else "rejected")], protected=True)
    values, source, execution = fresh()
    runtime = FourLegRuntime(account, values)
    complete(runtime, NOW)
    pending = execution.checkpoint()["pending"]
    runtime.crash_after_dispatch = delivery == "crash"
    if delivery == "crash":
        with pytest.raises(SimulatedRuntimeCrash):
            complete(runtime, later)
    else:
        result = complete(runtime, later)[0]
        if delivery == "async":
            fact = BrokerFact.terminal(result.operation_id, "rejected", 0, later)
            assert len(runtime.observe_fact(fact, now=later)) == 1
            assert runtime.observe_fact(fact, now=later) == ()
        assert execution.checkpoint()["pending"] == pending
        assert len(source.events) == 1 and source.events[0][0] == "reject"
        assert account.pending_feedback == ()
    restarted = BookAccountOwner.boot(account.path, account.account,
        binding=binding(protected=True), synthetic_broker=BootstrapBroker([]))
    values, recovered_source, recovered_execution = fresh()
    FourLegRuntime.recover(restarted, values)
    assert len(recovered_source.events) == 1
    assert recovered_execution.checkpoint()["pending"] == pending
    assert restarted.pending_feedback == ()
    assert restarted.synthetic_broker.commands == []
