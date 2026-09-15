"""Pure close proposals: full package validation without a database or signing key."""
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest

from account_close_calculation import calculate_close, ProposedClose, Refusal, canonical_bytes
from account_close_evidence import sha256_hex
from account_close_test_support import ACCOUNT, CALENDAR, POLICY_DIGEST, package, utc, b7_previous_package
from book_policy import candidate_book_protection_policy
from c1_signal_daemon.book_protocol import Mode

POLICY = candidate_book_protection_policy()
S14, S15, S16 = (f"tradeify-account-day:2026-09-{d}" for d in (14, 15, 16))
NOW14 = datetime(2026, 9, 14, 21, 10, tzinfo=timezone.utc)


def initial_head():
    return SimpleNamespace(session_id="tradeify-account-day:2026-09-11", equity="100000", peak="100000",
                           package_sha256="0" * 64)


def calculate(p, sources, head, *, prev=None, now=NOW14):
    if prev is None:
        prev = b7_previous_package(head.equity, head.session_id)
    return calculate_close(p, sources, policy=POLICY, head={**vars(head),
        "as_of_utc": utc(CALENDAR.schedule_for(head.session_id).closes_at)},
        previous_package=prev, account=p["account_id"], calendar_digest=CALENDAR.calendar_digest,
        policy_digest=POLICY_DIGEST, calendar=CALENDAR, scope=p["scope"], now=now)


def proposed_head(p, result):
    assert isinstance(result, ProposedClose), result
    return SimpleNamespace(session_id=p["session_id"], equity=str(result.equity), peak=str(result.peak),
                           package_sha256=sha256_hex(canonical_bytes(p)))


def test_proposal_uses_shared_law_without_mutating_inputs():
    head = initial_head()
    p, sources = package(head, S14, NOW14)
    before = deepcopy((p, sources, vars(head)))
    result = calculate(p, sources, head)
    assert isinstance(result, ProposedClose)
    assert str(result.equity) == "100244.46" and result.peak == result.equity
    assert result.mode_next == Mode.NORMAL
    assert (p, sources, vars(head)) == before
    p, sources = package(head, S14, NOW14, gross="-1100")
    assert calculate(p, sources, head).mode_next == Mode.PROTECTED


@pytest.mark.parametrize("value", ["1e309", "1e1000000"])
def test_numeric_range_is_a_refusal_before_arithmetic_or_policy_overflow(value):
    head = initial_head()
    p, sources = package(head, S14, NOW14)
    p["equity"]["net_equity"] = value
    p["ledger"]["gross_trade_pnl"] = value
    p["ledger"]["trading_costs"] = {k: "0" for k in p["ledger"]["trading_costs"]}
    p["dashboard"].update(balance=value, trailing_threshold=value)
    assert calculate(p, sources, head) == Refusal("numeric_range")


@pytest.mark.parametrize("scope", ["record_only", "submit_account_close"])
@pytest.mark.parametrize("field", ["balance", "trailing_threshold"])
@pytest.mark.parametrize("value", ["1e309", "1e1000000"])
def test_dashboard_values_are_bounded_before_comparison(scope, field, value):
    head = initial_head()
    p, sources = package(head, S14, NOW14, scope=scope)
    p["dashboard"][field] = value
    assert calculate(p, sources, head) == Refusal("numeric_range")


def catchup():
    head = initial_head()
    p1, f1 = package(head, S14, NOW14)
    h1 = proposed_head(p1, calculate(p1, f1, head))
    now = NOW14 + timedelta(days=2)
    p2, f2 = package(h1, S15, now, scope="record_only", prior_tx=p1["ledger"]["transactions"])
    # Build actual full-history cash reports including the next missed session.
    future_head = SimpleNamespace(session_id=S15, equity=p2["equity"]["net_equity"],
                                  peak=p2["equity"]["net_equity"], package_sha256="1" * 64)
    p3, f3 = package(future_head, S16, now, scope="record_only", prior_tx=p2["ledger"]["transactions"])
    p2["ledger"]["transactions"] = p3["ledger"]["transactions"]
    p2["ledger"]["coverage"] = p3["ledger"]["coverage"]
    for source in p2["sources"]:
        if source["role"].startswith("cash_history") or source["role"] == "balance_history":
            f2[source["file"]] = f3[source["file"]]
            source["sha256"] = sha256_hex(f2[source["file"]])
    p2["dashboard"].update(p3["dashboard"])
    return p1, h1, p2, f2, now


