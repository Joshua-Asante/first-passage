#!/usr/bin/env python3
"""guard_operator_acts.py — agent calls that would perform an operator act.

Rule owner: `docs/adr/2026-07-14-cc-cursor-surface-allocation.md` §Decision, "Action
classes and the authority block" (2026-09-25 revision). Capability ids in the messages
are the ones registered in `scripts/seat_authority.yml`.

Operator acts (risk ``high``) are performed by the operator through an act they already
perform. When an agent session reaches for one, this PreToolUse hook puts the call in
front of the operator (``ask``): the harness prompt is an authenticated operator
interaction, which a model's "the operator approved this" is not. A forbidden act is
refused outright (``deny``): no approval unlocks it for an agent.

  * ``pr.merge``     — ask, **only when pinned to a full 40-hex head SHA**: the GitHub MCP
                       ``merge_pull_request`` tool with ``expectedHeadSha``; ``gh pr merge
                       --match-head-commit <sha>``; a ``gh api`` call on a
                       ``pulls/<n>/merge`` path with a ``sha`` field, or a
                       ``mergePullRequest`` mutation with ``expectedHeadOid``. GitHub refuses
                       the merge if the head moved, so the operator's answer approves exactly
                       the bytes named in the prompt. An unpinned merge is denied with the
                       pinned form to use (``pr.merge_unpinned``).
  * ``pr.auto_merge``— deny: the GitHub MCP ``enable_pr_auto_merge`` tool;
                       ``gh pr merge --auto``; an ``enablePullRequestAutoMerge`` mutation.
                       Merge authority is the operator's with no automated exception.
  * ``main.direct_push`` — deny: ``git push`` with ``main`` as a destination (``main``,
                       ``HEAD:main``, ``+x:refs/heads/main``, ``--delete main``). ``main``
                       takes PRs only. A push with no refspec is not judged (the current
                       branch is not visible to the hook; branch protection covers it).
  * ``rail.deploy``  — ask: ``fly deploy`` / ``flyctl deploy``.
  * ``rail.arm``     — ask: ``c1_rail_arm.py --arm`` (as a script or ``-m`` module),
                       including inside ``fly ssh console -C '…'``. ``--disarm`` and
                       ``--status`` never ask: disarming is a risk-reducing exit and must
                       never wait on a prompt.

**Scope — what this hook is not.** It is one enforcement point among the ones the ADR
names, for the Claude Code harness only. Credentials held off agent environments,
GitHub branch protection and the arming interlock in `ops/c1_rail/c1_rail_arm.py`
stay the boundaries; this hook adds a prompt where an agent session holds a credential
that could otherwise act. It cannot see ``trade.submit``: that is enforced by the
trading credentials never being present in an agent environment.

**Reading commands.** Bash commands are read with `scripts/_shell_tokens.py` in strict
mode, judging words in command position (wrappers, ``bash -c`` scripts and ``$(…)``
bodies are expanded by that module), so a commit message or grep pattern that mentions
``gh pr merge`` does not prompt. A command the tokenizer cannot read falls back to raw
regexes and asks — toward asking, as `guard_shell_command.py` does.

Contract: JSON on stdin (``tool_name``, ``tool_input``); on a match, Claude Code's
PreToolUse decision JSON on stdout; on anything else, nothing (a hook ``allow`` would
override the operator's permission settings). Fail-open on malformed input.
"""
from __future__ import annotations

import json
import re
import sys

try:  # imported as `scripts.guard_operator_acts` (tests, repo root on sys.path)
    from scripts._shell_tokens import ShellSyntaxError, expand, program, segments
except ImportError:  # run as `python scripts/guard_operator_acts.py`
    from _shell_tokens import ShellSyntaxError, expand, program, segments

ASK, DENY = "ask", "deny"

MCP_MERGE = "mcp__github__merge_pull_request"
MCP_AUTO_MERGE = "mcp__github__enable_pr_auto_merge"
_SHA = re.compile(r"[0-9a-fA-F]{40}")

