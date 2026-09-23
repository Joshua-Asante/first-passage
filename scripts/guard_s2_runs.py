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
import stat
import sys

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
WRAPPERS = frozenset({"command", "builtin", "exec", "nohup", "nice", "time", "sudo", "!",
                      "if", "then", "elif", "else", "while", "until", "do",
                      "done", "fi"})
SHELLS = frozenset({"bash", "sh", "zsh", "dash", "ksh"})
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
_ASSIGNMENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*=")


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
                f"(scripts/s2_run_evidence.py {run.get('databaseId')}"
                f"{' --expect-scope S2_DIAGNOSTIC_SUPERVISION' if mode == 's2' else ''}) "
                f"instead of re-running. Deliberate re-dispatch: {OVERRIDE} gh workflow run ….")
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


# --- tokenizer (D14) ----------------------------------------------------------

def _matching_paren(text: str, start: int) -> int:
    """Index of the ')' matching the '$(' whose body starts at `start`.

    Shell-aware, so a quote, `(` or `)` inside a heredoc body, a comment or an
    escaped character does not unbalance the scan (a heredoc in `$(cat <<'EOF'
    … EOF)` is the standard commit-message idiom).
    """
    depth, quote, i = 1, "", start
    pending: list[str] = []  # heredoc delimiters whose bodies start at the next newline
    while i < len(text):
        ch = text[i]
        if quote:
            if ch == "\\" and quote == '"':
                i += 2
                continue
            if ch == quote:
                quote = ""
            i += 1
            continue
        if ch == "\\":
            i += 2
            continue
        if ch in "'\"":
            quote = ch
        elif ch == "#" and (i == start or text[i - 1] in " \t\n;|&("):
            newline = text.find("\n", i)
            i = len(text) if newline < 0 else newline
            continue
        elif text.startswith("<<", i):
            i, delimiter = _consume_redirection(text, i)
            if delimiter:
                pending.append(delimiter)
            continue
        elif ch == "\n" and pending:
            i += 1
            for delimiter in pending:
                i = _heredoc_end(text, i, delimiter)
            pending.clear()
            continue
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return len(text)


def _skip_word(text: str, i: int) -> int:
    """Index after the shell word at text[i] (quotes and escapes honoured)."""
    quote = ""
    while i < len(text):
        ch = text[i]
        if quote:
            if ch == "\\" and quote == '"':
                i += 2
                continue
            if ch == quote:
                quote = ""
        elif ch == "\\":
            i += 1
        elif ch in "'\"":
            quote = ch
        elif ch in " \t\n;|&()<>":
            return i
        i += 1
    return i


def _consume_redirection(text: str, i: int) -> tuple[int, str]:
    """Skip the redirection starting at text[i]; a heredoc returns its delimiter."""
    if text[i:i + 2] == "<<" and text[i + 2:i + 3] != "<":
        i += 2 + (1 if text[i + 2:i + 3] == "-" else 0)
        while i < len(text) and text[i] in " \t":
            i += 1
        end = _skip_word(text, i)
        # Quoting or escaping any part of the delimiter only disables expansion.
        word = text[i:end].replace("'", "").replace('"', "").replace("\\", "")
        return end, word
    i += 3 if text[i:i + 3] == "<<<" else 1  # a here-string's word is data
    while i < len(text) and text[i] in "<>&":
        i += 1
    while i < len(text) and text[i] in " \t":
        i += 1
    return _skip_word(text, i), ""


def _heredoc_end(text: str, i: int, delimiter: str) -> int:
    """Index after the heredoc body that starts at text[i] (just past a newline)."""
    while i <= len(text):
        eol = text.find("\n", i)
        if eol < 0:
            return len(text)
        if text[i:eol].strip() == delimiter:
            return eol + 1
        i = eol + 1
    return i


_ANSI_SIMPLE = {"a": "\a", "b": "\b", "e": "\x1b", "E": "\x1b", "f": "\f", "n": "\n",
                "r": "\r", "t": "\t", "v": "\v", "\\": "\\", "'": "'", '"': '"', "?": "?"}


