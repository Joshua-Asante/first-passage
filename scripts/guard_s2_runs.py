"""guard_s2_runs.py — refuse the two S2-loop moves that wasted hosted runs in S2.

Why: an S2 supervision run is ~25 min on a fresh host. During S2 (2026-09-19/21)
three runs were cancelled by pushes to a PR branch mid-run (the pull_request
run's `cancel-in-progress` concurrency kills it on every new push, docs-only
pushes included), and same-SHA re-dispatches re-rolled a real race instead of
root-causing it (`.claude/skills/s2-linux-run/SKILL.md` §1, §3). Both are
knowable before the command runs, so refuse them then.

Refusals:
  * **push** — a `git push` to a branch whose `pull_request` S2 run is queued or
    in progress. Dispatched runs (own concurrency group) are not cancelled by a
    push and are not counted.
  * **dispatch** — a full (non-`cases`) `gh workflow run qualification-s2-supervision`
    on a SHA that already has an S2 run in flight, or a completed run that
    passed (you already have the evidence) or failed (a failure on unchanged
    code is a finding, not a re-roll). Cancelled/skipped/timed-out runs do not
    count. `cases` diagnostic dispatches are never refused.

Override: put `FP_S2_GUARD=off` in the command (Claude hook) or the environment
(git hook) — for a deliberate cancel or a re-dispatch whose reason you can state.

Entry points (both fail open — no `gh`, offline, unparseable input → allow):
  * `python scripts/guard_s2_runs.py claude-hook` — Claude Code PreToolUse Bash
    hook (`.claude/settings.json`); stdin is the tool payload, stdout the
    `hookSpecificOutput.permissionDecision` JSON (shape as in guard_shell_command.py).
  * `python scripts/guard_s2_runs.py pre-push` — from `scripts/githooks/pre-push`;
    stdin is git's `<local ref> <local sha> <remote ref> <remote sha>` lines;
    exit 1 refuses the push. This layer covers every harness, not only Claude.

`push_refusal()` and `dispatch_refusal()` are the pure functions the tests pin.
"""
from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
import sys

WORKFLOW = "qualification-s2-supervision.yml"
IN_FLIGHT = {"queued", "in_progress", "waiting", "requested", "pending"}
DEFINITIVE = {"success", "failure"}
DIAGNOSTIC_TITLE = "S2 DIAGNOSTIC"
OVERRIDE = "FP_S2_GUARD=off"
_SEGMENT = re.compile(r"&&|\|\||;|\||\n")


def _is_diagnostic(run: dict) -> bool:
    return str(run.get("displayTitle", "")).startswith(DIAGNOSTIC_TITLE)


def push_refusal(branch: str, runs: list[dict]) -> str | None:
    """Reason to refuse a push to `branch`, given its recent S2 runs, else None."""
    live = [r for r in runs if r.get("event") == "pull_request" and r.get("status") in IN_FLIGHT]
    if not live:
        return None
    ids = ", ".join(str(r.get("databaseId")) for r in live)
    return (f"S2 run {ids} is in flight on the pull request for '{branch}'; a push now "
            f"refires the workflow and cancel-in-progress kills that run (~25 min lost). "
            f"Commit locally and push after it finishes (docs commits included). "
            f"Deliberate cancel: prefix the command with {OVERRIDE}.")


def dispatch_refusal(sha: str, runs: list[dict], *, diagnostic: bool) -> str | None:
    """Reason to refuse a full S2 dispatch on `sha`, else None."""
    if diagnostic or not sha:
        return None
    same = [r for r in runs if r.get("headSha") == sha and not _is_diagnostic(r)]
    live = [r for r in same if r.get("status") in IN_FLIGHT]
    if live:
        return (f"S2 run {live[0].get('databaseId')} is already in flight on {sha[:12]}; a second "
                f"full run on the same bytes adds nothing. Wait for it and read its artifact.")
    done = [r for r in same if r.get("status") == "completed" and r.get("conclusion") in DEFINITIVE]
    if not done:
        return None
    run = done[0]
    if run.get("conclusion") == "success":
        return (f"S2 run {run.get('databaseId')} already passed on {sha[:12]}; read its artifact "
                f"(scripts/s2_run_evidence.py {run.get('databaseId')}) instead of re-running.")
    return (f"S2 run {run.get('databaseId')} already failed on {sha[:12]}. A failure on unchanged "
            f"code is a finding, not a re-roll: root-cause it from the artifact (s2-linux-run §3), or "
            f"iterate on one case with -f cases='<expr>'. Justified re-dispatch: prefix {OVERRIDE}.")


# --- command parsing --------------------------------------------------------

def _segments(command: str) -> list[list[str]]:
    out = []
    for part in _SEGMENT.split(command):
        try:
            tokens = shlex.split(part)
        except ValueError:
            continue
        while tokens and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", tokens[0]):
            tokens = tokens[1:]  # leading VAR=value assignments
        if tokens:
            out.append(tokens)
    return out


