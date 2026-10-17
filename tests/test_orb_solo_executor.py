"""Source-free executor tests. No strategy, exports, scoring or MC."""
from dataclasses import replace
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from zoneinfo import ZoneInfo

import pytest

from discovery.orb_solo_executor import (
    AccountingGuard, Limits, Sample, StopExecution, admit_tier,
    verify_identity, run_owned, BudgetLedger,
)


def test_budget_preserves_historical_charge():
    limits = Limits()
    assert limits.prior_cpu_seconds == 8.04 * 3600
    assert limits.phase_cpu_seconds == 12 * 3600
    assert limits.total_cpu_seconds == 42 * 3600
    guard = AccountingGuard(limits)
    guard.observe(Sample(0, 0, 0, 0, 0))
    with pytest.raises(StopExecution, match='CPU'):
        guard.observe(Sample(1, (12 - 8.04) * 3600, 0, 0, 0))


@pytest.mark.parametrize('sample', [
    Sample(1, float('nan'), 0, 0, 0), Sample(1, -1, 0, 0, 0),
    Sample(1, 1, -1, 0, 0), Sample(1, 1, 0, -1, 0),
])
def test_invalid_measurement_refused(sample):
    with pytest.raises(StopExecution):
        AccountingGuard(Limits()).observe(sample)


def test_stale_and_decreasing_accounting_refused():
    guard = AccountingGuard(Limits(max_sample_gap=1))
    guard.observe(Sample(0, 2, 0, 0, 0))
    with pytest.raises(StopExecution, match='decreasing'):
        guard.observe(Sample(.1, 1, 0, 0, 0))
    with pytest.raises(StopExecution, match='stale'):
        guard.observe(Sample(2, 2, 0, 0, 0))


@pytest.mark.parametrize('field,value,reason', [
    ('memory_bytes', 16 * 1024**3, 'memory'),
    ('new_disk_bytes', 2 * 1024**3, 'disk'),
    ('elapsed', 48 * 3600, 'wall'),
])
def test_resource_thresholds(field, value, reason):
    sample = replace(Sample(0, 0, 0, 0, 0), **{field: value})
    with pytest.raises(StopExecution, match=reason):
        AccountingGuard(Limits()).observe(sample)


def test_identity_refuses_changed_missing_or_unlisted_file(tmp_path):
    source = tmp_path / 'source.txt'
    source.write_text('original')
    pins = {str(source): hashlib.sha256(source.read_bytes()).hexdigest()}
    verify_identity(pins)
    source.write_text('changed')
    with pytest.raises(StopExecution, match='identity'):
        verify_identity(pins)
    source.unlink()
    with pytest.raises(StopExecution):
        verify_identity(pins)
    with pytest.raises(StopExecution):
        verify_identity({})


def test_budget_ledger_never_resets_unknown_or_prior_charge(tmp_path):
    path = tmp_path/'budget.json'
    ledger = BudgetLedger.create(path)
    assert ledger.read()['charged_cpu_seconds'] == 8.04*3600
    ledger.begin()
    # Lost controller leaves a durable reservation and refuses another start.
    assert BudgetLedger(path).read()['status'] == 'running'
    with pytest.raises(StopExecution, match='unresolved'):
        BudgetLedger(path).begin()
    with pytest.raises(FileExistsError):
        BudgetLedger.create(path)
    ledger.finish(3, accounting_complete=False)
    assert ledger.read()['charged_cpu_seconds'] == 12*3600
    assert ledger.read()['status'] == 'unknown'
    with pytest.raises(StopExecution):
        ledger.begin()


def test_budget_ledger_charges_shutdown_and_rejects_decrease(tmp_path):
    ledger = BudgetLedger.create(tmp_path/'budget.json')
    ledger.begin()
    ledger.finish(2, accounting_complete=True)
    assert ledger.read()['charged_cpu_seconds'] == 8.04*3600+2+60
    assert ledger.read()['status'] == 'idle'
    with pytest.raises(StopExecution):
        ledger.finish(-1, accounting_complete=True)


def lot(entry='10:00', exit='11:00', qty=1):
    from types import SimpleNamespace
    ny = ZoneInfo('America/New_York')
    return SimpleNamespace(entry_ny=datetime.fromisoformat('2024-01-08T'+entry).replace(tzinfo=ny),
                           exit_ny=datetime.fromisoformat('2024-01-08T'+exit).replace(tzinfo=ny), qty=qty)


