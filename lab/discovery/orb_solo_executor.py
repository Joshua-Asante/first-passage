"""Study-scoped Windows resource boundary. No scoring entry point.

Commands are owned before resume; Job accounting includes exited descendants.
Controller CPU is separate and added once. Receipts never authorize a run.
Polling disk/controller-memory guards require a bounded writer/controller; until
the scoring adapter supplies those bounds this module is not scoring readiness.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from collections import deque
from datetime import time as clock_time
import hashlib
import json
import math
import os
from pathlib import Path
import time
from zoneinfo import ZoneInfo

TIERS = ('Bulenox_100K', 'Tradeify_Select_100K', 'MFFU_Rapid_100K', 'BluSky_Premium_100K')


class StopExecution(RuntimeError):
    """An unavailable or exceeded control fails closed."""


class BudgetLedger:
    """Exclusive setup-phase debit journal. A lost lease is never auto-resumed.

    Candidate/reference phase transitions are deliberately absent. The scoring
    adapter must separately bind its phase journal before it can be released.
    """
    def __init__(self, path):
        self.path = Path(path)
        self.lock = self.path.with_suffix(self.path.suffix+'.lock')
        self.owned = False

    @classmethod
    def create(cls, path):
        ledger = cls(path)
        with ledger.path.open('x', encoding='utf-8') as handle:
            json.dump(dict(status='idle', charged_cpu_seconds=8.04*3600,
                           phase_cap_seconds=12*3600, total_cap_seconds=42*3600), handle)
            handle.flush()
            os.fsync(handle.fileno())
        return ledger

    def read(self):
        try:
            state = json.loads(self.path.read_text(encoding='utf-8'))
            if state['status'] not in ('idle', 'running', 'unknown', 'exhausted') or not math.isfinite(state['charged_cpu_seconds']):
                raise ValueError('invalid journal')
            if state['charged_cpu_seconds'] < 8.04*3600 or state['phase_cap_seconds'] != 12*3600 or state['total_cap_seconds'] != 42*3600:
                raise ValueError('journal policy drift')
            return state
        except (OSError, ValueError, KeyError, TypeError) as exc:
            raise StopExecution('budget journal unavailable or invalid') from exc

    def _write(self, state):
        pending = self.path.with_suffix(self.path.suffix+'.pending')
        with pending.open('x', encoding='utf-8') as handle:
            json.dump(state, handle, allow_nan=False)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(pending, self.path)

    def begin(self):
        try:
            with self.lock.open('x', encoding='utf-8') as handle:
                handle.write(str(os.getpid()))
                handle.flush()
                os.fsync(handle.fileno())
        except FileExistsError as exc:
            raise StopExecution('unresolved budget lease; no restart') from exc
        self.owned = True
        state = self.read()
        if state['status'] != 'idle' or state['charged_cpu_seconds']+60 >= state['phase_cap_seconds']:
            # Preserve the lease too: a failed start cannot silently release it.
            raise StopExecution('unresolved or exhausted budget; no restart')
        state.update(status='running', reserved_upper_cpu_seconds=state['phase_cap_seconds'])
        self._write(state)
        return state['charged_cpu_seconds']

    def finish(self, cpu_seconds, *, accounting_complete):
        if not self.owned or not math.isfinite(cpu_seconds) or cpu_seconds < 0:
            raise StopExecution('invalid or unowned budget completion')
        state = self.read()
        if state['status'] != 'running':
            raise StopExecution('budget completion without running lease')
        if accounting_complete:
            # Charge a full shutdown/seal reserve, including work after the final
            # native sample and journal/receipt publication; never credit it back.
            charged = state['charged_cpu_seconds']+cpu_seconds+60
            state.update(charged_cpu_seconds=charged,
                         status='idle' if charged < state['phase_cap_seconds'] else 'exhausted')
        else:
            state.update(charged_cpu_seconds=state['reserved_upper_cpu_seconds'], status='unknown')
        self._write(state)
        self.lock.unlink()
        self.owned = False
        return state


@dataclass(frozen=True)
class Limits:
    prior_cpu_seconds: float = 8.04 * 3600
    phase_cpu_seconds: float = 12 * 3600
    total_cpu_seconds: float = 42 * 3600
    cpu_reserve_seconds: float = 60
    wall_seconds: float = 48 * 3600
    memory_bytes: int = 16 * 1024**3
    disk_bytes: int = 2 * 1024**3
    disk_reserve_bytes: int = 64 * 1024**2
    poll_seconds: float = .05
    max_sample_gap: float = 1

    def validate(self):
        values = asdict(self)
        if any(not math.isfinite(v) or v < 0 for v in values.values()):
            raise StopExecution('invalid resource limits')
        if not 0 < self.poll_seconds < self.max_sample_gap:
            raise StopExecution('invalid polling interval')
        if self.cpu_reserve_seconds >= min(self.phase_cpu_seconds, self.total_cpu_seconds) - self.prior_cpu_seconds:
            raise StopExecution('no CPU shutdown reserve')
        if self.disk_reserve_bytes >= self.disk_bytes:
            raise StopExecution('no disk shutdown reserve')


@dataclass(frozen=True)
class Sample:
    elapsed: float
    cpu_seconds: float
    memory_bytes: int
    new_disk_bytes: int
    active_processes: int


class AccountingGuard:
    def __init__(self, limits: Limits):
        limits.validate()
        self.limits = limits
        self.previous = None

    def observe(self, sample: Sample):
        if any(not math.isfinite(v) or v < 0 for v in asdict(sample).values()):
            raise StopExecution('missing or invalid accounting')
        if self.previous:
            if sample.elapsed < self.previous.elapsed or sample.cpu_seconds < self.previous.cpu_seconds:
                raise StopExecution('decreasing accounting')
            if sample.elapsed - self.previous.elapsed > self.limits.max_sample_gap:
                raise StopExecution('stale accounting')
        self.previous = sample
        limit = self.limits
        if sample.cpu_seconds + limit.prior_cpu_seconds >= min(limit.phase_cpu_seconds, limit.total_cpu_seconds) - limit.cpu_reserve_seconds:
            raise StopExecution('CPU shutdown threshold')
        if sample.elapsed >= limit.wall_seconds - limit.max_sample_gap:
            raise StopExecution('wall shutdown threshold')
        if sample.memory_bytes >= limit.memory_bytes:
            raise StopExecution('memory shutdown threshold')
        if sample.new_disk_bytes >= limit.disk_bytes - limit.disk_reserve_bytes:
            raise StopExecution('disk shutdown threshold')


def verify_identity(pins: dict[str, str]):
    if not pins:
        raise StopExecution('empty identity pins')
    for name, digest in pins.items():
        try:
            path = Path(name)
            if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                raise StopExecution(f'identity drift: {path.name}')
        except OSError as exc:
            raise StopExecution('identity input unavailable') from exc


def admit_tier(tier, trades, *, micro_cap, g1, cost_multiple):
    """Structural predicate only; callers must bind G1/G2 evidence to frozen pins.

    Entry sorts before exit at ties: a just-closing lot still consumes capacity.
    """
    def reject(reason):
        return dict(admissible=False, reason=reason)
    if tier not in TIERS:
        return reject('tier outside frozen four; FXIFY conditional')
    if g1 is not True or not math.isfinite(cost_multiple) or cost_multiple < 4:
        return reject('G1/G2 evidence missing or insufficient')
    if type(micro_cap) is not int or micro_cap <= 0 or not trades:
        return reject('invalid capacity or empty lots')
    events = []
    ny = ZoneInfo('America/New_York')
    for trade in trades:
        entry, exit_ = trade.entry_ny, trade.exit_ny
        if entry.utcoffset() is None or exit_.utcoffset() is None:
            return reject('timezone missing')
        entry, exit_ = entry.astimezone(ny), exit_.astimezone(ny)
        if entry.date() != exit_.date() or exit_ < entry or not math.isfinite(trade.qty) or trade.qty <= 0 or int(trade.qty) != trade.qty:
            return reject('invalid lot interval or quantity')
        if tier == 'MFFU_Rapid_100K' and exit_.time() >= clock_time(16, 10):
            return reject('16:10 unmodeled')
        events.extend(((entry, 0, trade.qty), (exit_, 1, -trade.qty)))
    quantity = peak = 0
    for _, _, change in sorted(events):
        quantity += change
        peak = max(peak, quantity)
    if peak > micro_cap:
        return reject('concurrent micro_contract_cap exceeded')
    return dict(admissible=True, reason='structural predicates satisfied', peak_micro_contracts=peak)


def _native_types(job):
    cached=getattr(job,'_orb_native_types',None)
    if cached is not None:
        return cached
    c, w = job._ctypes, job._wintypes
    class Basic(c.Structure):
        _fields_ = [('process_time', c.c_int64), ('job_time', c.c_int64),
                    ('flags', w.DWORD), ('minimum_ws', c.c_size_t), ('maximum_ws', c.c_size_t),
                    ('active_limit', w.DWORD), ('affinity', c.c_size_t),
                    ('priority', w.DWORD), ('scheduling', w.DWORD)]
    class IO(c.Structure):
        _fields_ = [(name, c.c_uint64) for name in ('read_ops', 'write_ops', 'other_ops', 'read_bytes', 'write_bytes', 'other_bytes')]
    class Extended(c.Structure):
        _fields_ = [('basic', Basic), ('io', IO), ('process_memory', c.c_size_t),
                    ('job_memory', c.c_size_t), ('peak_process', c.c_size_t), ('peak_job', c.c_size_t)]
    class Memory(c.Structure):
        _fields_ = [('cb', w.DWORD), ('faults', w.DWORD)] + [(name, c.c_size_t) for name in (
            'peak_ws', 'ws', 'peak_paged', 'paged', 'peak_nonpaged', 'nonpaged', 'pagefile', 'peak_pagefile', 'private')]
    job._orb_native_types=(Extended,Memory)
    return job._orb_native_types


def _set_native_limits(job, memory_bytes):
    c = job._ctypes
    Extended, _ = _native_types(job)
    limits = Extended()
    # Hard aggregate committed-memory ceiling for every descendant, including
    # venv launchers. Keep 1 GiB of the total for the controller.
    limits.basic.flags = job.JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE | 0x200
    limits.job_memory = memory_bytes - 1024**3
    if limits.job_memory <= 0 or not job._kernel.SetInformationJobObject(job.handle, 9, c.byref(limits), c.sizeof(limits)):
        raise StopExecution('native aggregate memory limit unavailable')


def _native_sample(job):
    c, w = job._ctypes, job._wintypes
    Extended, Memory = _native_types(job)
    basic, extended, returned = job._accounting(), Extended(), w.DWORD()
    for kind, value in ((1, basic), (9, extended)):
        if not job._kernel.QueryInformationJobObject(job.handle, kind, c.byref(value), c.sizeof(value), c.byref(returned)):
            raise StopExecution('authoritative Job accounting unavailable')
    kernel = job._kernel
    kernel.GetCurrentProcess.restype = w.HANDLE
    psapi=getattr(job,'_orb_psapi',None)
    if psapi is None:
        psapi=c.WinDLL('psapi',use_last_error=True)
        psapi.GetProcessMemoryInfo.argtypes=[w.HANDLE,w.LPVOID,w.DWORD]
        psapi.GetProcessMemoryInfo.restype=w.BOOL
        job._orb_psapi=psapi
    memory = Memory()
    memory.cb = c.sizeof(memory)
    if not psapi.GetProcessMemoryInfo(kernel.GetCurrentProcess(), c.byref(memory), c.sizeof(memory)):
        raise StopExecution('controller memory accounting unavailable')
    if memory.private >= 1024**3:
        raise StopExecution('controller memory reserve exceeded')
    # Total*Time retains exited-process CPU. Do not add per-PID/worker totals.
    return ((basic.TotalUserTime + basic.TotalKernelTime) / 10_000_000,
            int(extended.peak_job + memory.private), int(basic.ActiveProcesses))


def _disk_bytes(root):
    total = 0
    for path in root.rglob('*'):
        if path.is_symlink():
            raise StopExecution('output symlink refused')
        if path.is_file():
            total += path.stat().st_size
    return total


def run_owned(commands, *, cwd, output, pins, limits=Limits(), ledger=None, sample_capacity=4096):
    """Run at most two exact worker-role commands; descendants stay in one Job.

    This low-level boundary deliberately has no CLI or scoring authorization.
    A future adapter must pin commands, bound writers and assert tier evidence.
    Synthetic tests may call it directly. Never auto-resume a stopped receipt.
    """
    started, controller_start = time.monotonic(), time.process_time()
    limits.validate()
    if type(sample_capacity) is not int or not 1 <= sample_capacity <= 4096:
        raise StopExecution('invalid bounded sample capacity')
    if not 1 <= len(commands) <= 2 or any(not cmd or not all(isinstance(arg, str) for arg in cmd) for cmd in commands):
        raise StopExecution('one or two explicit worker commands required')
    if os.name != 'nt':
        raise StopExecution('Windows Job capability required')
    if ledger is not None:
        prior = ledger.begin()
        if limits.prior_cpu_seconds != prior or limits.phase_cpu_seconds != 12*3600 or limits.total_cpu_seconds != 42*3600:
            raise StopExecution('limits disagree with durable budget journal')
    verify_identity(pins)
    from scripts.agent_handoff import WindowsJob, _spawn_windows_suspended_in_job
    output = Path(output)
    if output.is_symlink():
        raise StopExecution('output symlink refused')
    output.mkdir(parents=True, exist_ok=False)
    guard = AccountingGuard(limits)
    guard.observe(Sample(0, 0, 0, 0, 0))
    processes, handles, samples = [], [], deque(maxlen=sample_capacity)
    sampling=dict(observations=0,first=None,memory_bytes_max=0,active_processes_max=0)
    job = None
    receipt = dict(status='stopped', reason='incomplete setup', limits=asdict(limits),
                   command_sha256=hashlib.sha256(json.dumps(commands).encode()).hexdigest(),
                   pins=pins, accounting_complete=False, active_processes=None)
    last_job_cpu = 0
    try:
        job = WindowsJob.create()
        _set_native_limits(job, limits.memory_bytes)
        for number, command in enumerate(commands):
            stdout = (output/f'worker-{number}.stdout').open('wb')
            stderr = (output/f'worker-{number}.stderr').open('wb')
            handles.extend((stdout, stderr))
            processes.append(_spawn_windows_suspended_in_job(command, Path(cwd), stdout, stderr, job))
        while True:
            verify_identity(pins)
            measured_cpu, memory, active = _native_sample(job)
            sample = Sample(time.monotonic()-started, measured_cpu+time.process_time()-controller_start,
                            memory, _disk_bytes(output), active)
            if any(not math.isfinite(value) or value < 0 for value in asdict(sample).values()):
                raise StopExecution('invalid authoritative accounting')
            last_job_cpu=measured_cpu
            samples.append(asdict(sample))
            sampling['observations']+=1
            sampling['first']=sampling['first'] or asdict(sample)
            sampling['memory_bytes_max']=max(sampling['memory_bytes_max'],memory)
            sampling['active_processes_max']=max(sampling['active_processes_max'],active)
            guard.observe(sample)
            if active == 0 and all(p.poll() is not None for p in processes):
                codes = [p.wait(timeout=1) for p in processes]
                if any(codes):
                    raise StopExecution(f'worker exit codes: {codes}')
                receipt.update(status='completed', reason='all owned processes completed', exit_codes=codes)
                break
            time.sleep(limits.poll_seconds)
    except (Exception, KeyboardInterrupt) as exc:
        receipt.update(status='stopped', reason=f'{type(exc).__name__}: {exc}')
    finally:
        if job is not None:
            try:
                job.terminate()
                deadline = time.monotonic()+5
                while job.active_processes() and time.monotonic() < deadline:
                    time.sleep(.01)
                final_cpu, _, active = _native_sample(job)
                if not math.isfinite(final_cpu) or final_cpu < last_job_cpu or active:
                    raise StopExecution('terminal accounting or tree shutdown failed')
                receipt.update(job_cpu_seconds=final_cpu, active_processes=active, accounting_complete=True)
            except Exception as exc:
                receipt.update(status='stopped', reason=f'terminal accounting unavailable: {exc}', accounting_complete=False)
            finally:
                job.close()  # Kernel kills owned descendants on controller loss too.
        for process in processes:
            try:
                process.wait(timeout=5)
            except Exception:
                receipt.update(status='stopped', accounting_complete=False, reason='worker wait failed')
            finally:
                if process._handle:
                    if not process._kernel.CloseHandle(process._handle):
                        receipt.update(status='stopped', reason='worker handle close failed')
                    process._handle = None
        for handle in handles:
            handle.close()
        controller_cpu = time.process_time()-controller_start
        receipt.update(controller_cpu_seconds=controller_cpu,
                       cpu_seconds=receipt.get('job_cpu_seconds', last_job_cpu)+controller_cpu,
                       elapsed=time.monotonic()-started,samples=list(samples),sampling=sampling)
        if not receipt['accounting_complete']:
            receipt['status'] = 'stopped'
        if ledger is not None:
            try:
                receipt['budget'] = ledger.finish(receipt['cpu_seconds'], accounting_complete=receipt['accounting_complete'])
            except Exception as exc:
                receipt.update(status='stopped', reason=f'budget journal not sealed: {exc}')
        data=json.dumps(receipt,separators=(',',':'),allow_nan=False).encode('utf-8')
        if len(data)>2*1024**2:
            raise StopExecution('bounded receipt size exceeded; no success publication')
        with (output/'receipt.json').open('xb') as handle:
            handle.write(data)
            handle.flush(); os.fsync(handle.fileno())
    return receipt
