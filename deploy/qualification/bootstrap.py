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
