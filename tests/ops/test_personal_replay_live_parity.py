"""Card D Part 1: public synthetic consumer parity; D7 remains PENDING-P4.

This is capability evidence, never FG at R1. No private adapter is loaded.
"""
from dataclasses import replace
from datetime import timedelta
import hashlib
import json
from pathlib import Path
import subprocess

import pytest

from c1_rail.book_account_owner import BookAccountOwner, BrokerFact, BrokerResult
from c1_rail.book_policy import BOOK_LEGS, candidate_book_protection_policy, validate_size_vector
from c1_rail.qualification.model import PathBar, SessionSchedule, ET
from c1_rail.qualification.replay import BookReplay, Instrument
from c1_signal_daemon.book_adapters import ADAPTER_BY_LEG, synthetic_adapter_registry
from c1_signal_daemon.book_bundle_execution import BundleExecution, SizingInputs
from c1_signal_daemon.book_protocol import ExecutionEvent, FillTiming, Mode, OrderIntent
from c1_signal_daemon.book_runtime import FourLegRuntime
from c1_signal_daemon.feed import Bar
from c1_signal_daemon.tv_broker_emulator import TVBrokerEmulator
from mc.simulation import EvaluationState
from book_bootstrap_fixtures import BootstrapBroker, activate_fresh
from test_four_leg_runtime import NOW, binding

LEGS = tuple(s.leg_id for s in BOOK_LEGS)
POLICY = candidate_book_protection_policy()
VECTOR = {
    "aegis_6j": {"base": 3, "adds": "UNCHANGED"},
    "dj30_mym_p250": {"risk_multiplier": "1/2", "cap_reserve_multiplier": "1/1", "adds": "OFF"},
    "vanguard_mgc": {"base_by_port": {"1": 1, "2": 1}, "adds": "OFF"},
    "orb_mnq_v7": {"base": 1, "adds": "OFF"},
}
NORMAL_BASE = dict(aegis_6j=8, dj30_mym_p250=5, vanguard_mgc=2, orb_mnq_v7=1)
REASONS = {"adapter": "shared_sizing_zero", "replay": "zero policy quantity", "owner": "zero_size"}
CONSUMERS = (
    "ops/c1_signal_daemon/book_bundle_execution.py",
    "ops/c1_rail/qualification/replay.py",
    "ops/c1_rail/book_account_owner.py",
    "ops/c1_rail/book_sizing_context.py",
    "ops/c1_signal_daemon/book_runtime.py",
    "ops/c1_rail/book_policy.py",
)


class Script:
    """Feedback changes the third signal; missing/doubled rejection changes it."""
    def __init__(self, leg_id, active, zero=False):
        self.leg_id, self.active, self.zero = leg_id, active, zero
        self.events, self.signals, self.states = [], [], []
        self.index = 0

    def set_mode(self, mode):
        return []

    def on_execution(self, event):
        self.events.append(event)

    def checkpoint(self):
        return {"index": self.index, "rejects": sum(e.event == "reject" for e in self.events),
                "fills": [(e.fill.kind, e.fill.qty) for e in self.events if e.fill]}

    def on_bar(self, bar):
        state = self.checkpoint()
        self.states.append(state)
        index = self.index
        self.index += 1
        if not self.active or index > 2:
            return []
        if index == 0:
            kind = "entry"
        elif self.zero:
            # The zero-port control retries the nonzero port only after one refusal.
            if state["rejects"] != 1 or state["fills"]:
                return []
            kind = "entry"
        elif index == 1 or state["rejects"] == 1:
            kind = "add"
        else:
            return []
        qty = NORMAL_BASE[self.leg_id] if kind == "entry" else 1
        if self.zero and index > 0 and self.leg_id == "vanguard_mgc":
            qty = 1
        spec = next(s for s in BOOK_LEGS if s.leg_id == self.leg_id)
        action = OrderIntent(f"{kind}-{index}", self.leg_id, kind, spec.entry_side, qty,
                             timing=FillTiming.THIS_CLOSE, stop_dist_pts=24,
                             bar_time=bar.ts)
        self.signals.append((kind, qty))
        return [action]


