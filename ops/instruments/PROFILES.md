# INSTRUMENT PROFILES — mechanism x instrument verdict index

> **GENERATED — do not hand-edit; source = ledger PROFILE blocks.**
> Regenerate: `python scripts/instrument_profiles.py build`
> Source of record is always `ops/instruments/<SYM>.md`.


## Matrix

| Mechanism | 6J | BTCUSD | ES | EURGBP | EURUSD | GER40 | M2K | M6A | M6B | MCL | MES | MGC | MJY | MNQ | MYM | NAS100 | NG | NQ | SPX500 | USDCAD | USOIL | XAGUSD | XAUUSD | YM | ZB | ZF | ZN |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| band-pierce-continuation | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | F | . | . | . | . | . | . | . |
| commodity-carry-term-structure | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | D | . | . | . | . | . | . |
| compression-gated-breakout | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | A | . | . | . | . |
| daily-range-state-persistence | . | . | . | . | . | . | . | . | . | A | . | D | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . |
| day-of-week-selection-gate | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | D | . | . | . | . | . | . | . | . | . | . | . |
| event-window-reversal | . | . | . | . | D | . | . | . | . | . | . | D | . | . | D | . | D | . | . | . | . | . | . | . | . | . | D |
| htf-compression-breakout-5m | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . |
| ict-liquidity | . | . | . | . | . | . | . | . | . | . | . | . | . | D | D | . | . | . | D | . | . | . | . | . | . | . | . |
| impulse-pullback-vwap-reclaim | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . |
| index-dispersion | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | D | . | . | . | . | . | . | . | . |
| intraday-momentum | . | . | . | . | . | . | . | . | . | . | . | . | . | D | . | . | . | D | . | . | . | . | . | . | . | . | . |
| london-range-failed-extension-fade | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . |
| mean-reversion-fade | . | . | . | D | . | . | . | . | . | . | . | . | . | . | . | . | . | . | D | D | D | . | . | . | . | . | . |
| naive-direction-mirror | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | D | . | . | . | . | . | . | D | . | . | . | . |
| opening-pressure | . | . | . | . | . | . | . | . | . | . | . | . | . | D | D | . | . | D | . | . | . | . | . | . | . | . | . |
| opening-range-breakout | . | . | . | . | . | A | . | . | . | . | . | . | . | A | . | A | . | A | D | D | . | . | . | . | D | D | . |
| opening-range-continuation | . | . | . | . | . | . | . | . | . | . | . | . | . | . | D | . | . | . | . | . | . | . | . | . | . | . | . |
| order-flow-depth-imbalance | . | . | . | . | . | . | . | . | . | . | . | . | . | D | . | . | . | . | . | . | . | . | . | . | . | . | . |
| overnight-range-failed-extension-fade | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . |
| pdh-pdl-breakout-rth | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . |
| pdh-pdl-failed-break-reclaim | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . |
| pullback-failure-resumption | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . |
| regime-overlay | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | D | . | . | D | . | . | . | D | . | . | . | . |
| sweep-failure-filtered-continuation | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . |
| tod-baseline-range-trigger | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . |
| trend-following | . | D | . | . | . | . | . | . | . | . | . | . | . | . | L | L | . | . | . | D | A | D | L | . | . | . | . |
| turn-of-month | . | . | A | . | A | . | . | . | . | . | . | . | . | . | . | . | . | . | D | . | . | . | . | . | . | . | . |
| venue-transfer | A | . | . | . | . | . | . | . | . | . | . | . | D | . | D | . | . | . | . | . | . | . | . | D | . | . | . |

Legend: D=DEAD · A=AMBIGUOUS-PARKED · F=CONTINGENT-FORWARD · L=LIVE · `.`=untested


## band-pierce-continuation

Entering in the direction of a statistical band pierce (e.g. an NY-morning σ-threshold) that shows follow-through.