def test_admission_clock_cap_ties_and_missing_gates():
    kwargs = dict(micro_cap=2, g1=True, cost_multiple=4)
    assert admit_tier('MFFU_Rapid_100K', [lot()], **kwargs)['admissible']
    for exit in ('16:10', '16:11'):
        assert admit_tier('MFFU_Rapid_100K', [lot(exit=exit)], **kwargs)['reason'] == '16:10 unmodeled'
    assert not admit_tier('Bulenox_100K', [lot(qty=2), lot(entry='11:00')], **kwargs)['admissible']
    assert not admit_tier('Bulenox_100K', [lot()], **{**kwargs, 'g1':False})['admissible']
    assert not admit_tier('Bulenox_100K', [lot()], **{**kwargs, 'cost_multiple':3.99})['admissible']
    assert not admit_tier('FXIFY_Futures_Flex_100K', [lot()], **kwargs)['admissible']


@pytest.mark.skipif(os.name != 'nt', reason='real Windows Job capability required')
def test_native_completed_grandchild_cpu_and_no_orphans(tmp_path):
    # Work occurs in the grandchild, including after the immediate worker exits.
    child = "import time; end=time.process_time()+.20\nwhile time.process_time()<end: pass"
    code = f'import subprocess,sys; subprocess.Popen([sys.executable,"-c",{child!r}])'
    command = [sys.executable, '-c', code]
    result = run_owned([command], cwd=tmp_path, output=tmp_path/'evidence',
                       pins={str(Path(__file__)): hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
                       limits=replace(Limits(), poll_seconds=.02))
    assert result['status'] == 'completed'
    assert result['job_cpu_seconds'] >= .18
    assert result['active_processes'] == 0
    samples = result['samples']
    assert all(b['cpu_seconds'] >= a['cpu_seconds'] for a,b in zip(samples, samples[1:]))


@pytest.mark.skipif(os.name != 'nt', reason='real Windows Job capability required')
def test_native_cpu_stop_kills_busy_tree_and_preserves_receipt(tmp_path):
    command = [sys.executable, '-c', 'while True: pass']
    limits = replace(Limits(), prior_cpu_seconds=0, phase_cpu_seconds=1,
                     cpu_reserve_seconds=.5, poll_seconds=.02)
    result = run_owned([command], cwd=tmp_path, output=tmp_path/'evidence',
                       pins={str(Path(__file__)): hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
                       limits=limits)
    assert result['status'] == 'stopped'
    assert 'CPU' in result['reason']
    assert result['active_processes'] == 0
    assert result['cpu_seconds'] < 1
    assert json.loads((tmp_path/'evidence'/'receipt.json').read_text())['status'] == 'stopped'


def test_no_more_than_two_worker_roles_and_no_overwrite(tmp_path):
    pins = {str(Path(__file__)): hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    with pytest.raises(StopExecution, match='worker'):
        run_owned([[sys.executable, '-c', 'pass']]*3, cwd=tmp_path,
                  output=tmp_path/'evidence', pins=pins)
    (tmp_path/'existing').mkdir()
    with pytest.raises((FileExistsError, StopExecution)):
        run_owned([[sys.executable, '-c', 'pass']], cwd=tmp_path,
                  output=tmp_path/'existing', pins=pins)


@pytest.mark.skipif(os.name != 'nt', reason='real Windows Job capability required')
def test_native_disk_stop(tmp_path):
    output = tmp_path/'evidence'
    code = f"from pathlib import Path; import time; Path({str(output/'payload')!r}).write_bytes(b'x'*(2*1024**2)); time.sleep(5)"
    result = run_owned([[sys.executable, '-c', code]], cwd=tmp_path, output=output,
                       pins={str(Path(__file__)): hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
                       limits=replace(Limits(), disk_bytes=2*1024**2, disk_reserve_bytes=1024**2, poll_seconds=.02))
    assert result['status'] == 'stopped' and 'disk' in result['reason']
    assert result['active_processes'] == 0


@pytest.mark.skipif(os.name != 'nt', reason='real Windows Job capability required')
def test_native_memory_ceiling(tmp_path):
    result = run_owned([[sys.executable, '-c', "payload=bytearray(128*1024**2)"]], cwd=tmp_path,
                       output=tmp_path/'evidence',
                       pins={str(Path(__file__)): hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
                       limits=replace(Limits(), memory_bytes=1024**3+32*1024**2, poll_seconds=.02))
    assert result['status'] == 'stopped'
    assert result['active_processes'] == 0
    assert 'MemoryError' in (tmp_path/'evidence'/'worker-0.stderr').read_text()


@pytest.mark.skipif(os.name != 'nt', reason='real Windows Job capability required')
def test_controller_loss_closes_job_and_kills_worker(tmp_path):
    import ctypes
    from ctypes import wintypes
    worker_pid = tmp_path/'worker.pid'
    root = Path(__file__).resolve().parents[1]
    source = Path(__file__).resolve()
    child = f"import os,time; from pathlib import Path; Path({str(worker_pid)!r}).write_text(str(os.getpid())); time.sleep(30)"
    body = (
        f"import sys; sys.path[:0]=[{str(root)!r},{str(root/'lab')!r},{str(root/'core')!r}]; "
        "from discovery.orb_solo_executor import run_owned,BudgetLedger; "
        f"ledger=BudgetLedger.create({str(tmp_path/'budget.json')!r}); "
        f"run_owned([[sys.executable,'-c',{child!r}]], cwd={str(tmp_path)!r}, "
        f"output={str(tmp_path/'evidence')!r}, ledger=ledger, pins={{{str(source)!r}:{hashlib.sha256(source.read_bytes()).hexdigest()!r}}})"
    )
    # Base interpreter avoids killing just the venv forwarding launcher.
    controller = subprocess.Popen([sys._base_executable, '-c', body], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    handle = None
    try:
        deadline = time.monotonic()+8
        while not worker_pid.exists() and time.monotonic() < deadline and controller.poll() is None:
            time.sleep(.02)
        assert worker_pid.exists(), controller.communicate(timeout=1)
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        kernel.OpenProcess.restype = wintypes.HANDLE
        kernel.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        handle = kernel.OpenProcess(0x100000, False, int(worker_pid.read_text()))
        assert handle
        controller.kill()
        controller.communicate(timeout=5)
        assert kernel.WaitForSingleObject(handle, 5000) == 0
        # Interrupted controller cannot publish a successful terminal receipt.
        assert not (tmp_path/'evidence'/'receipt.json').exists()
        ledger = BudgetLedger(tmp_path/'budget.json')
        assert ledger.read()['reserved_upper_cpu_seconds'] == 12*3600
        with pytest.raises(StopExecution, match='unresolved'):
            ledger.begin()
    finally:
        if controller.poll() is None:
            controller.kill()
            controller.communicate(timeout=5)
        if handle:
            kernel.CloseHandle(handle)


@pytest.mark.skipif(os.name != 'nt', reason='real Windows Job capability required')
def test_missing_native_accounting_stops_owned_tree(tmp_path, monkeypatch):
    import discovery.orb_solo_executor as executor
    def unavailable(job):
        raise StopExecution('authoritative Job accounting unavailable')
    monkeypatch.setattr(executor, '_native_sample', unavailable)
    # Fault injection verifies refusal/cleanup; actual capability is tested above.
    result = run_owned([[sys.executable, '-c', 'import time; time.sleep(30)']],
                       cwd=tmp_path, output=tmp_path/'evidence',
                       pins={str(Path(__file__)): hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    assert result['status'] == 'stopped'
    assert not result['accounting_complete']
    assert 'accounting' in result['reason']


@pytest.mark.skipif(os.name != 'nt', reason='real Windows Job capability required')
def test_two_native_worker_roles_and_journal_seal(tmp_path):
    ledger = BudgetLedger.create(tmp_path/'budget.json')
    result = run_owned([[sys.executable, '-c', 'import time; time.sleep(.05)']]*2,
                       cwd=tmp_path, output=tmp_path/'evidence', ledger=ledger,
                       pins={str(Path(__file__)): hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    assert result['status'] == 'completed'
    assert result['active_processes'] == 0
    assert result['exit_codes'] == [0, 0]
    assert ledger.read()['charged_cpu_seconds'] >= 8.04*3600+60


@pytest.mark.skipif(os.name != 'nt', reason='real Windows Job capability required')
@pytest.mark.parametrize('failure', ['stale', 'decreasing'])
def test_accounting_fault_stops_running_tree(tmp_path, monkeypatch, failure):
    import discovery.orb_solo_executor as executor
    observe = AccountingGuard.observe
    observations = []
    def fault(self, sample):
        if observations and sample.active_processes:
            sample = replace(sample, **({'elapsed':10} if failure == 'stale' else {'cpu_seconds':-1}))
        observations.append(sample)
        return observe(self, sample)
    monkeypatch.setattr(AccountingGuard, 'observe', fault)
    result = executor.run_owned([[sys.executable, '-c', 'import time; time.sleep(30)']],
                                cwd=tmp_path, output=tmp_path/'evidence',
                                pins={str(Path(__file__)):hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    assert result['status'] == 'stopped'
    assert result['active_processes'] == 0
    assert result['accounting_complete']


@pytest.mark.skipif(os.name != 'nt', reason='real Windows Job capability required')
def test_completed_process_handles_do_not_accumulate(tmp_path):
    import ctypes
    from ctypes import wintypes
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.GetProcessHandleCount.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
    def count():
        value = wintypes.DWORD()
        assert kernel.GetProcessHandleCount(kernel.GetCurrentProcess(), ctypes.byref(value))
        return value.value
    before = count()
    for index in range(4):
        result = run_owned([[sys.executable, '-c', 'pass']], cwd=tmp_path,
                           output=tmp_path/f'evidence-{index}',
                           pins={str(Path(__file__)):hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
        assert result['status'] == 'completed'
    assert count() <= before+1
