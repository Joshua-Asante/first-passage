"""S6 G5-side result authentication and the metered result unit's driver.

``authenticate_campaign_result`` produces the result-key signature over the
canonical aggregate digest, the expected revision and the snapshot identity;
the signed candidate is staged privately (role ``result_authentication``) by
the driver below and is never returned as authority. Signature verification
against the current enrollment lives in :func:`verify_result_authentication`,
which the service re-runs between T1 and T2.
"""
from ..contract import canonical_json_bytes as encoded, parse_canonical_json
from . import campaign_result
from .protocol import decode_base64, fields, sha256


def _authentication_core(*, attempt_id, aggregate_sha256, campaign_revision, snapshot_sha256):
    return encoded(dict(schema=campaign_result.RESULT_AUTHENTICATION_SCHEMA,
                        attempt_id=attempt_id, aggregate_sha256=aggregate_sha256,
                        campaign_revision=campaign_revision, snapshot_sha256=snapshot_sha256))


def verify_result_authentication(raw, *, context, current_keys):
    """The enrollment-bound signature check (the service's between-T1/T2 gate)."""
    doc = campaign_result.ResultStore._parse_authentication(raw, attempt_id=context.attempt_id)
    signature = doc['signature']
    if signature['key_id'] not in context.domain.result_key_ids:
        raise ValueError('result authentication key is not enrolled for results')
    key = current_keys[signature['key_id']]
    if sha256(key.public_key) != context.domain.trusted_key_sha256[signature['key_id']]:
        raise ValueError('result authentication key identity differs')
    core = _authentication_core(attempt_id=context.attempt_id,
                                aggregate_sha256=doc['aggregate_sha256'],
                                campaign_revision=doc['campaign_revision'],
                                snapshot_sha256=doc['snapshot_sha256'])
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    Ed25519PublicKey.from_public_bytes(key.public_key).verify(
        decode_base64(signature['value_b64']), core)
    return doc


def _sign_authentication(core, key_id, key):
    import base64
    value = key.sign(core)
    return encoded(dict(parse_canonical_json(core, label='core'),
        signature=dict(algorithm='Ed25519', key_id=key_id,
                       value_b64=base64.b64encode(value).decode('ascii'))))


def authenticate_campaign_result(context, *, attestations, artifacts, assessment_receipts,
                                 snapshot_bytes, current_keys, credential_reference) -> bytes:
    """G5's result-key signature over the canonical aggregate (S6 §1).

    Validates the aggregate exactly as the service will (the same pure
    validator), then signs the fixed core with the enrolled result credential
    and self-checks the signature before returning the envelope for private
    staging. No publication path lives here.
    """
    from .credentials import load_credential
    validated = campaign_result.validate_campaign_result(
        context, validated_result_bytes_for(assessment_receipts, attestations, artifacts,
                                            snapshot_bytes, context),
        attestations=attestations, artifacts=artifacts,
        assessment_receipts=assessment_receipts, snapshot_bytes=snapshot_bytes,
        current_keys=current_keys)
    key_id, authority, key = load_credential(credential_reference)
    if (authority != context.domain.authority_class
            or key_id not in context.domain.result_key_ids or key_id not in current_keys
            or sha256(key.public_key().public_bytes_raw()) != sha256(current_keys[key_id].public_key)):
        raise ValueError('G5 result credential enrollment differs')
    core = _authentication_core(attempt_id=context.attempt_id,
                                aggregate_sha256=validated.aggregate_sha256,
                                campaign_revision=validated.expected_revision,
                                snapshot_sha256=validated.snapshot_sha256)
    raw = _sign_authentication(core, key_id, key)
    verify_result_authentication(raw, context=context, current_keys=current_keys)
    return raw


def validated_result_bytes_for(assessment_receipts, attestations, artifacts, snapshot_bytes, context):
    """The canonical aggregate bytes for the given custody rows (the driver and
    the service double both build the candidate this way before signing)."""
    rows = [campaign_result.parse_receipt_row(row) for row in assessment_receipts]
    return campaign_result.build_campaign_result(
        checkpoint_receipts=rows,
        cutoffs={row['checkpoint']: row['cutoff_bytes'] for row in rows},
        budget_digest=sha256(snapshot_bytes), release=context.installed_release,
        policy=context.policy)


