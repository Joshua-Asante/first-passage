"""Assemble an ``account_close_package/v3`` from the venue's actual report exports.

Operator-side producer for the attended settlement contract. It reads the Tradovate
cash-history windows, the account-balance history, the Tradeify dashboard values and the
positions/orders views exactly as exported, deduplicates overlapping windows by
transaction id, classifies every cash row, reconciles the ledger from the nominal
funding basis in decimal arithmetic, maps every row to its Tradeify account session,
cross-checks the dashboard, and emits the package plus a figures-free qualification
report. It never prints account values. It does not sign, submit or accept anything;
``account_close_calculation.verify_package`` remains the judge.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal
from zoneinfo import ZoneInfo

from .book_policy import FIRM_RULES, TIER
from .book_session_calendar import SessionCalendar
from .account_close_calculation import CONTRACT, PACKAGE_SCHEMA

from .account_close_evidence import (
    AssemblyError, CashRow, SourceFile, ET, COST_TYPES, TRADE_TYPE, FUND_TYPE,
    MAX_WINDOW_DAYS, _decimal, _iso, account_session_date, session_id_for,
    parse_cash_windows, parse_balance_history, sha256_hex, require_aware, validate_source_files,
)

STARTING_BALANCE = Decimal(str(FIRM_RULES[TIER]["starting_balance"]))
WIDTH = STARTING_BALANCE * Decimal(str(FIRM_RULES[TIER]["max_dd_pct"])) / 100


from .account_close_ledger import Ledger, reconcile, equity_at_end_of, check_balance_history, transactions_for


def assemble(*, account_id: str, cash: list[SourceFile], balance: SourceFile, dashboard: SourceFile,
             positions: SourceFile, orders: SourceFile, inception: SourceFile,
             dashboard_balance: str, dashboard_threshold: str, inception_utc: datetime,
             session_id: str, predecessor_session_id: str, predecessor_package_sha256: str,
             calendar: SessionCalendar, policy_digest: str, report_tz: ZoneInfo,
             attestations: dict, unresolved_runtime_requests: list,
             open_positions: int, working_orders: int, scope: str,
             close_equity: SourceFile | None = None, close_equity_value: str | None = None) -> tuple[dict, dict, dict]:
    """Return (package, sources bytes by file, figures-free qualification report).

    ``scope`` is the signed challenge scope. A historical close (``record_only``) requires
    ``close_equity``: a separately captured venue source showing account equity at that close, and
    the operator-typed value it shows. No such venue report is known today, so historical catch-up
    refuses by design until one exists (invariant A7/V11).
    """
    require_aware(inception_utc, "inception_utc")
    all_files = cash + [balance, dashboard, positions, orders, inception] + ([close_equity] if close_equity else [])
    validate_source_files(all_files, account_id=account_id)
    expected_roles = [(balance, "balance_history"), (dashboard, "dashboard"), (positions, "positions"),
                      (orders, "orders"), (inception, "inception")]
    if any(f.role != role for f, role in expected_roles) or any(f.role != "cash_history" for f in cash):
        raise AssemblyError("source role does not match input")
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
    session_day_for_row = date.fromisoformat(session_id.split(":")[1])
    if not historical and [r for r in rows if r.kind == TRADE_TYPE and r.ts_utc > row.closes_at]:
        raise AssemblyError("effective-close flatness not established; venue equity at the close required")
    balance_rows = parse_balance_history(balance.data, account_id=account_id)
    balance_report = check_balance_history(ledger, balance_rows)
    if balance_report["mismatches"]:
        raise AssemblyError("balance history disagrees with the reconciled ledger")
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
    if historical:
        # Historical catch-up: the fresh full history legitimately contains fills from later missed
        # sessions, so flatness cannot be inferred from their absence, and a balance row is cash, not
        # equity, if a position was carried. Only venue-backed close equity establishes the close.
        if close_equity is None or close_equity.role != "close_equity" or close_equity_value is None:
            raise AssemblyError("historical close equity evidence required for record_only")
        if _decimal(close_equity_value, "close equity") != net_equity:
            raise AssemblyError("venue close equity disagrees with the reconciled cash balance; boundary not flat")
        flat_basis = "VENUE_EQUITY_AT_CLOSE"
    else:
        # Flat at the effective close follows only when the account is flat at capture AND no fill
        # occurred between that close and the capture: a position carried past the close would have
        # produced a later Trade Paired row. A later flat snapshot alone proves nothing.
        if later_fills or open_positions or working_orders:
            raise AssemblyError("effective-close flatness not established; venue equity at the close required")
        flat_basis = "DAILY_FLATTEN_CONFIRMED_NO_LATER_FILLS"
    dash_balance = _decimal(dashboard_balance, "dashboard balance")
    dash_threshold = _decimal(dashboard_threshold, "dashboard threshold")
    peak = max(ledger.peak, net_equity)
    windows = []
    for win in sorted(cash, key=lambda f: f.window_from):
        start = datetime.combine(win.window_from, time(0), tzinfo=report_tz).astimezone(timezone.utc)
        end = min(datetime.combine(win.window_to + timedelta(days=1), time(0), tzinfo=report_tz).astimezone(timezone.utc),
                  win.captured_utc)
        rows_in = next(w["rows"] for w in window_report["windows"] if w["file"] == win.name)
        windows.append({"file": win.name, "from_utc": _iso(start), "to_utc": _iso(end), "rows": rows_in, "complete": True})
    transactions = transactions_for(rows)
    latest_cash = max(cash, key=lambda f: f.window_to)
    package = {
        "schema": PACKAGE_SCHEMA, "contract": CONTRACT, "account_id": account_id, "venue": TIER,
        "session_id": session_id, "predecessor_session_id": predecessor_session_id,
        "predecessor_package_sha256": predecessor_package_sha256,
        "calendar_digest": calendar.calendar_digest, "policy_digest": policy_digest,
        "effective_close_utc": _iso(row.closes_at), "source_publication_utc": None,
        "report_timezone": report_tz.key,
        "inception_utc": _iso(inception_utc),
        "equity": {"net_equity": str(net_equity), "basis": "NET_OF_TRADING_COSTS",
                   "at_effective_close": "FLAT" if not historical else "VENUE_EQUITY",
                   "flatness_basis": flat_basis,
                   "equity_at_effective_close": None if not historical else str(net_equity),
                   "valuation_basis": None if not historical else
                   f"venue close-equity capture {close_equity.name} for trade date "
                   f"{session_day_for_row.isoformat()}, corroborated by the balance-history row"},
        "ledger": {"predecessor_net_equity": str(predecessor_equity), "gross_trade_pnl": str(bucket["gross"]),
                   "trading_costs": {k: str(v) for k, v in bucket["costs"].items()},
                   "adjustments_abs_total": str(ledger.adjustments_abs_total), "unknown_rows": ledger.unknown_rows,
                   "unlinked_fee_rows": ledger.unlinked_fee_rows, "transactions": transactions, "revisions": [],
                   "coverage": {"window_limit_days": MAX_WINDOW_DAYS, "windows": windows}},
        "dashboard": {"balance": str(dash_balance), "trailing_threshold": str(dash_threshold),
                      "captured_utc": _iso(dashboard.captured_utc)},
        "positions": {"open_positions": open_positions, "working_orders": working_orders,
                      "captured_utc": _iso(positions.captured_utc)},
        "sources": [{"role": f.role, "file": f.name, "sha256": sha256_hex(f.data), "captured_utc": _iso(f.captured_utc), "account_id": f.account_id}
                    for f in [latest_cash, balance, dashboard, positions, orders, inception]
                    + ([close_equity] if close_equity is not None else [])] +
                   [{"role": f"cash_history:{f.window_from.isoformat()}..{f.window_to.isoformat()}", "file": f.name,
                     "sha256": sha256_hex(f.data), "captured_utc": _iso(f.captured_utc), "account_id": f.account_id}
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
