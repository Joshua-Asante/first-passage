"""Administrator-only disposable host setup and manifest-scoped retirement."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import platform
import shutil
import stat
import subprocess
import sys
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.qualification_boundary_environment import TRUST_MODEL, protected, run
from scripts.record_verification import snapshot

ROLES = ('qclient', 'qexec', 'qg5')
# These names are shared host-wide, even across installation-layout variants.
IDENTITY_STATE = Path('/var/lib/fp-qualification-identities')


def load_config():
    return json.loads((ROOT / 'tools/qualification_verification/host.json').read_bytes())


def resolve_roles(config):
    first = config['uid_start']
    if type(first) is not int or first <= 0 or first + len(ROLES) >= 2**32:
        raise ValueError('invalid identity configuration')
    return {name: first + index for index, name in enumerate(ROLES)}


def public_observations(manifest):
    """Explicit export allowlist, separate from private resource ownership."""
    return {'schema': 'qualification_host_observations/v1',
            'trust_model': TRUST_MODEL,
            **{name: manifest[name] for name in ('run_id', 'host_config_sha256',
                'facts', 'runtime', 'roles')},
            'source_commit': manifest['source']['commit'],
            'source_fingerprint': manifest['source']['fingerprint']}


def validate_inputs(source, config):
    if config['schema'] != 'qualification_test_host/v1':
        raise ValueError('host schema')
    resolve_roles(config)
    for relative, expected in config['locks'].items():
        path = resource_path(source, relative)
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('lock digest mismatch: ' + relative)


def resource_path(root, relative):
    path = PurePosixPath(relative)
    if not relative or path.is_absolute() or '..' in path.parts or str(path) == '.' or '\\' in relative or ':' in relative:
        raise ValueError('unsafe resource path')
    result = root.joinpath(*path.parts)
    if result.resolve() != result.absolute() or not result.resolve().is_relative_to(root.resolve()):
        raise ValueError('resource link/escape')
    return result


def inspect_tree(path):
    if path.is_symlink():
        raise ValueError('resource link')
    if not path.exists():
        return []
    device = path.stat().st_dev
    result = []
    for directory, dirs, files in os.walk(path, followlinks=False):
        for entry in [Path(directory), *(Path(directory) / name for name in dirs + files)]:
            info = entry.lstat()
            if stat.S_ISLNK(info.st_mode):
                raise ValueError('resource link')
            if info.st_dev != device or os.path.ismount(entry):
                raise ValueError('resource mount')
            if not (stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode) or stat.S_ISSOCK(info.st_mode)):
                raise ValueError('unsupported resource object')
            result.append(entry)
    return result


def validate_owned_tree(path, uid):
    if path.exists() and path.stat().st_uid != uid:
        raise ValueError('tree owner mismatch')
    inspect_tree(path)


def require_inactive_principals(uids):
    for process in Path('/proc').iterdir():
        if not process.name.isdecimal():
            continue
        try:
            values = (process / 'status').read_text().splitlines()
        except FileNotFoundError:
            continue
        uid_line = next(line for line in values if line.startswith('Uid:'))
        if set(map(int, uid_line.split()[1:])) & uids:
            raise ValueError('active test principal')


def validate_resources(manifest, root):
    seen = set()
    for item in manifest['resources']:
        kind = item.get('kind')
        if kind == 'tree':
            if set(item) != {'kind', 'path', 'uid'} or item['path'] not in ('code', 'env', 'data', 'keys', 'scratch'):
                raise ValueError('invalid tree resource')
            resource_path(root, item['path'])
            identity = kind, item['path']
        elif kind in ('user', 'group'):
            if set(item) != {'kind', 'name', 'id'} or item['name'] not in ROLES:
                raise ValueError('invalid identity resource')
            expected = resolve_roles(manifest['host_config'])
            if manifest['roles'] != expected or type(item['id']) is not int or item['id'] != expected[item['name']]:
                raise ValueError('invalid identity resource')
            identity = kind, item['name']
        else:
            # No arbitrary commands, processes, image tags, mounts or provider IDs.
            raise ValueError('unsupported resource kind')
        if identity in seen:
            raise ValueError('duplicate resource')
        seen.add(identity)


def save(path, data, *, exclusive=False, mode=0o600):
    raw = (json.dumps(data, indent=2, sort_keys=True) + '\n').encode()
    flags = os.O_WRONLY | os.O_CREAT | (os.O_EXCL if exclusive else os.O_TRUNC)
    temporary = path if exclusive else path.with_suffix('.tmp')
    fd = os.open(temporary, flags | getattr(os, 'O_NOFOLLOW', 0), mode)
    with os.fdopen(fd, 'wb') as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    if not exclusive:
        os.replace(temporary, path)
    directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)


@contextmanager
def ownership_lock(root):
    import fcntl
    fd = os.open(root / 'owner.lock', os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield
    finally:
        os.close(fd)


@contextmanager
def identity_reservation():
    """Serialize host-wide name/ID collision checks, creation and retirement."""
    administrator()
    protected(IDENTITY_STATE.parent)
    IDENTITY_STATE.mkdir(mode=0o700, exist_ok=True)
    protected(IDENTITY_STATE)
    with ownership_lock(IDENTITY_STATE):
        yield IDENTITY_STATE / 'reservation.json'


def reservation_owner(path):
    if not path.exists():
        return None
    doc = json.loads(path.read_bytes())
    if doc.get('schema') != 'qualification_identity_reservation/v1' or 'owner' not in doc:
        raise ValueError('invalid identity reservation')
    return doc['owner']


def require_available_reservation(path):
    if reservation_owner(path) is not None:
        raise ValueError('host identities are reserved; clean up the owning manifest first')


def require_reservation_owner(path, manifest_path, manifest):
    expected = {'run_id': manifest['run_id'], 'manifest': str(manifest_path)}
    owner = reservation_owner(path)
    # A crash between manifest creation and reservation cannot own resources.
    if owner != expected and not (owner is None and not manifest['resources']):
        raise ValueError('identity reservation owner mismatch')


def write_reservation(path, owner):
    save(path, {'schema': 'qualification_identity_reservation/v1', 'owner': owner})


def administrator():
    if platform.system() != 'Linux' or os.geteuid() != 0:
        raise ValueError('Linux administrator required')


def host_facts(config):
    administrator()
    release = platform.freedesktop_os_release()
    if (release['ID'], release['VERSION_ID'], platform.machine()) != (
            config['os_id'], config['os_release'], config['architecture']):
        raise ValueError('unsupported OS/architecture')
    version = run([config['python'], '-I', '-c', 'import platform; print(platform.python_version())'])
    if version != config['python_version']:
        raise ValueError('Python patch mismatch')
    docker = json.loads(run([config['docker'], '--host', 'unix:///var/run/docker.sock',
                            'version', '--format', '{{json .Server}}']))
    if docker['Version'] != config['docker_version']:
        raise ValueError('Docker version mismatch')
    package = run(['/usr/bin/dpkg-query', '-W', '-f=${Version}', config['docker_package']])
    if package != config['docker_package_version']:
        raise ValueError('Docker package mismatch')
    return {'os': release, 'python': version, 'docker': docker,
            'docker_package': package, 'kernel': platform.release(),
            'packages': run(['/usr/bin/dpkg-query', '-W', '-f=${Package}=${Version}\n']),
            'images': run([config['docker'], '--host', 'unix:///var/run/docker.sock',
                           'image', 'ls', '--no-trunc', '--format', '{{json .}}']),
            'containers': run([config['docker'], '--host', 'unix:///var/run/docker.sock',
                               'ps', '-a', '--no-trunc', '--format', '{{json .}}'])}


def provision(source, *, manifest_output=None):
    config = load_config()
    validate_inputs(source, config)
    facts = host_facts(config)
    with identity_reservation() as reservation:
        require_available_reservation(reservation)
        return provision_reserved(source, config, facts, reservation, manifest_output)


def provision_reserved(source, config, facts, reservation, manifest_output):
    """Caller holds the host-wide identity reservation lock throughout setup."""
    import grp
    import pwd
    roles = resolve_roles(config)
    # Existing names/IDs are not ours, even if they look like an earlier test.
    for name, uid in roles.items():
        for lookup, value in ((pwd.getpwnam, name), (grp.getgrnam, name),
                              (pwd.getpwuid, uid), (grp.getgrgid, uid)):
            try:
                lookup(value)
            except KeyError:
                continue
            raise ValueError('pre-existing test identity: ' + name)
    parent = Path(config['parent'])
    protected(parent.parent)
    parent.mkdir(mode=0o755, exist_ok=True)
    protected(parent)
    if run(['/usr/bin/findmnt', '-n', '-o', 'FSTYPE', '-T', str(parent)]) != config['filesystem']:
        raise ValueError('native ext4 required')
    root = parent / uuid4().hex
    root.mkdir(mode=0o711)
    manifest = {'schema': 'qualification_host_ownership/v2', 'run_id': root.name,
                'root': str(root), 'state': 'provisioning', 'resources': [],
                'host_config_sha256': hashlib.sha256((ROOT / 'tools/qualification_verification/host.json').read_bytes()).hexdigest(),
                'host_config': config, 'facts': facts, 'roles': roles, 'source': snapshot(source)}
    manifest_path = root / 'ownership.json'
    save(manifest_path, manifest, exclusive=True)
    write_reservation(reservation, {'run_id': root.name, 'manifest': str(manifest_path)})
    if manifest_output is not None:
        fd = os.open(manifest_output, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, 'w') as stream:
            stream.write(str(manifest_path) + '\n')
    print(f'Private ownership manifest: {manifest_path}', flush=True)
    with ownership_lock(root):
        try:
            def own(item):
                manifest['resources'].append(item)
                save(manifest_path, manifest)
            for name, uid in roles.items():
                own({'kind': 'group', 'name': name, 'id': uid})
                run(['/usr/sbin/groupadd', '--gid', str(uid), name])
                own({'kind': 'user', 'name': name, 'id': uid})
                run(['/usr/sbin/useradd', '--uid', str(uid), '--gid', str(uid),
                     '--no-create-home', '--no-log-init', '--home-dir', '/nonexistent',
                     '--shell', '/usr/sbin/nologin', '--comment', root.name, name])
            run(['/usr/sbin/usermod', '--append', '--groups', 'docker', 'qexec'])
            for relative, uid, mode in (('code', 0, 0o755), ('env', 0, 0o755),
                    ('data', manifest['roles']['qexec'], 0o700), ('keys', 0, 0o755),
                    ('scratch', manifest['roles']['qexec'], 0o700)):
                own({'kind': 'tree', 'path': relative, 'uid': uid})
                target = root / relative
                target.mkdir(mode=mode)
                os.chown(target, uid, uid)
            (root / 'evidence').mkdir(mode=0o700)
            for relative in manifest['source']['files']:
                src = resource_path(source, relative)
                if manifest['source']['files'][relative] == 'deleted' and not src.exists():
                    continue
                if not src.is_file():
                    raise ValueError('source entry must be a regular file')
                dst = resource_path(root / 'code', relative)
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, dst)
                dst.chmod(0o644)
                if hashlib.sha256(dst.read_bytes()).hexdigest() != manifest['source']['files'][relative]:
                    raise ValueError('source drift during staging')
            if snapshot(source) != manifest['source']:
                raise ValueError('source drift during staging')
            python = root / 'env/bin/python'
            run([config['python'], '-I', '-m', 'venv', '--copies', '--without-pip', str(root / 'env')])
            # venv's convenience alias is not needed; retained trees reject links.
            alias = root / 'env/lib64'
            if alias.is_symlink() and os.readlink(alias) == 'lib':
                alias.unlink()
            # The system pip only installs into this new, owned environment.
            subprocess.run([config['python'], '-I', '-m', 'pip', '--python', str(python),
                'install', '--require-hashes', '--only-binary=:all:', '-r', str(root / 'code/requirements-ops.lock'),
                '-r', str(root / 'code/tools/qualification_verification/requirements-signing.lock')], check=True,
                env={'PATH': '/usr/bin:/bin', 'HOME': '/nonexistent', 'PIP_DISABLE_PIP_VERSION_CHECK': '1'})
            run([str(python), '-I', str(root / 'code/scripts/fp.py'), '--env', str(root / 'env'), 'doctor'])
            key_code = ('from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey; '
                        'from pathlib import Path; import sys; '
                        'Path(sys.argv[1]).write_bytes(Ed25519PrivateKey.generate().private_bytes_raw())')
            for name in ('qexec', 'qg5'):
                directory = root / 'keys' / name
                directory.mkdir(mode=0o700)
                uid = manifest['roles'][name]
                os.chown(directory, uid, uid)
                key = directory / 'TEST_ONLY.key'
                run([str(python), '-I', '-c', key_code, str(key)])
                key.chmod(0o400); os.chown(key, uid, uid)
            manifest['state'] = 'host_ready_boundary_unconfigured'
            manifest['runtime'] = {'python': str(python), 'version': config['python_version'],
                'packages': json.loads(run([str(python), '-I', '-c',
                    'import importlib.metadata as m, json; '
                    'print(json.dumps(sorted((d.metadata["Name"], d.version) for d in m.distributions())))']))}
            save(manifest_path, manifest)
            save(root / 'evidence/host-observations.json', public_observations(manifest),
                 exclusive=True, mode=0o400)
        except BaseException as exc:
            manifest['state'] = 'setup_failed'
            manifest['failure'] = type(exc).__name__
            save(manifest_path, manifest)
            raise
    return manifest_path


def cleanup(manifest_path):
    import grp
    import pwd
    administrator()
    manifest_path = protected(manifest_path)
    if manifest_path.name != 'ownership.json' or manifest_path.stat().st_mode & 0o077:
        raise ValueError('private ownership manifest required')
    root = manifest_path.parent
    with identity_reservation() as reservation, ownership_lock(root):
        manifest = json.loads(manifest_path.read_bytes())
        if (manifest.get('schema') != 'qualification_host_ownership/v2'
                or manifest.get('root') != str(root) or manifest.get('run_id') != root.name
                or root.parent != Path(manifest['host_config']['parent']) or len(root.name) != 32
                or any(c not in '0123456789abcdef' for c in root.name)):
            raise ValueError('ownership identity mismatch')
        validate_resources(manifest, root)
        receipt = {'schema': 'qualification_host_cleanup/v1', 'run_id': root.name,
                   'manifest_sha256': hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
                   'removed': [], 'retained': ['ownership.json', 'evidence', 'owner.lock', 'retired.json'],
                   'failures': [], 'ok': False}
        try:
            retired = root / 'retired.json'
            if retired.exists():
                prior = json.loads(protected(retired).read_bytes())
                if prior != {'manifest_sha256': receipt['manifest_sha256']}:
                    raise ValueError('retirement identity mismatch')
                # A prior completed cleanup owns no current identities. It must
                # never inspect/remove a replacement run using the same IDs.
                if reservation_owner(reservation) == {'run_id': root.name, 'manifest': str(manifest_path)}:
                    write_reservation(reservation, None)
                receipt['ok'] = True
                receipt['already_retired'] = True
                save(root / ('cleanup-' + uuid4().hex + '.json'), receipt, exclusive=True, mode=0o400)
                return receipt
            require_reservation_owner(reservation, manifest_path, manifest)
            uids = {r['id'] for r in manifest['resources'] if r['kind'] == 'user'}
            require_inactive_principals(uids)
            # Boundary containers/services are not produced by this host-only slice.
            # Any later producer must extend this manifest before enabling acceptance.
            containers = run(['/usr/bin/docker', '--host', 'unix:///var/run/docker.sock',
                              'ps', '-aq', '--filter', 'label=fp.qualification.host=' + root.name])
            if containers:
                raise ValueError('boundary containers require boundary-owned cleanup')
            for item in manifest['resources']:
                if item['kind'] == 'user':
                    try:
                        user = pwd.getpwnam(item['name'])
                    except KeyError:
                        try:
                            pwd.getpwuid(item['id'])
                        except KeyError:
                            continue
                        raise ValueError('UID reused')
                    if user.pw_uid != item['id'] or user.pw_gecos != root.name:
                        raise ValueError('user ownership mismatch')
                elif item['kind'] == 'group':
                    try:
                        group = grp.getgrnam(item['name'])
                    except KeyError:
                        try:
                            grp.getgrgid(item['id'])
                        except KeyError:
                            continue
                        raise ValueError('GID reused')
                    if group.gr_gid != item['id'] or group.gr_mem:
                        raise ValueError('group shared or replaced')
                    if any(p.pw_gid == item['id'] and p.pw_uid not in uids for p in pwd.getpwall()):
                        raise ValueError('group has unrelated consumer')
                else:
                    path = resource_path(root, item['path'])
                    validate_owned_tree(path, item['uid'])
            # Validate everything before removing anything; never follow a link.
            for item in reversed(manifest['resources']):
                if item['kind'] == 'tree':
                    path = resource_path(root, item['path'])
                    if path.exists():
                        shutil.rmtree(path)
                elif item['kind'] == 'user':
                    try:
                        pwd.getpwnam(item['name'])
                    except KeyError:
                        continue
                    run(['/usr/sbin/userdel', item['name']])
                else:
                    try:
                        grp.getgrnam(item['name'])
                    except KeyError:
                        continue
                    run(['/usr/sbin/groupdel', item['name']])
                receipt['removed'].append(item)
            # The locks provide exclusivity. Atomic publication prevents a hard
            # kill from leaving a partial authoritative retirement certificate.
            save(retired, {'manifest_sha256': receipt['manifest_sha256']}, mode=0o400)
            write_reservation(reservation, None)
            receipt['ok'] = True
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            receipt['failures'].append(type(exc).__name__ + ': ' + str(exc) if isinstance(exc, ValueError)
                                       else type(exc).__name__)
        save(root / ('cleanup-' + uuid4().hex + '.json'), receipt, exclusive=True, mode=0o400)
    return receipt


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT)
    parser.add_argument('--manifest', type=Path)
    parser.add_argument('--manifest-output', type=Path)
    args = parser.parse_args(argv)
    try:
        if args.manifest:
            result = cleanup(args.manifest)
            print(json.dumps(result))
            return 0 if result['ok'] else 2
        provision(args.source.resolve(), manifest_output=args.manifest_output)
        return 0
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f'Host setup/cleanup failed: {type(exc).__name__}: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
