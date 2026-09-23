"""S2 run guard: unit pins for the pure decisions, the parser and the entry points.

Rewritten for the 2026-09-23 hardening (docs/briefs/handoffs/
2026-09-23-guard-s2-runs-hardening.md). The pre-hardening suite encoded
behavior that card's §3 found defective — most notably the "s3 covers s2"
coverage lattice and the hook's `allow` output — so those rows are gone and
every change is listed in the handoff §7 supersession list. The integration
coverage, including every spelling the parser must accept, lives in the frozen
acceptance suite (tests/test_guard_s2_runs_acceptance.py); this file pins the
pure functions and the entry points one level up from its `_run` seam.
"""
import io
import json
import sys

import pytest

from scripts import guard_s2_runs as guard

SHA = "a" * 40
OTHER = "b" * 40


def run(**fields):
    base = {"databaseId": 1, "headSha": SHA, "status": "completed", "conclusion": "success",
            "event": "workflow_dispatch", "displayTitle": "Qualification S2 supervision [s3] (feat)"}
    return {**base, **fields}


# --- pure decisions: pushes (D3) ---------------------------------------------

@pytest.mark.parametrize("status", sorted(guard.IN_FLIGHT))
def test_push_refused_while_an_open_prs_run_is_in_flight(status):
    reason = guard.push_refusal(
        "feat", [run(event="pull_request", status=status, conclusion=None, databaseId=7,
                    displayTitle="Qualification S2 supervision [s3] (462/merge)")],
        open_numbers={"462"})
    assert reason and "7" in reason and guard.OVERRIDE in reason


def test_push_allowed_when_the_live_runs_pr_is_closed():
    prior = run(event="pull_request", status="in_progress", conclusion=None,
                displayTitle="Qualification S2 supervision [s3] (459/merge)")
    assert guard.push_refusal("feat", [prior], open_numbers=set()) is None


def test_push_refused_when_the_pr_list_lookup_fails():
    prior = run(event="pull_request", status="in_progress", conclusion=None,
                displayTitle="Qualification S2 supervision [s3] (459/merge)")
    assert guard.push_refusal("feat", [prior], open_numbers=None)


def test_untitled_live_pr_run_counts_while_any_pr_is_open():
    prior = run(event="pull_request", status="in_progress", conclusion=None,
                displayTitle="Some PR title")
    assert guard.push_refusal("feat", [prior], open_numbers={"462"})
    assert guard.push_refusal("feat", [prior], open_numbers=set()) is None


def test_push_with_no_live_runs_is_always_allowed():
    assert guard.push_refusal("feat", [], open_numbers={"462"}) is None


# --- pure decisions: dispatch cancellation (D4) --------------------------------

def test_full_dispatch_refused_while_a_full_dispatch_run_is_live():
    prior = run(status="in_progress", conclusion=None)
    reason = guard.dispatch_cancel_refusal("feat", [prior], diagnostic=False)
    assert reason and "cancel" in reason


def test_diagnostic_and_full_dispatches_are_separate_groups():
    live = [run(status="in_progress", conclusion=None,
                displayTitle="S2 DIAGNOSTIC [s3] (deadline)")]
    assert guard.dispatch_cancel_refusal("feat", live, diagnostic=False) is None
    assert guard.dispatch_cancel_refusal("feat", live, diagnostic=True)


def test_pull_request_runs_never_reach_the_dispatch_decision():
    # The caller queries --event workflow_dispatch; a PR run in the list is a
    # different event and is filtered before the pure decision runs.
    assert guard.dispatch_cancel_refusal("feat", [], diagnostic=False) is None


# --- pure decisions: dispatch redundancy (D5) ----------------------------------

