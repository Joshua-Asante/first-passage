"""Guest entry points under isolated CPython."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
if __name__ == '__main__':
    mode = sys.argv.pop(1)
    if mode == 'watchdog':
        from scripts.azure_jobs.watchdog import main
        main(sys.argv[1])
    elif mode == 'recover':
        import json
        from scripts.azure_jobs.watchdog import read, recover
        lease = json.loads(sys.argv[2])
        config = {**read(sys.argv[1]), 'deadline': lease['deadline']}
        sys.exit(0 if recover(config, lease, sys.argv[3]) else 75)
    elif mode == 'snapshot':
        from scripts.record_verification import snapshot
        from scripts.azure_jobs.control import atomic
        atomic(Path(sys.argv[2]), snapshot(Path(sys.argv[1])))
    elif mode == 'execute':
        from scripts.azure_jobs.guest import main
        main(mode)
    else:
        raise ValueError('invalid guest mode')
