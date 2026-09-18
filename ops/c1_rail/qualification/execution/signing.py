"""Execution signer: only durable captured journal payloads can be signed."""
import base64
from datetime import datetime, timezone

from ..contract import canonical_json_bytes as encoded, parse_canonical_json
from .credentials import load_credential
from .protocol import sha256
from .verification import verify_execution


def sign_captured(execution_id, *, store, credential_reference):
    with store.transaction() as connection:
        row = store._row(connection, execution_id)
        if row['state'] != 'CAPTURED' or row['validity'] != 'VALID':
            raise ValueError('VALID durable CAPTURED execution required')
        revision = row['revision']
        context, keys = store.context(execution_id, now=datetime.now(timezone.utc))
        payload_bytes = store.get_captured_payload(execution_id)
        payload = parse_canonical_json(payload_bytes, label='durable capture')
        artifacts = {item['sha256']: store.fetch(row['attempt_id'], item['sha256']) for item in payload['artifacts']}
    key_id, authority, key = load_credential(credential_reference)
    if (authority != context.domain.authority_class or key_id not in context.domain.execution_key_ids
            or key_id not in keys or sha256(key.public_key().public_bytes_raw()) != sha256(keys[key_id].public_key)):
        raise ValueError('execution credential enrollment differs')
    raw = encoded(dict(schema='qualification_execution_attestation/v1', payload=payload,
        signature=dict(algorithm='Ed25519', key_id=key_id,
                       value_b64=base64.b64encode(key.sign(payload_bytes)).decode('ascii'))))
    verify_execution(raw, artifacts, context=context, expected_attempt_id=row['attempt_id'], current_keys=keys)
    with store.transaction():
        # Current authority and validity are checked again after signing. A VOID
        # committed while signing cannot publish this envelope.
        context, keys = store.context(execution_id, now=datetime.now(timezone.utc))
        verify_execution(raw, artifacts, context=context, expected_attempt_id=row['attempt_id'], current_keys=keys)
        store.publish_attestation(execution_id, raw, expected_revision=revision)
    return raw