MESSAGES = {
    "pr.merge_unpinned": ("Merge refused: not pinned to a head SHA (pr.merge). Re-issue it "
                          "pinned so the approval covers exact bytes.",
                          "An operator approval must bind to the exact head. Re-issue the "
                          "merge pinned to the full 40-hex head SHA the operator reviewed: MCP "
                          "`expectedHeadSha`, `gh pr merge --match-head-commit <sha>`, a REST "
                          "`sha` field, or GraphQL `expectedHeadOid`."),
    "pr.merge": ("Merging is an operator act (pr.merge). Confirm only if you, the operator, "
                 "are merging this PR now.",
                 "Merge authority is the operator's (surface-allocation ADR). Do not merge "
                 "unless the operator confirms this prompt; otherwise report the PR as "
                 "ready and stop."),
    "pr.auto_merge": ("Auto-merge is forbidden to agents (pr.auto_merge).",
                      "Auto-merge is retired: merge authority is the operator's with no "
                      "automated exception. Report the PR as ready instead."),
    "rail.deploy": ("Deploying the c1 rail is an operator act (rail.deploy). Confirm to "
                    "proceed.",
                    "A rail deploy is an operator act. Do not proceed unless the operator "
                    "confirms this prompt."),
    "main.direct_push": ("Pushing to main is forbidden (main.direct_push): main takes PRs "
                         "only.",
                         "`main` requires a PR and the required status; a direct push "
                         "bypasses both. Push a `glm/`, `codex/` or `claude/` branch and "
                         "open a PR."),
    "rail.arm": ("Arming the c1 rail is an operator act (rail.arm): M1 RESOLVED and a GO "
                 "for this armed session. Confirm to proceed.",
                 "Arming requires M1 RESOLVED and a per-session operator GO. Do not proceed "
                 "unless the operator confirms this prompt."),
}

_FALLBACK = (
    (re.compile(r"\bgh\b.*\bpr\s+merge\b.*--auto\b"), DENY, "pr.auto_merge"),
    (re.compile(r"enablePullRequestAutoMerge"), DENY, "pr.auto_merge"),
    (re.compile(r"\bgh\b.*\bpr\s+merge\b"), DENY, "pr.merge_unpinned"),
    (re.compile(r"pulls/[^/\s]+/merge\b|mergePullRequest"), DENY, "pr.merge_unpinned"),
    (re.compile(r"\b(fly|flyctl)\b.*\bdeploy\b"), ASK, "rail.deploy"),
    (re.compile(r"c1_rail_arm\S*\s.*--arm\b"), ASK, "rail.arm"),
)
_GH_GLOBAL_VALUES = frozenset({"-R", "--repo", "--hostname"})
_GIT_GLOBAL_VALUES = frozenset({"-C", "-c", "--git-dir", "--work-tree", "--namespace",
                                "--config-env", "--exec-path"})
# Push options that take their value as the next word. `--signed` and
# `--force-with-lease` take one only after `=`, and `--force-if-includes` none.
_GIT_PUSH_VALUES = frozenset({"-o", "--push-option", "--receive-pack", "--exec",
                              "--repo", "--recurse-submodules"})
_MAIN = frozenset({"main", "refs/heads/main"})
_FLY_COMMAND_OPTS = frozenset({"-C", "--command"})
_PYTHONS = re.compile(r"(python(\d+(\.\d+)?)?|py|pypy3?)")


def _positional(args: list[str], takes_value: frozenset[str]) -> list[str]:
    """`args` without options (and the values of the options in `takes_value`)."""
    out, skip = [], False
    for arg in args:
        if skip:
            skip = False
        elif arg in takes_value:
            skip = True
        elif not arg.startswith("-"):
            out.append(arg)
    return out


def _option_value(args: list[str], name: str) -> str | None:
    for i, arg in enumerate(args):
        if arg == name and i + 1 < len(args):
            return args[i + 1]
        if arg.startswith(name + "="):
            return arg.split("=", 1)[1]
    return None


def _pinned(ok: bool) -> tuple[str, str]:
    return (ASK, "pr.merge") if ok else (DENY, "pr.merge_unpinned")


def _judge_gh(args: list[str]) -> tuple[str, str] | None:
    words = _positional(args, _GH_GLOBAL_VALUES)
    if words[:2] == ["pr", "merge"]:
        if any(a == "--auto" or a.startswith("--auto=") for a in args):
            return DENY, "pr.auto_merge"
        sha = _option_value(args, "--match-head-commit")
        return _pinned(bool(sha and _SHA.fullmatch(sha)))
    if words[:1] == ["api"]:
        text = " ".join(args)
        if "enablePullRequestAutoMerge" in text:
            return DENY, "pr.auto_merge"
        if "mergePullRequest" in text:
            return _pinned(bool(re.search(r"expectedHeadOid\W+[0-9a-fA-F]{40}\b", text)))
        if re.search(r"pulls/[^/\s]+/merge\b", text):
            return _pinned(any(re.fullmatch(r"sha=[0-9a-fA-F]{40}", a) for a in args))
    return None


