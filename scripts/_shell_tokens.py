"""_shell_tokens.py — the shell tokenizer module the harness guards share.

Moved 2026-09-23 out of `scripts/guard_s2_runs.py` (card 1, D14) so that
`scripts/guard_shell_command.py` (card 2, E1) reads commands with the same
module instead of keeping a copy
(`docs/briefs/handoffs/2026-09-23-harness-guards-hardening.md` §0 read 2).

One module, two scanners: `segments(strict=False)` runs `_default_segments`
(card 1's loop, with `matching_paren`, `_consume_redirection`, `_heredoc_end`
and `_skip_word`) and `segments(strict=True)` runs `_strict_segments` (card 2's
loop, with `_strict_close`, `_heredoc_word`, `_redirection_operator_end` and
`_strict_heredoc_end`). They share the ANSI-C decoder and the wrapper option
tables, not their scanning; a fix to one scanner does not reach the other.

  * **default** (``strict=False``) — card 1's reading for `guard_s2_runs.py`, as
    of its #470 review round 3 (`guard_s2_runs.py` imports `segments`,
    `expand` and `matching_paren` under its old private names; card 1's
    acceptance and regression suites pin the result). It never raises
    `ShellSyntaxError`: unterminated input runs to the end of the command.
    (Nesting deeper than Python's recursion limit raises `RecursionError`, as
    card 1's own tokenizer did; `guard_s2_runs` then fails open.)

      - a ``$(…)``/backquote substitution stays inside its word, and its body's
        segments come just before the enclosing segment (the shell runs it
        first); `matching_paren` skips quotes, escapes, comments and heredoc
        bodies, so the ``$(cat <<'EOF' … EOF)`` commit idiom stays balanced;
      - ``<<<`` is a here-string; a heredoc delimiter drops its quotes and
        backslashes, and several heredocs on a line are skipped in order;
      - ``$'…'`` is decoded with bash's ANSI-C escapes (``\\c`` stops at the
        closing quote, as in bash) and ``$"…"`` is read as ``"…"``; an empty
        quoted word is kept as a token, so ``$''#x`` is the word ``#x``;
      - `expand` skips the options of ``sudo``, ``nice``, ``time``, ``exec``,
        ``command`` and ``nohup`` getopt-style with the tables strict mode uses
        (``sudo -u me``, ``time -p``, ``nice -n 5``, ``sudo --``). ``env`` and
        ``timeout`` keep card 1's readers: only ``env -u``/``--unset`` takes a
        value, and ``timeout`` drops every dash word and then the duration, so
        ``timeout -k 5 60 cmd`` and ``env -C dir cmd`` hide ``cmd`` (strict mode
        reads both).
  * **strict** (``strict=True``) — the shell guard's reading, which must not
    lose a word that follows a command substitution and must know when it could
    not read the command at all (E1 falls back to the raw-string regexes then):

      - a ``$(…)``/backquote substitution stays inside its word, and its body's
        segments follow the enclosing segment instead of splitting it (so
        ``git commit -m "$(cat <<'EOF' … EOF)" --no-verify`` keeps its flag);
      - substitutions inside double quotes are found anywhere in the word, and
        the ``$(…)`` matcher skips quoted text and heredoc bodies (an apostrophe
        in a heredoc commit message no longer unbalances it);
      - ``<<<`` is a here-string, not a heredoc; a redirection target (and a
        here-string word) is read as a word and then dropped, so a ``$(…)``,
        backquote or ``<(…)``/``>(…)`` inside it is still re-parsed as the
        commands bash runs (``echo x > "$(cmd)"``); a redirection with no
        target raises; ``<(…)``/``>(…)`` process substitutions are words whose
        bodies are re-parsed;
      - a heredoc delimiter gets bash's quote removal (``"E\\"F"`` is
        ``E"F``; ``'E\\F'`` and ``"E\\F"`` keep the backslash; ``E\\F`` is
        ``EF``), and its body ends only on a line that equals it exactly
        (leading tabs stripped for ``<<-``); an unquoted delimiter's body joins
        backslash-newline pairs before that comparison and a quoted one's does
        not; several heredocs on a line are skipped in order; inside ``$(…)``
        or ``<(…)`` a line that starts with the delimiter and has a ``)`` later
        ends the body there and what follows the delimiter is a new command, as
        bash 5.2 reads ``EOF)"``; inside ``(( … ))`` and
        ``$(( … ))`` arithmetic, ``<<``, ``<`` and ``>`` are operators, never a
        heredoc or redirection;
      - backslash-newline is a line continuation only where bash removes it:
        in an unquoted word and inside double quotes, never inside single
        quotes, a quoted heredoc body or a comment (``# note \\`` ends at its
        newline); a backslash before a carriage return escapes the CR;
      - inside double quotes a backslash escapes only ``$``, a backquote,
        ``"``, ``\\`` and newline, as in bash, so a quoted Windows path such as
        ``"C:\\Program Files\\Git\\cmd\\git.exe"`` keeps its backslashes;
        ``$'…'`` is decoded with bash's ANSI-C escapes and ``$"…"`` is read as
        ``"…"``; a quote starts a word even when it is empty, so ``''#`` is a
        word and not a comment, and an empty quoted word is kept as a token;
      - an unterminated quote, ``$(`` or backquote, and a heredoc whose
        delimiter line never comes, raise `ShellSyntaxError`;
      - `program` splits on backslashes too and casefolds (``GIT.EXE``);
      - `expand` strips leading assignments at every level, reads the options of
        ``sudo``, ``env``, ``timeout``, ``nice``, ``xargs``, ``command``,
        ``exec``, ``nohup`` and ``time`` getopt-style (``sudo -Eu root``,
        ``timeout -vk 5``, ``nohup -- cmd``),
        splits ``env -S '…'`` into the command it runs, drops ``{``/``}`` and
        ``function name``, re-parses ``eval`` arguments and
        ``find -exec``/``-execdir``/``-ok``/``-okdir`` commands, and finds the
        script of ``bash``/``sh`` the way bash reads its options: ``c`` in any
        ``-``/``+`` group, each ``o``/``O`` in a group taking one word
        (``bash -euo pipefail -c '…'``), and ``-`` or ``--`` ending options.
"""
from __future__ import annotations

