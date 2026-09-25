"""Acceptance tests for scripts/guard_operator_acts.py.

Rule owner: docs/adr/2026-07-14-cc-cursor-surface-allocation.md §Decision, "Action
classes and the authority block" (2026-09-25 revision). Operator acts ask; forbidden
acts deny; data that merely mentions them, and risk-reducing exits, stay silent.
Command words are built by concatenation so no test source line is itself a command
a shell guard would stop on.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
GUARD = REPO / "scripts" / "guard_operator_acts.py"
sys.path.insert(0, str(REPO))
from scripts import guard_operator_acts as g  # noqa: E402

MERGE = "gh pr " + "merge"
DEPLOY = "fly " + "deploy"
ARM = "python ops/c1_rail/c1_rail_arm.py --" + "arm"


@pytest.mark.parametrize("command", [
    f"{MERGE} 501 --squash",
    f"{MERGE} --repo Joshua-Asante/first-passage 501",
    f"gh -R Joshua-Asante/first-passage pr merge 501",
    f"cd /repo && {MERGE} 501",
    f"bash -c '{MERGE} 501'",
    "gh api -X PUT repos/o/r/pulls/501/" + "merge",
])
def test_merge_asks(command):
    # Fails if an agent can merge by shell without an operator prompt.
    assert g.classify_command(command) == ("ask", "pr.merge")


@pytest.mark.parametrize("command", [
    f"{MERGE} 501 --auto --squash",
    "gh api graphql -f query='mutation { enablePullRequest" + "AutoMerge(input: {}) { x } }'",
])
def test_auto_merge_denied(command):
    # Fails if auto-merge (retired, no automated exception) is merely asked, not refused.
    assert g.classify_command(command) == ("deny", "pr.auto_merge")


def test_mcp_tools():
    # Fails if the GitHub MCP merge path bypasses the operator, or auto-merge is askable.
    assert g.classify({"tool_name": "mcp__github__merge_pull_request"}) == ("ask", "pr.merge")
    assert g.classify({"tool_name": "mcp__github__enable_pr_auto_merge"}) == (
        "deny", "pr.auto_merge")
    assert g.classify({"tool_name": "mcp__github__pull_request_read"}) is None


@pytest.mark.parametrize("command", [
    f"{DEPLOY} -a c1-rail",
    "flyctl -a c1-rail " + "deploy --image x",
])
def test_rail_deploy_asks(command):
    # Fails if a c1 rail deploy can run without an operator prompt.
    assert g.classify_command(command) == ("ask", "rail.deploy")


@pytest.mark.parametrize("command", [
    f"{ARM} --hours 4",
    "python3 -m ops.c1_rail.c1_rail_arm --" + "arm",
    "fly ssh console -a c1-rail -C '" + ARM + "'",
])
def test_arm_asks(command):
    # Fails if arming the rail can run without an operator prompt.
    assert g.classify_command(command) == ("ask", "rail.arm")


@pytest.mark.parametrize("command", [
    "python ops/c1_rail/c1_rail_arm.py --disarm",
    "python ops/c1_rail/c1_rail_arm.py --status",
    "fly ssh console -a c1-rail -C 'python ops/c1_rail/c1_rail_arm.py --disarm'",
    "fly status -a c1-rail",
    "gh pr view 501",
    "gh pr create --title 'do not " + MERGE + " yet' --body x",
    f"git commit -m 'document {MERGE} and {DEPLOY}'",
    f"grep -rn '{MERGE}' docs/",
    f"echo '{ARM}'",
])
def test_data_and_risk_reducing_exits_are_silent(command):
    # Fails if disarm/status waits on a prompt, or if text that only mentions an act asks
    # (a background agent has nobody to answer a prompt — guard_shell_command F29).
    assert g.classify_command(command) is None


def test_unreadable_command_falls_back_to_asking():
    # Fails if an unterminated quote hides a merge from the guard.
    assert g.classify_command(f"{MERGE} 501 'unterminated") == ("ask", "pr.merge")


def _run(payload) -> str:
    return subprocess.run([sys.executable, str(GUARD)], input=payload,
                          capture_output=True, text=True, check=True).stdout


def test_hook_contract():
    # Fails if the hook emits a non-PreToolUse shape, or emits anything (an allow) on
    # benign input, or blocks on malformed input.
    out = json.loads(_run(json.dumps({"tool_name": "mcp__github__merge_pull_request",
                                      "tool_input": {}})))
    block = out["hookSpecificOutput"]
    assert block["hookEventName"] == "PreToolUse"
    assert block["permissionDecision"] == "ask"
    assert _run(json.dumps({"tool_name": "Bash", "tool_input": {"command": "ls"}})) == ""
    assert _run("not json") == ""


def test_settings_wire_the_hook():
    # Fails if the hook is not registered for both the Bash and the MCP merge tools.
    settings = json.loads((REPO / ".claude" / "settings.json").read_text())
    wired = [(e["matcher"], h["command"]) for e in settings["hooks"]["PreToolUse"]
             for h in e["hooks"]]
    ours = [m for m, c in wired if "guard_operator_acts.py" in c]
    assert "Bash" in ours
    assert any("merge_pull_request" in m and "enable_pr_auto_merge" in m for m in ours)
