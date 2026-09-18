# Qualification structural closure design

Status: DRAFT for review, 2026-09-17. The user requested the design and plan;
this document authorizes no implementation, commit, merge, provisioning, production
qualification, signature, policy admission or deployment.

Baseline: PR 415, `bfad2f187e05980369dbf0e8f75801f621ba998d`, inspected in
`.worktrees/pr415-bounded-repairs`. Remote head was refreshed while drafting.
The implementation coordinator owns acceptance across all boundaries. Existing
worktrees and uncommitted documents are preserved.

Related documents:

- [Structural assessment](../../notes/audits/2026-09-17-pr415-structural-assessment.md).
- [Implementation plan](../plans/2026-09-17-qualification-structural-closure.md).
- [Existing N1 boundary design](2026-09-17-qualification-execution-boundary-design.md).
- [Existing N1 boundary plan](../plans/2026-09-17-qualification-execution-boundary.md).
- [Linux environment plan](../plans/2026-09-17-linux-isolation-test-environment.md).

This is a proposed successor for semantic policy, artifact meaning and acceptance
coverage. It incorporates the N1 boundary's isolation/capture protocol with the
explicit amendments below. It does not silently declare the older proposals
implemented or approved. On approval, update their status headers to reference this
document and apply the amendments before executing their dependent tasks.

## 1. Decision and delivery sequence

Preserve replay, sampling, kernel evaluation, exact statistical decisions and the
accepted risk policy. Replace implicit qualification requirements with executable
policy and evidence contracts, then move execution authority behind the protected
boundary. Verify lifecycle behavior and invariant coverage across that composition.

| Order | Deliverable | Acceptance claim |
| --- | --- | --- |
| 1 | Canonical qualification policy and real legality evidence | The contract describes the required product and prerequisites; source admission cannot invent legality PASS. |
| 2 | Canonical retained evidence and role-to-content validation | Retained artifacts contain exactly the evidence used for the claimed assessment. This alone proves no execution. |
| 3 | Protected N1 launch, capture, attestation and G5 | A real synthetic N1 run reaches protected acceptance; a coherent fabrication cannot. |
| 4 | Lifecycle conformance through real processes | Retry, interruption, VOID and restart preserve one execution and the current acceptance state. |
| 5 | Invariant-based acceptance gate and review closure | Missing required tests, weakened checks and incomplete family dispositions cannot appear accepted. |

Lifecycle guards and tests start with the journal implementation in step 3; step 4
completes cross-process conformance. Likewise, each earlier step includes its own
negative tests; step 5 binds them into the final acceptance gate.

The first independently reviewable slice is step 1. Steps 1 and 2 are library and
synthetic-conformance increments, not runnable production releases. The first
protected release remains N1_ONLY with production execution disabled. Passing N1
means CONTINUE/PARTIAL, never E1 PASS. Actual qualification requires a subsequent
complete N2/Part A execution and cumulative-budget design, implementation and
acceptance. This document reserves its evidence contracts but does not invent
multi-checkpoint execution/recovery capabilities.

## 2. Alternatives and rationale

1. Continue adding local checks to v1. Lowest immediate change count, but leaves
   caller-owned execution and duplicated declarations at the acceptance boundary.
   Useful regressions are retained; this is not the selected architecture.
2. Canonical policy/evidence plus a controlled N1 boundary. Selected: addresses the
   demonstrated semantic and authority failures while preserving computational
   mechanics. Costs include schema migration and a real Linux acceptance host.
3. Rewrite the complete qualification engine or adopt a remote service now. Not
   selected: the evidence does not implicate the entire replay/kernel, and a new
   platform would still need the same product and evidence semantics.

## 3. Governing constraints and trust model

- Keep source loading, sampling, replay, kernel evaluation and exact statistical decisions unchanged except for explicit prerequisite/evidence interfaces defined here.
- Do not change risk constants, lot sizing, accepted policy behavior, RNG formulas, approved depths or no-redraw rules.
- TEST_ONLY reduces fixture workload and uses generated credentials; it does not relax semantic, artifact or provenance checks in the conformance route.
- No automatic migration of active v1/v3 attempts; old artifacts cannot acquire execution attestations retroactively.
- All complete PASS/seal entry points reject in the N1_ONLY release.
- No real qualification starts under the N1_ONLY release.
- Secrets remain outside versioned configuration.
- Use the selected checkout's launcher and lock; do not duplicate dependency versions or bypass environment validation.
- Real Linux process/UID/container evidence is required for isolation acceptance; unavailable critical capabilities are a failed prerequisite, not a passing skip.

