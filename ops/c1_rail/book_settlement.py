"""Attended account-close owner: challenge, signed submission, durable acceptance.

Implements the operator-approved settlement contract
(``docs/spec/2026-09-15-tradeify-attended-settlement-contract.md``): an
operator-attested, evidence-backed account close becomes exactly one durable
``SettledClose`` for the sizing consumer, in account-session order, under a
one-use 300-second challenge signed by an enrolled operator key. Nothing here
acknowledges an incident, clears a halt, releases a reservation or authorizes
risk; activation and resumption remain separate owners.

Refusals are values (``Refusal``); durable-state faults raise
``SettlementError`` and the caller must treat the account as blocked.
"""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from contextlib import closing, contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from uuid import uuid4
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from book_policy import FIRM_RULES, TIER, ProtectionPolicy, is_protected, require_policy
from book_session_calendar import SessionCalendar
from book_sizing_context import SettledClose
from c1_signal_daemon.book_protocol import Mode
from ed25519_verify import is_strong_public_key, verify as ed25519_verify

CONTRACT = "docs/spec/2026-09-15-tradeify-attended-settlement-contract.md"
SEAL_CONTRACT = "docs/spec/2026-09-12-tradeify-account-snapshot-seal-contract.md"
SEAL_CHECKS = tuple(f"C{i}" for i in range(1, 11))
_SEAL_VALUES = frozenset({"balance", "equity", "trailing_threshold", "prior_trade_days", "prior_max_day_profit",
                          "consistency_display_pct", "profit_target_display", "cash_adjustments_total",
                          "token_trade_fill_dates", "positions_export_shows_flat", "working_orders_count"})
PACKAGE_SCHEMA = "account_close_package/v1"
CHALLENGE_SCHEMA = "settlement_challenge/v1"
SCOPES = ("submit_account_close", "record_only")
CHALLENGE_LIFETIME = timedelta(seconds=300)
EVIDENCE_FRESHNESS = timedelta(minutes=30)
MAX_HISTORY_WINDOW_DAYS = 14
REQUIRED_SOURCE_ROLES = frozenset({"dashboard", "positions", "orders", "balance_history", "cash_history", "inception"})
CLOSE_SENSITIVE_ROLES = frozenset({"dashboard", "positions", "orders", "balance_history", "cash_history"})
FLATNESS_BASES = frozenset({"DAILY_FLATTEN_CONFIRMED_NO_LATER_FILLS", "VENUE_EQUITY_AT_CLOSE"})
TRADING_COST_KEYS = ("commission", "exchange", "clearing", "nfa")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_SESSION_ID = re.compile(r"^tradeify-account-day:\d{4}-\d{2}-\d{2}$")
_WIDTH = Decimal(str(FIRM_RULES[TIER]["starting_balance"])) * Decimal(str(FIRM_RULES[TIER]["max_dd_pct"])) / 100


class SettlementError(RuntimeError):
    """Durable settlement state missing, corrupt, tampered or fenced; refuse everything."""


@dataclass(frozen=True)
class Refusal:
    reason: str
    halt_required: bool = False


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
    return value if value.is_finite() else None


def _aware(now: datetime) -> bool:
    return isinstance(now, datetime) and now.tzinfo is not None and now.utcoffset() is not None


# --------------------------------------------------------------------------- package verification


