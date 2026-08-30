#!/usr/bin/env python3
"""Report-only: Notice GRADUATE/INCREMENT verdicts whose cited K is above the
DSR-reachable band.

Writes nothing. Exit code is always 0. Not a gate.

Widened 2026-08-30 (Codex review, PR #223) from GRADUATE-only: a Status line
reading e.g. "OPEN -- INCREMENT" routes into a Q-brief the same way GRADUATE
does (both mean "this candidate cleared its stage-1 bar and is being carried
forward"), and was silently skipped before this fix even when it cited the
same over-floor manifest as its GRADUATE siblings.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "lab"))

from research_utils.axis_screen import CAP, floor_at_k  # noqa: E402

STATUS_RE = re.compile(r"^\*\*Status:\*\*")
MANIFEST_RE = re.compile(r"discovery_manifests/[\w.-]+\.json")


def _valid_k(value: object) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        return None
    return value


def run_audit(
    repo_root: Path,
) -> tuple[list[tuple[str, str, int, float]], list[str], int, int]:
    notice_dir = repo_root / "docs" / "notes" / "notice"
    notices = sorted(notice_dir.glob("N-*.md"))
    total = len(notices)
    flagged: list[tuple[str, str, int, float]] = []
    skips: list[str] = []
    promoted_scanned = 0
    ROUTED_TOKENS = ("GRADUATE", "INCREMENT")

    for path in notices:
        text = path.read_text(encoding="utf-8")
        status_line = next(
            (line for line in text.splitlines() if STATUS_RE.match(line)),
            None,
        )
        if status_line is None or not any(tok in status_line for tok in ROUTED_TOKENS):
            continue
        promoted_scanned += 1
        seen: list[str] = []
        for match in MANIFEST_RE.findall(text):
            if match not in seen:
                seen.append(match)
        for match in seen:
            man_path = repo_root / match
            if not man_path.is_file():
                skips.append(f"[skip] manifest not found: {match}")
                continue
            try:
                data = json.loads(man_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                skips.append(f"[skip] no valid K in manifest: {match}")
                continue
            k = _valid_k(data.get("K") if isinstance(data, dict) else None)
            if k is None:
                skips.append(f"[skip] no valid K in manifest: {match}")
                continue
            floor = floor_at_k(k)
            if floor > CAP:
                flagged.append((path.name, match, k, floor))

    flagged.sort(key=lambda row: row[0])
    return flagged, skips, promoted_scanned, total


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Report-only Notice GRADUATE/INCREMENT K vs DSR-reachable band",
    )
    parser.add_argument("--repo-root", type=Path, default=None)
    args = parser.parse_args(argv)
    root = args.repo_root.resolve() if args.repo_root is not None else REPO
    flagged, skips, promoted_scanned, total = run_audit(root)
    for msg in skips:
        print(msg, file=sys.stderr)
    for notice_file, manifest_path, k, floor in flagged:
        print(
            f"{notice_file}\t{manifest_path}\tK={k}\t"
            f"floor_at_k(K)={floor:.4f}\tCAP={CAP}"
        )
    print(
        f"[audit] {len(flagged)} flagged / {promoted_scanned} "
        f"GRADUATE/INCREMENT notices scanned / {total} total notices"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