Trusted principals are the administrator, OS/container runtime, approved installed
service/G5/worker code and enrolled approval authorities. The requesting client,
its interpreter, paths, objects, clocks, environment and proposed evidence are
untrusted. Approved worker/port correctness remains a code-review assumption;
attestation is not a proof against a malicious approved worker or administrator.

Retain qclient, qexec, worker and qg5 separation from the N1 design. qexec owns
launch/capture/journal and its execution key; qg5 owns adjudication and result key;
worker has neither journal nor credentials. Release enrollment also separates
freeze/result/execution/seal key IDs and actual public-key fingerprints.

## 4. Ground truth and ownership

Rule 0 was applied before drafting: read `core/firm_rules.py`,
`core/dd_geometry.py`, `core/mc/preflight.py`, `ops/c1_rail/book_policy.py` and
`ops/c1_rail/policy_fingerprint.py` at the baseline.

- `book_policy.TIER` selects `Tradeify_Select_100K`; its starting balance comes
  from `FIRM_RULES[TIER]["starting_balance"]`, currently 100000.
- `firm_kwargs(account=...)` intentionally supports a research basis override.
  Preserve that API. Qualification must enforce its narrower product constraint.
- `POLICY_REGISTRY` is pre-admission empty. The canonical validator is
  `policy_fingerprint.validate_registry(source, expected_rows={})`; source
  construction currently does not call it.
- Approved workload comes from the signed trust-domain workload policy and exact
  depth approval. Do not turn fixture N1/N2 counts into new compiled production
  constants. Exact decision probabilities remain Decimal through adjudication.
- Existing source construction owns calendar, population, reviewed source, settings,
  costs and adapter checks. Preserve their real producers and error distinctions.

| Value or decision | Authoritative producer | Consumer |
| --- | --- | --- |
| Fixed semantic policy | Installed release builder resolving canonical code owners | G1, source admission, worker, G5 |
| Workload/budget/attempt permission | Existing signed domain, F1 and depth approvals | Service/worker/G5 at their existing validity points |
| Retained input bytes | Source owners; administrator staging verifies/copies bytes | Worker and pure evidence validators |
| Legality record | Actual source admission + canonical registry check | Worker capture; G5 rechecks static facts and validates admission binding |
| Outcome/path bytes | Approved worker executing the derived plan | Supervisor captures; G5 adjudicates |
| Runtime execution facts | Inspected launch/exit plus labeled worker observations | Attestation verifier; G5 |
| Journal snapshot and current validity | Service-owned SQLite journal | G5 and commit transaction |
| Stage result and output manifest | G5 serialization of verified captured evidence | Result authentication and service commit |
| Current accepted state | Service transaction, serialized against VOID | STATUS and dependent consumers |

## 5. Canonical policy and G1 semantic validation

Add stdlib-only `qualification/policy.py` for closed schemas, stage dependencies,
artifact rules and comparison. Add `policy_sources.py` for release-build resolution
from canonical installed owners. `policy_sources.py` is not imported merely by
importing `contract.py`; listener image imports must remain small and stdlib-only.
If shared canonical JSON helpers are extracted, put them in `encoding.py` and
preserve the exact existing encoding. No new serialization recipe is allowed.

The builder emits `qualification_policy/v1` canonical bytes with exactly:

```text
schema, policy_id = tradeify-e1-pristine/v1
product = {tier, original_basis, state_class = PRISTINE}
pre_admission_registry = EMPTY
stage_order = [LEGALITY,N1,N2,PART_B,PART_A]
stage_populations = {LEGALITY:[],N1:[FULL,H1,H2],N2:[FULL],PART_B:[H1,H2],PART_A:[REGIME]}
checkpoint_groups = {N1:[N1],CUTOFF:[],N2:[N2,PART_B],PART_A:[PART_A]}
stage_artifact_roles = {LEGALITY:legality_result,N1:n1_result,N2:n2_result,PART_B:part_b_result,PART_A:part_a_result}
base_artifact_roles = [attempt_journal,path_inventory,runtime_load_trace]
optional_artifact_roles = [diagnostics_private]
source_owner_sha256 = {book_policy:<digest>,firm_rules:<digest>,policy_fingerprint:<digest>}
```

