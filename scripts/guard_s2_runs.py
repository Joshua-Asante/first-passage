"""guard_s2_runs.py — refuse the moves that would cancel or re-roll an S2 run.

Why: an S2 supervision run is ~25 min on a fresh host. During S2 (2026-09-19/21)
three runs were cancelled by pushes to a PR branch mid-run (the pull_request
run's `cancel-in-progress` concurrency kills it on every new push, docs-only
pushes included), and same-SHA re-dispatches re-rolled a real race instead of
root-causing it (`.claude/skills/s2-linux-run/SKILL.md` §1, §3). Both are
knowable before the command runs, so refuse them then.

What is refused (everything else is allowed; the module never blocks on its own
failure — a failed lookup allows the action, the one exception being the
open-PR refinement below, which keeps refusing when `gh pr list` fails):

  * **push** — a push (shell `git push` or `gh pr update-branch`, the GitHub
    MCP write tools, or the git pre-push layer) to a branch with an in-flight
    `pull_request` run of this workflow whose PR is still open. A tip carrying
    a skip-CI marker is allowed unless an earlier segment of the same command
    ran a git command that can move the tip.
  * **dispatch** — a full `gh workflow run` of this workflow while any full
    `workflow_dispatch` run is live on the ref (a diagnostic dispatch forms its
    own concurrency group and only blocks diagnostics), or when the newest
    definitive same-mode `workflow_dispatch` run on the dispatched SHA already
    decided it: `success` → read the artifact, `failure` → root-cause it, do
    not re-roll. `[s2]` and `[s3]` are incomparable (an s3 run installs the v5
    dispatch profile, an s2 run the v4 funded one — neither covers the other);
    `pull_request` runs tested the merge ref and never count as the head's
    bytes; `cases` is accepted in `s3` only, so an s2 diagnostic is refused.
  * **rerun** — `gh run rerun` of a definitive full run of this workflow, or of
    a run whose concurrency group is live (same ref and kind, or, for
    `pull_request` runs, the same PR).

Override: `FP_S2_GUARD=off` as a leading assignment on the guarded segment, an
earlier `export FP_S2_GUARD=off` segment, or (pre-push layer) the environment.

Entry points (fail open — no `gh`, offline, unparseable input → no output; the
hook never approves anything, it only denies):
  * `python scripts/guard_s2_runs.py claude-hook` — Claude Code PreToolUse hook
    for Bash and the GitHub MCP write tools (`.claude/settings.json`); stdin is
    the tool payload, stdout the deny JSON, and nothing when it does not deny.
  * `python scripts/guard_s2_runs.py pre-push` — from `scripts/githooks/pre-push`;
    stdin is git's `<local ref> <local sha> <remote ref> <remote sha>` lines;
    exit 1 refuses the push.

`push_refusal()`, `dispatch_cancel_refusal()`, `dispatch_redundancy_refusal()`
and `rerun_refusal()` are the pure functions the tests pin; `_run()` is the one
process boundary every `gh`/`git` call goes through.
"""
from __future__ import annotations

import json
import os
import posixpath
import re
import subprocess
import sys

try:  # imported as `scripts.guard_s2_runs` (tests, repo root on sys.path)
    from scripts._shell_tokens import expand as _expand
    from scripts._shell_tokens import is_assignment as _is_assignment
    from scripts._shell_tokens import segments as _segments
    from scripts._shell_tokens import strip_assignments as _strip_assignments
except ImportError:  # run as `python scripts/guard_s2_runs.py`: scripts/ is sys.path[0]
    from _shell_tokens import expand as _expand
    from _shell_tokens import is_assignment as _is_assignment
    from _shell_tokens import segments as _segments
    from _shell_tokens import strip_assignments as _strip_assignments

WORKFLOW_FILE = "qualification-s2-supervision.yml"
WORKFLOW_NAME = "Qualification S2 supervision"
WORKFLOW_ID = "362153971"
IN_FLIGHT = frozenset({"queued", "in_progress", "waiting", "requested", "pending"})
DEFINITIVE = frozenset({"success", "failure"})
DIAGNOSTIC_TITLE = "S2 DIAGNOSTIC"
OVERRIDE = "FP_S2_GUARD=off"
DEFAULT_MODE = "s3"  # the workflow's `mode` input default
SKIP_CI_MARKERS = ("[skip ci]", "[ci skip]", "[no ci]", "[skip actions]",
                   "[actions skip]", "skip-checks: true")
