# Qualification Structural Closure Implementation Plan

> **For agentic workers:** Execute with superpowers:executing-plans; use superpowers:subagent-driven-development when bounded delegation is useful and authorized. Preserve the behavioral contract and integration owner. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make qualification policy, retained evidence, protected N1 execution and lifecycle acceptance enforce the same explicit invariants.

**Architecture:** Canonical semantic policy and evidence libraries feed a protected N1 supervisor/worker/G5 route. The service owns execution and journal state; G5 reconstructs artifacts from captured bytes and commits against an exact logical snapshot. Independent conformance and lifecycle tests close the demonstrated review families.

**Tech Stack:** Existing Python operations environment and dependency lock, canonical JSON and Ed25519 helpers, Decimal, SQLite, pytest, Linux peer credentials and Docker as specified by the existing N1 boundary design.

**Spec:** [Qualification structural closure design](../specs/2026-09-17-qualification-structural-closure-design.md). Executors also read the linked N1 boundary design/plan and Linux environment plan with the amendments in this spec.

## Global Constraints

- Keep source loading, sampling, replay, kernel evaluation and exact statistical decisions unchanged except for explicit prerequisite/evidence interfaces defined here.
- Do not change risk constants, lot sizing, accepted policy behavior, RNG formulas, approved depths or no-redraw rules.
- TEST_ONLY reduces fixture workload and uses generated credentials; it does not relax semantic, artifact or provenance checks in the conformance route.
- No automatic migration of active v1/v3 attempts; old artifacts cannot acquire execution attestations retroactively.
- All complete PASS/seal entry points reject in the N1_ONLY release.
- No real qualification starts under the N1_ONLY release.
- Secrets remain outside versioned configuration.
- Use the selected checkout's launcher and lock; do not duplicate dependency versions or bypass environment validation.
- Real Linux process/UID/container evidence is required for isolation acceptance; unavailable critical capabilities are a failed prerequisite, not a passing skip.

Status: IMPLEMENTING under the subsequent user handoff. Baseline PR415 `bfad2f187e05980369dbf0e8f75801f621ba998d`.
The implementation coordinator owns combined acceptance. No agent dispatch or
implementation is authorized by this draft. User requested documents, not code.

## Scope and sequencing

Execute in the recommended order: Tasks 1-2 semantic policy/legality; Tasks 3-4
evidence; Tasks 5-7 protected N1; Task 8 lifecycle conformance; Task 9 invariant gate.
These are reviewable increments of one outcome. Library acceptance in Tasks 1-4
does not activate v2, authorize v1 production use or close execution provenance.

Task 5 incorporates the existing N1 plan Task 1. Task 6 incorporates its Tasks 2-5.
Task 7 incorporates its Task 6. Tasks 8-9 incorporate and extend its Task 7. Apply
this spec's amendments first; do not execute two conflicting plans independently.
Existing implementation prototypes are inputs to review, never presumed accepted.

At execution time, refresh remote PR/main and relevant worktree state; create a
fresh isolated worktree with `superpowers:using-git-worktrees`. Preserve existing
prototypes, dirty main, unrelated artifacts and independently owned worktrees.
Confirm no successor released the proposed v2 schemas; increment versions if it did.
Run the new checkout's `./fp.ps1 doctor` before Python. Record actual interpreter,
baseline revision and relevant baseline failures. Reuse the baseline audit probes
only as reproduction references; permanent tests belong in the implementation tree.

Each task: write the specified rejection and nearby positive tests, run the focused
selection to establish its failure, implement the contract, rerun the affected
selection, inspect evidence, and review the full behavior before proceeding.
Commit only under implementation/commit authorization then in force. A suggested
commit boundary is the completion of each numbered task; PR publication is separate.

## Shared interfaces

All interfaces below are proposed, not claims about existing code. The existing
`ValidatedFrozenContract`, `ProductionSource`, statistical helpers and runtime
inventory are read at the selected revision before adapting call sites.

```python
# qualification/policy.py -- standard library only
@dataclass(frozen=True)
class QualificationPolicy:
    canonical_bytes: bytes
    sha256: str
    tier: str
    original_basis: Decimal

def parse_policy(raw: bytes) -> QualificationPolicy: ...
def validate_contract_semantics(document: dict, policy: QualificationPolicy,
                                *, workload_policy) -> None: ...
def required_output_roles(policy: QualificationPolicy, *, stages: tuple[str, ...],
                          completion: str, verdict: str) -> tuple[str, ...]: ...

# qualification/policy_sources.py -- installed build-time canonical owners
def build_qualification_policy() -> bytes: ...

# qualification/legality.py -- pure bytes verification
def verify_static_legality(*, contract_sha256: str, domain_sha256: str,
                          policy: QualificationPolicy,
                          geometry_bytes: bytes,
                          expected_geometry_sha256: str) -> None: ...
def build_legality_record(*, contract_sha256: str, domain_sha256: str,
                         policy: QualificationPolicy, geometry_bytes: bytes,
                         expected_geometry_sha256: str,
                         source_admission_bytes: bytes) -> bytes: ...

# qualification/source_admission.py -- calls the existing real source factory
@dataclass(frozen=True)
class AdmittedSource:
    source: ProductionSource
    source_admission_bytes: bytes
    legality_bytes: bytes

def admit_source(contract: ValidatedFrozenContract, *, artifact_root: Path,
                 policy: QualificationPolicy) -> AdmittedSource: ...

# qualification/evidence.py -- pure consistency, no signing or persistence
@dataclass(frozen=True)
class InspectedEvidence:
    envelope_bytes: bytes
    output_bytes_by_role: Mapping[str, bytes]

def build_stage_artifact(*, contract, policy: QualificationPolicy, stage: str,
                         input_plan_sha256: str, outcome_bytes: bytes,
                         path_inventory_bytes: bytes,
                         prior_stage_outcomes: Mapping[str, bytes]) -> bytes: ...
def build_n1_evidence(*, contract, policy: QualificationPolicy,
                      worker_result_bytes: bytes, plan_bytes: bytes,
                      execution_attestation_bytes: bytes,
                      journal_snapshot_bytes: bytes,
                      installed_release_bytes: bytes) -> InspectedEvidence: ...
def compare_n1_evidence(proposed: InspectedEvidence, *,
                        expected: InspectedEvidence) -> None: ...
```

Ellipses in this interface block are signature notation, not implementation stubs.
Concrete behavior is specified in the tasks and spec. `QualificationPolicy` stores
only these convenience properties; other policy data is parsed from its canonical
bytes through private helpers. `workload_policy` is the existing
`QualificationWorkloadPolicy`; semantic validation reads its named fields.

`InspectedEvidence` deliberately has no accepted/authorized flag. Its builder checks
internal structure/bindings, but does not authenticate an execution. Task 7's protected
G5 verifies original signatures/custody/current policy before invoking it and signing
the resulting exact bytes. Passing an `InspectedEvidence` object to a signer is not
an available API.

Use the old N1 plan's `ExecutionContext`, `ArtifactBytes`, `VerifiedExecution`,
`ValidatedEvidence` and `ExecutionStore` with these explicit extensions:

```python
# Added ExecutionContext fields; existing validated release/domain/contract remain.
policy: QualificationPolicy

# Added VerifiedExecution field (computed after verification, not client data).
worker_result_bytes: bytes

# Added ValidatedEvidence fields, alongside result_bytes, attestation_sha256,
# n1_decision and expected_revision from the old plan.
output_bytes_by_role: Mapping[str, bytes]
journal_snapshot_sha256: str

# Added methods to service-private execution/store.py
snapshot_for_assessment(attempt_id: str) -> bytes
store_proposed_artifact(attempt_id: str, role: str, payload: bytes) -> str  # digest
```

Rename the earlier draft's `VerifiedExecution.result_bytes` to
`worker_result_bytes` and update all callers together. There are no wire aliases
or dual sources of authority. `ValidatedEvidence.expected_revision` is always a campaign revision.

## Task 1: One policy rejects the wrong product and evidence requirements

**Outcome:** A deterministic policy built from the canonical owners rejects wrong
product initial state, substituted policy bytes and caller-chosen output requirements.
This is the first independently deliverable semantic-library slice.

**Owner and dependencies:** Coordinator owns product semantics. Existing
`book_policy.TIER`, `FIRM_RULES`, signed workload and canonical JSON are inputs.
Task 5 wires this same library into the new signed G1 path; no active authority is
claimed before then.

