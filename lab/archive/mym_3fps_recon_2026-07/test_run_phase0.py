from __future__ import annotations

import math
from datetime import date

import pandas as pd
import pytest

from research_utils.camp_import import load_camp_sibling

_run = load_camp_sibling("run_phase0", __file__)
END_DATE_EXCLUSIVE = _run.END_DATE_EXCLUSIVE
START_DATE = _run.START_DATE
build_events = _run.build_events
evaluate = _run.evaluate
round_trip_cost_bp = _run.round_trip_cost_bp
third_fridays = _run.third_fridays


def _synthetic_event_frame(
    event_dates: list[date],
    *,
    overnight_multiplier: float = 1.001,
    noon_multiplier: float = 0.999,
) -> pd.DataFrame:
    rows = []
    for event_date in event_dates:
        friday = pd.Timestamp(event_date, tz="America/New_York")
        rows.extend(
            [
                {
                    "time": friday - pd.Timedelta(days=1) + pd.Timedelta(hours=15, minutes=59),
                    "open": 40_000.0,
                    "close": 40_000.0,
                },
                {
                    "time": friday + pd.Timedelta(hours=9, minutes=30),
                    "open": 40_000.0 * overnight_multiplier,
                    "close": 40_000.0 * overnight_multiplier,
                },
                {
                    "time": friday + pd.Timedelta(hours=12),
                    "open": 40_000.0 * overnight_multiplier * noon_multiplier,
                    "close": 40_000.0 * overnight_multiplier * noon_multiplier,
                },
            ]
        )
    return pd.DataFrame(rows).set_index("time")


def test_third_friday_calendar_is_frozen_native_micro_window() -> None:
    dates = third_fridays(START_DATE, END_DATE_EXCLUSIVE)
    assert len(dates) == 87
    assert dates[0] == date(2019, 5, 17)
    assert dates[-1] == date(2026, 7, 17)
    assert all(day.weekday() == 4 for day in dates)


def test_build_events_uses_thursday_close_and_friday_open_to_noon_short() -> None:
    event_date = date(2024, 3, 15)
    events = build_events(_synthetic_event_frame([event_date]), [event_date])
    assert len(events) == 1
    assert events.iloc[0]["overnight_spike_bp"] == pytest.approx(math.log(1.001) * 1e4)
    assert events.iloc[0]["short_reversal_bp"] == pytest.approx(-math.log(0.999) * 1e4)


def test_missing_exact_checkpoint_drops_event() -> None:
    event_date = date(2024, 3, 15)
    frame = _synthetic_event_frame([event_date])
    frame = frame.drop(pd.Timestamp("2024-03-15 12:00", tz="America/New_York"))
    assert build_events(frame, [event_date]).empty


def test_cost_law_uses_micro_notional_and_one_tick_each_side() -> None:
    assert round_trip_cost_bp(40_000.0, 0.91) == pytest.approx(1.41)


def test_evaluate_resolves_only_when_all_mechanism_and_economic_gates_pass() -> None:
    dates = third_fridays(date(2020, 1, 1), date(2022, 1, 1))
    events = build_events(
        _synthetic_event_frame(dates, overnight_multiplier=1.002, noon_multiplier=0.998),
        dates,
    )
    events["overnight_spike_bp"] += pd.Series(range(len(events)), dtype=float) * 0.01
    events["short_reversal_bp"] += pd.Series(range(len(events)), dtype=float) * 0.01
    result = evaluate(events, len(dates))
    assert result["verdict"] == "RESOLVED"
    assert all(result["gates"].values())


def test_wrong_sign_reversal_is_falsified_even_if_absolute_effect_is_large() -> None:
    dates = third_fridays(date(2020, 1, 1), date(2022, 1, 1))
    events = build_events(
        _synthetic_event_frame(dates, overnight_multiplier=1.002, noon_multiplier=1.002),
        dates,
    )
    events["overnight_spike_bp"] += pd.Series(range(len(events)), dtype=float) * 0.01
    events["short_reversal_bp"] -= pd.Series(range(len(events)), dtype=float) * 0.01
    result = evaluate(events, len(dates))
    assert result["verdict"] == "FALSIFIED"
    assert result["gates"]["P0_2_intraday_reversal"] is False
    assert result["gates"]["P0_3_cost_law"] is False


def test_low_coverage_is_ambiguous_not_a_return_verdict() -> None:
    dates = third_fridays(date(2020, 1, 1), date(2022, 1, 1))
    events = build_events(_synthetic_event_frame(dates[:5]), dates)
    assert evaluate(events, len(dates))["verdict"] == "AMBIGUOUS"
