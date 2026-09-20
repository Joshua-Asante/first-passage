"""Host input/ownership validation must fail before making privileged changes."""
import hashlib
import errno
import importlib
import json
import stat
from contextlib import contextmanager, nullcontext
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


def environment_module():
    """Owns `protected` and `protected_executable`; host re-imports both by name."""
    return importlib.import_module('scripts.qualification_boundary_environment')


def test_changed_lock_is_rejected_before_provisioning(tmp_path):
    host = host_module()
    (tmp_path / 'requirements-ops.lock').write_text('tampered')
    with pytest.raises(ValueError, match='lock'):
        host.validate_inputs(tmp_path, host.load_config()[0])


def test_host_config_matches_committed_lock_bytes():
    host = host_module()
    host.validate_inputs(ROOT, host.load_config()[0])


def test_signing_installation_uses_canonical_shared_version():
    host = host_module()
    shared = (ROOT / 'tools/local_verification/requirements-extra.txt').read_bytes()
    hashes = json.dumps({'schema':'qualification_signing_wheel/v1','package':'cryptography','sha256':'a'*64}).encode()
    actual = host.signing_requirements(shared, hashes)
    pin = next(line for line in shared.decode().splitlines() if line.startswith('cryptography=='))
    assert actual == (pin + ' --hash=sha256:' + 'a'*64 + '\n').encode()
    assert host.signing_requirements(b'cryptography==99.1.2\n', hashes).startswith(b'cryptography==99.1.2 ')


@pytest.mark.parametrize('shared', [b'',b'cryptography>=1\n',b'cryptography==1.2.3\ncryptography==2.3.4\n'])
def test_signing_requirement_rejects_missing_or_ambiguous_version(shared):
    host = host_module()
    with pytest.raises(ValueError, match='canonical signing pin'):
        host.signing_requirements(shared,b'{"package":"cryptography","schema":"qualification_signing_wheel/v1","sha256":"' + b'a'*64 + b'"}')


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
    monkeypatch.setattr(environment_module(), 'protected', protection)
    if reject:
        with pytest.raises(ValueError, match='unprotected'):
            host.protected_executable(str(executable))
    else:
        host.protected_executable(str(executable))
        assert tmp_path in checked and checked[-1] == executable


def test_executable_cannot_be_a_directory(tmp_path, monkeypatch):
    host = host_module()
    monkeypatch.setattr(environment_module(), 'protected', lambda path: path)
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
    monkeypatch.setattr(environment_module(), 'protected', protected)
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
    manifest = minimal_manifest(host)
    manifest['resources'] = [{'kind': 'shell', 'command': 'anything'}]
    with pytest.raises(ValueError, match='unsupported resource'):
        host.validate_resources(manifest, tmp_path)


def tree_record(host, manifest, relative):
    """The record provisioning retains: the canonical binding resolved from the manifest roles."""
    return {'kind': 'tree', 'path': relative, **host.resolve_tree_binding(relative, manifest['roles'])}


def canonical_metadata(host, manifest, relative):
    binding = host.resolve_tree_binding(relative, manifest['roles'])
    return binding['uid'], binding['gid'], int(binding['mode'], 8)


def model_tree_metadata(monkeypatch, trees):
    """Model Linux owner/group/mode for chosen directories through the Path.stat double.

    `trees` maps a directory to (uid, gid, mode); mutate it to model a later
    metadata repair. Windows cannot create Linux owners or modes itself.
    """
    original = Path.stat
    def metadata(target, *args, **kwargs):
        if target in trees and kwargs.get('follow_symlinks') is not False:
            info = original(target, *args, **kwargs)
            uid, gid, mode = trees[target]
            return SimpleNamespace(st_uid=uid, st_gid=gid, st_mode=stat.S_IFDIR | mode, st_dev=info.st_dev)
        return original(target, *args, **kwargs)
    monkeypatch.setattr(Path, 'stat', metadata)


