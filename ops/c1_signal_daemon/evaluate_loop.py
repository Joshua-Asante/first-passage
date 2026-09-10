"""Evaluate loop: bars → strategy → fail-closed gate → optional B1 POST."""
from __future__ import annotations

import logging
import threading
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
        coordinator=None,
        boot_id: str | None = None,
    ) -> None:
        self._source = source
        self._client = client
        self._strategy = strategy or NullStrategy()
        self._bar_period_s = float(bar_period_s)
        self.emit_enabled = bool(emit_enabled)
        self._last_bar_ts: datetime | None = None
        self._last_post: tuple[int, str] | None = None
        self._coordinator = coordinator
        self._boot_id = boot_id
        self._step_lock = threading.Lock()

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
            emit_enabled=(self._coordinator.effective_emit if self._coordinator else self.emit_enabled),
            connected=self._source.connected,
            strategy=type(self._strategy).__name__,
            feed_mode=getattr(self._source, "feed_mode", "idle"),
            boot_id=getattr(self._coordinator, "boot_id", self._boot_id),
            ceremony_id=getattr(self._coordinator, "ceremony_id", None),
            ceremony_state=getattr(self._coordinator, "state", "DISABLED"),
            effective_emit=(self._coordinator.effective_emit if self._coordinator else self.emit_enabled),
        )

    def step(self, now: datetime | None = None) -> dict[str, Any]:
        """One poll cycle. Returns an audit record (never raises on no-fire)."""
        with self._step_lock:
            return self._step(now)

    def _step(self, now):
        realtime = now is None
        now = now or datetime.now(timezone.utc)
        if self._coordinator and not self._coordinator.before_poll(self._source, now):
            return {"action": "suppress", "reason": "ceremony_disabled"}
        if self._coordinator and isinstance(self._strategy, NullStrategy):
            from c1_signal_daemon.m1_stage1_strategy import M1Stage1TestStrategy
            self._strategy = M1Stage1TestStrategy(self._coordinator)
        bar = self._source.poll()
        if self._coordinator and bar is not None:
            if not self._coordinator.accept_bar(bar, getattr(self._source, "binding", None), now):
                return {"action": "suppress", "reason": "ceremony_bar_rejected"}
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

        if not (self._coordinator.effective_emit if self._coordinator else self.emit_enabled):
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
        if self._coordinator:
            if not self._coordinator.reserve(payload, datetime.now(timezone.utc) if realtime else now):
                return {"action": "suppress", "reason": "ceremony_not_reserved"}
            try:
                status, body = self._client.post_b1(payload)
            except Exception:
                self._coordinator.outcome(unknown=True)
                return {"action": "transport_unknown"}
            self._coordinator.outcome(status, body)
            log.info("m1_b1_post status=%s", status)
            return {"action": "posted", "http_status": status}
        status, body = self._client.post_b1(payload)
        self._last_post = (status, body)
        log.info("b1_post status=%s body_prefix=%r", status, body[:120])
        return {
            "action": "posted",
            "http_status": status,
            "payload": payload,
        }
