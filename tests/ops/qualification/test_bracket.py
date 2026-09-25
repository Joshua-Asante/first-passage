"""Path-position bracket convention (ratified 2026-09-23); synthetic adapters only."""
import random
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest

from c1_signal_daemon.book_protocol import OrderIntent, Side
from c1_signal_daemon.feed import Bar
from c1_rail.qualification.bracket import (
    BracketScheduleQuotes, BracketVerdict, BracketRun, placement, run_bracket, vertex_split,
)
from c1_rail.qualification.model import PathOutcome, SessionSchedule
from c1_rail.qualification.replay import BookReplay, ReplayNeedsContext, accepted_path
from mc.simulation import EvaluationState

from test_replay import engine, entry, first_entry, path_session

T0 = datetime(2026, 1, 5, 20, 45, tzinfo=timezone.utc)
INSTANT = T0 + timedelta(minutes=10)
STATE = EvaluationState(100000, 100000, 100000, 0, 0)


def _validate(bar, index):
    """Run one vertex split through the engine's own split validator."""
    prefix, suffix = vertex_split(bar, index, INSTANT)
    class Stub:
        split_bar = staticmethod(lambda *args: (prefix, suffix))
        def __call__(self, *args):
            return prefix.close
    pb = SimpleNamespace(source_bar_time=bar.ts)
    left, right = BookReplay._split(SimpleNamespace(schedule_quotes=Stub()), None, pb, {'leg': bar}, INSTANT)
    assert (left['leg'], right['leg']) == (prefix, suffix)
    assert prefix.close == accepted_path(bar)[index]


def test_every_vertex_split_passes_the_engine_validator_unchanged():
    rng = random.Random(20260923)
    bars = [Bar(T0, 100, 120, 90, 110, 7), Bar(T0, 100, 110, 90, 95, 1),   # H-O = O-L tie
            Bar(T0, 100, 100, 90, 100, 1), Bar(T0, 100, 110, 100, 100, 1),  # flat open, flat close
            Bar(T0, 100, 100, 100, 100, 1)]
    for _ in range(5000):
        o, c = rng.randint(50, 150), rng.randint(50, 150)
        bars.append(Bar(T0, o, max(o, c) + rng.randint(0, 20), min(o, c) - rng.randint(0, 20), c,
                        rng.randint(0, 9)))
    for bar in bars:
        for index in range(4):
            _validate(bar, index)


@pytest.mark.parametrize('run,position,expected', [
    ('R1', 1, ('adverse', 1)), ('R2', 1, ('favourable', 2)),
    ('R1', -3, ('adverse', 2)), ('R2', -3, ('favourable', 1)),
    ('R1', 0, ('fill', 3)), ('R2', 0, ('cancel', 0)),
])
def test_two_run_table(run, position, expected):
    path = accepted_path(Bar(T0, 100, 120, 90, 110))
    assert path == [100, 90, 120, 110]  # the nearer extreme first
    assert placement(run, position, path) == expected


def test_adverse_extreme_at_the_open_places_at_the_open_vertex():
    path = accepted_path(Bar(T0, 100, 110, 100, 105))
    assert placement('R1', 1, path) == ('adverse', 0)


def test_placement_refuses_without_observed_exposure():
    quotes = BracketScheduleQuotes('R1')
    session = SimpleNamespace(occurrence=0, source=SimpleNamespace(source_session_date=T0.date()))
    pb = SimpleNamespace(source_bar_time=T0, bars=(('leg', Bar(T0, 100, 110, 90, 100)),))
    with pytest.raises(ReplayNeedsContext, match='exposure'):
        quotes.split_bar(session, pb, INSTANT, 'leg')
    quotes.observe_exposure(session, INSTANT - timedelta(minutes=1), {'leg': 1})
    with pytest.raises(ReplayNeedsContext, match='exposure'):
        quotes.split_bar(session, pb, INSTANT, 'leg')


def test_interval_split_places_on_the_remaining_path():
    quotes = BracketScheduleQuotes('R1')
    session = SimpleNamespace(occurrence=0, source=SimpleNamespace(source_session_date=T0.date()))
    remaining = Bar(T0 + timedelta(minutes=5), 110, 110, 90, 105)  # 110 -> 90 -> 105
    quotes.observe_exposure(session, INSTANT, {'leg': 1})
    prefix, suffix = quotes.split_interval(session, None, remaining, INSTANT, 'leg')
    assert (prefix.close, suffix.open, suffix.close) == (90, 90, 105)
    assert quotes(session, INSTANT, 'leg') == 90


def flatten_session(side_bar):
    return path_session(start_hour=20, prices=[(100, 100, 100, 100)] * 3 + [side_bar])


