#!/usr/bin/env python3
"""Cursor afterFileEdit adapter → Claude PostToolUse lock/sync hooks.

Remaps Cursor's afterFileEdit JSON ({file_path, edits}) into the
tool_input shape expected by scripts/lock_event_hook.py and
scripts/sync_skills_hook.py, then runs both. Fail-open: never blocks
edits (always exit 0). Sync/gate stderr is forwarded so the agent can
see deploy blocks.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def _repo_root() -> Path:
    # .cursor/hooks/after_file_edit.py → repo root is parents[2]
    return Path(__file__).resolve().parents[2]


def _to_claude_payload(data: dict) -> dict:
    file_path = str(data.get("file_path", "") or "")
    edits = data.get("edits") or []
    tool_input: dict = {"file_path": file_path, "edits": edits}
    if edits and isinstance(edits, list) and isinstance(edits[0], dict):
        # Prefer first edit strings for lock_event_hook's old/new scan.
        tool_input.setdefault("old_string", edits[0].get("old_string", ""))
        tool_input.setdefault("new_string", edits[0].get("new_string", ""))
    return {"tool_input": tool_input}


def _run_hook(script: Path, payload: dict, cwd: Path) -> None:
    if not script.exists():
        sys.stderr.write(
            f"after_file_edit: MISSING HOOK {script} "
            f"— Cursor-side lock/sync guard did NOT run\n"
        )
        return
    proc = subprocess.run(
        [sys.executable, str(script)],
        input=json.dumps(payload).encode("utf-8"),
        cwd=str(cwd),
        check=False,
        capture_output=True,
    )
    if proc.stderr:
        sys.stderr.buffer.write(proc.stderr)
    # Claude sync_skills_hook exits 2 on gate/deploy failure; surface text
    # but do not fail-closed the Cursor edit.
    if proc.returncode not in (0, None) and proc.stdout:
        sys.stderr.buffer.write(proc.stdout)


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    payload = _to_claude_payload(data if isinstance(data, dict) else {})
    root = _repo_root()
    scripts = root / "scripts"
    _run_hook(scripts / "lock_event_hook.py", payload, root)
    _run_hook(scripts / "sync_skills_hook.py", payload, root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
