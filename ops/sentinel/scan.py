"""INQHIORI Sentinel — Tier-1 deterministic scanners (no LLM, report-only).

Reads repo files and emits Findings. Fails open: a parse miss yields no finding,
never a false positive. The quarterly LLM probe is the general backstop.

Design: docs/spec/2026-06-23-inqhiori-sentinel-design.md
"""
from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

ROUTING = ("Action", "Forward", "Closed")


@dataclass(frozen=True)
class Finding:
    id: str
    category: str       # "skew"|"obligation"|"precondition"|"hygiene"|"memory"|"prereg"
    routing: str        # one of ROUTING
    summary: str
    source: str         # "path:line" or "path"
    next_step: str


def _read(root: Path, rel: str) -> str:
    p = root / rel
    return p.read_text(encoding="utf-8") if p.exists() else ""


def _line_of(text: str, needle: str) -> int:
    for i, line in enumerate(text.splitlines(), 1):
        if needle in line:
            return i
    return 0


def _md_section(text: str, heading_prefix: str, marker: str = "## ") -> tuple[str, int]:
    """Return (section body, 1-based start line) for `{marker}{heading_prefix}…`.

    Body runs until the next heading at the SAME marker level or EOF. Empty
    string / 0 if missing. `marker` defaults to `"## "` (existing callers);
    pass `"### "` for STATE.md's date subheadings.
    """
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith(marker) and heading_prefix in line[len(marker):]:
            start = i
            break
    if start is None:
        return "", 0
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith(marker):
            end = j
            break
    return "\n".join(lines[start:end]), start + 1


# Year-row Tag column still at [M] or [L] (ignore prose that mentions those tokens).
_UNVERIFIED_REGIME_TAG = re.compile(r"^\|\s*20\d{2}.*\|\s*\[([ML])\]\s*\|?\s*$")


# --------------------------------------------------------------------------- #
# skew_scan
# --------------------------------------------------------------------------- #

# Registry of "retraction skews": a canonical claim whose source-of-truth has
# superseded/retracted it but whose canonical line carries no caveat token.
# v1 ships the one proven case (C1); add entries here (<=6) as new skews are found.
_RETRACTION_CHECKS = (
    {
        "id": "SKEW-headroom-fixed1r",
        "canonical_needle": "p99 DD 0.63pp headroom",
        "history_needles": ("provisionally retracted", "fixed-1R"),
        "caveat_token": "fixed-1R",
        "summary": (
            "CLAUDE.md asserts 'p99 DD 0.63pp headroom' with no fixed-1R caveat, but "
            "docs/mc_anchor_history.md (Q-SWAP-2) provisionally retracted that margin to "
            "0.45pp under fixed-1R modeling (M-SWAP-1). Lock criterion still passes (4.55% < 5%)."
        ),
        "next_step": (
            "Append a fixed-1R caveat + Q-SWAP-2 cross-ref to the headroom line at CLAUDE.md, "
            "mirroring the regime and gross-of-swap caveats already inline."
        ),
    },
)


def skew_scan(root: Path) -> list[Finding]:
    """Detect canonical claims whose source-of-truth retracted them, uncaveated."""
    findings: list[Finding] = []
    claude = _read(root, "CLAUDE.md")
    history = _read(root, "docs/mc_anchor_history.md")
    lines = claude.splitlines()
    for chk in _RETRACTION_CHECKS:
        needle = chk["canonical_needle"]
        if needle not in claude:
            continue
        if not all(h in history for h in chk["history_needles"]):
            continue
        ln = _line_of(claude, needle)
        canonical_line = lines[ln - 1] if 0 < ln <= len(lines) else ""
        if chk["caveat_token"] in canonical_line:
            continue  # already caveated on the claim line -> remediated
        findings.append(Finding(
            id=chk["id"], category="skew", routing="Action",
            summary=chk["summary"], source=f"CLAUDE.md:{ln}", next_step=chk["next_step"],
        ))
    return findings


# --------------------------------------------------------------------------- #
# obligation_scan
# --------------------------------------------------------------------------- #

# Files where dated obligations legitimately live. Curated to avoid ADR-date noise.
# USDCAD ledger: only the Regime calendar section (session log has many ISO dates).
_OBLIGATION_FILES = (
    "CLAUDE.md",
    "docs/notes/audits/rule-2-trip-log.md",
)
_USDCAD_LEDGER = "ops/instruments/USDCAD.md"
_REGIME_CAL_HEADING = "Regime calendar"
_OBLIGATION_KW = ("next", "trigger", "review", "due", "slate", "audit", "gate", "quarterly")
_ISO_DATE = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")