def _ansi_c(text: str, i: int, buf: list[str]) -> int:
    """Decode a bash `$'…'` body starting at text[i] into buf; returns the next index."""
    while i < len(text):
        ch = text[i]
        if ch == "'":
            return i + 1
        if ch != "\\" or i + 1 >= len(text):
            buf.append(ch)
            i += 1
            continue
        esc = text[i + 1]
        if esc in _ANSI_SIMPLE:
            buf.append(_ANSI_SIMPLE[esc])
            i += 2
            continue
        width = {"x": 2, "u": 4, "U": 8}.get(esc)
        if width:
            digits = re.match(r"[0-9a-fA-F]{1,%d}" % width, text[i + 2:])
            if digits and int(digits.group(0), 16) <= 0x10FFFF:
                buf.append(chr(int(digits.group(0), 16)))
                i += 2 + len(digits.group(0))
                continue
        octal = re.match(r"[0-7]{1,3}", text[i + 1:])
        if octal:
            buf.append(chr(int(octal.group(0), 8) & 0xFF))
            i += 1 + len(octal.group(0))
            continue
        if esc == "c" and i + 2 < len(text):
            buf.append(chr(ord(text[i + 2]) & 0x1F))
            i += 3
            continue
        buf.append("\\" + esc)
        i += 2
    return i


def _segments(command: str) -> list[list[str]]:
    """Split `command` into shell segments of tokens, quote- and heredoc-aware.

    Backslash-newline continuations are joined; newline, `;`, `&&`, `||`, `|`,
    `&`, `(` and `)` separate segments; redirections and heredoc bodies are
    dropped. A `$(…)` (or backquote) command substitution stays part of the
    word it appears in — callers resolve such a token as "the current branch"
    when it names a push destination or a `--ref` — and its body is emitted as
    segments of its own just before the enclosing command, because the shell
    runs it first. The rest of the enclosing command is kept (a substitution
    never ends it). `$'…'` (ANSI-C) and `$"…"` (locale) quoting are decoded.
    """
    text = command.replace("\\\r\n", "").replace("\\\n", "")
    segments: list[list[str]] = []
    tokens: list[str] = []
    buf: list[str] = []
    subs: list[list[str]] = []  # substitution bodies, emitted before their command

    quoted_word = [False]  # the current word had quotes, so it exists even if empty

    def flush_token() -> None:
        if buf or quoted_word[0]:
            tokens.append("".join(buf))
            buf.clear()
        quoted_word[0] = False

    def flush_segment() -> None:
        flush_token()
        if subs:
            segments.extend(subs)
            subs.clear()
        if tokens:
            segments.append(list(tokens))
            tokens.clear()

    def substitution(i: int) -> int:
        """Keep the `$(…)`/backquote source at text[i] in the word; queue its body."""
        if text[i] == "`":
            close = text.find("`", i + 1)
            close = len(text) - 1 if close < 0 else close
            body = text[i + 1:close]
        else:
            close = _matching_paren(text, i + 2)
            body = text[i + 2:close]
        buf.append(text[i:close + 1])
        subs.extend(_segments(body))
        return close + 1

    def quoted(i: int) -> int:
        """Scan a quoted region into the token buffer; returns the next index."""
        quoted_word[0] = True
        quote = text[i]
        i += 1
        while i < len(text):
            ch = text[i]
            if ch == quote:
                return i + 1
            if quote == '"' and ((ch == "$" and text[i + 1:i + 2] == "(") or ch == "`"):
                i = substitution(i)
                continue
            if quote == '"' and ch == "\\" and i + 1 < len(text):
                buf.append(text[i + 1])
                i += 2
            else:
                buf.append(ch)
                i += 1
        return i

    def redirection_step(i: int) -> int | None:
        """Consume a redirection at text[i] (or `&>`), or None if there is none."""
        ch = text[i]
        if ch == "&":
            if text[i + 1:i + 2] != ">":
                return None
            flush_token()
            start = i + 1
        elif ch in "<>":
            if buf and "".join(buf).isdigit():
                buf.clear()  # an fd prefix such as the 2 in 2>&1
            else:
                flush_token()
            start = i
        else:
            return None
        end, delimiter = _consume_redirection(text, start)
        if delimiter:
            pending_heredocs.append(delimiter)
        return end

    def separator_step(i: int) -> int | None:
        """Consume a command separator at text[i], or None if there is none."""
        ch = text[i]
        if ch not in "\n;|&()":
            return None
        if ch in "|&" and text[i + 1:i + 2] == ch:
            i += 1  # && or ||
        flush_token()
        flush_segment()
        return i + 1

    i = 0
    pending_heredocs: list[str] = []
    while i < len(text):
        ch = text[i]
        if ch in " \t":
            flush_token()
            i += 1
            continue
        if ch in "\n;":
            flush_token()
            i += 1
            if ch == "\n" and pending_heredocs:
                for delimiter in pending_heredocs:
                    i = _heredoc_end(text, i, delimiter)
                pending_heredocs.clear()
            flush_segment()
            continue
        if ch == "#" and not buf:
            newline = text.find("\n", i)
            i = len(text) if newline < 0 else newline
            continue
        if ch == "$" and text[i + 1:i + 2] == "'":
            quoted_word[0] = True
            i = _ansi_c(text, i + 2, buf)
            continue
        if ch == "$" and text[i + 1:i + 2] == '"':
            i = quoted(i + 1)
            continue
        if (ch == "$" and text[i + 1:i + 2] == "(") or ch == "`":
            i = substitution(i)
            continue
        if ch in "'\"":
            i = quoted(i)
            continue
        step = redirection_step(i)
        if step is None:
            step = separator_step(i)
        if step is not None:
            i = step
            continue
        if ch == "\\":
            buf.append(text[i + 1:i + 2])
            i += 2
        else:
            buf.append(ch)
            i += 1
    flush_segment()
    return segments