Numbers requiring exact identity use canonical decimal strings. `original_basis`
is derived at build from the firm rule, never written as a second source constant.
This policy does not copy quantities, protection triggers or scales. Their existing
owners remain pinned runtime dependencies. It also does not contain approvals,
sample depths, environment paths, credentials, release hash or its own hash.

The installed release manifest binds `qualification_policy_sha256` and the source
owner hashes. V2 domain and contract each add `policy_sha256` binding that same
policy digest; policy bytes are
a retained `qualification_policy` input artifact. Consumers require byte equality
with the approved installation's policy, not merely a matching caller hash. The
builder generates policy before release before domain before contract, preventing
digest cycles. Post-build activation uses the exact reviewed release digest.

G1 v2 uses the existing field/type/signature/workload checks plus:

1. Policy, installation, domain and contract identities agree.
2. Initial state is pristine and its basis equals the policy's resolved basis;
   equity/peak equal basis, prior days and prior max-day profit remain zero.
3. Stage shapes/order and joint N2/Part B relationship match policy; N3 remains
   outside E1 acceptance. Workloads still match signed domain/approval.
4. The old mutable `result_plan.required_output_roles` and optional-role overrides
   are absent in v2. `result_plan` contains exactly `policy_sha256` and
   `adjudicator_closure_sha256`. Role requirements derive from policy + assessment.
5. All new semantic/evidence modules belong to the installed component closures.

TEST_ONLY uses the same semantic policy and artifact schemas. Its signed workload,
source/port fixtures and generated role keys differ explicitly; caller flags cannot
select it in an OPERATOR installation. Legacy lightweight unit fixtures remain
useful as tests of isolated helpers but are excluded from conformance acceptance.

## 6. Actual legality evidence

Introduce `legality.py` with no signing or journal authority. Source admission first
verifies retained byte identities and calls the canonical registry validator on
the artifact whose pinned runtime module is `dd_geometry`; role resolution uses
the compiled runtime mapping and rejects zero/multiple matches. Do not scan an
arbitrary live registry or import retained source to inspect it.

Then run existing source construction. After its successful checks, encode a
closed `qualification_source_admission/v1` record containing contract, domain and
policy digests; ordered retained role/hash inventory; FULL/H1/H2 population
digests; effective-settings digest; and fixed success IDs for the checks already
performed (retained identities, calendar/population/provider binding, coverage,
schedule evidence, costs, adapter/settings binding). These IDs are produced in
the successful code path, not accepted as caller-supplied booleans.

`qualification_legality_result/v1` contains exactly schema, contract/domain/policy
digests, geometry source hash, source-admission hash, check ID
`PRE_ADMISSION_REGISTRY_EMPTY`, and status `PASS`. The record exists only when both
the registry check and actual source construction succeed. G5 rechecks the registry
against exact retained bytes and verifies admission/output/contract linkage. The
protected capture establishes which admission ran; pure library validation alone
does not establish provenance.

Malformed, missing or substituted source/geometry fails closed before N1 replay.
The service performs the static registry check before dispatch; a nonempty registry
yields `LEGALITY_REGISTRY_NOT_EMPTY` without a launch. The worker repeats the check
against its exact input snapshot. If a failure is discovered after start, the
already-created dispatch stays consumed and becomes ABORTED; no replay outcome,
CUTOFF or PASS evidence is created. This is not a fabricated statistical E1 FAIL. Retain diagnostic
reason and approved-attempt consumption where applicable. Do not automatically
issue a replacement attempt. Authenticating a LEGALITY-only terminal result is
outside this release, whose accepted terminal prefix remains LEGALITY/N1.