def verify_package(package: dict, sources: dict[str, bytes], *, head: dict, previous_package: dict | None,
                   account: str, calendar_digest: str, policy_digest: str, calendar: SessionCalendar,
                   scope: str, now: datetime) -> str | None:
    """Return the first refusal reason, or None when every contract check passes."""
    if not isinstance(package, dict) or package.get("schema") != PACKAGE_SCHEMA or package.get("contract") != CONTRACT:
        return "package_schema"
    required = {"schema", "contract", "account_id", "venue", "session_id", "predecessor_session_id",
                "predecessor_package_sha256", "calendar_digest", "policy_digest", "effective_close_utc",
                "source_publication_utc", "operator_signed_utc", "report_timezone", "inception_utc",
                "equity", "ledger", "dashboard", "positions", "sources", "attestations",
                "unresolved_runtime_requests", "scope", "settlement_basis"}
    if set(package) != required:
        return "package_keys"
    if package["account_id"] != account or package["venue"] != TIER:
        return "wrong_account"
    if package["scope"] != scope:
        return "scope_mismatch"
    if package["settlement_basis"] not in ("VENUE_ROW", "NO_ACTIVITY_DASHBOARD_CORROBORATED"):
        return "settlement_basis"
    if scope == "record_only" and package["settlement_basis"] != "VENUE_ROW":
        return "historical_close_needs_venue_row"
    if package["calendar_digest"] != calendar_digest or package["policy_digest"] != policy_digest:
        return "digest_mismatch"
    session_id = package["session_id"]
    if not isinstance(session_id, str) or not _SESSION_ID.match(session_id):
        return "session_id"
    if package["predecessor_session_id"] != head["session_id"] or \
            package["predecessor_package_sha256"] != head["package_sha256"]:
        return "predecessor_mismatch"
    row = calendar.schedule_for(session_id)
    if row is None:
        return "session_not_in_calendar"
    if row.prior_session_id != head["session_id"]:
        return "out_of_order_settlement"
    effective = _utc(package["effective_close_utc"])
    if effective is None or effective != row.closes_at:
        return "effective_close_not_session_close"
    head_as_of = _utc(head["as_of_utc"])
    if head_as_of is None or effective <= head_as_of:
        return "effective_close_not_after_predecessor"
    if effective > now:
        return "effective_close_in_future"
    if package["source_publication_utc"] is not None:
        published = _utc(package["source_publication_utc"])
        if published is None or published > now:
            return "source_publication_utc"
    signed = _utc(package["operator_signed_utc"])
    if signed is None or signed > now:
        return "operator_signed_in_future"
    try:
        ZoneInfo(package["report_timezone"])
    except (ZoneInfoNotFoundError, TypeError, ValueError):
        return "report_timezone"
    inception = _utc(package["inception_utc"])
    if inception is None or inception >= effective:
        return "inception_utc"

    src_rows = package["sources"]
    if not isinstance(src_rows, list) or not src_rows:
        return "sources_missing"
    roles: dict[str, dict] = {}
    seen_files: set[str] = set()
    seen_digests: set[str] = set()
    for src in src_rows:
        if not isinstance(src, dict) or set(src) != {"role", "file", "sha256", "captured_utc"}:
            return "source_row"
        if src["role"] in roles:
            return "duplicate_source_role"
        # Filenames are unique across every source; digests are unique across the required roles
        # (independent artifacts). Several empty cash windows may legitimately share bytes.
        if src["file"] in seen_files or (src["role"] in REQUIRED_SOURCE_ROLES and src["sha256"] in seen_digests):
            return "source_not_distinct"
        seen_files.add(src["file"])
        if src["role"] in REQUIRED_SOURCE_ROLES:
            seen_digests.add(src["sha256"])
        data = sources.get(src["file"])
        if data is None or not _HEX64.match(str(src["sha256"])) or sha256_hex(data) != src["sha256"]:
            return "source_bytes_mismatch"
        captured = _utc(src["captured_utc"])
        if captured is None:
            return "source_captured_utc"
        if captured > now:
            return "future_capture"
        if src["role"] != "inception" and now - captured > EVIDENCE_FRESHNESS:
            return "stale_evidence"
        if (src["role"] in CLOSE_SENSITIVE_ROLES or src["role"].startswith("cash_history")) and captured < effective:
            return "capture_before_effective_close"
        roles[src["role"]] = src
    if not REQUIRED_SOURCE_ROLES <= set(roles):
        return "source_role_missing"

    equity = package["equity"]
    if not isinstance(equity, dict) or set(equity) != {"net_equity", "basis", "at_effective_close",
                                                       "flatness_basis", "equity_at_effective_close",
                                                       "valuation_basis"}:
        return "equity_keys"
    net_equity = _decimal(equity["net_equity"])
    if net_equity is None or net_equity < 0 or equity["basis"] != "NET_OF_TRADING_COSTS":
        return "net_equity"
    if equity["flatness_basis"] not in FLATNESS_BASES:
        return "flatness_basis"
    if equity["flatness_basis"] == "VENUE_EQUITY_AT_CLOSE":
        venue_equity = _decimal(equity["equity_at_effective_close"])
        if venue_equity is None or venue_equity != net_equity or not str(equity["valuation_basis"] or "").strip():
            return "venue_equity_at_close"
    else:
        if equity["at_effective_close"] != "FLAT" or package["unresolved_runtime_requests"] != []:
            return "flatness_uncertain"
        pos_view = package["positions"]
        if not isinstance(pos_view, dict) or pos_view.get("open_positions") != 0 or pos_view.get("working_orders") != 0:
            return "flatness_uncertain"

    ledger = package["ledger"]
    if not isinstance(ledger, dict) or set(ledger) != {"predecessor_net_equity", "gross_trade_pnl", "trading_costs",
                                                       "adjustments_abs_total", "unknown_rows", "unlinked_fee_rows",
                                                       "transactions", "revisions", "coverage"}:
        return "ledger_keys"
    predecessor_equity = _decimal(ledger["predecessor_net_equity"])
    if predecessor_equity is None or predecessor_equity != Decimal(head["equity"]):
        return "predecessor_equity_mismatch"
    gross = _decimal(ledger["gross_trade_pnl"])
    costs = ledger["trading_costs"]
    if gross is None or not isinstance(costs, dict) or set(costs) != set(TRADING_COST_KEYS):
        return "ledger_values"
    cost_values = [_decimal(costs[k]) for k in TRADING_COST_KEYS]
    if any(v is None or v < 0 for v in cost_values):
        return "trading_costs"
    adjustments = _decimal(ledger["adjustments_abs_total"])
    if adjustments is None or adjustments != 0:
        return "cash_adjustments_present"
    if ledger["unknown_rows"] != 0 or ledger["unlinked_fee_rows"] != 0:
        return "unclassified_ledger_rows"
    if predecessor_equity + gross - sum(cost_values) != net_equity:
        return "ledger_arithmetic"
    txs = ledger["transactions"]
    if not isinstance(txs, list) or any(not isinstance(t, dict) or set(t) != {"id", "sha256", "session_id"}
                                        or not isinstance(t["id"], str) or not re.fullmatch(r"[0-9A-Za-z_.:-]{1,64}", t["id"])
                                        or not isinstance(t["sha256"], str) or not _HEX64.match(t["sha256"])
                                        or not isinstance(t["session_id"], str) or not _SESSION_ID.match(t["session_id"])
                                        for t in txs):
        return "transactions"
    ids = [t["id"] for t in txs]
    if len(ids) != len(set(ids)):
        return "duplicate_transaction_id"
    if ledger["revisions"] != []:
        return "transaction_revision_detected"
    if previous_package is not None:
        before = {t["id"]: t["sha256"] for t in previous_package["ledger"]["transactions"]}
        after = {t["id"]: t["sha256"] for t in txs}
        if any(after.get(k) != v for k, v in before.items()):
            return "history_changed"
        # Every transaction not retained from the predecessor must belong to the proposed session;
        # a late-added historical row is a correction, never a silent addition.
        if any(t["id"] not in before and t["session_id"] != session_id for t in txs):
            return "history_changed"
    cov = ledger["coverage"]
    if not isinstance(cov, dict) or set(cov) != {"window_limit_days", "windows"}:
        return "coverage_keys"
    limit = cov["window_limit_days"]
    if isinstance(limit, bool) or not isinstance(limit, int) or not 0 < limit <= MAX_HISTORY_WINDOW_DAYS:
        return "coverage_window_limit"
    windows = cov["windows"]
    if not isinstance(windows, list) or not windows:
        return "coverage_windows"
    cursor = None
    for win in windows:
        if not isinstance(win, dict) or set(win) != {"from_utc", "to_utc", "rows", "complete"}:
            return "coverage_window_row"
        start, end = _utc(win["from_utc"]), _utc(win["to_utc"])
        if start is None or end is None or end <= start or end - start > timedelta(days=limit):
            return "coverage_window_span"
        if win["complete"] is not True or isinstance(win["rows"], bool) or not isinstance(win["rows"], int) or win["rows"] < 0:
            return "coverage_window_incomplete"
        if cursor is None:
            if start > inception:
                return "coverage_gap_at_inception"
        elif start > cursor:
            return "coverage_gap"
        cursor = end
    if cursor < _utc(roles["cash_history"]["captured_utc"]):
        return "coverage_ends_before_capture"

    dash = package["dashboard"]
    if not isinstance(dash, dict) or set(dash) != {"balance", "trailing_threshold", "captured_utc"}:
        return "dashboard_keys"
    balance, threshold = _decimal(dash["balance"]), _decimal(dash["trailing_threshold"])
    if balance is None or threshold is None or _utc(dash["captured_utc"]) is None:
        return "dashboard_values"
    if dash["captured_utc"] != roles["dashboard"]["captured_utc"]:
        return "capture_time_unbound"
    peak = max(Decimal(head["peak"]), net_equity)
    if scope == "record_only":
        # Historical catch-up: the dashboard shows the CURRENT balance and peak. The venue balance
        # row (assembler basis VENUE_ROW) corroborates the historical close; the dashboard may only
        # show a peak at or above the historical one.
        if threshold + _WIDTH < peak:
            return "dashboard_disagreement"
    elif balance != net_equity or threshold + _WIDTH != peak:
        return "dashboard_disagreement"
    pos = package["positions"]
    if not isinstance(pos, dict) or set(pos) != {"open_positions", "working_orders", "captured_utc"}:
        return "positions_keys"
    for key in ("open_positions", "working_orders"):
        if isinstance(pos[key], bool) or not isinstance(pos[key], int) or pos[key] < 0:
            return "positions_values"
    if _utc(pos["captured_utc"]) is None or pos["captured_utc"] != roles["positions"]["captured_utc"]:
        return "capture_time_unbound"
    att = package["attestations"]
    expected_att = {"reflects_effective_close", "costs_included_once", "no_known_pending_correction",
                    "no_conflicting_observation"}
    if not isinstance(att, dict) or set(att) != expected_att or any(att[k] is not True for k in expected_att):
        return "attestation_incomplete"
    if not isinstance(package["unresolved_runtime_requests"], list):
        return "unresolved_requests"
    if scope == "record_only" and now - effective < timedelta(0):
        return "record_only_not_historical"
    return None


