# Phase 4 Completion Handoff Implementation Plan

> **For agentic workers:** Execute with superpowers:executing-plans; use superpowers:subagent-driven-development when bounded delegation is useful and authorized. Preserve the behavioral contract and integration owner. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a disarmed candidate whose actual feed, account, broker route, settlement/recovery producers and portfolio bindings have passed their governing acceptance gates, ready for Phase 5 attended operations.

**Architecture:** Establish decisive route and deployment feasibility before production Phase 3 F1, then consume the completed Phase 3 evidence chain for final qualification and binding. Extend CAP-20260916 as the sole capability verdict record. One coordinator owns the combined result; the existing account owner retains broker-command permission and outstanding obligations.

**Tech Stack:** Existing Python daemon/listener, feed and observation interfaces, settlement verifier, durable account owner, canonical configuration/fingerprint tooling, private original captures and operations launcher.

**Spec:** [Phase 4 qualification plan](2026-09-16-phase4-real-capability-qualification.md), [self-service capability closure](2026-09-16-self-service-capability-closure.md), [CAP-20260916](../../briefs/phase4-preparation/2026-09-16/capability-decision.md), [feasibility design](../specs/2026-09-16-tradeify-settlement-order-feasibility-design.md), [bounded platform-protection direction](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md), and accepted TB-I4/TB-I5/TB-V1 and settlement/rail contracts referenced by those owners.

## Global Constraints

- **DRAFT HANDOFF, 2026-09-17.** Drafting executes nothing. Later execution progresses within existing authority; feed funding, new provider contact, order drills, host changes and production-service deployment require their applicable concrete authorization. Reuse existing valid permission rather than asking again.
- Successful exit consumes the [Phase 3 completion handoff](2026-09-17-phase3-completion-handoff.md): authenticated E1 seal, completed D0 and affirmative D1 ORB GO. Part A early feasibility is a required input to that handoff's pre-freeze checkpoint, not optional overlap and not dependent on Phase 3 completion. All work retains its existing authority boundaries.
- Keep the fixed book and accepted policy unchanged. Read current production policy/sizing/configuration before binding; no recalibration to accommodate provider behavior or observed results.
- Preserve private original bytes, provenance and revisions in approved ignored roots. Public records contain permitted identities, verdicts and limitations. Do not expose credentials or account values.
- Use canonical reusable configuration, explicit environment variants and account bindings, with secret references and boundary validation. Bind the resolved configuration identity used by both qualification and candidate activation preparation.
- Remain disarmed. This phase grants no B7, final n3, deployment GO, initial arm or Phase 5 operational acceptance.

---

## Starting facts and contract precedence

