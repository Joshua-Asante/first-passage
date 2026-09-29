"""CC-3: an ordinary unknown transport outcome is an incident that durably ends automation.

Card: docs/briefs/handoffs/2026-09-29-cc3-ordinary-unknown-halt.md; halt/resume §2 `:26`,
incident ADR §A11.2. Every case runs against the existing owner and synthetic route in a
disposable ``tmp_path`` store. Evidence class: synthetic / replay engineering. No real broker
producer, adapter, same-session restart or later-session resume is exercised here.
"""
from __future__ import annotations

from dataclasses import replace
from datetime import timedelta
import json
import sqlite3
from types import SimpleNamespace
import threading

import pytest

from c1_rail.book_account_owner import (
    AccountOwnerError,
    BookAccountOwner,
    BrokerFact,
    BrokerResult,
)
from c1_signal_daemon.book_protocol import Cancel, OrderIntent, Side
from book_bootstrap_fixtures import BootstrapBroker
from test_book_account_owner import NOW, binding, intent, owner

LEG = "dj30_mym_p250"
KINDS = ("entry", "add", "close", "cancel")
FILLED = BrokerFact.fill("execution-1", "base", LEG, "entry", 2, 100.0, NOW)
CANCELLED = BrokerFact.terminal("base", "cancelled", 2, NOW)
LATER = NOW + timedelta(seconds=1)


def _dispatch(account, action, event, at=LATER):
    return account.dispatch(action, occurrence=account.make_occurrence("direct", event), now=at)


def _incident_ids(account):
    return tuple(row["incident_id"] for row in account.incidents)


def _bootstrap(account):
    with sqlite3.connect(account.path) as db:
        return json.loads(db.execute("SELECT body FROM bootstrap_identity").fetchone()[0])


def _other_leg_entry(order_id):
    return OrderIntent(order_id, "orb_mnq_v7", "entry", Side.BUY, 1, bar_time=NOW)


def _scenario(tmp_path, kind):
    """A live, activated owner and the ordinary action of ``kind`` whose send comes next."""
    prior = {
        "entry": [],
        "add": [BrokerResult("accepted", (FILLED, CANCELLED))],
        "close": [BrokerResult("accepted", (FILLED, CANCELLED))],
        "cancel": [BrokerResult("accepted")],
    }[kind]
    account, route = owner(tmp_path, prior)
    if prior:
        assert _dispatch(account, intent(), "base", NOW).transport_state == "accepted"
    action = {
        "entry": intent(),
        "add": intent("add-1", kind="add", qty=12),
        "close": OrderIntent("exit-1", LEG, "exit", Side.SELL, 2,
                             scope_fill_ids=("execution-1",), bar_time=NOW),
        "cancel": Cancel(LEG, "base"),
    }[kind]
    assert (account.permission, account.authority) == ("RUNNING", "NORMAL")
    return account, route, action


def _assert_unknown_incident(account, route, sent, *, commands, unresolved=True):
    assert sent.transport_state == "unknown"
    assert (sent.attempt_id in account.unresolved_attempts) is unresolved
    assert (account.permission, account.authority) == ("HALTED", "INTERVENTION")
    assert _incident_ids(account) == ("ordinary-unknown:" + sent.attempt_id,)
    assert account.incidents[0]["reason"] == "execution"
    assert _bootstrap(account)["state"] == "ineligible"
    assert _bootstrap(account)["invalidation"] == "incident:ordinary-unknown:" + sent.attempt_id
    assert len(route.commands) == commands


@pytest.mark.parametrize("kind", KINDS)
def test_unknown_result_halts_before_return(tmp_path, kind):
    account, route, action = _scenario(tmp_path, kind)
    before = account.status()["generation"]
    exposure = account.exposure(LEG)
    route.queue(BrokerResult("unknown"))

    sent = _dispatch(account, action, kind + "-unknown")

    _assert_unknown_incident(account, route, sent, commands=len(route.commands))
    assert route.commands[-1].operation_id == sent.operation_id
    assert account.status()["generation"] == before + 1
    if kind in ("entry", "add"):
        assert account.exposure(LEG)[1] >= exposure[1]  # the reservation is retained
    else:
        assert account.exposure(LEG) == exposure
    sends = len(route.commands)
    fenced = _dispatch(account, _other_leg_entry("after-" + kind), "after-" + kind)
    assert fenced.refusal_reason == "intervention_fence"
    assert len(route.commands) == sends


