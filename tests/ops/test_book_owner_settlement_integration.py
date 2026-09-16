"""The repaired close verifier and runtime owner share one writer boundary."""
import json
from datetime import datetime, timezone

import pytest

from c1_rail.book_policy import candidate_book_protection_policy
from c1_rail.book_settlement import Receipt, Refusal, sha256_hex
from c1_rail.book_settlement import SettlementStore
from c1_rail.book_account_owner import AccountOwnerError, BookAccountOwner, SyntheticBroker
from test_book_account_owner import binding


KEY_ID = "1f75cea0c36941f8964d393490b6886bcbcdb010b4bc67dd45e925d1a04604aa"
TOOL = "7" * 64
SESSION = "tradeify-account-day:2026-09-11"
CLOSE = datetime(2026, 9, 11, 21, tzinfo=timezone.utc)
NOW = datetime(2026, 9, 12, 14, tzinfo=timezone.utc)


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


def test_revision_and_account_intervention_commit_before_failing_notification(tmp_path):
    owner, store = integrated(tmp_path)
    seal = seal_bytes()
    receipt = store.bootstrap_b7(
        seal, expected_seal_sha256=sha256_hex(seal), expected_tool_sha256=TOOL,
        session_id=SESSION, effective_close_utc=CLOSE,
        policy=candidate_book_protection_policy(), now=NOW,
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
