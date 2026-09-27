"""H5(b) synthetic attended-incident rehearsal of incident ADR §A11.2 (halt/resume §4.1).

Card: docs/briefs/handoffs/2026-09-27-h5b-attended-incident-rehearsal.md, read at the
dispatch revision (PR #520). Every case runs against the EXISTING owners in a disposable
``tmp_path`` store, with a synthetic account, session and clock. Nothing here arms,
deploys, sends to a broker or vendor, or notifies an external channel. The evidence class
is *Synthetic / replay engineering*. A pass here resolves no obligation that needs a real
producer (card §4).

What the cases show:
- after each scripted incident (S1-S6), no path restarts automation in the same session;
- a correctly handled refusal (S7) refuses only that request, and the session keeps running;
- the local notifier (``FileAckNotifier``) cannot change the halt, generation or permission.

Reused, not duplicated (cited in the evidence note):
- ``tests/ops/test_book_halt.py::test_running_injected_into_database_never_grants_permission``;
- ``tests/ops/test_book_bootstrap_migration.py::test_empty_history_cannot_rearm``,
  ``::test_running_activation_is_noop_after_activity`` and
  ``::test_halt_wins_serialized_race_with_fresh_activation``;
- ``tests/ops/test_c1_rail_telemetry.py::test_file_ack_notifier_notify_and_acknowledge``;
- H4's pending ``test_refreshed_evidence_never_restores_permission_after_incident_halt`` and
  ``test_stale_evidence_blocks_admission_loosening_and_takeover`` (H4 card; another branch).

Not rehearsed:
- S7's stale-individual-signal sub-case. No owner implements that refusal (card §10, Variance
  2026-09-27).
- O-1 to O-5 of halt/resume §4.1, which stay OPEN.
"""
from __future__ import annotations

import ast
from dataclasses import replace
from datetime import datetime, timedelta
import json
from pathlib import Path
import re
import sqlite3
import sys

import pytest

from c1_rail.book_account_owner import (
    MAX_FACT_AGE,
    AccountOwnerError,
    BookAccountOwner,
    BrokerFact,
    BrokerResult,
)
from c1_rail.book_policy import leg
from c1_rail_telemetry import FileAckNotifier
from c1_signal_daemon.book_protocol import BAR_PERIOD, Bracket, BracketAmend, Cancel, Mode, Side
from book_bootstrap_fixtures import BootstrapBroker, activate_fresh
from book_protection_fixtures import ProtectionScenario
from test_book_account_owner import NOW, SESSION, binding, intent


REPO = Path(__file__).resolve().parents[2]
RAIL = REPO / "ops" / "c1_rail"
# Halt/resume §2 `:28`: the preserved source timeout, 2 * bar_period + 30 seconds.
SOURCE_TIMEOUT = 2 * BAR_PERIOD + timedelta(seconds=30)
LEGS = ("aegis_6j", "dj30_mym_p250", "vanguard_mgc", "orb_mnq_v7")
# The only error `_activate_bootstrap` raises once the bootstrap is ineligible or bound to
# another boot. Every activation assertion below uses a binding that is otherwise fresh, so
# this message proves that the incident, not stale evidence, is why activation is refused.
INELIGIBLE = "fresh bootstrap entitlement required"


def _rehearsal_owner(tmp_path, results, **binding_changes):
    """A fresh, activated synthetic owner whose binding stays valid for the whole window."""
    bound = binding()
    bound.update(valid_until=NOW + timedelta(hours=2), max_evidence_age=timedelta(hours=2))
    bound.update(binding_changes)
    broker = BootstrapBroker(list(results))
    account = BookAccountOwner.boot(tmp_path / "owner.sqlite", "synthetic-account",
                                    binding=bound, synthetic_broker=broker)
    activate_fresh(account)
    return account, broker


def _state(account):
    status = account.status()
    return status["permission"], status["authority"], status["generation"]


def _incident_ids(account):
    return tuple(row["incident_id"] for row in account.incidents)


