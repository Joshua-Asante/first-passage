#!/usr/bin/env python3
"""guard_operator_acts.py — agent calls that would perform an operator act.

Rule owner: `docs/adr/2026-07-14-cc-cursor-surface-allocation.md` §Decision, "Action
classes and the authority block" (2026-09-25 revision). Capability ids in the messages
are the ones registered in `scripts/seat_authority.yml`.

Operator acts (risk ``high``) are performed by the operator through an act they already
perform. When an agent session reaches for one, this PreToolUse hook puts the call in
front of the operator (``ask``): the harness prompt is an authenticated operator
interaction, which a model's "the operator approved this" is not. A forbidden act is
refused outright (``deny``): no approval unlocks it for an agent. One prompt names every
operator act in the call, because one answer approves all of them.

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
                       cannot prove the call is not a merge or an auto-merge.
                       ``gh pr merge --disable-auto`` is silent: gh disables auto-merge and
                       returns before merging.
  * ``pr.auto_merge``— deny: the GitHub MCP ``enable_pr_auto_merge`` tool;
                       ``gh pr merge --auto``; an ``enablePullRequestAutoMerge`` mutation.
                       Merge authority is the operator's with no automated exception.
  * ``main.direct_push`` — deny: ``git push`` with ``main`` as a destination (``main``,
                       ``HEAD:main``, ``+x:refs/heads/main``, ``--delete main``), a bulk push
                       that includes it (``--all`` / ``--branches`` / ``--mirror`` or git's
                       abbreviations of them), the matching refspec ``:``, or a glob
                       destination that covers ``main``. ``main`` takes PRs only. A push with
                       no refspec is not judged (the current branch is not visible to the
                       hook; branch protection covers it).
  * ``rail.deploy``  — ask: ``fly deploy`` / ``flyctl deploy``.
  * ``rail.arm``     — ask: ``c1_rail_arm.py --arm`` (or argparse's ``--ar``), as a script
                       or ``-m`` module, through the ``fp.ps1`` launcher or ``pwsh``, and
                       inside ``fly ssh console -C '…'``. An arm that passes
                       ``--acknowledge-m1-unresolved`` still asks, under a prompt that says
                       M1 is not resolved. ``--disarm`` and ``--status`` never ask:
                       disarming is a risk-reducing exit and must never wait on a prompt.

**Scope — what this hook is not.** It is one enforcement point among the ones the ADR
names, for the Claude Code harness only. Credentials held off agent environments,
GitHub branch protection and the arming interlock in `ops/c1_rail/c1_rail_arm.py`
stay the boundaries; this hook adds a prompt where an agent session holds a credential
that could otherwise act. It cannot see ``trade.submit``: that is enforced by the
trading credentials never being present in an agent environment.

**Reading commands.** Bash and PowerShell tool commands are read with
`scripts/_shell_tokens.py` in strict mode, judging words in command position (wrappers,
``bash -c`` scripts and ``$(…)`` bodies are expanded by that module; ``pwsh`` /
``powershell`` command lines and the ``fp.ps1`` launcher are unwrapped here; in PowerShell
text a backslash is read as a path separator, not an escape), so a commit message or grep
pattern that mentions ``gh pr merge`` does not prompt. A command the
tokenizer cannot read falls back to raw regexes, toward refusing: unreadable text cannot
prove a pin.

Contract: JSON on stdin (``tool_name``, ``tool_input``); on a match, Claude Code's
PreToolUse decision JSON on stdout; on anything else, nothing (a hook ``allow`` would
override the operator's permission settings). Fail-open on malformed input.
"""
from __future__ import annotations

