"""Tests for core/lib/file_lock.py — portable exclusive advisory locking.

Two Windows regressions live here, both about the lock file itself:

* The lock file used to be bootstrapped by appending one byte through the
  ``a+b`` handle whenever ``tell() == 0``. The CRT append is seek-then-write,
  so callers touching the same fresh lock file together could write into the
  byte a sibling had just locked and raise ``PermissionError`` (the
  load-timing flake first seen in
  tests/ops/qualification/execution/test_files.py, worked around there by
  pre-warming the lock in fb8ac89). Windows byte-range locks may cover a
  region past end-of-file, so the payload was never needed: the lock file is
  now created empty and never written by anyone.
* The acquire used to be ``msvcrt.locking(LK_LOCK)``, which is not a blocking
  wait — the CRT retries once a second and gives up after ten attempts with
  ``OSError(EDEADLOCK)``. It now polls ``LK_NBLCK`` and waits indefinitely,
  like POSIX ``flock``.

Herd shape: one herd spreads small cohorts over many fresh paths (the
first-touch race), a second piles a large cohort onto a single path (the
wait), and a third runs the first-touch race across separate interpreters,
which share no in-process state.
"""
from __future__ import annotations

import errno
import os
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from lib import file_lock
from lib.file_lock import exclusive_file_lock

REPO_ROOT = Path(__file__).resolve().parents[2]
CORE_ROOT = REPO_ROOT / "core"


def _increment_under_lock(target: Path, rounds: int) -> None:
    """Read-modify-write a text counter ``rounds`` times under the lock."""
    for _ in range(rounds):
        with exclusive_file_lock(target):
            value = int(target.read_text(encoding="utf-8")) if target.exists() else 0
            target.write_text(str(value + 1), encoding="utf-8")


def _assert_counter_and_lock_file(target: Path, expected: int) -> None:
    """No lost updates, and a lock file nobody ever wrote to."""
    assert int(target.read_text(encoding="utf-8")) == expected
    lock_path = target.with_name(target.name + ".lock")
    assert lock_path.exists()
    assert lock_path.stat().st_size == 0


def test_thread_herd_on_fresh_lock_paths_has_no_lost_updates(tmp_path):
    """Cohorts racing the first touch of many fresh lock paths at once."""
    paths, cohort, rounds = 16, 3, 2
    targets = [tmp_path / f"counter-{index}.txt" for index in range(paths)]
    barrier = threading.Barrier(paths * cohort)
    errors: list[BaseException] = []

    def worker(target: Path) -> None:
        try:
            barrier.wait()  # every cohort hits its fresh lock path together
            _increment_under_lock(target, rounds)
        except BaseException as exc:  # pylint: disable=broad-except
            errors.append(exc)

    with ThreadPoolExecutor(max_workers=paths * cohort) as pool:
        futures = [pool.submit(worker, target) for target in targets for _ in range(cohort)]
        for future in futures:
            future.result()

    assert not errors, errors
    for target in targets:
        _assert_counter_and_lock_file(target, cohort * rounds)
    expected_names = sorted(
        name for target in targets for name in (target.name, target.name + ".lock")
    )
    assert sorted(path.name for path in tmp_path.iterdir()) == expected_names


def test_heavy_thread_contention_on_one_path_has_no_lost_updates(tmp_path):
    """The shape the old LK_LOCK acquire could not serve.

    16 threads x 25 rounds on one lock path holds the lock well past the
    CRT's ten-attempt give-up: on the previous acquire this raised
    ``OSError(36, 'Resource deadlock avoided')`` for five of the threads.
    """
    target = tmp_path / "counter.txt"
    workers, rounds = 16, 25
    barrier = threading.Barrier(workers)
    errors: list[BaseException] = []

    def worker() -> None:
        try:
            barrier.wait()
            _increment_under_lock(target, rounds)
        except BaseException as exc:  # pylint: disable=broad-except
            errors.append(exc)

    with ThreadPoolExecutor(max_workers=workers) as pool:
        for future in [pool.submit(worker) for _ in range(workers)]:
            future.result()

    assert not errors, errors
    _assert_counter_and_lock_file(target, workers * rounds)


_CHILD = """
import sys, time
from pathlib import Path
from lib.file_lock import exclusive_file_lock
target = Path(sys.argv[1]); rounds = int(sys.argv[2]); gate = Path(sys.argv[3])
deadline = time.monotonic() + 60
while not gate.exists():  # the cohort starts together on the fresh lock path
    if time.monotonic() > deadline:
        raise SystemExit("gate never opened")
    time.sleep(0.0005)
for _ in range(rounds):
    with exclusive_file_lock(target):
        value = int(target.read_text(encoding="utf-8")) if target.exists() else 0
        target.write_text(str(value + 1), encoding="utf-8")
"""


