# Phase 3 Completion Handoff Implementation Plan

> **For agentic workers:** Execute with superpowers:executing-plans; use superpowers:subagent-driven-development when bounded delegation is useful and authorized. Preserve the behavioral contract and integration owner. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete production qualification of the fixed portfolio through authenticated E1 PASS/seal, completed D0 admission and separate affirmative D1 ORB GO, or report the prescribed failure/blocker without claiming successful Phase 3 exit.

**Architecture:** Consume the accepted successor of PR 415, close its execution-authority findings, and reuse the existing F01–F52 preparation and qualification mechanics. One coordinating agent owns source-to-execution-to-admission acceptance; source owners supply facts and designated authorities approve only concrete, current subjects.

**Tech Stack:** Existing Python qualification/replay libraries, operations launcher, durable attempt storage, signed trust domains and the proposed controlled execution boundary where accepted. Private inputs and results remain in approved ignored evidence roots.

**Spec:** [Phase 3 qualification plan](2026-09-16-phase3-simplified-qualification.md), [production readiness packet](2026-09-16-phase3-production-readiness-budget-handoff.md), [execution-boundary design](../specs/2026-09-17-qualification-execution-boundary-design.md), its [N1 implementation plan](2026-09-17-qualification-execution-boundary.md), and the accepted qualification preregistration/TB-P2/F01–F52 owners referenced there.

## Global Constraints

- **DRAFT HANDOFF, 2026-09-17.** This request authorizes drafting only. A later instruction to execute this handoff resumes completion work; it does not itself supply F1, exact-depth signatures, admission approval, ORB GO or production-service deployment authority.
- Reuse valid existing approvals and accepted evidence. Prepare exact decision subjects before requesting missing authority; batch independent unresolved choices and continue unaffected work.
- Preserve the fixed four-leg portfolio and seven-bundle evidence population. Do not tune rules, allocations, source windows, thresholds or sampling after results are seen.
- Keep secrets, private source bodies, account values, signatures and numerical results outside public documents. Confirm ignore status before writing private artifacts.
- Preserve other tasks' worktrees and unrelated edits. Select an isolated accepted successor; do not run from another task's dirty checkout.
- Configuration belongs in canonical versioned objects with explicit variants and instance bindings. Secrets are references; validation and execution must consume the same resolved configuration identity.
- Stop before Phase 4 portfolio materialization, production-feed purchase, broker tests, fresh B7, final n3, deployment GO or trading activation.

---

## Read first: current state and precedence

