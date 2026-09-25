"""s2_run_evidence.py — read a qualification S2 workflow run's artifact as evidence.

A green check on the `qualification-s2-supervision` workflow is not evidence;
the uploaded artifact is. This prints the facts an executor or coordinator must
cite for a run and exits non-zero unless every one of them holds:

  record.json     status=completed, exit_code=0, verification_exit_code=0,
                  source_stable=true, capture_complete=true, cleanup.ok=true,
                  metadata.acceptance_scope equal to --expect-scope, and a
                  measured before.commit (the host's `git rev-parse HEAD`)
  invariants.json passed=true, and required_nodeids (the selection's required
                  nodes) is a non-empty list bound to the expected scope's exact
                  file set: every nodeid starts with '<file>::' for a file of
                  that set, and every file of the set contributes at least one
                  nodeid
  junit.xml       tests >= len(required_nodeids), failures=0, errors=0, skipped=0
  the run         for a workflow_dispatch (any event but pull_request) run, the
                  measured commit equals the run's headSha

Usage (from any checkout with `gh` authenticated):

    python scripts/s2_run_evidence.py <run-id> [--dest DIR] [--expect-head SHA]
        [--expect-scope {S4_JOINT_N2,S3_N1_CAPTURE,S2_DIAGNOSTIC_SUPERVISION}]

`--expect-scope` names the one scope that can read ok. The default is
S4_JOINT_N2, the workflow's new default `s4` mode and its acceptance-grade joint
set; S3_N1_CAPTURE (an `s3` run) and S2_DIAGNOSTIC_SUPERVISION (an `s2` run)
read ok only when asked for explicitly. Each scope is also bound to its exact
file set (S4_JOINT_N2 -> S4_CASES, S3_N1_CAPTURE -> S3_CASES,
S2_DIAGNOSTIC_SUPERVISION -> S2_CASES, the tuples the selector defines), so a
required-node list that misses a file of that set, or carries a node from any
other file, is refused. DIAGNOSTIC_SUBSET (a `cases` run) and N1_ONLY_TEST_ONLY
are never ok.

`--expect-head` refuses a run whose head is not the bytes you are claiming for:
7 to 40 hexadecimal characters, compared case-insensitively as a prefix of the
run's headSha. Anything else is refused while parsing arguments, before any gh call.

`facts.tested_commit` is the record's `before.commit`, the commit the host
measured. `facts.tested_commit_kind` says what it is:
  head                a workflow_dispatch (or any non-pull_request) run tested
                      the run's head; tested_commit must equal headSha.
  pull_request_merge  a pull_request run checked out refs/pull/N/merge, so it
                      tested a merge commit, never the head's bytes alone; the
                      commit is printed but not bound to headSha.

The artifact is downloaded into DIR (default: a temp dir) with `gh run download`;
nothing is written into the repository. Pure read; no acceptance decision.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# `python scripts/s2_run_evidence.py` puts only scripts/ on sys.path, and the
# selector that owns each scope's file set lives one level up.
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.qualification_boundary_verification import S2_CASES, S3_CASES, S4_CASES

ARTIFACT = "qualification-s2-supervision"
# The only scopes whose green can be read as boundary evidence, default first.
# A diagnostic subset (the workflow's `cases` input) records DIAGNOSTIC_SUBSET
# and --test-only records N1_ONLY_TEST_ONLY; neither can ever be requested.
ACCEPTANCE_SCOPES = ("S4_JOINT_N2", "S3_N1_CAPTURE", "S2_DIAGNOSTIC_SUPERVISION")
DEFAULT_SCOPE = ACCEPTANCE_SCOPES[0]
# Each acceptance scope reads ok only for its own file set (C2 ruling 1): the
# selector's tuples, imported rather than duplicated, so the reader cannot drift
# from the selection it is asked to accept.
SCOPE_FILES = {
    "S4_JOINT_N2": S4_CASES,
    "S3_N1_CAPTURE": S3_CASES,
    "S2_DIAGNOSTIC_SUPERVISION": S2_CASES,
}
RUN_FIELDS = "headSha,headBranch,event,conclusion,status,createdAt"
HEAD_PREFIX = re.compile(r"[0-9a-fA-F]{7,40}")
# `git rev-parse HEAD`: a full SHA-1 or SHA-256 object name.
COMMIT = re.compile(r"[0-9a-fA-F]{40}|[0-9a-fA-F]{64}")


def run_head(run_id: str) -> dict:
    """Return the run's head, event and state from `gh run view`."""
    out = subprocess.run(
        ["gh", "run", "view", run_id, "--json", RUN_FIELDS],
        check=True, capture_output=True, text=True,
    ).stdout
    return json.loads(out)


