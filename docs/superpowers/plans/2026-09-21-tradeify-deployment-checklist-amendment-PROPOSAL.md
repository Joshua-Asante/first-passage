# Tradeify Deployment Checklist — Amendment Proposal (2026-09-21)

> **Status: PROPOSAL for operator ratification.** Amends [the 2026-09-20 checklist](2026-09-20-tradeify-deployment-checklist.md); it does not replace it. Every packet not named here keeps its 09-20 text, envelope and acceptance criteria. This amendment changes no portfolio, statistical criterion, authority, source-evidence requirement or operator GO; it adds one gate (T00), one tooling packet (T01b), and re-sequences work that the original already allowed to run in parallel. Ratify by merging this PR and ticking the decisions in §4; until then the 09-20 checklist governs.

## 1. Why amend now

S2 was accepted on 2026-09-21 (PR #436 ledger entry). Two facts from that work drive this amendment:

1. **Engineering is not the critical path.** T14 (production feed) is blocked on a provider and funding decision (Databento retired 2026-09-10, no replacement approved); T09 (real broker adapter) is blocked on the actual Tradovate order path; T07 (settlement) on real exports. None can start without operator decisions, and T15 cannot join until all three agree with the engineering. At the S2 pace the spine finishes in weeks and then waits.
2. **The Linux loop dominated S2's wall time.** About twenty hosted runs at ~25 minutes each; every packet needed two to five iterations. The suite grows past thirty nodes with S3. Cheap tooling (a labelled single-case diagnostic mode, two-host sharding, cached provisioning) was identified during S2 and deferred; it pays back inside S3's first iteration.

And one fact that predates S2: the bounded feasibility screen of 2026-09-09 returned **FRAGILE** — under a 10 % haircut on winning days no menu entry clears the 50 % pass floor, H1→H2 pass-frequency swings of +63 to −37 points with opposite signs across entries, and every "zero bust" result an EOD-clock lower bound. The deployment target has not been re-screened since. Building nine to thirteen million tokens of qualification machinery ahead of that answer is the wrong order.

## 2. New and changed packets

### T00 — Feasibility re-screen of the deployment target (NEW GATE; 250k–500k)
**Selected outcome:** A pre-registered, intraday-honest re-screen of exactly the expressions the checklist proposes to deploy, yielding GO (continue the spine as specified) or NO-GO (dispatch a portfolio-adjustment packet before T02). Neither outcome touches any locked parameter.
**Prerequisites:** the 2026-09-09 screen (`docs/superpowers/plans/2026-09-10-tradeify-feasibility-screen.md`, commit `69be794`; gitignored output under the phase-1 population worktree's `feasibility-screen/`, `screen.py`, 46 tests, `*-v1-preserved.*`); the canonical phase-1 ledgers (one `canonical_trades.csv` partitioned by `strategy_id`, in `codex/tradeify-joint-replay` @ `00b2bb7`); the real engine `core/mc/simulation.py::simulate_path` + `core/mc/preflight.py::firm_kwargs` with the intraday bust clock (standing lesson: EOD-only bust figures are lower bounds); the load-bearing-numbers owner for any quoted tier figure.
**Ownership:** coordinator dispatches one executor; **the operator ratifies the pre-registered floor and scenarios before the run** (strategy-validation discipline: the bar is fixed before the numbers exist and does not move after).
- [ ] Pin the deployment target: the exact "fixed four-strategy" expressions, captured sizes and allocations the checklist's Goal names (the 09-09 menu had seven entries; the four must be named by identity, not by description).
- [ ] Pre-register: pass floor per partition (full/H1/H2), the three scenarios (`unchanged`, `losses_x1.10`, 10 % winning-day haircut), the intraday-honest bust clock as mandatory, and the NO-GO condition — verbatim, in the packet, before execution.
- [ ] Re-run the screen with the intraday clock on the pinned target; retain `results.json`/`REPORT.md` under the private root; record digests.
- [ ] Return GO/NO-GO against the pre-registered condition only. On NO-GO: name what the numbers say (which legs, which seam) and stop; the adjustment is a separate operator-ruled packet (T00b), never an in-packet re-tune.
**Verification:** the existing 46 screen tests plus the intraday flag; every quoted figure bound to the pinned ledger digests. **Forbidden:** carrying EOD-clock "zero bust" forward as survival; moving the floor after seeing results; re-optimizing any expression.
**Return boundary:** a verdict and its evidence. No spine packet dispatches on a FRAGILE/NO-GO verdict; a GO verdict is a precondition for T02 and is cited in T15's F1.

### T01 — DONE (S2 accepted 2026-09-21)
Ledger entry "Coordinator acceptance — S2 budgeted admission and real Linux work supervision, 2026-09-21"; PR #436 merge gated on run 35555309697. B1–B6 as written are satisfied; nothing further.

### T01b — Linux evidence loop tooling (NEW; 100k–250k; before T02)
**Selected outcome:** an S3 iteration costs minutes, not a 25-minute fresh host, without weakening acceptance-grade runs.
- [ ] `workflow_dispatch` input `cases` (a `-k` expression) that runs a labelled **diagnostic** run: invariants are expected to fail (not every node present), the record carries `acceptance_scope=DIAGNOSTIC_SUBSET`, and `s2_run_evidence.py` refuses it as evidence. Single-case iteration in ~5 minutes.
- [ ] Shard the full suite across two fresh hosts by manifest node list (the OOM case last on its shard); the artifact-read script merges both records and requires both.
- [ ] Cache the provisioned venv and worker image as a keyed workflow cache; provisioning falls from ~7 to ~2 minutes; the host facts step still records the actual host.
- [ ] Keep the `s2-linux-run` skill and README section current.
**Verification:** one acceptance-grade sharded run fifteen green with both records; one diagnostic run refused by the evidence script. **Return boundary:** tooling only; no change to any registered node or assertion.

### T02 — S3 (unchanged scope; sequencing and ceremony amended)
The four design decisions were ruled 2026-09-21 (draft packet `docs/briefs/handoffs/2026-09-21-full-e1-s3-n1-genuine-capture-DRAFT.md`): new versioned campaign tables + one FULL_E1 checkpoint evidence family; G5 as a host transient unit under the work slice; the bootstrap-level readiness handshake for every payload + a bounded output mount + phase-limited BudgetGuard; release/v5 + profile/v5 opening N1 dispatch only. **Amended process:** one executor (GLM), one coordinator (Claude); exactly one design-freeze checkpoint (the C1 shape: head, line-1 record, interface table, fixture ledger, fail-on-base evidence) before the Linux run; **the schema family and the result/seal interfaces are frozen and published at that checkpoint** so T05 can start (§T05); one independent review at return. Predecessor: T00 GO + T01b.

### T03 / T04 — S4 / S5 (unchanged; sequential after T02)
They extend T02's checkpoint machinery to more stages and share its owners; no parallel writer.

### T05 — S6–S7 (AMENDED: parallel build, sequenced acceptance)
The result-commit and seal code consumes captures and assessments; it does not need N2 or Part A to exist to be built. **Start T05's build on an isolated branch when T02's checkpoint publishes the frozen schema family and interfaces**, with a named file boundary (its own modules and its own versioned tables; no edits to the service/store files T03/T04 are writing — a needed edit there is a CHECKPOINT to the coordinator). Accept T05 only after T04, against the real captures. The 09-20 text's "preparation of future tests on an isolated branch against explicitly agreed interfaces" is extended to implementation under that boundary.

### T06 — S8 (AMENDED: folded, not built)
Every slice registers its E01–E12 coverage as it lands (the slice's Linux cases are its E-cases; the manifest is the authority). T06 then consists of the integrated sharded run on the final candidate plus the combined independent review — its stated return boundary — with no separate build packet.

### External tracks — START NOW, not "alongside" (unchanged scope; sequencing amended)
- **T07** (settlement), **T08** (broker/protection feasibility), **T10** (real source and freeze packet) dispatch as soon as T00's pre-registration is ratified; they need no engineering predecessor.
- **T14** provider-neutral work (entitlement/cost/symbol/roll/session proposal, frozen equivalence criteria) dispatches now; provider-specific work waits on decision D-feed (§4).
- **T09** follows T08 and needs decision D-broker (§4).
- **T13** follows the incident-amendment ruling (the bounded platform-protection ADR is still Proposed).

### Review and ceremony (all packets)
Adversarial review stays — it found the two P2 findings and three resume races in S2 — but is batched: one independent review per packet at return, one coordinator checkpoint at design freeze, one ledger entry per packet. The Codex PR bot is at its usage limit; decision D-codex (§4) either funds it or accepts the in-session independent reviewer as the standing substitute. One writer per surface, always; the dual-executor overlap of 2026-09-20 is not to be repeated.

## 3. Amended dependency and dispatch summary

- **Gate:** T00 GO → spine. NO-GO → T00b (portfolio adjustment, operator-ruled) → T00 again.
- **Spine:** T01b → T02 → T03 → T04 → (T05 accepted) → T06 (integrated run + combined review).
- **Parallel with the spine:** T05 build from T02's freeze checkpoint; T07, T08, T10, T14-neutral from T00's ratification; T09 after T08 + D-broker; T13 after the incident ruling; T11 after T06; T12 prepares against T02's frozen interfaces, needs T06 + a timing answer before F1.
- **Join:** T15 (freeze, production E1, D0/D1) → T16 → T17 as written.

## 4. Operator decisions this amendment needs (tick to ratify)

- [ ] **D-T00** — ratify the T00 pre-registration (pinned four expressions, floors, scenarios, intraday clock, NO-GO condition) before the screen runs.
- [ ] **D-feed** — name the production feed provider (or the funding gate that must clear first); T14 provider-specific work is blocked until this is ticked.
- [ ] **D-broker** — grant the actual Tradovate/CrossTrade order-path access T09 needs (no agent places a trade; the adapter is qualified against real request/fill identities under the existing disarmed posture).
- [ ] **D-codex** — fund the Codex PR bot, or accept the in-session independent reviewer as the standing review for every packet.
- [ ] **D-sequence** — accept §2's T05 parallel build and §T06 fold.

## 5. Honest timeline

At the S2 pace (five packets, two days, multi-agent), with T01b landed first and T05 in parallel, the spine T02–T06 is roughly three weeks of agent work. The external tracks are bounded by the four decisions above, not by tokens. The four-firm program falsifier is dated 2026-11-08: a first attended Tradeify session before that date is plausible only if D-feed and D-broker are decided within the next week and T00 returns GO. If T00 returns NO-GO, the fastest path to a Tradeify deployment is the portfolio adjustment, and the spine should not be accelerated ahead of it.

## 6. Verification of this planning artifact

No new test-pass or capability claim is made. T00 is the only new acceptance gate; T01b is tooling; every other change re-sequences work the 09-20 text already permitted in parallel. Nothing here is a commit, merge, provider contact or deployment.