@pytest.mark.parametrize("prior_mode,status,conclusion,requested,refused", [
    ("s3", "completed", "success", "s3", True),
    ("s3", "completed", "failure", "s3", True),
    ("s2", "completed", "success", "s2", True),
    ("s2", "completed", "failure", "s2", True),
    ("s3", "completed", "success", "s2", False),   # s3 runs on the v5 install, never v4
    ("s3", "completed", "failure", "s2", False),
    ("s2", "completed", "success", "s3", False),   # s2 and s3 are incomparable
    ("s2", "completed", "failure", "s3", False),
    ("s3", "completed", "cancelled", "s3", False),
    ("s3", "completed", "skipped", "s3", False),
])
def test_redundancy_compares_bytes_and_mode_only(prior_mode, status, conclusion,
                                                 requested, refused):
    prior = run(status=status, conclusion=conclusion,
                displayTitle=f"Qualification S2 supervision [{prior_mode}] (feat)")
    reason = guard.dispatch_redundancy_refusal(SHA, [prior], mode=requested)
    assert (reason is not None) is refused


@pytest.mark.parametrize("prior", [
    run(displayTitle="Qualification S2 supervision (feat)"),          # no mode recorded
    run(displayTitle="Qualification S2 supervision s3 (feat)"),       # unbracketed mode
    run(headSha=OTHER),                                               # different bytes
    run(displayTitle="S2 DIAGNOSTIC [s3] (deadline)"),                # never coverage
    run(event="pull_request",
        displayTitle="Qualification S2 supervision [s3] (462/merge)"),  # merge-ref bytes
])
def test_incomplete_or_foreign_runs_are_not_coverage(prior):
    assert guard.dispatch_redundancy_refusal(SHA, [prior], mode="s3") is None


def test_the_newest_definitive_same_mode_run_decides():
    older = run(conclusion="failure", databaseId=1, createdAt="2026-09-23T01:00:00Z")
    newer = run(conclusion="success", databaseId=2, createdAt="2026-09-23T02:00:00Z")
    assert "passed" in guard.dispatch_redundancy_refusal(SHA, [older, newer], mode="s3")
    older, newer = (dict(older, conclusion="success"), dict(newer, conclusion="failure"))
    assert "re-roll" in guard.dispatch_redundancy_refusal(SHA, [older, newer], mode="s3")


def test_failure_refusal_points_at_root_cause_and_a_runnable_diagnostic():
    reason = guard.dispatch_redundancy_refusal(SHA, [run(conclusion="failure", databaseId=9)],
                                               mode="s3")
    assert "re-roll" in reason
    assert "-f mode=s3 -f cases=" in reason
    assert f"{guard.OVERRIDE} gh workflow run" in reason


# --- pure decisions: reruns (D11) ----------------------------------------------

@pytest.mark.parametrize("conclusion,refused", [("success", True), ("failure", True),
                                                ("cancelled", False)])
def test_rerun_of_a_definitive_full_run_is_a_re_roll(conclusion, refused):
    view = run(conclusion=conclusion, databaseId=101)
    assert (guard.rerun_refusal(view, [view]) is not None) is refused


def test_rerun_that_would_cancel_a_live_run_of_the_same_group_is_refused():
    view = run(conclusion="cancelled", databaseId=101)
    live = run(status="in_progress", conclusion=None, databaseId=102)
    assert guard.rerun_refusal(view, [live])
    live_diagnostic = dict(live, displayTitle="S2 DIAGNOSTIC [s3] (deadline)")
    assert guard.rerun_refusal(view, [live_diagnostic]) is None


def test_rerun_of_a_pr_run_cancels_only_the_same_pr():
    view = run(event="pull_request", conclusion="cancelled", databaseId=201,
               displayTitle="Qualification S2 supervision [s3] (462/merge)")
    same = run(event="pull_request", status="in_progress", conclusion=None, databaseId=202,
               displayTitle="Qualification S2 supervision [s3] (462/merge)")
    other = run(event="pull_request", status="in_progress", conclusion=None, databaseId=203,
                displayTitle="Qualification S2 supervision [s3] (459/merge)")
    assert guard.rerun_refusal(view, [same])
    assert guard.rerun_refusal(view, [other]) is None


# --- parsing ----------------------------------------------------------------