def _bootstrap(account):
    with sqlite3.connect(account.path) as db:
        return json.loads(db.execute("SELECT body FROM bootstrap_identity").fetchone()[0])


def _dispatch(account, action, event, at):
    return account.dispatch(action, occurrence=account.make_occurrence("direct", event), now=at)


def _other_leg_entry(order_id, at):
    return replace(intent(order_id), leg_id="orb_mnq_v7", qty=1, bar_time=at)


def _assert_no_same_session_activation(account, at):
    before = account.status()
    with pytest.raises(AccountOwnerError, match=INELIGIBLE):
        activate_fresh(account, now=at)
    after = account.status()
    assert (after["permission"], after["authority"]) == ("HALTED", "INTERVENTION")
    assert after["generation"] == before["generation"]
    assert after["boot_id"] == before["boot_id"]
    assert _bootstrap(account)["state"] == "ineligible"


def _stale_fact_incident(account, at):
    """S2(a): a broker fact older than MAX_FACT_AGE (halt/resume §2 `:26`, lost evidence)."""
    stale = BrokerFact.fill("exec-stale", "base", "dj30_mym_p250", "entry", 1, 100.0,
                            at - MAX_FACT_AGE - timedelta(seconds=1))
    assert account.observe(stale, now=at) == ()


def _complete_bar(account, bar_time):
    body = {leg_id: {"close": 100, "leg": leg_id} for leg_id in LEGS}
    for leg_id in LEGS:
        account.record_partial_bar(leg_id, bar_time, body[leg_id], acquired_at=bar_time)
    account.record_barrier(bar_time, body, session_id=SESSION.session_id, mode=Mode.NORMAL)


# -- S1: lost response (halt/resume §2 `:26`, uncertain outcome: incident) -----------------

def test_lost_entry_response_blocks_risk_add_at_once(tmp_path):
    account, broker = _rehearsal_owner(tmp_path, [BrokerResult("unknown"), BrokerResult("accepted")])
    sent = _dispatch(account, intent(), "base", NOW)
    assert sent.transport_state == "unknown"
    assert account.unresolved_attempts == (sent.attempt_id,)

    at = NOW + timedelta(seconds=1)  # well inside the order's first bar
    refused = _dispatch(account, _other_leg_entry("other", at), "other", at)
    assert refused.refusal_reason == "unknown_order"
    assert refused.transport_state == "not_attempted"
    assert len(broker.commands) == 1


@pytest.mark.xfail(strict=True, reason=(
    "CC-3 (TB-I3/T09), open defect: the owner raises no halt for an ordinary unknown entry "
    "outcome (halt/resume §2 `:26`) and admits risk-adds again in the same session after an "
    "accepted, postdating terminal, contrary to incident ADR §A11.2 (halt/resume §4.1). "
    "Pinned under the recorded coordinator variance, card §7 option (B); this XFAIL is NOT "
    "acceptance of §A11.2 behavior."))
def test_lost_entry_response_terminal_does_not_restart_automation_in_session(tmp_path):
    account, broker = _rehearsal_owner(tmp_path, [BrokerResult("unknown"), BrokerResult("accepted")])
    _dispatch(account, intent(), "base", NOW)
    blocked_at = NOW + timedelta(seconds=1)
    assert _dispatch(account, _other_leg_entry("other", blocked_at), "other",
                     blocked_at).refusal_reason == "unknown_order"

    terminal_at = NOW + timedelta(seconds=2)
    account.observe(BrokerFact.terminal("base", "cancelled", 0, terminal_at), now=terminal_at)

    retry_at = NOW + timedelta(seconds=3)
    retry = _dispatch(account, _other_leg_entry("after-terminal", retry_at), "after-terminal", retry_at)
    # §A11.2: the incident ends automated trading for the session. Once the §2 halt exists,
    # the owner is HALTED and nothing admits a further risk-add in this session.
    assert (account.permission, account.authority) == ("HALTED", "INTERVENTION")
    assert retry.refusal_reason is not None
    assert len(broker.commands) == 1


