# Protected Full E1 Campaign Implementation Plan

> **Remaining-work delegation:** [Full E1 execution slices](2026-09-18-full-e1-execution-slices.md) now owns the bounded S1-S8 decomposition after accepted Task 1a/1b. This document retains the original roadmap and acceptance history. Use the new plan plus the governing specification for future assignments; do not run the older broad Tasks 2-6 as unrestricted handoffs.

> **For agentic workers:** Execute with superpowers:executing-plans; use superpowers:subagent-driven-development when bounded delegation is useful and authorized. Preserve the behavioral contract and integration owner. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete the protected synthetic E1 route through genuine N1, joint N2/Part B, Part A, independent G5, atomic result commit and separate sealing.

**Architecture:** Extend accepted PR425's service-owned N1 execution boundary, canonical policy/evidence interfaces and store with the combined foundation incorporated in PR425. Reuse the statistical engine through store-free compute adapters; persist campaign state, budget, captures and idempotent authority receipts. One coordinating implementer owns integration and revision-bound Linux acceptance.

**Tech Stack:** Existing operations Python/launcher, SQLite transactions, canonical JSON and enrolled signatures, Linux Unix peer credentials, Docker workers, Linux cgroup accounting, disposable Ubuntu verification harness.

**Spec:** [Protected full E1 campaign successor specification](../specs/2026-09-17-protected-full-e1-campaign.md). Read both files before execution.

## Global Constraints

- FULL_E1 initially has `authority_class=TEST_ONLY` and `production_execution=false`.
- N1 prerequisite satisfied at PR425 merge `1e4928360b95812b04725dc1e8da97709d670ff4`; full-E1 acceptance still requires specification §6.
- Direct CrossTrade → Tradovate remains the intended broker route.
- No in-place continuation of an N1_ONLY attempt into FULL_E1.
- All depths, thresholds, namespaces and budgets come from the frozen contract, not copied constants.
- Part A remains one dispatched compute operation using the existing append loop.
- The execution service verifies both and owns publication receipts.
- Administrator and Docker-privileged qexec are trusted; distinct UIDs do not confine malicious qexec.
- Preserve unrelated working-tree changes. Use the isolated checkout at PR425 merge `1e4928360b95812b04725dc1e8da97709d670ff4` for these documents and implementation.
- Run the checkout's `./fp.ps1 doctor` before project Python work, then `./fp.ps1 python -m pytest ...`; on Linux use `python -I scripts/fp.py doctor` and `python -I scripts/fp.py python ...`. Never bypass launcher validation.

## Starting points and acceptance discipline

The accepted baseline is PR425 merge `1e4928360b95812b04725dc1e8da97709d670ff4`. PR415 was closed without merging; PR425 includes its foundation as part of the combined implementation. Specification §0 records final head `63a92fd31753c0770e998975f87187f9c92f6505`, successful two-host 464-case boundary verification, successful final hosted pytest and independent review. The foundation prerequisite is satisfied.

Work in `C:/Users/joshu/.codex/worktrees/full-e1-spec-baseline/multi_firm_operations`, initially clean and detached at that merge. Do not use the old mutable structural-closure checkout. Canonical interfaces, the lifecycle model and `tests/ops/qualification/invariant_manifest.json` exist at this baseline. New names below are proposed successor interfaces. N1 remains N1_ONLY/TEST_ONLY; full-campaign or production authority is not inherited.

Former PR425 stop-readiness/OOM/lifecycle/concurrency/invariant/review blockers are closed by later accepted evidence. Preserve their regressions rather than assigning historical repairs to this successor. The coordinator evaluates any new finding on its evidence and scope.

This is the full roadmap. Corrected Task 1a is accepted at the exact local state recorded below; its earlier conflict and pending-review entries are historical. Task 1b durable admission without dispatch has now reached its accepted return boundary, under docs/briefs/handoffs/2026-09-18-full-e1-task1b-durable-admission.md. Task 2 durable lifetime budget/recovery is the next roadmap outcome; it has not been implemented or accepted. Task 1 remains the combined admission outcome. Combined acceptance remains with the coordinator.

Each task follows a failing-test/minimal-change/passing-test cycle and ends in a focused commit after its checks. Use fixture-driven tests for contracts and real-host tests for OS/process guarantees. Pure unit mocks are never the acceptance producer for actual execution, resource counters or Linux isolation. No broker work is required here.

## Successor interface map

Keep canonical JSON bytes at the external boundary. Define transport schemas/strict parsers in proposed `execution/campaign_protocol.py`. Extend existing `qualification/checkpoint_plan.py` for pure campaign/checkpoint plan derivation; `execution/plan.py` remains an active adapter. Extend `qualification/policy.py`/`policy_sources.py`, `qualification/evidence.py` and `qualification/journal_snapshot.py` for their existing policy, artifact and snapshot responsibilities. Do not introduce a parallel campaign-plan, output-role or snapshot authority. Reject unknown fields, bool-as-int values, excessive sizes/depth, wrong domains and noncanonical bytes using accepted N1 helpers.

```python
# Proposed shared functions in qualification/checkpoint_plan.py.
def derive_campaign_plan(contract, *, policy, execution_release_sha256: str,
                         source_bundle_sha256: str, attempt_id: str,
                         exact_depth_approval_sha256: str) -> bytes: ...
def derive_checkpoint_plan(campaign_plan: bytes, checkpoint: str,
                           predecessor_receipt: bytes | None) -> bytes: ...
# Proposed transport parsers in execution/campaign_protocol.py.
def parse_campaign_request(raw: bytes) -> dict: ...
def parse_campaign_result(raw: bytes) -> dict: ...
```

`campaign_plan` binds the admitted contract/domain/release/source/budget identities and ordered N1/N2/PART_A inventories, retaining Part A's potential expanded seed inventory separately from actually executed paths. `checkpoint_plan` binds its predecessor assessment receipt; worker and G5 independently derive it through the same canonical pure owner. The request supplies only `operation`, `attempt_id`, `bundle_sha256`, `request_id`; installed admission obtains all authoritative identities. The execution adapter consumes `ExecutionContext` from `verify_bundle` and supplies its contract, canonical policy, installed release digest, retained bundle digest and exact-depth approval to the pure producer above. Each consumer verifies those bindings; no client-supplied policy or source digest overrides the context.

Proposed operation field sets (all include `operation` and `attempt_id`): SUBMIT_E1 adds `bundle_sha256, request_id`; STATUS and SNAPSHOT add nothing; FETCH adds `object_sha256`; STORE_ARTIFACT adds `role, bytes_b64`; STORE_RESULT adds `envelope_bytes_b64`; COMMIT_CHECKPOINT_ASSESSMENT adds `checkpoint, envelope_sha256, authentication_bytes_b64, expected_revision`; COMMIT_E1_RESULT adds `envelope_sha256, authentication_bytes_b64, expected_revision`; VOID adds `reason, approval_bytes_b64`. FETCH is restricted to published membership for clients; G5 may fetch its private candidates. Seal work is service-to-qseal IPC, not a client operation: `SIGN_COMMITTED_PASS` carries `intent_bytes_b64, result_bytes_b64, authentication_bytes_b64, result_receipt_bytes_b64`; every field is verified against the intent and current locked campaign. COMMIT_E1_SEAL is a private service action taking that exact intent and signature, not an exposed signer publication endpoint. Use new versioned parsers for these full-campaign requests; existing N1 field sets stay unchanged.