# --------------------------------------------------------------------------- durable store


class SettlementStore:
    """SQLite FULL-synchronous, account-bound, boot-fenced settled-close chain."""

    def __init__(self, path, account: str, boot_id: str):
        self.path = Path(path)
        self.account = account
        self.boot_id = boot_id

    @contextmanager
    def _tx(self, *, create: bool = False):
        try:
            uri = self.path.resolve().as_uri() + ("?mode=rwc" if create else "?mode=rw")
            with closing(sqlite3.connect(uri, uri=True, timeout=5, isolation_level=None)) as db:
                db.execute("PRAGMA synchronous=FULL")
                db.execute("BEGIN IMMEDIATE")
                yield db
                db.commit()
        except (sqlite3.Error, OSError, ValueError) as exc:
            raise SettlementError("settlement state unavailable") from exc

    # ---- schema and state -------------------------------------------------

    @staticmethod
    def _create(db, account, boot_id, calendar_digest, policy_digest, keys):
        db.execute("CREATE TABLE state (version INTEGER, account TEXT, boot_id TEXT, calendar_digest TEXT, "
                   "policy_digest TEXT, trusted_keys TEXT, restore_pending INTEGER, invalidated INTEGER)")
        db.execute("INSERT INTO state VALUES (1, ?, ?, ?, ?, ?, 0, 0)",
                   (account, boot_id, calendar_digest, policy_digest, json.dumps(keys, sort_keys=True)))
        db.execute("CREATE TABLE chain (seq INTEGER PRIMARY KEY, session_id TEXT UNIQUE, predecessor_session_id TEXT, "
                   "package_sha256 TEXT, equity TEXT, peak TEXT, as_of_utc TEXT, mode_next TEXT, origin TEXT, "
                   "scope TEXT, accepted_utc TEXT, status TEXT, row_hash TEXT)")
        db.execute("CREATE TABLE packages (package_sha256 TEXT PRIMARY KEY, session_id TEXT, kind TEXT, "
                   "package_json TEXT, source_digests TEXT, received_utc TEXT)")
        db.execute("CREATE TABLE sources (package_sha256 TEXT, file TEXT, sha256 TEXT, data BLOB, "
                   "PRIMARY KEY (package_sha256, file))")
        db.execute("CREATE TABLE challenges (challenge_id TEXT PRIMARY KEY, envelope_sha256 TEXT, envelope_json TEXT, "
                   "scope TEXT, issued_utc TEXT, expires_utc TEXT, status TEXT, consumed_utc TEXT)")
        db.execute("CREATE TABLE events (seq INTEGER PRIMARY KEY AUTOINCREMENT, kind TEXT, session_id TEXT, "
                   "detail TEXT, utc TEXT)")
        db.execute("CREATE TABLE receipts (receipt_id TEXT PRIMARY KEY, session_id TEXT, package_sha256 TEXT, "
                   "accepted_utc TEXT)")

    def _state(self, db, *, check_boot: bool = True) -> dict:
        rows = db.execute("SELECT version, account, boot_id, calendar_digest, policy_digest, trusted_keys, "
                          "restore_pending, invalidated FROM state").fetchall()
        if len(rows) != 1 or rows[0][0] != 1 or rows[0][1] != self.account or (check_boot and rows[0][2] != self.boot_id):
            raise SettlementError("invalid or fenced settlement owner")
        version, account, boot, cal, pol, keys, restore_pending, invalidated = rows[0]
        return {"account": account, "boot_id": boot, "calendar_digest": cal, "policy_digest": pol,
                "trusted_keys": json.loads(keys), "restore_pending": bool(restore_pending),
                "invalidated": bool(invalidated)}

    @staticmethod
    def _row_hash(prev_hash: str, fields: tuple) -> str:
        return sha256_hex((prev_hash + "|" + "|".join(str(f) for f in fields)).encode("utf-8"))

    def _chain(self, db) -> list[dict]:
        rows = db.execute("SELECT seq, session_id, predecessor_session_id, package_sha256, equity, peak, as_of_utc, "
                          "mode_next, origin, scope, accepted_utc, status, row_hash FROM chain ORDER BY seq").fetchall()
        out = []
        prev_hash, prev_session = "", None
        for expected, row in enumerate(rows, 1):
            (seq, session_id, predecessor, package_sha256, equity, peak, as_of, mode_next, origin, scope,
             accepted, status, row_hash) = row
            fields = (seq, session_id, predecessor, package_sha256, equity, peak, as_of, mode_next, origin, scope,
                      accepted, status)
            if seq != expected or row_hash != self._row_hash(prev_hash, fields):
                raise SettlementError("settlement chain integrity failure")
            if prev_session is not None and predecessor != prev_session:
                raise SettlementError("settlement chain predecessor break")
            stored = db.execute("SELECT package_json, kind, source_digests FROM packages WHERE package_sha256=?",
                                (package_sha256,)).fetchone()
            expected_kind = "B7_SEAL" if origin == "B7" else "ACCOUNT_CLOSE"
            if stored is None or stored[1] != expected_kind \
                    or sha256_hex(stored[0].encode("utf-8")) != package_sha256:
                raise SettlementError("settlement package integrity failure")
            if expected_kind == "ACCOUNT_CLOSE":
                declared = json.loads(stored[2])
                retained = {f: (s, d) for f, s, d in db.execute(
                    "SELECT file, sha256, data FROM sources WHERE package_sha256=?", (package_sha256,))}
                if set(retained) != set(declared) or any(
                        retained[f][0] != declared[f] or sha256_hex(bytes(retained[f][1])) != declared[f] for f in declared):
                    raise SettlementError("settlement source-bytes integrity failure")
            out.append({"seq": seq, "session_id": session_id, "predecessor_session_id": predecessor,
                        "package_sha256": package_sha256, "equity": equity, "peak": peak, "as_of_utc": as_of,
                        "mode_next": mode_next, "origin": origin, "scope": scope, "accepted_utc": accepted,
                        "status": status})
            prev_hash, prev_session = row_hash, session_id
        return out

    def _append_chain(self, db, **row) -> dict:
        chain = self._chain(db)
        seq = len(chain) + 1
        prev_hash = db.execute("SELECT row_hash FROM chain WHERE seq=?", (seq - 1,)).fetchone()
        prev_hash = prev_hash[0] if prev_hash else ""
        fields = (seq, row["session_id"], row["predecessor_session_id"], row["package_sha256"], row["equity"],
                  row["peak"], row["as_of_utc"], row["mode_next"], row["origin"], row["scope"], row["accepted_utc"],
                  "ACCEPTED")
        db.execute("INSERT INTO chain VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", fields + (self._row_hash(prev_hash, fields),))
        return {**row, "seq": seq, "status": "ACCEPTED"}

    def _event(self, db, kind: str, session_id: str | None, detail: dict, now: datetime) -> None:
        db.execute("INSERT INTO events (kind, session_id, detail, utc) VALUES (?,?,?,?)",
                   (kind, session_id, json.dumps(detail, sort_keys=True), _iso(now)))

    # ---- lifecycle ----------------------------------------------------------

    @classmethod
    def boot(cls, path, account: str, *, trusted_keys: dict[str, list[str]], calendar_digest: str,
             policy_digest: str, now: datetime) -> "SettlementStore":
        """One call per process boot. A restart begins restore-pending with open challenges voided."""
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
        store = cls(path, account, str(uuid4()))
        existed = store.path.exists()
        with store._tx(create=True) as db:
            tables = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if not tables and not existed:
                store._create(db, account, store.boot_id, calendar_digest, policy_digest, trusted_keys)
                store._event(db, "boot", None, {"boot_id": store.boot_id, "fresh": True}, now)
            else:
                old = store._state(db, check_boot=False)
                store._chain(db)
                voided = db.execute("UPDATE challenges SET status='VOIDED_RESTART' WHERE status='ISSUED'").rowcount
                db.execute("UPDATE state SET boot_id=?, restore_pending=1", (store.boot_id,))
                store._event(db, "boot", None, {"boot_id": store.boot_id, "fresh": False,
                                                "voided_challenges": voided}, now)
                if old["calendar_digest"] != calendar_digest or old["policy_digest"] != policy_digest:
                    # The monthly calendar extension and any policy replacement freeze are audited
                    # rotations: the accepted-close chain is preserved, open challenges are already
                    # voided, and every later challenge binds the new digests.
                    db.execute("UPDATE state SET calendar_digest=?, policy_digest=?", (calendar_digest, policy_digest))
                    store._event(db, "digests_rotated", None, {
                        "calendar": [old["calendar_digest"], calendar_digest],
                        "policy": [old["policy_digest"], policy_digest]}, now)
                if old["trusted_keys"] != trusted_keys:
                    # Rotation/revocation is an audited enrollment change; the chain is preserved and
                    # only currently enrolled keys can sign from this boot on.
                    db.execute("UPDATE state SET trusted_keys=?", (json.dumps(trusted_keys, sort_keys=True),))
                    store._event(db, "trusted_keys_rotated", None, {
                        "removed": sorted(set(old["trusted_keys"]) - set(trusted_keys)),
                        "added": sorted(set(trusted_keys) - set(old["trusted_keys"])),
                        "scope_changes": sorted(k for k in set(old["trusted_keys"]) & set(trusted_keys)
                                                if old["trusted_keys"][k] != trusted_keys[k])}, now)
            store._state(db)
        return store

    def reconcile_restore(self, now: datetime) -> dict:
        """Verify the durable chain after a restart; permission stays with the halt owner."""
        with self._tx() as db:
            state = self._state(db)
            chain = self._chain(db)
            db.execute("UPDATE state SET restore_pending=0")
            self._event(db, "restore_reconciled", chain[-1]["session_id"] if chain else None,
                        {"rows": len(chain)}, now)
            return {"rows": len(chain), "invalidated": state["invalidated"]}

    def bootstrap_b7(self, seal_bytes: bytes, *, expected_seal_sha256: str, expected_tool_sha256: str,
                     session_id: str, effective_close_utc: datetime, policy: ProtectionPolicy,
                     now: datetime) -> Receipt | Refusal:
        """Seat the chain head from the sealed B7 snapshot; distinct from any later close.

        The seal's exact bytes and the sealer's tool digest are supplied out of band by the
        B7 owner; the document must carry the seal contract, exactly the ten checks passed,
        three distinct evidence digests, and values whose C3/C4/C8 derivations re-check here.
        ``effective_close_utc`` is the account close the seal window follows (the seal
        contract's C5 boundary: a weekday 17:00 ET close, or Friday's before a weekend).
        """
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
        if seal["contract"] != SEAL_CONTRACT or not _HEX64.match(expected_tool_sha256 or "")                 or seal["tool_sha256"] != expected_tool_sha256:
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
        if not isinstance(values, dict) or set(values) != _SEAL_VALUES or not isinstance(derived, dict)                 or not {"original_basis", "historical_eod_peak", "valid_until"} <= set(derived):
            return Refusal("seal_values")
        balance, equity = _decimal(values["balance"]), _decimal(values["equity"])
        threshold, peak = _decimal(values["trailing_threshold"]), _decimal(derived["historical_eod_peak"])
        adjustments = _decimal(values["cash_adjustments_total"])
        if balance is None or equity is None or threshold is None or peak is None or adjustments is None:
            return Refusal("seal_values")
        if balance != equity or values["positions_export_shows_flat"] is not True or values["working_orders_count"] != 0:
            return Refusal("seal_c3")
        if peak != threshold + _WIDTH or peak < balance or peak <= 0:
            return Refusal("seal_c4")
        if adjustments != 0 or _decimal(derived["original_basis"]) != Decimal(str(FIRM_RULES[TIER]["starting_balance"])):
            return Refusal("seal_c8")
        valid_until = derived.get("valid_until")
        try:
            expiry = datetime.fromisoformat(valid_until)
        except (TypeError, ValueError):
            return Refusal("seal_valid_until")
        if expiry.tzinfo is None or now >= expiry:
            return Refusal("seal_expired")
        if not (expiry - timedelta(hours=49) <= effective_close_utc < expiry):
            return Refusal("effective_close_outside_seal_window")
        if not isinstance(session_id, str) or not _SESSION_ID.match(session_id):
            return Refusal("session_id")
        close_local = effective_close_utc.astimezone(ZoneInfo("America/New_York"))
        if close_local.weekday() >= 5 or (close_local.hour, close_local.minute, close_local.second) != (17, 0, 0) \
                or close_local.date().isoformat() != session_id.split(":")[1]:
            return Refusal("effective_close_not_session_close")
        mode = Mode.PROTECTED if is_protected(float(equity), float(peak), policy) else Mode.NORMAL
        with self._tx() as db:
            state = self._state(db)
            if state["restore_pending"]:
                return Refusal("restore_reconciliation_required")
            if self._chain(db):
                return Refusal("chain_already_seated")
            digest = sha256_hex(seal_bytes)
            db.execute("INSERT INTO packages VALUES (?,?,?,?,?,?)",
                       (digest, session_id, "B7_SEAL", seal_bytes.decode("utf-8"), "{}", _iso(now)))
            self._append_chain(db, session_id=session_id, predecessor_session_id="", package_sha256=digest,
                               equity=str(equity), peak=str(peak), as_of_utc=_iso(effective_close_utc),
                               mode_next=mode.value, origin="B7", scope="", accepted_utc=_iso(now))
            self._event(db, "b7_bootstrap", session_id, {"seal_sha256": digest, "mode_next": mode.value}, now)
            receipt = Receipt(str(uuid4()), session_id, digest, _iso(now), str(equity), str(peak), mode.value, "B7")
            db.execute("INSERT INTO receipts VALUES (?,?,?,?)", (receipt.receipt_id, session_id, digest, _iso(now)))
            return receipt

    # ---- challenge --------------------------------------------------------

    def issue_challenge(self, *, scope: str, target_session_id: str | None, proposed_session_id: str,
                        package_sha256: str, halt_generation: int, permission: str,
                        calendar: SessionCalendar, now: datetime) -> dict | Refusal:
        if scope not in SCOPES:
            return Refusal("unknown_scope")
        if not _aware(now):
            return Refusal("invalid_now")
        if not _HEX64.match(package_sha256 or ""):
            return Refusal("package_digest")
        if isinstance(halt_generation, bool) or not isinstance(halt_generation, int) or halt_generation < 1:
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
            if state["invalidated"]:
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
                       (envelope["challenge_id"], sha256_hex(canonical_bytes(envelope)), json.dumps(envelope, sort_keys=True),
                        scope, envelope["issued_utc"], envelope["expires_utc"], "ISSUED", None))
            self._event(db, "challenge_issued", proposed_session_id, {"challenge_id": envelope["challenge_id"],
                                                                     "scope": scope}, now)
            return envelope

    # ---- submission -------------------------------------------------------

    def submit(self, *, envelope: dict, signature: bytes, key_id: str, package: dict, sources: dict[str, bytes],
               halt_generation: int, policy: ProtectionPolicy, calendar: SessionCalendar, now: datetime,
               on_halt=None) -> Receipt | Refusal:
        """Exactly-once acceptance under the single-writer transaction; no state advance on refusal."""
        if not _aware(now):
            return Refusal("invalid_now")
        policy = require_policy(policy)
        if not isinstance(envelope, dict) or envelope.get("schema") != CHALLENGE_SCHEMA:
            return Refusal("envelope_schema")
        with self._tx() as db:
            state = self._state(db)
            if state["restore_pending"]:
                return Refusal("restore_reconciliation_required")
            if state["invalidated"]:
                return Refusal("chain_invalidated")
            scopes = state["trusted_keys"].get(key_id)
            if not scopes or envelope.get("scope") not in scopes:
                return Refusal("unknown_key_or_scope")
            message = canonical_bytes(envelope)
            if not ed25519_verify(bytes.fromhex(key_id), message, signature):
                return Refusal("bad_signature")
            row = db.execute("SELECT envelope_sha256, status, expires_utc FROM challenges WHERE challenge_id=?",
                             (envelope.get("challenge_id"),)).fetchone()
            if row is None:
                return Refusal("challenge_unknown")
            envelope_sha256, status, expires_utc = row
            if envelope_sha256 != sha256_hex(message):
                return Refusal("challenge_mismatch")
            if status != "ISSUED":
                return Refusal("challenge_consumed")
            if now >= _utc(expires_utc):
                db.execute("UPDATE challenges SET status='EXPIRED' WHERE challenge_id=?", (envelope["challenge_id"],))
                return Refusal("challenge_expired")
            if envelope["account"] != self.account or envelope["boot_id"] != self.boot_id \
                    or envelope["halt_generation"] != halt_generation \
                    or envelope["calendar_digest"] != state["calendar_digest"] \
                    or envelope["policy_digest"] != state["policy_digest"] \
                    or calendar.calendar_digest != state["calendar_digest"]:
                return Refusal("stale_boot_generation_or_digest")
            package_bytes = canonical_bytes(package) if isinstance(package, dict) else b""
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
                if on_halt is not None:
                    on_halt("settlement:duplicate:" + str(session_id), "protection")
                return Refusal("duplicate_settlement", halt_required=True)
            previous = db.execute("SELECT package_json, kind FROM packages WHERE package_sha256=?",
                                  (head["package_sha256"],)).fetchone()
            if previous is None or (head["origin"] == "ACCOUNT_CLOSE" and previous[1] != "ACCOUNT_CLOSE"):
                raise SettlementError("settlement package integrity failure")
            previous_package = json.loads(previous[0]) if previous[1] == "ACCOUNT_CLOSE" else None
            reason = verify_package(package, sources, head=head, previous_package=previous_package,
                                    account=self.account, calendar_digest=state["calendar_digest"],
                                    policy_digest=state["policy_digest"], calendar=calendar,
                                    scope=envelope["scope"], now=now)
            if reason is not None:
                self._event(db, "submission_refused", session_id, {"reason": reason,
                                                                   "challenge_id": envelope["challenge_id"]}, now)
                if reason == "out_of_order_settlement":
                    if on_halt is not None:
                        on_halt("settlement:out_of_order:" + str(session_id), "protection")
                    return Refusal(reason, halt_required=True)
                return Refusal(reason)
            net_equity = Decimal(str(package["equity"]["net_equity"]))
            peak = max(Decimal(head["peak"]), net_equity)
            mode = Mode.PROTECTED if is_protected(float(net_equity), float(peak), policy) else Mode.NORMAL
            digest = envelope["package_sha256"]
            declared_sources = {s["file"]: s["sha256"] for s in package["sources"]}
            db.execute("INSERT INTO packages VALUES (?,?,?,?,?,?)",
                       (digest, session_id, "ACCOUNT_CLOSE", package_bytes.decode("utf-8"),
                        json.dumps(declared_sources, sort_keys=True), _iso(now)))
            for file_name, file_sha in declared_sources.items():
                db.execute("INSERT INTO sources VALUES (?,?,?,?)", (digest, file_name, file_sha, sqlite3.Binary(sources[file_name])))
            db.execute("UPDATE challenges SET status='CONSUMED', consumed_utc=? WHERE challenge_id=?",
                       (_iso(now), envelope["challenge_id"]))
            self._append_chain(db, session_id=session_id, predecessor_session_id=head["session_id"],
                               package_sha256=digest, equity=str(net_equity), peak=str(peak),
                               as_of_utc=package["effective_close_utc"], mode_next=mode.value, origin="ACCOUNT_CLOSE",
                               scope=envelope["scope"], accepted_utc=_iso(now))
            receipt = Receipt(str(uuid4()), session_id, digest, _iso(now), str(net_equity), str(peak), mode.value,
                              "ACCOUNT_CLOSE")
            db.execute("INSERT INTO receipts VALUES (?,?,?,?)", (receipt.receipt_id, session_id, digest, _iso(now)))
            self._event(db, "close_accepted", session_id, {"receipt_id": receipt.receipt_id, "scope": envelope["scope"],
                                                          "mode_next": mode.value}, now)
            return receipt

    # ---- corrections and reads ---------------------------------------------

    def record_revision(self, *, session_id: str, revised_package: dict, now: datetime, on_halt=None) -> Refusal:
        """A changed accepted record invalidates it and every dependent row; never overwrites."""
        with self._tx() as db:
            self._state(db)
            chain = self._chain(db)
            index = next((i for i, r in enumerate(chain) if r["session_id"] == session_id), None)
            if index is None:
                return Refusal("session_not_accepted")
            revised_bytes = canonical_bytes(revised_package) if isinstance(revised_package, dict) else b""
            digest = sha256_hex(revised_bytes)
            if digest == chain[index]["package_sha256"]:
                return Refusal("revision_identical")
            db.execute("INSERT OR IGNORE INTO packages VALUES (?,?,?,?,?,?)",
                       (digest, session_id, "REVISION", revised_bytes.decode("utf-8"), "{}", _iso(now)))
            db.execute("UPDATE chain SET status='INVALIDATED' WHERE seq>=?", (chain[index]["seq"],))
            self._rehash(db)
            db.execute("UPDATE state SET invalidated=1")
            db.execute("UPDATE challenges SET status='VOIDED_REVISION' WHERE status='ISSUED'")
            self._event(db, "revision_recorded", session_id, {"revised_sha256": digest,
                                                             "invalidated_from_seq": chain[index]["seq"]}, now)
        if on_halt is not None:
            on_halt("settlement:revision:" + session_id, "protection")
        return Refusal("accepted_record_revised", halt_required=True)

    def _rehash(self, db) -> None:
        rows = db.execute("SELECT seq, session_id, predecessor_session_id, package_sha256, equity, peak, as_of_utc, "
                          "mode_next, origin, scope, accepted_utc, status FROM chain ORDER BY seq").fetchall()
        prev = ""
        for fields in rows:
            prev = self._row_hash(prev, fields)
            db.execute("UPDATE chain SET row_hash=? WHERE seq=?", (prev, fields[0]))

    def status(self) -> dict:
        """Read-only projection; never advances state or consumes a challenge."""
        with self._tx() as db:
            state = self._state(db)
            chain = self._chain(db)
            head = chain[-1] if chain else None
            return {"account": self.account, "boot_id": self.boot_id, "restore_pending": state["restore_pending"],
                    "invalidated": state["invalidated"], "rows": len(chain), "head": head,
                    "grants_activation": False, "grants_resume": False}

    def settled_close(self) -> tuple[SettledClose, Mode] | Refusal:
        """The consumer's SettledClose for the chain head, or why none is available."""
        with self._tx() as db:
            state = self._state(db)
            if state["restore_pending"]:
                return Refusal("restore_reconciliation_required")
            if state["invalidated"]:
                return Refusal("chain_invalidated")
            chain = self._chain(db)
            if not chain:
                return Refusal("chain_not_seated")
            head = chain[-1]
            close = SettledClose(head["session_id"], _utc(head["as_of_utc"]), float(Decimal(head["equity"])),
                                 float(Decimal(head["peak"])), head["package_sha256"])
            return close, Mode(head["mode_next"])


