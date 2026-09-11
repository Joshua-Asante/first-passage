"""Retired provider stays absent while option D supplies the bounded source."""
import importlib.util
import json

import pytest

from c1_signal_daemon import daemon, m1_stage1_control as control
from test_c1_signal_daemon_m1 import prepared, manifest, NOW


def test_no_retired_provider_module_or_dependency():
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    assert importlib.util.find_spec("c1_signal_daemon.databento_live_source") is None
    assert not (root / "deploy/c1_signal_daemon/requirements.txt").exists()


def test_runtime_wires_operator_source_but_stale_boot_stays_inert(tmp_path):
    _, store, path = prepared(tmp_path)
    control.enable(store, path, "offline-001", boot_id="boot-A", reviewed=manifest(), now=NOW)
    cfg = json.loads(path.read_text())
    cfg["m1_test"]["state_path"] = str(store.path)
    path.write_text(json.dumps(cfg))
    def forbidden(*args, **kwargs):
        pytest.fail("retired source runtime attempted HTTP")
    loop = daemon.build_loop(path, boot_id="boot-B", transport=forbidden)
    for _ in range(3):
        loop.step(NOW)
    heartbeat = loop.heartbeat(NOW, poll_interval_s=0.1)
    assert heartbeat.strategy == "NullStrategy"
    assert heartbeat.feed_mode == "operator_input"
    assert heartbeat.poll_interval_s == 0.1
    assert not heartbeat.connected and not heartbeat.effective_emit
    assert loop._coordinator is not None


@pytest.mark.parametrize("action", ["prepare", "enable"])
def test_runtime_cli_refuses_offline_marker_without_state_writes(tmp_path, action, capsys, monkeypatch):
    _, store, path = prepared(tmp_path)
    reviewed = tmp_path / "manifest.json"
    value = manifest()
    if action == "prepare":
        control.close(store, path, "offline-001")
        value["ceremony_id"] = "new-id"
    from datetime import datetime
    class Clock:
        fromisoformat = datetime.fromisoformat
        @staticmethod
        def now(tz):
            return NOW
    monkeypatch.setattr(control, "datetime", Clock)
    reviewed.write_text(json.dumps(value))
    before = store.path.read_bytes(), path.read_bytes()
    result = control.main([action, "--state", str(store.path), "--config", str(path),
        "--boot-id", "boot-A", "--manifest", str(reviewed), "--ceremony-id", value["ceremony_id"]])
    assert result == 2
    assert "ceremony control failed closed" in capsys.readouterr().out
    assert (store.path.read_bytes(), path.read_bytes()) == before


def test_inject_cli_refuses_offline_marker(tmp_path, capsys):
    _, store, path = prepared(tmp_path)
    control.enable(store, path, "offline-001", boot_id="boot-A", reviewed=manifest(), now=NOW)
    upload = tmp_path / "m1_upload_offline-001.json"
    upload.write_text(json.dumps({"open": 1, "high": 2, "low": 1,
                                  "close": 2, "volume": 1}))
    result = control.main(["inject", "--state", str(store.path), "--config", str(path),
        "--boot-id", "boot-A", "--ceremony-id", "offline-001", "--contract", "MYMZ6",
        "--time", manifest()["target"], "--bar-file", str(upload)])
    assert result == 2
    assert capsys.readouterr().out.startswith("inject refused:")
    assert not upload.exists()


def test_operator_runtime_does_not_log_each_idle_poll(tmp_path, monkeypatch, caplog):
    import logging
    from types import SimpleNamespace
    from test_c1_signal_daemon_m1 import cfg
    value = cfg()
    value["strategy"] = "null"
    value["m1_test"]["state_path"] = str(tmp_path / "idle-state.json")
    path = tmp_path / "config.json"
    path.write_text(json.dumps(value))
    monkeypatch.setattr(daemon, "serve_health", lambda **kwargs: SimpleNamespace(
        serve_forever=lambda: None, shutdown=lambda: None))
    polls = []
    def sleep(interval):
        polls.append(interval)
        if len(polls) == 3:
            raise KeyboardInterrupt
    monkeypatch.setattr(daemon.time, "sleep", sleep)
    with caplog.at_level(logging.INFO):
        assert daemon.run_daemon(path, value) == 0
    assert len(polls) == 3
    assert not any(r.getMessage().startswith("step ") for r in caplog.records)


