# MECHANISMS — candidate mechanism vocabulary

**Purpose:** the controlled vocabulary the `PROFILE` blocks in `ops/instruments/<SYM>.md` bind to,
plus the CLASS-level findings that belong to a mechanism rather than to any one instrument.

**Growth rule:** a candidate declares its nearest existing class, or explicitly declares `NEW`.
`NEW` is permitted — it lands here in the SAME COMMIT as the pre-registration that introduced it.
An id that never reaches this file fails the P2 gate with a nearest-match suggestion.

## opening-range-continuation

Entering in the direction of an opening-range break and holding the position for continuation past the initial move.

- **Class finding:** Session-aware continuation on MYM failed on seven independent grounds at once (D2–D8, N=403) — placebo p=0.2144, gross/cost ratio 0.693 against a 4.00 bar, net −0.0210R. D3 is arithmetically unrescuable by sizing (gross/cost reduces to 0.655; contracts and stop-width cancel out). [MYM.md M2/M3](MYM.md)

## opening-range-breakout

Trading the break of a session opening range in the direction of the break.

- **Class finding:** Equity-index-specific — ZB *fades* its opening range; the within-day placebo returned p=0.0010, sign-reversed. Do not transplant to a risk-off instrument. [ZB.md B1](ZB.md)

## intraday-momentum

A next-bar or intraday continuation signal keyed to the prior bar's or prior session's directional momentum (Baltussen-class).

- **Class finding:** Baltussen-class intraday momentum is statistically ABSENT on modern MNQ — the cost-geometry thesis was real (hurdle fell 11.06→3.01 bp) but the OOS edge decayed negative (gross Sharpe +0.88→−0.13), corroborating the published post-2021 decay and an external 14-signal-family falsification (arXiv 2605.04004). [NQ.md N3](NQ.md)

## opening-pressure

Opening-session volume or range interpreted as directional pressure predicting the remainder of the session.

- **Class finding:** Opening-volume × directional-efficiency (OPENPRESS-1) is FALSIFIED on the MYM limb — wrong-signed plus cost-law FAIL, with no threshold/window/instrument rescue licensed. [MYM.md](MYM.md)

## event-window-reversal

A directional bet keyed to a scheduled settlement, auction, or macro-release window (settlement / auction / macro-release limbs).

- **Class finding:** The settlement limb does not reproduce at useful magnitude — MYM's third-Friday derivative-settlement reversal cleared exact-coverage sourcing (84/87, 96.6% PASS) but both power legs sit below the 0.2139 floor and the tradable limb is negative in 2024–2026. [MYM.md M5](MYM.md)
- **Class finding:** *Auction limb (2026-07-27) — dies at the PROCUREMENT GATE, not on edge, on ANY instrument.* Closing-auction/MOC-imbalance is reject-at-bar for an instrument-independent reason, hence recorded as a class finding rather than a cell. It is **not** killed by the free-data classification (the signal is exchange-licensed, unlike LETF EOD rebalance whose signal is public-AUM-derivable) nor by the a4 category prior (a published **signed** imbalance is not participant-category splitting) — those non-kills are stated so a future session does not borrow the wrong one. What binds: free-data route 1 requires **demonstrating** a vol-orthogonal, within-era-robust edge (F1 had no δ at all — unclaimed, not cleared); the order-flow modality is parenthesised to the standing *"don't buy explanatory data before a survivor justifies it"* rule (Avenue-A qualifying triple unmet; *scoped-not-procured*); and harvest Req 2 independently renders it UNSCREENABLE with the δ-extraction probe route **circular** (it needs the gated data). Cheapest re-open is free: a published cohort δ for imbalance → index-futures response, citable without procurement. [F1 ruling](../../docs/briefs/2026-07-27-f1-moc-imbalance-mym-ruling.md)

## turn-of-month

A calendar-timed return premium around the turn of the month, from institutional month-end cash flows reinvested at the turn.

- **Class finding:** No tradeable turn-of-month premium on SPX500's canonical Pepperstone feed (2017–2026, n=113 turns) — the existence battery is hard-absent (Welch t=0.64, label-perm p=0.25), the effect is entirely COVID-concentrated, and the halves sign-reverse. [SPX500.md F5](SPX500.md)

## trend-following

Riding an established directional move rather than fading it or timing its start (regime-capture / breakout-and-hold constructs).

