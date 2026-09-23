"""Acceptance suite for the S2 evidence and diagnostic-tooling card (G1-G8).

Card: docs/briefs/handoffs/2026-09-23-s2-evidence-tooling-hardening.md. Coordinator-authored
and frozen by SHA-256 in that card: the worker makes these pass without editing this file.
`s2_run_evidence.run_head` and `.download` are the reader's only gh seams; the tests replace
them, so no gh is needed.
"""
import importlib
import json
import os
import re
import subprocess
from pathlib import Path

import pytest
import yaml

from scripts import s2_run_evidence as evidence

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/qualification-s2-supervision.yml"
SKILL = ROOT / ".claude/skills/s2-linux-run/SKILL.md"
README = ROOT / "tools/qualification_verification/README.md"
HEAD = "abcdef0123456789abcdef0123456789abcdef01"
MERGE = "1111111111111111111111111111111111111111"


def write_artifact(dest, *, scope="S3_N1_CAPTURE", required=19, tests=19, tested=HEAD):
    record_dir = Path(dest) / "record0"
    record_dir.mkdir(parents=True)
    record = {"status": "completed", "exit_code": 0, "verification_exit_code": 0,
              "source_stable": True, "capture_complete": True, "cleanup": {"ok": True},
              "metadata": {"acceptance_scope": scope},
              "before": None if tested is None else {"commit": tested, "fingerprint": "f"}}
    (record_dir / "record.json").write_text(json.dumps(record), encoding="utf-8")
    (record_dir / "invariants.json").write_text(
        json.dumps({"passed": True, "required_nodeids": [f"n{i}" for i in range(required)]}), encoding="utf-8")
    (record_dir / "junit.xml").write_text(
        f'<testsuites><testsuite tests="{tests}" failures="0" errors="0" skipped="0"/></testsuites>',
        encoding="utf-8")


@pytest.fixture
def gh(monkeypatch, tmp_path):
    """Replace the reader's gh seams; `state` controls the run and the artifact."""
    state = {"head": {"headSha": HEAD, "headBranch": "feat", "event": "workflow_dispatch",
                      "conclusion": "success", "status": "completed", "createdAt": "2026-09-23T00:00:00Z"},
             "artifact": {}, "calls": []}

    def run_head(run_id):
        state["calls"].append(("head", run_id))
        return dict(state["head"])

    def download(run_id, dest):
        state["calls"].append(("download", run_id))
        write_artifact(dest, **state["artifact"])
    monkeypatch.setattr(evidence, "run_head", run_head)
    monkeypatch.setattr(evidence, "download", download)
    state["dest"] = tmp_path / "dl"
    return state


def read(gh, capsys, *extra):
    code = evidence.main(["35800000000", "--dest", str(gh["dest"]), *extra])
    out = capsys.readouterr().out
    return code, (json.loads(out) if out.strip().startswith("{") else {"raw": out})


# --- G1: the acceptance-grade scope is s3 unless asked otherwise ------------------

def test_g1_an_s2_mode_run_is_not_acceptance_by_default(gh, capsys):
    gh["artifact"] = {"scope": "S2_DIAGNOSTIC_SUPERVISION", "required": 15, "tests": 15}
    code, out = read(gh, capsys)
    assert code != 0 and out["ok"] is False
    assert "S3_N1_CAPTURE" in json.dumps(out)


def test_g1_an_s2_mode_run_is_readable_when_asked_for_explicitly(gh, capsys):
    gh["artifact"] = {"scope": "S2_DIAGNOSTIC_SUPERVISION", "required": 15, "tests": 15}
    code, out = read(gh, capsys, "--expect-scope", "S2_DIAGNOSTIC_SUPERVISION")
    assert code == 0 and out["ok"] is True


def test_g1_an_s3_run_is_acceptance_by_default(gh, capsys):
    code, out = read(gh, capsys)
    assert code == 0 and out["ok"] is True


@pytest.mark.parametrize("scope", ["DIAGNOSTIC_SUBSET", "N1_ONLY_TEST_ONLY"])
def test_g1_diagnostic_and_test_only_scopes_are_never_acceptance(gh, capsys, scope):
    gh["artifact"] = {"scope": scope}
    for extra in ([], ["--expect-scope", "S2_DIAGNOSTIC_SUPERVISION"]):
        code, out = read(gh, capsys, *extra)
        assert code != 0 and out.get("ok") is not True
        gh["dest"] = gh["dest"].with_name(gh["dest"].name + "x")


