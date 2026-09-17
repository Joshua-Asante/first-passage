"""Synthetic continuous replay acceptance; never loads private adapters."""
from datetime import date, datetime, timedelta, timezone
from dataclasses import replace
from decimal import Decimal

import pytest

from c1_signal_daemon.book_protocol import Side, OrderIntent, FillTiming, Bracket, Cancel, BracketAmend
from c1_signal_daemon.feed import Bar
from c1_rail.qualification.replay import BookReplay, Instrument, ReplayNeedsContext, ReplayDeadlineFailure, lifetime_adverse_mark
from c1_rail.book_policy import BOOK_LEGS, candidate_book_protection_policy
from c1_rail.qualification.model import SourceBar, SourceSession, SessionSchedule, PathBar, PathSession, ET
from mc.simulation import EvaluationState
from c1_signal_daemon.tv_broker_emulator import TVBrokerEmulator


class Adapter:
    def __init__(self, leg_id, emit=None):
        self.leg_id, self.emit = leg_id, emit
        self.bars, self.feedback, self.modes = [], [], []

    def on_bar(self, bar):
        self.bars.append(bar)
        return self.emit(self, bar) if self.emit else []

    def set_mode(self, mode):
        self.modes.append(mode)
        return []

    def on_execution(self, event):
        self.feedback.append(event)


def path_session(occurrence=0, prices=None, start_hour=14, source_day=5):
    origin = datetime(2026, 1, source_day, start_hour, tzinfo=timezone.utc)
    source_date = origin.astimezone(ET).date()
    prices = prices or [(100, 100, 100, 100), (100, 110, 90, 100)]
    if not (start_hour == 20 and len(prices) == 4):
        last = prices[-1][-1]
        prices = [*prices, (last, last, last, last)]
    deadline = origin + timedelta(minutes=15 * len(prices))
    sourcebars = tuple(SourceBar(origin + timedelta(minutes=15*i), tuple(
        (s.leg_id, Bar(origin + timedelta(minutes=15*i), *p)) for s in BOOK_LEGS))
        for i, p in enumerate(prices))
    source = SourceSession(str(source_day), source_date, sourcebars,
        SessionSchedule(deadline - timedelta(minutes=15), deadline - timedelta(minutes=5), deadline))
    pathorigin = datetime(2026, 2, 2 + occurrence, 14, tzinfo=timezone.utc)
    bars = tuple(PathBar(pathorigin + timedelta(minutes=15*i), sb.source_bar_time,
        source_date, sb.source_bar_time.astimezone(ET), sb.bars) for i, sb in enumerate(sourcebars))
    return PathSession(occurrence, date(2026, 2, 2+occurrence), source, bars, True, True)


def engine(emitters=None, quotes=None, sizing=None, instruments=None, state=None, broker_factory=None):
    emitters = emitters or {}
    adapters = {s.leg_id: Adapter(s.leg_id, emitters.get(s.leg_id)) for s in BOOK_LEGS}
    inst = instruments or {s.leg_id: Instrument(1, 1, 0, 0) for s in BOOK_LEGS}
    class FlatTailQuotes:
        def __call__(self, *args):
            return quotes(*args) if quotes else 100

        def split_bar(self, session, pb, instant, k):
            original = dict(pb.bars)[k]
            price = self(session, instant, k)
            if not original.open == original.high == original.low == original.close == price:
                raise ReplayNeedsContext("synthetic fixture lacks split OHLC")
            return original, Bar(instant, price, price, price, price)
    provider = quotes if hasattr(quotes, "split_bar") else FlatTailQuotes()
    replay = BookReplay(adapters, inst, policy=candidate_book_protection_policy(),
        initial_state=state or EvaluationState(100000, 100000, 100000, 0, 0),
        sizing_inputs=sizing or (lambda k, a, p: dict(lifecycle_tier="AUTHORIZED", **(
            dict(risk_dollars=700, per_contract_risk=35, cap_alloc=80) if k == "dj30_mym_p250"
            else dict(normal_base=1) if k == "vanguard_mgc" else {}))),
        schedule_quotes=provider, **({"broker_factory":broker_factory} if broker_factory else {}))
    return replay, adapters


def entry(adapter, bar, *, side=Side.BUY, timing=FillTiming.THIS_CLOSE, bracket=None):
    return [OrderIntent("base", adapter.leg_id, "entry", side, 1,
                        timing=timing, bracket=bracket, bar_time=bar.ts)]


def first_entry(adapter, bar):
    return entry(adapter, bar) if len(adapter.bars) == 1 else []


@pytest.mark.parametrize('kind', ['exit', 'flat'])
def test_scheduler_flatten_retires_queued_close_with_feedback(kind):
    def emit(adapter, bar):
        if len(adapter.bars) == 1:
            return entry(adapter, bar)
        if len(adapter.bars) == 2:
            return [OrderIntent('queued-close', adapter.leg_id, kind, Side.SELL, None,
                                timing=FillTiming.NEXT_OPEN)]
        return []
    session = path_session(prices=[(100, 100, 100, 100)] * 3)
    origin = session.source.bars[0].source_bar_time
    schedule = SessionSchedule(origin + timedelta(minutes=20), origin + timedelta(minutes=30),
                               origin + timedelta(minutes=35))
    session = replace(session, source=replace(session.source, schedule=schedule))
    replay, adapters = engine({'orb_mnq_v7': emit})
    result = replay.run((session,))
    assert result.sessions[0].end_edge.is_flat
    assert any(e.event == 'cancel' and e.order_id == 'queued-close'
               for e in adapters['orb_mnq_v7'].feedback)


