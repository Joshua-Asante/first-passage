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
if len(sys.argv) < 2 or sys.argv[1] not in ('worker', 'supervisor', 'g5'):
    raise SystemExit('fixed process role required')
role = sys.argv.pop(1)
sys.dont_write_bytecode = True
sys.path[:0] = [str(ROOT / part) for part in ('ops', 'core', 'lab', 'governance', '')]
import importlib
module = 'service' if role == 'supervisor' else role
importlib.import_module('c1_rail.qualification.execution.' + module).main()
