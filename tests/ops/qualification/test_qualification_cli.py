import base64
from datetime import datetime, timezone

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from c1_rail.qualification.attempt import AttemptStore
from c1_rail.qualification.contract import canonical_json_bytes
from c1_rail.qualification_cli import (
    QualificationCLIError, exact_depth_subject, load_trusted_approval_keys, main,
    validate_e1_preflight,
)
from c1_rail.qualification.preflight import PreflightError, preflight_binding_bytes


NOW = datetime(2026, 9, 15, 20, tzinfo=timezone.utc)


def registry(private, authority="TEST_ONLY"):
    public = private.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    return canonical_json_bytes({
        "schema": "qualification_trusted_keys/v1",
        "keys": [{"authority_class": authority, "key_id": "operator",
                  "public_key_b64": base64.b64encode(public).decode(),
                  "revoked_at": None}],
    })


def test_production_registry_refuses_test_authority():
    private = Ed25519PrivateKey.generate()
    with pytest.raises(QualificationCLIError, match="TEST_ONLY"):
        load_trusted_approval_keys(registry(private))
    assert load_trusted_approval_keys(
        registry(private), allow_test_authority=True)["operator"].authority_class == "TEST_ONLY"


def test_preflight_atomically_reserves_new_output_root_and_binds_approval(tmp_path):
    import hashlib
    from signed_g5_fixture import build_signed_g5_fixture
    from composition_fixture import signed_approval
    fixture = build_signed_g5_fixture(tmp_path / 'artifacts')
    contract = fixture.contract
    private = fixture.private_keys['test-freeze']
    keys = fixture.trusted_keys
    def approval(private, subject_sha):
        assert hashlib.sha256(subject).hexdigest() == subject_sha
        return signed_approval(subject, private, key_id='test-freeze',
            scope='APPROVE_E1_EXACT_DEPTH', contract_sha256=contract.contract_sha256)
    subject = exact_depth_subject(contract, attempt_id="attempt-1")
    receipt = validate_e1_preflight(
        contract, attempt_id="attempt-1", output_root=tmp_path / "new-output",
        exact_depth_approval_bytes=approval(private, hashlib.sha256(subject).hexdigest()),
        trusted_keys=keys, now=NOW, trust_domain=fixture.domain)
    assert receipt.contract_sha256 == contract.contract_sha256
    assert (tmp_path / "new-output").is_dir()
    assert b'"exact_depth_approval_sha256"' in preflight_binding_bytes(receipt)

    occupied = tmp_path / "occupied"
    occupied.mkdir()
    (occupied / "retained.txt").write_text("preserve", encoding="utf-8")
    with pytest.raises(PreflightError, match="must be new"):
        validate_e1_preflight(
            contract, attempt_id="attempt-1", output_root=occupied,
            exact_depth_approval_bytes=approval(
                private, hashlib.sha256(subject).hexdigest()),
            trusted_keys=keys, now=NOW,
            trust_domain=fixture.domain)


def test_status_command_does_not_rotate_boot_or_append_events(tmp_path, capsys):
    path = tmp_path / "attempt.sqlite"
    store = AttemptStore.open(
        path, campaign_id="campaign", contract_digest="a" * 64,
        trust_domain_sha256="d" * 64,
        boot_id="boot-A", now=NOW)
    before = store.status()
    assert main(["status", str(path)]) == 0
    after = AttemptStore.inspect(path)["status"]
    assert before == after
    assert '"boot_id":"boot-A"' in capsys.readouterr().out