def test_replay_close_entry_first_bar_has_only_fees_then_adverse_next_bar():
    replay, adapters = engine({"orb_mnq_v7": first_entry})
    result = replay.run((path_session(),))
    assert result.sessions[0].intraday_low == -10
    assert result.sessions[0].pnl == 0
    assert result.sessions[0].fills == 2
    assert result.sessions[0].end_edge.is_flat
    assert len(adapters["orb_mnq_v7"].bars) == 3


def test_repeated_reverse_source_bars_keep_adapter_state_and_accept_occurrences():
    def every_other(a, b):
        return entry(a, b) if len(a.bars) % 3 == 1 else []
    replay, adapters = engine({"orb_mnq_v7": every_other})
    result = replay.run((path_session(source_day=6), path_session(1, source_day=6), path_session(2, source_day=5)))
    assert [r.fills for r in result.sessions] == [2, 2, 2]
    assert len(adapters["orb_mnq_v7"].bars) == 9
    assert adapters["orb_mnq_v7"].bars[0].ts == adapters["orb_mnq_v7"].bars[3].ts


def test_barrier_aegis_capacity_precedes_other_legs_and_rejects_without_clip():
    emitters = {s.leg_id: (lambda a, b: entry(a, b, side=Side.SELL if a.leg_id == "aegis_6j" else Side.BUY)
                         if len(a.bars) == 1 else []) for s in BOOK_LEGS}
    replay, adapters = engine(emitters)
    result = replay.run((path_session(),))
    aegis_fills = [e.fill for e in adapters["aegis_6j"].feedback if e.fill]
    assert aegis_fills[0].qty == 8
    for k in ("dj30_mym_p250", "vanguard_mgc", "orb_mnq_v7"):
        assert any(e.event == "reject" for e in adapters[k].feedback)
    assert result.sessions[0].fills == 2


def test_striker_rounded_normal_quantity_is_not_risk_input():
    replay, _ = engine({"dj30_mym_p250": first_entry}, sizing=lambda *args:
                       dict(lifecycle_tier="AUTHORIZED", normal_base=20))
    with pytest.raises(ValueError, match="risk_dollars"):
        replay.run((path_session(),))


def test_missing_schedule_quote_refuses_instead_of_next_bar_price():
    def missing(*args):
        raise KeyError("no quote")
    replay, _ = engine({"orb_mnq_v7": first_entry}, quotes=missing)
    with pytest.raises(ReplayNeedsContext, match="source-instant"):
        replay.run((path_session(),))


def test_same_bar_take_profit_does_not_erase_adverse_lifetime():
    def emit(a, b):
        return entry(a, b, bracket=Bracket(limit=120)) if len(a.bars) == 1 else []
    replay, _ = engine({"orb_mnq_v7": emit})
    result = replay.run((path_session(prices=[(100, 100, 100, 100), (100, 120, 90, 115)]),))
    assert result.sessions[0].pnl == 20
    assert result.sessions[0].intraday_low == -10


def test_venue_commission_charged_once_on_repeated_source_occurrences():
    inst = {s.leg_id: Instrument(1, 1, 0, 3.10 if s.leg_id == "aegis_6j" else .91)
            for s in BOOK_LEGS}
    def emit(a, b):
        return entry(a, b) if len(a.bars) % 3 == 1 else []
    replay, _ = engine({"orb_mnq_v7": emit}, instruments=inst)
    result = replay.run((path_session(), path_session(1)))
    assert [r.pnl for r in result.sessions] == pytest.approx([-1.82, -1.82])
    assert [r.intraday_low for r in result.sessions] == pytest.approx([-10.91, -10.91])


class SplitQuotes:
    def __call__(self, session, instant, k):
        return 100

    def split_bar(self, session, pb, instant, k):
        original = dict(pb.bars)[k]
        return (Bar(original.ts, 100, 100, 100, 100),
                Bar(instant, 100, 110, 10, 100))


def closing_session():
    return path_session(start_hour=20, prices=[(100, 100, 100, 100)] * 3 + [(100, 110, 10, 100)])


def test_intrabar_flatten_does_not_inherit_post_flatten_low_and_signals_once():
    replay, adapters = engine({"orb_mnq_v7": first_entry}, quotes=SplitQuotes())
    result = replay.run((closing_session(),))
    assert result.sessions[0].intraday_low == 0
    assert result.sessions[0].fills == 2
    assert len(adapters["orb_mnq_v7"].bars) == 4
    flat = [e.fill for e in adapters["orb_mnq_v7"].feedback if e.fill and e.fill.kind == "flat"]
    assert flat[0].bar_time.hour == 20 and flat[0].bar_time.minute == 55
    assert any(e.path_time.minute == 55 and e.kind == "scheduled_flatten" for e in result.events)


def test_intrabar_exposure_without_split_fails_closed():
    replay, _ = engine({"orb_mnq_v7": first_entry})
    with pytest.raises(ReplayNeedsContext, match="split OHLC"):
        replay.run((closing_session(),))


def test_split_must_reaggregate_original_ohlc():
    class Bad(SplitQuotes):
        def split_bar(self, session, pb, instant, k):
            return Bar(pb.source_bar_time, 100, 100, 100, 100), Bar(instant, 100, 100, 100, 100)
    replay, _ = engine({"orb_mnq_v7": first_entry}, quotes=Bad())
    with pytest.raises(ReplayNeedsContext, match="aggregate"):
        replay.run((closing_session(),))


