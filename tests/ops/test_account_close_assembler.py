"""Venue report exports (synthetic, exact column shapes) -> package -> verify_package -> consumer."""
from dataclasses import replace
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from account_close_assembler import (
    AssemblyError, SourceFile, account_session_date, assemble, parse_cash_windows, reconcile,
)
from book_policy import candidate_book_protection_policy
from book_session_calendar import load_ratified_calendar
from book_settlement import canonical_bytes, sha256_hex, verify_package
from book_sizing_context import SettledClose, size_book_request
from c1_signal_daemon.book_protocol import Mode
from test_tradeify_sizing_integration import inputs

REPO = Path(__file__).resolve().parents[2]
CAL_DIR = REPO / "ops" / "calendars"
CALENDAR = load_ratified_calendar(CAL_DIR / "book_session_calendar_2026-09.json",
                                  overlay_path=CAL_DIR / "book_closure_overlay.json",
                                  ratified_path=CAL_DIR / "RATIFIED.json", repo_root=REPO)
POLICY = candidate_book_protection_policy()
CT = ZoneInfo("America/Chicago")
ACCOUNT = "TDFYSL000000000000"
HEADER = "Account,Transaction ID,Timestamp,Date,Delta,Amount,Cash Change Type,Currency,Contract\n"
CAPTURE = datetime(2026, 9, 15, 11, 17, tzinfo=timezone.utc)
NOW = datetime(2026, 9, 15, 11, 25, tzinfo=timezone.utc)
S11, S14, S15 = ("tradeify-account-day:2026-09-%02d" % d for d in (11, 14, 15))


def row(tid, ts, delta, amount, kind, contract="MYMU6", d=None):
    day = d or ts.split(" ")[0]
    y, m, dd = day[6:10], day[0:2], day[3:5]
    quoted = f'"{amount}"' if "," in amount else amount
    return f"{ACCOUNT},{tid},{ts},{y}-{m}-{dd},{delta},{quoted}, {kind},USD,{contract}\n"


def trade_rows(base_id, ts, gross, running):
    """One paired trade as the venue reports it: four fee rows then the paired P&L row."""
    fees = [("Commission", "-1.00"), ("Exchange Fee", "-1.20"), ("Clearing Fee", "-0.30"), ("Nfa Fee", "-0.10")]
    out, bal = "", Decimal(running)
    for i, (kind, delta) in enumerate(fees):
        bal += Decimal(delta)
        out += row(base_id + i, ts, delta, f"{bal:,.2f}", kind)
    bal += Decimal(gross)
    out += row(base_id + 4, ts, gross, f"{bal:,.2f}", "Trade Paired")
    return out, bal


def synthetic():
    fund = row(100000000001, "07/18/2026 10:00:00", "100000.00", "100,000.00", "Fund Transaction", contract="")
    t1, bal1 = trade_rows(100000000100, "09/10/2026 09:31:00", "25.00", "100000.00")     # session 09-10
    t2, bal2 = trade_rows(100000000200, "09/14/2026 10:02:00", "-10.00", str(bal1))       # session 09-14
    windows = [
        ("cash-history-2026-07-04_2026-07-17.csv", date(2026, 7, 4), date(2026, 7, 17), "\r\n"),   # empty result export
        ("cash-history-2026-07-17_2026-07-30.csv", date(2026, 7, 17), date(2026, 7, 30), HEADER + fund),
        ("cash-history-2026-07-30_2026-08-12.csv", date(2026, 7, 30), date(2026, 8, 12), HEADER),
        ("cash-history-2026-08-12_2026-08-25.csv", date(2026, 8, 12), date(2026, 8, 25), HEADER),
        ("cash-history-2026-08-25_2026-09-07.csv", date(2026, 8, 25), date(2026, 9, 7), HEADER),
        ("cash-history-2026-09-07_2026-09-15.csv", date(2026, 9, 7), date(2026, 9, 15), HEADER + t1 + t2),
    ]
    cash = [SourceFile("cash_history", n, body.encode("utf-8"), CAPTURE - timedelta(minutes=2), f, t)
            for n, f, t, body in windows]
    balance_csv = ("Account ID,Account Name,Trade Date,Total Amount,Total Realized PNL\n"
                   f"{ACCOUNT},synthetic,2026-07-18,\"100,000.00\",0.00\n"
                   f"{ACCOUNT},synthetic,2026-07-19,\"100,000.00\",0.00\n"
                   f"{ACCOUNT},synthetic,2026-09-10,\"{bal1:,.2f}\",25.00\n"
                   f"{ACCOUNT},synthetic,2026-09-11,\"{bal1:,.2f}\",0.00\n"
                   f"{ACCOUNT},synthetic,2026-09-14,\"{bal2:,.2f}\",-10.00\n")
    files = dict(
        balance=SourceFile("balance_history", "balance.csv", balance_csv.encode(), CAPTURE - timedelta(minutes=3)),
        dashboard=SourceFile("dashboard", "dashboard.png", b"png-dash", CAPTURE),
        positions=SourceFile("positions", "positions.txt", b"positions empty", CAPTURE),
        orders=SourceFile("orders", "orders.txt", b"orders zero", CAPTURE),
        inception=SourceFile("inception", "activation.eml", b"eml", datetime(2026, 7, 18, 16, 20, 5, tzinfo=timezone.utc)),
    )
    return cash, files, bal1, bal2


