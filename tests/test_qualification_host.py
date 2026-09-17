"""Host input/ownership validation must fail before making privileged changes."""
import hashlib
import errno
import importlib
import json
import stat
from contextlib import nullcontext
from pathlib import Path
import sys
import subprocess
from types import SimpleNamespace
import pytest

ROOT = Path(__file__).resolve().parents[1]


def host_module():
    name = 'tools.qualification_verification.host'
    assert importlib.util.find_spec(name), 'host provisioning is missing'
    return importlib.import_module(name)


def test_changed_lock_is_rejected_before_provisioning(tmp_path):
    host = host_module()
    (tmp_path / 'requirements-ops.lock').write_text('tampered')
    with pytest.raises(ValueError, match='lock'):
        host.validate_inputs(tmp_path, host.load_config()[0])


def test_host_config_matches_committed_lock_bytes():
    host = host_module()
    host.validate_inputs(ROOT, host.load_config()[0])


@pytest.mark.parametrize('field', ['python', 'docker'])
@pytest.mark.parametrize('value', ['python3', './docker', '/usr/../tmp/tool', '', None, 42])
def test_config_rejects_ambient_executable_selection(field, value):
    host = host_module()
    config = {**host.load_config()[0], field: value}
    with pytest.raises(ValueError, match='executable'):
        host.validate_inputs(ROOT, config)


@pytest.mark.parametrize('reject', ['parent', 'target', None])
def test_executable_requires_protected_parent_and_resolved_target(tmp_path, monkeypatch, reject):
    host = host_module()
    executable = tmp_path / 'tool.exe'
    executable.write_bytes(b'test executable')
    executable.chmod(0o755)
    checked = []
    def protection(path):
        checked.append(path)
        if path == (tmp_path if reject == 'parent' else executable if reject == 'target' else None):
            raise ValueError('unprotected path')
        return path
    monkeypatch.setattr(host, 'protected', protection)
    if reject:
        with pytest.raises(ValueError, match='unprotected'):
            host.protected_executable(str(executable))
    else:
        host.protected_executable(str(executable))
        assert tmp_path in checked and checked[-1] == executable


def test_executable_cannot_be_a_directory(tmp_path, monkeypatch):
    host = host_module()
    monkeypatch.setattr(host, 'protected', lambda path: path)
    with pytest.raises(ValueError, match='executable'):
        host.protected_executable(str(tmp_path))


@pytest.mark.parametrize('failure', ['writable-hop', 'unowned-link', 'cycle', None])
@pytest.mark.parametrize('relative', [False, True])
def test_executable_validates_intermediate_symlink_hops(tmp_path, monkeypatch, failure, relative):
    host = host_module()
    target = tmp_path / 'actual.exe'
    target.write_bytes(b'approved')
    target.chmod(0o755)
    first = tmp_path / 'bin/python'
    middle = tmp_path / 'aliases/current'
    first.parent.mkdir()
    middle.parent.mkdir()
    links = {first: middle, middle: first if failure == 'cycle' else target}
    original_stat, original_resolve = Path.lstat, Path.resolve
    # Model POSIX links where the Windows development host cannot create them;
    # the disposable-host tests exercise the same cases with real links.
    monkeypatch.setattr(Path, 'lstat', lambda path, *a, **kw:
        SimpleNamespace(st_mode=stat.S_IFLNK | 0o777,
                        st_uid=1000 if path == middle and failure == 'unowned-link' else 0)
        if path in links else original_stat(path, *a, **kw))
    monkeypatch.setattr(Path, 'resolve', lambda path, *a, **kw:
                        target if path in links else original_resolve(path, *a, **kw))
    monkeypatch.setattr(host.os, 'readlink', lambda path:
        host.os.path.relpath(links[path], path.parent) if relative else str(links[path]))
    def protected(path):
        if failure == 'writable-hop' and middle.parent in (path, *path.parents):
            raise ValueError('unprotected path')
        return path
    monkeypatch.setattr(host, 'protected', protected)
    if failure:
        with pytest.raises(ValueError, match='unprotected|symlink'):
            host.protected_executable(str(first))
    else:
        host.protected_executable(str(first))


@pytest.mark.parametrize('locks', [{}, {'requirements-ops.lock': '0' * 64},
                                    {**host_module().load_config()[0]['locks'], 'extra.lock': '0' * 64}])
