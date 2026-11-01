# Strengthening the generation phase: failure census, pre-run screen, resources, throughput, supply — DRAFT

**Status:** DRAFT investigation for Joshua. It recommends; it decides, ratifies and edits nothing else ([Rule 3](../operational_rules.md#rule-3--the-operator-decides-grants-are-literal)). No gate, skill, locked surface or standing instruction was changed.
**Date:** 2026-11-01 · **Author:** Claude Code (cloud) · **Base:** `main` at `9d95503`; archive `first-passage-archive` at `a75a188` (shallow).
**Budget (Rule 2):** ≤6 iterations including one self-review; three read-only subagents (two census, one inventory) plus a coordinator pass; about $15 of agent compute; **K = 0** (no search, backtest or data read). Stopped within bound.
**Question (Rule 9):** which changes to generation raise the rate of viable, *distinct*, venue-native candidates per unit of elapsed time? Decision it feeds: what the builder rounds and the 11-08 research checks adopt next.
**Reading limits:** census rows marked † in the subagent returns rest on catalogue one-liners, not full RESULTS; categories are judgment calls (several efforts fit two). Counts are of efforts recorded in the two repos, not of every trial. No backtest dollars, prices, parameters or account data appear here ([AGENTS.md §Data movement](../../AGENTS.md#public-clone-posture)).

---

## 0. Orientation and dedup (Rules 0, 8)

Read: `AGENTS.md`, `STATE.md`, the generation skills, `strategy_harvest.md`, the 08-30 candidate-contract and evaluation-order ADRs, the EM screen spec, Q-KBUDGET-1, M-15 to M-25, M-46, M-49, M-50, the [10-24 subtraction ruling](2026-10-24-assumption-challenge-rulings-proposal.md#operator-ruling-joshua-2026-10-24), the [10-30 expansion ruling](../adr/2026-07-12-prop-portfolio-four-friendly-firms.md) (Addendum 2026-10-29, "Order of expansion"), the builder ([`lab/builder/README.md`](../../lab/builder/README.md), [R1 registration](../briefs/pre-registration/2026-11-01-builder-r1-mcl-orb-registration.md)), and the [11-08 research-checks prep](2026-11-08-research-checks-prep.md).

Dedup search (pasted):

```
$ rg -l -i -e "generation (phase|throughput|bottleneck)" -e "candidate supply" -e "effect-prior supply" -e "hit rate" docs lab/CATALOG.md PIPELINES.md STATE.md .claude/skills
docs/superpowers/specs/2026-09-01-three-speed-alpha-research-design.md
docs/spec/2026-08-06-mnq-daily-cadence-tight-daily-loss-target-spec.md
docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md
docs/notes/audits/2026-08-18-block-shuffle-placebo-does-not-control-for-tr-autocorrelation.md
docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md
docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md
docs/ltm/notes/archive/sessions/SESSIONS-2026-Q3.md
docs/briefs/programs/2026-08-18-step0-daily-geometry-mechanism-slate.md
docs/briefs/Q-VOLREGIME-1-intraday-bar-volume-regime.md
docs/briefs/Q-RANGEXFER-1-overnight-range-gap-magnitude-transfer.md
docs/briefs/closures/Q-KBUDGET-1-axis-reachability-screen.md
```

Nearest priors, and how this note differs:
- The [three-speed design](../superpowers/specs/2026-09-01-three-speed-alpha-research-design.md) (Vet → Generate → Confirm) is still `Proposed`. It shapes the funnel; it holds no census and no supply plan.
- [Q-KBUDGET-1 §4](../briefs/closures/Q-KBUDGET-1-axis-reachability-screen.md#4--lesson-candidates-dated-anchors-candidate-status-until-they-re-fire) already concluded that "the binding constraint on discovery has fully moved from statistics machinery to *effect-prior supply*" (2026-07-14). This note tests that conclusion against everything since and finds it holds.
- The [11-08 prep §3](2026-11-08-research-checks-prep.md#3-sourcing-channel-retirement-4-limb-2-first-starvation-check) recommends ruling that channel starvation is binding and that the builder is the response. This note supplies the evidence for that ruling and says what the response needs.
- The sibling [prop-firm microstructure study](https://github.com/Joshua-Asante/first-passage/blob/claude/prop-firm-microstructure-study/docs/notes/2026-11-01-prop-firm-microstructure-study-DRAFT.md) (branch `claude/prop-firm-microstructure-study`, unmerged) owns per-firm venue facts, cost tables and barrier geometry. This note links it and does not restate them.

---

## 1. Failure census

Two independent passes:
- **(A)** the current repo: `docs/briefs/closures/`, `docs/rejected_candidates.md`, `lab/CATALOG.md`, `discovery_manifests/`;
- **(B)** archive-only closures, RESULTS and preregs.

Each pass assigned every closed generation effort one primary cause. About 20 efforts appear in both passes, sometimes under different labels (DISC-CAMP-0: DEAD_AXIS vs NO_MECHANISM; H-OD-1: COSTS vs GATE_UNREACHABLE). So the passes are reported side by side, not summed into one exact total. Governance, ops and sizing closures are excluded (25 in A).

| Primary cause | (A) 65 rows | (B) 53 rows | Exemplars (citation) |
|---|---|---|---|
| GENUINE_NULL: well-posed test, no edge | 19 (+~25 hidden in grouped rows) | 18 | MSL-C1/C2/C3-K2 ([closures](../briefs/closures/)); MNQSR-1 0/14; TNEC CON-3..5; DL-1/DL-2 ([charter](../adr/2026-08-16-deep-iteration-lane-charter.md)) |
| **Pre-run arithmetic** (sum of the four rows below) | **18** | **18** | — |
| · COSTS_FILLS: published δ far under cost | 6 | 8 | H-ZNAUC-1, MYM-3FPS-1, D5, H-OD-1; "dominant null mode" ([ZN.md R3](../../ops/instruments/ZN.md)) |
| · INSUFFICIENT_SAMPLE: power or cadence at the realised N | 7 | 4 | MSL-S2A (cadence), ZF event ORB, buyback-blackout, Q-ICT-SWEEPFVG-1 |
| · DEAD_AXIS: DSR floor at K above any realistic edge | 3 | 4 | DISC-CAMP-0 / Q-GATECART-1 (K=3,177 → floor 2.05), Q-MNQSEL-1, H-FCCARRY-1 |
| · GATE_UNREACHABLE | 2 | 2 | Q-HARV-0 (M-49 anchor), Q-RANGEXFER-1, Aegis→6J Stage 1 |
| **Mechanism or supply dry** | **9** (NO_MECH 7, DOMAIN_BAR 2) | **9** (NO_MECH 6, SUPPLY_DRY 3) | MNQBASE-1, Q-TNEC-ENV-1 (54/56 cells empty), Q-INVENTORY-1, harvest deep search, VOLREGIME T0, Friday-DOW |
| **Venue rule or transfer** | **13** (VENUE 8, TRANSFER 5) | **3** | Q-TXG-1 walls, Guardian→MGC, Striker→MNQ, Q-COMPOSE-1, ORB-MNQ-1 payable leg, T00 / FLOOR-HALF |
| FEED_DATA, defect, confound | 3 | 2 | Striker→MYM (early-close bar), Q-OFCHAN-1 (7.36% coverage), MNQ15 (no input route), RANGECOND look-ahead (retracted after verdict) |
| PROCESS_OVERHEAD, duplicate | 3 | 3 | ORB-HC-1 (closed at spec review, untested), ST-EH-1 (operator-stopped at ~100 of 570 chunks), Q-USOIL-1 (parked 8 weeks, never run), Q-ICT-1 (moot) |

**$0-catchability.**
- (A): 37 yes, 7 partly, 18 no, 3 n/a. Of the 37, 14 were in fact killed by the repo's own Stage-0/Phase-0 screens. That leaves **23 efforts that ran, or were pre-registered, before a check that would have killed them for $0.**
- (B): 30 yes, 8 partly, 15 no.
- Nearly every "no" is a GENUINE_NULL, which is the honest cost of testing.

**The checks that would have caught them** (A; B is similar):

| Check | Efforts |
|---|---|
| detectability: DSR floor at K, power at N, gate reachability | 12 |
| mechanism statement | 8 |
| barrier feasibility or venue legality | 7 |
| published δ vs cost | 5 |
| feed or calendar availability | 3 |

**Recurring modes.**
1. **Pre-run arithmetic decided the outcome** (18 + 18 rows). Cost hurdle, power and the DSR floor were computable from cited inputs before any pull: M-19, M-20 and M-49 each record it. The K-wall study found the floor crosses the ratified cap at **K = 4** (`archive:lab/analysis/c1/catalogue_k_wall_2026-08-05/RESULTS.md`), so any catalogue beyond a handful of cells was dead on arrival.
2. **A saturated domain kept being re-mined.** Most GENUINE_NULLs are MNQ/MYM intraday OHLCV timing or order-flow cells. A raised domain bar has existed since 07-21 ([RC "Single-instrument index-futures intraday OHLCV directional timing"](../rejected_candidates.md)), and the 08-08 audit graded the object layer **Degenerating** with SNAG firing a second cycle (`archive:docs/notes/audits/programme-audit/2026-08-08-quarterly-audit.md#1--verdicts`).
3. **Supply ran dry at the mechanism requirement** (9 + 9). Sourcing for named counterparties returned zero admissible seeds repeatedly; there has been no harvest screen-PASS since 2026-07-16 ([prep §3–4](2026-11-08-research-checks-prep.md)).
4. **Edges treated as strategy-owned rather than strategy × venue × clock** (13 + 3). Every port into the Tradeify trailing barrier died on bust, not edge, including cells that passed cost (Striker→MNQ). The pattern runs from 07-16 (6J) to 10-19 (T00).
5. **Feed churn, and defects found after the verdict.** Four sources were retired: Dukascopy 06-17, OANDA 06-24, Pepperstone 08-02 (CFD panels deleted 08-03), and Databento 09-10. Each took its panels and re-pull paths with it ([Databento addendum](../adr/2026-07-10-databento-research-stack.md#addendum-2026-09-10---operator-retirement-of-databento)). RANGECOND flipped from RESOLVED to FALSIFIED after Codex found a look-ahead.

---

## 2. Minimal ordered pre-run screen

**Design constraint.** The [10-24 ruling](2026-10-24-assumption-challenge-rulings-proposal.md#operator-ruling-joshua-2026-10-24) says "don't create replacement machinery", and Rule 36 forbids a new layer without a decision. Every limb below already has an owner except P2's cross-firm and native clauses and P3. The proposal is **one ordered front-door pass that calls the existing owners, at generation-open, before K is ledgered**. It is not a new gate stack. The pass is cheapest-first and stops at the first fail. Each limb costs $0 and needs no data read.

| # | Limb (output) | Existing owner (no duplicate) | Past failures it would have caught |
|---|---|---|---|
| P0 | **Prior consult:** instrument × mechanism cell priors, register hits, domain bars. *Advisory under Rule 26: disclose, don't block.* | `scripts/instrument_profiles.py cell` ([profile index ADR](../adr/2026-07-25-instrument-profile-index.md)); [rejected_candidates](../rejected_candidates.md); Rules 8 and 27 | Q-ICT-1 (duplicate); the MNQ/MYM timing re-mines; Guardian→MGC (prior already DEAD) |
| P1 | **Mechanism statement:** who pays, when, why it survives, how it dies; or the 1b evidence-robustness path. | [harvest Req 1a/1b](../methodology/strategy_harvest.md#1-the-four-admission-requirements-all-mandatory-before-screening); [counterparty boundaries 2-A](../adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md); candidate-contract discriminator | Friday-DOW, ST-EH-1, DISC-CAMP-0, SLR-MYM-1, VOLREGIME T0, MOC wake |
| P2 | **Venue legality for the named target firm:** expressible natively (NinjaScript / Tradovate / TV-via-Tradovate for Tradeify); intraday-flat by the firm's flatten time; product offered; news and hold rules; **not the same strategy as one running at another firm**. | Firm facts: `core/firm_rules.py` and the [envelope](../../ops/prop_envelope_default.md) (Rules 16, 17). Native and exclusivity facts: [route record 10-12, 10-24](../briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md). **The cross-firm distinctness clause and the native-expressibility clause have no generation-time owner today.** | Index dispersion (options barred), Q-BTC-3, Striker→MYM (flatten bar), Track B (external engine barred at Tradeify) |
| P3 | **Feed availability:** the admitted canonical feed covers the instrument, bar size, window and session calendar the test needs. | Rule 18; [`core/data/bar_data/README.md`](../../core/data/bar_data/README.md); `tv_exports/cme/SHA256SUMS`. No pre-run check exists; it is a one-line lookup. | MNQ15 pilot, Q-OFCHAN-1, Striker→MYM candidate 1, the cross-index RV universe gap |
| P4 | **Detectability:** DSR floor at the declared K versus the best in-house edge and the corrected literature (M-19); confirm-power ≥ 0.50 at the declared N (Req 4); every close label reachable (M-25, M-49). | Harvest Req 4; `lab/research_utils/axis_screen.py`; eval-order step 1 (EM0); [gate-reachability-audit](../../.claude/workflows/gate-reachability-audit.js) workflow | DISC-CAMP-0, Q-GATECART-1, Q-HARV-0, Q-RANGEXFER-1, ZF ORB, buyback, COT, H-FCCARRY-1, Q-MNQSEL-1, ST-EH-1 |
| P5 | **Barrier feasibility:** the edge × frequency implied by cited shape priors against the firm's target-to-trail geometry and flatten clock. | [EM screen](../spec/2026-08-05-eval-mechanism-shape-screen.md) (Tradeify Select only); eval-order step 5 (shape priors); M-18 (finding stands; rule retired). For other firms' rows, see the sibling study §4. | Aegis→6J H-SOLO, Striker→MNQ, Guardian→MGC, ORB-MNQ-1 payable leg |
| P6 | **Cost and slip sensitivity, report-only:** net δ under 0 / 0.5 / 1 / 1.5 ticks of entry slip, in the gate's own units and price basis (M-16, M-20). *It does not kill: Req 5 was deleted 10-24. It is printed before trials so nothing is spent blind.* | [`cost_geometry_pregate.py`](../../scripts/cost_geometry_pregate.py) (report-only since 10-24); builder's 1-tick-per-side costing | H-ZNAUC-1, MYM-3FPS-1, D5, H-OD-1, FIXREV, US500 discovery, Q-TNEC-CON-2, MNQ-ANALOGUE-1 |
| P7 | **Risk breadth against the target firm's book:** `ρ` = candidate daily-$std / book daily-$std, and `n_eff_risk_delta` (M-21). | `lab/research_utils/breadth.py`; the [Stage-8 risk-N_eff ADR](../adr/2026-07-20-stage8-variance-dominance-risk-neff-gate.md) | Q-COMPOSE-1 |

**Coverage.** Census A's 37 "yes" rows map to P4 (12), P1 (8), P2 + P5 (7), P3 (3) and P0 (2), which is 32 rows. The other 5 are cost rows: P6 now prints them before trials but no longer kills them.

**What is new.**
- P2's cross-firm and native clauses are new because the 10-12, 10-24 and 10-30 facts post-date every generation owner.
- P3 is a lookup that was never written down.
- Everything else is **re-ordering**: today these limbs sit in five owners and fire at different stages (harvest admission, eval-order steps 1 and 5, compose prereg). The builder's own gates (5a–5g) run **after** cards are ledgered, so they spend K.

**Not proposed.**
- Re-introducing a cost kill.
- Any new threshold.
- Any change to the builder's frozen gates.

---

## 3. Resource inventory

| Resource | What exists (cited) | Constraint | Leverage | Use |
|---|---|---|---|---|
| CME TV bar exports | 10 `BAR_EXPORT_v0.2` files: six instruments (MNQ, MYM, M2K, MGC, MCL, 6J), exported 07-13 to 08-17 ([`SHA256SUMS`](../../core/data/tv_exports/cme/SHA256SUMS)); bytes gitignored | Only feed admitted (Rule 18). New instruments or windows need an **operator export** plus a SHA256SUMS delta (Rule 19). Cloud sessions can't read the bytes, so runs route local. | **High**: TV is an active subscription ([ledger](../../docs/pursuits/SUBSCRIPTION_LEDGER.md)), so each new instrument costs operator minutes, not money | **Underused.** No export since 08-17; no rates, FX-major, equity-index-other or metals-other symbol exported |
| `bar_data` M15 panels | 6 panels from 2022 on; MCL and M2K end 2026-07-02 ([README](../../core/data/bar_data/README.md)) | The pre-2022 depth is gone with Pepperstone; panels refresh only by fresh export | Medium: about 4 years limits power for event mechanisms (Req 4) | Used by builder R1 |
| External panels | COR3M, DSPX, S5FI, sector SPDR, COT gold ([README](../../core/data/external/README.md)) | Filed for a regime battery that closed NULL | Low to medium (conditioning only) | Idle |
| Retired Databento data | Operator-local caches only (MNQ 1m 2019–2026, MBP-10, ZN 1m) | Retirement addendum: "neither deletes data nor grants new rights". Use needs an operator ruling | Medium for depth and flow, but the rights are unclear | Not recommended now (§6 D6) |
| Strategy builder v1 | Ledger-first, hash-chained trials; ORB block library on closed 15m bars; gates 5a–5g; 70/30 split ([README](../../lab/builder/README.md)); R1 MCL ORB registered 11-01, K = 8 | Venue MC (5h), the Pine/NinjaScript compilers and Azure wiring are not built. Only ORB blocks exist. | **Highest**: the only live generator | Just started |
| Mining stack | `lab/discovery/miner.py` (stumpy, ruptures, catch22); `register_search.py`; pinned research environment | Blind mining is DSR-dead beyond K ≈ 4 (K-wall) | Low for selection; useful for **feature description** in Notice phase only | Idle since 08-29 (correctly) |
| Validation primitives | DSR, permutation, step-0 battery, breadth, axis_screen ([README](../../lab/research_utils/README.md)) | SPA, StepM and PBO dormant | High: they make P4, P6 and P7 seconds-cost | Used |
| MC engine | `core/mc/`, `core/portfolio_mc.py`; vendor-free regression | — | High for P5 per firm row | Used at deployment, not at generation |
| Negative knowledge | 59 register entries, 61 machine tags; 30 instrument ledgers; profiles matrix of 35 mechanisms × 27 instruments (47 DEAD, 19 PARKED, 3 LIVE, most cells untested) ([PROFILES.md](../../ops/instruments/PROFILES.md)) | Advisory since 10-30 (Rule 26). `mechanism_prior_tags.json` was never populated. | **High**: the untested cells *are* the supply map | **Underused**: consulted by exit code, not used to aim |
| Harvest channels | HARV ranks 1–6 ([§2.3](../methodology/strategy_harvest.md#23-ranked-channel-portfolio-replaces-the-old-screenability-only-tiers)); MSL closed; route B and the census retired 08-24 | Tier A (trend, carry, positioning) is mostly **multi-day**, and every firm forces intraday flat (§5) | Medium, and only if re-aimed at intraday mechanisms | Starved since 07-16 |
| Agent capacity | Claude cloud sessions, Codex review, Workflow (≤10 agents by default); seats in [`seat_authority.yml`](../../scripts/seat_authority.yml) | Cross-agent review; spend, scope and evidence-claim changes stay with Joshua | High for zero-K work (P0–P7 sheets, literature extraction, priors) | Spent mostly on spec and review loops (§4) |
| Azure VM | 32 vCPU, ≤12 h runs, weekly ceiling ([policy](../governance/azure-compute-vm-policy.md)) | Operator `az login`; private inputs only for §60-named runs; **public-only run rule still "Open"** | Low today: builder runs are cheap | Idle for generation |
| TV agent browser | Page-level reads at human cadence; no scripted automation; manual export only ([ADR](../adr/2026-07-27-tv-agent-browser-access.md)) | Pine never leaves to third parties | Medium: lets an agent check a symbol's history depth and session before asking for an export | Unused for generation |
| Native-platform constraint | Tradeify eval accepts NinjaScript, Tradovate or TV-via-Tradovate logic only; no bridges; no cross-firm reuse ([route record](../briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md)) | Binding for Tradeify; other firms' automation terms differ (sibling study §1.2) | **High as a design input**: closed-bar, single-instrument, order-type-simple logic ports to every native platform | Not a generation input today |

---

## 4. Throughput: where elapsed time goes

**Evidence**

| Effort | Idea → verdict | Where the time went |
|---|---|---|
| R2VBUCK / R2AGRUN / R2FLOW (08-08) | same day, two sessions each | operator GO between G0 and Explore |
| TNEC CON-1..5 (08-09 → 08-12) | 4 days, 17 session entries for five $0 cells | freeze, GO, ITERATE packet, branch election per cell |
| Q-TXG-1 (08-11 → 08-12) | about 8 entries | design, plan, block freeze, election, re-argument packet |
| DISC-CAMP-0 (07-11 → 07-13) | verdict clear on 07-13 | then Stage 4→7 drivers built for a zero-survivor traversal (PR #364) |
| Aegis→6J (07-16) | four prereg versions in one day | re-registration churn |
| Q-USOIL-1 (06-15 → 08-09) | about 8 weeks, never run | operator queue |
| MSL closure (10-07 → 10-25) | 18 days | operator queue |
| Q-SFCLEAR-3 (10-13 → 10-29) | 16 days, never run | spec, about 10 review folds, pause |
| ORB-HC-1 (→ 10-21) | closed untested | 3 Codex spec rounds |
| Native Aegis spec (10-26 → 10-28) | 13 versions, 12 Codex rounds; 24 dispatch attempts, 29 freeze records | [M-50](../methodology/lessons/methodology_lessons.md) |
| ORB horizon edition (10-30 → 11-01) | v11 READY; 4 registration PRs | version ceremony |
| **Builder v1** (10-30 → 11-01) | spec → engine PR in about 2 h → R1 registered; R1 draft clean on Codex round 2 | **the fast path** |

Sources: archive `SESSIONS-2026-Q3.md` and archive `docs/SESSIONS.md`, `docs/SESSIONS.md`, the closures above, and PR metadata. Git history in this clone starts 2026-10-10.

**Reading**

1. **Runs are cheap and fast** (hours, $0, small K). **Elapsed time is spent before and around runs**: spec and review loops, per-cell election packets, and operator-queue hops.
2. **The 08-08 audit counted 48 → 121 ADRs in 38 days with none removed.** The 10-24 subtraction began the reversal.

**Load-bearing for generation (keep, never lighten)**
- K ledgered before data (Rule 23);
- frozen criteria and holdout reserved before Explore;
- mechanical verdicts (Rule 24);
- generation never blesses (Rule 25);
- cross-agent review of a **registration** (Rule 5);
- every frozen control (Rules 10–15).

**Could be lighter at the generation stage, within those rules**
- **Per-cell operator GO inside an approved envelope.** Already deleted by the 10-24 ruling ("Routine permission requests for research steps inside an explicitly approved scope") and allowed by the [candidate contract](../adr/2026-08-30-candidate-contract.md#campaign-authority). What remains is to **use** it: one envelope per builder round (instrument set, K ceiling, windows, $0 data) approved once.
- **Per-cell election and ITERATE packets.** The builder's run spec plus its report.json carry the same facts. One registration per round, not per cell.
- **Spec review loops.** Stop on a recurring failure family, not a finding count (M-50, already recorded); for a registration, cap at two rounds before escalating. A clean round 2 is the observed norm for builder registrations.
- **Post-verdict build-out.** Don't build downstream drivers for a zero-survivor traversal (DISC-CAMP-0).

---

## 5. Distinct-edge supply

**Facts that shape supply**
- **Every automation-friendly firm forces intraday flat with no overnight or weekend holds.** Flatten times: Bulenox 16:59, Tradeify 16:45, MFFU 16:10, BluSky about 16:45 ET (`core/firm_rules.py` `weekend_holds: False` rows; sibling study §1.2).
  - Harvest's Tier A (trend, carry, term structure, positioning) is predominantly multi-day, so it is structurally hard to express at these venues.
  - **Mechanism class priority (harvest §2.1) is aimed at classes the venues cannot hold.**
- **Each firm needs its own strategy** (10-30 ruling). Scaling inside Tradeify adds accounts of one strategy; that is perfectly correlated, so it adds no breadth.
- **Breadth means different things at two levels:**
  - Within one firm's book, admissibility is risk breadth against a dollar-trailing barrier (M-21).
  - Across firms, each account has its own barrier, so cross-firm independence matters for **program-level correlated failure** and for the honest "distinct strategy" claim, not for any one barrier.
- **The canonical feed holds six instruments,** and the most-mined two (MNQ, MYM) carry a raised domain bar.

**Supply strategy (ranked by independent candidates per unit of effort)**
1. **Vary instrument × clock × mechanism together, not parameters.**
   - Two candidates are distinct when they differ in **at least two of**: asset class or instrument, the session window they trade (Asia, London, US-open, US-pm, event window), and the counterparty named in P1.
   - That is also the cheapest honest answer to Tradeify's exclusivity reading ([10-21 follow-up](2026-10-21-tradeify-native-followup-questions-DRAFT.md): "Different filenames, rewritten code or changed parameters cannot settle it").
2. **Intraday mechanisms with a named, constrained counterparty that recur daily** (power at about 4 years of 15m bars needs daily events; Req 4):
   - each product's own **opening auction** and its **liquidity handoffs**: equity cash open, COMEX metals open, NYMEX energy open, London open for FX futures;
   - **scheduled-release windows** where hedgers must act (energy inventory, rates and FX macro releases);
   - **end-of-session inventory flattening** by intraday participants, including the prop population itself, all forced flat at about the same minute (sibling study §2–3).
   - Each needs P6 cost sensitivity printed first: the census says published intraday effects are usually smaller than costs.
3. **New instruments before new parameters.** The untested cells in `PROFILES.md` and the instruments the firms list but the feed lacks (equity-index other than NQ/YM, rates, FX majors, metals other than gold) are where independence is cheapest. Product availability per firm is a P2 input, owned by the envelope and the sibling study.
4. **Native-first block design.** Closed-bar, single-instrument, stop/limit/market logic with a hard flatten time ports to NinjaScript, Tradovate and Pine alike. The builder's closed-15m-bar compiler already sits inside that envelope; keep new blocks there.
5. **Deprioritise** MNQ/MYM intraday OHLCV timing, blind wide mining, monthly-event mechanisms (presumptively dead at about 4 years: Req 4), and cross-instrument ports of a locked book (the Q-TXG-1 walls). All remain advisory priors (Rule 26), not bans.

---

## 6. Recommendations (ranked)

**Agent within existing authority** = zero-K, report-only or tooling work a card or the current task already grants; any repo change lands by PR with cross-agent review. **Joshua** = a scope, threshold, spend, data-rights or evidence-claim change (Rule 3).

| # | Change | Evidence | Speed / hit-rate effect | Cost | Reversible | Owner to amend | Who |
|---|---|---|---|---|---|---|---|
| 1 | **Run the P0–P7 pass as a report-only pre-flight on every builder card set and harvest seed, before ledgering.** One script that calls the existing owners and prints one sheet. | §1: 23 (A) efforts spent before a $0 check; §2 | Removes about half of historical deaths before K is spent; leaves K for live cells | About one agent session plus review; no new threshold | Yes (report-only) | `lab/builder/README.md` and builder spec (Joshua's); eval-order step 1 cites it | Agent builds it report-only; **Joshua** decides whether any limb blocks |
| 2 | **Widen the canonical feed by operator export:** add instruments the firms offer and the feed lacks, and refresh MCL and M2K. | §3 row 1; §5 item 3; MNQ15 and OFCHAN feed failures; supply concentrated on six symbols | Largest lever on *distinct* supply; breaks the MNQ/MYM saturation | Operator minutes per symbol; $0 marginal | Yes | `core/data/bar_data/README.md`; SHA256SUMS (Rule 19) | **Joshua** (operator export); agent prepares the symbol list with P2/P3 rows and uses TV page reads to confirm history depth |
| 3 | **Add a target-firm field and a distinctness declaration at generation-open** (P2): which firm the candidate is sourced for, and why it is distinct from any strategy at another firm (§5 item 1 test). | 10-24 and 10-30 rulings; the 10-21 follow-up | Prevents building an edge no second firm may run; aims supply per firm | Field plus one paragraph per round | Yes | [candidate contract](../adr/2026-08-30-candidate-contract.md) fields; builder card schema | **Joshua** (contract field); agent drafts |
| 4 | **Approve one generation envelope per builder round:** instrument set, K ceiling, windows, $0 data, report-only VM use for public inputs. No per-cell asks inside it. | §4: per-cell GO and election packets dominate elapsed time; 10-24 already deleted routine asks | Rounds stop waiting on the operator queue | One decision per round | Yes (envelope expires with the round) | [candidate contract §Campaign authority](../adr/2026-08-30-candidate-contract.md#campaign-authority) (no change needed); [VM policy](../governance/azure-compute-vm-policy.md) "Open" item | **Joshua** |
| 5 | **Re-aim the supply map:** a zero-K sheet ranking untested `PROFILES.md` cells by native-expressible intraday mechanism, daily event rate and feed availability; populate the mechanism-prior tags so register lessons aim, not just block. | §3 negative-knowledge row; §5 | Converts negative knowledge into a ranked queue; raises hit rate per round | One to two agent sessions | Yes | `ops/instruments/PROFILES.md` (generated); `mechanism_prior_extract.py` | Agent |
| 6 | **Re-tier harvest §2.1 for intraday-flat venues:** mark multi-day Tier A classes "venue-inexpressible unless an intraday expression is named", and promote daily-recurring intraday counterparty mechanisms. | §5 first fact; harvest starved since 07-16 | Stops sourcing effort on classes the venues cannot hold | Doc edit | Yes | [strategy_harvest §2.1](../methodology/strategy_harvest.md#21-mechanism-class-priority) | **Joshua** (methodology priority); agent drafts |
| 7 | **Cap registration review at two rounds, then escalate by failure family**, for generation registrations only. | M-50; ORB-HC-1; ORB horizon v9–v11; builder R1 clean on round 2 | Cuts multi-day loops | None | Yes | M-50 holder; [coordinator skill](../../.claude/skills/coordinator/SKILL.md) (skill edit = release) | **Joshua** (Rule 6 and 7 limits are his); agent applies M-50 already |
| 8 | **Verify venue facts at generation-open, not at deployment:** P2 reads `firm_rules` and the envelope; any [RV] row in the sibling study blocks only its own firm's candidates until re-read. | Census mode 4; M-24; drawdown-lock and EOD-clock corrections | Fewer late venue kills | Re-read per firm row (already scheduled 12-31) | Yes | `core/firm_rules.py`, envelope (Rules 16, 17) | Agent (reads); firm-row edits by PR |
| 9 | **Keep retired channels retired and Databento caches unused** pending an explicit rights ruling. | Retirement addendum; route B 0 for 4 | Avoids rights and feed churn | — | — | — | **Joshua** only if he wants depth or flow data back |

**Dependencies.**
- 1 needs no decision to start.
- 2 and 3 multiply the value of 1 and 5.
- 4 matters only once a second round is queued.

---

## 7. Decisions for Joshua

1. **D1:** Is the P0–P7 pre-flight report-only (recommended start), or do P1–P4 block a card set before ledgering?
2. **D2:** Which instruments to export next. An agent will bring a ranked list with each symbol's firm availability and history depth.
3. **D3:** Is a target-firm field and distinctness declaration required at generation-open (candidate-contract field)?
4. **D4:** Approve a standing per-round generation envelope, and close the VM policy's public-only run rule (or leave the VM out of generation).
5. **D5:** Re-tier harvest §2.1 for intraday-flat venues, and mark MNQ/MYM intraday OHLCV timing as a deprioritised domain (advisory, Rule 26).
6. **D6:** Whether the retained Databento caches may ever be used (default: no).

The 11-08 sitting already asks whether starvation is binding ([prep §3](2026-11-08-research-checks-prep.md#3-sourcing-channel-retirement-4-limb-2-first-starvation-check)). The census supports "yes", with the builder plus D1–D3 as the response.
