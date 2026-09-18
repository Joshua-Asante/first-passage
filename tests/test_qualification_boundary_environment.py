"""Fast prerequisite diagnostics; these do not establish Linux isolation."""
import importlib
import json
from pathlib import Path
import pytest


def environment():
    name = 'scripts.qualification_boundary_environment'
    assert importlib.util.find_spec(name), 'environment preflight is missing'
    return importlib.import_module(name)


def test_unsupported_platform_is_failed_readiness(tmp_path, monkeypatch):
    env = environment()
    monkeypatch.setattr(env.platform, 'system', lambda: 'Windows')
    report = env.inspect_environment(tmp_path / 'absent.json', b'{}')
    assert report['purpose'] == 'environment_readiness'
    assert not report['ready']
    assert 'linux' in {failure['name'] for failure in report['failures']}
    with pytest.raises(ValueError, match='linux'):
        env.require_environment(report)


@pytest.mark.parametrize('report', [{}, {'ready': True},
    {'schema': 'qualification_environment/v1', 'ready': True, 'failures': []}])
def test_incomplete_reports_cannot_authorize_execution(report):
    with pytest.raises(ValueError):
        environment().require_environment(report)


def test_failed_probe_keeps_named_failure_without_exception_bytes():
    env = environment()
    report = env.new_report()
    env.check(report, 'docker', lambda: (_ for _ in ()).throw(OSError('secret contents')))
    assert report['failures'] == [{'name': 'docker', 'reason': 'OSError'}]
    assert 'secret contents' not in json.dumps(report)


def test_success_boolean_cannot_override_failed_prerequisite():
    env = environment()
    report = env.new_report()
    env.check(report, 'docker', lambda: False)
    report['ready'] = True
    with pytest.raises(ValueError, match='docker'):
        env.require_environment(report)


def test_missing_profile_is_a_named_dependency_failure(tmp_path, monkeypatch):
    env = environment()
    monkeypatch.setattr(env.platform, 'system', lambda: 'Linux')
    monkeypatch.setattr(env, 'load_profile', lambda raw: (_ for _ in ()).throw(ImportError()))
    report = env.inspect_environment(tmp_path / 'absent.json', b'{}')
    assert not report['ready']
    assert 'execution_profile' in {f['name'] for f in report['failures']}


def test_scratch_is_probed_as_execution_uid(monkeypatch):
    env = environment()
    roles = {'qclient': {'uid': 11}, 'qexec': {'uid': 12}, 'qg5': {'uid': 13}}
    doc = {'data': '/data', 'execution_key': '/exec-key', 'result_key': '/result-key',
           'docker_socket': '/docker', 'scratch': '/scratch'}
    def access(role, action, path):
        owners = {'/data': 12, '/exec-key': 12, '/result-key': 13, '/docker': 12}
        return {'allowed': role['uid'] == owners.get(path), 'uid': role['uid'], 'groups': []}
    monkeypatch.setattr(env, 'probe_access', access)
    report = env.permissions(doc, roles)
    assert not report['ok'], 'inaccessible qexec scratch must fail readiness'
    assert any(p['path'] == '/scratch' and p['role'] == 'qexec' and not p['allowed']
               for p in report['probes'])

@pytest.mark.parametrize('missing', ['docker', 'image', 'signing', 'roles', 'trusted_roots', 'evidence'])
def test_missing_mandatory_prerequisite_fails_before_execution(tmp_path, monkeypatch, missing):
    from types import SimpleNamespace
    env = environment()
    raw = b'canonical-test-double'
    doc = {'roles': {}, 'trusted_roots': ['/code'], 'docker_socket': '/var/run/docker.sock',
           'worker_image_id': 'sha256:' + 'a' * 64, 'profile_sha256': env.hashlib.sha256(raw).hexdigest(),
           'scratch': str(tmp_path), 'evidence': str(tmp_path)}
    monkeypatch.setattr(env.platform, 'system', lambda: 'Linux')
    monkeypatch.setattr(env.os, 'geteuid', lambda: 0, raising=False)
    monkeypatch.setattr(env.socket, 'SO_PEERCRED', 17, raising=False)
    monkeypatch.setattr(env, 'load_profile', lambda data: SimpleNamespace(scratch_bytes=1))
    monkeypatch.setattr(env, 'read_instance', lambda path: doc)
    monkeypatch.setattr(env, 'identities', lambda doc: {'qexec': {'uid': 12}})
    monkeypatch.setattr(env, 'trusted_roots', lambda doc: ['/code'])
    monkeypatch.setattr(env, 'permissions', lambda doc, roles: {'ok': True, 'probes': []})
    monkeypatch.setattr(env, 'storage', lambda doc: {'data': 'ext4'})
    monkeypatch.setattr(env.os, 'statvfs', lambda path: SimpleNamespace(f_bavail=100, f_frsize=100), raising=False)
    monkeypatch.setattr(env.importlib.metadata, 'version', lambda name: '50.0.1')
    def external(command):
        if 'version' in command:
            if missing == 'docker':
                raise OSError('daemon absent')
            return '{"Version":"28.0.4"}'
        return json.dumps([{'Id': 'wrong' if missing == 'image' else doc['worker_image_id'], 'RepoDigests': []}])
    monkeypatch.setattr(env, 'run', external)
    def denied(*args):
        raise PermissionError('fixture denial')
    if missing in ('roles', 'trusted_roots', 'evidence'):
        monkeypatch.setattr(env, {'roles': 'identities', 'trusted_roots': 'trusted_roots',
                                 'evidence': 'writable_directory'}[missing], denied)
    if missing == 'signing':
        monkeypatch.setattr(env.importlib.metadata, 'version', denied)
    report = env.inspect_environment(tmp_path / 'instance.json', raw)
    assert missing in {failure['name'] for failure in report['failures']}
    with pytest.raises(ValueError):
        env.require_environment(report)

