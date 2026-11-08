"""Exercise the launcher at its process boundary, including nested Python."""
import importlib.metadata
import importlib.util
import json
import os
from pathlib import Path
import shutil
import site
import subprocess
import sys
import venv

import pytest

SOURCE = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def ops_env(tmp_path_factory):
    """Build an offline fixture venv even when CI runs pytest in global Python."""
    environment = tmp_path_factory.mktemp("operations env")
    venv.EnvBuilder(with_pip=False).create(environment)
    python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    target = Path(subprocess.check_output(
        [str(python), "-I", "-c", "import sysconfig; print(sysconfig.get_path('purelib'))"], text=True
    ).strip())
    # Test-only dependency reuse: no network or installs during the test run.
    # Production environment setup does not add these paths.
    paths = [str(Path(pytest.__file__).resolve().parents[1]), *site.getsitepackages()]
    (target / "fixture-dependencies.pth").write_text(
        "\n".join(path for path in paths if Path(path).is_dir()) + "\n", encoding="utf-8"
    )
    return str(environment)


@pytest.fixture
def checkout(tmp_path):
    root = tmp_path / "checkout with spaces"
    (root / "scripts").mkdir(parents=True)
    launcher = SOURCE / "scripts/fp.py"
    assert launcher.is_file(), "operations launcher has not been implemented"
    shutil.copy2(launcher, root / "scripts/fp.py")
    shutil.copy2(SOURCE / "scripts/gate_manifest.py", root / "scripts/gate_manifest.py")
    (root / "requirements-ops.lock").write_text(
        f"pytest=={importlib.metadata.version('pytest')}\n", encoding="utf-8"
    )
    (root / 'pyproject.toml').write_text('[tool.pytest.ini_options]\n')
    (root / '.gitignore').write_text('.cache/\n__pycache__/\n.pytest_cache/\n')
    subprocess.run(['git', 'init', '-q', str(root)], check=True)
    subprocess.run(['git', '-C', str(root), 'add', '.'], check=True)
    subprocess.run(['git', '-C', str(root), '-c', 'user.name=Test',
                    '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'fixture'], check=True)
    return root


XDIST_PROBE = 'def test_worker():\n    import os\n    assert os.environ["PYTEST_XDIST_WORKER"].startswith("gw")\n'


@pytest.mark.parametrize('fails', [False, True])
def test_pytest_runs_directly_and_returns_its_result(checkout, ops_env, fails):
    (checkout / 'test_example.py').write_text('def test_value():\n    assert ' + str(not fails) + '\n')
    result = launch(checkout, '--env', ops_env, 'python', '-m', 'pytest', 'test_example.py', '-q')
    assert result.returncode == int(fails), result.stderr
    assert ('1 failed' if fails else '1 passed') in result.stdout
    assert not (checkout / '.cache/fp-verification').exists()


@pytest.mark.parametrize('selection', [('test_parallel.py', '-q'), ('-q', '--', 'test_parallel.py')])
def test_workers_run_pytest_under_xdist(checkout, ops_env, selection):
    (checkout / 'test_parallel.py').write_text(XDIST_PROBE)
    result = launch(checkout, '--env', ops_env, '--workers', '2', 'python', '-m', 'pytest', *selection)
    assert result.returncode == 0, result.stdout + result.stderr


def test_zero_workers_run_serially(checkout, ops_env):
    (checkout / 'test_serial.py').write_text('def test_serial():\n    import os\n    assert "PYTEST_XDIST_WORKER" not in os.environ\n')
    result = launch(checkout, '--env', ops_env, '--workers', '0', 'python', '-m', 'pytest', 'test_serial.py', '-q')
    assert result.returncode == 0, result.stdout + result.stderr


def test_workers_are_refused_outside_pytest(checkout, ops_env):
    result = launch(checkout, '--env', ops_env, '--workers', '2', 'python', '-c', "print('RAN')")
    assert result.returncode == 2 and '--workers applies only to pytest commands' in result.stderr
    assert 'RAN' not in result.stdout


def launch(root, *args, env=None):
    process_env = os.environ.copy()
    process_env.pop("FP_OPS_ENV", None)
    process_env.pop("PYTEST_XDIST_WORKER", None)  # Set when this suite itself runs under xdist.
    process_env.update(env or {})
    return subprocess.run(
        [sys.executable, "-I", str(root / "scripts/fp.py"), *args],
        cwd=root.parent, env=process_env, capture_output=True, text=True, check=False,
    )


def test_parent_and_nested_python_use_selected_environment(checkout, ops_env):
    code = (
        "import json,os,shutil,subprocess,sys; "
        "child=subprocess.check_output([shutil.which('python'),'-c','import sys; print(sys.prefix)'],text=True); "
        "print(json.dumps([sys.prefix,child.strip(),os.getcwd(),sys.argv[1:],"
        "os.environ.get('VIRTUAL_ENV'),os.environ.get('PYTHONPATH')]))"
    )
    result = launch(checkout, "--env", ops_env, "python", "-c", code,
                    "space value", 'quote"value', "", "$literal", "--flag",
                    env={"PYTHONPATH": str(checkout / "untrusted"),
                         "PYTHONHOME": str(checkout / "invalid-home")})
    assert result.returncode == 0, result.stderr
    values = json.loads(result.stdout)
    assert Path(values[0]).samefile(ops_env)
    assert Path(values[1]).samefile(ops_env)
    assert Path(values[2]).samefile(checkout)
    assert values[3] == ["space value", 'quote"value', "", "$literal", "--flag"]
    assert Path(values[4]).samefile(ops_env)
    assert values[5] is None


def test_child_exit_status_is_preserved(checkout, ops_env):
    result = launch(checkout, "--env", ops_env, "python", "-c", "raise SystemExit(17)")
    assert result.returncode == 17


def test_invalid_explicit_environment_does_not_fall_back(checkout, ops_env):
    result = launch(checkout, "--env", str(checkout / "missing"), "python", "-c", "print('RAN')",
                    env={"FP_OPS_ENV": ops_env})
    assert result.returncode == 2
    assert "RAN" not in result.stdout
    assert "missing" in result.stderr


def test_environment_variable_selects_venv(checkout, ops_env):
    result = launch(checkout, "doctor", env={"FP_OPS_ENV": ops_env})
    assert result.returncode == 0, result.stderr
    assert str(Path(ops_env)) in result.stdout


def test_doctor_names_shared_supplements_when_signing_is_absent(checkout, tmp_path):
    """The qualification bridge fails, not skips, without cryptography; say what supplies it."""
    environment = tmp_path / "bare env"
    venv.EnvBuilder(with_pip=False).create(environment)
    python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    purelib = Path(subprocess.check_output(
        [str(python), "-I", "-c", "import sysconfig; print(sysconfig.get_path('purelib'))"], text=True
    ).strip())
    metadata = purelib / "fixture_marker-1.0.dist-info"
    metadata.mkdir()
    (metadata / "METADATA").write_text(
        "Metadata-Version: 2.1\nName: fixture-marker\nVersion: 1.0\n", encoding="utf-8")
    (checkout / "requirements-ops.lock").write_text("fixture-marker==1.0\n", encoding="utf-8")
    result = launch(checkout, "--env", str(environment), "doctor")
    assert result.returncode == 0, result.stderr
    assert "Optional signing dependency: absent" in result.stdout
    assert "tools/local_verification/requirements-extra.txt" in result.stdout


def test_lock_mismatch_blocks_execution(checkout, ops_env):
    (checkout / "requirements-ops.lock").write_text("pytest==0.0.0\n", encoding="utf-8")
    result = launch(checkout, "--env", ops_env, "python", "-c", "print('RAN')")
    assert result.returncode == 2
    assert "pytest" in result.stderr and "0.0.0" in result.stderr
    assert "RAN" not in result.stdout


def test_missing_package_blocks_execution(checkout, ops_env):
    (checkout / "requirements-ops.lock").write_text("first-passage-nonexistent-dependency==1.0\n", encoding="utf-8")
    result = launch(checkout, "--env", ops_env, "doctor")
    assert result.returncode == 2
    assert "first-passage-nonexistent-dependency" in result.stderr


def test_global_python_is_not_an_operations_venv(checkout):
    result = launch(checkout, "--env", sys.base_prefix, "doctor")
    assert result.returncode == 2


def test_check_uses_actual_gate_runner_and_selected_child_python(checkout, ops_env):
    output = checkout / "gate-result.json"
    (checkout / "scripts/probe.py").write_text(
        "import json,sys\nfrom pathlib import Path\n"
        "Path('gate-result.json').write_text(json.dumps([sys.prefix, str(Path.cwd())]))\n"
        "raise SystemExit(7)\n", encoding="utf-8"
    )
    (checkout / "scripts/gates.yml").write_text(
        "version: 1\ngates:\n  - id: probe\n    tier: always\n"
        "    cmd:\n      - python\n      - scripts/probe.py\n", encoding="utf-8"
    )
    result = launch(checkout, "--env", ops_env, "check")
    assert result.returncode != 0
    prefix, cwd = json.loads(output.read_text())
    assert Path(prefix).samefile(ops_env)
    assert Path(cwd).samefile(checkout)


@pytest.mark.parametrize("command,folder", [("test", "tests"), ("test-ops", "tests/ops")])
def test_test_commands_execute_requested_suite(checkout, ops_env, command, folder):
    target = checkout / folder
    target.mkdir(parents=True)
    (target / "test_example.py").write_text("def test_example():\n    assert False, 'real-test-ran'\n", encoding="utf-8")
    result = launch(checkout, "--env", ops_env, command, "-q", "-p", "no:cacheprovider")
    assert result.returncode == 1
    assert "real-test-ran" in result.stdout


def test_powershell_wrapper_preserves_arguments(checkout, ops_env):
    shell = shutil.which("pwsh")
    if not shell:
        pytest.skip("PowerShell unavailable")
    shutil.copy2(SOURCE / "fp.ps1", checkout / "fp.ps1")
    # The wrapper's bootstrap may use PATH Python; task execution must not.
    result = subprocess.run(
        [shell, "-NoProfile", "-File", str(checkout / "fp.ps1"), "--env", ops_env,
         "python", "-c", "import json,sys; print(json.dumps(sys.argv[1:])); sys.exit(19)",
         "space value", 'quote"value', "", "$literal", "--flag"],
        cwd=checkout.parent, capture_output=True, text=True, check=False,
    )
    assert result.returncode == 19, result.stderr
    assert json.loads(result.stdout) == ["space value", 'quote"value', "", "$literal", "--flag"]


def test_default_selection_finds_main_checkout_from_linked_worktree(checkout, tmp_path):
    spec = importlib.util.spec_from_file_location("fp", SOURCE / "scripts/fp.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    main = tmp_path / "main checkout"
    common = main / ".git"
    metadata = common / "worktrees" / "linked"
    metadata.mkdir(parents=True)
    (metadata / "commondir").write_text("../..\n", encoding="utf-8")
    (checkout / '.git').rename(checkout / '.git-fixture-metadata')
    (checkout / ".git").write_text(f"gitdir: {metadata}\n", encoding="utf-8")
    expected = main / "tmp/ops-env"
    expected.mkdir(parents=True)
    assert module.resolve_environment(checkout, None) == expected
    local = checkout / "tmp/ops-env"
    local.mkdir(parents=True)
    assert module.resolve_environment(checkout, None) == local


def test_explicit_selection_wins_over_environment_variable(checkout, ops_env):
    result = launch(checkout, "--env", ops_env, "doctor",
                    env={"FP_OPS_ENV": str(checkout / "missing")})
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("content", ["", "pytest>=1\n"])
def test_invalid_lockfile_does_not_approve_environment(checkout, ops_env, content):
    (checkout / "requirements-ops.lock").write_text(content, encoding="utf-8")
    result = launch(checkout, "--env", ops_env, "doctor")
    assert result.returncode == 2
    assert "lock" in result.stderr.lower()


def test_explicit_empty_selection_does_not_fall_back(checkout, ops_env):
    result = launch(checkout, "--env", "", "doctor", env={"FP_OPS_ENV": ops_env})
    assert result.returncode == 2
    assert "empty" in result.stderr.lower()


def test_powershell_native_error_preference_preserves_exit_status(checkout, ops_env):
    shell = shutil.which("pwsh")
    if not shell:
        pytest.skip("PowerShell unavailable")
    shutil.copy2(SOURCE / "fp.ps1", checkout / "fp.ps1")
    env = os.environ.copy()
    env["FP_OPS_ENV"] = ops_env
    result = subprocess.run(
        [shell, "-NoProfile", "-Command",
         "$PSNativeCommandUseErrorActionPreference = $true; "
         "& ./fp.ps1 python -c 'raise SystemExit(17)'; exit $LASTEXITCODE"],
        cwd=checkout, env=env, capture_output=True, text=True, check=False,
    )
    assert result.returncode == 17, result.stderr


@pytest.mark.parametrize('route', [('python', '-m', 'pytest'), ('test',), ('test-ops',)])
def test_external_tests_use_checkout_configuration(checkout, ops_env, route):
    for folder, value in [(checkout.parent, 'PARENT'), (checkout, 'CHECKOUT')]:
        (folder / 'imports').mkdir()
        (folder / 'imports/sentinel.py').write_text(f'VALUE = {value!r}\n')
        (folder / 'pyproject.toml').write_text('[tool.pytest.ini_options]\npythonpath = ["imports"]\n')
    (checkout / 'tests/ops').mkdir(parents=True)
    external = checkout.parent / 'test_external.py'
    external.write_text('from sentinel import VALUE\ndef test_root():\n    assert VALUE == "CHECKOUT"\n')
    result = launch(checkout, '--env', ops_env, *route, str(external), '-q')
    assert result.returncode == 0, result.stdout + result.stderr


def test_delimited_external_selection_preserves_launcher_options(checkout, ops_env):
    external = checkout.parent / 'test_outside.py'
    external.write_text('def test_ok():\n    pass\n')
    result = launch(checkout, '--env', ops_env, 'python', '-m', 'pytest', '-q', '--', str(external))
    assert result.returncode == 0, result.stdout + result.stderr


def test_deliberate_overrides_are_retained(checkout, ops_env):
    (checkout / 'alternate').mkdir()
    (checkout / 'alternate/sentinel.py').write_text('VALUE = "OVERRIDE"\n')
    (checkout / 'test_override.py').write_text('from sentinel import VALUE\ndef test_ok():\n    assert VALUE == "OVERRIDE"\n')
    result = launch(checkout, '--env', ops_env, 'python', '-m', 'pytest', 'test_override.py',
                    '-o', 'pythonpath=alternate', '-q')
    assert result.returncode == 0, result.stdout + result.stderr
