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
