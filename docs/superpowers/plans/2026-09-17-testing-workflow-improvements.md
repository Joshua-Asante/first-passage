# Testing Workflow Improvements Implementation Plan

> **For agentic workers:** Execute with superpowers:executing-plans; use superpowers:subagent-driven-development when bounded delegation is useful and authorized. Preserve the behavioral contract and integration owner. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make local test feedback faster and unambiguous without weakening revision-bound verification.

**Architecture:** Extend the existing operations launcher and verification recorder. Pin pytest configuration to the selected checkout, keep baseline execution separate from implementation, and expose bounded progress independently of final acceptance evidence.

**Tech Stack:** Existing Python >=3.11 operations environment, PowerShell wrapper, pytest/xdist, Git worktrees, JSON verification records.

**Spec:** The user's September 17 request to improve the testing environment and the requirements in this plan. Linux isolation is a separate deliverable in [the companion plan](2026-09-17-linux-isolation-test-environment.md).

## Global Constraints

- Planning only; this document does not authorize implementation or infrastructure changes.
- Follow AGENTS.md; run the selected checkout's launcher doctor before Python work.
- Preserve the existing requirement for completed records, zero verification exit status, stable source, complete capture, valid reports and confirmed owned cleanup where applicable.
- No production qualification, deployment, production credentials or changes to replay/statistical mechanics.
- Use canonical configuration sources; consumers must not duplicate suite selections or progress defaults.
- Do not edit an actively tested checkout, including its Git index or HEAD.
- This plan was grounded in read-only inspection of PR415-based launcher/recorder tooling in `.worktrees/qualification-execution-boundary`. Recheck the chosen implementation baseline: these tools may not yet be present on main.

## Ownership and sequence

The implementing coordinator owns combined acceptance. `fp.py` owns interpreter and checkout selection; pytest owns test execution; `RunRecord` owns evidence and acceptance. Progress displays have no authority to declare success.

Implement Tasks 1 and 2 first, then Task 3. The Linux companion can proceed independently. Do not interrupt or change the ongoing qualification implementation to adopt this plan.

### Task 1: Pytest always uses the selected checkout

**Outcome:** Launching an external scratch test or invoking the launcher from another directory cannot silently select a parent repository's configuration or import roots.

**Files:** Modify `scripts/fp.py`, `tests/test_fp_launcher.py`, `scripts/README.md`.

**Proposed interface:** Internal helper `pytest_configuration_args(root: Path, args: list[str]) -> list[str]`. All launcher pytest routes consume it.

- [ ] Add subprocess regression tests using the existing fixture checkout and launcher helpers. Give the parent and selected checkout different pytest configuration/import sentinels. Exercise `test`, `test-ops` and `python -m pytest`, including an absolute external test path and a foreign working directory.
- [ ] Define the behavior explicitly: inject `-c <checkout>/pyproject.toml` and `--rootdir=<checkout>`. Accept equivalent explicit options; reject conflicting ones before pytest starts. Recognize both split and equals forms. Keep deliberate `-o` options available and recorded.
- [ ] Preserve external scratch-test support, but record hashes of explicit external test files before and after execution. If those files change, reject acceptance. Label external supporting imports/data as outside the measured source inventory unless separately captured. Do not claim the entire scratch-test dependency closure is covered.
- [ ] Confirm expected failure against the existing launcher, implement the helper and record metadata, then rerun. An import/setup failure is not evidence that the new root-selection behavior works.

Core behavioral assertion, implemented in the subprocess test fixture:

```python
# Parent config imports PARENT; selected checkout config imports CHECKOUT.
# The external test asserts the imported sentinel equals CHECKOUT.
result = launch(checkout, '--env', ops_env, 'python', '-m', 'pytest', str(external_test), '-q')
assert result.returncode == 0
```

**Acceptance:** Correct sentinel imported, exact checkout/config paths recorded, conflicting options fail clearly, existing custom JUnit and worker behavior remain intact, modified external test bytes cannot earn a passing verification record.

### Task 2: Baseline testing no longer blocks implementation

**Outcome:** A baseline run measures a fixed revision in its own checkout while implementation proceeds elsewhere; neither result is misrepresented as testing the other tree.

**Files:** Modify `scripts/README.md` and `tools/local_verification/README.md`. Extend `tests/test_record_verification.py` only for behavior not already covered.