- **Class finding:** USOIL's regime-capture trend leg (breakout / long-short / vol-target / trailing) passes every non-multiplicity gate (broad, fat-tail-robust, plateau-stable) but fails honest-N multiplicity correction on two independent gates (B-1 PBO 0.655, B-3 DSR p=0.215) — best-of-36 is selection noise, not edge. [USOIL.md](USOIL.md)

## naive-direction-mirror

Flipping an existing signal's or strategy's direction (long↔short) without redesigning entry/exit for the new direction.

- **Class finding:** The naive Guardian-inverse on XAUUSD (flip the locked long-only trend-rider's own entries/exits to short) is DEAD — mean −2.09R/trade full panel (~−3.4R recent); inverting a profitable trend-rider loses by construction and needs its own compression-gated timing, not a mirror. [XAUUSD.md D1](XAUUSD.md)

## compression-gated-breakout

Gating a breakout entry on a prior volatility-compression phase resolving into expansion.

- **Class finding:** A compression-gated short-primary construct on XAUUSD is not killed by the cheap tests, but the intended trailing-short payoff is 100% in the censored region (0/203 trades reach short FE≥1.5R) — a design-test mismatch that blocked a build decision pending a bar-level backtest. [XAUUSD.md F4](XAUUSD.md)
- **Class finding:** Dense-1m MNQ compression→expansion with-break at G=10 session-flat (`Q-TNEC-CON-2`) is gross-positive (~+0.9–1.0 pt) but net-negative under Tradeify RT 1.41 (`AMBIGUOUS-HOLD` non-promotable). An HTF-5m-bias → LTF-1m directed with-break filter on the same family is `FALSIFIED` at the parent cheap falsifier (both arms CI entirely &lt;0). [MNQ.md](MNQ.md)

## daily-range-state-persistence

**NEW 2026-08-18.** Conditioner-role, not entry-role: does a day's True Range being in the
trailing top quintile predict elevated next-day True Range (vs its own trailing median)?
Distinct from `compression-gated-breakout` / `htf-compression-breakout-5m` (both entry-role
compression→expansion triggers on MNQ) — this class makes no entry claim, only a
range-state-forecasting claim, and is scoped to the non-index triad
([Step-0 daily-geometry slate](../../docs/briefs/2026-08-18-step0-daily-geometry-mechanism-slate.md)
§2 row S1). Grounding: evidence-robustness (volatility clustering — ARCH/GARCH canon), not a
per-instrument WHO claim.

**Measurement history:** the class's first battery (block-shuffle placebo) was invalidated
2026-08-18 — it did not control True-Range autocorrelation
([audit note](../../docs/notes/audits/2026-08-18-block-shuffle-placebo-does-not-control-for-tr-autocorrelation.md)).
The **corrected class battery** (IAAFT normal-scores null; presence-gates/attribution-types
wiring; NEW L4 by-year regime limb) is the standing test —
[frozen spec + ADDENDUM-1](../../docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md).
Both class findings below are OFFICIAL under it (2026-08-18, operator PROCEED).

- **Class finding (corrected battery, OFFICIAL):** GC (parent, train era 2010–2019)
  top-quintile TR → elevated next-day TR: **NULL (driving L2 + L4)** — obs 0.5299 at the
  **8.4th percentile** of GC's own linear-ACF surrogate band (the earlier "near-miss" framing
  is retracted: the rate sat below the zero-mechanism benchmark's center); by-year 5/9 > 0.50
  vs required 7. Ledger cell `DEAD` (re-proposal bar: the corrected battery + a different
  construction or longer panel). [MGC.md G4](MGC.md) ·
  [`RESULTS_S1A.md`](../../lab/analysis/_inbox/rangestate_gc_2026-08/RESULTS_S1A.md) §6
- **Class finding (corrected battery, OFFICIAL):** CL (parent, train era 2010–2019)
  top-quintile TR → elevated next-day TR: **SIGNAL-GENERIC** — presence passes (CI lb 0.5651;
  halves; L4 boundary-exact 6/8 under the rule's own n_cond<20 exclusion, a disclosed
  prediction-miss adjudicated rules-govern); attribution GENERIC (obs at the 69th percentile
  of its own linear-ACF band, p_upper 0.3107) — **canon-attributed volatility clustering,
  SURVIVAL-ONLY durability. NOT a mechanism; does NOT discharge MCL's mechanism-owed status;
  NOT a conditioner license** (ADDENDUM-1 A6 rails travel with any quote; the crisis>calm
  per-year ordering and drop-cluster diagnostic are mandatory co-quotes). **Conditioner-engineering
  branch PARKED** — [`Q-CONDVAL-1`](../../docs/briefs/closures/Q-CONDVAL-1-closure-falsified.md)
  `FALSIFIED` 2026-08-18 (committed C−U 0.130 < frozen `L_star` 0.423 at the N-EDGE cell; O2
  discharged). Finding stands. [MCL.md C4/C5/C6](MCL.md) ·
  [`RESULTS_S1B.md`](../../lab/analysis/_inbox/rangestate_mcl_2026-08/RESULTS_S1B.md) §5

## htf-compression-breakout-5m

**NEW 2026-08-10.** Trade the **5m** compression→expansion break itself (not an HTF bias filter on 1m scalps): structural stop at the opposite quiet extreme; first valid signal per RTH session only (temporal selectivity under [`ADR 2026-08-10`](../../docs/adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md)); session-flat; Tradeify RT. Distinct from `compression-gated-breakout` dense-1m / fixed-G cells.

- **Class finding:** MNQ HTF-native 5m with-break (`Q-TNEC-CON-3`) explore → `AMBIGUOUS-HOLD` — long +0.073R with CI straddling 0; short −0.026R; not FALSIFIED; not live-pass; CONFIRM unread. [MNQ.md](MNQ.md) · [`RESULTS`](../../lab/analysis/c1/mnq_tnec_con3_htf_native_break_2026-08/RESULTS.md)

## pdh-pdl-breakout-rth

**NEW 2026-08-10.** First RTH close beyond prior-RTH high (long) or low (short) → enter next 1m open; structural stop at the opposite prior extreme; first valid signal per session; session-flat; Tradeify RT. Through-break continuation — distinct from compression-break (CON-2/3), ORB, MNQPROX OF-approach contrast, and N9/C10 level-touch attraction/fade.

- **Class finding:** MNQ PDH/PDL with-break (`Q-TNEC-CON-4`) explore → `AMBIGUOUS-HOLD` — long −0.007R / short +0.005R; CIs straddle; stop ≈257 pt; gross/(4×RT) ≈0.27×; not FALSIFIED; not live-pass; CONFIRM unread. [MNQ.md](MNQ.md) · [`RESULTS`](../../lab/analysis/c1/mnq_tnec_con4_pdh_pdl_break_2026-08/RESULTS.md)

## impulse-pullback-vwap-reclaim

**NEW 2026-08-11.** First-30m RTH bias (close@09:59 vs open@09:30) → after 10:00 require close on the bias side of session typical-price VWAP → pullback tag → reclaim close back through VWAP with bias → enter next 1m open; structural stop at the pullback extreme (tag→reclaim); first valid signal per session; session-flat; Tradeify RT. Continuation-on-retest — distinct from through-break (CON-1–4), compression, fade-to-VWAP, and ORB.

- **Class finding:** MNQ impulse→pullback→VWAP-reclaim (`Q-TNEC-CON-5`) explore → `AMBIGUOUS-HOLD` — long −0.184R / short −0.360R; CIs straddle; stop ≈17.5 pt; gross/(4×RT) ≈0.11×; not FALSIFIED; not live-pass; CONFIRM unread. [MNQ.md](MNQ.md) · [`RESULTS`](../../lab/analysis/c1/mnq_tnec_con5_impulse_pullback_vwap_2026-08/RESULTS.md)

## regime-overlay

A deploy-vs-wait or sizing gate keyed to an inferred market regime state rather than to price action directly.

- **Class finding:** Gold's KER/TSMOM trend-persistence regime-gate (`KER_126 ≥ 0.12` AND `TSMOM_252 > 0`) is FALSIFIED — its in-sample separation was an n≈2-regime-block artifact and the OOS falsifiers invert (DEPLOY +0.004R vs WAIT +0.284R). [XAUUSD.md D2](XAUUSD.md)

## band-pierce-continuation

Entering in the direction of a statistical band pierce (e.g. an NY-morning σ-threshold) that shows follow-through.

- **Class finding:** Raw band pierces carry no directional edge — post-pierce excursions are symmetric at 1.9σ lower-band NY-morning pierces on USDCAD; only the impulse-confirmed cohort (~27%) follows through, which is what BPC-001 conditions on. [USDCAD.md](USDCAD.md)

## ict-liquidity

ICT-style liquidity-sweep / fair-value-gap geometry (sweep → FVG → opposing-pool draw) used as an entry signal.

- **Class finding:** Sweep→same-direction-FVG→opposing-pool-draw direction is real on SPX500 (block-permutation p=0.0144) but fails robustness (drop-top-3 = −0.152R, 95% block-CI straddles 0). [SPX500.md D2](SPX500.md)
- **Class finding — CORRECTED 2026-08-04; supersedes the former "the 1M 0%-fill wall is feed-general" clause, which is REFUTED.** The archived closure attributed US500's **0 fills in 247 attempts** to an instrument-general *price law* — "displacement FVGs continue rather than retrace within 6 bars" — and predicted recurrence on "NAS100 or any fast 1m index". **That law is false on native micro data.** MNQ retraces to FVG mid within the frozen `retraceK=6` **59.06%** of the time (n=128,089; 58–60% in *every* year 2019–2026, including the 2020 crash and 2022 bear), and ES **59.88%** (n=124,748). Every escape route is refuted at 45×+ the ≤1.2% rate that 0-of-247 requires: raid-conditioning leaves it at **59.01%**, the arm-delay curve is nearly flat (**55.91%** even armed 8 bars late — mid-touches recur, they are not one-shot), and ES retraced **62.33%** in the *exact* 2026-06-24→26 window that produced the 0/247. **0/247 was platform-side by elimination** — the deployed (now lost) script, TV's strategy-tester fill handling, or the retired Pepperstone US500 CFD feed; not further separable, and recorded as a residual, never as "bug X". **Consequence for this class:** do **not** cite "1m FVGs don't retrace" against an execution layer on any instrument; **do** require any such design to demonstrate fills on native data rather than trusting TV-tester fill behavior. [MNQ.md W3](MNQ.md) · [`RESULTS_1M_DIAG.md`](../../lab/analysis/_inbox/ict_mnq_2026-08/RESULTS_1M_DIAG.md)
- **Class finding:** **Liquidity pools are anti-attractors**, replicated on three independent instruments — old highs/lows are swept far *less* often than a radius-matched MC null, on every side measured (US500 0.55/0.34 vs base 0.76/0.61; NQ 0.5401/0.3128 vs 0.7756/0.6014; MNQ 0.5303/0.3397 vs 0.8020/0.6502). Any construct keying on "price is drawn to old highs/lows" argues against three panels. The companion **bear-FVG draw** is the real positive of this class (NQ 0.8630 vs base 0.7494, RESOLVED). [MNQ.md N9](MNQ.md) · [`RESULTS.md`](../../lab/analysis/_inbox/ict_mnq_2026-08/RESULTS.md) §3

## order-flow-depth-imbalance

**NEW 2026-08-05.** Resting displayed size, aggregated across book levels, used as a directional
predictor of near-term price. The first mechanism class in this estate sourced from **order-flow
(MBP-10) data rather than OHLCV** — the "different modality" limb of the 2026-07-21
index-futures-intraday domain bar (route 2).

> ⚖ **RULED 2026-08-05 — scope pinned.** `MNQFLOW-1` ran the **blind** pre-registration and was
> ruled **inadmissible** as a gate-cleared discovery (recorded deviation; Avenue A §6 unmodified).
> Consequently the predictability finding below is a **quarantined measurement** — cite it as "one
> blind probe, three sessions, clean null", never as a settled class kill, and never to foreclose
> the sanctioned survivor-tied thread (`mnq_orb_flow_substrate_2026-08-05`). The **depth census
> stands unconditionally** (selection-free, descriptive) and is mandatory disclosed context for any
> size-derived successor. [`ruling §7`](../../docs/notes/2026-08-05-order-flow-probe-governance-question.md)

- **Class finding:** 10-level size imbalance carries **no** directional information at the
  1-minute horizon on NQ. Spearman ρ(I_t, r_{t+1}) = **−0.01205** on n=1,167 RTH minute pairs —
  wrong-signed against the predicted positive, and at the **36.7th percentile** of a within-day
  shuffled null (p_emp 0.633). [MNQ.md](MNQ.md) · [`RESULTS.md`](../../lab/archive/mnq_orderflow_probe_2026-08-04/RESULTS.md)
- **Class finding — the depth census is the reusable constraint.** NQ front-month displays a
  **median 67 contracts across all twenty price levels** (p05 40 / p95 94), ≈3.4 per level, so any
  ratio built from displayed size is coarse by construction: 525 distinct values in 1,167
  observations, **78.1% inside a tie group**, 5.8% exactly zero. **Any future size-derived book
  feature on this instrument family must argue against that census first** — the constraint is how
  little book there is to observe, not the estimator. [MNQ.md](MNQ.md)
- **Scope, load-bearing:** measured on **NQ parent** depth under proxy-discipline Rule 4 —
  structural discovery only; no MNQ tick value, cost, or fill assumption is derivable from it. One
  feature at one horizon over three sessions does **not** close the order-flow modality; it closes
  that modality's cheapest swing.

## index-dispersion

Trading the spread between index-level and single-name volatility or correlation rather than index direction.

- **Class finding:** Index dispersion / correlation-risk-premium as a 5th book leg was killed pre-build at the venue falsifier — futures-prop firms are options-free and Cboe DSPX has no listed tradable derivative. [SPX500.md D4](SPX500.md)

## venue-transfer

Porting a locked strategy to a different venue or contract without re-deriving parameters.

- **Class finding:** Structural venue costs, not signal decay, are the usual killer — DJ30 to MYM returned an OOS PF ratio of 0.559 against a 0.8x gate. [YM.md Y3](YM.md)

## mean-reversion-fade

Fading an overextended move back toward a reference level rather than following it.

- **Class finding:** A short-only mean-reversion spike-fader on USOIL is DEAD on the canonical feed — gross AND net E[R] negative at every target cell, placebo p=0.718, thirds all negative; a sub-ATR confirmation stop is infeasible on cost-geometry grounds. [USOIL.md D3](USOIL.md)

## day-of-week-selection-gate

A calendar / day-of-week (or adjacent session / hour-block) selection gate that admits or blocks trades by clock time rather than by price action.

- **Class finding:** A post-hoc Friday-only cut on the NAS100 ORB is DEAD — wide-family best-of-K fails (fw-p 0.0996 over a 24-cut eyeballed family; Friday rank 2/24), the OPEX-flow mechanism is falsified, and the thin 2025–26 tail fails. Orthogonality/era pass does not rescue a cut inside the selection envelope. [NAS100.md N10](NAS100.md)

## commodity-carry-term-structure

A directional bet keyed to commodity futures curve state (contango / backwardation) or roll-yield / carry rather than to spot price action.

- **Class finding:** Curve-state conditioning on USOIL does not separate forward returns from contango (5d gap −0.024R, Welch p=0.74) — a disguised long-oil trend trade, F1-FALSIFIED. [USOIL.md D2](USOIL.md)

## london-range-failed-extension-fade

**NEW 2026-08-12 (MSL-C2).** Fade a failed extension of the London-session high/low (formed before COMEX RTH) into the COMEX open: reclaim after a break that does not follow through; structural stop beyond the swept London extreme; truncated-loss exit; session-flat; first valid signal per session. Session-structure displacement — **not** a scheduled auction/fix window.

- **Class finding:** MGC explore IS **FALSIFIED 2026-08-13** — both arms mean ≈ −0.18R, CI entirely &lt; 0 (long n=327 CI [−0.287, −0.071]; short n=310 CI [−0.292, −0.075]); DELETE FAIL. CONFIRM unread. [closure](../../docs/briefs/closures/MSL-C2-closure-falsified.md) · [RESULTS](../../lab/archive/msl_c2_mgc_2026-08/RESULTS_g2.md)

Rejected nearest classes (one-line):
- `event-window-reversal` — R8/LBMA-fix family; this is session-structure, not a scheduled auction.
- `venue-transfer` / `trend-following` — Guardian→MGC transfer is DEAD(N-SURV); this is not a port.
- `pdh-pdl-breakout-rth` / `opening-range-continuation` — through-break continuation; opposite direction / different reference.
- `mean-reversion-fade` — nearest generic MR (USOIL spike-fader class finding); distinct constraint (London-range *failure* selects the trade).

## pdh-pdl-failed-break-reclaim

**NEW 2026-08-13 (MSL-C3).** Fade a **failed** break of prior-day RTH high/low (PDH/PDL): reclaim after a sweep that does not follow through; structural stop beyond the swept extreme; truncated-loss exit; session-flat by 16:00 ET; k=1 first valid signal per session. Mean-reversion-at-a-level (route ①) — **not** through-break continuation.

- **Class finding:** MYM explore **FALSIFIED** (both-arms CI &lt; 0) — [C1 RESULTS](../../lab/archive/msl_c1_mym_2026-08/RESULTS_g2.md) · [closure](../../docs/briefs/closures/MSL-C1-closure-falsified.md). M2K unpaid path [OPERATOR-KILL](../../docs/briefs/closures/MSL-C3-closure-operator-kill.md) (B4 declined; class not killed at C3). **M2K dual-axis explore FALSIFIED 2026-08-13** (Axis A both-arms IS 95% CI entirely &lt; 0; long n=293 CI [−0.256, −0.038]; short n=295 CI [−0.307, −0.089]; pooled −0.171R) — [closure](../../docs/briefs/closures/MSL-C3-K2-closure-falsified.md) · [RESULTS](../../lab/archive/msl_c3_m2k_2026-08/RESULTS_g2.md). Does not clear or reopen the MYM explore kill.

Rejected nearest classes (one-line):
- `pdh-pdl-breakout-rth` — through-break continuation (CON-4); opposite selector.
- `opening-range-continuation` / `opening-pressure` — OR continuation/pressure; dead on MYM.
- `ict-liquidity` — SLR-MYM-1 home; ICT weekly-gated first-30m sweep — different framing; Stage-0 FALSIFIED as scoped.
- `london-range-failed-extension-fade` — C2 MGC London/COMEX; FALSIFIED explore.
- `overnight-range-failed-extension-fade` — Globex overnight H/L failure fade; distinct reference class (co-scored with this class only under C3 K=2 revive).
- `mean-reversion-fade` — generic USOIL spike-fader; no PDH/PDL failure constraint.

## overnight-range-failed-extension-fade

**NEW 2026-08-13 (MSL-C3 K2 revive).** Fade a **failed** extension of the Globex **overnight** high/low into the RTH probe window: reclaim after a break that does not follow through; structural stop beyond the swept overnight extreme; truncated-loss exit; session-flat by 16:00 ET; k=1 first valid signal per session. Mean-reversion-at-a-level (route ①) — **not** PDH/PDL RTH prior-day, **not** London/COMEX (C2), **not** WSTRUCT weekly.

- **Class finding:** M2K explore **FALSIFIED 2026-08-13** (Axis B both-arms IS 95% CI entirely &lt; 0; long n=359 CI [−0.220, −0.021]; short n=378 CI [−0.204, −0.014]; pooled −0.114R). CONFIRM unread. [closure](../../docs/briefs/closures/MSL-C3-K2-closure-falsified.md) · [RESULTS](../../lab/archive/msl_c3_m2k_2026-08/RESULTS_g2.md).

Rejected nearest classes (one-line):
- `pdh-pdl-failed-break-reclaim` — prior-day **RTH** H/L; distinct clock/reference (sibling scored axis on C3 K2, not a substitute id).
- `london-range-failed-extension-fade` — C2 MGC London→COMEX; metals session structure; FALSIFIED explore.
- `pdh-pdl-breakout-rth` — through-break continuation; opposite selector.
- `opening-range-continuation` / `opening-pressure` — OR continuation/pressure; dead on MYM.
- `mean-reversion-fade` — generic USOIL spike-fader; no overnight-range failure constraint.
- WSTRUCT weekly-structure — SUPERSEDED-ON-COST; not this session-scale card.

## pullback-failure-resumption

**NEW 2026-08-13 (MSL-S2A).** Join an established **intraday** directional move after a pullback fails to reverse it — continuation entry on the resumption bar; hard stop beyond the pullback extreme; target at `rr` ∈ [2, 3] of that stop; session-flat; k=1 first valid signal per session. One trigger class: *pullback-failure resumption*. Not breakout-from-range, not compression-expansion, not MR-at-level.

- **Class finding:** MCL explore **FALSIFIED** (N-ACT 0.511 trades/week; long FLIP FAIL) — [S2A RESULTS](../../lab/archive/msl_s2a_mcl_2026-08/RESULTS_g2.md) · [closure](../../docs/briefs/closures/MSL-S2A-closure-falsified.md). CONFIRM unread.

Rejected nearest classes (one-line):
- `opening-range-continuation` / `opening-pressure` — OR break/pressure continuation; dead on MYM; different reference.
- `pdh-pdl-breakout-rth` — through-break of prior-day extreme; not pullback-failure on an established move.
- `impulse-pullback-vwap-reclaim` — CON-5 VWAP reclaim (paused dense-1m lane); different selector.
- `compression-gated-breakout` / `htf-compression-breakout-5m` — compression→expansion; second trigger class, not licensed.
- `trend-following` — USOIL regime-capture / breakout-and-hold; no pullback-failure constraint; CFD-era.
- `band-pierce-continuation` — σ-band pierce follow-through; different trigger.
- `mean-reversion-fade` — USOIL spike-fader; opposite direction.
- `event-window-reversal` / `Q-MCLTAS-1` — TAS/settlement; different modality.
- `london-range-failed-extension-fade` / `pdh-pdl-failed-break-reclaim` — slate-1 MR-at-level fades; opposite family.

## tod-baseline-range-trigger

**NEW 2026-08-20 (`Q-TODVOL-1`).** Within-instrument temporal selectivity under
[`ADR 2026-08-10`](../../docs/adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md) §2-B —
first RTH bar, outside the opening-range window, whose range exceeds a frozen multiple of the
**same time-of-day slot's own trailing median range** (causal, `.shift(1)`); enter in that bar's
own close-vs-open direction; stop/target sized off the triggering bar's own range (not an
independent point count); session-flat; first valid signal per session (k=1). Causal story:
volatility clustering (ARCH/GARCH-class serial dependence in absolute returns) as a real-time,
per-moment information-arrival signal — distinct from a fixed clock window (ORB) or a reference
price level (PDH/PDL, VWAP). Runs on **native 15m RTH bars** — explicitly outside the paused
dense-1m/G=10 lane ([`DENSE1M-UNPAUSE closure`](../../docs/briefs/closures/DENSE1M-UNPAUSE-closure-resolved-u0-keep.md),
U0 KEEP stands) — so gated by the [`2026-08-16 CON-5-scope ADR`](../../docs/adr/2026-08-16-con5-timeframe-scope-cheap-falsifier-gate.md)
§2 D2 pre-G0 cheap falsifier before route ① counts as open for it.