# --- command-word parsing -----------------------------------------------------

def _is_assignment(token: str) -> bool:
    return bool(_ASSIGNMENT.match(token))


def _strip_assignments(tokens: list[str]) -> list[str]:
    i = 0
    while i < len(tokens) and _is_assignment(tokens[i]):
        i += 1
    return tokens[i:]


def _override_on_segment(tokens: list[str]) -> bool:
    """Whether the segment carries the override as one of its leading assignments."""
    for token in tokens:
        if not _is_assignment(token):
            break
        if token == OVERRIDE:
            return True
    return False


def _leading_gh_repo(tokens: list[str]) -> str | None:
    """GH_REPO set for the segment by its leading assignments or an `env` prefix."""
    value, i = None, 0
    while i < len(tokens) and _is_assignment(tokens[i]):
        if tokens[i].startswith("GH_REPO="):
            value = tokens[i].split("=", 1)[1] or None
        i += 1
    if i < len(tokens) and os.path.basename(tokens[i]).removesuffix(".exe") == "env":
        for token in tokens[i + 1:]:
            if token.startswith("GH_REPO="):
                value = token.split("=", 1)[1] or None
            elif not (_is_assignment(token) or token.startswith("-")):
                break
    return value


def _shell_script(tokens: list[str]) -> str | None:
    for i, token in enumerate(tokens[1:], 1):
        if token == "-c" or re.fullmatch(r"-[a-zA-Z]*c", token):
            return tokens[i + 1] if i + 1 < len(tokens) else None
    return None


def _after_env(tokens: list[str]) -> list[str]:
    rest = tokens[1:]
    while rest and (_is_assignment(rest[0]) or rest[0].startswith("-")):
        rest = rest[2:] if rest[0] in ("-u", "--unset") and len(rest) > 1 else rest[1:]
    return rest


_WRAPPER_VALUE_LETTERS = {"sudo": "ughpCDrtTU", "time": "fo", "nice": "n", "exec": "a"}


def _after_options(tokens: list[str], value_letters: str) -> list[str]:
    """The words after a wrapper and its options (`sudo -u me`, `time -p`)."""
    rest = tokens[1:]
    while rest and rest[0].startswith("-") and rest[0] != "-":
        option = rest[0]
        if option == "--":
            rest = rest[1:]
            break
        takes_value = (not option.startswith("--") and option[-1] in value_letters) \
            or option in ("--user", "--group", "--host", "--prompt", "--chdir")
        rest = rest[2:] if takes_value and len(rest) > 1 else rest[1:]
    return rest