def test_g1_evaluate_defaults_to_the_s3_scope(tmp_path):
    write_artifact(tmp_path, scope="S2_DIAGNOSTIC_SUPERVISION", required=15, tests=15)
    assert evidence.evaluate(tmp_path)[0] is False
    assert evidence.evaluate(tmp_path, expect_scope="S2_DIAGNOSTIC_SUPERVISION")[0] is True


# --- G2: the node set is non-empty and every required node ran ----------------------

@pytest.mark.parametrize("required,tests", [(0, 19), (19, 18)])
def test_g2_an_empty_or_short_run_is_not_acceptance(gh, capsys, required, tests):
    gh["artifact"] = {"required": required, "tests": tests}
    code, out = read(gh, capsys)
    assert code != 0 and out["ok"] is False


# --- G3: the bytes the host measured are the bytes claimed ---------------------------

def test_g3_a_dispatch_run_must_have_measured_its_head(gh, capsys):
    gh["artifact"] = {"tested": MERGE}
    code, out = read(gh, capsys)
    assert code != 0 and out["ok"] is False
    assert MERGE in json.dumps(out)


def test_g3_a_record_without_a_measured_commit_is_not_acceptance(gh, capsys):
    gh["artifact"] = {"tested": None}
    code, out = read(gh, capsys)
    assert code != 0 and out["ok"] is False


def test_g3_a_pull_request_run_reports_that_it_tested_a_merge_commit(gh, capsys):
    gh["head"]["event"] = "pull_request"
    gh["artifact"] = {"tested": MERGE}
    code, out = read(gh, capsys)
    assert code == 0 and out["ok"] is True
    assert out["facts"]["tested_commit"] == MERGE
    assert out["facts"]["tested_commit_kind"] == "pull_request_merge"


def test_g3_the_dispatch_run_reports_its_tested_commit(gh, capsys):
    code, out = read(gh, capsys)
    assert out["facts"]["tested_commit"] == HEAD
    assert out["facts"]["tested_commit_kind"] == "head"


def test_g3_run_head_asks_gh_for_the_event(monkeypatch):
    seen = {}

    def fake_run(cmd, **kwargs):
        seen["cmd"] = cmd
        return subprocess.CompletedProcess(cmd, 0, stdout=json.dumps({"headSha": HEAD, "event": "push"}), stderr="")
    monkeypatch.setattr(evidence.subprocess, "run", fake_run)
    evidence.run_head("1")
    fields = seen["cmd"][seen["cmd"].index("--json") + 1].split(",")
    assert "event" in fields and "headSha" in fields


# --- G4: --expect-head is a real hex prefix, compared case-insensitively ------------

@pytest.mark.parametrize("value", ["", "a", "abcdef", "zzzzzzz", HEAD + "0"])
def test_g4_malformed_expect_head_is_refused_before_any_gh_call(gh, capsys, value):
    with pytest.raises(SystemExit) as exc:
        evidence.main(["35800000000", "--dest", str(gh["dest"]), "--expect-head", value])
    assert exc.value.code != 0
    assert gh["calls"] == []


@pytest.mark.parametrize("value", [HEAD[:7], HEAD, HEAD.upper(), HEAD[:12].upper()])
def test_g4_a_matching_prefix_in_any_case_is_accepted(gh, capsys, value):
    code, out = read(gh, capsys, "--expect-head", value)
    assert code == 0 and out["ok"] is True


def test_g4_a_different_head_is_refused(gh, capsys):
    code, _ = read(gh, capsys, "--expect-head", "bbbbbbb")
    assert code != 0


# --- G5: --cases is validated before anything runs ----------------------------------

def boundary():
    return importlib.import_module("scripts.qualification_boundary_verification")


@pytest.fixture
def linux_root(monkeypatch):
    module = boundary()
    monkeypatch.setattr(module.platform, "system", lambda: "Linux")
    monkeypatch.setattr(module.os, "geteuid", lambda: 0, raising=False)
    return module


