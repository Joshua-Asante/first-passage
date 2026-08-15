"""Tests for scripts/m1_item5_capture.py — M1 §4 item 5 gate helper."""
from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts" / "m1_item5_capture.py"


def _load():
    import sys

    spec = importlib.util.spec_from_file_location("m1_item5_capture", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    # dataclasses looks up cls.__module__ in sys.modules during decoration
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


cap = _load()


def _triad(
    *,
    event_id: str = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
    leg_id: str = "dj30_mym",
    signal_type: str = "entry",
    qty_out: int = 8,
    stop: float = 60.82,
    close: float = 52985.0,
    bar_time: int = 1785512700000,  # 2026-07-31 09:05 ET-ish placeholder
    dry_run: bool = True,
    floored: bool | None = None,
    body_category: str = "b1_json",
    transport_state: str = "not_attempted",
    lifecycle: float = 0.5,
    dd_scale: float = 1.0,
    e_firm: float = 100_000.0,
    base_risk: float = 0.007,
    dollars_per_pt: float = 0.50,
    cap_alloc: float = 69.0,
    pyr_pct: float = 750.0,
) -> cap.Triad:
    r_eff = base_risk * dd_scale * lifecycle
    risk_dollars = e_firm * r_eff
    per_contract = stop * dollars_per_pt
    qty_base_raw = math.floor(risk_dollars / per_contract) if per_contract > 0 else 0
    reserve_cap = math.floor(cap_alloc / (1 + pyr_pct / 100))
    if floored is None:
        floored = qty_out == 0
    # Allow caller to force a mismatched qty_out for negative tests.
    submit = qty_out > 0
    req = {
        "kind": "request_received",
        "event_id": event_id,
        "seq": 1,
        "ts_utc": "2026-07-31T13:05:00+00:00",
        "auth_ok": True,
        "body_category": body_category,
        "body_sha256": "abc",
        "parsed": {
            "leg_id": leg_id,
            "signal_type": signal_type,
            "bar_time": bar_time,
            "close": close,
            "stop_dist_pts": stop,
        },
        "order_id": f"{leg_id}-{signal_type}-{bar_time}",
    }
    dec = {
        "kind": "decision",
        "event_id": event_id,
        "seq": 2,
        "ts_utc": "2026-07-31T13:05:00+00:00",
        "leg_id": leg_id,
        "signal_type": signal_type,
        "qty_out": qty_out,
        "submit": submit,
        "halt": False,
        "halt_reason": None,
        "floored": floored,
        "leg_key": "Striker",
        "dd_scale": dd_scale,
        "lifecycle_multiplier": lifecycle,
        "r_eff": r_eff,
        "risk_dollars": risk_dollars,
        "per_contract": per_contract,
        "qty_base_raw": qty_base_raw,
        "reserve_cap": reserve_cap,
        "pre_send": True,
        "current_equity": e_firm,
        "dry_run": dry_run,
        "order_id": f"{leg_id}-{signal_type}-{bar_time}",
    }
    tr = {
        "kind": "transport_result",
        "event_id": event_id,
        "seq": 3,
        "ts_utc": "2026-07-31T13:05:00+00:00",
        "transport_state": transport_state,
        "http_status": None,
        "error": None,
        "dry_run": dry_run,
        "payload_sha256": None,
        "execution_verified": False,
        "order_id": f"{leg_id}-{signal_type}-{bar_time}",
    }
    return cap.Triad(event_id=event_id, request=req, decision=dec, transport=tr)


def test_pass_nonzero_mym_entry():
    v = cap.evaluate_triad(_triad())
    assert v.ok, v.reasons
    assert v.qty_out == 8
    assert v.expected_band_qty == 8


def test_reject_qty_zero_mnq_class():
    """The 07-28 MNQ floored decision must not unlock item 5."""
    t = _triad(
        leg_id="nas100_mnq",
        qty_out=0,
        stop=126.75,
        close=28051.5,
        dollars_per_pt=2.0,
        base_risk=0.0037,
        cap_alloc=11.0,
        pyr_pct=1000.0,
    )
    # Force qty fields consistent with floor-to-zero.
    t.decision["qty_out"] = 0
    t.decision["qty_base_raw"] = 0
    t.decision["floored"] = True
    t.decision["submit"] = False
    t.decision["reserve_cap"] = 1
    t.decision["risk_dollars"] = 185.0
    t.decision["per_contract"] = 253.5
    t.decision["r_eff"] = 0.00185
    v = cap.evaluate_triad(t)
    assert not v.ok
    # It must be rejected for the SUBSTANTIVE reason (floored to zero), not for
    # being MNQ. The leg guard was widened 2026-08-02 (item 5 is leg-agnostic by
    # its own text); this test now pins the guard that actually did the work on
    # 07-28 and must never be relaxed.
    assert any("qty_out=0" in r for r in v.reasons)
    assert any("floored" in r for r in v.reasons)
    assert not any("need one of" in r for r in v.reasons), (
        "must NOT be rejected on leg identity"
    )


def test_accept_nonzero_mnq_entry():
    """Widened 2026-08-02: a NON-ZERO MNQ entry is valid item-5 evidence.

    MNQ needs stop <= 92.5 pts at WATCH-1 0.50x (reserve_cap = floor(11/11) = 1),
    so this is the case the 07-28 event would have been had its stop been tighter.
    """
    t = _triad(
        leg_id="nas100_mnq",
        qty_out=1,
        stop=60.0,
        close=29600.0,
        dollars_per_pt=2.0,
        base_risk=0.0037,
        cap_alloc=11.0,
        pyr_pct=1000.0,
    )
    t.decision["qty_out"] = 1
    t.decision["qty_base_raw"] = 1
    t.decision["floored"] = False
    t.decision["submit"] = True
    t.decision["reserve_cap"] = 1
    t.decision["risk_dollars"] = 185.0
    t.decision["per_contract"] = 120.0
    t.decision["r_eff"] = 0.00185
    v = cap.evaluate_triad(t)
    assert v.ok, f"non-zero MNQ entry should be item-5 evidence; got {v.reasons}"


def test_reject_mym_qty_zero():
    t = _triad(qty_out=0, stop=200.0)  # would floor
    t.decision["qty_out"] = 0
    t.decision["qty_base_raw"] = 0
    t.decision["floored"] = True
    t.decision["submit"] = False
    t.decision["per_contract"] = 100.0
    t.decision["risk_dollars"] = 350.0
    v = cap.evaluate_triad(t)
    assert not v.ok
    assert any("qty_out=0" in r for r in v.reasons)


def test_reject_armed_send():
    v = cap.evaluate_triad(
        _triad(dry_run=False, transport_state="accepted"),
        require_dry_run=True,
    )
    assert not v.ok
    assert any("dry_run" in r for r in v.reasons)


def test_cliff_at_87_50_still_eight():
    assert cap.expected_mym_entry_qty(87.50) == 8
    assert cap.expected_mym_entry_qty(87.51) == 7


def test_bar_time_decode_matches_07_28_mnq():
    utc, et = cap.decode_bar_time(1785253500000)
    assert utc.isoformat() == "2026-07-28T15:45:00+00:00"
    assert et.hour == 11 and et.minute == 45


def test_section_2b_delta():
    v = cap.evaluate_triad(_triad(close=52985.0), confirmed_close=52982.0)
    assert v.ok
    assert v.close_delta == pytest.approx(-3.0)
    assert any("signal-identity" in w for w in v.warnings)


def test_write_acceptance_refuses_overwrite(tmp_path):
    path = tmp_path / "acc.json"
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "status": "CODE_LANDED",
                "adr": "2026-07-22-c1-venue-native-monitoring-maturity.md",
                "code_commit_or_branch": "test",
                "offline_tests_note": "n",
                "secrets_present": False,
                "dry_run_strategy_signal_event_id": "already-set",
                "notes": ["a", "b", "c"],
            }
        ),
        encoding="utf-8",
    )
    v = cap.evaluate_triad(_triad())
    with pytest.raises(SystemExit):
        cap.write_acceptance(
            path,
            event_id=v.event_id,
            operator=None,
            confirm_resolved=False,
            verdict=v,
        )


