"""FTS5 index, search, and guarded staged-write store for the recall sidecar.

Q-XMEM-1's Delete route (parent brief Phase A2). Retrieval is deterministic and
verbatim — there is no LLM anywhere in this path. That is the whole point: it
DELETES the extraction-LLM/embedder exposure boundary rather than localising
it, which is what let the Rule-7 denylist become a mechanical reject-list
(see `guard.py`).

Two invariants worth stating because they are easy to erode:

1. **The cold store is indexed.** `.rgignore` hides `lab/archive/` and
   `docs/ltm/` from default agent search, which is the documented trap where an
   empty Grep reads as "no prior work". An index that inherited that blindness
   would reproduce the defect it exists to fix.

2. **Scope is search + staged write. There is no summarisation surface.**
   Adding one re-creates the retired `weekly_review_feeder`. The frozen scope
   is a guard against that, and `test_no_summarisation_surface_exists` pins it.

Staged notes live in their own table and are NOT promoted into the document
corpus — they are staged for operator review, never treated as authority.
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

from ops.recall import guard

_SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__"}

_SCHEMA = """
CREATE VIRTUAL TABLE IF NOT EXISTS docs USING fts5(path, body);
CREATE TABLE IF NOT EXISTS notes (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    text    TEXT NOT NULL,
    created TEXT NOT NULL DEFAULT (datetime('now'))
);
"""


# Low-information words. Found by real usage 2026-07-27: "did we ever try five
# minute bars" pushed the correct cold-store doc out of the top 4 entirely,
# while the same question in corpus vocabulary returned it at ranks 1-3. Under
# OR semantics these terms match most of the corpus and dilute bm25.
_STOPWORDS = frozenset("""
a an and are as at be been but by can did do does for from had has have how
into is it its may not now of on or our out over should so than that the their
then there these they this those to try use used using was were what when
where which who why will with would you your ever any some more most just
""".split())


@dataclass(frozen=True)
class Hit:
    path: str
    snippet: str
    matched_terms: int = 0
    query_terms: int = 0

    @property
    def weak(self) -> bool:
        """True when the hit covers too little of the query to trust.

        A nonsense query still returns whatever shares one common word — the
        control query "quantum computing portfolio optimization" matched "cent
        quantum" in a rounding ADR. Coverage is the honest signal that a result
        is incidental rather than an answer.
        """
        if self.query_terms <= 1:
            return False
        return self.matched_terms * 2 < self.query_terms


@dataclass(frozen=True)
class Note:
    id: int
    text: str
    created: str


def open_db(path: Path | str) -> sqlite3.Connection:
    conn = sqlite3.connect(str(path))
    conn.executescript(_SCHEMA)
    return conn


def _iter_markdown(root: Path):
    for p in sorted(root.rglob("*.md")):
        if _SKIP_DIRS & set(p.parts):
            continue
        try:
            yield p, p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue


def build(conn: sqlite3.Connection, root: Path) -> int:
    """(Re)build the document index. Idempotent — replaces prior contents."""
    root = Path(root)
    conn.execute("DELETE FROM docs")
    rows = [(str(p.relative_to(root).as_posix()), body)
            for p, body in _iter_markdown(root)]
    conn.executemany("INSERT INTO docs(path, body) VALUES (?,?)", rows)
    conn.commit()
    return len(rows)


def doc_count(conn: sqlite3.Connection) -> int:
    return conn.execute("SELECT count(*) FROM docs").fetchone()[0]


def all_paths(conn: sqlite3.Connection) -> list[str]:
    return [r[0] for r in conn.execute("SELECT path FROM docs")]


def _terms(query: str) -> list[str]:
    seen, out = set(), []
    for raw in query.lower().split():
        t = "".join(ch for ch in raw if ch.isalnum() or ch in "-_")
        if len(t) > 2 and t not in _STOPWORDS and t not in seen:
            seen.add(t)
            out.append(t)
    return out


def _match_expr(query: str) -> str:
    return " OR ".join(f'"{t}"' for t in _terms(query))


def search(conn: sqlite3.Connection, query: str, limit: int = 10) -> list[Hit]:
    terms = _terms(query)
    if not terms:
        return []
    try:
        rows = conn.execute(
            "SELECT path, snippet(docs, 1, '', '', '…', 12), body "
            "FROM docs WHERE docs MATCH ? ORDER BY bm25(docs) LIMIT ?",
            (" OR ".join(f'"{t}"' for t in terms), limit),
        ).fetchall()
    except sqlite3.OperationalError:
        return []
    hits = []
    for path, snippet, body in rows:
        low = body.lower()
        hits.append(Hit(
            path=path,
            snippet=snippet,
            matched_terms=sum(1 for t in terms if t in low),
            query_terms=len(terms),
        ))
    return hits


def stage_note(conn: sqlite3.Connection, text: str,
               repo_root: Path) -> guard.Verdict:
    """Write a note for operator review, refusing Rule-7 content outright."""
    verdict = guard.check(text, guard.load_denylist(Path(repo_root)))
    if not verdict.ok:
        return verdict
    conn.execute("INSERT INTO notes(text) VALUES (?)", (text,))
    conn.commit()
    return verdict


def staged_notes(conn: sqlite3.Connection) -> list[Note]:
    return [Note(*r) for r in conn.execute(
        "SELECT id, text, created FROM notes ORDER BY id")]
