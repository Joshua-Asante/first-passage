"""Unit tests for scripts/repo_retrieve.py — Q-XMEM-1 Limb B FTS."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
_SPEC = importlib.util.spec_from_file_location(
    "repo_retrieve", REPO / "scripts" / "repo_retrieve.py"
)
rr = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = rr
_SPEC.loader.exec_module(rr)


def _mini_repo(tmp_path: Path) -> Path:
    (tmp_path / "lab").mkdir()
    (tmp_path / "docs" / "briefs" / "closures").mkdir(parents=True)
    (tmp_path / "docs" / "adr").mkdir(parents=True)
    (tmp_path / "docs" / "ltm" / "briefs").mkdir(parents=True)
    (tmp_path / "lab" / "archive" / "spent").mkdir(parents=True)
    (tmp_path / "docs" / "notes" / "audits" / "programme-audit").mkdir(parents=True)
    (tmp_path / "docs" / "notes" / "notice").mkdir(parents=True)
    (tmp_path / "docs" / "methodology").mkdir(parents=True)
    (tmp_path / "docs" / "spec").mkdir(parents=True)

    (tmp_path / "lab" / "CATALOG.md").write_text(
        "# Catalog\n\n### Active\n\n"
        "| slug | theme | status | one-liner | path | card |\n"
        "|---|---|---|---|---|---|\n"
        "| magdon_ismail_mdd | risk | ACTIVE | closed-form MDD | lab/analysis/x/ | — |\n",
        encoding="utf-8",
    )
    (tmp_path / "docs" / "briefs" / "INDEX.md").write_text(
        "# Roster\n\n## Open\n\n| Q | Status |\n|---|---|\n"
        "| **Q-XMEM-1** | OPEN |\n",
        encoding="utf-8",
    )
    (tmp_path / "docs" / "rejected_candidates.md").write_text(
        "# Rejected\n\n### Magdon-Ismail closed-form MDD\n\nbarred.\n",
        encoding="utf-8",
    )
    (tmp_path / "docs" / "SESSIONS.md").write_text(
        "# Sessions\n\n## 2026-08-15a — retrieve\n\nFocus: FTS.\n",
        encoding="utf-8",
    )
    (tmp_path / "STATE.md").write_text(
        "# State\n\n## Queue\n\n- retrieve limb unpaid\n",
        encoding="utf-8",
    )
    (tmp_path / "docs" / "adr" / "2026-06-16-rule-2-budget-before-acting.md").write_text(
        "# ADR 2026-06-16 — Rule 2\n\n**Status:** `PROPOSED`\n",
        encoding="utf-8",
    )
    (tmp_path / "docs" / "briefs" / "closures" / "Q-X-closure-falsified.md").write_text(
        "# Q-X — CLOSURE: FALSIFIED\n\n**Verdict:** FALSIFIED\n",
        encoding="utf-8",
    )
    (tmp_path / "docs" / "ltm" / "briefs" / "secret.md").write_text(
        "LTM body must never be indexed Magdon-Ismail\n",
        encoding="utf-8",
    )
    (tmp_path / "lab" / "archive" / "spent" / "RESULTS.md").write_text(
        "archive body Magdon-Ismail must never be indexed\n",
        encoding="utf-8",
    )
    (tmp_path / "docs" / "briefs" / "Q-SAMPLE-brief.md").write_text(
        "# Q-SAMPLE — a brief body\n\nMagdon-Ismail context.\n",
        encoding="utf-8",
    )
    (tmp_path / "docs" / "notes" / "audits" / "2026-01-01-sample-audit.md").write_text(
        "# Sample audit\n\nMagdon-Ismail top-level audit.\n",
        encoding="utf-8",
    )
    (tmp_path / "docs" / "notes" / "audits" / "programme-audit" / "2026-01-01-nested-audit.md").write_text(
        "# Nested programme audit\n\nMagdon-Ismail nested audit.\n",
        encoding="utf-8",
    )
    (tmp_path / "docs" / "notes" / "notice" / "N-2026-01-01-sample-notice.md").write_text(
        "notice body must never be indexed — only docs/notes/audits/ is in scope\n",
        encoding="utf-8",
    )
    (tmp_path / "docs" / "methodology" / "sample_method.md").write_text(
        "# Sample methodology\n\nMagdon-Ismail method context.\n",
        encoding="utf-8",
    )
    (tmp_path / "docs" / "spec" / "sample_spec.md").write_text(
        "# Sample spec\n\nMagdon-Ismail spec context.\n",
        encoding="utf-8",
    )
    return tmp_path


def test_collect_chunks_hot_surfaces_only(tmp_path):
    repo = _mini_repo(tmp_path)
    chunks = rr.collect_chunks(repo)
    paths = {c["path"] for c in chunks}
    assert "lab/CATALOG.md" in paths
    assert "docs/briefs/INDEX.md" in paths
    assert "docs/rejected_candidates.md" in paths
    assert "docs/SESSIONS.md" in paths
    assert "STATE.md" in paths
    assert any(p.startswith("docs/adr/") for p in paths)
    assert any(p.startswith("docs/briefs/closures/") for p in paths)
    assert not any("docs/ltm/" in p for p in paths)
    assert not any("lab/archive/" in p for p in paths)


def test_collect_chunks_v3_widened_surfaces(tmp_path):
    """2026-08-15 v3 remeasurement widening — one-revision cap."""
    repo = _mini_repo(tmp_path)
    chunks = rr.collect_chunks(repo)
    paths = {c["path"] for c in chunks}
    assert "docs/briefs/Q-SAMPLE-brief.md" in paths
    assert "docs/notes/audits/2026-01-01-sample-audit.md" in paths
    assert "docs/notes/audits/programme-audit/2026-01-01-nested-audit.md" in paths
    assert "docs/methodology/sample_method.md" in paths
    assert "docs/spec/sample_spec.md" in paths
    # docs/notes/notice/ is a sibling of docs/notes/audits/, not itself in
    # scope -- only the audits/ subtree widened, per the frozen prereg.
    assert not any("docs/notes/notice/" in p for p in paths)


def test_rebuild_and_query_returns_paths(tmp_path):
    repo = _mini_repo(tmp_path)
    db = tmp_path / "idx.sqlite"
    n = rr.rebuild(repo, db)
    assert n > 0
    hits = rr.query(db, "Magdon-Ismail closed-form MDD", limit=8)
    assert hits
    hit_paths = {p for p, _h, _s in hits}
    assert "docs/rejected_candidates.md" in hit_paths or "lab/CATALOG.md" in hit_paths
    assert not any("docs/ltm/" in p for p in hit_paths)
    assert not any("lab/archive/" in p for p in hit_paths)


def test_cli_rebuild_then_query(tmp_path):
    repo = _mini_repo(tmp_path)
    db = tmp_path / "idx.sqlite"
    rc = rr.main(["--repo", str(repo), "--db", str(db), "--rebuild",
                  "--query", "Q-XMEM-1", "--limit", "4"])
    assert rc == 0


def _ranking_repo(tmp_path: Path) -> Path:
    """A repo shaped to distinguish ranked from rowid-order results.

    8 decoy CATALOG rows each mention the probe term once (weak match) and
    are inserted first (collect_chunks scans lab/CATALOG.md before
    docs/briefs/closures/). One closure, inserted last, mentions the probe
    term many times (strong bm25 match). Without ORDER BY rank, a LIMIT-5
    query returns rowid order — the first 5 decoys, never the target.
    """
    (tmp_path / "lab").mkdir()
    (tmp_path / "docs" / "briefs" / "closures").mkdir(parents=True)

    rows = "\n".join(
        f"| decoy_{i} | risk | ACTIVE | mentions zzzprobe once | lab/analysis/decoy_{i}/ | — |"
        for i in range(8)
    )
    (tmp_path / "lab" / "CATALOG.md").write_text(
        "# Catalog\n\n### Active\n\n"
        "| slug | theme | status | one-liner | path | card |\n"
        "|---|---|---|---|---|---|\n" + rows + "\n",
        encoding="utf-8",
    )
    (tmp_path / "docs" / "briefs" / "closures" / "Q-TARGET-closure-resolved.md").write_text(
        "# Q-TARGET — CLOSURE: RESOLVED\n\n"
        "zzzprobe zzzprobe zzzprobe zzzprobe zzzprobe — the strong match.\n",
        encoding="utf-8",
    )
    return tmp_path


def test_query_ranks_strongest_match_first_not_insertion_order(tmp_path):
    """Adversarial: fails if ORDER BY rank is dropped from query()'s SQL."""
    repo = _ranking_repo(tmp_path)
    db = tmp_path / "idx.sqlite"
    rr.rebuild(repo, db)

    hits = rr.query(db, "zzzprobe", limit=5)
    hit_paths = [p for p, _h, _s in hits]
    assert "docs/briefs/closures/Q-TARGET-closure-resolved.md" in hit_paths, (
        "the strong bm25 match was inserted last and did not surface in the "
        "top 5 — ranking is not applying (rowid/insertion order instead)"
    )

    # Confirm the fixture actually distinguishes the two orderings: an
    # unranked rowid-order query over the same table must miss the target.
    import sqlite3
    con = sqlite3.connect(db)
    try:
        unranked = con.execute(
            "SELECT path FROM chunks WHERE chunks MATCH ? LIMIT 5", ('"zzzprobe"',)
        ).fetchall()
    finally:
        con.close()
    unranked_paths = [p for (p,) in unranked]
    assert "docs/briefs/closures/Q-TARGET-closure-resolved.md" not in unranked_paths, (
        "fixture is not discriminating — rowid order already surfaces the "
        "target, so this test cannot detect a missing ORDER BY rank"
    )


