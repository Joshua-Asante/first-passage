# STATE — First Passage

**Last curated:** 2026-08-18

This file is the **open-threads + forward-obligation register** — cross-session
items with no other home, plus the forward-trigger board. It is **not** a state
snapshot: it carries no risk %, MC anchor, strategy version, hash, working-tree
status, or canonical-owner table. Those live with their owners — see
[`docs/operational_rules.md`](docs/operational_rules.md) §7.

For uncommitted work: `git status`. For history: `git log`. For session narrative
and the live **Open / next**: [`docs/SESSIONS.md`](docs/SESSIONS.md) (read its top
entry first).

**Anti-accretion (standing):**

- New operator decision → **a concise decision-index entry** + owning ADR
  (never a paragraph here) — relaxed 2026-08-19 from a strict one-line cap;
  concise still means no multi-sentence narrative, see
  [`docs/operational_rules.md`](docs/operational_rules.md) Rule 7 edit log.
- Item leaves the queue or closes → **delete the STATE row**; do not leave
  “Cleared …” footnotes.
- Forward triggers: date/criterion + owner link only; detail stays with the owner.
- Retention test for every row: *open or still owed, and no other home.* If either
  fails, it leaves.
- **Entry classes + 40-word cap (W5 direction):** Decision / Build / Measurement /
  Hygiene — see [`W5 ADR`](docs/adr/2026-08-07-w5-governance-diet.md); prefer links
  over prose.

---

## OPERATOR QUEUE — strictly ordered, ≤5 live items

**Agent-hours are cheap and budgeted (K-ledger, cost dry-runs, $700 spend ceiling);
operator-hours are the binding resource and were the only unrationed one.** This
board is the sequencing fix: the next operator-attention items in dependency order,
so they are not served in whatever order the week happens to present them.
**Pointers only** — each item's owner artifact holds the detail (Rule 7).

**Standing rule: new decision packets, advisor triage, and sizing questions queue
BEHIND this list.** Items leave when done; it stays ≤5 so it cannot decay into a backlog.

