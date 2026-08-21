"""Schema and validation for cross-campaign mechanism-prior tag records.

See docs/superpowers/specs/2026-08-20-cross-campaign-mechanism-prior-design.md.
"""

from __future__ import annotations

MECHANISM_TIERS = {"A", "B", "C", "unclear"}
SOURCING_CHANNEL_RANKS = {"1", "2", "3", "4", "5", "6", "1-tie", "n/a"}
OUTCOMES = {"SURVIVED", "KILLED_AT_ADMISSION", "KILLED_AT_TEST", "AMBIGUOUS"}

REQUIRED_FIELDS = {
    "mechanism_tier",
    "sourcing_channel_rank",
    "target_instrument_family",
    "outcome",
    "provenance",
}

PROVENANCE_REQUIRED_FIELDS = {"source_path", "source_ref", "tagged_at"}


class TagValidationError(ValueError):
    """Raised when a proposed tag record fails schema validation."""


def validate_tag_record(record: dict) -> None:
    """Raise TagValidationError if `record` does not conform to the schema.

    Does not mutate `record`. Safe to call before appending. Extra keys
    (e.g. provenance.reasoning) are always allowed -- this validates the
    required shape, not a closed schema.
    """
    missing = REQUIRED_FIELDS - record.keys()
    if missing:
        raise TagValidationError(f"missing required fields: {sorted(missing)}")

    if record["mechanism_tier"] not in MECHANISM_TIERS:
        raise TagValidationError(
            f"mechanism_tier {record['mechanism_tier']!r} not in {sorted(MECHANISM_TIERS)}"
        )
    if record["sourcing_channel_rank"] not in SOURCING_CHANNEL_RANKS:
        raise TagValidationError(
            f"sourcing_channel_rank {record['sourcing_channel_rank']!r} "
            f"not in {sorted(SOURCING_CHANNEL_RANKS)}"
        )
    if record["outcome"] not in OUTCOMES:
        raise TagValidationError(f"outcome {record['outcome']!r} not in {sorted(OUTCOMES)}")

    instrument = record["target_instrument_family"]
    if not isinstance(instrument, str) or not instrument.strip():
        raise TagValidationError("target_instrument_family must be a non-empty string")

    provenance = record["provenance"]
    if not isinstance(provenance, dict):
        raise TagValidationError("provenance must be an object")
    missing_prov = PROVENANCE_REQUIRED_FIELDS - provenance.keys()
    if missing_prov:
        raise TagValidationError(f"provenance missing fields: {sorted(missing_prov)}")

    if "supersedes" in record and not isinstance(record["supersedes"], dict):
        raise TagValidationError("supersedes, if present, must be an object with source_path/source_ref")
