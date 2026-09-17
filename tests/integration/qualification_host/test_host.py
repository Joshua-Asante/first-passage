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
