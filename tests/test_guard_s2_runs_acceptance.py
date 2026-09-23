"""Acceptance suite for the S2 run guard hardening card.

Card: docs/briefs/handoffs/2026-09-23-guard-s2-runs-hardening.md. Coordinator-authored
and frozen by SHA-256 in that card: the worker makes these pass without editing this
file. Every gh/git call is faked at the one seam the card requires,
``guard._run(cmd: list[str], cwd: str | None = None) -> str | None``, and the fake
answers only the flags real gh/git would honour (requested --json fields, --limit,
--branch, --head), so a call that drops a flag gets the answer real gh would give.
The finding numbers (F1..F28) refer to the card's §3 table.
"""
import io
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

from scripts import guard_s2_runs as guard
from scripts import guard_open_verification_record, guard_shell_command
from test_fp_launcher import checkout, ops_env  # noqa: F401  pylint: disable=unused-import
from test_git_hooks import environment, hook_checkout  # noqa: F401  pylint: disable=unused-import

ROOT = Path(__file__).resolve().parents[1]
X = "a" * 40      # the ref's remote tip
Y = "b" * 40      # another commit
REPO = "/repo"
WORKFLOW_NAME = "Qualification S2 supervision"
WORKFLOW_FILE = "qualification-s2-supervision.yml"
WORKFLOW_ID = "362153971"
OVERRIDE = "FP_S2_GUARD=off"


# --- the fake gh/git ---------------------------------------------------------

def _opt(cmd, *names):
    """Value of the first matching flag, in `--f v`, `--f=v`, `-fv` or `-f=v` form."""
    for i, arg in enumerate(cmd):
        for name in names:
            if arg == name and i + 1 < len(cmd):
                return cmd[i + 1]
            if arg.startswith(name + "="):
                return arg[len(name) + 1:]
            if len(name) == 2 and arg.startswith(name) and len(arg) > 2 and not arg.startswith("--"):
                return arg[2:].removeprefix("=")
    return None


def _jq(value, expr):
    for part in [p for p in expr.split(".") if p]:
        value = value.get(part) if isinstance(value, dict) else None
    return "" if value is None else str(value)


def _emit(cmd, payload):
    """Shape a gh answer as real gh would: --json filters fields, --jq extracts, else a table."""
    fields = _opt(cmd, "--json")
    jq = _opt(cmd, "--jq", "-q")
    if jq:
        return _jq(payload, jq) + "\n"
    if fields is None:
        return "TABLE OUTPUT (not JSON)\n"
    keep = set(fields.split(","))
    if isinstance(payload, list):
        return json.dumps([{k: v for k, v in item.items() if k in keep} for item in payload])
    return json.dumps({k: v for k, v in payload.items() if k in keep})