def test_enabled_ceremony_awaiting_injection_does_not_log_each_poll(tmp_path, monkeypatch, caplog):
    import logging
    from types import SimpleNamespace
    from c1_rail.m1_stage1_contract import OPERATOR_INPUT_SOURCE
    from test_c1_signal_daemon_m1 import cfg, manifest
    value = cfg()
    value["m1_test"]["state_path"] = str(tmp_path / "state.json")
    path = tmp_path / "config.json"
    path.write_text(json.dumps(value))
    store = control.CeremonyStore(value["m1_test"]["state_path"])
    store.boot("boot-A")
    reviewed = manifest(source=OPERATOR_INPUT_SOURCE)
    control.prepare(store, path, reviewed, boot_id="boot-A", now=NOW)
    control.enable(store, path, "offline-001", boot_id="boot-A", reviewed=reviewed, now=NOW)
    monkeypatch.setattr(daemon.uuid, "uuid4", lambda: SimpleNamespace(hex="boot-A"))
    monkeypatch.setattr(daemon, "serve_health", lambda **kwargs: SimpleNamespace(
        serve_forever=lambda: None, shutdown=lambda: None))
    polls = []
    def sleep(interval):
        polls.append(interval)
        if len(polls) == 3:
            raise KeyboardInterrupt
    monkeypatch.setattr(daemon.time, "sleep", sleep)
    with caplog.at_level(logging.INFO):
        assert daemon.run_daemon(path, value) == 0
    assert not any(r.getMessage().startswith("step ") for r in caplog.records)


@pytest.mark.parametrize("interval", [0, -1, "1", True, float("nan")])
def test_load_config_rejects_nonpositive_or_nonfinite_poll_interval(tmp_path, interval):
    from test_c1_signal_daemon_m1 import cfg
    value = cfg()
    value["poll_interval_s"] = interval
    path = tmp_path / "config.json"
    path.write_text(json.dumps(value))
    with pytest.raises(ValueError):
        daemon.load_config(path)


@pytest.mark.parametrize("interval,accepted", [(5, False), (1, True), (0.5, True)])
def test_prepare_enforces_ceremony_poll_interval(tmp_path, interval, accepted):
    from c1_rail.m1_stage1_contract import OPERATOR_INPUT_SOURCE
    from test_c1_signal_daemon_m1 import cfg, manifest
    value = cfg()
    value["poll_interval_s"] = interval
    path = tmp_path / "config.json"
    path.write_text(json.dumps(value))
    store = control.CeremonyStore(tmp_path / "state.json")
    store.boot("boot-A")
    reviewed = manifest(source=OPERATOR_INPUT_SOURCE)
    if accepted:
        control.prepare(store, path, reviewed, boot_id="boot-A", now=NOW)
        assert store.read()["ceremonies"]["offline-001"]["state"] == "READY"
    else:
        with pytest.raises(control.CeremonyError):
            control.prepare(store, path, reviewed, boot_id="boot-A", now=NOW)
        assert store.read()["ceremonies"] == {}


def test_build_loop_cleans_operator_input_orphans_at_boot(tmp_path):
    from test_c1_signal_daemon_m1 import cfg
    value = cfg()
    value["m1_test"]["state_path"] = str(tmp_path / "state.json")
    path = tmp_path / "config.json"
    path.write_text(json.dumps(value))
    for name in ("m1_bar_old.json", "m1_upload_old.json", "m1_claim_old"):
        (tmp_path / name).write_text("private")
    loop = daemon.build_loop(path, boot_id="boot-A")
    assert loop._source.feed_mode == "operator_input"
    assert loop._source.connected is False
    assert loop._coordinator is not None
    assert not any((tmp_path / name).exists() for name in (
        "m1_bar_old.json", "m1_upload_old.json", "m1_claim_old"))
