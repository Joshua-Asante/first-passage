"""PR 365 at ea8a5db: coherent reads, durable commands and broker quantity conservation."""
from dataclasses import replace

import pytest

from book_protocol import Bracket
from tests.ops.tb_s3_kernel.broker import BrokerOrder
from tests.ops.tb_s3_kernel.harness import MIN, Sequence, entry, fill_lot, make_world
from tests.ops.tb_s3_kernel.kernel import KernelRefusal
from tests.ops.test_tb_s3_kernel_redesign import Crash, crash_once


@pytest.mark.parametrize("reboot", [False, True])
def test_admission_waits_for_full_read_matching_the_latest_position(reboot):
    w = make_world()
    if reboot:
        Sequence.start(w).restart()
        w.advance(MIN)
        w.snap()
        assert w.kernel.reconcile_restart(w.now).ok
    w.advance(MIN)
    pos = replace(w.broker.snapshot("MGC"), order_level=False)
    w.kernel.apply_evidence(pos)
    d = w.kernel.admit_entry(entry("vanguard_mgc", 1, Bracket(stop=90)), w.now)
    assert not d.ok
    assert d.reason == "unknown_state"
    assert not w.broker.orders
    w.snap("MGC")
    assert w.kernel.admit_entry(entry("vanguard_mgc", 1, Bracket(stop=90)), w.now).ok


def test_restart_cannot_use_full_evidence_superseded_by_position_only():
    w = make_world()
    Sequence.start(w).restart()
    w.advance(MIN)
    w.snap()
    w.kernel.apply_evidence(replace(w.broker.snapshot("MGC"), order_level=False))
    assert w.kernel.reconcile_restart(w.now).reason == "evidence_owed"
    w.snap("MGC")
    assert w.kernel.reconcile_restart(w.now).ok


def test_orphan_cancel_waits_for_a_coherent_flat_read():
    w = make_world()
    w.broker.orders["orphan"] = BrokerOrder("orphan", "MGC", "vanguard_mgc", "stop",
                                           "sell", 1, "stop", price=90)
    w.snap("MGC")
    w.kernel.apply_evidence(replace(w.broker.snapshot("MGC"), order_level=False))
    assert w.kernel.cancel("orphan", w.now).reason == "protective_cancel_refused"
    assert w.broker.orders["orphan"].status == "working"
    w.snap("MGC")
    assert w.kernel.cancel("orphan", w.now).ok


def test_close_retry_waits_for_full_evidence_after_a_new_position_read():
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90))
    w.broker.inject["close"] = ("partial", 1)
    op = w.kernel.close("fill", lot, w.now, "exit")
    w.advance(MIN)
    w.snap()
    w.kernel.apply_evidence(replace(w.broker.snapshot("MGC"), order_level=False))
    with pytest.raises(KernelRefusal, match="reconcile"):
        w.kernel.retry(op.op_id, w.now)
    assert w.broker.positions["MGC"] == 1
    w.snap("MGC")
    w.kernel.retry(op.op_id, w.now)
    assert w.broker.positions["MGC"] == 0


@pytest.mark.parametrize("scope", ["fill", "sym"])
def test_consumed_scope_cancels_its_never_dispatched_close(scope):
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90))
    crash_once(w.kernel, "close", "planned")
    with pytest.raises(Crash):
        w.kernel.close(scope, lot if scope == "fill" else "MGC", w.now, "exit",
                       op_id="exit-before-stop")
    w.broker.trigger(w.broker.lots[lot].protection["stop"])
    Sequence.start(w).restart()
    w.advance(MIN)
    w.snap("MGC")  # deliver the covering scope evidence before resuming planned dispatch
    assert w.kernel.operations["exit-before-stop"].status == "complete"
    assert not [e for e in w.broker.log if e["event"] == "close"]
    w.snap()
    assert w.kernel.reconcile_restart(w.now).ok
    assert not w.kernel.risk_add_blocked
    Sequence.start(w).restart()
    w.kernel.progress(w.now)
    assert not [e for e in w.broker.log if e["event"] == "close"]


