"""Run only installed qualification entrypoints under isolated Python."""
import os
from pathlib import Path
import stat
import sys

HERE = Path(__file__).parent
ROOT = HERE / 'code' if (HERE / 'code').is_dir() else HERE
if not sys.flags.isolated or sys.platform != 'linux':
    raise SystemExit('isolated Linux interpreter required')
for path in (Path(__file__), ROOT, *ROOT.parents):
    info = path.lstat()
    if stat.S_ISLNK(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o022:
        raise SystemExit('unprotected installed bootstrap/code')
if len(sys.argv) < 2 or sys.argv[1] not in ('worker', 'supervisor', 'g5', 'campaign_guardian', 'campaign_probe', 'campaign_control'):
    raise SystemExit('fixed process role required')
role = sys.argv.pop(1)
sys.dont_write_bytecode = True
if role in ('worker', 'campaign_probe', 'g5'):
    # The payload's resume safety net, before sys.path and before any import
    # that can spawn threads (the worker imports the compute stack and numpy,
    # whose OpenBLAS builds its pool at import). Install the no-op SIGUSR1
    # handler FIRST -- a resume in the handler-only window is harmlessly
    # ignored -- then block SIGUSR1 in the leader: every thread created later
    # inherits the blocked mask, so a guardian resume can only ever sit
    # pending for the main thread's sigtimedwait. Without this, glibc's
    # pthread_create briefly leaves a sibling unblocked while the leader holds
    # the block, and the kernel's fatal-default group exit bypasses the
    # container-init drop (complete_signal since 4.15: exit 138, run
    # 35543486564). Standard library only; S3's worker imports numpy first
    # and is covered by this same block.
    import signal
    signal.signal(signal.SIGUSR1, lambda *_: None)
    signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGUSR1})
    # 'g5' joins the payload roles for the campaign mode only: the S3 qg5 unit
    # calls the same readiness handshake as the worker (D2); an N1_ONLY g5
    # never waits on it, and the inherited block is inert there.
if role == 'campaign_guardian':
    # The original absolute BOOTTIME deadline is enforced by a kernel SIGKILL
    # timer from here, before any campaign import or construction; the guardian
    # later re-derives the same instant from its durable reservation and refuses
    # a differing argv. An already-past absolute timer fires at once, so queued
    # or late starts and expired work need no further path. Standard library and
    # ctypes only; the layout is the supported x86_64 ABI.
    import ctypes
    import platform
    import signal
    import time
    if platform.machine() != 'x86_64':
        raise SystemExit('supported Linux x86_64 timer ABI required')
    try:
        deadline = sys.argv[sys.argv.index('--deadline-boottime-ns') + 1]
    except (ValueError, IndexError):
        raise SystemExit('fixed guardian deadline argument required') from None
    if not deadline.isascii() or not deadline.isdigit() or int(deadline) <= 0:
        raise SystemExit('fixed guardian deadline argument required')
    deadline = int(deadline)

    class Event(ctypes.Structure):
        _fields_ = [('value', ctypes.c_void_p), ('signo', ctypes.c_int),
                    ('notify', ctypes.c_int), ('padding', ctypes.c_byte * 48)]

    class Timespec(ctypes.Structure):
        _fields_ = [('seconds', ctypes.c_long), ('nanoseconds', ctypes.c_long)]

    class TimerSpec(ctypes.Structure):
        _fields_ = [('interval', Timespec), ('value', Timespec)]
    libc = ctypes.CDLL('libc.so.6', use_errno=True)
    timer = ctypes.c_void_p()
    event = Event(None, signal.SIGKILL, 0)
    specification = TimerSpec(Timespec(0, 0), Timespec(*divmod(deadline, 10**9)))
    if libc.timer_create(time.CLOCK_BOOTTIME, ctypes.byref(event), ctypes.byref(timer)):
        raise SystemExit('guardian deadline timer_create failed: ' + str(ctypes.get_errno()))
    if libc.timer_settime(timer, 1, ctypes.byref(specification), None):
        raise SystemExit('guardian absolute deadline failed: ' + str(ctypes.get_errno()))
    if time.clock_gettime_ns(time.CLOCK_BOOTTIME) >= deadline:
        # Armed anyway: the kernel delivers an elapsed absolute timer immediately.
        raise SystemExit('original deadline passed before guardian bootstrap')
sys.path[:0] = [str(ROOT / part) for part in ('ops', 'core', 'lab', 'governance', '')]
if role == 'campaign_control':
    # This private child has no independent authority. Close the parent-death
    # race before exec, preserving SIGKILL through the unprivileged exec.
    import ctypes
    import resource
    from tools.qualification_verification.container_ownership import CAMPAIGN_BUS_START
    parent = int(sys.argv.pop(1))
    libc = ctypes.CDLL('libc.so.6', use_errno=True)
    if libc.prctl(1, 9, 0, 0, 0) or os.getppid() != parent:
        raise SystemExit('control parent lost')
    if resource.getrlimit(resource.RLIMIT_CPU) != (1, 1):
        raise SystemExit('control hard CPU limit differs')
    command = sys.argv[1:]
    if tuple(command[:len(CAMPAIGN_BUS_START)]) != CAMPAIGN_BUS_START:
        raise SystemExit('fixed private lifecycle command required')
    os.execv(command[0], command)

import importlib
module = {'supervisor': 'service', 'campaign_guardian': 'service', 'campaign_probe': 'worker'}.get(role, role)
entry = importlib.import_module('c1_rail.qualification.execution.' + module)
getattr(entry, role + '_main' if role.startswith('campaign_') else 'main')()