# -- S2: stale evidence ---------------------------------------------------------------------

def test_stale_broker_fact_halts_and_blocks_same_session_activation(tmp_path):
    account, broker = _rehearsal_owner(tmp_path, [BrokerResult("accepted"), BrokerResult("accepted")])
    assert _dispatch(account, intent(), "base", NOW).transport_state == "accepted"
    assert _state(account) == ("RUNNING", "NORMAL", 1)

    at = NOW + timedelta(seconds=5)
    _stale_fact_incident(account, at)
    assert _state(account) == ("HALTED", "INTERVENTION", 2)
    assert _incident_ids(account) == ("stale-fact:exec-stale",)
    assert _bootstrap(account)["invalidation"] == "incident:stale-fact:exec-stale"

    # A fresh, valid fact afterwards is recorded but restores nothing.
    fresh = BrokerFact.fill("exec-fresh", "base", "dj30_mym_p250", "entry", 1, 100.0, at)
    assert account.observe(fresh, now=at)
    assert _state(account) == ("HALTED", "INTERVENTION", 2)
    assert _incident_ids(account) == ("stale-fact:exec-stale",)

    later = at + timedelta(seconds=1)
    assert _dispatch(account, _other_leg_entry("after", later), "after",
                     later).refusal_reason == "intervention_fence"
    _assert_no_same_session_activation(account, later)
    assert len(broker.commands) == 1


def test_feed_silence_halt_survives_feed_recovery_in_session(tmp_path):
    account, broker = _rehearsal_owner(tmp_path, [BrokerResult("accepted")])
    _complete_bar(account, NOW)

    account.check_source_silence(now=NOW + SOURCE_TIMEOUT, max_silence=SOURCE_TIMEOUT)
    assert _state(account) == ("RUNNING", "NORMAL", 1)  # at the timeout, not past it

    expired = NOW + SOURCE_TIMEOUT + timedelta(seconds=1)
    account.check_source_silence(now=expired, max_silence=SOURCE_TIMEOUT)
    halted = _state(account)
    assert halted == ("HALTED", "INTERVENTION", 2)
    incident = "feed-silence:" + SESSION.session_id + ":" + NOW.isoformat()
    assert _incident_ids(account) == (incident,)
    assert account.incidents[0]["reason"] == "feed"

    # Fresh bars return; halt/resume §3: "No feed recovery ... clears permission."
    recovered = NOW + 3 * BAR_PERIOD
    _complete_bar(account, recovered)
    account.check_source_silence(now=recovered + timedelta(seconds=1), max_silence=SOURCE_TIMEOUT)
    assert _state(account) == halted
    assert _incident_ids(account) == (incident,)

    at = recovered + timedelta(seconds=2)
    assert _dispatch(account, intent("after-recovery"), "after-recovery",
                     at).refusal_reason == "intervention_fence"
    _assert_no_same_session_activation(account, at)
    assert broker.commands == []


# -- S3: missed alert (halt/resume §3, attendance) ------------------------------------------

