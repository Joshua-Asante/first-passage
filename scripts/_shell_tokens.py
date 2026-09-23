"""_shell_tokens.py — the one shell tokenizer the harness guards share.

Moved 2026-09-23 out of `scripts/guard_s2_runs.py` (card 1, D14) so that
`scripts/guard_shell_command.py` (card 2, E1) reads commands with the same
quote-, heredoc- and substitution-aware scanner instead of keeping a second one
(`docs/briefs/handoffs/2026-09-23-harness-guards-hardening.md` §0 read 2).

One scanner, two modes:

  * **default** (``strict=False``) — card 1's frozen behavior, unchanged by the
    move: `guard_s2_runs.py` imports `segments`/`expand` under its old private
    names and its acceptance suite pins the result.
  * **strict** (``strict=True``) — the shell guard's reading, which must not
    lose a word that follows a command substitution and must know when it could
    not read the command at all (E1 falls back to the raw-string regexes then):

      - a ``$(…)``/backquote substitution stays inside its word, and its body's
        segments follow the enclosing segment instead of splitting it (so
        ``git commit -m "$(cat <<'EOF' … EOF)" --no-verify`` keeps its flag);
      - substitutions inside double quotes are found anywhere in the word, and
        the ``$(…)`` matcher skips quoted text and heredoc bodies (an apostrophe
        in a heredoc commit message no longer unbalances it);
      - ``<<<`` is a here-string, not a heredoc; redirection targets and heredoc
        delimiters are read as quoted words; several heredocs on a line are
        skipped in order;
      - an unterminated quote, ``$(`` or backquote raises `ShellSyntaxError`;
      - `expand` strips leading assignments at every level, reads the options of
        ``sudo``, ``env``, ``timeout``, ``nice``, ``xargs``, ``command``,
        ``exec`` and ``time``, drops ``{``/``}``, re-parses ``eval`` arguments and
        ``find -exec``/``-execdir``/``-ok``/``-okdir`` commands, and finds the
        script of ``bash -ec '…'`` (any short cluster holding ``c``).
"""
from __future__ import annotations

import os
import re

WRAPPERS = frozenset({"command", "builtin", "exec", "nohup", "time", "sudo", "!",
                      "if", "then", "elif", "else", "while", "until", "do",
                      "done", "fi"})
SHELLS = frozenset({"bash", "sh", "zsh", "dash", "ksh"})

_ASSIGNMENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*=")
_WORD_END = " \t\n;|&()<>"

# strict-mode wrapper options that take the next word as their value
_SUDO_VALUES = frozenset({"-u", "-g", "-h", "-p", "-C", "-D", "-r", "-t", "-T", "-U",
                          "--user", "--group", "--host", "--prompt", "--close-from",
                          "--chdir", "--role", "--type", "--command-timeout",
                          "--other-user"})
_ENV_VALUES = frozenset({"-u", "--unset", "-C", "--chdir", "-S", "--split-string"})
_TIMEOUT_VALUES = frozenset({"-s", "--signal", "-k", "--kill-after"})
_NICE_VALUES = frozenset({"-n", "--adjustment"})
_XARGS_VALUES = frozenset({"-a", "-d", "-E", "-I", "-L", "-n", "-P", "-s", "--arg-file",
                           "--delimiter", "--max-args", "--max-procs", "--max-chars",
                           "--process-slot-var"})
_TIME_VALUES = frozenset({"-f", "-o", "--format", "--output"})
_EXEC_VALUES = frozenset({"-a"})
_SHELL_VALUES = frozenset({"-o", "+o", "-O", "+O", "--rcfile", "--init-file"})
_FIND_EXEC = frozenset({"-exec", "-execdir", "-ok", "-okdir"})
_STRICT_WRAPPERS = {"sudo": _SUDO_VALUES, "nice": _NICE_VALUES, "xargs": _XARGS_VALUES,
                    "time": _TIME_VALUES, "exec": _EXEC_VALUES, "command": frozenset()}


class ShellSyntaxError(ValueError):
    """A strict read met a command the shell would reject or keep reading."""


# --- scanning helpers ---------------------------------------------------------