class FakeShell:
    """Answers the gh/git calls the guard is allowed to make; anything else returns None."""

    def __init__(self):
        self.runs = {}                  # branch -> list of run dicts
        self.open_prs = {}              # branch -> list of open PR numbers
        self.pr_list_fails = False
        self.default_branch = "main"
        self.repo_view_fails = False
        self.symbolic_ref = "origin/main"
        self.tips = {}                  # branch -> remote tip sha
        self.current = {REPO: "feat"}   # directory -> checked-out branch
        self.local_branches = ["feat", "main"]
        self.views = {}                 # run id (str) -> run dict
        self.pr_heads = {}              # PR number (str) or None (current) -> head branch
        self.messages = {}              # rev -> commit message
        self.run_list_fails = False
        self.calls = []

    def __call__(self, cmd, cwd=None):
        cmd = [str(c) for c in cmd]
        self.calls.append((cmd, cwd))
        tool = os.path.basename(cmd[0]).removesuffix(".exe")
        if tool == "gh":
            return self.gh(cmd)
        if tool == "git":
            return self.git(cmd, cwd)
        return None

    def gh(self, cmd):
        words = set(cmd[1:])
        if {"run", "list"} <= words:
            if self.run_list_fails:
                return None
            branch = _opt(cmd, "--branch", "-b")
            workflow = _opt(cmd, "--workflow", "-w")
            limit = int(_opt(cmd, "--limit", "-L") or 20)
            runs = [r for r in self.runs.get(branch, [])] if branch else [r for v in self.runs.values() for r in v]
            if workflow not in (WORKFLOW_FILE, WORKFLOW_NAME, WORKFLOW_ID):
                runs = runs + [decoy_run(branch or "main")]
            runs = sorted(runs, key=lambda r: r["createdAt"], reverse=True)[:limit]
            return _emit(cmd, runs)
        if {"run", "view"} <= words:
            rid = next((c for c in cmd[3:] if c.isdigit()), None)
            view = self.views.get(rid)
            return None if view is None else _emit(cmd, view)
        if {"pr", "list"} <= words:
            if self.pr_list_fails:
                return None
            head = _opt(cmd, "--head", "-H")
            state = _opt(cmd, "--state", "-s") or "open"
            numbers = self.open_prs.get(head, []) if state == "open" else []
            return _emit(cmd, [{"number": n} for n in numbers])
        if {"pr", "view"} <= words:
            number = next((c for c in cmd[3:] if c.isdigit()), None)
            head = self.pr_heads.get(number)
            return None if head is None else _emit(cmd, {"headRefName": head, "number": int(number or 0)})
        if {"repo", "view"} <= words:
            if self.repo_view_fails:
                return None
            return _emit(cmd, {"defaultBranchRef": {"name": self.default_branch},
                               "nameWithOwner": "Joshua-Asante/first-passage"})
        if "api" in words:
            path = next((c for c in cmd[2:] if c.startswith("repos/")), "")
            match = re.search(r"/(?:git/ref/heads|git/refs/heads|commits|branches)/(.+)$", path)
            sha = self.tips.get(match.group(1)) if match else None
            if sha is None:
                return None
            return _emit(cmd, {"sha": sha, "object": {"sha": sha}, "commit": {"sha": sha}})
        return None

    def git(self, cmd, cwd):
        args = cmd[1:]
        where = cwd
        while args and args[0].startswith("-"):
            if args[0] in ("-C", "-c", "--git-dir", "--work-tree") and len(args) > 1:
                if args[0] == "-C":
                    where = os.path.join(where or REPO, args[1])
                args = args[2:]
            else:
                args = args[1:]
        here = os.path.normpath(where or REPO)
        if args[:3] == ["rev-parse", "--abbrev-ref", "HEAD"] or args[:2] == ["branch", "--show-current"] \
                or args[:3] == ["symbolic-ref", "--short", "HEAD"]:
            branch = self.current.get(here)
            return None if branch is None else branch + "\n"
        if args[:3] == ["symbolic-ref", "--short", "refs/remotes/origin/HEAD"] \
                or args[:2] == ["symbolic-ref", "refs/remotes/origin/HEAD"]:
            return None if self.symbolic_ref is None else self.symbolic_ref + "\n"
        if args[:1] == ["ls-remote"]:
            out = []
            for ref in args[1:]:
                name = ref.removeprefix("refs/heads/")
                if name in self.tips:
                    out.append(f"{self.tips[name]}\trefs/heads/{name}")
            return "\n".join(out) + ("\n" if out else "")
        if args[:1] == ["for-each-ref"]:
            return "".join(b + "\n" for b in self.local_branches)
        if args[:1] in (["log"], ["show"]):
            rev = next((a for a in reversed(args[1:]) if not a.startswith("-")), "HEAD").removeprefix("refs/heads/")
            if rev == "HEAD":
                rev = self.current.get(here, "HEAD")
            msg = self.messages.get(rev)
            return None if msg is None else msg + "\n"
        return None


def decoy_run(branch):
    """A failed run of another workflow: only visible to a gh call that drops --workflow."""
    return {"databaseId": 999, "headSha": X, "status": "completed", "conclusion": "failure",
            "event": "workflow_dispatch", "displayTitle": f"{WORKFLOW_NAME} [s3] ({branch})",
            "workflowName": "Other", "headBranch": branch, "createdAt": "2026-09-23T09:59:00Z"}


def pr_run(number, *, status="in_progress", conclusion=None, sha=X, mode="s3", rid=11,
           created="2026-09-23T01:00:00Z", branch="feat", title=None):
    return {"databaseId": rid, "headSha": sha, "status": status, "conclusion": conclusion,
            "event": "pull_request", "displayTitle": title or f"{WORKFLOW_NAME} [{mode}] ({number}/merge)",
            "workflowName": WORKFLOW_NAME, "headBranch": branch, "createdAt": created}


def dispatch_run(branch="feat", *, mode="s3", status="completed", conclusion="success", sha=X,
                 rid=21, created="2026-09-23T02:00:00Z", cases=None, title=None):
    if title is None:
        title = (f"S2 DIAGNOSTIC [{mode}] ({cases})" if cases
                 else f"{WORKFLOW_NAME} [{mode}] ({branch})")
    return {"databaseId": rid, "headSha": sha, "status": status, "conclusion": conclusion,
            "event": "workflow_dispatch", "displayTitle": title, "workflowName": WORKFLOW_NAME,
            "headBranch": branch, "createdAt": created}


@pytest.fixture
def sh(monkeypatch):
    fake = FakeShell()
    fake.tips = {"feat": X, "main": Y, "wip": Y, "other": Y}
    monkeypatch.setattr(guard, "_run", fake)
    return fake


