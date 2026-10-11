"""Prepared protection continuations under an unhealthy source (D-7 = B)."""
from dataclasses import asdict, replace
from datetime import timedelta
import sqlite3

import pytest

from c1_rail.book_account_owner import FENCED_STATES, BrokerFact, BrokerResult
from c1_rail.book_protection import (
    ProtectionRead, bracket_from_dict, is_loosening, normalize_bracket, occurrence_key,
)
from c1_rail.book_protection_owner import PROTECTION_PERIOD
from c1_signal_daemon.book_adapters import ADAPTER_BY_LEG
from c1_signal_daemon.book_protocol import Bracket, BracketAmend, Side
from c1_signal_daemon.book_runtime import FourLegRuntime, _feedback
import test_four_leg_runtime as fixtures
from test_four_leg_runtime import NOW, LEGS, bars, entry, inert_adapters
from test_book_runtime_occurrences import waiting_runtime
from book_protection_fixtures import ProtectionScenario

LEG = "orb_mnq_v7"
SEEN = NOW + timedelta(seconds=3)  # boundary B is prepared here
T1, T2 = SEEN + timedelta(seconds=1), SEEN + timedelta(seconds=2)
ESTABLISHED, LOOSEN, TIGHTEN = Bracket(stop=98), Bracket(stop=97), Bracket(stop=99)
OMIT = object()


def extend(monkeypatch, **session):
    """test_book_loop_continuation.py:51-57's binding extension, plus a session variant."""
    original = fixtures.binding

    def extended(**kwargs):
        result = original(**kwargs)
        result["valid_until"] = NOW + timedelta(hours=1)
        result["max_evidence_age"] = timedelta(hours=1)
        if session:
            result["session"] = replace(result["session"], **session)
        return result
    monkeypatch.setattr(fixtures, "binding", extended)


def redeliver(runtime, now, healthy=OMIT):
    if healthy is OMIT:
        return runtime.redeliver_prepared_boundary(NOW, now=now)
    return runtime.redeliver_prepared_boundary(NOW, now=now, sources_healthy=healthy)


def filled_account(path, *, establish=ESTABLISHED):
    """One ORB fill with its entry's accepted terminal and, optionally, established protection."""
    path.mkdir()
    account = fixtures.owner(path, [])
    broker = account.synthetic_broker
    broker.queue(BrokerResult("accepted"))
    action = entry(LEG, 1)
    assert account.dispatch(action, occurrence=account.make_occurrence("direct", "entry"),
                            now=NOW).transport_state == "accepted"
    entry_id = broker.commands[0].operation_id
    account.observe(broker.execute_entry(entry_id, fill_id="base", quantity=1, price=100, at=NOW), now=NOW)
    broker.advance(NOW + timedelta(seconds=1))
    account.observe(BrokerFact.terminal(entry_id, "filled", 1, broker.now), now=broker.now)
    if establish is not None:
        amend, occurrence = BracketAmend(LEG, establish, ("base",)), account.make_occurrence("direct", "establish")
        assert account.dispatch(amend, occurrence=occurrence, now=broker.now).refusal_reason == "awaiting_evidence"
        broker.advance(NOW + timedelta(seconds=2))
        broker.queue(BrokerResult("accepted"))
        assert account.dispatch(amend, occurrence=occurrence, now=broker.now).transport_state == "accepted"
        command = broker.commands[-1]
        broker.apply(command.operation_id, outcome="applied", at=SEEN)
        account.observe_protection(broker.read_protection(ProtectionRead(command.occurrence, (LEG,), NOW)), now=SEEN)
        assert account.protection_owners[0].observed == establish
    broker.advance(SEEN)
    return account, broker


def established(path, bracket):
    """Boundary B (bar NOW, prepared at SEEN) carries one BracketAmend, awaiting evidence."""
    account, broker = filled_account(path)
    registry = inert_adapters()
    registry[LEG].actions = [BracketAmend(LEG, bracket, ("base",))]
    runtime = FourLegRuntime(account, registry)
    for _, raw in account.pending_feedback:
        registry[raw["leg_id"]].mode = runtime._desired_mode()
        runtime.deliver_confirmed_events((_feedback(raw),))
    for leg in LEGS:
        results = runtime.on_completed_bar(leg, bars()[leg], now=SEEN)
    assert [r.refusal_reason for r in results] == ["awaiting_evidence"]
    return account, broker, runtime


