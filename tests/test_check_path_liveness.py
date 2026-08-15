"""Unit tests for scripts/check_path_liveness.py — MANIFEST parent-dir liveness."""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_CPL_PATH = REPO_ROOT / "scripts" / "check_path_liveness.py"
_spec = importlib.util.spec_from_file_location("check_path_liveness", _CPL_PATH)
cpl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cpl)

REAL_PINE_MANIFEST = REPO_ROOT / "core" / "strategies" / "MANIFEST.sha256"


def test_real_pine_manifest_all_dirs_resolve():
    assert cpl.check_pine_manifest(REAL_PINE_MANIFEST, REPO_ROOT) == []


def test_bad_pine_manifest_dir_is_flagged(tmp_path):
    bad = tmp_path / "MANIFEST.sha256"
    bad.write_text(
        "0" * 64 + "  core/strategies/PHANTOM/striker_dj30_v4.5.pine\n",
        encoding="utf-8",
    )
    misses = cpl.check_pine_manifest(bad, REPO_ROOT)
    assert any("PHANTOM" in m for m in misses), misses


def test_pine_bytes_absent_dir_present_is_not_a_miss(tmp_path):
    manifest = tmp_path / "MANIFEST.sha256"
    manifest.write_text(
        "0" * 64 + "  core/strategies/guardian/guardian_gold_DOES_NOT_EXIST.pine\n",
        encoding="utf-8",
    )
    assert cpl.check_pine_manifest(manifest, REPO_ROOT) == []


def test_cli_exit_zero_on_real_tree():
    r = subprocess.run([sys.executable, str(_CPL_PATH)],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr


def test_cli_exit_nonzero_on_bad_manifest(tmp_path):
    bad = tmp_path / "MANIFEST.sha256"
    bad.write_text(
        "0" * 64 + "  core/strategies/PHANTOM/striker_dj30_v4.5.pine\n",
        encoding="utf-8",
    )
    r = subprocess.run(
        [sys.executable, str(_CPL_PATH), "--pine-manifest", str(bad)],
        capture_output=True, text=True,
    )
    assert r.returncode == 1, r.stdout + r.stderr