Authenticated GitHub inspection on 2026-09-17 confirmed [PR 411](https://github.com/Joshua-Asante/first-passage/pull/411) MERGED at `7c317703869d252e35560e994d9bd11576152827`. CAP's older statement that 411 is open is historical. Refresh the accepted design/runtime at execution and reconcile the exact delta; merging a design does not establish live capability.

CAP-20260916 currently records **BLOCKED FOR LIVE RELEASE**. The assessment identified missing settlement/recovery evidence and a production integration gap; synthetic account-owner tests do not qualify an actual broker. Refresh those findings against the selected current baseline instead of assuming they remain unchanged or have been resolved.

The September 17 platform-protection ADR records operator direction but remains **Proposed**, with governing-contract propagation pending. Reconcile it before dependent implementation: new strategy commands remain fenced, while specifically qualified pre-existing protection may continue through bounded signal/control faults. Unknown requests remain blocked and same-session strategy reactivation remains prohibited. Do not copy the older blanket-pause requirement or treat the amendment as route qualification.

Assess ordinary ATM against the exact platform/environment first. Do not assume a Tradovate server-side capability exists in a local/NinjaScript route or switch accounts/platforms implicitly. Any normal-path economic difference needs explicit disposition; convenient template behavior cannot replace accepted portfolio semantics.

## Part A: Early feasibility before production F1

Complete the decisive source/semantic investigation in Tasks 1–2 alongside Phase 3 engineering and input preparation. Do not wait for E1/D0/D1 to begin it. Source-independent feed preparation may also proceed within M1/A9/O-4 authority. Source feasibility can be established before consumer implementation; required live qualification cannot.

Return evidence to the [Phase 3 pre-freeze checkpoint](2026-09-17-phase3-completion-handoff.md#sequencing-and-pre-freeze-deployment-feasibility-checkpoint), using CAP references rather than copied verdicts:

- [ ] Identify accessible settlement and request-resolution producers with supported coverage, correlation and delayed-effect semantics. Distinguish remaining bounded consumer tests from missing provider guarantees. An unresolved decisive guarantee blocks the pre-freeze checkpoint even if other engineering can continue.
- [ ] Map intended route/feed/incident behavior to the frozen portfolio and shared-manifest inventory. Resolve differences and identify necessary changes before F1. Complete affected behavior-changing engineering before freezing it; record exact contract-authorized later bindings and their verification procedure. No blanket exemption for adapters, configuration or operations code is implied.
- [ ] Supply measured report-availability/collection facts where available, activation/session constraints and required operator actions to the Phase 3 launch-time assessment. Mark unknowns explicitly. Resolve timing-critical contract conflicts before accepting the checkpoint; do not assume evening approval survives a boot, evidence or session change.
- [ ] Record a supported recovery path or return the route/contract decision needed. Do not substitute indefinite polling, flatness or an account reset for a missing closure protocol.

**Part A exit:** the coordinator can accept or block each Phase 3 feasibility limb from named evidence. CAP rows may remain UNPROVEN pending real consumer acceptance; that status cannot hide an unknown decisive source guarantee. Part A grants no route PASS, feed funding, account mutation, production signature or live authority. It does not require every Phase 4 task to complete before F1.

## Task 1: Establish the accepted baseline and one capability inventory

**Outcome:** Every live requirement has a producer, consumer, bound environment and a current evidence verdict.

- [ ] Pin clean accepted code, applicable PR 411 successor and current incident-contract disposition. During Part A, bind the current Phase 3 candidate/preparation and mark completion artifacts pending; do not require E1/D0/D1 to investigate feasibility. At Part B entry, bind actual Phase 3 completion artifacts. Preserve unrelated worktrees; record exact revision and configuration identities.
- [ ] Reconcile and propagate the platform-protection authority split through the governing halt/resume and rail contracts, feasibility design, CAP, Phase 4/5/6 acceptance lists and operating/arming procedure before dependent implementation. Existing design direction needs no repeat permission; unresolved substantive differences require a concrete decision.
- [ ] Update CAP in place with S1–S5 settlement, R1–R5 recovery and every used N1/L2 primitive, plus feed, symbols, TB-I4 and candidate identity. Preserve historical rows as dated evidence.
- [ ] For each row retain source/entitlement, account/environment/route, coverage/query bounds/timezone, effective and capture times, original-byte digest, consumer/code/config identity, verdict, requalification trigger and one next action/owner.
- [ ] Establish the actual production chain and all possible actors using qualified read-only status or a consistent isolated snapshot. Do not call boot/migration/reconciliation methods merely to inspect production; copying an active SQLite main file alone is not a consistent snapshot.

**Acceptance:** Verdicts remain `QUALIFIED`, `UNPROVEN`, `UNSUPPORTED` or `AMENDMENT_REQUIRED`. A source-feasibility checkpoint can support an integration proposal while remaining UNPROVEN pending consumer acceptance. No competing capability ledger is created.

## Task 2: Close decisive recovery, settlement and normal-route gaps

**Outcome:** Actual supported sources can establish the account state and every possibly effective request's disposition through the intended consumers.

**Starting files:** `ops/c1_rail/book_account_owner.py`, `book_settlement.py`, `account_close_evidence.py`, `account_close_calculation.py`, their observation/reconciliation boundaries and existing tests on the accepted baseline. The detailed collection sequence belongs to the self-service closure plan.

**Two passes:** Part A establishes source feasibility and settles semantic differences; Part B closes remaining actual consumer/route acceptance. Reuse valid evidence between passes. Implementation that changes a frozen component must be accepted before F1 or follow its explicit later-change/invalidation rule, regardless of which task names the work.

- [ ] Investigate no-returned-ID request resolution early. Establish a key available before transport, supported lookup and causal coverage, terminal/no-future-effect semantics and all-actor scope. Empty history, exhausted pagination, timeout or apparent flatness cannot prove failure/quiescence.
- [ ] Identify the exact settlement predecessor and accepted chain, or produce evidence of no chain; missing export access is not evidence of absence. Retain original reports, timezone/session interpretation, adjustments, closing equity/finality and full required history. Do not replace an absent historical close with current balance or a new date.
- [ ] Pass an authorized isolated anchor/subsequent-close rehearsal through the actual verifier and account-owner consumer. Keep rehearsal receipts outside the production chain. Historical/record-only submissions must satisfy the accepted fresh-capture/history requirements.
- [ ] Map all four ports' real normal-operation requirements to the selected route: resting entries, brackets, amendments, scoped close, sibling cleanup, residual protection, trailing/OCO, ownership/FIFO, takeover and scheduled closure where used. Supported semantics and retained actual traces must substantiate each requirement.
- [ ] Apply the bounded ATM assessment, including dependencies during signal/host faults, partial fills, uncertain entry/modification, manual-close races and cutoff. Record precise normal-path differences; do not implement a custom protective manager merely to satisfy superseded pause wording.
- [ ] Where evidence is missing, prepare one bounded test with exact account/environment, actions, capture, expected result, intervention and teardown. Obtain only its necessary authority before account mutation. Do not manufacture live lost responses or unmanaged exposure.
- [ ] Once source semantics are adequate, implement only the identified production adapter/ingestion gap under a concrete interface/test packet. Pass retained actual observations through isolated consumers; test repeated fill credit, conflicting identity, sibling unknown attempts, delayed effects, corrections and restart with synthetic fault cases.

**Acceptance:** Real producer evidence reaches settlement and request/ownership consumers. Unknown requests retain reservations/ownership until their own supported outcome; resolving one does not clear another. Required capabilities missing or unsupported block the dependent route. Support replies can help but are neither a mandatory waiting step nor sufficient acceptance by themselves.

## Part B: Final qualification and binding after Phase 3

Before accepting this part, consume authenticated E1 PASS/seal, completed D0 and affirmative D1, plus the pre-freeze feasibility record and accepted later-binding rules. Complete remaining Task 2 consumer/route evidence, then Tasks 3–4. Earlier authorized preparation and captures can be reused within their identities, coverage and freshness; no ceremony is repeated solely because the phase label changed.

If final observations contradict early feasibility assumptions or require a frozen behavior change, stop affected acceptance and apply the governing amendment/requalification rule. Do not patch the runtime and preserve the old qualification by relabeling the change as integration. Phase 5 work touching frozen behavior obeys the same rule.

## Task 3: Select, bind and qualify the actual feed

**Outcome:** All four symbols pass the frozen feed protocol with signal emission disabled.

**Files/interfaces:** Accepted TB-I5 successor; existing `ops/c1_signal_daemon/feed.py`, its source interface and book synchronization barrier; `tests/ops/test_c1_signal_daemon_feed.py`. Use the Phase 4 plan's feed packet rather than inventing a competing comparison.

- [ ] Verify M1 RESOLVED before authoring/freezing TB-I5 and satisfy current A9/O-4 restrictions. Freeze overlap, OHLC/time/session conventions, holiday/roll handling, precision, tolerances, timing, missing/revised bars and binary decisions before seeing candidate results.
- [ ] Complete A9-PREP with a provider-neutral adapter contract and mocked auth/renewal/reconnect/stale-data refusal cases. Prepare current provider entitlement/licensing, all-symbol coverage, costs, endpoints, retention and a booked collection window. Obtain selection/funding only on that concrete proposal.
- [ ] Implement the approved source adapter after the relevant authority, with explicit reconnect/backfill/correction ordering and deterministic completion semantics. A `connected=True` flag does not establish these guarantees.
- [ ] Capture original delivered bytes with emission disabled; compare all four symbols to canonical accepted panels under the frozen protocol. Record source/configuration, window, verifier version and PASS/FAIL.
- [ ] Verify actual consumer behavior on stale/disconnected, duplicate/out-of-order, correction, roll/DST/early-close and missing-symbol barrier cases. Preserve any failure; no post-result tolerance, window or strategy changes to obtain PASS.

**Acceptance:** Complete four-symbol TB-I5 PASS and source-consumer evidence. Selection, payment or a connected feed is not equivalent to qualification. No unavailable symbol may be silently replaced.

## Task 4: Accept symbols, deduplication and the disarmed candidate

**Outcome:** The candidate binds the actual qualified route/source to the exact sealed portfolio under the governing fingerprint law.

**Files:** Accepted TB-V1 configuration owners, `ops/c1_rail/policy_fingerprint.py`, `tests/ops/test_book_host_bindings.py`, actual instrument records and the frozen TB-I4 preregistration/implementation plan.

- [ ] Verify account-accessible 6J, MGC, MYM and MNQ contracts, expiry/roll mapping, quantity/tick/point conventions and required order semantics. Continuous chart symbols are not order bindings; do not substitute MJY for 6J.
- [ ] Execute TB-I4's frozen R1–R6 and planted-defect cases only after its M1, implementation GO and prescribed disarmed-host checks. Keep signal deduplication distinct from real request/fill identity and unknown-request resolution.
- [ ] Confirm E1 seal, completed D0 and affirmative D1 before materializing TB-V1. Apply exactly the accepted active legs, allocations and lifecycle initialization with verified symbols and capabilities.
- [ ] Bind feed/route/observation configuration and dependencies into the candidate inventory. Prove shared-component equality with F1/E1 and apply the exact later-binding rules resolved before F1. A newly discovered change outside those rules requires explicit invalidation/requalification; do not defer defining the boundary until this task or silently rehash the freeze.
- [ ] Run affected binding/fingerprint and consumer tests, required repository checks and independent combined review. Any separately authorized host materialization must preserve disarm and verify durable read-back.
- [ ] Update CAP and its private evidence index with accepted scope, complete candidate identities, source expiry/coverage, settlement cadence, requalification triggers and unresolved limitations. Add the Phase 5 handoff there instead of creating a second acceptance record.

**Acceptance:** Missing/mismatched source, route, policy, allocation, lifecycle, symbol or capability refuses the candidate. A config flag cannot enable an unqualified route. Image/config identities and required evidence all describe the same candidate.

## Verification, exit and Phase 5 handoff

Before project Python use, run `./fp.ps1 doctor` from the selected checkout. Run focused tests through `./fp.ps1 python -m pytest <selected-paths>` and the checkout's required `./fp.ps1 check`/standard suites. If PowerShell 7.3+ is unavailable, use the documented `python -I scripts/fp.py <command>` bootstrap. Report command, interpreter, revision/working-tree state, results and skips/failures; never bypass environment validation.

Mock tests establish consumer behavior only. Live capability claims additionally need retained original observations, supported semantics and actual account/route binding. Record exact source coverage and freshness rather than extrapolating from one successful trace.

Successful Phase 4 exit requires **Phase 3 completion; frozen four-symbol TB-I5 PASS; qualified S1–S5, R1–R5 and every used N1/L2 capability; accepted symbol verification and TB-I4; and a verified disarmed TB-V1 candidate**. An exact infeasibility finding can complete an investigation while leaving this phase blocked.

Hand Phase 5 the CAP record and private evidence references, exact image/configuration/fingerprint identities, qualified producers and invocation procedures, reconciled incident authority split, actor/obligation inventory, settlement/reconciliation procedure, limitations and requalification triggers. [Phase 5](2026-09-16-phase5-attended-operations.md) owns real notification/heartbeat acceptance, acknowledgment, intervention/disarm, restoration and later-session activation; [Phase 6](2026-09-16-phase6-exact-release-launch.md) owns combined release acceptance, fresh B7, sole final n3, deployment GO and effective initial activation.

No provider purchase, contact, capture, order drill, implementation, deployment or activation was performed while drafting this handoff.
