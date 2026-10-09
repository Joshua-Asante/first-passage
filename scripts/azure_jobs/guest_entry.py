"""Guest entry points under isolated CPython."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
if __name__ == '__main__':
    mode = sys.argv.pop(1)
    if mode == 'watchdog':
        from scripts.azure_jobs.watchdog import main
        main(sys.argv[1])
    elif mode == 'snapshot':
        from scripts.record_verification import snapshot
        from scripts.azure_jobs.control import atomic
        atomic(Path(sys.argv[2]), snapshot(Path(sys.argv[1])))
    elif mode in {'execute', 'republish'}:
        from scripts.azure_jobs.guest import main
        main(mode)
    else:
        raise ValueError('invalid guest mode')
