import json
from pathlib import Path

import pytest

from lab.research_utils.mechanism_prior_ingest import ingest, main, validate_batch
from lab.research_utils.mechanism_prior_schema import TagValidationError
from lab.research_utils.mechanism_prior_store import load_all_records


def _write_proposed(path: Path, records: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(r) for r in records) + "\n", encoding="utf-8")


def _prov(ref: str) -> dict:
    return {"source_path": "docs/rejected_candidates.md", "source_ref": ref, "tagged_at": "2026-08-20"}


def test_validate_batch_all_valid_returns_no_errors(valid_tag_record):
    records = [valid_tag_record(provenance=_prov("1")), valid_tag_record(provenance=_prov("2"))]
    assert validate_batch(records) == []


def test_validate_batch_reports_each_bad_record_with_locator(valid_tag_record):
    bad = valid_tag_record(mechanism_tier="nope", provenance=_prov("3"))
    good = valid_tag_record(provenance=_prov("1"))
    errors = validate_batch([good, bad])
    assert len(errors) == 1
    assert "record 1" in errors[0]
    assert "3" in errors[0]


def test_ingest_appends_full_valid_batch(tmp_path, valid_tag_record):
    proposed = tmp_path / "proposed.jsonl"
    store = tmp_path / "tags.json"
    records = [valid_tag_record(provenance=_prov(ref)) for ref in ("1", "2", "3")]
    _write_proposed(proposed, records)

    count = ingest(proposed, store_path=store)

    assert count == 3
    assert len(load_all_records(store)) == 3


def test_ingest_rejects_whole_batch_on_any_invalid_record(tmp_path, valid_tag_record):
    proposed = tmp_path / "proposed.jsonl"
    store = tmp_path / "tags.json"
    bad = valid_tag_record(outcome="MAYBE", provenance=_prov("2"))
    records = [valid_tag_record(provenance=_prov("1")), bad, valid_tag_record(provenance=_prov("3"))]
    _write_proposed(proposed, records)

    with pytest.raises(TagValidationError, match="0 records appended"):
        ingest(proposed, store_path=store)

    assert not store.exists()


def test_cli_exit_code_1_on_bad_batch(tmp_path, capsys, valid_tag_record):
    proposed = tmp_path / "proposed.jsonl"
    store = tmp_path / "tags.json"
    bad = valid_tag_record(mechanism_tier="nope", provenance=_prov("1"))
    _write_proposed(proposed, [bad])

    exit_code = main([str(proposed), "--store", str(store)])

    assert exit_code == 1
    assert "batch rejected" in capsys.readouterr().err


def test_cli_exit_code_0_and_message_on_success(tmp_path, capsys, valid_tag_record):
    proposed = tmp_path / "proposed.jsonl"
    store = tmp_path / "tags.json"
    _write_proposed(proposed, [valid_tag_record(provenance=_prov("1"))])

    exit_code = main([str(proposed), "--store", str(store)])

    assert exit_code == 0
    assert "appended 1 records" in capsys.readouterr().out
