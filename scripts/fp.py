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
import shlex
import subprocess
import sys
import tempfile
import tomllib
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


def expand_pytest_argument_files(root: Path, args: list[str]) -> tuple[list[str], set[Path]]:
    """Match pytest's one-argument-per-line files, before any validation."""
    files = set()
    remaining = 100_000

    def expand(arguments, stack):
        nonlocal remaining
        result = []
        for argument in arguments:
            remaining -= 1
            if remaining < 0:
                raise ValueError('Pytest argument file expansion exceeds 100000 arguments')
            if not argument.startswith('@'):
                result.append(argument)
                continue
            path = root / argument[1:]
            identity = path.resolve()
            if identity in stack or len(stack) >= 16:
                raise ValueError(f'Cyclic or excessively nested pytest argument file: {path}')
            with path.open('r', encoding=sys.getfilesystemencoding(),
                           errors=sys.getfilesystemencodeerrors()) as source:
                content = source.read(1_000_001)
            if len(content) > 1_000_000:
                raise ValueError(f'Pytest argument file exceeds 1000000 characters: {path}')
            files.add(path)
            # Like argparse, nested relative paths resolve from pytest's cwd,
            # not from the containing argument file's directory.
            result.extend(expand(content.splitlines(), (*stack, identity)))
        return result

    return expand(args, ()), files


def configured_pytest_arguments(root: Path, args: list[str]) -> list[str]:
    """Materialize pytest's single addopts layer so inputs cannot hide in it."""
    config = tomllib.loads((root / 'pyproject.toml').read_text(encoding='utf-8'))
    table = config.get('tool', {}).get('pytest', {})
    native = {key: value for key, value in table.items() if key != 'ini_options'}
    legacy = table.get('ini_options', {})
    if native and legacy:
        raise ValueError('Cannot combine native pytest configuration and ini_options')
    value = (native or legacy).get('addopts', [])
    iterator = iter(args)
    for argument in iterator:
        if argument == '--':
            break
        override = None
        if argument in ('-o', '--override-ini'):
            override = next(iterator, '')
        elif argument.startswith('--override-ini='):
            override = argument.split('=', 1)[1]
        elif argument.startswith('-o') and not argument.startswith('--'):
            override = argument[2:].removeprefix('=')
        if override is not None:
            name, separator, selected = override.partition('=')
            if separator and name.strip() == 'addopts':
                value = selected
    if isinstance(value, str):
        return shlex.split(value)
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError('Pytest addopts must be a string or list of strings')
    return value


def pytest_report_selection(args: list[str]) -> tuple[list[str], dict[str, str]]:
    """Separate output option values from possible source paths, honoring --."""
    inputs = []
    outputs = {}
    iterator = iter(args)
    for argument in iterator:
        if argument == '--':
            inputs.extend(iterator)
            break
        key, separator, value = argument.partition('=')
        if key in ('--junitxml', '--junit-xml', '--log-file'):
            if not separator:
                value = next(iterator, '')
            if not value:
                raise ValueError(f'{key} destination is missing')
            outputs['junit' if key != '--log-file' else 'log'] = value
        else:
            inputs.append(argument)
    return inputs, outputs


def pytest_configuration_args(root: Path, args: list[str]) -> list[str]:
    """Normalize checkout selection and reject competing explicit selections."""
    result = []
    iterator = iter(args)
    for argument in iterator:
        if argument == '--':
            result.extend([argument, *iterator])
            break
        key, separator, value = argument.partition('=')
        if key in ('-c', '--config-file', '--rootdir'):
            if not separator:
                value = next(iterator, '')
        elif argument.startswith('-c') and not argument.startswith('--'):
            key, value = '-c', argument[2:]
        else:
            result.append(argument)
            continue
        expected = root if key == '--rootdir' else root / 'pyproject.toml'
        comparable = os.path.expandvars(value) if key == '--rootdir' else value
        if not value or (root / comparable).resolve() != expected.resolve():
            raise ValueError(f'Conflicting pytest {key}: expected {expected}, got {value!r}')
    return ['-c', str(root / 'pyproject.toml'), '--rootdir=' + str(root), *result]


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
                # Parse ambient arguments once, so they cannot silently override
                # the checkout contract or escape the recorded command.
                ambient = shlex.split(child_env.pop('PYTEST_ADDOPTS', ''))
                expanded, argument_files = expand_pytest_argument_files(root, [*ambient, *command[3:]])
                configured, config_files = expand_pytest_argument_files(
                    root, configured_pytest_arguments(root, expanded))
                argument_files |= config_files
                # Suppress pytest's later addopts expansion: it is now explicit.
                command[3:] = pytest_configuration_args(root, [*configured, *expanded])
                report.update(pytest_config=str(root / 'pyproject.toml'), pytest_root=str(root))
                input_args, output_options = pytest_report_selection(command[3:])
                destination = output_options.get('junit')
                source_candidates = {
                    Path(os.path.abspath(root / arg.split('::', 1)[0]))
                    for arg in input_args if not arg.startswith('-')
                    and (root / arg.split('::', 1)[0]).is_file()
                } | argument_files
                trailing = []
                if '--' in command:
                    delimiter = command.index('--')
                    trailing, command = command[delimiter:], command[:delimiter]
                pytest_options = command[3:]
                command += ['-o', 'addopts=', '-p', 'scripts.pytest_junit_subtests', '-p', 'scripts.pytest_progress']
                child_env['FP_PYTEST_PROGRESS_DIR'] = str(output)
                child_env['FP_PYTEST_PROGRESS_RUN'] = record.data['run_id']
                if options.workers is not None:
                    command += ['-n', str(options.workers)]
                    if options.workers:
                        command += ['--dist=loadscope']
                if destination is None:
                    destination = str(output / 'junit.xml')
                    command += ['--junitxml=' + destination]
                reports = [(root / os.path.expanduser(os.path.expandvars(destination))).resolve()]
                outputs = [*reports]
                if 'log' in output_options:
                    outputs.append((root / output_options['log']).resolve())
                if any(p.resolve() == out or (out.exists() and p.samefile(out))
                       for p in source_candidates for out in outputs):
                    raise ValueError('Pytest output overlaps a selected source or argument file')
                record.track_external_files({p for p in source_candidates
                                             if not p.is_relative_to(root) or
                                             not p.resolve().is_relative_to(root)})
            with tempfile.TemporaryDirectory(prefix='fp-pytest-') as scratch:
                if pytest_task and not any(a == '--basetemp' or a.startswith('--basetemp=') for a in pytest_options):
                    command += ['--basetemp=' + str(Path(scratch) / 'pytest')]
                record.execute(command + (trailing if pytest_task else []), env=child_env, reports=reports)
        return record.data['verification_exit_code']
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print(f"fp: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
