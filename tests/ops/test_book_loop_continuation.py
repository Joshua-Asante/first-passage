"""The live loop continues retained evidence waits without replaying adapters."""
from dataclasses import replace
from datetime import timedelta

import pytest

from c1_rail.book_account_owner import BookAccountOwner
from c1_rail.book_protection import ProtectionRead
from c1_signal_daemon.book_evaluate_loop import FourLegEvaluateLoop
from c1_signal_daemon.book_runtime import FourLegRuntime
from test_book_runtime_occurrences import waiting_runtime
from test_four_leg_runtime import NOW, LEGS, bars, binding, inert_adapters
from book_bootstrap_fixtures import BootstrapBroker


class Source:
    def __init__(self):
        self.bars = []

    def poll(self):
        return self.bars.pop(0) if self.bars else None


def loop_for(runtime):
    return FourLegEvaluateLoop(sources={leg: Source() for leg in LEGS}, runtime=runtime)


def test_loop_continues_delayed_evidence_once_without_replaying_adapter(tmp_path):
    account, broker, runtime = waiting_runtime(tmp_path)
    loop = loop_for(runtime)
    before = runtime.observable_state()["adapters"]
    broker.drop_reads = True
    broker.advance(NOW + timedelta(seconds=1))
    waiting = loop.step(now=broker.now)
    assert waiting[0].refusal_reason == "awaiting_evidence"
    assert runtime.pending_bar_times == (NOW,)
    assert len(broker.commands) == 1
    broker.drop_reads = False
    broker.advance(NOW + timedelta(seconds=2))
    completed = loop.step(now=broker.now)
    assert completed[0].transport_state == "accepted"
    assert account.retained_barriers[0]["completed"]
    assert runtime.pending_bar_times == ()
    assert runtime.observable_state()["adapters"] == before
    assert loop.step(now=broker.now) is None
    assert len(broker.commands) == 2


def test_loop_continuation_allows_following_boundary(tmp_path, monkeypatch):
    import test_four_leg_runtime as fixtures
    original = fixtures.binding
    def extended_binding(**kwargs):
        result = original(**kwargs)
        result["valid_until"] = NOW + timedelta(hours=1)
        result["max_evidence_age"] = timedelta(hours=1)
        return result
    monkeypatch.setattr(fixtures, "binding", extended_binding)
    account, broker, runtime = waiting_runtime(tmp_path)
    loop = loop_for(runtime)
    broker.advance(NOW + timedelta(seconds=1))
    loop.step(now=broker.now)
    assert account.retained_barriers[0]["completed"]
    command = broker.commands[-1]
    broker.apply(command.operation_id, outcome="applied", at=NOW + timedelta(seconds=2))
    snapshot = broker.read_protection(ProtectionRead(command.occurrence, ("orb_mnq_v7",), NOW))
    runtime.observe_protection(snapshot, now=broker.now)
    next_time = NOW + timedelta(minutes=15)
    for leg, bar in bars().items():
        loop.sources[leg].bars.append(replace(bar, ts=next_time))
    assert loop.step(now=next_time) == ()
    assert account.authority == "NORMAL"
    assert len(account.retained_barriers) == 2
    assert all(row["completed"] for row in account.retained_barriers)
    assert len(broker.commands) == 2


@pytest.mark.parametrize("restart", [False, True])
def test_reconstructed_loop_never_resends_prepared_boundary(tmp_path, restart):
    account, broker, runtime = waiting_runtime(tmp_path)
    if restart:
        account = BookAccountOwner.boot(account.path, account.account, binding=binding(),
                                        synthetic_broker=BootstrapBroker([]))
    another = FourLegRuntime(account, inert_adapters())
    broker.advance(NOW + timedelta(seconds=1))
    assert loop_for(another).step(now=broker.now) is None
    assert not account.retained_barriers[0]["completed"]
    assert len(broker.commands) == 1
    if restart:
        assert account.authority == "INTERVENTION"
        assert account.synthetic_broker.commands == []


def test_expired_evidence_wait_halts_before_loop_continuation(tmp_path):
    account, broker, runtime = waiting_runtime(tmp_path)
    late = NOW + timedelta(minutes=15)
    broker.advance(late)
    assert loop_for(runtime).step(now=late) is None
    assert account.authority == "INTERVENTION"
    assert len(broker.commands) == 1