@pytest.mark.parametrize("argv", [
    ["--host-only", "--cases", "downtime"],
    ["--s2", "--cases", "downtime"],
    ["--test-only", "--cases", "downtime"],
    ["--s3", "--cases", "   "],
    ["--s3", "--cases", "\t"],
    ["--s3", "--cases", "alpha or ("],
    ["--s3", "--cases", "and"],
])
def test_g5_invalid_cases_are_refused_before_the_manifest_is_read(linux_root, capsys, argv):
    assert linux_root.main(argv) == 2
    err = capsys.readouterr().err
    assert "--cases" in err and "--manifest" not in err


def test_g5_a_valid_expression_proceeds_to_the_next_prerequisite(linux_root, capsys):
    assert linux_root.main(["--s3", "--cases", "downtime or (deadline and not oom)"]) == 2
    assert "--manifest" in capsys.readouterr().err


# --- G6: the workflow refuses bad inputs before provisioning ------------------------

def _steps():
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))["jobs"]["s2-supervision"]["steps"]


def test_g6_inputs_are_validated_before_the_host_is_provisioned():
    names = [s.get("name", s.get("uses", "")) for s in _steps()]
    assert "Validate inputs" in names
    assert names.index("Validate inputs") < names.index("Provision protected TEST_ONLY host")


@pytest.mark.parametrize("mode,cases,ok", [
    ("s3", "", True), ("s2", "", True), ("s3", "downtime or deadline", True),
    ("s3", "   ", False), ("s3", "\t", False), ("s2", "downtime", False), ("s4", "", False),
])
def test_g6_the_validation_step_accepts_exactly_the_runnable_inputs(tmp_path, shell, mode, cases, ok):
    step = next(s for s in _steps() if s.get("name") == "Validate inputs")
    env = {k: v for k, v in step.get("env", {}).items()}
    assert set(env) >= {"BOUNDARY_MODE", "BOUNDARY_CASES"}, "inputs must reach the script through env"
    assert "${{" not in step["run"], "inputs are never interpolated into the script"
    script = tmp_path / "validate.sh"
    script.write_text(step["run"], encoding="utf-8")
    result = subprocess.run([shell, str(script)], env=dict(os.environ, BOUNDARY_MODE=mode, BOUNDARY_CASES=cases),
                            capture_output=True, text=True, check=False, timeout=30)
    assert (result.returncode == 0) is ok, result.stdout + result.stderr


# --- G7: the pull_request path filter covers what the run depends on ----------------

def _matches(pattern, path):
    regex = re.escape(pattern).replace(r"\*\*", "\0").replace(r"\*", "[^/]*").replace("\0", ".*")
    return re.fullmatch(regex, path) is not None


@pytest.mark.parametrize("path", [
    "scripts/pytest_qualification_collection.py",
    "tools/local_verification/requirements-extra.txt",
    "scripts/fp.py",
    "pyproject.toml",
    "tests/conftest.py",
    "core/lib/file_lock.py",
    "ops/c1_rail/book_policy.py",
    "ops/c1_rail/book_schedule.py",
    "ops/c1_rail/policy_fingerprint.py",
])
def test_g7_pull_requests_touching_run_inputs_fire_the_workflow(path):
    assert (ROOT / path).exists(), path
    patterns = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))[True]["pull_request"]["paths"]
    assert any(_matches(p, path) for p in patterns), path


# --- G8: the skill and README name the dispatch run and the real facts ---------------

@pytest.mark.parametrize("doc", [SKILL, README])
def test_g8_the_dispatch_lookup_cannot_return_a_pull_request_run(doc):
    text = doc.read_text(encoding="utf-8")
    lookups = [line for line in text.splitlines() if "gh run list" in line and "qualification-s2-supervision" in line]
    assert lookups, doc
    for line in lookups:
        assert "--event workflow_dispatch" in line and "--commit" in line, line
        assert "--limit 1" not in line, line


@pytest.mark.parametrize("doc", [SKILL, README])
def test_g8_docs_name_the_default_s3_selection_and_the_real_invariant_key(doc):
    text = doc.read_text(encoding="utf-8")
    assert "S3_CASES" in text, doc
    assert "required_nodeids" in text, doc
    assert "`required` = every registered node" not in text, doc


def test_g8_docs_say_a_diagnostic_run_always_ends_red():
    for doc in (SKILL, README):
        lines = doc.read_text(encoding="utf-8").lower().splitlines()
        assert any("diagnostic" in line and "always" in line and ("red" in line or "fail" in line)
                   for line in lines), doc
