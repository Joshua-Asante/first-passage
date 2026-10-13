"""Card A P1-P7: public synthetic P0 replay, halt parity and preservation."""
import hashlib
import json
from dataclasses import asdict, replace

import pytest

from c1_rail import book_policy as bp
from c1_rail import personal_drawdown_halt as live
from c1_rail.qualification import replay as replay_module
from c1_rail.qualification.replay import BookReplay, Instrument, ReplayNeedsContext
from c1_signal_daemon.book_protocol import Side, OrderIntent, FillTiming, Mode
from c1_signal_daemon.tv_broker_emulator import TVBrokerEmulator
from mc.simulation import EvaluationState
from test_replay import Adapter, engine, path_session, first_entry, entry, schedule_split
from c1_signal_daemon.feed import Bar


def personal():
    assert hasattr(bp, "PersonalP0Policy"), "P0 policy is not implemented"
    return bp.PersonalP0Policy()


def personal_engine(emit=None, *, equity=100000, peak=100000, price=100,
                    pointvalue=1, mintick=.000001, slip=0, fee=0,
                    broker_factory=TVBrokerEmulator):
    adapters = {s.leg_id: Adapter(s.leg_id, emit if s.leg_id == "orb_mnq_v7" else None)
                for s in bp.BOOK_LEGS}
    instruments = {s.leg_id: Instrument(mintick, pointvalue, slip, fee) for s in bp.BOOK_LEGS}
    class FlatTailQuotes:
        def __call__(self, *args):
            return price

        def split_bar(self, session, pb, instant, k, *, exposure):
            original = dict(pb.bars)[k]
            if not original.open == original.high == original.low == original.close == price:
                raise ReplayNeedsContext("synthetic fixture lacks split OHLC")
            return schedule_split(original, Bar(instant, price, price, price, price))
    replay = BookReplay(adapters, instruments, policy=personal(),
        initial_state=EvaluationState(original_basis=peak, current_equity=equity,
            historical_eod_peak=peak, prior_trade_days=1, prior_max_day_profit=0),
        sizing_inputs=lambda k, a, p: dict(lifecycle_tier="AUTHORIZED", **(
            dict(risk_dollars=700, per_contract_risk=35, cap_alloc=80) if k == "dj30_mym_p250"
            else dict(normal_base=1) if k == "vanguard_mgc" else {})),
        schedule_quotes=FlatTailQuotes(),
        broker_factory=broker_factory)
    return replay, adapters


def latches(result):
    return [e for e in result.events if e.kind == "personal_halt_latched"]


@pytest.mark.parametrize("equity,latched", [
    (85000, True), (85001, False), (84999, True),
    (85000.04, True), (85000.06, False),
])
def test_threshold_and_rounding_match_live_halt(equity, latched, tmp_path):
    replay, _ = personal_engine(equity=equity)
    result = replay.run((path_session(),))
    halt = live.PersonalDrawdownHalt.initialize(
        tmp_path / "synthetic-halt.json", account="synthetic",
        portfolio_id="synthetic", starting_equity=100000)
    state = halt.observe(equity)
    assert bool(latches(result)) is latched
    assert (state["state"] == "HALTED") is latched
    if latched:
        record = json.loads(latches(result)[0].detail)
        assert record == {"peak": 100000, "equity": equity}
        assert latches(result)[0].path_time == result.events[1].path_time


def test_p0_calls_the_live_pure_predicate():
    assert hasattr(live, "drawdown_breached"), "pure live predicate is not extracted"
    assert replay_module.drawdown_breached is live.drawdown_breached
    assert live.drawdown_breached(100000, 85000.04, tier="Personal_Tradovate")
    assert not live.drawdown_breached(100000, 85000.06, tier="Personal_Tradovate")


@pytest.mark.parametrize("equity", [100000, 99900, 98500, 85000, 1])
def test_p0_never_constructs_old_clock_or_enters_protected(equity, monkeypatch):
    personal()
    def forbidden(*args, **kwargs):
        raise AssertionError("P0 constructed the Tradeify clock")
    monkeypatch.setattr(replay_module, "BookProtectionClock", forbidden)
    replay, adapters = personal_engine(equity=equity)
    result = replay.run((path_session(), path_session(1)))
    assert [e.detail for e in result.events if e.kind == "session_mode"] == ["normal", "normal"]
    assert all(a.modes == [Mode.NORMAL, Mode.NORMAL] for a in adapters.values())


