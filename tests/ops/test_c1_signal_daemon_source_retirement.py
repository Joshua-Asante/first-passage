"""Retirement leaves no executable feed or attended emission route."""
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


def test_runtime_stays_null_even_with_previously_enabled_ceremony(tmp_path):
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
    heartbeat = loop.heartbeat(NOW)
    assert heartbeat.strategy == "NullStrategy"
    assert heartbeat.feed_mode == "unavailable"
    assert not heartbeat.connected and not heartbeat.effective_emit


@pytest.mark.parametrize("action", ["prepare", "enable"])
def test_attended_activation_is_blocked_without_state_writes(tmp_path, action, capsys, monkeypatch):
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
    assert "no approved source" in capsys.readouterr().out
    assert (store.path.read_bytes(), path.read_bytes()) == before


def test_unavailable_runtime_does_not_log_each_poll(tmp_path, monkeypatch, caplog):
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
