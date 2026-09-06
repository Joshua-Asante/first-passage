"""lab/ARCHIVED.json support in archive_lab_analysis (2026-09-06 reduction ADR).

Archived-elsewhere studies keep a CATALOG row whose body cell is the archive
URL; the index never resolves paths against disk and a slug never renders
twice.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_PATH = _REPO / "scripts" / "archive_lab_analysis.py"
_spec = importlib.util.spec_from_file_location("archive_lab_analysis_archived_index_ut", _PATH)
ala = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = ala
_spec.loader.exec_module(ala)


def _hot(root: Path, theme: str, slug: str, status: str = "ACTIVE") -> str:
    d = root / "lab" / "analysis" / theme / slug
    d.mkdir(parents=True)
    (d / "RESULTS.md").write_text(
        f"**Theme:** {theme}\n**Status:** {status} — live body\n", encoding="utf-8"
    )
    (root / "lab" / "analysis" / theme / "README.md").write_text(f"# {theme}\n", encoding="utf-8")
    return f"lab/analysis/{theme}/{slug}/RESULTS.md"


def _index(root: Path, studies: dict) -> None:
    (root / "lab").mkdir(parents=True, exist_ok=True)
    (root / "lab" / "ARCHIVED.json").write_text(
        json.dumps(
            {
                "schema": 1,
                "archive_repo": "https://example.invalid/archive",
                "archive_commit": "deadbeef",
                "studies": studies,
            }
        ),
        encoding="utf-8",
    )


def test_no_index_leaves_scan_unchanged(tmp_path: Path) -> None:
    p = _hot(tmp_path, "c1", "live")
    rows = ala.scan_lab(tmp_path, tracked_override={"live": frozenset({p})})
    assert [r.slug for r in rows] == ["live"]
    assert ala.load_archived_index(tmp_path) == {}


def test_indexed_study_with_no_dir_gets_archived_row(tmp_path: Path) -> None:
    p = _hot(tmp_path, "c1", "live")
    _index(
        tmp_path,
        {
            "gone": {
                "theme": "c1",
                "status": "FALSIFIED",
                "one_liner": "no edge",
                "closed": "2026-08-01",
                "baseline_body": "lab/analysis/c1/gone/",
                "retained_files": [],
            }
        },
    )
    rows = {r.slug: r for r in ala.scan_lab(tmp_path, tracked_override={"live": frozenset({p})})}
    assert set(rows) == {"live", "gone"}
    gone = rows["gone"]
    assert gone.hot == "no"
    assert gone.status == "FALSIFIED"
    assert gone.one_liner == "no edge"
    assert gone.body == "https://example.invalid/archive/tree/deadbeef/lab/analysis/c1/gone/"
    assert gone.card == "—"

    text = ala.render_catalog(list(rows.values()))
    hot, archived = text.split("## Archived", 1)
    assert "gone" not in hot.split("## Hot bodies", 1)[1]
    assert "| gone | FALSIFIED | no edge |" in archived
    assert "example.invalid/archive/tree/deadbeef/lab/analysis/c1/gone/" in archived


def test_indexed_row_replaces_partial_remnant_without_duplicating_slug(tmp_path: Path) -> None:
    fixture = _hot(tmp_path, "c1", "partial", status="CLOSED")
    _index(
        tmp_path,
        {
            "partial": {
                "theme": "c1",
                "status": "CLOSED",
                "one_liner": "kept one fixture",
                "closed": "2026-07-30",
                "baseline_body": "lab/analysis/c1/partial/",
                "retained_files": [fixture],
            }
        },
    )
    rows = ala.scan_lab(tmp_path, tracked_override={"partial": frozenset({fixture})})
    assert [r.slug for r in rows].count("partial") == 1
    (row,) = [r for r in rows if r.slug == "partial"]
    assert row.hot == "no"
    assert row.card == "lab/analysis/c1/partial/ (1 file(s) retained)"
    assert row.body.startswith("https://example.invalid/archive/tree/deadbeef/")


def test_malformed_index_is_ignored(tmp_path: Path) -> None:
    p = _hot(tmp_path, "c1", "live")
    (tmp_path / "lab" / "ARCHIVED.json").write_text("{not json", encoding="utf-8")
    assert ala.load_archived_index(tmp_path) == {}
    (tmp_path / "lab" / "ARCHIVED.json").write_text(json.dumps({"studies": []}), encoding="utf-8")
    assert ala.load_archived_index(tmp_path) == {}
    rows = ala.scan_lab(tmp_path, tracked_override={"live": frozenset({p})})
    assert [r.slug for r in rows] == ["live"]


def test_full_check_treats_an_indexed_remnant_as_a_remnant_not_a_hot_body(
    tmp_path: Path,
) -> None:
    """An indexed study's leftover files are fixtures, not a body to validate.

    ``scan_lab`` renders indexed slugs under ``## Archived`` from the index, but
    ``check_lab`` walks ``iter_hot_bodies`` independently. Without the index skip
    it re-judged those remnants as hot bodies and emitted ``empty one-liner:``
    against studies the catalog already showed as archived elsewhere -- the
    checker contradicting the catalog it exists to validate.
    """
    remnant = tmp_path / "lab" / "analysis" / "c1" / "remnant"
    remnant.mkdir(parents=True)
    # No parsable disposition -> the scan cannot derive a one-liner, which is
    # exactly the shape of the real remnants (STAGE0.md-style cards).
    (remnant / "RESULTS.md").write_text(
        "# Remnant\n\n**Theme:** c1\n\nFixture body.\n", encoding="utf-8"
    )
    (tmp_path / "lab" / "analysis" / "c1" / "README.md").write_text("# c1\n", encoding="utf-8")
    tracked = {"remnant": frozenset({"lab/analysis/c1/remnant/RESULTS.md"})}

    # Not indexed -> judged as a hot body, so the fixture is non-vacuous.
    before = ala.check_lab(tmp_path, tracked_override=tracked)
    assert "empty one-liner: remnant" in before

    _index(
        tmp_path,
        {
            "remnant": {
                "theme": "c1",
                "status": "CLOSED",
                "one_liner": "archived elsewhere",
                "baseline_body": "lab/analysis/c1/remnant/",
                "retained_files": ["lab/analysis/c1/remnant/RESULTS.md"],
            }
        },
    )
    after = ala.check_lab(tmp_path, tracked_override=tracked)
    assert "empty one-liner: remnant" not in after
    assert not any("remnant" in issue for issue in after), after