# git subcommands whose earlier presence in the same command makes the tip's
# message unknowable at PreToolUse time, voiding the skip-CI exemption (D3).
TIP_MOVERS = frozenset({"commit", "pull", "merge", "rebase", "cherry-pick",
                        "revert", "am", "reset"})
MCP_PUSH_TOOLS = frozenset({"push_files", "create_or_update_file", "delete_file"})
MCP_TOOLS = MCP_PUSH_TOOLS | {"update_pull_request_branch", "actions_run_trigger"}
RUN_FIELDS = ("databaseId,headSha,status,conclusion,event,displayTitle,headBranch,"
              "createdAt,workflowName,workflowDatabaseId")
VIEW_FIELDS = ("databaseId,status,conclusion,event,displayTitle,headBranch,headSha,"
               "workflowName,workflowDatabaseId")
S2_CASES_NOTE = ("the workflow accepts `cases` only with mode s3 (an s2 selection has "
                 "nothing to subset), so this dispatch would fail at setup; re-run it "
                 "as `-f mode=s3 -f cases='<expr>'` or a full s3 dispatch.")

_TITLE_MODE = re.compile(r"\[(s2|s3)\]")
_TITLE_PR = re.compile(r"\((\d+)/merge\)")


# --- run-dict helpers ---------------------------------------------------------

def _is_ours(run: dict) -> bool:
    """Whether `run` belongs to this workflow (belt and braces over --workflow)."""
    return (str(run.get("workflowDatabaseId")) == WORKFLOW_ID
            or str(run.get("workflowName", "")).casefold() == WORKFLOW_NAME.casefold())


def _is_diagnostic(run: dict) -> bool:
    return str(run.get("displayTitle", "")).startswith(DIAGNOSTIC_TITLE)


def _run_mode(run: dict) -> str | None:
    """The bracketed boundary mode a run's title records, or None when it names none."""
    match = _TITLE_MODE.search(str(run.get("displayTitle", "")))
    return match.group(1) if match else None


def _pr_number(run: dict) -> str | None:
    """The PR whose merge ref a pull_request run tested, or None for other titles."""
    match = _TITLE_PR.search(str(run.get("displayTitle", "")))
    return match.group(1) if match else None


def _same_pr(left: dict, right: dict) -> bool:
    """Whether two pull_request runs share a concurrency group (the same PR)."""
    numbers = (_pr_number(left), _pr_number(right))
    if numbers[0] and numbers[1]:
        return numbers[0] == numbers[1]
    branches = (str(left.get("headBranch") or ""), str(right.get("headBranch") or ""))
    return bool(branches[0]) and branches[0] == branches[1]


# --- pure decisions -----------------------------------------------------------

def push_refusal(branch: str, live_runs: list[dict], *,
                 open_numbers: set[str] | None) -> str | None:
    """Reason to refuse a push to `branch`, or None.

    `live_runs` are the in-flight pull_request runs of this workflow on the
    branch; `open_numbers` are the numbers of that branch's open PRs, or None
    when `gh pr list` failed (then every live run counts — the refinement may
    not weaken the refusal it refines).
    """
    blocking = []
    for run in live_runs:
        number = _pr_number(run)
        if open_numbers is None or (number is None and open_numbers) \
                or (number is not None and number in open_numbers):
            blocking.append(run)
    if not blocking:
        return None
    ids = ", ".join(str(r.get("databaseId")) for r in blocking)
    return (f"S2 run {ids} is in flight on the pull request for '{branch}'; a push now "
            f"refires the workflow and cancel-in-progress kills that run (~25 min "
            f"lost). Commit locally and push after it finishes (docs commits "
            f"included), or push a tip carrying [skip ci]. Deliberate cancel: "
            f"{OVERRIDE} git push … (pre-push layer: {OVERRIDE} in the environment).")


def dispatch_cancel_refusal(ref: str, runs: list[dict], *, diagnostic: bool) -> str | None:
    """Reason to refuse a dispatch on `ref`, or None (concurrency group only)."""
    live = [r for r in runs if r.get("status") in IN_FLIGHT
            and str(r.get("event")) == "workflow_dispatch"
            and _is_diagnostic(r) == diagnostic]
    if not live:
        return None
    ids = ", ".join(str(r.get("databaseId")) for r in live)
    kind = "diagnostic" if diagnostic else "full"
    return (f"a {kind} dispatch on '{ref}' would enter the same concurrency group as "
            f"S2 run {ids} and cancel it (~25 min lost); wait for it and read its "
            f"artifact. Deliberate: {OVERRIDE} gh workflow run ….")


