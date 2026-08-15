"""Tests for ops/c1_rail/c1_rail_telemetry.py — c1 M1 monitoring spine.

Covers ADR docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md §4:
append-only JSONL, secret denylist, concurrent writes, startup validation,
reconcile verdicts, execution state store, operator notifier, assert_no_secrets.
"""
from __future__ import annotations

import json
import threading
from pathlib import Path

import pytest

from c1_rail_telemetry import (
    SCHEMA_VERSION,
    BrokerEvidence,
    EventLedger,
    ExecutionStateStore,
    FileAckNotifier,
    TelemetryError,
    TransportOutcome,
    _cli_reconcile,
    append_broker_evidence,
    assert_no_secrets,
    format_arming_deviation,
    iter_arming_deviations,
    make_request_received,
    make_transport_payload,
    new_event_id,
    reconcile_chain,
    reconcile_event,
    write_reconciliation,
)


# ── helpers ──────────────────────────────────────────────────────────────────

def _ledger(tmp_path: Path, name: str = "events.jsonl") -> EventLedger:
    return EventLedger(tmp_path / name)


def _append_decision(ledger: EventLedger, *, event_id: str, qty: int = 9,
                     signal_type: str = "entry") -> dict:
    return ledger.append(
        "decision",
        {"leg_id": "dj30_mym", "signal_type": signal_type, "qty_out": qty,
         "submit": True, "halt": False},
        event_id=event_id,
        order_id=f"dj30_mym-{signal_type}-1",
    )


def _append_transport(ledger: EventLedger, *, event_id: str,
                      state: str = "accepted", http_status: int = 200) -> dict:
    return ledger.append(
        "transport_result",
        make_transport_payload(
            TransportOutcome(state=state, http_status=http_status),
            dry_run=False,
            payload_sha256="abc123",
        ),
        event_id=event_id,
        order_id=f"dj30_mym-entry-1",
    )


# ── 1. append + seq monotonic + schema_version ───────────────────────────────

def test_append_request_decision_transport_seq_monotonic(tmp_path):
    ledger = _ledger(tmp_path)
    eid = new_event_id()

    req = ledger.append(
        "request_received",
        {
            "auth_ok": True,
            "body_category": "b1_json",
            "body_sha256": "deadbeef",
            "parsed": {"leg_id": "dj30_mym"},
        },
        event_id=eid,
    )
    dec = _append_decision(ledger, event_id=eid, qty=9)
    tr = _append_transport(ledger, event_id=eid)

    for rec in (req, dec, tr):
        assert rec["schema_version"] == SCHEMA_VERSION == 1
        assert rec["event_id"] == eid

    records = list(ledger.iter_records())
    assert [r["seq"] for r in records] == [1, 2, 3]
    assert all(r["schema_version"] == 1 for r in records)


# ── 2. secret denylist ───────────────────────────────────────────────────────

@pytest.mark.parametrize("bad_key", [
    "secret_key", "webhook_secret", "path_token", "bearer",
])
def test_append_rejects_secret_denylist_keys(tmp_path, bad_key):
    ledger = _ledger(tmp_path)
    with pytest.raises(TelemetryError, match="secret-denylist|release blocker"):
        ledger.append(
            "decision",
            {bad_key: "leaked-value", "qty_out": 9},
            event_id=new_event_id(),
        )


# ── 3. concurrent appends ────────────────────────────────────────────────────

def test_concurrent_appends_produce_valid_ordered_jsonl(tmp_path):
    ledger = _ledger(tmp_path)
    barrier = threading.Barrier(2)
    errors: list[Exception] = []

    def worker(prefix: str) -> None:
        try:
            barrier.wait(timeout=5)
            for i in range(20):
                eid = f"{prefix}-{i}"
                ledger.append(
                    "decision",
                    {"leg_id": f"{prefix}_leg", "signal_type": "entry",
                     "qty_out": i + 1},
                    event_id=eid,
                )
        except Exception as exc:  # noqa: BLE001 — collect for main-thread assert
            errors.append(exc)

    t_mym = threading.Thread(target=worker, args=("MYM",))
    t_mnq = threading.Thread(target=worker, args=("MNQ",))
    t_mym.start()
    t_mnq.start()
    t_mym.join(timeout=30)
    t_mnq.join(timeout=30)

    assert errors == []
    reloaded = EventLedger(ledger.path)
    assert reloaded.healthy
    assert not reloaded.risk_add_blocked
    records = list(reloaded.iter_records())
    assert len(records) == 40
    seqs = [r["seq"] for r in records]
    assert seqs == list(range(1, 41))


