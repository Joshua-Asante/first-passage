"""Synthetic package producer shared by pure calculation and durable-owner tests."""
from datetime import datetime, timedelta, timezone
import csv
import io
from decimal import Decimal
from pathlib import Path
from zoneinfo import ZoneInfo

from c1_rail.account_close_calculation import CONTRACT, PACKAGE_SCHEMA
from c1_rail.account_close_evidence import sha256_hex
from c1_rail.book_session_calendar import load_ratified_calendar

REPO = Path(__file__).resolve().parents[2]
CAL_DIR = REPO / "ops/calendars"
CALENDAR = load_ratified_calendar(CAL_DIR / "book_session_calendar_2026-09.json",
    overlay_path=CAL_DIR / "book_closure_overlay.json", ratified_path=CAL_DIR / "RATIFIED.json", repo_root=REPO)
ACCOUNT = "synthetic-account"
POLICY_DIGEST = "b" * 64

# Original synthetic rows retained so the existing inventory-only fixture API can
# reproduce exact prior report content, including costs and nondefault gross P&L.
_RAW_ROWS = {}


def utc(value):
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def history_windows(captured):
    cursor = datetime(2026, 8, 20, tzinfo=ZoneInfo("America/New_York"))
    windows = []
    while cursor < captured:
        end = min(cursor + timedelta(days=14), captured)
        windows.append({"from_utc": utc(cursor), "to_utc": utc(end), "rows": 0, "complete": True})
        if end == captured:
            break
        cursor += timedelta(days=13)
    return {"window_limit_days": 14, "windows": windows}


def package(head, session_id: str, now: datetime, *, gross="250.00", prior_tx=(), net=None,
            flatness="DAILY_FLATTEN_CONFIRMED_NO_LATER_FILLS", scope="submit_account_close",
            basis="VENUE_ROW") -> tuple[dict, dict[str, bytes]]:
    row = CALENDAR.schedule_for(session_id)
    costs = {"commission": "4.00", "exchange": "1.20", "clearing": "0.30", "nfa": "0.04"}
    net_equity = Decimal(head.equity) + Decimal(gross) - sum(Decimal(v) for v in costs.values())
    if net is not None:
        net_equity = Decimal(net)
    peak = max(Decimal(head.peak), net_equity)
    captured = utc(now - timedelta(minutes=5))
    files = {"dashboard.png": b"dash-" + session_id.encode(), "positions.csv": b"pos-" + session_id.encode(),
             "orders.csv": b"ord-" + session_id.encode(),
             "balance_history.csv": b"bal-" + session_id.encode(), "cash_history.csv": b"cash-" + session_id.encode(),
             "inception.pdf": b"inception-evidence"}
    txs = [dict(t) for t in prior_tx] + \
          [{"id": f"tx-{session_id[-5:]}-{i}", "sha256": sha256_hex(f"row-{session_id}-{i}".encode()),
            "session_id": session_id} for i in range(2)]
    pkg = {
        "schema": PACKAGE_SCHEMA, "contract": CONTRACT, "account_id": ACCOUNT, "venue": "Tradeify_Select_100K",
        "session_id": session_id, "predecessor_session_id": head.session_id,
        "predecessor_package_sha256": head.package_sha256, "calendar_digest": CALENDAR.calendar_digest,
        "policy_digest": POLICY_DIGEST, "effective_close_utc": utc(row.closes_at),
        "source_publication_utc": None,
        "report_timezone": "America/New_York", "inception_utc": "2026-08-20T13:00:00Z",
        "equity": {"net_equity": str(net_equity), "basis": "NET_OF_TRADING_COSTS", "at_effective_close": "FLAT",
                   "flatness_basis": flatness, "equity_at_effective_close": None, "valuation_basis": None},
        "ledger": {"predecessor_net_equity": head.equity, "gross_trade_pnl": gross, "trading_costs": costs,
                   "adjustments_abs_total": "0", "unknown_rows": 0, "unlinked_fee_rows": 0,
                   "transactions": txs, "revisions": [],
                   "coverage": history_windows(now - timedelta(minutes=5))},
        "dashboard": {"balance": str(net_equity), "trailing_threshold": str(peak - 3000), "captured_utc": captured},
        "positions": {"open_positions": 0, "working_orders": 0, "captured_utc": captured},
        "sources": [{"role": r, "file": f, "sha256": sha256_hex(files[f]), "captured_utc": captured if r != "inception" else "2026-08-20T13:05:00Z"}
                    for r, f in (("dashboard", "dashboard.png"), ("positions", "positions.csv"), ("orders", "orders.csv"),
                                 ("balance_history", "balance_history.csv"), ("cash_history", "cash_history.csv"),
                                 ("inception", "inception.pdf"))],
        "attestations": {"reflects_effective_close": True, "costs_included_once": True,
                         "no_known_pending_correction": True, "no_conflicting_observation": True},
        "unresolved_runtime_requests": [],
        "scope": scope, "settlement_basis": basis,
    }
    if scope == "record_only":
        files["close_equity.png"] = b"synthetic venue close equity-" + session_id.encode()
        pkg["sources"].append({"role": "close_equity", "file": "close_equity.png",
                               "sha256": sha256_hex(files["close_equity.png"]), "captured_utc": captured})
        pkg["equity"].update(flatness_basis="VENUE_EQUITY_AT_CLOSE", at_effective_close="VENUE_EQUITY_AT_CLOSE",
                             equity_at_effective_close=str(net_equity), valuation_basis="close_equity.png")
    for src in pkg["sources"]:
        src["account_id"] = ACCOUNT
    # Every declared history window has its own retained export, including empty ranges.
    windows = pkg["ledger"]["coverage"]["windows"]
    for i, win in enumerate(windows):
        if i == len(windows) - 1:
            win["file"] = "cash_history.csv"
        else:
            name = f"cash_history_{i}.csv"
            files[name] = f"earlier cash window {i}".encode()
            pkg["sources"].append({"role": f"cash_history:{i}", "file": name,
                "sha256": sha256_hex(files[name]), "captured_utc": captured, "account_id": ACCOUNT})
            win["file"] = name
    _bind_csv_reports(pkg, files, head, gross, prior_tx)
    return pkg, files