# ADR trigger-schedule surface (2026-08-03, gate-stack audit X2/X3).
#
# The design spec (docs/spec/2026-06-23-inqhiori-sentinel-design.md §4.1) named
# `docs/adr/*` as one of five obligation_scan surfaces. The IMPLEMENTATION PLAN
# (docs/spec/2026-06-23-inqhiori-sentinel-plan.md, Step 3 code block) already
# narrowed that to three files, dropping docs/adr/* silently -- _OBLIGATION_FILES
# above is a faithful build of the PLAN, not a code-vs-plan bug. The plan is a
# spent, dated artifact; corrected here at the point future sessions will read
# it (this comment + the design-spec addendum), not by rewriting the plan's
# historical text.
#
# Naive per-line keyword+date scanning of 100 ADR files reproduces exactly the
# "ADR-date noise" the original curation comment warns against: 48 of them
# mention 2026-08-08 somewhere (verified 2026-08-03, `rg -l 2026-08-08
# docs/adr/*.md | wc -l`), and most of that text is incidental (commit dates,
# Change-history rows, §0 verification stamps) -- not a trigger. So this scan
# is restricted to the ADR template's own canonical field (brief-authoring
# references/adr.md §4/§10): a `**Trigger check schedule:**` / `**Check
# schedule:**` line, plus up to 3 bounded continuation lines (the field wraps
# on long entries -- e.g. 2026-08-03-lifecycle-ladder-intermediate-rung.md:143).
#
# The gate-stack audit's X3 finding was that ~29 of those fields name a
# convening vehicle using 7 different phrasings ("quarterly programme audit",
# "quarterly review", "quarterly regime check", "checkpoint", "progress
# check", "quarterly slate(s)", "forward-trigger review"), and framed
# normalizing those 7 names as a PREREQUISITE for any fix ("a regex cannot
# bind an event spelled seven ways"). Re-checked here (2026-08-03): those
# phrasings do NOT all denote the identical mechanism -- several ADRs
# distinguish "programme-audit slate" from "portfolio regime trigger" as
# separate, merely CO-SCHEDULED cadences (e.g. 2026-06-22-cost-geometry-pregate.md:82
# "alongside the standing regime + instrument-ledger triggers"). Building a
# vehicle-alias table that treats them as one object would be the false
# equivalence the D-S-A gate's forbidden-test discipline exists to catch.
#
# This scan sidesteps vehicle-name matching entirely: it doesn't need to know
# WHAT convenes on a date, only THAT a trigger field names that date, then lets
# a downstream check (precondition_scan's board-sync block) ask whether the
# board reflects it. No normalization table needed.
_ADR_TRIGGER_FIELD = re.compile(r"^\*\*(?:Trigger check schedule|Check schedule):\*\*\s*(.*)$")
_ADR_NEW_FIELD = re.compile(r"^\*\*[A-Za-z][^*]*:\*\*")
_ADR_DATE_PREFIX = re.compile(r"^\d{4}-\d{2}-\d{2}-.+\.md$")


def _adr_files(root: Path) -> list[str]:
    """Sorted `docs/adr/*.md` relative paths, excluding non-dated files (INDEX.md)."""
    d = root / "docs" / "adr"
    if not d.is_dir():
        return []
    return sorted(
        f"docs/adr/{p.name}" for p in d.iterdir()
        if p.is_file() and _ADR_DATE_PREFIX.match(p.name)
    )


def _adr_trigger_field_span(text: str) -> tuple[str, int]:
    """Return (joined trigger-field text, 1-based start line), or ("", 0).

    Captures the `**Trigger check schedule:**` / `**Check schedule:**` line
    plus up to 3 continuation lines, stopping at a blank line, a new bold
    field, or a `---` rule -- bounded so a wrapped date doesn't get missed
    without risking a runaway match into unrelated prose.
    """
    lines = text.splitlines()
    for i, line in enumerate(lines):
        m = _ADR_TRIGGER_FIELD.match(line.strip())
        if not m:
            continue
        span = [m.group(1)]
        for j in range(i + 1, min(i + 4, len(lines))):
            nxt = lines[j].strip()
            if not nxt or nxt == "---" or _ADR_NEW_FIELD.match(nxt):
                break
            span.append(nxt)
        return " ".join(span), i + 1
    return "", 0


def _adr_trigger_dates(root: Path, asof: date, horizon: date) -> dict[str, list[tuple[str, int]]]:
    """Map ISO date -> [(adr_relpath, line_no), ...] for ADR trigger-field dates
    within [asof, horizon]. One ADR can contribute to multiple dates (a field
    naming "2026-08-08, then 2026-11-08" is two real, distinct obligations)."""
    by_date: dict[str, list[tuple[str, int]]] = {}
    for rel in _adr_files(root):
        text = _read(root, rel)
        span, ln = _adr_trigger_field_span(text)
        if not span:
            continue
        for m in _ISO_DATE.finditer(span):
            try:
                d = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            except ValueError:
                continue
            if not (asof <= d <= horizon):
                continue
            by_date.setdefault(d.isoformat(), []).append((rel, ln))
    return by_date


