"""Independent broker evidence, deadlines and restart fences via real journals."""
from dataclasses import replace
from datetime import timedelta
import sqlite3

import pytest

from c1_rail.book_account_owner import AccountOwnerError, BookAccountOwner
from c1_rail.book_protection import ProtectionRead
from c1_signal_daemon.book_protocol import Bracket, BracketAmend
from c1_signal_daemon.book_evaluate_loop import FourLegEvaluateLoop
from test_book_runtime_occurrences import waiting_runtime
from test_four_leg_runtime import NOW, LEGS, binding


def pending_confirmation(tmp_path):
    account, broker, runtime = waiting_runtime(tmp_path)
    broker.advance(NOW + timedelta(seconds=1))
    runtime.redeliver_prepared_boundary(NOW, now=broker.now)
    command = broker.commands[-1]
    return account, broker, runtime, command


def applied_snapshot(tmp_path):
    account, broker, runtime, command = pending_confirmation(tmp_path)
    broker.apply(command.operation_id, outcome="applied", at=NOW + timedelta(seconds=2))
    snapshot = broker.read_protection(ProtectionRead(command.occurrence, ("orb_mnq_v7",), NOW))
    return account, broker, runtime, command, snapshot


@pytest.mark.parametrize("change", [
    {"account_epoch": "foreign-epoch"},
    {"account": "foreign-account"},
    {"sequence": True},
    {"positions": (("runtime-base", True),)},
    {"positions": ()},
    {"as_of": NOW - timedelta(minutes=16)},
    {"as_of": NOW + timedelta(minutes=1)},
])
def test_invalid_evidence_never_confirms_desired_protection(tmp_path, change):
    account, broker, runtime, command, snapshot = applied_snapshot(tmp_path)
    account.observe_protection(replace(snapshot, **change), now=broker.now)
    assert account.authority == "INTERVENTION"
    row = account.protection_owners[0]
    assert row.observed is None
    assert row.pending_operation == command.operation_id
    assert row.deadline == NOW + timedelta(minutes=15)


@pytest.mark.parametrize("partial", ["incomplete", "positions_only", "equal_time"])
def test_insufficient_evidence_cannot_resolve_pending_operation(tmp_path, partial):
    account, broker, runtime, command, snapshot = applied_snapshot(tmp_path)
    if partial == "incomplete":
        snapshot = replace(snapshot, complete=False)
    elif partial == "positions_only":
        snapshot = replace(snapshot, orders=(), resolved_operations=())
    else:
        snapshot = replace(snapshot, as_of=NOW)
    account.observe_protection(snapshot, now=broker.now)
    row = account.protection_owners[0]
    assert row.pending_operation == command.operation_id
    assert row.deadline == NOW + timedelta(minutes=15)


def test_duplicate_evidence_does_not_renew_currency_or_deadline(tmp_path):
    account, broker, runtime, command, snapshot = applied_snapshot(tmp_path)
    partial = replace(snapshot, complete=False)
    account.observe_protection(partial, now=broker.now)
    account.observe_protection(partial, now=NOW + timedelta(minutes=14))
    assert account.protection_owners[0].deadline == NOW + timedelta(minutes=15)
    account.check_protection_deadlines(now=NOW + timedelta(minutes=15))
    assert account.authority == "INTERVENTION"


def test_conflicting_fact_id_and_rollback_stream_are_incidents(tmp_path):
    account, broker, runtime, command, snapshot = applied_snapshot(tmp_path)
    account.observe_protection(snapshot, now=broker.now)
    original = account.protection_owners[0]
    account.observe_protection(replace(snapshot, complete=False), now=broker.now)
    assert account.authority == "INTERVENTION"
    assert account.protection_owners[0] == original
    before = len(account.incidents)
    account.observe_protection(replace(snapshot, fact_id="new-fact-old-sequence"), now=broker.now)
    assert len(account.incidents) > before
    assert account.protection_owners[0] == original


def test_missing_working_order_in_complete_read_preserves_obligation(tmp_path):
    account, broker, runtime, command, snapshot = applied_snapshot(tmp_path)
    account.observe_protection(snapshot, now=broker.now)
    original = account.protection_owners[0]
    broker.advance(NOW + timedelta(seconds=3))
    newer = broker.read_protection(ProtectionRead(command.occurrence, ("orb_mnq_v7",), NOW))
    account.observe_protection(replace(newer, orders=()), now=broker.now)
    assert account.authority == "INTERVENTION"
    assert account.protection_owners[0].observed == original.observed
    assert account.exposure("orb_mnq_v7") == (1, 0)


def test_idle_loop_enforces_original_deadline_at_exact_boundary(tmp_path):
    account, broker, runtime, command = pending_confirmation(tmp_path)
    class Source:
        def poll(self):
            return None
    loop = FourLegEvaluateLoop(sources={leg: Source() for leg in LEGS}, runtime=runtime)
    loop.step(now=NOW + timedelta(minutes=15) - timedelta(microseconds=1))
    assert account.authority == "NORMAL"
    loop.step(now=NOW + timedelta(minutes=15))
    assert account.authority == "INTERVENTION"
    assert account.protection_owners[0].deadline == NOW + timedelta(minutes=15)
    assert len(broker.commands) == 2


