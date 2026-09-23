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
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
GUARD = REPO / "scripts" / "guard_shell_command.py"
# Destructive words are built by concatenation so no test source line is itself
# a command a shell guard would stop on.
RMRF, HARD, NOV, FORCE = "rm " + "-rf", "git reset " + "--hard", "--no-" + "verify", "--for" + "ce"


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
    """Fail-open is the contract: a parse error must never block a command.

    2026-09-23: fail-open no longer means emitting `allow` — a hook `allow`
    bypasses the operator's permission rules — so unparsable input now
    produces no output at all and defers to the normal permission flow.
    """
    monkeypatch.setattr(sys, "stdin", io.StringIO("{not json"))
    assert mod.main() == 0
    assert capsys.readouterr().out.strip() == ""


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
    this test is what stops it coming back. It exercises a command that asks
    (`rm -rf`), because a benign command now produces no output at all (D15).
    """
    monkeypatch.setattr(
        sys, "stdin", io.StringIO(json.dumps({"tool_input": {"command": "rm -rf /tmp/x"}}))
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


# --- 2026-09-23 card 2 (E1-E3): commands, not text -----------------------------
# The acceptance suite (tests/test_harness_guards_acceptance.py) pins the card's
# cases; these pin how the strict tokenizer reads the neighbouring spellings.

@pytest.mark.parametrize(
    "cmd",
    [
        # a flag after a command substitution stays in its command
        f"git commit -m \"$(cat <<'EOF'\nfix: it's (F29)\nEOF\n)\" {NOV}",
        f"git push origin \"$(git branch --show-current)\" {FORCE}",
        # substitutions anywhere in a double-quoted word run
        f"echo \"cleaning $({RMRF} build)\"",
        f"echo \"x `{RMRF} build` y\"",
        # runners whose arguments are a command
        f"find . -name '*.pyc' -exec {RMRF} {{}} +",
        f"ls | xargs -n1 {RMRF}",
        f"eval '{RMRF} d'",
        f"{{ {RMRF} d; }}",
        f"sudo -u root {RMRF} d",
        f"timeout -s KILL 5 {HARD}",
        f"nice -n 5 {RMRF} d",
        f"bash -ec '{HARD}'",
        f"X=1 bash -c 'Y=2 {HARD}'",
        f"cat <<< 'x'\n{RMRF} d",  # a here-string is not a heredoc
        # abbreviations git 2.43 accepts for the guarded long options
        "git clean --f", "git checkout --forc", "git restore --staged --w f",
        "git switch --disc x", "git branch --d --forc x", "rm --r --f d",
        # option values are not flags: -s takes "S", so this restores the work tree
        "git restore -sS f",
        "git checkout -fb x",
    ],
)
def test_strict_reading_still_asks(mod, cmd):
    """Spellings the shell or git would run as a destructive operation still ask."""
    assert mod.classify(cmd)[0] == "ask", cmd


@pytest.mark.parametrize(
    "cmd",
    [
        f"git commit -m \"$(cat <<'EOF'\ndon't {RMRF} (ever\nEOF\n)\"",
        f"gh pr create --body \"$(cat <<'EOF'\nNever `{RMRF}`; don't {NOV}.\nEOF\n)\"",
        f"echo 'x `{RMRF} build` y'",
        f"cat <<< '{RMRF} d'\necho ok",
        f"# {RMRF}\necho ok",
        f"git log --oneline | grep '{FORCE}'",
        "command -v rm",
        "git commit -mn",                 # -m with the message "n"
        "git commit -uno -m x",           # -u with the mode "no"
        "git commit -m x -- -n",          # after --, -n is a path
        "git -c core.editor=vim commit -m x",
        "git checkout -bfix",
        "git switch -c fix",
        "git restore --staged --no-worktree f",
        "git push -o +x origin main",     # a push option, not a refspec
        "git push --force-with-lease --force-if-includes origin x",
        "rm -r -- -f",                    # after --, -f is a path
    ],
)
def test_strict_reading_allows(mod, cmd):
    """Data, lookups and option values never read as a guarded command (F29)."""
    assert mod.classify(cmd)[0] == "allow", cmd


@pytest.mark.parametrize(
    "cmd",
    [
        "git commit -qn -m x",
        "git --config-env=core.hooksPath=HP commit -m x",
        "git -c core.hooksPath commit -m x",
        "git commit --no-g -m x",
        f"git rebase {NOV} main",
    ],
)
def test_strict_reading_finds_bypasses(mod, cmd):
    """Clusters, config options and abbreviations that skip hooks ask (E2)."""
    permission, agent_msg, _ = mod.classify(cmd)
    assert permission == "ask" and "standing path" in agent_msg, cmd


@pytest.mark.parametrize(
    "command,expected",
    [
        (f"cat > p.py <<'EOF'\nx = '{RMRF} /'\nEOF", None),
        ("git commit -n -m x", "ask"),
    ],
)
def test_hook_runs_as_a_script(command, expected):
    """The §4 live smoke, run the way Claude Code runs the hook (script path, stdin)."""
    result = subprocess.run(
        [sys.executable, str(GUARD)], input=json.dumps({"tool_input": {"command": command}}),
        capture_output=True, text=True, encoding="utf-8", cwd=REPO, check=False, timeout=30,
    )
    assert result.returncode == 0, result.stderr
    if expected is None:
        assert result.stdout == ""
    else:
        assert json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"] == expected
