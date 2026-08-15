"""Controls for the recall sidecar's index, search, and staged-write store.

Scope is frozen by the parent brief at SEARCH + STAGED WRITE. There is
deliberately no summarisation path — that is how the retired
weekly_review_feeder came back, and the frozen scope exists to prevent it.

The cold-store control is the load-bearing one: `.rgignore` hides
`lab/archive/` and `docs/ltm/` from default agent search, which produced the
documented "empty Grep over LTM reads as no prior work" trap. An index that
inherits that blindness would reproduce the defect it exists to fix.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from ops.recall import index as rindex  # noqa: E402


@pytest.fixture()
def corpus(tmp_path: Path) -> Path:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "live.md").write_text(
        "# Trailing drawdown survival\nskew governs the loss side.",
        encoding="utf-8")
    (tmp_path / "docs" / "ltm").mkdir()
    (tmp_path / "docs" / "ltm" / "cold.md").write_text(
        "# Retired feeder\nthe weekly review feeder was retired.",
        encoding="utf-8")
    (tmp_path / "lab" / "archive" / "old_study").mkdir(parents=True)
    (tmp_path / "lab" / "archive" / "old_study" / "RESULTS.md").write_text(
        "# Opening pressure\nfalsified on hash pinned bar export.",
        encoding="utf-8")
    (tmp_path / "notes.txt").write_text("not markdown", encoding="utf-8")
    return tmp_path


@pytest.fixture()
def db(corpus: Path, tmp_path: Path):
    conn = rindex.open_db(tmp_path / "recall.db")
    rindex.build(conn, corpus)
    return conn


# --- indexing ---------------------------------------------------------------

def test_indexes_markdown_only(db):
    assert rindex.doc_count(db) == 3          # not notes.txt


def test_indexes_cold_store(db):
    """lab/archive and docs/ltm are hidden from rg by .rgignore - index them."""
    paths = {Path(p).name for p in rindex.all_paths(db)}
    assert "cold.md" in paths
    assert "RESULTS.md" in paths


def test_search_finds_cold_store_document(db):
    """The documented empty-Grep-over-LTM trap, closed."""
    hits = rindex.search(db, "weekly review feeder retired", limit=5)
    assert any("cold.md" in h.path for h in hits)


def test_search_ranks_and_limits(db):
    hits = rindex.search(db, "drawdown skew loss", limit=1)
    assert len(hits) == 1
    assert "live.md" in hits[0].path


def test_search_returns_snippet(db):
    hits = rindex.search(db, "skew governs", limit=3)
    assert hits and hits[0].snippet.strip()


def test_rebuild_is_idempotent(db, corpus):
    rindex.build(db, corpus)
    assert rindex.doc_count(db) == 3


def test_search_empty_query_returns_nothing(db):
    assert rindex.search(db, "   ", limit=5) == []


# --- staged write (guarded) -------------------------------------------------

def test_staged_note_is_written_and_searchable(db):
    r = rindex.stage_note(db, "pointer: falsifier RESULTS for the delete route",
                          repo_root=_REPO_ROOT)
    assert r.ok, r.reason
    assert any("delete route" in n.text for n in rindex.staged_notes(db))


def test_staged_write_refuses_rule7_content(db):
    r = rindex.stage_note(db, "DJ30 risk is 0.70% per trade", repo_root=_REPO_ROOT)
    assert not r.ok
    assert "0.70" in r.reason
    assert rindex.staged_notes(db) == []      # nothing persisted


def test_staged_notes_do_not_pollute_corpus_search(db):
    """Notes are staged for review, not promoted into the document corpus."""
    rindex.stage_note(db, "pointer: unrelated scratch note", repo_root=_REPO_ROOT)
    assert rindex.doc_count(db) == 3


def test_no_summarisation_surface_exists():
    """Frozen scope: search + staged write only (retired feeder guard)."""
    for banned in ("summarise", "summarize", "digest", "rollup"):
        assert not hasattr(rindex, banned)


# --- query hygiene: real-usage defects found 2026-07-27 ---------------------
#
# Running natural-language questions against the sidecar surfaced two defects:
#   1. Low-information words ("did we ever try...") diluted bm25 ranking enough
#      to push the correct cold-store doc out of the top 4 entirely, while the
#      same question in corpus vocabulary returned it at ranks 1-3.
#   2. A nonsense control query returned four confident-looking hits with no
#      signal that nothing relevant existed ("quantum" matched "cent quantum").

def test_stopwords_are_dropped_from_match(db):
    """'did we ever try five minute bars' must not query on did/ever/try."""
    expr = rindex._match_expr("did we ever try five minute bars")
    for junk in ("did", "ever", "try", "was", "the"):
        assert junk not in expr, f"stopword {junk!r} leaked into: {expr}"
    assert "minute" in expr


def test_stopword_only_query_returns_nothing(db):
    assert rindex.search(db, "did we ever have the", limit=5) == []


def test_hit_reports_matched_term_count(db):
    hits = rindex.search(db, "drawdown skew loss", limit=1)
    assert hits[0].matched_terms >= 1
    assert hits[0].query_terms == 3


def test_low_coverage_hit_is_flagged_weak(db):
    """A hit matching one term out of several is not a confident answer."""
    hits = rindex.search(db, "skew unrelatedwordone unrelatedwordtwo", limit=1)
    assert hits and hits[0].weak is True


def test_full_coverage_hit_is_not_weak(db):
    hits = rindex.search(db, "trailing drawdown skew", limit=1)
    assert hits and hits[0].weak is False
