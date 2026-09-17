from datetime import date,datetime,timedelta,timezone
import pytest
from c1_rail.qualification.model import SessionSchedule
from c1_rail.qualification.clock import AccountClock,ClockCoverageError,SourceDayStatus,SourceDayDisposition
from c1_rail.book_schedule import SchedulePhase


def test_source_clock_refuses_missing_closed_or_future_dates():
    day=date(2020,1,6);end=datetime(2020,1,6,21,tzinfo=timezone.utc)
    schedule=SessionSchedule(end-timedelta(minutes=15),end-timedelta(minutes=5),end)
    clock=AccountClock(((day,schedule),(date(2020,1,7),SourceDayDisposition(SourceDayStatus.EXCHANGE_CLOSED,'documented closure'))),day,date(2020,1,7),'a'*64)
    assert clock.schedule_for(day) is schedule
    assert clock.phase_for(day, schedule.cutoff) is SchedulePhase.CUTOFF
    assert clock.phase_for(day, schedule.flatten_start) is SchedulePhase.FLATTEN
    assert clock.phase_for(day, schedule.own_flat_deadline) is SchedulePhase.DEADLINE
    with pytest.raises(ClockCoverageError,match='bind source'):
        clock.phase_for(day, schedule.cutoff+timedelta(days=1))
    with pytest.raises(ClockCoverageError,match='closure'):
        clock.schedule_for(date(2020,1,7))
    with pytest.raises(ClockCoverageError,match='coverage'):
        clock.schedule_for(date(2020,1,8))


def test_no_source_schedule_substitution_or_implicit_calendar():
    day=date(2020,1,6);end=datetime(2020,1,7,21,tzinfo=timezone.utc)
    schedule=SessionSchedule(end-timedelta(minutes=15),end-timedelta(minutes=5),end)
    with pytest.raises(ValueError,match='source date'):
        AccountClock(((day,schedule),),day,day,'a'*64)
    with pytest.raises(ValueError):
        AccountClock((),day,day,'September deployment permissions')


@pytest.mark.parametrize('status',[SourceDayStatus.EXCHANGE_CLOSED,SourceDayStatus.POLICY_DENIED,SourceDayStatus.UNKNOWN])
def test_source_day_dispositions_keep_distinct_reasons(status):
    day=date(2020,1,6)
    disposition=SourceDayDisposition(status,'retained specific reason')
    clock=AccountClock(((day,disposition),),day,day,'a'*64)
    assert clock.disposition_for(day) is disposition
    with pytest.raises(ClockCoverageError,match=status.value):
        clock.schedule_for(day)


def test_untyped_none_cannot_claim_exchange_closure():
    day=date(2020,1,6)
    with pytest.raises(ValueError,match='typed'):
        AccountClock(((day,None),),day,day,'a'*64)
