"""Pure account-close validation and calculation; no signing or database writes."""
from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal, InvalidOperation
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .book_policy import FIRM_RULES, TIER, ProtectionPolicy, is_protected, require_policy
from .book_session_calendar import SessionCalendar
from c1_signal_daemon.book_protocol import Mode
from .account_close_evidence import (sha256_hex, verify_source_manifest, verify_history_coverage,
    AssemblyError, SourceFile, parse_cash_windows, parse_balance_history, COST_TYPES)
from .account_close_ledger import reconcile, equity_at_end_of, check_balance_history, transactions_for

CONTRACT = "docs/spec/2026-09-15-tradeify-attended-settlement-contract.md"

PACKAGE_SCHEMA = "account_close_package/v3"

EVIDENCE_FRESHNESS = timedelta(minutes=30)

CLOSE_SENSITIVE_ROLES = frozenset({"dashboard", "positions", "orders", "balance_history", "cash_history", "close_equity"})

FLATNESS_BASES = frozenset({"DAILY_FLATTEN_CONFIRMED_NO_LATER_FILLS", "VENUE_EQUITY_AT_CLOSE"})

SETTLEMENT_BASES = frozenset({"VENUE_ROW", "NO_ACTIVITY_DASHBOARD_CORROBORATED"})

TRADING_COST_KEYS = ("commission", "exchange", "clearing", "nfa")

_HEX64 = re.compile(r"^[0-9a-f]{64}$")

_SESSION_ID = re.compile(r"^tradeify-account-day:\d{4}-\d{2}-\d{2}$")

_TX_ID = re.compile(r"^[0-9A-Za-z_.:-]{1,64}$")

_WIDTH = Decimal(str(FIRM_RULES[TIER]["starting_balance"])) * Decimal(str(FIRM_RULES[TIER]["max_dd_pct"])) / 100

_PACKAGE_KEYS = frozenset({
    "schema", "contract", "account_id", "venue", "session_id", "predecessor_session_id",
    "predecessor_package_sha256", "calendar_digest", "policy_digest", "effective_close_utc",
    "source_publication_utc", "report_timezone", "inception_utc",
    "equity", "ledger", "dashboard", "positions", "sources", "attestations",
    "unresolved_runtime_requests", "scope", "settlement_basis"})

_EQUITY_KEYS = frozenset({"net_equity", "basis", "at_effective_close", "flatness_basis",
                          "equity_at_effective_close", "valuation_basis"})

_LEDGER_KEYS = frozenset({"predecessor_net_equity", "gross_trade_pnl", "trading_costs", "adjustments_abs_total",
                          "unknown_rows", "unlinked_fee_rows", "transactions", "revisions", "coverage"})

_ATTESTATIONS = frozenset({"reflects_effective_close", "costs_included_once", "no_known_pending_correction",
                           "no_conflicting_observation"})

@dataclass(frozen=True)
class Refusal:
    reason: str
    halt_required: bool = False

def canonical_bytes(payload: dict) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode("utf-8")

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

def _aware(now: object) -> bool:
    return isinstance(now, datetime) and now.tzinfo is not None and now.utcoffset() is not None

def _is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)

class _Ctx:
    """Everything one invariant may need; built once per submission."""

    def __init__(self, package, sources, head, previous_package, account, calendar_digest, policy_digest,
                 calendar, scope, now, issued_utc):
        self.p, self.sources, self.head, self.prev = package, sources, head, previous_package
        self.account, self.calendar_digest, self.policy_digest = account, calendar_digest, policy_digest
        self.calendar, self.scope, self.now, self.issued_utc = calendar, scope, now, issued_utc
        self.row = None
        self.effective = None
        self.inception = None
        self.roles: dict[str, dict] = {}
        self.net_equity: Decimal | None = None
        self.peak: Decimal | None = None