def test_stale_resting_order_cancel_releases_capacity_even_when_flat():
    def emit(a, b):
        return [OrderIntent("rest", a.leg_id, "entry", Side.BUY, 1, "stop", 200)] if len(a.bars) == 1 else []
    replay, adapters = engine({"orb_mnq_v7": emit})
    result = replay.run((path_session(prices=[(100, 100, 100, 100)] * 4),))
    assert result.sessions[0].fills == 0
    assert result.sessions[0].end_edge.is_flat
    cancelled = [e for e in adapters["orb_mnq_v7"].feedback if e.event == "cancel"]
    assert len(cancelled) == 1
    assert cancelled[0].bar_time.minute == 30


def test_aegis_whole_leg_takeover_closes_striker_before_entry():
    def striker(a, b):
        return entry(a, b) if len(a.bars) == 1 else []
    def aegis(a, b):
        return entry(a, b, side=Side.SELL) if len(a.bars) == 2 else []
    replay, adapters = engine({"aegis_6j": aegis, "dj30_mym_p250": striker})
    result = replay.run((path_session(prices=[(100,100,100,100)] * 3),))
    assert result.sessions[0].fills == 4
    assert any(e.kind == "capacity_takeover_admitted" for e in result.events)
    closed = [e.fill for e in adapters["dj30_mym_p250"].feedback if e.fill and e.fill.kind == "flat"]
    assert closed[0].qty == 20
    assert closed[0].reason == "capacity_takeover_close"


def test_cutoff_uses_completed_bar_time_not_open_label():
    def emit(a, b):
        return entry(a, b) if len(a.bars) == 3 else []
    replay, adapters = engine({"orb_mnq_v7": emit})
    result = replay.run((closing_session(),))
    assert result.sessions[0].fills == 0
    assert any(e.event == "reject" and e.detail == "scheduled entry cutoff"
               for e in adapters["orb_mnq_v7"].feedback)


def test_same_calculation_cancel_cannot_create_a_fill_or_fee():
    def emit(a, b):
        return entry(a, b) + [Cancel(a.leg_id, "base")] if len(a.bars) == 1 else []
    replay, adapters = engine({"orb_mnq_v7": emit})
    result = replay.run((path_session(),))
    assert result.sessions[0].fills == 0
    assert result.sessions[0].pnl == 0
    assert result.sessions[0].end_edge.is_flat
    assert any(e.event == "cancel" for e in adapters["orb_mnq_v7"].feedback)


def test_duplicate_accepted_entry_same_path_bar_dropped():
    def emit(a, b):
        return entry(a, b) * 2 if len(a.bars) == 1 else []
    replay, _ = engine({"orb_mnq_v7": emit})
    result = replay.run((path_session(),))
    assert result.sessions[0].fills == 2
    assert any(e.kind == "duplicate_dropped" for e in result.events)


def test_midbar_stop_marks_only_post_entry_remainder_in_engine():
    def emit(a, b):
        return [OrderIntent("rest", a.leg_id, "entry", Side.BUY, 1, "stop", 120)] if len(a.bars) == 1 else []
    replay, _ = engine({"orb_mnq_v7": emit}, quotes=lambda *args: 120)
    result = replay.run((path_session(prices=[(100, 100, 100, 100), (100, 130, 90, 115), (120,120,120,120)]),))
    assert result.sessions[0].intraday_low == -5


def test_crossleg_adverse_marks_sum_without_favorable_netting():
    replay, _ = engine({"orb_mnq_v7": first_entry, "vanguard_mgc": first_entry})
    result = replay.run((path_session(),))
    assert result.sessions[0].intraday_low == -20


def test_mode_changes_from_prior_settled_path_close_only():
    def emit(a, b):
        return entry(a, b) if len(a.bars) % 3 == 1 else []
    inst = {s.leg_id: Instrument(1, 100, 0, 0) for s in BOOK_LEGS}
    replay, adapters = engine({"orb_mnq_v7": emit}, instruments=inst, quotes=lambda *args: 80)
    prices = [(100,100,100,100), (100,100,80,80)]
    result = replay.run((path_session(prices=prices), path_session(1, prices=prices)))
    assert [m.value for m in adapters["orb_mnq_v7"].modes] == ["normal", "protected"]
    assert [r.pnl for r in result.sessions] == [-2000, -2000]


def test_confirmed_deadline_violation_is_t_infinity_with_partial_record():
    replay, _ = engine({"orb_mnq_v7": first_entry})
    replay._flatten = lambda *args: None  # synthetic broker withholds closure
    with pytest.raises(ReplayDeadlineFailure) as caught:
        replay.run((path_session(),))
    record = caught.value.result.sessions[-1]
    assert record.flat_before_deadline is False
    assert not record.end_edge.is_flat
    assert any(e.kind == "deadline_failure" for e in caught.value.result.events)


def test_schedule_cannot_invent_path_time_after_retained_bars():
    session = path_session()
    source = SourceSession(session.source.session_id, session.source.source_session_date,
        session.source.bars[:-1], session.source.schedule)
    short = PathSession(0, session.path_session_date, source, session.bars[:-1], True, True)
    replay, _ = engine()
    with pytest.raises(ReplayNeedsContext, match="retained path interval"):
        replay.run((short,))


