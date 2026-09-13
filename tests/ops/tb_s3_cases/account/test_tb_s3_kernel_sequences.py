"""Short event permutations checked against a hand-derived obligation oracle.

Neither the oracle nor expected allocations use the kernel's rule helpers.
Independent symbol deliveries commute; older facts cannot undo a newer completion.
"""


import copy


from itertools import permutations


import pytest


from book_protocol import Bracket


from tests.ops.tb_s3_kernel.account_harness import MIN, Sequence, entry, fill_lot, make_world


@pytest.mark.parametrize("delivery", list(permutations(("old-a", "old-b", "done-a", "done-b"))))
@pytest.mark.parametrize("restart_cut", [None, 0, 2, 4])
def test_two_owners_remain_independent_across_reordered_reads_and_restart(delivery, restart_cut):
    """Each owner clears only on its own covering completion; stale reads cannot undo it."""
    w = make_world()
    a = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90))
    b = fill_lot(w, "orb_mnq_v7", 3, Bracket(stop=90))
    trace = Sequence.start(w)
    trace.acquire("old-a", "MGC")
    trace.acquire("old-b", "MNQ")
    w.kernel.close("fill", a, w.now, "exit", op_id="close-a")
    w.kernel.close("fill", b, w.now, "exit", op_id="close-b")
    w.advance(MIN)
    trace.acquire("done-a", "MGC")
    trace.acquire("done-b", "MNQ")
    completed = set()
    for index, event in enumerate(delivery):
        if restart_cut == index:
            trace.restart()
        trace.deliver(event)
        if event.startswith("done-"):
            completed.add(event[-1])
        assert w.kernel.lots[a].qty == (0 if "a" in completed else 2), trace.history
        assert w.kernel.lots[b].qty == (0 if "b" in completed else 3), trace.history
        assert set(w.kernel.blocks.get("unknown_order", ())) == {
            f"close-{owner}" for owner in {"a", "b"} - completed}, trace.history
        if len(completed) != 2:
            assert w.kernel.admit_entry(entry("aegis_6j", 1), w.now).reason == "policy_block"
        before = copy.deepcopy(w.kernel.store.data)
        for _ in range(index):
            w.kernel.kill_status(False, w.now)
        assert w.kernel.store.data == before, trace.history
    if restart_cut == 4:
        trace.restart()
    assert w.kernel.ledger.confirmed["vanguard_mgc"] == 0
    assert w.kernel.ledger.confirmed["orb_mnq_v7"] == 0
    assert len([e for e in w.broker.log if e["event"] == "close"]) == 2