def test_process_herd_on_fresh_lock_paths_has_no_lost_updates(tmp_path):
    """The same first-touch race across interpreters, which share no locks."""
    paths, cohort, rounds = 3, 3, 2
    targets = [tmp_path / f"counter-{index}.txt" for index in range(paths)]
    gate = tmp_path / "go"
    env = {**os.environ, "PYTHONPATH": str(CORE_ROOT)}
    children = [
        subprocess.Popen(  # pylint: disable=consider-using-with
            [sys.executable, "-c", _CHILD, str(target), str(rounds), str(gate)],
            cwd=str(REPO_ROOT),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        for target in targets
        for _ in range(cohort)
    ]
    gate.write_text("go", encoding="utf-8")
    results = [child.communicate(timeout=120) for child in children]

    failures = [
        (child.returncode, err)
        for child, (_, err) in zip(children, results)
        if child.returncode != 0
    ]
    assert failures == []
    for target in targets:
        _assert_counter_and_lock_file(target, cohort * rounds)
    expected_names = sorted(
        ["go"] + [name for target in targets for name in (target.name, target.name + ".lock")]
    )
    assert sorted(path.name for path in tmp_path.iterdir()) == expected_names


def test_lock_file_is_created_empty_and_never_written(tmp_path):
    """The lock object is byte 0 of a zero-length file, on both platforms."""
    target = tmp_path / "state.json"
    lock_path = target.with_name(target.name + ".lock")
    with exclusive_file_lock(target):
        assert lock_path.stat().st_size == 0
    stamp = lock_path.stat().st_mtime_ns
    for _ in range(3):
        with exclusive_file_lock(target):
            pass
    assert lock_path.stat().st_size == 0
    assert lock_path.stat().st_mtime_ns == stamp
    assert sorted(path.name for path in tmp_path.iterdir()) == ["state.json.lock"]


def test_pre_existing_one_byte_lock_file_still_locks(tmp_path):
    """Lock files left by the previous implementation keep working."""
    target = tmp_path / "state.json"
    lock_path = target.with_name(target.name + ".lock")
    lock_path.write_bytes(b"\0")
    with exclusive_file_lock(target):
        pass
    assert lock_path.read_bytes() == b"\0"  # still never written by the lock


# The former acquire, msvcrt.locking(LK_LOCK), retried once a second and gave
# up after ten attempts. A wait that outlasts that bound is the regression, so
# this test costs its hold in wall clock; there is no shorter proof.
_CRT_GIVE_UP_SECONDS = 10.0
_HOLD_SECONDS = 11.0


@pytest.mark.skipif(os.name != "nt", reason="Windows acquire path only")
def test_windows_acquire_waits_past_the_crt_give_up(tmp_path):
    """The acquire waits for its turn instead of erroring after ~10s."""
    target = tmp_path / "state.json"
    holding = threading.Event()
    released: list[float] = []

    def holder() -> None:
        with exclusive_file_lock(target):
            holding.set()
            time.sleep(_HOLD_SECONDS)
            released.append(time.monotonic())

    thread = threading.Thread(target=holder)
    thread.start()
    try:
        assert holding.wait(timeout=30)
        started = time.monotonic()
        with exclusive_file_lock(target):
            acquired = time.monotonic()
    finally:
        thread.join(timeout=60)

    assert released, "holder never completed"
    assert acquired >= released[0]  # the wait outlasted the holder
    assert acquired - started > _CRT_GIVE_UP_SECONDS


@pytest.mark.skipif(os.name != "nt", reason="Windows acquire path only")
def test_windows_acquire_propagates_unexpected_errors(tmp_path, monkeypatch):
    """Only EACCES means contention; anything else must not be polled on."""
    calls: list[int] = []

    def locking(fd, mode, nbytes):  # pylint: disable=unused-argument
        calls.append(mode)
        raise OSError(errno.EIO, "Input/output error")

    monkeypatch.setattr(file_lock.msvcrt, "locking", locking)
    with pytest.raises(OSError) as raised:
        with exclusive_file_lock(tmp_path / "state.json"):
            pass
    assert raised.value.errno == errno.EIO
    assert calls == [file_lock.msvcrt.LK_NBLCK]  # first attempt, no spin
