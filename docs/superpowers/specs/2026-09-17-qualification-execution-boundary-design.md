# N1 execution attestation boundary

Status: proposed design for the user's requested vertical checkpoint, 2026-09-17.
Planning only. No implementation, deployment, F1 freeze, exact-depth execution,
production signature, admission, or live activation is authorized by this file.

Baseline inspected: PR 415, `5e935c89e0c004ae76717765f91889e9b8257b7a`, in
`.worktrees/phase3-post413-integration`. The coordinating implementer owns combined
acceptance. Rebase the design against the selected implementation revision before
coding; preserve unrelated worktrees and changes.

## 1. Decision and acceptance boundary

Move N1 dispatch, execution capture, journal finalization and execution signing
behind a controlled service. Require its signed attestation and captured output
bytes at G5. Keep source loading, sampling, replay, kernel evaluation and exact
statistical decisions unchanged.

The first slice supports exactly N1 and its deterministic CUTOFF record:

* An executed N1 failure reaches an authenticated, durably committed terminal
  E1 FAIL through G5, with LEGALITY/N1 as its result prefix.
* An executed N1 pass receives an attested checkpoint and a CONTINUE decision.
  It remains an incomplete campaign; this release cannot launch N2 or Part A.
* A full E1 PASS cannot be accepted or sealed by this release. Adding attestations
  to only N1 must not leave an unattested N2/Part A route accepted by G5.

No real qualification should start under this N1-only release. A real passing N1
would be stranded: subsequent stages and cumulative resource accounting across
them are not implemented. Synthetic acceptance demonstrates the vertical design;
production execution requires the later complete campaign release and its own
approvals. Production authority schema/rejection tests do not run real sources.

The invariant is: **matching evidence can establish consistency; only the
controlled execution owner can attest an execution; G5 decides the result.**

## 2. Current implementation and required interface changes

| Existing code | Current responsibility/problem | Proposed treatment |
|---|---|---|
| `qualification/attempt.py` | Writable journal; caller can start, consume and complete checkpoints | Service-private schema-v4 writer; no caller completion endpoint |
| `qualification/production.py` | Executor owns source and writable store; consumption precedes computation | Extract the N1 compute adapter and budget guard; worker receives no store |
| `qualification/orchestration.py` | Builds seed records, executes, accepts returned objects, completes journal | Canonical plan derivation shared with service/G5; legacy production entry fails closed |
| `qualification/runner.py`, `provider.py`, `replay.py`, `regime.py` | Actual deterministic mechanics | Retain behavior and RNG formula; call from pinned worker |
| `qualification/seal.py` | G5 consumes caller objects and a caller-supplied store | V2 G5 consumes signed captured bytes; service commits under current validity |
| `qualification/result_adjudication.py` | Pure decisions mixed with live-module reflection | Reuse pure decisions; v2 does not execute retained source to establish provenance |
| `qualification/trust_domain.py`, `contract.py` | Freeze, result and seal roles; closed v1 schemas | V2 binds execution key, service/release identity and required attestation policy |
| `qualification_cli.py` | Read-only local journal status | Add service submit/status/fetch; retain local inspection as historical information |

`ProductionExecutor._admit()` currently invokes `consume_checkpoint_dispatch()`
before `_run_stage`. That consumed flag must not be renamed into an execution
proof. The new attestation is created after captured output has been finalized.

## 3. Trust model and selected platform

Use a dedicated Linux service deployment with Docker Engine for worker isolation.
Windows remains supported for pure unit/development tests, not as evidence of this
OS permission boundary. Existing Docker verification scripts are test harnesses,
not production execution authorities.

Trusted: host administrator, kernel/container runtime, approved supervisor and G5
releases, the approved worker/port implementation, and enrolled approval keys.
Untrusted: the requesting agent/client process, its Python objects, workspace,
paths, proposed results, environment variables and retry behavior. The worker has
no authority to write the journal or sign. Its code is reviewed and pinned; this
design does not prove correct computation by a malicious approved worker or
protect against a compromised administrator/kernel.

