"""Administrator-only disposable host setup and manifest-scoped retirement."""
from __future__ import annotations

import argparse
from collections import deque
import errno
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import platform
import re
import shutil
import sqlite3
import stat
import subprocess
import sys
import time
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.qualification_boundary_environment import TRUST_MODEL, protected, run
from scripts.record_verification import snapshot
from tools.qualification_verification.container_ownership import HOST_LABEL, BUILD_LABEL, host_identity, owned_containers
from tools.qualification_verification.role_policy import ROLES, ROLE_GROUPS, owned_group_members

REQUIRED_LOCKS = frozenset({
    'requirements-ops.lock',
    'tools/local_verification/requirements-extra.txt',
    'tools/qualification_verification/signing-wheel.json',
})
# These names are shared host-wide, even across installation-layout variants.
IDENTITY_STATE = Path('/var/lib/fp-qualification-identities')
CGROUP_ROOT = Path('/sys/fs/cgroup')
PROCESS_STOP_TIMEOUT = 30


def load_config():
    raw = (ROOT / 'tools/qualification_verification/host.json').read_bytes()
    return json.loads(raw), hashlib.sha256(raw).hexdigest()


def signing_requirements(shared_bytes, wheel_bytes):
    """Resolve the sole version owner with a separately reviewed Linux wheel hash."""
    pins = [line.strip() for line in shared_bytes.decode('utf-8').splitlines()
            if line.strip().lower().startswith('cryptography')]
    if len(pins) != 1 or re.fullmatch(r'cryptography==[0-9]+\.[0-9]+\.[0-9]+', pins[0]) is None:
        raise ValueError('one exact canonical signing pin required')
    wheel = json.loads(wheel_bytes)
    if (type(wheel) is not dict or set(wheel) != {'schema','package','sha256'}
            or wheel['schema'] != 'qualification_signing_wheel/v1' or wheel['package'] != 'cryptography'
            or type(wheel['sha256']) is not str or re.fullmatch('[0-9a-f]{64}',wheel['sha256']) is None):
        raise ValueError('reviewed signing wheel identity required')
    return (pins[0] + ' --hash=sha256:' + wheel['sha256'] + '\n').encode('ascii')


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
    validate_executable_paths(config)
    if not isinstance(config.get('locks'), dict) or set(config['locks']) != REQUIRED_LOCKS:
        raise ValueError('host configuration must identify every required lock')
    for relative, expected in config['locks'].items():
        path = resource_path(source, relative)
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('lock digest mismatch: ' + relative)


def validate_executable_paths(config):
    for name in ('python', 'docker'):
        value = config.get(name)
        if (not isinstance(value, str) or not PurePosixPath(value).is_absolute()
                or '..' in PurePosixPath(value).parts or '\\' in value or '\0' in value):
            raise ValueError('absolute executable path required: ' + name)


def protected_executable(value):
    requested = Path(value)
    if not requested.is_absolute():
        raise ValueError('absolute executable path required')
    path = protected(Path(requested.anchor))
    pending = deque(requested.parts[1:])
    links = 0
    # Resolve one component at a time: resolve() would hide writable intermediate
    # directories and symlinks. Check directories before processing any '..'.
    while pending:
        part = pending.popleft()
        if part == '..':
            path = path.parent
            continue
        candidate = path / part
        info = candidate.lstat()
        if stat.S_ISLNK(info.st_mode):
            links += 1
            if info.st_uid != 0 or links > 40:
                raise ValueError('unprotected or cyclic executable symlink')
            target = Path(os.readlink(candidate))
            if target.is_absolute():
                path = protected(Path(target.anchor))
                pending.extendleft(reversed(target.parts[1:]))
            else:
                pending.extendleft(reversed(target.parts))
        else:
            path = protected(candidate)
            if pending and not stat.S_ISDIR(info.st_mode):
                raise ValueError('executable ancestor must be a directory')
    if not path.is_file() or not os.access(path, os.X_OK):
        raise ValueError('regular executable required')


def validate_host_executables(config):
    validate_executable_paths(config)
    for name in ('python', 'docker'):
        protected_executable(config[name])