def attach_runtime(tmp_path, bracket):
    """Local copy of waiting_runtime (test_book_runtime_occurrences.py:40-64), bracket parameterised."""
    from c1_rail.book_synthetic_protection import SyntheticProtectionBroker
    account = fixtures.owner(tmp_path, [])
    occurrence = account.make_occurrence("direct", "entry")
    broker = SyntheticProtectionBroker([BrokerResult("accepted"), BrokerResult("accepted")],
        account=account.account, account_epoch=occurrence.account_epoch, at=NOW)
    account.synthetic_broker = broker
    action = entry(LEG, 1)
    account.dispatch(action, occurrence=occurrence, now=NOW)
    account.observe(broker.execute_entry(action.order_id, fill_id="runtime-base", quantity=1,
                                        price=100, at=NOW), now=NOW)
    registry = inert_adapters()
    registry[LEG].actions = [BracketAmend(LEG, bracket, ("runtime-base",))]
    runtime = FourLegRuntime(account, registry)
    for _, raw in account.pending_feedback:
        registry[raw["leg_id"]].mode = runtime._desired_mode()
        runtime.deliver_confirmed_events((_feedback(raw),))
    for leg in LEGS:
        results = runtime.on_completed_bar(leg, bars()[leg], now=NOW)
    assert results[0].refusal_reason == "awaiting_evidence"
    assert not account.retained_barriers[0]["completed"]
    return account, broker, runtime


def row(account, fid="base"):
    with account._transaction() as db:
        return account._protection_rows(db)["protection:" + fid]


def child(account, ordinal=0):
    occurrence = account.make_occurrence("runtime", NOW.isoformat(), ordinal)
    identity = "control:" + occurrence_key(occurrence) + ":0"
    with account._transaction() as db:
        op = account._protection_operations(db)[identity]
        reserved = db.execute("SELECT 1 FROM operations WHERE operation_id=?", (identity,)).fetchone()
    return occurrence, identity, op, reserved is not None


def generation(account):
    with account._transaction() as db:
        return account._state(db)["generation"]


def effective(bracket, leg=LEG, side=Side.BUY):
    return normalize_bracket(bracket, side, ADAPTER_BY_LEG[leg].mintick)


def assert_premise(account, now, bracket, *, loosening, fid="base", leg=LEG):
    """The owner's own loosening test on the row, and no fenced request state (§3)."""
    current = row(account, fid)
    observed, side = bracket_from_dict(current["observed"]), Side(current["side"])
    assert current["ever_protected"] and observed is not None
    assert is_loosening(observed, effective(bracket, leg, side), side) is loosening
    assert not set(account.request_classification(now=now).values()) & set(FENCED_STATES)


def protection_commands(broker, start=0):
    return [c for c in broker.commands[start:] if c.protection_change is not None]


def dump(account):
    db = sqlite3.connect(account.path)
    try:
        return tuple(db.iterdump())
    finally:
        db.close()


# F1 ---------------------------------------------------------------------------------------

def test_f1_unhealthy_loosening_is_held_then_sent_on_healthy_step(tmp_path, monkeypatch):
    extend(monkeypatch)
    account, broker, runtime = established(tmp_path / "f1", LOOSEN)
    assert_premise(account, T1, LOOSEN, loosening=True)
    feedback, sent = account.all_feedback, len(broker.commands)
    broker.advance(T1)
    held = runtime.redeliver_prepared_boundary(NOW, now=T1, sources_healthy=False)
    assert [r.refusal_reason for r in held] == ["held_unhealthy"]
    assert [r.transport_state for r in held] == ["not_attempted"]
    assert len(broker.commands) == sent
    occurrence, identity, op, reserved = child(account)
    state = account.occurrence_state(occurrence)
    assert state["state"] == "awaiting_evidence" and not state["attempted"]
    assert op["status"] == "awaiting_evidence" and not reserved
    protected = row(account)
    assert protected["pending_operation"] == identity
    assert protected["deadline"] == (SEEN + PROTECTION_PERIOD).isoformat()
    assert runtime.pending_bar_times == (NOW,)
    assert not account.retained_barriers[0]["completed"]
    assert account.all_feedback == feedback  # no local refusal, delivered or pending
    broker.advance(T2)
    broker.queue(BrokerResult("accepted"))
    sent_results = redeliver(runtime, T2)
    assert [r.transport_state for r in sent_results] == ["accepted"]
    assert len(broker.commands) == sent + 1
    assert broker.commands[-1].protection_change.effective == effective(LOOSEN)
    assert account.retained_barriers[0]["completed"]
    assert runtime.pending_bar_times == ()


