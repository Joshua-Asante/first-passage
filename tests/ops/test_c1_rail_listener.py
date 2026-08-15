"""Tests for ops/c1_rail/c1_rail_listener.py — the Option C listener that ties the
sizing host to a live CrossTrade order (docs/spec/c1_nt8_sizing_host_impl.md
§2.4 addendum, resolved 2026-07-18).

This is the pure decision-routing function only: given an incoming B1 alert
payload, run it through C1SizingHostReference, and — unless halted, floored,
or in DRY_RUN — build and send a CrossTrade order via the injected `sender`.
The actual HTTP-server socket wiring (TV -> this process) is a thin,
separately-owned adapter around this function and is not exercised here,
matching the pattern already used for ops/cli.py's own entrypoint.

Safety invariants under test (spec §5/§6, carried over unchanged from the
NT8-hosted design — Option C changes the transport, never the fail-safe):
  - halt          -> sender NEVER called, regardless of dry_run
  - floored (qty 0, not a halt) -> sender NEVER called
  - dry_run=True  -> sender NEVER called, decision still computed + returned
  - dry_run defaults to True unless explicitly disabled
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

import pytest

from c1_rail_listener import arming_expiry_reason, handle_signal
from c1_rail_telemetry import EventLedger, TelemetryError
from c1_sizing_host_reference import C1SizingHostReference, generate_constants

TIER = "Tradeify_Select_100K"
E_FIRM = 100_000.0


def _write_json(path, obj):
    path.write_text(json.dumps(obj), encoding="utf-8")
    return path


@pytest.fixture
def host(tmp_path):
    _write_json(tmp_path / "lifecycle_state.json",
                {"Striker": "WATCH-1", "Striker NAS100": "WATCH-1"})
    _write_json(tmp_path / "c1_dd_state.json",
                {"account": TIER, "peak_equity": E_FIRM,
                 "last_updated_utc": "2026-07-18T00:00:00Z"})
    _write_json(tmp_path / "c1_sizing_constants.json", generate_constants(TIER))
    return C1SizingHostReference(
        lifecycle_state_path=tmp_path / "lifecycle_state.json",
        dd_state_path=tmp_path / "c1_dd_state.json",
        constants_path=tmp_path / "c1_sizing_constants.json",
    )


def entry_payload(leg_id="dj30_mym", stop_dist_pts=60.8201):
    return {"leg_id": leg_id, "signal_type": "entry", "bar_time": 1752778800000,
            "close": 44100.0, "stop_dist_pts": stop_dist_pts}


class _CapturingSender:
    def __init__(self, status=200):
        self.calls = []
        self._status = status

    def __call__(self, url, body, headers):
        self.calls.append({"url": url, "body": body, "headers": headers})
        return self._status


def _armed_until(hours=1.0):
    """A still-open arming deadline, computed rather than hardcoded.

    A literal date here would be a time bomb: the suite would pass until that
    date and then fail everywhere for a reason unrelated to the code.
    """
    return (datetime.now(timezone.utc) + timedelta(hours=hours)).isoformat()


def _config(**overrides):
    # dry_run=False + a live armed_until == a correctly-armed rail, which is
    # what these tests are about. Arming expiry is exercised deliberately in
    # the arming-window section below, never incidentally here.
    cfg = dict(account="TDFYSL100642026", secret_key="test-secret",
               webhook_id="abc123", webhook_secret="xyz789",
               destination="tradovate", dry_run=False,
               armed_until=_armed_until())
    cfg.update(overrides)
    return cfg


# ── the happy path ────────────────────────────────────────────────────────

def test_entry_signal_submits_when_not_halted(host):
    sender = _CapturingSender()
    result = handle_signal(entry_payload(), host, current_equity=E_FIRM,
                           config=_config(), sender=sender)
    assert not result.decision.halt
    assert result.decision.qty_out == 8
    assert result.sent is True
    assert result.http_status == 200
    assert len(sender.calls) == 1
    assert "MYM" in sender.calls[0]["body"] or "instrument=" in sender.calls[0]["body"]
    assert "qty=8;" in sender.calls[0]["body"]
    assert "destination=tradovate;" in sender.calls[0]["body"]


def test_add_signal_after_entry_submits_correct_qty(host):
    sender = _CapturingSender()
    entry_result = handle_signal(entry_payload(), host, current_equity=E_FIRM,
                                 config=_config(), sender=sender)
    host.confirm_executed_base("Striker", entry_result.decision.qty_out)
    add_payload = {"leg_id": "dj30_mym", "signal_type": "add", "bar_time": 2,
                   "close": 44200.0, "stop_dist_pts": 60.8201}
    result = handle_signal(add_payload, host, current_equity=E_FIRM,
                           config=_config(), sender=sender)
    assert result.decision.qty_out == 60
    assert result.sent is True
    assert result.transport_state == "accepted"
    assert "qty=60;" in sender.calls[-1]["body"]
    assert "flatten_first" not in sender.calls[-1]["body"]


def test_exit_signal_sends_closeposition_without_quantity(host):
    sender = _CapturingSender()
    handle_signal(entry_payload(), host, current_equity=E_FIRM,
                  config=_config(), sender=sender)
    exit_payload = {"leg_id": "dj30_mym", "signal_type": "exit", "bar_time": 3,
                    "close": 44050.0, "stop_dist_pts": 60.8201}
    result = handle_signal(exit_payload, host, current_equity=E_FIRM,
                           config=_config(), sender=sender)
    assert result.sent is True
    body = sender.calls[-1]["body"]
    assert "command=closeposition;" in body
    assert "quantity=" not in body


# ── safety invariants: sender must NEVER fire on these paths ───────────────

def test_halted_signal_never_calls_sender_even_when_not_dry_run(host, tmp_path):
    (tmp_path / "lifecycle_state.json").unlink()
    sender = _CapturingSender()
    result = handle_signal(entry_payload(), host, current_equity=E_FIRM,
                           config=_config(dry_run=False), sender=sender)
    assert result.decision.halt
    assert result.sent is False
    assert sender.calls == []


def test_floored_zero_qty_never_calls_sender(host, tmp_path):
    _write_json(tmp_path / "lifecycle_state.json",
                {"Striker": "RETIRED", "Striker NAS100": "WATCH-1"})
    sender = _CapturingSender()
    result = handle_signal(entry_payload(), host, current_equity=E_FIRM,
                           config=_config(dry_run=False), sender=sender)
    assert not result.decision.halt
    assert result.decision.qty_out == 0
    assert result.sent is False
    assert sender.calls == []


def test_dry_run_computes_but_never_calls_sender(host):
    sender = _CapturingSender()
    result = handle_signal(entry_payload(), host, current_equity=E_FIRM,
                           config=_config(dry_run=True), sender=sender)
    assert not result.decision.halt
    assert result.decision.qty_out == 8  # decision still computed
    assert result.sent is False
    assert result.dry_run is True
    assert sender.calls == []
    # the payload that WOULD have been sent is still surfaced for audit review
    assert result.payload_text is not None
    assert "qty=8;" in result.payload_text


def test_dry_run_defaults_true_when_key_absent(host):
    """Safety default: omitting dry_run from config must NOT fail open to live."""
    sender = _CapturingSender()
    cfg = _config()
    del cfg["dry_run"]
    result = handle_signal(entry_payload(), host, current_equity=E_FIRM,
                           config=cfg, sender=sender)
    assert result.dry_run is True
    assert result.sent is False
    assert sender.calls == []


def test_unknown_leg_id_halts_and_never_calls_sender(host):
    sender = _CapturingSender()
    result = handle_signal(entry_payload(leg_id="guardian_mgc"), host,
                           current_equity=E_FIRM, config=_config(dry_run=False),
                           sender=sender)
    assert result.decision.halt
    assert sender.calls == []


# ── non-200 from CrossTrade surfaces, doesn't silently succeed ─────────────

def test_non_200_from_crosstrade_surfaces_in_result(host):
    sender = _CapturingSender(status=500)
    result = handle_signal(entry_payload(), host, current_equity=E_FIRM,
                           config=_config(dry_run=False), sender=sender)
    assert result.sent is True  # HTTP response received = accepted transport
    assert result.http_status == 500
    assert result.transport_state == "accepted"


def test_transport_unknown_blocks_risk_add(host, tmp_path):
    def timeout_sender(url, body, headers):
        raise TimeoutError("simulated timeout after bytes may have left")

    ledger = EventLedger(tmp_path / "events.jsonl")
    result = handle_signal(
        entry_payload(), host, current_equity=E_FIRM,
        config=_config(dry_run=False), sender=timeout_sender, ledger=ledger,
    )
    assert result.sent is False
    assert result.transport_state == "unknown"
    assert ledger.risk_add_blocked

    blocked = handle_signal(
        entry_payload(), host, current_equity=E_FIRM,
        config=_config(dry_run=False), sender=_CapturingSender(), ledger=ledger,
    )
    assert blocked.decision.halt
    assert blocked.sent is False
    assert "reconcile before retry" in (blocked.decision.halt_reason or "").lower()


class _FailingDecisionLedger(EventLedger):
    """Test double: fail decision append for risk-add pre-send persistence."""

    def append(self, kind, payload, *, event_id, order_id=None):
        if kind == "decision":
            raise TelemetryError("simulated pre-send decision write failure")
        return super().append(kind, payload, event_id=event_id, order_id=order_id)


def test_pre_send_telemetry_failure_halts_entry(host, tmp_path):
    ledger = _FailingDecisionLedger(tmp_path / "events.jsonl")
    sender = _CapturingSender()
    result = handle_signal(
        entry_payload(), host, current_equity=E_FIRM,
        config=_config(dry_run=False), sender=sender, ledger=ledger,
    )
    assert result.decision.halt
    assert "telemetry pre-send persist failed" in (result.decision.halt_reason or "")
    assert result.sent is False
    assert result.transport_state == "not_attempted"
    assert sender.calls == []


# ── arming expiry (2026-07-27 forgotten-disarm failure class) ─────────────
#
# Arming carries an absolute wall-clock deadline. Once it lapses the rail must
# stop opening risk WITHOUT losing its ability to close risk — the same
# asymmetry the exit_on_equity_failure drill enforces for state faults.


def _expired_config(**overrides):
    return _config(armed_until=_armed_until(hours=-1), **overrides)


def test_expired_arming_blocks_entry(host):
    sender = _CapturingSender()
    result = handle_signal(entry_payload(), host, current_equity=E_FIRM,
                           config=_expired_config(), sender=sender)
    assert result.decision.halt is True
    assert "arming expired at" in (result.decision.halt_reason or "")
    assert result.sent is False
    assert result.transport_state == "not_attempted"
    assert sender.calls == []


def test_expired_arming_blocks_add(host):
    """The add leg carries the pyramid — it must be blocked too."""
    sender = _CapturingSender()
    add = {"leg_id": "dj30_mym", "signal_type": "add", "bar_time": 2,
           "close": 44200.0, "stop_dist_pts": 60.8201}
    result = handle_signal(add, host, current_equity=E_FIRM,
                           config=_expired_config(), sender=sender)
    assert result.decision.halt is True
    assert "arming expired" in (result.decision.halt_reason or "")
    assert sender.calls == []


@pytest.mark.parametrize("signal_type", ["exit", "flat"])
def test_expired_arming_still_relays_exit_and_flat(host, signal_type):
    """LOAD-BEARING. If expiry blocked flats, a window lapsing mid-position
    would strand an open position with no way to close it — turning a safety
    feature into the more dangerous state. Risk-reduction must always relay."""
    sender = _CapturingSender()
    handle_signal(entry_payload(), host, current_equity=E_FIRM,
                  config=_config(), sender=sender)          # open while valid
    sender.calls.clear()

    closing = {"leg_id": "dj30_mym", "signal_type": signal_type, "bar_time": 3,
               "close": 44300.0, "stop_dist_pts": 60.8201}
    result = handle_signal(closing, host, current_equity=E_FIRM,
                           config=_expired_config(), sender=sender)

    assert result.decision.halt is False
    assert result.sent is True
    assert len(sender.calls) == 1
    assert "closeposition" in sender.calls[0]["body"]
    assert "quantity=" not in sender.calls[0]["body"]


def test_valid_arming_window_still_sends(host):
    """Positive control — the gate must not block a correctly-armed rail."""
    sender = _CapturingSender()
    result = handle_signal(entry_payload(), host, current_equity=E_FIRM,
                           config=_config(), sender=sender)
    assert result.decision.halt is False
    assert result.decision.qty_out == 8
    assert result.sent is True
    assert len(sender.calls) == 1


def test_disarmed_rail_unaffected_by_expired_window(host):
    """dry_run=True short-circuits first: no send, and no arming-expiry halt
    (a disarmed rail isn't 'expired', it's simply off)."""
    sender = _CapturingSender()
    result = handle_signal(entry_payload(), host, current_equity=E_FIRM,
                           config=_expired_config(dry_run=True), sender=sender)
    assert result.sent is False
    assert result.dry_run is True
    assert result.decision.halt is False
    assert "arming expired" not in (result.decision.halt_reason or "")
    assert sender.calls == []


@pytest.mark.parametrize("bad,expect", [
    (None, "armed_until absent"),
    (12345, "must be an ISO-8601 string"),
    ("not-a-date", "unparseable"),
    ("2099-01-01T00:00:00", "no timezone"),
])
def test_arming_expiry_fails_safe_on_bad_values(host, bad, expect):
    """Every malformed value reads as EXPIRED, never as 'armed'."""
    sender = _CapturingSender()
    cfg = _config(armed_until=bad)
    result = handle_signal(entry_payload(), host, current_equity=E_FIRM,
                           config=cfg, sender=sender)
    assert result.decision.halt is True
    assert expect in (result.decision.halt_reason or "")
    assert sender.calls == []


def test_arming_expiry_reason_returns_none_only_when_open():
    """Direct unit coverage of the predicate, including the boundary."""
    assert arming_expiry_reason({"armed_until": _armed_until(hours=1)}) is None
    assert arming_expiry_reason({"armed_until": _armed_until(hours=-1)}) is not None
    # Deadline exactly now counts as expired (>= comparison, not >).
    now = datetime.now(timezone.utc).isoformat()
    assert arming_expiry_reason({"armed_until": now}) is not None


def test_arming_expiry_reason_clock_injection_is_opt_in_and_not_config_driven():
    """`now` is a keyword arg, never a config key.

    The boot gate and the per-request risk-add gate pass nothing and must keep
    reading real time. A clock reachable from the config body would be a
    fail-open: the untrusted half of the system could vote itself a window.
    """
    past = _armed_until(hours=-1)
    assert arming_expiry_reason({"armed_until": past}) is not None
    # A config carrying its own `now` must not be mistaken for the injected one.
    assert arming_expiry_reason(
        {"armed_until": past, "now": _armed_until(hours=+1)}) is not None
    # Injection is honoured only through the keyword.
    before = datetime.fromisoformat(past) - timedelta(hours=1)
    assert arming_expiry_reason({"armed_until": past}, now=before) is None