Remove the empty-dict-to-PASS convention from the v2 decision path. The existing
statistical helpers remain unchanged; the v2 adapter requires independently
validated legality plus actual N1 outcome bytes. Changing only a digest, status
label or Python object cannot supply that input.

## 7. Canonical evidence and artifact relationships

Create `evidence.py` for canonical parsing/encoding and semantic comparison. It has
no signer, archive writer or journal access. It operates on bytes, not file paths,
callbacks or caller-owned outcome objects. Internal frozen dataclasses simplify
code; they are never a security capability.

The accepted result is built from verified captured bytes. G5 may also validate a
proposed envelope by reconstructing it and comparing every authoritative field.
Artifact hashes derive from the bytes generated by this reconstruction.

| Role | Canonical contents and required relation |
| --- | --- |
| `legality_result` | Exact legality record, binding captured source admission and retained geometry. |
| `n1_result`, `n2_result`, `part_b_result`, `part_a_result` | `qualification_stage_result/v1`: schema, contract/domain/policy digests, stage, input-plan hash, outcome-array hash, decision and population counts. Decision/counts derive from exact captured outcomes and unchanged rules. |
| `path_inventory` | Exact ordered canonical path inventory used to bind seeds, populations, panel identities and outcome hashes. |
| `runtime_load_trace` | `qualification_runtime_trace/v2`: installed release/profile/image/runtime identities plus exact attestation IDs and captured worker load manifest; checked against launch evidence, not only against a declared role/hash map. |
| `attempt_journal` | `qualification_journal_snapshot/v1`, a logical snapshot of the service journal at one pre-assessment revision; never a mutable SQLite-file hash. |
| `diagnostics_private` | Optional non-authoritative diagnostics with schema/version/attempt binding; cannot satisfy a mandatory role or change any decision. |

The result's `outputs` has sorted entries `{role,sha256,byte_length,privacy:PRIVATE}`.
All mandatory evidence is PRIVATE in this slice. Human/public summaries are derived
outside this authoritative inventory and grant no qualification authority. There
is no client-chosen path: storage uses content hashes and attempt membership.

The closed `qualification_result_envelope/v2` contains exactly:

```text
schema, attempt_id, contract_sha256, trust_domain_sha256, policy_sha256
shared_manifest_sha256, exact_depth_approval_sha256, execution_release_sha256
producer = {service_id,g5_code_sha256,g5_runtime_sha256}
started_utc, completed_utc, completion, verdict, terminal_reason
stage_results = [{stage,status,input_sha256,output_sha256,population_counts}]
outputs = [{role,sha256,byte_length,privacy}]
path_inventory_sha256, runtime_load_trace_sha256
journal_revision, journal_snapshot_sha256
execution_attestations = {N1:<attestation-envelope digest>}
checkpoint_assessment = {checkpoint:N1,decision:CONTINUE|FAILURE}
previous_result_sha256 = null
```

`producer` values derive from the protected release, and times from the verified
execution attestation. `completed_utc` records N1 execution completion even for
PARTIAL campaign progress; it does not mean E1 completion. `terminal_reason` is
`N1_SCREEN_FAILURE` for COMPLETE/FAIL and null for PARTIAL/NONE. There is only one
N1 assessment; previous-result chaining is unsupported and must be null.
`stage_results.output_sha256` equals the corresponding role artifact hash; its
`input_sha256` equals the input-plan identity in that artifact (the legality entry
uses its bound source-admission hash). Counts/status must match that artifact.
LEGALITY has the policy-defined empty population-count map and PASS status.
The three top-level retained-evidence hashes equal their role hashes. This replaces
v1's separate outcome digest/output file declarations with an explicit relationship.
Outcome-array hashes remain inside stage artifacts and bind the captured arrays.

The generic role/prefix schema can describe full E1 for future compatibility tests,
but this closed N1 envelope and its active parser reject non-N1 attestations and
assessments. A complete-campaign envelope extension must be specified and versioned
before enabling those other prefixes in the service.

The role function is deterministic:

```text
required roles = base_artifact_roles + stage_artifact_roles for the executed stage prefix
```

It validates the prefix/decision combination before returning roles:

| Assessment | Stage prefix | Completion/verdict | Release support |
| --- | --- | --- | --- |
| N1 fails | LEGALITY,N1 | COMPLETE/FAIL | N1_ONLY |
| N1 passes | LEGALITY,N1 | PARTIAL/NONE + CONTINUE | N1_ONLY |
| Joint N2/Part B fails | LEGALITY,N1,N2,PART_B | COMPLETE/FAIL | Future complete campaign only |
| Part A completes | LEGALITY,N1,N2,PART_B,PART_A | COMPLETE/PASS or COMPLETE/FAIL | Future complete campaign only |

For N1, mandatory roles are `attempt_journal`, `legality_result`, `n1_result`,
`path_inventory`, `runtime_load_trace`. A failed N1 does not need fictional later
results. The full prefix requires all eight mandatory roles. Unsupported prefixes,
later-stage artifacts in an N1-only result, absent roles, extra roles, duplicate
roles, and a path/role alias are rejected. Full-prefix schema tests do not enable
full-prefix execution or acceptance in the N1 release.

Separate the execution attestation inventory (`plan`, `worker_result`) from these
G5 output roles. The former proves capture; the latter records the adjudicated
interpretation. G5 deterministically projects admission/outcomes/path/runtime facts
from the attested worker frame and binds each output to its correct source. A
digest-consistent unrelated file fails even if all declaration hashes are updated.

## 8. Journal snapshot without a hash cycle

Add `ExecutionStore.snapshot_for_assessment(attempt_id) -> bytes` in the proposed
service store. Under a consistent read transaction it returns schema, attempt,
contract/domain/policy identities, validity, campaign revision, event head, ordered
execution summaries and committed attestation hashes. It creates no journal event.
Use the campaign revision for assessment concurrency; per-execution revisions
remain for launch/capture transitions.

G5 fetches this exact snapshot through the authenticated service connection and
retains it as `attempt_journal`. The v2 envelope includes both `journal_revision`
and `journal_snapshot_sha256`. On first commit, qexec regenerates the logical
snapshot under its writer transaction and compares exact bytes/hash/revision and
validity before appending CUTOFF/assessment events. Fetch/archive membership changes,
STORE_ARTIFACT and STORE_RESULT candidate storage do not advance the campaign revision. A different
outcome-bearing event or VOID does, and makes a new first commit stale.

There is no self-reference: precommit snapshot -> output manifest -> result envelope
-> result authentication -> commit event/receipt. The snapshot excludes its own
digest and future result events. Persisted capture/attestation follows the earlier
design's analogous acyclic chain. Exact committed retries compare the complete
stored request identity before applying first-commit revision checks; they return
the same historical receipt with separately current validity. A new signature,
envelope or stage inventory is a conflict, not an identical retry.

This retry check must also be reachable after approval expiry or VOID. Transport
authorization and exact equality with the already verified stored request are
required, but do not reapply first-acceptance expiry checks to historical receipt
retrieval. The response marks it as historical and reports current validity and
current acceptance-policy eligibility separately; retrieving it grants no new
authority. Protected G5 first checks for a stored assessment and fetches its exact
receipt/envelope/authentication on retry, rather than creating a new signature or
snapshot. For a genuinely new assessment all current-policy checks remain mandatory.

## 9. Protected N1 integration: amendments to the existing design

Retain its dedicated Linux installation, peer-credential socket, fixed image,
read-only input custody, bounded framing, exclusive capture, durable START_INTENT,
CAPTURED-before-signing, signature publication transaction and no-redraw recovery.
Add these amendments before implementing the corresponding old tasks:

1. Release/domain/contract bind the semantic policy. Extend the release's G5/shared
   closure for evidence/legality validation without executing retained worker code.
2. `ExecutionContext` carries validated policy bytes and reconstructed v2 contract.
   Each trusted process reconstructs its own context; no serialized Python objects.
3. Replace the prior statement that successful source construction alone establishes
   LEGALITY with section 6's real registry check and admission record.
4. Worker result frame includes exact admission and legality records, ordered N1
   outcomes, path inventory, runtime load manifest and final budget observations.
   Attested `worker_result` hash binds all of them. Worker still declares no
   authoritative statistical decision.