Rejected nearest classes (one-line):
- `compression-gated-breakout` / `htf-compression-breakout-5m` — requires a *prior compression phase resolving into expansion*; this class has no compression precondition and can trigger on the very first eligible bar of a session if it alone clears the threshold.
- `intraday-momentum` (Baltussen-class) — fixed-lag prior-bar/prior-session momentum continuation, statistically ABSENT on modern MNQ (class finding above); this class conditions entry timing on a real-time volatility-threshold crossing, not a blanket prior-period-direction claim.
- `opening-range-breakout` / `opening-range-continuation` — fixed first-N-bars window (ORB-MNQ-1's own territory, explicitly excluded here); this class's trigger window is data-dependent and can fire at any point later in the session.
- `pdh-pdl-breakout-rth` / `pdh-pdl-failed-break-reclaim` / `impulse-pullback-vwap-reclaim` / `band-pierce-continuation` / `ict-liquidity` — all keyed to a fixed **reference price level**; this class is keyed to a **time-of-day-conditioned volatility baseline**, no price level involved.
- `opening-pressure` — opening-session volume/range only; this class's trigger can occur at any RTH slot, not just the open.

- **Class finding:** MNQ D2 pre-G0 falsifier `FAIL` — mean signed gross **+0.2546 pt** vs the
  generous **2.82 pt** pass bar (0.5× the 4×RT hurdle), n=975 signals, 54.26% session coverage.
  Not a close call — 9% of the required bar. Route ① stays open in principle
  ([`ADR 2026-08-10`](../../docs/adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md));
  this specific causal story (volatility-threshold entry, stop/target sized off the trigger bar's
  own range) does not supply a candidate through it. Re-proposal bar: a structurally different
  criterion, not a re-tuned θ/lookback/stop-target on this shape.
  [`FREEZE`](../../lab/archive/todvol_1_2026-08-20/FREEZE.md) ·
  [`RESULTS`](../../lab/archive/todvol_1_2026-08-20/RESULTS.md).

## sweep-failure-filtered-continuation

**NEW 2026-08-14 (MSL-S2B).** Trend-continuation entry on **MYM** **gated** by a PDH/PDL sweep-failure state — the sweep-failure is a **filter, never the entry**; hard stop; target at `rr` ∈ [2, 3]; session-flat by 16:00 ET; k=1 first valid signal per session. Consumes C1's DELETE-PASS selection evidence in **filter role** (entry-role construct remains dead). Not OR continuation; not PDH/PDL failed-break reclaim entry; not through-break.

- **Class finding:** Stage-1 **FAIL** (route) — index raised bar unbound for continuation *entry*; SLR route ① clears MR-at-level *filter* only; temporal-selectivity route blocked by Q-TNEC-CON-5 pause; composite clearance forbidden. [STAGE1](../../lab/analysis/c1/msl_s2b_mym_2026-08/STAGE1.md) · [closure](../../docs/briefs/closures/MSL-S2B-closure-stage1-fail-route.md). $0 / K=0; G0 never frozen.

Rejected nearest classes (one-line):
- `pdh-pdl-failed-break-reclaim` — C1 **entry-role** FALSIFIED on MYM; this id is filter-role gated continuation, not a silent reopen of that entry.
- `opening-range-continuation` / `opening-pressure` — OR break/pressure continuation; dead on MYM (seven gates); different reference.
- `pdh-pdl-breakout-rth` — through-break of prior-day extreme (CON-4); opposite selector to sweep-failure filter.
- `ict-liquidity` / SLR-MYM-1 — sweep-as-**entry**; Stage-0 FALSIFIED as scoped; filter role is a different `(mechanism, role)` pair.
- `pullback-failure-resumption` — S2A continuation without PDH/PDL sweep-failure gate; FALSIFIED N-ACT on MCL.
- `impulse-pullback-vwap-reclaim` — CON-5; paused dense-1m lane; different selector.
- `trend-following` / `band-pierce-continuation` — unconstrained or σ-band continuation; no sweep-failure filter.
- `mean-reversion-fade` — USOIL spike-fader **entry** bar; role-asymmetry does not auto-clear a continuation entry.

## expiry-oi-strike-convergence

**NEW 2026-08-21 (MSL-S4).** Discharges the 2026-08-14 WHO-track E1 stop rule
([closure](../../docs/briefs/closures/MSL-S7-closure-resolved-e1-hold.md)) — first WHO named
outside the 2026-08-10 INTAKE-DRY set and outside a transfer of C1/C2/C3/S2A/S2B. Near a
published options expiry, price statistically converges toward the strike carrying the largest
open interest more than on non-expiry control sessions; enter in the direction that closes the
gap between current price and that strike when price is displaced from it by more than a
threshold, inside a declared pre-expiry window. WHO: options market-makers who wrote the
concentrated open interest at that strike, mechanically obligated to keep a delta-neutral book
as time-to-expiry shrinks and near-the-money gamma rises (Γ ∝ 1/√T) — a hedging-requirements /
expiry-mechanics constraint (ADR clause-1-admissible), not a preference. The trade direction is
read directly off observable data (spot price vs. the published strike), never off an assumption
about unobservable dealer gamma sign — the load-bearing distinction from the sibling construct
below, which this class does **not** reopen.

- **Class finding:** none yet — G0 frozen on operator B4 GO 2026-08-21; Explore-confirm (charter
  step 5a) **deferred by explicit operator override** (no Databento/market-data access in the
  sourcing session's environment) rather than scored — Pine authored CC-solo directly off the
  frozen construct, with the operator's own TV backtest as the first empirical evidence instead
  of a pre-Pine Explore score. This is a disclosed deviation from the charter's default step
  ordering, not a silent skip. [`STAGE1`](../../lab/analysis/c1/msl_s4_mgc_2026-08/STAGE1.md) ·
  [`PREREG_G0`](../../lab/analysis/c1/msl_s4_mgc_2026-08/PREREG_G0.md) ·
  [`RUNBOOK`](../../lab/analysis/c1/msl_s4_mgc_2026-08/RUNBOOK.md).

Rejected nearest classes (one-line):
- **Directional dealer-gamma-sign forecast** (informal sibling construct, never declared an id —
  "assume dealers are net long/short gamma at a strike, predict trend-continuation or
  mean-reversion accordingly") — stays correctly **DEAD**, not reopened here: dealer sign at a
  specific strike/day is unobservable, so the trade direction is never entailed (same BE1
  "constraint carries neither sign nor level" failure that killed the FX 10:00 NY option cut and
  the `regime-overlay` NAS100 dealer-gamma gate below). This class's direction is read off
  price-vs-published-strike instead, which is always observable — the reason it survives where
  the sibling does not.
- `london-range-failed-extension-fade` / `pdh-pdl-failed-break-reclaim` /
  `overnight-range-failed-extension-fade` — nearest **generic** MR-at-level family (the sharpest
  honest adjacency: `london-range-failed-extension-fade` is **FALSIFIED on this exact instrument,
  MGC**). Distinct data-generating process: session price-action level (every session) vs.
  published options-positioning level (only near a listed expiry).
- `event-window-reversal` — scheduled release whose *direction* is itself uncertain a priori
  (symmetric information-shock framing); this construct's direction is deterministic given
  observable displacement, not an event-shock guess.
- `regime-overlay` (XAUUSD KER/TSMOM sizing gate; NAS100 dealer-gamma-regime-gate) — a
  sizing/deploy gate on inferred regime state; this construct is an entry-role trigger, not a
  conditioning overlay.