def _after_timeout(tokens: list[str]) -> list[str]:
    rest = tokens[1:]
    while rest and rest[0].startswith("-"):
        rest = rest[1:]
    return rest[1:] if rest else rest


def _expand(tokens: list[str]) -> list[list[str]]:
    """Strip wrapper words (env/timeout/sudo/if/…) and re-parse `bash -c '…'`."""
    out: list[list[str]] = []
    work = list(tokens)
    while work:
        base = os.path.basename(work[0]).removesuffix(".exe")
        if base in SHELLS:
            script = _shell_script(work)
            if script is None:
                break
            for segment in _segments(script):
                out.extend(_expand(segment))
            return out
        if base == "env":
            work = _after_env(work)
            continue
        if base == "timeout":
            work = _after_timeout(work)
            continue
        if base in WRAPPERS:
            work = _after_options(work, _WRAPPER_VALUE_LETTERS.get(base, ""))
            continue
        break
    if work:
        out.append(work)
    return out


def _join_dir(base: str, target: str) -> str:
    """Resolve a `cd`/`-C` target against the hook's directory.

    `~` is expanded; a target built from a substitution or variable cannot be
    known here, so the directory stays as it was (usually the same checkout)
    rather than becoming a path that does not exist (which would fail open).
    """
    if not target or "$" in target or "`" in target:
        return base
    if target.startswith("~"):
        target = os.path.expanduser(target)
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


def _whole_substitution(word: str) -> bool:
    """Whether `word` is exactly one `$(…)` or backquote substitution."""
    if word.startswith("`"):
        return len(word) > 1 and word.endswith("`") and "`" not in word[1:-1]
    return word.startswith("$(") and _matching_paren(word, 2) == len(word) - 1


def _resolve_specs(specs: list[tuple[str, str | None]], dir_now: str) -> list[tuple[str, str | None]]:
    """Map push specs to concrete (branch, tip-source); unknown ones are skipped.

    A `$(…)`/backquote destination resolves to the current branch of the
    directory the segment runs in; a bare `$VAR` is unknowable, so the push is
    allowed. A None source means no tip message can be read (MCP / update-branch).
    """
    resolved: list[tuple[str, str | None]] = []
    current, have_current = "", False
    for destination, source in specs:
        destination = str(destination).removeprefix("refs/heads/")
        refers_to_current = destination in ("", "HEAD") or _whole_substitution(destination)
        if refers_to_current and not have_current:
            current, have_current = _current_branch(dir_now), True
        branch = current if refers_to_current else destination
        if not branch or "$" in branch or "`" in branch:
            continue  # built from a variable or a partial substitution: unknowable
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


# gh flags that take a value when spaced (`-R x`); cobra's command lookup skips
# these values, so a leaf's flags may stand before the group or leaf word (F30).
_GH_VALUE_FLAGS = frozenset({"-R", "--repo", "-r", "--ref", "-f", "-F", "--field",
                             "--raw-field", "-j", "--job"})
_PFLAG_TRUE = frozenset({"1", "t", "T", "true", "TRUE", "True"})
UNKNOWN = object()  # an input the guard cannot read (`-F key=@-`, an unreadable file; D10)


class _FileInput(str):
    """A typed `-F key=@path` value: gh sends the file's bytes, read at dispatch time."""


def _gh_command(tokens: list[str]) -> tuple[str, str, list[str]] | None:
    """(group, leaf, rest) for a gh segment, the way cobra finds the command.

    Flags (and a spaced flag's value) are not command words wherever they stand;
    the first two words are the group and the leaf, and everything else keeps
    its original order for the leaf's parser. A help request is no command.
    """
    words, rest, i = [], [], 1
    while i < len(tokens):
        token = tokens[i]
        if token == "--":
            rest.extend(tokens[i:])
            break
        if token in ("-h", "--help"):
            return None
        if token.startswith("-") and len(token) > 1:
            rest.append(token)
            if token in _GH_VALUE_FLAGS and i + 1 < len(tokens):
                rest.append(tokens[i + 1])
                i += 1
        elif len(words) < 2:
            words.append(token)
        else:
            rest.append(token)
        i += 1
    if len(words) < 2:
        return None
    return words[0], words[1], rest