Client operations: SUBMIT_E1, STATUS, FETCH. G5 operations: assessment snapshot/fetch, private candidate staging, COMMIT_CHECKPOINT_ASSESSMENT and COMMIT_E1_RESULT. Seal role receives only committed-PASS lookup and exact service-created seal intents; service owns COMMIT_E1_SEAL. Operator retains VOID. No client advance, complete-checkpoint, seed, result-upload or generic launch operation.

The public API uses authenticated role transport; private store methods never accept a caller's object as proof. The service verifies signatures/canonical artifacts before entering transaction methods; those methods repeat revision/validity/membership/budget checks under the same lock as VOID.

## Task 1: Admit immutable FULL_E1 campaigns from the accepted baseline

### Bounded execution sizing

Task 1 is split into two coordinator-selected checkpoints. [Task 1a handoff](../../briefs/handoffs/2026-09-18-full-e1-task1a-canonical-plan.md) implements the pure canonical FULL_E1 planning producer/validator and verified-context adapter only. Its planning artifact grants no authority, and all N1_ONLY release/service restrictions remain unchanged. Task 1b later implements versioned release/protocol support and durable service admission/status/invalidation without dispatch. Task 1a completion does not complete Task 1. The narrower handoff controls its authorized footprint and return boundary; the broader Task 1 contract below describes the combined admission outcome.

Task 1a adds `validate_campaign_plan(...) -> dict` beside `derive_campaign_plan(...) -> bytes` in the existing canonical owner, and `derive_campaign_plan_from_context(context) -> bytes` in the existing execution adapter. It does not implement `derive_checkpoint_plan`, campaign request/result parsers or activate any endpoint. These Task 1a functions are now implemented locally; see the resumed progress entry for signatures, evidence and limits.

### Task 1a progress — 2026-09-18: returned on scope conflict

**Status:** NOT IMPLEMENTED / NOT ACCEPTED. The Task 1a implementation handoff was selected, but its explicit conflict-return boundary was reached during prerequisite inspection, before production or test edits. Task 1 and full E1 remain incomplete. The following entry supersedes the earlier documentation-only description of the current assignment; it does not change the governing specification.

**Workspace/base:** `C:/Users/joshu/.codex/worktrees/full-e1-spec-baseline/multi_firm_operations`, detached HEAD `1e4928360b95812b04725dc1e8da97709d670ff4`. Initial tracked diff empty; the handoff, this roadmap and the successor specification were the three intentional untracked files. Only this roadmap was edited in this attempt; no commit, push, PR, service hookup or authority change.

**Blocking conflict:** the handoff requires a zero-appended-range positive case when `expanded_panels == initial_panels`, with planning derived from verified frozen inputs. Canonical `QualificationWorkloadPolicy.__post_init__` in `ops/c1_rail/qualification/trust_domain.py:84` rejects duplicate depth values, and line 93 requires expanded panels to strictly exceed initial panels. Line 94 binds PART_A/REGIME to that pair. `verify_bundle` reconstructs this workload before domain/contract admission. Consequently an equal-count signed bundle cannot produce the required verified context. The lower-level Part A engine supports equality, but that does not establish accepted frozen-input support. Bypassing validation or mutating an admitted object would not satisfy the handoff.

**Coordinator decision required:** either revise Task 1a to test equality as an unsupported frozen configuration (retaining current accepted policy), or issue a separately scoped change to the canonical workload/admission rules and their regressions before requiring equality as a positive campaign-plan case. The latter needs `trust_domain.py` outside Task 1a's allowed footprint; no such change was made. This is a requirement/scope conflict, not a newly claimed PR425 defect.

**Reproduction:** after launcher doctor, a temporary signed `build_bundle` fixture was reconstructed with `verify_bundle(..., NOW)`; authority was TEST_ONLY, initial/expanded panels were 2/4. Direct validator construction with `dataclasses.replace(workload, part_a_expanded_panels=workload.part_a_initial_panels)` rejected with `expanded panels must exceed initial panels`. Also setting a copied `stage_population_depths['PART_A']['REGIME']` to `(2, 2)` rejected with `sorted unique workload depths required`. Both expected exceptions were asserted; the launcher command exited 0. These were direct validator rejection checks, not altered admitted-context evidence. Fixture files were temporary and removed automatically.

The reproduction ran through `./fp.ps1 python -c <probe>` with `ops`, `tests/ops/qualification`, and `tests/ops/qualification/execution` added to `sys.path`. The probe imported `build_bundle`, `NOW`, `verify_bundle`, `dataclasses.replace`, `TemporaryDirectory` and `Path`; verified the fixture before the two validator calls above. Two earlier probe setup attempts failed (missing import path, then a `None` production default workload); neither is acceptance evidence. The final probe used the actual signed fixture workload. Direct `python -c` commands do not produce pytest verification records.

**Verification:**

- `./fp.ps1 doctor`: exit 0; Python `C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`, version 3.13.2; 62 locked packages matched; optional signing dependency 50.0.1.
- `./fp.ps1 --workers 2 python -m pytest tests/ops/qualification/execution/test_bundle.py tests/ops/qualification/execution/test_release.py tests/ops/qualification/execution/test_protocol.py tests/ops/qualification/test_checkpoint_validation.py tests/ops/qualification/test_seed_probability_vectors.py tests/ops/qualification/test_semantic_policy.py -q --tb=short`: **173 passed**, zero failures/errors/skips, pytest duration 37.36 seconds. Recorder: `.cache/fp-verification/20260918T235615Z-3be64adfa903/record.json`; inspected status completed, exit_code 0, verification_exit_code 0, source_stable true, capture_complete true, empty capture/report errors, valid JUnit counts. Tested tracked source is the unchanged merge above; this progress entry was added after recording completed.
- No new campaign test suite or producer/consumer was added; no red/green implementation cycle is claimed. `./fp.ps1 check` and Linux/full-route verification were not run because the conflict-return checkpoint was reached before implementation. Selected baseline regressions passing does not mean all gates passed.

**Canonical ownership and interfaces:** `checkpoint_plan.py` remains the pure N1 owner and `execution/plan.py` its active adapter. Proposed `derive_campaign_plan`, `validate_campaign_plan`, `derive_campaign_plan_from_context` and `qualification_campaign_plan/v1` remain unimplemented. Read-only mechanics inspection confirmed the shared N1/N2 probe address (`probe`, FULL, panel None, path 0, purpose path) and Part A's two probe addresses (panel 0, paths 0/1, purpose probe); future inventories must preserve these semantics. No seed inventory representation/size acceptance is claimed.

**Remaining Task 1b obligations:** versioned FULL_E1 release admission, closed SUBMIT_E1 protocol, service-owned durable identity/receipt, duplicate/conflict handling, status and invalidation without worker launch. Budget lifecycle, dispatch/restart, G5 continuation, results and seals remain subsequent work. Existing N1_ONLY attempts gain no migration or dispatch authority. Return to the coordinator at this conflict checkpoint; do not advance to Task 1b or Task 2.
### Combined Task 1 outcome