5. Add read-only `SNAPSHOT {attempt_id}` for qg5. Add qg5-only
   `STORE_ARTIFACT {attempt_id,role,bytes_b64}` to retain bounded proposed G5 output
   bytes. It is not a completion API; role/schema/privacy/attempt membership are
   checked, and no campaign revision or verdict changes. Client cannot call it.
6. `STORE_RESULT` accepts the reconstructed v2 envelope only from qg5 and requires
   all listed artifacts already retained. `COMMIT_N1_RESULT` atomically checks
   snapshot identity, exact capture membership, signature, current key/release/
   approval policy and current validity before recording CUTOFF and assessment.
7. G5 constructs the role-specific artifacts in section 7. Missing/wrong provenance
   is rejected before authentication, even if pure semantic checks pass.
8. The Unix client verifies the server's configured identity as well as the server
   authorizing peer UID. qg5 obtains socket/key paths from protected configuration.
9. Signing installation consumes the existing canonical verification dependency
   configuration; do not implement the old plan's wording as a second literal
   signing-library version pin.

N1 failure produces one accepted terminal failure. N1 CONTINUE records progress
and CUTOFF but launches no N2 and cannot seal. Input or infrastructure failure is
not relabeled statistical failure. Existing expiry-at-start and expiry-at-G5 rules
are preserved, including consumption without retry if approval expires after
authorized launch. Actual host/key compromise remains outside the threat model.

## 10. Lifecycle and failure contract

Use the existing proposed states PENDING, DISPATCHED, START_INTENT, RUNNING,
CAPTURED, ATTESTED, ABORTED and IN_DOUBT, with campaign VALID/VOID independent.
The service is their sole persistent owner; no Python visibility trick supplies
the access boundary. Real OS permissions deny qclient and worker journal access.

| Event sequence | Required observable result |
| --- | --- |
| Duplicate/concurrent submit | One execution ID and at most one actual start; changed bound request conflicts. |
| Crash after START_INTENT or uncertain capture | IN_DOUBT; stop only the exact owned worker; no redraw/start retry. |
| Crash after durable CAPTURED | Sign only stored payload and bytes; no recomputation. |
| VOID before attestation publication | No published completion attestation; capture remains historical/diagnostic. |
| VOID before first result commit | No accepted result or CUTOFF commit. |
| Commit then VOID | Historical receipt retained; current validity VOID; future acceptance/activation unavailable. |
| Lost commit response, exact retry after restart | Same receipt and unchanged event history, with current validity separately reported. |
| Same result with refreshed authentication | Conflict; original authentication/receipt remain unchanged. |
| Output/key/release or approval invalid at acceptance | Reject; no accepted state and no implied retry permission. |
| Full E1 PASS/seal in N1_ONLY | Reject regardless of otherwise consistent signatures/artifacts. |

The complete-campaign sealer remains unimplemented for v2. Its reserved rule is the
existing good pattern: verify the separate sealer signature, then serialize current
validity and exact committed result identity with publication under the same writer
lock as VOID. No step may claim future v2 sealing accepted based on legacy tests.

## 11. Migration and release boundaries

Use the already proposed domain/v2, contract/v2, result-envelope/v2 and service DB
schema v4; add the policy/evidence fields before these drafts become released wire
formats. Verify whether any successor has shipped before assigning versions.
If v2 has been released, increment rather than reinterpret accepted bytes.

During steps 1 and 2, new functions return inspected semantic evidence, not an
active result. Their library tests establish the new boundary behavior; wiring
them into the signed v2 G1/service/G5 route is mandatory in step 3 and is part of
combined acceptance. Preserve existing v1 parsers for historical inspection and mechanics
regressions. At step 3 cutover, active public v1 execution/authentication/commit/seal
entry points reject with `LEGACY_QUALIFICATION_INSPECTION_ONLY`; independent
read-only verification of historical signatures remains available. Do not provide
an `allow_legacy`, skipped-attestation or same-process production fallback.

N1_ONLY installation refuses all OPERATOR execution and all complete PASS/seal
requests. OPERATOR schema and rejection tests use generated keys without running
production workloads. Existing v1 campaigns are retained read-only; failure to
install the new service leaves active qualification unavailable. No automatic
rollback to weaker acceptance. The currently paused PR remains paused throughout
the preparatory slices.

