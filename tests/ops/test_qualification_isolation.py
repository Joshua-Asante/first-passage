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
    "test_signed_composition_uses_real_source_dispatch_replay_and_g5_across_reopen",
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


def test_qualification_suite_in_clean_process(request, record_property):
    """Legacy flat imports must not contaminate signed canonical inventories."""
    repository = Path(__file__).resolve().parents[2]
    parent_report = getattr(request.config.option, "xmlpath", None)
    report_root = (Path(parent_report).resolve().parent if parent_report else
                   repository / ".cache" / "fp-verification")
    retained = report_root / ("qualification-child-" + uuid4().hex)
    retained.mkdir(parents=True)
    report = retained / "junit.xml"
    output = retained / "output.log"
    record_property("qualification_child_junit", str(report))
    record_property("qualification_child_output", str(output))
    command = [sys.executable, "-m", "pytest", "tests/ops/qualification",
               "tests/ops/test_phase3_provenance_acceptance.py",
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
    with tempfile.TemporaryDirectory(prefix="fp-qualification-") as scratch, output.open(
            "w", encoding="utf-8") as stream:
        command.append("--basetemp=" + str(Path(scratch) / "pytest"))
        record_property("qualification_child_command", repr(command))
        try:
            completed = subprocess.run(
                command, cwd=repository, env=environment, stdout=stream,
                stderr=subprocess.STDOUT, timeout=1800, check=False)
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
                      and case.get("name") in _SIGNED_CASES]
            provenance = [case for case in cases
                          if case.get("classname", "").endswith("test_phase3_provenance_acceptance")
                          and case.get("name", "").split("[", 1)[0] in _PROVENANCE_CASES]
            provenance_counts = Counter(case.get("name", "").split("[", 1)[0]
                                        for case in provenance)
            if (not cases or counts["failure"] or counts["error"]
                    or len(signed) != len(_SIGNED_CASES)
                    or {case.get("name") for case in signed} != _SIGNED_CASES
                    or dict(provenance_counts) != _PROVENANCE_CASES
                    or any(case.find("skipped") is not None for case in signed + provenance)):
                failure = failure or "child report lacks complete passing signed composition evidence"
        except ET.ParseError as exc:
            failure = failure or f"child JUnit is invalid: {exc}"
    else:
        failure = failure or "child JUnit report is missing"
    if failure:
        tail = output.read_text(encoding="utf-8", errors="replace")[-12000:]
        pytest.fail(f"{failure}\nRetained report: {report}\nOutput: {output}\n{tail}")
