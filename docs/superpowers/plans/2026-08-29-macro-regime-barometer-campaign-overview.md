# Macro Regime Barometer Campaign — Overview & Phase Index

**Status:** `AWAITING GO` — authored 2026-08-29 at operator request (the dedicated
regime-awareness scoping session that
[`N-2026-08-28`](../../notes/notice/N-2026-08-28-regime-conditionality-cross-cutting-forward-item.md)
§6 names as its re-check trigger). **Each phase carries its own GO gate; nothing below is
authorized by this overview.** Queue-bind note: under the queue-led convention, phase GOs
function as operator promotions. This campaign holds **no STATE queue row** and queues behind
the live rows ([Survive-bound ADR](../../adr/2026-08-09-survive-bound-is-the-queue-cap.md));
authoring this plan is neither a promotion nor a GO. The notice stays `HOLD` until the Phase-1
Pre-Q opens (see §Governance mechanics).

**Loop-of-Record:** STRATEGIC (this plan) wrapping **≤3 constituent OUTER INQHIORI
investigations** — the Rule-2 STRATEGIC budget, exactly consumed by Phases 1–3
([canon §14–§15](../../methodology/inqhiori-canon.md);
[Rule-2 ADR](../../adr/2026-06-16-rule-2-budget-before-acting.md)). Each constituent
investigation is OUTER (budget 8 iterations, no self-extension) and declares its own D-S-A
domain (data) in its Pre-Q. Phase 4 is a build (system-domain, The Algorithm post-H), not an
OUTER investigation, and sits outside this budget behind its own operator GOs.

**Objective:** decide, through at most three pre-registered investigations, whether a
**cross-asset market-state barometer** — a small state vector estimated forward-only from data
the estate already holds, consumed **down-only** as participation/sizing conditioning — is
real, estimable, and worth integrating for the futures-era estate; and exit through a **typed
terminal state**: an `INTEGRATE` closure handing a frozen entry packet to an integration build,
or a typed `STOP` with explicit re-proposal bars. Terminal success is a Phase-3 closure whose
frozen gates included: measured reduction of hostile-state intraday-honest bust on ≥2 named
consumption targets, with median-days-to-pass degradation and benign-state drag inside frozen
bounds (exact numerals frozen in the Phase-3 PREREG before any consumption run — this overview
deliberately does not pick them). Every non-INTEGRATE exit below is a **designed outcome, not a
process failure**.

---

## §1 The reformulation — why this is not attempt N+1

**The record.** The regime-detection domain was SNAG-closed 2026-06-28 after 9 consecutive
nulls ([`rejected_candidates.md`](../../rejected_candidates.md) §SNAG; audit
`docs/notes/audits/programme-audit/2026-07-01-portfolio-audit.md`). What failed, specifically:

- **Per-trade outcome classifiers** — Q-REGIME-AEGIS-1: USDJPY trend-persistence vs Aegis
  win/loss, AUC ≈ 0.499 ([`6J.md`](../../../ops/instruments/6J.md) J6). Its own RESULTS invoked
  INQHIORI §6: no third same-level detector.
- **Free exogenous leading indicators vs book episodes** — the regime-signal battery + its
  extension: 14 candidates across 4 families (NFCI, MOVE, HYG/LQD, VIX-term, VVIX, SKEW, DSPX,
  COR1M/3M, breadth, DIX, GEX…), all null at N=33 episodes; free option-implied signals are
  empirically **coincident, not leading**
  (`lab/archive/regime_signal_research_2026-06-25/CLOSURE.md`).
- **A cross-asset vol/liquidity composite** — Q-REGIME-COND-1 (VIX + HYG/LQD + MOVE + DXY,
  point-in-time): FALSIFIED — its forward second-moment content on SPY is repackaged trailing
  volatility (corr +0.648 with trailing 20d RV; residual states placebo-indistinguishable;
  median state dwell 3–4 days, flipping faster than the horizons it predicted)
  (`lab/archive/regime_cond_2026-06-30/FINDINGS.md`).