def _flag_values(rest: list[str], short: str, long: str) -> list[tuple[int, str]]:
    """(index, value) for every pflag spelling of one flag, in order.

    Spellings: `-X v`, `-Xv`, `-X=v`, `--long v`, `--long=v`.
    """
    found, i = [], 0
    while i < len(rest):
        arg = rest[i]
        if arg == "--":
            break
        if arg in (short, long) and i + 1 < len(rest):
            found.append((i, rest[i + 1]))
            i += 2
            continue
        if arg.startswith(long + "="):
            found.append((i, arg.split("=", 1)[1]))
        elif arg.startswith(short) and len(arg) > len(short) and not arg.startswith("--"):
            found.append((i, arg[len(short):].removeprefix("=")))
        i += 1
    return found


def _repo_of(rest: list[str]) -> str | None:
    """The repository gh uses: the last `-R/--repo` in any spelling (pflag)."""
    values = _flag_values(rest, "-R", "--repo")
    return values[-1][1] if values else None


def _positionals(rest: list[str]) -> list[str]:
    """Non-flag words of `rest`, skipping every spaced flag value."""
    out, i = [], 0
    while i < len(rest):
        arg = rest[i]
        if arg == "--":
            out.extend(rest[i + 1:])
            break
        if arg.startswith("-") and len(arg) > 1:
            i += 2 if arg in _GH_VALUE_FLAGS else 1
            continue
        out.append(arg)
        i += 1
    return out


_FIELD_FLAG = re.compile(r"--(raw-)?field=([^=]+)=(.*)", re.DOTALL)
_JOINED_FIELD = re.compile(r"-([fF])([^=]+)=(.*)", re.DOTALL)
_JOINED_FIELD_EQ = re.compile(r"-([fF])=(.+)", re.DOTALL)
_TYPED_FIELD_FLAGS = ("-F", "--field")


def _dispatch_fields(rest: list[str]) -> dict:
    """Workflow inputs as gh sends them: typed `-F/--field` over raw `-f/--raw-field`.

    gh applies typed fields after raw ones, so a typed value wins for its key
    whatever the argument order (F31); within one kind the last one wins. A
    typed value starting with `@` is read from a file by gh (`@-` is stdin);
    it is kept as a _FileInput and resolved against the segment's directory.
    """
    raw, typed = {}, {}

    def put(kind: str, key: str, value: str) -> None:
        if kind == "typed":
            typed[key] = _FileInput(value[1:]) if value.startswith("@") else value
        else:
            raw[key] = value

    i = 0
    while i < len(rest):
        arg = rest[i]
        if arg == "--":
            break
        following = rest[i + 1] if i + 1 < len(rest) else ""
        if arg in ("-f", "-F", "--field", "--raw-field"):
            if "=" in following:
                key, _, value = following.partition("=")
                put("typed" if arg in _TYPED_FIELD_FLAGS else "raw", key, value)
            i += 2
            continue
        if match := _FIELD_FLAG.fullmatch(arg):
            put("raw" if match.group(1) else "typed", match.group(2), match.group(3))
        elif match := _JOINED_FIELD.fullmatch(arg):
            put("typed" if match.group(1) == "F" else "raw", match.group(2), match.group(3))
        elif match := _JOINED_FIELD_EQ.fullmatch(arg):
            if "=" in match.group(2):
                key, _, value = match.group(2).partition("=")
                put("typed" if match.group(1) == "F" else "raw", key, value)
        i += 1
    return {**raw, **typed}


def _parse_dispatch(tokens: list[str]) -> dict | None:
    """The dispatch a `gh workflow run` segment describes, or None for others.

    Reads flags as pflag does (`-rX`, `-r=X`, `-fK=V`, `-f=K=V`, `--field=K=V`,
    `--raw-field=K=V`, `-F K=V`), finds the command the way cobra does (flags
    may stand before `workflow` or `run`), accepts the workflow selector
    anywhere, and keeps a `--json` dispatch unknown (its inputs cannot be read).
    """
    command = _gh_command(tokens)
    if command is None or command[:2] != ("workflow", "run"):
        return None
    rest = command[2]
    refs = _flag_values(rest, "-r", "--ref")
    selector = next(iter(_positionals(rest)), None)
    if selector is None or not _is_workflow(selector):
        return None
    flags = rest[:rest.index("--")] if "--" in rest else rest
    json_inputs = any(arg == "--json" or arg.split("=", 1)[1] in _PFLAG_TRUE
                      for arg in flags if arg == "--json" or arg.startswith("--json="))
    return {"ref": refs[-1][1] if refs else "", "fields": _dispatch_fields(rest),
            "json": json_inputs, "repo": _repo_of(rest)}