def test_split_cannot_reorder_tv_extrema_even_if_ohlc_aggregation_matches():
    class Reordered(SplitQuotes):
        def split_bar(self, session, pb, instant, k):
            # Original O-H-L-C is replaced with O-L-H-L-C, which is not parity.
            return Bar(pb.source_bar_time,100,100,90,100), Bar(instant,100,110,10,100)
    replay, _ = engine({"orb_mnq_v7": first_entry}, quotes=Reordered())
    with pytest.raises(ReplayNeedsContext, match="accepted emulator path"):
        replay.run((closing_session(),))


def test_cancel_before_new_entry_does_not_cancel_new_order():
    def emit(a, b):
        return [Cancel(a.leg_id)] + entry(a, b) if len(a.bars) == 1 else []
    replay, _ = engine({"orb_mnq_v7": emit})
    assert replay.run((path_session(),)).sessions[0].fills == 2


@pytest.mark.parametrize("leg_id,side,prices,expected_pnl,expected_low", [
    ("orb_mnq_v7", Side.BUY, (80,85,70,80), -20, -30),
    ("aegis_6j", Side.SELL, (120,130,115,120), -160, -240),
])
def test_gap_stop_uses_open_price_and_full_adverse_lifetime(leg_id,side,prices,expected_pnl,expected_low):
    def emit(a, b):
        return entry(a,b,side=side,bracket=Bracket(stop=95 if side is Side.BUY else 105)) if len(a.bars)==1 else []
    replay, _ = engine({leg_id:emit})
    result = replay.run((path_session(prices=[(100,100,100,100),prices]),))
    assert result.sessions[0].pnl == expected_pnl
    assert result.sessions[0].intraday_low == expected_low


def test_same_bar_stop_target_uses_tv_order_but_retains_adverse_mark():
    def emit(a,b):
        return entry(a,b,bracket=Bracket(stop=95,limit=105)) if len(a.bars)==1 else []
    replay, _ = engine({"orb_mnq_v7":emit})
    result = replay.run((path_session(prices=[(100,100,100,100),(100,106,80,100)]),))
    assert result.sessions[0].pnl == 5
    assert result.sessions[0].intraday_low == -20


def test_protected_striker_77_displaced_by_protected_aegis_30():
    def striker(a,b):
        if len(a.bars)==1:
            return entry(a,b)
        if len(a.bars)==2:
            return [OrderIntent("add",a.leg_id,"add",Side.BUY,1,timing=FillTiming.THIS_CLOSE)]
        return []
    def aegis(a,b):
        return entry(a,b,side=Side.SELL) if len(a.bars)==3 else []
    replay, adapters = engine({"dj30_mym_p250":striker,"aegis_6j":aegis},
        state=EvaluationState(100000,98000,100000,1,0),
        sizing=lambda k,a,p: dict(lifecycle_tier="AUTHORIZED", **(
            dict(risk_dollars=700,per_contract_risk=4,cap_alloc=80) if k=="dj30_mym_p250" else {})))
    result = replay.run((path_session(prices=[(100,100,100,100)]*4),))
    striker_fills=[e.fill for e in adapters["dj30_mym_p250"].feedback if e.fill]
    assert [f.qty for f in striker_fills[:2]] == [22,55]
    assert sum(f.qty for f in striker_fills if f.kind=="flat") == 77
    aegis_fills=[e.fill for e in adapters["aegis_6j"].feedback if e.fill]
    assert aegis_fills[0].qty == 3
    assert any(e.kind=="capacity_takeover_admitted" for e in result.events)


def test_partial_takeover_close_refuses_aegis_and_preserves_remaining_truth():
    def aegis(a,b):
        return entry(a,b,side=Side.SELL) if len(a.bars)==2 else []
    replay, adapters = engine({"dj30_mym_p250":first_entry,"aegis_6j":aegis})
    normal_flatten = replay._flatten
    def partial(k, bar, reason):
        if reason == "capacity_takeover_close":
            replay._submit(k, [OrderIntent("partial",k,"flat",Side.SELL,1,
                           timing=FillTiming.THIS_CLOSE,reason=reason)], bar)
        else:
            normal_flatten(k,bar,reason)
    replay._flatten = partial
    result = replay.run((path_session(prices=[(100,100,100,100)]*3),))
    assert not any(e.fill for e in adapters["aegis_6j"].feedback)
    assert any(e.event=="reject" for e in adapters["aegis_6j"].feedback)
    fills = [e.fill for e in adapters["dj30_mym_p250"].feedback if e.fill]
    assert [f.qty for f in fills] == [20,1,19]
    assert result.sessions[0].end_edge.is_flat
    assert any(e.kind=="capacity_takeover_refused" for e in result.events)


def test_stop_before_flatten_boundary_is_not_delayed_to_schedule_quote():
    class Quotes:
        def __call__(self,*args):
            return 80
        def split_bar(self,session,pb,instant,k):
            return Bar(pb.source_bar_time,100,100,80,80), Bar(instant,80,80,10,80)
    prices = [(100,100,100,100)]*3 + [(100,100,10,80)]
    def emit(a,b):
        return entry(a,b,bracket=Bracket(stop=95)) if len(a.bars)==1 else []
    replay, adapters=engine({"orb_mnq_v7":emit},quotes=Quotes())
    result=replay.run((path_session(start_hour=20,prices=prices),))
    fills=[e.fill for e in adapters["orb_mnq_v7"].feedback if e.fill]
    assert [f.price for f in fills] == [100,95]
    assert result.sessions[0].pnl == -5
    assert len(adapters["orb_mnq_v7"].bars)==4


