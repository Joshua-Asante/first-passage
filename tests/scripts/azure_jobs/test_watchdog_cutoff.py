"""Synthetic shutdown regressions: no Azure, credentials or real guest required."""
import json
import os
from pathlib import Path
import sys
import threading
import time
from types import SimpleNamespace

import pytest

from scripts.azure_jobs import watchdog
from scripts.azure_jobs.control import atomic


class Stopped(BaseException):
    pass


def test_stalled_recovery_bundle_cannot_veto_deallocation(tmp_path, monkeypatch):
    job = tmp_path / 'jobs/job'
    atomic(tmp_path / 'config.json', {'guest_root': str(tmp_path)})
    atomic(job / 'spec.json', {'expected_outputs': ['out']})
    atomic(job / 'state.json', {'status': 'running', 'phase': 'executing'})
    atomic(job / 'heartbeat.json', {'time': 0})
    (job / 'stdout.log').write_text('retained partial output')
    lease = {'job_id': 'job', 'deadline': 2000, 'bootstrap_deadline': 500}
    clock = [1000.0]
    bundling = threading.Event()
    release = threading.Event()
    deallocated = threading.Event()
    workers = []
    errors = []

    def stalled_bundle(*args, **kwargs):
        clock[0] = lease['deadline'] + 1
        bundling.set()
        release.wait(5)  # Outer test cleanup bounds even the pre-fix reproduction.
        raise OSError('synthetic stalled bundler stopped')

    class Owned:
        @staticmethod
        def create():
            return Owned()

        def close(self):
            release.set()  # Model kill-on-close without waiting for publication.

    def spawn(command, cwd, stdout, stderr, job=None):
        def run():
            try:
                watchdog.recover({'guest_root': str(tmp_path)}, lease, 'guest supervisor lost')
            except OSError:
                pass
        worker = threading.Thread(target=run)
        workers.append(worker)
        worker.start()
        assert bundling.wait(2)

        class Process:
            def poll(self):
                return None
        return Process()

    class FakeAzure:
        def __init__(self, config):
            pass

        def deallocate(self):
            deallocated.set()
            raise Stopped()

    monkeypatch.setattr(watchdog, 'Azure', FakeAzure)
    monkeypatch.setattr(watchdog, 'cloud_lease', lambda: dict(lease))
    monkeypatch.setattr(watchdog, 'terminate_tree', lambda name: True)
    monkeypatch.setattr(watchdog, 'bundle', stalled_bundle)
    monkeypatch.setattr(watchdog.time, 'time', lambda: clock[0])
    monkeypatch.setattr(watchdog.time, 'monotonic', lambda: clock[0])
    # These dependency names are absent before the fix; raising=False lets the
    # identical regression exercise the original synchronous recovery path.
    monkeypatch.setattr(watchdog, 'WindowsJob', Owned, raising=False)
    monkeypatch.setattr(watchdog, 'spawn_provider', spawn, raising=False)

    def run_watchdog():
        try:
            watchdog.main(tmp_path / 'config.json')
        except Stopped:
            pass
        except BaseException as exc:
            errors.append(exc)

    parent = threading.Thread(target=run_watchdog)
    parent.start()
    try:
        assert bundling.wait(2)
        assert deallocated.wait(1), 'stalled bundling blocked deallocation past the lease deadline'
        assert not errors
    finally:
        release.set()
        parent.join(2)
        for worker in workers:
            worker.join(2)
    assert not parent.is_alive()
    assert (job / 'stdout.log').read_text() == 'retained partial output'
    record = json.loads((job / 'record.json').read_text())
    assert record['status'] == 'interrupted'
    assert record['capture_complete'] is False
    assert not (job / 'archive.json').exists()