@pytest.mark.parametrize("kind", KINDS)
def test_send_exception_halts_and_retains_attempt(tmp_path, kind):
    account, route, action = _scenario(tmp_path, kind)
    before = account.status()["generation"]
    delegate = route.send

    def lost(command):
        delegate(command)  # bytes may have left before the transport failed
        raise ConnectionError("response lost")

    route.queue(BrokerResult("accepted"))
    route.send = lost
    sent = _dispatch(account, action, kind + "-exception")

    _assert_unknown_incident(account, route, sent, commands=len(route.commands))
    assert account.status()["generation"] == before + 1
    with sqlite3.connect(account.path) as db:
        state, observation = db.execute(
            "SELECT state, observation FROM attempts WHERE attempt_id=?", (sent.attempt_id,)).fetchone()
    assert state == "UNKNOWN" and json.loads(observation) == {"state": "unknown", "facts": []}
    route.send = delegate
    sends = len(route.commands)
    assert _dispatch(account, _other_leg_entry("after-exc"), "after-exc").refusal_reason == "intervention_fence"
    assert len(route.commands) == sends


def test_terminal_or_fill_after_unknown_never_resumes(tmp_path):
    # Facts attached to the unknown result settle the obligation but leave the incident.
    account, route, action = _scenario(tmp_path, "entry")
    route.queue(BrokerResult("unknown", (FILLED, CANCELLED)))
    sent = _dispatch(account, action, "attached")
    _assert_unknown_incident(account, route, sent, commands=1, unresolved=False)
    assert [event.fill.qty for event in sent.confirmed_events if event.fill] == [2]
    assert account.exposure(LEG) == (2, 0)
    assert account.unresolved_attempts == ()
    generation = account.status()["generation"]
    assert _dispatch(account, _other_leg_entry("after-attached"), "after-attached").refusal_reason \
        == "intervention_fence"
    assert account.status()["generation"] == generation
    assert len(route.commands) == 1

    # Facts observed after the unknown result reconcile the same way.
    later, later_route, later_action = _scenario(tmp_path / "later", "entry")
    later_route.queue(BrokerResult("unknown"))
    sent = _dispatch(later, later_action, "unknown-only")
    assert later.unresolved_attempts == (sent.attempt_id,)
    generation = later.status()["generation"]
    later.observe(FILLED, now=LATER)
    later.observe(CANCELLED, now=LATER)
    assert later.exposure(LEG) == (2, 0)
    assert later.unresolved_attempts == ()
    assert (later.permission, later.authority) == ("HALTED", "INTERVENTION")
    assert later.status()["generation"] == generation
    assert _incident_ids(later) == ("ordinary-unknown:" + sent.attempt_id,)
    assert _bootstrap(later)["invalidation"] == "incident:ordinary-unknown:" + sent.attempt_id
    at = LATER + timedelta(seconds=1)
    assert _dispatch(later, _other_leg_entry("after-fill"), "after-fill", at).refusal_reason \
        == "intervention_fence"
    assert len(later_route.commands) == 1


def test_unknown_halt_survives_restart_and_duplicate_occurrence(tmp_path):
    account, route, action = _scenario(tmp_path, "entry")
    route.queue(BrokerResult("unknown"))
    occurrence = account.make_occurrence("direct", "replayed")
    first = account.dispatch(action, occurrence=occurrence, now=LATER)
    _assert_unknown_incident(account, route, first, commands=1)
    generation = account.status()["generation"]
    incidents = account.incidents

    assert account.dispatch(action, occurrence=occurrence, now=LATER) == first
    assert len(route.commands) == 1
    assert account.status()["generation"] == generation
    assert account.incidents == incidents

    for restart in range(2):
        recovery = BootstrapBroker([])
        account = BookAccountOwner.boot(account.path, account.account, binding=account.binding,
                                        synthetic_broker=recovery)
        assert (account.permission, account.authority) == ("HALTED", "INTERVENTION")
        assert account.incidents == incidents
        assert account.unresolved_attempts == (first.attempt_id,)
        assert account.exposure(LEG) == (0, 3)
        assert account.status()["generation"] == generation + 1 + restart
        assert _dispatch(account, action, "replayed-after-%d" % restart,
                         LATER + timedelta(seconds=restart)).refusal_reason in (
            "intervention_fence", "duplicate_operation")
        assert account.dispatch(action, occurrence=occurrence, now=LATER) == first
        assert recovery.commands == []


