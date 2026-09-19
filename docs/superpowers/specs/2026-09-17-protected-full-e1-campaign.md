# Protected full E1 campaign successor specification

**Status:** Proposed; reviewable specification, not implementation acceptance.
**Decision date:** 2026-09-17
**Authors:** Codex, for Joshua
**Layer:** execution
**Related:** `2026-09-17-qualification-execution-boundary-design.md`; `2026-09-17-qualification-structural-closure-design.md`.
**Integration owner:** the coordinating full-E1 implementer, accountable for the complete Linux route and combined review.

## §0 — Production-source verification

### Accepted merged baseline — 2026-09-18

[PR425](https://github.com/Joshua-Asante/first-passage/pull/425) merged as `1e4928360b95812b04725dc1e8da97709d670ff4`. PR415 was closed without merging separately; PR425 against main incorporated the combined foundation and protected N1 implementation. This merged revision replaces the earlier stacked-PR prerequisite.

Accepted head `63a92fd31753c0770e998975f87187f9c92f6505` was tested in CI merge `3a4ae6601167274330475306628302acd43feb2a`. The [mandatory two-host boundary run](https://github.com/Joshua-Asante/first-passage/actions/runs/35401263108) succeeded, reporting 464/464 cases per host, zero skips, stable source and successful cleanup. The [final full hosted pytest run](https://github.com/Joshua-Asante/first-passage/actions/runs/35401263099) also completed successfully; earlier pending descriptions are stale. Independent review and detailed evidence are retained in `docs/notes/audits/2026-09-18-qualification-combined-verification.md`. These records satisfy the N1 prerequisite, not full-E1 acceptance.

Read at the merge before this amendment: `ops/c1_rail/qualification/execution/release_schema.py` still enforces N1_ONLY and production_execution=false; `policy.py` still permits PARTIAL/NONE only for the N1 prefix. Canonical owners remain `qualification/checkpoint_plan.py`, `policy.py`/`policy_sources.py`, `evidence.py` and `journal_snapshot.py`. The accepted manifest is `tests/ops/qualification/invariant_manifest.json`, paired with `tests/ops/qualification/execution/lifecycle_model.py` and `scripts/check_qualification_invariants.py`.

Former stop-readiness, OOM, lifecycle/concurrency, invariant-wiring and combined-review blockers are historical and closed by subsequent accepted evidence. Historical failed runs remain failed evidence; the old exit137 observation is not retroactively confirmed as OOM. Preserve the corrected implementation and regressions rather than reopening those repairs.

Documentation workspace: `C:/Users/joshu/.codex/worktrees/full-e1-spec-baseline/multi_firm_operations`, detached at the merge above. Both successor drafts were copied from the original documentation checkout, which remains unchanged.

### Initial authoring snapshot (historical)

Read before authoring on 2026-09-17. Main documentation checkout: commit `c2e6eb2cbe159b60fdff7873b9e96aef943c46df`. Implementation inspected in `.worktrees/qualification-structural-closure`, whose HEAD was `6be024a`; that worktree contains active, uncommitted N1 changes. These are observations, not an accepted revision. Paths below are relative to that worktree; SHA256 identifies the inspected working bytes.

| Source | SHA256 | Grounded observation |
|---|---|---|
| `ops/c1_rail/qualification/orchestration.py` | `c762e690e4bd98d987d4069fcbd5e24e5b8b2a8ca4a60c9b7bf416b1560c4bfb` | N1, CUTOFF, joint N2/Part B, Part A; existing controller is not the protected route |
| `ops/c1_rail/qualification/part_a.py` | `6c164842a5d5bbdf6a3e5e4a6d0c54b7f4eb2dfa253dc37e670b76567a70e82e` | One probe, initial panels, conditional append, final floor/FULL sanity check |
| `ops/c1_rail/qualification/result_adjudication.py` | `8ad0eb57de12324877d538da6c326d0c91bce86c925794482393a2b66a738204` | Pure replay adjudication and exact Decimal panel-prefix expansion decision |
| `ops/c1_rail/qualification/production.py` | `a8a5ab3fef9d553a51b2e30b3d43929e6f6c9b98e4c2afe496242d1f8d117786` | Request adapters and replay mechanics; legacy store/executor authority must not be reused |
| `ops/c1_rail/qualification/execution/compute.py` | `bbcd8c52e94e36ac0f648526617541da1f4c30d32dec9e4c796cfc731e517fee` | Store-free N1 adapter, factory source, budget-wrapped replay |
| `ops/c1_rail/qualification/execution/budget.py` | `409247b5b3941eadd27a272302c2d31511d2fe169a63068a35e76a7781aba645` | Process-local clock and memory guard; not a durable campaign budget |
| `ops/c1_rail/qualification/execution/store.py` | `b8a1fee44b7c1f67e405db666e95a78a5cc24e652a704ad159a8aa6be8f3ae15` | Service-owned capture, revisioned assessment, historical receipt retry |
| `ops/c1_rail/qualification/execution/service.py` | `d35fb74fb8770bb75aaed964d0fa6b9bf4253641f943da6b92dd6cfa489f5793` | Client/G5/operator ACLs, Docker dispatch and recovery |
| `ops/c1_rail/qualification/execution/g5.py` | `ddd35b43d1fdab0ddf7af9fecfc03e5f4a030f149d413d5b9496d8977542149a` | Capture reconstruction, result authentication, historical inspection |
| `ops/c1_rail/qualification/execution/release_schema.py` | `7a4fce48475c8fc76fcd38381df6bfc8ad1b6b101831c3a7863f872b15b37c2f` | Closed N1_ONLY release, production_execution=false |
| `tools/qualification_verification/README.md` | `4e63dee651a5338b85afa6c1093c12595f2e36c4b36e719e455cb60781a052d1` | Disposable Ubuntu host; privileged qexec is explicitly trusted |

Also inspected `execution/worker.py`, `execution/protocol.py`, and the legacy `seal.py` entry points. Governing N1 design explicitly excludes full PASS/sealing and requires a successor. At initial authoring, N1 acceptance was not established. This historical snapshot is superseded by the accepted merged baseline above.

## §1 — Context and scope

The statistical engine already expresses E1. The missing capability is controlled execution and durable authority through its entire sequence. Protected N1 currently offers a FAIL result or a passing checkpoint; passing N1 alone is insufficient to authorize E1 PASS. A process-local budget cannot enforce one allowance across service restarts, multiple workers, G5 and sealing.

**Decision driver:** make one synthetic campaign demonstrably complete from admitted input through captured computation, independent adjudication, atomic result commit and separate seal authority.

Direct CrossTrade → Tradovate remains the intended broker route. Broker connectivity, account deployment, live activation and real qualification are outside this engineering acceptance. Synthetic sources must traverse the installed protected execution route and retain TEST_ONLY authority throughout.

## §2 — Decision and normative behavioral contract

**Decision:** extend the accepted protected N1 interfaces with one service-owned campaign state machine; reuse the existing replay, RNG and statistical routines behind that boundary.
**Effective:** N1 prerequisite satisfied at PR425 merge `1e4928360b95812b04725dc1e8da97709d670ff4`; full-E1 acceptance still requires §6.

### 2.1 Prerequisite and release compatibility

Use PR425 merge `1e4928360b95812b04725dc1e8da97709d670ff4` and the §0 accepted evidence as the implementation baseline. The foundation dependency is satisfied; no separate PR415 merge or further N1 repair assignment is required. Task 1 records those identities and delivers only its bounded FULL_E1 admission/plan outcome. N1 isolation, lifecycle, concurrency, invariant and review guarantees remain regression requirements. Newly discovered regressions return to the coordinator with evidence; they do not automatically revive the historical blocker list.

Extend PR425's canonical owners: `qualification/checkpoint_plan.py` for pure plans; `qualification/policy.py` and `policy_sources.py` for policy and output-role requirements; `qualification/evidence.py` for artifact parsing/reconstruction; and `qualification/journal_snapshot.py` for logical snapshots. Execution-layer adapters may compose these functions but must not maintain competing policy, plan, artifact-role or snapshot definitions. Extend the accepted lifecycle model, invariant manifest, report validator and recorder for full-E1 acceptance instead of introducing a second acceptance framework.

Introduce an explicitly versioned `FULL_E1` capability; keep `N1_ONLY` behavior closed. FULL_E1 initially has `authority_class=TEST_ONLY` and `production_execution=false`. New schemas must not silently reinterpret N1 v1/v2 records as full campaigns. Existing N1 receipts remain inspectable. No in-place continuation of an N1_ONLY attempt into FULL_E1: its release, approvals and budget did not authorize that campaign. Fresh synthetic FULL_E1 attempts use the accepted N1 implementation under the new release.

### 2.2 Ownership and input producers

| Owner | Produces and owns | May not supply |
|---|---|---|
| Installed release/admission authority | Canonical resolved profile, contract, source bundle, exact-depth approval, runtime/worker/source identities, key enrollment | Unbound mutable runtime overrides |
| Client | Campaign request identity and registered bundle digest; status/fetch/retry requests | Stage choice, paths to code, seeds, outcomes, cutoff, resource measurements or verdict |
| Execution service (trusted qexec) | Campaign journal, plans, launch intents, owned container IDs, captures, artifact membership, budget ledger, validity and commit receipts | Client-asserted execution proof |
| Worker | Actual per-path outcomes, panel source occurrence order and structured observations, through bounded captured output | Journal writes, signing keys, Docker or next-stage authorization |
| Independent G5 (qg5) | Reconstructed evidence, deterministic stage decisions, authenticated assessments/final result bound to snapshot | Replacement draws, replay execution or caller-object provenance |
| Separate seal process (qseal) | Seal signature for exact committed complete PASS under current validity | Result signature, stage dispatch, policy mutation |
| Operator | Authenticated VOID request | Undo VOID or replenish a started campaign |

qexec owns persistent validity and serializes all authority publication. qg5 and qseal run separate installed processes/UIDs and hold different credentials. Preserve the N1 trust assumption: administrator and Docker-privileged qexec are trusted. Direct UID/key separation does not defend against a malicious root-equivalent qexec. Worker/client/G5/seal principals receive no Docker access. Neither G5 nor qseal loads caller source as executable code.


### 2.2a Bounded campaign-plan transport

The service derives and durably retains the canonical campaign plan from verified installed inputs. Admission returns a small immutable receipt binding its digest and total byte length; it does not return the whole plan through N1 transport. The measured reference plan is 21,623,745 bytes.

FULL_E1 defines versioned authenticated plan-chunk retrieval with a canonical configured maximum of 1 MiB raw bytes per response, within the resolved RPC frame limit after base64/JSON encoding. Requests bind attempt, object digest, offset and length. Validate exact integer types (reject bool), nonnegative offset below object length, and positive length no greater than the chunk limit. The last chunk clips at EOF. Responses bind digest, offset, total length, actual chunk length and canonical base64 bytes. Every fetch verifies attempt/object membership and role access; arbitrary digest access is forbidden. Clients verify ordered offsets, total length and the reassembled SHA256. Identical reads recover identical bytes after restart. Read-only historical access after VOID does not authorize any new execution or publication.

Whole plans remain bounded by the canonical planner's 64 MiB cap and the resolved profile input limit. Configure reusable bounds once in their canonical owners; N1 output/RPC limits and closed schemas are not increased or reinterpreted. Admission-only Task 1b retains frozen budget identity; execution activation still requires section 2.5 accounting, including campaign-specific admission/provider work.

### 2.3 Stage progression

Campaign progression and validity are separate fields. `VALID -> VOID` is irreversible. The service alone advances progression using a committed G5 assessment and matching journal revision.

| Durable predecessor | Next action | Accepted outcome |
|---|---|---|
| ADMITTED | Reserve campaign budget; dispatch N1 once | Captured and attested FULL/H1/H2 |
| N1 capture | G5 reconstructs N1; commit its assessment and deterministic CUTOFF | N1 FAIL -> terminal statistical FAIL; PASS -> N2_READY |
| N2_READY | One N2 worker dispatch | One ordered FULL/H1/H2 batch |
| N2 capture | G5 assesses N2 and PART_B together | Either FAIL -> terminal statistical FAIL; both PASS -> PART_A_READY |
| PART_A_READY | One Part A worker dispatch | Initial panels plus prescribed expansion, if required |
| Part A capture | G5 reconstructs prefix, expansion and final decision | FAIL -> terminal statistical FAIL; PASS -> FULL_PASS_READY |
| Terminal statistical result ready | G5 authenticates aggregate; service commits full result | RESULT_COMMITTED_FAIL or RESULT_COMMITTED_PASS |
| RESULT_COMMITTED_PASS | Separate seal authority under atomic current checks | SEALED_PASS receipt |

LEGALITY is reconstructed from admitted evidence according to the accepted N1 contract. Do not infer legality from `outcomes['LEGALITY']={}` or trust the legacy helper's unconditional LEGALITY PASS. Missing/invalid admission is a rejected or aborted campaign, not an invented statistical observation.

CUTOFF contains no replay draws. Preserve the accepted N1 cutoff receipt. Additionally bind the frozen N2/PART_B exact depths and maximum failure cutoffs in the successor's continuation plan. The inspected legacy controller's CUTOFF names N2/PART_B thresholds, while the protected N1 store records N1 assessment cutoffs; these are different records, not interchangeable schemas.

Only legal stage prefixes may commit statistical FAIL: LEGALITY/N1; LEGALITY/N1/N2/PART_B; or all five stages. A passing incomplete prefix is CONTINUE only. N2 and PART_B are always assessed together after the complete joint batch; neither has an independently dispatched retry or early partial-batch verdict. Stop before any later dispatch after a failed stage. Resource failures, missing capture, corrupt evidence and uncertain execution are operational terminal/incomplete states, never fabricated statistical FAIL or PASS.

PR425's `policy.required_output_roles` already recognizes those complete FAIL/full-result shapes, but permits `(completion='PARTIAL', verdict='NONE')` only for LEGALITY/N1. Extend that canonical policy for the passing LEGALITY/N1/N2/PART_B prefix under the new FULL_E1 policy/schema identity. This is a continuation assessment, never aggregate PASS: both N2 and PART_B decisions must be PASS, the service commits their shared capture/assessment once, and only then may it dispatch Part A. Update canonical evidence reconstruction, snapshot parsing, G5 authentication, store transition and consumers together. N1_ONLY retains its existing rejection of this continuation. Missing/failed halves and a prefix omitting PART_B cannot obtain continuation authority.

### 2.4 Statistical and RNG preservation

Reuse `runner._run_stage`, provider/replay/source admission, `regime.domain_seed`, seed identities, and pure `adjudicate_replay_outcomes`/`adjudicate_panel_inventory`. Extract store-free adapters where necessary; do not call `run_production_e1`, `_execute_e1` or construct `ProductionExecutor` for protected work.

N1 runs the contract's FULL/H1/H2 depths. One N2 request supplies FULL at N2 depth and H1/H2 at PART_B depth. N2 failure and speed calculations share the same FULL outcomes; Part B consumes the same captured H1/H2 rows. Assert exact population order, counts, seeds, attempt/release identity and artifact digests. No separate Part B worker, extra FULL speed sample or regenerated path inventory.

Part A uses `contract.replay.part_a` and the same N2 FULL pass rate, recomputed by worker and G5 from captured N2 bytes. Keep the existing disjoint probe namespace and charge that probe to the campaign budget. No extra pilot on recovery.

For initial panel rates, G5 computes inverse ECDF at rank `ceil(percentile * initial_panels)`, clamped to the first rank, using exact Decimal arithmetic. Expansion is required iff `abs(initial_p5 - expansion_center_p5) <= expansion_tolerance`; equality is included. Append indices `[initial_panels, expanded_panels)` only. Final PASS requires final percentile >= expansion_center_p5 and <= that same N2 FULL pass rate. Apply the FULL sanity check after prescribed expansion; an initial sanity excess does not cancel expansion.

Retain panel-major ordered source-session occurrences (duplicates allowed as prescribed by sampling), panel identities, path seed digests and outcomes. The first initial_panels entries of an expanded result must be byte-identical to its retained initial-prefix artifact. G5 rejects reordering, replacement, omitted expansion and unnecessary expansion. Accepted frozen workloads require expanded_panels > initial_panels. Equal panel limits reject at canonical workload validation; the lower-level engine accepting equality does not establish an admissible campaign. No expansion means the initial percentile lies outside the frozen tolerance band, not that the configured limits are equal. All depths, thresholds, namespaces and budgets come from the frozen contract, not copied constants.

The existing compute routine uses float rates before converting the close-call comparison to Decimal; G5 uses exact Decimal rates. Boundary parity tests must prove agreement on supported frozen configurations. If they disagree, stop integration and resolve that engine discrepancy explicitly; do not silently change a threshold, accept disagreement, or introduce a second statistical formula.

Part A remains one dispatched compute operation using the existing append loop. This release does not promise partial-panel resume: interruption before a complete durable capture makes that operation IN_DOUBT. This preserves no-redraw behavior without redesigning the statistical engine.

### 2.5 Durable campaign budget

Create one immutable budget binding at FULL_E1 admission using `contract.replay.budget`; its digest is in all plans, captures, assessments and receipts. Start accounting before campaign-specific source admission/provider work. Cover source proof/pilots, worker computation, capture/serialization, attestation, G5 reconstruction/authentication, service commit work, qseal verification/signing and finalization. No fresh allowance per process, stage, assessment or retry.

Wall budget is elapsed time from persisted campaign start to fixed deadline, including downtime and queues. On the same Linux boot, use a persisted boot ID and CLOCK_BOOTTIME deadline, plus UTC for audit; process restart cannot reset either. A boot-ID change or unusable/regressing trusted clock before completion causes `BUDGET_UNCERTAIN`, blocks new authority and retains history. Cross-boot active continuation is intentionally unsupported in this release. Completed receipts remain readable.

CPU is cumulative trusted supervisor-observed process/cgroup usage, including descendants. Use isolated campaign work processes for G5, seal and service-heavy work so usage is attributable; socket wait time is wall time, not fabricated CPU. Persist reservations before launching each work unit. The sum of settled charges and outstanding maximum reservations cannot exceed the campaign CPU cap. Resolve successful reservations from trusted counters exactly once. If crash cleanup loses a counter, charge the whole reservation; never refund an unknown interval. Poll/enforce the reserved CPU allowance and kill work that exceeds it; any overrun permanently blocks authority. OS CPU-rate limits alone do not enforce cumulative CPU seconds.

Memory is a maximum concurrent campaign footprint, not a sum of peaks. Observe/enforce a common campaign cgroup (or equivalent parent aggregation) for all attributed descendants; separate worker limits cannot each spend the full cap concurrently. Retain peak, OOM events and cgroup identities. Missing trustworthy accounting is fail-closed. Enforce output/storage/frame limits separately using the canonical profile.

The profile defines phase reservation ceilings including verification/finalization, once in a canonical versioned configuration. Admission validates that a feasible route fits the frozen cap; inability to reserve a later phase aborts without draws. Reservations allocate the original allowance and never increase it. Check remaining budget before and immediately at dispatch, assessment commit, full-result commit and seal publication. Deadline reached means no new authority even if computation already passed. Diagnostic cleanup and read-only historical receipt retrieval may continue on separately bounded host resources; they cannot compute, authenticate or sign replacement qualification evidence.

### 2.6 Exact dispatch, restart and retry semantics

Each operation is keyed by `(attempt_id, checkpoint)`; Part A is one checkpoint. A unique constraint plus expected campaign revision serializes concurrent requests. Bind request bytes, parent assessment receipt, plan, source/release identity and budget binding. Same logical request returns the existing status/receipt. A changed digest under the same key is an idempotency conflict.

| Persisted boundary at interruption | Recovery action |
|---|---|
| Request not durably admitted | Retry admission with same identity; no execution existed |
| RESERVED, no START_INTENT | Inspect/clean only owned unstarted container; continue same reservation if valid and budget permits |
| START_INTENT or RUNNING, no complete durable capture | Persist IN_DOUBT before cleanup; stop owned worker; never relaunch this checkpoint |
| Complete CAPTURED including exact output, exit status and runtime facts | Revalidate/archive/sign that capture; never rerun computation |
| ATTESTED, no G5 assessment | G5 reconstructs retained bytes under remaining campaign budget; no draws |
| Durable signed assessment candidate, reply/commit uncertain | Retry exact candidate bytes; recover committed receipt or revalidate and commit that candidate |
| Committed CONTINUE | Dispatch only the next not-started checkpoint using the original budget |
| Committed result or seal, response lost | Return byte-identical receipt plus current validity; no recomputation/new signature |
| VOID, terminal abort, IN_DOUBT or BUDGET_UNCERTAIN | Historical inspection and owned cleanup only; no continuation or sealing |

A merely readable spool file is not a complete durable capture. Recovery requires the accepted N1 capture finalization protocol and content membership; absence of required facts leaves uncertainty. Cleanup failure cannot undo IN_DOUBT or make historical APIs unavailable. No new attempt ID may be allocated automatically to evade exhausted budget or uncertain dispatch; a separately authorized new campaign is outside retry semantics.

G5 may repeat deterministic validation after a crash before a durable signed candidate, charged to the same budget; it may not repeat statistical computation. Persist a canonical signing intent with fixed payload, key ID and signing time before signing. Deterministic signing or a signer idempotency store must recover that exact signature after uncertain responses. An existing signature/receipt is never replaced with fresh time, key or authority.

### 2.7 Evidence and independent G5

Every checkpoint capture attestation binds attempt/checkpoint/execution IDs, frozen contract and trust domain, exact release/image/profile, source/admission evidence, budget identity, plan/seed inventory, predecessor receipt, journal revision/head, captured byte hashes/lengths, exit status and trusted lifecycle/resource observations. Complete output is archived before execution signing. Client-supplied hashes alone establish nothing.

G5 independently derives expected plans from the frozen contract, checks signatures and current enrolled keys, reconstructs PathOutcome values from captured bytes, verifies all ordered counts/digests, re-evaluates decisions using installed pinned pure routines and binds its result to a service snapshot. It validates all prior checkpoint attestations for the aggregate, including N2/PART_B sharing and Part A prefix. A worker's `passed` field is never the adjudication authority. G5 does not rerun stochastic trials.

Aggregate result includes the ordered stage prefix, all checkpoint assessments/attestations, path/panel inventory digests, CUTOFF/continuation binding, budget ledger snapshot and admission/release bindings. The result's precommit snapshot deliberately excludes its own commit receipt to avoid a digest cycle; the commit receipt binds that result plus the resulting journal event. Missing stage/artifact, stale snapshot, wrong signing role/domain or modified source rejects publication.

### 2.8 Protected commit, separate seal, and VOID

Use the service's one durable transactional store for campaign validity, revision, result publication, seal publication and VOID. Candidate outputs remain private until their atomic commit. G5 holds the result key; qseal holds the separate seal key. The execution service verifies both and owns publication receipts.

PR415's atomic VOID/seal ordering, exact authentication binding and historical retry regressions supply reusable semantics and test cases. PR425 retires their legacy public authority route. Port those guarantees to the protected service and separate signer; do not reactivate `qualification/seal.py` authority entry points or regard legacy composition tests as protected Linux acceptance.

For a new full-result commit, within the serialized transaction recheck VALID, current approval/key eligibility, exact expected snapshot/revision, complete accepted prefix, authenticated result/capture membership and remaining budget. Publish result/authentication/artifact membership and one immutable result receipt atomically. A statistical FAIL can be committed as evidence, never sealed.

Only RESULT_COMMITTED_PASS with all LEGALITY/N1/N2/PART_B/PART_A decisions PASS may reach qseal. Before requesting a signature, the service acquires the same campaign transaction lock used by VOID and validates current approval/key eligibility, exact result receipt and budget. qseal independently verifies that committed result/authentication and the service-bound seal intent. Its fixed payload binds attempt, result/authentication/receipt digests, release/domain, seal intent ID, key ID and fixed time. Candidate signature stays private. Recheck validity and budget immediately before atomic publication of seal bytes and receipt. Bound signing duration by remaining budget; signing failure rolls back publication, not the durable idempotency intent.

A durable seal intent is prepared before this locked signing phase. After crash, recovery first looks for its existing receipt/signature and rechecks current validity before publishing anything uncommitted. Never re-sign with different payload/time. A candidate seal signature alone is not an accepted seal: verification requires the committed seal receipt and current service validity. The qseal process cannot publish candidates through another channel.

VOID and both publication transactions have a single observable ordering. If VOID commits first, new result/seal publication fails. If publication commits first, retain its historical receipt; later VOID makes it unusable as current authority. Retry returns the old receipt with `historical=true` and current validity, including VOID/expired approval; it must not misleadingly claim current eligibility. Downstream consumers must check current validity, not treat an offline historical signature as irrevocable authorization. Expiry/revocation checks for new authority occur inside the same critical section; retain the exact policy/key-set revision checked.

## §3 — Alternatives considered

| Alternative | Reason rejected |
|---|---|
| Wrap the legacy caller-controlled controller and attach final signatures | Caller-held store/results do not establish supervised execution |
| Reimplement the statistics in a new campaign runner | Adds divergence without solving authority or lifecycle ownership |
| Separate Part B draw batch or rerun FULL for speed | Violates existing joint-batch sampling and changes the experiment |
| Resume Part A by recreating its worker and skipping panels | Existing engine does not provide durable per-panel execution ownership; uncertain draws could repeat |
| Wait for broker integration before synthetic acceptance | Broker route does not establish this execution boundary and is not its prerequisite |

## §4 — Falsifier and response

If any tested route publishes a new usable result/seal after VOID, repeats a started draw, resets campaign budget on restart, accepts fabricated output, changes panel-prefix identity or accepts incomplete PASS, then reject this release and stop integration/activation. Preserve evidence and amend the design explicitly before rerunning acceptance. Otherwise accept only when every §6 requirement is demonstrated at the selected revision. Check on every candidate release and every change to execution, adjudication, budget, signing, storage or deployment configuration.

## §5 — Forbidden moves

- Reopen caller-controlled production execution to finish N2/Part A after protected N1; the entire campaign must use protected capture.
- Turn interrupted execution into statistical FAIL, redraw under the same attempt, reset an allowance, or allocate a fresh attempt automatically.
- Mint a fresh result/seal on retry, or return a historical receipt without current validity.
- Copy frozen statistical constants into service configuration or adjust expansion thresholds to make synthetic acceptance pass.

## §6 — Acceptance and consequences

**ACCEPT** only after all cases below pass on the exact integrated revision on disposable Linux, with no critical skips and independent combined review closed. **REJECT** if any case fails, evidence is missing, N1 acceptance is absent, or a load-bearing review finding remains. Windows/unit success is development evidence only.

| ID | Executable scenario and required observation |
|---|---|
| E01 | Synthetic genuine PASS: actual protected N1/N2/Part A launches, G5 reconstruction, one full PASS receipt, separate qseal receipt; all TEST_ONLY |
| E02 | Actual N1 failure: authenticated FAIL, no N2/Part A launch, no seal |
| E03 | N2 FULL fails with halves passing; halves fail with FULL passing: one joint batch, both assessments, no Part A, no seal |
| E04 | Part A below floor and above FULL: final FAIL; sanity check applied after any prescribed expansion |
| E05 | Admitted unequal panel limits: no expansion, expansion and inclusive exact tolerance boundary produce correct counts and unchanged expanded prefix with one disjoint pilot. Equal limits and duplicate PART_A depths reject before campaign planning/execution. |
| E06 | Crashes before start intent, after intent, during each worker, after capture, after signing and before/after commit: recovery follows §2.6, actual launch history proves no redraw |
| E07 | Concurrent duplicate submissions/assessments/commit/seal and lost replies: one logical dispatch/receipt; changed payload conflicts; retries recover identical bytes |
| E08 | Exhaust budget during N2, Part A expansion, capture, G5 and sealing; restart between stages and while reservations open; no allowance reset/new authority; host reboot blocks unfinished campaign |
| E09 | Fabricate/alter outcome, signature, seed, panel prefix, source/image, artifact membership or stage order; client cannot write store/read keys/use Docker; every attack rejects |
| E10 | Barrier-controlled VOID races against stage dispatch, result commit and seal; force both orderings; historical receipt remains but current authority never survives VOID |
| E11 | Approval expiry/key revocation before dispatch/commit/seal; retained receipts recover without re-signing; wrong signing role or TEST_ONLY-to-OPERATOR promotion rejects |
| E12 | Service/G5/qseal restart and cleanup failure: historical inspection available, durable uncertainty precedes cleanup, no orphan worker can publish late authority |

Sources for positive and statistical-failure scenarios are deterministic synthetic market/session fixtures replayed through the actual engine; injected completed outcomes are only negative/parser tests. A fixture's expected verdict must be established using the frozen engine before campaign admission; thresholds cannot change after results. Reduced TEST_ONLY contracts may keep host tests practical but cannot stand in for exact-depth production qualification. Include separate parity/boundary tests at supported contract configurations.

Required report: candidate commit and dirty-source hashes, accepted N1 commit/evidence reference, resolved configuration/lock/runtime/image identities, actual UIDs/groups and permission probes, Docker lifecycle events, capture/attestation digests, G5/result/seal receipts, budget reservations/charges, fault injection boundary and both race orderings. Reports must expose failures/skips and cleanup status. Independent review covers the complete behavior, security assumptions, statistical preservation and evidence—not merely separate modules.

The accepted N1 reference must identify the PR425 merge and incorporated foundation (PR415 was not separately merged), including its completed invariant-gate and combined-review evidence. Register E01–E12 as extensions of `tests/ops/qualification/invariant_manifest.json` and the accepted SQL-free lifecycle model; use its exact-test-identity, critical-skip, child-report/hash and recorder/CI validation. Preserve N1 regression coverage when adding campaign transitions. A list of scenario names in this document is not a second manifest or acceptance authority.

Benefit: one auditable campaign with unchanged mechanics. Cost: new durable state/accounting and a seal process; conservative uncertainty loses interrupted attempts. Risks: accounting attribution and lock/signing integration can fail on real hosts; E06/E08/E10 specifically gate those capabilities. Downstream code, harness, CLI/docs and release schemas are assigned in the companion plan; none are claimed updated by this proposal.

## §7 — Implementation plan and trace closure

After accepted Task 1a/1b, the [delegable execution-slice plan](../plans/2026-09-18-full-e1-execution-slices.md) supplies the bounded S1-S8 assignments. The original six-task roadmap below remains the coverage/history map; the successor decomposition does not reduce sections 2 or 6. Future executable releases use fresh budgeted attempts; existing unmetered admission-only campaigns remain historical and are not retroactively charged or activated.

Implement [the companion plan](../plans/2026-09-17-protected-full-e1-campaign.md) as one integrated outcome. Task 1 binds accepted PR425 and its canonical interfaces; Task 2 establishes durable budget/recovery; Task 3 adds controlled stages; Task 4 extends canonical evidence/policy for N2 continuation and aggregate G5; Task 5 ports atomic final commit/seal guarantees to the protected authority; Task 6 extends accepted PR425 Linux invariants and obtains combined review. These are roadmap tasks; a bounded execution handoff selects an outcome after prerequisites are met.

Trace: registered synthetic bundle -> admitted immutable campaign/budget -> N1 capture/assessment -> one joint N2 capture/assessment -> one Part A capture with prefix -> aggregate authenticated result -> atomic publication -> distinct seal intent/signature/publication. Every arrow requires matching predecessor receipt and current service state. FAIL terminates the trace before the next compute arrow. Uncertainty prevents all forward compute arrows; retained capture permits validation only. VOID prevents every new authority arrow. Required capabilities not present in inspected N1: multi-checkpoint campaign store, durable multi-process budget, full G5 artifact reconstruction, qseal runtime and atomic full-result/seal publication.

## §10 — Runnable audit hooks

Run documentation checks from the isolated merged-baseline checkout:

```powershell
.\fp.ps1 doctor
.\fp.ps1 python C:/Users/joshu/.codex/plugins/cache/personal/superpowers/6.3.0+codex.20260918013113/skills/brief-authoring/scripts/check_brief.py docs/superpowers/specs/2026-09-17-protected-full-e1-campaign.md --type adr
rg -n 'E0[1-9]|E1[0-2]|Task [1-6]' docs/superpowers/plans/2026-09-17-protected-full-e1-campaign.md
git show 1e4928360b95812b04725dc1e8da97709d670ff4:ops/c1_rail/qualification/checkpoint_plan.py
git show 1e4928360b95812b04725dc1e8da97709d670ff4:ops/c1_rail/qualification/policy.py
git show 1e4928360b95812b04725dc1e8da97709d670ff4:ops/c1_rail/qualification/journal_snapshot.py
```

Expected: doctor and mechanical checker exit zero, plan maps every E01–E12 case, and committed sources show the shared N1 derivation, N1-only partial assessment shape and canonical snapshot owner described in §0. Initial authoring hashes are historical, not assertions about the current worktree. Task 1 records the merged baseline and accepted evidence; it does not repeat closed N1 repairs. Future executable acceptance commands and files are explicitly proposed in the plan. No Linux full-campaign run is claimed here.

## Verification

Documentation-only deliverable. Mechanical and reference checks are recorded in the delivery note. N1 acceptance is established by §0 evidence. Full-E1 runtime implementation and Linux acceptance remain outstanding.

### Documentation verification recorded 2026-09-17

Main checkout HEAD `c2e6eb2cbe159b60fdff7873b9e96aef943c46df`, with these two new untracked documentation files and pre-existing unrelated changes. `./fp.ps1 doctor` passed: interpreter `C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`, Python 3.13.2, 62 locked packages matched. `./fp.ps1 python C:/Users/joshu/.codex/plugins/cache/personal/superpowers/6.3.0+codex.20260913005651/skills/brief-authoring/scripts/check_brief.py docs/superpowers/specs/2026-09-17-protected-full-e1-campaign.md --type adr` passed 5/5 checks. A launcher-run `python -c` documentation assertion checked all E01–E12 IDs in both documents, six plan tasks, context input binding, reciprocal links, absence of unresolved placeholder markers and trailing whitespace: PASS. The three engine hashes in §10 matched §0. No runtime tests or Linux campaign acceptance ran for this documentation-only change; no complete gate-suite claim is made.


### Earlier PR425 amendment verification (historical)

Documentation-only amendment against main checkout `c2e6eb2cbe159b60fdff7873b9e96aef943c46df`; both successor documents remain local, untracked files. Production-source reads used committed PR425 `6590b61e8d3bb2c2b26d5a47d68951216a3d8835`, excluding the worktree's uncommitted concurrency edits. `./fp.ps1 doctor` passed with `C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe` (Python 3.13.2; 62 locked packages). The §10 mechanical checker at skill version `6.3.0+codex.20260918013113` passed 5/5. Launcher-run documentation assertions passed for six tasks, all twelve acceptance IDs, canonical owner references, consistent plan producer inputs, explicit N2 continuation, reciprocal links and whitespace. Manual contract review traced canonical policy/plan production through captured evidence, G5 continuation, store progression and the extended invariant gate. No runtime code, PR content or PR425 acceptance status was changed; runtime suites and Linux acceptance were not run for this amendment.


### Isolated merged-baseline verification — 2026-09-18

Workspace: `C:/Users/joshu/.codex/worktrees/full-e1-spec-baseline/multi_firm_operations`, detached HEAD `1e4928360b95812b04725dc1e8da97709d670ff4`. Only the two successor Markdown files are new; no tracked runtime files changed. `./fp.ps1 doctor` passed using `C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`, Python 3.13.2, with 62 locked packages matched. `./fp.ps1 python <brief-authoring-skill>/scripts/check_brief.py docs/superpowers/specs/2026-09-17-protected-full-e1-campaign.md --type adr` passed 5/5, using skill version `6.3.0+codex.20260918013113`. The writing-plans `scripts/validate_handoff.py` passed on Task 1 extracted to a disposable temporary file, launched with the same verified interpreter. `./fp.ps1 python %TEMP%/check-full-e1-merged-docs.py` passed revision, six-task, twelve-case, canonical-source, link and whitespace assertions; all twelve acceptance rows remain byte-for-byte equal as text to the original draft. Manual review covered the prerequisite and producer/consumer changes. The original shared-checkout drafts are preserved. No runtime tests, new Linux run, commit, push or PR were performed. The documentation handoff is complete; full-E1 implementation remains unstarted.

### Panel-count contract correction after Task 1a return

The original equal-panel positive scenario is withdrawn as a specification error; E05 now requires rejection of equal limits, preserving the accepted workload policy. At merge `1e4928360b95812b04725dc1e8da97709d670ff4`, `trust_domain.py` requires strictly increasing panel limits and unique PART_A depths; `contract.py` and `policy.py` bind the contract to that workload. `part_a.py` is more permissive at its lower-level request boundary, which is not frozen campaign admission. No production policy, engine, threshold or acceptance evidence has been changed. Inclusive equality at the expansion-tolerance boundary remains required. Earlier verification notes describing unchanged E05 refer to earlier document revisions and do not certify this corrected wording.


## S2 coordinator clarification: attributed resource scope (2026-09-19)

The campaign cap covers attributed process/cgroup resources, not total-machine incremental costs. Include all campaign controllers/guardians, launch clients, workers, descendants and role helpers, and campaign-specific shared-qexec authentication, admission, source proof, planning, serialization, custody, reconstruction and finalization. Include every CPU/memory cost reported by the selected scope without subtraction. Ordinary shared dockerd/system-manager and host kernel/background costs outside that scope are excluded. Only fixed bounded lifecycle requests may use this exclusion: no image building, archive processing or campaign computation may be moved into excluded infrastructure. Platform waits, queueing and downtime consume the original BOOTTIME deadline.

The diagnostic v3 candidate binds this interpretation in canonical `CAMPAIGN_RESOURCE_SCOPE` and its installed profile identity. Its proposed CPU charge is measured final payload cgroup usage plus the entire immutable installed orchestration bound, reserved together before work. A persistent host parent conservatively shares MemoryMax across all included campaigns/controllers, with swap disabled; its peak/OOM observations are never reset between works. Cross-campaign interference and group OOM can invalidate every attempt on that host. This is deliberately conservative and does not establish a whole-host bound. Neither this clarification nor a configured bound proves Linux enforcement; all original fail-closed authority, no-redraw and immutable-charge rules remain. N1_ONLY and accepted S1 history remain unchanged.

The local S2 candidate is INCOMPLETE / NOT ACCEPTED. Identified lifetime-accounting and crash-after-control-claim gaps require follow-up before executable activation. Real Linux evidence is a separate missing prerequisite. No S3 dispatch is authorized.