def decide(command, cwd=REPO):
    return guard.refusal_for_command(command, cwd=cwd)


def hook(payload, capsys):
    out_before = capsys.readouterr()  # drain
    del out_before
    assert guard.claude_hook(io.StringIO(json.dumps(payload))) == 0
    return capsys.readouterr().out


def live_pr(sh, branch="feat", number=462):
    sh.open_prs[branch] = [number]
    sh.runs.setdefault(branch, []).append(pr_run(number, branch=branch))


DISPATCH = f"gh workflow run {WORKFLOW_FILE} --ref feat"


# --- F24: the Claude hook never approves; it only denies ----------------------

def test_f24_hook_is_silent_when_it_has_no_decision(sh, capsys):
    out = hook({"tool_name": "Bash", "tool_input": {"command": "ls -la"}, "cwd": REPO}, capsys)
    assert out.strip() == ""


def test_f24_hook_is_silent_when_the_guard_itself_fails(sh, capsys, monkeypatch):
    def boom(*_a, **_k):
        raise RuntimeError("gh exploded")
    monkeypatch.setattr(guard, "_run", boom)
    live_pr(sh)
    out = hook({"tool_name": "Bash", "tool_input": {"command": "git push origin feat"}, "cwd": REPO}, capsys)
    assert out.strip() == ""
    assert guard.claude_hook(io.StringIO("not json")) == 0
    assert capsys.readouterr().out.strip() == ""


def test_f24_hook_denies_in_the_pretooluse_shape(sh, capsys):
    live_pr(sh)
    out = json.loads(hook({"tool_name": "Bash", "tool_input": {"command": "git push origin feat"},
                           "cwd": REPO}, capsys))
    block = out["hookSpecificOutput"]
    assert block["hookEventName"] == "PreToolUse"
    assert block["permissionDecision"] == "deny"
    assert "cancel" in block["permissionDecisionReason"]


@pytest.mark.parametrize("command", ["ls -la", "git status", "python -m pytest -q"])
def test_f24_guard_shell_command_does_not_approve_benign_commands(command, capsys, monkeypatch):
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps({"tool_input": {"command": command}})))
    assert guard_shell_command.main() == 0
    out = capsys.readouterr().out.strip()
    assert out == "" or json.loads(out)["hookSpecificOutput"]["permissionDecision"] != "allow"


def test_f24_guard_shell_command_still_asks_on_destructive_commands(capsys, monkeypatch):
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps({"tool_input": {"command": "git reset --hard"}})))
    assert guard_shell_command.main() == 0
    assert json.loads(capsys.readouterr().out)["hookSpecificOutput"]["permissionDecision"] == "ask"


# --- F28: the Edit/Write hook never approves either ----------------------------

def _write_hook(payload, capsys, monkeypatch):
    monkeypatch.setattr(sys, "stdin", io.StringIO(payload))
    assert guard_open_verification_record.main() == 0
    return capsys.readouterr().out.strip()


def test_f28_write_guard_does_not_approve_writes(tmp_path, capsys, monkeypatch):
    root = tmp_path / "repo"
    (root / ".git").mkdir(parents=True)
    for target in (root / "docs" / "x.md", tmp_path / "outside" / "y.md"):
        out = _write_hook(json.dumps({"tool_input": {"file_path": str(target)}}), capsys, monkeypatch)
        assert out == "" or json.loads(out)["hookSpecificOutput"]["permissionDecision"] != "allow", target
    out = _write_hook("not json", capsys, monkeypatch)
    assert out == "" or json.loads(out)["hookSpecificOutput"]["permissionDecision"] != "allow"


def test_f28_write_guard_still_denies_while_a_record_is_open(tmp_path, capsys, monkeypatch):
    root = tmp_path / "repo"
    folder = root / ".cache" / "fp-verification" / "r1"
    folder.mkdir(parents=True)
    (root / ".git").mkdir()
    started = datetime.now(timezone.utc).isoformat()
    (folder / "record.json").write_text(json.dumps({"status": "running", "started_at": started}), encoding="utf-8")
    out = _write_hook(json.dumps({"tool_input": {"file_path": str(root / "docs" / "x.md")}}), capsys, monkeypatch)
    assert json.loads(out)["hookSpecificOutput"]["permissionDecision"] == "deny"


# --- pushes: which runs a push can cancel (F6, F21) ---------------------------

def test_push_refused_while_open_prs_run_is_live(sh):
    live_pr(sh)
    reason = decide("git push origin feat")
    assert reason and "cancel" in reason and f"{OVERRIDE} git push" in reason


def test_f6_push_allowed_when_the_live_runs_pr_is_no_longer_open(sh):
    sh.runs["feat"] = [pr_run(459)]
    sh.open_prs["feat"] = []
    assert decide("git push origin feat") is None


