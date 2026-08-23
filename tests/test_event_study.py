"""T2 event-study — planted mean shift recovered."""

import numpy as np
import pandas as pd

from research_utils.event_study import event_study, month_end_events


def test_planted_mean_shift_recovered():
    idx = pd.bdate_range("2020-01-01", periods=260)
    rng = np.random.default_rng(3)
    r = pd.Series(rng.normal(0.0, 0.01, size=len(idx)), index=idx)
    events = month_end_events(idx)
    assert len(events) >= 8
    planted = r.copy()
    planted.loc[events] = planted.loc[events] + 0.08
    got = event_study(planted, events, window=(0, 0))
    assert got["n_events"] == len(events)
    assert got["mean_shift"] > 0.04
    assert got["lock_decision"] is None
    assert got["family"] == "constraint_flow"


def test_month_end_events_inside_index():
    idx = pd.bdate_range("2021-01-01", "2021-12-31")
    events = month_end_events(idx)
    assert events.isin(idx).all()
    assert 10 <= len(events) <= 12
