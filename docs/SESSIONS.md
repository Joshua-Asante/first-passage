# Session Log

Chronological progress log, **newest first**. One entry per working session. Each entry
**links out** to the detailed artifacts (ADRs, notices, briefs, commits) rather than
duplicating them. Complements `MEMORY.md` (durable atomic facts, recalled by relevance);
this file is the narrative timeline you can scan top-to-bottom.

**Entry classes (W5 direction):** Decision / Build / Measurement / Hygiene — prefer
links; keep prose beyond the five fields ≤ **~40 words** where possible
([`W5 ADR`](adr/2026-08-07-w5-governance-diet.md)). Skip Hygiene-only turns.

Next session opens by reading the top entry's **Open / next**.

Same-day letter: `python scripts/roll_sessions.py --next-label YYYY-MM-DD` before writing (a-first; bare claims `a`).

---
## 2026-08-18f — Operator "OK on both": MNQSR-1 and Q-CAPA-1 bank

**Focus:** Discharge the two OPEN items from 18e after operator *"OK on both"*.

**Shipped:** Read as both count. Notice-phase closed manifests bank; Cap-seat K folds into the family tally. Live figure at [`MNQ.md` §K_BANKED](../ops/instruments/MNQ.md). Addendum on [`ADR 2026-08-04`](adr/2026-08-04-family-k-bank-disclosure-not-gate.md); ledger / N16 / DEAD rows updated. Disclosure-only.

**Decisions/defects:** [ADR 2026-08-04 Addendum 2026-08-18](adr/2026-08-04-family-k-bank-disclosure-not-gate.md) — lane label does not exempt; Cap seat and family bank are not mutually exclusive. TNEC/R2/DSTRUCT `K=1 (disclosure; Cap not claimed)` rows stay out.

**Open / next:** Carry 18d: S1b conditioner-engineering prereg electable (new GO, new K); S2 cheap falsifier; S3 matched-day prereg. 18e OPEN rulings discharged.

**Live-ops state:** c1 warm/disarmed at incumbent; eval live; no book; no arming.

---
## 2026-08-18e — MNQ K_banked ledger recon: Q-TXG-1 backfilled (5→6); MNQSR-1 / Q-CAPA-1 flagged OPEN

**Focus:** Reconcile stale `K_banked(MNQ)` on [`ops/instruments/MNQ.md`](../ops/instruments/MNQ.md) after a pre-reg disclosure pass found the last `bank X→Y` was 2026-08-05a.

**Shipped:** [`MNQ.md`](../ops/instruments/MNQ.md) §K_BANKED + DEAD/session-log backfill. Unambiguous +1: `Q-TXG-1` striker×MNQ `DEAD(N-SURV)` (closure §10 banked K=1) → **5→6**. `MNQSR-1` Notice-phase K=14 and `Q-CAPA-1` Cap-seat K=1 flagged **OPEN** (no silent pick). Harvest Req 3 snapshot now points at the ledger. Disclosure-only.

**Decisions/defects:** none — no ADR. Two operator rulings owed (Notice-phase banking; Cap-seat vs family tally). Owner: MNQ §K_BANKED.

**Open / next:** Operator rule whether `MNQSR-1` K=14 (once, not 28) banks, and whether `Q-CAPA-1` Cap-seat is inside the family 6 or a separate reserved seat. Carry 18d: S1b conditioner-engineering prereg electable (new GO, new K); S2 cheap falsifier; S3 matched-day prereg.

**Live-ops state:** c1 warm/disarmed at incumbent; eval live; no book; no arming.

---
## 2026-08-18d — Corrected null designed, verified, and run OFFICIALLY: S1a NULL (near-miss dissolved), S1b SIGNAL-GENERIC; H-SLATE RESOLVED

**Focus:** Operator commission ("take that on now, and identify how this affects S1a's result",
ultracode) — build the structural repair the 18c audit owed, then re-score both screens.

**Shipped:** (1) 4-lens **design panel** (`wf_ebc728eb-2ef`) → frozen class-battery spec
([`corrected-null battery`](spec/2026-08-18-magnitude-persistence-corrected-null-battery.md)):
IAAFT normal-scores surrogates (raw-TR domain FORBIDDEN — verdict-flipping, measured; AR(1)
EXCLUDED as strawman), **presence-gates / attribution-TYPES** wiring (SIGNAL-GENERIC vs
SIGNAL-EXCESS — canon-grounded claims are not retargeted at novelty), NEW L4 by-year regime
limb, pre-registered interpretation table, spec committed before any official seed (`12877c4`).
(2) Pilot surfaced a **spec-internal conflict**: the frozen "S1b L4 known-fail 6/9" prediction
never applied the L4 rule's own n_cond<20 exclusion (CL 2010 n=14 → L4 PASS 6/8). 4-lens
**pre-official verification** (`wf_e06ebc90-c3e`; independent reimplementation **bit-exact,
44/44 quantities**) ruled FIX-THEN-RUN + rules-govern; FIX-1/2/3 (flag/diagnostic layer only,
scoring asserted bit-identical), 16-item **ADDENDUM-1** appended, scoped operator election
**PROCEED** taken. (3) **Official run** (M=1000, frozen seeds, drawn once): **S1a (GC) NULL**
(driving L2+L4; obs at **8.4th pct** of its own linear-ACF band — the "near-miss" was below
the zero-mechanism benchmark; CASE A, framing retracted). **S1b (CL) SIGNAL-GENERIC** (69th
pct — generic volatility clustering; A6 rails: no mechanism wording, no mechanism-owed
discharge, no conditioner license). **Slate §4 → RESOLVED.** Propagation: RESULTS addenda ×2,
[`RESULTS_CORRECTED`](../lab/analysis/_inbox/rangestate_corrected_2026-08/RESULTS_CORRECTED.md),
MECHANISMS/MGC(cell→DEAD)/MCL(C5) + session logs, audit note **Closed (immediate+structural)**,
`strategy-validation` §5 autocorrelation clause + `futures-anomaly-discovery` battery-reuse red
flag (authoring path), memories.

**Decisions/defects:** The design panel caught its own seed-collision (R10) and the
verification caught a mis-calibrated diagnostic domain (z-domain gate ran ~2.7× looser than
the Spearman quantity the tolerance was calibrated on — FIX-2). The L4 prediction-miss was
handled append-only with both counterfactual readings disclosed (realized false-pass 0.1178 vs
frozen-representative 0.090); no parameter moved after any result was seen.

**Open / next:** S1b's conditioner-engineering prereg is electable (new GO, new K; must
confront calm-regime OPEN + O2 arithmetic + O3 lift gate + L4 boundary). S2 needs its stage-1
$0 cheap falsifier (overnight-state vs matched day-session-history conditioning) before any
null design; S3 needs its matched-day prereg. Slate 2026-09-15 date now moot (RESOLVED).

**Live-ops state:** c1 warm/disarmed at incumbent; eval live; no book; no arming.

---

## 2026-08-18c — S1b runs SIGNAL, adversarial review finds it NOT-CONFIRMED: placebo test invalidated

**Focus:** Operator GO ("GO S1b") off the Step-0 slate queue — daily True-Range top-quintile
persistence on crude oil (CL), replicating S1a's frozen object on a second instrument.

**Shipped:** First raw battery reading was the program's first **SIGNAL** (gateHit 0.6282,
n=425, all four frozen limbs clear, placebo p=0.0005). Given SIGNAL is the highest-stakes
outcome type, launched a heavier adversarial-verify workflow than S1a's (independent
reimplementation from the frozen prereg text alone + regime-concentration drop-year test +
placebo-design skepticism). **Result: the placebo null is structurally misspecified** — it does
not control for CL's own ordinary True-Range autocorrelation (measured log-TR lag-1 ρ=0.4520).
20 independent zero-mechanism AR(1) surrogates calibrated only to that one coefficient cleared
the identical battery at a *higher* rate (0.72–0.80) than the real data. Independently
corroborated: removing the 2011/2014/2016 crisis-year cluster flips the verdict to NULL; the
calm-year subset alone is a clean NULL failing its own placebo. **Verdict downgraded to
`NOT-CONFIRMED`.** Since S1a shares the identical placebo function byte-for-byte, its own
placebo pass (p=0.0095) is retroactively suspect too — corrected in the same pass (S1a's
bottom-line NULL is unchanged, since it already failed the CI limb independently, but the
"live prior for S1b" framing is retracted). Full root-cause + repair plan:
[audit note](../docs/notes/audits/2026-08-18-block-shuffle-placebo-does-not-control-for-tr-autocorrelation.md).
[`RESULTS_S1B.md`](../lab/analysis/_inbox/rangestate_mcl_2026-08/RESULTS_S1B.md) ·
[`RESULTS_S1A.md`](../lab/analysis/_inbox/rangestate_gc_2026-08/RESULTS_S1A.md) (corrected).

**Decisions/defects:** The defect is program-level, not S1b-specific — the four-limb battery
(designed for `H-DSTRUCT-MNQ-1`'s directional-match claim, reused verbatim for a
magnitude-persistence claim) was never re-validated for the new claim family's confound
(autocorrelation, not base-rate skew). Caught by the adversarial-verify discipline itself,
specifically because the stakes of a SIGNAL result warranted heavier scrutiny than a routine
NULL — the review that would have been skipped as "redundant on unchanged code" is exactly what
found this. Board writes: `MECHANISMS.md` `daily-range-state-persistence` heading corrected
(both class findings re-typed `test invalid`); `MGC.md` G4 + `MCL.md` C4 corrected/added; Step-0
slate S1a/S1b sections corrected, **S2/S3 paused**, §4 falsifier clock paused (not stopped, not
extended past 2026-09-15).

**Open / next:** Structural repair owed before any further magnitude-persistence-class Tier-1
screen: design a corrected, autocorrelation-matched null (AR/GARCH-calibrated surrogate or
phase-randomized surrogate) — a fresh methodology decision, not attempted this session.
`strategy-validation` §5 owes an explicit autocorrelation-confound clause alongside its existing
directional-drift clause. S2/S3 stay paused until then.

**Live-ops state:** c1 warm/disarmed at incumbent; eval live; no book; no arming.

---

## 2026-08-18a — W×ORB gate stopped at dedup; H-DSTRUCT-MNQ-1 NULL; Step-0 daily-geometry slate drafted

**Focus:** Mechanism-by-mechanism program kickoff (operator thread): can the validated W layer
gate ORB-MNQ? Does a daily-native version of the structure stand alone? Then build the Step-0
mechanism slate.

**Shipped:** (1) W×ORB stratification **STOPPED at freeze-stage dedup, $0, nothing run** —
Q-WLEGB-1 already falsified sub-weekly transfer, and its own prereg §1 had rejected the
ORB-entry form under the F2 guard ("a fifth ORB conditioning gate wearing a different label").
(2) `H-DSTRUCT-MNQ-1` (daily close-vs-EMA20 → next-day RTH O→C; frozen prereg; $0; K=1
disclosed) → **NULL, 3 of 4 limbs failed**; bearish arm carries zero information (up-rate
54.03% vs 54.39% unconditional). Monotonic profile complete: weekly real → transfer null →
daily-native null. MNQ ledger DEAD row added.
[`PREREG`](../lab/analysis/_inbox/dstruct_mnq_2026-08/PREREG_DSTRUCT.md) ·
[`RESULTS`](../lab/analysis/_inbox/dstruct_mnq_2026-08/RESULTS_DSTRUCT.md).
(3) Step-0 slate drafted: [`brief`](briefs/2026-08-18-step0-daily-geometry-mechanism-slate.md)
— daily-geometry class (range/level, not direction) on the non-index triad, per-row WHO +
dedup + cost arithmetic + frozen Tier-1 screen specs. Operator marks owed on the slate.

**Decisions/defects:** None new. The two negative results cost $0 and one hour combined — the
Tier-1 screen tier working as designed.

**Open / next:** Operator GO on the slate's screen queue (§6); deep-lane charter §7 steps 2–4
(`--lane deep` flag, doc scoping, skill wiring) still owed before the next lane campaign.

**Live-ops state:** c1 warm/disarmed at incumbent; eval live; no book; no arming.

---

## 2026-08-18b — S1a (GC range-state persistence) run: NULL near-miss, adversarially verified

**Focus:** Operator GO ("GO S1a") off the Step-0 slate queue — first live lane-adjacent screen
of the mechanism-by-mechanism program: daily True-Range top-quintile persistence, GC train era.

**Shipped:** Frozen prereg + first-draft runner authored, $0 pull ($0.0000 confirmed at
estimate), Step-0 panel-integrity battery run pre-freeze (caught the standing
`databento ohlcv-1d weekend bars` lesson live — 434 phantom Sunday bars, dropped per the
established remedy). Before trusting any number: 4-lens + synthesis adversarial-verify workflow
(mirroring this repo's own DL-1 precedent) — lookahead/leakage clean (independently corroborated
by an exact arithmetic identity); one MUST-FIX caught (CI block size 10d contradicted the
prereg's own 60-day clustering rationale; CI also implemented non-circular despite being
declared circular) and fixed before the trusted run, both corrections verdict-preserving and
conservative. **Result: NULL, near-miss** — 3 of 4 frozen limbs pass (n-floor, halves, placebo
p=0.0095) but the corrected CI lower bound (0.4545) falls 4.55pp short of 0.50. Board writes:
new `MECHANISMS.md` heading `daily-range-state-persistence`; `MGC.md` G4 + session log; CATALOG
row. [`PREREG`](../lab/analysis/_inbox/rangestate_gc_2026-08/PREREG_S1A.md) ·
[`RESULTS`](../lab/analysis/_inbox/rangestate_gc_2026-08/RESULTS_S1A.md).

**Decisions/defects:** Two adversarial-review-caught defects, both disclosed and fixed pre-trust
rather than silently patched (CI block size; CI circularity + a hand-typed roll-date example
list, 2 of 5 dates wrong, corrected to script-persisted output). A separate panel-completeness
gap (13 gap-days, 2 unexplained by holidays, <1% of observations) was found, disclosed as
bounded-materiality, not fixed (doesn't warrant a mid-campaign design change to a frozen object).

**Open / next:** S1b (MCL) is queued next per the slate's own order; the S1a near-miss (placebo
clears, CI doesn't) is a live prior for it, not a blind re-test. Operator GO owed on S1b/S2/S3.

---
## 2026-08-17f — Harvest Req-3 relief-valve line + parent-ADR reader-intercept

**Focus:** Internal doc-skew on `strategy_harvest.md`: the relief-valve heading still called Req-3 (family K-bank) "truly final" after the 2026-08-04 demotion to disclosure-not-gate.

**Shipped:** `cursor/harvest-req3-disclosure-intercept`. Living line rewritten to match the amended Req-3 row; one-line reader-intercept placed immediately above frozen §2 item 3 in [`2026-07-15-external-mechanism-harvest-intake.md`](adr/2026-07-15-external-mechanism-harvest-intake.md) (ratified text unedited). Source of the demotion: [`2026-08-04-family-k-bank-disclosure-not-gate.md`](adr/2026-08-04-family-k-bank-disclosure-not-gate.md). $0 / K=0.

**Decisions/defects:** None new — intercept only. Living skill [`.claude/skills/futures-anomaly-discovery/SKILL.md`](../.claude/skills/futures-anomaly-discovery/SKILL.md) still restates "a burned family kills the seed" as current intake procedure (blast-radius owed, left outside this docs-only ask).

**Open / next:** Skill restatement above is the leftover. Staging any of the 6 Koijen axis-2 leads for a real Req-1a Path 1a/1b pass is a fresh operator decision, not licensed by 2026-08-17b — none attempted here. If pursued, resolve the Della Corte/Kosowski overlap before staging either as independent. Not touched: whether this changes the broader MSL WHO-track disposition. Carry: queue #0 weekly token (deadline **2026-08-21**); S2 deep-iteration lane 1/2 abandonment budget spent; four-firms §4 2026-11-08.

**Live-ops state:** c1 warm/disarmed at incumbent; eval live; no book; no arming.

---

## 2026-08-17c — Six-lead P3 un-HOLD: dry-run $0, sleeve CLOSED (calendar-spread SCREEN-FAIL)

**Focus:** Operator: "unHOLD P3." Record the GO; run only the plan's Phase-1 packet (paper
read, USOIL-carry dedup, Databento multi-tenor `estimate`).

