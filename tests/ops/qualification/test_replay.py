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


def schedule_split(prefix, suffix, executes=True):
    """The frozen T00 step-1b split return; legacy two-Bar tuples are refused."""
    from c1_rail.qualification.model import ScheduleSplit
    return ScheduleSplit(prefix, suffix, executes)


def engine(emitters=None, quotes=None, sizing=None, instruments=None, state=None, broker_factory=None):
    emitters = emitters or {}
    adapters = {s.leg_id: Adapter(s.leg_id, emitters.get(s.leg_id)) for s in BOOK_LEGS}
    inst = instruments or {s.leg_id: Instrument(1, 1, 0, 0) for s in BOOK_LEGS}
    class FlatTailQuotes:
        def __call__(self, *args):
            return quotes(*args) if quotes else 100

        def split_bar(self, session, pb, instant, k, *, exposure):
            original = dict(pb.bars)[k]
            price = self(session, instant, k)
            if not original.open == original.high == original.low == original.close == price:
                raise ReplayNeedsContext("synthetic fixture lacks split OHLC")
            return schedule_split(original, Bar(instant, price, price, price, price))
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

    def split_bar(self, session, pb, instant, k, *, exposure):
        original = dict(pb.bars)[k]
        return schedule_split(Bar(original.ts, 100, 100, 100, 100),
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
        def split_bar(self, session, pb, instant, k, *, exposure):
            return schedule_split(Bar(pb.source_bar_time, 100, 100, 100, 100), Bar(instant, 100, 100, 100, 100))
    replay, _ = engine({"orb_mnq_v7": first_entry}, quotes=Bad())
    with pytest.raises(ReplayNeedsContext, match="aggregate"):
        replay.run((closing_session(),))


def resting_orb_entry(price, *, cancel_at=None):
    """ORB's base stop entry, placed once on the first bar (§59 Rulings 6 and 7(a), L1).

    ``cancel_at`` stands in for the port's own session-end cancel. Each
    adapter bar records the replay's view of the entry before it evaluates.
    """
    seen = []
    def emit(a, b):
        replay = seen[0]
        seen.append((len(a.bars), tuple(replay.brokers["orb_mnq_v7"].pending_order_ids()),
                     replay.ledger.reserved.get("orb_mnq_v7", 0),
                     tuple(e.event for e in a.feedback if e.event == "cancel")))
        if len(a.bars) == 1:
            return [OrderIntent("rest", a.leg_id, "entry", Side.BUY, 1, "stop", price)]
        if len(a.bars) == cancel_at:
            return [Cancel(a.leg_id, "rest")]
        return []
    return emit, seen


def run_orb(emit, seen, prices, *, quote=100):
    replay, adapters = engine({"orb_mnq_v7": emit}, quotes=lambda *args: quote)
    seen.insert(0, replay)
    result = replay.run((path_session(prices=prices),))
    return replay, adapters["orb_mnq_v7"], result, seen[1:]


def test_orb_base_entry_is_not_cancelled_one_bar_after_admission():
    emit, seen = resting_orb_entry(200)
    replay, adapter, result, views = run_orb(emit, seen, [(100, 100, 100, 100)] * 4)
    # Bars 3 and 4 are past RC-9's one-bar age: the entry still rests,
    # its reservation is held and no cancel feedback has been delivered.
    for number in (3, 4):
        assert views[number - 1] == (number, ("rest",), 1, ())
    cancelled = [e for e in adapter.feedback if e.event == "cancel"]
    assert len(cancelled) == 1 and cancelled[0].bar_time.minute == 0 and cancelled[0].bar_time.hour == 15
    assert result.sessions[0].fills == 0
    assert result.sessions[0].end_edge.is_flat


def test_orb_base_entry_fills_on_crossing_after_first_bar():
    emit, seen = resting_orb_entry(110)
    prices = [(100, 100, 100, 100)] * 3 + [(100, 115, 95, 110)]
    replay, adapter, result, views = run_orb(emit, seen, prices, quote=110)
    fills = [e.fill for e in adapter.feedback if e.fill]
    assert [(f.kind, f.price, f.bar_time.minute) for f in fills[:1]] == [("entry", 110, 45)]
    assert views[2] == (3, ("rest",), 1, ())
    assert not any(e.event == "cancel" for e in adapter.feedback)
    assert result.sessions[0].end_edge.is_flat


def test_orb_base_entry_ends_on_port_session_end_cancel_and_releases_capacity():
    emit, seen = resting_orb_entry(200, cancel_at=4)
    replay, adapter, result, views = run_orb(emit, seen, [(100, 100, 100, 100)] * 4)
    assert views[3] == (4, ("rest",), 1, ())
    cancelled = [e for e in adapter.feedback if e.event == "cancel"]
    assert [(e.order_id, e.bar_time.minute) for e in cancelled] == [("rest", 45)]
    assert views[4] == (5, (), 0, ("cancel",))
    assert result.sessions[0].fills == 0
    assert result.sessions[0].end_edge.is_flat


def test_orb_base_entry_cancelled_at_scheduled_cutoff():
    emit, seen = resting_orb_entry(200)
    session = path_session(prices=[(100, 100, 100, 100)] * 4)
    replay, adapters = engine({"orb_mnq_v7": emit})
    seen.insert(0, replay)
    result = replay.run((session,))
    cutoff = session.source.schedule.cutoff
    cancelled = [e for e in adapters["orb_mnq_v7"].feedback if e.event == "cancel"]
    assert [(e.order_id, e.bar_time) for e in cancelled] == [("rest", cutoff)]
    assert any(e.kind == "scheduled_cutoff" and e.detail == cutoff.isoformat() for e in result.events)
    assert replay.ledger.reserved.get("orb_mnq_v7", 0) == 0
    assert result.sessions[0].end_edge.is_flat


@pytest.mark.parametrize("leg_id,kind,created", [
    ("vanguard_mgc", "entry", 1),
    ("dj30_mym_p250", "entry", 1),
    ("orb_mnq_v7", "add", 2),
])
def test_one_bar_cancel_still_applies_to_non_orb_base_resting_order(leg_id, kind, created):
    def emit(a, b):
        if kind == "add" and len(a.bars) == 1:
            return entry(a, b)
        if len(a.bars) == created:
            return [OrderIntent("rest", a.leg_id, kind, Side.BUY, 1, "stop", 200)]
        return []
    replay, adapters = engine({leg_id: emit})
    result = replay.run((path_session(prices=[(100, 100, 100, 100)] * 4),))
    cancelled = [e for e in adapters[leg_id].feedback if e.event == "cancel" and e.order_id == "rest"]
    assert len(cancelled) == 1
    assert cancelled[0].bar_time.minute == 15 * (created + 1)
    assert not any(e.fill and e.fill.order_id == "rest" for e in adapters[leg_id].feedback)
    assert result.sessions[0].end_edge.is_flat


@pytest.mark.parametrize("prices,fill_minute", [
    ([(100, 100, 100, 100)] * 3 + [(100, 115, 95, 110)], 45),
    ([(100, 100, 100, 100), (100, 104, 99, 103), (103, 109, 101, 108), (108, 109, 104, 105)], None),
])
def test_orb_base_entry_lifecycle_matches_emulator_without_schedule_overlay(prices, fill_minute):
    """Parity (RC-4): over bars with no schedule event inside the span, the
    replay's ORB base entry fills or keeps resting exactly as the emulator's."""
    from c1_signal_daemon.tv_broker_emulator import run_adapter
    emit, seen = resting_orb_entry(110)
    replay, adapter, result, views = run_orb(emit, seen, prices, quote=prices[-1][-1])
    session = path_session(prices=prices)
    span = [dict(pb.bars)["orb_mnq_v7"] for pb in session.bars
            if pb.source_bar_time < session.source.schedule.cutoff]
    assert len(span) == 4
    mirror = Adapter("orb_mnq_v7", lambda a, b: (
        [OrderIntent("rest", a.leg_id, "entry", Side.BUY, 1, "stop", 110)] if len(a.bars) == 1 else []))
    emulator = run_adapter(mirror, span, TVBrokerEmulator("orb_mnq_v7", 1, 1, 0, 0, margin_pct=0))
    emulated = [e.fill.bar_time for e in mirror.feedback if e.fill and e.fill.kind == "entry"]
    replayed = [e.fill.bar_time for e in adapter.feedback if e.fill and e.fill.kind == "entry"]
    assert replayed == emulated
    assert [t.minute for t in replayed] == ([] if fill_minute is None else [fill_minute])
    assert not any(e.event == "cancel" for e in mirror.feedback)
    before_cutoff = [e for e in adapter.feedback
                     if e.event == "cancel" and e.bar_time < session.source.schedule.cutoff]
    assert before_cutoff == []
    if fill_minute is None:
        assert emulator.pending_order_ids() == ["rest"]
        assert views[3] == (4, ("rest",), 1, ())


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
        def split_bar(self, session, pb, instant, k, *, exposure):
            # Original O-H-L-C is replaced with O-L-H-L-C, which is not parity.
            return schedule_split(Bar(pb.source_bar_time,100,100,90,100), Bar(instant,100,110,10,100))
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
        def split_bar(self,session,pb,instant,k,*,exposure):
            return schedule_split(Bar(pb.source_bar_time,100,100,80,80), Bar(instant,80,80,10,80))
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
    def split_bar(self,session,pb,instant,k,*,exposure):
        self.calls.append(('split',k,instant))
        if k!='orb_mnq_v7':raise AssertionError('inert leg requested split')
        return super().split_bar(session,pb,instant,k,exposure=exposure)


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
        def split_bar(self,*args,**kwargs):raise AssertionError('flat path requested split')
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
        def split_bar(self,*args,exposure):raise ReplayNeedsContext('pending exposure missing split')
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
        def split_bar(self,session,pb,instant,k,*,exposure):
            self.calls.append(('split',k,instant))
            assert k=='orb_mnq_v7'
            original=dict(pb.bars)[k]
            return schedule_split(original,Bar(instant,100,100,100,100))
    quotes=PendingQuotes();replay,adapters=engine({'orb_mnq_v7':resting},quotes=quotes)
    result=replay.run((session,))
    assert result.sessions[0].fills==0 and result.sessions[0].end_edge.is_flat
    assert all(instant==cutoff for _,_,instant in quotes.calls)
    assert len([e for e in adapters['orb_mnq_v7'].feedback if e.event=='cancel'])==1
    assert all(len(a.bars)==4 for a in adapters.values())


# ---- T00 step-1b Task 2: frozen bracket split interface (packet §7) ----
# Case names carry the §7 "Required test update" item number (item1..item7).

def bracket_provider(run):
    """A fresh run-local provider over reviewed (here empty) evidence rows."""
    import json
    from c1_rail.qualification.production_source import (
        ScheduleExecutionBracket, parse_schedule_execution_evidence)
    raw = json.dumps({'schema': 'qualification-schedule-execution/v1', 'rows': []}).encode()
    return ScheduleExecutionBracket(parse_schedule_execution_evidence(raw)).for_run(run)


def exposure_of(position, pending, reserved):
    from c1_rail.qualification.model import ScheduleExposure
    return ScheduleExposure(position, pending, reserved)


class Recording:
    """Delegates to a frozen provider; records each split and the engine state."""

    def __init__(self, inner):
        self.inner, self.calls, self.replay = inner, [], None

    def __call__(self, session, instant, k):
        return self.inner(session, instant, k)

    def _state(self, k):
        r = self.replay
        return (r.brokers[k].position(), tuple(r.brokers[k].pending_order_ids()),
                r.ledger.reserved.get(k, 0),
                sum(i.qty for (leg, _), (i, _) in r.orders.items() if leg == k))

    def split_bar(self, session, pb, instant, k, *, exposure):
        state = self._state(k)
        split = self.inner.split_bar(session, pb, instant, k, exposure=exposure)
        self.calls.append(('bar', session.occurrence, k, instant, dict(pb.bars)[k], exposure, split, state))
        return split

    def split_interval(self, session, pb, original, instant, k, *, exposure):
        state = self._state(k)
        split = self.inner.split_interval(session, pb, original, instant, k, exposure=exposure)
        self.calls.append(('interval', session.occurrence, k, instant, original, exposure, split, state))
        return split


def bracket_engine(run, emitters, **kwargs):
    quotes = Recording(bracket_provider(run))
    replay, adapters = engine(emitters, quotes=quotes, **kwargs)
    quotes.replay = replay
    return replay, adapters, quotes


def cutoff_session(prices, *, occurrence=0, bar=1, offset=5, source_day=5):
    """Four M15 bars; cutoff ``offset`` minutes into ``bar``, flatten +10, deadline +15."""
    session = path_session(occurrence, start_hour=20, prices=prices, source_day=source_day)
    cutoff = session.source.bars[bar].source_bar_time + timedelta(minutes=offset)
    return replace(session, source=replace(session.source, schedule=SessionSchedule(
        cutoff, cutoff + timedelta(minutes=10), cutoff + timedelta(minutes=15))))


def stub_split(prefix, suffix, executes, quote=None):
    class Stub:
        def __call__(self, session, instant, k):
            return prefix.close if quote is None else quote

        def split_bar(self, session, pb, instant, k, *, exposure):
            return schedule_split(prefix, suffix, executes)
    return Stub()


T2_START = datetime(2026, 3, 2, 20, 45, tzinfo=timezone.utc)
T2_INSTANT = T2_START + timedelta(minutes=7)


def split_direct(provider, bar, exposures, *, session=None):
    from types import SimpleNamespace
    session = session or SimpleNamespace(occurrence=0, bars=(),
                                         source=SimpleNamespace(source_session_date=bar.ts.date()))
    pb = SimpleNamespace(source_bar_time=bar.ts, bars=(('leg', bar),))
    return BookReplay._split(SimpleNamespace(schedule_quotes=provider), session, pb,
                             {'leg': bar}, T2_INSTANT, exposures)


def test_t2_item1_split_refuses_legacy_two_bar_tuple():
    original = Bar(T2_START, 100, 100, 100, 100)

    class TupleProvider:
        def __call__(self, *args):
            return 100

        def split_bar(self, session, pb, instant, k, *, exposure):
            return original, Bar(instant, 100, 100, 100, 100)
    with pytest.raises(ReplayNeedsContext, match='ScheduleSplit'):
        split_direct(TupleProvider(), original, {'leg': exposure_of(1, False, 0)})


def test_t2_item1_split_refuses_positional_legacy_provider():
    original = Bar(T2_START, 100, 100, 100, 100)

    class Legacy:
        def __call__(self, *args):
            return 100

        def split_bar(self, session, pb, instant, k):
            return original, Bar(instant, 100, 100, 100, 100)
    with pytest.raises(TypeError, match='exposure'):
        split_direct(Legacy(), original, {'leg': exposure_of(1, False, 0)})


@pytest.mark.parametrize('channel', ['observe_exposure', 'prefix_is_empty'])
def test_t2_item1_split_refuses_side_channel_providers(channel):
    original = Bar(T2_START, 100, 100, 100, 100)
    provider = stub_split(original, Bar(T2_INSTANT, 100, 100, 100, 100), True)
    setattr(type(provider), channel, lambda self, *args: pytest.fail('side channel consulted'))
    with pytest.raises(ReplayNeedsContext, match='side channel'):
        split_direct(provider, original, {'leg': exposure_of(1, False, 0)})


@pytest.mark.parametrize('exposures', [{}, {'leg': None}, {'leg': (1, False, 0)}])
def test_t2_item1_split_requires_a_captured_exposure_for_every_leg(exposures):
    original = Bar(T2_START, 100, 100, 100, 100)
    provider = stub_split(original, Bar(T2_INSTANT, 100, 100, 100, 100), True)
    with pytest.raises(ReplayNeedsContext, match='exposure'):
        split_direct(provider, original, exposures)


def test_t2_item1_split_returns_one_schedule_split_per_leg():
    from c1_rail.qualification.model import ScheduleSplit
    original = Bar(T2_START, 100, 120, 90, 110, 7)
    splits = split_direct(bracket_provider('R1'), original, {'leg': exposure_of(1, False, 0)})
    assert type(splits) is dict and list(splits) == ['leg']
    assert type(splits['leg']) is ScheduleSplit


# Path 100 -> 110 -> 90 -> 105: a short's favourable vertex (90) is reached
# only after the high, so its R2 lifetime low still carries the high.
@pytest.mark.parametrize('leg_id,side,qty', [('orb_mnq_v7', Side.BUY, 1), ('aegis_6j', Side.SELL, 8)])
def test_t2_item2_held_long_and_short_flatten_at_each_runs_vertex(leg_id, side, qty):
    session = path_session(start_hour=20, prices=[(100, 100, 100, 100)] * 3 + [(100, 110, 90, 105)])
    def emit(a, b):
        return entry(a, b, side=side) if len(a.bars) == 1 else []
    long = side is Side.BUY
    expected = {'R1': (90 if long else 110, -10 * qty, -10 * qty),
                'R2': (110 if long else 90, 10 * qty, 0 if long else -10 * qty)}
    for run in ('R1', 'R2'):
        replay, adapters, quotes = bracket_engine(run, {leg_id: emit})
        record = replay.run((session,)).sessions[0]
        flats = [e.fill for e in adapters[leg_id].feedback if e.fill and e.fill.kind == 'flat']
        (call,) = quotes.calls
        assert call[5] == exposure_of(qty if long else -qty, False, 0)
        assert call[6].prefix_executes is True
        assert (flats[0].price, record.pnl, record.intraday_low) == expected[run]
        assert all(len(a.bars) == 4 for a in adapters.values())


def test_t2_item2_position_plus_pending_follows_position_rule_and_prefix_reach():
    # Schedule bar path 100 -> 90 -> 115 -> 100. The long's R1 adverse vertex
    # (90) never reaches the pending add's 105 stop; R2's favourable vertex
    # (115) does, so only R2's executed prefix fills the add.
    session = cutoff_session([(100, 100, 100, 100), (100, 100, 100, 100),
                              (100, 115, 90, 100), (100, 100, 100, 100)], bar=2)
    def emit(a, b):
        if len(a.bars) == 1:
            return entry(a, b)
        if len(a.bars) == 2:
            return [OrderIntent('add', a.leg_id, 'add', Side.BUY, 1, 'stop', 105)]
        return []
    adds = {}
    for run in ('R1', 'R2'):
        replay, adapters, quotes = bracket_engine(run, {'orb_mnq_v7': emit})
        record = replay.run((session,)).sessions[0]
        (call,) = quotes.calls
        exposure, split = call[5], call[6]
        assert exposure.position == 1 and exposure.pending is True and exposure.reserved > 0
        assert split.prefix_executes is True
        assert split.prefix.close == (90 if run == 'R1' else 115)
        adds[run] = [e.fill.price for e in adapters['orb_mnq_v7'].feedback if e.fill and e.fill.kind == 'add']
        assert record.end_edge.is_flat
    assert adds == {'R1': [], 'R2': [105]}


def test_t2_item3_r2_pending_only_cancels_before_gap_open_fill_on_ordinary_bar():
    session = cutoff_session([(100, 100, 100, 100), (110, 115, 85, 100),
                              (100, 100, 100, 100), (100, 100, 100, 100)])
    def resting(a, b):
        return [OrderIntent('pending', a.leg_id, 'entry', Side.BUY, 1, 'stop', 105)] if len(a.bars) == 1 else []
    outcome = {}
    for run in ('R1', 'R2'):
        replay, adapters, quotes = bracket_engine(run, {'orb_mnq_v7': resting})
        record = replay.run((session,)).sessions[0]
        (call,) = quotes.calls
        assert call[5] == exposure_of(0, True, 1)
        assert (call[6].prefix_executes, call[6].prefix.close) == ((True, 100) if run == 'R1' else (False, 110))
        feedback = adapters['orb_mnq_v7'].feedback
        outcome[run] = ([e.fill.price for e in feedback if e.fill],
                        any(e.event == 'cancel' and e.order_id == 'pending' for e in feedback),
                        record.pnl, record.intraday_low)
        assert record.end_edge.is_flat and all(len(a.bars) == 4 for a in adapters.values())
    assert outcome['R1'][:3] == ([110, 100], False, -10)
    assert outcome['R2'] == ([], True, 0, 0)


def test_t2_item3_r2_pending_only_cancels_on_flat_zero_volume_bar():
    # Prefix and suffix have identical flat OHLC and zero volume, so no bar
    # shape can reveal the empty execution prefix; only prefix_executes can.
    session = cutoff_session([(100, 100, 100, 100)] * 4)
    def queued(a, b):
        return [OrderIntent('pending', a.leg_id, 'entry', Side.BUY, 1, timing=FillTiming.NEXT_OPEN)] if len(a.bars) == 1 else []
    for run in ('R1', 'R2'):
        replay, adapters, quotes = bracket_engine(run, {'orb_mnq_v7': queued})
        record = replay.run((session,)).sessions[0]
        (call,) = quotes.calls
        split = call[6]
        assert call[5] == exposure_of(0, True, 1)
        shape = lambda bar: (bar.open, bar.high, bar.low, bar.close, bar.volume)
        assert shape(split.prefix) == shape(split.suffix) == (100, 100, 100, 100, 0)
        assert split.prefix_executes is (run == 'R1')
        fills = [e.fill for e in adapters['orb_mnq_v7'].feedback if e.fill]
        if run == 'R1':
            assert [f.kind for f in fills] == ['entry', 'flat'] and record.fills == 2
        else:
            assert fills == [] and record.fills == 0
            assert any(e.event == 'cancel' and e.order_id == 'pending'
                       for e in adapters['orb_mnq_v7'].feedback)
        assert record.end_edge.is_flat


def test_t2_item3_non_executing_prefix_is_refused_for_a_position_leg():
    session = path_session(start_hour=20, prices=[(100, 100, 100, 100)] * 4)
    class SkipsPrefix:
        def __call__(self, session, instant, k):
            return 100

        def split_bar(self, session, pb, instant, k, *, exposure):
            original = dict(pb.bars)[k]
            return schedule_split(original, Bar(instant, 100, 100, 100, 100), False)
    replay, _ = engine({'orb_mnq_v7': first_entry}, quotes=SkipsPrefix())
    with pytest.raises(ReplayNeedsContext, match='non-executing prefix'):
        replay.run((session,))


def t2_generated_bars():
    import random
    rng = random.Random(20260929)
    bars = [Bar(T2_START, 100, 120, 90, 110, 7), Bar(T2_START, 100, 110, 90, 95, 1),  # H-O = O-L tie
            Bar(T2_START, 100, 100, 90, 100, 1), Bar(T2_START, 100, 110, 100, 100, 1),  # flat open/close
            Bar(T2_START, 100, 110, 90, 110, 2), Bar(T2_START, 100, 110, 90, 90, 2),    # close at an extreme
            Bar(T2_START, 100, 100, 100, 100, 1), Bar(T2_START, 100, 100, 100, 100, 0)]  # flat, zero volume
    for _ in range(20000):
        o, c = rng.randint(50, 150), rng.randint(50, 150)
        bars.append(Bar(T2_START, o, max(o, c) + rng.randint(0, 20), min(o, c) - rng.randint(0, 20), c,
                        rng.randint(0, 9)))
    return bars


def test_t2_item4_frozen_splits_of_20000_generated_bars_pass_split_unchanged():
    from types import SimpleNamespace
    from c1_rail.qualification.model import ScheduleSplit
    from c1_rail.qualification.replay import accepted_path
    cases = [('R1', (1, False, 0), min, True), ('R2', (1, False, 0), max, True),
             ('R1', (-2, True, 1), max, True), ('R2', (-2, True, 1), min, True),
             ('R1', (0, True, 1), lambda p: p[-1], True), ('R2', (0, True, 1), lambda p: p[0], False)]
    providers = {run: bracket_provider(run) for run in ('R1', 'R2')}
    checked = 0
    for n, bar in enumerate(t2_generated_bars()):
        path = accepted_path(bar)
        for j, (run, exposure, vertex, executes) in enumerate(cases):
            session = SimpleNamespace(occurrence=n * len(cases) + j, bars=(),
                                      source=SimpleNamespace(source_session_date=bar.ts.date()))
            splits = split_direct(providers[run], bar, {'leg': exposure_of(*exposure)}, session=session)
            split = splits['leg']
            assert type(split) is ScheduleSplit and split.prefix_executes is executes
            assert split.prefix.close == vertex(path) == providers[run](session, T2_INSTANT, 'leg')
            checked += 1
    assert checked >= 20000 * len(cases)


@pytest.mark.parametrize('executes', [True, False])
def test_t2_item4_split_rejections_unchanged_even_when_prefix_does_not_execute(executes):
    from c1_rail.qualification.bracket import vertex_split
    original = Bar(T2_START, 100, 120, 90, 110, 7)  # accepted path 100 -> 90 -> 120 -> 110
    prefix, suffix = vertex_split(original, 1, T2_INSTANT)
    exposures = {'leg': exposure_of(0, True, 1)}
    assert split_direct(stub_split(prefix, suffix, executes), original, exposures)['leg'].prefix == prefix
    rejected = [
        ('aggregate', replace(prefix, high=121), suffix, None),
        ('aggregate', prefix, replace(suffix, volume=1), None),
        ('aggregate', replace(prefix, open=99, low=90), suffix, None),
        ('aggregate', replace(prefix, ts=T2_INSTANT), suffix, None),
        ('aggregate', prefix, replace(suffix, ts=T2_START), None),
        ('aggregate', prefix, replace(suffix, open=91), None),
        ('invalid split OHLC', Bar(T2_START, 100, 100, 100, 90, 7), Bar(T2_INSTANT, 90, 120, 90, 110, 0), None),
        ('schedule price', prefix, suffix, prefix.close + 1),
        ('accepted emulator path', Bar(T2_START, 100, 120, 90, 120, 7), Bar(T2_INSTANT, 120, 120, 90, 110, 0), None),
    ]
    for message, bad_prefix, bad_suffix, quote in rejected:
        with pytest.raises(ReplayNeedsContext, match=message):
            split_direct(stub_split(bad_prefix, bad_suffix, executes, quote), original, exposures)


def test_t2_item5_second_same_bar_boundary_splits_retained_suffix_with_fresh_exposure():
    # Cutoff 2 and flatten 12 minutes into one source bar whose path is
    # 100 -> 95 -> 130 -> 110; a pending add stop at 105 rests at the cutoff.
    session = cutoff_session([(100, 100, 100, 100), (100, 100, 100, 100),
                              (100, 130, 95, 110), (100, 100, 100, 100)], bar=2, offset=2)
    cutoff, flatten = session.source.schedule.cutoff, session.source.schedule.flatten_start
    def emit(a, b):
        if len(a.bars) == 1:
            return entry(a, b)
        if len(a.bars) == 2:
            return [OrderIntent('add', a.leg_id, 'add', Side.BUY, 1, 'stop', 105)]
        return []
    for run, first_close, flat_price in (('R1', 95, 95), ('R2', 130, 130)):
        replay, adapters, quotes = bracket_engine(run, {'orb_mnq_v7': emit})
        record = replay.run((session,)).sessions[0]
        first, second = quotes.calls
        assert (first[0], first[3], first[4]) == ('bar', cutoff, dict(session.bars[2].bars)['orb_mnq_v7'])
        assert first[5].position == 1 and first[5].pending is True and first[5].reserved > 0
        assert first[6].prefix.close == first_close
        # The second split receives the first split's suffix, not the source bar.
        assert (second[0], second[3], second[4]) == ('interval', flatten, first[6].suffix)
        assert second[5].pending is False and second[5].reserved == 0
        assert second[5].position == (1 if run == 'R1' else 1 + first[5].reserved)
        for call in (first, second):
            position, pending, reserved, outstanding = call[7]
            assert call[5] == exposure_of(position, bool(pending), reserved)
            assert reserved == outstanding
        flats = [e.fill for e in adapters['orb_mnq_v7'].feedback if e.fill and e.fill.kind == 'flat']
        assert flats and all(f.price == flat_price for f in flats)
        assert record.end_edge.is_flat and all(len(a.bars) == 4 for a in adapters.values())


def t2_resting(price, kind='entry'):
    def emit(a, b):
        if kind == 'add':
            if len(a.bars) == 1:
                return entry(a, b)
            return [OrderIntent('add', a.leg_id, 'add', Side.BUY, 1, 'stop', price)] if len(a.bars) == 2 else []
        return [OrderIntent('rest', a.leg_id, 'entry', Side.BUY, 1, 'stop', price)] if len(a.bars) == 1 else []
    return emit


@pytest.mark.parametrize('leg_id,emit,bar,expected', [
    ('orb_mnq_v7', first_entry, 1, (1, False, 0)),                                    # THIS_CLOSE position
    ('vanguard_mgc', lambda a, b: entry(a, b, timing=FillTiming.NEXT_OPEN) if len(a.bars) == 1 else [],
     1, (0, True, 1)),                                                                 # queued NEXT_OPEN entry
    ('dj30_mym_p250', t2_resting(200), 1, (0, True, 20)),                              # resting stop entry
    ('orb_mnq_v7', t2_resting(200), 1, (0, True, 1)),                                  # L1 resting base entry
    ('orb_mnq_v7', t2_resting(200, 'add'), 2, None),                                   # position + resting add
])
@pytest.mark.parametrize('run', ['R1', 'R2'])
def test_t2_item6_native_states_satisfy_reservation_invariants_at_schedule_callbacks(run, leg_id, emit, bar, expected):
    session = cutoff_session([(100, 100, 100, 100)] * 4, bar=bar)
    replay, _, quotes = bracket_engine(run, {leg_id: emit})
    record = replay.run((session,)).sessions[0]
    assert quotes.calls and record.end_edge.is_flat
    for call in quotes.calls:
        position, pending, reserved, outstanding = call[7]
        assert call[5] == exposure_of(position, bool(pending), reserved)
        assert reserved == outstanding                 # reservation equals the order sum
        assert reserved == 0 or pending                # a reservation implies a pending order
    first = quotes.calls[0][5]
    if expected is None:
        assert first.position == 1 and first.pending is True and first.reserved > 0
    else:
        assert first == exposure_of(*expected)


@pytest.mark.parametrize('held', [False, True])
def test_t2_item6_reservation_only_state_is_refused_before_any_split(held):
    session = cutoff_session([(100, 100, 100, 100)] * 4)
    seen = []
    def inject(a, b):
        if len(a.bars) == 1:
            seen[0].ledger.reserved['orb_mnq_v7'] = seen[0].ledger.reserved.get('orb_mnq_v7', 0) + 1
            return entry(a, b) if held else []
        return []
    for run in ('R1', 'R2'):
        replay, _, quotes = bracket_engine(run, {'orb_mnq_v7': inject})
        seen[:] = [replay]
        with pytest.raises(ReplayNeedsContext, match='broker-pending'):
            replay.run((session,))
        assert quotes.calls == []


def test_t2_item7_one_bar_call_unchanged_costs_and_occurrence_local_quotes():
    # One source session replayed twice: the first occurrence holds a long at
    # the cutoff, the second only a pending stop. The same source (date, leg,
    # instant) gets each occurrence's own exposure-dependent placement.
    prices = [(100, 100, 100, 100), (100, 115, 90, 100), (100, 100, 100, 100), (100, 100, 100, 100)]
    sessions = (cutoff_session(prices), cutoff_session(prices, occurrence=1))
    assert sessions[0].source == sessions[1].source
    cutoff = sessions[0].source.schedule.cutoff
    def emit(a, b):
        if len(a.bars) == 1:
            return entry(a, b)
        if len(a.bars) == 5:
            return [OrderIntent('pending', a.leg_id, 'entry', Side.BUY, 1, 'stop', 120)]
        return []
    inst = {s.leg_id: Instrument(1, 1, 0, .91) for s in BOOK_LEGS}
    placed = {}
    for run in ('R1', 'R2'):
        replay, adapters, quotes = bracket_engine(run, {'orb_mnq_v7': emit}, instruments=inst)
        result = replay.run(sessions)
        assert [(c[1], c[3], c[5]) for c in quotes.calls] == [
            (0, cutoff, exposure_of(1, False, 0)), (1, cutoff, exposure_of(0, True, 1))]
        placed[run] = tuple(quotes(s, cutoff, 'orb_mnq_v7') for s in sessions)
        assert [c[6].prefix.close for c in quotes.calls] == list(placed[run])
        assert [s.fills for s in result.sessions] == [2, 0]
        assert [s.pnl for s in result.sessions] == pytest.approx([-1.82, 0])
        source_bars = [dict(pb.bars)['orb_mnq_v7'] for s in sessions for pb in s.bars]
        assert adapters['orb_mnq_v7'].bars == source_bars      # original bars once; no segments
        assert all(len(a.bars) == 8 for a in adapters.values())
    assert placed == {'R1': (90, 100), 'R2': (115, 100)}
