"""Evaluate loop — fail-closed + emit_disabled gates."""
from __future__ import annotations

from datetime import datetime, timezone

from c1_signal_daemon.evaluate_loop import EvaluateLoop
from c1_signal_daemon.feed import Bar
from c1_signal_daemon.listener_client import ListenerClient
from c1_signal_daemon.strategy_protocol import NullStrategy, Signal


class _Source:
    def __init__(self, bar: Bar | None, connected: bool = True) -> None:
        self._bar = bar
        self.connected = connected

    def poll(self) -> Bar | None:
        return self._bar


class _AlwaysSignal:
    def on_bar(self, bar: Bar) -> Signal | None:
        return Signal(
            leg_id="nas100_mnq",
            signal_type="entry",
            close=bar.close,
            stop_dist_pts=10.0,
            bar_time="t-fresh",
        )


TOKEN = "b" * 32
NOW = datetime(2026, 8, 8, 15, 0, tzinfo=timezone.utc)
BAR = Bar(
    ts=NOW,
    open=1.0,
    high=2.0,
    low=0.5,
    close=1.5,
)


def _client(calls: list):
    def transport(url, body, headers):
        calls.append(body)
        return 200, "ok"

    return ListenerClient(
        base_url="https://c1-rail.fly.dev",
        path_token=TOKEN,
        transport=transport,
    )


def test_fail_closed_suppresses_all_when_disconnected():
    calls: list = []
    loop = EvaluateLoop(
        source=_Source(BAR, connected=False),
        client=_client(calls),
        strategy=_AlwaysSignal(),
        emit_enabled=True,
        bar_period_s=900.0,
    )
    rec = loop.step(NOW)
    assert rec["action"] == "suppress"
    assert rec["reason"] == "feed_unhealthy"
    assert calls == []


def test_emit_disabled_suppresses_even_when_healthy():
    calls: list = []
    loop = EvaluateLoop(
        source=_Source(BAR, connected=True),
        client=_client(calls),
        strategy=_AlwaysSignal(),
        emit_enabled=False,
        bar_period_s=900.0,
    )
    rec = loop.step(NOW)
    assert rec["action"] == "suppress"
    assert rec["reason"] == "emit_disabled"
    assert calls == []


def test_null_strategy_never_posts():
    calls: list = []
    loop = EvaluateLoop(
        source=_Source(BAR, connected=True),
        client=_client(calls),
        strategy=NullStrategy(),
        emit_enabled=True,
        bar_period_s=900.0,
    )
    rec = loop.step(NOW)
    assert rec["action"] == "idle"
    assert calls == []


def test_emit_enabled_posts_b1():
    calls: list = []
    loop = EvaluateLoop(
        source=_Source(BAR, connected=True),
        client=_client(calls),
        strategy=_AlwaysSignal(),
        emit_enabled=True,
        bar_period_s=900.0,
    )
    rec = loop.step(NOW)
    assert rec["action"] == "posted"
    assert len(calls) == 1


def test_heartbeat_exposes_emit_flag():
    loop = EvaluateLoop(
        source=_Source(None, connected=True),
        client=_client([]),
        emit_enabled=False,
    )
    hb = loop.heartbeat(NOW)
    assert hb.ok is True
    assert hb.emit_enabled is False
    assert hb.feed_healthy is False  # no bar yet
