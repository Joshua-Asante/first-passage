"""Runtime provenance is retained before dispatch and is stable on replay."""
from dataclasses import asdict
from datetime import timedelta

from c1_signal_daemon.book_protocol import Bracket, BracketAmend, Cancel
from c1_signal_daemon.book_runtime import FourLegRuntime
from c1_signal_daemon.book_evaluate_loop import FourLegEvaluateLoop
from test_four_leg_runtime import NOW, LEGS, bars, inert_adapters, owner, entry


def test_sorted_batch_includes_mode_action_occurrences(tmp_path):
    account = owner(tmp_path, [])
    registry = inert_adapters()
    registry[LEGS[0]].set_mode = lambda mode: [Cancel(LEGS[0])]
    registry[LEGS[-1]].actions = [Cancel(LEGS[-1])]
    runtime = FourLegRuntime(account, registry)
    for leg in LEGS:
        runtime.on_completed_bar(leg, bars()[leg], now=NOW)
    retained = account.retained_barriers[0]
    assert retained["completed"]
    assert [row["occurrence"]["ordinal"] for row in retained["actions"]] == [0, 1]
    assert all(row["occurrence"] == asdict(account.make_occurrence(
        "runtime", NOW.isoformat(), index))
        for index, row in enumerate(retained["actions"]))


def test_idle_loop_checks_protection_deadlines(tmp_path):
    account = owner(tmp_path, [])
    runtime = FourLegRuntime(account, inert_adapters())
    checks = []
    account.check_protection_deadlines = lambda *, now: checks.append(now)
    class Source:
        def poll(self):
            return None
    loop = FourLegEvaluateLoop(sources={leg: Source() for leg in LEGS}, runtime=runtime)
    assert loop.step(now=NOW) is None
    assert checks == [NOW]


def waiting_runtime(tmp_path):
    from c1_rail.book_account_owner import BrokerResult
    from c1_rail.book_synthetic_protection import SyntheticProtectionBroker
    account = owner(tmp_path, [])
    occurrence = account.make_occurrence("direct", "entry")
    broker = SyntheticProtectionBroker([BrokerResult("accepted"), BrokerResult("accepted")],
        account=account.account, account_epoch=occurrence.account_epoch, at=NOW)
    account.synthetic_broker = broker
    action = entry("orb_mnq_v7", 1)
    account.dispatch(action, occurrence=occurrence, now=NOW)
    account.observe(broker.execute_entry(action.order_id, fill_id="runtime-base", quantity=1,
                                        price=100, at=NOW), now=NOW)
    registry = inert_adapters()
    registry["orb_mnq_v7"].actions = [BracketAmend("orb_mnq_v7", Bracket(stop=98), ("runtime-base",))]
    runtime = FourLegRuntime(account, registry)
    # Deliver the committed setup fill before the first strategy boundary.
    from c1_signal_daemon.book_runtime import _feedback
    for _, raw in account.pending_feedback:
        registry[raw["leg_id"]].mode = runtime._desired_mode()
        runtime.deliver_confirmed_events((_feedback(raw),))
    for leg in LEGS:
        results = runtime.on_completed_bar(leg, bars()[leg], now=NOW)
    assert results[0].refusal_reason == "awaiting_evidence"
    assert not account.retained_barriers[0]["completed"]
    return account, broker, runtime


def test_prepared_boundary_continues_original_batch_without_adapter_reevaluation(tmp_path):
    account, broker, runtime = waiting_runtime(tmp_path)
    before = account.retained_barriers[0]["actions"]
    for adapter in runtime.adapters.values():
        adapter.on_bar = lambda bar: (_ for _ in ()).throw(AssertionError("reevaluated"))
    broker.advance(NOW + timedelta(seconds=1))
    results = runtime.redeliver_prepared_boundary(NOW, now=broker.now)
    assert results[0].transport_state == "accepted"
    assert account.retained_barriers[0]["completed"]
    assert account.retained_barriers[0]["actions"] == before
    assert len(broker.commands) == 2
    assert runtime.redeliver_prepared_boundary(NOW, now=broker.now) == ()
    assert len(broker.commands) == 2


def test_reconstructed_runtime_cannot_continue_prepared_boundary(tmp_path):
    account, broker, runtime = waiting_runtime(tmp_path)
    another = FourLegRuntime(account, inert_adapters())
    broker.advance(NOW + timedelta(seconds=1))
    assert another.redeliver_prepared_boundary(NOW, now=broker.now) == ()
    assert not account.retained_barriers[0]["completed"]
    assert len(broker.commands) == 1


def test_waiting_boundary_keeps_slot_when_partial_bar_expiry_runs(tmp_path):
    account, broker, runtime = waiting_runtime(tmp_path)
    runtime.expire_barrier(NOW, now=NOW + timedelta(minutes=16))
    assert runtime.pending_bar_times == (NOW,)
    assert not account.retained_barriers[0]["completed"]


def test_listener_protective_execution_delivers_once_without_resuming_takeover(tmp_path):
    from c1_rail.book_protection import ProtectionRead
    from c1_rail.c1_rail_listener import handle_book_protection, handle_book_protection_execution
    account, broker, runtime = waiting_runtime(tmp_path)
    broker.advance(NOW + timedelta(seconds=1))
    runtime.redeliver_prepared_boundary(NOW, now=broker.now)
    command = broker.commands[-1]
    broker.apply(command.operation_id, outcome="applied", at=NOW + timedelta(seconds=2))
    snapshot = broker.read_protection(ProtectionRead(command.occurrence, ("orb_mnq_v7",), NOW))
    handle_book_protection(snapshot, account, now=broker.now)
    account.resume_takeover = lambda **kwargs: (_ for _ in ()).throw(AssertionError("observer resumed takeover"))
    event = broker.execute_protection("protection:runtime-base", quantity=1, price=98,
                                      terminal=True, at=NOW + timedelta(seconds=3))
    before = len(runtime.adapters["orb_mnq_v7"].events)
    feedback = handle_book_protection_execution(event, account, runtime, now=broker.now)
    assert len(feedback) == 1
    assert len(runtime.adapters["orb_mnq_v7"].events) == before + 1
    assert account.exposure("orb_mnq_v7") == (0, 0)
    assert handle_book_protection_execution(event, account, runtime, now=broker.now) == ()
    assert len(runtime.adapters["orb_mnq_v7"].events) == before + 1