def minimal_manifest(host):
    config = host.load_config()[0]
    return {'host_config': config, 'roles': host.resolve_roles(config),
            'tree_bindings': host.tree_bindings_identity(), 'resources': []}


def test_cleanup_manifest_rejects_duplicate_resources(tmp_path):
    host = host_module()
    manifest = minimal_manifest(host)
    manifest['resources'] = [tree_record(host, manifest, 'data'), tree_record(host, manifest, 'data')]
    with pytest.raises(ValueError, match='duplicate'):
        host.validate_resources(manifest, tmp_path)


def test_tree_bindings_are_resolved_from_one_canonical_table():
    host = host_module()
    roles = {'qclient': 61000, 'qexec': 61001, 'qg5': 61002}
    assert host.TREES == ('code', 'env', 'data', 'keys', 'scratch')
    assert host.resolve_tree_binding('data', roles) == {'uid': 61001, 'gid': 61001, 'mode': '0700'}
    assert host.resolve_tree_binding('scratch', roles) == {'uid': 61001, 'gid': 61001, 'mode': '0700'}
    for administered in ('code', 'env', 'keys'):
        assert host.resolve_tree_binding(administered, roles) == {'uid': 0, 'gid': 0, 'mode': '0755'}
    with pytest.raises(KeyError):
        host.resolve_tree_binding('evidence', roles)
    identity = host.tree_bindings_identity()
    assert identity['schema'] == 'qualification_tree_bindings/v1'
    assert len(identity['sha256']) == 64 and identity == host.tree_bindings_identity()


def test_tree_bindings_identity_is_derived_from_the_canonical_table(monkeypatch):
    from tools.qualification_verification import role_policy
    table = {name: [owner, group, format(mode, '04o')]
             for name, (owner, group, mode) in role_policy.TREE_BINDINGS.items()}
    expected = hashlib.sha256(json.dumps(table, sort_keys=True).encode()).hexdigest()
    assert role_policy.tree_bindings_identity()['sha256'] == expected
    # An unbumped edit to the table changes the identity, so retained manifests no longer match it.
    edited = dict(role_policy.TREE_BINDINGS)
    edited['data'] = ('qexec', 'qexec', 0o770)
    monkeypatch.setattr(role_policy, 'TREE_BINDINGS', edited)
    assert role_policy.tree_bindings_identity()['sha256'] != expected


REJECTIONS = {'missing-mode': 'invalid tree resource', 'extra-field': 'invalid tree resource',
              'integer-mode': 'invalid tree resource', 'short-mode': 'inconsistent tree binding',
              'boolean-uid': 'invalid tree resource', 'unknown-path': 'invalid tree resource',
              'weakened-gid': 'inconsistent tree binding', 'weakened-mode': 'inconsistent tree binding',
              'identity-digest': 'tree binding configuration mismatch',
              'identity-schema': 'tree binding configuration mismatch',
              'mixed-legacy': 'invalid tree resource', 'roles': 'roles do not match'}


@pytest.mark.parametrize('tamper', sorted(REJECTIONS))
def test_cleanup_rejects_malformed_or_inconsistent_tree_bindings(tmp_path, tamper):
    """A retained binding must equal the canonical resolution; the filesystem never vouches for it."""
    host = host_module()
    manifest = minimal_manifest(host)
    # False == 0 and True == 1 under ==; a boolean must still be rejected by type.
    item = tree_record(host, manifest, 'code' if tamper == 'boolean-uid' else 'data')
    if tamper == 'missing-mode':
        del item['mode']
    elif tamper == 'extra-field':
        item['sticky'] = False
    elif tamper == 'integer-mode':
        item['mode'] = 0o700
    elif tamper == 'short-mode':
        item['mode'] = '700'
    elif tamper == 'boolean-uid':
        item['uid'] = False
    elif tamper == 'unknown-path':
        item['path'] = 'evidence'
    elif tamper == 'weakened-gid':
        item['gid'] = manifest['roles']['qclient']
    elif tamper == 'weakened-mode':
        item['mode'] = '0770'
    elif tamper == 'identity-digest':
        manifest['tree_bindings'] = {**manifest['tree_bindings'], 'sha256': 'f' * 64}
    elif tamper == 'identity-schema':
        manifest['tree_bindings'] = {**manifest['tree_bindings'], 'schema': 'qualification_tree_bindings/v0'}
    elif tamper == 'mixed-legacy':
        manifest['resources'].append({'kind': 'tree', 'path': 'code', 'uid': 0})
    elif tamper == 'roles':
        manifest['roles'] = {**manifest['roles'], 'qexec': manifest['roles']['qexec'] + 1}
    manifest['resources'].insert(0, item)
    with pytest.raises(ValueError, match=REJECTIONS[tamper]):
        host.validate_resources(manifest, tmp_path)