- **Class finding:** Raw band pierces carry no directional edge — post-pierce excursions are symmetric at 1.9σ lower-band NY-morning pierces on USDCAD; only the impulse-confirmed cohort (~27%) follows through, which is what BPC-001 conditions on. [USDCAD.md](USDCAD.md)

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| USDCAD | CONTINGENT-FORWARD | 2026-06-16 | ../../docs/ltm/briefs/pre-registration/FWD-PREREG-BPC-USDCAD-TUE-2026-06-11.md |


## commodity-carry-term-structure

A directional bet keyed to commodity futures curve state (contango / backwardation) or roll-yield / carry rather than to spot price action.

- **Class finding:** Curve-state conditioning on USOIL does not separate forward returns from contango (5d gap −0.024R, Welch p=0.74) — a disguised long-oil trend trade, F1-FALSIFIED. [USOIL.md D2](USOIL.md)

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| USOIL | DEAD | 2026-06-06 | ../../docs/rejected_candidates.md |


## compression-gated-breakout

Gating a breakout entry on a prior volatility-compression phase resolving into expansion.

- **Class finding:** A compression-gated short-primary construct on XAUUSD is not killed by the cheap tests, but the intended trailing-short payoff is 100% in the censored region (0/203 trades reach short FE≥1.5R) — a design-test mismatch that blocked a build decision pending a bar-level backtest. [XAUUSD.md F4](XAUUSD.md)

- **Class finding:** Dense-1m MNQ compression→expansion with-break at G=10 session-flat (`Q-TNEC-CON-2`) is gross-positive (~+0.9–1.0 pt) but net-negative under Tradeify RT 1.41 (`AMBIGUOUS-HOLD` non-promotable). An HTF-5m-bias → LTF-1m directed with-break filter on the same family is `FALSIFIED` at the parent cheap falsifier (both arms CI entirely &lt;0). [MNQ.md](MNQ.md)

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| XAUUSD | AMBIGUOUS-PARKED | 2026-06-15 | ../../lab/analysis/legacy/xauusd_cgb_2026-06-15/RESULTS.md |


## daily-range-state-persistence

**NEW 2026-08-18.** Conditioner-role, not entry-role: does a day's True Range being in the

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| MCL | AMBIGUOUS-PARKED | 2026-08-18 | ../../lab/analysis/_inbox/rangestate_mcl_2026-08/RESULTS_S1B.md |
| MGC | DEAD | 2026-08-18 | ../../lab/analysis/_inbox/rangestate_gc_2026-08/RESULTS_S1A.md |


## day-of-week-selection-gate

A calendar / day-of-week (or adjacent session / hour-block) selection gate that admits or blocks trades by clock time rather than by price action.

- **Class finding:** A post-hoc Friday-only cut on the NAS100 ORB is DEAD — wide-family best-of-K fails (fw-p 0.0996 over a 24-cut eyeballed family; Friday rank 2/24), the OPEX-flow mechanism is falsified, and the thin 2025–26 tail fails. Orthogonality/era pass does not rescue a cut inside the selection envelope. [NAS100.md N10](NAS100.md)

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| NAS100 | DEAD | 2026-06-27 | ../../docs/ltm/briefs/Q-ORB-FRIDAY-1-closure-falsified.md |


## event-window-reversal

A directional bet keyed to a scheduled settlement, auction, or macro-release window (settlement / auction / macro-release limbs).

- **Class finding:** The settlement limb does not reproduce at useful magnitude — MYM's third-Friday derivative-settlement reversal cleared exact-coverage sourcing (84/87, 96.6% PASS) but both power legs sit below the 0.2139 floor and the tradable limb is negative in 2024–2026. [MYM.md M5](MYM.md)

