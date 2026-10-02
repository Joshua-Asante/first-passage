"""The qseal process: the separate seal authority's signing body (S7, F4).

``sign_committed_pass`` lives only here: it independently re-parses the
committed result (outcome PASS, all five stage decisions PASS -- recomputed,
never caller-supplied), verifies the G5 result authentication and the service
receipt, verifies the intent binds exactly those digests plus the release
digest, intent id, seal key id and the fixed signing instant, and signs the
fixed payload with the seal credential from its own protected root. It has no
publication path: publication is the service store's T2 under the VOID lock.

``main`` is the ``seal`` entrypoint: a private bounded IPC listener (a Unix
socket owned by the seal principal, one request/response, 256 KiB frames,
RuntimeMaxUSec from the SEAL phase). The private SIGN_COMMITTED_PASS request
is not a campaign-protocol operation. No module-level mutable state.
"""
import base64
import os
import socket
import sys
from pathlib import Path

from ..contract import canonical_json_bytes as encoded, parse_canonical_json
from .campaign_result import ResultStore, parse_result_receipt
from .campaign_seal import parse_seal_intent, parse_seal_signature, seal_core
from .protocol import decode_base64, fields, sha256

FRAME_LIMIT = 262144
SEAL_REQUEST_SCHEMA = 'qualification_seal_request/v1'
SIGN_COMMITTED_PASS = 'SIGN_COMMITTED_PASS'


def _load_seal_credential(credential_root):
    """The Linux credential loader: the protected private key under the seal
    principal's own root (tests inject a loader through ``_loader``)."""
    from .credentials import load_credential
    return load_credential(credential_root)


def sign_committed_pass(intent_bytes, result_bytes, authentication_bytes, receipt_bytes,
                        *, credential_root, current_keys, _loader=None):
    """Sign the fixed seal payload -- only from the committed PASS result.

    Recomputes the PASS decision from the result bytes (a caller-supplied
    verdict is never accepted), verifies the G5 authentication's binding to
    the same aggregate and the service receipt's binding to both, checks the
    intent names exactly those digests plus the intent id, the seal key id and
    the fixed signing instant, then signs with the seal credential. Returns
    the seal document; never publishes.
    """
    intent = parse_seal_intent(intent_bytes, attempt_id=parse_canonical_json(
        intent_bytes, label='seal intent')['attempt_id'])
    attempt_id = intent['attempt_id']
    result = _require_committed_pass(result_bytes, attempt_id)
    _require_authentication(authentication_bytes, result_bytes, intent, attempt_id)
    _require_service_receipt(receipt_bytes, result_bytes, intent, attempt_id)
    if (intent['result_sha256'] != sha256(result_bytes)
            or intent['authentication_sha256'] != sha256(authentication_bytes)
            or intent['result_receipt_sha256'] != sha256(receipt_bytes)
            or intent['release_sha256'] != result['binding']['execution_release_sha256']):
        raise ValueError('seal intent binding differs')
    loader = _loader or _load_seal_credential
    key_id, authority, key = loader(credential_root)
    if key_id != intent['key_id']:
        raise ValueError('seal key is not enrolled for sealing')
    enrolled = current_keys.get(key_id)
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    public = key.public_key().public_bytes(serialization.Encoding.Raw,
                                           serialization.PublicFormat.Raw)
    if (authority != 'TEST_ONLY' or enrolled is None
            or sha256(public) != sha256(enrolled.public_key)):
        raise ValueError('seal key is not enrolled for sealing')
    if enrolled.revoked_at is not None:
        raise ValueError('seal key is revoked')
    core = seal_core(attempt_id, intent_id=intent['intent_id'],
                     result_sha256=intent['result_sha256'],
                     authentication_sha256=intent['authentication_sha256'],
                     result_receipt_sha256=intent['result_receipt_sha256'],
                     release_sha256=intent['release_sha256'],
                     domain_sha256=intent['domain_sha256'],
                     signed_at_utc=intent['signing_at_utc'])
    value = key.sign(core)
    raw = encoded(dict(parse_canonical_json(core, label='seal core'),
        signature=dict(algorithm='Ed25519', key_id=key_id,
                       value_b64=base64.b64encode(value).decode('ascii'))))
    parse_seal_signature(raw, attempt_id=attempt_id)
    Ed25519PublicKey.from_public_bytes(public).verify(value, core)
    return raw


