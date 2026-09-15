"""Shared-law sizing with actual broker-emulator feedback; synthetic bars."""
from datetime import datetime, timezone

import pytest

from c1_rail.book_policy import candidate_book_protection_policy
from c1_signal_daemon.book_bundle_execution import (
    BundleExecution, SizingInputs, check_margin_phase, run_sized_adapter,
)
from c1_signal_daemon.book_protocol import ExecutionEvent, Fill, FillTiming, Mode, OrderIntent, Side
from c1_signal_daemon.feed import Bar
from c1_signal_daemon.tv_broker_emulator import TVBrokerEmulator, run_adapter

NOW = datetime(2026, 9, 14, 14, tzinfo=timezone.utc)
LEG = "dj30_mym_p250"


class Source:
    leg_id = LEG

    def __init__(self):
        self.actions = []
        self.events = []

    def on_bar(self, bar):
        return self.actions

    def on_execution(self, event):
        self.events.append(event)

    def checkpoint(self):
        return {"events": len(self.events)}


def owner(source, **overrides):
    settings = dict(leg_id=source.leg_id, mode=Mode.PROTECTED, lifecycle_tier="AUTHORIZED",
                    cap_alloc=20, risk_dollars=100, pointvalue=0.5)
    settings.update(overrides)
    return BundleExecution(source, SizingInputs(**settings), policy=candidate_book_protection_policy())


def intent(kind="entry", qty=5, oid="base"):
    return OrderIntent(oid, LEG, kind, Side.BUY, qty,
                       timing=FillTiming.THIS_CLOSE, stop_dist_pts=24, bar_time=NOW)


def event(fid, oid, kind, qty, entry_id=None):
    fill = Fill(fid, oid, LEG, kind, Side.BUY if kind in ("entry", "add") else Side.SELL,
                qty, 100, NOW, entry_fill_id=entry_id, commission=qty * .91)
    return ExecutionEvent("fill", LEG, NOW, fill=fill, order_id=oid)


def test_risk_is_scaled_before_floor_not_from_capped_normal_quantity():
    source = Source()
    source.actions = [intent()]
    execution = owner(source)
    bar = Bar(NOW, 100, 101, 99, 100)
    sized = execution.on_bar(bar)
    # floor(100 * .4 / (24 * .5)) = 3, versus floor(source cap 5 * .4) = 2.
    assert sized[0].qty == 3
    assert source.actions[0].qty == 5
    broker = TVBrokerEmulator(leg_id=LEG, mintick=1, pointvalue=.5,
                             slippage_ticks=0, commission_per_side=.91)
    for observed in broker.submit(sized, bar):
        execution.on_execution(observed)
    assert execution.confirmed_base == 3
    assert source.events == broker.events
    source.actions = [intent("add", 12, "add")]
    assert execution.on_bar(bar)[0].qty == 7


def test_partial_confirmations_and_partial_exit_do_not_use_intended_base():
    source = Source()
    execution = owner(source)
    source.actions = [intent()]
    execution.on_bar(Bar(NOW, 100, 101, 99, 100))
    execution.on_execution(event("f1", "base", "entry", 1))
    source.actions = [intent("add", 12, "add")]
    # An unresolved base fill blocks adding until its terminal remainder is known.
    with pytest.raises(ValueError, match="pending_base"):
        execution.on_bar(Bar(NOW, 100, 101, 99, 100))
    execution.on_execution(ExecutionEvent("cancel", LEG, NOW, order_id="base"))
    assert execution.on_bar(Bar(NOW, 100, 101, 99, 100))[0].qty == 2
    execution.on_execution(event("f2", "add", "add", 2))
    execution.on_execution(event("x1", "exit", "exit", 1, "f2"))
    assert execution.open_quantity == 2
    assert execution.confirmed_base == 1
    execution.on_execution(event("x2", "exit", "exit", 1, "f1"))
    execution.on_execution(event("x3", "exit", "exit", 1, "f2"))
    assert execution.confirmed_base == execution.open_quantity == 0


def test_duplicate_or_unknown_fills_cannot_advance_feedback():
    source = Source()
    execution = owner(source)
    source.actions = [intent()]
    execution.on_bar(Bar(NOW, 100, 101, 99, 100))
    observed = event("f1", "base", "entry", 3)
    execution.on_execution(observed)
    with pytest.raises(ValueError, match="duplicate_fill"):
        execution.on_execution(observed)
    with pytest.raises(ValueError, match="unknown_entry"):
        execution.on_execution(event("f2", "unknown", "entry", 1))
    assert source.events == [observed]