**Selected outcome:** a registered FULL_E1 TEST_ONLY bundle yields one durable campaign identity and canonical plan; N1_ONLY history remains readable and cannot be promoted. No replay dispatch is added.
**Prerequisites:** satisfied N1 foundation at merge `1e4928360b95812b04725dc1e8da97709d670ff4`, with §0 final-head Linux/pytest/review evidence and existing canonical policy/plan/evidence/snapshot/invariant owners. New FULL_E1 schemas remain implementation work.
**Ownership:** the selected implementation executor delivers Task 1; the coordinating full-E1 agent accepts it and retains combined acceptance. This documentation amendment starts no implementation executor.
**Verification:** checkout launcher doctor, campaign protocol/plan tests and accepted N1 protocol/plan/release regressions. Retain exact revision/working-tree identity, command, interpreter and results. Demonstrate identical-request reuse, conflicting-request rejection, canonical identity binding and zero admission-time worker launches.
**Checkpoint:** report verified admission/plan delivery or a blocking interface/scope finding to the coordinator; record evidence and unresolved issues in this task's implementation progress entry before returning.
**Return boundary:** return after Task 1's reviewable changes and checks, or on an unresolved prerequisite/scope conflict. Exclude Task 2 budgets, N2/Part A dispatch, G5 continuation, sealing, PR425 repairs, push/PR/merge and production activity. Each follow-on outcome requires coordinator selection.

**Files:** Modify `execution/release_schema.py`, `execution/admission.py`, `execution/protocol.py`, `execution/service.py`, `execution/store.py`, `execution/runtime.py`, `execution/plan.py`, `qualification/checkpoint_plan.py`, `qualification/policy.py`, `qualification/policy_sources.py`, and `qualification_cli.py` under `ops/c1_rail/` (execution paths are under `qualification/`). Create `ops/c1_rail/qualification/execution/campaign_protocol.py`, `tests/ops/qualification/execution/test_campaign_protocol.py`, `test_campaign_plan.py`. Extend the accepted release/fixture builders in `tests/ops/qualification/execution/` after locating their actual paths at the accepted revision.

**Contract:** integration owner verifies N1 evidence before code changes. Admission owns immutable configuration; store owns uniqueness. An identical admission request returns the existing campaign; changed bundle under the same attempt rejects. Closed N1 schemas retain their original interpretation.

**Consumes:** accepted N1 `verify_bundle`, canonical JSON/digest helpers and peer-role transport. **Produces:** the four interfaces above; a versioned FULL_E1 release and campaign schema bound to canonical profile/budget identities.

- [ ] Record the merge and §0 Linux/pytest/review evidence; verify canonical files and manifest in this isolated checkout. PR415 has no separate merge prerequisite. Run this checkout's doctor and inspect existing changes before editing. Preserve source/configuration identity in the implementation evidence; report new mismatches to the coordinator instead of switching baselines.

- [ ] Add parser/plan tests, including a pure closed-request test:

```python
import pytest
from c1_rail.qualification.execution.campaign_protocol import parse_campaign_request
from c1_rail.qualification.contract import canonical_json_bytes

def test_client_cannot_supply_outcomes():
    raw = canonical_json_bytes(dict(operation='SUBMIT_E1', attempt_id='synthetic-e1',
        bundle_sha256='a'*64, request_id='request-1', outcomes=[]))
    with pytest.raises(ValueError):
        parse_campaign_request(raw)
```

- [ ] Run `./fp.ps1 python -m pytest tests/ops/qualification/execution/test_campaign_protocol.py tests/ops/qualification/execution/test_campaign_plan.py -q`; first observe the intended missing successor capability, then implement schemas, role ACLs and plan derivation. Add frozen-contract fixture cases asserting joint N2 population counts and deterministic Part A seed-prefix identities.
- [ ] Define unique `(attempt_id, checkpoint)` storage and immutable campaign binding. Store admitted request bytes before replying; reject same identity/different bundle and N1_ONLY migration. Serialize request handling through existing service transactions.
- [ ] Re-run selected tests plus accepted N1 protocol/plan/release tests; record outcomes and commit this behavior.

**Acceptance:** E07/E09/E11 schema and identity cases; no worker launch during rejected admission. Return to the coordinator before selecting Task 2; historical active-worktree hashes are not the implementation baseline.

## Task 2: Preserve one budget and no-redraw recovery across process lifetimes

**Outcome:** a process crash cannot replenish CPU/wall budget or repeat a started checkpoint; captured work remains recoverable.

**Files:** Create `ops/c1_rail/qualification/execution/campaign_budget.py`, `campaign_store.py`, `tests/ops/qualification/execution/test_campaign_budget.py`, `test_campaign_recovery.py`. Modify `execution/store.py`, `service.py`, `launcher.py`, `budget.py`, `profile.py`, `qualification/journal_snapshot.py`, the accepted SQL-free `tests/ops/qualification/execution/lifecycle_model.py` and existing instance/profile fixtures. Store schema migration must preserve historical N1 tables/receipts; new full campaigns use separate versioned tables within the same validity/transaction authority.

**Consumes:** Task 1 admitted campaign/plan. **Produces:**

```python
# campaign_budget.py: observed values come only from the protected supervisor.
def remaining_cpu(cap_ns: int, charges_ns: tuple[int, ...],
                  reservations_ns: tuple[int, ...]) -> int:
    return cap_ns - sum(charges_ns) - sum(reservations_ns)

# campaign_store.py methods on proposed CampaignStore wrapping the existing DB:
# admit(plan_bytes: bytes, request_bytes: bytes, clock_bytes: bytes) -> bytes
# reserve_work(attempt_id: str, work_id: str, limits_bytes: bytes,
#              *, expected_revision: int) -> bytes
# settle_work(attempt_id: str, work_id: str, observations_bytes: bytes) -> bytes
# recover(attempt_id: str, observations_bytes: bytes) -> bytes
# snapshot(attempt_id: str) -> bytes
```

`clock_bytes` includes boot ID, BOOTTIME start/deadline and audit UTC. `limits_bytes` binds phase ceilings to the canonical profile. Work ID is unique for compute, capture, each G5 assessment and final seal phase. `observations_bytes` contains supervisor-authenticated cgroup/process identity, CPU usage, peak/OOM and lifecycle facts. It is not a wire operation available to clients/workers. Persist counter settlements once; unknown counters consume their reservation. `snapshot` exposes immutable identity, progression, validity, revision/head and budget state through versioned extensions of `qualification/journal_snapshot.py`, excluding secret configuration; the store does not define its own competing snapshot format.

- [ ] Write accounting/recovery tests before implementation. Minimal arithmetic invariant:

```python
from c1_rail.qualification.execution.campaign_budget import remaining_cpu

def test_outstanding_reservation_cannot_be_spent_again():
    assert remaining_cpu(100, (20,), (60,)) == 20
    # Unknown usage after crash settles at the full reserved ceiling.
    assert remaining_cpu(100, (20, 60), ()) == 20
```

- [ ] Run `./fp.ps1 python -m pytest tests/ops/qualification/execution/test_campaign_budget.py tests/ops/qualification/execution/test_campaign_recovery.py -q` and observe failures for unimplemented durable transitions. Add DB reopen tests for same-boot deadline retention, changed boot rejection, exactly-once settlement and duplicate reservation conflict.
- [ ] Implement transactional admission/reservation/settlement plus inherited dispatch states. Recovery classification is literal:

```text
RESERVED without START_INTENT -> same reservation, if still eligible
START_INTENT/RUNNING without durable capture -> IN_DOUBT, then cleanup
CAPTURED -> validation/attestation of saved bytes only
ATTESTED -> G5 using remaining budget
committed assessment -> next not-started checkpoint only
terminal/VOID/uncertain clock -> historical access only
```

- [ ] Add supervisor resource attribution: campaign cgroup/process ownership, cumulative CPU measurement including descendants, total concurrent memory enforcement, deadline enforcement, and bounded work processes for G5/finalization. Persist reservations before creating work; retain counters before cleanup. Account CPU overrun as terminal even if sampling notices it after the cap. Keep status/fetch operational when cleanup or signing fails.
- [ ] Re-run targeted tests and accepted N1 recovery tests. Record local model-test limits; Linux enforcement remains owed in Task 6. Commit after passing local checks.