def _v1_shape(c: _Ctx):
    p = c.p
    if not isinstance(p, dict) or p.get("schema") != PACKAGE_SCHEMA or p.get("contract") != CONTRACT:
        return "package_schema"
    if set(p) != _PACKAGE_KEYS:
        return "package_keys"
    for key, allowed in (("equity", _EQUITY_KEYS), ("ledger", _LEDGER_KEYS), ("attestations", _ATTESTATIONS)):
        if not isinstance(p[key], dict) or set(p[key]) != allowed:
            return f"{key}_keys"
    if not isinstance(p["dashboard"], dict) or set(p["dashboard"]) != {"balance", "trailing_threshold", "captured_utc"}:
        return "dashboard_keys"
    if not isinstance(p["positions"], dict) or set(p["positions"]) != {"open_positions", "working_orders", "captured_utc"}:
        return "positions_keys"
    if not isinstance(p["unresolved_runtime_requests"], list):
        return "unresolved_requests"
    try:
        ZoneInfo(p["report_timezone"])
    except (ZoneInfoNotFoundError, TypeError, ValueError):
        return "report_timezone"
    return None


def _v2_account(c: _Ctx):
    if c.p["account_id"] != c.account or c.p["venue"] != TIER:
        return "wrong_account"
    return None


def _v3_scope(c: _Ctx):
    if c.scope not in ("submit_account_close", "record_only"):
        return "scope_unknown"
    if c.p["scope"] != c.scope:
        return "scope_mismatch"
    if c.p["settlement_basis"] not in SETTLEMENT_BASES:
        return "settlement_basis"
    if c.scope == "record_only" and c.p["settlement_basis"] != "VENUE_ROW":
        return "historical_close_needs_venue_row"
    return None


def _v4_digests(c: _Ctx):
    if c.p["calendar_digest"] != c.calendar_digest or c.p["policy_digest"] != c.policy_digest:
        return "digest_mismatch"
    return None


def _v5_session_chain(c: _Ctx):
    sid = c.p["session_id"]
    if not isinstance(sid, str) or not _SESSION_ID.match(sid):
        return "session_id"
    if c.p["predecessor_session_id"] != c.head["session_id"] or \
            c.p["predecessor_package_sha256"] != c.head["package_sha256"]:
        return "predecessor_mismatch"
    c.row = c.calendar.schedule_for(sid)
    if c.row is None:
        return "session_not_in_calendar"
    if c.row.prior_session_id != c.head["session_id"]:
        return "out_of_order_settlement"
    return None


def _v6_effective_close(c: _Ctx):
    c.effective = _utc(c.p["effective_close_utc"])
    if c.effective is None or c.effective != c.row.closes_at:
        return "effective_close_not_session_close"
    head_as_of = _utc(c.head["as_of_utc"])
    if head_as_of is None or c.effective <= head_as_of:
        return "effective_close_not_after_predecessor"
    return None


def _v8_sources(c: _Ctx):
    result = verify_source_manifest(c.p, c.sources)
    if isinstance(result, str):
        return result
    c.roles = result
    return None


def _v7_chronology(c: _Ctx):
    """One ordering over every timestamp the package and the challenge carry."""
    p, now = c.p, c.now
    c.inception = _utc(p["inception_utc"])
    if c.inception is None:
        return "chronology:timestamp_shape"
    if not c.inception < c.effective:
        return "chronology:inception_not_before_close"
    if c.effective > now:
        return "chronology:effective_close_in_future"
    published = None
    if p["source_publication_utc"] is not None:
        published = _utc(p["source_publication_utc"])
        if published is None or published > now:
            return "chronology:publication_after_receipt"
    captures = {}
    for role, src in c.roles.items():
        captured = _utc(src["captured_utc"])
        if captured is None:
            return "chronology:capture_shape"
        if captured > now:
            return "chronology:capture_in_future"
        if role != "inception":
            if now - captured > EVIDENCE_FRESHNESS:
                return "chronology:stale_evidence"
            if (role in CLOSE_SENSITIVE_ROLES or role.startswith("cash_history")) and captured < c.effective:
                return "chronology:capture_before_effective_close"
        if published is not None and role != "inception" and published > captured:
            return "chronology:publication_after_capture"
        captures[role] = captured
    if p["dashboard"]["captured_utc"] != c.roles["dashboard"]["captured_utc"] or \
            p["positions"]["captured_utc"] != c.roles["positions"]["captured_utc"]:
        return "chronology:capture_time_unbound"
    if c.issued_utc is not None and any(t > c.issued_utc for r, t in captures.items() if r != "inception"):
        return "chronology:capture_after_challenge"
    return verify_history_coverage(p["ledger"]["coverage"], c.roles,
                                   report_timezone=p["report_timezone"], inception=c.inception)


