#!/usr/bin/env python3
"""check_instrument_ledger_coverage.py -- mechanical pre-flight for
ops/instruments/<SYM>.md coverage (docs/operational_rules.md §8).

THE FAILURE MODE (2026-08-19, Research Analyst inaugural session):

  A draft named a candidate mechanism (the D5 Baltussen intraday-momentum
  axis) for MNQ as "genuinely unspent." ops/instruments/MNQ.md already
  recorded, HIGH confidence, that the same axis had been built and killed
  twice (finding N5). The drafting session's mining prompts never pointed at
  that ledger, and check_advisor_dedup.py's corpus didn't cover it either
  (fixed separately, same day -- see that script's own docstring). Caught by
  the operator asking whether the draft overlapped the ledger, not by any
  automated check. Head of Research's own same-day review named the deeper
  pattern: the same class of gap is live elsewhere -- e.g. docs/
  rejected_candidates.md's ORB-MNQ-1 Tradeify-rejection row is flagged in its
  own text as carrying "no dedup-machinery tag -- must be checked by hand."

THE MECHANICAL RULE (deliberately narrow, matching check_pursuit_records.py's
own M-8 discipline -- report only what can be checked without judgment):

  For every known instrument symbol (derived from ops/instruments/*.md
  filenames, i.e. no hand-maintained list to drift) that appears as a
  whole-word token in the target artifact, the artifact must also cite
  ops/instruments/<SYM>.md (any relative path ending in that) somewhere in
  its text. A symbol mentioned without that citation is reported.

  This tool does NOT attempt to judge whether a docs/rejected_candidates.md
  domain-level closure is "relevant" to a given instrument -- that requires
  reading and judgment, the same reason check_advisor_dedup.py calls itself
  a search assistant, not a gate. For each symbol found, this tool instead
  prints the raw grep hit count in docs/rejected_candidates.md as a reminder
  to check by hand, same posture as check_advisor_dedup.py's own advisory
  output.

SEVERITY: WARN / report-only. Exit 0 always on a completed scan -- gate
composition (whether/how this is wired into the pre-commit tier stack) is
owned by scripts/gates.yml via gate_manifest.py, not decided here. Exit 2
only on CLI misuse (missing/unreadable target file).

SCOPE: any single markdown file passed as a CLI argument. Typical callers:
a new lab/analysis/<theme>/<slug>/ body, a new docs/briefs/ entry, or
(historically) a persona-authored draft (persona system retired 2026-08-31 --
see docs/adr/2026-08-31-persona-hierarchy-full-retirement.md) -- per
operational_rules.md §8's own scope ("opening any new
lab/analysis/<theme>/<slug>/ directory or scoping new core/-adjacent
implementation work").

Usage:
    python scripts/check_instrument_ledger_coverage.py <path-to-artifact.md>
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INSTRUMENTS_DIR = REPO_ROOT / "ops" / "instruments"
REJECTED_PATH = REPO_ROOT / "docs" / "rejected_candidates.md"

# Non-symbol files that live alongside the per-instrument ledgers -- excluded
# explicitly rather than guessed at, so a future addition to this small list
# doesn't silently start being treated as a ticker.
NON_SYMBOL_STEMS = frozenset({"MECHANISMS", "PROFILES"})


def known_symbols(instruments_dir: Path) -> list[str]:
    """Derive the instrument-symbol set from ops/instruments/*.md filenames
    -- no hand-maintained list, so it can't drift out of sync with the
    ledger directory the way a copied-in constant would."""
    if not instruments_dir.is_dir():
        return []
    symbols = []
    for md in sorted(instruments_dir.glob("*.md")):
        stem = md.stem
        if stem in NON_SYMBOL_STEMS:
            continue
        if not stem.isalnum():
            continue
        if not stem.isupper():
            continue
        symbols.append(stem)
    return symbols


def find_mentioned_symbols(text: str, symbols: list[str]) -> list[str]:
    mentioned = []
    for sym in symbols:
        if re.search(rf"\b{re.escape(sym)}\b", text):
            mentioned.append(sym)
    return mentioned


def cites_ledger(text: str, sym: str) -> bool:
    return f"instruments/{sym}.md" in text


def rejected_candidates_hits(sym: str, rejected_text: str) -> int:
    return len(re.findall(rf"\b{re.escape(sym)}\b", rejected_text))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("target", type=Path, help="Path to the artifact to check.")
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    args = ap.parse_args(argv)

    if not args.target.is_file():
        print(f"check_instrument_ledger_coverage: no such file: {args.target}", file=sys.stderr)
        return 2

    text = args.target.read_text(encoding="utf-8", errors="replace")
    instruments_dir = args.repo_root / "ops" / "instruments"
    rejected_path = args.repo_root / "docs" / "rejected_candidates.md"

    symbols = known_symbols(instruments_dir)
    if not symbols:
        print("check_instrument_ledger_coverage: no ops/instruments/*.md ledgers found -- nothing to check.")
        return 0

    mentioned = find_mentioned_symbols(text, symbols)
    if not mentioned:
        print(f"check_instrument_ledger_coverage: {args.target} -- no known instrument symbols mentioned. Nothing to check.")
        return 0

    rejected_text = rejected_path.read_text(encoding="utf-8", errors="replace") if rejected_path.is_file() else ""

    missing = [s for s in mentioned if not cites_ledger(text, s)]

    print(f"check_instrument_ledger_coverage: {args.target}")
    print(f"  instrument symbols mentioned: {mentioned}")
    print()

    if missing:
        print(f"WARN: {len(missing)} symbol(s) mentioned without citing their ops/instruments/<SYM>.md ledger:")
        for s in missing:
            print(f"  - {s}: expected a citation containing 'instruments/{s}.md' somewhere in this artifact.")
            print(f"    That ledger's own purpose line makes it mandatory reading before naming any")
            print(f"    candidate mechanism for {s} -- see docs/operational_rules.md §8.")
        print()
    else:
        print("OK: every mentioned instrument symbol's ledger is cited somewhere in this artifact.")
        print()

    print("Advisory only (not scored pass/fail -- read and judge, don't assume from a count):")
    for s in mentioned:
        n = rejected_candidates_hits(s, rejected_text)
        print(f"  - {s}: {n} whole-word hit(s) in docs/rejected_candidates.md -- check by hand for relevance.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
