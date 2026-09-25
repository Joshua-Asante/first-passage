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
SHA = "0123456789abcdef0123456789abcdef01234567"
PIN = f"--match-head-commit {SHA}"


@pytest.mark.parametrize("command", [
    f"{MERGE} 501 --squash {PIN}",
    f"{MERGE} --repo Joshua-Asante/first-passage 501 --match-head-commit={SHA}",
    f"gh -R Joshua-Asante/first-passage pr merge 501 {PIN}",
    f"cd /repo && {MERGE} 501 {PIN}",
    f"bash -c '{MERGE} 501 {PIN}'",
    "gh api -X PUT repos/o/r/pulls/501/" + f"merge -f sha={SHA}",
    "gh api graphql -f query='mutation { merge" + f"PullRequest(input: {{expectedHeadOid: \"{SHA}\"}}) {{ x }} }}'",
])
def test_pinned_merge_asks(command):
    # Fails if a merge pinned to a head SHA runs without an operator prompt.
    assert g.classify_command(command) == ("ask", "pr.merge")


@pytest.mark.parametrize("command", [
    f"{MERGE} 501 --squash",
    f"{MERGE} 501 --match-head-commit abc123",
    f"bash -c '{MERGE} 501'",
    "gh api -X PUT repos/o/r/pulls/501/" + "merge",
    "gh api graphql -f query='mutation { merge" + "PullRequest(input: {}) { x } }'",
])
def test_unpinned_merge_denied(command):
    # Fails if an approval could merge bytes other than the head the operator saw
    # (Astra finding 2, PR #503 at 72c435c).
    assert g.classify_command(command) == ("deny", "pr.merge_unpinned")


@pytest.mark.parametrize("command", [
    f"bash -c '{MERGE} 501 {PIN}; {MERGE} 502 --auto'",
    f"{MERGE} 501 {PIN} && {MERGE} 502 --auto",
    f"sh -c '{DEPLOY}; {MERGE} 502 --auto'",
])
def test_deny_wins_over_ask_in_one_command(command):
    # Fails if a promptable act earlier in a command launders a forbidden one after it
    # (Astra finding 1, PR #503 at 72c435c).
    assert g.classify_command(command) == ("deny", "pr.auto_merge")


@pytest.mark.parametrize("command", [
    f"{MERGE} 501 --auto --squash",
    "gh api graphql -f query='mutation { enablePullRequest" + "AutoMerge(input: {}) { x } }'",
])
def test_auto_merge_denied(command):
    # Fails if auto-merge (retired, no automated exception) is merely asked, not refused.
    assert g.classify_command(command) == ("deny", "pr.auto_merge")


def test_mcp_tools():
    # Fails if the GitHub MCP merge path bypasses the operator, or auto-merge is askable.
    merge = "mcp__github__merge_pull_request"
    assert g.classify({"tool_name": merge, "tool_input": {"expectedHeadSha": SHA}}) == (
        "ask", "pr.merge")
    assert g.classify({"tool_name": merge, "tool_input": {}}) == ("deny", "pr.merge_unpinned")
    assert g.classify({"tool_name": merge, "tool_input": {"expectedHeadSha": "abc"}}) == (
        "deny", "pr.merge_unpinned")
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


@pytest.mark.parametrize("command", [
    "git push origin main",
    "git push origin HEAD:main",
    "git push -u origin +feature:refs/heads/main",
    "git push origin --delete main",
    "git -C /repo push origin main",
    "git push origin claude/x main",
])
def test_push_to_main_denied(command):
    # Fails if a direct push to main, a merge-equivalent that bypasses the PR and the
    # required status, gets through (Fable review of #503, finding A).
    assert g.classify_command(command) == ("deny", "main.direct_push")


@pytest.mark.parametrize("command", [
    "git push -u origin claude/bold-shannon-cc2xmr",
    "git push origin HEAD:refs/heads/claude/x",
    "git push origin main:claude/backup",
    "git fetch origin main",
    "git push",
])
def test_other_pushes_are_silent(command):
    # Fails if a branch push, or a push whose destination is not main, prompts.
    assert g.classify_command(command) is None


def test_unreadable_command_fails_closed():
    # Fails if an unterminated quote hides a merge from the guard (unreadable text cannot
    # prove a pin, so it is refused as unpinned).
    assert g.classify_command(f"{MERGE} 501 'unterminated")[0] == "deny"


def _run(payload) -> str:
    return subprocess.run([sys.executable, str(GUARD)], input=payload,
                          capture_output=True, text=True, check=True).stdout


def test_hook_contract():
    # Fails if the hook emits a non-PreToolUse shape, or emits anything (an allow) on
    # benign input, or blocks on malformed input.
    out = json.loads(_run(json.dumps({"tool_name": "mcp__github__merge_pull_request",
                                      "tool_input": {"expectedHeadSha": SHA}})))
    block = out["hookSpecificOutput"]
    assert block["hookEventName"] == "PreToolUse"
    assert block["permissionDecision"] == "ask"
    assert SHA in block["permissionDecisionReason"]  # the operator sees what they approve
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
