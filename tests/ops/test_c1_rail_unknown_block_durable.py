"""A transport_unknown risk-add block survives restart until operator resolution.

M1 ADR (docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md) §4 item 4
and acceptance item 8: an uncertain send blocks further risk-add and requires
broker reconciliation. The block used to live only in EventLedger memory, so a
listener restart re-opened risk-add with the unknown still unreconciled. These
tests pin the durable form: the block is re-derived from the JSONL stream and
lifts only on a recorded ``transport_unknown_resolution``.
"""
from __future__ import annotations

import pytest

from c1_rail_listener import handle_signal
from c1_rail_telemetry import (
    BrokerEvidence,
    EventLedger,
    TelemetryError,
    TransportOutcome,
    _cli_reconcile,
    append_broker_evidence,
    make_transport_payload,
)
from test_c1_rail_listener import (  # noqa: F401 — host is a fixture
    E_FIRM,
    _CapturingSender,
    _config,
    entry_payload,
    host,
)


def _timeout_sender(url, body, headers):
    raise TimeoutError("simulated timeout after bytes may have left")


def _send_unknown(host, path):
    ledger = EventLedger(path)
    result = handle_signal(entry_payload(), host, current_equity=E_FIRM,
                           config=_config(dry_run=False),
                           sender=_timeout_sender, ledger=ledger)
    assert result.transport_state == "unknown"
    return ledger, result.event_id


def _unknown(ledger, event_id, order_id="leg-entry-1"):
    ledger.append("transport_result", make_transport_payload(
        TransportOutcome(state="unknown", error="TimeoutError"), dry_run=False),
        event_id=event_id, order_id=order_id)


def _evidence(ledger, event_id):
    append_broker_evidence(ledger, BrokerEvidence(
        event_id=event_id, crosstrade_receive=False,
        notes="Alert History shows no receipt; Tradovate flat"))


# ── the defect: restart lifted the block ────────────────────────────────────

def test_restart_rederives_unknown_block_and_refuses_risk_add(host, tmp_path):
    path = tmp_path / "events.jsonl"
    _, eid = _send_unknown(host, path)

    restarted = EventLedger(path)  # new process: no in-memory state carried
    assert restarted.healthy
    assert restarted.risk_add_blocked
    assert eid in restarted.unresolved_unknowns
    assert "reconcile before retry" in (restarted.block_reason or "")

    sender = _CapturingSender()
    blocked = handle_signal(entry_payload(), host, current_equity=E_FIRM,
                            config=_config(dry_run=False), sender=sender,
                            ledger=restarted)
    assert blocked.decision.halt
    assert sender.calls == []


@pytest.mark.parametrize("signal_type", ["exit", "flat"])
def test_restart_block_still_relays_exit_and_flat(host, tmp_path, signal_type):
    path = tmp_path / "events.jsonl"
    _send_unknown(host, path)
    sender = _CapturingSender()
    payload = {**entry_payload(), "signal_type": signal_type}
    result = handle_signal(payload, host, current_equity=E_FIRM,
                           config=_config(dry_run=False), sender=sender,
                           ledger=EventLedger(path))
    assert result.sent is True
    assert len(sender.calls) == 1


class _DropTransportLedger(EventLedger):
    def append(self, kind, payload, *, event_id, order_id=None):
        if kind == "transport_result":
            raise TelemetryError("planted: transport record not persisted")
        return super().append(kind, payload, event_id=event_id,
                              order_id=order_id)


class _RecordingNotifier:
    def __init__(self):
        self.calls = []

    def notify(self, level, message, *, event_id=None, details=None):
        self.calls.append((level, message, dict(details or {})))


def test_unpersisted_unknown_falls_back_to_in_process_block(host, tmp_path):
    ledger = _DropTransportLedger(tmp_path / "events.jsonl")
    notifier = _RecordingNotifier()
    handle_signal(entry_payload(), host, current_equity=E_FIRM,
                  config=_config(dry_run=False), sender=_timeout_sender,
                  ledger=ledger, notifier=notifier)
    assert ledger.risk_add_blocked
    assert ledger.unresolved_unknowns == {}
    unknown_alert = [c for c in notifier.calls if "transport_unknown" in c[1]]
    assert unknown_alert[0][2]["block_durable"] is False


# ── resolution: recorded, evidenced, durable ────────────────────────────────

def test_resolution_requires_broker_evidence_then_lifts_durably(host, tmp_path):
    path = tmp_path / "events.jsonl"
    ledger, eid = _send_unknown(host, path)

    with pytest.raises(TelemetryError, match="broker_evidence"):
        ledger.resolve_transport_unknown(eid, resolved_by="operator",
                                         note="checked")
    assert EventLedger(path).risk_add_blocked

    _evidence(ledger, eid)
    ledger.resolve_transport_unknown(eid, resolved_by="operator",
                                     note="no receipt; flat")
    assert not ledger.risk_add_blocked

    restarted = EventLedger(path)
    assert restarted.healthy
    assert not restarted.risk_add_blocked
    assert restarted.unresolved_unknowns == {}
    sender = _CapturingSender()
    resumed = handle_signal({**entry_payload(), "bar_time": 1752779700000},
                            host, current_equity=E_FIRM,
                            config=_config(dry_run=False), sender=sender,
                            ledger=restarted)
    assert resumed.decision.halt is False
    assert len(sender.calls) == 1