**Files:** Create `ops/c1_rail/qualification/policy.py`, `policy_sources.py`,
`tests/ops/qualification/test_semantic_policy.py`, and
`tests/ops/qualification/semantic_fixture.py`. Modify `contract.py` only if extracting
its unchanged encoder/parser to new stdlib-only `encoding.py`; update imports and
image closure together in that case. Read `core/firm_rules.py`, `book_policy.py`,
`trust_domain.py` and `test_contract.py` first.

**Interfaces:** Produces `build_qualification_policy`, `parse_policy`,
`validate_contract_semantics`, `required_output_roles` from the shared interface.

- [x] Define `semantic_fixture.semantic_case() -> tuple[dict, QualificationPolicy, QualificationWorkloadPolicy]`.
  Start with existing `test_contract._document()` and its workload fields; project
  the proposed v2 policy/result-plan fields exactly as spec section 5. Generate policy
  from installed code. This helper supplies parsed semantic inputs, not signatures
  or source-execution proof. Keep an independently written wrong-basis test:

```python
def test_pristine_50k_cannot_describe_fixed_100k_product():
    document, policy, workload = semantic_case()
    for field in ('original_basis', 'current_equity', 'historical_eod_peak'):
        document['initial_state'][field] = '50000'
    with pytest.raises(ValueError, match='PRODUCT_BASIS_MISMATCH'):
        validate_contract_semantics(document, policy, workload_policy=workload)
```

- [x] Add valid 100000, zero/negative/wrong-shaped fields, nonpristine state, changed
  stage populations/order, removed Part B and unknown/placeholder result-plan roles.
  Reject bool-as-number and nonfinite values through existing strict parsers.
- [x] Build policy in dependency order: read tier from `book_policy.TIER`; read its
  firm starting balance; hash exact installed owner files; emit the closed document
  from spec section 5 with the existing canonical encoder. The builder takes no
  caller tier, role-list or balance override.

```python
tier = book_policy.TIER
basis = Decimal(str(FIRM_RULES[tier]['starting_balance']))
if not basis.is_finite() or basis <= 0:
    raise ValueError('INVALID_CANONICAL_PRODUCT_BASIS')
# Populate product from tier/basis; all remaining keys follow spec section 5.
# Consumers compare parsed initial state to this resolved basis before issuance.
```

- [x] Implement exact policy schema and semantic relations; require
  `document['policy_sha256'] == policy.sha256` and
  `document['result_plan']['policy_sha256'] == policy.sha256`; reject obsolete role
  overrides. Compare workload fields to the signed workload object without baking
  test depths or probabilities into policy.
- [x] Implement prefix/role mapping from the policy, including N1 FAIL and
  CONTINUE as spec section 7. The function recognizes future full prefixes for
  schema tests; supported-release enforcement belongs to Task 7.
- [x] Prove the valid policy matches canonical code and a deliberately changed
  generated policy fails comparison with installed expected bytes. Keep fixed
  expected stage/role vectors independent of the role-producing helper.

Run: `./fp.ps1 python -m pytest tests/ops/qualification/test_semantic_policy.py tests/ops/qualification/test_contract.py tests/ops/qualification/test_trust_domain.py -q --tb=short`.

**Exit:** All semantic cases have the intended rejection reason and nearby positive
case; no risk/source constants changed; no producer-local second role inventory.

## Task 2: Actual source admission produces legality evidence

**Outcome:** Retained nonempty registry prevents replay; an admitted source carries
an exact, reproducible legality record and source-admission record.

**Owner and dependencies:** Source admission owns actual source checks; canonical
registry validator owns registry semantics. Task 1 policy and existing
`ProductionSource._build_domain` supply inputs. qexec/worker integration in Tasks
5-7 consumes these same functions.

**Files:** Create `qualification/legality.py`, `source_admission.py`,
`tests/ops/qualification/test_legality_evidence.py`. Read production source's
`_prepare_domain_inputs`, retained trace, source factories and `verify_for`.
Modify `production_source.py` only for a bounded shared prepared-input helper if
needed; do not duplicate source parsing or skip any current check.

**Interfaces:** Produces `verify_static_legality`, `build_legality_record`,
`admit_source` and `AdmittedSource` as specified above.

- [x] Write canonical registry tests using bytes, not monkeypatching the live
  `POLICY_REGISTRY`. Use an existing valid row/provenance AST fixture from
  `tests/ops/test_policy_fingerprint.py` for the nonempty case; hash its exact bytes.

```python
def test_bound_nonempty_registry_is_not_legality_pass(nonempty_geometry_bytes):
    policy = parse_policy(build_qualification_policy())
    raw = nonempty_geometry_bytes
    with pytest.raises(ValueError, match='LEGALITY_REGISTRY_NOT_EMPTY'):
        verify_static_legality(contract_sha256='a' * 64,
            domain_sha256='b' * 64, policy=policy, geometry_bytes=raw,
            expected_geometry_sha256=hashlib.sha256(raw).hexdigest())
```

- [x] Define `nonempty_geometry_bytes` in the new test file by adapting that existing
  parser fixture. It is a source-byte fixture only; it grants no approval.
  Add missing/wrong digest, malformed source, multiple geometry-role matches and
  valid empty registry. Separate malformed source from confirmed nonempty contents.
- [x] Resolve geometry by the validated runtime role-to-module mapping for
  `dd_geometry`. Verify bytes against frozen identity, call
  `validate_registry(raw, expected_rows={})`, then invoke real source construction.
  Admission must use exact retained bytes shared with source construction; a fresh
  unrelated read after validation is not an acceptable binding.
- [x] Build source-admission bytes only after successful existing factory checks.
  Derive role hashes from `source.prepared.load_trace`/`retained_bytes`; derive
  population hashes from the exact ordered contract/source populations. Then build
  legality bytes from that admission hash and the actual checked geometry bytes.
- [x] If avoiding a second source read requires a factory change, extract
  `_build_from_prepared(contract, prepared, *, domain)` inside `production_source.py`.
  Existing `_build_domain` calls `_prepare_domain_inputs` then this helper;
  `admit_source` verifies static legality on that same `prepared` inventory and
  calls this helper. `prepared` is the existing `PreparedProductionInputs`, produced
  by `_prepare_domain_inputs`; verify its contract/domain and retained hashes at
  consumption. This is internal reuse, not a public caller-supplied prepared-source
  capability. Keep all existing checks and source issuance in the extracted body.
- [x] Use the existing signed composition builder to construct a real valid source
  and verify both records. Add a resigned retained-source case with nonempty geometry
  that fails through `admit_source` before any replay provider is created. The signed
  byte identities must be coherent so the intended semantic failure is reached.
- [x] Change a source input to trigger an existing source validation failure and
  assert no legality PASS record is returned. Do not convert missing source context
  or parser failures into statistical FAIL.

Run: `./fp.ps1 python -m pytest tests/ops/qualification/test_legality_evidence.py tests/ops/test_policy_fingerprint.py tests/ops/qualification/test_production_source.py -q --tb=short`.

**Exit:** A real source admission owns the evidence producer; empty evidence has no
PASS meaning. Direct legacy factory calls do not become a v2 acceptance path.

## Task 3: Retained artifact roles are projections of actual evidence

**Outcome:** The canonical role manifest and each stage artifact reflect the exact
outcomes and input identities; unrelated bytes with matching declarations fail.

**Files:** Create `qualification/evidence.py`,
`tests/ops/qualification/test_evidence_artifacts.py`; extend `semantic_fixture.py`.
Read `result_adjudication.py`, `orchestration.py`, `seal.py` and the existing
`composition_result_fixture.py`. Keep legacy mechanics helpers; do not import
G5/signing/store into the pure evidence module.

**Interfaces:** Produces `build_stage_artifact` and role-content comparison used by
`build_n1_evidence` in Task 4. All documents use spec section 7's closed schemas.

- [x] Write a parameterized role test for both N1 terminal/progress cases and the
  future complete prefix. N1 requires exactly five mandatory roles; complete E1
  requires eight. Test all single mandatory-role omissions and all later-stage
  additions to N1. No fixture-specific `private-result` role is accepted.

```python
@pytest.mark.parametrize('completion,verdict', [('COMPLETE','FAIL'),('PARTIAL','NONE')])
def test_n1_prefix_requires_real_evidence_roles(completion, verdict):
    policy = parse_policy(build_qualification_policy())
    assert required_output_roles(policy, stages=('LEGALITY','N1'),
        completion=completion, verdict=verdict) == (
        'attempt_journal','legality_result','n1_result','path_inventory','runtime_load_trace')
```

