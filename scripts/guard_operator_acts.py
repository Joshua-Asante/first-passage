#!/usr/bin/env python3
"""guard_operator_acts.py — agent calls that would perform an operator act.

Rule owner: `docs/adr/2026-07-14-cc-cursor-surface-allocation.md` §Decision, "Action
classes and the authority block" (2026-09-25 revision). Capability ids in the messages
are the ones registered in `scripts/seat_authority.yml`.

**Best effort, not the enforcement boundary** (operator ruling 2026-09-25: "keep the hook
best-effort, ruleset as enforcement"). This hook reads the common ways a Claude Code
session writes an operator act and puts the call in front of the operator (``ask``) or
refuses it (``deny``). It reads command text, so a determined or unusual form gets past
it (see *Not read* below). What enforces is server-side or in the rail itself, verified
read-only on 2026-09-25:

  * GitHub ruleset 21071355 ``main-protection`` (active on ``refs/heads/main``, empty
    bypass list, ``current_user_can_bypass: never``): a pull request is required, the
    ``skills (3.12)`` status is required and strict, and non-fast-forward updates and
    deletion are blocked. It stops a direct or forced push to ``main`` from any
    credential. It does **not** stop a credential with write access from merging a PR
    whose status is green: the merge prompt below is best effort, and an agent without a
    merge-capable credential is the real limit.
  * The repository setting ``allow_auto_merge: false``: GitHub refuses to enable
    auto-merge on any PR, whoever asks.
  * The arming interlock in `ops/c1_rail/c1_rail_arm.py`
    (``validate_c1_monitoring_acceptance.validate(require_resolved=True)``): it refuses to
    arm unless the M1 artifact validates as RESOLVED, or ``--acknowledge-m1-unresolved``
    is given against a structurally valid unresolved artifact (which writes an
    ``arming_deviation`` record). It does not check for an operator GO.
  * ``fly deploy`` has **no** server-side enforcement: only where the Fly credential is
    held, and this hook's prompt.

Operator acts (risk ``high``) are performed by the operator through an act they already
perform. When the hook recognises one, it asks: the harness prompt is an operator
interaction, which a model's "the operator approved this" is not. A forbidden act it
recognises is refused (``deny``). One prompt names every operator act it found in the
call, because one answer approves all of them.

  * ``pr.merge``     — ask, **only when pinned to a full 40-hex head SHA**: the GitHub MCP
                       ``merge_pull_request`` tool with ``expectedHeadSha``; ``gh pr merge
                       --match-head-commit <sha>`` (the last one given, as gh reads it); a
                       ``gh api`` call on a ``pulls/<n>/merge`` path with a ``sha`` request
                       field; or a ``mergePullRequest`` mutation whose ``expectedHeadOid``
                       argument is a SHA literal or a variable the call supplies as one (a
                       SHA in a comment or a string pins nothing, and every merge in the
                       mutation must be pinned). GitHub refuses the merge if the head moved,
                       so the operator's answer approves exactly the bytes the prompt names.
                       An unpinned merge is denied with the pinned form to use
                       (``pr.merge_unpinned``), and so is a ``gh api`` call whose body the
                       hook cannot read (``--input``, or a ``-F`` field read from a file): it
                       cannot prove the call is not a merge or an auto-merge. That refuses
                       a read-only ``gh api graphql --input q.json`` too. A merge call with a
                       flag the hook does not know is refused the same way: it cannot tell
                       which word is the pin. ``gh pr merge --disable-auto`` and ``--help``
                       are silent: gh disables auto-merge (or prints help) and returns
                       before merging.
  * ``pr.auto_merge``— deny: the GitHub MCP ``enable_pr_auto_merge`` tool;
                       ``gh pr merge --auto`` (unless its last value is one of pflag's
                       false spellings, which leaves a merge, judged as ``pr.merge``); an
                       ``enablePullRequestAutoMerge`` mutation.
                       Merge authority is the operator's with no automated exception.
                       Server-side, ``allow_auto_merge: false`` refuses it for every form.
  * ``main.direct_push`` — deny: ``git push`` with ``main`` as a destination (``main``,
                       ``HEAD:main``, ``+x:refs/heads/main``, ``--delete main``), a bulk push
                       that includes it (``--all`` / ``--branches`` / ``--mirror`` or git's
                       abbreviations of them), the matching refspec ``:``, or a glob
                       destination that covers ``main``. ``main`` takes PRs only. A push with
                       no refspec is not judged (the current branch is not visible to the
                       hook), nor is a dry run (``--dry-run`` / ``-n`` in effect after the
                       last ``--no-dry-run``): it updates nothing. Server-side, the ruleset
                       refuses every push to ``main``.
  * ``rail.deploy``  — ask: ``fly deploy`` / ``flyctl deploy`` (any Fly app, not only the
                       rail's). Nothing server-side backs this prompt.
  * ``rail.arm``     — ask: ``c1_rail_arm.py --arm`` (or argparse's ``--ar``), as a script
                       or ``-m`` module, through the ``fp.ps1`` launcher or ``pwsh``, and
                       inside ``fly ssh console -C '…'`` (``-sC '…'`` and ``-C'…'`` too).
                       An arm that passes
                       ``--acknowledge-m1-unresolved`` still asks, under a prompt that says
                       M1 is not resolved. ``--disarm`` and ``--status`` never ask:
                       disarming is a risk-reducing exit and must never wait on a prompt.

**Scope — what this hook is not.** It covers the Claude Code harness only (Codex and
Z Code sessions are not hooked). It adds a prompt where an agent session holds a
credential that could otherwise act; it does not replace the ruleset, the repository
setting, the arming interlock or keeping credentials off agent environments. It cannot
see ``trade.submit``: that is enforced by the trading credentials never being present in
an agent environment.

**Reading commands.** Bash and PowerShell tool commands are read with
`scripts/_shell_tokens.py` in strict mode, judging words in command position (wrappers,
``bash -c`` scripts and ``$(…)`` bodies are expanded by that module; ``pwsh`` /
``powershell`` command lines and the ``fp.ps1`` launcher are unwrapped here; in PowerShell
text a backslash is read as a path separator and a backtick escape is resolved), so a
commit message or grep pattern that mentions ``gh pr merge`` does not prompt. ``gh``
flags are read as pflag reads them (shorthand clusters such as ``-iX POST``, a value
flag taking the next word even when it starts with ``-``); flags before the subcommand
name are read as cobra reads them while it looks for the subcommand (only ``-h`` /
``--help`` / ``--version`` are booleans there) and also the looser way this hook read
them before. ``fly`` and ``git`` global flags the hook does not list are read both as
taking the next word and as not. A command the tokenizer cannot read falls back to raw
regexes, toward refusing: unreadable text cannot prove a pin.

**Not read (residual classes, left to the server-side boundaries above).**

  * Values the shell computes at run time: shell or PowerShell variables and
    expressions (``$b='main'; git push origin $b``), ``Invoke-Expression``,
    ``Start-Process``, ``pwsh -Command -`` (stdin), and encodings other than
    ``-EncodedCommand``.
  * PowerShell structure beyond a plain pipeline: script blocks (``1..1 |
    ForEach-Object { … }``, ``try { … } catch {}``) and dot-sourcing
    (``. gh pr merge …``).
  * Configuration that changes what a command does: user-defined ``gh`` / ``git``
    aliases, ``git -c alias.x=push``, ``push.default`` / ``remote.<r>.push`` /
    ``remote.<r>.mirror``, and gh or git flags this hook's tables do not list.
  * Other routes to the same effect: GitHub API writes to ``main`` other than a merge
    (a ``git/refs`` update, for example), other clients or scripts that call GitHub, and
    remote execution on the rail other than ``fly ssh console -C`` (``fly machine exec``,
    for example).

Contract: JSON on stdin (``tool_name``, ``tool_input``); on a match, Claude Code's
PreToolUse decision JSON on stdout; on anything else, nothing (a hook ``allow`` would
override the operator's permission settings). Fail-open on malformed input.
"""
from __future__ import annotations