def test_one_resolution_does_not_lift_another_unknown(tmp_path):
    ledger = EventLedger(tmp_path / "events.jsonl")
    _unknown(ledger, "a")
    _unknown(ledger, "b")
    _evidence(ledger, "a")
    ledger.resolve_transport_unknown("a", resolved_by="op", note="flat")
    assert ledger.risk_add_blocked
    assert list(EventLedger(ledger.path).unresolved_unknowns) == ["b"]


@pytest.mark.parametrize("event_id, resolved_by, note, match", [
    ("never-seen", "op", "x", "not an unresolved"),
    ("u", "", "x", "resolved_by"),
    ("u", "op", "  ", "note"),
])
def test_resolution_refusals_append_nothing(tmp_path, event_id, resolved_by,
                                            note, match):
    ledger = EventLedger(tmp_path / "events.jsonl")
    _unknown(ledger, "u")
    _evidence(ledger, "u")
    before = len(list(ledger.iter_records()))
    with pytest.raises(TelemetryError, match=match):
        ledger.resolve_transport_unknown(event_id, resolved_by=resolved_by,
                                         note=note)
    assert len(list(ledger.iter_records())) == before
    assert ledger.risk_add_blocked


def test_accepted_and_failed_sends_do_not_block(tmp_path):
    ledger = EventLedger(tmp_path / "events.jsonl")
    for eid, state in (("a", "accepted"), ("f", "failed"),
                       ("n", "not_attempted")):
        ledger.append("transport_result", make_transport_payload(
            TransportOutcome(state=state), dry_run=False), event_id=eid)
    assert not EventLedger(ledger.path).risk_add_blocked


def test_clear_risk_add_block_cannot_lift_a_durable_unknown(tmp_path):
    ledger = EventLedger(tmp_path / "events.jsonl")
    _unknown(ledger, "u")
    with pytest.raises(TelemetryError, match="resolve_transport_unknown"):
        ledger.clear_risk_add_block()
    assert ledger.risk_add_blocked

    # NEGATIVE CONTROL: the in-process-only block still clears as before.
    other = EventLedger(tmp_path / "other.jsonl")
    other.block_risk_add("manual")
    other.clear_risk_add_block()
    assert not other.risk_add_blocked


# ── a second process writing the same ledger ────────────────────────────────

def test_append_after_foreign_append_keeps_seq_monotonic(tmp_path):
    path = tmp_path / "events.jsonl"
    listener = EventLedger(path)
    listener.append("decision", {"qty_out": 1}, event_id="d1")
    arm_helper = EventLedger(path)  # c1_rail_arm.py runs as its own process
    arm_helper.append("arming_deviation", {"gate": "M1"}, event_id="dev")
    listener.append("decision", {"qty_out": 2}, event_id="d2")

    reloaded = EventLedger(path)
    assert reloaded.healthy
    assert [r["seq"] for r in reloaded.iter_records()] == [1, 2, 3]


def test_foreign_resolution_lifts_running_listener_block(tmp_path):
    path = tmp_path / "events.jsonl"
    listener = EventLedger(path)
    _unknown(listener, "u")
    _evidence(listener, "u")
    assert listener.risk_add_blocked

    EventLedger(path).resolve_transport_unknown("u", resolved_by="op",
                                                note="flat")
    assert not listener.risk_add_blocked
    listener.append("decision", {"qty_out": 1}, event_id="next")
    assert EventLedger(path).healthy


# ── CLI ─────────────────────────────────────────────────────────────────────

def test_cli_lists_and_resolves_unknown(tmp_path, capsys):
    path = tmp_path / "events.jsonl"
    ledger = EventLedger(path)
    _unknown(ledger, "u", order_id="dj30_mym-entry-1")

    assert _cli_reconcile(["--events", str(path), "--unresolved"]) == 0
    out = capsys.readouterr().out
    assert "unresolved_transport_unknown: 1" in out
    assert "event_id=u" in out

    with pytest.raises(SystemExit, match="broker_evidence"):
        _cli_reconcile(["--events", str(path), "--resolve-unknown",
                        "--event-id", "u", "--resolved-by", "op",
                        "--note", "flat"])
    _evidence(ledger, "u")
    assert _cli_reconcile(["--events", str(path), "--resolve-unknown",
                           "--event-id", "u", "--resolved-by", "op",
                           "--note", "flat"]) == 0
    assert "remaining=0" in capsys.readouterr().out
    resolution = [r for r in EventLedger(path).iter_records()
                  if r["kind"] == "transport_unknown_resolution"]
    assert len(resolution) == 1
    assert resolution[0]["order_id"] == "dj30_mym-entry-1"
    assert resolution[0]["resolved_by"] == "op"
