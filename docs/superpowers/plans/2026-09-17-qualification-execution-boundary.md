# N1 Execution Attestation Boundary Implementation Plan

> **For agentic workers:** Execute with superpowers:executing-plans; use superpowers:subagent-driven-development when bounded delegation is useful and authorized. Preserve the behavioral contract and integration owner. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Execute one authorized synthetic N1 checkpoint through a controlled service and require its execution attestation at G5, preserving replay and statistical mechanics.

**Architecture:** A protected Linux supervisor owns the active journal, launches a pinned worker with no journal/key access, captures immutable output and signs execution facts. A protected G5 process verifies those facts and independently adjudicates captured outcomes; service transactions record acceptance against current validity. The N1-only release cannot produce E1 PASS or continue to N2.

**Tech Stack:** Python >=3.11, existing locked operations dependencies, existing canonical JSON/Ed25519 verification, cryptography 50.0.1 for service signing, SQLite, Linux Unix sockets/peer credentials, Docker Engine, pytest and the repository verification launcher.

**Spec:** [N1 execution attestation boundary](../specs/2026-09-17-qualification-execution-boundary-design.md).

## Global Constraints

- Planning only. No implementation, deployment, F1 freeze, exact-depth execution, production signature, admission, or live activation is authorized by this file.
- Keep source loading, sampling, replay, kernel evaluation and exact statistical decisions unchanged.
- TEST_ONLY reduces fixture workloads, not required provenance checks.
- No automatic v3-to-v4 in-flight migration; old artifacts cannot acquire execution attestations retroactively.
- All complete PASS/seal entry points fail `UNSUPPORTED_ATTESTED_CHECKPOINT_SET` in the N1-only release.
- Secrets stay outside versioned configuration.
- No real qualification should start under this N1-only release.
- Use the checkout's `fp.ps1` launcher; run doctor before Python work. Portable equivalent: `python -I scripts/fp.py`.
- Report actual command, interpreter, tested revision/working tree, results and unresolved skips/failures. No production acceptance from synthetic fixtures.

Status: proposed implementation plan, based on reviewed PR415 head `5e935c8`.
User requested design/planning, not implementation. The coordinating implementer
owns the complete launch-to-G5 outcome. No delegation is assigned by this plan.

---

## Contract inventory and sequencing

Read the spec and `docs/notes/audits/2026-09-17-pr415-qualification-review.md` first.
Reverify the chosen baseline's `contract`, `trust_domain`, `preflight`, `attempt`,
`production`, `orchestration`, `seal` and CLI interfaces. Use an isolated worktree
at implementation time; do not alter the preserved PR415 checkout opportunistically.

Tasks 1–7 are dependent engineering increments. Each has a bounded test cycle,
but only Task 7 establishes the complete boundary. Do not expose the service as
production-ready between them. Task 1 creates shared protocol values; Task 2 is
the sole active persistence owner; Task 3 supplies real compute; Task 4 controls
launch/capture; Task 5 exposes authenticated operations and signs; Task 6 replaces
G5's caller-data acceptance; Task 7 verifies the composition and permission boundary.

New files below live under `ops/c1_rail/qualification/execution/` unless a full path
is given. Keep this package's `__init__.py` free of executable setup and signer
imports. The dependency graph is `protocol/plan/profile <- worker or supervisor
or g5`; worker and g5 must not import supervisor/signer/store/launcher.

### Shared public and internal interfaces

These signatures are the cross-task contract. All wire bytes use the spec's closed
schemas. Dataclasses below are internal conveniences, not unforgeable authority.

```python
# execution/protocol.py
@dataclass(frozen=True)
class ExecutionRecord:
    execution_id: str
    attempt_id: str
    state: str
    revision: int
    plan_sha256: str
    attestation_sha256: str | None

@dataclass(frozen=True)
class CapturedOutput:
    container_id: str
    result_bytes: bytes
    exit_code: int
    oom_killed: bool
    supervisor_wall_ns: int

@dataclass(frozen=True)
class VerifiedExecution:
    attestation_bytes: bytes
    result_bytes: bytes
    plan_bytes: bytes
    execution_id: str
    attempt_id: str

@dataclass(frozen=True)
class ValidatedEvidence:
    result_bytes: bytes
    attestation_sha256: str
    n1_decision: str        # CONTINUE or FAILURE
    expected_revision: int

# Names for type annotations only; these are not runtime capabilities.
JsonObject = dict[str, object]
ArtifactBytes = dict[str, bytes]   # SHA-256 -> immutable bytes
```