def test_legacy_manifest_records_are_accepted_only_in_their_exact_historical_shape(tmp_path):
    host = host_module()
    manifest = minimal_manifest(host)
    del manifest['tree_bindings']
    manifest['resources'] = [{'kind': 'tree', 'path': 'data', 'uid': manifest['roles']['qexec']},
                             {'kind': 'tree', 'path': 'code', 'uid': 0}]
    assert host.validate_resources(manifest, tmp_path) == ['data', 'code']
    manifest['resources'].append(tree_record(host, manifest, 'keys'))
    with pytest.raises(ValueError, match='invalid tree resource'):
        host.validate_resources(manifest, tmp_path)
    # The producer's owner for each path is known; a foreign or non-integer owner is not authority.
    for uid in (0, manifest['roles']['qclient']):
        manifest['resources'] = [{'kind': 'tree', 'path': 'data', 'uid': uid}]
        with pytest.raises(ValueError, match='inconsistent tree resource'):
            host.validate_resources(manifest, tmp_path)
    # False == 0 and 0.0 == 0 by value: only the type guard rejects them on a root-owned tree.
    for uid in (False, 0.0):
        manifest['resources'] = [{'kind': 'tree', 'path': 'code', 'uid': uid}]
        with pytest.raises(ValueError, match='inconsistent tree resource'):
            host.validate_resources(manifest, tmp_path)


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
    host.boundary_containers({'docker': '/opt/qualified/docker'}, 'a'*32)
    assert commands == [['/opt/qualified/docker', '--host', 'unix:///var/run/docker.sock',
                         'ps', '-aq', '--no-trunc', '--filter', 'label=fp.qualification.host='+'a'*32]]


