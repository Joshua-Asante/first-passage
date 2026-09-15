"""Assemble an ``account_close_package/v1`` from the venue's actual report exports.

Operator-side producer for the attended settlement contract. It reads the Tradovate
cash-history windows, the account-balance history, the Tradeify dashboard values and the
positions/orders views exactly as exported, deduplicates overlapping windows by
transaction id, classifies every cash row, reconciles the ledger from the nominal
funding basis in decimal arithmetic, maps every row to its Tradeify account session,
cross-checks the dashboard, and emits the package plus a figures-free qualification
report. It never prints account values. It does not sign, submit or accept anything;
``book_settlement.verify_package`` remains the judge.
"""
from __future__ import annotations

import csv
import hashlib
import io
import re
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal, InvalidOperation
from zoneinfo import ZoneInfo

from book_policy import FIRM_RULES, TIER
from book_session_calendar import SessionCalendar
from book_settlement import CONTRACT, PACKAGE_SCHEMA, sha256_hex

ET = ZoneInfo("America/New_York")
CASH_COLUMNS = ["Account", "Transaction ID", "Timestamp", "Date", "Delta", "Amount", "Cash Change Type",
                "Currency", "Contract"]
BALANCE_COLUMNS = ["Account ID", "Account Name", "Trade Date", "Total Amount", "Total Realized PNL"]
COST_TYPES = {"Commission": "commission", "Exchange Fee": "exchange", "Clearing Fee": "clearing", "Nfa Fee": "nfa"}
TRADE_TYPE = "Trade Paired"
FUND_TYPE = "Fund Transaction"
STARTING_BALANCE = Decimal(str(FIRM_RULES[TIER]["starting_balance"]))
WIDTH = STARTING_BALANCE * Decimal(str(FIRM_RULES[TIER]["max_dd_pct"])) / 100
MAX_WINDOW_DAYS = 14


class AssemblyError(ValueError):
    """The exports cannot be turned into a verifiable package; the reason names the defect."""


@dataclass(frozen=True)
class CashRow:
    transaction_id: str
    account: str
    ts_local: datetime
    ts_utc: datetime
    trade_date: date
    delta: Decimal
    amount_after: Decimal
    kind: str
    contract: str
    content_sha256: str


@dataclass(frozen=True)
class SourceFile:
    role: str
    name: str
    data: bytes
    captured_utc: datetime
    window_from: date | None = None    # cash windows only, inclusive UI labels
    window_to: date | None = None
    query_complete: bool | None = None  # cash windows only: operator-typed from the retained query capture


def _decimal(text: str, label: str) -> Decimal:
    try:
        value = Decimal(text.replace(",", "").replace("$", "").strip())
    except (InvalidOperation, AttributeError) as exc:
        raise AssemblyError(f"{label}: not a decimal") from exc
    if not value.is_finite():
        raise AssemblyError(f"{label}: not finite")
    return value


def _local(text: str, tz: ZoneInfo, label: str) -> datetime:
    try:
        naive = datetime.strptime(text.strip(), "%m/%d/%Y %H:%M:%S")
    except ValueError as exc:
        raise AssemblyError(f"{label}: timestamp format") from exc
    fold0, fold1 = naive.replace(tzinfo=tz, fold=0), naive.replace(tzinfo=tz, fold=1)
    if fold0.utcoffset() != fold1.utcoffset():
        raise AssemblyError(f"{label}: ambiguous local time")
    if fold0.astimezone(timezone.utc).astimezone(tz).replace(tzinfo=None) != naive:
        raise AssemblyError(f"{label}: nonexistent local time")
    return fold0


def account_session_date(ts: datetime) -> date | None:
    """Tradeify account day containing ``ts``, or None when no session contains it.

    A session runs 18:00 ET to 17:00 ET the next calendar date, Sunday evening through Friday.
    The 17:00-18:00 ET break, Friday after 17:00, Saturday and Sunday before 18:00 belong to
    no session; a cash row there is refused rather than attributed to a neighbouring session.
    """
    local = ts.astimezone(ET)
    if time(17, 0) <= local.time() < time(18, 0):
        return None
    day = local.date() + timedelta(days=1) if local.time() >= time(18, 0) else local.date()
    if day.weekday() >= 5:
        return None
    if local.weekday() == 4 and local.time() >= time(18, 0):    # Friday evening: no session opens
        return None
    return day


def session_id_for(day: date) -> str:
    return f"tradeify-account-day:{day.isoformat()}"