@pytest.mark.parametrize("command,expected", [
    ('git commit -m "a; git push origin feat"', [["git", "commit", "-m",
                                                 "a; git push origin feat"]]),
    ("cat > notes.md <<'EOF'\ngit push origin feat\nEOF", [["cat"]]),
    ("git push -u origin HEAD 2>&1 | tail -5",
     [["git", "push", "-u", "origin", "HEAD"], ["tail", "-5"]]),
    ("echo hi\ngit push origin feat", [["echo", "hi"], ["git", "push", "origin", "feat"]]),
    ("git push -u origin \\\n  feat", [["git", "push", "-u", "origin", "feat"]]),
    ("out=$(git push origin feat 2>&1)", [["out=$(git push origin feat 2>&1)"],
                                          ["git", "push", "origin", "feat"]]),
    ("git push origin wip:feat $BRANCH", [["git", "push", "origin", "wip:feat", "$BRANCH"]]),
])
def test_segments_are_quote_and_heredoc_aware(command, expected):
    assert guard._segments(command) == expected


@pytest.mark.parametrize("args,mode,expected", [
    (["-u", "origin", "feat"], "specs", [("feat", "feat")]),
    (["origin", "HEAD:refs/heads/feat"], "specs", [("refs/heads/feat", "HEAD")]),
    (["--force-with-lease", "origin", "+feat:feat"], "specs", [("feat", "feat")]),
    ([], "specs", [("", "")]),
    (["-o", "ci.skip", "origin", "feat"], "specs", [("feat", "feat")]),
    (["origin", "wip", "feat"], "specs", [("wip", "wip"), ("feat", "feat")]),
    (["--delete", "origin", "feat"], "none", []),
    (["-d", "origin", "feat"], "none", []),
    (["origin", ":feat"], "specs", []),  # a deletion refspec updates nothing
    (["--tags"], "none", []),
    (["-n", "origin", "feat"], "none", []),
    (["--all", "origin"], "all", []),
    (["--mirror", "origin"], "all", []),
])
def test_push_specs(args, mode, expected):
    assert guard._push_specs(args) == (mode, expected)


@pytest.mark.parametrize("command,ref,fields,json_inputs", [
    ("gh workflow run qualification-s2-supervision.yml --ref feat", "feat", {}, False),
    ("gh workflow run qualification-s2-supervision --ref=feat", "feat", {}, False),
    ("gh workflow run qualification-s2-supervision.yml -rfeat", "feat", {}, False),
    ("gh workflow run qualification-s2-supervision.yml -r=feat", "feat", {}, False),
    ("gh workflow run qualification-s2-supervision.yml --ref refs/heads/feat",
     "refs/heads/feat", {}, False),
    ("gh workflow run 362153971 --ref feat", "feat", {}, False),
    ("gh workflow run 'qualification s2 supervision' --ref feat", "feat", {}, False),
    ("gh workflow run .github/workflows/qualification-s2-supervision.yml --ref feat",
     "feat", {}, False),
    ("gh workflow run qualification-s2-supervision.yml --ref feat -f cases='deadline and not oom'",
     "feat", {"cases": "deadline and not oom"}, False),
    ("gh workflow run qualification-s2-supervision.yml --ref feat -f cases=",
     "feat", {"cases": ""}, False),
    ("gh workflow run qualification-s2-supervision.yml --ref feat -f mode=s2",
     "feat", {"mode": "s2"}, False),
    ("gh workflow run qualification-s2-supervision.yml --field=mode=s2 --ref feat",
     "feat", {"mode": "s2"}, False),
    ("gh workflow run qualification-s2-supervision.yml -f mode=s2 -f cases=deadline",
     "", {"mode": "s2", "cases": "deadline"}, False),
    ("gh workflow run qualification-s2-supervision.yml --json", "", {}, True),
])
def test_dispatch_parsing(command, ref, fields, json_inputs):
    parsed = guard._parse_dispatch(guard._segments(command)[0])
    assert parsed == {"ref": ref, "fields": fields, "json": json_inputs, "repo": None}


@pytest.mark.parametrize("command", [
    "gh workflow run other.yml --ref feat",
    "gh workflow run tests.yml --ref feat",
    "gh run list",
    "gh workflow list",
])
def test_other_workflow_commands_are_not_dispatches(command):
    assert all(guard._parse_dispatch(tokens) is None
               for tokens in guard._segments(command))


# --- entry points -----------------------------------------------------------

