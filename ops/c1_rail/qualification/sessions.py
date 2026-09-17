"""Simulated session arrays and descriptive path-week activity."""
from datetime import timedelta
import numpy as np


def validate_sessions(records):
    if not records:
        raise ValueError('nonempty session path required')
    for a, b in zip(records, records[1:]):
        next_day = a.path_session_date + timedelta(days=1)
        while next_day.weekday() >= 5:
            next_day += timedelta(days=1)
        if b.occurrence != a.occurrence + 1 or b.path_session_date != next_day:
            raise ValueError('path sessions must be unique contiguous business occurrences')
    if any(row.path_session_date.weekday() >= 5 for row in records):
        raise ValueError('path calendar must be business sessions')


def session_arrays(records):
    validate_sessions(records)
    return np.asarray([[row.pnl] for row in records],dtype=float), np.asarray([row.intraday_low for row in records],dtype=float)


class WeekClock:
    """Counts observed Mon–Fri buckets; has no authority to fail an evaluation."""
    def count_idle(self, records):
        validate_sessions(records)
        weeks = {}
        for row in records:
            monday = row.path_session_date - timedelta(days=row.path_session_date.weekday())
            weeks[monday] = weeks.get(monday, 0) + row.fills
        return sum(count == 0 for count in weeks.values())
