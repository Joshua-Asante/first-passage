"""Static checks on the S2 supervision workflow's r1 dispatch mode (H9 checkpoint R1).

The `r1` mode reaches the workflow only through the coordinator's
Joshua-approved patch (2026-10-02-r1-tooling-build-card.md, SS4 G8 and SS5):
dispatch-only, the default stays `s4`, `timeout-minutes` is 180 (D4), and
`cases` stays a diagnostic subset that accepts it. This test reads the
workflow bytes, so it passes only where that patch is applied; it never
dispatches anything and claims no Linux evidence.
"""
from pathlib import Path

import yaml

WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/qualification-s2-supervision.yml"


def _workflow():
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


def _mode_input(workflow):
    # YAML 1.1 parses a bare `on:` key as boolean True.
    triggers = workflow[True] if True in workflow else workflow["on"]
    return triggers["workflow_dispatch"]["inputs"]["mode"]


def _job(workflow):
    return workflow["jobs"]["s2-supervision"]


def test_mode_options_gain_r1_and_default_stays_s4():
    mode = _mode_input(_workflow())
    assert mode["type"] == "choice"
    assert mode["options"] == ["s2", "s3", "s4", "s5", "r1"]
    assert mode["default"] == "s4"  # r1 is dispatch-only, never the default
    assert "r1" in mode["description"]


def test_timeout_minutes_is_180():
    assert _job(_workflow())["timeout-minutes"] == 180  # D4: the ~90 min s5 run 36936558798 plus files 5 and 6


def test_both_mode_case_lists_accept_r1():
    text = WORKFLOW.read_text(encoding="utf-8")
    shell_steps = [step["run"] for step in _job(_workflow())["steps"] if "run" in step]
    mode_gates = [run for run in shell_steps if 'case "$mode" in' in run]
    assert len(mode_gates) == 2  # Validate inputs + Doctor and targeted boundary run
    for run in mode_gates:
        assert 'case "$mode" in s2|s3|s4|s5|r1)' in run
        assert "expected s2, s3, s4, s5 or r1" in run
    assert text.count('case "$mode" in s2|s3|s4|s5|r1)') == 2
    assert 'case "$mode" in s2|s3|s4|s5)' not in text  # no gate left refusing r1


def test_cases_diagnostic_subset_allows_r1():
    shell = "\n".join(step["run"] for step in _job(_workflow())["steps"] if "run" in step)
    assert '[ "$mode" != "r1" ]' in shell
    assert "cases is a diagnostic subset for mode s3, s4, s5 or r1 only" in shell


def test_the_patch_changes_no_trigger_permission_runner_or_artifact():
    workflow = _workflow()
    triggers = workflow[True] if True in workflow else workflow["on"]
    assert set(triggers) == {"workflow_dispatch", "pull_request"}
    assert workflow["permissions"] == {"contents": "read"}
    job = _job(workflow)
    assert job["runs-on"] == "ubuntu-24.04"
    artifact = next(step for step in job["steps"]
                    if step.get("name") == "Retain S2 invariant evidence (no keys or private manifest)")
    assert artifact["with"]["name"] == "qualification-s2-supervision"
    assert artifact["with"]["retention-days"] == 14
