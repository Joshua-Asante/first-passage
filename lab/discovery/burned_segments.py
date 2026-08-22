"""burned_segments.py — ledger of sealed data windows already read/spent.

Seeded by the 2026-08-22 dual-panel review's finding B1: GROW spec v1's D3
proposed re-reading the shared CON-2/3/4/5 MNQ CONFIRM window, unaware CON-4
had already spent it under the U1 override on 2026-08-20. This module answers
"is (instrument, window) already burned?" mechanically, so a future campaign
prereg cannot repeat that mistake.

Standalone checker only -- NOT yet wired into register_search.open_run (named
forward work, docs/adr/2026-08-22-grow-lane-build-authorization.md §2.2). A
campaign author calls this by hand at prereg-authoring time until the wiring
lands; an unlisted window is neither burned nor clean -- callers must not
read absence as "safe".
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from research_utils.repo_root import repo_root

BURNED_SEGMENTS_PATH = repo_root() / "discovery_manifests" / "burned_segments.json"


def load_burned_segments(path: str | Path | None = None) -> list[dict[str, Any]]:
    p = Path(path) if path is not None else BURNED_SEGMENTS_PATH
    if not p.exists():
        return []
    raw = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError(f"{p}: burned-segments ledger must be a JSON array")
    return raw


def _parse(d: str) -> date:
    return date.fromisoformat(d)


def is_window_burned(
    instrument: str,
    window_start: str,
    window_end: str,
    *,
    path: str | Path | None = None,
) -> bool:
    """True if [window_start, window_end] overlaps any burned segment for
    ``instrument`` (case-sensitive symbol match). Overlap, not exact match --
    a narrower sub-window inside a burned segment is still burned data."""
    start = _parse(window_start)
    end = _parse(window_end)
    if end < start:
        raise ValueError("window_end must be >= window_start")
    for seg in load_burned_segments(path):
        if seg.get("instrument") != instrument:
            continue
        seg_start = _parse(seg["window_start"])
        seg_end = _parse(seg["window_end"])
        if start <= seg_end and seg_start <= end:
            return True
    return False
