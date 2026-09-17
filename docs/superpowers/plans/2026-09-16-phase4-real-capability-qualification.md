# Phase 4 Real Capability Qualification Implementation Plan

> **Design amendment, 2026-09-17 UTC:** Apply the [bounded platform-protection incident contract](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md) when reassessing normal primitives and incident behavior. Qualify ordinary ATM plus a thin command-and-observation bridge before proposing custom trailing infrastructure. Programmatic ATM pause is no longer a universal requirement; uncertainty, protection identity/quantity, economic fidelity and no-same-session reactivation remain gates. Governing-contract propagation is pending.

> **For agentic workers:** Execute with superpowers:executing-plans; use superpowers:subagent-driven-development when bounded delegation is useful and authorized. Preserve the behavioral contract and integration owner. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish that one production feed and one actual account/execution route support the frozen four-leg portfolio, then bind the qualified identities into a disarmed candidate for Phase 5.

**Architecture:** Reuse the approved settlement/order-feasibility matrix as the single capability record. Resolve decisive route gaps before paid feed onboarding, apply one frozen four-symbol feed protocol with emission disabled, and reuse retained observations across consumer acceptance tests. The existing account owner remains the sole execution authority; the record and collection procedures grant no permission to trade.

**Tech Stack:** Existing Python signal daemon and listener, retained observations and durable journals, settlement verifier, instrument records, policy/runtime fingerprint tooling, pytest and private evidence files. No new service, evidence database, route failover or general workflow engine.