def resource_path(root, relative):
    path = PurePosixPath(relative)
    if not relative or path.is_absolute() or '..' in path.parts or str(path) == '.' or '\\' in relative or ':' in relative:
        raise ValueError('unsafe resource path')
    result = root.joinpath(*path.parts)
    if result.resolve() != result.absolute() or not result.resolve().is_relative_to(root.resolve()):
        raise ValueError('resource link/escape')
    return result


def inspect_tree(path, *, allow_initial_venv_alias=False):
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
                # venv --copies still creates this convenience alias. A killed
                # setup can leave it behind before the normal unlink. Walk and
                # rmtree never follow it; permit only this exact private alias.
                if (allow_initial_venv_alias and entry == path / 'lib64'
                        and info.st_uid == info.st_gid == 0 and os.readlink(entry) == 'lib'):
                    result.append(entry)
                    continue
                raise ValueError('resource link')
            if info.st_dev != device or os.path.ismount(entry):
                raise ValueError('resource mount')
            if not (stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode) or stat.S_ISSOCK(info.st_mode)):
                raise ValueError('unsupported resource object')
            result.append(entry)
    return result


def validate_owned_tree(path, uid, *, allow_initial_owner=False, allow_initial_venv_alias=False):
    if path.exists():
        info = path.stat()
        if info.st_uid != uid:
            # mkdir precedes chown during setup. Only that empty, private
            # administrator-owned intermediate is safe to retire on retry.
            initial = (allow_initial_owner and info.st_uid == info.st_gid == 0
                       and stat.S_ISDIR(info.st_mode) and stat.S_IMODE(info.st_mode) == 0o700
                       and not any(path.iterdir()))
            if not initial:
                raise ValueError('tree owner mismatch')
    inspect_tree(path, allow_initial_venv_alias=allow_initial_venv_alias)


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


def validate_owned_user(user, item, run_id, groups):
    """Reject identity drift, including changes to supplementary groups."""
    if (user.pw_uid != item['id'] or user.pw_gid != item['id']
            or user.pw_gecos != run_id):
        raise ValueError('user ownership mismatch')
    memberships = {group.gr_name for group in groups if item['name'] in group.gr_mem}
    expected = set(ROLE_GROUPS[item['name']])
    # An interrupted setup may not have enrolled qexec in Docker yet. Missing
    # intended authority is safe to retire; additional authority is drift.
    if not memberships <= expected:
        raise ValueError('user supplementary groups changed')


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


def process_groups(root):
    """Only this run's exact registered process groups are eligible for retirement."""
    registry = root / 'process-groups.json'
    if not registry.exists():
        return []  # No child can launch before the first registration is durable.
    doc = json.loads(protected(registry).read_bytes())
    if not isinstance(doc, list) or any(not isinstance(item, str) or len(item) != 32
            or any(c not in '0123456789abcdef' for c in item) for item in doc):
        raise ValueError('invalid process group registry')
    return [CGROUP_ROOT / ('fp-qualification-' + root.name + '-' + item) for item in doc]


def create_process_group(root):
    protected(CGROUP_ROOT)
    if not (CGROUP_ROOT / 'cgroup.controllers').is_file():
        raise ValueError('cgroup v2 required')
    group_id = uuid4().hex
    group = CGROUP_ROOT / ('fp-qualification-' + root.name + '-' + group_id)
    if group.exists():
        raise ValueError('pre-existing process group')
    prior = process_groups(root)
    save(root / 'process-groups.json', [p.name.rsplit('-', 1)[1] for p in prior] + [group_id])
    group.mkdir()
    if not (group / 'cgroup.kill').is_file():
        raise ValueError('cgroup.kill required')
    return group


# A child may survive a killed caller before this code runs. Its payload still
# cannot execute unless it joins the owned group; removal closes late entry.
ENTER_PROCESS_GROUP = '''
import os, sys
fd = os.open(sys.argv[1], os.O_WRONLY)
try:
    os.write(fd, b'0')
finally:
    os.close(fd)
os.execv(sys.argv[2], sys.argv[2:])
'''