def test_f6_push_refused_when_only_another_open_pr_is_live(sh):
    sh.runs["feat"] = [pr_run(459, rid=11), pr_run(462, rid=12)]
    sh.open_prs["feat"] = [462]
    assert decide("git push origin feat")


def test_f6_untitled_live_pr_run_counts_while_a_pr_is_open(sh):
    sh.runs["feat"] = [pr_run(462, title="Some PR title")]
    sh.open_prs["feat"] = [462]
    assert decide("git push origin feat")


def test_f6_open_pr_lookup_failure_keeps_refusing(sh):
    live_pr(sh)
    sh.pr_list_fails = True
    assert decide("git push origin feat")


def test_push_fails_open_when_run_list_fails(sh):
    live_pr(sh)
    sh.run_list_fails = True
    assert decide("git push origin feat") is None


@pytest.mark.parametrize("marker", ["[skip ci]", "[ci skip]", "[no ci]", "[skip actions]", "[actions skip]",
                                    "docs\n\n\nskip-checks: true"])
def test_f21_push_of_a_skip_ci_tip_is_allowed(sh, marker):
    live_pr(sh)
    sh.messages["feat"] = f"docs: notes {marker}"
    assert decide("git push origin feat") is None


def test_f21_skip_ci_is_not_trusted_after_a_commit_in_the_same_command(sh):
    live_pr(sh)
    sh.messages["feat"] = "docs [skip ci]"  # the OLD tip; the new commit's message is unknown
    assert decide('git commit -m "real change" && git push origin feat')


# --- pushes: parsing (F7, F8, F14, F15, F16, F17, F18, F19, F27) --------------

@pytest.mark.parametrize("command", [
    "git push -u origin HEAD 2>&1 | tail -5",
    "git push origin feat > /tmp/push.log 2>&1",
    "env FOO=1 git push origin feat",
    "command git push origin feat",
    "timeout 120 git push origin feat",
    "/usr/bin/git push origin feat",
    'bash -c "git push origin feat"',
    "sh -c 'git push origin feat'",
    "if git push origin feat; then echo ok; fi",
    "(cd /repo && git push origin feat)",
    "git fetch & git push origin feat",
    "git push -u origin \\\n  feat",
    "echo hi\ngit push origin feat",
    "GIT_TRACE=1 git push origin feat",
    'git push -u origin "$(git branch --show-current)"',
    "git push -u origin $(git rev-parse --abbrev-ref HEAD)",
    "git -c push.default=current push origin feat",
    "git push origin +feat",
    "git push origin wip:feat",
    "git push origin wip feat",
    f"gh workflow run {WORKFLOW_FILE} --ref other -f cases=x && git push origin feat",
    "out=$(git push origin feat 2>&1)",
])
def test_pushes_that_update_a_live_branch_are_refused(sh, command):
    live_pr(sh)
    assert decide(command), command


@pytest.mark.parametrize("command", [
    'git commit -m "refuse; git push origin feat; while live"',
    'git commit -m "a && git push origin feat"',
    'grep -rnE "gh workflow run|git push|FP_S2_GUARD" scripts .claude',
    "rg -n 'cancel-in-progress|git push' .github",
    'git log -E --grep="guard|git push"',
    "cat > notes.md <<'EOF'\ngit push origin feat\nEOF",
    "git commit -m \"$(cat <<'EOF'\nfix: guard\n\ngit push origin feat\nEOF\n)\"",
    "git push origin --delete feat",
    "git push -d origin feat",
    "git push origin :feat",
    "git push --tags",
    "git push --dry-run origin feat",
    "git push -n origin feat",
    "git push origin wip",
    'git push origin "$BRANCH"',
])
def test_commands_that_do_not_update_a_live_branch_are_allowed(sh, command):
    live_pr(sh)
    assert decide(command) is None, command


def test_f14_push_all_checks_every_local_branch(sh):
    sh.current[REPO] = "main"
    sh.local_branches = ["main", "feat"]
    live_pr(sh, "feat")
    assert decide("git push --all origin")
    assert decide("git push --mirror origin")


def test_f15_cd_and_dash_c_resolve_the_branch_where_the_push_runs(sh):
    live_pr(sh, "feat")              # the session checkout (/repo) is on feat
    sh.current["/wt/other"] = "other"
    assert decide("cd /wt/other && git push -u origin HEAD") is None
    assert decide("git -C /wt/other push -u origin HEAD") is None
    sh.current[REPO] = "main"
    sh.current["/wt/feat"] = "feat"
    assert decide("cd /wt/feat && git push -u origin HEAD")
    assert decide("git -C /wt/feat push")


def test_f15_relative_cd_resolves_against_the_hook_cwd(sh):
    live_pr(sh, "feat")
    sh.current[REPO] = "main"
    sh.current["/repo/sub"] = "feat"
    assert decide("cd sub && git push")