- **Class finding:** *Auction limb (2026-07-27) — dies at the PROCUREMENT GATE, not on edge, on ANY instrument.* Closing-auction/MOC-imbalance is reject-at-bar for an instrument-independent reason, hence recorded as a class finding rather than a cell. It is **not** killed by the free-data classification (the signal is exchange-licensed, unlike LETF EOD rebalance whose signal is public-AUM-derivable) nor by the a4 category prior (a published **signed** imbalance is not participant-category splitting) — those non-kills are stated so a future session does not borrow the wrong one. What binds: free-data route 1 requires **demonstrating** a vol-orthogonal, within-era-robust edge (F1 had no δ at all — unclaimed, not cleared); the order-flow modality is parenthesised to the standing *"don't buy explanatory data before a survivor justifies it"* rule (Avenue-A qualifying triple unmet; *scoped-not-procured*); and harvest Req 2 independently renders it UNSCREENABLE with the δ-extraction probe route **circular** (it needs the gated data). Cheapest re-open is free: a published cohort δ for imbalance → index-futures response, citable without procurement. [F1 ruling](../../docs/briefs/2026-07-27-f1-moc-imbalance-mym-ruling.md)

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| EURUSD | DEAD | 2026-06-22 | ../../docs/rejected_candidates.md |
| MGC | DEAD | 2026-08-10 | ../../lab/analysis/harvest/tnec_l2_sourcing_2026-08-10/DELTA_EXTRACTION_R8.md |
| MYM | DEAD | 2026-07-21 | ../../docs/briefs/closures/MYM-3FPS-1-closure-falsified.md |
| NG | DEAD | 2026-07-21 | ../../lab/archive/ng_eia_recon_2026-07/RESULTS.md |
| ZN | DEAD | 2026-07-20 | ../../docs/briefs/closures/H-ZNAUC-1-closure-screen-fail.md |


## htf-compression-breakout-5m

**NEW 2026-08-10.** Trade the **5m** compression→expansion break itself (not an HTF bias filter on 1m scalps): structural stop at the opposite quiet extreme; first valid signal per RTH session only (temporal selectivity under [`ADR 2026-08-10`](../../docs/adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md)); session-flat; Tradeify RT. Distinct from `compression-gated-breakout` dense-1m / fixed-G cells.

- **Class finding:** MNQ HTF-native 5m with-break (`Q-TNEC-CON-3`) explore → `AMBIGUOUS-HOLD` — long +0.073R with CI straddling 0; short −0.026R; not FALSIFIED; not live-pass; CONFIRM unread. [MNQ.md](MNQ.md) · [`RESULTS`](../../lab/analysis/c1/mnq_tnec_con3_htf_native_break_2026-08/RESULTS.md)

_No instrument has a recorded verdict on this mechanism._


## ict-liquidity

ICT-style liquidity-sweep / fair-value-gap geometry (sweep → FVG → opposing-pool draw) used as an entry signal.

- **Class finding:** Sweep→same-direction-FVG→opposing-pool-draw direction is real on SPX500 (block-permutation p=0.0144) but fails robustness (drop-top-3 = −0.152R, 95% block-CI straddles 0). [SPX500.md D2](SPX500.md)

- **Class finding:** **Liquidity pools are anti-attractors**, replicated on three independent instruments — old highs/lows are swept far *less* often than a radius-matched MC null, on every side measured (US500 0.55/0.34 vs base 0.76/0.61; NQ 0.5401/0.3128 vs 0.7756/0.6014; MNQ 0.5303/0.3397 vs 0.8020/0.6502). Any construct keying on "price is drawn to old highs/lows" argues against three panels. The companion **bear-FVG draw** is the real positive of this class (NQ 0.8630 vs base 0.7494, RESOLVED). [MNQ.md N9](MNQ.md) · [`RESULTS.md`](../../lab/analysis/_inbox/ict_mnq_2026-08/RESULTS.md) §3

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| MNQ | DEAD | 2026-08-04 | ../../lab/archive/mnq_fvg_draw_probe_2026-08-04/RESULTS.md |
| MYM | DEAD | 2026-07-29 | ../../docs/briefs/closures/SLR-MYM-1-closure-falsified-stage0.md |
| SPX500 | DEAD | 2026-06-17 | #D2 |


## impulse-pullback-vwap-reclaim

