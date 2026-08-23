"""Event-study harness (constraint/flow family first).

Windowed mean around event timestamps. First named prior is JPY month-end
flow; this module is calendar-agnostic so a month-end index can be injected
without a vendor CSV. Skip-if-missing is the CLI's job.
"""
from __future__ import annotations

from typing import Any, Iterable

import numpy as np
import pandas as pd


def month_end_events(index: pd.DatetimeIndex) -> pd.DatetimeIndex:
    """Business-month-end stamps that fall inside `index` (constraint/flow prior)."""
    if index.empty:
        return pd.DatetimeIndex([])
    month_ends = pd.bdate_range(index.min(), index.max(), freq="BME")
    return month_ends.intersection(index)


def event_study(
    returns: pd.Series,
    events: Iterable[pd.Timestamp],
    window: tuple[int, int] = (-1, 1),
) -> dict[str, Any]:
    """Mean return in [pre, post] around each event vs the non-event complement.

    Recovers a planted mean shift: event-window mean > complement mean when
    events carry a positive add.
    """
    if not isinstance(returns.index, pd.DatetimeIndex):
        raise TypeError("returns must be a DatetimeIndex series")
    series = returns.sort_index().astype(float).replace([np.inf, -np.inf], np.nan).dropna()
    if series.empty:
        raise ValueError("returns series is empty")
    pre, post = window
    if pre > post:
        raise ValueError("window must have pre <= post")

    idx = series.index
    event_locs: list[int] = []
    for raw in events:
        ts = pd.Timestamp(raw)
        if ts.tzinfo is not None:
            ts = ts.tz_convert(None) if ts.tz is not None else ts.tz_localize(None)
        if ts not in idx:
            # nearest-on-or-before for a calendar stamp that missed a holiday
            pos = idx.searchsorted(ts, side="right") - 1
            if pos < 0:
                continue
            ts = idx[pos]
        event_locs.append(int(idx.get_loc(ts)))

    n = len(series)
    event_mask = np.zeros(n, dtype=bool)
    for loc in event_locs:
        lo = max(0, loc + pre)
        hi = min(n, loc + post + 1)
        event_mask[lo:hi] = True

    values = series.to_numpy()
    event_mean = float(values[event_mask].mean()) if event_mask.any() else float("nan")
    complement = values[~event_mask]
    complement_mean = float(complement.mean()) if len(complement) else float("nan")
    return {
        "n": n,
        "n_events": len(event_locs),
        "window": [pre, post],
        "event_mean": event_mean,
        "complement_mean": complement_mean,
        "mean_shift": event_mean - complement_mean
        if np.isfinite(event_mean) and np.isfinite(complement_mean)
        else float("nan"),
        "family": "constraint_flow",
        "lock_decision": None,
    }
