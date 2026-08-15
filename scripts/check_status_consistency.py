#!/usr/bin/env python3
"""check_status_consistency.py — cross-surface study-status gate (governance tier).

The same study-closure verdict is restated across three surfaces, hand-synced:
  - lab/CATALOG.md            — study index + status (the AUTHORITY here)
  - ops/instruments/*.md      — DEAD/REJECTED lists (anti-SNAG accounting)
  - docs/rejected_candidates.md — portfolio re-proposal registry

This gate treats CATALOG as the machine-readable status authority and flags a
SHARED slug (joined via the lab/(analysis|archive)/<slug>/ path that all three
surfaces carry) whose status drifts:

  C2 (HARD) — a CATALOG row self-inconsistent: table vs status word vs body-tier.
  C3 (HARD) — a lab/analysis/<slug>/<file> link that no longer resolves but is
              present under lab/archive/<slug>/ (stale tier link; suggest
              repoint) OR under lab/analysis/<theme>/<slug>/ (flat-to-theme-nest
              move; suggest repoint).
  NOTE      — a slug cited as rejected with no CATALOG row (scoped orphan; does
              NOT change the exit code — the surfaces are deliberately not 1:1).

A "C1" status-contradiction check (a slug dead-listed / rejected here but
CATALOG-Active) was designed but DROPPED after its first real run: rejection
contexts link the APPARATUS / parent study (often legitimately still Active) as
evidence, not the rejected sub-direction, so the slug-join yielded only false
positives (a rejected NAS100 ORB *gate* linking the active orb_universe harness;
a rejected XAUUSD *sub-thesis* linking the HOLD parent study). The mechanically-
reliable signal is the link TIER (C3) + CATALOG self-consistency (C2), not a
semantic "is this study dead" join. See the design doc.

A "C4" intra-STATE.md check was likewise designed and DROPPED, 2026-07-25, before
shipping. Motivating incident: on 2026-07-24 STATE.md contradicted ITSELF — the
pointer log recorded the prop §4 falsifier DISCHARGED (2026-07-15) while the
forward-trigger board 180 lines below still restated the obligation as fully open.
A session read the forward board, treated the falsifier as live, and authored a
recording of a discharge that had by then ALSO been withdrawn upstream. Every
cross-FILE gate was green throughout; the contradiction was intra-file.

Two designs were built and measured against the actual pre-incident file. Both are
unreachable, for the same underlying reason — there is no shared anchor to join on:
  (i)  cross-section join ("forward board cites an ADR the pointer log closed"):
       the pointer-log bullet recording the discharge cites 32 repo paths and NOT
       ONE is the four-firms ADR whose falsifier it discharged. Shared paths
       between the two bullets: zero.
  (ii) root-cause completeness ("a terminal entry must name an ADR"): the same
       bullet DOES cite an ADR — the 07-14 candidate-class amendment, not the 07-12
       ADR the status belongs to. "Cites some ADR" passes while the relevant one is
       absent.
Separating those needs semantic knowledge of which ADR a given status belongs to,
which is the C1 mistake in new clothing. Recorded here so the next pass does not
re-derive it: the reachable fix for this class is a WRITING convention (a terminal
pointer-log entry names its owning ADR) enforced at authoring time, not a gate.

Honest limitation (cf. check_root_doc_liveness's class-1-vs-class-2): an entry
whose rejection is expressed only in prose, or via [[memory]] / docs/.../brief.md
links with NO lab/(analysis|archive)/<slug>/ anchor, is NOT joinable and is
skipped (e.g. NAS100's memory-linked "Q-NAS-4" row). This gate reports what it
can join; it is not a completeness proof.

Reads only committed markdown -> environment-independent (green on CI / clone).

Exit codes: 0 = no HARD findings (NOTEs allowed); 1 = one or more C2/C3.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Closed theme-dir set (must match scripts/archive_lab_analysis.THEME_ORDER).
# scripts/ aren't packages — do not import; tests/test_check_status_consistency.py
# pins csc._THEME_ORDER == ala.THEME_ORDER.
# Optional theme segment so nested hot paths lab/analysis/<theme>/<slug>/…
# capture the study slug, not the theme directory name.
_THEME_ORDER = (
    "c1", "striker", "orb", "aegis", "regime", "harvest", "mc", "legacy", "_inbox",
)
_THEMES = frozenset(_THEME_ORDER)
_THEME_ALT = "|".join(re.escape(t) for t in _THEME_ORDER)

# lab/<tier>/[<theme>/]<slug>[/rest] — matches the repo-relative tail even when
# the actual markdown link is written ../../lab/... (the ../../ prefix is
# ignored; group(0) is the canonical repo-relative path, resolvable against
# REPO_ROOT). Flat stubs and flat archive paths omit the theme group.
SLUG_LINK_RE = re.compile(
    rf"lab/(analysis|archive)/(?:(?:{_THEME_ALT})/)?"
    rf"([^`/\s)#\]]+)(?:/[^`/\s)#\]]*)?"
)
# Eviction-retrieval tokens. Mask the clause they belong to (not the whole
# line) so a live lab/ citation sharing the line is still scanned.
HISTORICAL_LINE_RE = re.compile(r"git\s+show|pre-prune-", re.IGNORECASE)
_CLAUSE_STOP = frozenset(" \t`;)")
# A markdown header whose text contains DEAD / REJECTED / PARKED opens a
# rejection section in a ledger.
DEAD_HEADER_RE = re.compile(r"^#{1,6}\s+.*\b(?:DEAD|REJECTED|PARKED)\b", re.IGNORECASE)
HEADER_RE = re.compile(r"^(#{1,6})\s+\S")

LIVE_STATUS = frozenset({"ACTIVE", "HOLD"})
TERMINAL_STATUS = frozenset({"CLOSED", "FALSIFIED", "RETIRED"})


@dataclass(frozen=True)
class CatalogEntry:
    slug: str
    status: str
    table: str            # "active" | "archived"
    body_tier: str | None  # "live" | "archived" | None
    lineno: int


@dataclass(frozen=True)
class Assertion:
    surface: str
    lineno: int
    slug: str
    link_tier: str        # "analysis" | "archive"
    target: str           # repo-relative path, e.g. "lab/analysis/foo/RESULTS.md"
    asserts_rejection: bool


@dataclass(frozen=True)
class Finding:
    severity: str         # "HARD" | "NOTE"
    code: str             # "C2" | "C3" | "NOTE"
    surface: str
    lineno: int
    message: str


def parse_catalog(text: str) -> dict[str, CatalogEntry]:
    """Index every CATALOG row -> CatalogEntry. `table` comes from the most recent
    `## Active` / `## Archived` header; `body_tier` is "archived" if the row carries
    a lab/archive/ link (the body column), else "live" if it carries a lab/analysis/
    link, else None (correctly handling an archived row whose `card` stub is a
    lab/analysis/ path while its `body` is lab/archive/).

    Column layout: if the table header includes ``theme``, map ``status`` / ``body``
    by header name (Active 6-col schema). Otherwise use legacy fixed positions
    (status at 1, body at 4 — the pre-theme 7-col Active / Archived schema)."""
    catalog: dict[str, CatalogEntry] = {}
    table: str | None = None
    # None => legacy fixed positions; dict => name->index from a themed header.
    col_map: dict[str, int] | None = None
    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if re.match(r"^##\s+Active\b", line):
            table = "active"
            col_map = None
            continue
        if re.match(r"^##\s+Archived\b", line):
            table = "archived"
            col_map = None
            continue
        if re.match(r"^##\s+", line):                # any other section ends the table
            table = None
            col_map = None
            continue
        if table is None or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        slug = cells[0]
        if not slug or slug.lower() == "slug":       # header row
            headers = [c.lower() for c in cells]
            if "theme" in headers:
                col_map = {name: i for i, name in enumerate(headers)}
            else:
                col_map = None
            continue
        if set(slug) <= set("-: "):                  # separator row
            continue
        # Tier comes from the `body` column specifically, NOT the whole row: a
        # free-text one-liner mentioning a lab/archive/ path must not flip the
        # tier and raise a false C2. Archived rows carry a lab/archive/ body
        # even though their `card` stub is a lab/analysis/ path.
        if col_map is not None:
            status_idx = col_map.get("status")
            status = (
                cells[status_idx]
                if status_idx is not None and status_idx < len(cells)
                else ""
            )
            body_idx = col_map.get("body")
            body_cell = (
                cells[body_idx] if body_idx is not None and body_idx < len(cells) else ""
            )
        else:
            status = cells[1]
            body_cell = cells[4] if len(cells) >= 5 else ""
        if "lab/archive/" in body_cell:
            body_tier: str | None = "archived"
        elif "lab/analysis/" in body_cell:
            body_tier = "live"
        else:
            body_tier = None
        catalog[slug] = CatalogEntry(slug, status, table, body_tier, lineno)
    return catalog


def check_catalog_internal(catalog: dict[str, CatalogEntry]) -> list[Finding]:
    """C2 — a CATALOG row whose table membership disagrees with its body-path tier
    or with the class of its status word. Only known status words (LIVE/TERMINAL)
    are class-checked, so an unrecognised status word never false-positives."""
    findings: list[Finding] = []
    for e in catalog.values():
        expected_tier = "live" if e.table == "active" else "archived"
        if e.body_tier is not None and e.body_tier != expected_tier:
            findings.append(Finding(
                "HARD", "C2", "lab/CATALOG.md", e.lineno,
                f"{e.slug}: in the {e.table} table but its body path is "
                f"{e.body_tier}-tier (expected {expected_tier})"))
        su = e.status.upper()
        status_class = ("live" if su in LIVE_STATUS
                        else "terminal" if su in TERMINAL_STATUS else None)
        expected_class = "live" if e.table == "active" else "terminal"
        if status_class is not None and status_class != expected_class:
            findings.append(Finding(
                "HARD", "C2", "lab/CATALOG.md", e.lineno,
                f"{e.slug}: status '{e.status}' is {status_class} but sits in the "
                f"{e.table} table"))
    return findings


def _links_in_line(line: str) -> list[tuple[str, str, str]]:
    """(link_tier, slug, repo_relative_target) for each lab-slug link in a line."""
    return [(m.group(1), m.group(2), m.group(0)) for m in SLUG_LINK_RE.finditer(line)]


def _enclosing_paren_span(line: str, start: int, end: int) -> tuple[int, int] | None:
    """If [start:end] sits inside a (...), return that pair's span."""
    depth = 0
    open_idx: int | None = None
    for i in range(start - 1, -1, -1):
        ch = line[i]
        if ch == ")":
            depth += 1
        elif ch == "(":
            if depth == 0:
                open_idx = i
                break
            depth -= 1
    if open_idx is None:
        return None
    depth = 0
    for i in range(open_idx, len(line)):
        ch = line[i]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                if i >= end - 1:
                    return (open_idx, i + 1)
                return None
    return None


