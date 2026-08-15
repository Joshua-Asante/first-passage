"""Feed health / staleness — build ADR formula 2×period + 30s."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from c1_signal_daemon.feed import feed_healthy, last_bar_age_s, staleness_limit_s


def test_staleness_limit_formula():
    assert staleness_limit_s(900.0) == 1830.0  # 2*900 + 30


def test_feed_unhealthy_when_disconnected():
    now = datetime(2026, 8, 8, 12, 0, tzinfo=timezone.utc)
    assert not feed_healthy(
        connected=False,
        last_bar_ts=now,
        now=now,
        bar_period_s=900.0,
    )


def test_feed_unhealthy_when_stale():
    now = datetime(2026, 8, 8, 12, 0, tzinfo=timezone.utc)
    stale = now - timedelta(seconds=1831)
    assert not feed_healthy(
        connected=True,
        last_bar_ts=stale,
        now=now,
        bar_period_s=900.0,
    )


def test_feed_healthy_inside_window():
    now = datetime(2026, 8, 8, 12, 0, tzinfo=timezone.utc)
    fresh = now - timedelta(seconds=100)
    assert feed_healthy(
        connected=True,
        last_bar_ts=fresh,
        now=now,
        bar_period_s=900.0,
    )


def test_last_bar_age_none_without_bar():
    now = datetime(2026, 8, 8, 12, 0, tzinfo=timezone.utc)
    assert last_bar_age_s(None, now) is None
