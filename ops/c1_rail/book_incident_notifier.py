"""Durable, channel-agnostic incident notification for the book route.

Card: docs/briefs/handoffs/2026-10-02-book-incident-notifier-build-card.md (FROZEN by
coordinator (3), 2026-10-02). Every committed ``incidents`` row of the book owner becomes one
notification job in the notifier's own journal, keyed by an opaque incident key. Detection,
each attempt, provider acceptance, delivery, delivery failure and the loss of every channel
are separate append-only events.

Isolation (card §3.7): the notifier reads incidents only through an injected read callable
(``BookAccountOwner.read_incidents`` bound to a path), never holds an owner instance, never
writes the owner DB and imports no broker, dispatch, arm or config-write module. A channel
or journal failure surfaces here and cannot change or block the owner's halt.

Out of this build (card §8): any concrete provider binding, the 60 s alternate-channel
escalation, acting on ``ALL_CHANNELS_LOST``, the external heartbeat and attendance.
"""
from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sqlite3
import threading
from typing import Protocol

try:  # pytest and the rail put ops/c1_rail on sys.path; the package import is the fallback.
    from c1_rail_telemetry import assert_no_secrets
except ImportError:  # pragma: no cover - exercised only outside the rail's path setup
    from .c1_rail_telemetry import assert_no_secrets


INCIDENT_KEY_DOMAIN = b"first-passage/book-incident-notification/v1\x00"
PUBLISH_STATES = ("accepted", "rejected", "unknown")
# kind -> (needs a secret reference, delivers). Concrete providers are OWED to D-MON.
# A non-delivering kind (local_file) is evidence only: its acceptance never ends a round,
# never counts against ALL_CHANNELS_LOST and never closes a job (card §3.3).
CHANNEL_KINDS = {"fake": (True, True), "local_file": (False, False)}
_SECRET_REF = re.compile(r"^(env|secret):[A-Z][A-Z0-9_]{0,63}$")
_NAME = re.compile(r"^[a-z][a-z0-9_-]{0,31}$")
_DIGEST = re.compile(r"^[0-9a-f]{64}$")
_CONFIG_KEYS = {"channels", "publish_timeout_s", "retry_initial_s", "retry_max_s"}
_CHANNEL_KEYS = {"name", "kind", "secret_ref"}
_JOURNAL = (
    "CREATE TABLE IF NOT EXISTS jobs (incident_key TEXT PRIMARY KEY, reason TEXT NOT NULL, "
    "detected_at TEXT NOT NULL, generation INTEGER NOT NULL, config_digest TEXT NOT NULL, "
    "state TEXT NOT NULL, next_attempt_at TEXT NOT NULL, rounds INTEGER NOT NULL, "
    "channels_lost INTEGER NOT NULL)",
    "CREATE TABLE IF NOT EXISTS events (sequence INTEGER PRIMARY KEY AUTOINCREMENT, "
    "incident_key TEXT NOT NULL, kind TEXT NOT NULL, channel TEXT, at TEXT NOT NULL, "
    "detail TEXT NOT NULL)",
)


class NotifierStoreError(RuntimeError):
    """The notifier's own journal is unavailable; the owner is never touched."""


class NotifierConfigError(ValueError):
    """Notifier configuration is invalid or carries an inline secret."""