def test_host_config_requires_exactly_the_consumed_locks(locks):
    host = host_module()
    config = {**host.load_config()[0], 'locks': locks}
    with pytest.raises(ValueError, match='every required lock'):
        host.validate_inputs(ROOT, config)


@pytest.mark.parametrize('relative', ['../outside', '/etc/passwd', 'data/../../outside', '.', ''])
def test_cleanup_manifest_cannot_name_escape_or_root(tmp_path, relative):
    host = host_module()
    with pytest.raises(ValueError):
        host.resource_path(tmp_path, relative)


def test_cleanup_manifest_rejects_unknown_resource_kind(tmp_path):
    host = host_module()
    with pytest.raises(ValueError, match='resource'):
        host.validate_resources({'resources': [{'kind': 'shell', 'command': 'anything'}]}, tmp_path)


def test_cleanup_manifest_rejects_duplicate_resources(tmp_path):
    host = host_module()
    with pytest.raises(ValueError, match='duplicate'):
        host.validate_resources({'resources': [
            {'kind': 'tree', 'path': 'data', 'uid': 61001},
            {'kind': 'tree', 'path': 'data', 'uid': 61001}]}, tmp_path)


def test_cleanup_tree_refuses_link_without_removing_target(tmp_path):
    host = host_module()
    target = tmp_path / 'sentinel'
    target.write_text('keep')
    tree = tmp_path / 'data'
    tree.mkdir()
    try:
        (tree / 'alias').symlink_to(target)
    except OSError:
        pytest.skip('symlink creation unavailable on this development host')
    with pytest.raises(ValueError, match='link'):
        host.inspect_tree(tree)
    assert target.read_text() == 'keep'


def test_public_observations_exclude_private_manifest_fields():
    host = host_module()
    manifest = {'run_id': 'a' * 32, 'host_config_sha256': 'b' * 64,
                'facts': {'python': '3.12.3', 'docker': {'Version': '28.0.4'}},
                'runtime': {'packages': [['cryptography', '50.0.1']]},
                'roles': {'qclient': 61000, 'qexec': 61001, 'qg5': 61002},
                'source': {'commit': 'c' * 40, 'fingerprint': 'd' * 64},
                'resources': [{'path': '/private/TEST_ONLY.key'}],
                'private_future_field': 'do not export'}
    assert hasattr(host, 'public_observations'), 'non-secret host inventory export is missing'
    report = host.public_observations(manifest)
    assert report['runtime']['packages'] == [['cryptography', '50.0.1']]
    assert report['facts']['docker']['Version'] == '28.0.4'
    assert 'resources' not in report and 'private_future_field' not in report


def test_host_facts_exports_only_opaque_inventory_ids(monkeypatch):
    host = host_module()
    config = host.load_config()[0]
    commands = []

    def observed_run(command):
        commands.append(command)
        if 'version' in command:
            return json.dumps({'Version': config['docker_version']})
        if command[0] == config['python']:
            return config['python_version']
        if command[:2] == ['/usr/bin/dpkg-query', '-W']:
            return config['docker_package_version'] if config['docker_package'] in command else ''
        return ''

    monkeypatch.setattr(host, 'administrator', lambda: None)
    monkeypatch.setattr(host, 'protected_executable', lambda value: None)
    monkeypatch.setattr(host.platform, 'freedesktop_os_release',
                        lambda: {'ID': config['os_id'], 'VERSION_ID': config['os_release']})
    monkeypatch.setattr(host.platform, 'machine', lambda: config['architecture'])
    monkeypatch.setattr(host.platform, 'release', lambda: 'test-kernel')
    monkeypatch.setattr(host, 'run', observed_run)
    host.host_facts(config)
    container_command = next(command for command in commands if 'ps' in command)
    assert container_command[-1] == '{{json .ID}}'
    assert '.Command' not in container_command[-1] and '.Labels' not in container_command[-1]
    image_command = next(command for command in commands if 'image' in command)
    assert image_command[-1] == '{{json .ID}}'


def test_cleanup_uses_retained_docker_executable(monkeypatch):
    host = host_module()
    commands = []
    monkeypatch.setattr(host, 'run', lambda command: commands.append(command) or '')
    host.boundary_containers({'docker': '/opt/qualified/docker'}, 'run-id')
    assert commands == [['/opt/qualified/docker', '--host', 'unix:///var/run/docker.sock',
                         'ps', '-aq', '--filter', 'label=fp.qualification.host=run-id']]