import os
import re
import shlex

WRAPPERS = frozenset({"command", "builtin", "exec", "nohup", "nice", "time", "sudo", "!",
                      "if", "then", "elif", "else", "while", "until", "do",
                      "done", "fi"})
SHELLS = frozenset({"bash", "sh", "zsh", "dash", "ksh"})

_ASSIGNMENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*=")
_WORD_END = " \t\n;|&()<>"

# Wrapper options that take a value: (short letters, long options).
# Short groups are read getopt-style: the first value letter takes the rest of
# the group, or the next word when it ends the group (`sudo -Eu root`, `-uroot`).
_SUDO_OPTS = ("aCcDghpRrTtUu", frozenset({
    "--auth-type", "--close-from", "--login-class", "--chdir", "--group", "--host",
    "--prompt", "--chroot", "--role", "--type", "--command-timeout", "--other-user",
    "--user"}))
_ENV_OPTS = ("CSu", frozenset({"--chdir", "--split-string", "--unset"}))
_TIMEOUT_OPTS = ("ks", frozenset({"--kill-after", "--signal"}))
_NICE_OPTS = ("n", frozenset({"--adjustment"}))
_XARGS_OPTS = ("adEILnPs", frozenset({
    "--arg-file", "--delimiter", "--max-args", "--max-procs", "--max-chars",
    "--process-slot-var"}))
_TIME_OPTS = ("fo", frozenset({"--format", "--output"}))
_EXEC_OPTS = ("a", frozenset())
# bash/sh long options that take a value; each o/O in a short group (-o, -euo,
# +O) takes one following word as well
_SHELL_LONG_VALUES = frozenset({"--rcfile", "--init-file"})
_FIND_EXEC = frozenset({"-exec", "-execdir", "-ok", "-okdir"})
_WRAPPER_OPTS = {"sudo": _SUDO_OPTS, "nice": _NICE_OPTS, "xargs": _XARGS_OPTS,
                 "time": _TIME_OPTS, "exec": _EXEC_OPTS, "command": ("", frozenset()),
                 "nohup": ("", frozenset())}
# inside double quotes a backslash escapes only these; before anything else it stays
_DQUOTE_ESCAPES = '$`"\\\n'
# bash's ANSI-C ($'…') escapes: single letters, then octal/hex/unicode codes
_ANSI_SIMPLE = {"a": "\a", "b": "\b", "e": "\x1b", "E": "\x1b", "f": "\f", "n": "\n",
                "r": "\r", "t": "\t", "v": "\v", "\\": "\\", "'": "'", '"': '"', "?": "?"}