`ExecutionProfile` wraps canonical validated profile bytes with typed properties
for the spec's fields; `ExecutionContext` holds the separately validated frozen
contract, domain, installed release bytes, retained bundle index and approval bytes.
Both are reconstructed inside each trusted process; the client never supplies
instances. `verify_bundle(bundle_dir, installed_release, trusted_keys, now)` is the
only producer of `ExecutionContext`. Define it in `admission.py`; it reads/hashes
staged bytes and invokes existing validators, never imports retained ports.

## Task 1: Freeze exact plans, release policy and execution evidence schemas

**Outcome:** One canonical derivation of N1 inputs and a closed v2 trust policy
reject substitution, role-key aliases and unsupported production activation.

**Files:**
- Create: `execution/{__init__,protocol,profile,plan,admission,verification}.py`.
- Modify: `qualification/{contract,trust_domain,preflight,orchestration}.py`.
- Create tests: `tests/ops/qualification/execution/{test_protocol,test_plan,test_admission,test_verification}.py`.
- Update: `tests/ops/qualification/{test_contract,test_trust_domain,test_result_key_binding}.py`.

**Interfaces:**

```python
parse_profile(raw: bytes) -> ExecutionProfile
derive_n1_plan(contract, *, attempt_id: str,
               exact_depth_approval_sha256: str) -> bytes
verify_bundle(bundle_dir: Path, installed_release: bytes,
              trusted_keys: dict, now: datetime) -> ExecutionContext
verify_execution(attestation: bytes, artifacts: ArtifactBytes, *,
                 context: ExecutionContext, expected_attempt_id: str,
                 current_keys: dict) -> VerifiedExecution
```

**Behavioral contract:** Freeze/release authorities own policy and key enrollment;
the build owns image manifests; existing source owners own retained input bytes.
Execution clients cannot alter any resolved policy or seed. `verify_execution`
verifies signatures and bytes but cannot persist completion or create a signature.

- [ ] Add negative tests for duplicate/unknown JSON fields; noncanonical bytes;
  matching IDs with substituted public bytes; different IDs sharing a public key;
  TEST_ONLY release in an OPERATOR installation; unapproved release/image identity;
  N1_ONLY profile with production execution enabled; unsupported checkpoint N2.
- [ ] Extract the seed-record construction from orchestration into `plan.py` while
  retaining `domain_seed` unchanged. Include ordered FULL/H1/H2 paths, original
  probe address, source-proof work and exact source-population hashes in v2 plans.
- [ ] Add fixed seed vectors and exact plan-byte vectors. Derive expected values
  independently once from the existing formula at the baseline, retain them as
  fixtures, and compare the refactor against them; do not call the new helper to
  calculate the expected value inside its own test.
- [ ] Add a substitution regression that changes seed, namespace and population
  digest and rehashes all dependent records. Verification must reject it, even
  when a TEST_ONLY execution key signs the internally consistent wrong plan.

```python
def test_distinct_role_ids_cannot_alias_one_key(operator_domain_case):
    doc, keys = operator_domain_case
    doc['execution_key_ids'] = ['execution']
    keys['execution'] = replace(keys['producer'], key_id='execution')
    doc['trusted_key_sha256']['execution'] = doc['trusted_key_sha256']['producer']
    with pytest.raises(ValueError, match='public.key.*separation'):
        validate_signed_domain_case(doc, keys)
```

`operator_domain_case` and `validate_signed_domain_case` are new test helpers in
`execution/conftest.py`: adapt the existing `test_trust_domain.operator_case`, use
generated distinct keys for freeze/result/seal/execution, and sign the final v2
domain with the fixture freeze key. They never execute an OPERATOR workload.

- [ ] Introduce explicit version dispatch: legacy schemas are inspection-only;
  active schema is domain/v2 + frozen-contract/v2 + preflight/v2. Add the execution
  release role and required attested checkpoints to the signed identities.
- [ ] Validate installed release approval with `APPROVE_EXECUTION_RELEASE`; check
  exact source hashes against the ordinary code inventory and approved image.
  Keep staging paths within the service root, rejecting links and special files.
- [ ] Derive/check separate supervisor, worker and G5 ordinary-code closures from
  their real entry points, including new execution modules. Keep four port roles
  explicitly contract-bound; do not reuse the old closure list without checking
  its completeness for the new entry points.
- [ ] Run targeted tests through the checkout launcher; inspect their actual
  rejection reason so a signature fixture error does not masquerade as a policy test.

```powershell
.\fp.ps1 doctor
.\fp.ps1 python -m pytest tests/ops/qualification/execution/test_protocol.py tests/ops/qualification/execution/test_plan.py tests/ops/qualification/execution/test_admission.py tests/ops/qualification/execution/test_verification.py tests/ops/qualification/test_contract.py tests/ops/qualification/test_trust_domain.py tests/ops/qualification/test_result_key_binding.py -q --tb=short
```

