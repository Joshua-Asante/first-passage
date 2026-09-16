"""Regression sequences for PR 409's durable execution contract."""
from dataclasses import replace
from datetime import timedelta

import pytest

from c1_rail.book_account_owner import BookAccountOwner, BrokerFact, BrokerResult, SyntheticBroker
from c1_signal_daemon.book_protocol import Cancel, Mode, OrderIntent, Side
from c1_signal_daemon.book_runtime import FourLegRuntime
from test_book_account_owner import NOW, SESSION, binding, intent, owner
from test_four_leg_runtime import (
    inert_adapters, entry, owner as normal_owner, binding as normal_binding,
)


def filled_owner(tmp_path):
    return owner(tmp_path, [BrokerResult("accepted", (
        BrokerFact.fill("base-fill", "base", "dj30_mym_p250", "entry", 3, 100, NOW),
        BrokerFact.terminal("base", "filled", 3, NOW),
    ))])


def test_scheduled_close_survives_ticks_and_partial_terminal(tmp_path):
    account, route = filled_owner(tmp_path)
    account.dispatch(intent(), now=NOW)
    start = SESSION.flatten_start
    account.advance_schedule(now=start)
    first = route.commands[-1]
    account.advance_schedule(now=start + timedelta(seconds=1))
    assert account.authority == "SCHEDULED_EXIT"
    assert len(route.commands) == 2
    account.observe(BrokerFact.fill("partial-flat", first.operation_id,
        "dj30_mym_p250", "flat", 1, 100, start + timedelta(seconds=2),
        entry_execution_id="base-fill"), now=start + timedelta(seconds=2))
    account.advance_schedule(now=start + timedelta(seconds=3))
    assert account.authority == "SCHEDULED_EXIT"
    assert len(route.commands) == 2
    account.observe(BrokerFact.terminal(first.operation_id, "cancelled", 1,
        start + timedelta(seconds=4)), now=start + timedelta(seconds=4))
    account.advance_schedule(now=start + timedelta(seconds=5))
    remainder = route.commands[-1]
    assert remainder.operation_id != first.operation_id
    assert remainder.quantity == 2
    account.advance_schedule(now=start + timedelta(seconds=6))
    assert len(route.commands) == 3
    account.observe(BrokerFact.fill("remaining-flat", remainder.operation_id,
        "dj30_mym_p250", "flat", 2, 100, start + timedelta(seconds=7),
        entry_execution_id="base-fill"), now=start + timedelta(seconds=7))
    account.advance_schedule(now=start + timedelta(seconds=8))
    assert account.exposure("dj30_mym_p250") == (0, 0)
    assert account.authority == "SCHEDULED_EXIT"


@pytest.mark.parametrize("reenter", [False, True])
def test_add_uses_remaining_current_base(tmp_path, reenter):
    account, route = filled_owner(tmp_path)
    account.dispatch(intent(), now=NOW)
    close_qty = 3 if reenter else 2
    route.queue(BrokerResult("accepted", (BrokerFact.fill("close-fill", "close",
        "dj30_mym_p250", "exit", close_qty, 100, NOW,
        entry_execution_id="base-fill"),)))
    account.dispatch(replace(intent("close", kind="exit", qty=close_qty),
        side=Side.SELL), now=NOW)
    if reenter:
        route.queue(BrokerResult("accepted", (
            BrokerFact.fill("new-fill", "new", "dj30_mym_p250", "entry", 1, 100, NOW),
            BrokerFact.terminal("new", "cancelled", 1, NOW),
        )))
        account.dispatch(intent("new"), now=NOW)
    result = account.dispatch(intent("add-current", kind="add"), now=NOW)
    assert result.refusal_reason is None
    assert result.quantity == 2  # Striker rounds 1.5 times the remaining base upward.
    assert route.commands[-1].operation_id == "add-current"


@pytest.mark.parametrize("kind", ["entry", "add", "exit", "flat"])
@pytest.mark.parametrize("leg_id", ["dj30_mym_p250", "aegis_6j"])
def test_wrong_side_never_reserves_or_sends(tmp_path, kind, leg_id):
    account, route = owner(tmp_path, [])
    before = account.observable_accounting()
    expected = Side.SELL if leg_id == "aegis_6j" else Side.BUY
    wrong = (Side.BUY if expected is Side.SELL else Side.SELL) if kind in (
        "entry", "add") else expected
    result = account.dispatch(replace(intent(kind=kind), leg_id=leg_id, side=wrong), now=NOW)
    assert result.refusal_reason == "order_side_mismatch"
    assert route.commands == []
    assert account.observable_accounting() == before