def build(cash, files, bal1, bal2, **over):
    args = dict(account_id=ACCOUNT, cash=cash, dashboard_balance=f"{bal2:,.2f}",
                dashboard_threshold=str(max(bal1, bal2) - 3000), inception_utc=datetime(2026, 7, 18, 15, tzinfo=timezone.utc),
                session_id=S14, predecessor_session_id=S11, predecessor_package_sha256="0" * 64,
                calendar=CALENDAR, policy_digest="b" * 64, report_tz=CT,
                operator_signed_utc=NOW - timedelta(minutes=1),
                attestations={"reflects_effective_close": True, "costs_included_once": True,
                              "no_known_pending_correction": True, "no_conflicting_observation": True},
                unresolved_runtime_requests=[], open_positions=0, working_orders=0, **files)
    args.update(over)
    return assemble(**args)


def test_account_session_mapping_across_the_evening_boundary_and_weekend():
    """18:00 ET opens the next account day; Friday evening rolls to Monday."""
    assert account_session_date(datetime(2026, 9, 14, 21, 59, tzinfo=timezone.utc)) == date(2026, 9, 14)  # 17:59 ET
    assert account_session_date(datetime(2026, 9, 14, 22, 0, tzinfo=timezone.utc)) == date(2026, 9, 15)   # 18:00 ET
    assert account_session_date(datetime(2026, 9, 11, 23, 30, tzinfo=timezone.utc)) == date(2026, 9, 14)  # Fri 19:30 ET
    assert account_session_date(datetime(2026, 9, 13, 22, 30, tzinfo=timezone.utc)) == date(2026, 9, 14)  # Sun 18:30 ET


def test_exports_reconcile_into_a_package_the_verifier_and_consumer_accept():
    """Real column shapes in, decimal ledger continuity, dashboard cross-check, verifier PASS, consumer OK."""
    cash, files, bal1, bal2 = synthetic()
    package, sources, report = build(cash, files, bal1, bal2)
    assert report["duplicates_removed"] == 0 and report["revisions"] == 0
    assert report["classified"] == {"Fund Transaction": 1, "Commission": 2, "Exchange Fee": 2,
                                    "Clearing Fee": 2, "Nfa Fee": 2, "Trade Paired": 2}
    assert report["adjustments_abs_total_is_zero"] and report["unknown_rows"] == 0 and report["unlinked_fee_rows"] == 0
    assert report["balance_history"]["mismatches"] == 0
    assert report["dashboard_balance_equals_net_equity"] and report["dashboard_threshold_plus_width_equals_peak"]
    assert package["equity"]["net_equity"] == str(bal2) and package["ledger"]["gross_trade_pnl"] == "-10.00"
    assert package["ledger"]["trading_costs"] == {"commission": "1.00", "exchange": "1.20", "clearing": "0.30", "nfa": "0.10"}
    assert {s["role"] for s in package["sources"]} >= {"cash_history", "balance_history", "dashboard", "positions",
                                                       "orders", "inception"}
    assert sum(s["role"].startswith("cash_history") for s in package["sources"]) == 6
    head = {"session_id": S11, "package_sha256": "0" * 64, "equity": str(bal1), "peak": str(bal1),
            "as_of_utc": "2026-09-11T21:00:00Z"}
    assert verify_package(package, sources, head=head, previous_package=None, account=ACCOUNT,
                          calendar_digest=CALENDAR.calendar_digest, policy_digest="b" * 64, calendar=CALENDAR,
                          scope="submit_account_close", now=NOW) is None
    close = SettledClose(S14, CALENDAR.schedule_for(S14).closes_at, float(bal2), float(bal1),
                         sha256_hex(canonical_bytes(package)))
    consumer_now = datetime(2026, 9, 15, 13, 30, tzinfo=timezone.utc)
    session = CALENDAR.session_for(consumer_now, expected_digest=CALENDAR.calendar_digest).session
    request, context, binding = inputs(protected=False)
    binding = replace(binding, session=session, settlement=close, policy_digest="b" * 64)
    context = replace(context, session_id=S15, calendar_digest=CALENDAR.calendar_digest, settled=close, mode=Mode.NORMAL,
                      policy_digest="b" * 64, as_of=consumer_now, valid_until=consumer_now + timedelta(seconds=30))
    assert not size_book_request(request, context=context, binding=binding, policy=POLICY, now=consumer_now).halt


