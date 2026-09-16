"""Durable offline four-leg account owner.

The owner serializes every mutation, reserves capacity before dispatch and treats
transport acceptance as no execution evidence.  A ``SyntheticBroker`` is an
explicit Python-only test seam; no configuration or HTTP path can construct it.
Every boot starts HALTED with a fresh boot/generation while retained operations,
attempts, facts and reservations remain owned.
"""
from __future__ import annotations

from contextlib import closing, contextmanager
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

from .book_account_lock import AccountSerializer
from .book_capacity import (
    CapacityState,
    CompleteTakeover,
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
    target_operation_id: str | None = None


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
}

_SETTLEMENT_TABLES = {
    "state", "chain", "superseded_chain", "packages", "sources", "b7_history",
    "challenges", "events", "receipts", "sqlite_sequence",
}


class BookAccountOwner:
    """Single durable account writer; production transport is intentionally absent."""

    def __init__(self, path, account, binding, synthetic_broker, crash_at=None):
        self.path = Path(path)
        self.account = _text(account, "account")
        self.binding = self._validate_binding(binding)
        if synthetic_broker is not None and not (
                isinstance(synthetic_broker, SyntheticBroker) and synthetic_broker.synthetic):
            raise AccountOwnerError("only the explicit SyntheticBroker test seam is supported")
        self.synthetic_broker = synthetic_broker
        if crash_at not in (None, "after_reservation", "before_send", "after_send"):
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
        existed = owner.path.exists()
        with owner.serializer.acquire(), owner._transaction(create=True) as db:
            tables = {row[0] for row in db.execute(
                "SELECT name FROM sqlite_master WHERE type='table'")}
            if not tables:
                if existed:
                    raise AccountOwnerError("account owner state unavailable")
                for name, fields in _SCHEMA.items():
                    db.execute(f"CREATE TABLE {name} ({fields})")
                db.execute("INSERT INTO owner_state VALUES (1, ?, ?, ?, 1, 'HALTED', "
                           "'INTERVENTION', 0)",
                           (owner.account, str(uuid4()), str(uuid4())))
                record = _binding_record(owner.binding)
                raw = _body(record)
                db.execute("INSERT INTO runtime_bindings(session_id, body, digest) VALUES (?, ?, ?)",
                           (owner.binding["session"].session_id, raw,
                            hashlib.sha256(raw.encode("utf-8")).hexdigest()))
            else:
                owner._validate_schema(db)
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
                db.execute("UPDATE owner_state SET boot_id=?, generation=generation+1, "
                           "permission='HALTED', authority='INTERVENTION'", (str(uuid4()),))
            current = owner._state(db)
            owner._capacity(db)
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
            state = self._state(db)
            return self.settlement_store.issue_challenge(
                scope=scope, target_session_id=target_session_id,
                proposed_session_id=proposed_session_id,
                package_sha256=package_sha256,
                halt_generation=state["generation"], permission=state["permission"],
                calendar=calendar, now=now)

    def submit_settlement(self, *, envelope, signature, key_id, package, sources,
                          calendar, now, on_halt=None):
        if self.settlement_store is None:
            raise AccountOwnerError("settlement store is not attached")
        with self._unified_settlement_transaction() as db:
            state = self._state(db)
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
            result = self.settlement_store.record_revision(
                session_id=session_id, revised_package=revised_package,
                sources=sources, now=now, on_halt=None)
            incident_id = (self._settlement_local.halt_incident
                           if getattr(result, "halt_required", False) else None)
        if getattr(result, "halt_required", False) and on_halt is not None:
            on_halt(incident_id, "protection")
        return result

    def _validate_settlement_binding(self, db, now):
        if self.settlement_store is None:
            return None
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
        rows = db.execute("SELECT * FROM owner_state").fetchall()
        if len(rows) != 1:
            raise AccountOwnerError("invalid account owner state")
        schema, account, epoch, boot, generation, permission, authority, sequence = rows[0]
        if (schema != 1 or account != self.account or not epoch or not boot
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
            "WHERE a.state='UNKNOWN' OR o.status IN ('reserved','attempted','takeover_pending') "
            "ORDER BY a.rowid"))

    def status(self):
        """Pure validated read."""
        with self._transaction() as db:
            state = self._state(db)
            capacity = self._capacity(db)
            actor = db.execute("SELECT kind FROM runtime_actors WHERE boot_id=?",
                               (state["boot_id"],)).fetchone()
            return {**state, "exposures": tuple((row.leg_id, row.confirmed, row.reserved)
                                                for row in exposures(capacity)),
                    "unresolved_attempts": tuple(row[0] for row in self._unresolved_attempt_rows(db)),
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

    def record_local_refusal(self, action, reason, *, now):
        """Retain one final owner refusal as adapter feedback before delivery.

        Local policy/capacity decisions have no broker fact, but adapters still
        need a durable rejection to retire the intent.  Transient takeover and
        duplicate-operation responses are deliberately excluded by the runtime.
        """
        _time(now)
        _text(reason, "local refusal")
        if not isinstance(action, (OrderIntent, BracketAmend, Cancel)):
            raise AccountOwnerError("typed book action required")
        order_id = action.order_id
        boundary_time = getattr(action, "bar_time", None) or now
        _time(boundary_time, "local refusal boundary")
        identity = _body({"action": asdict(action), "reason": reason})
        fact_id = "local-refusal:" + hashlib.sha256(identity.encode("utf-8")).hexdigest()
        event = ExecutionEvent("reject", action.leg_id, boundary_time,
                               order_id=order_id, detail=reason)
        raw = _body(asdict(event))
        with self.serializer.acquire(), self._transaction() as db:
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
        """Test-only activation; no production/config/HTTP route exposes this method."""
        _time(now, "activation time")
        if self.synthetic_broker is None:
            raise AccountOwnerError("synthetic activation requires SyntheticBroker")
        cancels = []
        with self.serializer.acquire(), self._transaction() as db:
            state = self._state(db)
            settlement_refusal = self._validate_settlement_binding(db, now)
            if settlement_refusal is not None:
                raise AccountOwnerError(settlement_refusal)
            if now < self.binding["session"].opens_at or now >= self.binding["session"].risk_add_cutoff:
                raise AccountOwnerError("outside synthetic risk-add window")
            if self._capacity(db).blocks:
                raise AccountOwnerError("capacity state blocked")
            desired = (Mode.PROTECTED if is_protected(
                self.binding["settlement"].equity, self.binding["settlement"].peak,
                self.binding["policy"]) else Mode.NORMAL)
            retained = db.execute(
                "SELECT session_id, mode, operation_ids, generation FROM protection_state "
                "ORDER BY rowid DESC LIMIT 1").fetchone()
            session_id = self.binding["session"].session_id
            if retained is None:
                db.execute("INSERT INTO protection_state VALUES (?, ?, '[]', ?)",
                           (session_id, desired.value, state["generation"]))
            elif retained[0] == session_id:
                if retained[1] != desired.value:
                    self._halt_db(db, "intraday-mode-change:" + session_id,
                                  "protection", now)
                    raise AccountOwnerError("settlement-driven mode changed intraday")
                pending_ids = tuple(json.loads(retained[2]))
                if pending_ids:
                    capacity = self._capacity(db)
                    pending = tuple(identity for identity in pending_ids if next(
                        operation for operation in capacity.operations
                        if operation.request.operation_id == identity).terminal is None)
                    if pending:
                        if retained[3] != state["generation"]:
                            raise AccountOwnerError("protection cancellation recovery required")
                        db.execute("UPDATE owner_state SET permission='HALTED', authority='NORMAL'")
                        cancels = [Cancel("orb_mnq_v7", identity) for identity in pending]
            else:
                capacity = self._capacity(db)
                pending = ()
                if retained[1] == Mode.NORMAL.value and desired is Mode.PROTECTED:
                    pending = tuple(operation.request.operation_id for operation in capacity.operations
                                    if operation.request.leg_id == "orb_mnq_v7"
                                    and db.execute("SELECT kind FROM operations WHERE operation_id=?",
                                                   (operation.request.operation_id,)).fetchone()[0] == "add"
                                    and operation.status == "active" and operation.terminal is None)
                db.execute("INSERT INTO protection_state VALUES (?, ?, ?, ?)",
                           (session_id, desired.value, _body(pending), state["generation"]))
                if pending:
                    db.execute("UPDATE owner_state SET permission='HALTED', authority='NORMAL'")
                    cancels = [Cancel("orb_mnq_v7", identity) for identity in pending]
            if not cancels:
                db.execute("UPDATE owner_state SET permission='RUNNING', authority='NORMAL'")
                return replace_dict(state, permission="RUNNING", authority="NORMAL")
        for cancel in cancels:
            self.dispatch(cancel, now=now)
        with self.serializer.acquire(), self._transaction() as db:
            capacity = self._capacity(db)
            if any(next(operation for operation in capacity.operations
                        if operation.request.operation_id == cancel.order_id).terminal is None
                   for cancel in cancels):
                raise AccountOwnerError("protection cancellation remains unresolved")
            db.execute("UPDATE owner_state SET permission='RUNNING', authority='NORMAL'")
            return self._state(db)

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

    def _base_evidence(self, db, leg_id):
        row = db.execute("SELECT operation_id, requested FROM operations WHERE leg_id=? "
                         "AND kind='entry' ORDER BY rowid LIMIT 1", (leg_id,)).fetchone()
        if row is None:
            return None, 0, 0
        capacity = self._capacity(db)
        confirmed = sum(f.quantity for f in capacity.fills if f.operation_id == row[0])
        return row[0], row[1], confirmed

    def _open_fill_quantities(self, db, leg_id):
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

    def dispatch(self, action, *, now):
        _time(now)
        if not isinstance(action, (OrderIntent, BracketAmend, Cancel)):
            raise AccountOwnerError("typed book action required")
        action_body = _body(asdict(action))
        operation_id = (action.order_id if isinstance(action, OrderIntent) else
                        "control:" + hashlib.sha256(action_body.encode("utf-8")).hexdigest()[:24])
        with self.serializer.acquire(), self._thread:
            with self._transaction() as db:
                state = self._state(db)
                settlement_refusal = self._validate_settlement_binding(db, now)
                if settlement_refusal is not None:
                    return DispatchResult(operation_id, 0, refusal_reason=settlement_refusal)
                if state["authority"] == "INTERVENTION":
                    return DispatchResult(operation_id, 0, refusal_reason="intervention_fence")
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
                if ready_takeover:
                    db.execute("UPDATE operations SET status='reserved' WHERE operation_id=?",
                               (operation_id,))
                elif isinstance(action, OrderIntent) and action.kind in ("entry", "add"):
                    if state["permission"] != "RUNNING" or state["authority"] != "NORMAL":
                        return DispatchResult(operation_id, 0, refusal_reason="risk_add_not_authorized")
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
                    action.order_id if isinstance(action, Cancel) else None,
                )
                db.execute("INSERT INTO attempts VALUES (?, ?, 'UNKNOWN', ?, ?, NULL)",
                           (attempt_id, operation_id, state["generation"], _body(asdict(command))))
                db.execute("UPDATE operations SET status='attempted' WHERE operation_id=?",
                           (operation_id,))
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
            for fact in result.facts:
                events.extend(self._observe_locked(
                    fact, now=now,
                    boundary_time=getattr(action, "bar_time", None) or now))
            with self._transaction() as db:
                db.execute("UPDATE attempts SET state=?, observation=? WHERE attempt_id=?",
                           (result.state.upper(), _body({"state": result.state,
                                                        "facts": [f.fact_id for f in result.facts]}), attempt_id))
                if result.facts and isinstance(action, (Cancel, BracketAmend)):
                    db.execute("UPDATE operations SET status='observed' WHERE operation_id=?",
                               (operation_id,))
            return DispatchResult(operation_id, quantity, attempt_id, result.state,
                                  confirmed_events=tuple(events))

    def advance_schedule(self, *, now):
        """Apply cutoff, scheduled flatten and deadline using the bound session clock."""
        _time(now)
        session = self.binding["session"]
        try:
            phase = classify_schedule(session, now)
        except ScheduleError:
            self.halt("schedule-missing:" + session.session_id, "schedule", now=now)
            return ()
        actions = []
        with self.serializer.acquire(), self._thread, self._transaction() as db:
            state = self._state(db)
            if state["authority"] == "INTERVENTION":
                return ()
            capacity = self._capacity(db)
            if phase in (SchedulePhase.CUTOFF, SchedulePhase.FLATTEN,
                         SchedulePhase.DEADLINE) and state["authority"] == "NORMAL":
                db.execute("UPDATE owner_state SET permission='HALTED', authority='SCHEDULED_EXIT', "
                           "generation=generation+1")
                for operation in capacity.operations:
                    if (operation.status == "active" and operation.terminal is None
                            and operation.request.leg_id in {row.leg_id for row in BOOK_LEGS}):
                        actions.append(Cancel(operation.request.leg_id,
                                              operation.request.operation_id))
            if phase in (SchedulePhase.FLATTEN, SchedulePhase.DEADLINE):
                for exposure in exposures(capacity):
                    if exposure.confirmed:
                        operation_id = "scheduled-flat:" + session.session_id + ":" + exposure.leg_id
                        actions.append(OrderIntent(
                            operation_id, exposure.leg_id, "flat",
                            opposite(leg(exposure.leg_id).entry_side), exposure.confirmed,
                            bar_time=now, reason="scheduled_flatten",
                        ))
        results = tuple(self.dispatch(action, now=now) for action in actions)
        if phase is SchedulePhase.DEADLINE:
            with self.serializer.acquire(), self._thread, self._transaction() as db:
                if self._state(db)["authority"] == "SCHEDULED_EXIT":
                    capacity = self._capacity(db)
                    unresolved = bool(self._unresolved_attempt_rows(db))
                    occupied = any(row.confirmed or row.reserved for row in exposures(capacity))
                    if unresolved or occupied:
                        self._halt_db(db, "own-flat-deadline:" + session.session_id,
                                      "schedule", now)
        return results

    def advance_takeover(self, *, now):
        """Drive only a retained Aegis priority takeover; incidents revoke it."""
        _time(now)
        actions = []
        with self.serializer.acquire(), self._thread, self._transaction() as db:
            state = self._state(db)
            capacity = self._capacity(db)
            if state["authority"] != "NORMAL" or capacity.takeover is None:
                return (), False
            displaced = capacity.takeover.displaced
            for operation in capacity.operations:
                if (operation.request.leg_id in displaced and operation.status == "active"
                        and operation.terminal is None):
                    actions.append(Cancel(operation.request.leg_id,
                                          operation.request.operation_id))
            for exposure in exposures(capacity):
                if exposure.leg_id in displaced and exposure.confirmed:
                    actions.append(OrderIntent(
                        "takeover-flat:" + capacity.takeover.operation_id + ":" + exposure.leg_id,
                        exposure.leg_id, "flat", opposite(leg(exposure.leg_id).entry_side),
                        exposure.confirmed, bar_time=now, reason="aegis_takeover",
                    ))
        results = tuple(self.dispatch(action, now=now) for action in actions)
        with self.serializer.acquire(), self._thread, self._transaction() as db:
            state = self._state(db)
            capacity = self._capacity(db)
            if state["authority"] != "NORMAL" or capacity.takeover is None:
                return results, False
            displaced = capacity.takeover.displaced
            clear = all(row.confirmed == 0 and row.reserved == 0
                        for row in exposures(capacity) if row.leg_id in displaced)
            terminal = all(operation.terminal is not None for operation in capacity.operations
                           if operation.status == "active"
                           and operation.request.leg_id in displaced)
            if not clear or not terminal:
                return results, False
            next_sequence = capacity.sequence + 1
            proof = Quiescence(next_sequence, displaced, 0, 0, 0, 0)
            complete = CompleteTakeover(capacity.takeover.operation_id, proof)
            capacity = self._append_capacity(
                db, "takeover", complete, now,
                event_id="takeover-complete:" + capacity.takeover.operation_id)
            if capacity.blocks:
                self._halt_db(db, "takeover-proof:" + complete.operation_id,
                              "execution", now)
                return results, False
            return results, True

    def _halt_db(self, db, incident_id, reason, now):
        state = self._state(db)
        inserted = db.execute("INSERT OR IGNORE INTO incidents VALUES (?, ?, ?, ?)",
                              (incident_id, reason, now.isoformat(), state["generation"])).rowcount
        db.execute("UPDATE owner_state SET permission='HALTED', authority='INTERVENTION', "
                   "generation=generation+?", (1 if inserted else 0,))

    def observe(self, fact, *, now):
        with self.serializer.acquire():
            return self._observe_locked(fact, now=now, boundary_time=fact.as_of)

    def _observe_locked(self, fact, *, now, boundary_time=None):
        if not isinstance(fact, BrokerFact):
            raise AccountOwnerError("typed broker fact required")
        _time(now)
        try:
            _time(fact.as_of, "fact time")
        except AccountOwnerError:
            with self._transaction() as db:
                self._halt_db(db, "fact-time:" + str(uuid4()), "execution", now)
            return ()
        with self._transaction() as db:
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
                if operation_kind in ("exit", "flat"):
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
                    if fact.cumulative_filled != consumed:
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