- [ ] Review the v2 wire vectors and authority-class matrix; commit this increment
  only under implementation/commit authorization in force.

## Task 2: Make the service journal the sole completion owner

**Outcome:** An attempt has at most one launch intent, and no caller can turn a
consumed flag into a service-recognized completed execution.

**Files:** Create `execution/store.py`, tests `execution/test_store.py`; modify
`qualification/attempt.py` only to make v3 mutation unavailable to active v2 flows
and retain explicit historical inspection.

**Interfaces:** `ExecutionStore(path)` has these service-internal methods:

```python
reserve(request_bytes: bytes, plan_bytes: bytes, *, now: datetime) -> ExecutionRecord
record_container(execution_id: str, container_id: str, *, expected_revision: int) -> ExecutionRecord
record_start_intent(execution_id: str, *, expected_revision: int, now: datetime) -> ExecutionRecord
record_running(execution_id: str, *, expected_revision: int, now: datetime) -> ExecutionRecord
record_capture(execution_id: str, capture_bytes: bytes, *, expected_revision: int) -> ExecutionRecord
get_captured_payload(execution_id: str) -> bytes
publish_attestation(execution_id: str, attestation_bytes: bytes,
                    *, expected_revision: int) -> ExecutionRecord
record_abort(execution_id: str, reason: str, *, uncertain: bool) -> ExecutionRecord
commit_assessment(evidence: ValidatedEvidence, authentication_bytes: bytes,
                  *, now: datetime) -> bytes
void(attempt_id: str, reason: str, approval_bytes: bytes, *, now: datetime) -> bytes
status(attempt_id: str) -> bytes
```

The authenticated supervisor calls these after validation. They are not RPC
operations or a security boundary for another program with access to the DB file.
OS ownership prevents qclient/worker from accessing that file at all.

**Storage:** One SQLite schema-v4 DB. Tables: `campaigns` (domain/contract/attempt
identity, validity/reason, event head/count), `executions` (checkpoint, plan/request/
release, state, container and capture/attestation digests, revision), `events`
(campaign sequence, canonical body, previous/current hashes), `objects` (hash,
length, role, immutable archive location), `execution_objects` (execution/object
membership), and `assessments` (N1 assessment, canonical envelope/authentication,
derived CUTOFF bytes, commit event). Unique execution identity is the spec's tuple.
Foreign keys bind every object/event/assessment to its campaign/execution.

- [ ] Write races/restart tests against real SQLite connections: duplicate submit;
  conflicting request for an existing approved attempt; two completion writers;
  VOID between capture and signature persistence; VOID before assessment commit.
- [ ] Implement state transitions with `BEGIN IMMEDIATE` and expected revisions.
  Persist START_INTENT before launch. Never permit RUNNING/IN_DOUBT back to PENDING.
  Idempotency returns stored bytes only for exact bindings and reports validity.
- [ ] Implement CAPTURED -> ATTESTED as a separate transaction; `record_capture`
  requires durable archive membership and exact capture facts. Append the capture
  event first and construct/store its unsigned attestation payload in that same
  transaction, as specified, so the capture digest has no self-reference. Persist signature
  and completion event together. A caller-provided `consumed=True` has no field.
- [ ] Add crash tests at the three boundaries: start intent, captured commit and
  signed-but-uncommitted attestation. Only the captured/signing case can resume.

```python
def test_capture_cannot_publish_after_void(captured_case):
    store, record, envelope, void_approval, now = captured_case
    store.void(record.attempt_id, 'fixture invalidation', void_approval, now=now)
    with pytest.raises(ValueError, match='VOID'):
        store.publish_attestation(record.execution_id, envelope,
                                  expected_revision=record.revision)
    assert json.loads(store.status(record.attempt_id))['validity'] == 'VOID'
```

`captured_case` is a store-level fixture in `execution/conftest.py`: stage bounded
immutable TEST_ONLY artifacts, reserve/start/capture with exact hashes, produce
a fixture execution signature, and an operator-scope TEST_ONLY VOID approval.
This fixture tests transactions only; it is excluded from end-to-end acceptance.

- [ ] Verify integrity after reopening and corruption of transition fields,
  signature/object membership, event chain or duplicate execution rows.
- [ ] Run `.\fp.ps1 python -m pytest tests/ops/qualification/execution/test_store.py tests/ops/qualification/test_attempt.py -q --tb=short`.
- [ ] Review the no-redraw traces and commit the bounded increment if authorized.

## Task 3: Run unchanged N1 mechanics without a journal or signer

**Outcome:** A fixed worker entry point produces serialized real N1 outcomes and
cannot complete the authoritative attempt itself.