def accept_campaign_result(socket_path, *, attempt_id, work_id):
    """The metered result unit's run: RESULT_SNAPSHOT, fetch actual custody
    members, validate, authenticate, stage privately, COMMIT_E1_RESULT."""
    import base64
    import os
    from pathlib import Path
    import tempfile
    from .admission import verify_bundle
    from .campaign_protocol import CHECKPOINT_CHUNK_LIMIT
    from .client import request
    from .files import read_regular, relative_parts
    from .g5 import utc_now
    from .keys import load_keys
    from .runtime import load_instance, installed_code_root
    config = fields(load_instance(installed_code_root() / 'qualification-installation/g5.json'),
                    {'installation_root', 'socket_path', 'g5_uid', 'scratch_root',
                     'result_credential'})
    if str(socket_path) != config['socket_path'] or os.geteuid() != config['g5_uid']:
        raise ValueError('protected G5 identity/socket differs')
    release = read_regular(Path(config['installation_root']), 'release.json',
                           limit=16 * 1024 * 1024)
    authority = parse_canonical_json(release, label='release')['authority_class']
    keys = load_keys(read_regular(Path(config['installation_root']), 'keys.json',
                                  limit=1024 * 1024), authority_class=authority)

    def call(operation, **values):
        return request(socket_path, operation, dict(attempt_id=attempt_id, **values))

    snapshot = call('RESULT_SNAPSHOT')
    parsed = campaign_result.parse_result_snapshot(snapshot, attempt_id=attempt_id)

    def fetch(digest_value):
        result = bytearray()
        total = None
        while total is None or len(result) < total:
            length = CHECKPOINT_CHUNK_LIMIT if total is None else min(
                CHECKPOINT_CHUNK_LIMIT, total - len(result))
            chunk_doc = parse_canonical_json(call('FETCH_CHECKPOINT_MEMBER',
                checkpoint='N1', object_sha256=digest_value, offset=len(result),
                length=length), label='member chunk')
            if (chunk_doc['schema'] != 'qualification_campaign_checkpoint_chunk/v1'
                    or chunk_doc['object_sha256'] != digest_value
                    or chunk_doc['offset'] != len(result)):
                raise ValueError('checkpoint chunk metadata differs')
            total = chunk_doc['total_byte_length']
            result.extend(decode_base64(chunk_doc['bytes_b64']))
        raw = bytes(result)
        if sha256(raw) != digest_value or len(raw) != total:
            raise ValueError('fetched checkpoint member identity differs')
        return raw

    with tempfile.TemporaryDirectory(dir=config['scratch_root']) as directory:
        root = Path(directory)
        # The retained bundle members reconstruct the same enrollment context
        # the service validated against (the N1 driver's pattern).
        members = {member['role']: member['sha256'] for member in
                   parse_canonical_json(call('CHECKPOINT_SNAPSHOT', checkpoint='N1'),
                                        label='checkpoint snapshot')['members']}
        index_raw = fetch(members['retained_bundle_index'])
        (root / 'index.json').write_bytes(index_raw)
        index = parse_canonical_json(index_raw, label='bundle index')
        for item in index['entries']:
            relative_parts(item['path'])
            path = root / item['path']
            path.parent.mkdir(parents=True, exist_ok=True)
            digest_value = next(members['retained_context_' + entry['role']]
                                for entry in index['entries'] if entry['role'] == item['role'])
            with path.open('xb') as output:
                output.write(fetch(digest_value))
        context = verify_bundle(root, release, keys, utc_now())
        if context.attempt_id != attempt_id:
            raise ValueError('campaign attempt identity differs')
        rows = []
        attestations = {}
        artifacts = {}
        for row in parsed['checkpoints']:
            custody = {name: row[name] for name in row}
            custody['attempt_id'] = attempt_id
            custody['campaign_id'] = parsed['campaign_id']
            custody['assessment_bytes'] = fetch(row['assessment_sha256'])
            custody['cutoff_bytes'] = fetch(row['cutoff_sha256'])
            custody['receipt_bytes'] = fetch(row['receipt_sha256'])
            rows.append(campaign_result.parse_receipt_row(custody))
            attestations[row['checkpoint']] = fetch(row['attestation_sha256'])
            artifacts[row['checkpoint']] = dict(result=fetch(row['result_sha256']),
                                                payload=fetch(row['payload_sha256']))
        validated = campaign_result.validate_campaign_result(
            context, validated_result_bytes_for(rows, attestations, artifacts, snapshot, context),
            attestations=attestations, artifacts=artifacts, assessment_receipts=rows,
            snapshot_bytes=snapshot, current_keys=keys)
        authentication = authenticate_campaign_result(
            context, attestations=attestations, artifacts=artifacts,
            assessment_receipts=rows, snapshot_bytes=snapshot, current_keys=keys,
            credential_reference=config['result_credential'])
        campaign_result.require_verified_result(validated)
        staged = parse_canonical_json(call('STAGE_CHECKPOINT_ARTIFACT', checkpoint='N1',
            role='result_authentication',
            bytes_b64=base64.b64encode(authentication).decode('ascii')),
            label='staged artifact receipt')
        if staged != {'artifact_sha256': sha256(authentication)}:
            raise ValueError('staged result authentication identity differs')
        proposed = dict(work_id=work_id,
            candidate_bytes_b64=base64.b64encode(validated.result_bytes).decode('ascii'),
            authentication_sha256=sha256(authentication),
            expected_revision=validated.expected_revision,
            artifacts=[dict(role='result_authentication', sha256=sha256(authentication))])
        return call('COMMIT_E1_RESULT', **proposed)