def _v9_ledger(c: _Ctx):
    ledger = c.p["ledger"]
    predecessor = _decimal(ledger["predecessor_net_equity"])
    if predecessor is None or predecessor != Decimal(c.head["equity"]):
        return "predecessor_equity_mismatch"
    gross = _decimal(ledger["gross_trade_pnl"])
    costs = ledger["trading_costs"]
    if gross is None or not isinstance(costs, dict) or set(costs) != set(TRADING_COST_KEYS):
        return "ledger_values"
    values = [_decimal(costs[k]) for k in TRADING_COST_KEYS]
    if any(v is None or v < 0 for v in values):
        return "trading_costs"
    adjustments = _decimal(ledger["adjustments_abs_total"])
    if adjustments is None or adjustments != 0:
        return "cash_adjustments_present"
    if ledger["unknown_rows"] != 0 or ledger["unlinked_fee_rows"] != 0:
        return "unclassified_ledger_rows"
    equity = c.p["equity"]
    c.net_equity = _decimal(equity["net_equity"])
    if c.net_equity is None or c.net_equity < 0 or equity["basis"] != "NET_OF_TRADING_COSTS":
        return "net_equity"
    if any(not math.isfinite(float(v)) for v in [predecessor, gross, c.net_equity, *values]):
        return "numeric_range"
    if predecessor + gross - sum(values) != c.net_equity:
        return "ledger_arithmetic"
    return None


def _v10_transactions(c: _Ctx):
    ledger = c.p["ledger"]
    txs = ledger["transactions"]
    if not isinstance(txs, list) or any(
            not isinstance(t, dict) or set(t) != {"id", "sha256", "session_id"}
            or not isinstance(t["id"], str) or not _TX_ID.match(t["id"])
            or not isinstance(t["sha256"], str) or not _HEX64.match(t["sha256"])
            or not isinstance(t["session_id"], str) or not _SESSION_ID.match(t["session_id"]) for t in txs):
        return "transactions"
    ids = [t["id"] for t in txs]
    if len(ids) != len(set(ids)):
        return "duplicate_transaction_id"
    if ledger["revisions"] != []:
        return "transaction_revision_detected"
    if c.prev is None:
        return "predecessor_inventory_required"
    if c.prev.get("report_timezone") != c.p["report_timezone"]:
        return "report_timezone_changed"
    # Current closes cannot include later-session activity. Earlier history is valid.
    if c.scope == "submit_account_close" and any(t["session_id"] > c.p["session_id"] for t in txs):
        return "history_changed"
    if c.prev is not None:
        before = {t["id"]: (t["sha256"], t["session_id"]) for t in c.prev["ledger"]["transactions"]}
        after = {t["id"]: (t["sha256"], t["session_id"]) for t in txs}
        if any(after.get(k) != v for k, v in before.items()):
            return "history_changed"
        if any(t["id"] not in before and t["session_id"] <= c.head["session_id"] for t in txs):
            return "history_changed"
    return None