@pytest.mark.parametrize("target", ["missing", "other-leg", "terminal", "close"])
def test_invalid_cancel_target_never_sends(tmp_path, target):
    account, route = filled_owner(tmp_path)
    account.dispatch(intent(), now=NOW)
    if target == "other-leg":
        account.dispatch(OrderIntent("orb", "orb_mnq_v7", "entry", Side.BUY, 1), now=NOW)
        target_id = "orb"
    elif target == "close":
        account.dispatch(replace(intent("close", kind="exit", qty=1), side=Side.SELL), now=NOW)
        target_id = "close"
    else:
        target_id = {"missing": "missing", "terminal": "base"}[target]
    count = len(route.commands)
    result = account.dispatch(Cancel("dj30_mym_p250", target_id), now=NOW)
    assert result.refusal_reason == "invalid_cancel_target"
    assert len(route.commands) == count


def test_cancel_all_expands_only_pending_targets_of_its_leg(tmp_path):
    account, route = owner(tmp_path, [])
    account.dispatch(intent(), now=NOW)
    account.dispatch(OrderIntent("orb", "orb_mnq_v7", "entry", Side.BUY, 1), now=NOW)
    result = account.dispatch(Cancel("orb_mnq_v7"), now=NOW)
    assert result.refusal_reason is None
    assert route.commands[-1].kind == "cancel"
    assert route.commands[-1].target_operation_id == "orb"
    assert route.commands[-1].leg_id == "orb_mnq_v7"
    count = len(route.commands)
    account.dispatch(Cancel("orb_mnq_v7"), now=NOW)
    assert len(route.commands) == count
    account.observe(BrokerFact.terminal("orb", "cancelled", 0, NOW), now=NOW)
    account.dispatch(Cancel("orb_mnq_v7"), now=NOW)
    assert len(route.commands) == count
    assert account.exposure("dj30_mym_p250") == (0, 3)


def test_async_takeover_completes_and_sends_retained_aegis_once(tmp_path):
    account = normal_owner(tmp_path, [])
    adapters = inert_adapters()
    runtime = FourLegRuntime(account, adapters)
    runtime._mode_actions(Mode.NORMAL)
    runtime.deliver_confirmed(account.dispatch(entry("orb_mnq_v7", 1), now=NOW))
    runtime.observe_fact(BrokerFact.fill("orb-fill", "entry:orb_mnq_v7",
        "orb_mnq_v7", "entry", 1, 100, NOW), now=NOW)
    aegis = entry("aegis_6j", 8)
    assert account.dispatch(aegis, now=NOW).refusal_reason == "takeover_pending"
    controls, done = account.advance_takeover(now=NOW)
    assert not done
    for result in controls:
        runtime.deliver_confirmed(result)
    route = account.synthetic_broker
    flat = next(c for c in route.commands if c.kind == "flat")
    # Cancellation arrives first: the already pending close must not be rebuilt.
    runtime.observe_fact(BrokerFact.terminal("entry:orb_mnq_v7", "filled", 1,
        NOW + timedelta(seconds=1)), now=NOW + timedelta(seconds=1))
    assert account.authority == "NORMAL"
    assert len([c for c in route.commands if c.kind == "flat"]) == 1
    fact = BrokerFact.fill("orb-close", flat.operation_id, "orb_mnq_v7", "flat",
        1, 100, NOW + timedelta(seconds=2), entry_execution_id="orb-fill")
    runtime.observe_fact(fact, now=NOW + timedelta(seconds=2))
    runtime.observe_fact(fact, now=NOW + timedelta(seconds=3))
    assert [c.operation_id for c in route.commands].count(aegis.order_id) == 1
    assert account.exposure("aegis_6j") == (0, 8)
    assert account.exposure("orb_mnq_v7") == (0, 0)
    assert account.authority == "NORMAL"
    assert account.pending_feedback == ()


