"""Session history and adapter provenance are prerequisites to dispatch."""
from dataclasses import replace
from datetime import timedelta, timezone
import json
import sqlite3

import pytest

from c1_rail.book_account_owner import AccountOwnerError, BookAccountOwner
from c1_signal_daemon.book_adapters import synthetic_adapter_registry
from c1_signal_daemon.book_protocol import Cancel
from c1_signal_daemon.book_runtime import FourLegRuntime
from c1_signal_daemon.book_protocol import Mode
from c1_signal_daemon.feed import Bar
from test_four_leg_runtime import (
    Adapter, BootstrapBroker, LEGS, NOW, binding, entry, inert_adapters, owner,
)


def complete(runtime, instant=NOW):
    for leg_id in LEGS:
        runtime.on_completed_bar(leg_id, Bar(instant, 100, 101, 99, 100, 10), now=instant)


@pytest.mark.parametrize("offset", [timedelta(minutes=15), timedelta(minutes=1), timedelta(hours=1)])
def test_first_boundary_cannot_skip_session_history(tmp_path, offset):
    account = owner(tmp_path, [])
    runtime = FourLegRuntime(account, inert_adapters())
    instant = account.binding["session"].opens_at + offset
    with pytest.raises(AccountOwnerError, match="noncontiguous"):
        complete(runtime, instant)
    assert account.retained_partial_bars == ()
    assert account.retained_barriers == ()
    assert account.authority == "INTERVENTION"
    assert account.synthetic_broker.commands == []


@pytest.mark.parametrize("bad_time", [None, NOW - timedelta(minutes=15), NOW + timedelta(minutes=15)])
@pytest.mark.parametrize("producer", ["on_bar", "set_mode"])
def test_entire_batch_rejects_order_from_another_boundary(tmp_path, bad_time, producer):
    class BadAdapter(Adapter):
        def set_mode(self, mode):
            super().set_mode(mode)
            return self.actions if producer == "set_mode" else []

        def on_bar(self, bar):
            super().on_bar(bar)
            return self.actions if producer == "on_bar" else []

    account = owner(tmp_path, [])
    values = {leg: Adapter(leg) for leg in LEGS}
    values[LEGS[0]] = Adapter(LEGS[0], [entry(LEGS[0], 1)])
    values[LEGS[-1]] = BadAdapter(LEGS[-1], [replace(entry(LEGS[-1], 1), bar_time=bad_time)])
    runtime = FourLegRuntime(account, synthetic_adapter_registry(values))
    with pytest.raises(AccountOwnerError, match="bar_time"):
        complete(runtime)
    assert account.authority == "INTERVENTION"
    assert account.retained_barriers[0]["actions"] is None
    assert account.observable_accounting()["operations"] == ()
    assert account.synthetic_broker.commands == []
    restarted = BookAccountOwner.boot(account.path, "synthetic-account", binding=binding(),
                                     synthetic_broker=BootstrapBroker([]))
    with pytest.raises(AccountOwnerError, match="incomplete retained"):
        FourLegRuntime.recover(restarted, inert_adapters())
    assert restarted.authority == "INTERVENTION"
    assert restarted.synthetic_broker.commands == []


@pytest.mark.parametrize("action", [entry(LEGS[1], 1), Cancel(LEGS[1])])
def test_adapter_cannot_emit_another_legs_action(tmp_path, action):
    account = owner(tmp_path, [])
    values = {leg: Adapter(leg) for leg in LEGS}
    values[LEGS[0]] = Adapter(LEGS[0], [action])
    runtime = FourLegRuntime(account, synthetic_adapter_registry(values))
    with pytest.raises(AccountOwnerError, match="leg_id"):
        complete(runtime)
    assert account.authority == "INTERVENTION"
    assert account.retained_barriers[0]["actions"] is None
    assert account.synthetic_broker.commands == []


@pytest.mark.parametrize("partial", [False, True])
def test_retained_bar_payload_must_match_its_boundary(tmp_path, partial):
    account = owner(tmp_path, [])
    runtime = FourLegRuntime(account, inert_adapters())
    if partial:
        runtime.on_completed_bar(LEGS[0], Bar(NOW, 100, 101, 99, 100, 10), now=NOW)
    else:
        complete(runtime)
    table = "partial_bars" if partial else "barriers"
    with sqlite3.connect(account.path) as db:
        body = json.loads(db.execute(f"SELECT body FROM {table}").fetchone()[0])
        payload = body if partial else body[LEGS[0]]
        payload["ts"] = (NOW + timedelta(minutes=15)).isoformat()
        db.execute(f"UPDATE {table} SET body=?", (json.dumps(body),))
    with pytest.raises(AccountOwnerError, match="invalid retained bar"):
        FourLegRuntime.recover(account, inert_adapters())
    assert account.authority == "INTERVENTION"
    assert account.synthetic_broker.commands == []


def test_session_open_and_contiguous_history_replay_without_sending(tmp_path):
    account = owner(tmp_path, [])
    runtime = FourLegRuntime(account, inert_adapters())
    complete(runtime)
    complete(runtime, NOW + timedelta(minutes=15))
    restarted = BookAccountOwner.boot(account.path, "synthetic-account", binding=binding(),
                                     synthetic_broker=BootstrapBroker([]))
    recovered = FourLegRuntime.recover(restarted, inert_adapters())
    assert recovered.adapters[LEGS[0]].bars == [NOW.isoformat(), (NOW + timedelta(minutes=15)).isoformat()]
    assert restarted.synthetic_broker.commands == []


