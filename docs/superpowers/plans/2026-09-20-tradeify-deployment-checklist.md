# Tradeify Deployment Checklist Implementation Plan

> **For agentic workers:** Execute with superpowers:executing-plans; use superpowers:subagent-driven-development when bounded delegation is useful and authorized. Preserve the behavioral contract and integration owner. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver the fixed four-strategy Tradeify portfolio as an authorized attended release, with bounded execution assignments and evidence-backed acceptance.

**Architecture:** Retain the protected qualification service selected by B0. Complete synthetic E1 engineering while progressing settlement, route feasibility, source preparation and attended operations independently. Freeze only after behavior and launch feasibility are settled; production qualification, final binding and activation remain separate decisions.

**Tech Stack:** Existing Python replay/qualification service, Linux execution harness, durable account owner/settlement verifier, production feed and broker adapters, signed release/configuration evidence.

**Spec:** Existing full-E1 S1-S8 specification/roadmap, Phase 3/4 completion handoffs, Phase 5 attended operations and Phase 6 exact-release launch. This checklist organizes those requirements; it changes no portfolio, statistical criterion, authority or source-evidence requirement.

## Current-state audit — September 20, 2026

Read authenticated GitHub PR status and fetched `origin/main`; baseline
`b703448` (PR #439). Main documentation checkout remains at `c2e6eb2` and has
unrelated staged/untracked files. Its root STATE is stale; source inspection here
used `git show origin/main:<path>`, not that checkout's old runtime. No live account,
host or private-source inspection and no runtime tests were performed for this
planning update. Test counts below are attributed historical records, not new runs.

| Area | Established status | Consequence |
|---|---|---|
| Track A / M1 | Committed A8 readiness record reports RESOLVED/PASS, disarmed listener v11, September 14 | Do not rebuild M1; verify freshness only where consumed |
| Simpler batch alternative | PRs #430/#432 merged; B0 explicitly retains protected service | No batch migration task. Manual report review/recovery remains the first-release preference |
| S1 persistence | #428 merged | Reuse accepted durable budget/attempt semantics |
| S2 base and scheduler | #429, #433, #434 merged; #435 improves test evidence | Substantial engineering exists; merge does not establish full E1 |
| Linux environment and configuration | #437 closed #423/#424; #438/#439 merged | Reuse canonical host configuration/tree-binding and gate improvements |
| S2 enforcement closeout | #436 OPEN at `03ef76a` (T01 re-read ~15:30Z): `main` `b703448` merged in, acceptance review 0 BLOCKING / 9 ADVISORY, zero review threads; merge-head S2 run 35518729717 in progress | Closeout packet is an assignment, not completed acceptance; T01 owns it |
| S2 known residuals | Resume-before-exec race (G3, worker branch `0ba2775` local, unpushed, no Linux run), reserved work-name issue (A3, in G4's scope), polkit documentation issue (A4, unowned), store-side advisories A1/A2/A5/A7 (G4 worker started) | T01 makes G3 a required part of S2 acceptance; #436 does not merge on a head that would kill real S3 workers |
| Full protected E1 | Main compute adapter remains N1-only; S3-S8 remain future integrated outcomes | Synthetic complete E1 is not yet established |
| Actual source/F1 | Production-readiness record remains a candidate; synthetic source tests do not accept actual inputs | Refresh F01-F52 and real evidence before freeze |
| Broker transport | Main `book_account_owner.py` still supports only explicit SyntheticBroker and otherwise refuses `production_route_unavailable` | Production adapter is real remaining implementation work |
| Settlement/route | CAP-20260916: R1 qualified locally only; S1-S5, R2-R5 and whole-route N1 unproven | Live release remains blocked pending real producers/consumer traces |
| Incident amendment | Bounded platform-protection ADR remains Proposed on main | Propagate accepted direction before dependent implementation; no native ATM equivalence assumed |
| Production E1, D0/D1, final n3, launch | No accepted completion found in inspected records | Keep distinct future gates; do not infer readiness from merged scaffolding |

References on the inspected baseline:
- [B0 decision](https://github.com/Joshua-Asante/first-passage/blob/b703448/docs/superpowers/plans/2026-09-19-attended-batch-qualification.md).
- [E1 execution slices](https://github.com/Joshua-Asante/first-passage/blob/b703448/docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md).
- [Capability record](https://github.com/Joshua-Asante/first-passage/blob/b703448/docs/briefs/phase4-preparation/2026-09-16/capability-decision.md).
- [Production readiness](https://github.com/Joshua-Asante/first-passage/blob/b703448/docs/briefs/phase3-preparation/2026-09-15/production-readiness.md).
- [S2 current PR](https://github.com/Joshua-Asante/first-passage/pull/436).
- Local September 20 handoff: `docs/briefs/handoffs/2026-09-20-glm-s2-closeout-s3-dispatch.md` (untracked here; proposed closeout and S3 dispatch requirements, not executed return).

Tradeify's support reply supplied by Joshua closes the proprietary certified-close
source avenue. Tradovate-specific report semantics still need evidence. Manual
collection is accepted; it does not waive close equity/flatness or history. No
Tradovate support response beyond that supplied correspondence was established.

## Packet sizing and ownership

The following are task-sized planning envelopes, not token forecasts or minimum
spend. Each includes context acquisition, implementation where applicable,
verification, review/fixes and a coordinator return. A 500k ceiling can finish
well below 500k. Use approximately 60% for construction, 25% verification/review,
15% corrections/return; uncertainty may change that split. At halfway, compare
remaining scope with remaining budget; split at an observable acceptance boundary
before consuming the last quarter. Never stop a risky change halfway and call it
accepted because a token budget was reached.

These are roadmap packets, not simultaneous execution orders. Before dispatch,
the coordinator pins the accepted predecessor, source/config identities, exact
interfaces, executable checks and existing authority in a bounded handoff. Assign
one packet per task; retain smaller checkpoints inside complex packets. No user
task, subagent, token goal or implementation is started by this checklist.

**Common ownership:** one deployment coordinator accepts all returns. Each packet
has one executor owning its integrated outcome. Independent review consumes the
same source-bound evidence; reviewers do not modify the executor's checkout.
Joshua retains the applicable funding, ratification, merge and operational GOs.

**Common verification:** before project Python, use that checkout's `./fp.ps1 doctor`;
run focused tests and required gates via its launcher. Retain interpreter, source/
configuration identity, commands, results, failures/skips and actual Linux evidence
for OS claims. Reuse unchanged evidence. Never replace actual broker/feed/settlement
evidence with a mock. Keep originals and private financial/account facts in approved
private roots. Shared reusable configuration has one canonical owner; bind the
resolved identity at qualification and activation.

## Qualification engineering packets

### T01 — Close S2 and make real worker launch reliable (500k–750k)
**Selected outcome:** S2 accepted as the enforced work boundary on a head that already contains the G3 launch repair, so the first real S3 worker start inherits neither the resume-before-exec race nor the store-side gaps the acceptance review named as S3 preconditions.
**Prerequisites:** Current [#436](https://github.com/Joshua-Asante/first-passage/pull/436) head with #437/#438/#439 merged in; the two live sub-workers below return before integration. Existing closeout owner (GLM) retains this work.
**Ownership:** GLM is the T01 executor and integrates every return; the G3 and G4 workers are sub-executors whose branches GLM merges, not parallel owners of acceptance. The coordinator (Joshua) accepts. Executable packet: [GLM T01 handoff](../../briefs/handoffs/2026-09-20-glm-t01-s2-closeout-g3-worker-launch.md). It supersedes steps 1–5 and 7 of the earlier [GLM closeout packet](https://github.com/Joshua-Asante/first-passage/blob/03ef76a/docs/briefs/handoffs/2026-09-20-glm-s2-closeout-s3-dispatch.md) (on the #436 branch) and **withdraws its step 6**: S3 packet authoring is T02's opening act, not a T01 deliverable, because T02's prerequisite is "resolve S3 Q1–Q12 in the current preparation/dispatch packet" and T01's return boundary excludes every S3 act.

**Verified starting state (2026-09-20 ~15:30Z; re-verify before dispatch):**
- #436 head `03ef76a`, base `main`, `MERGEABLE`/`UNSTABLE` (S2 run, `pytest (3.11)`, boundary host 2 in progress; `skills (3.12)`, CodeRabbit, build, listener, daemon, semgrep green); **0 review threads, no reviews**. Branch since `915035c`: GLM closeout packet committed (`21f02b6`), prior GLM packets backfilled (`cf77edd`), `origin/main` `b703448` merged clean (`b0ced74`), independent acceptance review note **0 BLOCKING / 9 ADVISORY / 10 NOTE, VERIFIED WITH CAVEATS** plus the G4 packet (`03ef76a`).
- Accepted-quality evidence on code-identical heads: runs 35489657203 (`5ac3ad0`) and 35493582848 (`bbafe68`), 15/15, 0 skips, invariants 15/15, cleanup ok. Merge-head run **35518729717** (`03ef76a`) in progress — this is the head-bound run the closeout requires; 35517586779 (`915035c`) was cancelled by the push.
- **G3** (`claude/s2-g3-resume-before-exec`, local worker worktree, locked): one code commit `0ba2775` over `4281d2e` — `campaign_supervisor.py` +158/−, `test_campaign_supervision.py` +290, Linux test +67; commit message claims A2 (guardian half) and A4 folds. **Not on `origin`, no S2 run, §7 pending.**
- **G4** (`claude/s2-g4-store-invariants`, local worker worktree, locked): at `03ef76a` with uncommitted edits to `campaign_store.py`, `campaign_funding.py`, `campaign_budget.py`. Not on `origin`, §7 pending. Owns A1, A2 (store half), A5, A7, A9-3 (= the A3 work-id validator).
- Residuals still open on the candidate: R-G3 (repair in flight), A3/A9-3 validator (G4), A4 README wording (nobody), OOM terminal duality (disclosed, test-only), Windows isolation bridge never claimed.

**Steps (order matters; wait points marked ⏸):**
- [ ] **1. Boundary evidence.** ⏸ Read run 35518729717. Fifteen green → boundary evidence complete. 14/15 carrying only the R-G3 signature (`descendants` work; payload exit non-zero < 0.5 s after the first RESUMED; no burner children; no OOM) → record as R-G3 and dispatch **one** rerun; any other failure, or a second failure, is a return to the coordinator, not a re-roll.
- [ ] **2. Draft the boundary acceptance entry** (append-only, ledger `docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md`): heading `### Coordinator acceptance — S2 enforcement gaps (G1/G2), 2026-09-20`; runs, record IDs, counts, `source_stable`/`capture_complete`, invariants, cleanup for `5ac3ad0`, `bbafe68` and the merge head; steering findings 1–2 at `9d7a731`; the verbatim disclosed-limitations list (R-G3 with rate and fail-closed nature, A3, A4, OOM duality, bridge, "accepted work boundary only — no statistical execution, no N1/N2/Part A dispatch, no activation"). Wording is "S2 ACCEPTED as the enforced work boundary" and nothing wider. **Hold the entry uncommitted until step 6** so it can name the post-G3 head; report the draft at the step-3 checkpoint.
- [ ] **3. G3 return.** ⏸ Wait for G3's §7. Judge it against the frozen repair: resume gated on `/proc/<pid>/exe` basename = installed interpreter and `comm` ≠ `runc:[…]`; `comm`/`exe` retained on PROCESS and RESUMED; `PAYLOAD_EXIT` retained on both settlement paths; Windows regressions (a)(b)(c); Linux assertions in existing nodes only; no probe/profile/ceiling change; `campaign_probe.py` byte-identical. G3 must push its branch and show **one fifteen-green S2 run on its own head** before merge. Record the observed `comm`/`exe` values for runc-init vs python if captured. **Checkpoint (T01): report boundary acceptance (steps 1–2) and G3 readiness as two separate verdicts, even if both are ready.**
- [ ] **4. G4 return.** ⏸ Wait for G4's §7. Each of A1, A2-store, A5, A7, A9-3 gets one disposition: **landed** (Windows test + record ID), or **deferred** with the reason and named as a T02 precondition in the acceptance entry. A9-3 landed ⇒ the A3 validator is closed (derive reserved prefixes from the GLOB constants, no copied strings); A9-3 deferred ⇒ the S3 naming rule in T02's packet is the interim guard. Refuse any version bump that arrived without a `CHECKPOINT`. G4's branch also needs one S2 run before merge; a `descendants` red on G4's pre-G3 bytes with the R-G3 signature is expected and disclosed, not re-rolled.
- [ ] **5. Integrate.** Merge G3, then G4, into `claude/s2-enforcement-gaps-fab5e6` with merge commits (expected touch points: `record_work_transition` CAPTURED-after-settlement refusal from G4 vs G3's guardian-side IN_DOUBT-before-settle — both must survive; `parse_supervision_event` gains `comm`/`exe`/`PAYLOAD_EXIT` from G3, G4 must not enumerate data keys). Byte-check each worker's owned files against its head after the merge. **A4 README wording** lands here as a docs commit: `tools/qualification_verification/README.md` §S2 states that under the accepted polkit rule qexec can start arbitrary transient units including `User=root`, polkit contributes no containment for unit starts, membership rests on the guardian's code checks and `bootstrap.py`'s `campaign_control` fixed-prefix check; delete "manage-units scope"; grep `polkit|manage-units` across README, plans and `campaign_host.py` comments first. Windows selection lines 1–3 + `./fp.ps1 check` on the integrated head with record IDs; push.
- [ ] **6. Post-G3 head-bound run.** ⏸ The push fires the PR-path S2 run on the integrated head. **Fifteen green required with no rerun allowance for a `descendants` failure** — after G3 that signature is a G3 defect, not the known race. Any red → diagnose from the artifact, return. On green: finalise the acceptance entry (add the integrated head, run, G3 and G4 dispositions, the S3 handshake contract sentence — "a real worker's entrypoint must call the probe-side block-then-await resume helper before any work; the guardian resumes only after the observed init pid has exec'd the installed interpreter" — and the review dispositions from step 7); commit; push.
- [ ] **7. Review.** Request one Codex review round on the diff since `03ef76a` only (G3 + G4 + README + ledger). Disposition every Codex/CodeRabbit thread: confirmed-and-repaired, refuted-with-evidence, or deferred-to-named-owner; list them in the acceptance entry. A repair here re-enters step 6.
- [ ] **8. Merge #436.** Preconditions: `skills (3.12)` green on the merge head, step-6 run green, review clear, `mergeStateStatus` not `BEHIND`. Merge commit; branch kept (worker worktrees and evidence runs reference it); PR body rewritten to "ACCEPTED as the enforced work boundary" with the limitations list. Record the merge SHA in the return.
**Verification:** Linux — the merge-head run (step 1), G3's own run, G4's own run, the post-G3 integrated run (step 6); each cited with run ID, record ID, 15/15, 0 skips, invariants passed, both owned-cleanup receipts ok. Windows (PowerShell, `./fp.ps1`, doctor first) — §2.6 lines 1–3 of the G1 packet and `check` on the integrated head, `git diff --check`, `git diff --stat` before every commit. The isolation bridge stays unclaimed and disclosed.
**Rerun rule:** exactly one R-G3-signature rerun is permitted, and only on a pre-G3 head (steps 1 and 4). Nothing else is re-rolled.
**Checkpoints:** after step 3 (two separate verdicts); before step 5 if either worker returned `BLOCKED`/`CHECKPOINT` or the merge is not clean; before step 8 if the step-6 run is not fifteen-green; the moment a version bump, profile/ceiling/release literal, or probe-side change appears in any return.
**Forbidden:** rebase/squash/force-push of the integration branch; relaxing any Linux assertion; re-rolling outside the rerun rule; claiming Windows results as Linux evidence; touching `campaign_probe.py`, profiles, ceilings, release literals, `role_policy.TREE_BINDINGS`, `host.json`, gates or required checks; authoring S3 code or the S3 packet; any activation, N1/N2/Part A dispatch, G5 verdict, result or seal; `git stash`.
**Return boundary:** S2 accepted as the enforced work boundary **and** G3 merged with a fifteen-green integrated run; G4 items landed or named as T02 preconditions; #436 merged. No N1 dispatch, no S3 packet, no claim of full E1. If G3 cannot reach fifteen-green inside the envelope, return `DONE_WITH_CONCERNS` with the boundary acceptance held back — do not merge #436 on a head that would kill real S3 workers.

### T02 — Protected N1 capture and independent decision / S3 (750k–1M)
**Selected outcome:** Genuine N1 -> retained capture -> metered G5 -> committed CONTINUE or statistical failure.
**Prerequisites:** T01; resolve S3 Q1-Q12 in the current preparation/dispatch packet.
**Ownership:** S3 executor integrates worker, capture custody, snapshot/schema and G5; coordinator accepts.
- [ ] Bind release/profile, phase budget, capture storage and G5 launch/accounting topology.
- [ ] Reuse the corrected readiness handshake; preserve N1_ONLY historical contracts.
- [ ] Commit one N1 decision under current revision/validity; PASS reaches N2_READY only.
**Verification:** Real reduced TEST_ONLY PASS/FAIL; fabrication, source/seed mutation, budget, crash and VOID tests; Linux trace.
**Checkpoint:** Return interface conflicts before dependent code; review capture-to-G5 evidence together.
**Return boundary:** Accepted S3; no N2, Part A, full result or seal.

### T03 — Joint N2/Part B / S4 (500k–750k)
**Selected outcome:** One joint batch produces both required decisions without extra sampling.
**Prerequisites:** T02 accepted capture/assessment interfaces.
**Ownership:** S4 executor; coordinator accepts.
- [ ] Extend canonical checkpoint plans and actual compute/capture for FULL and halves.
- [ ] Independently adjudicate both components; advance only on both PASS.
- [ ] Preserve exact depths, streams, evidence membership and one lifetime allowance.
**Verification:** Genuine joint PASS/failure combinations, exact counts/seeds, duplicate dispatch and crash/VOID cases.
**Checkpoint:** Present one complete source-to-decision trace.
**Return boundary:** Accepted PART_A_READY or prescribed failure; no Part A execution.

### T04 — Part A with prescribed expansion / S5 (750k–1M)
**Selected outcome:** Protected Part A preserves the initial prefix and performs only prescribed expansion.
**Prerequisites:** T03; existing canonical Part A/statistical owners.
**Ownership:** S5 executor; coordinator accepts.
- [ ] Integrate actual initial/conditional expansion compute, capture and G5.
- [ ] Keep expansion in its prescribed compute operation, without new draw namespaces.
- [ ] Enforce cumulative resource limits and required final checks.
**Verification:** Expansion/no-expansion, boundary equality, prefix identity, failure and interrupted capture; genuine synthetic trace.
**Checkpoint:** Review expansion mechanics before accepting aggregate output.
**Return boundary:** Accepted Part A decision; no aggregate commit or seal.

### T05 — Complete result and separate seal / S6-S7 (750k–1M)
**Selected outcome:** Exact complete result is atomically committed and an independent sealer publishes PASS only.
**Prerequisites:** T04; canonical full-result evidence and authority schemas.
**Ownership:** One executor across result/seal boundaries; coordinator accepts S6 before proceeding to S7 within this assignment.
- [ ] Reconstruct full-result membership or allowed statistical-failure prefix from retained captures.
- [ ] Bind current validity/revision and distinct enrolled result/seal keys.
- [ ] Persist exact signing intent, commit and identical receipt recovery; refuse stale/VOID/partial results.
**Verification:** Full PASS/failure, duplicate/conflicting requests, invalidation races, crash cuts and historical receipt identity.
**Checkpoint:** S6 result commit is an explicit internal acceptance boundary; split S7 into its own task if needed.
**Return boundary:** Result and seal accepted; no production authority.

### T06 — Full synthetic E1 acceptance / S8 (500k–750k)
**Selected outcome:** One integrated Linux release proves SEALED_PASS and the complete required negative-case suite.
**Prerequisites:** T01-T05 integrated at one source/configuration identity.
**Ownership:** Integration executor and independent review; coordinator owns final engineering acceptance.
- [ ] Execute required E01-E12 cases through actual installed roles; close invariant/CI/evidence gaps.
- [ ] Verify no forbidden continuation, uncharged work or fabricated acceptance across the combined path.
- [ ] Record exact accepted release, Linux evidence and limitations.
**Verification:** Full governing synthetic suite, required gates and independent combined review; no mock substitutes for OS properties.
**Checkpoint:** Report first integrated result and each material cross-component finding.
**Return boundary:** Synthetic E1 engineering accepted; production E1/n3 remain separate.

## External capabilities and production preparation

### T07 — Manual settlement procedure accepted end to end (500k–750k)
**Selected outcome:** Real report originals establish an admissible initial chain and subsequent close through the verifier/account owner.
**Prerequisites:** Account/report access and applicable operator authority; independent of T01-T06.
**Ownership:** Settlement executor; Joshua supplies account-only facts and reviews exact packages; coordinator accepts CAP S1-S5.
- [ ] Establish existing accepted-chain status before selecting a predecessor; no silent reset.
- [ ] Resolve exact Tradovate report timezone, session/filter semantics, coverage, costs and correction handling.
- [ ] Collect manual exports with context; reconcile history and close equity or supported same-boundary flatness.
- [ ] Rehearse isolated anchor/subsequent-close ingestion, correction refusal and restoration; record repeatable daily procedure/time.
**Verification:** Actual original-byte consumer traces plus synthetic missing/correction/restart cases. No signature creates missing source facts.
**Checkpoint:** Return promptly on an unsupported decisive source fact; continue independent collection only.
**Return boundary:** CAP-backed accepted procedure or precise blocked producer/contract decision; no account reset or activation.

### T08 — Broker and protection feasibility decided (500k–750k)
**Selected outcome:** One exact route supports required order semantics and unknown-request closure, or a concrete incompatibility is established.
**Prerequisites:** Current account/platform entitlement; bounded captures/drills require their applicable authorization.
**Ownership:** Capability executor; coordinator owns CAP R2-R5/N1 and incident-contract reconciliation.
- [ ] Inventory all actors, delayed requests, order/fill correlation and terminal/no-future-effect evidence.
- [ ] Map all four legs' entries, partial fills, adds, native amendments, trailing/OCO, scoped exits, takeover and cutoff.
- [ ] Resolve known inline-trail/cancel-replace incompatibilities; assess native protection without assuming economic equivalence.
- [ ] Reconcile proposed bounded incident protection with governing contracts before dependent implementation.
**Verification:** Source-backed semantics and retained actual traces; unsupported route returns a decision, not more speculative adapter code.
**Checkpoint:** Early go/no-go on unknown-request resolution and missing normal primitives.
**Return boundary:** Implementation-ready capability contract or exact route/behavior decision; no whole-route PASS from documentation alone.

### T09 — Actual broker adapter and reconciliation (750k–1M)
**Selected outcome:** Real observations and transport reach the durable account owner under the accepted route contract.
**Prerequisites:** T08 viable route; approved drill environment and exact interfaces. T07 settlement producer available for combined rehearsal.
**Ownership:** Broker integration executor; coordinator accepts combined CAP consumer evidence.
- [ ] Replace the synthetic-only transport gap with the qualified adapter, preserving intent-before-send and unresolved reservations.
- [ ] Ingest real request/order/fill/protection identities, history coverage and terminal outcomes.
- [ ] Prove ordinary four-leg lifecycle, partial fills, cancellation races, restart and manual intervention through owner consumers.
**Verification:** Retained actual route traces plus fault-injected consumer cases; no live manufactured lost response or unmanaged exposure.
**Checkpoint:** Review transport/ownership end to end; if normal execution and recovery exceed scope, split at an accepted normal-route boundary while keeping release blocked.
**Return boundary:** Accepted adapter/reconciliation evidence; disarmed, no autonomous activation.

### T10 — Actual source and freeze packet ready (500k–750k)
**Selected outcome:** Every F01-F52 prerequisite has accepted actual evidence or an explicit unresolved blocker.
**Prerequisites:** Existing preparation artifacts; starts alongside T01, final inventory consumes T06 and pre-freeze dependencies.
**Ownership:** Source/freeze executor; coordinator owns combined freeze readiness.
- [ ] Reconcile seven evidence bundles with the four live ports; reuse valid admission/parity reviews.
- [ ] Accept source/settings, warm-up, active coverage, calendars and cutoff chronology under their real limitations.
- [ ] Prepare canonical inventories, frozen statistical definitions and representative full-workload measurement.
- [ ] Bind intended route/feed/incident/operations changes to the freeze inventory and permitted later bindings.
**Verification:** Actual source consumption/parity and source-bound manifests; authorized representative measurements, not a real attempt used as a benchmark.
**Checkpoint:** Identify missing producer facts early; no guessed historical deadline or coverage.
**Return boundary:** Decision-ready F1 packet, not F1 approval or reserved attempt.

### T11 — Production-class qualification service ready (500k–750k)
**Selected outcome:** The accepted full-E1 engine supports the governed production authority and actual source path.
**Prerequisites:** T06; T10 supplies actual-source contract requirements.
**Ownership:** Qualification release executor; coordinator accepts production-readiness evidence.
- [ ] Implement/review exact production installation, key/role enrollment, release schema and source boundaries; TEST_ONLY cannot promote itself.
- [ ] Validate approved immutable source/configuration loading and authority rejection without consuming a real E1 sample.
- [ ] Complete installed invocation/status/capture procedure and realistic measured resource envelope.
**Verification:** Wrong authority, keys, source, runtime and stale approval refusals; installed host/source evidence and synthetic-authority rehearsal where permitted.
**Checkpoint:** Return any requirement for a new release/authority contract before claiming readiness.
**Return boundary:** Production-capable machinery ready; no real F1/E1 dispatch.

### T12 — Final n3 machinery and launch timing proven (750k–1M)
**Selected outcome:** Separate n3 authorization/capture/adjudication works and a defensible B7-to-activation window exists.
**Prerequisites:** T02 interfaces for preparation; final engineering consumes T05/T06. Timing consumes report/route facts from T07/T08.
**Ownership:** Final-stage executor; coordinator owns freeze-impact and launch-feasibility acceptance.
- [ ] Define and implement protected n3 authority using existing canonical statistical owners; E1 cannot request n3 or vice versa.
- [ ] Bind account seal, exact release, frozen depth/streams and no-redraw semantics.
- [ ] Measure synthetic capture, compute, adjudication, signing, GO/reseal, restart and activation sequence with operator availability.
**Verification:** Stale B7, intervening activity, identity drift, uncertain dispatch, expiry/VOID and timing margins; no real n3 consumed.
**Checkpoint:** Resolve timing-critical semantic conflicts before F1; final exact-candidate rehearsal remains T17.
**Return boundary:** Accepted n3 machinery and timing envelope; no final real draw or activation.

### T13 — Attended operations and recovery implemented (750k–1M)
**Selected outcome:** Alerts, halt, manual intervention, restoration and later-session authorization work through actual consumers.
**Prerequisites:** T08 accepted incident semantics; preparation overlaps, final acceptance consumes T07/T09.
**Ownership:** Operations executor; coordinator accepts with operator rehearsal.
- [ ] Fence every sender, preserve obligations and qualified continuing protection only within its accepted scope.
- [ ] Verify real notification delivery, failure/escalation, external heartbeat and durable acknowledgment.
- [ ] Restore records without stale authority; reconcile unknown orders before fresh later-session permission.
- [ ] Rehearse manual intervention and disarm; acknowledgment never equals permission to resume.
**Verification:** Actual delivery/intervention traces; restart/backup, missed alert, stale evidence and ambiguous protection cases.
**Checkpoint:** Freeze-affecting behavior must finish before F1 or have an explicit permitted binding rule.
**Return boundary:** Accepted attended operating procedure and implementation; no live GO.

### T14 — Production feed selected and qualified (500k–1M)
**Selected outcome:** All four symbols pass the frozen feed protocol through actual adapters with emission disabled.
**Prerequisites:** M1 complete; observe standing A9/O-4 funding restriction. Provider-neutral prep can start now; provider-specific work waits for applicable selection/funding authority.
**Ownership:** Feed executor; coordinator owns TB-I5 acceptance.
- [ ] Prepare entitlement, cost, symbol/roll/session and retention proposal, plus frozen equivalence criteria.
- [ ] Implement approved adapter and qualify original delivered bytes against canonical panels.
- [ ] Verify reconnect, corrections/backfill, duplicate/out-of-order, stale/missing symbol, DST/early-close and synchronization behavior.
**Verification:** Actual four-symbol equivalence and consumer tests; no post-result tolerance changes.
**Checkpoint:** Resolve feed freeze-impact before F1; later funded binding must be explicitly permitted, not presumed exempt.
**Return boundary:** Feed PASS or exact blocker; no signal emission or account orders.

## Qualification and launch

### T15 — Freeze, production E1 and admission (500k–750k envelope; likely less agent work)
**Selected outcome:** One authorized production attempt reaches its prescribed disposition; on PASS, seal plus D0 and separate D1.
**Prerequisites:** T06/T10/T11 and accepted pre-freeze feasibility from T07-T09/T12/T13/T14 as applicable. Complete all behavior-changing frozen work first. Final provider-funded binding may remain only under explicit accepted later-binding rules.
**Ownership:** Qualification coordinator; Joshua supplies exact required decisions.
- [ ] Accept recoverability, shared-inventory change boundary, final-stage ownership and timing checkpoint.
- [ ] Present F1 then its derived exact-depth/budget subject; preserve distinct dependent approvals.
- [ ] Execute production E1 once; retain actual outputs and prescribed failure/interruption disposition.
- [ ] On PASS obtain authenticated seal, D0 admission and affirmative D1 ORB decision.
**Verification:** Exact input/runtime/configuration/authority identity and captured result; no replacement namespace or repair after seeing results.
**Checkpoint:** Return immediately on actual failure or missing authority; continue only independently authorized preparation.
**Return boundary:** Accepted portfolio admission or true non-PASS/blocker; no live activation.

### T16 — Bind and accept the disarmed candidate (500k–750k)
**Selected outcome:** Qualified portfolio, real feed/route, settlement and operations describe one exact deployable candidate.
**Prerequisites:** T07/T09/T13/T14/T15; all required symbols and deduplication evidence.
**Ownership:** Release integration executor; coordinator owns combined acceptance.
- [ ] Materialize accepted live legs/allocations and symbol bindings; verify TB-I4 deduplication prerequisites/cases.
- [ ] Bind actual configuration, image, source/route evidence and release inventory using canonical owners.
- [ ] Prove equality to qualified shared components and only permitted later bindings; requalify if required by a change.
- [ ] Independently review complete candidate and perform separately authorized disarmed integration.
**Verification:** Whole-path real evidence and synthetic fault traces; wrong account/symbol/config/source/evidence refuse readiness.
**Checkpoint:** Any unexplained freeze delta blocks acceptance, even when individual tests pass.
**Return boundary:** Exact accepted disarmed candidate; no fresh expiring B7 until launch preparation is complete.

### T17 — Final rehearsal, sole n3 and initial activation (500k–750k envelope; likely less agent work)
**Selected outcome:** Exact authorized release is effectively active for the approved attended session.
**Prerequisites:** T12/T16, operator availability, complete release packet and applicable integration/launch authority.
**Ownership:** Launch coordinator; Joshua supplies deployment GO and distinct bounded initial-session authorization.
- [ ] Rehearse the entire timed procedure on the final candidate with synthetic inputs.
- [ ] Capture fresh B7, verify account/history/flatness/orders and execution fingerprint; run sole final n3.
- [ ] Apply actual verdict/expiry/void rules; no Part A rerun or automatic replacement draw.
- [ ] Obtain deployment GO, permitted reseal and initial-session authority; verify post-restart image/configuration and durable activation acknowledgment.
**Verification:** Effective runtime activation and source-bound receipts, not merely a config write; failure leaves the candidate disarmed or halted as prescribed.
**Checkpoint:** Stop at each genuine missing operational authority or failed gate; never interpret elapsed time as approval.
**Return boundary:** Authorized attended deployment demonstrated, or precise terminal/blocking disposition. Ongoing performance review is a subsequent assignment.

## Dependency and dispatch summary

- Engineering spine: **T01 -> T02 -> T03 -> T04 -> T05 -> T06**.
- Start **T07, T08 and T10** alongside that spine. Reuse ongoing owners rather than dispatch duplicate work.
- **T09 follows T08**; operations preparation T13 follows the incident decision and finalizes with T07/T09.
- **T11 follows T06**; T12 can prepare against stable interfaces earlier but needs integrated acceptance and a timing answer before F1.
- T14 starts with provider-neutral work only; standing source-independent/funding gates control provider-specific execution.
- **T15** is the join for production qualification: engineering, actual-source readiness and pre-freeze feasibility/behavior inventory must agree.
- **T16 -> T17** closes real binding, combined operational acceptance and actual launch.

Do not serialize all external work behind E1. Do not freeze E1 while required
route/incident changes are still unknown. Do not require paid-feed final binding
before its governing funding checkpoint merely because a task number is lower.

## Verification of this planning artifact

Current status was checked through authenticated GitHub queries and fetched Git
objects. No new test-pass or live-capability claim is made. Before dispatch,
refresh the moving #436 head and ongoing owner returns. The primary checkout's
old staged September 19 documents are not the current B0 record and were left
untouched. This checklist is not a commit, merge, provider contact or deployment.
