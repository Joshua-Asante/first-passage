# Azure offline job runner implementation plan

> **For agentic workers:** Execute with superpowers:executing-plans. The coordinator owns combined acceptance.

**Status:** Earlier acceptance remains historical. Five-finding repair handoff below is active; coordinator owns combined acceptance and native Windows verification.

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

- [x] Write failing tests for reservation and stop/verify semantics.
- [x] Implement atomic locked state and Azure adapter; run focused launcher tests.
- [x] Evaluate the outcome before guest integration.

## Handoff 2 — durable guest execution and complete evidence

**Selected outcome:** Commands dispatch once, read durable status, retrieve hashed complete/partial files and cancel the owned process tree.
**Prerequisites:** Handoff 1 accepted; clean runner revision published before guest fetch; independent shutdown identity installed before unaccompanied jobs.
**Ownership:** Codex implements and integrates, Claude reviews.
**Verification:** Windows process tests include descendant CPU, cancellation and kill-on-controller-close. Fake transport tests include truncated/corrupt results and path traversal. Bounded guest probes establish watchdog and observed deallocation.
**Checkpoint:** Record remote safety evidence before full suite dispatch.
**Return boundary:** Return failures to coordinator; do not weaken safety gates to run acceptance.

- [x] Test/implement job contract and evidence verification.
- [x] Reuse existing Windows Job Object launch; retain stdout/stderr and launcher records.
- [x] Install a SYSTEM watchdog with no password and minimum identity permissions.
- [x] Test controller disconnect, cancellation and idle deallocation.

## Handoff 3 — public acceptance and review

**Selected outcome:** Exact PR #742 suite completes on Windows with evidence posted to the runner PR.
**Prerequisites:** Safety probes pass; public GitHub fetch at exact SHA; operations lock installation and doctor; collection confirms Windows compatibility. First run maximum 8 hours plus 1 hour overhead, eight pytest workers (launcher maximum), subject to available weekly ledger.
**Ownership:** Codex executes approved acceptance and reports; Claude independently reviews; Joshua merges.
**Verification:** Full suite record status, exit code, stable source, capture, report validity, process CPU/wall time, per-file hashes, ledger cost and observed VM deallocation. Explicitly distinguish skips and Linux acceptance.
**Checkpoint:** Report results or exact blocking evidence on the PR, retaining all partial outputs locally.
**Return boundary:** Stop at reviewed PR and results comment; no merge, next campaign or private transfer.

- [x] Run collection and full authorized suite through `scripts/fp.py` under the pinned ops venv.
- [x] Retrieve and verify evidence, deallocate and reconcile actual charged duration.
- [x] Obtain independent Claude review, fix concrete findings and rerun affected checks.
- [x] Open PR, post acceptance evidence and return to Joshua.

## Evidence and unresolved dependencies

Combined acceptance is complete; see final closure below. Tracked files in the primary checkout remain untouched. The operator-approved managed identity and private public-results container are provisioned; their bindings remain in ignored local configuration. The ledger includes a conservative 900-second historical seed and every build/probe interval. There is no budget alert or nightly shutdown.

The checkpoint entries below retain the status at each stage; the final closure controls current status.

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
Independent Claude review of the atomic repair found no blocker. Its follow-ups
added a recoverable heartbeat cadence and made the reaper stop marker best-effort
so a storage failure cannot veto deallocation. Red `20261009T065555Z-79a4a2d0d71b`
and green `20261009T065628Z-b13c9a2d1420` (90 passed, completed/0/stable) bind those
paths; exact retry timing and cleanup-error preservation also have coverage.
The final independent Claude review found **no blocker** in these bounded follow-ups
and verified their red/green records. The green record attests the pre-commit working
tree; the committed runtime was subsequently tested remotely as recorded below.


### Full pinned qualification result

Full public Windows qualification completed at the requested PR #742 SHA `ed4d7c9e8283d91c01e4c470bb5091b619fc504c`.