def _matching_paren(text: str, start: int) -> int:
    """Index of the ')' matching the '$(' whose body starts at `start`."""
    depth, quote, i = 1, "", start
    while i < len(text):
        ch = text[i]
        if quote:
            if ch == quote:
                quote = ""
        elif ch in "'\"":
            quote = ch
        elif ch == "\\":
            i += 1
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return len(text)


def _quote_end(text: str, i: int) -> int:
    """Index just past the quoted region opening at text[i] (strict; raises if open)."""
    quote = text[i]
    i += 1
    while i < len(text):
        ch = text[i]
        if ch == quote:
            return i + 1
        if quote == '"':
            if ch == "\\":
                i += 2
                continue
            if ch == "$" and text[i + 1:i + 2] == "(":
                i = _strict_close(text, i + 2) + 1
                continue
            if ch == "`":
                i = _backquote_close(text, i + 1) + 1
                continue
        i += 1
    raise ShellSyntaxError(f"unterminated {quote} quote")


def _backquote_close(text: str, start: int) -> int:
    """Index of the backquote closing the one before `start` (strict; raises if open)."""
    i = start
    while i < len(text):
        if text[i] == "\\":
            i += 2
            continue
        if text[i] == "`":
            return i
        i += 1
    raise ShellSyntaxError("unterminated backquote")


def _word_end(text: str, i: int) -> int:
    """Index just past the shell word starting at text[i] (strict; quote-aware)."""
    while i < len(text) and text[i] not in _WORD_END:
        ch = text[i]
        if ch in "'\"":
            i = _quote_end(text, i)
        elif ch == "\\":
            i += 2
        elif ch == "$" and text[i + 1:i + 2] == "(":
            i = _strict_close(text, i + 2) + 1
        elif ch == "`":
            i = _backquote_close(text, i + 1) + 1
        else:
            i += 1
    return min(i, len(text))


def _strict_close(text: str, start: int) -> int:
    """Index of the ')' closing the '$(' whose body starts at `start`.

    Quote-, backquote- and heredoc-aware: a heredoc body inside the substitution
    is skipped whole, so an apostrophe or parenthesis in it cannot unbalance the
    match. Raises `ShellSyntaxError` when the substitution never closes.
    """
    depth, i, pending = 1, start, []
    while i < len(text):
        ch = text[i]
        if ch in "'\"":
            i = _quote_end(text, i)
            continue
        if ch == "\\":
            i += 2
            continue
        if ch == "`":
            i = _backquote_close(text, i + 1) + 1
            continue
        if ch == "#" and (i == start or text[i - 1] in " \t\n;|&("):
            newline = text.find("\n", i)
            i = len(text) if newline < 0 else newline
            continue
        if text.startswith("<<<", i):
            i += 3
            continue
        if text.startswith("<<", i):
            i, delimiter = _consume_redirection(text, i, strict=True)
            if delimiter:
                pending.append(delimiter)
            continue
        if ch == "\n" and pending:
            i += 1
            for delimiter in pending:
                i = _heredoc_end(text, i, delimiter)
            pending.clear()
            continue
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    raise ShellSyntaxError("unterminated $(")


def _consume_redirection(text: str, i: int, *, strict: bool = False) -> tuple[int, str]:
    """Skip the redirection starting at text[i]; a heredoc returns its delimiter."""
    if text[i:i + 2] == "<<" and not (strict and text[i:i + 3] == "<<<"):
        i += 2 + (1 if text[i + 2:i + 3] == "-" else 0)
        while i < len(text) and text[i] in " \t":
            i += 1
        if strict:
            end = _word_end(text, i)
            return end, re.sub(r"[\"'\\]", "", text[i:end])
        word = ""
        while i < len(text) and text[i] not in " \t\n;|&()":
            word += text[i]
            i += 1
        return i, word.strip("'\"")
    i += 1
    while i < len(text) and text[i] in "<>&":
        i += 1
    while i < len(text) and text[i] in " \t":
        i += 1
    if strict:
        return _word_end(text, i), ""
    while i < len(text) and text[i] not in " \t\n;|()&":
        i += 1
    return i, ""


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


# --- the tokenizer ------------------------------------------------------------

