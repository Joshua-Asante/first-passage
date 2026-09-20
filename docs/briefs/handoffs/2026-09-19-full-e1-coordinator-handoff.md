# Coordinator handoff — remaining Protected Full E1 engineering

> Use superpowers:writing-plans for bounded handoffs and superpowers:executing-plans for execution. Coordinate sequential implementation and independent review; the coordinator owns combined acceptance. Publication of this draft is not S2 acceptance.

**Goal:** One genuine protected synthetic TEST_ONLY E1 runs N1, one joint N2/Part B batch and prescribed Part A, receives independent G5 decisions, atomically commits a complete result, and obtains a separate qseal seal, with integrated Linux E01–E12 evidence.

**Selected outcome:** Finish the remaining engineering by accepting one bounded outcome at a time. First close S2's three source blockers and prove its real Linux supervision boundary; only then dispatch S3. Use the existing eight-slice roadmap, not a replacement implementation.

**Prerequisites:** Accepted S1 commit `430fc72186a0e642c8811be17d459fd87cbf7533` is in [PR #428](https://github.com/Joshua-Asante/first-passage/pull/428), still open at publication. This S2 draft is stacked on `codex/full-e1-s1-durable-budget`; its publication branch is `codex/full-e1-s2-supervision`. Resolve the current branch tip/PR head before assigning work; do not assume either PR has merged. S2-R1 alone has independent local code acceptance. Overall S2 is INCOMPLETE / NOT ACCEPTED.

**Ownership:** The successor coordinator owns roadmap, interfaces, serialized writers, review acceptance and combined E1 acceptance. Assign one implementer per bounded repair/slice; independent review may run in parallel read-only. Existing S2 executor task is `01a0b78e-1079-7a12-b993-52a79a911c55` (Implement S2 budgeted supervision), stopped at its accepted R1 return. Prior coordinator task is `01a0b724-7577-7612-8fd6-2420e13359f2` (Coordinate protected E1 execution). Never depend on task history alone; contracts and evidence below are durable.

**Verification:** Run the tested checkout's `./fp.ps1 doctor` before Python work. Use its `./fp.ps1 python -m pytest`, `./fp.ps1 check` and `git diff --check`, or the documented `python -I scripts/fp.py` bootstrap on supported hosts. Record interpreter, exact source/config identity, commands, exits, reports, skips and cleanup. Reuse unchanged source-bound evidence; independently review risky interface changes. Mocked Windows tests do not establish Linux isolation, timers, accounting or cleanup.

**Checkpoint:** At each repair/slice return, verify evidence/source correspondence, assess review findings and update the roadmap disposition before dispatching the successor. Report concrete cross-component conflicts before dependent code; routine scoped decisions belong to the coordinator. Keep one writer for shared store/service/protocol/profile files.

**Return boundary:** Combined engineering completes only at accepted S8. Return earlier for a concrete missing permission, host/resource dependency or unresolved interface conflict with the affected work explicitly blocked. This handoff does not authorize merge, production deployment, paid provisioning, brokerage/account actions, policy changes or automatic promotion of this draft. The user authorized this commit/push/PR; later publication actions follow the new coordinator's explicit assignment.

## Read these authoritative documents first

- [Execution slices and common contract](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md): S1–S8 outcomes, tests, E01–E12 mapping, output-size and revision closure.
- [Governing specification](../../superpowers/specs/2026-09-17-protected-full-e1-campaign.md).
- [S2 handoff and coordinator resource decisions](2026-09-19-full-e1-s2-budgeted-supervision.md).
- [R1 handoff](2026-09-19-full-e1-s2-r1-recovery-authority.md) and [accepted independent review](2026-09-19-full-e1-s2-r1-review.md).
- [Local S2 implementation plan](../../superpowers/plans/2026-09-19-s2-local-supervision.md).

Historical starting-state paragraphs in the roadmap describe earlier recovery, not the current checkout. This publication branch includes the exact recovered Task1a/1b + accepted S1 through its base, then the incomplete S2 candidate + accepted local R1. Never restart at bare PR425 merge or reconstruct accepted predecessors from memory.

## Current acceptance and evidence

S1 local persisted semantics and its two repairs are accepted. S2-R1 closes interrupted recovery and physical-dispatch acknowledgement authority windows; independent reviewer found no actionable defect. Its deliberate liveness restriction is accepted for this repair: lost owner token, unknown launch acknowledgement or a new recovery need after the one-use slot leaves authority blocked. No uncharged restart continuation exists. Any future continuation needs its own bounded design within the original allowance.

Final R1 records use Python 3.13.2 at `C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`, 62 locked packages, via the candidate checkout launcher:

| Record | Result |
|---|---|
| `20260919T053710Z-bb97fb5412e6` | Seven-file S2 selection: 272 passed, zero skips |
| `20260919T053709Z-4451d9666c45` | Snapshot/model/artifact selection: 41 passed, zero skips |
| `20260919T053710Z-c203c5457d90` | Full check FAILED at unchanged `STATE.md:74` weekly deadline 2026-09-18; preceding evidence-store suite ran 72 cases with three existing skips |

All three records are source-stable and capture-complete with no capture/report errors, fingerprint `49187f49137a2674fe078697e7e9c37c3e4051aeabd1b63883a147b53afaa6df`. Coordinator verified all runtime/test/config hashes against the actual records. Only the disclosed roadmap ledger was appended afterward; publication adds handoff documents. Do not call the full check passing or edit a deadline merely to hide failure. Investigate its current owning workflow and resolve truthfully before merge readiness.

Local immutable evidence packets (not required at runtime and not embedded in Git):

- `C:/Users/joshu/multi_firm_operations/recovery/full-e1-s2-20260919/`: frozen incomplete S2; source.zip SHA256 `a6129041940bcb8749c5a0a9a7d72e11ca1323b45f9331faf3d44ff498917c91`.
- `C:/Users/joshu/multi_firm_operations/recovery/full-e1-s2-r1-20260919/`: accepted bounded R1; source.zip SHA256 `a18d6d376e07fb737967c87f4081e120bc9d77dc1a7672c8f0c20461aa8c1d62`; manifest `5de150f268f879f73eb1105309d9eb24337f9900ab8df8fe015cd26a175d9c09`; SHA256SUMS `736a68541a6adcf5ea9f3625fa47a1beda59435297ea0821a20be0ac2f639e2f`. Coordinator independently verified all 254 entries and all 2,076 source files.
- Candidate checkout: `C:/Users/joshu/.codex/worktrees/full-e1-s2-supervision/multi_firm_operations`.

On a different host, use the published source and transfer retained records if source-bound acceptance needs auditing. Missing local packets are not permission to invent evidence or silently substitute a different source state.

## Next bounded handoffs: finish S2 first

### S2-R2 — reserve before scheduler/bootstrap campaign work

Recommended next implementation. In `tests/integration/qualification_boundary/campaign_driver.py`, ExecutionService construction precedes `service.py::schedule_campaign_probe` reservation. Imports/context validation can consume campaign CPU and fail repeatedly without a lifetime charge. A one-second process limit alone does not solve this.

Trace the actual entrypoint to the first campaign-specific work. Place a minimal trusted, durably funded intent before that work using the existing authority/configuration owners. Define its producer, immutable identity, controller limit, crash semantics and consumers before coding. Demonstrate repeated failed construction, failure after intent, duplicate requests and insufficient remaining allowance cannot gain free work or a new budget. Preserve R1 barriers and historical transport. Return this outcome for review before another repair; if bootstrap cannot be funded without changing the contract, report the exact conflict.

### S2-R3 — charge post-admission VOID authentication

`service.py::_diagnostic_campaign_request` authenticates post-admission VOID from enrolled originals/keys inside an unmetered branch. Invalid/nonidentical requests can repeat expensive authentication. Distinguish cheap bounded transport/historical replay from signature verification. Enroll funded bounded authentication before doing it and preserve cancellation's no-new-authority semantics, durable VOID ordering and exact historical retries. Test repeated invalid requests, exhaustion, restart, concurrent publication and accepted cancellation; do not let an unauthenticated client forge authoritative VOID. Coordinate any temporary pending cancellation barrier explicitly.

### S2-R4 — enforce the original deadline before guardian bootstrap

`campaign_supervisor.py::guardian_main` installs its absolute BOOTTIME timer after Python/context/runtime construction. Relative system-manager runtime limits do not establish original-deadline coverage across queueing/suspend. Provide an independently enforced original deadline before campaign imports/activation. Preserve the single lifetime clock, boot-change refusal and controller accounting. Demonstrate queued start, stalled bootstrap, parent/guardian death and already-expired work on supported Linux. Do not treat refusal of later authority as proof that processes were terminated by the deadline.

### S2 real Linux acceptance and independent combined review

No Linux run, installed release hash or image digest exists for the returned candidate. Existing target: disposable Ubuntu 24.04 x86_64, systemd/cgroup v2, Docker and the existing owned two-host harness. Seven registered targeted cases are only a starting set. Cover CPU aggregate descendants and controller limits, memory common hierarchy/OOM, lost counters, guardian/client death, unknown termination, cleanup failure, original deadline, insufficient authenticated allowance, VOID, restart barriers and actual UID/process membership. Retain unconditional owned cleanup and source/config/image identities. Use the existing `scripts/qualification_boundary_verification.py --s2 --manifest ...` through the host's validated operations launcher; discover the actual configured host/manifest first.

PR CI does not automatically prove this boundary. Inspect workflow scope before claiming coverage. Prepare a concrete candidate and existing access route before requesting any missing privileged-host authorization; do not provision paid infrastructure. S2 acceptance requires the three repairs plus meaningful real-host evidence and independent review, with any remaining liveness limitation explicitly assessed against the campaign goal.

## Continue the established roadmap after S2 acceptance

| Slice | Required observable outcome and return boundary |
|---|---|
| S3 | Genuine N1 executes once, authentic capture retained, independent G5 decision committed. PASS -> N2_READY; statistical FAIL stops. No N2 or aggregate PASS yet. |
| S4 | One joint worker batch yields frozen-depth N2 FULL and Part B H1/H2. G5 commits both from the same capture. Both PASS -> PART_A_READY; either FAIL stops. |
| S5 | One Part A operation retains initial panels and appends only when prescribed. G5 verifies the exact preserved prefix/inventory. PASS -> FULL_PASS_READY; otherwise statistical FAIL. |
| S6 | G5 constructs authenticated full result from retained evidence. Service atomically commits complete PASS or allowed early-failure prefix against VOID. Exact retries recover identical receipt. |
| S7 | Separate installed qseal signs only complete RESULT_COMMITTED_PASS. Service atomically publishes seal receipt against VOID; exact lost-reply recovery preserves current validity. |
| S8 | Exact integrated candidate runs genuine synthetic SEALED_PASS plus all E01–E12 failure, expansion, recovery and invalidity cases on Linux/two-host harness; independent combined review has no blocking findings. |

Read each full slice for exact source/test interfaces before drafting its dispatch. Give every executor an actual accepted predecessor identity, six-field handoff, explicit tests and return boundary. Stage acceptance does not imply combined acceptance. Keep no-draw-on-uncertainty, original Part A prefix, joint N2 batch, frozen thresholds/seeds/depths, G5/qseal identity separation, source-bound configuration and finalization costs intact. Never execute via legacy ProductionExecutor paths. No production capability or account activity is part of this engineering goal.

## Shared decisions that successors must preserve

The budget bounds attributed campaign processes/cgroups, including controllers, qexec campaign work, all descendants, signing/reconstruction and finalization. Ordinary shared platform daemons outside that scope are excluded explicitly; in-scope OS/system costs are not subtracted. No expensive campaign work may be offloaded to excluded infrastructure. Platform waits still consume original wall time. Canonical profiles bind this interpretation.

Raw payload CPU and the installed conservative controller charge are distinct. The entire immutable controller charge is reserved inside the same phase/campaign allowance; configured ceilings require enforcement proof. Common concurrent memory includes campaign controllers/helpers; it is not independent full allowances per child. Unknown counters/termination and overruns bar authority permanently.

Current formats include diagnostic release/profile v3, budget observation/profile v2 and snapshot v4 with recovery/dispatch barriers; the existing database remains v6. Historical readers/semantics are preserved, but old binaries cannot consume new populated records. No downgrade or in-place activation of old dormant/N1 attempts. Store transactions serialize authority; external OS effects are not made atomic by SQLite. Persist intent/barrier first and preserve uncertain outcomes after failed acknowledgement.

## Publication and monitoring

Keep this PR draft while blockers remain; do not promote or merge it to satisfy a monitoring exit condition. Track remote checks/reviews separately from local acceptance and real Linux evidence. Refresh head/base before edits, preserve concurrent work and retarget after S1 integrates only with the correct ancestry. Read the repository babysit workflow when owning PR maintenance. Review requested changes against the governing scope; report consequential expansion instead of silently implementing the whole remaining roadmap during PR maintenance.

Publication base refresh: S1 tip advanced to `f95837ce74b3204890dd1c8bff3cfce37d48456e` by merging four unrelated epistemic planning documents from main. Publication incorporates that documentation-only base update; the accepted runtime predecessor remains `430fc72186a0e642c8811be17d459fd87cbf7533`. No S2 runtime/test edits accompany it.

Publication authorization: the user explicitly approved a command-local pre-commit hook bypass after the unchanged overdue STATE.md gate blocked publication. This exception permits the blocked draft commit, not merge readiness or S2 acceptance. No persistent hook configuration or deadline is changed. The failed hook selected system Python 3.14.3 automatically; that run does not substitute for the source-bound operations-environment checks above.

## Published handoff

Draft PR: https://github.com/Joshua-Asante/first-passage/pull/429
Implementation commit: 292f283. Published head: c77aac476127a31e58ede2c1c0ff03e6406474ce.
Base: codex/full-e1-s1-durable-budget at f95837ce74b3204890dd1c8bff3cfce37d48456e (PR428).
The user approved the one-command hook bypass; it was used for the implementation commit only. The documentation-only base merge ran normally. Worktree was clean after publication. Runtime/test/tool/script/deployment bytes still matched the frozen R1 inventory. Initial remote checks were running; no human reviews or inline comments, and CodeRabbit skipped automatic review because the PR is draft. This local publication addendum follows the committed handoff and does not change source acceptance.