def test_overlapping_windows_dedupe_by_id_and_revisions_refuse():
    """Boundary-date rows appear in two windows; identical content is one row, changed content refuses."""
    cash, files, bal1, bal2 = synthetic()
    dup = cash[1].data.decode().splitlines()[1]                       # the fund row
    cash[0] = replace(cash[0], data=(HEADER + dup + "\n").encode())    # also present in the first window
    rows, report = parse_cash_windows(cash, report_tz=CT)
    assert report["raw_rows"] == 12 and report["distinct"] == 11 and report["revisions"] == []
    changed = dup.replace("100,000.00", "100,000.01")
    cash[0] = replace(cash[0], data=(HEADER + changed + "\n").encode())
    rows, report = parse_cash_windows(cash, report_tz=CT)
    assert report["revisions"] == ["100000000001"]
    with pytest.raises(AssemblyError, match="changed contents"):
        build(cash, files, bal1, bal2)


@pytest.mark.parametrize("defect,match", [
    ("second_fund", "adjustment"), ("unknown_type", "unknown"), ("unlinked_fee", "unlinked"),
    ("running_balance", "running balance"), ("later_fill", "flatness"), ("open_position", "flatness"),
    ("balance_history", "balance history"), ("dashboard_balance", None), ("dashboard_threshold", None),
])
def test_defective_exports_are_refused_or_flagged(defect, match):
    """Adjustments, unknown rows, unlinked fees, continuity breaks, later fills and disagreements surface."""
    cash, files, bal1, bal2 = synthetic()
    over = {}
    last = cash[5].data.decode()
    if defect == "second_fund":
        extra = row(100000000900, "09/14/2026 15:00:00", "50.00", f"{bal2 + 50:,.2f}", "Fund Transaction", contract="")
        cash[5] = replace(cash[5], data=(last + extra).encode())
    elif defect == "unknown_type":
        extra = row(100000000900, "09/14/2026 15:00:00", "-5.00", f"{bal2 - 5:,.2f}", "Platform Fee", contract="")
        cash[5] = replace(cash[5], data=(last + extra).encode())
    elif defect == "unlinked_fee":
        cash[5] = replace(cash[5], data=last.replace(", Commission,USD,MYMU6", ", Commission,USD,", 1).encode())
    elif defect == "running_balance":
        cash[5] = replace(cash[5], data=last.replace(",25.00,", ",26.00,", 1).encode())
    elif defect == "later_fill":
        extra, _ = trade_rows(100000000900, "09/14/2026 17:30:00", "1.00", str(bal2))   # 18:30 ET, after the close
        cash[5] = replace(cash[5], data=(last + extra).encode())
    elif defect == "open_position":
        over = {"open_positions": 1}
    elif defect == "balance_history":
        over = {"balance": replace(files["balance"], data=files["balance"].data.replace(
            f'"{bal2:,.2f}"'.encode(), f'"{bal2 - 1:,.2f}"'.encode()))}
    elif defect == "dashboard_balance":
        over = {"dashboard_balance": f"{bal2 + 1:,.2f}"}
    elif defect == "dashboard_threshold":
        over = {"dashboard_threshold": str(bal1 - 3001)}
    if match is None:
        package, sources, report = build(cash, files, bal1, bal2, **over)
        assert not (report["dashboard_balance_equals_net_equity"] and report["dashboard_threshold_plus_width_equals_peak"])
        head = {"session_id": S11, "package_sha256": "0" * 64, "equity": str(bal1), "peak": str(bal1),
                "as_of_utc": "2026-09-11T21:00:00Z"}
        assert verify_package(package, sources, head=head, previous_package=None, account=ACCOUNT,
                              calendar_digest=CALENDAR.calendar_digest, policy_digest="b" * 64, calendar=CALENDAR,
                              scope="submit_account_close", now=NOW) == "dashboard_disagreement"
    else:
        with pytest.raises(AssemblyError, match=match):
            build(cash, files, bal1, bal2, **over)