import base64
import binascii
import fnmatch
import functools
import json
import re
import sys
from typing import NamedTuple

try:  # imported as `scripts.guard_operator_acts` (tests, repo root on sys.path)
    from scripts._shell_tokens import expand, program, segments
except ImportError:  # run as `python scripts/guard_operator_acts.py`
    from _shell_tokens import expand, program, segments

ASK, DENY = "ask", "deny"

MCP_MERGE = "mcp__github__merge_pull_request"
MCP_AUTO_MERGE = "mcp__github__enable_pr_auto_merge"
SHELL_TOOLS = frozenset({"Bash", "PowerShell"})
_SHA = re.compile(r"[0-9a-fA-F]{40}")

# Every capability id the hook emits and its decision. A deny is a registry `forbidden:`
# entry (or the unpinned form of `pr.merge`); an ask is a registry `high` capability.
DECISION = {
    "pr.merge": ASK,
    "pr.merge_unpinned": DENY,
    "pr.auto_merge": DENY,
    "main.direct_push": DENY,
    "rail.deploy": ASK,
    "rail.arm": ASK,
}

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

# Details that change a hit's message; its capability and decision stay the same.
OPAQUE = "opaque"
UNREAD = "unread"
M1_UNRESOLVED = "m1-unresolved"
_DETAIL_MESSAGES = {
    ("pr.merge_unpinned", OPAQUE): (
        "Refused: the request body is in a file the guard cannot read (pr.merge / "
        "pr.auto_merge). Re-issue it with the query and fields inline.",
        "`gh api --input` and `-F name=@file` hide the request from the guard, so it "
        "cannot prove the call is not a merge or an auto-merge. Put the query and fields "
        "inline (`-f query='…'`); a merge must still pin the head SHA."),
    ("pr.merge_unpinned", UNREAD): (
        "Refused: this gh call has a flag the guard does not know, or one missing its "
        "value, so it cannot read the request or the pin (pr.merge / pr.auto_merge).",
        "The guard reads `gh` flags as gh v2.92.0 does; with an unknown flag it cannot tell "
        "an option's value from a flag, so it cannot prove the call is not an unpinned "
        "merge. Re-issue it with the documented flags only; a merge must pin the head SHA."),
    ("rail.arm", M1_UNRESOLVED): (
        "Arming the c1 rail with M1 UNRESOLVED (rail.arm, --acknowledge-m1-unresolved): "
        "this overrides the M1 RESOLVED interlock and writes an arming_deviation record. "
        "Confirm only if you, the operator, are taking that deviation for this armed "
        "session now.",
        "This arm overrides an unresolved M1 (AGENTS.md: dry_run=false requires M1 "
        "RESOLVED). Do not proceed unless the operator confirms this prompt."),
}


class Hit(NamedTuple):
    """One operator or forbidden act found in a call."""

    cap: str
    detail: str | None = None  # the pinned head SHA for pr.merge; a message detail otherwise

    @property
    def decision(self) -> str:
        return DECISION[self.cap]


_MERGE_PATH = re.compile(r"pulls/+[^/\s]+/+merge\b", re.IGNORECASE)
_FALLBACK = (
    (re.compile(r"\bgh\b.*\bpr\s+merge\b.*--auto\b"), "pr.auto_merge"),
    (re.compile(r"enablePullRequestAutoMerge"), "pr.auto_merge"),
    (re.compile(r"\bgh\b.*\bpr\s+merge\b"), "pr.merge_unpinned"),
    (re.compile(_MERGE_PATH.pattern + r"|mergePullRequest", re.IGNORECASE),
     "pr.merge_unpinned"),
    (re.compile(r"\bgit\b[^;&|\n]*\bpush\b[^;&|\n]*(?:[\s:+'\"](?:(?:refs/)?heads/)?main"
                r"(?![\w./:-])|\s--(?:all?|b[a-z]*|m[a-z]*)(?![\w-])|\s\+?:(?=[\s'\"]|$))"),
     "main.direct_push"),
    (re.compile(r"\b(fly|flyctl)\b.*\bdeploy\b"), "rail.deploy"),
    (re.compile(r"c1_rail_arm\S*\s.*--arm?\b"), "rail.arm"),
)

