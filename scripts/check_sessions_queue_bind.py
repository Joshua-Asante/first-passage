#!/usr/bin/env python3
"""Newest SESSIONS Open/next must cite every live STATE operator-queue row.

Owns the queue-bind mechanical limb (Survive-bound addendum 2026-08-23 /
W5 addendum 2026-08-23). Reads only STATE.md and docs/SESSIONS.md — no leftover
name parsing, no other trees.

Exit 0 if every live ``#N`` appears in the newest entry's Open/next line.
Exit 1 on a missing row, a missing section, or an unreadable file.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_STATE = REPO / "STATE.md"
DEFAULT_SESSIONS = REPO / "docs" / "SESSIONS.md"

QUEUE_SECTION_RE = re.compile(
    r"^## OPERATOR QUEUE\b.*?(?=^## |\Z)",
    re.M | re.S,
)
ROW_RE = re.compile(r"^\| (\d+) \|", re.M)
ENTRY_SPLIT_RE = re.compile(r"(?m)^## \d{4}-\d{2}-\d{2}")
OPEN_NEXT_RE = re.compile(
    r"\*\*Open / next:?\*\*(.*?)(?=\n\*\*[A-Za-z]|\n---|\Z)",
    re.S,
)


def live_queue_ids(state_text: str) -> list[int]:
    section = QUEUE_SECTION_RE.search(state_text)
    if section is None:
        raise ValueError("STATE.md has no OPERATOR QUEUE section")
    ids = [int(m.group(1)) for m in ROW_RE.finditer(section.group(0))]
    if not ids:
        raise ValueError("OPERATOR QUEUE table has no numbered rows")
    return ids


def newest_open_next(sessions_text: str) -> str:
    parts = ENTRY_SPLIT_RE.split(sessions_text, maxsplit=2)
    if len(parts) < 2:
        raise ValueError("docs/SESSIONS.md has no dated entry")
    newest_body = parts[1]
    match = OPEN_NEXT_RE.search(newest_body)
    if match is None:
        raise ValueError("newest SESSIONS entry has no Open / next field")
    return match.group(1)


def missing_row_cites(open_next: str, ids: list[int]) -> list[int]:
    return [n for n in ids if f"#{n}" not in open_next]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--file", type=Path, default=DEFAULT_SESSIONS)
    args = parser.parse_args(argv)
    try:
        state_text = args.state.read_text(encoding="utf-8")
        sessions_text = args.file.read_text(encoding="utf-8")
        ids = live_queue_ids(state_text)
        open_next = newest_open_next(sessions_text)
    except (OSError, ValueError) as exc:
        print(f"sessions-queue-bind: FAIL — {exc}", file=sys.stderr)
        return 1
    missing = missing_row_cites(open_next, ids)
    if missing:
        cited = ", ".join(f"#{n}" for n in missing)
        print(
            f"sessions-queue-bind: FAIL — newest Open/next omits {cited}",
            file=sys.stderr,
        )
        return 1
    print(
        "sessions-queue-bind: OK — newest Open/next cites "
        + ", ".join(f"#{n}" for n in ids)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
