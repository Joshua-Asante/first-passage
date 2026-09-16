"""Completed-bar synchronization and feedback recovery use the durable listener owner."""
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sqlite3
import threading

import pytest

from book_policy import candidate_book_protection_policy
from book_sizing_context import BookSession, SettledClose
from c1_rail.book_account_owner import (
    AccountOwnerError,
    BookAccountOwner,
    BrokerFact,
    BrokerResult,
    SyntheticBroker,
)
from c1_signal_daemon.book_protocol import FillTiming, Mode, OrderIntent, Side
from c1_signal_daemon.book_adapters import (
    ADAPTERS,
    load_book_adapters,
    port_sha256,
    synthetic_adapter_registry,
)
from c1_signal_daemon.book_runtime import FourLegRuntime, SimulatedRuntimeCrash
from c1_signal_daemon.book_evaluate_loop import FourLegEvaluateLoop
from c1_signal_daemon.feed import Bar
from c1_rail.c1_rail_listener import handle_book_fact


NOW = datetime(2026, 9, 15, 14, tzinfo=timezone.utc)
LEGS = ("aegis_6j", "dj30_mym_p250", "vanguard_mgc", "orb_mnq_v7")


def binding(*, protected=False):
    session = BookSession(
        "tradeify-account-day:2026-09-15", "tradeify-account-day:2026-09-14",
        NOW - timedelta(hours=1), NOW + timedelta(hours=1),
        NOW + timedelta(hours=2), "c" * 64,
        NOW + timedelta(hours=1, minutes=10),
        NOW + timedelta(hours=1, minutes=15),
    )
    equity = 98_500.0 if protected else 100_000.0
    return {
        "session": session,
        "settlement": SettledClose(session.prior_session_id,
                                    session.opens_at - timedelta(minutes=1),
                                    equity, 100_000.0, "e" * 64),
        "policy": candidate_book_protection_policy(),
        "policy_digest": "d" * 64,
        "snapshot_digest": "a" * 64,
        "as_of": NOW - timedelta(seconds=1),
        "valid_until": NOW + timedelta(minutes=5),
        "max_evidence_age": timedelta(seconds=30),
        "lifecycle_tiers": {leg: "AUTHORIZED" for leg in LEGS},
        "cap_allocations": {leg: 80 for leg in LEGS},
        "risk_dollars": {"dj30_mym_p250": 100},
    }


class Adapter:
    def __init__(self, leg_id, actions=()):
        self.leg_id = leg_id
        self.actions = list(actions)
        self.mode = None
        self.bars = []
        self.events = []
        self.history = []

    def set_mode(self, mode):
        self.mode = mode
        return []

    def on_bar(self, bar):
        self.bars.append(bar.ts.isoformat())
        self.history.append(("bar", bar.ts.isoformat()))
        return list(self.actions)

    def on_execution(self, event):
        self.events.append((event.event, event.order_id,
                            event.fill.fill_id if event.fill else None))
        self.history.append(("event", event.fill.fill_id if event.fill else event.order_id))

    def checkpoint(self):
        return {"mode": self.mode.value, "bars": list(self.bars),
                "events": list(self.events), "history": list(self.history)}


def entry(leg_id, qty, *, stop=1):
    side = Side.SELL if leg_id == "aegis_6j" else Side.BUY
    return OrderIntent("entry:" + leg_id, leg_id, "entry", side, qty,
                       timing=FillTiming.THIS_CLOSE, stop_dist_pts=stop,
                       bar_time=NOW)


def adapters():
    return synthetic_adapter_registry({
        "aegis_6j": Adapter("aegis_6j", [entry("aegis_6j", 8)]),
        "dj30_mym_p250": Adapter("dj30_mym_p250", [entry("dj30_mym_p250", 5, stop=24)]),
        "vanguard_mgc": Adapter("vanguard_mgc", [entry("vanguard_mgc", 2)]),
        "orb_mnq_v7": Adapter("orb_mnq_v7", [entry("orb_mnq_v7", 1)]),
    })


def inert_adapters():
    return synthetic_adapter_registry({leg_id: Adapter(leg_id) for leg_id in LEGS})


def bars():
    return {leg: Bar(NOW, 100, 101, 99, 100, 10) for leg in LEGS}


def owner(tmp_path, results, *, protected=False):
    result = BookAccountOwner.boot(
        tmp_path / "owner.sqlite", "synthetic-account",
        binding=binding(protected=protected),
        synthetic_broker=SyntheticBroker(results),
    )
    result.activate_synthetic(now=NOW)
    return result