def download(run_id: str, dest: Path) -> None:
    """Download the run's evidence artifact into `dest`."""
    subprocess.run(["gh", "run", "download", run_id, "-n", ARTIFACT, "-D", str(dest)],
                   check=True, capture_output=True, text=True)


def junit_totals(path: Path) -> dict:
    """Sum the tests/failures/errors/skipped attributes over every testsuite."""
    root = ET.parse(path).getroot()
    suites = root.findall(".//testsuite") if root.tag != "testsuite" else [root]
    return {k: sum(int(s.get(k, 0)) for s in suites)
            for k in ("tests", "failures", "errors", "skipped")}


def expect_head_prefix(value: str) -> str:
    """argparse type for --expect-head: 7-40 hex characters, returned lowercase."""
    if HEAD_PREFIX.fullmatch(value) is None:
        raise argparse.ArgumentTypeError(
            f"must be 7 to 40 hexadecimal characters (a commit prefix), got {value!r}")
    return value.lower()


def _is_zero(value) -> bool:
    """An exit code of exactly integer 0 (a JSON `false` is not 0)."""
    return isinstance(value, int) and not isinstance(value, bool) and value == 0


def _tested_commit(record: dict):
    """The record's `before.commit` (the host's `git rev-parse HEAD`), or None."""
    before = record.get("before")
    commit = before.get("commit") if isinstance(before, dict) else None
    return commit if isinstance(commit, str) else None


def _bind_commit(facts: dict, head: dict | None) -> list[str]:
    """Set tested_commit_kind from the run's event; return the binding refusals."""
    tested = facts["tested_commit"]
    if tested is None or COMMIT.fullmatch(tested) is None:
        facts["tested_commit_kind"] = None
        return [f"record.before.commit is missing or not a full commit id ({tested!r}): "
                "the bytes the host measured are unknown"]
    if head is None:
        # A bare artifact read (no run): the commit is reported, not bound.
        facts["tested_commit_kind"] = None
        return []
    if head.get("event") == "pull_request":
        facts["tested_commit_kind"] = "pull_request_merge"
        return []
    facts["tested_commit_kind"] = "head"
    head_sha = head.get("headSha")
    if not isinstance(head_sha, str) or tested.lower() != head_sha.lower():
        return [f"the host measured {tested} but the run's headSha is {head_sha}"]
    return []


def _file_set_refusals(scope: str, required: list[str]) -> list[str]:
    """Why `required` is not exactly the scope's file set (empty when it is).

    Every required nodeid must start with '<file>::' for a file of the scope's
    set, and every file of that set must contribute at least one nodeid, so a
    19-node S3 record cannot read as S4 (the N2 file is missing) and a 22-node
    S4 record cannot read as S3 (the N2 file is foreign).
    """
    files = SCOPE_FILES[scope]
    prefixes = tuple(path + "::" for path in files)
    refusals = [f"required nodes do not match the {scope} file set: missing {path}"
                for path, prefix in zip(files, prefixes)
                if not any(node.startswith(prefix) for node in required)]
    foreign = []
    for node in required:
        path = node.split("::", 1)[0]
        if not node.startswith(prefixes) and path not in foreign:
            foreign.append(path)
    refusals += [f"required nodes do not match the {scope} file set: foreign {path}"
                 for path in foreign]
    return refusals