# Flag tables: long name -> (shorthand, takes a value), as `--help` lists them. gh
# v2.92.0 (`gh api --help`, `gh pr merge --help`, inherited flags included); fly
# v0.4.102 global flags plus the app/config flags its commands share.
_GH_API_FLAGS = {
    "cache": ("", True), "field": ("F", True), "header": ("H", True),
    "hostname": ("", True), "include": ("i", False), "input": ("", True),
    "jq": ("q", True), "method": ("X", True), "paginate": ("", False),
    "preview": ("p", True), "raw-field": ("f", True), "silent": ("", False),
    "slurp": ("", False), "template": ("t", True), "verbose": ("", False),
    "help": ("h", False)}
_GH_MERGE_FLAGS = {
    "admin": ("", False), "author-email": ("A", True), "auto": ("", False),
    "body": ("b", True), "body-file": ("F", True), "delete-branch": ("d", False),
    "disable-auto": ("", False), "match-head-commit": ("", True), "merge": ("m", False),
    "rebase": ("r", False), "squash": ("s", False), "subject": ("t", True),
    "repo": ("R", True), "help": ("h", False)}
_FLY_FLAGS = {
    "access-token": ("t", True), "app": ("a", True), "config": ("c", True),
    "debug": ("", False), "verbose": ("", False), "help": ("h", False)}
_GH_TRUE = frozenset({"1", "t", "T", "TRUE", "true", "True"})  # pflag's true spellings
_GH_FALSE = frozenset({"0", "f", "F", "FALSE", "false", "False"})  # and its false ones
_GRAPHQL_ENDPOINT = re.compile(r"(^|/)graphql/?(\?|$)", re.IGNORECASE)
_GIT_GLOBAL_VALUES = frozenset({"-C", "-c", "--git-dir", "--work-tree", "--namespace",
                                "--config-env", "--exec-path", "--attr-source",
                                "--super-prefix"})
_GIT_GLOBAL_BOOLS = frozenset({"-p", "-P", "--paginate", "--no-pager", "--bare",
                               "--no-replace-objects", "--literal-pathspecs",
                               "--glob-pathspecs", "--noglob-pathspecs",
                               "--icase-pathspecs", "--no-optional-locks", "--no-advice",
                               "-v", "--version", "-h", "--help"})
# Push options that take their value as the next word. `--signed` and
# `--force-with-lease` take one only after `=`, and `--force-if-includes` none.
_GIT_PUSH_VALUES = frozenset({"-o", "--push-option", "--receive-pack", "--exec",
                              "--repo", "--recurse-submodules"})
_GIT_PUSH_SHORT_BOOLS = frozenset("vqnfud46")  # `git push -h`: the short booleans
_GIT_BULK_PUSH = ("all", "branches", "mirror")  # git accepts any unambiguous prefix
# Every `git push` long option (`git push -h`, git 2.50): what a `--no-<prefix>` must be
# unique among before git reads it as the negation of one.
_GIT_PUSH_LONG = ("all", "atomic", "branches", "delete", "dry-run", "exec", "follow-tags",
                  "force", "force-if-includes", "force-with-lease", "ipv4", "ipv6",
                  "mirror", "no-verify", "porcelain", "progress", "prune", "push-option",
                  "quiet", "receive-pack", "recurse-submodules", "repo", "set-upstream",
                  "signed", "tags", "thin", "verbose", "verify")
_MAIN = frozenset({"main", "heads/main", "refs/heads/main"})
_PYTHONS = re.compile(r"(python(\d+(\.\d+)?)?|py|pypy3?)")

# pwsh 7.6 and Windows PowerShell 5.1 command-line parameters (`pwsh -?`, `powershell
# -?`), with each alias that is not a prefix of its name: what the parameter does with
# the words after it. A typed name may be any prefix; every parameter it could name is
# taken, and one that names none (pwsh then fails) is read as a switch and as taking a value.
_PS_PARAMS = {
    "command": "command", "commandwithargs": "command", "cwa": "command",
    "file": "file", "encodedcommand": "encoded", "ec": "encoded",
    "configurationfile": "value", "configurationname": "value", "custompipename": "value",
    "encodedarguments": "value", "ea": "value", "executionpolicy": "value", "ep": "value",
    "inputformat": "value", "if": "value", "outputformat": "value", "of": "value",
    "psconsolefile": "value", "settingsfile": "value", "version": "value",
    "windowstyle": "value", "workingdirectory": "value", "wd": "value",
    "help": "switch", "?": "switch", "interactive": "switch", "login": "switch",
    "mta": "switch", "sta": "switch", "noexit": "switch", "nologo": "switch",
    "noninteractive": "switch", "noprofile": "switch", "noprofileloadtime": "switch",
    "namedpipeservermode": "switch", "servermode": "switch", "socketservermode": "switch",
    "sshservermode": "switch"}
# A PowerShell backtick escape: `` `u{…} ``, a line break (continuation), or one character.
_PS_ESCAPE = re.compile(r"`(u\{[0-9A-Fa-f]{1,6}\}|\r\n|[\s\S])")
_PS_CONTROL = {"n": "\n", "r": "\n", "t": "\t", "0": " ", "a": " ", "b": " ", "e": " ",
               "f": " ", "v": " "}
_PS_PLAIN = re.compile(r"[\w.,:=@+%/-]")  # characters with no meaning to the POSIX reader

