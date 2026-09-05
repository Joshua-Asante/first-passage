#!/usr/bin/env python3
"""private_content_scan.py — pre-push scan of a commit range for private bytes.

Needles are built IN MEMORY from the private files this script is pointed at
and are never written anywhere; nothing on disk is touched. The scan reports
matches by LOCATION (class, commit, file, line) — never a matched token. A
reported PATH is itself redacted where a needle matched it (a private value can
appear in a FILENAME) and carries a short digest of the true path instead, so
the location survives for local remediation while the scanner's own output —
which the worker pastes into the PR body — stays publishable.

What each commit is compared against: EVERY parent. A merge's own contribution
starts as the set of PATHS that differ from ALL parents — its conflict
resolution — so a merge of ``origin/main`` is audited without re-reporting
everything ``main`` brought in (which would otherwise stop the packet on the
repository's own tracked images). BINARY evidence for those paths is UNIONed
across parents (a path can be binary in one parent and text in another). TEXT
evidence is NOT the union of every added line on those paths: when main and the
packet branch edit different hunks of the same file, the merged file differs
from both parents, and unioning would report a needle that landed solely from
``main``. Added lines are kept only when they appear against every parent that
has a text view of the path; a parent against which the path is binary is
skipped for that intersection so a binary/text resolution cannot lose its text
hit. An ordinary one-parent commit is simply its diff against that parent.

Git runs with ``core.quotePath=false`` and path lists are read NUL-delimited,
so a non-ASCII filename cannot slip past a prefix or suffix test.

Needle classes (campaign-state §47b step 6b, 2026-09-04):
  TITLE  every key of the JSON object at --json-key (default ``inputs``)
  PAIR   every (key, value) of that object in four serializations:
         ``"k": v`` · ``"k":v`` · ``k: v`` · ``k=v``
  VALUE  every value of that object that is distinctive — a string of at
         least four characters, or a number with a decimal point or at least
         four digits (trivial scalars are covered by TITLE/PAIR and by the
         worker's provenance self-read; a bare ``true`` would match every file)
  CELL   every cell of every data row (header skipped) of each --csv file
         that carries a decimal point or a date
Tokens listed in --exclude files (one per line) are dropped from every class.
Those classes are matched against added lines, commit messages, AND the paths
a commit introduces — a private title or value in a FILENAME is published
exactly like one in a blob, and is reported as class NAME.

Two further classes need no needles: PATH (a tree path under a --path-prefix
in ANY commit of the range, or a path with a --forbid-suffix INTRODUCED by a
commit — added, copied, or renamed to) and BINARY (a file a commit adds or
modifies as binary — a screenshot or a zipped export cannot be text-scanned,
so it fails closed; deletions are not flagged).

Exit codes: 0 clean · 2 hits · 3 needles could not be built (a missing or
unreadable private file, or an empty class for one of them — the scan never
runs "empty") · 4 git failure. Only 0 is a pass.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
_DECIMAL = re.compile(r"\d\.\d")
_HUNK = re.compile(r"@@ -\d+(?:,\d+)? \+(\d+)")
_EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
# The scan must read the objects the PUSH will carry, under a patch format it can
# parse -- neither of which is a property of the machine it runs on.
#   --no-replace-objects: a refs/replace/<commit> entry redirects every read to a
#     substitute object that is NOT pushed, so a replaced commit was scanned in
#     place of the one being published and the scan reported CLEAN.
#   diff.noprefix / mnemonicPrefix / srcPrefix / dstPrefix: the a/ and b/ patch
#     prefixes are stripped when a header path is decoded, so a repository
#     configured to omit or rename them corrupted every path that itself begins
#     with the prefix text, and the merge filter then dropped its hits.
#   diff.external / GIT_EXTERNAL_DIFF / an attribute textconv: each replaces
#     the patch text wholesale, which empties every text class at once. These
#     cannot be pinned by ``-c`` (an empty ``diff.external`` makes git exit 128),
#     so the diff call sites pass ``--no-ext-diff``/``--no-textconv`` and
#     ``_git_env`` drops the environment variable. A regression test asserts the
#     flags are present, because this comment once claimed them before the code
#     did.
_GIT_PINS = (
    "-c", "core.quotePath=false",
    "-c", "diff.noprefix=false",
    "-c", "diff.mnemonicPrefix=false",
    "-c", "diff.srcPrefix=a/",
    "-c", "diff.dstPrefix=b/",
)
# Text-safe armourings of binary content. A screenshot carried as any of these is
# NUL-free, so a NUL test alone is not a fail-closed binary check.
# Each alternative requires a real PAYLOAD, not just the marker: a file that
# merely mentions a data URI -- this module's own tests do -- is not an armoured
# binary, and a control that fires on every such mention is one nobody can run.
_ARMOURED = re.compile(
    rb"data:[\w.+-]+/[\w.+-]+;base64,[A-Za-z0-9+/]{256,}"
    rb"|\"image/(?:png|jpe?g|gif|bmp|webp|svg\+xml)\"\s*:\s*\"[A-Za-z0-9+/]{256,}"
    rb"|[A-Za-z0-9+/]{512,}={0,2}"
)
# A contiguous run is not enough: base64 is conventionally WRAPPED at 64 or 76
# columns, which breaks every long run while leaving the payload intact. Density
# over the whole blob catches the wrapped form -- a body that is overwhelmingly
# base64 alphabet across many long lines is an armoured binary whatever its
# newlines.
_B64_LINE = re.compile(rb"^[A-Za-z0-9+/]{40,}={0,2}$")
_GROUPED = re.compile(r"^[+-]?\d{4,}(?:\.\d+)?$")
_UESC = re.compile(r"\\u([0-9a-fA-F]{4})", re.IGNORECASE)
# Git C-quotes patch-header paths that contain tab/newline/quote/backslash even
# when core.quotePath=false; name-status -z does not. Octal escapes cover the rest.
_SIMPLE_ESC = {"n": "\n", "t": "\t", "r": "\r", "a": "\a", "b": "\b", "f": "\f", "v": "\v", '"': '"', "\\": "\\"}
_OCTAL_ESC = re.compile(r"\\([0-7]{1,3})")
# Raw JSON value lexeme after a key — preserves non-canonical number spellings
# (1.2500, 1e-2) that json.loads/dumps would collapse.
_KEY_VALUE_LEX = re.compile(
    r'(?P<key>"(?:[^"\\]|\\.)*")\s*:\s*'
    r'(?P<val>true|false|null|"(?:[^"\\]|\\.)*"|'
    r"-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?)"
)


class NeedleError(RuntimeError):
    """Raised when a needle class cannot be built; the scan must not run."""


def _git(args: list[str], cwd: Path) -> str:
    # Captured as BYTES and decoded here, deliberately. ``text=True`` enables
    # universal-newline translation, which rewrites every CR in git's output:
    # one inside a NUL-delimited path mangles the name, and one inside an added
    # line splits the record so everything after it lands in a fragment carrying
    # no "+" column and is never scanned. ``errors="replace"`` additionally
    # destroys a filename byte that is not valid UTF-8; ``surrogateescape`` makes
    # it round-trip, since subprocess encodes POSIX argv with the same handler.
    proc = _git_raw(args, cwd)
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args[:2])} failed with status {proc.returncode}")
    return proc.stdout.decode("utf-8", "surrogateescape")


def _git_env() -> dict[str, str]:
    """The caller's environment minus the levers that rewrite diff output.

    ``GIT_EXTERNAL_DIFF`` is inherited from whoever runs the scanner, so a
    difftastic or delta user's shell could silence every text class without any
    repository configuration at all.
    """
    return {
        key: value
        for key, value in os.environ.items()
        if key not in {"GIT_EXTERNAL_DIFF", "GIT_TEXTCONV_CACHE"}
    }


def _git_raw(args: list[str], cwd: Path) -> subprocess.CompletedProcess[bytes]:
    """One pinned git invocation, output left as bytes.

    Every git call in this module goes through here, so a new call site cannot
    quietly miss ``--no-replace-objects`` or the format pins.
    """
    return subprocess.run(
        ["git", "--no-replace-objects", *_GIT_PINS, *args],
        cwd=cwd,
        capture_output=True,
        env=_git_env(),
    )


def _z_fields(out: str) -> list[str]:
    fields = out.split("\0")
    if fields and fields[-1] == "":
        fields.pop()
    return fields


def _parents(commit: str, cwd: Path) -> list[str]:
    """Every parent of the commit; git's empty tree for a root commit."""
    tokens = _git(["rev-list", "--parents", "-n", "1", commit], cwd).split()
    return tokens[1:] or [_EMPTY_TREE]