@pytest.mark.parametrize("arrival", [LEGS, tuple(reversed(LEGS))])
def test_same_bar_capacity_winner_is_independent_of_arrival_order(tmp_path, arrival):
    account = owner(tmp_path, [BrokerResult("accepted")])
    runtime = FourLegRuntime(account, adapters())
    result = None
    for leg_id in arrival:
        result = runtime.on_completed_bar(leg_id, bars()[leg_id], now=NOW)

    assert [row.operation_id for row in result] == [
        "entry:aegis_6j", "entry:dj30_mym_p250", "entry:vanguard_mgc", "entry:orb_mnq_v7"
    ]
    assert result[0].transport_state == "accepted"
    assert [row.refusal_reason for row in result[1:]] == [
        "insufficient_observed_capacity", "insufficient_observed_capacity",
        "insufficient_observed_capacity",
    ]
    assert [command.leg_id for command in account.synthetic_broker.commands] == ["aegis_6j"]
    assert account.exposure("aegis_6j") == (0, 8)
    for leg_id in LEGS[1:]:
        assert runtime.adapters[leg_id].events == [
            ("reject", "entry:" + leg_id, None)
        ]


def test_local_capacity_refusals_are_durable_adapter_feedback(tmp_path):
    account = owner(tmp_path, [BrokerResult("accepted")])
    runtime = FourLegRuntime(account, adapters())
    for leg_id in LEGS:
        runtime.on_completed_bar(leg_id, bars()[leg_id], now=NOW)

    assert account.pending_feedback == ()
    assert len(account.all_feedback) == 3

    restarted = BookAccountOwner.boot(
        account.path, "synthetic-account", binding=binding(),
        synthetic_broker=SyntheticBroker([]),
    )
    fresh = adapters()
    FourLegRuntime.recover(restarted, fresh)

    for leg_id in LEGS[1:]:
        assert fresh[leg_id].events == [("reject", "entry:" + leg_id, None)]
    assert restarted.synthetic_broker.commands == []


def test_fact_commit_before_feedback_recovers_without_resend(tmp_path):
    fact = BrokerFact.fill("fill-aegis", "entry:aegis_6j", "aegis_6j",
                           "entry", 1, 100.0, NOW)
    account = owner(tmp_path, [BrokerResult("accepted", (fact,))])
    runtime = FourLegRuntime(account, adapters(), crash_after_dispatch=True)
    with pytest.raises(SimulatedRuntimeCrash):
        for leg_id in LEGS:
            runtime.on_completed_bar(leg_id, bars()[leg_id], now=NOW)

    restarted = BookAccountOwner.boot(
        tmp_path / "owner.sqlite", "synthetic-account", binding=binding(),
        synthetic_broker=SyntheticBroker([]),
    )
    fresh = adapters()
    recovered = FourLegRuntime.recover(restarted, fresh)

    assert restarted.permission == "HALTED"
    assert fresh["aegis_6j"].checkpoint()["events"] == [
        ("fill", "entry:aegis_6j", "fill-aegis")
    ]
    assert recovered.pending_feedback == ()
    assert restarted.synthetic_broker.commands == []


def test_missing_bar_expiry_halts_whole_book_without_dispatch(tmp_path):
    account = owner(tmp_path, [])
    runtime = FourLegRuntime(account, adapters())
    runtime.on_completed_bar("aegis_6j", bars()["aegis_6j"], now=NOW)

    runtime.expire_barrier(NOW, now=NOW + timedelta(minutes=15, seconds=31))

    assert account.permission == "HALTED"
    assert account.authority == "INTERVENTION"
    assert account.synthetic_broker.commands == []
    assert account.incidents[-1]["reason"] == "barrier"


def test_partial_barrier_survives_restart_and_expires_without_dispatch(tmp_path):
    account = owner(tmp_path, [])
    runtime = FourLegRuntime(account, adapters())
    runtime.on_completed_bar("aegis_6j", bars()["aegis_6j"], now=NOW)

    restarted = BookAccountOwner.boot(
        account.path, "synthetic-account", binding=binding(),
        synthetic_broker=SyntheticBroker([]))
    recovered = FourLegRuntime(restarted, adapters())
    recovered.expire_barrier(NOW, now=NOW + timedelta(minutes=15, seconds=31))

    assert restarted.authority == "INTERVENTION"
    assert restarted.synthetic_broker.commands == []
    assert restarted.retained_partial_bars == ()