def dispatch_redundancy_refusal(sha: str, runs: list[dict], *, mode: str) -> str | None:
    """Reason to refuse a full `mode` dispatch on `sha`, or None (redundancy only).

    Only completed, definitive, non-diagnostic `workflow_dispatch` runs of this
    workflow on `sha` carrying the same bracketed mode tag are coverage, and the
    newest of them decides.
    """
    decided = [r for r in runs
               if r.get("status") == "completed" and r.get("conclusion") in DEFINITIVE
               and str(r.get("event")) == "workflow_dispatch"
               and r.get("headSha") == sha and _run_mode(r) == mode
               and not _is_diagnostic(r)]
    if not decided:
        return None
    run = max(decided, key=lambda r: str(r.get("createdAt", "")))
    if run.get("conclusion") == "success":
        return (f"S2 run {run.get('databaseId')} [{mode}] already passed on "
                f"{sha[:12]} (same bytes, same mode): read its artifact "
                f"(scripts/s2_run_evidence.py {run.get('databaseId')}) instead of "
                f"re-running. Deliberate re-dispatch: {OVERRIDE} gh workflow run ….")
    return (f"S2 run {run.get('databaseId')} [{mode}] already failed on {sha[:12]}, "
            f"and the newest definitive same-mode run decides: a re-dispatch on "
            f"unchanged bytes is a re-roll, not a fix. Root-cause it from the "
            f"artifact (s2-linux-run §3), or iterate on one case with "
            f"-f mode=s3 -f cases='<expr>'. Justified re-dispatch: "
            f"{OVERRIDE} gh workflow run ….")


def rerun_refusal(view: dict, runs: list[dict]) -> str | None:
    """Reason to refuse `gh run rerun` of the viewed run, or None.

    `runs` are this workflow's runs on the viewed run's branch; they decide the
    cancellation half (same ref and kind, or the same PR).
    """
    if (str(view.get("event")) == "workflow_dispatch" and not _is_diagnostic(view)
            and str(view.get("status")) == "completed"
            and str(view.get("conclusion")) in DEFINITIVE):
        outcome = "already passed" if view.get("conclusion") == "success" else "already failed"
        return (f"S2 run {view.get('databaseId')} {outcome}; rerunning it on unchanged "
                f"bytes is a re-roll, not a fix — read its artifact or root-cause the "
                f"failure. Justified rerun: {OVERRIDE} gh run rerun "
                f"{view.get('databaseId')}.")
    live = [r for r in runs if r.get("status") in IN_FLIGHT]
    if str(view.get("event")) == "pull_request":
        group = [r for r in live if r.get("event") == "pull_request" and _same_pr(view, r)]
    else:
        group = [r for r in live if r.get("event") == "workflow_dispatch"
                 and _is_diagnostic(r) == _is_diagnostic(view)]
    if group:
        ids = ", ".join(str(r.get("databaseId")) for r in group)
        return (f"rerunning S2 run {view.get('databaseId')} would enter the same "
                f"concurrency group as live run {ids} and cancel it (~25 min lost). "
                f"Justified: {OVERRIDE} gh run rerun {view.get('databaseId')}.")
    return None


def _has_skip_ci(message: str) -> bool:
    folded = message.casefold()
    return any(marker in folded for marker in SKIP_CI_MARKERS)


# --- command-word parsing -----------------------------------------------------
# The tokenizer (D14) and wrapper expansion live in scripts/_shell_tokens.py,
# shared with guard_shell_command.py; this module uses their default mode.

def _override_on_segment(tokens: list[str]) -> bool:
    """Whether the segment carries the override as one of its leading assignments."""
    for token in tokens:
        if not _is_assignment(token):
            break
        if token == OVERRIDE:
            return True
    return False


def _join_dir(base: str, target: str) -> str:
    """Resolve a `cd`/`-C` target against the hook's directory."""
    if not target:
        return base
    if target.startswith("/") or target.startswith("\\\\") \
            or re.match(r"^[A-Za-z]:[\\/]", target):
        return posixpath.normpath(target.replace("\\", "/"))
    return posixpath.normpath(posixpath.join(base.replace("\\", "/"), target))