@pytest.mark.parametrize(('name', 'memberships'), [
    ('qclient', []), ('qg5', []), ('qg5',['qclient']), ('qexec', ['docker']), ('qexec', []),
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
    lock_payloads = {relative:(ROOT / relative).read_bytes() for relative in host.REQUIRED_LOCKS}
    locks = {relative: hashlib.sha256(raw).hexdigest() for relative,raw in lock_payloads.items()}
    config = {**host.load_config()[0], 'parent': str(tmp_path / 'runs'), 'locks': locks}
    config_path = tmp_path / 'tools/qualification_verification/host.json'
    config_path.parent.mkdir(parents=True)
    config_path.write_text(json.dumps(config))
    for relative in host.REQUIRED_LOCKS:
        lock = tmp_path / relative
        lock.parent.mkdir(parents=True, exist_ok=True)
        lock.write_bytes(lock_payloads[relative])
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
    original_iterdir = Path.iterdir
    monkeypatch.setattr(Path, 'iterdir', lambda path:
                        iter(()) if path == Path('/proc') else original_iterdir(path))
    return host, config_path, reservation


@pytest.mark.parametrize('role', ['qclient', 'qexec', 'qg5'])
@pytest.mark.parametrize('uid_field', range(4))
def test_provision_refuses_live_role_uid_before_publication(
        provisioning_attempt, monkeypatch, role, uid_field):
    host, config_path, reservation = provisioning_attempt
    config = json.loads(config_path.read_bytes())
    config['uid_start'] = 62000
    config_path.write_text(json.dumps(config))
    uid = {'qclient': 62000, 'qexec': 62001, 'qg5': 62002}[role]
    process = host.ROOT / 'proc/123'
    process.mkdir(parents=True)
    uids = [0, 0, 0, 0]
    uids[uid_field] = uid
    (process / 'status').write_text('Name:\tlingering\nUid:\t' + '\t'.join(map(str, uids)) + '\n')
    locked = False
    @contextmanager
    def reservation_lock():
        nonlocal locked
        locked = True
        try:
            yield reservation
        finally:
            locked = False
    original_iterdir = Path.iterdir
    def iterdir(path):
        if path == Path('/proc'):
            assert locked, 'live UID check must hold the host-wide identity lock'
            return iter([process])
        return original_iterdir(path)
    monkeypatch.setattr(Path, 'iterdir', iterdir)
    monkeypatch.setattr(host, 'identity_reservation', reservation_lock)
    output = host.ROOT / 'manifest-output'
    with pytest.raises(ValueError, match='active test principal'):
        host.provision(host.ROOT, manifest_output=output)
    assert not (host.ROOT / 'runs').exists()
    assert not output.exists()
    assert host.reservation_owner(reservation) is None


def test_provision_ignores_unrelated_and_exited_processes(provisioning_attempt, monkeypatch):
    host, _, _ = provisioning_attempt
    process = host.ROOT / 'proc/123'
    process.mkdir(parents=True)
    (process / 'status').write_text('Uid:\t61999\t61999\t61999\t61999\n')
    original_iterdir = Path.iterdir
    monkeypatch.setattr(Path, 'iterdir', lambda path:
                        iter([process, process.parent / '124']) if path == Path('/proc')
                        else original_iterdir(path))
    with pytest.raises(ValueError, match='stop before identities'):
        host.provision(host.ROOT)


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
                                     'tools/local_verification/requirements-extra.txt', 'tools/qualification_verification/signing-wheel.json'])
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
                                     'tools/local_verification/requirements-extra.txt', 'tools/qualification_verification/signing-wheel.json'])
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
        manifest['resources'] = [tree_record(host, manifest, 'code')]
        model_tree_metadata(monkeypatch, {path.parent / 'code': canonical_metadata(host, manifest, 'code')})
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


def test_cleanup_docker_mutations_join_owned_cgroup(cleanup_attempt,monkeypatch):
    host,path,_,_=cleanup_attempt
    group=path.parent/'cleanup-group'
    calls=[]
    monkeypatch.setattr(host,'boundary_cleanup_plan',lambda *args:dict(containers=['a'*64],images=['sha256:'+'b'*64]))
    monkeypatch.setattr(host,'create_process_group',lambda root:group)
    monkeypatch.setattr(host,'run_owned',lambda owner,command,**kwargs:calls.append((owner,command)))
    result=host.cleanup(path)
    assert result['ok']
    assert len(calls)==2 and all(owner==group for owner,_ in calls)
    assert calls[0][1][-3:]==['--force','--','a'*64]
    assert calls[1][1][-3:]==['rm','--','sha256:'+'b'*64]


def test_cleanup_group_member_requires_manifest_owned_account(cleanup_attempt,monkeypatch):
    host,path,manifest,_=cleanup_attempt
    manifest['resources']=[dict(kind='group',name='qclient',id=61000)]
    host.save(path,manifest)
    group=SimpleNamespace(gr_name='qclient',gr_gid=61000,gr_mem=['qg5'])
    monkeypatch.setattr(sys.modules['grp'],'getgrnam',lambda name:group)
    monkeypatch.setattr(sys.modules['pwd'],'getpwall',lambda:[],raising=False)
    removed=[]
    monkeypatch.setattr(host,'run_owned',lambda *args,**kwargs:removed.append(args))
    result=host.cleanup(path)
    assert not result['ok'] and not removed
    assert 'member' in ' '.join(result['failures'])