- **Vol-level brakes** — the VIX>20 T2b brake left H1 bust at 18.00% and pushed median pass
  time to 127d (`lab/archive/regime_remc_2026-06-22/RESULTS.md`): the hostile window is
  substantially **low-vol chop**, so vol-class axes flag the wrong regime.
- **Trailing classifiers on the one measured futures-era break** — vol and mean-R classifiers
  for ORB-MNQ's 2021-09-28 break, both refuted
  ([`Q-ORBCUSH-1 closure`](../../briefs/closures/Q-ORBCUSH-1-closure-falsified.md);
  [`MNQ.md`](../../../ops/instruments/MNQ.md) N17).

The notice's §4-C ("a cross-asset, volatility/liquidity-based signal … has not been tried") is
**too strong as written** and no Pre-Q in this campaign may repeat it: Q-REGIME-COND-1 was that
construction. What has genuinely never been tried is pinned by three axes, and a constituent
investigation that abandons any of them collapses back into the closed thread:

| Axis | Every closed attempt | This campaign |
|---|---|---|
| **Target variable** | CFD book's N=33 co-drawdown episodes (retired, unextendable) · SPY forward moments · one strategy's per-trade W/L · challenge pass-rate | The **futures-era estate's own survival object**: state-conditional edge coherence and intraday-honest bust geometry on the MNQ/MYM/6J/M6A/HG/MGC/MCL/M2K panels |
| **Unit of analysis** | Single signal → single outcome separation (AUC, episode rank) | A **state vector + per-mechanism-family exposure map** — coherence of many edges' measured conditional performance under one low-dimensional state |
| **Consumption bar** | *Leading* prediction (peak-sampled episode severity; per-trade AUC) | **Nowcast + persistence**: concurrent state estimate whose dwell time exceeds the participation/sizing horizon — the bar participation analysis showed survives imperfect detection (`regime_stress` step 4: regimes are persistent multi-year blocks; deploy/wait viable; and the Dacco-Satchell qualifier: sizing uses can add value despite imperfect detection) |

**The barometer is a vector, not a dial.** The estate's own record refutes a binary
good/bad-regime dial: the Aegis/Guardian family dies in 2020–23 chop, but NAS100-ORB was
negative every year 2014–2019 and positive in 2021–22, GER40-ORB's best year was 2022,
BTC trend-propensity was strongest in 2020–22, SPX turn-of-month existed *only* in the COVID
window, the M6A/HG candidate was strongest in 2022–23 and dead by 2025, and ORB-MNQ's
confirmed failure year is 2026 (per-ledger citations in §Phase-1). A state under which these
are *coherent* — each mechanism family carrying a stable state-conditional loading — is the
falsifiable object. "H1 bad / H2 good" is not.

**New evidence since the SNAG closure** (what licenses re-entry at all): the notice's
four-candidate cross-asset assembly on futures-era, non-CFD measurements (assembled 2026-08-28,
after the 2026-06-28 closure); the M6A/HG registration
(`core/tv_export_loader.py`, commit `7bdfa1d`); the N20 corrected anchored apparatus — the
closest thing to a positive in the record: mean-R separation of the 2021-09-28 break clears
decisively at W3 (59.4pp, direction stable across all windows), failing only the
association-strength floor at shorter windows ([`MNQ.md`](../../../ops/instruments/MNQ.md)
N20); and the M-Q-REGIME-1 2024-04-30 structural-inflection lesson (+2.06σ multi-boundary
discriminator, never investigated —
[`methodology_lessons.md`](../../methodology/lessons/methodology_lessons.md) M-Q-REGIME-1).

