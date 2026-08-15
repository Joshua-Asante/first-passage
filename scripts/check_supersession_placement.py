#!/usr/bin/env python3
"""check_supersession_placement.py — a withdrawing addendum needs an upstream warning.

THE FAILURE MODE (operational_rules.md Rule 14; two firings 2026-08-02, both
caught only by a manual pre-merge review):

  A finding is withdrawn/superseded in an addendum appended at the BOTTOM of a
  document, while the withdrawn claim keeps standing in the position a reader
  actually reads — the headline, the §Verdict, the top-of-card table. Documents
  are consumed in READING order; corrections were being applied in WRITING
  order. Trap #12 (frozen bodies, impeachment-in-addendum) protects the record;
  without a reader-intercept it sacrifices the reader.

THE MECHANICAL RULE (deliberately narrow — M-8: mechanical thresholds scope to
the mechanizable subset):

  For files in scope, if a supersession token (WITHDRAWN / SUPERSEDED /
  RETRACTED / "resolves against") first appears AT OR AFTER an addendum-class
  heading, the text BEFORE that heading must contain either a supersession
  token or an explicit pointer to the addendum. A banner like the
  book-composition brief's ">⚠ ... SUPERSEDED ... see Addendum" satisfies it;
  silence does not.

  What this deliberately does NOT catch: a claim retracted three paragraphs
  below itself INSIDE a section (firing #2, the 08-04 desk card). That is
  judgment, owned by Rule 14's prose and the restating-surfaces sweep — a gate
  pretending to cover it would be vacuous assurance.

  What this deliberately does NOT catch: a file with NO addendum heading at all -
  scan_file returns early, so a document that simply never corrects itself (e.g. a
  mooted desk card) scans clean. Missing-intercept-entirely is a human obligation
  under Rules 11/14, not a gated one.

SCOPE (the two doc classes consumed top-down under time pressure; extension is
a Rule-14 edit, not a flag):
  - docs/notes/rail_build/*DESK_CARD*.md
  - lab/analysis/**/RESULTS*.md         (theme nest; lab/archive/ is LTM — excluded)

Exit 0 clean, 1 on violations. Warn-only on files it cannot read.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Headings that mark appended-correction territory.
ADDENDUM_HEADING = re.compile(
    r"^#{2,}\s.*\b(addendum|impeachment|resolution|correction)\b", re.IGNORECASE
)
# Tokens that assert a claim above/elsewhere is no longer current.
SUPERSESSION = re.compile(
    r"\b(withdrawn|superseded|retracted|resolves\s+against)\b", re.IGNORECASE
)
# An upstream pointer to the addendum also satisfies the intercept.
POINTER = re.compile(r"\baddendum\b", re.IGNORECASE)


def scan_file(path: Path) -> str | None:
    """Return a violation message, or None if the file is clean."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:  # unreadable -> warn, never hard-fail the gate
        print(f"WARN supersession-placement: cannot read {path}: {exc}")
        return None

    first_addendum = next(
        (i for i, l in enumerate(lines) if ADDENDUM_HEADING.match(l)), None
    )
    if first_addendum is None:
        return None  # no appended-correction territory -> nothing to check

    tail = "\n".join(lines[first_addendum:])
    if not SUPERSESSION.search(tail):
        return None  # addendum is additive, not withdrawing -> fine

    head = "\n".join(lines[:first_addendum])
    if SUPERSESSION.search(head) or POINTER.search(head):
        return None  # reader-intercept exists upstream

    tok = SUPERSESSION.search(tail).group(0)
    try:
        shown = path.relative_to(REPO)
    except ValueError:  # test fixtures / out-of-tree paths
        shown = path
    return (
        f"{shown}: addendum at line {first_addendum + 1} "
        f"withdraws content ({tok!r}) but NOTHING upstream warns the reader — "
        f"add a head banner or in-body marker at the superseded claim "
        f"(operational_rules.md Rule 14; pattern: book-composition brief §2)"
    )


def in_scope(repo: Path) -> list[Path]:
    files: list[Path] = []
    files += sorted((repo / "docs" / "notes" / "rail_build").glob("*DESK_CARD*.md"))
    lab = repo / "lab" / "analysis"
    if lab.is_dir():
        for path in sorted(lab.glob("**/RESULTS*.md")):
            rel = path.relative_to(repo).as_posix()
            if "/lab/archive/" in f"/{rel}/" or rel.startswith("lab/archive/"):
                continue
            files.append(path)
    return files


def main() -> int:
    violations = [msg for f in in_scope(REPO) if (msg := scan_file(f))]
    if violations:
        for v in violations:
            print(f"HARD supersession-placement: {v}")
        print(f"check_supersession_placement: {len(violations)} violation(s).")
        return 1
    print("check_supersession_placement: OK - every withdrawing addendum has an "
          "upstream reader-intercept.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
