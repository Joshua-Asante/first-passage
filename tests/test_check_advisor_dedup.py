"""Unit tests for scripts/check_advisor_dedup.py -- advisor-intake prior-art search.

Synthetic fixtures pin the mechanics (slug extraction, digit-gating, corpus
loading per surface, ranking) so correctness doesn't depend on the live corpus
staying stable. The acid test -- does this actually surface the real
Q-ICT-1-closure-moot.md / gate-audit prior art for the two files that
motivated it -- was run manually against the live repo (both rank in the top
2, driven by slug match) and is not repeated here as an automated test,
since asserting exact rank against a corpus that grows every session would
itself be a source of spurious test breakage.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_PATH = REPO_ROOT / "scripts" / "check_advisor_dedup.py"
_spec = importlib.util.spec_from_file_location("check_advisor_dedup", _PATH)
cad = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = cad
_spec.loader.exec_module(cad)


def test_extract_terms_finds_digited_slugs():
    slugs, _ = cad.extract_terms("This closes Q-ICT-1 and forks Q-ARCH-1, blocked by S-MYM-ORC-02.")
    assert slugs == {"Q-ICT-1", "Q-ARCH-1", "S-MYM-ORC-02"}


def test_extract_terms_drops_digitless_template_tokens():
    """PRE-Q, D-S-A, RESOLVED-REAL are generic Pre-Q brief boilerplate, not
    identifying slugs -- every staged brief shares them, so treating them as
    identity anchors would dilute the signal (regression: an earlier cut of
    this tool counted them, inflating slug-match scores on unrelated briefs)."""
    slugs, _ = cad.extract_terms("**Type:** PRE-Q brief. **D-S-A domain:** data. Verdict RESOLVED-REAL.")
    assert slugs == set()


def test_extract_terms_strips_markdown_before_keywords():
    _, keywords = cad.extract_terms("# Title\n\nSee [`the link`](docs/adr/x.md) for **bold** detail.")
    assert "bold" in keywords
    assert "detail" in keywords
    # markdown syntax chars must not survive into keyword tokens
    assert not any("`" in k or "*" in k for k in keywords)


def test_extract_terms_ignores_stopwords():
    _, keywords = cad.extract_terms("this that with from into before after brief closure status")
    assert keywords == set()


def test_title_of_prefers_first_heading():
    assert cad._title_of("# Real Title\n\nbody", "fallback") == "Real Title"
    assert cad._title_of("no heading here", "fallback") == "fallback"


def test_split_by_h2_groups_sessions_entries():
    text = (
        "# Session Log\n\nintro\n\n"
        "## 2026-01-01 -- first entry\n\nbody one\n\n"
        "## 2026-01-02 -- second entry\n\nbody two\n"
    )
    parts = cad._split_by_h2(text)
    assert len(parts) == 3  # preamble + 2 entries
    assert "first entry" in parts[1]
    assert "second entry" in parts[2]
    assert "first entry" not in parts[2]


def test_split_by_h3_groups_rejected_candidates_entries():
    text = (
        "# Rejected candidates\n\n## Entries\n\n"
        "### Guardian on XAGUSD\n\nrejected reasoning\n\n"
        "### Custodian on EURUSD\n\nother reasoning\n"
    )
    parts = cad._split_by_h3(text)
    assert len(parts) == 2
    assert all(p.lstrip().startswith("### ") for p in parts)
    assert "Guardian" in parts[0]
    assert "Custodian" in parts[1]


def test_load_corpus_reads_all_eight_surfaces(tmp_path: Path):
    (tmp_path / "docs" / "briefs" / "closures").mkdir(parents=True)
    (tmp_path / "docs" / "notes" / "audits").mkdir(parents=True)
    (tmp_path / "docs" / "briefs" / "rnd-pipeline").mkdir(parents=True)
    (tmp_path / "docs" / "adr").mkdir(parents=True)
    (tmp_path / "docs").mkdir(exist_ok=True)
    (tmp_path / "lab").mkdir(exist_ok=True)
    (tmp_path / "ops" / "instruments").mkdir(parents=True)

    (tmp_path / "docs" / "briefs" / "closures" / "Q-X-1-closure.md").write_text(
        "# Q-X-1 -- closure MOOT\n\nQ-X-1 details here.\n", encoding="utf-8")
    (tmp_path / "docs" / "notes" / "audits" / "audit-note.md").write_text(
        "# Audit note\n\nQ-X-1 audit context.\n", encoding="utf-8")
    (tmp_path / "docs" / "SESSIONS.md").write_text(
        "# Session Log\n\n## 2026-01-01 -- Q-X-1 session\n\nQ-X-1 work happened.\n",
        encoding="utf-8")
    (tmp_path / "lab" / "CATALOG.md").write_text(
        "| slug | status | one-liner | card | body | heavy | closed |\n"
        "|---|---|---|---|---|---|---|\n"
        "| q_x_1_2026 | CLOSED | Q-X-1 study | c | b | - | - |\n",
        encoding="utf-8")
    (tmp_path / "docs" / "rejected_candidates.md").write_text(
        "# Rejected\n\n## Entries\n\n### Q-X-1 rejected sub-thesis\n\ndetail\n",
        encoding="utf-8")
    (tmp_path / "ops" / "instruments" / "ZZZ.md").write_text(
        "# INSTRUMENT LEDGER -- ZZZ\n\nQ-X-1 finding lives here too.\n", encoding="utf-8")
    (tmp_path / "docs" / "briefs" / "rnd-pipeline" / "Q-X-1-rescope.md").write_text(
        "# Campaign scoping -- Q-X-1 rescope\n\nQ-X-1 rescope detail.\n", encoding="utf-8")
    (tmp_path / "docs" / "adr" / "2026-01-01-q-x-1-ruling.md").write_text(
        "# ADR: Q-X-1 ruling\n\nQ-X-1 decided here.\n", encoding="utf-8")
    (tmp_path / "docs" / "adr" / "INDEX.md").write_text(
        "# ADR index (derived)\n\nQ-X-1 must not surface from this scaffolding file.\n",
        encoding="utf-8")
    (tmp_path / "docs" / "adr" / "README.md").write_text(
        "# docs/adr/\n\nQ-X-1 must not surface from this scaffolding file.\n", encoding="utf-8")
    (tmp_path / "docs" / "adr" / "TOMBSTONES.md").write_text(
        "# ADR Tombstone Index\n\nQ-X-1 must not surface from this scaffolding file.\n",
        encoding="utf-8")

    chunks = cad.load_corpus(tmp_path)
    surfaces = {c.surface for c in chunks}
    assert "docs/briefs/closures/Q-X-1-closure.md" in surfaces
    assert "docs/notes/audits/audit-note.md" in surfaces
    assert any(c.surface == "docs/SESSIONS.md" and "Q-X-1 session" in c.label for c in chunks)
    assert any(c.surface == "lab/CATALOG.md" and c.label == "q_x_1_2026" for c in chunks)
    assert any(c.surface == "docs/rejected_candidates.md" and "Q-X-1 rejected" in c.label for c in chunks)
    assert any(c.surface == "ops/instruments/ZZZ.md" and "ZZZ" in c.label for c in chunks)
    assert any(c.surface == "docs/briefs/rnd-pipeline/Q-X-1-rescope.md" for c in chunks)
    assert any(c.surface == "docs/adr/2026-01-01-q-x-1-ruling.md" for c in chunks)
    assert "docs/adr/INDEX.md" not in surfaces
    assert "docs/adr/README.md" not in surfaces
    assert "docs/adr/TOMBSTONES.md" not in surfaces


def test_score_prioritizes_slug_match_over_keyword_volume():
    """A chunk sharing the exact slug but few keywords must outrank a chunk
    sharing many keywords but no slug -- the whole point of the slug/keyword
    split (see the module docstring's motivating incident)."""
    staged_slugs, staged_keywords = cad.extract_terms(
        "Q-ICT-1 timeframe residual selection gate falsifiable hypothesis")
    slug_chunk = cad.Chunk("a.md", "unrelated title", "Q-ICT-1 is mentioned here, nothing else shared.")
    keyword_chunk = cad.Chunk("b.md", "unrelated title",
                              "timeframe residual selection gate falsifiable hypothesis "
                              "but no shared identifier at all in this chunk of prose")
    slug_score = cad.score(staged_slugs, staged_keywords, slug_chunk)[0]
    keyword_score = cad.score(staged_slugs, staged_keywords, keyword_chunk)[0]
    assert slug_score > keyword_score


def test_main_exits_zero_even_with_no_corpus(tmp_path: Path):
    staged = tmp_path / "staged.md"
    staged.write_text("# New topic\n\nQ-NEW-1 nothing shares this.\n", encoding="utf-8")
    empty_root = tmp_path / "empty_repo"
    empty_root.mkdir()
    rc = cad.main([str(staged), "--repo-root", str(empty_root)])
    assert rc == 0


def test_main_exits_zero_on_missing_staged_file(tmp_path: Path):
    rc = cad.main([str(tmp_path / "does-not-exist.md")])
    assert rc == 0


def test_main_keywords_mode_exits_zero(tmp_path: Path):
    """--keywords is mutually exclusive with staged_file; always exit 0."""
    empty_root = tmp_path / "empty_repo"
    empty_root.mkdir()
    rc = cad.main(["--keywords", "Magdon-Ismail closed-form", "--repo-root", str(empty_root)])
    assert rc == 0


def test_main_rejects_both_inputs_but_exits_zero(tmp_path: Path):
    staged = tmp_path / "staged.md"
    staged.write_text("noise\n", encoding="utf-8")
    rc = cad.main([str(staged), "--keywords", "also"])
    assert rc == 0
