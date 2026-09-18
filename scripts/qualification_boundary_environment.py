"""Inspect disposable Linux prerequisites. Never provision or launch a worker."""
from __future__ import annotations

import hashlib
import importlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import socket
import stat
import subprocess
import sys
import tempfile
from tools.qualification_verification.role_policy import ROLES, ROLE_GROUPS

SCHEMA = 'qualification_environment/v1'
TRUST_MODEL = 'trusted_administrator_and_privileged_qexec/v1'
REQUIRED = frozenset(('linux', 'administrator', 'execution_profile', 'instance',
    'signing', 'peer_credentials', 'roles', 'trusted_roots', 'permissions',
    'native_storage', 'docker', 'image', 'profile_binding', 'evidence', 'scratch'))


def new_report():
    return {'schema': SCHEMA, 'purpose': 'environment_readiness', 'ready': False,
            'trust_model': TRUST_MODEL,
            'checks': {}, 'failures': [], 'python': sys.version.split()[0],
            'interpreter': sys.executable, 'platform': platform.platform()}


def check(report, name, probe):
    """Retain observations, but never exception text that might contain secrets."""
    try:
        value = probe()
        if value is False or value is None:
            raise ValueError()
        report['checks'][name] = {'ok': True, 'observed': value}
        return value
    except (OSError, ValueError, KeyError, TypeError, ImportError,
            subprocess.SubprocessError):
        reason = type(sys.exception()).__name__
        report['checks'][name] = {'ok': False}
        report['failures'].append({'name': name, 'reason': reason})
        return None


def require_environment(report):
    if report.get('trust_model') != TRUST_MODEL:
        raise ValueError('Environment trust model must explicitly include privileged qexec')
    failures = report.get('failures', [])
    checks = report.get('checks', {})
    missing = sorted(name for name in REQUIRED if checks.get(name, {}).get('ok') is not True)
    if (report.get('schema') != SCHEMA or report.get('purpose') != 'environment_readiness'
            or report.get('ready') is not True or failures or missing):
        names = sorted(set(missing + [f.get('name', 'malformed') for f in failures]))
        raise ValueError('Environment prerequisites failed: ' + ', '.join(names))


def load_profile(raw):
    # Optional until the boundary owner lands its implementation. Absence is a
    # named failed prerequisite, never a replacement profile or acceptance skip.
    module = importlib.import_module('c1_rail.qualification.execution.profile')
    return module.parse_profile(raw)