def failure_receipts(root):
    return [json.loads(p.read_text()) for p in sorted(root.glob('cleanup-*.json'))]


def first_mismatch(observed, binding):
    """The validator names the first differing field in uid, gid, mode order."""
    names = ('owner', 'group', 'mode')
    return next(name for name, a, b in zip(names, observed, binding) if a != b)


@pytest.mark.parametrize('relative', ['code', 'env', 'data', 'keys', 'scratch'])
@pytest.mark.parametrize('state', ['provisioning', 'setup_failed'])
@pytest.mark.parametrize('drift', [None, 'owner', 'group', 'restrictive-umask', 'contents', 'ready'])
def test_cleanup_recovers_only_the_empty_initial_tree(cleanup_attempt, monkeypatch, relative, state, drift):
    """mkdir(0o700) precedes chmod/chown; only that exact intermediate is retirable on retry."""
    host, path, manifest, reservation = cleanup_attempt
    tree = path.parent / relative
    tree.mkdir(mode=0o700)
    if drift == 'contents':
        (tree / 'unexpected').write_text('retain')
    manifest['state'] = 'host_ready_boundary_unconfigured' if drift == 'ready' else state
    manifest['resources'] = [tree_record(host, manifest, relative)]
    host.save(path, manifest)
    # Windows cannot create Linux owners/modes. Keep real files and cleanup;
    # model only the metadata left between the privileged mkdir and chown.
    observed = (61000 if drift == 'owner' else 0, 61000 if drift == 'group' else 0,
                0o750 if drift == 'restrictive-umask' else 0o700)
    model_tree_metadata(monkeypatch, {tree: observed})
    result = host.cleanup(path)
    if drift is None:
        assert result['ok'], result
        assert not tree.exists()
        assert host.reservation_owner(reservation) is None
        assert host.cleanup(path)['already_retired']
    else:
        assert not result['ok']
        assert tree.exists()
        assert host.reservation_owner(reservation) is not None
        assert not (path.parent / 'retired.json').exists()
        field = first_mismatch(observed, canonical_metadata(host, manifest, relative))
        assert result['failures'] == ['ValueError: tree ' + field + ' mismatch']


@pytest.mark.parametrize('relative', ['data', 'scratch', 'code'])
@pytest.mark.parametrize('drift', [None, 'owner', 'group', 'mode', 'setgid'])
def test_cleanup_rejects_completed_tree_binding_drift_and_recovers_after_repair(
        cleanup_attempt, monkeypatch, relative, drift):
    """A ready host's tree must match its retained uid, gid and mode exactly before recursive deletion."""
    host, path, manifest, reservation = cleanup_attempt
    tree = path.parent / relative
    tree.mkdir()
    (tree / 'placed-later').write_text('retain')
    manifest['state'] = 'host_ready_boundary_unconfigured'
    manifest['resources'] = [tree_record(host, manifest, relative)]
    host.save(path, manifest)
    uid, gid, mode = canonical_metadata(host, manifest, relative)
    drifted = {'owner': (manifest['roles']['qclient'], gid, mode), 'group': (uid, manifest['roles']['qclient'], mode),
               'mode': (uid, gid, mode | 0o070), 'setgid': (uid, gid, mode | stat.S_ISGID)}
    trees = {tree: drifted.get(drift, (uid, gid, mode))}
    model_tree_metadata(monkeypatch, trees)
    result = host.cleanup(path)
    if drift is None:
        assert result['ok'], result
        assert not tree.exists()
        assert host.reservation_owner(reservation) is None
        return
    field = first_mismatch(trees[tree], (uid, gid, mode))
    assert not result['ok']
    assert result['failures'] == ['ValueError: tree ' + field + ' mismatch']
    assert (tree / 'placed-later').read_text() == 'retain'
    assert host.reservation_owner(reservation) == {'run_id': path.parent.name, 'manifest': str(path)}
    assert not (path.parent / 'retired.json').exists()
    assert [receipt['ok'] for receipt in failure_receipts(path.parent)] == [False]
    # Restore the canonical metadata: cleanup succeeds once and stays idempotent.
    trees[tree] = (uid, gid, mode)
    repaired = host.cleanup(path)
    assert repaired['ok'], repaired
    assert not tree.exists()
    assert host.reservation_owner(reservation) is None
    assert host.cleanup(path)['already_retired']


