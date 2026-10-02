# Tradeify Deployment Checklist Implementation Plan

> **For agentic workers:** Execute with superpowers:executing-plans; use superpowers:subagent-driven-development when bounded delegation is useful and authorized. Preserve the behavioral contract and integration owner. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver the fixed four-strategy Tradeify portfolio as an authorized attended release, with bounded execution assignments and evidence-backed acceptance.

**Architecture:** Retain the protected qualification service selected by B0. Complete synthetic E1 engineering while progressing settlement, route feasibility, source preparation and attended operations independently. Freeze only after behavior and launch feasibility are settled; production qualification, final binding and activation remain separate decisions.

**Tech Stack:** Existing Python replay/qualification service, Linux execution harness, durable account owner/settlement verifier, production feed and broker adapters, signed release/configuration evidence.

**Spec:** Existing full-E1 S1-S8 specification/roadmap, Phase 3/4 completion handoffs, Phase 5 attended operations and Phase 6 exact-release launch. This checklist organizes those requirements; it changes no portfolio, statistical criterion, authority or source-evidence requirement.

## Current state — September 26, 2026 (refreshed from the acceptance ledger)

Derived from the [execution-slices acceptance ledger](2026-09-18-full-e1-execution-slices.md#progress-ledger-and-present-disposition)
at `main@70aa348`; the ledger and each packet's acceptance record own these outcomes, and this table
only routes to them. The September 20 audit below is retained as the dated baseline T01 was planned against.

| Packet | Accepted outcome | Blocker | Owner | Next decision |
|---|---|---|---|---|
| T01 / S2 | **ACCEPTED** 2026-09-21 as the enforced work boundary, G3 launch repair and G4 items landed; #436 merged — [acceptance](2026-09-18-full-e1-execution-slices.md#coordinator-acceptance--s2-budgeted-admission-and-real-linux-work-supervision-2026-09-21) | None | Done | None |
| T02 / S3 | **ACCEPTED** 2026-09-22 at `a8a983e` (genuine protected N1 capture, committed independent G5 decision); #455 merged — [acceptance](2026-09-18-full-e1-execution-slices.md#coordinator-acceptance--s3-genuine-protected-n1-capture-and-committed-independent-g5-decision-2026-09-22) | None | Done | None |
| T03 / S4 | **ACCEPTED** 2026-09-25 at C2 close, after the 2026-09-24 CHANGES REQUIRED and R1–R5 repairs; condition read `ok` (run 36188223563); #501 merged at `228447c` — [C2 close](2026-09-18-full-e1-execution-slices.md#coordinator-checkpoint-c2-close--s4-accepted-2026-09-25-claude-code) · [condition read](https://github.com/Joshua-Asante/first-passage/pull/501#issuecomment-5840025679) | None | Done | None |
| T04 / S5 | ~~Not accepted; packet drafted, D1–D3 ruled~~ — [packet](../../briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md). *2026-10-01:* **C3 ACCEPTED** for TEST_ONLY on the evidence at `claude/s5-part-a@606e6e0` ([ruling](2026-09-18-full-e1-execution-slices.md#operator-ruling--c3-accepted-s5-accepted-for-test_only-on-landing-2026-10-01)). **S5 ACCEPTED for TEST_ONLY** when landing PR #578 merged at H = `1fe99fa` (merge `83329e2`). The named defects D-S5-1/D-S5-2/D-S5-3 are open | None for TEST_ONLY. The 2026-09-25 freeze hold ([ledger](2026-09-18-full-e1-execution-slices.md#operator-ruling--s5-freeze-held-2026-09-25)) was released for the build at CP-1b on 2026-09-28 ([ledger](2026-09-18-full-e1-execution-slices.md#operator-ruling--cp-1b-s5-hold-released-for-the-test_only-build-2026-09-28)), and C3 was accepted on 2026-10-01. The remaining gate is D-S5-1/D-S5-2/D-S5-3, fixed in two slices (#586, merged `981eb12`; then the D-S5-3 slice, #589), both before T05 R1 ([defects ruling](2026-09-18-full-e1-execution-slices.md#operator-ruling--land-s5-with-two-named-test_only-defects-fix-before-t05-2026-10-01) · [D-S5-3 ruling](2026-09-18-full-e1-execution-slices.md#operator-ruling--d-s5-3-capture-exact-retry-demotion-also-gates-t05-r1-2026-10-01)) | Operator (rulings); then campaign coordinator (freeze, dispatch) | ~~Operator: §5.1 boundary list, N1 resource accounting, N2 interruption recovery; then freeze S5 at the merged head~~ *2026-10-01, superseded:* the build was released at CP-1b (2026-09-28) and C3 accepted (2026-10-01). Next: **two D-S5 fix slices, each with its own full S4-plus-Part-A Linux run and its own acceptance: #586 (D-S5-1/D-S5-2; merged `981eb12`), then the D-S5-3 slice, #589 (from `claude/capture-retry-noop`)**. Both must merge **before T05 integration acceptance (R1)** ([defects ruling](2026-09-18-full-e1-execution-slices.md#operator-ruling--land-s5-with-two-named-test_only-defects-fix-before-t05-2026-10-01) · [D-S5-3 ruling](2026-09-18-full-e1-execution-slices.md#operator-ruling--d-s5-3-capture-exact-retry-demotion-also-gates-t05-r1-2026-10-01)) |
| T05 / S6–S7 | S6 accepted as an interface; S6+S7 **accepted as a build** (`35c8c08`, then the settlement-rule follow-up `c3cea75`); build **frozen at `claude/t05-result-seal@6cf2732`** (`c3cea75` + #468 settlement wait + `main` through 09-23); acceptance proper not granted — [build entry](2026-09-18-full-e1-execution-slices.md#t05-s7-return--build-complete-s6--s7-at-35c8c08-accepted-as-a-build-acceptance-proper-waits-on-t04-2026-09-21) · [follow-up](2026-09-18-full-e1-execution-slices.md#t05-follow-up--the-s3-settlement-rule-applied-to-the-result-and-seal-commits-accepted-into-the-build-2026-09-22) · [frozen head](../../briefs/handoffs/2026-09-24-full-e1-coordinator-handoff.md) | ~~Waits on T04/S5 acceptance~~ *2026-10-01:* S5 is accepted for TEST_ONLY (#578). T05 waits on **both D-S5 fix slices merged, each with its own full S4-plus-Part-A Linux run: #586 (D-S5-1/D-S5-2; merged `981eb12`), then the D-S5-3 slice, #589 (from `claude/capture-retry-noop`)** ([defects ruling](2026-09-18-full-e1-execution-slices.md#operator-ruling--land-s5-with-two-named-test_only-defects-fix-before-t05-2026-10-01) · [D-S5-3 ruling](2026-09-18-full-e1-execution-slices.md#operator-ruling--d-s5-3-capture-exact-retry-demotion-also-gates-t05-r1-2026-10-01)) | Campaign coordinator | Integrate the frozen head `6cf2732` after S5 acceptance, on a `main` that includes the D-S5 fix (integration preparation H9 may start earlier) |
| T06 / S8 | Not started | T01–T05 integrated at one identity; **S5 open questions Q1 and Q7 decided by the statistical owner** (C3 ruling 2026-10-01) | Campaign coordinator | Dispatch after T05 integration |

External packets as of the [2026-09-24 handoff entry](2026-09-18-full-e1-execution-slices.md#coordinator-handoff--end-of-2026-09-24-campaign-ownership-passes-to-the-next-coordinator-session):
T07 blocked on three S2 source facts ([packet](../../briefs/handoffs/2026-09-21-tradeify-t07-manual-settlement-procedure.md));
T08 R3 = NONE, live release held pending the vendor question ([packet](../../briefs/handoffs/2026-09-21-tradeify-t08-broker-protection-feasibility.md));
T10 step 4 budget term awaits a synthetic probe ([packet](../../briefs/handoffs/2026-09-21-tradeify-t10-source-and-freeze-packet.md));
~~T00 INSUFFICIENT on P7(b)~~ *2026-10-01:* the **T00 step-1 return is complete: P7 MET (RESOLVED) at code `2baa516`** (this does not satisfy D-feed (a), which needs step-3 GO-evidence) on `claude/t00-p7-tasks-3-4` ([closure](../../briefs/handoffs/2026-09-24-tradeify-t00-p7-closure.md)). **Pending gate:** P7 re-run, `accept_p7_record` and a fresh source approval at the head T00 merges at, after S5 and, as recommended, after both D-S5 fix slices (#586, merged; and the D-S5-3 fix, #589) ([C3 ruling](2026-09-18-full-e1-execution-slices.md#operator-ruling--c3-accepted-s5-accepted-for-test_only-on-landing-2026-10-01)).
**Sequencing from 2026-09-27:** the [staged-acceptance addendum](#addendum-2026-09-27--staged-acceptance-evidence-proportional-to-the-next-step) governs the order of next actions, the S5 build-entry/C3 split and the operator checkpoints; the rows above still own outcomes.
**Current sequence from 2026-09-28:** the [continuation addendum](#addendum-2026-09-28--current-sequence-after-the-route-commissioning-documentary-closeout) states which step is next in each workstream after the route-commissioning documentary closeout. It changes no packet outcome, gate, authority or checkpoint, and the 2026-09-27 addendum still governs sequencing wherever the two meet.
Campaign ownership: the Claude Code coordinator under the [2026-09-25 transfer](2026-09-18-full-e1-execution-slices.md#coordinator-transfer--claude-code-continuation-2026-09-25). No production, activation, arm or trade authority follows from any row.

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
| S2 enforcement closeout | #436 OPEN at `12d6a6f` (T01 re-read ~15:45Z): `main` `b703448` merged in, acceptance review 0 BLOCKING / 9 ADVISORY, zero review threads; head-bound S2 run 35519689776 in progress | GLM holds the engineering work order; acceptance and merge are the coordinator's (T01 part B) |
| S2 known residuals | Resume-before-exec race (G3 @ `0ba2775`, unverified), work-id validator A9-3 + store advisories A1/A2/A5/A7 (G4 @ `8c764d8`, WIP, untested), polkit README sentence A4 (unowned); both workers stopped by the operator, GLM finishes them under the 09-20 acceptance-continuation packet | T01 makes G3 a required part of S2 acceptance; #436 does not merge on a head that would kill real S3 workers |
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
**Prerequisites:** Current [#436](https://github.com/Joshua-Asante/first-passage/pull/436) head with #437/#438/#439 merged in (done at `b0ced74`). GLM already holds the work order for the engineering half.
**Ownership:** Two parts. **Part A (GLM):** finish the stopped G3 and G4 workers, integrate, Codex, return — under the coordinator's [`2026-09-20-glm-s2-acceptance-continuation.md`](https://github.com/Joshua-Asante/first-passage/blob/12d6a6f/docs/briefs/handoffs/2026-09-20-glm-s2-acceptance-continuation.md) (on the #436 branch), which governs GLM and withholds acceptance and merge. **Part B (coordinator):** judge the return, write the acceptance entry, merge — under the [T01 packet](../../briefs/handoffs/2026-09-20-glm-t01-s2-closeout-g3-worker-launch.md). The T01 packet supersedes the acceptance/merge content of the earlier [GLM closeout packet](https://github.com/Joshua-Asante/first-passage/blob/03ef76a/docs/briefs/handoffs/2026-09-20-glm-s2-closeout-s3-dispatch.md) (its "G3 is not a merge gate" ruling is reversed here) and **withdraws its step 6**: S3 packet authoring is T02's opening act, because T02's prerequisite is "resolve S3 Q1–Q12 in the current preparation/dispatch packet" and T01's return boundary excludes every S3 act.

**Status (2026-09-26):** complete — every step discharged by the [S2 acceptance entry](2026-09-18-full-e1-execution-slices.md#coordinator-acceptance--s2-budgeted-admission-and-real-linux-work-supervision-2026-09-21) (written under that title rather than B5's draft title) and the #436 merge.

**Verified starting state (2026-09-20 ~15:45Z; re-verify before dispatch):**
- #436 head `12d6a6f` (= `03ef76a` + continuation packet), base `main`, mergeable, **0 review threads, no reviews**. `03ef76a` = `origin/main` `b703448` merged clean (`b0ced74`) + independent acceptance review **0 BLOCKING / 9 ADVISORY / 10 NOTE, VERIFIED WITH CAVEATS** + the G4 packet.
- Accepted-quality evidence on code-identical heads: runs 35489657203 (`5ac3ad0`) and 35493582848 (`bbafe68`), 15/15, 0 skips, invariants 15/15, cleanup ok. Head-bound runs on the `main`-merged tree: 35517586779 and 35518729717 both cancelled by the next push; **35519689776 (`12d6a6f`) in progress**.
- **Workers stopped by the operator mid-task; GLM finishes both.** G3 `claude/s2-g3-resume-before-exec` @ `0ba2775`: one commit (packet repair + coordinator addendum: A2 guardian half, A4 funding-pending tolerance), **no verification run, §7 empty**. G4 `claude/s2-g4-store-invariants` @ `8c764d8`: coordinator-pushed WIP of uncommitted edits, **no tests, hooks bypassed, mid-rewrite of `claim_void_authentication`, possibly non-compiling**.
- Residuals: R-G3 (G3), A9-3 work-id validator (G4), A4 README sentence (unowned — part B), OOM terminal duality (test-only, disclosed), Windows isolation bridge never claimed; review A3/A6/A8 recorded as S3 preconditions, not repaired.

**Steps (order matters; WAIT = wait point):**
- [x] **A1–A5 (GLM, by reference).** Finish G3 (Windows §2.6 lines 1–2, one fifteen-green S2 run on its head, §7) → finish G4 (five rulings with Windows regressions, one S2 run, §7; a needed version bump is a `CHECKPOINT`, not a change) → merge G3 then G4 into the integration branch, byte-check owned files, §2.6 lines 1–3 + `check`, push → PR-path S2 run on the integrated head fifteen green with the artifact read → Codex round dispositioned → ledger entry "GLM continuation 2 — S2 acceptance candidate" (closed A1/A2/A4/A5/A7/A9-3 vs recorded A3/A6/A8), PR body updated. Return.
- [x] **B1. Judge the return** (WAIT for it; re-run or read the cited records; read the integrated run's artifact; owned-file byte checks; `campaign_probe.py`/profiles/ceilings/release literals unchanged since `4281d2e`). **Checkpoint (T01): state boundary evidence and G3 readiness as two separate verdicts, even if both are ready.**
- [x] **B2. G3 is a merge gate.** A `descendants` red on the post-G3 head is a G3 defect — no rerun; back to GLM with the artifact facts. The single R-G3-signature rerun (`descendants`; payload exit non-zero < 0.5 s after the first RESUMED; no burner children; no OOM) applies to pre-G3 heads only.
- [x] **B3. Disposition each G4 item** (A1, A2-store, A5, A7, A9-3): landed with a named Windows test + record ID, or deferred with reason as a T02 precondition. A9-3 deferred ⇒ T02's packet carries the S3 naming rule.
- [x] **B4. A4 README sentence** (docs commit, or one-line delegation to GLM): qexec can start arbitrary transient units incl. `User=root`; polkit contributes no containment for unit starts; membership rests on the guardian's code checks and `bootstrap.py`'s `campaign_control` prefix check; "manage-units scope" removed; grep `polkit|manage-units` first. The docs push re-fires the S2 run; it must stay green.
- [x] **B5. Acceptance entry** (append-only): `### Coordinator acceptance — S2 enforcement gaps (G1/G2) with G3 launch repair, 2026-09-20` — every run with record ID/counts/SHA, steering findings at `9d7a731`, G3 and G4 dispositions, review dispositions, the S3 handshake contract sentence ("a real worker's entrypoint must call the probe-side block-then-await resume helper before any work; the guardian resumes only after the observed init pid has exec'd the installed interpreter"), the A4 sentence, the verbatim limitations list ending "accepted work boundary only — no statistical execution, no N1/N2/Part A dispatch, no activation". Says "S2 ACCEPTED as the enforced work boundary; G3 launch repair landed" and nothing wider.
- [x] **B6. Merge #436** — `skills (3.12)` green on the merge head, post-G3 run green, review clear, not `BEHIND` (merge `main` in if it moved; S2 run repeats). Merge commit, branch kept, PR body rewritten. Record the SHA.
**Verification:** Linux — the `main`-merged head-bound run, G3's own run, G4's own run, the integrated post-G3 run, the docs-push run; each with run ID, record ID, 15/15, 0 skips, invariants passed, both owned-cleanup receipts ok, checked-out SHA. Windows (PowerShell, `./fp.ps1`, doctor first) — §2.6 lines 1–3 of the G1 packet and `check` on the integrated head; `git diff --check`; `git diff --stat` before every commit. The isolation bridge stays unclaimed and disclosed.
**Checkpoints:** B1 (two verdicts); before B5 if either verdict is not ready; before B6 if `main` moved or a review thread is open; immediately on any version bump, profile/ceiling/release-literal or probe-side change in the return.
**Forbidden:** writing "S2 ACCEPTED" before the post-G3 integrated run is fifteen green; merging with a `descendants` failure on the post-G3 head; rebase/squash/force-push of the integration branch; relaxing any Linux assertion; re-rolling outside the rerun rule; claiming Windows results as Linux evidence; touching `campaign_probe.py`, profiles, ceilings, release literals, `role_policy.TREE_BINDINGS`, `host.json`, gates or required checks; authoring S3 code or the S3 packet; any activation, N1/N2/Part A dispatch, G5 verdict, result or seal; `git stash`.
**Return boundary:** S2 accepted as the enforced work boundary **and** G3 merged with a fifteen-green integrated run; G4 items landed or named as T02 preconditions; #436 merged. No N1 dispatch, no S3 packet, no claim of full E1. If G3 cannot reach fifteen-green inside the envelope, return `DONE_WITH_CONCERNS` with the boundary acceptance held back — do not merge #436 on a head that would kill real S3 workers.

### T02 — Protected N1 capture and independent decision / S3 (750k–1M)
**Status (2026-09-26):** accepted — see the S3 row in [Current state](#current-state--september-26-2026-refreshed-from-the-acceptance-ledger).
**Selected outcome:** Genuine N1 -> retained capture -> metered G5 -> committed CONTINUE or statistical failure.
**Prerequisites:** T01; resolve S3 Q1-Q12 in the current preparation/dispatch packet.
**Ownership:** S3 executor integrates worker, capture custody, snapshot/schema and G5; coordinator accepts.
- [x] Bind release/profile, phase budget, capture storage and G5 launch/accounting topology.
- [x] Reuse the corrected readiness handshake; preserve N1_ONLY historical contracts.
- [x] Commit one N1 decision under current revision/validity; PASS reaches N2_READY only.
**Verification:** Real reduced TEST_ONLY PASS/FAIL; fabrication, source/seed mutation, budget, crash and VOID tests; Linux trace.
**Checkpoint:** Return interface conflicts before dependent code; review capture-to-G5 evidence together.
**Return boundary:** Accepted S3; no N2, Part A, full result or seal.

### T03 — Joint N2/Part B / S4 (500k–750k)
**Status (2026-09-26):** accepted — see the S4 row in [Current state](#current-state--september-26-2026-refreshed-from-the-acceptance-ledger).
**Selected outcome:** One joint batch produces both required decisions without extra sampling.
**Prerequisites:** T02 accepted capture/assessment interfaces.
**Ownership:** S4 executor; coordinator accepts.
- [x] Extend canonical checkpoint plans and actual compute/capture for FULL and halves.
- [x] Independently adjudicate both components; advance only on both PASS.
- [x] Preserve exact depths, streams, evidence membership and one lifetime allowance.
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
**Carried obligation (operator, 2026-09-29):** an independently observed pilot draw, replacing the TEST_ONLY plan-agreement pilot identity (S5 B4), is due with T05 and before CP-6; see H9 in [staged acceptance](../../briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md).

### T06 — Full synthetic E1 acceptance / S8 (500k–750k)
**Selected outcome:** One integrated Linux release proves SEALED_PASS and the complete required negative-case suite.
**Prerequisites:** T01-T05 integrated at one source/configuration identity. *2026-10-01:* also S5 open questions **Q1** (whether a committed FAIL on an exhausted campaign counts under ADR §4) and **Q7** (R7's production evidence standard), decided by the statistical owner before S8 starts ([C3 ruling](2026-09-18-full-e1-execution-slices.md#operator-ruling--c3-accepted-s5-accepted-for-test_only-on-landing-2026-10-01)).
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
**Selected outcome:** Real observations and transport reach the controller boundary selected by the accepted capability allocation and route contract. The existing durable account owner is reusable machinery, not a predetermined architecture.
**Prerequisites:** T08 viable route, decided under the [2026-09-26 route-feasibility-first addendum](#addendum-2026-09-26--route-feasibility-is-the-first-deployment-decision) (accepted REST assessment and any contract acceptance it requires); coordinator-accepted [TradingView/CrossTrade capability allocation and deletion map](../../briefs/handoffs/2026-09-25-tradeify-capability-allocation-deletion-map.md), with resulting operator-owned behavior/contract decisions accepted, before finalizing or implementing T09; approved drill environment and exact interfaces. T07 settlement producer available for combined rehearsal.
**Ownership:** Broker integration executor; coordinator accepts combined CAP consumer evidence.
The steps below are the current implementation baseline; the coordinator must rescope them to the accepted allocation before dispatch, retaining required behavior without duplicating qualified vendor capabilities.
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
- **Route feasibility first** (2026-09-26 addendum): T08 plus the REST assessment decide the route before any route-dependent work. **T09 follows the accepted T08/REST result, [capability allocation/deletion map](../../briefs/handoffs/2026-09-25-tradeify-capability-allocation-deletion-map.md) and any resulting contract or expression acceptance**; operations preparation T13 follows the incident decision and finalizes with T07/T09.
- **T11 follows T06**; T12 can prepare against stable interfaces earlier but needs integrated acceptance and a timing answer before F1.
- T14 starts with provider-neutral work only; standing source-independent/funding gates control provider-specific execution.
- **T15** is the join for production qualification: engineering, actual-source readiness and pre-freeze feasibility/behavior inventory must agree.
- **T16 -> T17** closes real binding, combined operational acceptance and actual launch.
- **2026-09-27:** the next bounded action per workstream, its evidence classes and the operator checkpoints CP-1a..CP-9 are in the [staged-acceptance addendum](#addendum-2026-09-27--staged-acceptance-evidence-proportional-to-the-next-step); where it differs from the order above, it governs sequencing.

Do not serialize all external work behind E1. Do not freeze E1 while required
route/incident changes are still unknown. Do not require paid-feed final binding
before its governing funding checkpoint merely because a task number is lower.

## Addendum 2026-09-26 — route feasibility is the first deployment decision

**Operator direction (2026-09-26).** The operator confirmed on 2026-09-26, verbatim: "confirm route-first, the T09 gates and the allocation objective" ([PR #506 comment](https://github.com/Joshua-Asante/first-passage/pull/506#issuecomment-5845088628)). The first deployment decision is route
feasibility; route-dependent work waits on it. T08's current verdict blocks the route as
contracted (R3 = NONE; [T08 §7.8](../../briefs/handoffs/2026-09-21-tradeify-t08-broker-protection-feasibility.md#78-operator-ruling-on-the-return-2026-09-24)).
The 09-25 support reply corrects the earlier durable-replay premise and makes
CrossTrade-mediated REST worth assessing. It does not establish safe resolution
of lost responses.

1. **Decision owner.** The bounded
   [CrossTrade REST route assessment](../../briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md)
   returns two separate answers, which stay separate in every consumer:
   - **Portfolio execution:** can the route execute the unchanged accepted portfolio?
   - **Ambiguous requests:** how does the route handle a request whose outcome is unknown?

   Better responses or a same-session lookup do not answer the second question.
2. **T09 stays behind that result.** No adapter, REST producer, endpoint or fallback implementation starts until all four rows of the [gate acceptance record](#t09-gate-acceptance-record) are accepted against named revisions. Finalize T09 scope against the accepted allocation before implementation.

   **Allocation objective (operator direction, confirmed 2026-09-26; [PR #506 comment](https://github.com/Joshua-Asante/first-passage/pull/506#issuecomment-5845088628)):** let TradingView and CrossTrade own the capabilities they can reliably provide for the exact route; our shared controller fills evidenced gaps. The map must justify retained local responsibilities and identify components that can be removed, reduced or avoided, separating preserved portfolio behavior from simplifications requiring a decision. It consumes the REST assessment as evidence rather than repeating it. Existing account-owner machinery is a reuse candidate, not a required final boundary. The dated allocation handoff must be committed and refreshed against the current route-native edition decisions and completed REST return before dispatch.

   Adjacent work may continue only where it is independent of both route choice and capability allocation. This applies to the engineering spine, T07, T10 and provider-neutral T14; those packet labels are not blanket exemptions. Defer work whose value depends on retaining a component under evaluation. Offline qualification obligations remain unless separately changed by their owner. Producing the private route-native edition files (ORB/Striker and Vanguard production handoffs, gates G2b and G3b) is not adjacent work: by operator ruling 2026-09-26 it waits until gate D accepts the allocation map.
3. **Freeze stays behind it too.** Do not freeze E1 while route, incident or capability-allocation changes are unknown. The freeze inventory must reflect the accepted allocation, resulting behavior decisions and required requalification.

### T09 gate acceptance record

This table owns the gate definitions; STATE and the REST disposition link here. Each acceptance must name the artifact revision, reviewer, date and any residual conditions. **Gate A was accepted with changes on 2026-09-26; gates B–D remain pending.** A returned finding, a draft pre-registration or a passing documentation check is not an acceptance.

| Gate / owner | Evidence and completion condition | Acceptance record | Work unlocked |
|---|---|---|---|
| A — factual assessment / coordinator | Review the REST return, retained vendor evidence and Vanguard source return. Record the disposition of each material finding, correction and the dispatch-process breach. Keep session-scoped positive recovery distinct from unestablished cross-session recovery and absent negative closure. | REST coordinator disposition, with a linked disposition on the Vanguard return; exact evidence revisions. **Accepted with changes 2026-09-26** (operator ruling; recorded by the coordinating session): [REST §6.11](../../briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md#611-gate-a-factual-disposition), accepted text at `5037ba4`, including the Vanguard A6 disposition. Residuals: A3 classifier constraint; A6 successor-binding check at freeze; drill map by behavior and interface. | Use accepted findings for the operator decision and allocation/design analysis; no behavior change or T09 implementation. |
| B — behavior and contract decisions / operator | Following factual disposition, choose Vanguard edition or rejection and record the resulting book consequence. Accept the required expression contracts and unknown-request policy (Proposed B or another amendment), including decision-bearing OWED rules; link required pre-registration/requalification obligations. Allocation-induced changes also require operator acceptance before D closes. | Campaign §59 decision/addendum and the owning incident amendment; named revisions, not draft existence. Pending. | Plan against the approved behavior and recovery contract; no route qualification, replay or live GO. |
| C — viable for bounded design / coordinator, within B's operator authority | Produce a per-leg requirement-to-route map for the chosen expressions and recovery contract. No required unsupported primitive may remain without an accepted expression/contract resolution. Every unproven primitive must have a named validation method, owner, failure consequence and explicit hold on dependent rehearsal/qualification. State the exact interface assumptions and bounded T09 deliverable. If a required capability cannot be supplied or tested, return BLOCKED. | T08/REST coordinator disposition linking the feasibility map and residual validation obligations. Pending. | Technical viability for the bounded design only; all four gates are still needed for T09 dispatch. |
| D — capability allocation and T09 scope / coordinator; operator for resulting behavior changes | Accept the TradingView/CrossTrade/local [responsibility and deletion map](../../briefs/handoffs/2026-09-25-tradeify-capability-allocation-deletion-map.md). Every retained local responsibility has an evidenced gap; every removed/reduced responsibility has a qualified replacement or stays retained pending proof. Record any new B decisions and revisit C if allocation changes its assumptions. Commit a bounded T09 handoff with exact interfaces, verification and return boundary. | Accepted allocation map plus T09 handoff revisions, linked here when available. Pending. | With A–C accepted, dispatch only the bounded T09 work. Deletion, account actions, drills, requalification and release still require their own authority and evidence. |

Acceptance of evidence (A) is separate from acceptance of changed behavior (B). C permits bounded design with explicitly held validation dependencies; it is not a whole-route PASS. E1 freeze still requires the accepted allocation and complete behavior inventory, and execution/release retain their existing qualification gates.

No drill, account access, vendor contact, spend, contract change or GO is granted by this addendum.

## Addendum 2026-09-27 — staged acceptance: evidence proportional to the next step

**Operator direction (2026-09-27, in session).** "Adopt evidence proportional to the next step: establish enough to bound that step, execute it under explicit limits, and use the results to decide what follows. Unknowns should block the activity they affect, rather than every downstream preparation task." The direction "changes sequencing and evidence collection. It does not waive portfolio qualification or authorize trades." It authorizes this revision of the sequence and the preparation of the handoffs in the [staged acceptance handoff set](../../briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md). It does not by itself authorize account actions, spending, S5 execution, production attempts or deployment. Those approvals are taken at the checkpoints in §4, each against a reviewable return, not through repeated requests about routine implementation.

**Revised 2026-09-27 after the operator's review of `9448373`.** The corrections:
- Consume the returns of [#519](https://github.com/Joshua-Asante/first-passage/pull/519) at its pinned head instead of redispatching their work.
- Separate the authority to prepare a measurement proposal from the authority to execute measurements.
- §A11 does not settle the fence classification, which becomes a contract decision.
- "No same-session resume" becomes an explicit policy choice.
- Commissioning evidence can support capability acceptance within its demonstrated scope.
- CP-3 comes before each order-producing action.
- S5's pre-build feasibility is arithmetic on proposed values.
- RC-4/RC-5 assignment happens now.
- Result/seal integration keeps its full-S5-acceptance dependency.

The changed gates are in §0.

This addendum governs **sequencing** where it differs from the packet order above. It changes no packet's selected outcome, verification standard, statistical criterion or authority. It also leaves unchanged the T09 gate record, campaign §59 and incident ADR §A11/§A11.1. Owners stay as the [routing rule](../../../STATE.md) names them:
- the execution-slices ledger owns the S5 conditions;
- the drill plan and the incident ADR own route drills;
- CAP owns capability outcomes;
- the handoff set owns the individual assignments.

**Returns consumed, not redispatched** (#519, unmerged, reviewed at its pinned head [`8c15f18`](https://github.com/Joshua-Asante/first-passage/tree/8c15f1853e64f14f50995e3f1c55a620a0f674b7); each carries a coordinator review "ACCEPTED AS INPUT"):
- the S5 Part A measurement proposal, together with its fix round and coordinator review;
- the ORB lifecycle evidence;
- the account-fence four-state trace;
- the close-semantics C-a note.

The handoffs H1–H4 in the handoff set continue from those returns.

### 0. Changed gates

| Gate | Existing authority (unchanged) | Proposed amendment (this addendum) | Decision still required |
|---|---|---|---|
| **S5 hold: what releases the build** | S5 HELD. RC-1 is now met on `main`: #517 merged at `5ad04cf`. Ruling 2026-09-26 §6 authorizes *preparing* a measurement proposal only | RC-3 splits. **RC-3a** is at build entry: an approved rule applied to a valid record from an approved forced-expansion measurement of the **existing** engine, giving a provisional PART_A ceiling, plus Σ-feasibility as **arithmetic on the proposed `/v7` values**. **RC-3b** is at Checkpoint C3: the adapter measurement (Stage 1c), the **executed** binding check on the built `/v7`, and the Stage 2/PA-5 consistency check. **RC-4/RC-5 assignment** is made now and stays a build-entry condition: RC-5 is assigned by the coordinator (H7), and the RC-4 slice is named by the operator (CP-1a). Only the seed-view implementation and the host attestations are staged before F1 *[Corrected 2026-09-27: of the host attestations, only OF-7 is staged before F1 (G-F1); the full OF-1..OF-7 set is read at CP-8, per the ledger's RC-5 entry.]* | **RULED 2026-09-27:** the staged structure is approved, the rule's scope is PART_A only (TEST_ONLY), and arithmetic is the pre-build feasibility ([ledger](2026-09-18-full-e1-execution-slices.md#operator-ruling--s5-staged-gates-approved-part-a-only-rule-scope-hold-kept-2026-09-27)). **CP-1a RULED 2026-09-27** ([ledger](2026-09-18-full-e1-execution-slices.md#operator-ruling--cp-1a-decisions-16-adopted-as-recommended-hold-kept-2026-09-27)): the rule's parameters (decision (1)) and the `/v7` N2 ruling (decision (3), 360 s CPU / 900 s wall, TEST_ONLY diagnostic profile only). **Still required:** **CP-1b** (hold release) *[2026-09-28: CP-1b released the TEST_ONLY build. 2026-10-01: C3 accepted, and S5 accepted for TEST_ONLY on #578's merge ([ruling](2026-09-18-full-e1-execution-slices.md#operator-ruling--c3-accepted-s5-accepted-for-test_only-on-landing-2026-10-01)).]* |
| **Measurement execution** | None. Preparation authority grants no CI-configuration change, Linux dispatch or artifact download | One approval of a concrete **measurement dispatch**, with its steps, limits and outputs. The coordinator then executes within it without asking again | **CP-1a RULED 2026-09-27** ([ledger](2026-09-18-full-e1-execution-slices.md#operator-ruling--cp-1a-decisions-16-adopted-as-recommended-hold-kept-2026-09-27), decision (2)): the bounded dispatch is approved, image-first with the `host_venv` fallback, and the coordinator executes within the §12.7 caps without asking again. *[2026-09-27: execution is sequenced by the gate in [r2 "Current authority"](../../notes/2026-09-27-s5-part-a-measurement-proposal-r2.md): the harness PR merged by the operator, its evidence archived on `first-passage-archive`'s `main`, and the post-merge audit recorded on the H1 row.]* **Still owed:** the Stage 0 coverage check (r2 §16.4), run locally. *[2026-09-28: done; coverage holds. The measurements are executed, and the CP-1b packet is in the [ledger](2026-09-18-full-e1-execution-slices.md#coordinator-cp-1b-packet--build-entry-status-2026-09-28).]* *As presented:* approve the dispatch ([r2 §14.1](../../notes/2026-09-27-s5-part-a-measurement-proposal-r2.md) decision (2), which folds in #519 decision 4), including host venv versus worker image. Stage 0 is optional calibration: the S4 logs are preserved, and the 2026-10-09 expiry binds only if the preserved set does not cover Stage 0's inputs, which is verified locally, owed (r2 §16.4). The dispatch must show adapter-level forced expansion at Stage 1c and complete aggregate-memory evidence (ruling 2026-09-27) |
| **Fence repair** | B–D packet: a required correctness repair, resolved before the ORB freeze; coordinator trace; T09 repair. §A11 item 1 fixes the **response** to an unresolved request (preserve-and-block), not which requests are unresolved | Once the classification contract is accepted, a synthetic classification-and-consumer packet (H4) may precede T09. The evidence producer and route integration stay T09's. A synthetic return cannot mark the fence obligation resolved | **RULED 2026-09-27** ([§59 Ruling 7(b)](../../briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#ruling-7--orb-lifecycle-l1-reaffirmed-and-the-account-fence-classification-contract-2026-09-27)): the fresh-evidence classification, stale at one bar and pinned in tests, and refreshed evidence never resumes a halted account. The synthetic repair is authorized; the real producer and route acceptance are retained. **Still required:** acceptance of the H4 return (synthetic half); T09 for the rest |
| **ORB lifecycle** | Ruling 5 fixed the resolution order; the evidence has been returned (#519) | None | **RULED 2026-09-27** ([§59 Ruling 7(a)](../../briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#ruling-7--orb-lifecycle-l1-reaffirmed-and-the-account-fence-classification-contract-2026-09-27)): L1 with the earlier operational cutoff; no count run is needed; the spec and replay correction is authorized as a bounded change, verified before freeze. **Still required:** acceptance of the corrections |
| **Same-session resumption** | §A11 item 1: one attended session, then explicit review before extension. §A11 item 4: resumption needs a new operator resume after reconciliation, per rev9 §4, which **permits** conditional same-session resumption. The Phase 5 plan's stricter rule is PROPOSED only | Recommended: after any commissioning or first-release incident, no same-session restart of automation, then review | **RULED 2026-09-27** ([incident ADR §A11.2](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a112--operator-ruling-no-same-session-restart-of-automation-after-an-incident-2026-09-27)): for commissioning and the first attended release, an incident ends automated trading for that session; review before another. Owner text via H5 (a) |
| **Read target** (T07 R1–R3; REST R-1/R-2) | T07 reads authorized 2026-09-25 against the D1 transaction. R-1/R-2 authorized 2026-09-26 once entitlement is confirmed. The known-order definition is OPEN | Use an operator-placed preservation trade where it meets the read's evidence requirements: a completed one for R-2 and the T07 reads; for R-1, only in the same session as a preservation trade the operator places anyway | **RULED 2026-09-27** ([incident ADR §A11.3](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a113--operator-ruling-preservation-trade-evidence-as-the-target-of-authorized-reads-2026-09-27)): reuse is approved where scope and timing qualify; no additional trade. **Still required (CP-2):** the entitlement record and confirmation of each transaction identity |
| **Order-producing commissioning rows** | None authorized. Each is prepared individually (§A11.1 item 5) | None | **CP-3**, in writing, **before each** row |
| **Result/seal integration** | T05's frozen head integrates after S5 acceptance | Integration *preparation* may start once S5 C3 is accepted. Integration **acceptance** still follows full S5 acceptance. Recovery (D3) has its own checkpoint | None new; the coordinator keeps combined acceptance |

### 1. Circular prerequisites corrected

**1.1 S5 measured an adapter it had not built yet (RC-3).** The S5 draft's RC-3 asked for a *measured* PART_A envelope "of the TEST_ONLY workload S5 will run" before the hold is released, and `/v7` does not exist before the build. The #519 proposal already finds three further facts:
- the TEST_ONLY fixture (2, 4, 2) can never expand;
- maximum expansion therefore needs a forced-expansion harness on the existing engine;
- the N2 derivation and the real artifacts (D̂) are uncovered until C3.

**Correction** (owner: the [execution-slices ledger](2026-09-18-full-e1-execution-slices.md#operator-direction--s5-build-entry-separated-from-checkpoint-c3-acceptance-2026-09-27)):
- **Build entry** consumes a valid forced-expansion record of the existing `_run_part_a` on the reference runtime (#519 Stage 1b). The rule is applied to it as a **provisional** ceiling. Σ-feasibility is **proposed-value arithmetic** (#519 proposal §5).
- **Checkpoint C3** consumes the adapter measurement (Stage 1c), the executed `bind_budget` check on the built `/v7`, and Stage 2/PA-5.

The circular condition is removed, not renamed. Nothing at build entry requires the adapter, `/v7` or a service-route run. The precedent: S4's N2 ceiling was set at Checkpoint C2 from a measurement taken during the build.

**1.2 The ORB freeze loop.** Freezing the edition pre-registration needs the edition files. Their production waits on gate D (G2b). Gate D needs a bounded T09 handoff, and T09 is held until "the edition rules …, including the ORB resting-entry lifecycle (B-13), are frozen or explicitly held" ([B–D packet §5](../../notes/2026-09-26-tradeify-bd-decision-packet.md)). Two moves break the loop:
- **(a) Lifecycle evidence already exists** from pre-freeze sources: the declared ORB and its accepted replay, with no edition replay (#519 lifecycle note). The operator's B-13 ruling makes the lifecycle frozen for gate D's purposes.
- **(b) The fence repair splits:**
  - The **state-classification contract** (#519 trace §6.1–§6.2) is decided at CP-4. It becomes a synthetic implementation (H4) that can land before the freeze inventory is fixed.
  - The **evidence producer and route integration** stay in T09, so gate D's T09 handoff names them as the remaining fence obligation.

  §A11 is not the basis for (b): it fixes preserve-and-block as the *response* to an unresolved request, not the classification of an acknowledged, freshly evidenced working order.

**1.3 The settlement reads wait on an order-producing drill.** T07 reads R1–R3 read the D1 transaction ([session plan §0 addendum](../../notes/2026-09-25-t08-drills-t07-reads-operator-session.md)), and D1 is not cleared for execution (§A11.1 item 6). **Correction, ruled 2026-09-27 ([incident ADR §A11.3](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a113--operator-ruling-preservation-trade-evidence-as-the-target-of-authorized-reads-2026-09-27)); the entitlement record and transaction identity are still confirmed at CP-2:**
- where a preservation trade meets a read's evidence requirements, the reads target that trade;
- a **completed** trade can serve R-2 (prior-session lookup) and the T07 report reads;
- **R-1** (same-session) needs a same-session known order, so it runs only in the session in which the operator places a preservation trade anyway. One old trade cannot supply a new same-session observation.

This adds no exposure beyond the trade the account already requires; that trade itself is not exposure-free. The correction does not settle drill-plan open question 9 (how preservation trades on the book's own symbols are treated in operation).

**1.4 Stated, not circular.**
- **Feed.** D-feed condition (b) needs the F1 packet, and the F1 packet must bind the feed. The packet therefore carries the provider-neutral feed contract and an explicit **later-binding rule** for the funded provider. That rule is accepted with the packet (T15 already requires explicit accepted later-binding rules).
- **Attended operations.** Rev9 permits conditional same-session resumption with operator approval ([halt/resume §4](../../spec/2026-09-14-tb-s3-halt-resume-contract.md)). The Phase 5 plan proposes stricter text. The operator ruled on 2026-09-27 (§A11.2): no same-session restart of automation after an incident during commissioning and the first attended release. H5 step (a) applies it to the halt/resume owner text before T13 implementation.

### 2. Evidence classes and what each may support

| Class | Produced by | May support | Does not constitute |
|---|---|---|---|
| **Commissioning observation** | Operator-run route commissioning sessions, attended-operations rehearsals, settlement collection | After review, **capability acceptance for its demonstrated scope**: CAP rows and T08 §7 against the drill map's behavior rows (REST §6.11), on the interface and in the environment observed | Production E1/n3 results, portfolio admission, or whole-route acceptance |
| **Synthetic / replay engineering** | TEST_ONLY campaigns, `SyntheticBroker` consumer tests, replay | Engineering acceptance of classification, consumer behavior and qualification machinery | Actual broker, feed or settlement evidence (common verification rule above), or a complete obligation that needs a real producer |
| **Production qualification** | The single authorized production E1 and the sole final n3 under the protected service | Admission (D0/D1) and the launch decision | — |

Commissioning records carry the label `COMMISSIONING_OBSERVATION` and state their scope (behavior, interface, environment, date).

### 3. Staged acceptance by workstream

Each requirement is classified as:
- **[1]** required before the next bounded action;
- **[2]** evidence that action collects;
- **[3]** required before expanding authority or exposure.

Handoff IDs refer to the [handoff set](../../briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md). A class-[3] item never blocks a class-[1] step it does not affect.

| Workstream (owners) | Next bounded action | [1] Before that action | [2] Collected by it | [3] Before expanding authority or exposure |
|---|---|---|---|---|
| **Broker route** (drill plan; T08; CAP R2–R5; incident ADR §A11.1) | **H2**: prepare one operator-run commissioning session packet, automation disarmed. Stage 0 is read-only. Stage 1 lists normal-case order rows, each individually specified | For the packet: Gate A accepted (in place); the drill plan, §A11.1 and the #519 close-semantics return as inputs. **Before stage 0:** entitlement confirmation, known-order confirmation (§1.3), actor inventory (§0.1, including the timed exit and firm-side auto-liquidation candidates from #519), host disarm confirmation. **Before each stage-1 row:** CP-3 written authorization for that row; its documentary prerequisites (for X-3, the residual-risk decision per CR-3, since #519 left M OPEN/CONFLICTING); P-1; the environment decision, with no automatic fallback to the live eval | Actual entry-with-stop, stop `Working` quantity, cancel of a resting entry with its children, rejected-change behavior, liquidation normal case, fresh reads for reconciliation. Also any `unknown` outcome and its read-first recovery | Review of each row's traces before the next row, a second session, a multi-contract design or X-5; capability acceptance of the observed scope; gates B–D (CP-5) before T09 |
| **ORB lifecycle and fence** (§59 Rulings 3/5; B–D packet B-13 and fence row; #519 lifecycle and trace notes) | **H3**: disposition #519's two returns and apply the 2026-09-27 rulings (§59 Ruling 7) to the specification owners. Then **H4**: the bounded synthetic repair plus the replay correction | For H3: #519's returns at `8c15f18`, and Ruling 7 (both in place). **For H4:** H3's owner text and the H4 dispatch card (coordinator acceptance) | H3: the coordinator disposition, operator decision questions, and proposed rail-spec owner text. H4: synthetic verification of classification and consumer behavior (trace §6.4 cases), kept separate from the owed items: the real evidence producer and route integration | The real producer and route integration (T09) before the fence obligation counts as resolved. Any lifecycle change enters the edition pre-registration and requalification before freeze (§5). A replay change (L1) is an E1 freeze-inventory change |
| **S5 and resource limits** (execution-slices ledger; S5 draft §5; #519 measurement proposal) | **H1**: correct #519's proposal and return a concrete measurement dispatch for approval. Then execute it within the approval | For H1: nothing further (ruling §6 preparation authority). **For executing the measurements:** CP-1a. *[2026-09-28: CP-1a is ruled; execution also needed the harness merged, its evidence on the archive's `main` and a post-merge `audit --verify` ([r2 "Current authority"](../../notes/2026-09-27-s5-part-a-measurement-proposal-r2.md)). All hold since [#534](https://github.com/Joshua-Asante/first-passage/pull/534) merged.]* **For the build:** RC-1 (met); the §3.4(d) text applied; RC-4/RC-5 assigned; RC-6 re-anchor, including #519's non-expansion finding and the `/v7` pitfalls; RC-3a; CP-1b | H1: the corrected proposal and the dispatch. Execution: valid Stage 1b records (Stage 0 calibration if approved). Build: the Stage 1c adapter record and the executed binding check at C3 | **S5 acceptance:** C3 items; RC-3b; the full RC-2 owner text. **Before F1:** the RC-4 seed-view change and its admission check, the OF-7 attestation (G-F1), and K3. *[Corrected 2026-09-27: this row said "OF attestations". Only OF-7 falls due before F1 admission; the full OF-1..OF-7 set is read at CP-8, per the ledger's RC-5 entry and the host row below.]* Production budgets remain separately governed |
| **Result/seal and recovery** (T05 frozen head `6cf2732`; S5 draft §3) | **H9**: integration *preparation* once S5 C3 is accepted *(2026-10-01: **READY**, since C3 is accepted. The preparation work itself is not yet returned and must be returned before R1)* | S5 C3 accepted (field sets, `/v8` snapshot, capture contract) | A prepared integration branch and its interface diff | **Integration acceptance** after full S5 acceptance (checkpoint R1). *2026-10-01:* R1 also requires **both D-S5 fix slices merged, each with its own full S4-plus-Part-A Linux run read ok and its own acceptance: #586 (D-S5-1/D-S5-2; merged `981eb12`), then the D-S5-3 slice, #589 (from `claude/capture-retry-noop`)**, and the integration branch rebuilt on a `main` that includes it ([defects ruling](2026-09-18-full-e1-execution-slices.md#operator-ruling--land-s5-with-two-named-test_only-defects-fix-before-t05-2026-10-01) · [D-S5-3 ruling](2026-09-18-full-e1-execution-slices.md#operator-ruling--d-s5-3-capture-exact-retry-demotion-also-gates-t05-r1-2026-10-01)). **Recovery-slice acceptance** after the D3 owner text is accepted (checkpoint R2). Coordinator combined acceptance before T06/S8 |
| **Production qualification host** (T11; OF-1..OF-7; contract-delta K3/K6/K8) | **H7**: assign RC-4/RC-5 now (resolving S5 draft §6 Q12), and write the host and credential specification | None beyond the 2026-09-26 direction to assign the attestations to their gates | An owner, gate and record location for each OF; the RC-4 owner and slice; a host bill of materials; a cost line if provisioning needs spend | Provisioning, including any spend, at CP-8. OF-1..OF-7 attested by attended reads, key custody recorded, K3 salt custody and installed identities verified before any production attempt is admitted |
| **Settlement evidence** (T07; CAP S1–S5) | **H6**: bounded operator collection of report originals for the confirmed target, then a reconstruction rehearsal | CP-2 confirmation of the target (§1.3); the S2 source-fact questions listed in collection order | Actual report coverage, `Timestamp` offset, `Date` meaning after rollover, query-bound semantics; missing-data detection; the restoration and correction-refusal trace; the procedure's time | The S3/B7 predecessor choice (no silent reset); the operator-facing sign/submit entry point before a live close chain; T07 acceptance before T16 |
| **Attended operations** (Phase 5 plan; halt/resume contract; T13) | **H5**: (a) apply §A11.2 to the halt/resume owner text (accepted 2026-09-27); (b) rehearse incident-versus-refusal behavior, fencing, intervention and restart with synthetic incidents | For (b): the (a) amendment accepted | Owner-level incident-versus-refusal behavior; restart without stale authority; no same-session restart after an incident (including a deliberate operator stop). Real delivery and 60 s escalation are T13's, unless the operator runs that leg at dispatch | Commissioning traces folded in; the attended recovery procedure for an unresolved request before any session that could produce one; T13 acceptance before T16 |
| **Feed** (O-4; D-feed; T10/T14) | **H8**: provider-neutral preparation only | Standing permission (STATE source disposition) | Symbol, roll and session mapping; equivalence protocol (TB-I5 successor spec); gap, reconnect and correction handling; the later-binding rule text | The funding decision (CP-7) after T00 is non-INSUFFICIENT and T10 phase 2 is assembled. *(Step-1 resolution, P7 MET at `2baa516`, does **not** satisfy this. D-feed (a) needs the step-3 screen's verdict outside {INSUFFICIENT, NO-GO-evidence}, which in practice means GO-evidence after step 2 is ratified.)* After funding: shadow collection with emission disabled; actual equivalence, gap, reconnect and correction evidence before trading use |
| **Final launch** (T12, T15–T17; Phase 6 plan; §A11 item 1) | **H10**: rehearse the exact candidate, then authorize one attended session | T16 accepted candidate; T12 timing envelope | The timed rehearsal on the final candidate; fresh B7; the sole n3 | Qualification and admission (D0/D1), current account evidence, final n3, deployment GO and session authority (CP-9); explicit review of that session before any extension |

### 4. Operator checkpoints — where approval is taken

Each checkpoint takes the decision once, against a returned artifact. Between checkpoints the coordinator acts within the approvals already given, without re-asking. Agents may place orders, exit positions and cancel orders only at the operator's direction for the specific act; `trade.submit` is an operator act at risk `high`, never grantable in a card. Arming, live-spend and per-session GO requirements are unchanged. No merge happens without the operator, and nothing is armed without M1 plus a session GO. Owner: [surface-allocation ADR Addendum 2026-09-30b](../../adr/2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-09-30b).

| CP | Decision | Reviewed against | Unlocks |
|---|---|---|---|
| CP-1a | **RULED 2026-09-27: all six decisions adopted as recommended** ([ledger](2026-09-18-full-e1-execution-slices.md#operator-ruling--cp-1a-decisions-16-adopted-as-recommended-hold-kept-2026-09-27)). RC-4 slice sequencing: K3/RC-4 is dispatched after S5 acceptance and lands before S8/T06. The next step is H1 step (b), executing the approved measurements. *As presented:* **Already decided, not asked again** (r2 §14.1): the staged structure and PART_A TEST_ONLY scope (ruled 2026-09-27); arithmetic as pre-build feasibility; the numeric defaults, **conditionally approved 2026-09-26**; N2 not under the rule; the RC-4/RC-5 assignment; S4 evidence preserved. **Six decisions, presented together, each with a recommendation and what it unlocks:**<br>– (1) the measurement parameters: confirm the 2026-09-26 applicability conditions are met, and decide what that approval left out (pilot-budget term and PA-2b, PA-3a/PA-3b, re-run caps, re-measurement triggers);<br>– (2) the bounded dispatch and runtime (Stage 0 optional and separable, with coverage of the preserved logs verified locally, owed; Stage 1a/1b; Stage 1c at C3; Stage 2; host venv or worker image);<br>– (3) the separate `/v7` N2 ruling;<br>– (4) D2 timing;<br>– (5) the RC-4 slice;<br>– (6) the Stage 1c seam and its signed-route exclusion.<br>Sequence: CP-1a → approved measurements → RC-3a evidence and updated build-entry table → CP-1b → S5 build; the adapter measurement and executed binding check stay at C3. Accepting the packet is not approval to execute it. *[Superseded 2026-09-27 (Codex review of db608632): that held before the ruling. CP-1a decision (2) now approves the bounded measurements. Their execution is sequenced by r2 §12.9: it waits until the revised H1(b) harness PR is returned with retained evidence and merged, the evidence is archived on `first-passage-archive`'s `main`, and the post-merge audit is recorded on the H1 row ([r2 "Current authority"](../../notes/2026-09-27-s5-part-a-measurement-proposal-r2.md)). S5 stays HELD. See r2 "Current authority".]* *Revised 2026-09-27 after #519's merged corrections (r2 §16).* | [H1 r2 CP-1a packet](../../notes/2026-09-27-s5-part-a-measurement-proposal-r2.md) §14.1, reconciled in §16 | The coordinator executes the approved measurements and applies the rule to TEST_ONLY ceilings with recorded evidence |
| CP-1b | Release the S5 hold for the **build**. *[**RULED 2026-09-28:** released for the TEST_ONLY build at release head `05f3788` ([ledger](2026-09-18-full-e1-execution-slices.md#operator-ruling--cp-1b-s5-hold-released-for-the-test_only-build-2026-09-28)). RC-2, RC-3b and the C3 obligations stay open.]* | RC status table with RC-3a met | S5 build dispatch; C3 applies RC-3b within the approved rule |
| CP-2 | Supply or confirm the route facts: entitlement, known-order definition, read target (§1.3), sim/demo availability, actor inventory, whether drill costs count against the $700 ceiling | H2 stage-0 section | Operator-performed R-1/R-2 and the H6 collection |
| CP-3 | Authorize **each** order-producing commissioning row, in writing, with environment and exposure limits, before that row | H2 stage-1 row, after the prior row's traces | That row only; its traces return before the next |
| CP-4 | Rule B-13 (the ORB lifecycle); accept the state-classification contract. **RULED 2026-09-27** (§59 Ruling 7): L1, and the fresh-evidence contract | #519 returns | H3 applies the owner text; H4 (synthetic repair plus replay correction); the ORB side of edition preparation |
| CP-5 | Accept gates B–D using commissioning traces, H3/H4 and the allocation map | Gate record above | Bounded T09 dispatch (including the fence's producer and route integration); edition file production (G2b) |
| CP-6 | Freeze / F1: feed later-binding rule, RC-4 change landed, K3, complete behavior inventory. *2026-10-01:* also **S5 open question Q9** (when a never-retried, retry-eligible IN_DOUBT counts as closed, and so the salt reveal), decided in the RC-4 slice ([C3 ruling](2026-09-18-full-e1-execution-slices.md#operator-ruling--c3-accepted-s5-accepted-for-test_only-on-landing-2026-10-01)). **Carried residual (operator, 2026-09-29, S5 C3 step 1):** G5 independent bars verification, i.e. the calendar ↔ population-index ↔ bars consistency that PART_A's G5 does not re-verify ([ledger](2026-09-18-full-e1-execution-slices.md)). **Carried (operator, 2026-09-30, S5 C3 memory stop):** a per-phase Part A memory field (the payload unit's own `memory.peak`); for TEST_ONLY, PA-5 is CPU-only and PA-3b uses the slice-wide `memory_peak_bytes` as an upper bound ([ledger](2026-09-18-full-e1-execution-slices.md)) | T10 phase-2 packet; §5 check | Reservation of the production attempt (distinct dependent approvals retained) |
| CP-7 | Feed funding (O-4) | D-feed conditions; H8 packet | Provider-specific adapter and shadow collection |
| CP-8 | Production host provisioning (and any spend); admit the production attempt after OF attestation. **Carried (operator, 2026-09-30, S5 C3 memory stop), for T11 host sizing:** the TEST_ONLY qualification slice's unreclaimable headroom is 11.8 % (a 225.7 MB anon + kernel peak against 256,000,000 B), with the THP share (up to 48 MB `anon_thp`, `enabled=[always]`) to be separated ([ledger](2026-09-18-full-e1-execution-slices.md)). **Carried (operator, 2026-10-01, S5 Stage 2 / PA-5), for T11 host sizing:** (i) PA-5 k = 4.078929 (whole settled charge, run `36766144433`) against the Stage 1c prescribed maximum, with the TEST_ONLY PART_A CPU headroom of 13.142 s (10.95 % of 120 s) after re-application; (ii) the host difference: the service ran on an EPYC 9V74 and the Stage 1c maximum on an EPYC 7763, which Stage 1b measured 1.534× slower. Normalized to the 7763, the PART_A CPU ceiling would be 130 s (compute only) to 160 s (whole charge scaled), not 120 s, so a slower runner could hit the 120 s cap; (iii) PA-3b memory headroom, unshowable from the clipped slice-wide `memory_peak_bytes` ([ledger](2026-09-18-full-e1-execution-slices.md), [`stage2.json`](../../notes/2026-09-27-s5-part-a-measurement/stage2.json)) | H7 plus the attested reads | Production E1 once (T15) |
| CP-9 | Deployment GO and authority for one attended session | T16 candidate; H10 rehearsal; fresh B7/n3 | One attended session; explicit review before extension (§A11 item 1) |

### 5. Behavior-changing findings settle before the final freeze

A commissioning, settlement, feed or rehearsal finding that would change intended behavior goes to its owner decision **before CP-6**, and no later. Examples: lifecycle, expression, exit, fence classification, recovery, cutoff or takeover. The owner decisions are gate B, B-13, the classification contract, the edition pre-registration and the incident contract. The result is one of:
- a pre-registered change with its requalification (K=1 per §59); or
- an explicit accepted later-binding rule; or
- a hold that blocks freeze.

A finding recorded after CP-6 that changes behavior voids the freeze inventory for the affected component; it is not absorbed as a binding. Findings that do not change behavior (latency, report timing, operator workload) are recorded against their behavior rows and inform limits only.

## Addendum 2026-09-28 — current sequence after the route-commissioning documentary closeout

**What this addendum is.** A **derived mirror** (Rule 7) of the current sequence. Its owners are the 2026-09-27 addendum's §3 rows, the handoff set's status table and the linked packets, and they govern wherever this table differs. It is a refresh of the **current sequence only**, written by the bounded Claude Code coordinator session commissioned by the [2026-09-28 delegation](2026-09-28-tradeify-next-step-delegation.md), read at `main@180aa74`. It **changes no packet's selected outcome, gate, evidence class, statistical criterion, authority or checkpoint**, and it adds no checkpoint. Where it and the 2026-09-27 addendum meet, the 2026-09-27 addendum governs; §0's gate table, §3's workstream rows and §4's CP-1a..CP-9 are untouched. It authorizes nothing: no merge, dispatch, drill, read, trade, spend, freeze, arm or GO. The deployment coordinator retains combined acceptance and the operator retains every named operational decision.

**Ownership note** (refreshed 2026-09-28 03:48 UTC). [#536](https://github.com/Joshua-Asante/first-passage/pull/536) (r2 procedure/status/evidence corrections) **merged** at `48c178a`. Open against main, each keeping its owner:
- [#537](https://github.com/Joshua-Asante/first-passage/pull/537) (`fadfc29`): H1(b) evidence and the CP-1b packet.
- [#538](https://github.com/Joshua-Asante/first-passage/pull/538) (`40b84da`): S4 run-logs retention. Its diff records operator adoption and executed work, not the proposal its body describes.
- [#539](https://github.com/Joshua-Asante/first-passage/pull/539) (`a8d7451`): the r2 §12.3 Stage 1b dispatch block, split out of #536.

This addendum consumes their returns by reference and redispatches none of them. #536's edit to the 2026-09-27 addendum (§3 "S5 and resource limits") is merged, and #537 edits §0 "Measurement execution"; this addendum touches neither line.

### Current sequence by workstream

| Workstream | The next step, as of 2026-09-28 | Immediately before it | Do not do |
|---|---|---|---|
| **Qualification** | Consume #537's H1(b) return (READY_FOR_CP-1b; measured `main@7675c08`; its H1 evidence package pushed in archive #844 at `54923331`, final check hash `38c4db66` present in that archive branch). Before the **CP-1b** decision: #537's review and merge, archive #844 merged into the archive's `main`, and the post-merge audit recorded on the H1 row. Per #537, the H1 evidence counts as ARCHIVED only once archive #844 merges, with the post-merge audit owed then. Holding both, with #537's merge, before CP-1b follows the executive review of #540 (2026-09-28). Then take CP-1b from its own ruling. **S4 run-log retention** (#538; archive #845 at `88b2458`) is **separate work**: Stage 0 is optional calibration that supplies no ceiling (r2 §16.4), and no ruling makes it a CP-1b prerequisite. *(Corrected 2026-09-28 after the executive review of #540: an earlier version of this row placed #538's retention before CP-1b.)* | The merges are the operator's; the H1 post-merge audit is owed on the H1 row | Repeat any measurement. Make #538/#845 a CP-1b prerequisite without an explicit ruling. Infer CP-1b from any card, including this one. Treat the earlier review comments on #537 as current — they may address an older head |
| **S5 → T05 → S8** | After CP-1b: the S5 build, then C3 (RC-3b: the Stage 1c adapter record, the executed `bind_budget` check on the built `/v7`, Stage 2 / PA-5). **T05 integration preparation** may start once C3 is accepted; integration **acceptance** still waits on full S5 acceptance. **S8 / T06** follows T05 integration at one identity | CP-1b for the build; C3 for the preparation | Start the build before CP-1b. Accept integration before full S5 acceptance. Start S8 before T05 integrates |
| **External route** | **CP-2 recorded 2026-09-28** ([packet §1.1](../../notes/2026-09-27-route-commissioning-session-packet.md#11-cp-2-record-2026-09-28)): entitlement confirmed, no equivalent sandbox, evenings permitted, and the six rulings adopted. Next: **Stage 0** in the session of this week's preservation trade (due by 2026-10-02): host disarm read, actor inventory, then R-1 on that trade; R-2 after a reset. **F-6(a):** Tradeify answered 2026-09-28 with conditional permission; X-1's CP-3 carries the operator's attestation of its conditions, and the operator ruled (2026-09-28) that portfolios adapted to each firm's rules count as distinct strategies for its exclusive-use condition. *(Later 2026-09-28: the attended-session checklist is [packet §1.2](../../notes/2026-09-27-route-commissioning-session-packet.md#12-next-attended-session-checklist-2026-09-28). CP-2 is not complete: each read's target binding is missing; the entitlement capture and the venue reply are owed but gate nothing. Before X-1, the A-11 decision (§7) is also open.)* | The P-1-entitlement capture is owed but is not a gate (drill plan line 40) | Authorize more than one row at a time. Place an additional trade. Send any request before CP-3 for that row |
| **B–D closeout** | The [B–D packet §7 addendum](../../notes/2026-09-26-tradeify-bd-decision-packet.md) reconciles the residual conditions, records the allocation delta and states why **T09 is not specifiable**. Gates B–D are accepted at **CP-5**, reviewed against commissioning traces that do not exist yet | X-1's trace is the cheapest evidence that bears on the largest part of the T09 interface table | Write a T09 card. Label T09 dispatchable. Reopen a ruled choice because an older table says OPEN |
| **M2 (X-2's precondition)** | *(Later 2026-09-28: **returned**, [#541](https://github.com/Joshua-Asante/first-passage/pull/541), Q1–Q4 `OPEN`; the coordinator's review of the return is owed. Next, and the operator's: whether to send the note §5 vendor question, and the GC-2b decision for Striker and Aegis (card §8).)* The operator starts the **carded, DISPATCH-READY** [M2](../../briefs/handoffs/2026-09-27-m2-modify-semantics.md) in a local session of the primary checkout, on a frozen revision descending from #532's merge `6da1b2b` (card §0.5, §9). If its return leaves Q1 OPEN or CONFLICTING, the operator decides whether to send its draft vendor question and whether that uses the one permitted T08 follow-up | #532 merged. The public pages give no answer ([§3.7 closure C.6](../../notes/2026-09-27-route-commissioning-session-packet.md#c6-m2-x-2s-documentary-precondition-the-exact-remaining-dependency)), so the retained captures decide | Re-card or edit M2 (its premise check pins the card text). Run it outside the primary checkout |
| **Fence and ORB** | H3 and **H4** are accepted (H4 synthetic scope, #522 at `9e18d85`). Next: the ORB L1 amendments (ORB-1, RC-9, rail S2, the qualification replay) return for acceptance before edition freeze | §59 Ruling 7, in place | Treat a synthetic H4 return as resolving the fence. Its **real producer and route integration stay T09's** |
| **Attended operations** | H5(a) is accepted and H5(b) is accepted PARTIAL (#521). Remaining: CC-3 (the ordinary-unknown halt) and the durable resume owner, toward T13; reconcile the commissioning packet's §0 reading with the accepted halt/resume §4 text | H5(a) and H5(b) accepted | Build option B or automatic recovery. Design a same-session restart |
| **Settlement** | H6's bounded operator collection, once a qualifying **completed** T07 target is confirmed (CP-2 ruling 2026-09-28: post-rollover timing, zone-explicit timestamp; this week's preservation trade is reused if it qualifies) | Target confirmation (packet §2.4) | Read before the target's transaction identity is confirmed |
| **Feed** | Provider-neutral preparation has **returned** ([note](../../notes/2026-09-27-feed-provider-neutral-preparation.md)); carry its actual residuals into the F1 packet's later-binding rule. Funding is **CP-7**, after T00 is non-INSUFFICIENT and T10 phase 2 is assembled *(Step-1 resolution, P7 MET at `2baa516`, does **not** satisfy this. D-feed (a) needs the step-3 screen's verdict outside {INSUFFICIENT, NO-GO-evidence}, which in practice means GO-evidence after step 2 is ratified.)* | — | Open another preparation assignment. Select or contact a provider |
| **Separate bounded work** | **H8(c)** keeps its existing test card, and **CC-3** (the ordinary-unknown halt) and the real evidence producer stay owed with their existing owners | — | Write a new omission study. Fold either into this sequence |

**What this sequence rests on, restated so it is not assumed away.** No commissioning row has run, so there is **no actual-route observation** of any kind. Gate A is accepted with changes; gates B, C and D are pending. S5 is **HELD**. TradingView has no live role. Preserve-and-block for one attended session is the posture, with no same-session restart of automation after an incident. Statistical qualification and the sole final n3 are not waived by any step above.

## Addendum 2026-10-01 — continuation after X-1

Dated and additive. The 2026-09-28 continuation above is unchanged as the record of its date. **Its "next step" (Stage 0 / R-1 on the week's preservation trade) and its "no commissioning row has run" statement are superseded:**

- **X-1 executed on 2026-09-30** (T0 23:42:32Z, in the operator-amended 23:30–00:00Z window). A **scoped GC-2a PASS, evidence accepted with limits**, with no release ratification. Codex's X-1 acceptance is [PR #572](https://github.com/Joshua-Asante/first-passage/pull/572); the record and its limits are in the [X-1 decision packet §8](../../notes/2026-09-29-x1-decision-packet.md#8-post-execution-record-and-corrections--2026-09-30).
- *Mirror; the owner is the [X-1 packet §8 R-1 tooling ruling](../../notes/2026-09-29-x1-decision-packet.md#8-post-execution-record-and-corrections--2026-09-30), which defines options A, B and C and the fallback:* ~~**R-1 on X-1's order is owed.**~~ *(Historical: discharged 2026-10-01; see the update at the end of this bullet.)* The same-session window closes **2026-10-01 at ~17:00 ET**, the next reset (drill plan R-1 table, precondition 3). **Option A is selected** (operator, 2026-10-01): the builder is dispatched to build a reviewed R-1 v3.2 collector with the `clOrdId` step, for build and offline testing only. The read is Joshua's, after local-Codex acceptance only. **Start-by rule: start by 16:30 ET or C; started reads run to the ~17:00 gate.** If the read has not started by 16:30 ET, for any reason, C applies: R-1 is rehomed under the R-1 table, and nothing runs ([§8 start-by rule](../../notes/2026-09-29-x1-decision-packet.md#8-post-execution-record-and-corrections--2026-09-30)). **Update 2026-10-01 08:59Z: R-1 DISCHARGED** for X-1's order (`LOCATED_WITH_CLORDID`; operator-run, option A, before 16:30 ET; the start-by rule is spent and C did not apply). Mirror of the [drill plan's R-1 result](../../notes/2026-09-26-tradeify-route-drill-plan-draft.md#r-1-result-on-x-1s-order--2026-10-01).
- **The attended-input adapter** is retrospectively accepted for X-1 run-1930 only, **qualified**. Its pin/path-safety review and the reconstruction of the resolved import set are owed. **Future use stays barred** until both are accepted.
- **Still owed after X-1:** the drill plan's "X-1 acceptance" addendum (#572), and the governance sweep for the 2026-09-30 AGENTS.md amendment. The next order-producing row needs its own CP-3.

## Addendum 2026-10-01 — first-session simplification rulings (six cuts)

**Source.** Joshua, in the coordinating session on 2026-10-01: "go with all six recommended cuts". He was replying to the coordinator's disposition of current work toward the first attended Tradeify eval deployment, which keeps all four strategies and full portfolio behavior.

**What these rulings do.** They scope, defer or cancel work. They do **not** change accepted contracts, stop running tasks or weaken any guarantee. Each still needs its owner's text where noted. Retained everywhere:
- confirmed broker feedback to all four ports;
- reservation-plus-halt for an unknown request;
- settlement of every session;
- the baked activation gates;
- M1.

1. **Route amendment: first-release scope only.** Option B's resume machinery is **out of scope** of the bounded-exposure unknown-request amendment for the first release: rules 4′, 4a–4c, 9′ and 12, the §A3 figures, and UB-2, UB-6, UB-9 and UB-10 ([incident ADR addendum](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md)). Those wait for a later release.
   - The first-release text is narrow. An unknown request means its reservation is held and trading halts, and the only release is a uniquely correlated outcome (T08 §7.10, PR #575). The §A2 rule-7 non-entry rule is included.
   - T09 is specified against the unamended E3. The halt/resume §3–§4 and E3 diffs are not required for the first release.
   - Both step-4 reviews stay, applied to the narrow text.
   - The §A1 trace, UB-7 evidence, the close contract and X-2/X-4 stay.
   - Owed: the route/incident coordinator writes the narrow text. The operator merges #575, then accepts the text, then gate B.
2. **Feed: no-spend steps move earlier.**
   - Written provider questions Q1–Q12 and reads of published terms are **allowed now**, with no account, signup, credential or spend ([feed note](../../notes/2026-09-27-feed-provider-neutral-preparation.md)). Agents may draft the questions. Sending any message stays the operator's act.
   - The feed-equivalence spec may be **frozen now**, before any provider data.
   - Signup and spend stay behind D-feed (a)+(b) and CP-7.
   - *Operator ruling, 2026-10-01 (D-Q1):* **feed costs only** (subscription and CME licence fees) **do not count toward the $700 ceiling**. Refundable deposits and minimum balances stay under the cap until the operator rules on them separately ([rail GO ADR addendum](../../adr/2026-07-17-c1-rail-build-account-registration-go.md)). *Defined 2026-10-01 (D-Q6/D-Q7):* any non-refundable charge whose purpose is receiving the market data is a feed cost and is exempt; that covers required API or data-access fees and one-time setup charges.
3. **X-4: reduced build path.** GC-4's required observation is unchanged:
   1. one resting MNQ buy-stop bracket is placed;
   2. the parent shows `Working` with both children `Suspended`;
   3. the parent alone is cancelled;
   4. all three end terminal, with no fill, the account flat and nothing working.

   The build is **small reviewed extensions to X-1's accepted round-7 generator and sender** (stop entry type, two children, a parent cancel bound to the parent's account path), with **R-1 v3.2** for the terminal reads and the coordinator classifying from the sealed bytes. **A bounded pre-cancel status reader is kept.** This is a reviewed, GET-only extension of R-1 v3.2, or an equivalent reviewed reader. It captures and seals the parent as `Working` and both children as `Suspended` **before** the cancel, because terminal reads cannot reconstruct that intermediate state. Without that sealed pre-cancel read, the drill does not establish GC-4.
   - **Cut from the drafted suite** (#572's X-4 handoff): `x4_profile`, the observer's read budget and rate machinery, the asynchronous late-response channel, `x4_attended_input`, `x4_adjudicate`, and the multi-pass reviews. One focused review replaces those reviews.
   - **Kept:**
     - a one-use placement claim and a one-use cancel claim, each surviving a restart, including an unknown placement (MUST-PASS, because `order_id` idempotency is disproven);
     - raw response bytes sealed before parsing;
     - validation of both child identities;
     - attended cancel of every live order if the account is flat.
   - This supersedes the drafted suite where they differ. #572's six recorded C1 items apply only where they bind the kept items.
4. **#571: parked, whole.** It changes only the legacy c1-rail `EventLedger` path. The book route uses CC-3's durable halt and never reaches it.
   - **Guard while parked:**
     - `dry_run=true` stays;
     - **no `c1_rail_arm` of any legacy leg**, including the M1 Stage-1 test leg;
     - #571 is retained and deployed before any legacy re-arm or M1 Stage-1 ceremony.
   - The M1 limitation is recorded in the [M1 ADR addendum of 2026-10-01](../../adr/2026-07-22-c1-venue-native-monitoring-maturity.md).
5. **Secondary simplifications.**
   - **D-GO:** the signed-GO evaluation is closed, and the baked GO stays. Reopen it only if T12 timing shows the reseal does not fit B7.
   - **D-HIST, the successor venue and the M-B idle-clock monitor:** deferred until a successor attempt is authorized.
   - **T13:** the later-session activation machinery and backup-restore rehearsals are deferred. T13's T16 acceptance covers the first session only, which is the initial activation. Kept: disarmed fail-closed restart, no restart within a session, and the durable unknown-request block.
   - **Automatic feed repair:** simplified to *a gap is an incident and halts the session*. Warm-up, delivered-data equivalence and gap detection stay.
   - **D-MON:** simplified. The existing channels are checked against the halt/resume contract. Any gap is filled by a no-cost external provider, not an in-house build. **The channel choice is still the operator's.** The alternate-channel escalation stays.
6. **T00 step 2: reuse the existing pre-registration's scoring clauses.**
   - The step-2 pre-registration reuses [`2026-08-26-prop-survivor-scoring-prereg-v2.md`](../../briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md) by citing **its reusable scoring clauses only**. It does **not** import that preregistration's falsifier disposition (G8). **A T00 screen is not four-firm §4 falsifier evidence** (operator ruling 2026-09-23, condition 4). The step-2 contract states that non-falsifier disposition itself. It adds only the expressions, pass floor, scenarios, intraday clock, NO-GO condition and the counting of R1/R2 `UNDETERMINED` days.
   - It may be drafted now, in parallel with the S5 landing. Ratification stays the operator's act.
   - **Still open:** how D-feed (a) treats a NO-GO T00 result whose risk the operator accepts into F1. This decision is still required.

7. **Partial-leg closes and the first-release close form** *(operator rulings, 2026-10-01, in the coordinating session:)*
   - *"partial-leg closes are unsupported for the first release";*
   - *the scope was first clarified on the coordinator's recommendation;*
   - *after Codex's reviews found conflicts with the C-a close direction and with gate C, it was revised to the coordinator's (a′), which Joshua agreed directly.*
   1. **Unsupported in the first release:** any *intentional* partial exit, meaning a strategy or the operator choosing to close only part of a leg (a scale-out).
   2. **The first-release close form is C-a:** one whole-leg broker liquidation, a quantity-less REST close mapped to one `liquidateposition` ([C-a](../../notes/2026-09-26-close-semantics-c-a.md); [incident ADR §A11.1](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a111--operator-ruling-close-direction-2026-09-26)).
      - It is used for **every** strategy close, scheduled flatten and attended recovery close.
      - The editions pre-registration's owed rows **ORB-6 and STR-7 are answered** for the first release as "follow the accepted close realization (C-a)". There are **no N-sequential one-contract exits**.
      - **Entries keep §2's one-contract-per-request rule.** Sizing is unchanged, and legs are not capped.
      - For the first release, the §6 exit-split replay item is moot, because a C-a close is one request. The entry-split replay stays.
   3. **Gate C is kept.**
      - C-a stays investigation-only until its M1–M9 are answered and **X-3** traces exactly this execution form. That includes protection cleanup after liquidation, no reversal, and the remainder if the liquidation fills only partly.
      - UB-5 and the rail contract's L2(d)/L2(e) obligations stay at gate C.
      - A single liquidation whose outcome is unknown or partial is an incident: halt and attended reconciliation, with the reservation held (§A12 F1 as proposed in PR #584).
   4. **If C-a fails its investigation or X-3,** the close form returns to the operator before the first release. Sequential one-contract exits would then need their own gate-C evidence: orphan-protection cleanup, reversal prevention and durable remainder recovery.
   5. **Prerequisite, a Rule-0 source check.** The "exit-side partials moot" statements in T08 and the session plan are withdrawn by the incident contract, so this ruling does not rest on them. Before the first release, a source check must establish that every close path is **whole-leg by intent**. It covers:
      - the four legs' Pine and accepted ports, including **STR-5** (whether Striker's crossed-level exit can apply to a subset);
      - the rail- and attended-owned paths: the multi-leg rail spec, halt/resume, and T13's fill-scoped and queued recovery CLOSE.

      Private sources are read in place, under the private read surface. **Any intentional subset exit found returns to the operator** before the first release.
   - For §A12's F4 partial-close row (PR #584), the first-release disposition is: intentional partial exits unsupported, and every close via C-a. That is an input to the operator's acceptance of §A12; this entry does not amend §A12's text.
   - Nothing here changes a strategy, sizing or protection rule.

**Also recorded:**
- **#570** (the simplification decision packet) is the vehicle for D-GO, D-HIST, D-REC and D-MON.
- **#579** (the audit-rescope card) is **not dispatched**; no new audit starts.
- **Qualification recovery (D3, R1–R10) is unchanged** by these rulings. Any simplification of it comes back as a separate D3 amendment, using #570 §4's interruption-cost comparison.

## Verification of this planning artifact

Current status was checked through authenticated GitHub queries and fetched Git
objects. No new test-pass or live-capability claim is made. Before dispatch,
refresh the moving #436 head and ongoing owner returns. The primary checkout's
old staged September 19 documents are not the current B0 record and were left
untouched. This checklist is not a commit, merge, provider contact or deployment.
