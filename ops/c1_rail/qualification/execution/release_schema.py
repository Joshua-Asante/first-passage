"""Closed release values; signature and installed-byte verification are separate."""

from pathlib import PurePosixPath
import re

from ..contract import canonical_json_bytes, parse_canonical_json
from .profile import parse_profile
from .protocol import fields, digest, identity, sha256

PORT_ROLES = (
    'aegis_runtime_port',
    'orb_runtime_port',
    'striker_runtime_port',
    'vanguard_runtime_port',
)
DIAGNOSTIC_RELEASE = 'qualification_execution_release/v3'
# The only revision whose installation opens the funded private scheduler
# route: execution profile/v4 + budget profile/v3 + full snapshot/v5. It keeps
# every v3 restriction: FULL_E1, TEST_ONLY, probes only, no statistical dispatch.
EXECUTABLE_DIAGNOSTIC_RELEASE = 'qualification_execution_release/v4'
# D4: the S3 dispatch revision -- profile/v5 + budget profile/v3 -- the only one
# whose dispatch_enabled may be True, and only for the closed N1 checkpoint set
# named by dispatch_checkpoints. v3/v4 keep refusing every dispatch.
DISPATCH_DIAGNOSTIC_RELEASE = 'qualification_execution_release/v5'
PROCESS_ROLES = ('supervisor', 'worker', 'g5')
KEY_ROLES = ('freeze', 'result', 'seal', 'execution')
WORKER_ENTRYPOINT = ('/opt/ops/bin/python', '-I', '/opt/qualification/bootstrap.py', 'worker')


def _source_path(value):
    if (
        type(value) is not str
        or not value
        or '\\' in value
        or ':' in value
        or PurePosixPath(value).is_absolute()
        or str(PurePosixPath(value)) != value
        or any(part in ('', '..', '.') for part in value.split('/'))
    ):
        raise ValueError('canonical relative source path required')