**Shipped:** branch `docs/p3-unhold-dry-run` —
[`P3_DRYRUN`](../lab/analysis/harvest/six_lead_cf_2026-08-17/P3_DRYRUN.md) · plan §13 mark
HOLD→GO · STATE decision-index line · CANDIDATE_ROWS addendum. Paper (Bianchi et al. *JBF*
2023 / arXiv `2308.00383`): S-strategy is long-front / short-fourth on Δslope. Dedup vs
dead USOIL carry: DISTINGUISHABLE. Venue-legal 12-parent `estimate`: `ohlcv-1d` /
`ohlcv-1m` / `definition` **$0.0000**; `tbbo` CL-parent **$1,543.90** (contrast). Sleeve
closed on the standing Tradeify calendar-spread SCREEN-FAIL, not on cost. No pull. $0 · K=0.

**Decisions/defects:** Screen-level "trades the change in slope" understated the load-bearing
fact — the profitable expression is a **spread**. L (outright Δlevel) is venue-legal and
unprofitable in the paper; an outright-on-Δslope rewrite is a different construct, not
licensed. Limb-2 untouched (never admitted).

**Open / next:** P4 (dealer-gamma) and P5 (13F fund-overweight) stay HOLD. Carry: 17e's
Q-POLFRONT-1 intraday-honest finding (5.1× does not survive; deep-lane must not lean on it);
F1 queue row 1; B7-REFIRE/M1 row 2; weekly token (deadline **2026-08-21**); four-firms §4
2026-11-08.

**Live-ops state:** c1 warm/disarmed at incumbent; eval live; no book; no arming.

---

## 2026-08-17e — Q-POLFRONT-1 intraday-honest fork executed: 5.1× policy frontier does not survive

**Focus:** Operator GO ("open the intraday-honest remeasurement") on the named-but-unopened
Q-POLFRONT-1 closure fork — learn how much of the 5.1× policy-vs-flat sizing ratio survives a
real intraday clock instead of the EOD-close proxy.

**Shipped:** Three design iterations, each triggered by the previous one's self-diagnosed
failure. v1 (instrument-price-shape ratio) and v2 (resampled real-trade ratio, derived from the
primary checkout's real Striker DJ30/NAS100 trade CSVs, reusing W1's own `_leg_daily_excursion`)
both collapsed every cell to 75–99%+ bust uniformly for both arms — diagnosed as a units-
conflation bug and a resampling-saturation bug respectively, invalidated pre-write-up. v3
(deterministic median multiplier from the same real-trade ratio source) landed a structurally
sensible result: median flat-arm delta +18.0pp (2/24 cells still clear 3.0%), median policy-arm
delta +98.1pp (1/26 cells still clear). Adversarially verified (4 reviewers + synthesis,
1 re-run after a connection failure): `SAFE_WITH_CAVEATS` — independent reimplementation
reproduced both headline numbers and derived a closed-form proof of the policy-arm collapse
mechanism (any winning day breaches once `r_base > ROPE/(|win_mult|×b)`); two confirmed
calibration biases (pyramiding contamination, multi-trade-day summing) both push toward
overstating risk, no offsetting bias found. [`RESULTS`](../lab/analysis/c1/q_polfront_1_2026-08/RESULTS_INTRADAY_HONEST.md) ·
[`OPERATIONALIZATION`](../lab/analysis/c1/q_polfront_1_2026-08/OPERATIONALIZATION_INTRADAY_HONEST.md).

**Decisions/defects:** Own defect caught and disclosed, not silently repaired: the v2→v3
iteration ran faster than the "freeze method before computing a number" discipline was
re-applied — the design doc's §5/§6 (documenting v2/v3) were written *after* the numbers existed,
caught by the adversarial pass's doctrine-scope lens, repaired with an honest post-hoc dating
rather than a backdated pretense.

**Open / next:** 5.1× headline is superseded as a usable sizing multiplier — deep-lane GO-1
should not lean on the policy frontier; flat frontier is usable only at low R relative to ROPE.
A bias-corrected re-measurement (de-pyramiding, de-duplicating multi-trade days) is named but not
attempted — the pyramiding contamination may not be cleanly separable from this trade record at
all (NAS100 base-only PF is 0.31). Six-lead pursuit thread (17d) and its carries unchanged.

**Live-ops state:** c1 warm/disarmed at incumbent; eval live; no book; no arming.

---

## 2026-08-17d — Six-lead pursuit thread closes: P1-CF/P2-CF FAIL, limb-2 ruled, channel addendum landed

**Focus:** Continue the six-lead pursuit plan from 17b's OpenAlex fork resolution — operator GO on
P1/P2 cheap falsifiers, rule the limb-2 counter question, land the drafted channel-scope addendum
("GO, land it as-is").

**Shipped:** P1-CF/P2-CF (fade-overnight-move + venue-expressible next-day-reversal, MGC+6J)
executed on primary-checkout panels → **FAIL all four legs** (three gross-negative outright,
fourth insignificant/below cost hurdle). Harvest §4 limb-2 counter **ruled — does not increment**
(never admitted through intake; not the named kill class), count stays 0/2. OpenAlex-substitute
sourcing-channel addendum landed on the harvest intake ADR (light tier, $0/K=0).
[`CF LOG`](../lab/analysis/harvest/six_lead_cf_2026-08-17/LOG.md) ·
[`harvest intake ADR`](adr/2026-07-15-external-mechanism-harvest-intake.md) ·
[`plan`](briefs/2026-08-17-six-lead-pursuit-plan.md) §13.

**Decisions/defects:** None new beyond the three landings above — all three were already
recommended/drafted by the plan's own §13 marks packet; this session executed and ratified them,
closing the thread's last open item (STATE queue row 3, now deleted).

**Open / next:** Six-lead pursuit thread fully landed. P3–P5 (curve-slope momentum, dealer-gamma,
mutual-fund overweight) stay **HOLD** per the operator's 2026-08-17 marks — no fresh work
licensed. Carry: F1 (Tradeify discharge reading, 2026-11-08) now queue row 1; B7-REFIRE/M1 row 2;
weekly token trade (deadline **2026-08-21**) still unrecorded this week.

**Live-ops state:** c1 warm/disarmed at incumbent; eval live; no book; no arming.

---

## 2026-08-17b — Koijen axis-2 (Carry) fork resolved: OpenAlex substitute → 6 screen-level leads

**Focus:** Operator: "Take the Koijen axis-2 fork to me for a decision" (surfaced from the S3
progress audit earlier this session), then "admit OpenAlex substitute" once presented the fork as
recorded 2026-08-16 (`BLOCKED-AT-SOURCE`, S2 has no record of the seed paper).

**Shipped:** Full OpenAlex citation pull (296 citing works of Koijen et al. 2018 *Carry*) →
disclosed keyword/topic pre-filter (234 shortlisted) → 25-agent Workflow (7 parallel screen
batches → adversarial verify on 17 flags → synthesis) → **7 records / 6 distinct papers survived**,
concentrated in overnight-closure-reversal and dealer/fund hedging-flow mechanisms — a materially
different result from sibling axis-1 (TSMOM), which ran to full depth on S2 and found 0. Recorded:
[`SOURCES_LOG`](../lab/analysis/harvest/koijen_axis2_openalex_2026-08-17/SOURCES_LOG.md) ·
[`CANDIDATE_ROWS addendum`](../lab/analysis/harvest/radar_tier_a_burst_2026-07/CANDIDATE_ROWS.md).
$0 · K=0 — screen only, no pull, no register_search, no Cap claim.

**Decisions/defects:** None of the 6 leads is an admitted Req-1a candidate — every one carries a
named, unresolved, load-bearing question (most commonly: is the WHO's driving variable
reconstructible in real time, and does the edge survive this venue's cost/spread reality, the
dominant null mode for prior real-mechanism candidates here). Two of the 7 flagged records are
duplicate OpenAlex entries for one paper (Da/Tang/Tao/Yang, *Mgmt Sci* 2023); two others (Della
Corte & Kosowski, overlapping authors across two overnight-reversal titles) may be one research
program presented as two leads — flagged explicitly rather than silently double-counted, not yet
resolved. 10 of the original 17 screen-stage flags reverted to REJECT under adversarial re-check
(disguised carry/momentum variants once abstracts were read; a COT-lag data-access wall; one
hedging-compliance-framing kill; a wrong-instrument-class correction).

**Open / next:** Staging any of the 6 leads for a real Req-1a Path 1a/1b pass is a fresh operator
decision, not licensed by this record — none attempted here. If pursued, resolving the Della
Corte/Kosowski overlap (read both papers directly) should come before staging either as
independent. Not touched: whether this changes the broader MSL WHO-track disposition (still framed
as dry pending any of these actually clearing Req-1a). Carry: queue #0 weekly token (deadline
**2026-08-21**); S2 deep-iteration lane 1/2 abandonment budget spent; four-firms §4 2026-11-08.

**Live-ops state:** c1 warm/disarmed at incumbent; eval live; no book; no arming.

---

## 2026-08-17a — MSL-S2B successor's CON-5 D2 falsifier executed: `D2_FAIL`

**Focus:** Operator: "run the S3 falsifier gate once MYM_M15.csv is available." Panel had become
locally available (primary checkout, not this worktree — copied + hash-verified); execute the D2
gate frozen in the 2026-08-16 CON-5 ADR.

**Shipped:** `sweep-failure-filtered-continuation` × MYM 15m, IS panel only (CONFIRM untouched) —
[runner](../lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_s2b_con5_d2_2026-08-17.py) ·
[LOG](../lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_s2b_con5_d2_2026-08-17_LOG.md) ·
forward-pointer addendum on [STAGE1.md](../lab/analysis/c1/msl_s2b_mym_2026-08/STAGE1.md). Result:
mean signed gross **−1.00 pt** / 850 signals (52.96% coverage of 1,605 IS sessions), WR 25.41% ≈ the
box's own rr=3 breakeven, **−0.044×** vs the +11.28 pt (0.5×4×RT) pass bar → **`D2_FAIL`**, clean and
non-marginal. Per the ADR's D2 clause this closes route B (temporal-selectivity-as-continuation) for
this construct-shape at $0, no Board debate needed. MSL-S2B's frozen 2026-08-14 `STAGE-1 FAIL`
verdict is unchanged (D3 prospective-only, no retro-edit). $0 · K=0.

**Decisions/defects:** No document had ever operationalized S2B's "continuation entry" trigger
beyond a qualitative story — surfaced and put to the operator rather than invented; elected: reuse
sibling MSL-C1's own PDH/PDL sweep + failed-extension-reclaim signal, flip/continuation side, on
S2B's own placeholder 40/120 stop-target box (not re-tuned). Real bug caught before scoring: naively
reusing C1's `path_pts_stop_target_flat` verbatim silently paid every target hit as C1's symmetric
+40 instead of S2B's asymmetric +120 (first run: mean −19.07 pt); a kind-by-kind sanity check caught
it, fixed with a locally-corrected path function, re-scored. **Also caught here, own mistake:** a
`git checkout -- docs/SESSIONS.md` intended to revert an append-only-violating rename of the
pre-existing duplicate `2026-08-16h` heading (see below) instead discarded this entire entry;
re-applied from conversation record, duplicate/separator defect below is untouched as found.

**Open / next:** STATE + SESSIONS lines landed per operator request; commit still pending — the
pre-existing `2026-08-16h` duplicate-label / missing-separator defect (both headings below,
predates this session — confirmed present on pristine HEAD, unrelated to this work) makes
`roll_sessions.py --check-order` and `--check-append-only` mutually unsatisfiable for anyone who
touches this file: renaming the duplicate to fix order fails append-only; leaving it fails order.
Flagged to the operator rather than silently resolved with `--no-verify`. Not touched: the CON-5
ADR's own §4 falsifiable-hypothesis tracking (this is its first data point — a FAIL, not the
PASS-then-dies case §4 names) and any Board-level write beyond this record. Carry: S3's other open
items unchanged (CON-5 falsifier itself is now discharged; Koijen axis-2 operator fork; MSL WHO
track still dry); queue #0 weekly token (deadline **2026-08-21**); S2 deep-iteration lane 1/2
abandonment budget spent; four-firms §4 2026-11-08.

**Live-ops state:** c1 warm/disarmed at incumbent; eval live; no book; no arming.

---

## 2026-08-16h — S3 WHO-drought relief: CON-5 scope ADR + M6A Tier-A sourcing (both candidates dead pre-manifest)

**Focus:** Operator: "relieve the WHO drought through doors already open" (2026-08-16 diagnostic S3). Recon workflow (4 threads + adversarial verify) → CON-5 scope election → M6A Path-1b sourcing → wrap.