The claim is supervised execution under these assumptions, not a cryptographic
proof of arbitrary computation. Source hashes and reflection remain integrity
diagnostics where useful; they cannot promote caller data to execution authority.

| Principal | Allowed | Forbidden |
|---|---|---|
| `qclient` | Submit approved bundle identity; read permitted status/artifacts | Service key, journal, Docker socket, service/worker code edits, completion API |
| `qexec` supervisor | Verify requests, own attempt DB, control container launch, capture outputs, sign execution | Issue F1/exact-depth approvals, decide statistical acceptance, hold result/seal keys |
| Worker container | Read exact input snapshot, run fixed entry point, emit framed output | Network, journal, signing keys, Docker socket, caller workspace, writable code |
| `qg5` | Read immutable attestation/artifacts, run pinned adjudicator, sign result acceptance | Execution-signing key, direct journal writes, caller callbacks or source execution |
| Operator/administrator | Enroll reviewed releases/keys, install service, stage retained bundles, invalidate attempts under operator authority | These powers are outside the untrusted-client threat model |

Service code/config are administrator-owned and not writable by qclient or worker.
qg5 uses a distinct OS identity and protected code/key path. qexec's access to the
Docker daemon makes it part of the privileged trusted computing base. No general
Docker operation is exposed through its RPC interface. Docker documents why
daemon control must be limited to trusted users:
[Docker Engine security](https://docs.docker.com/engine/security/).

The supervisor and G5 run from administrator-installed, immutable code and locked
virtual environments whose exact manifests are approved in the release. The
worker runs in the pinned container image. G5 is a one-shot protected entry point
invoked by the operator/service manager under qg5; it accepts only an attempt ID
and reads its configured service socket. The initial slice does not give qclient
an arbitrary command runner or the ability to assume qg5's identity. The Linux
test administrator invokes this same entry point under the real qg5 UID.

Alternative rejected for this slice: a same-user subprocess with a private Python
token. The caller could still modify its code/state or reach its credentials.
A remote managed execution service could implement the same protocol later but
adds infrastructure not needed for the first Linux boundary test.

## 4. Configuration, release and authority binding

Add one canonical, closed `ExecutionProfile` in
`ops/c1_rail/qualification/execution/profile.py`. Deployment variants compose its
security settings, while an instance configuration supplies socket/storage paths,
UIDs and credential references. Do not duplicate flag lists in worker, service,
Docker tests and deployment documentation. Consumers validate the resolved profile.

The administrator-approved release manifest, generated after image build, records:

* schema `qualification_execution_release/v1`, immutable release ID and profile
  SHA-256; profile includes protocol version, supported checkpoints `[N1]`, explicit
  input/output/log byte limits, worker UID, isolation settings and operational limits;
* worker image content ID/digest, supervisor code/runtime manifest digest and G5
  code/runtime manifest digest; exact Python patch/platform and dependency-lock
  hashes belong to each runtime manifest;
* ordinary first-party source hashes, fixed worker entry point, and the four
  permitted contract-bound port loader roles; no other input may be imported;
* authority class and service ID; `N1_ONLY` capability and production execution
  disabled in this initial release;
* execution public-key fingerprint and distinct result/freezer/sealer fingerprints.

Do not bake this manifest into the image whose digest it contains. Generate it
after building; its canonical bytes are approved and staged separately. The frozen
contract includes it as the `execution_release` artifact. Source-role hashes in
the contract must agree with the image release's ordinary-code inventory; private
ports remain exact contract-bound retained bytes loaded by the reviewed loader.

The release manifest is approved under the existing detached-approval format with
scope `APPROVE_EXECUTION_RELEASE`; the subject and contract digest fields both
bind its SHA-256. The administrator's protected release-approval registry is the
trust root at installation. Installation validates once, activates that exact
manifest digest, and the service checks the installed digest and image identity
before every dispatch. Runtime requests cannot select or override a release.
The release classifies ordinary code into supervisor, worker and G5 closures and
their shared dependencies. Mandatory-role tests derive/check each closure from
the actual entry points. New execution modules must be included; the old 68-module
inventory must not silently become the new release's completeness definition.
V2 G5 verifies release identity without executing the worker closure in its process.

V2 domain adds `execution_key_ids`, `execution_service_id`,
`execution_release_sha256`, `required_attested_checkpoints=[N1,N2,PART_A]`.
V2 contract adds required artifact `execution_release`, and binds the v2 domain.
Keys for execution, freeze, result and seal must be disjoint by both ID and actual
public-key fingerprint. The trust domain cannot enroll an unknown execution key:
it must also match the protected service-release registry.

All approval, release, contract and attestation authority classes must agree.
TEST_ONLY fixtures can use only TEST_ONLY installations. There is no request flag
that enables test authority on an OPERATOR service. Existing workload/depth and
source controls remain enforced; a new trust schema does not relax them.

Secrets stay outside versioned configuration. The execution key is readable only
by qexec (and trusted administrator), result key only by qg5. Neither is mounted
into the worker. Production enrollment and deployment are later operator actions,
not steps performed by this planning task or by automatic synthetic acceptance.

## 5. Input and execution plan

An administrator stages a retained bundle into the service-owned content-addressed
store. The staging command copies and verifies bytes; it never imports modules.
The bundle index is a canonical sorted role/path/hash/length inventory with only
regular files and safe relative paths. Existing signed G1 artifacts, contract,
domain/release approvals and exact-depth approval are retained without alteration.
Its identity is the hash of this index. Data producers remain the existing source,
calendar, settings and approval owners; staging supplies custody, not authority.

RPC requests name only the bundle digest and signed attempt identity. No arbitrary
host path, output root, Python object, executable, seed, environment or container
argument crosses this request interface. The service reserves its own output root.
The caller cannot change staged bytes after admission.

`derive_n1_plan(contract, *, attempt_id, exact_depth_approval_sha256) -> bytes`
returns canonical `qualification_checkpoint_plan/v2` bytes with:

* contract/domain/release identities, attempt ID, checkpoint N1, authority class;
* exact FULL/H1/H2 depths, horizon, initial-state and replay configuration digests;
* ordered decision-path addresses and complete seed records, including source-pool
  SHA-256 derived from each exact frozen population;
* separately labeled existing `probe/FULL/0` seed and existing FULL/H1/H2 source
  proof work; these are not decision samples or independently repeatable endpoints;
* exact original budget fields and a mechanics-version identity.

Reuse `regime.domain_seed` unchanged. Preserve its existing probe purpose and all
domain discriminators; do not silently switch to a different probe seed. The
service, worker and G5 each derive the expected plan from their validated contract.
They compare complete canonical bytes, not mutually supplied hashes. Worker output
does not determine what plan was authorized. Centralize the seed-record helper
currently in orchestration and retain fixed-vector tests independently of it.

The existing source factory admission becomes an explicit worker admission record
binding contract, retained inventory and successful source construction. LEGALITY
PASS in the N1 envelope is permitted only with that captured record; no new
statistical legality algorithm is introduced.

## 6. Transport and worker custody

Use a local Unix-domain socket with peer-credential authorization. Requests and
responses are length-prefixed canonical JSON: 4-byte unsigned big-endian length,
then exactly that many UTF-8 bytes. Limits come from the resolved profile; duplicate
fields, trailing frames, malformed numbers and unknown fields fail closed. One
request per connection. Remote clients use an operator-configured transport to
the authorized client identity; no public HTTP endpoint is added.

Allowed operations:

| Operation | Authorized peer | Effect |
|---|---|---|
| `SUBMIT_N1 {attempt_id,bundle_sha256}` | qclient | Verify/freeze request identity; durably dispatch at most once |
| `STATUS {attempt_id}` | qclient/qg5 | Read state; no boot claim or mutation |
| `FETCH {attempt_id,object_sha256}` | qclient/qg5 per artifact privacy | Return only an object belonging to that attempt |
| `STORE_RESULT {attempt_id,envelope_bytes_b64}` | qg5 | Retain a bounded proposed v2 envelope; grants no authority |
| `COMMIT_N1_RESULT {attempt_id,envelope_sha256,authentication_bytes}` | qg5 | Atomically record a G5 N1 assessment; only a terminal failure completes E1 |
| `VOID {attempt_id,reason,operator_approval_bytes}` | operator peer | Validate scoped invalidation; durably mark VOID |

There is no `complete`, `consume`, `sign`, `set_verdict` or arbitrary upload RPC.
G5 stores a proposed envelope using its role-specific content-store interface;
this stores bytes only and cannot create an execution record. Artifact membership,
size and privacy checks apply equally to proposal storage. qclient cannot use it.

VOID requires a domain-enrolled freeze/operator key and scope
`VOID_QUALIFICATION_ATTEMPT`. Its canonical subject is
`{schema:qualification_void_subject/v1,attempt_id,contract_sha256,trust_domain_sha256,reason}`;
the detached approval binds that subject and the actual frozen contract. The
service derives and verifies the subject from its stored campaign and request
reason, including current expiry/revocation. A valid signature for another
attempt/reason cannot invalidate this one.

The supervisor uses an explicit argument vector and fixed Docker endpoint. It
creates a stopped container with a durable execution ID label, inspects the
effective image/entrypoint/mount/security configuration, records its ID, durably
records START_INTENT, and starts that exact container once. It never invokes a
shell or forwards caller environment variables.

Worker profile: pinned image content identity, non-root UID, read-only rootfs,
no network, all capabilities dropped, no-new-privileges, no privileged/host
PID/IPC mode, bounded tmpfs scratch, PID/memory limits, no restart policy, no
Docker socket, no secret/journal mounts. Inputs are service-owned read-only
snapshots; interpreter import roots and entrypoint come from the image. Do not
mount the development checkout. Exact options are rendered from the profile and
checked against Docker inspection; see the official
[container run reference](https://docs.docker.com/reference/cli/docker/container/run/).
All three trusted entry points use an isolated Python invocation and an
administrator-owned bootstrap that adds only immutable application roots: image
layers for the worker, protected installed code for the supervisor and G5.
Neither current working directory nor PYTHONPATH, user site packages or retained
data directories may supply ordinary imports. The four explicit port-loader roles
are the sole reviewed exception and load only their exact contract-bound bytes.

The worker emits exactly one bounded canonical result frame on stdout; logs use
bounded stderr. The supervisor captures these streams into private spool files.
The result frame contains execution ID, plan SHA-256, admission record, ordered
FULL/H1/H2 outcomes, path inventory and final budget observations. Each outcome is
a closed JSON record; objects, pickle and executable serialized values are banned.
The worker reports no authoritative PASS/FAIL decision.

Finalize only after stream EOF, daemon-confirmed container exit, exit code zero,
no OOM/timeout, exact output shape/count/plan binding and final worker budget check.
Reject truncated, duplicate or extra frames. Capture diagnostics separately; they
cannot masquerade as result frames. The supervisor copies finalized bytes to its
immutable archive and fsyncs files/directories before preparing a completion.
No caller/worker retains a writable alias to the archived files. Fetching an
artifact never imports it or follows artifact-supplied paths.

Preserve the current compute budget starting point immediately before provider
construction after source admission, including source proofs, probe, kernel,
aggregation and worker serialization. Supervisor enforces an outer wall deadline
of the profile's admission limit plus the contract's compute-wall budget plus
the profile's capture limit. Record that total separately from the worker's
compute-phase wall/CPU/peak-memory observations; do not label worker telemetry as
independently measured host metrics. Separate finite admission/capture limits
bound setup and transport. Docker CPU rate
limits are not a substitute for cumulative CPU-seconds checks. Use worker process
CPU/peak-memory checks from the existing executor, preserving final checks, plus
daemon OOM/exit facts. Ambiguous accounting never earns a completion attestation.

## 7. Durable state, concurrency and recovery

Use one service-owned SQLite schema-v4 journal, with campaign-scoped event chains
and a unique key `(trust_domain_sha256, contract_sha256, approved_attempt_id, checkpoint)`.
It is the sole active state owner; old per-campaign AttemptStore databases are
historical only. The unique index prevents another record for the same execution.
Requests differing only in client request IDs cannot create another attempt.
Different attempt approvals remain a governance decision; this slice grants none.

Schema v4 stores execution ID, plan/request digests, selected release, start intent,
container ID, spool/archive identities, attestation payload/signature and a
monotonically increasing journal revision. Campaign validity remains separate.

| State | Allowed transition and owner | Failure/restart disposition |
|---|---|---|
| `PENDING` | Service verifies approvals/bundle and reserves dispatch | Rejected admission has no outcome-bearing execution |
| `DISPATCHED` | Service creates/inspects one stopped container | Recovery may abandon; never create replacement after uncertain creation |
| `START_INTENT` | Durable intent before starting exact container | Any uncertainty becomes `IN_DOUBT`; never call start again |
| `RUNNING` | Observed start; service captures exclusive output stream | Crash, lost capture, timeout or abnormal exit becomes `IN_DOUBT`/`ABORTED` |
| `CAPTURED` | Service has durable immutable output + verified exit facts | Signing may resume from this exact payload without rerun |
| `ATTESTED` | Transaction persists signature and completion event | Identical submit returns stored receipt; no repeated execution |

`ABORTED` and `IN_DOUBT` are execution states, never statistical FAILURE. A valid
run with losing paths can be ATTESTED and later adjudicated FAIL. N1 statistical
PASS can only be CONTINUE, not E1 PASS.

Use `BEGIN IMMEDIATE`, unique constraints and expected-revision checks. Concurrent
identical submissions return the same execution identity; conflicting bindings
are rejected. No execution begins while holding a long-running database lock.

Two-phase local completion:

1. After durable capture, transaction verifies validity/revision and records
   CAPTURED with the exact unsigned payload. Commit it before signing.
2. Service signs only that stored payload using the enrolled execution key.
3. Transaction rechecks validity, execution identity and unchanged captured payload,
   persists signature and ATTESTED event atomically. A racing VOID prevents commit.
4. Only committed attestations are served. Crash after signing but before commit
   permits re-signing identical stored bytes; it never permits re-execution.

Avoid a capture hash cycle: the capture event binds finalized object hashes,
launch/exit facts and plan identity, excluding the unsigned payload's own hash.
The store appends that event, then constructs the unsigned payload with the
resulting event digest/revision in the same CAPTURED transaction. The later
ATTESTED event binds the signed envelope hash.

On service restart, kill/contain any exact owned still-running container before
marking IN_DOUBT; never adopt an incomplete stdout stream as a result. If container
identity cannot be established, block that campaign and report operator action.
Do not remove unrelated containers. A durable CAPTURED record may finish signing
only if validity and key/release admission remain valid. Unreferenced spools are
diagnostic artifacts, not recoverable proof of successful execution.

## 8. Attestation and G5 acceptance

The execution envelope has closed fields `{schema,payload,signature}`. Its payload:

```text
schema = qualification_execution_attestation_payload/v1
scope = ATTEST_CHECKPOINT_EXECUTION
authority_class, service_id, execution_id, attempt_id, checkpoint = N1
contract_sha256, trust_domain_sha256, exact_depth_approval_sha256
execution_release_sha256, profile_sha256, plan_sha256
retained_bundle_sha256, runtime_manifest_sha256, worker_image_digest
dispatch_event_sha256, capture_event_sha256, capture_revision
authorized_at_utc, started_utc, completed_utc
completion = COMPLETED
artifacts = ordered [{role, sha256, byte_length}]
observations = {exit_code, oom_killed, supervisor_wall_ns,
                worker_compute_wall_ns, worker_cpu_ns, worker_peak_memory_bytes}
```

Signature is Ed25519 over canonical payload bytes with algorithm, key ID and
canonical base64 signature. Key scope is `ATTEST_CHECKPOINT_EXECUTION`; fingerprints
must match both domain and installed release. No `PASS` field exists. Dispatch
and capture events precede the attestation, avoiding a digest cycle. The later
ATTESTED event binds its envelope hash.

The closed artifact inventory contains exactly `plan` and `worker_result`, each
once, in that order. The worker result embeds admission, path inventory and budget
observations; diagnostics are excluded. The retained bundle index identifies the
original contract, domain, release and approvals by digest. G5 fetches those exact
bytes through attempt-scoped membership, verifies their signatures and bindings,
and never substitutes a caller-selected context for the attested bundle.

`authorized_at_utc` is the protected-clock instant persisted with START_INTENT;
`started_utc` is the daemon-observed container start, not the intent timestamp.
Recheck that the observed start falls within the approval validity interval before
attesting. Expiry between intent and actual launch rejects completion attestation;
the attempt remains consumed and cannot be retried. Missing or contradictory
timestamps are indeterminate execution, never successful completion.

Historical execution attestations do not expire merely because time passes.
Approvals must be valid at authoritative admission/start instants. Preserve the
existing additional exact-depth approval validity check at G5 acceptance, using
the protected G5/service clocks rather than a caller-supplied time. Current key
revocation/domain/release policy is checked at acceptance. An approval that expires
after launch can leave historical execution evidence, but cannot yield newly
accepted qualification evidence after expiry. It grants no rerun or automatic
extension. Changing that approval policy is outside this structural repair.

G5 v2 runs in its own protected process and:

1. Parses original frozen contract/domain/release bytes and retained approvals.
2. Verifies attestation signature, authority, role fingerprints, service/release,
   attempt/checkpoint and exact artifact bytes/lengths.
3. Independently derives the N1 plan and compares exact seed/population inventories.
4. Parses immutable captured outcome bytes into fresh internal values; accepts no
   caller `PathOutcome`, `FrozenAdjudicator`, callback or `AttemptStore` argument.
5. Runs the unchanged N1 statistical decision. Captured losing paths stay losing.
6. Produces result-envelope/v2 with `execution_attestations={N1: envelope_sha256}`.
   A failed N1 has COMPLETE/FAIL and LEGALITY/N1; a passing N1 has PARTIAL/NONE
   plus its checkpoint CONTINUE assessment. N2/PART_A content is unsupported.

V2 retains the applicable existing result-envelope fields, replaces the raw
SQLite-file hash with `journal_revision`, and adds
`execution_attestations` plus `checkpoint_assessment={checkpoint:N1,decision}`.
These fields are covered by result authentication. G5 constructs the expected
envelope from captured bytes; validation of an externally proposed envelope must
compare it to that reconstruction. Service-returned assessment receipts expose
`completion`, `verdict`, `n1_decision`, `result_sha256` and current validity;
these are derived from the committed envelope, not independently editable labels.
STATUS supplies the authoritative pre-commit journal revision. A
stale assessment cannot commit, even if its execution signature remains valid.

The service records deterministic CUTOFF from the approved contract and the signed
G5 assessment, referencing N1 attestation and decision digests. CUTOFF has no
execution attestation because it contains no new replay; arbitrary caller cutoff
receipts are forbidden. Its recording and terminal failure commit occur in one
transaction. For passing N1, record CUTOFF and progress without completing TB_E1.

`COMMIT_N1_RESULT` verifies qg5 peer, result-scope signature and key fingerprint,
exact attestation membership and result prefix, then checks current validity and
expected journal revision in the same transaction as CUTOFF/result recording.
A stale snapshot is not an acceptance capability. VOID winning the transaction
race rejects commit; commit winning records a historical result that a later VOID
invalidates for future use. Idempotent retries return the stored response only
when bindings match; they still disclose current invalidation.

G5 pure validation returns `ValidatedEvidence`, never an execution capability or
durable qualification decision. Only the authenticated service commit establishes
the accepted result's current journal relation. Live use requires current status;
an offline signed record proves historical facts, not absence of later invalidation.

All complete PASS/seal entry points fail `UNSUPPORTED_ATTESTED_CHECKPOINT_SET` in
the N1-only release. Future sealing must use the same transactional validity/
publication pattern and separate sealer key; this slice does not implement it.

## 9. Compatibility and migration

New authorities use domain/v2, frozen-contract/v2, result-envelope/v2 and attempt
schema v4. Detached approval encoding can remain v1 with the new scoped subjects.
The preflight binding gains a v2 schema and service-owned output identity. Exact
depth subject already binds contract digest, so the release binding travels with it.

No automatic v3-to-v4 in-flight migration; old artifacts cannot acquire execution
attestations retroactively. Keep read-only v1/v3 inspection and pure mechanics
tests. Historical validation must be labeled evidence inspection and cannot call
active authentication/commit/seal functions. Existing in-process production
`run_production_e1` and caller checkpoint-completion paths reject active v2 use.
Do not add `allow_legacy` or `skip_attestation` switches to an authority boundary.

Update tests that fabricated outcomes to test evidence consistency only. At least
one equivalent fabrication must now reach the real G5 acceptance endpoint and be
rejected. TEST_ONLY reduces fixture workloads, not required provenance checks.

## 10. Required acceptance cases

| Case | Expected observable outcome |
|---|---|
| Real synthetic source -> worker -> losing N1 -> G5 -> commit | One launch; attested exact bytes; COMPLETE/FAIL; reopened store retains result |
| Real synthetic source -> passing N1 | ATTESTED/CONTINUE; no N2 launch; no E1 PASS/seal |
| Caller fabricates all matching outcomes, hashes and receipts | G5 rejects missing/invalid execution signature; no result commit |
| Caller requests arbitrary image/command/path/seed/complete/sign | Closed API rejects; no Docker call or journal completion |
| Caller edits its Python outcome class or verifier | Protected worker/G5 unaffected; fabricated outputs still rejected |
| Seed/source-pool/namespace changed consistently | Independently derived plan mismatch, even with otherwise valid TEST_ONLY signature |
| Distinct signing IDs share key bytes | Domain/release enrollment rejected |
| Worker attempts journal/key/socket/code write | Real OS/container permission rejection; no authority material exposed |
| Duplicate submit, concurrent submit, reconnect after lost response | Same execution ID and at most one start; exact receipt replay only |
| Kill after start intent/before captured commit | IN_DOUBT, no attestation and no redraw after restart |
| Kill after CAPTURED/before ATTESTED | Resume signing exact captured payload; launch count remains one |
| VOID races with attestation/acceptance | Transaction winner determines history; VOID prevents any later acceptance |
| Exit zero but partial/extra output, OOM, budget overrun, corrupt spool | No COMPLETED attestation; diagnostic retention only |
| Expired approval before start | No start; no attestation; no replacement attempt implied |
| Approval expires after authorized start | No accepted G5 result after expiry; historical execution evidence grants no rerun |
| V1 evidence or mixed TEST_ONLY/OPERATOR artifacts | Active v2 acceptance rejects; inspection remains available |
| Full PASS containing only N1 attestation | Reject unsupported/missing N2/PART_A provenance |

Run the decisive tests against real separate processes/UIDs and real containers
on Linux. Mocks can test parsers/state machines but cannot satisfy isolation or
launch-to-G5 acceptance. Capture launch IDs, artifact digests, process identities,
permission failures and journal transitions with the tested revision. No access
to private sources is necessary for these engineering cases.

## 11. Implementation and remaining operational dependencies

Implementation sequence and exact interfaces are in the companion plan. A fresh
isolated worktree is required at implementation time, based on the accepted PR
415 successor. This document does not edit the reviewed branch.

Required operational producers are explicit: administrator provides the isolated
Linux host, identities, installed release and socket permissions; build tooling
produces image/runtime/profile digests; freeze authority approves release/domain/
contract and depth; existing source owners supply retained artifacts; qexec issues
execution attestations; qg5 issues result authentications. Unavailable production
credentials or sources block production activation, not synthetic implementation.

Known scope change: the September 16 simplified-qualification plan says “no new
service” and uses in-process `run_production_e1`. This design is its proposed
successor only for execution provenance. On implementation approval, update that
plan's affected engineering/API sections by reference; preserve its model,
approval, privacy and no-redraw obligations. Do not silently carry both routes as
equivalent authority paths.
