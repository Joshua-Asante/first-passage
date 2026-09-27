"""H8(c): an omitted required slot ends the session, whichever detector reports it.

Card: docs/briefs/handoffs/2026-09-27-h8c-omission-incident-session-end.md (dispatch
revision 08196100). Ruling: halt/resume contract §4.1, *Qualifications*, "An omitted
required slot is an incident" (operator, 2026-09-27), under incident ADR §A11.2.

Every case drives the EXISTING owners (``FourLegEvaluateLoop``, ``FourLegRuntime``,
``BookAccountOwner`` and the listener's book handlers) in a disposable ``tmp_path`` store,
with a synthetic account, session, clock, adapters and broker. Nothing here arms,
deploys, sends to a broker or vendor, or notifies an external channel. The evidence
class is *Synthetic / replay engineering*: it shows how the current owner implementation
behaves. It is not live-feed evidence, a production re-arming policy or a resume
mechanism (card §5).

"Ends the session" (card §2): ``permission == HALTED``, ``authority == INTERVENTION`` and
no broker command dispatched after the halt.

Timing facts pinned here (H8(b) note §5, re-derived, not copied): with the loop stepped
within the 30 s slack, a single-leg omission at boundary b2 is recorded first as
``feed-silence`` (anchored on b1) and then as ``barrier-expired`` for b2 in the same step,
at the first step strictly after b2 + 15 m 30 s. ``bar-sequence`` arises only when a
later boundary reaches ``FourLegRuntime.on_completed_bar`` with no expiry call between.
A loop slower than the slack makes bars late (``invalid-bar-time``).

Reused fixtures (no fixture module added): ``tests/ops/test_four_leg_runtime.py``
(binding, adapters, ``Adapter``, ``entry``), ``tests/ops/book_bootstrap_fixtures.py``
(``BootstrapBroker``, ``activate_fresh``) and ``tests/ops/test_attended_incident_rehearsal.py``
(the bootstrap-body read and the ineligibility message).
"""
from __future__ import annotations

from dataclasses import replace
from datetime import timedelta
import json
import sqlite3

import pytest

from c1_rail.book_account_owner import AccountOwnerError, BookAccountOwner, BrokerFact, BrokerResult
from c1_rail.book_protection import ProtectionRead
from c1_rail.c1_rail_listener import handle_book_fact, handle_book_protection
from c1_signal_daemon.book_adapters import synthetic_adapter_registry
from c1_signal_daemon.book_evaluate_loop import FourLegEvaluateLoop
from c1_signal_daemon.book_protocol import BAR_PERIOD, BAR_SLACK, OrderIntent, Side
from c1_signal_daemon.book_runtime import FourLegRuntime, LEG_ORDER
from c1_signal_daemon.feed import Bar
from book_bootstrap_fixtures import BootstrapBroker, activate_fresh
from test_attended_incident_rehearsal import INELIGIBLE, _bootstrap
from test_four_leg_runtime import (
    LEGS, NOW, Adapter, adapters as entry_adapters, binding as runtime_binding, entry,
    inert_adapters,
)


SESSION = runtime_binding()["session"]
SID = SESSION.session_id
ACCOUNT = "synthetic-account"
MGC = "vanguard_mgc"
# Halt/resume §2 `:28` source timeout, as the loop passes it (book_evaluate_loop.py:33).
SILENCE = 2 * BAR_PERIOD + BAR_SLACK
# Each completed bar is delivered 2 s after it closes. With a cadence of 29 s or less every
# bar is handled inside its 30 s slack: any 29 whole seconds hold one step.
DELIVERY = timedelta(seconds=2)
CADENCE = timedelta(seconds=15)


def boundary(k):
    """Bar-open of the k-th 15-minute slot of the bound session (b0 = session open)."""
    return SESSION.opens_at + k * BAR_PERIOD


def expiry_threshold(k):
    """A partial barrier expires strictly after bar_open + 15 m 30 s (book_runtime.py:483)."""
    return boundary(k) + BAR_PERIOD + BAR_SLACK


def bar(k):
    price = 100 + k
    return Bar(boundary(k), price, price + 1, price - 1, price, 10)


def steps(start, end, cadence):
    at = start
    while at <= end:
        yield at
        at += cadence


def feed_silence_id(anchor_slot):
    return "feed-silence:" + SID + ":" + boundary(anchor_slot).isoformat()


BARRIER_EXPIRED_B2 = "barrier-expired:" + boundary(2).isoformat()