def owned_command(group, command, interpreter):
    return [interpreter or sys.executable, '-I', '-c', ENTER_PROCESS_GROUP,
            str(group / 'cgroup.procs'), *command]


def owned_environment():
    return {'PATH': '/usr/sbin:/usr/bin:/sbin:/bin', 'HOME': '/nonexistent',
            'PIP_DISABLE_PIP_VERSION_CHECK': '1'}


def start_owned(root, command, *, stdout, stderr, interpreter=None):
    group=create_process_group(root)
    return subprocess.Popen(owned_command(group,command,interpreter),stdin=subprocess.DEVNULL,
                            stdout=stdout,stderr=stderr,env=owned_environment())


def run_owned(group, command, *, capture_output=True, timeout=30, interpreter=None):
    result = subprocess.run(owned_command(group,command,interpreter), check=True, text=True,
        capture_output=capture_output, timeout=timeout,
        env=owned_environment())
    return result.stdout.strip() if capture_output else ''


def stop_process_groups(root):
    for group in process_groups(root):
        deadline = time.monotonic() + PROCESS_STOP_TIMEOUT
        while group.exists():
            protected(group)
            try:
                # The kernel permits removal only when empty. This also retires
                # a never-used group on kernels without cgroup.kill, and closes
                # late entry without a separate racy population check.
                group.rmdir()
            except OSError as exc:
                if exc.errno != errno.EBUSY or time.monotonic() >= deadline:
                    raise
                # Kernel kill covers descendants, including concurrent forks.
                # A populated group without kill support still fails closed.
                with (group / 'cgroup.kill').open('w') as stream:
                    stream.write('1')
                time.sleep(0.05)


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
    validate_host_executables(config)
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
                           'image', 'ls', '--no-trunc', '--format', '{{json .ID}}']),
            # Container commands and labels may contain administrator secrets.
            # The public inventory needs only opaque daemon-assigned identities.
            'containers': run([config['docker'], '--host', 'unix:///var/run/docker.sock',
                               'ps', '-a', '--no-trunc', '--format', '{{json .ID}}'])}


def boundary_containers(config, run_id):
    """Find resources using the Docker executable retained for this host run."""
    return run([config['docker'], '--host', 'unix:///var/run/docker.sock',
                'ps', '-aq', '--no-trunc', '--filter', 'label=' + HOST_LABEL + '=' + host_identity(run_id)])


def boundary_registry(root):
    doc = json.loads(protected(root/'boundary-resources.json').read_bytes())
    if (type(doc) is not dict or set(doc) != {'schema','run_id','build_id','image_id','release_sha256'}
            or doc['schema'] != 'qualification_boundary_ownership/v1' or doc['run_id'] != root.name):
        raise ValueError('boundary ownership registry differs')
    host_identity(doc['run_id']); host_identity(doc['build_id'])
    for field,pattern in (('image_id','sha256:[0-9a-f]{64}'),('release_sha256','[0-9a-f]{64}')):
        value=doc[field]
        if value is not None and (type(value) is not str or re.fullmatch(pattern,value) is None):
            raise ValueError('boundary ownership identity differs')
    if (doc['image_id'] is None) != (doc['release_sha256'] is None):
        raise ValueError('incomplete boundary enrollment')
    return doc


def begin_boundary_build(root):
    """Publish ownership before any image builder or service child is started."""
    administrator(); protected(root)
    doc=dict(schema='qualification_boundary_ownership/v1',run_id=host_identity(root.name),
             build_id=uuid4().hex,image_id=None,release_sha256=None)
    save(root/'boundary-resources.json',doc,exclusive=True,mode=0o400)
    return doc


def enroll_boundary(root, *, image_id, release_bytes):
    administrator(); protected(root)
    doc=boundary_registry(root)
    if doc['image_id'] is not None or type(image_id) is not str or re.fullmatch('sha256:[0-9a-f]{64}',image_id) is None:
        raise ValueError('immutable boundary enrollment required')
    doc.update(image_id=image_id,release_sha256=hashlib.sha256(release_bytes).hexdigest())
    save(root/'boundary-resources.json',doc,mode=0o400)


