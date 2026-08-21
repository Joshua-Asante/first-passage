import pytest

from lab.research_utils.mechanism_prior_schema import (
    TagValidationError,
    validate_tag_record,
)


def test_valid_record_passes(valid_tag_record):
    validate_tag_record(valid_tag_record())  # must not raise


def test_missing_field_rejected(valid_tag_record):
    record = valid_tag_record()
    del record["outcome"]
    with pytest.raises(TagValidationError, match="missing required fields"):
        validate_tag_record(record)


def test_bad_mechanism_tier_rejected(valid_tag_record):
    with pytest.raises(TagValidationError, match="mechanism_tier"):
        validate_tag_record(valid_tag_record(mechanism_tier="Z"))


def test_bad_sourcing_channel_rank_rejected(valid_tag_record):
    with pytest.raises(TagValidationError, match="sourcing_channel_rank"):
        validate_tag_record(valid_tag_record(sourcing_channel_rank="7"))


def test_bad_outcome_rejected(valid_tag_record):
    with pytest.raises(TagValidationError, match="outcome"):
        validate_tag_record(valid_tag_record(outcome="MAYBE"))


def test_empty_instrument_family_rejected(valid_tag_record):
    with pytest.raises(TagValidationError, match="target_instrument_family"):
        validate_tag_record(valid_tag_record(target_instrument_family="  "))


def test_provenance_must_be_object(valid_tag_record):
    with pytest.raises(TagValidationError, match="provenance must be an object"):
        validate_tag_record(valid_tag_record(provenance="not-a-dict"))


def test_provenance_missing_subfield_rejected(valid_tag_record):
    record = valid_tag_record()
    del record["provenance"]["tagged_at"]
    with pytest.raises(TagValidationError, match="provenance missing fields"):
        validate_tag_record(record)


def test_n_a_sourcing_channel_allowed_for_mined_entries(valid_tag_record):
    validate_tag_record(valid_tag_record(sourcing_channel_rank="n/a"))  # must not raise


def test_extra_provenance_fields_allowed(valid_tag_record):
    record = valid_tag_record()
    record["provenance"]["reasoning"] = "cites the closure's own FALSIFIED verdict"
    validate_tag_record(record)  # must not raise -- extra fields are fine