@pytest.mark.parametrize('drift', [None, 'group', 'mode', 'owner'])
def test_legacy_manifest_retires_on_producer_owner_and_group_only(cleanup_attempt, monkeypatch, drift):
    """Pre-binding v3 records: the producer set gid == uid; the mode was never recorded."""
    host, path, manifest, reservation = cleanup_attempt
    tree = path.parent / 'data'
    tree.mkdir()
    (tree / 'run-owned').write_text('legacy')
    manifest['state'] = 'host_ready_boundary_unconfigured'
    del manifest['tree_bindings']
    manifest['resources'] = [{'kind': 'tree', 'path': 'data', 'uid': manifest['roles']['qexec']},
                             {'kind': 'tree', 'path': 'code', 'uid': 0}]
    host.save(path, manifest)
    uid = manifest['roles']['qexec']
    model_tree_metadata(monkeypatch, {tree: (manifest['roles']['qclient'] if drift == 'owner' else uid,
                                             manifest['roles']['qclient'] if drift == 'group' else uid,
                                             0o770 if drift == 'mode' else 0o700)})
    result = host.cleanup(path)
    if drift in ('owner', 'group'):
        assert not result['ok']
        assert result['failures'] == ['ValueError: tree ' + drift + ' mismatch']
        assert (tree / 'run-owned').exists()
        assert host.reservation_owner(reservation) is not None
        assert not (path.parent / 'retired.json').exists()
        return
    assert result['ok'], result
    assert result['legacy_tree_bindings'] == ['data', 'code']
    assert not tree.exists()
    assert host.cleanup(path)['already_retired']


def test_weakened_binding_matching_the_filesystem_is_a_recorded_refusal(cleanup_attempt, monkeypatch):
    """An edited record is refused before validation of the tree, with a receipt and nothing touched."""
    host, path, manifest, reservation = cleanup_attempt
    tree = path.parent / 'data'
    tree.mkdir()
    (tree / 'placed-later').write_text('retain')
    manifest['state'] = 'host_ready_boundary_unconfigured'
    weakened = {**tree_record(host, manifest, 'data'), 'gid': manifest['roles']['qclient'], 'mode': '0770'}
    manifest['resources'] = [weakened]
    host.save(path, manifest)
    model_tree_metadata(monkeypatch, {tree: (weakened['uid'], weakened['gid'], 0o770)})
    result = host.cleanup(path)
    assert not result['ok']
    assert result['failures'] == ['ValueError: inconsistent tree binding']
    assert (tree / 'placed-later').read_text() == 'retain'
    assert host.reservation_owner(reservation) is not None
    assert not (path.parent / 'retired.json').exists()
    assert [receipt['ok'] for receipt in failure_receipts(path.parent)] == [False]


