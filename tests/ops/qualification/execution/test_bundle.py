"""Byte-only admission revalidates originals and the installed release identity."""
import importlib
import json

import pytest
from bundle_fixture import build_bundle
from test_contract import NOW


def verify(case):
    admission = importlib.import_module('c1_rail.qualification.execution.admission')
    return admission.verify_bundle(case['root'], case['release'], case['keys'], NOW)


def test_original_signed_context_is_reconstructed_without_source_execution(tmp_path):
    case = build_bundle(tmp_path / 'bundle')
    context = verify(case)
    assert context.contract.contract_sha256 == case['contract'].contract_sha256
    assert context.attempt_id == case['attempt_id']
    assert context.retained_bundle_index == case['index']


def test_changed_retained_bytes_cannot_borrow_index_identity(tmp_path):
    case = build_bundle(tmp_path / 'bundle')
    (case['root'] / case['paths']['orb_runtime_port']).write_bytes(b'caller code')
    with pytest.raises(ValueError, match='retained.*identity|length'):
        verify(case)


def test_signed_bundle_cannot_select_another_installed_release(tmp_path):
    case = build_bundle(tmp_path / 'bundle')
    case['release'] = case['release'].replace(b'unit-release', b'other-release')
    with pytest.raises(ValueError, match='installed release'):
        verify(case)


def test_resigned_nonempty_registry_is_rejected_at_bundle_admission(tmp_path):
    from test_legality_evidence import NONEMPTY
    case = build_bundle(tmp_path / 'bundle',geometry_bytes=NONEMPTY)
    with pytest.raises(ValueError,match='LEGALITY_REGISTRY_NOT_EMPTY'):
        verify(case)