@pytest.mark.parametrize(('name', 'memberships'), [
    ('qclient', []), ('qg5', []), ('qexec', ['docker']), ('qexec', []),
])
def test_cleanup_accepts_only_expected_role_group_memberships(name, memberships):
    host = host_module()
    uid = host.resolve_roles(host.load_config()[0])[name]
    user = SimpleNamespace(pw_uid=uid, pw_gid=uid, pw_gecos='run')
    groups = [SimpleNamespace(gr_name=group, gr_mem=[name]) for group in memberships]
    host.validate_owned_user(user, {'kind': 'user', 'name': name, 'id': uid}, 'run', groups)


@pytest.mark.parametrize(('name', 'memberships'), [
    ('qclient', ['disk']), ('qg5', ['docker']), ('qexec', ['disk']), ('qexec', ['docker', 'disk']),
])
def test_cleanup_rejects_changed_role_group_memberships(name, memberships):
    host = host_module()
    uid = host.resolve_roles(host.load_config()[0])[name]
    user = SimpleNamespace(pw_uid=uid, pw_gid=uid, pw_gecos='run')
    groups = [SimpleNamespace(gr_name=group, gr_mem=[name]) for group in memberships]
    with pytest.raises(ValueError, match='supplementary groups'):
        host.validate_owned_user(user, {'kind': 'user', 'name': name, 'id': uid}, 'run', groups)


def test_cleanup_accepts_resolved_nondefault_identity_ids(tmp_path):
    host = host_module()
    config = {**host.load_config()[0], 'uid_start': 62000}
    manifest = {'host_config': config, 'roles': {'qclient': 62000, 'qexec': 62001, 'qg5': 62002},
                'resources': [{'kind': 'user', 'name': 'qexec', 'id': 62001},
                              {'kind': 'group', 'name': 'qexec', 'id': 62001}]}
    host.validate_resources(manifest, tmp_path)


def test_cleanup_rejects_role_id_swap_even_within_range(tmp_path):
    host = host_module()
    manifest = {'host_config': host.load_config()[0],
                'roles': {'qclient': 61000, 'qexec': 61001, 'qg5': 61002},
                'resources': [{'kind': 'user', 'name': 'qclient', 'id': 61001}]}
    with pytest.raises(ValueError, match='identity'):
        host.validate_resources(manifest, tmp_path)


def test_reservation_prevents_claiming_an_interrupted_runs_groups(tmp_path):
    host = host_module()
    assert hasattr(host, 'require_available_reservation'), 'shared durable reservation is missing'
    reservation = tmp_path / 'reservation.json'
    reservation.write_text(json.dumps({'schema': 'qualification_identity_reservation/v1',
                                       'owner': {'run_id': 'first', 'manifest': '/first/ownership.json'}}))
    with pytest.raises(ValueError, match='reserved'):
        host.require_available_reservation(reservation)


def test_old_manifest_cannot_retire_another_runs_identities(tmp_path):
    host = host_module()
    assert hasattr(host, 'require_reservation_owner'), 'reservation owner validation is missing'
    reservation = tmp_path / 'reservation.json'
    reservation.write_text(json.dumps({'schema': 'qualification_identity_reservation/v1',
                                       'owner': {'run_id': 'new', 'manifest': '/new/ownership.json'}}))
    with pytest.raises(ValueError, match='reservation owner'):
        host.require_reservation_owner(reservation, tmp_path / 'ownership.json',
                                       {'run_id': 'old', 'resources': [{'kind': 'group'}]})