def test_expired_lease_bypasses_recovery_and_boot_grace(tmp_path, monkeypatch):
    atomic(tmp_path / 'config.json', {'guest_root': str(tmp_path)})
    class FakeAzure:
        def __init__(self, config):
            pass

        def deallocate(self):
            raise Stopped()
    monkeypatch.setattr(watchdog, 'Azure', FakeAzure)
    monkeypatch.setattr(watchdog, 'cloud_lease', lambda: {'job_id': 'job', 'deadline': 100, 'bootstrap_deadline': 50})
    monkeypatch.setattr(watchdog.time, 'time', lambda: 101)
    monkeypatch.setattr(watchdog.time, 'monotonic', lambda: 0)
    monkeypatch.setattr(watchdog.time, 'sleep', lambda _: pytest.fail('expired lease waited through boot grace'))
    monkeypatch.setattr(watchdog, 'recover', lambda *a: pytest.fail('recovery started after cutoff'))
    monkeypatch.setattr(watchdog, 'terminate_tree', lambda *a: True)
    with pytest.raises(Stopped):
        watchdog.main(tmp_path / 'config.json')


@pytest.mark.parametrize('stop_fails', [False, True])
@pytest.mark.parametrize('mapping_matches', [False, True])
def test_expired_lease_stops_only_owned_job_despite_cloud_failure(
        tmp_path, monkeypatch, stop_fails, mapping_matches):
    """Exercise the actual native-stop wrapper with synthetic kernel/Azure APIs.

    The supervisor does no work or timeout polling. The watchdog must stop its
    named workload even when every deallocation attempt fails, and keep retrying
    without archive work, process enumeration or waits on workload completion.
    """
    import ctypes
    atomic(tmp_path / 'config.json', {'guest_root': str(tmp_path)})
    atomic(tmp_path / 'control/sessions/session.json', {
        'session_id': 'session' if mapping_matches else 'other-session',
        'source_job_id': 'original' if mapping_matches else 'unrelated',
    })
    lease = {'job_id': 'session', 'deadline': 100, 'bootstrap_deadline': 50}
    owned_name = 'Local\\FP-Offline-' + ('original' if mapping_matches else 'session')
    live = {owned_name, 'Local\\FP-Offline-unrelated'}
    calls = []
    attempts = []
    clock = [101.0]

    class NativeCall:
        def __init__(self, fn):
            self.fn = fn

        def __call__(self, *args):
            return self.fn(*args)

    def open_job(access, inherit, name):
        assert (access, inherit, name) == (8, False, owned_name)
        calls.append('open')
        return 123

    def terminate(handle, code):
        assert (handle, code) == (123, 130)
        calls.append('terminate')
        if stop_fails:
            return False
        live.discard(owned_name)
        return True

    def close(handle):
        assert handle == 123
        calls.append('close')

    kernel = SimpleNamespace(OpenJobObjectW=NativeCall(open_job),
                             TerminateJobObject=NativeCall(terminate),
                             CloseHandle=NativeCall(close))
    monkeypatch.setattr(ctypes, 'WinDLL', lambda *a, **k: kernel, raising=False)

    class FakeAzure:
        def __init__(self, config):
            pass

        def deallocate(self):
            calls.append('deallocate')
            attempts.append(clock[0])
            if not stop_fails:
                assert owned_name not in live, 'stalled supervisor left workload running'
            assert 'Local\\FP-Offline-unrelated' in live
            raise OSError('synthetic Azure outage')

    def sleep(seconds):
        assert seconds == 5
        calls.append('sleep')
        clock[0] += seconds
        if len(attempts) == 3:
            raise Stopped()

    monkeypatch.setattr(watchdog, 'Azure', FakeAzure)
    monkeypatch.setattr(watchdog, 'cloud_lease', lambda: dict(lease))
    monkeypatch.setattr(watchdog, 'time', SimpleNamespace(
        time=lambda: clock[0], monotonic=lambda: clock[0], sleep=sleep))
    monkeypatch.setattr(watchdog, 'bounded_recover', lambda *a: pytest.fail('archive recovery after expiry'))
    with pytest.raises(Stopped):
        watchdog.main(tmp_path / 'config.json')
    assert calls == ['open', 'terminate', 'close', 'deallocate', 'sleep'] * 3
    assert attempts == [101, 106, 111]


