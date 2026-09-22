"""Portable advisory file locking for single-file state transactions."""

from __future__ import annotations

from contextlib import contextmanager
import errno
import os
from pathlib import Path
import time
from typing import Iterator

if os.name == "nt":
    import msvcrt  # pylint: disable=import-error
else:
    import fcntl

# Poll schedule for the Windows acquire. See _acquire_windows_lock: the CRT's
# own LK_LOCK wait gives up, so the wait is spelled out here instead.
_WINDOWS_POLL_INITIAL_SECONDS = 0.0005
_WINDOWS_POLL_MAX_SECONDS = 0.02


def _acquire_windows_lock(fd: int) -> None:
    """Block until byte 0 of ``fd`` is exclusively locked.

    ``msvcrt.locking(LK_LOCK)`` is not a blocking wait: the CRT retries once
    a second and gives up after ten attempts with ``OSError(EDEADLOCK)``, so
    a caller that merely waited ten seconds for its turn saw a hard error
    instead of the lock. POSIX ``flock(LOCK_EX)`` waits indefinitely and no
    consumer of this module catches a give-up, so the Windows branch polls
    the non-blocking form and waits as long as POSIX would.

    Only ``EACCES`` — the CRT's contention code for ``LK_NBLCK`` — is
    retried; any other error propagates rather than spinning.
    """
    delay = _WINDOWS_POLL_INITIAL_SECONDS
    while True:
        try:
            # msvcrt is imported under the same os.name guard that gates every
            # call site of this helper.
            # pylint: disable-next=possibly-used-before-assignment
            msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
            return
        except OSError as exc:
            if exc.errno != errno.EACCES:
                raise
        time.sleep(delay)
        delay = min(delay * 2, _WINDOWS_POLL_MAX_SECONDS)


@contextmanager
def exclusive_file_lock(target: Path) -> Iterator[None]:
    """Serialize read-modify-write transactions associated with ``target``.

    Nothing ever writes to the lock file. Windows byte-range locks may cover
    a region past end-of-file, so byte 0 of a zero-length lock file is a
    perfectly good lock object, and ``open("a+b")`` creates the file with
    ``OPEN_ALWAYS`` semantics that concurrent callers can issue at the same
    time without conflict. The Windows branch used to append a one-byte
    payload when it saw ``tell() == 0``; because the CRT append is
    seek-then-write, a herd on a fresh lock file could write into the byte a
    sibling had just locked and raise ``PermissionError``. A writerless lock
    file has no such race to lose.
    """
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    lock_path = target.with_name(f"{target.name}.lock")

    with lock_path.open("a+b") as lock_file:
        if os.name == "nt":
            lock_file.seek(0)
            _acquire_windows_lock(lock_file.fileno())
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
