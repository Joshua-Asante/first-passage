"""Predicate for automatic Codex judgment-review requests."""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "check_codex_judgment_review.py"

_SPEC = importlib.util.spec_from_file_location("check_codex_judgment_review", SCRIPT)
mod = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
sys.modules[_SPEC.name] = mod
_SPEC.loader.exec_module(mod)


def _decide(**kwargs):
    defaults = dict(
        head_branch="cursor/example-6bd4",
        draft=False,
        labels=set(),
        body="",
        changed_files=["tests/test_example.py"],
        existing_comments="",
    )
    defaults.update(kwargs)
    return mod.should_request_review(**defaults)


def test_judgment_paths() -> None:
    assert mod.is_judgment_path("docs/adr/2026-07-14-cc-cursor-surface-allocation.md")
    assert mod.is_judgment_path("STATE.md")
    assert mod.is_judgment_path("core/dd_protection.py")
    assert mod.is_judgment_path("core/mc/engine.py")
    assert mod.is_judgment_path("ops/c1_rail/c1_rail_arm.py")
    assert mod.is_judgment_path(".github/workflows/claude.yml")
    assert mod.is_judgment_path("./.claude/skills/handoff-verify/SKILL.md")
    assert mod.is_judgment_path("core/strategies/striker.pine")
    assert not mod.is_judgment_path("tests/test_example.py")
    assert not mod.is_judgment_path("lab/analysis/c1/foo/RESULTS.md")
    assert not mod.is_judgment_path("scripts/check_boundaries.py")


def test_draft_never_triggers() -> None:
    decision = _decide(
        draft=True,
        labels={mod.LABEL},
        changed_files=["docs/adr/x.md"],
    )
    assert decision == mod.Decision(False, "draft")


def test_marker_is_idempotent() -> None:
    decision = _decide(
        labels={mod.LABEL},
        changed_files=["docs/adr/x.md"],
        existing_comments=f"already ran\n{mod.MARKER}\n",
    )
    assert decision == mod.Decision(False, "already_requested")


def test_label_is_explicit_opt_in() -> None:
    decision = _decide(
        head_branch="feat/human",
        labels={mod.LABEL},
        changed_files=["tests/test_example.py"],
    )
    assert decision == mod.Decision(True, "label")


def test_body_token_is_explicit_opt_in() -> None:
    decision = _decide(
        head_branch="feat/human",
        body="Please look.\nCodex-Review: Judgment\n",
        changed_files=["tests/test_example.py"],
    )
    assert decision == mod.Decision(True, "body_token")


def test_cursor_plus_judgment_surface() -> None:
    decision = _decide(changed_files=["docs/adr/x.md", "tests/test_x.py"])
    assert decision == mod.Decision(True, "cursor_judgment_surface")


def test_cursor_chore_does_not_fire() -> None:
    decision = _decide(changed_files=["tests/test_example.py", "lab/analysis/c1/foo.py"])
    assert decision == mod.Decision(False, "no_match")


def test_human_branch_on_adr_does_not_auto_fire() -> None:
    decision = _decide(
        head_branch="claude/author-an-adr",
        changed_files=["docs/adr/x.md"],
    )
    assert decision == mod.Decision(False, "no_match")


def test_labeled_other_is_ignored() -> None:
    decision = _decide(
        changed_files=["docs/adr/x.md"],
        event_action="labeled",
        event_label="bug",
    )
    assert decision == mod.Decision(False, "labeled_other")


def test_cli_writes_trigger_and_reason(tmp_path: Path) -> None:
    files = tmp_path / "files.txt"
    files.write_text("docs/adr/x.md\n", encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--head-branch",
            "cursor/example-6bd4",
            "--draft",
            "false",
            "--changed-files-file",
            str(files),
        ],
        cwd=REPO,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "TRIGGER=yes" in result.stdout
    assert "REASON=cursor_judgment_surface" in result.stdout
