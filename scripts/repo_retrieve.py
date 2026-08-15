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
once built). None of this re-authorizes the tool for Rule 8 sub-rule 8/10
attestations — that is Phase 2: a frozen v3 pre-registration re-measures
this exact file against the same 0.70 / R_fts5 > R_rg table before its
output is trusted again. The `check_advisor_dedup.py` companion call stays
disabled until that measurement lands.

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

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gate_fire_log import log_fire  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
DEFAULT_DB = REPO / ".cache" / "repo_retrieve.sqlite"

# Hot surfaces only. LTM / archive bodies are excluded by construction.
HOT_FILES = (
    "lab/CATALOG.md",
    "docs/briefs/INDEX.md",
    "docs/rejected_candidates.md",
    "docs/SESSIONS.md",
    "STATE.md",
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


def collect_chunks(repo: Path) -> list[dict[str, str]]:
    chunks: list[dict[str, str]] = []

    catalog = repo / "lab" / "CATALOG.md"
    if catalog.is_file():
        chunks.extend(chunk_by_heading("lab/CATALOG.md", _read(catalog), H3))
        # Table rows are the actual liveness units.
        for line in _read(catalog).splitlines():
            if line.startswith("|") and ("ACTIVE" in line or "HOLD" in line):
                cells = [c.strip() for c in line.strip("|").split("|")]
                if cells and cells[0] not in {"slug", "---"}:
                    chunks.append(_chunk("lab/CATALOG.md", cells[0], line))

    index = repo / "docs" / "briefs" / "INDEX.md"
    if index.is_file():
        chunks.extend(chunk_by_heading("docs/briefs/INDEX.md", _read(index), H2))

    rejected = repo / "docs" / "rejected_candidates.md"
    if rejected.is_file():
        chunks.extend(chunk_by_heading("docs/rejected_candidates.md", _read(rejected), H3))

    sessions = repo / "docs" / "SESSIONS.md"
    if sessions.is_file():
        sess_chunks = chunk_by_heading("docs/SESSIONS.md", _read(sessions), H2)
        chunks.extend(sess_chunks[:24])  # newest-first file; keep a working window

    state = repo / "STATE.md"
    if state.is_file():
        chunks.extend(chunk_by_heading("STATE.md", _read(state), H2))

    adr_dir = repo / "docs" / "adr"
    if adr_dir.is_dir():
        for path in sorted(adr_dir.glob("*.md")):
            if path.name.upper() == "INDEX.md" or path.name.upper() == "TOMBSTONES.md":
                continue
            lines = _read(path).splitlines()[:24]
            heading = next((l for l in lines if H1.match(l)), path.name)
            chunks.append(_chunk(f"docs/adr/{path.name}", heading, "\n".join(lines)))

    closures = repo / "docs" / "briefs" / "closures"
    if closures.is_dir():
        for path in sorted(closures.glob("*.md")):
            lines = _read(path).splitlines()[:20]
            heading = next((l for l in lines if H1.match(l)), path.name)
            chunks.append(
                _chunk(f"docs/briefs/closures/{path.name}", heading, "\n".join(lines))
            )

    return [c for c in chunks if c["text"].strip()]


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
