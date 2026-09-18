# Qualification structural closure — bounded implementation handoff

Latest checkpoint: commit `67b93dd853113f7bb693cae9256ad3b2cb65f356`, Linux run
[35299214700](https://github.com/Joshua-Asante/first-passage/actions/runs/35299214700).
Host1:18passed/1failed; host2:17passed/2failed; both cleanups succeeded.
Pin consistency is repaired. Stopped-worker verification and the host2 OOM
discrepancy remain open. The sections below preserve the earlier handoffs in order;
the final checkpoint and governing plan supersede their older next-step guidance.

Acceptance remains **HELD**. This is a lifecycle/fault-verification checkpoint,
not completion of the nine-task plan or qualification acceptance.

## Revision and ownership

- Coordinator: `/root`; canonical policy/configuration and combined acceptance remain coordinator-owned.
- Branch: `codex/qualification-structural-closure`, pushed checkpoint
  `9a85772454a507da09903c0b2ca492a70301f0d8`.
- Checkout: `C:/Users/joshu/multi_firm_operations/.worktrees/qualification-structural-closure`.
- Governing [plan](../../superpowers/plans/2026-09-17-qualification-structural-closure.md)
  and [design](../../superpowers/specs/2026-09-17-qualification-structural-closure-design.md).
- The user-directed return boundary is to observe existing Linux run
  [35296382825](https://github.com/Joshua-Asante/first-passage/actions/runs/35296382825),
  retain its evidence and return. No additional repair/rerun cycle is authorized
  within this bounded continuation.
- Main checkout, unrelated changes and prototype worktrees remain preserved.
  The auxiliary `codex/qualification-invariant-gate` worktree remains intact;
  its four delivered files were copied into and committed on the implementation branch.

## Implemented checkpoint

Tasks 1–4 provide canonical policy, actual retained registry/source admission,
role-specific evidence reconstruction and acyclic logical snapshots. Tasks 5–7
provide signed v2 admission/preflight, protected worker execution/capture/G5 and
atomic N1 result commit. The public v1 authentication/claim/commit/seal routes and
legacy OPERATOR executor now reject with `LEGACY_QUALIFICATION_INSPECTION_ONLY`.
Historical signature/replay/private-v3 consistency tests remain.

Task 8 now has an independent SQL-free lifecycle model and real Linux tests for
CAPTURED signer denial/restart, VOID and original retries, actual stopped-worker
and supervisor death, empty output with zero exit, CPU/wall/memory faults and
real approval expiry. Passing fixture admission is not worker-fault evidence;
the Linux run below determines the actual result of these new cases.

Task 9 has the report-validation library and tests, including exact node IDs,
critical skips/failures, ambiguous JUnit identities, duplicate reports and
hash-bound child reports. The canonical invariant manifest and acceptance gate
are **not wired**. CI metadata continues to say acceptance is held.

## Verification already inspected

All local Python used this checkout's `./fp.ps1` launcher after doctor passed:
`C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`, Python 3.13.2,
62 locked packages and cryptography 50.0.1.

| Command selection (launcher prefix `./fp.ps1 --workers 2 python -m pytest`) | Actual result | Record under `.cache/fp-verification` |
| --- | --- | --- |
| Authority boundaries, historical seal/review/orchestration/production/composition, phase3 provenance, service, boundary fixture | 133 passed | `20260918T011115Z-dd623041ab3c` |
| `tests/ops/qualification/execution/test_boundary_fixture.py -q --tb=short` | 6 passed; signed fault fixture admission only | `20260918T013546Z-9f1b65d1a2ca` |
| `tests/test_qualification_invariant_manifest.py tests/ops/qualification/execution/test_lifecycle_model.py tests/ops/qualification/execution/test_store.py -q --tb=short` | 88 passed, 1 Windows symlink-privilege skip | `20260918T013959Z-f5dd157419d7` |
| `tests/ops/qualification/execution/test_request_concurrency.py -q --tb=short` | 2 passed; unused helper only | `20260918T014402Z-6c19e5d1e5e7` |

Each listed record completed with exit 0, stable source, complete capture and no
report errors. These records identify different working-tree snapshots; they
are not a claim that the entire latest combined suite passed.

`./fp.ps1 check` passed at the earlier cutover working tree, record
`20260918T012220Z-52644c82d707`, also stable/complete. It ran 72 evidence-store cases
with 3 existing skips. Private Pine/data/heavy-analysis artifacts were absent
and were not verified.

Earlier actual Linux evidence:

- Run `35293290005` at `2c6b025`: two fresh Ubuntu hosts each passed 6/6 incremental
  execution/G5/retry tests. Python 3.12.3, qclient/qexec/qg5 UIDs 61000/61001/61002;
  stable/complete records and successful cleanup. Independent review checked 346
  retained object hashes and capture/receipt/UID/cleanup links.
- Run `35295798574` at `16ffe7e`: each host passed 6 and failed 6, no skips;
  stable/complete records, cleanup successful. All failures were raw-test-driver
  timeouts because it omitted `shutdown(SHUT_WR)`. Production client already did
  this. The driver fix is in `9a85772`; the three initial lifecycle cases passed
  on each host. Evidence: `.cache/qualification-linux/35295798574`.

## Partial work preserved outside the committed checkpoint

- `ops/c1_rail/qualification/execution/service.py`: new `BoundedConnections`
  helper, **unused**. `serve()` remains serial. No RPC/transaction wiring changed.
- `tests/ops/qualification/execution/test_request_concurrency.py`: two focused
  scheduler tests, observed RED before implementation and now passing. They do
  not establish actual peer isolation or VOID/commit contention.
- This handoff and the final plan ledger update are uncommitted documentation.

## Remaining acceptance work

Task 8 still requires administrator-controlled interruption before start/after
intent/during output, expiry between intent and observed start, real worker
permission probes, wrong retained object and current key/release invalidity at
acceptance, lost-acknowledgment handling, and both actual VOID/publication and
VOID/first-commit writer orders. Serial socket handling cannot show two competing
request writers; a socket backlog is not SQLite lock evidence.

Task 9 still requires the canonical nine-invariant manifest tied to actual
collection and execution, recorder/CI wiring, three targeted mutation checks in
a disposable copy, complete combined checks and independent integration review.
The current `--test-only` route remains incremental diagnostics.

Recommended next bounded assignment: repair the synthetic fault producer's
historical port-pin consistency, require real source admission before dispatch,
and verify the five failed fault cases on fresh Linux hosts without weakening
production validation. Then return with that evidence before concurrency work. Preserve the
unused helper as a draft until its real service integration is tested. A proposed
administrator-only TEST_ONLY tracing driver may observe SQLite trace callbacks
and pause real transactions; it must not replace state, inputs, outcomes or peer
identity, and must retain its measured identity and control-channel authentication.

The ceiling remains synthetic **N1_ONLY**: terminal FAIL or PARTIAL/CONTINUE.
No full E1 PASS/seal, OPERATOR execution, production keys, qualification,
provisioning spend, deployment or merge has been authorized or performed.

## Final Linux run and process disposition

Run 35296382825 completed **failure** on both fresh Ubuntu hosts at committed
`9a85772454a507da09903c0b2ca492a70301f0d8`. Each collected 19 tests:
**14 passed, 5 failed, 0 skipped, 0 errors**. Both real approval-expiry cases,
raw client rejection, capture/G5, restart and original-receipt/VOID cases passed.
The stopped-worker case and four exit/CPU/wall/memory cases failed.

Worker stderr shows actual retained-source rejection before the intended fault:
`historical admission does not retain corrected Striker/four-leg ports` from
`production_source.py:595`. The signed fault fixture changes runtime source,
but its historical admission port map does not match the resolved domain pins.
The static fixture checks did not exercise this full source-admission path.
The intended SIGSTOP/zero-exit/budget/OOM behavior remains unverified. No repair
or rerun was performed after this result.

Artifacts are retained under `.cache/qualification-linux/35296382825/`:

- Host 1: `qualification-host-readiness-1/9dcc797a435246468b1e64c1b1d30d6f/record.json`.
- Host 2: `qualification-host-readiness-2/0a31b4031d9e4825aa398912c240345b/record.json`.

Both records have stable source, complete capture, no capture errors, exit 1
and report errors explicitly identifying failed JUnit cases. These are valid
failure evidence, not passing acceptance records. Each cleanup receipt reports
success with no failures, retiring 13 exact containers, the owned image, role
users and owned runtime trees. Repeated cleanup reports already retired.

Linux doctor selected each host's protected `env/bin/python`, Python 3.12.3,
62 locked packages and cryptography 50.0.1. CI used that interpreter with
`-I scripts/fp.py --env <host-env> doctor`, followed by launcher `python
scripts/qualification_boundary_verification.py --test-only --manifest <manifest>`;
the recorded selection was `-m pytest tests/integration/qualification_boundary
-q --tb=short --junitxml=<record>/junit.xml`.

Both CI jobs and the review agent are complete. No local Python/test process
remained at the final process inspection. The unused concurrency helper and its
two tests remain uncommitted alongside this handoff and the updated plan.
Implementation is stopped at this bounded checkpoint; acceptance remains HELD.

### Fault-fixture continuation — publishing blocked

The requested pin repair is committed locally as `61d7ff2` (base `9a85772`). Final port bytes now precede historical/population/review hashing; fixture assembly exercises real source admission before staging, and Linux fault checks require the actual fault callback marker. Local source/fixture regression selection:67passed; gates passed, retaining the existing3 evidence-store skips and unavailable private artifacts. Records: `20260918T020047Z-039752d69106` and `20260918T020207Z-a5b7de307566`, both completed/exit0/stable/complete/no report errors, operations Python3.13.2. The Git commit hook independently invoked its configured Python3.14.3 static checks; these are not substituted for launcher evidence.

Automatic approval review rejected `git push origin HEAD:refs/heads/codex/qualification-structural-closure`: external GitHub repository payload requires explicit trusted-user destination authorization. No push, dispatch or fresh Linux verification occurred. Required approval: publish commit61d7ff2 to `Joshua-Asante/first-passage`, branch `codex/qualification-structural-closure`, and dispatch the existing two disposable Ubuntu TEST_ONLY jobs. The five real faults remain unverified until that evidence is obtained; acceptance remains HELD. Existing service scheduler draft and test, main checkout and other worktrees are preserved. Resume with this commit and existing local evidence; do not repeat the repair.

### Four-fault verification and corrected stop driver — return checkpoint

User approved publishing61d7ff2 and two-host CI. Run35298023879 completed18passed/1failed on each host, zero skips/errors; cleanup succeeded. Inspected314 retained object hashes per host, record artifact hashes, admission/legality bindings and four real fault markers/outcomes. Zero-exit, CPU, wall and memory faults are verified with no attestation/result and one start. Source pins are repaired.

SIGSTOP case failed because the fixture tried to stop PID-namespace init from inside that namespace; the process instead exited0 and produced ordinary ATTESTED evidence. This is not stopped-worker evidence. Correction committed as `67b93dd`: callback waits at its marker; administrator sends SIGSTOP to the exact container and requires host process stateT before supervisor death/restart. Local fixture6passed and gates passed (`20260918T021700Z-0aa653ad055b`, `20260918T021722Z-31310dda4d6e`), stable/complete, operations Python3.13.2. No production validation or execution topology changes.

Automatic approval review rejected pushing67b93dd because the prior approval covered only61d7ff2. Required explicit approval: push67b93dd to `Joshua-Asante/first-passage`, branch `codex/qualification-structural-closure`, and run two fresh disposable Ubuntu TEST_ONLY jobs. No second push or dispatch occurred. Resume at that publication step; retain `.cache/qualification-linux/35298023879/inspection.json` as a failed-overall/four-fault evidence summary. Fifth fault remains unverified; acceptance HELD. Unused concurrency draft/test and other worktrees preserved.

### Latest approved CI result —35299214700 at67b93dd

The user approved the corrected commit and job dispatch. Push succeeded. Both jobs completed failure: host1 18passed/1failed (stop), host2 17passed/2failed (stop and OOMKilled),19collected each, no skips/errors. Both records stable/complete with successful owned cleanup. Evidence is retained in `.cache/qualification-linux/35299214700`, including `inspection.json` and `failure-detail.json`; full disposition is appended to the governing plan.

Source-pin consistency is repaired. Complete five-fault verification remains incomplete. The stop driver waits on buffered stderr that is not flushed until capture EOF; both exported stop logs were empty and no observed-stop receipt exists. A buffer-independent readiness observation is needed. Host2 memory reached its fault marker and exited137 but Docker reported OOMKilled=false; kernel/cgroup OOM evidence and exit ordering need investigation before accepting it. Do not treat missing host2 memory start-event export as zero starts, or its unexecuted retry assertions as verified.

Branch HEAD67b93dd is pushed. No further code changes or runs were made after this result. Plan/handoff updates remain local; unused concurrency work is preserved. Acceptance HELD, synthetic N1_ONLY ceiling unchanged. Return this failed verification checkpoint before selecting the next bounded readiness/OOM investigation.

### Five-fault readiness/OOM repair — bounded execution

**Selected outcome:** Verify stop, zero-exit, CPU, wall and confirmed memory OOM on both fresh disposable Linux hosts.
**Prerequisites:** PR425 base `6590b61`; prior run `35299214700` and its retained inspections. Existing dirty lifecycle work is excluded in separate worktree `qualification-fault-verification`.
**Ownership:** This task owns fault repair and evidence; the PR425 coordinator retains combined qualification acceptance.
**Verification:** Local launcher/fixture regressions, then the existing real `--test-only` workflow on both Ubuntu hosts; require actual stopped state, OOMKilled plus ordered OOM/die events, one launch, no attestation/result, exact retry and successful cleanup. Retain source identity and reports.
**Checkpoint:** Record local checks and fresh hosted run evidence here before handoff.
**Return boundary:** Return the five-fault result; no lifecycle expansion, invariant-gate acceptance, draft removal, merge, or production qualification.

Confirmed readiness cause: worker uses `os.write(2, ...)`, but launcher buffers its file until EOF. Per-chunk flush fixes the shared capture owner without changing final fsync or log limits. Regression `test_capture_exposes_stderr_before_worker_eof` failed with an empty live log before the fix. Related cases: all five callbacks share capture; normal EOF retains flush/fsync; bounded log/output rejection is unchanged.

Historical host2 memory cause remains unconfirmed: container `27279ed72cff826c7d0f063fcbf8a83837e8077531e14078b3ec684486bf1526` exited137 after 3.116 seconds, OOMKilled=false, no retained kernel/cgroup events. No claim of OOM is made for that run. Host pressure from a single 1.5 GB allocation is a hypothesis, not a finding. The canonical TEST_ONLY profile now limits the worker to256 MB, contract memory budget derives from that profile, and the fault charges paced1 MB resident chunks capped at about twice the limit. Fresh acceptance additionally requires an OOM event before die; kernel/oomd diagnostics are exported for future ambiguous deaths.

Local evidence: operations Python3.13.2 at `C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`; doctor matched62 locked packages. `./fp.ps1 --workers 2 python -m pytest tests/ops/qualification/execution/test_launcher.py tests/ops/qualification/execution/test_profile.py tests/ops/qualification/execution/test_boundary_fixture.py -q --tb=short`:29passed; record `20260918T031851Z-6d15a0e93674`, completed/exit0/stable. Red regression record `20260918T031746Z-19fcfa8456fc` failed at the expected live-log assertion. Hosted acceptance remains pending.
