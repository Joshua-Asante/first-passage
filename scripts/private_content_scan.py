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
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
_DECIMAL = re.compile(r"\d\.\d")
_HUNK = re.compile(r"@@ -\d+(?:,\d+)? \+(\d+)")
_EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
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
    proc = subprocess.run(
        ["git", "-c", "core.quotePath=false", *args],
        cwd=cwd,
        capture_output=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args[:2])} failed with status {proc.returncode}")
    return proc.stdout.decode("utf-8", "surrogateescape")


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


def _distinctive(value: object) -> bool:
    if isinstance(value, bool) or value is None:
        return False
    if isinstance(value, str):
        return len(value) >= 4
    if isinstance(value, (int, float)):
        text = json.dumps(value)
        return "." in text or sum(ch.isdigit() for ch in text) >= 4
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
    for key, value in obj.items():
        key = str(key)
        if not key:
            continue
        title.add(key)
        # numeric lexemes only — quoted string lexemes duplicate the parsed form
        raw_nums = {
            lex for lex in lexemes.get(key, ())
            if lex not in {"true", "false", "null"} and not lex.startswith('"')
        }
        forms = _value_forms(value, raw_lexemes=raw_nums or None)
        for form in forms:
            pair.update({f'"{key}": {form}', f'"{key}":{form}', f"{key}: {form}", f"{key}={form}"})
        if _distinctive(value):
            value_needles.update(forms)
    return {"TITLE": title, "PAIR": pair, "VALUE": value_needles}


def build_csv_needles(path: Path) -> set[str]:
    try:
        with path.open(encoding="utf-8", errors="replace", newline="") as handle:
            rows = list(csv.reader(handle))
    except OSError as exc:
        raise NeedleError(f"cannot read CSV needle source: {path.name}") from exc
    cells: set[str] = set()
    for row in rows[1:]:
        for cell in row:
            cell = cell.strip()
            if cell and (_DECIMAL.search(cell) or _DATE.search(cell)):
                cells.add(cell)
    if not cells:
        raise NeedleError(f"{path.name}: no data cells with a decimal point or a date")
    return cells


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
        compiled[name] = re.compile("(?:" + "|".join(re.escape(n) for n in ordered) + ")")
    return compiled


# ------------------------------------------------------------------- per-parent reads


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
    # split on "\n" ONLY: git delimits patch records with LF, while str.splitlines()
    # also breaks on \v, \f, \r, \x1c-\x1e, \x85, \u2028 and \u2029 — a needle after such a
    # byte would land in a fragment with no "+" marker and never be scanned.
    for raw in _git(["diff", "--no-color", base, commit], cwd).split("\n"):
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
            for name, pattern in patterns.items():
                if pattern.search(line_text):
                    hits.add((name, current_file, new_line, line_text))
        elif raw.startswith(" "):
            new_line += 1
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


def _binary_vs(base: str, commit: str, cwd: Path) -> set[str]:
    """Files the commit adds or modifies as binary vs base (numstat '-\\t-' rows)."""
    fields = _z_fields(_git(["diff", "--numstat", "-z", "--diff-filter=ACMRT", base, commit], cwd))
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
        _git(["diff", "--find-renames", "--find-copies", "--name-status", "-z", base, commit], cwd)
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
            if pattern.search(line):
                hits.append((name, commit, "<commit message>", number))
                message_hits += 1
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
            if any(path.startswith(prefix) for prefix in prefixes):
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
        if any(path.endswith(suffix) for suffix in suffixes):
            hits.append(("PATH", commit, path, 0))
        for name, pattern in patterns.items():
            if pattern.search(path):
                hits.append(("NAME", commit, path, 0))
    for path in sorted(binary):
        hits.append(("BINARY", commit, path, 0))
    return hits


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", action="append", default=[], type=Path, help="private JSON snapshot (repeatable)")
    parser.add_argument("--json-key", default="inputs", help="object key holding the private title/value map")
    parser.add_argument("--csv", action="append", default=[], type=Path, help="private/vendor CSV (repeatable)")
    parser.add_argument("--exclude", action="append", default=[], type=Path, help="file of tokens to drop, one per line (repeatable)")
    parser.add_argument("--range", default="origin/main..HEAD", help="git revision range to scan")
    parser.add_argument("--path-prefix", action="append", default=[], help="tree path prefix that must appear in no commit (repeatable)")
    parser.add_argument("--forbid-suffix", action="append", default=[], help="file suffix that no commit may introduce (repeatable)")
    parser.add_argument("--repo", default=".", type=Path, help="repository root (default: cwd)")
    args = parser.parse_args(argv)
    cwd = args.repo.resolve()

    classes: dict[str, set[str]] = {"TITLE": set(), "PAIR": set(), "VALUE": set(), "CELL": set()}
    try:
        if not args.json and not args.csv:
            raise NeedleError("no needle sources given (--json / --csv)")
        for path in args.json:
            for name, needles in build_json_needles(path, args.json_key).items():
                classes[name].update(needles)
        for path in args.csv:
            classes["CELL"].update(build_csv_needles(path))
        excluded: set[str] = set()
        for path in args.exclude:
            try:
                excluded.update(line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
            except OSError as exc:
                raise NeedleError(f"cannot read exclude file: {path.name}") from exc
        for name in classes:
            classes[name] = {n for n in classes[name] if n and n not in excluded}
        if args.json and not (classes["TITLE"] and classes["PAIR"]):
            raise NeedleError("TITLE/PAIR classes are empty after exclusions")
        if args.csv and not classes["CELL"]:
            raise NeedleError("CELL class is empty after exclusions")
    except NeedleError as exc:
        print(f"SCAN result=ERROR reason={exc}")
        return 3
    patterns = compile_classes({name: needles for name, needles in classes.items() if needles})
    print("needle classes: " + " ".join(f"{name}={len(needles)}" for name, needles in classes.items()))

    try:
        commits = _git(["rev-list", "--reverse", args.range], cwd).split()
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
    except RuntimeError as exc:
        print(f"SCAN result=ERROR reason={exc}")
        return 4
    for name, commit, file, line in all_hits:
        shown, redacted = _redact(file, patterns)
        # Digest over the path's TRUE bytes, so it stays a usable local
        # remediation handle for a name that is not valid UTF-8; the displayed
        # form is made printable separately, since a surrogate would crash stdout.
        digest = (
            f" path_sha256={hashlib.sha256(file.encode('utf-8', 'surrogateescape')).hexdigest()[:12]}"
            if redacted
            else ""
        )
        shown = shown.encode("utf-8", "replace").decode("utf-8", "replace")
        print(f"HIT class={name} commit={commit[:8]} file={shown} line={line}{digest}")
    if all_hits:
        print(f"SCAN result=HITS count={len(all_hits)} commits={len(commits)}")
        return 2
    print(f"SCAN result=CLEAN commits={len(commits)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
