"""Offline ceremony fixtures. These are never genuine M1 item-5 evidence."""
from datetime import datetime, timedelta, timezone
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor

import pytest

from c1_signal_daemon import daemon
from c1_signal_daemon.feed import Bar
from c1_signal_daemon.listener_client import ListenerClient
from c1_signal_daemon.evaluate_loop import EvaluateLoop

NOW = datetime(2026, 9, 10, 20, 0, tzinfo=timezone.utc)
TARGET = NOW + timedelta(minutes=2)


def api():
    from c1_signal_daemon import m1_stage1
    return m1_stage1


def cfg():
    return dict(listener_base_url="https://offline.invalid", path_token="x" * 32,
                bind_host="127.0.0.1", bind_port=8081, bar_period_s=60,
                emit_enabled=False, poll_interval_s=0.1, strategy="m1_stage1_test",
                m1_test={"enabled": False})


def manifest(**changes):
    from c1_rail.m1_stage1_contract import contract_sha256
    value = dict(ceremony_id="offline-001", target=TARGET.isoformat(),
                 expires=(TARGET + timedelta(seconds=140)).isoformat(),
                 contract_sha256=contract_sha256(), expected_qty=1,
                 preflight_sha256="a" * 64, venue_contract="MYMZ6",
                 source={"kind": "offline_fixture", "schema": "ohlcv-1m", "symbol": "MYM1!"})
    value.update(changes)
    return value


def prepared(tmp_path):
    m = api()
    path = tmp_path / "config.json"
    path.write_text(json.dumps(cfg()))
    store = m.CeremonyStore(tmp_path / "state.json")
    store.boot("boot-A")
    m.prepare(store, path, manifest(), boot_id="boot-A", now=NOW)
    return m, store, path


def test_config_defaults_and_truthy_flags_fail_closed(tmp_path):
    path = tmp_path / "c.json"
    c = cfg()
    del c["strategy"]
    del c["m1_test"]
    path.write_text(json.dumps(c))
    loaded = daemon.load_config(path)
    assert loaded["strategy"] == "null"
    assert loaded["m1_test"]["enabled"] is False
    for value in ("false", "true", 1, [], None):
        c["emit_enabled"] = value
        path.write_text(json.dumps(c))
        with pytest.raises((ValueError, SystemExit)):
            daemon.load_config(path)


def test_prepare_cannot_emit_and_enable_requires_current_boot(tmp_path):
    m, store, path = prepared(tmp_path)
    assert store.read()["ceremonies"]["offline-001"]["state"] == "READY"
    assert daemon.load_config(path)["emit_enabled"] is False
    with pytest.raises(m.CeremonyError):
        m.enable(store, path, "offline-001", boot_id="old", reviewed=manifest(), now=NOW)
    m.enable(store, path, "offline-001", boot_id="boot-A", reviewed=manifest(), now=NOW)
    assert daemon.load_config(path)["emit_enabled"] is True
    store.boot("boot-B")
    assert store.read()["ceremonies"]["offline-001"]["state"] == "CLOSED"
    with pytest.raises(m.CeremonyError):
        m.enable(store, path, "offline-001", boot_id="boot-B", reviewed=manifest(), now=NOW)


def test_corrupt_or_removed_state_never_reinitialized(tmp_path):
    m, store, path = prepared(tmp_path)
    store.path.write_text("{")
    with pytest.raises(m.CeremonyError):
        store.boot("other")
    store.path.unlink()
    with pytest.raises(m.CeremonyError):
        store.boot("other")


def test_ownership_lock_excludes_second_daemon(tmp_path):
    m = api()
    with m.DaemonOwnership(tmp_path / "owner.lock"):
        with pytest.raises(m.CeremonyError):
            with m.DaemonOwnership(tmp_path / "owner.lock"):
                pass


def active_loop(tmp_path, outcome=(200, '{"listener_id":"fixture-1"}')):
    m, store, path = prepared(tmp_path)
    m.enable(store, path, "offline-001", boot_id="boot-A", reviewed=manifest(), now=NOW)
    class Source:
        connected = True
        binding = manifest()["source"]
        def activate(self, binding, *, ceremony_id):
            assert binding == self.binding
            assert ceremony_id == "offline-001"
        def deactivate(self):
            pass
        def poll(self):
            return Bar(TARGET, 41000, 41002, 40999, 41001, 3)
    calls = []
    def transport(url, body, headers):
        # The reservation must already be durable when bytes leave the client.
        assert store.read()["ceremonies"]["offline-001"]["state"] == "SEND_RESERVED"
        calls.append(body)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome
    coordinator = m.M1Coordinator(store, path, boot_id="boot-A")
    loop = EvaluateLoop(source=Source(), strategy=m.M1Stage1TestStrategy(coordinator),
                        coordinator=coordinator, bar_period_s=60,
                        client=ListenerClient(base_url="https://offline.invalid", path_token="x" * 32,
                                              transport=transport))
    return loop, store, calls, path