# -- Harness: a synthetic clock, four completed-bar feeds and scripted adapters -------------

class Clock:
    def __init__(self, now=NOW):
        self.now = now


class Feed:
    """One leg's completed-bar source. ``poll()`` takes no clock, so it reads a shared one.

    Bar k becomes available ``DELIVERY`` after it closes. ``omitted`` slots never arrive,
    and nothing arrives after ``stop_after``. One bar per poll, oldest first.
    """

    def __init__(self, clock, *, slots=8, omitted=(), stop_after=None):
        self.clock = clock
        self.queue = [bar(k) for k in range(slots)
                      if k not in omitted and (stop_after is None or k <= stop_after)]

    def poll(self):
        if self.queue and self.queue[0].ts + BAR_PERIOD + DELIVERY <= self.clock.now:
            return self.queue.pop(0)
        return None


def feeds(clock, *, omitted=(), stop_after=None):
    """Ordered four-leg sources; ``omitted`` applies to MGC only."""
    return {leg_id: Feed(clock, omitted=omitted if leg_id == MGC else (), stop_after=stop_after)
            for leg_id in LEG_ORDER}


class ScriptedAdapter(Adapter):
    """``test_four_leg_runtime.Adapter`` whose actions are keyed by bar-open."""

    def __init__(self, leg_id, script=None):
        super().__init__(leg_id)
        self.script = dict(script or {})

    def on_bar(self, value):
        super().on_bar(value)
        return list(self.script.get(value.ts, ()))


def scripted(**scripts):
    return synthetic_adapter_registry({leg_id: ScriptedAdapter(leg_id, scripts.get(leg_id))
                                       for leg_id in LEGS})


def at_bar(action, k):
    return replace(action, bar_time=boundary(k))


# -- Harness: owner, runtime and loop -------------------------------------------------------

def bound():
    """The runtime fixture binding, kept valid through the risk-add window.

    The activation cases need every other precondition to hold at an in-window attempt
    after b2's expiry, so ``valid_until`` and ``max_evidence_age`` cover the window.
    """
    value = runtime_binding()
    value.update(valid_until=SESSION.risk_add_cutoff,
                 max_evidence_age=SESSION.risk_add_cutoff - value["as_of"])
    return value


def session(tmp_path, registry=None, results=()):
    broker = BootstrapBroker(list(results))
    account = BookAccountOwner.boot(tmp_path / "owner.sqlite", ACCOUNT, binding=bound(),
                                    synthetic_broker=broker)
    activate_fresh(account, now=NOW)
    runtime = FourLegRuntime(account, registry if registry is not None else inert_adapters())
    return account, broker, runtime


def state(account):
    status = account.status()
    return status["permission"], status["authority"], status["generation"]


def incident_rows(account):
    return tuple((row["incident_id"], row["reason"], row["at"], row["generation"])
                 for row in account.incidents)


def exposures(account):
    return {leg_id: (confirmed, reserved)
            for leg_id, confirmed, reserved in account.status()["exposures"]}


def assert_session_ended(account, broker, commands_at_halt):
    assert state(account)[:2] == ("HALTED", "INTERVENTION")
    assert len(broker.commands) == commands_at_halt


def obligations(account):
    """Recovery obligations the owner retains, read without mutation."""
    status = account.status()
    with sqlite3.connect(account.path) as db:
        plans = tuple(row[0] for row in db.execute(
            "SELECT operation_id FROM takeover_plans ORDER BY operation_id"))
        events = tuple(db.execute(
            "SELECT event_id, operation_id, ordinal, kind, body FROM takeover_events "
            "ORDER BY operation_id, ordinal"))
    return {
        "exposures": status["exposures"],
        "unresolved_attempts": status["unresolved_attempts"],
        "operations": account.observable_accounting()["operations"],
        "protection": account.protection_owners,
        "pending_feedback": account.pending_feedback,
        "takeover_plans": plans,
        "takeover_events": events,
    }


def run_with_omission(account, runtime, *, cadence=CADENCE, inject=None):
    """Step the loop from session open with MGC omitting b2 until the book halts.

    ``inject(at)`` runs after each pre-halt step. Returns the obligations read just before
    the halt step, the halt step, the loop and the clock.
    """
    clock = Clock()
    loop = FourLegEvaluateLoop(sources=feeds(clock, omitted=(2,)), runtime=runtime)
    before = None
    for at in steps(NOW, expiry_threshold(2) + cadence, cadence):
        if at > expiry_threshold(2) and before is None:
            before = obligations(account)
        clock.now = at
        loop.step(now=at)
        if account.authority == "INTERVENTION":
            return before, at, loop, clock
        assert state(account) == ("RUNNING", "NORMAL", 1), incident_rows(account)
        if inject is not None:
            inject(at)
    raise AssertionError("the omission did not halt the book")


