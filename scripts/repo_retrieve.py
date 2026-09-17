#!/usr/bin/env python3
"""Repo-local retrieval over hot liveness surfaces (Q-XMEM-1 Limb B).

Not a Rule-7 owner. Returns paths + snippets; the agent must Read the owner.
Does not ingest docs/ltm/ or lab/archive/ bodies (LTM stays catalog-gated).

FTS5 over a curated hot corpus is the cheap slice. A local-embedder vector
slot is documented in Q-XMEM-1 v1.2 and is not built here.

2026-08-15 (Phase 1 of the governance-belt audit's remediation): the query
that shipped on 2026-08-14 omitted FTS5's ``ORDER BY rank``, so results came
back in rowid (insertion) order rather than relevance order — measured at
recall@5 = 0.086 against the frozen 2026-07-27 falsifier, tied with the plain
`rg` incumbent it exists to beat. Fixed here, along with UTF-8-safe output
(the prior hardcoded arrow/ellipsis characters crashed on Windows cp1252
stdout) and HEAD-stamped staleness (the index previously never refreshed
once built).

2026-08-15 (Phase 2, v3 remeasurement, one-revision cap): re-measuring the
ranked tool against the frozen v3 pre-registration
(docs/briefs/pre-registration/2026-08-15-fts5-delete-falsifier-prereg-v3.md)
found a reachability ceiling of 0.676 -- below the 0.70 floor regardless of
ranking quality, because brief bodies, methodology, spec, and audit-note
prose were entirely outside the corpus. Widened `collect_chunks()` to add
`docs/briefs/*.md`, `docs/notes/audits/**`, `docs/methodology/*.md`,
`docs/spec/*.md` (still excluding `docs/ltm/` and `lab/archive/`) -- the one
widening revision the v3 pre-registration permits. See
lab/analysis/harvest/limb_b_remeasure_2026-08/RESULTS.md for the measured
verdict on this corpus.

Usage:
  python scripts/repo_retrieve.py --rebuild
  python scripts/repo_retrieve.py --query "Magdon-Ismail closed-form MDD"
"""
from __future__ import annotations

import argparse
import re
import sqlite3
import subprocess
import sys
from pathlib import Path
from dataclasses import dataclass

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gate_fire_log import log_fire  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
DEFAULT_DB = REPO / ".cache" / "repo_retrieve.sqlite"

# Hot surfaces only; archives are excluded by construction. Order is observable.
@dataclass(frozen=True)
class CorpusSource:
    pattern: str
    mode: str
    limit: int | None = None
    omit_section: str | None = None


CORPUS_SOURCES = (
    CorpusSource("lab/CATALOG.md", "catalog", omit_section="## In flight"),
    CorpusSource("docs/briefs/INDEX.md", "heading_h2"),
    CorpusSource("docs/rejected_candidates.md", "heading_h3"),
    CorpusSource("docs/SESSIONS.md", "heading_h2", 24),
    CorpusSource("STATE.md", "heading_h2"),
    # Preserve existing membership, including INDEX/TOMBSTONES (see execution record).
    CorpusSource("docs/adr/*.md", "header_lines", 24),
    CorpusSource("docs/briefs/closures/*.md", "header_lines", 20),
    CorpusSource("docs/briefs/*.md", "header_lines", 24),
    CorpusSource("docs/briefs/programs/*.md", "header_lines", 24),
    CorpusSource("docs/notes/audits/**/*.md", "header_lines", 24),
    CorpusSource("docs/methodology/*.md", "header_lines", 24),
    CorpusSource("docs/spec/*.md", "header_lines", 24),
)


H3 = re.compile(r"^###\s+")
H2 = re.compile(r"^##\s+")
H1 = re.compile(r"^#\s+")


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _chunk(path: str, heading: str, body: str) -> dict[str, str]:
    text = f"{heading}\n{body}".strip()
    return {"path": path, "heading": heading.strip(), "text": text}


