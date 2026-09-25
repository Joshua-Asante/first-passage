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

  * ``pr.merge``     — ask: the GitHub MCP ``merge_pull_request`` tool; ``gh pr merge``;
                       a ``gh api`` call on a ``pulls/<n>/merge`` path or a
                       ``mergePullRequest`` GraphQL mutation.
  * ``pr.auto_merge``— deny: the GitHub MCP ``enable_pr_auto_merge`` tool;
                       ``gh pr merge --auto``; an ``enablePullRequestAutoMerge`` mutation.
                       Merge authority is the operator's with no automated exception.
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

MCP_ACTS = {
    "mcp__github__merge_pull_request": (ASK, "pr.merge"),
    "mcp__github__enable_pr_auto_merge": (DENY, "pr.auto_merge"),
}

MESSAGES = {
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
    "rail.arm": ("Arming the c1 rail is an operator act (rail.arm): M1 RESOLVED and a GO "
                 "for this armed session. Confirm to proceed.",
                 "Arming requires M1 RESOLVED and a per-session operator GO. Do not proceed "
                 "unless the operator confirms this prompt."),
}

_FALLBACK = (
    (re.compile(r"\bgh\b.*\bpr\s+merge\b.*--auto\b"), DENY, "pr.auto_merge"),
    (re.compile(r"enablePullRequestAutoMerge"), DENY, "pr.auto_merge"),
    (re.compile(r"\bgh\b.*\bpr\s+merge\b"), ASK, "pr.merge"),
    (re.compile(r"pulls/[^/\s]+/merge\b|mergePullRequest"), ASK, "pr.merge"),
    (re.compile(r"\b(fly|flyctl)\b.*\bdeploy\b"), ASK, "rail.deploy"),
    (re.compile(r"c1_rail_arm\S*\s.*--arm\b"), ASK, "rail.arm"),
)
_GH_GLOBAL_VALUES = frozenset({"-R", "--repo", "--hostname"})
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


def _judge_gh(args: list[str]) -> tuple[str, str] | None:
    words = _positional(args, _GH_GLOBAL_VALUES)
    if words[:2] == ["pr", "merge"]:
        if any(a == "--auto" or a.startswith("--auto=") for a in args):
            return DENY, "pr.auto_merge"
        return ASK, "pr.merge"
    if words[:1] == ["api"]:
        text = " ".join(args)
        if "enablePullRequestAutoMerge" in text:
            return DENY, "pr.auto_merge"
        if re.search(r"pulls/[^/\s]+/merge\b", text) or "mergePullRequest" in text:
            return ASK, "pr.merge"
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


def _judge_python(args: list[str]) -> tuple[str, str] | None:
    arms = "--arm" in args
    target = any(a.replace("\\", "/").endswith("c1_rail_arm.py") for a in args) or any(
        args[i] == "-m" and i + 1 < len(args) and args[i + 1].endswith("c1_rail_arm")
        for i in range(len(args)))
    return (ASK, "rail.arm") if arms and target else None


def _judge_segment(tokens: list[str]) -> tuple[str, str] | None:
    for words in expand(tokens, strict=True):
        if not words:
            continue
        base, args = program(words[0], strict=True), [str(w) for w in words[1:]]
        if base == "gh":
            found = _judge_gh(args)
        elif base in ("fly", "flyctl"):
            found = _judge_fly(args)
        elif _PYTHONS.fullmatch(base):
            found = _judge_python(args)
        elif base.endswith("c1_rail_arm.py"):
            found = (ASK, "rail.arm") if "--arm" in args else None
        else:
            found = None
        if found:
            return found
    return None


def classify_command(command: str) -> tuple[str, str] | None:
    """(decision, capability) for a Bash command, or None when it is not an operator act."""
    try:
        parsed = segments(command, strict=True)
    except (ShellSyntaxError, RecursionError):
        for pattern, decision, cap in _FALLBACK:
            if pattern.search(command):
                return decision, cap
        return None
    worst = None
    for tokens in parsed:
        found = _judge_segment([str(t) for t in tokens])
        if found and (worst is None or found[0] == DENY):
            worst = found
    return worst


def classify(payload: dict) -> tuple[str, str] | None:
    """(decision, capability) for a PreToolUse payload, or None."""
    name = payload.get("tool_name") or ""
    if name in MCP_ACTS:
        return MCP_ACTS[name]
    if name == "Bash":
        command = (payload.get("tool_input") or {}).get("command")
        if isinstance(command, str):
            return classify_command(command)
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        found = classify(payload) if isinstance(payload, dict) else None
    except Exception:  # fail-open: a broken hook must not block unrelated work
        return 0
    if found:
        decision, cap = found
        user_msg, agent_msg = MESSAGES[cap]
        sys.stdout.write(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
            "permissionDecisionReason": user_msg,
            "additionalContext": agent_msg,
        }}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
