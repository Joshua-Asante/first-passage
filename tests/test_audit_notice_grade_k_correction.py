"""Synthetic fixtures for scripts/audit_notice_grade_k_correction.py.

Does not depend on the live docs/notes/notice corpus.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "lab"))

import audit_notice_grade_k_correction as audit  # noqa: E402


def _write_notice(repo: Path, name: str, body: str) -> Path:
    d = repo / "docs" / "notes" / "notice"
    d.mkdir(parents=True, exist_ok=True)
    p = d / name
    p.write_text(body, encoding="utf-8")
    return p


def _write_manifest(repo: Path, name: str, k: object) -> Path:
    d = repo / "discovery_manifests"
    d.mkdir(parents=True, exist_ok=True)
    p = d / name
    p.write_text(json.dumps({"K": k}), encoding="utf-8")
    return p


def _run(repo: Path, capsys):
    code = audit.main(["--repo-root", str(repo)])
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def test_graduate_high_k_flagged(tmp_path, capsys):
    _write_manifest(tmp_path, "high.json", 5)
    _write_notice(
        tmp_path,
        "N-2026-01-01-high.md",
        "**Status:** `OPEN` — GRADUATE\n\nSee discovery_manifests/high.json\n",
    )
    code, out, err = _run(tmp_path, capsys)
    assert code == 0
    assert "N-2026-01-01-high.md" in out
    assert "discovery_manifests/high.json" in out
    assert "K=5" in out
    assert "[audit] 1 flagged / 1 GRADUATE/INCREMENT notices scanned / 1 total notices" in out
    assert err == ""


def test_graduate_in_band_k_not_flagged(tmp_path, capsys):
    _write_manifest(tmp_path, "low.json", 2)
    _write_notice(
        tmp_path,
        "N-2026-01-01-low.md",
        "**Status:** GRADUATE\n\ndiscovery_manifests/low.json\n",
    )
    code, out, err = _run(tmp_path, capsys)
    assert code == 0
    assert "N-2026-01-01-low.md" not in out.split("[audit]")[0]
    assert "[audit] 0 flagged / 1 GRADUATE/INCREMENT notices scanned / 1 total notices" in out
    assert err == ""


def test_held_high_k_not_flagged(tmp_path, capsys):
    _write_manifest(tmp_path, "high.json", 5)
    _write_notice(
        tmp_path,
        "N-2026-01-01-held.md",
        "**Status:** `HELD until operator scope call`\n\n"
        "discovery_manifests/high.json\n",
    )
    code, out, err = _run(tmp_path, capsys)
    assert code == 0
    assert "[audit] 0 flagged / 0 GRADUATE/INCREMENT notices scanned / 1 total notices" in out
    assert err == ""


def test_held_table_cell_body_graduate_not_flagged(tmp_path, capsys):
    _write_manifest(tmp_path, "historical.json", 5)
    _write_notice(
        tmp_path,
        "N-2026-01-01-table.md",
        "**Status:** `HELD`\n\n"
        "Later prose mentions GRADUATE as a historical word.\n\n"
        "| prior | `discovery_manifests/historical.json` |\n",
    )
    code, out, err = _run(tmp_path, capsys)
    assert code == 0
    assert "[audit] 0 flagged / 0 GRADUATE/INCREMENT notices scanned / 1 total notices" in out
    assert "historical.json" not in out.split("[audit]")[0]
    assert err == ""


def test_missing_manifest_skip_exit_zero(tmp_path, capsys):
    _write_notice(
        tmp_path,
        "N-2026-01-01-missing.md",
        "**Status:** GRADUATE\n\ndiscovery_manifests/absent.json\n",
    )
    code, out, err = _run(tmp_path, capsys)
    assert code == 0
    assert "[skip] manifest not found: discovery_manifests/absent.json" in err
    assert "[audit] 0 flagged / 1 GRADUATE/INCREMENT notices scanned / 1 total notices" in out


def test_two_distinct_manifests_checked_independently(tmp_path, capsys):
    _write_manifest(tmp_path, "high.json", 5)
    _write_manifest(tmp_path, "low.json", 2)
    _write_notice(
        tmp_path,
        "N-2026-01-01-two.md",
        "**Status:** GRADUATE\n\n"
        "discovery_manifests/high.json and discovery_manifests/low.json\n",
    )
    code, out, err = _run(tmp_path, capsys)
    assert code == 0
    assert err == ""
    body = out.split("[audit]")[0]
    assert "discovery_manifests/high.json" in body
    assert "discovery_manifests/low.json" not in body
    assert "[audit] 1 flagged / 1 GRADUATE/INCREMENT notices scanned / 1 total notices" in out


def test_increment_high_k_flagged(tmp_path, capsys):
    """Added 2026-08-30 (Codex review, PR #223): a Status line reading
    INCREMENT rather than GRADUATE routes into a Q-brief the same way and
    must not be silently skipped just because it uses the other word."""
    _write_manifest(tmp_path, "high.json", 5)
    _write_notice(
        tmp_path,
        "N-2026-01-01-increment.md",
        "**Status:** `OPEN` — **INCREMENT** (both strata decisive)\n\n"
        "discovery_manifests/high.json\n",
    )
    code, out, err = _run(tmp_path, capsys)
    assert code == 0
    assert "N-2026-01-01-increment.md" in out
    assert "K=5" in out
    assert "[audit] 1 flagged / 1 GRADUATE/INCREMENT notices scanned / 1 total notices" in out
    assert err == ""


def test_two_graduate_notices_same_manifest_two_rows(tmp_path, capsys):
    _write_manifest(tmp_path, "shared.json", 5)
    _write_notice(
        tmp_path,
        "N-2026-01-01-a.md",
        "**Status:** GRADUATE\n\ndiscovery_manifests/shared.json\n",
    )
    _write_notice(
        tmp_path,
        "N-2026-01-01-b.md",
        "**Status:** GRADUATE\n\ndiscovery_manifests/shared.json\n",
    )
    code, out, err = _run(tmp_path, capsys)
    assert code == 0
    assert err == ""
    rows = [ln for ln in out.splitlines() if ln.startswith("N-")]
    assert len(rows) == 2
    assert rows[0].startswith("N-2026-01-01-a.md")
    assert rows[1].startswith("N-2026-01-01-b.md")
    assert all("discovery_manifests/shared.json" in ln for ln in rows)
    assert "[audit] 2 flagged / 2 GRADUATE/INCREMENT notices scanned / 2 total notices" in out
