"""Host input/ownership validation must fail before making privileged changes."""
import hashlib
import importlib
import json
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
    config = {**host.load_config()[0], 'parent': str(tmp_path / 'runs'), 'locks': {}}
    config_path = tmp_path / 'tools/qualification_verification/host.json'
    config_path.parent.mkdir(parents=True)
    config_path.write_text(json.dumps(config))
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
    monkeypatch.setattr(host, 'snapshot', lambda source: {'files': {}})
    monkeypatch.setattr(host.os, 'O_NOFOLLOW', getattr(host.os, 'O_NOFOLLOW', 0), raising=False)
    def run(command):
        if command[0] == '/usr/bin/findmnt':
            return 'ext4'
        raise ValueError('stop before identities')
    monkeypatch.setattr(host, 'run', run)
    monkeypatch.setattr(host, 'create_process_group', lambda root: root / 'fake-cgroup')
    monkeypatch.setattr(host, 'run_owned', lambda group, command, **kwargs: run(command))
    return host, config_path, reservation


def test_manifest_hash_describes_loaded_config_during_host_probe_drift(provisioning_attempt, monkeypatch):
    host, config_path, _ = provisioning_attempt
    original = config_path.read_bytes()
    def drift(config):
        config_path.write_text(json.dumps({**config, 'uid_start': 62000}))
        return {}
    monkeypatch.setattr(host, 'host_facts', drift)
    with pytest.raises(ValueError, match='stop before identities'):
        host.provision(host.ROOT)
    manifest = json.loads(next((host.ROOT / 'runs').glob('*/ownership.json')).read_bytes())
    assert manifest['host_config'] == json.loads(original)
    assert manifest['host_config_sha256'] == hashlib.sha256(original).hexdigest()


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
    config['locks'] = {relative: hashlib.sha256(b'approved').hexdigest()}
    config_path.write_text(json.dumps(config))
    def drift(config):
        lock.write_bytes(b'unapproved')
        return {}
    monkeypatch.setattr(host, 'host_facts', drift)
    monkeypatch.setattr(host, 'snapshot', lambda source:
                        {'files': {relative: hashlib.sha256(lock.read_bytes()).hexdigest()}})
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
    config['locks'] = {relative: digest}
    config_path.write_text(json.dumps(config))
    def snapshot(source):
        for staged in (host.ROOT / 'runs').glob('*/code/' + relative):
            staged.write_bytes(b'tampered after copy')
        return {'files': {relative: digest}}
    monkeypatch.setattr(host, 'snapshot', snapshot)
    monkeypatch.setattr(host.os, 'chown', lambda *args: None, raising=False)
    def execute(group, command, **kwargs):
        assert command[0].startswith('/usr/sbin/'), 'environment activation preceded lock validation'
        return ''
    monkeypatch.setattr(host, 'run_owned', execute)
    with pytest.raises(ValueError, match='lock digest'):
        host.provision(host.ROOT)


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
