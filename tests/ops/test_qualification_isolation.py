"""Full-suite bridge; retain the clean child's source-inventory test evidence."""
import hashlib
from collections import Counter
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from uuid import uuid4
import xml.etree.ElementTree as ET

import pytest


_SIGNED_CASES = {
    "test_historical_composition_preserves_replay_but_cannot_issue_authority",
    "test_real_composition_receipt_failure_survives_reopen_without_another_dispatch",
    "test_signed_composition_rejects_retained_bytes_and_import_alias_substitution",
    "test_independently_signed_composition_domains_cannot_be_crosswired",
    "test_signed_approval_expiry_preserves_completed_n1_without_later_dispatch",
    "test_preflight_refuses_replacement_enrolled_key_bytes_before_reserving_root",
}

_PROVENANCE_CASES = {
    "test_effective_inputs_are_parsed_from_the_verified_bytes": 1,
    "test_result_authentication_rejects_receipt_fields_changed_after_validation": 4,
    "test_authenticated_consumers_recheck_canonical_receipt_fields": 8,
}

# The former single child (tests/ops/qualification plus the provenance file)
# split by directory into two clean children: every file outside execution/
# lands in "core", so the union stays the whole selection as files are added.
# Each shard asserts the signed/provenance evidence its own selection holds.
_EXECUTION = "tests/ops/qualification/execution"
_SHARDS = {
    "execution": ([_EXECUTION], set(), {}),
    "core": (["tests/ops/qualification", "--ignore=" + _EXECUTION,
              "tests/ops/test_phase3_provenance_acceptance.py"],
             _SIGNED_CASES, _PROVENANCE_CASES),
}


@pytest.mark.parametrize("shard", sorted(_SHARDS))
def test_qualification_suite_in_clean_process(shard, request, record_property):
    """Legacy flat imports must not contaminate signed canonical inventories."""
    selection, signed_cases, provenance_cases = _SHARDS[shard]
    repository = Path(__file__).resolve().parents[2]
    parent_report = getattr(request.config.option, "xmlpath", None)
    report_root = (Path(parent_report).resolve().parent if parent_report else
                   repository / ".cache" / "fp-verification")
    retained = report_root / (f"qualification-child-{shard}-" + uuid4().hex)
    retained.mkdir(parents=True)
    report = retained / "junit.xml"
    output = retained / "output.log"
    record_property("qualification_child_junit", str(report))
    record_property("qualification_child_output", str(output))
    command = [sys.executable, "-m", "pytest", *selection,
               "-n", "0", "--junitxml=" + str(report)]
    environment = os.environ.copy()
    # The selected interpreter/environment is inherited from the launcher.
    # Parent selection/worker options must not filter or distribute this child.
    for name in ("PYTEST_ADDOPTS", "PYTEST_XDIST_WORKER",
                 "PYTEST_XDIST_WORKER_COUNT", "PYTEST_XDIST_TESTRUNUID"):
        environment.pop(name, None)
    failure = None
    # Generated source fixtures must stay outside the checkout: source gates
    # deliberately inspect Python files even when Git ignores their directory.
    # Each child is a serial run of its shard, so its timeout is a hang bound,
    # not a performance gate; runner variance alone must not fail this test.
    # The unsharded child's junit recorded 3,530 s of test time at 7e9bd50
    # (CI run 37233382687) and hit this cap at 84% after T00 P-A (#672) added
    # ~50 tests. Split, that run's test time is 1,917 s (execution) and
    # 1,613 s (core, before #672's test_screen_authority.py).
    child_timeout = 3600
    with tempfile.TemporaryDirectory(prefix="fp-qualification-") as scratch, output.open(
            "w", encoding="utf-8") as stream:
        command.append("--basetemp=" + str(Path(scratch) / "pytest"))
        record_property("qualification_child_command", repr(command))
        record_property("qualification_child_timeout_s", child_timeout)
        try:
            completed = subprocess.run(
                command, cwd=repository, env=environment, stdout=stream,
                stderr=subprocess.STDOUT, timeout=child_timeout, check=False)
            if completed.returncode:
                failure = f"child pytest exited {completed.returncode}"
        except (OSError, subprocess.TimeoutExpired) as exc:
            failure = str(exc)
            stream.write("\nQualification child did not complete: " + failure + "\n")
    record_property("qualification_child_output_sha256",
                    hashlib.sha256(output.read_bytes()).hexdigest())
    if report.is_file():
        raw = report.read_bytes()
        record_property("qualification_child_junit_sha256", hashlib.sha256(raw).hexdigest())
        try:
            cases = ET.fromstring(raw).findall(".//testcase")
            counts = {name: sum(case.find(name) is not None for case in cases)
                      for name in ("failure", "error", "skipped")}
            record_property("qualification_child_tests", len(cases))
            for name, count in counts.items():
                record_property("qualification_child_" + name, count)
            signed = [case for case in cases
                      if case.get("classname", "").endswith("test_composition_route")
                      and case.get("name") in signed_cases]
            provenance = [case for case in cases
                          if case.get("classname", "").endswith("test_phase3_provenance_acceptance")
                          and case.get("name", "").split("[", 1)[0] in provenance_cases]
            provenance_counts = Counter(case.get("name", "").split("[", 1)[0]
                                        for case in provenance)
            if (not cases or counts["failure"] or counts["error"]
                    or len(signed) != len(signed_cases)
                    or {case.get("name") for case in signed} != signed_cases
                    or dict(provenance_counts) != provenance_cases
                    or any(case.find("skipped") is not None for case in signed + provenance)):
                failure = failure or "child report lacks complete passing signed composition evidence"
        except ET.ParseError as exc:
            failure = failure or f"child JUnit is invalid: {exc}"
    else:
        failure = failure or "child JUnit report is missing"
    if failure:
        tail = output.read_text(encoding="utf-8", errors="replace")[-12000:]
        pytest.fail(f"{failure}\nRetained report: {report}\nOutput: {output}\n{tail}")
