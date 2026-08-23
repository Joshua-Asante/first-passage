"""P5 — REPO_MAP machine block must match check_boundaries.py layer maps."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "check_repo_map_layers.py"


def _load():
    spec = importlib.util.spec_from_file_location("check_repo_map_layers", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_live_maps_match():
    inv = _load()
    assert inv.main([]) == 0


def test_mutated_prefix_fails(tmp_path):
    inv = _load()
    boundaries = (REPO / "scripts" / "check_boundaries.py").read_text(encoding="utf-8")
    yml = (REPO / "scripts" / "repo_map_layers.yml").read_text(encoding="utf-8")
    bad_yml = yml.replace("core/: core", "core/: lab")
    b_path = tmp_path / "check_boundaries.py"
    y_path = tmp_path / "repo_map_layers.yml"
    b_path.write_text(boundaries, encoding="utf-8")
    y_path.write_text(bad_yml, encoding="utf-8")
    assert inv.main(["--boundaries", str(b_path), "--yml", str(y_path)]) == 1


def test_matching_copies_pass(tmp_path):
    inv = _load()
    boundaries = (REPO / "scripts" / "check_boundaries.py").read_text(encoding="utf-8")
    yml = (REPO / "scripts" / "repo_map_layers.yml").read_text(encoding="utf-8")
    b_path = tmp_path / "check_boundaries.py"
    y_path = tmp_path / "repo_map_layers.yml"
    b_path.write_text(boundaries, encoding="utf-8")
    y_path.write_text(yml, encoding="utf-8")
    assert inv.main(["--boundaries", str(b_path), "--yml", str(y_path)]) == 0