def segments(command: str, *, strict: bool = False) -> list[list[str]]:
    """Split `command` into shell segments of tokens, quote- and heredoc-aware.

    Backslash-newline continuations are joined; newline, `;`, `&&`, `||`, `|`,
    `&`, `(` and `)` separate segments; redirections and heredoc bodies are
    dropped. A `$(…)` (or backquote) command substitution leaves its source
    text as one token — callers resolve that token as "the current branch" when
    it names a push destination or a `--ref` — and its body is spliced in as
    segments of its own, because the shell runs it. Strict mode differs as the
    module docstring lists and raises `ShellSyntaxError` on unreadable input.
    """
    text = command.replace("\\\r\n", "").replace("\\\n", "")
    out: list[list[str]] = []
    tokens: list[str] = []
    buf: list[str] = []
    deferred: list[list[str]] = []   # strict: substitution bodies, after their segment
    heredocs: list[str] = []         # delimiters whose bodies start at the next newline

    def flush_token() -> None:
        if buf:
            tokens.append("".join(buf))
            buf.clear()

    def flush_segment() -> None:
        flush_token()
        if tokens:
            out.append(list(tokens))
            tokens.clear()
        out.extend(deferred)
        deferred.clear()

    def substitution(i: int, body: int, close: int) -> int:
        """Record the substitution text[i:close + 1] whose body starts at `body`."""
        buf.append(text[i:close + 1])
        if strict:
            deferred.extend(segments(text[body:close], strict=True))
        else:
            flush_token()
            flush_segment()
            out.extend(segments(text[body:close]))
        return close + 1

    def quoted(i: int) -> int:
        """Scan a quoted region into the token buffer; returns the next index."""
        quote = text[i]
        i += 1
        while i < len(text):
            ch = text[i]
            if ch == quote:
                return i + 1
            if quote == '"' and ch == "$" and text[i + 1:i + 2] == "(" and (strict or not buf):
                if strict:
                    i = substitution(i, i + 2, _strict_close(text, i + 2))
                    continue
                # A substitution standing as the whole quoted word: keep its
                # source as the token and splice its body in as segments.
                i = substitution(i, i + 2, _matching_paren(text, i + 2))
                if text[i:i + 1] == quote:
                    i += 1
                return i
            if strict and quote == '"' and ch == "`":
                i = substitution(i, i + 1, _backquote_close(text, i + 1))
                continue
            if quote == '"' and ch == "\\" and i + 1 < len(text):
                buf.append(text[i + 1])
                i += 2
            else:
                buf.append(ch)
                i += 1
        if strict:
            raise ShellSyntaxError(f"unterminated {quote} quote")
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
        end, delimiter = _consume_redirection(text, start, strict=strict)
        if delimiter:
            if strict:
                heredocs.append(delimiter)
            else:
                heredocs[:] = [delimiter]
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
    while i < len(text):
        ch = text[i]
        if ch in " \t":
            flush_token()
            i += 1
            continue
        if ch in "\n;":
            flush_token()
            i += 1
            if ch == "\n" and heredocs:
                for delimiter in heredocs:
                    i = _heredoc_end(text, i, delimiter)
                heredocs.clear()
            flush_segment()
            continue
        if ch == "#" and not buf:
            newline = text.find("\n", i)
            i = len(text) if newline < 0 else newline
            continue
        if ch == "$" and text[i + 1:i + 2] == "(":
            close = _strict_close(text, i + 2) if strict else _matching_paren(text, i + 2)
            i = substitution(i, i + 2, close)
            continue
        if ch == "`":
            if strict:
                close = _backquote_close(text, i + 1)
            else:
                close = text.find("`", i + 1)
                close = len(text) - 1 if close < 0 else close
            i = substitution(i, i + 1, close)
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
    return out


# --- command words --------------------------------------------------------------

def is_assignment(token: str) -> bool:
    """Whether `token` is a leading `NAME=value` shell assignment."""
    return bool(_ASSIGNMENT.match(token))


def strip_assignments(tokens: list[str]) -> list[str]:
    """`tokens` without its leading `NAME=value` assignments."""
    i = 0
    while i < len(tokens) and is_assignment(tokens[i]):
        i += 1
    return tokens[i:]


def program(word: str, *, strict: bool = False) -> str:
    """The program a command word names: its basename without `.exe`."""
    if strict:
        word = word.replace("\\", "/").rsplit("/", 1)[-1]
    return os.path.basename(word).removesuffix(".exe")


