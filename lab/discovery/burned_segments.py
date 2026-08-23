"""burned_segments.py — ledger of sealed data windows already read/spent.

Seeded by the 2026-08-22 dual-panel review's finding B1: GROW spec v1's D3
proposed re-reading the shared CON-2/3/4/5 MNQ CONFIRM window, unaware CON-4
had already spent it under the U1 override on 2026-08-20. This module answers
"is (instrument, window) already burned?" mechanically, so a future campaign
prereg cannot repeat that mistake.

Extended 2026-08-22 per docs/adr/2026-08-22-grow0-two-ledger-k-question.md
section 2 Part B (charter section 2.2(iv), disclosure-only): each segment now
carries a ``consultations`` list (source/date/declared_k/floor_at_k per read)
instead of a single flat read_date/source pair, so a *second* consultation of
an overlapping window is recorded as its own entry, never a silent overwrite.
``consultation_count``/``consultation_history`` are channel-agnostic -- they
count every recorded read regardless of which channel (deep-lane, CON-class,
or otherwise) originated it, per the ADR's own correction that this ledger is
already cross-channel in practice.

Standalone checker only -- NOT yet wired into register_search.open_run (named
forward work, docs/adr/2026-08-22-grow-lane-build-authorization.md section
2.2). A campaign author calls this by hand at prereg-authoring time until the
wiring lands; an unlisted window is neither burned nor clean -- callers must
not read absence as "safe". Section 2.2(iv)'s own disclosure obligation is
likewise enforced by human review at prereg time, not by an automated gate,
until that same wiring lands.
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


def _overlapping_segments(
    instrument: str,
    window_start: str,
    window_end: str,
    *,
    path: str | Path | None,
) -> list[dict[str, Any]]:
    """Every segment for ``instrument`` whose window overlaps [start, end]."""
    start = _parse(window_start)
    end = _parse(window_end)
    if end < start:
        raise ValueError("window_end must be >= window_start")
    out = []
    for seg in load_burned_segments(path):
        if seg.get("instrument") != instrument:
            continue
        seg_start = _parse(seg["window_start"])
        seg_end = _parse(seg["window_end"])
        if start <= seg_end and seg_start <= end:
            out.append(seg)
    return out


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
    return bool(_overlapping_segments(instrument, window_start, window_end, path=path))


def consultation_count(
    instrument: str,
    window_start: str,
    window_end: str,
    *,
    path: str | Path | None = None,
) -> int:
    """``M`` -- the total number of recorded consultations (any channel)
    against any segment overlapping [window_start, window_end] for
    ``instrument``. Zero for an unlisted or never-consulted window; this is a
    disclosure count, not a refusal (charter section 2.2(iv))."""
    return len(consultation_history(instrument, window_start, window_end, path=path))


def consultation_history(
    instrument: str,
    window_start: str,
    window_end: str,
    *,
    path: str | Path | None = None,
) -> list[dict[str, Any]]:
    """Every recorded consultation (channel-agnostic) against any segment
    overlapping [window_start, window_end] for ``instrument``, flattened
    across segments. Each entry carries whatever of
    ``source``/``date``/``declared_k``/``floor_at_k`` the recording channel
    supplied -- ``declared_k``/``floor_at_k`` are ``None`` for consultations
    recorded before this disclosure existed (the seed entry)."""
    out: list[dict[str, Any]] = []
    for seg in _overlapping_segments(instrument, window_start, window_end, path=path):
        out.extend(seg.get("consultations", []))
    return out