**Acceptance:** E06/E08/E12 models now; actual process/cgroup and hard-kill evidence in Task 6. No per-stage fresh `BudgetGuard.from_contract()` can become the campaign authority.

## Task 3: Execute joint N2 and Part A through the protected worker

**Outcome:** genuine synthetic campaign computation follows the frozen stage sequence, with one N2 batch and prefix-preserving conditional Part A expansion.

**Files:** Modify `execution/compute.py`, `worker.py`, `evidence.py`, `plan.py`, `service.py`, and canonical `qualification/checkpoint_plan.py`. Create `execution/campaign_compute.py`, `tests/ops/qualification/execution/test_campaign_compute.py`, `test_campaign_evidence.py`. Reuse `runner.py`, `provider.py`, `replay.py`, `regime.py`, `part_a.py`, `seed_identity.py`; change engine internals only if explicit parity investigation proves a necessary extraction. Worker-capture encoding remains distinct from canonical qualification artifact reconstruction in Task 4.

**Consumes:** Task 2 work reservation and Task 1 derived checkpoint plan. **Produces:**

```python
# campaign_compute.py
# budget follows accepted BudgetGuard.check_and_measure/remaining_wall_seconds.
def run_joint_n2_compute(contract, source, budget): ...  # existing StageRun

def run_part_a_compute(contract, source, budget,
                       n2_capture_bytes: bytes): ...  # existing PartAResult

# evidence.py extensions
# encode_campaign_worker_result(context, execution_id: str, plan_bytes: bytes,
#                               result, observations: dict) -> bytes
# parse_campaign_worker_result(raw: bytes, *, context, execution_id: str,
#                              plan_bytes: bytes) -> dict
```

Use the N1 adapter pattern: source.verify_for, budget-wrapped source.replay, `_ReplayProvider`, `stage_request(contract, 'n2', remaining)`, `_run_stage`. For Part A extract the request/proof-provider composition from `ProductionExecutor.run_part_a` into a store-free adapter and call `_run_part_a`; worker reconstructs FULL pass rate from the preceding captured N2 result. No legacy store/executor object crosses into compute.

- [ ] Add red compute tests using actual synthetic source/replay fixture producers from accepted N1. For both n1/n2, compare protected adapter outcomes and seed inventories to existing pure mechanics at identical frozen input. Add conditional expansion and boundary parity assertions using exact rates with the accepted contract fixture, not hand-selected outcome-only positive campaigns.
- [ ] Run `./fp.ps1 python -m pytest tests/ops/qualification/execution/test_campaign_compute.py tests/ops/qualification/execution/test_campaign_evidence.py -q`; record expected missing adapters/schema failures.
- [ ] Implement the adapters and strict output encoding. N2 encoding retains FULL/H1/H2 together; Part A encoding retains source occurrences and initial-prefix artifact plus full panel-major inventory. Capture manifest includes pilot usage and budget identity but never treats pilot trials as final stage trials.
- [ ] Derive both worker and service plans independently; dispatch only from committed predecessor PASS assessment. Add rejection tests for PART_B as a requested checkpoint, caller seeds, extra path, missing half-population, altered panel prefix, wrong n2 FULL dependency and invalid panel counts.
- [ ] Re-run parity/evidence tests and accepted N1 compute tests. Any float/Decimal expansion mismatch invokes specification §2.4's integration stop; document its exact contract/input instead of relaxing assertions. Commit verified protected adapters.

**Acceptance:** E02–E05 statistical/capture behavior and E09 fabricated variants. Part A hard kill is IN_DOUBT; no partial-panel resume claim.

## Task 4: Independently reconstruct every checkpoint and the aggregate result

**Outcome:** G5 authorizes continuation from captured results and authenticates only complete passing campaigns or legal failing prefixes.

**Files:** Modify `execution/g5.py`, `verification.py`, `protocol.py`, `service.py`, canonical `qualification/evidence.py`, `policy.py`, `policy_sources.py`, `checkpoint_plan.py` and `journal_snapshot.py`; create `execution/campaign_g5.py`, `tests/ops/qualification/execution/test_campaign_g5.py`. Reuse pure functions in `result_adjudication.py`; retain accepted N1 legality/source reconstruction. Extend candidate artifact schemas and runtime source closure inventories in their canonical owners. The new G5 module orchestrates verification/signing; it must not duplicate canonical artifact reconstruction.

**Consumes:** Task 3 captured bytes/attestations and Task 2 service snapshot. **Produces:**

```python
# qualification/evidence.py; artifacts maps digest -> immutable fetched bytes.
def reconstruct_campaign(context, *, snapshot_bytes: bytes,
                         attestations: dict[str, bytes],
                         artifacts: dict[str, bytes]) -> bytes: ...

# execution/campaign_g5.py consumes the canonical reconstruction above.
def authenticate_campaign(context, *, result_bytes: bytes,
                          snapshot_bytes: bytes,
                          credential_reference: str) -> bytes: ...
```

Result bytes explicitly encode ordered decisions, prefix/completeness, attestation/assessment inventories and precommit journal/budget snapshot identities. Authentication binds result digest, revision, authority/domain and approved result key. G5 uses enrolled installed code; callers cannot provide a decision callback. Keep stage-assessment signatures distinct from final-result signatures by schema/scope. Signing intents fix payload/time/key and preserve exact candidate bytes across retries.

**N2 continuation contract:** extend canonical `policy.required_output_roles` under the new FULL_E1 policy identity to admit stages `('LEGALITY','N1','N2','PART_B')` with `completion='PARTIAL', verdict='NONE'`. Canonical evidence reconstruction additionally requires all four stage decisions PASS, exact shared N2 capture and accepted predecessor receipt. G5 authenticates that continuation; the service atomically commits it and moves to PART_A_READY. A failed N2 or half-population produces complete FAIL, never continuation; missing PART_B, partial aggregate PASS and N1_ONLY use reject. Update policy, artifact schemas, logical snapshot, G5 and store tests together rather than adding an execution-local exception.

- [ ] Add tests that reconstruct a genuine synthetic N1/N2/Part A capture chain through accepted source fixtures. Test an incomplete passing prefix and all three failing prefixes separately. Minimal result-shape rule to encode in the schema tests:

```python
# Proposed helper in canonical qualification/policy.py, added in this task.
def complete_pass(policy, decisions: dict[str, str]) -> bool:
    return (tuple(decisions) == tuple(_document(policy)['stage_order'])
            and all(value == 'PASS' for value in decisions.values()))

def test_n1_pass_is_not_full_pass(full_e1_policy):
    assert not complete_pass(full_e1_policy, {'LEGALITY':'PASS', 'N1':'PASS'})
```

`full_e1_policy` is produced by the Task 1 canonical policy builder/parser fixture for the new FULL_E1 identity; it is not a hand-maintained test dictionary. `_document` is the existing validated-policy accessor in `qualification/policy.py`.

