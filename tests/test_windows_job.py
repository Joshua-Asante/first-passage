"""Portable unit tests for lab/discovery/windows_job.py.

Carried over from the retired tests/test_agent_handoff.py with the helpers they
cover. Native Job behaviour (accounting, descendants, termination) is exercised
on Windows by tests/test_orb_solo_executor.py and tests/test_orb_solo_release.py.
"""
import inspect
import sys

from discovery import windows_job as WJ


def test_process_ids_retries_when_buffer_reports_more_data():
    """ERROR_MORE_DATA must enlarge the PID-list buffer and retry."""
    import ctypes
    from ctypes import wintypes

    # Linux CPython may lack ctypes.set_last_error; stub get_last_error on the
    # object process_ids actually calls so the retry path stays portable.
    class CT:
        Structure = ctypes.Structure
        c_size_t = ctypes.c_size_t
        byref = staticmethod(ctypes.byref)
        sizeof = staticmethod(ctypes.sizeof)
        _last = 0

        @classmethod
        def get_last_error(cls):
            return cls._last

    job = WJ.WindowsJob(handle=1)
    job._ctypes = CT
    job._wintypes = wintypes
    capacities = []

    def fake_query(handle, info_class, buf, buflen, retlen):
        header = ctypes.sizeof(wintypes.DWORD) * 2
        capacity = (buflen - header) // ctypes.sizeof(ctypes.c_size_t)
        capacities.append(capacity)

        class Hdr(ctypes.Structure):
            _fields_ = [
                ('NumberOfAssignedProcesses', wintypes.DWORD),
                ('NumberOfProcessIdsInList', wintypes.DWORD),
                ('ProcessIdList', ctypes.c_size_t * max(capacity, 1)),
            ]

        info = ctypes.cast(buf, ctypes.POINTER(Hdr)).contents
        if capacity < 100:
            info.NumberOfAssignedProcesses = 100
            info.NumberOfProcessIdsInList = 0
            CT._last = WJ.WindowsJob.ERROR_MORE_DATA
            return 0
        info.NumberOfAssignedProcesses = 2
        info.NumberOfProcessIdsInList = 2
        info.ProcessIdList[0] = 11
        info.ProcessIdList[1] = 22
        CT._last = 0
        return 1

    class Kernel:
        QueryInformationJobObject = staticmethod(fake_query)

    job._kernel = Kernel()
    assert job.process_ids() == [11, 22]
    assert capacities[0] == WJ.WindowsJob._PID_LIST_INITIAL_CAPACITY
    assert capacities[1] >= 100


def test_assign_requires_a_process_handle():
    job = WJ.WindowsJob(handle=1)
    calls = []

    class Kernel:
        @staticmethod
        def AssignProcessToJobObject(job_handle, process_handle):
            calls.append((job_handle, process_handle))
            return 1

    job._kernel = Kernel()
    try:
        job.assign(object())
    except OSError as exc:
        assert 'handle unavailable' in str(exc)
    else:
        raise AssertionError('assign without a process handle must fail closed')
    assert calls == []
    job.assign(type('P', (), {'_handle': 42})())
    assert calls == [(1, 42)]


def test_windows_os_handle_uses_msvcrt(monkeypatch):
    calls = []

    class FakeMsvcrt:
        @staticmethod
        def get_osfhandle(fd):
            calls.append(fd)
            return 0xABCD

    class FileObj:
        def fileno(self):
            return 7

    monkeypatch.setitem(sys.modules, 'msvcrt', FakeMsvcrt)
    assert WJ.windows_os_handle(FileObj()) == 0xABCD
    assert calls == [7]


def test_windows_spawn_stdio_converts_fd_and_inherits_nul():
    """Native CreateProcess path must use Win32 HANDLEs and an inheritable NUL."""
    source = inspect.getsource(WJ._spawn_windows_suspended_in_job)
    assert 'windows_os_handle' in source
    assert 'SECURITY_ATTRIBUTES' in source
    assert 'bInheritHandle = True' in source
    assert 'SetHandleInformation' in source
    # Must not pass CRT fileno() directly to DuplicateHandle.
    assert 'HANDLE(fileobj.fileno())' not in source
    assert 'msvcrt.get_osfhandle' in source or 'windows_os_handle(fileobj)' in source


def test_spawn_creates_suspended_and_assigns_before_resume():
    """The child is created suspended, joined to the Job, then resumed."""
    source = inspect.getsource(WJ._spawn_windows_suspended_in_job)
    assert 'CREATE_SUSPENDED' in source
    assign = source.index('job.assign(carrier)')
    resume = source.index('kernel.ResumeThread(info.hThread)')
    create = source.index('kernel.CreateProcessW(\n')
    assert create < assign < resume


def test_job_kills_owned_tree_on_close():
    """KILL_ON_JOB_CLOSE is set so a lost controller cannot orphan workers."""
    source = inspect.getsource(WJ.WindowsJob.create)
    assert 'LimitFlags = cls.JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE' in source
    assert WJ.WindowsJob.JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE == 0x2000
