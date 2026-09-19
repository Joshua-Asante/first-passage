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

Current authoritative workspace: `C:/Users/joshu/.codex/worktrees/full-e1-recovery/multi_firm_operations`. It is detached at that merge **with exactly recovered accepted Task 1a/1b source changes**. The original worktree is no longer present. The checksummed recovery snapshot and fresh verification records are indexed in [the recovery packet](C:/Users/joshu/multi_firm_operations/recovery/full-e1-20260919/README.md). Checking out the merge alone loses those changes. Do not start a future agent on that bare merge and describe it as the accepted successor.

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
3. **Reservations cover the rest of the route.** Canonical installed configuration names admission, checkpoint/source proof/probe, capture/attestation, each G5 assessment, aggregate validation/commit and sealing/finalization ceilings. Validate feasibility against the frozen cap, including prescribed maximum expansion. Actual CPU counters settle reservations once; unknown usage consumes its full reservation. Remaining wall time includes queues and downtime. Memory is an enforced shared concurrent footprint, not independent full-size allowances per process.
4. **Staged development does not change admitted releases.** Before all stages exist, test signed diagnostic releases can expose only implemented checkpoints; reaching the end of their allowed prefix stops without final PASS or seal. A later code/profile revision uses a fresh attempt. Final acceptance uses a release enabling all three compute checkpoints and the complete G5/result/seal route.
5. **Snapshots and transport have one owner.** Extend `qualification/journal_snapshot.py`, `qualification/checkpoint_plan.py`, policy/evidence owners and existing versioned campaign protocol. Plans remain non-authoritative inputs; the service's recorded dispatch intent authorizes work. Keep 1 MiB bounded chunks and explicit total-size limits. G5 needs authenticated access to retained inputs/captures and private candidate staging; a digest with no authorized producer/fetch route is not an interface.
6. **Signing recovery is durable.** Fixed payload, key, signing time and intent identity precede signing. Recover exact signed candidate/receipt on retry. Missing capture never licenses another draw; missing deterministic G5 validation may be repeated only under the original remaining budget. VOID/expiry/revocation bar new authority while exact historical receipts remain inspectable with current validity.

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

**Behavior:** Worker and G5 independently derive the same N2 FULL pass rate from captured outcomes. Preserve the disjoint Part A pilot addresses, outer panel seeds, path addresses and source occurrence order, including legitimate duplicate occurrences. Retain the exact original prefix before extending indices `[initial_panels, expanded_panels)`; the final prefix must be byte-identical. Conditional expansion uses inclusive tolerance equality. Apply the final floor and FULL sanity comparison after required expansion. A crash during panels without complete durable capture is IN_DOUBT: no panel resume, replacement pilot or checkpoint rerun.

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