# ── 4. truncated / malformed tail ───────────────────────────────────────────

def test_malformed_json_tail_marks_ledger_unhealthy(tmp_path):
    path = tmp_path / "events.jsonl"
    path.write_text(
        '{"schema_version":1,"seq":1,"kind":"decision","event_id":"a"}\n'
        '{"truncated": true\n',
        encoding="utf-8",
    )
    ledger = EventLedger(path)
    assert not ledger.healthy
    assert ledger.risk_add_blocked is True
    assert "malformed JSONL" in (ledger.unhealthy_reason or "")


def test_non_monotonic_seq_marks_ledger_unhealthy(tmp_path):
    path = tmp_path / "events.jsonl"
    path.write_text(
        '{"schema_version":1,"seq":1,"kind":"decision","event_id":"a"}\n'
        '{"schema_version":1,"seq":1,"kind":"decision","event_id":"b"}\n',
        encoding="utf-8",
    )
    ledger = EventLedger(path)
    assert not ledger.healthy
    assert ledger.risk_add_blocked


# ── 5. reconcile_chain / reconcile_event verdicts ──────────────────────────

def test_reconcile_chain_ok():
    evidence = BrokerEvidence(
        event_id="e1",
        crosstrade_receive=True,
        crosstrade_validate=True,
        crosstrade_execute=True,
        fill_qty=9,
        position_after=9,
    )
    assert reconcile_chain(
        intended_qty=9, transport_state="accepted", evidence=evidence,
    ) == "CHAIN_OK"


def test_broker_evidence_s4_eq_fields_roundtrip():
    """S4 additive execution-quality fields survive to_dict/from_dict."""
    evidence = BrokerEvidence(
        event_id="e-eq",
        fill_qty=1,
        fill_price=21000.25,
        intended_price=21000.0,
        fill_slippage_pts=0.25,
        fill_latency_ms=120.0,
        commission_usd=0.91,
        signal_origin="python_daemon",
    )
    loaded = BrokerEvidence.from_dict(evidence.to_dict())
    assert loaded.intended_price == 21000.0
    assert loaded.fill_slippage_pts == 0.25
    assert loaded.signal_origin == "python_daemon"
    # Pre-S4 overlays (no EQ keys) still load
    legacy = BrokerEvidence.from_dict({"event_id": "e-legacy", "fill_qty": 2})
    assert legacy.fill_qty == 2
    assert legacy.intended_price is None


def test_reconcile_rail_only_no_evidence():
    assert reconcile_chain(
        intended_qty=9, transport_state="accepted", evidence=None,
    ) == "RAIL_ONLY"


def test_reconcile_rail_only_transport_no_fill():
    evidence = BrokerEvidence(
        event_id="e1",
        crosstrade_receive=True,
        crosstrade_validate=True,
        crosstrade_execute=True,
        fill_qty=None,
    )
    assert reconcile_chain(
        intended_qty=9, transport_state="accepted", evidence=evidence,
    ) == "RAIL_ONLY"


def test_reconcile_rejected_wrong_secret_shape():
    """B6 incident: HTTP 200 transport but CrossTrade validate=False."""
    evidence = BrokerEvidence(
        event_id="e1",
        crosstrade_receive=True,
        crosstrade_validate=False,
        crosstrade_execute=False,
        fill_qty=None,
    )
    assert reconcile_chain(
        intended_qty=9, transport_state="accepted", evidence=evidence,
    ) == "REJECTED"


def test_reconcile_qty_mismatch():
    evidence = BrokerEvidence(
        event_id="e1",
        crosstrade_receive=True,
        crosstrade_validate=True,
        crosstrade_execute=True,
        fill_qty=8,
    )
    assert reconcile_chain(
        intended_qty=9, transport_state="accepted", evidence=evidence,
    ) == "QTY_MISMATCH"


def test_reconcile_no_flat_confirm():
    evidence = BrokerEvidence(
        event_id="e1",
        crosstrade_receive=True,
        crosstrade_validate=True,
        crosstrade_execute=True,
        fill_qty=0,
        flat_confirmed=False,
        position_after=0,
    )
    assert reconcile_chain(
        intended_qty=None, transport_state="accepted", evidence=evidence,
        signal_type="exit",
    ) == "NO_FLAT_CONFIRM"