@pytest.mark.parametrize('code,expected', [(0, True), (75, False), (1, RuntimeError)])
def test_recovery_worker_result_and_ownership_cleanup(tmp_path, monkeypatch, code, expected):
    closed = []
    owned = SimpleNamespace(close=lambda: closed.append(True))
    monkeypatch.setattr(watchdog.WindowsJob, 'create', lambda: owned)
    commands = []
    def spawn(command, cwd, stdout, stderr, job):
        commands.append(command)
        assert job is owned
        return SimpleNamespace(poll=lambda: code)
    monkeypatch.setattr(watchdog, 'spawn_provider', spawn)
    lease = {'job_id': 'session', 'source_job_id': 'original', 'deadline': time.time() + 60}
    if expected is RuntimeError:
        with pytest.raises(RuntimeError, match='recovery failed'):
            watchdog.bounded_recover(tmp_path / 'config.json', lease, 'cancelled')
    else:
        assert watchdog.bounded_recover(tmp_path / 'config.json', lease, 'cancelled') is expected
    assert json.loads(commands[0][-2]) == lease
    assert commands[0][0] == sys.executable
    assert closed == [True]


@pytest.mark.parametrize('wall_step', [0, -10, 10])
def test_recovery_cutoff_survives_wall_clock_stall_or_jump(tmp_path, monkeypatch, wall_step):
    clock = [1000.0, 0.0]
    closed = []
    owned = SimpleNamespace(close=lambda: closed.append(True))
    monkeypatch.setattr(watchdog.WindowsJob, 'create', lambda: owned)
    monkeypatch.setattr(watchdog, 'spawn_provider', lambda *a, **k: SimpleNamespace(poll=lambda: None))
    def sleep(seconds):
        clock[0] += wall_step
        clock[1] += seconds
    monkeypatch.setattr(watchdog, 'time', SimpleNamespace(
        time=lambda: clock[0], monotonic=lambda: clock[1], sleep=sleep))
    with pytest.raises(TimeoutError, match='cutoff'):
        watchdog.bounded_recover(tmp_path / 'config.json', {'deadline': 1001}, 'cancelled')
    assert clock[1] <= 1
    assert closed == [True]


def test_recovery_has_a_publication_cap_even_before_lease_deadline(tmp_path, monkeypatch):
    clock = [0.0]
    owned = SimpleNamespace(close=lambda: None)
    monkeypatch.setattr(watchdog.WindowsJob, 'create', lambda: owned)
    monkeypatch.setattr(watchdog, 'spawn_provider', lambda *a, **k: SimpleNamespace(poll=lambda: None))
    def sleep(seconds):
        clock[0] += seconds
    monkeypatch.setattr(watchdog, 'time', SimpleNamespace(
        time=lambda: 1000, monotonic=lambda: clock[0], sleep=sleep))
    with pytest.raises(TimeoutError):
        watchdog.bounded_recover(tmp_path / 'config.json', {'deadline': 100000}, 'cancelled')
    assert clock[0] == watchdog.PUBLICATION_SECONDS


def test_recovery_spawn_and_diagnostic_failure_still_deallocate(tmp_path, monkeypatch):
    atomic(tmp_path / 'config.json', {'guest_root': str(tmp_path)})
    lease = {'job_id': 'job', 'deadline': 2000, 'bootstrap_deadline': 500}
    def fail(*args, **kwargs):
        raise OSError('synthetic failure')
    class FakeAzure:
        def __init__(self, config):
            pass

        def deallocate(self):
            raise Stopped()
    monkeypatch.setattr(watchdog, 'Azure', FakeAzure)
    monkeypatch.setattr(watchdog, 'cloud_lease', lambda: lease)
    monkeypatch.setattr(watchdog, 'bounded_recover', fail)
    monkeypatch.setattr(watchdog, 'terminate_tree', lambda *a: True)
    monkeypatch.setattr(watchdog, 'print', fail, raising=False)
    monkeypatch.setattr(watchdog, 'time', SimpleNamespace(time=lambda: 1000, monotonic=lambda: 0))
    with pytest.raises(Stopped):
        watchdog.main(tmp_path / 'config.json')