def _omit_h2_section(text: str, heading: str) -> str:
    """Drop a ``##`` section (heading + body until the next ``##``)."""
    out: list[str] = []
    skipping = False
    for line in text.splitlines():
        if line.startswith("## "):
            skipping = line.strip() == heading
            if skipping:
                continue
        if skipping:
            continue
        out.append(line)
    return "\n".join(out)


def chunk_by_heading(rel: str, text: str, heading_re: re.Pattern[str]) -> list[dict[str, str]]:
    chunks: list[dict[str, str]] = []
    current_h = rel
    buf: list[str] = []
    for line in text.splitlines():
        if heading_re.match(line):
            if buf:
                chunks.append(_chunk(rel, current_h, "\n".join(buf)))
            current_h = line.strip()
            buf = []
        else:
            buf.append(line)
    if buf:
        chunks.append(_chunk(rel, current_h, "\n".join(buf)))
    return chunks


def _collect_source(repo: Path, source: CorpusSource) -> list[dict[str, str]]:
    if source.mode not in {"catalog", "heading_h2", "heading_h3", "header_lines"}:
        raise ValueError(f"unsupported corpus mode: {source.mode}")
    if source.limit is not None and (type(source.limit) is not int or source.limit <= 0):
        raise ValueError("corpus limit must be a positive integer")
    if (source.mode == "catalog" and source.limit is not None
            or source.mode == "header_lines" and source.limit is None
            or source.omit_section is not None and source.mode != "catalog"):
        raise ValueError("invalid corpus mode/limit/section combination")
    chunks: list[dict[str, str]] = []
    for path in sorted(repo.glob(source.pattern)):
        # Literal sources required files; glob sources historically also read
        # matching directories through _read's empty-on-OSError behavior.
        if not any(c in source.pattern for c in "*?[") and not path.is_file():
            continue
        rel = path.relative_to(repo).as_posix()
        text = _read(path)
        if source.mode == "header_lines":
            lines = text.splitlines()[:source.limit]
            heading = next((line for line in lines if H1.match(line)), path.name)
            chunks.append(_chunk(rel, heading, "\n".join(lines)))
        else:
            if source.omit_section is not None:
                text = _omit_h2_section(text, source.omit_section)
            heading_re = H2 if source.mode == "heading_h2" else H3
            chunks.extend(chunk_by_heading(rel, text, heading_re)[:source.limit])
            if source.mode == "catalog":
                for line in text.splitlines():
                    if line.startswith("|") and ("ACTIVE" in line or "HOLD" in line):
                        cells = [c.strip() for c in line.strip("|").split("|")]
                        if cells and cells[0] not in {"slug", "---"}:
                            chunks.append(_chunk(rel, cells[0], line))
    return chunks


def collect_chunks(repo: Path) -> list[dict[str, str]]:
    return [chunk for source in CORPUS_SOURCES for chunk in _collect_source(repo, source)
            if chunk["text"].strip()]


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db_path)
    con.execute("PRAGMA foreign_keys=ON")
    return con


def _git_head(repo: Path) -> str | None:
    """Current commit SHA, or None if unavailable (not a git checkout, no git binary)."""
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo, capture_output=True, text=True, timeout=5, check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if out.returncode != 0:
        return None
    return out.stdout.strip() or None


def _stamped_head(db_path: Path) -> str | None:
    if not db_path.is_file():
        return None
    con = sqlite3.connect(db_path)
    try:
        row = con.execute("SELECT value FROM meta WHERE key='head_sha'").fetchone()
        return row[0] if row else None
    except sqlite3.OperationalError:
        return None
    finally:
        con.close()