def _iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_cash_windows(files: list[SourceFile], *, report_tz: ZoneInfo) -> tuple[list[CashRow], dict]:
    """Union of windows, deduplicated by transaction id; revisions and duplicates are named."""
    rows: dict[str, CashRow] = {}
    revisions: list[str] = []
    per_window = []
    accounts: set[str] = set()
    ordered = sorted(files, key=lambda f: f.window_from)
    for win in ordered:
        if win.window_from is None or win.window_to is None or win.window_to < win.window_from:
            raise AssemblyError(f"{win.name}: window labels")
        if win.query_complete is not True:
            raise AssemblyError(f"{win.name}: query completion not attested from the retained query capture")
        text = win.data.decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(text))
        count = 0
        if not reader.fieldnames:
            # An empty query result exports as an empty file or a bare line ending.
            if text.strip():
                raise AssemblyError(f"{win.name}: unreadable header")
        elif reader.fieldnames != CASH_COLUMNS:
            raise AssemblyError(f"{win.name}: unexpected cash columns")
        else:
            for raw in reader:
                count += 1
                tid = raw["Transaction ID"].strip()
                if not re.fullmatch(r"\d+", tid):
                    raise AssemblyError(f"{win.name}: transaction id shape")
                if raw["Currency"].strip() != "USD":
                    raise AssemblyError(f"{win.name}: currency")
                ts_local = _local(raw["Timestamp"], report_tz, f"{win.name}:{tid}")
                content = "|".join(raw[c].strip() for c in CASH_COLUMNS)
                row = CashRow(tid, raw["Account"].strip(), ts_local, ts_local.astimezone(timezone.utc),
                              date.fromisoformat(raw["Date"].strip()), _decimal(raw["Delta"], "delta"),
                              _decimal(raw["Amount"], "amount"), raw["Cash Change Type"].strip(),
                              raw["Contract"].strip(), sha256_hex(content.encode("utf-8")))
                accounts.add(row.account)
                if tid in rows:
                    if rows[tid].content_sha256 != row.content_sha256:
                        revisions.append(tid)
                    continue
                rows[tid] = row
        per_window.append({"file": win.name, "from": win.window_from.isoformat(), "to": win.window_to.isoformat(),
                           "rows": count, "complete": True})
    if len(accounts) > 1:
        raise AssemblyError("cash rows span more than one account")
    ordered_rows = sorted(rows.values(), key=lambda r: (r.ts_utc, int(r.transaction_id)))
    return ordered_rows, {"windows": per_window, "revisions": revisions, "distinct": len(ordered_rows),
                          "raw_rows": sum(w["rows"] for w in per_window)}


def parse_balance_history(data: bytes, *, account_id: str) -> list[tuple[date, Decimal, Decimal]]:
    reader = csv.DictReader(io.StringIO(data.decode("utf-8-sig")))
    if reader.fieldnames != BALANCE_COLUMNS:
        raise AssemblyError("unexpected balance-history columns")
    out = []
    venue_ids: set[str] = set()
    for raw in reader:
        # The venue names the account in "Account Name"; "Account ID" is its numeric internal id.
        if raw["Account Name"].strip() != account_id:
            raise AssemblyError("balance history row belongs to a different account")
        venue_ids.add(raw["Account ID"].strip())
        out.append((date.fromisoformat(raw["Trade Date"].strip()), _decimal(raw["Total Amount"], "balance"),
                    _decimal(raw["Total Realized PNL"], "pnl")))
    if len(venue_ids) > 1:
        raise AssemblyError("balance history spans more than one venue account id")
    if not out or [d for d, _, _ in out] != sorted(d for d, _, _ in out):
        raise AssemblyError("balance history empty or unordered")
    return out


@dataclass(frozen=True)
class Ledger:
    basis: Decimal
    fund_row: CashRow
    sessions: dict[date, dict]           # per account session: gross, costs, net_after, rows
    equity_after: dict[date, Decimal]    # running net after each session with activity
    peak: Decimal
    unknown_rows: int
    unlinked_fee_rows: int
    adjustments_abs_total: Decimal
    classified: dict[str, int]