def _git_split(tokens: list[str], base_dir: str) -> tuple[str, str | None, list[str]]:
    """(resolved dir, git subcommand, its args) for one git segment."""
    i, target = 1, ""
    takes_value = ("-C", "-c", "--git-dir", "--work-tree", "--namespace")
    while i < len(tokens) and tokens[i].startswith("-"):
        if tokens[i] in takes_value and i + 1 < len(tokens):
            if tokens[i] == "-C":
                target = tokens[i + 1]
            i += 2
        else:
            i += 1
    if i >= len(tokens):
        return _join_dir(base_dir, target), None, []
    return _join_dir(base_dir, target), tokens[i], tokens[i + 1:]


def _push_specs(args: list[str]) -> tuple[str, list[tuple[str, str]]]:
    """(mode, specs) for a `git push` argument list.

    mode is "none" (nothing is updated), "all" (every local branch) or "specs";
    a spec is (destination, source-for-tip-message), with "" meaning HEAD/the
    current branch.
    """
    remote, refspecs, skip_next = None, [], False
    all_branches = deleting = tags = dry_run = False
    takes_value = ("-o", "--push-option", "--repo", "--receive-pack", "--exec")
    for arg in args:
        if skip_next:
            skip_next = False
        elif arg in takes_value:
            skip_next = True
        elif arg == "--":
            refspecs.extend(args[args.index(arg) + 1:])
            break
        elif arg.startswith("-"):
            all_branches |= arg in ("--all", "--branches", "--mirror")
            deleting |= arg in ("-d", "--delete")
            tags |= arg == "--tags"
            dry_run |= arg in ("-n", "--dry-run")
        elif remote is None:
            remote = arg
        else:
            refspecs.append(arg)
    if dry_run or deleting or (tags and not refspecs):
        return "none", []
    if all_branches:
        return "all", []
    if not refspecs:
        return "specs", [("", "")]
    specs: list[tuple[str, str]] = []
    for spec in refspecs:
        source, sep, destination = spec.lstrip("+").partition(":")
        if not sep:
            source = destination = spec.lstrip("+")
        if not destination or (sep and not source):
            continue  # a deletion, or no destination given
        specs.append((destination, source))
    return "specs", specs


def _resolve_specs(specs: list[tuple[str, str | None]], dir_now: str) -> list[tuple[str, str | None]]:
    """Map push specs to concrete (branch, tip-source); unknown ones are skipped.

    A `$(…)`/backquote destination resolves to the current branch of the
    directory the segment runs in; a bare `$VAR` is unknowable, so the push is
    allowed. A None source means no tip message can be read (MCP / update-branch).
    """
    resolved: list[tuple[str, str | None]] = []
    current, have_current = "", False
    for destination, source in specs:
        refers_to_current = destination in ("", "HEAD") \
            or str(destination).startswith(("$(", "`"))
        if refers_to_current and not have_current:
            current, have_current = _current_branch(dir_now), True
        branch = current if refers_to_current else str(destination)
        if not branch or branch.startswith("$"):
            continue
        branch = branch.removeprefix("refs/heads/")
        if source in ("", "HEAD"):
            if not have_current:
                current, have_current = _current_branch(dir_now), True
            resolved.append((branch, current.removeprefix("refs/heads/")))
        else:
            resolved.append((branch, str(source).removeprefix("refs/heads/")))
    return resolved


def _is_workflow(selector: str) -> bool:
    return selector in (WORKFLOW_FILE, WORKFLOW_FILE.removesuffix(".yml"), WORKFLOW_ID) \
        or selector.casefold() == WORKFLOW_NAME.casefold() \
        or selector.endswith(f"/{WORKFLOW_FILE}")


def _repo_flag(tokens: list[str]) -> str | None:
    args = tokens[1:]
    for i, arg in enumerate(args):
        if arg in ("-R", "--repo") and i + 1 < len(args):
            return args[i + 1]
        if arg.startswith("--repo="):
            return arg.split("=", 1)[1]
    return None


_FIELD_FLAG = re.compile(r"--(raw-)?field=([^=]+)=(.*)")
_JOINED_FIELD = re.compile(r"-([fF])([^=]+)=(.*)")
_JOINED_FIELD_EQ = re.compile(r"-([fF])=(.+)")
_TYPED_FIELD_FLAGS = ("-F", "--field")
_JOINED_REF = re.compile(r"-r(.+)")


