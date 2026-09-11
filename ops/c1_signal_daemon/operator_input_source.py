"""One-shot operator-attended bar source for the bounded M1 ceremony."""
from __future__ import annotations

import json
import logging
import math
from pathlib import Path

from c1_rail.m1_stage1_contract import OPERATOR_INPUT_SOURCE
from c1_signal_daemon.feed import Bar
from c1_signal_daemon.m1_stage1_control import digest, utc
from c1_signal_daemon.m1_stage1_state import CeremonyError

log = logging.getLogger(__name__)

_RECORD_KEYS = {
    "schema_version", "ceremony_id", "boot_id", "venue_contract", "timestamp",
    "open", "high", "low", "close", "volume", "bar_sha256",
}


def cleanup_orphans(state_dir):
    state_dir = Path(state_dir)
    for pattern in ("m1_bar_*.json", "m1_upload_*.json", "m1_claim_*"):
        for path in state_dir.glob(pattern):
            path.unlink(missing_ok=True)


class OperatorInputSource:
    feed_mode = "operator_input"

    def __init__(self, state_dir: Path, *, boot_id: str):
        self.state_dir = Path(state_dir)
        self.boot_id = boot_id
        self.binding = None
        self.ceremony_id = None
        self._connected = False
        self._handed_out = False
        self._rejection_logged = False

    @property
    def connected(self):
        return self._connected

    def activate(self, binding, *, ceremony_id):
        if binding != OPERATOR_INPUT_SOURCE:
            raise CeremonyError("operator input binding refused")
        if self.binding == binding and self.ceremony_id == ceremony_id:
            return
        self.binding = dict(binding)
        self.ceremony_id = ceremony_id
        self._connected = False
        self._handed_out = False
        self._rejection_logged = False

    def _reject(self):
        if not self._rejection_logged:
            log.warning("operator_input: published bar rejected")
            self._rejection_logged = True
        return None

    def poll(self):
        if self.binding is None or self._handed_out:
            return None
        path = self.state_dir / f"m1_bar_{self.ceremony_id}.json"
        if not path.exists():
            return None
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(value, dict) or set(value) != _RECORD_KEYS:
                return self._reject()
            if (type(value["schema_version"]) is not int or value["schema_version"] != 1
                    or value["ceremony_id"] != self.ceremony_id
                    or value["boot_id"] != self.boot_id):
                return self._reject()
            numbers = [value[key] for key in ("open", "high", "low", "close", "volume")]
            if not all(type(number) in (int, float) and math.isfinite(number) and number > 0
                       for number in numbers):
                return self._reject()
            open_, high, low, close, volume = numbers
            if not low <= min(open_, close) <= max(open_, close) <= high:
                return self._reject()
            timestamp = utc(value["timestamp"])
            bar_value = {key: value[key] for key in
                         ("timestamp", "open", "high", "low", "close", "volume",
                          "venue_contract")}
            if value["bar_sha256"] != digest({"bar": bar_value, "source": self.binding}):
                return self._reject()
        except (OSError, ValueError, KeyError, TypeError, CeremonyError):
            return self._reject()
        self._handed_out = True
        self._connected = True
        return Bar(timestamp, float(open_), float(high), float(low), float(close), float(volume))

    def deactivate(self):
        if self.binding is None:
            return
        ident = self.ceremony_id
        self.binding = None
        self.ceremony_id = None
        self._connected = False
        self._handed_out = False
        self._rejection_logged = False
        for name in (f"m1_bar_{ident}.json", f"m1_upload_{ident}.json", f"m1_claim_{ident}"):
            (self.state_dir / name).unlink(missing_ok=True)
