"""Staged bytes cannot follow aliases or escape their protected root."""
import importlib
import os
from pathlib import Path
import subprocess
import sys

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


@pytest.mark.parametrize('after_publication', [False, True])
def test_archive_recovers_process_death_at_publication(tmp_path, after_publication):
    """A dead publisher must leave neither an unreadable digest nor temp debris."""
    driver = '''
import os, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1] + '/ops')
sys.path.insert(0, sys.argv[1] + '/core')
from c1_rail.qualification.execution.files import archive_bytes
after = sys.argv[3] == 'True'
def interrupted(function):
    def publish(*args, **kwargs):
        if after:
            function(*args, **kwargs)
        os._exit(71)
    return publish
os.link = interrupted(os.link)
os.replace = interrupted(os.replace)
archive_bytes(Path(sys.argv[2]), b'original')
'''
    repo = Path(__file__).resolve().parents[4]
    archive = tmp_path / 'objects'
    result = subprocess.run([sys.executable, '-c', driver, str(repo), str(archive),
                             str(after_publication)], check=False, capture_output=True, timeout=20)
    assert result.returncode == 71, result.stderr.decode()
    module = files()
    digest = module.archive_bytes(archive, b'original')
    assert module.read_regular(archive, digest, limit=8) == b'original'
    assert (archive / digest).stat().st_nlink == 1
    assert [path.name for path in archive.iterdir()] == [digest]


def test_archive_retry_reestablishes_directory_durability(tmp_path, monkeypatch):
    module = files()
    digest = module.archive_bytes(tmp_path, b'original')
    synced = []
    monkeypatch.setattr(module, 'fsync_directory', lambda root: synced.append(root))
    assert module.archive_bytes(tmp_path, b'original') == digest
    assert synced == [tmp_path.parent, tmp_path]


def test_concurrent_archive_publishers_keep_one_immutable_object(tmp_path):
    module = files()
    # Windows bootstraps a fresh lock file by appending one byte before
    # byte-range locking it; the CRT append is seek-then-write, so a herd of
    # publishers on an empty lock file can append into the byte a sibling
    # just locked (PermissionError). Publish the bootstrap byte first; the
    # publishers themselves then only lock and unlock, never write it.
    with module.exclusive_file_lock(tmp_path.parent / (tmp_path.name + '.publication')):
        pass
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=4) as pool:
        digests = list(pool.map(lambda _: module.archive_bytes(tmp_path, b'original'), range(8)))
    assert len(set(digests)) == 1
    assert module.read_regular(tmp_path, digests[0], limit=8) == b'original'
    assert sorted(path.name for path in tmp_path.iterdir()) == [digests[0]]