_ANSI_CODE = re.compile(r"[0-7]{1,3}|x[0-9A-Fa-f]{1,2}|u[0-9A-Fa-f]{1,4}|U[0-9A-Fa-f]{1,8}")


class ShellSyntaxError(ValueError):
    """A strict read met a command the shell would reject or keep reading."""


# --- scanning helpers ---------------------------------------------------------

def matching_paren(text: str, start: int) -> int:
    """Index of the ')' matching the '$(' whose body starts at `start` (default mode).

    Shell-aware, so a quote, `(` or `)` inside a heredoc body, a comment or an
    escaped character does not unbalance the scan (a heredoc in `$(cat <<'EOF'
    … EOF)` is the standard commit-message idiom). Returns len(text) when the
    substitution never closes.
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


def _ansi_end(text: str, i: int) -> int:
    """Index just past the `$'…'` string whose opening quote is text[i] (strict)."""
    i += 1
    while i < len(text):
        if text[i] == "\\":
            i += 2
            continue
        if text[i] == "'":
            return i + 1
        i += 1
    raise ShellSyntaxError("unterminated $' quote")


def _code_point(code: str) -> str:
    """The character an ANSI-C octal (`101`), `x41`, `u0041` or `U00000041` code names."""
    if code[0] in "01234567":
        return chr(int(code, 8) & 0xFF)
    value = int(code[1:], 16)
    return chr(value) if value <= 0x10FFFF else ""


def _ansi_c(body: str) -> str:
    """The value of `$'body'`: bash's ANSI-C escapes decoded, others kept."""
    out: list[str] = []
    i = 0
    while i < len(body):
        ch, nxt = body[i], body[i + 1:i + 2]
        if ch != "\\" or not nxt:
            out.append(ch)
            i += 1
        elif nxt in _ANSI_SIMPLE:
            out.append(_ANSI_SIMPLE[nxt])
            i += 2
        elif nxt == "c" and i + 2 < len(body):
            out.append(chr(ord(body[i + 2]) & 0x1F))  # \cx: control-x
            i += 3
        elif match := _ANSI_CODE.match(body, i + 1):
            out.append(_code_point(match.group()))
            i = match.end()
        else:
            out.append(ch + nxt)
            i += 2
    return "".join(out)


def _word_end(text: str, i: int) -> int:
    """Index just past the shell word starting at text[i] (strict; quote-aware)."""
    while i < len(text) and text[i] not in _WORD_END:
        ch = text[i]
        if ch in "'\"":
            i = _quote_end(text, i)
        elif ch == "\\":
            i += 2
        elif ch == "$" and text[i + 1:i + 2] == "'":
            i = _ansi_end(text, i + 1)
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
    arithmetic = text[start:start + 1] == "("  # $(( … )): `<<` is a shift there
    while i < len(text):
        ch = text[i]
        if ch == "$" and text[i + 1:i + 2] == "'":
            i = _ansi_end(text, i + 1)
            continue
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
        if text.startswith("<<", i) and not arithmetic:
            i, delimiter = _heredoc_word(text, i)
            pending.append(delimiter)
            continue
        if ch == "\n" and pending:
            i += 1
            for delimiter in pending:
                i, cut = _strict_heredoc_end(text, i, delimiter, comsub=True)
                if cut:  # `EOF)`: the `)` at text[i] closes this substitution
                    break
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


def _skip_word(text: str, i: int) -> int:
    """Index after the shell word at text[i] (quotes and escapes honoured; default mode)."""
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
    """Skip the redirection starting at text[i]; a heredoc returns its delimiter.

    Default mode only; strict mode reads redirections with `_heredoc_word` and
    `_redirection_operator_end`.
    """
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
    """Index after the heredoc body that starts at text[i] (default mode only)."""
    while i <= len(text):
        eol = text.find("\n", i)
        if eol < 0:
            return len(text)
        if text[i:eol].strip() == delimiter:
            return eol + 1
        i = eol + 1
    return i


def _ansi_word(text: str, i: int) -> tuple[str, int]:
    """(value, next index) of the `$'…'` whose opening quote is text[i] (default mode).

    An unterminated string runs to the end of the command instead of raising.
    """
    try:
        end = _ansi_end(text, i)
    except ShellSyntaxError:
        return _ansi_c(text[i + 1:]), len(text)
    return _ansi_c(text[i + 1:end - 1]), end