def test_daemon_loop_expires_missing_bar_without_external_coordinator(tmp_path):
    class Source:
        def __init__(self, value=None):
            self.value = value

        def poll(self):
            value, self.value = self.value, None
            return value

    account = owner(tmp_path, [])
    runtime = FourLegRuntime(account, adapters())
    sources = {leg_id: Source(bars()[leg_id] if leg_id == "aegis_6j" else None)
               for leg_id in LEGS}
    loop = FourLegEvaluateLoop(sources=sources, runtime=runtime)
    loop.step(now=NOW)
    loop.step(now=NOW + timedelta(minutes=15, seconds=31))
    assert account.authority == "INTERVENTION"
    assert account.retained_partial_bars == ()


def test_skipped_complete_boundary_halts_before_next_barrier_dispatch(tmp_path):
    account = owner(tmp_path, [])
    runtime = FourLegRuntime(account, inert_adapters())
    for leg_id in LEGS:
        runtime.on_completed_bar(leg_id, bars()[leg_id], now=NOW)
    skipped = NOW + timedelta(minutes=30)
    with pytest.raises(AccountOwnerError, match="noncontiguous"):
        runtime.on_completed_bar(
            "aegis_6j", Bar(skipped, 100, 101, 99, 100, 10), now=skipped)
    assert account.authority == "INTERVENTION"


@pytest.mark.parametrize("bad_time", [
    NOW - timedelta(minutes=15, seconds=31),
    NOW + timedelta(seconds=1),
])
def test_stale_or_future_completed_bar_halts_before_dispatch(tmp_path, bad_time):
    account = owner(tmp_path, [])
    runtime = FourLegRuntime(account, adapters())
    with pytest.raises(AccountOwnerError, match="stale, future"):
        runtime.on_completed_bar(
            "aegis_6j", Bar(bad_time, 100, 101, 99, 100, 10), now=NOW)
    assert account.authority == "INTERVENTION"
    assert account.synthetic_broker.commands == []


def test_runtime_replay_of_identical_bars_and_facts_has_same_observable_state(tmp_path):
    def run(root, arrival):
        facts = (BrokerFact.fill("fill-aegis", "entry:aegis_6j", "aegis_6j",
                                 "entry", 1, 100.0, NOW),)
        account = owner(root, [BrokerResult("accepted", facts)])
        runtime = FourLegRuntime(account, adapters())
        for leg_id in arrival:
            runtime.on_completed_bar(leg_id, bars()[leg_id], now=NOW)
        return runtime.observable_state()

    assert run(tmp_path / "runtime", LEGS) == run(tmp_path / "replay", tuple(reversed(LEGS)))


def test_accepted_private_runtime_identities_load_and_cross_the_durable_barrier(tmp_path, monkeypatch):
    repo = Path(__file__).resolve().parents[2]
    primary = repo if repo.name == "multi_firm_operations" else repo.parents[1]
    private_root = (primary / "lab" / "analysis" / "c1" /
                    "tradeify_seven_strategy_phase1_2026-09" / "inputs" /
                    "private_overrides" / "op1" / "2026-09-14-seven" /
                    "step3-coverage" / "corrected-ports")
    assert (private_root / "effective_inputs.json").is_file(), private_root
    monkeypatch.setenv("FP_PORT_ROOT", str(private_root))

    actual = load_book_adapters()
    assert set(actual) == set(LEGS)
    assert {row.leg_id: port_sha256(row.leg_id) for row in ADAPTERS} == {
        row.leg_id: row.runtime_sha256 for row in ADAPTERS
    }
    account = owner(tmp_path, [], protected=True)
    runtime = FourLegRuntime(account, actual)
    result = None
    for leg_id in reversed(LEGS):
        result = runtime.on_completed_bar(leg_id, bars()[leg_id], now=NOW)
    assert result == ()
    assert account.retained_barriers[0]["completed"] is True


