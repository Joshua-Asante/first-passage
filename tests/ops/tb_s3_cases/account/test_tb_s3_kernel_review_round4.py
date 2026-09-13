"""PR 365 at ea8a5db: coherent reads, durable commands and broker quantity conservation."""


from dataclasses import replace


import pytest


from book_protocol import Bracket


from tests.ops.tb_s3_kernel.broker import BrokerOrder


from tests.ops.tb_s3_kernel.account_harness import MIN, Sequence, entry, fill_lot, make_world


from tests.ops.tb_s3_kernel.kernel import KernelRefusal


from tests.ops.tb_s3_cases.support.test_tb_s3_kernel_redesign import Crash, crash_once


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
