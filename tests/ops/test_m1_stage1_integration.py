"""Offline fixture input -> real hook/client/HTTP adapter/listener/ledger.

These synthetic fixtures are software tests, not M1 item-5 evidence.
"""
from datetime import datetime, timedelta, timezone
import io
import json
from uuid import uuid4

import pytest

import c1_rail_listener
from c1_rail_http_server import make_handler
from c1_rail_telemetry import EventLedger
from c1_sizing_host_reference import C1SizingHostReference, generate_constants
from c1_rail.m1_stage1_contract import OPERATOR_INPUT_SOURCE, contract_sha256
from c1_rail.m1_stage1_control import project_evidence
from c1_signal_daemon.feed import Bar
from c1_signal_daemon.evaluate_loop import EvaluateLoop
from c1_signal_daemon.listener_client import ListenerClient
from c1_signal_daemon.m1_stage1 import M1Coordinator
from c1_signal_daemon.m1_stage1_control import prepare, enable, close, inject
from c1_signal_daemon.m1_stage1_state import CeremonyStore
from c1_signal_daemon.m1_stage1_strategy import M1Stage1TestStrategy
from c1_signal_daemon.operator_input_source import OperatorInputSource, cleanup_orphans


def write(path, value):
    path.write_text(json.dumps(value))
    return str(path)


@pytest.mark.parametrize("dry_run,equity", [(True, 100000.), (True, 98000.), (False, 100000.)])
@pytest.mark.parametrize("source_mode", ["offline", "operator"])
def test_fixture_hook_to_http_decision_and_closed_proof(
        tmp_path, monkeypatch, dry_run, equity, source_mode):
    def never_send(*args, **kwargs):
        pytest.fail("venue sender reached by test identity")
    monkeypatch.setattr(c1_rail_listener, "send_to_crosstrade", never_send)
    target = datetime(2026, 9, 10, 14, tzinfo=timezone.utc)
    now = target - timedelta(minutes=1)
    received = target + timedelta(seconds=61)
    cid = str(uuid4())
    constants = generate_constants("Tradeify_Select_100K")
    constants["leg_map"]["m1_stage1_test"]["cap_alloc"] = 1
    cfg = {
        "lifecycle_state_path": write(tmp_path / "lifecycle.json", {"M1 Stage1 Test": "AUTHORIZED"}),
        "constants_path": write(tmp_path / "constants.json", constants),
        "dd_state_path": write(tmp_path / "dd.json", {"peak_equity": 100000.}),
        "equity_path": write(tmp_path / "equity.json", {"current_equity": equity}),
        "equity_source": "file", "dry_run": dry_run,
        "armed_until": None if dry_run else "2099-01-01T00:00:00+00:00",
        "account": "OFFLINE", "secret_key": "OFFLINE", "webhook_id": "OFFLINE",
        "webhook_secret": "OFFLINE", "path_token": "x" * 32,
    }
    from pathlib import Path
    host = C1SizingHostReference(*(Path(cfg[k]) for k in
                                 ("lifecycle_state_path", "dd_state_path", "constants_path")))
    ledger = EventLedger(tmp_path / "events.jsonl")
    Handler = make_handler(host, cfg, ledger=ledger)
    calls = []
    store = CeremonyStore(tmp_path / "daemon-state.json")
    store.boot("offline-boot")
    daemon_cfg = tmp_path / "daemon.json"
    write(daemon_cfg, {"listener_base_url": "https://offline.invalid", "path_token": "x" * 32,
        "bind_host": "127.0.0.1", "bind_port": 8080, "bar_period_s": 60,
        "poll_interval_s": 1, "emit_enabled": False, "strategy": "null"})
    source_binding = (OPERATOR_INPUT_SOURCE if source_mode == "operator" else
                      {"kind": "offline_fixture", "schema": "ohlcv-1m", "symbol": "MYM1!"})
    manifest = {"ceremony_id": cid, "target": target.isoformat(),
        "expires": (target + timedelta(seconds=140)).isoformat(), "source": source_binding,
        "contract_sha256": contract_sha256(), "expected_qty": 1,
        "preflight_sha256": "e" * 64, "venue_contract": "MYMZ6"}
    prepare(store, daemon_cfg, manifest, boot_id="offline-boot", now=now)
    enable(store, daemon_cfg, cid, boot_id="offline-boot", reviewed=manifest, now=now)

    def transport(url, body, headers):
        assert store.read()["ceremonies"][cid]["state"] == "SEND_RESERVED"
        calls.append(body)
        handler = Handler.__new__(Handler)
        handler.path = "/c1/" + cfg["path_token"]
        handler.headers = {"Content-Length": str(len(body)), **headers}
        handler.rfile = io.BytesIO(body)
        responses = []
        handler.send_response = responses.append
        handler.send_header = lambda *args: None
        handler.end_headers = lambda: None
        handler.wfile = io.BytesIO()
        handler.do_POST()  # actual authentication, parsing, equity and listener path
        assert len(responses) == 1
        return responses[0], handler.wfile.getvalue().decode("utf-8")

    if source_mode == "operator":
        upload = tmp_path / f"m1_upload_{cid}.json"
        upload.write_text(json.dumps({"open": 44000., "high": 44002., "low": 43999.,
                                      "close": 44001., "volume": 5.}))
        receipt = inject(store, daemon_cfg, ceremony_id=cid, boot_id="offline-boot",
                         contract="MYMZ6", time=target.isoformat(), bar_file=upload,
                         now=received)
        source = OperatorInputSource(tmp_path, boot_id="offline-boot")
    else:
        class OfflineFixtureSource:
            connected = True
            binding = source_binding
            def activate(self, binding, *, ceremony_id):
                assert binding == self.binding
                assert ceremony_id == cid
            def deactivate(self):
                pass
            def poll(self):
                return Bar(target, 44000., 44002., 43999., 44001., 5)
        source = OfflineFixtureSource()
    coordinator = M1Coordinator(store, daemon_cfg, boot_id="offline-boot")
    loop = EvaluateLoop(source=source, client=ListenerClient(base_url="https://offline.invalid",
        path_token="x"*32, transport=transport), strategy=M1Stage1TestStrategy(coordinator),
        coordinator=coordinator, bar_period_s=60)
    assert loop.step(received)["action"] == "posted"
    loop.step(received)
    assert len(calls) == 1
    close(store, daemon_cfg, cid)
    rows = list(ledger.iter_records())
    if dry_run:
        assert store.read()["ceremonies"][cid]["response"]["response_kind"] == "dry_run_computed"
        proof = project_evidence(rows, store.read(), cid)
        assert proof["expected_qty"] == proof["observed_qty"] == 1
        assert proof["offline_test_only"] is (source_mode == "offline")
        assert proof["operator_attended_input"] is (source_mode == "operator")
        assert proof["qualifying_live_source"] is False
        assert proof["venue_contract"] == ("MYMZ6" if source_mode == "operator" else None)
        assert proof["dry_run"] is True and proof["sender_invoked"] is False
        assert proof["listener_event_id"] == rows[0]["event_id"]
        assert str(equity) not in json.dumps(proof)
        if source_mode == "operator":
            assert receipt["bar_sha256"] == store.read()["ceremonies"][cid]["bar_sha256"]
    else:
        assert any(r.get("halt_reason") == "m1_test_requires_explicit_dry_run" for r in rows)
        with pytest.raises(ValueError):
            project_evidence(rows, store.read(), cid)
    store.boot("offline-new-boot")
    assert store.read()["enabled"] is False
    assert host.open_leg_state == {}