def test_concurrent_dispatch_serializes_behind_unknown_halt(tmp_path):
    account, route, action = _scenario(tmp_path, "entry")
    delegate = route.send
    entered, release = threading.Event(), threading.Event()

    def held(command):
        entered.set()
        assert release.wait(10)
        return delegate(command)

    route.queue(BrokerResult("unknown"))
    route.send = held
    first_occurrence = account.make_occurrence("direct", "first")
    second_occurrence = account.make_occurrence("direct", "second")
    results = {}
    first = threading.Thread(target=lambda: results.update(
        first=account.dispatch(action, occurrence=first_occurrence, now=LATER)))
    second = threading.Thread(target=lambda: results.update(
        second=account.dispatch(_other_leg_entry("second"), occurrence=second_occurrence, now=LATER)))
    first.start()
    assert entered.wait(10)
    second.start()
    second.join(0.5)
    assert second.is_alive()  # the second sender waits for the first result
    assert "second" not in results
    release.set()
    first.join(10)
    second.join(10)
    assert not first.is_alive() and not second.is_alive()

    _assert_unknown_incident(account, route, results["first"], commands=1)
    assert results["second"].refusal_reason == "intervention_fence"
    assert results["second"].transport_state == "not_attempted"


def test_unknown_halts_remaining_cancel_targets(tmp_path):
    # A partly filled base entry and two adds are all still-working cancel targets on the leg.
    working = BrokerResult("accepted", (FILLED,))
    account, route = owner(tmp_path, [working, BrokerResult("accepted"), BrokerResult("accepted")])
    for name, action in (("base", intent()), ("add-1", intent("add-1", kind="add", qty=12)),
                         ("add-2", intent("add-2", kind="add", qty=12))):
        placed = _dispatch(account, action, name, NOW)
        assert placed.transport_state == "accepted", placed
    exposure = account.exposure(LEG)
    assert exposure[1] > 0
    route.queue(BrokerResult("unknown"))
    route.queue(BrokerResult("accepted"))
    route.queue(BrokerResult("accepted"))

    swept = _dispatch(account, Cancel(LEG, None), "sweep")

    assert swept.transport_state == "unknown"
    assert [c.kind for c in route.commands] == ["entry", "add", "add", "cancel"]
    assert route.commands[-1].target_operation_id == "base"  # the first target; the other two are never sent
    with sqlite3.connect(account.path) as db:
        attempted = db.execute("SELECT attempt_id FROM attempts WHERE operation_id LIKE 'control:%'").fetchall()
    assert len(attempted) == 1
    first_target = SimpleNamespace(attempt_id=attempted[0][0], transport_state=swept.transport_state)
    _assert_unknown_incident(account, route, first_target, commands=4)
    assert account.exposure(LEG) == exposure  # every entry/add reservation is retained
    assert account.status()["generation"] == 2


def test_accepted_rejected_and_refused_do_not_gain_unknown_incident(tmp_path):
    accepted, route = owner(tmp_path / "accepted", [BrokerResult("accepted")])
    assert _dispatch(accepted, intent(), "accepted", NOW).transport_state == "accepted"
    rejected, _ = owner(tmp_path / "rejected", [BrokerResult("rejected")])
    assert _dispatch(rejected, intent(), "rejected", NOW).transport_state == "rejected"
    refused, refused_route = owner(tmp_path / "refused", [])
    zero = _dispatch(refused, replace(intent("too-wide"), stop_dist_pts=10**6), "too-wide", NOW)
    assert zero.refusal_reason == "zero_size" and zero.transport_state == "not_attempted"
    flat = _dispatch(refused, OrderIntent("empty-flat", LEG, "flat", Side.SELL, None, bar_time=NOW),
                     "empty-flat", NOW)
    assert flat.refusal_reason == "zero_exposure"

    for account in (accepted, rejected, refused):
        assert (account.permission, account.authority) == ("RUNNING", "NORMAL")
        assert account.incidents == ()
        assert account.status()["generation"] == 1
    assert refused_route.commands == []
    assert len(route.commands) == 1


