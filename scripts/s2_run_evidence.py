"""s2_run_evidence.py — read a qualification S2 workflow run's artifact as evidence.

A green check on the `qualification-s2-supervision` workflow is not evidence;
the uploaded artifact is. This prints the facts an executor or coordinator must
cite for a run and exits non-zero unless every one of them holds:

  record.json     status=completed, exit_code=0, verification_exit_code=0,
                  source_stable=true, capture_complete=true, cleanup.ok=true
  invariants.json passed=true, and the required node set is reported
  junit.xml       failures=0, errors=0, skipped=0

Usage (from any checkout with `gh` authenticated):

    python scripts/s2_run_evidence.py <run-id> [--dest DIR] [--expect-head SHA]

`--expect-head` refuses a run whose head is not the bytes you are claiming for.
The artifact is downloaded into DIR (default: a temp dir) with `gh run download`;
nothing is written into the repository. Pure read; no acceptance decision.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ARTIFACT = "qualification-s2-supervision"


def run_head(run_id: str) -> dict:
    out = subprocess.run(
        ["gh", "run", "view", run_id, "--json", "headSha,headBranch,conclusion,status,createdAt"],
        check=True, capture_output=True, text=True,
    ).stdout
    return json.loads(out)


def download(run_id: str, dest: Path) -> None:
    subprocess.run(["gh", "run", "download", run_id, "-n", ARTIFACT, "-D", str(dest)],
                   check=True, capture_output=True, text=True)


def junit_totals(path: Path) -> dict:
    root = ET.parse(path).getroot()
    suites = root.findall(".//testsuite") if root.tag != "testsuite" else [root]
    return {k: sum(int(s.get(k, 0)) for s in suites) for k in ("tests", "failures", "errors", "skipped")}


def evaluate(dest: Path) -> tuple[bool, dict]:
    records = list(dest.glob("*/record.json"))
    if len(records) != 1:
        return False, {"error": f"expected exactly one record.json under {dest}, found {len(records)}"}
    record_dir = records[0].parent
    record = json.loads(records[0].read_text(encoding="utf-8"))
    facts = {
        "record_id": record_dir.name,
        "status": record.get("status"),
        "exit_code": record.get("exit_code"),
        "verification_exit_code": record.get("verification_exit_code"),
        "source_stable": record.get("source_stable"),
        "capture_complete": record.get("capture_complete"),
        "cleanup_ok": (record.get("cleanup") or {}).get("ok"),
        # The only scopes whose green can be read as boundary evidence; a
        # diagnostic subset (the workflow's `cases` input) names itself and is
        # refused below regardless of its outcome.
        "acceptance_scope": (record.get("metadata") or {}).get("acceptance_scope"),
    }
    inv_path = record_dir / "invariants.json"
    if inv_path.exists():
        inv = json.loads(inv_path.read_text(encoding="utf-8"))
        required = inv.get("required_nodeids", inv.get("required", []))
        facts["invariants_passed"] = inv.get("passed")
        facts["required_nodes"] = len(required) if isinstance(required, list) else required
    else:
        facts["invariants_passed"] = None
    junit_path = record_dir / "junit.xml"
    facts["junit"] = junit_totals(junit_path) if junit_path.exists() else None
    ok = (
        facts["acceptance_scope"] in ("S2_DIAGNOSTIC_SUPERVISION", "S3_N1_CAPTURE")
        and facts["status"] == "completed" and facts["exit_code"] == 0 and facts["verification_exit_code"] == 0
        and facts["source_stable"] is True and facts["capture_complete"] is True and facts["cleanup_ok"] is True
        and facts["invariants_passed"] is True and facts["junit"] is not None
        and facts["junit"]["failures"] == 0 and facts["junit"]["errors"] == 0 and facts["junit"]["skipped"] == 0
    )
    return ok, facts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("run_id")
    parser.add_argument("--dest", type=Path, help="download directory (default: temp)")
    parser.add_argument("--expect-head", help="refuse unless the run's headSha starts with this")
    args = parser.parse_args(argv)
    head = run_head(args.run_id)
    if args.expect_head and not head["headSha"].startswith(args.expect_head):
        print(json.dumps({"ok": False, "run": head, "error": "run head differs from the claimed bytes"}, indent=2))
        return 2
    dest = args.dest or Path(tempfile.mkdtemp(prefix=f"s2-{args.run_id}-"))
    download(args.run_id, dest)
    ok, facts = evaluate(dest)
    print(json.dumps({"ok": ok, "run": head, "artifact_dir": str(dest), "facts": facts}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
