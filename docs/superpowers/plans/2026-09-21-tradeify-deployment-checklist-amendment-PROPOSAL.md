# Tradeify Deployment Checklist — Amendment Proposal (2026-09-21)

> **Status: PROPOSAL for operator ratification.** Amends [the 2026-09-20 checklist](2026-09-20-tradeify-deployment-checklist.md); it does not replace it. Every packet not named here keeps its 09-20 text, envelope and acceptance criteria. This amendment changes no portfolio, statistical criterion, authority, source-evidence requirement or operator GO; it adds one bounded investment decision (T00, not a gate), one incremental tooling packet (T01b), and re-sequences work that the original already allowed to run in parallel. Revision 2 folds the Codex review of `d8f60ea` (three findings, all verified against source; dispositions in section 7). Ratify by merging this PR and ticking the decisions in §4; until then the 09-20 checklist governs. **Routing rule:** earlier handoffs (including the eleven September 12–19 packets preserved by PR #444) remain historical evidence of assignments, context and provenance; current dispatch follows the September 20 checklist as amended here and the latest specifically assigned handoff. A packet is not newly dispatchable merely because it was committed, and an older packet's ownership statements (e.g. the September 12 handoff naming Astra as coordinator) do not override later ownership decisions.

## 1. Why amend now

S2 was accepted on 2026-09-21 (PR #436 ledger entry). Two facts from that work drive this amendment:

1. **Engineering is not the critical path.** T14 (production feed) is blocked on a provider and funding decision (Databento retired 2026-09-10, no replacement approved); T09 (real broker adapter) is blocked on the actual Tradovate order path; T07 (settlement) on real exports. None can start without operator decisions, and T15 cannot join until all three agree with the engineering. At the S2 pace the spine finishes in weeks and then waits.
2. **The Linux loop dominated S2's wall time.** About twenty hosted runs at ~25 minutes each; every packet needed two to five iterations. The suite grows past thirty nodes with S3. Cheap tooling (a labelled single-case diagnostic mode, two-host sharding, cached provisioning) was identified during S2 and deferred; it pays back inside S3's first iteration.

And one open question that predates S2: the bounded feasibility screen of 2026-09-09 returned a FRAGILE disposition on a seven-entry menu that is **not** the selected four-strategy book, and its closure record (`docs/notes/2026-09-10-tradeify-protection-selection.md`, "Feasibility screen closure") states that subsequent review found an incorrect all-halves speed requirement and unsupported lower-bound language, and that "the report's disposition is not an accepted qualification or rejection". So the deployment target has no accepted feasibility evidence either way. That is a reason to buy the evidence early and cheaply if a faithful producer exists, not a reason to gate the spine on a screen that may not be able to answer.

## 2. New and changed packets

### T00 — Feasibility evidence for the selected book (NEW; investment decision, not a gate; 250k–500k, may return early)
**Selected outcome:** an honest answer to "does a faithful producer exist that can screen the selected four-strategy book under Tradeify Select's rules with a synchronized intraday clock?" and, only if it does, a bounded pre-registered screen. Three outcomes are legitimate: **GO-evidence**, **NO-GO-evidence**, or **INSUFFICIENT** (no faithful producer / model incompatibility / missing synchronized intraday input), each with its cost. T00 runs in parallel with the spine and feeds T15's F1 and the operator's investment decision; **it does not gate T02.**
**Why the 09-09 screen cannot simply be re-run:** `core/mc/simulation.py::simulate_path` takes `intraday_low` as an optional per-day minimum-equity *excursion* series supplied by the caller (dollars below that day's opening equity, so entries are `<= 0` and unscaled — not absolute intraday lows); there is no flag that reconstructs synchronized intraday equity from daily trade cashflows, and the replay specification records why recorded-trade arithmetic cannot reproduce the selected book's integer sizing, ORB base/add behavior, capacity and takeover rules. A screen without a faithful producer and a real intraday series cannot make an intraday-honest survival claim; the standing lesson (`lesson_tradeify_trail_enforced_intraday`) forbids carrying an EOD-clock result forward as survival, and whether such a result is even a bound for the selected book is itself unestablished.
**Ownership:** coordinator dispatches one executor; the operator ratifies any pre-registration **only after step 1 reports a producer exists**.
- [ ] **Step 1: producer inventory (return early if negative).** Identify and verify an existing faithful replay/output producer for the selected four expressions (the joint-replay worktree's canonical ledgers and its replay engine are the first candidates; state exactly what each reproduces of integer sizing / ORB base-add / capacity / takeover and whether it emits a synchronized `intraday_low`). If none exists, return **INSUFFICIENT** with the input/model blocker and the cost of building the producer; that is a decision for the operator, not an in-packet build.
- [ ] **Step 2: pin and pre-register** (only after step 1 is positive and ratified): the four expressions by identity, captured sizes and allocations; the pass floor per partition; the scenarios; the intraday clock as mandatory; the NO-GO condition, verbatim before execution, unchanged after.
- [ ] **Step 3: run and return** GO-evidence / NO-GO-evidence against the pre-registered condition only, with `results.json`/`REPORT.md` retained under the private root and every figure bound to ledger digests. A NO-GO-evidence verdict is presented to the operator as an investment decision (adjust the book, or accept the risk into T15's F1), never routed automatically to a portfolio-adjustment packet.
**Verification:** the producer's own tests plus the screen tests; a synchronized `intraday_low` actually supplied (its provenance recorded), or the verdict is INSUFFICIENT. **Forbidden:** EOD-clock "zero bust" as survival; moving the floor after results; re-optimizing any expression; claiming a verdict the producer cannot support.

### T01 — DONE (S2 accepted 2026-09-21)
Ledger entry "Coordinator acceptance — S2 budgeted admission and real Linux work supervision, 2026-09-21"; PR #436 merge gated on run 35557000399 (fifteen green, record `b16ef734…`); the earlier run 35555309697 failed on the deadline case's stopper and was repaired in `a519bfb` before the gate was met. B1–B6 as written are satisfied; nothing further.

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
Every slice registers its Linux cases as E-cases as it lands, but that does not deliver E01–E12 by itself: the complete installed PASS-to-seal path, crashes across signing/commit boundaries, cumulative budgets and VOID races across components are cross-component cases with no single-slice owner. The 09-18 S8 slice assigns fixture/driver/harness implementation (`test_full_campaign_boundary.py`, manifest, verification scripts, workflow); that work is retained. **Amended shape:** (a) a cross-component E-case ownership table is written at T02's interface freeze, each of E01–E12 named to the slice that builds its test, with the ones that span slices assigned to T06 explicitly; (b) T06 keeps a bounded integration/fix allowance (250k–500k) for the driver, fixtures, harness extension and the final integrated run (sharded only if T01b's sharding was adopted on measured savings) plus the combined independent review; (c) what is removed is only the duplicate ceremony (a separate acceptance write-up per E-case already accepted with its slice), not the tests.

### External tracks — START NOW, not "alongside" (unchanged scope; sequencing amended)
- **T07** (settlement), **T08** (broker/protection feasibility), **T10** (real source and freeze packet) dispatch **immediately under their existing authority** — packets authored 2026-09-21: [T07](../../briefs/handoffs/2026-09-21-tradeify-t07-manual-settlement-procedure.md), [T08](../../briefs/handoffs/2026-09-21-tradeify-t08-broker-protection-feasibility.md), [T10](../../briefs/handoffs/2026-09-21-tradeify-t10-source-and-freeze-packet.md); they need no engineering predecessor and no T00 outcome, since real report semantics and broker capabilities can invalidate the approach regardless of historical performance.
- **T14** provider-neutral work (entitlement/cost/symbol/roll/session proposal, frozen equivalence criteria) dispatches now; provider-specific work waits on decision D-feed (§4).
- **T09** follows T08 and needs decision D-broker (§4).
- **T13** follows the incident-amendment ruling (the bounded platform-protection ADR is still Proposed).

### Review and ceremony (all packets)
Adversarial review stays (it found the two P2 findings and three resume races in S2) but is consolidated: one independent review per packet at return **plus focused verification of every fix that follows it** (a literal one-review ceiling would leave later changes unreviewed), one coordinator checkpoint at design freeze, one ledger entry per packet. The protected-service architecture selected by B0 is retained; no architecture migration is proposed. Manual settlement/recovery and better concurrency are the nearer opportunities. The Codex PR bot is at its usage limit; decision D-codex (§4) either funds it or accepts the in-session independent reviewer as the standing substitute. One writer per surface, always; the dual-executor overlap of 2026-09-20 is not to be repeated.

## 3. Amended dependency and dispatch summary

- **T00** runs in parallel; its verdict (GO-evidence / NO-GO-evidence / INSUFFICIENT) is an operator investment decision feeding T15's F1; it gates nothing.
- **Spine:** T02 (T01b diagnostic mode inside its first iteration) → T03 → T04 → (T05 accepted) → T06 (cross-component E-cases per the ownership table, integrated run, combined review).
- **Parallel with the spine:** T00; T05 build from T02's interface freeze; T07, T08, T10, T14-neutral immediately; T09 after T08 + D-broker; T13 after the incident ruling; T11 after T06; T12 prepares against T02's frozen interfaces, needs T06 + a timing answer before F1.
- **Join:** T15 (freeze, production E1, D0/D1) → T16 → T17 as written.

## 4. Operator decisions this amendment needs (tick to ratify)

- [x] **D-T00** — authorize T00 step 1 (producer inventory, may return INSUFFICIENT); ratify any pre-registration only after step 1 reports a faithful producer with a synchronized intraday series. **— RULED 2026-09-22 (adopted as recommended): TICKED for step 1 only, under conditions 1–4 of the addendum row; see Addendum 2026-09-22.**
- [x] **D-feed** — name the production feed provider (or the funding gate that must clear first); T14 provider-specific work is blocked until this is ticked. **— RULED 2026-09-22 (adopted as recommended): TICKED as a gate — provider-specific work opens on T00 verdict ∉ {INSUFFICIENT, NO-GO-evidence} AND the T10 phase-2 F1 packet; A′ shortlisted, not applied; see Addendum 2026-09-22.**
- [x] **D-broker** — grant the actual Tradovate/CrossTrade order-path access T09 needs (no agent places a trade; the adapter is qualified against real request/fill identities under the existing disarmed posture). **— RULED 2026-09-22 (adopted as recommended): TICKED conditionally — granted automatically on T08 R3 = fence exists, void on R3 = none; read-only scope; every drill separately authorized; see Addendum 2026-09-22.**
- [x] **D-codex** — fund the Codex PR bot, or accept the in-session independent reviewer as the standing review for every packet. **— RULED 2026-09-22 (adopted as recommended): TICKED as the hybrid — separate-session refute-first review per packet; cross-vendor review at acceptance gates only; PR bot not funded; see Addendum 2026-09-22.**
- [x] **D-sequence** — accept the T05 parallel build behind the explicit interface freeze and the T06 fold-with-preserved-work. **— RULED 2026-09-22 (adopted as recommended): TICKED with two conditions — versioned T02 freeze; E01–E12 ownership table gates T02's checkpoint; see Addendum 2026-09-22.**

## 5. Provisional timeline

No measured critical path exists yet; this is an estimate to be replaced by measured packet durations. At the S2 pace, with T01b's diagnostic mode inside T02 and T05 in parallel, the spine T02–T06 is roughly three weeks of agent work, and T11, T12 (n3 machinery), T09/T14 integration and T15–T17 remain substantial work beyond it. The external tracks are bounded by the decisions in section 4, not by tokens. The four-firm program falsifier is dated 2026-11-08 and is discharged or fired by a dated lab re-MC of a pre-registered candidate (four-firm ADR §4), not by a live session; its measured state is 0-of-4 clearers. D-T00 is the only §4 decision that can bear on that clock, and only if the operator rules T00's screen to be falsifier evidence (Addendum 2026-09-22, D-T00 condition 4); otherwise the falsifier needs its own dated re-MC before 2026-11-08 regardless of §4. D-feed and D-broker set the pace of a first attended session, which the falsifier does not require; that session is bounded by the §4 decisions and by T07/T08's verdicts, not by 2026-11-08. *(Revised in place 2026-09-22 on ratification of Addendum 2026-09-22; prior sentence preserved in its §3.)* T00's verdict changes the investment decision, not the schedule.

## 6. Verification of this planning artifact

No new test-pass or capability claim is made. T00 is a parallel investment decision and gates nothing (there is no new acceptance gate); T01b is tooling; every other change re-sequences work the 09-20 text already permitted in parallel. Nothing here is a commit, merge, provider contact or deployment.

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
## Addendum 2026-09-22 — §4 dispositions (RATIFIED 2026-09-22 — all five adopted as recommended) and the §5 correction (applied)

> **Status: RATIFIED 2026-09-22.** Operator ruling, in session 2026-09-22, verbatim: **"Adopt all five as recommended."** Each row's *Wording to adopt* is now in force with the meaning that row defines; the §4 boxes are ticked with a dated pointer each, and the §3 correction is applied to §5 (prior sentence preserved in §3). What this ratification grants is exactly the five wordings and nothing wider: T00 **step 1 only** (no step-2 pre-registration, no screen run); D-feed as a **gate** (no provider named, no signup, no credential staging); D-broker **conditional on T08 R3** (no access granted yet); D-codex as the **hybrid** (no bot funding); D-sequence with its two conditions. No deployment, arming, activation, statistical dispatch or spend is granted; T00 step 1 is authorized, not dispatched — dispatch is the coordinating task's separate act under §58. The recommendation text below is preserved as authored. Prior Status line, for the record: "RECOMMENDATION. Nothing in this addendum ticks a §4 box or grants any authority."

### 0. Reads (Rule 0). Anchors are `git log -1 --format='%h %as' -- <path>` on `main@528b3c9`.

| Path | Anchor | Read |
|---|---|---|
| `docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md` | `d53a06e` 2026-09-13 | §4 falsifier :75–85; §0 clearer count :187, :219–229; single-clearer ruling :296–323 |
| `docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md` | `d53a06e` 2026-09-13 | Status line :9 |
| `docs/notes/2026-09-10-tradeify-protection-selection.md` | `d53a06e` 2026-09-13 | "Feasibility screen closure" :58–62 |
| `docs/adr/2026-08-08-s2b-signal-daemon-build.md` | `7c3ace8` 2026-09-14 | Live CME bar source row :48; A′ scoring :201, :209–223; operational risk :216; A′ not-applied :258–266 |
| `docs/adr/2026-07-17-c1-rail-build-account-registration-go.md` | `d53a06e` 2026-09-13 | Ceiling :40, :58 |
| `docs/notes/2026-09-12-tradeify-portfolio-coordinator-dispatch-1.md` | `d53a06e` 2026-09-13 | TB-S2 scope :44; TB-I2 status :53, :110 |
| `docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md` | `a39adf5` 2026-09-20 | #434 in-session review :525; continuation-2 return, G4 :567; Codex refusal + relayed external review :573–575; S6–S8 prerequisites :255–308; S2 acceptance :618–638 |
| `docs/briefs/handoffs/2026-09-21-full-e1-s3-n1-genuine-capture-DRAFT.md` | `a39adf5` 2026-09-20 | §0.5 ruled decisions :8–10; §1 "Interfaces (all ABSENT at f2606b0)" :18 |
| `docs/briefs/handoffs/2026-09-21-tradeify-t08-broker-protection-feasibility.md` | `dff1855` 2026-09-21 | §2 R3 early go/no-go; §5 operator inputs |
| `docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md` | `3feaaea` 2026-09-20 | T05 :140–150; T06 :151–161; T09 :188–198; T14 :245–255 |
| `core/mc/simulation.py` | `d53a06e` 2026-09-13 | `simulate_path` signature :309–326; `intraday_low` docstring :330–345; validation :357–366 |
| `STATE.md` | `72cec05` 2026-09-21 | 2026-11-08 forward-trigger block :155–172 |
| `AGENTS.md` (Live-execution posture: "No agent may place a trade"; spend ceiling row) | — | read in session |

**Found on second search.** A first search for `overlap`, `two writers`, `same surface`, `collid`, `overwrote` and `not to be repeated` across the ledger, `docs/SESSIONS.md`, the 09-20/09-21 handoffs and the 09-20 audits missed it; the literal phrase `dual-executor` found it. The incident this amendment's review paragraph cites is recorded in the execution-slices ledger twice — the S2 acceptance entry (`:636`: "the dual-executor history on G4 (`9727d95` committed by a second GLM session from the first's edits) is disclosed in the continuation-2 return") and the continuation-2 return itself (`:567`, G4: "the stopped worker's WIP `8c764d8` completed by the successor; `9727d95` is an operator commit of the first-round state"). `9727d95` resolves (2026-09-20, "fix(s2-g4): complete the store-invariant rulings from the second session's uncommitted implementation"). `lab/analysis/c1/tradeify_book_replay_2026-09/` does not exist.

### 1. The finding that reorders §4: the 2026-11-08 clock is a lab re-MC clock, not a live-session clock

The four-firm ADR's revert trigger (`:79`) reads: *"by 2026-11-08, no pre-registered portfolio candidate clears the pass-rate ceiling on any `AUTOMATION_FRIENDLY_PROP_FIRMS` tier in a dated lab re-MC → demote this program to research-only."* Its H (`:77`) is a **challenge-pass simulation**, explicitly "before any live account." The measured state is **0-of-4 clearers** (`:229`); the survivor-scoring pre-registration is `FROZEN / not-yet-exercised` (`prereg-v2:9`); the 09-09 screen's disposition "is not an accepted qualification or rejection" (`protection-selection:60`). STATE's 11-08 block already says it (`STATE.md:164`): *"absent the required qualifying clearance, demote to research-only."*

A production feed and a broker adapter contribute nothing to that trigger. Of the five §4 decisions, only **D-T00** can bear on it — and only if T00's screen is ruled to be falsifier evidence (row D-T00, condition 4). §5's sentence tying the date to D-feed and D-broker misattributes the urgency; §3 below proposes the correction.

### 2. Dispositions

Each row: recommended disposition · grounds · exact wording to adopt on ratification · operator ruling (blank until ruled).

#### D-T00 — **TICK step 1 now.** The one decision on the 11-08 clock.

**Grounds.** Step 1 is an inventory with an early INSUFFICIENT return, and its answer is genuinely open: the only in-repo replay artifact is the TB-S2 emulator, scoped as "per-leg TV-faithful replay broker … **not** the synchronized multi-leg replay" (`dispatch-1:44`); TB-I2, the engine that would be synchronized, is **BLOCKED** and never built (`dispatch-1:53, :110`); its study dir is absent. The "joint replay" and "canonical ledgers" T00 names are real but private artifacts of the seven-strategy campaign (`docs/adr/2026-09-05-tradeify-select-striker-expression-readmission.md:103`; `docs/methodology/lessons/methodology_lessons.md:1505`), built for the seven-entry menu and unverified for the selected four. That gap is what step 1 measures.

*Correction, 2026-09-22 (T00 step-1 return; prior sentence preserved above):* "the only in-repo replay artifact is the TB-S2 emulator" and "never built" are stale. TB-I2's engine was built, relocated from `lab/` to `ops/c1_rail/qualification/` ([Phase 3 tooling plan](2026-09-15-phase3-qualification-tooling.md) line 5), so the `lab/analysis/c1/tradeify_book_replay_2026-09/` study dir is absent only by relocation. Scored in the [T00 step-1 return](../../briefs/handoffs/2026-09-22-tradeify-t00-step1-producer-inventory.md#7-executor-return) §7.4, that package meets P1–P6 and fails P7, so the step-1 verdict is INSUFFICIENT. This corrects the grounds only; the ratified *Wording to adopt* and the operator ruling below are unchanged.

**Wording to adopt.** "D-T00 TICKED for step 1 only. Step 1's producer test uses `simulate_path`'s definition of `intraday_low` — a per-day minimum-equity *excursion* from the day's opening equity, entries `<= 0`, unscaled (`core/mc/simulation.py:325–345`) — as a named acceptance criterion; a producer emitting absolute lows fails it. Step 1 states, per expression of the selected four, what the producer reproduces of integer sizing / ORB base-add / capacity / takeover. Step 2's pre-registration cites `2026-08-26-prop-survivor-scoring-prereg-v2.md` and either adopts it or states why the selected book falls outside it; no second pre-registration for the same falsifier. Condition 4 — the operator rules, before step 2, whether T00's screen is §4 falsifier evidence: if yes, its ceiling, tiers and dating follow the four-firm ADR §4 as frozen; if no, the falsifier needs its own dated re-MC before 2026-11-08 regardless of T00."

**Operator ruling:** ADOPTED AS RECOMMENDED — operator, 2026-09-22, in session, verbatim: "Adopt all five as recommended." The *Wording to adopt* above is in force with the meaning this row defines.

**Condition 4 ruling:** NO — operator, 2026-09-23, in session, verbatim: "A T00 screen does not count as falsifier evidence." Under the wording above, the falsifier needs its own dated re-MC before 2026-11-08 regardless of T00; D-T00 no longer bears on the 11-08 clock. The operator accepted the step-1 return the same day ([return §7.8](../../briefs/handoffs/2026-09-22-tradeify-t00-step1-producer-inventory.md#78-operator-rulings-on-the-return-2026-09-23)).

#### D-feed — **TICK AS A GATE, not a provider.**

**Grounds.** The operator's own 2026-09-11 deferral (`s2b ADR:48`) sets the rule: *"provider-specific implementation, signup, subscription and credential staging wait until the fixed book clears every source-independent gate and the operator returns for the funding decision."* None has cleared. A′, the shortlisted route, is a personal live Tradovate account whose daemon-volume credential is a **live, order-capable brokerage login** — "the worst secret-at-rest profile of any option" (`:216`; Codex #344 confirmed order-capability unless vendor-scoped) — with a $1,000 parked deposit and KYC (`:201`), against the rail's **$700 all-in** ceiling to first live fill (`rail GO ADR:58`). No 11-08 dependency (§1). T14 provider-neutral preparation is already permitted and running.

**Wording to adopt.** "D-feed TICKED as a gate: provider-specific work opens when **(a)** T00 returns a verdict other than INSUFFICIENT or NO-GO-evidence **and (b)** T10 phase 2 has assembled the F1 packet. A′ remains shortlisted, not applied. T14 provider-neutral work proceeds now and may produce a dated KYC-readiness checklist; no signup, subscription or credential staging before both conditions hold. Whether a refundable deposit counts against the $700 ceiling is an operator reading recorded when (a) and (b) hold, not before."

**Operator ruling:** ADOPTED AS RECOMMENDED — operator, 2026-09-22, in session, verbatim: "Adopt all five as recommended." The *Wording to adopt* above is in force with the meaning this row defines.

#### D-broker — **DEFER; make it conditional on T08's R3 verdict.**

**Grounds.** T08's first step is a hard early go/no-go: whether any mechanism yields the unknown-request terminal fence the contract requires; if none, "T09 cannot be specified" (T08 §2). Nothing in T08 waits on D-broker — its R2/R4 evidence comes from the operator's own exports (T08 §5), not agent access. No 11-08 dependency (§1). AGENTS.md: "No agent may place a trade."

**Wording to adopt.** "D-broker TICKED conditionally: granted automatically when T08 returns R3 = fence exists, and void if T08 returns R3 = none. Scope: read-only request/order/fill/protection history and CrossTrade webhook identities. Every drill carries its own written authorization. No order-capable credential leaves the operator's hands."

**Operator ruling:** ADOPTED AS RECOMMENDED — operator, 2026-09-22, in session, verbatim: "Adopt all five as recommended." The *Wording to adopt* above is in force with the meaning this row defines.

#### D-codex — **HYBRID; neither option as written.**

**Grounds.** The PR bot refused at usage limits twice (#429; #436 — `ledger:573`). The operator-relayed **external** Codex review of `14a0e28` then found two P2 findings, "both confirmed as mechanisms; merge HELD" (`ledger:573`): cross-vendor review has demonstrated value at an acceptance gate. **In-session** independent review also has a record — the #434 host-fix review (0 BLOCKING / 5 ADVISORY / 6 NOTE, `ledger:525`) and the G5 P2-closure audit — and on this amendment itself found four factual defects after the last Codex pass (PR #448, `82e453c`). But that reviewer shares the author's vendor; the two P2s that held #436 were a different-vendor catch. The binary framing hides this: independence is worth paying for where a wrong acceptance is expensive, not on every push.

**Wording to adopt.** "D-codex TICKED as a hybrid. **(a)** Default per-packet review at return is an in-session independent review in a *separate* session, refute-first, run through `.claude/skills/pre-ratification-adversarial-panel`. **(b)** Cross-vendor review is required at acceptance gates only — each S-slice coordinator acceptance, T06's integrated run, T15's F1 — via the operator-relayed external Codex path that produced the `14a0e28` findings. **(c)** The Codex PR bot is not funded for per-push review; the D-codex row is re-read if (b)'s relay path stops being available."

**Operator ruling:** ADOPTED AS RECOMMENDED — operator, 2026-09-22, in session, verbatim: "Adopt all five as recommended." The *Wording to adopt* above is in force with the meaning this row defines.

#### D-sequence — **TICK, with two conditions.**

**Grounds.** T05's parallel build is bounded as the 09-20 text and this amendment require: a named file boundary, CHECKPOINT on any needed edit to T03/T04's files, acceptance only after T04 against real captures, and a freeze that already carries transaction ownership, VOID serialization, signing recovery and budget accounting (§7 dispositions). T06's fold removes only duplicate ceremony; the E01–E12 work stays with an ownership table. The residual risk is the freeze itself: the S3 DRAFT lists every interface T05 would consume as "all ABSENT at f2606b0; produce together, one owner" (`DRAFT:18`) — they are born during T02, and S4/S5 (prerequisites at `execution-slices:182, :225`) may move them.

**Wording to adopt.** "D-sequence TICKED with two conditions. **(1)** The T02 interface freeze is versioned: a tagged commit plus a schema version; T05 builds against that tag only; any post-freeze change to a frozen interface is a CHECKPOINT to the coordinator that names T05 as affected. **(2)** The cross-component E01–E12 ownership table is a gate on T02's checkpoint acceptance, not a courtesy deliverable — T02's checkpoint is not accepted without it."

**Citation grounded.** The review paragraph's "dual-executor overlap of 2026-09-20" is recorded: G4's first worker session stopped with uncommitted WIP (`8c764d8`), a second GLM session completed from those edits, and the operator committed the first-round state as `9727d95` (`execution-slices:567`, `:636`). One firing — under AGENTS.md's promotion rule (high-severity or independently recurring) it stays a candidate lesson, not yet a registry entry; capture it in `docs/methodology/lessons/` on a second firing. The one-writer-per-surface rule and condition (1) above stand on it.

**Operator ruling:** ADOPTED AS RECOMMENDED — operator, 2026-09-22, in session, verbatim: "Adopt all five as recommended." The *Wording to adopt* above is in force with the meaning this row defines.

### 3. §5 correction (APPLIED 2026-09-22 with the rows above; prior wording preserved here)

Replaced, in §5 — prior wording: *"The four-firm program falsifier is dated 2026-11-08: a first attended Tradeify session before that date is plausible only if D-feed and D-broker are decided within the next week and nothing in T07/T08 invalidates the route."*

With: *"The four-firm program falsifier is dated 2026-11-08 and is discharged or fired by a dated lab re-MC of a pre-registered candidate (four-firm ADR §4), not by a live session; its measured state is 0-of-4 clearers. D-T00 is the only §4 decision that can bear on that clock, and only if the operator rules T00's screen to be falsifier evidence (Addendum 2026-09-22, D-T00 condition 4); otherwise the falsifier needs its own dated re-MC before 2026-11-08 regardless of §4. D-feed and D-broker set the pace of a first attended session, which the falsifier does not require; that session is bounded by the §4 decisions and by T07/T08's verdicts, not by 2026-11-08."*

### 4. Boundary — what this addendum does not do

As authored (2026-09-22, pre-ratification) it ticked no §4 box and edited no §4 or §5 text. On ratification the same day the §4 boxes were ticked with dated pointers and §3's correction was applied to §5, prior wording preserved in §3. Beyond the five wordings it grants no GO, spend, access, signup or dispatch; opens no packet (T00, T09, T14 provider-specific, or any other). It changes no frozen definition, threshold, ceiling, allocation, `dd_protection` constant or MC calibration. It records recommendations for the operator's ruling and nothing more.

### 5. Audit hooks

```
# The clearer count §1 relies on; a change here re-opens §1 and D-T00 condition 4
grep -n "0-of-4" docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md
# Expect FROZEN / not-yet-exercised until a candidate is scored under it
grep -n "^\*\*Status:\*\*" docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md
# Expect 0 unticked after ratification 2026-09-22 (5 before it)
grep -n "^- \[ \] \*\*D-" docs/superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md
# Rows still awaiting a ruling — expect 0 after ratification 2026-09-22
grep -c "^\*\*Operator ruling:\*\* _(pending)_" docs/superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md
# Ratification pointers on the §4 lines — expect 5
grep -c "^- \[x\] \*\*D-.*RULED 2026-09-22" docs/superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md
# The dual-executor record D-sequence cites; expect execution-slices :636 (acceptance) and :567 (continuation-2 return)
grep -rn -i "dual-executor" docs/methodology/lessons/ docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md
# TB-I2's specified lab/ footprint: expect "No such file" (the engine was relocated, not abandoned; corrected 2026-09-22 per the T00 step-1 return)
ls lab/analysis/c1/tradeify_book_replay_2026-09/ 2>&1
# The relocated synchronized replay T00 step 1 scored (P1–P6 MET, P7 NOT MET); expect the BookReplay class and the runner's simulate_path call
grep -n "^class BookReplay" ops/c1_rail/qualification/replay.py; grep -n "intraday_low=low" ops/c1_rail/qualification/runner.py
# The intraday_low definition D-T00 binds to
sed -n '325p;330,334p' core/mc/simulation.py
```

### 6. Verification (run by the author before commit)

```
$ python3 <link resolver over this file>   # Expected: 0 broken relative links
$ make check                                # Expected: exit 0
$ for f in <§0 paths>; do git log -1 --format='%h %as' -- "$f"; done   # Expected: the §0 anchor column
```
