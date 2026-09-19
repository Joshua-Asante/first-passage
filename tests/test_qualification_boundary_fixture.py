"""The real boundary fixture hands its retained host configuration to preflight.

These construction checks run on the development host with the privileged
collaborators replaced; the disposable Linux runs exercise the real ones.
"""
import importlib.util
import json
from pathlib import Path
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIRECTORY = ROOT / 'tests/integration/qualification_boundary'
HOST_CONFIG = {'python': '/opt/fp/bin/python3', 'docker': '/opt/fp/bin/docker',
               'parent': '/var/lib/fp'}
ROLES = {'qclient': 61000, 'qexec': 61001, 'qg5': 61002}


def fixture_module(monkeypatch):
    # The fixture's conftest imports its sibling transport module by bare name,
    # exactly as pytest loads it on the disposable host.
    monkeypatch.syspath_prepend(str(FIXTURE_DIRECTORY))
    spec = importlib.util.spec_from_file_location('qualification_boundary_conftest',
                                                  FIXTURE_DIRECTORY / 'conftest.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def installed_host(tmp_path, name, *, supervisor, instance, profile):
    """A retained ownership manifest plus the installation files the fixture reads."""
    root = tmp_path / (name * 32)
    installation = root / 'code/qualification-installation'
    installation.mkdir(parents=True)
    (root / 'evidence').mkdir()
    manifest = {'run_id': root.name, 'roles': ROLES, 'host_config': HOST_CONFIG,
                'state': 'host_ready_boundary_unconfigured'}
    path = root / 'ownership.json'
    path.write_text(json.dumps(manifest))
    (installation / 'supervisor.json').write_text(json.dumps(supervisor))
    (installation / 'test-instance.json').write_bytes(instance)
    (installation / 'profile.json').write_bytes(profile)
    return root, installation, path


@pytest.mark.parametrize('diagnostic', [False, True], ids=['boundary', 's2'])
def test_fixture_passes_its_retained_host_configuration_to_preflight(tmp_path, monkeypatch,
                                                                     diagnostic):
    conftest = fixture_module(monkeypatch)
    environment = sys.modules['scripts.qualification_boundary_environment']
    root, installation, path = installed_host(
        tmp_path, 'a', supervisor={'socket_path': str(tmp_path / 'service.sock')},
        instance=b'{"schema": "qualification_test_instance/v1"}',
        profile=b'canonical-profile-bytes')
    monkeypatch.setenv('FP_QUALIFICATION_S2', '1' if diagnostic else '0')
    image = 'sha256:' + 'c' * 64
    events = []
    def record(event, value=None):
        events.append(event)
        return value
    monkeypatch.setattr(conftest.host, 'create_process_group',
                        lambda root: record('group', root / 'group'))
    monkeypatch.setattr(conftest, 'build_worker', lambda root, manifest: record('build', image))
    monkeypatch.setattr(conftest.Boundary, 'admin',
                        lambda self, *arguments: record(('admin', arguments), {}))
    monkeypatch.setattr(conftest.Boundary, 'restart', lambda self, **kwargs: record('restart'))
    inspected = []
    report = environment.new_report()
    report.update(ready=True, checks={name: {'ok': True} for name in environment.REQUIRED})
    def inspect(instance_path, profile_bytes, **kwargs):
        inspected.append((instance_path, profile_bytes, kwargs))
        return record('inspect', report)
    monkeypatch.setattr(conftest, 'inspect_environment', inspect)
    saved = []
    def save(path, data, **kwargs):
        saved.append((path, data, kwargs))
        record('save')
    monkeypatch.setattr(conftest.host, 'save', save)
    required = []
    monkeypatch.setattr(conftest, 'require_environment',
                        lambda report: record('require', required.append(report)))

    boundary = conftest.Boundary(path)

    assert boundary.manifest['host_config'] == HOST_CONFIG
    # The keyword is the retained manifest object itself, never a reloaded default host.json.
    assert inspected == [(installation / 'test-instance.json', b'canonical-profile-bytes',
                          {'host_config': boundary.manifest['host_config']})]
    assert inspected[0][2]['host_config'] is boundary.manifest['host_config']
    assert saved == [(root / 'evidence/boundary/environment.json', report, {'exclusive': True})]
    assert required == [report]
    install = ('admin', ('install', '--image', image) + (('--diagnostic',) if diagnostic else ()))
    assert events == ['group', 'build', install, 'inspect', 'save', 'require', 'restart']


def test_fixture_does_not_start_the_service_when_preflight_is_not_ready(tmp_path, monkeypatch):
    conftest = fixture_module(monkeypatch)
    environment = sys.modules['scripts.qualification_boundary_environment']
    root, _, path = installed_host(tmp_path, 'b', supervisor={}, instance=b'{}', profile=b'')
    monkeypatch.delenv('FP_QUALIFICATION_S2', raising=False)
    monkeypatch.setattr(conftest.host, 'create_process_group', lambda root: root / 'group')
    monkeypatch.setattr(conftest, 'build_worker', lambda root, manifest: 'sha256:' + 'd' * 64)
    monkeypatch.setattr(conftest.Boundary, 'admin', lambda self, *arguments: {})
    started = []
    monkeypatch.setattr(conftest.Boundary, 'restart', lambda self, **kwargs: started.append(True))
    # Every other prerequisite holds, so the refusal can only come from the client check.
    report = environment.new_report()
    report['checks'] = {name: {'ok': name != 'docker_client'} for name in environment.REQUIRED}
    report['failures'].append({'name': 'docker_client', 'reason': 'ValueError'})
    monkeypatch.setattr(conftest, 'inspect_environment',
                        lambda instance_path, profile_bytes, **kwargs: report)
    saved = []
    monkeypatch.setattr(conftest.host, 'save', lambda path, data, **kwargs: saved.append(path))
    with pytest.raises(ValueError, match='prerequisites failed: docker_client$'):
        conftest.Boundary(path)
    assert saved == [root / 'evidence/boundary/environment.json'], 'the failed report is retained'
    assert started == []
