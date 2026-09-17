"""Exactly-once journal for one qualification campaign.

The journal deliberately does not run qualification work.  It only records the
two outcome-bearing stages and fences writers by boot identity.  Result
manifests and their receipts are committed in the same SQLite transaction.
"""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterator


SCHEMA_VERSION = 3
STAGES = ("TB_E1", "TB_E2_N3")
E1_CHECKPOINTS = ("N1", "CUTOFF", "N2", "PART_A")
OUTCOMES = ("PASS", "FAILURE", "UNRESOLVED")
VERDICTS = ("PENDING", "FALSIFIED", "RESOLVED", "AMBIGUOUS")
VALIDITIES = ("VALID", "VOID")
ZERO_HASH = "0" * 64
_DIGEST = re.compile(r"[0-9a-f]{64}\Z")
_VALIDATED_RESULT_TOKEN = object()


class AttemptJournalError(RuntimeError):
    """Base class for fail-closed journal errors."""


class AttemptConflict(AttemptJournalError):
    """A caller repeated an operation with different immutable inputs."""


class AttemptCorrupt(AttemptJournalError):
    """The durable journal no longer satisfies its schema or hash chain."""


class BootFenceError(AttemptJournalError):
    """A writer from a superseded process boot attempted a mutation."""


class TransitionError(AttemptJournalError):
    """A requested stage transition is not legal."""


@dataclass(frozen=True, slots=True)
class StageClaim:
    campaign_id: str
    contract_digest: str
    stage: str
    binding_sha256: str
    reservation_sequence: int
    reservation_event_digest: str
    state: str


@dataclass(frozen=True, slots=True)
class StageDispatch:
    campaign_id: str
    contract_digest: str
    stage: str
    reservation_event_digest: str
    dispatch_sequence: int
    dispatch_event_digest: str


@dataclass(frozen=True, slots=True)
class CheckpointDispatch:
    campaign_id: str
    contract_digest: str
    checkpoint: str
    parent_reservation_event_digest: str
    binding_sha256: str
    dispatch_sequence: int
    dispatch_event_digest: str


@dataclass(frozen=True, slots=True)
class ValidatedResultClaim:
    campaign_id: str
    contract_digest: str
    stage: str
    manifest_sha256: str
    outcome: str
    producer_scope: str
    attestation_digest: str
    result_stages: tuple[str, ...]
    _validation_token: object | None = field(default=None, repr=False, compare=False)


def _issue_validated_result_claim(
    *, campaign_id: str, contract_digest: str, stage: str,
    manifest_sha256: str, outcome: str, producer_scope: str,
    attestation_digest: str, result_stages: tuple[str, ...],
) -> ValidatedResultClaim:
    """Internal capability constructor used only after result authentication."""
    return ValidatedResultClaim(
        campaign_id, contract_digest, stage, manifest_sha256, outcome,
        producer_scope, attestation_digest, result_stages, _VALIDATED_RESULT_TOKEN,
    )


class _DuplicateJSONKey(ValueError):
    pass


def _closed_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise _DuplicateJSONKey(f"duplicate JSON key: {key}")
        value[key] = item
    return value


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _canonical_input(value: bytes | bytearray | memoryview, label: str) -> bytes:
    if not isinstance(value, (bytes, bytearray, memoryview)):
        raise ValueError(f"{label} must be canonical JSON bytes")
    raw = bytes(value)
    try:
        decoded = raw.decode("utf-8")
        parsed = json.loads(
            decoded, object_pairs_hook=_closed_object,
            parse_constant=lambda token: (_ for _ in ()).throw(
                ValueError(f"non-finite JSON value {token}")),
        )
        encoded = _canonical(parsed)
    except _DuplicateJSONKey as exc:
        raise ValueError(str(exc)) from exc
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError, TypeError) as exc:
        raise ValueError(f"{label} must be canonical JSON bytes") from exc
    if raw != encoded:
        raise ValueError(f"{label} must be canonical JSON bytes")
    return raw


