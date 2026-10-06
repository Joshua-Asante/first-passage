"""Operator CLI: ``record-delivery`` records Joshua's acknowledgment of a page as delivery.

Card: docs/briefs/handoffs/2026-10-03-dmon-grafana-irm-binding-card-DRAFT.md (FROZEN 2026-10-04),
§3.7, invariants C1-C7 (OQ-1 RULED YES). Operating sequence: acknowledge in IRM, run this with
the live-page driver's journal and ``notifier-config.json``, wait for ``safe to resolve (rail
side)``, and only then resolve the alert group. ``safe`` closes the rail-side window only; the
provider-side residual (C6, OQ-6) stays open.

C1: imports only the stdlib and ``book_incident_notifier``. It never imports a channel module,
resolves no secret reference, makes no HTTP request, never runs a round and has no broker,
dispatch, arm or owner path. The recorded digest is operator-reported acknowledgment, not
authenticated attendance (TB-I3).
"""
from __future__ import annotations

import argparse
from contextlib import closing
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import sqlite3
import sys
import time

if not __package__:  # run as a script: the notifier sits beside this file
    sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from .book_incident_notifier import (
        _JOURNAL_SCHEMA, CHANNEL_KINDS, IncidentNotifier, NotifierConfig, NotifierConfigError,
        NotifierStoreError, _journal_schema)
except ImportError:
    from book_incident_notifier import (
        _JOURNAL_SCHEMA, CHANNEL_KINDS, IncidentNotifier, NotifierConfig, NotifierConfigError,
        NotifierStoreError, _journal_schema)


ACK_DOMAIN = b"first-passage/book-incident-operator-ack/v1\x00"
SAFE = "safe to resolve (rail side)"
NOT_SAFE = "not safe; wait and re-run"
ALREADY = "already delivered"
REFUSED, UNSAFE = 2, 3
LOCK_WAIT_S = 5
POLL_S = 0.2
_KEY = re.compile(r"^[0-9a-f]{64}$")


class Refusal(Exception):
    """A C3 check failed; ``check`` names it. No event is written."""

    def __init__(self, check, detail=""):
        super().__init__(check)
        self.check, self.detail = check, detail


class _InertChannel:
    """Carries a spec's name and kind for the constructor's check (C4); never publishes."""

    def __init__(self, name, kind):
        self.name, self.kind = name, kind

    def publish(self, idempotency_key, payload):  # noqa: ARG002
        raise RuntimeError("record-delivery never publishes")


def _no_incidents():
    raise RuntimeError("record-delivery never reads owner incidents")


def _read_only(journal):
    """C3 item 3's read-only open: no rollback, no create, no move-aside."""
    return sqlite3.connect(Path(journal).resolve().as_uri() + "?mode=ro", uri=True,
                           timeout=LOCK_WAIT_S, isolation_level=None)


def _store_check(exc):
    return "journal-lock" if "locked" in str(exc).lower() else "journal-faulty"


def _load_config(path, channel):
    """C3 item 1: a valid config and exactly one named delivering channel."""
    try:
        config = NotifierConfig.from_mapping(json.loads(Path(path).read_text(encoding="utf-8")))
    except (OSError, ValueError, NotifierConfigError) as exc:
        raise Refusal("config", type(exc).__name__) from None
    delivering = [spec.name for spec in config.channels if CHANNEL_KINDS[spec.kind][1]]
    if channel is None:
        if len(delivering) != 1:
            raise Refusal("channel", "more than one delivering channel; name one with --channel")
        channel = delivering[0]
    elif channel not in delivering:
        raise Refusal("channel", "not a delivering channel in the config")
    return config, channel


def _precheck(journal, key, channel, config_digest):
    """C3 items 2-5 on a read-only open; returns the job's state.

    The supplied config must be the one the job was journaled under (its digest), so its
    channel roles are the notifier's (review r4179168634).
    """
    path = Path(journal)
    if not path.is_file():
        raise Refusal("journal-missing")
    try:
        with closing(_read_only(path)) as db:
            if (db.execute("PRAGMA integrity_check").fetchall() != [("ok",)]
                    or _journal_schema(db) != _JOURNAL_SCHEMA):
                raise Refusal("journal-faulty")
            if not _KEY.match(key):
                raise Refusal("key-unknown", "not 64 lowercase hex")
            job = db.execute("SELECT state, config_digest FROM jobs WHERE incident_key=?",
                             (key,)).fetchone()
            if job is None:
                raise Refusal("key-unknown")
            if job[1] != config_digest:
                raise Refusal("config-mismatch", "not the config this job was journaled under")
            if db.execute("SELECT 1 FROM events WHERE incident_key=? AND channel=? "
                          "AND kind='attempt'", (key, channel)).fetchone() is None:
                raise Refusal("no-attempt", "no page went out on this channel")
            if any(_failure_outcome(detail) is None for (detail,) in db.execute(
                    "SELECT detail FROM events WHERE incident_key=? AND channel=? "
                    "AND kind='delivery_failed'", (key, channel))):
                raise Refusal("journal-faulty", "malformed delivery_failed detail")
            return job[0]
    except sqlite3.Error as exc:
        raise Refusal(_store_check(exc), type(exc).__name__) from None