- [ ] Run `./fp.ps1 python -m pytest tests/ops/qualification/execution/test_campaign_g5.py -q` red, then implement independent plan derivation, strict inventory reconstruction, admitted legality and pure adjudication. Validate N2/PART_B sharing before any stage result is authenticated.
- [ ] Add red/green canonical-policy and evidence tests for the N2 continuation contract above: genuine joint PASS reaches PART_A_READY; N2 failure, either half failure, omitted PART_B, altered shared capture and N1_ONLY release cannot. Verify the same role inventory is used by candidate staging, G5 and commit validation.
- [ ] Implement service commit of checkpoint assessments with expected revision, current validity/eligibility/budget and private candidate membership checks. Only these commits produce N2_READY/PART_A_READY. Refuse post-failure extra evidence and stale continuation assessments.
- [ ] Exercise tampering across each link: missing attestation, changed output digest, wrong source/image, inconsistent prefix, wrong current keys, altered cutoff, invented legality, replayed assessment from another attempt and stale snapshot. G5 rejection never launches replacement draws.
- [ ] Re-run G5 tests and accepted historical-N1 tests; commit the independent continuation/aggregate behavior.

**Acceptance:** E01–E05 reconstruction and E09/E11 authority rejection. Independent G5 means separate deployed process and credential in Task 6; in-process tests do not establish this isolation.

## Task 5: Atomically publish full results and separate seals against VOID

**Outcome:** only complete authenticated PASS can reach the separate seal signer; lost replies recover identical historical receipts and concurrent VOID prevents new usable authority.

**Files:** Modify `execution/campaign_store.py`, `store.py`, `service.py`, `release_schema.py`, `runtime.py`, `release.py`, and `qualification_cli.py`. Create `execution/campaign_seal.py`, `tests/ops/qualification/execution/test_campaign_commit.py`, `test_campaign_seal.py`. Extend host configuration/provisioning for qseal using the canonical configuration owner in `tools/qualification_verification/`; preserve the existing trust model. Retain legacy `qualification/seal.py` only for historical compatibility, with no protected full-route fallback.

**Consumes:** Task 4 authenticated aggregate and Task 2 ledger/snapshot. **Produces:**

```python
# CampaignStore methods, service-private after signature verification:
# commit_result(result_bytes: bytes, authentication_bytes: bytes,
#               *, expected_revision: int) -> bytes
# prepare_seal(attempt_id: str, result_receipt_bytes: bytes,
#              *, expected_revision: int) -> bytes
# commit_seal(intent_bytes: bytes, signature_bytes: bytes,
#             *, expected_revision: int) -> bytes
# recover_receipt(attempt_id: str, operation: str, payload_sha256: str) -> bytes

# campaign_seal.py: installed qseal process, never a client callback.
def sign_committed_pass(intent_bytes: bytes, *, committed_result_bytes: bytes,
                        authentication_bytes: bytes, result_receipt_bytes: bytes,
                        credential_reference: str) -> bytes: ...
```

Service serializes qseal invocation/publication with VOID under its campaign transaction lock, using a bounded signer timeout and already-persisted canonical signing intent. Candidate signature is private until commit. `recover_receipt` returns existing receipt bytes, historical status and current validity; mismatched payload conflicts. Persist receipt/artifact membership/event in the same transaction. Key policy/approval checks and budget checks occur immediately before new authority publication.

Reuse PR415's exact authentication/receipt retry and atomic seal-versus-VOID semantics and regression cases. PR425 retires the legacy public authority functions, so port those cases to the protected service/qseal boundaries and retain legacy rejection tests. Passing a legacy in-process composition case cannot establish protected execution or seal authority.

- [ ] Write red atomic tests using separate SQLite connections/processes and barriers, not a mock validity flag. Define both serialization outcomes:

```text
VOID acquires and commits first -> new result/seal commit rejects; receipt absent
commit acquires and commits first -> exactly one receipt; later VOID retained
retry after either ordering -> no new signature, current validity is VOID
```

- [ ] Run `./fp.ps1 python -m pytest tests/ops/qualification/execution/test_campaign_commit.py tests/ops/qualification/execution/test_campaign_seal.py -q`; confirm missing full commit/seal behavior.
- [ ] Implement transactional publication and separate qseal process/role/runtime/credential binding. New seal requests must fetch the exact committed aggregate; no incomplete PASS or FAIL reaches signing. Before publication repeat current validity, key-policy revision and budget checks even when signature already exists privately.
- [ ] Add crash points after signing-intent persistence, after signature persistence and after commit/before reply. Recover fixed bytes without new timestamp/key. Require committed receipt plus live validity for accepted seal verification; prohibit candidate fetch by clients.
- [ ] Add expiry/revocation, wrong role/domain, concurrent duplicate, stale revision, exhausted finalization budget and VOID-during-signing cases. A stalled signer releases no authority and is cleaned up without unlocking an uncommitted candidate to the client.
- [ ] Re-run targeted tests plus N1 atomic/historical receipt coverage, then commit. Document lock ordering and maximum lock-held duration from the canonical profile to prevent unbounded VOID starvation.

**Acceptance:** E07/E08/E10/E11/E12 atomic models; Task 6 proves distinct qseal access and races through actual service sockets.

## Task 6: Prove the complete Linux route and obtain combined review

**Outcome:** exact candidate revision has genuine launch-to-seal evidence for all E01–E12 cases and independent review of the complete composed route.

**Files:** Extend `scripts/qualification_boundary_verification.py`, `scripts/check_qualification_invariants.py`, `tests/ops/qualification/execution/lifecycle_model.py`, `tests/ops/qualification/invariant_manifest.json`, `tests/test_qualification_invariant_manifest.py`, `tools/qualification_verification/host.py`, `host.json`, `README.md`, `tests/integration/qualification_boundary/`, `.github/workflows/qualification-execution-boundary.yml`. The manifest and CI/report validation are already delivered by PR425; extend their accepted semantics and node mappings. Create `tests/integration/qualification_boundary/test_full_e1_campaign.py` and an evidence report under `docs/notes/audits/` dated for actual acceptance. Reuse the accepted recorder/manifest/cleanup framework; do not create a parallel evidence authority.

**Consumes:** Tasks 1–5 and accepted PR425 host setup, lifecycle model, invariant manifest and CI/reporting gate. **Produces:** proposed CLI selector `--campaign full-e1` on the existing verifier, E01–E12 entries in that canonical manifest, immutable evidence bundle and combined review verdict.

- [ ] Extend the existing host fixture producer with actual synthetic sources for passing N1/N2/Part A, early N1 fail, N2 FULL fail, half-population fail, below-floor Part A, above-FULL sanity failure and expansion/no-expansion. Register each source bundle with TEST_ONLY frozen contracts through ordinary admission. Fixture generation must never directly write passing output artifacts.
- [ ] Add the full-route suite with actual qclient/qexec/qg5/qseal UIDs, protected installed code, worker images and private credentials. Retain Docker create/start/die history to assert one launch per dispatched checkpoint and zero starts for stopped stages. Compare original/expanded panel prefixes and receipt bytes from the archived artifacts.
- [ ] Extend accepted PR425's lifecycle model and canonical invariant manifest with full-campaign transitions and E01–E12 mappings. Preserve its exact collected/executed test identities, critical-skip/failure rejection, child-report hash binding and mutation checks. Verify the extended suite is selected by the same recorder/CI gate; do not substitute a second scenario-list validator.
- [ ] Install deterministic fault barriers only in the approved TEST_ONLY harness configuration. Exercise every E06 crash boundary, E08 budget phase and both orderings of E10 races through sockets/processes; hard-kill tests include recovery/owned cleanup. A test configuration must never be admitted as an OPERATOR release.
- [ ] On a fresh supported disposable Linux host, provision with the accepted harness and run its launcher doctor. Implement and run this successor invocation (the selector is new, not present-day functionality):