@pytest.mark.parametrize("closes,latched,peak", [
    ([100, 120, 102, 110], True, 120000),
    ([100, 99, 120, 119], False, 120000),
])
def test_running_peak_and_recovery(closes, latched, peak):
    prices = [(p, p, p, p) for p in closes]
    replay, _ = personal_engine(first_entry, pointvalue=1000, price=closes[-1])
    result = replay.run((path_session(prices=prices),))
    assert bool(latches(result)) is latched
    if latched:
        assert json.loads(latches(result)[0].detail) == {"peak": peak, "equity": 102000}


def test_latch_blocks_entry_and_add_flattens_next_open_with_costs_and_leaves_zero_days():
    def emit(a, b):
        return [OrderIntent(f"entry-{len(a.bars)}", a.leg_id, "entry", Side.BUY, 1,
                            timing=FillTiming.THIS_CLOSE),
                OrderIntent(f"add-{len(a.bars)}", a.leg_id, "add", Side.BUY, 1,
                            timing=FillTiming.THIS_CLOSE)]
    replay, adapters = personal_engine(emit, pointvalue=1000, mintick=1, slip=1, fee=3, price=75)
    session = path_session(prices=[(100,100,100,100), (80,80,80,80), (75,75,75,75)])
    result = replay.run((session, path_session(1, prices=[(75,75,75,75)] * 3)))
    latch, = latches(result)
    assert latch.path_time == session.bars[1].path_time + replay_module.timedelta(minutes=15)
    forced = [e for e in result.events if e.kind == "fill" and json.loads(e.detail)["reason"] == "personal_halt"]
    assert len(forced) == 1
    fill = json.loads(forced[0].detail)
    assert fill["price"] == 74 and fill["commission"] == 3
    assert fill["source_time"] == session.bars[2].source_bar_time.isoformat()
    assert forced[0].path_time == session.bars[2].path_time
    after = [e for e in result.events if e.kind == "fill" and e.path_time >= latch.path_time]
    assert all(json.loads(e.detail)["kind"] not in ("entry", "add") for e in after)
    refused = [e for e in adapters["orb_mnq_v7"].feedback if e.event == "reject" and e.detail == "personal_halt"]
    assert {e.order_id.split("-")[0] for e in refused} == {"entry", "add"}
    assert result.sessions[1].pnl == 0 and result.sessions[1].fills == 0
    assert result.sessions[0].end_edge.is_flat
    assert any(e.kind == "personal_halt_flat_confirmed" for e in result.events)


@pytest.mark.parametrize("failure", ["flat", "working"])
def test_unconfirmed_flat_or_working_order_leaves_flatten_owed(failure):
    class UncertainBroker(TVBrokerEmulator):
        uncertain = False

        def _close_scope(self, intent, price, ts, *, slip):
            if intent.reason == "personal_halt":
                self.uncertain = True
                if failure == "flat":
                    return []
            return super()._close_scope(intent, price, ts, slip=slip)

        def pending_order_ids(self):
            return super().pending_order_ids() + (["unconfirmed-order"] if self.uncertain and failure == "working" else [])

    replay, _ = personal_engine(first_entry, pointvalue=1000, price=75, broker_factory=UncertainBroker)
    session = path_session(prices=[(100,100,100,100), (80,80,80,80), (75,75,75,75)])
    with pytest.raises(ReplayNeedsContext, match="personal.*flatten"):
        replay.run((session,))
    assert replay.personal_halted and replay.personal_flatten_owed
    assert not any(e.kind == "personal_halt_flat_confirmed" for e in replay.events)


def test_replay_uses_personal_cap_not_tradeify(monkeypatch):
    policy = personal()
    monkeypatch.setitem(bp.FIRM_RULES[policy.tier], "micro_contract_cap", 1)
    def emit(a, b):
        return entry(a,b) if len(a.bars) <= 2 else []
    replay, adapters = personal_engine(emit)
    # Unique IDs avoid the independent working-order duplicate check.
    adapters["orb_mnq_v7"].emit = lambda a,b: [
        replace(x, order_id=f"entry-{len(a.bars)}") for x in emit(a,b)]
    result = replay.run((path_session(prices=[(100,100,100,100)] * 3),))
    fills = [json.loads(e.detail) for e in result.events if e.kind == "fill"]
    assert sum(f["qty"] for f in fills if f["kind"] == "entry") == 1
    assert any("cap" in e.detail for e in result.events if e.kind == "refused")