- Command: operations Python 3.13.2, `scripts/fp.py --workers 8 python -m pytest tests/ops/qualification -q`.
- Original launcher record: `20261009T063015Z-2b680e51fa8a/record.json`.
- **2,339 passed, 1 skipped, 7 xfailed; all 2,347 collected.** No failures or errors. The skip is the Linux thread-directed SIGSTOP test; the seven existing xfails say `awaits K3/RC-4`. This Windows result does not replace Linux-specific acceptance.
- Launcher and runner: `status: completed`, exit code `0`, verification exit `0`, `source_stable: true`, complete capture, no report errors. Clean pinned source matched before/after.
- Process-tree CPU: **5,118.6875 seconds (1.421858 CPU-hours)**. Workload wall: **1,350.9274312 seconds (22m 30.93s)**; original launcher duration 1,350.5126881 seconds.
- Complete outputs retrieved after execution: **19 artifacts**, every file's SHA-256 checked against the archive manifest. ZIP: **360,170 bytes**, SHA-256 `234961cae1ff1083a600cdd2149118b3a5f3009a79fded8a82e92a510360be02`. Publication through descriptor preparation took 4.640830 seconds.
- Azure power state independently confirmed **VM deallocated**; ledger interval closed with no active reservation. Billed-time estimate conservatively includes admission through observed deallocation: **1,582.849596 seconds, $1.2751** at $2.90/hour. Weekly ledger after this job: **$3.9063 / $125** (includes setup/safety probes and the historical seed).
- Retrieved workload CPU report: **1.424501 hours this week and month / 5,000 monthly planning hours**; no CPU hard stop. Bootstrap-only diagnostic/failed-start sessions have no workload CPU record.

Runner runtime for this job was `16639bbf1e7b453a0aa0067b7a88172c3bb209d0`. Its heartbeat thread stopped during the run; the independent guards preserved execution and idle deallocation. A Windows state-file replacement race was reproduced locally and repaired in runner PR #746, with follow-up safeguards under review. The successful pinned qualification source and artifacts were not modified. No private inputs or statistical campaigns were run.