def _unquote_path(header_path: str) -> str:
    """Decode a git-diff ``+++``/``---`` path to the raw tree path.

    Patch headers C-quote paths containing tab, newline, quote, or backslash
    even when ``core.quotePath=false``; NUL-delimited name-status does not.
    Without decoding, a merge filter comparing header paths to resolved paths
    silently drops every hit on such a file.
    """
    decoded = header_path
    if len(decoded) >= 2 and decoded[0] == '"' and decoded[-1] == '"':
        inner = decoded[1:-1]
        out: list[str] = []
        i = 0
        while i < len(inner):
            if inner[i] == "\\" and i + 1 < len(inner):
                nxt = inner[i + 1]
                if nxt in _SIMPLE_ESC:
                    out.append(_SIMPLE_ESC[nxt])
                    i += 2
                    continue
                octal = _OCTAL_ESC.match(inner, i)
                if octal:
                    out.append(chr(int(octal.group(1), 8)))
                    i = octal.end()
                    continue
                out.append(nxt)
                i += 2
            else:
                out.append(inner[i])
                i += 1
        decoded = "".join(out)
    if decoded.startswith(("a/", "b/")):
        decoded = decoded[2:]
    return decoded


# --------------------------------------------------------------------------- needles


def _value_forms(value: object, *, raw_lexemes: set[str] | None = None) -> set[str]:
    forms = {json.dumps(value)}
    if isinstance(value, str):
        forms.add(value)
    if raw_lexemes:
        forms.update(raw_lexemes)
    return forms


def _alt_encodings(text: str) -> set[str]:
    """The same characters as a NON-UTF-8 file's bytes would decode to.

    Git output is decoded with ``surrogateescape``, so a file saved in cp1252 or
    latin-1 yields lone surrogates where the non-ASCII bytes were, and a UTF-8
    needle can never match it. Each needle carrying non-ASCII therefore also
    contributes its surrogate-escaped byte view.
    """
    if text.isascii():
        return set()
    out: set[str] = set()
    for codec in ("cp1252", "latin-1"):
        try:
            raw = text.encode(codec)
        except (UnicodeEncodeError, LookupError):
            continue
        out.add(raw.decode("utf-8", "surrogateescape"))
    return {form for form in out if form != text}


def _percent_encoded(text: str) -> set[str]:
    """A URL- or JSON-escaped copy of a private string is the same disclosure."""
    if not text or text.isalnum():
        return set()
    try:
        forms = {quote(text, safe=""), quote(text, safe="/")}
    except UnicodeEncodeError:
        # A surrogate-escaped byte cannot be percent-encoded; the byte view is
        # already carried as its own needle form by ``_alt_encodings``.
        return set()
    return {form for form in forms if form != text}


