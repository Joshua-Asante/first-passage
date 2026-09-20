"""Fast prerequisite diagnostics; these do not establish Linux isolation."""
import importlib
import json
from pathlib import Path
import pytest


HOST_CONFIG = {'python': '/usr/bin/python3', 'docker': '/usr/bin/docker'}
NONDEFAULT_CONFIG = {'python': '/opt/fp/bin/python3', 'docker': '/opt/fp/bin/docker'}
SOCKET = 'unix:///var/run/docker.sock'
IMAGE_ID = 'sha256:' + 'a' * 64
PRIVATE_DIGEST = 'private.example/team/worker@sha256:' + 'b' * 64


def environment():
    name = 'scripts.qualification_boundary_environment'
    assert importlib.util.find_spec(name), 'environment preflight is missing'
    return importlib.import_module(name)


def ready_host(env, tmp_path, monkeypatch, *, raw=b'canonical-test-double'):
    """Model a ready disposable host up to Docker client selection; callers supply `run`."""
    from types import SimpleNamespace
    doc = {'roles': {}, 'trusted_roots': ['/code'], 'docker_socket': '/var/run/docker.sock',
           'worker_image_id': IMAGE_ID, 'profile_sha256': env.hashlib.sha256(raw).hexdigest(),
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
    monkeypatch.setattr(env.os, 'statvfs', lambda path: SimpleNamespace(f_bavail=100, f_frsize=100),
                        raising=False)
    monkeypatch.setattr(env.importlib.metadata, 'version', lambda name: '50.0.1')
    # The development host has no protected POSIX executable to present; the
    # disposable Linux tests exercise real ownership, links and modes.
    monkeypatch.setattr(env, 'protected_executable', lambda value: None)
    return doc, raw


def docker_double(doc, *, digests=(), image_id=None):
    """A Docker client double that records every invocation it receives."""
    commands = []
    def external(command):
        commands.append(list(command))
        if command[3:] == ['version', '--format', '{{json .Server}}']:
            return '{"Version":"28.0.4"}'
        if command[3:5] == ['image', 'inspect']:
            return json.dumps([{'Id': image_id or doc['worker_image_id'],
                                'RepoDigests': list(digests),
                                'RepoTags': [value.split('@')[0] + ':latest'
                                             for value in digests]}])
        raise AssertionError('unexpected external command: ' + repr(command))
    return external, commands


def test_unsupported_platform_is_failed_readiness(tmp_path, monkeypatch):
    env = environment()
    monkeypatch.setattr(env.platform, 'system', lambda: 'Windows')
    report = env.inspect_environment(tmp_path / 'absent.json', b'{}', host_config=HOST_CONFIG)
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
    report = env.inspect_environment(tmp_path / 'absent.json', b'{}', host_config=HOST_CONFIG)
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

@pytest.mark.parametrize('missing', ['docker_client', 'docker', 'image', 'signing', 'roles',
                                     'trusted_roots', 'evidence'])
def test_missing_mandatory_prerequisite_fails_before_execution(tmp_path, monkeypatch, missing):
    env = environment()
    doc, raw = ready_host(env, tmp_path, monkeypatch)
    def external(command):
        if 'version' in command:
            if missing == 'docker':
                raise OSError('daemon absent')
            return '{"Version":"28.0.4"}'
        return json.dumps([{'Id': 'wrong' if missing == 'image' else doc['worker_image_id'], 'RepoDigests': []}])
    monkeypatch.setattr(env, 'run', external)
    def denied(*args):
        raise PermissionError('fixture denial')
    if missing in ('roles', 'trusted_roots', 'evidence', 'docker_client'):
        monkeypatch.setattr(env, {'roles': 'identities', 'trusted_roots': 'trusted_roots',
                                 'evidence': 'writable_directory',
                                 'docker_client': 'protected_executable'}[missing], denied)
    if missing == 'signing':
        monkeypatch.setattr(env.importlib.metadata, 'version', denied)
    report = env.inspect_environment(tmp_path / 'instance.json', raw, host_config=HOST_CONFIG)
    assert missing in {failure['name'] for failure in report['failures']}
    with pytest.raises(ValueError):
        env.require_environment(report)


def test_inspect_environment_requires_the_retained_host_configuration(tmp_path):
    """The configuration is an explicit keyword; there is no default host or PATH fallback."""
    env = environment()
    with pytest.raises(TypeError):
        env.inspect_environment(tmp_path / 'absent.json', b'{}')
    with pytest.raises(TypeError):
        env.inspect_environment(tmp_path / 'absent.json', b'{}', HOST_CONFIG)


def test_docker_queries_use_the_configured_protected_client(tmp_path, monkeypatch):
    env = environment()
    doc, raw = ready_host(env, tmp_path, monkeypatch)
    external, commands = docker_double(doc)
    # One sequence for both collaborators, so the order of protection and queries is proven.
    sequence = []
    def validated(value):
        sequence.append(('protected', value))
    def run(command):
        sequence.append(('run', list(command)))
        return external(command)
    monkeypatch.setattr(env, 'protected_executable', validated)
    monkeypatch.setattr(env, 'run', run)
    report = env.inspect_environment(tmp_path / 'instance.json', raw, host_config=NONDEFAULT_CONFIG)
    env.require_environment(report)
    client = [NONDEFAULT_CONFIG['docker'], '--host', SOCKET]
    assert sequence == [('protected', NONDEFAULT_CONFIG['docker']),
                        ('run', [*client, 'version', '--format', '{{json .Server}}']),
                        ('run', [*client, 'image', 'inspect', IMAGE_ID])]
    assert report['checks']['docker_client'] == {'ok': True,
                                                 'observed': NONDEFAULT_CONFIG['docker']}
    assert '/usr/bin/docker' not in json.dumps(commands)


@pytest.mark.parametrize('case', ['absent', 'not-a-mapping', 'missing-key', 'relative',
                                  'parent-segment', 'windows-path', 'not-a-string', 'unprotected'])
def test_invalid_or_unprotected_client_fails_readiness_before_invocation(tmp_path, monkeypatch,
                                                                         case):
    env = environment()
    doc, raw = ready_host(env, tmp_path, monkeypatch)
    host_config = {'absent': None, 'not-a-mapping': HOST_CONFIG['docker'],
                   'missing-key': {'python': HOST_CONFIG['python']},
                   'relative': {**HOST_CONFIG, 'docker': 'docker'},
                   'parent-segment': {**HOST_CONFIG, 'docker': '/usr/bin/../local/bin/docker'},
                   'windows-path': {**HOST_CONFIG, 'docker': 'C:\\docker.exe'},
                   'not-a-string': {**HOST_CONFIG, 'docker': 12},
                   'unprotected': HOST_CONFIG}[case]
    if case == 'unprotected':
        def unprotected(value):
            raise ValueError('unprotected path')
        monkeypatch.setattr(env, 'protected_executable', unprotected)
    external, commands = docker_double(doc)
    monkeypatch.setattr(env, 'run', external)
    report = env.inspect_environment(tmp_path / 'instance.json', raw, host_config=host_config)
    assert commands == [], 'an unvalidated client must never be executed'
    assert not report['ready']
    assert {'name': 'docker_client', 'reason': 'ValueError'} in report['failures']
    assert 'docker' not in report['checks'] and 'image' not in report['checks']
    with pytest.raises(ValueError, match='docker_client'):
        env.require_environment(report)


def test_readiness_requires_the_client_selection_check():
    env = environment()
    report = env.new_report()
    checks = {name: {'ok': True} for name in env.REQUIRED - {'docker_client'}}
    report.update(ready=True, checks=checks)
    with pytest.raises(ValueError, match='docker_client'):
        env.require_environment(report)


def test_mismatched_image_identity_still_rejects_with_the_configured_client(tmp_path, monkeypatch):
    env = environment()
    doc, raw = ready_host(env, tmp_path, monkeypatch)
    external, commands = docker_double(doc, image_id='sha256:' + 'f' * 64)
    monkeypatch.setattr(env, 'run', external)
    report = env.inspect_environment(tmp_path / 'instance.json', raw, host_config=NONDEFAULT_CONFIG)
    assert commands[-1][:5] == [NONDEFAULT_CONFIG['docker'], '--host', SOCKET, 'image', 'inspect']
    assert {'name': 'image', 'reason': 'ValueError'} in report['failures']
    assert report['checks']['image'] == {'ok': False}
    assert 'f' * 64 not in json.dumps(report), 'a rejected observation never enters the report'
    with pytest.raises(ValueError, match='image'):
        env.require_environment(report)


def test_environment_evidence_retains_only_the_opaque_image_identity(tmp_path, monkeypatch):
    env = environment()
    doc, raw = ready_host(env, tmp_path, monkeypatch)
    external, _ = docker_double(doc, digests=[PRIVATE_DIGEST])
    monkeypatch.setattr(env, 'run', external)
    report = env.inspect_environment(tmp_path / 'instance.json', raw, host_config=HOST_CONFIG)
    env.require_environment(report)
    assert report['checks']['image']['observed'] == {'id': IMAGE_ID}
    evidence = tmp_path / 'environment.json'
    from tools.qualification_verification import host
    if hasattr(env.os, 'O_DIRECTORY'):
        host.save(evidence, report, exclusive=True)  # the fixture's evidence-writing path
    else:
        # Windows cannot fsync a directory; the writer serializes with exactly these options.
        evidence.write_bytes((json.dumps(report, indent=2, sort_keys=True) + '\n').encode())
    serialized = evidence.read_text()
    for private in ('RepoDigests', 'RepoTags', 'digests', 'private.example', 'team/worker',
                    'b' * 64):
        assert private not in serialized, private + ' must not reach retained evidence'
    assert IMAGE_ID in serialized

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
