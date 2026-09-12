"""Fault injection for the image validator, without a Docker daemon.

Run the real shell orchestration with a failing Docker boundary. A broken image
must produce a complete failing table, not terminate at the first launch.
"""

import ast
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import types

import pytest


ROOT = Path(__file__).resolve().parents[2]
LISTENER = "L1 L2 L3 L4 L5a L5b L6 L6b L7 L8 L9".split()
DAEMON = "D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11".split()


def test_d6_preserves_copied_fixture_and_uses_generated_manifest(tmp_path, monkeypatch, capsys):
    """Copied inputs may be unwritable; the CLI must use a separate validated manifest."""
    from c1_rail.m1_stage1_contract import contract_sha256
    from c1_signal_daemon.m1_stage1_state import CeremonyStore

    data = tmp_path / "data"
    data.mkdir()
    fixture = tmp_path / "copied_manifest.json"
    fixture.write_bytes((ROOT / "tests/fixtures/c1_image_validation/ceremony_manifest.json").read_bytes())
    original = fixture.read_bytes()
    config = json.loads((ROOT / "tests/fixtures/c1_image_validation/c1_signal_daemon_config.json").read_text())
    config["poll_interval_s"] = 1
    config["m1_test"]["state_path"] = str(data / "c1_m1_stage1_state.json")
    (data / "c1_signal_daemon_config.json").write_text(json.dumps(config))
    CeremonyStore(data / "c1_m1_stage1_state.json").boot("d6-test-boot")

    source = (ROOT / "scripts/c1_image_validation.sh").read_text(encoding="utf-8")
    found = re.search(r'cat >"\$LOG_DIR/D6_probe.py" <<\x27PY\x27\n(.*?)\nPY\n', source, re.S)
    assert found, "D6 executable probe missing"
    # Run the actual probe and CLI, adapting only container paths to this checkout.
    paths = {"/app": str(ROOT), "/app/ops": str(ROOT / "ops"),
             "/data": str(data), "/tmp/ceremony_manifest.json": str(fixture)}

    class LocalPaths(ast.NodeTransformer):
        def visit_Constant(self, node):
            if isinstance(node.value, str) and node.value in paths:
                return ast.copy_location(ast.Constant(paths[node.value]), node)
            return node

    calls = []
    real_run = subprocess.run

    def record_cli(args, **kwargs):
        result = real_run(args, **kwargs)
        if "--manifest" in args:
            manifest_path = Path(args[args.index("--manifest") + 1])
            calls.append((args[2], manifest_path, json.loads(manifest_path.read_text()),
                          result.returncode))
        return result

    monkeypatch.setattr(subprocess, "run", record_cli)
    monkeypatch.setattr(tempfile, "tempdir", str(tmp_path))
    tree = ast.fix_missing_locations(LocalPaths().visit(ast.parse(found.group(1))))
    exec(compile(tree, "D6_probe.py", "exec"), {"__name__": "d6_probe"})
    assert fixture.read_bytes() == original, "copied fixture was modified"
    assert [action for action, _, _, _ in calls] == ["prepare", "enable"]
    for _, path, value, code in calls:
        assert path != fixture and path.is_file()
        assert value["contract_sha256"] == contract_sha256()
        assert code == 2
    output = capsys.readouterr().out
    assert "inject: exit=2; config/state hashes unchanged; upload/bar/claim absent" in output
    assert not list(data.glob("m1_bar_*")) and not list(data.glob("m1_claim_*"))


def d11_probe():
    """Load the actual in-image probe without running its real-clock ceremony."""
    source = (ROOT / "scripts/c1_image_validation.sh").read_text(encoding="utf-8")
    found = re.search(r'cat >"\$LOG_DIR/D11_probe.py" <<\x27PY\x27\n(.*?)\nPY\n', source, re.S)
    assert found, "D11 executable probe missing"
    module = types.ModuleType("d11_probe")
    exec(compile(found.group(1), "D11_probe.py", "exec"), module.__dict__)
    return module


def test_d11_cli_failure_stops_before_wait(tmp_path):
    """A refused prepare must fail the probe before reaching its target wait."""
    probe = d11_probe()
    child = tmp_path / "refuse.py"
    child.write_text('print("ceremony control failed closed")\nraise SystemExit(2)\n')
    probe.CLI = [sys.executable, str(child)]
    with pytest.raises(AssertionError, match="prepare exit=2"):
        probe.command("prepare", 0)


def test_d11_captured_value_leak_is_not_echoed(tmp_path, capsys):
    """A faulty CLI printing a bar value fails without amplifying it to CI logs."""
    probe = d11_probe()
    child = tmp_path / "leak.py"
    child.write_text('print("41001")\n')
    probe.CLI = [sys.executable, str(child)]
    with pytest.raises(AssertionError, match="bar value leaked"):
        probe.command("inject", 0)
    assert "41001" not in capsys.readouterr().out


def test_d11_wait_refuses_a_missed_window():
    """A delayed runner must fail promptly instead of injecting outside the test window."""
    probe = d11_probe()
    with pytest.raises(AssertionError, match="missed injection checkpoint"):
        probe.wait_until(0, latest=1)


@pytest.fixture
def shell():
    """Use Git Bash on Windows, rather than the unrelated WSL launcher."""
    executable = (
        Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "Git/bin/bash.exe"
        if os.name == "nt" else shutil.which("bash")
    )
    if not executable or not Path(executable).exists():
        pytest.skip("Bash is required for the Linux image harness")
    return str(executable)


