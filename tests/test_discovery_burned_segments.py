"""Burned-segment ledger — dual-panel audit finding B1 (2026-08-22).

CON-2/3/4/5 share one physical MNQ CONFIRM window (2025-09-01 -> 2026-08-05);
CON-4's read spent it 2026-08-20. A deep-lane campaign that later touches this
window is a second consultation of a burned segment, forbidden by GROW spec
v2's Boundary. This module is a standalone checker (not yet wired into
register_search.open_run -- named forward work in the 2026-08-22 build ADR
§2.2) that answers one question: is (instrument, window) already burned?
"""
from __future__ import annotations

from discovery.burned_segments import (
    BURNED_SEGMENTS_PATH,
    is_window_burned,
    load_burned_segments,
)


def test_seed_file_exists_and_loads():
    segments = load_burned_segments()
    assert segments, "burned_segments.json must not be empty at seed time"


def test_seed_contains_the_shared_con_window():
    segments = load_burned_segments()
    matches = [
        s
        for s in segments
        if s["instrument"] == "MNQ"
        and s["window_start"] == "2025-09-01"
        and s["window_end"] == "2026-08-05"
    ]
    assert matches, "the shared CON-2/3/4/5 MNQ window must be seeded as burned"
    assert matches[0]["read_date"] == "2026-08-20"


def test_is_window_burned_true_for_seeded_window():
    assert is_window_burned("MNQ", "2025-09-01", "2026-08-05") is True


def test_is_window_burned_false_for_unrelated_window():
    assert is_window_burned("MGC", "2010-01-01", "2011-01-01") is False


def test_is_window_burned_true_for_overlap_not_just_exact_match():
    # A campaign proposing a sub-window entirely inside the burned segment is
    # still touching burned data -- exact-match-only would let a narrower
    # slice of the same burned window sneak through unflagged.
    assert is_window_burned("MNQ", "2025-10-01", "2025-11-01") is True


def test_is_window_burned_false_for_adjacent_non_overlapping_window():
    assert is_window_burned("MNQ", "2026-08-06", "2026-09-01") is False


def test_path_is_repo_relative_and_committed_location():
    assert BURNED_SEGMENTS_PATH.name == "burned_segments.json"
    assert BURNED_SEGMENTS_PATH.parent.name == "discovery_manifests"
