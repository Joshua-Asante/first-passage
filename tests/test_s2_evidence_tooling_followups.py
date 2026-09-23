"""Follow-ups from the independent review of card 3 (S2 evidence tooling).

Non-frozen regression tests; the card's frozen acceptance suite is unchanged.
"""
import importlib
import os
import subprocess
from pathlib import Path

import pytest
import yaml

from scripts import guard_s2_runs as guard

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/qualification-s2-supervision.yml"


def _step(name):
    steps = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))["jobs"]["s2-supervision"]["steps"]
    return next(s for s in steps if s.get("name") == name)


@pytest.fixture
def linux_root(monkeypatch):
    module = importlib.import_module("scripts.qualification_boundary_verification")
    monkeypatch.setattr(module.platform, "system", lambda: "Linux")
    monkeypatch.setattr(module.os, "geteuid", lambda: 0, raising=False)
    return module


@pytest.mark.parametrize("expression", ["not " * 2000 + "a", "(" * 400 + "a" + ")" * 400])
def test_too_deep_an_expression_is_refused_like_any_uncompilable_one(linux_root, capsys, expression):
    """pytest's parser raises RecursionError, not SyntaxError, for very deep input."""
    assert linux_root.main(["--s3", "--cases", expression]) == 2
    assert "--cases" in capsys.readouterr().err


@pytest.mark.parametrize("cases,ok", [
    (" ", False), ("　  ", False), (" downtime", True), ("-downtime", True),
])
def test_validate_inputs_uses_the_wrappers_whitespace_test(tmp_path, shell, cases, ok):
    """NBSP and other Unicode spaces are whitespace to the wrapper's str.strip()."""
    step = _step("Validate inputs")
    script = tmp_path / "validate.sh"
    script.write_text(step["run"], encoding="utf-8")
    result = subprocess.run([shell, str(script)], capture_output=True, text=True, check=False, timeout=30,
                            env=dict(os.environ, BOUNDARY_MODE="s3", BOUNDARY_CASES=cases))
    assert (result.returncode == 0) is ok, result.stdout + result.stderr


def test_boundary_run_passes_cases_in_equals_form():
    """`--cases=<expr>` lets a valid -k expression start with '-'."""
    run = _step("Doctor and targeted boundary run")["run"]
    assert '"--cases=$cases"' in run
    assert '--cases "$cases"' not in run


def test_wrapper_accepts_a_leading_dash_expression_in_equals_form(linux_root, capsys):
    assert linux_root.main(["--s3", "--cases=-downtime"]) == 2  # stops at the next prerequisite
    err = capsys.readouterr().err
    assert "--manifest" in err and "--cases" not in err


@pytest.mark.parametrize("mode,scope", [("s2", " --expect-scope S2_DIAGNOSTIC_SUPERVISION"), ("s3", "")])
def test_guard_advice_reads_a_passed_run_with_its_own_scope(mode, scope):
    """The reader's default scope is S3; a passed s2 run must be read as s2."""
    run = {"databaseId": 21, "headSha": "a" * 40, "status": "completed", "conclusion": "success",
           "event": "workflow_dispatch", "displayTitle": f"Qualification S2 supervision [{mode}] (feat)",
           "workflowName": "Qualification S2 supervision", "createdAt": "2026-09-23T00:00:00Z"}
    reason = guard.dispatch_redundancy_refusal("a" * 40, [run], mode=mode)
    assert f"scripts/s2_run_evidence.py 21{scope})" in reason
