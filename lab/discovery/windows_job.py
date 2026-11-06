"""Windows Job Object helpers for the ORB solo executor boundary.

Moved verbatim from the retired ``scripts/agent_handoff.py`` (governance cut 4,
2026-11). Only the pieces ``orb_solo_executor`` and ``orb_solo_release`` use:
a Job handle that owns a process tree, and a suspended CreateProcess launch that
assigns the child to the Job before its first instruction runs. Windows only;
nothing here runs at import time.
"""
from __future__ import annotations

import subprocess


class WindowsJob:
    """Retain a Windows Job Object handle for the owned provider tree."""

    JobObjectBasicAccountingInformation = 1
    JobObjectBasicProcessIdList = 3
    JobObjectExtendedLimitInformation = 9
    JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x2000
    PROCESS_TERMINATE = 0x0001
    PROCESS_SET_QUOTA = 0x0100
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    STILL_ACTIVE = 259
    ERROR_INVALID_PARAMETER = 87
    ERROR_ACCESS_DENIED = 5
    ERROR_MORE_DATA = 234
    # Cap for one QueryInformationJobObject PID-list read; jobs with more
    # processes retry with a larger buffer via NumberOfAssignedProcesses /
    # ERROR_MORE_DATA rather than failing closed on the first undersized read.
    _PID_LIST_INITIAL_CAPACITY = 64

    def __init__(self, handle):
        self.handle = handle
        self._kernel = None
        self._ctypes = None
        self._wintypes = None
        self._accounting = None

    @classmethod
    def _api(cls):
        import ctypes
        from ctypes import wintypes
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.CreateJobObjectW.argtypes = [wintypes.LPVOID, wintypes.LPCWSTR]
        kernel.CreateJobObjectW.restype = wintypes.HANDLE
        kernel.SetInformationJobObject.argtypes = [wintypes.HANDLE, wintypes.INT, wintypes.LPVOID, wintypes.DWORD]
        kernel.SetInformationJobObject.restype = wintypes.BOOL
        kernel.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
        kernel.AssignProcessToJobObject.restype = wintypes.BOOL
        kernel.QueryInformationJobObject.argtypes = [wintypes.HANDLE, wintypes.INT, wintypes.LPVOID, wintypes.DWORD, wintypes.LPDWORD]
        kernel.QueryInformationJobObject.restype = wintypes.BOOL
        kernel.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
        kernel.TerminateJobObject.restype = wintypes.BOOL
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        kernel.CloseHandle.restype = wintypes.BOOL
        kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        kernel.OpenProcess.restype = wintypes.HANDLE
        kernel.GetExitCodeProcess.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
        kernel.GetExitCodeProcess.restype = wintypes.BOOL
        return ctypes, wintypes, kernel

    @classmethod
    def create(cls):
        ctypes, wintypes, kernel = cls._api()

        class IO_COUNTERS(ctypes.Structure):
            _fields_ = [
                ('ReadOperationCount', ctypes.c_ulonglong),
                ('WriteOperationCount', ctypes.c_ulonglong),
                ('OtherOperationCount', ctypes.c_ulonglong),
                ('ReadTransferCount', ctypes.c_ulonglong),
                ('WriteTransferCount', ctypes.c_ulonglong),
                ('OtherTransferCount', ctypes.c_ulonglong),
            ]

        class JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
            _fields_ = [
                ('PerProcessUserTimeLimit', ctypes.c_int64),
                ('PerJobUserTimeLimit', ctypes.c_int64),
                ('LimitFlags', wintypes.DWORD),
                ('MinimumWorkingSetSize', ctypes.c_size_t),
                ('MaximumWorkingSetSize', ctypes.c_size_t),
                ('ActiveProcessLimit', wintypes.DWORD),
                ('Affinity', ctypes.c_size_t),
                ('PriorityClass', wintypes.DWORD),
                ('SchedulingClass', wintypes.DWORD),
            ]

        class JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
            _fields_ = [
                ('BasicLimitInformation', JOBOBJECT_BASIC_LIMIT_INFORMATION),
                ('IoInfo', IO_COUNTERS),
                ('ProcessMemoryLimit', ctypes.c_size_t),
                ('JobMemoryLimit', ctypes.c_size_t),
                ('PeakProcessMemoryUsed', ctypes.c_size_t),
                ('PeakJobMemoryUsed', ctypes.c_size_t),
            ]

        handle = kernel.CreateJobObjectW(None, None)
        if not handle:
            raise OSError('CreateJobObject failed')
        info = JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
        info.BasicLimitInformation.LimitFlags = cls.JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if not kernel.SetInformationJobObject(handle, cls.JobObjectExtendedLimitInformation, ctypes.byref(info), ctypes.sizeof(info)):
            kernel.CloseHandle(handle)
            raise OSError('SetInformationJobObject failed')
        job = cls(handle)
        job._kernel = kernel
        job._ctypes = ctypes
        job._wintypes = wintypes
        job._accounting = type('JOBOBJECT_BASIC_ACCOUNTING_INFORMATION', (ctypes.Structure,), {
            '_fields_': [
                ('TotalUserTime', ctypes.c_int64),
                ('TotalKernelTime', ctypes.c_int64),
                ('ThisPeriodTotalUserTime', ctypes.c_int64),
                ('ThisPeriodTotalKernelTime', ctypes.c_int64),
                ('TotalPageFaultCount', wintypes.DWORD),
                ('TotalProcesses', wintypes.DWORD),
                ('ActiveProcesses', wintypes.DWORD),
                ('TotalTerminatedProcesses', wintypes.DWORD),
            ]
        })
        return job

    def assign(self, process):
        handle = getattr(process, '_handle', None)
        if not handle:
            raise OSError('Windows process handle unavailable for job assignment')
        if not self._kernel.AssignProcessToJobObject(self.handle, int(handle)):
            raise OSError('AssignProcessToJobObject failed')

    def active_processes(self):
        info = self._accounting()
        returned = self._wintypes.DWORD()
        if not self._kernel.QueryInformationJobObject(
            self.handle, self.JobObjectBasicAccountingInformation, self._ctypes.byref(info),
            self._ctypes.sizeof(info), self._ctypes.byref(returned)
        ):
            raise OSError('QueryInformationJobObject failed')
        return int(info.ActiveProcesses)

    def process_ids(self):
        """Return PIDs currently associated with the job (may include an exiting leader)."""
        capacity = self._PID_LIST_INITIAL_CAPACITY
        while True:
            list_type = type(
                'JOBOBJECT_BASIC_PROCESS_ID_LIST',
                (self._ctypes.Structure,),
                {
                    '_fields_': [
                        ('NumberOfAssignedProcesses', self._wintypes.DWORD),
                        ('NumberOfProcessIdsInList', self._wintypes.DWORD),
                        ('ProcessIdList', self._ctypes.c_size_t * capacity),
                    ]
                },
            )
            info = list_type()
            returned = self._wintypes.DWORD()
            ok = self._kernel.QueryInformationJobObject(
                self.handle, self.JobObjectBasicProcessIdList, self._ctypes.byref(info),
                self._ctypes.sizeof(info), self._ctypes.byref(returned),
            )
            assigned = int(info.NumberOfAssignedProcesses)
            if not ok:
                err = self._ctypes.get_last_error()
                # Undersized buffer: NumberOfAssignedProcesses still names the
                # required size. Enlarge and retry instead of failing closed.
                if err == self.ERROR_MORE_DATA and assigned > capacity:
                    capacity = assigned
                    continue
                raise OSError(f'QueryInformationJobObject(ProcessIdList) failed: {err}')
            listed = int(info.NumberOfProcessIdsInList)
            if listed < assigned and capacity < assigned:
                capacity = assigned
                continue
            return [int(info.ProcessIdList[i]) for i in range(listed)]

    def _pid_still_active(self, pid):
        handle = self._kernel.OpenProcess(self.PROCESS_QUERY_LIMITED_INFORMATION, False, int(pid))
        if not handle:
            error = self._ctypes.get_last_error()
            # Process already gone — not a live descendant.
            if error in (self.ERROR_INVALID_PARAMETER, 0):
                return False
            # Access denied / other query failures must fail closed.
            raise OSError(f'OpenProcess({pid}) failed: {error}')
        try:
            code = self._wintypes.DWORD()
            if not self._kernel.GetExitCodeProcess(handle, self._ctypes.byref(code)):
                raise OSError(f'GetExitCodeProcess({pid}) failed')
            return int(code.value) == self.STILL_ACTIVE
        finally:
            self._kernel.CloseHandle(handle)

    def live_descendant_pids(self, exclude_pid=None):
        """Live PIDs in the job, optionally excluding an already-exited leader."""
        live = []
        for pid in self.process_ids():
            if exclude_pid is not None and int(pid) == int(exclude_pid):
                continue
            if self._pid_still_active(pid):
                live.append(int(pid))
        return live

    def terminate(self):
        self._kernel.TerminateJobObject(self.handle, 1)

    def close(self):
        if self.handle:
            self._kernel.CloseHandle(self.handle)
            self.handle = None