**Files:** Create `execution/{compute,budget,worker}.py`; modify
`qualification/production.py` to reuse extracted budget/compute helpers; create
`tests/ops/qualification/execution/{test_compute,test_worker}.py`. Read/reuse
`runner`, `provider`, `production_source`, `regime`, `model` and `adjudication`.

**Interfaces:**

```python
# budget.py: timestamps/counters are worker-owned, never request arguments.
class BudgetGuard:
    @classmethod
    def from_contract(cls, contract) -> 'BudgetGuard':
        return cls(contract.replay.budget)
    def remaining_wall_seconds(self) -> float:  # checks CPU/wall/peak memory
        return self.check_and_measure()['remaining_wall_seconds']

run_n1_compute(contract, source, budget: BudgetGuard) -> StageRun
run_worker(input_dir: Path, *, execution_id: str) -> bytes
```

`BudgetGuard.__init__(budget_spec)` captures monotonic wall and process CPU start;
`check_and_measure() -> dict` returns remaining wall, compute wall ns, CPU ns and
peak-memory bytes or raises `NeedsContext`. Reuse the existing peak-memory
implementation and final-check behavior. Initialize after source admission and
before `_ReplayProvider` creation. New output encoding is inside that budget.

- [ ] Create deterministic TEST_ONLY source fixtures using existing
  `composition_fixture.build_artifacts`: retain the current trading-port fixture
  for CONTINUE; use newly signed inert ports returning no orders for FAILURE
  (real replay yields unresolved paths). Recompute all affected artifacts, domain
  and approvals. No monkeypatch of replay, kernel or adjudicator generates outcomes.
- [ ] Compare old and extracted compute results on both fixtures: exact ordered
  outcome bytes and seeds must agree, excluding elapsed-time diagnostics that
  are genuinely nondeterministic. Record which fields are excluded and why.
- [ ] Extract only the N1 path: create `_ReplayProvider` from the admitted source,
  run `_run_stage(_stage_request(contract,'n1',remaining), provider,
  initial_state=_initial_state(contract), synthetic=domain.permits_synthetic)`, keep
  source proofs/probe, and apply budget checks around replay and after aggregation.
- [ ] Worker reconstructs/validates its context, requires exact derived plan, builds
  `ProductionSource`, computes, canonicalizes output, checks final budget and writes
  one result frame. Any exception/nonzero exit emits no success frame. Prohibit
  importing `store`, `signing`, `service`, `launcher` or legacy `AttemptStore`.

```python
def test_idle_real_source_is_execution_complete_but_statistically_fails(idle_compute_case):
    contract, source = idle_compute_case
    run = run_n1_compute(contract, source, BudgetGuard.from_contract(contract))
    assert all(row.status == 'UNRESOLVED'
               for _, rows in run.populations for row in rows)
    rules = contract.replay.decision_rules
    decision = adjudicate_stage(run, DecisionRules(
        rules.failure_ceiling, rules.alpha, rules.speed_target,
        rules.speed_horizon_sessions))
    assert decision.status == 'FAILURE'
```

`idle_compute_case` uses the newly signed inert-port fixture above, with existing
source admission/coverage and unchanged kernel; it returns validated contract and
factory-built source. It does not fabricate `StageRun` or `PathOutcome` values.

- [ ] Test malformed worker inputs, wrong plan, final CPU/memory/wall exhaustion
  and serialization failure. Retain existing budget regression suites.
- [ ] Run `.\fp.ps1 python -m pytest tests/ops/qualification/execution/test_compute.py tests/ops/qualification/execution/test_worker.py tests/ops/qualification/test_production.py tests/ops/qualification/test_production_budget_boundaries.py tests/ops/qualification/test_runner.py -q --tb=short`.
- [ ] Review output parity and commit if authorized. No policy constant changes.

## Task 4: Control actual launch and immutable output capture

**Outcome:** Only the supervisor selects/starts the worker; stopped completion
produces immutable service-owned bytes and launch facts, not a caller assertion.

**Files:** Create `execution/{launcher,archive}.py`,
`deploy/qualification/{Dockerfile.worker,profile.json,README.md}`, and
`tests/ops/qualification/execution/{test_launcher,test_archive}.py`.
Create `deploy/qualification/entrypoints/{worker,supervisor,g5}.py`: isolated
bootstrap scripts that add only immutable image roots (worker) or protected
installed roots (supervisor/G5) before importing their respective package entry
points. Include them in the release code closure.

**Interfaces:**

