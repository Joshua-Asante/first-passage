"""Source-calendar lookup, separate from path sessions and deployment permission."""
from dataclasses import dataclass
from datetime import date
from enum import Enum
from .model import ET, SessionSchedule
from c1_rail.book_schedule import classify_execution_phase


class ClockCoverageError(ValueError):
    pass


class SourceDayStatus(str,Enum):
    EXCHANGE_CLOSED='exchange_closed'
    POLICY_DENIED='policy_denied'
    UNKNOWN='unknown'


@dataclass(frozen=True)
class SourceDayDisposition:
    status: SourceDayStatus
    reason: str

    def __post_init__(self):
        if type(self.status) is not SourceDayStatus or type(self.reason) is not str or not self.reason.strip():
            raise ValueError('typed source disposition and explicit reason required')


@dataclass(frozen=True)
class AccountClock:
    schedules: tuple[tuple[date, SessionSchedule | SourceDayDisposition], ...]
    coverage_start: date
    coverage_end: date
    source_evidence_sha256: str

    def __post_init__(self):
        if type(self.schedules) is not tuple or not self.schedules or any(type(row) is not tuple or len(row)!=2 for row in self.schedules):
            raise ValueError('immutable explicit source schedule rows required')
        digest=self.source_evidence_sha256
        if type(digest) is not str or len(digest)!=64 or any(c not in '0123456789abcdef' for c in digest):
            raise ValueError('source evidence digest required')
        if self.coverage_start>self.coverage_end:
            raise ValueError('source coverage order')
        dates=tuple(day for day,_ in self.schedules)
        if tuple(sorted(set(dates)))!=dates:
            raise ValueError('unique ordered source dates required')
        for day,schedule in self.schedules:
            if not self.coverage_start<=day<=self.coverage_end:
                raise ValueError('source date outside coverage')
            if type(schedule) is not SessionSchedule and type(schedule) is not SourceDayDisposition:
                raise ValueError('typed source schedule or disposition required')
            if type(schedule) is SessionSchedule and schedule.own_flat_deadline.astimezone(ET).date()!=day:
                raise ValueError('schedule does not bind source date')

    def schedule_for(self, source_date):
        result=self.disposition_for(source_date)
        if type(result) is SourceDayDisposition:
            raise ClockCoverageError(f'{result.status.value}: {result.reason}')
        return result

    def disposition_for(self, source_date):
        if not self.coverage_start<=source_date<=self.coverage_end:
            raise ClockCoverageError('source calendar coverage exceeded')
        rows=dict(self.schedules)
        if source_date not in rows:
            raise ClockCoverageError('source calendar coverage missing for date')
        return rows[source_date]

    def phase_for(self,source_date,source_instant):
        from .panel import source_session_date
        if source_session_date(source_instant)!=source_date:
            raise ClockCoverageError('instant does not bind source session')
        schedule=self.schedule_for(source_date)
        return classify_execution_phase(cutoff=schedule.cutoff,
            flatten_start=schedule.flatten_start,own_flat_deadline=schedule.own_flat_deadline,
            now=source_instant)