import base64
import binascii
import fnmatch
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
M1_UNRESOLVED = "m1-unresolved"
_DETAIL_MESSAGES = {
    ("pr.merge_unpinned", OPAQUE): (
        "Refused: the request body is in a file the guard cannot read (pr.merge / "
        "pr.auto_merge). Re-issue it with the query and fields inline.",
        "`gh api --input` and `-F name=@file` hide the request from the guard, so it "
        "cannot prove the call is not a merge or an auto-merge. Put the query and fields "
        "inline (`-f query='…'`); a merge must still pin the head SHA."),
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


_FALLBACK = (
    (re.compile(r"\bgh\b.*\bpr\s+merge\b.*--auto\b"), "pr.auto_merge"),
    (re.compile(r"enablePullRequestAutoMerge"), "pr.auto_merge"),
    (re.compile(r"\bgh\b.*\bpr\s+merge\b"), "pr.merge_unpinned"),
    (re.compile(r"pulls/[^/\s]+/merge\b|mergePullRequest"), "pr.merge_unpinned"),
    (re.compile(r"\bgit\b[^;&|\n]*\bpush\b[^;&|\n]*(?:[\s:+'\"](?:refs/heads/)?main"
                r"(?![\w./:-])|\s--(?:all?|b[a-z]*|m[a-z]*)(?![\w-])|\s\+?:(?=[\s'\"]|$))"),
     "main.direct_push"),
    (re.compile(r"\b(fly|flyctl)\b.*\bdeploy\b"), "rail.deploy"),
    (re.compile(r"c1_rail_arm\S*\s.*--arm?\b"), "rail.arm"),
)
_GH_GLOBAL_VALUES = frozenset({"-R", "--repo", "--hostname"})
# `gh` options that take their value as the next word (global, `pr merge` and `api`).
_GH_VALUES = _GH_GLOBAL_VALUES | frozenset({
    "-f", "--raw-field", "-F", "--field", "-H", "--header", "-X", "--method", "--input",
    "-q", "--jq", "-t", "--template", "--cache", "-p", "--preview"})
_GH_FIELDS = {"-f": False, "--raw-field": False, "-F": True, "--field": True}  # typed?
_GH_TRUE = frozenset({"1", "t", "T", "TRUE", "true", "True"})  # pflag's true spellings
_GRAPHQL_ENDPOINT = re.compile(r"(^|/)graphql/?(\?|$)")
_MERGE_PATH = re.compile(r"pulls/[^/\s]+/merge\b")
_GIT_GLOBAL_VALUES = frozenset({"-C", "-c", "--git-dir", "--work-tree", "--namespace",
                                "--config-env", "--exec-path"})
# Push options that take their value as the next word. `--signed` and
# `--force-with-lease` take one only after `=`, and `--force-if-includes` none.
_GIT_PUSH_VALUES = frozenset({"-o", "--push-option", "--receive-pack", "--exec",
                              "--repo", "--recurse-submodules"})
_GIT_BULK_PUSH = ("all", "branches", "mirror")  # git accepts any unambiguous prefix
_MAIN = frozenset({"main", "heads/main", "refs/heads/main"})
_FLY_COMMAND_OPTS = frozenset({"-C", "--command"})
_PYTHONS = re.compile(r"(python(\d+(\.\d+)?)?|py|pypy3?)")
_PS_VALUE_PARAMS = ("configurationfile", "configurationname", "custompipename",
                    "encodedarguments", "executionpolicy", "inputformat", "outputformat",
                    "settingsfile", "windowstyle", "workingdirectory")

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


def _option_values(args: list[str], name: str) -> list[str]:
    """Every value given to `name` (``name v`` or ``name=v``), in order."""
    out, i = [], 0
    while i < len(args):
        if args[i] == name:
            if i + 1 < len(args):
                out.append(args[i + 1])
            i += 2
            continue
        if args[i].startswith(name + "="):
            out.append(args[i].split("=", 1)[1])
        i += 1
    return out


def _bool_flag(args: list[str], name: str) -> bool:
    """A gh (pflag) boolean flag's value: the last occurrence wins."""
    value = False
    for arg in args:
        if arg == name:
            value = True
        elif arg.startswith(name + "="):
            value = arg.split("=", 1)[1] in _GH_TRUE
    return value


def _merge_hit(sha: object) -> Hit:
    if isinstance(sha, str) and _SHA.fullmatch(sha):
        return Hit("pr.merge", sha)
    return Hit("pr.merge_unpinned")


def _judge_pr_merge(args: list[str]) -> list[Hit]:
    if any(a == "--auto" or a.startswith("--auto=") for a in args):
        return [Hit("pr.auto_merge")]
    flags = args[:args.index("--")] if "--" in args else args
    if _bool_flag(flags, "--disable-auto"):
        return []  # gh disables auto-merge and returns before merging
    pins = _option_values(flags, "--match-head-commit")
    return [_merge_hit(pins[-1] if pins else None)]


def _api_fields(args: list[str]) -> tuple[dict[str, str], bool]:
    """The request fields of a ``gh api`` call (last value wins), and whether any part
    of the request is read from a file the guard cannot see."""
    fields: dict[str, str] = {}
    opaque, i = False, 0
    while i < len(args):
        arg, pair, typed = args[i], None, False
        if arg in _GH_FIELDS:
            typed = _GH_FIELDS[arg]
            pair = args[i + 1] if i + 1 < len(args) else None
            i += 1
        elif arg.startswith(("--raw-field=", "--field=")):
            flag, pair = arg.split("=", 1)
            typed = flag == "--field"
        elif len(arg) > 2 and arg[:2] in ("-f", "-F"):  # `-fk=v` or pflag's `-f=k=v`
            typed, pair = arg[1] == "F", arg[3:] if arg[2] == "=" else arg[2:]
        elif arg == "--input" or arg.startswith("--input="):
            opaque = True
            if arg == "--input":
                i += 1
        elif arg in _GH_VALUES:
            i += 1  # another option's value (a header is not a request field)
        if pair is not None and "=" in pair:
            key, value = pair.split("=", 1)
            if typed and value.startswith("@"):
                opaque = True  # `-F name=@file` reads the value from a file
            fields[key] = value
        i += 1
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


def _judge_api(args: list[str], endpoint: str) -> list[Hit]:
    fields, opaque = _api_fields(args)
    text = " ".join(args)
    if "enablePullRequestAutoMerge" in text:
        return [Hit("pr.auto_merge")]
    if _GRAPHQL_ENDPOINT.search(endpoint) or "mergePullRequest" in text:
        if opaque or "query" not in fields:
            return [Hit("pr.merge_unpinned", OPAQUE)]
        if "mergePullRequest" not in text:
            return []
        pins = _graphql_pins(fields["query"], fields)
        if pins and all(isinstance(p, str) and _SHA.fullmatch(p) for p in pins):
            return [Hit("pr.merge", p) for p in pins]
        return [Hit("pr.merge_unpinned")]
    if _MERGE_PATH.search(text):
        return [Hit("pr.merge_unpinned", OPAQUE) if opaque else _merge_hit(fields.get("sha"))]
    return []


def _judge_gh(args: list[str]) -> list[Hit]:
    words = _positional(args, _GH_VALUES)
    if words[:2] == ["pr", "merge"]:
        return _judge_pr_merge(args)
    if words[:1] == ["api"]:
        return _judge_api(args, words[1] if len(words) > 1 else "")
    return []


def _judge_fly(args: list[str]) -> list[Hit]:
    hits: list[Hit] = []
    for i, arg in enumerate(args):
        value = None
        if arg in _FLY_COMMAND_OPTS and i + 1 < len(args):
            value = args[i + 1]
        elif arg.startswith("--command="):
            value = arg.split("=", 1)[1]
        if value is not None:
            hits += _command_hits(value)
    if "deploy" in _positional(args, frozenset({"-a", "--app", "-c", "--config"}))[:1]:
        hits.append(Hit("rail.deploy"))
    return hits


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
    that case stays with branch protection.
    """
    words = _positional(args, _GIT_GLOBAL_VALUES)
    if words[:1] != ["push"]:
        return []
    push_args = args[args.index("push") + 1:]
    if any(_bulk_push(a) for a in push_args):
        return [Hit("main.direct_push")]
    words = _positional(push_args, _GIT_PUSH_VALUES)
    # `--repo` names the remote, so every positional word is then a refspec.
    has_repo = any(a == "--repo" or a.startswith("--repo=") for a in push_args)
    refspecs = words if has_repo else words[1:]  # after the remote
    return [Hit("main.direct_push")] if any(_covers_main(s) for s in refspecs) else []


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
        if args[i] == "-m" and i + 1 < len(args):
            return args[i + 1]
        return args[i][2:] if args[i].startswith("-m") else ""

    target = any(a.replace("\\", "/").casefold().endswith("c1_rail_arm.py") for a in args) \
        or any(module(i).casefold().endswith("c1_rail_arm") for i in range(len(args)))
    return _judge_arm(args) if target else []


def _decode_powershell(value: str) -> str:
    try:
        return base64.b64decode(value, validate=True).decode("utf-16-le")
    except (binascii.Error, UnicodeDecodeError, ValueError):
        return ""


def _judge_powershell(args: list[str]) -> list[Hit]:
    """What `pwsh` / `powershell` would run: -Command text, a -File script and its
    arguments, or an -EncodedCommand (parameter names are case-insensitive prefixes)."""
    i = 0
    while i < len(args):
        arg = args[i]
        is_param = arg.startswith("-") or (arg.startswith("/") and "/" not in arg[1:])
        if not is_param:
            # A bare first argument is a -File for pwsh and a -Command for Windows
            # PowerShell; judge it both ways.
            return _words_hits(args[i:]) + _powershell_hits(" ".join(args[i:]))
        name, rest = arg.lstrip("-/").split(":", 1)[0].casefold(), args[i + 1:]
        if name and "command".startswith(name):
            return _powershell_hits(" ".join(rest))
        if name and "file".startswith(name):
            return _words_hits(rest)
        if name == "ec" or (name and "encodedcommand".startswith(name)):
            return _powershell_hits(_decode_powershell(rest[0])) if rest else []
        i += 2 if name and any(p.startswith(name) for p in _PS_VALUE_PARAMS) else 1
    return []


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
    try:
        hits: list[Hit] = []
        for tokens in segments(command, strict=True):
            for words in expand([str(t) for t in tokens], strict=True):
                hits += _words_hits([str(w) for w in words])
        return hits
    except Exception:  # unreadable (or unjudgeable): raw patterns, toward refusing
        return _fallback_hits(command)


def _powershell_hits(command: str) -> list[Hit]:
    r"""`_command_hits` for PowerShell text, where a backslash is a path separator and
    not an escape (`.\fp.ps1`, `C:\tools\gh.exe`): read it as `/` so the program
    it names survives the POSIX reading."""
    return _command_hits(command.replace("\\", "/"))


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