# GraphQL lexical grammar, enough to tell arguments from comments and strings.
_GQL_TOKEN = re.compile(
    r'(?P<skip>[\s,﻿]+|#[^\n\r]*)'
    r'|(?P<block>"""(?:\\"""|(?!""")[\s\S])*""")'
    r'|(?P<str>"(?:\\.|[^"\\\n\r])*")'
    r'|(?P<var>\$[_A-Za-z][_0-9A-Za-z]*)'
    r'|(?P<name>[_A-Za-z][_0-9A-Za-z]*)'
    r'|(?P<num>-?[0-9][_0-9A-Za-z.+-]*)'
    r'|(?P<punct>\.\.\.|[!&():=@\[\]{|}])')
_OPEN, _CLOSE = frozenset("([{"), frozenset(")]}")


def _spellings(tables: tuple[dict, ...], takes_value: bool) -> frozenset[str]:
    """The ``--name`` / ``-x`` spellings of the flags in `tables` that do (or do not)
    take a value."""
    return frozenset(spelling for table in tables for name, (short, value) in table.items()
                     if value == takes_value
                     for spelling in (f"--{name}", f"-{short}" if short else "") if spelling)


def _command_paths(args: list[str], values: frozenset[str], bools: frozenset[str],
                   depth: int) -> list[tuple[int, ...]]:
    """Every way a cobra program could pick its first `depth` command words from `args`,
    as their indices. While it looks for subcommands cobra skips a flag's value: a
    ``-x`` or ``--name`` written without ``=`` takes the next word unless it is a boolean.
    A flag the guard knows is read that way; any other is read both ways."""
    paths, seen, todo = set(), set(), [(0, ())]
    while todo:
        state = todo.pop()
        if state in seen:
            continue
        seen.add(state)
        i, picked = state
        if len(picked) == depth or i >= len(args) or args[i] == "--":
            paths.add(picked)
            continue
        arg = args[i]
        if arg and not arg.startswith("-"):
            todo.append((i + 1, picked + (i,)))
            continue
        takes = "=" not in arg and (arg.startswith("--") or len(arg) == 2)
        if takes and arg not in bools:
            todo.append((i + 2, picked))
        if not takes or arg not in values:
            todo.append((i + 1, picked))
    return sorted(paths)


def _without(args: list[str], indices: tuple[int, ...]) -> list[str]:
    return [arg for i, arg in enumerate(args) if i not in indices]


class _Parsed(NamedTuple):
    options: list[tuple[str, str]]  # (long name, value) in command-line order
    words: list[str]                # positional arguments
    unread: bool                    # a flag the table does not know, or one missing its value


def _pflag(args: list[str], table: dict) -> _Parsed:
    """`args` read as pflag (gh, fly) reads them against `table`. A value flag takes the
    rest of its shorthand cluster (``-XPOST``, ``-f=k=v``) or else the next word, even
    one that starts with ``-``; a boolean takes none; ``--`` ends the flags."""
    shorts = {short: name for name, (short, _) in table.items() if short}
    options: list[tuple[str, str]] = []
    words: list[str] = []
    unread, i = False, 0
    while i < len(args):
        arg, i = args[i], i + 1
        if arg == "--":
            words += args[i:]
            break
        if len(arg) < 2 or arg[0] != "-":
            words.append(arg)
        elif arg[1] == "-":
            name, eq, value = arg[2:].partition("=")
            spec = table.get(name)
            if spec is None or (not eq and spec[1] and i >= len(args)):
                unread = True
            elif eq:
                options.append((name, value))
            elif spec[1]:
                options.append((name, args[i]))
                i += 1
            else:
                options.append((name, "true"))
        else:
            rest = arg[1:]
            while rest:
                name, rest = shorts.get(rest[0]), rest[1:]
                if name is None or (table[name][1] and not rest and i >= len(args)):
                    unread = True
                    break
                if len(rest) > 1 and rest[0] == "=":
                    value, rest = rest[1:], ""
                elif not table[name][1]:
                    value = "true"
                elif rest:
                    value, rest = rest, ""
                else:
                    value, i = args[i], i + 1
                options.append((name, value))
    return _Parsed(options, words, unread)


def _merge_hit(sha: object) -> Hit:
    if isinstance(sha, str) and _SHA.fullmatch(sha):
        return Hit("pr.merge", sha)
    return Hit("pr.merge_unpinned")


def _judge_pr_merge(args: list[str]) -> list[Hit]:
    parsed = _pflag(args, _GH_MERGE_FLAGS)
    value = dict(parsed.options)  # pflag: the last occurrence wins
    # An `--auto` whose last value is not one of pflag's false spellings is auto-merge
    # (a value gh cannot parse is refused the same way); an explicit false is a merge.
    if ("auto" in value and value["auto"] not in _GH_FALSE) or (
            parsed.unread and any(a == "--auto" or a.startswith("--auto=") for a in args)):
        return [Hit("pr.auto_merge")]
    if parsed.unread:
        return [Hit("pr.merge_unpinned", UNREAD)]
    if value.get("help") in _GH_TRUE or value.get("disable-auto") in _GH_TRUE:
        return []  # gh prints help, or disables auto-merge and returns before merging
    return [_merge_hit(value.get("match-head-commit"))]


def _api_fields(parsed: _Parsed) -> tuple[dict[str, str], bool]:
    """The request fields of a ``gh api`` call (last value wins), and whether any part
    of the request is read from a file the guard cannot see."""
    fields: dict[str, str] = {}
    opaque = parsed.unread  # an unknown flag: which words are fields is not known either
    for name, value in parsed.options:
        if name == "input":
            opaque = True
        elif name in ("raw-field", "field"):
            key, eq, field = value.partition("=")
            if eq:
                opaque |= name == "field" and field.startswith("@")  # `-F k=@file`
                fields[key] = field
    return fields, opaque