def parse_release(raw):
    doc = parse_canonical_json(raw, label='execution release')
    if type(doc) is not dict:
        raise ValueError('closed schema object required')
    executable = doc.get('schema') == EXECUTABLE_DIAGNOSTIC_RELEASE
    dispatching = doc.get('schema') == DISPATCH_DIAGNOSTIC_RELEASE
    diagnostic = executable or dispatching or doc.get('schema') == DIAGNOSTIC_RELEASE
    campaign = diagnostic or doc.get('schema') == 'qualification_execution_release/v2'
    fields(
        doc,
        {
            'schema',
            'release_id',
            'profile',
            'profile_sha256',
            'authority_class',
            'service_id',
            'capability',
            'production_execution',
            'worker_image_digest',
            'runtime_manifests',
            'ordinary_code',
            'worker_entrypoint',
            'port_roles',
            'key_roles',
            'trusted_key_sha256',
            'qualification_policy_sha256',
            'source_owner_sha256',
        }
        | ({'dispatch_enabled'} if campaign else set())
        | ({'dispatch_checkpoints'} if dispatching else set())
        | ({'campaign_budget_profile'} if diagnostic else set()),
    )
    if campaign:
        if (
            doc['capability'] != 'FULL_E1'
            or doc['authority_class'] != 'TEST_ONLY'
            or doc['production_execution'] is not False
        ):
            raise ValueError('unsupported admission-only campaign release')
        if dispatching:
            # The closed D4 fact pair: dispatch only N1, only on this revision.
            if doc['dispatch_enabled'] is not True or doc['dispatch_checkpoints'] != ['N1']:
                raise ValueError('dispatch release must enable exactly the N1 checkpoint')
        elif doc['dispatch_enabled'] is not False:
            raise ValueError('unsupported admission-only campaign release')
    elif (
        doc['schema'] != 'qualification_execution_release/v1'
        or doc['authority_class'] not in ('TEST_ONLY', 'OPERATOR')
        or doc['capability'] != 'N1_ONLY'
        or doc['production_execution'] is not False
    ):
        raise ValueError('unsupported execution release')
    identity(doc['release_id'])
    identity(doc['service_id'])
    digest(doc['qualification_policy_sha256'])
    owners = fields(doc['source_owner_sha256'], {'book_policy', 'firm_rules', 'policy_fingerprint'})
    for value in owners.values():
        digest(value)
    profile = parse_profile(canonical_json_bytes(doc['profile']))
    if profile.values['schema'] in (
        'qualification_execution_profile/v4',
        'qualification_execution_profile/v5',
    ) and not (executable or dispatching):
        raise ValueError('funding profile is persistence-only; runtime release not enabled')
    if diagnostic:
        from .profile import parse_campaign_budget_profile

        budget_profile = parse_campaign_budget_profile(
            canonical_json_bytes(doc['campaign_budget_profile'])
        )
        expected = (
            ('qualification_execution_profile/v4', 'qualification_campaign_budget_profile/v3')
            if executable
            else (
                ('qualification_execution_profile/v5', 'qualification_campaign_budget_profile/v3')
                if dispatching
                else (
                    'qualification_execution_profile/v3',
                    'qualification_campaign_budget_profile/v2',
                )
            )
        )
        if (profile.values['schema'], budget_profile['schema']) != expected or budget_profile[
            'installed_profile_sha256'
        ] != profile.sha256:
            raise ValueError('diagnostic installed budget/profile binding differs')
    elif profile.values['schema'] == 'qualification_execution_profile/v3':
        raise ValueError('diagnostic profile requires release v3')
    if profile.capability != doc['capability']:
        raise ValueError('release profile capability differs')
    if digest(doc['profile_sha256']) != profile.sha256:
        raise ValueError('execution profile identity differs')
    if (
        type(doc['worker_image_digest']) is not str
        or re.fullmatch('sha256:[0-9a-f]{64}', doc['worker_image_digest']) is None
    ):
        raise ValueError('immutable worker image identity required')
    if doc['worker_entrypoint'] != list(WORKER_ENTRYPOINT) or doc['port_roles'] != list(PORT_ROLES):
        raise ValueError('fixed entrypoint and four port roles required')
    roles = fields(doc['key_roles'], KEY_ROLES)
    enrolled = set()
    for names in roles.values():
        if (
            type(names) is not list
            or not names
            or any(type(name) is not str for name in names)
            or names != sorted(set(names))
        ):
            raise ValueError('sorted nonempty signing role required')
        for name in names:
            identity(name)
        if enrolled.intersection(names):
            raise ValueError('signing role ID separation required')
        enrolled.update(names)
    fingerprints = fields(doc['trusted_key_sha256'], enrolled)
    for value in fingerprints.values():
        digest(value)
    seen = set()
    for names in roles.values():
        current = {fingerprints[name] for name in names}
        if seen.intersection(current):
            raise ValueError('signing public key separation required')
        seen.update(current)
    ordinary = doc['ordinary_code']
    if type(ordinary) is not dict or not ordinary:
        raise ValueError('ordinary source inventory required')
    by_name, paths = {}, set()
    for role, row in ordinary.items():
        identity(role)
        fields(row, {'module', 'path', 'sha256'})
        name = row['module']
        if (
            type(name) is not str
            or not all(part.isidentifier() for part in name.split('.'))
            or name.startswith(('ops.', 'core.', 'fp_qualification_port_'))
        ):
            raise ValueError('canonical ordinary source module required')
        _source_path(row['path'])
        digest(row['sha256'])
        if name in by_name or row['path'] in paths:
            raise ValueError('source inventory alias forbidden')
        by_name[name] = {'path': row['path'], 'sha256': row['sha256']}
        paths.add(row['path'])
    runtimes = fields(doc['runtime_manifests'], PROCESS_ROLES)
    covered = set()
    for runtime in runtimes.values():
        fields(
            runtime,
            {
                'python_version',
                'platform',
                'dependency_lock_sha256',
                'signing_configuration_sha256',
                'sources',
            },
        )
        if (
            type(runtime['python_version']) is not str
            or re.fullmatch(r'3\.\d+\.\d+', runtime['python_version']) is None
        ):
            raise ValueError('exact Python patch version required')
        if runtime['platform'] not in ('linux', 'win32'):
            raise ValueError('observed platform required')
        digest(runtime['dependency_lock_sha256'])
        digest(runtime['signing_configuration_sha256'])
        if type(runtime['sources']) is not dict or not runtime['sources']:
            raise ValueError('runtime source closure required')
        for name, row in runtime['sources'].items():
            if by_name.get(name) != row:
                raise ValueError('runtime source differs from inventory')
        covered.update(runtime['sources'])
    if covered != set(by_name):
        raise ValueError('ordinary source absent from process closures')
    return doc
