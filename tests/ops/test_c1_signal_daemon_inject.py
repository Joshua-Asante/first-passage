from datetime import datetime, timedelta, timezone
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path

import pytest

from c1_rail.m1_stage1_contract import OPERATOR_INPUT_SOURCE, contract_sha256
from c1_signal_daemon import m1_stage1_control as control
from c1_signal_daemon.m1_stage1_state import CeremonyError, CeremonyStore
from c1_signal_daemon.operator_input_source import OperatorInputSource


TARGET = datetime(2026, 9, 10, 14, tzinfo=timezone.utc)
CID = "option-d-1"
BOOT = "boot-1"


def _write(path, value):
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def _bar(**changes):
    value = {"open": 44000.0, "high": 44002.0, "low": 43999.0,
             "close": 44001.0, "volume": 7.0}
    value.update(changes)
    return value


def _ceremony(tmp_path, *, enable=True, config_enabled=True, manifest_changes=None):
    state = tmp_path / "state.json"
    store = CeremonyStore(state)
    store.boot(BOOT)
    cfg_path = tmp_path / "daemon.json"
    cfg = {"listener_base_url": "https://offline.invalid", "path_token": "x" * 32,
           "bind_host": "127.0.0.1", "bind_port": 8080, "bar_period_s": 60,
           "poll_interval_s": 1, "emit_enabled": False, "strategy": "null",
           "m1_test": {"enabled": False, "state_path": str(state)}}
    _write(cfg_path, cfg)
    manifest = {"ceremony_id": CID, "target": TARGET.isoformat(),
                "expires": (TARGET + timedelta(seconds=150)).isoformat(),
                "contract_sha256": contract_sha256(), "expected_qty": 1,
                "preflight_sha256": "e" * 64, "source": OPERATOR_INPUT_SOURCE,
                "venue_contract": "MYMZ6"}
    if manifest_changes:
        manifest.update(manifest_changes)
    control.prepare(store, cfg_path, manifest, boot_id=BOOT,
                    now=TARGET - timedelta(minutes=1))
    if enable:
        control.enable(store, cfg_path, CID, boot_id=BOOT, reviewed=manifest,
                       now=TARGET - timedelta(seconds=30))
    if not config_enabled:
        cfg = json.loads(cfg_path.read_text())
        cfg["m1_test"]["enabled"] = False
        cfg["emit_enabled"] = False
        _write(cfg_path, cfg)
    upload = _write(tmp_path / f"m1_upload_{CID}.json", _bar())
    return store, cfg_path, manifest, upload


def _inject(store, cfg_path, upload, *, now=None, **changes):
    args = {"ceremony_id": CID, "boot_id": BOOT, "contract": "MYMZ6",
            "time": TARGET.isoformat(), "bar_file": upload,
            "now": now or TARGET + timedelta(seconds=60)}
    args.update(changes)
    return control.inject(store, cfg_path, **args)


@pytest.mark.parametrize("elapsed,allowed,reason", [
    (59, False, "before window"), (60, True, None),
    (120, True, None), (121, False, "after window"),
])
def test_inject_window_boundaries_and_upload_cleanup(tmp_path, elapsed, allowed, reason):
    store, cfg_path, _, upload = _ceremony(tmp_path)
    if allowed:
        receipt = _inject(store, cfg_path, upload, now=TARGET + timedelta(seconds=elapsed))
        assert receipt["action"] == "inject"
        assert (tmp_path / f"m1_bar_{CID}.json").is_file()
    else:
        with pytest.raises(CeremonyError, match=reason):
            _inject(store, cfg_path, upload, now=TARGET + timedelta(seconds=elapsed))
        assert not (tmp_path / f"m1_bar_{CID}.json").exists()
    assert not upload.exists()


@pytest.mark.parametrize("changes,reason", [
    ({"contract": "MYMU6"}, "contract mismatch"),
    ({"time": "2026-09-10T14:01:00+00:00"}, "time mismatch"),
    ({"boot_id": "wrong"}, "not active"),
])
def test_inject_refuses_identity_mismatch_and_removes_upload(tmp_path, changes, reason):
    store, cfg_path, _, upload = _ceremony(tmp_path)
    with pytest.raises(CeremonyError, match=reason):
        _inject(store, cfg_path, upload, **changes)
    assert not upload.exists()


@pytest.mark.parametrize("enabled,config_enabled", [(False, True), (True, False)])
def test_inject_requires_journal_and_config_enablement(tmp_path, enabled, config_enabled):
    store, cfg_path, _, upload = _ceremony(
        tmp_path, enable=enabled, config_enabled=config_enabled)
    with pytest.raises(CeremonyError, match="not enabled"):
        _inject(store, cfg_path, upload)
    assert not upload.exists()