def obligation_scan(root: Path, asof: date, horizon_days: int = 60) -> list[Finding]:
    """Flag dated obligations within `horizon_days` of `asof`."""
    findings: list[Finding] = []
    horizon = asof + timedelta(days=horizon_days)
    seen: set[tuple[str, str]] = set()

    def _scan_text(rel: str, text: str, line_offset: int = 1) -> None:
        for i, line in enumerate(text.splitlines()):
            ln = line_offset + i
            low = line.lower()
            if not any(kw in low for kw in _OBLIGATION_KW):
                continue
            for m in _ISO_DATE.finditer(line):
                try:
                    d = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
                except ValueError:
                    continue
                if not (asof <= d <= horizon):
                    continue
                key = (rel, d.isoformat())
                if key in seen:
                    continue
                seen.add(key)
                days = (d - asof).days
                findings.append(Finding(
                    id=f"OBLIG-{d.isoformat()}",
                    category="obligation", routing="Action" if days <= 14 else "Forward",
                    summary=f"Dated obligation {d.isoformat()} is {days}d out — \"{line.strip()[:100]}\"",
                    source=f"{rel}:{ln}",
                    next_step="Confirm the obligation is scheduled and its inputs are ready (see precondition findings).",
                ))

    for rel in _OBLIGATION_FILES:
        _scan_text(rel, _read(root, rel))

    ledger = _read(root, _USDCAD_LEDGER)
    if ledger:
        section, start_ln = _md_section(ledger, _REGIME_CAL_HEADING)
        if section:
            _scan_text(_USDCAD_LEDGER, section, line_offset=start_ln)

    # docs/adr/* trigger-schedule fields, aggregated by date (see the module
    # comment above _ADR_TRIGGER_FIELD for why this is date-aggregated rather
    # than per-file: one row per matching ADR would be exactly the ADR-date
    # noise this scan was originally curated to avoid).
    by_date = _adr_trigger_dates(root, asof, horizon)
    for d_iso, hits in sorted(by_date.items()):
        rels = sorted({rel for rel, _ln in hits})
        d = date.fromisoformat(d_iso)
        days = (d - asof).days
        sample = ", ".join(rels[:3]) + (f", +{len(rels) - 3} more" if len(rels) > 3 else "")
        findings.append(Finding(
            id=f"OBLIG-adr-triggers-{d_iso}",
            category="obligation", routing="Action" if days <= 14 else "Forward",
            summary=(
                f"{len(rels)} ADR 'Trigger check schedule' field(s) name {d_iso} "
                f"({days}d out): {sample}"
            ),
            source=f"docs/adr/ ({len(rels)} file(s))",
            next_step=(
                f"rg -l \"{d_iso}\" docs/adr/*.md — cross-check against STATE.md's "
                f"### {d_iso} section (see PRECOND-board-sync findings if any)."
            ),
        ))

    return findings


# --------------------------------------------------------------------------- #
# precondition_scan
# --------------------------------------------------------------------------- #

# The next dated slate whose preconditions v1 tracks explicitly (C2). Generalizing
# precondition discovery from obligation_scan output is future work (spec §9).
# Rolled 2026-08-08 -> 2026-11-08 (weekly sentinel run, 2026-08-10): the prior
# slate DISCHARGED (STATE.md ### 2026-08-08); this constant is the only
# re-arm mechanism for the SLATE_DATE-gated precondition checks (spec addendum
# 2026-07-27) and does not advance itself.
SLATE_DATE = date(2026, 11, 8)


def _slate_verification_discharged(section: str, slate: date) -> bool:
    """True when the calendar section records THIS slate's verification pass as
    discharged. The precondition is "is the pass outstanding?", not "is every cell
    [H]?" — a discharge may deliberately leave a cell at [M]/[L] (USDCAD's 2026-07-02
    R6 pass holds 2026 YTD at [M] pending year-end). Requires the slate date on the
    line, so a discharge for a different slate does not suppress."""
    stamp = slate.isoformat()
    return any(stamp in line and "DISCHARGED" in line.upper() for line in section.splitlines())


def _board_sync_findings(root: Path, asof: date, horizon: date) -> list[Finding]:
    """Generalizes SLATE_DATE-only precondition checking to every date an ADR
    'Trigger check schedule' field names (2026-08-03, gate-stack audit X2/X3 —
    the "future work (spec §9)" the module comment above named).

    For each such date, checks how many of the contributing ADRs are actually
    referenced under STATE.md's matching `### {date}` heading. Sidesteps
    vehicle-name matching (see the _ADR_TRIGGER_FIELD comment): it only checks
    whether the SOURCE FILE is linked somewhere in that section's body, not
    whether the wording matches. Fails open — no `### {date}` heading, or an
    empty ADR-trigger set, both yield silence, never a false claim that
    something is "broken" (a discharged obligation is correctly absent from
    STATE.md; this scan cannot tell discharged from merely-unlinked, so it
    reports a gap for the operator to judge, not a verdict).
    """
    findings: list[Finding] = []
    by_date = _adr_trigger_dates(root, asof, horizon)
    if not by_date:
        return findings
    state_text = _read(root, "STATE.md")
    if not state_text:
        return findings
    for d_iso, hits in sorted(by_date.items()):
        rels = sorted({rel for rel, _ln in hits})
        section, _start_ln = _md_section(state_text, d_iso, marker="### ")
        covered = sum(1 for rel in rels if rel in section) if section else 0
        if covered >= len(rels):
            continue  # fully represented -> nothing to flag
        d = date.fromisoformat(d_iso)
        days = (d - asof).days
        where = f"STATE.md's ### {d_iso} section" if section else f"STATE.md (no ### {d_iso} heading)"
        findings.append(Finding(
            id=f"PRECOND-board-sync-{d_iso}",
            category="precondition", routing="Action" if days <= 14 else "Forward",
            summary=(
                f"{len(rels)} ADR trigger-schedule field(s) name {d_iso} ({days}d out); "
                f"{where} references only {covered} of them."
            ),
            source="STATE.md",
            next_step=(
                f"rg -l \"{d_iso}\" docs/adr/*.md, then add a STATE.md pointer row for any "
                f"still-live (undischarged) obligation under ### {d_iso}. A gap can also mean "
                f"the obligation was already discharged elsewhere — verify before adding a row."
            ),
        ))
    return findings