@pytest.mark.parametrize("kind", ["stop", "unrecognized"])
def test_restart_halts_on_unowned_order_attached_to_a_known_bare_lot(kind):
    w = make_world()
    lot = fill_lot(w, "dj30_mym_p250", 1)
    w.broker.orders["unowned"] = BrokerOrder("unowned", "MYM", "dj30_mym_p250",
                                            kind, "sell", 1, "stop", price=90,
                                            attached_to=lot)
    Sequence.start(w).restart()
    w.advance(MIN)
    w.snap()
    assert w.kernel.reconcile_restart(w.now).reason == "halted"
    assert "dj30_mym_p250" in w.kernel.halted_legs
    assert w.broker.orders["unowned"].status == "working"
    assert not [e for e in w.broker.log if e["event"] == "cancel"]


class CutStore:
    """Cut after an actual atomic durable write, independent of persist call counts."""

    def __init__(self, data, writes):
        self._data = data
        self.remaining = writes

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
        self.remaining -= 1
        if self.remaining == 0:
            raise Crash("durable write completed")


@pytest.mark.parametrize("command,reason", [("kill", "kill"), ("eod", "eod_flatten")])
@pytest.mark.parametrize("writes", [1, 2])
def test_first_durable_command_writes_contain_every_symbol_and_effect(command, reason, writes):
    w = make_world()
    fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90))
    w.kernel.store = CutStore(w.kernel.store.data, writes)
    with pytest.raises(Crash):
        getattr(w.kernel, command)(w.now)
    Sequence.start(w).restart()
    ops = [o for o in w.kernel.operations.values() if o.reason == reason]
    assert {o.sym for o in ops} == {"6J", "MGC", "MYM", "MNQ"}
    assert {e.owner for e in w.kernel.effects.values() if e.kind == "close"} >= {
        o.op_id for o in ops}
    w.kernel.progress(w.now)
    w.advance(MIN)
    w.snap()
    assert all(o.status == "complete" for o in ops)
    assert w.kernel.flatten_complete(reason, w.now)
    if command == "kill":
        assert w.kernel.dry_run


@pytest.mark.parametrize("writes", [1, 2])
def test_first_close_writes_include_all_required_entry_cancellations(writes):
    w = make_world()
    first = w.kernel.admit_entry(entry("vanguard_mgc", 1, Bracket(stop=90)), w.now)
    second = w.kernel.admit_entry(entry("vanguard_mgc", 1, Bracket(stop=90), kind="add"), w.now)
    assert first.ok and second.ok
    w.kernel.store = CutStore(w.kernel.store.data, writes)
    with pytest.raises(Crash):
        w.kernel.close("sym", "MGC", w.now, "exit", op_id="both-entries")
    Sequence.start(w).restart()
    assert {e.payload["ref"] for e in w.kernel.effects.values() if e.kind == "cancel"} == {
        first.ref, second.ref}
    w.kernel.progress(w.now)
    w.advance(MIN)
    w.snap()
    assert w.kernel.operations["both-entries"].status == "complete"
    assert w.broker.orders[first.ref].status == "cancelled"
    assert w.broker.orders[second.ref].status == "cancelled"


def test_takeover_first_write_owns_every_displaced_leg():
    w = make_world()
    fill_lot(w, "dj30_mym_p250", 22)
    fill_lot(w, "orb_mnq_v7", 10, Bracket(stop=90))
    request = entry("aegis_6j", 8)
    plan = w.kernel.admit_entry(request, w.now).takeover
    w.kernel.store = CutStore(w.kernel.store.data, 1)
    with pytest.raises(Crash):
        w.kernel.takeover(plan, w.now)
    Sequence.start(w).restart()
    assert {o.sym for o in w.kernel.operations.values() if o.reason == "capacity_takeover"} == {
        "MYM", "MNQ"}
    w.kernel.progress(w.now)
    w.advance(MIN)
    w.snap()
    assert w.kernel.reconcile_restart(w.now).ok
    assert w.kernel.settle_takeover(request, w.now).ok


