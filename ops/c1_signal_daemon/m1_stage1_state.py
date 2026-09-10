"""Private durable one-shot journal. Never use execution/account state as a latch."""
from __future__ import annotations

from contextlib import contextmanager
import copy
import json
import os
from pathlib import Path
import tempfile
import threading

DEFAULT_STATE_PATH = Path("/data/c1_m1_stage1_state.json")
STATES = frozenset({"DISABLED", "READY", "EVALUATED", "SEND_RESERVED", "EMITTED",
                    "RESPONSE_RECORDED", "TRANSPORT_UNKNOWN", "CLOSED"})
CLAIMED = STATES - {"DISABLED", "READY"}


class CeremonyError(ValueError):
    """Fail closed without exposing private state or configuration values."""


def require(condition):
    """Validation remains active under python -O."""
    if not condition:
        raise CeremonyError("ceremony validation failed")


_mutex_guard = threading.Lock()
_mutexes: dict[str, threading.RLock] = {}


def _mutex(path):
    with _mutex_guard:
        return _mutexes.setdefault(str(Path(path).resolve()), threading.RLock())


def _lock_file(handle, blocking=True):
    if os.name == "nt":
        import msvcrt
        handle.seek(0)
        msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK if blocking else msvcrt.LK_NBLCK, 1)
    else:
        import fcntl
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | (0 if blocking else fcntl.LOCK_NB))


def _unlock_file(handle):
    if os.name == "nt":
        import msvcrt
        handle.seek(0)
        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
    else:
        import fcntl
        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def atomic_json(path: Path, value: dict):
    """Durable private replacement; the stable companion lock is never replaced."""
    fd, name = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as out:
            json.dump(value, out, sort_keys=True, separators=(",", ":"), allow_nan=False)
            out.flush()
            os.fsync(out.fileno())
        os.replace(name, path)
        if os.name != "nt":
            directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
    finally:
        if os.path.exists(name):
            os.unlink(name)


class DaemonOwnership:
    """A nonblocking OS lock held for the entire daemon lifetime."""
    def __init__(self, path):
        self.path = Path(path)
        self.handle = None

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(self.path, os.O_RDWR | os.O_CREAT, 0o600)
        self.handle = os.fdopen(fd, "r+b")
        try:
            _lock_file(self.handle, blocking=False)
        except OSError:
            self.handle.close()
            self.handle = None
            raise CeremonyError("daemon ownership unavailable") from None
        return self

    def __exit__(self, *exc):
        if self.handle is not None:
            _unlock_file(self.handle)
            self.handle.close()
            self.handle = None


class CeremonyStore:
    def __init__(self, path=DEFAULT_STATE_PATH):
        self.path = Path(path)
        self.lock_path = self.path.with_suffix(self.path.suffix + ".lock")

    @contextmanager
    def locked(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with _mutex(self.lock_path):
            fd = os.open(self.lock_path, os.O_RDWR | os.O_CREAT, 0o600)
            with os.fdopen(fd, "r+b") as handle:
                _lock_file(handle)
                try:
                    yield handle
                finally:
                    _unlock_file(handle)

    def _read(self):
        try:
            obj = json.loads(self.path.read_text(encoding="utf-8"))
            require(type(obj["schema_version"]) is int and obj["schema_version"] == 1)
            require(isinstance(obj["boot_id"], str) and obj["boot_id"])
            require(type(obj["generation"]) is int and obj["generation"] >= 0)
            require(type(obj["enabled"]) is bool)
            require(isinstance(obj["ceremonies"], dict))
            require(isinstance(obj["tombstones"], dict))
            require(isinstance(obj["watermarks"], dict))
            require(obj["active"] is None or obj["active"] in obj["ceremonies"])
            for ident, item in obj["ceremonies"].items():
                require(item["state"] in STATES)
                require(item["manifest"]["ceremony_id"] == ident)
                require(isinstance(item["boot_id"], str))
                require(type(item["generation"]) is int)
                if item["state"] in CLAIMED:
                    require(ident in obj["tombstones"])
            return obj
        except (OSError, ValueError, KeyError, TypeError):
            raise CeremonyError("durable state unavailable or invalid") from None

    def read(self):
        with self.locked():
            return self._read()

    def boot(self, boot_id):
        """First boot provisions disabled state. A surviving lock marker forbids reset."""
        with self.locked() as handle:
            handle.seek(0)
            marker = handle.read()
            if not self.path.exists():
                if marker:
                    raise CeremonyError("durable state missing; restoration required")
                # Record the initialization BEFORE state creation; a crash fails closed.
                handle.seek(0)
                handle.write(b"initialized\n")
                handle.flush()
                os.fsync(handle.fileno())
                obj = dict(schema_version=1, boot_id=boot_id, generation=0,
                           enabled=False, active=None, ceremonies={}, tombstones={}, watermarks={})
            else:
                obj = self._read()
                # Idempotent same-boot calls cannot clear or re-enable any ceremony.
                if obj["boot_id"] == boot_id:
                    return
                obj["enabled"] = False
                for ident, item in obj["ceremonies"].items():
                    if item["state"] in {"READY", "DISABLED"}:
                        item["state"] = "CLOSED"
                        obj["tombstones"][ident] = {"reason": "boot_changed"}
                obj["boot_id"] = boot_id
                obj["active"] = None
                obj["generation"] += 1
            atomic_json(self.path, obj)

    def mutate(self, fn):
        with self.locked():
            obj = self._read()
            result = fn(obj)
            atomic_json(self.path, obj)
            return copy.deepcopy(result)

    def watermark(self, source_key, timestamp_ns):
        def advance(obj):
            previous = obj["watermarks"].get(source_key, -1)
            if timestamp_ns <= previous:
                return False
            obj["watermarks"][source_key] = timestamp_ns
            return True
        return self.mutate(advance)