def test_restart_observation_never_resumes_pending_mutation(tmp_path):
    account, broker, runtime, command, snapshot = applied_snapshot(tmp_path)
    reopened = BookAccountOwner.boot(account.path, account.account, binding=binding(), synthetic_broker=broker)
    assert reopened.authority == "INTERVENTION"
    reopened.observe_protection(snapshot, now=broker.now)
    assert reopened.protection_owners[0].observed == Bracket(stop=98)
    assert reopened.authority == "INTERVENTION"
    result = reopened.dispatch(BracketAmend("orb_mnq_v7", Bracket(stop=99), ("runtime-base",)),
        occurrence=reopened.make_occurrence("direct", "after-restart"), now=broker.now)
    assert result.refusal_reason == "intervention_fence"
    assert len(broker.commands) == 2


def test_incident_storage_failure_latches_local_suppression(tmp_path):
    account, broker, runtime, command, snapshot = applied_snapshot(tmp_path)
    with sqlite3.connect(account.path) as db:
        db.execute("CREATE TRIGGER fail_incident BEFORE INSERT ON incidents "
                   "BEGIN SELECT RAISE(ABORT, 'injected incident storage failure'); END")
    with pytest.raises(AccountOwnerError, match="unavailable"):
        account.observe_protection(replace(snapshot, account_epoch="foreign"), now=broker.now)
    with sqlite3.connect(account.path) as db:
        db.execute("DROP TRIGGER fail_incident")
    assert account.incidents == ()
    with pytest.raises(AccountOwnerError, match="suppression"):
        account.dispatch(BracketAmend("orb_mnq_v7", Bracket(stop=99), ("runtime-base",)),
            occurrence=account.make_occurrence("direct", "storage-restored"), now=broker.now)
    assert len(broker.commands) == 2


@pytest.mark.parametrize("when", [NOW + timedelta(seconds=31), NOW + timedelta(hours=1)])
def test_loosening_requires_current_binding_and_risk_add_window(tmp_path, when):
    account, broker, runtime, command, snapshot = applied_snapshot(tmp_path)
    account.observe_protection(snapshot, now=broker.now)
    action = BracketAmend("orb_mnq_v7", Bracket(stop=97), ("runtime-base",))
    occurrence = account.make_occurrence("direct", "late-loosening")
    broker.advance(when)
    first = account.dispatch(action, occurrence=occurrence, now=broker.now)
    if first.refusal_reason == "awaiting_evidence":
        broker.advance(when + timedelta(seconds=1))
        result = account.dispatch(action, occurrence=occurrence, now=broker.now)
    else:
        result = first
    assert result.refusal_reason in ("risk_add_not_authorized", "stale_account_evidence",
                                     "stale_or_future_account_evidence")
    assert len(broker.commands) == 2


@pytest.mark.parametrize("stop", [97, 99])
def test_operator_intervention_fences_loosening_and_tightening(tmp_path, stop):
    account, broker, runtime, command, snapshot = applied_snapshot(tmp_path)
    account.observe_protection(snapshot, now=broker.now)
    account.halt("operator-protection-test", "operator", now=broker.now)
    result = account.dispatch(BracketAmend("orb_mnq_v7", Bracket(stop=stop), ("runtime-base",)),
        occurrence=account.make_occurrence("direct", "post-halt"), now=broker.now)
    assert result.refusal_reason == "intervention_fence"
    assert len(broker.commands) == 2


def test_capacity_fact_gap_fences_later_loosening(tmp_path):
    from c1_rail.book_account_owner import BrokerFact
    account, broker, runtime, command, snapshot = applied_snapshot(tmp_path)
    account.observe_protection(snapshot, now=broker.now)
    entry_id = broker.commands[0].operation_id
    account.observe(BrokerFact.terminal(entry_id, "filled", 0, broker.now), now=broker.now)
    with account._transaction() as db:
        assert account._capacity(db).blocks
    result = account.dispatch(BracketAmend("orb_mnq_v7", Bracket(stop=97), ("runtime-base",)),
        occurrence=account.make_occurrence("direct", "blocked-loosening"), now=broker.now)
    assert result.refusal_reason in ("intervention_fence", "account_owner_blocked")
    assert len(broker.commands) == 2


def test_unchanged_revision_cannot_change_confirmed_components(tmp_path):
    account, broker, runtime, command, snapshot = applied_snapshot(tmp_path)
    account.observe_protection(snapshot, now=broker.now)
    broker.advance(NOW + timedelta(seconds=3))
    newer = broker.read_protection(ProtectionRead(command.occurrence, ("orb_mnq_v7",), NOW))
    altered = replace(newer.orders[0], effective=Bracket(stop=97))
    account.observe_protection(replace(newer, orders=(altered,)), now=broker.now)
    assert account.authority == "INTERVENTION"
    assert account.protection_owners[0].observed == Bracket(stop=98)


def test_complete_read_cannot_overstate_total_executable_coverage(tmp_path):
    from book_protection_fixtures import ProtectionScenario
    scenario = ProtectionScenario(tmp_path)
    scenario.enter(("first", "second"), quantities=(1, 2))
    scenario.establish("first", Bracket(stop=98))
    scenario.establish("second", Bracket(stop=98))
    snapshot = scenario.observe()
    altered = tuple(replace(row, quantity=3) for row in snapshot.orders)
    snapshot = replace(snapshot, fact_id="overstated-coverage", sequence=snapshot.sequence + 1,
                       orders=altered)
    scenario.owner.observe_protection(snapshot, now=scenario.now)
    assert scenario.owner.authority == "INTERVENTION"
    assert sum(row.quantity for row in scenario.owner.protection_owners) == 3