# Path 100 -> 110 -> 90 -> 105. A short's favourable vertex (90) is reached only
# after the high, so its R2 lifetime low still carries the high.
@pytest.mark.parametrize('side,bar,r1,r2,r2_low', [
    (Side.BUY, (100, 110, 90, 105), -10, 10, 0),
    (Side.SELL, (100, 110, 90, 105), -10, 10, -10),
])
def test_held_position_flattens_at_adverse_then_favourable_vertex(side, bar, r1, r2, r2_low):
    def emit(a, b):
        return entry(a, b, side=side) if len(a.bars) == 1 else []
    leg = 'aegis_6j' if side is Side.SELL else 'orb_mnq_v7'
    pnl, low, placed = {}, {}, {}
    for run in ('R1', 'R2'):
        quotes = BracketScheduleQuotes(run)
        replay, adapters = engine({leg: emit}, quotes=quotes)
        record = replay.run((flatten_session(bar),)).sessions[0]
        pnl[run], low[run] = record.pnl, record.intraday_low
        placed[run] = quotes.placements
        flats = [e.fill for e in adapters[leg].feedback if e.fill and e.fill.kind == 'flat']
        assert flats[0].price == placed[run][0].price
        assert all(len(a.bars) == 4 for a in adapters.values())
    qty = 8 if side is Side.SELL else 1
    assert (pnl['R1'], pnl['R2']) == (r1 * qty, r2 * qty)
    assert (low['R1'], low['R2']) == (r1 * qty, r2_low * qty)
    assert [(p.run, p.rule, p.position) for p in placed['R1'] + placed['R2']] == [
        ('R1', 'adverse', qty if side is Side.BUY else -qty),
        ('R2', 'favourable', qty if side is Side.BUY else -qty)]


def test_pending_only_leg_fills_in_r1_and_cancels_in_r2():
    session = path_session(start_hour=20, prices=[(100, 100, 100, 100), (100, 110, 90, 100),
                                                  (100, 100, 100, 100), (100, 100, 100, 100)])
    cutoff = session.source.bars[1].source_bar_time + timedelta(minutes=5)
    session = replace(session, source=replace(session.source, schedule=SessionSchedule(
        cutoff, cutoff + timedelta(minutes=10), cutoff + timedelta(minutes=15))))
    def resting(a, b):
        return [OrderIntent('pending', a.leg_id, 'entry', Side.BUY, 1, 'stop', 105)] if len(a.bars) == 1 else []
    outcome = {}
    for run in ('R1', 'R2'):
        quotes = BracketScheduleQuotes(run)
        replay, adapters = engine({'orb_mnq_v7': resting}, quotes=quotes)
        record = replay.run((session,)).sessions[0]
        outcome[run] = (record.fills, record.pnl, [(p.rule, p.price) for p in quotes.placements])
        assert record.end_edge.is_flat
    assert outcome['R1'] == (2, -5, [('fill', 100)])     # stop filled at 105, flattened at 100
    assert outcome['R2'] == (0, 0, [('cancel', 100)])    # cancelled at the open


def _outcome(status):
    return PathOutcome(status, 1 if status == 'PASS' else None,
                       None if status == 'PASS' else 'synthetic', ())


def test_verdict_takes_only_agreement_and_counts_the_rest_undetermined():
    def build(quotes):
        return engine({'orb_mnq_v7': first_entry}, quotes=quotes)[0]
    path = (flatten_session((100, 110, 90, 105)),)
    by_sign = lambda result, initial_state: _outcome('PASS' if result.sessions[0].pnl > 0 else 'FAILURE')
    split = run_bracket(build, path, initial_state=STATE, evaluate=by_sign)
    assert split.status == 'UNDETERMINED'
    assert [(r.run, r.outcome.status) for r in split.runs] == [('R1', 'FAILURE'), ('R2', 'PASS')]
    agreed = run_bracket(build, path, initial_state=STATE)  # real kernel: neither passes nor busts
    assert agreed.status == 'UNRESOLVED'
    assert all(r.placements for r in agreed.runs)


def test_verdict_rejects_folded_status_and_missing_run_labels():
    runs = (BracketRun('R1', _outcome('FAILURE'), ()), BracketRun('R2', _outcome('PASS'), ()))
    for status in ('PASS', 'FAILURE'):
        with pytest.raises(ValueError, match='agreement'):
            BracketVerdict(status, runs)
    with pytest.raises(ValueError, match='R1 then R2'):
        BracketVerdict('UNDETERMINED', runs[::-1])


def test_run_bracket_refuses_a_replay_not_wired_to_its_placements():
    def build(quotes):
        return engine({'orb_mnq_v7': first_entry})[0]
    with pytest.raises(ValueError, match='placements'):
        run_bracket(build, (flatten_session((100, 110, 90, 105)),), initial_state=STATE)

