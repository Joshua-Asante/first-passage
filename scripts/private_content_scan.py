#!/usr/bin/env python3
"""private_content_scan.py — pre-push scan of a commit range for private bytes.

Needles are built IN MEMORY from the private files this script is pointed at
and are never written anywhere; nothing on disk is touched. The scan reports
matches by LOCATION (class, commit, file, line) — never a matched token. A
reported PATH is itself redacted where a needle matched it (a private value can
appear in a FILENAME) and carries a short digest of the true path instead, so
the location survives for local remediation while the scanner's own output —
which the worker pastes into the PR body — stays publishable.

What each commit is compared against: EVERY parent. An ordinary one-parent
commit is its diff against that parent. A merge is read with git's COMBINED
diff, and only lines absent from EVERY parent — the ``++`` lines, its conflict
resolution — are scanned: a line inherited from one side renders as ``+ `` or
`` +`` and is not the merge's own, so a merge of ``origin/main`` neither
re-reports what ``main`` brought in nor lets a clean two-sided edit of one file
promote that whole file. Binary and path evidence is unioned across parents over
the paths that differ from all of them, so a path binary in one parent and text
in another cannot fall between the two.

Every diff is taken PER PATH with a ``:(literal)`` pathspec, and the path comes
from a NUL-delimited listing, never from a patch header — git C-quotes a header
path containing a tab, newline, quote or backslash regardless of
``core.quotePath``, and a header-derived name would then never match the raw
one.

Git runs with ``core.quotePath=false`` and path lists are read NUL-delimited,
so a non-ASCII filename cannot slip past a prefix or suffix test.

Needle classes (campaign-state §47b step 6b, 2026-09-04):
  TITLE  every key of the JSON object at --json-key (default ``inputs``)
  PAIR   every (key, value) of that object in four serializations:
         ``"k": v`` · ``"k":v`` · ``k: v`` · ``k=v``
  VALUE  every value of that object that is distinctive — a string of at
         least four characters, or a number with a decimal point, an exponent,
         or at least four digits (trivial scalars are covered by TITLE/PAIR and
         by the worker's provenance self-read; a bare ``true`` would match
         every file). A number contributes BOTH its source lexeme exactly as
         written in the snapshot (``1.2500``) and its canonical JSON spelling
         (``1.25``): a value copied from the chart keeps its trailing zeros, and
         a needle built from the round-tripped float alone would miss it on a
         word boundary.
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
_HUNK = re.compile(r"\+(\d+)")   # first "+N" in "@@ -a,b +c,d @@" or "@@@ -a,b -c,d +e,f @@@"
_EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


class NeedleError(RuntimeError):
    """Raised when a needle class cannot be built; the scan must not run."""


def _git(args: list[str], cwd: Path) -> str:
    # Captured as BYTES and decoded here, deliberately: ``text=True`` enables
    # universal-newline translation, which rewrites every CR in git's output --
    # including one inside a NUL-delimited path, and including one inside an
    # added line, where it would split the line and hide everything after it.
    # ``surrogateescape`` makes an undecodable byte round-trip: subprocess
    # encodes POSIX argv with the same handler, so a path that is not valid
    # UTF-8 still names the real tree entry through a ``:(literal)`` pathspec.
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


# --------------------------------------------------------------------------- needles


class _Num(str):
    """A JSON number kept as the exact lexeme written in the source file."""


def _canonical_number(lexeme: str) -> str:
    text = lexeme.lower()
    if "." in text or "e" in text:
        return json.dumps(float(lexeme))
    return json.dumps(int(lexeme))


def _value_forms(value: object) -> set[str]:
    if isinstance(value, _Num):
        return {str(value), _canonical_number(value)}
    forms = {json.dumps(value)}
    if isinstance(value, str):
        forms.add(value)
    return forms


def _distinctive(value: object) -> bool:
    if isinstance(value, bool) or value is None:
        return False
    if isinstance(value, _Num):
        text = value.lower()
        return "." in text or "e" in text or sum(ch.isdigit() for ch in text) >= 4
    if isinstance(value, str):
        return len(value) >= 4
    if isinstance(value, (int, float)):
        text = json.dumps(value)
        return "." in text or sum(ch.isdigit() for ch in text) >= 4
    return False


def build_json_needles(path: Path, json_key: str) -> dict[str, set[str]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"), parse_float=_Num, parse_int=_Num)
    except (OSError, ValueError) as exc:
        raise NeedleError(f"cannot read JSON needle source: {path.name}") from exc
    obj = payload.get(json_key) if isinstance(payload, dict) else None
    if not isinstance(obj, dict) or not obj:
        raise NeedleError(f"{path.name}: no non-empty object at key {json_key!r}")
    title: set[str] = set()
    pair: set[str] = set()
    value_needles: set[str] = set()
    for key, value in obj.items():
        key = str(key)
        if not key:
            continue
        title.add(key)
        for form in _value_forms(value):
            pair.update({f'"{key}": {form}', f'"{key}":{form}', f"{key}: {form}", f"{key}={form}"})
        if _distinctive(value):
            value_needles.update(_value_forms(value))
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
        # SUBSTRING, not word-bounded. A word boundary that counts "_" and digits
        # as word characters made every needle invisible the moment it was glued
        # into a longer identifier, filename or commit message -- and made the
        # report print such a path verbatim, because the redaction used the same
        # patterns. A disclosure control fails closed: a coincidental hit is
        # adjudicated, a missed one is published.
        compiled[name] = re.compile("(?:" + "|".join(re.escape(n) for n in ordered) + ")")
    return compiled


# ------------------------------------------------------------------- per-parent reads


def _scan_diff_text(text: str, ncols: int, path: str, patterns: dict[str, re.Pattern[str]]) -> set[tuple[str, str, int]]:
    """(class, path, new-line) for lines the diff ADDS, over a per-path diff of known path.

    ``ncols`` is the number of prefix columns: 1 for an ordinary diff, one per
    parent for a combined diff. A line counts as added only when EVERY column is
    ``+`` — in a combined diff that is a line absent from every parent, the
    merge's own contribution. Lines carrying any ``-`` are not in the result and
    do not advance the new-file line number. The path is the one the diff was
    asked for, so the C-quoted header is never parsed.
    """
    hits: set[tuple[str, str, int]] = set()
    new_line = 0
    in_hunk = False
    # split on "\n" ONLY: git delimits patch records with LF, while str.splitlines()
    # also breaks on \v, \f, \r, \x1c-\x1e, \x85, \u2028 and \u2029 — a needle after such a
    # byte would land in a fragment with no "+" marker and never be scanned.
    for raw in text.split("\n"):
        if raw.startswith("@@"):
            in_hunk = True
            match = _HUNK.search(raw)
            new_line = int(match.group(1)) - 1 if match else 0
            continue
        if not in_hunk or raw.startswith("\\") or len(raw) < ncols:
            continue
        cols, body = raw[:ncols], raw[ncols:]
        if "-" in cols:
            continue
        new_line += 1
        if all(col == "+" for col in cols):
            for name, pattern in patterns.items():
                if pattern.search(body):
                    hits.add((name, path, new_line))
    return hits


def _content_for(commit: str, parents: list[str], paths: set[str], cwd: Path, patterns: dict[str, re.Pattern[str]]) -> set[tuple[str, str, int]]:
    """Content hits for one commit over the given raw paths, one per-path diff each."""
    hits: set[tuple[str, str, int]] = set()
    for path in sorted(paths):
        spec = f":(literal){path}"
        if len(parents) == 1:
            text = _git(["diff", "--no-color", parents[0], commit, "--", spec], cwd)
            hits |= _scan_diff_text(text, 1, path, patterns)
        else:
            text = _git(["diff-tree", "--no-commit-id", "-c", "-p", "--no-color", commit, "--", spec], cwd)
            hits |= _scan_diff_text(text, len(parents), path, patterns)
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
        _git(["diff", "--find-renames", "--find-copies", "--name-status", "-z", "--diff-filter=ACMRT", base, commit], cwd)
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
    paths = _changed_vs(parents[0], commit, cwd) if resolved is None else resolved
    content = _content_for(commit, parents, paths, cwd, patterns)
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
        # The digest is over the path's TRUE bytes, so it stays a usable local
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