def test_rounded_stop_trigger_uses_broker_effective_level():
    def emit(a,b):
        return [OrderIntent("rounded",a.leg_id,"entry",Side.BUY,1,"stop",100.49)] if len(a.bars)==1 else []
    replay, _=engine({"orb_mnq_v7":emit},quotes=lambda *args:100.1)
    result=replay.run((path_session(prices=[(99,99,99,99),(99,100.2,98,100.1)]),))
    assert result.sessions[0].pnl == pytest.approx(.1)
    assert result.sessions[0].intraday_low == 0


def test_marketable_next_open_stop_retains_open_lifetime_after_conversion():
    def emit(a,b):
        return [OrderIntent("marketable",a.leg_id,"entry",Side.BUY,1,"stop",100)] if len(a.bars)==1 else []
    replay, _=engine({"orb_mnq_v7":emit},quotes=lambda *args:110)
    result=replay.run((path_session(prices=[(110,110,110,110),(90,120,80,110)]),))
    assert result.sessions[0].pnl == 20
    assert result.sessions[0].intraday_low == -10


def test_adverse_exit_slippage_combines_with_other_leg_remaining_excursion():
    def emit(a,b):
        return entry(a,b,bracket=Bracket(stop=95)) if len(a.bars)==1 else []
    inst={s.leg_id:Instrument(1,1,10 if s.leg_id=="orb_mnq_v7" else 0,0) for s in BOOK_LEGS}
    replay,_=engine({"orb_mnq_v7":emit,"vanguard_mgc":first_entry},instruments=inst)
    result=replay.run((path_session(prices=[(100,100,100,100),(100,100,90,100)]),))
    assert result.sessions[0].intraday_low == -35
    assert result.sessions[0].pnl == -25


def test_deadline_failure_keeps_earlier_adverse_excursion_after_recovery():
    replay,_=engine({"orb_mnq_v7":first_entry})
    replay._flatten=lambda *args:None
    with pytest.raises(ReplayDeadlineFailure) as caught:
        replay.run((path_session(),))
    assert caught.value.result.sessions[-1].intraday_low == -10


def test_original_batch_amend_precedes_orders_on_close_bracket_evaluation():
    def emit(a,b):
        return entry(a,b,bracket=Bracket(stop=110)) + [BracketAmend(a.leg_id,Bracket(stop=90))] if len(a.bars)==1 else []
    inst={s.leg_id:Instrument(1,1,0,0,orders_on_close=True) for s in BOOK_LEGS}
    replay,adapters=engine({"orb_mnq_v7":emit},instruments=inst)
    replay.run((path_session(prices=[(100,100,100,100)]*2),))
    fills=[e.fill for e in adapters["orb_mnq_v7"].feedback if e.fill]
    assert [f.kind for f in fills]==["entry","flat"]
    assert all(f.reason != "stop_close" for f in fills)


def test_oca_sibling_registered_before_marketable_stop_fills():
    def emit(a,b):
        if len(a.bars)==1:
            return entry(a,b)
        if len(a.bars)==2:
            return [OrderIntent("add-oca",a.leg_id,"add",Side.BUY,1,"stop",90,
                                timing=FillTiming.THIS_CLOSE,oca_group="pair"),
                    OrderIntent("entry-oca",a.leg_id,"entry",Side.BUY,1,"stop",95,
                                timing=FillTiming.THIS_CLOSE,oca_group="pair")]
        return []
    replay,adapters=engine({"orb_mnq_v7":emit})
    replay.run((path_session(prices=[(100,100,100,100)]*3),))
    fills=[e.fill for e in adapters["orb_mnq_v7"].feedback if e.fill]
    assert [f.kind for f in fills]==["entry","add","flat","flat"]
    assert any(e.event=="cancel" and e.order_id=="entry-oca"
               for e in adapters["orb_mnq_v7"].feedback)


def test_same_batch_add_has_no_unconfirmed_base_quantity():
    def emit(a,b):
        return entry(a,b)+[OrderIntent("premature",a.leg_id,"add",Side.BUY,1,
                                      timing=FillTiming.THIS_CLOSE)] if len(a.bars)==1 else []
    replay,adapters=engine({"orb_mnq_v7":emit})
    result=replay.run((path_session(),))
    assert result.sessions[0].fills==2
    assert any(e.event=="reject" and e.order_id=="premature"
               for e in adapters["orb_mnq_v7"].feedback)


class PartialBroker(TVBrokerEmulator):
    """Deterministic synthetic facts: half fills, terminal remainder cancel."""
    partial_kind = "entry"
    split_remainder = False

    def submit(self, actions, bar):
        start=len(self.events)
        super().submit(actions,bar)
        return self.events[start:]

    def _fill_entry(self,intent,price,ts,*,slip):
        if intent.kind != self.partial_kind or intent.qty < 2:
            return super()._fill_entry(intent,price,ts,slip=slip)
        qty=intent.qty//2
        event=super()._fill_entry(replace(intent,qty=qty),price,ts,slip=slip)
        if self.split_remainder:
            super()._fill_entry(replace(intent,qty=intent.qty-qty),price,ts,slip=slip)
        else:
            self._emit("cancel",ts,order_id=intent.order_id,detail="synthetic terminal remainder cancellation")
        return event