# --------------------------------------------------------------------------- enrolled operator keys


KEYS_SCHEMA = "operator_signing_keys/v1"
_KEY_ROW = frozenset({"key_id", "algorithm", "scopes", "account_binding", "enrolled_by", "enrolled_utc",
                      "instruction", "record", "revoked_utc"})


def load_operator_keys(path: Path, *, account_id: str | None = None) -> dict[str, list[str]]:
    """Read the tracked enrollment record into ``SettlementStore.boot`` trusted_keys; refuse whole on defect.

    A row's ``account_binding`` is either ``BOUND_AT_RUNTIME`` (usable for the account the
    runtime is booted for) or a literal account id, which must equal ``account_id``.
    """
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
        if not isinstance(row["scopes"], list) or not row["scopes"] or any(s not in SCOPES for s in row["scopes"])                 or len(set(row["scopes"])) != len(row["scopes"]):
            raise SettlementError(f"{label}: scopes")
        if _utc(row["enrolled_utc"]) is None or (row["revoked_utc"] is not None and _utc(row["revoked_utc"]) is None):
            raise SettlementError(f"{label}: timestamps")
        if row["revoked_utc"] is not None:
            # Append-only revocation: a later row naming an enrolled key with revoked_utc removes it
            # permanently; a revoked key id can never be enrolled again.
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
