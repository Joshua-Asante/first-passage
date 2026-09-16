"""Durable offline four-leg account owner.

The owner serializes every mutation, reserves capacity before dispatch and treats
transport acceptance as no execution evidence.  A ``SyntheticBroker`` is an
explicit Python-only test seam; no configuration or HTTP path can construct it.
Every boot starts HALTED with a fresh boot/generation while retained operations,
attempts, facts and reservations remain owned.
"""
from __future__ import annotations

from contextlib import closing, contextmanager, nullcontext
from dataclasses import asdict, dataclass, replace
from datetime import datetime, timedelta
from decimal import Decimal
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sqlite3
import threading
from uuid import uuid4
from lib.validation import require_finite_number

from c1_signal_daemon.book_validation import InputViolation, validate_action

from .book_protection import ActionOccurrence, ProtectionChange, occurrence_key
from .book_protection_owner import ProtectionOwnerMixin
from .book_takeover_owner import TakeoverOwnerMixin
from .book_bootstrap import BootstrapOwnerMixin
from .book_account_lock import AccountSerializer
from .book_capacity import (
    CapacityState,
    CompleteTakeover,
    RetireTakeover,
    Event as CapacityEvent,
    Fill as CapacityFill,
    Reduction,
    Reserve,
    Quiescence,
    Terminal,
    apply_event,
    exposures,
    project_capacity,
)
from .book_policy import BOOK_LEGS, is_protected, leg
from .book_sizing_context import (
    BookAccountContext,
    BookExposure,
    BookSizingBinding,
    BookSizingRequest,
    BookSession,
    SettledClose,
    size_book_request,
)
from .book_schedule import ScheduleError, SchedulePhase, classify_schedule
from c1_signal_daemon.book_adapters import ADAPTER_BY_LEG
from c1_signal_daemon.book_protocol import (
    BracketAmend,
    Cancel,
    ExecutionEvent,
    Fill,
    Mode,
    OrderIntent,
)


MAX_FACT_AGE = timedelta(seconds=30)


class AccountOwnerError(RuntimeError):
    """Durable owner state is missing, corrupt or conflicting."""


class SimulatedOwnerCrash(RuntimeError):
    """Explicit offline-only crash cut used by durability tests."""


def _canonical(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _encoded(value):
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, (Fraction, Decimal)):
        return str(value)
    if hasattr(value, "value"):
        return value.value
    raise TypeError(type(value).__name__)


def _body(value) -> str:
    return json.dumps(value, default=_encoded, sort_keys=True, separators=(",", ":"),
                      allow_nan=False)


PHASE1_ADMISSION_IDENTITIES = {
    "admission_contract": "4f027af56f18c119c18b24f6f867ecb0a64188085ea7a8a95c18b0a77d0e9dde",
    "independent_review": "dd9c5e7296535a934b973df7ec0ff8b87c6c3554fc092822820f633588654cfd",
    "accepted_run": "8ddf727b38b3044ad2c0e8cb05330933f94b9fb8c9f21be38dbeff41d7ad75e0",
    "run_py": "2ea9e16911214ebac0eaba840b6aab90b784cf2623d937ce91be91261053ff2b",
}


def _binding_record(binding):
    from c1_signal_daemon.book_adapters import (
        ADAPTERS, EFFECTIVE_INPUTS_SHA256, RUNTIME_EFFECTIVE_INPUTS_SHA256,
    )
    session = binding["session"]
    settlement = binding["settlement"]
    policy = binding["policy"]
    return {
        "session": asdict(session),
        "settlement": asdict(settlement),
        "policy": {"reference_mode": policy.reference_mode,
                   "trigger": policy.trigger, "scale": policy.scale,
                   "provenance": policy.provenance},
        "policy_digest": binding["policy_digest"],
        "snapshot_digest": binding["snapshot_digest"],
        "as_of": binding["as_of"], "valid_until": binding["valid_until"],
        "max_evidence_age_seconds": binding["max_evidence_age"].total_seconds(),
        "lifecycle_tiers": binding["lifecycle_tiers"],
        "cap_allocations": binding["cap_allocations"],
        "risk_dollars": binding["risk_dollars"],
        "runtime_identities": {
            row.leg_id: {"pine_sha256": row.pine_sha256,
                         "runtime_sha256": row.runtime_sha256}
            for row in ADAPTERS
        },
        "historical_effective_inputs_sha256": EFFECTIVE_INPUTS_SHA256,
        "effective_inputs_sha256": RUNTIME_EFFECTIVE_INPUTS_SHA256,
        "phase1_admission": PHASE1_ADMISSION_IDENTITIES,
    }


def _time(value, name="timestamp") -> datetime:
    if not isinstance(value, datetime) or value.utcoffset() is None:
        raise AccountOwnerError(f"{name} must be timezone-aware")
    return value


def _text(value, name="identity") -> str:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise AccountOwnerError(f"invalid {name}")
    return value


@dataclass(frozen=True)
class BrokerFact:
    fact_id: str
    kind: str
    operation_id: str
    leg_id: str
    order_kind: str
    quantity: int
    as_of: datetime
    price: float | None = None
    status: str | None = None
    cumulative_filled: int | None = None
    entry_execution_id: str | None = None

    @classmethod
    def fill(cls, execution_id, operation_id, leg_id, order_kind, quantity, price, as_of,
             *, entry_execution_id=None):
        return cls(execution_id, "fill", operation_id, leg_id, order_kind, quantity,
                   as_of, price=price, entry_execution_id=entry_execution_id)

    @classmethod
    def terminal(cls, operation_id, status, cumulative_filled, as_of):
        return cls("terminal:" + operation_id + ":" + status, "terminal", operation_id,
                   "", "", 0, as_of, status=status,
                   cumulative_filled=cumulative_filled)


@dataclass(frozen=True)
class BrokerResult:
    state: str
    facts: tuple[BrokerFact, ...] = ()

    def __post_init__(self):
        if self.state not in ("accepted", "rejected", "unknown"):
            raise ValueError("invalid synthetic transport state")
        if not isinstance(self.facts, tuple) or not all(isinstance(f, BrokerFact) for f in self.facts):
            raise ValueError("facts must be an explicit BrokerFact tuple")


@dataclass(frozen=True)
class BrokerCommand:
    attempt_id: str
    operation_id: str
    leg_id: str
    kind: str
    side: str | None
    quantity: int | None
    order_symbol: str
    authority: str
    generation: int
    action: OrderIntent | BracketAmend | Cancel
    target_operation_id: str | None = None
    occurrence: ActionOccurrence | None = None
    protection_change: ProtectionChange | None = None


class SyntheticBroker:
    """Labeled deterministic route for offline proof only."""

    synthetic = True

    def __init__(self, results):
        self._results = list(results)
        if not all(isinstance(item, BrokerResult) for item in self._results):
            raise ValueError("synthetic results must be BrokerResult values")
        self.commands: list[BrokerCommand] = []

    def queue(self, result):
        if not isinstance(result, BrokerResult):
            raise ValueError("synthetic result required")
        self._results.append(result)

    def send(self, command):
        if not isinstance(command, BrokerCommand):
            raise ValueError("typed broker command required")
        self.commands.append(command)
        return self._results.pop(0) if self._results else BrokerResult("unknown")


@dataclass(frozen=True)
class DispatchResult:
    operation_id: str
    quantity: int
    attempt_id: str | None = None
    transport_state: str = "not_attempted"
    refusal_reason: str | None = None
    confirmed_events: tuple[ExecutionEvent, ...] = ()


_SCHEMA = {
    "owner_state": "schema INTEGER NOT NULL, account TEXT NOT NULL, account_epoch TEXT NOT NULL, "
                   "boot_id TEXT NOT NULL, generation INTEGER NOT NULL, permission TEXT NOT NULL, "
                   "authority TEXT NOT NULL, sequence INTEGER NOT NULL",
    "incidents": "incident_id TEXT PRIMARY KEY, reason TEXT NOT NULL, at TEXT NOT NULL, "
                 "generation INTEGER NOT NULL",
    "operations": "operation_id TEXT PRIMARY KEY, leg_id TEXT NOT NULL, order_symbol TEXT NOT NULL, "
                  "kind TEXT NOT NULL, requested INTEGER, quantity INTEGER, session_id TEXT NOT NULL, "
                  "generation INTEGER NOT NULL, created_at TEXT NOT NULL, status TEXT NOT NULL, body TEXT NOT NULL",
    "attempts": "attempt_id TEXT PRIMARY KEY, operation_id TEXT NOT NULL UNIQUE, state TEXT NOT NULL, "
                "generation INTEGER NOT NULL, body TEXT NOT NULL, observation TEXT",
    "capacity_events": "sequence INTEGER PRIMARY KEY, event_id TEXT NOT NULL UNIQUE, as_of TEXT NOT NULL, "
                       "fact_type TEXT NOT NULL, body TEXT NOT NULL",
    "broker_facts": "fact_id TEXT PRIMARY KEY, body TEXT NOT NULL, feedback TEXT",
    "feedback": "fact_id TEXT PRIMARY KEY, body TEXT NOT NULL, delivered INTEGER NOT NULL DEFAULT 0, "
                "checkpoint TEXT, boundary_time TEXT",
    "barriers": "bar_time TEXT PRIMARY KEY, session_id TEXT NOT NULL, mode TEXT NOT NULL, "
                "body TEXT NOT NULL, actions TEXT, completed INTEGER NOT NULL DEFAULT 0",
    "partial_bars": "bar_time TEXT NOT NULL, leg_id TEXT NOT NULL, body TEXT NOT NULL, "
                    "acquired_at TEXT NOT NULL, PRIMARY KEY(bar_time, leg_id)",
    "timeline": "sequence INTEGER PRIMARY KEY, kind TEXT NOT NULL, ref_id TEXT NOT NULL UNIQUE, "
                "acquired_at TEXT NOT NULL",
    "protection_state": "session_id TEXT PRIMARY KEY, mode TEXT NOT NULL, operation_ids TEXT NOT NULL, "
                        "generation INTEGER NOT NULL",
    "runtime_bindings": "sequence INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT NOT NULL UNIQUE, "
                        "body TEXT NOT NULL, digest TEXT NOT NULL UNIQUE",
    "runtime_actors": "boot_id TEXT PRIMARY KEY, kind TEXT NOT NULL, body TEXT NOT NULL",
    "settlement_attachment": "singleton INTEGER PRIMARY KEY CHECK(singleton=1), "
                             "body TEXT NOT NULL, digest TEXT NOT NULL",
    "close_reservations": "operation_id TEXT PRIMARY KEY, allocations TEXT NOT NULL, "
                          "status TEXT NOT NULL",
    "action_occurrences": "key TEXT PRIMARY KEY, envelope TEXT NOT NULL, source TEXT NOT NULL, scope TEXT, result TEXT, state TEXT NOT NULL, prepared_at TEXT NOT NULL, generation INTEGER NOT NULL, boot_id TEXT NOT NULL",
    "protection_owners": "owner_id TEXT PRIMARY KEY, entry_fill_id TEXT NOT NULL UNIQUE, body TEXT NOT NULL",
    "protection_operations": "operation_id TEXT PRIMARY KEY, occurrence_key TEXT NOT NULL, owner_id TEXT NOT NULL, body TEXT NOT NULL",
    "protection_facts": "fact_id TEXT PRIMARY KEY, body TEXT NOT NULL, kind TEXT NOT NULL",
    "protection_streams": "stream_id TEXT PRIMARY KEY, body TEXT NOT NULL",
    "feed_watch": "session_id TEXT PRIMARY KEY, started_at TEXT NOT NULL",
    "bootstrap_identity": "singleton INTEGER PRIMARY KEY CHECK(singleton=1), body TEXT NOT NULL",
    "bootstrap_reads": "read_id TEXT PRIMARY KEY, body TEXT NOT NULL",
    "migration_records": "migration_id TEXT PRIMARY KEY, source_version INTEGER NOT NULL, source_digest TEXT NOT NULL, target_version INTEGER NOT NULL, body TEXT NOT NULL",
    "legacy_obligations": "obligation_id TEXT PRIMARY KEY, source_table TEXT NOT NULL, source_id TEXT NOT NULL, kind TEXT NOT NULL, body TEXT NOT NULL, UNIQUE(source_table, source_id, kind)",
    "takeover_plans": "operation_id TEXT PRIMARY KEY, occurrence_key TEXT NOT NULL UNIQUE, body TEXT NOT NULL",
    "takeover_events": "event_id TEXT PRIMARY KEY, operation_id TEXT NOT NULL, ordinal INTEGER NOT NULL, kind TEXT NOT NULL, body TEXT NOT NULL, UNIQUE(operation_id, ordinal)",
    "takeover_children": "operation_id TEXT PRIMARY KEY, takeover_id TEXT NOT NULL, occurrence_key TEXT NOT NULL UNIQUE, kind TEXT NOT NULL, target TEXT NOT NULL, body TEXT NOT NULL",
    "takeover_reads": "read_id TEXT PRIMARY KEY, operation_id TEXT NOT NULL, body TEXT NOT NULL",
    "takeover_inventory": "fact_id TEXT PRIMARY KEY, stream_id TEXT NOT NULL, sequence INTEGER NOT NULL, body TEXT NOT NULL, disposition TEXT NOT NULL, UNIQUE(stream_id, sequence)",
    "takeover_streams": "stream_id TEXT PRIMARY KEY, body TEXT NOT NULL",
}

