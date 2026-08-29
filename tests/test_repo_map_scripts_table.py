"""REPO_MAP.md §2.1 table is generated from SCRIPTS_LAYER + gates.yml + git ls-files."""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "check_repo_map_scripts_table.py"


def _load():
    spec = importlib.util.spec_from_file_location("check_repo_map_scripts_table", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _git_scripts() -> list[str]:
    out = subprocess.check_output(
        ["git", "ls-files", "scripts/*.py"],
        cwd=REPO,
        text=True,
    )
    return sorted(ln.strip() for ln in out.splitlines() if ln.strip())


def test_live_rows_cover_every_tracked_script():
    inv = _load()
    rows = inv.collect(
        repo=REPO,
        boundaries=REPO / "scripts" / "check_boundaries.py",
        gates_yml=REPO / "scripts" / "gates.yml",
    )
    assert [r[0] for r in rows] == _git_scripts()
    assert len(rows) >= 59


def test_layer_matches_scripts_layer_fallback():
    inv = _load()
    layer = inv._load_scripts_layer(REPO / "scripts" / "check_boundaries.py")
    rows = inv.collect(
        repo=REPO,
        boundaries=REPO / "scripts" / "check_boundaries.py",
        gates_yml=REPO / "scripts" / "gates.yml",
    )
    for rel, got, _gate, notes in rows:
        stem = Path(rel).stem
        expected = layer.get(stem, "governance")
        assert got == expected, rel
        if stem in layer:
            assert "layer fallback" not in notes, rel
        else:
            assert "layer fallback (not in SCRIPTS_LAYER)" in notes, rel


def test_wired_gate_ids_exist_in_gates_yml():
    inv = _load()
    gm = inv._load_gate_manifest()
    data = gm.load_manifest(REPO / "scripts" / "gates.yml")
    known = {g["id"] for g in data["gates"]}
    rows = inv.collect(
        repo=REPO,
        boundaries=REPO / "scripts" / "check_boundaries.py",
        gates_yml=REPO / "scripts" / "gates.yml",
    )
    for rel, _layer, gate_cell, notes in rows:
        if gate_cell == "—":
            assert (
                "manual/local only, not in gates.yml" in notes
                or rel.endswith("gate_manifest.py")
            ), rel
            continue
        for part in gate_cell.split("; "):
            gid = part.split(" (", 1)[0].strip("`")
            assert gid in known, f"{rel} cites unknown gate id {gid}"


def test_exit_zero_and_stats_notes():
    inv = _load()
    by_rel = {
        r[0]: r
        for r in inv.collect(
            repo=REPO,
            boundaries=REPO / "scripts" / "check_boundaries.py",
            gates_yml=REPO / "scripts" / "gates.yml",
        )
    }
    assert "WARN, --exit-zero" in by_rel["scripts/check_instrument_rejection_coverage.py"][3]
    assert "--stats (report-only)" in by_rel["scripts/check_falsifier_reachability.py"][3]
    assert "--check-tree-skew (report-only)" in by_rel[
        "scripts/validate_c1_monitoring_acceptance.py"
    ][3]
    assert by_rel["scripts/pine_lint.py"][1] == "lab"
    assert by_rel["scripts/lock_event_hook.py"][1] == "ops"
    assert by_rel["scripts/lock_event_hook.py"][2] == "—"


def test_write_then_check_passes(tmp_path):
    inv = _load()
    dest = tmp_path / "REPO_MAP.md"
    dest.write_text(
        REPO.joinpath("REPO_MAP.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    assert (
        inv.main(
            [
                "--write",
                "--root",
                str(REPO),
                "--repo-map",
                str(dest),
            ]
        )
        == 0
    )
    assert (
        inv.main(
            [
                "--check",
                "--root",
                str(REPO),
                "--repo-map",
                str(dest),
            ]
        )
        == 0
    )


def test_check_stale_table_fails(tmp_path):
    inv = _load()
    dest = tmp_path / "REPO_MAP.md"
    dest.write_text(
        REPO.joinpath("REPO_MAP.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    assert inv.main(["--write", "--root", str(REPO), "--repo-map", str(dest)]) == 0
    text = dest.read_text(encoding="utf-8")
    dest.write_text(
        text.replace("| `scripts/pine_lint.py` | lab |", "| `scripts/pine_lint.py` | ops |"),
        encoding="utf-8",
    )
    assert inv.main(["--check", "--root", str(REPO), "--repo-map", str(dest)]) == 1
