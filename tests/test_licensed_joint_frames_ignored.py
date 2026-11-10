"""The two vendor-derived joint frames stay out of git (data-rule fix D2, 2026-11-10).

Their producers (candidate24_joint_gate.py, c24_joint_gate.py) rewrite them in place when
vendor bars are present. The per-folder .gitignore keeps a rewrite from being committed.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FRAMES = (
    "lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate24_joint_frame.csv",
    "lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c24_joint_frame.csv",
)


@pytest.mark.parametrize("rel", FRAMES)
def test_frame_is_ignored_and_untracked(rel):
    git = shutil.which("git")
    if git is None:
        pytest.skip("git not available")
    ignored = subprocess.run(
        [git, "check-ignore", "--no-index", "-q", rel], cwd=ROOT, check=False
    )
    assert ignored.returncode == 0, f"{rel} is not git-ignored"
    tracked = subprocess.run(
        [git, "ls-files", "--error-unmatch", rel], cwd=ROOT, check=False, capture_output=True
    )
    assert tracked.returncode != 0, f"{rel} is tracked"
