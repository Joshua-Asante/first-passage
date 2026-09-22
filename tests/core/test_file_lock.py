"""Tests for core/lib/file_lock.py — portable exclusive advisory locking.

Regression: on Windows the lock file used to be bootstrapped by appending
one byte through an ``a+b`` handle whenever ``tell() == 0``. The CRT append
is seek-then-write, so callers bootstrapping the same fresh lock file
together could append into the byte a sibling had just locked and raise
``PermissionError`` (load-timing flake first seen in
tests/ops/qualification/execution/test_files.py, worked around there by
pre-warming the lock in fb8ac89). The lock file must now be published
race-free, and a herd must observe mutual exclusion on both platforms.

Herd shape: the race lives in the first touch of a fresh path, so the herd
spreads over many fresh paths with a small cohort per path, all released
from one barrier. Cohorts stay small because the Windows acquire is
``msvcrt.LK_LOCK`` (retry once per second, ten attempts), so a large cohort
on one path starves rather than blocks — that wait strategy is unchanged
here and bounds how much contention a single path can carry.
"""
from __future__ import annotations

import os
import subprocess
import sys
import threading
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
    assert int(target.read_text(encoding="utf-8")) == expected
    lock_path = target.with_name(target.name + ".lock")
    assert lock_path.exists()
    if os.name == "nt":
        assert lock_path.read_bytes() == b"\0"


def test_thread_herd_on_fresh_lock_paths_has_no_lost_updates(tmp_path):
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


def test_sequential_sessions_reuse_the_published_lock_file(tmp_path):
    target = tmp_path / "state.json"
    lock_path = target.with_name(target.name + ".lock")
    with exclusive_file_lock(target):
        pass
    before = lock_path.read_bytes()
    stamp = lock_path.stat().st_mtime_ns
    for _ in range(3):
        with exclusive_file_lock(target):
            pass
    assert lock_path.read_bytes() == before
    if os.name == "nt":
        assert before == b"\0"
        assert lock_path.stat().st_mtime_ns == stamp  # never written again
    assert sorted(path.name for path in tmp_path.iterdir()) == ["state.json.lock"]


@pytest.mark.skipif(os.name != "nt", reason="Windows bootstrap path only")
def test_windows_bootstrap_loser_discards_its_temp_file(tmp_path, monkeypatch):
    target = tmp_path / "state.json"
    lock_path = target.with_name(target.name + ".lock")
    real_mkstemp = file_lock.tempfile.mkstemp

    def mkstemp_then_sibling_publishes(*args, **kwargs):
        fd, name = real_mkstemp(*args, **kwargs)
        lock_path.write_bytes(b"\0")  # a sibling won the bootstrap first
        return fd, name

    monkeypatch.setattr(file_lock.tempfile, "mkstemp", mkstemp_then_sibling_publishes)
    with exclusive_file_lock(target):
        pass
    assert lock_path.read_bytes() == b"\0"
    assert sorted(path.name for path in tmp_path.iterdir()) == ["state.json.lock"]
