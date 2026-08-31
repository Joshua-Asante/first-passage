#!/usr/bin/env python3
"""check_advisor_dedup.py — prior-art search for a staged advisor/handoff artifact.

Motivating incident (2026-07-24): a web-advisor / Downloads-staged Pre-Q brief
and gate-audit note claimed an untested "Weekly+Daily residual" from an
imagined 2026-07-23 ICT top-down closure. `handoff-verify` caught it as
confabulated — no such run exists; the real corpus (`lab/archive/
ict_cascade_2026-06-18/`) had already closed PER-LAYER under a pre-registered
M=65 ledger. The catch cost a full session because nothing pointed the
executing session at the existing closure before it started reasoning about
the staged claims as if they were live.

THIS IS A SEARCH ASSISTANT, NOT A GATE. It cannot decide whether a staged
artifact duplicates prior work — that requires reading both and judging.  What
it can do mechanically: extract likely-identifying terms from the staged file
(slug-shaped tokens, title words) and rank existing repo artifacts by term
overlap, so the check that took a full session becomes a few-second lookup
BEFORE treating the staged content as new. Exit code is always 0 — there is
nothing here to "fail"; the output is advisory context for a human/agent
judgment call, same posture as check_adr_graph.py's opt-in A5/A7.

Corpus searched (the surfaces this repo already treats as closure-of-record):
  docs/briefs/closures/*.md        one chunk per file
  docs/notes/audits/*.md           one chunk per file
  docs/SESSIONS.md                 one chunk per "## " entry
  lab/CATALOG.md                   one chunk per "| slug | ..." row
  docs/rejected_candidates.md      one chunk per "### " entry
  ops/instruments/*.md             one chunk per file
  docs/briefs/rnd-pipeline/*.md    one chunk per file
  docs/adr/*.md                    one chunk per file (excl. INDEX/README/TOMBSTONES)

Third motivating incident (2026-08-31, ADR corpus audit): docs/adr/ was absent
from every surface above -- the tool that answers "does an ADR on this already
exist?" could not see a single ADR. Two same-shaped F1 discharges landed nine
days apart (2026-08-15, 2026-08-24) with no dedup hit between them, and a
persona-hierarchy ADR pasted this tool's "slugs found: (none)" as its own §0
dedup evidence -- a guaranteed false negative displayed as proof. Closed the
same way the second incident was: add the missing corpus surface.

Second motivating incident (2026-08-19): a Research Analyst inaugural-session
draft recommended GRADUATE on the D5 Baltussen intraday-momentum-footprint
axis for MNQ as "genuinely unspent," running check_advisor_dedup with
project-level keywords first. The tool correctly found no prior *project*
like it -- but the axis itself had already been ratified (Q-KBUDGET-1),
built, Stage-2-killed on IS-era prices, re-derived on OOS-native prices
(D5-RECOST-1, 2026-07-21) and killed again, HIGH-confidence, K=1 banked --
all recorded in ops/instruments/MNQ.md (finding N5) and docs/briefs/
rnd-pipeline/, neither of which this tool searched. Project-level dedup and
mechanism-level dedup are different questions; this tool answered the first
correctly and was silent on the second because its corpus never covered the
one surface (ops/instruments/) that repo doctrine already makes MANDATORY
reading for exactly this question ("any session deriving/testing/
adjudicating on <SYM> MUST read ops/instruments/<SYM>.md at session start").
Closing the corpus gap, not adding new judgment logic -- this tool still
only ranks by vocabulary overlap; a human/agent still has to read the hit
and decide.

Usage:
    python scripts/check_advisor_dedup.py <path-to-staged-file> [--top N]
    python scripts/check_advisor_dedup.py --keywords "Magdon-Ismail closed-form" [--top N]

Keyword-string mode (ADR 2026-08-13): run before any staged file or lab dir
exists — feeds extract_terms() from the string; ranking/corpus unchanged.
Exit code is always 0 in both modes.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SLUG_RE = re.compile(r"\b[A-Z][A-Za-z]*(?:-[A-Z0-9][A-Za-z0-9]*){1,4}\b")
WORD_RE = re.compile(r"[A-Za-z]{4,}")


def _has_digit(token: str) -> bool:
    """A hyphenated identifier only counts as a SLUG (near-certain identity
    anchor) if it contains a digit -- Q-ICT-1, S-MYM-ORC-02, ORB-MNQ-1. Without
    this, generic template tokens (PRE-Q, D-S-A, RESOLVED-REAL) matched too,
    diluting the slug-match signal with boilerplate every Pre-Q brief shares."""
    return any(c.isdigit() for c in token)
MD_LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
MD_SYNTAX_RE = re.compile(r"[`*_#\[\]()]")

STOPWORDS = frozenset("""
this that with from into over under about their there where when what which
does doing done have has had were was been being also than then some such
only just more most other another same both each every either neither
before after during while since until because although though whether
these those they them then very much many less least first second third
still even ever never always often always sometimes rather quite really
should would could might shall will may must can does did do the a an of
to in on at by is it as for and or but not no yes if so we you your our
brief closure status type opened focus context question hypothesis
""".split())


@dataclass(frozen=True)
class Chunk:
    surface: str
    label: str
    text: str


def extract_terms(text: str) -> tuple[set[str], set[str]]:
    """(slugs, keywords) — slugs are near-certain identity anchors
    (Q-ICT-1, S-MYM-ORC-02, ORB-MNQ-1); keywords are a coarse fallback."""
    slugs = {m.upper() for m in SLUG_RE.findall(text) if _has_digit(m)}
    plain = MD_LINK_RE.sub(r"\1", text)
    plain = MD_SYNTAX_RE.sub(" ", plain)
    keywords = {
        w.lower() for w in WORD_RE.findall(plain)
        if w.lower() not in STOPWORDS
    }
    return slugs, keywords


def _title_of(text: str, fallback: str) -> str:
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("#"):
            return s.lstrip("#").strip()
    return fallback


def _split_by_h2(text: str) -> list[str]:
    parts, buf = [], []
    for line in text.splitlines():
        if line.startswith("## ") and buf:
            parts.append("\n".join(buf))
            buf = []
        buf.append(line)
    if buf:
        parts.append("\n".join(buf))
    return parts


def _split_by_h3(text: str) -> list[str]:
    parts, buf = [], []
    for line in text.splitlines():
        if line.startswith("### ") and buf:
            parts.append("\n".join(buf))
            buf = []
        buf.append(line)
    if buf:
        parts.append("\n".join(buf))
    return [p for p in parts if p.lstrip().startswith("### ")]


def load_corpus(repo_root: Path) -> list[Chunk]:
    chunks: list[Chunk] = []

    closures_dir = repo_root / "docs" / "briefs" / "closures"
    if closures_dir.is_dir():
        for md in sorted(closures_dir.glob("*.md")):
            text = md.read_text(encoding="utf-8", errors="replace")
            surface = md.relative_to(repo_root).as_posix()
            chunks.append(Chunk(surface, _title_of(text, md.stem), text))

    audits_dir = repo_root / "docs" / "notes" / "audits"
    if audits_dir.is_dir():
        for md in sorted(audits_dir.rglob("*.md")):
            text = md.read_text(encoding="utf-8", errors="replace")
            surface = md.relative_to(repo_root).as_posix()
            chunks.append(Chunk(surface, _title_of(text, md.stem), text))

    sessions_path = repo_root / "docs" / "SESSIONS.md"
    if sessions_path.is_file():
        text = sessions_path.read_text(encoding="utf-8", errors="replace")
        surface = sessions_path.relative_to(repo_root).as_posix()
        for entry in _split_by_h2(text):
            title = _title_of(entry, "SESSIONS entry")
            if title in ("Session Log",):
                continue
            chunks.append(Chunk(surface, title, entry))

    catalog_path = repo_root / "lab" / "CATALOG.md"
    if catalog_path.is_file():
        text = catalog_path.read_text(encoding="utf-8", errors="replace")
        surface = catalog_path.relative_to(repo_root).as_posix()
        for line in text.splitlines():
            if line.startswith("| ") and "---" not in line and "slug" not in line.split("|")[1]:
                slug = line.split("|")[1].strip()
                if slug:
                    chunks.append(Chunk(surface, slug, line))

    rejected_path = repo_root / "docs" / "rejected_candidates.md"
    if rejected_path.is_file():
        text = rejected_path.read_text(encoding="utf-8", errors="replace")
        surface = rejected_path.relative_to(repo_root).as_posix()
        for entry in _split_by_h3(text):
            title = _title_of(entry, "rejected-candidates entry")
            chunks.append(Chunk(surface, title, entry))

    instruments_dir = repo_root / "ops" / "instruments"
    if instruments_dir.is_dir():
        for md in sorted(instruments_dir.glob("*.md")):
            text = md.read_text(encoding="utf-8", errors="replace")
            surface = md.relative_to(repo_root).as_posix()
            chunks.append(Chunk(surface, _title_of(text, md.stem), text))

    rnd_pipeline_dir = repo_root / "docs" / "briefs" / "rnd-pipeline"
    if rnd_pipeline_dir.is_dir():
        for md in sorted(rnd_pipeline_dir.glob("*.md")):
            text = md.read_text(encoding="utf-8", errors="replace")
            surface = md.relative_to(repo_root).as_posix()
            chunks.append(Chunk(surface, _title_of(text, md.stem), text))

    # ADRs are closures-of-record for governance/doctrine decisions the same
    # way docs/briefs/closures/ is for research campaigns -- omitted until
    # 2026-08-31 (found in the ADR corpus audit: two ADRs, 08-15 and 08-24,
    # discharged the same F1 nine days apart with no dedup hit between them).
    # INDEX.md/README.md/TOMBSTONES.md are corpus scaffolding, not decisions.
    adr_dir = repo_root / "docs" / "adr"
    if adr_dir.is_dir():
        skip = {"INDEX.md", "README.md", "TOMBSTONES.md"}
        for md in sorted(adr_dir.glob("*.md")):
            if md.name in skip:
                continue
            text = md.read_text(encoding="utf-8", errors="replace")
            surface = md.relative_to(repo_root).as_posix()
            chunks.append(Chunk(surface, _title_of(text, md.stem), text))

    return chunks


def score(staged_slugs: set[str], staged_keywords: set[str], chunk: Chunk) -> tuple[int, int, set[str], set[str]]:
    chunk_slugs, chunk_keywords = extract_terms(chunk.text)
    slug_hits = staged_slugs & chunk_slugs
    keyword_hits = staged_keywords & chunk_keywords
    # slug matches are near-certain identity signals; weight them heavily
    weighted = len(slug_hits) * 20 + len(keyword_hits)
    return weighted, len(keyword_hits), slug_hits, keyword_hits


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument(
        "staged_file",
        nargs="?",
        type=Path,
        default=None,
        help="Path to the staged artifact (e.g. a Downloads file).",
    )
    ap.add_argument(
        "--keywords",
        type=str,
        default=None,
        help="Keyword string to search (alternative to staged_file; "
        "for pre-file / build-intent checks).",
    )
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    ap.add_argument("--top", type=int, default=8, help="Max candidates to print (default 8).")
    ap.add_argument("--min-score", type=int, default=2, help="Drop candidates below this weighted score.")
    args = ap.parse_args(argv)

    # Always exit 0 — search assistant, not a gate. Mutual exclusion is
    # advisory messaging only.
    if args.keywords is not None and args.staged_file is not None:
        print(
            "check_advisor_dedup: pass either a staged_file or --keywords, not both",
            file=sys.stderr,
        )
        return 0
    if args.keywords is None and args.staged_file is None:
        print(
            "check_advisor_dedup: need a staged_file positional or --keywords",
            file=sys.stderr,
        )
        return 0

    if args.keywords is not None:
        staged_text = args.keywords
        print(f"check_advisor_dedup: keywords: {args.keywords!r}")
    else:
        assert args.staged_file is not None
        if not args.staged_file.is_file():
            print(
                f"check_advisor_dedup: no such file: {args.staged_file}",
                file=sys.stderr,
            )
            return 0
        staged_text = args.staged_file.read_text(encoding="utf-8", errors="replace")
        print(f"check_advisor_dedup: staged file: {args.staged_file}")

    staged_slugs, staged_keywords = extract_terms(staged_text)

    print(f"  slugs found:    {sorted(staged_slugs) or '(none)'}")
    print(f"  keywords found: {len(staged_keywords)} significant terms")
    print()

    corpus = load_corpus(args.repo_root)
    if not corpus:
        print("check_advisor_dedup: no corpus found under docs/briefs/closures, "
              "docs/notes/audits, docs/SESSIONS.md, lab/CATALOG.md, "
              "docs/rejected_candidates.md, ops/instruments, docs/adr, "
              "docs/briefs/rnd-pipeline — nothing to compare against.")
        return 0

    ranked = []
    for chunk in corpus:
        weighted, kw_count, slug_hits, kw_hits = score(staged_slugs, staged_keywords, chunk)
        if weighted >= args.min_score:
            ranked.append((weighted, kw_count, chunk, slug_hits, kw_hits))
    ranked.sort(key=lambda r: (-r[0], -r[1]))

    if not ranked:
        print("check_advisor_dedup: no overlapping prior art found above the "
              f"--min-score={args.min_score} threshold. This does NOT mean the "
              "content is new — it means nothing in the searched corpus "
              "shares enough vocabulary to surface. Still verify claimed repo "
              "state directly (handoff-verify) before treating as new work.")
        return 0

    source_label = (
        "keywords" if args.keywords is not None else "staged file"
    )
    print(f"POSSIBLE PRIOR ART — review before treating the {source_label} as new work "
          f"(top {min(args.top, len(ranked))} of {len(ranked)} candidate(s)):")
    print()
    for weighted, kw_count, chunk, slug_hits, kw_hits in ranked[: args.top]:
        print(f"  [{weighted:3d}] {chunk.surface} — {chunk.label}")
        if slug_hits:
            print(f"        SLUG MATCH: {sorted(slug_hits)}")
        shown = sorted(kw_hits)[:8]
        if shown:
            print(f"        shared terms: {shown}"
                  + (f" (+{len(kw_hits) - len(shown)} more)" if len(kw_hits) > len(shown) else ""))
        print()

    # DISABLED — repo_retrieve.py re-measured ASSISTIVE-ONLY 2026-08-15 (see
    # _fts_companion docstring below). This is a final disposition under a
    # frozen pre-registration, not a pending quarantine.
    # _fts_companion(args.repo_root, staged_text if args.keywords else None)
    return 0


def _fts_companion(repo_root: Path, keywords: str | None) -> None:
    """Fail-open FTS pass (Q-XMEM-1 Limb B). Never changes this tool's exit 0.

    DISABLED — the call site above stays commented out. Originally
    QUARANTINED 2026-08-15 when a 4-arm ablation against the frozen
    2026-07-27 recall falsifier found the shipped scripts/repo_retrieve.py
    scored recall@5 = 0.086, tied with the rg incumbent it exists to beat,
    because the query omitted `ORDER BY rank`. Fixed the same day (rank
    restored, UTF-8-safe output, HEAD-stamped staleness) and re-measured
    under a fresh frozen pre-registration
    (docs/briefs/pre-registration/2026-08-15-fts5-delete-falsifier-prereg-v3.md)
    with one permitted corpus-widening revision taken. Result:
    `ASSISTIVE-ONLY` — R_shipped@5 = 0.500, beats rg (0.088) decisively but
    stays below the 0.70 floor. This is the tool's settled disposition, not
    a bug awaiting a fix. Full record:
    lab/analysis/harvest/limb_b_remeasure_2026-08/RESULTS.md. Re-enabling
    this call site requires a fresh frozen registration clearing the floor,
    not a partial patch.
    """
    if not keywords:
        return
    retrieve = repo_root / "scripts" / "repo_retrieve.py"
    if not retrieve.is_file():
        return
    try:
        out = subprocess.run(
            [sys.executable, str(retrieve), "--query", keywords, "--limit", "5",
             "--repo", str(repo_root)],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return
    if out.returncode == 0 and out.stdout.strip():
        print("FTS companion (repo_retrieve — paths only, not authority):")
        print(out.stdout.rstrip())
        print()


if __name__ == "__main__":
    raise SystemExit(main())
