"""Offline SDK-shaped input -> real hook/client/HTTP adapter/listener/ledger.

These synthetic fixtures are software tests, not M1 item-5 evidence.
"""
from datetime import datetime, timedelta, timezone
import io
import json
from types import SimpleNamespace
from uuid import uuid4

import pytest

import c1_rail_listener
from c1_rail_http_server import make_handler
from c1_rail_telemetry import EventLedger
from c1_sizing_host_reference import C1SizingHostReference, generate_constants
from c1_rail.m1_stage1_contract import contract_sha256
from c1_rail.m1_stage1_control import project_evidence
from c1_signal_daemon.databento_live_source import DatabentoLiveBarSource
from c1_signal_daemon.evaluate_loop import EvaluateLoop
from c1_signal_daemon.listener_client import ListenerClient
from c1_signal_daemon.m1_stage1 import M1Coordinator
from c1_signal_daemon.m1_stage1_control import prepare, enable, close
from c1_signal_daemon.m1_stage1_state import CeremonyStore
from c1_signal_daemon.m1_stage1_strategy import M1Stage1TestStrategy


def write(path, value):
    path.write_text(json.dumps(value))
    return str(path)


@pytest.mark.parametrize("dry_run,equity", [(True, 100000.), (True, 98000.), (False, 100000.)])
def test_sdk_hook_to_http_decision_and_closed_proof(tmp_path, monkeypatch, dry_run, equity):
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
    source_binding = {"dataset": "GLBX.MDP3", "schema": "ohlcv-1m", "raw_symbol": "MYMU6",
                      "instrument_id": 123, "publisher_id": 1}
    manifest = {"ceremony_id": cid, "target": target.isoformat(),
        "expires": (target + timedelta(seconds=140)).isoformat(), "source": source_binding,
        "contract_sha256": contract_sha256(), "expected_qty": 1, "preflight_sha256": "e" * 64}
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
        handler._respond = lambda status, text: responses.append((status, text))
        handler.do_POST()  # actual authentication, parsing, equity and listener path
        assert len(responses) == 1
        return responses[0]

    stamp = int(target.timestamp()) * 10**9
    Mapping = type("SymbolMappingMsg", (SimpleNamespace,), {})
    OHLCV = type("OHLCVMsg", (SimpleNamespace,), {})
    class SDK:
        def add_callback(self, callback, error):
            self.callback = callback
        def subscribe(self, **kwargs):
            assert kwargs == {"dataset": "GLBX.MDP3", "schema": "ohlcv-1m",
                              "symbols": ["MYMU6"], "stype_in": "raw_symbol"}
        def start(self):
            self.callback(Mapping(stype_in="raw_symbol", stype_out="raw_symbol",
                stype_in_symbol="MYMU6", stype_out_symbol="MYMU6", instrument_id=123,
                publisher_id=1, start_ts=stamp-60*10**9, end_ts=stamp+3600*10**9))
            self.callback(OHLCV(rtype=33, instrument_id=123, publisher_id=1, ts_event=stamp,
                open=44000*10**9, high=44002*10**9, low=43999*10**9,
                close=44001*10**9, volume=5))
        def is_connected(self):
            return True
        def terminate(self):
            pass
    source = DatabentoLiveBarSource(store, sdk_factory=SDK, clock=lambda: received)
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
        proof = project_evidence(rows, store.read(), cid)
        assert proof["expected_qty"] == proof["observed_qty"] == 1
        assert proof["dry_run"] is True and proof["sender_invoked"] is False
        assert proof["dry_run_strategy_signal_event_id"] == rows[0]["event_id"]
        assert str(equity) not in json.dumps(proof)
    else:
        assert any(r.get("halt_reason") == "m1_test_requires_explicit_dry_run" for r in rows)
        with pytest.raises(ValueError):
            project_evidence(rows, store.read(), cid)
    store.boot("offline-new-boot")
    assert store.read()["enabled"] is False
    assert host.open_leg_state == {}