def test_missed_acknowledgment_never_changes_halt_or_permission(tmp_path, monkeypatch):
    account, broker = _rehearsal_owner(tmp_path, [])
    at = NOW + timedelta(seconds=5)
    _stale_fact_incident(account, at)
    halted = account.status()
    incidents = account.incidents

    # No owner emits an incident notification (evidence note: ABSENT, owed to Phase 5 WP2 /
    # T13). The harness writes the alert itself, so this measures only the local consumer
    # (Phase 5 WP2: "mocks prove only the local consumer behavior").
    clock = {"now": at}
    telemetry = sys.modules[FileAckNotifier.__module__]
    monkeypatch.setattr(telemetry, "utc_now_iso", lambda: clock["now"].isoformat())
    notifier = FileAckNotifier(tmp_path / "alerts.jsonl", tmp_path / "acks")
    alert_id = "SYNTHETIC-REHEARSAL:" + incidents[0]["incident_id"]
    notifier.notify("CRITICAL", "SYNTHETIC REHEARSAL: incident halt", event_id=alert_id,
                    details={"incident_id": incidents[0]["incident_id"]})
    alert = json.loads((tmp_path / "alerts.jsonl").read_text(encoding="utf-8"))
    assert datetime.fromisoformat(alert["ts_utc"]) == at

    # Missed: nothing is acknowledged 60 s after the first notification attempt.
    clock["now"] = at + timedelta(seconds=60)
    assert not notifier.is_acknowledged(alert_id)
    assert account.status() == halted and account.incidents == incidents

    # Late acknowledgment at +180 s appends attendance only.
    clock["now"] = at + timedelta(seconds=180)
    ack = json.loads(notifier.acknowledge(alert_id, operator="synthetic-operator").read_text(encoding="utf-8"))
    assert notifier.is_acknowledged(alert_id)
    assert datetime.fromisoformat(ack["acked_utc"]) - datetime.fromisoformat(alert["ts_utc"]) \
        == timedelta(seconds=180)
    assert account.status() == halted and account.incidents == incidents

    later = at + timedelta(seconds=181)
    assert _dispatch(account, intent("after-ack"), "after-ack", later).refusal_reason == "intervention_fence"
    _assert_no_same_session_activation(account, later)
    assert broker.commands == []


# -- S4: restart during an incident halt (halt/resume §2 `:33`, settled) --------------------

def test_restart_during_incident_halt_boots_halted_with_new_generation(tmp_path):
    account, broker = _rehearsal_owner(tmp_path, [])
    at = NOW + timedelta(seconds=5)
    _stale_fact_incident(account, at)
    before = account.status()
    incidents = account.incidents
    assert before["generation"] == 2

    restarted = BookAccountOwner.boot(account.path, account.account, binding=account.binding,
                                      synthetic_broker=broker)
    after = restarted.status()
    assert (after["permission"], after["authority"]) == ("HALTED", "INTERVENTION")
    assert after["boot_id"] != before["boot_id"]
    assert after["generation"] == before["generation"] + 1
    assert restarted.incidents == incidents  # incident rows retained
    bootstrap = _bootstrap(restarted)
    assert bootstrap["state"] == "ineligible"
    assert bootstrap["invalidation"] == "incident:stale-fact:exec-stale"  # first reason kept


def test_activation_refused_after_incident_and_restart_in_same_session(tmp_path):
    account, broker = _rehearsal_owner(tmp_path, [])
    at = NOW + timedelta(seconds=5)
    _stale_fact_incident(account, at)
    for restart in range(2):
        account = BookAccountOwner.boot(account.path, account.account, binding=account.binding,
                                        synthetic_broker=broker)
        later = at + timedelta(seconds=1 + restart)
        assert _dispatch(account, intent("after-restart-%d" % restart), "after-restart-%d" % restart,
                         later).refusal_reason == "intervention_fence"
        _assert_no_same_session_activation(account, later)
    assert account.status()["generation"] == 4
    assert broker.commands == []


# -- S5: ambiguous protection (halt/resume §2 `:26`, protection fault) ----------------------

_AMBIGUITY = {
    "identity": lambda snapshot: {"account_epoch": "foreign-epoch"},
    "quantity": lambda snapshot: {"orders": tuple(replace(row, quantity=row.quantity + 1)
                                                  for row in snapshot.orders)},
    "ownership": lambda snapshot: {"positions": (("unowned-fill", 1),) + tuple(snapshot.positions)},
}


