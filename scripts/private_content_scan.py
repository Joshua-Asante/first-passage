#!/usr/bin/env python3
"""private_content_scan.py — pre-push scan of a commit range for private bytes.

Needles are built IN MEMORY from the private files this script is pointed at
and are never written anywhere; nothing on disk is touched. The scan reads
the ADDED lines of every commit's patch and every commit message in a range
and reports whole-word, fixed-string matches by LOCATION (class, commit,
file, line) — never a matched token. It also walks every commit's tree for
forbidden path prefixes and every commit's added files for forbidden
suffixes.

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

Two further hit classes need no needles: PATH (a tree path under a
--path-prefix in ANY commit of the range, or a file with a --forbid-suffix
ADDED by any commit) and BINARY (any binary file added or modified by any
commit — a screenshot or a zipped export cannot be text-scanned, so it fails
closed). Every commit is read as its diff against its FIRST PARENT, so a merge
commit is scanned for everything that entered the branch through it.

Exit codes: 0 clean · 2 hits (content or path) · 3 needles could not be built
(a missing or unreadable private file, or an empty class for one of them —
the scan never runs "empty") · 4 git failure. Only 0 is a pass.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from pathlib import Path

_WORD = r"(?<![A-Za-z0-9_]){}(?![A-Za-z0-9_])"
_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
_DECIMAL = re.compile(r"\d\.\d")


class NeedleError(RuntimeError):
    """Raised when a needle class cannot be built; the scan must not run."""


def _git(args: list[str], cwd: Path) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args[:2])} failed with status {proc.returncode}")
    return proc.stdout


def _value_forms(value: object) -> set[str]:
    forms = {json.dumps(value)}
    if isinstance(value, str):
        forms.add(value)
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


def build_json_needles(path: Path, json_key: str) -> dict[str, set[str]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
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
        compiled[name] = re.compile(_WORD.format("(?:" + "|".join(re.escape(n) for n in ordered) + ")"))
    return compiled


_EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


def _first_parent(commit: str, cwd: Path) -> str:
    """The commit's first parent, or git's empty tree for a root commit."""
    tokens = _git(["rev-list", "--parents", "-n", "1", commit], cwd).split()
    return tokens[1] if len(tokens) > 1 else _EMPTY_TREE


def scan_commit(commit: str, cwd: Path, patterns: dict[str, re.Pattern[str]]) -> tuple[list[tuple[str, str, str, int]], int, int]:
    """Return (hits, added_hit_count, message_hit_count) for one commit; hits carry no token.

    The commit is read as its diff against its first parent (so a merge commit
    yields everything that entered the branch through it). Any binary file
    added or modified is a BINARY hit — its bytes cannot be text-scanned.
    """
    hits: list[tuple[str, str, str, int]] = []
    added = 0
    parent = _first_parent(commit, cwd)
    for line in _git(["diff", "--numstat", "--no-color", parent, commit], cwd).splitlines():
        parts = line.split("\t", 2)
        if len(parts) == 3 and parts[0] == "-" and parts[1] == "-":
            hits.append(("BINARY", commit, parts[2], 0))
    current_file = "<unknown>"
    new_line = 0
    for raw in _git(["diff", "--no-color", parent, commit], cwd).splitlines():
        if raw.startswith("diff --git "):
            current_file = raw.split(" b/", 1)[1] if " b/" in raw else "<unknown>"
            continue
        if raw.startswith("+++ "):
            current_file = raw[6:] if raw.startswith("+++ b/") else raw[4:]
            continue
        if raw.startswith("@@"):
            match = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)", raw)
            new_line = int(match.group(1)) - 1 if match else 0
            continue
        if raw.startswith("+"):
            new_line += 1
            text = raw[1:]
            for name, pattern in patterns.items():
                if pattern.search(text):
                    hits.append((name, commit, current_file, new_line))
                    added += 1
        elif raw.startswith(" "):
            new_line += 1
    message_hits = 0
    for number, line in enumerate(_git(["log", "-1", "--format=%B", commit], cwd).splitlines(), start=1):
        for name, pattern in patterns.items():
            if pattern.search(line):
                hits.append((name, commit, "<commit message>", number))
                message_hits += 1
    return hits, added, message_hits


def scan_paths(commit: str, cwd: Path, prefixes: list[str], suffixes: list[str]) -> list[tuple[str, str, str, int]]:
    """PATH hits: forbidden prefixes anywhere in the commit's tree; forbidden suffixes ADDED vs its first parent."""
    hits: list[tuple[str, str, str, int]] = []
    if prefixes:
        for path in _git(["ls-tree", "-r", "--name-only", commit], cwd).splitlines():
            if any(path.startswith(prefix) for prefix in prefixes):
                hits.append(("PATH", commit, path, 0))
    if suffixes:
        parent = _first_parent(commit, cwd)
        for path in _git(["diff", "--diff-filter=A", "--name-only", parent, commit], cwd).splitlines():
            if any(path.endswith(suffix) for suffix in suffixes):
                hits.append(("PATH", commit, path, 0))
    return hits


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", action="append", default=[], type=Path, help="private JSON snapshot (repeatable)")
    parser.add_argument("--json-key", default="inputs", help="object key holding the private title/value map")
    parser.add_argument("--csv", action="append", default=[], type=Path, help="private/vendor CSV (repeatable)")
    parser.add_argument("--exclude", action="append", default=[], type=Path, help="file of tokens to drop, one per line (repeatable)")
    parser.add_argument("--range", default="origin/main..HEAD", help="git revision range to scan")
    parser.add_argument("--path-prefix", action="append", default=[], help="tree path prefix that must appear in no commit (repeatable)")
    parser.add_argument("--forbid-suffix", action="append", default=[], help="file suffix that no commit may ADD (repeatable)")
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
            path_hits = scan_paths(commit, cwd, args.path_prefix, args.forbid_suffix)
            binary = sum(1 for h in hits if h[0] == "BINARY")
            print(f"commit {commit[:8]} added={added} message={message_hits} path={len(path_hits)} binary={binary}")
            all_hits.extend(hits)
            all_hits.extend(path_hits)
    except RuntimeError as exc:
        print(f"SCAN result=ERROR reason={exc}")
        return 4
    for name, commit, file, line in all_hits:
        print(f"HIT class={name} commit={commit[:8]} file={file} line={line}")
    if all_hits:
        print(f"SCAN result=HITS count={len(all_hits)} commits={len(commits)}")
        return 2
    print(f"SCAN result=CLEAN commits={len(commits)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
