#!/usr/bin/env python3
"""Repo-local retrieval over hot liveness surfaces (Q-XMEM-1 Limb B).

Not a Rule-7 owner. Returns paths + snippets; the agent must Read the owner.
Does not ingest docs/ltm/ or lab/archive/ bodies (LTM stays catalog-gated).

FTS5 over a curated hot corpus is the cheap slice. A local-embedder vector
slot is documented in Q-XMEM-1 v1.2 and is not built here.

Usage:
  python scripts/repo_retrieve.py --rebuild
  python scripts/repo_retrieve.py --query "Magdon-Ismail closed-form MDD"
"""
from __future__ import annotations

import argparse
import re
import sqlite3
import sys
from pathlib import Path

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
        con.commit()
    finally:
        con.close()
    return len(chunks)


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
        rows = con.execute(
            "SELECT path, heading, snippet(chunks, 2, '>>>', '<<<', '…', 16) "
            "FROM chunks WHERE chunks MATCH ? LIMIT ?",
            (match, limit),
        ).fetchall()
        return [(str(a), str(b), str(c)) for a, b, c in rows]
    finally:
        con.close()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", type=Path, default=REPO)
    ap.add_argument("--db", type=Path, default=DEFAULT_DB)
    ap.add_argument("--rebuild", action="store_true")
    ap.add_argument("--query", type=str, default=None)
    ap.add_argument("--limit", type=int, default=8)
    args = ap.parse_args(argv)

    if args.rebuild:
        n = rebuild(args.repo, args.db)
        print(f"repo_retrieve: rebuilt {n} chunks → {args.db}")
        if args.query is None:
            return 0

    if args.query is None:
        print("repo_retrieve: pass --query TEXT (and --rebuild on first use)",
              file=sys.stderr)
        return 2

    if not args.db.is_file():
        rebuild(args.repo, args.db)

    hits = query(args.db, args.query, limit=args.limit)
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
