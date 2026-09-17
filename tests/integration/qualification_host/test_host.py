"""Real Linux UID probes. No boundary service/worker acceptance is claimed."""
import json
import os
from pathlib import Path
import subprocess
import sys
import pytest
from scripts.qualification_boundary_environment import identities, permissions, protected, trusted_roots
from tools.qualification_verification.host import cleanup, inspect_tree, require_inactive_principals, validate_owned_tree, run


@pytest.fixture(scope='module')
def installed():
    name = os.environ.get('FP_QUALIFICATION_HOST_MANIFEST')
    if not name:
        pytest.skip('requires explicit disposable administrator host run')
    if sys.platform != 'linux' or os.geteuid() != 0:
        pytest.fail('Linux administrator required; critical host run cannot skip')
    path = protected(Path(name))
    manifest = json.loads(path.read_bytes())
    root = path.parent
    doc = {'roles': manifest['roles'], 'data': str(root / 'data'),
           'execution_key': str(root / 'keys/qexec/TEST_ONLY.key'),
           'result_key': str(root / 'keys/qg5/TEST_ONLY.key'),
           'docker_socket': '/var/run/docker.sock', 'scratch': str(root / 'scratch'),
           'trusted_roots': [str(root / 'code'), str(root / 'env')]}
    return path, manifest, doc


def test_real_distinct_uids_and_denied_permissions(installed):
    _, _, doc = installed
    roles = identities(doc)
    report = permissions(doc, roles)
    assert report['ok'], report
    assert len({p['uid'] for p in report['probes']}) == 3
    assert sum(not p['allowed'] for p in report['probes']) == 10
    # Public evidence contains UIDs/groups/path/access outcomes, never key bytes.
    root = installed[0].parent
    (root / 'evidence/permission-observations.json').write_text(json.dumps(report, indent=2))


def test_permission_weakening_is_detected(installed):
    path, _, doc = installed
    data = path.parent / 'data'
    original = data.stat().st_mode & 0o777
    try:
        data.chmod(0o777)
        report = permissions(doc, identities(doc))
        assert not report['ok']
        assert any(p['role'] == 'qclient' and p['action'] == 'write' and p['allowed']
                   for p in report['probes'])
    finally:
        data.chmod(original)


def test_installed_source_and_runtime_are_protected(installed):
    path, manifest, doc = installed
    assert trusted_roots(doc)
    observations = json.loads((path.parent / 'evidence/host-observations.json').read_bytes())
    assert observations['source_commit'] == manifest['source']['commit']
    assert observations['runtime']['packages'] == manifest['runtime']['packages']
    assert observations['facts']['docker']['Version'] == '28.0.4'
    import hashlib
    for relative, expected in manifest['source']['files'].items():
        if expected == 'deleted':
            assert not (path.parent / 'code' / relative).exists()
            continue
        assert hashlib.sha256((path.parent / 'code' / relative).read_bytes()).hexdigest() == expected
    output = run([str(path.parent / 'env/bin/python'), '-I', str(path.parent / 'code/scripts/fp.py'),
                  '--env', str(path.parent / 'env'), 'doctor'])
    assert 'Locked packages matched:' in output


def test_cleanup_refuses_active_uid_and_preserves_sentinel(installed):
    path, manifest, _ = installed
    uid = manifest['roles']['qclient']
    def drop():
        os.setgroups([]); os.setgid(uid); os.setuid(uid)
    process = subprocess.Popen(['/usr/bin/sleep', '30'], preexec_fn=drop)
    sentinel = path.parent / 'evidence/unrelated-sentinel'
    sentinel.write_text('retain')
    try:
        with pytest.raises(ValueError, match='active test principal'):
            require_inactive_principals({uid})
        with pytest.raises(BlockingIOError):
            cleanup(path)
        assert sentinel.read_text() == 'retain'
        assert (path.parent / 'keys/qexec/TEST_ONLY.key').exists()
    finally:
        process.terminate(); process.wait(timeout=5)


def test_cleanup_refuses_symlink_escape(installed):
    path, _, _ = installed
    sentinel = path.parent / 'evidence/unrelated-sentinel'
    sentinel.write_text('retain')
    alias = path.parent / 'data/escape'
    alias.symlink_to(sentinel)
    try:
        with pytest.raises(ValueError, match='link'):
            inspect_tree(path.parent / 'data')
        assert sentinel.read_text() == 'retain'
    finally:
        alias.unlink()


def test_cleanup_refuses_wrong_tree_owner(installed):
    path, manifest, _ = installed
    data = path.parent / 'data'
    os.chown(data, manifest['roles']['qclient'], manifest['roles']['qclient'])
    try:
        with pytest.raises(ValueError, match='owner mismatch'):
            validate_owned_tree(data, manifest['roles']['qexec'])
    finally:
        uid = manifest['roles']['qexec']
        os.chown(data, uid, uid)

