"""Portable advisory file locking for single-file state transactions."""

from __future__ import annotations

from contextlib import contextmanager
import os
from pathlib import Path
from typing import Iterator

if os.name == "nt":
    import msvcrt  # pylint: disable=import-error
else:
    import fcntl


@contextmanager
def exclusive_file_lock(target: Path) -> Iterator[None]:
    """Serialize read-modify-write transactions associated with ``target``."""
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    lock_path = target.with_name(f"{target.name}.lock")

    with lock_path.open("a+b") as lock_file:
        if os.name == "nt":
            if lock_file.tell() == 0:
                lock_file.write(b"\0")
                lock_file.flush()
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