def _numeric_spellings(text: str) -> set[str]:
    """Comma-grouped spellings of a bare number.

    A fixed-string needle over the digits alone cannot match ``102,500.00``: the
    separator breaks the run. The grouped form is generated so the common
    spreadsheet and report rendering of the same figure is covered.
    """
    if not _GROUPED.match(text):
        return set()
    sign = ""
    body = text
    if body[0] in "+-":
        sign, body = body[0], body[1:]
    whole, _, frac = body.partition(".")
    grouped = f"{int(whole):,}"
    out = {f"{sign}{grouped}"}
    if frac:
        out.add(f"{sign}{grouped}.{frac}")
    # A currency symbol in front of the same figure is the same figure.
    for form in list(out):
        out.add(f"${form}")
    return out


def _distinctive(value: object) -> bool:
    """Is this value specific enough to be a needle on its own?

    Trivial scalars are covered by TITLE and PAIR and by the worker's provenance
    self-read; a bare ``true`` would match every file.
    """
    if isinstance(value, bool) or value is None:
        return False
    if isinstance(value, str):
        text = value.strip()
        if len(text) < 4:
            return False
        digits = sum(character.isdigit() for character in text)
        if digits >= 4 or "." in text or "-" in text or "_" in text:
            return True
        return not text.isalpha() or len(text) >= 6
    if isinstance(value, (int, float)):
        text = str(value)
        return "." in text or "e" in text.lower() or sum(c.isdigit() for c in text) >= 4
    return False


def _raw_lexemes_by_key(raw: str) -> dict[str, set[str]]:
    """Map each JSON key to the value lexemes spelled in the source text.

    ``json.loads`` collapses ``1.2500`` to ``1.25``; a worker who copied the
    chart's spelling would then miss the VALUE needle. Keep every source
    lexeme so the scan is independent of canonicalization.
    """
    out: dict[str, set[str]] = {}
    for match in _KEY_VALUE_LEX.finditer(raw):
        key = json.loads(match.group("key"))
        if not isinstance(key, str):
            continue
        out.setdefault(key, set()).add(match.group("val"))
    return out


def build_json_needles(path: Path, json_key: str) -> dict[str, set[str]]:
    """TITLE/PAIR/VALUE needles from EVERY leaf of the object at ``json_key``.

    The walk is recursive. Reading only the first level meant a value nested one
    step below -- a grouped override map, a per-source section, any snapshot
    whose shape is not perfectly flat -- produced no needle at all, and the scan
    reported CLEAN with no indication of what it had skipped.
    """
    try:
        raw = path.read_text(encoding="utf-8")
        payload = json.loads(raw)
    except (OSError, ValueError) as exc:
        raise NeedleError(f"cannot read JSON needle source: {path.name}") from exc
    obj = payload.get(json_key) if isinstance(payload, dict) else None
    if not isinstance(obj, dict) or not obj:
        raise NeedleError(f"{path.name}: no non-empty object at key {json_key!r}")
    lexemes = _raw_lexemes_by_key(raw)
    title: set[str] = set()
    pair: set[str] = set()
    value_needles: set[str] = set()
    weak: set[str] = set()
    dropped: set[str] = set()

    def visit(node: object, key: str | None) -> None:
        if isinstance(node, dict):
            for inner_key, inner in node.items():
                inner_key = str(inner_key)
                if inner_key:
                    title.add(inner_key)
                visit(inner, inner_key or None)
            return
        if isinstance(node, list):
            for item in node:
                visit(item, key)
            return
        if key is None:
            return
        # BOTH numeric and quoted lexemes. Dropping quoted ones as "duplicating
        # the parsed form" was wrong: a JSON string may spell a character with an
        # optional escape, and ``json.dumps`` never recreates it, so the source
        # spelling is the only needle that matches a copy of the source.
        raw_forms: set[str] = set()
        for lex in lexemes.get(key, ()):
            if lex in {"true", "false", "null"}:
                continue
            raw_forms.add(lex)
            if lex.startswith('"') and lex.endswith('"') and len(lex) >= 2:
                raw_forms.add(lex[1:-1])
        forms = _value_forms(node, raw_lexemes=raw_forms or None)
        for form in forms:
            pair.update({f'"{key}": {form}', f'"{key}":{form}', f"{key}: {form}", f"{key}={form}"})
        if _distinctive(node):
            value_needles.update(forms)
            for form in list(forms):
                bare = form.strip('"')
                value_needles.update(_numeric_spellings(bare))
                value_needles.update(_alt_encodings(bare))
                value_needles.update(_percent_encoded(bare))
        elif isinstance(node, str) and len(node.strip()) >= 3:
            # Not a needle -- too short or too plain to match without flooding
            # ordinary prose -- but still a private token, so it is carried for
            # REDACTION only and the key is reported so the drop is not silent.
            weak.add(node.strip())
            dropped.add(key)

    visit(obj, None)
    return {
        "TITLE": title,
        "PAIR": pair,
        "VALUE": value_needles,
        "_WEAK": weak,
        "_DROPPED_KEYS": dropped,
    }


def build_csv_needles(path: Path) -> tuple[set[str], set[str]]:
    """Every distinctive cell of a private/vendor CSV, header row included.

    The header row is a cell like any other -- an account identifier published as
    a COLUMN NAME is the same disclosure as one in a row -- and distinctiveness
    is the same test the JSON side uses rather than "has a decimal point or an
    ISO date". That older rule had no pattern for the two classes the threat
    model actually names: an identifier (no decimal, no date) and a whole-dollar
    figure. Numeric cells additionally contribute a comma-grouped spelling, since
    a thousands separator breaks a fixed-string match on the digits alone.
    """
    cells: set[str] = set()
    weak: set[str] = set()
    try:
        # surrogateescape, not replace: a cp1252 or latin-1 export's non-UTF-8
        # bytes must SURVIVE into the needle, because git's output is decoded the
        # same way. Under "replace" the source held U+FFFD while the haystack
        # held surrogates, and an exact byte-for-byte copy matched nothing.
        text = path.read_bytes().decode("utf-8", "surrogateescape")
        rows = list(csv.reader(io.StringIO(text, newline="")))
    except OSError as exc:
        raise NeedleError(f"{path.name}: {exc}") from exc
    for row in rows:
        for cell in row:
            text = cell.strip()
            if not _distinctive(text):
                if len(text) >= 3:
                    weak.add(text)
                continue
            cells.add(text)
            cells.update(_numeric_spellings(text))
            cells.update(_alt_encodings(text))
            cells.update(_percent_encoded(text))
    if not cells:
        raise NeedleError(f"{path.name}: no distinctive cells")
    return cells, weak