@pytest.mark.parametrize("outcome,state", [((200, '{"listener_id":"fixture-1"}'), "RESPONSE_RECORDED"),
                                           ((409, "private refusal"), "RESPONSE_RECORDED"),
                                           (TimeoutError("secret-token"), "TRANSPORT_UNKNOWN")])
def test_normal_signal_client_path_is_durable_and_never_retries(tmp_path, outcome, state, caplog):
    loop, store, calls, path = active_loop(tmp_path, outcome)
    when = TARGET + timedelta(seconds=61)
    record = loop.step(when)
    loop.step(when)
    assert len(calls) == 1
    payload = json.loads(calls[0])
    assert payload["leg_id"] == "m1_stage1_test"
    assert payload["signal_type"] == "entry"
    assert payload["close"] == 41001
    assert payload["stop_dist_pts"] == 1
    assert set(payload) == {"leg_id", "signal_type", "bar_time", "close", "stop_dist_pts"}
    ceremony = store.read()["ceremonies"]["offline-001"]
    assert ceremony["state"] == state
    assert ceremony["request_sha256"] == hashlib.sha256(calls[0]).hexdigest()
    assert "payload" not in record
    assert "private refusal" not in caplog.text
    assert "secret-token" not in caplog.text
    assert "private refusal" not in str(loop.heartbeat(when).as_json_dict())
    store.boot("boot-B")
    loop.step(when)
    assert len(calls) == 1


def test_concurrent_steps_claim_at_most_once(tmp_path):
    loop, store, calls, path = active_loop(tmp_path)
    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(lambda _: loop.step(TARGET + timedelta(seconds=61)), range(20)))
    assert len(calls) == 1


def test_generation_tamper_suppresses_before_poll(tmp_path):
    loop, store, calls, path = active_loop(tmp_path)
    c = json.loads(path.read_text())
    c["m1_test"]["generation"] += 1
    path.write_text(json.dumps(c))
    assert loop.step(TARGET + timedelta(seconds=61))["action"] == "suppress"
    assert calls == []


def test_missing_target_closes_without_a_send(tmp_path):
    loop, store, calls, path = active_loop(tmp_path)
    loop.step(TARGET + timedelta(seconds=151))
    assert calls == []
    assert store.read()["ceremonies"]["offline-001"]["state"] == "CLOSED"


@pytest.mark.parametrize("stage", ["EVALUATED", "SEND_RESERVED", "EMITTED",
                                    "RESPONSE_RECORDED", "TRANSPORT_UNKNOWN", "CLOSED"])
def test_restart_preserves_all_claimed_stages(tmp_path, stage):
    m, store, path = prepared(tmp_path)
    def checkpoint(obj):
        obj["ceremonies"]["offline-001"]["state"] = stage
        obj["tombstones"]["offline-001"] = {"reason": "offline_crash_checkpoint"}
    store.mutate(checkpoint)
    store.boot("boot-after-crash")
    assert store.read()["ceremonies"]["offline-001"]["state"] == stage
    with pytest.raises(m.CeremonyError):
        m.prepare(store, path, manifest(), boot_id="boot-after-crash", now=NOW)


def test_failed_reservation_write_never_reaches_transport(tmp_path, monkeypatch):
    import c1_signal_daemon.m1_stage1_state as state
    loop, store, calls, path = active_loop(tmp_path)
    original = state.atomic_json
    def failing_write(path, obj):
        item = obj["ceremonies"].get("offline-001", {})
        if item.get("state") == "SEND_RESERVED":
            raise OSError("offline disk fault")
        return original(path, obj)
    monkeypatch.setattr(state, "atomic_json", failing_write)
    with pytest.raises(OSError):
        loop.step(TARGET + timedelta(seconds=61))
    assert calls == []
    assert store.read()["ceremonies"]["offline-001"]["state"] == "EVALUATED"
    monkeypatch.setattr(state, "atomic_json", original)
    loop.step(TARGET + timedelta(seconds=61))
    assert calls == []


def test_preflight_and_reviewed_manifest_cannot_change_on_enable(tmp_path):
    m, store, path = prepared(tmp_path)
    altered = manifest()
    altered["preflight_sha256"] = "b" * 64
    with pytest.raises(m.CeremonyError):
        m.enable(store, path, "offline-001", boot_id="boot-A", reviewed=altered, now=NOW)
    altered = manifest()
    altered["expected_qty"] = True
    with pytest.raises(m.CeremonyError):
        m.enable(store, path, "offline-001", boot_id="boot-A", reviewed=altered, now=NOW)


