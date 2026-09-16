#!/usr/bin/env python3
"""guard_shell_command.py — surface hook-bypass and destructive shell commands.

Ported 2026-09-15 from `.cursor/hooks/before_shell.py`, whose carrier (the
`.cursor/` harness) is removed by the Cursor retirement
(`docs/adr/2026-07-14-cc-cursor-surface-allocation.md`, Revision 2026-09-15).
The *discipline* had no surviving owner on the Claude/Codex surfaces, so it is
migrated here rather than dropped — `docs/operational_rules.md` Rule 16 R5: an
obligation is resolved, migrated or explicitly retired, never silently lost.

Two classes are surfaced so the operator confirms before they run:

  * **Git hook / signing bypass** — ``--no-verify`` / ``--no-gpg-sign``. Not the
    standing path (CLAUDE.md §Vendor-data integrity gate: "`git commit
    --no-verify` is not the standing path"). A git hook cannot guard this by
    construction — ``--no-verify`` is precisely what skips git hooks — so an
    agent-facing check is the only place the rule can be enforced at all.
  * **Destructive git / fs** — ``reset --hard``, ``clean -f``, ``checkout --``,
    force-push, ``branch -D``, ``rm -rf``. The standing safety rule wants a
    ``git status`` plus stash/commit first.

This is a **warn-class** gate: it returns ``ask``, never ``deny``. It keeps the
operator in control and never blocks outright, matching the "unless Joshua
explicitly asked" carve-out of the original.

**One intentional divergence from the Cursor original:** ``--force-with-lease``
no longer matches. The original's ``.*--force`` swept it up while the same
hook's message recommended it as the safe alternative — a warn-class gate that
fires on its own recommended path teaches the operator to click through. Plain
``--force`` and ``-f`` still ask.

**Wiring.** Registered as a `PreToolUse` Bash hook in
`.claude/settings.json` at the operator's 2026-09-15 instruction to execute the
retirement decisions. The entry is:

    {"matcher": "Bash",
     "hooks": [{"type": "command",
                "command": "python \\"$CLAUDE_PROJECT_DIR/scripts/guard_shell_command.py\\""}]}

Output contract: Claude Code's PreToolUse shape
(`hookSpecificOutput.permissionDecision`), NOT Cursor's `permission` key — see
`_emit`. Stdin carries the command at `tool_input.command`.

Contract (unchanged from the original): read a JSON payload on stdin, write a
decision JSON on stdout. Fail-open — any parse error yields ``allow``, so an
unrelated or malformed command is never blocked. `classify()` is the pure
function; it is what the tests pin, independent of any harness wiring.
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
    # `--force-with-lease` is deliberately excluded: it is the alternative this
    # guard's own message recommends. Asking on it trained the operator to click
    # through the prompt, which is how a warn-class gate stops working. This is
    # the one intentional divergence from `.cursor/hooks/before_shell.py`, whose
    # `.*--force` also matched `--force-with-lease`; found by
    # tests/scripts/test_guard_shell_command.py during the 2026-09-15 port.
    r"|git\s+push\b.*--force(?!-with-lease)"
    r"|git\s+push\b.*\s-f(\s|$)"
    r"|git\s+branch\s+-D"
    r"|rm\s+-rf"
)

NO_VERIFY_AGENT_MSG = (
    "`--no-verify` / `--no-gpg-sign` skips the repo's pre-commit gate stack "
    "(see `scripts/githooks/pre-commit` for the current set — deliberately not "
    "enumerated here, it changes). Not the standing path — fix the hook failure "
    "and re-commit unless Joshua explicitly asked to bypass."
)
DESTRUCTIVE_AGENT_MSG = (
    "Destructive command — `git status` first and stash (`-u`) or commit "
    "anything present. Never force-push main; prefer --force-with-lease / "
    "git restore / a revert commit."
)


def command_of(data: dict) -> str:
    """Extract the shell command from any of the payload shapes we accept.

    Kept tolerant on purpose: this ran against Cursor's ``beforeShellExecution``
    payload and now also has to accept Claude Code's ``PreToolUse`` shape
    (``tool_input.command``). An unrecognised shape yields "" → allow.
    """
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


def classify(cmd: str) -> tuple[str, str, str]:
    """Return (permission, agent_message, user_message) for one command."""
    if not cmd:
        return "allow", "", ""
    if NO_VERIFY.search(cmd):
        return (
            "ask",
            NO_VERIFY_AGENT_MSG,
            "Command bypasses git hooks/signing. Confirm to proceed.",
        )
    if DESTRUCTIVE.search(cmd):
        return (
            "ask",
            DESTRUCTIVE_AGENT_MSG,
            "Potentially destructive git/fs command. Confirm to proceed.",
        )
    return "allow", "", ""


def _emit(permission: str, agent_msg: str = "", user_msg: str = "") -> None:
    """Write Claude Code's PreToolUse decision contract.

    NOT Cursor's `{"permission", "agentMessage", "userMessage"}` shape — that was
    carried over verbatim in the first draft of this port and would have been
    ignored by Claude Code, making the documented wiring a silent no-op. Caught by
    adversarial review of the retirement PR before the hook was ever wired.

    Claude Code reads `hookSpecificOutput.permissionDecision` (allow|deny|ask),
    with `permissionDecisionReason` shown to the user and `additionalContext`
    passed to the model. Exit 0 means "parse this JSON".
    """
    block: dict = {
        "hookEventName": "PreToolUse",
        "permissionDecision": permission,
    }
    if user_msg:
        block["permissionDecisionReason"] = user_msg
    if agent_msg:
        block["additionalContext"] = agent_msg
    sys.stdout.write(json.dumps({"hookSpecificOutput": block}))


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        _emit("allow")
        return 0
    _emit(*classify(command_of(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