def test_reconcile_position_mismatch_on_flat():
    evidence = BrokerEvidence(
        event_id="e1",
        flat_confirmed=True,
        position_after=3,
    )
    assert reconcile_chain(
        intended_qty=None, transport_state="accepted", evidence=evidence,
        signal_type="exit",
    ) == "POSITION_MISMATCH"


def test_reconcile_event_joins_rail_and_evidence(tmp_path):
    ledger = _ledger(tmp_path)
    eid = new_event_id()
    _append_decision(ledger, event_id=eid, qty=9)
    _append_transport(ledger, event_id=eid)
    evidence = BrokerEvidence(
        event_id=eid,
        crosstrade_receive=True,
        crosstrade_validate=True,
        crosstrade_execute=True,
        fill_qty=9,
        position_after=9,
    )
    verdict = reconcile_event(ledger, event_id=eid, evidence=evidence)
    assert verdict == "CHAIN_OK"
    recs = [r for r in ledger.iter_records() if r.get("kind") == "reconciliation"]
    assert len(recs) == 1
    assert recs[0]["verdict"] == "CHAIN_OK"


# ── 6. ExecutionStateStore ───────────────────────────────────────────────────

def test_execution_state_store_round_trip(tmp_path):
    store = ExecutionStateStore(tmp_path / "exec_state.json")
    assert store.get_confirmed_base("Striker") is None

    store.set_confirmed_base("Striker", 9, event_id="e1", order_id="o1")
    assert store.get_confirmed_base("Striker") == 9

    store.clear_leg("Striker")
    assert store.get_confirmed_base("Striker") is None


def test_execution_state_store_load_into_hydrates_dict(tmp_path):
    store = ExecutionStateStore(tmp_path / "exec_state.json")
    store.set_confirmed_base("Striker", 9)
    store.set_confirmed_base("Striker NAS100", 7)

    open_legs: dict[str, int] = {}
    store.load_into(open_legs)
    assert open_legs == {"Striker": 9, "Striker NAS100": 7}


def test_execution_state_store_does_not_auto_seed_from_intended(tmp_path):
    """Intended entry qty must not seed the store — starts empty until set."""
    store = ExecutionStateStore(tmp_path / "exec_state.json")
    assert store.get_confirmed_base("Striker") is None
    # Only operator-attested set_confirmed_base populates the store.
    store.set_confirmed_base("Striker", 9)
    assert store.get_confirmed_base("Striker") == 9


# ── 7. FileAckNotifier ───────────────────────────────────────────────────────

def test_file_ack_notifier_notify_and_acknowledge(tmp_path):
    alert_path = tmp_path / "alerts.jsonl"
    ack_dir = tmp_path / "acks"
    notifier = FileAckNotifier(alert_path, ack_dir)
    alert_id = "alert-test-001"

    notifier.notify("WARNING", "transport_unknown", event_id=alert_id)
    assert alert_path.is_file()
    line = alert_path.read_text(encoding="utf-8").strip()
    record = json.loads(line)
    assert record["alert_id"] == alert_id
    assert record["level"] == "WARNING"
    assert not notifier.is_acknowledged(alert_id)

    ack_path = notifier.acknowledge(alert_id, operator="test-operator")
    assert ack_path.is_file()
    assert notifier.is_acknowledged(alert_id)


# ── 8. assert_no_secrets ─────────────────────────────────────────────────────

def test_assert_no_secrets_rejects_secret_shaped_string_values():
    with pytest.raises(TelemetryError, match="secret-shaped value"):
        assert_no_secrets({"note": "bearer: abc123token"})

    with pytest.raises(TelemetryError, match="secret-shaped value"):
        assert_no_secrets("password=supersecret")

    assert_no_secrets({"safe": "MYM entry qty=9"})


def test_write_reconciliation_appends_valid_record(tmp_path):
    ledger = _ledger(tmp_path)
    eid = new_event_id()
    rec = write_reconciliation(
        ledger, event_id=eid, order_id="o1", verdict="RAIL_ONLY",
        intended_qty=9, transport_state="accepted", signal_type="entry",
    )
    assert rec["verdict"] == "RAIL_ONLY"
    assert rec["schema_version"] == 1