def precondition_scan(root: Path, asof: date, horizon_days: int = 60) -> list[Finding]:
    """Check known inputs for dated slates are ready, when the slate is within horizon."""
    findings: list[Finding] = []
    horizon = asof + timedelta(days=horizon_days)

    if asof <= SLATE_DATE <= horizon:
        cal_text = _read(root, _USDCAD_LEDGER)
        section, start_ln = _md_section(cal_text, _REGIME_CAL_HEADING) if cal_text else ("", 0)
        unverified_ln = 0
        for i, line in enumerate(section.splitlines()):
            if _UNVERIFIED_REGIME_TAG.match(line):
                unverified_ln = start_ln + i
                break
        if unverified_ln and not _slate_verification_discharged(section, SLATE_DATE):
            findings.append(Finding(
                id="PRECOND-regime-calendar-unverified", category="precondition", routing="Action",
                summary=(
                    f"USDCAD regime calendar still has unverified [M]/[L] Tag cells; a verification pass "
                    f"is due before the {SLATE_DATE.isoformat()} slate."
                ),
                source=f"{_USDCAD_LEDGER}:{unverified_ln}",
                next_step="Verify the [M]/[L] regime-calendar Tag cells (year rows) before the slate date.",
            ))

        log = _read(root, "docs/notes/audits/rule-2-trip-log.md")
        if log:
            data_rows = [l for l in log.splitlines() if re.match(r"\s*\|\s*\d{4}-\d{2}-\d{2}\s*\|", l)]
            if len(data_rows) < 2:
                findings.append(Finding(
                    id="PRECOND-rule2-triplog-starved", category="precondition", routing="Action",
                    summary=(
                        f"rule-2-trip-log.md has {len(data_rows)} data row(s); the "
                        f"{SLATE_DATE.isoformat()} programme audit's Rule-2 graduation check "
                        f"needs >=1 entry per active loop class."
                    ),
                    source="docs/notes/audits/rule-2-trip-log.md",
                    next_step="Decide the Rule-2 first-wire / trip-log policy before the slate so the graduation check runs on real inputs.",
                ))

    findings.extend(_board_sync_findings(root, asof, horizon))
    return findings


# --------------------------------------------------------------------------- #
# sessions_scan (Tier-1: session-log roll-off window)
# --------------------------------------------------------------------------- #

_SESSIONS_ENTRY = re.compile(r"^## \d{4}-\d{2}-\d{2}[a-z]? ", re.M)


def sessions_scan(root: Path, max_entries: int = 20) -> list[Finding]:
    """Flag docs/SESSIONS.md when it holds more than `max_entries` dated entries —
    a nudge to run scripts/roll_sessions.py. Counts real `## YYYY-MM-DD` headings
    only (the fenced template line uses literal YYYY). Fail-open: missing -> []."""
    text = _read(root, "docs/SESSIONS.md")
    if not text:
        return []
    n = len(_SESSIONS_ENTRY.findall(text))
    if n <= max_entries:
        return []
    return [Finding(
        id="SESSIONS-over-window",
        category="hygiene",
        routing="Forward",
        summary=(
            f"docs/SESSIONS.md has {n} entries (> {max_entries} live-window); older "
            f"entries should roll to docs/ltm/notes/archive/sessions/."
        ),
        source="docs/SESSIONS.md",
        next_step=(
            f"Run `python scripts/roll_sessions.py` to archive entries beyond the newest "
            f"{max_entries}, then commit the SESSIONS.md + archive delta."
        ),
    )]


# --------------------------------------------------------------------------- #
# memory_scan (Tier-2: auto-memory base hygiene)
# --------------------------------------------------------------------------- #
#
# The auto-memory base lives OUTSIDE the repo (~/.claude/.../memory). This scan
# takes the dir as a param and no-ops when absent, so the public repo + CI stay
# clean. It rides the Sentinel as one more report-only scan when run with
# `--memory-dir`. Checks: byte budget, index<->file bijection (both ways),
# broken [[wikilinks]], and a conservative SoT-anchored stale-MC-anchor tripwire.

_MEMORY_BUDGET_KB = 25.0
_INDEX_SLUG = re.compile(r"\]\(([A-Za-z0-9_]+)\.md\)")
_WIKILINK = re.compile(r"\[\[([A-Za-z0-9_]+)\]\]")
# Matches an MC-anchor triple "XX.XX/Y.YY/Z.ZZ" (optional % and spaces).
_ANCHOR_TRIPLE = re.compile(r"(\d{2}\.\d{2})\s*%?\s*/\s*(\d\.\d{2})\s*%?\s*/\s*(\d\.\d{2})")
_HISTORICAL_MARKERS = ("SUPERSEDED", "HISTORICAL", "superseded", "historical")