def _failure_outcome(detail):
    """A delivery_failed detail's ``outcome``, or None unless it is a JSON object holding a
    string outcome, as the notifier journals it (``_publish_round``)."""
    try:
        parsed = json.loads(detail)
    except (TypeError, ValueError):
        return None
    outcome = parsed.get("outcome") if isinstance(parsed, dict) else None
    return outcome if isinstance(outcome, str) else None


def _closed(journal, key, channel):
    """C5: the job is delivered and the last attempt on (key, channel) has a later close.

    A close is ``provider_accepted``, ``delivery_failed`` other than ``timeout``, or
    ``late_outcome``; a ``delivery_failed`` {timeout} publish may still be running. A read
    error counts as not safe.
    """
    try:
        with closing(_read_only(journal)) as db:
            state = db.execute("SELECT state FROM jobs WHERE incident_key=?", (key,)).fetchone()
            if state != ("delivered",):
                return False
            rows = db.execute("SELECT kind, detail FROM events WHERE incident_key=? AND channel=? "
                              "ORDER BY sequence", (key, channel)).fetchall()
    except sqlite3.Error:
        return False
    last = max((index for index, (kind, _) in enumerate(rows) if kind == "attempt"), default=None)
    if last is None:
        return False
    for kind, detail in rows[last + 1:]:
        if kind in ("provider_accepted", "late_outcome"):
            return True
        outcome = _failure_outcome(detail) if kind == "delivery_failed" else None
        if outcome is not None and outcome != "timeout":  # a malformed row is never a close
            return True
    return False


def _delivered_digest(journal, key):
    """The evidence digest of the job's one delivered event, or None."""
    try:
        with closing(_read_only(journal)) as db:
            row = db.execute("SELECT detail FROM events WHERE incident_key=? AND kind='delivered'"
                             " ORDER BY sequence LIMIT 1", (key,)).fetchone()
    except sqlite3.Error:
        return None
    return None if row is None else json.loads(row[0]).get("evidence_digest")


def record_delivery(journal, config_path, key, *, channel=None, wait_s=120.0, out=print):
    """Record, then wait for the rail-side close (C2-C5). Returns the exit status."""
    if isinstance(wait_s, bool) or not isinstance(wait_s, (int, float)) or not (
            math.isfinite(wait_s) and wait_s > 0):
        raise Refusal("wait-s", "must be a finite number of seconds above 0")
    config, channel = _load_config(config_path, channel)
    state = _precheck(journal, key, channel, config.digest)
    if state == "delivered":
        out(ALREADY)
    else:
        recorded_at = datetime.now(timezone.utc).isoformat()
        digest = hashlib.sha256(ACK_DOMAIN + "\x00".join(
            (key, channel, recorded_at, "operator-reported acknowledgment")).encode("utf-8")
                                ).hexdigest()
        try:
            notifier = IncidentNotifier(
                journal, read_incidents=_no_incidents,
                channels={spec.name: _InertChannel(spec.name, spec.kind)
                          for spec in config.channels},
                config=config, clock=lambda: datetime.now(timezone.utc), rebuild=False)
            notifier.record_delivery(key, channel, digest)
        except NotifierStoreError as exc:
            raise Refusal(_store_check(exc.__cause__ or exc), "journal unavailable") from None
        # Another writer may have closed the job after the pre-check; record_delivery then
        # wrote nothing (J5), so report what the journal holds (review r4179168638).
        out("recorded delivered (operator-reported acknowledgment)"
            if _delivered_digest(journal, key) == digest else ALREADY)
    deadline = time.monotonic() + wait_s
    while True:
        if _closed(journal, key, channel):
            out(SAFE)
            return 0
        if time.monotonic() >= deadline:
            out(NOT_SAFE)
            return UNSAFE
        time.sleep(POLL_S)


def _parser():
    parser = argparse.ArgumentParser(prog="book_incident_operator_cli")
    commands = parser.add_subparsers(dest="command", required=True)
    record = commands.add_parser("record-delivery", help="record an acknowledged page as delivered")
    record.add_argument("--journal", required=True)
    record.add_argument("--config", required=True)
    record.add_argument("--channel")
    record.add_argument("--wait-s", type=float, default=120.0)
    record.add_argument("incident_key")
    return parser


def main(argv=None):
    args = _parser().parse_args(argv)
    try:
        return record_delivery(args.journal, args.config, args.incident_key,
                               channel=args.channel, wait_s=args.wait_s,
                               out=lambda line: print(line, flush=True))
    except Refusal as refusal:
        print("record-delivery refused: " + refusal.check
              + (" (" + refusal.detail + ")" if refusal.detail else ""), file=sys.stderr, flush=True)
        return REFUSED


if __name__ == "__main__":
    sys.exit(main())
