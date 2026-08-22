import pytest

from discovery.grow0_red_patch import (
    assert_intraday_channel_required,
    assert_singleton_attestation,
    reproduce_m23_parent_only_patch,
    run_red_patch,
)


def test_assert_intraday_channel_required_raises_on_none():
    with pytest.raises(ValueError):
        assert_intraday_channel_required(None)


def test_assert_intraday_channel_required_accepts_real_blocks():
    import numpy as np

    assert_intraday_channel_required(np.zeros((3, 5)))  # must not raise


def test_assert_singleton_attestation_raises_on_non_singleton_set():
    with pytest.raises(AssertionError):
        assert_singleton_attestation([1.0, 1.0, 2.0, 1.0], expected=1.0)


def test_assert_singleton_attestation_passes_on_singleton_set():
    assert_singleton_attestation([1.0, 1.0, 1.0, 1.0], expected=1.0)  # must not raise


def test_reproduce_m23_parent_only_patch_shows_workers_miss_the_patch():
    """This is the RED control's own 'the bug exists' sanity check -- workers under
    joblib's processes backend re-import firm_rules fresh, so they do NOT see the
    parent process's runtime patch."""
    attestations = reproduce_m23_parent_only_patch()
    assert len(attestations) == 4
    assert set(attestations) != {500.0}  # not all workers saw the parent's patch


def test_run_red_patch_reports_failed_as_expected():
    assert run_red_patch() == "FAILED_AS_EXPECTED"