def _gql_tokens(text: str) -> list[tuple[str, str]] | None:
    out, pos = [], 0
    while pos < len(text):
        match = _GQL_TOKEN.match(text, pos)
        if not match:
            return None
        if match.lastgroup != "skip":
            out.append((match.lastgroup, match.group()))
        pos = match.end()
    return out


def _gql_close(toks: list[tuple[str, str]], start: int) -> int | None:
    depth = 0
    for j in range(start, len(toks)):
        kind, text = toks[j]
        if kind == "punct" and text in _OPEN:
            depth += 1
        elif kind == "punct" and text in _CLOSE:
            depth -= 1
            if depth == 0:
                return j
    return None


def _gql_pin(arguments: list[tuple[str, str]], fields: dict[str, str]) -> str | None:
    """The head SHA one ``mergePullRequest(…)`` argument list pins, or None."""
    for j in range(len(arguments) - 2):
        (kind, text), colon, (vkind, value) = arguments[j:j + 3]
        if kind != "name" or colon != ("punct", ":"):
            continue
        if text == "expectedHeadOid":
            if vkind == "str":
                return value[1:-1]
            return fields.get(value[1:]) if vkind == "var" else None
        if text == "input" and vkind == "var":
            return fields.get(f"{value[1:]}[expectedHeadOid]")
    return None


def _graphql_pins(query: str, fields: dict[str, str]) -> list[str | None]:
    """The pin of each ``mergePullRequest`` field the query executes (comments and
    string contents are not arguments); empty when there is none or it cannot be read."""
    toks = _gql_tokens(query)
    if toks is None:
        return []
    pins: list[str | None] = []
    for i, tok in enumerate(toks):
        if tok == ("name", "mergePullRequest") and toks[i + 1:i + 2] == [("punct", "(")]:
            end = _gql_close(toks, i + 1)
            if end is None:
                return []
            pins.append(_gql_pin(toks[i + 2:end], fields))
    return pins


def _judge_api(args: list[str]) -> list[Hit]:
    """`args` are the ``gh api`` arguments without the ``api`` word."""
    parsed = _pflag(args, _GH_API_FLAGS)
    text = " ".join(args)
    if "enablePullRequestAutoMerge" in text:
        return [Hit("pr.auto_merge")]
    if not parsed.unread and dict(parsed.options).get("help") in _GH_TRUE:
        return []  # gh prints help and sends nothing
    fields, opaque = _api_fields(parsed)
    detail = UNREAD if parsed.unread else OPAQUE
    # With an unknown flag the endpoint is not known either: any word may be it.
    endpoints = args if parsed.unread else parsed.words[:1]
    if any(_GRAPHQL_ENDPOINT.search(e) for e in endpoints) or "mergePullRequest" in text:
        if opaque or "query" not in fields:
            return [Hit("pr.merge_unpinned", detail)]
        if "mergePullRequest" not in text:
            return []
        pins = _graphql_pins(fields["query"], fields)
        if pins and all(isinstance(p, str) and _SHA.fullmatch(p) for p in pins):
            return [Hit("pr.merge", p) for p in pins]
        return [Hit("pr.merge_unpinned")]
    if _MERGE_PATH.search(text):
        return [Hit("pr.merge_unpinned", detail) if opaque else _merge_hit(fields.get("sha"))]
    return []


_FLY_VALUE_FLAGS = _spellings((_FLY_FLAGS,), True)
_FLY_BOOL_FLAGS = _spellings((_FLY_FLAGS,), False)

# The boolean flags gh's root and `pr` commands define. While cobra looks for the
# subcommand, every other flag written without `=` takes the next word.
_GH_ROOT_BOOLS = frozenset({"-h", "--help", "--version"})
_GH_PR_BOOLS = frozenset({"-h", "--help"})
_GH_LOOSE_VALUES = frozenset({"-R", "--repo", "--hostname"})


def _cobra_strip(args: list[str], indices: list[int], bools: frozenset[str]) -> list[int]:
    """cobra's `stripFlags` over ``args[i] for i in indices``: the indices left as command
    words. ``--name`` or a two-character ``-x`` written without ``=`` takes the next word
    unless it is in `bools`; followed by only one word, cobra stops there."""
    out, k = [], 0
    while k < len(indices):
        arg = args[indices[k]]
        k += 1
        if arg == "--":
            break
        if arg.startswith("-") and "=" not in arg and (arg.startswith("--") or len(arg) == 2) \
                and arg not in bools:
            if len(indices) - k <= 1:
                break
            k += 1
        elif arg and not arg.startswith("-"):
            out.append(indices[k - 1])
    return out


def _gh_paths(args: list[str]) -> list[tuple[int, ...]]:
    """The indices of ``api`` or ``pr merge`` in a gh command line under two readings:
    cobra's (how gh finds its subcommand) and a loose one that takes every flag except
    ``-R`` / ``--repo`` / ``--hostname`` as a boolean (the reading this hook used before
    the cobra one; kept so that no form it caught is lost)."""
    paths: list[tuple[int, ...]] = []
    everything = list(range(len(args)))
    root = _cobra_strip(args, everything, _GH_ROOT_BOOLS)
    if root and args[root[0]] == "api":
        paths.append((root[0],))
    elif root and args[root[0]] == "pr":
        sub = _cobra_strip(args, [i for i in everything if i != root[0]], _GH_PR_BOOLS)
        if sub and args[sub[0]] == "merge":
            paths.append((root[0], sub[0]))
    loose, skip = [], False
    for i, arg in enumerate(args):
        if skip:
            skip = False
        elif arg in _GH_LOOSE_VALUES:
            skip = True
        elif not arg.startswith("-"):
            loose.append(i)
    if loose[:1] and args[loose[0]] == "api":
        paths.append((loose[0],))
    elif [args[i] for i in loose[:2]] == ["pr", "merge"]:
        paths.append(tuple(loose[:2]))
    return list(dict.fromkeys(paths))