def test_f16_override_counts_only_on_the_push_segment_itself(sh):
    live_pr(sh)
    assert decide(f"{OVERRIDE} git push origin feat") is None
    assert decide(f"export {OVERRIDE} && git push origin feat") is None
    assert decide(f"{OVERRIDE} git add -A && git commit -m x && git push origin feat")
    assert decide(f"grep {OVERRIDE} -r . && git push origin feat")


def test_f20_gh_pr_update_branch_is_a_push_to_the_prs_head(sh):
    live_pr(sh, "feat", 462)
    sh.pr_heads["462"] = "feat"
    sh.pr_heads[None] = "feat"
    assert decide("gh pr update-branch 462")
    assert decide("gh pr update-branch")


# --- dispatch: cancellation follows the concurrency group (F3, F4) -----------

@pytest.mark.parametrize("live", [
    dispatch_run(mode="s2", status="in_progress", conclusion=None),
    dispatch_run(mode="s3", status="queued", conclusion=None, sha=Y),
    dispatch_run(status="in_progress", conclusion=None, title=f"{WORKFLOW_NAME} (feat)"),  # no mode tag
])
def test_f3_f4_full_dispatch_refused_while_a_full_dispatch_run_is_live_on_the_ref(sh, live):
    sh.runs["feat"] = [live]
    reason = decide(DISPATCH)
    assert reason and "cancel" in reason


def test_f3_diagnostic_and_full_dispatches_are_separate_groups(sh):
    sh.runs["feat"] = [dispatch_run(status="in_progress", conclusion=None, cases="deadline")]
    assert decide(DISPATCH) is None
    assert decide(f"{DISPATCH} -f mode=s3 -f cases=other")
    sh.runs["feat"] = [dispatch_run(status="in_progress", conclusion=None)]
    assert decide(f"{DISPATCH} -f mode=s3 -f cases=other") is None


def test_f2_live_pr_run_does_not_block_a_dispatch(sh):
    live_pr(sh)
    assert decide(DISPATCH) is None


# --- dispatch: redundancy is same-bytes, same-mode (F2, F5, F22) -------------

@pytest.mark.parametrize("prior_mode,conclusion,requested,refused", [
    ("s3", "success", "s3", True),
    ("s3", "failure", "s3", True),
    ("s2", "success", "s2", True),
    ("s2", "failure", "s2", True),
    ("s3", "success", "s2", False),   # s3 runs the S2 nodes on the v5 install, never v4
    ("s3", "failure", "s2", False),
    ("s2", "success", "s3", False),
    ("s2", "failure", "s3", False),   # s3 installs --dispatch; an s2 failure need not recur
    ("s3", "cancelled", "s3", False),
])
def test_f5_modes_are_incomparable(sh, prior_mode, conclusion, requested, refused):
    sh.runs["feat"] = [dispatch_run(mode=prior_mode, conclusion=conclusion)]
    reason = decide(f"{DISPATCH} -f mode={requested}")
    assert (reason is not None) is refused


def test_f2_pr_runs_never_count_as_the_dispatchs_bytes(sh):
    sh.runs["feat"] = [pr_run(462, status="completed", conclusion="failure"),
                       pr_run(462, status="completed", conclusion="success", rid=12)]
    assert decide(DISPATCH) is None


def test_f22_the_newest_definitive_same_mode_run_decides(sh):
    sh.runs["feat"] = [dispatch_run(conclusion="failure", rid=1, created="2026-09-23T01:00:00Z"),
                       dispatch_run(conclusion="success", rid=2, created="2026-09-23T02:00:00Z")]
    assert "passed" in decide(DISPATCH)
    sh.runs["feat"] = [dispatch_run(conclusion="success", rid=1, created="2026-09-23T01:00:00Z"),
                       dispatch_run(conclusion="failure", rid=2, created="2026-09-23T02:00:00Z")]
    assert "re-roll" in decide(DISPATCH)


def test_untagged_or_other_sha_completed_runs_are_not_coverage(sh):
    sh.runs["feat"] = [dispatch_run(title=f"{WORKFLOW_NAME} (feat)"),
                       dispatch_run(title=f"{WORKFLOW_NAME} s3 (feat)", rid=22),
                       dispatch_run(sha=Y, rid=23)]
    assert decide(DISPATCH) is None


def test_failure_advice_names_a_runnable_diagnostic(sh):
    sh.runs["feat"] = [dispatch_run(conclusion="failure")]
    reason = decide(DISPATCH)
    assert "-f mode=s3 -f cases=" in reason and f"{OVERRIDE} gh workflow run" in reason