def owned_journal(path, uid):
    info=path.lstat()
    if (not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_uid != uid
            or info.st_mode & 0o077 or path.resolve() != path):
        raise ValueError('protected owned execution journal required')
    return path


def boundary_cleanup_plan(root, manifest):
    """Inspect only; caller stops owned cgroups/principals before reading SQL."""
    config=manifest['host_config']
    containers=boundary_containers(config,root.name).split()
    if not (root/'boundary-resources.json').exists():
        if containers:
            raise ValueError('boundary containers require boundary-owned cleanup')
        return dict(containers=[],images=[])
    registry=boundary_registry(root)
    docker=[config['docker'],'--host','unix:///var/run/docker.sock']
    container_ids=[]
    if containers:
        if registry['image_id'] is None or any(re.fullmatch('[0-9a-f]{64}',value) is None for value in containers):
            raise ValueError('unenrolled boundary containers')
        journal=owned_journal(root/'data/journal.sqlite',manifest['roles']['qexec'])
        with sqlite3.connect(journal.as_uri()+'?mode=ro',uri=True) as connection:
            connection.row_factory=sqlite3.Row
            connection.execute('PRAGMA query_only=ON')
            executions=[dict(row) for row in connection.execute('SELECT execution_id,container_id,release_sha256 FROM executions')]
        rows=json.loads(run([*docker,'inspect','--type=container',*containers]))
        if type(rows) is not list or sorted(row.get('Id') for row in rows) != sorted(containers):
            raise ValueError('boundary container discovery differs')
        container_ids=list(owned_containers(rows,executions,run_id=root.name,
            image_id=registry['image_id'],release_sha256=registry['release_sha256']))
    images=run([*docker,'image','ls','--all','--quiet','--no-trunc','--filter','label='+HOST_LABEL+'='+root.name]).split()
    image_ids=[]
    for image_id in sorted(set(images)):
        if re.fullmatch('sha256:[0-9a-f]{64}',image_id) is None:
            raise ValueError('boundary image discovery differs')
        rows=json.loads(run([*docker,'image','inspect',image_id]))
        if (type(rows) is not list or len(rows)!=1 or rows[0].get('Id')!=image_id
                or rows[0].get('Config',{}).get('Labels',{}).get(HOST_LABEL)!=root.name
                or rows[0]['Config']['Labels'].get(BUILD_LABEL)!=registry['build_id']
                or registry['image_id'] not in (None,image_id)):
            raise ValueError('boundary image ownership differs')
        image_ids.append(image_id)
    return dict(containers=container_ids,images=image_ids)


def provision(source, *, manifest_output=None):
    config, config_sha256 = load_config()
    validate_inputs(source, config)
    facts = host_facts(config)
    with identity_reservation() as reservation:
        require_available_reservation(reservation)
        return provision_reserved(source, config, config_sha256, facts, reservation, manifest_output)