def protected(path):
    """Reject links and writable/untrusted ancestors, including the object itself."""
    path = Path(path)
    if not path.is_absolute() or '..' in path.parts:
        raise ValueError('absolute protected path required')
    for part in (path, *path.parents):
        info = part.lstat()
        if stat.S_ISLNK(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o022:
            raise ValueError('unprotected path')
    return path


def read_instance(path):
    path = protected(path)
    doc = json.loads(path.read_bytes())
    expected = {'schema', 'authority_class', 'roles', 'trusted_roots', 'data',
                'execution_key', 'result_key', 'scratch', 'evidence', 'docker_socket',
                'worker_image_id', 'profile_sha256'}
    if set(doc) != expected or doc['schema'] != 'qualification_test_instance/v1':
        raise ValueError('instance schema')
    if doc['authority_class'] != 'TEST_ONLY' or doc['docker_socket'] != '/var/run/docker.sock':
        raise ValueError('TEST_ONLY local Docker required')
    if not doc['trusted_roots']:
        raise ValueError('trusted roots required')
    for name in ('data', 'execution_key', 'result_key', 'scratch', 'evidence'):
        path = Path(doc[name])
        if not path.is_absolute() or '..' in path.parts or path.resolve() != path:
            raise ValueError('unsafe instance path')
    return doc


def identities(doc):
    import grp
    import pwd
    result = {}
    if set(doc['roles']) != set(ROLES):
        raise ValueError('three roles required')
    docker_gid = grp.getgrnam('docker').gr_gid
    for role, uid in doc['roles'].items():
        if type(uid) is not int or uid <= 0:
            raise ValueError('non-root UID required')
        user = pwd.getpwuid(uid)
        groups = sorted(os.getgrouplist(user.pw_name, user.pw_gid))
        expected_groups = {uid} | {doc['roles'][group] if group in doc['roles'] else grp.getgrnam(group).gr_gid
                                   for group in ROLE_GROUPS[role]}
        if user.pw_gid != uid or docker_gid in doc['roles'].values() or set(groups) != expected_groups:
            raise ValueError('unexpected primary or supplementary group')
        result[role] = {'uid': uid, 'gid': user.pw_gid, 'groups': groups}
    if len(set(doc['roles'].values())) != 3:
        raise ValueError('role UIDs must differ')
    return result


# This child has no imports from the installed application or user environment.
ACCESS_PROBE = r'''
import json, os, socket, sys, uuid
role, action, path = json.loads(sys.argv[1])
os.setgroups(role['groups']); os.setgid(role['gid']); os.setuid(role['uid'])
allowed = False
try:
    if action == 'read':
        with open(path, 'rb') as stream: stream.read(1)
        allowed = True
    elif action == 'write':
        target = os.path.join(path, '.permission-probe-' + uuid.uuid4().hex)
        fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        os.close(fd); os.unlink(target); allowed = True
    elif action == 'socket':
        with socket.socket(socket.AF_UNIX) as client: client.connect(path)
        allowed = True
    else: raise ValueError('unknown probe')
except PermissionError:
    pass
print(json.dumps({'allowed': allowed, 'uid': os.geteuid(), 'groups': os.getgroups()}))
'''


def run(command):
    result = subprocess.run(command, capture_output=True, text=True, check=True,
                            timeout=30, env={'PATH': '/usr/sbin:/usr/bin:/sbin:/bin', 'HOME': '/nonexistent'})
    return result.stdout.strip()


def probe_access(role, action, path):
    return json.loads(run(['/usr/bin/python3', '-I', '-c', ACCESS_PROBE,
                           json.dumps([role, action, path])]))


def permissions(doc, roles):
    observations = []
    for role in roles:
        for action, field, owner in (
                ('write', 'data', 'qexec'), ('read', 'execution_key', 'qexec'),
                ('read', 'result_key', 'qg5'), ('socket', 'docker_socket', 'qexec'),
                ('write', 'scratch', 'qexec')):
            observation = probe_access(roles[role], action, doc[field])
            observation.update(role=role, action=action, path=doc[field], expected=role == owner)
            observations.append(observation)
    # Retain all denial observations even when one permission is weakened.
    return {'ok': all(o['allowed'] == o['expected'] for o in observations), 'probes': observations,
            'scope': 'direct_os_access_only', 'trust_model': TRUST_MODEL,
            'qexec_daemon_mediated_access_is_unrestricted': True}


def trusted_roots(doc):
    for root in doc['trusted_roots']:
        protected(root)
        for directory, dirs, files in os.walk(root, followlinks=False):
            for name in dirs + files:
                protected(Path(directory) / name)
    return doc['trusted_roots']


def storage(doc):
    observed = {name: run(['/usr/bin/findmnt', '-n', '-o', 'FSTYPE', '-T', doc[name]])
                for name in ('data', 'scratch', 'evidence')}
    if set(observed.values()) != {'ext4'}:
        raise ValueError('native ext4 required')
    return observed


def writable_directory(path):
    with tempfile.TemporaryFile(dir=path) as probe:
        probe.write(b'prerequisite'); probe.flush(); os.fsync(probe.fileno())
    return path


def inspect_environment(instance_path: Path, profile_bytes: bytes) -> dict:
    report = new_report()
    linux = check(report, 'linux', lambda: platform.system() == 'Linux')
    administrator = check(report, 'administrator', lambda: hasattr(os, 'geteuid') and os.geteuid() == 0)
    profile = check(report, 'execution_profile', lambda: load_profile(profile_bytes))
    if profile is not None:
        report['checks']['execution_profile']['observed'] = hashlib.sha256(profile_bytes).hexdigest()
    check(report, 'signing', lambda: importlib.metadata.version('cryptography'))
    check(report, 'peer_credentials', lambda: hasattr(socket, 'SO_PEERCRED'))
    if not linux or not administrator:
        return report
    doc = check(report, 'instance', lambda: read_instance(instance_path))
    if not doc:
        return report
    report['checks']['instance']['observed'] = str(instance_path)
    roles = check(report, 'roles', lambda: identities(doc))
    check(report, 'trusted_roots', lambda: trusted_roots(doc))
    if roles:
        observation = check(report, 'permissions', lambda: permissions(doc, roles))
        if observation and not observation['ok']:
            report['checks']['permissions']['ok'] = False
            report['failures'].append({'name': 'permissions', 'reason': 'access_mismatch'})
    check(report, 'native_storage', lambda: storage(doc))
    docker = ['/usr/bin/docker', '--host', 'unix://' + doc['docker_socket']]
    check(report, 'docker', lambda: json.loads(run([*docker, 'version', '--format', '{{json .Server}}'])))
    def image():
        observed = json.loads(run([*docker, 'image', 'inspect', doc['worker_image_id']]))
        if len(observed) != 1 or observed[0]['Id'] != doc['worker_image_id']:
            raise ValueError('image identity mismatch')
        return {'id': observed[0]['Id'], 'digests': observed[0].get('RepoDigests', [])}
    check(report, 'image', image)
    check(report, 'profile_binding', lambda: profile is not None and
          hashlib.sha256(profile_bytes).hexdigest() == doc['profile_sha256'])
    check(report, 'evidence', lambda: writable_directory(doc['evidence']))
    def scratch():
        writable_directory(doc['scratch'])
        available = os.statvfs(doc['scratch'])
        size = available.f_bavail * available.f_frsize
        if profile is None or size < profile.scratch_bytes:
            raise ValueError('insufficient scratch')
        return {'available_bytes': size}
    check(report, 'scratch', scratch)
    report['ready'] = not report['failures'] and set(report['checks']) == REQUIRED
    return report
