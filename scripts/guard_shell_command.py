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
    standing path (AGENTS.md §Vendor-data integrity gate: "`git commit
    --no-verify` is not the standing path"). A git hook cannot guard this by
    construction — ``--no-verify`` is precisely what skips git hooks — so an
    agent-facing check is the only place the rule can be enforced at all.
  * **Destructive git / fs** — ``reset --hard``, ``clean -f``, ``checkout --``,
    ``restore``, ``switch --discard-changes``, force-push, ``branch -D``,
    ``rm -rf``. The standing safety rule wants a ``git status`` plus
    stash/commit first.

**Commands, not text (2026-09-23, card
`docs/briefs/handoffs/2026-09-23-harness-guards-hardening.md` E1–E3).** The
guard used to `re.search` the raw command string, so it asked on destructive
text that was only data (a heredoc probe file, a grep pattern, a commit
message) — and a background agent has nobody to answer that prompt, so its
tool call never returned (F29) — while real spellings git accepts went
through (A1–A7). `classify()` now tokenizes with the tokenizer
`scripts/guard_s2_runs.py` uses (`scripts/_shell_tokens.py`, strict mode) and
judges only words in **command position**: each segment after ``sudo``,
``env``, ``command``, ``exec``, ``nohup``, ``time``, ``timeout`` (and the other
runners the tokenizer unwraps) are stripped, the script of ``bash -c``/``sh -c``
re-parsed, and the body of every ``$(…)`` substitution re-parsed. **Data is
never a command:** heredoc bodies (also inside a substitution), quoted
arguments of other programs (``grep``, ``rg``, ``echo``, ``printf``,
``git log --grep``, ``git commit -m``) and ``python -c`` strings. A command the
tokenizer cannot read (an unterminated quote or substitution) falls back to the
raw-string regexes below, so unparsable destructive text still asks.

What asks (git global options such as ``-C``, ``-c``, ``--no-pager``,
``--git-dir=``, ``--work-tree=`` are skipped to find the subcommand; option
clusters are read the way git reads them, so a letter inside an option's value
— ``-mn`` is the message "n" — is not a flag):

  * bypass, for ``commit``/``merge``/``push``/``am``/``rebase``/``cherry-pick``/
    ``revert``: a long option that is a prefix of ``--no-verify`` or
    ``--no-gpg-sign`` at least 6 characters long; ``-n`` in a ``commit`` short
    cluster (``-n`` is ``--dry-run`` for push and ``--no-stat`` for merge); a
    ``-c``/``--config-env`` global option setting ``core.hooksPath`` (any case);
  * destructive: ``reset`` with a prefix of ``--hard`` of at least 4 characters;
    ``clean -f``/``--force`` (``-n`` alone is a dry run); ``checkout`` with
    ``--`` or ``-f``/``--force``; ``restore`` unless it only touches the index
    (``--staged``/``-S`` without ``--worktree``/``-W``); ``switch -f``/
    ``--force``/``--discard-changes``; ``push -f``/``--force`` or a ``+refspec``;
    ``branch -D`` or delete plus force across arguments; ``rm`` (any path to
    the binary) with recursive plus force across arguments. Other long options
    match their unambiguous abbreviations too (git 2.43 accepts ``clean --f``,
    ``checkout --forc``, ``restore --w``, ``switch --disc``).

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
decision JSON on stdout. Fail-open — an unrelated or malformed command is
never blocked (2026-09-23: benign input now emits *nothing* rather than
``allow``, because a hook ``allow`` silently overrides the operator's
permission settings). `classify()` is the pure function; it is what the tests
pin, independent of any harness wiring.
"""
from __future__ import annotations

import json
import re
import sys

try:  # imported as `scripts.guard_shell_command` (tests, repo root on sys.path)
    from scripts._shell_tokens import ShellSyntaxError, expand, program, segments
except ImportError:  # run as `python scripts/guard_shell_command.py`: scripts/ is sys.path[0]
    from _shell_tokens import ShellSyntaxError, expand, program, segments

# The raw-string reading: used only when the tokenizer cannot read the command.
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
NO_VERIFY_USER_MSG = "Command bypasses git hooks/signing. Confirm to proceed."
DESTRUCTIVE_USER_MSG = "Potentially destructive git/fs command. Confirm to proceed."

# git subcommands that run hooks or sign (E2), and the long options that skip them
HOOKED = frozenset({"commit", "merge", "push", "am", "rebase", "cherry-pick", "revert"})
BYPASS_OPTIONS = ("--no-verify", "--no-gpg-sign")
# git global options that take the next word as their value
GIT_GLOBAL_VALUES = frozenset({"-C", "-c", "--git-dir", "--work-tree", "--namespace",
                               "--config-env", "--super-prefix", "--attr-source"})
# Short options whose value is the rest of the cluster or, when the letter ends
# the cluster, the next word (git's parse-options; per subcommand).
SHORT_VALUES = {
    "commit": "mFCct", "merge": "mFsX", "push": "o", "clean": "e", "checkout": "bB",
    "switch": "cC", "restore": "s", "branch": "u", "rebase": "sXx",
    "cherry-pick": "mX", "revert": "mX",
}
# Short options whose optional value can only be joined: the rest of the cluster.
JOINED_VALUES = {
    "commit": "uS", "merge": "S", "rebase": "S", "cherry-pick": "S", "revert": "S",
    "am": "SCp",
}
# Long options whose value may be the next word (only where an operand matters).
LONG_VALUES = {"push": frozenset({"--repo", "--receive-pack", "--exec", "--push-option"})}

_SHORT, _LONG, _END, _OPERAND = "short", "long", "end", "operand"


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


# --- reading options the way git and rm do ------------------------------------

def _options(args: list[str], sub: str = "") -> list[tuple[str, str]]:
    """(kind, word) for each flag, long option, `--` marker and operand in `args`.

    Short clusters yield one entry per letter and stop at a letter that takes a
    value (``-anm wip`` is -a -n -m; ``-mn`` is -m with the value "n"); options
    may follow operands; everything after ``--`` is an operand.
    """
    values, joined = SHORT_VALUES.get(sub, ""), JOINED_VALUES.get(sub, "")
    long_values = LONG_VALUES.get(sub, frozenset())
    out: list[tuple[str, str]] = []
    i, ended = 0, False
    while i < len(args):
        arg = args[i]
        i += 1
        if ended or arg == "-" or not arg.startswith("-"):
            out.append((_OPERAND, arg))
        elif arg == "--":
            ended = True
            out.append((_END, arg))
        elif arg.startswith("--"):
            out.append((_LONG, arg))
            if arg in long_values:
                i += 1
        else:
            for pos, letter in enumerate(arg[1:], 1):
                out.append((_SHORT, letter))
                if letter in joined:
                    break
                if letter in values:
                    i += 1 if pos == len(arg) - 1 else 0
                    break
    return out


def _abbrev(word: str, name: str, shortest: int = 3) -> bool:
    """Whether `word` spells the long option `name` (exactly, or a prefix of it)."""
    return word == name or (len(word) >= shortest and name.startswith(word))


def _has(opts: list[tuple[str, str]], letters: str = "", longs: tuple[str, ...] = ()) -> bool:
    """Whether a short flag in `letters` or a spelling of a long option in `longs` is set."""
    return any((kind == _SHORT and word in letters)
               or (kind == _LONG and any(_abbrev(word, name) for name in longs))
               for kind, word in opts)


def _git_parts(words: list[str]) -> tuple[list[str], str | None, list[str]]:
    """(config settings from global options, subcommand, its args) for a git command."""
    configs: list[str] = []
    i = 1
    while i < len(words) and words[i].startswith("-"):
        word = words[i]
        if word in GIT_GLOBAL_VALUES and i + 1 < len(words):
            if word in ("-c", "--config-env"):
                configs.append(words[i + 1])
            i += 2
            continue
        if word.startswith("--config-env="):
            configs.append(word.split("=", 1)[1])
        i += 1
    if i >= len(words):
        return configs, None, []
    return configs, words[i], words[i + 1:]


# --- the two classes -----------------------------------------------------------

def _bypasses(words: list[str]) -> bool:
    """Whether this command runs git with its hooks or signing skipped (E2)."""
    if program(words[0], strict=True) != "git":
        return False
    configs, sub, args = _git_parts(words)
    if sub not in HOOKED:
        return False
    if any(c.split("=", 1)[0].strip().casefold() == "core.hookspath" for c in configs):
        return True
    for kind, word in _options(args, sub):
        if kind == _LONG and any(_abbrev(word, name, 6) for name in BYPASS_OPTIONS):
            return True
        if kind == _SHORT and word == "n" and sub == "commit":
            return True
    return False


def _restore_discards(opts: list[tuple[str, str]]) -> bool:
    """`git restore` touches the work tree unless it only restores the index."""
    staged = worktree = False
    for kind, word in opts:
        if kind == _SHORT:
            staged |= word == "S"
            worktree |= word == "W"
        elif kind == _LONG:
            if word == "--no-staged":
                staged = False
            elif word == "--no-worktree":
                worktree = False
            elif _abbrev(word, "--staged"):
                staged = True
            elif _abbrev(word, "--worktree"):
                worktree = True
    return not staged or worktree


def _git_destroys(sub: str, opts: list[tuple[str, str]]) -> bool:
    """Whether `git <sub>` with these options discards work (E3)."""
    if sub == "reset":
        return any(kind == _LONG and _abbrev(word, "--hard", 4) for kind, word in opts)
    if sub == "clean":
        return _has(opts, "f", ("--force",))
    if sub == "checkout":
        return any(kind == _END for kind, _ in opts) or _has(opts, "f", ("--force",))
    if sub == "restore":
        return _restore_discards(opts)
    if sub == "switch":
        return _has(opts, "f", ("--force", "--discard-changes"))
    if sub == "push":
        return _has(opts, "f", ("--force",)) \
            or any(kind == _OPERAND and word.startswith("+") for kind, word in opts)
    if sub == "branch":
        return _has(opts, "D") or (_has(opts, "d", ("--delete",))
                                   and _has(opts, "f", ("--force",)))
    return False


def _destroys(words: list[str]) -> bool:
    """Whether this command is a destructive git or rm operation (E3)."""
    name = program(words[0], strict=True)
    if name == "rm":
        opts = _options(words[1:])
        return _has(opts, "rR", ("--recursive",)) and _has(opts, "f", ("--force",))
    if name != "git":
        return False
    _, sub, args = _git_parts(words)
    return sub is not None and _git_destroys(sub, _options(args, sub))


def _commands(cmd: str) -> list[list[str]]:
    """Every command the shell would run for `cmd`, wrappers stripped (strict read)."""
    found: list[list[str]] = []
    for segment in segments(cmd, strict=True):
        found.extend(words for words in expand(segment, strict=True) if words)
    return found


def _classify_text(cmd: str) -> tuple[str, str, str]:
    """The raw-string reading, for commands the tokenizer cannot read (E1)."""
    if NO_VERIFY.search(cmd):
        return "ask", NO_VERIFY_AGENT_MSG, NO_VERIFY_USER_MSG
    if DESTRUCTIVE.search(cmd):
        return "ask", DESTRUCTIVE_AGENT_MSG, DESTRUCTIVE_USER_MSG
    return "allow", "", ""


def classify(cmd: str) -> tuple[str, str, str]:
    """Return (permission, agent_message, user_message) for one command."""
    if not cmd:
        return "allow", "", ""
    try:
        commands = _commands(cmd)
    except (ShellSyntaxError, IndexError, RecursionError):
        return _classify_text(cmd)
    if any(_bypasses(words) for words in commands):
        return "ask", NO_VERIFY_AGENT_MSG, NO_VERIFY_USER_MSG
    if any(_destroys(words) for words in commands):
        return "ask", DESTRUCTIVE_AGENT_MSG, DESTRUCTIVE_USER_MSG
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
    """Emit a decision only when the command must be confirmed or blocked.

    A hook ``allow`` bypasses the operator's permission rules outright, so
    benign or unparsable input produces no output at all and defers to the
    normal permission flow; ``classify()`` still returns ``allow`` internally.
    """
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    permission, agent_msg, user_msg = classify(command_of(data))
    if permission != "allow":
        _emit(permission, agent_msg, user_msg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