def _judge_gh(args: list[str]) -> list[Hit]:
    """`gh pr merge` and `gh api` (cobra takes a subcommand's flags before its name too:
    ``gh -b x pr merge 1``)."""
    hits: list[Hit] = []
    for path in _gh_paths(args):
        if len(path) == 1:
            hits += _judge_api(_without(args, path))
        else:
            hits += _judge_pr_merge(_without(args, path))
    return hits


def _fly_commands(args: list[str]) -> list[str]:
    """Every value ``fly ssh console`` could run: ``--command v``, ``--command=v``, or a
    ``-C`` in a shorthand cluster, read both as taking the rest of the cluster and as
    taking the next word."""
    out = []
    for i, arg in enumerate(args):
        after = args[i + 1] if i + 1 < len(args) else ""
        if arg == "--command":
            out.append(after)
        elif arg.startswith("--command="):
            out.append(arg.split("=", 1)[1])
        elif arg.startswith("-") and not arg.startswith("--") and "C" in arg:
            rest = arg[arg.index("C") + 1:]
            out += [rest[1:] if rest.startswith("=") else rest, after]
    return [command for command in out if command]


def _judge_fly(args: list[str]) -> list[Hit]:
    hits: list[Hit] = []
    for command in _fly_commands(args):
        hits += _command_hits(command)
    paths = _command_paths(args, _FLY_VALUE_FLAGS, _FLY_BOOL_FLAGS, 1)
    if any([args[i] for i in path] == ["deploy"] for path in paths) and not _fly_help(args):
        hits.append(Hit("rail.deploy"))
    return hits


def _fly_help(args: list[str]) -> bool:
    """Whether cobra prints help and runs nothing: the last help setting before ``--`` is
    true. Each word is read by `_pflag`, so a help flag counts alone (``-h``,
    ``--help=<v>``), in a shorthand cluster (``-hac1-rail``) and after a flag that carries
    its value in its own word (``-ac1-rail --help``). A word the previous word may take
    as its value (``-a -h``; a flag the guard does not know is read both ways) may turn
    help off but never on."""
    help_on, prev = False, ""
    for arg in args:
        if arg == "--":
            break
        settings = [value for name, value in _pflag([arg], _FLY_FLAGS).options
                    if name == "help"]
        if settings:
            on = settings[-1] in _GH_TRUE
            maybe_value = _pflag([prev], _FLY_FLAGS).unread  # `prev` may want a word
            help_on = (help_on and on) if maybe_value else on
        prev = arg
    return help_on


def _bulk_push(arg: str) -> bool:
    """`--all` / `--branches` / `--mirror`, or a prefix git would expand to one."""
    if not arg.startswith("--"):
        return False
    name = arg[2:].split("=", 1)[0]
    return bool(name) and any(opt.startswith(name) for opt in _GIT_BULK_PUSH)


def _covers_main(spec: str) -> bool:
    body = spec.lstrip("+")
    if body == ":":
        return True  # the matching refspec pushes every branch both sides have
    dst = body.split(":", 1)[1] if ":" in body else body
    return dst in _MAIN or ("*" in dst and any(fnmatch.fnmatchcase(n, dst) for n in _MAIN))


def _judge_git(args: list[str]) -> list[Hit]:
    """`git push` whose destination is `main` — by refspec, bare branch, `--delete`, a
    bulk option, the matching refspec or a glob.

    A push with no refspec pushes the current branch, which this guard cannot see;
    that case stays with branch protection; so does a dry run, which updates nothing
    (`_push_dry_run`). A global option the guard does not list is
    read both as taking the next word and as not taking it.
    """
    for path in _command_paths(args, _GIT_GLOBAL_VALUES, _GIT_GLOBAL_BOOLS, 1):
        if not path or args[path[0]] != "push":
            continue
        push_args = args[path[0] + 1:]
        if not _push_dry_run(push_args) and _push_covers_main(push_args):
            return [Hit("main.direct_push")]
    return []


def _push_dry_run(push_args: list[str]) -> bool:
    """Whether git only simulates this push (it updates nothing): the last of
    ``--dry-run`` / ``-n`` (alone or in a short cluster) and ``--no-dry-run`` wins, each
    long form in any abbreviation git accepts. The value of a value option is skipped
    (``-o -n`` pushes), as is anything after ``--``. A word the guard cannot place — an
    ambiguous abbreviation, ``--dry-run=x``, an unknown short option — reads as not a dry
    run, so the push is judged."""
    dry, skip = False, False
    for arg in push_args:
        if skip:
            skip = False
        elif arg == "--":
            break
        elif arg.startswith("--"):
            name, eq, _ = arg[2:].partition("=")
            if _push_takes_next(arg):
                skip = True  # a value option (or an abbreviation of one)
            elif name and ("dry-run".startswith(name) or (
                    name.startswith("no-") and "no-dry-run".startswith(name))):
                # `--d` is ambiguous (`--delete`), and `--no-d` too (`--no-delete`).
                dry = not eq and len(name) >= 2 and not name.startswith("no-")
        elif arg.startswith("-") and len(arg) > 1:
            for char in arg[1:]:
                if char == "n":
                    dry = True
                elif char == "o":  # `-o`: its value is the rest of the cluster
                    break
                elif char not in _GIT_PUSH_SHORT_BOOLS:
                    dry = False
                    break
            skip = _push_takes_next(arg)  # `-no x`: a dry run whose `-o` takes `x`
    return dry


def _push_takes_next(arg: str) -> bool:
    """Whether git reads the word after this ``git push`` option word as its value: a
    long value option (or an abbreviation of one) written without ``=``, or a short
    cluster whose first ``o`` is its last character (``-o x``, ``-vo x``). In ``-ox`` the
    value is the rest of the word, so the next word is read on its own."""
    if arg.startswith("--"):
        name = arg[2:]
        return bool(name) and "=" not in name and any(
            o[2:].startswith(name) for o in _GIT_PUSH_VALUES if o.startswith("--"))
    return arg.startswith("-") and len(arg) > 1 and arg.find("o", 1) == len(arg) - 1