# F2 ---------------------------------------------------------------------------------------

@pytest.mark.parametrize("value", [0, None, "False", object()], ids=["zero", "none", "text", "object"])
def test_f2_sources_healthy_requires_exact_bool(tmp_path, monkeypatch, value):
    extend(monkeypatch)
    account, broker, runtime = established(tmp_path / "f2", LOOSEN)
    broker.advance(T1)
    before, sent = dump(account), len(broker.commands)
    # Unowned bar_time: only the runtime's own check can raise (before :436-437 returns ()).
    with pytest.raises(TypeError, match="sources_healthy must be bool"):
        runtime.redeliver_prepared_boundary(NOW + timedelta(minutes=15), now=T1, sources_healthy=value)
    with pytest.raises(TypeError, match="sources_healthy must be bool"):
        runtime.redeliver_prepared_boundary(NOW, now=T1, sources_healthy=value)
    with pytest.raises(TypeError, match="sources_healthy must be bool"):
        account.dispatch(BracketAmend(LEG, TIGHTEN, ("base",)),
                         occurrence=account.make_occurrence("direct", "f2"), now=T1, sources_healthy=value)
    assert len(broker.commands) == sent
    assert dump(account) == before
    assert not getattr(account, "_input_send_suppressed", False)
    assert runtime.pending_bar_times == (NOW,)


# G1 ---------------------------------------------------------------------------------------

@pytest.mark.parametrize("bracket, reason", [(TIGHTEN, None), (ESTABLISHED, "unchanged_protection")],
                         ids=["tighten", "equal"])
def test_g1_unhealthy_tightening_is_sent(tmp_path, monkeypatch, bracket, reason):
    extend(monkeypatch)
    sent = {}
    for healthy in (False, True):
        account, broker, runtime = established(tmp_path / str(healthy), bracket)
        assert_premise(account, T1, bracket, loosening=False)
        start = len(broker.commands)
        broker.advance(T1)
        broker.queue(BrokerResult("accepted"))
        results = redeliver(runtime, T1, healthy)
        assert [r.refusal_reason for r in results] == [reason]
        sent[healthy] = [(c.kind, c.quantity, c.protection_change.target.primitive, c.protection_change.effective)
                         for c in protection_commands(broker, start)]
        assert account.retained_barriers[0]["completed"]
        assert runtime.pending_bar_times == ()
    assert sent[False] == sent[True]
    assert len(sent[False]) == (0 if reason else 1)


# G2 ---------------------------------------------------------------------------------------

@pytest.mark.parametrize("bracket", [Bracket(stop=98), Bracket(stop=98, limit=105)], ids=["stop", "limit"])
def test_g2_unhealthy_first_attach_with_fresh_evidence_is_sent(tmp_path, bracket):
    account, broker, runtime = attach_runtime(tmp_path, bracket)
    target = row(account, "runtime-base")
    assert not target["ever_protected"] and target["observed"] is None
    # is_loosening alone reads a limit as loosening against None; the owner never does for an attach.
    assert is_loosening(None, effective(bracket), Side.BUY) is (bracket.limit is not None)
    broker.advance(NOW + timedelta(seconds=1))
    results = redeliver(runtime, broker.now, False)
    assert [r.transport_state for r in results] == ["accepted"]
    commands = protection_commands(broker)
    assert len(commands) == 1
    assert commands[0].protection_change.target.primitive == "attach"
    assert commands[0].protection_change.effective == effective(bracket)
    assert account.retained_barriers[0]["completed"]
    assert runtime.pending_bar_times == ()


# G3 ---------------------------------------------------------------------------------------