def _judge_fly(args: list[str]) -> tuple[str, str] | None:
    for i, arg in enumerate(args):
        value = None
        if arg in _FLY_COMMAND_OPTS and i + 1 < len(args):
            value = args[i + 1]
        elif arg.startswith("--command="):
            value = arg.split("=", 1)[1]
        if value is not None:
            found = classify_command(value)
            if found:
                return found
    if "deploy" in _positional(args, frozenset({"-a", "--app", "-c", "--config"}))[:1]:
        return ASK, "rail.deploy"
    return None


def _judge_git(args: list[str]) -> tuple[str, str] | None:
    """`git push` whose destination is `main` — by refspec, bare branch or `--delete`.

    A push with no refspec pushes the current branch, which this guard cannot see;
    that case stays with branch protection.
    """
    words = _positional(args, _GIT_GLOBAL_VALUES)
    if words[:1] != ["push"]:
        return None
    push_args = args[args.index("push") + 1:]
    words = _positional(push_args, _GIT_PUSH_VALUES)
    # `--repo` names the remote, so every positional word is then a refspec.
    has_repo = any(a == "--repo" or a.startswith("--repo=") for a in push_args)
    refspecs = words if has_repo else words[1:]  # after the remote
    for spec in refspecs:
        dst = spec.split(":", 1)[1] if ":" in spec else spec
        if dst.lstrip("+") in _MAIN:
            return DENY, "main.direct_push"
    return None


def _judge_python(args: list[str]) -> tuple[str, str] | None:
    arms = "--arm" in args
    target = any(a.replace("\\", "/").endswith("c1_rail_arm.py") for a in args) or any(
        args[i] == "-m" and i + 1 < len(args) and args[i + 1].endswith("c1_rail_arm")
        for i in range(len(args)))
    return (ASK, "rail.arm") if arms and target else None


def _worst(found: list[tuple[str, str]]) -> tuple[str, str] | None:
    """A deny anywhere wins over any ask: one wrapper cannot launder a forbidden act."""
    for item in found:
        if item[0] == DENY:
            return item
    return found[0] if found else None


def _judge_segment(tokens: list[str]) -> tuple[str, str] | None:
    hits: list[tuple[str, str]] = []
    for words in expand(tokens, strict=True):
        if not words:
            continue
        base, args = program(words[0], strict=True), [str(w) for w in words[1:]]
        if base == "gh":
            found = _judge_gh(args)
        elif base in ("fly", "flyctl"):
            found = _judge_fly(args)
        elif base == "git":
            found = _judge_git(args)
        elif _PYTHONS.fullmatch(base):
            found = _judge_python(args)
        elif base.endswith("c1_rail_arm.py"):
            found = (ASK, "rail.arm") if "--arm" in args else None
        else:
            found = None
        if found:
            hits.append(found)
    return _worst(hits)


def classify_command(command: str) -> tuple[str, str] | None:
    """(decision, capability) for a Bash command, or None when it is not an operator act."""
    try:
        parsed = segments(command, strict=True)
    except (ShellSyntaxError, RecursionError):
        for pattern, decision, cap in _FALLBACK:
            if pattern.search(command):
                return decision, cap
        return None
    hits = [f for f in (_judge_segment([str(t) for t in tokens]) for tokens in parsed) if f]
    return _worst(hits)


def classify(payload: dict) -> tuple[str, str] | None:
    """(decision, capability) for a PreToolUse payload, or None."""
    name = payload.get("tool_name") or ""
    tool_input = payload.get("tool_input") or {}
    if name == MCP_AUTO_MERGE:
        return DENY, "pr.auto_merge"
    if name == MCP_MERGE:
        sha = tool_input.get("expectedHeadSha")
        return _pinned(isinstance(sha, str) and bool(_SHA.fullmatch(sha)))
    if name == "Bash":
        command = tool_input.get("command")
        if isinstance(command, str):
            return classify_command(command)
    return None


def _pinned_sha(payload: dict) -> str | None:
    """The head SHA a merge call pins, shown in the operator's prompt."""
    tool_input = payload.get("tool_input") or {}
    if payload.get("tool_name") == MCP_MERGE:
        return tool_input.get("expectedHeadSha")
    match = _SHA.search(str(tool_input.get("command", "")))
    return match.group(0) if match else None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        found = classify(payload) if isinstance(payload, dict) else None
    except Exception:  # fail-open: a broken hook must not block unrelated work
        return 0
    if found:
        decision, cap = found
        user_msg, agent_msg = MESSAGES[cap]
        sha = _pinned_sha(payload) if (decision, cap) == (ASK, "pr.merge") else None
        if sha:
            user_msg += f" Head SHA being approved: {sha}."
        sys.stdout.write(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
            "permissionDecisionReason": user_msg,
            "additionalContext": agent_msg,
        }}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