> **This cap IS the portfolio-level Survive bound** (ruled 2026-08-09,
> [`ADR`](docs/adr/2026-08-09-survive-bound-is-the-queue-cap.md)). The bound is
> **concurrency-denominated, not hours-denominated** — Rule 2's §5 forbidden move #2
> bars expressing a budget in wall-clock "anywhere in canon or ADR" (*"neither client
> can meter wall-clock"*), and nothing in the estate meters operator time. The
> rationale paragraph above was deleted 2026-08-03 and **restored 2026-08-09**; four
> surfaces cite it, one with a runnable command
> (`docs/notes/2026-07-29-comparative-advantage-thesis.md:369`).

| # | Item | Owner artifact | Blocks |
|---|---|---|---|
| 1 | **F1 — how §4 reads a Tradeify-resting discharge** (2026-11-08). Eval is live ([`S1`](docs/adr/2026-08-07-loop-s1-environment-ratification.md)); locked Striker book barred. §4 still scores the frozen $100K×4 set with Tradeify in it. Ruling owed: whether a discharge resting *on Tradeify* (or the withdrawn Striker book) discharges the four-firms program. **Deciding it early would pre-empt §4** | [`ADR 2026-08-04`](docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md) §7 F1 · [four-firms §4](docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md) | 2026-11-08 §4 verdict reading |
| 2 | **B7-REFIRE Stage 1 + M1** — both wait on an acceptable strategy on the ruled (Python-native) host. Eval live; no book deployed | [`GO ADR Addendum`](docs/adr/2026-07-17-c1-rail-build-account-registration-go.md) · [`S2`](docs/adr/2026-08-07-loop-s2-signal-host-fork.md) · [`M1`](docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md) | live-signal / arming path |
| 3 | **`Q-NSURV-2` + `Q-ORBSURV-1` opened and pre-registered** (2026-08-20, operator "go bigger"), successors to the deferred N-SURV-layer-design + ORB-MNQ-1 re-PARK-scope question. Both FROZEN, Phase 1 not yet run — needs operator GO to execute (each ~few-minutes wall time, $0/K=0, no live-risk surface). `Q-ORBSURV-1` explicitly does **not** license unpark on `RESOLVED` (§5) | [`Q-NSURV-2`](docs/briefs/Q-NSURV-2-second-uncertainty-layer-design.md) · [`Q-ORBSURV-1`](docs/briefs/Q-ORBSURV-1-cushion-sizing-gate-configurations.md) | Phase 1 execution GO |

---

## Executed operator decisions — decision index

ADRs own the decision narrative ([`docs/operational_rules.md`](docs/operational_rules.md)
Rule 7; [`docs/adr/2026-07-16-root-doc-charter-dedup.md`](docs/adr/2026-07-16-root-doc-charter-dedup.md)).
One line per executed decision, newest first — consequence only. Posture summary:
[`CLAUDE.md`](CLAUDE.md) §Live-execution posture.

- **2026-08-20** — **N-SURV single-history magnitude blindspot graduated HOLD→RESOLVED (`Q-NSURV-1`).**
  Operator: "graduate N-SURV." Confirmed general on a second candidate (ORB-MNQ-1), not idiosyncratic
  to c1 — axis-dependent on sizing mechanism (bust for flat, pass for cushion-proportional). No closed
  N-SURV verdict re-opened. Fix-design question deferred to next session (queue #3 above).
- **2026-08-19** — **`"cme"` broker panel admitted; `breadth.py`'s risk-N_eff mechanism revived on
  canonical data.** ADR `Proposed`→`Accepted` (operator: "I accept... and you can touch
  core/mc/modes.py"). 2-leg baseline (Striker DJ30/MYM, Striker NAS100/MNQ — Guardian/Aegis
  deliberately excluded, see ADR §2), consumed only by the Stage-8 portfolio-breadth tool, not the MC
  engine's own panel loader. First real anchor: `n_eff_dependence=1.9988, n_eff_risk=1.0871` (2-leg,
  not comparable to the retired 4-leg Pepperstone Q-NEFF-1 anchor). $0/K=0, research tooling only, no
  live-risk surface. [`ADR`](docs/adr/2026-08-19-cme-broker-panel-admission-for-breadth-revival.md) ·
  [`design spec`](docs/superpowers/specs/2026-08-19-cme-breadth-revival-candidate-index-design.md).
- **2026-08-19** — **Persona-hierarchy review panel ADR ratified; first real C-suite panel run
  (GSUB-2) SUBTRACTs b2 + c1.** ADR `Proposed`→`Accepted` (operator: "ratify the ADR"). First
  real (non-rehearsal) GRAND-tier panel use: CIO+COO+CRO reviewed a frozen SUBTRACT-candidate
  proposal over the GSUB-1 PARK cohort, `CLEAR-WITH-CONCERNS` (no CRO hard-block, no confirmed
  BLOCKER, one CONCERN fixed pre-ratification). Operator ratified both nominations: **b2** (Striker
  MYM reconstruction — re-entry blocked by the standing Striker bar) and **c1** (Q-XMEM-1 — same
  permitted test GSUB-1 used, re-applied on updated elapsed-idle evidence) → `SUBTRACT`, ~80 days
  ahead of their scheduled 2026-11-08 expiry. Six other PARKs unchanged. $0/K=0, no live-risk
  surface (CRO's own independent review confirmed no `dry_run`/M1/`armed_until`/DD-constant touch).
  [`ADR`](docs/adr/2026-08-19-loop-persona-hierarchy-review-panel.md) ·
  [`GSUB-2`](docs/briefs/GSUB-2-park-cohort-early-review.md) ·
  [`closure`](docs/briefs/closures/GSUB-2-closure-resolved-loadbearing.md).
- **2026-08-18** — **MNQ family-K disclosure: Notice-phase closed manifests and Cap-seat K bank.**
  Operator *"OK on both"*. Disclosure-only; `K_eff` untouched. Live figure at owner.
  [`ADR 2026-08-04` Addendum](docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md) ·
  [`MNQ.md` §K_BANKED](ops/instruments/MNQ.md).
- **2026-08-18** — **Q-TRAINKILL-3 `AMBIGUOUS-HOLD` — event-class blocks split; TRAINKILL census STOP.**
  Operator GO off TK2 Iterate packet. Block F `NEG` 9.83:1; Block A `DEP` 4.06:1.
  No singleton working-model. No Q-TRAINKILL-4. $0/K=0.
  [`closure`](docs/briefs/closures/Q-TRAINKILL-3-closure-ambiguous-hold.md) ·
  [`RESULTS`](lab/analysis/_inbox/q_trainkill_3_2026-08/RESULTS.md).
- **2026-08-18** — **Q-TRAINKILL-2 `AMBIGUOUS-HOLD` — both named alternates fit; no singleton power finding.**
  Operator GO off TK1 Iterate packet. Recovery promoted MSL-S2A only. Limb 2: NEG
  and DEP-ZERO both clear 0.05. Do not pick after seeing g. $0/K=0.
  [`closure`](docs/briefs/closures/Q-TRAINKILL-2-closure-ambiguous-hold.md) ·
  [`RESULTS`](lab/analysis/_inbox/q_trainkill_2_2026-08/RESULTS.md).
- **2026-08-18** — **Q-TRAINKILL-1 `AMBIGUOUS-HOLD` — no named power finding; no gate number moves.**
  Operator GO off iteration-2 notice packet 3. Set n=15 / μ_bar=+0.10R / floor 0.05 frozen
  before the table. Scored g(0)=0.024 < 0.05; BOUNDED extremes disagree. B2 elects on
  existing evidence + H1 screen, hold disclosed. $0/K=0.
  [`closure`](docs/briefs/closures/Q-TRAINKILL-1-closure-ambiguous-hold.md) ·
  [`RESULTS`](lab/analysis/_inbox/q_trainkill_1_2026-08/RESULTS.md).
- **2026-08-18** — **Q-EXPR-1 `RESOLVED` (H1) — next slate admission screens claim horizon vs E1.**
  Operator GO off iteration-2 notice packet 2. Share bar 0.50 frozen before the table.
  H1 4/4 weekly/daily vs session envelope; H2 1/5 misses; H3 cannot fire (W+D same first day).
  $0/K=0.
  [`closure`](docs/briefs/closures/Q-EXPR-1-closure-resolved.md) ·
  [`RESULTS`](lab/analysis/_inbox/q_expr_1_2026-08/RESULTS.md).
- **2026-08-18** — **Q-CONDVAL-1 `FALSIFIED` — S1b conditioner-engineering branch parked.**
  Operator GO off iteration-2 notice packet 1. Three levers frozen before the lift was
  substituted (slate-2 center · α=0 C−U mapping · 0.50× hurdle at R=$75/RT=$4.12).
  Measured L=0.130 < `L_star`=0.423. O2 discharged. SIGNAL-GENERIC stands; mechanism-owed
  stands. $0/K=0.
  [`closure`](docs/briefs/closures/Q-CONDVAL-1-closure-falsified.md) ·
  [`RESULTS`](lab/analysis/_inbox/q_condval_1_2026-08/RESULTS.md).
- **2026-08-17** — **Six-lead P3 (L5 curve-slope) un-HOLD → GO → sleeve CLOSED (venue).**
  Operator un-HOLD. Paper read (Bianchi/Fan/Miffre/Zhang *JBF* 2023 / arXiv `2308.00383`):
  profitable S-strategy is a same-commodity calendar spread (Δslope → long front / short
  fourth). Distinguishes from the 2026-06-06 USOIL-carry kill (static state × outright) —
  DISTINGUISHABLE, not ADMIT. Databento `estimate` on the 12 venue-legal parents: `ohlcv-1d`
  / `ohlcv-1m` / `definition` all $0.0000 both windows; `tbbo` CL-parent $1,543.90 (contrast;
  over ceiling). Binding close is the standing Tradeify calendar-spread SCREEN-FAIL, not
  cost. No pull. Limb-2 untouched. P4/P5 stay HOLD. $0/K=0.
  [`P3_DRYRUN`](lab/analysis/harvest/six_lead_cf_2026-08-17/P3_DRYRUN.md) ·
  [`plan`](docs/briefs/2026-08-17-six-lead-pursuit-plan.md) §13.
- **2026-08-17** — **Q-POLFRONT-1 intraday-honest remeasurement fork executed — 5.1× policy
  frontier does NOT survive; flat frontier survives only at low R.** Operator GO. Three design
  attempts (v1 units-conflation, v2 resampling-saturation, both invalidated pre-write-up; v3
  landed, deterministic real-trade-calibrated median multiplier). Result: median flat-arm bust
  delta +18.0pp (2/24 cells still clear 3.0%); median policy-arm delta +98.1pp (1/26 cells still
  clear). Adversarially verified `SAFE_WITH_CAVEATS` (4 reviewers + synthesis): no coding defect,
  independent reimplementation reproduced both headline numbers and a closed-form collapse
  mechanism, but two confirmed calibration biases (pyramiding contamination, multi-trade-day
  summing) both push toward overstating risk — read magnitudes as a credible upper bound, not a
  tight estimate. Supersedes the 5.1× headline as a usable sizing multiplier; deep-lane GO-1
  should not lean on the policy frontier. $0/K=0, no live-risk surface, no `core/`/
  `dd_protection.py` touch. [`RESULTS`](lab/analysis/c1/q_polfront_1_2026-08/RESULTS_INTRADAY_HONEST.md) ·
  [`OPERATIONALIZATION`](lab/analysis/c1/q_polfront_1_2026-08/OPERATIONALIZATION_INTRADAY_HONEST.md) ·
  [`closure addendum`](docs/briefs/closures/Q-POLFRONT-1-closure-resolved-quantified.md#addendum-2026-08-17--fork-executed-neither-arm-survives-policy-near-totally-flat-mostly).
- **2026-08-17** — **Six-lead pursuit channel-scope addendum landed; queue row 3 closes.** OpenAlex
  admitted as a Semantic-Scholar-index-gap substitute citation-graph traversal channel (operator
  GO, "land it as-is"), light tier — no admission requirement, §4 falsifier, or counting machinery
  touched; retroactively documents the 2026-08-16 fork election. This was the only unlanded piece
  of the six-lead pursuit thread — Phase 0 DONE, P1-CF/P2-CF FAIL all four legs, limb-2 ruled does
  not increment (all landed earlier the same day, lines below). Thread has no open items;
  P3–P5 stay HOLD per the operator's own 2026-08-17 marks. $0/K=0, no live-risk surface.
  [`harvest intake ADR` addendum](docs/adr/2026-07-15-external-mechanism-harvest-intake.md#addendum-2026-08-17--openalex-admitted-as-a-sourcing-channel-substitute) ·
  [`plan`](docs/briefs/2026-08-17-six-lead-pursuit-plan.md) §13.
- **2026-08-17** — **Harvest §4 limb-2 counter ruled: P1-CF/P2-CF FAIL does NOT increment.**
  Operator direction ("rule the limb-2 counter question"). Two independent grounds: (1) neither
  lead was ever admitted through the intake — no manifest, no `register_search open`, no ratified
  inventory row — and §4's falsifier is scoped to mechanisms "admitted through this intake"; (2)
  even setting admission aside, the kill class doesn't match the counted categories (Stage-2
  cost-law / Clause-N power are named campaign stages this Phase-1 cheap-falsifier never routed
  through). Counting-machinery table gains a row; running count stays **0/2**; limb 1 and the
  machinery itself untouched. $0/K=0, no live-risk surface.
  [`harvest intake ADR` — Ruling 2026-08-17](docs/adr/2026-07-15-external-mechanism-harvest-intake.md) ·
  [`plan`](docs/briefs/2026-08-17-six-lead-pursuit-plan.md) §13.
- **2026-08-17** — **Six-lead pursuit P1-CF/P2-CF EXECUTED → FAIL, all four legs (MGC+6J).**
  Operator GO on P1 (L3=L6 overnight-reversal) + P2 (L1 index-flow reversal), HOLD on P3–P5, ran
  against on-hand frozen panels (`core/data/bar_data/MGC_M15.csv` / `6J_M15.csv`). Three legs
  gross-negative outright; the fourth (P1×6J) gross-positive but t=0.64 (not significant) and
  0.73× the 4× cost hurdle. Stop-trigger rate 3.3–4.7% rules out the hard-stop as the driver;
  long/short split shows each instrument's own trend swamping the fade — not a construction
  defect. Landed on 3 of 4 required surfaces (LOG · CANDIDATE_ROWS addendum · this line); no
  `rejected_candidates.md` row per the 2026-08-15 pre-G0-kills-are-not-§4-strikes precedent.
  **Harvest §4 limb-2 counter question still unmarked** — this FAIL is exactly the case it
  governs. $0/K=0 — panels on hand, no pull. [`CF LOG`](lab/analysis/harvest/six_lead_cf_2026-08-17/LOG.md) ·
  [`plan`](docs/briefs/2026-08-17-six-lead-pursuit-plan.md) §4.
- **2026-08-17** — **Six-lead pursuit Phase 0 executed; correction to the same-day Koijen axis-2
  entry below — 6 distinct papers corrects to 5.** SOURCES_LOG rows #3 ("Market Closure and
  Short-Term Reversal", Della Corte/Kosowski/Wang, 2015 draft) and #6 ("Overnight-Intraday
  Reversal Everywhere", +Liu, 2022 draft) are **the same paper** — same SSRN abstract `2730304`,
  explicit self-citation of the retitle, additive author list — read directly, not the "one
  research program, unresolved" hedge the fork note carried. Full plan + Phase 0 execution ledger
  (dedup, venue/cost screens, per-lead recommendations) at
  [`docs/briefs/2026-08-17-six-lead-pursuit-plan.md`](docs/briefs/2026-08-17-six-lead-pursuit-plan.md);
  primary evidence in the
  [SOURCES_LOG addendum](lab/analysis/harvest/koijen_axis2_openalex_2026-08-17/SOURCES_LOG.md#addendum-2026-08-17--3-and-6-are-the-same-paper-not-two-independent-leads-count-corrects-65).
  Notable dedup hit: `H-OD-1` (ES overnight-drift, dealer-inventory-risk mechanism, died Stage-2
  cost-law) is the closest prior estate precedent to this cohort's WHO family. $0/K=0 — two PDF
  reads + repo-internal screens, no data pull, no register_search, no Cap claim. Operator marks
  owed — queue row 3.
- **2026-08-17** — **Koijen axis-2 (Carry, JFE 2018) fork resolved: OpenAlex substitute executed →
  6 distinct screen-level leads, not "0 survivors" like axis-1.** Operator elected the
  OpenAlex-substitute branch of the 2026-08-16 fork (S2 has no record of the paper). 296 citing
  works → 234 keyword-shortlisted → 230 screened (7-agent workflow) → 17 flagged → **7 records / 6
  distinct papers** survived adversarial verify — concentrated in overnight/closure-reversal and
  hedging-flow mechanisms, not carry/trend-following. **None is an admitted Req-1a candidate** —
  every lead carries a named unresolved question (real-time WHO-variable reconstructibility;
  cost/spread survival, this program's dominant null mode). $0/K=0, no register_search, no Cap
  claim. [`SOURCES_LOG`](lab/analysis/harvest/koijen_axis2_openalex_2026-08-17/SOURCES_LOG.md) ·
  [`CANDIDATE_ROWS addendum`](lab/analysis/harvest/radar_tier_a_burst_2026-07/CANDIDATE_ROWS.md)
- **2026-08-17** — **MSL-S2B successor's CON-5 D2 falsifier executed → `D2_FAIL`; route B closes for
  this construct-shape at $0.** `sweep-failure-filtered-continuation` × MYM 15m, IS panel only
  (CONFIRM untouched): mean signed gross **−1.00 pt** across 850 signals (WR 25.41% ≈ the box's own
  rr=3 breakeven) vs the +11.28 pt (0.5×4×RT) pass bar — **−0.044×**, non-marginal. Entry trigger
  (never specified in the frozen card) operator-elected 2026-08-17: reuse MSL-C1's own sweep +
  failed-extension-reclaim signal, flip/continuation side, on S2B's own placeholder 40/120
  stop-target box (`card.yaml`, not re-tuned). MSL-S2B's frozen 2026-08-14 `STAGE-1 FAIL` verdict is
  unchanged (D3 prospective-only). $0/K=0, no Board debate needed per the ADR's own D2 clause.
  [`LOG`](lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_s2b_con5_d2_2026-08-17_LOG.md) ·
  [`ADR`](docs/adr/2026-08-16-con5-timeframe-scope-cheap-falsifier-gate.md) ·
  [`STAGE1 addendum`](lab/analysis/c1/msl_s2b_mym_2026-08/STAGE1.md)
- **2026-08-16** — **DL-1 ABANDONED (train scoring executed).** §6 steps 1–2 run: 10 frozen
  variants scored on GC.FUT TRAIN (2010–2019, 2,168 CME sessions). Nominee V7 (argmax train net
  annSR, no fallback) failed gates 2a/2b/2d — net annSR −0.42 (not >0); SPA consistent p=0.94 vs
  the ≤0.10 bar; M-16 +1-tick slip annSR −0.66. Gate 2c (cadence) passed. All 10 variants
  net-negative on TRAIN. Confirm partition (MGC.FUT) never read, per prereg §5. Charter counters:
  abandoned 1 (consecutive 1/2), active campaign none. $0/K=0 — no new pulls, K already declared
  at freeze. [`charter`](docs/adr/2026-08-16-deep-iteration-lane-charter.md) ·
  [`results`](lab/analysis/deep_lane/dl1_mgc_orc_2026-08-16/train_results.json)
- **2026-08-16** — **CON-5 pause scope ruled: dense-1m route-scoped, with a $0 cheap-falsifier gate for out-of-lane route-① reliance (operator election, third of three options).** Resolves MSL-S2B's internal inconsistency (same "dense-1m" qualifier read two ways in adjacent BINDING-BAR rows); harmonizes with — supersedes nothing of — the DL-1 GO's per-campaign pause adjudication and U0 KEEP (pause itself stands; nothing unpaused; S2B verdict untouched). Falsifier spec frozen, unexecuted (`MYM_M15.csv` absent in authoring worktree). $0/K=0. [`ADR`](docs/adr/2026-08-16-con5-timeframe-scope-cheap-falsifier-gate.md)
- **2026-08-16** — **Weekly venue-idle token trade: recurrence ruled — fresh-decision-per-week is the
  standing, closed design, not an open gap (operator election, closes S4's 5th governance hole).**
  The 2026-08-05 one-week exception was deliberately scoped to spend the book-composition brief's
  §5(5) forbidden-move override *once*, not to establish a standing licence — ratifying it as
  standing now would be a bigger, different decision than the one actually taken. What closes here
  is narrower: the *policy question itself* ("must recurrence be re-elected every week, or is that
  an unresolved gap") is answered **yes, re-election every week is correct and intended**, matching
  lived practice (3+ consecutive weeks covered without incident). The weekly operator-placed trade
  obligation itself is unchanged — still real, still unrecoverable if missed, still **no agent may
  place it** ([`CLAUDE.md`](CLAUDE.md) §Live-execution posture) — only the open-queue framing around
  it is discharged. Queue row 0 deleted (retention test: the policy question is now closed, not
  "open or still owed"). $0/K=0, no live-risk surface (a compliance-only idle-clock trade, not
  `dry_run`/M1 arming). [`S1`](docs/adr/2026-08-07-loop-s1-environment-ratification.md) ·
  [`ADR 2026-06-30`](docs/adr/2026-06-30-no-manual-trading-cfd-retirement.md) (stands, untouched)
- **2026-08-16** — **DL-1 prereg `FROZEN` (operator GO).** First deep-lane campaign live: gold ORC, GC-train 2010–2019 / MGC-confirm 2019–2026, K=10, strict-argmax nomination, confirm read once. GO adjudicated the five gathered items (bar-scope · pause reach · channel-origin · gold-ORB clearance · step-4 mapping). §6 step-1 pulls fired ($0, cache-tagged); train scoring = next session. [`prereg`](docs/briefs/pre-registration/2026-08-16-deep-lane-dl1-mgc-orc-prereg.md) · [`charter`](docs/adr/2026-08-16-deep-iteration-lane-charter.md)
- **2026-08-16** — **Databento parent-era cost dry-run executed; deep-lane GO-1 fully discharged.** Bar schemas (1d/1h/1m) on the design-box triad (GC/CL/6A train, MGC/MCL/M6A confirm) all $0.0000 both windows; tbbo priced for contrast ($2,209.69 train / $274.89 confirm) to show where the real cost gate sits. §7 step 1 (first campaign prereg, K≈10) is now the only remaining gate. $0/K=0. [`charter addendum`](docs/adr/2026-08-16-deep-iteration-lane-charter.md)
- **2026-08-16** — **Deep-iteration lane charter `Accepted` (operator "P2 + GO", overriding its own HOLD default eyes-open).** New candidate-producing channel: one family/campaign, three binding K conjuncts, untouched confirm, 2-campaign falsification budget. GO-1: first prereg after Q-POLFRONT-1 + Databento dry-run; GO-2: first campaign K≈10. No Cap change; N-SURV unedited. $0/K=0. [`charter`](docs/adr/2026-08-16-deep-iteration-lane-charter.md)
- **2026-08-16** — **State-policy packet marked `P2`.** Q-EVALSEQ-1 un-dormed scoring-only (frozen K=4 run licensed, harness anchor-verified before read); Q-POLFRONT-1 commissioned (named, not opened — brief owed); b5 renewed once (corrected wake; expiry 2027-02-08). Nothing deploys. $0 at mark. [`closure`](docs/briefs/closures/STATE-POLICY-closure-resolved-p2.md)
- **2026-08-16** — **Governance-holes closing pass (4 of 5 S4 items from the 2026-08-16 bottleneck
  diagnostic; weekly-token recurrence stays open, operator election).** (1) `AMBIGUOUS-HOLD` now
  counts toward every named consecutive/streak falsifier — dense-1m lane stop-rule and
  harvest-intake §4 patched; the CON-2→CON-5 sequence had run past the old counter uncounted.
  (2) D3 (Tradeify book-composition churn-posture fork) ruled **MOOT** — subject withdrawn
  2026-08-04, parent gate item D1 already MOOT; re-entry tied to fork F3. (3) GSUB-1 PARK register
  reconciled — 6/8 items confirmed no drift; b6 (+b1) corrected a stale F3-successor re-entry
  clause S1's no-migration ruling made unreachable; b5's own correction + renewal merged same day
  via [PR #21](https://github.com/Joshua-Asante/first-passage/pull/21). (4) `two_barrier_first_passage_track.md`
  deleted — failed all five retention prongs (R1–R5), zero consumers, motivating candidate (MSL-C1)
  already FALSIFIED without it; retrievable via `git log --follow` + `git show <commit>^:<path>`.
  $0/K=0, no live-risk surface. [`AMBIGUOUS-HOLD ADR`](docs/adr/2026-08-16-ambiguous-hold-counts-toward-null-run-thresholds.md) ·
  [`D3 addendum`](docs/briefs/2026-07-23-tradeify-book-composition.md#addendum-2026-08-16--§6-d3-ruled-mootstranded-governance-holes-closing-pass)
- **2026-08-15** — **`MNQ-SIZEDIV-1` KILLED pre-G0 at the Stage-2 falsifier; $90.22 spent; pre-G0 kill count → 2/3.** All three frozen limbs fired at once (TRAIN semester, n=252 trades/126 sessions): mean signed gross **−2.06 bp** (F1 ≤ +0.911); hit 0.4960 < base 0.5357 (F2); **relabel corr sign(A) vs same-session sign(R) = +0.7226** (F3) — the size-asymmetry divergence is substantially a same-day-direction relabel (daily momentum in disguise). Stage 3 not spent. No manifest, no Q-ID, **not** a §4 strike. Durable residue: any future session-scale size statistic must pre-clear **independence from same-day return sign**; trades caches reusable at $0 re-read (confirm-year $0 · semester $90.22). Ported 2026-08-16 from archive-lineage branch `claude/blind-channel-distinct-construct-0fcd2b`. [`STAGE2_FALSIFIER`](lab/analysis/c1/mnq_sizediv_blind_2026-08/STAGE2_FALSIFIER.md) · [`freeze`](lab/analysis/c1/mnq_sizediv_blind_2026-08/DESIGN_FREEZE.md)
- **2026-08-15** — **Blind-channel staged GO elected; `MNQ-SIZEDIV-1` frozen pre-data.** Session-unit aggressor-size-asymmetry divergence (`A = I_vw − I_cw` from prints) → next-session two-slot RTH; `K_intrinsic=1`; dedup executed clean (zero mechanism-family hits estate-wide). Measured costs: confirm-year **$0** / 3y **$462.27** (full era $1,100.53 and tbbo-3y $770.46 over the $700 ceiling — not authorized). Stage 1 = $0 pull + outcome-free diagnostics; Stage 2 falsifier ≤$120; Stage 3 ≤$400 + `register_search open --lane blind` (manifest boundary). Ported 2026-08-16 from archive lineage. [`freeze`](lab/analysis/c1/mnq_sizediv_blind_2026-08/DESIGN_FREEZE.md)
- **2026-08-15** — **Harvest §4 limb 2 pin marked `no`.** Already-closed D5 / H-OD-1 / H-TSMOM-1 do not increment. Post-mark count **0 / 2**. Not fired. Limb 1 still 0-of-2. No Cap change; no third channel. $0/K=0. [`harvest addendum`](docs/adr/2026-07-15-external-mechanism-harvest-intake.md)
- **2026-08-15** — **Harvest §4 limb 2 (R10) `Accepted`.** Operator GO after PR #15. Pin (do already-closed D5 / H-OD-1 / H-TSMOM-1 count?) unmarked — **not fired**. Limb 1 still 0-of-2. No Cap change; no third channel. $0/K=0. [`harvest addendum`](docs/adr/2026-07-15-external-mechanism-harvest-intake.md)
- **2026-08-15** — **08-03 gate-stack R3/R4/R5/R6 executed; R10 drafted `Proposed`.** Sentinel cross-tree pairing, H-TSMOM-1 living-harness pin, `var_trials` default `1/n`, `cost_mnq` `firm_key` required. Harvest §4 limb 2 is spec-only — operator GO still owed; limb 1 stays 0-of-2. $0/K=0. [`08-03 audit`](docs/notes/audits/programme-audit/2026-08-03-gate-stack-audit.md) · [`harvest addendum`](docs/adr/2026-07-15-external-mechanism-harvest-intake.md)
- **2026-08-15** — **Dense-1m unpause Board U0 KEEP recorded.** Branch A stands; OHLCV temporal-selectivity / entry-geometry default stays paused; no CON-6; analogue carve-out unchanged; E1/S2B untouched. $0/K=0. [`closure`](docs/briefs/closures/DENSE1M-UNPAUSE-closure-resolved-u0-keep.md) · [`packet`](docs/briefs/2026-08-15-dense1m-lane-unpause-review.md)
- **2026-08-15** — **Blind-channel generation attempt: naming set empty.** One post-N=3 write-up authorized; every standing door walked before any look; none yielded a distinct K≤3 construct without shopping. No screen, no manifest, count now **2/3** after SIZEDIV port (was 1/3 at write-up), not generation-dry. Stop generating; §4 `AMBIGUOUS-HOLD` trajectory accepted if still unsourced at 2026-11-08. $0/K=0. [`addendum`](docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md)
- **2026-08-15** — **Blind-channel consecutive-pre-G0-kill threshold elected N = 3.** Counting machinery (a)–(d) written on the channel ADR (canonical count line; STATE is a mirror). Running count **2/3** (SIZEDIV port). Generation-dry at next quarterly audit if N fires — not `FALSIFIED`, no third channel. Limb 4; amend-in-place; not light. $0/K=0. [`addendum`](docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md)
- **2026-08-15** — **`Q-CAPBAND-1` closed `RESOLVED` — Cap 1.0 evidence-ratified on the named axes.** Both band axes die on non-Cap gates: **D6** venue-dead (EURUSD `NOT TRADABLE` — CFD venue closed 2026-07-10); **D2-low** bar-bound (ES/NQ/YM all return the tier=always `index-intraday-ohlcv-directional-timing-2026-07-21`). So even at Cap 2.0 neither becomes fundable — the search-affordability finding does **not** rest on a possibly-miscalibrated constant. Discharges [2026-08-03 audit](docs/notes/audits/programme-audit/2026-08-03-gate-stack-audit.md) §5.4 item 3. ⚠ Scope: ratified **on the named axes only**, not in general; gates 1–2 stayed `unevaluable`. `CAP` byte-unedited; $0/K=0. [`closure`](docs/briefs/closures/Q-CAPBAND-1-closure-resolved.md)
- **2026-08-15** — **Aegis 1.83 WITHDRAWN as a reachability ceiling; `Q-CAPBAND-1` opened.** M-19 requires benchmarking a DSR floor against **both** the in-house edge (1.83) **and** the corrected published top decile (**S_B 0.85**), firing only when it exceeds *both*; only the first had been carried. 1.83 is also cohort-bound, **K-undeclared** and **un-deflated** — not placeable on the DSR axis. Corrections appended at both points of use. Operative bound relocates to **`CAP = 1.0`**, unsettled per the 2026-08-03 audit §5.4. `CAP` byte-unedited; $0/K=0. [`Q-CAPBAND-1`](docs/briefs/Q-CAPBAND-1-cap-band-counterfactual.md) · [`pre-reg`](docs/briefs/pre-registration/Q-CAPBAND-1-verdict-preregistration.md)
- **2026-08-15** — **Pre-G0 kills are NOT §4 strikes (blind channel).** Boundary is `register_search open`: the four battery stages test the candidate's economics, a pre-G0 falsifier tests whether it is worth testing at all. Ratified alongside: **mandatory pre-G0 kill counting + disclosure** with every §4 reading (count now **1**), because the ruling makes §4 harder to fire — degeneration-signal-#3 adjacency, named in the addendum. Consecutive-kill threshold left **uncovered** (queue row 3). Battery-closure definition untouched. $0/K=0. [`addendum`](docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md)
- **2026-08-15** — **Blind-channel cost geometry measured; `MNQ-ANALOGUE-1` killed pre-G0 at $0/K=0.** 5-instrument cost map primary-sourced (MNQ 3.65bp / MGC 6.68 / MYM 6.42 / M2K 11.03 / MCL 21.47 at panel medians); cost wall is a **frequency** wall (MNQ 2.27% capture @1/sess → 13.65% @6/sess). Operator ruled algorithmic-analogue a **new modality** (lifts CON-5 pause for that class); the authorized candidate then died — hit rate 0.5160 < base 0.5453, +0.837bp vs 3.64bp required, CI straddles 0. **Feasible set empty at $0.** No manifest, no Q-ID, **not** a §4 strike. [`notice`](docs/notes/notice/N-2026-08-15-blind-channel-cost-geometry-and-first-candidate-kill.md) · [`route ruling`](docs/adr/2026-08-15-analogue-modality-route-ruling.md) · [`K-cap addendum`](docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md)
- **2026-08-15** — **No-counterparty statistical sourcing channel `Accepted` (full-tier ADR).** Operator election ("admit a weaker evidentiary grade for candidate sourcing") operationalized: opens a `futures-anomaly-discovery`-owned `--lane blind` channel for no-counterparty candidates (motifs/change-points/HMM/symbolic regression), gated by K-accounting + mandatory frozen train/confirm split + DSR≥0.95 + cost-law + an own-series half-split DSR check + N-SURV unchanged. Req-1a and MSL fully untouched. 3-round adversarial hardening caught a fabricated quote, a wrong falsifier-trigger citation, a falsifier-reachability gap, and a regime-gate name-collision risk before ratification. $0/K=0. [`ADR`](docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md)
- **2026-08-15** — **F1/F2/Board-lite discharged (3 light ADRs).** F1: 2026-08-02 regime-gate scope narrowing ratified as-is (grounded in the gate's own `dd_protection`-class scope). F2: allocation-refresh-2 forward-monitor absence accepted explicitly (blocked — no live-fill route since the 2026-08-04 Tradeify de-scope). Board-lite: label papered as shorthand for two already-ratified rules. $0/K=0.
  [`F1 ADR`](docs/adr/2026-08-15-regime-gate-scope-ratification.md) · [`F2 addendum`](docs/adr/2026-05-23-allocation-refresh-2.md) · [`Board-lite ADR`](docs/adr/2026-08-15-board-lite-label-ratification.md)
- **2026-08-15** — **`Q-BUSTGATE-2` closed `RESOLVED` — bust ceiling reconfirmed unchanged.** Sole regime-admissible rung (0.50×)
  intraday-honest bust 0.72% ≤ 3.0%; 2026-08-13 population data + updated fee schedule checked, neither moves the ceiling;
  unconstrained-EV thread still points looser (narrowed, not reversed) but is non-decision-governing. No third re-derivation
  absent a structural-change ruling. $0/K=0. [`closure`](docs/briefs/closures/Q-BUSTGATE-2-closure-resolved.md) ·
  [`brief`](docs/briefs/Q-BUSTGATE-2-bust-gate-re-derivation-2026-08.md)
- **2026-08-15** — **MSL-era wall-scope audit + 08-03 follow-up verification landed.** 14 walls mapped, 4 flagged, 3 refuted on
  adversarial re-check (13/14 legitimately scoped — no over-tight composition found); 1 confirmed (`Board-lite` label unratified/
  unwired, kills it bundles independently sound). Of the 08-03 audit's own F1–F3/R1–R11: 3 DONE, 3 partial, 7 owed — F1/F2 now
  **7 days overdue**. [`audit`](docs/notes/audits/programme-audit/2026-08-15-msl-wall-scope-audit.md)
- **2026-08-14** — **MSL WHO-track `STILL DRY` (estate-wide).** Every Tradeify product group + census backlog walked; no WHO outside INTAKE-DRY / C1–S2B; no slate-4 card; camp not scaffolded. E1 stop rule stands. $0/K=0. [`notice`](docs/notes/notice/N-2026-08-14-msl-who-track.md)
- **2026-08-14** — **MSL §7 E1 HOLD recorded.** Phase 3 HOLD; no slate-4 card until NEW WHO; charter stays RATIFIED; yield not fired. $0/K=0. [`closure`](docs/briefs/closures/MSL-S7-closure-resolved-e1-hold.md) · [`packet`](docs/briefs/2026-08-14-msl-slate-generation-review.md)
- **2026-08-14** — **MSL §7 slate-generation review packet authored; election then recorded E1 (line above).** Yield not fired. $0/K=0. [`packet`](docs/briefs/2026-08-14-msl-slate-generation-review.md)
- **2026-08-14** — **MSL slate-3 `BLOCKED` (mechanism-dry).** Board-lite constraints frozen; no fade WHO outside 2026-08-10 INTAKE-DRY; camp not scaffolded; functional 3/3. $0/K=0. notice (`git show ef48b015:docs/notes/notice/N-2026-08-14-msl-slate-3-constraints.md`)
- **2026-08-14** — **MSL-S2B Stage-0/1 `STAGE-1 FAIL` (route; pre-G0).** Raised bar unbound for continuation *entry*; SLR route ① filter-only; temporal-selectivity paused; composite refused. G0 never frozen; slate-2 exhausted; Stage-1 deaths **2/3**. $0/K=0. [`closure`](docs/briefs/closures/MSL-S2B-closure-stage1-fail-route.md) · [`STAGE1`](lab/analysis/c1/msl_s2b_mym_2026-08/STAGE1.md)
- **2026-08-13** — **Dedup-first-before-new-work `Accepted`; §7 mechanical wiring merged (PR #800).** Rule 8 sub-rule 8 (paste search output before new `lab/analysis/` or `core/`-adjacent work); advisor-dedup hookify trigger committed + broadened to build-intent language; `check_advisor_dedup.py` gains a `--keywords` mode; `archive_lab_analysis.py` gains a same-theme collision WARN. Prompted by two same-session dedup misses. $0/K=0. [`ADR`](docs/adr/2026-08-13-dedup-first-before-new-work.md)
- **2026-08-13** — **Tradeify Select 100K checkout price re-sourced (PR #801).** Current: $265 list / $159 checkout (code AUG, expires 2026-08-31) / $169 reset / no activation fee — primary-sourced in-browser 2026-08-13 (WebFetch 403s the host). Historical $159 paid 2026-07-18 (GO ADR §B4) left untouched as the purchase record; this is the forward-modeling figure. $0/K=0. note (`git show 67e4b209:docs/notes/2026-08-13-tradeify-select-100k-checkout-price.md`)
- **2026-08-13** — **MSL-C3-K2 dual-axis explore FALSIFIED.** Both axes IS CI entirely &lt; 0; panel `M2K_M15` landed (TV); CONFIRM unread; S2B unblocked; $0/K spent=0. [`closure`](docs/briefs/closures/MSL-C3-K2-closure-falsified.md) · [`RESULTS_g2`](lab/archive/msl_c3_m2k_2026-08/RESULTS_g2.md) · [`PREREG_G0`](lab/archive/msl_c3_m2k_2026-08/PREREG_G0.md)
- **2026-08-13** — **MSL-C3-K2 dual-axis G0 FROZEN.** B4 paid after Stage-1 PASS; `K_intrinsic=2` (PDH/PDL + overnight); DSR floor 0.850; explore unpaid at freeze (superseded by FALSIFIED line above). [`ADR`](docs/adr/2026-08-13-msl-c3-k2-dual-axis-revive.md) · [`STAGE1_K2`](lab/archive/msl_c3_m2k_2026-08/STAGE1_K2.md) · [`PREREG_G0`](lab/archive/msl_c3_m2k_2026-08/PREREG_G0.md)
- **2026-08-13** — **MSL-C3-K2 dual-axis Stage-1 revive ELECTED.** Fresh Stage-1 PASS licensing `K_intrinsic=2` (PDH/PDL + overnight both scored); DSR floor 0.850; board ahead of S2B; B4 was unpaid at election (superseded by G0 freeze line above). [`ADR`](docs/adr/2026-08-13-msl-c3-k2-dual-axis-revive.md) · [`STAGE1_K2`](lab/archive/msl_c3_m2k_2026-08/STAGE1_K2.md)
- **2026-08-13** — **MSL-S2A explore GO → `FALSIFIED` (N-ACT).** IS trades/week 0.511; long FLIP FAIL; CONFIRM unread; STOP G0. $0/K=0. [`RESULTS_g2`](lab/archive/msl_s2a_mcl_2026-08/RESULTS_g2.md) · [closure](docs/briefs/closures/MSL-S2A-closure-falsified.md)
- **2026-08-13** — **MSL-S2A B4 GO → G0 FROZEN.** MCL `pullback-failure-resumption`; `K_intrinsic=1`; CONFIRM `2025-07-01→2026-07-02` unread; explore later FALSIFIED 2026-08-13. $0/K=0. [`PREREG_G0`](lab/archive/msl_s2a_mcl_2026-08/PREREG_G0.md)
- **2026-08-13** — **MSL slate-2 box ELECTED + P3.4 S2A Stage-1 PASS (B4 unpaid).** `rr`∈[2,3] / WR 0.30–0.42 / R-at-frontier; S2A MCL `pullback-failure-resumption`; SNAG registered; Magdon-Ismail not calibration; sprint lane not opened. $0/K=0. [`ADR`](docs/adr/2026-08-13-msl-slate-2-design-box.md) · [STAGE1](lab/archive/msl_s2a_mcl_2026-08/STAGE1.md)
- **2026-08-13** — **MSL-C2 explore GO → `FALSIFIED` (both-arms CI&lt;0).** IS mean ≈ −0.18R; DELETE FAIL; CONFIRM unread; STOP G0 → P3.2 C3 next. $0/K=0. [`RESULTS_g2`](lab/archive/msl_c2_mgc_2026-08/RESULTS_g2.md) · [closure](docs/briefs/closures/MSL-C2-closure-falsified.md)
- **2026-08-13** — **`implied_annualized_sr` DEMOTED gate → report-only (`IMPLIED-SR-REPORT-ONLY-2026-08-13`); Tradeify-native fade design-region REOPENED as geometry.** 1.83 is a cohort disclosure, not a FAIL. Measured-edge still gates on DSR-at-K. No mechanism admitted. $0/K=0. [`ADR`](docs/adr/2026-08-13-implied-sr-report-only-fade-reopen.md)
- **2026-08-12** — **MSL-C2 B4 GO → G0 FROZEN.** London-range failed-extension fade on MGC; K_intrinsic=1; CONFIRM 2025-09-01→2026-08-12 unread; explore/Pine unpaid (later explore FALSIFIED 2026-08-13). $0/K=0. [`PREREG_G0`](lab/archive/msl_c2_mgc_2026-08/PREREG_G0.md)
- **2026-08-12** — **MSL implied-SR off kill list (interim; now Superseded).** Absorbed by 2026-08-13 report-only ADR. [ADR](docs/adr/2026-08-12-msl-implied-sr-disclosure-not-kill.md)
- **2026-08-12** — **MSL Board B1–B3 + B8 ratified.** Channel Accepted (R-CHANNEL ☑ · R-FRAMING ☑ §2.1 · R-REQSCOPE ☑ do-not-bind); slate **C2→C3→C1**; Cursor wrapper allow-rule; `MYM1!`/`MNQ1!` occupancy released for new non-Striker research. S1 keep-warm + Striker redeploy bar stand. $0/K=0. [ratification](docs/adr/2026-08-12-msl-sourcing-channel-ratification.md) · [occupancy](docs/adr/2026-08-12-msl-mym-occupancy-release.md) · [plan](docs/briefs/2026-08-12-msl-program-plan.md)
- **2026-08-12** — **Q-TXG-1 CLOSED — FALSIFIED-at-walls (operator A).** H_A re-argument ruled CLOSE; third election barred; registry lane row filed. Re-proposal = different loss-side shape or different venue-class survival geometry (not new cells/ATR). [packet](docs/briefs/Q-TXG-1-ha-reargument.md) · [lane closure](docs/briefs/closures/Q-TXG-1-closure-falsified-at-walls.md) · [registry](docs/rejected_candidates.md)
- **2026-08-12** — **Q-TXG-1 cell #2 striker×MNQ → DEAD(N-SURV).** Cost PASS (mean_net_r 0.042 > 0.03); N-SURV FAIL full/H1/H2 bust ~98%/97%/99% vs ≤3.0%. K actual=declared=1. Cell #1 striker_nas100×MYM still open at authoring — lane H_A re-argument **not** fired. [closure](docs/briefs/closures/2026-08-12-q-txg-1-striker-mnq-cell-dead-nsurv.md) · [PANEL_SCORE](lab/archive/transfer_expression_grid_2026-08/cells/striker_mnq/PANEL_SCORE.json)
- **2026-08-12** — **Q-TXG-1 Blocks 2–3 frozen at .** Elected striker_nas100×MYM then striker×MNQ; cell PREREGs + ports hash-pinned + RUNSPECs authored. **HARD STOP before scoring** (Block 4 gated on operator native-TV exports). [ELECTION](lab/archive/transfer_expression_grid_2026-08/ELECTION.md) · [
as×MYM PREREG](docs/briefs/pre-registration/2026-08-12-q-txg-1-striker-nas100-mym-cell-prereg.md) · [striker×MNQ PREREG](docs/briefs/pre-registration/2026-08-12-q-txg-1-striker-mnq-cell-prereg.md)
- **2026-08-12** — **Q-TNEC-CON-5 Branch A STOP elected** (operator election via task start). Catalogue non-promotable; CONFIRM unread forever; dense-1m **OHLCV temporal-selectivity lane default paused** pending new modality / non-route-① thesis. Cite: 8 consecutive zero-yield closes since 2026-08-08 (Q-R2VBUCK-1 … Q-TNEC-CON-5) vs SNAG 3. Lane FALSIFIED counter **unchanged 1/3**. /K=0. [closure](docs/briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md)
- **2026-08-11** — **`Q-TXG-1` Block 1 executed at $0.** Transfer/expression grid compiled (4 mechanisms × ENV-1 7-micro pool); H_A **OPEN — 25 OPEN cells**. Block 2 election packet authorized. [`GRID_RESULTS`](lab/archive/transfer_expression_grid_2026-08/GRID_RESULTS.md) · [`PREREG`](lab/archive/transfer_expression_grid_2026-08/PREREG.md)
- **2026-08-11** — **`Q-SCORE-1` Block 1 H_A FALSIFIED at $0.** Assignability 37/53 (69.8%) under frozen Closed: grammar; grandfather-concentration **recent-spread** (7/15 undated not in GRANDFATHERED). Residue **RATIFIED 2026-08-11** (operator GO via task start): forward `Lane:`/`Closed:` fields in [`closure_record.md`](.claude/skills/brief-authoring/references/closure_record.md) (notice `git show 103365f5:docs/notes/notice/N-2026-08-11-q-score-1-forward-fields.md`); same grammar serves queued coverage-limb promote-to-HARD ADR. Block 2 still gated — re-entry needs fresh recount ≥80% under a new campaign id. No retro-edits of undated closures. [`BLOCK1_RESULTS`](lab/archive/approach_scoreboard_2026-08/BLOCK1_RESULTS.md) · [`PREREG`](lab/archive/approach_scoreboard_2026-08/PREREG.md) · [`closure`](docs/briefs/closures/Q-SCORE-1-closure-falsified.md)
- **2026-08-11** — **`Q-MCLTAS-1` closed `FALSIFIED` (Wall B magnitude) at $0/K=0 — the probe was never run.** Operator-authorized Stage 0a+0b (both free) against a pre-registered two-wall gate. **Wall B dispositive:** Req-5 hurdle 11.60 ticks = **14.87 bp** vs the estate causal-public δ ceiling **3.21 bp** (4.63×; floor 3.01×; 3.04× under the forbidden bare-commission ablation); in cohort-bound δ/σ against MCL's own **measured** σ surface, required 0.62–1.35 vs D5's committed 0.113/0.194 → **floor 3.2×, defensible 7.0×**. **Wall A:** {free ∧ signed ∧ exogenous ∧ window-aligned} sign sources **EMPTY** (TAS volume gross by construction; no CME settlement-window imbalance print — the structural asymmetry vs equity closing auctions); one entitled-costed route unverified and unable to reach Wall B. **Corrects the ENV-1 reading in both halves** — non-circularity is scoped to decay observables, and the cell was never "blocked on δ alone". Discharges the 2026-08-11 item-(b) ruling's probe requirement negatively. Registry row filed; MCL the instrument NOT rejected. [`closure`](docs/briefs/closures/Q-MCLTAS-1-closure-falsified.md) · [`RESULTS`](lab/analysis/c1/cheap_falsifiers_2026-08/_probe_stage0_RESULTS_2026-08-11.md)
- **2026-08-11** — **`Q-TNEC-ENV-1` post-closure rulings (JA, light record).** (a) MGC calibration row **KEPT** — calibration/known-answer, not re-litigation; R8 re-proposal bar unmodified. (b) MCL TAS re-open **CONFIRMED, narrow** — BE3's fade-scoped kill does not bar a TNEC-limb-scored TAS candidate; direction re-opens **only through a completed δ-extraction probe** (free CME TAS volumes, non-circular) — live, unowned next step; full intake chain still applies. [`closure`](docs/briefs/closures/Q-TNEC-ENV-1-closure.md)
- **2026-08-11** — **`Q-TNEC-ENV-1` closed `NULL` (H_B=0, STOP per PREREG F7) at $0.** Census pass (56 cells, 19 entries scored: 2 authored + 17 prior-census re-scores) found 0 SEED-GRADE; envelope (RESULTS.md §2) stands as documentation only. Key findings: mandated flows mostly name a spread direction an outright envelope can't admit; the re-scored 2026-07-26 census is δ-blind by its own construction; MCL settlement-window replication has a non-circular δ-probe route (CME TAS, free). Two items flagged for operator ruling, not adjudicated. Re-entry bar: new flow class or newly measured instrument, never a re-pass. [`closure`](docs/briefs/closures/Q-TNEC-ENV-1-closure.md) · [`RESULTS`](lab/archive/tnec_envelope_compile_2026-08/RESULTS.md)
- **2026-08-11** — **`Q-TNEC-ENV-1` Phase A executed at $0.** TNEC envelope compiled for {MNQ, MYM, MES, MGC, M2K, MCL, M6A}; H_A **NON-EMPTY**. Phase B census pass authorized (PREREG F7). [`RESULTS`](lab/archive/tnec_envelope_compile_2026-08/RESULTS.md) · [`PREREG`](lab/archive/tnec_envelope_compile_2026-08/PREREG.md)
- **2026-08-10** — **Temporal selectivity ruled OUTSIDE the mapped cost-ratio levers (`TEMPORAL-SELECTIVITY-OPEN-2026-08-10`, JA); dense-1m lane door-check REPAIRED.** "instrument-selection" = **cross**-instrument (provenance: cross-index RV dilution, +2.64 vs +5.19 bp) — within-instrument *moment* choice was never mapped ⇒ route ① open, under a priori-criterion + K-per-axis + F2-guard conditions. Price/hold-time stay exhausted; cross-index stays closed. Lane step **1a** now requires the executed profile consult (exit 1 when a prior binds) with every `BINDING BAR` answered by route — unanswered blocks the G0 freeze. Cell #3 is unblocked but **unauthored**; fresh Q-ID + G0 + explore GO is the path. [`ADR`](docs/adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md) · [`lane spec`](docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md)
- **2026-08-10** — **Dense-1m cell #3 cheap falsifier → `FALSIFIED` (exit-geometry lever) at $0; no G0 authored, no Q-ID spent — and the lane WAS blocked on an unbinding-gate finding (ruled + repaired same day, above).** Stop width cannot rescue the family (0.02–0.10× the 5.64-pt 4× bar across the whole ratified 5–20 pt band; CON-2's own basis 0.16–0.17×). Surviving lever is **trade count** — a once-per-session rule needs only **3.3%** of the perfect-foresight oracle (170 pt/session) vs ~20% at CON-2's ~6/day. ⚠ **The lane spec / CON-1 / CON-2 never cite the live `tier=always` [index-intraday-OHLCV raised bar](docs/rejected_candidates.md)** — both prior campaigns ran unbound (`lesson_gate_reachability_preregistration`, unbinding form, **5th firing**). Cell #3's only surviving design is OHLCV price-selectivity ⇒ fails the bar's route ①; route ② PAUSED (L1); route ③ unclearable ex ante. **Two operator items owed: a domain-bar ruling on within-instrument temporal selectivity, and the step-1 door-check repair.** [`falsifier`](lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_cost_geometry_2026-08-10_LOG.md) · [`lane spec intercept`](docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md)
- **2026-08-10** — **`Q-TNEC-CON-2` explore GO → `AMBIGUOUS-HOLD` (non-promotable) at $0.** Compression→break, dense-1m MNQ @ G=10: long net **−0.0507R** (n=4,321) / short **−0.0440R** (n=4,108), CIs straddle 0; **gross +0.90/+0.97 pt/trade eaten by the 1.41-pt RT** (0.65× vs 4×); halves sign-flip both arms. CONFIRM (2025-09-01→2026-08-05) reserved+unread; split+placebo+downgrades declared at GO pre-score; Cap not claimed; K=1 disclosure. Cell #3 needs a fresh G0 aimed at cost geometry. [`closure`](docs/briefs/closures/Q-TNEC-CON-2-closure-ambiguous-hold.md) · [`RESULTS_g2`](lab/analysis/c1/mnq_tnec_con2_compression_break_2026-08/RESULTS_g2.md)
- **2026-08-10** — **`implied_annualized_sr` PROMOTED report-only → gate (`IMPLIED-SR-GATE-2026-08-10`, JA in-session); Tradeify-native fade design-region CLOSED on its own arithmetic.** Freeze-time limb for any assumed-edge region (ceiling 1.83 CFD-era, futures-native 0.89 disclosed); measured-edge candidates untouched (DSR-at-K governs). Floor 2.98 as-ruled / 2.11 elective-ablated — zero admissible cells either way. $0/K=0. [`ADR`](docs/adr/2026-08-10-implied-sr-plausibility-gate.md)
- **2026-08-09** — **GRAND tier `Accepted` + GSUB-1 CLOSED `RESOLVED-LOADBEARING` (JA in-session, same day).** Quintessentials bound above STRATEGIC (pursuit domain; PARK re-entry+expiry; SUBTRACT armor; intake rule). 37-row inventory → **19 dispositions ratified** (8 PARK · 9 SUBTRACT · 2 MERGE) → 37 records at `docs/pursuits/`; 3 user-skill dirs archived+removed; ADR §4 satisfied (sunset did not arm). $0/K=0; no live-risk surface touched. [`ADR`](docs/adr/2026-08-09-grand-tier-quintessentials-binding.md) · [`closure`](docs/briefs/closures/GSUB-1-closure-resolved-loadbearing.md)
- **2026-08-09** — **`Q-MNQDTL-CON-1` explore GO → `FALSIFIED` (STOP catalogue) at $0.** ES−NQ 5m log divergence @ G=10 session-flat: long mean_R **−0.106** CI entirely &lt;0 (n=10,093); short **−0.111** (n=9,000); stop ~91%; TNEC `U U U F U`. Cap not claimed. [`closure`](docs/briefs/closures/Q-MNQDTL-CON-1-closure-falsified.md) · [`RESULTS`](lab/archive/mnq_con1_dense1m_stage0_2026-08/RESULTS.md)
- **2026-08-09** — **`Q-MNQDTL-CON-1` ENTRY named + explore harness wired.** ES−NQ 5m log-return divergence (relative contrarian) frozen in [`PREREG_G0`](lab/archive/mnq_con1_dense1m_stage0_2026-08/PREREG_G0.md); cheap falsifier `CHEAP_FALSIFIER_OK`; path-PnL scorer GO-gated (now discharged). Cap not claimed. PR [#699](https://github.com/Joshua-Asante/first-passage-archive/pull/699).
- **2026-08-08** — **PR693 parallel integrate:** CapFLOW Cap-spend path **BLOCKED** on join (estimate ~USD1.47 OK; Cap held). Construct Stage-0 geometry frozen; ENTRY later named 2026-08-09 (see above). [Cap RESULTS](lab/analysis/c1/mnq_capflow_orb_r_2026-08/RESULTS.md) · [Con PREREG_G0](lab/archive/mnq_con1_dense1m_stage0_2026-08/PREREG_G0.md) · PRs #695/#697/#696/#699
- **2026-08-08** — **TNEC-1 intake gate `RATIFIED` + edge-cohort ADR `Accepted` (§8 JA).** TNEC supersedes MNQDTL-1 **as intake gate** (MNQDTL stays RATIFIED historical; C1–C11 stand). `Q-CAPRES-2` reservation GO signed; Cap-spend / CapFLOW unpaid. Construct Stage-0 geometry frozen; ENTRY named 2026-08-09 (see board top). [`ADR`](docs/adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md) · [`TNEC-1`](docs/spec/2026-08-08-tradeify-necessary-conditions-target-spec.md) · [`Q-CAPRES-2`](docs/briefs/Q-CAPRES-2-mnq-cap-seat-reservation.md) · [`Q-MNQDTL-CON-1`](docs/briefs/Q-MNQDTL-CON-1-dense-1m-em-construct-scoping.md)
- **2026-08-08** — **Absolute path items 1–3 landed:** `Q-MNQSEL-2` Phase-0 `RESOLVED` (dense 1m G=10; S3 ≈0.858 both arms); `Q-CAPRES-2` Cap reservation unpaid + CapFLOW PREREG frozen unpaid; `Q-MNQDTL-CON-1` construct scoping unpaid; `Q-R2FLOW-1` closed FALSIFIED. $0 / Cap not re-spent. [`MNQSEL-2 RESULTS`](lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/RESULTS.md) · [`Q-CAPRES-2`](docs/briefs/Q-CAPRES-2-mnq-cap-seat-reservation.md) · [`Q-MNQDTL-CON-1`](docs/briefs/Q-MNQDTL-CON-1-dense-1m-em-construct-scoping.md)
- **2026-08-08** — **`Q-R2FLOW-1` explore GO → G2 `FALSIFIED` (STOP catalogue) at $0.** Clock-minute net signed aggressor size→60s mid: n **48,360**/48,360 coverage **100%**; ρ **−0.000701** CI includes 0; empty candidates. CONFIRM untouched; Cap not claimed. Re-proposal = new G0. [`RESULTS_g2`](lab/archive/mnq_r2flow_routeb_2026-08/RESULTS_g2.md) · [`brief`](docs/briefs/Q-R2FLOW-1-signed-minute-flow-route-b-scoping.md)
- **2026-08-08** — **`Q-R2AGRUN-1` CLOSED non-promotable (`AMBIGUOUS-HOLD`); `Q-R2FLOW-1` G0 frozen — explore GO unpaid.** Clock-minute net signed aggressor size → 60 s mid; K=1; OFCHAN cache; S6 ADMIT; Cap not claimed. [`closure`](docs/briefs/closures/Q-R2AGRUN-1-closure-ambiguous-hold.md) · [`brief`](docs/briefs/Q-R2FLOW-1-signed-minute-flow-route-b-scoping.md) · [`PREREG_G0`](lab/archive/mnq_r2flow_routeb_2026-08/PREREG_G0.md)
- **2026-08-08** — **`Q-R2AGRUN-1` explore GO → G2 `AMBIGUOUS-HOLD` (ITERATE) at $0.** Aggressor-run→60s mid: n **22,304,297**/22,304,297 coverage **100%**; ρ **−0.001306** CI excludes 0 / placebo PASS; \|ρ\| < 0.02 → empty candidates. CONFIRM untouched; Cap not claimed. [`RESULTS_g2`](lab/analysis/c1/mnq_r2agrun_routeb_2026-08/RESULTS_g2.md) · [`brief`](docs/briefs/Q-R2AGRUN-1-aggressor-run-length-route-b-scoping.md)
- **2026-08-08** — **`Q-R2AGRUN-1` G0 frozen (MNQDTL R2) — signed aggressor-run trade-count → 60 s mid; explore GO unpaid.** K=1; `N_min=2` a priori; OFCHAN `tbbo` cache reuse; CONFIRM `2025-09-01→2026-02-06`; S6 ADMIT; Cap not claimed. [`brief`](docs/briefs/Q-R2AGRUN-1-aggressor-run-length-route-b-scoping.md) · [`PREREG_G0`](lab/analysis/c1/mnq_r2agrun_routeb_2026-08/PREREG_G0.md)
- **2026-08-08** — **Quarterly dd_protection/regime review run: item 1 (C2→C0 revert check) confirmed dead, removed from the `fwd-quarterly-regime-ddrevert` cron.** Re-verified via direct execution: `time_to_pass.py --regime-check` now hard-errors (Pepperstone anchor retired), consistent with the 2026-07-22 D2 retirement — not a new decision, just closing the loop the cron kept re-asking. Item 2 (H1 HOLD §4 regime trigger) re-run: limb-2 reachability still `NOT_EXECUTABLE`; full-panel de-risk candidates re-confirmed `GATE FAIL` byte-identical to the ADR. HOLD unchanged; no `core/` edits. [`decompound ADR`](docs/adr/2026-06-07-decompound-remc-hold.md) · [`claims-rescope ADR`](docs/adr/2026-07-11-challenge-era-claims-rescope.md)
- **2026-08-08** — **ADR ceremony stakes-tiering `Accepted` (JA).** Full §0–§7 only when a limb fires (K/$ · live-risk · locked/non-regenerable · doctrine); else ≤300-word light record, same header block. Falsifier ≥⅕ light share + zero omitted-apparatus incidents, review rides first quarterly audit after 08-08. Forward-only. [`ADR`](docs/adr/2026-08-08-adr-ceremony-tiering.md)
- **2026-08-08** — **`Q-R2VBUCK-1` explore GO ratified (MNQDTL R2) → G2 `FALSIFIED` (STOP catalogue) at $0.** Volume-bucket aggressor→60s mid on OFCHAN EXPLORATION cache: n **77,656**/77,656 coverage **100%**; ρ **−0.005478** CI includes 0; empty candidates. CONFIRM untouched; Cap not claimed. Re-proposal = new G0. [`RESULTS_g2`](lab/archive/mnq_r2vbuck_routeb_2026-08/RESULTS_g2.md) · [`brief`](docs/briefs/Q-R2VBUCK-1-volume-bucket-aggressor-route-b-scoping.md)
- **2026-08-08** — **SPEC S2b `Accepted` + S2b build ADR `Accepted` + operator build GO.** Daemon minimal spec Accepted as-is ($0); build ADR locks Databento Live `ohlcv-1m`, `2×bar_period+30s` staleness, fail-closed-all, second Fly app `c1-signal-daemon`, emit-disabled default. Build GO licenses code + warm deploy only — no arming, no Striker redeploy, no M1 fabrication. [`SPEC S2b`](docs/spec/2026-08-07-loop-s2b-python-signal-daemon-spec.md) · [`build ADR`](docs/adr/2026-08-08-s2b-signal-daemon-build.md)
- **2026-08-07** — **Loop S1 environment ratification `Accepted` — F2+F3 ruled.** Incumbent `Tradeify_Select_100K` eval = environment for **new** strategies; rail kept warm/disarmed there; no successor migration now; Q-VENUEGEO-1 evidence recorded, unconsumed; withdrawn Striker legs stay barred. Board F2/F3 rows cleared. MNQDTL-1 R1 foreclosed; R2 live. $0/K=0/no arming. [`S1 ADR`](docs/adr/2026-08-07-loop-s1-environment-ratification.md) · [SPEC S1](docs/spec/2026-08-07-loop-s1-environment-ratification-spec.md)
- **2026-08-07** — **Closed-loop programme spec series S1–S6 `PROPOSED` + minimal-spec style ratified as the standing `docs/spec/` convention (JA).** Eight files: [template](docs/spec/TEMPLATE-minimal-spec.md) · [index](docs/spec/2026-08-07-loop-spec-index.md) · S1–S6 (environment ratification → signal-host fork → two-tier arbiter → sensor layer → bounded promotion lane → K-aware generation). Commissions only — admits nothing, arms nothing, spends nothing; $0/K=0. S1 direction (same day) later Accepted as the F2/F3 ADR above. S5 commissions a supersedes-in-part ADR on lifecycle Call 5 / M1 §5 / harvest §1 — **nothing is superseded until that ADR is Accepted**. 9-agent adversarial verification (25 findings, 5 BLOCKERs) applied pre-commit. **Same day: blast-radius sweep (7 agents) → [S7 alignment spec](docs/spec/2026-08-07-loop-s7-repo-alignment-spec.md) + propagation manifest (`git show 45e3ceac:docs/notes/2026-08-07-posture-a-alignment-manifest.md`) (~70 rows, 12 triggers); NOW repairs landed — S1 pointers on board rows 1/3, minimal-spec row in brief-authoring, gate-14 §4 friction datum #1 logged (Iterate ADR ledger) + Q-CAPA-1 `Board write:` token fixed.**
- **2026-08-07** — **`Q-MNQSEL-1` Phase-0 RUN → `FALSIFIED` (C2) at $0/K=0 — STOP this restart-clock universe.** Oracle top-1/day S3 long **0.3998** / short **0.3984** (both &lt; 0.40); S1 ≈ **−0.036** both arms; S5 median target-hits ≈ **97–98**/day; S6 ≈ **99.7–99.9%**. Pre-registered C4 expectation wrong. Re-proposal = different causal candidate set. Cap untouched. [`RESULTS`](lab/archive/mnq_selection_ceiling_2026-08/RESULTS.md) · [`brief`](docs/briefs/rnd-pipeline/Q-MNQSEL-1-selection-value-ceiling-scoping.md)
- **2026-08-06** — **EM0–EM5 mechanism-shape screen `RATIFIED`; §7 dispositions locked; first Route B G0 drafted as `Q-OFCHAN-1` — G2 `VOID-COVERAGE` (empty candidates; STOP).** Screen [`docs/spec/2026-08-05-eval-mechanism-shape-screen.md`](docs/spec/2026-08-05-eval-mechanism-shape-screen.md) Status `PROPOSED` → `RATIFIED 2026-08-06` / JA; §7 rows 1–9 ruled. First Avenue A Route B campaign: [`Q-OFCHAN-1`](docs/briefs/Q-OFCHAN-1-orderflow-channel-route-b-scoping.md) + [`PREREG_G0`](lab/analysis/c1/mnq_ofchan_routeb_2026-08/PREREG_G0.md) — K=1 L1 flicker-filtered imbalance → 60s mid return on `MNQ.v.0` RTH grid; EXPLORATION batch complete; **G2** [`RESULTS_g2`](lab/analysis/c1/mnq_ofchan_routeb_2026-08/RESULTS_g2.md) coverage **7.36%** → VOID-COVERAGE → empty list → STOP this catalogue (new G0 to reopen). Cap seat not claimed. CONFIRM untouched.

> ⚠ **Truncated to the newest 15 at the 2026-08-08 Great Prune.** Older executed decisions are
> owned by their ADRs (`docs/adr/`, tombstoned rows in [`TOMBSTONES.md`](docs/adr/TOMBSTONES.md));
> full prior index: `git show pre-prune-2026-08-08:STATE.md`.

## Dormant cross-session threads

Open investigations with no current session home. Closed threads leave (owners =
closures/ADRs).

Dormant threads b6/b7 (PARK — open) → [`docs/pursuits/`](docs/pursuits/) (ratified 2026-08-09, GSUB-1
Phase 3). c5/Q-MSCHAN-1 (SUBTRACT — dead) left this section per its own rule above; its record
stands alone at [`c5`](docs/pursuits/c5-q-mschan-1.md).

**Registry backfill debt (2026-08-15).** 33 closures classified as strategy-grounds kills
(read against each one's actual `**Verdict:**` line, not filename) never got a
`rejected_candidates.md` row — the 2026-08-03→08-11 feed-stop the registry-feed sub-rule
(9) was written to close. Forward-only: nothing new accretes here. Backfill is one
judgment call per row (which heading, how it's worded) and stays operator-paced —
`python scripts/check_closure_disposition.py --list-debt` lists the current set;
rows leave this debt only by landing in `docs/rejected_candidates.md`, not by editing
`REGISTRY_DEBT_2026_08` directly.

---

## Scheduled forward triggers

Canonical dates/criteria live with their owners; this board is a pointer so
obligations are not lost between sessions. Closed/retired/discharged rows are
deleted (not struck).

### Weekly — recurring (rolling; next deadline **2026-08-21**, bucket 08-17→08-21)

> Prior week 08-10→08-14 satisfied (operator-placed 2026-08-12). New week unpaid. Row stays
> live — roll this date forward each Monday. **Recurrence ruled 2026-08-16** (decision index,
> above): re-electing coverage every week is the standing design, not an open question — this
> row's own weekly cadence is that design in practice, not a symptom of anything unresolved.

- **Venue idle-clock — ≥1 operator-placed trade per Mon–Fri week on the live account (identifier
  redacted from the public tree).**
  Consequence of a miss is account **DELETION, not a warning** (Tradeify art. 10468318; venue day
  is 6pm-anchored, so a Fri 18:30 ET fill belongs to the *next* session). ⚠ **No agent may place
  it** — operator-placed at the venue; the rail is not the instrument (`dry_run` stays `true`).
  **Roll this date forward each Monday.** Booked here 2026-08-09 *specifically so the existing
  daily 07:04 `daily-repo-truth-sync` forward-obligation radar surfaces it* — that task reads this
  section for obligations dated within 7 days, and row 0's queue-table placement was invisible to
  it.   [`S1`](docs/adr/2026-08-07-loop-s1-environment-ratification.md) ·
  [audit FU-1](docs/notes/audits/programme-audit/2026-08-05-post-descope-claim-alignment-audit.md)

### No fixed date / gated

> ⚠ **Five threads are gated on first strategy-signal fill.** That gate is **an acceptable
> strategy**, not a missing venue. [`S1`](docs/adr/2026-08-07-loop-s1-environment-ratification.md)
> kept the incumbent `Tradeify_Select_100K` eval as the environment; the weekly idle-clock is
> live; there is no c1 book (locked Striker legs stay barred). **Q-SIGID-1** is **not** among
> them — pursuit standing **KEEP**, resolving via the S2b daemon; see [`c2`](docs/pursuits/c2-q-sigid-1.md).
> **Three have rows in the list below** — **PREREG-C1-DEDUPE-1**, **per-fill add-slippage
> capture (B7 Stage 2b)**, and the **forward regime-monitor successor**. **Two do not, and
> are re-homed here** because their only prior home was the deleted operator-queue row 3:
>
> - **lifecycle Call-1** — rolling-PF σ-source has no live data until a strategy is on the
>   book. Its 2026-08-08 review row below still stands but can only return AMBIGUOUS on thin data.
> - **ORB decay re-scope** — no other row in this file; recorded here so the deletion of queue
>   row 3 does not silently lose it.
>
> All five wait on the same thing as queue row 2 (B7 / M1). They are not closed, not
> discharged, and not re-homed to a successor venue — F3 was no-migration (S1).
> [`S1`](docs/adr/2026-08-07-loop-s1-environment-ratification.md) ·
> [`ADR 2026-08-04`](docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md) (Striker-book bar)

- **Sentinel Tier-2/3 promotion (limb B1)** — before next quarterly slate; promotion not a build. [`sentinel design`](docs/spec/2026-06-23-inqhiori-sentinel-design.md) · [`Hermes closure`](docs/briefs/closures/2026-07-27-hermes-agent-adoption-closure-resolved.md)
- **PREREG-C1-DEDUPE-1** — gated on M1 `RESOLVED` + separate operator GO. [`pre-reg`](docs/spec/PREREG-C1-DEDUPE-1-intent-key-functional-property.md) · [`impl plan`](docs/spec/PREREG-C1-DEDUPE-1-implementation-plan.md)
- **R&D tooling T2 / T3 / T4** — adoption ADR §7 (T4 rides 2026-08-08 Call-1 OC). [`ADR §7`](docs/adr/2026-07-11-tradable-anomalies-statistics-adoption.md)
- **Per-fill add-slippage capture (B7 Stage 2b)** — waits first strategy-signal **add** fill; prerequisite ledger price-capture landed. [`Q-COSTGEO-3`](docs/briefs/closures/Q-COSTGEO-3-closure-ambiguous-needs-depth.md) · B7 procedure in the private archive
- **Forward regime monitor / decompound limb-2 successor** — ORPHANED same hole: CFD limb-2 cannot fire; venue-native design landed (not ratified); gated on first live fill. [`decompound ADR §Addendum 2026-08-03`](docs/adr/2026-06-07-decompound-remc-hold.md) · [`Pepperstone retirement`](docs/adr/2026-08-02-pepperstone-feed-retirement.md)
- **CFD data-estate class-wide delete** — trigger-dated; blocked on T1 (F3 FUTURES_LOCK) + substrate Phase-6 confirm. [`CFD estate ADR`](docs/adr/2026-07-11-ops-cfd-estate-retirement.md) · [gate audit](docs/notes/audits/2026-07-17_gate_cfd-estate-classwide-delete.md)
- **Mechanism-sourcing radar** — on-demand cadence; 08-08/11-08 = progress/idle checkpoints; idle guard 2026-11-08. [`harvest §2`](docs/methodology/strategy_harvest.md)
### 2026-08-08 — DISCHARGED

> ✅ **The quarterly vehicle ran 2026-08-08.** Verdicts, the full rider partition
> (2 discharged / 37 owed / 3 moot / 5 unfalsifiable of 47), the unfalsifiable-check census, and
> every named follow-up now live in
> [`2026-08-08-quarterly-audit.md`](docs/notes/audits/programme-audit/2026-08-08-quarterly-audit.md).
> The former ~90-line rider blockquote is deleted per the retention test — it restated obligations
> the audit note now owns. **Operator rulings still open** are carried as queue rows, not here.

### 2026-10-11 (approx.)

- **prop_envelope §4 overlay 90-day re-verify** — rows verified 2026-07-13; stale after ~2026-10-11. [`prop_envelope`](ops/prop_envelope_default.md) · [`ratification ADR`](docs/adr/2026-07-13-prop-envelope-v1-ratification.md)

### 2026-11-08

- **ADR ceremony-tiering §Falsifier review** — first quarterly programme audit after 2026-08-08; check light share ≥⅕ and dated omitted-apparatus incidents (incl. 2026-08-14 candidate: implied-SR light records). Count 1-vs-2 is operator/audit. [`ADR addendum`](docs/adr/2026-08-08-adr-ceremony-tiering.md)
- **GRAND-tier ADR §4 scheduled re-read** — H already satisfied 2026-08-09 (19 ratified differences; tier load-bearing, sunset did **not** arm). This slate is the first scheduled re-check, not a sunset. [`ADR addendum`](docs/adr/2026-08-09-grand-tier-quintessentials-binding.md) · [`closure`](docs/briefs/closures/GSUB-1-closure-resolved-loadbearing.md)
- **GSUB-1 PARK expiries (6)** — b1 Aegis→6J · b3 ORB-MNQ line · b5 Q-FUNDPOL-1 · b6 Q-NAS-ECR-1 · b7 ICT line · c3 Q-TOM-SPX-1. Each converts to SUBTRACT absent explicit operator renewal (ADR §2.3). b2 (Striker-MYM) and c1 (Q-XMEM-1) already resolved to `SUBTRACT` early via GSUB-2 (2026-08-19, ~80 days ahead of this expiry) — dropped from this row, not still pending. [`docs/pursuits/`](docs/pursuits/)
- **Guardian-MGC (R7) transfer lane — SUBTRACT / DEAD(N-SURV) 2026-08-11** — exploratory N-SURV FAIL (full 42.2% / H1 72.4% / H2 16.5% bust vs ≤3.0%); margin-decisive; retroactive cell PREREG + typed closure filed. Re-entry = new mechanism evidence (not param retune). [`b8`](docs/pursuits/b8-guardian-mgc-transfer-lane.md) · [`closure`](docs/briefs/closures/2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md)
- **Prop-portfolio §4 primary falsifier (HARD)** — ≥1 candidate clears bust ceiling on ≥2 of 4 FRIENDLY firms; else demote program to research-only. Status undischarged (2026-07-22 withdrawal). [`four-firms ADR §4`](docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md) · [`withdrawal ADR`](docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md)
- **Mechanism-boundaries ADR §4** — clauses 2-A / 2-B / 2-C first check. [`ADR`](docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md)
- **Harvest-intake §4 doctrine falsifier + idle guard** — limb 1 still 0-of-2; limb 2 `Accepted` (R10 GO); pin marked `no`; post-mark count 0/2 (not fired). Idle = zero screen-PASS seeds beyond D5. [`harvest ADR §4`](docs/adr/2026-07-15-external-mechanism-harvest-intake.md)
- **Regime-monitor successor §6 gate** — if no live fill by 11-08, gap is ≥3 months; re-raise as standing-unfalsifiable in that programme audit. [`decompound ADR`](docs/adr/2026-06-07-decompound-remc-hold.md)
- **Blind-channel §4 reading** — sourced-vs-empty (`AMBIGUOUS-HOLD` if still unsourced); disclose pre-G0 count and whether N fired; analogue-modality ruling re-test (inert if no analogue manifest). Owner: [channel ADR](docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md) · [analogue ruling](docs/adr/2026-08-15-analogue-modality-route-ruling.md)
