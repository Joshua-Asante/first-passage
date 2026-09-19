"""Verify retained policy bytes without executing retained source.

Release signature validation is only one admission step. Trusted entry points
must also measure their installed code/runtime before serving or computing.
"""
from dataclasses import dataclass
import json
from pathlib import Path
import re
from types import MappingProxyType

from c1_rail.ed25519_verify import is_strong_public_key
from ..contract import (ObservedBindings, canonical_json_bytes, parse_canonical_json,
                        validate_frozen_contract, verify_detached_approval)
from ..preflight import exact_depth_subject
from ..trust_domain import (PRODUCTION_TRUST_POLICY, PortRuntimePin, QualificationWorkloadPolicy,
    _composition_test_trust_policy, validate_qualification_trust_domain)
from .files import read_regular, relative_parts
from .profile import parse_profile
from .protocol import digest, fields, identity, sha256
from .release_schema import parse_release, PORT_ROLES, WORKER_ENTRYPOINT, PROCESS_ROLES, KEY_ROLES
from ..policy import parse_policy
from ..policy_sources import build_qualification_policy
from ..legality import geometry_role, verify_static_legality



@dataclass(frozen=True)
class ExecutionRelease:
    canonical_bytes: bytes

    @property
    def document(self):
        return parse_canonical_json(self.canonical_bytes, label='execution release')

    @property
    def sha256(self):
        return sha256(self.canonical_bytes)

    @property
    def profile(self):
        return parse_profile(canonical_json_bytes(self.document['profile']))

    def runtime_sha256(self, role):
        return sha256(canonical_json_bytes(self.document['runtime_manifests'][role]))


def verify_release(raw: bytes, approval_bytes: bytes, trusted_keys: dict, *, now,
                   installation_authority: str) -> ExecutionRelease:
    doc = parse_release(raw)
    if installation_authority not in ('TEST_ONLY', 'OPERATOR') or doc['authority_class'] != installation_authority:
        raise ValueError('execution release installation authority differs')
    expected_policy = parse_policy(build_qualification_policy())
    if (doc['qualification_policy_sha256'] != expected_policy.sha256
            or doc['source_owner_sha256'] != json.loads(expected_policy.canonical_bytes)['source_owner_sha256']):
        raise ValueError('POLICY_IDENTITY_MISMATCH')
    for key_id, fingerprint in doc['trusted_key_sha256'].items():
        key = trusted_keys.get(key_id)
        if key is None or key.key_id != key_id or key.authority_class != installation_authority:
            raise ValueError('release key authority or identity differs')
        if not is_strong_public_key(key.public_key) or (key.revoked_at is not None and key.revoked_at <= now):
            raise ValueError('release key is invalid or revoked')
        if sha256(key.public_key) != fingerprint:
            raise ValueError('release actual public key differs')
    approval = verify_detached_approval(approval_bytes, trusted_keys=trusted_keys,
        expected_scope='APPROVE_EXECUTION_RELEASE',expected_subject_sha256=sha256(raw),
        expected_contract_sha256=sha256(raw),now=now,allow_test_authority=installation_authority=='TEST_ONLY')
    if approval.key_id not in doc['key_roles']['freeze'] or approval.authority_class != installation_authority:
        raise ValueError('release approver is not an enrolled freeze authority')
    return ExecutionRelease(raw)

@dataclass(frozen=True)
class ExecutionContext:
    contract: object
    domain: object
    release: ExecutionRelease
    retained_bundle_index: bytes
    retained_bytes: object
    bundle_dir: Path
    attempt_id: str
    exact_depth_approval: object
    policy: object

    @property
    def profile(self):
        return self.release.profile

    @property
    def installed_release(self):
        return self.release.canonical_bytes

    @property
    def bundle_sha256(self):
        return sha256(self.retained_bundle_index)


_CONTEXT_ROLES = {'contract', 'trust_domain', 'freeze_approval', 'domain_approval',
                  'release_approval', 'exact_depth_approval'}


def verify_bundle(bundle_dir: Path, installed_release: bytes, trusted_keys: dict, now) -> ExecutionContext:
    """Reconstruct context from original staged bytes; never import retained ports."""
    root = Path(bundle_dir)
    return _verify_bundle(root, installed_release, trusted_keys, now,
        lambda path, limit: read_regular(root, path, limit=limit))


def verify_retained_bundle(index_raw, retained, installed_release, trusted_keys, now):
    index = fields(parse_canonical_json(index_raw, label='retained index'), {'schema', 'attempt_id', 'entries'})
    by_path = {'index.json': index_raw}
    for row in index['entries']:
        fields(row, {'role', 'path', 'sha256', 'byte_length'})
        relative_parts(row['path'])
        if row['path'] in by_path or row['role'] not in retained:
            raise ValueError('retained inventory differs')
        by_path[row['path']] = retained[row['role']]
    if set(retained) != {row['role'] for row in index['entries']}:
        raise ValueError('retained inventory differs')
    def read(path, limit):
        raw = by_path[path]
        if type(raw) is not bytes or len(raw) > limit:
            raise ValueError('retained bytes exceed bound')
        return raw
    return _verify_bundle(Path('.'), installed_release, trusted_keys, now, read)