def test_schedule_and_feedback_are_replay_equivalent_after_same_bar_contention(tmp_path):
    def run(root, arrival):
        flat_id = "scheduled-flat:tradeify-account-day:2026-09-15:aegis_6j"
        entry_facts = (
            BrokerFact.fill("fill-aegis", "entry:aegis_6j", "aegis_6j", "entry",
                            1, 100.0, NOW),
            BrokerFact.terminal("entry:aegis_6j", "cancelled", 1, NOW),
        )
        flat_fact = BrokerFact.fill(
            "flat-aegis", flat_id, "aegis_6j", "flat", 1, 99.0,
            NOW + timedelta(hours=1, minutes=10), entry_execution_id="fill-aegis")
        account = owner(root, [BrokerResult("accepted", entry_facts),
                               BrokerResult("accepted", (flat_fact,))])
        runtime = FourLegRuntime(account, adapters())
        for leg_id in arrival:
            runtime.on_completed_bar(leg_id, bars()[leg_id], now=NOW)
        runtime.advance_schedule(now=account.binding["session"].risk_add_cutoff)
        runtime.advance_schedule(now=account.binding["session"].flatten_start)
        return runtime.observable_state()

    assert run(tmp_path / "runtime-schedule", LEGS) == run(
        tmp_path / "replay-schedule", tuple(reversed(LEGS)))


def test_delivered_feedback_checkpoint_replays_on_restart_without_resend(tmp_path):
    fact = BrokerFact.fill("fill-aegis", "entry:aegis_6j", "aegis_6j",
                           "entry", 1, 100.0, NOW)
    account = owner(tmp_path, [BrokerResult("accepted", (fact,))])
    runtime = FourLegRuntime(account, adapters())
    for leg_id in LEGS:
        runtime.on_completed_bar(leg_id, bars()[leg_id], now=NOW)
    assert account.pending_feedback == ()

    restarted = BookAccountOwner.boot(
        tmp_path / "owner.sqlite", "synthetic-account", binding=binding(),
        synthetic_broker=SyntheticBroker([]))
    fresh = adapters()
    FourLegRuntime.recover(restarted, fresh)
    assert fresh["aegis_6j"].events == [("fill", "entry:aegis_6j", "fill-aegis")]
    assert restarted.synthetic_broker.commands == []


def test_recovery_uses_each_retained_barriers_mode_not_current_session_mode(tmp_path):
    normal = binding()
    normal["settlement"] = replace(normal["settlement"], equity=100_000.0)
    account = BookAccountOwner.boot(
        tmp_path / "owner.sqlite", "synthetic-account", binding=normal,
        synthetic_broker=SyntheticBroker([]))
    account.activate_synthetic(now=NOW)
    runtime = FourLegRuntime(account, inert_adapters())
    for leg_id in LEGS:
        runtime.on_completed_bar(leg_id, bars()[leg_id], now=NOW)

    next_now = NOW + timedelta(days=1)
    protected = binding(protected=True)
    protected["session"] = replace(
        protected["session"], session_id="tradeify-account-day:2026-09-16",
        prior_session_id=normal["session"].session_id,
        opens_at=next_now - timedelta(hours=1), risk_add_cutoff=next_now + timedelta(hours=1),
        flatten_start=next_now + timedelta(hours=1, minutes=10),
        own_flat_deadline=next_now + timedelta(hours=1, minutes=15),
        closes_at=next_now + timedelta(hours=2))
    protected["settlement"] = replace(
        protected["settlement"], session_id=normal["session"].session_id,
        as_of=next_now - timedelta(hours=2))
    protected["as_of"] = next_now - timedelta(seconds=1)
    protected["valid_until"] = next_now + timedelta(minutes=5)
    restarted = BookAccountOwner.boot(
        account.path, "synthetic-account", binding=protected,
        synthetic_broker=SyntheticBroker([]))
    fresh = inert_adapters()
    recovered = FourLegRuntime.recover(restarted, fresh)
    assert {adapter.mode for adapter in fresh.values()} == {Mode.NORMAL}
    restarted.activate_synthetic(now=next_now)
    for leg_id in LEGS:
        recovered.on_completed_bar(
            leg_id, Bar(next_now, 102, 103, 101, 102, 12), now=next_now)
    assert restarted.retained_barriers[-1]["session_id"] == protected["session"].session_id
    assert restarted.retained_barriers[-1]["mode"] == Mode.PROTECTED.value


def test_daemon_loop_listener_and_async_fact_share_one_account_authority(tmp_path):
    class Source:
        def __init__(self, bar):
            self.bar = bar

        def poll(self):
            value, self.bar = self.bar, None
            return value

    account = owner(tmp_path, [BrokerResult("accepted")])
    runtime_adapters = adapters()
    runtime = FourLegRuntime(account, runtime_adapters)
    sources = {leg_id: Source(bars()[leg_id]) for leg_id in LEGS}
    result = FourLegEvaluateLoop(sources=sources, runtime=runtime).step(now=NOW)
    assert result[0].transport_state == "accepted"

    fact = BrokerFact.fill("async-fill", "entry:aegis_6j", "aegis_6j",
                           "entry", 1, 100.0, NOW)
    events = handle_book_fact(fact, account, runtime, now=NOW)
    assert events[0].fill.fill_id == "async-fill"
    assert runtime_adapters["aegis_6j"].events == [
        ("fill", "entry:aegis_6j", "async-fill")]
    assert account.pending_feedback == ()


