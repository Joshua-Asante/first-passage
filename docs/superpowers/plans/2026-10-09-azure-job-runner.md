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

## Handoff 1 — admit and retire one bounded VM session

**Selected outcome:** Tested persistent admission and deallocation behavior, including controller failure.
**Prerequisites:** Isolated branch based on `7aa2fb94ba4df87b216a881e2f261aec8ebb1971`; operations doctor passed on CPython 3.13.2 with 62 locked packages. Azure read confirms deallocated. Identity permission approved; installation still owed.
**Ownership:** Codex implements and coordinates; Codex retains combined acceptance; Claude independently reviews.
**Verification:** Launcher pytest exercises over-budget refusal, week rollover, duplicate/concurrent admission, uncertain deallocation, restart and fake Azure retries. Retain generated record path and actual result here.
**Checkpoint:** Before Azure start, evaluate fake failure evidence, ledger seed and guardian acknowledgement.
**Return boundary:** Return to coordinator after focused tests; no statistical or private dispatch.

- [ ] Write failing tests for reservation and stop/verify semantics.
- [ ] Implement atomic locked state and Azure adapter; run focused launcher tests.
- [ ] Evaluate the outcome before guest integration.

## Handoff 2 — durable guest execution and complete evidence

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

## Handoff 3 — public acceptance and review

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

Combined acceptance remains pending. The primary checkout remains untouched. The operator-approved managed identity and private public-results container are provisioned; their bindings remain in ignored local configuration. The ledger includes a conservative 900-second historical seed and every build/probe interval. There is no budget alert or nightly shutdown.

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


### Bootstrap diagnosis and third review corrections

A diagnostic smoke established MSI exit 1603; a bounded read-only guest inspection
isolated error 1606: the forward-slash Python target was interpreted as a network
location. The bootstrap now normalizes native Windows installer targets. These
diagnostic sessions did not run qualification or statistical workloads; each used
a ledger reservation, detached reaper, and observed deallocation.

Claude's third review confirmed C1-C5 fixed, then requested final command-view
retention, proof of ownership before declaring a stale-heartbeat supervisor dead,
bounded source snapshots, and smaller lifecycle corrections. The new candidate
attempts a final command read before cleanup on every submitted exit, keeps earlier
observations separately, retries cleanup before the next bounded submission, and
records successful cleanup to avoid repeated deletion. Azure rejects command
deletion while a VM is deallocated; cleanup failures never veto VM retirement.
A final read may still report Pending after Azure resets its view; it is diagnostic
evidence, never a replacement for a verified launcher record.

Source snapshots now run in deadline-bound Windows Job Objects, and preparation,
bundling and publication timing is retained. Re-entry marks idle without replay;
recovery sessions can be cancelled independently of the original job result.
Runner verification `20261009T054200Z-0360f7497ee4`: 77 passed, completed/exit 0,
source stable, including a real bounded Git snapshot and expiration regression.


### Public smoke and fourth review

The public smoke at runner commit `43ba78b236cf5bb3031a232268da14df7f7b6b4f`
completed all 77 tests on the Windows guest. Original launcher record
`20261009T055805Z-81882375bd44`: completed, exit/verification exit 0, source stable.
The host retrieved and verified 13 artifacts: ZIP SHA-256
`7b2a005e1d728cbbed799a2179b8645e4f9b885e85637f1cc27d0dc5e2deb730`,
290,957 bytes. Workload CPU 6.75 seconds, wall 16.5196924 seconds; publication
through descriptor preparation 3.999279 seconds. VM deallocation was observed
and the ledger interval closed. This is runner smoke evidence, not PR 742 acceptance.
Concurrent Managed Run Command status succeeded during bootstrap; Azure reported
asyncExecution=true and timeoutInSeconds=3300. Blob downloads with overwrite worked.

Claude's fourth frozen review found no new code-level blocker, but could not see
the cited local verification records: those were generated in the separate integration
worktree, not the frozen review checkout. The final review must receive readable
evidence in its own checkout. Cost follow-ups add an explicit force/pre-start cancel
path, a separately published 30-minute guest bootstrap cutoff, and a 300-second
upload reserve after source checking. Initial provisioning still depends on local
guardians until the guest watchdog is installed; successful smoke establishes that
installation path. Confirm the running task during the next remote safety probe.
Azure-side scheduled auto-shutdown remains excluded by the operator's ruling.