@pytest.mark.parametrize('uids', [
    {'qclient': 11, 'qexec': 11, 'qg5': 13},
    {'qclient': 0, 'qexec': 12, 'qg5': 13},
])
def test_roles_reject_shared_or_root_identity(monkeypatch, uids):
    import sys
    from types import SimpleNamespace
    env = environment()
    monkeypatch.setitem(sys.modules, 'pwd', SimpleNamespace(getpwuid=lambda uid:
                        SimpleNamespace(pw_name=f'q{uid}', pw_gid=uid)))
    monkeypatch.setitem(sys.modules, 'grp', SimpleNamespace(getgrgid=lambda gid:
                        SimpleNamespace(gr_name=f'q{gid}'), getgrnam=lambda name:
                        SimpleNamespace(gr_gid=999)))
    monkeypatch.setattr(env.os, 'getgrouplist', lambda name, gid: [gid], raising=False)
    with pytest.raises(ValueError):
        env.identities({'roles': uids})


def test_readiness_cannot_omit_its_privileged_supervisor_assumption():
    env = environment()
    report = env.new_report()
    report.update(ready=True, checks={name: {'ok': True} for name in env.REQUIRED})
    report.pop('trust_model', None)
    with pytest.raises(ValueError, match='trust model'):
        env.require_environment(report)


@pytest.mark.parametrize('role', ['qclient', 'qexec', 'qg5'])
@pytest.mark.parametrize('change', ['extra-disk', 'wrong-primary', 'valid'])
def test_roles_require_exact_group_sets(monkeypatch, role, change):
    import sys
    from types import SimpleNamespace
    env = environment()
    uids = {'qclient': 11, 'qexec': 12, 'qg5': 13}
    names = {uid: name for name, uid in uids.items()}
    def user(uid):
        return SimpleNamespace(pw_name=names[uid],
                               pw_gid=6 if names[uid] == role and change == 'wrong-primary' else uid)
    def groups(name, gid):
        result = [gid] + ([999] if name == 'qexec' else [11] if name == 'qg5' else [])
        return result + ([6] if name == role and change == 'extra-disk' else [])
    monkeypatch.setitem(sys.modules, 'pwd', SimpleNamespace(getpwuid=user))
    monkeypatch.setitem(sys.modules, 'grp', SimpleNamespace(
        getgrnam=lambda name: SimpleNamespace(gr_gid=999),
        getgrgid=lambda gid: SimpleNamespace(gr_name='disk' if gid == 6 else names.get(gid, 'docker'))))
    monkeypatch.setattr(env.os, 'getgrouplist', groups, raising=False)
    if change == 'valid':
        result = env.identities({'roles': uids})
        assert result['qclient']['groups'] == [11]
        assert result['qexec']['groups'] == [12, 999]
        assert result['qg5']['groups'] == [11,13]
    else:
        with pytest.raises(ValueError, match='group'):
            env.identities({'roles': uids})


def test_execution_role_requires_docker_membership(monkeypatch):
    import sys
    from types import SimpleNamespace
    env = environment()
    monkeypatch.setitem(sys.modules, 'pwd', SimpleNamespace(getpwuid=lambda uid:
                        SimpleNamespace(pw_name='qexec', pw_gid=uid)))
    monkeypatch.setitem(sys.modules, 'grp', SimpleNamespace(
        getgrnam=lambda name: SimpleNamespace(gr_gid=999),
        getgrgid=lambda gid: SimpleNamespace(gr_name='qexec')))
    monkeypatch.setattr(env.os, 'getgrouplist', lambda name, gid: [gid], raising=False)
    with pytest.raises(ValueError, match='group'):
        env.identities({'roles': {'qexec': 12, 'qclient': 11, 'qg5': 13}})