**Workflow:** Use existing Git worktrees and launchers; do not add a worktree manager or change default gate coverage.

- [ ] Document selecting and verifying the exact baseline commit, then creating a detached baseline worktree and a separate implementation worktree. Use native isolation tooling when available, otherwise Git. Use ignored project-local locations or an authorized external location.
- [ ] Run doctor in both checkouts. Share an environment only when each checkout's launcher validates its own lock. Never modify a shared environment during either run; use separate environments when dependency work is required.
- [ ] Start with the affected baseline selection. Run a broad baseline only when it resolves a concrete attribution question. Execute affected tests during development, then planned regressions and required gates on the final unchanged candidate.
- [ ] Verify with two temporary Git checkouts and a real child process: changes to the implementation tree do not invalidate a stable baseline record; changes to the baseline tree do invalidate its record. Preserve existing source-drift failure semantics.
- [ ] Document that baseline results are reusable only for their recorded inputs, revision and environment. They are never candidate acceptance evidence. Remove only owned baseline worktrees after their runs finish and evidence is retained.

Example sequence, after resolving the baseline commit and creating both worktrees:

```powershell
# Invoke each command from the named checkout, not from the parent repository.
.\fp.ps1 doctor
.\fp.ps1 --workers 2 python -m pytest tests/test_fp_launcher.py tests/test_record_verification.py -q --tb=short
```

**Acceptance:** Two actual overlapping runs retain distinct checkout/revision identities, candidate edits do not contaminate baseline evidence, and source mutation in the measured checkout still fails verification. Concurrency is optional when CPU/memory contention makes it slower.

### Task 3: Long runs report progress without inventing results

**Outcome:** A quiet test run displays elapsed time and observed activity every 30 seconds while keeping raw child output, exit propagation and final acceptance unchanged.

**Files:** Modify `scripts/record_verification.py`, `scripts/fp.py`, `tests/test_record_verification.py`; create `scripts/pytest_progress.py` and `tests/test_pytest_progress.py`; document in `scripts/README.md`.

**Proposed interfaces:** Recorder-owned progress interval default is 30 seconds. The launcher explicitly loads `scripts.pytest_progress` for its pytest subprocess and passes the unique evidence directory. The plugin writes bounded `progress.json` snapshots; the recorder reads them as advisory data. Missing plugin observations mean “test activity unavailable,” never “stuck” or “passed.”

- [ ] Write a real subprocess test with a quiet, deliberately waiting child; assert a heartbeat appears before child exit. Test nonzero child exit and interruption independently.
- [ ] Implement pytest hook reporting for collected count, completed node IDs, active node IDs, worker ID and observation time. Distinguish completed tests from passed tests and handle setup/teardown failures. Bound active-item display and metadata size.
- [ ] With xdist, write one atomic progress file per worker and let the controller aggregate distinct node IDs. Do not have multiple workers overwrite one shared snapshot. Final counts still come from validated JUnit.
- [ ] Exercise serial and two-worker runs with real tests that pass, fail, skip and wait. A worker crash must leave incomplete progress and a failed run. Corrupt/stale progress files cannot turn a failed run into success.
- [ ] Keep supervisor heartbeat output separate from retained child stdout/stderr. Preserve bounded pipe draining, descendant-handle detection, interruption and cleanup semantics. Do not add automatic termination based on elapsed time.

**Acceptance:** A quiet run produces a heartbeat within 35 seconds; test IDs come from pytest observations; no outcome is inferred from liveness; existing recorder failure cases still fail correctly.

## Supersession, migration and teardown

The replacement scope is behavior-specific. This plan extends the existing launcher and recorder; it does not introduce a replacement launcher, recorder or environment manager.