**Alternatives considered and rejected** (recorded so the choice is auditable): a
detector-first campaign (pick signals, test against outcomes) repeats the closed thread's
shape; a consumption-first campaign on hindsight labels licenses nothing forward and inverts
the dependency (consumption value is only meaningful for an estimable state — though hindsight
consequence-weighting is embedded in Phase 1); a single compressed OUTER loop conflates three
distinct falsifiable hypotheses (brief-authoring trap #11 — multi-question briefs split).

---

## §2 Phase index

| Phase | Constituent Q | Cost | Gate to start | Serial dependency |
|---|---|---|---|---|
| **0 — Governance packet** | — (this doc + pursuit entry record) | $0 / K=0 | operator ratification of the pursuit record + plan | none |
| **1 — State or artifact?** (OUTER-1) | `Q-MACROSTATE-1` | $0 / K registered (axis set frozen) | Phase-0 ratified + operator GO (this GO also graduates the notice) | none |
| **2 — Causally estimable?** (OUTER-2) | `Q-MACROSTATE-2` | $0 (bars-level, existing panels) | Phase-1 `STATE-COHERENT` + operator GO | Phase-1 reference segmentation + exposure map |
| **3 — Worth consuming?** (OUTER-3) | `Q-MACROSTATE-3` | $0 (reuses committed trade/daily-P&L artifacts + `core/mc`) | Phase-2 `RESOLVED` + operator GO | Phase-2 frozen nowcast |
| **4 — Integration build** | — (build, not an investigation) | design $0; build TBD | Phase-3 `INTEGRATE` closure + doctrine ADR + the two named operator rulings (§Phase-4) | Phase-3 entry packet |

Per-phase full plan documents are **authored at each GO, not now** — a deliberate deviation
from the viable-strategy pattern (which authored all phases up front): Phases 2–3 designs are
functions of Phase 1's verdict, and pre-authoring them would fail the retention test
([`operational_rules.md`](../../operational_rules.md) §Retention). Each phase opens as a
standard Pre-Q per
[`brief-authoring`](../../../.claude/skills/brief-authoring/references/inquire_brief.md) with
canon §3 headers, a frozen verdict pre-registration under `docs/briefs/pre-registration/`, a
campaign body under `lab/analysis/regime/<slug>/` with `PREREG.md`, a `register_search open`
manifest before any results are examined, a `gate-reachability-audit` pass at freeze, and a
typed closure under `docs/briefs/closures/`.

---

## §3 Phase 1 — `Q-MACROSTATE-1`: Is there a shared market state, or a discovery-era artifact?

**Question (symptom-only).** The estate's measured edges show strong, mechanism-heterogeneous
period-conditionality — some die in 2020–23, some live only then, some die in 2025–26 — across
asset classes and eras. Is there a low-dimensional cross-asset market-state representation
under which these conditional performances become **coherent** (stable state-conditional
loadings per mechanism family), or is the pattern explained by **when and how the candidates
were discovered** (the notice's mechanism B), or by nothing beyond era labels?

**Evidence base (frozen inputs, no new spend).** The notice's four candidates plus the wider
per-ledger record, both signs:

- *Hostile-in-H1:* the locked CFD book (H1 bust 13.84% / H2 0.21% —
  [`allocation-refresh-2`](../../adr/2026-05-23-allocation-refresh-2.md) Addendum 2026-08-02);
  Aegis-6J1 (H1 n=41 −0.0614R vs H2 +0.2285R — `6J.md` J14/J15); Class-S 2-leg book (H1 always
  the worse half at every sizing/clock —
  `lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS_INTRADAY_W1.md`);
  Silver/5th-leg insertions amplifying H1 co-drawdown (`ops/instruments/XAGUSD.md` F3;
  `decompound_ddprot_2026-06-21`).
- *Counter-signed or differently-dated:* NAS100-ORB (pre-2020 negative every year; 2021–22
  positive — `ops/instruments/NAS100.md` N1/N7); GER40-ORB (best year 2022 — `GER40.md` G2);
  BTC trend (strongest 2020–22 — `BTCUSD.md` durable #1); SPX turn-of-month (COVID-only —
  `SPX500.md` F5/D6); M6A/HG (strongest 2022–23, dead 2025 — the notice §0); ORB-MNQ (break
  2021-09-28; confirmed-negative 2026 — `MNQ.md` N1/N4); 6J orb-ny (fails on 2025–26 OOS —
  `6J.md` J16); combined book (fatal half 2026-02→2026-08 —
  `lab/analysis/c1/aegis_orbmnq_combined_book_2026-08-26/RESULTS.md` §9.5/§10.2).
- *Regime-stable controls* (invariants a real state must NOT spuriously "explain"): MNQ 1m FVG
  retrace 58–60% every year including the 2020 crash and 2022 bear (`MNQ.md` W3); ICT weekly
  hit-rate stable across halves and thirds (`MNQ.md` N8).

**Candidate state axes (small set, frozen in the PREREG; selection among them is K).** Built
from the $0 surface (§Data): (i) cross-asset drift/efficiency; (ii) cross-asset trend
**breadth** (fraction of the universe trending under a frozen definition); (iii)
dispersion/correlation (`core/data/external/` COR3M/DSPX/SECTOR panels — retained 2026-08 "for
a future exogenous regime-signal probe"); (iv) vol level+shape — included as a **control axis
only** (known to flag crisis, not chop); (v) **macro-event axes** — scheduled-event density,
event-window share of realized range, post-event drift persistence, and policy-cycle state
from the pinned CPI/NFP/FOMC calendars plus the rates complex (ZN/ZF panels exist in-repo as
reference series); (vi) daily credit/liquidity axes via the resurrected
`lab/archive/regime_cond_2026-06-30/panel.py` fetchers. Single-asset gold KER failed as a
*gate* (`rejected_candidates.md` — gold KER/TSMOM); efficiency enters here only as one input
axis to a cross-asset state — the Pre-Q must argue this distinction explicitly.

**Load-bearing null (frozen now).** The state earns existence only if it (a) explains edge
conditionality **beyond era fixed effects** — a state that merely relabels 2020-vs-2023 is the
era-orthogonality wall replayed at the existence level — and (b) survives the trailing-RV
orthogonalization that killed Q-REGIME-COND-1. Full-sample (hindsight) segmentation is
**licensed in this phase only**, for existence testing; any forward claim belongs to Phase 2.
Face-validity anchors the segmentation must recover after the fact: 2020-02/03, the 2021-09-28
break, the 2022 rate-shock window, the 2024-04-30 inflection (M-Q-REGIME-1), the 2026 decay
window; cross-checked against the hand-verified regime calendar in
[`USDCAD.md`](../../../ops/instruments/USDCAD.md) §Regime calendar — the estate's only
existing macro-regime table.

**Artifact control (mechanism B).** The Pre-Q freezes a discrimination design before any state
is fit — candidate designs to choose from at authoring: era-stratified re-discovery (would the
same screens run on a different era have selected these candidates?), and synthetic candidates
tuned per-era as a selection-bias yardstick. If discovery-era selection explains the observed
conditionality, the campaign closes.

**Verdict (typed, frozen in the verdict prereg):**
`STATE-COHERENT` → Phase-2 entry packet · `ARTIFACT-OR-RELABEL` → campaign **STOP** (the
deliverable is a discovery-era selection-discipline lesson routed to
`futures-anomaly-discovery`; a barometer cannot fix a selection artifact) ·
`AMBIGUOUS` → structured stop, operator adjudication.

**Kill criteria (frozen now):** coherence indistinguishable from the era-FE null; or state
explains the regime-stable controls as strongly as the conditional edges (over-fitting
signature); or Rule-2 OUTER budget (8 iterations) trips.

---

## §4 Phase 2 — `Q-MACROSTATE-2`: Is the state causally estimable with actionable dwell?

**Question (symptom-only).** Every prior real-time regime estimate either collapsed into
trailing volatility, lagged its own flips, or flipped faster than any horizon it informed. Can
the Phase-1 state be estimated **forward-only** — and does the causal estimate retain Phase-1's
coherence at a dwell time longer than the participation/sizing horizon it would feed?

**Bar (the reformulated detectability question).** NOT per-trade AUC against strategy outcomes
(Q-REGIME-AEGIS-1's level — barred). Frozen gates cover: (a) filtered-vs-smoothed state
agreement on held-out data; (b) retained state-conditional edge coherence out-of-fit under a
pre-registered era split; (c) dwell-time distribution vs the declared consumption horizon —
the strike that felled Q-REGIME-COND-1 (3–4-day dwell), made a first-class falsifier; (d) the
two frozen orthogonality walls as load-bearing nulls: trailing-RV orthogonalization and
era-orthogonality (year-FE / within-era variation); (e) the corrected-null battery for
autocorrelated series — ACF-matched / IAAFT surrogates per
[`magnitude-persistence corrected-null spec`](../../spec/2026-08-18-magnitude-persistence-corrected-null-battery.md),
cited valence-blind in PREREG §0. A **coincident** nowcast passes; only *persistence* is
required — this is where the bar genuinely differs from the failed leading-indicator bar.

**Discovery discipline** (owned by `futures-anomaly-discovery`, binding): HMM state count by
held-out likelihood, never in-sample; **filtered (forward-only) probabilities** for every
real-time claim — full-sample decode is a look-ahead leak; ruptures penalty fixed by principled
criterion or the sweep pre-registered as K; seeds/restarts count toward K; states are
conditioning variables, never entries; intraday vol U-shape deseasonalized first.

**Verdict:** `RESOLVED` (nowcast + frozen spec → Phase-3 entry packet) · `FALSIFIED` → typed
**STOP**, re-proposal bar = the record's named unexhausted levers only (paid high-resolution
dealer-gamma family; more accrued episodes; a construction change that re-clears §1's three
axes) · `AMBIGUOUS` → structured stop.

**Kill criteria (frozen now):** fails either orthogonality wall; dwell median below the
declared horizon; held-out coherence retention below the frozen floor; OUTER budget trips.

---

## §5 Phase 3 — `Q-MACROSTATE-3`: Does consuming it improve survival at bounded cost?

**Question (symptom-only).** A real, estimable state is still worthless if acting on it costs
more than it saves — the T2b brake *worked as a detector of something* and still pushed median
pass time from ≤45d to 127d. Applied **down-only** (participation / sizing haircut, never
selection of individual trades), does the Phase-2 nowcast improve the estate's survival
metrics at bounded cost in pass-time and benign-state drag?

**Method ($0 by construction).** Counterfactual application to committed artifacts, per
mechanism family via the Phase-1 exposure map (not uniformly):
`lab/analysis/c1/aegis_orbmnq_combined_book_2026-08-26/data/` (trade lists n=32→1,503; daily
P&L JSONs), `lab/archive/transfer_expression_grid_2026-08/cells/striker_mnq/daily_pnl_nsurv.csv`
(the committed intraday-honest daily series), `lab/archive/q_pyrparity_1_2026-07/` venue-edition
trade lists, plus operator-held hash-pinned exports. Survival claims run through the production
intraday-honest MC path (`core/mc/`; [W1 ADR](../../adr/2026-08-07-w1-intraday-honest-engine-remeasure.md) —
EOD-clock figures are lower bounds and may not headline). Acceptance shape: both-halves +
block-bootstrap on the campaign's **own frozen gates** — the
[regime-robustness gate](../../methodology/regime_robustness_gate.md) is cited as
informational context only; per the
[2026-08-24 scope ruling](../../adr/2026-08-24-regime-gate-scope-worked-nonexample-f1-discharge.md)
it may not be imported as a rider with a pre-negotiated consequence.

**Frozen-bound structure (numerals frozen in this phase's PREREG):** hostile-state
intraday-honest bust reduction on ≥2 named targets; median-days-to-pass degradation bound
(the 127d lesson); benign-state drag bound; state-flip whipsaw cost accounted at the Phase-2
dwell distribution.

**Verdict:** `INTEGRATE` (entry packet → Phase 4) · `ITERATE` (names — never opens — a
successor: paid-data family, or barometer-as-measurement-tool-only) · `STOP` (barometer
archived as an after-the-fact measurement lens; re-proposal bar recorded).

---

## §6 Phase 4 — Integration build (outside the STRATEGIC budget)

Only on a Phase-3 `INTEGRATE` closure. A build, governed by The Algorithm (system domain), all
operator-gated: (1) a **doctrine ADR** — a barometer consumed as a gate/overlay input trips
ceremony-tiering limb 4; (2) the **M-A build-gate scope ruling** the operator already owes
([`STATE.md`](../../../STATE.md) §No fixed date — whether "first live fill" binds a pure
market-data observer): the barometer's natural first home is the M-A shadow-observer slot,
alert-only; (3) the **dial question** — if consumption lands in the lifecycle-multiplier lane
(`scaled_risk = BASE_RISK × DD_SCALE × lifecycle`) it inherits the authorization axis's
down-only doctrine; anything touching a `dd_protection`-class constant runs the full
change-control chain (pre-registration → re-MC → both-halves regime gate → admitting ADR —
[`CLAUDE.md`](../../../CLAUDE.md) §Protection). Live-operation gap noted now: no
forward-looking calendar source exists (all event pins are historical), and FOMC 2024+ pinned
dates are assistant-knowledge, owing primary re-verification before any freeze that consumes
them (`lab/archive/msl_s2a_mcl_2026-08/construct_lib.py` caveat).

---

## §7 Standing constraints inherited by every phase

- **Clocks.** This campaign is subordinate to the 2026-11-08 §4 falsifier work (queue #1/#2)
  and does not feed it; natural review slot 2026-11-08 alongside the standing slate. No
  internal hard dates.
- **Budget.** Rule 2: STRATEGIC = the 3 constituent OUTER investigations above; OUTER = 8
  iterations each, no self-extension; trips log to `docs/notes/audits/rule-2-trip-log.md`.
  $0 through Phases 1–3 by construction; any data pull runs the mandatory Databento cost
  dry-run; $700 spend ceiling stands; paid families (dealer gamma) enter only as a named
  ITERATE successor, never as mid-phase scope creep.
- **K.** Every selection among axes/constructions/seeds is K; `register_search open` before
  results are examined; the K∈{2,3} band is the reachable load-bearing correction tier
  ([K-tiering ADR](../../adr/2026-08-24-validation-battery-k-tiering-and-gate-retirement.md));
  sealed-consultation disclosure per
  [GROW0](../../adr/2026-08-22-grow0-two-ledger-k-question.md) — `burned_segments.json`
  already burns **MNQ 2025-09-01→2026-08-05**: no consultation of that (instrument, window).
- **Don't-do list** (each with its owning bar): no gold KER/TSMOM re-run
  (`rejected_candidates.md` re-proposal bar); no VIX/MOVE/rate-vol threshold re-tunes (T2b,
  RATEVOL closures); no re-scoring the 33 CFD episodes (Thread-1 exhaustion; panel
  unextendable); no GEX/T10Y3M revisit absent both orthogonality walls on genuinely new data;
  no reopening RATES-EV-ZF-1 / NG-EIA-1 as candidates (the event axis here is *state
  construction*, not those event-trade candidates); Striker legs stay barred (MYM/MNQ
  occupancy released for non-Striker research only —
  [occupancy ADR](../../adr/2026-08-12-msl-mym-occupancy-release.md)); no full-sample decode
  behind any real-time claim; no regime-gate import as a pre-negotiated rider; no
  `dd_protection` touch outside the change-control chain; **no overlay or detection code
  built before its phase's Pre-Q, PREREG, and GO exist** (the notice's own forbidden move,
  standing overlay doctrine); TV `1!` continuous series are not back-adjusted and `.v.0` is
  the pinned index-micro symbology (measurement-hygiene watch items).
- **Honest terminal states.** Phase-1 `ARTIFACT-OR-RELABEL` closes the campaign with a
  selection-discipline lesson — the cheapest good outcome. Phase-2 `FALSIFIED` extends the
  detectability record to the reformulated construction and types the paid-data re-proposal
  bar. Phase-3 `STOP` retains the barometer as an after-the-fact measurement lens (Phase-1's
  descriptive artifact keeps that value regardless). All three are designed outcomes.

---

## §8 Data surface (all $0; details owned by the cited files)

Six-plus asset classes of intraday M15 CME panels (MNQ, MYM, 6J, MGC, MCL, M2K
`core/data/bar_data/` + BAR EXPORT v0.2 incl. newly registered **M6A and HG**, commit
`7bdfa1d`); cached Databento 1m (`MNQ.v.0` 2019-05→2026-08; parent NQ/ES 2010→2019; ES+RTY
2020→2026 priced $0.0000 on record); free daily risk axes with working point-in-time fetchers
(`lab/archive/regime_cond_2026-06-30/panel.py`); retained exogenous panels
(`core/data/external/`: COR3M, DSPX, S5FI, SECTOR_SPDR, COT-gold); pinned CPI/NFP/FOMC
calendars (`lab/archive/rates_ev_zf_recon_2026-07/build_calendar.py`,
`lab/archive/msl_s2a_mcl_2026-08/construct_lib.py` — FOMC 2024+ caveat above) and the ECON
EXPORT v0.1 cross-check tooling (`docs/spec/2026-08-18-econ-export-v01.md`, awaiting a first
TV export); reusable harnesses per campaign body (`panel.py`, `run_battery.py` residualization,
`assemble_panels.py`, `lab/research_utils/{breadth,detector_kit,event_study}.py`). Vendor-byte
lineage: bytes gitignored, `SHA256SUMS` delta in the same commit as any data change
([`CLAUDE.md`](../../../CLAUDE.md) §Vendor-data integrity gate); a derived barometer panel is
a derived artifact under the same manifest discipline.

---

## §9 Proposed GRAND pursuit entry record (for operator ratification — not opened by this doc)

> **Pursuit — macro-regime-barometer campaign.** Class: standing exploration.
> **Aim served:** the pipeline's *evaluate/measure/update* limbs — a market-state conditioning
> layer protecting deployed and candidate books' survival; serves, never replaces, candidate
> supply (queue #1). **Measure:** typed phase verdicts delivered on frozen gates
> (`Q-MACROSTATE-1/-2/-3` closures). **Survive bound (concurrency-denominated):** 0 operator
> queue rows until promoted, ≤1 while active; ≤3 constituent OUTER investigations (Rule-2
> STRATEGIC budget); $0 spend through Phase 3. **Review date:** 2026-11-08 (standing slate).

Ratification writes this (verbatim or amended) to `docs/pursuits/` per the GRAND intake rule
([GRAND ADR](../../adr/2026-08-09-grand-tier-quintessentials-binding.md) §2.5 — "No side-door
pursuits"); this overview deliberately does not create the file.

---

## §10 Governance mechanics

**Artifact sequence per phase:** Pre-Q brief (`docs/briefs/Q-MACROSTATE-n-….md`, canon §3
headers, §0 Rule-0 reads with anchors, §4 falsifiable H, §5 forbidden moves, §6 binary gates
with typed Disposition column) → verdict pre-registration (`docs/briefs/pre-registration/`,
frozen before analysis) → campaign body `lab/analysis/regime/<slug>/` with `PREREG.md` (§0
citing the governing corrected-null spec valence-blind) → `register_search open` → RESULTS →
typed closure (`## Iterate` block; `Registry:` line; board write). `gate-reachability-audit`
at every PREREG freeze; `pre-ratification-adversarial-panel` before operator ratification of
each closure.

**Notice graduation:** at the Phase-1 GO, the Pre-Q author flips
`N-2026-08-28-regime-conditionality-cross-cutting-forward-item.md` `**Status:**` from `HOLD`
to `GRADUATED to Q-MACROSTATE-1` and cites the notice in the Pre-Q's §2 lineage
([notice-log convention](../../adr/2026-08-15-notice-log-is-the-live-observation-routing-convention.md)).
Until then the notice stays `HOLD` and this plan is its forward pointer.

**Operator gates, in order:** ratify pursuit record + this plan → Phase-1 GO (graduates the
notice) → each subsequent phase GO on the prior phase's typed closure → any `register_search
open` on real data → any spend → Rule-2 tripwire extensions (owner-adjudicated only) → closure
ratifications → Phase-4's doctrine ADR + M-A scope ruling + dial ruling. Queue posture: this
campaign queues behind the live rows; promotion (if ever) drops another row (cap ≤5).

---

## §11 Provenance

Authored in the operator-directed dedicated session of 2026-08-29 (Claude Code), from four
repo-wide research passes (prior-regime autopsy; edge inventory; data/measurement
infrastructure; governance path) — every load-bearing claim above cites a repo artifact; zero
authority attaches to any external source. Amendment-first / dedup evidence (sub-rule 8),
literal outputs 2026-08-29 at `94a2de9`:

```text
$ grep -ril "barometer" --include='*.md' --include='*.py' . | grep -v '.git/'
(no output — no prior barometer artifact exists)

$ grep -in 'regime' docs/briefs/INDEX.md | head -6
182:  cushion-proportional-sizing regime break — **`FALSIFIED` 2026-08-20** — trailing mean-R
187:  (`ops/instruments/MNQ.md` N17). Bust-elimination itself is unaffected (regime-agnostic,
190:  [`RESULTS`](../../lab/archive/q_orbcush_1_2026-08/RESULTS_meanr_regime_gate.md) ·
191:  [`brief`](Q-ORBCUSH-1-regime-break-mechanism.md) ·
271:  … sole regime-admissible rung (0.50×)
347:- **Q-REGIME-RATEVOL-1** — … closed **FALSIFIED 2026-06-16** …
```

No existing owner holds a regime-*campaign* plan: the notice is a HOLD observation, the
viable-strategy plans own a different campaign, and every `Q-REGIME-*` / regime-lane artifact
is a closed investigation. New file justified under amendment-first.

---

## Verification

```bash
# The notice this plan answers, still HOLD until Phase-1 GO
grep -n "Status:" docs/notes/notice/N-2026-08-28-regime-conditionality-cross-cutting-forward-item.md
# expect: HOLD (flips to GRADUATED only at the Phase-1 GO)

# The SNAG closure this plan must not silently re-enter
grep -n "regime-detection" docs/rejected_candidates.md | head -2
# expect: "9 consecutive nulls, operator SNAG-closed 2026-06-28"

# The detectability anchor
grep -n "Q-REGIME-AEGIS-1" ops/instruments/6J.md | head -2
# expect: J6, AUC ~0.499, FALSIFIED

# The composite-already-tried correction (against notice §4-C)
grep -rn "trailing" lab/archive/regime_cond_2026-06-30/FINDINGS.md | head -3

# Rule-2 budgets this plan consumes
grep -n "STRATEGIC.*3 constituent" docs/methodology/inqhiori-canon.md

# Overlay doctrine
grep -n "No overlays without full INQHIORI" docs/methodology/inqhiori-canon.md
```
