"""Worker-owned cumulative CPU/wall/peak-memory observations."""
import os
from time import perf_counter_ns, process_time_ns

from ..runner import NeedsContext


def peak_memory_bytes():
    if os.name == 'nt':
        import ctypes
        from ctypes import wintypes
        class Counters(ctypes.Structure):
            _fields_ = [('cb', wintypes.DWORD), ('PageFaultCount', wintypes.DWORD)] + [
                (name, ctypes.c_size_t) for name in ('PeakWorkingSetSize', 'WorkingSetSize',
                'QuotaPeakPagedPoolUsage', 'QuotaPagedPoolUsage', 'QuotaPeakNonPagedPoolUsage',
                'QuotaNonPagedPoolUsage', 'PagefileUsage', 'PeakPagefileUsage')]
        counters = Counters()
        counters.cb = ctypes.sizeof(counters)
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.GetCurrentProcess.restype = wintypes.HANDLE
        psapi = ctypes.WinDLL('psapi', use_last_error=True)
        psapi.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(Counters), wintypes.DWORD]
        if not psapi.GetProcessMemoryInfo(kernel.GetCurrentProcess(), ctypes.byref(counters), counters.cb):
            raise NeedsContext('process memory observation unavailable')
        return counters.PeakWorkingSetSize
    try:
        import resource
        import sys
        return int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) * (1 if sys.platform == 'darwin' else 1024)
    except (ImportError, AttributeError) as exc:
        raise NeedsContext('process memory observation unavailable') from exc


class BudgetGuard:
    def __init__(self, budget_spec):
        self._spec = budget_spec
        self._wall_start = perf_counter_ns()
        self._cpu_start = process_time_ns()

    @classmethod
    def from_contract(cls, contract):
        return cls(contract.replay.budget)

    def remaining_wall_seconds(self):
        return self.check_and_measure()['remaining_wall_seconds']

    def check_and_measure(self):
        wall = perf_counter_ns() - self._wall_start
        cpu = process_time_ns() - self._cpu_start
        memory = peak_memory_bytes()
        remaining_ns = self._spec.maximum_wall_seconds * 1_000_000_000 - wall
        if min(wall, cpu, memory) < 0 or remaining_ns <= 0 or cpu > self._spec.maximum_cpu_seconds * 1_000_000_000:
            raise NeedsContext('frozen execution CPU/wall budget exhausted; no replacement draws')
        if memory > self._spec.maximum_memory_bytes:
            raise NeedsContext('frozen execution memory budget exceeded; no replacement draws')
        return dict(remaining_wall_seconds=remaining_ns / 1_000_000_000,
                    worker_compute_wall_ns=wall, worker_cpu_ns=cpu, worker_peak_memory_bytes=memory)
