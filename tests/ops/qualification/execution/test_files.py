"""Staged bytes cannot follow aliases or escape their protected root."""
import importlib
import os

import pytest


def files():
    return importlib.import_module('c1_rail.qualification.execution.files')


@pytest.mark.parametrize('path', ['../escape', '/absolute', 'C:/outside', 'a/../b', 'a\\b', '', 'a//b'])
def test_staged_path_cannot_escape_or_alias(tmp_path, path):
    with pytest.raises(ValueError, match='path'):
        files().read_regular(tmp_path, path, limit=100)


def test_regular_read_is_exact_and_bounded(tmp_path):
    (tmp_path / 'input').write_bytes(b'original')
    assert files().read_regular(tmp_path, 'input', limit=8) == b'original'
    with pytest.raises(ValueError, match='limit'):
        files().read_regular(tmp_path, 'input', limit=7)


def test_hardlink_cannot_keep_a_writable_alias(tmp_path):
    (tmp_path / 'input').write_bytes(b'original')
    os.link(tmp_path / 'input', tmp_path / 'alias')
    with pytest.raises(ValueError, match='regular|link'):
        files().read_regular(tmp_path, 'alias', limit=100)


def test_directory_cannot_masquerade_as_artifact(tmp_path):
    (tmp_path / 'input').mkdir()
    with pytest.raises(ValueError, match='regular'):
        files().read_regular(tmp_path, 'input', limit=100)


def test_archive_rechecks_existing_bytes_and_never_overwrites(tmp_path):
    module = files()
    digest = module.archive_bytes(tmp_path, b'original')
    assert module.archive_bytes(tmp_path, b'original') == digest
    (tmp_path / digest).chmod(0o600)
    (tmp_path / digest).write_bytes(b'changed!')
    with pytest.raises(ValueError, match='archive'):
        module.archive_bytes(tmp_path, b'original')
    assert (tmp_path / digest).read_bytes() == b'changed!'