# --- strict heredocs and redirections -------------------------------------------

def _unquote(word: str) -> tuple[str, bool]:
    """(delimiter, quoted): bash's quote removal on a heredoc word, and whether any
    part of it was quoted (a quoted delimiter's body is read literally)."""
    out: list[str] = []
    i, quoted = 0, False
    while i < len(word):
        ch = word[i]
        if ch == "\\" and word[i + 1:i + 2] == "\n":
            i += 2  # a line continuation, not a quote
        elif ch == "\\":
            out.append(word[i + 1:i + 2])
            i, quoted = i + 2, True
        elif ch == "'":
            end = word.find("'", i + 1)
            end = len(word) if end < 0 else end
            out.append(word[i + 1:end])
            i, quoted = end + 1, True
        elif ch == '"':
            i, quoted = i + 1, True
            while i < len(word) and word[i] != '"':
                pair = word[i:i + 2]
                if pair == "\\\n":
                    i += 2
                elif len(pair) == 2 and pair[0] == "\\" and pair[1] in _DQUOTE_ESCAPES:
                    out.append(pair[1])
                    i += 2
                else:
                    out.append(word[i])
                    i += 1
            i += 1
        else:
            out.append(ch)
            i += 1
    return "".join(out), quoted


def _heredoc_word(text: str, i: int) -> tuple[int, tuple[str, bool, bool]]:
    """(index after the word, (delimiter, quoted, strip tabs)) for the `<<` at text[i].

    Strict mode; raises `ShellSyntaxError` when no delimiter word follows.
    """
    dash = text[i + 2:i + 3] == "-"
    i += 3 if dash else 2
    while i < len(text) and text[i] in " \t":
        i += 1
    end = _word_end(text, i)
    if end == i:
        raise ShellSyntaxError("here-document without a delimiter")
    delimiter, quoted = _unquote(text[i:end])
    return end, (delimiter, quoted, dash)


def _redirection_operator_end(text: str, i: int) -> int:
    """Index of the target word after the (non-heredoc) redirection operator at text[i]."""
    i += 1
    while i < len(text) and text[i] in "<>&":
        i += 1
    if text[i - 1] == ">" and text[i:i + 1] == "|":
        i += 1  # >| writes even under noclobber
    while i < len(text) and text[i] in " \t":
        i += 1
    return i


def _continued(text: str, start: int, eol: int) -> bool:
    """Whether the newline at text[eol] is escaped: an odd run of backslashes before it."""
    run = 0
    while eol - run - 1 >= start and text[eol - run - 1] == "\\":
        run += 1
    return run % 2 == 1


def _join_continuations(line: str) -> str:
    """`line` with its backslash-newline pairs removed (an escaped backslash stays)."""
    out: list[str] = []
    i = 0
    while i < len(line):
        if line[i] == "\\" and i + 1 < len(line):
            if line[i + 1] != "\n":
                out.append(line[i:i + 2])
            i += 2
        else:
            out.append(line[i])
            i += 1
    return "".join(out)


def _strict_heredoc_end(text: str, i: int, delimiter: tuple[str, bool, bool], *,
                        comsub: bool = False, closed: bool = False) -> tuple[int, bool]:
    """(index after the heredoc body starting at text[i], whether a `)` cut it short).

    The body ends on the first line equal to the delimiter, as bash compares it:
    exactly, with leading tabs stripped for `<<-`, and — for an unquoted
    delimiter only — after backslash-newline pairs are joined. Inside `$( … )`
    or `<( … )` (`comsub`) a line that starts with the delimiter and has a `)`
    later ends the body after the delimiter, and the returned index is where the
    scan resumes: bash 5.2 reads `EOF)"` so (with a warning), and runs what
    follows the delimiter as a new command. `closed` says `text` is such a
    substitution's body with its closing `)` cut off, so its last line counts
    as cut when it starts with the delimiter. Raises `ShellSyntaxError` when no
    line ends the body: the rest of the command would otherwise be read as data,
    and a `<<` that was not a heredoc at all (a shift in `$[ … ]`) would hide
    every later command.
    """
    word, quoted, dash = delimiter
    while True:
        end = text.find("\n", i)
        while not quoted and end >= 0 and _continued(text, i, end):
            end = text.find("\n", end + 1)
        end = len(text) if end < 0 else end
        line = text[i:end]
        logical = line if quoted else _join_continuations(line)
        if dash:
            logical = logical.lstrip("\t")
        if logical == word:
            return min(end + 1, len(text)), False
        if comsub and logical.startswith(word) and (
                ")" in logical[len(word):] or (closed and end >= len(text))):
            if "\n" in line:
                raise ShellSyntaxError("here-document cut inside a continued line")
            return end - len(logical) + len(word), True
        if end >= len(text):
            raise ShellSyntaxError(f"here-document {word!r} never ends")
        i = end + 1