def test_actual_size_fees_and_exit_feedback_reach_adapter():
    class CashHalt(Source):
        def on_bar(self, bar):
            if not self.events:
                return [intent()]
            if len(self.events) == 1:
                return [OrderIntent("exit", LEG, "flat", Side.SELL, None,
                                    timing=FillTiming.THIS_CLOSE)]
            return []

    source = CashHalt()
    execution = owner(source)
    broker = TVBrokerEmulator(leg_id=LEG, mintick=1, pointvalue=.5,
                             slippage_ticks=0, commission_per_side=.91)
    run_adapter(execution, [Bar(NOW, 100, 100, 100, 100)] * 2, broker)
    assert [ev.fill.qty for ev in source.events] == [3, 3]
    assert sum(ev.fill.commission for ev in source.events) == pytest.approx(5.46)
    assert execution.open_quantity == execution.confirmed_base == 0


def test_protected_orb_add_is_refused_before_emulation():
    source = Source()
    source.leg_id = "orb_mnq_v7"
    execution = owner(source, pointvalue=2, cap_alloc=3)
    base = OrderIntent("b", source.leg_id, "entry", Side.BUY, 1, timing=FillTiming.THIS_CLOSE)
    source.actions = [base]
    bar = Bar(NOW, 100, 100, 100, 100)
    broker = TVBrokerEmulator(leg_id=source.leg_id, mintick=.25, pointvalue=2,
                             slippage_ticks=0, commission_per_side=.91)
    for ev in broker.submit(execution.on_bar(bar), bar):
        execution.on_execution(ev)
    source.actions = [OrderIntent("a", source.leg_id, "add", Side.BUY, 1)]
    assert execution.on_bar(bar) == []
    assert source.events[-1].event == "reject"
    assert execution.confirmed_base == 1


def test_margin_envelope_covers_replacement_turnover_fees_and_exit_slippage():
    broker = TVBrokerEmulator(leg_id="orb_mnq_v7", mintick=.25, pointvalue=2,
                             slippage_ticks=1, commission_per_side=.91,
                             initial_capital=1000, margin_pct=.1)
    bar = Bar(NOW, 100, 110, 90, 100)
    opening = OrderIntent("b", broker.leg_id, "entry", Side.BUY, 1,
                          timing=FillTiming.THIS_CLOSE)
    broker.submit([opening], bar)
    replacements = [OrderIntent("next", broker.leg_id, "entry", Side.BUY, 3)]
    assert check_margin_phase(broker, bar, replacements) is None
    # Enough for the current mark and nominal margin, insufficient for the
    # conservative old-lot exit plus THREE replacement round trips.
    broker.initial_capital = 100
    with pytest.raises(ValueError, match="margin_envelope_failed"):
        check_margin_phase(broker, bar, replacements)


@pytest.mark.parametrize("side,qty", [(Side.SELL, 1), (Side.BUY, 4)])
def test_margin_proof_refuses_unsupported_exposure(side, qty):
    broker = TVBrokerEmulator("orb_mnq_v7", .25, 2, 1, .91, margin_pct=.1)
    action = OrderIntent("unsupported", broker.leg_id, "entry", side, qty)
    with pytest.raises(ValueError, match="margin_domain"):
        check_margin_phase(broker, Bar(NOW, 100, 110, 90, 100), [action])


def test_margin_runner_includes_resting_stop_before_processing():
    source = Source()
    source.leg_id = "orb_mnq_v7"
    execution = owner(source, pointvalue=2, cap_alloc=3)
    broker = TVBrokerEmulator(source.leg_id, .25, 2, 1, .91, margin_pct=.1)
    # An unsupported short resting stop must be found from the broker queue,
    # even though the source returns no new actions this bar.
    broker.submit([OrderIntent("stop", source.leg_id, "entry", Side.SELL, 1,
                               order_type="stop", price=90)], Bar(NOW, 100, 110, 95, 100))
    with pytest.raises(ValueError, match="margin_domain_orders"):
        run_sized_adapter(execution, [Bar(NOW, 100, 110, 80, 100)], broker)
    assert broker.position() == 0


def test_margin_runner_checks_both_phases_and_post_submit():
    source = Source()
    source.leg_id = "orb_mnq_v7"
    execution = owner(source, pointvalue=2, cap_alloc=3)
    broker = TVBrokerEmulator(source.leg_id, .25, 2, 1, .91, margin_pct=.1)
    report = run_sized_adapter(execution, [Bar(NOW, 100, 110, 90, 100)], broker)
    assert report == {"bars": 1, "margin_phase_checks": 3}
