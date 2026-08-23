"""Burned-segment ledger — dual-panel audit finding B1 (2026-08-22).

CON-2/3/4/5 share one physical MNQ CONFIRM window (2025-09-01 -> 2026-08-05);
CON-4's read spent it 2026-08-20. A deep-lane campaign that later touches this
window is a second consultation of a burned segment, forbidden by GROW spec
v2's Boundary. This module is a standalone checker (not yet wired into
register_search.open_run -- named forward work in the 2026-08-22 build ADR
§2.2) that answers one question: is (instrument, window) already burned?

Extended 2026-08-22 (docs/adr/2026-08-22-grow0-two-ledger-k-question.md §2 Part
B, charter §2.2(iv)): each segment's single read_date/source pair migrated to
a ``consultations`` list, so consultation_count/consultation_history can
answer "how many times, by whom" -- channel-agnostic, disclosure-only, never
a refusal.
"""
from __future__ import annotations

import json

from discovery.burned_segments import (
    BURNED_SEGMENTS_PATH,
    consultation_count,
    consultation_history,
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
    consultations = matches[0]["consultations"]
    assert len(consultations) == 1
    assert consultations[0]["date"] == "2026-08-20"
    assert consultations[0]["source"] == (
        "docs/notes/audits/2026-08-22-grow-lane-dual-panel-review.md B1"
    )


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


def test_consultation_count_zero_for_unlisted_window():
    assert consultation_count("MGC", "2010-01-01", "2011-01-01") == 0
    assert consultation_history("MGC", "2010-01-01", "2011-01-01") == []


def test_consultation_count_one_for_the_seeded_entry():
    assert consultation_count("MNQ", "2025-09-01", "2026-08-05") == 1


def test_consultation_count_is_channel_agnostic_and_sums_across_overlapping_segments(
    tmp_path,
):
    # Two DIFFERENT channels/sources consulting overlapping-but-distinct
    # segments for the same instrument -- M sums across both, not just one.
    ledger = tmp_path / "burned_segments.json"
    ledger.write_text(
        json.dumps(
            [
                {
                    "instrument": "MGC",
                    "window_start": "2020-01-01",
                    "window_end": "2020-12-31",
                    "reason": "seed A",
                    "consultations": [
                        {
                            "source": "campaign-A",
                            "date": "2026-01-01",
                            "declared_k": 10,
                            "floor_at_k": 1.265,
                        }
                    ],
                },
                {
                    "instrument": "MGC",
                    "window_start": "2020-06-01",
                    "window_end": "2021-06-01",
                    "reason": "seed B, overlaps seed A",
                    "consultations": [
                        {
                            "source": "campaign-B",
                            "date": "2026-02-01",
                            "declared_k": 33,
                            "floor_at_k": 1.475,
                        }
                    ],
                },
            ]
        ),
        encoding="utf-8",
    )
    count = consultation_count("MGC", "2020-03-01", "2020-09-01", path=ledger)
    history = consultation_history("MGC", "2020-03-01", "2020-09-01", path=ledger)
    assert count == 2
    assert {c["source"] for c in history} == {"campaign-A", "campaign-B"}


def test_consultation_history_exposes_declared_k_and_floor_when_known(tmp_path):
    ledger = tmp_path / "burned_segments.json"
    ledger.write_text(
        json.dumps(
            [
                {
                    "instrument": "M6A",
                    "window_start": "2019-01-01",
                    "window_end": "2026-01-01",
                    "reason": "seed",
                    "consultations": [
                        {
                            "source": "campaign-C",
                            "date": "2026-03-01",
                            "declared_k": 5,
                            "floor_at_k": 1.1,
                        }
                    ],
                }
            ]
        ),
        encoding="utf-8",
    )
    history = consultation_history("M6A", "2019-06-01", "2019-07-01", path=ledger)
    assert history == [
        {
            "source": "campaign-C",
            "date": "2026-03-01",
            "declared_k": 5,
            "floor_at_k": 1.1,
        }
    ]