def test_f23_s2_diagnostic_is_refused_because_it_cannot_run(sh):
    reason = decide(f"{DISPATCH} -f mode=s2 -f cases=deadline")
    assert reason and "s3" in reason


def test_f1_dispatch_after_a_push_in_the_same_command_skips_the_stale_sha(sh):
    sh.runs["feat"] = [dispatch_run(conclusion="failure")]
    assert decide(f"git push origin feat && {DISPATCH}") is None
    sh.runs["feat"].append(dispatch_run(status="in_progress", conclusion=None, rid=30))
    assert decide(f"git push origin feat && {DISPATCH}")


# --- dispatch: which branch and which selector (F9, F13, F26) ----------------

def test_f26_no_ref_uses_the_default_branch_from_gh_then_origin_head(sh):
    sh.runs["main"] = [dispatch_run("main", sha=Y)]
    sh.runs["feat"] = []
    assert decide(f"gh workflow run {WORKFLOW_FILE}")
    sh.repo_view_fails = True
    assert decide(f"gh workflow run {WORKFLOW_FILE}")
    sh.symbolic_ref = None
    assert decide(f"gh workflow run {WORKFLOW_FILE}") is None


def test_f26_no_ref_never_uses_the_local_branch(sh):
    sh.runs["feat"] = [dispatch_run("feat")]
    sh.runs["main"] = []
    assert decide(f"gh workflow run {WORKFLOW_FILE}") is None


@pytest.mark.parametrize("command", [
    f"gh workflow run --ref feat {WORKFLOW_FILE}",
    f"gh workflow run -r feat {WORKFLOW_FILE}",
    f"gh workflow run {WORKFLOW_FILE} -rfeat",
    f"gh workflow run {WORKFLOW_FILE} -r=feat",
    f"gh workflow run {WORKFLOW_FILE} --ref refs/heads/feat",
    f"gh workflow run {WORKFLOW_ID} --ref feat",
    f"gh workflow run '{WORKFLOW_NAME}' --ref feat",
    f"gh workflow run '{WORKFLOW_NAME.lower()}' --ref feat",
    f"gh workflow run .github/workflows/{WORKFLOW_FILE} --ref feat",
    f"gh.exe workflow run {WORKFLOW_FILE} --ref feat",
    f"gh workflow run -R Joshua-Asante/first-passage {WORKFLOW_FILE} --ref feat",
    f"gh workflow --repo Joshua-Asante/first-passage run {WORKFLOW_FILE} --ref feat",
    f"gh workflow run {WORKFLOW_FILE} \\\n  --ref feat \\\n  -f mode=s3",
])
def test_f9_every_selector_spelling_is_recognised(sh, command):
    sh.runs["feat"] = [dispatch_run()]
    assert decide(command), command


def test_f9_repo_flag_is_passed_to_every_gh_query(sh):
    sh.runs["feat"] = [dispatch_run()]
    assert decide(f"gh workflow run -R Joshua-Asante/first-passage {WORKFLOW_FILE} --ref feat")
    gh_calls = [c for c, _ in sh.calls if os.path.basename(c[0]).removesuffix(".exe") == "gh"]
    assert gh_calls
    for call in gh_calls:
        if "api" in call[1:3]:   # gh api takes no -R; the repository must be explicit in the path
            assert any(a.startswith("repos/Joshua-Asante/first-passage/") for a in call), call
        else:
            assert _opt(call, "-R", "--repo") == "Joshua-Asante/first-passage", call
    assert not any(c[:1] == ["git"] and "ls-remote" in c for c, _ in sh.calls), "-R names the repo, not origin"


def test_other_workflows_are_ignored(sh):
    sh.runs["feat"] = [dispatch_run()]
    assert decide("gh workflow run tests.yml --ref feat") is None


@pytest.mark.parametrize("command", [
    f"{DISPATCH} -fcases=deadline",
    f"{DISPATCH} --raw-field=cases=deadline",
    f"{DISPATCH} -F cases=deadline",
])
def test_f13_diagnostic_field_spellings_are_diagnostic(sh, command):
    sh.runs["feat"] = [dispatch_run(conclusion="failure")]  # would refuse a full s3 dispatch
    assert decide(command) is None, command


@pytest.mark.parametrize("command", [f"{DISPATCH} -fmode=s2", f"{DISPATCH} --field=mode=s2"])
def test_f13_mode_field_spellings(sh, command):
    sh.runs["feat"] = [dispatch_run(mode="s2")]
    assert decide(command), command


def test_f13_json_inputs_are_unknown_so_the_check_fails_open(sh):
    sh.runs["feat"] = [dispatch_run()]
    assert decide(f"echo '{{\"mode\":\"s3\"}}' | {DISPATCH} --json") is None


# --- reruns (F10) --------------------------------------------------------------

