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


def verify_checkpoint_attestation(raw, *, context, current_keys):
    """Verify the campaign checkpoint attestation's execution-key signature."""
    from .campaign_store import parse_checkpoint_attestation
    from .protocol import decode_base64
    doc = parse_checkpoint_attestation(raw, attempt_id=context.attempt_id)
    signature = doc['signature']
    if signature['key_id'] not in context.domain.execution_key_ids:
        raise ValueError('checkpoint attestation key is not enrolled for execution')
    key = current_keys[signature['key_id']]
    if sha256(key.public_key) != context.domain.trusted_key_sha256[signature['key_id']]:
        raise ValueError('checkpoint attestation key identity differs')
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    Ed25519PublicKey.from_public_bytes(key.public_key).verify(
        decode_base64(signature['value_b64']), encoded(doc['payload']))
    return doc


def sign_checkpoint_attestation(payload, *, context, credential_reference, current_keys):
    """Attest exactly the archived checkpoint bytes with the execution credential."""
    key_id, authority, key = load_credential(credential_reference)
    if (authority != context.domain.authority_class or key_id not in context.domain.execution_key_ids
            or key_id not in current_keys
            or sha256(key.public_key().public_bytes_raw()) != sha256(current_keys[key_id].public_key)):
        raise ValueError('campaign checkpoint credential enrollment differs')
    import base64
    raw = encoded(dict(schema='qualification_campaign_checkpoint_attestation/v1', payload=payload,
        signature=dict(algorithm='Ed25519', key_id=key_id,
                       value_b64=base64.b64encode(key.sign(encoded(payload))).decode('ascii'))))
    verify_checkpoint_attestation(raw, context=context, current_keys=current_keys)
    return raw


def verify_checkpoint_assessment(raw, *, context, current_keys):
    """Verify the G5 candidate's result-key signature over the assessment core."""
    from .campaign_store import parse_checkpoint_assessment
    from .protocol import decode_base64, fields
    doc = parse_checkpoint_assessment(raw, attempt_id=context.attempt_id)
    signature = fields(doc['signature'], {'algorithm', 'key_id', 'value_b64'})
    if signature['key_id'] not in context.domain.result_key_ids:
        raise ValueError('checkpoint assessment key is not enrolled for results')
    key = current_keys[signature['key_id']]
    if sha256(key.public_key) != context.domain.trusted_key_sha256[signature['key_id']]:
        raise ValueError('checkpoint assessment key identity differs')
    core = {name: value for name, value in doc.items() if name != 'signature'}
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    Ed25519PublicKey.from_public_bytes(key.public_key).verify(
        decode_base64(signature['value_b64']), encoded(core))
    return doc