class WindowsOwnedProcess:
    """Minimal process adapter for CreateProcess + Job Object launches."""

    STILL_ACTIVE = 259

    def __init__(self, pid, process_handle, kernel, ctypes, wintypes):
        self.pid = int(pid)
        self._handle = int(process_handle)
        self._kernel = kernel
        self._ctypes = ctypes
        self._wintypes = wintypes
        self.returncode = None
        self.stdin = None
        self.stdout = None
        self.stderr = None

    def poll(self):
        if self.returncode is not None:
            return self.returncode
        code = self._wintypes.DWORD()
        if not self._kernel.GetExitCodeProcess(self._handle, self._ctypes.byref(code)):
            return None
        if code.value == self.STILL_ACTIVE:
            return None
        self.returncode = int(code.value)
        return self.returncode

    def wait(self, timeout=None):
        milliseconds = self._wintypes.DWORD(0xFFFFFFFF if timeout is None else max(0, int(timeout * 1000)))
        result = self._kernel.WaitForSingleObject(self._handle, milliseconds)
        if result == 0:  # WAIT_OBJECT_0
            return self.poll()
        if result == 0x00000102:  # WAIT_TIMEOUT
            raise subprocess.TimeoutExpired(cmd=None, timeout=timeout)
        raise OSError(f'WaitForSingleObject failed: {result}')

    def kill(self):
        self._kernel.TerminateProcess(self._handle, 1)