| Existing component or practice | Disposition | Replacement / retirement condition |
| --- | --- | --- |
| `fp.ps1`, `scripts/fp.py`, launcher environment selection and lock validation | Retain and extend | Existing commands remain supported; pytest configuration selection becomes explicit |
| `scripts/record_verification.py` and historical `record.json` evidence | Retain and extend | Preserve interpretation of existing records; add progress separately from final acceptance |
| Ambient pytest parent-root discovery through launcher commands | Replace | Task 1 subprocess cases pass for all launcher pytest routes |
| Repeated manual `-c`/`--rootdir` workarounds in maintained commands | Remove redundant options after migration | First verify that the launcher supplies equivalent behavior; historical audit commands remain unchanged |
| Full baseline run in the same checkout being edited | Replace as the default workflow | Task 2 validates separate checkout attribution; a stable single-checkout run remains valid when no concurrent edits occur |
| Manually polling stdout files for liveness | Replace routine use | Task 3 emits observed progress; retain raw logs for diagnosis |
| Pytest/xdist, `requirements-ops.lock`, shared validated operations venv | Retain | No tool/dependency migration or shared-environment deletion is implied |
| Existing generic Docker verification wrapper and sequence suites | Retain | See Linux companion; these are not superseded by qualification-specific isolation tests |

### Task 4: Migrate callers and retire only proven redundant paths

**Outcome:** Maintained entry points use the improved workflow with no competing configuration rules, abandoned test resources or loss of historical evidence.

**Files:** Review references in `scripts/README.md`, `tools/local_verification/README.md`, `.github/workflows/`, `tests/test_fp_launcher.py`, `tests/test_record_verification.py` and active implementation handoffs. Modify only affected maintained callers; do not rewrite historical audit evidence.

- [ ] At implementation time inventory callers with `rg` for `record_verification`, `docker_verification`, `local_verification`, explicit pytest root/config arguments and any existing progress plugins. Record which actually execute the launcher versus pytest directly. The inspected baseline is not proof that no later callers exist.
- [ ] Identify command compatibility before changing behavior: external test paths, explicit equivalent root/config, custom JUnit destinations, selected workers, foreign working directories and arbitrary-command recording. Keep tests for each supported path. Direct generic-recorder users must not acquire pytest-only argument injection.
- [ ] Run old and new behavior on equivalent fixed inputs in separate evidence directories. Require matching test selection and outcomes, aside from the intentional root-selection correction. Require final evidence validation and interruption semantics to remain intact.
- [ ] Update maintained caller documentation and remove redundant root-discovery/workaround branches in the same reviewed change. Preserve explicit conflicting-config rejection rather than silently choosing one option. Do not retain an undocumented legacy mode that restores ambient-root discovery.
- [ ] If an existing progress implementation is found, extend or replace it within Task 3. Remove its obsolete plugin registration and tests only after real serial/xdist equivalence passes. Keep one launcher registration and one recorder heartbeat owner so output is not duplicated.
- [ ] Register newly created baseline worktrees with their exact absolute path, revision, owning run and evidence directory. Before removal require the run to be terminal, no live child process, retained finalized evidence and a clean owned worktree. Use `git worktree remove` on that exact path; never force-remove a dirty or unowned worktree. Interrupted or uncertain runs require reconciliation first.
- [ ] Finish by searching maintained references again and exercising their commands. Report explicitly what was removed, retained and still used. Absence of search hits alone does not establish that a host resource is unused.

**Acceptance:** One effective pytest configuration-selection path and one progress producer per process; no stale maintained instructions; no active/dirty worktree removed; previous records remain readable. No change to global Git configuration, Docker Desktop, WSL installations or shared environments.

**Rollback:** Revert the launcher/progress code change if a compatibility regression appears. Preserve both old and new run records. Mark results affected by the original root-selection defect as unsuitable for the claimed scope; rollback must not silently bless them. Baseline checkout separation is reversible workflow guidance and requires no destructive rollback.

## Final verification and handoff

Run from the implementation checkout after edits stop:

```powershell
.\fp.ps1 doctor
.\fp.ps1 --workers 2 python -m pytest tests/test_fp_launcher.py tests/test_record_verification.py tests/test_pytest_progress.py tests/test_docker_verification.py -q --tb=short
.\fp.ps1 check
```

Repeat launcher/progress tests on Linux using `python -I scripts/fp.py` and its validated environment. Compare the same selected suite before/after, recording elapsed time and worker count; claim only observed improvements. Report revision/dirty fingerprint, interpreter, exact commands, record paths, results and unresolved failures.

Acceptance requires the external-test-root case, simultaneous baseline/candidate case and real quiet-subprocess case. Documentation and mocked subprocess tests alone cannot close those behaviors. Commits, PRs and infrastructure changes follow the authorization in force at implementation time.