_SETTLEMENT_TABLES = {
    "state", "chain", "superseded_chain", "packages", "sources", "b7_history",
    "challenges", "events", "receipts", "sqlite_sequence",
}


class BookAccountOwner(BootstrapOwnerMixin, TakeoverOwnerMixin, ProtectionOwnerMixin):
    """Single durable account writer; production transport is intentionally absent."""

    def __init__(self, path, account, binding, synthetic_broker, crash_at=None):
        self.path = Path(path)
        self.account = _text(account, "account")
        self.binding = self._validate_binding(binding)
        if synthetic_broker is not None and not (
                isinstance(synthetic_broker, SyntheticBroker) and synthetic_broker.synthetic):
            raise AccountOwnerError("only the explicit SyntheticBroker test seam is supported")
        self.synthetic_broker = synthetic_broker
        if crash_at not in (None, "after_reservation", "before_send", "after_send",
                            'takeover:PLAN', 'takeover:CONFIRM_CANCELLATIONS',
                            'takeover:CLOSE_DISPLACED', 'takeover:REVALIDATE', 'takeover:ATTEMPTED', 'takeover:RETIRED'):
            raise AccountOwnerError("unknown synthetic crash cut")
        self.crash_at = crash_at
        self.settlement_store = None
        self.serializer = AccountSerializer(self.path.with_suffix(self.path.suffix + ".lock"))
        self._thread = threading.RLock()
        self._settlement_local = threading.local()
        self._actor_boot_id = None

    @classmethod
    def boot(cls, path, account, *, binding, synthetic_broker=None, crash_at=None):
        owner = cls(path, account, binding, synthetic_broker, crash_at)
        owner.path.parent.mkdir(parents=True, exist_ok=True)
        with owner.serializer.acquire():
            return owner._boot_locked()

    def _boot_locked(owner):
        existed = owner.path.exists()
        with owner._transaction(create=True) as db:
            tables = {row[0] for row in db.execute(
                "SELECT name FROM sqlite_master WHERE type='table'")}
            if not tables:
                if existed:
                    raise AccountOwnerError("account owner state unavailable")
                for name, fields in _SCHEMA.items():
                    db.execute(f"CREATE TABLE {name} ({fields})")
                db.execute("INSERT INTO owner_state VALUES (4, ?, ?, ?, 1, 'HALTED', "
                           "'INTERVENTION', 0)",
                           (owner.account, str(uuid4()), str(uuid4())))
                attachment_body = _body({
                    "account": owner.account, "status": "NEVER_ATTACHED",
                })
                db.execute(
                    "INSERT INTO settlement_attachment VALUES (1, ?, ?)",
                    (attachment_body,
                     hashlib.sha256(attachment_body.encode("utf-8")).hexdigest()),
                )
                record = _binding_record(owner.binding)
                raw = _body(record)
                db.execute("INSERT INTO runtime_bindings(session_id, body, digest) VALUES (?, ?, ?)",
                           (owner.binding["session"].session_id, raw,
                            hashlib.sha256(raw.encode("utf-8")).hexdigest()))
                owner._new_bootstrap_db(db)
            else:
                version = db.execute("SELECT schema FROM owner_state").fetchall()
                if version in ([(1,)], [(2,)], [(3,)]):
                    raise AccountOwnerError("legacy schema requires explicit migration")
                if version != [(4,)]:
                    raise AccountOwnerError("invalid account owner schema version")
                owner._validate_schema(db)
                owner._settlement_attachment_state(db)
                state = owner._state(db)
                if state["account"] != owner.account:
                    raise AccountOwnerError("account owner mismatch")
                record = _binding_record(owner.binding)
                raw = _body(record)
                retained = db.execute(
                    "SELECT session_id, body FROM runtime_bindings ORDER BY sequence DESC LIMIT 1").fetchone()
                if retained is None:
                    raise AccountOwnerError("runtime binding authority missing")
                if retained[0] == owner.binding["session"].session_id:
                    if retained[1] != raw:
                        raise AccountOwnerError("runtime binding changed within session")
                else:
                    previous = json.loads(retained[1])
                    current = json.loads(raw)
                    immutable = ("policy", "policy_digest", "lifecycle_tiers", "cap_allocations",
                                 "risk_dollars", "runtime_identities",
                                 "historical_effective_inputs_sha256", "effective_inputs_sha256",
                                 "phase1_admission")
                    if (owner.binding["session"].prior_session_id != retained[0]
                            or owner.binding["settlement"].session_id != retained[0]
                            or any(previous[key] != current[key] for key in immutable)
                            or previous["session"]["calendar_digest"] != current["session"]["calendar_digest"]):
                        raise AccountOwnerError("unverified runtime binding transition")
                    db.execute(
                        "INSERT INTO runtime_bindings(session_id, body, digest) VALUES (?, ?, ?)",
                        (owner.binding["session"].session_id, raw,
                         hashlib.sha256(raw.encode("utf-8")).hexdigest()))
                owner._invalidate_bootstrap_db(db, 'restart')
                db.execute("UPDATE owner_state SET boot_id=?, generation=generation+1, "
                           "permission='HALTED', authority='INTERVENTION'", (str(uuid4()),))
            current = owner._state(db)
            owner._capacity(db)
            owner._validate_occurrence_state_db(db)
            owner._validate_protection_state_db(db)
            owner._validate_takeover_state_db(db)
            owner._bootstrap_db(db)
            owner._actor_boot_id = current["boot_id"]
        return owner

    @staticmethod
    def _validate_binding(binding):
        required = {"session", "settlement", "policy", "policy_digest", "snapshot_digest",
                    "as_of", "valid_until", "max_evidence_age", "lifecycle_tiers",
                    "cap_allocations", "risk_dollars"}
        if not isinstance(binding, dict) or set(binding) != required:
            raise AccountOwnerError("complete runtime binding required")
        if not isinstance(binding["session"], BookSession) or not isinstance(
                binding["settlement"], SettledClose):
            raise AccountOwnerError("typed session and settlement required")
        session = binding["session"]
        settlement = binding["settlement"]
        for name, value in (("session open", session.opens_at),
                            ("risk-add cutoff", session.risk_add_cutoff),
                            ("flatten start", session.flatten_start),
                            ("own-flat deadline", session.own_flat_deadline),
                            ("session close", session.closes_at),
                            ("settled close", settlement.as_of)):
            _time(value, name)
        if not (session.opens_at < session.risk_add_cutoff < session.flatten_start
                < session.own_flat_deadline <= session.closes_at):
            raise AccountOwnerError("invalid bound session schedule")
        if settlement.session_id != session.prior_session_id or settlement.as_of > session.opens_at:
            raise AccountOwnerError("settled close is not the exact prior session")
        for key in ("policy_digest", "snapshot_digest"):
            if (not isinstance(binding[key], str) or len(binding[key]) != 64
                    or any(char not in "0123456789abcdef" for char in binding[key])):
                raise AccountOwnerError(f"invalid {key}")
        if (not isinstance(session.calendar_digest, str) or len(session.calendar_digest) != 64
                or any(char not in "0123456789abcdef" for char in session.calendar_digest)):
            raise AccountOwnerError("invalid calendar digest")
        for key in ("as_of", "valid_until"):
            _time(binding[key], key)
        if binding["valid_until"] <= binding["as_of"]:
            raise AccountOwnerError("invalid evidence validity window")
        if set(binding["lifecycle_tiers"]) != {row.leg_id for row in BOOK_LEGS}:
            raise AccountOwnerError("complete lifecycle binding required")
        if set(binding["cap_allocations"]) != {row.leg_id for row in BOOK_LEGS}:
            raise AccountOwnerError("complete allocation binding required")
        return dict(binding)

    @contextmanager
    def _transaction(self, *, create=False):
        try:
            uri = self.path.resolve().as_uri() + ("?mode=rwc" if create else "?mode=rw")
            with closing(sqlite3.connect(uri, uri=True, timeout=5, isolation_level=None)) as db:
                db.execute("PRAGMA foreign_keys=ON")
                db.execute("PRAGMA synchronous=FULL")
                db.execute("BEGIN IMMEDIATE")
                yield db
                db.commit()
                phase = getattr(self, '_takeover_committed_phase', None)
                self._takeover_committed_phase = None
                if phase is not None and self.crash_at == 'takeover:' + phase:
                    raise SimulatedOwnerCrash('after durable takeover phase ' + phase)
        except AccountOwnerError:
            raise
        except (sqlite3.Error, OSError, ValueError, TypeError) as exc:
            raise AccountOwnerError("account owner state unavailable") from exc

    @staticmethod
    def _validate_schema(db):
        actual = {row[0]: row[1] for row in db.execute(
            "SELECT name, sql FROM sqlite_master WHERE type='table'")}
        names = set(actual)
        if not set(_SCHEMA).issubset(names) or not names.issubset(set(_SCHEMA) | _SETTLEMENT_TABLES):
            raise AccountOwnerError("invalid account owner schema")
        for name, fields in _SCHEMA.items():
            # Column order is durable: inserts deliberately use positional values.
            columns = fields.split(", PRIMARY KEY(")[0].split(", UNIQUE(")[0]
            expected = tuple(part.strip().split()[0] for part in columns.split(","))
            actual_columns = tuple(row[1] for row in db.execute(f"PRAGMA table_info({name})"))
            if actual_columns != expected:
                raise AccountOwnerError("invalid account owner schema columns: " + name)
        from .book_migration import validate_layout
        validate_layout(db, _SCHEMA)

    def _settlement_attachment_state(self, db):
        rows = db.execute(
            "SELECT singleton, body, digest FROM settlement_attachment").fetchall()
        if len(rows) != 1:
            raise AccountOwnerError("settlement attachment authority unavailable")
        singleton, raw, digest = rows[0]
        if (singleton != 1 or not isinstance(raw, str)
                or hashlib.sha256(raw.encode("utf-8")).hexdigest() != digest):
            raise AccountOwnerError("settlement attachment integrity failure")
        try:
            body = json.loads(raw)
        except (TypeError, ValueError):
            raise AccountOwnerError("settlement attachment integrity failure") from None
        status = body.get("status") if isinstance(body, dict) else None
        expected = ({"account", "status"} if status == "NEVER_ATTACHED"
                    else {"account", "status", "attached_utc"})
        if (status not in ("NEVER_ATTACHED", "ATTACHED") or set(body) != expected
                or body.get("account") != self.account
                or (status == "ATTACHED" and not isinstance(body.get("attached_utc"), str))):
            raise AccountOwnerError("settlement attachment identity mismatch")
        tables = {row[0] for row in db.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")}
        required = _SETTLEMENT_TABLES - {"sqlite_sequence"}
        present = tables & required
        if ((status == "ATTACHED" and present != required)
                or (status == "NEVER_ATTACHED" and present)):
            raise AccountOwnerError("settlement attachment/state mismatch")
        return status

    @contextmanager
    def _settlement_transaction(self, *, create=False):
        active = getattr(self._settlement_local, "db", None)
        if active is not None:
            yield active
            return
        with self.serializer.acquire(), self._thread, self._transaction(create=create) as db:
            self._state(db)
            yield db

    @contextmanager
    def _unified_settlement_transaction(self):
        with self.serializer.acquire(), self._thread, self._transaction() as db:
            if getattr(self._settlement_local, "db", None) is not None:
                raise AccountOwnerError("nested unified settlement transaction")
            self._settlement_local.db = db
            self._settlement_local.halt_incident = None
            try:
                yield db
            finally:
                del self._settlement_local.halt_incident
                del self._settlement_local.db

    def _settlement_halt_db(self, db, incident_id, domain, now):
        if domain != "protection":
            raise AccountOwnerError("unknown settlement halt domain")
        self._halt_db(db, incident_id, "protection", now)
        self._settlement_local.halt_incident = incident_id

    def open_settlement(self, *, trusted_keys, now):
        """Seat the accepted settlement component inside this owner's database.

        The owner supplies account, boot/generation-adjacent identity and both
        policy/calendar digests; callers cannot override those runtime bindings.
        Booting or accepting a close never changes account permission.
        """
        from .book_settlement import SettlementStore
        with self._transaction() as db:
            boot_id = self._state(db)["boot_id"]
        store = SettlementStore.boot(
            self.path, self.account, trusted_keys=trusted_keys,
            calendar_digest=self.binding["session"].calendar_digest,
            policy_digest=self.binding["policy_digest"], now=now,
            transaction=self._settlement_transaction, boot_id=boot_id,
            halt_in_transaction=self._settlement_halt_db,
        )
        self.settlement_store = store
        return store

    def issue_settlement_challenge(self, *, scope, target_session_id,
                                   proposed_session_id, package_sha256,
                                   calendar, now):
        if self.settlement_store is None:
            raise AccountOwnerError("settlement store is not attached")
        with self._unified_settlement_transaction() as db:
            if self._settlement_attachment_state(db) != "ATTACHED":
                raise AccountOwnerError("settlement verifier is not durably attached")
            state = self._state(db)
            return self.settlement_store.issue_challenge(
                scope=scope, target_session_id=target_session_id,
                proposed_session_id=proposed_session_id,
                package_sha256=package_sha256,
                halt_generation=state["generation"], permission=state["permission"],
                calendar=calendar, now=now)

    def submit_settlement(self, *, envelope, signature, key_id, package, sources,
                          calendar, now, on_halt=None):
        from .book_settlement import Refusal

        if self.settlement_store is None:
            raise AccountOwnerError("settlement store is not attached")
        with self._unified_settlement_transaction() as db:
            if self._settlement_attachment_state(db) != "ATTACHED":
                raise AccountOwnerError("settlement verifier is not durably attached")
            state = self._state(db)
            if (isinstance(envelope, dict) and envelope.get("scope") == "record_only"
                    and state["permission"] != "HALTED"):
                return Refusal("record_only_requires_halted")
            result = self.settlement_store.submit(
                envelope=envelope, signature=signature, key_id=key_id,
                package=package, sources=sources, halt_generation=state["generation"],
                policy=self.binding["policy"], calendar=calendar, now=now,
                on_halt=None)
            incident_id = (self._settlement_local.halt_incident
                           if getattr(result, "halt_required", False) else None)
        if getattr(result, "halt_required", False) and on_halt is not None:
            on_halt(incident_id, "protection")
        return result

    def record_settlement_revision(self, *, session_id, revised_package, sources,
                                   now, on_halt=None):
        if self.settlement_store is None:
            raise AccountOwnerError("settlement store is not attached")
        with self._unified_settlement_transaction() as db:
            if self._settlement_attachment_state(db) != "ATTACHED":
                raise AccountOwnerError("settlement verifier is not durably attached")
            result = self.settlement_store.record_revision(
                session_id=session_id, revised_package=revised_package,
                sources=sources, now=now, on_halt=None)
            incident_id = (self._settlement_local.halt_incident
                           if getattr(result, "halt_required", False) else None)
        if getattr(result, "halt_required", False) and on_halt is not None:
            on_halt(incident_id, "protection")
        return result

    def _validate_settlement_binding(self, db, now):
        attachment_state = self._settlement_attachment_state(db)
        if self.settlement_store is None:
            if attachment_state == "ATTACHED":
                self._halt_db(db, "settlement-verifier-unavailable:" + now.isoformat(),
                              "protection", now)
                return "settlement_verifier_unavailable"
            return None
        if attachment_state != "ATTACHED":
            self._halt_db(db, "settlement-attachment-invalid:" + now.isoformat(),
                          "protection", now)
            return "settlement_attachment_invalid"
        result = self.settlement_store.settled_close_from(db)
        if not isinstance(result, tuple):
            self._halt_db(db, "settlement-unavailable:" + now.isoformat(),
                          "protection", now)
            return "settlement_unavailable"
        close, _mode = result
        if close != self.binding["settlement"]:
            self._halt_db(db, "settlement-binding:" + now.isoformat(),
                          "protection", now)
            return "settlement_binding_changed"
        return None

    def _state(self, db):
        # Attachment state is part of the account authority, not an optional
        # settlement-side cache. Every account read/mutation validates it so
        # corruption after boot cannot wait for a caller to reopen the verifier.
        self._settlement_attachment_state(db)
        rows = db.execute("SELECT * FROM owner_state").fetchall()
        if len(rows) != 1:
            raise AccountOwnerError("invalid account owner state")
        schema, account, epoch, boot, generation, permission, authority, sequence = rows[0]
        if (schema != getattr(self, '_read_schema_version', 4) or account != self.account or not epoch or not boot
                or type(generation) is not int or generation < 1
                or permission not in ("HALTED", "RUNNING")
                or authority not in ("NORMAL", "SCHEDULED_EXIT", "INTERVENTION")
                or type(sequence) is not int or sequence < 0):
            raise AccountOwnerError("invalid account owner state")
        if self._actor_boot_id is not None and boot != self._actor_boot_id:
            raise AccountOwnerError("stale account owner boot")
        return {"account": account, "account_epoch": epoch, "boot_id": boot,
                "generation": generation, "permission": permission,
                "authority": authority, "sequence": sequence}

    def _next_sequence(self, db):
        state = self._state(db)
        sequence = state["sequence"] + 1
        db.execute("UPDATE owner_state SET sequence=?", (sequence,))
        return sequence

    def _capacity(self, db):
        state = self._state(db)
        result = CapacityState(state["account"], state["account_epoch"])
        rows = db.execute("SELECT sequence, event_id, as_of, fact_type, body "
                          "FROM capacity_events ORDER BY sequence").fetchall()
        for sequence, event_id, at, fact_type, raw in rows:
            data = json.loads(raw)
            if fact_type == "reserve":
                fact = Reserve(**data)
            elif fact_type == "fill":
                fact = CapacityFill(**data)
            elif fact_type == "terminal":
                fact = Terminal(**data)
            elif fact_type == "retire_takeover":
                fact = RetireTakeover(**data)
            elif fact_type == "reduction":
                fact = Reduction(data["reduction_id"], data["close_request_id"],
                                 tuple(tuple(row) for row in data["allocations"]))
            elif fact_type == "takeover":
                proof = data["proof"]
                fact = CompleteTakeover(
                    data["operation_id"],
                    Quiescence(proof["sequence"], tuple(proof["legs"]), proof["gross"],
                               proof["working"], proof["protection"], proof["pending"]),
                )
            else:
                raise AccountOwnerError("unknown retained capacity fact")
            instant = datetime.fromisoformat(at)
            envelope = CapacityEvent(event_id, sequence, instant, state["account"],
                                     state["account_epoch"], fact)
            result = apply_event(result, envelope, now=instant, max_age=MAX_FACT_AGE)
        return result

    def _append_capacity(self, db, fact_type, fact, at, *, event_id):
        sequence = self._next_sequence(db)
        db.execute("INSERT INTO capacity_events VALUES (?, ?, ?, ?, ?)",
                   (sequence, event_id, at.isoformat(), fact_type, _body(asdict(fact))))
        return self._capacity(db)

    def _append_timeline(self, db, kind, ref_id, acquired_at):
        if kind not in ("barrier", "feedback"):
            raise AccountOwnerError("unknown replay timeline kind")
        sequence = self._next_sequence(db)
        db.execute("INSERT INTO timeline VALUES (?, ?, ?, ?)",
                   (sequence, kind, ref_id, acquired_at.isoformat()))

    @property
    def permission(self):
        return self.status()["permission"]

    @property
    def authority(self):
        return self.status()["authority"]

    @property
    def incidents(self):
        with self._transaction() as db:
            self._state(db)
            return tuple({"incident_id": row[0], "reason": row[1], "at": row[2],
                          "generation": row[3]} for row in db.execute(
                              "SELECT incident_id, reason, at, generation FROM incidents "
                              "ORDER BY rowid"))

    @property
    def unresolved_attempts(self):
        with self._transaction() as db:
            self._capacity(db)
            return tuple(row[0] for row in self._unresolved_attempt_rows(db))

    @staticmethod
    def _unresolved_attempt_rows(db):
        return tuple(db.execute(
            "SELECT a.attempt_id, a.operation_id FROM attempts a "
            "JOIN operations o ON o.operation_id=a.operation_id "
            "WHERE (a.state='UNKNOWN' AND o.status NOT IN ('terminal','observed')) "
            "OR o.status IN ('reserved','attempted','takeover_pending') "
            "ORDER BY a.rowid"))

    def _ordinary_unknown_orders_db(self, db, *, now):
        """Derive the account fence from durable attempts, never transport receipts alone."""
        from c1_signal_daemon.book_runtime import BAR_PERIOD
        unresolved = []
        for identity, outcome, created in db.execute(
                "SELECT o.operation_id,a.state,o.created_at FROM operations o "
                "JOIN attempts a USING(operation_id) WHERE o.kind IN ('entry','add')"):
            prepared = datetime.fromisoformat(created)
            if outcome == 'REJECTED':
                continue
            if outcome != 'UNKNOWN' and now < prepared + BAR_PERIOD:
                continue
            resolved = any(fact['kind'] == 'terminal' and fact['operation_id'] == identity
                           and datetime.fromisoformat(fact['as_of']) > prepared
                           for raw, feedback in db.execute('SELECT body,feedback FROM broker_facts')
                           if feedback is not None for fact in (json.loads(raw),))
            if not resolved:
                unresolved.append(identity)
        return tuple(unresolved)

    def status(self):
        """Pure validated read."""
        with self._transaction() as db:
            state = self._state(db)
            self._bootstrap_db(db)
            capacity = self._capacity(db)
            actor = db.execute("SELECT kind FROM runtime_actors WHERE boot_id=?",
                               (state["boot_id"],)).fetchone()
            return {**state, "exposures": tuple((row.leg_id, row.confirmed, row.reserved)
                                                for row in exposures(capacity)),
                    "unresolved_attempts": tuple(row[0] for row in self._unresolved_attempt_rows(db)),
                    "legacy_obligations": tuple(dict(obligation_id=r[0], source_table=r[1], source_id=r[2],
                        kind=r[3], **json.loads(r[4])) for r in db.execute('SELECT * FROM legacy_obligations ORDER BY obligation_id')),
                    "runtime_actor_kind": actor[0] if actor else None,
                    "runtime_binding_digest": db.execute(
                        "SELECT digest FROM runtime_bindings ORDER BY sequence DESC LIMIT 1").fetchone()[0]}

    def register_runtime_actor(self, *, kind, runtime_identities, effective_inputs_sha256):
        """Bind the executing adapter receipt to this exact owner boot."""
        if kind not in ("accepted", "synthetic"):
            raise AccountOwnerError("unknown runtime actor kind")
        body = _body({"runtime_identities": runtime_identities,
                      "effective_inputs_sha256": effective_inputs_sha256})
        with self.serializer.acquire(), self._transaction() as db:
            state = self._state(db)
            if kind == "synthetic":
                if self.synthetic_broker is None:
                    raise AccountOwnerError("synthetic adapters require synthetic broker")
            else:
                retained = json.loads(db.execute(
                    "SELECT body FROM runtime_bindings ORDER BY sequence DESC LIMIT 1").fetchone()[0])
                if (runtime_identities != retained["runtime_identities"]
                        or effective_inputs_sha256 != retained["effective_inputs_sha256"]):
                    raise AccountOwnerError("adapter receipt does not match runtime binding")
            previous = db.execute("SELECT kind, body FROM runtime_actors WHERE boot_id=?",
                                  (state["boot_id"],)).fetchone()
            if previous and previous != (kind, body):
                raise AccountOwnerError("runtime actor changed within boot")
            db.execute("INSERT OR IGNORE INTO runtime_actors VALUES (?, ?, ?)",
                       (state["boot_id"], kind, body))

    def exposure(self, leg_id):
        leg(leg_id)
        with self._transaction() as db:
            row = next(item for item in exposures(self._capacity(db)) if item.leg_id == leg_id)
            return row.confirmed, row.reserved

    def check_source_silence(self, *, now, max_silence):
        """Retain startup monitoring and fence total silence in session coverage."""
        _time(now)
        session = self.binding["session"]
        if not session.opens_at <= now < session.closes_at:
            return
        with self.serializer.acquire(), self._transaction() as db:
            if self._state(db)["authority"] == "INTERVENTION":
                return
            db.execute("INSERT OR IGNORE INTO feed_watch VALUES (?, ?)",
                       (session.session_id, now.isoformat()))
            anchor = datetime.fromisoformat(db.execute(
                "SELECT started_at FROM feed_watch WHERE session_id=?",
                (session.session_id,)).fetchone()[0])
            times = [datetime.fromisoformat(row[0]) for row in db.execute(
                "SELECT bar_time FROM barriers WHERE session_id=?", (session.session_id,))]
            if times:
                anchor = max(times)
            if now > anchor + max_silence:
                self._halt_db(db, "feed-silence:" + session.session_id + ":" + anchor.isoformat(),
                              "feed", now)

    def record_partial_bar(self, leg_id, bar_time, body, *, acquired_at):
        """Durably retain one member of a four-leg barrier before returning."""
        leg(leg_id)
        _time(bar_time, "bar time")
        _time(acquired_at, "bar acquisition time")
        raw = _body(body)
        with self.serializer.acquire(), self._transaction() as db:
            previous = db.execute(
                "SELECT body FROM partial_bars WHERE bar_time=? AND leg_id=?",
                (bar_time.isoformat(), leg_id)).fetchone()
            if previous and previous[0] != raw:
                self._halt_db(db, "bar-conflict:" + bar_time.isoformat(),
                              "barrier", acquired_at)
                raise AccountOwnerError("conflicting bar identity")
            db.execute("INSERT OR IGNORE INTO partial_bars VALUES (?, ?, ?, ?)",
                       (bar_time.isoformat(), leg_id, raw, acquired_at.isoformat()))

    def record_barrier(self, bar_time, body, *, session_id, mode):
        """Atomically promote four partials to one complete input boundary."""
        _time(bar_time, "bar time")
        _text(session_id, "barrier session")
        if not isinstance(mode, Mode):
            raise AccountOwnerError("typed barrier mode required")
        raw = _body(body)
        with self.serializer.acquire(), self._transaction() as db:
            partials = tuple(db.execute(
                "SELECT leg_id, body FROM partial_bars WHERE bar_time=? ORDER BY leg_id",
                (bar_time.isoformat(),)))
            expected = tuple(sorted((leg_id, _body(body[leg_id])) for leg_id in body))
            if partials != expected:
                self._halt_db(db, "barrier-membership:" + bar_time.isoformat(),
                              "barrier", bar_time)
                raise AccountOwnerError("complete barrier does not match retained partials")
            previous = db.execute("SELECT session_id, mode, body FROM barriers WHERE bar_time=?",
                                  (bar_time.isoformat(),)).fetchone()
            identity = (session_id, mode.value, raw)
            if previous and previous != identity:
                self._halt_db(db, "barrier-conflict:" + bar_time.isoformat(),
                              "barrier", bar_time)
                raise AccountOwnerError("conflicting retained barrier")
            inserted = db.execute(
                "INSERT OR IGNORE INTO barriers(bar_time, session_id, mode, body) "
                "VALUES (?, ?, ?, ?)",
                (bar_time.isoformat(), session_id, mode.value, raw)).rowcount
            if inserted:
                self._append_timeline(db, "barrier", bar_time.isoformat(), bar_time)
            db.execute("DELETE FROM partial_bars WHERE bar_time=?", (bar_time.isoformat(),))

    def expire_partial_barrier(self, bar_time, *, now):
        """Atomically fence the account and retire an incomplete boundary."""
        _time(bar_time, "bar time")
        _time(now, "barrier expiry time")
        with self.serializer.acquire(), self._transaction() as db:
            if db.execute("SELECT 1 FROM partial_bars WHERE bar_time=?",
                          (bar_time.isoformat(),)).fetchone() is None:
                return False
            self._halt_db(db, "barrier-expired:" + bar_time.isoformat(), "barrier", now)
            db.execute("DELETE FROM partial_bars WHERE bar_time=?", (bar_time.isoformat(),))
            return True

    def record_barrier_actions(self, bar_time, actions):
        _time(bar_time, "bar time")
        raw = _body(actions)
        with self.serializer.acquire(), self._transaction() as db:
            row = db.execute("SELECT actions FROM barriers WHERE bar_time=?",
                             (bar_time.isoformat(),)).fetchone()
            if row is None:
                raise AccountOwnerError("barrier must precede actions")
            if row[0] is not None and row[0] != raw:
                self._halt_db(db, "action-conflict:" + bar_time.isoformat(),
                              "identity", bar_time)
                raise AccountOwnerError("conflicting retained action batch")
            db.execute("UPDATE barriers SET actions=? WHERE bar_time=?",
                       (raw, bar_time.isoformat()))

    def complete_barrier(self, bar_time):
        _time(bar_time, "bar time")
        with self.serializer.acquire(), self._transaction() as db:
            if db.execute("SELECT 1 FROM barriers WHERE bar_time=?",
                          (bar_time.isoformat(),)).fetchone() is None:
                raise AccountOwnerError("unknown barrier")
            db.execute("UPDATE barriers SET completed=1 WHERE bar_time=?",
                       (bar_time.isoformat(),))

    @property
    def retained_barriers(self):
        with self._transaction() as db:
            self._state(db)
            return tuple({"bar_time": row[0], "session_id": row[1], "mode": row[2],
                          "body": json.loads(row[3]),
                          "actions": None if row[4] is None else json.loads(row[4]),
                          "completed": bool(row[5])}
                         for row in db.execute(
                             "SELECT bar_time, session_id, mode, body, actions, completed "
                             "FROM barriers ORDER BY bar_time"))

    @property
    def retained_partial_bars(self):
        with self._transaction() as db:
            self._state(db)
            return tuple({"bar_time": row[0], "leg_id": row[1],
                          "body": json.loads(row[2]), "acquired_at": row[3]}
                         for row in db.execute(
                             "SELECT bar_time, leg_id, body, acquired_at FROM partial_bars "
                             "ORDER BY bar_time, leg_id"))

    @property
    def replay_timeline(self):
        with self._transaction() as db:
            self._state(db)
            return tuple({"sequence": row[0], "kind": row[1], "ref_id": row[2],
                          "acquired_at": row[3]} for row in db.execute(
                              "SELECT sequence, kind, ref_id, acquired_at FROM timeline "
                              "ORDER BY sequence"))

    @property
    def pending_feedback(self):
        with self._transaction() as db:
            self._state(db)
            return tuple((row[0], json.loads(row[1])) for row in db.execute(
                "SELECT fact_id, body FROM feedback WHERE delivered=0 ORDER BY rowid"))

    @property
    def all_feedback(self):
        with self._transaction() as db:
            self._state(db)
            return tuple({"fact_id": row[0], "body": json.loads(row[1]),
                          "delivered": bool(row[2]),
                          "checkpoint": None if row[3] is None else json.loads(row[3]),
                          "boundary_time": row[4]}
                         for row in db.execute(
                             "SELECT fact_id, body, delivered, checkpoint, boundary_time "
                             "FROM feedback ORDER BY rowid"))

    def acknowledge_feedback(self, fact_id):
        _text(fact_id, "fact")
        with self.serializer.acquire(), self._transaction() as db:
            if db.execute("SELECT 1 FROM feedback WHERE fact_id=?",
                          (fact_id,)).fetchone() is None:
                raise AccountOwnerError("unknown feedback")
            db.execute("UPDATE feedback SET delivered=1 WHERE fact_id=?", (fact_id,))

    def commit_feedback(self, fact_id, checkpoint, *, now):
        """Atomically retain adapter state and discharge one delivery obligation."""
        _text(fact_id, "fact")
        _time(now)
        raw = _body(checkpoint)
        with self.serializer.acquire(), self._transaction() as db:
            row = db.execute("SELECT delivered, checkpoint FROM feedback WHERE fact_id=?",
                             (fact_id,)).fetchone()
            if row is None:
                raise AccountOwnerError("unknown feedback")
            if row[0] and row[1] != raw:
                self._halt_db(db, "checkpoint-conflict:" + fact_id, "identity",
                              now)
                raise AccountOwnerError("conflicting adapter checkpoint")
            db.execute("UPDATE feedback SET delivered=1, checkpoint=? WHERE fact_id=?",
                       (raw, fact_id))

    def record_local_refusal(self, action, reason, *, now, operation_id=None, boundary_time=None):
        """Retain one final owner refusal as adapter feedback before delivery.

        Local policy/capacity decisions have no broker fact, but adapters still
        need a durable rejection to retire the intent.  Transient takeover and
        duplicate-operation responses are deliberately excluded by the runtime.
        """
        with self.serializer.acquire(), self._transaction() as db:
            return self._record_local_refusal_db(db, action, reason, now=now,
                operation_id=operation_id, boundary_time=boundary_time)

    def _record_local_refusal_db(self, db, action, reason, *, now,
                                 operation_id=None, boundary_time=None):
        _time(now)
        _text(reason, "local refusal")
        if not isinstance(action, (OrderIntent, BracketAmend, Cancel)):
            raise AccountOwnerError("typed book action required")
        order_id = (operation_id if isinstance(action, BracketAmend) else action.order_id)
        if isinstance(action, BracketAmend):
            _text(order_id, "refused control operation")
        boundary_time = getattr(action, "bar_time", None) or boundary_time or now
        _time(boundary_time, "local refusal boundary")
        identity = _body({"action": asdict(action), "reason": reason,
                          "boundary_time": boundary_time})
        fact_id = "local-refusal:" + hashlib.sha256(identity.encode("utf-8")).hexdigest()
        event = ExecutionEvent("reject", action.leg_id, boundary_time,
                               order_id=order_id, detail=reason)
        raw = _body(asdict(event))
        previous = db.execute(
            "SELECT body, delivered, boundary_time FROM feedback WHERE fact_id=?",
            (fact_id,),
        ).fetchone()
        expected = (raw, 0, boundary_time.isoformat())
        if previous is not None:
            if previous[0] != raw or previous[2] != boundary_time.isoformat():
                self._halt_db(db, "local-refusal-conflict:" + fact_id,
                              "identity", now)
                raise AccountOwnerError("conflicting local refusal identity")
            return () if previous[1] else (event,)
        db.execute(
            "INSERT INTO feedback(fact_id, body, delivered, boundary_time) "
            "VALUES (?, ?, 0, ?)",
            (fact_id, raw, boundary_time.isoformat()),
        )
        self._append_timeline(db, "feedback", fact_id, now)
        return (event,)

    def observable_accounting(self):
        """Stable replay comparison, excluding boot- and attempt-local UUIDs."""
        with self._transaction() as db:
            state = self._state(db)
            capacity = self._capacity(db)
            operations = tuple(db.execute(
                "SELECT operation_id, leg_id, kind, quantity, status FROM operations ORDER BY operation_id"))
            facts = tuple(db.execute(
                "SELECT fact_id, body FROM broker_facts ORDER BY fact_id"))
            return {
                "permission": state["permission"], "authority": state["authority"],
                "exposures": tuple((row.leg_id, row.confirmed, row.reserved)
                                   for row in exposures(capacity)),
                "operations": operations, "facts": facts,
            }

    def activate_synthetic(self, *, now):
        """One-use, inventory-proven offline bootstrap; never incident recovery."""
        try:
            return self._activate_bootstrap(now=now)
        except (AccountOwnerError, sqlite3.Error, OSError) as exc:
            cause = exc
            while cause is not None:
                if isinstance(cause, (sqlite3.Error, OSError)):
                    self._input_send_suppressed = True
                    break
                cause = cause.__cause__
            raise

    def halt(self, incident_id, reason, *, now):
        _text(incident_id, "incident")
        _time(now)
        if reason not in {"operator", "feed", "control", "barrier", "execution",
                          "protection", "identity", "schedule", "expiry"}:
            raise AccountOwnerError("invalid incident reason")
        with self.serializer.acquire(), self._transaction() as db:
            state = self._state(db)
            previous = db.execute("SELECT reason, at FROM incidents WHERE incident_id=?",
                                  (incident_id,)).fetchone()
            if previous and previous != (reason, now.isoformat()):
                raise AccountOwnerError("conflicting incident identity")
            self._halt_db(db, incident_id, reason, now)

    def record_input_incident(self, incident_id: str, violation: InputViolation,
                              *, source: str, now: datetime) -> None:
        """Commit a bounded diagnostic and authority fence without encoding input."""
        with self.serializer.acquire():
            self._record_input_incident_locked(incident_id, violation, source=source, now=now)

    def _record_input_incident_locked(self, incident_id, violation, *, source, now):
        _text(incident_id, "incident")
        _time(now)
        diagnostic = _canonical({"source": source, "code": violation.code,
                                 "field": violation.field})
        conflict = False
        try:
            with self._transaction() as db:
                previous = db.execute("SELECT reason FROM incidents WHERE incident_id=?",
                                      (incident_id,)).fetchone()
                if previous and previous[0] != diagnostic:
                    conflict = True
                    self._halt_db(db, "input-conflict:" + incident_id, "identity", now)
                else:
                    self._halt_db(db, incident_id, diagnostic, now)
        except Exception:
            self._input_send_suppressed = True
            raise
        if conflict:
            raise AccountOwnerError("conflicting input incident identity")

    def _base_evidence(self, db, leg_id):
        capacity = self._capacity(db)
        remaining = self._open_fill_quantities(db, leg_id, subtract_reservations=False)
        for identity, requested in db.execute(
                "SELECT operation_id, requested FROM operations WHERE leg_id=? "
                "AND kind='entry' ORDER BY rowid DESC", (leg_id,)):
            confirmed = sum(remaining.get(f.execution_id, 0) for f in capacity.fills
                            if f.operation_id == identity)
            if confirmed:
                return identity, requested, confirmed
        return None, 0, 0

    def _open_fill_quantities(self, db, leg_id, *, subtract_reservations=True):
        capacity = self._capacity(db)
        operation_legs = {operation.request.operation_id: operation.request.leg_id
                          for operation in capacity.operations}
        quantities = {}
        for fill in capacity.fills:
            if operation_legs[fill.operation_id] != leg_id:
                continue
            reduced = sum(quantity for reduction in capacity.reductions
                          for identity, quantity in reduction.allocations
                          if identity == fill.execution_id)
            quantities[fill.execution_id] = fill.quantity - reduced
        if not subtract_reservations:
            return quantities
        for close_id, raw in db.execute(
                "SELECT operation_id, allocations FROM close_reservations WHERE status='active'"):
            consumed = {identity: 0 for identity, _quantity in json.loads(raw)}
            for reduction in capacity.reductions:
                if reduction.close_request_id == close_id:
                    for identity, quantity in reduction.allocations:
                        consumed[identity] = consumed.get(identity, 0) + quantity
            for identity, quantity in json.loads(raw):
                if identity in quantities:
                    quantities[identity] -= quantity - consumed.get(identity, 0)
        return quantities

    def _reserve_close(self, db, action):
        available = self._open_fill_quantities(db, action.leg_id)
        if action.scope_fill_ids is not None:
            if len(set(action.scope_fill_ids)) != len(action.scope_fill_ids):
                raise AccountOwnerError("duplicate close scope identity")
            if any(identity not in available for identity in action.scope_fill_ids):
                return None, "unknown_close_scope"
            scoped = [(identity, available[identity]) for identity in action.scope_fill_ids]
        else:
            scoped = list(available.items())
        total = sum(max(0, quantity) for _identity, quantity in scoped)
        requested = total if action.qty is None else action.qty
        if requested <= 0:
            return None, "zero_exposure"
        if requested > total:
            return None, "close_exceeds_confirmed_exposure"
        allocations = []
        remaining = requested
        for identity, quantity in scoped:
            take = min(max(0, quantity), remaining)
            if take:
                allocations.append((identity, take))
                remaining -= take
            if remaining == 0:
                break
        if remaining or not allocations:
            return None, "close_allocation_incomplete"
        db.execute("INSERT INTO close_reservations VALUES (?, ?, 'active')",
                   (action.order_id, _body(allocations)))
        return tuple(allocations), None

    def _context(self, db, action, now):
        state = self._state(db)
        base_id, intended, confirmed = self._base_evidence(db, action.leg_id)
        session = self.binding["session"]
        context = BookAccountContext(
            state["account"], state["account_epoch"], action.order_id, action.leg_id,
            leg(action.leg_id).order_symbol, session.session_id,
            (Mode.PROTECTED if is_protected(
                self.binding["settlement"].equity,
                self.binding["settlement"].peak,
                self.binding["policy"],
            ) else Mode.NORMAL),
            self.binding["policy_digest"], self.binding["snapshot_digest"],
            session.calendar_digest, self.binding["settlement"], leg(action.leg_id).lifecycle_key,
            self.binding["lifecycle_tiers"][action.leg_id], self.binding["as_of"],
            self.binding["valid_until"], intended if action.kind == "add" else 0,
            confirmed if action.kind == "add" else 0, base_id if action.kind == "add" else None,
            tuple(BookExposure(row.leg_id, 0, 0) for row in BOOK_LEGS), (), (),
        )
        context = project_capacity(self._capacity(db), context)
        binding = BookSizingBinding(
            state["account"], state["account_epoch"], self.binding["policy_digest"],
            self.binding["snapshot_digest"], self.binding["settlement"], session,
            self.binding["max_evidence_age"], action.leg_id, leg(action.leg_id).order_symbol,
            self.binding["cap_allocations"][action.leg_id],
            self.binding["risk_dollars"].get(action.leg_id, 0),
        )
        request = BookSizingRequest(
            action.order_id, action.leg_id, leg(action.leg_id).order_symbol,
            action.kind, action.qty if action.kind == "entry" else None,
            Fraction(str(action.stop_dist_pts)) * Fraction(
                str(ADAPTER_BY_LEG[action.leg_id].pointvalue)),
        )
        return request, context, binding

    def _validate_occurrence_state_db(self, db):
        for key, envelope, source, scope, result, state, prepared_at, generation, boot_id in db.execute(
                "SELECT * FROM action_occurrences"):
            try:
                occurrence = ActionOccurrence(**json.loads(envelope))
                source_value = json.loads(source)
                valid = (occurrence_key(occurrence) == key and occurrence.account == self.account
                         and set(source_value) == {"type", "value"}
                         and source_value["type"] in ("OrderIntent", "BracketAmend", "Cancel")
                         and isinstance(source_value["value"], dict)
                         and state in ("prepared", "awaiting_evidence", "takeover_pending", "complete")
                         and type(generation) is int and generation > 0 and bool(boot_id))
                _time(datetime.fromisoformat(prepared_at))
                if scope is not None and not isinstance(json.loads(scope), list):
                    valid = False
                if result is not None:
                    self._restore_dispatch_result(result)
                elif state != "prepared":
                    valid = False
                if not valid:
                    raise ValueError("invalid retained occurrence")
            except (ValueError, TypeError, KeyError) as exc:
                raise AccountOwnerError("invalid retained occurrence") from exc

    def make_occurrence(self, producer, event_id, ordinal=0):
        """Bind caller-supplied provenance to this account's durable identity."""
        with self._transaction() as db:
            state = self._state(db)
        return ActionOccurrence(self.account, state["account_epoch"],
                                self.binding["session"].session_id, producer, event_id, ordinal)

    @staticmethod
    def _occurrence_attempt_db(db, key, operation_id):
        return db.execute("SELECT a.attempt_id, a.state FROM attempts a WHERE a.operation_id=? "
                          "OR a.operation_id IN (SELECT operation_id FROM protection_operations WHERE occurrence_key=?) "
                          "OR substr(a.operation_id,1,?)=? ORDER BY a.rowid DESC LIMIT 1",
                          (operation_id, key, len("control:" + key + ":"), "control:" + key + ":")).fetchone()

    def occurrence_state(self, occurrence):
        with self._transaction() as db:
            row = db.execute("SELECT state, boot_id, generation, result FROM action_occurrences WHERE key=?",
                             (occurrence_key(occurrence),)).fetchone()
            if row is None:
                return None
            result = json.loads(row[3]) if row[3] else {}
            attempted = bool(result.get("attempt_id")) or bool(self._occurrence_attempt_db(
                db, occurrence_key(occurrence), result.get("operation_id")))
            return dict(state=row[0], boot_id=row[1], generation=row[2], attempted=attempted)

    @staticmethod
    def _restore_dispatch_result(raw):
        from c1_signal_daemon.book_protocol import Side
        value = json.loads(raw)
        events = []
        for item in value.pop("confirmed_events", ()):
            item["bar_time"] = datetime.fromisoformat(item["bar_time"])
            if item.get("fill"):
                fill = item["fill"]
                fill["bar_time"] = datetime.fromisoformat(fill["bar_time"])
                fill["side"] = Side(fill["side"])
                item["fill"] = Fill(**fill)
            events.append(ExecutionEvent(**item))
        return DispatchResult(**value, confirmed_events=tuple(events))

    def dispatch(self, action, *, occurrence=None, now):
        try:
            with self.serializer.acquire():
                return self._dispatch_locked(action, occurrence=occurrence, now=now)
        except AccountOwnerError:
            self._input_send_suppressed = True
            raise

    def _dispatch_locked(self, action, *, occurrence=None, now):
        _time(now)
        if getattr(self, "_input_send_suppressed", False):
            raise AccountOwnerError("local send suppression after input incident storage failure")
        violation = validate_action(action)
        if violation is not None:
            self._record_input_incident_locked("input:" + str(uuid4()), violation,
                                              source="direct", now=now)
            raise AccountOwnerError("invalid action: " + violation.code + ":" + violation.field)
        if occurrence is None:
            return DispatchResult(getattr(action, "order_id", None) or "", 0,
                                  refusal_reason="source_occurrence_required")
        try:
            key = occurrence_key(occurrence)
        except (TypeError, ValueError) as exc:
            raise AccountOwnerError("invalid source occurrence") from exc
        self._check_protection_deadlines_locked(now=now)
        operation_id = action.order_id if isinstance(action, OrderIntent) else "control:" + key
        source = _body({"type": type(action).__name__, "value": asdict(action)})
        with self._transaction() as db:
            state = self._state(db)
            previous = db.execute("SELECT source,result,state,generation,boot_id FROM action_occurrences WHERE key=?", (key,)).fetchone()
            if previous is not None:
                if previous[0] != source:
                    self._halt_db(db, "occurrence-conflict:" + key, "identity", now)
                    return DispatchResult(operation_id, 0, refusal_reason="occurrence_conflict")
                attempt = self._occurrence_attempt_db(db, key, operation_id)
                if attempt and previous[2] in ("awaiting_evidence", "takeover_pending"):
                    retained = DispatchResult(operation_id, 0, attempt[0], attempt[1].lower(), "retained_attempt")
                    db.execute("UPDATE action_occurrences SET result=?, state='complete' WHERE key=?",
                               (_body(asdict(retained)), key))
                    return retained
                continuation = (previous[2] in ("awaiting_evidence", "takeover_pending")
                                and previous[3] == state["generation"] and previous[4] == state["boot_id"]
                                and not attempt)
                if not continuation:
                    return (self._restore_dispatch_result(previous[1]) if previous[1] else
                            DispatchResult(operation_id, 0, refusal_reason="retained_preparation"))
            else:
                if (occurrence.account != self.account or occurrence.account_epoch != state["account_epoch"]
                        or occurrence.session_id != self.binding["session"].session_id):
                    self._halt_db(db, "occurrence-binding:" + key, "identity", now)
                    return DispatchResult(operation_id, 0, refusal_reason="occurrence_binding_conflict")
                db.execute("INSERT INTO action_occurrences VALUES (?, ?, ?, NULL, NULL, 'prepared', ?, ?, ?)",
                           (key, _body(asdict(occurrence)), source, now.isoformat(), state["generation"], state["boot_id"]))
        if isinstance(action, BracketAmend):
            result = self._dispatch_protection_locked(action, occurrence, key, now=now)
        elif isinstance(action, Cancel) and action.order_id is None:
            with self._transaction() as db:
                row = db.execute("SELECT scope FROM action_occurrences WHERE key=?", (key,)).fetchone()
                if row[0] is None:
                    targets = tuple(o.request.operation_id for o in self._capacity(db).operations
                                    if o.request.leg_id == action.leg_id and o.status == "active" and o.terminal is None)
                    db.execute("UPDATE action_occurrences SET scope=? WHERE key=?", (_body(targets), key))
                else:
                    targets = tuple(json.loads(row[0]))
            results = tuple(self._dispatch_action_locked(Cancel(action.leg_id, target), occurrence=occurrence,
                             operation_id=operation_id + ":" + str(index), now=now)
                            for index, target in enumerate(targets))
            states = {item.transport_state for item in results}
            result = DispatchResult(operation_id, 0,
                transport_state=next((item for item in ("unknown", "rejected", "accepted") if item in states), "not_attempted"),
                refusal_reason=next((item.refusal_reason for item in results if item.refusal_reason not in (None, "duplicate_operation")), None),
                confirmed_events=tuple(event for item in results for event in item.confirmed_events))
        else:
            result = self._dispatch_action_locked(action, occurrence=occurrence, operation_id=operation_id, now=now)
        with self._transaction() as db:
            disposition = result.refusal_reason if result.refusal_reason in ("awaiting_evidence", "takeover_pending") else "complete"
            db.execute("UPDATE action_occurrences SET result=?,state=? WHERE key=?", (_body(asdict(result)), disposition, key))
        return result

    def _dispatch_action_locked(self, action, *, occurrence, operation_id, now):
        action_body = _body(asdict(action))
        if isinstance(action, (OrderIntent, BracketAmend)) and action.scope_fill_ids == ():
            return DispatchResult(operation_id, 0, refusal_reason="empty_scope")
        with self._thread:
            with self._transaction() as db:
                state = self._state(db)
                settlement_refusal = self._validate_settlement_binding(db, now)
                if settlement_refusal is not None:
                    return DispatchResult(operation_id, 0, refusal_reason=settlement_refusal)
                if state["authority"] == "INTERVENTION":
                    return DispatchResult(operation_id, 0, refusal_reason="intervention_fence")
                if (state["authority"] == "SCHEDULED_EXIT" and occurrence.producer != "schedule"
                        and not (isinstance(action, OrderIntent) and action.kind in ("entry", "add"))):
                    return DispatchResult(operation_id, 0, refusal_reason="scheduled_operation_required")
                existing = db.execute("SELECT body, quantity, status FROM operations WHERE operation_id=?",
                                      (operation_id,)).fetchone()
                ready_takeover = False
                if existing:
                    if existing[0] != action_body:
                        self._halt_db(db, "identity:" + operation_id, "identity", now)
                        return DispatchResult(operation_id, 0, refusal_reason="operation_identity_conflict")
                    if existing[2] == "takeover_pending":
                        capacity_operation = next(o for o in self._capacity(db).operations
                                                  if o.request.operation_id == operation_id)
                        if capacity_operation.status == "active":
                            ready_takeover = True
                            quantity = existing[1]
                        else:
                            return DispatchResult(operation_id, existing[1],
                                                  refusal_reason="takeover_pending")
                    else:
                        return DispatchResult(operation_id, existing[1], refusal_reason="duplicate_operation")
                if isinstance(action, OrderIntent):
                    expected = leg(action.leg_id).entry_side
                    if action.kind in ("exit", "flat"):
                        expected = opposite(expected)
                    if action.side is not expected:
                        return DispatchResult(operation_id, 0, refusal_reason="order_side_mismatch")
                if isinstance(action, Cancel):
                    target = db.execute(
                        "SELECT leg_id, kind, status FROM operations WHERE operation_id=?",
                        (action.order_id,)).fetchone()
                    pending = next((o for o in self._capacity(db).operations
                                    if o.request.operation_id == action.order_id), None)
                    if (target is None or target[0] != action.leg_id
                            or target[1] not in ("entry", "add")
                            or target[2] not in ("reserved", "attempted")
                            or pending is None or pending.status != "active"
                            or pending.terminal is not None):
                        return DispatchResult(operation_id, 0, refusal_reason="invalid_cancel_target")
                if ready_takeover:
                    session = self.binding["session"]
                    generation = db.execute(
                        "SELECT generation FROM operations WHERE operation_id=?",
                        (operation_id,)).fetchone()[0]
                    refusal = None
                    if (state["permission"] != "RUNNING" or state["authority"] != "NORMAL"
                            or generation != state["generation"]
                            or not session.opens_at <= now < session.risk_add_cutoff):
                        refusal = "risk_add_not_authorized"
                    elif not self.binding["as_of"] <= now < self.binding["valid_until"]:
                        refusal = "stale_or_future_account_evidence"
                    elif now - self.binding["as_of"] > self.binding["max_evidence_age"]:
                        refusal = "stale_account_evidence"
                    if refusal is None:
                        refusal = self._revalidate_takeover_db(db, operation_id, now=now)
                    if refusal is not None:
                        return self._retire_takeover_db(db, action, refusal, now)
                    db.execute("UPDATE operations SET status='reserved' WHERE operation_id=?",
                               (operation_id,))
                elif isinstance(action, OrderIntent) and action.kind in ("entry", "add"):
                    if state["permission"] != "RUNNING" or state["authority"] != "NORMAL":
                        return DispatchResult(operation_id, 0, refusal_reason="risk_add_not_authorized")
                    if self._ordinary_unknown_orders_db(db, now=now):
                        return DispatchResult(operation_id, 0, refusal_reason="unknown_order")
                    request, context, sized_binding = self._context(db, action, now)
                    decision = size_book_request(request, context=context, binding=sized_binding,
                                                 policy=self.binding["policy"], now=now)
                    if decision.halt:
                        return DispatchResult(operation_id, 0,
                                              refusal_reason=decision.halt_reason)
                    if decision.qty_out == 0:
                        return DispatchResult(operation_id, 0, refusal_reason="zero_size")
                    quantity = decision.qty_out
                    reserve = Reserve(operation_id, action.leg_id,
                                      leg(action.leg_id).order_symbol, quantity)
                    capacity = self._append_capacity(db, "reserve", reserve, now,
                                                     event_id="reserve:" + operation_id)
                    operation = next(o for o in capacity.operations
                                     if o.request.operation_id == operation_id)
                    if operation.status != "active":
                        db.execute("INSERT INTO operations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                   (operation_id, action.leg_id, leg(action.leg_id).order_symbol,
                                    action.kind, action.qty, quantity,
                                    self.binding["session"].session_id, state["generation"],
                                    now.isoformat(),
                                    "takeover_pending" if operation.status == "takeover" else "refused",
                                    action_body))
                        if operation.status == 'takeover':
                            self._publish_takeover_db(db, action, occurrence, quantity, now)
                        return DispatchResult(
                            operation_id, quantity if operation.status == "takeover" else 0,
                            refusal_reason=("takeover_pending" if operation.status == "takeover"
                                            else "insufficient_observed_capacity"))
                elif isinstance(action, OrderIntent):
                    if state["authority"] not in ("NORMAL", "SCHEDULED_EXIT"):
                        return DispatchResult(operation_id, 0, refusal_reason="mutation_not_authorized")
                    allocations, close_refusal = self._reserve_close(db, action)
                    if close_refusal is not None:
                        return DispatchResult(operation_id, 0, refusal_reason=close_refusal)
                    quantity = sum(row[1] for row in allocations)
                else:
                    if state["authority"] not in ("NORMAL", "SCHEDULED_EXIT"):
                        return DispatchResult(operation_id, 0, refusal_reason="mutation_not_authorized")
                    quantity = 0
                if not ready_takeover:
                    db.execute("INSERT INTO operations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                               (operation_id, action.leg_id, leg(action.leg_id).order_symbol,
                                getattr(action, "kind", type(action).__name__.lower()),
                                getattr(action, "qty", None), quantity,
                                self.binding["session"].session_id, state["generation"],
                                now.isoformat(), "reserved", action_body))
            if self.crash_at == "after_reservation":
                raise SimulatedOwnerCrash("after durable reservation")
            with self._transaction() as db:
                state = self._state(db)
                attempt_id = str(uuid4())
                command = BrokerCommand(
                    attempt_id, operation_id, action.leg_id,
                    getattr(action, "kind", type(action).__name__.lower()),
                    getattr(getattr(action, "side", None), "value", None), quantity,
                    leg(action.leg_id).order_symbol, state["authority"], state["generation"],
                    replace(action, qty=quantity) if isinstance(action, OrderIntent) else action,
                    action.order_id if isinstance(action, Cancel) else None,
                    occurrence,
                )
                db.execute("INSERT INTO attempts VALUES (?, ?, 'UNKNOWN', ?, ?, NULL)",
                           (attempt_id, operation_id, state["generation"], _body(asdict(command))))
                db.execute("UPDATE operations SET status='attempted' WHERE operation_id=?",
                           (operation_id,))
                if ready_takeover:
                    self._takeover_event_db(db, operation_id, 'ATTEMPTED', now, attempt_id=attempt_id)
            if self.crash_at == "before_send":
                raise SimulatedOwnerCrash("after attempt journal before send")
            if self.synthetic_broker is None:
                return DispatchResult(operation_id, quantity, attempt_id=attempt_id,
                                      refusal_reason="production_route_unavailable")
            try:
                result = self.synthetic_broker.send(command)
            except Exception:  # bytes may have left; UNKNOWN is retained
                result = BrokerResult("unknown")
            if self.crash_at == "after_send":
                raise SimulatedOwnerCrash("after transport before fact journal")
            events = []
            facts = result.facts
            if result.state == "rejected" and not facts:
                facts = (BrokerFact.terminal(operation_id, "rejected", 0, now),)
            for fact in facts:
                events.extend(self._observe_locked(
                    fact, now=now,
                    boundary_time=getattr(action, "bar_time", None) or now))
            with self._transaction() as db:
                db.execute("UPDATE attempts SET state=?, observation=? WHERE attempt_id=?",
                           (result.state.upper(), _body({"state": result.state,
                                                        "facts": [f.fact_id for f in facts]}), attempt_id))
            return DispatchResult(operation_id, quantity, attempt_id, result.state,
                                  confirmed_events=tuple(events))

    def _flatten_action(self, db, root_id, leg_id, reason, now):
        """Keep an unresolved close intact; allocate a new identity for its remainder."""
        prefix = root_id + ":remainder:"
        rows = tuple(db.execute(
            "SELECT operation_id, status FROM operations WHERE operation_id=? "
            "OR substr(operation_id, 1, ?)=?", (root_id, len(prefix), prefix)))
        if any(status != "terminal" for _identity, status in rows):
            return None
        quantity = sum(self._open_fill_quantities(db, leg_id).values())
        if quantity <= 0:
            return None
        identity = root_id if not rows else prefix + str(len(rows))
        return OrderIntent(identity, leg_id, "flat", opposite(leg(leg_id).entry_side),
                           quantity, bar_time=now, reason=reason)

    def advance_schedule(self, *, now):
        with self.serializer.acquire():
            return self._advance_schedule_locked(now=now)

    def _advance_schedule_locked(self, *, now):
        """Apply cutoff, scheduled flatten and deadline using the bound session clock."""
        _time(now)
        session = self.binding["session"]
        try:
            phase = classify_schedule(session, now)
        except ScheduleError:
            with self._transaction() as db:
                self._halt_db(db, "schedule-missing:" + session.session_id, "schedule", now)
            return ()
        actions = []
        retired = []
        with self._thread, self._transaction() as db:
            state = self._state(db)
            if state["authority"] == "INTERVENTION":
                return ()
            capacity = self._capacity(db)
            if phase in (SchedulePhase.CUTOFF, SchedulePhase.FLATTEN,
                         SchedulePhase.DEADLINE) and state["authority"] == "NORMAL":
                db.execute("UPDATE owner_state SET permission='HALTED', authority='SCHEDULED_EXIT', "
                           "generation=generation+1")
                for raw, in tuple(db.execute(
                        "SELECT body FROM operations WHERE status='takeover_pending'")):
                    retired.append(self._retire_takeover_db(
                        db, self._restore_intent(raw), "risk_add_not_authorized", now))
                capacity = self._capacity(db)
                for operation in capacity.operations:
                    if (operation.status == "active" and operation.terminal is None
                            and operation.request.leg_id in {row.leg_id for row in BOOK_LEGS}):
                        actions.append(Cancel(operation.request.leg_id,
                                              operation.request.operation_id))
            if phase in (SchedulePhase.FLATTEN, SchedulePhase.DEADLINE):
                for exposure in exposures(capacity):
                    if exposure.confirmed:
                        if any(operation.request.leg_id == exposure.leg_id
                               and operation.status == 'active' and operation.terminal is None
                               for operation in capacity.operations):
                            continue
                        operation_id = "scheduled-flat:" + session.session_id + ":" + exposure.leg_id
                        action = self._flatten_action(db, operation_id, exposure.leg_id,
                                                      "scheduled_flatten", now)
                        if action is not None:
                            actions.append(action)
        results = tuple(retired) + tuple(self._dispatch_locked(
            action, occurrence=self.make_occurrence("schedule", session.session_id + ":" +
                (action.order_id if isinstance(action, OrderIntent) else "cancel:" + action.order_id)),
            now=now) for action in actions)
        if phase is SchedulePhase.DEADLINE:
            with self._thread, self._transaction() as db:
                if self._state(db)["authority"] == "SCHEDULED_EXIT":
                    capacity = self._capacity(db)
                    unresolved = bool(self._unresolved_attempt_rows(db))
                    occupied = any(row.confirmed or row.reserved for row in exposures(capacity))
                    if unresolved or occupied:
                        self._halt_db(db, "own-flat-deadline:" + session.session_id,
                                      "schedule", now)
        return results

    def advance_takeover(self, *, now):
        with self.serializer.acquire():
            try:
                return self._advance_takeover_locked(now=now)
            except Exception:
                self._input_send_suppressed = True
                raise

    @staticmethod
    def _restore_intent(raw):
        from c1_signal_daemon.book_protocol import Bracket, FillTiming, Side
        value = json.loads(raw)
        value["side"] = Side(value["side"])
        value["timing"] = FillTiming(value["timing"])
        if value["bar_time"] is not None:
            value["bar_time"] = datetime.fromisoformat(value["bar_time"])
        if value["bracket"] is not None:
            value["bracket"] = Bracket(**value["bracket"])
        if value["scope_fill_ids"] is not None:
            value["scope_fill_ids"] = tuple(value["scope_fill_ids"])
        return OrderIntent(**value)

    def _retire_takeover_db(self, db, action, reason, now):
        identity = action.order_id
        if db.execute("SELECT 1 FROM attempts WHERE operation_id=?", (identity,)).fetchone():
            raise AccountOwnerError("cannot locally retire an attempted takeover")
        operation = next(o for o in self._capacity(db).operations
                         if o.request.operation_id == identity)
        if operation.status == "takeover":
            self._append_capacity(db, "retire_takeover", RetireTakeover(identity), now,
                                  event_id="takeover-refused:" + identity)
        else:
            self._append_capacity(db, "terminal", Terminal(identity, "rejected", 0), now,
                                  event_id="takeover-refused:" + identity)
        db.execute("UPDATE operations SET status='terminal' WHERE operation_id=?", (identity,))
        if self._takeover_plan_db(db, identity) is not None:
            self._takeover_event_db(db, identity, 'RETIRED', now, reason=reason)
        events = self._record_local_refusal_db(db, action, reason, now=now)
        return DispatchResult(identity, 0, refusal_reason=reason, confirmed_events=events)

    def resume_takeover(self, *, now):
        """Advance retained controls and dispatch an admitted, unattempted takeover."""

        with self.serializer.acquire():
            try:
                controls, _completed = self._advance_takeover_locked(now=now)
                with self._transaction() as db:
                    capacity = self._capacity(db)
                    ready = {o.request.operation_id for o in capacity.operations if o.status == "active"}
                    rows = tuple(db.execute(
                        "SELECT operation_id, body FROM operations WHERE status='takeover_pending'"))
                results = list(controls)
                for identity, raw in rows:
                    if identity not in ready:
                        continue
                    with self._transaction() as db:
                        occurrence_row = next((row for row in db.execute(
                            "SELECT envelope, source FROM action_occurrences WHERE state='takeover_pending'")
                            if json.loads(row[1])["value"].get("order_id") == identity), None)
                    if occurrence_row is None:
                        raise AccountOwnerError("takeover source occurrence missing")
                    occurrence = ActionOccurrence(**json.loads(occurrence_row[0]))
                    results.append(self._dispatch_locked(self._restore_intent(raw), occurrence=occurrence, now=now))
                return tuple(results)
            except Exception:
                self._input_send_suppressed = True
                raise

    def _halt_db(self, db, incident_id, reason, now):
        try:
            state = self._state(db)
            inserted = db.execute("INSERT OR IGNORE INTO incidents VALUES (?, ?, ?, ?)",
                                  (incident_id, reason, now.isoformat(), state["generation"])).rowcount
            db.execute("UPDATE owner_state SET permission='HALTED', authority='INTERVENTION', "
                       "generation=generation+?", (1 if inserted else 0,))
            if inserted:
                self._invalidate_bootstrap_db(db, 'incident:' + incident_id)
                for identity, in tuple(db.execute('SELECT operation_id FROM takeover_plans')):
                    if self._takeover_phase_db(db, identity) not in ('ATTEMPTED', 'RETIRED'):
                        self._takeover_event_db(db, identity, 'HALT', now, incident_id=incident_id)
        except (sqlite3.Error, OSError, AccountOwnerError):
            self._input_send_suppressed = True
            raise

    def observe(self, fact, *, now):
        with self.serializer.acquire():
            return self._observe_locked(fact, now=now, boundary_time=fact.as_of)

    def _observe_locked(self, fact, *, now, boundary_time=None, db=None):
        if not isinstance(fact, BrokerFact):
            raise AccountOwnerError("typed broker fact required")
        _time(now)
        try:
            _time(fact.as_of, "fact time")
        except AccountOwnerError:
            with (self._transaction() if db is None else nullcontext(db)) as db:
                self._halt_db(db, "fact-time:" + str(uuid4()), "execution", now)
            return ()
        if fact.kind == "fill":
            try:
                price = require_finite_number(fact.price, field="fill price", strictly_positive=True)
                if type(fact.price) not in (int, float):
                    fact = replace(fact, price=price)
            except (ValueError, TypeError, OverflowError):
                with (self._transaction() if db is None else nullcontext(db)) as db:
                    self._halt_db(db, "invalid-fill-price:" + str(fact.fact_id), "execution", now)
                return ()
        with (self._transaction() if db is None else nullcontext(db)) as db:
            previous = db.execute("SELECT body, feedback FROM broker_facts WHERE fact_id=?",
                                  (fact.fact_id,)).fetchone()
            raw = _body(asdict(fact))
            if previous:
                if previous[0] != raw:
                    self._halt_db(db, "fact-conflict:" + fact.fact_id, "execution", now)
                return ()
            if not timedelta(0) <= now - fact.as_of <= MAX_FACT_AGE:
                db.execute("INSERT INTO broker_facts VALUES (?, ?, NULL)", (fact.fact_id, raw))
                self._halt_db(db, "stale-fact:" + fact.fact_id, "execution", now)
                return ()
            operation = db.execute("SELECT leg_id, kind, body FROM operations WHERE operation_id=?",
                                   (fact.operation_id,)).fetchone()
            if operation is None:
                db.execute("INSERT INTO broker_facts VALUES (?, ?, NULL)", (fact.fact_id, raw))
                self._halt_db(db, "unknown-fact:" + fact.fact_id, "execution", now)
                return ()
            leg_id, operation_kind, operation_body = operation
            if (fact.kind == "fill"
                    and (fact.leg_id != leg_id or fact.order_kind != operation_kind)):
                db.execute("INSERT INTO broker_facts VALUES (?, ?, NULL)",
                           (fact.fact_id, raw))
                self._halt_db(db, "fact-identity:" + fact.fact_id,
                              "execution", now)
                return ()
            boundary_time = ((boundary_time or fact.as_of).isoformat()
                             if isinstance(boundary_time or fact.as_of, datetime)
                             else json.loads(operation_body).get("bar_time"))
            feedback = None
            if fact.kind == "fill" and fact.order_kind in ("entry", "add"):
                capacity_fact = CapacityFill(fact.fact_id, fact.operation_id, fact.quantity)
                capacity = self._append_capacity(db, "fill", capacity_fact, fact.as_of,
                                                 event_id="fill:" + fact.fact_id)
                fill = Fill(fact.fact_id, fact.operation_id, leg_id, fact.order_kind,
                            leg(leg_id).entry_side, fact.quantity, fact.price, fact.as_of)
                feedback = ExecutionEvent("fill", leg_id, fact.as_of, fill=fill,
                                          order_id=fact.operation_id)
            elif fact.kind == "fill" and fact.order_kind in ("exit", "flat"):
                if not fact.entry_execution_id:
                    self._halt_db(db, "unallocated-reduction:" + fact.fact_id,
                                  "execution", now)
                    db.execute("INSERT INTO broker_facts VALUES (?, ?, NULL)",
                               (fact.fact_id, raw))
                    return ()
                close_row = db.execute(
                    "SELECT allocations, status FROM close_reservations WHERE operation_id=?",
                    (fact.operation_id,)).fetchone()
                if close_row is None or close_row[1] != "active":
                    self._halt_db(db, "unowned-reduction:" + fact.fact_id,
                                  "execution", now)
                    db.execute("INSERT INTO broker_facts VALUES (?, ?, NULL)",
                               (fact.fact_id, raw))
                    return ()
                allocations = dict(json.loads(close_row[0]))
                already = sum(quantity for reduction in self._capacity(db).reductions
                              if reduction.close_request_id == fact.operation_id
                              for identity, quantity in reduction.allocations
                              if identity == fact.entry_execution_id)
                if (fact.entry_execution_id not in allocations
                        or fact.quantity > allocations[fact.entry_execution_id] - already):
                    self._halt_db(db, "reduction-allocation:" + fact.fact_id,
                                  "execution", now)
                    db.execute("INSERT INTO broker_facts VALUES (?, ?, NULL)",
                               (fact.fact_id, raw))
                    return ()
                reduction = Reduction(fact.fact_id, fact.operation_id,
                                      ((fact.entry_execution_id, fact.quantity),))
                capacity = self._append_capacity(db, "reduction", reduction, fact.as_of,
                                                 event_id="reduction:" + fact.fact_id)
                fill = Fill(fact.fact_id, fact.operation_id, leg_id, fact.order_kind,
                            opposite(leg(leg_id).entry_side), fact.quantity, fact.price,
                            fact.as_of, entry_fill_id=fact.entry_execution_id)
                feedback = ExecutionEvent("fill", leg_id, fact.as_of, fill=fill,
                                          order_id=fact.operation_id)
                consumed = sum(quantity for reduction in capacity.reductions
                               if reduction.close_request_id == fact.operation_id
                               for _identity, quantity in reduction.allocations)
                if consumed == sum(allocations.values()):
                    db.execute("UPDATE close_reservations SET status='filled' WHERE operation_id=?",
                               (fact.operation_id,))
                    db.execute("UPDATE operations SET status='terminal' WHERE operation_id=?",
                               (fact.operation_id,))
            elif fact.kind == "terminal":
                if operation_kind in ("cancel", "bracketamend"):
                    if fact.status != "rejected" or type(fact.cumulative_filled) is not int \
                            or fact.cumulative_filled != 0:
                        self._halt_db(db, "invalid-control-terminal:" + fact.fact_id,
                                      "execution", now)
                        db.execute("INSERT INTO broker_facts VALUES (?, ?, NULL)", (fact.fact_id, raw))
                        return ()
                    db.execute("UPDATE operations SET status='terminal' WHERE operation_id=?",
                               (fact.operation_id,))
                    capacity = self._capacity(db)
                elif operation_kind in ("exit", "flat"):
                    close_row = db.execute(
                        "SELECT allocations, status FROM close_reservations WHERE operation_id=?",
                        (fact.operation_id,)).fetchone()
                    if (close_row is None or close_row[1] not in ("active", "filled")
                            or (close_row[1] == "filled" and fact.status != "filled")):
                        self._halt_db(db, "unknown-close-terminal:" + fact.fact_id,
                                      "execution", now)
                        db.execute("INSERT INTO broker_facts VALUES (?, ?, NULL)",
                                   (fact.fact_id, raw))
                        return ()
                    consumed = sum(quantity for reduction in self._capacity(db).reductions
                                   if reduction.close_request_id == fact.operation_id
                                   for _identity, quantity in reduction.allocations)
                    allocated = sum(quantity for _identity, quantity in json.loads(close_row[0]))
                    if (fact.status not in ("filled", "cancelled", "rejected")
                            or type(fact.cumulative_filled) is not int
                            or fact.cumulative_filled != consumed
                            or (fact.status == "filled" and consumed != allocated)):
                        self._halt_db(db, "close-terminal-gap:" + fact.fact_id,
                                      "execution", now)
                        db.execute("INSERT INTO broker_facts VALUES (?, ?, NULL)",
                                   (fact.fact_id, raw))
                        return ()
                    db.execute("UPDATE close_reservations SET status=? WHERE operation_id=?",
                               (fact.status, fact.operation_id))
                    db.execute("UPDATE operations SET status='terminal' WHERE operation_id=?",
                               (fact.operation_id,))
                    capacity = self._capacity(db)
                else:
                    terminal = Terminal(fact.operation_id, fact.status, fact.cumulative_filled)
                    capacity = self._append_capacity(db, "terminal", terminal, fact.as_of,
                                                     event_id=fact.fact_id)
                    db.execute("UPDATE operations SET status='terminal' WHERE operation_id=?",
                               (fact.operation_id,))
                feedback = ExecutionEvent(
                    "reject" if fact.status == "rejected" else "cancel",
                    leg_id, fact.as_of, order_id=fact.operation_id,
                    detail=fact.status,
                )
            else:
                self._halt_db(db, "invalid-fact:" + fact.fact_id, "execution", now)
                db.execute("INSERT INTO broker_facts VALUES (?, ?, NULL)", (fact.fact_id, raw))
                return ()
            expected_takeover_block = (capacity.takeover is not None and
                                       capacity.blocks == ("takeover:" +
                                                           capacity.takeover.operation_id,))
            if capacity.blocks and not expected_takeover_block:
                self._halt_db(db, "capacity-fact:" + fact.fact_id, "execution", now)
                db.execute("INSERT INTO broker_facts VALUES (?, ?, NULL)", (fact.fact_id, raw))
                return ()
            if fact.kind == "fill" and fact.order_kind in ("entry", "add"):
                from .book_migration import quarantine_late_fill
                if not quarantine_late_fill(db, fact):
                    self._register_protection_fill_db(db, fact, operation_body)
            if fact.kind == "terminal" and operation_kind in ("entry", "add"):
                for control_id, control_body in tuple(db.execute(
                        "SELECT operation_id, body FROM operations "
                        "WHERE kind='cancel' AND leg_id=? AND status='attempted'", (leg_id,))):
                    if json.loads(control_body)["order_id"] == fact.operation_id:
                        db.execute("UPDATE operations SET status='observed' WHERE operation_id=?",
                                   (control_id,))
            feedback_raw = _body(asdict(feedback))
            db.execute("INSERT INTO broker_facts VALUES (?, ?, ?)",
                       (fact.fact_id, raw, feedback_raw))
            db.execute("INSERT INTO feedback(fact_id, body, delivered, boundary_time) VALUES (?, ?, 0, ?)",
                       (fact.fact_id, feedback_raw, boundary_time))
            self._append_timeline(db, "feedback", fact.fact_id, now)
            return (feedback,)


def opposite(side):
    from c1_signal_daemon.book_protocol import Side
    return Side.SELL if side is Side.BUY else Side.BUY


def replace_dict(value, **updates):
    result = dict(value)
    result.update(updates)
    return result