@pytest.mark.parametrize("view,refused", [
    (dispatch_run(conclusion="failure", rid=101), True),
    (dispatch_run(conclusion="success", rid=101), True),
    (dispatch_run(conclusion="cancelled", rid=101), False),
    (dispatch_run(conclusion="failure", rid=101, cases="deadline"), False),
    ({**dispatch_run(conclusion="failure", rid=101), "workflowName": "Other"}, False),
])
def test_f10_rerun_of_a_definitive_full_run_is_a_re_roll(sh, view, refused):
    sh.views["101"] = view
    sh.runs["feat"] = [view]
    assert (decide("gh run rerun 101") is not None) is refused
    assert (decide("gh run rerun 101 --failed") is not None) is refused


def test_f10_rerun_that_would_cancel_a_live_run_is_refused(sh):
    old = dispatch_run(conclusion="cancelled", rid=101, created="2026-09-23T01:00:00Z")
    sh.views["101"] = old
    sh.runs["feat"] = [old, dispatch_run(status="in_progress", conclusion=None, rid=102)]
    assert decide("gh run rerun 101")
    old_pr = pr_run(462, status="completed", conclusion="cancelled", rid=201, created="2026-09-23T01:00:00Z")
    sh.views["201"] = old_pr
    sh.runs["feat"] = [old_pr, pr_run(462, rid=202)]
    sh.open_prs["feat"] = [462]
    assert decide("gh run rerun 201")


def test_f10_rerun_fails_open_when_the_run_cannot_be_viewed(sh):
    assert decide("gh run rerun 404") is None


# --- MCP tools (F20) -----------------------------------------------------------

MCP = "mcp__github__"
OWNER = {"owner": "Joshua-Asante", "repo": "first-passage"}