def windows_os_handle(fileobj):
    """Map a Python file object to a Win32 HANDLE (not a CRT fd index)."""
    import msvcrt
    return int(msvcrt.get_osfhandle(fileobj.fileno()))


def _spawn_windows_suspended_in_job(command, cwd, stdout, stderr, job):
    import ctypes
    from ctypes import wintypes

    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    CREATE_SUSPENDED = 0x00000004
    CREATE_NO_WINDOW = 0x08000000
    CREATE_UNICODE_ENVIRONMENT = 0x00000400
    STARTF_USESTDHANDLES = 0x00000100
    HANDLE_FLAG_INHERIT = 0x00000001
    DUPLICATE_SAME_ACCESS = 0x00000002
    WAIT_OBJECT_0 = 0
    WAIT_TIMEOUT = 0x00000102

    class STARTUPINFOW(ctypes.Structure):
        _fields_ = [
            ('cb', wintypes.DWORD),
            ('lpReserved', wintypes.LPWSTR),
            ('lpDesktop', wintypes.LPWSTR),
            ('lpTitle', wintypes.LPWSTR),
            ('dwX', wintypes.DWORD),
            ('dwY', wintypes.DWORD),
            ('dwXSize', wintypes.DWORD),
            ('dwYSize', wintypes.DWORD),
            ('dwXCountChars', wintypes.DWORD),
            ('dwYCountChars', wintypes.DWORD),
            ('dwFillAttribute', wintypes.DWORD),
            ('dwFlags', wintypes.DWORD),
            ('wShowWindow', wintypes.WORD),
            ('cbReserved2', wintypes.WORD),
            ('lpReserved2', ctypes.POINTER(wintypes.BYTE)),
            ('hStdInput', wintypes.HANDLE),
            ('hStdOutput', wintypes.HANDLE),
            ('hStdError', wintypes.HANDLE),
        ]

    class PROCESS_INFORMATION(ctypes.Structure):
        _fields_ = [
            ('hProcess', wintypes.HANDLE),
            ('hThread', wintypes.HANDLE),
            ('dwProcessId', wintypes.DWORD),
            ('dwThreadId', wintypes.DWORD),
        ]

    kernel.CreateProcessW.argtypes = [
        wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.LPVOID, wintypes.LPVOID,
        wintypes.BOOL, wintypes.DWORD, wintypes.LPVOID, wintypes.LPCWSTR,
        ctypes.POINTER(STARTUPINFOW), ctypes.POINTER(PROCESS_INFORMATION),
    ]
    kernel.CreateProcessW.restype = wintypes.BOOL
    kernel.ResumeThread.argtypes = [wintypes.HANDLE]
    kernel.ResumeThread.restype = wintypes.DWORD
    kernel.TerminateProcess.argtypes = [wintypes.HANDLE, wintypes.UINT]
    kernel.TerminateProcess.restype = wintypes.BOOL
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel.CloseHandle.restype = wintypes.BOOL
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.DuplicateHandle.argtypes = [
        wintypes.HANDLE, wintypes.HANDLE, wintypes.HANDLE,
        ctypes.POINTER(wintypes.HANDLE), wintypes.DWORD, wintypes.BOOL, wintypes.DWORD,
    ]
    kernel.DuplicateHandle.restype = wintypes.BOOL
    kernel.SetHandleInformation.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.DWORD]
    kernel.SetHandleInformation.restype = wintypes.BOOL
    kernel.GetExitCodeProcess.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
    kernel.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    kernel.CreateFileW.argtypes = [
        wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID,
        wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE,
    ]
    kernel.CreateFileW.restype = wintypes.HANDLE

    class SECURITY_ATTRIBUTES(ctypes.Structure):
        _fields_ = [
            ('nLength', wintypes.DWORD),
            ('lpSecurityDescriptor', wintypes.LPVOID),
            ('bInheritHandle', wintypes.BOOL),
        ]

    def duplicate_inheritable(fileobj):
        # Python fileobj.fileno() is a CRT fd index on Windows, not a Win32 HANDLE.
        current = kernel.GetCurrentProcess()
        source = wintypes.HANDLE(windows_os_handle(fileobj))
        target = wintypes.HANDLE()
        if not kernel.DuplicateHandle(current, source, current, ctypes.byref(target), 0, True, DUPLICATE_SAME_ACCESS):
            raise OSError('DuplicateHandle failed for stdio')
        if not kernel.SetHandleInformation(target, HANDLE_FLAG_INHERIT, HANDLE_FLAG_INHERIT):
            kernel.CloseHandle(target)
            raise OSError('SetHandleInformation failed for duplicated stdio')
        return target

    # Inheritable NUL for stdin so CreateProcess can pass it to the child.
    # CreateFileW with lpSecurityAttributes=None yields a non-inheritable handle.
    GENERIC_READ = 0x80000000
    FILE_SHARE_READ = 0x00000001
    OPEN_EXISTING = 3
    security = SECURITY_ATTRIBUTES()
    security.nLength = ctypes.sizeof(SECURITY_ATTRIBUTES)
    security.lpSecurityDescriptor = None
    security.bInheritHandle = True
    nul = kernel.CreateFileW(
        'NUL', GENERIC_READ, FILE_SHARE_READ, ctypes.byref(security), OPEN_EXISTING, 0, None,
    )
    if not nul or nul == wintypes.HANDLE(-1).value:
        raise OSError('Failed to open NUL for provider stdin')
    if not kernel.SetHandleInformation(nul, HANDLE_FLAG_INHERIT, HANDLE_FLAG_INHERIT):
        kernel.CloseHandle(nul)
        raise OSError('SetHandleInformation failed for NUL stdin')

    startup = STARTUPINFOW()
    startup.cb = ctypes.sizeof(STARTUPINFOW)
    startup.dwFlags = STARTF_USESTDHANDLES
    startup.hStdInput = nul
    startup.hStdOutput = duplicate_inheritable(stdout)
    startup.hStdError = duplicate_inheritable(stderr)
    info = PROCESS_INFORMATION()
    command_line = ctypes.create_unicode_buffer(subprocess.list2cmdline(list(map(str, command))))
    created = kernel.CreateProcessW(
        None, command_line, None, None, True,
        CREATE_SUSPENDED | CREATE_NO_WINDOW | CREATE_UNICODE_ENVIRONMENT,
        None, str(cwd), ctypes.byref(startup), ctypes.byref(info),
    )
    # Ownership cleanup must cover the entire post-CreateProcess interval —
    # including stdio CloseHandle — so KeyboardInterrupt/SystemExit cannot
    # leave a suspended orphan before job assignment.
    try:
        if not created:
            for handle in (startup.hStdOutput, startup.hStdError, nul):
                try:
                    kernel.CloseHandle(handle)
                except OSError:
                    pass
            raise OSError(f'CreateProcessW failed: {ctypes.get_last_error()}')
        for handle in (startup.hStdOutput, startup.hStdError, nul):
            try:
                kernel.CloseHandle(handle)
            except OSError:
                pass
        carrier = type('HandleCarrier', (), {'_handle': int(info.hProcess)})()
        job.assign(carrier)
        resumed = kernel.ResumeThread(info.hThread)
        if resumed == 0xFFFFFFFF:
            raise OSError('ResumeThread failed')
    except BaseException:
        if created:
            try:
                kernel.TerminateProcess(info.hProcess, 1)
            except OSError:
                pass
            try:
                kernel.CloseHandle(info.hThread)
            except OSError:
                pass
            try:
                kernel.CloseHandle(info.hProcess)
            except OSError:
                pass
        raise
    kernel.CloseHandle(info.hThread)
    process = WindowsOwnedProcess(info.dwProcessId, info.hProcess, kernel, ctypes, wintypes)
    return process
