"""Append-only storage for mechanism-prior tag records.

JSON-Lines format -- one record per line, genuinely append-only. See
docs/superpowers/specs/2026-08-20-cross-campaign-mechanism-prior-design.md
§4/§6.
"""

from __future__ import annotations

import json
from pathlib import Path

from lab.research_utils.mechanism_prior_schema import validate_tag_record

DEFAULT_STORE_PATH = Path("lab/research_utils/mechanism_prior_tags.json")


def load_all_records(store_path: Path = DEFAULT_STORE_PATH) -> list[dict]:
    """Return every record in the store, in file order. Empty list if missing/empty."""
    if not store_path.exists():
        return []
    text = store_path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def _record_key(record: dict) -> tuple[str, str]:
    prov = record["provenance"]
    return (prov["source_path"], prov["source_ref"])


def load_latest_records(store_path: Path = DEFAULT_STORE_PATH) -> list[dict]:
    """Return one record per (source_path, source_ref), dropping any record
    a later record's `supersedes` pointer names. The superseded record still
    exists on disk (append-only) -- it is only excluded from this view.
    """
    all_records = load_all_records(store_path)
    latest: dict[tuple[str, str], dict] = {}
    superseded_keys: set[tuple[str, str]] = set()

    for record in all_records:
        key = _record_key(record)
        latest[key] = record
        if "supersedes" in record:
            sup = record["supersedes"]
            sup_key = (sup["source_path"], sup["source_ref"])
            if sup_key != key:
                superseded_keys.add(sup_key)

    return [rec for key, rec in latest.items() if key not in superseded_keys]


def append_record(record: dict, store_path: Path = DEFAULT_STORE_PATH) -> None:
    """Validate and append one record as a new line. Never overwrites."""
    validate_tag_record(record)
    store_path.parent.mkdir(parents=True, exist_ok=True)
    with store_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, sort_keys=True) + "\n")