def _parse_dispatch(tokens: list[str]) -> dict | None:
    """The dispatch a `gh workflow run` segment describes, or None for others.

    Reads flags as pflag does (`-rX`, `-r=X`, `-fK=V`, `-f=K=V`, `--field=K=V`,
    `--raw-field=K=V`, `-F K=V`), accepts the workflow selector anywhere after
    `run`, and keeps a `--json` dispatch unknown (its inputs cannot be read).
    gh applies typed `-F/--field` values after raw `-f/--raw-field` ones, so a
    typed field wins for its key whatever the argument order (F31).
    """
    if len(tokens) < 3 or tokens[1] != "workflow":
        return None
    i, repo = 2, None
    while i < len(tokens) and tokens[i] != "run":
        if tokens[i] in ("-R", "--repo") and i + 1 < len(tokens):
            repo = tokens[i + 1]
            i += 2
        elif tokens[i].startswith("--repo="):
            repo = tokens[i].split("=", 1)[1]
            i += 1
        elif tokens[i].startswith("-"):
            i += 1
        else:
            return None
    if i >= len(tokens) or tokens[i] != "run":
        return None
    tail = tokens[i + 1:]
    ref, selector, json_inputs = "", None, False
    raw, typed = {}, {}
    idx = 0
    while idx < len(tail):
        arg = tail[idx]
        following = tail[idx + 1] if idx + 1 < len(tail) else ""
        if arg == "--json" or arg.startswith("--json="):
            json_inputs = True
        elif arg in ("-r", "--ref"):
            ref = following
            idx += 1
        elif arg in ("-R", "--repo"):
            repo = following
            idx += 1
        elif arg.startswith("--ref="):
            ref = arg.split("=", 1)[1]
        elif arg.startswith("--repo="):
            repo = arg.split("=", 1)[1]
        elif arg in ("-f", "-F", "--field", "--raw-field"):
            if "=" in following:
                key, _, value = following.partition("=")
                (typed if arg in _TYPED_FIELD_FLAGS else raw)[key] = value
            idx += 1
        elif match := _FIELD_FLAG.fullmatch(arg):
            (raw if match.group(1) else typed)[match.group(2)] = match.group(3)
        elif match := _JOINED_FIELD.fullmatch(arg):
            (typed if match.group(1) == "F" else raw)[match.group(2)] = match.group(3)
        elif match := _JOINED_FIELD_EQ.fullmatch(arg):
            if "=" in match.group(2):
                key, _, value = match.group(2).partition("=")
                (typed if match.group(1) == "F" else raw)[key] = value
        elif match := _JOINED_REF.fullmatch(arg):
            ref = match.group(1).removeprefix("=")
        elif arg.startswith("-"):
            pass
        elif selector is None:
            selector = arg
        idx += 1
    if selector is None or not _is_workflow(selector):
        return None
    return {"ref": ref, "fields": {**raw, **typed}, "json": json_inputs, "repo": repo}


def _parse_rerun(tokens: list[str]) -> tuple[str | None, str | None] | None:
    if len(tokens) < 4 or tokens[1] != "run" or tokens[2] != "rerun":
        return None
    run_id = next((t for t in tokens[3:] if t.isdigit()), None)
    return run_id, _repo_flag(tokens)


def _parse_update_branch(tokens: list[str]) -> tuple[str | None, str | None] | None:
    if len(tokens) < 3 or tokens[1] != "pr" or "update-branch" not in tokens[2:]:
        return None
    rest = tokens[tokens.index("update-branch") + 1:]
    number = next((t for t in rest if t.isdigit()), None)
    return number, _repo_flag(tokens)


# --- gh / git access (fail open) ----------------------------------------------

def _run(cmd: list[str], cwd: str | None = None) -> str | None:
    """The module's only process boundary (D1): stdout on exit 0, else None."""
    try:
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                                encoding="utf-8", errors="replace", timeout=20,
                                check=False)
    except (OSError, subprocess.SubprocessError, ValueError):
        return None
    return result.stdout if result.returncode == 0 else None


def _gh_prefix(repo: str | None) -> list[str]:
    return ["gh", "-R", repo] if repo else ["gh"]


def _loads_json(out: str | None):
    if out is None:
        return None
    try:
        return json.loads(out)
    except ValueError:
        return None


def _gh_runs(repo: str | None, *, branch: str, event: str | None,
             cwd: str | None) -> list[dict] | None:
    if not branch:
        return None
    cmd = _gh_prefix(repo) + ["run", "list", "--workflow", WORKFLOW_FILE,
                              "--branch", branch]
    if event:
        cmd += ["--event", event]
    cmd += ["--limit", "30", "--json", RUN_FIELDS]
    data = _loads_json(_run(cmd, cwd=cwd))
    if not isinstance(data, list):
        return None
    return [r for r in data if isinstance(r, dict) and _is_ours(r)]