def _ambiguous_protection(tmp_path, kind):
    case = ProtectionScenario(tmp_path / kind)
    case.enter(("first", "second"), quantities=(1, 2), bracket=Bracket(stop=98))
    case.enter(("orb-fill",), bracket=None, leg="orb_mnq_v7")  # open, never protected
    snapshot = case.observe()
    assert {row.leg_id for row in snapshot.orders} == {"dj30_mym_p250"}
    assert _state(case.owner) == ("RUNNING", "NORMAL", 1)
    at = case.advance()
    ambiguous = replace(snapshot, fact_id="ambiguous-" + kind, sequence=snapshot.sequence + 1,
                        as_of=at, **_AMBIGUITY[kind](snapshot))
    case.owner.observe_protection(ambiguous, now=at)
    return case


def test_ambiguous_protection_halts_into_intervention_and_fences_mutations(tmp_path):
    for kind in _AMBIGUITY:
        case = _ambiguous_protection(tmp_path, kind)
        assert _state(case.owner) == ("HALTED", "INTERVENTION", 2), kind
        assert _incident_ids(case.owner) == ("protection:invalid-snapshot:ambiguous-" + kind,)
        assert case.owner.incidents[0]["reason"] == "protection"
        sent = len(case.broker.commands)
        mutations = {
            "tighten": BracketAmend("dj30_mym_p250", Bracket(stop=99)),
            "attach": BracketAmend("orb_mnq_v7", Bracket(stop=90)),
            "risk-add": replace(intent("risk-add"), leg_id="vanguard_mgc", qty=1),
            "cancel": Cancel("dj30_mym_p250"),
            "exit": replace(intent("exit"), kind="exit", side=Side.SELL, qty=1),
        }
        for name, action in mutations.items():
            result = case.dispatch(action, case.occurrence(kind + ":" + name))
            assert result.refusal_reason == "intervention_fence", (kind, name, result)
            assert result.transport_state == "not_attempted", (kind, name)
        assert len(case.broker.commands) == sent


def test_activation_refused_after_protection_incident_in_same_session(tmp_path):
    for kind in _AMBIGUITY:
        case = _ambiguous_protection(tmp_path, kind)
        _assert_no_same_session_activation(case.owner, case.advance())


# -- S6: operator stop (halt/resume §2 `:26`; O-6 decided 2026-09-27: incident) --------------

def test_operator_halt_leaves_no_same_session_activation_path(tmp_path):
    account, broker = _rehearsal_owner(tmp_path, [])
    assert _state(account) == ("RUNNING", "NORMAL", 1)
    at = NOW + timedelta(seconds=5)
    account.halt("operator-stop:synthetic", "operator", now=at)
    assert _state(account) == ("HALTED", "INTERVENTION", 2)
    assert account.incidents[0]["reason"] == "operator"
    account.halt("operator-stop:synthetic", "operator", now=at)  # duplicate report: idempotent
    assert _state(account) == ("HALTED", "INTERVENTION", 2)
    assert len(account.incidents) == 1

    later = at + timedelta(seconds=1)
    assert _dispatch(account, intent("after-stop"), "after-stop", later).refusal_reason == "intervention_fence"
    _assert_no_same_session_activation(account, later)
    assert broker.commands == []


# -- Structural: no permission transition to RUNNING other than bootstrap ------------------

_WRITE = re.compile(r"\b(INSERT|UPDATE|REPLACE)\b", re.IGNORECASE)
_OWNER_STATE_WRITE = re.compile(r"\b(INSERT\s+(OR\s+\w+\s+)?INTO|REPLACE\s+INTO|UPDATE)\s+owner_state\b",
                                re.IGNORECASE)
_RUNNING_OR_NORMAL = re.compile(r"'(RUNNING|NORMAL)'")
_BOUND_AUTHORITY = re.compile(r"\b(permission|authority)\s*=\s*\?", re.IGNORECASE)
_DYNAMIC_TARGET = re.compile(r"\b(INTO|UPDATE)\s*\{\}", re.IGNORECASE)
_OWNER_STATE_COLUMNS = ("schema", "account", "account_epoch", "boot_id", "generation",
                        "permission", "authority", "sequence")


