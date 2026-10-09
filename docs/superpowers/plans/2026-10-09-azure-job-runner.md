# Azure offline job runner implementation plan

> **For agentic workers:** Execute with superpowers:executing-plans. The coordinator owns combined acceptance.

**Goal:** A shared `run / status / results / cancel` interface for separately authorized offline Windows jobs.
**Architecture:** One serialized local ledger reserves VM time before Azure start. Managed Run Command launches durable guest supervision. A separate local guardian covers bootstrap and confirms deallocation; a credential-free guest watchdog deallocates independently using a VM-scoped identity. Results persist on the OS disk and are published to the operator-approved private Blob container for retrieval after deallocation.
**Tech Stack:** Python standard library, existing Windows Job Object implementation, PowerShell 5.1, Azure CLI and Managed Run Command.
**Spec:** Joshua's 2026-10-09 instruction in this task governs. This plan carries forward the useful runner design from the uncommitted 2026-10-08 Azure plan; it supersedes that draft's pending provisioning, budget and acceptance steps for this runner only. Resource identities belong exclusively in ignored local configuration.

## Authority and constraints

Build/test authority includes the public qualification suite at `ed4d7c9e8283d91c01e4c470bb5091b619fc504c` on PR #742. No statistical campaign, private transfer, live execution or acceptance-criterion change. Never request/read/store the admin password. Joshua approved a managed identity with only read/deallocate on this VM on 2026-10-09. Merge remains Joshua's. Independent Claude review required; no Codex mentions or force push.

Weekly running-time ceiling: $125 at $2.90/hour, tracked conservatively from before start through observed deallocation. Weeks use Monday 00:00 UTC. Reserve job maximum plus setup/collection/shutdown overhead; reject reservations crossing the weekly boundary. Monthly 5,000 process CPU-hours is reporting only. Never reset an open interval or treat API submission as deallocation. Existing pre-run usage must be reconciled before first admission.

Only clean, pinned GitHub commits are accepted. Each job requires a named operator authority, environment, maximum wall time and expected output paths. The initial implementation transfers no private inputs at all, even if a ruling is named; later transfer support requires its own review. Operations and research environment paths cannot coincide. Windows success does not establish Linux qualification acceptance.

## Behavioral contract and combined acceptance

Controller owns durable ledger and admission lock; guest owns job state, Job Object, CPU accounting, output inventory and cancellation marker. Local guardian owns deallocation verification and closes running intervals only after Azure says `VM deallocated`. Guest watchdog owns independent deadline/idle deallocation when the submitting client disappears. Controller crash must not orphan startup: guardian acknowledgement precedes VM start. Reboots do not retry jobs. Shutdown remains pending on Azure failures, with retry; ledger continues charging. Azure outages can delay the physical deallocation, so reserve a shutdown margin and disclose any overrun rather than claim an absolute billing guarantee.

Managed Run Command output is a bounded transport, not evidence storage. Guest writes files before signaling terminal state; results retrieval verifies archive and per-file hashes. Partial files remain available after cancellation/timeout. Retrieval needing VM restart is a separately ledger-reserved maintenance interval with the same guardian. Never mark verification complete unless launcher status/exit/source/capture/reports and artifact hashes agree.

## Roadmap

1. Admission, persistent time ledger, Azure adapter and idle shutdown tested with fakes.
2. Guest job/process supervision, watchdog, results retrieval and four-command interface.
3. Public guest bootstrap, bounded safety probes, pinned suite collection and full acceptance.
4. README, independent Claude review, code PR and results comment; operator merge.

## Handoff 1 â€” admit and retire one bounded VM session

**Selected outcome:** Tested persistent admission and deallocation behavior, including controller failure.
**Prerequisites:** Isolated branch based on `7aa2fb94ba4df87b216a881e2f261aec8ebb1971`; operations doctor passed on CPython 3.13.2 with 62 locked packages. Azure read confirms deallocated. Identity permission approved; installation still owed.
**Ownership:** Codex implements and coordinates; Codex retains combined acceptance; Claude independently reviews.
**Verification:** Launcher pytest exercises over-budget refusal, week rollover, duplicate/concurrent admission, uncertain deallocation, restart and fake Azure retries. Retain generated record path and actual result here.
**Checkpoint:** Before Azure start, evaluate fake failure evidence, ledger seed and guardian acknowledgement.
**Return boundary:** Return to coordinator after focused tests; no statistical or private dispatch.

- [ ] Write failing tests for reservation and stop/verify semantics.
- [ ] Implement atomic locked state and Azure adapter; run focused launcher tests.
- [ ] Evaluate the outcome before guest integration.

## Handoff 2 â€” durable guest execution and complete evidence

