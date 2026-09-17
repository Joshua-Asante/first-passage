"""Run First Passage commands in the checkout's locked operations environment."""
from __future__ import annotations

import argparse
from contextlib import nullcontext
import importlib.util
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from uuid import uuid4


# Executed by the selected interpreter, not by the bootstrap Python on PATH.
PROBE = """
import importlib.metadata as md, json, sys
from pathlib import Path
expected = json.loads(sys.argv[1])
errors = []
if sys.prefix == sys.base_prefix or not Path(sys.prefix).samefile(sys.argv[2]):
    errors.append('selected Python is not the requested isolated virtual environment')
if sys.version_info < (3, 11):
    errors.append('Python 3.11 or newer is required')
for name, version in expected.items():
    try:
        actual = md.version(name)
    except md.PackageNotFoundError:
        errors.append(name + ' is missing (expected ' + version + ')')
        continue
    if actual != version:
        errors.append(name + ': expected ' + version + ', installed ' + actual)
try:
    signing = md.version('cryptography')
except md.PackageNotFoundError:
    signing = 'absent; signed settlement tests may skip'
print(json.dumps({'python': sys.executable, 'version': sys.version.split()[0],
                  'errors': errors, 'signing': signing}))
"""


def resolve_environment(root: Path, explicit: str | None) -> Path:
    """Prefer an explicit or checkout-local venv; share the main venv in worktrees."""
    if explicit is not None:
        if not explicit.strip():
            raise ValueError("Operations environment selection is empty; supply a venv directory")
        return Path(explicit).expanduser().resolve()
    local = root / "tmp/ops-env"
    if local.exists():
        return local
    marker = root / ".git"
    if marker.is_file():
        directive = marker.read_text(encoding="utf-8").strip()
        if directive.startswith("gitdir: "):
            metadata = (root / directive[8:]).resolve()
            common_file = metadata / "commondir"
            if common_file.is_file():
                common = (metadata / common_file.read_text(encoding="utf-8").strip()).resolve()
                return common.parent / "tmp/ops-env"
    return local


def locked_requirements(path: Path) -> dict[str, str]:
    """Accept the unconditional, hash-pinned pip-compile format used by this repo."""
    requirements = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", "--hash=")):
            continue
        match = re.fullmatch(r"([A-Za-z0-9_.-]+)==([^\s;\\]+)\s*\\?", stripped)
        if not match:
            raise ValueError(f"Unsupported lockfile requirement: {stripped}")
        name, version = match.groups()
        if name in requirements:
            raise ValueError(f"Duplicate lockfile requirement: {name}")
        requirements[name] = version
    if not requirements:
        raise ValueError(f"Empty operations lockfile: {path}")
    return requirements


def prepare(root: Path, environment: Path) -> tuple[Path, dict[str, str], dict]:
    """Validate the venv and prepare an environment inherited by all children."""
    config = environment / "pyvenv.cfg"
    if not config.is_file():
        raise ValueError(f"Operations virtual environment missing: {environment}; use --env PATH")
    settings = dict(line.lower().split("=", 1) for line in config.read_text(encoding="utf-8").splitlines()
                    if "=" in line)
    settings = {key.strip(): value.strip() for key, value in settings.items()}
    if settings.get("include-system-site-packages") != "false":
        raise ValueError(f"Operations environment must disable system site-packages: {environment}")
    python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not python.is_file():
        raise ValueError(f"Operations interpreter missing: {python}")
    child_env = os.environ.copy()
    child_env["PATH"] = str(python.parent) + os.pathsep + child_env.get("PATH", "")
    child_env["VIRTUAL_ENV"] = str(environment)
    child_env["PYTHONNOUSERSITE"] = "1"
    for key in ("PYTHONHOME", "PYTHONPATH"):
        child_env.pop(key, None)
    expected = locked_requirements(root / "requirements-ops.lock")
    result = subprocess.run(
        [str(python), "-I", "-c", PROBE, json.dumps(expected), str(environment)],
        cwd=root, env=child_env, capture_output=True, text=True, timeout=30, check=False,
    )
    if result.returncode:
        raise ValueError(f"Operations interpreter failed: {python}\n{result.stderr.strip()}")
    report = json.loads(result.stdout)
    if report["errors"]:
        raise ValueError("Operations environment does not match this checkout:\n  "
                         + "\n  ".join(report["errors"]))
    report["locked_packages"] = len(expected)
    return python, child_env, report


