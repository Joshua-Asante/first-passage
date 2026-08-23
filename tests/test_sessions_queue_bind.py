"""Newest SESSIONS Open/next must cite every live STATE queue row number."""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "check_sessions_queue_bind.py"

_SPEC = importlib.util.spec_from_file_location("check_sessions_queue_bind", SCRIPT)
mod = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
_SPEC.loader.exec_module(mod)


def _write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def _state(rows: str) -> str:
    return (
        "# STATE\n\n"
        "## OPERATOR QUEUE — strictly ordered, ≤5 live items\n\n"
        "| # | Item | Owner artifact | Blocks |\n"
        "|---|---|---|---|\n"
        f"{rows}\n\n"
        "---\n\n"
        "## Executed operator decisions — decision index\n\n"
        "- **2026-08-23** — unrelated.\n"
    )


def _sessions(open_next: str) -> str:
    return (
        "# Session Log\n\n---\n\n"
        "## 2026-08-24z — newest\n\n"
        "**Focus:** x.\n\n"
        f"**Open / next:** {open_next}\n\n"
        "**Live-ops state:** unchanged.\n\n"
        "---\n\n"
        "## 2026-08-24y — older\n\n"
        "**Open / next:** leftovers only, no row numbers.\n"
    )


def test_missing_row_exits_one(tmp_path: Path) -> None:
    state = _write(
        tmp_path / "STATE.md",
        _state("| 1 | F1 | a | b |\n| 2 | B7 | a | b |\n| 3 | Blind | a | b |\n"),
    )
    sessions = _write(
        tmp_path / "SESSIONS.md",
        _sessions("**STATE queue:** #1 F1 · #2 B7-REFIRE + M1."),
    )
    rc = subprocess.call(
        [sys.executable, str(SCRIPT), "--state", str(state), "--file", str(sessions)],
        cwd=REPO,
    )
    assert rc == 1


def test_all_rows_cited_exits_zero(tmp_path: Path) -> None:
    state = _write(
        tmp_path / "STATE.md",
        _state("| 1 | F1 | a | b |\n| 2 | B7 | a | b |\n| 3 | Blind | a | b |\n"),
    )
    sessions = _write(
        tmp_path / "SESSIONS.md",
        _sessions("**STATE queue:** #1 F1 · #2 B7-REFIRE + M1 · #3 Blind last slot."),
    )
    rc = subprocess.call(
        [sys.executable, str(SCRIPT), "--state", str(state), "--file", str(sessions)],
        cwd=REPO,
    )
    assert rc == 0


def test_parser_does_not_read_lab_or_adr() -> None:
    src = SCRIPT.read_text(encoding="utf-8")
    assert "lab/" not in src
    assert "docs/adr" not in src
    assert "docs/SESSIONS.md" in src
    assert "STATE.md" in src


def test_live_ids_scoped_to_operator_queue() -> None:
    text = _state("| 1 | F1 | a | b |\n| 2 | B7 | a | b |\n")
    text += "\n## Forward board\n\n| 9 | decoy |\n"
    assert mod.live_queue_ids(text) == [1, 2]


def test_newest_open_next_ignores_older_entry() -> None:
    body = _sessions("**STATE queue:** #1 · #2 · #3")
    assert "#3" in mod.newest_open_next(body)
    assert "leftovers only" not in mod.newest_open_next(body)
