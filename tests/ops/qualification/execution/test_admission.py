"""Installed release identity and authority cannot be supplied by a request."""
import importlib
import json
from dataclasses import replace

import pytest
from c1_rail.qualification.contract import canonical_json_bytes
from composition_fixture import signed_approval, digest
from test_trust_domain import NOW
from test_domain import v2_case
from test_profile import document


@pytest.fixture
def release_case():
    from c1_rail.qualification.policy_sources import build_qualification_policy
    policy_bytes = build_qualification_policy()
    domain, _, private, keys = v2_case()
    profile = document()
    roles = {role: domain[role + '_key_ids'] for role in ('freeze', 'result', 'seal', 'execution')}
    runtime = {'python_version': '3.13.2', 'platform': 'win32', 'dependency_lock_sha256': 'b' * 64, 'signing_configuration_sha256': 'c' * 64,
               'sources': {'c1_rail.qualification.execution.protocol': {
                   'path': 'ops/c1_rail/qualification/execution/protocol.py', 'sha256': 'c' * 64}}}
    doc = dict(schema='qualification_execution_release/v1', release_id='test-release',
        qualification_policy_sha256=digest(policy_bytes),source_owner_sha256=json.loads(policy_bytes)['source_owner_sha256'],
        profile=profile, profile_sha256=digest(canonical_json_bytes(profile)),
        authority_class='TEST_ONLY', service_id='fixture-service', capability='N1_ONLY',
        production_execution=False, worker_image_digest='sha256:' + 'd' * 64,
        runtime_manifests={role: runtime for role in ('supervisor', 'worker', 'g5')},
        ordinary_code={'protocol': {'module': 'c1_rail.qualification.execution.protocol',
            'path': 'ops/c1_rail/qualification/execution/protocol.py', 'sha256': 'c' * 64}},
        worker_entrypoint=['/opt/ops/bin/python', '-I', '/opt/qualification/bootstrap.py', 'worker'],
        port_roles=['aegis_runtime_port', 'orb_runtime_port', 'striker_runtime_port', 'vanguard_runtime_port'],
        key_roles=roles, trusted_key_sha256=dict(domain['trusted_key_sha256']))
    return doc, private, keys


def verify(values, **kwargs):
    doc, private, keys = values
    raw = canonical_json_bytes(doc)
    approval = signed_approval(raw, private, key_id='test', scope='APPROVE_EXECUTION_RELEASE')
    module = importlib.import_module('c1_rail.qualification.execution.admission')
    return module.verify_release(raw, approval, keys, now=NOW, **kwargs)


def test_release_signature_binds_resolved_profile_image_and_authorities(release_case):
    release = verify(release_case, installation_authority='TEST_ONLY')
    assert release.profile.worker_uid == 65532
    assert release.sha256 == digest(canonical_json_bytes(release_case[0]))


def test_test_release_cannot_install_into_operator_service(release_case):
    with pytest.raises(ValueError, match='authority'):
        verify(release_case, installation_authority='OPERATOR')


@pytest.mark.parametrize('mutation', [
    lambda d: d.update(production_execution=True),
    lambda d: d.update(worker_image_digest='latest'),
    lambda d: d.update(profile_sha256='f' * 64),
    lambda d: d['profile'].update(network='host'),
    lambda d: d.update(worker_entrypoint=['sh']),
    lambda d: d.update(port_roles=[]),
    lambda d: d['runtime_manifests'].pop('g5'),
    lambda d: d.update(extra=True),
])
def test_release_rejects_unapproved_execution_configuration(release_case, mutation):
    mutation(release_case[0])
    with pytest.raises(ValueError):
        verify(release_case, installation_authority='TEST_ONLY')


def test_release_key_aliases_rejected_even_when_domain_ids_differ(release_case):
    doc, _, keys = release_case
    keys['execution'] = replace(keys['result'], key_id='execution')
    doc['trusted_key_sha256']['execution'] = doc['trusted_key_sha256']['result']
    with pytest.raises(ValueError, match='separation'):
        verify(release_case, installation_authority='TEST_ONLY')