def test_delayed_async_feedback_replays_after_later_bar_in_acquisition_order(tmp_path):
    account = owner(tmp_path, [BrokerResult("accepted")])
    live_adapters = adapters()
    runtime = FourLegRuntime(account, live_adapters)
    for leg_id in LEGS:
        runtime.on_completed_bar(leg_id, bars()[leg_id], now=NOW)
    later = NOW + timedelta(minutes=15)
    for leg_id in LEGS:
        runtime.on_completed_bar(
            leg_id, Bar(later, 101, 102, 100, 101, 11), now=later)
    handle_book_fact(
        BrokerFact.fill("delayed-fill", "entry:aegis_6j", "aegis_6j",
                        "entry", 1, 101.0, later), account, runtime, now=later)
    live_history = list(live_adapters["aegis_6j"].history)

    restarted = BookAccountOwner.boot(
        account.path, "synthetic-account", binding=binding(),
        synthetic_broker=SyntheticBroker([]))
    fresh = adapters()
    FourLegRuntime.recover(restarted, fresh)
    assert fresh["aegis_6j"].history == live_history
    assert live_history[-1] == ("event", "delayed-fill")


def test_async_fact_commit_cannot_overtake_live_bar_application(tmp_path):
    entered = threading.Event()
    release = threading.Event()
    fact_done = threading.Event()

    class BlockingAdapter(Adapter):
        def on_bar(self, bar):
            entered.set()
            assert release.wait(2)
            return super().on_bar(bar)

    account = owner(tmp_path, [BrokerResult("accepted")])
    account.dispatch(entry("aegis_6j", 8), now=NOW)
    values = {leg_id: Adapter(leg_id) for leg_id in LEGS}
    values["aegis_6j"] = BlockingAdapter("aegis_6j")
    runtime = FourLegRuntime(account, synthetic_adapter_registry(values))
    for leg_id in LEGS[1:]:
        runtime.on_completed_bar(leg_id, bars()[leg_id], now=NOW)

    bar_thread = threading.Thread(target=lambda: runtime.on_completed_bar(
        "aegis_6j", bars()["aegis_6j"], now=NOW))
    bar_thread.start()
    assert entered.wait(2)

    fact = BrokerFact.fill("serialized-fill", "entry:aegis_6j", "aegis_6j",
                           "entry", 1, 100.0, NOW)
    fact_thread = threading.Thread(target=lambda: (
        handle_book_fact(fact, account, runtime, now=NOW), fact_done.set()))
    fact_thread.start()
    assert not fact_done.wait(0.05)
    release.set()
    bar_thread.join(2)
    fact_thread.join(2)
    assert fact_done.is_set()
    assert values["aegis_6j"].history == [
        ("bar", NOW.isoformat()), ("event", "serialized-fill")]


def test_unreceipted_adapter_dictionary_is_rejected(tmp_path):
    account = owner(tmp_path, [])
    with pytest.raises(ValueError, match="registry"):
        FourLegRuntime(account, {leg_id: Adapter(leg_id) for leg_id in LEGS})


def test_corrupt_retained_adapter_checkpoint_halts_recovery(tmp_path):
    fact = BrokerFact.fill("fill-aegis", "entry:aegis_6j", "aegis_6j",
                           "entry", 1, 100.0, NOW)
    account = owner(tmp_path, [BrokerResult("accepted", (fact,))])
    runtime = FourLegRuntime(account, adapters())
    for leg_id in LEGS:
        runtime.on_completed_bar(leg_id, bars()[leg_id], now=NOW)
    with sqlite3.connect(account.path) as db:
        db.execute("UPDATE feedback SET checkpoint='{}' WHERE fact_id='fill-aegis'")

    restarted = BookAccountOwner.boot(
        account.path, "synthetic-account", binding=binding(),
        synthetic_broker=SyntheticBroker([]))
    with pytest.raises(AccountOwnerError, match="checkpoint"):
        FourLegRuntime.recover(restarted, adapters())
    assert restarted.authority == "INTERVENTION"
