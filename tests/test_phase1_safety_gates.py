"""Regression tests for Phase-1 repository safety gates."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    ("script", "module"),
    (
        ("scripts/mc_user_guardian.py", "scripts.mc_user_guardian"),
    ),
)
def test_direct_script_supports_absolute_path_and_module_import(
    script: str, module: str, tmp_path: Path
) -> None:
    absolute_result = subprocess.run(
        [sys.executable, "-E", str(REPO_ROOT / script), "--help"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    import_result = subprocess.run(
        [sys.executable, "-E", "-c", f"import {module}"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )

    assert absolute_result.returncode == 0, absolute_result.stderr
    assert "usage:" in absolute_result.stdout.lower()
    assert import_result.returncode == 0, import_result.stderr