def omission_halt(tmp_path, registry=None):
    account, broker, runtime = session(tmp_path, registry)
    _before, halted_at, loop, clock = run_with_omission(account, runtime)
    assert incident_rows(account) == (
        (feed_silence_id(1), "feed", halted_at.isoformat(), 1),
        (BARRIER_EXPIRED_B2, "barrier", halted_at.isoformat(), 2),
    )
    return account, broker, runtime, loop, clock, halted_at


def fill_once(broker, account, runtime, order, fill_id, quantity, *, at_or_after, terminal):
    """An ``inject`` that delivers one broker fill (and optionally its terminal) once."""
    done = []

    def inject(at):
        if done or at < at_or_after:
            return
        fact = broker.execute_entry(order, fill_id=fill_id, quantity=quantity, price=100.0, at=at)
        assert handle_book_fact(fact, account, runtime, now=at)[0].fill.fill_id == fill_id
        if terminal:
            assert handle_book_fact(BrokerFact.terminal(order, "filled", quantity, at),
                                    account, runtime, now=at) == ()
        done.append(at)
    return inject


# -- Detector nodes ------------------------------------------------------------------------

@pytest.mark.parametrize("omitted", [(2,), (2, 3, 4, 5, 6, 7)], ids=["one-slot", "six-slots"])
@pytest.mark.parametrize("cadence", [timedelta(seconds=15), timedelta(seconds=29)],
                         ids=["15s", "29s"])
def test_single_leg_omission_under_loop_records_feed_silence_then_barrier_expired(
        tmp_path, omitted, cadence):
    """Under the loop, `feed-silence` then `barrier-expired` in one step; count-independent."""
    # test_four_leg_runtime's entry adapters: Aegis's b0 entry is accepted before the gap.
    account, broker, runtime = session(tmp_path, entry_adapters(), [BrokerResult("accepted")])
    clock = Clock()
    loop = FourLegEvaluateLoop(sources=feeds(clock, omitted=omitted), runtime=runtime)

    halted_at = halt_result = commands_at_halt = None
    # Run past b3's own expiry threshold, so the six-slot case also omits a later boundary.
    for at in steps(NOW, expiry_threshold(3) + cadence, cadence):
        clock.now = at
        result = loop.step(now=at)
        if halted_at is None and account.authority == "INTERVENTION":
            halted_at, halt_result, commands_at_halt = at, result, len(broker.commands)
        if halted_at is None:
            assert state(account) == ("RUNNING", "NORMAL", 1), at
            assert account.incidents == ()
        else:
            assert result is None

    # The halt is at the first step strictly after b2 + 15 m 30 s, never at or before it.
    assert halted_at is not None
    assert halted_at > expiry_threshold(2) >= halted_at - cadence
    assert halt_result is None
    # First `feed-silence`, anchored on b1 (the latest complete barrier), then
    # `barrier-expired` for b2, in that one step. Each new row bumps the generation.
    assert incident_rows(account) == (
        (feed_silence_id(1), "feed", halted_at.isoformat(), 1),
        (BARRIER_EXPIRED_B2, "barrier", halted_at.isoformat(), 2),
    )
    assert state(account) == ("HALTED", "INTERVENTION", 3)
    # The session ended: nothing was dispatched after the halt (Aegis's b0 entry predates it).
    assert [command.operation_id for command in broker.commands] == ["entry:aegis_6j"]
    assert_session_ended(account, broker, commands_at_halt)
    assert account.retained_partial_bars == ()
    assert [row["bar_time"] for row in account.retained_barriers] == [
        boundary(0).isoformat(), boundary(1).isoformat()]