def test_orphan_cancel_first_write_includes_its_recoverable_effect():
    w = make_world()
    w.broker.orders["orphan"] = BrokerOrder("orphan", "MGC", "vanguard_mgc", "stop",
                                           "sell", 1, "stop", price=90)
    w.snap("MGC")
    w.kernel.store = CutStore(w.kernel.store.data, 1)
    with pytest.raises(Crash):
        w.kernel.cancel("orphan", w.now)
    Sequence.start(w).restart()
    w.kernel.progress(w.now)
    w.advance(MIN)
    w.snap()
    assert w.broker.orders["orphan"].status == "cancelled"
    assert w.kernel.reconcile_restart(w.now).ok
    assert not w.kernel.risk_add_blocked


@pytest.mark.parametrize("settlement", [False, True])
def test_never_dispatched_entry_first_write_recovers_without_a_phantom_reservation(settlement):
    w = make_world()
    if settlement:
        fill_lot(w, "dj30_mym_p250", 22)
        request = entry("aegis_6j", 8)
        plan = w.kernel.admit_entry(request, w.now).takeover
        w.kernel.takeover(plan, w.now)
        w.advance(MIN)
        w.snap()
    else:
        request = entry("vanguard_mgc", 1, Bracket(stop=90))
    before = set(w.broker.orders)
    w.kernel.store = CutStore(w.kernel.store.data, 1)
    with pytest.raises(Crash):
        if settlement:
            w.kernel.settle_takeover(request, w.now)
        else:
            w.kernel.admit_entry(request, w.now)
    Sequence.start(w).restart()
    w.advance(MIN)
    w.snap()
    assert w.kernel.reconcile_restart(w.now).ok
    assert w.kernel.ledger.reserved[request.leg_id] == 0
    assert not w.kernel.halted_legs
    assert set(w.broker.orders) == before


@pytest.mark.parametrize("writes", [1, 2])
def test_rejected_attach_outcome_first_writes_include_required_recovery(writes):
    w = make_world()
    lot = fill_lot(w, "dj30_mym_p250", 1)
    w.broker.inject["attach"] = "reject"

    def cut_outcome(stage, effect):
        if stage == "executed" and effect.kind == "attach":
            w.kernel.effect_hook = None
            w.kernel.store = CutStore(w.kernel.store.data, writes)

    w.kernel.effect_hook = cut_outcome
    with pytest.raises(Crash):
        w.kernel.amend(lot, Bracket(stop=90), w.now)
    Sequence.start(w).restart()
    w.kernel.progress(w.now)
    w.advance(MIN)
    w.snap()
    assert w.broker.positions["MYM"] == 0
    assert not w.broker.snapshot("MYM").working
    assert "protection_gap" not in w.kernel.blocks


@pytest.mark.parametrize("quantity", [None, 3])
@pytest.mark.parametrize("allowance,remaining", [(0, 4), (1, 3), (3, 1)])
def test_partial_broker_close_consumes_one_total_budget_across_lots(quantity, allowance, remaining):
    w = make_world()
    fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90))
    fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90), kind="add")
    w.broker.inject["close"] = ("partial", allowance)
    w.broker.close(sym="MGC", qty=quantity)
    assert w.broker.positions["MGC"] == remaining
    assert sum(l.qty for l in w.broker.lots.values()) == remaining
    w.advance(MIN)
    w.snap()
    assert w.kernel.ledger.confirmed["vanguard_mgc"] == remaining


def test_broker_partial_allowance_is_also_capped_by_requested_quantity():
    w = make_world()
    fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90))
    fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90), kind="add")
    w.broker.inject["close"] = ("partial", 3)
    w.broker.close(sym="MGC", qty=1)
    assert w.broker.positions["MGC"] == 3
