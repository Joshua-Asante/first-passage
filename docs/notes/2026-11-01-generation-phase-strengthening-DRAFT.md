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

---

## 8. Second pass (2026-11-03): the live generator's reach, the native target, the supply map

**Base:** `main` at `18e24bc` (builder 5h, search-wide K, holdout runner and W1 merged; microstructure study and venue-fact register merged).
**Budget (Rule 2):** ≤6 iterations; one read-only subagent; K = 0. Arithmetic only, from public inputs (K, session counts, the builder's own formula). No data, RESULTS or private prereg read.
**Reading limit:** R1's private pre-registration may already hold the disclosure in §8.1; this pass could not read it. Nothing here predicts R1's result.

### 8.1 Builder gate 5f sets a high floor at R1's K and window

**Mechanism (Rule 0).**
- Gate 5f passes when DSR ≥ 0.95 ([`gates.py`](../../lab/builder/gates.py) `THRESHOLDS`).
- `dsr()` takes the per-session series, with every development session included and a no-trade day counted as zero (`daily()`), and deflates against `SR0 = E[max of K] × √(1/(n−1))`.
- Under near-normal moments, a pass therefore needs a per-session Sharpe of at least `(E[max Z_K] + 1.645)/√(n−1)`. This is M-19's closed form, so it depends on K and years, not on trade frequency.
- R1 is K = 8 on 812 development sessions ([registration](../briefs/pre-registration/2026-11-01-builder-r1-mcl-orb-registration.md)).
- Reproduce with the standard library: `NormalDist().inv_cdf` plus the Euler–Mascheroni constant, as in `research_utils/deflated_sharpe.expected_max_sharpe`.

**Minimum annualised net Sharpe needed to pass 5f:**

| K | 812 sessions (R1 development, ~3.2 y) | ~4 y | ~8 y |
|---|---|---|---|
| 1 | 0.92 | 0.82 | 0.58 |
| 2 | 1.21 | 1.08 | 0.77 |
| 4 | 1.50 | 1.35 | 0.95 |
| **8** | **1.73** | 1.55 | 1.10 |
| 24 (e.g. `k_scope: ledger` after three 8-card rounds) | 2.02 | 1.81 | 1.28 |

**Probability that 5f passes, given the true annualised Sharpe** (812 sessions; normal approximation; 5f only, so every other gate lowers it further):

| True Sharpe | K = 1 | K = 8 | K = 24 |
|---|---|---|---|
| 0.85 (M-19's corrected published top-decile single strategy) | 0.45 | **0.06** | 0.02 |
| 1.0 | 0.56 | 0.10 | 0.03 |
| 1.5 | 0.85 | 0.34 | 0.18 |
| 1.83 (M-19's best in-house validated edge) | 0.95 | 0.57 | 0.37 |

**Reading.**
- At R1's K and window, the 5f floor (1.73) sits above the literature's top decile (0.85) and just under the best edge the programme has ever validated (1.83). That 1.83 is Aegis on the retired Pepperstone CFD panel. The ledger records the **futures-native best as about 0.89** ([MCL.md 2026-08-10b](../../ops/instruments/MCL.md)), which passes 5f at K = 8 about 7% of the time. [M-19](../methodology/lessons/methodology_lessons.md) calls an axis dead only when the floor exceeds *both*, so R1 is **not formally dead, but it is near-dead**: a top-decile real edge passes 5f about 6% of the time.
- The same arithmetic was disclosed before freeze for ORB reconstruction and ST-EH-1. [ADR 2026-07-12 §2.4](../adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md) still requires that disclosure in every campaign pre-registration. **The public R1 registration does not show it; whether the private draft does is for the coordinator to confirm.**
- This is the census's first mode (§1) recurring in the newest generator, from a cause the first pass missed. **The data window, not the search, now sets the floor.** The pre-2022 intraday depth went with the retired feeds (§3), so the admitted TV exports give about 4–4.6 years in total, and 70% of that goes to development.

**Levers, cheapest honest one first.** None of them touches 5f's threshold, which Rule 23 and the frozen controls keep binding.

1. **Years of history.** Going from 3.2 to 8 years cuts the K = 8 floor from 1.73 to 1.10. Candidate sources, **all unverified**, each needing an operator check or ruling (Rules 18 and 19):
   - deeper TradingView intraday history on the current plan;
   - NinjaTrader's historical data through the Tradeify connection (depth and terms of use unknown);
   - the retained Databento caches (rights ruling, D6).
   Bar size does not matter for n (the floor is per session), so a closed-bar logic on 30m or 60m bars could use longer exports if TradingView offers them.
2. **Few cards per instrument, mechanism-first.** At K = 2 the floor at 812 sessions is 1.21, not 1.73. **K is banked:** `ledger.k()` counts every distinct card ever logged on the instrument, and honest K (Rule 23) counts them whichever ledger file holds them. A later round on the same instrument therefore starts from its bank (MCL starts at 8 after R1), not from zero. Eight parameter cells of one block spend the instrument's budget for one hypothesis.
3. **Keep `k_scope: instrument` unless a round really shares one hypothesis across instruments.** `ledger` scope adds every instrument's bank to every card's K (the family-bank effect: Q-KBUDGET-1 L-cand-1). Instrument scope excludes other instruments' cards but does not reset the instrument's own bank.
4. **Pool one mechanism across weakly correlated instruments as one card.** An equal-risk pool of M legs with true Sharpe 1.0 at pairwise ρ = 0 reaches pooled Sharpe √M: power at K = 8 rises from 0.10 to 0.29 (M = 2) and 0.69 (M = 4). At ρ = 0.6 it barely moves (0.17 at M = 4). This works only across asset classes, not across equity-index micros [INF on strategy-return correlation].
   **Tension:** a pooled card is one strategy, so it supplies one firm, not several (§5).
5. **Test the mechanism, not only the payoff.** The candidate contract's independent [mechanism discriminator](../adr/2026-08-30-candidate-contract.md#contract-fields-and-freezes) is measured on its own observable (event counts, conditional moves), which can have far more power than the payoff Sharpe. Under the [terminal taxonomy](../adr/2026-08-30-evaluation-order.md#confirm-verdicts), a discriminator pass with a failed payoff is `EXPRESSION-FAIL`: the mechanism stands and the next round tries another expression of it. A clean discriminator fail is `MARKET-NULL` and stops the line. The builder's gates 5a–5g have no discriminator today, so every builder failure is silent on the mechanism, which wastes the census's main lesson (mode 3).

### 8.2 The native target is NinjaScript, so generate in it

**Facts.** For Tradeify evaluation accounts, the only fully automated native route is a NinjaScript strategy in NinjaTrader ([routes note](2026-10-13-tradeify-compliant-automation-routes.md), routes 1–3):
- Tradovate "has no strategy engine".
- TradingView's support says automated strategy trading with a brokerage account "is not available", which leaves Pine as a research and alert surface.
- Rithmic-side platforms are not named in the native-logic reply. The question is open ([deep-dive Q7](2026-11-01-tradeify-venue-deep-dive-DRAFT.md#62-questions-to-send-tradeify-one-message-joshua-sends)).

**Consequences for generation.**
1. **Every builder block should be NinjaScript-expressible on closed bars** with stop, limit or market orders and a hard flatten time. The builder's closed-15m compiler already fits; keep new blocks inside that envelope.
   Build the NinjaScript compiler before survivors queue, not after: a survivor without a native expression cannot reach a Tradeify evaluation.
2. **Research and execution feeds differ.**
   - Generation scores on TradingView CME bars.
   - A Tradeify evaluation fills on the platform simulator against its own feed ([microstructure study §2.2](2026-11-01-prop-firm-microstructure-study-DRAFT.md)).
   - For closed-bar logic the bars should agree, but session calendars, rolls and missing bars can differ (the W1 commit already counts missing bars).
   - **A per-instrument feed-equivalence spot check** (same sessions, TradingView export vs NinjaTrader history) belongs before a survivor goes to Joshua for the forward GO, not after.
3. **Distinctness is now cheap to state:** a different NinjaScript strategy class, instrument and session window, described in plain language Joshua can give unaided ([deep-dive §6.4 item 17](2026-11-01-tradeify-venue-deep-dive-DRAFT.md#64-research-and-modelling-each-needs-its-own-pre-registration-and-go-where-it-spends)).

### 8.3 Supply map (zero-K, from `ops/instruments/` and the register)

**Matrix** ([`PROFILES.md`](../../ops/instruments/PROFILES.md), 36 mechanisms × 27 instruments):

| Status | Cells |
|---|---|
| DEAD | 47 |
| AMBIGUOUS-PARKED | 19 |
| CONTINGENT-FORWARD | 1 |
| LIVE | 3 (all legacy, none with a venue) |
| untested | 902 |

The untested count overstates supply:
- Only **185** of the 902 untested cells sit on admitted-feed instruments.
- At least 11 cells marked untested were in fact tested or are in flight. Examples: MNQ compression, PDH/PDL and VWAP classes recorded in `MECHANISMS.md` but not in the matrix; 6J ORB falsified out of sample; MCL ORB is R1.
- The builder expresses one family today: ORB stop-breakout on closed 15m bars.

**Finding.** Of the 36 classes in [`MECHANISMS.md`](../../ops/instruments/MECHANISMS.md), only one records a WHO (expiry open interest: options market-makers, weekly). Across that catalogue and the register, **no alive cell is daily, intraday and has a named counterparty.** Every named-payer class is either:
- monthly or weekly: turn-of-month, carry, expiry open interest. Those are underpowered at about 4 years (harvest Req 4).
- dead where it is daily: MCL settlement ([RC](../rejected_candidates.md)), the gold fix.

So daily intraday candidates enter either through harvest Path 1b (evidence-robustness) or the no-counterparty channel, which caps declared K at 3. On the §8.1 arithmetic, that cap helps.

**Ranked cells** (all intraday-flat-expressible, daily, in the admitted feed, NinjaScript closed-bar expressible):

| # | Cell | Firms | Why it ranks | Nearest prior |
|---|---|---|---|---|
| 1 | MGC × prior-day high/low break (RTH) | T B F S | non-index, level-based not clock-based | MNQ CON-4 AMBIGUOUS-HOLD; MGC London fade FALSIFIED (opposite selector); Select 100K granularity wall ([MGC.md W5](../../ops/instruments/MGC.md)) |
| 2 | MCL × prior-day high/low break | T B F | MCL intake-dry rested on the deleted 4× multiple ([MCL.md 08-10b](../../ops/instruments/MCL.md)) [INF: reopenable] | MCL pullback-resumption FALSIFIED |
| 3 | MCL × compression-gated breakout | T B F | different cost geometry from MNQ; not ORB | MNQ gross-positive, net-negative |
| 4 | MGC × compression-gated breakout | T B F S | reopens a parked gold cell on the venue-legal contract | XAUUSD PARKED (spot panel deleted) |
| 5 | 6J × prior-session breakout continuation | T B F (full 6J only, no M6J) | Asia/London window; distinct from Aegis (mean reversion) | M6A infeasible; 12-contract cap |
| 6 | MCL / MGC × intraday momentum | T B F (S for MGC) | non-index | NQ/MNQ dead on post-2021 decay |

**Families that could each seed a different firm.** These sit in four different Tradeify product groups, so they also avoid the cross-account opposing-direction rule, which binds within a group ([envelope](../../ops/prop_envelope_default.md)):

| Family | Product group | Role |
|---|---|---|
| (a) US-open equity-index ORB | Equity Index | ORB-MNQ; Tradeify scales by adding accounts of it |
| (b) COMEX metals level and compression breaks | Metals | [INF] better at Bulenox or BluSky than Select 100K, because of the granularity wall |
| (c) NYMEX energy session breaks and momentum | Energy | R1 is ORB, so the next MCL card should be a different mechanism |
| (d) FX Asia/London continuation | Currencies | 6J now, M6E once exported |

Weakness: the counterparty of (a)–(d) differs only by asset-class microstructure. None names a payer, so each enters by Path 1b or the no-counterparty channel.

**Feed gaps, ranked by cells unlocked** [INF on counts]:
1. More years for the existing six (§8.1). MCL and M2K also end 2026-07-02.
2. **M6E**: offered at Tradeify, Bulenox and MFFU; BluSky's markets page (article 17115915, 2026-09-23) lists 6E but not M6E ([export ranking](2026-11-04-instrument-export-ranking-DRAFT.md); correction 2026-11-04). It removes 6J's full-size sizing problem.
3. Micro DAX (FDXM/FDXS): Tradeify only; the European session runs entirely before the flatten; outside the US-index raised bar.
4. M6A.
5. MES adds little: same product group as MNQ, and under the raised bar.

### 8.4 What changes in the recommendations

The second pass adds or reorders. §6 stands otherwise.

| # | Change | Evidence | Effect | Who |
|---|---|---|---|---|
| **A** (new, first) | **Put a reachability line in every builder round's registration:** 5f floor and pass probability at the round's K and session count against 0.85 and the futures-native best. Rounds whose floor exceeds both are re-scoped (fewer cards, longer data) before freeze. | §8.1; ADR 2026-07-12 §2.4 already requires the disclosure | Stops spending rounds whose survivor rate is a few percent | Agent: compute and draft per round. Re-scoping a frozen round is **Joshua's** |
| **B** (raises §6 #2) | **History depth before new instruments:** check what TradingView and NinjaTrader can export intraday, and how far back, for the six admitted instruments plus M6E. | §8.1 table: 3.2 → 8 years halves the floor's excess | Largest single lever on hit rate | Agent: TradingView page-level check of plan depth. Exports, and admitting a second source, are **Joshua's** (Rules 18, 19) |
| **C** (new) | **Treat each instrument's banked builder K as a budget:** few cards per instrument, from different mechanisms, `k_scope: instrument`. | §8.1 levers 2–3; §9.3 budget table | Keeps rounds inside reach | **Joshua** (round design is his spec) |
| **D** (new) | **Add a mechanism discriminator to builder cards**, so a failure says whether the mechanism or the expression died. | §8.1 lever 5; census mode 3 | Turns silent failures into aimed next rounds | **Joshua** (builder spec); agent drafts |
| **E** (new) | **Build the NinjaScript compiler before survivors queue; add a per-instrument TradingView vs NinjaTrader feed spot check** before a survivor's forward GO. | §8.2 | Removes a late, certain blocker | Agent within builder build steps already listed; the spot check needs the operator's NinjaTrader |
| **F** (sharpens §6 #5) | **Seed rounds 2–4 from §8.3 families (b)–(d), one firm each**, ranked cells first. | §8.3 | Distinct supply per firm, outside the saturated domain | **Joshua** picks; agent drafts cards |

**Decisions for Joshua added by this pass:**
- **D7:** Should every builder registration carry the §8.1 reachability line, with a re-scope rule when the floor exceeds both benchmarks?
- **D8:** History depth. Authorise the agent check, then decide exports or a second admitted source.
- **D9:** Builder round shape. *Decided 2026-11-03: see §10.1.*
- **D10:** Which §8.3 family seeds which firm.

---

## 9. Operator direction and delegated calls (2026-11-03)

### 9.1 What Joshua said, verbatim (2026-11-03, this session)

> "More years of data - I have Tradingview premium, which can give 15min bar data far in the past with the bar export tool, and the micro futures that we specialize in date back to 2019.
> Let's add M6E to the feed
> I trust your judgement on D7 and D8, let's discuss D9 and D10 further. Before we discuss, hand it to Codex to review"

**Contract launch dates bound the depth, whatever the plan allows** (web-checked 2026-11-03):

| Instrument | Trades from | Usable history | Source |
|---|---|---|---|
| MES / MNQ / MYM / M2K | 2019-05-06 | about 7.5 years | [CME launch release](https://www.cmegroup.com/media-room/press-releases/2019/5/06/cme_group_announceslaunchofnewmicroe-miniequityindexfutures.html), [CME FAQ](https://www.cmegroup.com/education/frequently-asked-questions-micro-e-mini-equity-index-futures.html) |
| MCL | 2021-07-12 | about 5.3 years; **stays the shortest-history instrument** | [CME MCL FAQ](https://www.cmegroup.com/education/articles-and-reports/micro-wti-crude-oil-futures-faq) |
| MGC, 6J, M6E | older contracts | depth set by what TradingView returns; measure at export | — |

M6E: 12,500 euros, tick 0.0001 = $1.25 ([CME contract specs](https://cmegroup.com/trading/fx/e-micros/e-micro-euro_contractSpecs_futures.html)). It is a Rule 17 quote to re-read when it is encoded.

### 9.2 D7, decided by Claude under Joshua's delegation

**Rule.** Every builder registration states the 5f floor at its K and development-session count, and the pass probability for a true Sharpe of 0.85 (the literature's top decile) and 0.89 (the futures-native best, [MCL.md 08-10b](../../ops/instruments/MCL.md)).

- **Reachable** means the floor at **banked K** (the instrument's distinct builder cards already logged, plus the round's new cards, under `k_scope: instrument`) is ≤ 0.89. A futures-native-best edge then passes at least half the time. This is M-19's test with the in-house benchmark set to the futures-native best.
- If a round's floor is above 0.89, it is re-scoped **before freeze**: fewer cards, a longer window, or pooling.
- If it still cannot reach, the registration says so in one line, and Joshua decides whether the round's other value justifies it (as ST-EH-1 did).

**Why this layer.** [ADR 2026-07-12 §2.4](../adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md) already requires the disclosure. The rule only fixes the benchmark and the action, so no new gate is added and 5f's threshold is untouched.

**Durable fix.** A report-only `reachability(k, n)` line in the builder's run report, computed before any card is evaluated. D9 is now decided (§10.1), so it can land by its own PR.

**R1** is **not run as pinned** (Joshua, ruled 2026-11-03, recorded effective 2026-11-08: [registration status note](../briefs/pre-registration/2026-11-01-builder-r1-mcl-orb-registration.md)). Its re-registration on the current engine is owed and is a new freeze, so this rule applies to it. At K = 8 on MCL with D9's holdout it would not be reachable (floor 1.59; 9% pass at 0.89). At K = 1 it is (0.84; 54%). Joshua agreed on 2026-11-04 to re-scope it to one MCL card (§11).

### 9.3 D8, decided by Claude under Joshua's delegation

**Use TradingView Premium only, at full 15m depth. No second source.**
- NinjaTrader history and the Databento caches stay closed; D6 stays "no".
- Re-export the six admitted instruments, each from its contract start or TradingView's limit, whichever is later. Add M6E.
- Each export is an operator act and lands as follows. The export session must run locally, because cloud checkouts lack the CSV bytes.
  1. Run the BAR EXPORT v0.2 exporter on the symbol at 15m (`M6E1!`, `MNQ1!`, `MYM1!`, `M2K1!`, `MGC1!`, `MCL1!`, `6J1!`), with as many year-pages as the row limit needs.
  2. Validate **each instrument's complete page set in one call**: `scripts/validate_bar_export_v2.py --in <every page for that symbol> …`, with the combined `--expected-unique-bars` and first/last open. The validator only detects conflicting overlaps among pages passed together. The refresh path (`core/bar_export_loader._parse_pages`) silently keeps the last duplicate, so page-by-page validation could hide a disagreement.
  3. **The CSV bytes stay local.** They are gitignored (`.gitignore`: `core/data/tv_exports/**/*.csv`, `core/data/bar_data/*.csv`), and AGENTS.md's public-clone posture forbids committing vendor CSVs. Commit only the `SHA256SUMS` delta (and refreshed panel sidecars), in the same commit as the data change on disk, with hooks installed (Rule 19).
  4. **M6E only, in that same landing** (create-on-touch: [profile-index ADR §2b](../adr/2026-07-25-instrument-profile-index.md); the loader's own "extend when a new symbol's export lands"):
     - the `PRICE_COL_BY_INSTRUMENT` entry in `core/tv_export_loader.py`;
     - the `INSTRUMENT_SPECS` row in `core/instrument_specs.py`, with the CME quote;
     - `ops/instruments/M6E.md`;
     - a regenerated `PROFILES.md`.
     Nothing is added before the bytes exist.
- Refresh the `bar_data` M15 panels and their sidecars from the new exports.
- **Extend the admitted calendar before evaluating any pre-2022 session.** The builder refuses any session outside `ops/calendars/cme_holiday_calendar_2022_2026.json`'s coverage window (`lab/builder/data.py` `Calendar`, coverage 2022-01-01..2026-12-31; [README](../../lab/builder/README.md) "Frozen calendar"), so deeper exports alone unlock nothing.
  - The extension is a new calendar file (or version) under the same `cme_holiday_calendar/v1` schema, reaching back to each window's start: 2019-05 for the equity micros, further for MGC, 6J and M6E.
  - It needs the same kind of operator acceptance the current file got ([calendars README](../../ops/calendars/README.md), D19, scoped to date membership).
  - The current file has equity, metals and FX columns but no energy columns. The builder reads only `entries[].date`, so this matters only if a consumer starts reading per-group status.
  - R1 keeps its pinned calendar (Rule 23).
  - Flagged on the PR by the operator's comment of 2026-11-03.

**Recomputed reach** on the real windows. Each cell is the 5f floor / P(pass | true 0.89), with the normal approximation:

| Window | Split | K = 1 | K = 2 | K = 4 | K = 8 |
|---|---|---|---|---|---|
| Equity micros, ~7.5 y | 70% development (current spec) | 0.72 / 0.65 | **0.95 / 0.45** | 1.18 / 0.26 | 1.36 / 0.14 |
| Equity micros, ~7.5 y | all development, forward confirm | 0.60 / 0.79 | **0.79 / 0.61** | 0.99 / 0.40 | 1.13 / 0.25 |
| MCL, ~5.3 y | 70% development | 0.85 / 0.53 | 1.12 / 0.33 | 1.40 / 0.16 | 1.61 / 0.08 |
| MCL, ~5.3 y | all development, forward confirm | 0.71 / 0.66 | 0.94 / 0.45 | 1.17 / 0.26 | 1.35 / 0.15 |
| ~10 y (MGC / 6J / M6E if TradingView reaches) | 70% development | 0.62 / 0.76 | 0.82 / 0.58 | 1.02 / 0.37 | 1.17 / 0.23 |

**Reading under D7** (floor ≤ 0.89 at banked K). This is the **total builder budget per instrument**, not per round:

| Window | 70/30 split | All history for development, forward confirm |
|---|---|---|
| Equity micros, ~7.5 y | **K = 1** | K = 2 |
| MCL, ~5.3 y | K = 1 (taken by R1's re-registration, §11) | K = 1 |
| ~10 y (MGC / 6J / M6E if TradingView reaches) | K = 2 | K = 4 |

With the current 70/30 split, each equity micro supports **one** honest builder card under D7, and a 10-year contract two. K = 8 is not reachable on any window. MCL, R1's instrument, has one look, which R1's re-registration takes (§11). **The round-shape question (D9) is therefore mostly a budget-allocation question: which single look per instrument is worth spending, and whether to buy more looks with a forward confirm or with pooling.**

## 10. D9 and D10: the discussion frame (no decision taken)

### 10.1 D9: the shape of a builder round — DECIDED 2026-11-03

**Joshua, 2026-11-03, verbatim:** "go with your recommendations on D9".

**Why.** `ledger.k()` banks every card ever run on an instrument, and D7 sets reach at floor ≤ 0.89, so each instrument has a small **lifetime** budget of looks. The budget depends on development sessions. Under the old 70/30 split, the holdout share was what cost looks, not the holdout itself. Arithmetic is the §8.1 closed form, with development sessions = total sessions − 378.

| Development / holdout | Equity micros (~7.5 y) | ~10-year contracts | MCL (~5.3 y) |
|---|---|---|---|
| 70/30 (R1's shape) | 1 look | 2 looks | 1 (R1's re-registration, §11) |
| **Fixed ~18-month holdout (~378 sessions), decided** | **2 looks** (development ≈ 1,512) | **3 looks** (≈ 2,142) | 1 (R1's re-registration, §11) |
| All development, forward confirm | 2 looks | 4 looks | 1 (R1's re-registration, §11) |

A forward confirm buys nothing over the fixed holdout for the equity micros. It also needs the NinjaScript compiler, and matching a 378-session holdout takes about 18 months of forward trading. It stays a later stage, not the confirm.

**Decided package** (applies from R2; R1 is unchanged):
1. **Holdout = the last ~18 months (~378 sessions) of each instrument's pinned export,** set through the run spec's date-pinned `split: {dev_start, dev_end, holdout_end}`. This is a registration choice: no engine or `THRESHOLDS` change. The holdout is looked at once per survivor, as the builder already enforces.
2. **One card per instrument per round, each a different mechanism.**
   - Mechanism-first, with one pre-committed parameter set and no grid.
   - Plateau robustness comes from the 5d ±1-step neighbours. They are simulated only as a kill check and never ledgered or selected among (`gates._plateau`, `cards.neighbours`), so they cost no K.
   - Each round spends one look per instrument and **keeps the next in reserve**.
3. **One mechanism discriminator per card, report-only for now.** It is declared at registration with its observable, null, direction and threshold (candidate-contract field). A result says whether the mechanism or the expression failed, which aims the reserve look. Making a clean discriminator fail terminal is a later decision.
4. **`k_scope: instrument`.** A pooled multi-instrument card is allowed only by explicit registration choice and spends one look on **each** instrument it touches. Whether a pooled card can supply a firm is D10's question.
5. **The D7 reachability line in every registration:** the 5f floor at banked K plus new cards, and the pass probability at true Sharpe 0.85 and 0.89.
6. **R1** is re-registered on the current engine as **one MCL card** (Joshua: not run as pinned, 2026-11-03; re-scoped to one card, 2026-11-04; §11). That card uses MCL's single look.

**Owners and next steps.**
- Items 1–5 are applied by each round's registration, in the form of the [builder round template](../briefs/pre-registration/TEMPLATE-builder-round.md). R2's is the first.
- The report-only `reachability(k, n)` line in the builder's run report (D7's durable fix, §9.2) lands by its own PR.
- The pre-2022 calendar extension (§9.3) gates any 2019-onward window.

### 10.2 D10: which family seeds which firm

**Inputs:**
- the §8.3 families and their product groups;
- per-firm product availability (§8.3 ranked cells; [venue-fact register](2026-11-01-prop-firm-venue-fact-register-DRAFT.md));
- §9.3 reach by history;
- the 10-30 rule: one strategy per firm; Tradeify scales by accounts.

**Rulings so far:**
- Joshua, 2026-11-03, verbatim: "For now we are not letting index stay Tradeify only. But we'll reevaluate when we expand to other firms."
- The cross-firm hedging control still applies whenever index books run both at Tradeify and elsewhere (Tradeify ESA §6.7(c),(i); [deep-dive](2026-11-01-tradeify-venue-deep-dive-DRAFT.md#1-what-changed-in-the-picture) item 5). They must never hold opposite directions at the same moment.

**Deployment order** (Joshua, 2026-11-04, verbatim: "go with your recommendations on both"):
- **Tradeify first, for now.** The 10-30 order of expansion stands. The [venue-terms note](2026-11-03-cross-firm-exclusivity-and-account-caps-DRAFT.md) (PR #1040) found Bulenox, MFFU and BluSky silent on running one strategy at several firms, and Futureify permissive only for copying in. No current BluSky page states that automation is permitted. Silence is not permission (Rule 17).
- **Reopen trigger.** Revisit the order when both hold:
  - at least two of Bulenox, MFFU, BluSky and Futureify confirm in writing that a user-built automated strategy may run there while the same strategy runs at another firm, and that automation is permitted on that route;
  - a book has passed its holdout.

  The upside is slots: one book gets 5 at Tradeify (8 with V2 Select 300K), against 16–18 across the other four (note §3).
- **Owed by Joshua** (agents never contact firms): send the support questions in note §4, plus one for Tradeify: does the same logic on a different instrument count as a distinct strategy? Joshua has ruled on that question ahead of the answer (below); it is still worth sending, and a contrary written answer reopens the ruling.

**Distinct books** (same ruling):
- A book is distinct from one running at Tradeify if its trading logic differs, or if it trades a different instrument (next bullet). Different sizing, risk limits or weights alone do not make it distinct (Tradeify, 2026-10-08: "Using the same bot across multiple firms is against policy, even if risk limits, sizing, or weights differ"; quoted in note §1.5).
- D4b's reading, "Portfolios adapted to each firm's rules are treated as distinct strategies" (2026-09-28, relayed; [origin log](2026-10-15-deployment-decision-origin-log.md)), is retired where "adapted" means sizing or weights only.
- **Different instrument** (Joshua, 2026-11-04, verbatim, relayed by the merge-train conductor: "A different instrument counts as distinct, we can safely infer"; asked whether to wait for Tradeify's written answer, he chose "Rule it now"). The same logic on a different instrument counts as a distinct strategy for Tradeify's exclusivity rule. The same logic on the same instrument at another firm stays prohibited.
  - This supersedes the interim reading recorded earlier on 2026-11-04 (#1076), under which the same logic on a different instrument counted as the same strategy.
  - It is an explicit exception to Rule 17's broad reading of venue silence. It rests on Tradeify support's 2026-10-12 reply (note §1.5): "If you write distinct strategies (different logic) running on one privately owned engine, you may use some exclusively on Tradeify and others elsewhere, as long as the strategies used on Tradeify are not used at other firms". Tradeify has not confirmed the instrument case in writing.
  - Consequence: R1's MCL ORB is no longer barred from seeding another firm on distinctness grounds. The reopen trigger above still applies: written confirmations from two of the other four firms, and a passed holdout.
  - The cross-firm hedging control still binds distinct books (above), including correlated products at BluSky.

**Family-to-firm mapping.** The FX rows were decided by Joshua on 2026-11-04 ("go with your recommendations on both"); the rest stays proposed. The deployment order is set above (Tradeify first, with a reopen trigger).

| Firm | Family | Why | Watch |
|---|---|---|---|
| Tradeify | US-open index ORB | in flight; native NinjaScript | first in the deployment order (2026-11-04) |
| BluSky | Metals: MGC, proposed | MGC offered; full automation welcomed | **R2 skips MGC** (Joshua, 2026-11-04): both MGC dossiers fail harvest Req 1, and the no-counterparty channel was not used |
| MFFU | FX: **6J** (decided 2026-11-04; the Tokyo-fix card is held with R2, see §11) | R2's card ([R2 dossier index](../briefs/dossiers/R2/INDEX.md)); avoids MFFU's funded metals cap | 6J full-size only; venue legality re-checked for MFFU in the dossier |
| Bulenox | FX: **M6E pre-fix** (decided 2026-11-04) | cheapest M6E costs ($0.50/side; MFFU $0.72, Tradeify $0.80, per `core/firm_rules.py` comments); a micro suits the harsh intraday-high trail | enters only after the M6E landing and if its pre-registration answers the EUR/USD fix-reversal re-proposal bar |
| FXIFY | later | rules provisional | — |

**Open questions:**
1. Energy: MCL's one look goes to R1's re-registration, which is ORB. Answered by the different-instrument ruling above: an MCL ORB is distinct from the index ORB, so distinctness no longer bars it from another firm.
2. Is a different instrument enough distinctness under Tradeify's rule? Ruled yes by Joshua (above), ahead of Tradeify's written answer, which is still owed.

---

## 11. Updates, 2026-11-04

**Exports landed** (operator, 2026-11-03). There are 91 annual BAR EXPORT v0.2 pages, gitignored, none committed. Spans are in New York time; every final bar is at 16:45:

| Symbol | First bar | Last bar | Pages |
|---|---|---|---|
| MNQ1! / MYM1! / M2K1! | 2019-05-05 | 2026-11-02 | 8 each |
| MGC1! | 2010-10-04 | 2026-11-02 | 17 |
| MCL1! | 2021-07-11 | 2026-11-02 | 6 |
| 6J1! | 2001-01-22 | 2026-11-02 | 26 |
| M6E1! | 2009-03-23 | 2026-11-02 | 18 |

- The operator reports 2,016,728 bars validated with zero errors by a local script.
- The repo validator run (§9.3 step 2), the `SHA256SUMS` delta and the M6E landing are owed to a local session. That run, not the local script, is the verification of record (Rule 21).

**Calendar.**
- Coverage stays **2016-01-01..2026-12-31** (Joshua, 2026-11-03: "Keep 2016, and go with option B"; PR #1045). For 2009–2015, the third-party encodings disagree on 3–8 dates a year, against 0–1 from 2016, so those years need CME's primary advisories, which the cloud cannot reach.
- **Option B** (PR #1048): the builder closes a calendar date only when at least one recorded status is not `NORMAL`. It fails closed on a missing or unknown status, so the 20 informational 2022–2026 rows become traded sessions.
- The reachability line (D7's durable fix) merged as PR #1042.

**Lifetime builder looks per instrument under D7 and D9** (#1045 and #1048 merged):

| Instrument | Usable window | Looks |
|---|---|---|
| MNQ / MYM / M2K | 2019-05 → 2026-11 (~7.5 y) | 2 each |
| MCL | 2021-07 → 2026-11 (~5.3 y) | 1 (R1's re-registration) |
| MGC / M6E / 6J | 2016-01 → 2026-11 (~10.8 y; the calendar binds, not the export) | 4 each |

Pre-2016 depth (MGC to 2010, M6E to 2009, 6J to 2001) would raise those budgets steeply. It needs a primary-sourced calendar extension first.

**R1** (Joshua, 2026-11-04, agreeing to the recommendation):
- The owed re-registration is re-scoped to **one MCL card** so that it is reachable under D7.
- The card is chosen and justified **before** any result, from the registered eight and by stated rationale, never by outcome (Rules 23, 25).
- Recorded at the owner: the [registration's status note](../briefs/pre-registration/2026-11-01-builder-r1-mcl-orb-registration.md).

**R2 composition** (Joshua, 2026-11-04, "go with your recommendations on both"), recorded in the [R2 dossier index](../briefs/dossiers/R2/INDEX.md) (PR #1061):
- 6J Tokyo-fix (post-fix leg) was chosen as R2's card. Its spot USD/JPY cohort is admissible under [strategy_harvest §4a](../methodology/strategy_harvest.md#4a-spot-cohorts-for-same-pair-cme-fx-futures-ruling-2026-11-04).
- M6E pre-fix enters only after its landing, and only if its pre-registration clears the fix-reversal bar. Its spot EUR/USD cohort is admissible under the same §4a conditions.
- MGC is skipped.
- No index card: MNQ, MYM and M2K hold. The overnight drift has decayed since 2021 (NY Fed, 2026-07-01), and intraday momentum is underpowered.

**R2 held** (Joshua, 2026-11-04, verbatim: "go with option a, hold R2"). No R2 look is spent. Three reasons:
- **6J fails on costs.** The MFFU venue re-check on PR #1061 found every 6J leg net negative at the builder's frozen 1 tick/side slip (`THRESHOLDS["5b_slippage_ticks_per_side"]`, 2 ticks round trip). The post-fix leg breaks even only below about 1.8 ticks of total round-trip slip.
- **M6E is worse:** 0.7–1.0 tick of slip consumes it.
- **The builder can't express either cell.** It has only ORB blocks.

So running R2 would have spent one of 6J's lifetime looks on a card the arithmetic already fails (census mode 1). The next dossier wave is re-aimed:
1. Rank cells by **cost headroom**: the cited per-event effect in ticks against all-in round-trip cost (commission plus 2 ticks of slip at the target firm). Then check power at the instrument's look budget.
2. Include M6A and MES (chosen for export, 2026-11-04).
3. Prefer mechanisms the builder can express, or ones that justify building a new block.

**R3 found no card** ([R3 index](../briefs/dossiers/R3/INDEX.md), PR #1066). All 28 cells fail cost headroom or power, so every lifetime look stays in reserve.

**Dossier-wave entry test** (Joshua, 2026-11-04, verbatim: "yes to the R3 entry test and the §11 pointer PR"). A new dossier wave runs only when one of these holds:
- A cited cohort meets [R3's frontier](../briefs/dossiers/R3/INDEX.md#the-trade-off-in-one-line-per-instrument): a haircut per-event mean of at least 1.5 × all-in round-trip cost, with δ/σ at or above the instrument's power break-even. At the break-even that means a multi-hour or full-session window on an index micro or MGC; a higher-δ/σ signal qualifies on a shorter window.
- Fill evidence shows an FX fix leg can trade within the slip its R3 row allows.

The test is K = 0 arithmetic, run before any dossier is written (census mode 1).

**Gate-stack calibration** (K = 0, synthetic; [RESULTS](../../lab/analysis/_inbox/builder_power_2026-11/RESULTS.md), PR #1067):
- **Series layer** (5a, 5c, 5f and the holdout look; no 5d or 5e): 5c binds. At S = 0.89 the series pass rate sits below the 5f closed form by 0.09–0.27 at K = 1 and 0.01–0.15 at K = 2 on 1,510 sessions (0.43–0.61 and 0.36–0.50, against 0.70 and 0.51), and by 0.10–0.36 and 0.03–0.23 on 2,350 sessions (0.50–0.76 and 0.48–0.68, against 0.86 and 0.71). At K = 4 it can sit slightly above. D7's reachability line stays a 5f-only disclosure; these figures do not estimate R1's full-stack pass probability.
- **Bar layer** (one synthetic MNQ card and generator, with 5d and 5e): the whole stack passes at most 1% at every true Sharpe tested, almost entirely because of 5e. The owner's generator limits apply.
- On that card and generator, 5e almost never passes (look-ahead through the realised side). The T1/T2 diagnostic ([PR #1072](https://github.com/Joshua-Asante/first-passage/pull/1072)) found the production statistic passing 3/400 paths per cell, with strong side-rule sensitivity; its V2 check failed, so no valid zero-edge null was measured. Neither result predicts R1.
- **5e ruling.** Joshua, 2026-11-04, gave two rulings: "go with (a), make 5e report-only for breakout cards" (to the #1072 session), then "go with your recommendation on 5e, window slide" (to this note's session). Asked which holds, he chose "Window slide replaces". A same-day window-slide placebo (lesson M-17) stays a kill gate for every card; the report-only branch is dropped. The production owner is [PR #1074](https://github.com/Joshua-Asante/first-passage/pull/1074), and R1's re-registration pins its engine.
- 5g placement rarely clears at latent book correlation 0.3. Open: whether its cap should be read against its independence baseline.

**Deployment bar** (K = 0, synthetic; [firm atlas RESULTS](../../lab/analysis/c1/firm_feasibility_atlas_2026-11/RESULTS.md), PR #1069):
- With risk sized to the drawdown allowance, the profit-target ÷ drawdown ratio decides feasibility, and bust, not pass, binds.
- Nothing clears the bust ceiling at 0.05 R net per trade or less. A low-win-rate breakout family needs about 0.20 R net.
- Bulenox is excluded from the lookup: the engine does not model its intraday-high trail.
- Inference: because feasibility barely differs by firm, D10's deployment order (§10.2) turns on venue terms and costs.