def test_inject_refuses_expired_manifest(tmp_path):
    store, cfg_path, _, upload = _ceremony(
        tmp_path, manifest_changes={"expires": (TARGET + timedelta(seconds=61)).isoformat()})
    with pytest.raises(CeremonyError, match="not active"):
        _inject(store, cfg_path, upload, now=TARGET + timedelta(seconds=61))
    assert not upload.exists()


@pytest.mark.parametrize("raw", [
    None,
    [],
    {"open": 1, "high": 2, "low": 1, "close": 2},
    _bar(extra=1),
    _bar(open=True),
    _bar(open=0),
    _bar(open=-1),
    _bar(high=float("inf")),
    _bar(low=44001.5),
])
def test_inject_refuses_every_bad_bar_class(tmp_path, raw):
    store, cfg_path, _, upload = _ceremony(tmp_path)
    if raw is None:
        upload.write_text('{"open":', encoding="utf-8")
    else:
        upload.write_text(json.dumps(raw), encoding="utf-8")
    with pytest.raises(CeremonyError, match="bad bar file"):
        _inject(store, cfg_path, upload)
    assert not upload.exists()
    assert not (tmp_path / f"m1_claim_{CID}").exists()


def test_inject_publishes_distinct_one_shot_and_duplicate_claim_persists(tmp_path):
    store, cfg_path, _, upload = _ceremony(tmp_path)
    receipt = _inject(store, cfg_path, upload)
    published = tmp_path / f"m1_bar_{CID}.json"
    claim = tmp_path / f"m1_claim_{CID}"
    assert published.is_file() and claim.is_file() and not upload.exists()
    source = OperatorInputSource(tmp_path, boot_id=BOOT)
    source.activate(OPERATOR_INPUT_SOURCE, ceremony_id=CID)
    assert source.poll().close == 44001.0
    duplicate = _write(upload, _bar())
    with pytest.raises(CeremonyError, match="already injected"):
        _inject(store, cfg_path, duplicate)
    assert not duplicate.exists()
    assert json.loads(published.read_text())["bar_sha256"] == receipt["bar_sha256"]


@pytest.mark.parametrize("candidate", ["state", "config", "published", "sibling"])
def test_upload_path_validation_precedes_state_and_changes_nothing(tmp_path, candidate):
    store, cfg_path, _, upload = _ceremony(tmp_path)
    paths = {"state": store.path, "config": cfg_path,
             "published": tmp_path / f"m1_bar_{CID}.json",
             "sibling": tmp_path / "m1_upload_other.json"}
    paths["published"].write_text("published", encoding="utf-8")
    paths["sibling"].write_text("sibling", encoding="utf-8")
    before = {path: path.read_bytes() for path in set(paths.values()) | {upload}}
    with pytest.raises(CeremonyError, match="bad upload path"):
        _inject(store, cfg_path, paths[candidate], boot_id="wrong")
    assert {path: path.read_bytes() for path in before} == before


def test_close_removes_all_operator_input_files(tmp_path):
    store, cfg_path, _, upload = _ceremony(tmp_path)
    _inject(store, cfg_path, upload)
    control.close(store, cfg_path, CID)
    assert not any((tmp_path / name).exists() for name in (
        f"m1_upload_{CID}.json", f"m1_bar_{CID}.json", f"m1_claim_{CID}"))


@pytest.mark.parametrize("after_replace", [False, True])
def test_publication_failure_keeps_claim_and_prevents_retry(tmp_path, monkeypatch, after_replace):
    store, cfg_path, _, upload = _ceremony(tmp_path)
    original = control.atomic_json

    def fail(path, value):
        if after_replace:
            original(path, value)
        raise OSError("private publication detail")

    monkeypatch.setattr(control, "atomic_json", fail)
    with pytest.raises(CeremonyError, match="publication uncertain"):
        _inject(store, cfg_path, upload)
    published = tmp_path / f"m1_bar_{CID}.json"
    assert published.exists() is after_replace
    assert (tmp_path / f"m1_claim_{CID}").is_file()
    monkeypatch.setattr(control, "atomic_json", original)
    second = _write(upload, _bar())
    with pytest.raises(CeremonyError, match="already injected"):
        _inject(store, cfg_path, second)
    assert not second.exists()
    if after_replace:
        source = OperatorInputSource(tmp_path, boot_id=BOOT)
        source.activate(OPERATOR_INPUT_SOURCE, ceremony_id=CID)
        assert source.poll().close == 44001.0


