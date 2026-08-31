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
    `../adr/<file>.md` / `../../adr/<file>.md` form, AND the cited `<file>.md` must
    actually exist under `docs/adr/` — a syntactically well-formed but nonexistent or
    misspelled path does not count as provenance. A citation by ADR TITLE alone, with
    no path, is invisible here (measured false-negative risk — cheap to add if it proves
    common; not observed in the corpus at introduction time).

  * SCOPED TO `docs/spec/` ONLY. A structurally similar canon-adjacent artifact filed
    under `docs/notes/` or elsewhere is invisible here (raised in PR #233 review,
    2026-08-31) — not extended without a corpus census first: `docs/notes/` is far more
    heterogeneous than `docs/spec/` (audits, research notes, notice logs, interpretive
    commentary that explicitly disclaims changing any gate), and applying this
    heuristic there unstudied risks false-positive noise the way it would not for the
    uniformly decision/build-shaped `docs/spec/` corpus.

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
    # Slug allows dots: real ADR filenames carry version numbers, e.g.
    # 2026-04-17-guardian-v5.1-architecture.md, 2026-04-23-guardian-risk-relock-0.34.md
    # (found by PR #233 review round 1). Greedy [\w.-]+ backtracks to let the trailing
    # literal \.md match, so this does not swallow the extension itself.
    #
    # Exactly one `../` (not `(?:\.\./)+`): scan() below only visits docs/spec/*.md
    # direct children, so the correct relative path up to docs/adr/ is always exactly
    # one level. `has_live_adr_citation` below checks only the cited basename's
    # existence, not the literal number of `../` segments written -- allowing two or
    # more would let a citation like `../../adr/<real-file>.md` (which actually
    # resolves outside docs/, to a nonexistent path) count as live provenance just
    # because a same-named file happens to exist under docs/adr/ (found by PR #233
    # review round 6). The negative lookbehind is required, not cosmetic: without it
    # `\.\./adr/` still matches the embedded substring starting one `../` in, so
    # `../../adr/x.md` would match at offset 3 even with the `+` removed -- confirmed
    # by direct regex testing before adding the lookbehind.
    r"(?<!\.\./)(?:docs/adr/|\.\./adr/)(\d{4}-\d{2}-\d{2}[a-z]?-[\w.-]+)\.md"
)


def has_live_adr_citation(text: str, adr_dir: Path) -> bool:
    """True iff at least one cited ADR path resolves to a real file under adr_dir.

    A syntactically well-formed but nonexistent or misspelled path (e.g. a typo, or
    a citation to a not-yet-written ADR) does not count as provenance — found by
    PR #233 review: the prior version treated a regex match alone as sufficient.
    """
    for slug in ADR_CITE_RE.findall(text):
        if (adr_dir / f"{slug}.md").exists():
            return True
    return False


def scan(spec_dir: Path) -> tuple[list[str], list[str], list[str]]:
    """Returns (all_scanned, canon_amending, zero_citation_findings), each a list of paths."""
    adr_dir = spec_dir.parent / "adr"
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
        if not has_live_adr_citation(text, adr_dir):
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
        "canon-owner file) should cite the ADR(s) it reconciles against — this script "
        "checks for a citation resolving to a real file under docs/adr/, nothing more; "
        "it cannot judge whether no relevant ADR in fact exists yet. docs/spec/README.md: "
        "\"ADRs own the decision; specs here commission or describe a build.\" Consider "
        "landing decision-shaped content as an ADR instead, so check_adr_graph.py's "
        "coverage applies."
    )
    return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