def test_write_acceptance_item5_only(tmp_path):
    path = tmp_path / "acc.json"
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "status": "CODE_LANDED",
                "adr": "2026-07-22-c1-venue-native-monitoring-maturity.md",
                "code_commit_or_branch": "test",
                "offline_tests_note": "n",
                "secrets_present": False,
                "notes": ["a", "b", "c", "d"],
            }
        ),
        encoding="utf-8",
    )
    v = cap.evaluate_triad(_triad())
    assert v.ok
    cap.write_acceptance(
        path,
        event_id=v.event_id,
        operator=None,
        confirm_resolved=False,
        verdict=v,
    )
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["dry_run_strategy_signal_event_id"] == v.event_id
    assert data["status"] == "CODE_LANDED"
    assert "operator_signoff" not in data


def test_write_acceptance_resolved(tmp_path):
    path = tmp_path / "acc.json"
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "status": "CODE_LANDED",
                "adr": "2026-07-22-c1-venue-native-monitoring-maturity.md",
                "code_commit_or_branch": "test",
                "offline_tests_note": "n",
                "secrets_present": False,
                "notes": ["a", "b", "c"],
            }
        ),
        encoding="utf-8",
    )
    v = cap.evaluate_triad(_triad())
    cap.write_acceptance(
        path,
        event_id=v.event_id,
        operator="joshua",
        confirm_resolved=True,
        verdict=v,
    )
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["status"] == "RESOLVED"
    assert data["operator_signoff"]["operator"] == "joshua"