def compile_classes(classes: dict[str, set[str]]) -> dict[str, re.Pattern[str]]:
    compiled = {}
    for name, needles in classes.items():
        ordered = sorted(needles, key=len, reverse=True)
        # SUBSTRING, not word-bounded. A boundary that counted "_" and digits as
        # word characters made every needle invisible the moment it was glued
        # into a longer identifier, filename or commit message -- and made the
        # report print such a path VERBATIM, because ``_redact`` uses the same
        # patterns. A disclosure control fails closed: a coincidental hit is
        # adjudicated under the step 6b rule, a missed one is published.
        # IGNORECASE, for the same fail-closed reason as the substring choice and
        # to match the path tests: a lowercased or differently-cased copy of a
        # private tag is the same disclosure, and the NAME class must not be
        # stricter than the suffix and prefix tests applied to the same path.
        # Each needle also contributes its case-folded form, because matching is
        # done against the folded haystack too (see ``_matches``).
        widened = set(ordered) | {n.casefold() for n in ordered}
        parts = sorted(widened, key=len, reverse=True)
        compiled[name] = re.compile("(?:" + "|".join(re.escape(n) for n in parts) + ")", re.IGNORECASE)
    return compiled


# ------------------------------------------------------------------- per-parent reads


def _matches(pattern: re.Pattern[str], text: str) -> bool:
    """Match on the raw text and on its case-folded view.

    ``re.IGNORECASE`` is simple case mapping: it does not equate the German
    sharp s with ``SS``, nor any other expanding fold. Needles carry their
    case-folded form, so folding the haystack too closes the pair.
    """
    views = [text]
    folded = text.casefold()
    if folded != text:
        views.append(folded)
    # A JSON string may spell any character with an optional \uXXXX escape, and
    # ``json.dumps`` never recreates one, so the escaped copy matches no needle.
    # Enumerating escaped needle forms is combinatorial; decoding the HAYSTACK is
    # not, so the unescaped view is searched too.
    if "\\u" in text or "\\U" in text:
        unescaped = _UESC.sub(lambda m: chr(int(m.group(1), 16)), text)
        if unescaped != text:
            views.append(unescaped)
            if unescaped.casefold() != unescaped:
                views.append(unescaped.casefold())
    return any(pattern.search(view) for view in views)


def _flush(
    hits: set[tuple[str, str, int, str]],
    block: list[str],
    start: int,
    current_file: str,
    patterns: dict[str, re.Pattern[str]],
) -> None:
    """Scan a run of consecutive added lines as one string."""
    if len(block) < 2:
        return
    joined = "\n".join(block)
    for name, pattern in patterns.items():
        if _matches(pattern, joined):
            hits.add((name, current_file, start, joined))


def _content_vs(
    base: str, commit: str, cwd: Path, patterns: dict[str, re.Pattern[str]]
) -> set[tuple[str, str, int, str]]:
    """(class, file, new-line, text) for ADDED lines matching a needle vs base.

    The ``+++`` file header is recognised by parser STATE, not by its prefix: an
    added line whose own text starts with ``++ `` renders as ``+++ `` inside a
    hunk and must be scanned, not consumed as a header. Header paths are passed
    through ``_unquote_path`` so a C-quoted tab/newline name still matches the
    raw path returned by NUL-delimited name-status.
    """
    hits: set[tuple[str, str, int, str]] = set()
    current_file = "<unknown>"
    new_line = 0
    in_hunk = False
    # A private value can legally contain a newline -- a quoted CSV cell does --
    # so its needle spans lines and no single added record can match it. Runs of
    # consecutive added lines are therefore scanned as a BLOCK as well.
    block: list[str] = []
    block_start = 0
    # split on "\n" ONLY: git delimits patch records with LF, while str.splitlines()
    # also breaks on \v, \f, \r, \x1c-\x1e, \x85, \u2028 and \u2029 — a needle after such a
    # byte would land in a fragment with no "+" marker and never be scanned.
    for raw in _git(["diff", "--no-ext-diff", "--no-textconv", "--no-color", base, commit], cwd).split("\n"):
        if raw.startswith("diff --git "):
            in_hunk = False
            current_file = "<unknown>"
            continue
        if raw.startswith("@@"):
            in_hunk = True
            match = _HUNK.match(raw)
            new_line = int(match.group(1)) - 1 if match else 0
            continue
        if not in_hunk:
            if raw.startswith("+++ "):
                current_file = _unquote_path(raw[4:])
            continue
        if raw.startswith("+"):
            new_line += 1
            line_text = raw[1:]
            if not block:
                block_start = new_line
            block.append(line_text)
            for name, pattern in patterns.items():
                if _matches(pattern, line_text):
                    hits.add((name, current_file, new_line, line_text))
        elif raw.startswith(" "):
            new_line += 1
            _flush(hits, block, block_start, current_file, patterns)
            block = []
        else:
            _flush(hits, block, block_start, current_file, patterns)
            block = []
    _flush(hits, block, block_start, current_file, patterns)
    return hits