@pytest.fixture
def provisioning_attempt(tmp_path, monkeypatch):
    """Exercise publication with real files, stopping before privileged creation."""
    host = host_module()
    lock_bytes = b'approved'
    locks = {relative: hashlib.sha256(lock_bytes).hexdigest() for relative in host.REQUIRED_LOCKS}
    config = {**host.load_config()[0], 'parent': str(tmp_path / 'runs'), 'locks': locks}
    config_path = tmp_path / 'tools/qualification_verification/host.json'
    config_path.parent.mkdir(parents=True)
    config_path.write_text(json.dumps(config))
    for relative in host.REQUIRED_LOCKS:
        lock = tmp_path / relative
        lock.parent.mkdir(parents=True, exist_ok=True)
        lock.write_bytes(lock_bytes)
    monkeypatch.setattr(host, 'ROOT', tmp_path)
    reservation = tmp_path / 'reservation.json'
    def missing(_):
        raise KeyError
    monkeypatch.setitem(sys.modules, 'pwd', SimpleNamespace(getpwnam=missing, getpwuid=missing))
    monkeypatch.setitem(sys.modules, 'grp', SimpleNamespace(getgrnam=missing, getgrgid=missing))
    monkeypatch.setattr(host, 'protected', lambda path: path)
    monkeypatch.setattr(host, 'host_facts', lambda config: {})
    monkeypatch.setattr(host, 'identity_reservation', lambda: nullcontext(reservation))
    monkeypatch.setattr(host, 'ownership_lock', lambda root: nullcontext())
    # Linux directory fsync is covered on the disposable host; retain actual JSON files here.
    def save(path, data, **kwargs):
        path.write_text(json.dumps(data))
    monkeypatch.setattr(host, 'save', save)
    monkeypatch.setattr(host, 'snapshot', lambda source: {'files': {
        **locks, 'tools/qualification_verification/host.json':
        hashlib.sha256(config_path.read_bytes()).hexdigest()}})
    monkeypatch.setattr(host.os, 'O_NOFOLLOW', getattr(host.os, 'O_NOFOLLOW', 0), raising=False)
    def run(command):
        if command[0] == '/usr/bin/findmnt':
            return 'ext4'
        raise ValueError('stop before identities')
    monkeypatch.setattr(host, 'run', run)
    monkeypatch.setattr(host, 'create_process_group', lambda root: root / 'fake-cgroup')
    monkeypatch.setattr(host, 'run_owned', lambda group, command, **kwargs: run(command))
    return host, config_path, reservation


def test_config_probe_drift_is_rejected_before_creating_run(provisioning_attempt, monkeypatch):
    host, config_path, reservation = provisioning_attempt
    def drift(config):
        config_path.write_text(json.dumps({**config, 'uid_start': 62000}))
        return {}
    monkeypatch.setattr(host, 'host_facts', drift)
    with pytest.raises(ValueError, match='config.*snapshot'):
        host.provision(host.ROOT)
    assert host.reservation_owner(reservation) is None
    assert not list((host.ROOT / 'runs').glob('*'))


@pytest.mark.parametrize('failure', ['existing', 'missing-parent', 'flush'])
def test_output_failure_does_not_reserve_host(provisioning_attempt, monkeypatch, failure):
    host, _, reservation = provisioning_attempt
    output = host.ROOT / 'manifest-output'
    if failure == 'existing':
        output.write_text('keep existing output')
    elif failure == 'missing-parent':
        output = host.ROOT / 'missing' / 'output'
    else:
        def fail_flush(fd):
            raise OSError('output flush failed')
        monkeypatch.setattr(host.os, 'fsync', fail_flush)
    with pytest.raises(OSError):
        host.provision(host.ROOT, manifest_output=output)
    assert host.reservation_owner(reservation) is None
    assert not list((host.ROOT / 'runs').glob('*'))
    if failure == 'existing':
        assert output.read_text() == 'keep existing output'
    else:
        assert not output.exists()


@pytest.mark.parametrize('publish_output', [False, True])
def test_setup_failure_keeps_advertised_cleanup_path(provisioning_attempt, capsys, publish_output):
    host, _, reservation = provisioning_attempt
    output = host.ROOT / 'manifest-output' if publish_output else None
    with pytest.raises(ValueError, match='stop before identities'):
        host.provision(host.ROOT, manifest_output=output)
    owner = host.reservation_owner(reservation)
    assert Path(owner['manifest']).is_file()
    assert owner['manifest'] in capsys.readouterr().out
    if output:
        assert output.read_text().strip() == owner['manifest']


@pytest.mark.parametrize('relative', ['requirements-ops.lock',
                                     'tools/qualification_verification/requirements-signing.lock'])
def test_probe_time_lock_drift_is_rejected_before_reservation(provisioning_attempt, monkeypatch, relative):
    host, config_path, reservation = provisioning_attempt
    lock = host.ROOT / relative
    lock.parent.mkdir(parents=True, exist_ok=True)
    lock.write_bytes(b'approved')
    config = json.loads(config_path.read_bytes())
    config['locks'][relative] = hashlib.sha256(b'approved').hexdigest()
    config_path.write_text(json.dumps(config))
    def drift(config):
        lock.write_bytes(b'unapproved')
        return {}
    monkeypatch.setattr(host, 'host_facts', drift)
    monkeypatch.setattr(host, 'snapshot', lambda source:
                        {'files': {name: hashlib.sha256((source / name).read_bytes()).hexdigest()
                                   for name in host.REQUIRED_LOCKS}})
    with pytest.raises(ValueError, match='lock'):
        host.provision(host.ROOT)
    assert host.reservation_owner(reservation) is None


