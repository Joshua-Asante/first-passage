"""The repaired close verifier and runtime owner share one writer boundary."""
import json
import sqlite3
from dataclasses import replace
from datetime import datetime, timedelta, timezone

import pytest

from c1_rail.book_policy import candidate_book_protection_policy
from c1_rail.book_settlement import (
    Receipt, Refusal, SettlementError, canonical_bytes, sha256_hex,
)
from c1_rail.book_settlement import SettlementStore
from c1_rail.book_account_owner import (
    _SETTLEMENT_TABLES, AccountOwnerError, BookAccountOwner, BrokerResult,
    SyntheticBroker,
)
from c1_rail.c1_rail_listener import handle_book_action
from test_book_account_owner import binding as owner_binding, intent
from test_book_settlement import (
    CALENDAR, NOW14, Operator, S14, S15, b7_seal, package, seat,
)
from settlement_signing import signing_envelope


KEY_ID = "1f75cea0c36941f8964d393490b6886bcbcdb010b4bc67dd45e925d1a04604aa"
TOOL = "7" * 64
SESSION = "tradeify-account-day:2026-09-11"
CLOSE = datetime(2026, 9, 11, 21, tzinfo=timezone.utc)
NOW = datetime(2026, 9, 12, 14, tzinfo=timezone.utc)


def binding():
    result = owner_binding()
    result["session"] = replace(result["session"], calendar_digest=CALENDAR.calendar_digest)
    return result


def seal_bytes():
    document = {
        "values": {
            "balance": "100000", "equity": "100000", "trailing_threshold": "97000",
            "prior_trade_days": 3, "prior_max_day_profit": "0",
            "consistency_display_pct": "0", "profit_target_display": "6000",
            "cash_adjustments_total": "0", "token_trade_fill_dates": [],
            "positions_export_shows_flat": True, "working_orders_count": 0,
        },
        "derived": {
            "original_basis": "100000", "historical_eod_peak": "100000",
            "at_high_water_mark": True, "carried_drawdown": "0",
            "valid_until": "2026-09-13T18:00:00-04:00",
        },
        "evidence": {
            "E1": {"path": "dash.png", "sha256": "1" * 64,
                   "captured_at": "2026-09-12T09:00:00-04:00"},
            "E2": {"path": "pos.csv", "sha256": "2" * 64,
                   "captured_at": "2026-09-12T09:01:00-04:00"},
            "E3": {"path": "cash.csv", "sha256": "3" * 64,
                   "captured_at": "2026-09-12T09:02:00-04:00"},
        },
        "checks": {f"C{i}": "pass" for i in range(1, 11)},
        "seal_timestamp": "2026-09-12T10:00:00-04:00",
        "tool_sha256": TOOL,
        "contract": "docs/spec/2026-09-12-tradeify-account-snapshot-seal-contract.md",
    }
    return json.dumps(document).encode("utf-8")


def integrated(tmp_path):
    owner = BookAccountOwner.boot(tmp_path / "owner.sqlite", "synthetic-account",
                                  binding=binding(), synthetic_broker=SyntheticBroker([]))
    store = owner.open_settlement(
        trusted_keys={KEY_ID: ["submit_account_close", "record_only"]}, now=NOW)
    return owner, store


def test_shared_database_boot_does_not_arm_and_survives_owner_restart(tmp_path):
    owner, store = integrated(tmp_path)
    assert owner.permission == "HALTED"
    assert store.status()["rows"] == 0
    with pytest.raises(AccountOwnerError, match="settlement_unavailable"):
        owner.activate_synthetic(now=datetime(2026, 9, 15, 14, tzinfo=timezone.utc))
    assert owner.authority == "INTERVENTION"

    restarted = BookAccountOwner.boot(tmp_path / "owner.sqlite", "synthetic-account",
                                      binding=binding(), synthetic_broker=SyntheticBroker([]))
    restored_store = restarted.open_settlement(
        trusted_keys={KEY_ID: ["submit_account_close", "record_only"]}, now=NOW)
    assert restarted.permission == "HALTED"
    assert restored_store.status()["restore_pending"] is True


def test_lost_settlement_tables_cannot_repeat_first_owner_attachment(tmp_path):
    owner, store = integrated(tmp_path)
    receipt = store.bootstrap_b7(
        seal_bytes(), expected_seal_sha256=sha256_hex(seal_bytes()),
        expected_tool_sha256=TOOL, session_id=SESSION,
        effective_close_utc=CLOSE, policy=candidate_book_protection_policy(),
        now=NOW, calendar=CALENDAR,
    )
    assert isinstance(receipt, Receipt)
    with sqlite3.connect(owner.path) as db:
        for table in sorted(_SETTLEMENT_TABLES - {"sqlite_sequence"}):
            db.execute(f"DROP TABLE {table}")

    with pytest.raises((SettlementError, AccountOwnerError),
                       match="settlement (state unavailable|attachment/state mismatch)"):
        owner.open_settlement(trusted_keys={KEY_ID: ["submit_account_close"]}, now=NOW)


