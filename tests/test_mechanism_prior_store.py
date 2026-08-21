import json

import pytest

from lab.research_utils.mechanism_prior_schema import TagValidationError
from lab.research_utils.mechanism_prior_store import (
    append_record,
    load_all_records,
    load_latest_records,
)


def test_load_all_records_missing_file_returns_empty(tmp_path):
    assert load_all_records(tmp_path / "nope.json") == []


def test_append_then_load_round_trips(tmp_path, valid_tag_record):
    store = tmp_path / "tags.json"
    append_record(valid_tag_record(), store_path=store)
    records = load_all_records(store)
    assert len(records) == 1
    assert records[0]["mechanism_tier"] == "A"


def test_append_is_one_line_per_record(tmp_path, valid_tag_record):
    store = tmp_path / "tags.json"
    append_record(
        valid_tag_record(provenance={"source_path": "x", "source_ref": "1", "tagged_at": "d"}), store_path=store
    )
    append_record(
        valid_tag_record(provenance={"source_path": "x", "source_ref": "2", "tagged_at": "d"}), store_path=store
    )
    lines = store.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2
    json.loads(lines[0])
    json.loads(lines[1])


def test_append_rejects_invalid_record(tmp_path, valid_tag_record):
    store = tmp_path / "tags.json"
    with pytest.raises(TagValidationError):
        append_record(valid_tag_record(mechanism_tier="nope"), store_path=store)
    assert not store.exists()


def test_append_never_truncates_existing_content(tmp_path, valid_tag_record):
    store = tmp_path / "tags.json"
    append_record(
        valid_tag_record(provenance={"source_path": "x", "source_ref": "1", "tagged_at": "d"}), store_path=store
    )
    append_record(
        valid_tag_record(provenance={"source_path": "x", "source_ref": "2", "tagged_at": "d"}), store_path=store
    )
    assert len(load_all_records(store)) == 2


def test_load_latest_prefers_superseding_record(tmp_path, valid_tag_record):
    store = tmp_path / "tags.json"
    original = valid_tag_record(
        mechanism_tier="B",
        provenance={"source_path": "docs/rejected_candidates.md", "source_ref": "entry-9", "tagged_at": "2026-08-18"},
    )
    append_record(original, store_path=store)

    correction = valid_tag_record(
        mechanism_tier="A",
        provenance={
            "source_path": "docs/rejected_candidates.md",
            "source_ref": "entry-9-correction",
            "tagged_at": "2026-08-20",
        },
        supersedes={"source_path": "docs/rejected_candidates.md", "source_ref": "entry-9"},
    )
    append_record(correction, store_path=store)

    latest = load_latest_records(store)
    assert len(latest) == 1
    assert latest[0]["mechanism_tier"] == "A"


def test_load_latest_keeps_unrelated_records(tmp_path, valid_tag_record):
    store = tmp_path / "tags.json"
    append_record(
        valid_tag_record(provenance={"source_path": "x", "source_ref": "1", "tagged_at": "d"}), store_path=store
    )
    append_record(
        valid_tag_record(provenance={"source_path": "x", "source_ref": "2", "tagged_at": "d"}), store_path=store
    )
    assert len(load_latest_records(store)) == 2