@pytest.mark.parametrize("failure,target,expected", [
    (failure, target, expected)
    for failure in ("build", "runtime", "post_copy")
    for target, expected in (("listener", LISTENER), ("daemon", DAEMON),
                             ("all", LISTENER + DAEMON))
] + [("manifest", "daemon", DAEMON), ("empty_suite", "daemon", DAEMON)])
def test_docker_failure_emits_every_result(shell, tmp_path, target, expected, failure):
    """Docker create/exec failures must not suppress later checks or the summary."""
    script = ROOT / "scripts/c1_image_validation.sh"
    if failure in ("manifest", "empty_suite"):
        # Isolate malformed/missing inputs; never mutate the checked-in fixtures.
        checkout = tmp_path / "checkout"
        (checkout / "scripts").mkdir(parents=True)
        shutil.copytree(ROOT / "tests/fixtures/c1_image_validation",
                        checkout / "tests/fixtures/c1_image_validation")
        script = Path(shutil.copy2(script, checkout / "scripts"))
        if failure == "manifest":
            (checkout / "tests/fixtures/c1_image_validation/ceremony_manifest.json").write_text(
                "{}", encoding="utf-8",
            )
    stub = tmp_path / "boundary.sh"
    docker_body = (
        'if [ "$1" = build ] && [ "$FAILURE" != build ]; then exit 0; fi\n'
        'echo "injected Docker failure: $*" >&2\n'
        "exit 125\n"
    )
    # Python probes spawn Docker directly, outside Bash functions. Shadow that
    # executable too so Linux CI cannot accidentally use its real Docker daemon.
    bindir = tmp_path / "bin"
    bindir.mkdir()
    docker = bindir / "docker"
    docker.write_text("#!/bin/sh\n" + docker_body, encoding="utf-8")
    docker.chmod(0o755)
    stub.write_text(
        "docker() {\n"
        '  if [[ "$1" == build && "$FAILURE" != build ]]; then return 0; fi\n'
        '  if [[ "$FAILURE" == empty_suite && "$*" == *"bash -lc"* ]]; then\n'
        '    echo "1 passed"; return 0\n'
        '  fi\n'
        '  if [[ "$FAILURE" == post_copy ]]; then\n'
        '    case "$*" in\n'
        '      "run --rm -i "*)\n'
        '        local previous="" argument\n'
        '        for argument in "$@"; do\n'
        '          if [[ "$previous" == -v ]]; then\n'
        '            printf "{}" > "${argument%:/data}/c1_sizing_constants.json"\n'
        '          fi\n'
        '          previous="$argument"\n'
        '        done\n'
        '        return 0 ;;\n'
        '      "run -d --name c1-L4 "*) return 0 ;;\n'
        '      "inspect "*" c1-L4") echo true; return 0 ;;\n'
        '      "logs c1-L4") echo "dry_run=True armed_until=-"; return 0 ;;\n'
        '      "cp "*"c1-L4:/tmp/_http_get.py") return 0 ;;\n'
        '      "cp "*"c1-L4:/tmp/_http_post.py")\n'
        '        POST_COPIES=$((${POST_COPIES:-0} + 1))\n'
        '        if [[ "$POST_COPIES" == 1 ]]; then return 0; fi ;;\n'
        '      "exec c1-L4 python /tmp/_http_get.py "*)\n'
        '        printf \'200\\n{"ok":true,"service":"c1_rail_http_server"}\\n\'; return 0 ;;\n'
        '      "exec c1-L4 python /tmp/_http_post.py "*)\n'
        '        printf "200\\ndry_run: computed, not sent\\n"; return 0 ;;\n'
        '      "exec c1-L4 python ops/c1_rail/m1_stage1_control.py migrate "*)\n'
        '        touch "$LOG_DIR/L4_data/stub.m1-backup-ci"\n'
        '        printf \'{"before":{"constants":"x","lifecycle":"y"}}\\n\'; return 0 ;;\n'
        '      "exec -i c1-L4 python -") echo contract-hash; return 0 ;;\n'
        '    esac\n'
        '  fi\n'
        '  echo "injected Docker failure: $*" >&2\n'
        "  return 125\n"
        "}\n"
        "sleep() { :; }\n"
        'python3() { "$TEST_PYTHON" "$@"; }\n',
        encoding="utf-8",
    )
    logs = tmp_path / "logs"
    env = dict(os.environ, BASH_ENV=stub.as_posix(), FAILURE=failure,
               PATH=str(bindir) + os.pathsep + os.environ["PATH"],
               TEST_PYTHON=Path(sys.executable).as_posix(),
               C1_IMAGE_VALIDATION_LOG_DIR=logs.as_posix())
    result = subprocess.run(
        [shell, script.as_posix(), target], cwd=ROOT, env=env,
        capture_output=True, text=True, timeout=90, check=False,
    )
    summary = logs / "summary.txt"
    assert summary.exists(), result.stdout + result.stderr
    lines = summary.read_text(encoding="utf-8").splitlines()
    passing = set() if failure == "build" else {"L1", "D1"}
    if failure == "post_copy":
        passing.add("L4")
    wanted = [f"{'PASS' if key in passing else 'FAIL'} {key}"
              for key in expected]
    assert lines[:-1] == wanted, result.stdout + result.stderr
    assert result.returncode == 1, result.stdout + result.stderr
    if failure == "post_copy" and target != "daemon":
        assert "injected Docker failure: cp" in (logs / "L5b.post.err").read_text(
            encoding="utf-8",
        )
        assert not (logs / "L5b.out").exists()
    if failure != "build":
        last_logs = (["L9_inimage.log"] if target == "listener" else
                     ["D10.err", "D11.err"] if target == "daemon" else
                     ["L9_inimage.log", "D10.err", "D11.err"])
        for name in last_logs:
            assert "injected Docker failure" in (logs / name).read_text(encoding="utf-8")