def test_ensure_fresh_rebuilds_on_head_drift(tmp_path, monkeypatch):
    repo = _mini_repo(tmp_path)
    db = tmp_path / "idx.sqlite"

    monkeypatch.setattr(rr, "_git_head", lambda _repo: "sha-aaa")
    assert rr.ensure_fresh(repo, db) is True
    assert rr._stamped_head(db) == "sha-aaa"

    # Same HEAD -> no rebuild needed.
    assert rr.ensure_fresh(repo, db) is False

    # HEAD moved -> must rebuild and re-stamp.
    monkeypatch.setattr(rr, "_git_head", lambda _repo: "sha-bbb")
    assert rr.ensure_fresh(repo, db) is True
    assert rr._stamped_head(db) == "sha-bbb"


def test_ensure_fresh_falls_back_when_head_unknown(tmp_path, monkeypatch):
    repo = _mini_repo(tmp_path)
    db = tmp_path / "idx.sqlite"
    monkeypatch.setattr(rr, "_git_head", lambda _repo: None)
    assert rr.ensure_fresh(repo, db) is True   # missing -> build regardless
    assert rr.ensure_fresh(repo, db) is False  # exists, nothing to compare -> no-op


def test_cli_handles_non_ascii_snippet_without_crashing(tmp_path, capsys):
    """Regression: the prior hardcoded arrow/ellipsis chars crashed on cp1252 stdout."""
    repo = _mini_repo(tmp_path)
    db = tmp_path / "idx.sqlite"
    rc = rr.main(["--repo", str(repo), "--db", str(db), "--rebuild",
                  "--query", "Magdon-Ismail closed-form MDD", "--limit", "4"])
    assert rc == 0