**Spec:** [Deployment phase breakdown](2026-09-15-deployment-phase-breakdown.md), [Phase 3 plan](2026-09-16-phase3-simplified-qualification.md), and the approved [settlement/order-feasibility design, PR 411](https://github.com/Joshua-Asante/first-passage/pull/411). Read the accepted successors of the Track B umbrella, rail-extension contract, attended-settlement contract and Track A A9 funding checkpoint before execution. Their inspected copies reside in `.worktrees/phase3-f1-preparation` and `.worktrees/tradeify-feasibility-design`; those worktrees are references, not execution baselines.

## Global Constraints

- **PROPOSED — planning only, 2026-09-16.** No capability test, provider selection, purchase, account change, support contact, implementation, deployment or order action is authorized by drafting this plan.
- Preserve the fixed four-leg book, existing sizing/protection/allocation laws, source-independent qualification and distinct operator approvals.
- One incumbent account, one qualified feed, one execution route and one durable account owner. No automatic provider substitution or shortened semantic fallback.
- Source-independent preparation may overlap earlier phases within its existing authority. Successful Phase 4 exit and TB-V1 binding require the prescribed Phase 3 E1/D0/D1 prerequisites.
- M1 `RESOLVED` through controlled input is not production-feed qualification. TB-I4 and TB-I5 retain their own M1/GO/disarmed prerequisites.
- Funding remains at Track A A9/O-4. A shortlisted provider is not selected, entitled or funded. Present current concrete facts at that checkpoint.
- Freeze the CME feed-equivalence protocol before observing candidate provider data. Do not apply or edit the old Pepperstone/XAUUSD test to claim CME equivalence.
- Actual order actions remain separately scoped and operator-executed. Isolated consumer rehearsals and synthetic failures cannot establish real broker guarantees.
- Raw reports, account identities, credentials, signatures, source and financial values stay under the primary checkout's approved ignored private roots, never inside worktrees. Public output uses permitted digests, verdicts and limitations.
- Preserve the approved minimal attended profile: an incident ends automated trading for that account session. Future-session activation still requires complete reconciliation and fresh bounded authority. Phase 5 owns the operational implementation and contract propagation.
- Phase 4 does not capture the expiring B7 launch seal, run n3, grant deployment GO or arm the portfolio.

---

## Design and operator workflow

The coordinating agent owns integration and one capability decision record. Existing source/report owners produce evidence; existing verifiers and consumers determine acceptance; Joshua retains account-only facts, feed selection/spend and authorized platform actions. No report generator becomes a permission owner.

Use four work packages:

1. Establish route feasibility and the exact evidence gaps.
2. Freeze the CME protocol and qualify the approved feed.
3. Close real-route evidence gaps through bounded characterization and consumer tests.
4. Bind the qualified portfolio and hand off the disarmed candidate.

Work package 1 is deliberately cheap: reuse existing records, entitlement facts and read-only observations. It should expose a decisive missing guarantee before paid feed onboarding. It need not manufacture difficult live traces just to reach the funding checkpoint. Work packages 2 and 3 may collect independent evidence during the same planned window once their separate prerequisites are met.

| Operator occasion | Prepared result | Required decision/action |
|---|---|---|
| Capability exception, only if needed | Exact unsupported/unproven requirement, existing evidence and one concrete alternative or amendment | Resolve the route/contract choice; no repeated flat-account polling |
| Feed checkpoint | Current provider, entitlement/licensing facts, total cost, collection-ready adapter plan, frozen protocol and booked validation window | Select and fund the exact proposal under A9; no open-ended spending |
| Bounded route test, only where retained evidence is insufficient | Account/environment, exact actions, evidence capture, intervention and teardown procedure | Authorize the named scope and perform required platform actions |
| Acceptance handoff | One record with verifier results, limitations, identities and remaining blockers | Resolve only outstanding operator-owned dispositions; technical evidence is accepted by its designated reviewers |

Combine preparation and compatible collection, not authority. A feed purchase, an order test, production settlement acceptance and portfolio activation remain separate scopes. Reuse valid prior approvals rather than asking again. Agent work covers retrieval, comparisons, hashing, trace assembly, test execution and report preparation under the execution authority in force.

## One capability record

Create `docs/briefs/phase4-preparation/2026-09-16/capability-decision.md` when this plan is executed, or extend the existing feasibility record if one has already been accepted. Do not create a competing record. Link Phase 3 evidence rather than copying its checklist.

Each row names: requirement and consuming contract; actual account/environment and route; producer and entitlement; source semantics and coverage; original-byte location/digest; capture/effective times; code/config revision; consumer verification; verdict; one next action; conditions requiring requalification. Use the approved verdicts `QUALIFIED`, `UNPROVEN`, `UNSUPPORTED`, `AMENDMENT_REQUIRED`. Missing evidence is not demonstrated incompatibility.

| Group | Coverage | Evidence producer → acceptance consumer |
|---|---|---|
| settlement-S1–S5 | Account/adjustments, session boundary, close equity, finished-close acceptance, continuous chain and repeatable procedure | Actual reports/capture procedure → settlement verifier → accepted account-owner/listener boundary |
| recovery-R1 | Durable operation and attempt before transport, crash uncertainty | Accepted PR 409 successor's journal tests → existing account owner; local engineering property |
| recovery-R2–R5 | Request/order/fill correlation, no-ID request resolution, complete causal history, account-wide request closure | Supported route/platform records and actor controls → existing reconciliation consumers |
| normal-N1 | Every normal primitive used by the four accepted ports | Supported actual route semantics and retained traces → listener/registry L2 admission and execution owners |
| Feed | Four-symbol overlap, session/timezone, aggregation, rolls, timing, correction/backfill behavior | Selected entitled feed and canonical TV panels → frozen TB-I5 comparison and source consumer tests |
| Symbol binding | 6J, MGC, MYM and MNQ actual tradable contracts and supported order semantics | Account-accessible instrument metadata and accepted verification records → TB-V1/listener bindings |
| Dedupe | Frozen TB-I4 R1–R6, plus actual request/execution identity consumption | Accepted implementation and real observations → durable dedupe/accounting consumers |
| Candidate identity | Source/config, route, verified symbols, admitted policy, active legs, frozen allocations and dependencies | Accepted artifacts → fingerprint/config verification and disarmed candidate |

Store a raw capture once and reference it wherever relevant. Its capture scope, freshness and source guarantees must satisfy every use; one successful trace does not prove unrelated capabilities. Exhausted pagination is not history completeness, a client tag is not broker deduplication, and flat positions do not prove request quiescence.

## Work package 1: Establish feasibility before expanding implementation

**Outcome:** Each decisive capability has either reusable qualifying evidence or one bounded next test/source; demonstrated incompatibilities stop dependent work before adapter/recovery construction.

**Inputs/files:** Approved feasibility design sections 4–6; existing producer/probe notes; accepted successors of `account_close_evidence.py`, `account_close_calculation.py`, `book_settlement.py` and the PR 409 account owner; rail-extension E1/E2/E3/K1 and L2 contracts. Pin actual paths/revisions on the accepted baseline instead of assuming all files exist in the inspected older worktrees.

- [ ] Pin the accepted integration revision and applicable contract revisions. Inspect Phase 3 state, M1 state and existing capability evidence without waking or changing another task.
- [ ] Establish whether an accepted production settlement chain actually exists; identify its exact missing predecessor, if any. A synthetic bootstrap or previously discussed date is not an accepted anchor.
- [ ] Inventory all actors: runtime, manual access, remote working orders, managers, triggers, copiers and queued/scheduled actions. Record delayed effects and what evidence can close each obligation.
- [ ] Map S1–S5 and R2–R5/N1 to actual entitled producers. Prioritize closing-equity provenance, no-returned-ID request resolution, complete history, remote quiescence and native protection/close semantics.
- [ ] Reuse valid accepted settlement traces. Otherwise specify the approved isolated anchor-plus-subsequent-close rehearsal, including source timezone, adjustments, chronology, predecessor and correction handling. Rehearsal receipts cannot enter the production chain.
- [ ] Record each remaining gap with exactly one collection/test capable of changing its verdict. If no supported producer can meet the requirement, return the route/contract decision before provider-specific production implementation.

**Acceptance:** A report-backed close reaches the actual verifier and intended consumer under isolated non-authorizing rehearsal, or remains explicitly unproven. A missing historical close is not replaced by current balance or a new date. A no-ID ambiguous request has an evidence-backed resolution protocol or an explicit blocker. R1 tests alone never qualify R2–R5. No account migration, database reset or new source law is implicit.

The approved feasibility design's release table governs: missing settlement, recovery or normal primitives blocks live release even with no same-session resume. Finishing this assessment with a precise blocker is a valid work-package result, not successful Phase 4 exit.

## Work package 2: Freeze and apply the actual feed protocol

**Outcome:** All four symbols pass a provider-neutral protocol fixed before candidate data is observed, using the selected source with emission disabled.

**Files:** Create `docs/spec/2026-09-16-cme-execution-feed-equivalence-test.md` only if no accepted TB-I5 successor exists; otherwise use that successor unchanged. Existing consumer boundary: `ops/c1_signal_daemon/feed.py`, `BarSource.poll() -> Bar | None` and `connected: bool`; existing feed tests: `tests/ops/test_c1_signal_daemon_feed.py`. Reconcile with the accepted multi-symbol completion barrier. Passing the simple `BarSource` protocol does not prove equivalence or ordered backfill delivery.

- [ ] Verify M1 `RESOLVED` before authoring/freezing the TB-I5 specification under its stated entry gate. Resolve the current A9/O-4 restrictions from the accepted Track A plan.
- [ ] Freeze the exact overlap window, all four symbol mappings, OHLC aggregation and timestamp conventions, timezone/session boundaries, holiday/early-close behavior, roll/continuous-series handling, precision/tolerances, timing cutoffs, missing/duplicate/revised-bar handling and binary decision rule. No results-driven threshold or window selection.
- [ ] Define correction/backfill/reconnect delivery explicitly: retained original and revision bytes, logical bar identity, eligibility for adapter evaluation, stale/gap disposition and deterministic completion markers. Missing transport capabilities are engineering gaps, not facts supplied by `connected=True`.
- [ ] Prepare the concrete feed proposal at A9: current quote and recurring/one-time costs, licensing, exchange coverage for every symbol, account/API entitlement, authentication/renewal, retention/history limits, permitted adapter preparation and scheduled validation. Verify current vendor facts at execution time; this plan selects no provider or price.
- [ ] Satisfy A9-PREP with the provider-neutral adapter contract and mocked auth/renewal/reconnect/staleness/fail-closed tests. The later provider-selection ruling opens the provider-specific packet naming endpoints, token renewal, dated-contract mappings, secret fields and the live test procedure. Do not require an already connected paid adapter to obtain that ruling, and do not bootstrap account/subscription access as preparation. Any vendor questions requiring messages to others need explicit contact authorization.
- [ ] After source selection/funding and implementation authority, deliver the adapter behind the accepted source interface. Use failing synthetic boundary tests before minimal repairs, then preserve raw delivered bars for the frozen comparison. Verify emission is disabled before and after collection.
- [ ] Apply the frozen comparison to all four symbols. Record source/config digests, window, verifier version, exclusions permitted by the frozen rule and PASS/FAIL. A missing required symbol or incomplete window cannot produce PASS.

**Consumer acceptance cases:** disconnect and stale data; reconnect with backfill; duplicate completed bar; out-of-order bar; correction after completion; timezone/DST and early close; roll mapping; missing participant at the book-wide barrier; configuration drift. Each test must assert the accepted consumer's delivery/refusal behavior, not just parsing. Use retained real captures for actual source claims and synthetic cases for hard-to-observe branches.

**Failure disposition:** Feed FAIL blocks the dependent live test. Investigate the source without tuning the strategy/adapters to make results match, switching providers automatically or moving thresholds after observation. Any successor protocol/source change follows its governing requalification process. Preserve the original result.

## Work package 3: Qualify actual route behavior and close evidence gaps

**Outcome:** Real source semantics and observations support each used primitive and every recovery guarantee, and the existing consumers correctly retain identity/ownership across uncertainty.

**Files/owners:** Accepted rail-extension contract; approved feasibility design; existing instrument records under `ops/instruments/`; accepted account owner, settlement verifier, broker observation ingestion and execution tests. TB-I4 consumes `PREREG-C1-DEDUPE-1` and its existing frozen implementation plan verbatim, including R1–R6 and planted-defect tests. No replacement dedupe design is introduced here.

- [ ] Verify every symbol against the actual account/route: tradable contract identity, expiry/roll mapping, tick/point/quantity conventions and supported order features. Do not infer order bindings from continuous data symbols or substitute MJY for 6J.
- [ ] Enumerate each port's declared L2 requirements and link them to normal-N1. Include resting stop entries; per-order bracket/attach; native atomic amendment; scoped close and attached-order removal; residual protection after partial fills; trailing/OCO behavior and protection-owner/FIFO allocation where used.
- [ ] Qualify required primitives using supported semantics plus retained actual evidence. Cancel/replace does not become atomic amendment; concurrent cancel/close does not become atomic scoped closure; locally tracked extrema do not become native trailing.
- [ ] Where actual evidence is absent, prepare one bounded operator-run procedure per necessary action sequence: account/environment, prerequisite state, action, identity/capture fields, expected evidence, stop condition, intervention and teardown. Specify its authorization separately. Do not deliberately lose a live response or create unmanaged exposure to manufacture a fault trace.
- [ ] Demonstrate supported no-ID request resolution and account-wide reconciliation through existing consumers. Independently exercise synthetic lost-response, partial-fill/cancel race, delayed remote action and restart cases without claiming the simulation proves provider guarantees.
- [ ] Execute TB-I4 only after M1 and its effective implementation GO/disarmed checks. Verify `dry_run=True` by the prescribed host read; distinguish this signal-deduplication gate from real execution-ID deduplication and request resolution.
- [ ] Feed retained observations through accepted isolated consumers: repeated fill credits once, contradictory identity is rejected, two unknown attempts remain independently owned, resolving one never clears the other, and history revisions preserve their correction obligations.
- [ ] Verify closure of each authorized test action and capture final account/order state. Any unresolved request/exposure remains an attended intervention obligation; ending a test window cannot discharge it.

**Acceptance:** Every used L2 item and S/R capability is independently qualified for the actual route/account, with source semantics and consumer traces. Ambiguous requests retain reservation/ownership until their own valid outcome. Restart/session rollover and apparent flatness cannot clear them. Missing completeness/quiescence guarantees block the route; manual attendance is not an evidence waiver.

Measure actual operator time and evidence latency where demonstrated, especially settlement submission and recovery closure. Mark unmeasured values unknown. If the procedure cannot meet the governing schedule/freshness bounds, present an exact feasibility or amendment decision rather than quietly relaxing them.

## Work package 4: Bind the portfolio and hand off a disarmed candidate

**Outcome:** The qualified identities are materialized in the candidate image/config and verified against the sealed portfolio, ready for Phase 5 operations integration.

**Files/interfaces:** TB-V1's existing binding/config owners, `ops/c1_rail/policy_fingerprint.py`, `tests/ops/test_book_host_bindings.py`, and the accepted runtime inventory. Existing fingerprint APIs include `build_shared_manifest(*, policy_row, geometry_source, registry_rows, components, tool_source, dependency_artifacts)` and `verify_shared_manifest(expected, **observed)`. These verify supplied inventories; they do not authorize a new shared component or a freeze amendment.

- [ ] Require actual E1 seal, D0 admission, separate affirmative D1 ORB GO and all symbol prerequisites before materializing TB-V1. A pending PR or withholding ORB is not a substitute.
- [ ] Materialize exactly the frozen active legs and allocations, accepted lifecycle initialization, verified symbols and qualified capabilities under TB-V1. Read production policy/binding code before edits; do not recalibrate values from feed or broker results.
- [ ] Include the accepted dedupe, source adapter/config, route/observation bindings and dependency identities in the candidate inventory. Prove the required equality of shared components against F1/E1 using the governing manifest rules.
- [ ] Reconcile the late-selected feed identity with the fingerprint contract explicitly. If the accepted contract defines a permitted later binding, prove that exact transition; if a newly selected source changes an already frozen shared component, stop for its required replacement/invalidation decision. Never silently add or rehash a field to preserve a claimed match.
- [ ] Run existing binding/fingerprint and affected consumer tests on the exact candidate, then the accepted repository's required checks and independent integration review. Preserve disarmed configuration and verify read-back for any separately authorized host change.
- [ ] Publish the public-safe capability record and handoff: qualified scope, evidence/config/code digests, unresolved items, requalification triggers, source coverage/expiry, settlement cadence and operator procedures. Keep the detailed attachments private.

**Acceptance cases:** missing/mismatched symbol, active-leg set, allocation, lifecycle row, capability or source digest refuses the candidate; stale evidence cannot inherit acceptance; an unqualified route cannot be enabled by a config flag. Duplicate observations cannot duplicate accounting. Accepted binding changes do not arm the host or grant permission to emit.

Phase 5 consumes this candidate and the actual reconciliation producers to complete incident fencing, notifications, acknowledgment, restore and the approved future-session-only reactivation behavior. The separately authorized combined attended dry-run and exact-release acceptance remain at their owning Phase 6 gate. This plan does not duplicate those ceremonies.

## Requalification and stop rules

| Change/event | Required disposition |
|---|---|
| Account/environment/route or enabled remote actor changes | Reassess affected S/R/N guarantees and bindings before use; no portable PASS by provider name |
| Feed adapter/config, aggregation, session or roll behavior changes | Apply the owning identity/change rule and repeat affected protocol acceptance; do not erase prior failure |
| Report correction, incomplete history or contradictory request evidence | Preserve raw revisions, invalidate affected acceptance through existing owners and retain obligations |
| Contract rollover | Apply the qualified rollover/mapping procedure and required symbol verification; a continuous chart symbol grants no order authority |
| Provider lacks a necessary guarantee | Mark UNSUPPORTED in examined scope and stop dependent work; present a concrete alternate route or explicit amendment |
| Evidence merely missing | Mark UNPROVEN with one bounded next acquisition; avoid unchanged repeated probes |
| Scope-limited/synthetic success | Retain its exact evidentiary scope; never promote it to production capability acceptance |

## Exit and execution boundary

Successful Phase 4 exit requires: frozen TB-I5 PASS on all four symbols; qualified settlement-S1–S5, recovery-R1–R5 and every used normal-N1 primitive; accepted symbol verification and TB-I4; completed Phase 3 prerequisites; and verified TB-V1/candidate identity under the existing fingerprint law. Reuse prior accepted evidence where its scope and freshness still apply.

A precise infeasibility finding can complete the assessment while leaving deployment blocked. There is no live-ready designation for a route with unresolved request history simply because the release is attended or does not resume in the same session.

This is a phase-level execution design, not a fabricated provider-specific implementation packet. Exact feed thresholds, collection commands and route actions are authored/frozen by their owning packets at the gates above, using the actual selected source and accepted baseline. Before dependent code or account actions, those packets must contain the concrete producer interfaces, executable tests and bounded procedures. Drafting this plan performs none of them.
