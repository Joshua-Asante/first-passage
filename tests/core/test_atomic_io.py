"""Tests for core/lib/atomic_io.py — same-directory temp + os.replace writes —
and its remaining wiring site (core/dd_protection.save_state).

ops/accounts._save_all was retired with the multiplier spine (substrate Phase 2).
core/dd_protection_state.json remains the sole persistence layer for that tool;
the pre-fix direct `open(path, "w")` / `Path.write_text` writers could leave a
truncated file on a crash/interrupt mid-write — silent state loss. The helper
guarantees the target is either the old bytes or the complete new bytes, never
a prefix. The temp file lives in the target's own directory so os.replace never
crosses a volume boundary (cross-volume replace raises on Windows).
"""
from __future__ import annotations

import json

import pytest

from lib import atomic_io
from lib.atomic_io import atomic_write_text


# ── helper: success paths ──────────────────────────────────────────

def test_atomic_write_creates_file_with_content(tmp_path):
    target = tmp_path / "state.json"
    atomic_write_text(target, '{"a": 1}')
    assert target.read_text(encoding="utf-8") == '{"a": 1}'


def test_atomic_write_overwrites_existing(tmp_path):
    target = tmp_path / "state.json"
    target.write_text("OLD", encoding="utf-8")
    atomic_write_text(target, "NEW")
    assert target.read_text(encoding="utf-8") == "NEW"


def test_atomic_write_leaves_no_temp_residue(tmp_path):
    target = tmp_path / "state.json"
    atomic_write_text(target, "x")
    assert [p.name for p in tmp_path.iterdir()] == ["state.json"]


def test_atomic_write_accepts_str_path(tmp_path):
    # Wiring sites pass Path objects today, but the helper is the
    # designated repo-wide writer — pin the str-path convenience.
    target = tmp_path / "state.json"
    atomic_write_text(str(target), "x")
    assert target.read_text(encoding="utf-8") == "x"


# ── helper: failure mid-write must not touch the original ──────────

def test_atomic_write_failure_before_commit_leaves_original(tmp_path, monkeypatch):
    target = tmp_path / "state.json"
    target.write_text("ORIGINAL", encoding="utf-8")

    def boom(src, dst):
        raise OSError("simulated crash before commit")

    monkeypatch.setattr(atomic_io.os, "replace", boom)
    with pytest.raises(OSError, match="simulated crash"):
        atomic_write_text(target, "NEW CONTENT")
    assert target.read_text(encoding="utf-8") == "ORIGINAL"
    # temp file cleaned up on the failure path too
    assert [p.name for p in tmp_path.iterdir()] == ["state.json"]


def test_atomic_write_failure_during_write_leaves_original(tmp_path, monkeypatch):
    target = tmp_path / "state.json"
    target.write_text("ORIGINAL", encoding="utf-8")

    real_fdopen = atomic_io.os.fdopen

    class _BrokenWriter:
        def __init__(self, f):
            self._f = f

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return self._f.__exit__(*exc)

        def write(self, text):
            raise OSError("simulated disk-full mid-write")

    monkeypatch.setattr(
        atomic_io.os, "fdopen",
        lambda fd, *a, **kw: _BrokenWriter(real_fdopen(fd, *a, **kw)),
    )
    with pytest.raises(OSError, match="disk-full"):
        atomic_write_text(target, "NEW CONTENT")
    assert target.read_text(encoding="utf-8") == "ORIGINAL"
    assert [p.name for p in tmp_path.iterdir()] == ["state.json"]


# ── wiring: core/dd_protection.save_state ──────────────────────────

@pytest.fixture
def dd_state_file(tmp_path, monkeypatch):
    import dd_protection
    path = tmp_path / "dd_protection_state.json"
    monkeypatch.setattr(dd_protection, "STATE_FILE", path)
    return path


def test_dd_protection_save_state_roundtrips(dd_state_file):
    import dd_protection
    state = dd_protection._default_state()
    state["last_equity"] = 199_000.0
    dd_protection.save_state(state)
    assert dd_protection.load_state() == state
    assert json.loads(dd_state_file.read_text(encoding="utf-8")) == state


def test_dd_protection_save_state_failure_leaves_original(dd_state_file, monkeypatch):
    import dd_protection
    original = dd_protection._default_state()
    dd_protection.save_state(original)

    def boom(src, dst):
        raise OSError("simulated crash before commit")

    monkeypatch.setattr(atomic_io.os, "replace", boom)
    with pytest.raises(OSError, match="simulated crash"):
        dd_protection.save_state({"peak_equity": 0})
    assert dd_protection.load_state() == original


def test_dd_protection_load_rejects_non_finite_state(dd_state_file):
    import dd_protection

    dd_state_file.write_text(
        '{"starting_equity":200000,"peak_equity":200000,'
        '"last_equity":NaN,"history":[]}',
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="not strict JSON"):
        dd_protection.load_state()


def test_dd_protection_load_rejects_peak_below_last_equity(dd_state_file):
    import dd_protection

    dd_state_file.write_text(
        '{"starting_equity":200000,"peak_equity":200000,'
        '"last_equity":201000,"history":[]}',
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="peak_equity must be"):
        dd_protection.load_state()
