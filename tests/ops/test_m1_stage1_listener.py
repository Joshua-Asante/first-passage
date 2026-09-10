"""M1 test identity: real sizing and routing, external sender replaced only."""
import json
import math

import pytest

import c1_rail_listener as listener
from c1_rail_telemetry import EventLedger, TelemetryError
from c1_sizing_host_reference import C1SizingHostReference, generate_constants

LEG = "m1_stage1_test"
KEY = "M1 Stage1 Test"


def payload(**overrides):
    return {"leg_id": LEG, "signal_type": "entry", "bar_time": "m1-stage1:offline",
            "close": 44000.0, "stop_dist_pts": 1.0, **overrides}


def write(path, data):
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


@pytest.fixture
def host(tmp_path):
    constants = generate_constants("Tradeify_Select_100K")
    constants["leg_map"][LEG] = {
        "leg_key": KEY, "base_risk": .0000125, "pyr_pct": 0.,
        "dollars_per_pt": .5, "cap_alloc": 1,
    }
    return C1SizingHostReference(
        write(tmp_path / "lifecycle.json", {KEY: "AUTHORIZED"}),
        write(tmp_path / "dd.json", {"peak_equity": 100000.}),
        write(tmp_path / "constants.json", constants),
    )


def forbidden(*args, **kwargs):
    pytest.fail("forbidden payload/sender/host path reached")


@pytest.mark.parametrize("equity,scale,raw", [(100000., 1., 2), (98000., .4, 1)])
def test_real_host_and_dry_run_one_micro(host, tmp_path, equity, scale, raw):
    ledger = EventLedger(tmp_path / "events.jsonl")
    result = listener.handle_signal(payload(), host, equity,
        config={"dry_run": True, "account": "OFFLINE", "secret_key": "offline"},
        sender=forbidden, ledger=ledger)
    assert not result.decision.halt
    assert (result.decision.qty_out, result.decision.qty_base_raw) == (1, raw)
    assert result.decision.dd_scale == scale
    assert not result.sent and result.dry_run is True
    assert result.transport_state == "not_attempted"
    assert "instrument=MYM1!;" in result.payload_text
    records = list(ledger.iter_records())
    decision = next(r for r in records if r["kind"] == "decision")
    assert decision["qty_out"] == 1 and decision["dry_run"] is True
    assert decision["sender_invoked"] is False
    assert decision["test_only"] is True
    assert all(r["event_id"] == result.event_id for r in records)
    assert host.open_leg_state == {}


@pytest.mark.parametrize("mode", [False, None, 0, 1, "true", "false", "absent"])
@pytest.mark.parametrize("kind", ["entry", "add", "exit", "flat"])
def test_guard_precedes_host_and_payload_even_with_valid_state(host, tmp_path, monkeypatch, mode, kind):
    monkeypatch.setattr(host, "process_signal", forbidden)
    monkeypatch.setattr(listener, "build_crosstrade_payload", forbidden)
    cfg = {"dry_run": mode, "armed_until": "2099-01-01T00:00:00+00:00"}
    if mode == "absent":
        cfg.pop("dry_run")
    ledger = EventLedger(tmp_path / "events.jsonl")
    result = listener.handle_signal(payload(signal_type=kind), host, 100000.,
                                    config=cfg, sender=forbidden, ledger=ledger)
    assert result.decision.halt_reason == "m1_test_requires_explicit_dry_run"
    assert result.decision.qty_out == 0 and not result.sent
    assert result.payload_text is None
    assert list(ledger.iter_records())[0]["halt_reason"] == result.decision.halt_reason


@pytest.mark.parametrize("kind", ["add", "exit", "flat"])
def test_test_identity_has_no_close_or_add_path(host, kind):
    result = listener.handle_signal(payload(signal_type=kind), host, 100000.,
                                    config={"dry_run": True}, sender=forbidden)
    assert result.decision.halt_reason == "m1_test_entry_only"
    assert host.process_signal(payload(signal_type=kind), 100000.).halt


def test_ledger_failure_cannot_bypass_live_prohibition(host, tmp_path, monkeypatch):
    ledger = EventLedger(tmp_path / "events.jsonl")
    def broken(*a, **k):
        raise TelemetryError("offline write failure")
    monkeypatch.setattr(ledger, "append", broken)
    result = listener.handle_signal(payload(), host, 100000., config={"dry_run": False},
                                    sender=forbidden, ledger=ledger)
    assert not result.sent and result.decision.halt


