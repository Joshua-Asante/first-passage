"""EvaluateLoop coordination; durable claim precedes ordinary ListenerClient POST."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import math
import uuid

from c1_signal_daemon.listener_client import serialize_b1_payload
from c1_signal_daemon.m1_stage1_control import (close, digest, enable, prepare,
                                               utc, validate_manifest)
from c1_signal_daemon.m1_stage1_state import CeremonyError, CeremonyStore, DaemonOwnership
from c1_signal_daemon.m1_stage1_strategy import M1Stage1TestStrategy


class M1Coordinator:
    def __init__(self, store, config_path, *, boot_id):
        self.store, self.config_path, self.boot_id = store, config_path, boot_id
        self.current_manifest = None
        self.effective_emit = False
        self.state = "DISABLED"
        self.ceremony_id = None
        self._accepted_bar = None

    def _active(self, obj, now):
        from c1_signal_daemon.daemon import load_config
        cfg = load_config(self.config_path)
        gate = cfg["m1_test"]
        item = obj["ceremonies"].get(obj["active"])
        if (not item or obj["boot_id"] != self.boot_id or item["boot_id"] != self.boot_id
                or obj["enabled"] is not True or item["state"] != "READY"
                or obj["active"] in obj["tombstones"]
                or cfg["emit_enabled"] is not True or gate["enabled"] is not True
                or cfg["strategy"] != "m1_stage1_test" or cfg["bar_period_s"] != 60
                or gate.get("boot_id") != self.boot_id or gate.get("ceremony_id") != obj["active"]
                or gate.get("generation") != obj["generation"]
                or item["generation"] != obj["generation"]
                or gate.get("manifest_sha256") != item["manifest_sha256"]
                or digest(item["manifest"]) != item["manifest_sha256"]):
            return None
        validate_manifest(item["manifest"])
        if now >= utc(item["manifest"]["expires"]):
            return None
        return item

    def before_poll(self, source, now):
        self.effective_emit = False
        self.current_manifest = None
        self._accepted_bar = None
        try:
            obj = self.store.read()
            self.ceremony_id = obj["active"]
            item = obj["ceremonies"].get(obj["active"], {})
            self.state = item.get("state", "DISABLED")
            if self.state == "READY" and now >= utc(item["manifest"]["expires"]):
                self.close_attempt("expired")
                source.deactivate()
                return False
            active = self._active(obj, now)
            if active is None:
                source.deactivate()
                return False
            self.current_manifest = active["manifest"]
            source.activate(active["manifest"]["source"])
            self.effective_emit = True
            return True
        except (CeremonyError, OSError, ValueError, KeyError, TypeError, SystemExit):
            self.state = "DISABLED"
            source.deactivate()
            return False

    def accept_bar(self, bar, binding, now):
        value = self.current_manifest
        if not value or binding != value["source"]:
            return False
        if bar.ts > utc(value["target"]):
            self.close_attempt("target_missed")
            return False
        numbers = (bar.open, bar.high, bar.low, bar.close, bar.volume)
        valid = (bar.ts == utc(value["target"]) and bar.ts.tzinfo is not None
                and 60 <= (now - bar.ts).total_seconds() <= 150
                and all(math.isfinite(n) and n > 0 for n in numbers)
                and bar.low <= min(bar.open, bar.close) <= max(bar.open, bar.close) <= bar.high)
        if valid:
            self._accepted_bar = dict(timestamp=bar.ts.isoformat(), open=float(bar.open),
                                      high=float(bar.high), low=float(bar.low), close=float(bar.close),
                                      volume=float(bar.volume))
        return valid

    def reserve(self, payload, now):
        with self.store.locked():
            obj = self.store._read()
            item = self._active(obj, now)
            if item is None or self.current_manifest != item["manifest"]:
                return False
            expected = "m1-" + digest({key: item["manifest"][key] for key in
                                       ("ceremony_id", "target", "contract_sha256", "source")})
            from c1_rail.m1_stage1_contract import LEG_ID, STOP_DIST_PTS
            if (self._accepted_bar is None or payload != dict(
                    leg_id=LEG_ID, signal_type="entry", bar_time=expected,
                    close=self._accepted_bar["close"], stop_dist_pts=STOP_DIST_PTS)):
                return False
            from c1_signal_daemon.m1_stage1_state import atomic_json
            ident = obj["active"]
            item["event_identity"] = expected
            item["request_sha256"] = hashlib.sha256(serialize_b1_payload(payload)).hexdigest()
            item["bar"] = self._accepted_bar.copy()
            item["bar_sha256"] = digest({"bar": item["bar"], "source": item["manifest"]["source"]})
            obj["tombstones"][ident] = dict(event_identity=expected, reason="evaluation_claimed")
            item["state"] = "EVALUATED"
            atomic_json(self.store.path, obj)
            item["state"] = "SEND_RESERVED"
            obj["enabled"] = False
            atomic_json(self.store.path, obj)
            self.state = "SEND_RESERVED"
            self.effective_emit = False
            return True

    def outcome(self, status=None, body=None, *, unknown=False):
        def advance(item, expected, terminal):
            closed = item["state"] == "CLOSED"
            pending = item.get("previous_state") if closed else item["state"]
            if pending != expected:
                raise CeremonyError("invalid response transition")
            # Operator close is permanent, including while the request is in flight.
            # Record the late outcome under it without reopening the gate or state.
            item["previous_state" if closed else "state"] = terminal
            self.state = item["state"]

        def record(obj):
            item = obj["ceremonies"][self.ceremony_id]
            advance(item, "SEND_RESERVED", "TRANSPORT_UNKNOWN" if unknown else "EMITTED")
            if not unknown:
                kind = "rejected" if not 200 <= status < 300 else "http_success"
                if body == "dry_run: computed, not sent":
                    kind = "dry_run_computed"
                item["response"] = {"http_status": status,
                                    "body_sha256": hashlib.sha256(body.encode()).hexdigest(),
                                    "response_kind": kind}
        self.store.mutate(record)
        if not unknown:
            def response(obj):
                item = obj["ceremonies"][self.ceremony_id]
                try:
                    data = json.loads(body)
                    listener_id = data.get("listener_id", data.get("log_id"))
                    if isinstance(listener_id, str):
                        item["listener_id"] = str(uuid.UUID(listener_id))
                except (ValueError, AttributeError, TypeError):
                    pass
                advance(item, "EMITTED", "RESPONSE_RECORDED")
            self.store.mutate(response)

    def close_attempt(self, reason):
        def record(obj):
            item = obj["ceremonies"].get(obj["active"])
            obj["enabled"] = False
            if item and item["state"] == "READY":
                item["state"] = "CLOSED"
                obj["tombstones"].setdefault(obj["active"], {"reason": reason})
        self.store.mutate(record)
        self.state = "CLOSED"
        self.effective_emit = False