def test_g3_attach_without_evidence_waits_and_halt_replays_stored_result(tmp_path):
    account, broker, runtime = waiting_runtime(tmp_path)
    broker.drop_reads = True
    broker.advance(NOW + timedelta(seconds=1))
    results = redeliver(runtime, broker.now, False)
    assert [r.refusal_reason for r in results] == ["awaiting_evidence"]
    assert len(broker.commands) == 1
    assert runtime.pending_bar_times == (NOW,)
    before = generation(account)
    account.halt("g3-feed-halt", "feed", now=broker.now)
    assert generation(account) == before + 1
    broker.drop_reads = False
    broker.advance(NOW + timedelta(seconds=2))
    replayed = redeliver(runtime, broker.now)
    assert [r.refusal_reason for r in replayed] == ["awaiting_evidence"]
    assert len(broker.commands) == 1
    assert runtime.pending_bar_times == (NOW,)


# G4 ---------------------------------------------------------------------------------------

@pytest.mark.parametrize("kind", ["tighten", "attach", "loosen"])
def test_g4_hold_never_replaces_fence_on_fresh_dispatch(tmp_path, monkeypatch, kind):
    extend(monkeypatch)
    account, broker = filled_account(tmp_path / kind, establish=None if kind == "attach" else ESTABLISHED)
    bracket = {"tighten": TIGHTEN, "attach": ESTABLISHED, "loosen": LOOSEN}[kind]
    if kind == "attach":
        read = broker.read_protection(ProtectionRead(account.make_occurrence("direct", "read"), (LEG,), NOW))
        account.observe_protection(read, now=SEEN)
        target = row(account)
        assert not target["ever_protected"] and target["observed"] is None and target["evidence_at"]
    else:
        assert_premise(account, SEEN, bracket, loosening=kind == "loosen")
    sent = len(broker.commands)
    account.halt("g4-feed-halt", "feed", now=SEEN)
    broker.advance(T1)
    broker.queue(BrokerResult("accepted"))
    result = account.dispatch(BracketAmend(LEG, bracket, ("base",)),
                              occurrence=account.make_occurrence("direct", "g4-" + kind), now=T1,
                              sources_healthy=False)
    assert result.refusal_reason == "intervention_fence"
    assert len(broker.commands) == sent


# G5 ---------------------------------------------------------------------------------------

def test_g5_outside_session_loosening_is_still_refused(tmp_path, monkeypatch):
    extend(monkeypatch, risk_add_cutoff=T1)
    account, broker, runtime = established(tmp_path / "g5", LOOSEN)
    assert_premise(account, T1, LOOSEN, loosening=True)
    assert account.authority == "NORMAL"
    broker.advance(T1)
    results = redeliver(runtime, T1, False)
    assert [r.refusal_reason for r in results] == ["risk_add_not_authorized"]
    occurrence, identity, op, reserved = child(account)
    assert op["status"] == "refused"
    assert not reserved
    protected = row(account)
    assert protected["pending_operation"] is None and protected["deadline"] is None
    sent = len(broker.commands)
    broker.advance(T2)
    broker.queue(BrokerResult("accepted"))
    assert redeliver(runtime, T2) == ()
    assert len(broker.commands) == sent


# G6 ---------------------------------------------------------------------------------------

@pytest.mark.parametrize("scope", [("first", "second"), ("second", "first")], ids=["loosen-first", "tighten-first"])
def test_g6_mixed_scope_parent_is_held_whole(tmp_path, scope):
    leg = "dj30_mym_p250"
    scenario = ProtectionScenario(tmp_path)
    scenario.enter(("first", "second"), quantities=(1, 2))
    scenario.establish("first", Bracket(stop=98))
    scenario.establish("second", Bracket(stop=96))
    action = BracketAmend(leg, Bracket(stop=97), scope)
    occurrence = scenario.occurrence("mixed")
    assert scenario.dispatch(action, occurrence).refusal_reason == "awaiting_evidence"
    scenario.advance()
    assert_premise(scenario.owner, scenario.now, action.bracket, loosening=True, fid="first", leg=leg)
    assert_premise(scenario.owner, scenario.now, action.bracket, loosening=False, fid="second", leg=leg)
    sent = len(scenario.protection_commands)
    scenario.broker.queue(BrokerResult("accepted"))
    scenario.broker.queue(BrokerResult("accepted"))
    held = scenario.owner.dispatch(action, occurrence=occurrence, now=scenario.now, sources_healthy=False)
    assert held.refusal_reason == "held_unhealthy"
    assert len(scenario.protection_commands) == sent
    assert scenario.owner.occurrence_state(occurrence)["state"] == "awaiting_evidence"
    scenario.advance()
    released = scenario.owner.dispatch(action, occurrence=occurrence, now=scenario.now)
    assert released.transport_state == "accepted"
    commands = scenario.protection_commands[sent:]
    assert sorted(c.protection_change.target.owner_id for c in commands) == ["protection:first", "protection:second"]