def _eviction_clause_span(line: str, start: int, end: int) -> tuple[int, int]:
    """Widen a HISTORICAL_LINE_RE match to its retrieval clause.

    Consumes a following ``rev:path`` token (and wrapping backticks), then
    the parenthetical the clause sits inside when there is one. Evicted-blob
    paths that are the git-show argument stay hidden; a citation elsewhere
    on the line does not.
    """
    while end < len(line) and line[end] not in _CLAUSE_STOP:
        end += 1
    matched = line[start:end]
    if re.match(r"git\s+show\b", matched, re.IGNORECASE):
        while end < len(line) and line[end] in " \t":
            end += 1
        while end < len(line) and line[end] not in _CLAUSE_STOP:
            end += 1
    if start > 0 and line[start - 1] == "`":
        start -= 1
    if end < len(line) and line[end] == "`":
        end += 1
    return _enclosing_paren_span(line, start, end) or (start, end)


def _mask_eviction_idioms(line: str) -> str:
    """Strip git-show / pre-prune- retrieval clauses; leave the rest intact."""
    if not HISTORICAL_LINE_RE.search(line):
        return line
    pieces: list[str] = []
    last = 0
    for m in HISTORICAL_LINE_RE.finditer(line):
        a, b = _eviction_clause_span(line, m.start(), m.end())
        if a < last:
            continue
        pieces.append(line[last:a])
        last = b
    pieces.append(line[last:])
    return "".join(pieces)


