from datetime import datetime, timezone
import json
import logging
import math
import os
from pathlib import Path
import threading
import time

import pytest

from c1_rail.m1_stage1_contract import contract_sha256
from c1_signal_daemon.m1_stage1_control import validate_manifest
from c1_signal_daemon.m1_stage1_state import CeremonyError


OPERATOR_SOURCE = {
    "kind": "operator_attended_input",
    "schema": "ohlcv-1m",
    "symbol": "MYM1!",
}


def manifest(**changes):
    value = {
        "ceremony_id": "option-d-1",
        "target": "2026-09-10T14:00:00+00:00",
        "expires": "2026-09-10T14:02:30+00:00",
        "contract_sha256": contract_sha256(),
        "expected_qty": 1,
        "preflight_sha256": "e" * 64,
        "source": OPERATOR_SOURCE,
        "venue_contract": "MYMZ6",
    }
    value.update(changes)
    return value


@pytest.mark.parametrize("venue_contract", ["MYMU6", "MYMZ6"])
def test_manifest_accepts_current_or_next_quarterly_contract(venue_contract):
    value = manifest(venue_contract=venue_contract)
    assert validate_manifest(value) is value


@pytest.mark.parametrize("venue_contract", ["MYMH7", "MYMN6", "MYMZ5"])
def test_manifest_refuses_expired_nonquarterly_or_far_contract(venue_contract):
    with pytest.raises(CeremonyError):
        validate_manifest(manifest(venue_contract=venue_contract))


def _source_module():
    from c1_signal_daemon import operator_input_source
    return operator_input_source


def bar_record(**changes):
    from c1_signal_daemon.m1_stage1_control import digest
    record = {
        "schema_version": 1,
        "ceremony_id": "option-d-1",
        "boot_id": "boot-1",
        "venue_contract": "MYMZ6",
        "timestamp": "2026-09-10T14:00:00+00:00",
        "open": 44000.0,
        "high": 44002.0,
        "low": 43999.0,
        "close": 44001.0,
        "volume": 7.0,
    }
    record.update(changes)
    bar = {key: record[key] for key in
           ("timestamp", "open", "high", "low", "close", "volume", "venue_contract")}
    if "bar_sha256" not in record:
        numbers = [record[key] for key in ("open", "high", "low", "close", "volume")]
        try:
            representable = all(type(n) in (int, float) and math.isfinite(n)
                                for n in numbers)
        except OverflowError:
            representable = False
        record["bar_sha256"] = (digest({"bar": bar, "source": OPERATOR_SOURCE})
                                if representable else "e" * 64)
    return record


def write_record(path, **changes):
    path.write_text(json.dumps(bar_record(**changes)), encoding="utf-8")


def test_operator_source_inactive_binding_and_one_shot(tmp_path):
    mod = _source_module()
    source = mod.OperatorInputSource(tmp_path, boot_id="boot-1")
    assert source.poll() is None
    assert source.connected is False
    assert source.binding is None and source.ceremony_id is None
    with pytest.raises(CeremonyError):
        source.activate({"kind": "foreign"}, ceremony_id="option-d-1")
    source.activate(OPERATOR_SOURCE, ceremony_id="option-d-1")
    source.activate(OPERATOR_SOURCE.copy(), ceremony_id="option-d-1")
    published = tmp_path / "m1_bar_option-d-1.json"
    write_record(published)
    bar = source.poll()
    assert (bar.ts, bar.open, bar.high, bar.low, bar.close, bar.volume) == (
        datetime(2026, 9, 10, 14, tzinfo=timezone.utc), 44000.0, 44002.0,
        43999.0, 44001.0, 7.0)
    assert source.connected is True
    assert source.poll() is None
    assert source.connected is True


