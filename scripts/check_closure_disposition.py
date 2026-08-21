#!/usr/bin/env python3
"""check_closure_disposition.py — every new closure carries a typed Iterate block.

THE FAILURE MODE (ADR 2026-08-04-iterate-closure-exit-mandatory §1; measured
baseline in its §0):

  Closures already do forward-disposition work — 10/10 in the pre-ADR survey —
  but under 7+ different section names, never as a typed field, and the
  board-write pointer (which STATE row / SESSIONS Open-next line the closure
  adds) is explicit in only 2/10. The ADR-layer version of that missing limb is
  the paid incident: the 08-08 board gap (SESSIONS 2026-08-04a, audit R9 — the
  quarterly audit vehicle unscheduled while ~31 ADRs' obligations rode it).

THE MECHANICAL RULE (deliberately narrow — M-8; the dropped C1/C4 checks in
check_status_consistency.py are the recorded proof that SEMANTIC closure
completeness has no reachable gate):

  A non-grandfathered file under docs/briefs/closures/ must contain
    (1) a heading whose text contains "Iterate",
    (2) a "Next:" line carrying exactly ONE of INTEGRATE / ITERATE / STOP
        (all three at once = the unfilled template placeholder), and
    (3) a "Board write" token.
  Entry-packet quality, stop-rule honesty, and disposition-vs-§6 consistency
  are judgment — owned by the brief-authoring closure checklist and the
  quarterly methodology audit (the owning ADR's §4 ceremony limb), never here.

COVERAGE LIMB (self-arming — ADR 2026-08-12-closure-disposition-coverage-hard):

  The Iterate-token scan can only see closures that EXIST. A second limb
  derives campaigns that claim a closed/terminal verdict (INDEX Open rows
  with CLOSED/FALSIFIED/VOID/AMBIGUOUS-… Status; INDEX Recently closed
  bullets; CATALOG rows that name a Q-ID alongside archive-owed CLOSED/
  FALSIFIED) and reports any with no matching file under
  docs/briefs/closures/ or docs/ltm/briefs/. Severity is owned by
  COVERAGE_OWNING_ADR (not the Iterate ADR): Proposed ⇒ WARN + exit 0;
  Accepted ⇒ HARD + exit 1. Historical gaps listed in
  COVERAGE_GRANDFATHERED stay excluded forever (belt-churn YELLOW
  2026-08-08 — a HARD fire on pre-promotion gaps would block unrelated
  work). That set is empty at authoring: PR #745 cleared the backlog
  9 → 0 (SESSIONS 2026-08-11v). Never append IDs here to dodge the gate;
  a newly discovered pre-promotion gap needs a superseding ADR.

SEVERITY (self-arming on ratification; two owning ADRs):

  Iterate limb → OWNING_ADR (2026-08-04-iterate-closure-exit-mandatory).
  Coverage limb → COVERAGE_OWNING_ADR
  (2026-08-12-closure-disposition-coverage-hard).
  While an owning ADR is `Proposed`, that limb's violations print as WARN
  and do not flip the exit code. Once `Accepted`, that limb's violations
  are HARD and contribute exit 1. A missing/unparseable ADR degrades its
  limb to WARN with a loud notice (fail-open: this gate must never block
  unrelated commits on its own broken dependency — M-22 posture).
  Explicit-path mode (authoring-time: `python scripts/check_closure_disposition.py
  <file>...`) always exits 1 on Iterate-token violations — an opt-in check
  of a named file wants a hard answer and cannot block unrelated work.
  Explicit-path mode does not run the coverage limb.

SCOPE (extension is an ADR edit — supersede in part — not a flag):
  - docs/briefs/closures/*.md, minus the GRANDFATHERED set (the 34 closures
    that predate the Iterate ADR; forward-only, no retro-editing per its §5).
  - Coverage: newly claimed terminal verdicts without a closure record,
    minus COVERAGE_GRANDFATHERED.

Exit 0 clean / WARN-tier, 1 on HARD violations. Warn-only on unreadable files.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CLOSURES_DIR = REPO / "docs" / "briefs" / "closures"
LTM_BRIEFS_DIR = REPO / "docs" / "ltm" / "briefs"
INDEX_PATH = REPO / "docs" / "briefs" / "INDEX.md"
CATALOG_PATH = REPO / "lab" / "CATALOG.md"
OWNING_ADR = REPO / "docs" / "adr" / "2026-08-04-iterate-closure-exit-mandatory.md"
# Coverage-limb severity owner (supersedes the 2026-08-04 ADR in part —
# advisory-coverage clause only). Independent of OWNING_ADR so Iterate can
# stay HARD while coverage is still Proposed.
COVERAGE_OWNING_ADR = (
    REPO / "docs" / "adr" / "2026-08-12-closure-disposition-coverage-hard.md"
)

# A heading whose text contains "Iterate" ("## Iterate — loop exit",
# "## 6. Iterate", "### §5 — Iterate" all match; "Iterating" does not).
ITERATE_HEADING = re.compile(r"^#{2,}\s.*\bIterate\b", re.IGNORECASE)
# The typed branch line: "- **Next:** ITERATE" / "Next: STOP" / "**Next**: X".
# The colon is MANDATORY (in either bold position) so prose like
# "Next steps: ITERATE on sizing" never satisfies the gate (adversarial
# finding, 2026-08-04 pre-ratification review).
NEXT_LINE = re.compile(
    r"^\s*(?:[-*]\s*)?\*{0,2}Next(?::\*{0,2}|\*{0,2}:)\s*(?P<rest>.+)$"
)
BRANCH_TOKEN = re.compile(r"\b(INTEGRATE|ITERATE|STOP)\b")
# The unfilled-template signature: two branch tokens joined by | or / .
# Plain prose mentioning a second token ("STOP — do not ITERATE without new
# mechanism evidence") is legal; only separator-joined tokens are the
# placeholder (adversarial finding: false-fail on re-proposal-bar prose).
PLACEHOLDER = re.compile(
    r"\b(?:INTEGRATE|ITERATE|STOP)\b\s*[|/]\s*\b(?:INTEGRATE|ITERATE|STOP)\b"
)
# The board pointer: "- **Board write:** ..." (hyphen or space; any decoration).
BOARD_TOKEN = re.compile(r"\bBoard[\s-]+write\b", re.IGNORECASE)
# Registry feed (2026-08-15): strategy-grounds kills must name the
# rejected_candidates row, or an explicit n/a reason. Forward-only —
# REGISTRY_GRANDFATHERED holds every closure on disk at land time.
REGISTRY_TOKEN = re.compile(
    r"^\s*(?:[-*]\s*)?\*{0,2}Registry(?::\*{0,2}|\*{0,2}:)\s*(?P<rest>.+)$"
)

# Markdown fence delimiter. Fenced content is stripped before scanning so a
# quoted template (the realistic paste-from-closure_record.md path) can never
# satisfy the gate (adversarial finding: fence-blindness false pass).
FENCE_DELIM = re.compile(r"^\s*(```|~~~)")

# ADR Status header token, same grammar family as check_adr_graph.py
# (backticks optional so a de-backticked header degrades the parse gracefully
# rather than silently disarming a ratified gate).
STATUS_LINE = re.compile(r"^\*\*Status:\*\*\s*`?(?P<tok>[A-Za-z][\w/-]*)`?")

# ── coverage limb: campaign ID + terminal-verdict recognition ──────────
# Bold IDs as stored in INDEX (M-AHF: **Q-OFCHAN-1**, not bare Q-OFCHAN-1).
BOLD_CAMPAIGN_ID = re.compile(
    r"\*\*"
    r"(?P<id>(?:Q|H|GSUB|MNQBASE|OPENPRESS|MYM|SLR|ST)"
    r"-[A-Z0-9]+(?:-[A-Z0-9]+)*)"
    r"\*\*"
)
# Loose ID mention (CATALOG one-liners; no bold required).
LOOSE_CAMPAIGN_ID = re.compile(
    r"\b(?P<id>(?:Q|H|GSUB|MNQBASE|OPENPRESS|MYM|SLR|ST)"
    r"-[A-Z0-9]+(?:-[A-Z0-9]+)*)\b"
)
# Open-table Status tokens that mean "this Q filed a terminal verdict".
# Bare RESOLVED is excluded (Q-CAPRES-2 stays Open with residual work;
# FILLTAX Status prose can say "Gate RESOLVED" while remaining OPEN).
# RESOLVED-ABSENT is excluded (Layer-A limb, formal DEAD close reserved).
OPEN_TABLE_TERMINAL = re.compile(
    r"(?i)(?<![\w-])(?:"
    r"CLOSED(?:-[\w]+)?"
    r"|FALSIFIED(?:-[\w]+)?"
    r"|VOID(?:-[\w]+)?"
    r"|AMBIGUOUS(?:-[\w]+)?"
    r"|ABORT(?:ED)?"
    r"|MOOT"
    r"|RETIRED"
    r"|BLOCKED-RETIRED"
    r"|OPERATOR-STOPPED"
    r"|SCREEN-FAIL"
    r")(?![\w-])"
)
# Status / section markers that are explicitly NOT closure-bearing.
NON_CLOSURE_BEARING = re.compile(
    r"(?i)\b(?:"
    r"DORMANT"
    r"|PARKED"
    r"|DRAFT(?:ED)?(?:-NOT-OPENED)?"
    r"|RESOLVED-ABSENT"
    r")\b"
)
# Primary OPEN status token (backticked or bold) — skip even if later prose
# mentions RESOLVED/FALSIFIED hypothetically.
OPEN_STATUS_PRIMARY = re.compile(
    r"(?i)(?:\*\*`?|`)OPEN(?:`?\*\*|`|\*\*)"
)
# CATALOG one-liner / status cells that claim a closed campaign.
CATALOG_TERMINAL = re.compile(
    r"(?i)(?:archive\s+owed\s*\([^)]*\)|\bCLOSED\b|\bFALSIFIED\b|\bVOID\b|"
    r"\bAMBIGUOUS(?:-[\w]+)?\b|\bRETIRED\b)"
)
# Filename → campaign ID. Standard: ID-closure-slug. Nonstandard house names
# in closures/ (Q-KBUDGET-HARVEST-1-bounded-…, Q-HARV-0-month-end-…): ID then
# a lowercase prose token.
CLOSURE_FILENAME_STANDARD = re.compile(
    r"^((?:Q|H|GSUB|MNQBASE|OPENPRESS|MYM|SLR|ST)"
    r"-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*?)-closure(?:-|$)"
)
CLOSURE_FILENAME_NONSTANDARD = re.compile(
    r"^((?:Q|H|GSUB|MNQBASE|OPENPRESS|MYM|SLR|ST)"
    r"-[A-Z0-9]+(?:-[A-Z0-9]+)*)-[a-z]"
)

# Closures on disk at ADR authoring time (2026-08-04). Forward-only boundary —
# permanent record, per the ADR's §5 first forbidden move. Never append here to
# dodge the gate; a new closure complies instead.
GRANDFATHERED = frozenset({
    "2026-07-16-aegis-6j-prop-reconstruction-stage1-falsified.md",
    "2026-07-16-aegis-6j-prop-reconstruction-stage2-hsolo-falsified.md",
    "2026-07-16-striker-mym-reconstruction-candidate-1-ambiguous.md",
    "2026-07-16-striker-mym-reconstruction-candidate-2-falsified.md",
    "2026-07-27-hermes-agent-adoption-closure-resolved.md",
    "H-FBEIA-1-closure-screen-fail.md",
    "H-FCCARRY-1-closure-screen-fail.md",
    "H-ZNAUC-1-closure-screen-fail.md",
    "MYM-3FPS-1-closure-falsified.md",
    "OPENPRESS-1-closure-falsified.md",
    "Q-6JCOMPOSE-1-closure-void-unexecutable.md",
    "Q-6JCOMPOSE-2-closure-void-c2-red-gate-unreachable.md",
    "Q-BOOKFIT-1-closure-resolved.md",
    "Q-BUSTGATE-1-closure-falsified.md",
    "Q-C1PANEL-1-closure-ambiguous.md",
    "Q-CAPALLOC-2-closure-resolved-fragile.md",
    "Q-COMPOSE-1-closure-falsified.md",
    "Q-COSTGEO-1-closure-ambiguous.md",
    "Q-COSTGEO-2-closure-aborted.md",
    "Q-COSTGEO-3-closure-ambiguous-needs-depth.md",
    "Q-FUNNEL-1-closure-resolved.md",
    "Q-GATECART-1-survivor-gate-cartography.md",
    "Q-GEOFIT-1-closure-ambiguous-parameterization.md",
    "Q-HARV-0-month-end-rebalance-ES.md",
    "Q-ICT-1-closure-moot.md",
    "Q-INVENTORY-1-closure-falsified.md",
    "Q-JOINT-TAIL-WEEKLY-closure-retired.md",
    "Q-KBUDGET-1-axis-reachability-screen.md",
    "Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md",
    "Q-OBJCOHERE-1-closure-falsified-coherent.md",
    "Q-PYRPARITY-1-closure-falsified-nonproportional.md",
    "Q-RAIL-1-closure-resolved.md",
    "SLR-MYM-1-closure-falsified-stage0.md",
    "ST-EH-1-closure-operator-stopped.md",
})

# Campaign IDs that claimed a terminal verdict without a joinable closure
# record at the coverage-limb promote-to-HARD ADR's authoring baseline
# (2026-08-12). Empty: PR #745 cleared the backlog 9 → 0 (SESSIONS
# 2026-08-11v). Permanent forward-only boundary — never append to dodge;
# a genuine newly discovered pre-promotion gap needs a superseding ADR.
COVERAGE_GRANDFATHERED: frozenset[str] = frozenset()

# Closures on disk at the registry-feed land (2026-08-15). Forward-only —
# new closures must carry a Registry line. Never append here to dodge;
# a new file complies instead. Why this set exists: the 2026-08-03→08-11
# kill run produced ~15 closures with zero rejected_candidates rows because
# Iterate/Board-write were gated and the registry append was checklist-only.
#
# 2026-08-15 (governance-belt audit action 4): split from one 66-name set
# into two, classified by reading each closure's actual **Verdict:** line —
# not its filename — because filename suffixes disagree with substance often
# enough to matter (e.g. "...costgeo-2-closure-aborted.md" reads FALSIFIED-
# shaped but is a $0 data-cost-estimate abort with zero candidate ever
# proposed; "...tnec-env-1-closure.md" reads NULL/STOP-shaped but is a
# zero-seed-grade harvest sweep, not a tested-and-killed mechanism). Both
# sets remain exempt from the mechanical gate (REGISTRY_GRANDFATHERED below
# is their union) — the split is a triage aid, not a gate-behavior change.
#
# REGISTRY_GRANDFATHERED_NA — genuinely n/a. RESOLVED / governance / VOID /
# AMBIGUOUS(-HOLD) / a premise that was never tested (empty intake, zero
# candidates, a sanity-check that failed before authoring, an operator stop
# reached "pre-adjudication" with no H1/H2 verdict ever computed). None of
# these assert a mechanism was tried and found not to work.
REGISTRY_GRANDFATHERED_NA = frozenset({
    "2026-07-16-striker-mym-reconstruction-candidate-1-ambiguous.md",
    "2026-07-27-hermes-agent-adoption-closure-resolved.md",
    "GSUB-1-closure-resolved-loadbearing.md",
    "MNQBASE-1-closure-intake-dry.md",
    "MSL-S7-closure-resolved-e1-hold.md",
    "Q-6JCOMPOSE-1-closure-void-unexecutable.md",
    "Q-6JCOMPOSE-2-closure-void-c2-red-gate-unreachable.md",
    "Q-BOOKFIT-1-closure-resolved.md",
    "Q-C1PANEL-1-closure-ambiguous.md",
    "Q-CAPA-1-closure-resolved.md",
    "Q-CAPALLOC-2-closure-resolved-fragile.md",
    "Q-COSTGEO-1-closure-ambiguous.md",
    "Q-COSTGEO-2-closure-aborted.md",
    "Q-COSTGEO-3-closure-ambiguous-needs-depth.md",
    "Q-FUNNEL-1-closure-resolved.md",
    "Q-GEOFIT-1-closure-ambiguous-parameterization.md",
    "Q-HARV-0-month-end-rebalance-ES.md",
    "Q-ICT-1-closure-moot.md",
    "Q-ICT-CASCADE-1-closure-insufficient-n.md",
    "Q-JOINT-TAIL-WEEKLY-closure-retired.md",
    "Q-KBUDGET-1-axis-reachability-screen.md",
    "Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md",
    "Q-MNQSEL-2-closure-resolved.md",
    "Q-OFCHAN-1-closure-void-coverage.md",
    "Q-R2AGRUN-1-closure-ambiguous-hold.md",
    "Q-RAIL-1-closure-resolved.md",
    "Q-TNEC-CON-2-closure-ambiguous-hold.md",
    "Q-TNEC-CON-3-closure-ambiguous-hold.md",
    "Q-TNEC-CON-4-closure-ambiguous-hold.md",
    "Q-TNEC-CON-5-closure-ambiguous-hold.md",
    "Q-TNEC-ENV-1-closure.md",
    "Q-USOIL-1-closure-subtract.md",
    "ST-EH-1-closure-operator-stopped.md",
})

# REGISTRY_DEBT_2026_08 — strategy-grounds kills (FALSIFIED / DEAD / STOP /
# STAGE-1 FAIL / OPERATOR-KILL, or a SCREEN-FAIL whose own text states the
# mechanism has no edge / doesn't clear costs — same substance, caught at an
# earlier stage) that owe a `rejected_candidates.md` row and never got one.
# Each row's own re-proposal bar (new mechanism evidence, not new packaging)
# depends on this registry actually naming what was tried — see STATE.md's
# "registry backfill debt" row. Backfilling is operator-paced, one row is
# one judgment call on how to phrase the heading; this set only says which
# 33 closures still owe that call, not what the heading should say.
REGISTRY_DEBT_2026_08 = frozenset({
    "2026-07-16-aegis-6j-prop-reconstruction-stage1-falsified.md",
    "2026-07-16-aegis-6j-prop-reconstruction-stage2-hsolo-falsified.md",
    "2026-07-16-striker-mym-reconstruction-candidate-2-falsified.md",
    "2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md",
    "2026-08-12-q-txg-1-striker-mnq-cell-dead-nsurv.md",
    "2026-08-12-q-txg-1-striker-nas100-mym-cell-dead-cost.md",
    "H-FBEIA-1-closure-screen-fail.md",
    "H-FCCARRY-1-closure-screen-fail.md",
    "H-ZNAUC-1-closure-screen-fail.md",
    "MSL-C1-closure-falsified.md",
    "MSL-C2-closure-falsified.md",
    "MSL-C3-closure-operator-kill.md",
    "MSL-C3-K2-closure-falsified.md",
    "MSL-S2A-closure-falsified.md",
    "MSL-S2B-closure-stage1-fail-route.md",
    "MYM-3FPS-1-closure-falsified.md",
    "OPENPRESS-1-closure-falsified.md",
    "Q-BUSTGATE-1-closure-falsified.md",
    "Q-CAPFLOW-1-closure-falsified.md",
    "Q-COMPOSE-1-closure-falsified.md",
    "Q-GATECART-1-survivor-gate-cartography.md",
    "Q-INVENTORY-1-closure-falsified.md",
    "Q-MCLTAS-1-closure-falsified.md",
    "Q-MNQDTL-CON-1-closure-falsified.md",
    "Q-MNQSEL-1-closure-falsified.md",
    "Q-OBJCOHERE-1-closure-falsified-coherent.md",
    "Q-PYRPARITY-1-closure-falsified-nonproportional.md",
    "Q-R2FLOW-1-closure-falsified.md",
    "Q-R2VBUCK-1-closure-falsified.md",
    "Q-SCORE-1-closure-falsified.md",
    "Q-TVCOV-1-closure-falsified.md",
    "Q-TXG-1-closure-falsified-at-walls.md",
    "SLR-MYM-1-closure-falsified-stage0.md",
})

# Union — the mechanical gate's exemption set. Every name above, either
# bucket. Do not append here directly; append to the correct sub-set.
REGISTRY_GRANDFATHERED = REGISTRY_GRANDFATHERED_NA | REGISTRY_DEBT_2026_08


def _strip_fences(lines: list[str]) -> list[str]:
    """Return `lines` with fenced code-block content AND delimiters removed."""
    out: list[str] = []
    in_fence = False
    marker = ""
    for line in lines:
        m = FENCE_DELIM.match(line)
        if m:
            if not in_fence:
                in_fence, marker = True, m.group(1)
            elif m.group(1) == marker:
                in_fence, marker = False, ""
            continue
        if not in_fence:
            out.append(line)
    return out


def adr_status(adr_path: Path = OWNING_ADR) -> str:
    """Return the owning ADR's Status token, or 'MISSING' if unreadable.

    A leading YAML frontmatter block is skipped; after that, only the header
    region is scanned (up to the first '## ' or '---' line), matching
    check_adr_graph.py's boundary so an addendum Status line never re-arms or
    disarms the gate."""
    try:
        lines = adr_path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return "MISSING"
    start = 0
    if lines and re.match(r"^---\s*$", lines[0]):  # YAML frontmatter
        for i in range(1, len(lines)):
            if re.match(r"^---\s*$", lines[i]):
                start = i + 1
                break
    for line in lines[start:]:
        if line.startswith("## ") or re.match(r"^---\s*$", line):
            break
        m = STATUS_LINE.match(line)
        if m:
            return m.group("tok")
    return "MISSING"


def scan_file(path: Path) -> str | None:
    """Return a violation message, or None if the closure is compliant.

    Fenced content is stripped first; the Next/Board searches are scoped to
    the region AFTER the Iterate heading when one exists, so a prose mention
    above the block can neither satisfy nor shadow the real fields."""
    try:
        raw = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:  # unreadable -> warn, never hard-fail the gate
        print(f"WARN closure-disposition: cannot read {path}: {exc}")
        return None

    try:
        shown = path.relative_to(REPO)
    except ValueError:  # test fixtures / out-of-tree paths
        shown = path

    lines = _strip_fences(raw)
    problems: list[str] = []

    heading_idx = next(
        (i for i, l in enumerate(lines) if ITERATE_HEADING.match(l)), None
    )
    if heading_idx is None:
        problems.append("no 'Iterate' heading")
        region = lines  # still report the other gaps precisely
    else:
        region = lines[heading_idx + 1:]

    branch_line: str | None = None
    for l in region:
        m = NEXT_LINE.match(l)
        if m and BRANCH_TOKEN.search(m.group("rest")):
            branch_line = m.group("rest")
            break
    if branch_line is None:
        problems.append("no 'Next:' line with an INTEGRATE/ITERATE/STOP token")
    elif PLACEHOLDER.search(branch_line):
        problems.append(
            "'Next:' line still carries separator-joined branch tokens "
            "(unfilled template placeholder — pick exactly one)"
        )

    if not any(BOARD_TOKEN.search(l) for l in region):
        problems.append("no 'Board write' line (verbatim pointer, or "
                        "'none — STOP, nothing owed')")

    if not problems:
        return None
    return (
        f"{shown}: closure lacks its typed Iterate block — {'; '.join(problems)} "
        f"(template: .claude/skills/brief-authoring/references/closure_record.md; "
        f"ADR 2026-08-04-iterate-closure-exit-mandatory)"
    )


def scan_registry(path: Path) -> str | None:
    """Return a violation if a non-grandfathered closure lacks Registry.

    Token-only (same posture as Board write). `n/a — <reason>` is legal.
    Heading-join quality is judgment — not this gate.
    """
    if path.name in REGISTRY_GRANDFATHERED:
        return None
    try:
        raw = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        print(f"WARN closure-disposition: cannot read {path}: {exc}")
        return None
    try:
        shown = path.relative_to(REPO)
    except ValueError:
        shown = path
    lines = _strip_fences(raw)
    heading_idx = next(
        (i for i, l in enumerate(lines) if ITERATE_HEADING.match(l)), None
    )
    region = lines[heading_idx + 1:] if heading_idx is not None else lines
    if any(REGISTRY_TOKEN.match(l) for l in region):
        return None
    return (
        f"{shown}: closure lacks a Registry line "
        "(`Registry: rejected_candidates.md — ### heading` or "
        "`Registry: n/a — <reason>`). The 2026-08-03 feed-stop happened "
        "because this append was checklist-only."
    )


def in_scope(closures_dir: Path = CLOSURES_DIR) -> list[Path]:
    if not closures_dir.is_dir():
        return []
    return sorted(
        p for p in closures_dir.glob("*.md") if p.name not in GRANDFATHERED
    )


# ── coverage limb ─────────────────────────────────────────────

@dataclass(frozen=True)
class ClaimedClosed:
    """A campaign ID that claims a terminal verdict somewhere load-bearing."""

    campaign_id: str
    source: str  # e.g. "INDEX Open", "INDEX Recently closed", "CATALOG"


@dataclass(frozen=True)
class MissingClosure:
    campaign_id: str
    sources: tuple[str, ...]


def campaign_id_from_closure_filename(name: str) -> str | None:
    """Extract a campaign ID from a closure filename, or None if unjoinable.

    Date-prefixed reconstruction closures (2026-07-16-aegis-…) return None —
    they are not Q-roster join keys. Grandfathered Iterate exemption is
    orthogonal: those files still count as closure records when joinable.
    """
    stem = name[:-3] if name.endswith(".md") else name
    m = CLOSURE_FILENAME_STANDARD.match(stem)
    if m:
        return m.group(1)
    m = CLOSURE_FILENAME_NONSTANDARD.match(stem)
    if m:
        return m.group(1)
    return None


def ltm_closure_corpus_present(ltm_briefs_dir: Path = LTM_BRIEFS_DIR) -> bool:
    """True iff this checkout has joinable LTM closure files.

    Public seed excludes ``docs/ltm/**`` (2026-08-14 transition ADR). A later
    restore of a non-closure artifact under ``docs/ltm/briefs/`` (e.g. the
    2026-08-21 ``rnd-pipeline/discovery-campaign-template.md``) creates the
    directory without the historical Q-* corpus. Directory existence is not
    corpus presence — the same six campaigns ``b7eb60d`` waived when the
    directory was absent.
    """
    if not ltm_briefs_dir.is_dir():
        return False
    return any(
        campaign_id_from_closure_filename(path.name)
        for path in ltm_briefs_dir.glob("*.md")
    )


def closure_campaign_ids_on_disk(
    *,
    closures_dir: Path = CLOSURES_DIR,
    ltm_briefs_dir: Path = LTM_BRIEFS_DIR,
) -> set[str]:
    """Campaign IDs that have at least one closure file on disk.

    Scans docs/briefs/closures/ and docs/ltm/briefs/ (older closures; INDEX
    notes this split). Grandfathered names are included — coverage asks
    'does a record exist?', not 'does it carry Iterate tokens?'.
    """
    ids: set[str] = set()
    for directory in (closures_dir, ltm_briefs_dir):
        if not directory.is_dir():
            continue
        for path in directory.glob("*.md"):
            cid = campaign_id_from_closure_filename(path.name)
            if cid:
                ids.add(cid)
    return ids


def claimed_closed_campaigns_from_index(text: str) -> list[ClaimedClosed]:
    """Parse INDEX.md for campaigns claiming a filed terminal verdict.

    Open table: Status column must carry CLOSED / FALSIFIED / VOID /
    AMBIGUOUS-… (etc.). Bare RESOLVED, RESOLVED-ABSENT, OPEN, DRAFT, and
    DORMANT are not closure-bearing. Recently closed: every bold campaign
    ID is claimed-closed by section membership. Dormant section: skipped.
    """
    claimed: list[ClaimedClosed] = []
    section: str | None = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if re.match(r"^##\s+Open\b", line):
            section = "open"
            continue
        if re.match(r"^##\s+Dormant\b", line):
            section = "dormant"
            continue
        if re.match(r"^##\s+Recently closed\b", line):
            section = "recent"
            continue
        if re.match(r"^##\s+", line):
            section = None
            continue
        if section == "dormant" or section is None:
            continue

        if section == "open":
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) < 2:
                continue
            q_cell, status_cell = cells[0], cells[1]
            if q_cell.lower() == "q" or status_cell.lower() == "status":
                continue
            m = BOLD_CAMPAIGN_ID.search(q_cell)
            if not m:
                continue
            cid = m.group("id")
            if NON_CLOSURE_BEARING.search(status_cell):
                continue
            if OPEN_STATUS_PRIMARY.search(status_cell):
                continue
            if not OPEN_TABLE_TERMINAL.search(status_cell):
                continue
            claimed.append(ClaimedClosed(cid, "INDEX Open"))
            continue

        if section == "recent":
            # Bullets may wrap; collect bold IDs on any line in the section.
            if not (line.lstrip().startswith("-") or line.startswith("  ")):
                # Still allow wrapped continuation lines that carry a bold ID.
                if "**" not in line:
                    continue
            for m in BOLD_CAMPAIGN_ID.finditer(line):
                claimed.append(
                    ClaimedClosed(m.group("id"), "INDEX Recently closed")
                )
    return claimed


def claimed_closed_campaigns_from_catalog(text: str) -> list[ClaimedClosed]:
    """Parse lab/CATALOG.md for Q-IDs named alongside a terminal stamp.

    Only rows that both (a) mention a campaign ID and (b) carry CLOSED /
    FALSIFIED / archive-owed language are claimed. Slug-only archived rows
    without a Q-ID are unreachable joins and are skipped (no false positive
    from inventing IDs from slugs).
    """
    claimed: list[ClaimedClosed] = []
    table: str | None = None
    for raw in text.splitlines():
        line = raw.strip()
        if re.match(r"^##\s+Active\b", line):
            table = "active"
            continue
        if re.match(r"^##\s+Archived\b", line):
            table = "archived"
            continue
        if re.match(r"^##\s+", line):
            table = None
            continue
        if table is None or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not cells or cells[0].lower() == "slug":
            continue
        row_text = " | ".join(cells)
        if table == "archived":
            # Archived table: any named Q-ID is a closed campaign claim.
            terminal = True
        else:
            terminal = bool(CATALOG_TERMINAL.search(row_text))
        if not terminal:
            continue
        for m in LOOSE_CAMPAIGN_ID.finditer(row_text):
            claimed.append(ClaimedClosed(m.group("id"), "CATALOG"))
    return claimed


def missing_closure_campaigns(
    repo: Path = REPO,
    *,
    grandfathered: frozenset[str] = COVERAGE_GRANDFATHERED,
) -> list[MissingClosure]:
    """Return terminal-verdict campaigns that have no closure record on disk.

    Campaign IDs in `grandfathered` (COVERAGE_GRANDFATHERED by default) are
    excluded — historical gaps stay WARN-exempt / silent so a HARD coverage
    fire never blocks unrelated work on pre-promotion debt.
    """
    index_path = repo / "docs" / "briefs" / "INDEX.md"
    catalog_path = repo / "lab" / "CATALOG.md"
    closures_dir = repo / "docs" / "briefs" / "closures"
    ltm_dir = repo / "docs" / "ltm" / "briefs"

    claimed: list[ClaimedClosed] = []
    if index_path.is_file():
        try:
            claimed.extend(
                claimed_closed_campaigns_from_index(
                    index_path.read_text(encoding="utf-8")
                )
            )
        except OSError as exc:
            print(f"WARN closure-disposition: cannot read {index_path}: {exc}")
    if catalog_path.is_file():
        try:
            claimed.extend(
                claimed_closed_campaigns_from_catalog(
                    catalog_path.read_text(encoding="utf-8")
                )
            )
        except OSError as exc:
            print(f"WARN closure-disposition: cannot read {catalog_path}: {exc}")

    on_disk = closure_campaign_ids_on_disk(
        closures_dir=closures_dir, ltm_briefs_dir=ltm_dir
    )

    if not ltm_closure_corpus_present(ltm_dir):
        # Public seed excludes docs/ltm/** (2026-08-14 transition ADR). A
        # campaign whose closure lives only there is unverifiable here, not
        # missing — same posture as check_adr_graph.py's A3 check. Directory
        # existence is not enough: a nested non-closure restore must not
        # re-arm HARD coverage against an absent corpus (b7eb60d class).
        return []

    by_id: dict[str, list[str]] = {}
    for c in claimed:
        by_id.setdefault(c.campaign_id, []).append(c.source)

    missing: list[MissingClosure] = []
    for cid, sources in sorted(by_id.items()):
        if cid in on_disk:
            continue
        if cid in grandfathered:
            continue
        # Deduplicate source labels while preserving order.
        uniq: list[str] = []
        for s in sources:
            if s not in uniq:
                uniq.append(s)
        missing.append(MissingClosure(cid, tuple(uniq)))
    return missing


def report_missing_closure_coverage(
    missing: list[MissingClosure],
    *,
    hard: bool = False,
) -> int:
    """Print coverage findings. Returns 1 iff hard and any missing, else 0."""
    if not missing:
        return 0
    tier = "HARD" if hard else "WARN"
    posture = (
        "coverage limb armed HARD "
        "(ADR 2026-08-12-closure-disposition-coverage-hard Accepted)"
        if hard
        else (
            "advisory while coverage ADR is Proposed — "
            "Accepted flips this limb HARD "
            "(lesson_green_gate_is_not_coverage; "
            "ADR 2026-08-12-closure-disposition-coverage-hard)"
        )
    )
    print(
        f"{tier} closure-disposition coverage: {len(missing)} campaign(s) claim "
        "a terminal verdict with no closure record under docs/briefs/closures/ "
        f"or docs/ltm/briefs/ ({posture}):"
    )
    for m in missing:
        src = ", ".join(m.sources)
        print(f"  - {m.campaign_id}  [{src}]")
    return 1 if hard else 0


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv

    if argv and argv[0] == "--list-debt":
        # 2026-08-15 (governance-belt audit action 4): operator triage list
        # for REGISTRY_DEBT_2026_08 -- closures that owe a rejected_candidates
        # row and never got one. Report-only; does not touch closure files or
        # rejected_candidates.md itself.
        names = sorted(REGISTRY_DEBT_2026_08)
        print(f"check_closure_disposition: {len(names)} closure(s) owe a "
              "rejected_candidates.md row (REGISTRY_DEBT_2026_08):")
        for name in names:
            print(f"  - {name}")
        return 0

    if argv:  # explicit-path mode: authoring-time, always hard (Iterate only)
        violations: list[str] = []
        for a in argv:
            p = Path(a)
            # Grandfathered closures stay exempt here too — hard-failing them
            # would invite exactly the retro-editing the ADR's §5 forbids.
            try:
                grandfathered = (p.resolve().parent == CLOSURES_DIR.resolve()
                                 and p.name in GRANDFATHERED)
            except OSError:
                grandfathered = False
            if grandfathered:
                print(f"SKIP closure-disposition: {p.name} is grandfathered "
                      "(pre-ADR closure; forward-only mandate)")
                continue
            if (msg := scan_file(p)):
                violations.append(msg)
            if (msg := scan_registry(p)):
                violations.append(msg)
        for v in violations:
            print(f"HARD closure-disposition: {v}")
        if violations:
            return 1
        print("check_closure_disposition: OK — Iterate block tokens present.")
        return 0

    iterate_status = adr_status(OWNING_ADR)
    iterate_hard = iterate_status == "Accepted"
    violations = [msg for f in in_scope() if (msg := scan_file(f))]
    registry_violations = [
        msg for f in in_scope() if (msg := scan_registry(f))
    ]

    coverage_status = adr_status(COVERAGE_OWNING_ADR)
    coverage_hard = coverage_status == "Accepted"
    missing = missing_closure_campaigns()

    if iterate_status == "MISSING":
        print("WARN closure-disposition: owning ADR "
              "2026-08-04-iterate-closure-exit-mandatory.md missing or has no "
              "parseable Status token — Iterate limb degraded to WARN. If the "
              "ADR was renamed, update OWNING_ADR here in the same commit.")
    if coverage_status == "MISSING":
        print("WARN closure-disposition: coverage ADR "
              "2026-08-12-closure-disposition-coverage-hard.md missing or has "
              "no parseable Status token — coverage limb degraded to WARN. If "
              "the ADR was renamed, update COVERAGE_OWNING_ADR here in the "
              "same commit.")

    iterate_exit = 0
    if violations:
        tier = "HARD" if iterate_hard else "WARN"
        for v in violations:
            print(f"{tier} closure-disposition: {v}")
        if iterate_hard:
            print(f"check_closure_disposition: {len(violations)} violation(s).")
            iterate_exit = 1
        else:
            print(f"check_closure_disposition: {len(violations)} warning(s) — "
                  f"Iterate limb is WARN-tier while the owning ADR is "
                  f"`{iterate_status}`; it hard-fails once `Accepted`.")
    else:
        print("check_closure_disposition: OK — every non-grandfathered closure "
              "carries its typed Iterate block.")

    # Registry limb rides the Iterate ADR's severity (same closure file,
    # same authoring moment). Grandfathered names are already skipped.
    if registry_violations:
        tier = "HARD" if iterate_hard else "WARN"
        for v in registry_violations:
            print(f"{tier} closure-disposition registry: {v}")
        if iterate_hard:
            iterate_exit = 1
    else:
        print("check_closure_disposition: OK — every post-2026-08-15 closure "
              "carries a Registry line.")

    coverage_exit = report_missing_closure_coverage(
        missing, hard=coverage_hard
    )
    return 1 if (iterate_exit or coverage_exit) else 0


if __name__ == "__main__":
    sys.exit(main())
