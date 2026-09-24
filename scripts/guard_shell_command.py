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
through (A1–A7). `classify()` now tokenizes with `scripts/_shell_tokens.py` in
strict mode (`scripts/guard_s2_runs.py` uses its default mode, a separate
scanner) and judges only words in **command position**: each segment after ``sudo``,
``env``, ``command``, ``exec``, ``nohup``, ``time``, ``timeout`` (and the other
runners the tokenizer unwraps) are stripped, the script of ``bash -c``/``sh -c``
re-parsed, and the body of every ``$(…)``, backquote and ``<(…)``/``>(…)``
substitution re-parsed — also inside a redirection target or a ``<<<`` word
(``echo x > "$(cmd)"`` runs ``cmd``).

**Fail toward asking (operator ruling 2026-09-23, card 2 round 3).** The
command-position reading alone missed text bash runs without a readable
``-c`` script (``bash <<EOF``, ``… | sh``, ``source <(…)``, a ``$(…)`` in an
unquoted heredoc, runners such as ``stdbuf``/``coproc``, git's own
``submodule foreach``/``rebase -x``/``bisect run``). So after it, main's
raw-string regexes below still run over the command with only **proven data**
blanked: a comment; a heredoc body whose delimiter is quoted, or unquoted with
no ``$(``, backquote or ``<(``; a literal redirection target or here-string
word; a quoted argument of ``echo``/``printf``/``grep``/``rg``; a git
commit/merge/tag message or log ``--grep`` pattern; a ``python -c`` string. A
``$(…)`` inside such data is code and stays visible. Nothing is blanked when
the command runs text the guard cannot read (a shell with no ``-c`` script,
``source``/``.``/``eval``, a command word built from ``$…``), and a command
the tokenizer cannot read at all (an unterminated quote or substitution, a
``case`` inside ``$(…)``) gets the raw regexes whole. The guard therefore asks
wherever main's guard asked, except on that data (F29).

What asks (git global options such as ``-C``, ``-c``, ``--no-pager``,
``--git-dir=``, ``--work-tree=`` are skipped to find the subcommand; option
clusters are read the way git reads them, so a letter inside an option's value
— ``-mn`` is the message "n" — is not a flag, and neither is the word after a
long option that takes one — ``--message '-n …'`` is a message):

  * bypass, for ``commit``/``merge``/``pull``/``push``/``am``/``rebase``/
    ``cherry-pick``/``revert``: a long option that is a prefix of
    ``--no-verify`` or ``--no-gpg-sign`` at least 6 characters long; ``-n`` in
    a ``commit`` or ``am`` short cluster (``-n`` is ``--no-verify`` for ``am``
    in git 2.43; it is ``--dry-run`` for push and ``--no-stat`` for merge and
    pull); config that disables signing or redirects hooks —
    ``core.hooksPath`` at any value, and ``commit.gpgSign``/``tag.gpgSign``
    set false, matched case-insensitively — whether it comes from a
    ``-c``/``--config-env`` global option or from the segment's leading
    ``GIT_CONFIG_COUNT``/``GIT_CONFIG_KEY_<n>``/``GIT_CONFIG_VALUE_<n>`` or
    ``GIT_CONFIG_PARAMETERS`` environment assignments (a ``--config-env``
    ``NAME:VAR`` names the key but reads the value from the environment, so
    naming one of these keys asks). ``pull`` is beyond E2's list: it
    merges, so ``git pull --no-verify`` skips the pre-merge-commit hook;
  * an alias judged as what it runs: ``git -c alias.<name>=<value> <name> …``
    reads the value as the subcommand plus its arguments; a value starting
    with ``!`` is a shell command, re-parsed with the strict reader. A dashed
    ``git-<sub>`` program, with or without a path, is judged as ``git <sub>``;
  * destructive: ``reset`` with a prefix of ``--hard`` (``--h`` already resets
    hard in git 2.43; the card's E3 said at least 4 characters) or of
    ``--merge`` (``--me``; ``--keep`` keeps the work tree and never asks);
    ``clean -f``/``--force`` or ``-i``/``--interactive``, and any non-dry-run
    ``clean`` once ``clean.requireForce`` is set false (``-n`` alone is a dry
    run); ``checkout`` with ``--`` or ``-f``/``--force``; ``restore`` unless
    it only touches the index (``--staged``/``-S`` without
    ``--worktree``/``-W``); ``switch -f``/``--force``/``--discard-changes``;
    ``push -f``/``--force``, ``--mirror`` or a ``+refspec`` — including a
    ``+`` on the ``remote.<name>.push`` refspec configured for the remote
    being pushed to; ``branch -D`` or delete plus force across arguments;
    ``rm`` (any path to the binary) with recursive plus force across
    arguments. Other long options match their unambiguous abbreviations too
    (git 2.43 accepts ``clean --f``, ``checkout --forc``, ``restore --w``,
    ``switch --disc``).

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
    from scripts._shell_tokens import (SHELLS, ShellSyntaxError, Word, expand, is_assignment,
                                       program, segments)
except ImportError:  # run as `python scripts/guard_shell_command.py`: scripts/ is sys.path[0]
    from _shell_tokens import (SHELLS, ShellSyntaxError, Word, expand, is_assignment,
                               program, segments)

# The raw-string reading: main's guard before card 2. It asks on any match left
# after proven data is blanked (`_residual`), and on the whole command when the
# tokenizer cannot read it or the command runs text the guard cannot read.
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

# git subcommands that run hooks or sign (E2), and the long options that skip them.
# `pull` is here because it merges: `git pull --no-verify` skips the
# pre-merge-commit and commit-msg hooks (`git pull -h`, git 2.43), and this repo
# installs scripts/githooks/pre-merge-commit.
HOOKED = frozenset({"commit", "merge", "pull", "push", "am", "rebase", "cherry-pick",
                    "revert"})
BYPASS_OPTIONS = ("--no-verify", "--no-gpg-sign")
# git config keys that disable signing or redirect hooks when set on a HOOKED
# subcommand (card 4): `core.hooksPath` at any value, and commit.gpgSign /
# tag.gpgSign set false. Keys match case-insensitively; the settings reach git
# through `-c`/`--config-env` or leading GIT_CONFIG_* environment assignments.
HOOK_PATH_KEY = "core.hookspath"
SIGN_OFF_KEYS = frozenset({"commit.gpgsign", "tag.gpgsign"})
# the values git's config parser reads as a false boolean
GIT_FALSE = frozenset({"", "false", "no", "off", "0"})
# git resolves an alias chain at most this deep here (item 5)
ALIAS_LIMIT = 5
# git global options that take the next word as their value
GIT_GLOBAL_VALUES = frozenset({"-C", "-c", "--git-dir", "--work-tree", "--namespace",
                               "--config-env", "--super-prefix", "--attr-source",
                               "--shallow-file"})
# Programs whose quoted arguments are only printed or matched (E1's examples).
DATA_PROGRAMS = frozenset({"echo", "printf", "grep", "egrep", "fgrep", "rg"})
# git subcommands whose -m/--message value is a message, and those whose --grep
# value is a pattern.
MESSAGE_SUBS = frozenset({"commit", "merge", "tag"})
GREP_SUBS = frozenset({"log", "shortlog", "rev-list"})
# Short options whose value is the rest of the cluster or, when the letter ends
# the cluster, the next word (git's parse-options; per subcommand).
SHORT_VALUES = {
    "commit": "mFCct", "merge": "mFsX", "pull": "sXo", "push": "o", "clean": "e",
    "checkout": "bB", "switch": "cC", "restore": "s", "branch": "u", "rebase": "sXx",
    "cherry-pick": "mX", "revert": "mX",
}
# Short options whose optional value can only be joined: the rest of the cluster.
JOINED_VALUES = {
    "commit": "uS", "merge": "S", "pull": "rjS", "rebase": "S", "cherry-pick": "S",
    "revert": "S", "am": "SCp",
}
# Long options whose value may be the next word, so that word is data, never a
# flag or an operand (`commit --message '-n …'`; per `git <sub> -h`, git 2.43).
_PICK_VALUES = frozenset({"--cleanup", "--mainline", "--strategy", "--strategy-option"})
LONG_VALUES = {
    "push": frozenset({"--repo", "--receive-pack", "--exec", "--push-option"}),
    "commit": frozenset({"--message", "--file", "--author", "--date", "--template",
                         "--reuse-message", "--reedit-message", "--squash", "--fixup",
                         "--trailer", "--cleanup", "--pathspec-from-file"}),
    "merge": frozenset({"--message", "--file", "--strategy", "--strategy-option",
                        "--cleanup", "--into-name"}),
    "pull": frozenset({"--strategy", "--strategy-option", "--cleanup", "--upload-pack",
                       "--depth", "--deepen", "--shallow-since", "--shallow-exclude",
                       "--refmap", "--server-option", "--negotiation-tip"}),
    "rebase": frozenset({"--onto", "--whitespace", "--exec", "--strategy",
                         "--strategy-option"}),
    "cherry-pick": _PICK_VALUES,
    "revert": _PICK_VALUES,
    "am": frozenset({"--quoted-cr", "--whitespace", "--directory", "--exclude",
                     "--include", "--patch-format"}),
}

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
            # git reads a unique prefix of a long option as the option itself
            if arg in long_values or len([n for n in long_values if _abbrev(arg, n)]) == 1:
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

def _config_bypasses(configs: list[str]) -> bool:
    """Whether a git config setting disables signing or redirects hooks (item 4).

    `core.hooksPath` set to anything redirects the hooks; `commit.gpgSign` /
    `tag.gpgSign` set to a value git reads as false skip signing. Keys match
    case-insensitively. `--config-env NAME:VAR` names the key but reads the
    value from `VAR`, which this guard cannot see, so naming one of these keys
    asks (fail toward asking).
    """
    for config in configs:
        name, has_value, value = config.partition("=")
        name = name.strip()
        from_env = ":" in name  # `--config-env NAME:VAR` collected with its VAR
        key = (name.partition(":")[0] if from_env else name).casefold()
        if key == HOOK_PATH_KEY:
            return True
        if key in SIGN_OFF_KEYS and (from_env
                                     or (has_value and value.strip().casefold() in GIT_FALSE)):
            return True
    return False


def _bypasses(words: list[str], configs: tuple[str, ...] = ()) -> bool:
    """Whether this command runs git with its hooks or signing skipped (E2).

    `configs` adds settings gathered outside the command's own words — the
    leading `GIT_CONFIG_*` environment assignments of its segment (item 4).
    """
    if program(words[0], strict=True) != "git":
        return False
    found, sub, args = _git_parts(words)
    if sub not in HOOKED:
        return False
    if _config_bypasses([*found, *configs]):
        return True
    for kind, word in _options(args, sub):
        if kind == _LONG and any(_abbrev(word, name, 6) for name in BYPASS_OPTIONS):
            return True
        # `-n` is --no-verify for commit and for am (git 2.43); for push it is
        # --dry-run and for merge/pull --no-stat
        if kind == _SHORT and word == "n" and sub in ("commit", "am"):
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


def _config_is_false(configs: tuple[str, ...] | list[str], key: str) -> bool:
    """Whether `key` is set to a value git reads as false among `configs`."""
    for config in configs:
        name, has_value, value = config.partition("=")
        if has_value and name.strip().casefold() == key \
                and value.strip().casefold() in GIT_FALSE:
            return True
    return False


def _config_push_forces(configs: tuple[str, ...] | list[str],
                        operands: list[str]) -> bool:
    """Whether a `remote.<name>.push` refspec forces this push (item 6).

    git uses `remote.<name>.push` when pushing to `name`, and a leading `+` on
    its refspec is a force push. With no remote operand the push goes to the
    current branch's remote, which the guard cannot read, so a configured `+`
    asks there too (fail toward asking).
    """
    for config in configs:
        name, has_value, value = config.partition("=")
        parts = name.strip().casefold().split(".")
        if not has_value or len(parts) != 3 or parts[0] != "remote" or parts[2] != "push":
            continue
        if parts[1] and value.startswith("+") and (
                not operands or parts[1] in (word.casefold() for word in operands)):
            return True
    return False


def _git_destroys(sub: str, opts: list[tuple[str, str]],
                  configs: tuple[str, ...] = ()) -> bool:
    """Whether `git <sub>` with these options discards work (E3, item 6)."""
    if sub == "reset":
        # `--h` is already a hard reset in git 2.43: no other reset option starts
        # with h; `--me` reaches --merge the same way (--m stays ambiguous with
        # --mixed); --keep keeps the work tree, so it never asks
        return any(kind == _LONG and (_abbrev(word, "--hard", 3) or _abbrev(word, "--merge", 4))
                   for kind, word in opts)
    if sub == "clean":
        # without requireForce=false git refuses to clean unforced; with it set
        # false every non-dry-run clean discards, so `-d` or paths are not needed
        if _has(opts, "f", ("--force",)) or _has(opts, "i", ("--interactive",)):
            return True
        return not _has(opts, "n", ("--dry-run",)) \
            and _config_is_false(configs, "clean.requireforce")
    if sub == "checkout":
        return any(kind == _END for kind, _ in opts) or _has(opts, "f", ("--force",))
    if sub == "restore":
        return _restore_discards(opts)
    if sub == "switch":
        return _has(opts, "f", ("--force", "--discard-changes"))
    if sub == "push":
        operands = [word for kind, word in opts if kind == _OPERAND]
        return _has(opts, "f", ("--force",)) \
            or any(kind == _LONG and _abbrev(word, "--mirror") for kind, word in opts) \
            or any(word.startswith("+") for word in operands) \
            or _config_push_forces(configs, operands)
    if sub == "branch":
        return _has(opts, "D") or (_has(opts, "d", ("--delete",))
                                   and _has(opts, "f", ("--force",)))
    return False


def _destroys(words: list[str], configs: tuple[str, ...] = ()) -> bool:
    """Whether this command is a destructive git or rm operation (E3)."""
    name = program(words[0], strict=True)
    if name == "rm":
        opts = _options(words[1:])
        return _has(opts, "rR", ("--recursive",)) and _has(opts, "f", ("--force",))
    if name != "git":
        return False
    found, sub, args = _git_parts(words)
    return sub is not None and _git_destroys(sub, _options(args, sub), (*found, *configs))


def _alias_target(configs: list[str], sub: str) -> tuple[bool, str] | None:
    """(is a shell command, its text) for the `alias.<sub>` setting among
    `configs`, or None when none defines it.

    A value starting with `!` is a shell command git runs through the shell;
    any other value is the subcommand plus its arguments.
    """
    wanted = f"alias.{sub}".casefold()
    for config in configs:
        name, has_value, value = config.partition("=")
        if not has_value or name.strip().casefold() != wanted:
            continue
        value = value.strip()
        if value.startswith("!"):
            return True, value[1:]
        if value:
            return False, value
    return None


def _judged(words: list[str], depth: int = 0) -> list[list[str]]:
    """The command words to judge: a dashed `git-<sub>` program, with or without
    a path, is `git <sub>` (item 7), and `git -c alias.<name>=… <name> …` is
    judged as what the alias runs (item 5).

    A `!` alias value is re-parsed with strict `segments`/`expand`; any other
    value takes the alias name's place as the subcommand and its arguments
    (the alias's own `-c` definition stays in front of it, as the command's
    other global options do). Unreadable input raises, and `classify` then
    falls back to the raw-string reading whole — fail toward asking.
    """
    name = program(words[0], strict=True)
    if name.startswith("git-") and len(name) > 4:
        return _judged(["git", name[4:], *words[1:]], depth)
    if name != "git" or depth >= ALIAS_LIMIT:
        return [words]
    found, sub, args = _git_parts(words)
    if sub is None:
        return [words]
    alias = _alias_target(found, sub)
    if alias is None:
        return [words]
    is_shell, value = alias
    if not is_shell:
        lines = segments(value, strict=True)
        if not lines:
            return [words]
        # words[:i] keeps the global options (and the alias definition); args
        # are contiguous after words[i], so i = len(words) - len(args) - 1
        head = words[:len(words) - len(args) - 1]
        out = _judged([*head, *lines[0], *args], depth + 1)
        for extra in lines[1:]:
            out.extend(_judged(extra, depth + 1))
        return out
    out: list[list[str]] = []
    for segment in segments(value, strict=True):
        for inner in expand(segment, strict=True):
            if inner:
                out.extend(_judged(inner, depth + 1))
    return out


def _env_configs(assignments: list[str]) -> list[str]:
    """The git config settings one segment's leading `GIT_CONFIG_*` assignments
    name: `GIT_CONFIG_COUNT` with `GIT_CONFIG_KEY_<n>`/`GIT_CONFIG_VALUE_<n>`
    pairs, and `GIT_CONFIG_PARAMETERS` (git quotes each `key=value` entry)."""
    env = {}
    for word in assignments:
        env_name, _, value = word.partition("=")
        env[env_name] = value
    configs = []
    count = env.get("GIT_CONFIG_COUNT", "")
    if count.isdigit():
        for i in range(int(count)):
            key = env.get(f"GIT_CONFIG_KEY_{i}")
            if key is not None:
                configs.append(f"{key}={env.get(f'GIT_CONFIG_VALUE_{i}', '')}")
    parameters = env.get("GIT_CONFIG_PARAMETERS", "")
    if parameters:
        configs += [quoted or bare for quoted, bare
                    in re.findall(r"'([^']*)'|([^'\s]+)", parameters)]
    return configs


def _env_git_configs(cmd: str) -> list[tuple[list[str], list[list[str]]]]:
    """(config settings, the commands they prefix) for each segment whose
    leading `GIT_CONFIG_*` assignments name git config settings.

    Those assignments reach the git command of their segment as `-c` settings
    do (item 4), so the commands are judged with them.
    """
    pairs = []
    for segment in segments(cmd, strict=True):
        i = 0
        while i < len(segment) and is_assignment(segment[i]):
            i += 1
        if i == 0:
            continue
        configs = _env_configs(segment[:i])
        if not configs:
            continue
        commands = [judged for words in expand(segment[i:], strict=True) if words
                    for judged in _judged(words)]
        if commands:
            pairs.append((configs, commands))
    return pairs


def _commands(cmd: str, bodies: list | None = None) -> list[list[str]]:
    """Every command the shell would run for `cmd`, wrappers stripped and git
    aliases and dashed `git-<sub>` programs resolved (strict read).

    With `bodies`, words carry their source spans and heredoc bodies are collected.
    """
    found: list[list[str]] = []
    for segment in segments(cmd, strict=True, bodies=bodies):
        for words in expand(segment, strict=True):
            if words:
                found.extend(_judged(words))
    return found


# --- fail toward asking (operator ruling 2026-09-23) --------------------------

def _runs_unread_text(words: list[str]) -> bool:
    """Whether this command runs text the guard cannot read as commands.

    A shell with no `-c` script (it reads stdin — a heredoc, a here-string, a
    pipe — or a file or `<(…)`), `source`/`.`/`eval` (whose strict re-parse
    leaves a substituted word), and a command word built from `$…` or a
    backquote. `expand` has already replaced `bash -c '…'` by its script's
    commands, so a shell still standing here has no readable script.
    """
    first = words[0]
    if "$" in first or "`" in first:
        return True
    return program(first, strict=True) in SHELLS | {"source", ".", "eval"}


def _git_data(words: list[str], index: int) -> bool:
    """Whether words[index] is a git commit/merge/tag message or a log --grep pattern."""
    _, sub, args = _git_parts(words)
    first = len(words) - len(args)
    if sub is None or index < first:
        return False
    word, prev = words[index], words[index - 1] if index > first else ""
    if sub in MESSAGE_SUBS:
        return (word.startswith("--") and _abbrev(word.split("=", 1)[0], "--message")
                and "=" in word) \
            or (bool(re.fullmatch(r"-[A-Za-z]*m", prev)) or _abbrev(prev, "--message")) \
            or bool(re.match(r"-[A-Za-z]*m.", word))
    if sub in GREP_SUBS:
        return word.startswith("--grep=") or prev == "--grep"
    return False


_RUNS = re.compile(r"\$\(|`|[<>]\(")  # text bash would run inside an expanding word


def _dropped_is_data(literal: bool, text: str, kind: str) -> bool:
    """Whether text the tokenizer dropped (see `segments`' `bodies`) is only data.

    A comment; a heredoc body whose delimiter was quoted, or with no `$(`,
    backquote or `<(`; a redirection target or here-string word with none of
    those outside single quotes (a quote inside an unquoted heredoc body is
    only a character, so that stripping applies to words alone).
    """
    if kind == "substitution":
        return False
    if literal:
        return True
    if kind == "target":
        text = re.sub(r"'[^']*'", "", text)
    return not _RUNS.search(text)


def _data_spans(commands: list[list[str]], bodies: list) -> list[tuple[int, int]]:
    """Source spans that are only data: E1's data, and nothing that bash executes.

    Dropped text that `_dropped_is_data` accepts; a quoted argument of an
    echo/printf/grep/rg; a git commit/merge/tag message or log --grep pattern;
    a `python -c` string.
    """
    spans = [(start, end) for start, end, literal, text, kind in bodies
             if _dropped_is_data(literal, text, kind)]
    for words in commands:
        name = program(words[0], strict=True)
        spans += [(word.start, word.end) for index, word in enumerate(words[1:], 1)
                  if isinstance(word, Word) and _is_data_word(name, words, index)]
    return spans


def _is_data_word(name: str, words: list[str], index: int) -> bool:
    """Whether words[index] of a `name` command is only printed, matched or run as Python."""
    if name in DATA_PROGRAMS:
        return words[index].quoted
    if name == "git":
        return _git_data(words, index)
    return name.startswith("python") and bool(re.fullmatch(r"-[A-Za-z]*c", words[index - 1]))


def _residual(cmd: str, data: list[tuple[int, int]], bodies: list) -> str:
    """`cmd` with its data blanked (same length, so nothing else moves).

    A substitution inside a data word is code: it is restored, and only the
    data inside it (a quoted heredoc, a printf argument) is blanked again. The
    spans nest, so applying them outermost first gets every level right.
    """
    marks = [(start, end, True) for start, end in data]
    marks += [(start, end, False) for start, end, _, _, kind in bodies if kind == "substitution"]
    chars = list(cmd)
    for start, end, blank in sorted(marks, key=lambda mark: mark[0] - mark[1]):
        chars[start:end] = " " * (end - start) if blank else cmd[start:end]
    return "".join(chars)


def _classify_text(cmd: str) -> tuple[str, str, str]:
    """The raw-string reading, for commands the tokenizer cannot read (E1)."""
    if NO_VERIFY.search(cmd):
        return "ask", NO_VERIFY_AGENT_MSG, NO_VERIFY_USER_MSG
    if DESTRUCTIVE.search(cmd):
        return "ask", DESTRUCTIVE_AGENT_MSG, DESTRUCTIVE_USER_MSG
    return "allow", "", ""


def classify(cmd: str) -> tuple[str, str, str]:
    """Return (permission, agent_message, user_message) for one command.

    Fail toward asking: the command-position reading asks on its own (E2/E3),
    and main's raw-string reading still asks on whatever is left once proven
    data is blanked. So the guard asks at least where main's guard did, except
    on E1's data (F29).
    """
    if not cmd:
        return "allow", "", ""
    bodies: list = []
    try:
        commands = _commands(cmd, bodies)
        env_pairs = _env_git_configs(cmd)
    except (ShellSyntaxError, IndexError, RecursionError):
        return _classify_text(cmd)
    if any(_bypasses(words) for words in commands) \
            or any(_bypasses(words, tuple(configs))
                   for configs, group in env_pairs for words in group):
        return "ask", NO_VERIFY_AGENT_MSG, NO_VERIFY_USER_MSG
    if any(_destroys(words) for words in commands) \
            or any(_destroys(words, tuple(configs))
                   for configs, group in env_pairs for words in group):
        return "ask", DESTRUCTIVE_AGENT_MSG, DESTRUCTIVE_USER_MSG
    if any(_runs_unread_text(words) for words in commands):
        return _classify_text(cmd)
    return _classify_text(_residual(cmd, _data_spans(commands, bodies), bodies))


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