@pytest.mark.parametrize("omitted", [(2,), (2, 3, 4, 5, 6, 7)], ids=["one-slot", "six-slots"])
def test_omission_reaching_runtime_before_expiry_records_bar_sequence(tmp_path, omitted):
    """A later boundary reaching the runtime before any expiry call records `bar-sequence`."""
    account, broker, runtime = session(tmp_path, entry_adapters(), [BrokerResult("accepted")])
    for k in (0, 1):
        for leg_id in LEG_ORDER:
            runtime.on_completed_bar(leg_id, bar(k), now=boundary(k) + BAR_PERIOD + DELIVERY)
    arrived = boundary(2) + BAR_PERIOD + DELIVERY
    for leg_id in LEG_ORDER:
        if leg_id != MGC:
            assert runtime.on_completed_bar(leg_id, bar(2), now=arrived) is None
    assert runtime.pending_bar_times == (boundary(2),)
    assert state(account) == ("RUNNING", "NORMAL", 1) and account.incidents == ()
    commands_at_halt = len(broker.commands)
    assert commands_at_halt == 1

    # b3 reaches the runtime with b2 still pending and no expire_barrier call between.
    later = boundary(3) + BAR_PERIOD + DELIVERY
    first = next(leg_id for leg_id in LEG_ORDER if leg_id != MGC or 3 not in omitted)
    with pytest.raises(AccountOwnerError, match="noncontiguous bar boundary"):
        runtime.on_completed_bar(first, bar(3), now=later)

    assert incident_rows(account) == (
        ("bar-sequence:" + boundary(3).isoformat(), "barrier", later.isoformat(), 1),)
    assert state(account) == ("HALTED", "INTERVENTION", 2)
    assert_session_ended(account, broker, commands_at_halt)


def test_all_legs_silent_uncaptured_early_close_records_feed_silence(tmp_path):
    """All four legs going silent records `feed-silence` only; no scheduled cutoff path."""
    # A regular permitted row stays in force; every leg stops after b1 (an early close that
    # no captured calendar source recorded). Aegis's b0 entry is still active at the cutoff.
    account, broker, runtime = session(tmp_path, entry_adapters(), [BrokerResult("accepted")])
    clock = Clock()
    loop = FourLegEvaluateLoop(sources=feeds(clock, stop_after=1), runtime=runtime)

    halted_at = commands_at_halt = halt_incidents = halt_state = None
    for at in steps(NOW, SESSION.risk_add_cutoff + timedelta(minutes=1), CADENCE):
        clock.now = at
        result = loop.step(now=at)
        if halted_at is None and account.authority == "INTERVENTION":
            halted_at, commands_at_halt = at, len(broker.commands)
            halt_incidents, halt_state = incident_rows(account), state(account)
        if halted_at is not None:
            assert result is None
    assert halted_at is not None and halted_at < SESSION.risk_add_cutoff
    # The silence threshold for anchor b1 equals b2's expiry threshold; no partial exists.
    assert halted_at > boundary(1) + SILENCE >= halted_at - CADENCE
    assert halt_incidents == ((feed_silence_id(1), "feed", halted_at.isoformat(), 1),)
    assert halt_state == ("HALTED", "INTERVENTION", 2)
    assert account.retained_partial_bars == ()

    # Stepped through the scheduled risk-add cutoff: the scheduled path was NOT taken. No
    # SCHEDULED_EXIT, no generation bump and no scheduled cancel of the still-active entry.
    assert state(account) == halt_state
    assert incident_rows(account) == halt_incidents
    assert commands_at_halt == 1
    assert_session_ended(account, broker, commands_at_halt)
    assert exposures(account)["aegis_6j"] == (0, 8)


def test_late_bar_invalid_bar_time_regression_ends_session(tmp_path):
    """Not an omission: every leg delivers every bar; the loop polls slower than BAR_SLACK."""
    account, broker, runtime = session(tmp_path, entry_adapters(), [BrokerResult("accepted")])
    clock = Clock()
    loop = FourLegEvaluateLoop(sources=feeds(clock), runtime=runtime)
    cadence = timedelta(seconds=60)
    raised_at = None
    for at in steps(NOW, boundary(2), cadence):
        clock.now = at
        try:
            loop.step(now=at)
        except AccountOwnerError as exc:
            assert str(exc) == "bar is stale, future, or outside the bound session"
            raised_at = at
            break
        assert state(account) == ("RUNNING", "NORMAL", 1)

    # b0 is handled at 16 m 00 s, after bar_open + 15 m 30 s (book_runtime.py:350-353).
    assert raised_at == boundary(0) + BAR_PERIOD + timedelta(minutes=1)
    assert raised_at > expiry_threshold(0)
    assert incident_rows(account) == (
        ("invalid-bar-time:" + boundary(0).isoformat(), "barrier", raised_at.isoformat(), 1),)
    assert state(account) == ("HALTED", "INTERVENTION", 2)
    assert broker.commands == []  # b0 was never evaluated, so nothing was ever sent
    for at in steps(raised_at + cadence, raised_at + 3 * cadence, cadence):
        clock.now = at
        assert loop.step(now=at) is None
    assert_session_ended(account, broker, 0)
    assert len(account.incidents) == 1