def _atomic_slugs(mem_dir: Path) -> set[str]:
    return {p.stem for p in mem_dir.glob("*.md")} - {"MEMORY"}


def _stale_anchor_findings(mem_dir: Path, files: set[str], repo_root: Path | None) -> list[Finding]:
    """Flag a memory file asserting a non-current MC anchor as 'canonical' with no
    historical marker. SoT-anchored (compares to CLAUDE.md), fail-open, conservative:
    a file carrying any SUPERSEDED/HISTORICAL marker is never flagged."""
    if repo_root is None:
        return []
    claude = repo_root / "CLAUDE.md"
    if not claude.exists():
        return []
    cm = _ANCHOR_TRIPLE.search(claude.read_text(encoding="utf-8"))
    if not cm:
        return []  # can't establish the current anchor -> say nothing
    current = cm.groups()
    out: list[Finding] = []
    for slug in sorted(files):
        text = (mem_dir / f"{slug}.md").read_text(encoding="utf-8")
        if any(marker in text for marker in _HISTORICAL_MARKERS):
            continue  # explicitly framed as history -> not a current-claim
        for line in text.splitlines():
            if "canonical anchor" not in line.lower():
                continue
            m = _ANCHOR_TRIPLE.search(line)
            if m and m.groups() != current:
                out.append(Finding(
                    id=f"MEM-stale-anchor-{slug}", category="memory", routing="Action",
                    summary=(
                        f"{slug}.md asserts MC anchor {'/'.join(m.groups())} as canonical, but "
                        f"CLAUDE.md current is {'/'.join(current)}, with no historical marker."
                    ),
                    source=f"{slug}.md",
                    next_step="Reframe as historical (add a SUPERSEDED/HISTORICAL marker) or update to the current anchor.",
                ))
                break
    return out


def memory_scan(mem_dir: Path | None, repo_root: Path | None = None,
                budget_kb: float = _MEMORY_BUDGET_KB) -> list[Finding]:
    """Lint the auto-memory base. No-ops (returns []) when mem_dir is absent or
    has no MEMORY.md index, so it is safe to wire unconditionally into the CLI."""
    if mem_dir is None or not mem_dir.is_dir():
        return []
    index_path = mem_dir / "MEMORY.md"
    if not index_path.exists():
        return []  # fail open

    findings: list[Finding] = []
    index_text = index_path.read_text(encoding="utf-8")

    kb = index_path.stat().st_size / 1024
    if kb > budget_kb:
        findings.append(Finding(
            id="MEM-budget-over", category="memory", routing="Action",
            summary=f"MEMORY.md is {kb:.1f}KB, over the {budget_kb:.0f}KB always-loaded budget.",
            source="MEMORY.md",
            next_step="Run a consolidate-memory pass: collapse repo-redundant closures to pointers, synthesize families, tighten hooks.",
        ))

    files = _atomic_slugs(mem_dir)
    indexed = set(_INDEX_SLUG.findall(index_text))
    for slug in sorted(files - indexed):
        findings.append(Finding(
            id=f"MEM-orphan-file-{slug}", category="memory", routing="Action",
            summary=f"Memory file '{slug}.md' has no MEMORY.md index line (unfindable on recall).",
            source=f"{slug}.md",
            next_step="Add an index line, or delete the file if its content has moved to a repo SoT.",
        ))
    for slug in sorted(indexed - files):
        findings.append(Finding(
            id=f"MEM-dangling-index-{slug}", category="memory", routing="Action",
            summary=f"MEMORY.md indexes '{slug}.md' but no such file exists.",
            source="MEMORY.md",
            next_step="Remove the stale index line or restore the file.",
        ))

    broken: set[tuple[str, str]] = set()
    for slug in sorted(files):
        for target in _WIKILINK.findall((mem_dir / f"{slug}.md").read_text(encoding="utf-8")):
            if target not in files:
                broken.add((slug, target))
    for src, target in sorted(broken):
        findings.append(Finding(
            id=f"MEM-broken-link-{target}", category="memory", routing="Action",
            summary=f"[[{target}]] in {src}.md does not resolve to a memory file.",
            source=f"{src}.md",
            next_step="Repoint the link to an existing slug (e.g. the meta-lesson that absorbed it).",
        ))

    findings += _stale_anchor_findings(mem_dir, files, repo_root)
    return findings