```python
create_worker(context: ExecutionContext, *, execution_id: str,
              input_dir: Path, profile: ExecutionProfile) -> str  # container ID
inspect_worker(container_id: str, *, context: ExecutionContext,
               profile: ExecutionProfile) -> bytes              # canonical facts
start_and_capture(container_id: str, *, spool_dir: Path,
                  profile: ExecutionProfile, maximum_wall_seconds: int) -> CapturedOutput
archive_capture(capture: CapturedOutput, *, archive_dir: Path) -> ArtifactBytes
stop_owned_worker(container_id: str, *, execution_id: str) -> None
```

`create_worker` does not start. The service records START_INTENT between inspection
and `start_and_capture`. The launcher has no signing function. Profile/image are
selected from installed context, never RPC arguments. `archive_capture` uses safe
regular files, fsync and content-addressed final paths; duplicate bytes are allowed,
different bytes under an existing digest are rejected.

- [ ] Build an allowlisted worker image context from required ordinary module
  roles and dependency locks. Do not relax the listener's root `.dockerignore` or
  copy private files into an image. Stage a separate build context; use the reviewed
  four-port loader to read contract-pinned port bytes from the input mount.
- [ ] Generate runtime/source manifest during build, then emit the external release
  manifest after obtaining actual image identity. Dependency versions and Python
  patch are observed, never guessed. Only matching manifests can be activated.
- [ ] Implement non-shell Docker argument construction from `ExecutionProfile` and
  inspect effective settings before start. Limit the Docker endpoint to protected
  configuration; ignore client `DOCKER_HOST`, PATH, PYTHONPATH and environment.
- [ ] Implement bounded stdout frame capture and stderr logging, daemon exit/OOM
  verification, timeout cancellation and no restart. Reject output after extra
  frames, missing EOF, malformed admission/result records or budget violations.

```python
def test_zero_exit_with_truncated_output_never_archives_success(launcher_case):
    capture = launcher_case.run_fault_worker('truncated_result')
    with pytest.raises(ValueError, match='frame'):
        archive_capture(capture, archive_dir=launcher_case.archive_dir)
```

`launcher_case` installs only a TEST_ONLY profile and fault image in a disposable
Linux test host. `run_fault_worker` selects an administrator-installed test image
variant, not a production RPC override. Its output cannot pass production release
enrollment. This fixture is defined in `tests/integration/qualification_boundary/conftest.py`.

- [ ] Test symlink/special-file output, spool mutation, wrong container label,
  stopped-image mismatch and client environment injection. Keep launch count and
  actual inspected settings in the test evidence.
- [ ] Run parser/archive unit tests with the launcher; run Docker launch tests on
  Linux. Mark local non-Linux cases explicitly unsupported, and require them in
  the Linux acceptance job rather than counting skips as acceptance.
- [ ] Review custody from input staging to final archive and commit if authorized.

## Task 5: Expose the narrow service and publish durable attestations

**Outcome:** qclient can request work, but cannot complete it, alter its journal,
or ask the service to sign supplied outcomes.

**Files:** Create `execution/{service,client,signing,release}.py`;
`deploy/qualification/{qualification-execution.service,instance.example.json}`;
`tests/ops/qualification/execution/{test_service,test_signing,test_release}.py`;
modify `qualification_cli.py` for explicit remote operations and historical status.

**Interfaces:**

```python
# service.py
handle_request(peer_uid: int, request_bytes: bytes) -> bytes
recover_service() -> None
# signing.py: imported only by service; signs a stored CAPTURED payload.
sign_captured(execution_id: str, *, store: ExecutionStore,
              credential_reference: str) -> bytes
# client.py
request(socket_path: Path, operation: str, fields: JsonObject) -> bytes
# release.py: administrator-only installation/staging, never request actions.
install_release(manifest_bytes: bytes, approval_bytes: bytes,
                *, instance_config: bytes) -> None
stage_bundle(source_dir: Path, *, instance_config: bytes) -> str
```

`peer_uid` is obtained by the server from Linux socket credentials; it is not read
from JSON. Main service startup reconstructs the protected context and store,
serves the socket, and dispatches a single active worker at a time in this release.
Concurrent requests are serialized by journal identity, not an in-memory flag.

- [ ] Implement SUBMIT_N1/STATUS/FETCH/STORE_RESULT/COMMIT_N1_RESULT/VOID with closed
  fields, role ACLs and bounded canonical framing. Reject every unknown operation.
  `handle_request` has no generic path/function/image/command forwarding.
- [ ] CLI commands are `submit-n1 --socket --attempt-id --bundle-sha256`,
  `service-status --socket --attempt-id` and `fetch --socket --attempt-id --sha256`.
  Existing `status JOURNAL` remains read-only historical inspection. No client
  command accepts private signing keys or journal write paths.
