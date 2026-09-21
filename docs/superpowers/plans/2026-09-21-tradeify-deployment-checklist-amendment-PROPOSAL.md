# Tradeify Deployment Checklist — Amendment Proposal (2026-09-21)

> **Status: PROPOSAL for operator ratification.** Amends [the 2026-09-20 checklist](2026-09-20-tradeify-deployment-checklist.md); it does not replace it. Every packet not named here keeps its 09-20 text, envelope and acceptance criteria. This amendment changes no portfolio, statistical criterion, authority, source-evidence requirement or operator GO; it adds one bounded investment decision (T00, not a gate), one incremental tooling packet (T01b), and re-sequences work that the original already allowed to run in parallel. Revision 2 folds the Codex review of `d8f60ea` (three findings, all verified against source; dispositions in section 7). Ratify by merging this PR and ticking the decisions in §4; until then the 09-20 checklist governs.

## 1. Why amend now

S2 was accepted on 2026-09-21 (PR #436 ledger entry). Two facts from that work drive this amendment:

1. **Engineering is not the critical path.** T14 (production feed) is blocked on a provider and funding decision (Databento retired 2026-09-10, no replacement approved); T09 (real broker adapter) is blocked on the actual Tradovate order path; T07 (settlement) on real exports. None can start without operator decisions, and T15 cannot join until all three agree with the engineering. At the S2 pace the spine finishes in weeks and then waits.
2. **The Linux loop dominated S2's wall time.** About twenty hosted runs at ~25 minutes each; every packet needed two to five iterations. The suite grows past thirty nodes with S3. Cheap tooling (a labelled single-case diagnostic mode, two-host sharding, cached provisioning) was identified during S2 and deferred; it pays back inside S3's first iteration.

And one open question that predates S2: the bounded feasibility screen of 2026-09-09 returned a FRAGILE disposition on a seven-entry menu that is **not** the selected four-strategy book, and its closure record (`docs/notes/2026-09-10-tradeify-protection-selection.md`, "Feasibility screen closure") states that subsequent review found an incorrect all-halves speed requirement and unsupported lower-bound language, and that "the report's disposition is not an accepted qualification or rejection". So the deployment target has no accepted feasibility evidence either way. That is a reason to buy the evidence early and cheaply if a faithful producer exists, not a reason to gate the spine on a screen that may not be able to answer.

## 2. New and changed packets

### T00 — Feasibility evidence for the selected book (NEW; investment decision, not a gate; 250k–500k, may return early)
**Selected outcome:** an honest answer to "does a faithful producer exist that can screen the selected four-strategy book under Tradeify Select's rules with a synchronized intraday clock?" and, only if it does, a bounded pre-registered screen. Three outcomes are legitimate: **GO-evidence**, **NO-GO-evidence**, or **INSUFFICIENT** (no faithful producer / model incompatibility / missing synchronized intraday input), each with its cost. T00 runs in parallel with the spine and feeds T15's F1 and the operator's investment decision; **it does not gate T02.**
**Why the 09-09 screen cannot simply be re-run:** `core/mc/simulation.py::simulate_path` takes `intraday_low` as an optional per-day minimum-equity series supplied by the caller; there is no flag that reconstructs synchronized intraday equity from daily trade cashflows, and the replay specification records why recorded-trade arithmetic cannot reproduce the selected book's integer sizing, ORB base/add behavior, capacity and takeover rules. A screen without a faithful producer and a real intraday series yields EOD-clock lower bounds, which the standing lesson forbids carrying forward as survival.
**Ownership:** coordinator dispatches one executor; the operator ratifies any pre-registration **only after step 1 reports a producer exists**.
- [ ] **Step 1: producer inventory (return early if negative).** Identify and verify an existing faithful replay/output producer for the selected four expressions (the joint-replay worktree's canonical ledgers and its replay engine are the first candidates; state exactly what each reproduces of integer sizing / ORB base-add / capacity / takeover and whether it emits a synchronized `intraday_low`). If none exists, return **INSUFFICIENT** with the input/model blocker and the cost of building the producer; that is a decision for the operator, not an in-packet build.
- [ ] **Step 2: pin and pre-register** (only after step 1 is positive and ratified): the four expressions by identity, captured sizes and allocations; the pass floor per partition; the scenarios; the intraday clock as mandatory; the NO-GO condition, verbatim before execution, unchanged after.
- [ ] **Step 3: run and return** GO-evidence / NO-GO-evidence against the pre-registered condition only, with `results.json`/`REPORT.md` retained under the private root and every figure bound to ledger digests. A NO-GO-evidence verdict is presented to the operator as an investment decision (adjust the book, or accept the risk into T15's F1), never routed automatically to a portfolio-adjustment packet.
**Verification:** the producer's own tests plus the screen tests; a synchronized `intraday_low` actually supplied (its provenance recorded), or the verdict is INSUFFICIENT. **Forbidden:** EOD-clock "zero bust" as survival; moving the floor after results; re-optimizing any expression; claiming a verdict the producer cannot support.

### T01 — DONE (S2 accepted 2026-09-21)
Ledger entry "Coordinator acceptance — S2 budgeted admission and real Linux work supervision, 2026-09-21"; PR #436 merge gated on run 35555309697. B1–B6 as written are satisfied; nothing further.

### T01b — Linux evidence loop tooling (NEW; incremental; 50k–250k; not an all-or-nothing predecessor)
**Selected outcome:** an S3 iteration on a single failing case costs minutes, not a 25-minute fresh host, without weakening acceptance-grade runs.
- [ ] **First and small (lands during T02's first iteration, not before it):** `workflow_dispatch` input `cases` (a `-k` expression) for a labelled **diagnostic** run: invariants expected to fail, record marked `acceptance_scope=DIAGNOSTIC_SUBSET`, refused by `s2_run_evidence.py` as evidence.
- [ ] **Only when measured savings justify the implementation and evidence-validation work:** two-host sharding by manifest node list (OOM case last on its shard; the evidence script merges both records and requires both); cached provisioned venv/worker image with the host-facts step still recording the actual host.
**Verification:** one diagnostic run refused by the evidence script; for each later item, a measured before/after on an acceptance-grade run. **Return boundary:** tooling only; no change to any registered node or assertion.

### T02 — S3 (unchanged scope; sequencing and ceremony amended)
The four design decisions were ruled 2026-09-21 (draft packet `docs/briefs/handoffs/2026-09-21-full-e1-s3-n1-genuine-capture-DRAFT.md`): new versioned campaign tables + one FULL_E1 checkpoint evidence family; G5 as a host transient unit under the work slice; the bootstrap-level readiness handshake for every payload + a bounded output mount + phase-limited BudgetGuard; release/v5 + profile/v5 opening N1 dispatch only. **Amended process:** one executor (GLM), one coordinator (Claude); exactly one design-freeze checkpoint (the C1 shape: head, line-1 record, interface table, fixture ledger, fail-on-base evidence) before the Linux run; **the schema family and the result/seal interfaces are frozen and published at that checkpoint** so T05 can start (§T05); one independent review at return. Predecessor: T01 (S2 accepted). T00 is parallel, not a predecessor; T01b's diagnostic mode lands inside T02's first iteration.

### T03 / T04 — S4 / S5 (unchanged; sequential after T02)
They extend T02's checkpoint machinery to more stages and share its owners; no parallel writer.

### T05 — S6–S7 (AMENDED: parallel build, sequenced acceptance)
The result-commit and seal code consumes captures and assessments; it does not need N2 or Part A to exist to be built. **Start T05's build on an isolated branch when T02's checkpoint publishes an explicit interface freeze**: the schema family AND transaction ownership (which store method owns the commit), VOID serialization against publication (the single observable ordering of spec 2.8), signing-intent/recovery semantics, and budget accounting for the result/seal phases, with a named file boundary (its own modules and its own versioned tables; no edits to the service/store files T03/T04 are writing — a needed edit there is a CHECKPOINT to the coordinator). Accept T05 only after T04, against the real captures. The 09-20 text's "preparation of future tests on an isolated branch against explicitly agreed interfaces" is extended to implementation under that boundary.

### T06 — S8 (AMENDED: fold the ceremony, preserve the work)
Every slice registers its Linux cases as E-cases as it lands, but that does not deliver E01–E12 by itself: the complete installed PASS-to-seal path, crashes across signing/commit boundaries, cumulative budgets and VOID races across components are cross-component cases with no single-slice owner. The 09-18 S8 slice assigns fixture/driver/harness implementation (`test_full_campaign_boundary.py`, manifest, verification scripts, workflow); that work is retained. **Amended shape:** (a) a cross-component E-case ownership table is written at T02's interface freeze, each of E01–E12 named to the slice that builds its test, with the ones that span slices assigned to T06 explicitly; (b) T06 keeps a bounded integration/fix allowance (250k–500k) for the driver, fixtures, harness extension and the final integrated sharded run plus the combined independent review; (c) what is removed is only the duplicate ceremony (a separate acceptance write-up per E-case already accepted with its slice), not the tests.

### External tracks — START NOW, not "alongside" (unchanged scope; sequencing amended)
- **T07** (settlement), **T08** (broker/protection feasibility), **T10** (real source and freeze packet) dispatch **immediately under their existing authority**; they need no engineering predecessor and no T00 outcome, since real report semantics and broker capabilities can invalidate the approach regardless of historical performance.
- **T14** provider-neutral work (entitlement/cost/symbol/roll/session proposal, frozen equivalence criteria) dispatches now; provider-specific work waits on decision D-feed (§4).
- **T09** follows T08 and needs decision D-broker (§4).
- **T13** follows the incident-amendment ruling (the bounded platform-protection ADR is still Proposed).

### Review and ceremony (all packets)
Adversarial review stays (it found the two P2 findings and three resume races in S2) but is consolidated: one independent review per packet at return **plus focused verification of every fix that follows it** (a literal one-review ceiling would leave later changes unreviewed), one coordinator checkpoint at design freeze, one ledger entry per packet. The protected-service architecture selected by B0 is retained; no architecture migration is proposed. Manual settlement/recovery and better concurrency are the nearer opportunities. The Codex PR bot is at its usage limit; decision D-codex (§4) either funds it or accepts the in-session independent reviewer as the standing substitute. One writer per surface, always; the dual-executor overlap of 2026-09-20 is not to be repeated.

## 3. Amended dependency and dispatch summary

- **T00** runs in parallel; its verdict (GO-evidence / NO-GO-evidence / INSUFFICIENT) is an operator investment decision feeding T15's F1; it gates nothing.
- **Spine:** T02 (T01b diagnostic mode inside its first iteration) → T03 → T04 → (T05 accepted) → T06 (cross-component E-cases per the ownership table, integrated sharded run, combined review).
- **Parallel with the spine:** T00; T05 build from T02's interface freeze; T07, T08, T10, T14-neutral immediately; T09 after T08 + D-broker; T13 after the incident ruling; T11 after T06; T12 prepares against T02's frozen interfaces, needs T06 + a timing answer before F1.
- **Join:** T15 (freeze, production E1, D0/D1) → T16 → T17 as written.

## 4. Operator decisions this amendment needs (tick to ratify)

- [ ] **D-T00** — authorize T00 step 1 (producer inventory, may return INSUFFICIENT); ratify any pre-registration only after step 1 reports a faithful producer with a synchronized intraday series.
- [ ] **D-feed** — name the production feed provider (or the funding gate that must clear first); T14 provider-specific work is blocked until this is ticked.
- [ ] **D-broker** — grant the actual Tradovate/CrossTrade order-path access T09 needs (no agent places a trade; the adapter is qualified against real request/fill identities under the existing disarmed posture).
- [ ] **D-codex** — fund the Codex PR bot, or accept the in-session independent reviewer as the standing review for every packet.
- [ ] **D-sequence** — accept the T05 parallel build behind the explicit interface freeze and the T06 fold-with-preserved-work.

## 5. Provisional timeline

No measured critical path exists yet; this is an estimate to be replaced by measured packet durations. At the S2 pace, with T01b's diagnostic mode inside T02 and T05 in parallel, the spine T02–T06 is roughly three weeks of agent work, and T11, T12 (n3 machinery), T09/T14 integration and T15–T17 remain substantial work beyond it. The external tracks are bounded by the decisions in section 4, not by tokens. The four-firm program falsifier is dated 2026-11-08: a first attended Tradeify session before that date is plausible only if D-feed and D-broker are decided within the next week and nothing in T07/T08 invalidates the route. T00's verdict changes the investment decision, not the schedule.

## 6. Verification of this planning artifact

No new test-pass or capability claim is made. T00 is the only new acceptance gate; T01b is tooling; every other change re-sequences work the 09-20 text already permitted in parallel. Nothing here is a commit, merge, provider contact or deployment.

## 7. Review dispositions (Codex review of `d8f60ea`, folded in revision 2)

| Finding | Verified against | Disposition |
|---|---|---|
| P1: T00 did not specify the inputs/execution model its verdict needs (`simulate_path` needs an actual `intraday_low` series; uniform P&L scaling cannot reproduce integer sizing / ORB base-add / capacity / takeover) | `core/mc/simulation.py` lines 309-357; the replay specification | **Accepted.** T00 rewritten: step 1 producer inventory with an INSUFFICIENT outcome; no verdict without a faithful producer and a real intraday series; not a gate. |
| P2: the rationale treated a corrected historical interpretation as an established rejection | `docs/notes/2026-09-10-tradeify-protection-selection.md`, "Feasibility screen closure" | **Accepted.** Section 1 rewritten; three outcomes; presented as an investment decision. |
| P2: folding T06 left cross-component test construction unassigned | execution-slices plan, S8 Files and steps | **Accepted.** T06 keeps the fixture/driver/harness work with an ownership table and a bounded allowance; only duplicate ceremony is folded. |
| T07/T08/T10 should not wait for T00 | | **Accepted**; they start immediately. |
| T01b should be incremental | | **Accepted**; diagnostic selection first, shard/cache when measured. |
| T05's freeze must include transaction ownership, VOID serialization, signing recovery, budget accounting | | **Accepted**; written into T05. |
| One-review ceiling must not leave fixes unreviewed; retain the B0 architecture | | **Accepted**; both written into the review paragraph. |
| Three-week estimate is provisional | | **Accepted**; section 5 relabelled and scoped. |
