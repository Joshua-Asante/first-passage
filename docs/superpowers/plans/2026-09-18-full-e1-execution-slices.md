# Protected Full E1 Execution — Delegable Implementation Plan

> **For agentic workers:** Execute with superpowers:executing-plans; use superpowers:subagent-driven-development when bounded delegation is useful and authorized. Preserve the behavioral contract and integration owner. Execute only the slice assigned by the coordinator, then return. This document does not authorize an agent to continue into its successor slice.

**Goal:** Run one genuine protected synthetic E1 campaign through N1, one joint N2/Part B batch, prescribed Part A, independent G5, atomic full-result commit and separate sealing, with accepted interruption/invalidity behavior on Linux.

**Architecture:** Continue the accepted Task 1a planner and Task 1b dormant admission in the existing protected execution service. The service owns state, resource attribution, dispatch, capture and publication; installed independent G5 reconstructs results; a separate installed qseal signs only a complete committed PASS. Reuse the existing engine and canonical policy/evidence owners.

**Tech Stack:** Operations Python and fp launcher; canonical JSON and enrolled Ed25519 signatures; existing SQLite ExecutionStore; Linux peer credentials, cgroup v2 and Docker; existing disposable Ubuntu harness and invariant manifest.

**Spec:** [Governing full-E1 specification](../specs/2026-09-17-protected-full-e1-campaign.md). [Original roadmap and accepted evidence](2026-09-17-protected-full-e1-campaign.md). This plan replaces the original roadmap's remaining task decomposition with eight bounded handoffs; it does not replace its acceptance requirements or historical evidence.

## Global constraints

- FULL_E1 initially has `authority_class=TEST_ONLY` and `production_execution=false`.
- No in-place continuation of an N1_ONLY attempt into FULL_E1.
- All depths, thresholds, namespaces and budgets come from the frozen contract, not copied constants.
- Part A remains one dispatched compute operation using the existing append loop.
- The execution service verifies both and owns publication receipts.
- Administrator and Docker-privileged qexec are trusted; distinct UIDs do not confine malicious qexec.
- Do not call `run_production_e1`, `_execute_e1` or construct `ProductionExecutor` to execute protected work. Legacy caller-controlled execution stays closed.
- Preserve one joint N2 batch, the initial Part A prefix, exact seed/probe addresses and the accepted statistical formulas. Equal configured initial/expanded panel counts reject; inclusive expansion-tolerance equality remains a positive case.
- Operational interruption, malformed capture, exhausted/uncertain budget and VOID are not statistical FAIL observations.
- Synthetic acceptance is separate from actual feed/broker feasibility and live deployment. No broker, subscription, account, live-performance distribution or launch-date dependency is introduced here.
- Verification is proportional: reuse unchanged evidence; check affected interfaces per slice; reserve the full E01–E12 campaign suite and combined review for the integrated candidate. Real Linux accounting/isolation claims require real-host evidence, not mocks.

## Starting state and handoff preparation

Accepted merge: `1e4928360b95812b04725dc1e8da97709d670ff4` (PR425; PR415 was not separately merged).

Current authoritative workspace: `C:/Users/joshu/.codex/worktrees/full-e1-recovery/multi_firm_operations`. It is detached at that merge **with exactly recovered accepted Task 1a/1b source changes**. The original worktree is no longer present. The checksummed recovery snapshot and fresh verification records are indexed in the recovery packet `recovery/full-e1-20260919/README.md` (local-only, not in this repo; archived in the private first-passage-archive, SHA-256 `50bb068cc6b1fa7399ba6dd351ab61af6985c45c8e4e489f42eb9679c70be411`). Checking out the merge alone loses those changes. Do not start a future agent on that bare merge and describe it as the accepted successor.

Already accepted; do not rebuild:

| Checkpoint | Actual capability | Evidence |
|---|---|---|
| Task 1a | Canonical campaign plan, exact-byte validator and verified-context adapter; PLANNING_ONLY | Original 216-case record; refreshed campaign-plan regressions in Task 1b final run |
| Task 1b | Dormant FULL_E1 admission; immutable plan/source custody; status, exact retries, authorized VOID; bounded chunks and verifying client; exact v4-to-v5 journal migration | `.cache/fp-verification/20260919T003248Z-100e170d5b7e/record.json`: 182 passed, no skips; check `20260919T003321Z-44e0f6cac19f/record.json`: success, three evidence-store skips/advisories; independent review accepted |

Existing release/profile v2 have `dispatch_enabled=false` and no executable checkpoints. They cannot run E1. Existing CampaignStore is a wrapper around ExecutionStore's database/transaction authority, not a second database. It already exposes `admit(request_bytes, context, plan, *, now)`, `retry(request_bytes)`, `status(attempt)`, `context(attempt, installed_release, keys, *, now)`, `chunk(request)`, `void_retry(request_bytes)` and `void(request_bytes, *, now)`. Preserve their historical meanings.

Before delegating S1, the coordinator packages accepted Task 1a/1b into a named `codex/` branch/commit, or provides a checksummed source snapshot plus the accepted verification records. This planning deliverable makes no commit. If reusing the current checkout, compare current implementation/test bytes to the final record before edits. If the record/snapshot is unavailable or differs, return the specific baseline conflict; do not rebuild from memory. Preserve unrelated CAP/feed documentation. No destructive reset or blanket staging.

Each later assignment names the actual accepted predecessor commit/snapshot, not a guessed future SHA. The executor records that identity, reads AGENTS.md, this entire common contract, the governing specification and its selected slice. Changes to an accepted predecessor require proportionate re-review.

## Sequence and useful parallel work

| Slice | Reviewable outcome | Depends on | Original roadmap |
|---|---|---|---|
| S1 | Durable lifetime budget and recovery state, without process launch | Accepted 1a/1b | Task 2, persisted model |
| S2 | Budgeted admission and real Linux work supervision | S1 | Task 2, runtime enforcement |
| S3 | Genuine protected N1 capture and committed G5 decision | S2 | Tasks 3/4, N1 vertical route |
| S4 | One joint N2/Part B capture and committed G5 continuation/failure | S3 | Tasks 3/4, joint stage |
| S5 | Genuine Part A with prescribed expansion and G5 decision | S4 | Tasks 3/4, Part A |
| S6 | Authenticated complete result and atomic commit | S5; fail-prefix cases from S3/S4 | Task 5, result |
| S7 | Separate qseal and atomic seal publication | S6 | Task 5, seal |
| S8 | Integrated Linux campaign acceptance and combined review | S1–S7 | Task 6 |

Default implementation order is sequential: most slices share the service, store, protocol and evidence owners. Do not assign simultaneous writers to those files. Useful parallel work is read-only review, synthetic-source scenario design, and preparation of future tests on an isolated branch against explicitly agreed interfaces. S8 harness preparation may begin during S3–S7, but its execution/acceptance requires the integrated candidate. Feed/CrossTrade work remains independently parallel.

Each slice is one test-and-review checkpoint, not a promised number of hours. If a slice cannot meet its outcome within its contract, return a concrete interface/scope finding. The coordinator can split it around a meaningful observable outcome; never label an implementation fragment accepted simply because files were edited.

## Shared execution and evidence contract

**Ownership:** The assigned agent implements one slice. The coordinator accepts its returned behavior and owns integration; independent reviewers assess the changed behavior. Only the coordinator accepts the full campaign.

**Verification commands:** Run from the checkout being tested:

```powershell
./fp.ps1 doctor
./fp.ps1 --workers 2 python -m pytest <the selected slice test paths below> -q --tb=short
./fp.ps1 check
git diff --check
```

The angle-bracket expression denotes the explicit path list provided in each slice, not a command to copy literally. On Linux use `python -I scripts/fp.py doctor` and `python -I scripts/fp.py python -m pytest` through the configured operations environment. No system-Python fallback. For real boundary tests use the accepted harness command in S8; local Docker/Windows tests do not substitute for its Linux guarantees.

Write behavior tests first, observe the intended missing behavior, implement the smallest change, and run the affected selection once on stable final sources. Retain actual interpreter, command, source identity, counts, failures/skips and record paths. A pass requires completed capture, exit/verification exit zero, stable source, valid reports and successful required cleanup. Do not rerun a valid unchanged record merely for another reviewer. Investigate failures; do not weaken tests or thresholds to obtain PASS.

**Return packet for every slice:** Changed behavior/interfaces; accepted starting and final identities; exact checks/records; remaining dependencies; review findings/disposition; any schema/profile migration and rollback limitations. Update this plan's progress ledger after recorder closure. Default return is reviewable local changes; commit/push/PR actions follow the coordinator's explicit assignment. A future agent must not assume publication authorization from this plan alone.

**Checkpoint:** Report an impossible governing requirement or necessary consequential interface change before dependent implementation. Ordinary fixes within the selected behavior remain authorized. Do not ask the operator to approve routine implementation decisions already assigned to the coordinator.

### Contract decisions carried across slices

1. **Fresh executable attempts.** Task 1b's dormant campaigns have no lifetime charge history. Retain their plans/receipts as historical admission-only objects. Do not upgrade them, fabricate past usage or activate them later. S2 introduces a new closed execution-capable release/profile revision and fresh attempts. N1_ONLY attempts likewise never migrate into FULL_E1.
2. **Accounting starts before campaign work.** S1/S2 persist a bounded provisional admission intent before the campaign-specific validation/planning process. The installed profile supplies its maximum reservation before the frozen contract is trusted. Once validated, bind the frozen cap and compute the deadline from the original start; include already consumed admission time/CPU, and reject if it cannot fit. No reset when admission succeeds or retries. Authentication failure produces no qualification authority. Keep cheap transport/role checks and bounded historical inspection outside stochastic work; do not smuggle reconstruction/signing through an uncharged status endpoint.
3. **Reservations cover the rest of the route.** Canonical installed configuration names admission, checkpoint/source proof/probe, capture/attestation, each G5 assessment, aggregate validation/commit and sealing/finalization ceilings. Validate feasibility against the frozen cap, including prescribed maximum expansion. Actual CPU counters settle reservations once; unknown usage consumes its full reservation. Remaining wall time includes queues and downtime. Memory is an enforced shared concurrent footprint, not independent full-size allowances per process. In this design the cumulative bound is per work and kernel-enforced: payload quota × guardian `RuntimeMaxUSec` + the guardian's `LimitCPU` allowance + the bounded control-helper CPU never exceeds that work's reservation (the allowances include the existing enforcement-granularity margins, counted once), and settled charges plus open reservations never exceed the frozen cap (AUDIT-2026-09-25-qualification-assurance-contract-delta#N1). A campaign-level rate quota is not a substitute. Every phase, PART_A, RESULT and SEAL included, reserves its installed phase ceiling; PART_A's is measured at maximum expansion. No per-phase CPU figure enters a statistical decision. The operator fixes a measurement-and-margin rule (the measurement standard and the margin) by ruling. The coordinator may set TEST_ONLY diagnostic ceilings only by applying that rule (a cited measurement, the rule's margin, a ledger entry); anything outside it needs an operator ruling. Production ceilings and caps are frozen with F1 by their owners and are never set under that rule. The approved rule's scope is PART_A only, TEST_ONLY (operator rulings 2026-09-26 and 2026-09-27; CP-1a 2026-09-27). Every other TEST_ONLY diagnostic phase ceiling comes from an operator ruling: `/v7`'s N2 compute phase takes 360 s CPU / 900 s wall, the M13 values extended by CP-1a decision (3) to the `/v7` TEST_ONLY diagnostic profile only.
4. **Staged development does not change admitted releases.** Before all stages exist, test signed diagnostic releases can expose only implemented checkpoints; reaching the end of their allowed prefix stops without final PASS or seal. A later code/profile revision uses a fresh attempt. Final acceptance uses a release enabling all three compute checkpoints and the complete G5/result/seal route.
5. **Snapshots and transport have one owner.** Extend `qualification/journal_snapshot.py`, `qualification/checkpoint_plan.py`, policy/evidence owners and existing versioned campaign protocol. Plans remain non-authoritative inputs; the service's recorded dispatch intent authorizes work. Keep 1 MiB bounded chunks and explicit total-size limits. G5 needs authenticated access to retained inputs/captures and private candidate staging; a digest with no authorized producer/fetch route is not an interface.
6. **Signing recovery is durable.** Fixed payload, key, signing time and intent identity precede signing. Recover exact signed candidate/receipt on retry. Missing capture never licenses another draw; a spec §2.6 bounded same-sample re-execution is not a draw (AUDIT-2026-09-25-qualification-assurance-contract-delta#N2); missing deterministic G5 validation may be repeated only under the original remaining budget. VOID/expiry/revocation bar new authority while exact historical receipts remain inspectable with current validity.

## S1 — Durable budget and recovery state without launch

**Selected outcome:** One persisted campaign allowance and operation history survive reopen, duplicate calls and uncertain completion; no process is launched and no authority is activated.

**Prerequisites:** Accepted Task 1a/1b source snapshot. Existing dormant v2 receipts remain unchanged. No Linux host is required to accept deterministic store behavior; OS observations in these tests are explicitly simulated trusted inputs.

**Ownership:** S1 executor owns persistence/accounting changes; coordinator accepts S1 and the full campaign.

**Files:** Extend `ops/c1_rail/qualification/execution/campaign_store.py`, `store.py`, `profile.py` and `ops/c1_rail/qualification/journal_snapshot.py`; add `execution/campaign_budget.py`; extend `tests/ops/qualification/execution/lifecycle_model.py`; add `test_campaign_budget.py` and `test_campaign_recovery.py`. Paths under `execution/` use the qualification package above. Store/schema changes remain additive with exact layout validation, transactional migration and historical v4/v5 readability.

**Interfaces, proposed and owned by this slice:** Add private CampaignStore methods `begin_admission(request_bytes, profile_bytes, clock_bytes) -> bytes`, `bind_budget(attempt_id, contract_budget_bytes, *, expected_revision) -> bytes`, `reserve_work(attempt_id, work_id, phase, limits_bytes, *, expected_revision) -> bytes`, `settle_work(attempt_id, work_id, observations_bytes) -> bytes`, `record_work_transition(attempt_id, work_id, transition_bytes, *, expected_revision) -> bytes`, `recover_work(attempt_id, work_id, observations_bytes) -> bytes`, and `budget_snapshot(attempt_id) -> bytes`. These proposed names are not presently callable; downstream slices consume the accepted S1 names recorded on return. Snapshot encoding belongs to the canonical snapshot module. No public caller supplies trusted clock/counter observations.

**Behavior:** Persist immutable request/profile/budget bindings, boot ID, original BOOTTIME start/deadline and UTC audit value, revision/head, reservations, settled charges, observed common memory peak/OOM, operation IDs, dispatch/capture/signing boundaries and irreversible terminal states. Reject changed payloads under existing keys. Exact settlement is idempotent; conflicting observations reject. Boot change/regressing trusted clock marks BUDGET_UNCERTAIN. An overrun permanently bars authority. IN_DOUBT is durable before cleanup. RESERVED without START_INTENT may reuse the same reservation; START_INTENT/RUNNING without finalized capture never reexecutes; CAPTURED can only validate saved bytes. VOID serializes with all transitions in ExecutionStore's existing transaction.

- [x] Implement model/store tests for one cap across two stages, open reservations, duplicate settlement, lost counters, wall expiry during downtime, changed boot, concurrent reservation, rollback and VOID ordering.
- [x] Introduce canonical phase configuration and closed private observation schemas with exact integer/identity checks; never accept worker-asserted CPU as authoritative.
- [x] Extend the logical snapshot/model and database together; retain historical dormant receipts and avoid cycles between snapshots and their own commit events.
- [x] Verify model/store parity and reopen behavior with actual SQLite, then return before any launch integration.

A required test vector for the pure arithmetic helper produced in `campaign_budget.py`:

```python
from c1_rail.qualification.execution.campaign_budget import remaining_cpu

def test_open_reservation_cannot_be_spent_twice():
    assert remaining_cpu(100, (20,), (60,)) == 20
    assert remaining_cpu(100, (20, 60), ()) == 20
```

**Verification:** Selected paths: `tests/ops/qualification/execution/test_campaign_budget.py`, `test_campaign_recovery.py`, `test_campaign_admission.py`, `test_store.py`, `test_lifecycle_model.py` in the same test directory. Exercise real transaction interleavings for the changed state; no resource-performance benchmark.

**Checkpoint:** Return the budget/state snapshot schemas and source-bound test evidence, or a precise conflict with accepted persistence semantics.

**Return boundary:** S1 ends at locally verified persisted semantics. Exclude OS counter enforcement, stage execution, G5/results/seals and Linux campaign acceptance.

## S2 — Budgeted admission and real Linux work supervision

**Selected outcome:** A fresh executable-campaign admission and supervised test work consume the same durable allowance, with real CPU/memory/wall enforcement and interruption recovery. Qualification-stage dispatch remains disabled until S3.

**Prerequisites:** Accepted S1. Disposable supported Linux host for OS acceptance; without it, local implementation can return but this slice's Linux enforcement claim remains pending and executable activation is blocked. Use existing host provisioning; no paid infrastructure assumption.

**Ownership:** S2 executor integrates supervisor/admission/accounting and host configuration; coordinator accepts the boundary.

**Files:** `execution/service.py`, `admission.py`, `launcher.py`, `budget.py`, `runtime.py`, `profile.py`, `release_schema.py`, `release.py`, `campaign_store.py`; add `execution/campaign_supervisor.py` as the process-accounting adapter, not another store; extend `tools/qualification_verification/host.json`, `host.py`, `provision.sh`, `cleanup.py`, `role_policy.py`, installed `deploy/qualification/bootstrap.py`, and the existing instance/image fixtures where required. Add `tests/ops/qualification/execution/test_campaign_supervision.py`. Record every changed installed source/config identity.

**Interfaces:** Existing `verify_bundle`/`verify_retained_bundle` and canonical plan producer remain the admission consumers. Proposed supervisor adapter `observe_campaign_clock() -> bytes`, `run_campaign_work(context, reservation_bytes, input_manifest_bytes) -> bytes`, and `recover_campaign_work(context, reservation_bytes) -> bytes` produce trusted closed observations/capture references for S1. The manifest selects only installed fixed roles/entrypoints; no client command/path/code argument. S2 also supplies private service scheduling of metered G5/commit/seal work for later slices, initially tested with harmless fixed probe work.

**Behavior:** Create the durable admission intent and bounded work scope before verifying/deriving campaign inputs. Revalidate originals at publication; bind the authenticated budget to the original start and charge all admission work. Old v2 dormant rows remain inspectable only. Enforce cumulative CPU (not only rate), shared memory and BOOTTIME deadline for descendants; Docker workers and role-separated helpers must belong to the attributed hierarchy. Persist owned process/container identities before start. Counter loss charges the reservation. Stop and retain terminal status on overrun/OOM. Cleanup failure cannot restore authority or erase history. Shared service orchestration cost must be conservatively attributed; expensive serialization, reconstruction and signing cannot escape into the unmetered RPC handler.

- [ ] Add real-host tests using fixed synthetic CPU/descendant/memory probes: exceed a reservation, aggregate two descendants, lose a counter, restart supervisor and fail cleanup.
- [ ] Implement installed release/profile/config changes and fixed-role process runner; bind resolved phase ceilings and resource scope to admission and receipts.
- [ ] Move heavy admission/planning work under the runner. Keep historical cheap receipt access available; any fresh eligibility reconstruction uses a bounded accounted path and does not mint authority.
- [ ] Observe actual cgroup counters and process absence after cleanup; retain evidence in the existing recorder. Preserve N1_ONLY isolation/lifecycle regressions touched by the launcher changes.

**Verification:** Local `test_campaign_supervision.py`, `test_campaign_budget.py`, `test_campaign_recovery.py`, `test_campaign_admission.py`, `test_profile.py`, `test_release.py`, `test_service.py`; Linux targeted accounting/lifecycle cases registered in the existing harness/manifest. This early real-host check directly resolves the platform risk rather than deferring it to S8.

**Checkpoint:** Return measured Linux process/cgroup/counter evidence, exact release/config identity and accounting ownership map. Explicitly identify any phase still executing outside that scope.

**Return boundary:** Accept only the enforced work boundary, not statistical execution. No N1/N2/Part A draw dispatch, G5 verdict, result or seal. A host/access blocker returns implementation plus missing evidence without a false Linux PASS.
## S3 — Genuine protected N1 and committed independent G5 decision

**Selected outcome:** A fresh budgeted campaign runs actual N1 once, archives a genuine capture and commits G5's deterministic N1 assessment. PASS reaches N2_READY; FAIL terminates computation. No N2 launch or aggregate PASS is possible in this slice.

**Prerequisites:** Accepted S2 accounting boundary, S1 snapshot/state contract, accepted N1 engine/capture code. A diagnostic release exposes only implemented N1 progression. A future complete release uses a fresh attempt; it does not upgrade this diagnostic campaign.

**Ownership:** S3 executor owns the end-to-end N1 campaign integration, including G5, rather than delegating worker and verifier into independently accepted fragments. Coordinator accepts the checkpoint.

**Files:** `execution/worker.py`, `compute.py`, `evidence.py`, `archive.py`, `signing.py`, `service.py`, `g5.py`, `campaign_protocol.py`, `campaign_store.py`, `client.py`, `runtime.py`; canonical `qualification/checkpoint_plan.py`, `evidence.py`, `journal_snapshot.py`, `policy.py`/`policy_sources.py`; corresponding installed fixtures and `tests/ops/qualification/execution/test_campaign_n1.py`. Preserve `derive_n1_plan` behavior and the N1_ONLY wire path.

**Interfaces:** Implement proposed canonical `derive_checkpoint_plan(campaign_plan: bytes, checkpoint: str, predecessor_receipt: bytes | None) -> bytes`; S3 accepts only checkpoint N1 and no predecessor. Later slices extend this same owner. Add `validate_campaign_checkpoint(context, *, checkpoint, plan_bytes, attestation_bytes, artifacts, snapshot_bytes, current_keys)` in the active G5 adapter, returning a canonical assessment plus output bytes, expected revision and snapshot identity. Canonical evidence reconstruction remains below that adapter. Introduce one closed FULL_E1 checkpoint result/attestation/assessment schema, not a competing N1 statistics implementation. Add G5-only snapshot, member-artifact fetch, private staging and COMMIT_CHECKPOINT_ASSESSMENT operations to the campaign protocol; operator/client ACLs remain separate.

**Behavior:** Service derives N1 inputs from admitted originals and its budget reservation, records one START_INTENT, launches the approved worker, finalizes capture, and attests exactly those archived bytes. Source admission, provider construction, probe, draws, serialization and capture are charged. Worker-local BudgetGuard is a secondary bound supplied with remaining phase limits; calling `from_contract` must not allocate a fresh full campaign allowance. G5 runs as the metered installed qg5 role, fetches actual capture/input members, independently reconstructs LEGALITY/N1 and commits its signed assessment under the service lock. Preserve the N1 cutoff receipt and bind future N2 thresholds distinctly. Only an accepted PASS assessment produces N2_READY; a failed N1 produces a terminal statistical prefix eligible for S6's later FAIL commit.

- [ ] Add one deterministic synthetic-source N1 PASS and one FAIL through actual compute, capture, reconstruction and store; assert exactly one worker and zero N2/Part A workers.
- [ ] Implement the shared checkpoint plan/result/attestation/snapshot protocol and actual producers/consumers together. G5 reads captured bytes, never worker verdicts as authority, and never reruns draws.
- [ ] Connect each accepted N1 lifecycle boundary to S1/S2 accounting. After START_INTENT without finalized capture persist IN_DOUBT and clean up; after capture recover only saved bytes.
- [ ] Persist fixed assessment signing intent/candidate before commit. Commit checks current revision/validity/enrollment/budget atomically; retry exact candidate or receipt without fresh time/signature.
- [ ] Validate N1_ONLY compatibility and return at N2_READY or terminal N1 failure.

**Verification:** `test_campaign_n1.py`, `test_campaign_recovery.py`, `test_worker.py`, `test_capture_archive.py`, `test_service_assessment.py`, `test_checkpoint_validation.py` (last under `tests/ops/qualification/`). Add Linux targeted N1 campaign dispatch/G5/capture recovery cases to the existing harness. Negative cases: altered outcomes, stale snapshot, wrong signer, source substitution, expiry, budget exhaustion in G5 and VOID before commit. Local fake completed output is not a positive campaign test.

**Checkpoint:** Return one genuine N1 capture/assessment trace, exact source/seed preservation evidence, charged G5 trace and no-redraw recovery evidence.

**Return boundary:** No joint N2, Part A, aggregate-result commit or seal. A passing prefix remains CONTINUE, never full PASS.

## S4 — One joint N2/Part B execution and G5 assessment

**Selected outcome:** After a committed N1 PASS, exactly one worker produces FULL at frozen N2 depth and H1/H2 at frozen Part B depth. G5 commits both decisions from that same batch; both PASS reaches PART_A_READY, either FAIL ends computation.

**Prerequisites:** Accepted S3 with an actual N1 assessment receipt and S1/S2 remaining budget. Signed new release enables N1 and joint N2 only. Use fresh campaign attempts for the new release.

**Ownership:** S4 executor owns joint batch, evidence and continuation together; coordinator accepts the result.

**Files:** `execution/compute.py`, `worker.py`, `evidence.py`, `g5.py`, `service.py`, `campaign_store.py`, `campaign_protocol.py`; canonical `checkpoint_plan.py`, `policy.py`, `policy_sources.py`, `evidence.py`, `journal_snapshot.py` in qualification; add `tests/ops/qualification/execution/test_campaign_n2.py` and extend existing semantic/checkpoint tests.

**Interfaces:** Extend the S3 checkpoint producer for `N2` with the exact committed N1 predecessor receipt. Add `run_n2_compute(contract, source, budget)` beside `run_n1_compute`, using existing `stage_request(contract, 'n2', budget.remaining_wall_seconds())`, `_ReplayProvider`, `_run_stage` and `initial_state`. Extend the same worker-result/G5 assessment schema and `validate_campaign_checkpoint` for the joint ordered LEGALITY/N1/N2/PART_B prefix. The service stores one N2 execution identity, not a PART_B execution. Any changed shared schema must be propagated to the installed fixture/manifest producers and earlier stage consumers before accepting the slice.

**Behavior:** Derive populations and addresses from the frozen contract and accepted planner. FULL failure/speed calculations share identical FULL outcomes; H1/H2 exclusively supply Part B. There is no extra pilot outside the engine's original probe, extra speed sample, standalone Part B job or partial-batch decision. Extend canonical policy's presently N1-only partial/NONE shape for a versioned FULL_E1 passing joint prefix. Preserve N1_ONLY rejection of that new continuation. Snapshot, assessment, stage transition and artifact roles must agree on the new prefix.

- [ ] First add the two discriminating synthetic cases: FULL fails while halves pass, and halves fail while FULL passes. Each produces one batch, both decisions, no Part A launch.
- [ ] Wire the existing N2 mechanics through the same supervised capture and independent G5 route as S3, with frozen population counts and predecessor binding.
- [ ] Extend canonical continuation policy and consumers together; reject missing halves, changed order/count/seed, substituted FULL for speed and replayed/stale predecessor.
- [ ] Add joint PASS to PART_A_READY and crash-after-intent/capture recovery cases; stop at that boundary.

A producer-level regression must directly establish the inherited mapping:

```python
from c1_rail.qualification.execution.compute import stage_request

def test_joint_depths_are_from_the_frozen_contract(tmp_path):
    from bundle_fixture import build_bundle
    contract = build_bundle(tmp_path)['contract']
    request = stage_request(contract, 'n2', 1.0)
    assert request.depths == (
        ('FULL', contract.stage_specs['N2'].exact_depth),
        ('H1', contract.stage_specs['PART_B'].exact_depth),
        ('H2', contract.stage_specs['PART_B'].exact_depth),
    )
```

Here `contract` is produced by the existing signed bundle fixture, not a caller-fabricated substitute; the one-second argument tests only request construction, not real execution feasibility.

**Verification:** `test_campaign_n2.py`, `test_campaign_n1.py`, `test_campaign_recovery.py` under execution, plus `tests/ops/qualification/test_semantic_policy.py`, `test_checkpoint_validation.py`, `test_seed_probability_vectors.py`. Retain a targeted genuine Linux joint-batch trace; reuse unchanged host/isolation evidence.

**Checkpoint:** Return the canonical continuation schema and actual batch-to-two-decisions trace, including both asymmetric failure cases.

**Return boundary:** No Part A, aggregate commit or seal. Do not reimplement or retune failure/speed statistics.

## S5 — Genuine Part A, preserved expansion prefix and G5 decision

**Selected outcome:** After the joint PASS receipt, one Part A operation produces initial panels and, exactly when prescribed, appended panels. G5 verifies the captured inventory and reaches FULL_PASS_READY or terminal statistical FAIL.

**Prerequisites:** Accepted S4, actual captured N2 FULL bytes and both passing decisions, remaining campaign allowance sufficient for the configured reservation. A new signed diagnostic release supports all three compute checkpoints; fresh attempt required.

**Ownership:** S5 executor owns engine adaptation, prefix capture and reconstruction; coordinator accepts statistical preservation and lifecycle behavior.

**Files:** `execution/compute.py`, `worker.py`, `evidence.py`, `g5.py`, `service.py`, `campaign_store.py`; canonical `checkpoint_plan.py`, `evidence.py`, `journal_snapshot.py`; inspect `qualification/part_a.py`, `regime.py`, `provider.py`, `replay.py` and adjudicators before edits. Add `tests/ops/qualification/execution/test_campaign_part_a.py`. Engine edits are limited to necessary store-free integration; a numerical behavior discrepancy returns to the coordinator before changing accepted formulas.

**Interfaces:** Add `run_part_a_compute(contract, source, budget, *, n2_full_outcomes)` that adapts the existing `_run_part_a` loop and its request/provider/proof inputs. Extend `derive_checkpoint_plan` for `PART_A`, binding the exact joint predecessor and N2 capture. Extend `validate_campaign_checkpoint` to reconstruct panel-major source-session occurrence inventories, path outcomes, initial-prefix artifact and expansion decision using canonical installed adjudicators.

**Behavior:** Worker and G5 independently derive the same N2 FULL pass rate from captured outcomes. Preserve the disjoint Part A pilot addresses, outer panel seeds, path addresses and source occurrence order, including legitimate duplicate occurrences. Retain the exact original prefix before extending indices `[initial_panels, expanded_panels)`; the final prefix must be byte-identical. Conditional expansion uses inclusive tolerance equality. Apply the final floor and FULL sanity comparison after required expansion. A crash during panels without complete durable capture is IN_DOUBT: no panel resume, replacement pilot or checkpoint rerun. S5 builds this terminal subset; the §2.6 re-execution is a later slice after S5 and before S8, and S5-D1's retained initial prefix is the retained complete record that full-E1 spec §2.6's comparison schema compares.

- [ ] Add engine-adapter boundary tests before wiring: no expansion, required expansion, exact tolerance equality, below-floor failure and above-FULL failure, plus unchanged initial prefix.
- [ ] Trace actual `_run_part_a` inputs and reuse its sampling/append loop; capture the prefix from that computation rather than reconstructing it by another replay.
- [ ] Wire one metered worker invocation and independent G5 reconstruction. Reject omitted/unnecessary expansion, substituted/reordered prefix, altered source occurrences, missing pilot identity and mismatched N2 FULL baseline.
- [ ] Compare float-based compute and exact-Decimal G5 decisions on supported frozen boundary configurations. If parity fails, return an engine-contract conflict; never relax a tolerance or let worker/G5 disagree.
- [ ] Verify interruption during expansion cannot relaunch, and remaining budget exhaustion blocks completion without inventing a statistical failure.

Required prefix assertion in the new adapter/capture test (both byte lists come from one actual run):

```python
assert final_panel_bytes[:len(initial_panel_bytes)] == initial_panel_bytes
assert actual_panel_count == (expanded_panels if expansion_required else initial_panels)
assert part_a_worker_launch_count == 1
```

**Verification:** `test_campaign_part_a.py`, `test_campaign_n2.py`, `test_campaign_recovery.py` under `tests/ops/qualification/execution/`, plus `tests/ops/qualification/test_part_a.py`, `test_regime.py`, `test_evidence_reconstruction.py` and `test_result_adjudication.py` under qualification. Pure boundary tests may use exact outcome vectors; Linux positive/failure campaigns must use actual synthetic market/session sources. If an exact equality cannot be produced economically through market fixtures, retain the arithmetic boundary test separately and do not falsely call it a full-route witness.

**Checkpoint:** Return actual Part A captures, initial/final prefix identities, expansion/no-expansion decisions and parity results. Explain any reduced TEST_ONLY depths distinctly from reference-depth qualification.

**Return boundary:** All compute stages and checkpoint G5 decisions now exist, but no aggregate result authority or seal is claimed.

## S6 — Authenticated full-result construction and atomic commit

**Selected outcome:** G5 constructs an authenticated aggregate from retained captures/assessments; the service atomically commits one complete PASS or an allowed early-failure prefix. Exact retries recover the same receipt. Incomplete PASS, fabricated evidence and VOID-first publication reject.

**Prerequisites:** Accepted S3–S5 captures and committed checkpoint decisions, S1/S2 accounting and current keys. Genuine early-failure fixtures from S3/S4 must remain usable; completion does not require executing later stages after failure.

**Ownership:** S6 executor owns aggregate reconstruction, authentication and service publication; coordinator accepts atomicity/provenance together.

**Files:** Canonical `qualification/evidence.py`, `policy.py`, `policy_sources.py`, `journal_snapshot.py`; `execution/g5.py`, `campaign_protocol.py`, `campaign_store.py`, `service.py`, `client.py`, signing support; add `tests/ops/qualification/execution/test_campaign_result_commit.py`. Do not invoke legacy public result authority.

**Interfaces:** Add canonical `validate_campaign_result(context, result_bytes, *, attestations, artifacts, assessment_receipts, snapshot_bytes, current_keys)` returning verified evidence for service use. Add G5 aggregate entrypoint `authenticate_campaign_result(context, *, attestations, artifacts, assessment_receipts, snapshot_bytes, current_keys, credential_reference)`; its signed candidate is staged privately. Extend the closed G5 protocol with COMMIT_E1_RESULT carrying envelope digest, exact authentication and expected revision; CampaignStore supplies `commit_campaign_result(validated_evidence, authentication_bytes, *, now) -> bytes` and exact retry lookup. Values returned by a pure validator are not caller-issued capability objects.

**Behavior:** Allowed statistical FAIL prefixes are LEGALITY/N1; LEGALITY/N1/N2/PART_B; or all stages. PASS requires all LEGALITY/N1/N2/PART_B/PART_A PASS. Operational abort/uncertainty stays incomplete. Reconstruct all captured memberships and predecessor links, not merely the latest verdict. The precommit snapshot excludes its own receipt. Reserve finalization before taking the assessment snapshot; arrange accounting settlement/publication so legitimate charged verification does not itself invalidate its own snapshot, without overlooking concurrent semantic state changes or VOID. Explicitly test this against the S1 revision contract. The final receipt binds the result/authentication and resulting journal head plus budget settlement.

- [ ] Write genuine all-stage PASS and each legal early FAIL aggregate tests; reject missing/extra/out-of-order stages and successful incomplete prefixes.
- [ ] Implement private artifact staging, exact signing intent and candidate retention under the original allowance. Fresh signing/validation retries are charged; saved receipt retries are historical reads.
- [ ] In one service transaction recheck snapshot/revision, membership, VALID, current approvals/keys and budget, then publish result/authentication/artifact membership and receipt together.
- [ ] Force both VOID/publication orderings with barriers; also lose the response after commit, expire/revoke keys before commit, and exhaust finalization budget. Verify one immutable receipt and truthful current-validity wrappers.

**Verification:** `test_campaign_result_commit.py`, `test_campaign_recovery.py`, existing `test_service_assessment.py`, canonical evidence/policy regressions affected by the new aggregate. Linux targeted real-G5 commit/VOID tests are required before calling the installed publication path accepted; no seal test yet.

**Checkpoint:** Return complete result wire/authentication schemas, exact private/public artifact membership, budget/snapshot ordering explanation and race/retry evidence.

**Return boundary:** A complete committed TEST_ONLY result exists. No seal authority, production qualification or live deployment.
## S7 — Separate seal authority and atomic publication

**Selected outcome:** Only a complete authenticated RESULT_COMMITTED_PASS can obtain a seal from installed qseal. The service publishes one seal receipt atomically against VOID; lost replies recover exact historical bytes and expose current validity.

**Prerequisites:** Accepted S6 complete PASS result and receipt, genuine FAIL/prefix rejection fixtures, S1/S2 finalization allowance and installed signing recovery. A distinct qseal process/UID/credential is required; an in-process mock does not establish separation.

**Ownership:** S7 executor integrates seal authority, installation and publication; coordinator accepts the complete boundary.

**Files:** Add `ops/c1_rail/qualification/execution/seal_service.py`; extend `service.py`, `campaign_store.py`, `campaign_protocol.py`, `client.py`, `runtime.py`, `release_schema.py`, `release.py`, `keys.py`, fixed `deploy/qualification/bootstrap.py` role selection and host role/config/cleanup files. Add `tests/ops/qualification/execution/test_campaign_seal.py`. Inspect legacy seal tests for semantic cases only; legacy public `qualification/seal.py` authority remains retired.

**Interfaces:** Private service-to-qseal SIGN_COMMITTED_PASS request contains exact intent, committed result, result authentication and result receipt. Proposed `sign_committed_pass(intent_bytes, result_bytes, authentication_bytes, receipt_bytes) -> bytes` lives only in the fixed installed qseal process and uses its installed credential. Private CampaignStore `prepare_seal_intent(attempt_id, intent_bytes, *, expected_revision) -> bytes`, `commit_campaign_seal(intent_bytes, signature_bytes, *, now) -> bytes` and exact retry lookup share the existing validity authority. Add a protected read-only client inspection helper returning historical receipt plus current validity/eligibility; consumers must not infer present authorization from offline signature existence.

**Behavior:** Persist fixed intent identity/payload/key/time before signing. Service acquires the same serialization lock as VOID and verifies current complete PASS, exact receipt, current approvals/keys and budget. qseal independently validates scope and committed result; it cannot accept caller-supplied PASS or publish itself. Bound private IPC/signing duration by the remaining reserved phase, retain exact candidate durably, and recheck immediately before publication. A signing failure rolls back publication, not the durable intent. Recovery uses identical candidate/signature or the fixed deterministic signing operation, never fresh time/key/payload. FAIL, incomplete, uncommitted, uncertain, exhausted or VOID campaigns never gain a new seal. Later VOID preserves history but revokes current usability.

- [ ] Add PASS-only eligibility, wrong role/result/domain, altered intent, expired/revoked key and lost-signing-response tests before implementing the service seam.
- [ ] Install qseal with a separate credential/root, fixed source/runtime manifest and bounded IPC. Update real permission probes and cleanup ownership; qseal has no Docker, worker or result-key authority.
- [ ] Implement durable intent/candidate recovery and publication with both forced VOID race orderings. Assert no alternate candidate publication path and exact receipt recovery after later VOID/expiry.
- [ ] Add actual Linux qseal process/UID/signature/cleanup evidence; keep the privileged-qexec trust assumption explicit.

**Verification:** `test_campaign_seal.py`, `test_campaign_result_commit.py`, `test_campaign_recovery.py`, affected installed release/runtime/role-policy tests. Linux focused cases prove credential separation, budget enforcement, signer interruption and actual locked publication. Retain fail/partial rejection without running unnecessary statistical paths.

**Checkpoint:** Return installed signer identity/config, committed PASS-to-seal trace, restart/idempotency evidence and both VOID orderings. Confirm downstream inspection checks current validity.

**Return boundary:** The route is implemented through sealing, still pending S8 integrated acceptance. No production authority, real-account qualification or deployment.

## S8 — Integrated synthetic Linux acceptance and independent combined review

**Selected outcome:** On the exact integrated candidate, one genuine synthetic campaign reaches SEALED_PASS, failure/expansion/recovery/invalidity cases satisfy E01–E12, and independent combined review has no unresolved blocking findings.

**Prerequisites:** Accepted S1–S7 and their exact integrated source/config identities. A disposable supported Ubuntu 24.04 host with the existing privileged harness is available. Hosted execution requires the coordinator's authorized publication/CI route; if unavailable, return the specific host/publication access dependency rather than substituting Windows/unit results.

**Ownership:** S8 executor integrates the acceptance scenarios and reports; coordinator owns the final ACCEPT/REJECT; an independent reviewer examines the combined implementation and evidence. Separate slice acceptance is not full acceptance.

**Files:** Extend the existing `tests/ops/qualification/invariant_manifest.json`, `tests/ops/qualification/execution/lifecycle_model.py`, `scripts/qualification_boundary_verification.py`, `scripts/check_qualification_invariants.py`, `tools/qualification_verification/` fixture/provision/cleanup owners and `.github/workflows/qualification-execution-boundary.yml`. Add `tests/ops/qualification/execution/test_full_campaign_boundary.py` for actual installed-route scenarios. Preserve accepted N1 invariant coverage and the existing two-host workflow; do not create a second acceptance manifest. Keep `qualification_cli.py` read-only; a synthetic campaign driver uses the protected client, not an added legacy execute/seal command.

**Interfaces:** The driver submits only registered bundle/attempt/request identities through the authenticated service and reads receipts/artifacts through its bounded client API. Source fixtures construct actual synthetic market/session inputs; worker/G5/qseal processes produce output and signatures. Manifest entries name exact executable test node IDs and retained evidence. The recorder validates actual reports, critical skips, source/config hashes and cleanup.

- [ ] Establish expected synthetic source verdicts before admission using the frozen engine. Retain source identity; never modify thresholds after observing the campaign. Use reduced signed TEST_ONLY depths for host practicality and separate supported-configuration arithmetic parity tests.
- [ ] Extend existing fixtures/driver to traverse all installed processes. Register E01–E12 below with exact node IDs after tests exist; evidence must include producer, consumer and runtime trace, not just scenario names.
- [ ] Run targeted new Linux cases during development. Freeze the integrated candidate and run the existing full boundary gate on its two disposable hosts; do not repeat unaffected historical jobs just to increase evidence volume.
- [ ] Inspect original recorder/JUnit/invariant outputs, hashes, resource charges, role probes, actual launch histories, result/seal receipts and cleanup. A failed/skipped critical case or missing evidence rejects acceptance.
- [ ] Obtain one independent combined review of security assumptions, unchanged statistical mechanics, actual stage sequence, budget/recovery, publication and retained evidence. Resolve findings and rerun only affected checks plus the final gate when integration changed.
- [ ] Coordinator records ACCEPT or REJECT against the exact candidate and all remaining deployment limitations. No live-performance distribution is part of this synthetic engineering gate.

Existing real-host command sequence (run on the disposable host, not the Windows developer environment):

```bash
sudo bash tools/qualification_verification/provision.sh --manifest-output /tmp/qualification-manifest-path
manifest="$(sudo cat /tmp/qualification-manifest-path)"
host_root="$(dirname "$manifest")"
sudo "$host_root/env/bin/python" -I scripts/fp.py --env "$host_root/env" doctor
sudo "$host_root/env/bin/python" -I scripts/fp.py --env "$host_root/env" python scripts/qualification_boundary_verification.py --test-only --manifest "$manifest"
# The harness/workflow must run owned cleanup even when the command above fails.
sudo /usr/bin/python3 -I tools/qualification_verification/cleanup.py --manifest "$manifest"
```

Use the existing workflow's unconditional cleanup and evidence export when running hosted. A shell operator must preserve the failing exit status while performing cleanup; the illustrative sequence alone is not a replacement recorder or fault-safe shell wrapper.

**Verification:** Actual protected full route plus the canonical invariant gate, successful cleanup, zero critical skips, same candidate on the existing two-host matrix, and closed combined review. Standard local check advisories remain disclosed; they cannot be laundered into a blanket all-gates claim.

**Checkpoint:** Return one indexed evidence bundle and an E01–E12 coverage report with exact paths/job URLs, counts, runtime/source identities and unresolved findings. Coordinator makes the disposition.

**Return boundary:** Stop after synthetic full-E1 ACCEPT or precise REJECT/blocker. No broker order, account funding, production qualification, live launch or automatic deployment. Reassess deployment timing alongside the independent feed/route milestone.

## Combined acceptance coverage

This table maps requirements to implementation owners; the executable manifest remains the acceptance authority.

| Spec case | Required observation | Owning slices |
|---|---|---|
| E01 | Genuine N1 → joint N2/Part B → Part A → G5 aggregate → result receipt → separate seal | S3–S8 |
| E02 | N1 failure stops later workers; authenticated FAIL; no seal | S3, S6–S8 |
| E03 | FULL/half asymmetric failures share one joint batch; no Part A | S4, S6–S8 |
| E04 | Part A floor/sanity failures, sanity after prescribed expansion | S5, S6–S8 |
| E05 | No/required expansion, inclusive tolerance boundary, exact prefix/pilot; invalid equal limits reject | Accepted 1a; S5, S8 |
| E06 | Crash at reservation/intent/run/capture/sign/commit boundaries; actual launch history proves no redraw | S1–S8, each changed boundary |
| E07 | Concurrent duplicates, conflicts and lost replies return one exact operation/receipt | S1, S3–S8; accepted 1b admission |
| E08 | Exhaust compute/capture/G5/seal budgets, outstanding reservations, downtime and reboot uncertainty | S1/S2 and each charged phase, S8 |
| E09 | Fabricated outputs/seeds/prefix/source/image/membership/order reject; actual permissions enforced | S2–S8 |
| E10 | Both forced VOID orderings against dispatch/result/seal; historical receipt has no current authority | S1–S3, S6–S8 |
| E11 | Expiry/revocation and role/domain mismatch prevent new authority; exact historical retry | S2–S8 |
| E12 | Service/G5/qseal restart and cleanup failure preserve uncertainty/history, no late publication | S1–S3, S6–S8 |

Before final review, trace these concrete sequences through the actual producers and persisted state:

1. Fresh budgeted admission → N1 PASS → joint PASS → Part A PASS → authenticated full result → atomic commit → separate seal.
2. Each early statistical failure → no later worker → permitted FAIL prefix → result receipt → seal refusal.
3. START_INTENT → crash without durable capture → IN_DOUBT → owned cleanup → historical access only.
4. CAPTURED → crash → same saved bytes → charged G5 reconstruction → exact assessment receipt, no new draw.
5. G5/signing candidate durable → lost reply → exact candidate or receipt recovery; remaining budget never resets.
6. VOID before publication versus publication before VOID → no new authority in the first ordering, historical-only authority in the second.
7. Admission CPU spent before budget binding → binding includes the original start/charge; no activation of old unmetered dormant rows.


### Artifact-size and revision closure required during implementation

S3 extends the existing bounded plan transport to role-authorized retained-input/capture reads and private G5 candidate writes as needed. Use an immutable object manifest with whole digest/length, fixed bounded chunks, explicit staging/finalize membership and idempotent retries. A partial upload is never a candidate result; a client never receives G5 write permissions. Check the outer encoded frame, not just raw bytes. Reuse the canonical chunk configuration rather than copy another set of limits.

S4/S5 must test the actual new output representation at the supported reference depths and ensure worker output, archive, G5 input and any private candidate transport fit the resolved FULL_E1 profile and frozen memory budget. The plan's 64 MiB cap is not automatically an output cap. New FULL_E1 limits must be explicit, versioned, source-bound and checked end to end; N1_ONLY limits remain unchanged. A representation that cannot fit returns a concrete interface/resource conflict before execution activation, not a silent truncation, threshold change or generic increase. This is functional compatibility testing, not a live performance study.

S1 defines the versioned snapshot/revision rules consumed by S3/S6/S7. Serialize authority-changing work per campaign; reserve the work before obtaining its signing snapshot. Persisted resource observations must remain attributable without allowing a legitimate assessment to bypass a changed stage, validity or signing intent. Specify the exact distinction between authority revision, accounting observations and settlement in the new schema, then test budget settlement plus publication as one serialized action. N1 snapshot semantics remain unchanged. The final result cannot contain its own receipt or future seal costs; receipts bind subsequent finalization charges, and every later authority action checks the current ledger. No cyclic digest or uncharged finalization is allowed.

## Copyable delegation instruction

Give each future agent this whole plan and the governing specification, then send this instruction with the selected ID and an actual predecessor reference filled in by the coordinator:

> Implement only slice S1 (replace with the assigned slice ID) from `docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md`. Start from the coordinator-provided accepted predecessor commit/snapshot, preserving its changes. Read AGENTS.md, the common execution contract, your slice and the linked specification. Use the checkout launcher. Deliver the selected observable outcome, actual verification records and exact source identity; return at the slice boundary or a concrete prerequisite/scope conflict. Do not continue into another slice, alter statistical policy, use legacy execution, publish remotely or perform live/account actions unless separately included in this assignment. The coordinator owns combined acceptance.

The coordinator supplies the real predecessor reference and any authorized commit/PR action in the assignment; an agent must never substitute an invented SHA. For a reviewer, attach the returned changed range/snapshot, governing slice, actual records and known limitations. For S8, request combined review rather than another duplicate per-module review.

## Progress ledger and present disposition

| Item | State at plan delivery |
|---|---|
| Protected N1 foundation | ACCEPTED PR425 baseline |
| Task 1a canonical campaign planning | ACCEPTED local implementation |
| Task 1b dormant admission/transport | ACCEPTED local implementation |
| S1 | ACCEPTED LOCAL persisted semantics after recovery repair; Linux enforcement remains S2 |
| S2–S8 | NOT STARTED |
| Full synthetic E1 acceptance | INCOMPLETE |
| Feed/API/demo access | None available per operator; not a synthetic E1 prerequisite |
| Live performance characterization | Collected during a later authorized bounded rollout; no mature-distribution entry gate |

This is a planning-only deliverable. It authorizes no execution by itself. Each assigned implementation agent receives the selected slice and accepted predecessor, while the coordinator retains integration and full acceptance. No new runtime source, test implementation, commit, PR, Linux run or account action is performed by drafting this plan.
### Planning validation — 2026-09-18

Validated from the isolated checkout at base `1e4928360b95812b04725dc1e8da97709d670ff4` plus accepted Task 1a/1b source and the documentation edits. `pwsh -NoProfile -File ./fp.ps1 doctor` passed with operations Python 3.13.2 (`C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`), 62 matching locked packages. A temporary document-check script run with `pwsh -NoProfile -File ./fp.ps1 python <temporary-script-path>` applied the writing-plans validator to each of the eight extracted handoffs: all eight passed. It also checked E01–E12 coverage, relative links, whitespace, Python example syntax and SHA256 equality of all 13 accepted implementation/test files against the final Task 1b snapshot: PASS. The temporary script was removed; this was a documentation check, not a pytest or Linux verification record.

Coordinator self-review traced admission/accounting, N1 and joint continuation, Part A prefix/parity, G5 snapshot/candidate transport, result publication and separate sealing through the named owners. Explicit obligations include fresh executable attempts, large captured-artifact transport and accounting/publication revision consistency. Those are implementation requirements, not claimed working interfaces. No runtime suite was rerun and no implementation agent was dispatched for this planning-only request. `git diff --check` passed.
### Coordinator recovery closure — 2026-09-19 UTC

Accepted Task 1a/1b recovered from archived tool history; all 13 implementation/test SHA-256 values match the accepted source identities. Base remains `1e4928360b95812b04725dc1e8da97709d670ff4`. Source-set identity: `5cee6b6aad3559ec46c3694f3713959bca51bbd94fe6f3ebd84fc64ce299d91c`. Fresh regression record `20260919T010503Z-d08fafc388e1`: 182 passed, zero skips; fresh check record `20260919T011143Z-78dca2688769`: success with three evidence-store skips and existing advisories. Both records have complete capture, stable source and zero verification exit. Original verification directories were not recovered; archived extracts are historical evidence, and the fresh complete records are retained in the recovery packet. Documentation was recovered from archived edits and the operator-supplied plan; only baseline pointers and this recovery closure are new. S1 is READY for a separately assigned executor; S1–S8 remain unimplemented by this recovery. Full synthetic E1 remains incomplete.

### S1 executor return — 2026-09-19 UTC

S1 is implemented and locally verified, **delivered for coordinator review, not accepted by the executor**. The task **Coordinate protected E1 execution** owns integration, independent review and acceptance. S2 was not started.

Isolated checkout: `C:/Users/joshu/.codex/worktrees/full-e1-s1-budget/multi_firm_operations`, detached at `1e4928360b95812b04725dc1e8da97709d670ff4` with the exact hash-verified Task 1a/1b recovery overlay. No commit, push, PR, merge, deployment, qualification launch, actual signing/publication or statistical-policy change.

One private provisional admission and immutable budget/phase configuration now persist in ExecutionStore's existing database and validity authority. Additive v6 is installed transactionally on first metered intent after exact v5 validation; historical v4/v5 and dormant v2 records retain their meanings. Durable work reservations, exact settlement, conservative unknown-counter charges, clock/memory/OOM terminal facts, recovery before cleanup, immutable capture/signing candidate custody, accounting versus authority revisions, and VOID ordering are implemented. No dormant receipt can be activated or retroactively charged.

Doctor passed with Python 3.13.2 at `C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`, 62 locked packages. Final required five-file pytest selection: **137 passed, zero skips**, 161.24 seconds, record `.cache/fp-verification/20260919T022827Z-a490deace717/record.json`. Final `./fp.ps1 check`: exit zero, record `.cache/fp-verification/20260919T022825Z-2e000d635f50/record.json`; 72 evidence-store tests with three existing skips, plus existing absent Pine/data/heavy-artifact, weak-date and duplicate-label advisories. Both records closed with stable source, complete capture, zero command/verification exits and no capture/report errors. `git diff --check` passed. This ledger update follows recorder closure; runtime/test bytes match both records.

Exact interfaces, closed schemas, acyclic signing/revision rules, failed development records, migration/rollback limitations and source inventory are preserved outside the disposable checkout at `C:/Users/joshu/multi_firm_operations/recovery/full-e1-s1-20260919/README.md`. Its manifest and SHA256SUMS bind the final snapshot. Trusted observations here are simulated; S2 and later slices still owe installed supervision, genuine capture/signing/publication integration and real Linux evidence. Full E1 acceptance remains INCOMPLETE.

### S1 coordinator recovery repair closure — 2026-09-19 UTC

The coordinator implemented the two review findings under the user's direct assignment. Already-settled recovery now observes fresh boot/time/resource facts without replacing the immutable charge. Fixed-intent signing recovery uses an explicitly linked, separately charged retry reservation; it preserves the original payload/key/time and prepared authority token while retaining terminal budget/VOID checks. First linked retry emits logical snapshot v2, preserving v1 history; database v6 is unchanged.

Independent code review ACCEPT at the exact final runtime/test hashes; no blocking findings remain. Required five-file selection: 166 passed, zero skips, completed record 20260919T025423Z-77702de7e430. Standard check: exit zero, completed record 20260919T025445Z-61f40acba8e7; 72 evidence-store cases, three pre-existing skips and existing artifact/date/session advisories. Both records have stable source, complete capture and zero command/verification exits. This ledger update follows recorder closure; runtime/test sources are unchanged.

Coordinator disposition: ACCEPT for local S1 persisted semantics only. Repaired source and all development/final evidence are preserved at C:/Users/joshu/multi_firm_operations/recovery/full-e1-s1-repaired-20260919/README.md. The old disposable S1 checkout disappeared; this repair restored its exact checksummed return into full-e1-s1-recovery-fixes at the original merge baseline. No S2 implementation, OS enforcement, actual signing/publication, remote action, merge, deployment or account action. Full E1 remains incomplete. Future assignments must use the repaired packet, not the superseded S1 return.


## S2 coordinator clarification: attributed resource scope (2026-09-19)

The campaign cap covers attributed process/cgroup resources, not total-machine incremental costs. Include all campaign controllers/guardians, launch clients, workers, descendants and role helpers, and campaign-specific shared-qexec authentication, admission, source proof, planning, serialization, custody, reconstruction and finalization. Include every CPU/memory cost reported by the selected scope without subtraction. Ordinary shared dockerd/system-manager and host kernel/background costs outside that scope are excluded. Only fixed bounded lifecycle requests may use this exclusion: no image building, archive processing or campaign computation may be moved into excluded infrastructure. Platform waits, queueing and downtime consume the original BOOTTIME deadline.

The diagnostic v3 candidate binds this interpretation in canonical `CAMPAIGN_RESOURCE_SCOPE` and its installed profile identity. Its proposed CPU charge is measured final payload cgroup usage plus the entire immutable installed orchestration bound, reserved together before work. A persistent host parent conservatively shares MemoryMax across all included campaigns/controllers, with swap disabled; its peak/OOM observations are never reset between works. Cross-campaign interference and group OOM can invalidate every attempt on that host. This is deliberately conservative and does not establish a whole-host bound. Neither this clarification nor a configured bound proves Linux enforcement; all original fail-closed authority, no-redraw and immutable-charge rules remain. N1_ONLY and accepted S1 history remain unchanged.

The local S2 candidate is INCOMPLETE / NOT ACCEPTED. Identified lifetime-accounting and crash-after-control-claim gaps require follow-up before executable activation. Real Linux evidence is a separate missing prerequisite. No S3 dispatch is authorized.

### S2 local candidate return — 2026-09-19, INCOMPLETE / NOT ACCEPTED

S2 is delivered for coordinator review as a frozen local candidate, not accepted and not executable activation. Accepted S1 predecessor remains 430fc72186a0e642c8811be17d459fd87cbf7533. The coordinator requested the bounded return after the durable recovery claim-before-observation fix. Demonstrated remaining defects include private scheduler construction before reservation, interrupted recovery claims not gating positive authority, and unmetered post-admission cancellation authentication. Original-deadline coverage before guardian timer installation is also unresolved. No Linux host ran; that evidence prerequisite is separate from source defects. S3-S8 remain NOT STARTED.

Final required seven-file selection: 197 passed, zero skips, record 20260919T044917Z-4ae4f65a973d. Affected ownership/host/invariant/recorder/model selection: 214 passed, three Windows/POSIX skips, record 20260919T044938Z-307fff6cf94a. Standard check FAILED at the unchanged overdue STATE.md weekly deadline (2026-09-18 versus current 2026-09-19 ET), record 20260919T044939Z-219eec8aef71; earlier 72 evidence-store cases completed with three existing skips. All three final records have stable source and complete capture; suite exits 0, gate exits 1. Interpreter: C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe, Python 3.13.2. git diff --check passed. This ledger entry follows recorder closure; runtime/test/config bytes remain exactly those tested.

Complete source/config/docs, all failed and passing development evidence, final hashes, explicit blockers, actual interfaces and source-defect reproduction are preserved at C:/Users/joshu/multi_firm_operations/recovery/full-e1-s2-20260919/README.md. A retained reproduction shows BOUND VALID surviving a claimed/interrupted recovery and allowing a new reservation. No statistical draw, actual signing, account action, commit, push, PR, publication or deployment occurred. Coordinator owns independent review, further repair selection and acceptance.


### S2-R1 executor return — 2026-09-19 UTC

Bounded interrupted-recovery authority/completion repair is delivered for coordinator review, not self-accepted. Snapshot/v4 atomically binds a recovery claim to its temporary authority barrier, ephemeral owner and durable observations/completion. A spent completed owner encountering a new active recovery need commits a continuation-required refusal; historical replay cannot clear it. Lost ownership remains safely blocked, without a new allowance. Immutable settlement, terminal facts, VOID and fixed-intent tokens are preserved.

The coordinator-authorized physical-dispatch extension commits a pending marker before the OS effect, then rechecks authority and a fresh clock under the serialized start gate. The bounded system-manager acknowledgement is a queued-job reply, independent of guardian qualification/readiness. Client completion is awaited outside the store lock with spawn time subtracted from the original deadline; the guardian waits only after its existing absolute timer is installed. Docker uses its bounded start response. Only the live owner can acknowledge its own marker. Lost acknowledgement or persistent post-effect database failures, including failed recovery, remain blocked after reopen. This introduces no process, continuation or resource grant.

Final required seven-file selection: **272 passed, zero skips**, 209.62 seconds, record `20260919T053710Z-bb97fb5412e6`. Final affected journal-snapshot/lifecycle-model/artifact selection: **41 passed, zero skips**, 66.48 seconds, record `20260919T053709Z-4451d9666c45`. Final `fp.ps1 check` FAILED on the unchanged overdue `STATE.md:74` weekly deadline (2026-09-18 versus 2026-09-19 ET), record `20260919T053710Z-c203c5457d90`; its 72 evidence-store cases completed with three existing skips and existing advisories. All three records closed with stable source, complete capture and no capture/report errors. Their tested source fingerprint is `49187f49137a2674fe078697e7e9c37c3e4051aeabd1b63883a147b53afaa6df`. Commands used this checkout's `fp.ps1` with validated Python 3.13.2 at `C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`; doctor passed. This ledger append follows recorder closure; runtime/test/config bytes remain unchanged. Packet assembly also requires `git diff --check` success.

Accepted S1 remains `430fc72186a0e642c8811be17d459fd87cbf7533`. All 2,076 frozen S2 source hashes matched before repair. The separate return packet at `C:/Users/joshu/multi_firm_operations/recovery/full-e1-s2-r1-20260919/README.md` preserves complete source, repair differences, exact interfaces/limitations, final records and all failed/passing R1 development evidence; SHA256SUMS and manifest bind the return. The original 316-file S2 packet is verified unchanged. Coordinator owns independent R1 review and combined acceptance.

**Overall S2 remains INCOMPLETE / NOT ACCEPTED.** Scheduler construction before lifetime reservation, post-admission VOID authentication accounting and pre-timer/bootstrap deadline coverage remain open, as does all real Linux enforcement evidence. No Linux host run, installed image/release identity, actual signing/draw, commit, push, PR, activation, deployment, publication, paid provisioning or S3 dispatch occurred.

## Successor coordinator checkpoint — S2-R2 funding interface (2026-09-19)

Overall S2 remains INCOMPLETE / NOT ACCEPTED; S3-S8 remain blocked. Current checkout HEAD is c77aac476127a31e58ede2c1c0ff03e6406474ce. Remote PR429 matches that head and is open; the repository owner marked it ready for review at 2026-09-19T09:43:40Z. No PR state, publication or merge action was taken by this coordinator. PR428 remains open at 6b860639f6f49b35e4f89facfbfde5bea20394ff.

The exact f95837c..6b86063 base delta is preserved as uncommitted S2 changes: missing-plan rejection, decreasing memory-peak uncertainty, their recovery tests and the operator-attested STATE missed-week update. Independent read-only review found no actionable regression. Recovery verification 20260919T100454Z-c75cc600d7a0 passed 68 tests with zero skips. Standard check 20260919T101422Z-44f9ee67e1cf passed, including 72 evidence-store cases with three existing skips and disclosed repository advisories. Both records completed with command/verification exits zero, stable source, complete capture and no capture/report errors. Interpreter: C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe, Python 3.13.2, 62 locked packages, after this checkout's doctor. The prior published-head STATE failure remains historical failed evidence; the imported operator-owned update resolves the current local gate truthfully. This ledger append is after recorder closure.

R2 is not implemented. The proposed warm-service scheduler removes per-request constructor/import work but does not fund CampaignStore._budget/_save_budget full-history validation and serialization before reservation commit. Independent contract review confirmed that a wire/history byte cap alone does not close this accounting gap. New test_campaign_scheduler.py retains 15 intentionally failing regressions in source-stable, capture-complete record 20260919T100953Z-42977cf0e724 (both exits 1; JUnit failure report expected). No R2 runtime changes were made.

Concrete design decision pending: introduce a canonical compact funding intent inside the same ExecutionStore authority, with strict database v7 and a fresh versioned installed diagnostic profile. Atomically reserve the full existing phase allowance and one-use owner before full-history work; pending preparation blocks all new authority. Funded materialization transfers the same reservation into normal history without double charge. Lost owner retains the reservation/barrier without refund or restart continuation. Preserve old snapshots as historical and refuse stale current exports; maintain negative VOID/terminal ordering. This requires coordinated store, snapshot/export, profile, service and all authority-gate changes, not just scheduler relocation. A reviewed detailed proposal and evidence inventory are at C:/Users/joshu/multi_firm_operations/tmp/full-e1-coordinator-20260919/r2-return.md. Runtime edits are paused at this structural interface decision; the next handoff must resolve and accept the revised contract before implementation.

The existing two-host Ubuntu workflow currently runs --test-only N1 coverage, never --s2. No S2 Linux run, installed release hash or image digest exists. Existing seven S2 tests require expanded evidence; the sequential-role test also confuses lexical work order with newest work, and the downtime test does not establish independent termination by deadline. R3 authentication accounting and R4 pre-bootstrap deadline remain open. No statistical execution, provisioning, deployment, account action, commit or push occurred.

### Coordinator acceptance — S2-R2a persistence, 2026-09-19

R2a is locally ACCEPTED as the bounded persistence prerequisite only. Delivered strict DBv7, fresh execution profile/v4 + budget profile/v3 + snapshot/v5, bounded compact funding claims, live-owner atomic materialization without a second debit, pending authority/export barriers, negative/recovery preservation, and integrity that refuses missing/stale authority rather than rebuilding it. Existing release schemas reject this profile; runtime activation is not delivered. Independent reviewer closed all actionable findings, including predecessor validation and missing materialized-intent coverage.

Tested source: c77aac476127a31e58ede2c1c0ff03e6406474ce plus preserved S1 overlay and uncommitted R2a, fingerprint 0ec013d29be006dadbcbc72f82b7173535b4b2f3255ad831f0a49f58c1adfd3f. Coordinator independently compared all 2,088 captured file hashes with actual checkout bytes: zero mismatches. Python 3.13.2 at C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe, 62 locked packages, validated with this checkout's fp.ps1 doctor.

Final source-bound records under .cache/fp-verification: 20260919T110352Z-59d6fa6a497e (funding47 passed, zero skips); 20260919T110450Z-2380d5ed6980 (funding/budget/recovery/supervision257 passed, zero skips); 20260919T110920Z-a2365379e666 (fp.ps1 check passed, evidence-store72 cases with3 existing skips and disclosed advisory/absent-data warnings). All completed with command/verification exit0, stable source, complete capture and no capture/report errors. git diff --check passed. Earlier375-case compatibility run is retained separately; intentionally aborted110150 run is not passing evidence. This acceptance paragraph is the only candidate change after final verification; runtime/test/config bytes remain as tested.

Full local return: C:/Users/joshu/multi_firm_operations/tmp/full-e1-coordinator-20260919/r2a-return.md. R2b's15 prospective scheduler tests remain explicitly red; no claim that all tests pass. No real Linux run, installed release activation, commit/push or production action. Overall R2 and S2 remain INCOMPLETE / NOT ACCEPTED.

Latest user instruction: STOP AT R2a. R2b is UNASSIGNED and must not begin in this task continuation; R3/R4 and S3-S8 remain outside the stopping boundary. Any later R2b work requires a fresh assignment using the accepted predecessor and explicit startup/recovery funding interfaces.

### S2-R2b executor return — 2026-09-19 UTC

Assignment: [S2-R2b handoff](../../briefs/handoffs/2026-09-19-full-e1-s2-r2b-warm-service-scheduler.md) (dispatched by the B0 decision). Predecessor `codex/full-e1-s2-supervision@ab0ea52` (the handoff named `8aa5753`; two newer commits on that branch — the `main@06dc814` merge and the P1 terminal-clock-overlay / P2 `scheduler_fixture.py` fix — were read and built on). Executor: Claude Code, local Windows checkout, branch `claude/s2-r2b-completion-e740d3` (the handoff's default `codex/…` name was not used because the executor is not Codex). This entry is a return, not an acceptance; the R2a stopping line above is unchanged (the coordinator rewrites the ledger disposition on acceptance).

Changed interfaces: route schema literal `qualification_campaign_schedule_request/v1` (unchanged R2a parser, now routed by `ExecutionService.handle_request` only for `SO_PEERCRED` uid == `service_uid`, framed at ≤1024 bytes in `_serve_connection`, and only under a startup-cached `schedule_eligible`); release literal `qualification_execution_release/v4` (`release_schema.EXECUTABLE_DIAGNOSTIC_RELEASE`: execution profile/v4 + budget profile/v3 + snapshot/v5, `FULL_E1`/`TEST_ONLY`/`dispatch_enabled=False`/`production_execution=False`; every older literal still refuses profile/v4 with the persistence-only message); split tail `campaign_supervisor.launch_prepared_campaign_work(context, reservation_bytes, enrollment_bytes)` (consumes a materialized intent without a second START_OWNER claim; `run_campaign_work` keeps admission's prepare-and-launch route through the shared `_launch`); owned timer `campaign_supervisor.owned_boottime_deadline(deadline_ns)` (retired in `finally`; armed only around the funded launch tail); `service.schedule_campaign_probe` deleted; `tests/integration/qualification_boundary/campaign_driver.py` deleted; private-route harness transport `tests/integration/qualification_boundary/private_route.py` (`schedule_frame`, `exchange`, `forked_exchange`) used by `Boundary.schedule`; `raw_request` refuses the schedule schema; the diagnostic Linux fixture now installs the funded revision. `recover_service` reports `FUNDING_PENDING` for pending funded attempts and never materializes (restart ownership: see the addendum below).

Producer chain: claim → (no token: compact status, no effect) → materialize → `launch_prepared_campaign_work`; no `reserve_work` on the route; duplicates get `scheduler_status`; `controller_cpu_guard` (1 s / 10 s) wraps the whole active tail and consumes START_OWNER's existing allowance; no allowance, ceiling, `campaign_protocol.permitted` or R2 contract text changed.

Records (this checkout's `fp.ps1`, Python 3.13.2 at `tmp/ops-env`, 62 locked packages, doctor passed): `20260919T131055Z-8a504bc2c299` (byte-exact recovered file + funding suite: 15 failed / 50 passed, zero skips — the historical 15 reproduced); `20260919T131148Z-60ae0555939a` (new R2a funding-only baseline: 50 passed); `20260919T131205Z-748de6de7e69` (`tests/ops/qualification/execution --collect-only`: 625 tests, zero collection errors); `20260919T132207Z-fb62e6b1b61e` (adapted `test_campaign_scheduler.py`: 30 passed, zero skips; 15 → 30 = the original 15 plus crash-after-materialization, six refusal cases, concurrent duplicates, non-eligible release, oversize request, first-request import fault, timer success/duplicate, launch-tail identity, restart reporting, transport child); `20260919T132506Z-aa361d03cb40` (Step 2.7 first selection, `--workers 2`, nine files: 369 passed, zero skips); `20260919T143716Z-64219b68ad35` (Step 2.7 second selection: 73 passed, 1 pre-existing environmental skip `test_child_must_remain_under_evidence_root[symlink]`; the isolation bridge is deselected under an explicit selection by `tests/ops/conftest.py`); `20260919T133345Z-26d94b7846bb` (`tests/ops` whole directory so the bridge executes: 2840 passed, 18 skipped, 1 failed = the bridge itself, whose `-n 0` child timed out at its 1800 s limit at 72% with zero failures on this Windows host); `20260919T140712Z-55221d5abab6` (the bridge child's exact selection `tests/ops/qualification tests/ops/test_phase3_provenance_acceptance.py`, `--workers 2`: 1442 passed, 1 pre-existing Linux-only skip, zero failures; the bridge's junit assertions re-applied to this report hold — six signed composition cases, provenance counts 1/4/8, none skipped); `20260919T143609Z-3c041c65d96c` (`fp.ps1 check`: exit 0). `git diff --check` clean. All records `source_stable=true`, `capture_complete=true`.

Linux status: **Linux acceptance pending** — no enrolled host in this session. Not run: the seven registered S2 node IDs plus the two new cases `test_s2_private_route_is_service_peer_only_and_bounded_in_framing` and `test_s2_warm_service_starts_one_guardian_per_work_with_no_scheduler_unit`, and `scripts/qualification_boundary_verification.py --s2`. Windows results are simulated-adapter evidence only.

Limitations / concerns: (1) the R2 contract's sentence "that module is retained outside this PR's tree (uncommitted)" (`2026-09-19-full-e1-s2-r2-funded-scheduler.md`) is now stale and was not edited (forbidden surface); (2) restart ownership for funded attempts — RULED, see the addendum below; (3) R3 (`service.py` post-admission VOID unmetered) and R4 (deadline before guardian bootstrap) untouched; (4) the second Step 2.7 selection carries one pre-existing environmental skip (`test_child_must_remain_under_evidence_root[symlink]`: Windows cannot create test symlinks), and `test_qualification_isolation.py` only executes under an ancestor-directory selection (`tests/ops/conftest.py`), so it was proven by a `tests/ops` run rather than the handoff's literal file list.

#### R2b addendum — operator ruling on restart ownership, 2026-09-19 UTC

Operator ruled that funded work interrupted by a service restart is auto-recovered, not left for manual disposition. `recover_service` under an execution-capable installation now gives materialized funded works the same bounded per-work `recover_campaign_work` restart path v2-profile attempts already had (durable uncertainty/no-redraw before cleanup; a spent RECOVERY_OWNER on a later restart marks continuation required exactly as for v2). A pending one-use intent is still reported as `FUNDING_PENDING` and never materialized — its work is not in the snapshot, so the loop cannot touch it — and a persistence-only (v3) installation still resumes nothing. The `FUNDING_NO_RESTART_OWNERSHIP` label from the first return is withdrawn. Note for the reviewer: the first return's manual-disposition posture would have failed the registered S2 cases `test_s2_guardian_death_recovers_before_cleanup` and `test_s2_original_deadline_survives_service_downtime`, which assert `IN_DOUBT` after `restart()`; the ruling is also what those invariants require. Records: `20260919T154607Z-68b9370300f9` (Step 2.7 first selection re-run on the ruled bytes, `--workers 2`: 371 passed, zero skips — the 369 plus the two restart cases replacing the withdrawn one); `git diff --check` clean.

### Coordinator acceptance — S2-R2b funded scheduler integration, 2026-09-19

R2b is ACCEPTED as the funded scheduler integration only (operator ruling 2026-09-19, [PR #433](https://github.com/Joshua-Asante/first-passage/pull/433) at its final head, base `main@ae58ad6`). Accepted: the closed service-identity private route funded by `claim_scheduler_bootstrap` before any construction; `launch_prepared_campaign_work` consuming a materialized intent without a second START_OWNER; the execution-capable release `qualification_execution_release/v4`; the owned deadline timer; restart auto-recovery of interrupted funded work (`e0ef70c`); the forked harness transport replacing the per-request scheduler. Local records as listed in the executor return above; CI green on the final head.

Scope of the acceptance: the successful S2 Linux evidence (run 35460338493, 9/9, record `715817af73db4a2994591333cbf82d37`) was produced on the stacked [PR #434](https://github.com/Joshua-Asante/first-passage/pull/434), which additionally carries six pre-existing S2 host-side fixes (`campaign_host.py`, `container_ownership.py`, `campaign_supervisor.py`, `campaign_store.py`) and the S2 CI job; on #433's bytes alone S2 host enrollment does not succeed. That evidence therefore accepts nothing here beyond the integration. **Overall S2 remains INCOMPLETE / NOT ACCEPTED**: #434's fixes await their own review, R3 (post-admission VOID metering) and R4 (pre-bootstrap absolute deadline) remain open, no installed-release activation on a real host has been authorized, and no statistical dispatch exists. The R2a stopping line above is superseded for R2b only by this acceptance; R3/R4 and S3–S8 stay stopped.
#### S2 CI job evidence — 2026-09-19 UTC (PR #434, stacked on #433)

`qualification_boundary_verification.py --s2` on one fresh hosted `ubuntu-24.04` host, Actions run 35460338493 at `77dee89`: **9 passed / 0 failed / 0 skipped** (the seven registered S2 node IDs plus `test_s2_private_route_is_service_peer_only_and_bounded_in_framing` and `test_s2_warm_service_starts_one_guardian_per_work_with_no_scheduler_unit`). Record `715817af73db4a2994591333cbf82d37`: exit 0/0, `source_stable=true`, `capture_complete=true`, `invariants.json passed=true`, owned cleanup `ok=true`; N1 boundary on the same head green on both hosts (run 35460340344). Reaching it required six pre-existing S2 host-side fixes in `tools/qualification_verification/{campaign_host,container_ownership}.py`, `campaign_supervisor.py` and `campaign_store.py` (recorded on PR #434), one guardian polling-cost fix and one Linux-case settlement race fix. This is diagnostic evidence for the coordinator (`qualification_acceptance=coordinator_review_required`), not S2 acceptance; the R2b return's "Linux acceptance pending" is dischargeable by this record on acceptance of #434.

#### Coordinator acceptance — S2 host-side fixes (PR #434), 2026-09-19

Operator accepted all six pre-existing S2 host fixes carried by [PR #434](https://github.com/Joshua-Asante/first-passage/pull/434), including the two that change what the system promises: (3) the common slice no longer asserts `memory.oom.group=1` — systemd rewrites that attribute on every realization and sets it only for `OOMPolicy=kill` service/scope units, so the invariant was unsatisfiable; group OOM termination is carried by the guardian unit's `OOMPolicy=kill` and the payload's `BindsTo` interlock, and the OOM case still reads `memory.events` on the parent slice; (5) the qexec polkit rule allows `manage-units` when no `unit` detail is present, because `StartTransientUnit` is authorized by systemd's generic check with no details — a transient start cannot be prefix-bound by polkit; this stays inside the recorded trust model (qexec root-equivalent through the Docker daemon; `bootstrap.py`'s `campaign_control` still hard-checks the fixed command prefix) and is now a standing S2 trust fact recorded in the harness README. The S2 CI workflow is diagnostic evidence, not a required check; overall S2 remains INCOMPLETE / NOT ACCEPTED (R3/R4 open, no activation authorized).

### Coordinator checkpoint — S2 enforcement gaps (G1/G2), 2026-09-19/20

After PR #433/#434 merged at `main@f2606b0`, the operator listed the remaining sequence (close five S2 enforcement gaps → accept S2 as an integrated boundary → S3–S8) and the coordinator split the five gaps into two parallel packets on disjoint files: [S2-G1](../../briefs/handoffs/2026-09-19-full-e1-s2-g1-supervisor-enforcement.md) (kernel-bounded payload CPU via `CPUQuotaPerSecUSec` × `RuntimeMaxUSec` on the payload slice; absolute BOOTTIME deadline on the guardian argv armed in `bootstrap.py` before any campaign import; identity-gated completion with a SIGUSR1 start/resume handshake) and [S2-G2](../../briefs/handoffs/2026-09-19-full-e1-s2-g2-service-metering.md) (post-admission VOID signature verification only inside a durably charged one-use controller operation; a ruled pending-cancellation barrier on new positive authority; exact `SUBMIT_E1` retry resumes a structurally absent `RESERVED` admission and restart never spends a recovery slot on it). Integration branch `claude/s2-enforcement-gaps-fab5e6`.

**G2 ACCEPTED as a component** at `d60c242` (code head `66fed05`, fast-forwarded into the integration branch): no versioned schema change (charges/refusals are `full_campaign_objects` rows folded into the funding projection), no G1 file touched. Windows records (ops-env Python 3.13.2): `20260919T232116Z-6645aa5de496` 406 passed / 0 skipped; `20260919T232125Z-7280036e3c59` 73 passed + the known Windows symlink skip; `20260919T220049Z-1896aa0e2ea8` 1475 passed + the Linux-only skip; `check` `20260919T214929Z-4d71d35741b9` exit 0; junit totals verified by the coordinator. Linux: its three new nodes green on runs 35472053638 / 35473241020 / 35474214547 (3/3 each, cleanup ok). Coordinator rulings: barrier scoped to admitted campaigns in `_check_budget`, unconditional on `reserve_work`/`claim_scheduler_bootstrap` (an unscoped barrier would deadlock the admission guardian, which binds before it authenticates a pre-admission body); pre-admission refusals retained as `void_admission_refusal_*` and the body cleared without failing admission; expired unstarted admissions terminalised at restart through the ownerless negative path. G2's root-cause analysis of the hung pre-existing cases on its branch (guardian raises in `_run_probe`'s unguarded post-inspect reads → self-recovery → `cleanup` SIGKILLs the guardian itself before `_complete_recovery`, spending the one-use slot) was credited and handed to G1.

**G1 IN PROGRESS, NOT ACCEPTED** — branch `claude/s2-g1-supervisor-enforcement` @ `ddf76c2`. Linux runs: 35469217005 (e42d52f) 3/12 — payload slice `cpu.max` not realized when the guardian looked; 35472701398 (2f51248) 0/12 — every admission hung (orphaned runtime methods from the host repair); 35476561750 (ddf76c2, after restoring the methods and closing the self-recovery race + unguarded reads) **9/12 in 1415 s**: the deadline-before-bootstrap case and eight pre-existing cases pass; failing: `test_s2_payload_cpu_is_kernel_bounded_without_guardian` (assertion on the measured bound), `test_s2_probe_that_exits_before_observation_never_completes` (`bounded Docker lifecycle operation failed` while the host kills the container), `test_s2_shared_memory_oom_is_retained_last` (now ends `IN_DOUBT` rather than `BUDGET_*`). G1's interim return (branch head `efd91c4`, §7 of its packet) reports all relayed items done in code — inspect→read gap tolerated, guardian self-failure path without self-kill or a stranded slot, RESERVED slot guard in `recover_campaign_work`, the two R2b nodes registered (twelve S2 nodes), the `warm_service` unit-GC race fixed, handshake helpers exposed for S3 — plus Windows-green, not host-verified repairs for the three run-3 failures (Windows first selection 383 passed / 0 skips, record `20260919T233631Z-74519c578520`; `check` rc 0). Run 4 on `efd91c4` was dispatched at wrap-up as Actions run 35478031666. Successor's first move: read that run; if twelve green, merge G1 into the integration branch (expect a `tests/ops/qualification/invariant_manifest.json` union conflict with G2's three nodes).

**Independent review of PR #434's six host fixes (owed since merge):** 0 BLOCKING / 5 ADVISORY / 6 NOTE, checked against systemd v255 and Linux v6.8 sources (note in the coordinator's session scratchpad, to be folded into the integration PR). Corrections this entry makes: (A2) the head-bound green S2 run for #434 is **35464802898 at `cf4c6d8`** (9 passed in 548 s, exit 0, source_stable), not only 35460338493 at `77dee89`; (A1) the group-OOM statement in the S2 host-fix acceptance overstates — with `memory.oom.group=1` set only on the guardian unit, a payload OOM under Docker's delegated scope is a single-process kill, and the guardian's poll loop does not read `memory.events`; authority still fails closed at settlement, but "stop on OOM" is late and is a G1-side follow-up; (A4) under the accepted polkit rule qexec can start arbitrary transient units (including `User=root`) — hierarchy membership rests on the guardian's code checks, and the harness README must say so; (A3) work identifiers with the prefixes `control_` or `event_` collide with the supervision-object GLOBs — S3+ checkpoint names must avoid them and a store-side validator is owed. Overall **S2 remains INCOMPLETE / NOT ACCEPTED**; no activation, no S3 dispatch. S3 preparation (read-only trace of the N1 vertical against the S3 interfaces; synthetic PASS/FAIL sources confirmed) is retained in the coordinator's session notes for the S3 packet.

### GLM continuation — S2 integration return, 2026-09-20

Executor: GLM, continuation implementation/integration owner per the [GLM continuation handoff](../../briefs/handoffs/2026-09-19-glm-s2-enforcement-continuation.md). This entry is a return for coordinator review; every stopping line above is unchanged and nothing here accepts anything.

**Run 4 disposition (35478031666, G1-only diagnostic at `efd91c4`): 11/12 in 1443 s** — record `0dd4ec44ef9544d9916f7ad09415a6fc`, exit 1/1, `source_stable=true`, `capture_complete=true`, both owned-cleanup receipts ok. `test_s2_shared_memory_oom_is_retained_last` passes with the non-zero-exit repair. The two remaining reds are confirmed **evidence-design defects, not enforcement defects**: (a) `payload_cpu` passed *vacuously* — the retained `<attempt>-payload-bound.json` shows peak **0.689 s over 296 samples of a ~297 s stopped window** (run 3: 0.549 s / 296), i.e. the two burners never ran; (b) `probe_that_exits_before_observation` failed because the guarded host kill lands on the **created** (not yet started) container as a docker 409 no-op, the guardian then observes and completes the work, and the fresh-*work* retry is refused ('compute phase already reserved' — one work per phase per campaign; the packet's own wording was fresh *admits*).

**Confirmed diagnoses from the run-3/4 artifacts.** (1) *Lost resume*: the RESUMED event records the guardian's **send**, not the probe's receipt; the first SIGUSR1 lands ~166 ms after container create, before the probe's `block_resume_signal()` arms, and as PID 1 in its PID namespace the unhandled signal is ignored by the kernel (harmless but lost). Every other case is rescued by the bounded re-sends (25 × 200 ms); this test stopped the guardian 47 ms after the first send, killing that coverage — `journal.log` shows the container scope deactivating 31 s after start (the probe's 30 s `await_resume` timeout), the init exiting non-zero, the burners never forking. (2) *Unwinnable race*: sighting the container at create and killing there is systematically a no-op; the race that matters is [container Running → guardian's first identity retention]. (3) *Stop-on-OOM owed and absent*: the plan's S2 behavior row says "stop and retain terminal status on overrun/OOM"; the overrun stop existed, the OOM stop did not (the poll loop never read `memory.events` — A1). (4) *Restart-2 recovery barrier*: `recover_service` calls the recovery entry for every work at every restart; the first restart spends the one-use RECOVERY_OWNER slot on settled work (harmless, completes), and the second restart's spent-slot claim flips those completed rows to `continuation_required`, permanently barring the attempt's positive authority — no suite case restarts a campaign with completed works twice, so only analysis exposed it.

**Integration state** — branch `claude/s2-enforcement-gaps-fab5e6`: merge `ab5d375` brought G1 `efd91c4` into `cce72c9`; the expected `invariant_manifest.json` conflict was resolved by semantic union — **fifteen S2 nodes** (seven original + two R2b route + three G1 under `test_campaign_supervision_linux.py`, plus G2's three under `test_campaign_service_linux.py`), no new duplicates (the manifest's pre-existing cross-entry nodes are unchanged on both parents), no non-S2 invariants lost. G1-owned files verified byte-identical to `efd91c4` and G2-owned files byte-identical to `d60c242` after the merge. Repairs `bb88b7e` + doc correction `b0300e1`:

- `_run_probe` now stops the payload on the first parent `memory.events` `oom_kill` increment over a loop-start baseline — durable IN_DOUBT before the kill, same shape as the overrun stop; settlement retains the OOM facts and drives the terminal state. The overstated group-OOM comments/wording were corrected in `campaign_supervisor.py` and the local-supervision plan (A1).
- `recover_campaign_work` reports status for **settled** work (COMPLETED, or uncertainty already settled by an observation) whose recovery row already completed with no continuation need; un-settled work and legacy claimed rows keep the deliberate spent-slot refusal. The RESERVED-no-enrollment guard no longer swallows legacy recovery rows — this reconciled G1's guard with G2's pinned `RECOVERY_PENDING` label, a merge conflict visible only on the integrated branch.
- The payload-CPU case proves the burn **before** the guardian STOP (sustained ≥150 ms/s `cpu.stat` growth — only real burners under the 33.336/100000 quota do that) and after it (slice populated across the window, `nr_throttled > 0`, `peak ≥ baseline + 0.15×window`), with the kernel upper bound (`quota × wall ≤ budget + one granule`) unchanged. No ceiling, bound or profile constant was touched.
- The unobserved-exit case kills only a container docker reports **running** and retries with a fresh admit per shot (up to 10); the winning shot must show zero retained PROCESS events, exactly one `PROCESS_UNOBSERVED` naming the killed container, `FAILURE` events, IN_DOUBT with no observation, no recovery row authored by the guardian, and a completing recovery with an unspent slot after restart — every COMPLETED work in the suite is also asserted to carry a retained alive-verified identity.
- The ABORTED/IN_DOUBT question is resolved in favour of the governing state machine: `WORK_PREDECESSORS['ABORTED']==('RESERVED',)` (plus linked signing retries through `recover_work`) makes ABORTED the *provable no-effect* state; a started work whose container exits unobserved is genuinely uncertain — IN_DOUBT with a measured settlement and the full-reservation charge on counter loss. No predecessor was added; the G1 packet's §0.5(C) "ABORTED" label for this case contradicts the accepted machine and stands corrected by its own §7.1(a) deviation disclosure.
- Guardian self-failure (G1's `_guardian_self_failure`) re-verified in source and by the new/retained Windows regressions: commits IN_DOUBT only from START_INTENT/RUNNING, retains a bounded FAILURE event, best-effort retires the container, never claims a slot and never runs `cleanup` (no self-kill); BindsTo retires the slice and the service restart recovers with an unspent slot.

**Windows verification on `bb88b7e`** (code bytes; `b0300e1` differs only by the docs correction above; ops-env Python 3.13.2 through the checkout's `fp.ps1`, doctor 62 packages): §2.6 line 1 (ten execution files, `--workers 2`) **419 passed / 0 skipped**, exit 0, record `20260920T005716Z-154ad561d4a1`; line 2 (lifecycle/artifact/manifest/campaign_host) **79 passed + the pre-existing Windows symlink skip**, exit 0, record `20260920T010558Z-25aadfcbc855`. A line-3 run on those bytes (1492 passed / 1 skipped) was invalidated for source instability by a concurrent docs edit in the same checkout — superseded by the final records below. `make audit` and the isolation bridge were not run (the bridge exceeds its 1800 s limit on this box — standing caveat, never claimed).

**Integrated Linux runs.** Run 35482452099 (`pull_request` @ `b0300e1`, merge ref = branch head): **13/15** — G2's three service nodes green on integrated bytes for the first time, the OOM stop and recovery-skip changes host-green, and both remaining failures were test-coordination defects (Codex steering findings 1 and 2, below). Run 35486413008 (steering repairs `9d7a731`): **14/15** — both steering findings repaired and evidenced; the one failure was the deadline case's over-strict post-kill event assert (host-speed dependent; repaired in `db667a2`, no production change). **Run 35487909157 (evidence run, `pull_request` @ `db667a2b1cf6df8ee2c102c4646e4b7d13110ecd`, merge ref = branch head; `main` unmoved at `f2606b0`): 15/15 passed / 0 failed / 0 errors / 0 skipped in 1509.8 s** — record `a405108383cb41e1a92b3e08fecfba9e`, exit 0/0, `source_stable=true`, `capture_complete=true`, `invariants.json passed=true` with all **fifteen** registered S2 nodes present and passed, both owned-cleanup receipts ok. **Run 35489657203 (final head `5ac3ad0` = `db667a2` plus the ledger docs only): 15/15 / 0 skipped** — record `bfc76b0412a44ebf866f277261b08291`, exit 0/0, stable, capture complete, invariants passed, cleanup ok; its unobserved-exit case won the race on the FIRST attempt (`unseen0`, 17 completed works checked with retained identities) and its payload case measured peak 99.061 s, throttled 2970/2974 periods.

Run 35492219418 (`9b2559e`, docs-only over `5ac3ad0`): 14/15 — the shared-memory OOM case met the stop-on-OOM half of a genuine race for the first time (the kernel kills this probe's single-process victim at the same instant the `oom_kill` increment becomes visible; the settle path had always landed first on runs 4–8). The guardian's stop commits durable IN_DOUBT before the kill, so the campaign ends IN_DOUBT rather than the settle path's budget terminal; the load-bearing `oom_events>0` retention held. The case's accepted terminal set now includes IN_DOUBT with that justification — the same duality the overrun stop already has in the two-descendants case — repaired in a test-only commit (no production change). **Run 35493582848 (that repair, `bbafe68`, now the branch head): 15/15 / 0 skipped** — record `f0c6408089d5425a8994b3d555d6cf56`, exit 0/0, `source_stable=true`, `capture_complete=true`, invariants passed (15/15 nodes), cleanup ok; the OOM case passed through the settle path this time (`oom_kill=1, oom_group_kill=0` — the single-process kill) and the unobserved-exit race was won on the first attempt. The branch is now green on its final head and on the two prior code-identical heads (`db667a2`, `5ac3ad0`).

**Steering dispositions (Codex findings, run 35482452099-bound):**

- *Finding 1 — payload readiness mistook interpreter startup for the load: CONFIRMED, repaired in `9d7a731`.* That run's artifact shows baseline 0.272 s → peak 0.553 s of interpreter CPU satisfying the old single-interval gate, `populated 31/295` (the new discriminating assertions refused the vacuous pass as designed; the init again died at the 30 s `await_resume` timeout — the container scope deactivated ~31 s after start). The repaired gate requires, BEFORE the guardian STOP, that the guardian has alive-verified **at least three payload-scope PROCESS identities** (init + both burner children — the forks exist only after the init actually consumed the resume, and cgroup membership binds them to the enrolled container scope) **and** cpu.stat growth ≥150 ms in each of two consecutive ≥1 s intervals (startup totals under 0.6 s and decay; burners sustain ~333 ms/s). Container exit facts are retained before the restart's cleanup; there is no container stderr to retain anywhere (LogConfig `none`), and the lost-resume→timeout cause remains bounded-journal inference, not conclusively established — the case now records docker's exit State on every shot. Final-run evidence (`boundary/<attempt>-payload-bound.json` of 35487909157): `baseline_payload_identities=3`, `peak=99.014317 s` of the 100 s budget over a 294.9 s stopped window (≤ budget+granule), `populated 293/294` (the allowed final-sample race), `nr_periods=2972 / nr_throttled=2969` — runnable descendants exercised the independent kernel bound continuously while the guardian was stopped. No ceiling, bound or profile constant changed.
- *Finding 2 — guardian PROCESS events were mistaken for payload observation: CONFIRMED, repaired in `9d7a731`.* That run retained **four won races** (unseen0–3: PROCESS_UNOBSERVED exit 137 + FAILURE + IN_DOUBT) that the `any PROCESS event` predicate discarded. Two defects: (a) classification — fixed by `payload_process_events` (cgroup-scope membership against the enrolled payload slice; no second classifier; `identity_retained` and the case's final assertions use it, and a winning shot now asserts payload events are empty **while the guardian's own event exists** as the negative control); (b) the 120 s wait missed `settle_work`'s settled-RUNNING shape — settle commits an observation without a work-state transition, so a correctly-settled non-zero exit sits RUNNING-with-observation and only restart recovery moves it IN_DOUBT (pinned by a Windows regression). The unseen5 stall is fully explained by (b): the guardian exited cleanly at 02:06:41 ("Deactivated successfully", 3.017 s CPU, no stderr, no FAILURE) having settled its observation — not a supervisor failure to record. A timeout now captures state/transitions/events/unit-facts/docker-inspect before any restart. The unseen4 variant (docker's Running flag lagging the removed cgroup scope → escaped `FileNotFoundError` → still a correct refusal) is now tolerated bounded (~1 s) in `_run_probe` so the informative PROCESS_UNOBSERVED path is reached; a persistently unreadable running container still raises (both Windows-pinned). Run 35487909157: race won at `attempts=3` (`refusal=PROCESS_UNOBSERVED`, recovery completed, unspent slot; attempts 1–2 legitimately lost and settled without credit), all 19 COMPLETED works across attempts carrying retained payload identities; the final-head run 35489657203 won on the first attempt (`unseen0`, 17 completed works checked) — the retry budget and the first-shot win are both demonstrated across the two green runs.
- *Run-6 failure (deadline case) — test over-strictness, repaired in `db667a2`, no production change:* how far the resumed guardian gets in the ~1.2 s before its timer fires is host-speed dependent (runs 3/4/5 died mid-import; run 6 reached the argv-verification DEADLINE event and died in the ack wait). The post-kill assert now forbids exactly the activity kinds (RESUMED/PROCESS_UNOBSERVED/CLEANUP/FAILURE) and keeps the enforcement facts: Result=signal at the deadline, ExecMainStatus=9, NRestarts=0, work never leaves START_INTENT, payload never populated, full-reservation charge at restart. Final run's evidence: `supervision_kinds=[]` (died mid-import this time).

**Final Windows verification on `9d7a731`/`db667a2` bytes** (`db667a2` differs from `9d7a731` only by the Linux integration test file, which no Windows selection collects; interpreter and launcher unchanged): §2.6 line 1 **421 passed / 0 skipped**, exit 0, record `20260920T031137Z-eb07a39ec8ed` (`9d7a731`); line 2 **79 passed + the known Windows symlink skip**, exit 0, record `20260920T032104Z-1eae37f5ac9b` (`9d7a731`); line 3 (`tests/ops/qualification` + phase3, `--workers 2`) **1494 passed + the Linux-only skip** (1495 collected), exit 0/0, `source_stable=true`, record `20260920T040222Z-dfe69327a137` (`db667a2`); `check` exit 0 (absent-tree data warnings only), record `20260920T043625Z-234eacf14883`; `git diff --check` clean.

Overall **S2 remains INCOMPLETE / NOT ACCEPTED**; PR #436 stays draft pending coordinator review; no merge, no activation, no S3 dispatch.


### GLM continuation 2 — S2 acceptance candidate, 2026-09-20

Executor: GLM, per the GLM continuation 2 handoff. A return for coordinator review; every stopping line above is unchanged and nothing here accepts anything. Status: **RESOLVED** — G3 and G4 finished, integrated on `claude/s2-enforcement-gaps-fab5e6`, and the integrated PR run is fifteen green (details below). S2 acceptance itself remains the coordinator's/operator's entry.

**G3 — resume-before-exec + A2/A4 folds: RESOLVED at `7f26e08`** (the stopped worker's code `0ba2775`, successor-verified, plus the §7 doc). The successor re-read the full diff against the packet and verified every claim: resume gated on the init's exec'd image (`_pre_exec_init`/`_interpreter_image`; `exe` basename when the guardian can read the link, `comm` otherwise); `comm`/`exe` retained and parser-enforced in PROCESS/RESUMED; `PAYLOAD_EXIT` (docker `State`) retained before settlement on every path; durable IN_DOUBT before the measured settlement on the non-credited non-zero exit (intent variant included; linked signing retries keep the settle-only shape); the poll-loop authority read alone re-polls the funding-pending refusal bounded at 5 s — pinned to the store's exact literal, every other refusal and the `_transition` read untouched. Windows: §2.6 line 1 **432/0 skips** (`20260920T153410Z-dcbe7ff032be`), line 2 **79+1 symlink skip** (`20260920T155300Z-cbfd160b4e2e`). Linux: **run 35521178744 fifteen green** (record `38306dc03e044f9b89b429a1e0625700`, 15/0/0/0 in 1502.1 s, exit 0/0, stable, capture complete, invariants passed, cleanup ok) — dispatched as 35521069166 and cancelled by the per-ref concurrency when an identical dispatch started 2 min later; artifact read, not trusted from the check mark. Host image facts retained by the suite: the admission guardian `exe` is the installed interpreter path (own-UID link readable); every payload PROCESS/RESUMED carries `comm='python'`, `exe=''` (the ptrace gate across UIDs, exactly as predicted); no retained image names `runc:[`. §7 of the packet holds the full return.

**G4 — store invariants A1/A2/A5/A7/A9-3: RESOLVED at `8879c0f`** (the stopped worker's WIP `8c764d8` completed by the successor; `9727d95` is an operator commit of the first-round state; `d165f1a` and `8879c0f` carry the repairs and the operator's A5 correction). **A1**: `claim_void_authentication` is three-way — the funded charge unchanged on a fundable BOUND campaign; refusal while bootstrap/recovery/dispatch windows are open; **sequence 0**, one uncharged attempt under the caller's controller guard, when the campaign is VALID but its budget is terminal or not BOUND with no open window. The outcome is retained by body digest (`void_terminal_refusal_<sha256>`, own schema/sequence, integrity-checked) or as the VOID receipt; the body clears either way; a re-queue of a refused digest is refused outright; a distinct body gets its own attempt. **A2 (store)**: CAPTURED/SIGNING_INTENT refused on a settled work; COMPLETED requires credit established before settlement (admission and linked signing retries keep their capture-less productions; the WIP's broader COMPLETED-from-RUNNING refusal kept and disclosed). **A5**: CAPTURED/SIGNING_INTENT/COMPLETED require an enrollment plus a retained payload-scope PROCESS identity — **retries included, per the operator's correction (no identity waiver; the Windows retry scene now retains enrollment and a payload-scope PROCESS identity for parent and retry)** — binding only when the attempt carries a PROCESS-kind supervision event, which every production admission guardian retains as its first durable act (store-only and recovery-only journals stay dormant); the integrity walk enforces the same scope. **A7**: `reserve_work` consults `_remaining_after_charges` (a reservation fitting the snapshot's pre-charge remaining but not the projection's terminalises), `bind_budget`'s cap check adds the charged term, `budget_snapshot` documents the pre-charge view; no schema change anywhere. **A9-3**: `validate_work_id` refuses `control_`/`event_` prefixes and the fixed `admission` identity at `reserve_work` and `parse_request`. One existing test was updated to the ruling's semantics (the terminal-campaign cancellation test now proves the exact retry records the VOID uncharged — its old expectation was the A1 defect itself). Windows: line 1 **434/0 skips** (`20260920T174306Z-d312183ec8d6`), line 2 **79+1 symlink skip** (`20260920T175741Z-179f13226c77`). Linux: run **35524805026** on `d165f1a` — **14/15**, the one failure being the successor's own case-2(c) extension leg with an over-narrow wait predicate (the restart terminalised the campaign BUDGET_UNCERTAIN — counters lost with the retired slice — while the predicate demanded IN_DOUBT; root-caused from the artifact, repaired test-only to the full terminal set); the other fourteen nodes green including every G1/G2/G3-owned node. Per operator steering the integrated PR run proves the repaired leg; no second G4-branch run. §7 of the packet holds the full return.

**Integration.** The operator pushed the G3 merge (`2f530b1`) and merged `main` (#440, docs-only) on top (`1e28d8b`); the successor reset its local integration worktree to the remote head and merged the corrected G4 (`8879c0f`) — merge `14a0e28` plus the ledger/PR-docs commit. No conflicts: G3 and G4 own disjoint files; `invariant_manifest.json` untouched by both. After the merge, G3-owned files are byte-identical to `claude/s2-g3-resume-before-exec` and G4-owned files byte-identical to `claude/s2-g4-store-invariants`, with **one disclosed exception**: `tests/ops/qualification/execution/test_campaign_supervision.py` = G3's head **plus exactly the operator-directed 32-line retry-scene identity addition** (G4's A5 evidence). Integrated Windows verification on the final tree: §2.6 line 1 **445/0 skips** (`20260920T181026Z-619d61aedbe1`; one earlier 445-pass record was voided for source instability by the successor's own concurrent ledger-draft edit in the same checkout — the standing lesson, relearned), line 2 **79+1 symlink skip** (`20260920T181942Z-f098ab3ad897`), line 3 **1519 collected, 1518 passed + 1 Linux-only skip** (`20260920T182055Z-f5d26735a7d7`), `check` exit 0 (`20260920T190042Z-5fb4ff8d0810`, absent-tree data warnings only), `git diff --check` clean. The intermediate G3+G4 tree (`1e97011`, superseded by the #440 merge) carried the same line-3 result (1518+1, `20260920T180021Z-3972cc21247e`); the final tree differs from it by #440's two docs files and G4's correction commit only.

**Integrated Linux evidence run:** run **35530964034** (`pull_request` on the pushed head `14a0e28`) — **15/15 passed / 0 failed / 0 errors / 0 skipped** in 1515.4 s (record `fe5443885ff9412f9b872621cb2b36d7`, exit 0/0, `source_stable=true`, `capture_complete=true`, `invariants.json passed=true` with all fifteen required nodes, owned-cleanup receipt ok, 9 removals), read from the downloaded artifact, not the check mark. The case-2(c) terminal-VOID leg passed through the **BUDGET_UNCERTAIN** terminal path (evidence `s2-queued-cancellation.json`: the restart's recovery lost the wall work's counters with its retired slice, the campaign terminalised BUDGET_UNCERTAIN with the work IN_DOUBT and validity VALID, and the operator's body authenticated once uncharged — `charges: []`, `void_authentication_attempts == 0`, remaining allowance 9860 s unchanged). The operator's own pre-G4 PR run 35525302963 (`1e28d8b`, G3+main) was also fifteen green, so the branch is host-green with and without G4.

**Codex review:** the `@codex review` trigger was posted (PR comment 5751943717) and the bot refused — **usage limits reached** (same failure as #429's second attempt); no bot review exists on the PR. The operator then relayed an **external Codex review of `14a0e28`** (isolated snapshot, ops-env Python 3.13.2; 3 counterexamples reproduced, 8 existing control cases green, stable-source records; no full gates, no fresh Linux run) with **two P2 findings — both confirmed as mechanisms; merge HELD**:
- *P2-1 — the A5 identity guard is gated on evidence presence, not the execution contract.* An enrolled work can reach CAPTURED with zero PROCESS events, and stripping all PROCESS rows from an already-credited journal lets it reopen clean. This is precisely G4 §7's disclosed limitation (a): the PROCESS-kind engagement scope exists because the packet's unqualified rule refuses the compact funding model and the store-only journals (enrolled, crediting, OS-free — reproduced in this session's own first line-1 run), and the operator's in-flight steering directed exactly this shape ("keep the binds-only-when-supervision-events-exist guard") while the relayed review now asks for a contract-dependent guard. Those two directives conflict; the fix shape is known (bind to the funded profile + enrollment with retry identities, and resolve the compact-model conflict by versioning or by changing the model tests), but changing a green, evidence-bound boundary after the run without a ruling is not the successor's call. **Disposition: CHECKPOINT for the coordinator**, with the smallest change and its blast radius to follow the ruling.
- *P2-2 — G3's PROCESS parser breaks pre-G3 journals.* The unchanged `qualification_campaign_supervision_event/v1` schema now *requires* comm/exe, so a valid predecessor event (every retained journal from runs through 35493582848, and the #423/#424 evidence journals) fails `ExecutionStore` reopen with 'closed schema fields required'. Confirmed mechanically — this session's own G4 tests needed an adaptive event-shape helper to pass under both parser generations. The strict shape was the G3 packet's frozen §2.1/§2.3(c) order (its Windows tests pin the old shape's rejection), so accepting the historical shape or versioning the event schema is a **coordinator ruling on the packet**, not a successor repair: it re-touches G3's parser and its pinned tests, needs a Windows re-run, and any versioned-shape decision also bears on P2-1's contract question. **Disposition: CHECKPOINT for the coordinator** — the same class as the packet's version-bump CHECKPOINT clause.
No fold loop applies (zero review rounds on the PR itself); both findings stand open against the held merge.

**Review advisories closed vs recorded for S3** (from `docs/notes/audits/2026-09-20-pr436-s2-integrated-acceptance-review.md`): **closed on this candidate** — A1 (terminal-but-VALID recordability, store + Linux case-2(c) leg), A2 (guardian half in G3, store half in G4), A4 (the poll-loop re-poll bound, G3), A5 (transition precondition + integrity walk, G4), A7 (one allowance view at the store grants, G4), A9-3 (work-id validator, G4; A9-4's README trust-model wording remains open and is folded into the S3 preconditions below with A3/A6/A8). **recorded as S3 preconditions, not repaired** — A3 (any service restart destroys running work, healthy guardian included — the case-2(c) leg relies on exactly this ruled behavior), A6 (the OOM *stop* half remains Windows-proven plus the one red-run host trace; the green runs' OOM case settles), A8 (dead guardians reconcile only via their own timer or a service restart). A9-4 (README qexec wording) stays open for S3 alongside them.

No allowance, ceiling, profile, release, snapshot or DB-version change anywhere in G3/G4; no `campaign_probe.py` change; no skipped or relaxed Linux case; no S3 work; no merge of #436; no activation. PR #436's description now carries the current facts. **S2 remains INCOMPLETE / NOT ACCEPTED pending the coordinator's acceptance entry.**

### Coordinator rulings on the two P2 findings — S2-G5 dispatched, 2026-09-20

GLM's continuation-2 return is accepted as delivered work: G3 and G4 integrated at `14a0e28`, fifteen green on run 35530964034 (record `fe5443885ff9412f9b872621cb2b36d7`), Windows lines 1–3 and `check` green on the final tree. Its CHECKPOINT on the two external-review P2 findings was correct — silently repairing either would have crossed a frozen instruction. Both are confirmed mechanisms on the head: `_supervision_events_present` scopes the A5 identity rule by evidence presence (an enrolled work can be credited with zero PROCESS events; stripping PROCESS rows reopens clean), and `parse_supervision_event` requires `comm`/`exe` under the unchanged `…supervision_event/v1` literal (every pre-G3 journal fails reopen). **Rulings** (packet [S2-G5](../../briefs/handoffs/2026-09-20-full-e1-s2-g5-contract-identity-and-event-versioning.md)): R1 — payload identity binds by contract = enrollment (an enrolled non-admission work needs ≥1 payload-scope PROCESS event for credit, enforced on transition and on reopen; un-enrolled persistence-layer works are the explicit store-only distinction; no version change); R2 — `v1` is restored to its pre-G3 strict shape and a `v2` event schema carries the image-bearing PROCESS/RESUMED and the new kinds, producers emit v2 only, consumers read both strictly; R3 — labels: A5 is implemented-but-reopened until G5 closes it; G3's launch repair is host-evidenced with journal compatibility open until G5; A9-4 is **closed** (README lines 196–201, commit `e85f96c`), GLM's return mislabels it. Review advisories still recorded for S3 unchanged: A3, A6, A8. **S2 remains INCOMPLETE / NOT ACCEPTED; PR #436 merge held** until G5 returns fifteen green with the compatibility regressions and the independent reviewer confirms both P2s closed. No S3 dispatch. The Codex PR bot is at its usage limit (comment 5751943717); the external Codex review of `14a0e28` stands in for it on this candidate and its author is to be named in the acceptance entry.

### S2-G5 return — contract-bound identity and versioned supervision events, 2026-09-20

Executor: ZCode, per the S2-G5 packet (rulings R1/R2/R3). A return for coordinator review; nothing here accepts anything. Status: **CHECKPOINT** — the repair is complete, fail-on-base-proven and Windows-verified, and the single Linux run is **14/15** on a failure root-caused outside the packet's change surface (below); R1/R2/R3 themselves stand resolved.

Branch `claude/s2-g5-contract-identity`, head `3db58c8` plus the docs commit carrying this ledger entry; `git diff --stat 9e075db...3db58c8` = six files, +322/-114 (three production, three test).

**R1 (P2-1 closed):** the identity rule binds by execution contract — a retained `supervision_<work>` enrollment — not by `_supervision_events_present` evidence presence (deleted; no presence-based scoping remains). An enrolled non-admission work needs >=1 payload-scope PROCESS event (either schema version) for CAPTURED/SIGNING_INTENT/COMPLETED at transition time and on reopen (integrity refuses an enrolled credited work without identity; stripping every PROCESS row fails reopen). Un-enrolled persistence-layer works are explicitly outside the rule; the one Windows scene that enrolled-and-credited with zero PROCESS events (the compact funding 'seal' scene) now retains a simulated payload identity; **un-enrolments: none** (store-only scenes never enrolled; scenes that enroll but never credit keep their honest enrollment). No production path credits an enrolled work unobserved (materialize/prepare both continue into a real guardian; the admission is the exempt work) — the packet's CHECKPOINT condition did not fire.

**R2 (P2-2 closed):** `v1` restored to the exact pre-G3 strict shape so every historical journal (runs through 35493582848, the #423/#424 evidence journals) reopens; `v2` carries the image-bearing PROCESS/RESUMED plus PAYLOAD_EXIT; all producers (ten `_retain_event` sites plus both CONTROL producers) emit v2 only; consumers read both strictly. **Ruling refinement accepted at GO:** DEADLINE and PROCESS_UNOBSERVED are G1-era kinds retained in every historical journal (pre-G3 producers `4281d2e:879/1146`), so v1 accepts them and refuses only PAYLOAD_EXIT — packet §2.4's rejection list is corrected accordingly.

**Fail-on-base:** against `9e075db` production with the branch's tests, the event-free refusal test fails DID-NOT-RAISE (P2-1's mechanism) and the predecessor v1-journal test fails `closed schema fields required` (P2-2's mechanism); both pass on the branch.

**Windows** (recorded from a clean commit worktree; the shared main checkout's `tmp/` debris — a nested clone and vendored deps — breaks repo-wide source snapshots and pre-commit boundary gates there, a hygiene item for the coordinator): line 1 **448/0 skips** (`20260920T224155Z-76415c6fe302`), line 2 **79+1 symlink skip** (`20260920T230342Z-4c16ef3f532b`), line 3 **1521+1 Linux-only skip** (`20260920T230459Z-d726c1d98df7`), `check` exit 0 (`20260920T233542Z-57f79b918bed`), `git diff --check` clean.

**Linux:** run **35543486564** on `3db58c8`, record `db7afc5d5b464e7a8ae301d8c82e4e73` (exit 1/1, stable, capture complete, cleanup ok), artifact-read via `scripts/s2_run_evidence.py` (from `origin/main` #447). Fourteen nodes green with v2 events and the enrollment-bound rule exercised throughout; the one failure is `test_s2_shared_memory_oom_is_retained_last`, root-caused from the artifact: the memory payload (guardian-retained payload-scope PROCESS `comm='python'`, RESUMED — post-G3 gating intact) died ~540 ms after shim connect with **ExitCode 138 (SIGUSR1 — the guardian's bounded resume re-send), `oom_killed=false`, zero `oom_kill` anywhere, parent peak 242.7 MB below the 256 MB limit**; the guardian then took exactly the designed non-credited path (IN_DOUBT, measured settle, campaign IN_DOUBT) and the case's own host-side `oom_kill>0` wait was the only failing assertion. The prior green run 35530964034 on `14a0e28` shows the same case dying at exactly the limit by OOM (**137, `oom_killed=true`, `oom_events=1`**) four hours earlier. Nothing in the G5 diff touches the resume handshake, the re-send window, the probe or that case; a fatal USR1 delivery to the payload init is outside the design's stated safety properties (SIG_DFL drops to a namespace init; blocked + no-op handler is immune). Reported per the s2-linux-run skill (no same-SHA re-roll, no Linux assertion relaxed); **coordinator ruling needed**: re-dispatch on a rotated runner, investigate the docker/runc signal path, or open the repair as its own packet.

**R3:** A5 = implemented, reopened by P2-1, closed by R1 (bracketed correction in the G4 packet §7); G3's journal compatibility = open under P2-2, closed by R2, the launch repair itself host-evidenced (bracketed correction in the G3 packet §7); A9-4 = **closed** — `tools/qualification_verification/README.md` lines 196-201 carry commit `e85f96c`'s polkit trust-model correction, verified present on this branch and an ancestor of its head — GLM's continuation-2 entry mislabeled it open and stands unedited per the append-only rule. Review advisories recorded for S3 unchanged: A3, A6, A8.

No allowance/ceiling/profile/release/snapshot/DB-version change beyond the supervision event schema; no Linux assertion relaxed; no `campaign_probe.py` change; no S3 work; no merge of #436; no activation. **S2 remains INCOMPLETE / NOT ACCEPTED pending the coordinator's acceptance entry.**

### S2-G5 addendum return — readiness-token resume handshake, 2026-09-21

Executor: ZCode, per the coordinator's revised ruling on the 14/15 (run 35543486564: the OOM-case payload died of the guardian's SIGUSR1, exit 138, no OOM anywhere). The ruling supplied the mechanism from separate research: the worker import chain pulls numpy, whose OpenBLAS builds a thread pool at import; glibc's `pthread_create` leaves a sibling briefly unblocked while the leader holds the block, and the kernel's fatal-default group exit bypasses the container-init drop (`complete_signal` since 4.15). It also **retracts G3 §1's "Go runtime dies on SIGUSR1" mechanism** (Go's SIGUSR1 is notify-only; runc's init never died of it — the earlier 14/15 was this same numpy-import window, and G3's image gate moved the send later without removing the race); the research note is `docs/notes/audits/2026-09-20-sigusr1-container-init-mechanism.md` (coordinator-committed) for the reviewer.

**The repair (branch `claude/s2-g5-contract-identity`, final head `2a00902` = `4e6ba9d` + `ddf5e8e` + the Env fix):** `bootstrap.py` installs the no-op SIGUSR1 handler and then blocks SIGUSR1 for the payload roles (`worker`, `campaign_probe`) as the first act — before `sys.path` and before any import that can spawn threads — so every later thread inherits the blocked mask and a resume can only ever sit pending for the main thread's `sigtimedwait`; this also covers S3's worker, which imports numpy first. `campaign_probe.block_resume_signal()` becomes verification (the block must still be armed) plus the readiness declaration: it writes the fixed token `fpq-armed` (within TASK_COMM_LEN-1) to `/proc/self/comm`. The guardian's send condition is `comm == token`, re-evaluated every poll, with the interpreter-image gate kept as a harmless second condition and the bounded re-send window unchanged; a comm change for a known (pid, start_ticks) is retained as its own PROCESS event, so a retained PROCESS carrying the token proves the probe reached the handshake. Every send is retained as its own `RESUMED`/v2 event carrying its ordinal (`send_count`), the boottime of that send, and the target's `Threads`/`SigBlk`/`SigCgt` read at the send — a healthy send shows bit 9 (SIGUSR1) set in both SigBlk and SigCgt, the evidence the mechanism question needs; the Linux `resumed_image` asserts exactly that. Belt, not the fix: the probe container's Env carries the controller-environment thread limits (`OPENBLAS_NUM_THREADS=1` and siblings). The interim v2 RESUMED shape in run 35543486564's red journal is superseded by this closed shape; that journal is not evidence and does not reopen under the strict parser (disclosed).

**Branch Linux evidence:** run **35548558302** on `ddf5e8e` failed **9/15** — root-caused from the artifact journal to a defect in the addendum itself, not the handshake: the belt passed `Env` as a dict where the docker create API requires a list of `K=V` strings, so every probe `POST /containers/create` was refused and the guardians self-failed before any container existed. Fixed at `2a00902` (Env built exactly like the guardian unit's `Environment`, with a new Windows regression constructing the real fixed body — the shape was previously never asserted on Windows because every scene stubs `probe_container_body`). Per the coordinator's follow-up ruling, **no further branch Linux run is dispatched**: the coordinator merges the branch and the PR run on the merged head is the single Linux evidence; lines 2-3 and `check` on the merged tree only on request.

**Windows on the final addendum bytes** (`2a00902`, same clean worktree; ops-env 3.13.2): §2.6 line 1 (ten execution files, `--workers 2`) **450 passed / 0 skipped**, exit 0, record `20260921T013255Z-b2ad638aba3f` (450 = the R1/R2 suite's 448 + the bootstrap-ordering guard + the Env-shape regression). Intermediate records on `ddf5e8e`: line 1 449/0 (`20260921T004315Z-1df104b0816b`), line 2 79+1 symlink (`20260921T005057Z-79d19a52673f`), line 3 1522+1 (`20260921T005125Z-8e5ab06f3f0b` — ID per the record directory created at line-3 start). Regressions: the token-gate scene (runc -> bare interpreter -> token: no send until the token, exactly one RESUMED with count 1, the interpreter and the token rename retained as two PROCESS events), the kept image gate's table, the parser matrix (v2 RESUMED requires the token and bounds send_count/send_boottime_ns/threads positive and the masks 1..16 hex; v1 unchanged), the completing scene's RESUMED facts, the bootstrap source-order guard (handler+block precede `sys.path` and every import but `signal`), and the Env-shape regression.

S2 remains INCOMPLETE / NOT ACCEPTED pending the coordinator's acceptance entry and the P2-closure reviewer's confirmation; no merge of #436 by this worker; no S3 dispatch; no activation.

### Coordinator acceptance — S2 budgeted admission and real Linux work supervision, 2026-09-21

S2 is **ACCEPTED as the enforced work boundary** on `claude/s2-enforcement-gaps-fab5e6` @ `4ef913a` (PR #436; the final integration head `d7fcf36` merges `main` on top and is byte-identical on the S2 surface — `ops/c1_rail/qualification`, `deploy/qualification`, `tests/integration/qualification_boundary`, `tests/ops/qualification`, the verification script and the host tooling — so its repeat S2 run is the merge gate, recorded on PR #436, not new evidence), the integrated candidate that closes the five enforcement gaps the operator listed on 2026-09-19 and the two P2 findings of the external review. Acceptance means exactly what the slice's return boundary allows: the accounting, enforcement, interruption-recovery and cancellation behavior of admission and supervised test work on a real Linux host. It authorizes no statistical dispatch, no installed-release activation on a non-disposable host, no S3 work by itself.

**What closed, and where the evidence is.**
| Gap / finding | Repair | Evidence |
|---|---|---|
| Independent payload CPU enforcement | G1: `CPUQuotaPerSecUSec` × `RuntimeMaxUSec` on the payload slice, verified realized; kernel bound independent of the guardian | `test_s2_payload_cpu_is_kernel_bounded_without_guardian` (guardian STOPped; peak ≈ budget, `nr_throttled` > 0) |
| Original deadline before bootstrap | G1: absolute BOOTTIME SIGKILL armed in `bootstrap.py` before any campaign import; argv deadline cross-checked against the store | `test_s2_deadline_kills_guardian_before_bootstrap_completes` |
| Verified process identity | G1 + G3 + G5: alive-verified payload-scope PROCESS retained before credit; resume only after the entrypoint has exec'd [and declared readiness — G5 addendum]; identity bound to enrollment in the store and on reopen (R1) | `test_s2_probe_that_exits_before_observation_never_completes`; Windows: event-free credit refusal, PROCESS-stripping reopen refusal |
| Funded VOID authentication | G2 + G4: signature verification only inside a durably charged one-use operation; pending-cancellation barrier on new positive authority; VOID recordable on a terminal-but-VALID campaign (A1) | `test_campaign_service_linux.py` cases 1–2; Windows exhaustion/forgery/restart regressions |
| Safe admission retry | G2: exact `SUBMIT_E1` retry resumes a structurally absent RESERVED admission once; restart never spends a recovery slot on it; expired unstarted admissions terminalised | `test_campaign_service_linux.py` case 3; Windows crash-after-`begin_admission` regressions |
| P2-1 identity by contract (external review) | G5 R1 | fail-on-base reproduction + regressions (G5 §7 item 6) |
| P2-2 journal compatibility (external review) | G5 R2: `…supervision_event/v1` restored strict (G1-era kinds accepted, PAYLOAD_EXIT refused); `/v2` carries image-bearing PROCESS/RESUMED + PAYLOAD_EXIT; producers v2-only, readers both | predecessor-journal reopen regression; parser matrix |
| Guardian self-recovery race (G2's root cause) | G1/G3: `_guardian_self_failure` (durable IN_DOUBT, FAILURE event, no self-kill, no spent slot) | fifteen-green runs |
| Pre-exec resume race (coordinator root cause, run 35494972519) | G3: resume gated on the exec'd image; PAYLOAD_EXIT retained on every path | run 35521178744 |
| Post-exec resume race (run 35543486564, exit 138; mechanism: numpy-import OpenBLAS thread creation under glibc's leader signal block lets `complete_signal` group-exit a PID-1 with SIG_DFL — the same window as run 35494972519) | G5 addendum: handler installed and SIGUSR1 blocked process-wide in `bootstrap.py` before any import; readiness token in `comm`; send count + `Threads`/`SigBlk`/`SigCgt` retained; thread-limit env in the container body | run 35552151992 on `deacbb4`: the handshake held on all eight payloads (first send `SigBlk=0`/`SigCgt=0x202`, later sends `SigBlk=0x200`, `Threads=1`); three cases failed only on the coordinator's over-strict evidence assertion (the blocked mask is cleared by `do_sigtimedwait` during the wait), corrected test-only at `4ef913a`; **run 35553674384 fifteen green** |

**Final evidence on the accepted head.** Linux: integrated PR run 35553674384 on `4ef913a`, 15/15, 0 skipped, record `1b32bd6d9c454fc89b8f176f8565af0d`, `source_stable=true`, `capture_complete=true`, invariants passed (15 required), cleanup ok — read from the artifact (`scripts/s2_run_evidence.py`). Windows (ops-env Python 3.13.2, `fp.ps1`): recorded on `deacbb4` (code-identical to `4ef913a` and `d7fcf36` for every collected file): line 1 450 passed / 0 skipped (`20260921T015015Z-1d58ac276a56`), line 2 79 + the known symlink skip (`20260921T015832Z-4005cc2e57eb`), line 3 1523 + the Linux-only skip (`20260921T020008Z-0b7d01a6b707`), `check` exit 0 (`20260921T023414Z-fcb4a104ff4f`), `git diff --check` clean; G5's own records on `3db58c8`/`ddf5e8e` stand in its packet §7. Independent reviews: acceptance review 2026-09-20 (`docs/notes/audits/2026-09-20-pr436-s2-integrated-acceptance-review.md`, 0 BLOCKING / 9 ADVISORY); external Codex review of `14a0e28` (two P2s, both closed above; the Codex PR bot was at its usage limit, comment 5751943717); P2-closure review of G5 (`docs/notes/audits/2026-09-20-g5-p2-closure-independent-review.md`: P2-1 CLOSED, P2-2 CLOSED, 0 BLOCKING / 2 ADVISORY, fail-on-base reproduced by the reviewer); the SIGUSR1 mechanism note (`docs/notes/audits/2026-09-20-sigusr1-container-init-mechanism.md`) retracts G3's runc-Go account: the killer is the numpy-import thread-pool window under glibc's pthread_create leader block. Executors: Claude Code workers (G1, G2, G3-draft, G4-draft), GLM continuations 1–3 (integration, G3/G4 completion, G5), coordinator Claude; the dual-executor history on G4 (`9727d95` committed by a second GLM session from the first's edits) is disclosed in the continuation-2 return.

**Recorded, not repaired — S3 preconditions** (from the acceptance review; each is a ruled S2 behavior, not a defect): A3 — any service restart destroys every running work including a healthy guardian (R2b ruling); an S3 checkpoint therefore cannot survive a supervisor restart unless S3 adds a live-guardian reconciliation path or accepts the loss explicitly. A6 — the OOM *stop* half is host-evidenced by one red run and by Windows simulation; the green runs take the settle path; both are accepted terminal sets. A8 — a guardian killed by its bootstrap timer or refused at bootstrap leaves START_INTENT/RUNNING with no pending marker until a later clock observation or restart; S3 must decide whether the schedule route may proceed with an unreconciled sibling. Also for S3 (from the G5 closure review): the enrollment row is an un-chained retained object — deleting `supervision_<work>` together with the PROCESS rows after a legitimate credit reopens clean, and a store-direct caller that never enrolls credits freely; R1 rules un-enrolled works outside the identity rule, so this is recorded against A5 for S3 (candidate anchor: the chained START_INTENT `work_scope_id`), not treated as closed. "Every historical journal reopens" is proven for the parser; a pre-G1 journal whose guardian credited on `ExitCode==0` without an observed pid would be refused by the walk (no tooling reopens such journals; scope the claim). Also for S3: work identifiers must avoid the `control_`/`event_` prefixes (validator in place); snapshot totals are pre-charge, the funding projection is authoritative; the real worker entrypoint must reuse the probe's readiness handshake (block, install, write the token to `/proc/self/comm`, `sigtimedwait`) or it will be killed by the resume.

**Structural facts this acceptance rests on (unchanged):** the campaign cap covers attributed process/cgroup resources; raw payload CPU plus the immutable 20 s orchestration charge is settled once; unknown counters consume the reservation; a pending unauthenticated VOID body blocks new positive authority and never itself sets VOID; the guardian's authority poll remains the VOID→kill wiring; under the accepted polkit rule qexec can start arbitrary transient units and containment rests on the guardian's code checks (README §Trust boundary). No allowance, ceiling, profile, release, snapshot or DB version changed across G1–G5; the supervision **event** schema gained `/v2`.

**Merge:** PR #436 → `main` after this entry; the integration branch deleted the `s2-linux-run` skill before the operator merged it via #446, which resolves in `main`'s favour. Next: the S3 packet draft `docs/briefs/handoffs/2026-09-21-full-e1-s3-n1-genuine-capture-DRAFT.md` (the four §0.5 design decisions were ruled by the operator on 2026-09-21; freeze after re-anchoring at the merged head).

#### Merge record — PR #436, 2026-09-21

Merged to `main` at `abb3914` (03:51Z). Merge-gate evidence on the merge head `a519bfb`: S2 run 35557000399 — 15/15, 0 skipped, record `b16ef73402ea41709557056aa8cac352`, `source_stable=true`, `capture_complete=true`, invariants passed (15 required), cleanup ok, read from the artifact with `scripts/s2_run_evidence.py --expect-head a519bfb`; `pytest (3.11)` and every other check green. The first merge-gate run (35555309697 on `a39adf5`) was 14/15 on a **test-harness defect, not an established production defect**: the deadline case's stopper selected any guardian-cgroup process whose comm lacked a parenthesis and could therefore freeze the manager's forked child before its rename (comm still `systemd`), so the exec was never observed and `TimeoutStartSec` ended the unit with `Result=timeout`; fixed test-only at `a519bfb` (exact comm match); the assertions — termination by the guardian's own deadline timer, no payload activity, conservative recovery — are unchanged. The acceptance evidence on `4ef913a` stands for that revision. The S2 surface of `abb3914` is byte-identical to `4ef913a`. Next: T02/S3 packet freeze from `docs/briefs/handoffs/2026-09-21-full-e1-s3-n1-genuine-capture-DRAFT.md`, re-anchored at `abb3914`; T07/T08/T10 dispatchable now; the deployment-checklist amendment is PR #448 (proposal).


### Coordinator checkpoint C1 — S3 interface freeze ACCEPTED; GO for the Linux iteration, 2026-09-21

**Return inspected:** branch `claude/s3-n1-genuine-capture` off `main@abb3914`, head `71732aa` (e350e36 → 2d14faa manifest registration → 71732aa closure fix); `git diff --stat abb3914...71732aa` = 27 files, +2729/−90 (GLM reported +2715/−73 before its own re-count; the byte diff is the authority). Windows on the frozen bytes: line 1 556/0 (`20260921T103447Z-744a08c63966`), line 2 79 + the known symlink skip (`…T111358Z-60808e2e743d`), line 3 1537 + 1 Linux-only skip (`…T104256Z-fda2f6230fc9`), `check` 0 (`…T111255Z-91878bb1aba9`), `git diff --check` clean. Fail-on-base: `test_v4_service_route_refuses_the_dispatch_roles` and `test_full_e1_assessment_family_exists_and_is_closed` both fail at abb3914 production and pass at 71732aa. The coordinator read the diff, not only the summary: `ExecutionStore.executions` `CHECK(checkpoint='N1')` untouched (store.py gains only the v8 layout branch); the fifteen S2 manifest nodes survive byte-for-byte under QEXEC-01 (15 before, 15 after, four N1 nodes added); `test_campaign_supervision_linux.py` and every S2 assertion untouched; `--test-only` selection untouched, `--s3` strictly larger; the D4 literal refuses `dispatch_enabled=True` on v3/v4 and requires exactly `dispatch_checkpoints == ['N1']` on v5; the worker takes the handshake only on the guardian-launched argv (`--output /output` / `--campaign-limits`) and the N1_ONLY stdout path is byte-identical; `PhaseBudgetGuard` replaces `BudgetGuard.from_contract` for FULL_E1 only; the g5 unit is `Slice=<payload slice>`, `BindsTo` the guardian, `RuntimeMaxUSec` + `CPUQuotaPerSecUSec` from the N1_G5 phase; the io tmpfs mounts carry `size=`; `campaign_host.cleanup` stops and proves absence of `var-lib-fpq-*.mount` and `*-payload-g5.service`.

**Freeze accepted as published** (the full text now sits in the packet's §7; T05 builds against it): the three-schema family `qualification_campaign_checkpoint_{result,attestation,assessment}/v1` (+ `_attestation_payload/v1`), the `/v6` snapshot as a strict superset of `/v5` with one `checkpoints` field, the four G5-only operations with closed fields, transaction ownership T1 `persist_checkpoint_intent` / T2 `commit_checkpoint_assessment` (CampaignStore owns the commit and the progression advance; the service owns re-validation between them under `dispatch_lock`), VOID serialization through the dispatch lock (VOID first → T2 refuses `VOID campaign`; commit first → terminal state retained, later VOID flips validity only), signing/recovery (before T1 → IN_DOUBT under A3; between → the intent settles, exact retry returns the identical receipt with T1's instant; after T2 → byte-identical receipt, `historical=true`; a different candidate under a persisted intent always refuses), budget accounting (N1 settles payload CPU + orchestration with the capture/attestation tail inside the guardian; N1_G5 reserves its ceiling and reads the qg5 unit's own cgroup; N1_CAPTURE keeps no own reservation, as in S2; commit re-checks deadline/clock inside T2), and the E01–E12 ownership table (S3: E02, the N1 legs of E01/E06/E07/E08/E09/E10/E12; S4: E03 + the N2 halves; S5: E04/E05; S6: the FAIL/aggregate commits; S7: E11 + E12's seal side; cross-slice two-checkpoint tests named for T06).

**Readings ruled:** (1) D2 — the g5 unit under the *payload* slice (a child of the work slice) is the correct reading: it is what makes R1's enrollment-bound identity rule hold for the qg5 PROCESS events without touching the S2 gate. (2) D3 — the mount units need not be slice-bound: tmpfs pages are charged to the cgroup of the process that writes them (the worker, inside the payload slice) and `size=` caps the mount; "under the payload slice in the accounting sense" is therefore the substantive property, the explicit administrator stop + absence proof in `cleanup` is the ownership property, and no host-layer change is required before the acceptance run. (3) The existing `tests/ops/qualification/test_checkpoint_validation.py` extended in place — accepted as disclosed. (4) `campaign_budget.validate_recoveries`' v5 literal untouched — accepted (outside §2; unreachable by construction since the capture follows the payload dispatch rows); S4 will revisit if N2 changes the ordering. (5) Per-run fixture-derived closure/image digests — accepted; the first Linux run's record carries them. (6) The T1-crash/T2-retry window proven deterministically on Windows only — accepted for S3; T06 owns a service-kill fault injection if one is ever needed.

**Gaps that do not block the freeze but precede the acceptance-grade run** (§4 obligations the return did not carry): (a) five named negative regressions are absent from `test_campaign_n1.py` — *altered outcomes* (a worker verdict that disagrees with G5's reconstruction is refused; the verdict is never authority), *wrong signer* (an attestation under a non-guardian execution key and an assessment under a non-result key refuse in `g5.verify_checkpoint_*` and in the service commit — the store scene's placeholder signature is disclosed, so these live on the verified paths), *source substitution* (an input member that is not the admitted original refuses at fetch/validate), *expiry* (deadline passed at T2 refuses with no receipt), *N1_G5 budget exhaustion* (no credit, commit refused, work settles); (b) the pinned-vector tests D1 requires "extended, never replaced" were not touched: `test_release.py`/`test_profile.py` (v5 literal, the closed `dispatch_checkpoints` set, v4 with `dispatch_enabled=True` still refused), `test_journal_snapshot.py` (a `/v6` vector beside the `/v5` one, `/v5` bytes unchanged), `test_evidence_reconstruction.py` (a FULL_E1 assessment vector beside N1_ONLY); (c) the Linux tooling the packet authorizes for the first iteration is not landed: `.github/workflows/qualification-s2-supervision.yml` still invokes `--s2` and has no `cases` input, and `scripts/s2_run_evidence.py` neither reports `acceptance_scope` nor refuses `DIAGNOSTIC_SUBSET` by name (today it refuses it only because the subset run exits non-zero).

**GO, in this order (dispatch-first; the Windows and Linux clocks overlap):** (1) land (c) — `workflow_dispatch` inputs `mode` (`s2`|`s3`, default `s3`) and `cases` (a `-k` expression, empty = full), the `pull_request` invocation switched to `--s3` (S3_CASES ⊇ S2_CASES), `timeout-minutes` raised only on measured need; `s2_run_evidence.py` reports `acceptance_scope` and refuses anything but `S2_DIAGNOSTIC_SUPERVISION`/`S3_N1_CAPTURE` — push, then dispatch one `DIAGNOSTIC_SUBSET` run on `-k test_s3_genuine_pass` and record its wall time; (2) while it runs, draft (a) and (b) in the scratchpad; fold whatever the subset run teaches; commit; Windows lines 1–3 + `check` on the frozen bytes; push; (3) dispatch the acceptance-grade `--s3` run per `s2-linux-run` (nineteen required nodes: fifteen S2 + four N1), read it with `s2_run_evidence.py <run> --expect-head <sha>`; (4) return per §4 with the run/record identities and the per-run closure/image digests, and only then open the PR. T05's packet (complete result and separate seal, S6–S7) is authored by the coordinator against this freeze and dispatched in parallel behind its own file boundary.

### T05 (S6–S7) packet authored against the C1 freeze, 2026-09-21

`docs/briefs/handoffs/2026-09-21-full-e1-t05-result-and-seal.md` — parallel build behind a named file boundary (four new modules, three new test files, one Linux file written now and run only at acceptance), branch `claude/t05-result-seal` off `71732aa` so the S3 family parsers are importable; every touch into S3/S4/S5-owned files is an integration seam the coordinator applies after T04. Frozen: F1 boundary, F2 custody (DB `user_version` 9 = v8 + result + seal tables; two closed families), F3 progression names carried into S4/S5 (`N2_FAILED`, `PART_A_FAILED`, `FULL_PASS_READY` → `RESULT_COMMITTED_{PASS,FAIL}` → `SEALED_PASS`), F4 isolated charged units (`result_g5` on `RESULT`, `seal` on `SEAL`, D2 pattern), F5 signing recovery mirroring S3. Internal checkpoint C-R after S6 before any S7 code. Acceptance only after T04 against real captures.

### Coordinator checkpoint C-R — T05/S6 result commit ACCEPTED as an interface; S7 GO, 2026-09-21

`claude/t05-result-seal@c5caa2f` off `71732aa` (8c21bec implementation → c5caa2f: the validation-provenance registry removed; T2 re-derives every validated field from the persisted candidate bytes). Five files, +2369, none outside the §2 boundary (verified by name list). Windows: the S6 selection 573/0 (`20260921T152244Z-69b1cca861de`, re-recorded on the final tree `20260921T171640Z-0b5979c345e5`); line 2 79+1; full `tests/ops/qualification` + phase3 1554/1 of 1555 (`20260921T173015Z-bc3ffa2f6683`). Fail-on-base `20260921T153559Z-16250ea6dd86` (collection error at 71732aa — absence evidence, accepted). The one fold on the way: the legacy frozen-adjudicator's retained-executable walk swept the new module's mutable registry into its runtime receipt (33 failures outside T05's files); fixed inside the boundary by removing the registry — a stronger T2 gate with no module state.

**Accepted as the S6 freeze** (T05 §1 shapes as delivered; full text in the T05 packet §7): the result family `qualification_campaign_result/v1`, `…_result_authentication/v1`, `…_result_snapshot/v1` (excludes its own receipt), `…_result_intent/v1`, `…_result_receipt/v1`; operations `RESULT_SNAPSHOT`/`COMMIT_E1_RESULT`; T1 `ResultStore.persist_result_intent` / T2 `ResultStore.commit_campaign_result` with the service owning re-validation between them; VOID ordering forced both ways; exact retries byte-identical with the persisted instant; reserve → snapshot → aggregate → commit, receipt binds pre-charge totals and the pre-publication head. Verified in the T2 body: candidate byte-equality, outcome/prefix/checkpoint/receipt-digest re-derivation, chain-walk freshness to the T1 snapshot with only `CAPTURED`/`SIGNING_INTENT`/`SETTLE_WORK` admitted, VOID + cancellation barrier, `SIGNING_INTENT` window, deadline re-check, `historical=true` on retry.

**Rulings carried:** seams 15–19 accepted as listed (19 = the S3 `receipt_bytes`/`status()` defect, being folded by the S3 session; T05's `result_context` workaround removed at integration); post-seam `_advance` writes `RESULT_COMMITTED_*`/`SEALED_PASS` into the canonical budget `state`, the family projection is a mirror; the synthetic-predecessor overlay (`synthetic_predecessor=True` in every record; non-synthetic later-checkpoint rows refused at this revision) accepted; the fixture's re-signing of the S3 builders' placeholder signatures accepted as disclosed; **no seal principal exists at 71732aa** (role_policy roles = qclient/qexec/qg5; `seal_probe_uid` is a validated-but-never-created instance field) — the real principal + credential root is seam row 11 and a host-provisioning change at integration. **S7 GO:** commit the tests-first draft (ten §3 S7 cases) and build `campaign_seal.py`/`seal_service.py` against the frozen §1 shapes; `SealStore.reserve_seal_work` mirrors `reserve_result_work`; the Windows-injectable credential loader (`_loader=`) is accepted. Lines 2/3 + `check` once on the final tree; return per §4/§7; no Linux run; no PR.

### S4/T03 packet drafted and its four decisions ruled, 2026-09-21

`docs/briefs/handoffs/2026-09-21-full-e1-s4-joint-n2-part-b-DRAFT.md` (02c6b51) — authored in parallel with S3's Linux iteration so no packet-authoring gap sits between S3's acceptance and S4's dispatch. Operator rulings (all recommended options): **S4-D1** custody widened once to `PRIMARY KEY(attempt_id, checkpoint)` + `CHECK IN ('N1','N2','PART_A')` at DB `user_version` 9 (S5 needs no layout change; T05's tables become v10 at integration, one-line seam; column names unchanged for T05's accessor); **S4-D2** one capture, one attestation, one assessment with `stage_decisions {N2, PART_B}` and the campaign decision, one receipt bound to the committed N1 receipt — family `/v1` with checkpoint-keyed closed field sets, snapshot `/v7`; **S4-D3** release `/v6` + profile `/v6` with `['N1','N2']`, v5 stays exactly `['N1']`; **S4-D4** the joint `(PARTIAL, NONE)` continuation legal only under a versioned FULL_E1 policy identity, producers/consumers re-pinned together, N1_ONLY keeps rejecting. Freeze on S3's merge (anchors re-taken at the merge head).

### T05 S7 return — build COMPLETE (S6 + S7) at 35c8c08; ACCEPTED AS A BUILD, acceptance proper waits on T04, 2026-09-21

`claude/t05-result-seal@35c8c08` (37b52fe tests-first → 35c8c08 S7 build on c5caa2f). `git diff --stat 71732aa...HEAD` = 8 files, +3370; **none outside the §2 boundary** (verified by name list). Windows: S7 selection 583/0 (`20260921T193910Z-10ee48048f79`), line 2 79+1 (`…T195052Z-00ed24d80186`), line 3 1563/1/1 (`…T195224Z-406964761535`) — the single failure `test_files.py::test_concurrent_archive_publishers_keep_one_immutable_object` is outside T05's surface (no archive/files code in the delta), passed 15/15 in isolation on the same tree (`…T210308Z-afb9db3c5d2f`), disclosed as a load-timing flake rather than re-run away — accepted as disclosed and flagged for its own repair; `check` 0 (`…T210327Z-5d00d9c3c1ee`); `git diff --check` clean.

**Verified in the branch:** `seal_service.sign_committed_pass` recomputes PASS from the committed result bytes, verifies the G5 authentication, the service receipt and the intent's full digest set, signs the fixed payload with an injectable credential loader, and has no publication path; `main()` is a one-shot bounded IPC listener (0600 socket, 256 KiB frames). `SealStore`: `reserve_seal_work` (gated on the committed PASS), `prepare_seal_intent` (T1: payload, key id, signing instant persisted before any signature — signature column nullable for exactly that), `commit_campaign_seal` (T2: exact intent/signature retry, `VOID campaign` refusal, atomic seal + receipt, `SEALED_PASS` via the ruled `state_name` mechanism, `historical=true` on retry), `seal_receipt`/`inspect_seal` with eligibility recomputed from current facts. `request_seal` order: eligibility → `dispatch_lock` → T1 → qseal IPC → `verify_seal_intent` against the enrollment context → eligibility re-check → T2; a signing failure rolls back publication, never the intent. No module-level mutable state (legacy seal suite 24/24 alongside).

**Seam table now 21 + 3 rows** (C-R's 1–19 plus 2a `handle_request` REQUEST_SEAL/INSPECT_SEAL, 6a `runtime.ENTRYPOINTS['seal']`, 11a the installed `qualification-installation/seal.json` + 0400 seal-owned credential, 20 the production service→qseal transport (`seal_service.exchange`; the Windows double's `qseal_sign` removed at integration), 21 the `permitted` ACL rows). Dependency to carry: production `request_seal` needs seam 19 (S3's `CampaignStore.context` receipt defect — fixed on the S3 branch at 0803814; verified at integration). **Disposition:** the T05 build is complete and frozen at 35c8c08; no further T05 work until integration. Acceptance proper (amendment §T05: "accept only after T04, against the real captures") = seams applied on the S4/S5 merge head, the Linux file's cases run under the successor selector (real result-G5 unit, real qseal unit with a separate UID and credential root, both VOID orderings, cleanup absence), one independent review.

### S5/T04 packet drafted and its three decisions ruled, 2026-09-21

`docs/briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md` (52e7836). Operator rulings (all recommended options): **S5-D1** two durable artifacts from one Part A run (initial-prefix result fsynced before the expansion decision, final result after; both archived; crash between = IN_DOUBT with the prefix retained, no resume/replacement pilot/rerun); **S5-D2** the N2 FULL baseline derived on both sides from staged N2 custody (guardian stages the committed capture read-only; worker derives; G5 derives independently via S4's parsers; mismatch refuses); **S5-D3** release `/v7` + profile `/v7` with `['N1','N2','PART_A']`, result/seal route still disabled (T06/S8's flag with T05's integration), snapshot `/v8`. Freezes on S4's merge. The spine T02→T03→T04 now has no packet-authoring gap.

### Coordinator acceptance review — S3 CHANGES REQUIRED (three blockers), 2026-09-22

Executor return `RESOLVED` on `claude/s3-n1-genuine-capture@7405620` (PR #455). **Verified and accepted as far as it goes:** `s2_run_evidence.py 35736618719 --expect-head 7405620` → `ok: true`, record `3a209064a46d43289075847d29e9e096`, scope `S3_N1_CAPTURE`, exit 0/0, source_stable/capture_complete/cleanup_ok/invariants_passed true, 19 required nodes (15 S2 + 4 N1), junit 19/19. The ruled E06/E07 scene is the one implemented (fault-opened T1/T2 window, real qg5 kill inside it, exact redelivery with the original signing instant, byte-identical historical receipt, different candidate refused), and the dead-target gate became causal rather than a relaxed assertion.

**Not accepted — the PR's own checks, absent from §7** (review posted as PR #455 comment 5780265590): **B1** the cleanup gate is unstable on identical bytes — the PR-triggered run of the same workflow on the same head (35743709243) is `19 passed, 1 error` with `S3 owned units remain after cleanup` in teardown and `cleanup.ok: false`; a *killed* transient unit ends `failed` and systemd keeps it loaded until reset, so the g5-death case's unit outlives the 10 s absence poll while a cleanly-exited unit is GC'd — fix at the unit (`CollectMode=inactive-or-failed` on the qg5 and io mount units) plus `systemctl reset-failed` before the poll, keeping the explicit stop and absence proof. **B2** `test_campaign_n1_linux.py` hard-asserts `FP_QUALIFICATION_S3=1` instead of skipping, so the required `Qualification execution boundary (1)/(2)` jobs fail. **B3** `build (3.11)` at 7.97/10 against the 8.00 whole-repo Pylint gate (main is green) — density recipe, no blanket ignores.

**Exit criteria:** B1–B3 fixed; **two** independent clean runs on the identical final head (one dispatched 19-node run read with `--expect-head`, plus this PR's own S2-supervision check green on that head); Windows lines 1–3 + `check` refreshed if any file changed; §4 updated with the new identities. S4 stays undispatched until S3 merges; its packet and rulings are already frozen-pending-anchors.

### T05 follow-up — the S3 settlement rule applied to the result and seal commits, ACCEPTED into the build, 2026-09-22

`claude/t05-result-seal@c3cea75` (`be8dc42` tests-first → `c3cea75` fix, on `35c8c08`; 6 files +346/−22, none outside the §2 boundary — verified). The a8a983e rule in T05's own paths: `ResultStore._settlement_terminal` ends authority from the commit-produced states (`RESULT_COMMITTED_{PASS,FAIL}`, `SEALED_PASS`) and their frozen-bytes stand-ins (`COMMIT_PREDECESSOR_STATES` = the F3 names + `N2_READY`, needed until the enum seam lands), and the committing RESULT/SEAL work completes only in the state its own commit produced (`record_result_transition`'s completion gate; both runner tails skip `COMPLETED` when settlement ended authority). Records: T05 files 33/33 (`20260922T212235Z-e68904e68dbf`), S7 selection 589/0 (`…213752Z-67c474f752f4`), line 2 79+1 (`…215001Z-2100acf14347`), Linux file without its env var 6 skipped (`…215116Z-aeb7a48632bf`), `check` 0 (`…215325Z-578471964b3b`); fail-on-base at `35c8c08` shows exactly S3's P1 shape (`'N2_READY' == 'BUDGET_EXHAUSTED'`).

**Latent defect found and fixed within the boundary:** the seal commit never drove the qseal work's state machine (`record_result_transition`/`settle_result_work` refused every phase but RESULT), so a real seal work would have been stranded `RUNNING` with no settlement — the seal T1/T2 now follow the result commit's shape (CAPTURED→SIGNING_INTENT at T1, SIGNED with the seal receipt at T2, then the shared settle/complete rule). **Ruled kept, not deferred:** `seal_eligibility`/`_seal_predecessor` now refuse `REFUSED_BUDGET_STATES` — spec §2.8 / slice S7 ("FAIL, incomplete, uncommitted, uncertain, exhausted or VOID campaigns never gain a new seal"); before this a committed PASS on an exhausted campaign was still sealable. Disclosures accepted: one journal payload `qualification_campaign_seal_capture/v1`; `SEAL_PHASE`/`SEALED_PASS` now owned by `campaign_result`. **Integration items added:** (i) unify `ResultStore._settlement_terminal` with S3's `CampaignStore._settlement_terminal` into one store helper over one progression-state set, retiring the `N2_READY` stand-in once the enum seam lands; (ii) the branch tree still carries the pre-roll STATE deadline — the integration rebase takes main's `031d79a` roll, never a fresh one.

### Coordinator acceptance — S3 genuine protected N1 capture and committed independent G5 decision, 2026-09-22

**Accepted at `claude/s3-n1-genuine-capture@a8a983e`** (PR #455; merge candidate `3b37f6e` = `a8a983e` + main's `792d416`, which changes only `docs/SESSIONS.md` — no tested or imported byte differs). The executor (GLM) stopped at a coordinator checkpoint near its context limit; the coordinator finished the last defects in its own worktree (`ec41c10`, `a8a983e`, below) and owns the final head.

**Binding Linux evidence — two independent clean runs on the identical final head:**

| Run | Event | Record | Result |
|---|---|---|---|
| 35781007681 | workflow_dispatch | `3cba4ba7d07d43ebbc05be02cb408104` | `s2_run_evidence.py 35781007681 --expect-head a8a983e` → ok; scope `S3_N1_CAPTURE`; 19 required nodes (15 S2 + 4 N1); junit 19/0/0/0; source_stable, capture_complete, cleanup_ok, invariants_passed |
| 35781002126 | pull_request | `88b776bc89f04374880b3000ba1d8670` | same (`--expect-head a8a983e`) |

Superseded but green (kept as history, not binding): 35736618719 on `7405620` (record `3a209064…`, the first 19/19 — its `cleanup_ok` was later shown unstable by 35743709243 on the same head: 19 passed + teardown error); 35759104858 + 35763557929 on `5eb1f3a` (records `d4b1c4ed…`, `9b5576bd…`, the first two-clean-runs pair after the `CollectMode`/`reset-failed` fix); 35769454117 on `f8c00e6` (record `3e38d62e…`); 35777839744 on `ec41c10` (green, but that head still carried the P1/P2 defects below).

**Windows on the final head `a8a983e`:** line 1 (16 files, `--workers 2`) 589/0 (`20260922T203333Z-99f840370895`); line 2 (4 files) 79 + the known Windows symlink skip (`20260922T204541Z-2a56f6b60d76`); line 3 (`tests/ops/qualification` + phase3, `--workers 2`) 1570 + 1 Linux-only skip of 1571 (`20260922T204649Z-8d2846e330dd`); `check` exit 0 (`20260922T212732Z-a20e67808318`); `git diff --check` clean — every record completed 0/0, source_stable, on a clean tree at `a8a983e`. Earlier, on `ec41c10`: line 1 585/0 (`20260922T200457Z-ff4f66c8caba`), line 2 79+1 (`…201840Z-32ac2fb0a79a`), wrapper + manifest 59+1 (`…200059Z-94f67e33bd2c`); the P1/P2 store suites 264/0 (`…202813Z-deaecbfdc34c`). PR #455's own checks: all green on `a8a983e` (both `Qualification execution boundary` jobs, pytest, Pylint/build, S2 supervision, skills, daemon, listener, semgrep); on the merge candidate `3b37f6e`: all green (`CLEAN`/`MERGEABLE`), and its own S2-supervision run 35786085417 is a **third** clean 19-node run, on the exact merge bytes — `s2_run_evidence.py 35786085417 --expect-head 3b37f6e` → ok, record `d863932e92a342c7803fde9d781adb43`, 19 required nodes, junit 19/0/0/0, cleanup_ok.

**What is accepted (the C1 freeze, as built):** the FULL_E1 checkpoint family (`…_checkpoint_result/v1`, `…_attestation/v1` + payload, `…_assessment/v1`, receipt, cutoff, intent) in the v8 tables; the `/v6` snapshot; the four G5-only operations; T1 `persist_checkpoint_intent` / T2 `commit_checkpoint_assessment` with service-owned re-validation under `dispatch_lock`; VOID serialization through the lock; signing recovery (exact retry = byte-identical receipt with the persisted signing instant; a different candidate always refuses); budget accounting for N1/N1_G5; release/profile `/v5` opening N1 dispatch only. **Demonstrated on Linux:** genuine PASS → `N2_READY` and genuine FAIL → `N1_FAILED` through real worker compute (readiness handshake, bounded output mount, execution-key attestation) and the real qg5 host unit; guardian death mid-N1 → `IN_DOUBT`, no capture, across restarts; the ruled E06/E07 scene — the TEST_ONLY `hold_after_intent` fault opens the T1/T2 window, the real qg5 unit is killed inside it, a fresh unit redelivers the exact persisted candidate, the receipt carries the original signing instant, the wire retry returns the byte-identical receipt `historical=true`, and a different candidate refuses; every completed work carries a retained payload identity; all fifteen S2 nodes still green.

**Coordinator review findings and dispositions (review on PR #455, comment 5780265590):** B1 cleanup gate unstable on identical bytes → fixed (`CollectMode=inactive-or-failed` on the qg5 and io mount units + `systemctl reset-failed` before the absence poll; explicit stop and absence proof retained). B2 the N1 Linux file broke the required boundary jobs → fixed in three steps: skip guard (`b61cb67`), its missing import (`15badeb`), and the `--test-only` required-set derivation (`ec41c10`, coordinator: 464 required of 483 registered, zero N1, zero S2; `--s2` 15 and `--s3` 19 unchanged; regression `test_required_nodes_match_the_selected_file_set[--test-only]` fails against `aaf9646`'s byte-exact script and passes on `ec41c10`). B3 Pylint 7.97 → cleared by the density recipe (CI Pylint green). The dead-target gate: `resumed_image`'s `SigCgt` bit 9 invariant was **not** relaxed; the producer retains no RESUMED image for a target that is gone (causal: the readiness token is written only after the handler is installed).

**Independent review (Codex, on `ec41c10`) — two findings, both confirmed and fixed in `a8a983e`** (disposition: PR #455 comment 5784054589): **P1** T2 advanced to `N2_READY`/`N1_FAILED` while the qg5 unit still ran, and the later settlement's overrun went through `_terminal`, which only rewrote `PROVISIONAL`/`BOUND` — an over-budget G5 kept its success; now `_settlement_terminal` ends authority from `CHECKPOINT_PROGRESSION_STATES` too and the receipt stays historical. **P2** the committing G5 work could never reach `COMPLETED` (`_check_budget` refused every non-`BOUND` state; a second gate would have saved `CLOCK_TERMINAL`); now the settled `SIGNED` `N1_G5` work completes in the state its own commit produced. The commit-while-running order was kept deliberately: the qg5 unit carries the S2-accepted kernel CPU bound. Reproductions `test_committed_g5_settles_within_budget_and_completes` and `test_committed_g5_overrun_blocks_the_progression` (CONTINUE and FAILURE) fail at `ec41c10`, pass at `a8a983e`; the Linux PASS/FAIL cases now assert the committing G5 work reaches `COMPLETED` within its reservation — the transition the earlier 19/19 runs never checked. **Carried to T05's integration** (now in its packet): its result and seal commits share the shape and need the same rule.

**Executor disclosures recorded (from its checkpoint return):** (1) the corruption-restore — a first-draft AST `dict()`→literal converter spliced six files mid-expression; detected immediately by `ast.parse`; all thirteen touched files restored with `git checkout --` to `7405620`; the restore also silently reverted the uncommitted skip guard, so `5eb1f3a`'s message claimed an edit its tree lacked; no corrupt bytes were ever committed. (2) `aaf9646`'s message described a derivation its diff lacked (its patch script crashed after the first edit); caught in review; the executor's unpushed repair `6086b9f` was superseded by `ec41c10`, and its "478" count was wrong (483 − 19 = 464, matching CI). (3) One push while a run was in flight (`aaf9646` cancelled the `15badeb` PR run) — a discipline breach, the run's head superseded anyway. (4) `black -S -l 100` reformatted whole changed files, including pre-existing S2 code in them; behaviour-neutral, verified by the unchanged S2 Linux nodes. (5) The TEST_ONLY `hold_after_intent` fault input on the schedule request exists only to open the T1/T2 window for the E06/E07 scene. Lessons (5)–(7) of the S4 packet's carried list come from these.

**Preconditions carried to S4** are in the S4 packet §0 (anchors pinned at `a8a983e`; ten binding lessons; S4 dispatched 2026-09-22 off `a8a983e` in parallel, acceptance-grade Linux only after this merge and a rebase). **Not accepted by this entry:** anything beyond N1 — no N2/Part A, no result or seal authority, no activation; the full-campaign acceptance remains S8/T06's.

### Coordinator checkpoint C2 — S4 CHANGES REQUIRED; §0.6 decisions and the N2 ceiling ruled, 2026-09-24

**State found.** The S4 executor (GLM) pushed its build `a0a03cc` on 2026-09-22 and never returned C2: packet §7 still reads "_Pending._" No S4 session remained live. Companion PR #467 was operator-directed ("port the settlement fix where applicable"; "Implement the 467 and 468 fixes directly"). It merged into `claude/s4-joint-n2` at `80283b1`, where it peeled three S4 defects: `e82ac1e` (v6 setup refusal), `882d46e` (the test did not wait for #461's qg5 settlement) and `1db0017` (the START_CLIENT claim was terminal from `N2_READY`). The fourth layer was left untraced, because that session's egress policy blocked the run artifact. Four consecutive red full runs had tripped the packet's stop rule 2: 35882539669, 35919170318, 35922694962 and 35927503612.

**Root cause, traced from artifact 35927503612.** The tested merge tree `874ecf6` is byte-identical to `80283b1` (tree `5891467d`). Three failing nodes, and the same trace in each:
- the n2work guardian died on its first poll in `_await_dispatch_ack` (`campaign_supervisor.py:1301-1306`). Its liveness gate admits only `PROVISIONAL`/`BOUND`, and every N2 work launches from `N2_READY`;
- `journal.log` holds the `:1306` traceback for guardian pids 4893, 5309 and 5683, and each unit exits with status 1;
- the raise comes before guardian_main's `try`, so no FAILURE or IN_DOUBT was written, and each test's 330 s wait expired.

This is the guardian-side twin of the store gates that S4 and `1db0017` already made phase-scoped. It survived refute-first verification on three lenses: evidence consistency, code reachability, and an alternative-cause search. **Six more N1-only sites sit behind it, and each would have been one more blind Linux run:**
- `_assert_authority` at `:1325`, `:1397`, `:1448` and `:2386`;
- `guardian_task_bound` gives `n2_worker`/`n2_g5` `pids.max = 1`;
- the uid map has no `n2_worker`/`n2_g5` entry (KeyError);
- the compute `COMPLETED` gate is `BOUND`-only;
- `G5_COMMIT_STATES` contains `N2_READY`, so an N2 G5 is "committed" at launch and never resumed;
- the signing-retry finalize is `BOUND`-only and hard-codes `'checkpoint': 'N1'`.

**C2 audit.** The build was reviewed against the frozen packet on five lenses: D1 custody, D2 joint batch, D3 release, D4 policy, and forbidden items/seams. That produced 26 BLOCKING/MAJOR findings. Each was re-verified by two independent refuters, and 23 were confirmed. Beyond the stall layers, the confirmed defects are:
- **the 8→9 custody widening fails on every existing S3 v8 journal.** `widen_checkpoint_layout` builds `CREATE TABLE …_v9 ((…`, a SQL syntax error, and a single-paren fix would still fail the exact-layout walk because the renamed table's SQL is quoted. There is no exact v8 predecessor check before the rebuild, and the frozen S3 v8 literal no longer exists. No test covers any of this; fresh journals take the 7→9 path, which is why CI passed;
- **at v9 the startup integrity walk silently skips** the budget, funding and checkpoint walks (`CampaignStore.integrity` gates them on 6/7/8 and 8). This relaxes an S2/S3 assertion (§6);
- **VOID at v9 no longer records the authority-bearing budget VOID event** (`void()` gate `(6, 7, 8)`);
- **the `/v6` snapshot's S3 closed key set was relaxed in place.** It now accepts N2 entries, and `launch_gate` / `claim_supervision_control` rewrite a `/v7` snapshot back to `/v6` while the N2 entry is present (§6, S4-D2);
- **a v5 installation admits `checkpoint='N2'`** on the checkpoint operations; STAGE persists an N2 row;
- **the joint FAIL/PASS commit path is untested through the service** (`committed_n2` bypasses `service._commit_checkpoint`);
- **§3 refusals are not exercised through the reconstruction**, and the G5 builder does not close the batch shape (population count, stage labels, record consumption; missing halves raise IndexError);
- **E08's N2 half covers only a post-commit overrun.** There is no N2 compute or capture exhaustion case and no restart with the N2 reservation open. `CampaignStore._terminal` still acts only from `PROVISIONAL`/`BOUND`, so budget watchdogs do nothing for N2 phases in `N2_READY`;
- advisory: unset failure caps are recorded as `0` in the joint cutoff; a reused manifest node ID (`test_unsupported_prefix_decision[stages3-PARTIAL-NONE]`) changed meaning; stale scope text.

**Operator ruling — the N2 phase ceiling (M13), 2026-09-24.** Measured on Windows, `run_n2_compute` takes 211.39 s CPU, against 13.36 s for N1 (record `20260924T034139Z-59ce3c4b7643`), roughly 137 s on Linux by scaling. Every phase gets 120 s CPU / 300 s wall with a 20 s orchestration charge, so the payload has about 100 s. The genuine-pass and g5-death cases would therefore be SIGKILLed at the absolute deadline, again silently. The packet's Authority bars ceiling changes, so the question went to the operator. The operator selected "Raise N2 in /v6 only (Recommended)":
- **in the TEST_ONLY `/v6` diagnostic profile only, the N2 compute phase gets 360 s CPU / 900 s wall;**
- v5, every other phase, every statistic and every depth are unchanged;
- the Linux test waits are lengthened to match;
- the real N2 CPU is measured on the first run and recorded.

**Coordinator rulings on the §0.6 decisions:**
1. **Selector and scope.** Adopt the recommendation. `--s4` is a superset of `--s3`, with scope `S4_JOINT_N2`, and the workflow `mode` gains `s4`. `--s3` goes back to installing v5, so `S3_N1_CAPTURE` keeps meaning what C1 accepted: 19 nodes on `/v5`. `s2_run_evidence.py` accepts `S4_JOINT_N2` and binds each scope to its exact required node set, so a 19-node S3 record and a 22-node S4 record can no longer read identically. The stale restatements are corrected: the workflow `mode` text, the README count, the `fixture_install` comment and the N1 Linux docstring.
2. **Genuine Linux N2 FAIL.** Not required. The FAIL commit path stands on the Windows asymmetric cases, provided they run through the service's `COMMIT_CHECKPOINT_ASSESSMENT` path, and §7 discloses this.
3. **`validate_recoveries`' `/v5` literal.** Left unchanged: it is unreachable in N2, because dispatches are non-empty from the N1 launch onward. §7 records the reasoning.
4. **The `_settlement_terminal` seam.** The `ResultStore` unification stays with T05. S4 fixes `CampaignStore`'s own N1-only `_terminal` liveness in its own file, with E08 N2 tests.
5. **S4-D4 reading.** The single global `/v2` policy identity, with every consumer re-pinned, is accepted as the reading of D4. This holds on condition that N1_ONLY's rejection of the joint prefix is asserted by a registered QPOL-01 test and the reused node ID is given explicit, stable IDs.

**Repair order.** Single writer; every step lands on `claude/s4-joint-n2` through the coordinator's repair branch `claude/s4-c2-repair`.
- **R1**: the N2 guardian launch path, M1 plus the six latent sites, with six Windows regression tests and the Linux test hardening (the RUNNING gate, a work-scoped guardian kill, `reply['ok']`).
- **R2**: custody at v9 — an exact-DDL widening with a v8 predecessor check against a frozen S3 v8 literal, integrity at v9, VOID at v9, the `_terminal` liveness and the E08 N2 cases.
- **R3**: snapshot closure — `/v6` holds `{N1}` only, `/v7` requires N2, and the writers choose `/v7` whenever N2 is present.
- **R4**: the release binding for checkpoint ops, thresholds carried as `None`, shape closure in the G5 builder, service-path N2 commit tests, §3 refusal tests, and the QPOL-01/test-ID fixes.
- **R5**: the selector and scope, plus the M13 ceiling.

**Linux discipline.** Stop rule 1 comes first, then subset runs. Subset A is the guardian-death case, which needs R1 only. Subset C is every S4 case, after R5. Then one full run on the identical final head, read with `--expect-head`. Acceptance needs two clean runs and a cross-vendor review under D-codex (b).

**Coordinator process disclosures:**
- The R1 production patch is the diagnosis workflow's 14 exact textual replacements, each anchored once. The coordinator applied them by script: GLM hit its 60-iteration cap on a dry run of the same patch. GLM ported the regression tests and hardened the Linux file.
- The patch was first applied in the executor worktree `mfo-s4-wt`. It was then moved to the coordinator-owned `.claude/worktrees/s4-c2-repair`, and `mfo-s4-wt` was restored to its clean `80283b1` state.
- The existing execution suites passed 187/187 on the patched supervisor. That record is **source-unstable**, because a concurrent edit landed during the run, so it is not evidence. The evidence comes from the committed repair head.

**Not accepted by this entry:** S4 itself. There is no Linux evidence yet, and no N2/Part A authority, activation or statistical dispatch.

### Coordinator handoff — end of 2026-09-24 (campaign ownership passes to the next coordinator session)

Recorded under STATE's handoff obligation (campaign record §58): the coordinating role passes to **the next coordinator session that opens [the 2026-09-24 coordinator handoff](../../briefs/handoffs/2026-09-24-full-e1-coordinator-handoff.md)**; until one does, the role rests with the operator. State at `main@d1d6423`: S1–S3 accepted; **S4 CHANGES REQUIRED** at C2 with the ruling merged and R1/R5 recorded on `claude/s4-c2-repair`, while **R2–R4 remain outstanding**; no acceptance-grade Linux evidence on the repair head; S5 unfrozen; T05 build frozen. External: T08 R3 = NONE (D-broker void; operator ruled item 1 — hold live release, vendor question, amendment scope); T10 step 4 finds per-path source re-verification the likely budget-dominant term (extrapolated, to be confirmed by a synthetic probe); T07 blocked on three S2 source facts; T00 INSUFFICIENT on P7(b). At this correction checkpoint #480, #483 and #489 are merged; the open queue is this handoff (#490), conflicted #482, stacked #488 and held #486. The handoff §3 records the conditional sequence. This entry accepts nothing and grants nothing.

### Coordinator transfer — Claude Code continuation, 2026-09-25

At the operator's request to stop the Codex implementation and hand off the rest to Claude Code, ownership passes to the next Claude Code session that reads [the committed continuation handoff](../../briefs/handoffs/2026-09-25-full-e1-claude-continuation.md). R1–R5 repairs and independent review are complete at `8f18c57`; Windows evidence is retained (803/0 line 1; 80/1 line 2; 1703/1 line 3; check passed with disclosed expected skips/advisories). Full Linux branch run 36180568493 has a success badge but its artifact is unread; PR run 36181780676 is active. PR #501 is draft; S4 remains NOT ACCEPTED. The local repair branch merged documentation-only `main@d92d828` at `9422078`; that merge and this handoff are intentionally not pushed while the PR Linux run is active. The successor owns artifact validation, safe final synchronization and PR readiness, then S5 → T05 integration → S8 under the existing acceptance and operator-merge boundaries. This transfer grants no production or live authority.

### Coordinator checkpoint C2 close — S4 ACCEPTED, 2026-09-25 (Claude Code)

The C2 bar was read from records: two artifact-read S4_JOINT_N2 Linux runs, 36180568493 (dispatch, head `8f18c57`) and 36181780676 (PR merge `fa4f5a6`, tree-identical to the pushed main merge). Each passed 22/22 required nodes with zero skips and cleanup ok. The frozen-head Windows lines 1–3 and `check`, PR Pylint 8.09 and the cross-vendor review close (ruling 5's stable-ID half closed by the coordinator) complete the bar. Hashes, identities and residual conditions are in the [S4 packet's acceptance read](../../briefs/handoffs/2026-09-21-full-e1-s4-joint-n2-part-b-DRAFT.md#coordinator-acceptance-read--claude-code-2026-09-25). The acceptance is conditioned on the pushed documentation head's PR S2 run reading `ok`. Next: operator merge GO for PR #501; then freeze S5 at the merge head (held 2026-09-25 — see [the S5-hold entry below](#operator-ruling--s5-freeze-held-2026-09-25)). This entry grants no production, activation or live authority.

### Operator ruling — S5 freeze HELD, 2026-09-25

The operator ruled on 2026-09-25: "merge 501, hold the S5 freeze" (recorded on [PR #501](https://github.com/Joshua-Asante/first-passage/pull/501#issuecomment-5840609727) and [PR #504](https://github.com/Joshua-Asante/first-passage/pull/504#issuecomment-5840609899)). PR #501 merged at `228447c`. The S5 freeze is **HELD** until the operator rules on the decisions in the [qualification-assurance contract delta](../../notes/audits/2026-09-25-qualification-assurance-contract-delta.md#immediate-proposed-decision-points) (#504): the §5.1 boundary list, N1 (resource accounting) and N2 (interruption recovery). The hold grants and changes nothing else: no S5 dispatch or freeze, no T05 or S8 acceptance, and no production, activation or live authority. Recorded 2026-09-26 at the operator's instruction "yes, add the S5-hold ledger entry to 505".

### Operator ruling — S5 directions adopted, hold kept, 2026-09-26

Operator decisions, 2026-09-26. Source: "operator ruling and coordination, 2026-09-26, relayed in session", together with the operator's structured-question answers the same day (the option selected for these rulings: "Adopt D1–D3 directions, keep hold", as the B–D decision packet's R-S5 row (PR #518) also records it). The written ruling is the governing text; it supersedes any shorthand recording of the same rulings made from the structured-question answers. Its §5 (S5 directions) and §6 (resource-envelope decision) decide the items of the [S5 decision draft](../../notes/2026-09-26-s5-decision-draft.md) (PR #517):
- **D1–D3 adopted as S5 directions** (draft §0), in the ruling's words below. The rest of the draft's D1–D3 text (for example the §5.1 boundary set B-1..B-5 and its conditions, the per-phase direction items and the rule R1–R10) is the draft's recommendation, not ruling text; its owner-text form is reviewed under RC-2. In the ruling's words:
  - D1: "Service-generated salt; private worker/G5 access; no client disclosure while computation or recovery remains possible." (draft §1)
  - D2: "Retain per-phase accounting." (draft §2)
  - D3: "Implement bounded same-sample recovery in a separate slice after S5 and before S8." (draft §3)
- **Admission crash, accepted by the operator.** "Joshua explicitly accepts that an admission crash after salt binding but before capture consumes and closes the attempt, preserving its identity and salt without continuing admission or generating another." (draft §1.4)
- **RC-6 retained.** "Retain RC-6." RC-1..RC-6 are in [S5 draft §5](../../notes/2026-09-26-s5-decision-draft.md#5-s5-release-conditions).
- **Gates for the seed view and host attestations.** The ruling directs: "Assign seed-view implementation and host attestations to their specified gates." It names no gate, owner, slice or record location. The seed view's gate in the draft: the client plan-view seed change (seed digests only) before F1, with an F1 admission check that refuses while the client can fetch seed values (draft §1.4, RC-4). For the attended host reads OF-1..OF-7 the draft specifies two gate sets that differ for OF-5..OF-7: its §1.3 table and its §1.5(a) proposed owner text (draft §6 Q12). This entry does not choose between them; the discrepancy stays open for the coordinator's owner-text and RC-5 work. The assignment is not yet made: RC-4 stays unmet until the change lands or its owner record holds the scheduling text RC-4 requires (a named owner and slice, the §2.2a client-view amendment applied, the F1 admission check), and RC-5 stays unmet until an owner record holds the assignment text (an owner for each read, its gate and where the record lands).
- **Resource-envelope decision.** The coordinator prepares a concrete measurement proposal identifying the maximum-expansion workload, the reference runtime, CPU/wall/memory capture, the proposed margin and budget feasibility, and returns the measurement-and-margin rule for operator approval. No numerical rule is approved yet. Once the rule is approved, the coordinator may apply it to TEST_ONLY diagnostic ceilings with recorded evidence. Production budgets remain separately governed. This preparation does not authorize held S5 execution. S5 measurement preparation is a separate bounded handoff; combined acceptance stays with the coordinator.
- **Hold kept.** In the ruling's words, S5 release remains "subject to their recorded gates", and the resource-envelope preparation "does not authorize held S5 execution". The coordinator returns "an RC-1–RC-6 status table and, when supported, a concrete S5 release proposal". The hold recorded in the entry above therefore stays: the S5 freeze is **HELD**. The release conditions are RC-1..RC-6 of [S5 draft §5](../../notes/2026-09-26-s5-decision-draft.md#5-s5-release-conditions), and under that section only an operator ruling recorded as a new entry in this ledger releases the hold. That release gate is the draft's, cited here; it is not ruling text.
- **Owner text.** After the stack (#515–#518) lands, the coordinator applies these decisions to their canonical owners and reconciles dependent wording. This entry applies none of the draft's proposed owner amendments (draft §1.5, §2.5, §3.4); RC-2 requires them accepted by the operator and applied.

**Not granted:** no S5 release, freeze, dispatch or execution; no approved numerical measurement-and-margin rule; no statistical dispatch; no Gate B, C or D acceptance; no production, activation or live authority. The ruling does not independently add merge authorization. Its closing boundary: "Gate A stays accepted. B–D acceptance, S5 release, order-producing drills, production qualification, deployment and arming remain subject to their recorded gates."

### Operator ruling — Part A measurement rule conditionally approved, S5 held, 2026-09-26

Operator decision, 2026-09-26, given in session by Joshua through a structured question. He selected "Conditional Part A-only approval", whose text was Astra's recommendation; it is recorded here as his decision. It rules, conditionally, on the measurement-and-margin rule returned by the [S5 Part A measurement proposal](../../notes/2026-09-26-s5-part-a-measurement-proposal.md) (§4 and §8, as corrected in PR #519; card: [S5 Part A handoff](../../briefs/handoffs/2026-09-26-s5-part-a-measurement-proposal.md)). This entry owns the ruling; the proposal and its card carry dated pointers.
- **Conditionally approved: the proposed numerical defaults, for PART_A TEST_ONLY measurement only.** CPU multiplier 2.0 (m_c, PA-1); wall multiplier 3.0 (m_w, PA-2) with the proposed 30-second launch allowance (L); memory multiplier 1.5 (m_m, PA-3a/PA-3b); warm-repeat spread threshold 1.30 (§3.2, PA-4); service/harness discrepancy threshold 1.25 (PA-5); the retained shared floors (120 s CPU, 300 s wall) and upward rounding. **Not** for other phases and **not** for production.
- **Applicability.** The rule becomes applicable only after the identified measurement defects are corrected and reviewed, including:
  - a concrete way to exercise maximum expansion through the built adapter, including the baseline derivation and real artifact writing;
  - aggregate memory evidence: a lower bound cannot establish memory feasibility;
  - separation of missing permission, invalid measurements and genuine evidence against the accounting design;
  - measurement in the worker image where practicable, with any runtime mismatch explicit and requiring validation.

  The pilot-budget formula needs validation under the service's throttling. *(Recording consequence, not ruling text: until the rule is applicable, the proposal's §6 application procedure does not start and no ceiling is applied under it.)*
- **Authorized:** preservation of the existing S4 evidence (done 2026-09-26: primary checkout `local_artifacts/s4-linux-run-logs-2026-09-25/`, 222 files in `SHA256SUMS`, whose SHA-256 is `e2c14228…189a7`; recorded in the card's coordinator correction); and preparation of the corrected harness/workflow. Its exact dispatch scope is returned for approval; no dispatch is authorized by this entry.
- **Not closed, not authorized.** No provisional ceiling closes RC-3. No S5 execution and no production budget is authorized.
- **N2 kept separate.** The coordinator returns an explicit `/v7` N2 disposition: no silent revert or carry-forward.
- **Staged gate amendment.** The coordinator returns an explicit staged gate amendment separating permission to build S5 from acceptance of its completed adapter. C3 adapter measurements cannot count as completed pre-build evidence.
- **Hold kept.** S5 stays **HELD**.

**Bearing on the proposal's §8 decisions (recording cross-reference, not ruling text).** Decision 1: the listed defaults are conditionally approved within the scope above; the pilot-budget formula (PA-1's `1.5 × P̂` term, PA-2b) is not among the listed defaults and needs validation. Decision 2: PART_A only; the phase-generic form is not approved. Decision 3: not decided; it returns as the N2 disposition. Decision 4: Stage 0 preservation is done; preparation of the corrected harness/workflow is authorized and its dispatch scope returns for approval; the worker-image condition above applies. Decisions 5–7 are not decided as posed; "no provisional ceiling closes RC-3" and the applicability conditions (aggregate memory evidence; separation of outcomes) bear on them.

**Returns owed by the coordinator:** (1) the corrected harness/workflow and its exact dispatch scope, for approval; (2) the explicit `/v7` N2 disposition; (3) the explicit staged gate amendment (build permission separate from completed-adapter acceptance).

**Not granted:** no S5 release, freeze, dispatch or execution; no ceiling set or applied; no production budget or cap; no measurement dispatch; no RC closed by this entry; no Gate B, C or D acceptance; no production, activation or live authority.

### Operator direction — S5 build entry separated from Checkpoint C3 acceptance, 2026-09-27

**Source.** An operator direction given in session on 2026-09-27: "Correct circular prerequisites first, particularly S5's requirement for measurements that depend on the adapter being built … Separate build-entry conditions from C3 acceptance conditions. No requirement to produce evidence from unbuilt code before allowing its construction." The operator's review of the first draft (`9448373`, same day) added three points:
- pre-build feasibility is arithmetic on proposed values, and the executed binding check is required at C3;
- RC-4/RC-5 assignments can be made now, with only their implementation and attestation staged later;
- preparation authority does not authorize the measurements.

The sequencing record is the [deployment-checklist addendum 2026-09-27](2026-09-20-tradeify-deployment-checklist.md#addendum-2026-09-27--staged-acceptance-evidence-proportional-to-the-next-step) §0–§1.1. This entry records how S5's release conditions (S5 draft §5 RC-1..RC-6) now divide. The measurement inputs are the [#519 measurement proposal](https://github.com/Joshua-Asante/first-passage/blob/8c15f1853e64f14f50995e3f1c55a620a0f674b7/docs/notes/2026-09-26-s5-part-a-measurement-proposal.md) at its pinned head, which carries its coordinator review "ACCEPTED AS INPUT".

| Stage | Conditions | Status 2026-09-27 |
|---|---|---|
| **Build entry** (releases the hold for the TEST_ONLY build only) | **RC-1**: D1–D3 ruled. **The §3.4(d) text** applied (S5 draft §4, consistency correction). **RC-4/RC-5 assignment**: the seed-view owner and slice, with the F1 admission-check text, and an owner, gate and record location for each of OF-1..OF-7, resolving S5 draft §6 Q12. **RC-6**: the packet re-anchored at the release head, including #519's findings that the (2, 4, 2) fixture cannot expand and the three `/v7` profile pitfalls. **RC-3a**:<br>– an operator-approved measurement-and-margin rule;<br>– a valid (PA-4) record from an operator-approved forced-expansion measurement of the **existing** `_run_part_a` on the reference runtime (#519 Stage 1b);<br>– the rule applied as a **provisional** PART_A TEST_ONLY ceiling, with D̂ uncovered;<br>– Σ-feasibility shown as **arithmetic on the proposed `/v7` values** (#519 proposal §5).<br>Then an operator hold-release entry here | **RC-1 met** on `main` (#517 merged at `5ad04cf`). The others are open. The measurement dispatch is prepared under [handoff H1](../../briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md#h1--s5-measurement-correct-the-519-proposal-return-a-measurement-dispatch) and executed only after the operator approves it. *[2026-09-28: superseded. The [CP-1a ruling](#operator-ruling--cp-1a-decisions-16-adopted-as-recommended-hold-kept-2026-09-27) approved the bounded dispatch (decision (2)) and met the RC-4/RC-5 assignment for build entry (decision (5)). The [H1(c) acceptance](#operator-acceptance--h1c-full-text-accepted-build-entry-sections-to-be-applied-2026-09-27) applied the §3.4(d) text and the RC-6 re-anchor, and RC-6 is met when CP-1b records the reviewed revision. RC-3a stays open.]* *[Status 2026-09-28, after the measurement: see the [CP-1b packet entry](#coordinator-cp-1b-packet--build-entry-status-2026-09-28). RC-1, the §3.4(d) text, the RC-4/RC-5 assignment and RC-3a are met there, and RC-6 is met subject to CP-1b naming the revision.]* |
| **Checkpoint C3 and S5 acceptance** | The S5 packet's C3 items. **RC-3b**:<br>– the adapter-specific measurement (#519 Stage 1c), which covers D̂ and ends the provisional status;<br>– the **executed** `bind_budget` Σ-feasibility check on the built `/v7` profile;<br>– the Stage 2 service-route consistency check (PA-5).<br>Inside the approved rule the coordinator re-applies with an entry here; outside it, an operator ruling. The full RC-2 owner-text set accepted and applied | ~~Open~~ *2026-10-01:* **C3 ACCEPTED**, and **S5 ACCEPTED for TEST_ONLY** on #578's merge at `1fe99fa` ([ruling](#operator-ruling--c3-accepted-s5-accepted-for-test_only-on-landing-2026-10-01)). D-S5-1/D-S5-2/D-S5-3 are open until both fix slices merge (#586, merged `981eb12`; then the D-S5-3 slice, #589), before T05 R1 |
| **Before F1** (expanding authority) | The RC-4 seed-view change landed, with its F1 admission check, and S5 Q9 decided in that slice (C3 ruling, 2026-10-01); OF-1..OF-7 attested by attended reads; K3 built. *[Corrected 2026-09-27: the OF attestations fall due at the gates the RC-5 entry below assigns; before F1 that is OF-7 (G-F1), and the full set is read at CP-8.]* | Open |

**Relation to the 2026-09-26 conditional ruling (recorded 2026-09-27, when #519's records reached this branch).** The [2026-09-26 entry](#operator-ruling--part-a-measurement-rule-conditionally-approved-s5-held-2026-09-26) asked the coordinator for three returns. This direction and the 2026-09-27 ruling below are its return (3), the staged gate amendment. The CP-1a packet ([H1 r2](../../notes/2026-09-27-s5-part-a-measurement-proposal-r2.md)) carries returns (1), the corrected harness/workflow and its dispatch scope, and (2), the `/v7` N2 disposition. Its two H1 acceptance conditions restate that entry's first two applicability conditions. The 2026-09-26 entry's other conditions still apply to the packet: separation of outcomes, the worker image where practicable, and validation of the pilot-budget formula. The 2026-09-26 entry conditionally approved the numerical defaults for PART_A TEST_ONLY, applicable only after the defects are corrected and reviewed. The 2026-09-27 ruling keeps them as candidates until the packet is ready. The two readings agree: no default applies before CP-1a. That entry also records the S4 run logs preserved on 2026-09-26 in the primary checkout. Whether that set covers Stage 0's inputs, which would lift the 2026-10-09 expiry from Stage 0, is for the coordinator to confirm at CP-1a.

**Not changed.** The hold stays **HELD** until an operator ruling recorded here releases it. No rule, measurement, CI-configuration change, Linux dispatch or artifact download is approved. No S5 dispatch, freeze or execution, statistical dispatch, production budget, production, activation or live authority follows from this entry. Production ceilings and caps remain frozen with F1 by their owners.

### Operator ruling — S5 staged gates approved, Part A-only rule scope, hold kept, 2026-09-27

**Source.** In session on 2026-09-27, the operator adopted this ruling by structured answer ("S5 staging, hold kept") to the text relayed the same day. The relayed text governs: "Approve the staged S5 build-entry/C3 structure, but retain the hold. Return the corrected Part A–only measurement rule and executable dispatch for CP-1a." Its detail, verbatim:
- "Approve: Existing-engine measurement and proposed-value budget arithmetic for build entry. Adapter-specific measurement and the executed `/v7` binding check at C3. Assigning seed-view and host-check owners now, with implementation and attestations due at their specified later gates."
- "Do not yet approve measurement execution or release S5. H1 must first return its corrected, executable dispatch, including forced expansion through the adapter and complete aggregate-memory evidence."
- "For the margin rule, my recommendation remains Part A–only TEST_ONLY scope. Keep the proposed multipliers as candidates until that packet is ready; do not silently extend the rule to N2."

**Effect.**
- The staged structure in the [2026-09-27 direction entry](#operator-direction--s5-build-entry-separated-from-checkpoint-c3-acceptance-2026-09-27) is **approved**: build entry, Checkpoint C3/acceptance, and before F1.
- The RC-4/RC-5 **assignment** may be made now. The coordinator records it here when [handoff H7](../../briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md) returns.
- The margin rule's scope is **PART_A only, TEST_ONLY**. The #519 proposal's multipliers remain candidates.
- `/v7`'s N2 ceiling therefore cannot come from the rule. It needs a separate operator ruling (for example, extending the M13 "/v6 only" ruling), which is returned with the CP-1a packet.
- H1's corrected dispatch must meet two acceptance conditions:
  - (1) Stage 1c forces maximum expansion **through the built adapter**, with the real N2 baseline derivation and real artifact writing;
  - (2) **complete aggregate-memory evidence**. A lower-bound memory fallback leaves memory feasibility unverified and cannot support the rule's application.

**Not granted:** measurement execution, CI-configuration change, Linux dispatch or artifact download; an approved numerical rule; S5 release, freeze, dispatch or execution. The hold stays **HELD**.

### Coordinator assignment — RC-5 host checks (recorded) and RC-4 seed view (slice pending the operator), 2026-09-27

**Source.** The operator ruling of 2026-09-27 ("Assigning seed-view and host-check owners now, with implementation and attestations due at their specified later gates"), acting on the [H7 return](../../notes/2026-09-27-host-obligations-assignment.md). The RC-5 assignment and the resolution of S5 draft §6 Q12 are coordinator acts: the 2026-09-26 entry above leaves Q12 "open for the coordinator's owner-text and RC-5 work". The RC-4 **slice** is one "the operator names" (S5 draft `:363`); this entry records it as the coordinator's proposal until the operator names it at CP-1a (item 5 of the [H1 r2 packet](../../notes/2026-09-27-s5-part-a-measurement-proposal-r2.md)), and the RC-4 assignment is not met until then.

**RC-5 (OF-1..OF-7).** S5 draft §6 Q12 is resolved to the stricter reading, which only adds gates: every OF is verified by an operator-attended host read at production-host provisioning (CP-8), before any production-authority release (any `OPERATOR`-class release, instance, trust-domain or key enrollment, and before CP-8 admits the production attempt), and after any access change. In addition, OF-5 is read before any arm and at each session GO, OF-6 at TB-I3 (NOT_APPLICABLE unless E3 is adopted), and OF-7 before F1 admission. Verifier: the operator (attended). Recorder: the operator; the coordinator checks completeness and records each attestation here. Record: a private raw transcript held by the operator outside every checkout and archived in `first-passage-archive`, plus a public attestation `docs/notes/qualification_host/attestations/<date>-<gate>.json` (schema `qualification_host_of_attestation/v1`: booleans, octal modes, role names, enumerated codes, dates and hashes only, no free-text field), linked here by path and SHA-256. An attestation satisfies a gate only if no trigger for that OF occurred between the read and the gate. Re-verification triggers:

| OF | Triggers (each also: host rebuild or reprovision) |
|---|---|
| OF-1 | account, group, sudoers or sudoers.d change; Docker install, upgrade or socket-permission change; new agent harness, agent OS account or cloud agent environment; change on an agent-hosting workstation account to SSH keys, SSH agent or forwarding, credential helpers or remote-access tooling |
| OF-2 | change under `/etc/polkit-1/rules.d`; principal creation, deletion, UID or authentication change; polkit or systemd upgrade |
| OF-3 | key generation, rotation, enrollment or revocation; new GitHub Actions secret (repository, environment or organization) or new workflow; new worktree root or agent environment |
| OF-4 | enrollment, release install, trust-domain or instance-document change |
| OF-5 | Fly membership or token change; broker credential issue or rotation; new agent environment or cloud environment secret; rail redeploy by a new path; each arm; each session GO |
| OF-6 | E3 adoption; GO key generation, rotation or device change; new agent environment; TB-I3 |
| OF-7 | release install; data or scratch tree binding change; qg5 route change; backup or snapshot configuration change |

An unverified OF is reported as "enforcement not established". The OF definitions' owner is boundary spec §3.1 once RC-2 applies S5 draft §1.5(a). Contract questions CQ-1..CQ-3 are open.

**RC-4 (client plan-view seed change).** *2026-10-01: this slice also decides S5 open question **Q9** (when a never-retried, retry-eligible IN_DOUBT counts as closed, and so when the salt is revealed), before F1 ([C3 ruling](#operator-ruling--c3-accepted-s5-accepted-for-test_only-on-landing-2026-10-01)).* Owner: the qualification coordinator, through this ledger. Slice (proposed; the operator names it): "K3/RC-4 — service salt and client plan view", covering the digests-only client view, the receipt's `client_view_sha256`/`client_view_byte_length`, `tb-s2-rng-v3` with service-generated salt, commitment and reveal, the S5 draft §1.6 tests and the service-side refusal of condition 1 below. It moves K3 out of TB-F1, where S5 draft §4 placed it. It is dispatched after S5 acceptance and lands before S8/T06 dispatch; its order against the D3 slice is set at dispatch. That S8/T06 precondition is sequencing, which the [checklist addendum 2026-09-27](2026-09-20-tradeify-deployment-checklist.md#addendum-2026-09-27--staged-acceptance-evidence-proportional-to-the-next-step) governs; this entry does not change the addendum, which must record it separately once the operator accepts the slice. It depends on the full-E1 spec §2.2a amendment of S5 draft §1.5(d), applied under RC-2 at Checkpoint C3 and not by this entry.

**F1 admission check (RC-4; AUDIT-2026-09-25-qualification-assurance-contract-delta#K3).** The production attempt is not admitted while the `client` role can fetch a seed value or the salt. Admission refuses unless every condition holds, and it evaluates them **before** the transaction that binds the F1 budget and generates the salt, so that a refusal generates no salt and consumes no attempt:
1. The contract's RNG recipe is `tb-s2-rng-v3`, and the installed release's plan-view mode for the `client` role is `client_view_digests_only`. The service refuses a `tb-s2-rng-v3` admission on any release without that mode.
2. The installed release digest equals the release named in F1, and that release was accepted with the negative client cases of S5 draft §1.6 passing on Linux on its bytes: no salt or seed value reaches `client` through `STATUS`, `FETCH_PLAN_CHUNK` or the receipt before closure.
3. The admission receipt schema binds `client_view_sha256` and `client_view_byte_length` beside `plan_sha256` and `plan_byte_length`. The client verifies the reassembled client view against them.
4. An OF-7 attestation at gate G-F1 is recorded for this host after the installed release was installed, with no OF-7 trigger since.

Any failed condition refuses admission. The refusal is recorded and is not a consumed attempt.

**Status.** The 2026-09-26 entry above required RC-4's owner record to hold "a named owner and slice, the §2.2a client-view amendment applied, the F1 admission check". The 2026-09-27 direction divides that by stage: build entry needs "the seed-view owner and slice, with the F1 admission-check text", and the full RC-2 owner-text set, §2.2a included, is applied at Checkpoint C3. On that reading, and **once the operator has accepted the RC-4 slice**, this entry meets the RC-4/RC-5 **assignment** at build entry; the coordinator confirms that status on recording. The implementation (the RC-4 change landed, K3 built) and the attestations (OF-1..OF-7) remain before F1, as the 2026-09-27 direction's "Before F1" row states. *[Corrected 2026-09-27: the attestations fall due at the gates this entry assigns under RC-5, with OF-7 before F1 admission and the full set at CP-8.]*

**Not granted:** S5 release, dispatch or execution; owner text applied; host provisioning or spend; credential or key creation; F1, CP-6 or CP-8 decisions; production, arm, deployment or live authority. The hold stays **HELD**.

**Recorded state (2026-09-27).** RC-5 is **assigned** (coordinator act). The RC-4 slice is **proposed, pending the operator at CP-1a item 5**, so the RC-4/RC-5 build-entry condition is not yet met. Host spend and sizing stay owed before CP-8 (checklist T11's measured envelope; the $700-ceiling scope is the single CP-2 question F-4 of the commissioning packet). *[Corrected 2026-09-27: the operator accepted the RC-4 slice at CP-1a decision (5) the same day; the coordinator confirmation there records the RC-4/RC-5 assignment at build entry as met (see the CP-1a ruling entry below).]*

### Coordinator entry — CP-1a packet reconciled with #519's merged corrections, 2026-09-27

**Source.** The operator's instruction "prepare the CP-1a packet" (2026-09-27), and the operator's sequencing guidance on PR #520 the same day. #519 merged its own review corrections to r1, and the [2026-09-26 conditional ruling](#operator-ruling--part-a-measurement-rule-conditionally-approved-s5-held-2026-09-26) was given on them. The CP-1a packet ([H1 r2](../../notes/2026-09-27-s5-part-a-measurement-proposal-r2.md)) predated both. Its [§16](../../notes/2026-09-27-s5-part-a-measurement-proposal-r2.md#16-reconciliation-with-519s-merged-corrections-and-the-2026-09-26-conditional-ruling-2026-09-27) now crosswalks the two in 28 rows. Its [§14.1](../../notes/2026-09-27-s5-part-a-measurement-proposal-r2.md#141-refreshed-decision-list-2026-09-27) is the refreshed decision list.

**Documentary corrections adopted by the coordinator** (each stricter; none is an operator decision):
- **C2:** the proposed SR-9, which keeps the packet's unnecessary-expansion rejection out of the SR-3 callable;
- **C3:** after CP-1a and the RC-6 fold-in, a missing SR or a failing P at C3 is a C3 nonconformance;
- **C6 and C25:** the PA-3a/PA-3b memory split, with PA-3b checked at Stage 2;
- **C8:** missing memory evidence is relabelled as not invalid;
- **C21:** PA-5 re-application without a valid forced Stage 1c arm stays provisional.

**Coordinator reading superseded.** For D2 timing, the packet now recommends the three-way outcome split (C7): blocked, invalid, and bound not establishable. That recommendation follows the 2026-09-26 ruling's requirement to separate missing permission, invalid measurements and genuine evidence. It replaces the coordinator's earlier release-point reading (critic X-10). The operator decides at CP-1a decision (4); the alternative stays stated there.

**CP-1a is six decisions**, presented together:
1. the measurement parameters: confirm the 2026-09-26 applicability conditions, and decide what that approval left out;
2. the bounded dispatch and runtime;
3. the `/v7` N2 ruling;
4. D2 timing;
5. the RC-4 slice;
6. the Stage 1c seam and its signed-route exclusion.

What is already ruled is not reopened. Stage 0 is optional calibration. The 2026-10-09 expiry binds only if the preserved S4 set does not cover Stage 0's inputs, and that coverage is verified locally, owed. M2 is not a CP-1a prerequisite.

**Not changed.** No rule is applied, no measurement approved, no ceiling set. The hold stays **HELD**. Accepting the packet is not approval to execute it. *[Superseded 2026-09-27 by the next entry: the operator ruled CP-1a the same day and approved the bounded measurements (decision (2)). The hold stays.]*

### Operator ruling — CP-1a decisions (1)–(6) adopted as recommended, hold kept, 2026-09-27

**Source.** In session on 2026-09-27, the operator answered the six CP-1a decisions of [H1 r2 §14.1](../../notes/2026-09-27-s5-part-a-measurement-proposal-r2.md#141-refreshed-decision-list-2026-09-27) by structured answer, choosing the recommended option each time:
- (1) "Confirm as recommended";
- (2) "All stages, image-first";
- (3) "Extend M13 values";
- (4) "Three-way split";
- (5) "K3/RC-4 slice";
- (6) "§7 seam + SR-9, hard proofs".

The recommendation texts in §14.1 and the option texts relayed in session govern.

**(1) Measurement parameters.**
- The 2026-09-26 applicability conditions are **confirmed met for the provisional build-entry application**, with the §16 resolutions adopted in the [coordinator entry above](#coordinator-entry--cp-1a-packet-reconciled-with-519s-merged-corrections-2026-09-27). Condition 4 (the worker image) is handled through (2). Condition 5 (the pilot-budget validation) is staged to C3.
- **The pilot-budget term** (PA-1's `1.5 × P̂`, with PA-2b) is kept in the provisional application. It is validated at C3 from Stage 2, through SR-8's export extended with the PART_A result's `probe_seconds` and `predicted_seconds`. It becomes final only when that check is recorded.
- **Memory:** PA-3a applies at build entry and PA-3b at C3. PA-3b's composition `m_m × (P₂ + max(0, M̂ − M̂ₚ))` is accepted as a provisional C3 check, with its additive assumption named UNVERIFIED in the application entry.
- **PA-4's re-run caps** (r2 §12.7) and the §9 re-measurement triggers, including the 0.8 thresholds, are **approved as written**.
- The numeric defaults stay as conditionally approved on 2026-09-26: PART_A TEST_ONLY only.

**(2) Measurement dispatch and runtime, approved as a bounded dispatch (r2 §12).** The coordinator executes within it, under H1 step (b), without asking again:
- **(a) Stage 0:** the local read of the preserved S4 artifacts in the operator's primary checkout, optional calibration only, with its public-clone review. The coverage check (r2 §16.4) runs first.
- **(b) Stage 1a:** Windows harness validation on the Windows host.
- **(c) Stage 1b:**
  - the dispatch-only measurement workflow file, a CI-configuration change, landed on `main` by the operator's merge if GitHub requires that;
  - `ci.dispatch` for that workflow only;
  - download of that workflow's own artifacts;
  - all within the §12.7 caps.
- **(d) Runtime: image-first.** Step (b) first records whether the worker build context can carry the harness and fixtures. If it can, Stage 1b runs in the worker image. If it cannot, it runs on `host_venv`, the finding is recorded, and PA-5 at C3 validates the mismatch.
- **(e) Stage 1c at C3:** approved, conditional on the (6) set and on the coordinator's recorded read of the `--stage 1c` harness diff. Stage 1c ends the provisional status with the worker-side residual (r2 §16 C4) named and carried by PA-5.
- **(f) Stage 2:** no new authority. It needs the SR-8 export.
- **Planning bound** (arithmetic, r2 §12.6): 368 runner-minutes worst case, or 628 with the SR-5 contingency.

**(3) `/v7` N2.** The M13 values, **360 s CPU / 900 s wall**, are extended from `/v6` to the **`/v7` TEST_ONLY diagnostic profile only**. The extension is explicit, so it is not the silent carry-forward the 2026-09-26 ruling excluded. Stage 0 may inform N2 but cannot set it. No N2 production value follows, and the margin rule does not apply to N2.

**(4) D2 timing: the three-way split** (r2 §16 C7):
- (i) A Σ failure from a valid record is the D2 ACCOUNTING-DESIGN FALSIFIER stop (r2 §10.3).
- (ii) Missing permission, or a run not executed, never engages the falsifier. It keeps the hold, because CP-1b needs RC-3a.
- (iii) An invalid measurement is investigated and re-measured only under a fresh approval.
  - *Operator-confirmed interpretation, 2026-09-27, reconciling (iii) with (1) and (2):* the §12.7 re-runs (one re-dispatch of a failed dry run and one `--failed` re-run per stage, for the classes marked "Once") are part of the approved dispatch, so the coordinator runs them without asking again. (iii) governs a **stopped** stage: a failure after that re-run, or a class with no re-run (I-4, I-5, I-7). The stop is diagnosed, and any new measurement dispatch needs a fresh operator approval. The operator accepted this interpretation in the Codex session by directing “handle these recommended steps directly” after review of PR #523. The approved retry caps and immediate-stop classes are unchanged; this confirmation does not release the S5 hold.
- (iv) The accounting-design question also returns if a diagnosis traces an invalid run to the workload itself.

This supersedes r2 §10.3's release-point reading and the §12.7 sentence that has the measurement limb engage when no valid record exists at the release point. **Still for the operator, when it arises:** whether a PART_A ceiling set by ruling, without a measurement, answers the measurement limb (recommendation item (v)). No S5 draft §2.3 owner text changes here; that is RC-2, at C3.

**(5) RC-4 slice accepted:** "K3/RC-4 — service salt and client plan view". It is dispatched after S5 acceptance and lands before S8/T06, which moves K3 out of TB-F1. The F1 admission check in the [RC-5/RC-4 coordinator entry](#coordinator-assignment--rc-5-host-checks-recorded-and-rc-4-seed-view-slice-pending-the-operator-2026-09-27) applies as written. **Coordinator confirmation:** with the slice accepted, the **RC-4/RC-5 assignment at build entry is met**. The implementation (the RC-4 change landed, K3 built) remains before F1 (CP-6). The OF attestations fall due at the gates the [RC-5 entry](#coordinator-assignment--rc-5-host-checks-recorded-and-rc-4-seed-view-slice-pending-the-operator-2026-09-27) assigns: OF-7 before F1 admission (F1 admission check, condition 4); the full OF-1..OF-7 set at production-host provisioning (CP-8) and before any production-authority release; OF-5 before any arm and at each session GO; OF-6 at TB-I3. The checklist addendum records the S8/T06 sequencing.

**(6) Stage 1c seam approved:**
- the r2 §7 seam, with S5 build requirements **SR-1..SR-9** (SR-9 as adopted, r2 §16 C2);
- proof obligations **P-1..P-7**;
- the SR-7 exception at the packet's four tolerance sites (lines 8, 35, 49 and 61).

**P-3, P-4 and P-5 are hard, non-waivable C3 preconditions.** After the RC-6 fold-in, a missing SR or a failing P at C3 is a C3 nonconformance returned to the S5 executor. #519's Stage 1c-prep is not adopted. H1 step (c) carries the approved set into the RC-6 re-anchor draft, which goes to the operator for acceptance.

**Status after this ruling.**
- CP-1a is **RULED**.
- **Next:** H1 step (b) executes the approved measurements. *[2026-09-27: execution follows the harness merge, not step (b) itself, and waits for the sequencing gate in [r2 "Current authority"](../../notes/2026-09-27-s5-part-a-measurement-proposal-r2.md) (§12.9).]* RC-3a evidence (a valid Stage 1b record, the rule applied as a provisional PART_A TEST_ONLY ceiling, the §10 arithmetic) and an updated build-entry table then go to **CP-1b**.
- RC-1 is met. RC-4/RC-5 are met for build entry.
- RC-3a, the §3.4(d) text and the RC-6 re-anchor remain open.

**Not granted:**
- the hold release (CP-1b);
- S5 build, freeze, dispatch or execution;
- any measurement beyond (2), and any other workflow, dispatch, re-run or download;
- a ceiling without a valid record;
- any value for other phases or for production;
- closing RC-3b;
- any S5 packet or owner-text edit before the operator accepts the RC-6 text;
- statistical dispatch;
- production, activation or live authority.

The hold stays **HELD**.

### Operator ruling — H1(c) draft: open questions and drafter's additions, 2026-09-27

**Source.** In session on 2026-09-27, the operator answered the open questions OQ-1..OQ-6 and the drafter's additions D-1..D-10 of the H1(c) draft, choosing the recommended option each time. The draft is the [S5 owner-text and RC-6 draft](https://github.com/Joshua-Asante/first-passage/pull/525), `docs/notes/2026-09-27-s5-owner-text-and-rc6-draft.md` at `f95a39be`, returned under the [H1 dispatch record](../../briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md#h1-steps-b-and-c-dispatch-record-frozen-2026-09-27). The answers were given by structured answer; the recommendation texts relayed in session govern.

| Item | Ruling |
|---|---|
| **OQ-1** (CP-1a (4)(v)) | **Kept open until it arises.** It matters only if no valid Stage 1b record exists. The three-way D2 split already keeps the hold whenever a run is missing. |
| **OQ-2** (the §3.4(d) forward reference) | **The D-2 bridging note.** The two §3.4(d) insertions are applied at build entry, each with a dated note. Until C3, the spec §2.6 rule's source is the operator's D3 direction (this ledger, 2026-09-26) and S5 draft §3.3. The notes are removed when the §2.6 text lands at C3. |
| **OQ-3** (SR-7's reach) | **One clarifying line** in the packet's new §1a: the five RC-2 owner sentences (slices plan `:17`, `:238`; full-E1 spec `:121`, `:123`, `:200` at `875ecf29`) govern route and contract values. The TEST_ONLY Stage 1c override is never one of these (P-3, P-4), and a forced result can never pass (P-5). The five owner sentences stay unchanged. The CP-1a exception does not widen beyond the packet's four sites. |
| **OQ-4** (the CI-configuration part of the S5 file scope) | **Approved, on the S4 precedent.** Within the S5 build, the executor may add an S5 value to the `mode` input of `.github/workflows/qualification-s2-supervision.yml` and extend the evidence reader so that SR-8's fields have a reader. The change lands through the operator's merge. Any dispatch of it needs its own grant at C3. |
| **OQ-5** (umbrella O-10) | **Not used.** The ledger's RC-4/RC-5 entries and the checklist already carry the assignment and the sequencing. |
| **OQ-6** (S5 draft §6) | **Q2 confirmed:** R4's "original deadline" is the campaign's, as the draft's §3.6 paragraph assumes. **Q1, Q7 and Q9 stay open to C3.** Q1 and Q7 are decided with the statistical owner. |
| **D-1..D-10** | **All ten accepted:** D-1 qualified tags; D-2 bridging note; D-3 boundary §3.1 placed at the end of §3; D-4 RC-5 pointer; D-5 S5 file scope, whose workflow part is approved by OQ-4; D-6 crash-case rewording; D-7 receipt field names; D-8 admission-crash consequence stated in full; D-9 sequencing clause in spec §2.6; D-10 rule scope and the `/v7` N2 value in contract decision 3. |

**Effect.** The H1(c) draft is revised to carry these answers, including the OQ-3 clarifying line, and is returned as revised. **Acceptance of the revised draft's full text remains the operator's.** It is not implied by these answers. No owner document is amended until that acceptance, and then only by a separate application commit: build-entry texts before CP-1b, RC-2 texts at C3.

**Not granted:** S5 release, build, freeze, dispatch or execution; any owner-text application; any workflow dispatch; closing RC-2, RC-3 or RC-6; anything outside the draft's scope. The hold stays **HELD**.

### Operator acceptance — H1(c) full text accepted; build-entry sections to be applied, 2026-09-27

**Source.** In session on 2026-09-27, the operator wrote: "I accept #525's full text at 011ce9e4; apply the build-entry sections". The accepted text is `docs/notes/2026-09-27-s5-owner-text-and-rc6-draft.md` at `011ce9e47859e702765b4e64e6e7d47cc2b759a6` ([#525](https://github.com/Joshua-Asante/first-passage/pull/525)). It carries the rulings of the entry above and the operator's three review corrections made before acceptance.

**Effect.**
- **Build-entry sections, applied now** by one application commit, against the **pinned application head** `origin/main` `875ecf29`, which is the draft's anchor head (no drift):
  - the draft's §1: the §3.4(d) text in slices-plan contract decision 6 and in S5 Behavior, with D-1 and the D-2 bridging notes;
  - the draft's §2: the RC-6 re-anchor of the S5 packet `docs/briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md`, with the §0.1 findings and pitfalls, §0.5 N2, the §1a seam (SR-1..SR-9, P-1..P-7, the OQ-3 line), the SR-7 exception at the four tolerance sites, the D-5 run-tooling scope, and the explicit C3 order.
- **CP-1b** names the resulting reviewed revision. If that revision differs from the application head in any file an anchor covers, the affected anchors are re-checked before CP-1b.
- **RC-2 sections (the draft's §3)** are **not applied now**. They are applied at C3 against their own pinned head.
- **Still open:** OQ-1, and Q1, Q7 and Q9 at C3.

**Not granted:** the hold release (CP-1b); S5 build, freeze, dispatch or execution; any RC-2 application before C3; any workflow dispatch; any measurement outside the CP-1a dispatch. RC-6 is met only when the application is merged and reviewed, and CP-1b records it. The hold stays **HELD**.

### Coordinator transfer and execution dispatch — H1 step (b) measurement, 2026-09-28

**Source.** Operator direction in session, 2026-09-28 (UTC). The operator relayed a draft "Post-H1 measurement execution — next-session handoff" and directed "Update to main and continue". Then, by structured answer:
- to "Who holds the coordinator role for executing H1 step (b)?": "This session";
- to "Must that ownership and dispatch record be merged to main before the first dispatch?": "Merge first";
- to "How should merges to main be handled while a Stage 1b run is in flight?": "Hold merges".

The relayed draft is not a committed record. This entry records what the operator adopted from it.

**Transfer (scoped).** Under STATE's handoff obligation, the coordinator role for H1 step (b) execution passes to the Claude Code session "Post-H1 measurement execution handoff". That session runs on the operator's Windows host, in worktree `.claude/worktrees/bracket-timing-convention-build-43a332`, on branch `claude/post-h1-measurement-execution-96350a`.
- **Scope:** the bounded r2 §12 measurement approved by CP-1a decision (2), the r2 §13 application and the CP-1b packet.
- **Unchanged:** other coordinator work stays where it is. The operator decides CP-1b and keeps merges and operational GOs.

**Starting state.** `origin/main` is at `6da1b2b2`.
- Merged: #523 (`c918cad5`), #525 (`ed3e476f`), #526 (`0dcceb08`, head `77b916f7`) and #527 (`6380dcb4`).
- The dispatch-only workflow is registered on the default branch (workflow ID 368645616) and has no runs.
- The harness, workflow, regression module and both fixtures are byte-identical from `6010cb50` to `6da1b2b2`.

**Preconditions before any measurement** (the Stage 0 read, Stage 1a or any dispatch):
1. The r2 "Current authority" gate: #534's H1-row record of the #842/#843 post-merge audits is on `main`.
2. This entry is on `main`.

**Findings recorded before execution.**
- **Line endings.** This host's system gitconfig sets `core.autocrlf=true`, so checkouts have CRLF bytes. The harness pins the LF SHA-256 of `composition_fixture.py` and `runtime_fixture.py` (`measure_part_a_max.py.txt:79-84`) and hashes working-tree bytes. So:
  - a Stage 1a bundle from a CRLF checkout can only exit 4 (H-SHAPE);
  - a combine from a CRLF checkout is refused.

  Stage 1a and the combine therefore run from a clean detached LF checkout, made with `git -c core.autocrlf=false worktree add --detach <path> <sha>`. No code changes.
- **Retention follow-up (#523): resolved.**
  - Records `20260927T180621Z-71bad46c8b99` and `20260927T180630Z-2534fb8215cf` are archived byte for byte in first-passage-archive#837 (pins `docs/evidence/PRIVATE_EVIDENCE.sha256:109-111`).
  - `scripts/evidence_archive.py audit --verify` against the archive's `main` at `b560ac2a` reports them ARCHIVED (166 pins: 78 ARCHIVED, 0 UNPUSHED, 88 MISSING, 0 CORRUPT).
  - The originals were written in a cloud session and are not on this host. The archived copies are the durable copies.
- **Stage 0 inputs.** The preserved set's `SHA256SUMS` hashes to `e2c14228…189a7`, as the 2026-09-26 entry records. The r2 §16.4 coverage check runs after the preconditions.
- **Cleanup failure.** README `:196` counts a failed owned cleanup against the `--failed` re-run. r2 §12.7 (`:689`) stops the stage instead, and r2 governs.
- **Runtime.** The workflow refuses `worker_image`. Stage 1b runs on `host_venv`, on the recorded static image-first finding (H1 row correction), and PA-5 at C3 validates the mismatch. The probe and dry run establish `host_venv` readiness only.
- **CP-1b inputs (not measurement blockers).**
  - #527's packet carries post-acceptance corrections 1, 2, 4–7 and 9–11, which await the operator's acceptance (owner-text draft `:905`).
  - `ops/c1_rail/qualification/replay.py` changed after the application head `875ecf29` (#522), so its anchors are re-checked before CP-1b.

**Execution dispatch.** This entry adds no authority beyond CP-1a decision (2), its confirmed re-run interpretation, and r2 §12.7 and §12.9.
1. **Stage 0.**
   - Run the r2 §16.4 coverage check in the primary checkout, read-only.
   - If coverage holds: the §12.1 local read and public-clone review. *[2026-09-28: run r2 §16.4's check-and-read block instead ([#536](https://github.com/Joshua-Asante/first-passage/pull/536)). The §12.1 extraction lines double-count systemd CPU lines and drop each line's run; r2 marks them superseded (helper review of #523, C1, C5 and C12).]*
   - Otherwise: record `UNAVAILABLE`. No download.
2. **Stage 1a.** Run the README Stage 1a commands through the LF checkout's `fp.ps1`.
3. **Stage 1b dry run.** *[2026-09-28: do not dispatch with the commands in steps 3–5. They never bind a run id, download or retain the evidence by run, job and attempt, or read the re-run decision from the records (helper review of #523, C2, C3, C6, C7 and C10). Stage 1b runs from r2 §12.3's tested dispatch block in [#539](https://github.com/Joshua-Asante/first-passage/pull/539), once it merges. That block stays within this entry's authority and the §12.7 caps.]* *[Coordinator record 2026-09-28: Stage 1b had already run under steps 3–4 as merged in #535, at 01:06–01:12 UTC, before this marker merged (#536, 03:18 UTC). The dry run was 36364714432 and the measure run 36364854404, both at head `7675c088`. Each run id was bound by listing this workflow's runs right after its dispatch: exactly one new run appeared each time, with its `headSha` confirmed, and the workflow has no other runs. Each run was watched to completion and its artifacts downloaded whole into a per-run directory, named by job and attempt. They are retained publicly under `stage1b/` and privately in first-passage-archive#844. The re-run decision was read from each job's record and summarize log: all exit 0, so no re-run was used. The marker governs any further Stage 1b dispatch. It does not invalidate the executed runs; see the [CP-1b packet entry](#coordinator-cp-1b-packet--build-entry-status-2026-09-28).]*
   - Command: `gh workflow run qualification-s5-part-a-measurement.yml -R Joshua-Asante/first-passage --ref main -f stage=1b -f mode=dry-run -f runtime=host_venv -f note_dir=docs/notes/2026-09-27-s5-part-a-measurement`.
   - Then `gh run watch`, and `gh run download` into scratch, pass or fail.
   - At most one re-dispatch, and only for I-1 or I-6.
4. **Stage 1b measure,** after a clean dry run.
   - Command: the same, with `-f mode=measure`.
   - At most one `gh run rerun --failed`, and only when every failed job exits 3 and is re-run eligible.
5. **Combine** from the LF checkout at the dispatched SHA.
6. **Application.** If the combined record is rule-applicable with `stop_class = none`, record the r2 §13 application entry here.

Every r2 §12.7 and §12.9 stop returns at once. A further dispatch after a stopped stage needs a fresh operator approval. Before each dispatch the coordinator tells the operator the window has started. The operator holds merges to `main` until the run ends (r2 §12 common limit).

**Output paths.**
- **Public,** under `docs/notes/2026-09-27-s5-part-a-measurement/`:
  - `windows-<utc>.json` and its `.record.json`;
  - `stage0/{SHA256SUMS,lines.txt,memory_peak.txt}`, after the review;
  - `stage1b/<run_id>-<job>-attempt<n>/`, with the r2 §12.3 file list, failed attempts included;
  - `stage1b/<run_id>-combined.json`;
  - a dated measurement section in the README (r2 `:627`).

  Also public:
  - pins in `docs/evidence/PRIVATE_EVIDENCE.sha256`;
  - this ledger, the H1 row and the CP-1b packet.
- **Private:** the complete downloaded artifacts (including `journal.log`) and the launcher records. They are archived in first-passage-archive by content address, through a `claude/*` branch PR that the operator merges.

**Not granted:**
- any other workflow, dispatch, re-run or download;
- Stage 1c or Stage 2;
- any profile, ceiling or release-literal edit;
- the hold release;
- S5 build, freeze, dispatch or execution;
- production, activation or live authority.

S5 stays **HELD**.

### Operator acceptance — H1(c) post-acceptance corrections 1, 2, 4–7 and 9–11, 2026-09-28

**Source.** In session on 2026-09-28 (UTC), asked "Is it your decision to accept post-acceptance corrections 1, 2, 4–7 and 9–11 … as build-entry text, with 3 and 8 staying at C3?", the operator answered by structured answer: "Yes, accept them".

**Scope.**
- The accepted corrections are the ones in the register of `docs/notes/2026-09-27-s5-owner-text-and-rc6-draft.md` (`:907-919`), at blob `bb082bca` (last changed in `e59333b`).
- They are applied in the S5 packet `docs/briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md` at blob `ee7329c1` (last mirror `7b6df3f`), which carries 14 "Post-acceptance" markers.
- Correction 5 (pre-decision prefix custody) adds an executor obligation: the initial-prefix artifact is written and fsynced before the expansion decision. Correction 2 drops a redundant seam-gate predicate, correction 9 makes CP-1b the only freeze trigger, and correction 10 states PA-5's prescribed-arm denominator. Corrections 1, 4, 6, 7 and 11 bring the S5 scope into validation, test selection and operator commands.

**Effect.**
- The build-entry text applied by #527 is now accepted text in full.
- Corrections 3 and 8 are C3 text and stay unaccepted until C3.

**Not granted:** the hold release, S5 build, freeze or dispatch, and any RC-2 application. S5 stays **HELD**.

### Coordinator application: PART_A TEST_ONLY diagnostic ceiling under the approved measurement-and-margin rule (2026-09-28)

**Rule and scope.**
- The rule is the r2 §9 measurement-and-margin rule. Its numeric defaults were conditionally approved on 2026-09-26 and confirmed by CP-1a decision (1): m_c 2.0, m_w 3.0, L 30 s, m_m 1.5, the floors 120 s / 300 s, and rounding up to whole 10 s. CP-1a (1) keeps the 1.5 × P̂ pilot-budget term provisionally; it is not among the 2026-09-26 defaults. O = 20 s is the profile constant `profile.py:212`.
- It is applied under the r2 §13 procedure.
- Scope: the `/v7` TEST_ONLY diagnostic profile, PART_A only. No production value is set or implied.

**§13 preconditions.**
- The CP-1a ruling is recorded above.
- The record is the combined Stage 1b record `docs/notes/2026-09-27-s5-part-a-measurement/stage1b/36364854404-combined.json` (SHA-256 `e1efa8fd127ce24f44f0cfcb8c9d0bf15d647af4def007fc3971f791e8613d73`). It shows:
  - `scope = combined`, `stage = 1b`, `mode = measure`;
  - `validity_ok = true`, `rule_applicable = true`;
  - `memory_feasibility = VERIFIED` and `stop_class = none`.
- The `/v7` N2 value is 360 s / 900 s, from CP-1a decision (3).

**Inputs.** From `summary.estimates` (forced arm; maxima over the 10 timed repeats of both jobs, cold included):
- Ĉ = 11.038634 s: job a, forced repeat 1 (cold). It is `max(C_w, CPUUsageNSec − setup) = max(10.518016, 15.141 − 4.103)`.
- Ŵ = 11.390639 s.
- P̂ = 8.426527 s.
- M̂ = 168,366,080 B: job b, forced repeat 1 (cold).

Ĉ and M̂ are shown exactly. Ŵ (recorded 11.390638705000004) and P̂ (recorded 8.426527197999889) are shown rounded to six places, and the computation uses them at full recorded precision. The only rounding applied is the final upward rounding of X and Y to whole 10 s. The per-job records are:
- job a: `…/stage1b/36364854404-a-attempt1/record.json` (SHA-256 `65bda0488acd9919116d29f2bc0c3af8cebf4e93b63d01fca0848130cedbbcc5`);
- job b: `…/stage1b/36364854404-b-attempt1/record.json` (SHA-256 `c67368207e145a33602749a40ef38df8abfed85bb4721b5ea8a7c4cfb4ada3d2`).

**Computation** (the arithmetic is reproduced by the harness screens: `sigma_screen` 120 / 300 and `pa3a_screen` 252,549,120):
- **PA-1:**
  - B = max(2.0 × 11.038634, 1.5 × 8.426527) = max(22.077268, 12.639791) = 22.077268.
  - X_raw = max(120, 22.077268 + 20) = 120, so **X = 120 s**.
  - It is **provisional: D̂ uncovered** until Stage 1c.
- **PA-2:**
  - Y_raw = max(300, 3.0 × (11.390639 + 30)) = max(300, 124.171916) = 300, so **Y = 300 s**.
  - It is **provisional** too.
  - m_w ≥ m_c ÷ (m_c − 1) holds (3 ≥ 2).
- **PA-2b:** 1.5 × P̂ = 12.639791 ≤ B, and X − 20 = 100 ≥ B.
  - The 1.5 × P̂ term stays provisional until the C3 check on SR-8's `probe_seconds` and `predicted_seconds` (CP-1a (1)).
- **PA-3a** (payload scope):
  - 1.5 × M̂ = 252,549,120 ≤ 256,000,000, so memory is **VERIFIED**. The margin is 3,450,880 B (1.35%).
  - The same test over every timed repeat of both arms (r2 §8.3's wording) uses M̂ = 169,336,832 (job a, prescribed cold) and gives 254,005,248, still within the bound (margin 0.78%).
  - Both exceed the unextended binding of 230,400,000. So the 256,000,000 reference needs the P4 tuple extended to `/v7`, which is precondition 1 below.
  - The memory maxima come from the cold repeats (about 165–169 MB against about 100 MB warm).
- **PA-3b:** the composition `m_m × (P₂ + max(0, M̂ − M̂ₚ))` is accepted as a provisional C3 check. Its additive assumption is **UNVERIFIED** (CP-1a (1)).

**Shared ceilings suffice.** X = 120 s and Y = 300 s equal the shared PART_A diagnostic values (`profile.py:209`). So r2 §13 step 5 does not trigger: no `/v7`-gated PART_A constant and no profile edit follow from this application.

**Feasibility (r2 §10.2, arithmetic on the proposed `/v7` values):**

| Row | CPU | Wall | Result |
|---|---|---|---|
| Σ phases, the code check (`campaign_store.py:2776-2783`) | 1,560 + 120 = 1,680 ≤ 10,000 | 3,900 + 300 = 4,200 ≤ 10,000 | feasible |
| + one signing retry of a 120 s / 300 s phase | 1,800 ≤ 10,000 | 4,500 ≤ 10,000 | feasible |
| + D3's two future compute re-executions (not S5) | 1,680 + 3 × 120 = 2,040 ≤ 10,000 | 4,200 + 3 × 300 = 5,100 ≤ 10,000 | feasible |
| Memory: max phase `memory_bytes` against the binding | 256,000,000 ≤ 256,000,000 with the P4 tuple extended | — | feasible only with the extension |

- The two gaps r2 §10.2 names stand: Σ counts one reservation per phase, and no code checks the wall slack between works.
- The **D2 ACCOUNTING-DESIGN FALSIFIER** is not engaged: Σ is feasible from a valid record.
- There is no PA-3 failure.

**`/v7` preconditions** (for the S5 build, not applied here):
1. add `/v7` to the P4 tuple at `fixture_producer.py:154-155`;
2. add `/v7` at `profile.py:219-226`;
3. add `/v7` at `profile.py:243-252`;
4. extend `profile.py:239` to `/v7` with 360 s / 900 s.

**Recorded alongside.**
- **Host variance.** The between-job forced median CPU ratio is 1.534. Job a ran on an AMD EPYC 7763 and job b on an AMD EPYC 9V74. r2 §6.2 records a ratio above 1.30 as host variance, not a validity failure. The PA-4 warm spread within each job and arm is about 1.01–1.02.
- **Runtime.** `host_venv`, CPython 3.12.3 on Ubuntu 24.04, kernel 6.17.0-1022-azure, systemd 255, 4 vCPU, swap off. PA-5 at C3 validates the host-to-worker mismatch (CP-1a (2)(d)).
- **C3 re-measurement trigger 5 thresholds:** 0.8 × B = 17.66 s and 0.8 × Y = 240 s.

**Not granted:** a production value; any value for another phase; closing RC-3b; the hold release; S5 build, freeze or dispatch. S5 stays **HELD**.

### Coordinator CP-1b packet — build-entry status, 2026-09-28

**Execution record (H1 step (b), under the dispatch entry above).** `main` was `7675c088` at Stage 1a, at both dispatches and after the combine; no commit landed on `main` during either Linux window.

| Stage | Outcome | Evidence |
|---|---|---|
| Stage 0 (optional calibration) | r2 §16.4 coverage **holds**: `SHA256SUMS` = `e2c14228…189a7`, all 222 files verify, and both log files are present in each run directory. Extraction and public-clone review are done, with the review rule recorded in the README. The read used the §16.4 block as it stood at `7675c088`, which greps both `journal.log` and `systemd-units.log`. So `lines.txt` double-counts the systemd CPU lines, which appear in both files, and carries no run or file labels. #536's corrected block (`journal.log` only, labelled lines, pin and entry checks) post-dates the read. This is calibration only; it sets nothing. *Deviation from the dispatch entry's output list:* `stage0/SHA256SUMS` is not committed. Its hash is cited instead, because a tracked `*SHA256SUMS` would pin 222 private files, two of which (110 MB each) cannot be archived | `docs/notes/2026-09-27-s5-part-a-measurement/stage0/{lines.txt,memory_peak.txt}`. It sets no ceiling and no N2 value |
| Stage 1a (Windows, LF checkout at `7675c088`, ops env CPython 3.13.2) | **Valid** (exit 0). The first invocation was refused by argparse before any repeat ran: PowerShell split the unquoted `--arms` list. The README command is corrected and the refusal log is archived. Memory is UNVERIFIED by design; the record is never rule-applicable | `windows-20260928T010154Z.json` (`1eaf8fb9…`) and its `.record.json` (`9ecff272…`) |
| Stage 1b accounting probe and dry run | Run **36364714432**, attempt 1: **valid** (exit 0). The probe is OK: in-unit peak 76.0 MB for a 64 MiB child, cgroup path matches, swap off. Memory is complete, CPU captured and cleanup exit 0. The image-first decision rests on the recorded static finding (`host_venv`) | `stage1b/36364714432-a-attempt1/` |
| Stage 1b measure | Run **36364854404**, attempt 1, jobs a and b: both **valid**, memory VERIFIED, cleanup exit 0. No re-run was used: 0 of 1 dry-run re-dispatches and 0 of 1 `--failed` re-runs | `stage1b/36364854404-{a,b}-attempt1/`; combined record `e1efa8fd127ce24f44f0cfcb8c9d0bf15d647af4def007fc3971f791e8613d73` |

The complete downloaded artifacts, including the journals, are private. So are the Stage 1a logs and the raw Stage 0 extracts. They are in the package `h1b-stage1b-measurement-evidence-2026-09-28.tar.gz` (SHA-256 `9b00b8c163f7514015256283a61998b60b1afa0fa5bd3dfc5c804ef573deee29`, 86 files with a `MANIFEST.tsv`), which is pinned in `docs/evidence/PRIVATE_EVIDENCE.sha256` and pushed to first-passage-archive in [first-passage-archive#844](https://github.com/Joshua-Asante/first-passage-archive/pull/844) (commit `7ae9a62`). It counts as ARCHIVED once the operator merges that PR, and the post-merge `audit --verify` is recorded then.

**Build-entry table** (this updates the [2026-09-27 direction entry](#operator-direction--s5-build-entry-separated-from-checkpoint-c3-acceptance-2026-09-27)'s status column):

| Condition | Status 2026-09-28 | Evidence |
|---|---|---|
| RC-1 | **Met** | #517 merged at `5ad04cf`; [D1–D3 ruling](#operator-ruling--s5-directions-adopted-hold-kept-2026-09-26) |
| §3.4(d) text | **Applied** | #527 application commit `afa26a66` (merged at `6380dcb4`): contract decision 6 and the S5 Behavior text in this plan, each with its D-2 bridging note (removed at C3) |
| RC-4/RC-5 assignment | **Met** | [RC-5 assignment](#coordinator-assignment--rc-5-host-checks-recorded-and-rc-4-seed-view-slice-pending-the-operator-2026-09-27); RC-4 slice accepted at [CP-1a (5)](#operator-ruling--cp-1a-decisions-16-adopted-as-recommended-hold-kept-2026-09-27). The implementation is due before F1; the attestations fall at their assigned gates |
| RC-6 | **Met, subject to CP-1b naming the revision** (the evidence and the re-check follow the table) | The packet was re-anchored at `875ecf29` by #527 |
| RC-3a | **Met** | The rule (CP-1a (1)); a valid record from the approved forced-expansion measurement of the existing engine (run 36364854404); the provisional application and the §10 arithmetic ([entry above](#coordinator-application-part_a-test_only-diagnostic-ceiling-under-the-approved-measurement-and-margin-rule-2026-09-28)) |
| RC-2 | At C3 (open) | The draft's §3 plus corrections 3 and 8 |
| RC-3b | At C3 (open) | Stage 1c, the executed `bind_budget` on the built `/v7`, and Stage 2/PA-5 |

**RC-6 evidence.**
- **Operator acceptance:** the full text at `011ce9e4`, and corrections 1, 2, 4–7 and 9–11 ([entry above](#operator-acceptance--h1c-post-acceptance-corrections-1-2-47-and-911-2026-09-28)).
- **Coordinator review:** at `7675c088`, all 99 build-entry PROPOSED lines of the note are present verbatim in the packet and this plan. At `afa26a66` it was 91 of 91 against the note at `011ce9e4`.
- **Anchor re-check against the candidate.** Between the application head `875ecf29` and `7675c088`, the only anchored code that changed is `ops/c1_rail/qualification/replay.py`, from #522. That change is the lifecycle-L1 exemption from the one-bar cancel for `orb_mnq_v7` base entries.
  - The packet cites `replay.py` only as a file-level Rule-0 read (packet line 12), with no line anchor.
  - `part_a.py` imports only `ReplayDeadlineFailure` from it, and that is unchanged.
  - Stage 1b measured `7675c088`, which includes the change.
  - The packet's statement that `ops/c1_rail/qualification/` is unchanged refers to `228447c` against `875ecf29`, and it remains true of those two commits.
  - The packet PR that carries this entry changes no anchored line or section. In this plan it changes only line 851 in place and appends entries at the end.

**CP-1b candidate revision:** `main` at the merge of the PR that carries this entry. It is documentation-only over `7675c088`.

**Coordinator recommendation, for the operator's decision:** release the S5 hold for the **TEST_ONLY build** at that revision.
- C3 obligations stay: Stage 1c through the built adapter with the SR/P set; the executed `bind_budget` Σ check on the built `/v7`; Stage 2/PA-5 with the named worker-side residual; PA-3b and the pilot-budget term validation; the RC-2 owner-text set with corrections 3 and 8; OQ-1, Q1, Q7 and Q9.
- The four `/v7` preconditions land with the S5 build.

**Not granted:** the hold release (the operator's, at CP-1b); S5 build, freeze or dispatch; Stage 1c or Stage 2; production, activation or live authority. S5 stays **HELD**.

### Operator ruling and execution — S4 run logs second copy (M-41), 2026-09-28

**Source.** The operator relayed a suggested ruling on #538 (the [retention proposal](../../notes/2026-09-27-s4-run-logs-archive-retention-proposal.md)) and, asked by structured question whether he adopted it, answered "Yes, adopt it". This entry records it as his decision.

**Ruling.** Option A is approved, with GO for the bounded preservation task:
- compress the two `journal.sqlite` files;
- archive and push the specified artifacts to first-passage-archive;
- open the registry/ledger PR through normal repository controls.

**Completion requires:**
1. verify the manifest and all 222 source files before packing, and leave the originals unchanged;
2. account for all 224 archive inputs; deduplicated blobs are acceptable, skipped or missing inputs are not;
3. fetch and verify against the archive's `origin/main` after the archive change lands, confirming every new registry entry ARCHIVED; an exit-zero audit alone is insufficient;
4. restore the complete 222-file set into a separate directory from archived blobs, decompress the two databases, and pass the original `SHA256SUMS`;
5. record the archive commit and verification evidence here; public changes are limited to approved metadata.

**Excluded:** deletion of the originals, changes to `evidence_archive.py`, and future S5 retention work.

**Execution, 2026-09-28** (primary checkout, ops interpreter CPython 3.13.2):
1. `SHA256SUMS` hashes to `e2c14228…189a7`, and `sha256sum -c` passes for all 222 files. A path, size and mtime snapshot of the 223 files, taken before packing and again after archiving, is identical.
2. Packed into the sibling directory `local_artifacts/s4-linux-run-logs-2026-09-25.packed/`, never inside the originals:
   - run 36180568493: 110,350,336 B → `6b83b7ea…8b15`, 1,723,740 B;
   - run 36181780676: 110,469,120 B → `83b07817…851a`, 1,728,948 B;
   - `PACKED_SHA256SUMS.tsv` is `cb978a83…5068`.

   Each `.xz` decompresses to its pinned original.
3. `evidence_archive.py put` over 224 inputs returned 0 with empty stderr: 114 archived and 110 already archived. The inputs are 120 distinct digests: 114 new blobs, and 6 already on the archive's `main`. No input was skipped. Every staged blob id equals `git hash-object --no-filters`. Archive commit `88b24580` is on branch `claude/evidence-s4-run-logs-2026-09-25`, first-passage-archive#845.
4. Registry: 120 pins were added to `docs/evidence/PRIVATE_EVIDENCE.sha256`, one per distinct digest, each under its first path in path order. *[Corrected 2026-09-28: the first registry commit added 224 lines, one per input, which duplicated 104 digests and failed `test_registry_digests_are_well_formed_and_unique`. The archived `SHA256SUMS` maps every path.]* The raw `journal.sqlite` digests are recorded in the comment, not pinned.
5. Pre-merge checks against the pushed archive branch:
   - `audit --verify` (with the 224-line registry, since corrected) reports 395 pins: 307 ARCHIVED, 0 UNPUSHED, 88 MISSING (pre-existing), 0 CORRUPT. None of the 120 new digests is listed as non-ARCHIVED.
   - A restore from archived blobs alone (`git cat-file blob`, both databases decompressed) into a scratch directory passes `sha256sum -c` for all 222 files.

**Post-merge verification, 2026-09-28.** The operator directed the merge of first-passage-archive#845. It merged as `2ec6f6c9`, and `88b24580` is an ancestor of the archive's `main`. After `git fetch`, the clone's `main` tracks `origin/main` at `2ec6f6c9`.
- **Check 3.** With the corrected 120-pin registry, `audit --verify` reports 291 pins: 203 ARCHIVED, 0 UNPUSHED, 88 MISSING (pre-existing), 0 CORRUPT. The 224-line registry had reported 395 pins, 307 of them ARCHIVED. None of the 120 new digests is listed as non-ARCHIVED. All 120 are present under `evidence/sha256/` on `origin/main`, and each committed blob (`git cat-file blob`) hashes to its address.
- **Check 4.** A restore from `origin/main` blobs alone rebuilt 222 files into a scratch directory, 2 of them by decompression. The restored `SHA256SUMS` hashes to `e2c14228…189a7`, and `sha256sum -c` passes for all 222 files. The scratch copy was then deleted.
- **Originals.** The path, size and mtime snapshot still matches the pre-packing snapshot.

All five completion checks are met. The originals and the `.packed/` sibling stay in the primary checkout; nothing was deleted.

### Operator ruling — CP-1b: S5 hold released for the TEST_ONLY build, 2026-09-28

**Source.** In session on 2026-09-28, the operator wrote: "I approve CP-1b for the S5 TEST_ONLY build, effective once the final cited verification record is retained and pinned, archive #844 is merged and its post-merge audit is recorded, and #537 is merged with passing checks. Record the actual #537 merge SHA as the accepted revision before dispatching the build. Include all four documented /v7 preconditions. Accept the memory result as provisional, with its narrow margin explicitly carried forward. RC-2, RC-3b and all listed C3 obligations remain open. This approval grants no production, activation or live authority."

The operator then set the order: merge #844, merge #537 once CI passed, run the audit against this entry's pin registry, and merge this entry after review and checks.

**Accepted revision (the release head).** `05f3788d9e4895308d6734e650a42875c59f669c` is the merge of [#537](https://github.com/Joshua-Asante/first-passage/pull/537) at 2026-09-28T16:27:11Z. Its PR head `6f1da0b3` is the operator's merge of `main` (#539, #540 and a `tests.yml` fetch-depth change) into the packet head `1dae754`.
- The S5 packet's "release head named in the CP-1b hold-release entry" is this SHA.
- Anchor re-check against it: between `7675c088` (the measured and re-checked revision) and `05f3788`, no anchored code changed, and neither did the S5 packet or the slices-plan anchor lines (`:17`, `:91`, `:233`, `:238`). The only other changes the packet could reach are #536's dated markers. In the S5 decision draft they are in place, at lines 374, 402 and 404. In the owner-text note they add two lines near the top. The packet cites neither document by line, and the acceptance entry above pins the note's blob.

**Conditions, each met before this entry.**
1. **The final cited verification record is retained and pinned.** #537's cited `check` records are:
   - `20260928T013657Z-0f0b5ae0df6b` (head `0a84674`);
   - `20260928T015253Z-8d29efff45e1` (head `fadfc29`);
   - `20260928T144557Z-6db9391ec782` (head `1dae754`, the final cited record; SHA-256 `26b21a0431da19d791a795357a5d8d042d57890768c34665b8b46d93993f3a82`). It shows status completed, exit 0, `source_stable: true` and complete capture.

   They are retained in first-passage-archive#844 and pinned in `docs/evidence/PRIVATE_EVIDENCE.sha256` by this entry's commit. The merged head's own checks are GitHub's (item 3).
2. **Archive #844 is merged, and its post-merge audit is recorded.** [first-passage-archive#844](https://github.com/Joshua-Asante/first-passage-archive/pull/844) merged at `e3672489`. `scripts/evidence_archive.py audit --verify` ran from this entry's tree, whose registry includes the three pins above, against the archive's `main` at `e3672489`. It reports **177 pins: 89 ARCHIVED, 0 UNPUSHED, 88 MISSING, 0 CORRUPT**. Every pin the H1 step (b) execution added is ARCHIVED and re-hashes correctly: the package `9b00b8c1…ee29` and the five check records (`90ce9b52…`, `c7246306…`, `d9afecf4…`, `38c4db66…`, `26b21a04…`). The 88 MISSING predate this work.
3. **#537 is merged with passing checks.** Every check on head `6f1da0b3` passed: `skills (3.12)`, `build (3.11)`, `pytest (3.11)`, both `Qualification execution boundary` jobs, CodeRabbit and semgrep. In addition, `.\fp.ps1 check` on `05f3788` itself (Windows ops env, CPython 3.13.2) gives status completed, exit 0, `source_stable: true` and complete capture (record `20260928T170538Z-6bf1970cc12d`, SHA-256 `c6baea9f2f0f8e411afc557cfb94a0f83de5afd7ceb90b22ec2e2b5598464625`, cited, not pinned).

**Effect: the S5 hold is RELEASED for the TEST_ONLY build only, effective when this entry is on `main`.**
- **Build preconditions.** All four `/v7` preconditions land with the S5 build:
  1. add `/v7` to the P4 tuple at `tests/integration/qualification_boundary/fixture_producer.py:154-155`;
  2. add `/v7` at `ops/c1_rail/qualification/execution/profile.py:219-226`;
  3. add `/v7` at `profile.py:243-252`;
  4. extend `profile.py:239` to `/v7` with 360 s CPU / 900 s wall (CP-1a (3)).

  The PART_A diagnostic ceilings stay at the shared 120 s / 300 s. The application entry above triggers no PART_A constant.
- **Memory: accepted as provisional, with the narrow margin carried forward.**
  - PA-3a gives 1.5 × M̂ = 252,549,120 ≤ 256,000,000, a margin of 3,450,880 B (1.35%).
  - Over every timed repeat of both arms it is 254,005,248, a margin of 0.78%.
  - Both hold only against the P4-extended binding of 256,000,000. The unextended binding of 230,400,000 would fail, which is why precondition 1 matters.
  - The margin is carried into C3: Stage 1c's M̂₁c and Stage 2's PA-3b are read against it. A figure that erodes it goes to an operator ruling (r2 §9 PA-3).
- **Still open (C3 and later).**
  - RC-2: the owner-text set, with corrections 3 and 8.
  - RC-3b:
    - Stage 1c through the built adapter, with SR-1..SR-9, P-1..P-7 and P-3/P-4/P-5 hard;
    - the coordinator's recorded read of the `--stage 1c` harness diff;
    - the executed `bind_budget` Σ check on the built `/v7`;
    - Stage 2/PA-5 with the named worker-side residual;
    - PA-3b, with its additive assumption UNVERIFIED;
    - the pilot-budget term's validation through SR-8.
  - OQ-1, Q1, Q7 and Q9.
  - The RC-4 implementation and OF attestations at their assigned gates.
- **Next.** The next coordinator issues the bounded S5 build handoff from this release head. This entry dispatches nothing.

**Not granted:**
- any production value, budget or cap;
- production qualification, activation or live authority;
- any arm, deployment or trade;
- S5 acceptance or a C3 decision;
- Stage 1c or Stage 2 execution without its C3 preconditions;
- any change to a locked or frozen control.

### Coordinator — S5 TEST_ONLY build dispatch card drafted, 2026-09-28

The CP-1b ruling's "Next" line (the bounded S5 build handoff from the release head) is now drafted as [the S5 build dispatch card](../../briefs/handoffs/2026-09-28-s5-test-only-build-dispatch.md), for review and the operator's merge.
- **What it does:** it freezes the S5 packet at the release head `05f3788` and dispatches it to the packet's named executor, GLM, through `glm_agent`. It adds no build requirement.
- **Where the build stops:** at the packet's §5 push-and-return, before any Linux or CI run.
- **Scope:** the packet's §2 files only. `fixture_producer.py`, which `/v7` precondition 1 edits, is one of §2's installed fixtures.
- **Drift check at drafting:** `origin/main` `d86f6ff` changes no code against `05f3788`, and the packet is byte-identical (SHA-256 `058c265e…d68c9`).

**Not granted:** dispatch before the merge; Stage 1c; any Linux or CI run; C3; S5 acceptance; any production value. RC-2, RC-3b and every C3 obligation in the CP-1b ruling stay open.

**Review folded, 2026-09-28.** One focused reviewer's four fixes and three minor findings on the draft (`6bf194d`) are folded into the card (its §9 records them). The corrections: `fixture_producer.py` is inside §2; the CP-1b ruling is read at the dispatch revision, not at the release head; the return names the `/v8` snapshot diff and the E-case ownership and defers the Linux-only items; the acceptance list carries every Windows-run §2 test file; and each `s5` dispatch, the subset iteration first, needs its own grant at C3, distinct from the C3 step 2 grant for the acceptance-grade run. A second focused review of the fold, on `f178c17`, found no blocker, and its five minor corrections are applied.

**Merged, and dispatch SHA recorded, 2026-09-28.** Codex accepted the card as a drafting outcome at `f98380d`, and the operator merged #547 at `eef77836473f7bc304018217f452fb68daa40f17`. That merge is the frozen dispatch revision in the card's §9, and the §9 premise items hold against it. This dispatches nothing: the GLM build dispatch needs the coordinator's grant, and every item under "Not granted" above still stands.

### Operator acceptance and coordinator application — RC-2 owner-text set (C3), 2026-09-29

**Source.** In session on 2026-09-29 the operator wrote: "accept corrections 3 and 8, and use the optional O-10 landing". Earlier the same day the operator gave GO to prepare the RC-2 owner text. Corrections 3 and 8 are the C3 evidence corrections in the register of `docs/notes/2026-09-27-s5-owner-text-and-rc6-draft.md`; correction 8's block replaces correction 3's and is the operative C3 check.

**Applied by this entry's commit**, against the pinned application head `origin/main` `3ce500e`:
- the accepted note's §3.1–§3.10 PROPOSED passages, verbatim, at their anchors, except for the four amendments recorded below. Every anchor is unchanged between `875ecf29` and `3ce500e`, and every "Current" quote matched its owner line before writing:
  - boundary spec §3.1;
  - full-E1 spec §2.2a, §2.4 (first and last paragraphs), §2.5, §2.6 (the two table rows and the new paragraph) and §5;
  - slices plan contract decision 3;
  - S5 draft §2.3.
- the two D-2 bridging notes ("This note is removed when the §2.6 text lands at C3"): contract decision 6 and S5 Behavior.

**Amendments after Codex review of this PR (2026-09-29).** Four passages differ from the accepted note's text:
- §2.2a seed digest (note §3.2). The note says each seed is replaced by "its digest", which leaves the construction undefined. The applied text specifies HMAC-SHA256 keyed by the attempt salt over the seed record's canonical bytes, with the client recomputing after reveal. The operator chose this wording in session on 2026-09-29. It is the wording proposed in `docs/notes/2026-09-27-host-obligations-assignment.md`.
- §2.6 re-execution limits (note §3.6). The note says "once, and at most twice per campaign". The applied text restates accepted rule R9 of `docs/notes/2026-09-26-s5-decision-draft.md`: once per interruption, at most twice per campaign, and an interruption of the second re-execution is terminal. This restates R9 and adds no new limit. The operator accepted this wording in session on 2026-09-29.
- §4 release falsifier (outside the note's passages). "Repeats a started draw" now carries the same exemption the accepted §5 text has: a §2.6 bounded same-sample re-execution is not a repeat. Without it, exercising the §2.6 path would trip the falsifier. The operator accepted this wording in session on 2026-09-29.
- Contract decision 3, cumulative bound (note §3.8). The note's inequality omits the control-helper CPU. The applied text adds it: payload quota × guardian runtime + guardian CPU allowance + bounded control-helper CPU ≤ the work's reservation, and settled charges + open reservations ≤ the frozen campaign cap, with the existing enforcement-granularity margins included in the allowances and counted once. This corrects an incomplete bound and restores the existing accounting. `guardian_unit_spec` subtracts `control_calls × (control_cpu_seconds + cpu_granularity_seconds)` before setting the guardian's `LimitCPU` (`ops/c1_rail/qualification/execution/campaign_supervisor.py`, lines 284–298), `_guardian_bus_call` documents the helpers as bounded separately (same file, lines 1574–1580), and the source analysis states the bound with the helper term (`docs/notes/2026-09-26-s5-decision-draft.md:211`). It is not a new ceiling, retry allowance or recovery authorization. The operator chose this in session on 2026-09-29. K3/recovery verifies that the complete bound remains enforced.

**Evidence** (on the applied tree):
- correction 8's block passes on the CRLF tree and an LF mirror, and fails on the unapplied tree as the note predicts;
- correction 3's block passes (for the record);
- the delta's §10 hook prints no `UNROUTED` for the boundary, K3, N1 or N2 rows. The full hook still prints `UNROUTED` for 13 rows outside RC-2 (K1, K2, K4–K8, N3–N5, E1–E3), which are not this set's.

**O-10: not applied.** The accepted note carries no O-10 passage: OQ-5 ruled it "Not used", and the note says the row is not drafted. The only earlier draft (S5 draft §1.5(b)) conflicts with:
- CP-1a (5)'s owner;
- D-8's admission-crash wording;
- §3.3's no-salt-hash rule.

Applying it would mean choosing wording. The coordinator drafted a reconciled O-10 row for the umbrella §0.8. The operator accepted it on 2026-09-29, and it lands in PR #555 after this commit merges, so that its routing reference to full-E1 spec §2.4 resolves.

**Effect.** RC-2 is met when this commit and the O-10 landing (PR #555, the optional RC-2 landing place the operator chose) are both merged and reviewed, and the C3 record cites both. Until then RC-2 stays open.

*[Updated 2026-09-30: both landings are merged. #552 merged at `37b590b` and #555 at `6c6759f`; this record cites both. The condition above is met on the merged, reviewed landings; the forward-looking text is the state at the time of writing.]*

**Not granted:** C3; S5 acceptance; Stage 1c; any Linux or CI run; any production value; the O-10 text.

### Operator rulings and recorded harness read — S5 C3 step 1, 2026-09-29

**Source.** The operator confirmed these in the "Coordinate parallel sessions" session on 2026-09-29 ("confirmed. send the read"). That session relayed them to this one, and the operator confirmed the relay directly here the same day ("Yes, record A–C").

**Reviewed heads.**
- S5 executor return: `claude/s5-part-a` at `c7713e7`, status DONE_WITH_CONCERNS (packet §7).
- Stage 1c harness: `claude/s5-stage1c-harness` at `0fe3e25`, which is `c7713e7` plus one harness commit.

**A. Recorded read of the Stage 1c harness diff** (r2 §12.4: "Without that record the dispatch is not made").
- **Scope:** two files only, `measure_part_a_max.py.txt` and its README under `docs/notes/2026-09-27-s5-part-a-measurement/`. Nothing under `ops/`, `core/`, `tests/` or the workflow changed.
- **The eight harness decisions are read and accepted:**
  1. the SR-5 capture is staged once per job and copied into each repeat;
  2. staging runs in a child process;
  3. the boundary opens before the receipt and assessment reads, which is conservative;
  4. admission is the whole `admit_source` call;
  5. the guard's memory limit is 64 GiB, so it measures and never trips;
  6. an S5-D1 prefix failure is I-4;
  7. the parent check is I-7 at summarize, for both jobs;
  8. P-7 is checked through `run_worker.__globals__` and `co_names`, before and after the call.
- **Checked:** the 1c path's post-call `dataclasses.replace(request, within_pp=...)` only rebuilds the record's workload description, outside the boundary. The adapter builds its own request, so the seam is not bypassed.
- **Condition before dispatch.** Run `tests/test_s5_part_a_measurement_harness.py` on `0fe3e25` through the launcher and record the result.
  - **Result (2026-09-29, from a detached LF worktree, ops-env CPython 3.13.2):** 138 collected, **129 passed, 8 skipped, 1 failed**. Record `20260929T184959Z-397992611a69` (SHA-256 `3047df3a…c6ce3a`), `source_stable` true, capture complete.
  - The one failure, `test_cli_unreadable_start_head_is_i7[ÿþ]`, **reproduces identically on the base `c7713e7`**: record `20260929T185050Z-5209d398750b` (SHA-256 `1d69db75…f0fd1`), with the same counts. No additional failures were observed in the executed Windows cases; the eight POSIX-only cases remain unexecuted there.
  - The 8 skips are the POSIX-stub workflow-step tests, which do not run on Windows.
  - The condition's word "passing" is **not literally met**, because of that one base-reproduced Windows failure. The operator decides whether this satisfies it before any Stage 1c dispatch.
  - **Operator ruling, 2026-09-29:** "met, and include the harness regression module in the first Linux subset". The condition is **met**. `tests/test_s5_part_a_measurement_harness.py` runs on Linux alongside the first C3 Linux subset, where its 8 POSIX-stub cases execute. The S5 subset selector (`-f mode=s5 -f cases=…`) selects only the boundary-integration files, so this module needs a companion Linux run bound to the same head. Retain the companion run's launcher record and cite it beside the first subset's record, with both records identifying the same tested commit and the companion results showing all eight POSIX-stub cases executed. Neither run is granted by this entry.

**B. Rulings on the §7 concerns of `c7713e7`.**
1. The four out-of-§2 test files (`test_campaign_funding.py`, `test_campaign_snapshot_versions.py`, `test_checkpoint_widening.py`, `test_checkpoint_validation.py`) are **ADMITTED**, test-only.
2. The G5 completion-state tuple gaining `FULL_PASS_READY` and `PART_A_FAILED` is **ACCEPTED**.
3. G5 dropping full source admission for PART_A is **ACCEPTED for TEST_ONLY**, on condition that Codex's C3 review confirms the G5 closure rule requires it. G5 relies on the contract-pinned calendar digest and the frozen FULL population.
4. Pilot identity checked against the plan is **ACCEPTED for TEST_ONLY**. **Carried forward:** before the acceptance-grade or production run it must be strengthened to an independently observed pilot draw.
5. The P-4 by-construction limitation is **ACCEPTED**: byte equality with the frozen derivation is at least as strong as a parser refusal.
6. The SR-8 CPU split exported as null is **ACCEPTED** as disclosed.
7. The hook-workaround writes are **ACCEPTED**: they were in scope and reviewed before each commit, and no new rule is added. Codex's C3 review is asked to look closely at the escalation-lane commits `e38b308`, `c2f834a`, `3362b43` and `d4afa5b`.
8. The Linux cases were not executed. There is no ruling; the C3 Linux grant covers them.
9. Memory at zero headroom from `bind_budget`: **PROCEED**. Stage 1c measures it. A measured excess is a stop at C3, and no budget is widened beforehand.

**C. The executed `bind_budget` evidence is now durable.** It is in [`docs/notes/2026-09-29-s5-c3-record/`](../../notes/2026-09-29-s5-c3-record/README.md): the script and its output, with SHA-256 pins.
- Σ CPU 1,680 ≤ 10,000; Σ wall 4,200 ≤ 10,000; max phase memory 256,000,000 = 256,000,000; state `BOUND`.
- The unextended control is `BUDGET_EXHAUSTED`.
- **RC-3b's executed budget-binding check is done; RC-3b remains open overall.** Stage 1c, measured memory feasibility, and Stage 2/PA-5 remain outstanding.

**Codex C3 step-1 review, 2026-09-29: RESOLVED** (a reviewer verdict, not C3 or S5 acceptance). Scope: `05f3788..c7713e7`, the four escalation-lane commits and the rulings above.
- **B3: yes.** The unchanged closure test (`tests/ops/qualification/execution/test_runtime.py:20`) excludes `production_source` from G5, so full source admission would violate it. The calendar-based replacement satisfies the rule and refuses all four re-minted mutations: nonexistent session, wrong-position session, substituted prefix and reordered prefix. The rule requires the loader's exclusion; it does not uniquely prescribe this implementation.
- **B7: yes.** `e38b308`, `c2f834a`, `3362b43` and `d4afa5b` match their declared scope. There are no weakened tolerances, suppressed assertions or production forcing paths. `537cb17` corrects `d4afa5b`'s wording to "before artifact creation".
- **Conformance.** Every SR-1..SR-9 and P-1..P-7 node exists, exercises its stated behavior and passes; P-3, P-4 and P-5 hold. The `/v7` roles, `/v8` snapshot, two-artifact custody and transitively bound N2 baseline are consistent with the packet. SR-8's Linux export production and P-7's Stage 1c execution remain unexecuted.
- **Disclosures.** All six are confirmed: pilot identity proves plan agreement only; P-4 holds by construction for the plans; G5 completion gains both states; the CPU split is null; above-FULL is unreachable at N2 depth 60; the inode case proves neither SIGKILL nor power-loss behavior.
- **Linux: yes, conditionally.** Green execution of the four Part A nodes would establish the four required witnesses. Discharging packet §4's full Linux line also needs the full S4-plus-Part-A selection with valid retained evidence.
- **Verification:** a fresh Windows launcher run of nine reviewed modules on the unchanged `c7713e7` (ops-env CPython 3.13.2): `python -m pytest tests/ops/qualification/execution/test_campaign_part_a.py tests/ops/qualification/execution/test_worker.py tests/ops/qualification/execution/test_runtime.py tests/ops/qualification/execution/test_release.py tests/ops/qualification/execution/test_profile.py tests/ops/qualification/test_journal_snapshot.py tests/ops/qualification/test_checkpoint_validation.py tests/ops/qualification/test_result_adjudication.py tests/test_s2_run_evidence.py -q` (the record's `requested_command`). The harness regression module is not among them; it ran separately on Linux (below). **340 passed, 0 skipped**; record `20260929T192731Z-28f8c6e20559` (SHA-256 `f22359a9122235f530d0af1d05cdecaf3cb973ede93d6d6e1363c7175f549d9c`). The record shows completed, exit 0, `source_stable` true, complete capture and no report errors; the coordinator re-read it.

**Still open at C3:**
- the operator's C3 step-1 decision;
- Stage 1c: Linux dispatch after the operator's C3 Linux grant;
- RC-2's merge (#552) and O-10's merge (#555);
- Stage 2/PA-5 after the acceptance-grade run;
- OQ-1, Q1, Q7 and Q9.

**Not granted:** the C3 Linux grant, any dispatch, C3 acceptance, any merge, and any production authority.

### Operator acceptance — S5 C3 step 1 accepted; C3 Linux grant, 2026-09-29

**Source.** In session on 2026-09-29 the operator wrote: "Accept C3 step 1. B3 accepted, with "G5 independent bars verification" carried to the CP-6 inventory as a residual. B4 accepted for TEST_ONLY; strengthening to an independently observed pilot draw is due with T05, before CP-6. B7 closed per Codex. C3 Linux grant: open a draft do-not-merge PR for claude/s5-stage1c-harness to get the harness module's Linux run at 0fe3e25, cited beside the first subset. Then Stage 1c (dry run, then measure), the first diagnostic subset, the full S4-plus-Part-A selection with retained evidence, then Stage 2/PA-5. No pushes to claude/s5-part-a or claude/s5-stage1c-harness while any run is in flight."

**Effect.**
- **C3 step 1 is ACCEPTED** on the S5 return `c7713e7` and the harness `0fe3e25`. The basis is the entry above: Codex RESOLVED, and the executed `bind_budget` check.
- **B3 is accepted.** The residual **"G5 independent bars verification"** is carried to the **CP-6 inventory**. For PART_A, G5 does not re-verify the calendar ↔ population-index ↔ bars consistency.
- **B4 is accepted for TEST_ONLY.** Strengthening pilot identity to an independently observed pilot draw is **due with T05, before CP-6**.
- **B7 is closed** per Codex's review.
- **C3 Linux grant, in this order:**
  1. The harness module's Linux run for `0fe3e25`, through a draft, do-not-merge PR of `claude/s5-stage1c-harness`. It is cited beside the first subset. `pull_request` CI checks out the PR merge ref, so the coordinator binds the run to `0fe3e25` by showing that the harness module, the harness and the measurement workflow are byte-identical there.
  2. Stage 1c: the dry run, then the measurement, under r2 §12.4 and the §12.7 caps.
  3. The first S5 diagnostic subset.
  4. The full S4-plus-Part-A selection (`mode=s5`), with retained evidence.
  5. Stage 2/PA-5 from that run.
- **Standing constraint:** no pushes to `claude/s5-part-a` or `claude/s5-stage1c-harness` while any run is in flight.

**Not granted:** S5 acceptance (it follows Stage 2/PA-5), any merge of the draft PR, any production value, and any activation or live authority. RC-2 still becomes met only when #552 merges and is reviewed. *[Updated 2026-09-30: #552 and #555 are merged (`37b590b`, `6c6759f`); RC-2 is met.]*

### Coordinator execution — C3 Linux grant steps 1–2; Stage 1c stopped PA3_FAILURE; operator ruling: fix the harness and re-measure, 2026-09-29

**Step 1: the harness regression module on Linux.**
- **Run:** draft do-not-merge [#557](https://github.com/Joshua-Asante/first-passage/pull/557), `pytest (3.11)` run `36624580401` (`pull_request`). It tested merge `0b5732ae` = `main` `37b590b` + `0fe3e25`.
- **Binding to `0fe3e25`:** at that merge, `tests/test_s5_part_a_measurement_harness.py`, the harness, its README and `.github/workflows/qualification-s5-part-a-measurement.yml` are byte-identical to `0fe3e25`.
- **Result:** **138 passed, 0 failed, 0 skipped**, including the 8 POSIX-stub cases that Windows skips. The run's junit SHA-256 is `080b4f0a4f883d2fcedcd05f149763380ad67067e8efd9b9953dee3dc2c0e796`. The JUnit file (1.33 MB, over the public tree's 1 MB file cap) is archived privately in [first-passage-archive#846](https://github.com/Joshua-Asante/first-passage-archive/pull/846); the second #557 run (`36641530220`, `b5f53da`) JUnit `4b2cb9ae4109196579a22e4fb61efa2c1ea29d6bb88544c74a14ca1254fdcea` is archived with it.
- It is cited beside the first diagnostic subset, as the operator ruled.

**Step 2: Stage 1c** (the r2 §12.3 block in its Stage 1c form, from the C3 record worktree; `BRANCH=claude/s5-stage1c-harness`, `BASELINE=2026-09-29T00:00:00Z`, `S5_HEAD=c7713e7`).
- **Dry run `36634115845`:** ran on `0fe3e25`, exit 0, `stop_class` none, cleanup clean, `dispatched_parent` = `c7713e7`.
- **Measure run `36634465166`:** ran on `0fe3e25`. Jobs a and b each had exit 0 and validity OK, clean cleanup receipts and `dispatched_parent` = `c7713e7`. No re-run was used.
- **CPU and wall screens:** feasible.
- **Combined record** `stage1c/36634465166-combined.json`: `memory_feasibility` **FAILED**, `stop_class` **`PA3_FAILURE`**. The PA-3a screen gives 1.5 × M̂ = **346,773,504 B > 256,000,000 B**, where M̂ is job a's `forced-1` peak of 231,182,336 B. Job b alone read VERIFIED (235,991,040 B).
- **The block stopped** on the stop class, as §12.7 requires.
- **Evidence retained** under `docs/notes/2026-09-27-s5-part-a-measurement/stage1c/`, with the manifest `downloads-s5-1c-20260929T213343Z.sha256`.
  - Following the Stage 1b precedent, `journal.log`, `summarize.log`, `probe.json` and `git-head.txt` are held back from the public tree. **Their private archive to first-passage-archive is done (2026-09-30, [first-passage-archive#846](https://github.com/Joshua-Asante/first-passage-archive/pull/846), awaiting the operator's merge): the held-back files of the dry runs `36634115845` and `36647169582` and the measurement runs `36634465166` and `36647434808`, checked by the archive tool's content-address verification.**
  - The public-clone review found only runner work-tree paths.

**Diagnosis (coordinator).** The excess is the **first repeat of each job's first arm**, whichever arm that is:

| Repeat | Peak | CPU |
|---|---|---|
| job a `forced-1` | 231,182,336 B | 111.6 s |
| job b `prescribed-1` | 232,239,104 B | 76.5 s |
| other arm's cold repeat | about 157–158 MB | normal |
| warm repeats | 87–91 MB | 5–11 s |

That repeat is the one where harness decision 1 builds the SR-5 staged N2 capture: a genuine depth-60 N2 worker, run in a child process inside the repeat's own unit. Its CPU is excluded as setup, but its memory lands in the unit's `memory.peak` (r2 §8.2). The PART_A payload footprint is the cold and warm figures, consistent with Stage 1b's cold maximum of 169 MB.

**Operator ruling (2026-09-29), chosen over two alternatives:** "Fix harness, re-measure". The alternatives were to rule the staging repeat out of this record, or to treat 346.8 MB as binding and hold S5. Under B9 this record stays a stop: no budget is widened, and it is not reinterpreted.

**Next:**
- the harness fix moves the SR-5 staging outside every measured unit, and a repeat refuses without the staged cache;
- the measurement branch is rebuilt as `c7713e7` plus one harness commit;
- the operator records a read of the new diff;
- the operator gives a fresh Stage 1c approval with a new `BASELINE`, for one dry run and one measure (this approval's §12.7 measure dispatch is spent).

The first diagnostic subset and everything after it wait for a valid Stage 1c.

### Archive record for the S5 C3 evidence (2026-09-30)
Private copies in `first-passage-archive`; none is acceptance evidence.
- [#846](https://github.com/Joshua-Asante/first-passage-archive/pull/846) (merged): the held-back Stage 1c files for dry runs `36634115845`, `36647169582` and measurement runs `36634465166`, `36647434808`, plus the #557 Linux JUnit files (`080b4f0a…`, `4b2cb9ae…`).
- [#847](https://github.com/Joshua-Asante/first-passage-archive/pull/847): the executed harness delta `c7713e7..b5f53da` (README, `measure_part_a_max.py.txt`, the harness test) as a tar, SHA-256 `004f69a27009fb6b1b4406e1a5f122466b1433ad31d9f8339268bd70367d1693`. `b5f53da` is no longer reachable from `claude/s5-stage1c-harness`.
- [#848](https://github.com/Joshua-Asante/first-passage-archive/pull/848): the diagnostic subset artifacts `36648289195` and `36652211355` (49 files); per-file hashes in [`subsets-archive.sha256`](../../notes/2026-09-29-s5-c3-record/subsets-archive.sha256) (manifest SHA-256 `1f2ab5bade742e065990c528538389cb1d100a37e540ee1285f513ac2c538e62`). - [#849](https://github.com/Joshua-Asante/first-passage-archive/pull/849): diagnostic subset `36660441353` (34 files, the re-run on `d2e00a9`); manifest [`subset-36660441353-archive.sha256`](../../notes/2026-09-29-s5-c3-record/subset-36660441353-archive.sha256), SHA-256 `4558561501efcb2bb6589b9d522bce01d1812fb371955ee797d8d256a740cb86`.
- [#850](https://github.com/Joshua-Asante/first-passage-archive/pull/850): diagnostic subset `36670938260` (37 files, run at `072c133`, JUnit `c75cb48e…`); manifest [`subset-36670938260-archive.sha256`](../../notes/2026-09-29-s5-c3-record/subset-36670938260-archive.sha256), SHA-256 `dbfdd7f9316a2b65c3ddcd0eb6a4887c5f3478da68bb4f5c57c285e100901009`.
- [#851](https://github.com/Joshua-Asante/first-passage-archive/pull/851): the full S4+Part-A run `36673465130` at `072c133` (103 files). **The run is RED:** a memory-cgroup OOM in the shared qualification slice (limit 250000 kB) killed the supervisor during S5 node (c), the 12 later nodes failed with a refused connection, and 14 of 26 failed. Load-bearing evidence, not acceptance. Manifest [`full-36673465130-archive.sha256`](../../notes/2026-09-29-s5-c3-record/full-36673465130-archive.sha256), SHA-256 `d2ac1f1050fc920c0635af0de233da2af70591acc6caecfdb7d612ce2e2a1a01`.
- [#852](https://github.com/Joshua-Asante/first-passage-archive/pull/852): the OOM diagnosis runs. `36678879864` is the instrumented full run at `553270d` (107 files, **RED**, it reproduced the C3 memory-cgroup OOM; includes `fp-diag/memory-samples.jsonl`); manifest [`diag-36678879864-archive.sha256`](../../notes/2026-09-29-s5-c3-record/diag-36678879864-archive.sha256), SHA-256 `80e5edf904cf92401c06fa9f117ab89701da1f6ec140f053039a54ff6eac42f4`. `36677826842` is the aborted attempt at `f0fc885` (14 files, zero tests, plugin import failure); manifest [`diag-36677826842-archive.sha256`](../../notes/2026-09-29-s5-c3-record/diag-36677826842-archive.sha256), SHA-256 `b1fc2009eaecb70a9fbbd96747c24f8fae5fc519979d3336e695fbe8488e8cf4`. Diagnostic evidence, not acceptance.

- [#853](https://github.com/Joshua-Asante/first-passage-archive/pull/853): the full S4+Part-A run `36766144433` at `606e6e0` (132 files; **GREEN**, 27/27 required nodes, record `20d0a964…`). Its `boundary/journal.sqlite` is 182 MB, over the archive tool's 95 MB cap, so it is archived as `journal.sqlite.gz` (SHA-256 `7ace9a9d11fbd0e79bdde119739597b9b0cf9119f269c24cba32ade226c84ef6`). That file decompresses byte for byte to the raw journal, SHA-256 `efec03b10f30f74ec8bd29a26792b5864fc99313c69f3b51fda3a305b1f1be86` (round trip verified). Manifest [`full-36766144433-archive.sha256`](../../notes/2026-09-29-s5-c3-record/full-36766144433-archive.sha256), SHA-256 `f1be0c76dc4447ae21ffcbc43dad3cc6b20633a20d9404e84cf9306dffccf52e`; it lists both the raw journal and the `.gz`. A full local copy is kept, gitignored, at `local_artifacts/s5-c3-evidence/full-36766144433/` in the primary checkout. Recorded by the coordinating session on 2026-09-30; archiving was approved by the operator.

#846–#852 are merged; #853 is open until the operator merges it. Later diagnostic subsets are archived the same way once the S5 session confirms them final.

### Harness fix `b5f53da` read; fresh Stage 1c approval, 2026-09-29

**Harness fix.** `claude/s5-stage1c-harness` was rebuilt as **`b5f53da44ea9ce4e75c17501ec8051836f5b2edf`** = `c7713e7` + one harness commit. It supersedes `0fe3e25` (force-with-lease; no run was in flight).
- **Scope:** three files only: `measure_part_a_max.py.txt`, its README, and `tests/test_s5_part_a_measurement_harness.py` (7 new tests, 14 cases). `.github`, `ops` and `core` are unchanged.
- **Staging:** SR-5 staging runs in the probe step's `--probe-verdict`, after the probe unit stops and before any `fp-s5pa-1c-*` unit starts. Its own peak is recorded as `setup_excluded` (`n2_staging`). Each repeat still copies and verifies the staged mount inside its unit. A repeat without the cache refuses (I-6).
- **README:** decision 1's old text is shown struck through as SUPERSEDED.
- **Windows regression at `b5f53da`:** record `20260929T224520Z-b94174d9d790` shows 143 passed, 8 skipped (POSIX-stub) and 1 failed, the base-reproduced `test_cli_unreadable_start_head_is_i7[ÿþ]`. `--check-stage 1c` exits 0.

**Coordinator read** (the "Coordinating parallel Claude sessions" session, 2026-09-29): **all six conditions MET, with two notes and no blocker.** The operator recorded it here on 2026-09-29.
- **Note 1 (file ownership):** the stager runs under `sudo`. The repeat units also run as root: `sudo systemd-run` with no `--uid`, workflow `:226`. A dry-run refusal is checked explicitly before the measure dispatch.
- **Note 2 (side effect in a verdict helper):** SR-5 staging now happens inside `--probe-verdict`, a helper whose name says it only judges. This is accepted because it keeps the workflow frozen, and `--check-stage 1c` pins the dependency. **By operator choice it is recorded here rather than in the README**, so the reviewed head stays `b5f53da`. The README takes it with the next harness change, if any.

**Operator approval, 2026-09-29:** "Record read + approve".
- A **fresh Stage 1c approval** for **one dry run and one measure** on `b5f53da`, under r2 §12.7's caps, with **`BASELINE=2026-09-29T23:07:49Z`**.
- It is a new measurement, not a re-run of `36634465166`. That run stays the recorded stop.
- It is dispatched only after #557's Linux regression of the harness module is bound to `b5f53da` by byte-identity and passes.

**Pre-committed stop rule:** if this measurement also fails PA-3 on memory, it is a real result. The stage stops at C3 and returns to the operator with the numbers. There is no second harness fix for the same issue, and nothing is widened.

**Owed from the operator:**
- the private archive of the held-back Stage 1c files;
- the #556 merge.

### Coordinator execution — Stage 1c (fresh approval) VALID, memory VERIFIED, 2026-09-29

**Linux regression of the harness module at `b5f53da`** (the approval's precondition):
- **Run:** #557 `pytest (3.11)` run `36641530220` tested merge `9acfc804` = `028c5ce` + `b5f53da`. At that merge the module, harness, README and measurement workflow are byte-identical to `b5f53da`.
- **Result:** **152 passed, 0 failed, 0 skipped**, including the 14 new cases and the 8 POSIX-stub cases. The run's junit SHA-256 is `4b2cb9aee4109196579a22e4fb61efa2c1ea29d6bb88544c74a14ca1254fdcea`.

**Stage 1c** (the r2 §12.3 block in its Stage 1c form; `BASELINE=2026-09-29T23:07:49Z`; `MEAS_HEAD=b5f53da`; `S5_HEAD=c7713e7`):

| Check | Dry run `36647169582` | Measure run `36647434808` |
|---|---|---|
| Head | `b5f53da` | `b5f53da` |
| Exit / validity | exit 0 | jobs a and b exit 0, validity OK |
| Cleanup receipts | clean | clean |
| `dispatched_parent` = `measured_parent` = `c7713e7` | yes | yes |
| Re-run used | — | none |

- **Staging placement.** Every record shows `n2_staging.placement = probe_verdict_before_measurement_loop` and `stager_in_measured_unit = false`, with the stager's cgroup `/system.slice/hosted-compute-agent.service`. The stager's own peak RSS, about 120 MB, is recorded as `setup_excluded`.
- **Coordinator note 1 is checked:** no repeat refused, and the dry run's exit is 0.
- **Combined record** `stage1c/36647434808-combined.json` (SHA-256 `024cdcdd7e3c499af49f1358f7a4a6048641badc9b0679a99999f4bb8ba1f87e`): `memory_feasibility` **VERIFIED**, `stop_class` **none**, validity OK.
  - **PA-3a:** 1.5 × M̂ = **235,739,136 B ≤ 256,000,000 B**, a margin of 20,260,864 B (7.9%).
  - **Σ screen:** feasible (CPU input 120 s ≤ 8,440 s; wall input 300 s ≤ 6,100 s).
- **Per-repeat peaks, both jobs:** cold repeats 155.8–157.3 MB; warm repeats 87.7–91.1 MB.
- **The stopped record** `36634465166` (PA3_FAILURE) stays retained as the stop, and nothing was widened.
- **Held back** as before: `summarize.log`, `probe.json` and `git-head.txt` (and `journal.log`, never copied). **Archived with the run above ([first-passage-archive#846](https://github.com/Joshua-Asante/first-passage-archive/pull/846), awaiting merge).**

**Effect.** Stage 1c through the built adapter is valid and **ends the PART_A ceiling's provisional status** (r2 §12.4 output; r2 §13 step 6), with the named worker-side residual still carried by PA-5.

**Next under the C3 Linux grant:**
1. The first diagnostic subset: `-f mode=s5 -f cases='test_s5_'` on `claude/s5-part-a`, which selects the four Part A Linux nodes. The harness module's Linux runs above are cited beside it.
2. The full S4-plus-Part-A selection, with retained evidence.
3. Stage 2/PA-5 from that run.

### Coordinator execution — first diagnostic subset: two S5 build defects found; operator rulings, 2026-09-30

**Subset 1: run `36648289195`** (`-f mode=s5 -f cases='test_s5_'` on `claude/s5-part-a` at `c7713e7`; `DIAGNOSTIC_SUBSET`; cleanup ok).
- **Result:** all four Part A nodes **errored at setup**. The `/v7` boundary install failed with `parse_release`: "funding profile is persistence-only; runtime release not enabled".
- **Root cause:** `tests/integration/qualification_boundary/fixture_producer.py` `release_document` mapped profiles v3–v6 only, so a `/v7` profile kept release schema v1. Precondition 1 had extended the cap tuple in the same file but not this mapping. The precondition-1 unit test masked the gap by overwriting the schema by hand.
- **Operator ruling:** "Fix on S5 branch". The fix is **`c016c60`** (escalation lane): `/v7` maps to release `/v7` with dispatch set `['N1','N2','PART_A']`. The unit test now takes `release_document`'s output as-is, and it fails on the unfixed fixture with `release/v1`. The change touches installed test fixtures only; `ops`, `core`, `.github`, `scripts`, `tools` and `docs` are unchanged since `c7713e7`.
- **Stage 1c equivalence.** Stage 1c's staging path imports `test_profile` only for `document()`. Between `c7713e7` and `c016c60`, `document()` and every module-level statement of `test_profile.py` are AST-identical, so the Stage 1c result (`36647434808`) stands for the measured code.
- **Harness branch** rebuilt as **`c3bec2f`** = `c016c60` + the same harness commit. Its harness files are byte-identical to the reviewed `b5f53da`.

**Subset 2: run `36652211355`** (the same subset on `c016c60`; `DIAGNOSTIC_SUBSET`; cleanup ok). The `/v7` install now succeeds.

| Node | Result |
|---|---|
| (c) payload death between the Part A writes | **passed** |
| (a) genuine Part A without expansion | **failed**: "bounded N1 campaign wait expired" (1,080 s) |
| (b) genuine below-floor Part A | **failed**: same |
| (d) g5 unit death and exact retry | **failed**: the kill returned 1, "unit not loaded" |

**Artifact diagnosis** (s2-linux-run §3; read-only, from `journal.sqlite`, `journal.log` and the units):
- **(a) and (b) are a ROUTE DEFECT.** Every attempt reached `PART_A_READY` in about 300 s, and the Part A worker completed. Then the `part_a_g5` commit failed inside its own transaction with `ValueError: campaign budget state differs`, so there was no receipt and the campaign stayed `PART_A_READY`.
  - **Root cause:** `CAMPAIGN_BUDGET_STATES` (`ops/c1_rail/qualification/journal_snapshot.py:118-129`) and `CAMPAIGN_CHECKPOINT_STATES` (`:491-502`) were never widened for `FULL_PASS_READY`/`PART_A_FAILED`. `d6ea766` added them to `CHECKPOINT_ADVANCES` only, so the T2 snapshot re-parse refuses the new state and the transaction rolls back.
  - **Windows missed it** because no test drives a real-store `commit_checkpoint_assessment(checkpoint='PART_A')`: the widening test asserts constants only. Codex's C3 step-1 review and the §7 conformance table did not reach it either.
- **(d) is a TEST DEFECT.** By the service's hold semantics (`service.py:725-728`), the g5 unit exits by itself right after T1. The S3/S4 cases run the same kill with `check=False`, but S5's `assert kill.returncode == 0` (added in 3c for Codex's P2) cannot pass.
- **(c)'s evidence** reads sound. It is cosmetic that the retained failure reason carries raw docker stream frame headers.

**Operator ruling, 2026-09-30:** "Fix both, re-verify". The fix, on the escalation lane on `claude/s5-part-a`:
- widen both tuples, and sweep every closed state set for the same omission;
- add a real-store PART_A commit test that fails on the unfixed code;
- make (d) assert that the unit is inactive or absent after T1, keeping every load-bearing check.

**Re-verification before the Linux grant continues:**
- Windows lines 1–3, `check` and `git diff --check` on the new head;
- a **C3 step-1 addendum**, with Codex re-reviewing the commit path;
- the harness branch rebuilt, with a Stage 1c byte-equivalence record;
- one subset re-run.

This is a new defect, not the Stage 1c memory issue, so the pre-committed stop rule does not apply.

### Coordinator execution — re-verification after "Fix both": subsets 3–4, Windows on the fix head, C3 step-1 addendum, 2026-09-30

**Fix commit `d2e00a9`** (escalation lane, on `c016c60`).
- **Route fix:** `FULL_PASS_READY` and `PART_A_FAILED` are added to:
  - `journal_snapshot.CAMPAIGN_BUDGET_STATES`;
  - `journal_snapshot.CAMPAIGN_CHECKPOINT_STATES`;
  - `campaign_funding._decode`'s state tuple. The sweep found this one; it is load-bearing, because with only the journal tuples fixed the commit still fails with "funding state differs".
- **Not widened, deliberately:** predecessor-receipt checks that must equal `PART_A_READY`, and `PROGRESSION_PHASES`, where terminal states admit no phase.
- **New test:** `test_campaign_n2::test_part_a_commit_advances_through_the_real_store` drives a real `CampaignStore` to both terminal states. It fails on the unfixed tuples: record `20260930T021026Z-b44a8e48f267`. The ticket set passes, 140: record `20260930T021459Z-18977f084c59`.
- **(d) change:** assert the g5 unit is inactive, failed or absent after T1.

**Subset 3: run `36660441353`** (on `d2e00a9`; `DIAGNOSTIC_SUBSET`; junit sha256 prefix `07f2e01073242863`). The route defect is fixed: (a) and (b) now reach their terminal states, and (c) passed. Two test defects that the route defect had masked surfaced:
- **(a) and (b) failed** the exact staged-role assertion. It expected only the two S5-D1 roles, but the G5 output roles (`attempt_journal`, `runtime_load_trace`, …) are staged too. The assertion was over-narrow; the code was right.
- **(d) failed** with `NameError: name 'kill' is not defined`. The `d2e00a9` change dropped the binding. This is the **first failed correction** of (d) under AGENTS.md's two-failure rule.

**Second correction `072c133`** (Opus escalation lane, on `d2e00a9`; the Linux test module only, +39/−6).
- **Staged-role check:** it stays **exact**, against `PART_A_STAGED_ROLES = S5-D1 roles ∪ G5 output roles`. Each role is sourced to `campaign_supervisor.py:1889-1892`/`:1951-1954`, `g5.py:748-759`, `evidence.py:2944-2960` and `policy.py:144-154`. A run-time check confirms the set equals those production constants, and a separate assertion keeps S5-D1 presence explicit. The coordinator condition was to keep the check exact, not narrow it.
- **(d):** the kill `CompletedProcess` is bound again, and its return code is recorded as a fact.
- **Local records:** collection 4 in `20260930T041954Z-a597a6e06a4f`; the manifest and selector tests 72 passed, 1 skipped in `20260930T042005Z-ba9bfd218ed6`.

**Windows on `d2e00a9`.** `072c133` changes only the Linux-only module above.

| Line | Record | Result |
|---|---|---|
| line 1 | `20260930T023033Z-a30f6d25dabb` | 1248 passed, **2 failed** |
| line 2 | `20260930T032142Z-cbd001445b30` | 80 passed, 1 skipped; completed, exit 0 |
| line 3 | `20260930T032313Z-584196cbf455` | 1839 passed, 1 skipped; completed, exit 0 |
| `check` | `20260930T045102Z-84d632f6b610` | completed, exit 0 |
| `git diff --check` | — | exit 0 |

Line 1's two failures are the known pre-existing base failures, `test_s2_evidence_tooling_followups::test_validate_inputs_uses_the_wrappers_whitespace_test[\xa0-False]` and `[\u3000 \u2003-False]`. They are outside the S5 change. Line 1 is not a pass, and this record does not describe it as one.

**Subset 4: run `36670938260`** (on `072c133`; `DIAGNOSTIC_SUBSET`; source stable, capture complete, cleanup ok; junit sha256 prefix `c75cb48e7153356c`). **All four Part A nodes passed**, 4/0/0/0. The verification exit of 2 is by design for a diagnostic run.

**Harness branch** rebuilt twice:
- `cd3623b` on `d2e00a9`;
- then **`db748f8`** = `072c133` + the harness commit, pushed with a lease from `cd3623b` after subset 4 closed.

Its harness files are byte-identical to the reviewed `b5f53da`: all 91 blobs, empty diff.

**Stage 1c closure equivalence, `c7713e7` → `072c133`** (asked for by the coordinator seat). The full per-module table is in [`docs/notes/2026-09-29-s5-c3-record/stage1c-equivalence/`](../../notes/2026-09-29-s5-c3-record/stage1c-equivalence/README.md). It is computed from git blob bytes by the static import closure, using `runtime.source_closure`'s resolution rule.
- **Measured closure.** Roots: `worker` (holding `run_part_a_body`), `compute`, `production_source`, `part_a`, `production`, `plan`, `runtime` and `test_contract`, whose `NOW` is imported inside `_repeat_mode_1c`. That is **68 modules**, including `replay`, `model`, `runner` and `test_trust_domain`, with the same membership at both commits. **All 68 are byte-identical** (SHA-256 at each commit is in the table). Codex's C3 re-review (P2) found that the first version of this table omitted `test_contract` from the measured roots and so counted 66. Codex recomputed the closure independently and got the same 68, all identical.
- **Not in the closure:** `journal_snapshot` and `campaign_funding`, the two ops modules `d2e00a9` changed. So the route fix cannot change what Stage 1c measured.
- **Staging closure** (outside every measured unit). Roots: the harness's fixtures, `composition_fixture`, `bundle_fixture`, `test_worker`, `test_contract` and `test_profile`. That is 63 modules, and one differs: `test_profile.py`, changed by `c016c60`. The changed definitions are test functions and `fixture_producer_module`. `document()`, the only name staging uses, is AST-identical at both commits.
- **Result:** Stage 1c `36647434808` (VERIFIED, 1.5×M̂ = 235,739,136 B) covers the measured code at `072c133`. No re-measure decision is needed.

**C3 step-1 addendum.** Two claims behind the step-1 acceptance were incomplete:
- **§7.7's closed-set claim** (the return's statement that every state set naming the Part A states was widened) did not hold. Three closed sets omitted the new terminal states.
- **The review did not exercise the commit path.** The Windows suite and Codex's step-1 review had no real-store `PART_A` commit test, only constant assertions. Only Linux exposed the defect.

`d2e00a9` adds that test.

**Codex C3 re-review, 2026-09-30** (scope `c7713e7..072c133` and harness `db748f8`; a reviewer verdict, not C3 acceptance):
- (A) State-set sweep: no further improper omissions. The remaining narrow sets enforce checkpoint prerequisites or phase-admission boundaries.
- (B) Staged roles: the exact ten-role union is correct against the cited production paths, for both PASS and FAIL.
- Harness: SR-5 generation runs outside the measured units. Repeat-local copying deliberately stays inside them. A missing cache refuses with I-6. The harness files match `b5f53da`. Four existing harness checks passed against the `db748f8` source under the validated operations Python 3.13.2.
- One P2: the closure table omitted `test_contract` from the measured roots. It is corrected above (68 modules), and the conclusion stands.
- Codex did not re-run the Linux integration or the full suites.
- **An independent second Codex review** (a cloud task submitted by the coordinator seat, `task_e_6abcabc95e24832c8ea05349c49ef647`): **RESOLVED, no findings**. It corroborates A, B and the harness:
  - an AST sweep of `ops/c1_rail/qualification` plus a grep of the state literals, which found the remaining narrow tuples are checkpoint-specific guards;
  - the ten-role set;
  - the unchanged closure, with neither `journal_snapshot` nor `campaign_funding` in it;
  - `db748f8`'s blobs matching `b5f53da`;
  - the (d) assertion.

  It judged the original closure roots appropriate and did not raise the `test_contract` point. The 68-module correction is the more conservative reading, and both agree the closure is unchanged. That review could not run the tests either, because its environment has no `tmp/ops-env`.

The step-1 acceptance stands with this addendum.

**Full S4-plus-Part-A selection: run `36673465130`** (`-f mode=s5` on `072c133`; record `e49e91ce…`, scope `S5_PART_A`, source stable, capture complete, cleanup ok, tested commit = head) is **RED, a C3 memory stop**.
- **Result:** 14 of 26 required nodes failed; `s2_run_evidence.py` refuses the record.
- **Passed (12):** every S2 service, S3 N1 and S4 N2 node, plus S5 (a) → `FULL_PASS_READY` and (b) → `PART_A_FAILED`.
- **Failure:** S5 (c) failed "private transport child failed" during its n2g5 dispatch. At 05:56:41 a memory-cgroup OOM in the shared qualification slice (250,000 kB of 250,000 kB) killed the supervisor service, which ended "Failed with result 'oom-kill'". The 12 later nodes all failed on ConnectionRefused: one cause, a cascade.
- **Stopped:** no re-dispatch and nothing widened, under step-1 item 9. The evidence is archived privately.

**Diagnosis.**
- **Operator ruling, 2026-09-30:** "Diagnose first, no runs". A read-only diagnosis followed.
- **Operator ruling:** "go with the one instrumented run". Diagnostic branch `claude/s5-diag-memory` (not for merge): `072c133` plus a root sampler and a test-labelling pytest plugin only, at the same limit, with no ops, core, tests or tools change.
  - The first attempt, `36677826842` at `f0fc885`, ran zero tests: `scripts/fp.py:104-105` strips `PYTHONPATH`, so the plugin could not import. That was an instrumentation defect.
  - The corrected run `36678879864` at `553270d` reproduced the OOM exactly: 1,747 samples, 0 sampler errors.
- **Attribution: a combination, with the leftover io tmpfs decisive.**
  - Each work's checkpoint io tmpfs pair (`campaign_supervisor.py:2084-2104`) is stopped only by the harness's campaign cleanup (`tools/qualification_verification/campaign_host.py:155-170`).
  - Slice shmem equals the mounts' used bytes exactly, +3.17 MB per work: the staged 135-file bundle plus the plan in `in`, and `result.frame` in `out`.
  - At the OOM: anon 194.8 + kernel 7.1 + shmem 53.9 = 255.8 MB, with 17 pairs. Without the tmpfs, S5 (c) peaks at about 202 MB.
  - **This is production code/lifecycle, not test debris:** no ops code releases the mounts.
  - Only four readers use the mounts, all before `retain_checkpoint_capture` (`:2377`). Retry, g5 and recovery read the store only.
- **Unreclaimable headroom without the tmpfs:** a 225.7 MB peak (anon 199.3 + kernel 26.4, in S4 guardian-death-mid-N2), which is **30.3 MB, 11.8 %**. THP is `enabled=[always]`, with `anon_thp` up to 48 MB. Supervisor anon grows 57.0 → 72.7 MB, then is flat: bounded.
- **`memory_peak_bytes` = 256,000,000 for attempt `505c81c0` is clipped.** It is the whole slice's never-reset `memory.peak` (`campaign_supervisor.py:974`, `:804`), already at the cap from S3 on. PA-5 compares CPU only. The memory figure bounds only the shared footprint, through PA-3b. A per-phase figure needs a new field, because the store refuses a decreasing `memory_peak_bytes` (`campaign_store.py:3118-3119`).

**Operator rulings, 2026-09-30.** Source: in the coordinating session Joshua wrote "I agree with your recommendation. Send it to the S5 agent." He confirmed all three directly in this session ("Confirmed, proceed").
1. **io-mount release fix: GO.**
   - The card is frozen at `docs/briefs/handoffs/2026-09-30-s5-io-mount-release-card.md` on `claude/s5-part-a` and implemented on the Opus escalation lane.
   - Release happens after `retain_checkpoint_capture`, and after `_archive_part_a_for_inspection` before IN_DOUBT. Campaign cleanup is the backstop.
   - Order: four fail-first tests → Windows lines 1–3, `check` and `git diff --check` → a closure re-run on the fix head → Codex → one Linux full S4-plus-Part-A selection.
   - The new Linux mount-count assertion becomes a **required node** under `QEXEC-01`.
2. **Stage 2 memory, option (a).**
   - For TEST_ONLY, PA-5 is CPU-only, and PA-3b takes the whole-footprint `memory_peak_bytes` as an upper bound on the shared footprint.
   - A **per-phase memory field** (the payload unit's own `memory.peak`) is a named item before production qualification, recorded in the CP-6 behavior inventory. It is not built in S5.
3. **The 11.8 % unreclaimable headroom, option (a).**
   - Accepted for TEST_ONLY, with the cap unchanged.
   - Carried to production host sizing (T11/CP-8) as a named item, with the THP share (up to 48 MB `anon_thp`) to be separated there.

The failed run `36673465130` stays on record as the stop. This addendum's PR stays held until the fix's Linux selection has been read.

### Coordinator execution — io-mount release fix; full S4-plus-Part-A selection GREEN, 2026-09-30

**Card and amendments** (the escalation lane is Opus; the card is `docs/briefs/handoffs/2026-09-30-s5-io-mount-release-card.md` on `claude/s5-part-a`):
- Frozen at `50d229f` after the operator's GO. Each amendment below was committed before the work it governs.
- **A1** (`a3c8e77`, ruling "Bind mounts to the work"): the executor returned NEEDS_CONTEXT, because the guardian cannot `StopUnit` its mounts. Its bus child admits only `StartTransientUnit` (`deploy/qualification/bootstrap.py:93`), and the polkit rule admits unit-scoped actions only for `fpq`-prefixed names (`tools/qualification_verification/campaign_host.py:88-93`). A1 therefore binds each io mount unit to the work's guardian unit with exactly `BindsTo=`/`After=`.
- **A2** (`eff41ca`, ruling "Amend node (c) as proposed"): node (c) read `out_path` after settlement, so its host reads moved to before settlement.
- **A3** (`e7c9826`, ruling "Freeze the guardian"): Codex found two P2s, A2's read still raced and node (4)'s sampling was insufficient. A3 held node (c)'s window with a cgroup freeze, and node (4) moved to exact journal intervals.
- **A4** (`68a7fd7`, ruling "Archive-based on Linux"): Codex found that the freeze's acquisition raced and that deadlines run on while frozen. That was **node (c)'s second failed correction**, so the coordinator stopped under the two-failure rule and returned to the operator.
  - Node (c) restarted with explicit criteria. It makes no host mount read, keeps every settled assertion, checks the prefix on the staged bytes, and adds the release check.
  - Archive-to-mount fidelity is proven by fake-bus test (2), which covers both the abnormal-exit and absent-frame paths.
  - Node (4) ends an interval only at a deactivation record and fails on any failed stop.
  - **Removed from node (c) by operator ruling:** the host-side listing, 0444, `f_ffree`, and the on-mount absence checks.

**Code.**
- `7c97a69`: the only production change. `_io_mount_properties` gains `guardian_unit` and adds exactly `BindsTo`/`After`, +19/−2 in `campaign_supervisor.py`.
- Tests:
  - `d33bddf`: tests (1)–(3), fail-first on `072c133` (record `20260930T171825Z-b5f2756d3eb8`); they pass on the fix (`20260930T171850Z-6f40aacff83b`, the acceptance set, 259 passed, 1 skipped).
  - `5268f5b`: the harness.
  - `0ab8f6b`: the new required node `test_s5_io_mount_pairs_are_released_with_each_work_guardian` under `QEXEC-01` (41 → 42 nodes).
  - `aeabbd4`, then `606e6e0`: the A3 and A4 test revisions.

**Verification.**
- Windows on `0ab8f6b`:
  - line 1, `20260930T173142Z-7020a1971a25`: 1254 passed, **2 failed**. These are the known base whitespace cases in `test_s2_evidence_tooling_followups`; line 1 is not a pass.
  - line 2, `20260930T180209Z-0c7b29f1db56`: 80 passed, 1 skipped.
  - line 3, `20260930T180319Z-eaf81326edda`: 1845 passed, 1 skipped.
  - `check`, `20260930T191134Z-8366de74c21c`: completed.
  - `git diff --check` is clean.
- Later commits change only the Linux test file.
  - On `aeabbd4`: line 2 plus boundary-verification, `20260930T191324Z-410943c4e83c`, 106 passed, 1 skipped; collection `20260930T191502Z-17ef4e47a239`, 5 nodes.
  - On `606e6e0`: `20260930T192328Z-616ea49366fa`, 78 passed, 1 skipped; collection `20260930T192336Z-bc60f17958e1`.
- The Stage 1c closure re-run on `0ab8f6b` is 68 measured modules, all byte-identical to `c7713e7`, with `campaign_supervisor`, `campaign_store` and `campaign_host` outside it.
- Codex:
  - `eff41ca..0ab8f6b`: two P2s, both in tests. Production ordering, custody, BindsTo and Stage 1c were confirmed.
  - `e7c9826`/`aeabbd4`: three P2s.
  - `606e6e0`: **RESOLVED, no actionable findings.**

**Linux full S4-plus-Part-A selection: run `36766144433`** (`-f mode=s5` on `606e6e0`; record `20d0a964…`) is **GREEN**, and `s2_run_evidence.py --expect-head 606e6e0 --expect-scope S5_PART_A` reads `ok: true` with no refusals.
- `status=completed`, exit 0, verification exit 0; source stable; capture complete; cleanup ok; the tested commit is the head.
- `invariants.json` passed, 27 required nodes; junit 27/0/0/0 (sha256 `e408ad06…`).
- The only OOM on the host was the deliberate `test_s2_shared_memory_oom_is_retained_last`, which killed its own payload inside its work slice at the run's end. The supervisor was not killed.
- The Part A observation's `memory_peak_bytes` is again 256,000,000. That is the clipped slice-wide peak, which by operator ruling (2) is an upper bound only.

**Next under the C3 Linux grant:** Stage 2/PA-5, CPU-only for TEST_ONLY.

**Not granted:** C3 acceptance, S5 acceptance, any merge of `claude/s5-part-a`, and any production authority.

**Not granted:** C3 acceptance, S5 acceptance, any merge of `claude/s5-part-a`, and any production authority.

### Stage 2 / PA-5 (2026-09-30)

**Record:** [`stage2.json`](../../notes/2026-09-27-s5-part-a-measurement/stage2.json), produced by [`stage2.py.txt`](../../notes/2026-09-27-s5-part-a-measurement/stage2.py.txt) (arithmetic over retained evidence only). The work was done by an Opus worker seat under the C3 Linux grant's step 5, with no new dispatch.

**Source.** The green full S4-plus-Part-A run `36766144433` at `606e6e0`. `s2_run_evidence.py 36766144433 --expect-head 606e6e0 --expect-scope S5_PART_A`, run through the launcher at `606e6e0`, reads `ok: true` with no refusals (27 required nodes; junit 27/0/0/0). The SR-8 export `boundary/part_a_observations.json` (SHA-256 `d4b682ce…`) comes from node (a), attempt `linux-cca27e50…`, `FULL_PASS_READY`, 2 → 2 panels.
- **Run binding.** The artifact's contents carry no GitHub run id, so the binding goes through GitHub's own records:
  - the artifact listing for run `36766144433` names artifact `11124634769` (`workflow_run.id` `36766144433`, head `606e6e0`) with digest `sha256:362c22af…`;
  - the retained zip hashes to that digest;
  - every input is read from inside that zip, and every input file is pinned by SHA-256 in the helper and in `stage2.json`.
- **Measured identities**, read from the run's journal (the attempt's admission receipt and its retained objects), with each digest recomputed from its bytes:
  - release `qualification_execution_release/v7` `15f6fcbc…`;
  - profile `qualification_execution_profile/v7` `31b22d2b…`;
  - policy `qualification_policy/v1` `21251022…`.
- The budget snapshot's whole profile and whole budget hash to the receipt's `budget_profile_sha256` and `budget_sha256`, so O and `maximum_memory_bytes` are the admitted values.
- **Archive:** the private inputs are the artifact zip (50.7 MB), the run and artifact listings, and the reader's output. They are under `local_artifacts/s5-c3-evidence/stage2-read-36766144433/` and archived in [first-passage-archive#854](https://github.com/Joshua-Asante/first-passage-archive/pull/854), with each blob verified to hash to its content address. Pin manifest: [`stage2-36766144433-archive.sha256`](../../notes/2026-09-29-s5-c3-record/stage2-36766144433-archive.sha256). The run's unpacked files are in #853 (merged).

**PA-5 (CPU-only for TEST_ONLY, ruling (2) above): RE-APPLY.**
- *Service* = **29.896463 s**: the PART_A work's `charge_cpu_ns`, the whole settled charge with nothing deducted (r1 PA-5, kept by r2 §9). SR-8's payload/guardian split is null (step-1 ruling B6), so the charge includes the 20 s O. *[Corrected 2026-09-30 after Codex review of `826caa3`: the first version deducted O and used 9.896463 s.]*
- *Harness* = 7.329488 s: the Stage 1c prescribed-arm maximum `cpu_input_s` (combined record `024cdcdd…`, job b `prescribed-1`, cold, on an EPYC 7763).
- **k = 29896463 / 7329488 = 4.078929 > 1.25.**
- **Re-application, computed and not adopted:**
  - **CPU:** Ĉ₁c × k = 43.429 s gives B = 86.858 s, so B + O = 106.858 s and the CPU ceiling stays **120 s**. The headroom is 13.142 s: 10.95 % of the 120 s ceiling, or 12.30 % of B + O. k can rise 15.1 % (to 4.696) before the CPU ceiling moves.
  - **Wall:** Ŵ₁c × k = 44.010 s gives 3 × (44.010 + 30) = 222.03 s, so the wall ceiling stays **300 s** (headroom 77.97 s; it holds while k ≤ 6.488).
  - Both equal the shared PART_A ceilings, so no new value or profile revision follows.
- **Non-governing diagnostic:** `cpu_ns` alone (9.896463 s) gives k = 1.350226, and also 120 s / 300 s.
- **Host normalization** (Codex P2, 2026-10-01). Both host facts are read from pinned evidence: the run's `kernel.log` names an EPYC 9V74, and the Stage 1c maximum ran on an EPYC 7763. Stage 1b (`36364854404`) gives a factor of 1.5344 (7763 / 9V74 forced median, same workload). That workload differs from Stage 1c and Stage 2, so the factor is indicative only.
  - **Measured host:** k = 4.0789, CPU ceiling **120 s**.
  - **Normalized to the 7763, compute only** (O is fixed overhead): k = 4.8005, B + O = 122.22 s, so the CPU ceiling would be **130 s**.
  - **Normalized to the 7763, whole charge scaled:** k = 6.2589, B + O = 153.28 s, so the CPU ceiling would be **160 s**.
  - The wall ceiling stays 300 s on every basis. Nothing is adopted.
- **Launch allowance L (PA-2):** measured at **4.848 s**, from the reservation's UTC to the PART_A capture's `started_utc`; the RUNNING transition is at 4.414 s. That is within L = 30 s. The re-application keeps L = 30 s, which is conservative, and the 300 s wall floor binds either way.

**PA-2b (CP-1a (1)(b)(i)):** holds against the applicable B. `predicted_seconds` = 27.082 s and `probe_seconds` = 3.988 s.
- The approved predicate, 1.5 × P ≤ B, gives 40.62 s ≤ 100 s (the applied ceiling minus O) and ≤ 86.86 s (the re-applied B).
- It **fails against the unscaled Stage 1c B** (21.29 s), because the service's throttled P is 3.4× the harness's P̂₁c. That B no longer governs after re-application, and this is recorded, not hidden.
- Engine diagnostic: 40.62 s ≤ 265.12 s, the lower bound on `budget_seconds`.
- The 1.5 × P̂ term's check is now recorded.

**Memory (`upper_bound_only_not_attribution`):** `memory_peak_bytes` 256,000,000 against `maximum_memory_bytes` 256,000,000.
- The binding is the attempt's budget snapshot, together with the PART_A phase `memory_bytes` in the measured release's campaign budget profile.
- The reading is clipped at the binding, and the work recorded 0 OOM events. It bounds the shared footprint above only.
- m_m headroom (PA-3b) cannot be shown from a clipped reading.
- It is not a Part A figure and not a PA-5 input.

**Re-measurement triggers (r2 §9):**
- **Trigger 6, k > 1.25, is engaged.**
- **Trigger 5 is not engaged.** By the operator's ruling of 2026-10-01 (below), its CPU limb compares compute-only CPU: `cpu_ns` 9.90 s ≤ 0.8 × B₁c = 17.04 s. The whole charge, 29.90 s, is kept as a diagnostic labelled "trigger 5 is not evaluated on this basis by ruling". Trigger 5's other limbs are not engaged either: the 34.88 s from reservation to CAPTURED is ≤ 240 s, the work COMPLETED, and there were 0 OOM events.

**Operator ruling, 2026-10-01 (trigger 5 basis).** Joshua, in the coordinating session: "go with your recommendation to rule that trigger 5 compares the compute-only CPU". The coordinator relayed it to this worker seat, and Joshua confirmed it directly here.
- r2 §9 trigger 5's CPU limb compares compute-only CPU (`cpu_ns`, O excluded), because O is fixed overhead and not workload.
- PA-5 keeps the whole-settled-charge basis.

**Dispositions:** trigger 6, the faster-host caveat and the PA-3b memory headroom are ruled in the next entry, "Operator rulings, 2026-10-01 (trigger 6, host, memory)".

**Not granted:** C3 acceptance, S5 acceptance, adoption of any re-applied value, any merge of `claude/s5-part-a`, and any production value.

### Operator rulings, 2026-10-01 (trigger 6, host, memory)

**Source.** Joshua, in the coordinating session: "Go with recommendations for all 4" (the fourth is the trigger 5 basis, recorded in the entry above). The coordinator relayed the rulings to the Stage 2 worker seat, and Joshua confirmed all three directly there ("Confirmed, record all 3"). They are recorded in [`stage2.json`](../../notes/2026-09-27-s5-part-a-measurement/stage2.json) under `operator_rulings`.

1. **Trigger 6 (k = 4.078929 > 1.25).** For TEST_ONLY, the PA-5 re-application leaves the ceilings unchanged at 120 s / 300 s, and that **answers the trigger**. No re-measurement is owed now.
2. **Faster host: accepted for TEST_ONLY.** The service ran on an EPYC 9V74, and the Stage 1c harness maximum was measured on an EPYC 7763. Three items are carried to production host sizing (T11/CP-8):
   - k = 4.078929;
   - the host difference;
   - the CPU headroom of 13.142 s (10.95 % of the 120 s ceiling).

   **Confirmed after the normalized result was put to Joshua directly** ("Stands: 120 s, carry 130–160 s"):
   - normalized to the 7763, the CPU ceiling would be 130 s (compute only) to 160 s (whole charge scaled);
   - the ruling keeps the TEST_ONLY ceiling at 120 s on the measured host;
   - the 130–160 s figures are carried to T11/CP-8;
   - a slower runner could hit the 120 s cap.
3. **PA-3b memory headroom: accepted for TEST_ONLY.** The clipped `memory_peak_bytes` reading cannot show m_m headroom. This is consistent with the 2026-09-30 ruling (2), and the item is carried to T11/CP-8.

The T11/CP-8 carries are listed in the [deployment checklist](2026-09-20-tradeify-deployment-checklist.md)'s CP-8 row.

**Next:** #569 is merge-ready once Codex is clean at its head. C3 acceptance goes to Joshua after it merges.

**Not granted:** C3 acceptance, S5 acceptance, any merge, and any production value or budget.

### Coordinator C3 acceptance packet — S5 Part A TEST_ONLY, 2026-10-01

**For the operator's decision.** This entry checks every C3 obligation the ledger names against the record on `main` at `cb5654f`, after #569 merged. The obligations come from the [stage table](#operator-direction--s5-build-entry-separated-from-checkpoint-c3-acceptance-2026-09-27), the CP-1b packet's "C3 obligations stay" list and the "Still open at C3" list of the C3 step-1 entry. It grants nothing by itself.

**Candidate.** `claude/s5-part-a` at **`606e6e0`**. Every execution record below names this head or one whose measured closure it keeps unchanged.

**C3 obligations**

| Obligation | Status | Evidence on `main` |
|---|---|---|
| C3 step 1 (the S5 return, Codex review, executed `bind_budget` Σ check on the built `/v7`) | **Met** | [C3 step 1 accepted](#operator-acceptance--s5-c3-step-1-accepted-c3-linux-grant-2026-09-29) on `c7713e7` and harness `0fe3e25`: Codex RESOLVED; B3 and B4 accepted with carries; B7 closed |
| RC-2 owner-text set, with corrections 3 and 8 | **Met** | Accepted 2026-09-29. #552 merged at `37b590b` and #555 (O-10) at `6c6759f`, both cited ([RC-2 entry](#operator-acceptance-and-coordinator-application--rc-2-owner-text-set-c3-2026-09-29)). The D-2 bridging notes are gone from this plan |
| RC-3b (i): Stage 1c through the built adapter | **Met** | Measure run `36647434808`, jobs a and b exit 0, validity OK, memory VERIFIED; the provisional status is ended ([Stage 1c entry](#coordinator-execution--stage-1c-fresh-approval-valid-memory-verified-2026-09-29)) |
| Stage 1c still binds the final head | **Met** | The closure re-run on `0ab8f6b` found all 68 measured modules byte-identical to `c7713e7`. From `0ab8f6b` to `606e6e0` only `tests/integration/qualification_boundary/test_campaign_part_a_linux.py` and the io-mount card changed (coordinator `git diff --name-only`, 2026-10-01), so the measured closure is unchanged |
| The two S5 build defects from the first diagnostic subset | **Met** | "Fix both, re-verify" (2026-09-30); subsets 3–4 and Windows on the fix head ([re-verification entry](#coordinator-execution--re-verification-after-fix-both-subsets-34-windows-on-the-fix-head-c3-step-1-addendum-2026-09-30)) |
| io-mount release defect (the C3 memory stop) | **Met** | The fix `7c97a69` and card A1–A4. The full S4-plus-Part-A selection, run **36766144433** at `606e6e0`, is GREEN, with 27/27 required nodes and `s2_run_evidence` ok ([entry](#coordinator-execution--io-mount-release-fix-full-s4-plus-part-a-selection-green-2026-09-30)). The archive is first-passage-archive#853, pinned by #568 |
| RC-3b (ii): Stage 2 / PA-5 service-route consistency | **Met (RE-APPLY, ceilings unchanged)** | k = 4.078929 > 1.25, re-applied inside the approved rule; ceilings 120 s CPU / 300 s wall ([Stage 2](#stage-2--pa-5-2026-09-30); `stage2.json`; #569 at `cb5654f`). The evidence is first-passage-archive#854 |
| PA-1's pilot-budget term (1.5 × P̂) and PA-2b | **Met for the applied budgets; one observation carried** | PA-2b holds against the applied B (100 s) and the re-applied B (86.86 s). It fails against the unscaled Stage 1c B (21.29 s), because the service's throttled P is 3.4 × P̂₁c. Recorded as non-governing after re-application and carried to CP-8 below |
| PA-3b memory | **Accepted for TEST_ONLY** | Ruling 2026-10-01 (3): the clipped `memory_peak_bytes` is an upper bound only and m_m headroom is not shown. Carried to T11/CP-8 |
| Re-measurement triggers 5 and 6 | **Answered** | Trigger 5 uses the compute-only CPU (operator, 2026-10-01). Trigger 6 is answered for TEST_ONLY by ruling 2026-10-01 (1) |
| Faster host (EPYC 9V74 against the harness's EPYC 7763) | **Accepted for TEST_ONLY** | Ruling 2026-10-01 (2): "Stands: 120 s, carry 130–160 s" |
| **OQ-1** | **Recommend: close as not arising** | It matters only if no valid Stage 1b record exists. One exists (run `36364854404`, both jobs valid) |
| **Q1**: whether a committed FAIL on an exhausted campaign counts as FALSIFIED under ADR §4 | **Recommend: reassign past C3** | This is campaign semantics, decided with the statistical owner. No TEST_ONLY Part A outcome depends on it. Recommended gate: before the first production statistical dispatch (S8 / T06) |
| **Q7**: R7's production evidence standard | **Recommend: reassign past C3** | This is production evidence, decided with the statistical owner. Recommended gate: before S8 / T06 |
| **Q9**: when a never-retried, retry-eligible IN_DOUBT counts as closed (and so when the salt is revealed) | **Recommend: reassign past C3** | Already recorded as an input to the K3/RC-4 slice and CQ-3 ([host-obligations note §D](../../notes/2026-09-27-host-obligations-assignment.md)). Recommended gate: the RC-4 slice, before F1 |

**Carried, not C3 conditions** (each owner keeps it):
- G5 independent bars verification goes to the CP-6 inventory (B3).
- An independently observed pilot draw is due with T05, before CP-6 (B4).
- The per-phase memory field goes to CP-6.
- To T11/CP-8:
  - the 11.8 % unreclaimable headroom and the THP share;
  - k = 4.078929, the host difference, and the 10.95 % CPU headroom;
  - the 130–160 s normalized ceiling;
  - PA-3b;
  - the PA-2b-against-unscaled-Stage-1c observation, as an input to the production budget.

**The landing step (not covered by any record above).** `claude/s5-part-a` has **no PR**. At the time of writing it is 29 commits ahead of `main` and 188 behind. S5 acceptance means landing it, and T00's merge hold waits on that landing.
- **The evidence binds `606e6e0`, not a merge result.** Any merge into a `main` that has moved produces a new tree that includes `main`'s changes, even when the branch itself is not updated. `--match-head-commit` pins the PR head, not the merged tree. So the landing must re-validate the tree that will actually land.
- **Landing procedure:**
  1. Update `claude/s5-part-a` from `main`. The update commit becomes the landing head **H**.
  2. At **H**, re-run the Stage 1c closure-equivalence check against `c7713e7`, using the same 68-module measured closure and the same method as the recorded check.
  3. At **H**, list every file `main` changed that lies in the import closure of the S5 Linux selection (`tests/integration/qualification_boundary/test_campaign_part_a_linux.py` and the S4 nodes run 36766144433 covered).
  4. At **H**, run the CI required checks, plus the qualification execution-boundary jobs.
  5. Run Codex at **H**, then merge **pinned to H**.
- **Decision rule at H:**
  - If the measured closure is byte-identical and no file in the S5 Linux selection's closure changed, the Stage 1c and run-36766144433 evidence carries to **H**. The landing proceeds on green CI and a clean Codex review.
  - If the measured closure changed, the landing returns to the operator for a Stage 1c re-measure decision.
  - If only the Linux selection's closure changed, a re-run of the full S4-plus-Part-A selection at **H** is required, under the existing C3 Linux grant, with retained evidence, before merge.
  - If `main` moves again before the merge, the update makes a new **H**, and steps 2–5 and this rule apply to it again.
- Codex findings at **H** route to the S5 owner session as single writer.

**Recommended decision, for the operator:**
1. **Accept C3** for S5 Part A **TEST_ONLY** on the evidence at `606e6e0` (the table above). It carries to the landing head only through the decision rule above.
2. **Close OQ-1** as not arising.
3. **Reassign Q1 and Q7** to the statistical owner, before S8 / T06. **Reassign Q9** to the RC-4 slice, before F1.
4. **Accept S5 for TEST_ONLY**, effective when the landing PR merges at a head **H** that satisfies the landing procedure and decision rule above. Then T05 and the T00 rebase follow. The T00 rebase re-runs P7 with a fresh source approval, because the P7 record binds its code head.

**Not granted by this packet or by acceptance:** any production value, budget, ceiling or host sizing; release activation on a non-disposable host; F1; S8 or any statistical dispatch; deployment, arming or live authority. Each still runs through its own gate.

### Operator ruling — C3 accepted; S5 accepted for TEST_ONLY on landing, 2026-10-01

**Source.** Joshua, in the coordinating session at about 17:45Z on 2026-10-01, replying to the four recommendations of the [coordinator C3 acceptance packet](#coordinator-c3-acceptance-packet--s5-part-a-test_only-2026-10-01) (merged in #576 at `2b98d22`): "accept 1–4".

**Effect.**
1. **C3 is ACCEPTED** for S5 Part A **TEST_ONLY**, on the evidence at `claude/s5-part-a@606e6e0` (the packet's table). It carries to the landing head **H** only through the packet's decision rule.
2. **OQ-1 is closed** as not arising. A valid Stage 1b record exists (run `36364854404`).
3. **Q1** (whether a committed FAIL on an exhausted campaign counts under ADR §4) and **Q7** (R7's production evidence standard) are **reassigned to the statistical owner**, to be decided before S8 / T06. **Q9** (closure of a never-retried, retry-eligible IN_DOUBT, and so the salt reveal) is **reassigned to the RC-4 slice**, before F1. None is a C3 condition any longer.
4. **S5 is ACCEPTED for TEST_ONLY**, effective when the `claude/s5-part-a` landing PR merges at a head **H** that satisfies the packet's landing procedure and decision rule. If the measured closure has changed at **H**, the landing returns to the operator, and S5 acceptance does not take effect until he decides.

**Carried items:** unchanged from the packet. They are G5 independent bars verification (CP-6), the independently observed pilot draw (T05, before CP-6), the per-phase memory field (CP-6), and the T11/CP-8 set.

**Next.**
- The coordinator opens the landing PR, updates `claude/s5-part-a` from `main` to **H**, and runs the closure-equivalence and Linux-closure checks at **H**.
- At **H**: CI, then Codex, then a merge pinned to **H**.
- After that, T05 and the T00 rebase. As accepted recommendation 4 states, the rebase re-runs P7 at the rebased head **with a fresh source approval**, whatever the date. The current approval's expiry, 2026-10-08T08:21:08Z, does not relax that. *(Ordering refined in the defects ruling below: P7 is accepted at the head T00 actually merges at.)*

**Not granted:** any production value, budget, ceiling or host sizing; release activation on a non-disposable host; F1; S8 or any statistical dispatch; deployment, arming or live authority.

### Operator ruling — land S5 with two named TEST_ONLY defects; fix before T05, 2026-10-01

**Source.** Codex reviewed the landing PR #578 at **H = `1fe99fa`** and raised two P2 code findings. Both were already present at `606e6e0`; the merge of `main` did not introduce them. Put to the operator by structured question, Joshua chose "Land now, fix before T05".

**The two named defects (TEST_ONLY, open):**
- **D-S5-1, Part A output mount sizing** (`ops/c1_rail/qualification/execution/campaign_supervisor.py`, the checkpoint io mount sized from the per-file `profile.output_byte_limit`; Codex thread 4158727147). A PART_A work's output tmpfs holds `part-a-initial.jsonl`, `part-a-final.jsonl` and `result.frame` at once. Each can be within its own limit while the total exceeds the mount, so a large valid result can hit ENOSPC and end IN_DOUBT. This **fails closed**: no wrong result can be accepted.
- **D-S5-2, Part A capture idempotency** (`ops/c1_rail/qualification/execution/campaign_store.py`, `retain_checkpoint_capture`; Codex thread 4158727154). The exact-retry check compares only the result and payload bytes. A retry with the same result, payload and transition bytes but different capture fields passes, and the family projection then overwrites `initial_prefix_sha256`, `final_sha256`, the panel counts and the expansion fact. This breaks the exact-retry contract.

**Effect.**
- **This replaces, for D-S5-1 and D-S5-2 only, the clean-Codex-review condition of the C3 landing procedure.** For the C3 ruling's item 4 (S5 acceptance), "Codex clean at H" means no Codex finding at H other than these two.
- **S5 acceptance for TEST_ONLY takes effect when #578 merges at `1fe99fa`** with the procedure otherwise met: the Linux run `36902447502` reads ok at H, CI is green, and Codex raises no other finding at H. It does not wait for the fix slice. The fix slice is a separate gate on T05, not a condition of S5 acceptance.
- #578 may merge at `1fe99fa` with these two P2 threads open, which overrides the merge train's no-open-P2 gate for these two only. **#578 lands before this ledger entry merges.** If anything else moves `main` past `2b98d22` first, including this entry, the packet's main-movement rule applies: a new H, with steps 2–5 again. It still needs the Linux run `36902447502` to read ok at H, green CI, and no further Codex finding at H.
- The follow-up fix slice (#586, for D-S5-1/D-S5-2) gets fail-first tests for each defect *(D-S5-3 adds a second, separate slice with its own run and acceptance; see the D-S5-3 ruling below)*, and **must merge before T05 integration acceptance** (checkpoint R1 in the deployment checklist's result/seal row; T05 is already built and frozen at `6cf2732`). T05 integration *preparation* (H9) may proceed meanwhile, but its integration branch is rebuilt on a `main` that includes the fix before R1. *(This names the event the operator's "fix before T05" gates.)* The fixes are outside the 68-module measured closure (`campaign_supervisor` and `campaign_store` are not in it). They are inside the Linux selection's closure, so the fix needs its own full S4-plus-Part-A Linux run.

- **T00 P7 ordering.** The P7 record binds its code head, so T00's P7 is re-run, freshly approved and accepted **at the head T00 actually merges at**. If `main` moves before T00 merges, for example by the D-S5 fix slice landing, that P7 run is repeated at the new head with a fresh approval. **Recommended order:** #578, then the D-S5 fix slice (#586), then the D-S5-3 fix, then the T00 rebase, P7 re-run, fresh approval and merge. That way P7 runs once. *(D-S5-3 added 2026-10-01; see the D-S5-3 ruling below.)*

**Not granted:** T05 integration acceptance (R1) before the fix lands, and no production use. Everything else in the C3 ruling above stands.

### Operator ruling — D-S5-3 (capture exact-retry demotion) also gates T05 R1, 2026-10-01

**Source.** Joshua, in the coordinating session on 2026-10-01: "yes, D-S5-3 gates R1 too".

**The defect, D-S5-3** (latent; found by the D-S5 fix-slice worker). In `ops/c1_rail/qualification/execution/campaign_store.py`, an *exact* `retain_checkpoint_capture` retry rewrites the checkpoint's family row as CAPTURED. Once the family has moved on, that demotes ATTESTED and COMMITTED rows and drops their attestation and receipt digests. It affects N1, N2 and PART_A. Today it is unreachable, because the only caller captures once per worker run. The fix makes an exact retry return without writing once all of its checks pass. It is held on a separate branch, `claude/capture-retry-noop`, to be opened after #586 merges. *(#586 merged at `981eb12`; the fix was opened as #589.)*

**Effect.**
- **D-S5-3 gates T05 integration acceptance (checkpoint R1)**, in the same way D-S5-1 and D-S5-2 do. Its fix must merge with **its own full S4-plus-Part-A Linux run read ok**, plus its own acceptance, because it changes N1/N2 store behavior. The T05 integration branch is rebuilt on a `main` that includes it.
- S5 TEST_ONLY acceptance is unaffected; it is already in effect.
- **Acceptance contract for the D-S5-3 slice.**
  - **Tested revision:** the branch is updated from `main` **after #586 merges**, so that it contains both fixes. Its full S4-plus-Part-A Linux run, its closure check and its acceptance are all bound to that updated head. D-S5-2 and D-S5-3 both modify `retain_checkpoint_capture`, and this run is the combined fixes' only full Linux run, because H9 R1 runs only the result/seal node set.
  - **Targeted regression:** a full Linux run cannot exercise an exact retry, because production captures once per worker run. So a **fail-first, store-level test** is a prerequisite of acceptance. It covers an exact retry after the family has progressed, for N1, N2 and PART_A. It shows ATTESTED and COMMITTED state, and the attestation and receipt digests, preserved with no write. Cite its red record on the unfixed code and its green record on the fixed code.
- The clean-review exception in the defects ruling above covers D-S5-1 and D-S5-2 only.

**Not granted:** T05 integration acceptance (R1) before the D-S5-3 fix lands, and no production use.

### Operator rulings — T05 environment sealing (C′) and the first-release host environment drift residual, 2026-10-02

*Joshua, directly in the coordinating session, on 2026-10-02. These rulings are owned here. H9 checkpoint R1 ([staged acceptance](../../briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md)) and the deployment checklist's T05 row link to this entry and carry it as an R1 gate.*

**Rulings, in order:**
1. **"scoping is fine, defer the sealing to T05".** T00's P7 `code_closure_sha256` identifies the Python-source closure plus the recorded interpreter binding. Environment sealing is owed by T05 before the R1 grant.
2. **"C for the T05 sealing"**, revised to **C′** after the H9 source check found that host-side code decides outcomes. That host-side code includes Part-A adjudication, calendar and deadline logic in Eastern time, budget exhaustion, VOID, and aggregate result and seal checks.
3. **"yes"** to the coordinator's narrowed C′. Identity checks cover only the finite, known R1 host entrypoints. Unmediated descendants and OS helpers join the residual.

**C′ obligation, owed by T05 before the R1 grant. It is a design: no build is dispatched by this entry.**
- **Worker base image.** It must be a **standing, operator-approved digest**, not a tag resolved at build time. A missing, tag-only or mismatched pin refuses. The initial digest and any later update need Joshua's approval and a reviewed change.
- **Host identity checks.** A signed release/runtime revision binds a finite mapping of the known R1 host entrypoints:
  - the runner/pytest admin fixture;
  - the service supervisor;
  - the campaign guardian, control and probes;
  - the N1, N2, PART_A and RESULT G5 roles;
  - qseal;
  - the Python bootstrap/owned-command wrapper.

  Each mapped launch is checked before it spawns, by the child itself, and by the controller through `/proc`. Each is rechecked at the checkpoint, result and seal authority transitions, and at **every VALID→VOID transition** (campaign spec :90 makes VOID its own irreversible authority transition). The checkpoint, result and seal rechecks run inside the original CPU/wall reservation and absolute deadline, with no refresh or retry. **The VOID recheck is uncharged.** It does not depend on remaining allowance or the deadline, matching the accepted uncharged VOID path (`claim_void_authentication`, sequence 0), so VOID stays possible for campaigns in BUDGET_UNCERTAIN, IN_DOUBT or past their deadline. A VOID recheck mismatch refuses an *automatic* VOID commit and leaves the campaign for the operator-recorded VOID path, which records the mismatch. It never leaves the campaign with authority to PASS.
- **Evidence and failures.** Launch and exit evidence is retained in versioned supervision events. **So is every transition-time recheck**: its expected identity, observed identity, transition and verdict, so that R1 can verify coverage. A mismatch, a failed check, a timeout or exhaustion refuses authority.
- **Unchanged.** Frozen v1 RESULT/SEAL and the DB10 two-table layout stay as they are, bound through the existing `release_sha256`. The design term is proposed as term 7 of the S6 DB10 draft, which stays DRAFT.

**Residual accepted by Joshua for the first release: "T05 C′ first-release host environment drift."**
- **Not covered by the checks:** an unchanged interpreter and lock identity does not seal installed distribution contents, tzdata or other data files, external mounts, late-loaded native or transitive libraries, or OS and kernel services. **Unmediated descendant processes and OS helper binaries (systemctl, busctl, docker), and OS daemons and the kernel, are not identity-covered either.**
- **Effect:** drift in any of these can change adjudication, calendar, deadline and VOID outcomes.
- **Size:** its magnitude is **unmeasured**.
- **No hermeticity claim** is made. Every R1 packet cites this residual, the expected identity contract and the observed coverage.

**Unchanged:**
- Full S5 custody.
- R1's Linux node set as its owner defines it (H9 checkpoint R1), under its own express grant. This entry does not change that set.
- Independent review.
- T00-first integration.
- Three qualification-path items still owed before R1:
  - truncated-calendar validation;
  - calendar-role binding;
  - reviewer identity and independence.