def test_restart_cannot_bypass_attached_settlement_verifier(tmp_path):
    owner, _store = integrated(tmp_path)
    restarted = BookAccountOwner.boot(
        owner.path, "synthetic-account", binding=binding(),
        synthetic_broker=SyntheticBroker([]),
    )

    with pytest.raises(AccountOwnerError, match="settlement_verifier_unavailable"):
        restarted.activate_synthetic(now=datetime(2026, 9, 15, 14, tzinfo=timezone.utc))

    assert restarted.permission == "HALTED"
    assert restarted.authority == "INTERVENTION"


def test_missing_attachment_record_is_not_never_attached(tmp_path):
    owner, _store = integrated(tmp_path)
    with sqlite3.connect(owner.path) as db:
        db.execute("DELETE FROM settlement_attachment")

    with pytest.raises(AccountOwnerError, match="attachment authority unavailable"):
        BookAccountOwner.boot(
            owner.path, "synthetic-account", binding=binding(),
            synthetic_broker=SyntheticBroker([]),
        )


@pytest.mark.parametrize("status", ["NEVER_ATTACHED", "ATTACHED"])
def test_attachment_state_must_match_settlement_tables(tmp_path, status):
    owner = BookAccountOwner.boot(
        tmp_path / "owner.sqlite", "synthetic-account", binding=binding(),
        synthetic_broker=SyntheticBroker([]),
    )
    if status == "ATTACHED":
        body = json.dumps(
            {"account": "synthetic-account", "status": status,
             "attached_utc": NOW.isoformat()},
            sort_keys=True, separators=(",", ":"))
    else:
        owner.open_settlement(
            trusted_keys={KEY_ID: ["submit_account_close"]}, now=NOW)
        body = json.dumps(
            {"account": "synthetic-account", "status": status},
            sort_keys=True, separators=(",", ":"))
    with sqlite3.connect(owner.path) as db:
        db.execute(
            "UPDATE settlement_attachment SET body=?, digest=? WHERE singleton=1",
            (body, sha256_hex(body.encode())),
        )

    with pytest.raises(AccountOwnerError, match="attachment/state mismatch"):
        BookAccountOwner.boot(
            owner.path, "synthetic-account", binding=binding(),
            synthetic_broker=SyntheticBroker([]),
        )


def test_attachment_corruption_after_boot_blocks_activation(tmp_path):
    owner, _store = integrated(tmp_path)
    with sqlite3.connect(owner.path) as db:
        db.execute("UPDATE settlement_attachment SET digest='broken'")

    with pytest.raises(AccountOwnerError, match="attachment integrity failure"):
        owner.activate_synthetic(now=datetime(2026, 9, 15, 14, tzinfo=timezone.utc))


def test_signed_synthetic_close_flows_through_unified_owner_into_listener_sizing(tmp_path):
    operator = Operator()
    initial = binding()
    initial_session = replace(
        initial["session"], session_id=S14, prior_session_id=SESSION,
        calendar_digest=CALENDAR.calendar_digest,
        opens_at=initial["session"].opens_at - timedelta(days=1),
        risk_add_cutoff=initial["session"].risk_add_cutoff - timedelta(days=1),
        flatten_start=initial["session"].flatten_start - timedelta(days=1),
        own_flat_deadline=initial["session"].own_flat_deadline - timedelta(days=1),
        closes_at=initial["session"].closes_at - timedelta(days=1),
    )
    initial["session"] = initial_session
    initial["policy_digest"] = "b" * 64
    initial["settlement"] = replace(
        initial["settlement"], session_id=SESSION, as_of=CLOSE,
        equity=100_000.0, peak=100_000.0,
    )
    initial["as_of"] -= timedelta(days=1)
    initial["valid_until"] -= timedelta(days=1)
    owner = BookAccountOwner.boot(
        tmp_path / "owner.sqlite", "synthetic-account", binding=initial,
        synthetic_broker=SyntheticBroker([]),
    )
    store = owner.open_settlement(
        trusted_keys={operator.key_id: ["submit_account_close", "record_only"]},
        now=NOW,
    )
    head = seat(store, b7_seal())
    proposed, sources = package(head, S14, NOW14)
    raw = owner.issue_settlement_challenge(
        scope="submit_account_close", target_session_id=S15,
        proposed_session_id=S14,
        package_sha256=sha256_hex(canonical_bytes(proposed)),
        calendar=CALENDAR, now=NOW14,
    )
    envelope = signing_envelope(raw, signed_at=NOW14)
    receipt = owner.submit_settlement(
        envelope=envelope, signature=operator.sign(envelope), key_id=operator.key_id,
        package=proposed, sources=sources, calendar=CALENDAR, now=NOW14,
    )
    assert isinstance(receipt, Receipt) and receipt.grants_activation is False
    settled, _mode = store.settled_close()

    next_binding = binding()
    next_binding["session"] = replace(
        next_binding["session"], calendar_digest=CALENDAR.calendar_digest)
    next_binding["policy_digest"] = "b" * 64
    next_binding["settlement"] = settled
    next_owner = BookAccountOwner.boot(
        owner.path, "synthetic-account", binding=next_binding,
        synthetic_broker=SyntheticBroker([BrokerResult("accepted")]),
    )
    next_store = next_owner.open_settlement(
        trusted_keys={operator.key_id: ["submit_account_close", "record_only"]},
        now=datetime(2026, 9, 15, 13, 59, tzinfo=timezone.utc),
    )
    next_store.reconcile_restore(datetime(2026, 9, 15, 13, 59, 1, tzinfo=timezone.utc))
    at = datetime(2026, 9, 15, 14, tzinfo=timezone.utc)
    with pytest.raises(AccountOwnerError, match='entitlement'):
        next_owner.activate_synthetic(now=at)
    # Preserve settled-close sizing coverage independently from send authority.
    from c1_rail.book_sizing_context import size_book_request
    with next_owner._transaction() as db:
        request, context, sizing_binding = next_owner._context(db, intent(), at)
    decision = size_book_request(request, context=context, binding=sizing_binding,
                                policy=next_binding['policy'], now=at)
    assert decision.qty_out == 8

    result = handle_book_action(intent(), next_owner, occurrence=next_owner.make_occurrence("direct", "test_book_owner_settlement_integration:236"), now=datetime(2026, 9, 15, 14, tzinfo=timezone.utc))

    assert result.refusal_reason is not None
    assert result.transport_state == "not_attempted"
    assert next_owner.permission == 'HALTED'
    assert next_owner.synthetic_broker.commands == []


