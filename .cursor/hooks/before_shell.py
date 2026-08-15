#!/usr/bin/env python3
"""Cursor beforeShellExecution guard — mirrors the hookify bash rules.

Surfaces (does NOT hard-deny) two classes of command so the operator confirms
before they run:

  * Git hook / signing bypass: ``--no-verify`` / ``--no-gpg-sign`` — not the
    standing path (CLAUDE.md Vendor-data integrity gate; git-workflow.mdc).
  * Destructive git / fs: ``reset --hard``, ``clean -f``, ``checkout --``,
    force-push, ``branch -D``, ``rm -rf`` — the standing safety rule wants a
    ``git status`` + stash/commit first.

Contract: reads Cursor's beforeShellExecution JSON on stdin, writes a decision
JSON on stdout. Returns ``ask`` on a match, ``allow`` otherwise. Fail-open:
any parse error → allow (never blocks an unrelated command). This is a warn-
class gate — ``ask`` keeps the operator in control; it never denies outright,
matching the "unless Joshua explicitly asked" carve-out.
"""
from __future__ import annotations

import json
import re
import sys

NO_VERIFY = re.compile(r"--no-verify|--no-gpg-sign")
DESTRUCTIVE = re.compile(
    r"git\s+reset\s+--hard"
    r"|git\s+clean\s+-[a-zA-Z]*f"
    r"|git\s+checkout\s+--"
    r"|git\s+push\b.*--force"
    r"|git\s+push\b.*\s-f(\s|$)"
    r"|git\s+branch\s+-D"
    r"|rm\s+-rf"
)


def _command(data: dict) -> str:
    if not isinstance(data, dict):
        return ""
    for key in ("command", "shell_command", "cmd"):
        val = data.get(key)
        if isinstance(val, str) and val:
            return val
    tool_input = data.get("tool_input")
    if isinstance(tool_input, dict):
        val = tool_input.get("command")
        if isinstance(val, str):
            return val
    return ""


def _emit(permission: str, agent_msg: str = "", user_msg: str = "") -> None:
    out: dict = {"permission": permission}
    if agent_msg:
        out["agentMessage"] = agent_msg
    if user_msg:
        out["userMessage"] = user_msg
    sys.stdout.write(json.dumps(out))


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        _emit("allow")
        return 0

    cmd = _command(data)
    if not cmd:
        _emit("allow")
        return 0

    if NO_VERIFY.search(cmd):
        _emit(
            "ask",
            agent_msg=(
                "`--no-verify` / `--no-gpg-sign` skips the repo's pre-commit "
                "gate stack (see `scripts/githooks/pre-commit` for the current "
                "set — deliberately not enumerated here, it changes). Not the "
                "standing path — fix the hook failure and re-commit unless Joshua "
                "explicitly asked to bypass."
            ),
            user_msg="Command bypasses git hooks/signing. Confirm to proceed.",
        )
        return 0

    if DESTRUCTIVE.search(cmd):
        _emit(
            "ask",
            agent_msg=(
                "Destructive command — `git status` first and stash (`-u`) or "
                "commit anything present. Never force-push main; prefer "
                "--force-with-lease / git restore / a revert commit."
            ),
            user_msg="Potentially destructive git/fs command. Confirm to proceed.",
        )
        return 0

    _emit("allow")
    return 0


if __name__ == "__main__":
    sys.exit(main())
