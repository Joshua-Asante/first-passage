"""Listener callbacks deliver reconciled outcomes through real runtime checkpoints."""
from dataclasses import replace
from datetime import timedelta

import pytest

from c1_rail.book_account_owner import BrokerFact, BrokerResult
from c1_rail.book_policy import candidate_book_protection_policy
from c1_rail.book_protection import ProtectionRead
from c1_rail.c1_rail_listener import handle_book_fact, handle_book_protection
from c1_signal_daemon.book_adapters import synthetic_adapter_registry
from c1_signal_daemon.book_bundle_execution import BundleExecution, SizingInputs
from c1_signal_daemon.book_protocol import Bracket, Mode, Side
from c1_signal_daemon.book_runtime import FourLegRuntime
from c1_signal_daemon.feed import Bar
from test_four_leg_runtime import Adapter, LEGS, NOW, entry, owner


LEG = "dj30_mym_p250"
LATER = NOW + timedelta(minutes=15)


class PlannedAdapter(Adapter):
    def __init__(self, plan):
        super().__init__(LEG)
        self.plan = plan

    def on_bar(self, bar):
        super().on_bar(bar)
        return self.plan.get(bar.ts, [])


class RuntimeExecution(BundleExecution):
    """Expose mode notification while retaining the real strict fill reducer."""
    def set_mode(self, mode):
        assert mode == self.inputs.mode
        return self.adapter.set_mode(mode)


def complete(runtime, instant):
    for leg in LEGS:
        result = runtime.on_completed_bar(leg, Bar(instant, 100, 101, 99, 100, 10), now=instant)
    return result


def setup_runtime(tmp_path, *, protected=False, closes=(), strict=False):
    account = owner(tmp_path, [BrokerResult("accepted")], protected=True)
    action = replace(entry(LEG, 5, stop=24), bracket=Bracket(stop=98) if protected else None)
    source = PlannedAdapter({NOW: [action], LATER: list(closes)})
    adapter = source
    if strict:
        adapter = RuntimeExecution(source, SizingInputs(LEG, Mode.PROTECTED, "AUTHORIZED", 80, 100, .5),
                                   policy=candidate_book_protection_policy())
    values = {leg: Adapter(leg) for leg in LEGS}
    values[LEG] = adapter
    runtime = FourLegRuntime(account, synthetic_adapter_registry(values))
    result = complete(runtime, NOW)
    assert result[0].quantity == 3
    at = NOW + timedelta(milliseconds=100)
    fact = account.synthetic_broker.execute_entry(action.order_id, fill_id="base-fill", quantity=3,
                                                  price=100, at=at)
    handle_book_fact(fact, account, runtime, now=at)
    return account, account.synthetic_broker, runtime, source, adapter


def snapshot(account, broker, *, at):
    broker.advance(at)
    return broker.read_protection(ProtectionRead(account.make_occurrence("direct", "snapshot"),
                                                 (LEG,), at - timedelta(milliseconds=1)))


def close(identity, *, quantity=1):
    return replace(entry(LEG, quantity, stop=24), order_id=identity, kind="exit", side=Side.SELL,
                   qty=quantity, scope_fill_ids=("base-fill",), bar_time=LATER)


def test_filled_entry_terminal_does_not_cancel_real_strict_adapter(tmp_path):
    account, broker, runtime, source, execution = setup_runtime(tmp_path, strict=True)
    before = account.all_feedback
    terminal = BrokerFact.terminal("entry:" + LEG, "filled", 3, broker.now)
    assert handle_book_fact(terminal, account, runtime, now=broker.now) == ()
    assert execution.open_quantity == 3
    assert execution.checkpoint()["pending"] == {}
    assert source.events == [("fill", "entry:" + LEG, "base-fill")]
    assert account.all_feedback == before
    assert account.pending_feedback == ()
    assert before[0]["delivered"]
    assert before[0]["checkpoint"]["open_quantity"] == 3


@pytest.mark.parametrize("quantity", [1, 3])
def test_listener_delivers_protected_close_only_after_residual_snapshot(tmp_path, quantity):
    account, broker, runtime, source, execution = setup_runtime(
        tmp_path, protected=True, closes=(close("close", quantity=quantity),), strict=True)
    before_close = snapshot(account, broker, at=LATER)
    handle_book_protection(before_close, account, runtime, now=LATER)
    broker.queue(BrokerResult("accepted"))
    assert complete(runtime, LATER)[0].transport_state == "accepted"
    at = LATER + timedelta(milliseconds=100)
    facts = broker.execute_close("close", execution_id="closed", quantity=quantity,
                                 price=100, terminal=True, at=at)
    for fact in facts:
        assert handle_book_fact(fact, account, runtime, now=at) == ()
    assert execution.open_quantity == 3
    assert account.exposure(LEG) == (3 - quantity, 0)
    assert len(source.events) == 1
    assert account.pending_feedback == ()
    before = tuple(account.all_feedback)
    assert handle_book_protection(before_close, account, runtime, now=at) == ()
    assert execution.open_quantity == 3
    assert tuple(account.all_feedback) == before
    at += timedelta(milliseconds=100)
    residual = snapshot(account, broker, at=at)
    released = handle_book_protection(residual, account, runtime, now=at)
    assert len(released) == 1 and released[0].event == "fill"
    assert execution.open_quantity == 3 - quantity
    assert len(source.events) == 2
    assert len(account.all_feedback) == len(before) + 1
    assert account.all_feedback[-1]["delivered"]
    assert account.all_feedback[-1]["checkpoint"]["open_quantity"] == 3 - quantity
    assert account.pending_feedback == ()
    assert handle_book_protection(residual, account, runtime, now=at) == ()
    assert len(source.events) == 2


@pytest.mark.parametrize("callback", ["fact", "protection", "schedule"])
def test_queued_close_resumes_through_runtime_callbacks_without_transient_reject(tmp_path, callback):
    account, broker, runtime, source, _ = setup_runtime(
        tmp_path, protected=callback == "protection", closes=(close("first"), close("second")))
    handle_book_protection(snapshot(account, broker, at=LATER), account, runtime, now=LATER)
    broker.queue(BrokerResult("accepted"))
    results = complete(runtime, LATER)
    assert [result.refusal_reason for result in results] == [None, "close_pending"]
    assert [command.operation_id for command in broker.commands] == ["entry:" + LEG, "first"]
    assert all(event[0] != "reject" for event in source.events)
    at = LATER + timedelta(milliseconds=100)
    broker.queue(BrokerResult("accepted"))
    if callback == "protection":
        for fact in broker.execute_close("first", execution_id="first-fill", quantity=1,
                                         price=100, terminal=True, at=at):
            handle_book_fact(fact, account, runtime, now=at)
        assert len(broker.commands) == 2
        at += timedelta(milliseconds=100)
        handle_book_protection(snapshot(account, broker, at=at), account, runtime, now=at)
    else:
        fact = BrokerFact.terminal("first", "cancelled", 0, at)
        if callback == "fact":
            handle_book_fact(fact, account, runtime, now=at)
        else:
            events = account.observe(fact, now=at)
            runtime.deliver_confirmed_events(events)
            runtime.advance_schedule(now=at)
    assert [command.operation_id for command in broker.commands] == ["entry:" + LEG, "first", "second"]
    assert broker.commands[-1].quantity == 1
    assert all(event[0] != "reject" for event in source.events)
    assert account.pending_feedback == ()
    runtime.advance_schedule(now=at)
    assert len(broker.commands) == 3