def test_operator_source_reactivation_discards_cached_bar(tmp_path):
    mod = _source_module()
    source = mod.OperatorInputSource(tmp_path, boot_id="boot-1")
    source.activate(OPERATOR_SOURCE, ceremony_id="option-d-1")
    write_record(tmp_path / "m1_bar_option-d-1.json")
    assert source.poll() is not None
    source.activate(OPERATOR_SOURCE, ceremony_id="option-d-2")
    assert source.connected is False
    assert source.ceremony_id == "option-d-2"
    assert source.poll() is None


def test_operator_source_deactivate_removes_bound_files(tmp_path):
    mod = _source_module()
    source = mod.OperatorInputSource(tmp_path, boot_id="boot-1")
    source.activate(OPERATOR_SOURCE, ceremony_id="option-d-1")
    for name in ("m1_bar_option-d-1.json", "m1_upload_option-d-1.json", "m1_claim_option-d-1"):
        (tmp_path / name).write_text("private", encoding="utf-8")
    source.deactivate()
    source.deactivate()
    assert source.connected is False
    assert source.binding is None and source.ceremony_id is None
    assert not any(tmp_path.iterdir())


@pytest.mark.parametrize("change", [
    {"ceremony_id": "wrong"},
    {"boot_id": "wrong"},
    {"bar_sha256": "f" * 64},
    {"open": float("nan")},
    {"high": float("inf")},
    {"low": -1.0},
    {"close": True},
    {"low": 44001.5},
    {"timestamp": "2026-09-10T14:00:00"},
    {"schema_version": 2},
    {"schema_version": True},
    {"open": 10 ** 400},
])
def test_operator_source_rejects_invalid_published_record(tmp_path, change, caplog):
    mod = _source_module()
    source = mod.OperatorInputSource(tmp_path, boot_id="boot-1")
    source.activate(OPERATOR_SOURCE, ceremony_id="option-d-1")
    write_record(tmp_path / "m1_bar_option-d-1.json", **change)
    with caplog.at_level(logging.WARNING):
        assert source.poll() is None
        assert source.poll() is None
    assert source.connected is False
    messages = [r.getMessage() for r in caplog.records]
    assert messages == ["operator_input: published bar rejected"]
    assert "44000" not in "".join(messages)


def test_operator_source_rejects_truncated_and_nonobject_json(tmp_path):
    mod = _source_module()
    source = mod.OperatorInputSource(tmp_path, boot_id="boot-1")
    source.activate(OPERATOR_SOURCE, ceremony_id="option-d-1")
    published = tmp_path / "m1_bar_option-d-1.json"
    for raw in ('{"schema_version":', '[]'):
        published.write_text(raw, encoding="utf-8")
        assert source.poll() is None


def test_cleanup_orphans_removes_only_operator_input_patterns(tmp_path):
    mod = _source_module()
    for name in ("m1_bar_a.json", "m1_upload_b.json", "m1_claim_c"):
        (tmp_path / name).write_text("private", encoding="utf-8")
    keep = tmp_path / "m1_state.json"
    keep.write_text("keep", encoding="utf-8")
    mod.cleanup_orphans(tmp_path)
    assert [p.name for p in tmp_path.iterdir()] == ["m1_state.json"]


def test_atomic_publication_race_never_raises_or_returns_partial_bar(tmp_path):
    mod = _source_module()
    source = mod.OperatorInputSource(tmp_path, boot_id="boot-1")
    source.activate(OPERATOR_SOURCE, ceremony_id="option-d-1")
    published = tmp_path / "m1_bar_option-d-1.json"
    temporary = tmp_path / "writer.tmp"
    raw = json.dumps(bar_record())

    def publish():
        with temporary.open("w", encoding="utf-8") as stream:
            stream.write(raw[:20])
            stream.flush()
            time.sleep(0.01)
            stream.write(raw[20:])
        os.replace(temporary, published)

    writer = threading.Thread(target=publish)
    writer.start()
    seen = []
    while writer.is_alive():
        seen.append(source.poll())
    writer.join()
    seen.append(source.poll())
    bars = [bar for bar in seen if bar is not None]
    assert len(bars) == 1
    assert bars[0].close == 44001.0