- [x] Normalize captured outcome arrays using the existing exact outcome fields,
  preserving ordering and diagnostics. Compute counts and outcome hash from these
  bytes. Adjudicate through unchanged Decimal statistical helpers; do not accept
  a caller decision argument to `build_stage_artifact`.
- [x] Bind stage input-plan digest, policy/contract/domain identity and path inventory.
  `prior_stage_outcomes` is empty for N1; later schema tests supply the exact earlier
  stage arrays, including N2 FULL outcomes needed for the Part A sanity comparison.
  Reject absent or incompatible prerequisite arrays. For Part A schema tests preserve panel-major ordering, exact inverse-ECDF behavior
  and expansion rules; do not introduce active Part A execution support.
- [x] Build a correct N1 result, replace its contents while recomputing the manifest
  hash/length, and require semantic mismatch. Cover swapped stage roles, altered
  population order and unrelated runtime trace. Include valid byte-for-byte artifacts.
- [x] Assert source legality must parse/verify and cannot be replaced by `{}` or
  a claimed PASS. Keep each rejection reason specific to the violated relationship.

Run: `./fp.ps1 python -m pytest tests/ops/qualification/test_evidence_artifacts.py tests/ops/qualification/test_result_adjudication.py tests/ops/qualification/test_checkpoint_validation.py tests/test_certification_power.py -q --tb=short`.

**Exit:** The semantic library compares artifact meaning, not just internal hash
consistency. Shared production helpers retain independently specified expected vectors.

## Task 4: Acyclic snapshots and reconstructed result envelopes

**Outcome:** Given captured bytes and one logical journal snapshot, the pure builder
produces exactly one N1 envelope/artifact set; changes to any authoritative input
are detected. It still provides no execution authority.

**Files:** Extend `qualification/evidence.py`; create
`qualification/journal_snapshot.py`, `tests/ops/qualification/test_journal_snapshot.py`,
`tests/ops/qualification/test_evidence_reconstruction.py`.

**Interfaces:**

```python
# journal_snapshot.py -- serializer/parser only, no DB access
def encode_assessment_snapshot(*, attempt_id: str, contract_sha256: str,
    trust_domain_sha256: str, policy_sha256: str, validity: str,
    campaign_revision: int, event_head: str,
    executions: tuple[dict, ...]) -> bytes: ...
def parse_assessment_snapshot(raw: bytes) -> dict: ...
```

Each execution entry contains exactly checkpoint, execution_id, execution_revision,
state, plan_sha256 and attestation_sha256. Sort by policy checkpoint order;
reject duplicate checkpoints, missing identities and incompatible state/hash pairs.
Snapshot objects describe state, not signature authority; only the real service
produces authoritative snapshots in Task 6.

- [x] Write fixed snapshot-byte vectors, including VOID, duplicate execution and
  wrong attempt rejection. Explicitly exclude future commit, envelope and snapshot
  self-digests. Keep the serializer's own expected vector handwritten.
- [x] Implement `build_n1_evidence` from the shared interface: check plan/outcome/
  legality/runtime/attestation structural bindings; derive stage decision; derive
  required roles; serialize snapshot and stage artifacts; construct the exact closed
  v2 envelope in design section 7. Stage output hashes now identify the role artifact;
  outcome-array hashes live inside it. Derive producer/times from protected release
  and captured attestation, not the current client clock. N1 completion time does
  not imply campaign completion. Reject previous-result chaining in this release.
- [x] Implement `compare_n1_evidence` as exact envelope byte equality plus exact
  role-to-bytes equality after strict parsing. No overloaded Python equality or
  subclass-controlled field influences acceptance.

```python
def test_consistently_rehashed_artifact_is_not_equivalent(inspected_n1_case):
    expected = inspected_n1_case
    outputs = dict(expected.output_bytes_by_role)
    outputs['n1_result'] = b'{"unrelated":true}'
    document = json.loads(expected.envelope_bytes)
    entry = next(row for row in document['outputs'] if row['role']=='n1_result')
    entry['sha256'] = hashlib.sha256(outputs['n1_result']).hexdigest()
    entry['byte_length'] = len(outputs['n1_result'])
    forged = InspectedEvidence(canonical_json_bytes(document), outputs)
    with pytest.raises(ValueError, match='EVIDENCE_SEMANTIC_MISMATCH'):
        compare_n1_evidence(forged, expected=expected)
```

`inspected_n1_case` is a new consistency-only fixture in the test file using Task 2
source admission, deterministic sample outcome bytes and a schema-valid fixture
attestation/snapshot. Its tests do not claim protected execution or sign production
results. Task 7 replaces its producers with actual capture for acceptance tests.

- [x] Test runtime, journal and legality substitutions, missing/surplus output roles,
  malformed JSON and wrong counts. Include both FAIL and CONTINUE from real mechanics
  fixtures where available; invalid supplied verdict cannot override reconstruction.
- [x] Ensure the pure module cannot import execution signer/service/archive/store.
  Record library completion separately from the active-boundary acceptance status.

Run: `./fp.ps1 python -m pytest tests/ops/qualification/test_journal_snapshot.py tests/ops/qualification/test_evidence_reconstruction.py tests/ops/qualification/test_evidence_artifacts.py -q --tb=short`.

**Exit:** Acyclic identity trace reviewed from snapshot to artifacts to envelope;
no mutable database-file hash and no in-memory authority claim.

## Task 5: Bind semantic policy into signed v2 G1 and release admission

**Outcome:** The active route cannot enroll or dispatch a contract that avoids Tasks
1-2. Signed malicious-but-consistent values fail before worker launch.

**Files and interfaces:** Execute existing N1 plan Task 1's `execution/{protocol,
profile,plan,admission,verification}.py` work and its release/domain/contract/preflight
schema changes. Extend `ExecutionContext.policy`; add policy artifact/digests to
release, domain, contract, and plan identity; add tests
`tests/ops/qualification/execution/test_semantic_admission.py`.

**Behavioral contract:** Installed release builder is the expected-policy producer;
freeze/depth authorities retain their existing roles. `verify_bundle` must invoke
Task 1 semantic validation and Task 2 static legality against immutable staged bytes.
The client never selects policy implementation, image or trust roots.

- [ ] First add signed OPERATOR-schema wrong-basis and role-override tests using
  generated distinct keys. A fixture signer re-signs the changed contract and domain
  as necessary; do not accept signature rejection as the intended semantic result.
  Confirm valid signed fixture returns a reconstructed v2 contract/context.
- [ ] Implement the closed v2 result-plan shape and policy digest binding; verify
  original signatures, exact byte identities and semantic constraints before receipt
  issuance. Compare policy bytes to the installed approved release's policy bytes.
- [ ] Reuse old Task 1 plan derivation and fixed vectors. Ensure semantic policy,
  initial state, probe, source-proof work and exact budget identities are bound.
  No new stream addresses or proof workloads are introduced.
- [ ] Check registry statically before reservation/launch and recheck in worker
  admission. Tests assert launch count zero for a coherent nonempty-registry bundle.
- [ ] Include new policy/evidence/registry-validator dependencies in actual G5,
  supervisor and worker closures. Resolve listener/daemon stdlib import packaging
  using exact COPY/ignore/inventory changes if required, never by broad directory copy.
- [ ] Preserve disjoint key ID/public-key rules at every v2 enrollment/consumer.
  Installation selects authority class; mixed TEST_ONLY/OPERATOR evidence fails.

Run the existing N1 Task 1 focused command plus
`./fp.ps1 python -m pytest tests/ops/qualification/execution/test_semantic_admission.py tests/ops/qualification/test_semantic_policy.py tests/ops/qualification/test_legality_evidence.py -q --tb=short`.

**Exit:** Signed v2 validation reaches the same semantic library tested in Tasks 1-2.
No production execution is enabled. Build identity and policy hash are retained.

## Task 6: Protected capture and journal own execution facts

**Outcome:** A real isolated worker executes N1 once; qexec captures and attests it,
and supplies stable logical snapshots without caller completion authority.

**Files/interfaces:** Implement existing N1 plan Tasks 2-5's store, compute, budget,
worker, launcher, archive, service, signing, release, CLI and deployment files. Add
the shared snapshot/store interfaces above and service operations from spec section 9.
Extend existing planned tests `execution/test_store.py`, `test_service.py`,
`test_worker.py`, `test_archive.py` and Linux boundary integration fixtures.

**Owner:** qexec owns journal/capture; worker owns observations only. Linux host setup
and cleanup come from the separate environment plan; do not provision a substitute
host or treat Docker Desktop tests as UID isolation acceptance.

- [ ] Implement the existing START_INTENT/CAPTURED/ATTESTED transactions and real
  worker profile. Use Task 2 `admit_source` in worker; source-admission and legality
  bytes travel inside the attested worker frame. Reject final budget excess and
  incomplete capture as specified by the existing design.
- [ ] Implement `snapshot_for_assessment` under a SQLite read transaction using
  Task 4 serializer. Snapshot from stored campaign/execution values only, not client
  summaries. Do not increment campaign revision on reads or artifact storage.
- [ ] Add qg5-only SNAPSHOT/STORE_ARTIFACT handlers and bounded artifact parsing.
  STORE_ARTIFACT returns its digest; bytes remain candidate evidence until commit.
  Role, privacy, length, hash and attempt membership checks occur before storage.
  qclient cannot call either write operation or supply journal/credential paths.
- [ ] Make candidate artifacts invisible to ordinary fetch until committed as result
  membership. qg5 may refetch its candidates; aborted candidates can remain private
  garbage for administrator-owned cleanup. Never overwrite an object at a digest.
- [ ] Server obtains peer UID from the socket; client checks server UID against
  protected instance configuration. Add wrong-server/wrong-peer rejection cases.
- [ ] Resolve the prior plan's signing dependency instruction by consuming canonical
  requirements; record actual installed versions, no second literal pin.

```python
def test_snapshot_read_and_candidate_storage_do_not_change_campaign(store_case):
    store, attempt_id, role, artifact_bytes = store_case
    before = store.snapshot_for_assessment(attempt_id)
    store.store_proposed_artifact(attempt_id, role, artifact_bytes)
    assert store.snapshot_for_assessment(attempt_id) == before