@pytest.mark.parametrize("partial", [False, True])
def test_recovery_rejects_retained_history_that_starts_mid_session(tmp_path, partial):
    account = owner(tmp_path, [])
    instant = NOW + timedelta(minutes=15)
    body = dict(ts=instant.isoformat(), open=100, high=101, low=99, close=100, volume=10)
    if partial:
        account.record_partial_bar(LEGS[0], instant, body, acquired_at=instant)
    else:
        for leg in LEGS:
            account.record_partial_bar(leg, instant, body, acquired_at=instant)
        account.record_barrier(instant, {leg: body for leg in LEGS},
                               session_id=account.binding["session"].session_id, mode=Mode.NORMAL)
        account.record_barrier_actions(instant, [])
        account.complete_barrier(instant)
    with pytest.raises(AccountOwnerError, match="noncontiguous"):
        FourLegRuntime.recover(account, inert_adapters())
    assert account.authority == "INTERVENTION"
    assert account.synthetic_broker.commands == []


def test_equivalent_timezone_delivery_cannot_create_another_boundary(tmp_path):
    account = owner(tmp_path, [])
    runtime = FourLegRuntime(account, inert_adapters())
    complete(runtime)
    equivalent = NOW.astimezone(timezone(timedelta(hours=-4)))
    complete(runtime, equivalent)
    assert len(account.retained_barriers) == 1
    assert runtime.adapters[LEGS[0]].bars == [NOW.isoformat()]
    assert account.synthetic_broker.commands == []


def test_recovery_cannot_replay_two_retained_spellings_of_one_instant(tmp_path):
    account = owner(tmp_path, [])
    complete(FourLegRuntime(account, inert_adapters()))
    instant = NOW.astimezone(timezone(timedelta(hours=-4)))
    body = dict(ts=instant.isoformat(), open=100, high=101, low=99, close=100, volume=10)
    for leg in LEGS:
        account.record_partial_bar(leg, instant, body, acquired_at=instant)
    account.record_barrier(instant, {leg: body for leg in LEGS},
                           session_id=account.binding["session"].session_id, mode=Mode.NORMAL)
    account.record_barrier_actions(instant, [])
    account.complete_barrier(instant)
    with pytest.raises(AccountOwnerError, match="noncontiguous"):
        FourLegRuntime.recover(account, inert_adapters())
    assert account.authority == "INTERVENTION"


@pytest.mark.parametrize("offset", [0, -4])
def test_recovery_rejects_partial_at_completed_boundary(tmp_path, offset):
    account = owner(tmp_path, [])
    complete(FourLegRuntime(account, inert_adapters()))
    instant = NOW.astimezone(timezone(timedelta(hours=offset)))
    body = dict(ts=instant.isoformat(), open=100, high=101, low=99, close=100, volume=10)
    account.record_partial_bar(LEGS[0], instant, body, acquired_at=instant)

    with pytest.raises(AccountOwnerError, match="noncontiguous"):
        FourLegRuntime.recover(account, inert_adapters())
    assert account.authority == "INTERVENTION"
    assert account.synthetic_broker.commands == []


@pytest.mark.parametrize("close", [100, 101])
def test_recovery_rejects_duplicate_partial_leg_in_equivalent_timezones(tmp_path, close):
    account = owner(tmp_path, [])
    body = dict(ts=NOW.isoformat(), open=100, high=101, low=99, close=100, volume=10)
    account.record_partial_bar(LEGS[0], NOW, body, acquired_at=NOW)
    equivalent = NOW.astimezone(timezone(timedelta(hours=-4)))
    duplicate = dict(body, ts=equivalent.isoformat(), close=close)
    account.record_partial_bar(LEGS[0], equivalent, duplicate, acquired_at=equivalent)

    with pytest.raises(AccountOwnerError, match="noncontiguous"):
        FourLegRuntime.recover(account, inert_adapters())
    assert account.authority == "INTERVENTION"
    assert account.synthetic_broker.commands == []


def test_recovery_keeps_distinct_partial_legs_and_completes_next_boundary(tmp_path):
    account = owner(tmp_path, [])
    runtime = FourLegRuntime(account, inert_adapters())
    complete(runtime)
    instant = NOW + timedelta(minutes=15)
    equivalent = instant.astimezone(timezone(timedelta(hours=-4)))
    for leg, timestamp in zip(LEGS[:2], (instant, equivalent)):
        runtime.on_completed_bar(leg, Bar(timestamp, 100, 101, 99, 100, 10), now=instant)

    recovered = FourLegRuntime.recover(account, inert_adapters())
    assert recovered.pending_bar_times == (instant,)
    for leg in LEGS[2:]:
        recovered.on_completed_bar(leg, Bar(instant, 100, 101, 99, 100, 10), now=instant)
    complete(recovered, NOW + timedelta(minutes=30))
    assert recovered.pending_bar_times == ()
    assert len(account.retained_barriers) == 3
    assert account.retained_partial_bars == ()
    assert recovered.adapters[LEGS[0]].bars == [
        NOW.isoformat(), instant.isoformat(), (NOW + timedelta(minutes=30)).isoformat()]
    assert account.synthetic_broker.commands == []


@pytest.mark.parametrize("mixed", [False, True])
def test_recovery_rejects_partial_keys_that_cannot_resume_in_utc(tmp_path, mixed):
    account = owner(tmp_path, [])
    equivalent = NOW.astimezone(timezone(timedelta(hours=-4)))
    for leg, instant in zip(LEGS[:2], (NOW if mixed else equivalent, equivalent)):
        body = dict(ts=instant.isoformat(), open=100, high=101, low=99, close=100, volume=10)
        account.record_partial_bar(leg, instant, body, acquired_at=instant)

    with pytest.raises(AccountOwnerError, match="noncontiguous"):
        FourLegRuntime.recover(account, inert_adapters())
    assert account.authority == "INTERVENTION"
    assert account.synthetic_broker.commands == []