def _open_pr_numbers(repo: str | None, branch: str, cwd: str | None) -> set[str] | None:
    cmd = _gh_prefix(repo) + ["pr", "list", "--head", branch, "--state", "open",
                              "--json", "number"]
    data = _loads_json(_run(cmd, cwd=cwd))
    if not isinstance(data, list):
        return None
    return {str(pr.get("number")) for pr in data if isinstance(pr, dict)}


def _gh_run_view(repo: str | None, run_id: str, cwd: str | None) -> dict | None:
    cmd = _gh_prefix(repo) + ["run", "view", run_id, "--json", VIEW_FIELDS]
    data = _loads_json(_run(cmd, cwd=cwd))
    return data if isinstance(data, dict) and data else None


def _pr_head_branch(repo: str | None, number: str | None, cwd: str | None) -> str:
    cmd = _gh_prefix(repo) + ["pr", "view"]
    if number:
        cmd.append(str(number))
    cmd += ["--json", "headRefName"]
    data = _loads_json(_run(cmd, cwd=cwd))
    if isinstance(data, dict):
        return str(data.get("headRefName") or "")
    return ""


def _default_branch(repo: str | None, cwd: str | None) -> str:
    """The branch `gh workflow run` dispatches when no --ref is given (D7)."""
    cmd = ["gh", "repo", "view"] + ([repo] if repo else []) \
        + ["--json", "defaultBranchRef"]
    data = _loads_json(_run(cmd, cwd=cwd))
    if isinstance(data, dict):
        ref = data.get("defaultBranchRef")
        name = ref.get("name") if isinstance(ref, dict) else None
        if name:
            return str(name)
    out = _run(["git", "symbolic-ref", "--short", "refs/remotes/origin/HEAD"],
               cwd=cwd)
    return (out or "").strip().removeprefix("origin/")


def _remote_sha(repo: str | None, ref: str, cwd: str | None) -> str:
    if re.fullmatch(r"[0-9a-f]{40}", ref):
        return ref
    ref = ref.removeprefix("refs/heads/")
    if repo:
        out = _run(["gh", "api", f"repos/{repo}/commits/{ref}", "--jq", ".sha"],
                   cwd=cwd)
        return out.strip() if out and out.strip() else ""
    out = _run(["git", "ls-remote", "origin", f"refs/heads/{ref}"], cwd=cwd)
    return out.split()[0] if out and out.split() else ""


def _current_branch(cwd: str | None) -> str:
    out = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=cwd)
    return (out or "").strip()


def _local_branches(cwd: str | None) -> list[str]:
    out = _run(["git", "for-each-ref", "--format=%(refname:short)", "refs/heads/"],
               cwd=cwd)
    return [line.strip() for line in (out or "").splitlines() if line.strip()]


def _commit_message(rev: str, cwd: str | None) -> str | None:
    return _run(["git", "log", "-1", "--format=%B", rev], cwd=cwd)


# --- action evaluation --------------------------------------------------------

def _push_reason(specs: list[tuple[str, str | None]], repo: str | None,
                 dir_now: str, *, trust_skip_ci: bool) -> str | None:
    """Refusal for the resolved (branch, tip-source) push specs, or None."""
    for branch, source in specs:
        runs = _gh_runs(repo, branch=branch, event="pull_request", cwd=dir_now)
        if runs is None:
            continue
        live = [r for r in runs if r.get("status") in IN_FLIGHT]
        if not live:
            continue
        if trust_skip_ci and source:
            message = _commit_message(source, dir_now)
            if message is not None and _has_skip_ci(message):
                continue
        reason = push_refusal(branch, live,
                              open_numbers=_open_pr_numbers(repo, branch, dir_now))
        if reason:
            return reason
    return None


def _resolve_ref(ref: str, repo: str | None, dir_now: str) -> str:
    """The branch a --ref token names; no --ref means the default branch (D7)."""
    if ref.startswith("$(") or ref.startswith("`"):
        return _current_branch(dir_now).removeprefix("refs/heads/")
    if ref.startswith("$"):
        return ""
    if ref:
        return ref.removeprefix("refs/heads/")
    return _default_branch(repo, dir_now)


