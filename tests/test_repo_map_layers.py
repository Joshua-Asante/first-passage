"""scripts/repo_map_layers.yml is the single layer-map definition (ADR 2026-06-05 §2.3, 2026-09-17).

The scanner loads it at import; check_repo_map_layers.py gates its schema. Pinned
here: the live file passes; the scanner's maps are exactly the file's contents;
and each schema / repository rule rejects the mutation it exists for.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
GATE = REPO / "scripts" / "check_repo_map_layers.py"
SCANNER = REPO / "scripts" / "check_boundaries.py"
LAYERS_YML = REPO / "scripts" / "repo_map_layers.yml"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def gate():
    return _load(GATE, "check_repo_map_layers")


@pytest.fixture(scope="module")
def scanner():
    return _load(SCANNER, "check_boundaries")


def _mutated(tmp_path: Path, old: str, new: str) -> Path:
    text = LAYERS_YML.read_text(encoding="utf-8")
    assert old in text, f"fixture assumption: {old!r} is in the live file"
    out = tmp_path / "repo_map_layers.yml"
    out.write_text(text.replace(old, new, 1), encoding="utf-8")
    return out


def test_live_file_passes(gate):
    assert gate.main([]) == 0


def test_scanner_maps_are_the_file_contents(scanner):
    data = scanner.load_layer_maps(LAYERS_YML)
    assert scanner.LAYER_MAPS_PATH == LAYERS_YML
    assert scanner.APP_LAYER_PREFIX == data["app_layer_prefix"]
    assert scanner.GOVERNANCE_PREFIXES == tuple(data["governance_prefixes"])
    assert scanner.SCRIPTS_LAYER == data["scripts_layer"]
    assert scanner.FLAT_IMPORT_ROOTS == tuple(data["flat_import_roots"])
    # The contract and the scan scope stay in the scanner; they are not layer maps.
    assert ("lab", "ops") not in scanner.LEGAL_EDGES
    assert "tests/" in scanner.EXEMPT_PREFIXES


@pytest.mark.parametrize("old,new,reason", [
    ("core/: core", "core/: lab", "an app prefix must name its own directory"),
    ("pine_lint: lab", "pine_lint: research", "unknown layer"),
    ("  - ops/c1_rail\n", "  - ops/c1_rail/\n", "flat root with trailing slash"),
    ("  - docs/\n", "  - docs\n", "governance prefix without trailing slash"),
    ("flat_import_roots:", "flat_roots:", "unknown section, required one missing"),
    ("  - scripts\n", "  - scripts\n  - scripts\n", "duplicate flat root"),
    ("  pine_lint: lab\n", "  pine_lint: lab\n  ghost_script: lab\n", "override for an untracked script"),
    ("  - ops/c1_signal_daemon\n", "  - ops/no_such_dir\n", "flat root that is not a directory"),
    ("  - scripts\n", "  - 010\n", "non-string scalar"),
    ("scripts_layer:\n", "scripts_layer: {}\n", "empty section"),
])
def test_schema_or_repository_violation_fails(gate, tmp_path, old, new, reason):
    bad = _mutated(tmp_path, old, new)
    assert gate.main(["--yml", str(bad), "--repo-root", str(REPO)]) == 1, reason


def test_unchanged_copy_passes_from_another_directory(gate, tmp_path):
    copy = _mutated(tmp_path, "core/: core", "core/: core")
    assert gate.main(["--yml", str(copy), "--repo-root", str(REPO)]) == 0


def test_unreadable_or_non_mapping_file_fails(gate, tmp_path):
    assert gate.main(["--yml", str(tmp_path / "absent.yml")]) == 1
    scalar = tmp_path / "scalar.yml"
    scalar.write_text("- just\n- a list\n", encoding="utf-8")
    assert gate.main(["--yml", str(scalar)]) == 1