def _introduced_vs(base: str, commit: str, cwd: Path) -> set[str]:
    """Destination paths the commit introduces vs base: added, copied, or RENAMED-to.

    ``--diff-filter=A`` alone misses a rename to a forbidden suffix, which git
    classifies ``R``.
    """
    fields = _z_fields(
        _git(
            ["diff", "--find-renames", "--find-copies", "--name-status", "-z", "--diff-filter=ACR", base, commit],
            cwd,
        )
    )
    paths: set[str] = set()
    index = 0
    while index < len(fields):
        status = fields[index]
        if status.startswith(("R", "C")):
            if index + 2 < len(fields):
                paths.add(fields[index + 2])
            index += 3
        else:
            if index + 1 < len(fields):
                paths.add(fields[index + 1])
            index += 2
    return paths


def _blob_is_opaque(commit: str, path: str, cwd: Path) -> bool:
    """Decide binaryness from the BLOB'S OWN BYTES, never from git's rendering.

    ``numstat`` reports "-\t-" only for what git *renders* as binary, and that
    verdict is driven by attributes -- a ``.gitattributes`` ``diff`` override in
    the tree, an untracked one in the worktree, or ``.git/info/attributes`` --
    none of which travels with the push. A screenshot could therefore be
    reclassified as text and scanned as if it were readable. Reading the blob
    removes that lever: a NUL byte in the first 8 KiB means the content cannot be
    text-scanned, and a git-lfs pointer means the real bytes are published to the
    LFS remote by the very push this is gating.
    """
    try:
        raw = _git_raw(["cat-file", "blob", f"{commit}:{path}"], cwd)
    except OSError:
        return True
    if raw.returncode != 0:
        return True
    body = raw.stdout
    if b"\0" in body:
        return True
    if body.startswith(b"version https://git-lfs.github.com/spec/v1"):
        return True
    # ARMOURED binary is still binary. A NUL test only recognises one ENCODING of
    # content that cannot be text-scanned; every text-safe armouring of the same
    # screenshot is NUL-free -- a base64 data: URI, a notebook's "image/png"
    # output cell, an SVG with an embedded image, a long unbroken base64 run --
    # and the fixed-string needles cannot match base64 of themselves. Scanning
    # the WHOLE blob rather than a fixed prefix also removes the "put the NUL
    # past byte 8192" variant.
    if _ARMOURED.search(body):
        return True
    lines = body.split(b"\n")
    b64_lines = sum(1 for line in lines if _B64_LINE.match(line.strip()))
    return b64_lines >= 8 and b64_lines * 2 >= sum(1 for line in lines if line.strip())


def _binary_vs(base: str, commit: str, cwd: Path) -> set[str]:
    """Files the commit adds or modifies as binary vs base (numstat '-\\t-' rows)."""
    fields = _z_fields(_git(["diff", "--no-ext-diff", "--no-textconv", "--numstat", "-z", "--diff-filter=ACMRT", base, commit], cwd))
    paths: set[str] = set()
    index = 0
    while index < len(fields):
        parts = fields[index].split("\t")
        if len(parts) < 3:
            index += 1
            continue
        added, deleted, path = parts[0], parts[1], parts[2]
        if path == "":
            path = fields[index + 2] if index + 2 < len(fields) else ""
            index += 3
        else:
            index += 1
        if added == "-" and deleted == "-" and path:
            paths.add(path)
    return paths


def _redact(text: str, patterns: dict[str, re.Pattern[str]]) -> tuple[str, bool]:
    """Replace every needle match in a path; report whether anything was replaced."""
    out = text
    for pattern in patterns.values():
        out = pattern.sub("<redacted>", out)
    return out, out != text


def _changed_vs(base: str, commit: str, cwd: Path) -> set[str]:
    """Every path whose content differs from base (any status; rename/copy destinations)."""
    fields = _z_fields(
        _git(["diff", "--no-ext-diff", "--find-renames", "--find-copies", "--name-status", "-z", base, commit], cwd)
    )
    paths: set[str] = set()
    index = 0
    while index < len(fields):
        if fields[index].startswith(("R", "C")):
            if index + 2 < len(fields):
                paths.add(fields[index + 2])
            index += 3
        else:
            if index + 1 < len(fields):
                paths.add(fields[index + 1])
            index += 2
    return paths


def _resolved_paths(parents: list[str], commit: str, cwd: Path) -> set[str] | None:
    """Paths a MERGE itself contributed: those differing from every parent.

    None for a one-parent commit, where no filtering applies and every hit
    against that single parent stands (filtering there could only drop evidence).
    """
    if len(parents) < 2:
        return None
    return set.intersection(*[_changed_vs(parent, commit, cwd) for parent in parents])


# ------------------------------------------------------------------------- scanning


def scan_commit(commit: str, cwd: Path, patterns: dict[str, re.Pattern[str]]) -> tuple[list[tuple[str, str, str, int]], int, int]:
    """Content and commit-message hits for one commit; hits carry no token."""
    parents = _parents(commit, cwd)
    resolved = _resolved_paths(parents, commit, cwd)
    content: set[tuple[str, str, int]] = set()
    if resolved is None:
        for name, file, line, _text in _content_vs(parents[0], commit, cwd, patterns):
            content.add((name, file, line))
    else:
        # Per parent: text hits on resolved paths, and which resolved paths are binary.
        # TEXT hits survive only when the same (class, file, line-text) is an addition
        # against every parent that has a text view of the path — so a needle that
        # arrived solely from main on a co-touched file is not attributed to the merge.
        # A parent against which the path is binary is skipped for that intersection
        # (round 17): otherwise a binary/text resolution would lose its text evidence.
        per_text: list[dict[str, dict[tuple[str, str], int]]] = []
        per_binary: list[set[str]] = []
        for parent in parents:
            by_file: dict[str, dict[tuple[str, str], int]] = {}
            for name, file, line, line_text in _content_vs(parent, commit, cwd, patterns):
                if file in resolved:
                    by_file.setdefault(file, {})[(name, line_text)] = line
            per_text.append(by_file)
            per_binary.append({p for p in _binary_vs(parent, commit, cwd) if p in resolved})
        for file in resolved:
            views = [
                per_text[i].get(file, {})
                for i in range(len(parents))
                if file not in per_binary[i]
            ]
            if not views:
                continue
            common = set(views[0])
            for view in views[1:]:
                common &= set(view)
            for name, line_text in common:
                content.add((name, file, views[0][(name, line_text)]))
    hits = [(name, commit, file, line) for name, file, line in sorted(content)]
    message_hits = 0
    for number, line in enumerate(_git(["log", "-1", "--format=%B", commit], cwd).split("\n"), start=1):
        for name, pattern in patterns.items():
            if _matches(pattern, line):
                hits.append((name, commit, "<commit message>", number))
                message_hits += 1
    # The IDENTITY headers are part of the commit object and are published by the
    # push exactly like its message, but ``%B`` returns only the body -- so an
    # author or committer name carrying a private value scanned CLEAN.
    identity = _git(
        ["log", "-1", "--format=%an%n%ae%n%cn%n%ce", commit], cwd
    ).split("\n")
    for number, line in enumerate(identity, start=1):
        for name, pattern in patterns.items():
            if _matches(pattern, line):
                hits.append((name, commit, "<commit identity>", number))
                message_hits += 1
                break
    return hits, len(content), message_hits