@pytest.mark.parametrize('relative', ['requirements-ops.lock',
                                     'tools/qualification_verification/requirements-signing.lock'])
def test_staged_locks_are_checked_before_environment_activation(provisioning_attempt, monkeypatch, relative):
    host, config_path, _ = provisioning_attempt
    lock = host.ROOT / relative
    lock.parent.mkdir(parents=True, exist_ok=True)
    lock.write_bytes(b'approved')
    digest = hashlib.sha256(b'approved').hexdigest()
    config = json.loads(config_path.read_bytes())
    config['locks'][relative] = digest
    config_path.write_text(json.dumps(config))
    def snapshot(source):
        for staged in (host.ROOT / 'runs').glob('*/code/' + relative):
            staged.write_bytes(b'tampered after copy')
        return {'files': {**config['locks'], 'tools/qualification_verification/host.json':
                         hashlib.sha256(config_path.read_bytes()).hexdigest()}}
    monkeypatch.setattr(host, 'snapshot', snapshot)
    monkeypatch.setattr(host.os, 'chown', lambda *args: None, raising=False)
    def execute(group, command, **kwargs):
        assert command[0].startswith('/usr/sbin/'), 'environment activation preceded lock validation'
        return ''
    monkeypatch.setattr(host, 'run_owned', execute)
    with pytest.raises(ValueError, match='lock digest'):
        host.provision(host.ROOT)


@pytest.mark.parametrize('observed', ['3.12.3', '3.12.4', ''])
def test_copied_interpreter_is_observed_before_installation(provisioning_attempt, monkeypatch, observed):
    host, _, _ = provisioning_attempt
    commands = []
    original_snapshot = host.snapshot
    monkeypatch.setattr(host, 'snapshot', lambda source:
        {**original_snapshot(source), 'commit': 'candidate', 'fingerprint': 'snapshot'})
    monkeypatch.setattr(host.os, 'chown', lambda *args: None, raising=False)
    monkeypatch.setattr(host, 'stop_process_groups', lambda root: None)
    original_is_symlink, original_readlink = Path.is_symlink, host.os.readlink
    # Model venv's lib64 alias on Windows as well as Linux, so rejecting the
    # interpreter cannot leave an alias which manifest-scoped cleanup rejects.
    monkeypatch.setattr(Path, 'is_symlink', lambda path:
                        path.exists() if path.name == 'lib64' else original_is_symlink(path))
    monkeypatch.setattr(host.os, 'readlink', lambda path:
                        'lib' if path.name == 'lib64' else original_readlink(path))
    def execute(group, command, **kwargs):
        commands.append(command)
        if 'venv' in command:
            (Path(command[-1]) / 'lib64').write_bytes(b'lib')
        if 'import platform; print(platform.python_version())' in command:
            assert command[0].endswith('env' + host.os.sep + 'bin' + host.os.sep + 'python')
            assert not (Path(command[0]).parents[1] / 'lib64').exists()
            return observed
        if any('Ed25519PrivateKey' in arg for arg in command):
            Path(command[-1]).write_bytes(b'test-only')
        if any('importlib.metadata' in arg for arg in command):
            return '[]'
        return ''
    monkeypatch.setattr(host, 'run_owned', execute)
    if observed != '3.12.3':
        with pytest.raises(ValueError, match='Python patch mismatch'):
            host.provision(host.ROOT)
        assert not any('pip' in command for command in commands)
    else:
        manifest_path = host.provision(host.ROOT)
        manifest = json.loads(manifest_path.read_bytes())
        assert manifest['runtime']['version'] == observed
        probe = next(i for i, command in enumerate(commands)
                     if 'import platform; print(platform.python_version())' in command)
        assert probe < next(i for i, command in enumerate(commands) if 'pip' in command)