def incident_key(incident_id: str) -> str:
    """Opaque idempotency key: plain SHA-256 over the domain-separated incident id (C-3)."""
    if not isinstance(incident_id, str) or not incident_id:
        raise ValueError("incident id required")
    return hashlib.sha256(INCIDENT_KEY_DOMAIN + incident_id.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class PublishResult:
    """A channel's answer. Acceptance is not delivery; ``delivered`` needs evidence."""
    state: str
    delivered: bool = False
    evidence_digest: str | None = None

    def __post_init__(self):
        if self.state not in PUBLISH_STATES:
            raise ValueError("invalid publish state")
        if self.delivered and self.state != "accepted":
            raise ValueError("only an accepted publish can carry delivery evidence")
        if self.evidence_digest is not None and not _DIGEST.match(self.evidence_digest):
            raise ValueError("evidence digest must be a sha256 hex digest")


class Channel(Protocol):
    name: str
    kind: str

    def publish(self, idempotency_key: str, payload: Mapping) -> PublishResult: ...


class FakeChannel:
    """Test channel: scripted outcomes, recorded calls. Never leaves the process."""
    kind = "fake"
    HANG = object()

    def __init__(self, name, outcomes=()):
        self.name = name
        self.outcomes = list(outcomes)
        self.calls = []
        self._released = threading.Event()

    def publish(self, idempotency_key, payload):
        self.calls.append((idempotency_key, dict(payload)))
        outcome = self.outcomes.pop(0) if self.outcomes else PublishResult("accepted", True)
        if outcome is FakeChannel.HANG:
            self._released.wait(5)
            return PublishResult("accepted")
        if isinstance(outcome, BaseException):
            raise outcome
        return outcome

    def release(self):
        self._released.set()


class LocalFileChannel:
    """Writes one local JSON record per incident key. Local evidence only, NOT delivery."""
    kind = "local_file"

    def __init__(self, name, directory):
        self.name = name
        self.directory = Path(directory)

    def publish(self, idempotency_key, payload):
        body = json.dumps(dict(payload), sort_keys=True, separators=(",", ":"))
        self.directory.mkdir(parents=True, exist_ok=True)
        target = self.directory / (idempotency_key + ".json")
        partial = target.with_suffix(".tmp")
        partial.write_text(body, encoding="utf-8")
        os.replace(partial, target)
        return PublishResult("accepted", evidence_digest=hashlib.sha256(
            body.encode("utf-8")).hexdigest())


@dataclass(frozen=True)
class ChannelSpec:
    name: str
    kind: str
    secret_ref: str | None = None

    def __post_init__(self):
        if not isinstance(self.name, str) or not _NAME.match(self.name):
            raise NotifierConfigError("invalid channel name")
        if self.kind not in CHANNEL_KINDS:
            raise NotifierConfigError("unknown channel kind")
        if self.secret_ref is None:
            if CHANNEL_KINDS[self.kind][0]:
                raise NotifierConfigError("channel requires a secret reference")
        elif not isinstance(self.secret_ref, str) or not _SECRET_REF.match(self.secret_ref):
            raise NotifierConfigError("secret_ref must name env:NAME or secret:NAME, never a value")


@dataclass(frozen=True)
class NotifierConfig:
    """Shared notifier settings plus an ordered channel list; no instance binding."""
    channels: tuple[ChannelSpec, ...]
    publish_timeout_s: float = 10.0
    retry_initial_s: float = 5.0
    retry_max_s: float = 300.0
    digest: str = field(init=False, compare=False)

    def __post_init__(self):
        if (not isinstance(self.channels, tuple) or not self.channels
                or not all(isinstance(spec, ChannelSpec) for spec in self.channels)):
            raise NotifierConfigError("at least one channel spec required")
        if len({spec.name for spec in self.channels}) != len(self.channels):
            raise NotifierConfigError("channel names must be unique")
        if not any(CHANNEL_KINDS[spec.kind][1] for spec in self.channels):
            raise NotifierConfigError("at least one delivering channel required")
        for name in ("publish_timeout_s", "retry_initial_s", "retry_max_s"):
            value = getattr(self, name)
            if (isinstance(value, bool) or not isinstance(value, (int, float))
                    or not math.isfinite(value) or value <= 0):
                raise NotifierConfigError(name + " must be a positive finite number")
        if self.retry_initial_s > self.retry_max_s:
            raise NotifierConfigError("retry_initial_s exceeds retry_max_s")
        canonical = json.dumps(self.resolved(), sort_keys=True, separators=(",", ":"))
        object.__setattr__(self, "digest", hashlib.sha256(canonical.encode("utf-8")).hexdigest())

    @classmethod
    def from_mapping(cls, raw):
        if not isinstance(raw, Mapping) or not set(raw) <= _CONFIG_KEYS:
            raise NotifierConfigError("unknown notifier config keys")
        channels = raw.get("channels")
        if not isinstance(channels, (list, tuple)):
            raise NotifierConfigError("channels must be a list")
        specs = []
        for entry in channels:
            if not isinstance(entry, Mapping) or not set(entry) <= _CHANNEL_KEYS:
                raise NotifierConfigError("unknown channel keys (inline values are refused)")
            specs.append(ChannelSpec(entry.get("name"), entry.get("kind"), entry.get("secret_ref")))
        settings = {key: raw[key] for key in _CONFIG_KEYS - {"channels"} if key in raw}
        return cls(tuple(specs), **settings)

    def resolved(self):
        """The validated configuration as data: references, never secret values."""
        return {"channels": [asdict(spec) for spec in self.channels],
                "publish_timeout_s": self.publish_timeout_s,
                "retry_initial_s": self.retry_initial_s,
                "retry_max_s": self.retry_max_s}


class IncidentNotifier:
    """Turns committed owner incidents into durable jobs and publishes them.

    ``read_incidents`` returns the owner's committed rows (``incident_id``, ``reason``,
    ``at``, ``generation``); ``clock`` returns an aware ``datetime``.
    """

    def __init__(self, store_path, *, read_incidents: Callable[[], Iterable[Mapping]],
                 channels: Mapping[str, Channel], config: NotifierConfig,
                 clock: Callable[[], datetime]):
        if not isinstance(config, NotifierConfig):
            raise NotifierConfigError("validated NotifierConfig required")
        if set(channels) != {spec.name for spec in config.channels} or any(
                channels[spec.name].kind != spec.kind or channels[spec.name].name != spec.name
                for spec in config.channels):
            raise NotifierConfigError("channels do not match the configuration")
        self.store_path = Path(store_path)
        self._read_incidents = read_incidents
        self._channels = tuple(channels[spec.name] for spec in config.channels)
        self.config = config
        self._clock = clock
        with self._journal() as db:
            for statement in _JOURNAL:
                db.execute(statement)

    # -- journal ---------------------------------------------------------------------------

    @contextmanager
    def _journal(self):
        """One short serialized transaction on the notifier's own journal, never the owner DB.

        The journal is a registered durable store (``scripts/check_durable_store_pragmas.py``):
        ``synchronous=FULL`` and an immediate transaction, on this file only.
        """
        try:
            self.store_path.parent.mkdir(parents=True, exist_ok=True)
            db = sqlite3.connect(self.store_path, timeout=5, isolation_level=None)
        except (sqlite3.Error, OSError) as exc:
            raise NotifierStoreError("notifier journal unavailable") from exc
        try:
            db.execute("PRAGMA synchronous=FULL")
            db.execute("BEGIN IMMEDIATE")
            yield db
            db.execute("COMMIT")
        except sqlite3.Error as exc:
            raise NotifierStoreError("notifier journal unavailable") from exc
        finally:
            try:
                if db.in_transaction:
                    db.execute("ROLLBACK")
            finally:
                db.close()

    def _now(self):
        now = self._clock()
        if not isinstance(now, datetime) or now.tzinfo is None:
            raise ValueError("aware clock time required")
        return now

    @staticmethod
    def _event(db, key, kind, channel, at, **detail):
        db.execute("INSERT INTO events(incident_key, kind, channel, at, detail) VALUES (?, ?, ?, ?, ?)",
                   (key, kind, channel, at.isoformat() if isinstance(at, datetime) else at,
                    json.dumps(detail, sort_keys=True)))

    # -- detection -------------------------------------------------------------------------

    @staticmethod
    def _parse(row):
        incident_id, reason, at, generation = (
            row["incident_id"], row["reason"], row["at"], row["generation"])
        if (not isinstance(reason, str) or not reason or not isinstance(at, str)
                or isinstance(generation, bool) or not isinstance(generation, int)):
            raise ValueError("malformed incident row")
        datetime.fromisoformat(at)
        return incident_key(incident_id), reason, at, generation

    @staticmethod
    def _malformed_key(row):
        """Opaque key for a skipped row: its incident key if the id is usable, else a digest."""
        try:
            return incident_key(row["incident_id"])
        except (KeyError, TypeError, ValueError):
            return hashlib.sha256(INCIDENT_KEY_DOMAIN + b"malformed\x00"
                                  + repr(row).encode("utf-8")).hexdigest()

    def poll(self):
        """Create one job per committed incident not yet journaled; return the new keys.

        A malformed row is skipped and recorded once as ``malformed_incident``; it never
        stops the other rows from being journaled.
        """
        now = self._now()
        rows, malformed = [], []
        for row in self._read_incidents():
            try:
                rows.append(self._parse(row))
            except (KeyError, TypeError, ValueError):
                malformed.append(self._malformed_key(row))
        created = []
        with self._journal() as db:
            for key in malformed:
                if not db.execute("SELECT 1 FROM events WHERE incident_key=? AND "
                                  "kind='malformed_incident'", (key,)).fetchone():
                    self._event(db, key, "malformed_incident", None, now,
                                condition="malformed incident row skipped")
            for key, reason, at, generation in rows:
                if db.execute("INSERT OR IGNORE INTO jobs VALUES (?, ?, ?, ?, ?, 'pending', ?, 0, 0)",
                              (key, reason, at, generation, self.config.digest,
                               now.isoformat())).rowcount:
                    self._event(db, key, "detected", None, at, journaled_at=now.isoformat())
                    created.append(key)
        return tuple(created)

    # -- publication -----------------------------------------------------------------------

    def run_once(self):
        """Poll, then always publish due jobs; a poll failure re-raises after publishing."""
        try:
            self.poll()
        except Exception as exc:  # noqa: BLE001 - re-raised below once due jobs are published
            self.publish_due()
            raise exc
        self.publish_due()

    def publish_due(self):
        now = self._now()
        with self._journal() as db:
            due = db.execute("SELECT incident_key, reason, detected_at, rounds, channels_lost, "
                             "next_attempt_at FROM jobs WHERE state='pending' ORDER BY rowid"
                             ).fetchall()
        for key, reason, detected_at, rounds, lost, next_at in due:
            if datetime.fromisoformat(next_at) <= now:
                self._publish_round(key, reason, detected_at, rounds, lost, now)

    def _publish_round(self, key, reason, detected_at, rounds, lost, now):
        payload = {"kind": "book_incident", "idempotency_key": key, "reason": reason,
                   "detected_at": detected_at}
        assert_no_secrets(payload)
        accepted = delivered = False
        for position, channel in enumerate(self._channels, 1):
            with self._journal() as db:
                self._event(db, key, "attempt", channel.name, now)
            result, failure = self._bounded_publish(channel, key, payload)
            delivers = CHANNEL_KINDS[channel.kind][1]
            # The outcome that ends the round commits with the job update, so a crash can never
            # leave a durable delivered event on a job still due for republish.
            with self._journal() as db:
                if result is None or result.state != "accepted":
                    self._event(db, key, "delivery_failed", channel.name, now,
                                outcome=failure or result.state)
                elif not delivers:
                    self._event(db, key, "local_evidence", channel.name, now,
                                evidence_digest=result.evidence_digest)
                else:
                    self._event(db, key, "provider_accepted", channel.name, now,
                                evidence_digest=result.evidence_digest)
                    accepted, delivered = True, result.delivered
                    if delivered:
                        self._event(db, key, "delivered", channel.name, now,
                                    evidence_digest=result.evidence_digest)
                if accepted or position == len(self._channels):
                    self._close_round(db, key, rounds + 1, lost, accepted, delivered, now)
            if accepted:
                break

    def _close_round(self, db, key, rounds, lost, accepted, delivered, now):
        delay = min(self.config.retry_initial_s * 2 ** min(rounds - 1, 62), self.config.retry_max_s)
        if not accepted and not lost:
            self._event(db, key, "all_channels_lost", None, now, condition="ALL_CHANNELS_LOST")
        elif accepted and lost:
            self._event(db, key, "channels_restored", None, now)
        db.execute("UPDATE jobs SET state=?, next_attempt_at=?, rounds=?, channels_lost=? "
                   "WHERE incident_key=?",
                   ("delivered" if delivered else "pending",
                    (now + timedelta(seconds=delay)).isoformat(), rounds,
                    0 if accepted else 1, key))

    def _bounded_publish(self, channel, key, payload):
        box = {}

        def call():
            try:
                box["result"] = channel.publish(key, dict(payload))
            except BaseException as exc:  # noqa: BLE001 - any channel failure is a failed attempt
                box["error"] = exc

        worker = threading.Thread(target=call, name="book-incident-publish", daemon=True)
        worker.start()
        worker.join(self.config.publish_timeout_s)
        if worker.is_alive():
            return None, "timeout"
        if "error" in box:
            return None, type(box["error"]).__name__
        if not isinstance(box.get("result"), PublishResult):
            return None, "invalid_result"
        return box["result"], None

    def record_delivery(self, key, channel, evidence_digest):
        """Append out-of-band delivery evidence (e.g. a provider receipt) and close the job."""
        if channel not in {item.name for item in self._channels if CHANNEL_KINDS[item.kind][1]}:
            raise ValueError("unknown or non-delivering channel")
        if not isinstance(evidence_digest, str) or not _DIGEST.match(evidence_digest):
            raise ValueError("evidence digest must be a sha256 hex digest")
        now = self._now()
        with self._journal() as db:
            if db.execute("UPDATE jobs SET state='delivered' WHERE incident_key=?",
                          (key,)).rowcount != 1:
                raise ValueError("unknown incident key")
            self._event(db, key, "delivered", channel, now, evidence_digest=evidence_digest)

    # -- reads -----------------------------------------------------------------------------

    def jobs(self):
        with self._journal() as db:
            return tuple({"incident_key": row[0], "reason": row[1], "detected_at": row[2],
                          "generation": row[3], "config_digest": row[4], "state": row[5],
                          "next_attempt_at": row[6], "rounds": row[7],
                          "channels_lost": bool(row[8])}
                         for row in db.execute("SELECT * FROM jobs ORDER BY rowid").fetchall())

    def events(self, key=None):
        with self._journal() as db:
            rows = db.execute("SELECT sequence, incident_key, kind, channel, at, detail FROM events "
                              "WHERE ? IS NULL OR incident_key=? ORDER BY sequence",
                              (key, key)).fetchall()
        return tuple({"sequence": row[0], "incident_key": row[1], "kind": row[2],
                      "channel": row[3], "at": row[4], "detail": json.loads(row[5])}
                     for row in rows)

    def channels_lost(self):
        """Keys whose latest round lost every channel (ALL_CHANNELS_LOST); recorded only."""
        with self._journal() as db:
            return tuple(row[0] for row in db.execute(
                "SELECT incident_key FROM jobs WHERE channels_lost=1 AND state='pending' "
                "ORDER BY rowid").fetchall())