def _verify_bundle(root, installed_release, trusted_keys, now, read):
    installed = parse_canonical_json(installed_release, label='installed release')
    profile = parse_profile(canonical_json_bytes(installed['profile']))
    index_raw = read('index.json', profile.input_byte_limit)
    index = fields(parse_canonical_json(index_raw, label='retained bundle index'), {'schema', 'attempt_id', 'entries'})
    if index['schema'] != 'qualification_retained_bundle/v1':
        raise ValueError('retained bundle schema differs')
    identity(index['attempt_id'])
    entries = index['entries']
    if type(entries) is not list or not entries:
        raise ValueError('closed retained inventory required')
    by_role, paths, total, retained = {}, set(), len(index_raw), {}
    for entry in entries:
        fields(entry, {'role', 'path', 'sha256', 'byte_length'})
        identity(entry['role']); relative_parts(entry['path']); digest(entry['sha256'])
        if entry['role'] in by_role or entry['path'] in paths or entry['path'] == 'index.json':
            raise ValueError('duplicate retained role/path')
        if type(entry['byte_length']) is not int or entry['byte_length'] < 0:
            raise ValueError('retained byte length required')
        total += entry['byte_length']
        if total > profile.input_byte_limit:
            raise ValueError('retained bundle byte limit exceeded')
        raw = read(entry['path'], max(1, entry['byte_length']))
        if len(raw) != entry['byte_length'] or sha256(raw) != entry['sha256']:
            raise ValueError('retained artifact identity or length differs')
        by_role[entry['role']] = entry
        paths.add(entry['path'])
        retained[entry['role']] = raw
    if list(by_role) != sorted(by_role) or not (_CONTEXT_ROLES | {'execution_release'}) <= set(by_role):
        raise ValueError('sorted complete retained context required')
    if retained['execution_release'] != installed_release:
        raise ValueError('bundle differs from installed release')
    release = verify_release(installed_release, retained['release_approval'], trusted_keys, now=now,
                             installation_authority=installed['authority_class'])
    domain_doc = parse_canonical_json(retained['trust_domain'], label='domain')
    if domain_doc.get('schema') != 'qualification_trust_domain/v2':
        raise ValueError('EXECUTION_ATTESTATION_REQUIRED: v2 domain required')
    if release.document['authority_class'] == 'TEST_ONLY':
        policy = _composition_test_trust_policy(
            accepted_historical_pins=domain_doc['accepted_historical_pins'],
            required_artifact_roles=domain_doc['required_artifact_roles'], runtime_code_roles=domain_doc['runtime_code_roles'],
            port_runtime_pins={leg: PortRuntimePin(**values) for leg, values in domain_doc['port_runtime_pins'].items()},
            effective_settings_sha256=domain_doc['effective_settings_sha256'],
            workload_policy=QualificationWorkloadPolicy(**domain_doc['workload_policy']))
    else:
        policy = PRODUCTION_TRUST_POLICY
    domain = validate_qualification_trust_domain(retained['trust_domain'], retained['domain_approval'],
                                                  trusted_keys, policy=policy, now=now)
    release_doc = release.document
    if domain.execution_service_id != release_doc['service_id'] or domain.execution_release_sha256 != release.sha256:
        raise ValueError('domain service/release identity differs')
    for role in KEY_ROLES:
        if list(getattr(domain, role + '_key_ids')) != release_doc['key_roles'][role]:
            raise ValueError('domain role enrollment differs from installed release')
    if dict(domain.trusted_key_sha256) != release_doc['trusted_key_sha256']:
        raise ValueError('domain public key registry differs from installed release')
    artifact_roles = set(by_role) - _CONTEXT_ROLES
    if artifact_roles != set(domain.required_artifact_roles):
        raise ValueError('retained artifact inventory differs from signed domain')
    observed = ObservedBindings(
        {by_role[role]['path']: by_role[role]['sha256'] for role in artifact_roles},
        {role: by_role[role]['sha256'] for role in artifact_roles},
        sha256(retained['effective_settings_successor']),
        json.loads(retained['effective_settings_successor'])['orb_mnq_v7']['adapter']['qty'])
    semantic_policy = parse_policy(retained['qualification_policy'])
    if (semantic_policy.sha256 != release_doc['qualification_policy_sha256']
            or semantic_policy.canonical_bytes != build_qualification_policy()):
        raise ValueError('POLICY_IDENTITY_MISMATCH')
    contract = validate_frozen_contract(retained['contract'], retained['freeze_approval'], trusted_keys,
        observed, now=now, trust_domain=domain,qualification_policy_bytes=semantic_policy.canonical_bytes)
    geometry = geometry_role(domain.runtime_code_roles)
    verify_static_legality(contract_sha256=contract.contract_sha256,domain_sha256=domain.sha256,
        policy=semantic_policy,geometry_bytes=retained[geometry],expected_geometry_sha256=by_role[geometry]['sha256'])
    ordinary_roles = set(domain.runtime_code_roles) - set(PORT_ROLES)
    if ordinary_roles != set(release_doc['ordinary_code']):
        raise ValueError('ordinary code inventory differs from approved release')
    for role, source in release_doc['ordinary_code'].items():
        entry = by_role[role]
        if (domain.runtime_code_roles[role] != source['module'] or entry['path'] != source['path']
                or entry['sha256'] != source['sha256']):
            raise ValueError('ordinary code identity differs from approved release')
    approval = verify_detached_approval(retained['exact_depth_approval'], trusted_keys=trusted_keys,
        expected_scope='APPROVE_E1_EXACT_DEPTH',
        expected_subject_sha256=sha256(exact_depth_subject(contract, attempt_id=index['attempt_id'])),
        expected_contract_sha256=contract.contract_sha256, now=now,
        allow_test_authority=domain.authority_class == 'TEST_ONLY')
    if approval.key_id not in domain.freeze_key_ids or approval.authority_class != domain.authority_class:
        raise ValueError('exact-depth approver not enrolled')
    return ExecutionContext(contract, domain, release, index_raw, MappingProxyType(retained), root,
                            index['attempt_id'], approval, semantic_policy)
