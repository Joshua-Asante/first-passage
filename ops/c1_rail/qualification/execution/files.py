"""Bounded regular-file custody; no artifact-controlled imports or output paths."""
from __future__ import annotations

import os
from pathlib import Path, PurePosixPath
import stat
import tempfile

from lib.file_lock import exclusive_file_lock

from .protocol import positive, sha256


def relative_parts(relative):
    if (type(relative) is not str or not relative or '\\' in relative or ':' in relative
            or relative.startswith('/') or str(PurePosixPath(relative)) != relative):
        raise ValueError('canonical relative path required')
    parts = relative.split('/')
    if any(part in ('', '.', '..') for part in parts):
        raise ValueError('unsafe artifact path')
    return parts


def _not_link(info):
    return not stat.S_ISLNK(info.st_mode) and not (getattr(info, 'st_file_attributes', 0) & 0x400)


def _regular(info):
    if not _not_link(info) or not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise ValueError('single-link regular file required')


def read_regular(root: Path, relative: str, *, limit: int) -> bytes:
    """On Linux pin every directory FD and refuse symlinks at every component."""
    parts = relative_parts(relative)
    positive(limit)
    root = Path(root)
    info = root.lstat()
    if not _not_link(info) or not stat.S_ISDIR(info.st_mode):
        raise ValueError('regular artifact root directory required')
    descriptors = []
    try:
        if os.name == 'posix':
            directory = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
            descriptors.append(directory)
            for part in parts[:-1]:
                directory = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory)
                descriptors.append(directory)
            descriptor = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
        else:
            path = root
            for part in parts:
                path = path / part
                if not _not_link(path.lstat()):
                    raise ValueError('artifact link forbidden')
            _regular(path.lstat())
            descriptor = os.open(path, os.O_RDONLY | os.O_BINARY)
        descriptors.append(descriptor)
        before = os.fstat(descriptor)
        _regular(before)
        if before.st_size > limit:
            raise ValueError('artifact byte limit exceeded')
        chunks = []
        remaining = limit + 1
        while remaining:
            chunk = os.read(descriptor, min(remaining, 1024 * 1024))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        raw = b''.join(chunks)
        after = os.fstat(descriptor)
        _regular(after)
        if (len(raw) > limit or len(raw) != before.st_size or
                (before.st_size, before.st_mtime_ns, before.st_ctime_ns) !=
                (after.st_size, after.st_mtime_ns, after.st_ctime_ns)):
            raise ValueError('artifact mutated or byte limit exceeded')
        return raw
    except OSError as exc:
        raise ValueError('unsafe or unavailable regular artifact') from exc
    finally:
        for descriptor in reversed(descriptors):
            os.close(descriptor)


def fsync_directory(root: Path):
    if os.name == 'posix':
        descriptor = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)


def archive_bytes(root: Path, raw: bytes) -> str:
    """Publish without replacement and durably seal the exact content address."""
    digest = sha256(raw)
    root = Path(root)
    root.mkdir(mode=0o700, parents=True, exist_ok=True)
    if not _not_link(root.lstat()):
        raise ValueError('archive root link forbidden')
    # A retry may follow a crash after mkdir but before parent persistence.
    fsync_directory(root.parent)
    # Separate from object names so exported archives contain only content.
    # OS locks are released on process death; every publisher checks under it.
    with exclusive_file_lock(root.parent / (root.name + '.publication')):
        return _publish_bytes(root, raw, digest)


def _remove_temporary(path):
    info = path.lstat()
    _regular(info)
    if os.name == 'posix' and info.st_uid != os.geteuid():
        raise ValueError('archive temporary owner differs')
    if os.name == 'nt':
        path.chmod(0o600)
    path.unlink()


def _publish_bytes(root, raw, digest):
    # With the publication lock held, these can only be abandoned writes.
    for abandoned in root.glob('.capture-*'):
        _remove_temporary(abandoned)
    destination = root / digest
    if destination.exists() or destination.is_symlink():
        if read_regular(root, digest, limit=max(1, len(raw))) != raw:
            raise ValueError('archive content collision or corruption')
        fsync_directory(root)
        return digest
    descriptor, temporary = tempfile.mkstemp(prefix='.capture-', dir=root)
    try:
        with os.fdopen(descriptor, 'wb') as output:
            output.write(raw)
            output.flush()
            os.chmod(temporary, 0o400)
            os.fsync(output.fileno())
        # Destination was checked while holding the shared publication lock.
        # Rename preserves one link across a crash, unlike link-then-unlink.
        os.replace(temporary, destination)
        fsync_directory(root)
    finally:
        if os.path.exists(temporary):
            _remove_temporary(Path(temporary))
    return digest
