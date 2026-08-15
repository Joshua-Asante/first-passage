"""Evaluate loop: bars → strategy → fail-closed gate → optional B1 POST."""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from c1_signal_daemon.b1_payload import build_b1_payload
from c1_signal_daemon.feed import BarSource, feed_healthy, last_bar_age_s
from c1_signal_daemon.heartbeat import HeartbeatState
from c1_signal_daemon.listener_client import ListenerClient
from c1_signal_daemon.strategy_protocol import NullStrategy, Strategy

log = logging.getLogger(__name__)


class EvaluateLoop:
    def __init__(
        self,
        *,
        source: BarSource,
        client: ListenerClient,
        strategy: Strategy | None = None,
        bar_period_s: float = 900.0,
        emit_enabled: bool = False,
    ) -> None:
        self._source = source
        self._client = client
        self._strategy = strategy or NullStrategy()
        self._bar_period_s = float(bar_period_s)
        self.emit_enabled = bool(emit_enabled)
        self._last_bar_ts: datetime | None = None
        self._last_post: tuple[int, str] | None = None

    def heartbeat(self, now: datetime | None = None) -> HeartbeatState:
        now = now or datetime.now(timezone.utc)
        healthy = feed_healthy(
            connected=self._source.connected,
            last_bar_ts=self._last_bar_ts,
            now=now,
            bar_period_s=self._bar_period_s,
        )
        return HeartbeatState(
            ok=True,
            last_bar_age_s=last_bar_age_s(self._last_bar_ts, now),
            feed_healthy=healthy,
            emit_enabled=self.emit_enabled,
            connected=self._source.connected,
        )

    def step(self, now: datetime | None = None) -> dict[str, Any]:
        """One poll cycle. Returns an audit record (never raises on no-fire)."""
        now = now or datetime.now(timezone.utc)
        bar = self._source.poll()
        if bar is not None:
            self._last_bar_ts = bar.ts

        healthy = feed_healthy(
            connected=self._source.connected,
            last_bar_ts=self._last_bar_ts,
            now=now,
            bar_period_s=self._bar_period_s,
        )
        if not healthy:
            return {"action": "suppress", "reason": "feed_unhealthy"}

        if bar is None:
            return {"action": "idle", "reason": "no_new_bar"}

        signal = self._strategy.on_bar(bar)
        if signal is None:
            return {"action": "idle", "reason": "strategy_none"}

        if not self.emit_enabled:
            return {
                "action": "suppress",
                "reason": "emit_disabled",
                "signal_type": signal.signal_type,
            }

        payload = build_b1_payload(
            leg_id=signal.leg_id,
            signal_type=signal.signal_type,
            bar_time=signal.bar_time,
            close=signal.close,
            stop_dist_pts=signal.stop_dist_pts,
        )
        status, body = self._client.post_b1(payload)
        self._last_post = (status, body)
        log.info("b1_post status=%s body_prefix=%r", status, body[:120])
        return {
            "action": "posted",
            "http_status": status,
            "payload": payload,
        }