def test_cleanup_is_idempotent_over_recorded_but_absent_and_partially_removed_trees(cleanup_attempt, monkeypatch):
    host, path, manifest, reservation = cleanup_attempt
    manifest['state'] = 'host_ready_boundary_unconfigured'
    manifest['resources'] = [tree_record(host, manifest, name) for name in host.TREES]
    host.save(path, manifest)
    # A crash after the record but before mkdir leaves no path; an interrupted
    # deletion leaves some trees gone. Both retire the remainder.
    present = {name: path.parent / name for name in ('env', 'keys')}
    for tree in present.values():
        tree.mkdir()
    model_tree_metadata(monkeypatch, {tree: canonical_metadata(host, manifest, name)
                                      for name, tree in present.items()})
    result = host.cleanup(path)
    assert result['ok'], result
    removed = [item['path'] for item in result['removed'] if item['kind'] == 'tree']
    assert removed == ['scratch', 'keys', 'data', 'env', 'code']
    assert not any(tree.exists() for tree in present.values())
    assert host.reservation_owner(reservation) is None
    replacement = {'run_id': 'b' * 32, 'manifest': str(path.parent.parent / ('b' * 32) / 'ownership.json')}
    host.write_reservation(reservation, replacement)
    assert host.cleanup(path)['already_retired']
    assert host.reservation_owner(reservation) == replacement


def test_provisioning_retains_the_binding_that_cleanup_validates(provisioning_attempt, monkeypatch):
    """Record → mkdir(0o700) → chmod → chown, and the retained record is the canonical resolution."""
    host, _, reservation = provisioning_attempt
    def run_owned(group, command, **kwargs):
        if command[0] in ('/usr/sbin/groupadd', '/usr/sbin/useradd', '/usr/sbin/usermod'):
            return ''
        raise ValueError('stop before the environment')
    monkeypatch.setattr(host, 'run_owned', run_owned)
    created, applied = [], []
    original_mkdir = host.os.mkdir
    def mkdir(target, mode=0o777, **kwargs):
        target = Path(target)
        if target.name in host.TREES and (target.parent / 'ownership.json').exists():
            recorded = json.loads((target.parent / 'ownership.json').read_text())['resources']
            assert any(item['kind'] == 'tree' and item['path'] == target.name
                       for item in recorded), 'the durable record precedes creation'
            created.append((target.name, mode))
        return original_mkdir(target, mode, **kwargs)
    monkeypatch.setattr(host.os, 'mkdir', mkdir)
    monkeypatch.setattr(host.os, 'chmod', lambda target, mode: applied.append(('chmod', Path(target).name, mode)))
    def chown(target, uid, gid):
        applied.append(('chown', Path(target).name, uid, gid))
    monkeypatch.setattr(host.os, 'chown', chown, raising=False)
    original_path_mkdir = Path.mkdir
    def stop_after_trees(target, *args, **kwargs):
        if target.name == 'evidence':
            raise ValueError('stop after the trees')
        return original_path_mkdir(target, *args, **kwargs)
    monkeypatch.setattr(Path, 'mkdir', stop_after_trees)
    with pytest.raises(ValueError, match='stop after the trees'):
        host.provision(host.ROOT)
    path = Path(host.reservation_owner(reservation)['manifest'])
    manifest = json.loads(path.read_text())
    assert manifest['state'] == 'setup_failed'
    assert manifest['tree_bindings'] == host.tree_bindings_identity()
    assert [item for item in manifest['resources'] if item['kind'] == 'tree'] == [
        tree_record(host, manifest, name) for name in host.TREES]
    assert created == [(name, 0o700) for name in host.TREES]
    expected = []
    for name in host.TREES:
        binding = host.resolve_tree_binding(name, manifest['roles'])
        expected += [('chmod', name, int(binding['mode'], 8)), ('chown', name, binding['uid'], binding['gid'])]
    assert applied == expected
    # The same records now drive cleanup of the interrupted host.
    monkeypatch.setattr(Path, 'mkdir', original_path_mkdir)
    monkeypatch.setattr(host, 'administrator', lambda: None)
    monkeypatch.setattr(host, 'validate_host_executables', lambda config: None)
    monkeypatch.setattr(host, 'require_inactive_principals', lambda uids: None)
    monkeypatch.setattr(host, 'boundary_containers', lambda config, run_id: '')
    original_stat = Path.stat
    monkeypatch.setattr(Path, 'stat', lambda target, *a, **kw:
        SimpleNamespace(st_mode=stat.S_IFREG | 0o600) if target == path else original_stat(target, *a, **kw))
    trees = {path.parent / name: canonical_metadata(host, manifest, name) for name in host.TREES}
    model_tree_metadata(monkeypatch, trees)
    result = host.cleanup(path)
    assert result['ok'], result
    assert not any(tree.exists() for tree in trees)
    assert host.reservation_owner(reservation) is None