def test_append_broker_evidence(tmp_path):
    ledger = _ledger(tmp_path)
    evidence = BrokerEvidence(
        event_id="e1", fill_qty=9,
        crosstrade_receive=True, crosstrade_validate=True,
    )
    rec = append_broker_evidence(ledger, evidence)
    assert rec["kind"] == "broker_evidence"
    assert rec["fill_qty"] == 9


# ── arming_deviation listing (Addendum 2026-07-31b read-back) ─────────────

def test_iter_arming_deviations_filters_other_kinds(tmp_path):
    ledger = _ledger(tmp_path)
    eid = new_event_id()
    _append_decision(ledger, event_id=eid, qty=8)
    ledger.append(
        "arming_deviation",
        {
            "gate": "M1",
            "gate_reason": "status is 'CODE_LANDED'",
            "operator_reason": "attended B7 Stage 2",
            "requested_hours": 4.0,
            "adr": "2026-07-22-c1-venue-native-monitoring-maturity.md",
            "addendum": "2026-07-31b",
        },
        event_id=new_event_id(),
    )
    ledger.append(
        "arming_deviation",
        {
            "gate": "M1",
            "gate_reason": "status is 'CODE_LANDED'",
            "operator_reason": "second attended deviation",
            "requested_hours": 2.0,
            "adr": "2026-07-22-c1-venue-native-monitoring-maturity.md",
            "addendum": "2026-07-31b",
        },
        event_id=new_event_id(),
    )
    devs = iter_arming_deviations(ledger)
    assert len(devs) == 2
    assert all(d["kind"] == "arming_deviation" for d in devs)
    assert devs[0]["operator_reason"] == "attended B7 Stage 2"
    assert "attended B7 Stage 2" in format_arming_deviation(devs[0])


def test_cli_deviations_lists_records_read_only(tmp_path, capsys):
    ledger = _ledger(tmp_path)
    ledger.append(
        "arming_deviation",
        {
            "gate": "M1",
            "gate_reason": "status is 'CODE_LANDED'",
            "operator_reason": "desk GO",
            "requested_hours": 1.0,
            "adr": "2026-07-22-c1-venue-native-monitoring-maturity.md",
            "addendum": "2026-07-31b",
        },
        event_id=new_event_id(),
    )
    after_write = ledger.path.read_text(encoding="utf-8")

    assert _cli_reconcile(["--events", str(ledger.path), "--deviations"]) == 0
    out = capsys.readouterr().out
    assert "arming_deviations: 1" in out
    assert "operator_reason='desk GO'" in out
    assert ledger.path.read_text(encoding="utf-8") == after_write, (
        "--deviations must not append to the ledger")


def test_cli_deviations_empty_ledger(tmp_path, capsys):
    ledger = _ledger(tmp_path)
    assert _cli_reconcile(["--events", str(ledger.path), "--deviations"]) == 0
    assert "arming_deviations: 0" in capsys.readouterr().out


def test_cli_deviations_rejects_event_id(tmp_path):
    ledger = _ledger(tmp_path)
    with pytest.raises(SystemExit, match="mutually exclusive"):
        _cli_reconcile(["--events", str(ledger.path), "--deviations",
                        "--event-id", "x"])


# ── request_received price fields vs secret scan (B7 prerequisite) ────────

def test_request_received_b1_price_fields_pass_secret_scan(tmp_path):
    """Realistic B1 parsed close/stop_dist_pts must append without TelemetryError."""
    from c1_rail_http_server import build_parsed_fields

    ledger = _ledger(tmp_path)
    eid = new_event_id()
    payload = {
        "leg_id": "dj30_mym",
        "signal_type": "add",
        "bar_time": "2026-07-24T14:00:00Z",
        "close": 52737.0,
        "stop_dist_pts": 80.0,
    }
    rec = ledger.append(
        "request_received",
        make_request_received(
            event_id=eid,
            auth_ok=True,
            body_category="b1_json",
            body_hash="abc123",
            order_id="dj30_mym-add-2026-07-24T14:00:00Z",
            parsed_fields=build_parsed_fields(payload, "add"),
        ),
        event_id=eid,
        order_id="dj30_mym-add-2026-07-24T14:00:00Z",
    )
    assert rec["parsed"]["close"] == 52737.0
    assert rec["parsed"]["stop_dist_pts"] == 80.0
    round_trip = list(ledger.iter_records())
    assert len(round_trip) == 1
    assert round_trip[0]["parsed"]["close"] == 52737.0
    assert round_trip[0]["parsed"]["stop_dist_pts"] == 80.0