**Shipped:** branch `claude/who-drought-s3-onmain` (authored on archive-lineage worktree `claude/who-drought-open-doors-cf6e31` @ `d46b2af`, replayed onto origin/main) — [CON-5 scope ADR](adr/2026-08-16-con5-timeframe-scope-cheap-falsifier-gate.md) `Accepted` (operator elected falsifier-gate, third of three options; D2 route-reliance-scoped; D2a harmonizes with DL-1's GO-adjudicated pause attestation, supersedes nothing) · forward addenda on [S2B closure](briefs/closures/MSL-S2B-closure-stage1-fail-route.md) + `STAGE1.md` (frozen verdict untouched) · [CANDIDATE_ROWS addendum](../lab/analysis/harvest/radar_tier_a_burst_2026-07/CANDIDATE_ROWS.md): `H-TSMOM-6A` CLOSED Clause-N FAIL (power 0.13–0.27; break-even SR 0.73 above the published currency sleeve — FAIL robust to the secondary-summary sourcing grade; 3/3 monthly-TSMOM siblings now dead on power) · `H-COTREV-6A` UNSCREENABLE Req 2 (no citable AUD reversal δ; Wang sign-direction caution carried, single-pass unverified). $0 · K=0 throughout.

**Decisions/defects:** Recon caught real defects pre-ship: C3-K2 "does not bind" language demoted to obiter (cleared its bar via SLR route, never needed temporal selectivity); a fabricated §-citation; my own drafted 1b(iv) class-FAIL claim contradicting H-TSMOM-1's scored 1b PASS (repaired to flagged-open-question before commit). ADR amended at replay: authoring worktree predated U0 KEEP + DL-1 attestation — read-set gap named in §0, D2 sharpened (as first drafted it would have demanded a falsifier from DL-1-class cards, contradicting DL-1's own GO). Koijen/Carry rank-1 citation traversal dispatched (result pending at entry time). Blind-channel next-candidate work **deliberately deferred** — worst EV on the board (non-index cost wall ≈27bp+/event for a mechanism-free construct; channel's own recorded expectation is AMBIGUOUS-HOLD at 11-08); forcing a second candidate risks a strike without advancing anything.

**Open / next:** (1) **MSL-S2B successor's D2 falsifier** — spec frozen in the ADR, needs `MYM_M15.csv` (absent in worktree; primary checkout or W4-gated pull). (2) DL-1 train engine + scoring (unchanged from 16g — untouched here). (3) Koijen axis-2 traversal DISCHARGED same session — `BLOCKED-AT-SOURCE` (S2 has no record for the *Carry* DOI; 404 + OpenAlex 299 both independently re-verified), recorded in CANDIDATE_ROWS with the operator fork (OpenAlex substitute = different instrument, or leave blocked) left open. Carry: queue #0 weekly token (deadline **2026-08-21**); blind channel paused 1/3; dense-1m U0 KEEP; MSL E1 HOLD; four-firms §4 2026-11-08.

---

## 2026-08-16h — DL-1 train scoring executed; campaign ABANDONED

**Focus:** Operator: "run the train scoring now." §6 step 2: score the 10 frozen variants on
TRAIN under the frozen conventions, apply the nomination gates.

**Shipped:** branch `claude/dl1-train-scoring-abandonment` (off `origin/main` — see
Decisions/defects) — [train-scoring engine](../lab/analysis/deep_lane/dl1_mgc_orc_2026-08-16/)
(stitch + fill engine + 10-variant scorer, wired to the repo's vetted SPA primitive
`research_utils.universe_gate.run_spa`), adversarially verified (5-agent workflow against the
frozen prereg text) before touching real data. All 10 variants net-negative on GC.FUT TRAIN
(2010–2019, 2,168 CME sessions); nominee V7 (argmax, no fallback) failed gates 2a/2b/2d.
[charter](adr/2026-08-16-deep-iteration-lane-charter.md) count line + change history updated
(abandoned 1, consecutive 1/2, active campaign none) · STATE decision-index line.

**Decisions/defects:** ABANDONMENT, not STRIKE — confirm partition (MGC.FUT) never read (prereg
§5, gate 3 never reached). Two real implementation bugs caught by testing + the adversarial pass
before the real run corrupted anything: an entry-scan/OR-window boundary off-by-one (dropped one
bar/day/variant), and a daily-P&L calendar that zero-filled over spurious Globex Sunday-reopen
dates (~16% inflation vs the √252 annualization). Both fixed, re-validated on real data, then the
full 9-year run executed. Separately, discovered this worktree's original branch
(`claude/dl1-train-engine-scoring-b9060d`) — and ~90 other local branches, including local
`main` — sit on a commit graph with **zero shared history** with the live `origin/main` (root
`880f025` vs `027a729`, no common ancestor); only 5 local branches (incl.
`claude/dry-funnel-election-packets`) were actually on the live lineage. Recorded here as
found; broader remediation flagged as a separate task, not attempted in this session.

**Open / next:** No active deep-lane campaign. Charter §7 steps 2–4 (lane code flag, doc
scoping, skill wiring) still owed. A second consecutive abandonment would trigger the §4(c)
audit-report duty. Local-main/origin-main disconnect (above) needs a repo-hygiene pass. Carry:
S3/S4 diagnostic-slate items untouched; queue #0 weekly token; blind channel paused 1/3;
dense-1m U0 KEEP; MSL E1 HOLD; four-firms §4 2026-11-08.

**Live-ops state:** c1 warm/disarmed at incumbent; eval live; no book; no arming.

---

## 2026-08-16g — DL-1 GO marked; prereg FROZEN; pulls fired; session wrap

**Focus:** Operator: "GO on DL-1, then we'll wrap the session." Record the mark; fire §6 step 1; stop deliberately before train scoring.

**Shipped:** branch `claude/dry-funnel-election-packets` — [DL-1 prereg](briefs/pre-registration/2026-08-16-deep-lane-dl1-mgc-orc-prereg.md) `OPEN — DRAFT` → **`FROZEN`** with the five gathered adjudications recorded on the Status block (bar-scope · pause reach · channel-origin · gold-ORB clearance · step-4 mapping) · [charter](adr/2026-08-16-deep-iteration-lane-charter.md) count line gains **active campaign: DL-1** + change-history row · STATE decision-index line · **both §6 step-1 pulls fired** ($0, cache-tagged `DL1-MGC-ORC`: MGC confirm 5,591,789 rows landed; GC train streaming at wrap).

**Decisions/defects:** train scoring deliberately NOT started — the backtest engine deserves a fresh session with its own fidelity gates (Q-EVALSEQ precedent: anchor-verify before any read), not an end-of-session build. Confirm partition remains virgin (cache era-tagged; nominee-only read per the frozen §6).

**Open / next:** (1) **DL-1 train engine + scoring** (§6 step 2: 10 variants, frozen conventions, strict-argmax, pinned SPA) — next session's first item; confirm read only after nomination gates. (2) Charter §7 steps 2–4 (lane code flag, doc scoping, skill wiring). (3) S3/S4 diagnostic-slate items untouched (WHO-drought relief; D3 fork, AMBIGUOUS-HOLD counting, weekly-token recurrence ruling, PARK triage, two-barrier Session 1). Carry: queue #0 weekly token (deadline **2026-08-21**); blind channel paused 1/3; dense-1m U0 KEEP; MSL E1 HOLD; four-firms §4 2026-11-08.

**Live-ops state:** c1 warm/disarmed at incumbent; eval live; no book; no arming.

---

## 2026-08-16f — DL-1 campaign prereg drafted (deep-lane §7 step 1); GO mark owed

**Focus:** Operator: "Draft the first lane campaign prereg." Family election + freeze candidate, adversarially reviewed before it reaches the mark.

**Shipped:** branch `claude/dry-funnel-election-packets` — [DL-1 prereg](briefs/pre-registration/2026-08-16-deep-lane-dl1-mgc-orc-prereg.md) (`OPEN — DRAFT`): NY-session opening-range continuation on gold, GC-parent train 2010–2019 / native-MGC confirm 2019–2026 (7.62y), K=10 frozen variants, strict-argmax nomination (no walk-down), pinned SPA (p≤0.10, stationary bootstrap B=10k seed 7), frozen scoring conventions (daily-P&L √252 Sharpe, 1 contract, $4.12 RT pin, adverse-first fills), conjuncts 1.170 floor / 0.959 power. 2-agent adversarial review applied pre-freeze: **10 blockers + 9 minors** — incl. a drifted route-1 quote whose elision was load-bearing, an unfrozen nomination fallback, and a **dedup miss the grep could not see** (CFD-era gold-ORB survey: "Closed for ORB: gold (long-beta + sub-cost)", placebo wrong-direction — now engaged as adverse prior §7.6). $0 · K=0 · nothing runs pre-mark.

**Decisions/defects:** none ratified. Five operator items gathered for the GO mark (Verification block): bar-scope reading (5th-leg BINDING BAR — route 1 demoted to disclosure per the F1 precedent); pause residual broad reading; channel-origin/harvest-intake judgment; "Closed for ORB: gold" re-proposal question + survey-panel overlap disclosure; step-4 strike-mapping ratification.

**Open / next:** operator GO mark on DL-1 (freezes the prereg; path lands on the charter count line; staged pulls fire). Charter §7 steps 2–4 (lane code flag, doc scoping, skill wiring) still owed. Carry: S3/S4 diagnostic-slate items untouched; queue #0 weekly token (deadline 08-21); blind channel paused 1/3; dense-1m U0 KEEP; MSL E1 HOLD.

**Live-ops state:** c1 warm/disarmed at incumbent; eval live; no book; no arming.

---

## 2026-08-16e — Databento parent-era dry-run → deep-lane GO-1 fully discharged

**Focus:** Operator: "Go on the Databento dry-run." Price bar-schema reachability for the design-box non-index triad before the first lane campaign prereg.

**Shipped:** branch `claude/dry-funnel-election-packets` — [charter addendum](adr/2026-08-16-deep-iteration-lane-charter.md) (8 free `estimate` calls: `definition` + `ohlcv-1d/1h/1m` on `GC/CL/6A` train 2010–2019 and `MGC/MCL/M6A` confirm 2019–2026, all $0.0000; `tbbo` priced for contrast at $2,209.69 train / $274.89 confirm). $0 billed (estimate-only, per skill Rule 1 — never bills).

**Decisions/defects:** roots confirmed live (`GC.FUT` not `GC` — parent symbology requires the `.FUT` suffix, corrected after one clean `400` from the API). Confirm window measured at 7.6 years — longer than the 6.5y GO-2 power design point, not shorter. Ruling: bar-level discovery is cost-gate-free for this triad; escalating past bars stays gated exactly as the skill's own Rule 2 already requires (candidate-survival-first, explicit `--max-cost`, never inferred from this dry-run). GO-1 fully discharged.

**Open / next:** first lane campaign prereg (§7 step 1, K≈10) is now the only remaining gate — must name the Q-POLFRONT-1 EOD-clock caveat as a mandatory risk if it leans on the policy frontier. Charter §7 steps 2–4 (code flag, doc scoping, skill wiring) still owed. Carry: S3/S4 from the original diagnostic slate (WHO-drought relief; governance holes) untouched. Queue #0 weekly token (deadline 08-21); blind channel paused 1/3; dense-1m U0 KEEP; MSL E1 HOLD.

**Live-ops state:** c1 warm/disarmed at incumbent; eval live; no book; no arming.

---

## 2026-08-16d — Q-POLFRONT-1 GO → `RESOLVED-QUANTIFIED`; EOD-clock caveat routed to GO-1

**Focus:** Operator GO on the Q-POLFRONT-1 run. Fidelity-gate the recovered seed-spec harness first (Rule 0); resolve the frozen brief's grid ambiguity before any policy number.

**Shipped:** branch `claude/dry-funnel-election-packets` — [camp](../lab/analysis/c1/q_polfront_1_2026-08/RESULTS.md) (30-cell frozen grid; sweep-range amendment recorded pre-read after a smoke test hit the search boundary — true policy ceiling proven `< ROPE` by construction) · [closure](briefs/closures/Q-POLFRONT-1-closure-resolved-quantified.md) · charter GO-1 line updated (frontier landed; Databento dry-run still owed) · INDEX/CATALOG rows. $0 · K=0.

**Decisions/defects:** `RESOLVED-QUANTIFIED` — median R_max ratio (policy/flat) **5.107×** ≥ 1.25× bar (24/30 cells, min 1.526×, 2 newly-admitted, no reversal under quantization). ⚠ **Load-bearing caveat, not a footnote:** mandatory intraday-stress arm shows the policy is far more EOD-clock-fragile than flat sizing (median bust delta +55.2pt vs +1.6pt) — carried into GO-1 as a **mandatory named risk**, not silently. Fidelity: harness bit-identical to recorded anchors, no environment drift (pure-numpy, unlike the book-comp harness).

**Open / next:** (1) Databento parent-era cost dry-run (deep-lane GO-1, last blocker). (2) First lane campaign prereg at K≈10 (GO-2), naming the EOD-clock caveat explicitly. (3) Intraday-honest policy remeasurement — named fork, not opened. (4) Charter §7 steps 2–4 (lane code flag, doc scoping, skill wiring). Carry: S3/S4 from the original diagnostic slate (WHO-drought relief; governance holes — D3 fork, AMBIGUOUS-HOLD counting, weekly-token recurrence, PARK triage, two-barrier Session 1) — untouched this session. Also: queue #0 weekly token (deadline 08-21); blind channel paused 1/3; dense-1m U0 KEEP; MSL E1 HOLD.

**Live-ops state:** c1 warm/disarmed at incumbent; eval live; no book; no arming.

---

## 2026-08-16c — Q-EVALSEQ-1 frozen run → `FALSIFIED`; bust-axis finding survives

**Focus:** Execute the P2-licensed frozen run. Fidelity-gate the recovered harness before any policy read.

**Shipped:** branch `claude/dry-funnel-election-packets` — [camp](../lab/analysis/c1/q_evalseq_1_2026-08/RESULTS.md) (OPERATIONALIZATION frozen pre-read; gate v1 FIRED → diagnosed as environment vintage, original itself prints 38.2 here; gate v2 port≡original PASS; control 75.01/20.18 matches the original's own sweep row) · [closure](briefs/closures/Q-EVALSEQ-1-closure-falsified.md) · CATALOG row · INDEX rows. $0 · K=3 consumed (the prereg's banked count).

**Decisions/defects:** `FALSIFIED` per the frozen §6 — best lift −1.06pt (c_cushion) vs +5pt; flat WATCH-1 stands; schedule family spent for pass-prob. **Surviving finding:** cushion-proportional sizing bust 20.18% → 0.00% (both halves) at 1.06pt of pass — EOD-clock / integer-floor / in-panel bounds disclosed; routed to Q-POLFRONT-1 (bust-axis reframe).

**Open / next:** (1) Q-POLFRONT-1 brief (bust-axis: base-R headroom at bust ≤ 3.0% under policy c) → operator GO → run. (2) Databento parent-era cost dry-run (deep-lane GO-1). (3) Charter §7 steps 2–4. Carry: queue #0 weekly token (deadline 08-21); blind channel paused 1/3; dense-1m U0 KEEP; MSL E1 HOLD.

**Live-ops state:** c1 warm/disarmed at incumbent; eval live; no book; no arming.

---

## 2026-08-16b — P2 + GO marked; stamps landed

**Focus:** Operator marked "P2 + GO" on the two 2026-08-16a packets. Record both elections; license the frozen run.

**Shipped:** branch `claude/dry-funnel-election-packets` — [P2 closure](briefs/closures/STATE-POLICY-closure-resolved-p2.md) · packet header mark · [Q-EVALSEQ-1 un-dorm stamp](briefs/pre-registration/2026-07-24-2leg-eval-frontload-schedule-preregistration.md) (scoring-only; §0–§10 byte-unedited) · [charter `Accepted`](adr/2026-08-16-deep-iteration-lane-charter.md) with GO-1/GO-2 conditions · [b5 renewal](../docs/pursuits/b5-q-fundpol-1.md) (corrected wake; expiry 2027-02-08) · STATE decision-index ×2 · INDEX rows (Q-EVALSEQ-1 OPEN; Q-POLFRONT-1 COMMISSIONED). $0 at mark.

**Decisions/defects:** charter GO is an eyes-open override of its own HOLD default (§1 third-door engagement; recorded in Status + change history). Q-POLFRONT-1 named, not opened — brief owed.

**Open / next:** (1) Q-EVALSEQ-1 frozen run — harness recovery from `pre-prune-2026-08-08` + anchor verification BEFORE any policy read, then K=4 MC + DSR/placebo + both-halves, close under its own §6. (2) Q-POLFRONT-1 brief. (3) Databento parent-era cost dry-run (deep-lane GO-1). (4) Charter §7 steps 2–4 (lane flag + doc scoping + skill wiring). Carry: queue #0 weekly token (deadline 08-21); blind channel paused 1/3; dense-1m U0 KEEP; MSL E1 HOLD.

**Live-ops state:** c1 warm/disarmed at incumbent; eval live; no book; no arming.

---

## 2026-08-16a — Bottleneck diagnostic → two election packets drafted

**Focus:** Operator: "address head on what may be holding us back from finding viable strategies for Tradeify" (ultracode). Diagnose, then draft the elected next steps.

**Shipped:** branch `claude/dry-funnel-election-packets` — [state-policy scoring packet](briefs/2026-08-16-state-policy-scoring-review.md) (`OWED-election`: P0 keep-dormant / P1 run Q-EVALSEQ-1 as frozen / P2 + policy frontier) · [deep-iteration lane charter](adr/2026-08-16-deep-iteration-lane-charter.md) (`Proposed`, full tier; default disposition HOLD to the 2026-11-08 §4 reading). $0 · K=0 · nothing runs.

**Decisions/defects:** none ratified — both artifacts are operator elections. Session diagnostic (8 readers + 7 refuters, operator-held): dryness = mechanism supply (matches the 08-15 wall audit) + an unmodeled within-attempt state-policy lever (every N-SURV number is constant-policy; Q-EVALSEQ-1 dormant) + no priced iteration depth. Refuted en route: ORB retry-EV rescue; small-weight compose; CONFIRM reads. Both drafts adversarially reviewed pre-commit (11 blockers fixed, incl. an unbinding K-predicate).

**Open / next:** operator marks owed: state-policy packet §6 (P0/P1/P2) · lane-charter GO-or-HOLD (default HOLD) · b5 PARK renew/lapse before 2026-11-08. Carry: queue #0 weekly token (deadline 08-21); blind channel paused 1/3; dense-1m U0 KEEP; MSL E1 HOLD; B7/M1 wait on a book.

**Live-ops state:** c1 warm/disarmed at incumbent; eval live; no book; no arming.

---

## 2026-08-15v — R10 historical-kill pin marked `no`

**Focus:** Operator marked the R10 pin `no`. Already-closed D5 / H-OD-1 / H-TSMOM-1 do not increment. Write 0/2 counting machinery. Do not fire.

**Shipped:** branch `cursor/r10-pin-no-8529` — [harvest addendum](adr/2026-07-15-external-mechanism-harvest-intake.md) pin marked `no`; counting machinery (a)–(d); running count **0 / 2**; not fired. Limb 1 unedited. $0 · K=0.

**Decisions/defects:** pin discharged. Only post-mark Stage-2 cost-law or Clause-N/power kills increment. This `no` is not a fire.

**Open / next:** (1) queue #0 weekly token, deadline 2026-08-21 — operator-placed. (2) Blind channel **paused** — count 1/3; re-enter only with a construct that is distinct without shopping; else hold to 11-08 `AMBIGUOUS-HOLD`. (3) dense-1m pause stands (U0 KEEP). (4) 2026-11-08 slate: channel §4 + count/N-fire + analogue re-test · harvest idle + **limb-2 post-mark count** (pin discharged) · F1 · ceremony-tiering. (5) B7/M1 still wait on a book. `Q-CAPBAND-1` re-opens only on a *new* band axis. MSL E1 HOLD / no slate-4 until NEW WHO.

**Live-ops state:** c1 warm/disarmed at incumbent; eval live; no book; no arming.

---

## 2026-08-15t — R10 harvest §4 limb 2 Accepted

**Focus:** Operator GO on the R10 addendum after PR #15 merged. Bind limb 2. Do not invent the historical-kill pin.

**Shipped:** branch `cursor/r10-go-8529` — [harvest addendum](adr/2026-07-15-external-mechanism-harvest-intake.md) `Proposed` → `Accepted`. Pin left unmarked. Not fired. Limb 1 unedited. $0 · K=0.

**Decisions/defects:** GO ≠ pin. Yes on the pin would fire immediately (D5 + H-OD-1 + H-TSMOM-1 are dated). This session does not mark yes or no.

**Open / next:** (1) queue #0 weekly token, deadline 2026-08-21 — operator-placed. (2) Blind channel **paused** — count 1/3; re-enter only with a construct that is distinct without shopping; else hold to 11-08 `AMBIGUOUS-HOLD`. (3) dense-1m pause stands (U0 KEEP). (4) R10 pin still owed — yes → fire / no → count starts at 0; rides 2026-11-08 if unmarked. (5) 2026-11-08 slate: channel §4 + count/N-fire + analogue re-test · harvest idle + limb-2 pin · F1 · ceremony-tiering. (6) B7/M1 still wait on a book. `Q-CAPBAND-1` re-opens only on a *new* band axis. MSL E1 HOLD / no slate-4 until NEW WHO.

**Live-ops state:** c1 warm/disarmed at incumbent; eval live; no book; no arming.

---

## 2026-08-15r — 08-03 gate-stack R3–R6 / R10

**Focus:** Execute the still-owed 08-03 mechanical repairs (R3–R6) and draft R10 without self-ratifying a new falsifier.

**Shipped:** branch `cursor/gate-stack-r3-r10-8529` — sentinel cross-tree pairing; H-TSMOM-1 living-harness pin; `var_trials` default `1/n`; `cost_mnq` `firm_key` required; harvest §4 limb 2 drafted `Proposed`. Merged `origin/main` (N=3 + dense-1m U0 KEEP); retitled off 15l. $0 · K=0.

**Decisions/defects:** R10 is spec-only — operator GO still owed; limb 1 unedited. Winning V-estimator / required `firm_key` were already ratified; this pass makes them executable.

**Open / next:** (1) queue #0 weekly token, deadline 2026-08-21 — operator-placed. (2) Blind channel **paused** — count 1/3; re-enter only with a construct that is distinct without shopping; else hold to 11-08 `AMBIGUOUS-HOLD`. (3) dense-1m pause stands (U0 KEEP). (4) 2026-11-08 slate: channel §4 + count/N-fire + analogue re-test · harvest idle + limb-2 pin · F1 · ceremony-tiering. (5) R10 operator GO — do not self-ratify. (6) B7/M1 still wait on a book. `Q-CAPBAND-1` re-opens only on a *new* band axis. MSL E1 HOLD / no slate-4 until NEW WHO.

**Live-ops state:** c1 warm/disarmed at incumbent; eval live; no book; no arming.

---

## 2026-08-15o — Blind-channel next-move sequence

**Focus:** After N=3 + empty naming, sequence what is actually next (no new construct, no Cap reopen).

**Shipped:** branch `cursor/blind-channel-n3-8529` — booked the 2026-11-08 channel §4 reading on the [STATE forward board](../STATE.md); merged `origin/main` (dense-1m U0 KEEP) and retitled off colliding 15j/15k. $0 · K=0.

**Decisions/defects:** none new. Owners remain the [channel ADR](adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md) and [analogue-modality ruling](adr/2026-08-15-analogue-modality-route-ruling.md).

**Open / next:** (1) queue #0 weekly token, deadline 2026-08-21 — operator-placed. (2) Blind channel **paused** — re-enter only with a construct that is distinct without shopping; else hold to 11-08 `AMBIGUOUS-HOLD`. (3) dense-1m pause stands (U0 KEEP). (4) 2026-11-08 slate: channel §4 + count/N-fire + analogue re-test · F1 · harvest idle · ceremony-tiering. (5) 08-03 [R3–R6 / R10](notes/audits/programme-audit/2026-08-03-gate-stack-audit.md) still owed on main (drafted on `cursor/gate-stack-r3-r10-8529`; do not treat as landed). (6) B7/M1 still wait on a book. `Q-CAPBAND-1` re-opens only on a *new* band axis. MSL E1 HOLD / no slate-4 until NEW WHO.

**Live-ops state:** c1 warm/disarmed at incumbent; eval live; no book; no arming.

---

## 2026-08-15n — Blind-channel N=3 election + empty generation attempt

**Focus:** Move the open-but-empty blind channel forward without raising Cap/K or retuning `MNQ-ANALOGUE-1`.

**Shipped:** branch `cursor/blind-channel-n3-8529` — consecutive-pre-G0-kill threshold elected **N = 3** on the [channel ADR](adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md) (limb 4, amend-in-place, counting machinery (a)–(d)); one generation attempt walked every standing door and named nothing. Count stays **1/3**. $0 · K=0.

**Decisions/defects:** N=3 discharges the pre-G0 addendum's uncovered item. Empty naming is not a second kill and not generation-dry. §4 `AMBIGUOUS-HOLD` trajectory accepted if still unsourced at 2026-11-08.

**Open / next:** `Q-CAPBAND-1` re-opens only on a *new* band axis; R3–R6/R10 from the 08-03 audit still owed. The 2026-11-08 §4 falsifier is the live clock (analogue-modality ruling re-test rides it). Weekly token unpaid for 08-17→08-21. Blind-channel generation paused pending a construct that is distinct without shopping.

**Live-ops state:** c1 warm/disarmed at incumbent; eval live; no book; no arming.

---

## 2026-08-15k — Dense-1m unpause U0 KEEP

**Focus:** Operator marked U0 KEEP on the unpaid dense-1m unpause packet. Leave the pause.

**Shipped:** branch `cursor/dense1m-unpause-plan-22c1` — packet `CLOSED-RESOLVED (U0 KEEP)` · [closure](briefs/closures/DENSE1M-UNPAUSE-closure-resolved-u0-keep.md). No ADR. No CON-6. $0 · K=0.

**Decisions/defects:** U0 KEEP. Owner of the pause remains [CON-5 Branch A](briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md). This closure records the mark only.

**Open / next:** dense-1m pause stands (U0). No CON-6. Carry: consecutive-pre-G0-kill threshold uncovered; `Q-CAPBAND-1` re-opens only on a *new* band axis; R3–R6/R10 from the 08-03 audit still owed. The 2026-11-08 §4 falsifier is the live clock. Weekly token unpaid for 08-17→08-21. MSL E1 HOLD / no slate-4 until NEW WHO.

**Live-ops state:** c1 warm/disarmed at incumbent; eval live; no book; no arming.

---

## 2026-08-15j — Dense-1m unpause Board packet (OWED-election)

**Focus:** Draft a reviewable plan for unpausing the dense-1m OHLCV temporal-selectivity / entry-geometry default. Pause stays until a Board mark.

**Shipped:** branch `cursor/dense1m-unpause-plan-22c1` — [packet](briefs/2026-08-15-dense1m-lane-unpause-review.md) presents U0 KEEP / U1 ADMIT-ONE / U2 OPEN-DEFAULT; elects none; no CON-6, no camp, no ADR. $0 · K=0.

**Decisions/defects:** none marked. Owner of the pause remains [CON-5 Branch A](briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md). U1/U2 would need a full limb-4 ADR.

**Open / next:** operator marks U0 / U1 / U2 on the packet. Carry: consecutive-pre-G0-kill threshold uncovered; `Q-CAPBAND-1` re-opens only on a *new* band axis; R3–R6/R10 from the 08-03 audit still owed. The 2026-11-08 §4 falsifier is the live clock. Weekly token unpaid for 08-17→08-21. MSL E1 HOLD / no slate-4 until NEW WHO.

**Live-ops state:** c1 warm/disarmed at incumbent; eval live; no book; no arming.

---

## 2026-08-15i — STATE weekly roll + de-scope over-read correction

**Focus:** Roll the idle-clock header past the satisfied 08-10→08-14 week; correct STATE pointers that treated Tradeify as a gone firm.

**Shipped:** branch `cursor/state-weekly-header-roll-ca60` — weekly deadline **2026-08-21** / bucket 08-17→08-21 (prior week satisfied 2026-08-12). Queue row 1 no longer says "de-scoped firm"; row 2 names B7 + M1 as waiting on an acceptable strategy; gated first-fill block no longer claims the execution surface is gone. Blast-radius: refreshed one-line pointers in `PIPELINES.md` P4/P5, `README.md`, `c1-rail` / `trade-csv-reconcile` skills, `ops/prop_envelope_default.md` E6 parenthetical. $0 · K=0.

**Decisions/defects:** none new. Owner of the narrow reading remains [`08-04 addendum`](adr/2026-08-04-tradeify-venue-descope-eval-included.md) + [`S1`](adr/2026-08-07-loop-s1-environment-ratification.md). ADR title left as filed.

**Open / next:** consecutive-pre-G0-kill threshold uncovered; `Q-CAPBAND-1` re-opens only on a *new* band axis; R3–R6/R10 from the 08-03 audit still owed. The 2026-11-08 §4 falsifier is the live clock. Weekly token unpaid for 08-17→08-21.

**Live-ops state:** c1 warm/disarmed at incumbent; eval live; no book; no arming.

---

## 2026-08-15h — Wall-scope audit · Q-BUSTGATE-2 · blind sourcing channel · Q-CAPBAND-1

**Focus:** Assess where Tradeify strategy research stands and how to make it more productive. Audit the admission walls, re-derive the bust ceiling, open the operator-elected weaker-grade sourcing channel, and price the Cap counterfactual.

**Shipped:** [wall-scope audit](notes/audits/programme-audit/2026-08-15-msl-wall-scope-audit.md) · [`Q-BUSTGATE-2`](briefs/Q-BUSTGATE-2-bust-gate-re-derivation-2026-08.md) + [pre-reg](briefs/pre-registration/Q-BUSTGATE-2-verdict-preregistration.md) + [closure](briefs/closures/Q-BUSTGATE-2-closure-resolved.md) `RESOLVED` · 3 light ADRs discharging F1/F2/Board-lite · [no-counterparty sourcing channel](adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md) (full tier) + K-cap and pre-G0 addenda · [analogue-modality route ruling](adr/2026-08-15-analogue-modality-route-ruling.md) · [`Q-CAPBAND-1`](briefs/Q-CAPBAND-1-cap-band-counterfactual.md) + [pre-reg](briefs/pre-registration/Q-CAPBAND-1-verdict-preregistration.md) + [closure](briefs/closures/Q-CAPBAND-1-closure-resolved.md) `RESOLVED`. **$0 · K=0 throughout**; no `core/` or `lab/` code touched.

**Decisions/defects:** Two suspected causes of the dry funnel were **eliminated on evidence**: gates (13/14 walls survived adversarial re-verification; the one finding was an unratified *label*) and the bust ceiling (reconfirmed unchanged under two new input classes). Cost geometry measured across 5 instruments with primary-sourced commissions — the cost wall is a **frequency** wall, and `floor_at_k` is K-driven not n-driven. The channel's first candidate `MNQ-ANALOGUE-1` died at its pre-G0 cheap falsifier (analogue hit rate 0.5160 *below* the 0.5453 base rate); feasible set now empty at $0. Operator withdrew Aegis 1.83 as a reachability ceiling — M-19 requires **both** anchors and 1.83 is cohort-bound, K-undeclared, un-deflated — which relocated the bound to `CAP = 1.0`; `Q-CAPBAND-1` then priced that counterfactual and ratified Cap on the named axes (D6 venue-dead, D2-low bar-bound). Structural finding: the binding constraint is **K** — searches large enough to discover set a floor above the corrected published top decile.

**Open / next:** consecutive-pre-G0-kill threshold uncovered; `Q-CAPBAND-1` re-opens only on a *new* band axis; R3–R6/R10 from the 08-03 audit still owed. The 2026-11-08 §4 falsifier is the live clock.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

**Provenance:** authored in the private archive (10 commits, `28fdcea..3df9d91`); replayed here as content since the two repos share no history. One private-class artifact (`docs/notes/notice/…`) is excluded from the public seed and referenced by `git show` pointer.

---

## 2026-08-15g — Root-doc liveness: 16 public-seed dead links repointed

**Focus:** `make check` / `check_root_doc_liveness.py` HARD-failed on 16 markdown links in `STATE.md` + `REPO_MAP.md` whose targets were omitted from the public seed (PR #5 restored `docs/notes/audits/` only).

**Shipped:** branch `cursor/root-doc-liveness-004b` — repointed, did not restore excluded trees. Surviving owners where they exist (`S1`, FU-1 audit, implied-SR ADRs, CFD-estate ADR, `strategy_harvest.md`); `git show <sha>:<path>` retrieval idiom elsewhere (same skip the gate already honors). Blast-radius: refreshed the three instrument-ledger SESSION LOG pointers that still markdown-linked the omitted WHO-track / slate-3 notices (`ops/instruments/MCL.md`, `M6A.md`). `make check` green.

**Decisions/defects:** no new ADR. Did not reverse PR #5's `notice/` / `rail_build/` / dated-notes exclusion.

**Open / next:** `path-liveness`/`root-doc-liveness` re-tier to `always` landed in
[PR #8](https://github.com/Joshua-Asante/first-passage/pull/8) (2026-08-15f). Limb C
(local-embedder vector) live per Q-XMEM-1, not authorized — needs a Rule 2 cost dry-run,
operator-paced. Excluded-tree inbound links outside the five root docs remain
(briefs/ADRs/skills); not this gate. Registry backfill (33 rows) stays operator-paced
(`--list-debt`). Carry: F1 2026-11-08; M1; weekly token; Magdon-Ismail B.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-15f — Gate reachability, registry debt split, Rule 2 narrowed

**Focus:** Phases 3/4/5 of the governance-belt audit's remediation, done in sequence.

**Shipped:** branch `claude/gate-belt-phase345-0815`, 3 commits — (1) reverted
`path-liveness`/`root-doc-liveness` to `always` (their `staged_regex` never matched
`lab/|core/|ops/`, so a moved/deleted link target skipped pre-commit); added
`test_path_conditional_gates_are_reachable`, a reachability probe for the 9 gates
that stay `path-conditional`. (2) Split `REGISTRY_GRANDFATHERED` (66, not 68 as
earlier estimated) into `REGISTRY_GRANDFATHERED_NA` (33) / `REGISTRY_DEBT_2026_08`
(33), classified by reading each closure's actual verdict, not its filename —
caught 2 filename-vs-substance mismatches doing it properly. `--list-debt` CLI mode
+ STATE.md pointer. (3) Narrowed Rule 2's always-on pointers from 5 surfaces to 1
(`inqhiori` only) — a judgment call, flagged as such, not a ratify/repeal; dated
addendum on the ADR itself.

**Decisions/defects:** no new ADR (one addendum, on the existing Rule 2 ADR). All
three phases independent, no file overlap between them.

**Open / next:** all seven governance-belt remediation phases now shipped
(Phases 0/0b/1/2 = PR #4/#5/#6/#7; Phases 3/4/5 = this session's PR). Registry
backfill itself (33 rows into `rejected_candidates.md`) stays operator-paced,
tracked via `--list-debt`. Rule 2 re-widens once the trip-log accrues real
evidence at the next programme audit (2026-11-08). Carry: F1 2026-11-08; M1;
weekly token; Magdon-Ismail B.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-15e — Limb B v3 re-measurement: `ASSISTIVE-ONLY` (final)

**Focus:** Phase 2 of the governance-belt audit's remediation — frozen v3 pre-registration,
re-measure `repo_retrieve.py` against the same 0.70 / `R_fts5 > R_rg` table the 2026-08-15d
entry left owed. (Phase 0b docs restore and Phase 1 rank/UTF-8/staleness patch landed
[PR #5](https://github.com/Joshua-Asante/first-passage/pull/5) / [#6](https://github.com/Joshua-Asante/first-passage/pull/6)
between that entry and this one, without their own SESSIONS rows — noted here for the record.)

**Shipped:** branch `claude/limb-b-remeasure-v3-0815` — frozen
[v3 pre-registration](briefs/pre-registration/2026-08-15-fts5-delete-falsifier-prereg-v3.md)
(measured = shipped, bound to `repo_retrieve.py`'s blob hash); Run A on the shipped tool
(`R_shipped@5 = 0.500`, floor FAIL, beats `rg` 0.088); one permitted corpus-widening revision
(`docs/briefs/*.md`, `docs/notes/audits/**`, `docs/methodology/`, `docs/spec/`, still excluding
`docs/ltm/`/`lab/archive/`); Run B on the widened, committed corpus — unchanged recall (0.500)
despite a higher reachability ceiling (0.676→0.735), a bm25-corpus-statistics effect reported
not chased. Final verdict **`ASSISTIVE-ONLY`** — no Run C, per the frozen cap.
[`RESULTS`](../lab/analysis/harvest/limb_b_remeasure_2026-08/RESULTS.md).

**Decisions/defects:** no new ADR. Companion call in `check_advisor_dedup.py` stays disabled —
settled disposition, not a pending fix. Q-XMEM-1 not closed (A3 pre-condition is a separate
operator gate). Found and fixed a blob-hash integrity bug in the harness itself mid-run
(hand-rolled sha1 disagreed with `git hash-object` under `core.autocrlf=true`) — the
measurement was unaffected, the diagnostic print was not.

**Open / next:** `path-liveness`/`root-doc-liveness` `path-conditional` re-tier revert still
owed (carried from 2026-08-15d, untouched this session). Limb C (local-embedder vector)
question is now live per Q-XMEM-1's own trigger but not authorized — needs a Rule 2 cost
dry-run, operator-paced. `docs/notes/audits/` restore (PR #5) covered only that subtree;
`docs/notes/notice/`, `docs/notes/rail_build/`, and dated top-level notes stay excluded — the
16 remaining `root-doc-liveness` dead links trace there. Carry: F1 2026-11-08; M1; weekly
token; Magdon-Ismail B.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-15d — Limb B (repo_retrieve) quarantined — governance-belt audit

**Focus:** Meta-layer programme audit of the PR #2 governance belt found `scripts/repo_retrieve.py` recall-regressed below its own 2026-07-27 `DELETE-HOLDS` authorization (unranked `FTS5 MATCH`; recall@5 measured at incumbent-parity, 0.086, tying the `rg` baseline it was built to beat). Verdict: **Degenerating** (meta layer).

**Shipped:** branch `claude/limb-b-quarantine-0815` — `check_advisor_dedup.py` FTS companion call disabled; session-discipline attestation instruction suspended; `docs/briefs/INDEX.md` + Q-XMEM-1 brief status cells flagged. No code fix yet — quarantine only.

**Decisions/defects:** no new ADR. Full seven-diagnostic audit + measurement lineage lives in `first-passage-archive` (`docs/notes/` omitted from this seed) — that repo is now GitHub-archived (read-only); restoring `docs/notes/` here, or another lineage channel, is an open operator call.

**Open / next:** re-rank + re-measure `repo_retrieve.py` against the frozen 0.70 / `R_fts5 > R_rg` table before re-enabling (owner: operator, due 2026-08-22). `path-liveness` / `root-doc-liveness` gates were re-tiered `path-conditional` in PR #2 with regexes that never match `lab/|core/|ops/` — miss a moved/deleted link target at pre-commit; revert owed. Carry: F1 2026-11-08; M1; weekly token; Magdon-Ismail B.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-15c — public-seed CI adaptation (skills + pytest)

**Focus:** Unblock Tests / Skills Check / Pylint on the public seed — dead `docs/notes/**` / `docs/ltm/**` / `docs/superpowers/**` cites and redacted baseline PF, not new product bugs.

**Shipped:** branch `cursor/public-seed-ci-adaptation-52bf` — [PR #3](https://github.com/Joshua-Asante/first-passage/pull/3) — drop or archive-repoint the excluded skill refs; skip pytest when those trees (or thin git ancestry) are absent; `BaselineDataUnavailable` when `baselines.md` holds the public-tree placeholder. Does not restore excluded trees or Pepperstone PF numbers.

**Decisions/defects:** none new. Follows [public-visibility transition](adr/2026-08-14-repo-public-visibility-transition.md) §6 seed exclusions.

**Open / next:** operator ruling still owed on `closure-disposition-coverage-hard.md` (new hard gate landed 4 days into F-2's own trigger window — worth it or not); GitHub webhook trigger's branch filter not yet narrowed to `cursor/*` (cosmetic, routine's own logic already re-scopes). Carry: F1 2026-11-08; M1; weekly token; Magdon-Ismail B.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-15b — search / memory / doc-weight phases (public replay)

**Focus:** Close the search-blindness → new artifact → stale index loop (registry feed, amendment-first, Limb B FTS, liveness sweep, Rule 2 pointers, gate/CI diet). Live rail out of scope. Replayed onto the public seed; merged after [PR #1](https://github.com/Joshua-Asante/first-passage/pull/1).

**Shipped:** branch `cursor/search-memory-liveness-2af2` — [PR #2](https://github.com/Joshua-Asante/first-passage/pull/2) — Rule 8.9/8.10 + addenda on [dedup-first](adr/2026-08-13-dedup-first-before-new-work.md) / [ceremony-tiering](adr/2026-08-08-adr-ceremony-tiering.md) / [W5](adr/2026-08-07-w5-governance-diet.md); [Q-XMEM-1](briefs/Q-XMEM-1-cross-surface-memory-sidecar-pilot.md) v1.2 Limb B; `scripts/repo_retrieve.py` + `scripts/sync_liveness_indexes.py`; INDEX CON-3/CON-4 repair. Mem0 T0 and local vector unpaid. Trip-log not replayed (`docs/notes/` omitted from the public seed).

**Decisions/defects:** no new ADR. Rule 2 stays PROPOSED.

**Open / next:** operator ruling still owed on `closure-disposition-coverage-hard.md` (new hard gate landed 4 days into F-2's own trigger window — worth it or not); GitHub webhook trigger's branch filter not yet narrowed to `cursor/*` (cosmetic, routine's own logic already re-scopes). Carry: F1 2026-11-08; M1; weekly token; Magdon-Ismail B. Limb A Mem0 T0 = operator GO only. Limb C vector only if Limb B misses.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-15a — Repoint historical PR/commit hrefs at first-passage-archive

**Focus:** After the 2026-08-14 public-repo transplant, historical GitHub PR/commit links still pointed at `first-passage` and 404'd; the objects live on the private archive.

**Shipped:** branch `cursor/repoint-archive-pr-links-52bf` — [PR #1](https://github.com/Joshua-Asante/first-passage/pull/1) — 48 hrefs in 8 files rewritten `first-passage` → `first-passage-archive` (`/pull/` + `/commit/` only). Append-only comparator treats that repo-name rewrite as non-mutation. Bare `PR #NNN` prose left alone.

**Decisions/defects:** none new. Owner: [transition ADR](adr/2026-08-14-repo-public-visibility-transition.md).

**Open / next:** operator ruling still owed on `closure-disposition-coverage-hard.md` (new hard gate landed 4 days into F-2's own trigger window — worth it or not); GitHub webhook trigger's branch filter not yet narrowed to `cursor/*` (cosmetic, routine's own logic already re-scopes). Carry: F1 2026-11-08; M1; weekly token; Magdon-Ismail B.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14y — F-2 closure + CC/Cursor autonomous-loop ADR + webhook live

**Focus:** Close the Great Prune's fired F-2 falsifier; ratify a CC/Cursor autonomous dispatch-detect-merge loop at operator direction.

**Shipped:** branch `claude/first-passage-requirements-review-8c0bd9` — [`2026-08-14-f2-adr-corpus-disposition.md`](notes/audits/programme-audit/2026-08-14-f2-adr-corpus-disposition.md) (126-ADR corpus classified, 0/4 tombstone candidates survived adversarial verification) · addendum on [`2026-08-08-great-prune.md`](adr/2026-08-08-great-prune.md) · [`2026-08-14-cc-cursor-autonomous-loop.md`](adr/2026-08-14-cc-cursor-autonomous-loop.md) (Supersedes-in-part `2026-07-14-cc-cursor-surface-allocation.md`) · webhook routine live (`trig_012nvuH7jqmjFUFgoFVpZ6RP`, every-6h cron + GitHub PR-opened event). $0 · K=0.

**Decisions/defects:** F-2 ruled fired-on-a-miscalibrated-premise, not degeneration; instrument replaced (content-sample re-test), no new hard gate. 5 backlog-fix chips this session dispatched independently merged as PRs #824-826/828/829 before this branch landed — direct re-implementation of the same 5 fixes was reconciled out via hard-reset-and-restore rather than committed, confirmed non-duplicative by adversarial re-check (all 5 PRs fully cover scope). Auto-mode classifier blocked `gate_manifest.py`/`pytest` mid-session; resolved via a `.claude/settings.json` permission-allow rule.

**Open / next:** operator ruling still owed on `closure-disposition-coverage-hard.md` (new hard gate landed 4 days into F-2's own trigger window — worth it or not); GitHub webhook trigger's branch filter not yet narrowed to `cursor/*` (cosmetic, routine's own logic already re-scopes). Carry: F1 2026-11-08; M1; weekly token; Magdon-Ismail B.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14x — breadth.py --self-test SKIP exits 2

**Focus:** Make `--self-test` SKIP distinguishable from PASS at the shell exit-code level.

**Shipped:** `main` — `lab/research_utils/breadth.py` SKIP returns `SELF_TEST_SKIP=2` (0 PASS / 1 FAIL unchanged); `tests/test_breadth.py` expects 2. Not wired in `scripts/gates.yml` / Makefile / CI.

**Decisions/defects:** none. Convention matches `pine_lint._self_test` missing-fixture = 2.

---

## 2026-08-14w — W1 materialized harness sys.path

**Focus:** Fix pre-existing `ModuleNotFoundError: reconcile` in `tests/test_nsurv_channel.py::test_w1_pin_reproduction_known_answer` when the pruned Class-S scoring harness is copied under pytest `tmp_path`.

**Shipped:** branch `cursor/w1-materialize-syspath-25b2` — [PR #832](https://github.com/Joshua-Asante/first-passage-archive/pull/832) — pin materialized `_ROOT` to the real repo (not `__file__.parents[3]`) in `_materialize_pruned_scoring_helpers`. Test-infrastructure only. $0 · K=0.

**Decisions/defects:** none new. Depth-relative `_ROOT` is correct at `lab/analysis/c1/<slug>/`; the bug is the materialization copy, not the historical harness.

**Open / next:** Raise Actions spending cap (operator). MSL still E1 HOLD, no slate-4 until NEW WHO. Carry: F-2; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B. Confirm #806 CI; cart confirm. Third-leg spec still restates 08-06 retained-not-released (owed).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14v — CI diet (A+C+D) + ripgrep

**Focus:** Cut GitHub Actions minutes after billing-limit brick on #825–#828; restore pytest `rg` so the 1524-pass suite can go green.

**Shipped:** branch `cursor/ci-diet-pr-main-2df9` — [PR #831](https://github.com/Joshua-Asante/first-passage-archive/pull/831) — `.github/workflows/{tests,pylint,skills-check}.yml`. A: PR + `main` only. C: pylint 3.11 only. D: skip Tests/Pylint on `*.md` / `.claude/**`. Tests job installs ripgrep.

**Decisions/defects:** none new. CI trigger/path diet only; no gate dropped from `scripts/gates.yml`.

**Open / next:** Raise Actions spending cap (operator). MSL still E1 HOLD, no slate-4 until NEW WHO. Carry: F-2; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B. Confirm #806 CI; cart confirm. Third-leg spec still restates 08-06 retained-not-released (owed).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14u — MSL falsifier survival-limb + explore-stage (5a) ADRs accepted

**Focus:** Operator election on the programme-audit's two follow-on ADRs; apply the charter/plan amendments each one owed.

**Shipped:** branch `claude/msl-programme-audit-2026-08-14` — [PR #830](https://github.com/Joshua-Asante/first-passage-archive/pull/830) — [survival-limb ADR](adr/2026-08-14-msl-yield-falsifier-survival-limb.md) Accepted (charter Gate line + plan §6/§7) · [explore-stage ADR](adr/2026-08-14-msl-explore-stage-5a.md) Accepted, light-tier (charter step **5a** + plan P3.x row) · [audit note](notes/audits/programme-audit/2026-08-14-msl-methodology-audit.md) §5/§11 discharge notes. $0 · K=0.

**Decisions/defects:** Non-disruptive "5a" insertion chosen over a full renumber — grep confirmed external step-number citations outside the charter. Owner: both ADRs above.

**Open / next:** MSL still E1 HOLD, no slate-4 until NEW WHO. Carry: F-2; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B. Confirm #806 CI; cart confirm.

---

## 2026-08-14t — C3 eviction-clause skip narrowed

**Focus:** Stop `check_status_consistency` whole-line-skipping a live `lab/` citation that shares a line with a `git show` / `pre-prune-` retrieval. Also correct the stale CLAUDE.md M1 interlock warning and make breadth `--self-test` SKIP exit 2.

**Shipped:** branch `fix/c3-eviction-clause-skip` — [PR #829](https://github.com/Joshua-Asante/first-passage-archive/pull/829) — `scripts/check_status_consistency.py` masks only the eviction clause (plus enclosing paren); mixed-line C3 regression; CLAUDE.md M1 line points at `validate(..., require_resolved=True)`; `lab/research_utils/breadth.py` `SELF_TEST_SKIP=2`; repointed the now-visible stale href in `docs/rejected_candidates.md`.

**Decisions/defects:** none. Twins still whole-line: `scripts/check_root_doc_liveness.py`, `scripts/check_md_relative_links.py`.

**Open / next:** CapFLOW Cap-spend FALSIFIED (Cap held). Carry: F-2; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; no slate-4 until NEW WHO. Confirm #806 CI; cart confirm. Third-leg spec still restates 08-06 retained-not-released (owed).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14s — MVD ceremony vs enforcement

**Focus:** Verify Stage-8 variance-dominance header (no edit) and reconcile MVD-discipline ceremony to what is actually enforced.

**Shipped:** branch `cursor/mvd-ceremony-reconcile-a1df` — [PR #828](https://github.com/Joshua-Asante/first-passage-archive/pull/828) — [MVD addendum](adr/2026-04-24-mvd-discipline.md). Stage-8 risk-N_eff ADR left unchanged (W4 in-part edge already complete). $0 · K=0.

**Decisions/defects:** none new. Owner: the 2026-08-14 addendum on [MVD discipline](adr/2026-04-24-mvd-discipline.md). Code checks untouched.

**Open / next:** CapFLOW Cap-spend FALSIFIED (Cap held). Carry: F-2; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; no slate-4 until NEW WHO. Confirm #806 CI; cart confirm. Third-leg spec still restates 08-06 retained-not-released (owed).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14r — Reconcile four partial-live ADRs

**Focus:** Dated Rule-14 addenda on four ADRs whose core decisions stand but whose machinery/status/occupancy framing had been overtaken.

**Shipped:** branch `cursor/adr-reconciliation-addenda-a1df` — [PR #827](https://github.com/Joshua-Asante/first-passage-archive/pull/827) — [reality-check](adr/2026-05-22-reality-check-harness.md) Component A dormant · [sweep-engine](adr/2026-06-05-sweep-engine.md) machinery retired / invariant live · [S7 occupancy](adr/2026-07-29-third-leg-symbol-occupancy-limb.md) 08-06 retained-not-released superseded · [venue-binding](adr/2026-08-05-strategy-venue-binding-axis.md) stalled/bypassed (Status stays Proposed). $0 · K=0.

**Decisions/defects:** none new. Owners: the four 2026-08-14 addenda. S7 untouched; Striker legs stay barred.

**Open / next:** CapFLOW Cap-spend FALSIFIED (Cap held). Carry: F-2; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; no slate-4 until NEW WHO. Confirm #806 CI; cart confirm. Third-leg spec still restates 08-06 retained-not-released (owed).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14q — Repair three vacuous gate scripts

**Focus:** Fix three live `scripts/` gate defects: A5 LOCK.md glob, `--enable` typo-pass, C3 theme-nest blind spot.

**Shipped:** branch `cursor/fix-dead-gate-scripts-bc8b` — [PR #825](https://github.com/Joshua-Asante/first-passage-archive/pull/825) — `scripts/check_adr_graph.py` · `scripts/check_status_consistency.py` · 11 instrument theme-nest repoints.

**Decisions/defects:** none. Gates now evaluate their targets (A5 once the age window opens; `--enable` rejects unknown ids; C3 flags flat-to-theme-nest).

**Open / next:** CapFLOW Cap-spend FALSIFIED (Cap held). Carry: F-2; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; no slate-4 until NEW WHO. Confirm #806 CI; cart confirm.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14p — Dead-trigger docs marked dormant

**Focus:** Four independently verified dead-trigger surfaces (2026-08-14): delete lock-brief template; dormancy-mark 1R live-calibration + E1–E4; discharge lean-portfolio meta-layer falsifier.

**Shipped:** branch `cursor/dormant-dead-trigger-docs-0ebd` — [PR #824](https://github.com/Joshua-Asante/first-passage-archive/pull/824) — [lock_decision.md deleted](../.claude/skills/brief-authoring/SKILL.md) · [1r_estimation](methodology/1r_estimation.md) · [lean-portfolio addendum](adr/2026-06-04-lean-portfolio-meta-layer.md) · [E1–E4](methodology/lessons/execution_lessons.md). $0 · K=0.

**Decisions/defects:** §4 falsifier of [lean-portfolio](adr/2026-06-04-lean-portfolio-meta-layer.md) recorded FIRED 2026-07-30 (ceremonial; children live). Owner: that ADR's 2026-08-14 addendum.

**Open / next:** CapFLOW Cap-spend FALSIFIED (Cap held). Carry: F-2; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; no slate-4 until NEW WHO. Confirm #806 CI; cart confirm.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14o — CapFLOW Cap-spend FALSIFIED (Cap held)

**Focus:** Discharge Q-CAPFLOW-1 Cap-spend: rebuild A×R join, score once under frozen PREREG.

**Shipped:** branch `cursor/capflow-score-0814` — [PR #823](https://github.com/Joshua-Asante/first-passage-archive/pull/823) — camp [`mnq_capflow_orb_r_2026-08`](../lab/analysis/c1/mnq_capflow_orb_r_2026-08/) · [RESULTS](../lab/analysis/c1/mnq_capflow_orb_r_2026-08/RESULTS.md) · [closure](briefs/closures/Q-CAPFLOW-1-closure-falsified.md). $0 new pull · Cap held · K=0.

**Decisions/defects:** CI includes 0 (ρ +0.020); C11 stands. Owner: [closure](briefs/closures/Q-CAPFLOW-1-closure-falsified.md).

**Open / next:** CapFLOW Cap-spend FALSIFIED (Cap held). Carry: F-2; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; no slate-4 until NEW WHO. Confirm #806 CI; cart confirm.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14n — MSL WHO-track (estate-wide; still dry)

**Focus:** Deep zero-data WHO track after E1 HOLD — every Tradeify product group + census backlog, not just MCL fade.

**Shipped:** branch `cursor/msl-who-track-85f5` — [PR #822](https://github.com/Joshua-Asante/first-passage-archive/pull/822) — [notice](notes/notice/N-2026-08-14-msl-who-track.md) · plan §6 P3.8 **STILL DRY** · no camp · no card · no new `MECHANISMS.md` id. $0 · K=0.

**Decisions/defects:** No NEW WHO. Closest leftovers (FX option-cut, USDA grains, Bund auction, LME warrants, pipeline nominations) die on sign / EIA-family / H-ZNAUC / F4 / §4.1a before 1a clears. Owner: [notice](notes/notice/N-2026-08-14-msl-who-track.md).

**Open / next:** no slate-4 card until NEW WHO. Carry: F-2; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B. Confirm #806 CI; cart confirm.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14m — MSL §7 E1 HOLD recorded

**Focus:** Record operator E1 HOLD on the §7 slate-generation packet.

**Shipped:** branch `cursor/msl-s7-e1-hold-85f5` — [PR #821](https://github.com/Joshua-Asante/first-passage-archive/pull/821) — [closure](briefs/closures/MSL-S7-closure-resolved-e1-hold.md) · plan §4/§6 Phase 3 **HOLD (E1)** · no camp · no E2 ADR. $0 · K=0.

**Decisions/defects:** E1 marked (plan confirmation). Charter stays RATIFIED. Yield not fired. Owner: [closure](briefs/closures/MSL-S7-closure-resolved-e1-hold.md).

**Open / next:** no slate-4 card until NEW WHO. Carry: F-2; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B. Confirm #806 CI; cart confirm.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14k — MSL §7 slate-generation review packet (OWED-election)

**Focus:** Plan-§7 Board packet: evidence + E1 HOLD / E2 CLOSE; do not elect.

**Shipped:** branch `cursor/msl-s7-board-review-85f5` — [PR #820](https://github.com/Joshua-Asante/first-passage-archive/pull/820) — [packet](briefs/2026-08-14-msl-slate-generation-review.md) · plan §6 P3.7 **OWED-election** · no camp · no E2 ADR. $0 · K=0.

**Decisions/defects:** Yield not fired (four G0s; two pre-G0 deaths). Operator owns E1/E2. Owner: [packet](briefs/2026-08-14-msl-slate-generation-review.md).

**Open / next:** Operator mark E1 (HOLD, recommended) or E2 (CLOSE via full ADR). Carry: F-2 disposition; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; research venvs. Confirm #806 CI; cart confirm.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14j — MSL slate-3 BLOCKED (mechanism-dry)

**Focus:** Board-lite slate-3 constraints + zero-data WHO attempt on MCL fade; stop if INTAKE-DRY.

**Shipped:** branch `cursor/msl-slate3-constraints-85f5` — [PR #819](https://github.com/Joshua-Asante/first-passage-archive/pull/819) — [notice](notes/notice/N-2026-08-14-msl-slate-3-constraints.md) · plan §6 P3.6 **BLOCKED** · no `msl_s3a_*` camp. $0 · K=0.

**Decisions/defects:** No WHO outside 2026-08-10 INTAKE-DRY; implied-SR reopen restored geometry not a flow family. §7 Board review owed (functional 3/3). Owner: [notice](notes/notice/N-2026-08-14-msl-slate-3-constraints.md).

**Open / next:** Operator §7 slate-generation review. Carry: F-2 disposition; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; research venvs. Confirm #806 CI; cart confirm.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14l — STATE F-2 queue row: fired-axis framing

**Focus:** Sharpen OPERATOR QUEUE row 2 so Great-prune F-2 reads as axis-fired, not “trending toward.”

**Shipped:** branch `docs/f2-queue-fired-axis-framing` — [PR #818](https://github.com/Joshua-Asante/first-passage-archive/pull/818) — re-measure at `origin/main` `df2c448`: ADR-count +14 (~400% of 50% ADR-Δ trigger, fired); file-Δ ~131% (fired); bytes ~63% of thresh (still short). [`STATE.md`](../STATE.md) row 2 only. Incidental: `msl_s2b` `verdict.md` + CATALOG heavy/one-liner align so `lab-catalog` passes (was red on main post-#817).

**Decisions/defects:** None — measurement/framing only; operator disposition still open ([`Great Prune §4 F-2`](adr/2026-08-08-great-prune.md)).

**Open / next:** Operator F-2 disposition still open (ADR-count axis already fired). Carry from 14i: Board next slate/channel after Stage-1 deaths 2/3; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; research venvs; `#806` CI; cart confirm.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14i — MSL-S2B Stage-0/1 FAIL (route)

**Focus:** S2B Stage-0 pins + Stage-1 door-check on MYM `sweep-failure-filtered-continuation`; route kill limb #1 first.

**Shipped:** branch `cursor/msl-s2b-stage01-85f5` — [PR #817](https://github.com/Joshua-Asante/first-passage-archive/pull/817) — camp [`msl_s2b_mym_2026-08`](../lab/analysis/c1/msl_s2b_mym_2026-08/) · [STAGE0](../lab/analysis/c1/msl_s2b_mym_2026-08/STAGE0.md) · [STAGE1](../lab/analysis/c1/msl_s2b_mym_2026-08/STAGE1.md) · [closure](briefs/closures/MSL-S2B-closure-stage1-fail-route.md) · MECHANISMS + registry + plan §6. $0 · K=0. No G0/Pine. Renumbered `14h`→`14i` on merge (#816 claimed `14h`).

**Decisions/defects:** Pre-G0 kill — raised bar unbound for continuation *entry*; SLR route ① filter-only; temporal-selectivity paused; composite refused. Owner: [second slate §S2B](briefs/2026-08-13-msl-second-slate.md) · [closure](briefs/closures/MSL-S2B-closure-stage1-fail-route.md).

**Open / next:** Stage-1 deaths **2/3**; slate-2 exhausted — Board owns next slate / channel review. Carry: Operator F-2 disposition (ADR-count axis already fired — from 14h/#816); CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; research venvs. On Windows: `make sync-skills` from primary checkout. Confirm #806 CI green; cart confirm.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14h — Post-chip-landing verification sweep + gap repair

**Focus:** Verify all 9 chips from 14a-14g actually landed correctly (8-agent workflow); fix what didn't.

**Shipped:** branch `claude/post-prune-simplification-acd9d7` — [PR #816](https://github.com/Joshua-Asante/first-passage-archive/pull/816) — archived `msl_c3_m2k_2026-08` + `msl_s2a_mcl_2026-08` (self-flagged owed since 14a-14g, never ran); fixed `archive_lab_analysis.rewrite_sibling_links()` multi-hop `../` corruption (64 links, +regression test); repointed 6 living-doc citations (STATE, `ops/instruments/*`, `rejected_candidates`) + rebuilt `PROFILES.md`/`profiles.json`; regenerated `lab/CATALOG.md` (also clears 9 phantom-Active rows [PR #809](https://github.com/Joshua-Asante/first-passage-archive/pull/809) reintroduced on `origin/main`); backfilled `Tier: light` on the one retire_adr stub written before [PR #812](https://github.com/Joshua-Asante/first-passage-archive/pull/812) landed; mirrored `mc` into `check_status_consistency._THEME_ORDER` (pre-existing pytest fail from PR #790, unrelated to 14a-14g); split STATE's dormant-threads pointer so Q-MSCHAN-1 (SUBTRACT/dead) no longer reads as open like b6/b7 (PARK).

**Decisions/defects:** [PR #810](https://github.com/Joshua-Asante/first-passage-archive/pull/810)'s on-machine `~/.claude/skills` resync still NOT done — `sync_skills.py` refuses `--force`-less deploy from a worktree checkout by design; needs `make sync-skills` from the primary checkout. F-2 ([809](https://github.com/Joshua-Asante/first-passage-archive/pull/809)/STATE queue row): ADR-count axis has already fired at 400% of its 50%-of-pruned-delta threshold (14 vs 3.5), not merely trending — byte/file framing undersold this.

**Open / next:** Operator F-2 disposition — now sharper: ADR-count axis already fired. On Windows: `make sync-skills` from primary checkout (from 14c/14g, still open). Confirm #806 CI green; cart confirm; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; research venvs. Ceremony-tiering falsifier review at first quarterly after 08-08 (STATE 11-08).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14g — Implied-SR candidate incident + light ADR word-cap trims

**Focus:** Log ceremony-tiering omitted-apparatus candidate (implied-SR light→full escalation); trim two over-300-word light ADRs.

**Shipped:** branch `cursor/implied-sr-incident-and-light-adr-trims-d214` — [PR #815](https://github.com/Joshua-Asante/first-passage-archive/pull/815) — [ceremony-tiering addendum](adr/2026-08-08-adr-ceremony-tiering.md) · STATE `### 2026-11-08` pointer · trims [C3 revive](adr/2026-08-13-msl-c3-k2-dual-axis-revive.md) · [Survive bound](adr/2026-08-09-survive-bound-is-the-queue-cap.md). No retired-ADR rewrites.

**Decisions/defects:** Candidate incident only (1-vs-2 = audit call). Owner: [ceremony tiering §Falsifier](adr/2026-08-08-adr-ceremony-tiering.md).

**Open / next:** Operator F-2 disposition (from 14b/14c). Confirm #806 CI green; cart confirm; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; research venvs. On Windows: `make sync-skills` (from 14c). Ceremony-tiering falsifier review at first quarterly after 08-08 (STATE 11-08).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14f — same-theme collision WARN test coverage

**Focus:** Pin `warn_new_slug_same_theme_collisions()` with positive/negative stderr tests so a silent catalog-parse refactor cannot drop the ADR 2026-08-13 report-only WARN.

**Shipped:** branch `cursor/test-same-theme-collision-warn-b103` — [PR #814](https://github.com/Joshua-Asante/first-passage-archive/pull/814) — [`tests/test_archive_lab_analysis.py`](../tests/test_archive_lab_analysis.py) (`test_warn_new_slug_same_theme_collision_emits_stderr`, `test_warn_new_slug_same_theme_collision_silent_without_overlap`).

**Decisions/defects:** Owner: [dedup-first before new work](adr/2026-08-13-dedup-first-before-new-work.md) §2 leg 3.

**Open / next:** Operator F-2 disposition (from 14b/14c). Confirm #806 CI green; cart confirm; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; research venvs. On Windows: `make sync-skills` (from 14c).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14e — CLAUDE.md MYM/MNQ occupancy pointer

**Focus:** Close the posture-summary gap for [MYM/MNQ occupancy release](adr/2026-08-12-msl-mym-occupancy-release.md) per root-doc charter §2 / Rule 7.

**Shipped:** branch `cursor/claude-mym-mnq-occupancy-pointer-85b2` — [PR #813](https://github.com/Joshua-Asante/first-passage-archive/pull/813) — one Standing-decision row in [`CLAUDE.md`](../CLAUDE.md) linking `[occupancy]` (no retelling).

**Decisions/defects:** Owner unchanged: [occupancy ADR](adr/2026-08-12-msl-mym-occupancy-release.md). Pointer-only; Striker redeploy bar stands.

**Open / next:** Operator F-2 disposition (from 14b/14c). Confirm #806 CI green; cart confirm; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; research venvs. On Windows: run `make sync-skills` (from 14c).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14d — Preserve Tier on retire_adr stubs

**Focus:** Stop `retire_adr.build_stub()` from dropping `**Tier:** light` so superseded light ADRs stay visible to hot-dir census greps.

**Shipped:** branch `cursor/preserve-retire-adr-tier-0f0c` — [PR #812](https://github.com/Joshua-Asante/first-passage-archive/pull/812) — [`scripts/retire_adr.py`](../scripts/retire_adr.py) `extract_tier` + stub carry-forward; tests in [`tests/test_retire_adr.py`](../tests/test_retire_adr.py). No already-retired stub rewrites.

**Decisions/defects:** None — tool fix only. Convention owner: [ADR ceremony tiering](adr/2026-08-08-adr-ceremony-tiering.md).

**Open / next:** Operator F-2 disposition (from 14b/14c). Confirm #806 CI green; cart confirm; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; research venvs. On Windows: `make sync-skills` (from 14c).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14c — ADR-tiering discoverability (brief-authoring + skills sync)

**Focus:** Make the 2026-08-08 ADR ceremony tiering convention discoverable at the ADR template and keep `~/.claude/skills/` from silently drifting.

**Shipped:** branch `cursor/adr-tiering-brief-authoring-fa22` — [PR #810](https://github.com/Joshua-Asante/first-passage-archive/pull/810) — tier-test branch atop [`.claude/skills/brief-authoring/references/adr.md`](../.claude/skills/brief-authoring/references/adr.md); [`scripts/sync_skills.py`](../scripts/sync_skills.py) / hook deploy to AppData **and** `~/.claude/skills/`; tests in [`tests/test_sync_skills.py`](../tests/test_sync_skills.py).

**Decisions/defects:** Owner: [ADR ceremony tiering](adr/2026-08-08-adr-ceremony-tiering.md). Cloud host had no prior `~/.claude/skills/brief-authoring` (copied fresh; Windows machine still needs `make sync-skills` or pull+hook).

**Open / next:** Operator F-2 disposition (from 14b). Confirm #806 CI green; cart confirm; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; research venvs. On Windows: run `make sync-skills` so the May-stale home brief-authoring cache is overwritten (script now backs both targets).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14b — escalate Great-prune F-2 re-accretion

**Focus:** Re-measure post-prune tracked size at current `origin/main` and surface F-2 breach on the OPERATOR QUEUE without deciding or building the gate.

**Shipped:** fast-forwarded local `main` to `669df95`; `STATE.md` OPERATOR QUEUE row 2 only (queue 3/5). Measure: HEAD 23,198,115 B / 2,161 files / 128 ADRs vs `7aab114` 20,343,262 / 1,757 / 114.

**Decisions/defects:** None — operator pick owed (gate now · recalibrate · accept as R1). Formal F-2 ADR limb breached (+14 ADRs vs 50% of −7 prune Δ); bytes at 62.4% of thresh. [`Great Prune §4`](adr/2026-08-08-great-prune.md).

**Open / next:** Operator F-2 disposition. Carry from 14a: Confirm build/pytest 3.11+3.12 + `validation-controls` green on #806; cart confirm; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; research venvs.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14a — validation-controls collection + ops lock py311

**Focus:** Unblock CI after Actions re-enable: `validation-controls` collection errors (stale ignore, `test_construct_lib` collisions, orphan import camps) plus `numpy==2.5.1`/`scipy==1.18.0` 3.12-only pins.

**Shipped:** branch `cursor/fix-validation-controls-collect-0813` — [PR #806](https://github.com/Joshua-Asante/first-passage-archive/pull/806) — archive ignore + `--import-mode=importlib` + [`camp_import.py`](../lab/research_utils/camp_import.py); `pyproject.toml` `numpy<2.5`/`scipy<1.18`, lock regenerated on 3.11 (`numpy==2.4.6`, `scipy==1.17.1`).

**Decisions/defects:** Hyphenated camp slugs cannot be packages; lock was compiled on 3.12 with unconstrained deps. Ops-lock 13z dropped here (main claimed 13z for PR #805).

**Open / next:** Confirm build/pytest 3.11+3.12 + `validation-controls` green on #806. Carry from 13z: cart confirm; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; research venvs.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13a — SESSIONS append-only gate + push-collision exemption

**Focus:** Packet 1 of union-merge hygiene: freeze prior SESSIONS entry bodies and stop treating two new top entries as a governance collision.

**Shipped:** branch `fix/sessions-append-only-collision` — [PR #808](https://github.com/Joshua-Asante/first-passage-archive/pull/808) — `roll_sessions.py --check-append-only` (gates.yml `sessions-append-only`); `check_push_collision` drops `docs/SESSIONS.md` when ours is append-only vs merge-base. Tests in `tests/test_roll_sessions.py` + `tests/test_check_push_collision.py`.

**Decisions/defects:** Mutating a merge-base heading still collides; only the new-heading delta is exempt. Packets 2–4 (auto-normalize, `--next-label` from origin/main, `--append` writer) not in this change.

**Open / next:** Cart confirm before any purchase; re-read fees after 2026-08-31 (or when AUG 5×40% exhausts → 30%). S2B may resume (C3-K2 board slot freed). Carry: CapFLOW; F1 2026-11-08; M1 arm-harden; weekly token. Magdon-Ismail B still undecided (do not wait). Recreate research venvs to pick up aiohttp 3.14.3. Next SESSIONS hygiene: packet 2 (auto `--normalize --reorder` + CI `--check-order`).

---

## 2026-08-13z — CATALOG duplicate-slug check hard-fail

**Focus:** Close the `lab/CATALOG.md` freshness false-pass where `_partition_catalog` last-wins on slug and drops Active+Archived (or same-table) duplicates from `--check --catalog-only`.

**Shipped:** branch `fix/catalog-duplicate-slug-check` — [PR #805](https://github.com/Joshua-Asante/first-passage-archive/pull/805) @ `f27888f` — `_partition_catalog` keys by `(section, slug)`; same-section dupes → `_CATALOG_STALE`; planted Active+Archived regression in `tests/test_archive_lab_analysis.py` (2026-08-13 MSL phantom-row class).

**Decisions/defects:** Defect in checker logic (instance rows already hand-fixed in PR #802); this is the gate hardening.

**Open / next:** Cart confirm before any purchase; re-read fees after 2026-08-31 (or when AUG 5×40% exhausts → 30%). S2B may resume (C3-K2 board slot freed). Carry: CapFLOW; F1 2026-11-08; M1 arm-harden; weekly token. Magdon-Ismail B still undecided (do not wait). Recreate research venvs to pick up aiohttp 3.14.3.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13y — TNEC-1 admission gate: EM1/D1/D2 disclosure-only

**Focus:** Align live `evaluate_admission` with ratified TNEC-1 / EM-screen supersession (code still refused on EM1 0.40R and D1/D2).

**Shipped:** branch `fix/tnec1-admission-disclosure-only` — [`admission_schema.py`](../lab/discovery/admission_schema.py) (N-EDGE gate; EM1/D1/D2 disclosure record); [`register_search.py`](../lab/discovery/register_search.py) + [futures-anomaly-discovery skill](../.claude/skills/futures-anomaly-discovery/SKILL.md) + [`strategy_harvest.md`](methodology/strategy_harvest.md) §6 pointer. Tests in [`test_register_search_admission.py`](../tests/test_register_search_admission.py).

**Decisions/defects:** None new — implements [TNEC-1](spec/2026-08-08-tradeify-necessary-conditions-target-spec.md) / [ADR 2026-08-08](adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md) §2-B already ratified.

**Open / next:** S2B may resume (C3-K2 board slot freed). Carry: CapFLOW; F1 2026-11-08; M1 arm-harden; weekly token. Magdon-Ismail B still undecided (do not wait). Recreate research venvs to pick up aiohttp 3.14.3.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13w — Tradeify Select 100K checkout price re-sourced

**Focus:** Re-verify current Select 100K eval checkout + reset fees (primary page; Rule 13) after JULY promo expiry made the GO ADR $159/$181 figures non-current for modeling.

**Shipped:** branch `cursor/tradeify-select-100k-price-78c1` — [PR #801](https://github.com/Joshua-Asante/first-passage-archive/pull/801) · [`2026-08-13-tradeify-select-100k-checkout-price.md`](notes/2026-08-13-tradeify-select-100k-checkout-price.md); sprint-lane §4 soft-fee caveat + RUNBOOK reset pointer + compliance replacement-cost forward pointer. Historical GO ADR §B4 unpaid overwrite. Label renumbered `13s`→`13w` on merge (collision with Dependabot triage `13s` on main).

**Decisions/defects:** Dated fact only — list $265 / AUG $159 / reset $169 / activation None; promo ends 2026-08-31. Cart line-items not authenticated this pass.

**Open / next:** Cart confirm before any purchase; re-read fees after 2026-08-31 (or when AUG 5×40% exhausts → 30%). S2B may resume (C3-K2 board slot freed). Carry: CapFLOW; F1 2026-11-08; M1 arm-harden; weekly token. Magdon-Ismail B still undecided (do not wait). Recreate research venvs to pick up aiohttp 3.14.3.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13v — ADR 2026-08-13 dedup-first mechanical wiring

**Focus:** Execute [`ADR 2026-08-13`](adr/2026-08-13-dedup-first-before-new-work.md) §7 Phases 1–5 (hookify + keyword search + Rule 8.8 + theme-collision WARN + brief-authoring link).

**Shipped:** branch `cursor/dedup-first-mechanical-wiring-0813` — [PR #800](https://github.com/Joshua-Asante/first-passage-archive/pull/800) @ `8a60c92`/`b48722a` — tracked `.claude/hookify.advisor-dedup-first.md`; `check_advisor_dedup.py --keywords`; Rule 8 sub-rule 8; `warn_new_slug_same_theme_collisions`; brief-authoring → §8. §10 audits PASS. [ADR](adr/2026-08-13-dedup-first-before-new-work.md). Label renumbered `13u`→`13v` on merge (collision with #799 soft-degrade on main).

**Decisions/defects:** Decision already Accepted; this session is pure mechanical execution (no re-litigation). Report-only WARN only — no `gates.yml` blocking change.

**Open / next:** S2B may resume (C3-K2 board slot freed). Carry: CapFLOW; F1 2026-11-08; M1 arm-harden; weekly token. Magdon-Ismail B still undecided (do not wait). Recreate research venvs to pick up aiohttp 3.14.3.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13u — catalog one-liner soft-degrade (msl_c3 blanking)

**Focus:** Diagnose archive_lab_analysis.py --check --catalog-only hard-fail at 9bcf3cb (CATALOG.md stale vs scan) — hand-authored one-liner blanking on scan when no RESULTS*/README source card.

**Shipped:** branch fix/catalog-one-liner-soft-degrade — soft-degrade in [archive_lab_analysis.py](../scripts/archive_lab_analysis.py) _compare_catalog (committed prose vs scan empty → WARN); tests in [test_archive_lab_analysis.py](../tests/test_archive_lab_analysis.py). Hand-deleted ghost Active row ict_mnq_2026-08 flat-path duplicate in [lab/CATALOG.md](../lab/CATALOG.md) (no --regenerate-catalog).

**Decisions/defects:** Root cause: mid-campaign STAGE*/PREREG-only bodies; choose_source_card returns None. Same class as heavy-column worktree tolerance (third live firing after Magdon catalog-ghost incident).

**Open / next:** S2B may resume (C3-K2 board slot freed). Carry: CapFLOW; F1 2026-11-08; M1 arm-harden; weekly token. Magdon-Ismail B still undecided (do not wait).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13t — MSL-C3-K2 explore FALSIFIED (both axes)

**Focus:** Land M2K BAR EXPORT panel; pay explore GO; score dual-axis IS under `K_intrinsic=2`.

**Shipped:** branch `cursor/msl-c3-k2-explore-023e` — [PR #798](https://github.com/Joshua-Asante/first-passage-archive/pull/798) · `M2K_M15.csv` pin `81922570…` · [`RESULTS_g2`](../lab/analysis/c1/msl_c3_m2k_2026-08/RESULTS_g2.md) · [closure](briefs/closures/MSL-C3-K2-closure-falsified.md) · registry/plan/M2K mirrors. $0 · K spent=0. CONFIRM unread. Label renumbered `13s`→`13t` on merge (collision with Dependabot hygiene on main).

**Decisions/defects:** Both axes CI entirely &lt; 0. Panel ends 2026-07-02 (TV truncation; MCL precedent). Globex session key fixed for Axis B overnight coherence.

**Open / next:** S2B may resume (C3-K2 board slot freed). Carry: CapFLOW; F1 2026-11-08; M1 arm-harden; weekly token. Magdon-Ismail B still undecided (do not wait).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13s — Dependabot aiohttp triage (Hygiene)

**Focus:** Triage GitHub “3 vulnerabilities (1 high, 2 moderate)” notice; no Dependabot auto-fix PRs open.

**Shipped:** branch `cursor/dependabot-aiohttp-triage-03ba` — [PR #797](https://github.com/Joshua-Asante/first-passage-archive/pull/797) · `aiohttp` pin `3.14.1`→`3.14.3` in `requirements-research.txt` · [triage note](notes/2026-08-13-dependabot-aiohttp-triage.md).

**Decisions/defects:** All three alerts = aiohttp research-only (via databento); not ops/rail. setuptools CVE deferred (`nolds` needs `setuptools<81`).

**Open / next:** S2B may resume (C3-K2 board slot freed). Carry: CapFLOW; F1 2026-11-08; M1 arm-harden; weekly token. Magdon-Ismail B still undecided (do not wait). Recreate research venvs to pick up aiohttp 3.14.3.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13r — MSL-C3-K2 dual-axis G0 FROZEN (B4 GO)

**Focus:** Operator B4 GO → freeze dual-axis `PREREG_G0` (`K_intrinsic=2`); GO-gated harness scaffold; no explore/panel/Pine.

**Shipped:** branch `cursor/msl-c3-k2-dual-axis-023e` — [PR #795](https://github.com/Joshua-Asante/first-passage-archive/pull/795) · [`PREREG_G0`](../lab/analysis/c1/msl_c3_m2k_2026-08/PREREG_G0.md) · `construct_lib` / `run_construct_g0` / `EXPLORE_GO.DRAFT` · STAGE1_K2/plan/M2K/registry mirrors. $0 · K spent=0. Explore unpaid.

**Decisions/defects:** Overnight window frozen a priori [18:00→09:29] ET. C1 MYM kill remains adjacency. Estate Cap/DSR/floor unchanged.

**Open / next:** Operator explore GO on C3-K2 (after W4 dry-run + panel pin) — or kill. S2B deferred (route still unresolved; no TV seat). Carry: CapFLOW; F1 2026-11-08; M1 arm-harden; weekly token. Magdon-Ismail B still undecided (do not wait).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13q — MSL-C3-K2 dual-axis Stage-1 revive

**Focus:** Operator elects fresh C3 Stage-1 licensing `K_intrinsic=2` (both PDH/PDL + overnight stories scored); board ahead of S2B.

**Shipped:** branch `cursor/msl-c3-k2-dual-axis-023e` — [PR #795](https://github.com/Joshua-Asante/first-passage-archive/pull/795) · [ADR](adr/2026-08-13-msl-c3-k2-dual-axis-revive.md) · [`STAGE1_K2`](../lab/analysis/c1/msl_c3_m2k_2026-08/STAGE1_K2.md) · `overnight-range-failed-extension-fade` NEW in MECHANISMS · profiles rebuild · plan/S2B/registry mirrors. $0 · K spent=0. B4 unpaid.

**Decisions/defects:** Paying K=2 is the ladder escape hatch — estate Cap/DSR/floor **not** loosened. Prior ≤1-story STAGE1 remains historical OPERATOR-KILL record.

**Open / next:** Operator B4 GO on C3-K2 → dual-axis G0 freeze — or kill. S2B deferred (route still unresolved; no TV seat). Carry: CapFLOW; F1 2026-11-08; M1 arm-harden; weekly token. Magdon-Ismail B still undecided (do not wait).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13p — MSL-S2A explore FALSIFIED (N-ACT)

**Focus:** Operator explore GO on S2A → IS harness + delete/flip (local MCL_M15).

**Shipped:** branch `cursor/msl-s2a-explore-f01c` — [PR #794](https://github.com/Joshua-Asante/first-passage-archive/pull/794) · [`RESULTS_g2`](../lab/analysis/c1/msl_s2a_mcl_2026-08/RESULTS_g2.md) · [closure](briefs/closures/MSL-S2A-closure-falsified.md). $0 · K=0. CONFIRM unread.

**Decisions/defects:** `FALSIFIED` (trades/week 0.511); long FLIP FAIL; DELETE PASS both (moot). Sub-tick sham guard before RESULTS-of-record.

**Open / next:** S2B route still unresolved (do not take TV seat) — or kill. Carry: CapFLOW; F1 2026-11-08; M1 arm-harden; weekly token. Magdon-Ismail B still undecided (do not wait).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13o — MSL-S2A G0 FROZEN (B4 GO)

**Focus:** Operator B4 GO on S2A → charter step 5 G0 freeze (pullback-failure resumption × MCL).

**Shipped:** branch `cursor/msl-s2a-g0-freeze-f01c` — [PR #793](https://github.com/Joshua-Asante/first-passage-archive/pull/793) · [`PREREG_G0`](../lab/analysis/c1/msl_s2a_mcl_2026-08/PREREG_G0.md) · STAGE1/MECHANISMS/plan §6. $0 · K=0. CONFIRM unread.

**Decisions/defects:** `K_intrinsic=1`; rr=3; session 09:00–14:30 ET; roll+FOMC calendars frozen; delete/flip unpaid until explore.

**Open / next:** Operator explore GO on S2A → IS harness + delete/flip — or kill. S2B route still unresolved. Carry: CapFLOW; S2b; F1 2026-11-08; M1 arm-harden; weekly token. Magdon-Ismail B still undecided (do not wait).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13n — MSL P3.4 S2A campaign (MCL continuation)

**Focus:** P3.4 campaign manager — elect slate-2 box, S2A Stage-0 SNAG + Stage-1 pre-G0 on MCL pullback-failure resumption.

**Shipped:** branch `cursor/msl-p34-s2a-campaign-f01c` @ `a37dba86` — [PR #792](https://github.com/Joshua-Asante/first-passage-archive/pull/792) · [box ADR](adr/2026-08-13-msl-slate-2-design-box.md) · [STAGE0](../lab/analysis/c1/msl_s2a_mcl_2026-08/STAGE0.md) · [STAGE1](../lab/analysis/c1/msl_s2a_mcl_2026-08/STAGE1.md). $0 · K=0. No G0. Relettered 13n after #791 claimed 13m.

**Decisions/defects:** box ELECTED (rr∈[2,3]); Magdon-Ismail not calibration; sprint lane not opened; session window 09:00–14:30 ET card-scoped.

**Open / next:** Operator B4 GO on S2A → G0 freeze — or kill. S2B route still unresolved. Carry: CapFLOW; S2b; F1 2026-11-08; M1 arm-harden; weekly token. Magdon-Ismail B still undecided (do not wait).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13m — catalog ghost rows after Magdon merge

**Focus:** Unblock `archive_lab_analysis.py --check --catalog-only` after PR #790 merge re-ghosted archive-flushed Active rows.

**Shipped:** branch `fix/orphan-mc-mdd-catalog` — hand-deleted 12 ghost Active rows in [`lab/CATALOG.md`](../lab/CATALOG.md) (no `--regenerate-catalog`). Heavy annotations untouched.

**Decisions/defects:** Magdon study itself landed correctly under `mc/`; ghosts were merge collateral from [`12126c58`](https://github.com/Joshua-Asante/first-passage-archive/commit/12126c58) onto [#789](https://github.com/Joshua-Asante/first-passage-archive/pull/789).

**Open / next:** B still undecided. Board — first MSL slate exhausted (C2 FALSIFIED · C3 OPERATOR-KILL · C1 FALSIFIED). Carry: CapFLOW; S2b; F1 2026-11-08; M1 arm-harden; weekly token.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13l — Magdon-Ismail MC bust validation

**Focus:** Magdon-Ismail MC bust validation — closed-form \(G_D\) vs production `simulate_path` trailing bust rates.

**Shipped:** branch `lab/mc-mdd-closed-form-2026-08` — [`RESULTS.md`](../lab/analysis/mc/mc_mdd_closed_form_2026-08/RESULTS.md) · harness + fixtures. $0 · K=0.

**Decisions/defects:** none (validation not calibration).

**Open / next:** B still undecided. Board — first MSL slate exhausted (C2 FALSIFIED · C3 OPERATOR-KILL · C1 FALSIFIED). Carry: CapFLOW; S2b; F1 2026-11-08; M1 arm-harden; weekly token.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13k — lab/analysis Wave-1 archive flush

**Focus:** Flush archive-owed hot bodies (option A); nest leftover flat inbox; park c1 cheap-falsifier debris. No `c1` split (B still open).

**Shipped:** branch `cursor/lab-archive-flush-ddac` @ `b2e3eec1` — 15 studies → [`lab/archive/`](../lab/archive/) + CARD stubs; `ict_mnq_2026-08` → [`_inbox`](../lab/analysis/_inbox/ict_mnq_2026-08/); [`cheap_falsifiers_2026-08`](../lab/analysis/c1/cheap_falsifiers_2026-08/). [`CATALOG`](../lab/CATALOG.md).

**Decisions/defects:** `git mv` EXDEV fallback in [`archive_lab_analysis.py`](../scripts/archive_lab_analysis.py). B (split `c1`) not taken.

**Open / next:** B still undecided. Board — first MSL slate exhausted (C2 FALSIFIED · C3 OPERATOR-KILL · C1 FALSIFIED). Carry: CapFLOW; S2b; F1 2026-11-08; M1 arm-harden; weekly token.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13j — MSL-C1 explore FALSIFIED (first slate exhausted)

**Focus:** Operator explore GO on C1 → IS harness + delete/flip score.

**Shipped:** branch `docs/msl-c1-explore` — harness · [`RESULTS_g2`](../lab/archive/msl_c1_mym_2026-08/RESULTS_g2.md) · [closure](briefs/closures/MSL-C1-closure-falsified.md) · registry. $0 · K=0. CONFIRM unread.

**Decisions/defects:** both arms CI entirely &lt; 0 (≈ −0.18/−0.11R); DELETE PASS moot; first slate C2/C3/C1 closed.

**Open / next:** Board — first MSL slate exhausted (C2 FALSIFIED · C3 OPERATOR-KILL · C1 FALSIFIED). Carry: CapFLOW; S2b; F1 2026-11-08; M1 arm-harden; weekly token.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13i — MSL-C1 G0 FROZEN (B4 GO)

**Focus:** Operator B4 GO on C1 → charter step 5 G0 freeze (PDH/PDL failed-break reclaim × MYM).

**Shipped:** branch `docs/msl-c3-kill-c1-stage1` — [`PREREG_G0`](../lab/analysis/c1/msl_c1_mym_2026-08/PREREG_G0.md) · STAGE1/MYM/MECHANISMS/plan §6. $0 · K=0. CONFIRM unread.

**Decisions/defects:** `K_intrinsic=1`; RTH PDH/PDL + 15m reclaim; delete/flip unpaid until explore.

**Open / next:** Operator explore GO on C1 → IS harness + delete/flip — or kill. Carry: CapFLOW; S2b; F1 2026-11-08; M1 arm-harden; weekly token.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13h — MSL-C3 OPERATOR-KILL → C1 Stage-1 PASS (B4 unpaid)

**Focus:** Operator kill C3 (B4 declined) → P3.3 C1 Stage-1 on MYM PDH/PDL reclaim.

**Shipped:** branch `docs/msl-c3-kill-c1-stage1` — [C3 closure](briefs/closures/MSL-C3-closure-operator-kill.md) · registry · [`C1 STAGE1`](../lab/analysis/c1/msl_c1_mym_2026-08/STAGE1.md) · preflight · plan §6. $0 · K=0.

**Decisions/defects:** C3 pre-G0 OPERATOR-KILL (class survives); Stage-1 deaths **1/3**; C1 route ① + B8 CLEAR; three limbs PASS.

**Open / next:** Operator B4 GO on C1 → G0 freeze — or kill → deaths 2/3. Carry: CapFLOW; S2b; F1 2026-11-08; M1 arm-harden; weekly token.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13f — MSL-C3 Stage-1 PASS (B4 unpaid)

**Focus:** P3.2 Stage-1 — freeze stories, route ①, door-check, $0 screens on M2K.

**Shipped:** branch `docs/msl-c3-stage0` — [`STAGE1`](../lab/analysis/c1/msl_c3_m2k_2026-08/STAGE1.md) · `pdh-pdl-failed-break-reclaim` NEW · preflight · profiles rebuild. $0 · K=0.

**Decisions/defects:** elected PDH/PDL failed-break reclaim; overnight story held; RAISED BAR CLEAR via SLR route ①; three limbs PASS.

**Open / next:** Operator B4 GO → G0 freeze — or kill → P3.3 C1. Carry: CapFLOW; S2b; F1 2026-11-08; M1 arm-harden; weekly token.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13e — MSL-C3 Stage-0 PASS (L3 + WSTRUCT + W4)

**Focus:** P3.2 C3 Stage-0 — record L3 one-shot + WSTRUCT sequencing + W4 before flight.

**Shipped:** branch `docs/msl-c3-stage0` — [`STAGE0`](../lab/analysis/c1/msl_c3_m2k_2026-08/STAGE0.md) PROCEED · [`M2K.md`](../ops/instruments/M2K.md) ACTIVE/session · plan §6. $0 · K=0.

**Decisions/defects:** family one-shot void (K_intrinsic=1 brake); WSTRUCT SUPERSEDED-ON-COST sequenced discharged; W4 no pull.

**Open / next:** P3.2 Stage-1 (2–3 stories + door-check + $0 screens at M2K RT $2.82). Carry: CapFLOW; S2b; F1 2026-11-08; M1 arm-harden; weekly token.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13d — MSL-C2 explore GO → FALSIFIED; hand to C3

**Focus:** Local restore `MGC_M15.csv` + issue explore GO; score IS; close C2 on FALSIFIED.

**Shipped:** branch `cursor/msl-c2-explore-prep-292d` — [`RESULTS_g2`](../lab/analysis/c1/msl_c2_mgc_2026-08/RESULTS_g2.md) · [closure](briefs/closures/MSL-C2-closure-falsified.md) · registry row. $0 · K=0. CONFIRM unread.

**Decisions/defects:** both arms CI entirely &lt; 0 (≈ −0.18R); DELETE FAIL. STOP this G0.

**Open / next:** P3.2 C3 (M2K) Stage-0 — L3 one-shot + WSTRUCT sequencing before flight. Carry: CapFLOW; S2b; F1 2026-11-08; M1 arm-harden; weekly token.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13c — MSL-C2 explore-path prep (harness + DRAFT GO)

**Focus:** Prep MSL-C2 explore path — freeze delete/flip in DRAFT; ship GO-gated IS harness; no score / Pine / C3.

**Shipped:** branch `cursor/msl-c2-explore-prep-292d` — [`EXPLORE_GO.DRAFT`](../lab/analysis/c1/msl_c2_mgc_2026-08/EXPLORE_GO.DRAFT.md) · [`construct_lib.py`](../lab/analysis/c1/msl_c2_mgc_2026-08/construct_lib.py) · [`run_construct_g0.py`](../lab/analysis/c1/msl_c2_mgc_2026-08/run_construct_g0.py) · synthetic tests · [explore-GO card](briefs/handoffs/2026-08-13-msl-c2-explore-go-card.md) (UNPAID). $0 · K=0.

**Decisions/defects:** none — explore GO still unpaid; `MGC_M15.csv` bytes still absent this checkout.

**Open / next:** Operator: restore `MGC_M15.csv` + issue explore GO per [card](briefs/handoffs/2026-08-13-msl-c2-explore-go-card.md) → `--explore-go` → Pine CC-solo → B5; else kill → P3.2 C3. Carry: CapFLOW; S2b; F1 2026-11-08; M1 arm-harden; weekly token.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

<!-- ARCHIVE-INDEX:START -->
## Archive index

Older entries rolled to `docs/ltm/notes/archive/sessions/` (newest first).

| Date | Session | Archive |
|---|---|---|
| 2026-08-13 | PR #779 conflict resolve vs main (#778) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-13 | implied-SR demoted to report-only; fade cells reinstated | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | MSL P3.1 C2 B4 GO → G0 FROZEN | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | MSL P3.1 Stage-1 C2 (MGC) PASS → B4 | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | MSL P2 claim-manifest close | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | MSL P3.1 Stage-0 MGC bars | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | MSL P2 umbrella frozen; LOCAL dispatch blocked (no cursor-agent) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | MSL Board B1–B3 + B8 ratified | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | MSL sourcing-channel charter + slate + program plan (P1-reviewed) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | Q-TXG-1 ATR/instrument inputs extension (data-present only) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | Q-TXG-1 H_A ruled CLOSE (FALSIFIED-at-walls) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | Q-TXG-1 H_A re-argument packet authored (ruling pending) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | Q-TXG-1 cell #1 striker_nas100×MYM DEAD(cost) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | Q-TXG-1 cell #2 striker×MNQ DEAD(N-SURV) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | Accept coverage-limb promote-to-HARD ADR | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | Promote coverage limb to self-arming HARD (Proposed) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | Q-TNEC-CON-5 Branch A STOP elected (OHLCV temporal lane paused) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | Ratify Q-SCORE-1 forward Lane:/Closed: fields | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | Q-TXG-1 Blocks 2–3 election freeze + sibling-swap ports | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | Q-TXG-1 Block 1 freeze + compile | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | Land: Guardian-MGC MGC_M15 BAR EXPORT pin | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | Q-SCORE-1 Block 1 H_A FALSIFIED (freeze + retro-map) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | Harden roll_sessions against same-day label collisions | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | Prep: Guardian-MGC bar-derived N-SURV re-run (scoping only) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Decision: Guardian→MGC cell PREREG + DEAD(N-SURV) closure | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Decision/Measurement: Guardian→MGC (R7) port + F5 fix + b8 ratification | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Governance prose control-character gate | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Q-TXG-1 Block-1 implementation plan (authored, not executed) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Hygiene: clear closure-disposition coverage backlog (9 → 0) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Q-SCORE-1 Block-1 implementation plan (freeze + retro-map) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Q-SCORE-1 approach-scoreboard design (derived lane ledger) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Q-TXG-1 transfer/expression grid design (ratified) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Hygiene: Guardian-MGC (R7) pursuit backfill (PROPOSED PARK) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | N-SURV candidate-P&L channel (P2) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Sentinel: weekly activity-decision status at session start | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | MCL ledger: repair stale "1m cache exists" claim | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Code DRY remainder (C5 + SWEEP) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | `Q-MCLTAS-1` scoped then closed `FALSIFIED` — probe never run | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Rule-7 DRY + Option B code DRY (slices 1–3 + code) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Block 1 intake screening re-run: MCL TAS re-open → still `SHAPE-UNSCREENABLE` | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | task-routing skill (local vs cloud) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Archive `usoil_regime_capture` (GSUB-1 residual) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Q-TNEC-CON-5 ITERATE packet (lean A STOP) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Q-TNEC-ENV-1 closed `NULL` (Phase B census 0 SEED-GRADE, STOP) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Q-TNEC-CON-5 explore GO → AMBIGUOUS-HOLD (ITERATE) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Q-TNEC-CON-5 G0 freeze (pullback-VWAP-reclaim; explore unpaid) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | CON-4 Branch B elected → CON-5 non-breakout design owed | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Q-TNEC-CON-4 ITERATE packet (lean A STOP) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Q-TNEC-CON-4 explore GO → AMBIGUOUS-HOLD (ITERATE) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Q-TNEC-ENV-1 Phase A compile → H_A NON-EMPTY (Phase B authorized) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | Q-TNEC-CON-4 G0 freeze (PDH/PDL break; explore unpaid) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | CON-3 Branch B elected → CON-4 design owed | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | Q-TNEC-CON-3 ITERATE packet (election A/B unpaid) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | Q-TNEC-CON-3 explore GO → AMBIGUOUS-HOLD (ITERATE) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | Q-TNEC-CON-3 G0 freeze (HTF-native 5m; explore unpaid) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | Cell #3 reformulated framing falsifier: EVT-1 `KILL` — both drafted framings ... | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | Master-Pattern-shaped HTF-bias cell killed at cheap falsifier ($0 / no Q-ID) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | R8 gold-fix δ-extraction → SCREEN-FAIL (informed-flow + cost-law) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | Block 1 intake screening on MCL → INTAKE-DRY; L2 sourcing re-stages gold-fix ... | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | refine-question skill (select-box question refinement) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | Lab-path relocation repair + relocation-rot gate | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | GRAND pursuit-records checker (WARN-tier) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | Skill-ref warn triage (checker + citations) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | Gate 14 coverage limb (missing-closure blind spot) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | Missing closures authored + stale Q-roster Open rows cleared | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | W1 class_s intraday both-halves MEASURED | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | Notion Phase 3 cold archival (retirement ADR addendum) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-09 | Four discernment calls made (SNAG · checker-canon · Survive · idle-clock) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-09 | GRAND ratified + GSUB-1 CLOSED `RESOLVED-LOADBEARING` (all 4 phases) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-09 | Repo-truth sync + host-verified arm status (Hygiene) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-09 | Q-TNEC-CON-2 G0 freeze (compression→expansion; explore unpaid) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-09 | Instrument lane survey RESOLVED (MCL/MES/MGC) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-09 | GRAND-tier ADR + GSUB-1 instantiated (`Proposed`; ratification pending) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-09 | Harden M1 arm interlock (validate, not status-only) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-09 | CON-1 explore GO → FALSIFIED (STOP) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-09 | CON-1 ES/NQ ENTRY freeze + explore harness wire | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-08 | PR693 TNEC parallel integrate (G + Cap + Con) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-08 | TNEC-1 necessity retarget ratified (Phase G) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-08 | Absolute path 1–2–3 (MNQSEL-2 / CapRES / construct) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-08 | Q-R2FLOW-1 explore GO → G2 FALSIFIED (STOP) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-08 | Q-R2AGRUN-1 non-promotable STOP + Q-R2FLOW-1 G0 | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-08 | Q-R2AGRUN-1 explore GO → G2 AMBIGUOUS-HOLD (ITERATE) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-08 | Q-R2AGRUN-1 G0 freeze (MNQDTL R2 next causal set) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-08 | Delete-phase gap audit (conventions friction, Measurement) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-08 | Q-R2VBUCK-1 explore GO ratified → G2 FALSIFIED (STOP) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-08 | Fix roll_sessions reorder stranding same-day entries | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-08 | ADR ceremony stakes-tiering RATIFIED (governance friction audit) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-08 | Q-R2VBUCK-1 G0 freeze (MNQDTL R2 Phase-0) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-08 | S2b Accept → build ADR → build GO → daemon land | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-07 | MNQDTL-1 §8 RATIFIED + S1 ledger hygiene (full package) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-07 | S2 signal-host fork Accepted + S2b daemon spec (docs only) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-07 | Closed-loop spec series S1–S7 (PROPOSED) + minimal-spec style ratified + blas... | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-07 | Q-MNQSEL-1 Phase-0 RUN → FALSIFIED (C2); STOP | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-07 | Q-MNQSEL-1 Phase-0 PREREG (selection-value ceiling; docs only) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-07 | Q-OFCHAN-1 G2 Stage-G → VOID-COVERAGE (STOP) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-07 | MNQDTL-1 amend: elect D2 L=$325 max loss (variant b) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
<!-- ARCHIVE-INDEX:END -->
