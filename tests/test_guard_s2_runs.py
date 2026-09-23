"""S2 run guard: refuse a push that would cancel a PR run, and a redundant full dispatch."""
import io
import json

import pytest

from scripts import guard_s2_runs as guard

SHA = "a" * 40
OTHER = "b" * 40


def run(**fields):
    base = {"databaseId": 1, "headSha": SHA, "status": "completed", "conclusion": "success",
            "event": "pull_request", "displayTitle": "Qualification S2 supervision (x)"}
    return {**base, **fields}


# --- pure decisions ---------------------------------------------------------

@pytest.mark.parametrize("status", sorted(guard.IN_FLIGHT))
def test_push_refused_while_pull_request_run_in_flight(status):
    reason = guard.push_refusal("feat", [run(status=status, conclusion=None, databaseId=7)])
    assert reason and "7" in reason and guard.OVERRIDE in reason


@pytest.mark.parametrize("runs", [
    [],
    [run()],                                                     # finished
    [run(status="in_progress", conclusion=None, event="workflow_dispatch")],  # own concurrency group
])
def test_push_allowed_when_no_pull_request_run_would_be_cancelled(runs):
    assert guard.push_refusal("feat", runs) is None


@pytest.mark.parametrize("prior,refused", [
    (run(status="in_progress", conclusion=None), True),
    (run(conclusion="success"), True),
    (run(conclusion="failure"), True),
    (run(conclusion="cancelled"), False),
    (run(conclusion="skipped"), False),
    (run(conclusion="failure", headSha=OTHER), False),          # different bytes
    (run(conclusion="failure", displayTitle="S2 DIAGNOSTIC (deadline)"), False),
])
def test_full_dispatch_refused_only_on_same_sha_live_or_definitive(prior, refused):
    assert (guard.dispatch_refusal(SHA, [prior], diagnostic=False) is not None) is refused


def test_diagnostic_dispatch_is_never_refused():
    assert guard.dispatch_refusal(SHA, [run(conclusion="failure")], diagnostic=True) is None


def test_failed_run_refusal_points_at_root_cause_and_diagnostic_mode():
    reason = guard.dispatch_refusal(SHA, [run(conclusion="failure", databaseId=9)], diagnostic=False)
    assert "finding, not a re-roll" in reason and "cases=" in reason


# --- parsing ----------------------------------------------------------------

@pytest.mark.parametrize("command,expected", [
    ("git push -u origin feat", ["feat"]),
    ("git push origin HEAD:refs/heads/feat", ["feat"]),
    ("git push --force-with-lease origin +feat:feat", ["feat"]),
    ("git push", []),
    ("git push -u origin HEAD", []),
    ("git -C /repo push -o ci.skip origin feat", ["feat"]),
    ("git log --grep push", None),
    ("git commit -m push", None),
    ("git -c push.default=current status", None),
])
def test_push_destinations(command, expected):
    (tokens,) = guard._segments(command)
    assert guard._git_push_branches(tokens) == expected


@pytest.mark.parametrize("command,expected", [
    ("gh workflow run qualification-s2-supervision.yml --ref feat", ("feat", False)),
    ("gh workflow run qualification-s2-supervision --ref=feat", ("feat", False)),
    ("gh workflow run qualification-s2-supervision.yml -r feat -f cases='deadline and not oom'", ("feat", True)),
    ("gh workflow run qualification-s2-supervision.yml --ref feat -f cases=", ("feat", False)),
    ("gh workflow run other.yml --ref feat", None),
    ("gh run list", None),
])
def test_dispatch_parsing(command, expected):
    (tokens,) = guard._segments(command)
    assert guard._gh_dispatch(tokens) == expected


# --- entry points -----------------------------------------------------------

@pytest.fixture
def live_pr_run(monkeypatch):
    monkeypatch.setattr(guard, "_runs", lambda branch: [run(status="in_progress", conclusion=None)])
    monkeypatch.setattr(guard, "_current_branch", lambda: "feat")
    monkeypatch.setattr(guard, "_remote_sha", lambda ref: SHA)


def hook(command):
    out = io.StringIO()
    stdin = io.StringIO(json.dumps({"tool_input": {"command": command}}))
    import sys
    real, sys.stdout = sys.stdout, out
    try:
        assert guard.claude_hook(stdin) == 0
    finally:
        sys.stdout = real
    return json.loads(out.getvalue())["hookSpecificOutput"]


@pytest.mark.usefixtures("live_pr_run")
@pytest.mark.parametrize("command", [
    "git add -A && git commit -m x && git push -u origin feat",
    "git push",
    "gh workflow run qualification-s2-supervision.yml --ref feat",
])
def test_claude_hook_denies(command):
    assert hook(command)["permissionDecision"] == "deny"


@pytest.mark.usefixtures("live_pr_run")
@pytest.mark.parametrize("command", [
    "FP_S2_GUARD=off git push -u origin feat",
    "git status && git log -1",
    "gh workflow run qualification-s2-supervision.yml --ref feat -f cases=deadline",
])
def test_claude_hook_allows(command):
    assert hook(command)["permissionDecision"] == "allow"


def test_claude_hook_fails_open_without_gh(monkeypatch):
    monkeypatch.setattr(guard, "_run", lambda cmd: None)  # gh/git absent or offline
    assert hook("git push -u origin feat")["permissionDecision"] == "allow"
    assert guard.claude_hook(io.StringIO("not json")) == 0


def test_pre_push_refuses_and_honours_override(live_pr_run, monkeypatch, capsys):
    line = f"refs/heads/feat {SHA} refs/heads/feat {OTHER}\n"
    assert guard.pre_push(io.StringIO(line)) == 1
    assert "FP_S2_GUARD=off" in capsys.readouterr().err
    monkeypatch.setenv("FP_S2_GUARD", "off")
    assert guard.pre_push(io.StringIO(line)) == 0


def test_pre_push_ignores_branch_deletion_and_tags(live_pr_run):
    lines = f"(delete) {'0' * 40} refs/heads/feat {OTHER}\nrefs/tags/v1 {SHA} refs/tags/v1 {'0' * 40}\n"
    assert guard.pre_push(io.StringIO(lines)) == 0
