#!/usr/bin/env python3
"""check_handoff_brief_form.py — handoff-contract item 1 as a gate: a card passes check_brief.py.

Owner of the rule: `docs/adr/2026-07-14-cc-cursor-surface-allocation.md` §Decision, handoff
contract item 1 ("A handoff brief under `docs/briefs/**` passing `check_brief.py`"). Until
2026-09-27 nothing ran it before a dispatch, and every card carded that day was dispatched or
readied MALFORMED; Addendum 2026-09-27 records the finding, the operator's exemption of four
files, and this gate.

A card is in scope when any of these holds:

  * it sits directly under `docs/briefs/handoffs/` and its name starts with a date on or
    after CUTOFF, or carries no date prefix at all (`README.md` excepted);
  * it is any `docs/briefs/**/*.md` carrying a `yaml authority` block (a worker card under
    item 7), read with `check_handoff_authority.py`'s own block reader.

Cards dated before CUTOFF are not retrofitted, following item 7's precedent ("historical
cards are not retrofitted"). The gate does not check them; item 1 still binds any of them
that is dispatched. The files in EXEMPT are the ruling's four, exempt by name only.

An in-scope card passes exactly when `python scripts/check_brief.py <card>` exits 0, with
the same type inference and verdict: this script adds scope, never rules.

Exit codes: 0 clean · 1 a card fails, or an exemption names no file.
"""
from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import re
import sys
from pathlib import Path
from typing import NamedTuple

REPO_ROOT = Path(__file__).resolve().parent.parent
SCAN_ROOT = Path("docs") / "briefs"
HANDOFFS = SCAN_ROOT / "handoffs"

# The ruling that added this gate; cards dated earlier are not retrofitted.
CUTOFF = "2026-09-27"

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


def in_scope(rel: Path, text: str) -> bool:
    """Whether the card at repository-relative `rel` is subject to this gate."""
    if _has_authority_block(text):
        return True
    if rel.parent != HANDOFFS or rel.name == "README.md":
        return False
    dated = _DATE_PREFIX.match(rel.name)
    return dated is None or dated.group(1) >= CUTOFF


def _check_brief_verdict(path: Path) -> tuple[int, str]:
    """Run check_brief.py's own CLI entry point on `path`; return its exit code and output."""
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
        code = check_brief.main([str(path)])
    return code, out.getvalue()


def scan(root: Path = REPO_ROOT, exempt: frozenset[str] = EXEMPT) -> Result:
    """Check every in-scope card under `root`; an exemption naming no file is a failure."""
    failures: list[Failure] = []
    checked = exempted = 0
    for rel_str in sorted(exempt):
        if not (root / rel_str).is_file():
            failures.append(Failure(rel_str, "exempt path not found: remove it from EXEMPT "
                                             "and the ruling, or restore the file"))
    for path in sorted((root / SCAN_ROOT).rglob("*.md")):
        rel = path.relative_to(root)
        rel_str = rel.as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        if not in_scope(rel, text):
            continue
        if rel_str in exempt:
            exempted += 1
            continue
        checked += 1
        code, report = _check_brief_verdict(path)
        if code != 0:
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