# -- After the omission halt ---------------------------------------------------------------

def test_recovered_bars_after_omission_halt_dispatch_nothing(tmp_path):
    """Recovered bars dispatch nothing, under the loop or by direct runtime delivery."""
    # Adapters that would emit an entry on each recovered bar, if they were ever evaluated.
    registry = scripted(orb_mnq_v7={
        boundary(k): [at_bar(replace(entry("orb_mnq_v7", 1), order_id=f"entry:orb:{k}"), k)]
        for k in (3, 4)})
    account, broker, runtime, loop, clock, halted_at = omission_halt(tmp_path, registry)
    halted = state(account)
    incidents = incident_rows(account)
    evaluated = {leg_id: list(registry[leg_id].bars) for leg_id in LEGS}
    assert evaluated["orb_mnq_v7"] == [boundary(0).isoformat(), boundary(1).isoformat()]
    assert broker.commands == []

    # All four legs resume on time from b3 (MGC omitted only b2). Under the loop, step
    # returns without dispatch and never polls the recovered feeds.
    for at in steps(halted_at + CADENCE, boundary(4) + BAR_PERIOD + DELIVERY, CADENCE):
        clock.now = at
        assert loop.step(now=at) is None
    assert all(loop.sources[leg_id].queue[0].ts == boundary(3) for leg_id in LEGS)
    assert state(account) == halted and incident_rows(account) == incidents

    # Direct runtime delivery of the recovered boundary. b2 never completed, so b3 is
    # noncontiguous: it records one more `bar-sequence` incident and dispatches nothing.
    at = boundary(3) + BAR_PERIOD + DELIVERY
    for leg_id in LEG_ORDER:
        with pytest.raises(AccountOwnerError, match="noncontiguous bar boundary"):
            runtime.on_completed_bar(leg_id, bar(3), now=at)
    assert incident_rows(account) == incidents + (
        ("bar-sequence:" + boundary(3).isoformat(), "barrier", at.isoformat(), halted[2]),)
    assert state(account) == ("HALTED", "INTERVENTION", halted[2] + 1)
    assert account.retained_partial_bars == ()
    assert [row["bar_time"] for row in account.retained_barriers] == [
        boundary(0).isoformat(), boundary(1).isoformat()]
    assert {leg_id: registry[leg_id].bars for leg_id in LEGS} == evaluated
    assert_session_ended(account, broker, 0)


def assert_activation_preconditions(account, at):
    """Every precondition `_activate_bootstrap` checks before entitlement holds at ``at``."""
    binding = account.binding
    assert binding["session"].opens_at <= at < binding["session"].risk_add_cutoff  # :121
    assert binding["as_of"] <= at < binding["valid_until"]                          # :123
    assert at - binding["as_of"] <= binding["max_evidence_age"]                     # :124
    assert getattr(account, "_input_send_suppressed", False) is False               # :115
    before = incident_rows(account)
    # The settlement check `_activate_bootstrap` runs first (book_bootstrap.py:117). It only
    # writes when it refuses; a validating binding returns None and leaves the journal as is.
    with account._transaction() as db:
        assert account._validate_settlement_binding(db, at) is None
    assert incident_rows(account) == before


def assert_refused_for_incident(account, at, incident_id):
    before = account.status()
    with pytest.raises(AccountOwnerError) as refused:
        account.activate_synthetic(now=at)
    # The only message `_activate_bootstrap` raises for an ineligible or rebound entitlement
    # (book_bootstrap.py:130-131). Stale, window, settlement and suppression refusals differ.
    assert str(refused.value) == INELIGIBLE
    body = _bootstrap(account)
    assert (body["state"], body["invalidation"]) == ("ineligible", "incident:" + incident_id)
    after = account.status()
    assert (after["permission"], after["authority"]) == ("HALTED", "INTERVENTION")
    assert (after["generation"], after["boot_id"]) == (before["generation"], before["boot_id"])