def _shell_script(tokens: list[str], *, strict: bool = False) -> str | None:
    """The script string of `bash -c '…'` (and friends), or None."""
    if not strict:
        for i, token in enumerate(tokens[1:], 1):
            if token == "-c" or re.fullmatch(r"-[a-zA-Z]*c", token):
                return tokens[i + 1] if i + 1 < len(tokens) else None
        return None
    has_c, rest = False, iter(tokens[1:])
    for token in rest:
        if token in _SHELL_VALUES:
            next(rest, None)
        elif token == "--":
            token = next(rest, None)
            return token if has_c else None
        elif token[:1] in "-+" and len(token) > 1:
            has_c |= token[0] == "-" and token[1] != "-" and "c" in token[1:]
        else:
            return token if has_c else None
    return None


def _after_options(tokens: list[str], values: frozenset) -> list[str]:
    """Drop the wrapper word and its options (the named ones consume a value)."""
    rest = tokens[1:]
    while rest and rest[0].startswith("-") and rest[0] != "-":
        if rest[0] == "--":
            return rest[1:]
        rest = rest[2:] if rest[0] in values else rest[1:]
    return rest


def _after_env(tokens: list[str], *, strict: bool = False) -> list[str]:
    """What `env` runs: its words after assignments and options."""
    if strict:
        rest = tokens[1:]
        while rest and (is_assignment(rest[0]) or rest[0].startswith("-")):
            if rest[0] == "--":
                return strip_assignments(rest[1:])
            rest = rest[2:] if rest[0] in _ENV_VALUES else rest[1:]
        return rest
    rest = tokens[1:]
    while rest and (is_assignment(rest[0]) or rest[0].startswith("-")):
        rest = rest[2:] if rest[0] in ("-u", "--unset") and len(rest) > 1 else rest[1:]
    return rest


def _after_timeout(tokens: list[str], *, strict: bool = False) -> list[str]:
    """What `timeout` runs: its words after options and the duration."""
    if strict:
        rest = _after_options(tokens, _TIMEOUT_VALUES)
        return rest[1:]
    rest = tokens[1:]
    while rest and rest[0].startswith("-"):
        rest = rest[1:]
    return rest[1:] if rest else rest


def _find_commands(tokens: list[str]) -> list[list[str]]:
    """The commands `find … -exec cmd … ;` (and -execdir/-ok/-okdir) would run."""
    found, i = [], 0
    while i < len(tokens):
        if tokens[i] in _FIND_EXEC:
            j = i + 1
            while j < len(tokens) and tokens[j] not in (";", "+"):
                j += 1
            found.extend(expand(tokens[i + 1:j], strict=True))
            i = j
        i += 1
    return found


def expand(tokens: list[str], *, strict: bool = False) -> list[list[str]]:
    """Strip wrapper words (env/timeout/sudo/if/…) and re-parse `bash -c '…'`."""
    out: list[list[str]] = []
    work = list(tokens)
    while work:
        if strict:
            work = strip_assignments(work)
            if not work:
                break
        base = program(work[0], strict=strict)
        if base in SHELLS:
            script = _shell_script(work, strict=strict)
            if script is None:
                break
            for segment in segments(script, strict=strict):
                out.extend(expand(segment, strict=strict))
            return out
        if base == "env":
            work = _after_env(work, strict=strict)
            continue
        if base == "timeout":
            work = _after_timeout(work, strict=strict)
            continue
        if strict and base == "command" and any(w in ("-v", "-V") for w in work[1:2]):
            return out  # a lookup, not a run
        if strict and base in _STRICT_WRAPPERS:
            work = _after_options(work, _STRICT_WRAPPERS[base])
            continue
        if strict and base in ("{", "}"):
            work = work[1:]
            continue
        if strict and base == "eval":
            for segment in segments(" ".join(work[1:]), strict=True):
                out.extend(expand(segment, strict=True))
            return out
        if strict and base == "find":
            out.append(work)
            out.extend(_find_commands(work))
            return out
        if base in WRAPPERS:
            work = work[1:]
            continue
        break
    if work:
        out.append(work)
    return out
