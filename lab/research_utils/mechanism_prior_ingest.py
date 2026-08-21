"""Batch-validate and append proposed mechanism-prior tag records.

Used by the one-time tagging pass (design spec §3/§4, Task 7 of this
plan). Reads a JSON-Lines file of PROPOSED records, validates every one
against the schema, and only appends to the store if the WHOLE batch is
valid -- never a partial append, so a malformed batch can be fixed and
re-run without hand-auditing what already landed.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from lab.research_utils.mechanism_prior_schema import TagValidationError, validate_tag_record
from lab.research_utils.mechanism_prior_store import DEFAULT_STORE_PATH, append_record


def load_proposed_records(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def validate_batch(records: list[dict]) -> list[str]:
    """Return one error string per invalid record (empty list if all valid)."""
    errors = []
    for i, record in enumerate(records):
        try:
            validate_tag_record(record)
        except TagValidationError as exc:
            ref = record.get("provenance", {}).get("source_ref", "?")
            errors.append(f"record {i} ({ref}): {exc}")
    return errors


def ingest(proposed_path: Path, store_path: Path = DEFAULT_STORE_PATH) -> int:
    """Validate then append every record in `proposed_path` to `store_path`.

    Returns the count appended. Raises TagValidationError (all failures
    joined) if any record is invalid -- nothing is appended in that case.
    """
    records = load_proposed_records(proposed_path)
    errors = validate_batch(records)
    if errors:
        raise TagValidationError("batch rejected, 0 records appended:\n" + "\n".join(errors))
    for record in records:
        append_record(record, store_path=store_path)
    return len(records)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("proposed", type=Path, help="JSON-Lines file of proposed tag records")
    parser.add_argument("--store", type=Path, default=DEFAULT_STORE_PATH)
    args = parser.parse_args(argv)

    try:
        count = ingest(args.proposed, args.store)
    except TagValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"appended {count} records to {args.store}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
