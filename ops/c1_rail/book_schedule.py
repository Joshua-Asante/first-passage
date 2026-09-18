"""Pure schedule classification shared by runtime and qualification replay.

This module classifies time only.  In particular it never supplies an execution
price: callers replaying a scheduled action between bars must bind explicit
source-instant price evidence.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum


class ScheduleError(ValueError):
    """The bound session schedule is absent or internally inconsistent."""


class SchedulePhase(str, Enum):
    CLOSED = "CLOSED"
    RISK_ADD = "RISK_ADD"
    CUTOFF = "CUTOFF"
    FLATTEN = "FLATTEN"
    DEADLINE = "DEADLINE"


def classify_schedule(session, now: datetime) -> SchedulePhase:
    """Return the phase at ``now`` using the exact bound account-session clock."""
    instants = (
        session.opens_at,
        session.risk_add_cutoff,
        session.flatten_start,
        session.own_flat_deadline,
        session.closes_at,
    )
    if not isinstance(now, datetime) or now.utcoffset() is None:
        raise ScheduleError("schedule clock must be timezone-aware")
    if any(value is None for value in instants):
        raise ScheduleError("schedule boundaries must be complete")
    if any(not isinstance(value, datetime) or value.utcoffset() is None for value in instants):
        raise ScheduleError("schedule boundaries must be timezone-aware")
    if not all(left < right for left, right in zip(instants, instants[1:])):
        raise ScheduleError("schedule boundaries must be strictly ordered")
    opens_at, cutoff, flatten, deadline, closes_at = instants
    if now < opens_at:
        return SchedulePhase.CLOSED
    if now < cutoff:
        return SchedulePhase.RISK_ADD
    if now < flatten:
        return SchedulePhase.CUTOFF
    if now < deadline:
        return SchedulePhase.FLATTEN
    # Deadline enforcement remains authoritative after the venue close.  A
    # late scheduler tick must not turn unresolved obligations back into a
    # harmless generic CLOSED state.
    return SchedulePhase.DEADLINE


def classify_execution_phase(*, cutoff: datetime, flatten_start: datetime,
                             own_flat_deadline: datetime, now: datetime) -> SchedulePhase:
    """Classify the three evidence-bound execution instants.

    Qualification replay can call this without inventing venue open/close
    metadata.  Source coverage and price evidence remain separate obligations.
    """
    instants = (cutoff, flatten_start, own_flat_deadline)
    if (not isinstance(now, datetime) or now.utcoffset() is None
            or any(not isinstance(value, datetime) or value.utcoffset() is None
                   for value in instants)):
        raise ScheduleError("execution schedule clock must be timezone-aware")
    if not all(left < right for left, right in zip(instants, instants[1:])):
        raise ScheduleError("execution schedule boundaries must be strictly ordered")
    if now < cutoff:
        return SchedulePhase.RISK_ADD
    if now < flatten_start:
        return SchedulePhase.CUTOFF
    if now < own_flat_deadline:
        return SchedulePhase.FLATTEN
    return SchedulePhase.DEADLINE
