"""Agent attribution must accompany real guarded publication, not just a marker."""
from datetime import datetime, timedelta, timezone
import json

import pytest

from c1_rail.m1_stage1_contract import contract_sha256
from c1_signal_daemon import m1_stage1_control as control
from c1_signal_daemon.m1_stage1_state import CeremonyError, CeremonyStore
from c1_signal_daemon.operator_input_source import OperatorInputSource

TARGET = datetime(2026, 9, 14, 15, 46, tzinfo=timezone.utc)
SOURCE = {"kind": "agent_attended_browser_capture", "schema": "ohlcv-1m", "symbol": "MYM1!"}


@pytest.mark.parametrize("value", [None, [], "invalid", 1])
def test_manifest_non_object_fails_with_controlled_refusal(value):
    with pytest.raises(CeremonyError):
        control.validate_manifest(value)


def setup_agent(tmp_path, *, operator=False):
    store = CeremonyStore(tmp_path / "state.json")
    store.boot("test-boot")
    cfg = tmp_path / "daemon.json"
    cfg.write_text(json.dumps({"listener_base_url": "https://offline.invalid",
        "path_token": "x" * 32, "bind_host": "127.0.0.1", "bind_port": 8080,
        "bar_period_s": 60, "poll_interval_s": 1, "emit_enabled": False,
        "strategy": "null"}))
    manifest = {"ceremony_id": "agent-test", "target": TARGET.isoformat(),
        "expires": (TARGET + timedelta(seconds=150)).isoformat(),
        "contract_sha256": contract_sha256(), "expected_qty": 1,
        "preflight_sha256": "e" * 64, "source": SOURCE, "venue_contract": "MYMZ6",
        "operator_authorization_sha256": "a" * 64}
    if operator:
        manifest["source"] = {"kind": "operator_attended_input", "schema": "ohlcv-1m", "symbol": "MYM1!"}
        del manifest["operator_authorization_sha256"]
    control.prepare(store, cfg, manifest, boot_id="test-boot", now=TARGET-timedelta(minutes=5))
    return store, cfg, manifest


def upload_agent(tmp_path, **changes):
    capture = {"actor": "codex", "captured_at": "2026-09-14T15:47:00+00:00",
        "chart_timestamp": "2026-09-14T11:46:00-04:00", "venue_contract": "MYMZ6",
        "bar_period_s": 60}
    capture.update(changes)
    path = tmp_path / "m1_upload_agent-test.json"
    path.write_text(json.dumps({"open": 100., "high": 102., "low": 99.,
                               "close": 101., "volume": 12., "capture": capture}))
    return path


def enable_agent(store, cfg, manifest, actor="codex"):
    control.enable(store, cfg, "agent-test", boot_id="test-boot", reviewed=manifest,
                   now=TARGET-timedelta(seconds=30), actor=actor)


def inject_agent(store, cfg, path, actor="codex"):
    return control.inject(store, cfg, ceremony_id="agent-test", boot_id="test-boot",
        contract="MYMZ6", time=TARGET.isoformat(), bar_file=path,
        now=TARGET+timedelta(seconds=61), actor=actor)


def test_agent_publication_carries_explicit_action_evidence_and_yields_once(tmp_path):
    store, cfg, manifest = setup_agent(tmp_path)
    enable_agent(store, cfg, manifest)
    receipt = inject_agent(store, cfg, upload_agent(tmp_path))
    item = store.read()["ceremonies"]["agent-test"]
    assert item["agent_evidence"]["enable"] == {"actor": "codex", "at": "2026-09-14T15:45:30+00:00"}
    assert item["agent_evidence"]["inject"] == {"actor": "codex", "at": "2026-09-14T15:47:01+00:00"}
    assert item["agent_evidence"]["bar_sha256"] == receipt["bar_sha256"]
    source = OperatorInputSource(tmp_path, boot_id="test-boot")
    source.activate(SOURCE, ceremony_id="agent-test")
    bar = source.poll()
    assert (bar.ts, bar.open, bar.high, bar.low, bar.close, bar.volume) == (TARGET, 100., 102., 99., 101., 12.)
    assert source.poll() is None
    control.close(store, cfg, "agent-test")
    assert store.read()["ceremonies"]["agent-test"]["agent_evidence"] == item["agent_evidence"]


@pytest.mark.parametrize("actor", [None, "operator"])
def test_agent_enable_requires_explicit_actor_without_enabling(tmp_path, actor):
    store, cfg, manifest = setup_agent(tmp_path)
    with pytest.raises(CeremonyError):
        enable_agent(store, cfg, manifest, actor)
    assert store.read()["enabled"] is False
    assert json.loads(cfg.read_text())["emit_enabled"] is False


@pytest.mark.parametrize("changes", [
    {"actor": "operator"}, {"chart_timestamp": "2026-09-14T11:47:00-04:00"},
    {"chart_timestamp": "2026-09-14T11:46:00"}, {"venue_contract": "MYMU6"},
    {"bar_period_s": 15}, {"bar_period_s": True},
    {"captured_at": "2026-09-14T15:46:59+00:00"},
    {"captured_at": "2026-09-14T15:47:02+00:00"},
    {"captured_at": "2026-09-14T15:47:00"}, {"extra": "unreviewed"},
])
def test_bad_capture_never_publishes(tmp_path, changes):
    store, cfg, manifest = setup_agent(tmp_path)
    enable_agent(store, cfg, manifest)
    path = upload_agent(tmp_path, **changes)
    with pytest.raises(CeremonyError):
        inject_agent(store, cfg, path)
    assert not path.exists()
    assert not (tmp_path / "m1_bar_agent-test.json").exists()


def test_agent_inject_requires_actor_and_preserves_no_publication(tmp_path):
    store, cfg, manifest = setup_agent(tmp_path)
    enable_agent(store, cfg, manifest)
    with pytest.raises(CeremonyError):
        inject_agent(store, cfg, upload_agent(tmp_path), actor=None)
    assert not (tmp_path / "m1_bar_agent-test.json").exists()


@pytest.mark.parametrize("authorization", [None, "", "x"*64])
def test_agent_manifest_rejects_missing_or_invalid_authorization(tmp_path, authorization):
    _, _, manifest = setup_agent(tmp_path)
    manifest["operator_authorization_sha256"] = authorization
    with pytest.raises(CeremonyError):
        control.validate_manifest(manifest)


@pytest.mark.parametrize("action", ["enable", "inject"])
def test_explicit_agent_action_cannot_be_labeled_as_manual(tmp_path, action):
    store, cfg, manifest = setup_agent(tmp_path, operator=True)
    if action == "enable":
        with pytest.raises(CeremonyError):
            enable_agent(store, cfg, manifest)
        assert store.read()["enabled"] is False
    else:
        enable_agent(store, cfg, manifest, actor=None)
        path = upload_agent(tmp_path)
        bar = json.loads(path.read_text())
        del bar["capture"]
        path.write_text(json.dumps(bar))
        with pytest.raises(CeremonyError):
            inject_agent(store, cfg, path)
        assert not (tmp_path / "m1_bar_agent-test.json").exists()
