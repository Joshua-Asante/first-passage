"""Evidence-located schedule placements (DRAFT convention); synthetic bars only."""
import json
import random
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest

from c1_signal_daemon.feed import Bar
from c1_rail.qualification.model import ScheduleExposure, ScheduleSplit
from c1_rail.qualification.production_source import ScheduleExecutionBracket, parse_schedule_execution_evidence
from c1_rail.qualification.replay import BookReplay
from c1_rail.qualification.schedule_evidence import evidence_row, evidence_rows

T0 = datetime(2024, 1, 2, 20, 45, tzinfo=timezone.utc)      # 15:45 ET
INSTANT = T0 + timedelta(minutes=10)                          # 15:55 ET
LEG = 'orb_mnq_v7'


def _fives(ticks):
    """Three 5-minute bars and their M15 aggregate from one tick path (301 points per bar)."""
    fives = [Bar(T0 + timedelta(minutes=5 * i), *(lambda t: (t[0], max(t), min(t), t[-1]))(ticks[i * 300:(i + 1) * 300 + 1]), 1)
             for i in range(3)]
    return Bar(T0, fives[0].open, max(b.high for b in fives), min(b.low for b in fives), fives[-1].close, 3), fives


def _validate(original, row):
    """The row through the parser and the engine's own split validator, in both bracket runs."""
    evidence = parse_schedule_execution_evidence(json.dumps(
        {'schema': 'qualification-schedule-execution/v1', 'rows': [row]}).encode())
    session = SimpleNamespace(occurrence=0, bars=(), source=SimpleNamespace(source_session_date=T0.date()))
    pb = SimpleNamespace(source_bar_time=T0, bars=((LEG, original),))
    splits = []
    for run in ('R1', 'R2'):
        provider = ScheduleExecutionBracket(evidence).for_run(run)
        split = BookReplay._split(SimpleNamespace(schedule_quotes=provider), session, pb, {LEG: original}, INSTANT,
                                  {LEG: ScheduleExposure(1, False, 0)})[LEG]
        assert type(split) is ScheduleSplit and split.prefix_executes and provider._placed == {}
        splits.append(split)
    assert splits[0] == splits[1]
    return splits[0]


def test_located_rows_pass_the_engine_validator_and_resolve_both_runs_identically():
    rng = random.Random(20261008)
    reasons = {}
    for _ in range(400):
        ticks = [1000]
        for _ in range(900):
            ticks.append(ticks[-1] + rng.choice((-1, 1)))
        original, fives = _fives(ticks)
        row, reason = evidence_row(LEG, original, INSTANT, fives)
        reasons[reason] = reasons.get(reason, 0) + 1
        if row is not None:
            split = _validate(original, row)
            assert split.prefix.close == split.suffix.open == fives[2].open
    assert reasons.get(None, 0) > 160 and set(reasons) <= {None, 'REVERSED', 'SEGMENT', 'PATH'}


def test_segment_follows_the_extremes_reached_before_the_instant():
    original = Bar(T0, 100, 120, 90, 110, 3)                  # accepted path 100 -> 90 -> 120 -> 110
    def five(i, o, h, l, c):
        return Bar(T0 + timedelta(minutes=5 * i), o, h, l, c, 1)
    cases = [  # (fives, expected prefix values, price)
        ([five(0, 100, 101, 90, 95), five(1, 95, 99, 94, 97), five(2, 97, 120, 96, 110)], (100, 100, 90, 97), 97),
        ([five(0, 100, 101, 90, 95), five(1, 95, 120, 94, 115), five(2, 115, 116, 109, 110)], (100, 120, 90, 115), 115),
        ([five(0, 100, 101, 95, 97), five(1, 97, 99, 96, 96), five(2, 96, 120, 90, 110)], (100, 100, 96, 96), 96),
    ]
    for fives, (o, h, l, c), price in cases:
        row, reason = evidence_row(LEG, original, INSTANT, fives)
        assert reason is None and row['price'] == price
        assert (row['prefix']['open'], row['prefix']['high'], row['prefix']['low'], row['prefix']['close']) == (o, h, l, c)
        _validate(original, row)


def test_unlocatable_candidates_are_dropped_with_a_reason():
    original = Bar(T0, 100, 120, 90, 110, 3)
    def five(i, o, h, l, c, v=1):
        return Bar(T0 + timedelta(minutes=5 * i), o, h, l, c, v)
    reversed_ = [five(0, 100, 120, 99, 118), five(1, 118, 119, 100, 101), five(2, 101, 102, 90, 110)]
    off_segment = [five(0, 100, 101, 90, 95), five(1, 95, 120, 94, 100), five(2, 100, 111, 99, 110)]
    mismatch = [five(0, 100, 101, 90, 95), five(1, 95, 105, 94, 104), five(2, 104, 120, 103, 110, 2)]
    gap = [five(0, 100, 101, 90, 95), five(2, 104, 120, 103, 110)]
    own_path = [five(0, 100, 101, 90, 95), five(1, 95, 105, 94, 104), five(2, 104, 120, 103, 110)]  # 100->104 first
    rows, drops = evidence_rows([(LEG, original, INSTANT, f) for f in (reversed_, off_segment, own_path, mismatch, gap)])
    assert rows == [] and drops == {'REVERSED': 1, 'SEGMENT': 1, 'PATH': 1, 'AGGREGATE': 1, 'MISSING': 1}
    with pytest.raises(ValueError):
        evidence_row('nope', original, INSTANT, reversed_)
    with pytest.raises(ValueError):
        evidence_row(LEG, original, T0, reversed_)


def test_bracket_uses_only_located_rows_and_places_the_residual():
    from c1_rail.qualification.production_source import LOCATED_CONVENTION, _consumed_splits
    original = Bar(T0, 100, 120, 90, 110, 3)                  # accepted path 100 -> 90 -> 120 -> 110
    def five(i, o, h, l, c):
        return Bar(T0 + timedelta(minutes=5 * i), o, h, l, c, 1)
    row, _ = evidence_row(LEG, original, INSTANT, [five(0, 100, 101, 90, 95), five(1, 95, 99, 94, 97),
                                                  five(2, 97, 120, 96, 110)])
    assert row['convention'] == LOCATED_CONVENTION
    unmarked = {k: v for k, v in row.items() if k != 'convention'}
    session = SimpleNamespace(occurrence=0, bars=(), source=SimpleNamespace(source_session_date=T0.date()))
    pb = SimpleNamespace(source_bar_time=T0, bars=((LEG, original),))
    for rows, expected in (([row], {'R1': 97, 'R2': 97}), ([unmarked], {'R1': 90, 'R2': 120})):
        evidence = parse_schedule_execution_evidence(json.dumps(
            {'schema': 'qualification-schedule-execution/v1', 'rows': rows}).encode())
        for run, price in expected.items():
            provider = ScheduleExecutionBracket(evidence).for_run(run)
            split = provider.split_bar(session, pb, INSTANT, LEG, exposure=ScheduleExposure(1, False, 0))
            assert split.prefix.close == price and provider(session, INSTANT, LEG) == price
            assert len(_consumed_splits(provider)) == (0 if 'convention' in rows[0] else 1)
    for bad in ({**row, 'convention': 'other'}, {**row, 'prefix': None, 'suffix': None}):
        with pytest.raises(ValueError):
            parse_schedule_execution_evidence(json.dumps(
                {'schema': 'qualification-schedule-execution/v1', 'rows': [bad]}).encode())
