"""Pure close proposals: full package validation without a database or signing key."""
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest

from account_close_calculation import calculate_close, ProposedClose, Refusal, canonical_bytes
from account_close_evidence import sha256_hex
from account_close_test_support import ACCOUNT, CALENDAR, POLICY_DIGEST, package, utc
from book_policy import candidate_book_protection_policy
from c1_signal_daemon.book_protocol import Mode

POLICY = candidate_book_protection_policy()
S14, S15, S16 = (f"tradeify-account-day:2026-09-{d}" for d in (14, 15, 16))
NOW14 = datetime(2026, 9, 14, 21, 10, tzinfo=timezone.utc)


def initial_head():
    return SimpleNamespace(session_id="tradeify-account-day:2026-09-11", equity="100000", peak="100000",
                           package_sha256="0" * 64)


def calculate(p, sources, head, *, prev=None, now=NOW14):
    return calculate_close(p, sources, policy=POLICY, head={**vars(head),
        "as_of_utc": utc(CALENDAR.schedule_for(head.session_id).closes_at)},
        previous_package=prev, account=ACCOUNT, calendar_digest=CALENDAR.calendar_digest,
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
    # Fresh history includes an already-observed transaction from the next missed session.
    future = {"id": "future", "sha256": "1" * 64, "session_id": S16}
    p2["ledger"]["transactions"].append(future)
    return p1, h1, p2, f2, now


def test_sequential_catchup_keeps_full_inventory_and_advances_one_close_at_a_time():
    p1, h1, p2, f2, now = catchup()
    h2 = proposed_head(p2, calculate(p2, f2, h1, prev=p1, now=now))
    assert h2.session_id == S15
    p3, f3 = package(h2, S16, now, scope="record_only", prior_tx=p2["ledger"]["transactions"])
    h3 = proposed_head(p3, calculate(p3, f3, h2, prev=p2, now=now))
    assert h3.session_id == S16
    assert any(t["id"] == "future" for t in p3["ledger"]["transactions"])


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
    assert calculate(p2, f2, h1, prev=p1, now=now) == Refusal("history_changed")


def test_current_scope_rejects_future_inventory_even_when_previously_observed():
    p1, h1, p2, f2, now = catchup()
    p2["scope"] = "submit_account_close"
    assert calculate(p2, f2, h1, prev=p1, now=now) == Refusal("history_changed")


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
