# Repeatable local verification execution record

Implemented on `codex/verification-reliability`, independently from configuration
PR 418, starting at main `6a3d4b37c9ce24e3726765d01a6804cae1976f59`.
The original checkout and configuration worktree were preserved. No deployment,
skill publication, live shared-hook installation or merge occurred.

## Disposition

| Packet | Result | Boundary preserved |
| --- | --- | --- |
| Subtest evidence | Complete: local and Docker entrypoints load a pinned pytest producer adapter; each subtest has a distinct XML identity and lifetime. Serial/xdist regressions exercise both APIs, repeated labels, pass/fail/skip, parent/teardown failures, captures and unchanged reports for other consumers. | Strict recorder is unchanged; malformed/mismatched reports still fail. |
| Test storage | Complete: opt-in temporary HOME/USERPROFILE/cache for agent-handoff and image fault-injection suites. Real child receipts are verified outside worker workspaces. | Production receipt/cache selection, locking and worker cleanup are unchanged. |
| Git hooks | Complete: all four versioned templates route consumers through the validated checkout launcher; invalid environments prevent consumers, with an advisory warning for post-merge. Both installers and LF checkout behavior are covered. | Existing checker arguments and blocking/advisory semantics remain; shared installed hooks are not overwritten. |

Isolation exposed two stale descendant-test workers with a hardcoded session ID.
Both now echo the requested session ID, allowing their original Windows/POSIX
cleanup assertions to run. Production process handling did not change.

Independent read-only review found a serial Docker argument-indentation error and
duplicated skip captures. Regressions reproduced both; fixes passed re-review
with no outstanding actionable findings. No checks were weakened or removed.

## Environment and evidence

Checkout: `C:/Users/joshu/multi_firm_operations/.worktrees/verification-reliability`.
PowerShell 7.6.6; Windows operations Python 3.13.2 at
`C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`; doctor
validated all 62 locked packages. Linux verification used the existing local
Docker image with Python 3.11.16; exact image/package metadata is in each record.
All project Python commands used this checkout's launcher. Docker used its
documented PowerShell entrypoint, source mounted read-only and networking off.

Record paths below are relative to this checkout. Each directory retains raw
stdout/stderr, source fingerprints and artifact hashes. Accepted runs have
`status=completed`, `verification_exit_code=0`, `source_stable=true`,
`capture_complete=true` and no report errors; Docker also has `cleanup.ok=true`.
Source and Git state stayed fixed throughout each run. Runtime code and tests
were unchanged after the full run; subsequent edits only completed this ledger
and the implementation plan.

Full-run source fingerprint:
`6afe100b03e76bc3f8dcfc55011001b4124ebff8ab90d0bfdeb1db732c51156e`.

| Command / purpose | Result | Record directory (append `/record.json`) |
| --- | --- | --- |
| `fp.ps1 --workers 2 test -q` | **6048 passed, 70 skipped, 48 subtests passed**, 25 warnings, 892.97s. Strict XML: 6166 total, 6096 passed, 70 skipped; zero failures/errors. | `.cache/fp-verification/20260917T155907Z-0a9ca25b637d` |
| `fp.ps1 --workers 2 python -m pytest` with the seven affected files listed below, `-q` | 161 passed, 8 skipped | `.cache/fp-verification/20260917T155455Z-b8a0aab79830` |
| `fp.ps1 check` | All gates exit zero; embedded evidence-store suite: 72 tests, 3 skipped | `.cache/fp-verification/20260917T155648Z-744b7ac3a6b0` |
| Docker serial: beliefs, reporter, agent-handoff and hooks | 110 passed, 3 skipped, 6 subtests passed | `.cache/fp-docker-verification/20260917T155538Z-0b3669c6b01f` |
| Docker two workers: beliefs, reporter and book-account owner | 40 passed, 6 subtests passed; JUnit and coverage JSON retained | `.cache/fp-docker-verification/20260917T155922Z-4c66ea13f1fb` |
| Docker serial: beliefs and book-account owner | 32 passed, 6 subtests passed; JUnit and coverage JSON retained | `.cache/fp-docker-verification/20260917T160111Z-67903131ea04` |

Affected files: `tests/test_fp_launcher.py`, `tests/test_record_verification.py`,
`tests/test_pytest_junit_subtests.py`, `tests/test_docker_verification.py`,
`tests/test_git_hooks.py`, `tests/test_agent_handoff.py`,
`tests/scripts/test_c1_image_validation.py`.

Docker commands use `tools/local_verification/run.ps1 -Workers 0` or `2`, with
`-TestPath` arrays of `tests/evidence_store/test_beliefs.py`,
`tests/test_pytest_junit_subtests.py`, `tests/test_agent_handoff.py`,
`tests/test_git_hooks.py`, and/or `tests/ops/test_book_account_owner.py` as selected
in the table. The initial serial selection exercises no configured coverage
target and retains no coverage JSON; its coverage warnings are disclosed and
are not coverage evidence. The subsequent serial and parallel runs qualify that
artifact path using actual book-owner tests.

Gate advisories include absent private Pine/data artifacts and historical-source
notices. Passing gates do not validate absent artifacts. Full-suite warnings
include existing deprecations, historical scoring notices and optional sklearn
fallback. Platform/optional integration skips remain visible in the reports.

## Failure history

Under `.cache/fp-verification/` (append `/record.json`):

- `20260917T153650Z-c3955484625d`: baseline selected run, 40 passed/2 failed;
  reproduced restricted-home failures before isolation.
- `20260917T153857Z-671b60721fe9`: passing-subtest regression, 2 failed;
  child pytest succeeded but strict verification rejected inconsistent XML.
- `20260917T154432Z-583a80b5e9df`: isolated suites, 85 passed/6 skipped/1 failed;
  exposed the stale Windows session fixture. The corrected targeted tests passed
  in `20260917T154715Z-9c502ee0f4be`.
- `20260917T154815Z-dc5fb081af5a`: hook regressions, 14 failed/3 passed before
  launcher routing/LF fixes; 17 passed in `20260917T155002Z-c52a7a6719ca`.
- `20260917T155406Z-4e09bc453a5a`: review regressions, 5 failed/5 passed before
  serial-Docker and duplicate-capture fixes; the final focused/full runs pass.

Earlier development failures remain in their original records; none is rewritten
as acceptance. PR 418's historical evidence is unchanged.

## Activation and accounting

Refresh installed hooks only when active linked checkouts contain the launcher
and a valid operations environment; the common Git hook directory is shared.
Disposable repositories establish installer behavior without breaking older
active checkouts. The pytest adapter uses private APIs of locked pytest 9.1.1;
its process regressions must accompany a pytest upgrade.

Exact byte accounting compares base Git blobs with final Git-clean bytes,
including all new tests and both documents, and verifies normalization against
`git hash-object --path`. Per-file measurements are retained in
`.cache/verification-byte-accounting.json`. Final totals are recorded below.

Net change: **+35219 bytes**, comprising implementation **+3233**, tests
**+14767**, and documentation **+17219**. This follow-up adds verification
capability and regression evidence; it is not a byte-reduction claim.