def scan_ledger(text: str, surface: str) -> list[Assertion]:
    """All lab-slug links in one instrument ledger. `asserts_rejection` is True for
    links inside a DEAD/REJECTED/PARKED section (in force until the next header at
    the same or a higher level), False elsewhere (e.g. durable-findings evidence).
    Git-show / pre-prune- retrieval clauses are masked so an evicted-blob
    path is not scanned; any other lab/ citation on the same line still is."""
    assertions: list[Assertion] = []
    in_dead = False
    dead_level = 0
    for lineno, raw in enumerate(text.splitlines(), start=1):
        hm = HEADER_RE.match(raw)
        if hm:
            level = len(hm.group(1))
            if DEAD_HEADER_RE.match(raw):
                in_dead, dead_level = True, level
            elif in_dead and level <= dead_level:
                in_dead = False
        for tier, slug, target in _links_in_line(_mask_eviction_idioms(raw)):
            assertions.append(Assertion(surface, lineno, slug, tier, target, in_dead))
    return assertions


def scan_rejected(text: str, surface: str) -> list[Assertion]:
    """All lab-slug links in docs/rejected_candidates.md. The whole file asserts
    rejection, so every link is `asserts_rejection=True`. Eviction-idiom
    clauses are masked; other citations on the same line are still scanned."""
    assertions: list[Assertion] = []
    for lineno, raw in enumerate(text.splitlines(), start=1):
        for tier, slug, target in _links_in_line(_mask_eviction_idioms(raw)):
            assertions.append(Assertion(surface, lineno, slug, tier, target, True))
    return assertions