def main(argv: list[str] | None = None) -> int:
    """Validate and run a task without changing the invoking shell's environment."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env", help="operations venv directory (before the command); defaults to FP_OPS_ENV")
    parser.add_argument('--workers', type=int, choices=range(0, 9),
                        help='Opt-in pytest workers, 0 through 8; nonzero uses loadscope')
    parser.add_argument("command", choices=("doctor", "python", "test", "test-ops", "check"))
    parser.add_argument("args", nargs=argparse.REMAINDER, help="arguments passed unchanged to the command")
    options = parser.parse_args(argv)
    if options.command == "doctor" and options.args:
        parser.error("doctor does not accept additional arguments")
    pytest_task = options.command in ('test', 'test-ops') or (
        options.command == 'python' and options.args[:2] == ['-m', 'pytest'])
    if options.workers is not None and not pytest_task:
        parser.error('--workers applies only to pytest commands')
    root = Path(__file__).resolve().parents[1]
    try:
        record = None
        if pytest_task or options.command == 'check':
            spec = importlib.util.spec_from_file_location('fp_recorder', root / 'scripts/record_verification.py')
            recorder = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(recorder)
            identity = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid4().hex[:12]
            output = root / '.cache' / 'fp-verification' / identity
            record = recorder.RunRecord(root, output, [options.command, *options.args], allow_ignored=True)
        with record if record is not None else nullcontext():
            if record is not None:
                record.begin()
            selection = options.env if options.env is not None else os.environ.get("FP_OPS_ENV")
            environment = resolve_environment(root, selection)
            python, child_env, report = prepare(root, environment)
            if options.command == "doctor":
                print(f"Checkout: {root}\nEnvironment: {environment}\nPython: {report['python']} "
                      f"({report['version']})\nLocked packages matched: {report['locked_packages']}\n"
                      f"Optional signing dependency: {report['signing']}")
                return 0
            commands = {
                "python": [],
                "test": ["-m", "pytest", "tests/"],
                "test-ops": ["-m", "pytest", "tests/ops/"],
                "check": ["scripts/gate_manifest.py", "--tier", "check"],
            }
            command = [str(python), *commands[options.command], *options.args]
            if record is None:
                return subprocess.call(command, cwd=root, env=child_env)
            report['workers'] = options.workers
            report['locked_requirements'] = locked_requirements(root / 'requirements-ops.lock')
            record.data['metadata'] = report
            reports = []
            if pytest_task:
                command += ['-p', 'scripts.pytest_junit_subtests']
                if options.workers is not None:
                    command += ['-n', str(options.workers)]
                    if options.workers:
                        command += ['--dist=loadscope']
                destination = None
                for index, argument in enumerate(options.args):
                    if argument in ('--junitxml', '--junit-xml'):
                        if index + 1 == len(options.args):
                            raise ValueError('JUnit destination is missing')
                        destination = options.args[index + 1]
                    elif argument.startswith(('--junitxml=', '--junit-xml=')):
                        destination = argument.split('=', 1)[1]
                if destination is None:
                    destination = str(output / 'junit.xml')
                    command += ['--junitxml=' + destination]
                reports = [(root / destination).resolve()]
            with tempfile.TemporaryDirectory(prefix='fp-pytest-') as scratch:
                if pytest_task and not any(a == '--basetemp' or a.startswith('--basetemp=') for a in options.args):
                    command += ['--basetemp=' + str(Path(scratch) / 'pytest')]
                record.execute(command, env=child_env, reports=reports)
        return record.data['verification_exit_code']
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print(f"fp: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