def test_claim_close_failure_is_publication_uncertain_and_claim_is_kept(
        tmp_path, monkeypatch):
    store, cfg_path, _, upload = _ceremony(tmp_path)
    original = control.os.close

    def close_then_fail(fd):
        original(fd)
        raise OSError("private close detail")

    monkeypatch.setattr(control.os, "close", close_then_fail)
    with pytest.raises(CeremonyError, match="publication uncertain"):
        _inject(store, cfg_path, upload)
    assert (tmp_path / f"m1_claim_{CID}").is_file()
    assert not (tmp_path / f"m1_bar_{CID}.json").exists()


def test_concurrent_injectors_publish_once_without_replacement(tmp_path):
    store, cfg_path, _, upload = _ceremony(tmp_path)

    def invoke():
        try:
            return "ok", _inject(store, cfg_path, upload)
        except CeremonyError as exc:
            return "refused", str(exc)

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: invoke(), range(2)))
    assert [kind for kind, _ in results].count("ok") == 1
    assert [kind for kind, _ in results].count("refused") == 1
    assert next(value for kind, value in results if kind == "refused") in {
        "already injected", "bad bar file"}
    published = json.loads((tmp_path / f"m1_bar_{CID}.json").read_text())
    assert published["bar_sha256"] == next(
        value["bar_sha256"] for kind, value in results if kind == "ok")


def test_receipt_contains_no_bar_values_or_field_names(tmp_path):
    store, cfg_path, _, upload = _ceremony(tmp_path)
    receipt = json.dumps(_inject(store, cfg_path, upload), sort_keys=True)
    for private in ("44000", "44002", "43999", "44001", '"open"', '"high"',
                    '"low"', '"close"', '"volume"'):
        assert private not in receipt


def test_canonical_upload_symlink_is_refused_without_touching_target(
        tmp_path, monkeypatch):
    outside = tmp_path / "outside.json"
    outside.write_text(json.dumps(_bar()), encoding="utf-8")
    store, cfg_path, _, upload = _ceremony(tmp_path)
    upload.unlink()
    real_symlink = True
    try:
        upload.symlink_to(outside)
    except OSError:
        real_symlink = False
        original = Path.is_symlink
        monkeypatch.setattr(Path, "is_symlink",
                            lambda self: self == upload or original(self))
    before = outside.read_bytes()
    with pytest.raises(CeremonyError, match="bad upload path"):
        _inject(store, cfg_path, upload)
    assert upload.is_symlink() or not real_symlink
    assert outside.read_bytes() == before


def test_inject_cli_prints_value_free_receipt_and_status_tracks_publication(
        tmp_path, monkeypatch, capsys):
    store, cfg_path, _, upload = _ceremony(tmp_path)
    assert control.safe_status(store)["source_status"] == "disconnected"

    class Clock:
        fromisoformat = datetime.fromisoformat

        @staticmethod
        def now(tz):
            return TARGET + timedelta(seconds=60)

    monkeypatch.setattr(control, "datetime", Clock)
    result = control.main([
        "inject", "--state", str(store.path), "--config", str(cfg_path),
        "--ceremony-id", CID, "--boot-id", BOOT, "--contract", "MYMZ6",
        "--time", TARGET.isoformat(), "--bar-file", str(upload),
    ])
    assert result == 0
    receipt = capsys.readouterr().out
    assert json.loads(receipt)["action"] == "inject"
    assert control.safe_status(store)["source_status"] == "bar_published"
    for private in ("44000", "44002", "43999", "44001", '"open"', '"high"',
                    '"low"', '"close"', '"volume"'):
        assert private not in receipt


def test_bad_upload_path_cli_verdict_precedes_consumed_ceremony_state(
        tmp_path, capsys):
    store, cfg_path, _, upload = _ceremony(tmp_path)
    _inject(store, cfg_path, upload)
    control.close(store, cfg_path, CID)
    protected = store.path.read_bytes()
    result = control.main([
        "inject", "--state", str(store.path), "--config", str(cfg_path),
        "--ceremony-id", CID, "--boot-id", BOOT, "--contract", "MYMZ6",
        "--time", TARGET.isoformat(), "--bar-file", str(store.path),
    ])
    assert result == 2
    assert capsys.readouterr().out.strip() == "inject refused: bad upload path"
    assert store.path.read_bytes() == protected


def test_inject_cli_missing_bar_file_fails_closed_without_traceback(tmp_path, capsys):
    store, cfg_path, _, _ = _ceremony(tmp_path)
    result = control.main([
        "inject", "--state", str(store.path), "--config", str(cfg_path),
        "--ceremony-id", CID, "--boot-id", BOOT, "--contract", "MYMZ6",
        "--time", TARGET.isoformat(),
    ])
    assert result == 2
    assert capsys.readouterr().out.strip() == "inject refused: bad upload path"