def test_close_disables_first_and_retains_receipt(tmp_path):
    m = api()
    loop, store, calls, path = active_loop(tmp_path)
    m.close(store, path, "offline-001")
    loop.step(TARGET + timedelta(seconds=61))
    assert calls == []
    assert daemon.load_config(path)["emit_enabled"] is False
    assert "offline-001" in store.read()["tombstones"]


def test_missing_state_after_boot_makes_health_and_steps_fail_closed(tmp_path):
    loop, store, calls, path = active_loop(tmp_path)
    store.path.unlink()
    assert loop.step(TARGET + timedelta(seconds=61))["action"] == "suppress"
    assert loop.heartbeat(NOW).effective_emit is False
    assert calls == []


def test_reservation_rejects_noncontract_signal(tmp_path):
    loop, store, calls, path = active_loop(tmp_path)
    coordinator = loop._coordinator
    assert coordinator.before_poll(loop._source, TARGET + timedelta(seconds=61))
    legitimate = loop._strategy.on_bar(loop._source.poll())
    payload = dict(leg_id="other_leg", signal_type="add", bar_time=legitimate.bar_time,
                   close=41001, stop_dist_pts=100)
    assert coordinator.reserve(payload, TARGET + timedelta(seconds=61)) is False
    assert store.read()["ceremonies"]["offline-001"]["state"] == "READY"


@pytest.mark.parametrize("flag", [True, 1.0, "true"])
def test_state_enabled_corruption_cannot_arm_with_bool_equivalent_generation(tmp_path, flag):
    loop, store, calls, path = active_loop(tmp_path)
    c = json.loads(path.read_text())
    c["m1_test"]["generation"] = flag
    path.write_text(json.dumps(c))
    assert loop.step(TARGET + timedelta(seconds=61))["action"] == "suppress"
    assert calls == []


def test_process_lock_and_optimized_validation(tmp_path):
    import subprocess
    import sys
    from pathlib import Path
    m, store, path = prepared(tmp_path)
    ops = Path(__file__).resolve().parents[2] / "ops"
    script = """
import sys
sys.path.insert(0, sys.argv[1])
from c1_signal_daemon.m1_stage1_state import DaemonOwnership, CeremonyError
try:
    with DaemonOwnership(sys.argv[2]):
        raise SystemExit(5)
except CeremonyError:
    raise SystemExit(0)
"""
    lock = tmp_path / "owner.lock"
    with m.DaemonOwnership(lock):
        child = subprocess.run([sys.executable, "-O", "-c", script, str(ops), str(lock)],
                               capture_output=True, text=True, timeout=15)
    assert child.returncode == 0, child.stderr
    script = """
import sys
sys.path.insert(0, sys.argv[1])
from c1_signal_daemon.m1_stage1_state import CeremonyStore, CeremonyError
try:
    CeremonyStore(sys.argv[2]).read()
except CeremonyError:
    raise SystemExit(0)
raise SystemExit(5)
"""
    broken = json.loads(store.path.read_text())
    broken["enabled"] = "true"
    store.path.write_text(json.dumps(broken))
    child = subprocess.run([sys.executable, "-O", "-c", script, str(ops), str(store.path)],
                           capture_output=True, text=True, timeout=15)
    assert child.returncode == 0, child.stderr


def test_response_receipt_redacts_body_and_retains_bar_fingerprint(tmp_path):
    loop, store, calls, path = active_loop(tmp_path, (409, "private-equity-token"))
    loop.step(TARGET + timedelta(seconds=61))
    item = store.read()["ceremonies"]["offline-001"]
    assert "private-equity-token" not in store.path.read_text()
    assert item["response"] == {"http_status": 409, "response_kind": "rejected",
                                "body_sha256": hashlib.sha256(b"private-equity-token").hexdigest()}
    assert item["bar"] == {"timestamp": TARGET.isoformat(), "open": 41000.0,
                           "high": 41002.0, "low": 40999.0, "close": 41001.0,
                           "volume": 3.0, "venue_contract": "MYMZ6"}
    assert len(item["bar_sha256"]) == 64