def _parse_rerun(tokens: list[str]) -> tuple[str | None, str | None, str | None] | None:
    """(run id, repo, job id) for `gh run rerun [<run-id>] [--job <job-id>]`."""
    command = _gh_command(tokens)
    if command is None or command[:2] != ("run", "rerun"):
        return None
    rest = command[2]
    run_id = next((t for t in _positionals(rest) if t.isdigit()), None)
    jobs = _flag_values(rest, "-j", "--job")
    job = jobs[-1][1] if jobs and jobs[-1][1].isdigit() else None
    return run_id, _repo_of(rest), job


def _parse_update_branch(tokens: list[str]) -> tuple[str | None, str | None] | None:
    command = _gh_command(tokens)
    if command is None or command[:2] != ("pr", "update-branch"):
        return None
    rest = command[2]
    selector = next(iter(_positionals(rest)), None)  # number, URL or branch
    return selector, _repo_of(rest)


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


def _api_repo(repo: str) -> tuple[list[str], str]:
    """(`--hostname` args, OWNER/REPO) for a `-R` value: [HOST/]OWNER/REPO or a URL."""
    text = re.sub(r"^[a-z+]+://", "", repo.strip())
    text = re.sub(r"^[^@/]+@", "", text)  # ssh user (git@host:owner/repo)
    text = re.sub(r"^([^/:]+):(\d+/)?", r"\1/", text)  # scp host:owner/repo, host:port/
    text = text.removesuffix(".git").strip("/")
    parts = [part for part in text.split("/") if part]
    host = parts[-3] if len(parts) >= 3 else ""
    owner_repo = "/".join(parts[-2:])
    return (["--hostname", host] if host and host != "github.com" else []), owner_repo


def _remote_sha(repo: str | None, ref: str, cwd: str | None) -> str:
    if re.fullmatch(r"[0-9a-f]{40}", ref):
        return ref
    ref = ref.removeprefix("refs/heads/")
    if repo:
        host, owner_repo = _api_repo(repo)
        out = _run(["gh", "api", *host, f"repos/{owner_repo}/commits/{ref}", "--jq", ".sha"],
                   cwd=cwd)
        return out.strip() if out and out.strip() else ""
    out = _run(["git", "ls-remote", "origin", f"refs/heads/{ref}"], cwd=cwd)
    return out.split()[0] if out and out.split() else ""


def _job_run_id(repo: str | None, job: str, cwd: str | None) -> str | None:
    """The run a `gh run rerun --job <id>` belongs to (D11), or None if unknown."""
    host, owner_repo = _api_repo(repo) if repo else ([], "{owner}/{repo}")
    out = _run(["gh", "api", *host, f"repos/{owner_repo}/actions/jobs/{job}",
                "--jq", ".run_id"], cwd=cwd)
    value = (out or "").strip()
    return value if value.isdigit() else None


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
    ref = ref.removeprefix("refs/heads/")
    if _whole_substitution(ref):
        return _current_branch(dir_now).removeprefix("refs/heads/")
    if "$" in ref or "`" in ref:
        return ""
    if ref:
        return ref.removeprefix("refs/heads/")
    return _default_branch(repo, dir_now)


def _input_value(value, dir_now: str):
    """A field value as gh sends it: a `@path` typed field reads the file (F31)."""
    if not isinstance(value, _FileInput):
        return value
    if str(value) in ("", "-"):
        return UNKNOWN  # stdin (or nothing): unknowable before the command runs
    path = _join_dir(dir_now or ".", str(value))
    limit = 1 << 16
    try:
        if not stat.S_ISREG(os.stat(path).st_mode):
            return UNKNOWN  # a FIFO, /dev/stdin or a directory: gh's read, not ours
        with open(path, "rb") as handle:
            data = handle.read(limit + 1)
    except (OSError, ValueError):
        return UNKNOWN
    if len(data) > limit:
        return UNKNOWN
    return data.decode("utf-8", errors="replace")