def test_repeated_bootstrap_activation_refused_after_omission_halt(tmp_path):
    """Same-session re-activation is refused because of the omission incident, and only it."""
    account, broker, _runtime, _loop, _clock, halted_at = omission_halt(tmp_path)
    at = halted_at + CADENCE
    assert_activation_preconditions(account, at)
    # The omission's first record (`feed-silence`) invalidated the bootstrap. The later
    # `barrier-expired` row keeps that first reason (book_bootstrap.py:102-103).
    assert_refused_for_incident(account, at, feed_silence_id(1))
    assert incident_rows(account)[-1][0] == BARRIER_EXPIRED_B2
    assert broker.commands == []


def test_reopened_journal_after_omission_halt_stays_halted(tmp_path):
    """A reboot on the retained journal stays HALTED and keeps the original invalidation."""
    account, broker, _runtime, _loop, _clock, halted_at = omission_halt(tmp_path)
    incidents = account.incidents
    before = account.status()

    reopened = BookAccountOwner.boot(account.path, ACCOUNT, binding=account.binding,
                                     synthetic_broker=broker)
    after = reopened.status()
    assert (after["permission"], after["authority"]) == ("HALTED", "INTERVENTION")
    assert after["boot_id"] != before["boot_id"]
    assert after["generation"] == before["generation"] + 1
    assert reopened.incidents == incidents
    # A restart keeps the first invalidation, not 'restart' (book_account_owner.py:387).
    assert _bootstrap(reopened)["invalidation"] == "incident:" + feed_silence_id(1)

    at = halted_at + CADENCE
    assert_activation_preconditions(reopened, at)
    assert_refused_for_incident(reopened, at, feed_silence_id(1))
    assert reopened.incidents == incidents
    assert broker.commands == []


def test_repeated_incident_id_preserves_identity_and_generation(tmp_path):
    """A repeated incident id keeps one row, its `at` and generation; conflicting `at` raises."""
    account, _broker, _runtime, _loop, _clock, halted_at = omission_halt(tmp_path)
    original = incident_rows(account)
    feed_id = original[0][0]
    halted = state(account)
    invalidation = _bootstrap(account)["invalidation"]

    def unchanged():
        assert incident_rows(account) == original
        assert state(account) == halted
        assert _bootstrap(account)["invalidation"] == invalidation

    # Path 1: the silence detector again, later, with the anchor (b1) unchanged. Under
    # INTERVENTION it returns before evaluating (book_account_owner.py:854-855).
    account.check_source_silence(now=halted_at + timedelta(minutes=5), max_silence=SILENCE)
    unchanged()

    # Path 2: halt() with the same id, reason and `at`: still one row, no generation bump.
    account.halt(feed_id, "feed", now=halted_at)
    unchanged()

    # Pinned: the same id with a different `at` is refused as a conflicting identity
    # (book_account_owner.py:1122-1123). Nothing is written; the authority stays INTERVENTION.
    with pytest.raises(AccountOwnerError, match="^conflicting incident identity$"):
        account.halt(feed_id, "feed", now=halted_at + timedelta(seconds=1))
    unchanged()
    assert account.authority == "INTERVENTION"