The latest authenticated GitHub inspection in this conversation on 2026-09-17 found [PR 415](https://github.com/Joshua-Asante/first-passage/pull/415) OPEN at `319ce56978d58156b13f0da474ce249f8e9e4d61`, newer than the reviewed `5e935c8`. The newer head's fixes were not reviewed in this handoff. Reported synthetic tests do not accept private production sources or authorize qualification. Refresh its final head, reviews, checks and actual merge commit at execution; a provisional merge candidate is not proof of a merge.

The [qualification review](../../notes/audits/2026-09-17-pr415-qualification-review.md) recommends holding acceptance on `5e935c8`. It records fabricated checkpoint completion, consistently substituted seeds/source bindings, sealing after VOID, class-descriptor mutation and overlapping signing-key identities. Establish each finding's disposition against the selected successor rather than asserting it remains present or has been fixed. Merging the PR does not by itself close a finding.

The proposed execution boundary supports **synthetic N1 only**. N1 PASS means CONTINUE; the release cannot run N2/Part A or produce full E1 PASS/seal, and its design forbids starting real qualification. Full-campaign support is a genuine remaining engineering dependency, not a feature supplied by this handoff. Complete and accept a successor specification and implementation before real F1/execution. Do not bypass the boundary through the legacy in-process runner.

Earlier plans retain useful preparation and statistical requirements. Where they prescribe direct `run_production_e1`/local journal calls, reconcile those recipes with the accepted execution boundary before use. Likewise, replace historical bare-Python test recipes with the selected checkout's launcher.

Production code inspected for this handoff includes `book_policy.py`, `qualification/orchestration.py` and `qualification/seal.py` at `5e935c8`. Candidate policy construction is distinct from registry admission. No numerical policy change is proposed. Re-read production policy, sizing and configuration on the selected execution revision before preparing D0 or any risk-control change.

## Sequencing and pre-freeze deployment-feasibility checkpoint

The work order is **qualification engineering + early Phase 4 feasibility + source preparation → feasibility checkpoint → production F1/E1 → final Phase 4 acceptance → Phases 5–6**. Engineering and intake can proceed while the checkpoint is open. This changes sequencing, not statistical criteria, Phase 3 exit conditions or PR 415's engineering scope.

The coordinator records checkpoint acceptance in the existing Phase 3 `decision-packet.md`. Reference CAP-20260916 for source/route findings and `compute-depth.md`/`execution.md` for timing and execution evidence; do not create a competing capability matrix. Consume [Phase 4 Part A](2026-09-17-phase4-completion-handoff.md#part-a-early-feasibility-before-production-f1) before Task 3 below.

- [ ] **Recoverability:** establish a credible, source-backed protocol for settlement continuity and no-returned-ID request closure on the intended account/route. Identify accessible producers, coverage and delayed-effect semantics. A named API or hypothetical support reply is insufficient. Remaining consumer implementation/tests may stay open for Phase 4; an unknown decisive source guarantee or unsupported required primitive blocks this checkpoint.
- [ ] **Freeze/change boundary:** enumerate planned feed, route, incident and operations changes against the actual F1/shared-manifest inventory. Record whether each changes frozen behavior/bytes, is a specifically permitted later binding, or requires requalification. Complete and accept behavior-changing work before freezing affected components. Permitted later bindings need an accepted contract and verification procedure before F1; this handoff creates no new exclusion. Resolve qualification impact of incident behavior without inventing outage frequencies or performance thresholds.
- [ ] **Launch feasibility:** establish a defensible timing envelope for B7 capture, sole final n3, adjudication/signing, deployment GO, permitted build/reseal, restart and effective activation. Use authorized representative/synthetic measurements, measured overhead and explicit uncertainty/margin; distinguish estimates from observed end-to-end timing. Name a permissible boundary window and signer/operator availability. Do not assume an ordinary weekday boundary accommodates an hours-long computation.
- [ ] **Final-stage ownership:** name the owner and concrete remaining implementation/acceptance work for n3 under the accepted execution-authority design. Full E1 support is not n3 support. If missing machinery prevents a defensible timing envelope, complete enough synthetic engineering to resolve that uncertainty before production F1; do not consume the real attempt as a benchmark.
- [ ] Record each limb's evidence, identities, disposition and remaining bounded work. Block production F1/E1 if feasibility depends on an unresolved semantic amendment, unknown decisive producer guarantee or unexplained launch-time assumption. Continue unaffected preparation and present the exact decision needed.

This checkpoint is an implementation-order prerequisite, not production route qualification, an additional performance criterion or a demand for fresh B7. Phase 4 retains actual capability acceptance; Phase 6 retains the complete timed rehearsal on the exact final candidate. A later change that invalidates checkpoint evidence reopens the affected limb and follows the existing freeze/change rules.

## Task 1: Accept the complete qualification execution path

**Outcome:** A clean, revision-bound release can execute and attest the complete frozen E1 campaign, with current-validity result acceptance and no caller-fabricated completion path.

**Files/owners:** `ops/c1_rail/qualification/`, `tests/ops/qualification/`, the existing `docs/briefs/phase3-preparation/2026-09-16/post413-integration-acceptance.md`, and the linked execution-boundary specification/plan. The coordinator owns combined acceptance; the controlled execution owner owns journal transitions/output capture, while G5 independently adjudicates captured results.

- [ ] Pin the accepted PR 415 successor, upstream runtime and governing contracts; inventory the exact disposition of each review finding. Reuse unchanged passing evidence and identify only the unproven delta.
- [ ] Complete the authorized N1 vertical slice under its own plan and real OS-isolation acceptance. Windows unit tests alone cannot demonstrate the proposed Linux permission boundary.
- [ ] Before expanding beyond N1, produce and accept a full-campaign successor packet covering legality/CUTOFF, N1, joint N2/Part B, Part A ordinary/conditional expansion, cumulative resource accounting, output capture, authentication, durable commit and seal. Name concrete producer/consumer interfaces, persistence owners and executable cases before implementing them. Preserve frozen sampling and decision mechanics.
- [ ] Close all review variants in that composed path: independently derive ordered seeds and source/panel identities; reject fabricated outputs; separate role public keys as well as IDs; enforce validity atomically against VOID; cover the class-state drift issue within the accepted threat model.
- [ ] Prove the complete route using real executor work on retained synthetic sources, plus rejection of fabrication, stream substitution, stale/cross-domain attestations, concurrent invalidation, duplicate dispatch, crash/restart and resource exhaustion. Reduced TEST_ONLY fixtures cannot weaken provenance checks or production workload policy.
- [ ] Obtain independent combined review and record exact release/configuration identities, commands, environment and results in the existing engineering acceptance record. A partially implemented boundary remains blocked for real qualification.

**Acceptance:** The designated executor's actual captured output reaches G5 and a currently valid commit/seal transition; caller-controlled journal contents or a mock PASS cannot substitute. All required E1 stages are supported. No real attempt is consumed to test the machinery.

## Task 2: Finish the actual-source freeze packet

**Outcome:** One decision-ready packet supplies every F1 requirement from an identified, accepted producer.

**Files:** Existing `docs/briefs/phase3-preparation/2026-09-15/` records: `requirements.md`, `production-readiness.md`, `identity-ledger.md`, `freeze-candidate.md`, `compute-depth.md`, `representative-workloads.md`, `execution.md` and `decision-packet.md` (create the last if absent). The production-readiness handoff supplies the detailed intake/measurement procedure; extend it rather than create a parallel inventory.

- [ ] Reconcile F01–F52 once against the accepted full-campaign release. For each row name consuming gate, producer, original evidence, revision/digest, disposition and exact next action. A later-gate classification requires its owning contract and cannot waive F1 evidence.
- [ ] Locate existing private seven-bundle bodies, settings, ports, panels and scoped admission receipts before requesting missing inputs. Bind the four accepted live ports to their actual successor evidence.
- [ ] Complete required source/settings parity, startup/warmup, calendar and coverage acceptance. Resolve between-bar cutoff chronology with admissible source evidence or a permitted explicit model decision; a signature cannot manufacture missing observations.
- [ ] Prepare the full workload and compute budget from declared assumptions and authorized representative measurement. Include source verification, replay, proofs, persistence, adjudication and the accepted execution service. Historical synthetic timing and draft depth numbers are not ratified budgets.
- [ ] Bind every preregistered monitoring definition, RNG namespace, partition, perturbation, statistic and disposition. Keep later diagnostic execution at its owning gate; do not turn monitoring into extra n3 acceptance criteria.
- [ ] Assemble immutable candidate bytes, source/runtime/dependency/configuration inventories and the tested execution recipe. Packet preparation must not reserve an attempt root, claim a journal boot or consume outcome-bearing samples.

**Acceptance:** No unresolved freeze prerequisite is labeled satisfied. Private evidence reaches its actual consumer, with limitations preserved. The packet presents material decisions together, while exact signing subjects remain sequential where they depend on earlier approval.

## Task 3: Freeze and execute the authorized E1 once

**Outcome:** One approved frozen attempt reaches its prescribed disposition with a complete durable evidence chain.

- [ ] Verify engineering/source readiness, accepted pre-freeze deployment-feasibility checkpoint and enrolled authorities; present the actual F1 candidate and obtain its required approval. Validate the resulting immutable frozen contract through the accepted release.
- [ ] Derive the separate exact-depth subject from that actual F1 and attempt identity. Obtain approval of its exact workload and budget before dispatch; reuse earlier ratifications only within their actual scope.
- [ ] Rehearse the final accepted invocation with synthetic authority before production use. Record the service/CLI/API recipe in `execution.md`; do not invent commands from historical library names.
- [ ] Verify the approved private output location, unused attempt and exact configuration/source identities. Dispatch once through the accepted full-campaign owner. Its controller runs the prescribed stages without stage-by-stage operator prompts.
- [ ] Track progress through read-only status. On interruption, budget failure or uncertain dispatch, retain the original attempt and captured bytes; do not create a fresh namespace, reduce depth or rerun for a better result.

**Acceptance:** Missing/expired approval or changed identity prevents dispatch. A failed early gate prevents subsequent computation where prescribed. The full campaign uses the frozen samples and budgets; restart cannot mint another attempt. Do not add fresh live B7 as a pristine-E1 prerequisite.

## Task 4: Authenticate, seal and complete admission

**Outcome:** Actual PASS supports the exact E1 seal, completed D0 and separate affirmative D1; other outcomes retain their proper disposition.

- [ ] Independently adjudicate actual captured outputs and obtain designated producer authentication over those bytes. Commit only under current attempt validity using the accepted authority boundary.
- [ ] For complete PASS only, obtain the separate seal authority's signature over the exact payload and complete the atomic valid seal transition. Historical committed PASS after VOID cannot seal.
- [ ] Prepare and complete D0 through its existing registry/governance process, binding the sealed policy and provenance. Use the authorized review/merge process; an open admission PR is not completed D0.
- [ ] Prepare the separate D1 ORB decision and its supersession evidence. Withholding ORB GO blocks downstream binding; do not remove ORB or modify the fixed book to bypass it.
- [ ] Add a dated completion section to the existing decision packet and pass its evidence references to the [Phase 4 handoff](2026-09-17-phase4-completion-handoff.md).

The handoff must name accepted code/service/configuration identities; F1 and ratifications; source/parity/calendar evidence; attempt/result/authentication/commit/seal identities; D0 acceptance and D1 decision; verification records; the feasibility checkpoint, permitted later-binding rules and n3 owner; remaining limits and invalidation triggers. Keep sensitive attachments private.

## Verification and completion rule

From the checkout being tested, first run `./fp.ps1 doctor`. Then run affected qualification/runtime tests through `./fp.ps1 python -m pytest <selected-paths>`, and the required `./fp.ps1 check` and standard suites prescribed by that checkout. Use `python -I scripts/fp.py <command>` only as the documented launcher fallback when PowerShell 7.3+ is unavailable. Diagnose environment failures; do not bypass them. Keep research-environment work separate.

For execution-boundary changes, retain actual Linux isolation/integration results as well as unit tests. Report command, interpreter, exact revision/working-tree state, actual results and material skips/failures. Do not repeat unchanged expensive suites without a relevant change or unresolved concern.

Successful Phase 3 exit requires **accepted complete execution machinery + accepted actual inputs + F1/exact-depth approval + authenticated E1 PASS/seal + completed D0 + affirmative D1**. A terminal statistical failure closes the attempt without satisfying that exit. A blocker report names the missing producer/decision and one next action; it does not relabel the phase complete. No Phase 4–6 operation is performed by drafting this handoff.