@pytest.mark.skipif(os.name != 'nt', reason='real Windows recovery worker Job Object')
def test_windows_stalled_bundle_worker_is_killed_and_disk_evidence_republishable(tmp_path, monkeypatch):
    """Local synthetic worker only; every workload and upload action is replaced."""
    from scripts.azure_jobs import guest
    from scripts.azure_jobs.contract import verify_inventory
    job = tmp_path / 'jobs/job'
    repo = tmp_path / 'repos/job'
    repo.mkdir(parents=True)
    (repo / 'out').write_text('synthetic partial output')
    spec = dict(job_id='job', commit='a' * 40, command=['fake.py'], environment='research',
                max_wall_seconds=60, expected_outputs=['out'], authority='synthetic test', private_inputs=[])
    atomic(job / 'spec.json', spec)
    atomic(tmp_path / 'config.json', {'guest_root': str(tmp_path)})
    marker = tmp_path / 'bundling'
    natural_completion = tmp_path / 'natural-completion'
    wrapper = tmp_path / 'stall.py'
    wrapper.write_text(
        'import sys, runpy, time\nfrom pathlib import Path\n'
        f'sys.path.insert(0, {str(Path(watchdog.__file__).resolve().parents[2])!r})\n'
        'from scripts.azure_jobs import watchdog\n'
        'watchdog.terminate_tree = lambda name: True\n'
        'def stall(*args, **kwargs):\n'
        f'    Path({str(marker)!r}).write_text("entered")\n'
        '    time.sleep(60)\n'
        f'    Path({str(natural_completion)!r}).write_text("completed naturally")\n'
        'watchdog.bundle = stall\n'
        f'runpy.run_path({str(Path(watchdog.__file__).with_name("guest_entry.py"))!r}, run_name="__main__")\n')
    original_spawn = watchdog.spawn_provider
    processes = []
    def spawn(command, cwd, stdout, stderr, job):
        process = original_spawn([*command[:2], str(wrapper), *command[3:]], cwd, stdout, stderr, job=job)
        processes.append(process)
        # Establish the stall before moving the parent's synthetic clock.
        deadline = time.monotonic() + 10
        while not marker.exists() and time.monotonic() < deadline:
            time.sleep(0.01)
        assert marker.exists(), 'worker did not enter bundling'
        assert process.poll() is None, 'worker exited before the cutoff'
        clock[0] = 2001
        return process
    clock = [1000]
    monkeypatch.setattr(watchdog, 'spawn_provider', spawn)
    monkeypatch.setattr(watchdog, 'time', SimpleNamespace(
        time=lambda: clock[0], monotonic=time.monotonic, sleep=time.sleep))
    with pytest.raises(TimeoutError):
        watchdog.bounded_recover(tmp_path / 'config.json', {'job_id': 'job', 'deadline': 2000}, 'guest supervisor lost')
    stopped_at = time.monotonic()
    for process in processes:
        process.wait(timeout=5)  # Kill-on-close guarantees exit, not its status code.
    assert time.monotonic() - stopped_at < 5
    assert not natural_completion.exists(), 'worker completed its stalled bundle naturally'
    before = (job / 'record.json').read_bytes()
    monkeypatch.setattr(guest, 'upload', lambda *a: None)
    for name in ('checkout', 'environment', 'run_tree'):
        monkeypatch.setattr(guest, name, lambda *a: pytest.fail('replayed workload'))
    guest.republish({'guest_root': str(tmp_path), 'session_id': 'maintenance'}, spec)
    assert (job / 'record.json').read_bytes() == before
    assert json.loads(before)['status'] == 'interrupted'
    rows = json.loads((job / 'manifest.json').read_text())
    verify_inventory(repo, {name: row for name, row in rows.items() if not name.startswith('runner/')})
