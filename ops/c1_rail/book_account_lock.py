"""One local-account serializer across durable commits and synchronous dispatch."""
from contextlib import contextmanager
import os
from pathlib import Path
import threading

from lib.file_lock import exclusive_file_lock


_REGISTRY = {}
_REGISTRY_LOCK = threading.Lock()


class AccountSerializer:
    """Canonical path, thread and OS locking; no lease stealing."""

    def __init__(self, path):
        self.path = Path(path).resolve()
        key = os.path.normcase(str(self.path))
        with _REGISTRY_LOCK:
            self._lock = _REGISTRY.setdefault(key, threading.RLock())

    @contextmanager
    def acquire(self):
        with self._lock:
            with exclusive_file_lock(self.path):
                yield
