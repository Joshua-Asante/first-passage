#!/usr/bin/env python3
"""Thin launcher — canonical module: lab/discovery/register_search.py.

Stdlib-only: must not import lab packages (governance→lab is illegal).
Requires a monorepo checkout. Prefer::

    PYTHONPATH=lab python -m discovery.register_search …
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[4]
_LAB = _REPO / "lab"
if not (_LAB / "discovery" / "register_search.py").is_file():
    sys.exit(
        "ABORT: lab/discovery/register_search.py not found under "
        f"{_REPO}. Skill launchers only work from a monorepo checkout. "
        "Use: PYTHONPATH=lab python -m discovery.register_search …"
    )
_ENV = os.environ.copy()
_ENV["PYTHONPATH"] = str(_LAB) + (
    os.pathsep + _ENV["PYTHONPATH"] if _ENV.get("PYTHONPATH") else ""
)
raise SystemExit(
    subprocess.call(
        [sys.executable, "-m", "discovery.register_search", *sys.argv[1:]],
        env=_ENV,
    )
)