@pytest.fixture
def owned_cleanup_fixture(installed, monkeypatch):
    """Real disposable files/locks, no additional identities or authority keys."""
    import shutil
    from uuid import uuid4
    from tools.qualification_verification import host
    parent = installed[0].parent.parent
    root = parent / uuid4().hex
    root.mkdir(mode=0o711)
    state = root / 'reservation-state'
    monkeypatch.setattr(host, 'IDENTITY_STATE', state)
    config = {**installed[1]['host_config'], 'uid_start': 62000}
    manifest = {'schema': 'qualification_host_ownership/v2', 'run_id': root.name,
                'root': str(root), 'host_config': config, 'roles': host.resolve_roles(config),
                'resources': []}
    path = root / 'ownership.json'
    host.save(path, manifest, exclusive=True)
    with host.identity_reservation() as reservation:
        host.write_reservation(reservation, {'run_id': root.name, 'manifest': str(path)})
    try:
        yield host, root, path, manifest
    finally:
        assert root.parent == parent and root.resolve() == root
        host.inspect_tree(root)
        shutil.rmtree(root)


def test_cleanup_reads_manifest_after_obtaining_locks(owned_cleanup_fixture, monkeypatch):
    from contextlib import contextmanager
    host, root, path, manifest = owned_cleanup_fixture
    original_lock = host.ownership_lock
    @contextmanager
    def complete_provision_before_lock(target):
        if target == root and not manifest['resources']:
            (root / 'code').mkdir()
            (root / 'code/owned-file').write_text('remove after reservation')
            manifest['resources'].append({'kind': 'tree', 'path': 'code', 'uid': 0})
            host.save(path, manifest)
        with original_lock(target):
            yield
    monkeypatch.setattr(host, 'ownership_lock', complete_provision_before_lock)
    result = host.cleanup(path)
    assert result['ok'], result
    assert not (root / 'code').exists()
    assert host.reservation_owner(host.IDENTITY_STATE / 'reservation.json') is None


def test_interrupted_retirement_can_resume_and_stale_cleanup_cannot_touch_replacement(
        owned_cleanup_fixture, monkeypatch):
    host, root, path, manifest = owned_cleanup_fixture
    (root / 'code').mkdir()
    manifest['resources'] = [{'kind': 'tree', 'path': 'code', 'uid': 0}]
    host.save(path, manifest)
    original_replace = host.os.replace
    def interrupt_publication(source, destination):
        if destination == root / 'retired.json':
            raise KeyboardInterrupt()
        return original_replace(source, destination)
    monkeypatch.setattr(host.os, 'replace', interrupt_publication)
    with pytest.raises(KeyboardInterrupt):
        host.cleanup(path)
    assert not (root / 'code').exists()
    assert not (root / 'retired.json').exists()
    with pytest.raises(ValueError, match='reserved'):
        host.require_available_reservation(host.IDENTITY_STATE / 'reservation.json')
    monkeypatch.setattr(host.os, 'replace', original_replace)
    assert host.cleanup(path)['ok']
    replacement = {'run_id': 'another-run', 'manifest': '/another-run/ownership.json'}
    with host.identity_reservation() as reservation:
        host.write_reservation(reservation, replacement)
    assert host.cleanup(path)['already_retired']
    assert host.reservation_owner(host.IDENTITY_STATE / 'reservation.json') == replacement


def test_two_real_processes_cannot_reserve_same_identities_after_hard_kill(
        owned_cleanup_fixture):
    import select
    host, root, _, _ = owned_cleanup_fixture
    with host.identity_reservation() as reservation:
        host.write_reservation(reservation, None)
    script = '''
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from tools.qualification_verification import host
host.IDENTITY_STATE = Path(sys.argv[2])
with host.identity_reservation() as reservation:
    host.require_available_reservation(reservation)
    host.write_reservation(reservation, {'run_id': 'interrupted', 'manifest': '/interrupted/ownership.json'})
    print('reserved', flush=True)
    sys.stdin.read()
'''
    child = subprocess.Popen([sys.executable, '-I', '-c', script, str(host.ROOT), str(host.IDENTITY_STATE)],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        assert select.select([child.stdout], [], [], 10)[0], 'child did not reach reservation'
        assert child.stdout.readline().strip() == 'reserved'
        with pytest.raises(BlockingIOError):
            with host.identity_reservation():
                pytest.fail('second provisioner acquired live reservation')
        child.kill()
        child.wait(timeout=5)
        with host.identity_reservation() as reservation:
            with pytest.raises(ValueError, match='reserved'):
                host.require_available_reservation(reservation)
            assert host.reservation_owner(reservation)['run_id'] == 'interrupted'
    finally:
        if child.poll() is None:
            child.kill()
            child.wait(timeout=5)
        for stream in (child.stdin, child.stdout, child.stderr):
            stream.close()
