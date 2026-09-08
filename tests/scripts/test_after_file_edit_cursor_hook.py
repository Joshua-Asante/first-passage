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


def test_adapter_surfaces_validator_failure(monkeypatch, capsys):
    mod = _load()
    recorded: list[Path] = []

    def _fake_run(script, payload, cwd):
        recorded.append(script)
        if script.name == "sync_skills_hook.py":
            sys.stderr.write("SKILL CHECK FAILED: check_skill_refs.py --all failed\n")
            sys.stderr.write("explicit release is pending\n")

    monkeypatch.setattr(mod, "_run_hook", _fake_run)
    stdin = sys.stdin
    try:
        sys.stdin = io.StringIO(json.dumps({
            "file_path": ".claude/skills/alpha/SKILL.md",
            "edits": [{"file_path": ".claude/skills/alpha/SKILL.md"}],
        }))
        assert mod.main() == 0
    finally:
        sys.stdin = stdin
    err = capsys.readouterr().err
    assert "SKILL CHECK FAILED" in err
    assert any(p.name == "sync_skills_hook.py" for p in recorded)
    assert any(p.name == "lock_event_hook.py" for p in recorded)


def test_adapter_unrelated_edit_still_invokes_hooks(monkeypatch):
    mod = _load()
    recorded: list[str] = []

    def _fake_run(script, payload, cwd):
        recorded.append(script.name)

    monkeypatch.setattr(mod, "_run_hook", _fake_run)
    stdin = sys.stdin
    try:
        sys.stdin = io.StringIO(json.dumps({"file_path": "docs/STATE.md", "edits": []}))
        assert mod.main() == 0
    finally:
        sys.stdin = stdin
    assert "lock_event_hook.py" in recorded
    assert "sync_skills_hook.py" in recorded