def _push_positional(push_args: list[str]) -> list[str]:
    """The repository and refspec words of a ``git push``: every word that is neither an
    option nor an option's value (`_push_takes_next`), and every word after ``--``."""
    out, skip = [], False
    for i, arg in enumerate(push_args):
        if skip:
            skip = False
        elif arg == "--":
            out += push_args[i + 1:]
            break
        elif arg.startswith("-") and len(arg) > 1:
            skip = _push_takes_next(arg)
        else:
            out.append(arg)
    return out


def _bulk_bit(name: str) -> str:
    return "mirror" if "mirror".startswith(name) else "all"  # `--branches` aliases `--all`


def _bulk_in_effect(push_args: list[str]) -> bool:
    """Whether a bulk option is still set once git has read every option, last wins per
    bit: ``--all`` / ``--branches`` (one bit; git 2.46+ aliases them) and ``--mirror``,
    each cleared by a later ``--no-<name>`` in any abbreviation git accepts as unique
    among `_GIT_PUSH_LONG`. A bulk-looking word counts wherever it stands (fail closed);
    a negation counts only in option position — not as a value option's value, not after
    ``--``, not with ``=`` and not when ambiguous (``--no-a``: git refuses the push)."""
    bits = {"all": False, "mirror": False}
    skip, options = False, True
    for arg in push_args:
        value, skip = skip, False
        if _bulk_push(arg):
            bits[_bulk_bit(arg[2:].split("=", 1)[0])] = True
            continue
        if value or not options:
            continue
        if arg == "--":
            options = False
        elif _push_takes_next(arg):
            skip = True  # `-o x`, `-vo x`, `--push-opt x`; `-ox` carries its own value
        elif arg.startswith("--no-") and "=" not in arg:
            rest = arg[5:]
            named = [o for o in _GIT_PUSH_LONG if o == rest] or [
                o for o in _GIT_PUSH_LONG if o.startswith(rest)]
            if rest and len(named) == 1 and named[0] in _GIT_BULK_PUSH:
                bits[_bulk_bit(named[0])] = False
    return any(bits.values())


def _push_covers_main(push_args: list[str]) -> bool:
    if _bulk_in_effect(push_args):
        return True
    # The first positional word is the repository, whatever `--repo` says: git reads
    # `--repo` only when no repository word is given (`repo = argv[0]` in
    # builtin/push.c; git 2.50: `git push -n --repo=origin main` looks for a repository
    # called `main`). Every later word is a refspec.
    return any(_covers_main(s) for s in _push_positional(push_args)[1:])


def _abbrev(arg: str, option: str, shortest: int) -> bool:
    """`arg` is `option` or an argparse abbreviation of it at least `shortest` long."""
    name = arg.split("=", 1)[0]
    return len(name) >= shortest and option.startswith(name)


def _judge_arm(args: list[str]) -> list[Hit]:
    if not any(_abbrev(a, "--arm", 4) for a in args):  # `--ar` is unique to `--arm`
        return []
    override = any(_abbrev(a, "--acknowledge-m1-unresolved", 5) for a in args)
    return [Hit("rail.arm", M1_UNRESOLVED if override else None)]


def _judge_python(args: list[str]) -> list[Hit]:
    def module(i: int) -> str:
        """The module a ``-m`` in the short cluster ``args[i]`` names: python reads a
        cluster left to right, and the first option that takes a value (``-c``, ``-m``,
        ``-W``, ``-X``) takes the rest of the word, or else the next word (``-Im mod``)."""
        arg = args[i]
        if not arg.startswith("-") or arg.startswith("--"):
            return ""
        for k, char in enumerate(arg[1:], start=2):
            if char == "m":
                return arg[k:] or (args[i + 1] if i + 1 < len(args) else "")
            if char in "cWX":
                return ""  # its value is the rest of the word, or the next word
        return ""

    target = any(a.replace("\\", "/").casefold().endswith("c1_rail_arm.py") for a in args) \
        or any(module(i).casefold().endswith("c1_rail_arm") for i in range(len(args)))
    return _judge_arm(args) if target else []


def _decode_powershell(value: str) -> str:
    try:
        return base64.b64decode(value, validate=True).decode("utf-16-le")
    except (binascii.Error, UnicodeDecodeError, ValueError):
        return ""


def _ps_kinds(arg: str) -> set[str]:
    """What a pwsh parameter could do: every `_PS_PARAMS` entry the typed name is a
    prefix of (case-insensitive). A name that matches none is read both as a switch and
    as taking a value."""
    name = arg.lstrip("-/").casefold()
    return {kind for param, kind in _PS_PARAMS.items() if param.startswith(name)} or {
        "switch", "value"}


def _judge_powershell(args: list[str]) -> list[Hit]:
    """What `pwsh` / `powershell` would run: -Command / -CommandWithArgs text, a -File
    script and its arguments, an -EncodedCommand, or a bare first argument (a -File for
    pwsh, a -Command for Windows PowerShell; judged both ways). Every reading of an
    ambiguous parameter is followed, so a parameter's value is not taken for the script."""
    hits: list[Hit] = []
    reach = {0}
    for i, arg in enumerate(args):
        if i not in reach:
            continue
        if not (arg.startswith("-") or (arg.startswith("/") and "/" not in arg[1:])):
            hits += _words_hits(args[i:]) + _powershell_hits(" ".join(args[i:]))
            continue
        kinds, rest = _ps_kinds(arg), args[i + 1:]
        if "command" in kinds:
            hits += _powershell_hits(" ".join(rest))
        if "file" in kinds:
            hits += _words_hits(rest)
        if "encoded" in kinds and rest:
            hits += _powershell_hits(_decode_powershell(rest[0]))
        if "switch" in kinds:
            reach.add(i + 1)
        if "value" in kinds:
            reach.add(i + 2)
    return hits


