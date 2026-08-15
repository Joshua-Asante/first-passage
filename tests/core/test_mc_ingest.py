"""Timezone-boundary tests for MC swap rollover counting."""

from datetime import datetime, timezone

from mc.ingest import count_rollovers


def test_naive_tradingview_timestamps_are_interpreted_as_eastern():
    assert count_rollovers(
        datetime(2026, 1, 2, 16, 30),
        datetime(2026, 1, 2, 17, 30),
    ) == 1


def test_aware_timestamps_are_converted_to_eastern_before_rollover_count():
    assert count_rollovers(
        datetime(2026, 1, 2, 21, 30, tzinfo=timezone.utc),
        datetime(2026, 1, 2, 22, 30, tzinfo=timezone.utc),
    ) == 1


def test_rollover_at_entry_is_strictly_excluded():
    assert count_rollovers(
        datetime(2026, 1, 2, 17, 0),
        datetime(2026, 1, 3, 16, 59),
    ) == 0