```

`store_case` is a SQLite unit fixture using generated TEST_ONLY captured state,
valid role-specific artifact bytes and no launched-worker claim. The real launch
case is mandatory separately in Tasks 7-8.

- [ ] Run existing N1 Tasks 2-5 unit selections, followed by real disposable-host
  launch/capture tests. Record actual UIDs, image/profile hashes, start count,
  denied accesses and owned cleanup. A missing host is an explicit blocked Linux
  milestone; continue only independent pure-library work, not simulated acceptance.

**Exit:** Protected facts have actual producers; there is no client complete/sign
RPC, no mutable workspace import path and no journal/key mount in the worker.

## Task 7: G5 reconstructs artifacts and commits against current validity

**Outcome:** A real losing N1 produces a committed failure; a real passing N1 produces
only progress; consistent fabricated evidence is rejected. Retained outputs exactly
match the facts adjudicated.

**Files:** Execute existing N1 plan Task 6's `execution/g5.py` and protected entrypoint
work. Modify planned `execution/store.py`/`service.py`; revise legacy active entry
points in `seal.py`/`orchestration.py`; create
`tests/ops/qualification/execution/test_artifact_acceptance.py` and extend real
`tests/integration/qualification_boundary/test_acceptance.py`.

**Interfaces:** Existing protected `accept_n1`, `authenticate_n1_evidence`,
`validate_n1_evidence` and `validate_result_envelope_v2` now require verified capture,
the exact service snapshot bytes and Task 4 reconstruction. Add
`journal_snapshot_bytes: bytes` as a keyword argument to all three validation/
authentication functions; `expected_revision` must equal the parsed campaign
revision. `accept_n1` fetches it and all original context/artifact bytes itself.

- [ ] Have protected G5 fetch authoritative context, attestation, original worker
  bytes and snapshot. Verify signature/custody/release/key/approval policy first;
  recheck static legality; call `build_n1_evidence`; authenticate only these original
  inputs and their reconstruction. Never sign a caller-built dataclass.
- [ ] Before fresh reconstruction, query STATUS for an existing N1 assessment. If
  present, fetch its stored envelope/authentication/receipt and verify their historical
  integrity; return the stored receipt with current validity/eligibility, not a new
  signature. Historical retrieval remains available after expiry or VOID to the
  authorized peer and cannot report a new acceptance. New assessments still apply
  all current approval/key/release checks.
- [ ] STORE_ARTIFACT all generated mandatory outputs, then STORE_RESULT the canonical
  envelope, then COMMIT_N1_RESULT. Attempt membership/privacy apply to each stage.
  The active result envelope has exactly the spec's authoritative fields; client
  output paths, arbitrary roles and caller-selected adjudicators are absent.
- [ ] Under `BEGIN IMMEDIATE`, first check for a stored exact retry using manifest,
  authentication digest, producer scope and ordered stages. Return stored receipt
  with current validity/eligibility if exact; changed identity conflicts. Transport
  authorization applies to both branches. Do not put first-acceptance expiry checks
  before this exact historical retry branch. For a first commit,
  rederive snapshot and compare bytes/hash/revision, require VALID and exact attested
  membership, then atomically record CUTOFF and terminal failure or progress.
- [ ] Add the exact retry test through the real public route after reopening the
  service/G5 processes. A refreshed signature for identical result bytes conflicts.
- [ ] Convert legacy active entry points to explicit rejection. Keep read-only v1
  inspection and historical signature verification; revise tests to distinguish
  historical consistency from active acceptance. No `allow_legacy` switch.
- [ ] Retain existing genuine trading fixture and signed inert-port failure fixture.
  Both use real source/replay and the same required artifact schema as production.
  Assert path/outcome/legality/runtime/journal identities inside the committed set.

```python
def test_losing_n1_retains_the_evidence_it_adjudicated(real_boundary):
    attempt = real_boundary.submit_fixture('inert_ports')
    accepted = real_boundary.accept_n1(attempt)
    assert accepted['completion'] == 'COMPLETE'
    assert accepted['verdict'] == 'FAIL'
    assert real_boundary.launch_count(attempt) == 1
    assert real_boundary.verify_retained_result(attempt) == 'VALID'
    assert real_boundary.executed_stages(attempt) == ['LEGALITY', 'N1']
```

`real_boundary` is the disposable Linux administrator harness from existing N1
Task 7: launch genuine installed services under their UIDs; submit only generated
signed TEST_ONLY bundles; observe Docker starts. `accept_n1` invokes protected qg5.
`verify_retained_result` refetches committed original bytes and runs the actual v2
verifier; `executed_stages` reads the authenticated envelope, not a fixture counter.
No outcome-producing function is monkeypatched by this fixture.

- [ ] Add coherent output substitution with rehashed manifests, forged completion,
  missing attestation, modified Python outcome object, wrong policy and descriptor
  injection on the client side. Each must fail without accepted result or second launch.
- [ ] Assert CONTINUE gives PARTIAL/NONE and no N2; all full PASS/seal routes fail.
  Recheck OPERATOR execution rejection in the N1_ONLY installed release.

Run existing N1 Task 6 selections plus
`./fp.ps1 python -m pytest tests/ops/qualification/execution/test_artifact_acceptance.py -q --tb=short`;
run real `test_acceptance.py` through the Linux boundary recorder script.

**Exit:** Actual launch -> captured bytes -> real G5 -> atomic commit is verified;
legacy bypass is unavailable; semantics and provenance are both mandatory.

## Task 8: Lifecycle invariants survive process failure and concurrency

**Outcome:** Event sequences preserve at-most-once execution, exact retry identity,
current validity and durable historical evidence after restart.

**Files:** Create `tests/integration/qualification_boundary/test_lifecycle.py`,
`tests/ops/qualification/execution/lifecycle_model.py`,
`tests/ops/qualification/execution/test_lifecycle_model.py`. Modify store/service only
for defects demonstrated by these tests, preserving the spec's state machine.

**Model:** A test-only reference tracks validity, launch-intent count, captured
identity, published attestation, committed result/authentication and event count.
It contains no SQL, production transition calls or production guard helper imports.
Use deterministic parameterized event traces and seeded sequences; no new property
test dependency is required. Compare public responses and persistent state to it.

- [ ] Test duplicate/concurrent submit, conflicting bindings, interruption before
  start, after start intent, during output, after CAPTURED and before publication.
  Actual child processes are killed at administrator-controlled test checkpoints;
  these checkpoints are unavailable in production builds and do not supply outcomes.
- [ ] Test VOID versus attestation publication and VOID versus first commit in both
  lock orders with real SQLite/process barriers. Observe second writer attempting
  the transaction before releasing the first; no sleep-based race assertion.
- [ ] Test exact commit retry after lost acknowledgment/process restart, commit then
  VOID then retry, approval expiry then retry, and refreshed authentication conflicts. Assert event history
  does not change for exact retries and current validity remains separately visible.
- [ ] Test input/approval expiration between intent and observed start; incomplete
  capture after zero exit; CPU/memory/wall excess; wrong retained object; and key/
  release invalidity at acceptance. No result and no automatic redraw follow.

```python
@pytest.mark.parametrize('first', ['void', 'commit'])
def test_void_and_first_commit_are_serialized(real_boundary, first):
    attempt = real_boundary.capture_fixture('inert_ports')
    trace = real_boundary.race_void_and_commit(attempt, first=first)
    assert trace.second_writer_observed_waiting
    assert trace.current_validity == 'VOID'
    assert trace.committed_result_exists is (first == 'commit')
    assert real_boundary.launch_count(attempt) == 1
