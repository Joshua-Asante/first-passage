"""Boundary wrapper must reject unsupported setups before running any tests."""
import importlib
import json
from pathlib import Path
import pytest


def runner():
    name = 'scripts.qualification_boundary_verification'
    assert importlib.util.find_spec(name), 'boundary verification wrapper is missing'
    return importlib.import_module(name)


def test_empty_or_skipped_acceptance_is_not_success():
    module = runner()
    for counts in ({'collected': 0, 'failed': 0, 'errors': 0, 'skipped': 0},
                   {'collected': 10, 'failed': 0, 'errors': 0, 'skipped': 1}):
        with pytest.raises(ValueError):
            module.require_tests(counts)


def test_partial_or_failed_report_is_rejected():
    module = runner()
    for counts in (None, {}, {'collected': 3, 'passed': 2, 'failed': 1, 'errors': 0, 'skipped': 0}):
        with pytest.raises(ValueError):
            module.require_tests(counts)


def test_nonlinux_entry_point_fails_without_provisioning(monkeypatch):
    module = runner()
    monkeypatch.setattr(module.platform, 'system', lambda: 'Windows')
    assert module.main(['--test-only']) != 0
