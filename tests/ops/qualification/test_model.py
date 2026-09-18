from datetime import datetime, date, timezone
import pytest
from c1_signal_daemon.feed import Bar
from c1_rail.qualification.model import (
    LEG_IDS, EdgeState, SourceBar, SessionSchedule, PathOutcome, ReplayResult,
)


def test_edge_requires_gross_positions_orders_and_reservations_for_all_legs():
    zero = tuple((leg, 0) for leg in LEG_IDS)
    assert EdgeState(zero, zero, zero).is_flat
    pending = tuple((leg, int(leg == LEG_IDS[-1])) for leg in LEG_IDS)
    assert not EdgeState(zero, pending, zero).is_flat
    with pytest.raises(ValueError):
        EdgeState(zero[:-1], zero, zero)
    with pytest.raises(ValueError):
        EdgeState(tuple((leg, -1) for leg in LEG_IDS), zero, zero)


def test_source_bar_refuses_mutated_time_or_invalid_ohlc():
    ts = datetime(2020, 1, 1, tzinfo=timezone.utc)
    with pytest.raises(ValueError):
        SourceBar(ts, ((LEG_IDS[0], Bar(ts, 100, 90, 80, 100)),))
    with pytest.raises(ValueError):
        SourceBar(ts.replace(tzinfo=None), ())


def test_session_schedule_and_outcome_invariants():
    ts = datetime(2020, 1, 1, tzinfo=timezone.utc)
    with pytest.raises(ValueError):
        SessionSchedule(ts, ts, ts)
    with pytest.raises(ValueError):
        PathOutcome('PASS', None, None, ())
    with pytest.raises(ValueError):
        PathOutcome('FAILURE', 2, 'deadline', ())
    assert PathOutcome('PASS', 0, None, ()).sessions_to_pass == 0


def test_replay_result_must_not_admit_mutable_validated_records():
    with pytest.raises(ValueError):
        ReplayResult([], ())
    with pytest.raises(ValueError):
        ReplayResult((), [])
