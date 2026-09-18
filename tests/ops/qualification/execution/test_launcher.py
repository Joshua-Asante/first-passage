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
    args = launcher.create_arguments(context, execution_id='fixture', input_dir=Path('/protected/input'), profile=profile)
    assert args[-4:] == ['worker', '--execution-id', 'fixture', '--input=/input']
    assert 'sha256:' + 'a' * 64 in args
    assert '--network=none' in args and '--read-only' in args
    assert '--cap-drop=ALL' in args and '--security-opt=no-new-privileges:true' in args
    assert '--restart=no' in args and '--user=65532:65532' in args
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