def striker_entry_then_add(a,b):
    if len(a.bars)==1:
        return entry(a,b)
    if len(a.bars)==2:
        return [OrderIntent("add",a.leg_id,"add",Side.BUY,50,timing=FillTiming.THIS_CLOSE)]
    return []


def test_partial_base_cancelled_remainder_add_uses_confirmed_base():
    replay,adapters=engine({"dj30_mym_p250":striker_entry_then_add},broker_factory=PartialBroker)
    result=replay.run((path_session(prices=[(100,100,100,100)]*3),))
    fills=[e.fill for e in adapters["dj30_mym_p250"].feedback if e.fill]
    assert [f.qty for f in fills[:2]]==[10,25]
    assert result.sessions[0].end_edge.is_flat
    assert replay.ledger.micro_used()==0


def test_two_confirmed_partial_base_fills_accumulate_before_add():
    class SplitBase(PartialBroker):
        split_remainder=True
    replay,adapters=engine({"dj30_mym_p250":striker_entry_then_add},broker_factory=SplitBase)
    result=replay.run((path_session(prices=[(100,100,100,100)]*3),))
    fills=[e.fill for e in adapters["dj30_mym_p250"].feedback if e.fill]
    assert [f.qty for f in fills[:3]]==[10,10,50]
    assert result.sessions[0].end_edge.is_flat


def test_partial_add_terminal_cancel_releases_exact_unused_capacity():
    class PartialAdd(PartialBroker):
        partial_kind="add"
    replay,adapters=engine({"dj30_mym_p250":striker_entry_then_add},broker_factory=PartialAdd)
    result=replay.run((path_session(prices=[(100,100,100,100)]*3),))
    fills=[e.fill for e in adapters["dj30_mym_p250"].feedback if e.fill]
    assert [f.qty for f in fills[:2]]==[20,25]
    assert result.sessions[0].end_edge.is_flat
    assert replay.ledger.micro_used()==0


@pytest.mark.parametrize("low,reason",[(95,"scheduled_flatten"),(85,"stop")])
def test_partial_scoped_exit_keeps_residual_and_its_bracket(low,reason):
    def emit(a,b):
        if len(a.bars)==1:
            return entry(a,b,bracket=Bracket(stop=90))
        if len(a.bars)==2:
            base=next(e.fill for e in a.feedback if e.fill)
            return [OrderIntent("partial-exit",a.leg_id,"exit",Side.SELL,10,
                timing=FillTiming.THIS_CLOSE,scope_fill_ids=(base.fill_id,))]
        return []
    replay,adapters=engine({"dj30_mym_p250":emit})
    result=replay.run((path_session(prices=[(100,100,100,100),(100,100,100,100),(100,100,low,100)]),))
    fills=[e.fill for e in adapters["dj30_mym_p250"].feedback if e.fill]
    assert [f.qty for f in fills]==[20,10,10]
    assert fills[-1].reason==reason
    assert result.sessions[0].end_edge.is_flat


def test_partial_at_capacity_boundary_releases_only_terminal_remainder():
    class PartialAegis(PartialBroker):
        def _fill_entry(self,intent,price,ts,*,slip):
            if self.leg_id!="aegis_6j":
                return TVBrokerEmulator._fill_entry(self,intent,price,ts,slip=slip)
            return super()._fill_entry(intent,price,ts,slip=slip)
    def aegis(a,b):
        return entry(a,b,side=Side.SELL) if len(a.bars)==1 else []
    replay,adapters=engine({"aegis_6j":aegis,"dj30_mym_p250":first_entry},broker_factory=PartialAegis)
    result=replay.run((path_session(),))
    fills={k:[e.fill for e in a.feedback if e.fill] for k,a in adapters.items()}
    assert fills["aegis_6j"][0].qty==4
    assert fills["dj30_mym_p250"][0].qty==20
    assert max(e.get("micro_used",0) for e in replay.ledger.events)<=80
    assert result.sessions[0].end_edge.is_flat


def test_final_bar_empty_flat_after_deadline_does_not_create_working_order():
    session=path_session()
    ts=session.source.bars[-1].source_bar_time+timedelta(minutes=15)
    sb=SourceBar(ts,tuple((s.leg_id,Bar(ts,100,100,100,100)) for s in BOOK_LEGS))
    pb=PathBar(session.bars[-1].path_time+timedelta(minutes=15),ts,
               session.source.source_session_date,ts.astimezone(ET),sb.bars)
    source=replace(session.source,bars=(*session.source.bars,sb))
    session=replace(session,source=source,bars=(*session.bars,pb))
    def emit(a,b):
        return [OrderIntent("empty-eod",a.leg_id,"flat",Side.SELL,None)] if len(a.bars)==4 else []
    replay,_=engine({"orb_mnq_v7":emit})
    result=replay.run((session,))
    assert result.sessions[0].flat_before_deadline
    assert result.sessions[0].end_edge.is_flat
    assert any(e.kind=="empty_exit_dropped" for e in result.events)


@pytest.mark.parametrize("qty",[None,1])
def test_stale_exit_scope_does_not_target_other_confirmed_lot(qty):
    def emit(a,b):
        if len(a.bars)==1:
            return entry(a,b)
        if len(a.bars)==2:
            return [OrderIntent("stale",a.leg_id,"exit",Side.SELL,qty,
                                scope_fill_ids=("already-closed",))]
        return []
    replay,adapters=engine({"orb_mnq_v7":emit})
    result=replay.run((path_session(),))
    assert any(e.kind=="empty_exit_dropped" for e in result.events)
    fills=[e.fill for e in adapters["orb_mnq_v7"].feedback if e.fill]
    assert [f.kind for f in fills]==["entry","flat"]