```

The harness methods install no alternate journal semantics: `capture_fixture`
stops orchestration after actual ATTESTED publication; `race_void_and_commit`
invokes real signed VOID and qg5 commit while test-only barriers control lock order.
It returns observations from actual events/responses. Reopen the store in a new
process before asserting final state.

- [ ] Verify the N1-only seal rejection under all relevant validity states. Keep
  existing v1 VOID/seal regression as historical coverage only; do not claim a v2
  full campaign sealer exists. Future full-campaign implementation inherits this
  transition contract and needs its own two-order sealing proof.

Run: `./fp.ps1 python -m pytest tests/ops/qualification/execution/test_lifecycle_model.py tests/ops/qualification/execution/test_store.py -q --tb=short`;
run Linux lifecycle tests through the boundary recorder.

**Exit:** Actual restart/race evidence agrees with the independent model; all
in-scope failure states have a disposition and no path redraws after uncertainty.

## Task 9: Gate acceptance on explicit invariants and their actual evidence

**Outcome:** CI cannot report qualification acceptance with omitted/renamed/skipped
critical tests; review closure is tied to a verified family, not a single example.

**Files:** Create `tests/ops/qualification/invariant_manifest.json`,
`scripts/check_qualification_invariants.py`,
`tests/test_qualification_invariant_manifest.py`; update the planned
`scripts/qualification_boundary_verification.py` and
`.github/workflows/qualification-execution-boundary.yml`. Update the PR/audit and
existing qualification acceptance documentation at execution, preserving history.

**Interfaces:**

```python
# check_qualification_invariants.py
def validate_manifest(manifest_bytes: bytes, *, collected_nodeids: set[str],
                      junit_paths: tuple[Path, ...], evidence_root: Path) -> dict: ...
```

Return `{passed:bool,missing:list[str],skipped:list[str],failed:list[str]}` with
invariant IDs and exact node IDs in diagnostics. Parse the existing recorder's
child JUnit manifests as well as parent reports; count each required case once.
Use recorded test IDs when present; otherwise resolve JUnit classname/name to a
unique collected node ID and reject ambiguity. Never infer execution from collection.

- [ ] Populate QPOL/QLEG/QART/QPLAN/QEXEC/QKEY/QSTATE/QISOL/QGATE entries with actual
  collected node IDs created above and existing seed/key tests. Each has the spec's
  requirement, owner, producer, consumer and evidence kind. No wildcard selectors
  or tests that merely share a promising name.
- [ ] Add unit report fixtures for missing ID, renamed test, skipped Linux test,
  failed setup, ambiguous JUnit identity, duplicate reports and complete success.
  Preserve xunit/subtest semantics used by the existing verification recorder.

```python
def test_critical_skip_cannot_satisfy_manifest(manifest_report_case):
    raw, collected, reports, root = manifest_report_case('critical_skip')
    result = validate_manifest(raw, collected_nodeids=collected,
                               junit_paths=reports, evidence_root=root)
    assert result['passed'] is False
    assert result['skipped']
