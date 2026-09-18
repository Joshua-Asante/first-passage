"""Launcher policy units; these do not establish Linux isolation."""
import importlib
from pathlib import Path
from types import SimpleNamespace

import pytest
from test_profile import document
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution.profile import parse_profile
from c1_rail.qualification.execution.protocol import CapturedOutput


def test_create_arguments_pin_effective_policy_and_ignore_environment(monkeypatch):
    launcher = importlib.import_module('c1_rail.qualification.execution.launcher')
    monkeypatch.setenv('DOCKER_HOST', 'tcp://attacker:2375')
    monkeypatch.setenv('PYTHONPATH', '/attacker')
    profile = parse_profile(encoded(document()))
    context = SimpleNamespace(release=SimpleNamespace(document={'worker_image_digest': 'sha256:' + 'a' * 64}),
                              profile=profile)
    args = launcher.create_arguments(context, execution_id='fixture', input_dir=Path('/protected/input'), profile=profile, host_run_id='a'*32)
    assert args[-4:] == ['worker', '--execution-id', 'fixture', '--input=/input']
    assert 'sha256:' + 'a' * 64 in args
    assert '--network=none' in args and '--read-only' in args
    assert '--cap-drop=ALL' in args and '--security-opt=no-new-privileges:true' in args
    assert '--restart=no' in args and '--user=65532:65532' in args
    assert '--label=fp.qualification.host='+'a'*32 in args
    assert launcher.docker_environment() == {'PATH': '/usr/bin:/bin', 'HOME': '/nonexistent', 'LANG': 'C.UTF-8'}


@pytest.mark.parametrize('raw', [b'', b'\x00\x00\x00\x02{', b'\x00\x00\x00\x02{}extra'])
def test_archive_rejects_incomplete_or_extra_frames(tmp_path, raw):
    archive = importlib.import_module('c1_rail.qualification.execution.archive')
    with pytest.raises(ValueError, match='frame'):
        archive.archive_capture(CapturedOutput('a' * 64, raw, 0, False, 1), archive_dir=tmp_path)


def test_archive_requires_daemon_success(tmp_path):
    archive = importlib.import_module('c1_rail.qualification.execution.archive')
    with pytest.raises(ValueError, match='abnormal'):
        archive.archive_capture(CapturedOutput('a' * 64, b'\x00\x00\x00\x02{}', 0, True, 1), archive_dir=tmp_path)


def test_capture_exposes_stderr_before_worker_eof(tmp_path, monkeypatch):
    """Buffered capture hides readiness while a worker waits to be stopped."""
    launcher = importlib.import_module('c1_rail.qualification.execution.launcher')
    marker = b'TEST_ONLY worker fault: stop\n'
    source = tmp_path / 'stderr-source'
    source.write_bytes(marker)
    stdout = (tmp_path / 'stdout-source').open('w+b')
    stderr = source.open('rb')
    process = SimpleNamespace(stdout=stdout, stderr=stderr, returncode=0,
                              wait=lambda **kw: 0, kill=lambda: None)
    spool = tmp_path / 'capture'

    class Selector:
        def __init__(self):
            self.streams = {}
            self.read_once = False

        def register(self, stream, _events, data):
            self.streams[stream] = SimpleNamespace(fileobj=stream, data=data)

        def get_map(self):
            return self.streams

        def select(self, **kw):
            if self.read_once:
                assert (spool / 'stderr.log').read_bytes() == marker
            self.read_once = True
            return [(key, 1) for key in self.streams.values()]

        def unregister(self, stream):
            del self.streams[stream]

        def close(self):
            pass

    monkeypatch.setattr(launcher.subprocess, 'Popen', lambda *a, **kw: process)
    monkeypatch.setattr(launcher, '_command', lambda *a: ['fake-docker', *a])
    monkeypatch.setattr(launcher.selectors, 'DefaultSelector', Selector)
    monkeypatch.setattr(launcher, '_inspect', lambda cid: dict(State=dict(
        Running=False, Status='exited', ExitCode=0, OOMKilled=False)))
    result = launcher.start_and_capture('a' * 64, spool_dir=spool,
        profile=parse_profile(encoded(document())), maximum_wall_seconds=1)
    assert result.exit_code == 0


@pytest.mark.parametrize('foreign', [False,True])
def test_orphan_discovery_requires_exact_name_labels_and_image(monkeypatch,foreign):
    import json
    launcher=importlib.import_module('c1_rail.qualification.execution.launcher')
    image='sha256:'+'b'*64
    row=dict(Id='c'*64,Name='/foreign' if foreign else '/qexec-fixture',Image=image,
        Config=dict(Image=image,Labels={'fp.qualification.host':'a'*32,
            'org.first-passage.qualification.execution':'fixture'}))
    def run(*arguments):
        if arguments[0]=='ps': return ('c'*64+'\n').encode()
        if arguments[:2]==('inspect','--type=container'): return json.dumps([row]).encode()
        raise AssertionError(arguments)
    monkeypatch.setattr(launcher,'_run',run)
    def find(): return launcher.find_owned_worker('fixture',host_run_id='a'*32,image_id=image,release_sha256='d'*64)
    if foreign:
        with pytest.raises(ValueError,match='owned container'): find()
    else: assert find()=='c'*64
