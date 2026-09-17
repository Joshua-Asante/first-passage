# Repeatable Local Verification Implementation Plan

> **For agentic workers:** Execute with superpowers:executing-plans. Preserve the behavioral contract and integration owner. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** A restricted local run produces complete, strictly validated evidence without depending on writable real-home storage or an arbitrary hook interpreter.

**Architecture:** Repair JUnit at its pytest producer, retain the recorder unchanged, isolate only test-owned storage, and bootstrap versioned Git hooks through the checkout launcher. The coordinator owns end-to-end acceptance. These steps integrate into one observable outcome: reproducible recorded verification under the existing restricted environment.

**Tech Stack:** Python 3.11+, locked pytest 9.1.1 and xdist 3.8.0, PowerShell/POSIX hooks, existing operations launcher and Docker evidence runner.

**Spec:** Approved conversation design: separate follow-up to PR 418; consistent passing/failing/skipped subtest evidence; temporary test home/cache outside worker workspaces; validated hook interpreter with explicit environment failures. User authorized execution on 2026-09-17. Base is main `6a3d4b3`; PR 418 remains untouched.

## Global constraints

- Run the checkout's `fp.ps1 doctor` before Python; all Python tasks use its launcher.
- Keep source/Git state unchanged during recorded runs. Retain raw reports and actual results, including failures.
- Do not relax `record_verification.junit_summary`, drop subtests, or infer omitted successes from an aggregate count.
- Production agent receipt locations, locking, identity and worker-cleanup protection stay unchanged.
- Existing pre-commit, merge, push and advisory post-merge semantics stay unchanged. No installed shared hooks are silently replaced during development.
- Preserve original checkouts; no deployment, publication or merge. Avoid dependency upgrades and a second generic report format.

## Task 1: Complete JUnit outcomes

**Files:** new `scripts/pytest_junit_subtests.py`; `scripts/fp.py`; `scripts/docker_verification.py`; `tests/test_fp_launcher.py`; focused reporter tests; `scripts/README.md`.

The pinned producer counts each `SubtestReport` but keys XML reporters by the parent node ID. A pytest-only adapter subclasses the existing JUnit producer. It copies each subtest report, assigns an ordinal identity under its original node ID, sends it through the unchanged producer and finalizes that individual testcase. It does not mutate the report other consumers receive. Parent reports, setup/teardown, captures, properties, output destination and recorder validation retain their existing owners. Controller-only configuration replaces the JUnit plugin before reports arrive; xdist workers only transmit reports. Both recorded pytest entrypoints load the adapter explicitly.

- [x] Add process regressions using real launcher fixture checkouts. Literal expectation: a parent plus two passing subtests yields three XML testcase outcomes; serial and two-worker results agree. Test unittest and pytest-fixture subtests, repeated labels, failures, skips, mixed failures/skips, parent failure and teardown failure. Assert preserved failure details and unique subtest identities.
- [x] Observe the passing-subtest regression fail on base: pytest exit 0, verification exit 5, inconsistent XML counts.
- [x] Implement the scoped producer adapter; retain existing strict mismatch/contradiction rejection tests.
- [x] Load with `-p scripts.pytest_junit_subtests` from fixed checkout cwd in local and Docker recorded pytest commands; copy support into launcher fixture checkouts.
- [x] Run affected suites and a Docker subtest case. Example acceptance: `fp.ps1 --workers 2 python -m pytest tests/test_fp_launcher.py tests/test_record_verification.py tests/test_pytest_junit_subtests.py -q`.

```python
# Independently specified success case, not a count derived from the producer:
assert record['test_summary'] == {
    'collected': 3, 'passed': 3, 'failed': 0, 'errors': 0, 'skipped': 0,
}
assert record['report_errors'] == []
```

## Task 2: Isolated test home storage

**Files:** `tests/conftest.py`, `tests/test_agent_handoff.py`, `tests/scripts/test_c1_image_validation.py`, focused fixture regression if needed.

Only suites that exercise home-based receipts/pip caches opt into a temporary home fixture. It sets the child-visible home variables with pytest monkeypatch for that test and restores them afterward. The temporary home is a sibling of the worker workspace, never inside it. Production cache selection is unchanged. Git test identity/settings must remain fixture-owned rather than accidentally inheriting real-home configuration.

- [x] Reproduce one agent-handoff permission failure and one image fault-injection failure in the restricted sandbox.
- [x] Extend the receipt-boundary regression: actual child receipts resolve under the parent temporary home and remain outside the worker workspace. Pytest/launcher retain ownership of temporary-tree cleanup.
- [x] Opt only the affected process suites into the fixture; preserve all original state/lock/receipt and injected-Docker outcome assertions.
- [x] Run `fp.ps1 --workers 2 python -m pytest tests/test_agent_handoff.py tests/scripts/test_c1_image_validation.py -q` without escalation.

```python
assert not receipt_root.is_relative_to(worker_workspace)
assert receipt_root.is_relative_to(isolated_home)
```

## Task 3: Launcher-backed Git hooks

**Files:** `scripts/githooks/{pre-commit,pre-merge-commit,pre-push,post-merge}`, hook process tests and `scripts/README.md`; existing installers only if a necessary installation boundary changes.

Each hook bootstraps with `python -I scripts/fp.py python <existing script and args>`. The bootstrap uses stdlib, chooses/validates the configured operations interpreter, and only then launches the existing hook consumer from that checkout. Blocking hooks propagate failures; advisory post-merge visibly reports environment failure and does not pretend a consumer ran. Preserve stdin/arguments where used, spaces in checkout paths, and linked-worktree root discovery. Installer tests use disposable repositories, not the shared live hooks directory.

- [x] Exercise actual hook templates in disposable repositories with a launcher fixture and misleading ambient interpreter environment; assert selected interpreter and checkout cwd.
- [x] Exercise missing/mismatched environments: no consumer side effect; clear error; blocking hook nonzero, advisory hook warns.
- [x] Replace bare consumer invocations with launcher calls; keep policy and checker arguments unchanged.
- [x] Verify all four templates and their installer behavior, then standard `fp.ps1 check`.

```sh
python -I scripts/fp.py python scripts/gate_manifest.py --tier pre-commit || exit 1
```

## Integration and related-case review

The failure family comprises subtest reports sharing a parent identity, process tests sharing real-home storage, and hooks bypassing interpreter selection. Check serial/xdist; local/Docker recorder commands; pass/failure/skip/error; worker cleanup versus outside receipts; all four hook templates and installed copies. Do not expand into unrelated scanner or runtime changes.

- [x] Independent review of reporting integrity, isolation boundaries and hook failure behavior; resolve findings before completion.
- [x] Run the full restricted `fp.ps1 --workers 2 test -q` and standard check, with stable source and valid evidence records. Report skips and any remaining failures precisely.
- [x] Retain source revision/fingerprint, interpreter, commands, record paths and net byte delta in an execution record. Historical PR 418 evidence remains historical.

Execution results and retained evidence: [execution record](2026-09-17-verification-reliability-execution.md).