def provision_reserved(source, config, config_sha256, facts, reservation, manifest_output):
    """Caller holds the host-wide identity reservation lock throughout setup."""
    import grp
    import pwd
    roles = resolve_roles(config)
    # Deleted accounts can leave processes holding their numeric credentials.
    # Reject those UIDs under the reservation lock before publishing or creating
    # anything that would grant the lingering processes access to this run.
    require_inactive_principals(set(roles.values()))
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
    source_snapshot = snapshot(source)
    if any(source_snapshot['files'].get(name) != digest for name, digest in config['locks'].items()):
        raise ValueError('lock digest mismatch in source snapshot')
    if source_snapshot['files'].get('tools/qualification_verification/host.json') != config_sha256:
        raise ValueError('host config digest mismatch in source snapshot')
    root = parent / uuid4().hex
    root.mkdir(mode=0o711)
    manifest = {'schema': 'qualification_host_ownership/v3', 'run_id': root.name,
                'root': str(root), 'state': 'provisioning', 'resources': [],
                'host_config_sha256': config_sha256,
                'host_config': config, 'facts': facts, 'roles': roles, 'source': source_snapshot}
    manifest_path = root / 'ownership.json'
    try:
        save(manifest_path, manifest, exclusive=True)
        # Publish recovery before reservation. No resources or children exist
        # yet, so failures here can roll back this exact unreserved run root.
        if manifest_output is not None:
            fd = os.open(manifest_output, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
            try:
                with os.fdopen(fd, 'w') as stream:
                    stream.write(str(manifest_path) + '\n')
                    stream.flush()
                    os.fsync(stream.fileno())
            except BaseException:
                manifest_output.unlink()
                raise
    except BaseException:
        shutil.rmtree(root)
        raise
    print(f'Private ownership manifest: {manifest_path}', flush=True)
    write_reservation(reservation, {'run_id': root.name, 'manifest': str(manifest_path)})
    with ownership_lock(root):
        try:
            process_group = create_process_group(root)
            def execute(command, **kwargs):
                return run_owned(process_group, command, **kwargs)
            def own(item):
                manifest['resources'].append(item)
                save(manifest_path, manifest)
            for name, uid in roles.items():
                own({'kind': 'group', 'name': name, 'id': uid})
                execute(['/usr/sbin/groupadd', '--gid', str(uid), name])
                own({'kind': 'user', 'name': name, 'id': uid})
                execute(['/usr/sbin/useradd', '--uid', str(uid), '--gid', str(uid),
                     '--no-create-home', '--no-log-init', '--home-dir', '/nonexistent',
                     '--shell', '/usr/sbin/nologin', '--comment', root.name, name])
            for name,groups in ROLE_GROUPS.items():
                if groups:
                    execute(['/usr/sbin/usermod', '--append', '--groups', ','.join(groups), name])
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
            validate_inputs(root / 'code', config)
            python = root / 'env/bin/python'
            execute([config['python'], '-I', '-m', 'venv', '--copies', '--without-pip', str(root / 'env')])
            # venv's convenience alias is not needed; retained trees reject links.
            alias = root / 'env/lib64'
            if alias.is_symlink() and os.readlink(alias) == 'lib':
                alias.unlink()
            runtime_version = execute([str(python), '-I', '-c',
                                       'import platform; print(platform.python_version())'])
            if runtime_version != config['python_version']:
                raise ValueError('copied Python patch mismatch')
            # The system pip only installs into this new, owned environment.
            signing_bytes = signing_requirements(
                (root / 'code/tools/local_verification/requirements-extra.txt').read_bytes(),
                (root / 'code/tools/qualification_verification/signing-wheel.json').read_bytes())
            signing_path = root / 'env/signing-requirements.txt'
            with signing_path.open('xb') as output:
                output.write(signing_bytes)
            signing_path.chmod(0o400)
            execute([config['python'], '-I', '-m', 'pip', '--python', str(python),
                'install', '--require-hashes', '--only-binary=:all:', '-r', str(root / 'code/requirements-ops.lock'),
                '-r', str(signing_path)],
                capture_output=False, timeout=None)
            execute([str(python), '-I', str(root / 'code/scripts/fp.py'), '--env', str(root / 'env'), 'doctor'])
            key_code = ('from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey; '
                        'from pathlib import Path; import sys; '
                        'Path(sys.argv[1]).write_bytes(Ed25519PrivateKey.generate().private_bytes_raw())')
            for name in ('qexec', 'qg5'):
                directory = root / 'keys' / name
                directory.mkdir(mode=0o700)
                uid = manifest['roles'][name]
                os.chown(directory, uid, uid)
                key = directory / 'TEST_ONLY.key'
                execute([str(python), '-I', '-c', key_code, str(key)])
                key.chmod(0o400); os.chown(key, uid, uid)
            manifest['runtime'] = {'python': str(python), 'version': runtime_version,
                'signing_requirements_sha256': hashlib.sha256(signing_bytes).hexdigest(),
                'packages': json.loads(execute([str(python), '-I', '-c',
                    'import importlib.metadata as m, json; '
                    'print(json.dumps(sorted((d.metadata["Name"], d.version) for d in m.distributions())))']))}
            stop_process_groups(root)
            manifest['state'] = 'host_ready_boundary_unconfigured'
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
        if (manifest.get('schema') != 'qualification_host_ownership/v3'
                or manifest.get('root') != str(root) or manifest.get('run_id') != root.name
                or root.parent != Path(manifest['host_config']['parent']) or len(root.name) != 32
                or any(c not in '0123456789abcdef' for c in root.name)):
            raise ValueError('ownership identity mismatch')
        validate_resources(manifest, root)
        receipt = {'schema': 'qualification_host_cleanup/v1', 'run_id': root.name,
                   'manifest_sha256': hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
                   'removed': [], 'retained': ['ownership.json', 'evidence', 'owner.lock', 'retired.json',
                                               'process-groups.json','boundary-resources.json'],
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
            stop_process_groups(root)
            from tools.qualification_verification.campaign_host import cleanup as cleanup_campaign_host
            cleanup_campaign_host(root, manifest, retire=True)
            validate_host_executables(manifest['host_config'])
            uids = {r['id'] for r in manifest['resources'] if r['kind'] == 'user'}
            require_inactive_principals(uids)
            boundary = boundary_cleanup_plan(root,manifest)
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
                    validate_owned_user(user, item, root.name, grp.getgrall())
                elif item['kind'] == 'group':
                    try:
                        group = grp.getgrnam(item['name'])
                    except KeyError:
                        try:
                            grp.getgrgid(item['id'])
                        except KeyError:
                            continue
                        raise ValueError('GID reused')
                    if group.gr_gid != item['id'] or not set(group.gr_mem) <= owned_group_members(item['name']):
                        raise ValueError('group shared or replaced')
                    owned_users={resource['name']:resource for resource in manifest['resources'] if resource['kind']=='user'}
                    for member in group.gr_mem:
                        if member not in owned_users:
                            raise ValueError('group member is not owned by this manifest')
                        try:
                            user=pwd.getpwnam(member)
                        except KeyError as exc:
                            raise ValueError('group member identity missing') from exc
                        validate_owned_user(user,owned_users[member],root.name,grp.getgrall())
                    if any(p.pw_gid == item['id'] and p.pw_uid not in uids for p in pwd.getpwall()):
                        raise ValueError('group has unrelated consumer')
                else:
                    path = resource_path(root, item['path'])
                    validate_owned_tree(path, item['uid'], allow_initial_owner=(
                        item['path'] in ('data', 'scratch')
                        and manifest.get('state') in ('provisioning', 'setup_failed')),
                        allow_initial_venv_alias=(item['path'] == 'env'
                        and manifest.get('state') in ('provisioning', 'setup_failed')))
            # Validate everything before removing anything; never follow a link.
            docker=[manifest['host_config']['docker'],'--host','unix:///var/run/docker.sock']
            cleanup_group = create_process_group(root) if boundary['containers'] or boundary['images'] else None
            for container in boundary['containers']:
                run_owned(cleanup_group,[*docker,'rm','--force','--',container],interpreter=manifest['host_config']['python'])
                receipt['removed'].append(dict(kind='container',id=container))
            for image_id in boundary['images']:
                # No force: an unrelated remaining consumer must block retirement.
                run_owned(cleanup_group,[*docker,'image','rm','--',image_id],interpreter=manifest['host_config']['python'])
                receipt['removed'].append(dict(kind='image',id=image_id))
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
                    if cleanup_group is None:
                        cleanup_group = create_process_group(root)
                    run_owned(cleanup_group, ['/usr/sbin/userdel', item['name']],
                              interpreter=manifest['host_config']['python'])
                else:
                    try:
                        grp.getgrnam(item['name'])
                    except KeyError:
                        continue
                    if cleanup_group is None:
                        cleanup_group = create_process_group(root)
                    run_owned(cleanup_group, ['/usr/sbin/groupdel', item['name']],
                              interpreter=manifest['host_config']['python'])
                receipt['removed'].append(item)
            # The locks provide exclusivity. Atomic publication prevents a hard
            # kill from leaving a partial authoritative retirement certificate.
            stop_process_groups(root)
            save(retired, {'manifest_sha256': receipt['manifest_sha256']}, mode=0o400)
            write_reservation(reservation, None)
            receipt['ok'] = True
        except (OSError, ValueError, sqlite3.Error, subprocess.SubprocessError) as exc:
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
