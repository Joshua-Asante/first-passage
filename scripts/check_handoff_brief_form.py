#!/usr/bin/env python3
"""check_handoff_brief_form.py — handoff-contract item 1 as a gate: a card passes check_brief.py.

Owner of the rule: `docs/adr/2026-07-14-cc-cursor-surface-allocation.md` §Decision, handoff
contract item 1 ("A handoff brief under `docs/briefs/**` passing `check_brief.py`"). Until
2026-09-27 nothing ran it before a dispatch, and every card carded that day was dispatched or
readied MALFORMED; Addendum 2026-09-27 records the finding, the operator's exemption of four
files, and this gate.

A card is in scope when either holds:

  * it sits directly under `docs/briefs/handoffs/` (`README.md` excepted) and is not a
    historical card named in GRANDFATHERED_FILE;
  * it is any `docs/briefs/**/*.md` carrying a `yaml authority` block (a worker card under
    item 7), read with `check_handoff_authority.py`'s own block reader.

The historical cards are the files dated before CUTOFF that were on `main` when this gate
landed. They are listed by name, so a new card given an earlier date is still checked. They
are not retrofitted, following item 7's precedent ("historical cards are not retrofitted");
item 1 still binds any of them that is dispatched. The files in EXEMPT are the ruling's four,
exempt by name only.

An in-scope card passes only when `python scripts/check_brief.py --type handoff <card>`
prints `RESULT: well-formed`. The type is forced, not inferred: every card in scope is a
handoff card by its directory or its authority block, and content-based inference would let a
card that omits §0.5 and the four-state return pass as `generic`. The checker's zero-exit
`NOT CHECKED` outcome (a light-tier header) does not pass either: it validates nothing. This
script adds scope, never rules: the handoff contract is `check_brief.py`'s own.

In a git checkout, a card with both staged and unstaged changes fails: pre-commit would
check the working-tree copy while the commit records the staged one.

Exit codes: 0 clean · 1 a card fails, or an exemption names no file.
"""
from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import re
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

REPO_ROOT = Path(__file__).resolve().parent.parent
SCAN_ROOT = Path("docs") / "briefs"
HANDOFFS = SCAN_ROOT / "handoffs"

# The ruling that added this gate; historical cards dated earlier are not retrofitted.
CUTOFF = "2026-09-27"
GRANDFATHERED_FILE = REPO_ROOT / "scripts" / "handoff_brief_form_grandfathered.txt"
_WELL_FORMED = "RESULT: well-formed"

# Exempt by the operator's dated ruling (ADR Addendum 2026-09-27, its *Ruling* table), as
# recorded deviations: dispatched or used for dispatch without passing item 1.
# tests/scripts/test_check_handoff_brief_form.py pins this set to that table.
EXEMPT = frozenset({
    "docs/briefs/handoffs/2026-09-27-h4-fence-classification-orb-l1-repair.md",
    "docs/briefs/handoffs/2026-09-27-h5b-attended-incident-rehearsal.md",
    "docs/briefs/handoffs/2026-09-27-h8c-omission-incident-session-end.md",
    "docs/briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md",
})

_DATE_PREFIX = re.compile(r"^(\d{4}-\d{2}-\d{2})-")


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, REPO_ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod  # dataclasses resolve their module by name
    spec.loader.exec_module(mod)
    return mod


check_brief = _load("check_brief")
authority = _load("check_handoff_authority")


class Failure(NamedTuple):
    """One refused card: its repository-relative path and the report explaining why."""
    path: str
    report: str


class Result(NamedTuple):
    """Outcome of one scan: refused cards, and how many were checked or exempted."""
    failures: list[Failure]
    checked: int
    exempted: int


def _has_authority_block(text: str) -> bool:
    return bool(authority.extract_blocks(text) or authority.stray_fences(text))


def load_grandfathered(path: Path = GRANDFATHERED_FILE) -> frozenset[str]:
    """Names of the historical cards; every one must be dated before CUTOFF."""
    names = frozenset(line.strip() for line in path.read_text(encoding="utf-8").splitlines()
                      if line.strip() and not line.lstrip().startswith("#"))
    for name in names:
        dated = _DATE_PREFIX.match(name)
        if dated is None or dated.group(1) >= CUTOFF:
            raise ValueError(f"{path.name}: {name!r} is not a card dated before {CUTOFF}")
    return names


def in_scope(rel: Path, text: str, grandfathered: frozenset[str]) -> bool:
    """Whether the card at repository-relative `rel` is subject to this gate."""
    if _has_authority_block(text):
        return True
    if rel.parent != HANDOFFS or rel.name == "README.md":
        return False
    return rel.name not in grandfathered


def _partially_staged(root: Path) -> set[str]:
    """Paths under the scan root with both staged and unstaged changes (empty outside git)."""
    def names(*args: str) -> set[str] | None:
        proc = subprocess.run(["git", "-C", str(root), "diff", "--name-only", *args, "--",
                               SCAN_ROOT.as_posix()], capture_output=True, text=True, check=False)
        return set(proc.stdout.split()) if proc.returncode == 0 else None
    staged, unstaged = names("--cached"), names()
    if staged is None or unstaged is None:
        return set()
    return staged & unstaged


def _check_brief_verdict(path: Path) -> tuple[int, str]:
    """Run check_brief.py's own CLI entry point on `path` as a handoff card; return its
    exit code and output."""
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
        code = check_brief.main(["--type", "handoff", str(path)])
    return code, out.getvalue()


def scan(root: Path = REPO_ROOT, exempt: frozenset[str] = EXEMPT,
         grandfathered: frozenset[str] | None = None) -> Result:
    """Check every in-scope card under `root`; an exemption naming no file is a failure."""
    if grandfathered is None:
        grandfathered = load_grandfathered()
    failures: list[Failure] = []
    checked = exempted = 0
    partial = _partially_staged(root)
    for rel_str in sorted(exempt):
        if not (root / rel_str).is_file():
            failures.append(Failure(rel_str, "exempt path not found: remove it from EXEMPT "
                                             "and the ruling, or restore the file"))
    for path in sorted((root / SCAN_ROOT).rglob("*.md")):
        rel = path.relative_to(root)
        rel_str = rel.as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        if not in_scope(rel, text, grandfathered):
            continue
        if rel_str in exempt:
            exempted += 1
            continue
        checked += 1
        if rel_str in partial:
            failures.append(Failure(rel_str, "staged and unstaged changes differ: stage the "
                                             "whole card, or stash the rest, then re-run"))
            continue
        code, report = _check_brief_verdict(path)
        if code != 0 or _WELL_FORMED not in report:
            failures.append(Failure(rel_str, report))
    return Result(failures, checked, exempted)


def main(argv: list[str] | None = None) -> int:
    """CLI entry point: scan the repository (or --root) and report refused cards."""
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=REPO_ROOT, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    result = scan(args.root)
    for failure in result.failures:
        print(f"HARD {failure.path}")
        for line in failure.report.rstrip().splitlines():
            print(f"    {line}")
    print(f"check_handoff_brief_form: {result.checked} card(s) in scope, "
          f"{result.exempted} exempt by ruling, {len(result.failures)} failing")
    return 1 if result.failures else 0


if __name__ == "__main__":
    sys.exit(main())