def _v10_source_ledger(c: _Ctx):
    """Recompute all machine-readable claims from the hash-bound original reports."""
    p, claimed = c.p, c.p["ledger"]
    tz = ZoneInfo(p["report_timezone"])
    by_file = {s["file"]: s for s in c.roles.values()}
    windows = claimed["coverage"]["windows"]
    cash = []
    for win in windows:
        src = by_file[win["file"]]
        start, end = _utc(win["from_utc"]).astimezone(tz), _utc(win["to_utc"]).astimezone(tz)
        # Coverage uses exclusive endpoints; UI query labels are inclusive dates.
        last = end.date() - timedelta(days=1) if end.time() == time(0) else end.date()
        cash.append(SourceFile("cash_history", src["file"], c.sources[src["file"]],
            _utc(src["captured_utc"]), start.date(), last, win["complete"], c.account))
    try:
        rows, report = parse_cash_windows(cash, report_tz=tz)
        if report["revisions"]:
            return "transaction_revision_detected"
        actual = transactions_for(rows)
        before = {t["id"]: (t["sha256"], t["session_id"]) for t in c.prev["ledger"]["transactions"]}
        after = {t["id"]: (t["sha256"], t["session_id"]) for t in actual}
        if any(after.get(k) != v for k, v in before.items()) or any(
                t["id"] not in before and t["session_id"] <= c.head["session_id"] for t in actual):
            return "history_changed"
        # Establish historical integrity from parsed rows before checking current
        # package claims: stale counts or spans must not downgrade a known correction.
        for source, window in zip(cash, windows):
            source_rows, _ = parse_cash_windows([source], report_tz=tz)
            start, end = _utc(window["from_utc"]), _utc(window["to_utc"])
            inclusive_end = end == source.captured_utc
            if any(r.ts_utc < start or r.ts_utc > end or (r.ts_utc == end and not inclusive_end)
                   for r in source_rows):
                return "source_row_outside_coverage"
        if {w["file"]: w["rows"] for w in report["windows"]} != {w["file"]: w["rows"] for w in windows}:
            return "source_row_count_mismatch"
        if actual != claimed["transactions"]:
            return "source_transactions_mismatch"
        ledger = reconcile(rows)
        balances = parse_balance_history(c.sources[c.roles["balance_history"]["file"]], account_id=c.account)
        if check_balance_history(ledger, balances)["mismatches"]:
            return "source_balance_disagreement"
    except (AssemblyError, ValueError, TypeError, KeyError, AttributeError, ArithmeticError):
        return "source_ledger_invalid"
    if ledger.unknown_rows or ledger.unlinked_fee_rows or ledger.adjustments_abs_total:
        return "source_ledger_unclassified"
    if ledger.fund_row.ts_utc < c.inception:
        return "source_activity_before_inception"
    day = date.fromisoformat(p["session_id"].split(":")[1])
    prior_day = date.fromisoformat(c.head["session_id"].split(":")[1])
    bucket = ledger.sessions.get(day, {"gross": Decimal(0), "costs": {k: Decimal(0) for k in COST_TYPES.values()}, "rows": 0})
    if (_decimal(claimed["predecessor_net_equity"]) != equity_at_end_of(ledger, prior_day)
            or c.net_equity != equity_at_end_of(ledger, day)
            or _decimal(claimed["gross_trade_pnl"]) != bucket["gross"]
            or any(_decimal(claimed["trading_costs"][k]) != v for k, v in bucket["costs"].items())):
        return "source_ledger_disagreement"
    venue_row = next((total for d, total, _ in balances if d == day), None)
    if p["settlement_basis"] == "VENUE_ROW":
        if venue_row != c.net_equity:
            return "source_close_row_missing"
    else:
        prior_rows = [(d, total) for d, total, _ in balances if d <= day]
        if venue_row is not None or bucket["rows"] or not prior_rows or prior_rows[-1][1] != c.net_equity:
            return "source_no_activity_unproven"
    c.full_history_equity = rows[-1].amount_after
    return None


def _v11_close_equity(c: _Ctx):
    equity, pos = c.p["equity"], c.p["positions"]
    for key in ("open_positions", "working_orders"):
        if not _is_int(pos[key]) or pos[key] < 0:
            return "positions_values"
    if equity["flatness_basis"] not in FLATNESS_BASES:
        return "flatness_basis"
    if c.scope == "record_only" and equity["flatness_basis"] != "VENUE_EQUITY_AT_CLOSE":
        return "venue_equity_at_close"
    if equity["flatness_basis"] == "DAILY_FLATTEN_CONFIRMED_NO_LATER_FILLS":
        if equity["at_effective_close"] != "FLAT" or c.p["unresolved_runtime_requests"] != [] \
                or pos["open_positions"] != 0 or pos["working_orders"] != 0:
            return "flatness_uncertain"
        return None
    venue_equity = _decimal(equity["equity_at_effective_close"])
    if venue_equity is None or venue_equity != c.net_equity or not str(equity["valuation_basis"] or "").strip() \
            or "close_equity" not in c.roles or c.roles["close_equity"]["file"] not in str(equity["valuation_basis"]):
        return "venue_equity_at_close"
    return None