def _git_push_branches(tokens: list[str]) -> list[str] | None:
    """Destination branches of a `git ... push ...`; [] means the current branch."""
    if not tokens or os.path.basename(tokens[0]) != "git":
        return None
    i = 1
    while i < len(tokens) and tokens[i].startswith("-"):  # global options: -C <path>, -c <k=v>, --no-pager
        i += 2 if tokens[i] in ("-C", "-c", "--git-dir", "--work-tree", "--namespace") else 1
    if i >= len(tokens) or tokens[i] != "push":
        return None
    args = tokens[i + 1:]
    positional, skip = [], False
    for arg in args:
        if skip:
            skip = False
            continue
        if arg in ("-o", "--push-option", "--repo", "--receive-pack", "--exec"):
            skip = True
            continue
        if arg.startswith("-"):
            continue
        positional.append(arg)
    branches = []
    for spec in positional[1:]:  # positional[0] is the remote
        dst = spec.lstrip("+").split(":")[-1]
        if dst and dst != "HEAD":
            branches.append(dst.removeprefix("refs/heads/"))
    return branches


def _gh_dispatch(tokens: list[str]) -> tuple[str, bool] | None:
    """(ref, diagnostic) for `gh workflow run <S2 workflow> ...`, else None."""
    if len(tokens) < 4 or os.path.basename(tokens[0]) != "gh" or tokens[1:3] != ["workflow", "run"]:
        return None
    if tokens[3] not in (WORKFLOW, WORKFLOW.removesuffix(".yml"), "Qualification S2 supervision"):
        return None
    ref, diagnostic, args = "", False, tokens[4:]
    for i, arg in enumerate(args):
        value = args[i + 1] if i + 1 < len(args) else ""
        if arg in ("--ref", "-r"):
            ref = value
        elif arg.startswith("--ref="):
            ref = arg.split("=", 1)[1]
        elif arg in ("-f", "-F", "--field", "--raw-field"):
            if value.startswith("cases=") and value.split("=", 1)[1].strip():
                diagnostic = True
        elif re.match(r"(--field|--raw-field)=cases=\S", arg):
            diagnostic = True
    return ref, diagnostic


# --- gh / git access (fail open) --------------------------------------------

def _run(cmd: list[str]) -> str | None:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=20, check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout if result.returncode == 0 else None


def _runs(branch: str) -> list[dict] | None:
    out = _run(["gh", "run", "list", "--workflow", WORKFLOW, "--branch", branch, "--limit", "30",
                "--json", "databaseId,headSha,status,conclusion,event,displayTitle"])
    try:
        return json.loads(out) if out is not None else None
    except ValueError:
        return None


def _current_branch() -> str:
    out = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    return (out or "").strip()


def _remote_sha(ref: str) -> str:
    if re.fullmatch(r"[0-9a-f]{40}", ref):
        return ref
    out = _run(["git", "ls-remote", "origin", f"refs/heads/{ref}"])
    return out.split()[0] if out and out.split() else ""


# --- entry points -----------------------------------------------------------

def refusal_for_command(command: str) -> str | None:
    if OVERRIDE in command:
        return None
    for tokens in _segments(command):
        branches = _git_push_branches(tokens)
        if branches is not None:
            for branch in branches or [_current_branch()]:
                runs = _runs(branch) if branch and branch != "HEAD" else None
                reason = push_refusal(branch, runs) if runs else None
                if reason:
                    return reason
        dispatch = _gh_dispatch(tokens)
        if dispatch is not None:
            ref, diagnostic = dispatch
            ref = ref or _current_branch()
            if diagnostic or not ref:
                continue
            runs = _runs(ref)
            reason = dispatch_refusal(_remote_sha(ref), runs, diagnostic=False) if runs else None
            if reason:
                return reason
    return None


def claude_hook(stdin) -> int:
    try:
        command = str((json.load(stdin).get("tool_input") or {}).get("command", ""))
        reason = refusal_for_command(command)
    except Exception:
        reason = None
    block: dict = {"hookEventName": "PreToolUse", "permissionDecision": "deny" if reason else "allow"}
    if reason:
        block["permissionDecisionReason"] = reason
    sys.stdout.write(json.dumps({"hookSpecificOutput": block}))
    return 0


def pre_push(stdin) -> int:
    if os.environ.get("FP_S2_GUARD") == "off":
        return 0
    for line in stdin:
        parts = line.split()
        if len(parts) != 4 or not parts[2].startswith("refs/heads/") or set(parts[1]) == {"0"}:
            continue
        branch = parts[2].removeprefix("refs/heads/")
        runs = _runs(branch)
        reason = push_refusal(branch, runs) if runs else None
        if reason:
            print(f"pre-push: {reason.replace('prefix the command with', 'set')}", file=sys.stderr)
            return 1
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