@pytest.mark.parametrize("obligation", ["takeover", "partial_fill"])
def test_distinct_detectors_neither_restore_authority_nor_drop_obligations(tmp_path, obligation):
    """Two detector records for one omission; neither restores authority or clears obligations."""
    fill_at = boundary(0) + BAR_PERIOD + timedelta(seconds=20)
    if obligation == "takeover":
        # b0: ORB takes one micro, filled. b1: Aegis needs the whole cap and publishes a
        # takeover plan that is still at PLAN when the omission halts the book.
        registry = scripted(orb_mnq_v7={boundary(0): [at_bar(entry("orb_mnq_v7", 1), 0)]},
                            aegis_6j={boundary(1): [at_bar(entry("aegis_6j", 8), 1)]})
        order, fill_id, terminal = "entry:orb_mnq_v7", "orb-fill", True
    else:
        # b0: a Striker entry partially fills; its remainder is still working at the halt.
        registry = scripted(dj30_mym_p250={
            boundary(0): [at_bar(entry("dj30_mym_p250", 5, stop=24), 0)]})
        order, fill_id, terminal = "entry:dj30_mym_p250", "dj30-fill", False
    account, broker, runtime = session(tmp_path, registry, [BrokerResult("accepted")] * 2)
    inject = fill_once(broker, account, runtime, order, fill_id, 1, at_or_after=fill_at,
                       terminal=terminal)
    before, halted_at, loop, _clock = run_with_omission(account, runtime, inject=inject)
    after = obligations(account)

    # Two separate records for one omission; the ruling requires no deduplication.
    assert incident_rows(account) == (
        (feed_silence_id(1), "feed", halted_at.isoformat(), 1),
        (BARRIER_EXPIRED_B2, "barrier", halted_at.isoformat(), 2),
    )
    # Neither restores authority, and the loop dispatches nothing afterwards.
    assert state(account) == ("HALTED", "INTERVENTION", 3)
    commands = len(broker.commands)
    assert loop.step(now=halted_at + CADENCE) is None
    assert_session_ended(account, broker, commands)

    # Obligations are neither lost nor cleared: every retained record is unchanged, and the
    # only takeover-journal change is appended HALT events.
    for key in ("exposures", "unresolved_attempts", "operations", "protection",
                "pending_feedback", "takeover_plans"):
        assert after[key] == before[key], key
    retained = len(before["takeover_events"])
    assert after["takeover_events"][:retained] == before["takeover_events"]
    appended = after["takeover_events"][retained:]
    assert [owner.entry_fill_id for owner in after["protection"]] == [fill_id]
    if obligation == "takeover":
        assert before["takeover_plans"] == ("entry:aegis_6j",)
        assert [row[3] for row in before["takeover_events"]] == ["PLAN"]
        assert exposures(account)["orb_mnq_v7"] == (1, 0)
        # One HALT event per incident row, in order; the second does not replace the first.
        assert [(row[0], row[3]) for row in appended] == [
            ("entry:aegis_6j:1", "HALT"), ("entry:aegis_6j:2", "HALT")]
        assert [json.loads(row[4])["incident_id"] for row in appended] == [
            feed_silence_id(1), BARRIER_EXPIRED_B2]
    else:
        assert appended == ()
        assert len(before["unresolved_attempts"]) == 1
        confirmed, reserved = exposures(account)["dj30_mym_p250"]
        assert confirmed == 1 and reserved > 0  # the working remainder is still owned