def rebuild(repo: Path, db_path: Path) -> int:
    chunks = collect_chunks(repo)
    con = connect(db_path)
    try:
        con.execute("DROP TABLE IF EXISTS chunks")
        con.execute(
            "CREATE VIRTUAL TABLE chunks USING fts5(path, heading, text)"
        )
        con.executemany(
            "INSERT INTO chunks(path, heading, text) VALUES (?, ?, ?)",
            [(c["path"], c["heading"], c["text"]) for c in chunks],
        )
        # Stamp the HEAD this index was built against, so a caller can detect
        # drift (2026-08-15: the index previously never refreshed once built).
        con.execute("DROP TABLE IF EXISTS meta")
        con.execute("CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT)")
        head = _git_head(repo)
        if head is not None:
            con.execute("INSERT INTO meta (key, value) VALUES ('head_sha', ?)", (head,))
        con.commit()
    finally:
        con.close()
    return len(chunks)


def ensure_fresh(repo: Path, db_path: Path) -> bool:
    """Rebuild the index if it's missing or stale against HEAD. Returns True if rebuilt.

    If HEAD can't be determined (no git, no .git dir), falls back to
    build-if-missing only — there is nothing to compare staleness against.
    """
    if not db_path.is_file():
        rebuild(repo, db_path)
        return True
    current_head = _git_head(repo)
    if current_head is not None and _stamped_head(db_path) != current_head:
        rebuild(repo, db_path)
        return True
    return False


def query(db_path: Path, q: str, *, limit: int) -> list[tuple[str, str, str]]:
    if not db_path.is_file():
        return []
    con = connect(db_path)
    try:
        # Quote the query as an FTS phrase prefix bag so operators in the
        # user's text cannot break MATCH.
        terms = [t for t in re.findall(r"[A-Za-z0-9_./-]+", q) if len(t) > 1]
        if not terms:
            return []
        match = " OR ".join(f'"{t}"' for t in terms[:12])
        # ORDER BY rank: FTS5's built-in bm25-based relevance order. Its
        # absence (2026-08-14 -> 2026-08-15) meant results came back in
        # rowid/insertion order — see module docstring.
        rows = con.execute(
            "SELECT path, heading, snippet(chunks, 2, '>>>', '<<<', '…', 16) "
            "FROM chunks WHERE chunks MATCH ? ORDER BY rank LIMIT ?",
            (match, limit),
        ).fetchall()
        return [(str(a), str(b), str(c)) for a, b, c in rows]
    finally:
        con.close()


def main(argv: list[str] | None = None) -> int:
    # 2026-08-15: the prior hardcoded arrow/ellipsis characters crashed on
    # Windows cp1252 stdout before any output was ever printed. Reconfigure
    # to UTF-8 with graceful replacement rather than crashing; wrapped
    # because reconfigure() isn't available on every stream type a test
    # harness might substitute.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", type=Path, default=REPO)
    ap.add_argument("--db", type=Path, default=DEFAULT_DB)
    ap.add_argument("--rebuild", action="store_true")
    ap.add_argument("--query", type=str, default=None)
    ap.add_argument("--limit", type=int, default=8)
    args = ap.parse_args(argv)

    if args.rebuild:
        n = rebuild(args.repo, args.db)
        print(f"repo_retrieve: rebuilt {n} chunks -> {args.db}")
        if args.query is None:
            return 0

    if args.query is None:
        print("repo_retrieve: pass --query TEXT (and --rebuild on first use)",
              file=sys.stderr)
        return 2

    ensure_fresh(args.repo, args.db)

    hits = query(args.db, args.query, limit=args.limit)
    log_fire("repo_retrieve", query=args.query, n_hits=len(hits))
    if not hits:
        print(f"repo_retrieve: no hits for {args.query!r}")
        return 0
    print(f"repo_retrieve: {len(hits)} hit(s) for {args.query!r}")
    print("(paths + snippets — Read the owner; this index is not authority)")
    for path, heading, snip in hits:
        print(f"- {path}")
        print(f"    {heading}")
        print(f"    {snip.replace(chr(10), ' ')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