class PartialBroker(TVBrokerEmulator):
    """Synthetic broker confirms two contracts and cancels the base remainder."""
    def submit(self, actions, bar):
        events = []
        for action in actions:
            partial = isinstance(action, OrderIntent) and action.kind == "entry" and action.qty > 2
            events.extend(super().submit([replace(action, qty=2) if partial else action], bar))
            if partial:
                events.append(ExecutionEvent("cancel", action.leg_id, bar.ts,
                                             order_id=action.order_id, detail="synthetic remainder"))
        return events


class OwnerBroker(BootstrapBroker):
    def __init__(self, partial):
        super().__init__()
        self.partial = partial

    def send(self, command):
        quantity = command.quantity
        partial = self.partial and command.kind == "entry" and quantity > 2
        filled = 2 if partial else quantity
        facts = [BrokerFact.fill("fill:" + command.operation_id, command.operation_id,
                                command.leg_id, command.kind, filled, 100, command.action.bar_time)]
        # Terminal evidence is observed asynchronously after dispatch.
        self.queue(BrokerResult("accepted", tuple(facts)))
        return super().send(command)


def exercise(tmp_path, route, leg_id, vector, *, partial=False, zero=False):
    sources = {k: Script(k, k == leg_id, zero) for k in LEGS}
    source = sources[leg_id]
    spec = ADAPTER_BY_LEG[leg_id]
    size = vector.leg(leg_id)
    broker_type = PartialBroker if partial else TVBrokerEmulator
    admitted, outcomes, exposures = [], [], []
    if route == "adapter":
        consumer = BundleExecution(source, SizingInputs(leg_id, Mode.NORMAL, "AUTHORIZED",
                                   80, 100, spec.pointvalue, size), policy=POLICY)
        broker = broker_type(leg_id, spec.mintick, spec.pointvalue, 0, 0)
    elif route == "replay":
        consumer = BookReplay(sources, {k: Instrument(ADAPTER_BY_LEG[k].mintick,
            ADAPTER_BY_LEG[k].pointvalue, 0, 0) for k in LEGS}, policy=POLICY,
            initial_state=EvaluationState(100000, 100000, 100000, 0, 0),
            sizing_inputs=lambda k, a, p: dict(lifecycle_tier="AUTHORIZED", normal_base=a.qty,
                risk_dollars=100, per_contract_risk=24 * ADAPTER_BY_LEG[k].pointvalue, cap_alloc=80),
            schedule_quotes=lambda *args: 100, broker_factory=broker_type, size_vector=vector)
    else:
        data = binding()
        data.update(size_vector=vector, valid_until=NOW + timedelta(hours=2),
                    max_evidence_age=timedelta(hours=2))
        broker = OwnerBroker(partial)
        consumer = BookAccountOwner.boot(tmp_path / "owner.sqlite", "synthetic-account",
                                         binding=data, synthetic_broker=broker)
        activate_fresh(consumer)
        runtime = FourLegRuntime(consumer, synthetic_adapter_registry(sources))
    for index in range(3):
        instant = NOW + timedelta(minutes=15 * index)
        bar = Bar(instant, 100, 100, 100, 100)
        if route == "adapter":
            actions = consumer.on_bar(bar)
            admitted.extend((a.kind, a.qty) for a in actions)
            for event in broker.submit(actions, bar):
                consumer.on_execution(event)
        elif route == "replay":
            pb = PathBar(instant, instant, instant.date(), instant.astimezone(ET),
                         tuple((k, bar) for k in LEGS))
            schedule = SessionSchedule(NOW + timedelta(hours=1), NOW + timedelta(hours=1, minutes=10),
                                       NOW + timedelta(hours=1, minutes=15))
            consumer._index, consumer._path_time = index, instant
            for action in source.on_bar(bar):
                sized = consumer._admit(action, pb, Mode.NORMAL, schedule)
                if sized is not None:
                    admitted.append((sized.kind, sized.qty))
                    consumer._submit(leg_id, [sized], bar)
        else:
            broker.advance(instant)
            for k in LEGS:
                result = runtime.on_completed_bar(k, bar, now=instant)
                if result is not None:
                    outcomes.extend(result)
            for command in broker.commands[len(admitted):]:
                partial_base = partial and command.kind == "entry" and command.quantity > 2
                observed = instant + timedelta(microseconds=1)
                runtime.observe_fact(BrokerFact.terminal(command.operation_id,
                    "cancelled" if partial_base else "filled",
                    2 if partial_base else command.quantity, observed), now=observed)
            admitted = [(c.kind, c.quantity) for c in broker.commands]
            exposures.append(consumer.exposure(leg_id))
    return dict(admitted=admitted, source=source, consumer=consumer,
                outcomes=outcomes, exposures=exposures)