def _dispatch_reason(parsed: dict, dir_now: str, pushed: list[str]) -> str | None:
    """Refusal for one parsed `gh workflow run` segment, or None to allow it."""
    mode_value = _input_value(parsed["fields"].get("mode"), dir_now)
    cases_value = _input_value(parsed["fields"].get("cases"), dir_now)
    if cases_value is UNKNOWN:
        return None  # gh reads it from a file: the concurrency group is unknowable (D10)
    mode = mode_value if mode_value is UNKNOWN else str(mode_value or DEFAULT_MODE)
    cases = str(cases_value or "")
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
    if not parsed["json"] and (mode is UNKNOWN or mode in ("s2", "s3")) and ref:
        runs = _gh_runs(parsed["repo"], branch=ref, event="workflow_dispatch",
                        cwd=dir_now)
    if diagnostic and mode == "s2":
        reason = S2_CASES_NOTE
    elif runs is not None:
        reason = dispatch_cancel_refusal(ref, runs, diagnostic=diagnostic)
        if reason is None and not diagnostic and mode is not UNKNOWN and ref not in pushed:
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


def _gh_segment(tokens: list[str], state: dict, guarded: bool,
                gh_repo: str | None = None) -> str | None:
    """Refusal for one gh segment; `gh_repo` is GH_REPO in effect for it (F30/D8)."""
    default_repo = gh_repo or state.get("gh_repo")
    dispatch = _parse_dispatch(tokens)
    if dispatch is not None:
        dispatch["repo"] = dispatch["repo"] or default_repo
        return _dispatch_reason(dispatch, state["dir"], state["pushed"]) if guarded else None
    rerun = _parse_rerun(tokens)
    if rerun is not None:
        run_id, repo, job = rerun
        repo = repo or default_repo
        if job:  # gh reruns the job's own run and ignores any run-id argument
            run_id = _job_run_id(repo, job, state["dir"])
        return _rerun_reason(run_id, repo, state["dir"]) if guarded else None
    update = _parse_update_branch(tokens)
    if update is not None:
        repo = update[1] or default_repo
        head = _pr_head_branch(repo, update[0], state["dir"])
        if head:
            state["pushed"].append(head)
        if not guarded or not head:
            return None
        return _push_reason([(head, None)], repo, state["dir"], trust_skip_ci=False)
    return None


def _eval_segment(tokens: list[str], state: dict, self_override: bool,
                  gh_repo: str | None = None) -> str | None:
    head = os.path.basename(tokens[0]).removesuffix(".exe")
    if head == "cd":
        state["dir"] = _join_dir(state["dir"], tokens[1] if len(tokens) > 1 else "")
        return None
    if head == "export":
        if OVERRIDE in tokens[1:]:
            state["export_override"] = True
        for token in tokens[1:]:
            if token.startswith("GH_REPO="):
                state["gh_repo"] = token.split("=", 1)[1] or None
        return None
    if head == "unset" and "GH_REPO" in tokens[1:]:
        state["gh_repo"] = None
        return None
    guarded = not (self_override or state["export_override"])
    if head == "git":
        return _git_segment(tokens, state, guarded)
    if head == "gh":
        return _gh_segment(tokens, state, guarded, gh_repo)
    return None


def refusal_for_command(command: str, cwd: str | None = None) -> str | None:
    """Reason to refuse `command` run from `cwd`, or None when it may run."""
    state = {"dir": (cwd or os.getcwd()).replace("\\", "/"), "pushed": [],
             "mover": False, "export_override": False,
             "gh_repo": os.environ.get("GH_REPO") or None}
    for raw in _segments(command):
        self_override = _override_on_segment(raw)
        gh_repo = _leading_gh_repo(raw)
        for tokens in _expand(_strip_assignments(raw)):
            if tokens:
                reason = _eval_segment(tokens, state, self_override, gh_repo)
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