def _dispatch_reason(parsed: dict, dir_now: str, pushed: list[str]) -> str | None:
    """Refusal for one parsed `gh workflow run` segment, or None to allow it."""
    mode = str(parsed["fields"].get("mode") or DEFAULT_MODE)
    cases = str(parsed["fields"].get("cases") or "")
    if cases and not cases.strip():
        # The workflow's concurrency group treats any non-empty `cases` as
        # diagnostic, so this would cancel a live diagnostic run (F32).
        return ("Refused: `cases` is whitespace only. The workflow would queue it in "
                "the diagnostic concurrency group (cancelling any live diagnostic run) "
                "without selecting a subset. Pass a pytest -k expression, or omit "
                "`cases` for a full run.")
    diagnostic = bool(cases)
    reason: str | None = None
    ref = "" if parsed["json"] else _resolve_ref(parsed["ref"], parsed["repo"],
                                                 dir_now)
    runs = None
    if not parsed["json"] and mode in ("s2", "s3") and ref:
        runs = _gh_runs(parsed["repo"], branch=ref, event="workflow_dispatch",
                        cwd=dir_now)
    if diagnostic and mode == "s2":
        reason = S2_CASES_NOTE
    elif runs is not None:
        reason = dispatch_cancel_refusal(ref, runs, diagnostic=diagnostic)
        if reason is None and not diagnostic and ref not in pushed:
            sha = _remote_sha(parsed["repo"], ref, dir_now)
            reason = dispatch_redundancy_refusal(sha, runs, mode=mode) if sha else None
    return reason


def _rerun_reason(run_id: str | None, repo: str | None, dir_now: str) -> str | None:
    if not run_id:
        return None
    view = _gh_run_view(repo, run_id, dir_now)
    if view is None or not _is_ours(view):
        return None
    runs = _gh_runs(repo, branch=str(view.get("headBranch") or ""), event=None,
                    cwd=dir_now)
    if runs is None:
        return None
    return rerun_refusal(view, runs)


def _update_branch_reason(number: str | None, repo: str | None,
                          dir_now: str) -> str | None:
    """`gh pr update-branch` is a push to the PR's head branch."""
    head = _pr_head_branch(repo, number, dir_now)
    if not head:
        return None
    return _push_reason([(head, None)], repo, dir_now, trust_skip_ci=False)


def _git_segment(tokens: list[str], state: dict, guarded: bool) -> str | None:
    dir_now, subcommand, args = _git_split(tokens, state["dir"])
    if subcommand != "push":
        if subcommand in TIP_MOVERS:
            state["mover"] = True
        return None
    mode, specs = _push_specs(args)
    if mode == "all":
        specs = [(branch, branch) for branch in _local_branches(dir_now)]
        mode = "specs"
    resolved = _resolve_specs(specs, dir_now) if mode == "specs" else []
    state["pushed"].extend(branch for branch, _ in resolved)
    if not guarded or not resolved:
        return None
    return _push_reason(resolved, None, dir_now, trust_skip_ci=not state["mover"])


def _hoist_repo_flag(tokens: list[str]) -> list[str]:
    """Move gh's inherited `-R/--repo` from before the subcommand to the end (F30).

    `gh -R owner/repo workflow run …` is valid; every parser below looks for the
    subcommand at `tokens[1]` and reads `-R` anywhere after it.
    """
    head, rest, moved = tokens[:1], tokens[1:], []
    while rest and rest[0].startswith("-"):
        if rest[0] in ("-R", "--repo") and len(rest) > 1:
            moved, rest = [*moved, "-R", rest[1]], rest[2:]
        elif rest[0].startswith("--repo="):
            moved, rest = [*moved, "-R", rest[0].split("=", 1)[1]], rest[1:]
        else:
            break
    return [*head, *rest, *moved]


def _gh_segment(tokens: list[str], state: dict, guarded: bool) -> str | None:
    tokens = _hoist_repo_flag(tokens)
    dispatch = _parse_dispatch(tokens)
    if dispatch is not None:
        return _dispatch_reason(dispatch, state["dir"], state["pushed"]) if guarded else None
    rerun = _parse_rerun(tokens)
    if rerun is not None:
        return _rerun_reason(rerun[0], rerun[1], state["dir"]) if guarded else None
    update = _parse_update_branch(tokens)
    if update is not None:
        return _update_branch_reason(update[0], update[1], state["dir"]) if guarded else None
    return None