def test_cli_prepare_enable_close_are_control_only(tmp_path, monkeypatch, capsys):
    from c1_signal_daemon import m1_stage1_control as control
    from c1_rail.m1_stage1_contract import OPERATOR_INPUT_SOURCE
    m = api()
    store = m.CeremonyStore(tmp_path / "state.json")
    store.boot("boot-A")
    path = tmp_path / "config.json"
    path.write_text(json.dumps(cfg()))
    value = manifest(ceremony_id="operator-001", source=OPERATOR_INPUT_SOURCE)
    reviewed = tmp_path / "manifest.json"
    reviewed.write_text(json.dumps(value))
    class Clock:
        @staticmethod
        def now(tz):
            return NOW
    monkeypatch.setattr(control, "datetime", Clock)
    # utc parsing still needs datetime.fromisoformat.
    Clock.fromisoformat = datetime.fromisoformat
    def forbidden(*args, **kwargs):
        raise AssertionError("control CLI must never send")
    monkeypatch.setattr(ListenerClient, "post_b1", forbidden)
    common = ["--state", str(store.path), "--config", str(path), "--boot-id", "boot-A",
              "--manifest", str(reviewed), "--ceremony-id", "operator-001"]
    assert control.main(["prepare", *common]) == 0
    assert control.main(["enable", *common]) == 0
    assert store.read()["enabled"] is True
    assert control.main(["close", *common]) == 0
    assert store.read()["enabled"] is False
    assert control.main(["status", *common]) == 0
    assert "path_token" not in capsys.readouterr().out


@pytest.mark.parametrize("unknown", [False, True])
def test_close_during_http_preserves_closed_state_and_terminal_outcome(tmp_path, unknown):
    m = api()
    loop, store, calls, path = active_loop(tmp_path)
    def transport(url, body, headers):
        calls.append(body)
        m.close(store, path, "offline-001")
        m.close(store, path, "offline-001")
        if unknown:
            raise TimeoutError("offline fixture timeout")
        return 200, "dry_run: computed, not sent"
    loop._client._transport = transport
    result = loop.step(TARGET + timedelta(seconds=61))
    assert result["action"] == ("transport_unknown" if unknown else "posted")
    item = store.read()["ceremonies"]["offline-001"]
    assert item["state"] == "CLOSED"
    assert item["previous_state"] == ("TRANSPORT_UNKNOWN" if unknown else "RESPONSE_RECORDED")
    assert (item["response"] is None) if unknown else item["response"]["response_kind"] == "dry_run_computed"
    assert loop.heartbeat(NOW).ceremony_state == "CLOSED"
    loop.step(TARGET + timedelta(seconds=61))
    assert len(calls) == 1


def test_close_between_response_checkpoints_is_never_reopened(tmp_path, monkeypatch):
    m = api()
    loop, store, calls, path = active_loop(tmp_path)
    original = store.mutate
    def interleaved(fn):
        result = original(fn)
        if store.read()["ceremonies"]["offline-001"]["state"] == "EMITTED":
            m.close(store, path, "offline-001")
        return result
    monkeypatch.setattr(store, "mutate", interleaved)
    loop.step(TARGET + timedelta(seconds=61))
    item = store.read()["ceremonies"]["offline-001"]
    assert item["state"] == "CLOSED"
    assert item["previous_state"] == "RESPONSE_RECORDED"
    assert item["response"]["http_status"] == 200
    assert store.read()["enabled"] is False


@pytest.mark.parametrize("stage", ["EVALUATED", "SEND_RESERVED", "EMITTED", "TRANSPORT_UNKNOWN"])
@pytest.mark.parametrize("disposition", ["active", "closed", "restarted"])
def test_unresolved_attempt_blocks_fresh_ceremony_identity(tmp_path, stage, disposition):
    m, store, path = prepared(tmp_path)
    def pending(obj):
        obj["ceremonies"]["offline-001"]["state"] = stage
        obj["tombstones"]["offline-001"] = {"reason": "offline_checkpoint"}
    store.mutate(pending)
    if disposition == "closed":
        m.close(store, path, "offline-001")
    if disposition == "restarted":
        store.boot("boot-B")
    before = store.path.read_bytes(), path.read_bytes()
    next_manifest = {**manifest(), "ceremony_id": "offline-new"}
    with pytest.raises(m.CeremonyError, match="unresolved"):
        m.prepare(store, path, next_manifest,
                  boot_id="boot-B" if disposition == "restarted" else "boot-A", now=NOW)
    assert (store.path.read_bytes(), path.read_bytes()) == before


def test_actual_newline_response_is_classified_without_changing_body_hash(tmp_path):
    body = "dry_run: computed, not sent\n"
    loop, store, calls, path = active_loop(tmp_path, (200, body))
    loop.step(TARGET + timedelta(seconds=61))
    response = store.read()["ceremonies"]["offline-001"]["response"]
    assert response["response_kind"] == "dry_run_computed"
    assert response["body_sha256"] == hashlib.sha256(body.encode()).hexdigest()