def test_recovery_and_evidence_entry_points_remain_available_after_omission_halt(tmp_path):
    """Firm condition (card §2): valid, causally appropriate evidence remains recordable."""
    exit_orb = OrderIntent("exit:orb_mnq_v7", "orb_mnq_v7", "exit", Side.SELL, 1,
                           scope_fill_ids=("orb-fill",), bar_time=boundary(1))
    registry = scripted(
        dj30_mym_p250={boundary(0): [at_bar(entry("dj30_mym_p250", 5, stop=24), 0)]},
        orb_mnq_v7={boundary(0): [at_bar(entry("orb_mnq_v7", 1), 0)], boundary(1): [exit_orb]})
    account, broker, runtime = session(tmp_path, registry, [BrokerResult("accepted")] * 3)
    inject = fill_once(broker, account, runtime, "entry:orb_mnq_v7", "orb-fill", 1,
                       at_or_after=boundary(0) + BAR_PERIOD + timedelta(seconds=20),
                       terminal=True)
    _before, halted_at, loop, _clock = run_with_omission(account, runtime, inject=inject)

    # Before the halt: a working Striker entry (unfilled) and a working ORB exit of the
    # filled ORB lot. Both orders, and the ORB position, existed before the halt.
    sent = [(command.operation_id, command.kind) for command in broker.commands]
    assert sent == [("entry:dj30_mym_p250", "entry"), ("entry:orb_mnq_v7", "entry"),
                    ("exit:orb_mnq_v7", "exit")]
    striker_quantity = broker.commands[0].quantity
    halted = state(account)
    incidents = incident_rows(account)
    assert [row[0] for row in incidents] == [feed_silence_id(1), BARRIER_EXPIRED_B2]

    def still_ended():
        assert state(account) == halted
        assert incident_rows(account) == incidents
        assert len(broker.commands) == len(sent)

    # 1. Broker facts for the pre-halt Striker entry, via the listener's book-fact handler.
    at = halted_at + timedelta(seconds=5)
    fill = broker.execute_entry("entry:dj30_mym_p250", fill_id="dj30-fill",
                                quantity=striker_quantity, price=100.0, at=at)
    events = handle_book_fact(fill, account, runtime, now=at)
    assert [(event.event, event.fill.fill_id) for event in events] == [("fill", "dj30-fill")]
    assert handle_book_fact(BrokerFact.terminal("entry:dj30_mym_p250", "filled",
                                                striker_quantity, at),
                            account, runtime, now=at) == ()
    assert ("fill", "entry:dj30_mym_p250", "dj30-fill") in registry["dj30_mym_p250"].events
    still_ended()

    # 2. Close feedback for the pre-halt ORB exit of the pre-halt ORB position.
    at = halted_at + timedelta(seconds=10)
    close_facts = broker.execute_close("exit:orb_mnq_v7", execution_id="orb-exit", quantity=1,
                                       price=99.0, terminal=True, at=at)
    assert [fact.kind for fact in close_facts] == ["fill", "terminal"]
    close_events = [event for fact in close_facts
                    for event in handle_book_fact(fact, account, runtime, now=at)]
    assert [(event.event, event.order_id) for event in close_events] == [
        ("fill", "exit:orb_mnq_v7")]
    assert ("fill", "exit:orb_mnq_v7", "orb-exit:orb-fill") in registry["orb_mnq_v7"].events
    still_ended()

    # 3. A complete protection read of both legs, via the listener's protection handler.
    prepared = halted_at + timedelta(seconds=15)
    read = ProtectionRead(account.make_occurrence("direct", "post-halt-protection-read"),
                          ("dj30_mym_p250", "orb_mnq_v7"), prepared)
    at = prepared + timedelta(milliseconds=100)
    broker.advance(at)
    snapshot = broker.read_protection(read)
    assert snapshot is not None and snapshot.complete
    assert handle_book_protection(snapshot, account, runtime, now=at) == ()
    with sqlite3.connect(account.path) as db:
        assert db.execute("SELECT kind FROM protection_facts WHERE fact_id=?",
                          (snapshot.fact_id,)).fetchone() == ("snapshot",)
    still_ended()

    # Every item was recorded: the accounting reflects the evidence and nothing is pending.
    accounting = account.observable_accounting()
    assert {"dj30-fill", "terminal:entry:dj30_mym_p250:filled", "orb-exit:orb-fill",
            "terminal:exit:orb_mnq_v7:filled"} <= {fact_id for fact_id, _ in accounting["facts"]}
    assert exposures(account) == {"aegis_6j": (0, 0), "dj30_mym_p250": (striker_quantity, 0),
                                  "vanguard_mgc": (0, 0), "orb_mnq_v7": (0, 0)}
    assert {row[0]: row[4] for row in accounting["operations"]} == {
        "entry:dj30_mym_p250": "terminal", "entry:orb_mnq_v7": "terminal",
        "exit:orb_mnq_v7": "terminal"}
    assert account.unresolved_attempts == ()
    assert account.pending_feedback == ()

    # 4. Status reads are available and pure.
    status = account.status()
    assert account.status() == status
    assert (status["permission"], status["authority"]) == ("HALTED", "INTERVENTION")
    assert runtime.observable_state()["account"] == account.observable_accounting()

    # None of it restarts automation: the loop still returns without dispatch.
    assert loop.step(now=halted_at + timedelta(seconds=30)) is None
    still_ended()


def test_scheduled_cutoff_without_omission_records_no_incident(tmp_path):
    """On-time delivery to the cutoff gives SCHEDULED_EXIT and no incident row."""
    # Aegis's b0 entry is still active at the cutoff, so the scheduled path has work to do.
    account, broker, runtime = session(tmp_path, entry_adapters(), [BrokerResult("accepted")] * 2)
    clock = Clock()
    loop = FourLegEvaluateLoop(sources=feeds(clock), runtime=runtime)
    for at in steps(NOW, SESSION.risk_add_cutoff + timedelta(seconds=30), CADENCE):
        clock.now = at
        loop.step(now=at)
        if at < SESSION.risk_add_cutoff:
            assert state(account) == ("RUNNING", "NORMAL", 1), at

    # Every leg delivered every boundary up to the cutoff (b3 closes at the cutoff).
    assert [(row["bar_time"], row["completed"]) for row in account.retained_barriers] == [
        (boundary(k).isoformat(), True) for k in range(4)]
    # SCHEDULED_EXIT, not INTERVENTION, and no incident row: a scheduled closure is not an
    # incident. The cutoff rotates the generation without invalidating the bootstrap record.
    assert state(account) == ("HALTED", "SCHEDULED_EXIT", 2)
    assert account.incidents == ()
    assert _bootstrap(account)["invalidation"] is None
    # The scheduled path ran: its own cancel of the resting risk-add under SCHEDULED_EXIT.
    assert [(command.kind, command.authority, command.target_operation_id,
             command.occurrence.producer) for command in broker.commands] == [
        ("entry", "NORMAL", None, "runtime"),
        ("cancel", "SCHEDULED_EXIT", "entry:aegis_6j", "schedule"),
    ]
