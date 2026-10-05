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

Outbox (card §0.5 item 4): the halt/resume owner ruled on 2026-10-03 that this journal plus
the bounded publish is HR :61's notification outbox, under four conditions. (1) The
idempotency key derives only from the committed ``incident_id``. (2) No import path reaches
a broker, order, rail-command or C-a close module. (3) Durability is not assumed: a missing
or corrupt journal is rebuilt from the owner's committed ``incidents`` rows, and a corrupt
one is moved aside, never deleted. (4) ``progress()``, a count of clean loops that never goes
back, lets the external missed-heartbeat monitor cover this notifier; the notifier sends no
heartbeat itself.

Bounded publish (relay review P2 on #628): a publish that outlives its timeout keeps running on
its daemon thread, never killed. A (job, channel) pair holds at most one live publish, and all
pairs together at most ``MAX_OUTSTANDING_PUBLISHES``. A refused channel fails for the round.
A late outcome is appended as evidence under the same closing guard as ``record_delivery``.

Job state (card §0.8, relay re-review P2 on #628): a job is ``pending`` until delivered, and
delivered is terminal. Every writer re-reads the job through ``_pending`` inside the transaction
that writes; only ``_transition`` updates a job after ``poll`` creates it, and one round runs at
a time. A job that is not pending gets nothing but evidence: no attempt, no publish, no round
state and no second ``delivered``.

Out of this build (card §8): any concrete provider binding, the 60 s alternate-channel
escalation, acting on ``ALL_CHANNELS_LOST``, the external heartbeat and attendance.
"""
from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from contextlib import closing, contextmanager
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
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
# HR :59 escalates 60 s after the first attempt without acknowledgment; the retry backoff
# cap stays below it so every escalation interval holds a retry (owner ruling 2026-10-03).
ESCALATION_STEP_S = 60.0
# Live publishes across all (job, channel) pairs. Each channel without a live publish keeps
# one slot reserved, so a hung channel cannot starve a healthy one; the config therefore
# refuses more channels than this. Card §0.7 justifies the value.
MAX_OUTSTANDING_PUBLISHES = 8
# kind -> (needs a secret reference, delivers). grafana_irm is the D-MON-1 binding
# (ops/c1_rail/book_incident_grafana_irm.py); this module never imports it.
# A non-delivering kind (local_file) is evidence only: its acceptance never ends a round,
# never counts against ALL_CHANNELS_LOST and never closes a job (card §3.3).
CHANNEL_KINDS = {"fake": (True, True), "local_file": (False, False),
                 "grafana_irm": (True, True)}
_SECRET_REF = re.compile(r"^(env|secret):[A-Z][A-Z0-9_]{0,63}$")
_NAME = re.compile(r"^[a-z][a-z0-9_-]{0,31}$")
_DIGEST = re.compile(r"^[0-9a-f]{64}$")
_CONFIG_KEYS = {"channels", "publish_timeout_s", "retry_initial_s", "retry_max_s",
                "max_jobs_per_round", "max_retained_incidents"}
_CHANNEL_KEYS = {"name", "kind", "secret_ref"}
_JOURNAL = (
    "CREATE TABLE IF NOT EXISTS jobs (incident_key TEXT PRIMARY KEY, reason TEXT NOT NULL, "
    "detected_at TEXT NOT NULL, generation INTEGER NOT NULL, config_digest TEXT NOT NULL, "
    "state TEXT NOT NULL, next_attempt_at TEXT NOT NULL, rounds INTEGER NOT NULL, "
    "channels_lost INTEGER NOT NULL)",
    "CREATE TABLE IF NOT EXISTS events (sequence INTEGER PRIMARY KEY AUTOINCREMENT, "
    "incident_key TEXT, kind TEXT NOT NULL, channel TEXT, at TEXT NOT NULL, "
    "detail TEXT NOT NULL)",
)
_SIDECARS = ("-journal", "-wal", "-shm")


def _journal_schema(db):
    """Table name -> column definitions, without SQLite's internal tables."""
    return {name: tuple(db.execute("SELECT * FROM pragma_table_info(?)", (name,)).fetchall())
            for (name,) in db.execute("SELECT name FROM sqlite_master WHERE type='table' "
                                      "AND name NOT LIKE 'sqlite_%'").fetchall()}


def _expected_schema():
    with closing(sqlite3.connect(":memory:")) as db:
        for statement in _JOURNAL:
            db.execute(statement)
        return _journal_schema(db)


_JOURNAL_SCHEMA = _expected_schema()


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
    retry_max_s: float = 30.0
    # Job rounds per pass (card NF1); the host binding floors it at 8 (OQ-NF-3 ruling (a)).
    max_jobs_per_round: int = 10
    # Owner rows above which poll records one over-bound event per crossing (card NF4).
    max_retained_incidents: int = 1000
    digest: str = field(init=False, compare=False)

    def __post_init__(self):
        if (not isinstance(self.channels, tuple) or not self.channels
                or not all(isinstance(spec, ChannelSpec) for spec in self.channels)):
            raise NotifierConfigError("at least one channel spec required")
        if len({spec.name for spec in self.channels}) != len(self.channels):
            raise NotifierConfigError("channel names must be unique")
        if len(self.channels) > MAX_OUTSTANDING_PUBLISHES:
            raise NotifierConfigError("more channels than MAX_OUTSTANDING_PUBLISHES")
        if not any(CHANNEL_KINDS[spec.kind][1] for spec in self.channels):
            raise NotifierConfigError("at least one delivering channel required")
        for name in ("publish_timeout_s", "retry_initial_s", "retry_max_s"):
            value = getattr(self, name)
            if (isinstance(value, bool) or not isinstance(value, (int, float))
                    or not math.isfinite(value) or value <= 0):
                raise NotifierConfigError(name + " must be a positive finite number")
        if self.retry_initial_s > self.retry_max_s:
            raise NotifierConfigError("retry_initial_s exceeds retry_max_s")
        if self.retry_max_s >= ESCALATION_STEP_S:
            raise NotifierConfigError("retry_max_s must be below the 60 s escalation step")
        for name in ("max_jobs_per_round", "max_retained_incidents"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value < 1:
                raise NotifierConfigError(name + " must be a positive integer")
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
                "retry_max_s": self.retry_max_s,
                "max_jobs_per_round": self.max_jobs_per_round,
                "max_retained_incidents": self.max_retained_incidents}


class IncidentNotifier:
    """Turns committed owner incidents into durable jobs and publishes them.

    ``read_incidents`` returns the owner's committed rows (``incident_id``, ``reason``,
    ``at``, ``generation``); ``clock`` returns an aware ``datetime``.
    """

    def __init__(self, store_path, *, read_incidents: Callable[[], Iterable[Mapping]],
                 channels: Mapping[str, Channel], config: NotifierConfig,
                 clock: Callable[[], datetime], rebuild: bool = True):
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
        self._last_loop_at = None
        self._progress = 0  # card NF6: clean, non-loud run_once calls; never decreases
        self._rebuild = rebuild  # card NF7: False opens an existing journal only, never rebuilds
        self._over_bound = False  # card NF4: the last committed poll read more than M rows
        self._publish_lock = threading.Lock()
        self._round_lock = threading.Lock()  # J0: one round at a time
        self._publishes = {}  # (incident key, channel name) -> Event set when the publish ends
        fault = self._journal_fault()
        if fault and not rebuild:
            raise NotifierStoreError("notifier journal faulty: " + fault)
        now = self._now() if fault else None
        moved = self._move_aside(now) if fault else None
        with self._journal() as db:
            if not rebuild and _journal_schema(db) != _JOURNAL_SCHEMA:
                raise NotifierStoreError("notifier journal is not initialized")
            for statement in _JOURNAL:
                db.execute(statement)
            if fault:
                self._event(db, None, "journal_rebuilt", None, now, cause=fault, moved_to=moved)
            # Card NF4: keys already journaled, in every state; poll inserts only new keys.
            self._known = {key for (key,) in db.execute("SELECT incident_key FROM jobs")}

    # -- journal ---------------------------------------------------------------------------

    @contextmanager
    def _journal(self):
        """One short serialized transaction on the notifier's own journal, never the owner DB.

        The journal is a registered durable store (``scripts/check_durable_store_pragmas.py``):
        ``synchronous=FULL`` and an immediate transaction, on this file only.
        """
        try:
            db = self._connect()
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

    def _connect(self):
        """Open the journal (card D2). ``rebuild=False`` opens an existing file only
        (``mode=rw``), so it creates no file or directory; every connection is
        ``synchronous=FULL``."""
        if self._rebuild:
            self.store_path.parent.mkdir(parents=True, exist_ok=True)
            db = sqlite3.connect(self.store_path, timeout=5, isolation_level=None)
        else:
            db = sqlite3.connect(self.store_path.resolve().as_uri() + "?mode=rw", uri=True,
                                 timeout=5, isolation_level=None)
        try:
            db.execute("PRAGMA synchronous=FULL")
        except BaseException:
            db.close()
            raise
        return db

    def _journal_fault(self):
        """Why an existing journal cannot be trusted, or None (condition 3).

        A missing or empty file is a fresh journal. Unreadable bytes, a schema other than
        ``_JOURNAL`` or a failed ``integrity_check`` is a fault. A journal that cannot be
        opened at all (a directory, a lock, a permission) is unavailable and raises, so a
        transient error never moves a journal aside.
        """
        if not self.store_path.is_file():
            return None
        try:
            with closing(self._connect()) as db:
                db.execute("PRAGMA synchronous=FULL")  # writable: a hot journal may roll back
                if db.execute("PRAGMA integrity_check").fetchall() != [("ok",)]:
                    return "integrity"
                schema = _journal_schema(db)
        except sqlite3.OperationalError as exc:
            raise NotifierStoreError("notifier journal unavailable") from exc
        except sqlite3.DatabaseError:
            return "unreadable"
        return None if schema in ({}, _JOURNAL_SCHEMA) else "schema"

    def _move_aside(self, now):
        """Rename a faulty journal and its SQLite sidecars to a timestamped name; never delete.

        The jobs are then re-derived from the owner's committed ``incidents`` rows by the next
        poll, and the stable incident key lets a provider group any republish (condition 3).
        """
        stamp = now.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        name, attempt = "%s.corrupt-%s" % (self.store_path.name, stamp), 0
        while any(self.store_path.with_name(name + suffix).exists() for suffix in ("",) + _SIDECARS):
            attempt += 1
            name = "%s.corrupt-%s-%d" % (self.store_path.name, stamp, attempt)
        try:
            for suffix in ("",) + _SIDECARS:
                source = self.store_path.with_name(self.store_path.name + suffix)
                if source.exists():
                    os.rename(source, self.store_path.with_name(name + suffix))
        except OSError as exc:
            raise NotifierStoreError("notifier journal could not be moved aside") from exc
        return name

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
        """Opaque key for a malformed row: its incident key if the id is usable, else a digest."""
        try:
            return incident_key(row["incident_id"])
        except (KeyError, TypeError, ValueError):
            return hashlib.sha256(INCIDENT_KEY_DOMAIN + b"malformed\x00"
                                  + repr(row).encode("utf-8")).hexdigest()

    def poll(self):
        """Create one job per committed incident not yet journaled; return the new keys.

        A malformed row still gets a job (reason ``malformed``, detected at the journal time,
        generation 0) so the operator is notified, plus one ``malformed_incident`` evidence
        event; its raw id is never journaled or sent, and it never blocks the other rows.
        """
        now = self._now()
        entries = []
        for row in self._read_incidents():
            try:
                entries.append(self._parse(row) + (False,))
            except (KeyError, TypeError, ValueError):
                entries.append((self._malformed_key(row), "malformed", now.isoformat(), 0, True))
        created, present = [], []
        over = len(entries) > self.config.max_retained_incidents
        with self._journal() as db:  # opened on every call (card NF8 counts it)
            for key, reason, at, generation, malformed in entries:
                if key in self._known:
                    continue
                if db.execute("INSERT OR IGNORE INTO jobs VALUES (?, ?, ?, ?, ?, 'pending', ?, 0, 0)",
                              (key, reason, at, generation, self.config.digest,
                               now.isoformat())).rowcount:
                    if malformed:
                        self._event(db, key, "malformed_incident", None, now,
                                    condition="malformed incident row")
                    self._event(db, key, "detected", None, at, journaled_at=now.isoformat())
                    created.append(key)
                present.append(key)
            if over and not self._over_bound:
                self._event(db, None, "retained_incidents_over_bound", None, now,
                            count=len(entries))
        # Card NF4: known keys and the crossing state change only after the COMMIT.
        self._known.update(present)
        self._over_bound = over
        return tuple(created)

    # -- publication -----------------------------------------------------------------------

    def run_once(self):
        """Poll, then always publish due jobs; a poll failure re-raises after publishing.

        Only a loop that completes without raising and without a loud pass (card NF3)
        refreshes ``liveness()`` and increments ``progress()``.
        """
        try:
            self.poll()
        except Exception as exc:  # noqa: BLE001 - re-raised below once due jobs are published
            self.publish_due()
            raise exc
        if self.publish_due():
            return
        self._last_loop_at = self._now()
        self._progress += 1

    def liveness(self):
        """Clock time of the last ``run_once`` that completed without raising, or None.

        A loud pass (card NF3) does not refresh it. It follows the caller's clock, which can
        step back; a heartbeat marks on ``progress()`` instead. Reading it runs no loop and
        sends nothing; the notifier never sends a heartbeat itself.
        """
        return self._last_loop_at

    def progress(self):
        """Count of ``run_once`` calls that completed without raising and without a loud pass.

        Card NF6 and condition 4: starts at 0 and never decreases, whatever the clock does. The
        external missed-heartbeat monitor's wrapper marks on an increase here.
        """
        return self._progress

    def publish_due(self):
        """At most ``max_jobs_per_round`` rounds, one round at a time (card §0.8 J0; NF1-NF3).

        The snapshot only nominates jobs, the first k due pending jobs in ``_nominate``'s
        order: each channel's admission re-reads the job (J2), so a job closed after the
        snapshot, by any writer, is skipped, never republished and never replaced. Deferring
        a due job writes one ``cap_deferred`` event in the snapshot transaction. Returns True
        when a due class-U job was deferred (a loud pass), else False.
        """
        with self._round_lock:
            now = self._now()
            with self._journal() as db:
                rows = db.execute("SELECT rowid, incident_key, generation, state, reason, "
                                  "detected_at, next_attempt_at, rounds, channels_lost "
                                  "FROM jobs ORDER BY rowid").fetchall()
                nominated, unaccepted, accepted = self._nominate(
                    rows, now, self.config.max_jobs_per_round)
                if unaccepted or accepted:
                    self._event(db, None, "cap_deferred", None, now,
                                unaccepted=unaccepted, accepted=accepted)
            for key, reason, detected_at in nominated:
                self._publish_round(key, {"kind": "book_incident", "idempotency_key": key,
                                          "reason": reason, "detected_at": detected_at}, now)
            return unaccepted > 0

    @staticmethod
    def _nominate(rows, now, k):
        """Card NF2 and NF5: the first k due pending jobs and the deferred counts per class.

        ``rows`` is every job in ``rowid`` order (no LIMIT). A halt sequence is a generation
        run: a job continues the previous job's sequence when that job's generation is at least
        1 and its own is exactly one more (card §0.5 item 12). A sequence has an accepted page
        once any of its jobs is delivered or class A. Class U (``rounds = 0`` or the latest
        round lost every channel) sorts by (tier, due, ``rowid``): tier 0 is the due first job
        of a sequence with no accepted page, tier 1 such a sequence's earliest-due class-U job
        when its first job is not due, tier 2 every other class-U job. Class A follows by
        (due, ``rowid``). Due times compare as parsed instants, never as text.
        """
        sequence, paged, previous, current = {}, set(), None, None
        for rowid, _key, generation, state, _reason, _at, _next, rounds, lost in rows:
            if previous is None or previous < 1 or generation != previous + 1:
                current = rowid
            sequence[rowid], previous = current, generation
            if state == "delivered" or (rounds > 0 and not lost):
                paged.add(current)
        unaccepted, accepted = [], []
        for rowid, key, _generation, state, reason, detected_at, next_at, rounds, lost in rows:
            if state != "pending":
                continue
            due = datetime.fromisoformat(next_at)
            if due <= now:
                item = (due, rowid, key, reason, detected_at)
                (unaccepted if rounds == 0 or lost else accepted).append(item)
        tiers = {}
        for item in unaccepted:  # rowid order: a sequence's first job comes first
            first = sequence[item[1]]
            if first in paged:
                continue
            if item[1] == first:
                tiers[first] = (0, item)
            elif first not in tiers or (tiers[first][0] == 1 and item[:2] < tiers[first][1][:2]):
                tiers[first] = (1, item)
        tier = {item[1]: number for number, item in tiers.values()}
        queue = (sorted(unaccepted, key=lambda item: (tier.get(item[1], 2), item[0], item[1]))
                 + sorted(accepted, key=lambda item: item[:2]))
        taken = min(len(unaccepted), k)
        return ([item[2:] for item in queue[:k]], len(unaccepted) - taken,
                len(accepted) - min(len(accepted), k - taken))

    def _publish_round(self, key, payload, now):
        assert_no_secrets(payload)
        for position, channel in enumerate(self._channels, 1):
            last = position == len(self._channels)
            # Admission (J2): the job must still be pending in the transaction that writes its
            # attempt or refusal, or nothing is recorded and the round ends. A refused channel
            # sends nothing and fails for the round (ALL_CHANNELS_LOST counts it).
            with self._journal() as db:
                job = self._pending(db, key)
                if job is None:
                    return
                refused = self._refusal(key, channel)
                self._event(db, key, refused or "attempt", channel.name, now)
                if refused and last:
                    self._transition(db, key, job, now, round_accepted=False)
            if refused:
                continue
            result, failure = self._bounded_publish(channel, key, payload)
            delivers = CHANNEL_KINDS[channel.kind][1]
            accepted = delivers and result is not None and result.state == "accepted"
            # Close (J3): the outcome is always evidence. Round state and delivery go through
            # _transition, which writes nothing for a job closed while this publish was in
            # flight; a crash can never leave a delivered event on a job still due.
            with self._journal() as db:
                if result is None or result.state != "accepted":
                    self._event(db, key, "delivery_failed", channel.name, now,
                                outcome=failure or result.state)
                else:
                    self._event(db, key, "provider_accepted" if delivers else "local_evidence",
                                channel.name, now, evidence_digest=result.evidence_digest)
                if accepted or last:
                    self._transition(db, key, self._pending(db, key), now,
                                     round_accepted=accepted,
                                     delivered=(channel.name, result.evidence_digest)
                                     if accepted and result.delivered else None)
            if accepted:
                return

    @staticmethod
    def _pending(db, key):
        """The job guard (card §0.8), read in the caller's write transaction: the pending job's
        ``(rounds, channels_lost)``, or None for a delivered or unknown job."""
        return db.execute("SELECT rounds, channels_lost FROM jobs WHERE incident_key=? "
                          "AND state='pending'", (key,)).fetchone()

    def _transition(self, db, key, job, now, *, round_accepted=None, delivered=None):
        """The only job update after ``poll`` creates it, in the caller's transaction.

        ``job`` is ``_pending``'s row from that transaction; None writes nothing, so delivered
        is terminal. ``delivered`` is ``(channel, evidence_digest)`` and writes the job's one
        ``delivered`` event. ``round_accepted`` closes a round (rounds, backoff, channel loss)
        from the re-read row; None (a late outcome, ``record_delivery``) keeps round state.
        """
        if job is None:
            return
        rounds, lost = job
        next_at = None
        if delivered is not None:
            self._event(db, key, "delivered", delivered[0], now, evidence_digest=delivered[1])
        if round_accepted is not None:
            rounds += 1
            delay = min(self.config.retry_initial_s * 2 ** min(rounds - 1, 62),
                        self.config.retry_max_s)
            if not round_accepted and not lost:
                self._event(db, key, "all_channels_lost", None, now, condition="ALL_CHANNELS_LOST")
            elif round_accepted and lost:
                self._event(db, key, "channels_restored", None, now)
            lost, next_at = int(not round_accepted), (now + timedelta(seconds=delay)).isoformat()
        db.execute("UPDATE jobs SET state=?, rounds=?, channels_lost=?, "
                   "next_attempt_at=COALESCE(?, next_attempt_at) "
                   "WHERE incident_key=? AND state='pending'",
                   ("pending" if delivered is None else "delivered", rounds, lost, next_at, key))

    def _refusal(self, key, channel):
        """Why ``channel`` may not start a publish for ``key`` now, or None.

        A pair whose publish is still live is ``publish_in_flight``. Otherwise the publish must
        fit under ``MAX_OUTSTANDING_PUBLISHES`` beside one reserved slot for every other channel
        with no live publish, or it is ``publish_capacity_exhausted``.
        """
        with self._publish_lock:
            self._publishes = {pair: done for pair, done in self._publishes.items()
                               if not done.is_set()}
            if (key, channel.name) in self._publishes:
                return "publish_in_flight"
            busy = {name for _key, name in self._publishes}
            reserved = sum(other.name not in busy for other in self._channels if other is not channel)
            if len(self._publishes) + 1 + reserved > MAX_OUTSTANDING_PUBLISHES:
                return "publish_capacity_exhausted"
        return None

    def _bounded_publish(self, channel, key, payload):
        box, done = {}, threading.Event()

        def call():
            try:
                outcome = channel.publish(key, dict(payload)), None
            except BaseException as exc:  # noqa: BLE001 - any channel failure is a failed attempt
                outcome = None, exc
            try:
                with self._publish_lock:  # exactly one of the round and this thread records it
                    box["outcome"] = outcome
                    late = "abandoned" in box
                if late:
                    self._record_late(channel, key, *self._classify(*outcome))
            finally:
                done.set()

        worker = threading.Thread(target=call, name="book-incident-publish", daemon=True)
        worker.start()
        with self._publish_lock:
            self._publishes[(key, channel.name)] = done
        worker.join(self.config.publish_timeout_s)
        with self._publish_lock:
            if "outcome" not in box:
                box["abandoned"] = True
                return None, "timeout"
        return self._classify(*box["outcome"])

    @staticmethod
    def _classify(result, error):
        if error is not None:
            return None, type(error).__name__
        if not isinstance(result, PublishResult):
            return None, "invalid_result"
        return result, None

    def _record_late(self, channel, key, result, failure):
        """Append the outcome of a publish that outlived its timeout, as evidence only.

        Rounds, backoff and channel loss stay the round's. Delivery evidence closes a pending
        job through ``_transition`` (J4); a closed job gets no second ``delivered``. A journal
        failure is swallowed, since a daemon thread must not raise: the job stays as it was and
        the next round republishes under the same key.
        """
        try:
            now = self._now()
            with self._journal() as db:
                if db.execute("SELECT 1 FROM jobs WHERE incident_key=?", (key,)).fetchone():
                    self._event(db, key, "late_outcome", channel.name, now,
                                outcome=failure or result.state,
                                delivered=result is not None and result.delivered,
                                evidence_digest=None if result is None else result.evidence_digest)
                    if result is not None and result.delivered and CHANNEL_KINDS[channel.kind][1]:
                        self._transition(db, key, self._pending(db, key), now,
                                         delivered=(channel.name, result.evidence_digest))
        except Exception:  # noqa: BLE001 - see the docstring
            pass

    def record_delivery(self, key, channel, evidence_digest):
        """Append out-of-band delivery evidence (e.g. a provider receipt) and close the job.

        Idempotent (J5): a job that is already delivered gets no second ``delivered`` event.
        """
        if channel not in {item.name for item in self._channels if CHANNEL_KINDS[item.kind][1]}:
            raise ValueError("unknown or non-delivering channel")
        if not isinstance(evidence_digest, str) or not _DIGEST.match(evidence_digest):
            raise ValueError("evidence digest must be a sha256 hex digest")
        now = self._now()
        with self._journal() as db:
            if db.execute("SELECT 1 FROM jobs WHERE incident_key=?", (key,)).fetchone() is None:
                raise ValueError("unknown incident key")
            self._transition(db, key, self._pending(db, key), now,
                             delivered=(channel, evidence_digest))

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