def _v12_dashboard(c: _Ctx):
    dash = c.p["dashboard"]
    balance, threshold = _decimal(dash["balance"]), _decimal(dash["trailing_threshold"])
    if balance is None or threshold is None:
        return "dashboard_values"
    if not math.isfinite(float(balance)) or not math.isfinite(float(threshold)):
        return "numeric_range"
    c.peak = max(Decimal(c.head["peak"]), c.net_equity)
    if not math.isfinite(float(c.net_equity)) or not math.isfinite(float(c.peak)) or float(c.peak) <= 0:
        return "numeric_range"
    if c.scope == "record_only":
        if balance != c.full_history_equity or threshold + _WIDTH < c.peak:
            return "dashboard_disagreement"
    elif balance != c.net_equity or threshold + _WIDTH != c.peak:
        return "dashboard_disagreement"
    return None


def _v13_attestations(c: _Ctx):
    if any(c.p["attestations"][k] is not True for k in _ATTESTATIONS):
        return "attestation_incomplete"
    return None


_INVARIANTS = (_v1_shape, _v2_account, _v3_scope, _v4_digests, _v5_session_chain, _v6_effective_close,
               _v8_sources, _v7_chronology, _v9_ledger, _v10_transactions, _v10_source_ledger, _v11_close_equity, _v12_dashboard,
               _v13_attestations)


def _verified_context(package: dict, sources: dict[str, bytes], *, head: dict, previous_package: dict | None,
                   account: str, calendar_digest: str, policy_digest: str, calendar: SessionCalendar,
                   scope: str, now: datetime, issued_utc: datetime | None = None) -> _Ctx | str:
    if not _aware(now) or (issued_utc is not None and not _aware(issued_utc)):
        return "invalid_now"
    ctx = _Ctx(package, sources, head, previous_package, account, calendar_digest, policy_digest,
               calendar, scope, now, issued_utc)
    for invariant in _INVARIANTS:
        reason = invariant(ctx)
        if reason is not None:
            return reason
    return ctx


def verify_package(package: dict, sources: dict[str, bytes], *, head: dict, previous_package: dict | None,
                   account: str, calendar_digest: str, policy_digest: str, calendar: SessionCalendar,
                   scope: str, now: datetime, issued_utc: datetime | None = None) -> str | None:
    """Return the first violated invariant's refusal, or None when every invariant holds."""
    result = _verified_context(package, sources, head=head, previous_package=previous_package, account=account,
        calendar_digest=calendar_digest, policy_digest=policy_digest, calendar=calendar, scope=scope,
        now=now, issued_utc=issued_utc)
    return result if isinstance(result, str) else None



@dataclass(frozen=True)
class ProposedClose:
    """Validated arithmetic result; the durable owner alone can accept it."""
    equity: Decimal
    peak: Decimal
    mode_next: Mode


def calculate_close(package: dict, sources: dict[str, bytes], *, policy: ProtectionPolicy, head: dict,
                    previous_package: dict | None, account: str, calendar_digest: str, policy_digest: str,
                    calendar: SessionCalendar, scope: str, now: datetime,
                    issued_utc: datetime | None = None) -> ProposedClose | Refusal:
    policy = require_policy(policy)
    result = _verified_context(package, sources, head=head, previous_package=previous_package, account=account,
        calendar_digest=calendar_digest, policy_digest=policy_digest, calendar=calendar, scope=scope,
        now=now, issued_utc=issued_utc)
    if isinstance(result, str):
        return Refusal(result, halt_required=result in {"history_changed", "transaction_revision_detected", "out_of_order_settlement", "report_timezone_changed"})
    mode = Mode.PROTECTED if is_protected(float(result.net_equity), float(result.peak), policy) else Mode.NORMAL
    return ProposedClose(result.net_equity, result.peak, mode)
