"""PR365 at23cf0e1: complete histories, gross exposure, future requests and bracket reissues."""


from dataclasses import replace


import pytest


from book_protocol import Bracket, BracketAmend


from tests.ops.tb_s3_kernel.broker import STALENESS_WINDOW


from tests.ops.tb_s3_kernel.harness import MIN, Sequence, entry, fill_lot, make_world


from tests.ops.tb_s3_cases.support.test_tb_s3_kernel_redesign import Crash, crash_once


def offsetting_lots(w):
    """Actual buy1/sell1 executions, zero net position, two open lots."""
    d = w.kernel.admit_entry(entry("vanguard_mgc", 2), w.now)
    w.broker.fill(d.ref, 1)
    w.advance(MIN)
    w.snap()
    w.broker.orders[d.ref].side = "sell"
    w.broker.fill(d.ref)
    w.advance(MIN)
    w.snap()
    assert w.broker.positions["MGC"] == 0
    assert sum(l.qty for l in w.broker.lots.values()) == 2


def defer_external(w, request_id, sym="MGC"):
    """An accepted external risk-add has no local reservation, effect or working ref yet."""
    w.broker.inject["place"] = "defer"
    w.broker.request("place", request_id, sym=sym, leg_id="external", kind="entry",
                     side="buy", qty=99, ref=request_id + "-order")