def scan_paths(
    commit: str,
    cwd: Path,
    prefixes: list[str],
    suffixes: list[str],
    patterns: dict[str, re.Pattern[str]],
) -> list[tuple[str, str, str, int]]:
    """PATH, NAME and BINARY hits for one commit."""
    hits: list[tuple[str, str, str, int]] = []
    if prefixes:
        for path in _z_fields(_git(["ls-tree", "-r", "--name-only", "-z", commit], cwd)):
            if any(path.casefold().startswith(prefix.casefold()) for prefix in prefixes):
                hits.append(("PATH", commit, path, 0))
    parents = _parents(commit, cwd)
    resolved = _resolved_paths(parents, commit, cwd)
    introduced: set[str] = set()
    binary: set[str] = set()
    for parent in parents:
        introduced |= _introduced_vs(parent, commit, cwd)
        binary |= _binary_vs(parent, commit, cwd)
    if resolved is not None:
        introduced &= resolved
        binary &= resolved
    for path in sorted(introduced):
        # Case-INSENSITIVE, and tested per path COMPONENT: ``Striker.PINE`` and a
        # DIRECTORY named ``exports.pine`` (whose children do not end in the
        # suffix) both slipped past an exact, whole-path test.
        folded = path.casefold()
        components = [part for part in folded.split("/") if part]
        # Tested against the WHOLE path and against each component: the component
        # test is what catches a DIRECTORY bearing a forbidden suffix, but on its
        # own it silently stopped matching any suffix that contains a "/", which
        # is a legitimate way to write one.
        if any(
            folded.endswith(suffix.casefold()) or any(part.endswith(suffix.casefold()) for part in components)
            for suffix in suffixes
        ):
            hits.append(("PATH", commit, path, 0))
        for name, pattern in patterns.items():
            if pattern.search(path):
                hits.append(("NAME", commit, path, 0))
    candidates = set(introduced)
    for parent in parents:
        candidates |= _changed_vs(parent, commit, cwd)
    if resolved is not None:
        candidates &= resolved | introduced
    # A path the commit DELETED is not a hit -- the docstring says so, and
    # ``_changed_vs`` carries every status, so the candidate set is intersected
    # with what actually exists in this commit's tree. Without that, every
    # deletion looked opaque, because ``cat-file`` cannot resolve a path that is
    # gone and the helper fails closed on error.
    present = set(_z_fields(_git(["ls-tree", "-r", "--name-only", "-z", commit], cwd)))
    binary |= {path for path in candidates & present if _blob_is_opaque(commit, path, cwd)}
    for path in sorted(binary):
        hits.append(("BINARY", commit, path, 0))
    return hits


def check_range_freshness(base: str, cwd: Path) -> str | None:
    """Is the range's left endpoint stale against the remote?

    The default range is anchored on a LOCAL tracking ref, which a missing fetch
    leaves behind the remote -- silently excluding commits the push would
    publish. Printing the endpoints made that auditable; this makes it fail
    closed when it can be checked at all. A network failure is reported and
    tolerated (the scan still runs); a confirmed MISMATCH is not.
    """
    if "/" not in base:
        return None
    remote, _, ref = base.partition("/")
    try:
        local = _git(["rev-parse", "--verify", base], cwd).strip()
    except RuntimeError:
        return None
    try:
        listing = _git(["ls-remote", remote, f"refs/heads/{ref}"], cwd)
    except RuntimeError:
        print(f"WARN could not reach {remote} to check {base} freshness; endpoints above are local")
        return None
    head = listing.split("\t")[0].strip() if listing.strip() else ""
    if head and head != local:
        return f"{base} is STALE: local {local[:8]}, remote {head[:8]} -- fetch and re-run"
    return None


