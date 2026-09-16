"""Attended account-close owner: challenge, signed submission, durable acceptance.

Implements the operator-approved settlement contract
(``docs/spec/2026-09-15-tradeify-attended-settlement-contract.md``) as the invariant table in
``docs/notes/2026-09-15-packet1-step5-invariant-table.md``: every claim the contract makes is
one named check (V1-V13 for a submitted package, O1-O8 for the durable owner). Nothing here
acknowledges an incident, clears a halt, releases a reservation or authorizes risk; activation
and resumption remain separate owners.

Refusals are values (``Refusal``); durable-state faults raise ``SettlementError`` and the
caller must treat the account as blocked.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import sqlite3
from contextlib import closing, contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from uuid import uuid4
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .book_policy import FIRM_RULES, TIER, ProtectionPolicy, is_protected, require_policy
from .book_session_calendar import SessionCalendar
from .account_close_calculation import CONTRACT, PACKAGE_SCHEMA, Refusal, verify_package, calculate_close
from .account_close_evidence import AssemblyError, parse_cash_report
from .account_close_ledger import reconcile, transactions_for
from .book_sizing_context import SettledClose
from c1_signal_daemon.book_protocol import Mode
from .ed25519_verify import is_strong_public_key, verify as ed25519_verify
from .settlement_signing import CHALLENGE_SCHEMA

SEAL_CONTRACT = "docs/spec/2026-09-12-tradeify-account-snapshot-seal-contract.md"
KEYS_SCHEMA = "operator_signing_keys/v1"
SCOPES = ("submit_account_close", "record_only")
CHALLENGE_LIFETIME = timedelta(seconds=300)
SEAL_CHECKS = tuple(f"C{i}" for i in range(1, 11))
PHASES = ("EMPTY", "SEATED", "ACCEPTING", "INVALIDATED")
STORE_VERSION = "4"
ET = ZoneInfo("America/New_York")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_SESSION_ID = re.compile(r"^tradeify-account-day:\d{4}-\d{2}-\d{2}$")
_WIDTH = Decimal(str(FIRM_RULES[TIER]["starting_balance"])) * Decimal(str(FIRM_RULES[TIER]["max_dd_pct"])) / 100
_BASIS = Decimal(str(FIRM_RULES[TIER]["starting_balance"]))
_SEAL_VALUES = frozenset({"balance", "equity", "trailing_threshold", "prior_trade_days", "prior_max_day_profit",
                          "consistency_display_pct", "profit_target_display", "cash_adjustments_total",
                          "token_trade_fill_dates", "positions_export_shows_flat", "working_orders_count"})
_KEY_ROW = frozenset({"key_id", "algorithm", "scopes", "account_binding", "enrolled_by", "enrolled_utc",
                      "instruction", "record", "revoked_utc"})
_STATE_FIELDS = ("version", "account", "boot_id", "calendar_digest", "policy_digest", "trusted_keys",
                 "restore_pending", "invalidated", "phase", "invalidated_from_seq", "history_sha256")


class SettlementError(RuntimeError):
    """Durable settlement state missing, corrupt, tampered or fenced; refuse everything."""


@dataclass(frozen=True)
class Receipt:
    receipt_id: str
    session_id: str
    package_sha256: str
    accepted_utc: str
    equity: str
    peak: str
    mode_next: str
    origin: str
    grants_activation: bool = False


def canonical_bytes(payload: dict) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _utc(text: object) -> datetime | None:
    if not isinstance(text, str) or not text.endswith("Z"):
        return None
    try:
        return datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _decimal(text: object) -> Decimal | None:
    if isinstance(text, bool) or not isinstance(text, (str, int)):
        return None
    try:
        value = Decimal(str(text))
    except InvalidOperation:
        return None
    return value if value.is_finite() and math.isfinite(float(value)) else None


def _aware(now: object) -> bool:
    return isinstance(now, datetime) and now.tzinfo is not None and now.utcoffset() is not None


def _is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


# =============================================================================== enrolled keys (O8)


def load_operator_keys(path: Path, *, account_id: str | None = None) -> dict[str, list[str]]:
    """Read the tracked enrollment record; append-only revocation is permanent; refuse whole on defect."""
    try:
        payload = json.loads(Path(path).read_bytes())
    except (OSError, ValueError) as exc:
        raise SettlementError("operator key record unavailable") from exc
    if not isinstance(payload, dict) or set(payload) != {"schema", "note", "keys"} or payload["schema"] != KEYS_SCHEMA:
        raise SettlementError("operator key record schema")
    rows = payload["keys"]
    if not isinstance(rows, list):
        raise SettlementError("operator key rows")
    keys: dict[str, list[str]] = {}
    revoked: set[str] = set()
    for index, row in enumerate(rows):
        label = f"keys[{index}]"
        if not isinstance(row, dict) or set(row) != _KEY_ROW:
            raise SettlementError(f"{label}: key set mismatch")
        key_id = row["key_id"]
        if not isinstance(key_id, str) or not re.fullmatch(r"[0-9a-f]{64}", key_id) \
                or not is_strong_public_key(bytes.fromhex(key_id)):
            raise SettlementError(f"{label}: not a strong Ed25519 public key")
        if row["algorithm"] != "ed25519" or row["enrolled_by"] != "operator":
            raise SettlementError(f"{label}: only operator-enrolled ed25519 keys are trusted")
        binding = row["account_binding"]
        if not isinstance(binding, str) or not binding.strip():
            raise SettlementError(f"{label}: account_binding required")
        if binding != "BOUND_AT_RUNTIME" and binding != account_id:
            raise SettlementError(f"{label}: key is bound to a different account")
        if not isinstance(row["scopes"], list) or not row["scopes"] or any(s not in SCOPES for s in row["scopes"]) \
                or len(set(row["scopes"])) != len(row["scopes"]):
            raise SettlementError(f"{label}: scopes")
        for key in ("instruction", "record"):
            if not isinstance(row[key], str) or not row[key].strip():
                raise SettlementError(f"{label}.{key}: required")
        if _utc(row["enrolled_utc"]) is None or (row["revoked_utc"] is not None and _utc(row["revoked_utc"]) is None):
            raise SettlementError(f"{label}: timestamps")
        if row["revoked_utc"] is not None:
            if key_id not in keys:
                raise SettlementError(f"{label}: revocation of a key that is not enrolled")
            del keys[key_id]
            revoked.add(key_id)
            continue
        if key_id in revoked:
            raise SettlementError(f"{label}: re-enrolment of a revoked key")
        if key_id in keys:
            raise SettlementError(f"{label}: duplicate active enrolment")
        keys[key_id] = list(row["scopes"])
    if not keys:
        raise SettlementError("no active operator key enrolled")
    return keys


# =============================================================================== durable owner (O1-O7)


class SettlementStore:
    """SQLite FULL-synchronous, account-bound, boot-fenced settled-close chain with a phased state row."""

    def __init__(self, path, account: str, boot_id: str, *, transaction=None,
                 halt_in_transaction=None):
        self.path = Path(path)
        self.account = account
        self.boot_id = boot_id
        self._transaction = transaction
        self._halt_in_transaction = halt_in_transaction

    # ---- storage primitives ------------------------------------------------

    @contextmanager
    def _tx(self, *, create: bool = False, after_commit=None):
        if self._transaction is not None:
            with self._transaction(create=create) as db:
                yield db
            for callback, args in after_commit or ():
                callback(*args)
            return
        try:
            uri = self.path.resolve().as_uri() + ("?mode=rwc" if create else "?mode=rw")
            with closing(sqlite3.connect(uri, uri=True, timeout=5, isolation_level=None)) as db:
                db.execute("PRAGMA synchronous=FULL")
                db.execute("BEGIN IMMEDIATE")
                yield db
                db.commit()
        except (sqlite3.Error, OSError, ValueError) as exc:
            raise SettlementError("settlement state unavailable") from exc
        for callback, args in after_commit or ():
            callback(*args)

    @staticmethod
    def _create(db):
        db.execute("CREATE TABLE state (" + ", ".join(f"{f} TEXT" for f in _STATE_FIELDS) + ", state_hash TEXT)")
        db.execute("CREATE TABLE chain (seq INTEGER PRIMARY KEY, session_id TEXT UNIQUE, predecessor_session_id TEXT, "
                   "package_sha256 TEXT, equity TEXT, peak TEXT, as_of_utc TEXT, mode_next TEXT, origin TEXT, "
                   "scope TEXT, accepted_utc TEXT, status TEXT, row_hash TEXT)")
        db.execute("CREATE TABLE superseded_chain (seq INTEGER, session_id TEXT, predecessor_session_id TEXT, "
                   "package_sha256 TEXT, equity TEXT, peak TEXT, as_of_utc TEXT, mode_next TEXT, origin TEXT, "
                   "scope TEXT, accepted_utc TEXT, status TEXT, superseded_utc TEXT, review_sha256 TEXT)")
        db.execute("CREATE TABLE packages (package_sha256 TEXT PRIMARY KEY, session_id TEXT, kind TEXT, "
                   "package_json TEXT, source_digests TEXT, received_utc TEXT)")
        db.execute("CREATE TABLE sources (package_sha256 TEXT, file TEXT, sha256 TEXT, data BLOB, "
                   "PRIMARY KEY (package_sha256, file))")
        db.execute("CREATE TABLE b7_history (seal_sha256 TEXT PRIMARY KEY, report_timezone TEXT)")
        db.execute("CREATE TABLE challenges (challenge_id TEXT PRIMARY KEY, envelope_sha256 TEXT, envelope_json TEXT, "
                   "scope TEXT, issued_utc TEXT, expires_utc TEXT, status TEXT, consumed_utc TEXT)")
        db.execute("CREATE TABLE events (seq INTEGER PRIMARY KEY AUTOINCREMENT, kind TEXT, session_id TEXT, "
                   "detail TEXT, utc TEXT)")
        db.execute("CREATE TABLE receipts (receipt_id TEXT PRIMARY KEY, session_id TEXT, package_sha256 TEXT, "
                   "accepted_utc TEXT)")

    @staticmethod
    def _state_hash(values: dict) -> str:
        return sha256_hex(("state|" + "|".join(str(values[f]) for f in _STATE_FIELDS)).encode("utf-8"))

    def _state(self, db, *, check_boot: bool = True) -> dict:
        """O1: one integrity-hashed state row for this account (and this boot unless restarting)."""
        columns = {r[1] for r in db.execute("PRAGMA table_info(state)")}
        if columns != set(_STATE_FIELDS) | {"state_hash"}:
            raise SettlementError("unsupported settlement store version; reviewed migration required")
        rows = db.execute("SELECT " + ", ".join(_STATE_FIELDS) + ", state_hash FROM state").fetchall()
        if len(rows) != 1:
            raise SettlementError("invalid or fenced settlement owner")
        values = dict(zip(_STATE_FIELDS, rows[0][:-1]))
        if rows[0][-1] != self._state_hash(values):
            raise SettlementError("settlement state integrity failure")
        if values["version"] != STORE_VERSION:
            raise SettlementError("unsupported settlement store version; reviewed migration required")
        if values["account"] != self.account \
                or (check_boot and values["boot_id"] != self.boot_id) or values["phase"] not in PHASES:
            raise SettlementError("invalid or fenced settlement owner")
        from_seq = int(values["invalidated_from_seq"])
        if from_seq < 0 or (from_seq > 0) != (values["invalidated"] == "1") \
                or (from_seq > 0) != (values["phase"] == "INVALIDATED"):
            raise SettlementError("settlement invalidation integrity failure")
        return {"account": values["account"], "boot_id": values["boot_id"], "calendar_digest": values["calendar_digest"],
                "policy_digest": values["policy_digest"], "trusted_keys": json.loads(values["trusted_keys"]),
                "restore_pending": values["restore_pending"] == "1", "invalidated": values["invalidated"] == "1",
                "phase": values["phase"], "invalidated_from_seq": from_seq,
                "history_sha256": values["history_sha256"]}

    _ALLOWED = {  # O3: phase transitions
        ("EMPTY", "SEATED"), ("SEATED", "ACCEPTING"), ("ACCEPTING", "ACCEPTING"), ("SEATED", "INVALIDATED"),
        ("ACCEPTING", "INVALIDATED"), ("INVALIDATED", "SEATED"), ("INVALIDATED", "ACCEPTING"),
        ("EMPTY", "EMPTY"), ("SEATED", "SEATED"), ("INVALIDATED", "INVALIDATED"),
    }

    def _transition(self, db, *, phase: str | None = None, **changes) -> None:
        """Every state mutation: validate the phase move, rewrite the row, rehash it."""
        current = dict(zip(_STATE_FIELDS, db.execute("SELECT " + ", ".join(_STATE_FIELDS) + " FROM state").fetchone()))
        if phase is not None:
            if (current["phase"], phase) not in self._ALLOWED:
                raise SettlementError(f"illegal settlement phase transition {current['phase']}->{phase}")
            current["phase"] = phase
        for key, value in changes.items():
            if key not in _STATE_FIELDS:
                raise SettlementError(f"unknown state field {key}")
            current[key] = "1" if value is True else "0" if value is False else str(value)
        values = {f: current[f] for f in _STATE_FIELDS}
        db.execute("UPDATE state SET " + ", ".join(f"{f}=?" for f in _STATE_FIELDS) + ", state_hash=?",
                   tuple(values[f] for f in _STATE_FIELDS) + (self._state_hash(values),))

    @staticmethod
    def _row_hash(prev_hash: str, fields: tuple) -> str:
        return sha256_hex((prev_hash + "|" + "|".join(str(f) for f in fields)).encode("utf-8"))

    @staticmethod
    def _history_digest(db) -> str:
        # One anchor covers both histories, including length/order and review
        # metadata. A per-row hash chain alone misses deletion of its suffix.
        active = db.execute("SELECT * FROM chain ORDER BY seq").fetchall()
        archived = db.execute("SELECT * FROM superseded_chain ORDER BY rowid").fetchall()
        revisions = db.execute("SELECT * FROM packages WHERE kind='REVISION' ORDER BY package_sha256").fetchall()
        events = db.execute("SELECT * FROM events ORDER BY seq").fetchall()
        b7_history = db.execute("SELECT * FROM b7_history ORDER BY seal_sha256").fetchall()
        return sha256_hex(canonical_bytes({"chain": active, "superseded_chain": archived,
                                          "revisions": revisions, "events": events, "b7_history": b7_history}))

    @staticmethod
    def _verify_retained_evidence(db, package_sha256: str, origin: str) -> None:
        """The same evidence obligation applies to active and superseded closes."""
        stored = db.execute("SELECT package_json, kind, source_digests FROM packages WHERE package_sha256=?",
                            (package_sha256,)).fetchone()
        kind = "B7_SEAL" if origin == "B7" else origin
        if stored is None or stored[1] != kind or sha256_hex(stored[0].encode("utf-8")) != package_sha256:
            raise SettlementError("settlement package integrity failure")
        b7_binding = db.execute("SELECT report_timezone FROM b7_history WHERE seal_sha256=?", (package_sha256,)).fetchone()
        if kind in ("ACCOUNT_CLOSE", "REVISION") or (kind == "B7_SEAL" and b7_binding):
            # Derive the source manifest from the hash-bound package, not merely
            # the mutable index alongside it.
            payload = json.loads(stored[0])
            declared = ({payload["evidence"]["E3"]["path"]: payload["evidence"]["E3"]["sha256"]}
                        if kind == "B7_SEAL" else {s["file"]: s["sha256"] for s in payload["sources"]})
            if json.loads(stored[2]) != declared:
                raise SettlementError("settlement source manifest integrity failure")
            retained = {f: (s, d) for f, s, d in db.execute(
                "SELECT file, sha256, data FROM sources WHERE package_sha256=?", (package_sha256,))}
            if set(retained) != set(declared) or any(
                    retained[f][0] != declared[f] or sha256_hex(bytes(retained[f][1])) != declared[f] for f in declared):
                raise SettlementError("settlement source-bytes integrity failure")

    def _chain(self, db) -> list[dict]:
        """O2: strict hash-chained sequence with retained, re-verified package and source bytes."""
        state = self._state(db, check_boot=False)
        if self._history_digest(db) != state["history_sha256"]:
            raise SettlementError("settlement chain integrity failure")
        for (digest,) in db.execute("SELECT package_sha256 FROM packages WHERE kind='REVISION'"):
            self._verify_retained_evidence(db, digest, "REVISION")
        for digest, origin in db.execute("SELECT package_sha256, origin FROM superseded_chain"):
            self._verify_retained_evidence(db, digest, origin)
        rows = db.execute("SELECT seq, session_id, predecessor_session_id, package_sha256, equity, peak, as_of_utc, "
                          "mode_next, origin, scope, accepted_utc, status, row_hash FROM chain ORDER BY seq").fetchall()
        out, prev_hash, prev_session = [], "", None
        for expected, row in enumerate(rows, 1):
            (seq, session_id, predecessor, package_sha256, equity, peak, as_of, mode_next, origin, scope,
             accepted, status, row_hash) = row
            fields = (seq, session_id, predecessor, package_sha256, equity, peak, as_of, mode_next, origin, scope,
                      accepted, status)
            if seq != expected or row_hash != self._row_hash(prev_hash, fields) or status != "ACCEPTED":
                raise SettlementError("settlement chain integrity failure")
            if prev_session is not None and predecessor != prev_session:
                raise SettlementError("settlement chain predecessor break")
            self._verify_retained_evidence(db, package_sha256, origin)
            out.append({"seq": seq, "session_id": session_id, "predecessor_session_id": predecessor,
                        "package_sha256": package_sha256, "equity": equity, "peak": peak, "as_of_utc": as_of,
                        "mode_next": mode_next, "origin": origin, "scope": scope, "accepted_utc": accepted,
                        "status": status})
            prev_hash, prev_session = row_hash, session_id
        return out

    def _retain_package(self, db, *, digest, session_id, kind, payload, declared, sources, now):
        """Reuse identical immutable content; acceptance and revision links remain separate."""
        db.execute("INSERT OR IGNORE INTO packages VALUES (?,?,?,?,?,?)",
                   (digest, session_id, kind, payload.decode("utf-8"),
                    json.dumps(declared, sort_keys=True), _iso(now)))
        for file_name, file_sha in declared.items():
            db.execute("INSERT OR IGNORE INTO sources VALUES (?,?,?,?)",
                       (digest, file_name, file_sha, sqlite3.Binary(sources[file_name])))
        self._verify_retained_evidence(db, digest, kind)

    def _append_chain(self, db, **row) -> None:
        seq = len(self._chain(db)) + 1
        prev = db.execute("SELECT row_hash FROM chain WHERE seq=?", (seq - 1,)).fetchone()
        fields = (seq, row["session_id"], row["predecessor_session_id"], row["package_sha256"], row["equity"],
                  row["peak"], row["as_of_utc"], row["mode_next"], row["origin"], row["scope"], row["accepted_utc"],
                  "ACCEPTED")
        db.execute("INSERT INTO chain VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                   fields + (self._row_hash(prev[0] if prev else "", fields),))
        self._transition(db, history_sha256=self._history_digest(db))

    def _event(self, db, kind: str, session_id: str | None, detail: dict, now: datetime) -> None:
        db.execute("INSERT INTO events (kind, session_id, detail, utc) VALUES (?,?,?,?)",
                   (kind, session_id, json.dumps(detail, sort_keys=True), _iso(now)))
        self._transition(db, history_sha256=self._history_digest(db))

    # ---- lifecycle (O3, O4) --------------------------------------------------

    @classmethod
    def boot(cls, path, account: str, *, trusted_keys: dict[str, list[str]], calendar_digest: str,
             policy_digest: str, now: datetime, transaction=None, boot_id: str | None = None,
             halt_in_transaction=None) -> "SettlementStore":
        """One call per process boot. A restart begins restore-pending; rotations are audited, never silent."""
        if not isinstance(account, str) or not account.strip():
            raise SettlementError("account identity required")
        if not _HEX64.match(calendar_digest or "") or not _HEX64.match(policy_digest or ""):
            raise SettlementError("calendar and policy digests required")
        if not isinstance(trusted_keys, dict) or not trusted_keys:
            raise SettlementError("at least one enrolled operator key required")
        for key_id, scopes in trusted_keys.items():
            if not isinstance(key_id, str) or not re.fullmatch(r"[0-9a-f]{64}", key_id) \
                    or not is_strong_public_key(bytes.fromhex(key_id)) \
                    or not isinstance(scopes, list) or not scopes or any(s not in SCOPES for s in scopes):
                raise SettlementError("trusted key must be a strong Ed25519 public key hex with contract scopes")
        if not _aware(now):
            raise SettlementError("aware clock required")
        store = cls(path, account, boot_id or str(uuid4()), transaction=transaction,
                    halt_in_transaction=halt_in_transaction)
        existed = store.path.exists()
        keys_json = json.dumps(trusted_keys, sort_keys=True)
        with store._tx(create=True) as db:
            tables = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            unified = "owner_state" in tables
            attachment = None
            if unified:
                if "settlement_attachment" not in tables:
                    raise SettlementError("settlement attachment authority unavailable")
                attachment_rows = db.execute(
                    "SELECT singleton, body, digest FROM settlement_attachment").fetchall()
                if len(attachment_rows) != 1:
                    raise SettlementError("invalid settlement attachment authority")
                singleton, attachment_body, attachment_digest = attachment_rows[0]
                if (singleton != 1
                        or sha256_hex(attachment_body.encode("utf-8")) != attachment_digest):
                    raise SettlementError("settlement attachment integrity failure")
                try:
                    attachment = json.loads(attachment_body)
                except (TypeError, ValueError):
                    raise SettlementError("settlement attachment integrity failure") from None
                status = attachment.get("status") if isinstance(attachment, dict) else None
                expected = ({"account", "status"} if status == "NEVER_ATTACHED"
                            else {"account", "status", "attached_utc"})
                if (status not in ("NEVER_ATTACHED", "ATTACHED")
                        or set(attachment) != expected or attachment["account"] != account
                        or (status == "ATTACHED"
                            and not isinstance(attachment.get("attached_utc"), str))):
                    raise SettlementError("settlement attachment identity mismatch")
            if "state" not in tables:
                if ((existed and not tables) or (tables and not unified)
                        or (attachment is not None
                            and attachment["status"] != "NEVER_ATTACHED")):
                    raise SettlementError("settlement state unavailable")
                cls._create(db)
                values = {"version": STORE_VERSION, "account": account, "boot_id": store.boot_id, "calendar_digest": calendar_digest,
                          "policy_digest": policy_digest, "trusted_keys": keys_json, "restore_pending": "0",
                          "invalidated": "0", "phase": "EMPTY", "invalidated_from_seq": "0",
                          "history_sha256": cls._history_digest(db)}
                db.execute("INSERT INTO state VALUES (" + ",".join("?" * (len(_STATE_FIELDS) + 1)) + ")",
                           tuple(values[f] for f in _STATE_FIELDS) + (cls._state_hash(values),))
                store._event(db, "boot", None, {"boot_id": store.boot_id, "fresh": True}, now)
                if unified:
                    attachment_body = json.dumps(
                        {"account": account, "status": "ATTACHED",
                         "attached_utc": _iso(now)},
                        sort_keys=True, separators=(",", ":"))
                    db.execute(
                        "UPDATE settlement_attachment SET body=?, digest=? WHERE singleton=1",
                        (attachment_body, sha256_hex(attachment_body.encode("utf-8"))),
                    )
            else:
                if unified and attachment["status"] != "ATTACHED":
                    raise SettlementError("settlement attachment authority unavailable")
                old = store._state(db, check_boot=False)
                store._chain(db)
                voided = db.execute("UPDATE challenges SET status='VOIDED_RESTART' WHERE status='ISSUED'").rowcount
                store._transition(db, boot_id=store.boot_id, restore_pending=True)
                store._event(db, "boot", None, {"boot_id": store.boot_id, "fresh": False,
                                                "voided_challenges": voided}, now)
                if old["calendar_digest"] != calendar_digest or old["policy_digest"] != policy_digest:
                    store._transition(db, calendar_digest=calendar_digest, policy_digest=policy_digest)
                    store._event(db, "digests_rotated", None, {"calendar": [old["calendar_digest"], calendar_digest],
                                                               "policy": [old["policy_digest"], policy_digest]}, now)
                if old["trusted_keys"] != trusted_keys:
                    store._transition(db, trusted_keys=keys_json)
                    store._event(db, "trusted_keys_rotated", None, {
                        "removed": sorted(set(old["trusted_keys"]) - set(trusted_keys)),
                        "added": sorted(set(trusted_keys) - set(old["trusted_keys"])),
                        "scope_changes": sorted(k for k in set(old["trusted_keys"]) & set(trusted_keys)
                                                if old["trusted_keys"][k] != trusted_keys[k])}, now)
            store._state(db)
        return store

    def reconcile_restore(self, now: datetime) -> dict | Refusal:
        """Verify the durable chain after a restart; permission stays with the halt owner."""
        if not _aware(now):
            return Refusal("invalid_now")
        with self._tx() as db:
            state = self._state(db)
            chain = self._chain(db)
            self._transition(db, restore_pending=False)
            self._event(db, "restore_reconciled", chain[-1]["session_id"] if chain else None, {"rows": len(chain)}, now)
            return {"rows": len(chain), "invalidated": state["invalidated"]}

    # ---- B7 seat (O5) --------------------------------------------------------

    def _b7_previous(self, seal, cash_history_bytes, report_timezone, effective_close, equity):
        """Derive inventory from the seal's E3 report; never from the new close."""
        if not isinstance(cash_history_bytes, bytes) or not isinstance(report_timezone, str) \
                or sha256_hex(cash_history_bytes) != seal["evidence"]["E3"]["sha256"]:
            raise AssemblyError("B7 history binding")
        rows = parse_cash_report(cash_history_bytes, report_tz=ZoneInfo(report_timezone),
            captured_utc=datetime.fromisoformat(seal["evidence"]["E3"]["captured_at"]), account_id=self.account)
        ids = [r.transaction_id for r in rows]
        if len(ids) != len(set(ids)) or any(r.ts_utc > effective_close for r in rows):
            raise AssemblyError("B7 history inventory")
        rows.sort(key=lambda r: (r.ts_utc, int(r.transaction_id)))
        ledger = reconcile(rows)
        end_equity = rows[-1].amount_after
        if ledger.unknown_rows or ledger.unlinked_fee_rows or ledger.adjustments_abs_total != 0 \
                or any(cost < 0 for bucket in ledger.sessions.values() for cost in bucket["costs"].values()) \
                or end_equity != equity:
            raise AssemblyError("B7 history economics")
        return {"report_timezone": report_timezone, "ledger": {"transactions": transactions_for(rows)}}

    def bootstrap_b7(self, seal_bytes: bytes, *, expected_seal_sha256: str, expected_tool_sha256: str,
                     session_id: str, effective_close_utc: datetime, policy: ProtectionPolicy,
                     now: datetime, cash_history_bytes: bytes | None = None,
                     report_timezone: str | None = None,
                     calendar: SessionCalendar | None = None) -> Receipt | Refusal:
        """Seat the chain head from the authenticated B7 snapshot; distinct from any later close."""
        policy = require_policy(policy)
        if not _aware(now) or not _aware(effective_close_utc):
            return Refusal("invalid_now")
        if not _HEX64.match(expected_seal_sha256 or "") or sha256_hex(seal_bytes) != expected_seal_sha256:
            return Refusal("seal_identity")
        try:
            seal = json.loads(seal_bytes)
        except ValueError:
            return Refusal("seal_not_json")
        if not isinstance(seal, dict) or set(seal) != {"values", "derived", "evidence", "checks", "seal_timestamp",
                                                       "tool_sha256", "contract"}:
            return Refusal("seal_schema")
        if seal["contract"] != SEAL_CONTRACT or not _HEX64.match(expected_tool_sha256 or "") \
                or seal["tool_sha256"] != expected_tool_sha256:
            return Refusal("seal_contract_or_tool")
        checks = seal["checks"]
        if not isinstance(checks, dict) or tuple(checks) != SEAL_CHECKS or any(v != "pass" for v in checks.values()):
            return Refusal("seal_checks")
        evidence = seal["evidence"]
        if not isinstance(evidence, dict) or set(evidence) != {"E1", "E2", "E3"} or any(
                not isinstance(r, dict) or set(r) != {"path", "sha256", "captured_at"} or not _HEX64.match(str(r["sha256"]))
                for r in evidence.values()) or len({r["sha256"] for r in evidence.values()}) != 3:
            return Refusal("seal_evidence")
        values, derived = seal["values"], seal["derived"]
        if not isinstance(values, dict) or set(values) != _SEAL_VALUES or not isinstance(derived, dict) \
                or not {"original_basis", "historical_eod_peak", "valid_until"} <= set(derived):
            return Refusal("seal_values")
        balance, equity = _decimal(values["balance"]), _decimal(values["equity"])
        threshold, peak = _decimal(values["trailing_threshold"]), _decimal(derived["historical_eod_peak"])
        adjustments = _decimal(values["cash_adjustments_total"])
        if any(v is None for v in (balance, equity, threshold, peak, adjustments)):
            return Refusal("seal_values")
        if equity < 0 or peak <= 0:
            return Refusal("seal_values")
        if balance != equity or values["positions_export_shows_flat"] is not True or values["working_orders_count"] != 0:
            return Refusal("seal_c3")
        if peak != threshold + _WIDTH or peak < balance or peak <= 0:
            return Refusal("seal_c4")
        if adjustments != 0 or _decimal(derived["original_basis"]) != _BASIS:
            return Refusal("seal_c8")
        try:
            expiry = datetime.fromisoformat(derived["valid_until"])
        except (TypeError, ValueError):
            return Refusal("seal_valid_until")
        if expiry.tzinfo is None or now >= expiry:
            return Refusal("seal_expired")
        try:
            sealed = datetime.fromisoformat(seal["seal_timestamp"])
            captures = [datetime.fromisoformat(r["captured_at"]) for r in evidence.values()]
        except (TypeError, ValueError):
            return Refusal("seal_chronology")
        if not _aware(sealed) or any(not _aware(t) for t in captures) \
                or not effective_close_utc <= sealed <= now \
                or any(not effective_close_utc <= t <= sealed for t in captures):
            return Refusal("seal_chronology")
        if not isinstance(session_id, str) or not _SESSION_ID.match(session_id):
            return Refusal("session_id")
        close_local = effective_close_utc.astimezone(ET)
        if close_local.weekday() >= 5 or (close_local.hour, close_local.minute, close_local.second, close_local.microsecond) != (17, 0, 0, 0) \
                or close_local.date().isoformat() != session_id.split(":")[1]:
            return Refusal("effective_close_not_session_close")
        reopen_local = (close_local + timedelta(days=2 if close_local.weekday() == 4 else 0)).replace(hour=18)
        if expiry != reopen_local.astimezone(timezone.utc):
            return Refusal("seal_reopen_mismatch")
        if cash_history_bytes is not None or report_timezone is not None:
            try:
                self._b7_previous(seal, cash_history_bytes, report_timezone, effective_close_utc, equity)
            except (ValueError, TypeError, KeyError, ArithmeticError):
                return Refusal("b7_history_invalid")
        mode = Mode.PROTECTED if is_protected(float(equity), float(peak), policy) else Mode.NORMAL
        with self._tx() as db:
            state = self._state(db)
            if state["restore_pending"]:
                return Refusal("restore_reconciliation_required")
            if state["phase"] != "EMPTY" or self._chain(db):
                return Refusal("chain_already_seated")
            if not isinstance(calendar, SessionCalendar):
                return Refusal("calendar_required")
            if calendar.calendar_digest != state["calendar_digest"]:
                return Refusal("calendar_digest_mismatch")
            if not _aware(calendar.ratified_at) or calendar.ratified_at > now:
                return Refusal("calendar_not_ratified")
            session = calendar.schedule_for(session_id)
            if session is None:
                return Refusal("calendar_session_unavailable")
            if session.closes_at != effective_close_utc:
                return Refusal("effective_close_not_session_close")
            successors = tuple(row for row in calendar.rows if row.prior_session_id == session_id)
            if len(successors) != 1:
                return Refusal("calendar_successor_unavailable")
            if successors[0].opens_at != expiry:
                return Refusal("seal_reopen_mismatch")
            digest = sha256_hex(seal_bytes)
            declared = {}
            if cash_history_bytes is not None:
                source = seal["evidence"]["E3"]
                declared = {source["path"]: source["sha256"]}
                db.execute("INSERT INTO sources VALUES (?,?,?,?)",
                           (digest, source["path"], source["sha256"], sqlite3.Binary(cash_history_bytes)))
                db.execute("INSERT INTO b7_history VALUES (?,?)", (digest, report_timezone))
                self._transition(db, history_sha256=self._history_digest(db))
            db.execute("INSERT INTO packages VALUES (?,?,?,?,?,?)",
                       (digest, session_id, "B7_SEAL", seal_bytes.decode("utf-8"), json.dumps(declared), _iso(now)))
            self._append_chain(db, session_id=session_id, predecessor_session_id="", package_sha256=digest,
                               equity=str(equity), peak=str(peak), as_of_utc=_iso(effective_close_utc),
                               mode_next=mode.value, origin="B7", scope="", accepted_utc=_iso(now))
            self._transition(db, phase="SEATED")
            self._event(db, "b7_bootstrap", session_id, {"seal_sha256": digest, "mode_next": mode.value}, now)
            receipt = Receipt(str(uuid4()), session_id, digest, _iso(now), str(equity), str(peak), mode.value, "B7")
            db.execute("INSERT INTO receipts VALUES (?,?,?,?)", (receipt.receipt_id, session_id, digest, _iso(now)))
            return receipt

    # ---- challenge (O6) ------------------------------------------------------

    def issue_challenge(self, *, scope: str, target_session_id: str | None, proposed_session_id: str,
                        package_sha256: str, halt_generation: int, permission: str,
                        calendar: SessionCalendar, now: datetime) -> dict | Refusal:
        if scope not in SCOPES:
            return Refusal("unknown_scope")
        if not _aware(now):
            return Refusal("invalid_now")
        if not _HEX64.match(package_sha256 or ""):
            return Refusal("package_digest")
        if not _is_int(halt_generation) or halt_generation < 1:
            return Refusal("halt_generation")
        if not isinstance(proposed_session_id, str) or not _SESSION_ID.match(proposed_session_id):
            return Refusal("session_id")
        expires = now + CHALLENGE_LIFETIME
        if scope == "submit_account_close":
            target = calendar.schedule_for(target_session_id) if isinstance(target_session_id, str) else None
            if target is None or target.permission != "PERMITTED":
                return Refusal("target_session_unavailable")
            if target.prior_session_id != proposed_session_id:
                return Refusal("target_not_successor")
            expires = min(expires, target.risk_add_cutoff)
            if expires <= now:
                return Refusal("target_cutoff_passed")
        else:
            if target_session_id is not None:
                return Refusal("record_only_takes_no_target")
            if permission != "HALTED":
                return Refusal("record_only_requires_halted")
        with self._tx() as db:
            state = self._state(db)
            if state["restore_pending"]:
                return Refusal("restore_reconciliation_required")
            if state["invalidated"] or state["phase"] == "INVALIDATED":
                return Refusal("chain_invalidated")
            chain = self._chain(db)
            if not chain:
                return Refusal("chain_not_seated")
            head = chain[-1]
            if calendar.calendar_digest != state["calendar_digest"]:
                return Refusal("calendar_digest_mismatch")
            envelope = {
                "schema": CHALLENGE_SCHEMA, "challenge_id": str(uuid4()), "account": self.account,
                "boot_id": self.boot_id, "halt_generation": halt_generation, "scope": scope,
                "target_session_id": target_session_id, "proposed_session_id": proposed_session_id,
                "predecessor_session_id": head["session_id"], "predecessor_package_sha256": head["package_sha256"],
                "contract": CONTRACT, "calendar_digest": state["calendar_digest"],
                "policy_digest": state["policy_digest"], "package_sha256": package_sha256,
                "issued_utc": _iso(now), "expires_utc": _iso(expires),
            }
            db.execute("INSERT INTO challenges VALUES (?,?,?,?,?,?,?,?)",
                       (envelope["challenge_id"], sha256_hex(canonical_bytes(envelope)),
                        json.dumps(envelope, sort_keys=True), scope, envelope["issued_utc"], envelope["expires_utc"],
                        "ISSUED", None))
            self._event(db, "challenge_issued", proposed_session_id, {"challenge_id": envelope["challenge_id"],
                                                                     "scope": scope}, now)
            return envelope

    # ---- submission (O6, O7, O8, then V1-V13) --------------------------------

    def submit(self, *, envelope: dict, signature: bytes, key_id: str, package: dict, sources: dict[str, bytes],
               halt_generation: int, policy: ProtectionPolicy, calendar: SessionCalendar, now: datetime,
               on_halt=None) -> Receipt | Refusal:
        """Exactly-once acceptance; refusals cannot advance closes and corrections quarantine history."""
        if not _aware(now):
            return Refusal("invalid_now")
        if not isinstance(key_id, str) or not re.fullmatch(r"[0-9a-f]{64}", key_id):
            return Refusal("unknown_key_or_scope")
        policy = require_policy(policy)
        if not isinstance(envelope, dict) or envelope.get("schema") != CHALLENGE_SCHEMA:
            return Refusal("envelope_schema")
        try:
            message = canonical_bytes(envelope)
        except (TypeError, ValueError):
            return Refusal("envelope_serialization")
        try:
            package_bytes = canonical_bytes(package) if isinstance(package, dict) else b""
        except (TypeError, ValueError):
            return Refusal("package_serialization")
        notifications = []
        with self._tx(after_commit=notifications) as db:
            state = self._state(db)
            if state["restore_pending"]:
                return Refusal("restore_reconciliation_required")
            if state["invalidated"] or state["phase"] == "INVALIDATED":
                return Refusal("chain_invalidated")
            scopes = state["trusted_keys"].get(key_id)
            if not scopes or envelope.get("scope") not in scopes:
                return Refusal("unknown_key_or_scope")
            if not ed25519_verify(bytes.fromhex(key_id), message, signature):
                return Refusal("bad_signature")
            row = db.execute("SELECT envelope_sha256, status FROM challenges "
                             "WHERE challenge_id=?", (envelope.get("challenge_id"),)).fetchone()
            if row is None:
                return Refusal("challenge_unknown")
            envelope_sha256, status = row
            issued_envelope = {k: v for k, v in envelope.items() if k != "operator_signed_utc"}
            if envelope_sha256 != sha256_hex(canonical_bytes(issued_envelope)):
                return Refusal("challenge_mismatch")
            if status != "ISSUED":
                return Refusal("challenge_consumed")
            # Chronology belongs to the exact signed envelope. Indexed copies
            # are not an independent authority for extending or shifting it.
            signed = _utc(envelope.get("operator_signed_utc"))
            if signed is None:
                return Refusal("chronology:signing_timestamp_shape")
            if signed < _utc(envelope["issued_utc"]):
                return Refusal("chronology:signed_before_challenge")
            if signed > now:
                return Refusal("chronology:signed_after_receipt")
            if now >= _utc(envelope["expires_utc"]):
                db.execute("UPDATE challenges SET status='EXPIRED' WHERE challenge_id=?", (envelope["challenge_id"],))
                return Refusal("challenge_expired")
            if envelope["account"] != self.account or envelope["boot_id"] != self.boot_id \
                    or envelope["halt_generation"] != halt_generation \
                    or envelope["calendar_digest"] != state["calendar_digest"] \
                    or envelope["policy_digest"] != state["policy_digest"] \
                    or calendar.calendar_digest != state["calendar_digest"]:
                return Refusal("stale_boot_generation_or_digest")
            if sha256_hex(package_bytes) != envelope["package_sha256"]:
                return Refusal("evidence_changed")
            chain = self._chain(db)
            head = chain[-1]
            if envelope["predecessor_session_id"] != head["session_id"] \
                    or envelope["predecessor_package_sha256"] != head["package_sha256"]:
                return Refusal("predecessor_advanced")
            session_id = package.get("session_id")
            if session_id != envelope["proposed_session_id"]:
                return Refusal("session_not_proposed")
            if any(r["session_id"] == session_id for r in chain):
                self._event(db, "duplicate_settlement_refused", session_id, {"challenge_id": envelope["challenge_id"]}, now)
                if self._halt_in_transaction is not None:
                    self._halt_in_transaction(db, "settlement:duplicate:" + str(session_id),
                                              "protection", now)
                if on_halt is not None:
                    notifications.append((on_halt, ("settlement:duplicate:" + str(session_id), "protection")))
                return Refusal("duplicate_settlement", halt_required=True)
            previous = db.execute("SELECT package_json, kind FROM packages WHERE package_sha256=?",
                                  (head["package_sha256"],)).fetchone()
            if previous is None or (head["origin"] == "ACCOUNT_CLOSE" and previous[1] != "ACCOUNT_CLOSE"):
                raise SettlementError("settlement package integrity failure")
            previous_package = json.loads(previous[0]) if previous[1] == "ACCOUNT_CLOSE" else None
            if previous[1] == "B7_SEAL":
                baseline = db.execute("SELECT report_timezone FROM b7_history WHERE seal_sha256=?",
                                      (head["package_sha256"],)).fetchone()
                if baseline:
                    seal = json.loads(previous[0])
                    data = db.execute("SELECT data FROM sources WHERE package_sha256=? AND file=?",
                        (head["package_sha256"], seal["evidence"]["E3"]["path"])).fetchone()[0]
                    previous_package = self._b7_previous(seal, bytes(data), baseline[0],
                                                        _utc(head["as_of_utc"]), Decimal(head["equity"]))
            proposal = calculate_close(package, sources, policy=policy, head=head, previous_package=previous_package,
                                    account=self.account, calendar_digest=state["calendar_digest"],
                                    policy_digest=state["policy_digest"], calendar=calendar,
                                    scope=envelope["scope"], now=now, issued_utc=_utc(envelope["issued_utc"]))
            if isinstance(proposal, Refusal):
                reason = proposal.reason
                self._event(db, "submission_refused", session_id, {"reason": reason,
                                                                   "challenge_id": envelope["challenge_id"]}, now)
                if reason in {"history_changed", "transaction_revision_detected", "report_timezone_changed"}:
                    # The refusal does not certify an earliest affected close.
                    # Quarantine the complete chain rather than leave any known
                    # suspect prefix available after restore reconciliation.
                    observation = {"account_id": self.account, "session_id": chain[0]["session_id"],
                                   "sources": package["sources"], "reason": reason,
                                   "observed_package": package, "signed_envelope": envelope,
                                   "signature": signature.hex(), "key_id": key_id}
                    self._record_revision(db, session_id=chain[0]["session_id"], revised_package=observation,
                                          sources=sources, now=now, from_seq=1)
                if proposal.halt_required:
                    if self._halt_in_transaction is not None:
                        label = "out_of_order" if reason == "out_of_order_settlement" else reason
                        self._halt_in_transaction(
                            db, "settlement:" + label + ":" + str(session_id),
                            "protection", now)
                    if on_halt is not None:
                        label = "out_of_order" if reason == "out_of_order_settlement" else reason
                        notifications.append((on_halt, ("settlement:" + label + ":" + str(session_id), "protection")))
                return proposal
            net_equity, peak, mode = proposal.equity, proposal.peak, proposal.mode_next
            digest = envelope["package_sha256"]
            declared = {s["file"]: s["sha256"] for s in package["sources"]}
            self._retain_package(db, digest=digest, session_id=session_id, kind="ACCOUNT_CLOSE",
                                 payload=package_bytes, declared=declared, sources=sources, now=now)
            db.execute("UPDATE challenges SET status='CONSUMED', consumed_utc=? WHERE challenge_id=?",
                       (_iso(now), envelope["challenge_id"]))
            self._append_chain(db, session_id=session_id, predecessor_session_id=head["session_id"],
                               package_sha256=digest, equity=str(net_equity), peak=str(peak),
                               as_of_utc=package["effective_close_utc"], mode_next=mode.value, origin="ACCOUNT_CLOSE",
                               scope=envelope["scope"], accepted_utc=_iso(now))
            self._transition(db, phase="ACCEPTING")
            receipt = Receipt(str(uuid4()), session_id, digest, _iso(now), str(net_equity), str(peak), mode.value,
                              "ACCOUNT_CLOSE")
            db.execute("INSERT INTO receipts VALUES (?,?,?,?)", (receipt.receipt_id, session_id, digest, _iso(now)))
            self._event(db, "close_accepted", session_id, {"receipt_id": receipt.receipt_id, "scope": envelope["scope"],
                                                          "mode_next": mode.value, "signed_envelope": envelope,
                                                          "signature": signature.hex(), "key_id": key_id}, now)
            self._transition(db, history_sha256=self._history_digest(db))
            return receipt

    # ---- corrections (O3) ----------------------------------------------------

    def _record_revision(self, db, *, session_id, revised_package, sources, now, from_seq):
        """Retain and quarantine under the caller's existing writer transaction."""
        state = self._state(db)
        rows = revised_package["sources"]
        declared = {src["file"]: src["sha256"] for src in rows}
        revision_bytes = canonical_bytes({"schema": "settlement_revision/v1", "account_id": self.account,
            "session_id": session_id, "sources": rows, "revised_package": revised_package})
        digest = sha256_hex(revision_bytes)
        self._retain_package(db, digest=digest, session_id=session_id, kind="REVISION",
                             payload=revision_bytes, declared=declared, sources=sources, now=now)
        boundary = min(state["invalidated_from_seq"] or from_seq, from_seq)
        self._transition(db, phase="INVALIDATED", invalidated=True, invalidated_from_seq=boundary)
        db.execute("UPDATE challenges SET status='VOIDED_REVISION' WHERE status='ISSUED'")
        self._event(db, "revision_recorded", session_id, {"revised_sha256": digest,
                                                        "invalidated_from_seq": from_seq}, now)

    def record_revision(self, *, session_id: str, revised_package: dict, sources: dict[str, bytes],
                        now: datetime, on_halt=None) -> Refusal:
        """Retain evidence of a correction and invalidate dependents; this never accepts corrected equity."""
        if not _aware(now):
            return Refusal("invalid_now")
        if not isinstance(revised_package, dict) or revised_package.get("account_id") != self.account \
                or revised_package.get("session_id") != session_id:
            return Refusal("revision_identity")
        rows = revised_package.get("sources")
        if not isinstance(rows, list) or not rows or not isinstance(sources, dict):
            return Refusal("revision_sources_required")
        declared = {}
        for src in rows:
            if not isinstance(src, dict) or not isinstance(src.get("file"), str) or not src["file"].strip() \
                    or not isinstance(src.get("sha256"), str) or not _HEX64.fullmatch(src["sha256"]) \
                    or src.get("account_id") != self.account or src["file"] in declared:
                return Refusal("revision_source_manifest")
            data = sources.get(src["file"])
            if not isinstance(data, bytes) or sha256_hex(data) != src["sha256"]:
                return Refusal("revision_source_bytes_mismatch")
            declared[src["file"]] = src["sha256"]
        if set(sources) != set(declared):
            return Refusal("revision_source_manifest")
        try:
            revised_bytes = canonical_bytes(revised_package)
        except (TypeError, ValueError):
            return Refusal("revision_package_shape")
        with self._tx() as db:
            state = self._state(db)
            chain = self._chain(db)
            index = next((i for i, r in enumerate(chain) if r["session_id"] == session_id), None)
            if index is None:
                return Refusal("session_not_accepted")
            if sha256_hex(revised_bytes) == chain[index]["package_sha256"]:
                return Refusal("revision_identical")
            self._record_revision(db, session_id=session_id, revised_package=revised_package,
                                  sources=sources, now=now, from_seq=chain[index]["seq"])
            if self._halt_in_transaction is not None:
                self._halt_in_transaction(db, "settlement:revision:" + session_id,
                                          "protection", now)
        if on_halt is not None:
            on_halt("settlement:revision:" + session_id, "protection")
        return Refusal("accepted_record_revised", halt_required=True)

    def resolve_invalidation(self, *, review_sha256: str, reviewed_by: str, now: datetime) -> dict | Refusal:
        """Re-seat the chain before the revised row under a reviewed reconciliation.

        Rows from the revised session onward move to ``superseded_chain`` (their packages and
        sources stay retained); the store leaves INVALIDATED, enters restore-pending, and the
        affected sessions are resubmitted in order. Nothing here accepts a close or grants activation.
        """
        if not _aware(now) or not _HEX64.match(review_sha256 or "") or not isinstance(reviewed_by, str) \
                or not reviewed_by.strip():
            return Refusal("review_record_required")
        with self._tx() as db:
            state = self._state(db)
            if state["phase"] != "INVALIDATED":
                return Refusal("chain_not_invalidated")
            from_seq = state["invalidated_from_seq"]
            if from_seq <= 1:
                return Refusal("b7_head_revised_reseal_required")
            chain = self._chain(db)
            if from_seq > len(chain):
                raise SettlementError("settlement invalidation integrity failure")
            revised_session = chain[from_seq - 1]["session_id"]
            db.execute("INSERT INTO superseded_chain SELECT seq, session_id, predecessor_session_id, package_sha256, "
                       "equity, peak, as_of_utc, mode_next, origin, scope, accepted_utc, 'SUPERSEDED', ?, ? "
                       "FROM chain WHERE seq>=? ORDER BY seq", (_iso(now), review_sha256, from_seq))
            db.execute("DELETE FROM chain WHERE seq>=?", (from_seq,))
            # The retained prefix is unchanged, including its hashes. Publish the
            # new archive anchor and clear the pending boundary in this transaction.
            remaining = chain[:from_seq - 1]
            phase = "SEATED" if remaining[-1]["origin"] == "B7" else "ACCEPTING"
            db.execute("UPDATE challenges SET status='VOIDED_RECONCILIATION' WHERE status='ISSUED'")
            self._event(db, "invalidation_resolved", revised_session, {"review_sha256": review_sha256,
                                                                   "reviewed_by": reviewed_by,
                                                                   "superseded_from_seq": from_seq,
                                                                   "new_head": remaining[-1]["session_id"]}, now)
            self._transition(db, phase=phase, invalidated=False, invalidated_from_seq=0, restore_pending=True,
                             history_sha256=self._history_digest(db))
            self._chain(db)
            return {"head": remaining[-1]["session_id"], "superseded_from_seq": from_seq, "restore_pending": True}

    # ---- reads ---------------------------------------------------------------

    def status(self) -> dict:
        """Read-only projection; never advances state or consumes a challenge."""
        with self._tx() as db:
            state = self._state(db)
            chain = self._chain(db)
            return {"account": self.account, "boot_id": self.boot_id, "phase": state["phase"],
                    "restore_pending": state["restore_pending"], "invalidated": state["invalidated"],
                    "rows": len(chain), "head": chain[-1] if chain else None,
                    "grants_activation": False, "grants_resume": False}

    def settled_close(self) -> tuple[SettledClose, Mode] | Refusal:
        """The consumer's SettledClose for the chain head, or why none is available."""
        with self._tx() as db:
            return self.settled_close_from(db)

    def settled_close_from(self, db) -> tuple[SettledClose, Mode] | Refusal:
        """Connection-taking consumer surface for a unified account transaction."""
        state = self._state(db)
        chain = self._chain(db)
        if state["restore_pending"]:
            return Refusal("restore_reconciliation_required")
        if state["invalidated"] or state["phase"] == "INVALIDATED":
            return Refusal("chain_invalidated")
        if not chain:
            return Refusal("chain_not_seated")
        head = chain[-1]
        close = SettledClose(head["session_id"], _utc(head["as_of_utc"]), float(Decimal(head["equity"])),
                             float(Decimal(head["peak"])), head["package_sha256"])
        return close, Mode(head["mode_next"])
