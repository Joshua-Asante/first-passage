"""Public key registry decoding. Private signing material is never loaded here."""
from datetime import datetime

from ..contract import TrustedApprovalKey, parse_canonical_json
from .protocol import decode_base64, fields, identity


def load_keys(raw, *, authority_class):
    doc = fields(parse_canonical_json(raw, label='public key registry'), {'schema', 'keys'})
    if doc['schema'] != 'qualification_trusted_keys/v1' or type(doc['keys']) is not list:
        raise ValueError('public key registry schema differs')
    keys = {}
    for row in doc['keys']:
        fields(row, {'key_id', 'public_key_b64', 'authority_class', 'revoked_at'})
        key_id = identity(row['key_id'])
        if key_id in keys or row['authority_class'] != authority_class or authority_class not in ('OPERATOR', 'TEST_ONLY'):
            raise ValueError('duplicate key or mixed authority')
        revoked = row['revoked_at']
        if revoked is not None:
            if type(revoked) is not str or not revoked.endswith('Z'):
                raise ValueError('UTC revocation instant required')
            revoked = datetime.fromisoformat(revoked.replace('Z', '+00:00'))
        public = decode_base64(row['public_key_b64'])
        if len(public) != 32:
            raise ValueError('Ed25519 public key required')
        keys[key_id] = TrustedApprovalKey(key_id, public, authority_class, revoked)
    return keys