@pytest.fixture
def live_pr(monkeypatch):
    live = [run(event="pull_request", status="in_progress", conclusion=None,
                displayTitle="Qualification S2 supervision [s3] (462/merge)")]
    seen = []

    def runs(repo, *, branch, event, cwd=None):
        seen.append(branch)
        return live if (branch == "feat" and event == "pull_request") else []

    monkeypatch.setattr(guard, "_gh_runs", runs)
    monkeypatch.setattr(guard, "_open_pr_numbers", lambda repo, branch, cwd=None: {"462"})
    monkeypatch.setattr(guard, "_current_branch", lambda cwd=None: "feat")
    monkeypatch.setattr(guard, "_remote_sha", lambda repo, ref, cwd=None: SHA)
    return seen


def hook(command):
    out = io.StringIO()
    stdin = io.StringIO(json.dumps({"tool_input": {"command": command}}))
    real, sys.stdout = sys.stdout, out
    try:
        assert guard.claude_hook(stdin) == 0
    finally:
        sys.stdout = real
    return out.getvalue()


def test_claude_hook_denies_in_the_pretooluse_shape(live_pr):
    block = json.loads(hook("git push origin feat"))["hookSpecificOutput"]
    assert block["permissionDecision"] == "deny" and block["permissionDecisionReason"]


@pytest.mark.usefixtures("live_pr")
@pytest.mark.parametrize("command", [
    "FP_S2_GUARD=off git push -u origin feat",
    "git status && git log -1",
    "gh workflow run qualification-s2-supervision.yml --ref feat -f cases=deadline",
])
def test_claude_hook_prints_nothing_when_it_does_not_deny(command):
    assert hook(command) == ""


def test_claude_hook_fails_open_without_gh(monkeypatch):
    monkeypatch.setattr(guard, "_run", lambda cmd, cwd=None: None)
    assert hook("git push -u origin feat") == ""
    assert guard.claude_hook(io.StringIO("not json")) == 0


def test_pre_push_refuses_and_honours_override(live_pr, monkeypatch, capsys):
    line = f"refs/heads/feat {SHA} refs/heads/feat {OTHER}\n"
    assert guard.pre_push(io.StringIO(line)) == 1
    assert guard.OVERRIDE in capsys.readouterr().err
    monkeypatch.setenv("FP_S2_GUARD", "off")
    assert guard.pre_push(io.StringIO(line)) == 0


def test_pre_push_ignores_branch_deletion_and_tags(live_pr):
    lines = f"(delete) {'0' * 40} refs/heads/feat {OTHER}\n" \
            f"refs/tags/v1 {SHA} refs/tags/v1 {'0' * 40}\n"
    assert guard.pre_push(io.StringIO(lines)) == 0


# Without --ref, gh dispatches the repository's default branch, not the local one (D7).
def test_dispatch_without_ref_checks_the_default_branch(monkeypatch):
    seen = []

    def runs(repo, *, branch, event, cwd=None):
        seen.append(branch)
        return [run()] if branch == "main" else []

    monkeypatch.setattr(guard, "_default_branch", lambda repo, cwd=None: "main")
    monkeypatch.setattr(guard, "_gh_runs", runs)
    monkeypatch.setattr(guard, "_remote_sha", lambda repo, ref, cwd=None: SHA)
    block = json.loads(hook("gh workflow run qualification-s2-supervision.yml")
                       )["hookSpecificOutput"]
    assert block["permissionDecision"] == "deny"
    assert "main" in seen and "feat" not in seen


def test_dispatch_without_ref_is_not_blocked_by_the_local_branchs_runs(monkeypatch):
    monkeypatch.setattr(guard, "_default_branch", lambda repo, cwd=None: "main")
    monkeypatch.setattr(guard, "_gh_runs",
                        lambda repo, *, branch, event, cwd=None: [] if branch == "main"
                        else [run()])
    monkeypatch.setattr(guard, "_remote_sha", lambda repo, ref, cwd=None: SHA)
    assert hook("gh workflow run qualification-s2-supervision.yml") == ""


def test_dispatch_without_ref_fails_open_when_default_branch_unknown(monkeypatch):
    monkeypatch.setattr(guard, "_default_branch", lambda repo, cwd=None: "")
    assert hook("gh workflow run qualification-s2-supervision.yml") == ""