def _arithmetic_end(text: str, i: int) -> int:
    """Index just past the `))` closing the `((` arithmetic command at text[i], or -1.

    -1 when the region cannot be read; the ordinary scan then decides (and
    raises on its own if the command is unreadable).
    """
    depth = 0
    try:
        while i < len(text):
            ch = text[i]
            if ch == "$" and text[i + 1:i + 2] == "'":
                i = _ansi_end(text, i + 1)
                continue
            if ch in "'\"":
                i = _quote_end(text, i)
                continue
            if ch == "\\":
                i += 2
                continue
            if ch == "$" and text[i + 1:i + 2] == "(":
                i = _strict_close(text, i + 2) + 1
                continue
            if ch == "`":
                i = _backquote_close(text, i + 1) + 1
                continue
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    return i + 1
            i += 1
    except ShellSyntaxError:
        pass
    return -1


# --- the tokenizer ------------------------------------------------------------

def segments(command: str, *, strict: bool = False,
             closed: bool = False) -> list[list[str]]:
    """Split `command` into shell segments of tokens, quote- and heredoc-aware.

    Newline, `;`, `&&`, `||`, `|`, `&`, `(` and `)` separate segments;
    redirections and heredoc bodies are dropped. A `$(…)` (or backquote) command
    substitution leaves its source text inside its word — callers resolve that
    token as "the current branch" when it names a push destination or a `--ref`
    — and its body becomes segments of its own, because the shell runs it: just
    before the enclosing segment in default mode, just after it in strict mode.
    The modes differ as the module docstring lists; strict mode raises
    `ShellSyntaxError` on unreadable input. `closed` (strict) marks `command` as
    the body of a `$(…)` or `<(…)`/`>(…)` whose closing `)` was cut off, for the
    `EOF)` heredoc rule.
    """
    if strict:
        return _strict_segments(command, closed=closed)
    return _default_segments(command)


def _default_segments(command: str) -> list[list[str]]:
    """Default-mode `segments` (card 1, #470 review round 3)."""
    text = command.replace("\\\r\n", "").replace("\\\n", "")
    out: list[list[str]] = []
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
            out.extend(subs)
            subs.clear()
        if tokens:
            out.append(list(tokens))
            tokens.clear()

    def substitution(i: int) -> int:
        """Keep the `$(…)`/backquote source at text[i] in the word; queue its body."""
        if text[i] == "`":
            close = text.find("`", i + 1)
            close = len(text) - 1 if close < 0 else close
            body = text[i + 1:close]
        else:
            close = matching_paren(text, i + 2)
            body = text[i + 2:close]
        buf.append(text[i:close + 1])
        subs.extend(_default_segments(body))
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
            value, i = _ansi_word(text, i + 1)
            buf.append(value)
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
    return out