def compare(tmp_path, record_property, leg_id, vector, *, partial=False, zero=False):
    inputs = dict(leg=leg_id, vector=vector.as_mapping(), partial=partial, zero=zero,
                  normal_base=NORMAL_BASE, risk=100, stop=24, mode="NORMAL", bars=3,
                  start=NOW.isoformat(), interval_minutes=15, price=100)
    root = Path(__file__).resolve().parents[2]
    identity = {path: subprocess.check_output(["git", "hash-object", path],
                cwd=root, text=True).strip() for path in (*CONSUMERS, "tests/ops/test_personal_replay_live_parity.py",
                             "tests/ops/test_four_leg_runtime.py", "tests/ops/book_bootstrap_fixtures.py")}
    record_property("consumer_git_blobs", json.dumps(identity, sort_keys=True))
    record_property("synthetic_inputs_sha256", hashlib.sha256(
        json.dumps(inputs, sort_keys=True).encode()).hexdigest())
    record_property("D7", "PENDING-P4")
    results = {route: exercise(tmp_path, route, leg_id, vector, partial=partial, zero=zero)
               for route in REASONS}
    assert results["adapter"]["admitted"] == results["replay"]["admitted"] == results["owner"]["admitted"]
    for route, result in results.items():
        source = result["source"]
        refusals = [e for e in source.events if e.event == "reject"]
        assert all(e.detail == REASONS[route] for e in refusals), (route, refusals, result["outcomes"])
        assert len({e.order_id for e in refusals}) == len(refusals)
        assert source.signals == results["adapter"]["source"].signals
        assert source.states == results["adapter"]["source"].states
        assert source.checkpoint() == results["adapter"]["source"].checkpoint()
    return results


@pytest.mark.parametrize("leg_id", LEGS)
def test_d1_d3_d6_entry_add_and_feedback(tmp_path, record_property, leg_id):
    results = compare(tmp_path, record_property, leg_id, validate_size_vector(VECTOR))
    assert len(results["adapter"]["admitted"]) == 1
    assert [e.event for e in results["adapter"]["source"].events] == ["fill", "reject", "reject"]


def test_d2_partial_confirmed_base(tmp_path, record_property):
    vector = validate_size_vector({**VECTOR, "dj30_mym_p250": {
        **VECTOR["dj30_mym_p250"], "adds": "UNCHANGED"}})
    results = compare(tmp_path, record_property, "dj30_mym_p250", vector, partial=True)
    assert results["adapter"]["admitted"] == [("entry", 4), ("add", 5)]
    assert results["adapter"]["source"].checkpoint()["fills"] == [("entry", 2), ("add", 5)]


@pytest.mark.parametrize("leg_id", ["aegis_6j", "vanguard_mgc"])
def test_d4_d5_zero_refusal_without_fill_or_reservation(tmp_path, record_property, leg_id):
    vector = validate_size_vector({**VECTOR, "aegis_6j": {"base": 0, "adds": "UNCHANGED"},
        "vanguard_mgc": {"base_by_port": {"1": 1, "2": 0}, "adds": "OFF"}})
    results = compare(tmp_path, record_property, leg_id, vector, zero=True)
    for route, result in results.items():
        first = result["source"].events[0]
        assert first.event == "reject" and first.fill is None and first.detail == REASONS[route]
    owner = results["owner"]
    assert owner["exposures"][0] == (0, 0)
    assert owner["outcomes"][0].quantity == 0
    assert owner["outcomes"][0].attempt_id is None
    assert owner["consumer"].exposure(leg_id)[1] == 0
    if leg_id == "aegis_6j":
        assert all(not r["admitted"] for r in results.values())
        assert owner["consumer"].exposure(leg_id) == (0, 0)