def _instant(value: datetime) -> str:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("now must be an aware datetime")
    return value.astimezone(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def _identifier(value: str, label: str) -> str:
    if not isinstance(value, str) or not value or value.strip() != value or len(value) > 200:
        raise ValueError(f"{label} must be a non-empty bounded string")
    return value


_SCHEMA = {
    "campaign": (
        ("singleton", "INTEGER", 0, 1), ("schema_version", "INTEGER", 1, 0),
        ("campaign_id", "TEXT", 1, 0), ("contract_digest", "TEXT", 1, 0),
        ("trust_domain_sha256", "TEXT", 1, 0),
        ("boot_id", "TEXT", 1, 0), ("verdict", "TEXT", 1, 0),
        ("validity", "TEXT", 1, 0), ("void_reason", "TEXT", 0, 0),
        ("ambiguity_reason", "TEXT", 0, 0),
        ("ambiguity_evidence_digest", "TEXT", 0, 0),
        ("event_head", "TEXT", 1, 0), ("event_count", "INTEGER", 1, 0),
    ),
    "stages": (
        ("stage", "TEXT", 0, 1), ("ordinal", "INTEGER", 1, 0),
        ("state", "TEXT", 1, 0), ("binding", "BLOB", 0, 0),
        ("reserved_at", "TEXT", 0, 0), ("started_at", "TEXT", 0, 0),
        ("completed_at", "TEXT", 0, 0), ("outcome", "TEXT", 0, 0),
    ),
    "manifests": (
        ("stage", "TEXT", 0, 1), ("body", "BLOB", 1, 0),
        ("digest", "TEXT", 1, 0),
    ),
    "receipts": (
        ("stage", "TEXT", 0, 1), ("body", "BLOB", 1, 0),
        ("digest", "TEXT", 1, 0),
    ),
    "checkpoints": (
        ("checkpoint", "TEXT", 0, 1), ("ordinal", "INTEGER", 1, 0),
        ("consumed", "INTEGER", 1, 0),
        ("state", "TEXT", 1, 0), ("binding", "BLOB", 0, 0),
        ("parent_reservation_event_digest", "TEXT", 0, 0),
        ("dispatch_sequence", "INTEGER", 0, 0),
        ("dispatch_event_digest", "TEXT", 0, 0),
        ("receipt", "BLOB", 0, 0), ("receipt_digest", "TEXT", 0, 0),
    ),
    "events": (
        ("seq", "INTEGER", 0, 1), ("prev_hash", "TEXT", 1, 0),
        ("kind", "TEXT", 1, 0), ("body", "BLOB", 1, 0),
        ("occurred_at", "TEXT", 1, 0), ("event_hash", "TEXT", 1, 0),
    ),
}


class AttemptStore:
    """One immutable campaign and its two ordered qualification stages."""

    def __init__(self, path: Path, campaign_id: str, contract_digest: str, boot_id: str,
                 trust_domain_sha256: str | None = None):
        self.path = Path(path)
        self.campaign_id = campaign_id
        self.contract_digest = contract_digest
        self.trust_domain_sha256 = trust_domain_sha256
        self.boot_id = boot_id
        self._issued_checkpoint_dispatches: dict[str, CheckpointDispatch] = {}

    @classmethod
    def inspect(cls, path: str | Path) -> dict[str, Any]:
        """Validate and inspect an existing journal without claiming its boot."""
        path = Path(path).resolve()
        if not path.is_file():
            raise FileNotFoundError(path)
        db = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True, isolation_level=None)
        db.row_factory = sqlite3.Row
        try:
            campaign = db.execute("SELECT * FROM campaign WHERE singleton=1").fetchone()
            if campaign is None:
                raise AttemptCorrupt("journal has no campaign singleton")
            store = cls(
                path, campaign["campaign_id"], campaign["contract_digest"], campaign["boot_id"],
                campaign["trust_domain_sha256"],
            )
            db.execute("BEGIN")
            store._validate(db)
            stages = [store._stage_view(row) for row in db.execute(
                "SELECT * FROM stages ORDER BY ordinal"
            )]
            checkpoints = [{
                "checkpoint": row["checkpoint"], "state": row["state"],
                "binding_bytes": bytes(row["binding"]) if row["binding"] is not None else None,
                "dispatch_event_digest": row["dispatch_event_digest"],
                "receipt_bytes": bytes(row["receipt"]) if row["receipt"] is not None else None,
            } for row in db.execute("SELECT * FROM checkpoints ORDER BY ordinal")]
            return {
                "status": store._status_view(store._campaign(db)),
                "stages": stages, "checkpoints": checkpoints,
            }
        finally:
            db.close()

    @classmethod
    def open(
        cls, path: str | Path, *, campaign_id: str, contract_digest: str,
        trust_domain_sha256: str, boot_id: str, now: datetime,
    ) -> "AttemptStore":
        path = Path(path)
        campaign_id = _identifier(campaign_id, "campaign_id")
        boot_id = _identifier(boot_id, "boot_id")
        if not isinstance(contract_digest, str) or not _DIGEST.fullmatch(contract_digest):
            raise ValueError("contract_digest must be a lowercase SHA-256 digest")
        if (not isinstance(trust_domain_sha256, str)
                or not _DIGEST.fullmatch(trust_domain_sha256)):
            raise ValueError("trust_domain_sha256 must be a lowercase SHA-256 digest")
        timestamp = _instant(now)
        path.parent.mkdir(parents=True, exist_ok=True)
        store = cls(path, campaign_id, contract_digest, boot_id, trust_domain_sha256)
        with store._connection() as db:
            db.execute("BEGIN IMMEDIATE")
            tables = store._table_names(db)
            if not tables:
                store._create_schema(db)
                db.execute(
                    "INSERT INTO campaign VALUES (1,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (SCHEMA_VERSION, campaign_id, contract_digest, trust_domain_sha256,
                     boot_id, "PENDING",
                     "VALID", None, None, None, ZERO_HASH, 0),
                )
                db.executemany(
                    "INSERT INTO stages(stage,ordinal,state) VALUES (?,?,?)",
                    ((stage, ordinal, "UNRESERVED") for ordinal, stage in enumerate(STAGES, 1)),
                )
                db.executemany(
                    "INSERT INTO checkpoints(checkpoint,ordinal,state) VALUES (?,?,?)",
                    ((name, ordinal, "PENDING")
                     for ordinal, name in enumerate(E1_CHECKPOINTS, 1)),
                )
                store._append_event(db, "CAMPAIGN_CREATED", {
                    "campaign_id": campaign_id, "contract_digest": contract_digest,
                    "trust_domain_sha256": trust_domain_sha256,
                }, timestamp)
                store._append_event(db, "BOOT_CLAIMED", {"boot_id": boot_id}, timestamp)
            else:
                store._validate(db)
                row = store._campaign(db)
                if (row["campaign_id"], row["contract_digest"], row["trust_domain_sha256"]) != (
                        campaign_id, contract_digest, trust_domain_sha256):
                    raise AttemptConflict("campaign identity differs from the durable singleton")
                if row["boot_id"] != boot_id:
                    db.execute("UPDATE campaign SET boot_id=? WHERE singleton=1", (boot_id,))
                    store._append_event(db, "BOOT_CLAIMED", {"boot_id": boot_id}, timestamp)
            db.commit()
        return store

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        db = sqlite3.connect(self.path, timeout=30, isolation_level=None)
        db.row_factory = sqlite3.Row
        try:
            db.execute("PRAGMA foreign_keys=ON")
            db.execute("PRAGMA synchronous=FULL")
            yield db
        finally:
            db.close()

    @contextmanager
    def _write(self) -> Iterator[sqlite3.Connection]:
        with self._connection() as db:
            db.execute("BEGIN IMMEDIATE")
            try:
                self._validate(db)
                if self._campaign(db)["boot_id"] != self.boot_id:
                    raise BootFenceError("boot identity has been superseded")
                yield db
                db.commit()
            except BaseException:
                db.rollback()
                raise

    @contextmanager
    def _read(self) -> Iterator[sqlite3.Connection]:
        with self._connection() as db:
            db.execute("BEGIN")
            try:
                self._validate(db)
                yield db
            finally:
                db.rollback()

    @staticmethod
    def _create_schema(db: sqlite3.Connection) -> None:
        statements = (
            """CREATE TABLE campaign (
                singleton INTEGER PRIMARY KEY CHECK(singleton=1),
                schema_version INTEGER NOT NULL, campaign_id TEXT NOT NULL,
                contract_digest TEXT NOT NULL, trust_domain_sha256 TEXT NOT NULL,
                boot_id TEXT NOT NULL,
                verdict TEXT NOT NULL, validity TEXT NOT NULL, void_reason TEXT,
                ambiguity_reason TEXT, ambiguity_evidence_digest TEXT,
                event_head TEXT NOT NULL, event_count INTEGER NOT NULL
            )""",
            """CREATE TABLE stages (
                stage TEXT PRIMARY KEY, ordinal INTEGER NOT NULL UNIQUE,
                state TEXT NOT NULL, binding BLOB, reserved_at TEXT,
                started_at TEXT, completed_at TEXT, outcome TEXT
            )""",
            """CREATE TABLE manifests (
                stage TEXT PRIMARY KEY REFERENCES stages(stage),
                body BLOB NOT NULL, digest TEXT NOT NULL
            )""",
            """CREATE TABLE receipts (
                stage TEXT PRIMARY KEY REFERENCES stages(stage),
                body BLOB NOT NULL, digest TEXT NOT NULL
            )""",
            """CREATE TABLE checkpoints (
                checkpoint TEXT PRIMARY KEY, ordinal INTEGER NOT NULL UNIQUE,
                consumed INTEGER NOT NULL DEFAULT 0,
                state TEXT NOT NULL, binding BLOB,
                parent_reservation_event_digest TEXT,
                dispatch_sequence INTEGER, dispatch_event_digest TEXT,
                receipt BLOB, receipt_digest TEXT
            )""",
            """CREATE TABLE events (
                seq INTEGER PRIMARY KEY, prev_hash TEXT NOT NULL,
                kind TEXT NOT NULL, body BLOB NOT NULL, occurred_at TEXT NOT NULL,
                event_hash TEXT NOT NULL
            )""",
        )
        for statement in statements:
            db.execute(statement)
        db.execute(f"PRAGMA user_version={SCHEMA_VERSION}")

    @staticmethod
    def _table_names(db: sqlite3.Connection) -> set[str]:
        return {row[0] for row in db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )}

    def _validate(self, db: sqlite3.Connection) -> None:
        if db.execute("PRAGMA user_version").fetchone()[0] != SCHEMA_VERSION:
            raise AttemptCorrupt("unsupported journal schema version")
        if self._table_names(db) != set(_SCHEMA):
            raise AttemptCorrupt("journal schema tables differ")
        for table, expected in _SCHEMA.items():
            actual = tuple(
                (row[1], row[2].upper(), row[3], row[5])
                for row in db.execute(f"PRAGMA table_info({table})")
            )
            if actual != expected:
                raise AttemptCorrupt(f"journal schema differs for {table}")
        campaigns = db.execute("SELECT * FROM campaign").fetchall()
        if len(campaigns) != 1:
            raise AttemptCorrupt("journal must contain exactly one campaign")
        campaign = campaigns[0]
        if (campaign["singleton"] != 1 or campaign["schema_version"] != SCHEMA_VERSION
                or campaign["verdict"] not in VERDICTS
                or campaign["validity"] not in VALIDITIES
                or not _DIGEST.fullmatch(campaign["contract_digest"])
                or not _DIGEST.fullmatch(campaign["trust_domain_sha256"])
                or not _DIGEST.fullmatch(campaign["event_head"])):
            raise AttemptCorrupt("campaign state is invalid")
        stages = db.execute("SELECT * FROM stages ORDER BY ordinal").fetchall()
        if [(row["stage"], row["ordinal"]) for row in stages] != [
                ("TB_E1", 1), ("TB_E2_N3", 2)]:
            raise AttemptCorrupt("stage inventory is invalid")
        for row in stages:
            if row["state"] not in (
                    "UNRESERVED", "RESERVED", "STARTED_IN_DOUBT", "COMPLETED"):
                raise AttemptCorrupt("stage state is invalid")
            values = (
                row["binding"], row["reserved_at"], row["started_at"],
                row["completed_at"], row["outcome"],
            )
            required = {
                "UNRESERVED": (False, False, False, False, False),
                "RESERVED": (True, True, False, False, False),
                "STARTED_IN_DOUBT": (True, True, True, False, False),
                "COMPLETED": (True, True, True, True, True),
            }[row["state"]]
            if tuple(value is not None for value in values) != required:
                raise AttemptCorrupt("stage transition fields are invalid")
            if row["outcome"] is not None and row["outcome"] not in OUTCOMES:
                raise AttemptCorrupt("stage outcome is invalid")
        completed = {row["stage"] for row in stages if row["state"] == "COMPLETED"}
        if stages[1]["state"] != "UNRESERVED" and (
                stages[0]["state"] != "COMPLETED" or stages[0]["outcome"] != "PASS"):
            raise AttemptCorrupt("TB_E2_N3 exists without a successful TB_E1 predecessor")
        checkpoints = db.execute("SELECT * FROM checkpoints ORDER BY ordinal").fetchall()
        if [(row["checkpoint"], row["ordinal"]) for row in checkpoints] != [
                (name, ordinal) for ordinal, name in enumerate(E1_CHECKPOINTS, 1)]:
            raise AttemptCorrupt("E1 checkpoint inventory is invalid")
        seen_incomplete = False
        for row in checkpoints:
            if (row['consumed'] not in (0, 1)
                    or (row['state'] == 'PENDING' and row['consumed'])
                    or (row['state'] == 'COMPLETED' and not row['consumed'])):
                raise AttemptCorrupt('checkpoint consumption state is invalid')
            if row["state"] not in ("PENDING", "STARTED_IN_DOUBT", "COMPLETED"):
                raise AttemptCorrupt("checkpoint state is invalid")
            if row["state"] != "COMPLETED":
                seen_incomplete = True
            elif seen_incomplete:
                raise AttemptCorrupt("checkpoint completion order is invalid")
            fields = (
                row["binding"], row["parent_reservation_event_digest"],
                row["dispatch_sequence"], row["dispatch_event_digest"],
                row["receipt"], row["receipt_digest"],
            )
            required = {
                "PENDING": (False, False, False, False, False, False),
                "STARTED_IN_DOUBT": (True, True, True, True, False, False),
                "COMPLETED": (True, True, True, True, True, True),
            }[row["state"]]
            if tuple(value is not None for value in fields) != required:
                raise AttemptCorrupt("checkpoint transition fields are invalid")
            if row["receipt"] is not None:
                try:
                    receipt = _canonical_input(row["receipt"], "checkpoint receipt")
                except ValueError as exc:
                    raise AttemptCorrupt("checkpoint receipt bytes are invalid") from exc
                if hashlib.sha256(receipt).hexdigest() != row["receipt_digest"]:
                    raise AttemptCorrupt("checkpoint receipt digest differs")
        manifests = {
            row["stage"]: row for row in db.execute("SELECT * FROM manifests")
        }
        receipts = {
            row["stage"]: row for row in db.execute("SELECT * FROM receipts")
        }
        if set(manifests) != completed or set(receipts) != completed:
            raise AttemptCorrupt("result manifest and receipt inventory is incomplete")
        for inventory, label in ((manifests, "manifest"), (receipts, "receipt")):
            for row in inventory.values():
                try:
                    body = _canonical_input(row["body"], label)
                except ValueError as exc:
                    raise AttemptCorrupt(f"{label} bytes are invalid") from exc
                if hashlib.sha256(body).hexdigest() != row["digest"]:
                    raise AttemptCorrupt(f"{label} digest differs")
        for stage in completed:
            receipt = json.loads(receipts[stage]["body"])
            stage_row = next(row for row in stages if row["stage"] == stage)
            expected_receipt = {
                "campaign_id": campaign["campaign_id"],
                "commit_event_sequence": receipt.get("commit_event_sequence"),
                "contract_digest": campaign["contract_digest"],
                "manifest_sha256": manifests[stage]["digest"],
                "outcome": stage_row["outcome"],
                "result_attestation_digest": receipt.get("result_attestation_digest"),
                "result_producer_scope": receipt.get("result_producer_scope"),
                "result_stages": receipt.get("result_stages"),
                "schema": "qualification_attempt_receipt/v1",
                "stage": stage,
            }
            if (receipt != expected_receipt
                    or not isinstance(receipt["commit_event_sequence"], int)
                    or receipt["commit_event_sequence"] < 1
                    or not isinstance(receipt["result_attestation_digest"], str)
                    or not _DIGEST.fullmatch(receipt["result_attestation_digest"])
                    or not isinstance(receipt["result_producer_scope"], str)
                    or not receipt["result_producer_scope"]
                    or not isinstance(receipt["result_stages"], list)
                    or not receipt["result_stages"]):
                raise AttemptCorrupt("receipt binding differs from its durable result")
        expected_verdict = "PENDING"
        if campaign["ambiguity_reason"] is not None:
            expected_verdict = "AMBIGUOUS"
        elif any(row["outcome"] == "FAILURE" for row in stages):
            expected_verdict = "FALSIFIED"
        elif any(row["outcome"] == "UNRESOLVED" for row in stages):
            expected_verdict = "AMBIGUOUS"
        elif stages[1]["outcome"] == "PASS":
            expected_verdict = "RESOLVED"
        if campaign["verdict"] != expected_verdict:
            raise AttemptCorrupt("campaign verdict differs from stage outcomes")
        if (campaign["validity"] == "VALID") != (campaign["void_reason"] is None):
            raise AttemptCorrupt("campaign validity and void reason differ")
        ambiguity = (campaign["ambiguity_reason"], campaign["ambiguity_evidence_digest"])
        if (ambiguity[0] is None) != (ambiguity[1] is None):
            raise AttemptCorrupt("ambiguity reason and evidence identity differ")
        if ambiguity[0] is not None:
            if (not _DIGEST.fullmatch(ambiguity[1])
                    or any(row["state"] != "UNRESERVED" for row in stages)
                    or campaign["verdict"] != "AMBIGUOUS"):
                raise AttemptCorrupt("pre-stage ambiguity state is invalid")
        self._validate_events(db, campaign)

    @staticmethod
    def _campaign(db: sqlite3.Connection) -> sqlite3.Row:
        return db.execute("SELECT * FROM campaign WHERE singleton=1").fetchone()

    @staticmethod
    def _event_hash(seq: int, previous: str, kind: str, body: bytes, occurred_at: str) -> str:
        payload = _canonical({
            "body": json.loads(body), "kind": kind, "occurred_at": occurred_at,
            "previous": previous, "sequence": seq,
        })
        return hashlib.sha256(payload).hexdigest()

    def _validate_events(self, db: sqlite3.Connection, campaign: sqlite3.Row) -> None:
        previous = ZERO_HASH
        count = 0
        for row in db.execute("SELECT * FROM events ORDER BY seq"):
            count += 1
            try:
                body = _canonical_input(row["body"], "event body")
                expected = self._event_hash(
                    count, previous, row["kind"], body, row["occurred_at"])
            except (ValueError, TypeError, json.JSONDecodeError) as exc:
                raise AttemptCorrupt("event chain contains invalid bytes") from exc
            if row["seq"] != count or row["prev_hash"] != previous or row["event_hash"] != expected:
                raise AttemptCorrupt("event chain verification failed")
            previous = expected
        if count != campaign["event_count"] or previous != campaign["event_head"]:
            raise AttemptCorrupt("event chain head differs")

    def _append_event(
        self, db: sqlite3.Connection, kind: str, body: dict[str, Any], occurred_at: str,
    ) -> tuple[int, str]:
        campaign = self._campaign(db)
        sequence = campaign["event_count"] + 1
        raw = _canonical(body)
        digest = self._event_hash(sequence, campaign["event_head"], kind, raw, occurred_at)
        db.execute(
            "INSERT INTO events VALUES (?,?,?,?,?,?)",
            (sequence, campaign["event_head"], kind, raw, occurred_at, digest),
        )
        db.execute(
            "UPDATE campaign SET event_head=?, event_count=? WHERE singleton=1",
            (digest, sequence),
        )
        return sequence, digest

    @staticmethod
    def _stage_name(stage: str) -> str:
        if stage not in STAGES:
            raise ValueError(f"stage must be one of {STAGES}")
        return stage

    @staticmethod
    def _stage_row(db: sqlite3.Connection, stage: str) -> sqlite3.Row:
        return db.execute("SELECT * FROM stages WHERE stage=?", (stage,)).fetchone()

    @staticmethod
    def _stage_view(row: sqlite3.Row) -> dict[str, Any]:
        return {
            "stage": row["stage"], "state": row["state"],
            "binding_bytes": bytes(row["binding"]) if row["binding"] is not None else None,
            "reserved_at": row["reserved_at"], "started_at": row["started_at"],
            "completed_at": row["completed_at"], "outcome": row["outcome"],
        }

    @staticmethod
    def _ensure_mutable(campaign: sqlite3.Row) -> None:
        if campaign["validity"] != "VALID" or campaign["verdict"] != "PENDING":
            raise TransitionError("attempt is terminal")

    def reserve(self, stage: str, binding_bytes: bytes, *, now: datetime) -> dict[str, Any]:
        stage = self._stage_name(stage)
        binding = _canonical_input(binding_bytes, "binding")
        timestamp = _instant(now)
        with self._write() as db:
            row = self._stage_row(db, stage)
            if row["state"] != "UNRESERVED":
                if bytes(row["binding"]) != binding:
                    raise AttemptConflict("stage binding differs from the durable reservation")
                return self._stage_view(row)
            campaign = self._campaign(db)
            self._ensure_mutable(campaign)
            if stage == "TB_E2_N3":
                first = self._stage_row(db, "TB_E1")
                if first["state"] != "COMPLETED" or first["outcome"] != "PASS":
                    raise TransitionError("TB_E1 must complete with PASS before TB_E2_N3")
            db.execute(
                "UPDATE stages SET state='RESERVED', binding=?, reserved_at=? WHERE stage=?",
                (binding, timestamp, stage),
            )
            self._append_event(db, "STAGE_RESERVED", {
                "binding_sha256": hashlib.sha256(binding).hexdigest(), "stage": stage,
            }, timestamp)
            return self._stage_view(self._stage_row(db, stage))

    def claimed_reservation(self, stage: str) -> StageClaim:
        """Return the reservation's durable event identity for a source-load gate."""
        stage = self._stage_name(stage)
        with self._read() as db:
            row = self._stage_row(db, stage)
            if row["state"] == "UNRESERVED":
                raise TransitionError("stage has no durable reservation claim")
            binding_digest = hashlib.sha256(bytes(row["binding"])).hexdigest()
            matches = []
            for event in db.execute(
                    "SELECT seq,body,event_hash FROM events WHERE kind='STAGE_RESERVED' ORDER BY seq"):
                body = json.loads(event["body"])
                if body == {"binding_sha256": binding_digest, "stage": stage}:
                    matches.append(event)
            if len(matches) != 1:
                raise AttemptCorrupt("reservation event identity is not unique")
            event = matches[0]
            return StageClaim(
                campaign_id=self.campaign_id,
                contract_digest=self.contract_digest,
                stage=stage,
                binding_sha256=binding_digest,
                reservation_sequence=event["seq"],
                reservation_event_digest=event["event_hash"],
                state=row["state"],
            )

    def verify_claim(self, claim: StageClaim, *, require_state: str) -> StageClaim:
        if not isinstance(claim, StageClaim):
            raise AttemptConflict("reservation claim was not store-issued")
        if require_state not in ("RESERVED", "STARTED_IN_DOUBT", "COMPLETED"):
            raise ValueError("require_state is invalid")
        stored = self.claimed_reservation(claim.stage)
        identity = (
            "campaign_id", "contract_digest", "stage", "binding_sha256",
            "reservation_sequence", "reservation_event_digest",
        )
        if any(getattr(claim, field) != getattr(stored, field) for field in identity):
            raise AttemptConflict("reservation claim differs from the durable claim")
        if claim.state != stored.state or stored.state != require_state:
            raise TransitionError(
                f"reservation claim state is stale; durable state is {stored.state}"
            )
        return stored

    def start_once(
        self, stage: str, claim: StageClaim, *, now: datetime,
    ) -> StageDispatch:
        stage = self._stage_name(stage)
        timestamp = _instant(now)
        if not isinstance(claim, StageClaim) or claim.stage != stage:
            raise AttemptConflict("reservation claim was not store-issued for this stage")
        stored = self.claimed_reservation(stage)
        identity = (
            "campaign_id", "contract_digest", "stage", "binding_sha256",
            "reservation_sequence", "reservation_event_digest",
        )
        if any(getattr(claim, field) != getattr(stored, field) for field in identity):
            raise AttemptConflict("reservation claim differs from the durable claim")
        if stored.state != "RESERVED" or claim.state != "RESERVED":
            raise TransitionError(
                f"stage was already dispatched and remains {stored.state}"
            )
        with self._write() as db:
            row = self._stage_row(db, stage)
            if row["state"] == "STARTED_IN_DOUBT":
                raise TransitionError("stage was already dispatched and remains STARTED_IN_DOUBT")
            if row["state"] == "COMPLETED":
                raise TransitionError("completed stage cannot be reopened")
            self._ensure_mutable(self._campaign(db))
            if row["state"] != "RESERVED":
                raise TransitionError("stage must be reserved before it is started")
            db.execute(
                "UPDATE stages SET state='STARTED_IN_DOUBT', started_at=? WHERE stage=?",
                (timestamp, stage),
            )
            sequence, digest = self._append_event(db, "STAGE_DISPATCHED", {
                "reservation_event_digest": claim.reservation_event_digest,
                "stage": stage,
            }, timestamp)
            return StageDispatch(
                campaign_id=self.campaign_id, contract_digest=self.contract_digest,
                stage=stage,
                reservation_event_digest=claim.reservation_event_digest,
                dispatch_sequence=sequence, dispatch_event_digest=digest,
            )

    @staticmethod
    def _checkpoint_name(checkpoint: str) -> str:
        if checkpoint not in E1_CHECKPOINTS:
            raise ValueError(f"checkpoint must be one of {E1_CHECKPOINTS}")
        return checkpoint

    def _verify_parent_identity(self, claim: StageClaim) -> StageClaim:
        if not isinstance(claim, StageClaim) or claim.stage != "TB_E1":
            raise AttemptConflict("checkpoint parent claim is invalid")
        stored = self.claimed_reservation("TB_E1")
        fields = (
            "campaign_id", "contract_digest", "stage", "binding_sha256",
            "reservation_sequence", "reservation_event_digest",
        )
        if any(getattr(claim, field) != getattr(stored, field) for field in fields):
            raise AttemptConflict("checkpoint parent claim differs from the durable reservation")
        return stored

    def start_checkpoint_once(
        self, checkpoint: str, parent_claim: StageClaim, binding_bytes: bytes, *,
        now: datetime,
    ) -> CheckpointDispatch:
        checkpoint = self._checkpoint_name(checkpoint)
        binding = _canonical_input(binding_bytes, "checkpoint binding")
        timestamp = _instant(now)
        stored_parent = self._verify_parent_identity(parent_claim)
        if stored_parent.state != "STARTED_IN_DOUBT":
            raise TransitionError("TB_E1 must be dispatched before checkpoint execution")
        with self._write() as db:
            self._ensure_mutable(self._campaign(db))
            row = db.execute(
                "SELECT * FROM checkpoints WHERE checkpoint=?", (checkpoint,)
            ).fetchone()
            if row["state"] != "PENDING":
                raise TransitionError(
                    f"checkpoint {checkpoint} was already dispatched and cannot rerun"
                )
            previous = db.execute(
                "SELECT checkpoint,state FROM checkpoints WHERE ordinal<? ORDER BY ordinal",
                (row["ordinal"],),
            ).fetchall()
            if any(item["state"] != "COMPLETED" for item in previous):
                raise TransitionError("E1 checkpoints must execute in N1 -> CUTOFF -> N2 -> PART_A order")
            binding_digest = hashlib.sha256(binding).hexdigest()
            sequence, digest = self._append_event(db, "E1_CHECKPOINT_DISPATCHED", {
                "binding_sha256": binding_digest, "checkpoint": checkpoint,
                "parent_reservation_event_digest": parent_claim.reservation_event_digest,
            }, timestamp)
            db.execute(
                "UPDATE checkpoints SET state='STARTED_IN_DOUBT', binding=?, "
                "parent_reservation_event_digest=?, dispatch_sequence=?, "
                "dispatch_event_digest=? WHERE checkpoint=?",
                (binding, parent_claim.reservation_event_digest, sequence, digest, checkpoint),
            )
            dispatch = CheckpointDispatch(
                campaign_id=self.campaign_id, contract_digest=self.contract_digest,
                checkpoint=checkpoint,
                parent_reservation_event_digest=parent_claim.reservation_event_digest,
                binding_sha256=binding_digest, dispatch_sequence=sequence,
                dispatch_event_digest=digest,
            )
            self._issued_checkpoint_dispatches[checkpoint] = dispatch
            return dispatch

    def consume_checkpoint_dispatch(
        self, dispatch: CheckpointDispatch,
    ) -> CheckpointDispatch:
        """Consume one exact in-process dispatch capability before outcome work."""
        if not isinstance(dispatch, CheckpointDispatch):
            raise AttemptConflict("checkpoint dispatch capability is invalid")
        issued = self._issued_checkpoint_dispatches.get(dispatch.checkpoint)
        if issued is not dispatch:
            raise AttemptConflict(
                "checkpoint dispatch was not freshly issued by this store instance")
        with self._write() as db:
            self._ensure_mutable(self._campaign(db))
            if self._campaign(db)["boot_id"] != self.boot_id:
                raise BootFenceError("boot identity has been superseded")
            row = db.execute(
                "SELECT * FROM checkpoints WHERE checkpoint=?", (dispatch.checkpoint,)
            ).fetchone()
            expected = (
                self.campaign_id, self.contract_digest, dispatch.checkpoint,
                row["parent_reservation_event_digest"],
                hashlib.sha256(bytes(row["binding"])).hexdigest(),
                row["dispatch_sequence"], row["dispatch_event_digest"],
            )
            actual = (
                dispatch.campaign_id, dispatch.contract_digest, dispatch.checkpoint,
                dispatch.parent_reservation_event_digest, dispatch.binding_sha256,
                dispatch.dispatch_sequence, dispatch.dispatch_event_digest,
            )
            if row["state"] != "STARTED_IN_DOUBT" or actual != expected or row['consumed']:
                raise AttemptConflict("checkpoint dispatch differs from durable dispatch")
            db.execute('UPDATE checkpoints SET consumed=1 WHERE checkpoint=?', (dispatch.checkpoint,))
        self._issued_checkpoint_dispatches.pop(dispatch.checkpoint)
        return dispatch

    def complete_checkpoint(
        self, checkpoint: str, dispatch: CheckpointDispatch, receipt_bytes: bytes, *,
        now: datetime,
    ) -> bytes:
        checkpoint = self._checkpoint_name(checkpoint)
        receipt = _canonical_input(receipt_bytes, "checkpoint receipt")
        timestamp = _instant(now)
        if not isinstance(dispatch, CheckpointDispatch) or dispatch.checkpoint != checkpoint:
            raise AttemptConflict("checkpoint dispatch claim is invalid")
        with self._write() as db:
            row = db.execute(
                "SELECT * FROM checkpoints WHERE checkpoint=?", (checkpoint,)
            ).fetchone()
            if row["state"] == "COMPLETED":
                if (row["dispatch_event_digest"] == dispatch.dispatch_event_digest
                        and bytes(row["receipt"]) == receipt):
                    return bytes(row["receipt"])
                raise AttemptConflict("checkpoint completion differs from the durable receipt")
            self._ensure_mutable(self._campaign(db))
            if not row['consumed']:
                raise TransitionError('checkpoint execution capability must be consumed before completion')
            expected = (
                self.campaign_id, self.contract_digest, checkpoint,
                row["parent_reservation_event_digest"],
                hashlib.sha256(bytes(row["binding"])).hexdigest(),
                row["dispatch_sequence"], row["dispatch_event_digest"],
            )
            actual = (
                dispatch.campaign_id, dispatch.contract_digest, dispatch.checkpoint,
                dispatch.parent_reservation_event_digest, dispatch.binding_sha256,
                dispatch.dispatch_sequence, dispatch.dispatch_event_digest,
            )
            if row["state"] != "STARTED_IN_DOUBT" or actual != expected:
                raise AttemptConflict("checkpoint dispatch differs from the durable dispatch")
            receipt_digest = hashlib.sha256(receipt).hexdigest()
            db.execute(
                "UPDATE checkpoints SET state='COMPLETED', receipt=?, receipt_digest=? "
                "WHERE checkpoint=?", (receipt, receipt_digest, checkpoint),
            )
            self._append_event(db, "E1_CHECKPOINT_COMPLETED", {
                "checkpoint": checkpoint, "dispatch_event_digest": dispatch.dispatch_event_digest,
                "receipt_sha256": receipt_digest,
            }, timestamp)
            return receipt

    def checkpoints(self) -> list[dict[str, Any]]:
        with self._read() as db:
            return [{
                "checkpoint": row["checkpoint"], "state": row["state"],
                "binding_bytes": bytes(row["binding"]) if row["binding"] is not None else None,
                "dispatch_event_digest": row["dispatch_event_digest"],
                "receipt_bytes": bytes(row["receipt"]) if row["receipt"] is not None else None,
            } for row in db.execute("SELECT * FROM checkpoints ORDER BY ordinal")]

    def _commit_validated_result(
        self, stage: str, manifest_bytes: bytes, *, outcome: str,
        validation_claim: ValidatedResultClaim, now: datetime,
    ) -> bytes:
        stage = self._stage_name(stage)
        if outcome not in OUTCOMES:
            raise ValueError(f"outcome must be one of {OUTCOMES}")
        manifest = _canonical_input(manifest_bytes, "result manifest")
        timestamp = _instant(now)
        manifest_digest = hashlib.sha256(manifest).hexdigest()
        if (not isinstance(validation_claim, ValidatedResultClaim)
                or validation_claim._validation_token is not _VALIDATED_RESULT_TOKEN):
            raise AttemptConflict("validated result claim is required")
        expected_claim = (
            self.campaign_id, self.contract_digest, stage, manifest_digest, outcome,
        )
        actual_claim = (
            validation_claim.campaign_id, validation_claim.contract_digest,
            validation_claim.stage, validation_claim.manifest_sha256,
            validation_claim.outcome,
        )
        if (actual_claim != expected_claim
                or not validation_claim.producer_scope
                or not _DIGEST.fullmatch(validation_claim.attestation_digest)
                or not isinstance(validation_claim.result_stages, tuple)
                or not validation_claim.result_stages):
            raise AttemptConflict("validated result claim binding differs")
        with self._write() as db:
            row = self._stage_row(db, stage)
            if row["state"] == "COMPLETED":
                saved = db.execute(
                    "SELECT m.body, r.body FROM manifests m JOIN receipts r USING(stage) "
                    "WHERE m.stage=?", (stage,),
                ).fetchone()
                if row["outcome"] == outcome and saved is not None and bytes(saved[0]) == manifest:
                    return bytes(saved[1])
                raise AttemptConflict("result differs from the completed durable result")
            self._ensure_mutable(self._campaign(db))
            if row["state"] != "STARTED_IN_DOUBT":
                raise TransitionError("stage must be started before result commit")
            if stage == "TB_E1":
                checkpoint_states = {
                    item["checkpoint"]: item["state"] for item in db.execute(
                        "SELECT checkpoint,state FROM checkpoints ORDER BY ordinal")
                }
                required_completed = {
                    ("LEGALITY", "N1"): ("N1", "CUTOFF"),
                    ("LEGALITY", "N1", "N2", "PART_B"): ("N1", "CUTOFF", "N2"),
                    ("LEGALITY", "N1", "N2", "PART_B", "PART_A"):
                        ("N1", "CUTOFF", "N2", "PART_A"),
                }.get(validation_claim.result_stages)
                if required_completed is None:
                    raise TransitionError("authenticated E1 result stage prefix is invalid")
                if any(checkpoint_states[name] != "COMPLETED" for name in required_completed):
                    raise TransitionError("required E1 result checkpoints are incomplete")
                if any(checkpoint_states[name] != "PENDING" for name in E1_CHECKPOINTS
                       if name not in required_completed):
                    raise TransitionError("E1 result continues beyond its terminal prefix")
                if outcome == "PASS" and len(required_completed) != len(E1_CHECKPOINTS):
                    raise TransitionError("passing E1 result requires every checkpoint")
            campaign = self._campaign(db)
            receipt = _canonical({
                "campaign_id": self.campaign_id,
                "commit_event_sequence": campaign["event_count"] + 1,
                "contract_digest": self.contract_digest,
                "manifest_sha256": manifest_digest,
                "outcome": outcome,
                "result_attestation_digest": validation_claim.attestation_digest,
                "result_producer_scope": validation_claim.producer_scope,
                "result_stages": list(validation_claim.result_stages),
                "schema": "qualification_attempt_receipt/v1",
                "stage": stage,
            })
            receipt_digest = hashlib.sha256(receipt).hexdigest()
            db.execute("INSERT INTO manifests VALUES (?,?,?)", (stage, manifest, manifest_digest))
            db.execute("INSERT INTO receipts VALUES (?,?,?)", (stage, receipt, receipt_digest))
            db.execute(
                "UPDATE stages SET state='COMPLETED', completed_at=?, outcome=? WHERE stage=?",
                (timestamp, outcome, stage),
            )
            verdict = "PENDING"
            if outcome == "FAILURE":
                verdict = "FALSIFIED"
            elif outcome == "UNRESOLVED":
                verdict = "AMBIGUOUS"
            elif stage == "TB_E2_N3":
                verdict = "RESOLVED"
            db.execute("UPDATE campaign SET verdict=? WHERE singleton=1", (verdict,))
            self._append_event(db, "RESULT_COMMITTED", {
                "manifest_sha256": manifest_digest, "outcome": outcome,
                "receipt_sha256": receipt_digest, "stage": stage,
                "result_attestation_digest": validation_claim.attestation_digest,
            }, timestamp)
            return receipt

    def commit_result(self, *args: Any, **kwargs: Any) -> bytes:
        raise TransitionError(
            "direct result commit is forbidden; use commit_validated_result with an authenticated claim"
        )

    def commit_validated_result(self, *args: Any, **kwargs: Any) -> bytes:
        raise TransitionError(
            "validated result commits are controller-private; use the authenticated G5 commit boundary"
        )

    def void(self, reason: str, *, now: datetime) -> dict[str, Any]:
        reason = _identifier(reason, "void reason")
        timestamp = _instant(now)
        with self._write() as db:
            campaign = self._campaign(db)
            if campaign["validity"] == "VOID":
                if campaign["void_reason"] != reason:
                    raise AttemptConflict("void reason differs from the durable reason")
                return self._status_view(campaign)
            db.execute(
                "UPDATE campaign SET validity='VOID', void_reason=? WHERE singleton=1", (reason,)
            )
            self._append_event(db, "ATTEMPT_VOIDED", {"reason": reason}, timestamp)
            return self._status_view(self._campaign(db))

    def mark_ambiguous(
        self, reason: str, evidence_digest: str, *, now: datetime,
    ) -> dict[str, Any]:
        reason = _identifier(reason, "ambiguity reason")
        if not isinstance(evidence_digest, str) or not _DIGEST.fullmatch(evidence_digest):
            raise ValueError("evidence_digest must be a lowercase SHA-256 digest")
        timestamp = _instant(now)
        with self._write() as db:
            campaign = self._campaign(db)
            if campaign["verdict"] == "AMBIGUOUS" and campaign["ambiguity_reason"] is not None:
                if (campaign["ambiguity_reason"], campaign["ambiguity_evidence_digest"]) != (
                        reason, evidence_digest):
                    raise AttemptConflict("ambiguity identity differs from the durable ambiguity")
                return self._status_view(campaign)
            self._ensure_mutable(campaign)
            if any(row[0] != "UNRESERVED" for row in db.execute("SELECT state FROM stages")):
                raise TransitionError("pre-stage ambiguity must be recorded before any stage reservation")
            db.execute(
                "UPDATE campaign SET verdict='AMBIGUOUS', ambiguity_reason=?, "
                "ambiguity_evidence_digest=? WHERE singleton=1",
                (reason, evidence_digest),
            )
            self._append_event(db, "ATTEMPT_AMBIGUOUS", {
                "evidence_digest": evidence_digest, "reason": reason,
            }, timestamp)
            return self._status_view(self._campaign(db))

    @staticmethod
    def _status_view(row: sqlite3.Row) -> dict[str, Any]:
        return {
            "campaign_id": row["campaign_id"], "contract_digest": row["contract_digest"],
            "trust_domain_sha256": row["trust_domain_sha256"],
            "boot_id": row["boot_id"], "verdict": row["verdict"],
            "validity": row["validity"], "void_reason": row["void_reason"],
            "ambiguity_reason": row["ambiguity_reason"],
            "ambiguity_evidence_digest": row["ambiguity_evidence_digest"],
            "event_head": row["event_head"], "event_count": row["event_count"],
        }

    def status(self) -> dict[str, Any]:
        with self._read() as db:
            return self._status_view(self._campaign(db))

    def stage(self, stage: str) -> dict[str, Any]:
        stage = self._stage_name(stage)
        with self._read() as db:
            return self._stage_view(self._stage_row(db, stage))

    def result(self, stage: str) -> dict[str, Any] | None:
        stage = self._stage_name(stage)
        with self._read() as db:
            row = db.execute(
                "SELECT m.body AS manifest, m.digest AS manifest_digest, "
                "r.body AS receipt, r.digest AS receipt_digest, s.outcome AS outcome "
                "FROM manifests m JOIN receipts r USING(stage) JOIN stages s USING(stage) "
                "WHERE m.stage=?", (stage,),
            ).fetchone()
            if row is None:
                return None
            return {
                "manifest_bytes": bytes(row["manifest"]),
                "manifest_digest": row["manifest_digest"],
                "receipt_bytes": bytes(row["receipt"]),
                "receipt_digest": row["receipt_digest"],
                "outcome": row["outcome"],
            }

    def events(self) -> list[dict[str, Any]]:
        with self._read() as db:
            return [{
                "sequence": row["seq"], "previous": row["prev_hash"],
                "kind": row["kind"], "body": json.loads(row["body"]),
                "occurred_at": row["occurred_at"], "digest": row["event_hash"],
            } for row in db.execute("SELECT * FROM events ORDER BY seq")]