def test_sequential_catchup_keeps_full_inventory_and_advances_one_close_at_a_time():
    p1, h1, p2, f2, now = catchup()
    h2 = proposed_head(p2, calculate(p2, f2, h1, prev=p1, now=now))
    assert h2.session_id == S15
    p3, f3 = package(h2, S16, now, scope="record_only", prior_tx=p2["ledger"]["transactions"])
    h3 = proposed_head(p3, calculate(p3, f3, h2, prev=p2, now=now))
    assert h3.session_id == S16
    assert any(t["session_id"] == S16 for t in p3["ledger"]["transactions"])


@pytest.mark.parametrize("mutation", ["added_old", "removed", "changed", "relabeled"])
def test_catchup_cannot_hide_corrections_to_retained_or_settled_history(mutation):
    p1, h1, p2, f2, now = catchup()
    txs = p2["ledger"]["transactions"]
    if mutation == "added_old":
        txs.append({"id": "new-old-row", "sha256": "2" * 64, "session_id": S14})
    elif mutation == "removed":
        txs.pop(0)
    elif mutation == "changed":
        txs[0]["sha256"] = "3" * 64
    else:
        txs[0]["session_id"] = S15
    assert calculate(p2, f2, h1, prev=p1, now=now) == Refusal("history_changed", True)


def test_current_scope_rejects_future_inventory_even_when_previously_observed():
    p1, h1, p2, f2, now = catchup()
    p2["scope"] = "submit_account_close"
    assert calculate(p2, f2, h1, prev=p1, now=now) == Refusal("history_changed", True)


def test_legacy_package_shape_cannot_silently_claim_new_source_guarantees():
    head = initial_head()
    p, sources = package(head, S14, NOW14)
    p["schema"] = "account_close_package/v1"
    assert calculate(p, sources, head) == Refusal("package_schema")


def test_unknown_scope_cannot_bypass_scope_specific_invariants():
    head = initial_head()
    p, sources = package(head, S14, NOW14)
    p["scope"] = "typo"
    p["ledger"]["transactions"][0]["session_id"] = S16
    assert calculate(p, sources, head) == Refusal("scope_unknown")

@pytest.mark.parametrize("mutation", ["coherent_arithmetic", "inventory", "window_count", "balance_bytes"])
def test_bound_reports_are_authoritative(mutation):
    from test_account_close_assembler import synthetic, build, NOW, S11, S14
    cash, files, bal1, bal2 = synthetic()
    p, sources, _ = build(cash, files, bal1, bal2, operator_signed_utc=NOW)
    head = SimpleNamespace(session_id=S11, equity=str(bal1), peak=str(bal1), package_sha256="0" * 64)
    from test_account_close_assembler import predecessor_inventory
    baseline = predecessor_inventory()
    assert isinstance(calculate(p, sources, head, prev=baseline, now=NOW), ProposedClose)
    if mutation == "coherent_arithmetic":
        from decimal import Decimal
        p["ledger"]["gross_trade_pnl"] = str(Decimal(p["ledger"]["gross_trade_pnl"]) + 1)
        p["equity"]["net_equity"] = str(Decimal(p["equity"]["net_equity"]) + 1)
        p["dashboard"]["balance"] = p["equity"]["net_equity"]
    elif mutation == "inventory":
        p["ledger"]["transactions"][0]["sha256"] = "9" * 64
    elif mutation == "window_count":
        p["ledger"]["coverage"]["windows"][0]["rows"] += 1
    else:
        source = next(s for s in p["sources"] if s["role"] == "balance_history")
        sources[source["file"]] = sources[source["file"]].replace(b"100,022.40", b"100,023.40")
        source["sha256"] = sha256_hex(sources[source["file"]])
    assert isinstance(calculate(p, sources, head, prev=baseline, now=NOW), Refusal)


def test_historical_dashboard_must_reconcile_current_full_history():
    head = initial_head()
    p, sources = package(head, S14, NOW14, scope="record_only")
    p["dashboard"]["balance"] = "1"
    assert calculate(p, sources, head) == Refusal("dashboard_disagreement")