# --------------------------------------------------------------------------- #
# preregistration_scan (Tier-1: freeze-before-results commit hygiene)
# --------------------------------------------------------------------------- #
#
# Convention (operational_rules.md Rule 8 sub-rule 7): a pre-registration /
# freeze artifact must land in a SEPARATE, EARLIER commit than the results or
# closure it gates — so "frozen before the run" is git-verifiable, not
# self-attested. The 2026-07-01 programme audit (R4) found flagship pre-regs
# (Q-INCUMBENT-REGIME-1, the clean-vintage re-MC, Phase-B §0.5 locks) that
# landed in the SAME commit as their results (`efeda82`). Gold standard:
# `46f47d1` (freeze) -> `913829b` (run).
#
# This scan flags a commit that INTRODUCES a results/closure artifact and, in
# the same commit, adds-or-modifies a CORRESPONDING pre-registration artifact.
# A freeze commit that carries a prereg alongside scaffold (runner `.py`,
# `panel.csv`, `coverage.json`) is fine — only prereg+results in one commit
# trips. Correspondence is by shared question-ID stem (`Q-…-N`) or shared
# `lab/analysis/<run>/` directory. Fail-open: any git error yields no finding.
#
# Shallow clones (this remote env, CI): commits at the graft boundary have no
# reachable parent, so their real delta is invisible — they are SKIPPED (see
# `_changed_files`), not flagged on their whole tree. The audit is therefore
# only complete against a full-history clone (the operator's local checkout or
# the pre-commit hook context); on a shallow clone it covers the commits whose
# parent is present, which is the recent window that matters for a fresh nudge.
#
# NOT covered (v1, documented — no silent cap): post-freeze edits to *verdict
# code* in a run commit whose prereg markdown is a proper ancestor (the
# Q-ORB-FRIDAY-1 / `3935d2c` class — prereg `711d499` is a true ancestor there,
# so this artifact-pairing check correctly does not fire). Detecting that needs
# semantic diffing of the run script, not artifact pairing; it is a Forward
# extension.
#
# Cross-tree pairing (gate-stack audit R3, 2026-08-15): a pre-registration
# under docs/briefs/pre-registration/ now pairs with a lab/analysis (or
# lab/archive) RESULTS/FINDINGS file when they share a Q-ID in the *basename
# or file body*, or when the RESULTS body cites the prereg path/basename.
# Path-only pairing still cannot see those pairs; preregistration_scan reads
# commit blobs (fail-open) and threads them into _corresponds. The scan still
# flags the commit, not each pair.

_PREREG_DIR = "docs/briefs/pre-registration/"
# A question-ID stem: "Q-" then hyphenated ALL-CAPS/digit segments, ending at the
# first pure-digit segment (parent-question identity). Matches Q-SWAP-2,
# Q-ORB-FRIDAY-1, Q-INCUMBENT-REGIME-1, Q-ORB-T10Y3M-1; T2a/T2b sub-phase tails
# collapse to the parent id (intentional — same parent question).
_QID_RE = re.compile(r"Q-(?:[A-Z0-9]+-)*?\d+(?![A-Z0-9])")


def _basename(path: str) -> str:
    return path.rsplit("/", 1)[-1]


def _parent_dir(path: str) -> str:
    return path.rsplit("/", 1)[0] if "/" in path else ""


def _is_prereg_artifact(path: str) -> bool:
    """A pre-registration / freeze artifact by path or name.

    The name-based branch is DOCUMENTS ONLY. A pre-registration is a written,
    reviewable record; code and data outputs that merely carry the token in
    their filename are scaffold, which §4's freeze shape explicitly treats as
    clean. Anchor: `run_phase123_freeze_tstar.py` (a Q-DRIFTEX-1 runner) was
    reported as Q-DRIFTEX-1's pre-registration on the 2026-08-03 weekly run,
    against a real prereg frozen one commit earlier — see the 2026-08-03
    addendum in the design spec.
    """
    if path.startswith(_PREREG_DIR):
        return True
    if not path.lower().endswith(".md"):
        return False
    b = _basename(path).upper()
    return "PREREG" in b or "FREEZE" in b  # PREREG covers *-preregistration.md too


def _is_result_artifact(path: str) -> bool:
    """A results/closure artifact. A prereg is never counted as its own result."""
    if _is_prereg_artifact(path):
        return False
    b = _basename(path)
    if path.startswith("docs/briefs/") and "closure" in b.lower():
        return True
    if path.startswith(("lab/analysis/", "lab/archive/")) and (
        b.startswith("RESULTS") or b.startswith("FINDINGS")
    ):
        return True
    return False


def _qids(path: str, text: str | None = None) -> set[str]:
    """Question-ID stems from the basename, plus any in `text` when supplied.

    Basename-only pairing misses the G1 family: most docs/briefs/pre-registration/
    files and lab/analysis RESULTS carry no Q-ID in the filename (gate-stack
    audit R3). Body extraction is opt-in so the pure path core stays cheap.
    """
    found = set(_QID_RE.findall(_basename(path)))
    if text:
        found |= set(_QID_RE.findall(text))
    return found


def _prereg_cited_in(result_text: str, prereg_path: str) -> bool:
    """True when a RESULTS/closure body names its pre-registration path or basename."""
    if not result_text:
        return False
    if prereg_path in result_text:
        return True
    base = _basename(prereg_path)
    return bool(base) and base in result_text