**Selected outcome:** Commands dispatch once, read durable status, retrieve hashed complete/partial files and cancel the owned process tree.
**Prerequisites:** Handoff 1 accepted; clean runner revision published before guest fetch; independent shutdown identity installed before unaccompanied jobs.
**Ownership:** Codex implements and integrates, Claude reviews.
**Verification:** Windows process tests include descendant CPU, cancellation and kill-on-controller-close. Fake transport tests include truncated/corrupt results and path traversal. Bounded guest probes establish watchdog and observed deallocation.
**Checkpoint:** Record remote safety evidence before full suite dispatch.
**Return boundary:** Return failures to coordinator; do not weaken safety gates to run acceptance.

- [ ] Test/implement job contract and evidence verification.
- [ ] Reuse existing Windows Job Object launch; retain stdout/stderr and launcher records.
- [ ] Install a SYSTEM watchdog with no password and minimum identity permissions.
- [ ] Test controller disconnect, cancellation and idle deallocation.

## Handoff 3 â€” public acceptance and review

**Selected outcome:** Exact PR #742 suite completes on Windows with evidence posted to the runner PR.
**Prerequisites:** Safety probes pass; public GitHub fetch at exact SHA; operations lock installation and doctor; collection confirms Windows compatibility. First run maximum 8 hours plus 1 hour overhead, eight pytest workers (launcher maximum), subject to available weekly ledger.
**Ownership:** Codex executes approved acceptance and reports; Claude independently reviews; Joshua merges.
**Verification:** Full suite record status, exit code, stable source, capture, report validity, process CPU/wall time, per-file hashes, ledger cost and observed VM deallocation. Explicitly distinguish skips and Linux acceptance.
**Checkpoint:** Report results or exact blocking evidence on the PR, retaining all partial outputs locally.
**Return boundary:** Stop at reviewed PR and results comment; no merge, next campaign or private transfer.

- [ ] Run collection and full authorized suite through `scripts/fp.py` under the pinned ops venv.
- [ ] Retrieve and verify evidence, deallocate and reconcile actual charged duration.
- [ ] Obtain independent Claude review, fix concrete findings and rerun affected checks.
- [ ] Open PR, post acceptance evidence and return to Joshua.

## Evidence and unresolved dependencies

Implementation and acceptance pending. The primary checkout remains untouched. Initial Azure read reports deallocated, with no managed identity yet. Historical connection-test running time still needs a conservative ledger seed from activity events. There is no budget alert or nightly shutdown.

### Build checkpoint and independent review (2026-10-09)

Handoff 1 accepted locally: persistent reservation, fake Azure deallocation and
restart/rollover cases pass. The independent Claude interim review identified stale
boot leases, publication liveness, shutdown exception handling, read-only status
consuming IDs, and missing recovery. Repairs use a pre-start VM metadata lease,
whole-supervisor heartbeat, job-fenced serialized retirement, conservative retry,
a separate status cache and explicit reconcile. Named Job Objects use the local
session namespace and reject existing-name adoption. Guest diagnostics stay out of
published records. The operator explicitly approved the private public-results Blob
container and its container-scoped identity access; management-channel chunking from
the initial design is superseded by that approved transport. No private-input path
was added. Local breakaway refusal remains fail-closed, pending the actual dispatch
probe. Combined acceptance remains pending remote safety and full-suite evidence.

Evidence before the final added regressions: focused runner/process ownership suite
129 passed, 6 skipped, record `20261009T043907Z-b769cafc406d`, completed/exit 0/stable.
Standard blocking gates passed at `20261009T043412Z-b5992aa403dc` (private manifests
reported their expected absent-tree skips). PR #742's exact pinned SHA collected all
2,347 tests on Windows with `20261009T042703Z-f084a30a2df9`, completed/exit 0/stable;
collection is not execution acceptance. Final frozen-tree evidence follows below.

Frozen candidate verification: `20261009T044446Z-97a1076bcf50` completed with exit 0, source stable, 132 passed and 6 skipped (CPython 3.13.2). A real detached local child survived its parent exit; no VM start was involved. The reviewed build now proceeds to public remote safety probes.


### Frozen review corrections and public probes (2026-10-09)

Claude's second independent review identified five remaining blockers: competing
result publishers, reconcile stopping healthy work, accumulated Managed Run Commands,
missing disk-only republishing, and no publication window before shutdown. The
integration candidate serializes recovery with the supervisor lock, publishes immutable
archives before descriptors, makes reconcile observation-only, deletes temporary/job
commands, and admits budgeted republishing under a fresh lease. Preparation/execution,
publication and shutdown have distinct cutoffs. Terminal Managed Run Command observations
are retained privately before resource cleanup.

Local affected verification `20261009T051810Z-6198360b4b18`: 140 passed, 6 skipped;
CPython 3.13.2, completed, exit/verification exit 0, source stable, capture complete.
Subsequent transcript finalization/documentation changes require fresh verification.

The first public smoke admission failed before VM start because a tag update assumed
an existing tags object; tag Merge fixes this. The second VM session deallocated
without a published archive; Azure's subsequent retained view was Pending, so no
payload outcome is asserted. These are failed acceptance attempts, not passes.
The ledger retains both intervals plus a conservative 900-second historical seed.
The VM was confirmed deallocated after both attempts. Full qualification execution
and final Claude approval remain pending.