def scan_refs(
    cwd: Path,
    base: str,
    walked: set[str],
    patterns: dict[str, re.Pattern[str]],
) -> list[tuple[str, str, str, int]]:
    """REF hits: what a push publishes that a commit range cannot express.

    ``git push`` carries ref NAMES and annotated TAG OBJECTS, and with
    ``--follow-tags`` or ``push.followTags`` it carries tags -- and the commits
    they reach -- that are outside ``origin/main..HEAD`` by construction. The
    walk is non-empty in that case, so the empty-range guard stays silent and the
    scan ends CLEAN while the push publishes a branch name, a tag message, or a
    whole side commit the scanner never opened.
    """
    hits: list[tuple[str, str, str, int]] = []
    try:
        branch = _git(["rev-parse", "--abbrev-ref", "HEAD"], cwd).strip()
    except RuntimeError:
        branch = ""
    if branch and branch != "HEAD":
        for name, pattern in patterns.items():
            if pattern.search(branch):
                hits.append(("REF", "-", branch, 0))
                break
    try:
        tags = [tag for tag in _git(["tag", "--list"], cwd).split("\n") if tag.strip()]
    except RuntimeError:
        return hits
    # Only tags this push could PUBLISH. Enumerating every local tag made an
    # unrelated, already-published one turn every otherwise-clean branch into
    # HITS -- a control that cries wolf on a normal clone is one nobody runs.
    # "--follow-tags" sends tags that are MISSING on the remote and reachable
    # from what is being pushed, so those are the two filters applied here.
    published: set[str] = set()
    remote_known = False
    try:
        listing = _git(["ls-remote", "--tags", "origin"], cwd)
        for row in listing.split("\n"):
            if "\t" in row:
                published.add(row.split("\t", 1)[1].strip().removesuffix("^{}"))
        remote_known = True
    except RuntimeError:
        published = set()
    for tag in tags:
        tag = tag.strip()
        if f"refs/tags/{tag}" in published:
            continue
        try:
            # Reachable from what is being pushed -- ``--follow-tags`` sends only
            # tags whose target the push carries or the remote already has.
            target = _git(["rev-list", "-n", "1", f"{tag}^{{commit}}"], cwd).strip()
            _git(["merge-base", "--is-ancestor", target, "HEAD"], cwd)
        except RuntimeError:
            continue
        if not remote_known:
            # No remote listing, so "already published" cannot be established.
            # FAIL CLOSED: scan the tag rather than assume it predates the push.
            # Target ancestry is NOT a substitute -- a tag object created now on
            # an old commit is missing on the remote and is exactly what
            # ``--follow-tags`` sends.
            pass
        for name, pattern in patterns.items():
            if pattern.search(tag):
                hits.append(("REF", "-", f"refs/tags/{tag}", 0))
                break
        try:
            kind = _git(["cat-file", "-t", tag], cwd).strip()
        except RuntimeError:
            continue
        if kind == "tag":
            try:
                body = _git(["cat-file", "-p", tag], cwd)
            except RuntimeError:
                body = ""
            for number, line in enumerate(body.split("\n"), start=1):
                for name, pattern in patterns.items():
                    if pattern.search(line):
                        hits.append(("REF", "-", f"refs/tags/{tag} (message)", number))
                        break
        try:
            target = _git(["rev-list", "-n", "1", f"{tag}^{{commit}}"], cwd).strip()
        except RuntimeError:
            continue
        if not target or target in walked:
            continue
        try:
            # An ancestor of the base is already published; anything else this tag
            # reaches would be newly published by a follow-tags push, unscanned.
            _git(["merge-base", "--is-ancestor", target, base], cwd)
        except RuntimeError:
            hits.append(("REF", target, f"refs/tags/{tag} (target outside the scanned range)", 0))
    return hits


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", action="append", default=[], type=Path, help="private JSON snapshot (repeatable)")
    parser.add_argument("--json-key", default="inputs", help="object key holding the private title/value map")
    parser.add_argument("--csv", action="append", default=[], type=Path, help="private/vendor CSV (repeatable)")
    parser.add_argument("--exclude", action="append", default=[], type=Path, help="file of tokens to drop, one per line (repeatable)")
    parser.add_argument("--range", default="origin/main..HEAD", help="git revision range to scan")
    parser.add_argument(
        "--no-remote-check",
        action="store_true",
        help="skip the ls-remote freshness check on the range's left endpoint (offline use)",
    )
    parser.add_argument(
        "--show-paths",
        action="store_true",
        help="print the redacted-path index mapping (LOCAL remediation only; never paste its output)",
    )
    parser.add_argument("--path-prefix", action="append", default=[], help="tree path prefix that must appear in no commit (repeatable)")
    parser.add_argument("--forbid-suffix", action="append", default=[], help="file suffix that no commit may introduce (repeatable)")
    parser.add_argument("--repo", default=".", type=Path, help="repository root (default: cwd)")
    args = parser.parse_args(argv)
    cwd = args.repo.resolve()
    # Resolve to the repository ROOT. Tree listings are relative to the git
    # directory being addressed, so pointing --repo (or the shell's cwd) at a
    # SUBDIRECTORY made every --path-prefix test look at truncated names and the
    # class reported nothing -- CLEAN on a force-added capture.
    try:
        top = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"], cwd=cwd, capture_output=True, env=_git_env()
        )
        if top.returncode == 0 and top.stdout.strip():
            cwd = Path(top.stdout.decode("utf-8", "surrogateescape").strip())
    except OSError:
        pass

    classes: dict[str, set[str]] = {"TITLE": set(), "PAIR": set(), "VALUE": set(), "CELL": set()}
    # Values too short or too plain to be needles -- a four-letter tag would
    # otherwise match ordinary prose. They are NEVER used to detect a hit, so they
    # create no false positives, but they ARE used to redact the report: a path
    # flagged for some other reason must not print such a token in clear.
    weak: set[str] = set()
    try:
        if not args.json and not args.csv:
            raise NeedleError("no needle sources given (--json / --csv)")
        dropped_keys: list[str] = []
        for path in args.json:
            built = build_json_needles(path, args.json_key)
            weak.update(built.pop("_WEAK", set()))
            dropped_keys.extend(sorted(built.pop("_DROPPED_KEYS", set())))
            for name, needles in built.items():
                classes[name].update(needles)
        for path in args.csv:
            cells, weak_cells = build_csv_needles(path)
            classes["CELL"].update(cells)
            weak.update(weak_cells)
        populated = {name: bool(needles) for name, needles in classes.items()}
        excluded: set[str] = set()
        for path in args.exclude:
            try:
                # surrogateescape, to match how needles are represented: an
                # exclusion list can legitimately name a non-UTF-8 token, and
                # a strict decode crashed with a traceback and exit 1 -- not one
                # of this script's documented codes, and not a fail-closed one.
                raw = path.read_bytes().decode("utf-8", "surrogateescape")
                excluded.update(line.strip() for line in raw.split("\n") if line.strip())
            except OSError as exc:
                raise NeedleError(f"cannot read exclude file: {path.name}") from exc
        for name in classes:
            classes[name] = {n for n in classes[name] if n and n not in excluded}
        weak = {n for n in weak if n and n not in excluded}
        # EVERY class that had needles must still have them. Testing only TITLE
        # and PAIR let an exclusion list zero the whole VALUE class while the scan
        # proceeded as if it were covered.
        for name, before in populated.items():
            if before and not classes[name]:
                raise NeedleError(f"{name} class is empty after exclusions")
        if args.json and not (classes["TITLE"] and classes["PAIR"]):
            raise NeedleError("TITLE/PAIR classes are empty after exclusions")
        if args.csv and not classes["CELL"]:
            raise NeedleError("CELL class is empty after exclusions")
    except NeedleError as exc:
        print(f"SCAN result=ERROR reason={exc}")
        return 3
    patterns = compile_classes({name: needles for name, needles in classes.items() if needles})
    # Redaction sees MORE than detection: the weak set too.
    redact_patterns = dict(patterns)
    if weak:
        redact_patterns.update(compile_classes({"_WEAK": weak}))
    print("needle classes: " + " ".join(f"{name}={len(needles)}" for name, needles in classes.items()))
    if dropped_keys:
        # COUNT ONLY. An input TITLE is itself a needle class here -- an input
        # name never legitimately appears in the published footprint -- so
        # naming the keys would have this report disclose exactly what the
        # TITLE class exists to catch. --show-paths prints them locally.
        print(f"non-distinctive, no VALUE needle (redaction-only): {len(dropped_keys)}")
        if args.show_paths:
            print("--- keys with no VALUE needle (LOCAL ONLY -- never paste) ---")
            for key in dropped_keys:
                print(f"  {key}")

    try:
        commits = _git(["rev-list", "--reverse", args.range], cwd).split()
        # The endpoints are PRINTED so a stale left-hand ref is auditable: the
        # default range is anchored on a LOCAL tracking ref, which a missing
        # fetch leaves behind the remote, silently excluding commits the push
        # would publish. The scan cannot verify freshness without the network,
        # so it states what it actually walked.
        try:
            endpoints = " ".join(
                _git(["rev-parse", "--short", endpoint], cwd).strip()
                for endpoint in args.range.replace("...", "..").split("..")
                if endpoint
            )
        except RuntimeError:
            endpoints = "unresolved"
        # REDACTED like any other printed path: this line echoes an
        # operator-supplied ref name, and a branch named after a private token
        # would otherwise be published on the CLEAN path, in the one output the
        # worker pastes into the PR body.
        shown_range, _ = _redact(args.range, redact_patterns)
        print(f"range {shown_range} -> {endpoints} commits={len(commits)}")
        base_of_range = next(
            (part for part in args.range.replace("...", "..").split("..") if part), "HEAD"
        )
        if not args.no_remote_check:
            stale = check_range_freshness(base_of_range, cwd)
            if stale:
                print(f"SCAN result=ERROR reason={stale}")
                return 3
        if not commits:
            # An EMPTY walk is not a pass. Exit 0 would be indistinguishable from
            # "the scanner never looked at the commits being pushed" -- a stale
            # ref, a wrong range, or a detached HEAD all produce it.
            print("SCAN result=ERROR reason=empty range: nothing was scanned")
            return 3
        all_hits: list[tuple[str, str, str, int]] = []
        for commit in commits:
            hits, added, message_hits = scan_commit(commit, cwd, patterns)
            path_hits = scan_paths(commit, cwd, args.path_prefix, args.forbid_suffix, patterns)
            counts = {"PATH": 0, "NAME": 0, "BINARY": 0}
            for klass, *_ in path_hits:
                counts[klass] += 1
            print(
                f"commit {commit[:8]} added={added} message={message_hits} "
                f"path={counts['PATH']} name={counts['NAME']} binary={counts['BINARY']}"
            )
            all_hits.extend(hits)
            all_hits.extend(path_hits)
        ref_hits = scan_refs(cwd, base_of_range, set(commits), patterns)
        if ref_hits:
            print(f"refs {len(ref_hits)}")
        all_hits.extend(ref_hits)
    except RuntimeError as exc:
        print(f"SCAN result=ERROR reason={exc}")
        return 4
    # A redacted path is identified by an INDEX, never by a digest of itself. A
    # short private token is brute-forceable from a truncated SHA-256, so the
    # digest that was meant to make a redacted hit actionable was an oracle that
    # handed the token back -- in the very output that gets pasted into the PR
    # body. The index is meaningless off this machine; `--show-paths` prints the
    # mapping locally, for the worker, and is never pasted anywhere.
    redacted_paths: list[str] = []
    for name, commit, file, line in all_hits:
        shown, redacted = _redact(file, redact_patterns)
        marker = ""
        if redacted:
            if file not in redacted_paths:
                redacted_paths.append(file)
            marker = f" path_index={redacted_paths.index(file)}"
        shown = shown.encode("utf-8", "replace").decode("utf-8", "replace")
        print(f"HIT class={name} commit={commit[:8]} file={shown} line={line}{marker}")
    if redacted_paths and args.show_paths:
        print("--- redacted path index (LOCAL ONLY -- never paste this block) ---")
        for index, file in enumerate(redacted_paths):
            printable = file.encode("utf-8", "replace").decode("utf-8", "replace")
            print(f"path_index={index} {printable}")
    if all_hits:
        print(f"SCAN result=HITS count={len(all_hits)} commits={len(commits)}")
        return 2
    print(f"SCAN result=CLEAN commits={len(commits)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
