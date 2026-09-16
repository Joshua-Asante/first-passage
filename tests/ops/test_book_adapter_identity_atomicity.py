"""Accepted adapter receipts must name the exact bytes that execute."""
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import py_compile
from types import SimpleNamespace

import pytest

from c1_signal_daemon import book_adapters


def _digest(data):
    return hashlib.sha256(data).hexdigest()


def _port(tmp_path, monkeypatch, *, value="NEW"):
    leg_id = "dj30_mym_p250"
    original = book_adapters.ADAPTER_BY_LEG[leg_id]
    source = (f"LEG_ID = {leg_id!r}\n"
              f"PINE_SHA256 = {original.pine_sha256!r}\n"
              f"VALUE = {value!r}\n").encode()
    path = tmp_path / f"{original.module}.py"
    path.write_bytes(source)
    monkeypatch.setenv("FP_PORT_ROOT", str(tmp_path))
    monkeypatch.setitem(
        book_adapters.ADAPTER_BY_LEG, leg_id,
        replace(original, runtime_sha256=_digest(source)))
    return leg_id, path, source


def test_unaccepted_port_is_rejected_before_its_top_level_code_executes(tmp_path, monkeypatch):
    marker = tmp_path / "executed.txt"
    leg_id, path, accepted = _port(tmp_path, monkeypatch)
    path.write_bytes(accepted +
                     f"from pathlib import Path\nPath({str(marker)!r}).write_text('ran')\n".encode())

    with pytest.raises(ValueError, match="accepted runtime identity"):
        book_adapters.load_port(leg_id)

    assert not marker.exists()


def test_verified_source_bytes_execute_without_timestamp_pyc_substitution(tmp_path, monkeypatch):
    leg_id, path, accepted = _port(tmp_path, monkeypatch)
    old = accepted.replace(b"'NEW'", b"'OLD'")
    path.write_bytes(old)
    py_compile.compile(str(path), doraise=True,
                       invalidation_mode=py_compile.PycInvalidationMode.TIMESTAMP)
    previous = path.stat()
    path.write_bytes(accepted)
    os.utime(path, ns=(previous.st_atime_ns, previous.st_mtime_ns))

    assert book_adapters.load_port(leg_id).VALUE == "NEW"


def test_effective_inputs_are_parsed_from_the_verified_snapshot(tmp_path, monkeypatch):
    path = tmp_path / "effective_inputs.json"
    accepted = {"_note": "synthetic identity fixture"}
    for row in book_adapters.ADAPTERS:
        accepted[row.leg_id] = {
            "adapter": {"sentinel": "accepted"}, "emulator": {}, "qty_scale": 1,
        }
    accepted_bytes = json.dumps(accepted).encode()
    changed = json.loads(accepted_bytes)
    for row in book_adapters.ADAPTERS:
        changed[row.leg_id]["adapter"]["sentinel"] = "changed"
    changed_bytes = json.dumps(changed).encode()
    path.write_bytes(accepted_bytes)
    monkeypatch.setenv("FP_PORT_ROOT", str(tmp_path))
    monkeypatch.setattr(book_adapters, "EFFECTIVE_INPUTS_SHA256", _digest(accepted_bytes))
    original_read = Path.read_bytes

    def read_then_change(source):
        data = original_read(source)
        if source == path:
            source.write_bytes(changed_bytes)
        return data

    monkeypatch.setattr(Path, "read_bytes", read_then_change)
    monkeypatch.setattr(book_adapters, "load_port", lambda leg_id: SimpleNamespace(
        build=lambda **values: SimpleNamespace(leg_id=leg_id, **values)))
    runtime_values = json.loads(accepted_bytes)
    runtime_values["orb_mnq_v7"]["adapter"]["qty"] = 1
    runtime_bytes = json.dumps(
        runtime_values, sort_keys=True, separators=(",", ":"), allow_nan=False,
    ).encode()
    monkeypatch.setattr(
        book_adapters, "RUNTIME_EFFECTIVE_INPUTS_SHA256", _digest(runtime_bytes))

    loaded = book_adapters.load_book_adapters()

    assert all(adapter.sentinel == "accepted" for adapter in loaded.values())