- [ ] Implement the launch sequence exactly: reserve -> create/inspect -> record
  container -> recheck approval/current validity -> durable START_INTENT -> start
  -> RUNNING -> capture/archive -> CAPTURED -> sign -> ATTESTED. Record the same
  authoritative start-intent instant used for approval validation as
  `authorized_at_utc`, separately from daemon-observed `started_utc`. Reject an
  attestation if actual start falls outside the approval interval or timestamps
  are missing/contradictory; add an expiry-between-intent-and-start regression
  asserting no attestation and no rerun.
- [ ] Archive the closed ordered artifact roles `plan` and `worker_result`.
  Make the attested bundle's original signed context bytes available through
  attempt-scoped FETCH; reject duplicate/unknown roles and context substitution.
- [ ] `sign_captured` loads payload from the store and verifies CAPTURED status,
  release/key enrollment and validity. It cannot accept arbitrary payload bytes.
  Only persisted ATTESTED envelopes are returned by FETCH.
- [ ] On recovery, abandon uncertain creation/start/capture without rerun; stop
  exact owned workers and mark IN_DOUBT. Resume only durable captured signing.
  Identical later submit returns stored state/receipt, never launches again.

```python
def test_client_cannot_promote_consistent_data_to_execution(service_client):
    response = service_client.raw_request({
        'operation': 'COMPLETE_CHECKPOINT',
        'attempt_id': 'fixture-attempt',
        'receipt_bytes_b64': base64.b64encode(b'{}').decode(),
    })
    assert response['error'] == 'UNKNOWN_OPERATION'
    assert service_client.launch_count() == 0
```

`service_client` starts the real service process with a generated TEST_ONLY
installation and a separate unprivileged peer. Its `raw_request` returns parsed
response bytes; `launch_count()` reads the fixture administrator's recorded Docker
events. Same-process mocks are permitted for unit parsing tests only.

- [ ] Add service credential/profile ownership checks, denied Docker socket/key/
  journal tests from qclient and worker, and client retry tests across restart.
  Service code is admin-owned; qexec's writable data directory cannot supply imports.
- [ ] Pin signing dependency in the explicit service build requirements. Keep
  signing imports out of stdlib-only listener images; rerun image import validation.
- [ ] Run service/release/signing tests and review API/OS permissions; commit if
  authorized. Installation on the user's real host remains a separate action.

## Task 6: Require captured execution at G5 and retire the bypass

**Outcome:** G5 accepts an attested real N1 failure and rejects an otherwise
consistent fabrication; passing N1 records progress only.

**Files:** Create `execution/g5.py` and `deploy/qualification/qualification-g5.service`;
modify `qualification/{seal,result_adjudication,orchestration}.py`;
create `tests/ops/qualification/execution/test_g5.py`; revise legacy seal/controller
tests and `composition_result_fixture.py` to distinguish inspection from acceptance.

**Interfaces:**

```python
validate_n1_evidence(context: ExecutionContext, attestation_bytes: bytes,
                     artifacts: ArtifactBytes, *, expected_attempt_id: str,
                     current_keys: dict, expected_revision: int) -> ValidatedEvidence
validate_result_envelope_v2(context: ExecutionContext, result_bytes: bytes, *,
                            attestations: dict[str, bytes], artifacts: ArtifactBytes,
                            expected_attempt_id: str, current_keys: dict,
                            expected_revision: int) -> ValidatedEvidence
authenticate_n1_evidence(context: ExecutionContext, attestation_bytes: bytes,
                         artifacts: ArtifactBytes, *, expected_attempt_id: str,
                         current_keys: dict, expected_revision: int,
                         credential_reference: str) -> tuple[ValidatedEvidence, bytes]
accept_n1(socket_path: Path, *, attempt_id: str) -> bytes
```

`accept_n1` is the protected qg5 entry point. It fetches the actual service record,
attestation and named artifacts, verifies them, derives/serializes the assessment,
signs the exact result under `ATTEST_E1_RESULT`, stores the proposed envelope and
requests commit. Neither client nor qg5 reads an arbitrary caller SQLite file.
Install G5 code and its locked virtual environment as administrator-owned files
whose actual code/runtime digests match the approved release. The one-shot service
manager/operator invocation runs under qg5 and accepts only the attempt ID; socket
and credential references come from protected configuration. qclient cannot select
an executable, import path, virtual environment or OS identity.
`authenticate_n1_evidence` is available only in the protected qg5 process;
it invokes captured-evidence verification on those original bytes before signing,
then returns canonical evidence and its authentication. It cannot sign an arbitrary
caller-constructed `ValidatedEvidence`. Returning a Python dataclass does
not independently grant authority.
`validate_result_envelope_v2` reconstructs the expected envelope through the same
captured-evidence path as `validate_n1_evidence` and compares every authoritative
field. It rejects unsupported stage sets before accepting claimed PASS. This is
the real verifier invoked by the raw-envelope negative test below. Both return
the canonical result bytes including signed journal revision and
checkpoint assessment; only the service can commit them.