@pytest.mark.parametrize('side,leg,open_price,trigger', [
    (Side.BUY, 'orb_mnq_v7', 110, 105),
    (Side.SELL, 'aegis_6j', 90, 95),
])
@pytest.mark.parametrize('order_type', ['stop', 'market'])
def test_r2_pending_only_cutoff_cancels_before_gap_open(side, leg, open_price, trigger, order_type):
    from c1_rail.qualification.replay import Instrument
    from c1_rail.book_policy import BOOK_LEGS
    session = path_session(start_hour=20, prices=[(100, 100, 100, 100),
        (open_price, 115, 85, 100), (100, 100, 100, 100), (100, 100, 100, 100)])
    cutoff = session.source.bars[1].source_bar_time + timedelta(minutes=5)
    session = replace(session, source=replace(session.source, schedule=SessionSchedule(
        cutoff, cutoff + timedelta(minutes=10), cutoff + timedelta(minutes=15))))
    def resting(adapter, bar):
        return [OrderIntent('pending', adapter.leg_id, 'entry', side, 1,
                            order_type, trigger if order_type == 'stop' else None)] if len(adapter.bars) == 1 else []
    instruments = {s.leg_id: Instrument(1, 1, 2, 0) for s in BOOK_LEGS}
    results = {}
    for run in ('R1', 'R2'):
        quotes = BracketScheduleQuotes(run)
        replay, adapters = engine({leg: resting}, quotes=quotes, instruments=instruments)
        record = replay.run((session,)).sessions[0]
        results[run] = record
        assert record.end_edge.is_flat
        assert all(len(a.bars) == 4 for a in adapters.values())
        if run == 'R2':
            assert any(e.event == 'cancel' and e.order_id == 'pending' for e in adapters[leg].feedback)
            assert not any(e.fill for e in adapters[leg].feedback)
    assert results['R1'].fills == 2
    assert results['R2'].fills == 0
    assert results['R2'].pnl == 0
    assert results['R2'].intraday_low == 0


def test_r2_pending_only_leg_cancels_while_another_leg_keeps_its_prefix():
    session = path_session(start_hour=20, prices=[(100, 100, 100, 100),
        (110, 115, 85, 100), (100, 100, 100, 100), (100, 100, 100, 100)])
    cutoff = session.source.bars[1].source_bar_time + timedelta(minutes=5)
    session = replace(session, source=replace(session.source, schedule=SessionSchedule(
        cutoff, cutoff + timedelta(minutes=10), cutoff + timedelta(minutes=15))))
    def resting(adapter, bar):
        return [OrderIntent('pending', adapter.leg_id, 'entry', Side.BUY, 1, 'stop', 105)] if len(adapter.bars) == 1 else []
    quotes = BracketScheduleQuotes('R2')
    replay, adapters = engine({'orb_mnq_v7': resting, 'vanguard_mgc': first_entry}, quotes=quotes)
    result = replay.run((session,))
    assert not any(e.fill for e in adapters['orb_mnq_v7'].feedback)
    assert result.sessions[0].end_edge.is_flat
    assert result.sessions[0].fills == 2  # the held Vanguard entry and scheduled flatten
    assert sorted((p.leg_id, p.rule) for p in quotes.placements if p.instant == cutoff) == [
        ('orb_mnq_v7', 'cancel'), ('vanguard_mgc', 'favourable')]


def test_r2_held_position_with_pending_add_keeps_prefix_fill():
    session = path_session(start_hour=20, prices=[(100, 100, 100, 100),
        (100, 100, 100, 100), (110, 115, 85, 100), (100, 100, 100, 100)])
    cutoff = session.source.bars[2].source_bar_time + timedelta(minutes=5)
    session = replace(session, source=replace(session.source, schedule=SessionSchedule(
        cutoff, cutoff + timedelta(minutes=10), cutoff + timedelta(minutes=15))))
    def emit(adapter, bar):
        if len(adapter.bars) == 1:
            return entry(adapter, bar)
        if len(adapter.bars) == 2:
            return [OrderIntent('add', adapter.leg_id, 'add', Side.BUY, 1, 'stop', 105)]
        return []
    quotes = BracketScheduleQuotes('R2')
    replay, adapters = engine({'orb_mnq_v7': emit}, quotes=quotes)
    result = replay.run((session,))
    adds = [e.fill for e in adapters['orb_mnq_v7'].feedback if e.fill and e.fill.kind == 'add']
    assert len(adds) == 1 and adds[0].price == 110
    assert next(p for p in quotes.placements if p.instant == cutoff).rule == 'favourable'
    assert result.sessions[0].end_edge.is_flat