@pytest.mark.parametrize("scenario,expected", [
    (0, "9ef5fef4fe3bbaffa5b7e58f2e537d7ed5f7c1780ea3a847ab36dc2f07179fb0"),
    (1, "e4af8a94f81ca53b943072e40ad39ffb7f3cf36756cdf8f770ce256066538c9b"),
    (2, "f7da10abe4305ac0269c53757c03800b4487fcb31c159ca6e837b7f998e4c03d"),
    (3, "0e4cff0f2aebe02bc701186041e5f5a1241aafaeda1da9629defec6d22691c08"),
])
def test_tradeify_outputs_byte_equal_cut_c0f459a(scenario, expected):
    emitters, state = {}, None
    if scenario in (1,3):
        emitters = {"orb_mnq_v7": first_entry}
    if scenario == 2:
        emitters = {s.leg_id: (lambda a,b: entry(a,b,side=Side.SELL if a.leg_id=="aegis_6j" else Side.BUY)
                              if len(a.bars)==1 else []) for s in bp.BOOK_LEGS}
    if scenario == 3:
        state = EvaluationState(original_basis=100000, current_equity=98000,
            historical_eod_peak=100000, prior_trade_days=1, prior_max_day_profit=0)
    replay, adapters = engine(emitters, state=state)
    result = replay.run((path_session(), path_session(1)))
    raw = json.dumps({"result": asdict(result),
        "feedback": {k: [asdict(e) for e in a.feedback] for k,a in adapters.items()},
        "clock": replay.clock.history}, default=str, sort_keys=True, separators=(",",":")).encode()
    assert hashlib.sha256(raw).hexdigest() == expected


@pytest.mark.parametrize("gap_minutes", [0, 30])
def test_late_personal_flat_cannot_retroactively_clear_schedule_deadline(gap_minutes):
    from datetime import timedelta
    from c1_rail.qualification.model import SessionSchedule, SourceBar
    from c1_rail.qualification.replay import ReplayDeadlineFailure

    class MissedScheduledFlat(TVBrokerEmulator):
        def _close_scope(self, intent, price, ts, *, slip):
            if intent.reason == "scheduled_flatten":
                return []
            return super()._close_scope(intent, price, ts, slip=slip)

    replay, _ = personal_engine(first_entry, pointvalue=1000, price=80,
                                broker_factory=MissedScheduledFlat)
    session = path_session(prices=[(100,100,100,100), (100,100,100,100),
                                   (80,80,80,80), (75,75,75,75)])
    origin = session.bars[0].source_bar_time
    delay = timedelta(minutes=gap_minutes)
    bars = tuple(replace(bar, path_time=bar.path_time + delay,
        source_bar_time=bar.source_bar_time + delay,
        source_time_et=bar.source_time_et + delay,
        bars=tuple((k, replace(value, ts=value.ts + delay)) for k, value in bar.bars))
        if i >= 3 else bar for i, bar in enumerate(session.bars))
    source = replace(session.source,
        bars=tuple(SourceBar(bar.source_bar_time, bar.bars) for bar in bars),
        schedule=SessionSchedule(origin + timedelta(minutes=30),
                                 origin + timedelta(minutes=40),
                                 origin + timedelta(minutes=45)))
    session = replace(session, bars=bars, source=source)
    with pytest.raises(ReplayDeadlineFailure):
        replay.run((session,))
    assert replay.personal_halted and replay.personal_flatten_owed
    assert not any(e.kind == "personal_halt_flat_confirmed" for e in replay.events)


def test_halt_then_same_bar_close_confirms_flat_before_bar_equity():
    def emit(a, b):
        if len(a.bars) == 1:
            return first_entry(a, b)
        if len(a.bars) == 2:
            return [OrderIntent("same-bar-close", a.leg_id, "flat", Side.SELL, None,
                                timing=FillTiming.THIS_CLOSE, reason="strategy_close")]
        return []

    replay, _ = personal_engine(emit, pointvalue=1000, price=75)
    session = path_session(prices=[(100,100,100,100), (80,80,80,80), (75,75,75,75)])
    result = replay.run((session,))
    latch, = latches(result)
    confirmed, = [e for e in result.events if e.kind == "personal_halt_flat_confirmed"]
    close, = [e for e in result.events if e.kind == "fill"
              and json.loads(e.detail)["reason"] == "strategy_close"]
    assert latch.path_time == close.path_time == confirmed.path_time
    latch_index = result.events.index(latch)
    close_equity_index = next(i for i, e in enumerate(result.events)
                              if i > latch_index and e.kind == "bar_equity")
    assert latch_index < result.events.index(close) < result.events.index(confirmed) < close_equity_index
    assert replay.personal_halted and not replay.personal_flatten_owed
    assert result.sessions[0].end_edge.is_flat
    assert not any(e.kind == "fill" and json.loads(e.detail)["reason"] == "personal_halt"
                   for e in result.events)