def test_crash_before_poll_removes_published_bar_and_allows_fresh_ceremony(tmp_path):
    target = datetime(2026, 9, 10, 14, tzinfo=timezone.utc)
    store = CeremonyStore(tmp_path / "state.json")
    store.boot("boot-1")
    cfg_path = tmp_path / "daemon.json"
    write(cfg_path, {"listener_base_url": "https://offline.invalid", "path_token": "x" * 32,
        "bind_host": "127.0.0.1", "bind_port": 8080, "bar_period_s": 60,
        "poll_interval_s": 1, "emit_enabled": False, "strategy": "null",
        "m1_test": {"enabled": False, "state_path": str(store.path)}})
    manifest = {"ceremony_id": "first", "target": target.isoformat(),
        "expires": (target + timedelta(seconds=150)).isoformat(),
        "source": OPERATOR_INPUT_SOURCE, "venue_contract": "MYMZ6",
        "contract_sha256": contract_sha256(), "expected_qty": 1,
        "preflight_sha256": "e" * 64}
    prepare(store, cfg_path, manifest, boot_id="boot-1", now=target - timedelta(minutes=1))
    enable(store, cfg_path, "first", boot_id="boot-1", reviewed=manifest,
           now=target - timedelta(seconds=30))
    upload = tmp_path / "m1_upload_first.json"
    upload.write_text(json.dumps({"open": 1, "high": 2, "low": 1,
                                  "close": 2, "volume": 1}))
    inject(store, cfg_path, ceremony_id="first", boot_id="boot-1", contract="MYMZ6",
           time=target.isoformat(), bar_file=upload, now=target + timedelta(seconds=60))
    assert (tmp_path / "m1_bar_first.json").is_file()
    store.boot("boot-2")
    cleanup_orphans(tmp_path)
    assert not (tmp_path / "m1_bar_first.json").exists()
    first = store.read()["ceremonies"]["first"]
    assert first["state"] == "CLOSED"
    assert store.read()["tombstones"]["first"]["reason"] == "boot_changed"
    next_target = target + timedelta(minutes=5)
    fresh = {**manifest, "ceremony_id": "second", "target": next_target.isoformat(),
             "expires": (next_target + timedelta(seconds=150)).isoformat()}
    prepare(store, cfg_path, fresh, boot_id="boot-2", now=target + timedelta(minutes=1))
    assert store.read()["ceremonies"]["second"]["state"] == "READY"
