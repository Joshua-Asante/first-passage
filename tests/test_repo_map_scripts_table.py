"""REPO_MAP.md §2.1 table is generated from repo_map_layers.yml scripts_layer + gates.yml + git ls-files."""
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
        layers=REPO / "scripts" / "repo_map_layers.yml",
        gates_yml=REPO / "scripts" / "gates.yml",
    )
    assert [r[0] for r in rows] == _git_scripts()
    assert len(rows) >= 59


def test_layer_matches_scripts_layer_fallback():
    inv = _load()
    layer = inv._load_scripts_layer(REPO / "scripts" / "repo_map_layers.yml")
    rows = inv.collect(
        repo=REPO,
        layers=REPO / "scripts" / "repo_map_layers.yml",
        gates_yml=REPO / "scripts" / "gates.yml",
    )
    for rel, got, _gate, notes in rows:
        stem = Path(rel).stem
        expected = layer.get(stem, "governance" + inv.FALLBACK_MARK)
        assert got == expected, rel
        assert "layer fallback" not in notes, rel


def test_defaults_live_in_legend_not_notes():
    """No-gate and layer-fallback defaults appear once, in the legend above the table."""
    inv = _load()
    rows = inv.collect(
        repo=REPO,
        layers=REPO / "scripts" / "repo_map_layers.yml",
        gates_yml=REPO / "scripts" / "gates.yml",
    )
    block = inv.render_generated_block(rows)
    assert inv.LEGEND in block
    assert block.index(inv.LEGEND) < block.index("| Script |")
    # Some Gate-— scripts run as harness hooks or in CI, so nothing may call them manual/local.
    assert "manual/local" not in block
    table = inv.render_table(rows)
    assert "layer fallback" not in table
    assert any(r[1] == "governance" + inv.FALLBACK_MARK for r in rows)


def test_wired_gate_ids_exist_in_gates_yml():
    inv = _load()
    gm = inv._load_gate_manifest()
    data = gm.load_manifest(REPO / "scripts" / "gates.yml")
    known = {g["id"] for g in data["gates"]}
    rows = inv.collect(
        repo=REPO,
        layers=REPO / "scripts" / "repo_map_layers.yml",
        gates_yml=REPO / "scripts" / "gates.yml",
    )
    for rel, _layer, gate_cell, notes in rows:
        if gate_cell == inv.NO_GATE:
            assert notes == "—" or rel.endswith("gate_manifest.py"), rel
            continue
        for part in gate_cell.split("; "):
            gid = part.split(" (", 1)[0].strip("`")
            assert gid in known, f"{rel} cites unknown gate id {gid}"


def test_script_from_cmd_ignores_glob_tokens():
    """A unittest pattern (test_*.py) is a token, never a script path."""
    inv = _load()
    module_run = [
        "python", "-m", "unittest", "discover",
        "-s", "tests/evidence_store", "-p", "test_*.py",
    ]
    assert inv._script_from_cmd(module_run) is None
    assert inv._script_from_cmd(["python", "run_[0-9].py"]) is None
    assert inv._script_from_cmd(["python", "scripts/a.py", "test_?.py"]) == "scripts/a.py"


def test_module_run_gate_attributed_via_staged_regex():
    """A gate whose cmd names no script is credited only through its staged_regex."""
    inv = _load()
    gates = [
        # module run: no script token in cmd
        {
            "id": "evidence-store",
            "tier": "path-conditional",
            "when": {"staged_regex": r"^(scripts/evidence_store/|tests/evidence_store/)"},
            "cmd": ["python", "-m", "unittest", "discover", "-s", "tests/evidence_store",
                    "-p", "test_*.py"],
        },
        # names a script: staged_regex must NOT spread it to matching scripts
        {
            "id": "boundaries",
            "tier": "path-conditional",
            "when": {"staged_regex": r"^scripts/"},
            "cmd": ["python", "scripts/check_boundaries.py"],
        },
        # module run without when.staged_regex: stays unattributed
        {
            "id": "bare-module-run",
            "tier": "always",
            "cmd": ["python", "-m", "pytest", "-q"],
        },
    ]
    scripts = [
        "scripts/evidence_store/store.py",
        "scripts/check_boundaries.py",
        "scripts/pine_lint.py",
    ]
    by = inv.gates_by_script(gates, scripts)
    assert [g["id"] for g in by["scripts/evidence_store/store.py"]] == ["evidence-store"]
    assert [g["id"] for g in by["scripts/check_boundaries.py"]] == ["boundaries"]
    assert "scripts/pine_lint.py" not in by
    assert all(g["id"] != "bare-module-run" for wired in by.values() for g in wired)


def test_evidence_store_rows_carry_the_evidence_store_gate():
    inv = _load()
    rows = inv.collect(
        repo=REPO,
        layers=REPO / "scripts" / "repo_map_layers.yml",
        gates_yml=REPO / "scripts" / "gates.yml",
    )
    evidence = [r for r in rows if r[0].startswith("scripts/evidence_store/")]
    assert evidence, "no tracked scripts/evidence_store/*.py rows found"
    for rel, _layer, gate_cell, _notes in evidence:
        assert "evidence-store" in gate_cell, rel


def test_exit_zero_and_stats_notes():
    inv = _load()
    by_rel = {
        r[0]: r
        for r in inv.collect(
            repo=REPO,
            layers=REPO / "scripts" / "repo_map_layers.yml",
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
