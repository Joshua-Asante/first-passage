"""External records must bind registry slot, enrolled key identity and bytes."""
import base64
from dataclasses import replace
import hashlib

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

from c1_rail.qualification.contract import TrustedApprovalKey, canonical_json_bytes
from c1_rail.qualification.seal import (
    AUTH_SCHEMA, SEAL_SCHEMA, ResultValidationError, TrustedResultKey,
    _verify_external_record,
)
from test_trust_domain import NOW, case, validate


@pytest.mark.parametrize('scope,schema,enrolled,other', [
    ('ATTEST_E1_RESULT', AUTH_SCHEMA, 'producer', 'seal'),
    ('SEAL_E1_PASS', SEAL_SCHEMA, 'seal', 'producer'),
])
def test_external_record_registry_slot_cannot_borrow_another_enrolled_role_key(
        scope, schema, enrolled, other):
    doc, policy, freeze, keys = case()
    private = {name: Ed25519PrivateKey.generate() for name in ('producer', 'seal')}
    for name, signer in private.items():
        raw = signer.public_key().public_bytes(
            serialization.Encoding.Raw, serialization.PublicFormat.Raw)
        keys[name] = TrustedApprovalKey(name, raw, 'TEST_ONLY')
    doc.update(result_key_ids=['producer'], seal_key_ids=['seal'],
               trusted_key_sha256={name: hashlib.sha256(key.public_key).hexdigest()
                                   for name, key in keys.items()})
    domain = validate(doc, policy, freeze, keys)
    payload = dict(scope=scope, subject_sha256='a'*64, contract_sha256='b'*64,
                   trust_domain_sha256=domain.sha256, attempt_id='synthetic-attempt',
                   issued_utc='2026-09-15T19:00:00Z', expires_utc='2026-09-16T19:00:00Z')

    def signed(signer):
        return canonical_json_bytes(dict(schema=schema, payload=payload,
            signature=dict(algorithm='Ed25519', key_id=enrolled,
                value_b64=base64.b64encode(signer.sign(canonical_json_bytes(payload))).decode())))

    key = TrustedResultKey(enrolled, keys[enrolled].public_key, 'TEST_ONLY', (scope,))
    arguments = dict(schema=schema, scope=scope, subject_sha256='a'*64,
                     contract_sha256='b'*64, attempt_id='synthetic-attempt',
                     now=NOW, trust_domain=domain, enrolled_key_ids=(enrolled,))
    assert _verify_external_record(signed(private[enrolled]),
        trusted_keys={enrolled: key}, **arguments) == enrolled
    substituted = replace(key, key_id=other, public_key=keys[other].public_key)
    with pytest.raises(ResultValidationError, match='key'):
        _verify_external_record(signed(private[other]),
            trusted_keys={enrolled: substituted}, **arguments)