@pytest.mark.parametrize("transport", ["accepted", "unknown"])
def test_async_cancel_terminal_resolves_control_attempt(tmp_path, transport):
    account, route = owner(tmp_path, [BrokerResult(transport), BrokerResult(transport)])
    account.dispatch(intent(), now=NOW)
    cancel = account.dispatch(Cancel("dj30_mym_p250", "base"), now=NOW)
    assert cancel.attempt_id in account.unresolved_attempts
    assert route.commands[-1].target_operation_id == "base"
    account.observe(BrokerFact.terminal("base", "cancelled", 0, NOW), now=NOW)
    assert account.unresolved_attempts == ()
    account.advance_schedule(now=SESSION.own_flat_deadline)
    assert account.authority == "SCHEDULED_EXIT"


def test_scheduled_flatten_handles_late_entry_fill(tmp_path):
    account, route = owner(tmp_path, [])
    account.dispatch(intent(), now=NOW)
    start = SESSION.flatten_start
    account.advance_schedule(now=start)
    account.observe(BrokerFact.fill("late-one", "base", "dj30_mym_p250", "entry",
        1, 100, start), now=start)
    account.advance_schedule(now=start)
    first = route.commands[-1]
    account.observe(BrokerFact.fill("close-one", first.operation_id, "dj30_mym_p250",
        "flat", 1, 100, start, entry_execution_id="late-one"), now=start)
    account.observe(BrokerFact.fill("late-two", "base", "dj30_mym_p250", "entry",
        2, 100, start), now=start)
    account.advance_schedule(now=start + timedelta(seconds=1))
    assert route.commands[-1].operation_id != first.operation_id
    assert route.commands[-1].quantity == 2
    assert account.authority == "SCHEDULED_EXIT"


def test_restart_does_not_resend_retained_scheduled_close(tmp_path):
    account, route = filled_owner(tmp_path)
    account.dispatch(intent(), now=NOW)
    account.advance_schedule(now=SESSION.flatten_start)
    restarted = BookAccountOwner.boot(account.path, account.account, binding=binding(),
        synthetic_broker=route)
    restarted.advance_schedule(now=SESSION.flatten_start + timedelta(seconds=1))
    restarted.resume_takeover(now=SESSION.flatten_start + timedelta(seconds=1))
    assert restarted.authority == "INTERVENTION"
    assert len(route.commands) == 2


@pytest.mark.parametrize("expired", ["age", "valid_until"])
def test_ready_takeover_rechecks_evidence_freshness(tmp_path, expired):
    bound = normal_binding()
    if expired == "valid_until":
        bound["max_evidence_age"] = timedelta(hours=1)
    account = BookAccountOwner.boot(tmp_path / "owner.sqlite", "synthetic-account",
                                   binding=bound, synthetic_broker=SyntheticBroker([]))
    account.activate_synthetic(now=NOW)
    account.dispatch(entry("orb_mnq_v7", 1), now=NOW)
    aegis = entry("aegis_6j", 8)
    assert account.dispatch(aegis, now=NOW).refusal_reason == "takeover_pending"
    late = NOW + timedelta(seconds=31) if expired == "age" else account.binding["valid_until"]
    account.observe(BrokerFact.terminal("entry:orb_mnq_v7", "cancelled", 0, late), now=late)
    account.resume_takeover(now=late)
    assert not any(c.operation_id == aegis.order_id for c in account.synthetic_broker.commands)


@pytest.mark.parametrize("status,cumulative", [("accepted", 1), ("filled", 1), ("cancelled", True)])
def test_invalid_close_terminal_cannot_release_a_flatten_remainder(tmp_path, status, cumulative):
    account, route = filled_owner(tmp_path)
    account.dispatch(intent(), now=NOW)
    start = SESSION.flatten_start
    account.advance_schedule(now=start)
    close_id = route.commands[-1].operation_id
    account.observe(BrokerFact.fill("partial", close_id, "dj30_mym_p250", "flat", 1,
        100, start, entry_execution_id="base-fill"), now=start)
    account.observe(BrokerFact.terminal(close_id, status, cumulative, start), now=start)
    account.advance_schedule(now=start + timedelta(seconds=1))
    assert account.authority == "INTERVENTION"
    assert len(route.commands) == 2
    assert account.exposure("dj30_mym_p250") == (2, 0)
