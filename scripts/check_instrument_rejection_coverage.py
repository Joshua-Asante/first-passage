#!/usr/bin/env python3
"""check_instrument_rejection_coverage.py -- the D4 enforcement instrument
for docs/adr/2026-08-09-rejection-register-topology-and-bar-wiring.md.

THE RULE (ADR D4 / D3): per D3's register-topology table, `ops/instruments/
<SYM>.md` DEAD/REJECTED tables own **per-direction, instrument-scoped**
mechanism rejections (`docs/rejected_candidates.md` owns the domain-level /
cross-instrument tier instead -- a different register, not checked here;
`docs/methodology/rejected_signals.md` owns the meta-layer tier and is
explicitly not machine-consulted at all). D4 says that per-direction rule "is
currently enforced by nothing" and orders exactly one check: does every
terminal-negative closure naming a specific instrument have a corresponding
DEAD row in that instrument's ledger? This script is that check. It answers
the ADR's own Section 4 falsifier limb (b), read again at the 2026-11-08 quarterly
gate: "the ledger-coverage rate for in-window instrument-scoped terminal-
negative closures is below 100% with no dated exception" -> FALSIFIED.

WHAT COUNTS AS "TERMINAL-NEGATIVE" (documented, not guessed -- Step 1 of the
authoring plan read the real **Verdict:** field vocabulary across every file
in docs/briefs/closures/ before this list was written; the plan's own
illustrative `**Instrument:**` field and `*-closure-falsified.md` / `*-dead*`
filename heuristic turned out not to match the real corpus and were replaced):

  A closure's primary verdict token is extracted from (in priority order):
    1. a `**Verdict:** <TOKEN>` line (the field ~85% of real closures carry);
    2. the H1 title's `... CLOSURE: <TOKEN>` fragment, case-insensitive on the
       word "closure" (a fallback for closures with no Verdict field but a
       token-bearing title, e.g. the Hermes/S-MYM-ORC family; Q-JOINT-TAIL-
       WEEKLY's title uses lowercase "closure:");
    3. a `## Verdict (...)` HEADING's body prose (the two Aegis->6J
       reconstruction closures and Q-GATECART-1 use this shape: no Verdict
       field, no title token, just a "## Verdict (exactly one)" section whose
       first bold line states the disposition) -- scanned for the same
       whole-word tokens as layer 4, but confined to that section only;
    4. a last-resort whole-word scan of the first 500 characters only (title
       + immediate metadata block) for one of the same tokens below -- never
       the whole body, so a deep-body mention of "FALSIFIED" describing a
       DIFFERENT, already-closed campaign can't false-positive a RESOLVED
       closure.
  That token is TERMINAL-NEGATIVE iff it starts with one of
  FALSIFIED / DEAD / NULL / KILL / OPERATOR-KILL / CLOSED-FALSIFIED, or
  contains the standalone word FAIL (covers SCREEN-FAIL, "STAGE-1 FAIL").
  Explicitly EXCLUDED, on real-corpus evidence, even though a case can be
  made for some of them: RESOLVED* (a pass, not a rejection), AMBIGUOUS*
  (unresolved -- the ADR's own Section 5 forbidden-move #2 warns a DEAD-table row is
  not automatically a mechanism rejection; this script does not adjudicate
  which AMBIGUOUS-HOLD rows the ADR's D3 prose separately calls "genuine"),
  VOID* / VOID-POWER* (a power/premise void, not a verdict on the mechanism),
  CLOSED-AMBIGUOUS, MOOT, ABORTED (a run that stopped before any mechanism
  verdict), NOT-KILLED (the literal opposite of a rejection). A closure whose
  verdict cannot be classified by any of the three layers is UNCLASSIFIED --
  reported separately, counted toward neither pass nor fail.

WHAT COUNTS AS "NAMING A SPECIFIC INSTRUMENT" (reuses this repo's own
established convention, scripts/check_instrument_ledger_coverage.py's
`known_symbols()` / whole-word-token approach, rather than inventing a new
one): the instrument-symbol universe is derived from `ops/instruments/*.md`
filenames (excluding MECHANISMS / PROFILES / README and any stem that isn't
all-uppercase-alnum -- no hand-maintained ticker list to drift). A closure is
IN SCOPE for this gate iff exactly one of those symbols appears as a
whole-word token anywhere in its text. Zero symbols named -> domain-level /
cross-instrument, D3's OTHER register, correctly out of scope here. Two or
more -> also out of scope (a genuinely cross-instrument closure is D3's
domain tier too, or the closure covers multiple per-instrument cells that
should each have their own closure file, as Q-TXG-1's two cells in fact do).
KNOWN UNDER-COUNT: a construct whose SIGNAL derives from two instruments but
is TRADED on a third (Q-MNQDTL-CON-1: "ES-NQ 5m divergence... x MNQ", per its
own Registry line) mentions three tickers and is therefore excluded here even
though the ADR's own D3 consequence-prose names this exact closure as MNQ-
ledger-owed. That closure's own self-declared Registry line disagrees with
the ADR and asks for `rejected_candidates.md` instead -- genuinely
adjudication-requiring, so this script does not guess which of 3+ tickers is
"the real one"; it excludes and lets a human read the GAP-adjacent domain
bucket. Do not read "e.g. ~30 domain/cross-instrument, therefore correctly
out of scope" (illustrative only -- run this script for the current count,
which drifts as the corpus grows; do not hand-maintain a point figure here)
as verified for every one of them -- it is a conservative default, not an
audit of each one.

WHAT COUNTS AS "A CORRESPONDING DEAD ROW": the named instrument's
`ops/instruments/<SYM>.md` must have a heading matching "Dead / Rejected" or
"Dead / parked" (both real spellings on disk today -- MNQ.md etc. use the
former, BTCUSD.md / USDCAD.md the latter), and EITHER (a) the closure's own
filename appears (as a markdown-link target substring or a bare stem match)
somewhere inside that heading's section, OR (b) the closure's campaign ID
(everything in its filename before "-closure", e.g. "Q-R2VBUCK-1" from
"Q-R2VBUCK-1-closure-falsified.md") appears as a whole word inside that same
section -- real DEAD-table rows often cite the campaign ID and link a
RESULTS/PREREG file rather than the closures/ file itself (verified example:
MNQ.md's Q-R2VBUCK-1 row links `RESULTS_g2.md`, never the closure filename,
but is unambiguously the row this gate is asking about). A mention found
elsewhere in the ledger file (SESSION LOG, a numbered finding outside the
DEAD heading) but NOT inside the DEAD section itself is still reported as a
GAP (with a distinguishing note) -- the ADR asks for a DEAD *row*, not just a
citation anywhere in the file.

SCOPE AND ITS LIMITS (read before trusting a green run):

  * UNCLASSIFIED VERDICTS AND MULTI/ZERO-INSTRUMENT CLOSURES ARE SKIPPED, NOT
    PASSED. They are counted and printed separately. A green run means "zero
    gaps among what this script could classify", never "every closure in the
    corpus was checked".
  * LEDGERS WITH NO DEAD-ISH HEADING AT ALL (today: 6J.md, GER40.md; also any
    redirect stub like US500.md -> SPX500.md) are reported as SKIPPED per
    affected closure, not silently counted as covered *or* as a gap. This is
    measured at run time from whatever ledgers exist on disk -- never
    hand-listed here, so it can't go stale.
  * TICKER MENTION IS NOT PROOF OF SCOPE. The "exactly one known ticker
    mentioned" in-scope rule inherits this repo's own established convention
    (check_instrument_ledger_coverage.py) and its own known failure mode: a
    governance/meta/programme-level closure that merely NAMES a strategy
    (`ORB-MNQ-1`), a sibling closure ID (`Q-USOIL-1`), or cites one legacy
    leg's Sharpe in a 4-way comparison table (`NAS100 1.45`) gets misread as
    a per-instrument mechanism rejection about that ticker. Three confirmed
    instances in the corpus at authoring time -- Q-OBJCOHERE-1 (mentions MNQ
    only via "ORB-MNQ-1" inside a doctrine-hierarchy coherence audit),
    Q-SCORE-1 (mentions USOIL only via "Q-USOIL-1" inside a closure-naming-
    convention audit), and Q-GATECART-1 (mentions NAS100 only as one of four
    locked legs' Sharpe figures inside a K-budget/DSR-demonstrability-floor
    finding) -- are independently confirmed non-instrument-mechanism by
    check_closure_disposition.py's own REGISTRY_GRANDFATHERED_NA /
    REGISTRY_DEBT_2026_08 sets (Q-GATECART-1 is in the DEBT set -- it owes a
    domain-register row, i.e. it IS a real rejection, just not an
    instrument-scoped one). This script does not special-case them (a
    hand-maintained exclusion list is exactly the kind of drift-prone
    constant this repo's own tooling philosophy avoids) -- read every GAP
    line, don't just trust the count.
  * PRESENCE, NOT CORRECTNESS. This checks that *a* row exists referencing
    the closure -- it does not (cannot, without judgment) verify the row
    correctly characterizes the closure's finding, matching the same M-8
    "report only what can be checked without judgment" discipline as
    check_pursuit_records.py / check_instrument_ledger_coverage.py.
  * WARN-TIER BY DESIGN, PER-INVOCATION HARD SIGNAL. Bare invocation (as run
    manually, or by pytest here) exits 1 on any real gap -- Step 6 of the
    authoring plan needs that honest number, not a pre-neutered one. The
    `--exit-zero` flag exists solely for the gates.yml WARN-tier wiring: this
    repo's gate runner (scripts/gate_manifest.py) treats any non-zero exit
    from ANY wired gate as a hard stop -- there is no tier that "runs and
    reports but never blocks" (the declared `soft` tier is dead code: see
    scripts/gates.yml's own header note; gate_manifest.py's `select_gates`
    drops it in `pre-commit` and never includes it in `check`). `--exit-zero`
    is therefore how gates.yml itself keeps ownership of this gate's
    severity (matching check_instrument_ledger_coverage.py's own stated
    posture -- "gate composition is owned by scripts/gates.yml ... not
    decided here") while still actually executing, unlike `soft`. Promote by
    dropping the flag from this gate's `cmd:` in scripts/gates.yml once the
    real-corpus run is clean or every remaining gap carries a dated,
    named exception (ADR Section 4 falsifier text, verbatim).

Usage:
    python scripts/check_instrument_rejection_coverage.py               # real signal, exit 1 on any gap
    python scripts/check_instrument_rejection_coverage.py --exit-zero   # gates.yml WARN-tier wiring
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path


def _repo_root() -> Path:
    override = os.environ.get("REPO_ROOT_OVERRIDE")
    if override:
        return Path(override)
    return Path(__file__).resolve().parents[1]


ROOT = _repo_root()
CLOSURES_DIR = ROOT / "docs" / "briefs" / "closures"
INSTRUMENTS_DIR = ROOT / "ops" / "instruments"

# Non-ticker files living alongside the per-instrument ledgers. Named
# explicitly (same posture as check_instrument_ledger_coverage.py's own
# NON_SYMBOL_STEMS) rather than guessed at, plus README -- that script's own
# stem-is-all-uppercase test would otherwise admit it as a "ticker" too.
NON_SYMBOL_STEMS = frozenset({"MECHANISMS", "PROFILES", "README"})

# Both real headings on disk today (2026-08-28): "DEAD / REJECTED
# (instrument-specific)" (most ledgers) and "Dead / parked (do not revive...)"
# (BTCUSD.md, USDCAD.md). Case-insensitive, tolerant of the parenthetical.
DEAD_HEADING_RE = re.compile(r"^#{1,4}\s*Dead\s*/\s*(?:Rejected|Parked)\b", re.IGNORECASE)
ANY_HEADING_RE = re.compile(r"^(#{1,6})\s+\S")

VERDICT_LINE_RE = re.compile(r"^\*\*Verdict:\*\*\s*(?P<rest>.+)$", re.MULTILINE)
# Case-insensitive on the literal word "closure:" only (real titles use both
# "CLOSURE:" and lowercase "closure:", e.g. Q-JOINT-TAIL-WEEKLY's) -- the
# captured token itself still must start uppercase per _TOKEN_RE below, so
# this cannot suddenly start parsing lowercase prose as a verdict.
TITLE_CLOSURE_RE = re.compile(
    r"^#\s.*\bCLOSURE:\s*(?P<rest>.+)$", re.MULTILINE | re.IGNORECASE
)
# A third real shape (the two Aegis->6J reconstruction closures, Q-GATECART-1):
# no Verdict field, no title token -- instead a "## Verdict (exactly one)"
# heading whose body prose states the disposition in bold
# ("**FALSIFIED -- H-SWEEP** (Stage-1).").
VERDICT_HEADING_RE = re.compile(r"^#{1,4}\s*Verdict\b", re.IGNORECASE)
_TOKEN_RE = re.compile(r"[A-Z][A-Z0-9\- ]*")

# Fallback layer 3 patterns -- first 500 chars only, see module docstring.
_FALLBACK_WORD_RES = [
    re.compile(r"\bFALSIFIED\b"),
    re.compile(r"\bDEAD\b"),
    re.compile(r"\bNULL\b"),
    re.compile(r"\bOPERATOR-KILL\b"),
    re.compile(r"\bCLOSED-FALSIFIED\b"),
    re.compile(r"\bKILL\b"),
    re.compile(r"\bFAIL\b"),
]

_NEGATIVE_PREFIX_RE = re.compile(
    r"^(FALSIFIED|DEAD|NULL|KILL|OPERATOR-KILL|CLOSED-FALSIFIED)\b"
)
_FAIL_WORD_RE = re.compile(r"\bFAIL\b")

FALLBACK_SCAN_CHARS = 500

# Campaign ID = everything before "-closure" in the filename (general, no
# hardcoded prefix whitelist -- check_closure_disposition.py's own
# (Q|H|GSUB|MNQBASE|OPENPRESS|MYM|SLR|ST)- allowlist already misses "MSL",
# proof that a hand-enumerated prefix set drifts). Date-prefixed nonstandard
# closures (e.g. "2026-08-12-q-txg-1-...-dead-nsurv.md", no "-closure-"
# substring at all) correctly return None -- those are covered via the
# filename-link check instead (verified: they DO carry literal closures/
# links in their DEAD rows).
_CAMPAIGN_ID_RE = re.compile(r"^(?P<id>.+?)-closure(?:-|$)")


def campaign_id_from_filename(name: str) -> str | None:
    stem = name[:-3] if name.endswith(".md") else name
    m = _CAMPAIGN_ID_RE.match(stem)
    return m.group("id") if m else None


def known_symbols(instruments_dir: Path) -> list[str]:
    """Instrument-symbol universe, derived from ops/instruments/*.md
    filenames -- no hand-maintained list, so it can't drift out of sync with
    the ledger directory (same convention as check_instrument_ledger_coverage.py)."""
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


def mentioned_symbols(text: str, symbols: list[str]) -> list[str]:
    return [s for s in symbols if re.search(rf"\b{re.escape(s)}\b", text)]


def _extract_token(rest: str) -> str:
    s = rest.strip().lstrip("`* ")
    m = _TOKEN_RE.match(s)
    if not m:
        return ""
    return re.sub(r"[\s\-]+$", "", m.group(0))


def is_terminal_negative(token: str) -> bool:
    if not token:
        return False
    if _NEGATIVE_PREFIX_RE.match(token):
        return True
    if _FAIL_WORD_RE.search(token):
        return True
    return False


@dataclass(frozen=True)
class Verdict:
    negative: bool
    token: str
    source: str  # "Verdict field" | "title CLOSURE: token" | "Verdict heading" | "fallback scan" | "unclassified"


def classify_verdict(text: str) -> Verdict:
    m = VERDICT_LINE_RE.search(text)
    if m:
        tok = _extract_token(m.group("rest"))
        if tok:
            return Verdict(is_terminal_negative(tok), tok, "Verdict field")
    m = TITLE_CLOSURE_RE.search(text)
    if m:
        tok = _extract_token(m.group("rest"))
        if tok:
            return Verdict(is_terminal_negative(tok), tok, "title CLOSURE: token")
    section = extract_section(text, VERDICT_HEADING_RE)
    if section:
        for pat in _FALLBACK_WORD_RES:
            fm = pat.search(section)
            if fm:
                return Verdict(True, fm.group(0), "Verdict heading")
    head = text[:FALLBACK_SCAN_CHARS]
    for pat in _FALLBACK_WORD_RES:
        fm = pat.search(head)
        if fm:
            return Verdict(True, fm.group(0), "fallback scan (first 500 chars)")
    return Verdict(False, "", "unclassified")


def extract_section(text: str, heading_re: re.Pattern) -> str | None:
    """Return the heading (matching `heading_re`) through to the next
    same-or-shallower heading, or None if no matching heading exists."""
    lines = text.splitlines()
    start = None
    start_level = 0
    for i, ln in enumerate(lines):
        if heading_re.match(ln):
            start = i
            start_level = len(re.match(r"^#{1,6}", ln).group(0))
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        hm = ANY_HEADING_RE.match(lines[j])
        if hm and len(hm.group(1)) <= start_level:
            end = j
            break
    return "\n".join(lines[start:end])


@dataclass(frozen=True)
class InScopeClosure:
    path: Path
    symbol: str
    token: str
    source: str


@dataclass(frozen=True)
class Gap:
    path: Path
    symbol: str
    reason: str


@dataclass(frozen=True)
class Skipped:
    path: Path
    symbol: str
    reason: str


def scan_closures(closures_dir: Path, symbols: list[str]) -> tuple[
    list[InScopeClosure], int, int, int, int
]:
    """Return (in_scope, n_scanned, n_unclassified, n_domain_or_cross,
    n_positive_or_excluded).

    2026-08-28 review fix: this docstring and the return annotation
    previously described a 3-tuple (in_scope, n_scanned, n_unclassified) and
    claimed n_domain_or_cross was "derivable by the caller" -- the function
    has always computed and returned all five values itself (see main()'s
    5-way unpack); the description had simply drifted out of sync with the
    code.
    """
    in_scope: list[InScopeClosure] = []
    n_scanned = 0
    n_unclassified = 0
    n_domain_or_cross = 0
    n_positive_or_excluded = 0
    for path in sorted(closures_dir.glob("*.md")):
        n_scanned += 1
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            n_unclassified += 1
            continue
        v = classify_verdict(text)
        if v.source == "unclassified":
            n_unclassified += 1
            continue
        if not v.negative:
            n_positive_or_excluded += 1
            continue
        mentioned = mentioned_symbols(text, symbols)
        if len(mentioned) != 1:
            n_domain_or_cross += 1
            continue
        in_scope.append(InScopeClosure(path, mentioned[0], v.token, v.source))
    return in_scope, n_scanned, n_unclassified, n_domain_or_cross, n_positive_or_excluded


def check_coverage(
    in_scope: list[InScopeClosure], instruments_dir: Path
) -> tuple[list[Path], list[Gap], list[Skipped]]:
    covered: list[Path] = []
    gaps: list[Gap] = []
    skipped: list[Skipped] = []

    ledger_text_cache: dict[str, str | None] = {}
    dead_section_cache: dict[str, str | None] = {}

    for item in in_scope:
        sym = item.symbol
        if sym not in ledger_text_cache:
            ledger_path = instruments_dir / f"{sym}.md"
            try:
                ledger_text_cache[sym] = ledger_path.read_text(
                    encoding="utf-8", errors="replace"
                )
            except OSError:
                ledger_text_cache[sym] = None
        ledger_text = ledger_text_cache[sym]

        if ledger_text is None:
            skipped.append(
                Skipped(item.path, sym, f"ops/instruments/{sym}.md unreadable or missing")
            )
            continue

        if sym not in dead_section_cache:
            dead_section_cache[sym] = extract_section(ledger_text, DEAD_HEADING_RE)
        section = dead_section_cache[sym]

        if section is None:
            skipped.append(
                Skipped(
                    item.path,
                    sym,
                    f"no 'Dead / Rejected' or 'Dead / parked' heading found in "
                    f"ops/instruments/{sym}.md",
                )
            )
            continue

        cid = campaign_id_from_filename(item.path.name)
        cid_in_section = bool(cid) and re.search(rf"\b{re.escape(cid)}\b", section)

        link_needle = f"closures/{item.path.name}"
        if link_needle in section or item.path.stem in section or cid_in_section:
            covered.append(item.path)
        elif link_needle in ledger_text or item.path.stem in ledger_text:
            gaps.append(
                Gap(
                    item.path,
                    sym,
                    "referenced elsewhere in the ledger, but not inside its "
                    "DEAD/REJECTED section",
                )
            )
        else:
            gaps.append(Gap(item.path, sym, "no reference found anywhere in the ledger"))

    return covered, gaps, skipped


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument(
        "--exit-zero",
        action="store_true",
        help="Always exit 0 (findings still print). gates.yml WARN-tier wiring "
        "flag -- see module docstring 'WARN-TIER BY DESIGN'.",
    )
    args = ap.parse_args(argv)

    print(
        "check_instrument_rejection_coverage: D4 enforcement instrument "
        "(ADR 2026-08-09-rejection-register-topology-and-bar-wiring, Section 4 falsifier "
        "limb b, next quarterly gate 2026-11-08)"
    )

    if not CLOSURES_DIR.is_dir():
        print(f"  no {CLOSURES_DIR} -- nothing to check.")
        return 0

    symbols = known_symbols(INSTRUMENTS_DIR)
    if not symbols:
        print(f"  no ops/instruments/*.md ledgers found under {INSTRUMENTS_DIR} -- nothing to check.")
        return 0

    in_scope, n_scanned, n_unclassified, n_domain_or_cross, n_excluded = scan_closures(
        CLOSURES_DIR, symbols
    )
    covered, gaps, skipped = check_coverage(in_scope, INSTRUMENTS_DIR)

    checkable = len(covered) + len(gaps)
    rate = (100.0 * len(covered) / checkable) if checkable else float("nan")

    print()
    print(f"  closures scanned                                          : {n_scanned}")
    print(f"    unclassified verdict (no parseable Verdict/title token)  : {n_unclassified}  [excluded either way]")
    print(f"    non-negative verdict (RESOLVED/AMBIGUOUS/VOID/etc.)      : {n_excluded}  [not a rejection]")
    print(f"    domain-level / cross-instrument (0 or 2+ tickers named)  : {n_domain_or_cross}  [D3's OTHER register -- rejected_candidates.md]")
    print(f"  in-scope (terminal-negative, exactly one instrument named) : {len(in_scope)}")
    print()
    print(f"  covered (linked inside the named DEAD/REJECTED section)   : {len(covered)}")
    print(f"  GAPS (no corresponding DEAD row)                          : {len(gaps)}")
    print(f"  SKIPPED (instrument ledger has no DEAD-ish section at all): {len(skipped)}  [uncheckable, not silently passed]")
    if checkable:
        print(f"  ledger-coverage rate (checkable in-scope only)            : {rate:.1f}%  ({len(covered)}/{checkable})")
    else:
        print("  ledger-coverage rate (checkable in-scope only)            : n/a (0 checkable)")

    if skipped:
        skipped_syms = sorted({s.symbol for s in skipped})
        print()
        print(f"  SKIPPED detail -- instruments with no DEAD-ish section: {skipped_syms}")
        for s in skipped:
            print(f"    - {s.path.name}  [{s.symbol}]  {s.reason}")

    if gaps:
        print()
        print("  GAP detail:")
        for g in gaps:
            print(f"    - {g.path.name}  [{g.symbol}]  {g.reason}")

    print()
    if not gaps:
        print("check_instrument_rejection_coverage: OK -- every checkable in-scope "
              "closure has a corresponding DEAD row.")
    else:
        print(f"check_instrument_rejection_coverage: {len(gaps)} gap(s). "
              "Add a DEAD/REJECTED row to the named instrument's ops/instruments/"
              "<SYM>.md (or record a dated exception per the ADR's Section 4 falsifier).")

    if args.exit_zero:
        return 0
    return 1 if gaps else 0


if __name__ == "__main__":
    sys.exit(main())