def test_revision_and_account_intervention_commit_before_failing_notification(tmp_path):
    owner, store = integrated(tmp_path)
    seal = seal_bytes()
    receipt = store.bootstrap_b7(
        seal, expected_seal_sha256=sha256_hex(seal), expected_tool_sha256=TOOL,
        session_id=SESSION, effective_close_utc=CLOSE,
        policy=candidate_book_protection_policy(), now=NOW, calendar=CALENDAR,
    )
    assert isinstance(receipt, Receipt)
    evidence = b"synthetic corrected observation"
    revised = {
        "account_id": "synthetic-account", "session_id": SESSION,
        "sources": [{"file": "corrected.txt", "sha256": sha256_hex(evidence),
                     "account_id": "synthetic-account"}],
    }

    def failed_notification(_reason, _domain):
        raise RuntimeError("simulated notifier failure")

    with pytest.raises(RuntimeError, match="notifier"):
        owner.record_settlement_revision(
            session_id=SESSION, revised_package=revised,
            sources={"corrected.txt": evidence}, now=NOW,
            on_halt=failed_notification)

    assert owner.permission == "HALTED"
    assert owner.authority == "INTERVENTION"
    assert owner.incidents[-1]["reason"] == "protection"
    assert store.status()["invalidated"] is True
    assert store.settled_close() == Refusal("chain_invalidated")


def test_settlement_boot_rechecks_owner_actor_after_boot_id_capture(tmp_path, monkeypatch):
    path = tmp_path / "owner.sqlite"
    stale = BookAccountOwner.boot(
        path, "synthetic-account", binding=binding(),
        synthetic_broker=SyntheticBroker([]))
    original_boot = SettlementStore.boot

    def racing_boot(*args, **kwargs):
        BookAccountOwner.boot(
            path, "synthetic-account", binding=binding(),
            synthetic_broker=SyntheticBroker([]))
        return original_boot(*args, **kwargs)

    monkeypatch.setattr(SettlementStore, "boot", racing_boot)
    with pytest.raises(AccountOwnerError, match="stale account owner boot"):
        stale.open_settlement(
            trusted_keys={KEY_ID: ["submit_account_close", "record_only"]}, now=NOW)

@pytest.mark.parametrize('key_id', [[], {}])
def test_malformed_signing_key_is_a_refusal_not_owner_storage_failure(tmp_path, key_id):
    operator = Operator()
    account = BookAccountOwner.boot(tmp_path/'owner.sqlite', 'synthetic-account', binding=binding())
    store = account.open_settlement(trusted_keys={operator.key_id: ['submit_account_close', 'record_only']}, now=NOW)
    head = seat(store, b7_seal())
    proposed, sources = package(head, S14, NOW14)
    raw = account.issue_settlement_challenge(scope='submit_account_close', target_session_id=S15,
        proposed_session_id=S14, package_sha256=sha256_hex(canonical_bytes(proposed)), calendar=CALENDAR, now=NOW14)
    envelope = signing_envelope(raw, signed_at=NOW14)
    before = account.path.read_bytes()
    result = account.submit_settlement(envelope=envelope, signature=operator.sign(envelope), key_id=key_id,
        package=proposed, sources=sources, calendar=CALENDAR, now=NOW14)
    assert result == Refusal('unknown_key_or_scope')
    assert account.path.read_bytes() == before
