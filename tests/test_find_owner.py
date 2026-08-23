"""Thin Rule 7 lookup — scripts/find_owner.py. Not a second owner table."""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "find_owner.py"
_SPEC = importlib.util.spec_from_file_location("find_owner", SCRIPT)
fo = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = fo
_SPEC.loader.exec_module(fo)


def _run(query: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), query],
        cwd=REPO,
        text=True,
        capture_output=True,
    )


def test_dd_protection_resolves_to_rule7():
    proc = _run("dd_protection")
    assert proc.returncode == 0, proc.stderr
    assert "core/dd_protection.py" in proc.stdout
    assert "operational_rules.md" in proc.stdout


def test_sessions_md_resolves():
    proc = _run("SESSIONS.md")
    assert proc.returncode == 0, proc.stderr
    assert "SESSIONS.md" in proc.stdout


def test_lab_catalog_resolves():
    proc = _run("lab/CATALOG.md")
    assert proc.returncode == 0, proc.stderr
    assert "CATALOG.md" in proc.stdout


def test_unknown_token_exits_nonzero():
    proc = _run("this-token-has-no-owner-zzzz")
    assert proc.returncode != 0
    assert "no owner" in proc.stdout