@pytest.mark.parametrize("timing",[FillTiming.THIS_CLOSE,FillTiming.NEXT_OPEN])
def test_same_batch_confirmed_market_entry_then_exit_keeps_native_scope(timing):
    def emit(a,b):
        return entry(a,b)+[OrderIntent("native-close",a.leg_id,"exit",Side.SELL,None,
                                      timing=timing)] if len(a.bars)==1 else []
    replay,adapters=engine({"orb_mnq_v7":emit})
    replay.run((path_session(),))
    fills=[e.fill for e in adapters["orb_mnq_v7"].feedback if e.fill]
    assert [f.order_id for f in fills]==["base","native-close"]


def test_cancelled_same_batch_entry_cannot_leave_empty_next_open_exit():
    def emit(a,b):
        return entry(a,b)+[Cancel(a.leg_id),OrderIntent("native-close",a.leg_id,"exit",Side.SELL,None)] if len(a.bars)==1 else []
    replay,_=engine({"orb_mnq_v7":emit})
    result=replay.run((path_session(),))
    assert result.sessions[0].fills==0
    assert any(e.kind=="empty_exit_dropped" for e in result.events)


def test_close_entry_has_no_prior_bar_excursion():
    bar = Bar(datetime(2026, 1, 5, tzinfo=timezone.utc), 100, 120, 80, 100)
    assert lifetime_adverse_mark(bar, Side.BUY, 100, 2, 1, "close") == 0


def test_open_long_and_short_contribute_full_adverse_extreme():
    bar = Bar(datetime(2026, 1, 5, tzinfo=timezone.utc), 100, 120, 90, 110)
    assert lifetime_adverse_mark(bar, Side.BUY, 100, 2, 1, "open") == -20
    assert lifetime_adverse_mark(bar, Side.SELL, 100, 3, 1, "open") == -60


def test_midbar_long_does_not_inherit_earlier_low():
    # O-L-H-C: the low is before the buy stop, so only the remainder counts.
    bar = Bar(datetime(2026, 1, 5, tzinfo=timezone.utc), 100, 130, 90, 115)
    assert lifetime_adverse_mark(bar, Side.BUY, 120, 1, 1, "midbar", 120) == -5


def test_midbar_requires_trigger_evidence():
    bar = Bar(datetime(2026, 1, 5, tzinfo=timezone.utc), 100, 130, 90, 115)
    with pytest.raises(ValueError, match="trigger"):
        lifetime_adverse_mark(bar, Side.BUY, 120, 1, 1, "midbar")


class StatefulStartupAdapter(Adapter):
    """Synthetic EMA/paper/readiness witness; not private native-port parity."""
    def __init__(self, leg_id):
        super().__init__(leg_id)
        self.ema=None
        self.paper=0.0
        self.trace=[]
        self.first_ready=None

    def on_bar(self,bar):
        self.bars.append(bar)
        previous=bar.close if self.ema is None else self.ema
        self.paper+=bar.close-previous
        self.ema=(previous+bar.close)/2
        self.trace.append((self.ema,self.paper))
        if self.first_ready is None and len(self.bars)>=4:
            self.first_ready=len(self.bars)
            return entry(self,bar)
        return []


def startup_engine():
    replay,_=engine(quotes=lambda session,instant,k:dict(session.source.bars[-1].bars)[k].close)
    adapter=StatefulStartupAdapter('orb_mnq_v7')
    replay.adapters[adapter.leg_id]=adapter
    return replay,adapter


def startup_path(days=(5,6,5)):
    return tuple(path_session(i,source_day=day,prices=[(price,price,price,price)]*2)
                 for i,day in enumerate(days) for price in [100 if day==5 else 104])


@pytest.mark.parametrize('days,expected',[
    ((5,6,5),[(100,0),(100,0),(100,0),(102,4),(103,6),(103.5,7),
              (101.75,3.5),(100.875,1.75),(100.4375,.875)]),
    ((6,5,6),[(104,0),(104,0),(104,0),(102,-4),(101,-6),(100.5,-7),
              (102.25,-3.5),(103.125,-1.75),(103.5625,-.875)])])
def test_repeated_reverse_occurrences_preserve_ema_and_paper_values(days,expected):
    replay,adapter=startup_engine()
    replay.run(startup_path(days))
    assert adapter.trace==expected
    assert adapter.bars[0].ts==adapter.bars[6].ts


def test_independent_paths_have_fresh_startup_broker_and_protection_state():
    first,first_adapter=startup_engine()
    before=first.run(startup_path())
    second,second_adapter=startup_engine()
    assert second_adapter.trace==[] and second_adapter.ema is None
    assert second.ledger.micro_used()==0 and second.confirmed_fill_count==0
    assert second.cash==100000 and second.clock.history==[]
    assert all(second.brokers[k] is not first.brokers[k] for k in second.brokers)
    after=second.run(startup_path())
    assert after==before and second_adapter.trace==first_adapter.trace
    second_adapter.trace.append(('independent','mutation'))
    assert first_adapter.trace[-1]==(100.4375,.875)


