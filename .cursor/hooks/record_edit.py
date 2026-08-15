#!/usr/bin/env python3
"""Cursor afterFileEdit — record hot-surface edits for blast-radius stop nudge.

Appends touched paths into ``.cursor/hooks/state/<conversation_id>.json``.
Fail-open: never blocks edits. Emits ``{}`` (no afterFileEdit output fields).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Cursor runs ``python .cursor/hooks/record_edit.py`` from repo root — ensure
# sibling imports resolve without requiring PYTHONPATH.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from blast_radius_ledger import record_edit, repo_root  # noqa: E402


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.stdout.write("{}")
        return 0

    if not isinstance(data, dict):
        sys.stdout.write("{}")
        return 0

    file_path = str(data.get("file_path") or "")
    conversation_id = str(data.get("conversation_id") or "default")
    if file_path:
        try:
            record_edit(conversation_id, file_path, repo_root())
        except Exception as exc:
            sys.stderr.write(f"[blast-radius record] {exc}\n")

    sys.stdout.write("{}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