Deployment-image dependency closure is part of integration: `contract.py` and
`trust_domain.py` are copied into listener/daemon images. Add any new stdlib parser
dependency to both Dockerfiles, `.dockerignore` and image-validation inventories,
or keep it lazily outside their import path. Never add worker/service/signing code
or private ports to those images merely to make an import pass.

## 12. Invariant acceptance and independent evidence

Maintain `tests/ops/qualification/invariant_manifest.json`, a closed array of
`{id,requirement,owner,producer,consumer,test_nodeids,evidence_kind}`. The manifest
organizes coverage; it never defines production policy. CI checks collected test
IDs, expected execution and zero critical skips using the existing recorder/JUnit
bridge. It cannot prove semantic adequacy from a name; reviewer inspection and
targeted mutation checks provide that part.

| ID | Required evidence |
| --- | --- |
| QPOL-01 | Resigned wrong product basis and placeholder output policy rejected; valid nearby case accepted. |
| QLEG-01 | Retained nonempty registry rejected through source admission; no N1 dispatch; valid empty registry produces bound evidence. |
| QART-01 | Coherently substituted output files fail role-to-content comparison; terminal-prefix role inventories accepted/rejected correctly. |
| QPLAN-01 | Exact vectors for all existing seed/probability consumers; coherent namespace/population substitutions rejected. |
| QEXEC-01 | Real losing/passing N1 through service and G5; client fabrication and mutable Python objects cannot authorize completion. |
| QKEY-01 | Both key ID and public-key alias separation at enrollment and consuming boundaries. |
| QSTATE-01 | Real process interruption/restart, duplicate submission, retry identity and both VOID/commit orderings. |
| QISOL-01 | Real qclient/worker denied key/journal/socket/code writes; exact installed identities captured. |
| QGATE-01 | V1 bypass, missing attestation, OPERATOR execution and full PASS/seal rejected by N1_ONLY. |

Acceptance uses production evidence schemas with generated keys, synthetic sources
and signed reduced workload. It has no callback that manufactures replay outcomes,
no alternate role inventory and no fixture-created completed execution. Pure unit
fixtures may create such records only in tests labeled consistency-only.

Targeted mutations disable basis validation, registry validation or artifact
comparison one at a time in a disposable test copy. The corresponding invariant
test must fail for its intended assertion, not import/setup failure. Expected
values for seeds/cutoffs and simple byte vectors are independent fixtures, not
computed by the production helper being tested. No new mutation framework is
required for the first slice.

For each review finding, record trigger, violated invariant, related stage/entry
points and disposition in the existing PR/audit. The integration owner verifies
the producer-to-consumer trace and regression family before requesting another
independent review. A green unit suite or one repaired example does not close an
unimplemented producer, Linux prerequisite or unsupported checkpoint.

## 13. Acceptance traces and limits

1. Signed contract with basis 50000 -> G1 semantic rejection -> no source execution.
2. Valid contract with a signed retained nonempty geometry registry -> registry
   rejection during actual admission -> no N1 result; attempt disposition retained.
3. Valid synthetic inert ports -> real replay -> captured UNRESOLVED N1 outcomes ->
   G5 FAIL artifacts -> atomic result commit -> identical receipt after restart.
4. Valid trading fixture -> real N1 -> CONTINUE/PARTIAL -> no N2 dispatch or seal.
5. Valid file hashes but unrelated `n1_result` bytes -> semantic mismatch -> no
   authentication/commit, even when the manifest is rehashed consistently.
6. Valid capture + precommit snapshot -> VOID wins writer lock -> commit rejected;
   reverse ordering retains historical result then marks current validity VOID.
7. Exact lost-response retry -> return stored receipt before first-commit revision
   check; changed authentication -> conflict; neither adds an execution.

Production dependencies remain owned by the operator/source/release teams:
approved full campaign capability, real source acceptance, actual isolated host,
keys, F1/depth approvals and budgets. The Linux environment plan supplies test-host
reproducibility and cleanup, not the execution service. No new infrastructure
provider or spend is assumed. This design reduces the identified failure families;
it does not promise elimination of all possible defects.