Minor fourth-review follow-ups retained for operator visibility: corrupted local
cleanup/CPU records can fail their commands; an external boot is not a runner-owned
ledger interval; failed guest commands prioritize deallocation and may require explicit
disk-only recovery instead of a paid grace period. None substitutes for the pending
cancel/disconnect/recovery probes or the full pinned qualification run.


### Code review closed; remaining acceptance in progress

Independent Claude final review of runtime commit
`16639bbf1e7b453a0aa0067b7a88172c3bb209d0`: **no code or evidence blocker**.
It read current-commit records in the frozen review checkout:
`20261009T060915Z-379b549f9055` (80 passed) and
`20261009T061005Z-705d815c5d58` (standard gates), both completed/exit 0/stable.
Four nonblocking coverage cases were then added without runtime changes: normal
cancel preserves publication, immediate idle bypasses boot grace, and missing/preparing
state reaches bootstrap shutdown despite a held recovery lock. All 84 runner tests
passed in `20261009T062444Z-51db3e5d2c08`, completed/exit 0/stable.

Remote safety evidence on that runtime:

- The running task reported watchdog commit `16639bb...`. Azure accepted an
  asynchronous Managed Run Command with a 31,500-second timeout while the workload
  was executing. The actual cancel CLI returned cancellation_requested.
- Cancellation produced interrupted/130, 10 hash-verified partial artifacts including
  the parent and owned-child output prefixes, CPU 1.109375 seconds and wall 21.0873809
  seconds. Deallocation was confirmed. ZIP SHA-256
  `a3d801c96ec9643c3b9811473907df18c3bb786dde0444899a54c46f904bdb70`.
- Controller-crash probe: the local guardian was killed only after checking its exact
  PID/session binding. The guest continued another 55.512897 seconds, completed/0/stable,
  and published 11 verified artifacts. Workload CPU 1.65625 seconds, wall 123.3335822
  seconds. VM deallocation was observed before the ledger was reconciled.
- Disk-only recovery preserved the cancelled job's execution artifacts byte-for-byte
  and retained interrupted/130. A fresh maintenance reservation closed after observed
  deallocation. Recovered ZIP SHA-256
  `b93f8e40a10c96076e1a3c7f734128d9d9c2073995f2debfec433dfe393bab89`.
  Original cancellation plus maintenance cost about $0.33 at the configured VM rate.

The exact PR 742 qualification job is now admitted under a 32,400-second reservation
(28,800-second maximum workload plus 3,600-second overhead). This paragraph records
admission only. Final full-suite evidence and the PR comment remain owed.


### Windows atomic-state repair during acceptance

The pinned qualification workload continued while its guest heartbeat thread stopped.
Managed Run Command exposed only the exception header, so its exact exception is
not established. Durable evidence showed an unchanged heartbeat and a leftover
heartbeat JSON temporary file two seconds later. Claude had already identified the
shared writer's Windows reader/replacement race as a nonblocking concern.

A local regression with an actual open Windows reader reproduced `PermissionError`
(`WinError 5`) at `os.replace`; red record `20261009T064550Z-6df33b173896`.
The common `atomic` writer now retries permission failures at most 20 times over
one second, retains the previous complete target until replacement succeeds, and
cleans its own temporary file without masking a write failure. Other I/O failures
are not retried. This covers guest heartbeat/state, host heartbeat/observations,
and the locked ledger through their existing shared writer. ZIP publication is
serialized under the guest lock and is not read by a competing live-state reader;
bootstrap PowerShell writes precede the new supervisor and are outside this fix.
No source on the running guest or its frozen controller checkout was changed.

Green verification: `20261009T064625Z-96023a543049` (87 runner tests passed) and
`20261009T064735Z-c82662a35524` (standard gates), both completed/exit 0/stable.
Public-clone private-manifest skips and existing advisory notes remain disclosed.
Independent Claude review of this repair is pending; qualification remains pending.