def test_preflight_clean_and_blocking():
    events = [
        {
            "kind": "request_received",
            "body_category": "b1_json",
            "ts_utc": "2026-07-28T16:07:59+00:00",
            "event_id": "x",
        }
    ]
    ok, msgs = cap.preflight_audit(
        events,
        "2026-07-28 15:28:19,562 INFO c1_rail_http: non-JSON alert body ignored\n",
    )
    assert ok, msgs

    bad_ok, bad_msgs = cap.preflight_audit(
        events,
        "2026-07-28 16:10:00,000 INFO c1_rail_http: non-JSON alert body ignored\n",
    )
    assert not bad_ok
    assert any("BLOCKING" in m for m in bad_msgs)


def test_load_jsonl_skips_fly_windows_trailer(tmp_path):
    p = tmp_path / "e.jsonl"
    row = {
        "kind": "request_received",
        "event_id": "e1",
        "body_category": "b1_json",
        "parsed": {},
    }
    p.write_text(
        json.dumps(row) + "\nError: The handle is invalid.\n",
        encoding="utf-8",
    )
    rows = cap.load_jsonl(p)
    assert len(rows) == 1


def test_cli_lists_and_refuses_zero(tmp_path):
    t = _triad(qty_out=8)
    # Also include a qty-0 MYM that must FAIL
    zero = _triad(event_id="00000000-0000-0000-0000-000000000001", qty_out=0, stop=200.0)
    zero.decision["qty_out"] = 0
    zero.decision["qty_base_raw"] = 0
    zero.decision["floored"] = True
    zero.decision["submit"] = False
    zero.decision["per_contract"] = 100.0
    zero.decision["risk_dollars"] = 350.0

    path = tmp_path / "events.jsonl"
    lines = []
    for triad in (zero, t):
        for part in (triad.request, triad.decision, triad.transport):
            lines.append(json.dumps(part))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    assert cap.main([str(path), "--list"]) == 0
    assert cap.main([str(path), "--event-id", zero.event_id]) == 2
    assert cap.main([str(path), "--latest"]) == 0

def test_write_acceptance_resolved_note_derives_leg(tmp_path):
    path = tmp_path / "acc.json"
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "status": "CODE_LANDED",
                "adr": "2026-07-22-c1-venue-native-monitoring-maturity.md",
                "code_commit_or_branch": "test",
                "offline_tests_note": "n",
                "secrets_present": False,
                "notes": ["a", "b", "c"],
            }
        ),
        encoding="utf-8",
    )
    t = _triad(leg_id="nas100_mnq", qty_out=1, stop=60.0, close=29600.0,
               dollars_per_pt=2.0, base_risk=0.0037, cap_alloc=11.0, pyr_pct=1000.0)
    t.decision["qty_out"] = 1
    t.decision["qty_base_raw"] = 1
    t.decision["floored"] = False
    t.decision["submit"] = True
    t.decision["reserve_cap"] = 1
    t.decision["risk_dollars"] = 185.0
    t.decision["per_contract"] = 120.0
    t.decision["r_eff"] = 0.00185
    v = cap.evaluate_triad(t)
    assert v.ok, v.reasons
    cap.write_acceptance(
        path,
        event_id=v.event_id,
        operator="joshua",
        confirm_resolved=True,
        verdict=v,
    )
    data = json.loads(path.read_text(encoding="utf-8"))
    note = data["operator_signoff"]["note"]
    assert "nas100_mnq" in note
    assert "MYM" not in note
    assert "dry_run=false send" not in note