def _corresponds(
    result_path: str,
    prereg_path: str,
    *,
    result_text: str | None = None,
    prereg_text: str | None = None,
) -> bool:
    """A results artifact corresponds to a prereg if they share a question-ID
    stem (basename or, when supplied, file body), share a containing directory
    (lab/analysis/<run>/ style), or the RESULTS body cites a
    docs/briefs/pre-registration/ path/basename (cross-tree G1 family)."""
    if _qids(result_path, result_text) & _qids(prereg_path, prereg_text):
        return True
    rd = _parent_dir(result_path)
    if rd != "" and rd == _parent_dir(prereg_path):
        return True
    if (
        prereg_path.startswith(_PREREG_DIR)
        and result_path.startswith(("lab/analysis/", "lab/archive/"))
        and _prereg_cited_in(result_text or "", prereg_path)
    ):
        return True
    return False


def _pair_violations(
    changed: list[tuple[str, str]],
    texts: dict[str, str] | None = None,
) -> list[tuple[str, str, str]]:
    """Pure core: given a commit's changed files [(status, path)], return the
    (result_path, prereg_path, prereg_status) triples worth reporting on.

    A results artifact must be INTRODUCED (status A). The prereg's own status is
    carried through because A and M are DIFFERENT claims, not degrees of one:
      A — the prereg first appears with the results: the freeze is self-attested.
      M — the prereg predates the results (its freeze may be a proper ancestor);
          the concern is only that the run commit moved frozen text.
    Collapsing them mislabels the second as the first — see the 2026-07-27
    addendum in the design spec.

    `texts` is an optional path -> file-body map (commit blob, not the working
    tree). When omitted, pairing is path-only — existing unit tests stay
    basename/directory. preregistration_scan supplies blobs so cross-tree
    G1-family pairs can fire."""
    preregs = [(p, s) for s, p in changed if s in ("A", "M") and _is_prereg_artifact(p)]
    results = [p for s, p in changed if s == "A" and _is_result_artifact(p)]
    pairs: list[tuple[str, str, str]] = []
    for rp in results:
        rtxt = None if texts is None else texts.get(rp)
        for pp, ps in preregs:
            ptxt = None if texts is None else texts.get(pp)
            if _corresponds(rp, pp, result_text=rtxt, prereg_text=ptxt):
                pairs.append((rp, pp, ps))
    return pairs


# A prereg's closure stamp lives on this header line; the body is retained unedited
# (docs/operational_rules.md Rule 8 sub-rule 7).
_STATUS_HEADER = "**Status:**"


def _git_lines(root: Path, *args: str) -> list[str] | None:
    """Run a git command in `root`; return stdout lines, or None on any failure
    (git absent, not a repo, non-zero exit, timeout, undecodable output).
    Fail-open by design.

    `encoding` is pinned rather than left to `text=True`, which would decode with
    the LOCALE default -- cp1252 on a stock Windows box. Git emits UTF-8, and this
    repo's docs are full of em-dashes, arrows and warning glyphs, so a locale decode
    either corrupts the diff silently (when the bytes happen to be cp1252-defined)
    or dies outright (when they are not). The death is the dangerous one: it raises
    in subprocess's reader THREAD, which subprocess swallows, so the parent sees
    returncode 0 with stdout None -- past the returncode check and straight into an
    AttributeError. Hence both the pinned codec and the explicit stdout guard."""
    try:
        out = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True, timeout=30, check=False,
            encoding="utf-8", errors="replace",  # implies text mode
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0 or out.stdout is None:
        return None
    return out.stdout.splitlines()


def _window_commits(root: Path, asof: date, lookback_days: int) -> list[str]:
    """Commits in [asof - lookback_days, asof], by committer date.

    Both bounds matter. `--since` alone leaves the window open at the top, so a
    past `--asof` still swept every commit up to HEAD -- the scan returned the
    same answer for every historical date, which silently defeats §4.1's injected
    `today` and §8's determinism criterion. Correct in the weekly case (asof ==
    today == HEAD) and wrong for every re-run of a past window, including the
    addenda's own "verified against live history" checks. See the 2026-08-24
    addendum in the design spec.
    """
    cutoff = (asof - timedelta(days=lookback_days)).isoformat()
    lines = _git_lines(
        root, "log", "--no-merges",
        "--since", f"{cutoff} 00:00:00",
        "--until", f"{asof.isoformat()} 23:59:59",
        "--pretty=format:%H",
    )
    return [ln.strip() for ln in lines if ln.strip()] if lines else []


