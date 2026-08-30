#!/usr/bin/env python3
"""Report-only: Notice GRADUATE verdicts whose cited K is above the DSR-reachable band.

Writes nothing. Exit code is always 0. Not a gate.
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
    graduate_scanned = 0

    for path in notices:
        text = path.read_text(encoding="utf-8")
        status_line = next(
            (line for line in text.splitlines() if STATUS_RE.match(line)),
            None,
        )
        if status_line is None or "GRADUATE" not in status_line:
            continue
        graduate_scanned += 1
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
    return flagged, skips, graduate_scanned, total


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Report-only Notice GRADUATE K vs DSR-reachable band",
    )
    parser.add_argument("--repo-root", type=Path, default=None)
    args = parser.parse_args(argv)
    root = args.repo_root.resolve() if args.repo_root is not None else REPO
    flagged, skips, graduate_scanned, total = run_audit(root)
    for msg in skips:
        print(msg, file=sys.stderr)
    for notice_file, manifest_path, k, floor in flagged:
        print(
            f"{notice_file}\t{manifest_path}\tK={k}\t"
            f"floor_at_k(K)={floor:.4f}\tCAP={CAP}"
        )
    print(
        f"[audit] {len(flagged)} flagged / {graduate_scanned} "
        f"GRADUATE notices scanned / {total} total notices"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
