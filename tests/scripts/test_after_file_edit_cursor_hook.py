"""Regression tests for .cursor/hooks/after_file_edit.py (A16)."""
from __future__ import annotations

import importlib.util
import io
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
HOOK = REPO / ".cursor" / "hooks" / "after_file_edit.py"


def _load():
    spec = importlib.util.spec_from_file_location("after_file_edit", HOOK)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_repo_root_resolves_scripts_lock_hook():
    mod = _load()
    root = mod._repo_root()
    lock = root / "scripts" / "lock_event_hook.py"
    assert lock.is_file(), f"expected {lock} (repo root={root})"
    assert (root / "scripts" / "sync_skills_hook.py").is_file()


def test_run_hook_loud_miss_on_missing_script(capsys):
    mod = _load()
    missing = Path("/nonexistent/lock_event_hook.py")
    mod._run_hook(missing, {"tool_input": {}}, REPO)
    err = capsys.readouterr().err
    assert "MISSING HOOK" in err
    assert "did NOT run" in err


def test_main_fail_open_on_bad_stdin():
    mod = _load()
    stdin = sys.stdin
    try:
        sys.stdin = io.StringIO("not json")
        assert mod.main() == 0
    finally:
        sys.stdin = stdin