def reconcile(rows: list[CashRow]) -> Ledger:
    """Nominal funding basis first, then trade P&L and transaction-linked costs per account session."""
    funds = [r for r in rows if r.kind == FUND_TYPE]
    if not funds:
        raise AssemblyError("no fund transaction establishes the nominal basis")
    fund = min(funds, key=lambda r: r.ts_utc)
    if fund.delta != STARTING_BALANCE or fund.amount_after != STARTING_BALANCE:
        raise AssemblyError("first fund transaction is not the nominal starting balance")
    if any(r.ts_utc < fund.ts_utc for r in rows):
        raise AssemblyError("cash activity precedes the funding basis")
    sessions: dict[date, dict] = {}
    running = STARTING_BALANCE
    unknown = unlinked = 0
    adjustments = Decimal(0)
    classified: dict[str, int] = {}
    peak = STARTING_BALANCE
    for row in rows:
        if row is fund:
            classified[FUND_TYPE] = classified.get(FUND_TYPE, 0) + 1
            continue
        day = account_session_date(row.ts_utc)
        if day is None:
            raise AssemblyError(f"cash row outside any account session at transaction {row.transaction_id[-4:]}; "
                                "explicit adjudication required")
        bucket = sessions.setdefault(day, {"gross": Decimal(0), "costs": {k: Decimal(0) for k in COST_TYPES.values()},
                                           "rows": 0, "trade_rows": 0, "last_ts_utc": row.ts_utc})
        bucket["rows"] += 1
        bucket["last_ts_utc"] = max(bucket["last_ts_utc"], row.ts_utc)
        classified[row.kind] = classified.get(row.kind, 0) + 1
        if row.kind == TRADE_TYPE:
            bucket["gross"] += row.delta
            bucket["trade_rows"] += 1
        elif row.kind in COST_TYPES:
            if not row.contract:
                unlinked += 1
            bucket["costs"][COST_TYPES[row.kind]] += -row.delta
        elif row.kind == FUND_TYPE:
            adjustments += abs(row.delta)
        else:
            unknown += 1
            adjustments += abs(row.delta)
        running += row.delta
        if running != row.amount_after:
            raise AssemblyError(f"running balance disagrees with the report at transaction {row.transaction_id[-4:]}")
    equity_after: dict[date, Decimal] = {}
    running = STARTING_BALANCE
    for day in sorted(sessions):
        bucket = sessions[day]
        running = running + bucket["gross"] - sum(bucket["costs"].values())
        bucket["net_after"] = running
        equity_after[day] = running
        peak = max(peak, running)
    return Ledger(STARTING_BALANCE, fund, sessions, equity_after, peak, unknown, unlinked, adjustments, classified)


def equity_at_end_of(ledger: Ledger, day: date) -> Decimal:
    value = ledger.basis
    for session_day in sorted(ledger.equity_after):
        if session_day <= day:
            value = ledger.equity_after[session_day]
    return value


def check_balance_history(ledger: Ledger, balance: list[tuple[date, Decimal, Decimal]]) -> dict:
    """Every venue balance row must equal the reconciled equity at the end of that trade date."""
    mismatches = 0
    for day, total, _ in balance:
        if equity_at_end_of(ledger, day) != total:
            mismatches += 1
    return {"rows": len(balance), "mismatches": mismatches, "first_date": balance[0][0].isoformat(),
            "last_date": balance[-1][0].isoformat()}


