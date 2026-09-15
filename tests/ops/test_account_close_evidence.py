"""Standalone evidence boundary tests; no calendar, signing, or settlement database."""
from dataclasses import replace
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import pytest

from account_close_evidence import (
    AssemblyError, SourceFile, parse_cash_windows, sha256_hex, validate_source_files,
    verify_source_manifest, verify_history_coverage, _decimal,
)

NOW = datetime(2026, 11, 11, 6, tzinfo=timezone.utc)
ACCOUNT = "synthetic-account"


def manifest(*, close=False):
    roles = ["dashboard", "positions", "orders", "inception", "balance_history", "cash_history", "cash_history:earlier"]
    if close:
        roles.append("close_equity")
    sources = {r: r.encode() for r in roles}
    p = {"account_id": ACCOUNT, "scope": "record_only" if close else "submit_account_close", "equity": {},
         "sources": [{"role": r, "file": r, "sha256": sha256_hex(sources[r]),
                      "captured_utc": "2026-11-11T06:00:00Z", "account_id": ACCOUNT} for r in roles]}
    return p, sources


def coverage():
    return {"window_limit_days": 14, "windows": [
        {"file": "cash_history:earlier", "from_utc": "2026-10-28T04:00:00Z", "to_utc": "2026-11-11T05:00:00Z", "rows": 0, "complete": True},
        {"file": "cash_history", "from_utc": "2026-11-10T05:00:00Z", "to_utc": "2026-11-11T06:00:00Z", "rows": 0, "complete": True}]}


def verify_coverage(cov, roles):
    return verify_history_coverage(cov, roles, report_timezone="America/New_York",
                                   inception=datetime(2026, 10, 28, 4, tzinfo=timezone.utc))


def test_full_window_binding_survives_fall_back():
    p, sources = manifest()
    roles = verify_source_manifest(p, sources)
    assert isinstance(roles, dict)
    assert verify_coverage(coverage(), roles) is None


@pytest.mark.parametrize("mutation,expected", [
    ("missing", "coverage_source_missing"), ("reuse", "coverage_source_reused"),
    ("unbound", "coverage_source_unbound"), ("wrong_role", "coverage_source_missing"),
    ("past_capture", "coverage_after_capture"), ("fifteen_dates", "coverage_window_span"),
])
def test_each_complete_window_requires_its_own_cash_capture(mutation, expected):
    p, sources = manifest()
    roles = verify_source_manifest(p, sources)
    cov = coverage()
    if mutation == "missing":
        del roles["cash_history:earlier"]
    elif mutation == "reuse":
        cov["windows"][1]["file"] = cov["windows"][0]["file"]
    elif mutation == "unbound":
        roles["cash_history:extra"] = {"file": "extra", "captured_utc": "2026-11-11T06:00:00Z"}
    elif mutation == "wrong_role":
        cov["windows"][0]["file"] = "dashboard"
    elif mutation == "past_capture":
        roles["cash_history:earlier"]["captured_utc"] = "2026-11-10T23:00:00Z"
    else:
        # Less than 14 elapsed wall days but touches 15 inclusive UI dates.
        cov["windows"][0].update(from_utc="2026-10-27T22:00:00Z", to_utc="2026-11-10T06:00:00Z")
    assert verify_coverage(cov, roles) == "chronology:" + expected


@pytest.mark.parametrize("source_role", ["dashboard", "positions", "orders", "balance_history", "cash_history:earlier", "inception"])
@pytest.mark.parametrize("reverse", [False, True])
def test_historical_equity_cannot_alias_any_other_evidence(source_role, reverse):
    p, sources = manifest(close=True)
    close = next(s for s in p["sources"] if s["role"] == "close_equity")
    sources["close_equity"] = sources[source_role]
    close["sha256"] = sha256_hex(sources[source_role])
    if reverse:
        p["sources"].reverse()
    assert verify_source_manifest(p, sources) == "source_not_distinct"


def test_distinct_empty_cash_queries_can_have_identical_csv_bytes():
    p, sources = manifest()
    for s in p["sources"]:
        if s["role"].startswith("cash_history"):
            sources[s["file"]] = b"\r\n"
            s["sha256"] = sha256_hex(b"\r\n")
    assert isinstance(verify_source_manifest(p, sources), dict)


@pytest.mark.parametrize("role", ["dashboard", "positions", "orders", "close_equity", "inception", "cash_history"])
@pytest.mark.parametrize("account", [None, "foreign-account"])
def test_source_identity_is_required_at_collection_and_verification(role, account):
    source = SourceFile(role, role, b"opaque capture", NOW, account_id=account)
    with pytest.raises(AssemblyError, match="source account"):
        validate_source_files([source], account_id=ACCOUNT)
    p, sources = manifest(close=True)
    next(s for s in p["sources"] if s["role"] == role)["account_id"] = account
    assert verify_source_manifest(p, sources) in {"source_row", "source_account_mismatch"}


@pytest.mark.parametrize("delta,valid", [(-1, True), (0, True), (1, False)])
def test_cash_capture_boundary_is_checked_before_deduplication(delta, valid):
    capture = datetime(2026, 11, 10, 15, tzinfo=timezone.utc)
    ts = capture + timedelta(seconds=delta)
    data = ("Account,Transaction ID,Timestamp,Date,Delta,Amount,Cash Change Type,Currency,Contract\n"
            f"{ACCOUNT},1,{ts.strftime('%m/%d/%Y %H:%M:%S')},2026-11-10,1,100001,Trade Paired,USD,MYM\n").encode()
    source = SourceFile("cash_history", "one.csv", data, capture, date(2026, 11, 10), date(2026, 11, 10), True, ACCOUNT)
    # Same row was valid in another, later-captured file; an impossible earlier capture still refuses.
    later = replace(source, name="later.csv", captured_utc=capture + timedelta(minutes=1))
    if valid:
        rows, report = parse_cash_windows([later, source], report_tz=ZoneInfo("UTC"))
        assert len(rows) == 1 and report["raw_rows"] == 2
    else:
        with pytest.raises(AssemblyError, match="after capture"):
            parse_cash_windows([later, source], report_tz=ZoneInfo("UTC"))


@pytest.mark.parametrize("value", ["1e309", "1e1000000"])
def test_parsed_money_is_bounded_before_assembler_arithmetic(value):
    with pytest.raises(AssemblyError, match="numeric range"):
        _decimal(value, "source value")


@pytest.mark.parametrize("timestamp,trade_date,valid", [
    ("11/10/2026 10:00:00", "2026-11-11", True),
    ("11/09/2026 10:00:00", "2026-11-10", False),
    ("11/09/2026 10:00:00", "2026-11-09", False),
])
def test_query_coverage_uses_report_timestamp_not_cme_business_date(timestamp, trade_date, valid):
    data = ("Account,Transaction ID,Timestamp,Date,Delta,Amount,Cash Change Type,Currency,Contract\n"
            f"{ACCOUNT},1,{timestamp},{trade_date},1,100001,Trade Paired,USD,MYM\n").encode()
    source = SourceFile("cash_history", "cash.csv", data, NOW, date(2026, 11, 10), date(2026, 11, 10), True, ACCOUNT)
    if valid:
        rows, _ = parse_cash_windows([source], report_tz=ZoneInfo("UTC"))
        assert rows[0].trade_date == date(2026, 11, 11)
    else:
        with pytest.raises(AssemblyError, match="outside query window"):
            parse_cash_windows([source], report_tz=ZoneInfo("UTC"))