def test_halt_storage_failure_suppresses_further_dispatch(tmp_path, monkeypatch):
    account, route, action = _scenario(tmp_path, "entry")
    route.queue(BrokerResult("unknown"))

    def broken(*args, **kwargs):
        raise sqlite3.OperationalError("disk I/O error")

    monkeypatch.setattr(account, "_invalidate_bootstrap_db", broken)
    with pytest.raises(AccountOwnerError, match="state unavailable"):
        _dispatch(account, action, "halt-fails")

    # No successful halt is claimed: the halt and the observation roll back together.
    assert len(route.commands) == 1
    assert account.incidents == ()
    with sqlite3.connect(account.path) as db:
        assert db.execute("SELECT state, observation FROM attempts").fetchall() == [
            ("UNKNOWN", None)]
    assert account.unresolved_attempts != ()
    with pytest.raises(AccountOwnerError, match="local send suppression"):
        _dispatch(account, _other_leg_entry("after-failure"), "after-failure")
    assert len(route.commands) == 1

    # A fresh boot fails closed with the attempt retained and nothing resent.
    recovery = BootstrapBroker([])
    restarted = BookAccountOwner.boot(account.path, account.account, binding=binding(),
                                      synthetic_broker=recovery)
    assert (restarted.permission, restarted.authority) == ("HALTED", "INTERVENTION")
    assert len(restarted.unresolved_attempts) == 1
    assert recovery.commands == []


def test_halt_storage_failure_stops_remaining_cancel_targets(tmp_path, monkeypatch):
    working = BrokerResult("accepted", (FILLED,))
    account, route = owner(tmp_path, [working, BrokerResult("accepted"), BrokerResult("accepted")])
    for name, action in (("base", intent()), ("add-1", intent("add-1", kind="add", qty=12)),
                         ("add-2", intent("add-2", kind="add", qty=12))):
        assert _dispatch(account, action, name, NOW).transport_state == "accepted"
    exposure = account.exposure(LEG)
    route.queue(BrokerResult("unknown"))
    route.queue(BrokerResult("accepted"))
    route.queue(BrokerResult("accepted"))

    def broken(*args, **kwargs):
        raise sqlite3.OperationalError("disk I/O error")

    monkeypatch.setattr(account, "_invalidate_bootstrap_db", broken)
    with pytest.raises(AccountOwnerError, match="state unavailable"):
        _dispatch(account, Cancel(LEG, None), "sweep")

    # Only the first target was sent; the failed halt claims nothing and blocks every later send.
    assert [c.kind for c in route.commands] == ["entry", "add", "add", "cancel"]
    assert account.incidents == ()
    assert account.exposure(LEG) == exposure
    with pytest.raises(AccountOwnerError, match="local send suppression"):
        _dispatch(account, Cancel(LEG, None), "sweep-again")
    assert len(route.commands) == 4


def test_protection_unknown_keeps_only_its_own_incident(tmp_path):
    from book_occurrence_fixtures import bare_protection_owner, prepare_protection
    from c1_signal_daemon.book_protocol import Bracket, BracketAmend
    account, route = bare_protection_owner(tmp_path)
    route.queue(BrokerResult("unknown"))
    outcome = prepare_protection(account, route,
        BracketAmend(LEG, Bracket(stop=99.0), ("base-fill",)), "unknown-attachment")
    assert outcome.transport_state == "unknown"
    assert [row["reason"] for row in account.incidents] == ["protection"]
    assert not any(i.startswith("ordinary-unknown:") for i in _incident_ids(account))