```bash
sudo bash tools/qualification_verification/provision.sh --manifest-output /tmp/qualification-manifest-path
manifest="$(sudo cat /tmp/qualification-manifest-path)"
host_root="$(dirname "$manifest")"
sudo "$host_root/env/bin/python" -I scripts/fp.py --env "$host_root/env" doctor
sudo "$host_root/env/bin/python" -I scripts/fp.py --env "$host_root/env" python \
  scripts/qualification_boundary_verification.py --test-only --campaign full-e1 --manifest "$manifest"
```

- [ ] Fail verification on any critical skip, missing case/evidence, altered candidate snapshot, incomplete receipt/capture, lifecycle mismatch or cleanup failure. Preserve reports after host teardown. Repeat fresh-host setup according to the accepted harness reproducibility gate.
- [ ] Run the checkout's `test`, `test-ops` and `check` standard suites/gates as required for the final integration; preserve command, interpreter, revision/dirty state and actual outcomes. Disclose any pre-existing gate failure; do not call the full suite passing when only targeted tests pass.
- [ ] Obtain independent combined review using the requesting-code-review skill. The reviewer receives the spec, plan, accepted N1 evidence, exact integrated diff and Linux E01–E12 report. Ask for both spec-compliance and quality/security/statistical review across boundaries. Resolve actionable findings and rerun affected scenarios; the coordinator owns acceptance.
- [ ] Record ACCEPT only if every specification §6 condition holds; otherwise record REJECT with the exact missing evidence/finding. Synthetic acceptance remains TEST_ONLY and confers no live qualification/deployment authority.

## Coverage and self-review

| Specification requirement | Owning tasks | Acceptance cases |
|---|---|---|
| Merged PR425 foundation, canonical interfaces and closed capability | 1 | E07, E09, E11 |
| Genuine stage sequence, early stops and one joint batch | 3, 4 | E01, E02, E03 |
| Part A prescribed expansion and original prefix | 3, 4 | E04, E05 |
| One durable compute/verify/finalize budget | 2, 4, 5 | E08 |
| Recovery without uncertain redraw and exact retries | 2, 4, 5 | E06, E07, E12 |
| Canonical N2 continuation, independent G5 and artifact provenance | 3, 4 | E01, E03, E09, E11 |
| Atomic full result, separate seal, VOID ordering | 5 | E07, E10, E11 |
| Extend PR425 Linux lifecycle/invariant gate and combined review | 6 | E01–E12 |

Before integration, trace one passing campaign, each early failure, an interrupted Part A, capture-before-crash, budget exhaustion in G5, lost seal response and both VOID orders through their actual producers/store transitions. Verify matching interface names, schema fields and predecessor digests across plan derivation, worker, G5 and publication. A correction to any shared contract requires checking every affected producer and consumer.

At delivery this is a proposed full-E1 specification and roadmap rebased on the accepted merged N1 foundation. No full-E1 runtime code, campaign execution or independent full-E1 review is claimed. Task 1a has accepted local pure-planning implementation and verification; Task 1b is selected to complete the admission outcome without dispatch. The N1 prerequisite is satisfied; full-E1 capabilities and §6 acceptance remain outstanding. Broker integration is not a dependency.



### Task 1a coordinator disposition — panel-count conflict resolved

**Decision:** preserve the canonical validator; equal initial/expanded panel limits are rejection cases, not positive planning inputs. The prior conflict entry remains historical evidence. Its request for a coordinator decision is satisfied by this disposition, which updates the handoff, specification §2.4 and E05 together. Task 1a is still NOT IMPLEMENTED / NOT ACCEPTED, but this specific scope conflict is closed and the corrected handoff is ready to resume. No canonical-validator change, footprint expansion, Task 1b work or agent dispatch is authorized by this documentation correction.

| Related case | Disposition |
|---|---|
| Equal expanded/initial limits with original workload depths | Reject: strict-greater workload invariant. |
| Equal limits with copied PART_A/REGIME pair `(2, 2)` | Reject: sorted unique depth invariant as well. |
| Valid greater expanded limit, unchanged initial seed prefix | Required positive planning case. |
| Lower-level Part A request permits equal counts | Intentionally broader engine input; not evidence of frozen-input support. |
| Percentile distance equals expansion tolerance | Still inclusive; unaffected statistical boundary. |

Evidence reviewed: unchanged merged validator and its contract/policy consumers; selected baseline record `.cache/fp-verification/20260918T235615Z-3be64adfa903/record.json` is completed with exit_code/verification_exit_code zero, source_stable/capture_complete true and no capture/report errors. The agent's 173 passing regressions remain baseline evidence, not Task 1a implementation acceptance. Reuse those results while their relevant sources remain unchanged; run new Task 1a rejection/positive tests as implementation proceeds. No runtime tests or Linux runs were performed for this documentation correction.

### Task 1a resumed progress — 2026-09-18: implemented and locally verified

**Outcome / return boundary:** delivered the corrected Task 1a pure planner, validating consumer and verified-context adapter, with local tests and diff review. Return to the coordinator for acceptance. Task 1 and full E1 remain incomplete. No commit, push, PR, service registration, source replay, Linux campaign, dispatch, reservation, G5 continuation, result or seal was performed. The earlier equal-panel conflict is resolved by the coordinator's correction; strict greater-than workload policy is unchanged.

**Workspace and tested state:** `C:/Users/joshu/.codex/worktrees/full-e1-spec-baseline/multi_firm_operations`, detached HEAD `1e4928360b95812b04725dc1e8da97709d670ff4`. Tracked modifications: `ops/c1_rail/qualification/checkpoint_plan.py`, `ops/c1_rail/qualification/execution/plan.py`, `tests/ops/qualification/execution/bundle_fixture.py`. Added untracked `tests/ops/qualification/execution/test_campaign_plan.py`. The three pre-existing untracked planning documents remain; only this roadmap was edited by this resumed implementation. The corrected handoff and governing specification were preserved. Final verification ran with these source/test edits; the progress documentation was updated afterward.

**Implemented public interfaces:**

```python
# ops/c1_rail/qualification/checkpoint_plan.py

def derive_campaign_plan(contract, *, policy, execution_release_sha256: str,
                         source_bundle_sha256: str, attempt_id: str,
                         exact_depth_approval_sha256: str) -> bytes: ...

def validate_campaign_plan(raw: bytes, *, contract, policy,
                           execution_release_sha256: str,
                           source_bundle_sha256: str, attempt_id: str,
                           exact_depth_approval_sha256: str) -> dict: ...

# ops/c1_rail/qualification/execution/plan.py

def derive_campaign_plan_from_context(context) -> bytes: ...
```

The pure producer uses unchanged validator-issued frozen inputs, canonical semantic policy and supplied identity bindings. The adapter consumes `verify_bundle`'s actual ExecutionContext, checks release/domain/policy/attempt/approval/index/retained-artifact cross-bindings, and invokes that producer. Neither Python object types nor plan bytes grant authority. Admission owns signature/current-validity checks; no new authority consumer is introduced.

**Closed wire shape:** `qualification_campaign_plan/v1`, `purpose=PLANNING_ONLY`, `target_capability=FULL_E1`, `authorizes_dispatch=false`, `authority_class=TEST_ONLY`. Top-level identities bind attempt, contract, domain, policy, actual execution release, retained source bundle index, exact-depth approval, initial state, replay, RNG namespace/mechanics and exact frozen budget plus its canonical digest. `checkpoint_groups` is the canonical ordered N1, joint N2/PART_B, PART_A grouping. `cutoff` holds frozen N2/PART_B thresholds and no seeds. `n1` is the unchanged existing producer's parsed subplan. `n2.depths` maps FULL to N2 and H1/H2 to PART_B; `n2.seed_inputs` is one population-major batch. `part_a.parameters` is the frozen Part A document; half-open `initial_panel_range` and `potential_appended_panel_range` select prefixes of `potential_panels`, whose entries contain only panel index, outer seed and ordered path seeds. `probes` explicitly identifies each compute checkpoint; N1/N2 retain their identical existing probe address. No sampled panel identity, source occurrence order, expansion decision or outcome is invented.

