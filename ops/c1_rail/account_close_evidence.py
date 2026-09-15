"""Source-bound report ingestion; no settlement, policy or storage authority."""
from __future__ import annotations

import csv
import hashlib
import io
import math
import re
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal, InvalidOperation
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


ET = ZoneInfo("America/New_York")
CASH_COLUMNS = ["Account", "Transaction ID", "Timestamp", "Date", "Delta", "Amount", "Cash Change Type",
                "Currency", "Contract"]
BALANCE_COLUMNS = ["Account ID", "Account Name", "Trade Date", "Total Amount", "Total Realized PNL"]
COST_TYPES = {"Commission": "commission", "Exchange Fee": "exchange", "Clearing Fee": "clearing", "Nfa Fee": "nfa"}
TRADE_TYPE = "Trade Paired"
FUND_TYPE = "Fund Transaction"
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
    account_id: str | None = None       # transcribed from this specific source, never from a filename


def _decimal(text: str, label: str) -> Decimal:
    # Validate the export spelling before removing currency/grouping characters.
    # Allow one leading sign and dollar symbol (in either order), and groups of
    # exactly three digits. Scientific notation retains the numeric-range check.
    if not isinstance(text, str) or not re.fullmatch(
            r"(?:[+-]?\$?|\$[+-]?)(?:(?:[0-9]+|[0-9]{1,3}(?:,[0-9]{3})+)"
            r"(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?", text.strip()):
        raise AssemblyError(f"{label}: not a decimal")
    try:
        value = Decimal(text.replace(",", "").replace("$", "").strip())
    except (InvalidOperation, AttributeError) as exc:
        raise AssemblyError(f"{label}: not a decimal") from exc
    if not value.is_finite():
        raise AssemblyError(f"{label}: not finite")
    if not math.isfinite(float(value)):
        raise AssemblyError(f"{label}: unsupported numeric range")
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
    require_aware(ts, "transaction timestamp")
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
    require_aware(value, "evidence timestamp")
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def require_aware(value: datetime, label: str) -> None:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise AssemblyError(f"{label}: timezone-aware timestamp required")


def validate_source_files(files: list[SourceFile], *, account_id: str) -> None:
    """Bind operator-transcribed identities to the specific retained captures."""
    names = set()
    for source in files:
        require_aware(source.captured_utc, source.name)
        if not isinstance(source.account_id, str) or not source.account_id.strip() or source.account_id != account_id:
            raise AssemblyError(f"{source.name}: source account missing or different account")
        if not isinstance(source.name, str) or not source.name.strip() or source.name in names:
            raise AssemblyError("source filenames must be nonempty and distinct")
        if not isinstance(source.data, bytes):
            raise AssemblyError(f"{source.name}: original source bytes required")
        names.add(source.name)


def parse_cash_report(data: bytes, *, report_tz: ZoneInfo, captured_utc: datetime,
                      account_id: str) -> list[CashRow]:
    """Parse retained cash bytes; makes no query-window or completeness assertion.

    Keep raw order and duplicate rows so the caller can detect inventory conflicts.
    Authentication of the retained bytes and capture metadata belongs to the owner.
    """
    if not isinstance(account_id, str) or not account_id.strip():
        raise AssemblyError("cash report: source account required")
    return _parse_cash_report(data, report_tz=report_tz, captured_utc=captured_utc,
                              account_id=account_id, label="cash report")


def _parse_cash_report(data: bytes, *, report_tz: ZoneInfo, captured_utc: datetime,
                       account_id: str | None, label: str) -> list[CashRow]:
    require_aware(captured_utc, label)
    text = data.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        # An empty query result exports as an empty file or a bare line ending.
        if text.strip():
            raise AssemblyError(f"{label}: unreadable header")
        return []
    if reader.fieldnames != CASH_COLUMNS:
        raise AssemblyError(f"{label}: unexpected cash columns")
    rows = []
    for raw in reader:
        if None in raw or any(value is None for value in raw.values()):
            raise AssemblyError(f"{label}: cash row column count")
        tid = raw["Transaction ID"].strip()
        if not re.fullmatch(r"\d+", tid):
            raise AssemblyError(f"{label}: transaction id shape")
        if raw["Currency"].strip() != "USD":
            raise AssemblyError(f"{label}: currency")
        ts_local = _local(raw["Timestamp"], report_tz, f"{label}:{tid}")
        content = "|".join(raw[c].strip() for c in CASH_COLUMNS)
        row = CashRow(tid, raw["Account"].strip(), ts_local, ts_local.astimezone(timezone.utc),
                      date.fromisoformat(raw["Date"].strip()), _decimal(raw["Delta"], "delta"),
                      _decimal(raw["Amount"], "amount"), raw["Cash Change Type"].strip(),
                      raw["Contract"].strip(), sha256_hex(content.encode("utf-8")))
        if row.ts_utc > captured_utc:
            raise AssemblyError(f"{label}:{tid}: transaction after capture")
        if account_id is not None and row.account != account_id:
            raise AssemblyError(f"{label}:{tid}: different account from query capture")
        rows.append(row)
    return rows