def _strict_segments(command: str, closed: bool = False) -> list[list[str]]:
    """Strict-mode `segments` (card 2, E1): raises `ShellSyntaxError` when unreadable."""
    text = command
    out: list[list[str]] = []
    tokens: list[str] = []
    buf: list[str] = []
    deferred: list[list[str]] = []   # substitution bodies, after their segment
    heredocs: list[tuple[str, bool, bool]] = []  # bodies start at the next newline
    arithmetic_end = -1              # end of the `(( … ))` command being read
    started = False                  # a quote opened the current word
    target = False                   # the next word is a redirection target

    def flush_token() -> None:
        nonlocal started, target
        if buf or started:
            word = "".join(buf)
            buf.clear()
            started = False
            if target:
                target = False  # a redirection target: its substitutions are deferred
            else:
                tokens.append(word)

    def flush_segment() -> None:
        flush_token()
        if target:
            raise ShellSyntaxError("redirection without a target")
        if tokens:
            out.append(list(tokens))
            tokens.clear()
        out.extend(deferred)
        deferred.clear()

    def substitution(i: int, body: int, close: int) -> int:
        """Record the substitution text[i:close + 1] whose body starts at `body`."""
        buf.append(text[i:close + 1])
        deferred.extend(_strict_segments(text[body:close], closed=text[i] != "`"))
        return close + 1

    def quoted(i: int) -> int:
        """Scan a quoted region into the token buffer; returns the next index."""
        nonlocal started
        quote = text[i]
        started = True  # '' and "" are words (`''#` is not a comment)
        i += 1
        while i < len(text):
            ch = text[i]
            if ch == quote:
                return i + 1
            if quote == '"' and ch == "$" and text[i + 1:i + 2] == "(":
                i = substitution(i, i + 2, _strict_close(text, i + 2))
                continue
            if quote == '"' and ch == "`":
                i = substitution(i, i + 1, _backquote_close(text, i + 1))
                continue
            if quote == '"' and text[i:i + 2] == "\\\n":
                i += 2  # a line continuation inside double quotes is removed
                continue
            if quote == '"' and ch == "\\" and text[i + 1:i + 2] not in _DQUOTE_ESCAPES:
                buf.append(ch)  # "C:\Program Files\Git\cmd\git.exe" keeps its backslashes
                i += 1
            elif quote == '"' and ch == "\\" and i + 1 < len(text):
                buf.append(text[i + 1])
                i += 2
            else:
                buf.append(ch)
                i += 1
        raise ShellSyntaxError(f"unterminated {quote} quote")

    def redirection_step(i: int) -> int | None:
        """Consume a redirection at text[i] (or `&>`), or None if there is none."""
        nonlocal target
        ch = text[i]
        if i < arithmetic_end and ch in "<>":
            flush_token()  # a comparison or shift inside (( … )), never a heredoc
            return i + 1
        if ch == "&":
            if text[i + 1:i + 2] != ">":
                return None
            flush_token()
            start = i + 1
        elif ch in "<>":
            if buf and not started and "".join(buf).isdigit():
                buf.clear()  # an fd prefix such as the 2 in 2>&1
            else:
                flush_token()
            start = i
        else:
            return None
        if text.startswith("<<", start) and not text.startswith("<<<", start):
            end, heredoc = _heredoc_word(text, start)
            heredocs.append(heredoc)
            return end
        # the target is read as the next word, so the commands in its
        # substitutions are recorded, and then dropped (E1)
        target = True
        return _redirection_operator_end(text, start)

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
                    i, cut = _strict_heredoc_end(text, i, delimiter, comsub=closed,
                                                 closed=closed)
                    if cut:  # what follows the delimiter is a new command
                        break
                heredocs.clear()
            flush_segment()
            continue
        if text[i:i + 2] == "\\\n":
            i += 2  # a line continuation: removed before bash reads words
            continue
        if not (buf or started) and i >= arithmetic_end and text.startswith("((", i):
            arithmetic_end = _arithmetic_end(text, i)  # its words still split as usual
        if ch == "#" and not (buf or started):
            newline = text.find("\n", i)
            i = len(text) if newline < 0 else newline
            continue
        if ch == "$" and text[i + 1:i + 2] == "'":
            end = _ansi_end(text, i + 1)
            buf.append(_ansi_c(text[i + 2:end - 1]))
            started, i = True, end
            continue
        if ch == "$" and text[i + 1:i + 2] == '"':
            i += 1  # $"…" is a translated "…"
            continue
        if ch in "<>" and text[i + 1:i + 2] == "(" and i >= arithmetic_end:
            i = substitution(i, i + 2, _strict_close(text, i + 2))  # <(…) / >(…)
            continue
        if ch == "$" and text[i + 1:i + 2] == "(":
            i = substitution(i, i + 2, _strict_close(text, i + 2))
            continue
        if ch == "`":
            i = substitution(i, i + 1, _backquote_close(text, i + 1))
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
    """The program a command word names: its basename without `.exe`.

    Strict mode also splits on backslashes and casefolds, because Windows paths
    and file names are case-insensitive (`GIT.EXE`, `C:\\...\\rm.exe`).
    """
    if strict:
        word = word.replace("\\", "/").rsplit("/", 1)[-1].casefold()
    return os.path.basename(word).removesuffix(".exe")