Validation independently re-derives the expected bytes from the frozen inputs and requires exact byte equality before parsing. This rejects unknown/noncanonical/malformed declarations, bool/int aliases, reordered/missing/extra seeds and coherently rehashed caller changes, without recursively parsing hostile input first. No second policy or N1 implementation was added.

**Representation and interface limits:** canonical owner caps materialization at 100,000 seed entries (including repeated probe declarations) and 64 MiB, with a conservative pre-materialization byte estimate including namespace size. Oversized signed workloads reject before calling the seed producer; they are never truncated. The context adapter additionally screens entry count at 4,096 bytes per entry against the smaller profile/frozen memory setting, and bounds retained bundle bytes and plan bytes by the profile input limit. This is an allocation screen, not measured memory enforcement or a budget reservation. The signed reference-depth test (N1 200 per population, N2/PART_B 970, Part A 100/200 panels with 200 paths each) produces **21,623,745 plan bytes**: 600 N1 paths, 2,910 joint N2 paths, 40,000 potential Part A paths and 200 outer addresses, plus declared probes. It fits the 64 MiB representation and 100,000,000-byte input limit. It exceeds the current N1 10,000,000-byte output and 15,000,000-byte RPC limits: Task 1b/later transport owners must explicitly account for full-plan storage/transport in the versioned FULL_E1 profile. This handoff does not serialize it through an N1 RPC, relax those limits, or assert executable-route feasibility. Actual process memory/runtime enforcement remains later work.

**Test-driven evidence:**

- Initial requested producer test failed because the adapter was absent: `.cache/fp-verification/20260919T000306Z-26dea9e3a987/record.json` (1 failure, expected red).
- Full initial contract tests: `.cache/fp-verification/20260919T000459Z-d85cd9755ff3/record.json` (33 failures for missing APIs, 1 existing workload rejection passed).
- First implementation: `.cache/fp-verification/20260919T000630Z-3cab090fa369/record.json` (34 passed).
- Diff review found the coherent retained-source/index edit family. Regression first failed with DID NOT RAISE: `.cache/fp-verification/20260919T000748Z-ae53b09420a9/record.json` (1 expected failure). Fixed cross-binding to frozen artifacts and freeze approval; covered content, path, extra-role and approval variants. Related mixed-context contract/domain/release/attempt/approval/index/retained-byte cases reject. Signature re-verification remains with `verify_bundle`, not the planner.
- Expanded campaign suite: `.cache/fp-verification/20260919T000845Z-9128c28b9795/record.json` (41 passed, zero skips; captured reference-size measurement). It includes retained signed fixture reconstruction, independent seed vectors, prefix boundaries, equal-count/duplicate-depth rejection, changed bindings, authority closure, oversized signed workload rejection and instrumented no-replay/no-sampling/no-launch/no-store/no-signing tests. Library instrumentation is not Linux isolation evidence.

**Final commands and results:**

Interpreter for all launcher work: `C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`, Python **3.13.2**. `./fp.ps1 doctor` passed, 62 locked packages matched, optional signing dependency 50.0.1.

```powershell
./fp.ps1 --workers 2 python -m pytest tests/ops/qualification/execution/test_campaign_plan.py tests/ops/qualification/execution/test_bundle.py tests/ops/qualification/execution/test_release.py tests/ops/qualification/execution/test_protocol.py tests/ops/qualification/test_checkpoint_validation.py tests/ops/qualification/test_seed_probability_vectors.py tests/ops/qualification/test_semantic_policy.py tests/ops/qualification/execution/test_preflight.py -q --tb=short
./fp.ps1 check
git diff --check
```

- Final targeted campaign/regression run: **216 passed in 75.69 seconds, zero failures/errors/skips**. Record `.cache/fp-verification/20260919T001032Z-a4746e394d31/record.json`: status completed, exit_code 0, verification_exit_code 0, source_stable true, capture_complete true, empty capture/report errors, matching valid JUnit counts.
- Standard check: exit 0. Record `.cache/fp-verification/20260919T001031Z-33aeb989a274/record.json`: status completed, exit_code/verification_exit_code 0, source_stable/capture_complete true, no capture/report errors. Its evidence-store unittest phase ran 72 tests with **3 skips**. Other reported limitations/advisories: absent local Pine/data/heavy artifacts, P5-WEAK instrument evidence dates and existing session-label duplicates. These are not full artifact validation or zero-skip gate evidence. The check recorder retains stdout/stderr rather than a pytest JUnit summary.
- `git diff --check` passed. Inspected the production diff, new tests, fixture variations and import/call boundaries. Existing N1 producer body, release/protocol/service/store and policy/statistical constants remain unchanged. Git emitted line-ending notices and the read-only sandbox could not access the user's global ignore file; neither changed repository contents or failed recorded verification.

**Remaining coordinator / Task 1b obligations:** review this exact local diff and the representation screens/schema; retain the actual N1_ONLY release identity as a planning binding only. Then separately deliver versioned FULL_E1 release admission, closed SUBMIT_E1 protocol, service-owned durable campaign identity/receipt, duplicate/conflict handling and status/invalidation without launch. Validate plan bytes from verified service-owned inputs, account for their measured transport size, and bind the exact resolved configuration/version before later activation. Budget lifecycle, dispatch/restart, G5 continuation, result/seal publication and Linux E01–E12 acceptance remain subsequent handoffs. No existing N1_ONLY attempt acquires migration or dispatch authority from Task 1a.

### Task 1a coordinator acceptance — 2026-09-18

**Disposition: ACCEPTED for the planning-only checkpoint.** The coordinator inspected the corrected handoff, all four changed source/test files, canonical workload/contract/profile consumers and recorded verification. An independent read-only code review returned no actionable findings and accepted Task 1a. N1 delegation, joint N2/Part B addresses, Part A outer/path/probe addresses, retained-input binding, exact-byte re-derivation and pre-materialization bounds satisfy this slice. No execution authority is introduced. Task 1, Task 1b and full-E1 acceptance remain incomplete.

**Accepted state:** detached merge `1e4928360b95812b04725dc1e8da97709d670ff4` plus the uncommitted implementation/test changes recorded above. For both `.cache/fp-verification/20260919T001032Z-a4746e394d31/record.json` and `20260919T001031Z-33aeb989a274/record.json`, the coordinator verified SHA256 equality between the recorded final snapshot and current `checkpoint_plan.py`, `execution/plan.py`, `bundle_fixture.py` and `test_campaign_plan.py`. Both records are completed, exit_code/verification_exit_code zero, source_stable/capture_complete true, without report errors. The recorded selected run contains 216 passed and zero failures/errors/skips, using operations Python 3.13.2; the check retains its three evidence-store skips and artifact/documentation advisories. `git diff --check` passed at review. These checks were reused, not rerun; the independent reviewer did not run external gates.

**Next handoff constraint:** the measured reference plan is 21,623,745 bytes. Task 1b must define a versioned, bounded storage/retrieval contract before exposing FULL_E1 plan bytes; it must not send this artifact through current N1 output/RPC limits or silently increase them. Service-side derivation/storage and a small digest/receipt response are a candidate design, but complete artifact retrieval limits/framing still require an explicit decision and tests. Planning byte/memory screens are not enforced campaign-resource budgets. No N1_ONLY attempt acquires migration/dispatch authority, and the accepted N1 release/profile remain unchanged.

