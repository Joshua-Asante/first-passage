#!/usr/bin/env python3
"""check_spec_provenance.py — WARN-tier census: canon-amending specs with zero ADR citations.

`docs/spec/README.md` says it plainly: "ADRs own the decision; specs here commission or
describe a build. Do not treat a `PROPOSED` spec as authorization." Nothing in
`scripts/gates.yml` enforces that line — `docs/spec/` carries zero gate coverage today
(confirmed: `grep -c docs/spec scripts/gates.yml` returns 0 before this gate). A spec that
steps outside the commission-a-build charter and proposes to amend canon (Rule 2, the
INQHIORI phase contract, operational rules, the regime-robustness gate) is exactly the
class no mechanical check touches — the same class `check_adr_graph.py` polices for
`docs/adr/` itself.

This script asks one narrow, cheap question: **does a canon-amending `docs/spec/` file
cite ANY ADR at all?** It does not verify the citations are the RIGHT ones (that needs a
human or `pre-ratification-adversarial-panel`) — a spec that cites some ADR and got the
wrong one is invisible here by design. A spec that cites zero, while proposing to amend
canon, is the specific failure this gate exists to surface: it means no dedup search
against existing decisions is even visible in the artifact.

SCOPE AND ITS LIMITS:

  * "Canon-amending" is detected two ways: (1) a `##`/`###` header containing
    "ratification", "canon edit(s)", or "amend*"; (2) a reference to a named canon-owner
    file (inqhiori-canon.md, operational_rules.md, strategy_lifecycle.md,
    regime_robustness_gate.md). Both are cheap syntactic heuristics, not semantic
    understanding — a spec that discusses ratification only in passing prose (no header)
    and never names a canon-owner file is invisible here.

  * ADR citations are counted as links matching `docs/adr/<file>.md` or a relative
    `../adr/<file>.md` / `../../adr/<file>.md` form. A citation by ADR TITLE alone, with
    no path, is invisible here (measured false-negative risk — cheap to add if it proves
    common; not observed in the corpus at introduction time).

  * WARN-TIER BY DESIGN. Always exits 0 unless --strict. No clean-baseline run has ever
    been done against this heuristic before today, so promoting straight to a hard gate
    would repeat the exact mistake `check_falsifier_reachability.py`'s own docstring
    warns against (the ADR governing that script bars promotion before a clean baseline
    exists) — this script follows the same discipline. Wired into `gates.yml` as
    `falsifier-reachability-census`'s sibling: `tier: always`, report-only.

  * SCANS THE WHOLE `docs/spec/` CORPUS EVERY RUN, not just staged files — same reasoning
    as `check_falsifier_reachability.py --stats`: a census is only informative if it is
    never silently stale between the commits that happen to touch `docs/spec/`.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

HEADER_RE = re.compile(
    r"^#{1,3}\s*.*\b(canon\s*edit|ratification|amend)\w*.*$",
    re.IGNORECASE | re.MULTILINE,
)
CANON_OWNER_RE = re.compile(
    r"\b(inqhiori-canon\.md|operational_rules\.md|strategy_lifecycle\.md|"
    r"regime_robustness_gate\.md)\b",
    re.IGNORECASE,
)
ADR_CITE_RE = re.compile(
    r"(?:docs/adr/|(?:\.\./)+adr/)(\d{4}-\d{2}-\d{2}[a-z]?-[\w-]+)\.md"
)


def scan(spec_dir: Path) -> tuple[list[str], list[str], list[str]]:
    """Returns (all_scanned, canon_amending, zero_citation_findings), each a list of paths."""
    scanned: list[str] = []
    amending: list[str] = []
    findings: list[str] = []
    for path in sorted(spec_dir.glob("*.md")):
        rel = str(path.relative_to(REPO_ROOT))
        scanned.append(rel)
        text = path.read_text(errors="replace")
        is_amending = bool(HEADER_RE.search(text)) or bool(CANON_OWNER_RE.search(text))
        if not is_amending:
            continue
        amending.append(rel)
        if not ADR_CITE_RE.search(text):
            findings.append(rel)
    return scanned, amending, findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stats", action="store_true", help="print the census summary")
    parser.add_argument(
        "--strict", action="store_true", help="exit 1 on findings (default: always exit 0)"
    )
    args = parser.parse_args(argv)

    spec_dir = REPO_ROOT / "docs" / "spec"
    scanned, amending, findings = scan(spec_dir)

    if args.stats:
        print(f"docs/spec/ files scanned   : {len(scanned)}")
        print(f"canon-amending (heuristic) : {len(amending)}")
        print(f"  -> zero ADR citations    : {len(findings)}")
        print()

    if not findings:
        print(
            f"check_spec_provenance: OK ({len(amending)} canon-amending spec(s) scanned, "
            "0 with zero ADR citations)"
        )
        print(
            "  NOTE: green means every canon-amending spec cites AT LEAST ONE ADR by path — "
            "not that the citation is the right one, or that dedup search was thorough. "
            "See module docstring for what this check cannot see."
        )
        return 0

    print(
        "check_spec_provenance: WARN -- canon-amending spec(s) with zero ADR citations\n"
    )
    for rel in findings:
        print(f"  {rel}")
    print(
        f"\n  {len(findings)} finding(s). A docs/spec/ file proposing to amend canon "
        "(a header naming ratification/canon edits/amendments, or a reference to a named "
        "canon-owner file) should cite the ADR(s) it reconciles against, or state "
        "explicitly that none exist yet. docs/spec/README.md: \"ADRs own the decision; "
        "specs here commission or describe a build.\" Consider landing decision-shaped "
        "content as an ADR instead, so check_adr_graph.py's coverage applies."
    )
    return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
