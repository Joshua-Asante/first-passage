"""Short event permutations checked against a hand-derived obligation oracle.

Neither the oracle nor expected allocations use the kernel's rule helpers.
Independent symbol deliveries commute; older facts cannot undo a newer completion.
"""


import copy


from itertools import permutations


import pytest


from book_protocol import Bracket


from tests.ops.tb_s3_kernel.harness import MIN, Sequence, entry, fill_lot, make_world


@pytest.mark.parametrize("cancel_outcome", ["reject", "unknown", "unknown_lost", "defer"])
@pytest.mark.parametrize("restart_cut", [False, True])
def test_partial_remainder_cancel_outcomes_keep_reservation_until_terminal(cancel_outcome, restart_cut):
    """A partial order always owns both its executed contract and its live remainder."""
    w = make_world()
    d = w.kernel.admit_entry(entry("vanguard_mgc", 3, Bracket(stop=90)), w.now)
    w.broker.fill(d.ref, qty=1)
    w.advance(MIN)
    w.snap()
    w.broker.inject["cancel"] = cancel_outcome
    w.kernel.cancel(d.ref, w.now)
    if restart_cut:
        Sequence.start(w).restart()
    w.advance(MIN)
    w.snap()
    assert w.kernel.ledger.confirmed["vanguard_mgc"] == 1
    assert w.kernel.pending[d.ref].reserved == (0 if cancel_outcome == "unknown" else 2)
    if cancel_outcome == "defer":
        w.broker.execute_next()
    elif cancel_outcome in ("reject", "unknown_lost"):
        w.broker.fill(d.ref, qty=2)
    w.advance(MIN)
    w.snap()
    assert w.kernel.pending[d.ref].reserved == 0
    assert w.kernel.ledger.confirmed["vanguard_mgc"] == (
        3 if cancel_outcome in ("reject", "unknown_lost") else 1)


@pytest.mark.parametrize("reboot", [False, True])
def test_two_rejected_owners_on_one_symbol_do_not_overwrite_each_other(reboot):
    """Even identical scopes have separate obligations when request identities differ."""
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90))
    for owner in ("a", "b"):
        w.broker.inject["close"] = "reject"
        w.kernel.close("fill", lot, w.now, "exit", op_id=owner)
    if reboot:
        Sequence.start(w).restart()
    assert set(w.kernel.blocks["close_rejected"]) == {"a", "b"}
    w.broker.trigger(w.kernel.expected[lot].working["stop"])
    w.advance(MIN)
    w.snap()
    assert "close_rejected" not in w.kernel.blocks
    assert all(w.kernel.operations[owner].status == "complete" for owner in ("a", "b"))
