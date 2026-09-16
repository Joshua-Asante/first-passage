"""Regression tests for scripts/guard_shell_command.py.

The guard was ported from `.cursor/hooks/before_shell.py` when the Cursor
harness was retired (`docs/adr/2026-07-14-cc-cursor-surface-allocation.md`,
Revision 2026-09-15). These tests pin the *logic* independently of any harness
wiring, so the discipline stays verifiable whether or not the operator elects to
register the PreToolUse hook. Retiring the Cursor carrier must not quietly
retire the rule it enforced.
"""
from __future__ import annotations

import importlib.util
import io
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
GUARD = REPO / "scripts" / "guard_shell_command.py"


def _load():
    spec = importlib.util.spec_from_file_location("guard_shell_command", GUARD)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def mod():
    return _load()


@pytest.mark.parametrize(
    "cmd",
    [
        "git commit --no-verify -m wip",
        "git commit -m x --no-gpg-sign",
        "git commit --no-verify --no-gpg-sign -m both",
    ],
)
def test_hook_bypass_asks(mod, cmd):
    """--no-verify is the one rule no git hook can enforce on itself."""
    permission, agent_msg, user_msg = mod.classify(cmd)
    assert permission == "ask"
    assert "standing path" in agent_msg
    assert user_msg


@pytest.mark.parametrize(
    "cmd",
    [
        "git reset --hard origin/main",
        "git clean -fd",
        "git clean -xdf",
        "git checkout -- .",
        "git push --force origin main",
        "git push origin main -f",
        "git branch -D feature",
        "rm -rf build/",
    ],
)
def test_destructive_asks(mod, cmd):
    permission, agent_msg, user_msg = mod.classify(cmd)
    assert permission == "ask"
    assert "git status" in agent_msg
    assert user_msg


@pytest.mark.parametrize(
    "cmd",
    [
        "git status",
        "git commit -m 'ordinary commit'",
        "git push origin my-branch",
        "git push --force-with-lease origin my-branch",
        "pytest tests/ -x",
        "rm build/artifact.o",
        "",
    ],
)
def test_benign_allows(mod, cmd):
    """Force-with-lease and a plain rm must not be swept up as destructive."""
    permission, agent_msg, user_msg = mod.classify(cmd)
    assert permission == "allow"
    assert agent_msg == ""
    assert user_msg == ""


@pytest.mark.parametrize(
    "payload,expected",
    [
        ({"command": "git status"}, "git status"),
        ({"shell_command": "ls"}, "ls"),
        ({"cmd": "pwd"}, "pwd"),
        ({"tool_input": {"command": "git diff"}}, "git diff"),
        ({"tool_input": {}}, ""),
        ({}, ""),
        ("not-a-dict", ""),
    ],
)
def test_command_extraction_accepts_both_payload_shapes(mod, payload, expected):
    """Cursor's beforeShellExecution shape and Claude's PreToolUse shape."""
    assert mod.command_of(payload) == expected


def test_malformed_stdin_fails_open(mod, monkeypatch, capsys):
    """Fail-open is the contract: a parse error must never block a command."""
    monkeypatch.setattr(sys, "stdin", io.StringIO("{not json"))
    assert mod.main() == 0
    out = json.loads(capsys.readouterr().out)
    assert out["hookSpecificOutput"]["permissionDecision"] == "allow"


def test_end_to_end_ask_via_stdin(mod, monkeypatch, capsys):
    monkeypatch.setattr(
        sys, "stdin", io.StringIO(json.dumps({"tool_input": {"command": "rm -rf /tmp/x"}}))
    )
    assert mod.main() == 0
    out = json.loads(capsys.readouterr().out)
    block = out["hookSpecificOutput"]
    assert block["permissionDecision"] == "ask"
    assert block["permissionDecisionReason"]
    assert block["additionalContext"]


def test_emits_claude_not_cursor_decision_shape(mod, monkeypatch, capsys):
    """The whole hook is inert if it emits Cursor's contract.

    The first draft of this port carried `.cursor/hooks/before_shell.py`'s
    `{"permission", "agentMessage", "userMessage"}` shape over verbatim. Claude
    Code reads `hookSpecificOutput.permissionDecision`, so that draft would have
    been a silent no-op once wired. Adversarial review caught it before wiring;
    this test is what stops it coming back.
    """
    monkeypatch.setattr(
        sys, "stdin", io.StringIO(json.dumps({"tool_input": {"command": "git status"}}))
    )
    assert mod.main() == 0
    out = json.loads(capsys.readouterr().out)
    assert set(out) == {"hookSpecificOutput"}, "top level must be hookSpecificOutput only"
    block = out["hookSpecificOutput"]
    assert block["hookEventName"] == "PreToolUse"
    assert block["permissionDecision"] in {"allow", "deny", "ask"}
    # Cursor's keys must not reappear at either level.
    for dead in ("permission", "agentMessage", "userMessage"):
        assert dead not in out
        assert dead not in block


def test_guard_is_actually_wired(mod):
    """An unwired gate nobody knows is unwired is a named failure class here.

    The guard was ported unwired, then registered at the operator's instruction.
    This pins that the registration exists and points at this script, so the
    discipline cannot be silently lost a second way.
    """
    settings = json.loads(
        (REPO / ".claude" / "settings.json").read_text(encoding="utf-8")
    )
    pre = settings.get("hooks", {}).get("PreToolUse", [])
    entries = [
        h.get("command", "")
        for group in pre
        if group.get("matcher") == "Bash"
        for h in group.get("hooks", [])
    ]
    assert any("guard_shell_command.py" in c for c in entries), (
        "guard_shell_command.py is not registered as a PreToolUse Bash hook"
    )
