#!/usr/bin/env python3
"""PostToolUse hook — validate skill edits; never publish.

Reads PostToolUse JSON from stdin. If the edited file is under
.claude/skills/, run check_skill_refs.py --all and
check_skills_no_constants.py, report their actual outcomes, and report
that an explicit release is pending. This hook never invokes
sync_skills.py publication and never creates backups.

Malformed stdin and unrelated edits stay benign (exit 0). Missing or
failing validators are visible and exit 2 — Cursor's after_file_edit
adapter forwards that stderr. A missing validator is never reported as
passed.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def is_under_worktrees(path: Path) -> bool:
    """True if *path* sits inside a `.claude/worktrees/` tree (worktree session)."""
    parts = [s.lower() for s in Path(path).parts]
    return any(
        parts[i] == ".claude" and parts[i + 1] == "worktrees"
        for i in range(len(parts) - 1)
    )


def _script_dir() -> Path:
    return Path(__file__).resolve().parent


def _iter_paths(tool_input: dict):
    yield str(tool_input.get("file_path", ""))
    for edit in tool_input.get("edits", []) or []:
        yield str(edit.get("file_path", ""))


def _run_validator(script: Path, argv: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(script), *argv],
        cwd=str(cwd),
        check=False,
        capture_output=True,
        text=True,
    )


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    tool_input = data.get("tool_input", {}) or {}
    paths = [p.replace("\\", "/") for p in _iter_paths(tool_input) if p]
    if not any("/.claude/skills/" in p or p.startswith(".claude/skills/") for p in paths):
        return 0

    script_dir = _script_dir()
    repo_root = script_dir.parent
    validators = [
        (script_dir / "check_skill_refs.py", ["--all"]),
        (script_dir / "check_skills_no_constants.py", []),
    ]
    missing = [path.name for path, _argv in validators if not path.exists()]
    if missing:
        print(
            "SKILL CHECK BLOCKED: missing validator(s) "
            + ", ".join(missing)
            + " — cannot validate. explicit release is pending; "
            "this hook does not publish.",
            file=sys.stderr,
        )
        return 2

    failed = False
    for script, argv in validators:
        result = _run_validator(script, argv, repo_root)
        label = " ".join([script.name, *argv]).strip()
        if result.returncode != 0:
            failed = True
            print(
                f"SKILL CHECK FAILED: {label} failed — repo edit kept; "
                "explicit release is pending; this hook does not publish.",
                file=sys.stderr,
            )
            sys.stderr.write(result.stdout or "")
            sys.stderr.write(result.stderr or "")
        else:
            print(f"SKILL CHECK: {label}: ok", file=sys.stderr)

    print(
        "explicit release is pending; this hook does not publish.",
        file=sys.stderr,
    )
    return 2 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