Final merged-base gates: `20261009T065818Z-b43be3fd224e`, completed/exit 0/stable.
Acceptance was posted on [PR 742](https://github.com/Joshua-Asante/first-passage/pull/742#issuecomment-6076069160)
and [runner PR 746](https://github.com/Joshua-Asante/first-passage/pull/746#issuecomment-6076069448).
The final runner smoke and Claude follow-up are closed below; neither changes the
pinned qualification result above.


### Final closure (2026-10-09)

Final runtime `98af2023b301df912ac9f92d6fb429568a7447e2` completed a fresh Windows
remote smoke: **90 passed**, original launcher `20261009T070211Z-4d8e7f3faef1`,
completed/exit 0/verification exit 0/source stable/complete capture. All 13 artifacts
were retrieved and hash-verified; ZIP 292,071 bytes, SHA-256
`203cbae1c7ad7c95bcd0072a35984cce0145355344b0d9f4d71b5d16f424742b`.
Workload CPU 5.3125 seconds, wall 15.036735 seconds; publication 4.262622 seconds.
VM deallocation was independently confirmed and the ledger has no active interval.
The smoke cost $0.1299. Final weekly VM ledger: 5,010.438778 seconds,
**$4.0362 / $125** including the conservative seed, provisioning and all probes.
Retrieved process workload CPU totals 1.425977 hours this week/month against the
5,000-hour monthly planning allowance; setup-only sessions have no workload CPU record.

Independent Claude reviewed the original runtime, the real Windows atomic-write
repair, and the final heartbeat/reaper follow-ups. Each final scoped review returned
**no blocker**; the last verified both red and green local evidence. Its earlier
claim that the guest traceback was proven was explicitly corrected: the exact
exception remains inferred, while the local Windows sharing failure is reproduced.

The requested full pinned qualification and cancellation/disconnect/recovery evidence
are retained above and in the PR comments. No public artifacts contain resource
bindings. PR #746 includes the current main via a normal merge, without force-push.
The implementation and evidence are ready for Joshua's merge; no further job authority
is implied. Linux acceptance and Windows-incompatible research pins retain their
separate paths and constraints described in the README.

## Five-finding repair handoff (2026-10-09)

**Selected outcome:** One bounded PR update closes review comments 4234697259,
4234697264, 4234697270, 4234697277 and 4234697285 without changing job authority.
**Prerequisites:** Refreshed head `a1ec9dd39f6faaa08b0f16bf5b5253c13e1dcaaa`;
actual comments and producers/consumers read; operations doctor Python 3.12.14,
62 locked packages. All five findings are present.
**Ownership:** This executor implements and pushes; existing coordinator owns
combined acceptance and independent verification. Retain the same reviewer.
**Verification:** Red/green regressions, affected runner tests, standard launcher
checks; every accepted record completed/zero/stable/complete. Native Windows
execution belongs to the coordinator; runner pytest does not prove Task Scheduler.
**Checkpoint:** Return contradictions or scope conflicts before dependent edits.
**Return boundary:** Ordinary fast-forward push (merge concurrent work only if
needed), replies to the five threads, exact SHA/evidence/CI return. No merge of
PR #746, #748 edits, Azure activity, new reviewer or deployment.

### Related-case map and execution steps

| Rule / case | Shared producer and consumer | Required proof |
| --- | --- | --- |
| Pinned entrypoint | contract.validate -> execute after checkout -> run_tree | Research `-c`, `-m`, stdin/options rejected; ordinary script accepted; missing/directory/symlink escape refused before launch |
| Completed outputs | execute / republish / watchdog.recover -> bundle -> results | Missing output at final packaging cannot remain completed; interrupted/failed partials remain retrievable; stale extracted files cannot satisfy manifest coverage |
| Launcher evidence | execute -> bundle for all publishers -> results | Operations auto-collects full referenced run directories; capture/JUnit/artifact hashes checked at publication and retrieval; missing/malformed/tampered evidence rejected |
| Recovery CPU identity | run(republish) session.json -> cpu_report | Maintenance aliases map to source workload; repeated recovery never adds CPU or false missing jobs; genuinely missing original remains reported |
| Preparation cancellation | checkout / environment / source-before -> owned run_tree -> watchdog recover | Cancel before/during setup stops only the owned tree, bounds waiting, retains setup stdout/stderr and interrupted result; no launch of workload after cancellation |

- [x] Write `tests/scripts/azure_jobs/test_review_repairs.py` red regressions for
  each row, including retrieval with a forged incomplete manifest and held guest lock.
- [x] Run focused tests via `python -I scripts/fp.py python -m pytest
  tests/scripts/azure_jobs/test_review_repairs.py -q --tb=short`; retain failures
  tied to the unchanged production source.
- [x] In `contract.py`, separate entrypoint syntax from artifact paths and add
  common completed-output/launcher-evidence validation used by guest and host.
- [x] In `guest.py`, resolve a real entrypoint within checkout, make common bundle
  strict for completed records and include launcher run directories automatically;
  downgrade a failed final packaging contract before publishing partial evidence.
- [x] In `runner.py`, validate completed archive contracts against current manifest
  membership, and map republish sessions to their original CPU identity.
- [x] In `guest.py`, run checkout/environment commands in cancel-aware owned trees,
  retain per-step setup captures, and pass cancellation to the pre-execution snapshot.
  Existing watchdog termination targets the same job identity during preparation.
- [x] Verify all three bundle callers and their terminal/partial cases, malformed
  inputs, entrypoint symlinks, artifact omission/hash changes and setup cancellation.
- [ ] Run affected tests and required checks; inspect diff and related-case map;
  commit, then run exact-head evidence checks without source edits during capture.
- [ ] Refresh/push without force, reply with evidence and Windows limitations,
  report current CI and return to coordinator.

**Execution rulings:** Keep the roadmap in this existing plan as the coordinator
requires. Apply writing-plans/executing-plans inline with a retained task ledger;
existing implementation/push authority supersedes redundant plan confirmations.
Do not dispatch the skills' suggested new reviewer: review remains with the
existing coordinator. Resource scope remains affected tests plus required gates.

### Implementation evidence and remaining handoff

Root causes and repairs follow the five rows above. All publishers now enforce the
same completed contract, and retrieval requires coverage in the current manifest
before accepting original launcher records and their capture/JUnit/artifact hashes.
An empty expected directory cannot prove completion in a file-only archive; failed
and interrupted jobs still allow partial outputs. A late packaging failure changes
an executing job's completion to failed before preserving the available archive.
Recovery of an already terminal record refuses incomplete completion without
rewriting the original evidence.

Linux, validated operations Python **3.12.14**, 62 locked packages; records live at
`.cache/fp-verification/<id>/record.json`:

| Stage | Launcher record | Result |
| --- | --- | --- |
| Red, unchanged production at `a1ec9dd39f6faaa08b0f16bf5b5253c13e1dcaaa` | `20261009T214118Z-feefe0a61250` | 25 failed, 3 passed; stable source, complete capture, exit/verification 1 |
| Initial repair | `20261009T214329Z-5de308d82d47` | 28 passed |
| Expanded affected suite | `20261009T214850Z-e0b1c274eead` | 161 passed, 11 Windows-only skips |
| Required `python -I scripts/fp.py check` | `20261009T214905Z-1008d986966c` | Completed, exit/verification 0 |

Green records are completed, exit/verification 0, stable source, complete capture,
and empty report errors. They capture the working patch, not a clean final commit;
exact-head reruns and push receipts belong in the five review replies/task return.
Standard checks retain their explicit public-clone limitations: absent private
Pine/data/heavy artifacts and absent deployed skills bundle are not verified.

The related-case sweep covers script arguments/options, missing/directory/symlink
entrypoints, disappearing output, all three publishers, terminal versus partial
archives, stale extracted output/capture files, malformed launcher records, internal
artifact hash disagreement, repeated recovery CPU aliases, and cancellation before
or during preparation while the live guest holds its lock. The watchdog can now
stop the same named owned tree during preparation; setup logs enter partial bundles.
Malformed JUnit metadata also follows the ordinary packaging-failure path (red
`20261009T214810Z-8a5af482f5a3`, then the expanded green suite).

Coordinator's separate native baseline reported **129 passed, 1 skipped, 1 failed**
at `a1ec9dd39f6faaa08b0f16bf5b5253c13e1dcaaa`, record
`20261009T213728Z-cd3d8ff92c4a`. The failed kill-on-close fixture incorrectly required
nonzero exit status. Its authorized correction asserts live worker at the stall
marker, bounded exit, no natural-completion sentinel, and retained disk republish
evidence; production termination semantics are unchanged. The new native preparation
fixture waits for a startup marker before cancellation to avoid timing assumptions.
Native final-head Job Object/cancellation/fixture execution remains with that same
coordinator. Baseline trailing-dot alias passed; trailing-space alias skipped because
the filesystem/API did not normalize it. Task Scheduler execution remains unverified;
Linux synthetic results and runner pytest do not establish Scheduler integration.

Scoped executor inspection found no further blocker in these five repair paths.
Independent acceptance stays with the existing coordinator/reviewer; the next two
unchecked steps above define the return boundary.

## Narrow v1 coordinator adjudication — 2026-10-09

This section supersedes the earlier broad implementation/ready-for-merge claims.
Starting head: `b16d6178b41b790411a542e7a16fb26d069ebbce`. Joshua ordered a
state-model-first rebuild after more than three review rounds. Preserve
`codex/azure-job-runner`; use ordinary commits and pushes, never force or delete.
The current coordinator owns combined acceptance. Earlier passing records remain
historical evidence and do not accept this rebuild.

### v1 contract and state model (written before implementation)

Scope: public repository fetched at a full pinned SHA, operations venv and launcher
only, no private inputs, one admitted job, run/status/results/cancel, $125 weekly
VM-time ledger, and verified deallocation on exit. Research entrypoints and
`results --recover` disk-only maintenance admission are deferred to another PR.
Partial evidence preservation during the current session is still required.

State has three independent axes; a successful workload exit alone is never job
completion. The controller owns admission, charge reservation and reconciliation;
the guest owns preparation/workload/result evidence. Azure instance view owns power
confirmation. An asynchronous start response is not proof that start has settled.
Local guardian/reaper and the installed guest Task Scheduler watchdog enforce
bounded deadlines; none may erase an uncertain operation to admit a successor.

| Axis | Enumerated values | Allowed transition / required evidence |
| --- | --- | --- |
| Job | `admitted`, `starting`, `preparing`, `running`, `stopping`, `publishing`, `cleanup`, `completed`, `failed`, `cancelled`, `alarm` | Forward progress or stopping from any nonterminal state; terminal only after cleanup/reconciliation, or explicit alarm. Cancel is sticky and forbids subsequent workload launch. |
| VM | `deallocated`, `start_pending`, `starting`, `running`, `deallocate_pending`, `unknown` | Only observed Azure `VM deallocated` confirms billing shutdown; stopped/unknown does not. A pending start fences shutdown confirmation until settled or alarmed. |
| Ledger | `idle`, `reserve_pending`, `charged`, `reconcile_pending`, `blocked` | Atomic reserve before any start; accrue from reservation through observed deallocation; reconcile once, retain active interval on failure. No new job during any pending/blocked operation. |
| Cleanup | `clear`, `pending`, `failed` | Register cleanup intent before submitting command; remove intent only after confirmed command removal. Failure blocks admission even if VM is deallocated. |
| Alarm | `none`, `active` | Nonzero foreground error / stderr plus best-effort durable alarm. Disk-write failure cannot suppress stderr or deallocation. Detached controller errors must surface through status. |

Ledger events are `reserve_requested`, `reserve_committed`, `start_requested`,
`start_settled`, `stop_requested`, `deallocate_requested`, `deallocate_verified`,
`reconcile_requested`, `reconcile_committed`, `alarm`. These name semantic events;
the implementation may persist a compact current-state record under one lock.
Persist irreversible intent before invoking Azure. Serialize start and cleanup
against cancellation and admission. A pending/failed intent survives process loss.
Do not call a failed diagnostic write a successful transition.

| Sequence | Enumerated events | Required end / test oracle |
| --- | --- | --- |
| S1 normal | 1 validate public pinned operations spec; 2 verify idle/deallocated/cleanup clear; 3 commit charge reservation; 4 record start pending and submit start; 5 settle start; 6 prepare; 7 run; 8 verify all outputs and launcher records/hashes; 9 publish; 10 cleanup; 11 deallocate and verify; 12 reconcile | completed only with verified result and no pending start, cleanup or ledger write |
| S2 cancel during preparation | 1 reserve/start; 2 begin owned setup; 3 persist stop intent; 4 stop owned preparation tree; 5 prohibit workload launch; 6 retain partial captures; 7 cleanup; 8 deallocate/verify; 9 reconcile | cancelled, VM deallocated; failed stop-write or guest transport still leads to deallocation or loud alarm |
| S3 controller loss | 1 reserve/start/prepare or run; 2 controller disappears; 3 independent deadline/heartbeat expires; 4 stop owned tree; 5 bounded partial publication; 6 request deallocation; 7 verify or alarm; 8 reconcile on controller return | no new admission from stale heartbeat or merely released OS lock; VM deallocated or alarm |
| S4 cleanup failure | 1 workload exits; 2 cleanup intent persists; 3 delete command fails; 4 continue deallocation; 5 verify power; 6 reconcile charge with cleanup fence retained | failed/alarm, new admission refused until explicit confirmed cleanup; never start a successor to hide cleanup debt |
| S5 deallocate failure | 1 stop intent; 2 deallocate API raises/times out; 3 query power independently; 4 bounded retry if needed; 5 verify deallocated or emit alarm | API failure cannot skip power observation; unresolved interval remains charged and admission blocked |
| S6 state write failure | 1 inject failure at reservation, session, stop, observation, cleanup or reconciliation write; 2 abort forward execution; 3 stop/deallocate if a start may exist; 4 verify independently; 5 emit alarm even if alarm storage fails | failed reservation causes zero starts; later write failure never vetoes shutdown; unreconciled interval blocks next admission |
| S7 ceiling mid-job | 1 reserve conservative setup/work/publication/shutdown allowance; 2 elapsed charge reaches stop threshold; 3 sticky stop; 4 kill owned tree; 5 bounded publication; 6 deallocate before reserved deadline or alarm; 7 reconcile actual elapsed usage | no extension or fresh reservation; charge all actual time even if ceiling exceeded by platform failure, report breach loudly |
| S8 cancel during start | 1 commit reservation and start intent; 2 asynchronous start requested; 3 cancellation; 4 wait boundedly for start to settle while fencing admission; 5 deallocate; 6 verify; 7 reconcile | an old deallocated observation during pending start cannot close the interval; unresolved start means alarm |
| S9 missing/tampered completion | 1 workload exits zero; 2 expected output/launcher/capture/report absent or digest wrong; 3 refuse completed publication/retrieval; 4 retain available failed evidence; 5 cleanup/deallocate/reconcile | never completed; stale extracted files cannot satisfy the current archive manifest |
| S10 concurrent admission | 1 first admission holds lock or persistent intent; 2 second run/status/cancel arrives; 3 serialize mutation; 4 inspect pending start/cleanup/ledger | no second start; status/results do not create admissions |

Cancellation after a terminal deallocated job is idempotent and cannot affect a
successor. Cancellation while running/publishing cannot rely exclusively on guest
marker delivery: bounded deallocation is the fallback. Controller-wide loss before
watchdog installation is a remaining platform boundary: a local detached process
is not an independent cloud backstop. VM verification must establish the preinstalled
Scheduler watchdog before admitting a new start, or report this prerequisite blocked.
A $125 ledger is a controller ceiling, not an Azure billing guarantee during cloud
control-plane failure; unconfirmed shutdown must alarm and retain its charge.

### Roadmap and bounded handoffs

1. State model and invariant-derived sequence tests.
2. Operations-only lifecycle implementation, results verification and local checks.
3. Bounded VM verification of Windows Job Objects, actual path normalization and
   Task Scheduler execution/restart, with final Azure power observation.
4. One fresh Hyper reviewer pass and Codex verdict against the identical full head.

**Selected outcome:** H1 freezes the above state/event contract and adds executable
sequence tests that fail on the old lifecycle. Completion is a reviewed model and
retained red evidence, not implementation acceptance.
**Prerequisites:** Current public source and prior evidence read; operations doctor
3.13.2/62 locked packages passed. Existing Hyper dot is the designated reviewer.
**Ownership:** This coordinator executes inline and retains combined acceptance.
**Verification:** Tests trace S1–S10 across real controller/ledger functions with
fault-injected Azure/storage boundaries, named event order and admission assertions.
**Checkpoint:** Record red results here before production changes; report any
missing independent deadline capability before VM admission.
**Return boundary:** Return to coordinator adjudication after red evidence; no VM
start or final review in H1. The coordinator may select H2 within Joshua's rebuild
instruction after assessing H1. Preserve all unrelated checkout changes.

- [x] Write the state axes and enumerated event sequences before implementation.
- [ ] Derive failing tests from S1–S10 and record the original failure mechanisms.
- [ ] Select H2 after assessing H1; narrow implementation and verify locally.
- [ ] Select H3 with exact pinned source and VM evidence/deallocation criteria.
- [ ] Select H4 only after H3 passes; retain both exact-head verdicts.