def _eval_segment(tokens: list[str], state: dict, self_override: bool) -> str | None:
    head = os.path.basename(tokens[0]).removesuffix(".exe")
    if head == "cd":
        state["dir"] = _join_dir(state["dir"], tokens[1] if len(tokens) > 1 else "")
        return None
    if head == "export":
        if OVERRIDE in tokens[1:]:
            state["export_override"] = True
        return None
    guarded = not (self_override or state["export_override"])
    if head == "git":
        return _git_segment(tokens, state, guarded)
    if head == "gh":
        return _gh_segment(tokens, state, guarded)
    return None


def refusal_for_command(command: str, cwd: str | None = None) -> str | None:
    """Reason to refuse `command` run from `cwd`, or None when it may run."""
    state = {"dir": (cwd or "").replace("\\", "/"), "pushed": [],
             "mover": False, "export_override": False}
    for raw in _segments(command):
        self_override = _override_on_segment(raw)
        for tokens in _expand(_strip_assignments(raw)):
            if tokens:
                reason = _eval_segment(tokens, state, self_override)
                if reason:
                    return reason
    return None


# --- entry points (D2) --------------------------------------------------------

def _mcp_refusal(tool: str, tool_input: dict, cwd: str | None) -> str | None:
    owner, name = tool_input.get("owner"), tool_input.get("repo")
    repo = f"{owner}/{name}" if owner and name else None
    if tool == "actions_run_trigger":
        method = str(tool_input.get("method") or "")
        if method == "run_workflow":
            inputs = tool_input.get("inputs")
            inputs = inputs if isinstance(inputs, dict) else {}
            if not _is_workflow(str(tool_input.get("workflow_id") or "")):
                return None
            parsed = {"ref": str(tool_input.get("ref") or ""),
                      "fields": {"mode": inputs.get("mode", ""),
                                 "cases": inputs.get("cases", "")},
                      "json": False, "repo": repo}
            return _dispatch_reason(parsed, cwd, [])
        if method in ("rerun_workflow_run", "rerun_failed_jobs"):
            return _rerun_reason(str(tool_input.get("run_id") or ""), repo, cwd)
        return None
    if tool == "update_pull_request_branch":
        return _update_branch_reason(str(tool_input.get("pullNumber") or ""),
                                      repo, cwd)
    branch = str(tool_input.get("branch") or "")
    if branch and not _has_skip_ci(str(tool_input.get("message") or "")):
        return _push_reason([(branch, None)], repo, cwd, trust_skip_ci=False)
    return None


def _hook_refusal(data) -> str | None:
    if not isinstance(data, dict):
        return None
    name = str(data.get("tool_name") or "")
    tool_input = data.get("tool_input")
    tool_input = tool_input if isinstance(tool_input, dict) else {}
    if name.startswith("mcp__github__"):
        tool = name.removeprefix("mcp__github__")
        if tool not in MCP_TOOLS:
            return None
        return _mcp_refusal(tool, tool_input, data.get("cwd"))
    command = str(tool_input.get("command") or "")
    if not command:
        return None
    return refusal_for_command(command, cwd=data.get("cwd"))


def claude_hook(stdin) -> int:
    """PreToolUse: print a deny only when refusing; never print an approval."""
    try:
        reason = _hook_refusal(json.load(stdin))
    except Exception:  # bad JSON, guard bug, exploded subprocess: all silent
        reason = None
    if reason:
        sys.stdout.write(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason}}))
    return 0


def pre_push(stdin) -> int:
    """git pre-push: exit 1 only when refusing, with the override in stderr."""
    if os.environ.get("FP_S2_GUARD") == "off":
        return 0
    for line in stdin:
        try:
            parts = line.split()
            if len(parts) != 4 or not parts[2].startswith("refs/heads/") \
                    or set(parts[1]) == {"0"}:
                continue
            branch = parts[2].removeprefix("refs/heads/")
            reason = _push_reason([(branch, parts[1])], None, None,
                                  trust_skip_ci=True)
            if reason:
                print(f"pre-push: {reason}", file=sys.stderr)
                return 1
        except Exception:
            continue
    return 0


def main(argv: list[str] | None = None) -> int:
    mode = (argv if argv is not None else sys.argv[1:])[:1]
    if mode == ["claude-hook"]:
        return claude_hook(sys.stdin)
    if mode == ["pre-push"]:
        return pre_push(sys.stdin)
    print("usage: guard_s2_runs.py claude-hook|pre-push", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