This acceptance ends coordinator review of Task 1a. No commit, push, new implementation handoff execution or full-E1 run was performed. The acceptance applies only while the reviewed implementation/test bytes remain unchanged; subsequent source changes require proportionate re-review and verification.

### Forward priorities and Task 1b selection — 2026-09-18

The operator has selected two parallel priorities: complete the protected synthetic E1 route, and resolve actual feed plus direct CrossTrade -> Tradovate feasibility. Other work is selected only when it directly unblocks one of those outcomes. Reassess the deployment timeline after both milestones have evidence; no launch date is committed. Broker feasibility does not gate synthetic implementation, and synthetic PASS does not establish live readiness.

Task 1a is accepted; do not repeat its corrected implementation. Task 1b is dispatched as a bounded admission-only handoff: installed versioned FULL_E1 TEST_ONLY release, authenticated closed requests, service-owned immutable plan and retained inputs, durable identity/receipt, duplicate/conflict/restart behavior, authorized VOID and bounded plan retrieval. No worker, G5 or qseal dispatch is enabled. The coordinator accepts the returned evidence before selecting budget/recovery, genuine execution, G5, commit/seal and Linux acceptance handoffs. Each remains subject to its actual prerequisites.

The selected transport contract stores the full plan privately in the existing service authority. Admission returns its digest and total byte length with a durable receipt. A FULL_E1-versioned plan-chunk operation returns canonical JSON carrying object digest, offset, total byte length and canonical base64 bytes; at most 1 MiB of raw bytes per request. Exact nonnegative integer offsets and positive integer lengths are required (bool aliases reject), with offsets below total length and length at most the configured chunk bound; the final response clips at EOF and reports its actual byte count. Reject wrong membership, unknown digests, unauthorized peers and out-of-range values. Each chunk remains within the resolved RPC frame bound after encoding. Retrieval is read-only and deterministic across restart; clients verify offsets, length and the digest after reassembly. Historical retrieval after VOID grants no authority. Whole-plan limits retain the canonical 64 MiB cap and resolved profile input bound. These reusable limits belong to canonical versioned configuration, not copied transport constants. Existing N1 limits and field sets stay unchanged.

Task 1b retains the exact frozen budget identity but does not establish enforced lifetime accounting. Before execution activation, Task 2 must account for campaign-specific admission/provider work as required by specification section 2.5; admission-only evidence cannot bypass that requirement.

The parallel feasibility investigation uses CAP-20260916 in docs/briefs/phase4-preparation/2026-09-16/capability-decision.md as the existing verdict owner. Its checkpoint is a current primary-source and repository evidence matrix plus bounded tests for the remaining unknowns. Read-only documentary work is authorized; account-specific mutations, order tests, subscriptions and external messages require their actual scope of authorization. Documentation alone does not qualify the account or feed.
### Operator direction: proportional verification and learning during rollout

The operator clarified that not everything must be measured before deployment. Predeployment evidence must be justified by the first operation it protects; uncertainty about an operational distribution is not automatically a blocker. Reuse unchanged revision-bound evidence, test changed boundaries, and run integrated Linux/combined review for the protected E1 result once the route exists. Synthetic provenance, no-redraw/budget integrity, authenticated G5 and atomic result/seal-versus-VOID remain correctness obligations of the selected E1 design.

Separate deterministic readiness from empirical learning. Before the relevant live operation, establish usable entitled inputs, account/instrument identity, the selected order/protection primitives, ownership of uncertain requests, intervention/closure behavior and working evidence capture. During an authorized bounded rollout, measure slippage, latency, fill quality, rejection frequency, feed gap/correction/reconnect rates and operational reliability. Mature estimates of those distributions are not prerequisites to their first controlled observation. Basic identity, chronology and fail-closed behavior are distinct from observed performance rates.

Use existing measurement/reporting paths, adding only missing producers needed by the selected rollout. Inspected code provides EventLedger/BrokerEvidence and c1_rail_slippage.py for event-to-fill joins and cohort summaries; current slippage coverage is MYM/MNQ add-focused, not complete four-leg telemetry. HeartbeatState provides current liveness rather than an established historical four-source recorder. This inspection does not establish an automatic policy-update consumer for all optional telemetry fields. Preserve original observations and review proposed updates through their actual authority; no calibration constants or risk policy changed here.

The feasibility checkpoint is narrowed accordingly: one provider/account acquisition decision when needed, then a non-emitting identity/basic-integrity observation window, followed by a separately scoped first order-capable session with capture and intervention responsibilities. Do not build a new provider-neutral conformance framework or require mature live-performance distributions first. Any existing gate that demands such distributions must be explicitly narrowed in its owning contract rather than reported as passed without evidence. No live action, spending, deployment or launch date is authorized by this planning direction.
### Task 1b coordinator acceptance — 2026-09-18

**Disposition: ACCEPTED for dormant admission only.** The independent reviewer accepted the final code with no outstanding actionable findings. The coordinator inspected service/consumer/storage behavior and verified all ten Task 1b implementation/test SHA256 values against both final verification snapshots and the independent review identities. Base remains detached `1e4928360b95812b04725dc1e8da97709d670ff4`, plus uncommitted Task 1a/1b and documentation edits. No commit, push, deployment, worker dispatch or live action occurred.

Final selected regression record `.cache/fp-verification/20260919T003248Z-100e170d5b7e/record.json`: 182 passed, zero failures/errors/skips; completed, exit/verification exit zero, stable source, complete capture and no report errors. The checkout launcher ran the command recorded in the Task 1b handoff with operations Python 3.13.2. Check record `.cache/fp-verification/20260919T003321Z-44e0f6cac19f/record.json` has the same successful record properties; its 72 evidence-store cases retain three skips and existing artifact/documentation advisories. Checks were run by the executor and inspected by the coordinator, not redundantly rerun. Independent review did not claim external gates. Final diff whitespace check passed before this documentation update.

Review corrections are included: production client verifies bounded ordered chunk reconstruction and whole digest; malformed types reject cleanly; huge offsets cannot overflow SQLite; missing VOID receipts explicitly fail restart validation. Actual reference-depth plan bytes round-trip through bounded chunks without enlarging N1 RPC/output limits. This is functional compatibility evidence, not a performance-distribution gate.

Implemented interfaces and exact commands are retained in [Task 1b handoff](../../briefs/handoffs/2026-09-18-full-e1-task1b-durable-admission.md). FULL_E1 release/profile v2 are explicitly TEST_ONLY, dispatch disabled, with no executable checkpoints. Schema v5 adds dormant campaign tables under the existing ExecutionStore transaction authority and migrates only the exact accepted v4 layout. Historical N1 rows remain readable; reverse use of a v5 database by old v4-only software is unsupported, so rollback is not an in-place downgrade. No attempt promotion is authorized.

Task 2 is the next implementation checkpoint: one durable lifetime budget and no-redraw recovery, including the required treatment of campaign-specific admission/planning costs before execution activation. Its proposed roadmap API must be reconciled with the actual Task 1b CampaignStore interfaces; do not replace the accepted store/validity authority or invent a second ledger. Genuine computation, G5, result commit/sealing and combined Linux E01-E12 acceptance remain incomplete. The coordinator retains combined acceptance. Broker/feed feasibility remains an independent track; no subscriptions or demo accounts are available, and performance learning is allocated to the bounded rollout as directed above.