def test_mode_is_sampled_once_for_guard_and_transport(host):
    class ChangingConfig(dict):
        def get(self, key, default=None):
            value = super().get(key, default)
            if key == "dry_run":
                self[key] = True
            return value
    result = listener.handle_signal(payload(), host, 100000.,
        config=ChangingConfig(dry_run=False, armed_until="2099-01-01T00:00:00+00:00",
                              account="OFFLINE", secret_key="offline",
                              webhook_id="offline", webhook_secret="offline"), sender=forbidden)
    assert result.decision.halt_reason == "m1_test_requires_explicit_dry_run"


@pytest.mark.parametrize("field,value", [
    ("cap_alloc", 2), ("cap_alloc", True), ("base_risk", math.nan),
    ("base_risk", .0001), ("pyr_pct", 1), ("dollars_per_pt", 2),
    ("leg_key", "Striker"), ("cap_alloc", -1),
])
def test_mutated_test_constants_fail_zero(host, field, value):
    constants = json.loads(host.constants_path.read_text())
    constants["leg_map"][LEG][field] = value
    write(host.constants_path, constants)
    decision = host.process_signal(payload(), 100000.)
    assert decision.halt and decision.qty_out == 0 and not decision.submit


@pytest.mark.parametrize("state", [None, [], "AUTHORIZED", {KEY: []}, {KEY: "unknown"}])
def test_malformed_lifecycle_fails_zero(host, state):
    write(host.lifecycle_state_path, state)
    assert host.process_signal(payload(), 100000.).qty_out == 0


@pytest.mark.parametrize("equity", [None, True, math.nan, math.inf, -1., 0., "100000"])
def test_invalid_equity_fails_zero(host, equity):
    decision = host.process_signal(payload(), equity)
    assert decision.halt and decision.qty_out == 0


@pytest.mark.parametrize("path_name", ["lifecycle_state_path", "constants_path", "dd_state_path"])
def test_unreadable_state_fails_zero(host, path_name):
    getattr(host, path_name).unlink()
    assert host.process_signal(payload(), 100000.).qty_out == 0


def test_no_headroom_is_not_borrowed(host):
    constants = json.loads(host.constants_path.read_text())
    constants["leg_map"]["dj30_mym"]["cap_alloc"] = 69
    constants["leg_map"]["nas100_mnq"]["cap_alloc"] = 11
    write(host.constants_path, constants)
    result = host.process_signal(payload(), 100000.)
    assert result.halt and result.qty_out == 0
    assert json.loads(host.constants_path.read_text()) == constants


def test_default_generator_keeps_test_cap_disabled():
    constants = generate_constants("Tradeify_Select_100K")
    assert constants["leg_map"][LEG]["cap_alloc"] == 0
    assert sum(r["cap_alloc"] for r in constants["leg_map"].values()) == 0


@pytest.mark.parametrize("field,value", [("stop_dist_pts", .5), ("stop_dist_pts", 2.), ("close", math.nan)])
def test_noncontract_signal_is_rejected(host, field, value):
    assert host.process_signal(payload(**{field: value}), 100000.).qty_out == 0


def test_zero_cap_and_retired_remain_zero(host):
    constants = json.loads(host.constants_path.read_text())
    constants["leg_map"][LEG]["cap_alloc"] = 0
    write(host.constants_path, constants)
    assert host.process_signal(payload(), 100000.).qty_out == 0
    constants["leg_map"][LEG]["cap_alloc"] = 1
    write(host.constants_path, constants)
    write(host.lifecycle_state_path, {KEY: "RETIRED"})
    assert host.process_signal(payload(), 100000.).qty_out == 0


def test_smallest_binary64_risk_boundary():
    # Independent hand-derived boundary: one tick costs .50, DD budget .50.
    r = .0000125
    assert math.floor(100000. * (r * .4) / .5) == 1
    assert math.floor(100000. * (math.nextafter(r, 0.) * .4) / .5) == 0


@pytest.mark.parametrize("peak", [True, None, [], "100000", 0., math.nan, math.inf])
def test_malformed_dd_never_creates_positive_quantity(host, peak):
    write(host.dd_state_path, {"peak_equity": peak})
    result = host.process_signal(payload(), 100000.)
    assert result.halt and result.qty_out == 0
