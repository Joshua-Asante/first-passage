#!/usr/bin/env python3
"""Thin launcher — canonical module: lab/research_utils/selection_tests.py.

Stdlib-only: must not import lab packages (governance→lab is illegal).
Requires a monorepo checkout. Prefer::

    PYTHONPATH=lab python -m research_utils.selection_tests …
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[4]
_LAB = _REPO / "lab"
if not (_LAB / "research_utils" / "selection_tests.py").is_file():
    sys.exit(
        "ABORT: lab/research_utils/selection_tests.py not found under "
        f"{_REPO}. Skill launchers only work from a monorepo checkout. "
        "Use: PYTHONPATH=lab python -m research_utils.selection_tests …"
    )
_ENV = os.environ.copy()
_ENV["PYTHONPATH"] = str(_LAB) + (
    os.pathsep + _ENV["PYTHONPATH"] if _ENV.get("PYTHONPATH") else ""
)
raise SystemExit(
    subprocess.call(
        [sys.executable, "-m", "research_utils.selection_tests", *sys.argv[1:]],
        env=_ENV,
    )
)