def test_publication_cannot_follow_supporting_captures():
    head = initial_head()
    p, sources = package(head, S14, NOW14)
    p["source_publication_utc"] = utc(NOW14 - timedelta(minutes=1))
    assert calculate(p, sources, head) == Refusal("chronology:publication_after_capture")


def test_out_of_order_and_history_refusals_require_halt():
    head = initial_head()
    p, sources = package(head, S16, NOW14 + timedelta(days=2))
    assert calculate(p, sources, head, now=NOW14 + timedelta(days=2)) == Refusal("out_of_order_settlement", True)
    p, sources = package(head, S14, NOW14)
    p["ledger"]["revisions"] = ["1"]
    assert calculate(p, sources, head) == Refusal("transaction_revision_detected", True)


@pytest.mark.parametrize("scope", ["record_only", "submit_account_close"])
def test_missing_predecessor_inventory_cannot_establish_baseline(scope):
    head = initial_head()
    p, sources = package(head, S14, NOW14, scope=scope)
    result = calculate_close(p, sources, policy=POLICY, head={**vars(head), "as_of_utc": utc(CALENDAR.schedule_for(head.session_id).closes_at)},
        previous_package=None, account=ACCOUNT, calendar_digest=CALENDAR.calendar_digest,
        policy_digest=POLICY_DIGEST, calendar=CALENDAR, scope=scope, now=NOW14)
    assert result == Refusal("predecessor_inventory_required")


def test_timezone_must_match_retained_predecessor():
    from account_close_test_support import b7_previous_package
    head = initial_head()
    p, sources = package(head, S14, NOW14)
    previous = b7_previous_package()
    previous["report_timezone"] = "America/Chicago"
    assert calculate(p, sources, head, prev=previous) == Refusal("report_timezone_changed", True)


def test_source_history_correction_cannot_hide_behind_unchanged_inventory_claims():
    import csv
    import io
    from decimal import Decimal
    from test_account_close_assembler import synthetic, build, NOW, S11, predecessor_inventory
    cash, files, bal1, bal2 = synthetic()
    p, sources, _ = build(cash, files, bal1, bal2, operator_signed_utc=NOW)
    head = SimpleNamespace(session_id=S11, equity=str(bal1), peak=str(bal1), package_sha256="0" * 64)
    baseline = predecessor_inventory()
    source = next(s for s in p["sources"] if s["role"] == "cash_history")
    reader = csv.DictReader(io.StringIO(sources[source["file"]].decode()))
    rows = list(reader)
    for row in rows:
        if row["Date"] == "2026-09-10":
            if row["Cash Change Type"].strip() == "Commission":
                row["Delta"] = "-2.00"
            if row["Cash Change Type"].strip() == "Trade Paired":
                row["Delta"] = "26.00"
            else:
                row["Amount"] = str(Decimal(row["Amount"].replace(",", "")) - 1)
    out = io.StringIO()
    writer = csv.DictWriter(out, reader.fieldnames)
    writer.writeheader()
    writer.writerows(rows)
    sources[source["file"]] = out.getvalue().encode()
    source["sha256"] = sha256_hex(sources[source["file"]])
    assert calculate(p, sources, head, prev=baseline, now=NOW) == Refusal("history_changed", True)


def test_cash_rows_must_lie_inside_the_signed_timestamp_span():
    from test_account_close_assembler import synthetic, build, NOW, S11, predecessor_inventory
    cash, files, bal1, bal2 = synthetic()
    p, sources, _ = build(cash, files, bal1, bal2, operator_signed_utc=NOW)
    head = SimpleNamespace(session_id=S11, equity=str(bal1), peak=str(bal1), package_sha256="0" * 64)
    source = dict(next(s for s in p["sources"] if s["role"] == "cash_history"))
    sources["partial.csv"] = sources[source["file"]]
    source.update(role="cash_history:partial", file="partial.csv")
    p["sources"].append(source)
    window = dict(p["ledger"]["coverage"]["windows"][-1])
    window.update(file="partial.csv", from_utc="2026-09-10T15:00:00Z")
    p["ledger"]["coverage"]["windows"].append(window)
    assert calculate(p, sources, head, prev=predecessor_inventory(), now=NOW) == Refusal("source_row_outside_coverage")