@pytest.fixture
def cleanup_attempt(provisioning_attempt, monkeypatch):
    host, _, reservation = provisioning_attempt
    with pytest.raises(ValueError, match='stop before identities'):
        host.provision(host.ROOT)
    path = Path(host.reservation_owner(reservation)['manifest'])
    manifest = json.loads(path.read_bytes())
    manifest['resources'] = []
    host.save(path, manifest)
    original_stat = Path.stat
    monkeypatch.setattr(Path, 'stat', lambda target, *a, **kw:
        SimpleNamespace(st_mode=stat.S_IFREG | 0o600) if target == path
        else original_stat(target, *a, **kw))
    monkeypatch.setattr(host, 'administrator', lambda: None)
    monkeypatch.setattr(host, 'validate_host_executables', lambda config: None)
    monkeypatch.setattr(host, 'require_inactive_principals', lambda uids: None)
    monkeypatch.setattr(host, 'boundary_containers', lambda config, run_id: '')
    return host, path, manifest, reservation


@pytest.mark.parametrize('resources', ['empty', 'tree', 'absent-accounts'])
def test_cleanup_without_account_commands_needs_no_new_cgroup(cleanup_attempt, monkeypatch, resources):
    host, path, manifest, reservation = cleanup_attempt
    if resources == 'tree':
        (path.parent / 'code').mkdir()
        manifest['resources'] = [{'kind': 'tree', 'path': 'code',
                                 'uid': (path.parent / 'code').stat().st_uid}]
    elif resources == 'absent-accounts':
        manifest['resources'] = [{'kind': 'group', 'name': 'qclient', 'id': 61000},
                                 {'kind': 'user', 'name': 'qclient', 'id': 61000}]
    host.save(path, manifest)
    def denied(root):
        raise PermissionError('cgroup creation unavailable')
    monkeypatch.setattr(host, 'create_process_group', denied)
    result = host.cleanup(path)
    assert result['ok'], result
    assert host.reservation_owner(reservation) is None
    assert not (path.parent / 'code').exists()
    assert host.cleanup(path)['already_retired']


def test_empty_registered_cgroup_without_kill_can_be_retired(tmp_path, monkeypatch):
    host = host_module()
    group = tmp_path / 'empty-group'
    group.mkdir()
    monkeypatch.setattr(host, 'process_groups', lambda root: [group])
    monkeypatch.setattr(host, 'protected', lambda path: path)
    host.stop_process_groups(tmp_path)
    assert not group.exists()


def test_populated_cgroup_without_kill_still_blocks_retirement(tmp_path, monkeypatch):
    host = host_module()
    group = tmp_path / 'populated-group'
    group.mkdir()
    monkeypatch.setattr(host, 'process_groups', lambda root: [group])
    monkeypatch.setattr(host, 'protected', lambda path: path)
    original_rmdir, original_open = Path.rmdir, Path.open
    def rmdir(path):
        if path == group:
            raise OSError(errno.EBUSY, 'populated cgroup')
        return original_rmdir(path)
    def open_file(path, *args, **kwargs):
        if path == group / 'cgroup.kill':
            raise FileNotFoundError('kill unavailable')
        return original_open(path, *args, **kwargs)
    monkeypatch.setattr(Path, 'rmdir', rmdir)
    monkeypatch.setattr(Path, 'open', open_file)
    with pytest.raises(FileNotFoundError):
        host.stop_process_groups(tmp_path)
    assert group.exists()


@pytest.mark.parametrize('exists', [False, True])
def test_child_payload_requires_successful_group_entry(tmp_path, exists):
    if exists and sys.platform != 'linux':
        pytest.skip('successful POSIX exec is verified on the disposable Linux hosts')
    host = host_module()
    group = tmp_path / 'group'
    group.mkdir()
    if exists:
        (group / 'cgroup.procs').touch()
    sentinel = tmp_path / 'payload-ran'
    command = [sys.executable, '-I', '-c',
               'from pathlib import Path; import sys; Path(sys.argv[1]).touch()', str(sentinel)]
    if exists:
        host.run_owned(group, command)
        assert (group / 'cgroup.procs').read_bytes() == b'0'
        assert sentinel.exists()
    else:
        with pytest.raises(subprocess.CalledProcessError):
            host.run_owned(group, command)
        assert not sentinel.exists()


@pytest.mark.parametrize('registry', [['../unrelated'], ['/sys/fs/cgroup'], [None], {}])
def test_process_registry_rejects_unowned_targets(tmp_path, monkeypatch, registry):
    host = host_module()
    (tmp_path / 'process-groups.json').write_text(json.dumps(registry))
    monkeypatch.setattr(host, 'protected', lambda path: path)
    with pytest.raises(ValueError, match='process group registry'):
        host.stop_process_groups(tmp_path)