def _changed_files(root: Path, sha: str) -> list[tuple[str, str]]:
    # No --root: a commit with no reachable first parent (a true root, or the
    # boundary of a SHALLOW clone where git grafts the history) yields an empty
    # diff and is skipped. That is deliberate fail-open — in a shallow clone the
    # graft boundary would otherwise report its entire tree as "added", flagging
    # every prereg+closure pair that merely coexists in the tree. We can only
    # audit freeze-vs-results when the commit's real delta against its parent is
    # visible.
    # -M (rename detection) is load-bearing, not a tidy-up. Without it git reports a
    # MOVE as delete-old + add-new, and `A` is exactly what "introduced here" keys on
    # -- so archiving a closed camp (`lab/analysis/<slug>/` -> `lab/archive/<slug>/`,
    # which relocates PREREG and RESULTS together by construction) read as a freeze
    # violation. Anchors: 1e40b11 and f2cbb7b on the 2026-08-24 weekly run, both pure
    # `--slug` relocations. See the 2026-08-24 addendum in the design spec.
    lines = _git_lines(root, "diff-tree", "--no-commit-id", "--name-status", "-M", "-r", sha)
    if not lines:
        return []
    changed: list[tuple[str, str]] = []
    for line in lines:
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        raw, path = parts[0], parts[-1]  # rename lines: new path is the last field
        code = raw[:1]
        if code == "R":
            # A rename is not an introduction: the artifact's freeze history lives at
            # the OLD path, which artifact-pairing cannot adjudicate. A pure move
            # (R100) therefore contributes nothing. A move that also EDITED the file
            # still moved frozen text, so it carries through as a modification.
            if raw[1:] in ("", "100"):
                continue
            code = "M"
        changed.append((code, path))
    return changed


def _prereg_edit_is_status_stamp_only(root: Path, sha: str, path: str) -> bool:
    """True when `sha`'s edit to `path` touches only the `**Status:**` header — the
    repo's closure-stamping convention, which leaves the frozen body unedited and is
    therefore not a freeze violation. Fail-open (unreadable diff -> True -> no
    finding), per this module's never-a-false-positive contract."""
    lines = _git_lines(root, "diff-tree", "-p", "--no-commit-id", "-r", sha, "--", path)
    if lines is None:
        return True
    touched = [
        ln[1:] for ln in lines
        if ln[:1] in ("+", "-") and not ln.startswith(("+++", "---"))
    ]
    if not touched:
        return True
    return all(t.lstrip().startswith(_STATUS_HEADER) for t in touched)


def preregistration_scan(root: Path, asof: date, lookback_days: int = 14) -> list[Finding]:
    """Flag commits in the last `lookback_days` whose results/closure artifact lands
    with a corresponding pre-registration. Two distinct findings, never conflated:

      PREREG-SAMECOMMIT — the prereg is ADDED alongside the results: the freeze is
          self-attested, not git-verifiable (Rule 8.7's core case).
      PREREG-RUNEDIT    — the prereg predates the results but the run commit edited
          it beyond its status header: the freeze may be a proper ancestor, so the
          claim is only that frozen text moved (a cheap proxy for the 3935d2c
          verdict-logic class). Closure status-header stamps are exempt.

    Report-only, fail-open (no git -> [])."""
    findings: list[Finding] = []
    for sha in _window_commits(root, asof, lookback_days):
        changed = _changed_files(root, sha)
        need = {
            p for s, p in changed
            if s in ("A", "M") and (_is_prereg_artifact(p) or _is_result_artifact(p))
        }
        texts: dict[str, str] = {}
        for rel in need:
            blob = _git_lines(root, "show", f"{sha}:{rel}")
            if blob is not None:
                texts[rel] = "\n".join(blob)
        pairs = _pair_violations(changed, texts or None)
        if not pairs:
            continue
        short = sha[:7]
        added = [(rp, pp) for rp, pp, st in pairs if st == "A"]
        edited = [
            (rp, pp) for rp, pp, st in pairs
            if st == "M" and not _prereg_edit_is_status_stamp_only(root, sha, pp)
        ]

        if added:
            rp, pp = added[0]
            extra = f" (+{len(added) - 1} more pair(s))" if len(added) > 1 else ""
            findings.append(Finding(
                id=f"PREREG-SAMECOMMIT-{short}",
                category="prereg", routing="Action",
                summary=(
                    f"Commit {short} introduces results/closure `{rp}` together with its "
                    f"pre-registration `{pp}`{extra} — the freeze is self-attested, not "
                    f"git-verifiable (Rule 8.7: prereg must be a separate, earlier commit)."
                ),
                source=rp,
                next_step=(
                    "Freeze the pre-registration in a separate, EARLIER commit than its results "
                    "(gold standard: 46f47d1 freeze -> 913829b run). For already-merged history, "
                    "log it Closed; catch the next one pre-merge by splitting the freeze commit "
                    "out. See docs/operational_rules.md Rule 8 sub-rule 7."
                ),
            ))

        if edited:
            rp, pp = edited[0]
            extra = f" (+{len(edited) - 1} more pair(s))" if len(edited) > 1 else ""
            findings.append(Finding(
                id=f"PREREG-RUNEDIT-{short}",
                category="prereg", routing="Action",
                summary=(
                    f"Commit {short} introduces results/closure `{rp}` and also edits the "
                    f"pre-existing pre-registration `{pp}`{extra} beyond its status header — "
                    f"the run commit must not move frozen verdict logic (Rule 8.7)."
                ),
                source=rp,
                next_step=(
                    "Diff the prereg against its freeze commit "
                    "(`git log --diff-filter=A -- <prereg>`, then `git diff <freeze> <run> -- "
                    "<prereg>`) and confirm no gate, threshold, or verdict rule moved. A "
                    "closure `**Status:**` stamp alone is exempt and never reaches here. "
                    "See docs/operational_rules.md Rule 8 sub-rule 7."
                ),
            ))
    return findings