def evaluate(dest: Path, *, expect_scope: str = DEFAULT_SCOPE,
             head: dict | None = None) -> tuple[bool, dict]:
    """Read one downloaded artifact; return (ok, facts).

    `head` is the run as `run_head` returns it. With it, a non-pull_request run
    must have measured its headSha; without it the measured commit is required
    and reported but not bound to a run.
    """
    if expect_scope not in ACCEPTANCE_SCOPES:
        raise ValueError(f"expect_scope must be one of {ACCEPTANCE_SCOPES}, got {expect_scope!r}")
    records = list(dest.glob("*/record.json"))
    if len(records) != 1:
        return False, {"error": f"expected exactly one record.json under {dest}, "
                                f"found {len(records)}",
                       "expected_scope": expect_scope}
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
        "acceptance_scope": (record.get("metadata") or {}).get("acceptance_scope"),
        "expected_scope": expect_scope,
        "tested_commit": _tested_commit(record),
    }
    inv_path = record_dir / "invariants.json"
    required = None
    if inv_path.exists():
        inv = json.loads(inv_path.read_text(encoding="utf-8"))
        required = inv.get("required_nodeids")
        facts["invariants_passed"] = inv.get("passed")
    else:
        facts["invariants_passed"] = None
    valid_required = isinstance(required, list) and all(isinstance(node, str) for node in required)
    facts["required_nodes"] = len(required) if valid_required else None
    junit_path = record_dir / "junit.xml"
    junit = facts["junit"] = junit_totals(junit_path) if junit_path.exists() else None

    refusals = [message for held, message in (
        (facts["acceptance_scope"] == expect_scope,
         f"acceptance_scope is {facts['acceptance_scope']!r}, expected {expect_scope}"),
        (facts["status"] == "completed", "record status is not completed"),
        (_is_zero(facts["exit_code"]) and _is_zero(facts["verification_exit_code"]),
         "record exit_code/verification_exit_code is not 0"),
        (facts["source_stable"] is True, "source_stable is not true"),
        (facts["capture_complete"] is True, "capture_complete is not true"),
        (facts["cleanup_ok"] is True, "cleanup.ok is not true"),
        (facts["invariants_passed"] is True, "invariants.json passed is not true"),
        (bool(facts["required_nodes"]), "invariants.json required_nodeids is missing or empty"),
        (junit is not None, "junit.xml is missing"),
    ) if not held]
    if junit is not None:
        if facts["required_nodes"] and junit["tests"] < facts["required_nodes"]:
            refusals.append(f"junit ran {junit['tests']} tests, fewer than the "
                            f"{facts['required_nodes']} required nodes")
        refusals += [f"junit {key}={junit[key]}"
                     for key in ("failures", "errors", "skipped") if junit[key] != 0]
    if valid_required and required:
        refusals += _file_set_refusals(expect_scope, required)
    refusals += _bind_commit(facts, head)
    facts["refusals"] = refusals
    return not refusals, facts


def main(argv: list[str] | None = None) -> int:
    """Read one run's artifact; print the facts; exit 0 only when every one holds."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", maxsplit=1)[0])
    parser.add_argument("run_id")
    parser.add_argument("--dest", type=Path, help="download directory (default: temp)")
    parser.add_argument("--expect-head", type=expect_head_prefix,
                        help="refuse unless the run's headSha starts with this "
                             "7-40 hex prefix (any case)")
    parser.add_argument("--expect-scope", choices=ACCEPTANCE_SCOPES, default=DEFAULT_SCOPE,
                        help="the only record scope that reads ok, and the file set its "
                             "required nodes must cover exactly (default: %(default)s)")
    args = parser.parse_args(argv)
    head = run_head(args.run_id)
    head_sha = head.get("headSha") if isinstance(head.get("headSha"), str) else ""
    if args.expect_head is not None and not head_sha.lower().startswith(args.expect_head):
        print(json.dumps({"ok": False, "run": head, "expected_head": args.expect_head,
                          "error": "run head differs from the claimed bytes"}, indent=2))
        return 2
    dest = args.dest or Path(tempfile.mkdtemp(prefix=f"s2-{args.run_id}-"))
    download(args.run_id, dest)
    ok, facts = evaluate(dest, expect_scope=args.expect_scope, head=head)
    print(json.dumps({"ok": ok, "run": head, "artifact_dir": str(dest), "facts": facts}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
