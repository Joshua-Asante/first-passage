from datetime import datetime, timedelta, timezone

import pytest

from c1_rail.book_sizing_context import BookSession
from c1_rail.book_schedule import ScheduleError, SchedulePhase, classify_schedule


OPEN = datetime(2026, 9, 15, 13, 30, tzinfo=timezone.utc)


def session():
    return BookSession(
        "session", "prior", OPEN, OPEN + timedelta(hours=6),
        OPEN + timedelta(hours=7), "c" * 64,
        OPEN + timedelta(hours=6, minutes=15),
        OPEN + timedelta(hours=6, minutes=30),
    )


@pytest.mark.parametrize(("offset", "expected"), [
    (timedelta(seconds=-1), SchedulePhase.CLOSED),
    (timedelta(), SchedulePhase.RISK_ADD),
    (timedelta(hours=6), SchedulePhase.CUTOFF),
    (timedelta(hours=6, minutes=15), SchedulePhase.FLATTEN),
    (timedelta(hours=6, minutes=30), SchedulePhase.DEADLINE),
    (timedelta(hours=7), SchedulePhase.DEADLINE),
])
def test_schedule_boundaries(offset, expected):
    assert classify_schedule(session(), OPEN + offset) is expected


def test_schedule_requires_aware_clock_and_complete_ordered_boundaries():
    with pytest.raises(ScheduleError, match="aware"):
        classify_schedule(session(), OPEN.replace(tzinfo=None))
    with pytest.raises(ScheduleError, match="complete"):
        classify_schedule(
            BookSession("s", "p", OPEN, OPEN + timedelta(hours=1),
                        OPEN + timedelta(hours=2), "c" * 64), OPEN)
    with pytest.raises(ScheduleError, match="ordered"):
        classify_schedule(
            BookSession("s", "p", OPEN, OPEN + timedelta(hours=1),
                        OPEN + timedelta(hours=2), "c" * 64,
                        OPEN + timedelta(minutes=30), OPEN + timedelta(hours=1, minutes=30)),
            OPEN,
        )


def test_flatten_phase_does_not_invent_a_bar_price():
    instant = OPEN + timedelta(hours=6, minutes=15)
    decision = classify_schedule(session(), instant)
    assert decision is SchedulePhase.FLATTEN
    assert not hasattr(decision, "price")