def check_notes(catalog: dict[str, CatalogEntry],
                assertions: list[Assertion]) -> list[Finding]:
    """NOTE — a slug asserted rejected with no CATALOG row (scoped orphan). Deduped
    by slug so a study cited in many places yields one note."""
    notes: list[Finding] = []
    seen: set[str] = set()
    for a in assertions:
        if not a.asserts_rejection or a.slug in catalog or a.slug in seen:
            continue
        seen.add(a.slug)
        notes.append(Finding(
            "NOTE", "NOTE", a.surface, a.lineno,
            f"{a.slug}: cited as rejected but has no CATALOG row "
            f"(uncatalogued; not a completeness failure)"))
    return notes


def _analysis_to_archive_target(target: str) -> str:
    """Map ``lab/analysis/[theme/]<slug>/...`` → flat ``lab/archive/<slug>/...``.

    Archive stays slug-flat; a nested hot link must drop the theme segment when
    suggesting the C3 repoint.
    """
    rest = target.removeprefix("lab/analysis/")
    parts = rest.split("/")
    if parts and parts[0] in _THEMES and len(parts) >= 2:
        parts = parts[1:]
    return "lab/archive/" + "/".join(parts)


def _analysis_to_theme_nest_targets(target: str, repo_root: Path) -> list[str]:
    """If ``lab/analysis/<slug>/...`` is gone, find ``lab/analysis/<theme>/<slug>/...``.

    Inserts one path segment after ``lab/analysis/`` and keeps every extra
    segment that actually resolves (future themes included, not just
    ``_THEMES``). An unresolved link with no such nest is a plain dead link.
    """
    prefix = "lab/analysis/"
    if not target.startswith(prefix):
        return []
    rest = target[len(prefix):]
    if not rest:
        return []
    analysis_root = repo_root / "lab" / "analysis"
    if not analysis_root.is_dir():
        return []
    found: list[str] = []
    for child in sorted(p for p in analysis_root.iterdir() if p.is_dir()):
        candidate = child / rest
        if candidate.exists():
            found.append(f"{prefix}{child.name}/{rest}")
    return found