@pytest.mark.parametrize('umask', [0o000, 0o022, 0o027, 0o077])
def test_tree_creation_accepts_every_owner_preserving_umask(tmp_path, monkeypatch, umask):
    host = host_module()
    monkeypatch.setattr(host.os, 'umask', lambda mask: umask)
    host.require_deterministic_tree_creation(tmp_path)


@pytest.mark.parametrize('condition', ['umask-0177', 'umask-0277', 'umask-0477', 'setgid-parent'])
def test_provisioning_refuses_environments_with_an_unattributable_intermediate(
        provisioning_attempt, monkeypatch, condition):
    host, _, reservation = provisioning_attempt
    parent = host.ROOT / 'runs'
    if condition.startswith('umask'):
        monkeypatch.setattr(host.os, 'umask', lambda mask, masked=int(condition[6:], 8): masked)
    else:
        original_stat = Path.stat
        monkeypatch.setattr(Path, 'stat', lambda target, *a, **kw:
            SimpleNamespace(st_mode=stat.S_IFDIR | stat.S_ISGID | 0o755, st_uid=0, st_gid=0)
            if target == parent else original_stat(target, *a, **kw))
    with pytest.raises(ValueError, match='umask|setgid'):
        host.provision(host.ROOT)
    assert not any(parent.iterdir()), 'nothing is created before the precondition holds'
    assert host.reservation_owner(reservation) is None


def test_empty_registered_cgroup_without_kill_can_be_retired(tmp_path, monkeypatch):
    host = host_module()
    group = tmp_path / 'empty-group'
    group.mkdir()
    monkeypatch.setattr(host, 'process_groups', lambda root: [group])
    monkeypatch.setattr(host, 'protected', lambda path: path)
    host.stop_process_groups(tmp_path)
    assert not group.exists()


@pytest.mark.parametrize('drift', [None, 'target', 'owner', 'group', 'name', 'ready'])
def test_cleanup_recovers_only_initial_venv_alias(cleanup_attempt, monkeypatch, drift):
    host, path, manifest, reservation = cleanup_attempt
    env = path.parent / 'env'
    env.mkdir()
    (env / 'lib').mkdir()
    alias = env / ('other' if drift == 'name' else 'lib64')
    # Model symlink metadata for Windows; Linux host tests use a real venv.
    alias.write_text('alias')
    manifest['state'] = 'host_ready_boundary_unconfigured' if drift == 'ready' else 'provisioning'
    manifest['resources'] = [tree_record(host, manifest, 'env')]
    host.save(path, manifest)
    model_tree_metadata(monkeypatch, {env: canonical_metadata(host, manifest, 'env')})
    original_lstat, original_readlink = Path.lstat, host.os.readlink
    monkeypatch.setattr(Path, 'lstat', lambda target:
        SimpleNamespace(st_mode=stat.S_IFLNK | 0o777,
            st_uid=61000 if drift == 'owner' else 0,
            st_gid=61000 if drift == 'group' else 0) if target == alias
        else original_lstat(target))
    monkeypatch.setattr(host.os, 'readlink', lambda target:
        ('../outside' if drift == 'target' else 'lib') if target == alias
        else original_readlink(target))
    result = host.cleanup(path)
    if drift is None:
        assert result['ok'], result
        assert not env.exists()
        assert host.reservation_owner(reservation) is None
        assert host.cleanup(path)['already_retired']
    else:
        assert not result['ok']
        assert alias.exists()
        assert host.reservation_owner(reservation) is not None


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
