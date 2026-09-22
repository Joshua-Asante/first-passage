"""Portable advisory file locking for single-file state transactions."""

from __future__ import annotations

from contextlib import contextmanager
import os
from pathlib import Path
import tempfile
from typing import Iterator

if os.name == "nt":
    import msvcrt  # pylint: disable=import-error
else:
    import fcntl

# Windows locks byte 0 of the lock file; the file is published with this
# payload exactly once and never written afterwards.
_WINDOWS_LOCK_PAYLOAD = b"\0"


def _bootstrap_windows_lock_file(lock_path: Path) -> None:
    """Publish ``lock_path`` with its one-byte payload, race-free.

    The former bootstrap appended the byte through an ``a+b`` handle when
    ``tell() == 0``. The CRT append is seek-then-write, so a herd on a fresh
    lock file could append into the byte a sibling had just locked and raise
    ``PermissionError``. Writing the payload to a private temp file and
    renaming it into place means the lock file is either absent or complete:
    no caller ever writes through a handle another caller may have locked.
    ``os.rename`` refuses an existing destination on Windows, so the loser of
    a concurrent bootstrap simply discards its temp file.
    """
    if lock_path.exists():
        return
    fd, tmp_name = tempfile.mkstemp(
        dir=lock_path.parent, prefix=lock_path.name + ".", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "wb") as tmp_file:
            tmp_file.write(_WINDOWS_LOCK_PAYLOAD)
            tmp_file.flush()
        os.rename(tmp_name, lock_path)
    except FileExistsError:
        os.unlink(tmp_name)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


@contextmanager
def exclusive_file_lock(target: Path) -> Iterator[None]:
    """Serialize read-modify-write transactions associated with ``target``."""
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    lock_path = target.with_name(f"{target.name}.lock")

    if os.name == "nt":
        _bootstrap_windows_lock_file(lock_path)

    with lock_path.open("a+b") as lock_file:
        if os.name == "nt":
            lock_file.seek(0)
            msvcrt.locking(lock_file.fileno(), msvcrt.LK_LOCK, 1)
        else:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)

        try:
            yield
        finally:
            if os.name == "nt":
                lock_file.seek(0)
                msvcrt.locking(lock_file.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