def check_c3(assertions: list[Assertion], repo_root: Path) -> list[Finding]:
    """C3 — a lab/analysis/<slug>/<file> link that no longer resolves but IS present
    under lab/archive/<slug>/ (the file moved on archive) or under
    lab/analysis/<theme>/<slug>/ (flat-to-theme-nest). Reports the repoint.
    Only analysis-tier links are candidates; a link to a surviving stub (e.g.
    .../CARD.md) resolves and does not fire; an unresolved link with no archive
    or theme-nest counterpart is a plain dead link, out of scope (§5). Nested
    hot links have their theme segment stripped in the suggested archive path."""
    findings: list[Finding] = []
    for a in assertions:
        if a.link_tier != "analysis":
            continue
        if (repo_root / a.target).exists():
            continue
        archive_target = _analysis_to_archive_target(a.target)
        if (repo_root / archive_target).exists():
            findings.append(Finding(
                "HARD", "C3", a.surface, a.lineno,
                f"stale tier link -> {a.target} (moved; repoint to {archive_target})"))
            continue
        nest_targets = _analysis_to_theme_nest_targets(a.target, repo_root)
        if nest_targets:
            findings.append(Finding(
                "HARD", "C3", a.surface, a.lineno,
                f"stale flat link -> {a.target} (moved; repoint to "
                f"{nest_targets[0]})"))
    return findings


def collect_findings(repo_root: Path, catalog_path: Path,
                     instruments_dir: Path, rejected_path: Path) -> list[Finding]:
    """Parse all three surfaces, join on slug, return every finding (HARD + NOTE)."""
    findings: list[Finding] = []
    catalog = parse_catalog(catalog_path.read_text(encoding="utf-8", errors="replace")) \
        if catalog_path.exists() else {}
    findings += check_catalog_internal(catalog)

    assertions: list[Assertion] = []
    if instruments_dir.is_dir():
        for md in sorted(instruments_dir.glob("*.md")):
            surface = md.relative_to(repo_root).as_posix()
            assertions += scan_ledger(
                md.read_text(encoding="utf-8", errors="replace"), surface)
    if rejected_path.exists():
        surface = rejected_path.relative_to(repo_root).as_posix()
        assertions += scan_rejected(
            rejected_path.read_text(encoding="utf-8", errors="replace"), surface)

    findings += check_c3(assertions, repo_root)
    findings += check_notes(catalog, assertions)
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--catalog", type=Path, default=None)
    parser.add_argument("--instruments-dir", type=Path, default=None)
    parser.add_argument("--rejected", type=Path, default=None)
    args = parser.parse_args()

    root = args.repo_root
    catalog_path = args.catalog or root / "lab" / "CATALOG.md"
    instruments_dir = args.instruments_dir or root / "ops" / "instruments"
    rejected_path = args.rejected or root / "docs" / "rejected_candidates.md"

    findings = collect_findings(root, catalog_path, instruments_dir, rejected_path)
    hard = [f for f in findings if f.severity == "HARD"]
    notes = [f for f in findings if f.severity == "NOTE"]

    for f in hard:
        print(f"HARD: {f.surface}:{f.lineno}: {f.code} {f.message}")
    for f in notes:
        print(f"NOTE: {f.surface}:{f.lineno}: {f.message}")

    if hard:
        print(f"\ncheck_status_consistency: {len(hard)} status contradiction(s). "
              "CATALOG is the status authority; CATALOG rows must be self-consistent "
              "(C2) and cross-surface links must point to the correct path — a moved "
              "analysis/ link should point to archive/ or analysis/<theme>/ (C3). "
              "Repoint or repair the drifting surface — do not relax the gate.")
        return 1
    print(f"check_status_consistency: OK — no status contradictions "
          f"({len(notes)} advisory note(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