def _require_committed_pass(result_bytes, attempt_id):
    from .campaign_result import parse_campaign_result
    result = parse_campaign_result(result_bytes, attempt_id=attempt_id)
    if result['outcome'] != 'PASS':
        raise ValueError('committed PASS result required')
    if any(row['status'] != 'PASS' for row in result['stages']):
        raise ValueError('committed PASS result required')
    return result


def _require_authentication(authentication_bytes, result_bytes, intent, attempt_id):
    authentication = ResultStore._parse_authentication(authentication_bytes,
                                                        attempt_id=attempt_id)
    if authentication['aggregate_sha256'] != sha256(result_bytes):
        raise ValueError('result authentication binding differs')


def _require_service_receipt(receipt_bytes, result_bytes, intent, attempt_id):
    receipt = parse_result_receipt(receipt_bytes, attempt_id=attempt_id)
    if (receipt['aggregate_sha256'] != sha256(result_bytes)
            or receipt['outcome'] != 'PASS'
            or receipt['campaign_state'] != 'RESULT_COMMITTED_PASS'):
        raise ValueError('service receipt binding differs')


def exchange(service, intent_bytes, result_bytes, authentication_bytes, receipt_bytes):
    """The service-side IPC transport to the qseal listener (Linux). The
    socket path and the SEAL phase bounds come from the installed instance;
    the request is one bounded frame, so is the response."""
    raise ValueError('qseal IPC requires the installed seal principal (Linux)')


def main():
    """The ``seal`` entrypoint: bind the private socket, serve one bounded
    SIGN_COMMITTED_PASS request, exit (RuntimeMaxUSec bounds the unit)."""
    from .keys import load_keys
    from .files import read_regular
    from .runtime import load_instance, installed_code_root
    config = fields(load_instance(installed_code_root() / 'qualification-installation/seal.json'),
                    {'installation_root', 'socket_path', 'seal_uid', 'credential_root'})
    if os.geteuid() != config['seal_uid']:
        raise SystemExit('protected seal identity differs')
    socket_path = Path(config['socket_path'])
    if socket_path.exists():
        socket_path.unlink()
    release = read_regular(Path(config['installation_root']), 'release.json',
                           limit=16 * 1024 * 1024)
    authority = parse_canonical_json(release, label='release')['authority_class']
    keys = load_keys(read_regular(Path(config['installation_root']), 'keys.json',
                                  limit=1024 * 1024), authority_class=authority)
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as listener:
        listener.bind(str(socket_path))
        os.chmod(socket_path, 0o600)
        listener.listen(1)
        connection, _ = listener.accept()
        with connection:
            frame = connection.recv(FRAME_LIMIT)
            if len(frame) >= FRAME_LIMIT:
                raise SystemExit('seal request exceeds frame bound')
            response = _serve(frame, config, keys)
            connection.sendall(response)


def _serve(frame, config, keys):
    document = parse_canonical_json(frame, label='seal request')
    fields(document, {'schema', 'operation', 'intent_b64', 'result_b64',
                      'authentication_b64', 'receipt_b64'})
    if (document['schema'] != SEAL_REQUEST_SCHEMA
            or document['operation'] != SIGN_COMMITTED_PASS):
        raise ValueError('private seal operation differs')
    signature = sign_committed_pass(
        decode_base64(document['intent_b64']), decode_base64(document['result_b64']),
        decode_base64(document['authentication_b64']), decode_base64(document['receipt_b64']),
        credential_root=config['credential_root'], current_keys=keys)
    return encoded(dict(ok=True, signature_b64=base64.b64encode(signature).decode('ascii')))


if __name__ == '__main__':
    main()