- [ ] Write the six review cases as active acceptance failures: fabricated outcomes
  with direct legacy consumption; consistently wrong seeds; voided attempt; caller
  descriptor injection; shared key ID; shared public bytes under different IDs.
- [ ] Parse outcome bytes into fresh internal values and use `adjudicate_stage`
  unchanged. Enforce exact source/seed/depth/order from the plan. Remove caller
  `PathOutcome`, callback, live `FrozenAdjudicator` and writable store parameters
  from v2 acceptance. G5 never `exec`s retained source or loads private ports.
- [ ] Build v2 envelope from captured evidence only. FAILURE yields COMPLETE/FAIL
  LEGALITY/N1; CONTINUE yields PARTIAL/NONE. Both bind the N1 attestation hash.
  Service stores deterministic CUTOFF and assessment atomically; only failure
  completes TB_E1. N2/PART_A requests fail in this release.
- [ ] `COMMIT_N1_RESULT` enforces qg5 role, trusted signature, current approval/key
  status, exact attestation/attempt binding, expected revision and VALID campaign
  in the committing transaction. Do not call old `_commit_validated_result` on
  caller-held objects. Implement conflict retry as refetch/revalidate, never redraw.

```python
def test_full_pass_cannot_borrow_only_n1_attestation(g5_case):
    context, attestation, objects = g5_case.completed_n1()
    forged = g5_case.propose_full_pass(attestation, objects)
    with pytest.raises(ValueError, match='UNSUPPORTED_ATTESTED_CHECKPOINT_SET'):
        g5_case.accept_raw_envelope(context, forged, objects)
```

`g5_case` is a verifier-unit fixture with generated TEST_ONLY signed objects;
`propose_full_pass` creates an envelope claiming later stages without corresponding
attestations. `accept_raw_envelope` invokes the real v2 envelope verifier, not a
mock. Task 7 repeats this attack through the actual qg5/service boundary.

- [ ] Active v1 authenticate/commit/seal and in-process production routes now
  reject with `EXECUTION_ATTESTATION_REQUIRED`; retain explicit historical
  inspection/pure simulation APIs with no authority-bearing return path. All v2
  full PASS seals reject the unsupported checkpoint set. No legacy bypass flag.
- [ ] Test stale validity and exact-depth approval expiring after start. Historical
  attestation remains inspectable; expired/revoked authority cannot gain acceptance.
- [ ] Run G5 tests plus existing exact-decimal, source, replay and key-binding
  regressions; explicitly update tests whose former positive fixture was fabricated.
- [ ] Review the protected qg5 signing/data flow and commit if authorized.

## Task 7: Prove the real boundary and make regressions gate acceptance

**Outcome:** A revision-bound Linux acceptance run establishes the actual service,
container, filesystem and G5 contracts, with all critical negative cases enforced.

**Files:** Create `tests/integration/qualification_boundary/{conftest,test_n1_flow,test_permissions,test_recovery,test_fabrication}.py`,
`scripts/check_qualification_authority_boundaries.py`,
`tests/test_qualification_authority_boundaries.py`,
`.github/workflows/qualification-execution-boundary.yml`,
`scripts/qualification_boundary_verification.py`; modify `scripts/gates.yml`,
`scripts/README.md` and deployment README. Update the prior simplified-qualification
plan's execution/API sections by reference after this design is approved.

**Integration fixture producer:** The new Linux verification script provisions
qclient/qexec/qg5 identities and protected temporary roots on a disposable CI VM,
builds the worker image from an allowlisted context and installs protected
supervisor/G5 code and locked environments, generates TEST_ONLY keys,
signs/releases their exact observed manifests, stages the real synthetic source bundles,
and starts the supervisor. It launches qclient/qg5 under different UIDs and retains
private test artifacts outside public logs. It never provisions production keys.
Cleanup checks exact owned paths/container IDs and does not follow untrusted paths.

Fixture `boundary_host` exposes `submit(kind)`, `wait_attested(attempt_id)`,
`assess(attempt_id)`, `status(attempt_id)`, `launch_count(attempt_id)`,
`restart_service()`, `kill_service_at(state)`, and `void(attempt_id)`; these operate
real processes/RPC. `kind` selects the signed CONTINUE or inert-port FAILURE
bundle from Task 3 before submission. State fault triggers are test-process
orchestration, not production RPC parameters or arbitrary callback injection.