def assemble(*, account_id: str, cash: list[SourceFile], balance: SourceFile, dashboard: SourceFile,
             positions: SourceFile, orders: SourceFile, inception: SourceFile,
             dashboard_balance: str, dashboard_threshold: str, inception_utc: datetime,
             session_id: str, predecessor_session_id: str, predecessor_package_sha256: str,
             calendar: SessionCalendar, policy_digest: str, report_tz: ZoneInfo,
             operator_signed_utc: datetime, attestations: dict, unresolved_runtime_requests: list,
             open_positions: int, working_orders: int, scope: str) -> tuple[dict, dict, dict]:
    """Return (package, sources bytes by file, figures-free qualification report)."""
    if scope not in ("submit_account_close", "record_only"):
        raise AssemblyError("scope must be submit_account_close or record_only")
    historical = scope == "record_only"
    rows, window_report = parse_cash_windows(cash, report_tz=report_tz)
    if window_report["revisions"]:
        raise AssemblyError("same transaction id with changed contents across windows")
    if rows and rows[0].account != account_id:
        raise AssemblyError("cash rows belong to a different account")
    ledger = reconcile(rows)
    if ledger.unknown_rows:
        raise AssemblyError("unknown cash change type; production refused")
    if ledger.unlinked_fee_rows:
        raise AssemblyError("unlinked fee row without a contract; production refused")
    if ledger.adjustments_abs_total != 0:
        raise AssemblyError("cash adjustment present (deposit, withdrawal, reset or later funding); production refused")
    row = calendar.schedule_for(session_id)
    if row is None:
        raise AssemblyError("session not in the ratified calendar")
    if [r for r in rows if r.kind == TRADE_TYPE and r.ts_utc > row.closes_at]:
        raise AssemblyError("effective-close flatness not established; venue equity at the close required")
    balance_rows = parse_balance_history(balance.data, account_id=account_id)
    balance_report = check_balance_history(ledger, balance_rows)
    if balance_report["mismatches"]:
        raise AssemblyError("balance history disagrees with the reconciled ledger")
    session_day_for_row = date.fromisoformat(session_id.split(":")[1])
    venue_row = next((total for d, total, _ in balance_rows if d == session_day_for_row), None)
    session_rows = ledger.sessions.get(session_day_for_row, {}).get("rows", 0)
    if venue_row is None:
        if session_rows:
            raise AssemblyError("balance history lacks the venue row for a session with activity")
        # No-activity session: the venue emits no row. Require query coverage over the session and
        # that the latest venue row on or before the session agrees with the reconciled equity;
        # the dashboard balance cross-check below supplies the venue-published close.
        prior_rows = [(d, total) for d, total, _ in balance_rows if d <= session_day_for_row]
        if not prior_rows or prior_rows[-1][1] != equity_at_end_of(ledger, session_day_for_row):
            raise AssemblyError("no venue balance observation supports the settled session")
        if historical:
            raise AssemblyError("historical catch-up needs the venue balance row for the settled session")
        balance_basis = "NO_ACTIVITY_DASHBOARD_CORROBORATED"
    else:
        if venue_row != equity_at_end_of(ledger, session_day_for_row):
            raise AssemblyError("venue balance row for the settled session disagrees with the ledger")
        balance_basis = "VENUE_ROW"
    row = calendar.schedule_for(session_id)
    prior = calendar.schedule_for(predecessor_session_id)
    if row is None or prior is None or row.prior_session_id != predecessor_session_id:
        raise AssemblyError("session or predecessor not in the ratified calendar")
    session_day = date.fromisoformat(session_id.split(":")[1])
    prior_day = date.fromisoformat(predecessor_session_id.split(":")[1])
    bucket = ledger.sessions.get(session_day, {"gross": Decimal(0), "costs": {k: Decimal(0) for k in COST_TYPES.values()},
                                               "rows": 0, "trade_rows": 0})
    predecessor_equity = equity_at_end_of(ledger, prior_day)
    net_equity = equity_at_end_of(ledger, session_day)
    later_fills = [r for r in rows if r.kind == TRADE_TYPE and r.ts_utc > row.closes_at]
    if isinstance(open_positions, bool) or isinstance(working_orders, bool) or \
            not isinstance(open_positions, int) or not isinstance(working_orders, int) \
            or open_positions < 0 or working_orders < 0:
        raise AssemblyError("open_positions and working_orders must be typed non-negative integers")
    # Flat at the effective close follows only when the account is flat at capture AND no fill
    # occurred between that close and the capture: a position carried past the close would have
    # produced a later Trade Paired row. A later flat snapshot alone proves nothing.
    if later_fills or open_positions or working_orders:
        raise AssemblyError("effective-close flatness not established; venue equity at the close required")
    flat_basis = "DAILY_FLATTEN_CONFIRMED_NO_LATER_FILLS"
    dash_balance = _decimal(dashboard_balance, "dashboard balance")
    dash_threshold = _decimal(dashboard_threshold, "dashboard threshold")
    peak = max(ledger.peak, net_equity)
    all_files = cash + [balance, dashboard, positions, orders, inception]
    captured = {f.name: f.captured_utc for f in all_files}
    windows = []
    for win in sorted(cash, key=lambda f: f.window_from):
        start = datetime.combine(win.window_from, time(0), tzinfo=report_tz).astimezone(timezone.utc)
        end = min(datetime.combine(win.window_to + timedelta(days=1), time(0), tzinfo=report_tz).astimezone(timezone.utc),
                  win.captured_utc)
        rows_in = next(w["rows"] for w in window_report["windows"] if w["file"] == win.name)
        windows.append({"from_utc": _iso(start), "to_utc": _iso(end), "rows": rows_in, "complete": True})
    def labelled_session(r: CashRow) -> str:
        # In-session rows were mapped by reconcile(); the nominal funding row precedes every session
        # and is labelled with the first account day after it.
        day = account_session_date(r.ts_utc)
        if day is None:
            day = r.ts_utc.astimezone(ET).date() + timedelta(days=1)
            while day.weekday() >= 5:
                day += timedelta(days=1)
        return session_id_for(day)

    transactions = [{"id": r.transaction_id, "sha256": r.content_sha256, "session_id": labelled_session(r)}
                    for r in rows]
    latest_cash = max(cash, key=lambda f: f.window_to)
    package = {
        "schema": PACKAGE_SCHEMA, "contract": CONTRACT, "account_id": account_id, "venue": TIER,
        "session_id": session_id, "predecessor_session_id": predecessor_session_id,
        "predecessor_package_sha256": predecessor_package_sha256,
        "calendar_digest": calendar.calendar_digest, "policy_digest": policy_digest,
        "effective_close_utc": _iso(row.closes_at), "source_publication_utc": None,
        "operator_signed_utc": _iso(operator_signed_utc), "report_timezone": report_tz.key,
        "inception_utc": _iso(inception_utc),
        "equity": {"net_equity": str(net_equity), "basis": "NET_OF_TRADING_COSTS", "at_effective_close": "FLAT",
                   "flatness_basis": flat_basis, "equity_at_effective_close": None, "valuation_basis": None},
        "ledger": {"predecessor_net_equity": str(predecessor_equity), "gross_trade_pnl": str(bucket["gross"]),
                   "trading_costs": {k: str(v) for k, v in bucket["costs"].items()},
                   "adjustments_abs_total": str(ledger.adjustments_abs_total), "unknown_rows": ledger.unknown_rows,
                   "unlinked_fee_rows": ledger.unlinked_fee_rows, "transactions": transactions, "revisions": [],
                   "coverage": {"window_limit_days": MAX_WINDOW_DAYS, "windows": windows}},
        "dashboard": {"balance": str(dash_balance), "trailing_threshold": str(dash_threshold),
                      "captured_utc": _iso(dashboard.captured_utc)},
        "positions": {"open_positions": open_positions, "working_orders": working_orders,
                      "captured_utc": _iso(positions.captured_utc)},
        "sources": [{"role": f.role, "file": f.name, "sha256": sha256_hex(f.data), "captured_utc": _iso(f.captured_utc)}
                    for f in [latest_cash, balance, dashboard, positions, orders, inception]] +
                   [{"role": f"cash_history:{f.window_from.isoformat()}..{f.window_to.isoformat()}", "file": f.name,
                     "sha256": sha256_hex(f.data), "captured_utc": _iso(f.captured_utc)}
                    for f in sorted(cash, key=lambda f: f.window_from) if f is not latest_cash],
        "attestations": dict(attestations),
        "unresolved_runtime_requests": list(unresolved_runtime_requests),
        "scope": scope,
        "settlement_basis": balance_basis,
    }
    sources = {f.name: f.data for f in all_files}
    report = {
        "schema": "account-close-assembly-report-v1",
        "cash_windows": window_report["windows"], "raw_rows": window_report["raw_rows"],
        "distinct_transactions": window_report["distinct"], "duplicates_removed": window_report["raw_rows"] - window_report["distinct"],
        "revisions": len(window_report["revisions"]), "classified": ledger.classified,
        "unknown_rows": ledger.unknown_rows, "unlinked_fee_rows": ledger.unlinked_fee_rows,
        "adjustments_abs_total_is_zero": ledger.adjustments_abs_total == 0,
        "sessions_with_activity": len(ledger.sessions),
        "balance_history": balance_report | {"settled_session_basis": balance_basis},
        "session": {"id": session_id, "predecessor": predecessor_session_id, "rows": bucket["rows"],
                    "trade_rows": bucket["trade_rows"], "later_fills_after_close": len(later_fills),
                    "flatness_basis": flat_basis},
        "historical_catch_up": historical,
        "dashboard_balance_equals_net_equity": dash_balance == net_equity,
        "dashboard_threshold_plus_width_equals_peak": dash_threshold + WIDTH == peak,
        "dashboard_peak_at_or_above_ledger_peak": dash_threshold + WIDTH >= peak,
        "peak_from_ledger_equals_dashboard_peak": ledger.peak == dash_threshold + WIDTH,
        "package_sha256": None,
    }
    return package, sources, report
