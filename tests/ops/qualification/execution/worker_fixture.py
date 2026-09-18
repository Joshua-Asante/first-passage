"""Fresh-process library worker fixture; not protected-execution evidence."""
from datetime import datetime
from pathlib import Path
import subprocess
import sys
import tomllib


def run_fixture_worker(input_dir, *, execution_id, now):
    """Keep actual worker observations independent of the pytest process history."""
    result = subprocess.run(
        [sys.executable, '-I', str(Path(__file__).resolve()),
         str(input_dir), execution_id, now.isoformat()],
        capture_output=True, timeout=120, check=False,
    )
    if result.returncode:
        raise RuntimeError('fixture worker failed: ' + result.stderr.decode('utf-8', errors='replace'))
    return result.stdout


def compute():
    """Run real computation with only the fixture's historical admission clock."""
    repository = Path(__file__).resolve().parents[4]
    config = tomllib.loads((repository / 'pyproject.toml').read_text(encoding='utf-8'))
    sys.path[:0] = [str(repository / path) for path in config['tool']['pytest']['ini_options']['pythonpath']]
    from c1_rail.qualification.execution import worker
    instant = datetime.fromisoformat(sys.argv[3])
    worker.utc_now = lambda: instant
    frame = worker.run_worker(Path(sys.argv[1]), execution_id=sys.argv[2])
    sys.stdout.buffer.write(frame)
    sys.stdout.buffer.flush()


def main():
    if sys.argv[1] == '--compute':
        del sys.argv[1]
        compute()
        return 0
    # Linux vfork/exec can retain the original pytest address space's peak RSS.
    # This interpreter has a fresh, small address space. A second process gets
    # new resource accounting based on that space before project imports occur.
    # Keep the inner timeout below the caller's so it kills/reaps its own worker.
    result = subprocess.run(
        [sys.executable, '-I', str(Path(__file__).resolve()), '--compute', *sys.argv[1:]],
        timeout=110, check=False,
    )
    return result.returncode


if __name__ == '__main__':
    raise SystemExit(main())