def _rail_sql_strings():
    """Every string literal (implicitly concatenated) in ops/c1_rail/*.py, with its function."""
    for path in sorted(RAIL.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        functions = {}
        for function in ast.walk(tree):
            if isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for child in ast.walk(function):
                    functions.setdefault(id(child), []).append(function)
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                text = node.value
            elif isinstance(node, ast.JoinedStr):
                text = "".join(part.value if isinstance(part, ast.Constant) else "{}"
                               for part in node.values)
            else:
                continue
            enclosing = functions.get(id(node))
            # ast.walk is breadth-first, so the last function recorded is the innermost.
            name = enclosing[-1].name if enclosing else "<module>"
            yield path.name, name, " ".join(text.split()), isinstance(node, ast.JoinedStr)


def test_only_bootstrap_activation_writes_running_permission():
    strings = list(_rail_sql_strings())
    assert strings, "scan found no source"

    # A parameterized permission/authority value cannot be resolved by the scan: stop (§7).
    assert [s[:2] for s in strings if _BOUND_AUTHORITY.search(s[2])] == []
    # A write whose table name is formatted in could target owner_state unseen: stop (§7).
    assert [s[:3] for s in strings if s[3] and _WRITE.search(s[2]) and _DYNAMIC_TARGET.search(s[2])] == []

    sites = sorted((file, function, sql) for file, function, sql, _dynamic in strings
                   if _OWNER_STATE_WRITE.search(sql))
    # Read at 521d8f2 and re-read at the dispatch revision: book_account_owner.py:334, :388,
    # :680, :1748, :1873; book_bootstrap.py:174; book_migration.py:412. A new site is a
    # card §7 stop, not a test update.
    assert [(file, function) for file, function, _sql in sites] == [
        ("book_account_owner.py", "_advance_schedule_locked"),  # :1748 HALTED/SCHEDULED_EXIT
        ("book_account_owner.py", "_boot_locked"),        # :334 creation, HALTED/INTERVENTION
        ("book_account_owner.py", "_boot_locked"),        # :388 restart, HALTED/INTERVENTION
        ("book_account_owner.py", "_halt_db"),            # :1873 HALTED/INTERVENTION
        ("book_account_owner.py", "_next_sequence"),      # :680 sequence only
        ("book_bootstrap.py", "_activate_bootstrap"),     # :174 RUNNING/NORMAL
        ("book_migration.py", "migrate_book_owner"),      # :412 HALTED/INTERVENTION
    ]

    # Positional INSERTs must carry literal permission and authority values.
    for file, function, sql in sites:
        insert = re.search(r"INSERT\s+.*owner_state\s+VALUES\s*\((.*)\)", sql, re.IGNORECASE)
        if insert:
            values = [value.strip() for value in insert.group(1).split(",")]
            assert len(values) == len(_OWNER_STATE_COLUMNS), (file, function, sql)
            for column in ("permission", "authority"):
                value = values[_OWNER_STATE_COLUMNS.index(column)]
                assert value.startswith("'") and value.endswith("'"), (file, function, column)

    running = [(file, function, sql) for file, function, sql in sites if _RUNNING_OR_NORMAL.search(sql)]
    assert running == [("book_bootstrap.py", "_activate_bootstrap",
                        "UPDATE owner_state SET permission='RUNNING', authority='NORMAL'")]

    # No other SQL write anywhere in the rail sets RUNNING permission or NORMAL authority.
    elsewhere = [(file, function) for file, function, sql, _dynamic in strings
                 if _WRITE.search(sql) and re.search(r"\b(permission|authority)\s*=\s*'(RUNNING|NORMAL)'", sql)]
    assert elsewhere == [("book_bootstrap.py", "_activate_bootstrap")]


# -- S7: correctly handled refusals (halt/resume §2 `:35`, `:30` before expiry) --------------

def _assert_request_level(account, *, generation=1):
    assert _state(account) == ("RUNNING", "NORMAL", generation)
    assert account.incidents == ()


def test_capacity_refusal_leaves_session_running(tmp_path):
    # Settled at peak, so NORMAL mode: Aegis's fixed 8 contracts x 10 micros fill the 80-micro
    # account cap, and any further risk-add is a capacity refusal.
    settled = replace(binding()["settlement"], equity=100_000.0)
    account, broker = _rehearsal_owner(tmp_path, [BrokerResult("accepted")] * 2, settlement=settled)
    aegis = replace(intent("aegis"), leg_id="aegis_6j", qty=8, side=leg("aegis_6j").entry_side)
    first = _dispatch(account, aegis, "aegis", NOW)
    assert first.transport_state == "accepted" and account.exposure("aegis_6j") == (0, 8)

    refused = _dispatch(account, _other_leg_entry("orb", NOW), "orb", NOW)
    assert refused.refusal_reason == "insufficient_observed_capacity"
    assert refused.transport_state == "not_attempted"
    _assert_request_level(account)
    assert len(broker.commands) == 1

    # Capacity frees; the next valid request in the same session is admitted.
    freed = NOW + timedelta(seconds=1)
    account.observe(BrokerFact.terminal("aegis", "cancelled", 0, freed), now=freed)
    at = NOW + timedelta(seconds=2)
    admitted = _dispatch(account, _other_leg_entry("orb-next", at), "orb-next", at)
    assert admitted.transport_state == "accepted"
    _assert_request_level(account)
    assert len(broker.commands) == 2


def test_zero_size_sizing_refusal_leaves_session_running(tmp_path):
    account, broker = _rehearsal_owner(tmp_path, [BrokerResult("accepted")])
    refused = _dispatch(account, replace(intent("too-wide"), stop_dist_pts=10**6), "too-wide", NOW)
    assert refused.refusal_reason == "zero_size"
    assert refused.transport_state == "not_attempted"
    _assert_request_level(account)
    assert broker.commands == []

    admitted = _dispatch(account, intent("next"), "next", NOW)
    assert admitted.transport_state == "accepted" and admitted.quantity > 0
    _assert_request_level(account)
    assert len(broker.commands) == 1


def test_duplicate_signal_refusal_leaves_session_running(tmp_path):
    account, broker = _rehearsal_owner(tmp_path, [BrokerResult("accepted")] * 2)
    assert _dispatch(account, intent("signal"), "signal", NOW).transport_state == "accepted"

    # The same signal arriving again under a new delivery occurrence is recognized.
    duplicate = _dispatch(account, intent("signal"), "signal-redelivered", NOW)
    assert duplicate.refusal_reason == "duplicate_operation"
    assert duplicate.transport_state == "not_attempted"
    _assert_request_level(account)
    assert len(broker.commands) == 1

    admitted = _dispatch(account, _other_leg_entry("next", NOW), "next", NOW)
    assert admitted.transport_state == "accepted"
    _assert_request_level(account)
    assert len(broker.commands) == 2


def test_incomplete_barrier_before_expiry_leaves_session_running(tmp_path):
    account, broker = _rehearsal_owner(tmp_path, [BrokerResult("accepted")])
    for leg_id in LEGS[:3]:  # orb_mnq_v7 has not arrived: the barrier is incomplete
        account.record_partial_bar(leg_id, NOW, {"close": 100, "leg": leg_id}, acquired_at=NOW)
    assert len(account.retained_partial_bars) == 3
    assert account.retained_barriers == ()
    _assert_request_level(account)

    # Halt/resume §2 `:30`: expiry is bar_period + 30 s after the expected boundary. Before it,
    # nothing halts, and the next valid request is admitted.
    before_expiry = NOW + BAR_PERIOD + timedelta(seconds=29)
    admitted = _dispatch(account, intent("next"), "next", before_expiry)
    assert admitted.transport_state == "accepted"
    _assert_request_level(account)
    assert len(account.retained_partial_bars) == 3
    assert len(broker.commands) == 1