```

`manifest_report_case` writes minimal report/record fixtures matching the current
recorder schema in `tmp_path`; it tests report parsing only. Real Linux acceptance
also requires completed recorder status, zero exit, stable source, complete capture,
valid reports and successful owned cleanup.

- [ ] Run controlled mutations in a disposable copy: bypass product-basis comparison,
  bypass registry validation, bypass role-to-content comparison. Each mutation must
  make its required test fail on the intended behavioral assertion; an import or
  setup error is inconclusive. Restore the copy before normal acceptance. Record
  exact mutation diff, test ID and outcome in the audit; no new mutation dependency.
- [ ] Add a compact review-family disposition to the existing audit template:
  invariant, trigger, related consumers, fixed/safe/unresolved evidence. For these
  changes fill actual N1/N2/Part B/Part A schema, public retry and legacy entry paths.
  Process guidance must not be used as a substitute for tests or access control.
- [ ] Run the combined focused qualification suite and repository gates using the
  implementation checkout. Run Linux composition/lifecycle/permission acceptance
  with the canonical profile and environment plan. Reuse prior valid records only
  where source/configuration inputs remain unchanged and behavior coverage applies.

```powershell
.\fp.ps1 doctor
.\fp.ps1 python -m pytest tests/ops/qualification tests/ops/test_phase3_provenance_acceptance.py tests/ops/test_qualification_isolation.py tests/test_certification_power.py tests/test_qualification_authority_boundaries.py tests/test_qualification_invariant_manifest.py -q --tb=short
.\fp.ps1 check
```

`test_qualification_authority_boundaries.py` is supplied by existing N1 Task 7;
absence is incomplete implementation, not grounds to drop the selector.

```bash
python -I scripts/fp.py doctor
python -I scripts/fp.py python scripts/qualification_boundary_verification.py --test-only
```

- [ ] Inspect records and actual reports, then report command, interpreter,
  revision/source fingerprint, environment/image/profile/policy identities, counts,
  critical skips/failures, denied accesses and cleanup. Do not describe a partial
  or interrupted run as accepted. Preserve missing private-source limitations.
- [ ] Request independent review of the combined boundary under the applicable
  review skill during implementation. It must examine invariant enforcement and
  affected unchanged consumers, not merely the newest patch.

**Exit:** Every discovered in-scope path has a supported disposition; the real N1
vertical route and its negative controls pass on one identified revision; remaining
full-campaign/production prerequisites are explicitly open.

## Self-review and acceptance trace map

| Design requirement | Plan owner/test boundary |
| --- | --- |
| Canonical product/state/stages/artifact policy | Tasks 1 and 5, semantic + signed G1 rejection |
| Real retained registry/source legality | Tasks 2 and 5-7, real source admission + captured record |
| Terminal-prefix roles and exact evidence contents | Tasks 3-4 and 7, reconstruction + public acceptance |
| Snapshot/commit acyclic identity and retry | Tasks 4, 6-8, real journal transaction and restart |
| Controlled actual execution and key separation | Existing N1 Tasks 1-6 as amended in Tasks 5-7 |
| No-redraw, VOID and interrupted capture | Task 8 plus mandatory store guards in Task 6 |
| Legacy refusal and N1_ONLY capability ceiling | Tasks 5 and 7-9, active endpoint rejection |
| Independent vectors and invariant-family closure | Every task; final gate Task 9 |
| Image imports and canonical dependency configuration | Tasks 1, 5-6 and existing image checks |

Walk the design's seven concrete traces through implemented producers before
acceptance. In particular, no artifact test can stand in for real capture; no
source-construction boolean can stand in for registry validation; no stored snapshot
can stand in for the current transactional validity check.

Planning review checked schema/role naming, task dependencies, required producer
availability, prefix handling, digest cycles, retry ordering and legacy cutover.
Implementation still requires approval and execution-time baseline reconciliation.
Full N2/Part A execution, complete-campaign cumulative budget persistence, v2 sealing,
actual-source qualification, production enrollment and deployment remain a subsequent
scope. They cannot be closed by this N1-only plan or silently inherited from v1.

## Execution ledger — 2026-09-17

- Owner: root coordinator; branch `codex/qualification-structural-closure` in `.worktrees/qualification-structural-closure`.
- Refreshed PR415 remains OPEN at `bfad2f187e05980369dbf0e8f75801f621ba998d`; main `31512368e6d1b9e1cc7acc6cf0baa752dea3bed7` is already its ancestor. No merge changes were needed.
- Preserved dirty main and both N1 prototype worktrees. Copied this plan, governing design, N1 documents, Linux plan and assessments into this checkout. Prototypes are review inputs only; no v2 release found on refreshed PR/main.
- `./fp.ps1 doctor`: Python 3.13.2, `C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`; 62 locked packages, cryptography 50.0.1.
- Task 1 implemented as a semantic library; signed v2 wiring remains Task 5. Focused semantic/contract/domain command: 100 passed, record `.cache/fp-verification/20260917T221621Z-a46008d00a17/record.json`; completed, exit zero, stable source, complete capture, no report errors. Initial red: 43 failures for absent implementation, after correcting a test-import collection error.
- Task 2 implementation added. Source factory consumes the same prepared snapshot after registry validation. Signed nonempty registry and invalid cost inputs reject. Fingerprint tests loaded canonical source under flat aliases; canonicalized their imports without weakening inventory checks. Expanded source run: 300 passed / 3 alias failures; follow-up legality/fingerprint/sizing selection: 265 passed, record `20260917T222558Z-ae0de8479008`. Task 2 final prescribed rerun remains due.
- User approved GitHub-hosted `ubuntu-24.04` acceptance target. Existing host-readiness branch `codex/linux-isolation-environment` at `7ca606d` has passing run https://github.com/Joshua-Asante/first-passage/actions/runs/35280061788. This is readiness only. Local QualificationBoundaryN1 WSL is Debian 12/ext4/Docker 20.10.24 and does not satisfy the specified OS target.
- Tasks 3–9 pending. No protected execution, v2 cutover, recorder acceptance, deployment, full E1 PASS, or merge claimed.

- Task 2 final combined regression: 195 passed in 106.71s using `./fp.ps1 --workers 2 python -m pytest tests/ops/qualification/test_legality_evidence.py tests/ops/qualification/test_evidence_reconstruction.py tests/ops/qualification/test_evidence_artifacts.py tests/ops/qualification/test_journal_snapshot.py tests/ops/qualification/test_production_source.py tests/ops/test_policy_fingerprint.py -q --tb=short`, record `20260917T223903Z-03e72c945aa0`: completed/exit 0, source stable, capture complete, no report errors. Independent review found prepared-input substitution; reproduced changed unquoted volumes with unchanged retained hashes, then fixed by canonical derivation/comparison from the same retained snapshot before issuance.
- Tasks 3–4 implemented in part; strict envelope/artifact self-comparison regressions pass (58 tests, record `20260917T224210Z-9697f8458402`). Complete N1 plan reconstruction added: eight coherently rehashed workload/probe/source-proof mutations first failed, then all 30 reconstruction cases passed (`20260917T224510Z-2d253f3784db`). Complete release/attestation schemas and signed wiring remain open; do not treat Tasks 3–4 as accepted.
- Host harness imported selectively from updated `c2ae5bf` (host files only, not older product code). No host provision, CI dispatch, protected execution or active acceptance has occurred in this checkout.
### Reconciliation and implementation checkpoint (23:28 UTC)

- Merged refreshed `origin/main` (`5cda6f4`, including PR420) into this isolated branch at `6be024ae2ef6ad14af98ff67fd95c3aa12af7346`. PR420 remains the canonical host harness. The old baseline statement above records earlier inspection, not current main. Main checkout and prototype worktrees remain preserved.
- The user's implementation handoff supersedes planning-only banners in these documents. No deployment, production keys, full-campaign execution or merge-to-main is authorized.
- Removed the host harness's duplicated signing version: `tools/local_verification/requirements-extra.txt` owns the pin; protected staged inputs plus `signing-wheel.json` derive the hash-locked installation requirement. Host unit selection: 154 passed, 2 platform skips (`20260917T230712Z-d27afa195cf7`). Those skips establish no Linux acceptance.
- Task 3/4 library reconstruction now uses complete closed release/attestation schemas, complete independently derived plans, exact role bytes and logical snapshots. Canonical policy owns stage/artifact/checkpoint inventories. Tasks remain open pending full checklist reconciliation and active integration.
- Task 5 signed v2 admission implementation validates installed policy, original approvals, disjoint keys, full role bindings and real static registry bytes. Signed wrong-basis/role override tests reach semantic rejection. Bundle/verification selection: 14 passed (`20260917T225946Z-afdd5a19e439`). Runtime installation, active preflight/cutover and launch-count evidence remain open.
- Task 6 library work: durable schema-v4 store, candidate-only artifact membership, unchanged revision on snapshot/storage, actual retained-source worker admission, budgeted original N1 replay, framed archive rejection. Compute/worker parity selection: 8 passed in 68.57s (`20260917T231258Z-b401b3cea657`). Archive: 6 passed (`20260917T231732Z-e7e19e824ff4`). Independent review found boolean path indices accepted by Python equality; actual-output regression reproduced DID NOT RAISE, then canonical byte comparison passed (`20260917T231900Z-2d774cc60ee0`).
- Worker closure test exposed legacy orchestration/attempt imports through seed derivation. Extracted unchanged canonical seed identity into `seed_identity.py`, shared by legacy and new callers. Runtime/seed-vector/reconstruction selection: 80 passed (`20260917T232049Z-0acc07e973f9`). This is source-inventory verification, not installed-image acceptance.
- Task 7 library work: G5 revalidates original signed capture/current context, compares worker observations, and reconstructs all five artifacts. Coherently rehashed substitutions reject: 7 passed (`20260917T232341Z-0bddcb662490`). Fixture signatures are explicitly consistency-only.
- Atomic store commit compares current snapshot under writer lock, promotes exact candidate artifacts, retains an acyclic immutable receipt, and checks exact retry identity before fresh validity/revision checks. Reopen/VOID preserves receipt; changed authentication conflicts. Store/atomic selection: 24 passed (`20260917T232713Z-f624ce958f43`). Public transport, current eligibility, approval-expiry retrieval and real process restart remain open.
- All commands above used this checkout's `./fp.ps1 --workers 2 python -m pytest <named selections> -q --tb=short`, interpreter `C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe` (3.13.2). Records through `232341Z` inspected completed/exit 0/stable source/complete capture/no report errors. Atomic record inspection remains due. `./fp.ps1 check` at earlier source passed (`20260917T230311Z-45337f01b731`), including 72 unittest cases / 3 skips; it is not a current full-suite result.
- Still open: protected signer/service/G5 entrypoints, canonical-host owned container/service cleanup, real worker image/install, Linux capture and public acceptance, v1 retirement, lifecycle/concurrency, invariant gate/mutations and combined independent review. `--test-only` remains blocked. qexec's Docker access remains root-equivalent; use fresh hosts; issue424 GID/mode drift remains deferred. Acceptance remains held, N1_ONLY ceiling unchanged.

### Library and service checkpoint (2026-09-18 00:17 UTC)

- Tasks 3–4 semantic-library checklist completed; this does not establish protected capture. Added populated ATTESTED/VOID handwritten snapshot vectors, revision ordering, later-stage prerequisite/Part A expansion and ordering cases, complete-prefix role omissions and concrete-container equality rejection.
- Implemented protected-entrypoint code for bootstrap, runtime measurement, credentials, native Docker launch/capture, supervisor, G5 and bounded peer-checked client. These entrypoints have not yet been installed or exercised on the disposable Linux target.
- G5 historical inspection returns no authority. Public service exact retries return the original stored authentication/receipt and separate current validity/eligibility, including expiry and VOID. Fresh acceptance still revalidates current approvals and enrolled keys.
- Independent review exposed malformed candidate inventory/deep JSON failures, CAPTURED startup recovery failure and cleanup-before-uncertainty ordering. Regressions reproduced each; strict parsing, per-attempt recovery and durable uncertainty before cleanup now pass focused tests.
- VOID uses historical enrollment only to identify the original cancellation authority, then verifies a new approval with current time, revocation and exact original public-key fingerprints. Failed Docker cleanup leaves durable VOID and separately reports CLEANUP_PENDING; recovery retries cleanup. The admission/reservation timestamp mismatch was reproduced, then fixed by using one verified instant under the writer transaction.
- Combined regression command: `./fp.ps1 --workers 2 python -m pytest tests/ops/qualification tests/test_certification_power.py tests/test_qualification_host.py -q --tb=short`. Record `20260917T234729Z-831325c64ee9`: 1013 passed, 4 failed, 2 platform skips in 1102.72s; failed status with stable source/complete capture. Three failures were fixture keyword drift; the fourth detected four missing ordinary dependency declarations. Declarations now include policy, policy_sources, seed_identity and policy_fingerprint. The flat-source fixture now selects explicit idle behavior instead of obsolete text replacement.
- Expanded corrective selection (artifact/reconstruction/snapshot/cost/closure/flat-source/service-assessment files): 184 passed in 82.86s, record `20260918T001301Z-c85000e701e1`. Latest service/assessment selection: 25 passed in 54.29s, record `20260918T001555Z-d618162b57e4`. Both inspected completed/exit 0/stable source/complete capture/no report errors. These correct all four combined-run failures; the complete combined suite has not been rerun at this state.
- All commands used this checkout's launcher and Python 3.13.2 at `C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`. Prior focused green records through `20260917T234633Z-b6e4709e8bc3` were also inspected stable/complete with zero report errors. Red records remain retained as failure evidence, not acceptance.
- Still open: real Linux installation/image and process/container capture, owned cleanup integration, active preflight/v1 retirement, real lifecycle/race conformance, invariant gate/mutations and combined independent acceptance review. `--test-only` remains blocked. No protected-release acceptance, full PASS/seal, OPERATOR execution, deployment or merge-to-main is claimed.
- Repository gates `./fp.ps1 check` passed at this checkpoint (`20260918T001824Z-f07e6a90c97b`), completed/exit zero/stable source/complete capture/no report errors. The evidence-store child ran 72 tests with 3 skips. Existing absent private Pine/data and heavy-analysis-artifact advisories remain; these gates do not verify those absent inputs.

### Host ownership integration checkpoint (2026-09-18 00:35 UTC)

- Working tree based on `b684878f24cafc993575e345de6a775fa0815768`. Canonical PR420 harness now supplies durable build/release ownership enrollment, exact dispatch/container/image cleanup planning and registered asynchronous service children. Shared role policy grants qg5 the client socket group while keeping service data/key denials.
- Supervisor restart discovers a container created before its ID reached the journal using exact dispatch/name/image/host bindings. It records IN_DOUBT before cleanup and never issues a new start. Docker failure retains CLEANUP_PENDING.
- Independent review found uncontained Docker cleanup subprocesses and group members admitted by name without manifest ownership. Both regressions reproduced; cleanup now uses registered cgroups for Docker mutations and requires each supplementary member's owned account identity.
- `./fp.ps1 doctor` reconfirmed Python 3.13.2 at `C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`, 62 locked packages and cryptography 50.0.1. `./fp.ps1 --workers 2 python -m pytest tests/test_qualification_host.py tests/test_qualification_boundary_cleanup.py tests/test_qualification_container_ownership.py tests/test_qualification_boundary_environment.py tests/ops/qualification/execution/test_service.py tests/ops/qualification/execution/test_launcher.py tests/ops/qualification/execution/test_release.py tests/ops/qualification/execution/test_runtime.py -q --tb=short`: 205 passed, 2 Windows platform skips in 8.99s. Record `20260918T003439Z-449856c2b6aa` inspected completed, exit 0, stable source, complete capture, no report errors.
- These are unit/diagnostic results, not Linux isolation acceptance. Real image/install/capture, lifecycle interruption, active v1 retirement and invariant acceptance remain open. `--test-only` remains blocked; N1_ONLY and privileged-qexec trust assumptions remain unchanged.

### Incremental Linux route connected (00:49 UTC)

- Added administrator image builder in `execution/image.py`, exact worker closure COPY list, canonical signing inputs, pinned resolved Python base, owned build identity and bounded registered build children. Added shared TEST_ONLY profile and protected fixture installer using host-generated execution/result seeds. The real test producer signs input proposals only; it never supplies outcomes.
- Connected `--test-only` to the incremental real-process suite. It installs supervisor/G5 under canonical role UIDs and tests losing/passing N1, exact G5 retry after service restart, duplicate submission and closed client operations. Its recorder explicitly marks qualification acceptance held pending lifecycle/cutover/invariant gates. Default workflow remains host readiness; manual `boundary=true` selects diagnostics on two fresh Ubuntu hosts. No Linux run yet at this checkpoint.
- Independent review required actual Docker start events and durable evidence export. Added exact-container daemon event counts, retained inspection, synthetic object archive/journal and public-key export before owned cleanup; private credentials and ownership manifests are excluded.
- Gate `./fp.ps1 check` first rejected governance-to-ops imports in the image builder (`20260918T004533Z-c1dff37cdb83`). Relocated the builder into the operations execution package; rules unchanged. Rerun `20260918T004717Z-c2821c398e67` completed/exit zero/stable source. Usual missing private Pine/data/heavy-artifact advisories and 3 evidence-store skips remain.
- Image/profile/current signed fixture tests: 21 passed (`20260918T004332Z-5dc2f98482d2`); wrapper/image tests after relocation: 10 passed (`20260918T004652Z-c681820ca382`). All used launcher Python 3.13.2. Full acceptance and full combined suite remain outstanding.

- User explicitly approved publishing the isolated branch and copied documents to `Joshua-Asante/first-passage` and running two disposable Ubuntu jobs after automatic approval review initially rejected the push. Checkpoint `f47b6b6` pushed; run https://github.com/Joshua-Asante/first-passage/actions/runs/35292929760 completed with six setup errors on each host. Both built/installed the image and passed environment inspection, then supervisor socket chown failed because qexec is not a member of the client group. Both records are stable, capture complete, cleanup successful; no execution acceptance. Artifacts retained locally under `.cache/qualification-linux/35292929760`.
- Corrected socket ownership via administrator-installed setgid socket directory; supervisor verifies inherited UID/GID instead of requiring unauthorized chown. Supplementary role authority unchanged. Real rerun pending.
- V2 preflight now binds service/execution output identity, original approval subject/digest, bundle, plan, policy and release; supervisor archives it in the reservation transaction. Legacy client-path preflight rejects v2 before creating directories. Initial two regressions reproduced missing binding and erroneous client reservation (`20260918T005038Z-406c8e89f486`). Corrected selection: 34 passed in 58.45s (`20260918T005306Z-365d3a12cb6d`), stable complete recorder. One intervening invocation selected a nonexistent legacy preflight test file and collected zero tests; it is retained as failed, not evidence of coverage.

### Protected capture and legacy cutover checkpoint (2026-09-18 01:32 UTC)

- User explicitly approved publishing this branch and copied documents to `Joshua-Asante/first-passage` and running both disposable Ubuntu CI jobs. Push and CI succeeded at `2c6b0251de49fcd04761d6d11b1bb7edb2496e3e`.
- Real Linux run https://github.com/Joshua-Asante/first-passage/actions/runs/35293290005: both fresh Ubuntu hosts passed 6/6 incremental N1 tests, zero skips. Python 3.12.3; actual qclient/qexec/qg5 UIDs61000/61001/61002. Each host retained three exact container identities with one daemon start each. Losing N1 committed COMPLETE/FAIL; trading N1 committed PARTIAL/NONE with CONTINUE. Original receipt survived service/G5 restart. Both recorder records completed/exit0/stable source/complete capture/no report errors and successful exact owned cleanup. Independent artifact review verified346 object hashes and inspected actual capture/receipt/UID/cleanup links. This establishes incremental N1 capture only, not Tasks8-9 acceptance.
- Retired public v1 authenticate/claim/commit/seal and OPERATOR executor/orchestration entrypoints with `LEGACY_QUALIFICATION_INSPECTION_ONLY`. Read-only historical authentication and private v3 journal mechanics retain signature, replay, field equality, retry and VOID coverage. No legacy allow switch or v2 full-campaign sealer exists.
- Initial cutover regression record20260918T010014Z-b5079ebef85b:44passed14expected old-authority-test failures, stable source. Updated historical tests and closed independently identified direct ProductionExecutor bypass. Current focused command selecting authority boundaries, seal, review repairs, orchestration, production, composition, phase3 provenance, service and boundary fixture:133passed in1215.51s, record20260918T011115Z-dd623041ab3c, completed/exit0/stable/complete/no report errors. Interpreter remains operations Python3.13.2 at `C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`.
- `./fp.ps1 check` record20260918T012220Z-52644c82d707 passed, stable/complete/no report errors;72 evidence-store cases with3 existing skips. Private Pine/data/heavy-analysis artifacts remain unavailable and are not verified.
- Added real raw-socket client UID rejection and initial Linux CAPTURED/signer-denial/restart/VOID/changed-authentication tests. They are pending fresh CI; no Linux acceptance claimed for these edits. Review strengthened signer denial to restart while credentials remain inaccessible before restoring access. Clean-process bridge now selects the renamed historical composition test explicitly.
- Task9 report parser is being implemented independently by `/root/review_libraries` in isolated `codex/qualification-invariant-gate` at2c6b025. Coordinator owns canonical manifest/CI integration. Parser-only43pass/1Windows symlink privilege skip is not combined acceptance; files not yet integrated.
- Tasks8-9 remain open: full real interruptions, expiry, worker permission probes, both writer-lock race orders, independent lifecycle model, exact invariant manifest, targeted mutations and combined review. Current serial RPC loop cannot demonstrate two competing request writers; bounded concurrent handling and administrator TEST_ONLY transaction observation are required. Acceptance remains held; N1_ONLY ceiling unchanged.

### Lifecycle and invariant-library checkpoint (2026-09-18 01:41 UTC)

- Committed/pushed `16ffe7e` and ran both approved fresh Ubuntu jobs in https://github.com/Joshua-Asante/first-passage/actions/runs/35295798574. Each collected12:6passed/6failed/0skipped. Failed records remain stable/complete with successful owned cleanup. Three real lifecycle cases (CAPTURED credential denial/restart, VOID before first commit, commit/VOID/original retry) passed per host. All six new raw-socket negatives timed out because the test driver omitted its required write-side EOF. Production client already performs shutdown(SHUT_WR); corrected only the adversarial driver. Rerun remains required; the failed run is not acceptance.
- Integrated independently implemented invariant-report checker and SQL-free lifecycle reference/model tests from `codex/qualification-invariant-gate`; retained that task-owned worktree and its records. Coordinator selection `./fp.ps1 --workers 2 python -m pytest tests/test_qualification_invariant_manifest.py tests/ops/qualification/execution/test_lifecycle_model.py tests/ops/qualification/execution/test_store.py -q --tb=short`:88passed/1Windows symlink privilege skip in39.90s, record20260918T013959Z-f5dd157419d7 (stable source). Canonical manifest/CI gate wiring and real race evidence remain open.
- Signed synthetic fault fixtures now support actual worker SIGSTOP, zero exit without a frame, CPU/wall overrun and memory pressure; exact-depth approvals can have a real short validity period. Fixture admission RED5expectedmissingargument failures, then6passed in36.60s record20260918T013546Z-9f1b65d1a2ca. These checks validate admission only; real fault/expiry Linux tests are added but pending execution.
- Added actual stopped-worker/supervisor death, missing frame despite zero exit, CPU/wall/memory failure, expiry without new authority, and original committed receipt retrieval with inaccessible signer after expiry. No production outcomes or clocks are replaced. Full Task8 writer ordering and Task9 invariant/mutation/combined review remain unresolved. Acceptance held.

### Bounded return checkpoint (2026-09-18 01:52 UTC)

- Pushed revision `9a85772454a507da09903c0b2ca492a70301f0d8` on `codex/qualification-structural-closure`. User-directed stopping boundary: observe the existing run, retain evidence, document remaining work and return; no further repair/rerun or Task8/9 integration cycle.
- Run https://github.com/Joshua-Asante/first-passage/actions/runs/35296382825 completed failure on both fresh Ubuntu hosts. Each:19 collected,14 passed,5 failed,0 skipped/errors. Actual expiry/original receipt, raw client rejection, initial capture/G5/restart/VOID cases passed. Stopped-worker and exit-zero/CPU/wall/memory cases failed before their intended faults because real source admission rejected historical port pins (`production_source.py:595`). Fault-fixture static checks did not cover this full path. Production validation must remain intact.
- Evidence retained in `.cache/qualification-linux/35296382825`; host1 record `9dcc797a435246468b1e64c1b1d30d6f`, host2 `0a31b4031d9e4825aa398912c240345b`. Both exit1/stable source/complete capture/no capture errors; report errors correctly identify failed JUnit cases. Both owned cleanups succeeded with no failures; repeated cleanup already retired. Linux launcher Python3.12.3,62 locked packages,cryptography50.0.1; doctor preceded launcher invocation of `scripts/qualification_boundary_verification.py --test-only --manifest <manifest>` and recorded `-m pytest tests/integration/qualification_boundary -q --tb=short --junitxml=<record>/junit.xml`.
- Preserved unused `BoundedConnections` helper and two scheduler tests uncommitted. Serve remains serial; no concurrency acceptance claimed. Local launcher test record `20260918T014402Z-6c19e5d1e5e7`:2passed/stable/complete/no report errors, Python3.13.2. No local test process or active review agent remains; both CI jobs complete.
- Tasks8-9 remain open. Next bounded assignment: make fault fixture historical port pins coherent and exercise full source admission, then verify the five intended faults on fresh Linux hosts and return before concurrency integration. No repair/rerun performed at this checkpoint. Acceptance HELD; synthetic N1_ONLY ceiling unchanged.
- Detailed durable handoff: [qualification structural closure handoff](../../notes/audits/2026-09-17-qualification-structural-closure-handoff.md). Main, unrelated changes and worktrees preserved.

### Bounded fault-fixture repair (2026-09-18)

**Selected outcome:** Repair signed synthetic fault inputs so full source admission succeeds and the five actual stop/zero-exit/CPU/wall/memory cases reach their intended faults on two fresh Linux hosts.
**Prerequisites:** Existing isolated branch at `9a85772454a507da09903c0b2ca492a70301f0d8`; retained two-host failure evidence from run35296382825; doctor passed using operations Python3.13.2. Existing branch publishing and disposable CI route are authorized for this verification.
**Ownership:** `/root` implements and reviews this bounded outcome; combined qualification acceptance remains coordinator-owned and HELD.
**Verification:** First reproduce all five full-source-admission failures locally, then run corrected fixture and affected composition/source tests and `./fp.ps1 check`. Publish only this bounded repair and its ledger, dispatch the existing two-host TEST_ONLY workflow, inspect exact revision, JUnit, capture, actual fault/one-start/retry evidence and owned cleanup, and retain artifacts locally.
**Checkpoint:** Record RED/GREEN evidence here; report Linux outcome with retained run/record identities before returning.
**Return boundary:** Return after verified five-fault delivery or a concrete scope/external blocker. No concurrency integration, invariant-gate wiring, full qualification acceptance, deployment or merge. Preserve the unused scheduler helper/tests and prior uncommitted handoff.

The shared fixture currently hashes ports into historical cases, population bindings and reviews before the boundary producer mutates ORB. Move the synthetic port transformation before that common assembly so all dependent identities derive from final bytes. Production validation remains unchanged. Local and administrator fixture preparation must exercise `admit_source` before dispatch; the protected worker independently repeats admission.

- [ ] Reproduce the five failures through `admit_source`, retaining the valid idle case.
- [ ] Assemble final port bytes before historical/population bindings and verify source admission before dispatch.
- [ ] Run focused regression checks and repository gates; inspect final diff.
- [ ] Publish repair, run fresh Linux hosts, inspect and retain fault/cleanup evidence, then return.

- RED: full-source fixture selection reproduced the exact historical port mismatch for all five fault variants; idle passed. Record `20260918T015803Z-060fc82c60a7`:5failed/1passed, exit1/stable source.
- GREEN before diagnostic marker addition:6passed, record `20260918T015916Z-6a64039116ea`, completed/exit0/stable/complete/no report errors.
- Final local selection: `./fp.ps1 --workers 2 python -m pytest tests/ops/qualification/execution/test_boundary_fixture.py tests/ops/qualification/test_composition_fixture.py tests/ops/qualification/test_production_source.py tests/ops/qualification/test_legality_evidence.py -q --tb=short`:67passed in187.93s, record `20260918T020047Z-039752d69106`. `./fp.ps1 check`:passed, record `20260918T020207Z-a5b7de307566`;72 evidence-store tests/3 existing skips, missing private Pine/data/heavy artifacts remain unverified. Both records completed/exit0/stable/complete/no report errors. Interpreter `C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`, Python3.13.2, working tree based on9a85772 with bounded repair and preserved unused service draft.
- Family disposition: historical cases/acceptance, population source-binding/review and domain/contract pins now all derive from final source bytes through the common fixture builder. Ordinary idle/trading producers retain the default path. Real `admit_source` succeeds before staging; worker repeats it. Administrator diagnostic admission/legality records are exported separately and do not confer worker authority. All five Linux assertions now require the fault callback stderr marker plus their actual process/container outcomes. Focused self-review found no production validator/policy change; no independent review claimed for this bounded patch.
- Local implementation and verification complete; fresh Linux fault evidence remains pending. The unrelated unused service scheduler and its tests remain excluded from the repair commit.