def _bind_csv_reports(pkg, files, head, gross, prior_tx):
    from account_close_evidence import CASH_COLUMNS, BALANCE_COLUMNS
    tz = ZoneInfo(pkg["report_timezone"])
    rows = [list(_RAW_ROWS[t["sha256"]]) for t in prior_tx if t["sha256"] in _RAW_ROWS]
    def add(tid, ts, delta, running, kind, contract="MYMU6"):
        raw = [ACCOUNT, str(tid), ts.strftime("%m/%d/%Y %H:%M:%S"), ts.date().isoformat(),
               str(delta), str(running), kind, "USD", contract]
        rows.append(raw)
    fund_ts = datetime(2026, 8, 20, 9, tzinfo=tz)
    if not any(r[6] == "Fund Transaction" for r in rows):
        add(1, fund_ts, "100000.00", "100000.00", "Fund Transaction", "")
    if not prior_tx and Decimal(head.equity) != Decimal("100000"):
        delta = Decimal(head.equity) - Decimal("100000")
        add(2, datetime.fromisoformat(head.session_id.split(":")[1]).replace(hour=12, tzinfo=tz),
            delta, head.equity, "Trade Paired")
    sid = pkg["session_id"]
    day = datetime.fromisoformat(sid.split(":")[1]).replace(hour=12, tzinfo=tz)
    base = int(day.strftime("%Y%m%d")) * 10
    existing = {r[1] for r in rows}
    if str(base) not in existing:
        running = Decimal(head.equity)
        for i, (kind, delta) in enumerate((("Commission", "-4.00"), ("Exchange Fee", "-1.20"),
                ("Clearing Fee", "-0.30"), ("Nfa Fee", "-0.04"), ("Trade Paired", gross))):
            running += Decimal(delta)
            add(base + i, day, delta, running, kind)
    rows.sort(key=lambda r: (datetime.strptime(r[2], "%m/%d/%Y %H:%M:%S"), int(r[1])))
    def csv_bytes(header, body):
        out = io.StringIO(newline="")
        writer = csv.writer(out, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(body)
        return out.getvalue().encode()
    inventory = []
    for raw in rows:
        digest = sha256_hex("|".join(raw).encode())
        _RAW_ROWS[digest] = list(raw)
        inventory.append({"id": raw[1], "sha256": digest, "session_id": "tradeify-account-day:" + raw[3]})
    pkg["ledger"]["transactions"] = inventory
    windows = pkg["ledger"]["coverage"]["windows"]
    for win in windows:
        start = datetime.fromisoformat(win["from_utc"].replace("Z", "+00:00"))
        end = datetime.fromisoformat(win["to_utc"].replace("Z", "+00:00"))
        selected = [r for r in rows if start <= datetime.strptime(r[2], "%m/%d/%Y %H:%M:%S").replace(tzinfo=tz) < end]
        files[win["file"]] = csv_bytes(CASH_COLUMNS, selected)
        win["rows"] = len(selected)
    amounts = {r[3]: r[5] for r in rows}
    amounts.setdefault(head.session_id.split(":")[1], head.equity)
    files["balance_history.csv"] = csv_bytes(BALANCE_COLUMNS,
        [["12345", ACCOUNT, d, amount, "0"] for d, amount in sorted(amounts.items())])
    for source in pkg["sources"]:
        source["sha256"] = sha256_hex(files[source["file"]])


def b7_cash_history(balance="100000", session_id="tradeify-account-day:2026-09-11"):
    """Synthetic sealed E3 rows, matching the subsequent fixture's funding identity."""
    from account_close_evidence import CASH_COLUMNS
    rows = [[ACCOUNT, "1", "08/20/2026 09:00:00", "2026-08-20", "100000.00", "100000.00", "Fund Transaction", "USD", ""]]
    if Decimal(balance) != Decimal("100000"):
        day = datetime.fromisoformat(session_id.split(":")[1])
        rows.append([ACCOUNT, "2", day.strftime("%m/%d/%Y") + " 12:00:00", day.date().isoformat(),
                     str(Decimal(balance) - Decimal("100000")), str(balance), "Trade Paired", "USD", "MYMU6"])
    out = io.StringIO(newline="")
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(CASH_COLUMNS)
    writer.writerows(rows)
    return out.getvalue().encode()


def b7_previous_package(balance="100000", session_id="tradeify-account-day:2026-09-11"):
    reader = csv.reader(io.StringIO(b7_cash_history(balance, session_id).decode()))
    next(reader)
    return {"report_timezone": "America/New_York", "ledger": {"transactions": [
        {"id": row[1], "sha256": sha256_hex("|".join(row).encode()), "session_id": "tradeify-account-day:" + row[3]}
        for row in reader]}}