@pytest.mark.parametrize("tool,tool_input", [
    ("push_files", {**OWNER, "branch": "feat", "files": [], "message": "x"}),
    ("create_or_update_file", {**OWNER, "branch": "feat", "path": "a", "content": "b", "message": "x"}),
    ("delete_file", {**OWNER, "branch": "feat", "path": "a", "message": "x"}),
    ("update_pull_request_branch", {**OWNER, "pullNumber": 462}),
])
def test_f20_mcp_pushes_are_guarded(sh, capsys, tool, tool_input):
    live_pr(sh)
    sh.pr_heads["462"] = "feat"
    out = json.loads(hook({"tool_name": MCP + tool, "tool_input": tool_input, "cwd": REPO}, capsys))
    assert out["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_f20_mcp_push_with_skip_ci_message_is_allowed(sh, capsys):
    live_pr(sh)
    payload = {"tool_name": MCP + "push_files",
               "tool_input": {**OWNER, "branch": "feat", "files": [], "message": "docs [skip ci]"}, "cwd": REPO}
    assert hook(payload, capsys).strip() == ""


def test_f20_mcp_workflow_dispatch_and_rerun_are_guarded(sh, capsys):
    sh.runs["feat"] = [dispatch_run(conclusion="failure", rid=101)]
    sh.views["101"] = sh.runs["feat"][0]
    run = {"tool_name": MCP + "actions_run_trigger", "cwd": REPO,
           "tool_input": {**OWNER, "method": "run_workflow", "workflow_id": WORKFLOW_FILE,
                          "ref": "feat", "inputs": {"mode": "s3"}}}
    assert json.loads(hook(run, capsys))["hookSpecificOutput"]["permissionDecision"] == "deny"
    rerun = {"tool_name": MCP + "actions_run_trigger", "cwd": REPO,
             "tool_input": {**OWNER, "method": "rerun_workflow_run", "run_id": 101}}
    assert json.loads(hook(rerun, capsys))["hookSpecificOutput"]["permissionDecision"] == "deny"
    diag = {"tool_name": MCP + "actions_run_trigger", "cwd": REPO,
            "tool_input": {**OWNER, "method": "run_workflow", "workflow_id": WORKFLOW_FILE,
                           "ref": "feat", "inputs": {"mode": "s3", "cases": "deadline"}}}
    assert hook(diag, capsys).strip() == ""


def test_f20_unrelated_mcp_tools_get_no_decision(sh, capsys):
    live_pr(sh)
    payload = {"tool_name": MCP + "get_file_contents", "tool_input": {**OWNER, "path": "a"}, "cwd": REPO}
    assert hook(payload, capsys).strip() == ""


def test_f20_settings_route_bash_and_the_mcp_tools_to_the_guard():
    settings = json.loads((ROOT / ".claude/settings.json").read_text(encoding="utf-8"))
    matchers = [entry.get("matcher", "") for entry in settings["hooks"]["PreToolUse"]
                if any("guard_s2_runs.py" in h.get("command", "") for h in entry.get("hooks", []))]
    names = ["Bash"] + [MCP + t for t in ("push_files", "create_or_update_file", "delete_file",
                                          "update_pull_request_branch", "actions_run_trigger")]
    for name in names:
        assert any(re.fullmatch(m, name) for m in matchers), name
    assert not any(re.fullmatch(m, MCP + "get_file_contents") for m in matchers)


# --- git pre-push layer (F11, F12, F21, F25) ------------------------------------

def pre_push(sh, lines, monkeypatch, env_off=False):
    if env_off:
        monkeypatch.setenv("FP_S2_GUARD", "off")
    else:
        monkeypatch.delenv("FP_S2_GUARD", raising=False)
    return guard.pre_push(io.StringIO("".join(line + "\n" for line in lines)))


def test_f12_pre_push_checks_the_remote_ref_not_the_local_one(sh, monkeypatch, capsys):
    live_pr(sh, "feat")
    assert pre_push(sh, [f"refs/heads/wip {X} refs/heads/feat {Y}"], monkeypatch) == 1
    assert "FP_S2_GUARD=off" in capsys.readouterr().err
    assert pre_push(sh, [f"refs/heads/feat {X} refs/heads/wip {Y}"], monkeypatch) == 0


def test_pre_push_ignores_deletions_tags_and_honours_the_override(sh, monkeypatch):
    live_pr(sh, "feat")
    assert pre_push(sh, [f"(delete) {'0' * 40} refs/heads/feat {Y}"], monkeypatch) == 0
    assert pre_push(sh, [f"refs/tags/v1 {X} refs/tags/v1 {'0' * 40}"], monkeypatch) == 0
    assert pre_push(sh, [f"refs/heads/feat {X} refs/heads/feat {Y}"], monkeypatch, env_off=True) == 0


def test_f6_pre_push_allows_when_the_pr_is_closed(sh, monkeypatch):
    sh.runs["feat"] = [pr_run(459)]
    sh.open_prs["feat"] = []
    assert pre_push(sh, [f"refs/heads/feat {X} refs/heads/feat {Y}"], monkeypatch) == 0


def test_f21_pre_push_allows_a_skip_ci_tip(sh, monkeypatch):
    live_pr(sh, "feat")
    sh.messages[X] = "docs: notes [skip ci]"
    assert pre_push(sh, [f"refs/heads/feat {X} refs/heads/feat {Y}"], monkeypatch) == 0


def test_f25_undecodable_output_fails_open(monkeypatch):
    def undecodable(*_a, **_k):
        raise UnicodeDecodeError("cp1252", b"\x81", 0, 1, "undefined")
    monkeypatch.setattr(guard.subprocess, "run", undecodable)
    assert guard._run(["gh", "run", "list"]) is None  # pylint: disable=protected-access


def test_run_passes_cwd_to_subprocess(monkeypatch):
    seen = {}

    def fake_run(cmd, **kwargs):
        seen.update(kwargs, cmd=cmd)
        return subprocess.CompletedProcess(cmd, 0, stdout="ok\n", stderr="")
    monkeypatch.setattr(guard.subprocess, "run", fake_run)
    assert guard._run(["git", "status"], cwd="/wt/x") == "ok\n"  # pylint: disable=protected-access
    assert seen["cwd"] == "/wt/x" and seen.get("encoding", "").lower().replace("-", "") == "utf8"


STDIN_PROBE = '''import os, sys
from pathlib import Path
Path(os.environ["GUARD_STDIN_LOG"]).write_text(sys.stdin.read(), encoding="utf-8")
raise SystemExit(int(os.environ.get("GUARD_EXIT", "0")))
'''


@pytest.mark.parametrize("guard_exit,hook_exit_nonzero", [(0, False), (1, True)])
def test_f11_pre_push_hook_feeds_git_refs_to_the_guard_and_honours_its_exit(
        hook_checkout, ops_env, shell, tmp_path, guard_exit, hook_exit_nonzero):
    root = hook_checkout
    (root / ".cache").mkdir(exist_ok=True)
    (root / "scripts" / "guard_s2_runs.py").write_text(STDIN_PROBE, encoding="utf-8")
    log = tmp_path / "stdin.log"
    env = dict(environment(root, ops_env), GUARD_STDIN_LOG=str(log), GUARD_EXIT=str(guard_exit))
    line = f"refs/heads/feat {X} refs/heads/feat {Y}\n"
    result = subprocess.run([shell, str(root / "scripts/githooks/pre-push")], cwd=root / "docs", env=env,
                            input=line, capture_output=True, text=True, encoding="utf-8", errors="replace",
                            check=False, timeout=45)
    assert line.strip() in log.read_text(encoding="utf-8")
    assert (result.returncode != 0) is hook_exit_nonzero, result.stdout + result.stderr