def parse_cash_windows(files: list[SourceFile], *, report_tz: ZoneInfo) -> tuple[list[CashRow], dict]:
    """Union of windows, deduplicated by transaction id; revisions and duplicates are named."""
    rows: dict[str, CashRow] = {}
    revisions: list[str] = []
    per_window = []
    accounts: set[str] = set()
    if not files:
        raise AssemblyError("cash windows missing")
    for win in files:
        require_aware(win.captured_utc, win.name)
        if type(win.window_from) is not date or type(win.window_to) is not date or win.window_to < win.window_from:
            raise AssemblyError(f"{win.name}: window labels")
        if (win.window_to - win.window_from).days + 1 > MAX_WINDOW_DAYS:
            raise AssemblyError(f"{win.name}: window exceeds local calendar-day limit")
    ordered = sorted(files, key=lambda f: f.window_from)
    for win in ordered:
        if win.window_from is None or win.window_to is None or win.window_to < win.window_from:
            raise AssemblyError(f"{win.name}: window labels")
        if win.query_complete is not True:
            raise AssemblyError(f"{win.name}: query completion not attested from the retained query capture")
        parsed = _parse_cash_report(win.data, report_tz=report_tz, captured_utc=win.captured_utc,
                                    account_id=win.account_id, label=win.name)
        count = len(parsed)
        for row in parsed:
            if not win.window_from <= row.ts_local.date() <= win.window_to:
                raise AssemblyError(f"{win.name}:{row.transaction_id}: transaction timestamp outside query window")
            accounts.add(row.account)
            tid = row.transaction_id
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
        if None in raw or any(value is None for value in raw.values()):
            raise AssemblyError("balance history row column count")
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



def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


REQUIRED_SOURCE_ROLES = frozenset({"dashboard", "positions", "orders", "balance_history", "cash_history", "inception"})
_SOURCE_KEYS = {"role", "file", "sha256", "captured_utc", "account_id"}


def verify_source_manifest(package: dict, sources: dict[str, bytes]) -> dict[str, dict] | str:
    """Return verified roles or a refusal. An attested identity is not inferred from bytes."""
    rows = package.get("sources")
    if not isinstance(rows, list) or not rows:
        return "source_row"
    if not isinstance(package.get("equity", {}), dict):
        return "source_row"
    required = REQUIRED_SOURCE_ROLES | ({"close_equity"} if package.get("scope") == "record_only" or
        package.get("equity", {}).get("flatness_basis") == "VENUE_EQUITY_AT_CLOSE" else set())
    roles, files, digest_roles = {}, set(), {}
    for src in rows:
        if not isinstance(src, dict) or set(src) != _SOURCE_KEYS or any(
                not isinstance(src[k], str) or not src[k].strip() for k in _SOURCE_KEYS) or not re.fullmatch(
                    r"[0-9a-f]{64}", src["sha256"]):
            return "source_row"
        if src["account_id"] != package.get("account_id"):
            return "source_account_mismatch"
        if parse_utc(src["captured_utc"]) is None:
            return "source_row"
        if src["role"] in roles:
            return "duplicate_source_role"
        prior_role = digest_roles.get(src["sha256"])
        if src["file"] in files or (prior_role is not None and not (
                _cash_role(src["role"]) and _cash_role(prior_role))):
            return "source_not_distinct"
        data = sources.get(src["file"]) if isinstance(sources, dict) else None
        if not isinstance(data, bytes) or sha256_hex(data) != src["sha256"]:
            return "source_bytes_mismatch"
        files.add(src["file"])
        digest_roles[src["sha256"]] = src["role"]
        roles[src["role"]] = dict(src)
    if not required <= roles.keys():
        return "source_role_missing"
    return roles


def _cash_role(role: str) -> bool:
    return role == "cash_history" or role.startswith("cash_history:")


def parse_utc(text: object) -> datetime | None:
    if not isinstance(text, str) or not text.endswith("Z"):
        return None
    try:
        return datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def verify_history_coverage(coverage: dict, roles: dict[str, dict], *, report_timezone: str,
                            inception: datetime) -> str | None:
    """Every continuous query interval has its own retained, account-bound source."""
    if not isinstance(coverage, dict) or set(coverage) != {"window_limit_days", "windows"}:
        return "chronology:coverage_keys"
    limit = coverage["window_limit_days"]
    if type(limit) is not int or not 0 < limit <= MAX_WINDOW_DAYS:
        return "chronology:coverage_window_limit"
    windows = coverage["windows"]
    if not isinstance(windows, list) or not windows:
        return "chronology:coverage_windows"
    try:
        tz = ZoneInfo(report_timezone)
    except (ZoneInfoNotFoundError, TypeError, ValueError):
        return "report_timezone"
    cash = {s["file"]: s for r, s in roles.items() if _cash_role(r)}
    cursor, used = None, set()
    for win in windows:
        if not isinstance(win, dict) or set(win) != {"file", "from_utc", "to_utc", "rows", "complete"}:
            return "chronology:coverage_window_row"
        if not isinstance(win["file"], str) or win["file"] not in cash:
            return "chronology:coverage_source_missing"
        if win["file"] in used:
            return "chronology:coverage_source_reused"
        start, end = parse_utc(win["from_utc"]), parse_utc(win["to_utc"])
        if start is None or end is None or end <= start:
            return "chronology:coverage_window_span"
        local_start, local_end = start.astimezone(tz), end.astimezone(tz)
        covered_dates = (local_end.date() - local_start.date()).days + (local_end.time() != time(0))
        if covered_dates > limit:
            return "chronology:coverage_window_span"
        if win["complete"] is not True or type(win["rows"]) is not int or win["rows"] < 0:
            return "chronology:coverage_window_incomplete"
        if cursor is None:
            if start > inception:
                return "chronology:coverage_gap_at_inception"
        elif start > cursor:
            return "chronology:coverage_gap"
        captured = parse_utc(cash[win["file"]]["captured_utc"])
        if captured is None or end > captured:
            return "chronology:coverage_after_capture"
        cursor = max(cursor, end) if cursor is not None else end
        used.add(win["file"])
    if used != cash.keys():
        return "chronology:coverage_source_unbound"
    if cursor != parse_utc(roles["cash_history"]["captured_utc"]):
        return "chronology:coverage_end_not_capture"
    if cursor <= inception:
        return "chronology:coverage_gap_at_inception"
    return None
