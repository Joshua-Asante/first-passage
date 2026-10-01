"""c1 venue-native monitoring spine (M1) — structured events + reconcile.

Implements the ops-owned half of
docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md:

  - append-only JSONL event stream (lock + flush + fsync)
  - immutable event variants (request / decision / transport / evidence /
    reconciliation)
  - honest transport states (accepted ≠ execution verified; unknown blocks
    risk-add and never auto-retries)
  - operator-attested broker-evidence overlay + six fixed reconcile verdicts
  - durable confirmed-base execution state (add sizing input)
  - injected operator-notification interface (no secrets in the ledger)

Does NOT own sizing arithmetic, lifecycle demotion, or Pine. Does NOT restore
ops/live_journal or ECR.
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import sys
import tempfile
import threading
import urllib.parse
import uuid
from dataclasses import asdict, dataclass, field, fields
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Protocol

# Standalone-run bootstrap (same pattern as ops/c1_rail/c1_rail_http_server.py). The
# reconcile CLI at the foot of this module is invoked directly at the
# desk (`python ops/c1_rail/c1_rail_telemetry.py --events ... --event-id ...`), where
# nothing has put core/ on sys.path yet — without this, `lib.*` below raises
# ModuleNotFoundError. Import-from-the-server is unaffected: the server runs the
# identical bootstrap first, so both inserts are already-present no-ops.
# parents[2] = repo root (this file lives under ops/c1_rail/).
_REPO_ROOT = Path(__file__).resolve().parents[2]
_RAIL_DIR = Path(__file__).resolve().parent
for _p in (str(_REPO_ROOT / "core"), str(_RAIL_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from lib.atomic_io import atomic_write_text  # noqa: E402
from lib.file_lock import exclusive_file_lock  # noqa: E402

log = logging.getLogger("c1_rail_telemetry")

SCHEMA_VERSION = 1

EVENT_KINDS = frozenset({
    "request_received",
    "decision",
    "transport_result",
    "broker_evidence",
    "reconciliation",
    # Written by ops/c1_rail/c1_rail_arm.py when an operator arms while the M1
    # acceptance artifact is not RESOLVED. Not a signal event — it records a
    # governance deviation in the same ledger the M1 gate is about, so the
    # deviation cannot exist without a record of it. See the monitoring ADR
    # Addendum 2026-07-31b: two such deviations (07-28, 07-31) each promised an
    # amendment "to be written after the fact" and neither was written until
    # 07-31. This makes that failure structurally impossible.
    "arming_deviation",
    # Operator attestation that one transport_unknown send has been reconciled
    # against the broker. Until one exists for an event_id, that unknown keeps
    # risk-add blocked across restarts (EventLedger re-derives it from disk).
    "transport_unknown_resolution",
})

TRANSPORT_STATES = frozenset({
    "not_attempted",
    "accepted",
    "failed",
    "unknown",
})

RECONCILE_VERDICTS = frozenset({
    "CHAIN_OK",
    "RAIL_ONLY",
    "REJECTED",
    "QTY_MISMATCH",
    "POSITION_MISMATCH",
    "NO_FLAT_CONFIRM",
})

# Secrets / auth material that must never appear as ledger field values.
SECRET_FIELD_DENYLIST = frozenset({
    "secret_key",
    "webhook_secret",
    "path_token",
    "webhook_id",  # URL path credential half — treat as secret for ledger
    "crosstrade_api_token",
    "bearer",
    "authorization",
    "password",
    "api_token",
})

_SECRET_VALUE_HINT = re.compile(
    r"(?i)(secret|token|bearer|password|authorization)\s*[:=]",
)


class TelemetryError(Exception):
    """Ledger / evidence / execution-state failure."""


class TelemetryUnhealthy(TelemetryError):
    """Stream corrupt or risk-add blocked until operator repair."""


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def new_event_id() -> str:
    return str(uuid.uuid4())


def body_sha256(raw: str | bytes) -> str:
    if isinstance(raw, str):
        raw = raw.encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def assert_no_secrets(obj: Any, *, path: str = "$") -> None:
    """Hard-fail if a denylisted key or secret-shaped value is present."""
    if isinstance(obj, Mapping):
        for key, value in obj.items():
            key_l = str(key).lower()
            if key_l in SECRET_FIELD_DENYLIST or any(
                bad in key_l for bad in ("secret", "token", "password", "bearer")
            ):
                raise TelemetryError(
                    f"secret-denylist key {key!r} at {path} — release blocker")
            assert_no_secrets(value, path=f"{path}.{key}")
    elif isinstance(obj, (list, tuple)):
        for i, item in enumerate(obj):
            assert_no_secrets(item, path=f"{path}[{i}]")
    elif isinstance(obj, str):
        if _SECRET_VALUE_HINT.search(obj):
            raise TelemetryError(
                f"secret-shaped value at {path} — release blocker")


@dataclass(frozen=True)
class TransportOutcome:
    """Honest send result — HTTP status alone is never execution verified."""
    state: str  # TRANSPORT_STATES
    http_status: int | None = None
    error: str | None = None

    def __post_init__(self) -> None:
        if self.state not in TRANSPORT_STATES:
            raise ValueError(f"invalid transport state {self.state!r}")


class OperatorNotifier(Protocol):
    def notify(self, level: str, message: str, *, event_id: str | None = None,
               details: Mapping[str, Any] | None = None) -> None: ...


class LoggingNotifier:
    """Default sink — CRITICAL/WARNING to the process logger."""

    def notify(self, level: str, message: str, *, event_id: str | None = None,
               details: Mapping[str, Any] | None = None) -> None:
        payload = {"event_id": event_id, "details": details or {}}
        if level.upper() == "CRITICAL":
            log.critical("%s | %s", message, payload)
        elif level.upper() == "WARNING":
            log.warning("%s | %s", message, payload)
        else:
            log.info("%s | %s", message, payload)


# Ack filenames are derived from alert ids, which are free text (the rehearsal
# ids contain ":", invalid in Windows filenames). Only these characters are kept
# literally; every other character, including uppercase letters, "." and "%", is
# percent-encoded from its UTF-8 bytes. ``urllib.parse.unquote`` therefore
# inverts the mapping, and distinct ids never share a filename even on a
# case-insensitive filesystem. UUID4 event ids use only kept characters, so
# their ack filenames are unchanged.
_ACK_NAME_KEEP = frozenset("abcdefghijklmnopqrstuvwxyz0123456789-_")
# Windows reserves these device names even with an extension ("con.ack.json").
_WINDOWS_DEVICE_NAMES = frozenset(
    {"con", "prn", "aux", "nul"}
    | {f"com{i}" for i in range(10)}
    | {f"lpt{i}" for i in range(10)}
)
ACK_SUFFIX = ".ack.json"
# Longest filename component ext4 and NTFS accept (bytes; ack names are ASCII).
_NAME_MAX = 255
# ``acknowledge`` stages the record in a same-directory temp file named from
# these, never from the alert id, so the ack name alone must fit ``_NAME_MAX``.
_ACK_TMP_PREFIX = ".ack-"
_ACK_TMP_SUFFIX = ".tmp"


def ack_filename(alert_id: str) -> str:
    """Filesystem-safe, collision-free ack filename for ``alert_id``.

    ``urllib.parse.unquote(name[:-len(ACK_SUFFIX)]) == alert_id``; the ack
    record also retains ``alert_id`` verbatim.
    """
    if not alert_id:
        raise ValueError("alert_id must be non-empty")
    stem = "".join(
        ch if ch in _ACK_NAME_KEEP
        else "".join(f"%{b:02X}" for b in ch.encode("utf-8"))
        for ch in alert_id
    )
    if stem in _WINDOWS_DEVICE_NAMES:
        stem = f"%{ord(stem[0]):02X}{stem[1:]}"
    name = stem + ACK_SUFFIX
    if len(name.encode("utf-8")) > _NAME_MAX:
        raise ValueError(f"alert_id too long for an ack filename: {alert_id!r}")
    return name


class FileAckNotifier:
    """Deployable attended notifier: write alert JSONL; operator drops ack.

    M1 requires a real reachable channel. This file sink is operator-reachable
    on the Fly volume (or local host dir) without inventing a third-party
    provider. A test double alone cannot pass M1 — the operator must write an
    ack file acknowledging a live alert id.
    """

    def __init__(self, alert_path: Path, ack_dir: Path) -> None:
        self.alert_path = Path(alert_path)
        self.ack_dir = Path(ack_dir)
        self.ack_dir.mkdir(parents=True, exist_ok=True)
        self.alert_path.parent.mkdir(parents=True, exist_ok=True)

    def notify(self, level: str, message: str, *, event_id: str | None = None,
               details: Mapping[str, Any] | None = None) -> None:
        alert_id = event_id or new_event_id()
        record = {
            "schema_version": SCHEMA_VERSION,
            "alert_id": alert_id,
            "ts_utc": utc_now_iso(),
            "level": level.upper(),
            "message": message,
            "details": dict(details or {}),
        }
        assert_no_secrets(record)
        line = json.dumps(record, separators=(",", ":"), sort_keys=True) + "\n"
        with exclusive_file_lock(self.alert_path):
            with self.alert_path.open("a", encoding="utf-8") as f:
                f.write(line)
                f.flush()
                os.fsync(f.fileno())
        LoggingNotifier().notify(level, message, event_id=alert_id, details=details)

    def acknowledge(self, alert_id: str, *, operator: str = "operator") -> Path:
        """Write an ack file for ``alert_id`` (operator / test harness).

        Re-acknowledging the same id returns the existing file unchanged, so
        the first acknowledgment stands, including against a concurrent
        acknowledgment. An existing file at this id's name that does not
        record this id is refused, never overwritten.
        """
        ack_path = self.ack_dir / ack_filename(alert_id)
        if not ack_path.is_file():
            record = {
                "schema_version": SCHEMA_VERSION,
                "alert_id": alert_id,
                "acked_utc": utc_now_iso(),
                "operator": operator,
            }
            fd, tmp_name = tempfile.mkstemp(
                dir=self.ack_dir, prefix=_ACK_TMP_PREFIX, suffix=_ACK_TMP_SUFFIX)
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    f.write(json.dumps(record, indent=2) + "\n")
                    f.flush()
                    os.fsync(f.fileno())
                # A hard link never replaces an existing name (unlike
                # os.replace) and publishes the complete, fsynced record: of
                # concurrent first acknowledgments exactly one creates the ack
                # file, and the rest fall through to the check below.
                os.link(tmp_name, ack_path)
                return ack_path
            except FileExistsError:
                pass
            finally:
                try:
                    os.unlink(tmp_name)
                except OSError:
                    pass
        try:
            existing = json.loads(ack_path.read_text(encoding="utf-8"))
        except ValueError as exc:
            raise ValueError(
                f"ack file {ack_path.name} is not a readable ack record; "
                f"refusing to overwrite it for alert_id {alert_id!r}") from exc
        if not isinstance(existing, dict) or existing.get("alert_id") != alert_id:
            raise ValueError(
                f"ack file {ack_path.name} records a different alert_id; "
                f"refusing to reuse it for {alert_id!r}")
        return ack_path

    def is_acknowledged(self, alert_id: str) -> bool:
        return (self.ack_dir / ack_filename(alert_id)).is_file()


@dataclass
class EventLedger:
    """Append-only JSONL with cross-thread lock, fsync, and startup validation."""

    path: Path
    _seq: int = field(default=0, init=False, repr=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False,
                                  repr=False)
    _healthy: bool = field(default=True, init=False, repr=False)
    _unhealthy_reason: str | None = field(default=None, init=False, repr=False)
    _risk_add_blocked: bool = field(default=False, init=False, repr=False)
    _block_reason: str | None = field(default=None, init=False, repr=False)
    # event_id -> order_id of every transport_unknown without a
    # transport_unknown_resolution, in ledger order. Derived from the stream,
    # so a restart cannot lift it.
    _unresolved_unknowns: dict[str, str | None] = field(
        default_factory=dict, init=False, repr=False)
    # Bytes this instance last saw on disk. Another process (c1_rail_arm.py,
    # the resolution CLI) may append between our writes; a size change makes
    # the next read or append rescan instead of reusing a stale seq.
    _known_size: int = field(default=0, init=False, repr=False)

    def __post_init__(self) -> None:
        self.path = Path(self.path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.validate_startup()

    @property
    def healthy(self) -> bool:
        return self._healthy

    @property
    def unhealthy_reason(self) -> str | None:
        return self._unhealthy_reason

    @property
    def risk_add_blocked(self) -> bool:
        self._refresh_if_changed()
        return (self._risk_add_blocked or not self._healthy
                or bool(self._unresolved_unknowns))

    @property
    def block_reason(self) -> str | None:
        self._refresh_if_changed()
        if not self._healthy:
            return self._unhealthy_reason
        if self._block_reason is not None:
            return self._block_reason
        if self._unresolved_unknowns:
            first = next(iter(self._unresolved_unknowns))
            return (f"transport_unknown for event_id={first} unresolved "
                    f"({len(self._unresolved_unknowns)} total); reconcile "
                    f"before retry")
        return None

    @property
    def unresolved_unknowns(self) -> dict[str, str | None]:
        """event_id -> order_id of every unreconciled transport_unknown."""
        self._refresh_if_changed()
        return dict(self._unresolved_unknowns)

    def block_risk_add(self, reason: str) -> None:
        """In-process block. A transport_unknown is durable on its own: its
        appended transport_result registers it and startup re-derives it."""
        self._risk_add_blocked = True
        self._block_reason = reason

    def clear_risk_add_block(self) -> None:
        """Operator repair only — never auto-clear on uncertain send.

        Clears the in-process block only. A durable transport_unknown clears
        through ``resolve_transport_unknown`` and nothing else.
        """
        self._refresh_if_changed()
        if not self._healthy:
            raise TelemetryUnhealthy(
                f"cannot clear risk-add block while ledger unhealthy: "
                f"{self._unhealthy_reason}")
        if self._unresolved_unknowns:
            raise TelemetryError(
                f"cannot clear risk-add block: unresolved transport_unknown "
                f"event_id(s) {sorted(self._unresolved_unknowns)}; record a "
                f"resolution with resolve_transport_unknown")
        self._risk_add_blocked = False
        self._block_reason = None

    def resolve_transport_unknown(self, event_id: str, *, resolved_by: str,
                                  note: str) -> dict:
        """Append the operator's reconciliation of one transport_unknown.

        Refused unless the event is an unresolved unknown and the ledger holds
        operator-attested ``broker_evidence`` for it: the resolution records
        what the broker showed; it is not a way to skip looking.
        """
        if not isinstance(resolved_by, str) or not resolved_by.strip():
            raise TelemetryError("resolved_by must be a non-empty string")
        if not isinstance(note, str) or not note.strip():
            raise TelemetryError("note must be a non-empty string")
        self._refresh_if_changed()
        if event_id not in self._unresolved_unknowns:
            raise TelemetryError(
                f"event_id={event_id} is not an unresolved transport_unknown")
        if not any(r.get("kind") == "broker_evidence"
                   and r.get("event_id") == event_id
                   for r in self.iter_records()):
            raise TelemetryError(
                f"no broker_evidence for event_id={event_id}; attest the "
                f"broker state before resolving")
        return self.append(
            "transport_unknown_resolution",
            {"resolved_by": resolved_by, "note": note},
            event_id=event_id,
            order_id=self._unresolved_unknowns[event_id],
        )

    def _track(self, record: Mapping[str, Any]) -> None:
        kind = record.get("kind")
        eid = str(record.get("event_id"))
        if (kind == "transport_result"
                and record.get("transport_state") == "unknown"):
            self._unresolved_unknowns[eid] = record.get("order_id")
        elif kind == "transport_unknown_resolution":
            self._unresolved_unknowns.pop(eid, None)

    def _disk_size(self) -> int:
        try:
            return self.path.stat().st_size
        except FileNotFoundError:
            return 0

    def _refresh_if_changed(self) -> None:
        """Rescan when another process has appended since our last look."""
        if self._healthy and self._disk_size() != self._known_size:
            with self._lock:
                with exclusive_file_lock(self.path):
                    if self._disk_size() != self._known_size:
                        self.validate_startup()

    def validate_startup(self) -> None:
        """Full-stream validation. Truncated/malformed tails block risk-add.

        Also re-derives every unresolved transport_unknown, so the block it
        imposed survives a process restart until an operator resolution.
        """
        self._unresolved_unknowns = {}
        if not self.path.exists():
            self._seq = 0
            self._healthy = True
            self._unhealthy_reason = None
            self._known_size = 0
            return
        last_seq = 0
        size = 0
        try:
            with self.path.open("rb") as f:
                size = os.fstat(f.fileno()).st_size
                for lineno, raw in enumerate(f, start=1):
                    line = raw.decode("utf-8")
                    if not line.strip():
                        continue
                    try:
                        obj = json.loads(line)
                    except ValueError as exc:
                        raise TelemetryUnhealthy(
                            f"malformed JSONL at {self.path.name}:{lineno}: "
                            f"{exc}") from exc
                    if not isinstance(obj, dict):
                        raise TelemetryUnhealthy(
                            f"non-object JSONL at {self.path.name}:{lineno}")
                    seq = obj.get("seq")
                    if not isinstance(seq, int) or seq <= last_seq:
                        raise TelemetryUnhealthy(
                            f"non-monotonic seq at {self.path.name}:{lineno} "
                            f"(got {seq!r}, last={last_seq})")
                    kind = obj.get("kind")
                    if kind not in EVENT_KINDS:
                        raise TelemetryUnhealthy(
                            f"unknown kind {kind!r} at "
                            f"{self.path.name}:{lineno}")
                    last_seq = seq
                    self._track(obj)
        except (TelemetryUnhealthy, UnicodeDecodeError) as exc:
            self._healthy = False
            self._unhealthy_reason = str(exc)
            self._risk_add_blocked = True
            self._block_reason = str(exc)
            self._seq = last_seq
            log.critical("event ledger unhealthy — risk-add blocked: %s", exc)
            return
        self._seq = last_seq
        self._known_size = size
        self._healthy = True
        self._unhealthy_reason = None
        if self._unresolved_unknowns:
            log.critical("unresolved transport_unknown in ledger — risk-add "
                         "blocked: %s", sorted(self._unresolved_unknowns))

    def append(self, kind: str, payload: Mapping[str, Any], *,
               event_id: str, order_id: str | None = None) -> dict:
        """Append one UTF-8 JSONL record under lock+fsync. Returns the record."""
        if kind not in EVENT_KINDS:
            raise TelemetryError(f"unknown event kind {kind!r}")
        record = {
            "schema_version": SCHEMA_VERSION,
            "seq": 0,  # filled under lock
            "ts_utc": utc_now_iso(),
            "kind": kind,
            "event_id": event_id,
            "order_id": order_id,
            **dict(payload),
        }
        assert_no_secrets(record)
        with self._lock:
            if not self._healthy:
                raise TelemetryUnhealthy(
                    f"ledger unhealthy: {self._unhealthy_reason}")
            with exclusive_file_lock(self.path):
                if self._disk_size() != self._known_size:
                    # Another process appended (arm helper, resolution CLI):
                    # reusing our cached seq would duplicate theirs and leave
                    # the stream non-monotonic at the next startup.
                    self.validate_startup()
                    if not self._healthy:
                        raise TelemetryUnhealthy(
                            f"ledger unhealthy: {self._unhealthy_reason}")
                next_seq = self._seq + 1
                record["seq"] = next_seq
                line = json.dumps(record, separators=(",", ":"),
                                  sort_keys=True) + "\n"
                with self.path.open("a", encoding="utf-8") as f:
                    f.write(line)
                    f.flush()
                    os.fsync(f.fileno())
                    self._known_size = os.fstat(f.fileno()).st_size
                self._seq = next_seq
                self._track(record)
        return record

    def iter_records(self) -> Iterable[dict]:
        if not self.path.exists():
            return
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    yield json.loads(line)


@dataclass
class ExecutionStateStore:
    """Durable broker-confirmed base qty per leg_key — survives restart.

    Cleared only by broker-confirmed flatness (operator evidence / reconcile).
    Intended entry quantity must never seed this store.
    """

    path: Path

    def __post_init__(self) -> None:
        self.path = Path(self.path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write({"legs": {}, "schema_version": SCHEMA_VERSION,
                         "last_updated_utc": utc_now_iso()})

    def _read(self) -> dict:
        try:
            obj = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise TelemetryError(
                f"execution state unreadable ({self.path.name}): {exc}") from exc
        if not isinstance(obj, dict) or "legs" not in obj:
            raise TelemetryError(
                f"execution state malformed ({self.path.name})")
        return obj

    def _write(self, obj: dict) -> None:
        assert_no_secrets(obj)
        atomic_write_text(self.path, json.dumps(obj, indent=2) + "\n")

    def get_confirmed_base(self, leg_key: str) -> int | None:
        legs = self._read().get("legs") or {}
        entry = legs.get(leg_key)
        if entry is None:
            return None
        qty = entry.get("confirmed_base_qty")
        if not isinstance(qty, int) or qty <= 0:
            return None
        return qty

    def set_confirmed_base(self, leg_key: str, qty: int, *,
                           event_id: str | None = None,
                           order_id: str | None = None) -> None:
        if not isinstance(qty, int) or qty <= 0:
            raise TelemetryError(
                f"confirmed base qty must be positive int, got {qty!r}")
        with exclusive_file_lock(self.path):
            state = self._read()
            legs = dict(state.get("legs") or {})
            legs[leg_key] = {
                "confirmed_base_qty": qty,
                "event_id": event_id,
                "order_id": order_id,
                "confirmed_utc": utc_now_iso(),
            }
            state["legs"] = legs
            state["last_updated_utc"] = utc_now_iso()
            state["schema_version"] = SCHEMA_VERSION
            self._write(state)

    def clear_leg(self, leg_key: str) -> None:
        with exclusive_file_lock(self.path):
            state = self._read()
            legs = dict(state.get("legs") or {})
            legs.pop(leg_key, None)
            state["legs"] = legs
            state["last_updated_utc"] = utc_now_iso()
            self._write(state)

    def load_into(self, open_leg_state: dict[str, int]) -> None:
        """Hydrate an in-memory open_leg_state from durable confirmed bases."""
        legs = self._read().get("legs") or {}
        open_leg_state.clear()
        for leg_key, entry in legs.items():
            qty = entry.get("confirmed_base_qty")
            if isinstance(qty, int) and qty > 0:
                open_leg_state[leg_key] = qty


def decision_fields(decision: Any) -> dict[str, Any]:
    """Flatten a SizingDecision (or duck-typed twin) for a decision event."""
    keys = (
        "leg_id", "signal_type", "qty_out", "submit", "halt", "halt_reason",
        "floored", "leg_key", "dd_scale", "lifecycle_multiplier", "r_eff",
        "risk_dollars", "per_contract", "qty_base_raw", "reserve_cap",
    )
    out: dict[str, Any] = {}
    for key in keys:
        if hasattr(decision, key):
            out[key] = getattr(decision, key)
    return out


def make_request_received(
    *, event_id: str, auth_ok: bool, body_category: str,
    body_hash: str, order_id: str | None = None,
    parsed_fields: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "auth_ok": auth_ok,
        "body_category": body_category,
        "body_sha256": body_hash,
        "parsed": dict(parsed_fields) if parsed_fields else None,
        "order_id": order_id,
    }


def make_transport_payload(outcome: TransportOutcome, *, dry_run: bool,
                           payload_sha256: str | None = None) -> dict:
    return {
        "transport_state": outcome.state,
        "http_status": outcome.http_status,
        "error": outcome.error,
        "dry_run": dry_run,
        "payload_sha256": payload_sha256,
        # Explicit: never claim execution from transport alone.
        "execution_verified": False,
    }


@dataclass(frozen=True)
class BrokerEvidence:
    """Operator-attested CrossTrade + Tradovate facts for one event/order.

    S4 execution-quality fields (optional, additive 2026-08-07): capture at fill
    one so fills/exits research un-suspends without a schema migration mid-stream.
    All new fields default None — pre-S4 overlays remain loadable.
    """
    event_id: str
    order_id: str | None = None
    crosstrade_receive: bool | None = None
    crosstrade_validate: bool | None = None
    crosstrade_execute: bool | None = None
    crosstrade_trace_id: str | None = None
    tradovate_order_id: str | None = None
    tradovate_status: str | None = None
    fill_qty: int | None = None
    fill_price: float | None = None
    position_after: int | None = None
    flat_confirmed: bool | None = None
    notes: str | None = None
    attested_utc: str = field(default_factory=utc_now_iso)
    schema_version: int = SCHEMA_VERSION
    # --- S4 per-fill execution quality (SPEC 2026-08-07-loop-s4) ---
    intended_price: float | None = None  # signal/alert close used for sizing
    fill_slippage_pts: float | None = None  # fill − intended, signed in points
    fill_latency_ms: float | None = None  # signal ts → fill ts
    commission_usd: float | None = None
    signal_origin: str | None = None  # "tv" | "python_daemon" | "canned" | "manual"
    exit_fill_price: float | None = None
    exit_slippage_pts: float | None = None

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        assert_no_secrets(d)
        return d

    @classmethod
    def from_dict(cls, obj: Mapping[str, Any]) -> "BrokerEvidence":
        known = {f.name for f in fields(cls)}
        kwargs = {k: obj[k] for k in known if k in obj}
        return cls(**kwargs)  # type: ignore[arg-type]


def append_broker_evidence(ledger: EventLedger, evidence: BrokerEvidence) -> dict:
    return ledger.append(
        "broker_evidence",
        evidence.to_dict(),
        event_id=evidence.event_id,
        order_id=evidence.order_id,
    )


def reconcile_chain(
    *,
    intended_qty: int | None,
    transport_state: str | None,
    evidence: BrokerEvidence | None,
    signal_type: str | None = None,
) -> str:
    """Emit exactly one of the six fixed M1 verdicts."""
    if transport_state not in (None, "accepted") and evidence is None:
        return "RAIL_ONLY"
    if evidence is None:
        return "RAIL_ONLY"

    # Downstream reject (CrossTrade validate/execute failed) — even on HTTP 200.
    if evidence.crosstrade_validate is False or evidence.crosstrade_execute is False:
        return "REJECTED"
    if (evidence.tradovate_status or "").lower() in {
        "rejected", "reject", "cancelled", "canceled", "failed",
    }:
        return "REJECTED"

    is_flat = signal_type in ("exit", "flat") or evidence.flat_confirmed is True
    if is_flat or signal_type in ("exit", "flat"):
        if evidence.flat_confirmed is not True:
            return "NO_FLAT_CONFIRM"
        if evidence.position_after not in (None, 0):
            return "POSITION_MISMATCH"
        return "CHAIN_OK"

    if evidence.fill_qty is None:
        # Transport accepted but no fill attached yet.
        if transport_state == "accepted":
            return "RAIL_ONLY"
        return "RAIL_ONLY"

    if intended_qty is not None and evidence.fill_qty != intended_qty:
        return "QTY_MISMATCH"

    if evidence.position_after is not None and intended_qty is not None:
        # For entry, position_after should equal fill; loose check if provided.
        if evidence.position_after != evidence.fill_qty:
            return "POSITION_MISMATCH"

    if (
        evidence.crosstrade_receive is True
        and evidence.crosstrade_validate is True
        and evidence.crosstrade_execute is True
        and evidence.fill_qty is not None
        and (intended_qty is None or evidence.fill_qty == intended_qty)
    ):
        return "CHAIN_OK"

    # Partial evidence without a clean reject → still rail-only until joined.
    return "RAIL_ONLY"


def write_reconciliation(
    ledger: EventLedger, *, event_id: str, order_id: str | None,
    verdict: str, intended_qty: int | None = None,
    evidence: BrokerEvidence | None = None,
    transport_state: str | None = None,
    signal_type: str | None = None,
) -> dict:
    if verdict not in RECONCILE_VERDICTS:
        raise TelemetryError(f"invalid reconcile verdict {verdict!r}")
    payload = {
        "verdict": verdict,
        "intended_qty": intended_qty,
        "transport_state": transport_state,
        "signal_type": signal_type,
        "evidence_event_id": evidence.event_id if evidence else None,
        "fill_qty": evidence.fill_qty if evidence else None,
        "flat_confirmed": evidence.flat_confirmed if evidence else None,
    }
    return ledger.append("reconciliation", payload, event_id=event_id,
                         order_id=order_id)


def load_evidence_overlay(path: Path) -> list[BrokerEvidence]:
    """Read operator-attested JSONL overlay (one BrokerEvidence per line)."""
    path = Path(path)
    if not path.exists():
        return []
    out: list[BrokerEvidence] = []
    with path.open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except ValueError as exc:
                raise TelemetryError(
                    f"evidence overlay malformed at {path.name}:{lineno}: "
                    f"{exc}") from exc
            out.append(BrokerEvidence.from_dict(obj))
    return out


def append_evidence_overlay(path: Path, evidence: BrokerEvidence) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(evidence.to_dict(), separators=(",", ":"),
                      sort_keys=True) + "\n"
    with exclusive_file_lock(path):
        with path.open("a", encoding="utf-8") as f:
            f.write(line)
            f.flush()
            os.fsync(f.fileno())


def find_records_for_event(ledger: EventLedger, event_id: str) -> list[dict]:
    return [r for r in ledger.iter_records() if r.get("event_id") == event_id]


def reconcile_event(
    ledger: EventLedger,
    *,
    event_id: str,
    evidence: BrokerEvidence | None = None,
) -> str:
    """Join rail records + evidence for one event_id; append reconciliation."""
    records = find_records_for_event(ledger, event_id)
    if not records:
        raise TelemetryError(f"no rail records for event_id={event_id}")
    decision = next((r for r in records if r.get("kind") == "decision"), None)
    transport = next(
        (r for r in records if r.get("kind") == "transport_result"), None)
    intended = decision.get("qty_out") if decision else None
    signal_type = decision.get("signal_type") if decision else None
    order_id = (decision or records[0]).get("order_id")
    transport_state = transport.get("transport_state") if transport else None
    if evidence is None:
        # Prefer evidence already in the ledger stream.
        ev_rec = next(
            (r for r in records if r.get("kind") == "broker_evidence"), None)
        if ev_rec is not None:
            evidence = BrokerEvidence.from_dict(ev_rec)
    verdict = reconcile_chain(
        intended_qty=intended if isinstance(intended, int) else None,
        transport_state=transport_state,
        evidence=evidence,
        signal_type=signal_type,
    )
    write_reconciliation(
        ledger, event_id=event_id, order_id=order_id, verdict=verdict,
        intended_qty=intended if isinstance(intended, int) else None,
        evidence=evidence, transport_state=transport_state,
        signal_type=signal_type,
    )
    return verdict


# ── CLI helpers (reconcile; APPENDS a reconciliation event) ───────────────

def iter_arming_deviations(ledger: EventLedger) -> list[dict]:
    """Return every `arming_deviation` record in ledger order.

    Pure read — the kind is written by `ops/c1_rail/c1_rail_arm.py` when an operator
    arms past an unresolved M1 gate. Nothing else in the reconcile path was
    reading it back, so deviations accumulated unsummarized.
    """
    return [r for r in ledger.iter_records() if r.get("kind") == "arming_deviation"]


def format_arming_deviation(record: Mapping[str, Any]) -> str:
    """One-line secret-free summary of an arming_deviation record."""
    parts = [
        f"seq={record.get('seq')!r}",
        f"ts_utc={record.get('ts_utc')!r}",
        f"operator_reason={record.get('operator_reason')!r}",
        f"gate_reason={record.get('gate_reason')!r}",
    ]
    if "requested_hours" in record:
        parts.append(f"requested_hours={record.get('requested_hours')!r}")
    return " ".join(parts)


def _cli_reconcile(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(
        description=(
            "c1 M1 reconciler (rail events + evidence overlay). Does NOT place, "
            "modify, or cancel any order — but is not read-only: it APPENDS a "
            "reconciliation event to the ledger recording the verdict. "
            "`--deviations` and `--unresolved` are read-only. "
            "`--resolve-unknown` appends the operator's resolution of one "
            "transport_unknown, which lifts its risk-add block."))
    ap.add_argument("--events", type=Path, required=True)
    ap.add_argument("--event-id", default=None,
                    help="reconcile this event_id (required unless --deviations)")
    ap.add_argument("--evidence", type=Path, default=None,
                    help="optional overlay JSONL; else use ledger broker_evidence")
    ap.add_argument("--deviations", action="store_true",
                    help="list arming_deviation records (read-only; no append)")
    ap.add_argument("--unresolved", action="store_true",
                    help="list unresolved transport_unknown events "
                         "(read-only; no append)")
    ap.add_argument("--resolve-unknown", action="store_true",
                    help="APPEND an operator resolution for --event-id; needs "
                         "broker_evidence for it, --resolved-by and --note")
    ap.add_argument("--resolved-by", default=None)
    ap.add_argument("--note", default=None)
    args = ap.parse_args(argv)
    ledger = EventLedger(args.events)

    if args.deviations:
        if args.event_id is not None:
            raise SystemExit("--deviations is mutually exclusive with --event-id")
        records = iter_arming_deviations(ledger)
        print(f"arming_deviations: {len(records)}")
        for record in records:
            print(format_arming_deviation(record))
        return 0

    if args.unresolved:
        if not ledger.healthy:
            raise SystemExit(f"ledger unhealthy: {ledger.unhealthy_reason}")
        unresolved = ledger.unresolved_unknowns
        print(f"unresolved_transport_unknown: {len(unresolved)}")
        for eid, oid in unresolved.items():
            print(f"event_id={eid} order_id={oid!r}")
        return 0

    if args.resolve_unknown:
        if not args.event_id:
            raise SystemExit("--resolve-unknown requires --event-id")
        try:
            ledger.resolve_transport_unknown(
                args.event_id, resolved_by=args.resolved_by or "",
                note=args.note or "")
        except TelemetryError as exc:
            raise SystemExit(f"refused: {exc}") from exc
        print(f"resolved event_id={args.event_id}; "
              f"remaining={len(ledger.unresolved_unknowns)}")
        return 0

    if not args.event_id:
        raise SystemExit("--event-id is required unless --deviations is set")

    evidence = None
    if args.evidence is not None:
        matches = [e for e in load_evidence_overlay(args.evidence)
                   if e.event_id == args.event_id]
        if not matches:
            raise SystemExit(f"no evidence for event_id={args.event_id}")
        evidence = matches[-1]
    verdict = reconcile_event(ledger, event_id=args.event_id, evidence=evidence)
    print(verdict)
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli_reconcile())