def test_identical_source_sequence_block_partition_does_not_reset_state_or_trades():
    path=startup_path()
    joined=tuple(replace(s,block_start=i==0,block_end=i==len(path)-1) for i,s in enumerate(path))
    split,split_adapter=startup_engine()
    continuous,continuous_adapter=startup_engine()
    split_result=split.run(path)
    continuous_result=continuous.run(joined)
    assert continuous_result==split_result
    assert continuous_adapter.trace==split_adapter.trace
    assert continuous_adapter.feedback==split_adapter.feedback


def test_startup_readiness_counts_original_bars_and_keeps_no_trade_sessions():
    path=startup_path()
    replay,adapter=startup_engine()
    result=replay.run(path)
    assert adapter.first_ready==4
    assert [s.fills for s in result.sessions]==[0,2,0]
    assert len(result.sessions)==len(path)==3
    assert adapter.bars==[dict(pb.bars)[adapter.leg_id] for session in path for pb in session.bars]
    assert len(adapter.trace)==9  # no prefed prefix, redraw, or schedule-segment updates


@pytest.mark.parametrize('risk,expected',[('124.9',4),('125',5)])
def test_c80_protected_striker_rounds_unscaled_risk_only_after_protection(risk,expected):
    replay,adapters=engine({'dj30_mym_p250':first_entry},
        state=EvaluationState(100000,98000,100000,1,0),
        sizing=lambda *args:dict(lifecycle_tier='AUTHORIZED',normal_base=12,
                                risk_dollars=Decimal(risk),per_contract_risk=Decimal('10'),cap_alloc=80))
    replay.run((path_session(prices=[(100,100,100,100)]*2),))
    fills=[e.fill for e in adapters['dj30_mym_p250'].feedback if e.fill]
    assert fills[0].qty==expected


class OrbOnlySplitQuotes(SplitQuotes):
    def __init__(self):self.calls=[]
    def __call__(self,session,instant,k):
        self.calls.append(('quote',k,instant))
        if k!='orb_mnq_v7':raise AssertionError('inert leg requested quote')
        return super().__call__(session,instant,k)
    def split_bar(self,session,pb,instant,k):
        self.calls.append(('split',k,instant))
        if k!='orb_mnq_v7':raise AssertionError('inert leg requested split')
        return super().split_bar(session,pb,instant,k)


def test_only_exposed_leg_requires_intrabar_split_and_flatten_quote():
    quotes=OrbOnlySplitQuotes()
    replay,adapters=engine({'orb_mnq_v7':first_entry},quotes=quotes)
    result=replay.run((closing_session(),))
    assert result.sessions[0].intraday_low==0
    assert result.sessions[0].fills==2 and result.sessions[0].end_edge.is_flat
    assert all(len(adapter.bars)==4 for adapter in adapters.values())
    assert all(k=='orb_mnq_v7' for _,k,_ in quotes.calls)
    assert not any(instant.minute==0 and instant.hour==21 for _,_,instant in quotes.calls)


def test_flat_path_needs_no_schedule_prices_or_splits_including_deadline():
    class NoEvidence:
        def __call__(self,*args):raise AssertionError('flat path requested quote')
        def split_bar(self,*args):raise AssertionError('flat path requested split')
    replay,adapters=engine(quotes=NoEvidence())
    result=replay.run((closing_session(),))
    assert result.sessions[0].fills==0 and result.sessions[0].flat_before_deadline
    assert all(len(adapter.bars)==4 for adapter in adapters.values())


def test_zero_position_pending_order_requires_pre_cutoff_interval_evidence():
    session=closing_session()
    # Place cutoff inside second source bar while the resting entry is young.
    cutoff=session.source.bars[1].source_bar_time+timedelta(minutes=5)
    session=replace(session,source=replace(session.source,schedule=SessionSchedule(
        cutoff,cutoff+timedelta(minutes=10),cutoff+timedelta(minutes=15))))
    def resting(a,b):
        return [OrderIntent('pending',a.leg_id,'entry',Side.BUY,1,'stop',200)] if len(a.bars)==1 else []
    class Missing:
        def __call__(self,*args):return 100
        def split_bar(self,*args):raise ReplayNeedsContext('pending exposure missing split')
    replay,_=engine({'orb_mnq_v7':resting},quotes=Missing())
    with pytest.raises(ReplayNeedsContext,match='pending exposure missing split'):
        replay.run((session,))


def test_pending_only_leg_consumes_its_split_then_cancels_without_later_quotes():
    session=closing_session()
    cutoff=session.source.bars[1].source_bar_time+timedelta(minutes=5)
    session=replace(session,source=replace(session.source,schedule=SessionSchedule(
        cutoff,cutoff+timedelta(minutes=10),cutoff+timedelta(minutes=15))))
    def resting(a,b):
        return [OrderIntent('pending',a.leg_id,'entry',Side.BUY,1,'stop',200)] if len(a.bars)==1 else []
    class PendingQuotes(OrbOnlySplitQuotes):
        def split_bar(self,session,pb,instant,k):
            self.calls.append(('split',k,instant))
            assert k=='orb_mnq_v7'
            original=dict(pb.bars)[k]
            return original,Bar(instant,100,100,100,100)
    quotes=PendingQuotes();replay,adapters=engine({'orb_mnq_v7':resting},quotes=quotes)
    result=replay.run((session,))
    assert result.sessions[0].fills==0 and result.sessions[0].end_edge.is_flat
    assert all(instant==cutoff for _,_,instant in quotes.calls)
    assert len([e for e in adapters['orb_mnq_v7'].feedback if e.event=='cancel'])==1
    assert all(len(a.bars)==4 for a in adapters.values())