**NEW 2026-08-11.** First-30m RTH bias (close@09:59 vs open@09:30) → after 10:00 require close on the bias side of session typical-price VWAP → pullback tag → reclaim close back through VWAP with bias → enter next 1m open; structural stop at the pullback extreme (tag→reclaim); first valid signal per session; session-flat; Tradeify RT. Continuation-on-retest — distinct from through-break (CON-1–4), compression, fade-to-VWAP, and ORB.

- **Class finding:** MNQ impulse→pullback→VWAP-reclaim (`Q-TNEC-CON-5`) explore → `AMBIGUOUS-HOLD` — long −0.184R / short −0.360R; CIs straddle; stop ≈17.5 pt; gross/(4×RT) ≈0.11×; not FALSIFIED; not live-pass; CONFIRM unread. [MNQ.md](MNQ.md) · [`RESULTS`](../../lab/analysis/c1/mnq_tnec_con5_impulse_pullback_vwap_2026-08/RESULTS.md)

_No instrument has a recorded verdict on this mechanism._


## index-dispersion

Trading the spread between index-level and single-name volatility or correlation rather than index direction.

- **Class finding:** Index dispersion / correlation-risk-premium as a 5th book leg was killed pre-build at the venue falsifier — futures-prop firms are options-free and Cboe DSPX has no listed tradable derivative. [SPX500.md D4](SPX500.md)

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| SPX500 | DEAD | 2026-06-30 | #D4 |


## intraday-momentum

A next-bar or intraday continuation signal keyed to the prior bar's or prior session's directional momentum (Baltussen-class).

- **Class finding:** Baltussen-class intraday momentum is statistically ABSENT on modern MNQ — the cost-geometry thesis was real (hurdle fell 11.06→3.01 bp) but the OOS edge decayed negative (gross Sharpe +0.88→−0.13), corroborating the published post-2021 decay and an external 14-signal-family falsification (arXiv 2605.04004). [NQ.md N3](NQ.md)

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| MNQ | DEAD | 2026-07-21 | ../../docs/briefs/rnd-pipeline/D5-RECOST-1-mnq-native-cost-law-rescope-scoping.md |
| NQ | DEAD | 2026-07-21 | ../../docs/briefs/rnd-pipeline/D5-RECOST-1-mnq-native-cost-law-rescope-scoping.md |


## london-range-failed-extension-fade

**NEW 2026-08-12 (MSL-C2).** Fade a failed extension of the London-session high/low (formed before COMEX RTH) into the COMEX open: reclaim after a break that does not follow through; structural stop beyond the swept London extreme; truncated-loss exit; session-flat; first valid signal per session. Session-structure displacement — **not** a scheduled auction/fix window.

_No instrument has a recorded verdict on this mechanism._


## mean-reversion-fade

Fading an overextended move back toward a reference level rather than following it.

- **Class finding:** A short-only mean-reversion spike-fader on USOIL is DEAD on the canonical feed — gross AND net E[R] negative at every target cell, placebo p=0.718, thirds all negative; a sub-ATR confirmation stop is infeasible on cost-geometry grounds. [USOIL.md D3](USOIL.md)

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| EURGBP | DEAD | 2026-06-21 | #D1 |
| SPX500 | DEAD | 2026-06-07 | #D1 |
| USDCAD | DEAD | 2026-06-26 | ../../lab/archive/usdcad_fade_2026-06-26/RESULTS.md |
| USOIL | DEAD | 2026-06-14 | ../../docs/adr/2026-06-14-reject-usoil-rdm-spike-fader.md |


## naive-direction-mirror

Flipping an existing signal's or strategy's direction (long↔short) without redesigning entry/exit for the new direction.