```python
def test_real_failure_survives_restart_without_redraw(boundary_host):
    attempt = boundary_host.submit('idle_failure')
    boundary_host.wait_attested(attempt)
    receipt = boundary_host.assess(attempt)
    assert receipt['completion'] == 'COMPLETE'
    assert receipt['verdict'] == 'FAIL'
    boundary_host.restart_service()
    assert boundary_host.status(attempt)['result_sha256'] == receipt['result_sha256']
    assert boundary_host.launch_count(attempt) == 1

def test_real_passing_n1_cannot_become_e1_pass(boundary_host):
    attempt = boundary_host.submit('trading_continue')
    boundary_host.wait_attested(attempt)
    receipt = boundary_host.assess(attempt)
    assert receipt['completion'] == 'PARTIAL'
    assert receipt['verdict'] == 'NONE'
    assert receipt['n1_decision'] == 'CONTINUE'
    assert boundary_host.status(attempt)['next_checkpoint'] == 'UNSUPPORTED'
```

- [ ] Run both positive flows using the unchanged source/replay/kernel mechanics.
  Record exact input/plan/image/output/attestation/result hashes and journal events.
- [ ] Run every spec section-10 rejection/restart/race case, including real
  filesystem/socket permissions. Require launch counts from observed container
  events, not fixture assumptions. Force VOID races on both sides of commit order.
- [ ] Boundary gate statically rejects worker/compute imports of signer/store/
  launcher/service; g5/verification imports of worker/signer/store/launcher; calls
  from old orchestration to active completion; and public RPC completion/sign
  operations. Exempt only named service-owned adapters, not broad test flags.
  This catches ordinary regressions; OS tests establish the security boundary.
- [ ] Add the gate once to `scripts/gates.yml`, with AST scanner tests for aliases
  and newly introduced direct imports. Use existing gate conventions.
- [ ] The Linux CI workflow creates its own validated operations environment,
  runs the launcher doctor, then runs the boundary verification script. Critical
  isolation tests cannot silently skip in that job. Local Windows unit tests may
  skip Linux integration with an explicit unsupported-platform reason.
- [ ] Use the existing verification recorder to retain revision, environment,
  profile/image digests, JUnit, stream capture, source stability and owned cleanup.
  Missing Docker, UID provisioning or an accepted runtime image is a failed setup,
  not successful acceptance. Do not reuse owner-controlled Docker harness results
  as a substitute for qclient permission tests.

Final verification commands, from the implementation checkout:

```powershell
.\fp.ps1 doctor
.\fp.ps1 python -m pytest tests/ops/qualification tests/ops/test_phase3_provenance_acceptance.py tests/test_qualification_authority_boundaries.py tests/ops/test_qualification_isolation.py -q --tb=short
.\fp.ps1 check
```

Linux boundary verification (disposable VM; script requires administrator test
setup privileges, not available to the simulated qclient):

```bash
python -I scripts/fp.py doctor
python -I scripts/fp.py python scripts/qualification_boundary_verification.py --test-only
```

`qualification_boundary_verification.py` runs selected integration tests with
`sys.executable`, propagates any failure/critical skip, records interpreter and
revision, and cleans up only its provisioned resources. It consumes the canonical
ExecutionProfile; it does not maintain a second copy of container security flags.

- [ ] Rerun listener/daemon image import tests because they copy contract and trust
  modules. Signing/service dependencies must not leak into stdlib-only images.
- [ ] Review the combined diff and acceptance traces; record remaining deployment
  prerequisites without describing them as completed capabilities. Commit the
  completed boundary only if authorized; PR creation/merge is separate scope.

## Self-review and handoff

Coverage: spec sections 1–5 -> Task 1; 6 -> Tasks 3–5; 7 -> Tasks 2/5;
8 -> Tasks 1/5/6; 9 -> Tasks 1/2/6; 10 -> Task 7; 11 -> Task 7 documentation.

Before declaring implementation accepted, trace these concrete sequences through
the actual processes and persisted records: losing N1 to terminal FAIL; passing
N1 to incomplete progress; forged coherent evidence to rejection; crash after
START_INTENT to IN_DOUBT without relaunch; crash after CAPTURED to identical
attestation publication; VOID winning/losing a transaction race; repeated request
after lost response returning identical execution identity. An API unit test or
signature fixture alone cannot close these traces.

Production dependencies remain: operator-approved complete multi-checkpoint
release, isolated host provisioning, real enrolled keys, actual retained source
acceptance, F1 and exact-depth approval, approved budgets and later qualification/
deployment gates. N2/Part A attestation and end-to-end cumulative budget persistence
must be designed as the next slice before any actual qualification execution.

This plan does not solve malicious approved-code correctness, host administrator
compromise or offline revocation discovery. Its guarantee is supervised execution
under the explicit trust model, with consistency and acceptance kept distinct.