def _words_hits(words: list[str]) -> list[Hit]:
    """Acts in one simple command (`words[0]` in command position)."""
    if not words:
        return []
    base, args = program(words[0], strict=True), [str(w) for w in words[1:]]
    if base == "gh":
        return _judge_gh(args)
    if base in ("fly", "flyctl"):
        return _judge_fly(args)
    if base == "git":
        return _judge_git(args)
    if base in ("pwsh", "powershell"):
        return _judge_powershell(args)
    if base == "fp.ps1":  # the project launcher runs `<command> <args>` (AGENTS.md)
        return _words_hits(args)
    if _PYTHONS.fullmatch(base):
        return _judge_python(args)
    if base.endswith("c1_rail_arm.py"):
        return _judge_arm(args)
    return []


def _fallback_hits(command: str) -> list[Hit]:
    hits = []
    for pattern, cap in _FALLBACK:
        if pattern.search(command):
            unresolved = cap == "rail.arm" and "--ack" in command
            hits.append(Hit(cap, M1_UNRESOLVED if unresolved else None))
    return hits


def _command_hits(command: str) -> list[Hit]:
    """Every act in a shell command, in order."""
    return list(_command_hits_cached(command))


@functools.lru_cache(maxsize=4096)
def _command_hits_cached(command: str) -> tuple[Hit, ...]:
    # Cached by text: following every reading of nested `pwsh -c` parameters judges the
    # same suffix text many times, which would otherwise grow exponentially.
    try:
        hits: list[Hit] = []
        for tokens in segments(command, strict=True):
            for words in expand([str(t) for t in tokens], strict=True):
                hits += _words_hits([str(w) for w in words])
        return tuple(dict.fromkeys(hits))
    except Exception:  # unreadable (or unjudgeable): raw patterns, toward refusing
        return tuple(_fallback_hits(command))


def _ps_escape(match: re.Match) -> str:
    esc = match.group(1)
    if esc.startswith("u{") and len(esc) > 2:
        code = int(esc[2:-1], 16)
        esc = chr(code) if code <= 0x10FFFF else " "
    elif esc in ("\r\n", "\n", "\r"):
        return " "  # a backtick at a line end continues the line
    elif esc in _PS_CONTROL:
        return _PS_CONTROL[esc]
    if esc in ("\n", "\r"):
        return "\n"
    return esc if _PS_PLAIN.fullmatch(esc) else "\\" + esc


def _powershell_hits(command: str) -> list[Hit]:
    r"""`_command_hits` for PowerShell text. A backslash is a path separator there, not an
    escape (`.\fp.ps1`, `C:\tools\gh.exe`), so it is read as `/`. The backtick is the
    escape: `` `m `` is `m`, `` `u{6d} `` is `m`, `` `n `` / `` `r `` a newline (toward
    splitting: a newline separates statements once the text reaches a nested
    `pwsh -c`), `` `t `` and the other control escapes a blank, and an escaped shell
    character (`` `" ``, `` `$ ``, `` `  ``) a POSIX-escaped literal."""
    return _command_hits(_PS_ESCAPE.sub(_ps_escape, command.replace("\\", "/")))


def _verdict(hits: list[Hit]) -> Hit | None:
    """A deny anywhere wins over any ask: one wrapper cannot launder a forbidden act."""
    for hit in hits:
        if hit.decision == DENY:
            return hit
    return hits[0] if hits else None


def _payload_hits(payload: dict) -> list[Hit]:
    name = payload.get("tool_name") or ""
    tool_input = payload.get("tool_input") or {}
    if name == MCP_AUTO_MERGE:
        return [Hit("pr.auto_merge")]
    if name == MCP_MERGE:
        return [_merge_hit(tool_input.get("expectedHeadSha"))]
    if name in SHELL_TOOLS:
        command = tool_input.get("command")
        if isinstance(command, str):
            return _powershell_hits(command) if name == "PowerShell" else _command_hits(command)
    return []


def classify_command(command: str) -> tuple[str, str] | None:
    """(decision, capability) for a shell command, or None when it is not an operator act."""
    hit = _verdict(_command_hits(command))
    return (hit.decision, hit.cap) if hit else None


def classify(payload: dict) -> tuple[str, str] | None:
    """(decision, capability) for a PreToolUse payload, or None."""
    hit = _verdict(_payload_hits(payload))
    return (hit.decision, hit.cap) if hit else None


def _message(hit: Hit) -> tuple[str, str]:
    return _DETAIL_MESSAGES.get((hit.cap, hit.detail), MESSAGES[hit.cap])


def _reasons(hits: list[Hit], first: Hit) -> tuple[str, str]:
    """(operator prompt, agent context). A deny names the refused act; an ask names every
    operator act in the call and every head SHA it pins, since one answer approves all."""
    if first.decision == DENY:
        return _message(first)
    users, agents, seen = [], [], set()
    for hit in hits:
        key = (hit.cap, None if hit.cap == "pr.merge" else hit.detail)
        if key not in seen:
            seen.add(key)
            user, agent = _message(hit)
            users.append(user)
            agents.append(agent)
    shas = list(dict.fromkeys(h.detail for h in hits if h.cap == "pr.merge" and h.detail))
    if shas:
        label = "Head SHA" if len(shas) == 1 else "Head SHAs"
        users.append(f"{label} being approved: {', '.join(shas)}.")
    return " ".join(users), " ".join(agents)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        hits = _payload_hits(payload) if isinstance(payload, dict) else []
    except Exception:  # fail-open: a broken hook must not block unrelated work
        return 0
    first = _verdict(hits)
    if first:
        user_msg, agent_msg = _reasons(hits, first)
        sys.stdout.write(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": first.decision,
            "permissionDecisionReason": user_msg,
            "additionalContext": agent_msg,
        }}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