- **Class finding:** The naive Guardian-inverse on XAUUSD (flip the locked long-only trend-rider's own entries/exits to short) is DEAD — mean −2.09R/trade full panel (~−3.4R recent); inverting a profitable trend-rider loses by construction and needs its own compression-gated timing, not a mirror. [XAUUSD.md D1](XAUUSD.md)

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| NAS100 | DEAD | 2026-05-05 | #N4 |
| XAUUSD | DEAD | 2026-06-15 | ../../lab/analysis/legacy/xauusd_cgb_2026-06-15/RESULTS.md |


## opening-pressure

Opening-session volume or range interpreted as directional pressure predicting the remainder of the session.

- **Class finding:** Opening-volume × directional-efficiency (OPENPRESS-1) is FALSIFIED on the MYM limb — wrong-signed plus cost-law FAIL, with no threshold/window/instrument rescue licensed. [MYM.md](MYM.md)

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| MNQ | DEAD | 2026-07-21 | ../../docs/briefs/closures/OPENPRESS-1-closure-falsified.md |
| MYM | DEAD | 2026-07-21 | ../../docs/briefs/closures/OPENPRESS-1-closure-falsified.md |
| NQ | DEAD | 2026-07-21 | ../../docs/briefs/closures/OPENPRESS-1-closure-falsified.md |


## opening-range-breakout

Trading the break of a session opening range in the direction of the break.

- **Class finding:** Equity-index-specific — ZB *fades* its opening range; the within-day placebo returned p=0.0010, sign-reversed. Do not transplant to a risk-off instrument. [ZB.md B1](ZB.md)

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| GER40 | AMBIGUOUS-PARKED | 2026-06-22 | #G2 |
| MNQ | AMBIGUOUS-PARKED | 2026-07-23 | ../../docs/briefs/2026-07-17-0808-packet-delta-and-sequence.md |
| NAS100 | AMBIGUOUS-PARKED | 2026-06-23 | #N7 |
| NQ | AMBIGUOUS-PARKED | 2026-07-23 | ../../docs/briefs/2026-07-17-0808-packet-delta-and-sequence.md |
| SPX500 | DEAD | 2026-06-22 | ../../lab/analysis/legacy/us500_discovery_2026-06-22/RESULTS.md |
| USDCAD | DEAD | 2026-06-14 | ../../lab/archive/usdcad_reverse_2026-06-14/RESULTS.md |
| ZB | DEAD | 2026-07-20 | ../../lab/archive/orb_zb_recon_2026-07/RESULTS.md |
| ZF | DEAD | 2026-07-21 | ../../lab/archive/rates_ev_zf_recon_2026-07/RESULTS.md |


## opening-range-continuation

Entering in the direction of an opening-range break and holding the position for continuation past the initial move.

- **Class finding:** Session-aware continuation on MYM failed on seven independent grounds at once (D2–D8, N=403) — placebo p=0.2144, gross/cost ratio 0.693 against a 4.00 bar, net −0.0210R. D3 is arithmetically unrescuable by sizing (gross/cost reduces to 0.655; contracts and stop-width cancel out). [MYM.md M2/M3](MYM.md)

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| MYM | DEAD | 2026-07-16 | ../../docs/briefs/closures/2026-07-16-striker-mym-reconstruction-candidate-2-falsified.md |


## order-flow-depth-imbalance

**NEW 2026-08-05.** Resting displayed size, aggregated across book levels, used as a directional

- **Class finding:** 10-level size imbalance carries **no** directional information at the

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| MNQ | DEAD | 2026-08-05 | ../../lab/archive/mnq_orderflow_probe_2026-08-04/RESULTS.md |


## overnight-range-failed-extension-fade

**NEW 2026-08-13 (MSL-C3 K2 revive).** Fade a **failed** extension of the Globex **overnight** high/low into the RTH probe window: reclaim after a break that does not follow through; structural stop beyond the swept overnight extreme; truncated-loss exit; session-flat by 16:00 ET; k=1 first valid signal per session. Mean-reversion-at-a-level (route ①) — **not** PDH/PDL RTH prior-day, **not** London/COMEX (C2), **not** WSTRUCT weekly.

- **Class finding:** none yet — held unread under original C3 ≤1-story license; now a **scored axis** under [`STAGE1_K2`](../../lab/archive/msl_c3_m2k_2026-08/STAGE1_K2.md) (`K_intrinsic=2`). B4 unpaid.

_No instrument has a recorded verdict on this mechanism._


## pdh-pdl-breakout-rth

**NEW 2026-08-10.** First RTH close beyond prior-RTH high (long) or low (short) → enter next 1m open; structural stop at the opposite prior extreme; first valid signal per session; session-flat; Tradeify RT. Through-break continuation — distinct from compression-break (CON-2/3), ORB, MNQPROX OF-approach contrast, and N9/C10 level-touch attraction/fade.

- **Class finding:** MNQ PDH/PDL with-break (`Q-TNEC-CON-4`) explore → `AMBIGUOUS-HOLD` — long −0.007R / short +0.005R; CIs straddle; stop ≈257 pt; gross/(4×RT) ≈0.27×; not FALSIFIED; not live-pass; CONFIRM unread. [MNQ.md](MNQ.md) · [`RESULTS`](../../lab/analysis/c1/mnq_tnec_con4_pdh_pdl_break_2026-08/RESULTS.md)

_No instrument has a recorded verdict on this mechanism._


## pdh-pdl-failed-break-reclaim

**NEW 2026-08-13 (MSL-C3).** Fade a **failed** break of prior-day RTH high/low (PDH/PDL): reclaim after a sweep that does not follow through; structural stop beyond the swept extreme; truncated-loss exit; session-flat by 16:00 ET; k=1 first valid signal per session. Mean-reversion-at-a-level (route ①) — **not** through-break continuation.

- **Class finding:** MYM explore **FALSIFIED** (both-arms CI &lt; 0) — [C1 RESULTS](../../lab/archive/msl_c1_mym_2026-08/RESULTS_g2.md) · [closure](../../docs/briefs/closures/MSL-C1-closure-falsified.md). M2K unpaid path [OPERATOR-KILL](../../docs/briefs/closures/MSL-C3-closure-operator-kill.md) (B4 declined; class not killed at C3). **Revive in flight:** M2K dual-axis Stage-1 at `K_intrinsic=2` — [`STAGE1_K2`](../../lab/archive/msl_c3_m2k_2026-08/STAGE1_K2.md) · [ADR](../../docs/adr/2026-08-13-msl-c3-k2-dual-axis-revive.md) — B4 unpaid; does not clear the MYM explore kill.

_No instrument has a recorded verdict on this mechanism._


## pullback-failure-resumption

**NEW 2026-08-13 (MSL-S2A).** Join an established **intraday** directional move after a pullback fails to reverse it — continuation entry on the resumption bar; hard stop beyond the pullback extreme; target at `rr` ∈ [2, 3] of that stop; session-flat; k=1 first valid signal per session. One trigger class: *pullback-failure resumption*. Not breakout-from-range, not compression-expansion, not MR-at-level.

- **Class finding:** MCL explore **FALSIFIED** (N-ACT 0.511 trades/week; long FLIP FAIL) — [S2A RESULTS](../../lab/archive/msl_s2a_mcl_2026-08/RESULTS_g2.md) · [closure](../../docs/briefs/closures/MSL-S2A-closure-falsified.md). CONFIRM unread.

_No instrument has a recorded verdict on this mechanism._


## regime-overlay

A deploy-vs-wait or sizing gate keyed to an inferred market regime state rather than to price action directly.

- **Class finding:** Gold's KER/TSMOM trend-persistence regime-gate (`KER_126 ≥ 0.12` AND `TSMOM_252 > 0`) is FALSIFIED — its in-sample separation was an n≈2-regime-block artifact and the OOS falsifiers invert (DEPLOY +0.004R vs WAIT +0.284R). [XAUUSD.md D2](XAUUSD.md)

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| NAS100 | DEAD | 2026-06-27 | ../../docs/ltm/briefs/Q-ORB-T10Y3M-1-closure-falsified.md |
| SPX500 | DEAD | 2026-06-20 | #D3 |
| XAUUSD | DEAD | 2026-07-01 | ../../docs/rejected_candidates.md |


## sweep-failure-filtered-continuation

**NEW 2026-08-14 (MSL-S2B).** Trend-continuation entry on **MYM** **gated** by a PDH/PDL sweep-failure state — the sweep-failure is a **filter, never the entry**; hard stop; target at `rr` ∈ [2, 3]; session-flat by 16:00 ET; k=1 first valid signal per session. Consumes C1's DELETE-PASS selection evidence in **filter role** (entry-role construct remains dead). Not OR continuation; not PDH/PDL failed-break reclaim entry; not through-break.

- **Class finding:** Stage-1 **FAIL** (route) — index raised bar unbound for continuation *entry*; SLR route ① clears MR-at-level *filter* only; temporal-selectivity route blocked by Q-TNEC-CON-5 pause; composite clearance forbidden. [STAGE1](../../lab/analysis/c1/msl_s2b_mym_2026-08/STAGE1.md) · [closure](../../docs/briefs/closures/MSL-S2B-closure-stage1-fail-route.md). $0 / K=0; G0 never frozen.

_No instrument has a recorded verdict on this mechanism._


## tod-baseline-range-trigger

**NEW 2026-08-20 (`Q-TODVOL-1`).** Within-instrument temporal selectivity under

- **Class finding:** none yet — D2 pre-G0 falsifier pending (this session).

_No instrument has a recorded verdict on this mechanism._


## trend-following

Riding an established directional move rather than fading it or timing its start (regime-capture / breakout-and-hold constructs).

- **Class finding:** USOIL's regime-capture trend leg (breakout / long-short / vol-target / trailing) passes every non-multiplicity gate (broad, fat-tail-robust, plateau-stable) but fails honest-N multiplicity correction on two independent gates (B-1 PBO 0.655, B-3 DSR p=0.215) — best-of-36 is selection noise, not edge. [USOIL.md](USOIL.md)

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| BTCUSD | DEAD | 2026-06-30 | ../../docs/ltm/briefs/Q-BTC-3-closure-falsified.md |
| MYM | LIVE | 2026-07-23 | ../../docs/briefs/2026-07-23-tradeify-book-composition.md |
| NAS100 | LIVE | 2026-05-05 | ../../core/strategies/_archive/nas/LOCK.md |
| USDCAD | DEAD | 2026-06-14 | ../../lab/archive/usdcad_reverse_2026-06-14/RESULTS.md |
| USOIL | AMBIGUOUS-PARKED | 2026-06-15 | #RGC-001 |
| XAGUSD | DEAD | 2026-07-01 | ../../docs/rejected_candidates.md |
| XAUUSD | LIVE | 2026-04-23 | ../../core/strategies/_archive/guardian/LOCK.md |


## turn-of-month

A calendar-timed return premium around the turn of the month, from institutional month-end cash flows reinvested at the turn.

- **Class finding:** No tradeable turn-of-month premium on SPX500's canonical Pepperstone feed (2017–2026, n=113 turns) — the existence battery is hard-absent (Welch t=0.64, label-perm p=0.25), the effect is entirely COVID-concentrated, and the halves sign-reverse. [SPX500.md F5](SPX500.md)

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| ES | AMBIGUOUS-PARKED | 2026-07-12 | ../../docs/briefs/closures/Q-HARV-0-month-end-rebalance-ES.md |
| EURUSD | AMBIGUOUS-PARKED | 2026-06-10 | ../../docs/rejected_candidates.md |
| SPX500 | DEAD | 2026-06-16 | #F5 |


## venue-transfer

Porting a locked strategy to a different venue or contract without re-deriving parameters.

- **Class finding:** Structural venue costs, not signal decay, are the usual killer — DJ30 to MYM returned an OOS PF ratio of 0.559 against a 0.8x gate. [YM.md Y3](YM.md)

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| 6J | AMBIGUOUS-PARKED | 2026-07-16 | ../../docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md |
| MJY | DEAD | 2026-07-05 | #M1 |
| MYM | DEAD | 2026-07-09 | ../../lab/archive/striker_dj30_mym_prototype_2026-07/RESULTS.md |
| YM | DEAD | 2026-07-09 | ../../lab/archive/striker_dj30_mym_prototype_2026-07/RESULTS.md |
