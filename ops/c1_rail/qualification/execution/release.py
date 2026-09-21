"""Administrator-only installation and immutable retained-byte staging."""
from datetime import datetime, timezone
import os
from pathlib import Path, PurePosixPath
import stat
import sys

from ..contract import canonical_json_bytes as encoded, parse_canonical_json
from .admission import verify_bundle, verify_release
from .files import fsync_directory, read_regular
from .keys import load_keys
from .protocol import fields, sha256
from .runtime import observe_runtime, protected_path, installed_code_root
from tools.qualification_verification.container_ownership import host_identity

INSTANCE_FIELDS = {'schema', 'authority_class', 'installation_root', 'data_root', 'daemon_data_root',
    'socket_path', 'socket_gid', 'client_uid', 'service_uid', 'g5_uid', 'operator_uid', 'execution_credential','host_run_id'}


def parse_instance(raw):
    config = parse_canonical_json(raw, label='instance')
    diagnostic = type(config) is dict and config.get('schema') == 'qualification_execution_instance/v2'
    fields(config, INSTANCE_FIELDS | ({'seal_probe_uid'} if diagnostic else set()))
    host_identity(config['host_run_id'])
    if config['schema'] not in ('qualification_execution_instance/v1', 'qualification_execution_instance/v2') or config['authority_class'] not in ('TEST_ONLY', 'OPERATOR'):
        raise ValueError('instance schema/authority differs')
    for name in ('installation_root', 'data_root', 'daemon_data_root', 'socket_path', 'execution_credential'):
        if (type(config[name]) is not str or not PurePosixPath(config[name]).is_absolute()
                or str(PurePosixPath(config[name])) != config[name] or '..' in PurePosixPath(config[name]).parts):
            raise ValueError('absolute protected instance paths required')
    values = [config[name] for name in ('client_uid', 'service_uid', 'g5_uid', 'operator_uid')]
    if any(type(value) is not int or value < 0 for value in values) or len(set(values)) != 4 or config['service_uid'] == 0 or config['g5_uid'] == 0:
        raise ValueError('distinct nonroot service/G5 identities required')
    if diagnostic and (type(config['seal_probe_uid']) is not int or config['seal_probe_uid'] <= 0 or config['seal_probe_uid'] in values):
        raise ValueError('distinct harmless seal probe UID required')
    if type(config['socket_gid']) is not int or config['socket_gid'] < 0:
        raise ValueError('socket group required')
    return config


def _admin():
    if sys.platform != 'linux' or os.geteuid() != 0:
        raise ValueError('Linux administrator installation required')


def _write(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    path.chmod(0o444)
    fsync_directory(path.parent)


def install_release(manifest_bytes, approval_bytes, *, instance_config):
    _admin()
    config = parse_instance(instance_config)
    root = Path(config['installation_root'])
    protected_path(root)
    keys = load_keys(read_regular(root, 'keys.json', limit=1024 * 1024), authority_class=config['authority_class'])
    release = verify_release(manifest_bytes, approval_bytes, keys, now=datetime.now(timezone.utc),
                             installation_authority=config['authority_class'])
    if (release.document['schema'] in ('qualification_execution_release/v3', 'qualification_execution_release/v4', 'qualification_execution_release/v5')) != (config['schema'] == 'qualification_execution_instance/v2'):
        raise ValueError('diagnostic instance/release versions must agree')
    if release.profile.worker_uid in (0, config['service_uid'], config['g5_uid'], config.get('seal_probe_uid')):
        raise ValueError('worker identity must be separate from host authorities')
    code_root = installed_code_root()
    protected_path(code_root)
    for role in ('supervisor', 'g5'):
        observed = observe_runtime(code_root, role)
        if observed != release.document['runtime_manifests'][role]:
            raise ValueError('installed source/runtime manifest differs')
        for row in observed['sources'].values():
            protected_path(code_root / row['path'])
    # The installer is not either execution process. Each fixed entrypoint
    # separately measures its loaded origins and isolated interpreter at startup.
    _write(root / 'release.json', manifest_bytes)
    _write(root / 'release-approval.json', approval_bytes)
    _write(root / 'supervisor.json', instance_config)


def stage_bundle(source_dir, *, instance_config):
    _admin()
    config = parse_instance(instance_config)
    installation = Path(config['installation_root'])
    release = read_regular(installation, 'release.json', limit=16 * 1024 * 1024)
    keys = load_keys(read_regular(installation, 'keys.json', limit=1024 * 1024), authority_class=config['authority_class'])
    context = verify_bundle(Path(source_dir), release, keys, datetime.now(timezone.utc))
    destination = Path(config['data_root']) / 'bundles' / context.bundle_sha256
    destination.mkdir(parents=True, exist_ok=False, mode=0o755)
    _write(destination / 'index.json', context.retained_bundle_index)
    for row in parse_canonical_json(context.retained_bundle_index, label='index')['entries']:
        _write(destination / row['path'], context.retained_bytes[row['role']])
    fsync_directory(destination)
    return context.bundle_sha256
