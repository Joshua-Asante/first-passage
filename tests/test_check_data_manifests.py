"""Unit test for scripts/check_data_manifests.py — pins the manifest-dir set.

Added 2026-07-01 alongside the CME-micro futures pivot: the cme/ raw-export
tree must be one of the dirs the vendor-data gate validates.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
_CDM_PATH = REPO_ROOT / "scripts" / "check_data_manifests.py"
_spec = importlib.util.spec_from_file_location("check_data_manifests", _CDM_PATH)
cdm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cdm)


def test_cme_dir_is_a_manifest_dir():
    names = {p.name for p in cdm.MANIFEST_DIRS}
    assert "cme" in names
    # and it lives under tv_exports
    assert any(p.as_posix().endswith("tv_exports/cme") for p in cdm.MANIFEST_DIRS)


# Pepperstone (panel + bar_export) left the contract 2026-08-03 under the futures
# pivot — docs/ltm/notes/2026-08-03-pepperstone-data-tombstone.md.
EXPECTED_MANIFEST_DIRS = (
    "core/data/tv_exports/cme",
    "core/data/bar_data",
    "core/data/external",
)


def test_retired_pepperstone_dirs_are_not_manifest_owners():
    """Regression: a retired vendor dir must not silently re-enter the contract."""
    rel = cdm.manifest_relative_dirs()
    assert not any("pepperstone" in d for d in rel), rel


def test_manifest_relative_dirs_are_machine_readable_and_repo_relative():
    assert cdm.manifest_relative_dirs() == EXPECTED_MANIFEST_DIRS


def test_list_dirs_cli_emits_json_manifest_ownership():
    result = subprocess.run(
        [sys.executable, str(_CDM_PATH), "--list-dirs"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert tuple(json.loads(result.stdout)) == EXPECTED_MANIFEST_DIRS


def test_manifest_ci_consumes_checker_owned_directory_list():
    workflow = (
        REPO_ROOT / ".github" / "workflows" / "manifest-check.yml"
    ).read_text(encoding="utf-8")

    assert "--list-dirs" in workflow
