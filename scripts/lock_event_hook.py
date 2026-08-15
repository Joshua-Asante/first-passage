#!/usr/bin/env python3
"""PostToolUse hook — fire verify_lock_anchors.py only on lock-event edits.

Per docs/operational_rules.md Rule 6: per-edit hooks on dd_protection.py /
firm_rules.py are too aggressive (routine code-only edits without locks fire
false positives). Filter to: a numeric on a `# LOCKED` line, or a version
string of form vN.N, or one of the known locked-constant names.

Reads PostToolUse JSON from stdin. Never blocks edits (exits 0 always). On
match, runs verify_lock_anchors.py.

⚠ CORRECTED 2026-08-08: the previous line claimed the verifier "appends to
analysis/skew_audit/". That directory has never existed and verify_lock_anchors.py
has no file sink at all — it reports on stdout only. Combined with the
capture_output=True + unconditional `return 0`, this hook RAN the verifier and
DISCARDED every finding it could produce, on every matching edit.
FIXED 2026-08-08 (see run() below): output is surfaced to stderr and the hook
returns 2 on a non-clean result, mirroring scripts/sync_skills_hook.py. It still
never blocks the edit — PostToolUse exit 2 reaches the agent, which is the right
severity for an advisory skew check.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

LOCKED_FILES = ("firm_rules.py", "dd_protection.py")
LOCKED_PATTERN = re.compile(
    r"#\s*LOCKED|v[0-9]+\.[0-9]+|DD_TRIGGER|DD_SCALE|RISK_TIERS|BASE_RISK|BASELINE_RISK"
)


def _stringify(value) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(_stringify(x) for x in value)
    if isinstance(value, dict):
        return "\n".join(_stringify(v) for v in value.values())
    return ""


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    tool_input = data.get("tool_input", {}) or {}
    file_path = str(tool_input.get("file_path", ""))
    if not any(file_path.replace("\\", "/").endswith(name) for name in LOCKED_FILES):
        return 0

    chunks: list[str] = []
    for key in ("old_string", "new_string", "content"):
        chunks.append(_stringify(tool_input.get(key)))
    for edit in tool_input.get("edits", []) or []:
        for key in ("old_string", "new_string"):
            chunks.append(_stringify(edit.get(key)))

    blob = "\n".join(c for c in chunks if c)
    if not LOCKED_PATTERN.search(blob):
        return 0

    script = Path(__file__).resolve().parent / "verify_lock_anchors.py"
    if not script.exists():
        return 0

    repo_root = script.parent.parent
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(repo_root),
        check=False,
        capture_output=True,
        text=True,
    )
    # Surface, don't swallow (fixed 2026-08-08). verify_lock_anchors returns a
    # meaningful decision.exit_code() and reports ONLY on stdout — it has no file
    # sink. The previous form captured both streams into a discarded variable and
    # returned 0 unconditionally, so every finding it could produce was destroyed
    # on every matching edit. Mirrors scripts/sync_skills_hook.py: a PostToolUse
    # exit 2 reaches the agent without blocking the edit, which is the right
    # severity for an advisory skew check.
    if result.returncode != 0:
        print(
            f"lock-anchor check reported findings (exit {result.returncode}) "
            f"after an edit to a locked-surface file:",
            file=sys.stderr,
        )
        if result.stdout:
            sys.stderr.write(result.stdout)
        if result.stderr:
            sys.stderr.write(result.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