# G7 ---------------------------------------------------------------------------------------

def observation(account, broker, results):
    """Commands, results and owner rows with random identifiers replaced by placeholders."""
    with account._transaction() as db:
        state = account._state(db)
        keys = [r[0] for r in db.execute("SELECT key FROM action_occurrences ORDER BY rowid")]
        attempts = [r[0] for r in db.execute("SELECT attempt_id FROM attempts ORDER BY rowid")]
        tables = {name: [tuple(r) for r in db.execute("SELECT * FROM " + name + " ORDER BY rowid")]
                  for name in ("action_occurrences", "protection_operations", "protection_owners")}
    commands = [(c.operation_id, c.kind, c.quantity,
                 c.protection_change and (c.protection_change.target.primitive, c.protection_change.effective))
                for c in broker.commands]
    text = repr((commands, [asdict(r) for r in results], tables))
    tokens = [(account.make_occurrence("direct", "x").account_epoch, "<epoch>"), (state["boot_id"], "<boot>")]
    tokens += [(k, "<key%d>" % i) for i, k in enumerate(keys)] + [(a, "<attempt%d>" % i) for i, a in enumerate(attempts)]
    for value, placeholder in sorted(tokens, key=lambda item: -len(item[0])):
        text = text.replace(value, placeholder)
    return text


def trace(name, path, healthy):
    if name in ("f1", "g1", "g5"):
        account, broker, runtime = established(path, {"f1": LOOSEN, "g1": TIGHTEN, "g5": LOOSEN}[name])
        broker.advance(T1)
        broker.queue(BrokerResult("accepted"))
        results = list(redeliver(runtime, T1, healthy))
        if name == "f1":
            assert [r.transport_state for r in results] == ["accepted"]  # sent at step 1, as on the base
    else:
        path.mkdir()
        account, broker, runtime = (attach_runtime(path, Bracket(stop=98, limit=105)) if name == "g2"
                                    else waiting_runtime(path))
        broker.drop_reads = name == "g3"
        broker.advance(NOW + timedelta(seconds=1))
        results = list(redeliver(runtime, broker.now, healthy))
        if name == "g3":
            account.halt("g7-feed-halt", "feed", now=broker.now)
            broker.drop_reads = False
            broker.advance(NOW + timedelta(seconds=2))
            results += redeliver(runtime, broker.now, healthy)
    return observation(account, broker, results)


@pytest.mark.parametrize("name", ["f1", "g1", "g2", "g3", "g5"])
def test_g7_healthy_step_equals_omitted_input(tmp_path, monkeypatch, name):
    extend(monkeypatch, **({"risk_add_cutoff": T1} if name == "g5" else {}))
    assert trace(name, tmp_path / "omitted", OMIT) == trace(name, tmp_path / "true", True)


# G8 ---------------------------------------------------------------------------------------

@pytest.mark.parametrize("halt", [False, True], ids=["no-halt", "feed-halt"])
def test_g8_hold_keeps_its_deadline(tmp_path, monkeypatch, halt):
    extend(monkeypatch)
    account, broker, runtime = established(tmp_path / "g8", LOOSEN)
    broker.advance(T1)
    assert [r.refusal_reason for r in redeliver(runtime, T1, False)] == ["held_unhealthy"]
    _, identity, _, _ = child(account)
    sent = len(broker.commands)
    if halt:
        account.halt("g8-feed-halt", "feed", now=T1)
        broker.advance(T2)
        replayed = redeliver(runtime, T2)
        assert [r.refusal_reason for r in replayed] == ["held_unhealthy"]
        assert len(broker.commands) == sent
        assert runtime.pending_bar_times == (NOW,)
    fault = "protection:deadline:" + identity
    deadline = SEEN + PROTECTION_PERIOD
    account.check_protection_deadlines(now=deadline - timedelta(microseconds=1))
    assert fault not in [i["incident_id"] for i in account.incidents]
    account.check_protection_deadlines(now=deadline)
    assert fault in [i["incident_id"] for i in account.incidents]
    assert account.protection_owners[0].observed == ESTABLISHED
    assert len(broker.commands) == sent
