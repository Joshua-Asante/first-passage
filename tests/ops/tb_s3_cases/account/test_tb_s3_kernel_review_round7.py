"""PR365 at23cf0e1: complete histories, gross exposure, future requests and bracket reissues."""


from dataclasses import replace


import pytest


from book_protocol import Bracket, BracketAmend


from tests.ops.tb_s3_kernel.broker import STALENESS_WINDOW


from tests.ops.tb_s3_kernel.account_harness import MIN, Sequence, entry, fill_lot, make_world


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


@pytest.mark.parametrize("route", ["feed", "daemon", "retained_close"])
def test_zero_net_position_does_not_skip_consumption_of_gross_lots(route):
    w = make_world()
    offsetting_lots(w)
    if route == "retained_close":
        crash_once(w.kernel, "close", "planned")
        with pytest.raises(Crash):
            w.kernel.close("sym", "MGC", w.now, "attended_external_recovery")
        Sequence.start(w).restart()
        w.advance(MIN)
        w.snap()
    else:
        w.advance(STALENESS_WINDOW + MIN)
        w.snap()
        if route == "feed":
            assert w.daemon.feed_loss_check("vanguard_mgc", w.now) is not None
        else:
            assert w.kernel.daemon_loss_check(w.now)
    assert all(l.qty == 0 for l in w.broker.lots.values())
    w.advance(MIN)
    w.snap()
    assert w.kernel.quiescent("MGC", w.now)


@pytest.mark.parametrize("route", ["tighten", "attach", "crossed"])
def test_daemon_accepts_the_bracket_dataclass_carried_by_the_adapter_protocol(route):
    w = make_world()
    leg = "vanguard_mgc" if route == "tighten" else "dj30_mym_p250"
    lot = fill_lot(w, leg, 1, Bracket(stop=90) if route == "tighten" else None)
    action = BracketAmend(leg, Bracket(stop=95), (lot,))
    result = w.daemon.reissue(action.leg_id, lot, action.bracket,
                              94 if route == "crossed" else 100, w.now)
    if route == "crossed":
        assert result == "close_time_exit"
        assert w.broker.lots[lot].qty == 0
    else:
        assert result in ("sent", "accepted")
        ref = w.broker.lots[lot].protection["stop"]
        assert w.broker.orders[ref].price == 95


def test_two_external_requests_resolve_individually_after_complete_account_coverage():
    w = make_world()
    defer_external(w, "one")
    defer_external(w, "two")
    w.advance(MIN)
    w.snap()
    w.broker.inject["place"] = "reject"
    w.broker.execute_next()
    w.advance(MIN)
    w.snap()
    w.kernel.session_open()
    assert w.kernel.risk_add_blocked
    w.broker.inject["place"] = "reject"
    w.broker.execute_next()
    w.advance(MIN)
    w.snap("MNQ")
    assert w.kernel.risk_add_blocked  # other symbol reads predate completion
    w.snap()
    assert not w.kernel.risk_add_blocked


def test_kill_cannot_complete_or_disarm_before_external_future_exposure_is_reconciled():
    w = make_world()
    defer_external(w, "kill-race")
    w.advance(MIN)
    w.snap()
    w.kernel.kill(w.now)
    w.advance(MIN)
    w.snap()
    assert not w.kernel.dry_run
    assert not w.kernel.flatten_complete("kill", w.now)
    w.broker.inject["place"] = "reject"
    w.broker.execute_next()
    w.advance(MIN)
    w.snap()
    assert w.kernel.dry_run
    assert w.kernel.flatten_complete("kill", w.now)