def _shell_script(tokens: list[str], *, strict: bool = False) -> str | None:
    """The script string of `bash -c '…'` (and friends), or None."""
    if not strict:
        for i, token in enumerate(tokens[1:], 1):
            if token == "-c" or re.fullmatch(r"-[a-zA-Z]*c", token):
                return tokens[i + 1] if i + 1 < len(tokens) else None
        return None
    # bash reads every letter of a `-`/`+` group: `c` (either sign) means the first
    # operand is the script, and each `o`/`O` takes one following word as its
    # value (`-euo pipefail`, `-oO pipefail extglob`); `-` alone ends options
    has_c, rest = False, iter(tokens[1:])
    for token in rest:
        if token in ("--", "-"):
            token = next(rest, None)
            return token if has_c else None
        if token in _SHELL_LONG_VALUES:
            next(rest, None)
        elif token.startswith("--"):
            continue
        elif token[:1] in "-+" and len(token) > 1:
            has_c |= "c" in token[1:]
            for _ in range(sum(letter in "oO" for letter in token[1:])):
                next(rest, None)
        else:
            return token if has_c else None
    return None


def _takes_next(word: str, spec: tuple[str, frozenset]) -> bool:
    """Whether the option word `word` takes the next word as its value (getopt-style).

    `spec` is (short letters, long options) that take a value. In a short group
    the first value letter takes the rest of the group, or the next word when
    it ends the group: `-Eu root` and `-u root` take `root`, `-uroot` does not.
    """
    letters, longs = spec
    if word.startswith("--"):
        return word in longs
    for pos, letter in enumerate(word[1:], 1):
        if letter in letters:
            return pos == len(word) - 1
    return False


def _after_options(tokens: list[str], spec: tuple[str, frozenset]) -> list[str]:
    """Drop the wrapper word and its options (those in `spec` consume a value)."""
    rest = tokens[1:]
    while rest and rest[0].startswith("-") and rest[0] != "-":
        if rest[0] == "--":
            return rest[1:]
        rest = rest[2:] if _takes_next(rest[0], spec) else rest[1:]
    return rest


def _env_split_string(rest: list[str]) -> tuple[list[str], int] | None:
    """(words, words used) when rest[0] is `env -S`/`--split-string`, else None.

    `env -S 'git reset …'` splits its value into the words it then runs, so the
    split words go back in front of the remaining arguments.
    """
    word, value = rest[0], None
    if word.startswith("--"):
        name, equals, joined = word.partition("=")
        if name != "--split-string":
            return None
        value = joined if equals else None
    else:
        letter = next((c for c in word[1:] if c in _ENV_OPTS[0]), "")
        if letter != "S":
            return None
        value = word[word.index("S") + 1:] or None
    used = 1
    if value is None:
        if len(rest) < 2:
            return [], 1
        value, used = rest[1], 2
    try:
        return shlex.split(value), used
    except ValueError as error:
        raise ShellSyntaxError(f"env -S: {error}") from error


def _after_env(tokens: list[str], *, strict: bool = False) -> list[str]:
    """What `env` runs: its words after assignments and options."""
    if strict:
        rest = tokens[1:]
        while rest and (is_assignment(rest[0]) or rest[0].startswith("-")):
            if rest[0] == "--":
                return strip_assignments(rest[1:])
            split = _env_split_string(rest) if not is_assignment(rest[0]) else None
            if split is not None:
                words, used = split
                rest = words + rest[used:]
            else:
                rest = rest[2:] if _takes_next(rest[0], _ENV_OPTS) else rest[1:]
        return rest
    rest = tokens[1:]
    while rest and (is_assignment(rest[0]) or rest[0].startswith("-")):
        rest = rest[2:] if rest[0] in ("-u", "--unset") and len(rest) > 1 else rest[1:]
    return rest


def _after_timeout(tokens: list[str], *, strict: bool = False) -> list[str]:
    """What `timeout` runs: its words after options and the duration."""
    if strict:
        rest = _after_options(tokens, _TIMEOUT_OPTS)
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
        if strict and base in _WRAPPER_OPTS:
            work = _after_options(work, _WRAPPER_OPTS[base])
            continue
        if strict and base in ("{", "}"):
            work = work[1:]
            continue
        if strict and base == "function":
            work = work[2:]  # `function name { body; }`: the body follows the name
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
            if strict:
                work = work[1:]
            else:
                work = _after_options(work, _WRAPPER_OPTS.get(base, ("", frozenset())))
            continue
        break
    if work:
        out.append(work)
    return out
