# INSTRUMENT PROFILES — mechanism x instrument verdict index

> **GENERATED — do not hand-edit; source = ledger PROFILE blocks.**
> Regenerate: `python scripts/instrument_profiles.py build`
> Source of record is always `ops/instruments/<SYM>.md`.


## Matrix

| Mechanism | 6J | BTCUSD | ES | EURGBP | EURUSD | GER40 | M2K | M6A | M6B | MCL | MES | MGC | MJY | MNQ | MYM | NAS100 | NG | NQ | SPX500 | USDCAD | USOIL | XAGUSD | XAUUSD | YM | ZB | ZF | ZN |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| band-pierce-continuation | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | F | . | . | . | . | . | . | . |
| bar-closing-location-autocorrelation | . | . | . | . | . | . | . | . | . | . | . | . | . | D | D | . | . | . | . | . | . | . | . | . | . | . | . |
| commodity-carry-term-structure | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | D | . | . | . | . | . | . |
| compression-gated-breakout | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | A | . | . | . | . |
| daily-range-state-persistence | . | . | . | . | . | . | . | . | . | A | . | D | . | A | A | . | . | . | . | . | . | . | . | . | . | . | . |
| day-of-week-selection-gate | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | D | . | . | . | . | . | . | . | . | . | . | . |
| event-window-reversal | . | . | . | . | D | . | . | . | . | . | . | D | . | . | D | . | D | . | . | . | . | . | . | . | . | . | D |
| expiry-oi-strike-convergence | . | . | . | . | . | . | . | . | . | . | . | A | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . |
| htf-compression-breakout-5m | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . |
| ict-liquidity | . | . | . | . | . | . | . | . | . | . | . | . | . | D | D | . | . | . | D | . | . | . | . | . | . | . | . |
| impulse-pullback-vwap-reclaim | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . |
| index-dispersion | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | D | . | . | . | . | . | . | . | . |
| intraday-bar-volume-regime | . | . | . | . | . | . | . | . | . | . | . | . | . | A | A | . | . | . | . | . | . | . | . | . | . | . | . |
| intraday-momentum | . | . | . | . | . | . | . | . | . | . | . | . | . | D | . | . | . | D | . | . | . | . | . | . | . | . | . |
| london-range-failed-extension-fade | . | . | . | . | . | . | . | . | . | . | . | D | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . |
| mean-reversion-fade | . | . | . | D | . | . | . | . | . | . | . | . | . | . | . | . | . | . | D | D | D | . | . | . | . | . | . |
| naive-direction-mirror | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | D | . | . | . | . | . | . | D | . | . | . | . |
| opening-pressure | . | . | . | . | . | . | . | . | . | . | . | . | . | D | D | . | . | D | . | . | . | . | . | . | . | . | . |
| opening-range-breakout | . | . | . | . | . | A | . | . | . | . | . | . | . | A | . | A | . | A | D | D | . | . | . | . | D | D | . |
| opening-range-continuation | . | . | . | . | . | . | . | . | . | . | . | . | . | . | D | . | . | . | . | . | . | . | . | . | . | . | . |
| order-flow-depth-imbalance | . | . | . | . | . | . | . | . | . | . | . | . | . | D | . | . | . | . | . | . | . | . | . | . | . | . | . |
| overnight-gap-magnitude-range-conditioning | . | . | . | . | . | . | . | . | . | . | . | . | . | . | A | . | . | . | . | . | . | . | . | . | . | . | . |
| overnight-gap-magnitude-range-conditioning-overnight-calm | . | . | . | . | . | . | . | . | . | . | . | . | . | . | D | . | . | . | . | . | . | . | . | . | . | . | . |
| overnight-range-day-session-transfer | . | . | . | . | . | . | . | . | . | . | . | . | . | . | A | . | . | . | . | . | . | . | . | . | . | . | . |
| overnight-range-failed-extension-fade | . | . | . | . | . | . | D | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . |
| overnight-range-transmission | . | . | . | . | . | . | . | . | . | . | . | . | . | A | . | . | . | . | . | . | . | . | . | . | . | . | . |
| pdh-pdl-breakout-rth | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . |
| pdh-pdl-failed-break-reclaim | . | . | . | . | . | . | D | . | . | . | . | . | . | . | D | . | . | . | . | . | . | . | . | . | . | . | . |
| prior-session-breakout-continuation | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . |
| pullback-failure-resumption | . | . | . | . | . | . | . | . | . | D | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . | . |
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


## bar-closing-location-autocorrelation

**NEW 2026-08-29.** Is a bar's closing-location-value (CLV = (close−low)/(high−low), where within its own H–L range the bar closed) serially correlated bar-to-bar, unconditional on level, session anchor, or volatility regime? Same-series, next-bar (CLV_t → CLV_t+1) — the independent-series IAAFT battery is the right tool here (unlike the three cross-series ids above), reused directly from `daily-range-state-persistence`'s S1 machinery at bar rather than session granularity. Distinct from every level/breakout/continuation construct in any instrument's DEAD table (those are directional-entry constructs keyed to a reference level or window; this is an unconditional shape-persistence statistic, no level or window involved). **Admission-route status under the 2026-07-21 single-instrument index-futures directional-timing raised bar (`docs/rejected_candidates.md`) is resolved by [`docs/adr/2026-08-29-clv-autocorrelation-admission-route-scope.md`](../../docs/adr/2026-08-29-clv-autocorrelation-admission-route-scope.md) (`Accepted`, ratified 2026-08-29, corrected and re-ratified 2026-08-30 — see that ADR's Change history).** The ruling: an unconditional bar-shape statistic with no entry rule attached does not trigger the raised bar's admission gate at all — that gate fires at Pre-Q admission for an actual directional-timing candidate, which neither instrument's finding is yet. If either is later converted into an entry construct, Route 1 is plausibly open (CLV's mechanism sits outside the raised bar's three specifically-mapped cost-re-derivation axes — price / instrument-selection / hold-time — not merely outside a single worked example of that route) independent of and in addition to Route 3 (beat `ORB-MNQ-1` net-of-cost); Route 2 does not apply (same OHLCV modality). Either route still requires a named $0 cost-law pre-screen before any Pre-Q, and Route 1 eligibility still requires full G0 discipline — see the ADR's 2-B/2-C/2-D.

- **Class finding:** MYM (all M15 bars, RTH+overnight, 2020-07→2026-07, n_pairs=141,119): lag-1 Spearman rho(CLV_t, CLV_t+1) = **−0.0370**, 95% CI **[−0.0422, −0.0319]** (excludes 0, negative — anti-persistence/mean-reversion, not momentum), both halves and all 7 years same-signed (magnitude shrinking over the panel, −0.073 in 2020 → −0.02/−0.03 by 2024–2026). Attribution **EXCESS**: obs sits at the 0th percentile of its own zero-mechanism (linear-ACF-preserving) IAAFT surrogate band, p_two_sided=0.0050 — **SIGNAL-EXCESS**, the strongest result of the batch this class-family produced this session. **DROP (2026-08-30)** — the $0 cost-law pre-screen named above has now run ([`c5_clv_cost_screen.py`](../../lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c5_clv_cost_screen.py)): decile-conditioned forward-return implied gross edge **+0.3609 bp/event**, 95% CI **[+0.2436, +0.4822]** — real but ~18× below MYM's own #M6 hurdle (6.57 bp/event, provisional). Fires ADR §4 D2 (fails cleanly): ledger cell **`DROP`** (was `AMBIGUOUS-PARKED`, itself corrected from an initial `CONTINGENT-FORWARD`), no Pre-Q authored. [MYM.md](MYM.md) · [`N-2026-08-29-mym-closing-location-autocorrelation.md`](../../docs/notes/notice/N-2026-08-29-mym-closing-location-autocorrelation.md)

- **Class finding:** (MNQ, 2026-08-29 — backfilled on reconciliation pass): MNQ (full continuous M15 bar sequence, RTH+overnight, n_pairs=141,540): lag-1 Spearman rho(CLV_t, CLV_t+1) = **−0.0301**, block-shuffle null (block=96≈1 day, 2000 permutations) band **[−0.0052, +0.0051]** — real, negative, both halves same-signed (H1 −0.0385, H2 −0.0219). **Not run through the IAAFT battery this session** (only the block-shuffle null, a weaker test than MYM's SIGNAL-EXCESS classification against the linear-ACF-preserving surrogate) — MNQ's result is directionally consistent with MYM's (same sign, same order of magnitude) but not yet typed SIGNAL-EXCESS vs SIGNAL-GENERIC on this instrument. **DROP (2026-08-30)** — the $0 cost-law pre-screen has now run ([`candidate5_clv_cost_screen.py`](../../lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate5_clv_cost_screen.py)): decile-conditioned forward-return implied gross edge **+0.1402 bp/event**, 95% CI **[−0.0381, +0.3244]** (straddles 0) — ~20× below MNQ's own N6 hurdle (3.01 bp/event, already a 4×-round-trip-cost figure, unit-comparable directly despite the "/session" label — see the script's own docstring). Fires ADR §4 D2 (fails cleanly): ledger cell **`DROP`** (was `AMBIGUOUS-PARKED`, itself corrected from an initial `CONTINGENT-FORWARD`). MYM's own cell (above) DROPs on the same pre-screen result, its own instrument-specific number. [MNQ.md](MNQ.md) · [`N-2026-08-29-mnq-clv-autocorrelation.md`](../../docs/notes/notice/N-2026-08-29-mnq-clv-autocorrelation.md)

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| MNQ | DEAD | 2026-08-30 | ../../docs/notes/notice/N-2026-08-29-mnq-clv-autocorrelation.md |
| MYM | DEAD | 2026-08-30 | ../../docs/notes/notice/N-2026-08-29-mym-closing-location-autocorrelation.md |


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

**NEW 2026-08-18.** Conditioner-role, not entry-role: does a day's True Range being in the trailing top quintile predict elevated next-day True Range (vs its own trailing median)? Distinct from `compression-gated-breakout` / `htf-compression-breakout-5m` (both entry-role compression→expansion triggers on MNQ) — this class makes no entry claim, only a range-state-forecasting claim, and was originally scoped to the non-index triad ([Step-0 daily-geometry slate](../../docs/briefs/2026-08-18-step0-daily-geometry-mechanism-slate.md) §2 row S1) — **widened 2026-08-29** to a single index-futures instrument (MYM), disclosed as a scope departure rather than assumed silently; the S1 (same-series, next-session) role this class tests is instrument-agnostic, only the original slate's naming was non-index-scoped. Grounding: evidence-robustness (volatility clustering — ARCH/GARCH canon), not a per-instrument WHO claim.

- **Class finding:** (corrected battery, OFFICIAL): GC (parent, train era 2010–2019) top-quintile TR → elevated next-day TR: **NULL (driving L2 + L4)** — obs 0.5299 at the **8.4th percentile** of GC's own linear-ACF surrogate band (the earlier "near-miss" framing is retracted: the rate sat below the zero-mechanism benchmark's center); by-year 5/9 > 0.50 vs required 7. Ledger cell `DEAD` (re-proposal bar: the corrected battery + a different construction or longer panel). [MGC.md G4](MGC.md) · [`RESULTS_S1A.md`](../../lab/analysis/_inbox/rangestate_gc_2026-08/RESULTS_S1A.md) §6

- **Class finding:** (corrected battery, OFFICIAL): CL (parent, train era 2010–2019) top-quintile TR → elevated next-day TR: **SIGNAL-GENERIC** — presence passes (CI lb 0.5651; halves; L4 boundary-exact 6/8 under the rule's own n_cond<20 exclusion, a disclosed prediction-miss adjudicated rules-govern); attribution GENERIC (obs at the 69th percentile of its own linear-ACF band, p_upper 0.3107) — **canon-attributed volatility clustering, SURVIVAL-ONLY durability. NOT a mechanism; does NOT discharge MCL's mechanism-owed status; NOT a conditioner license** (ADDENDUM-1 A6 rails travel with any quote; the crisis>calm per-year ordering and drop-cluster diagnostic are mandatory co-quotes). **Conditioner-engineering branch PARKED** — [`Q-CONDVAL-1`](../../docs/briefs/closures/Q-CONDVAL-1-closure-falsified.md) `FALSIFIED` 2026-08-18 (committed C−U 0.130 < frozen `L_star` 0.423 at the N-EDGE cell; O2 discharged). Finding stands. [MCL.md C4/C5/C6](MCL.md) · [`RESULTS_S1B.md`](../../lab/analysis/_inbox/rangestate_mcl_2026-08/RESULTS_S1B.md) §5

- **Class finding:** (lighter-weight reuse, M=200 not the frozen M=1,000 — disclosed): MYM (index-futures, full Globex-day session TR, 2020-07→2026-07) top-quintile TR → elevated next-session TR: **SIGNAL-GENERIC** — presence passes (n_cond=332; CI lb 0.6028; halves 0.6928/0.6627, both >0.50); attribution GENERIC (obs 0.6777 at the **22nd percentile** of its own linear-ACF surrogate band — below the band's own median, not a near-miss). Third instrument scored under the class, second SIGNAL-GENERIC of three (GC NULL, CL SIGNAL-GENERIC, MYM SIGNAL-GENERIC) — the modal outcome so far. **Not pursued as a conditioner** — the sibling CL SIGNAL-GENERIC already failed the downstream cost-effectiveness test (`Q-CONDVAL-1`, cited above); ledger cell `AMBIGUOUS-PARKED`, matching CL's own cell state for the identical verdict shape. [MYM.md](MYM.md) · [`N-2026-08-29-mym-rangestate-persistence.md`](../../docs/notes/notice/N-2026-08-29-mym-rangestate-persistence.md) · [`c1_results.json`](../../lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c1_results.json)

- **Class finding:** (MNQ, 2026-08-29 — backfilled on reconciliation pass): MNQ's own same-day score of this class reused the frozen corrected battery verbatim as a new instrument leaf. Raw gateHit **0.6867** (n_cond=332) beats both prior instruments (GC 0.5299, CL 0.6282) on presence limbs L1–L3, but this instrument's own by-year floor (L4) is structurally **AMBIGUOUS** (only 6 of the required 7 full calendar years qualify at n_cond≥20) and the attribution limb (L5) **VOIDs** — the IAAFT diagnostic gate fails at both iter=100 and iter=500, byte-identically, with the escalation ladder's Schreiber end-matching trim finding no improving offset. **Not a fourth verdict alongside NULL/SIGNAL-GENERIC/SIGNAL-GENERIC — uncertified**, the exact failure mode the corrected battery exists to catch (a naive L1–L3-only read would have called this SIGNAL). Ledger cell `AMBIGUOUS-PARKED`, re-open trigger is operator-scoped (panel extended to ≥7 full years, or a fresh surrogate-class design per the frozen spec's own O5 remedy) — not calendar-triggered. [MNQ.md](MNQ.md) · [`N-2026-08-29-mnq-daily-range-persistence.md`](../../docs/notes/notice/N-2026-08-29-mnq-daily-range-persistence.md)

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| MCL | AMBIGUOUS-PARKED | 2026-08-18 | ../../lab/analysis/_inbox/rangestate_mcl_2026-08/RESULTS_S1B.md |
| MGC | DEAD | 2026-08-18 | ../../lab/analysis/_inbox/rangestate_gc_2026-08/RESULTS_S1A.md |
| MNQ | AMBIGUOUS-PARKED | 2026-08-29 | ../../docs/notes/notice/N-2026-08-29-mnq-daily-range-persistence.md |
| MYM | AMBIGUOUS-PARKED | 2026-08-29 | ../../docs/notes/notice/N-2026-08-29-mym-rangestate-persistence.md |


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


## expiry-oi-strike-convergence

**NEW 2026-08-21 (MSL-S4).** Discharges the 2026-08-14 WHO-track E1 stop rule ([closure](../../docs/briefs/closures/MSL-S7-closure-resolved-e1-hold.md)) — first WHO named outside the 2026-08-10 INTAKE-DRY set and outside a transfer of C1/C2/C3/S2A/S2B. Near a published options expiry, price statistically converges toward the strike carrying the largest open interest more than on non-expiry control sessions; enter in the direction that closes the gap between current price and that strike when price is displaced from it by more than a threshold, inside a declared pre-expiry window. WHO: options market-makers who wrote the concentrated open interest at that strike, mechanically obligated to keep a delta-neutral book as time-to-expiry shrinks and near-the-money gamma rises (Γ ∝ 1/√T) — a hedging-requirements / expiry-mechanics constraint (ADR clause-1-admissible), not a preference. The trade direction is read directly off observable data (spot price vs. the published strike), never off an assumption about unobservable dealer gamma sign — the load-bearing distinction from the sibling construct below, which this class does **not** reopen.

- **Class finding:** G0 frozen on operator B4 GO 2026-08-21; Explore-confirm (charter step 5a) **deferred by explicit operator override** at freeze (no Databento/market-data access in the sourcing session's environment) rather than scored — Pine authored CC-solo directly off the frozen construct, with the operator's own TV backtest as the first empirical evidence instead of a pre-Pine Explore score. This is a disclosed deviation from the charter's default step ordering, not a silent skip. [`STAGE1`](../../lab/analysis/c1/msl_s4_mgc_2026-08/STAGE1.md) · [`PREREG_G0`](../../lab/analysis/c1/msl_s4_mgc_2026-08/PREREG_G0.md) · [`RUNBOOK`](../../lab/analysis/c1/msl_s4_mgc_2026-08/RUNBOOK.md).

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| MGC | AMBIGUOUS-PARKED | 2026-08-21 | ../../lab/analysis/c1/msl_s4_mgc_2026-08/_explore_confirm_2026-08-21_LOG.md |


## htf-compression-breakout-5m

**NEW 2026-08-10.** Trade the **5m** compression→expansion break itself (not an HTF bias filter on 1m scalps): structural stop at the opposite quiet extreme; first valid signal per RTH session only (temporal selectivity under [`ADR 2026-08-10`](../../docs/adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md)); session-flat; Tradeify RT. Distinct from `compression-gated-breakout` dense-1m / fixed-G cells.

- **Class finding:** MNQ HTF-native 5m with-break (`Q-TNEC-CON-3`) explore → `AMBIGUOUS-HOLD` — long +0.073R with CI straddling 0; short −0.026R; not FALSIFIED; not live-pass; CONFIRM unread. [MNQ.md](MNQ.md) · [`RESULTS`](../../lab/analysis/c1/mnq_tnec_con3_htf_native_break_2026-08/RESULTS.md)

_No instrument has a recorded verdict on this mechanism._


## ict-liquidity

ICT-style liquidity-sweep / fair-value-gap geometry (sweep → FVG → opposing-pool draw) used as an entry signal.

- **Class finding:** Sweep→same-direction-FVG→opposing-pool-draw direction is real on SPX500 (block-permutation p=0.0144) but fails robustness (drop-top-3 = −0.152R, 95% block-CI straddles 0). [SPX500.md D2](SPX500.md)

- **Class finding:** — CORRECTED 2026-08-04; supersedes the former "the 1M 0%-fill wall is feed-general" clause, which is REFUTED. The archived closure attributed US500's **0 fills in 247 attempts** to an instrument-general *price law* — "displacement FVGs continue rather than retrace within 6 bars" — and predicted recurrence on "NAS100 or any fast 1m index". **That law is false on native micro data.** MNQ retraces to FVG mid within the frozen `retraceK=6` **59.06%** of the time (n=128,089; 58–60% in *every* year 2019–2026, including the 2020 crash and 2022 bear), and ES **59.88%** (n=124,748). Every escape route is refuted at 45×+ the ≤1.2% rate that 0-of-247 requires: raid-conditioning leaves it at **59.01%**, the arm-delay curve is nearly flat (**55.91%** even armed 8 bars late — mid-touches recur, they are not one-shot), and ES retraced **62.33%** in the *exact* 2026-06-24→26 window that produced the 0/247. **0/247 was platform-side by elimination** — the deployed (now lost) script, TV's strategy-tester fill handling, or the retired Pepperstone US500 CFD feed; not further separable, and recorded as a residual, never as "bug X". **Consequence for this class:** do **not** cite "1m FVGs don't retrace" against an execution layer on any instrument; **do** require any such design to demonstrate fills on native data rather than trusting TV-tester fill behavior. [MNQ.md W3](MNQ.md) · [`RESULTS_1M_DIAG.md`](../../lab/analysis/_inbox/ict_mnq_2026-08/RESULTS_1M_DIAG.md)

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


## intraday-bar-volume-regime

**NEW 2026-08-29.** Does an M15 bar's volume, above its own time-of-day slot's trailing median (20 prior same-slot occurrences — the `tod-baseline-range-trigger` deseasonalization convention, reused not invented), predict the *next* bar's range above its own time-of-day-conditioned trailing median? Cross-series (volume, range), 1-bar lag — carries the same shared-regime confound as `overnight-range-day-session-transfer` (just at bar-scale, not session-scale), scored the same way: a $0 increment test against the mundane same-series (range→range) comparator, not a full corrected battery — **stratified on that comparator, not a marginal-rate diff** (see the 2026-08-29 correction below; a marginal-rate diff read the sign backwards). Distinct from `opening-pressure` (opening-window volume × directional efficiency, DEAD on MYM) — this is a magnitude-only, any-time-of-session claim. Null-validity grounding: mixture-of-distributions literature (Tauchen & Pitts 1983; Bollerslev & Jubinski 1999), the volume-clustering analogue of the ARCH/GARCH canon `daily-range-state-persistence` cites for range — a citation-based grounding, disclosed as lighter-weight than the repo-native frozen battery.

- **Class finding:** (corrected — stratified design, 2026-08-29, AUTHORITATIVE): same design correction as `overnight-range-day-session-transfer`/`overnight-gap-magnitude-range-conditioning` (marginal comparison → stratify on `bias_hist`, measure lift within stratum), applied here because same-bar volume and range are highly correlated (independently verified on MYM's own data: Spearman = **0.8618**, n=141,467). Within `bias_hist=0` (own range not elevated, n=71,492): lift **+0.1649** (0.4528 vs 0.2879). Within `bias_hist=1` (own range elevated, n=68,113): lift **+0.2455** (0.7150 vs 0.4695). Block-bootstrap on the minimum stratified lift: mean **+0.1648**, 95% CI **[+0.1537, +0.1761]**, p(lift≤0)≈0. **Within-stratum null-calibrated p COMPUTED 2026-08-30** (precondition cleared, vendor bars present this session): **p=0.00025 both strata.** **VERDICT: INCREMENT** (was UNRESOLVED). Cross-instrument corroboration: MNQ's own same-day candidate 3 (now registered under this same id — MNQ class finding below) found a similar shape, re-verified and equally decisive (p=0.00025 both strata) on the same 2026-08-30 pass. Ledger cell still `AMBIGUOUS-PARKED` — INCREMENT on the within-stratum precondition is not yet a certified conditioner (Phase 1's own joint-surrogation null, a different confound, is still owed per `Q-VOLREGIME-1`'s §5). **`Q-VOLREGIME-1`'s own Phase 0.5 precondition is now CLEARED on both instruments** (was `PRECONDITION-UNMET`/pending) — see that brief's own §4/§7. [MYM.md](MYM.md) · [`N-2026-08-29-mym-bar-volume-regime.md`](../../docs/notes/notice/N-2026-08-29-mym-bar-volume-regime.md)

- **Class finding:** (cross-instrument, MNQ, 2026-08-29; re-verified 2026-08-30 against live vendor bars — figures below CONFIRMED, not the original unverified numbers): backfilled on reconciliation pass — MNQ's own same-day bar-volume-regime candidate, independently run, correctly stratified on the trigger-bar side (not a marginal-vs-stratified correction like MYM's), found a near-identical shape: within-stratum lift **+22.3pp** (own-range-not-elevated stratum, n=67,417) / **+27.4pp** (own-range-elevated stratum, n=68,603), **within-stratum null-calibrated p=0.00025 both strata** (new script `candidate3_stratified_rerun.py`, same-bar volume/range Spearman correlation **0.88** (vs MYM's own 0.8618, independently measured — not assumed by analogy). **GRADUATE, precondition CLEARED** — reached independently before either session saw the other's work, now backed by a Type-I-controlled test on both sides. Direction limb (does volume predict next-bar directional continuation, not just range) is a clean null on MNQ; untested on MYM this session. **Code bug (Codex review, PR #210) fixed AND re-verified, 2026-08-30:** `candidate3_volume_regime.py`'s ToD-matched range-outcome variable compared the next bar's range against the *trigger* bar's own time-of-day threshold instead of the next bar's own — reintroducing the exact seasonality confound the ToD-matching exists to remove. Fixed in PR #210's commit; **re-run 2026-08-30 against live `MNQ_M15.csv`** — the marginal ToD-matched range lift shifts up (+18.1pp → **+19.1pp**, CI [0.684, 0.707]) and the incremental-stratified figures shift up similarly (+20.6pp/+25.6pp → +22.3pp/+27.4pp) — the fix strengthens the finding, it does not dissolve it. See `N-2026-08-29-mnq-bar-volume-regime.md`'s own 2026-08-30 update for the full detail. Registered here under MYM's id (`intraday-bar-volume-regime`) rather than a separate MNQ-named one — unlike the overnight-range/gap-magnitude split, this construct carries no unresolved nested-hypothesis structure blocking a straightforward merge, so (unlike `overnight-range-transmission`) no taxonomy-merge review was owed before authoring a shared Pre-Q. **Pre-Q opened 2026-08-30:** [`Q-VOLREGIME-1`](../../docs/briefs/Q-VOLREGIME-1-intraday-bar-volume-regime.md), scoring both instruments' own H independently (its own §6). [MNQ.md](MNQ.md) · [`N-2026-08-29-mnq-bar-volume-regime.md`](../../docs/notes/notice/N-2026-08-29-mnq-bar-volume-regime.md)

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| MNQ | AMBIGUOUS-PARKED | 2026-08-30 | ../../docs/notes/notice/N-2026-08-29-mnq-bar-volume-regime.md |
| MYM | AMBIGUOUS-PARKED | 2026-08-30 | ../../docs/notes/notice/N-2026-08-29-mym-bar-volume-regime.md |


## intraday-momentum

A next-bar or intraday continuation signal keyed to the prior bar's or prior session's directional momentum (Baltussen-class).

- **Class finding:** Baltussen-class intraday momentum is statistically ABSENT on modern MNQ — the cost-geometry thesis was real (hurdle fell 11.06→3.01 bp) but the OOS edge decayed negative (gross Sharpe +0.88→−0.13), corroborating the published post-2021 decay and an external 14-signal-family falsification (arXiv 2605.04004). [NQ.md N3](NQ.md)

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| MNQ | DEAD | 2026-07-21 | ../../docs/briefs/rnd-pipeline/D5-RECOST-1-mnq-native-cost-law-rescope-scoping.md |
| NQ | DEAD | 2026-07-21 | ../../docs/briefs/rnd-pipeline/D5-RECOST-1-mnq-native-cost-law-rescope-scoping.md |


## london-range-failed-extension-fade

**NEW 2026-08-12 (MSL-C2).** Fade a failed extension of the London-session high/low (formed before COMEX RTH) into the COMEX open: reclaim after a break that does not follow through; structural stop beyond the swept London extreme; truncated-loss exit; session-flat; first valid signal per session. Session-structure displacement — **not** a scheduled auction/fix window.

- **Class finding:** MGC explore IS **FALSIFIED 2026-08-13** — both arms mean ≈ −0.18R, CI entirely &lt; 0 (long n=327 CI [−0.287, −0.071]; short n=310 CI [−0.292, −0.075]); DELETE FAIL. CONFIRM unread. [closure](../../docs/briefs/closures/MSL-C2-closure-falsified.md) · [RESULTS](../../lab/archive/msl_c2_mgc_2026-08/RESULTS_g2.md)

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| MGC | DEAD | 2026-08-13 | ../../docs/briefs/closures/MSL-C2-closure-falsified.md |


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

**NEW 2026-08-05.** Resting displayed size, aggregated across book levels, used as a directional predictor of near-term price. The first mechanism class in this estate sourced from **order-flow (MBP-10) data rather than OHLCV** — the "different modality" limb of the 2026-07-21 index-futures-intraday domain bar (route 2).

- **Class finding:** 10-level size imbalance carries **no** directional information at the 1-minute horizon on NQ. Spearman ρ(I_t, r_{t+1}) = **−0.01205** on n=1,167 RTH minute pairs — wrong-signed against the predicted positive, and at the **36.7th percentile** of a within-day shuffled null (p_emp 0.633). [MNQ.md](MNQ.md) · [`RESULTS.md`](../../lab/archive/mnq_orderflow_probe_2026-08-04/RESULTS.md)

- **Class finding:** — the depth census is the reusable constraint. NQ front-month displays a **median 67 contracts across all twenty price levels** (p05 40 / p95 94), ≈3.4 per level, so any ratio built from displayed size is coarse by construction: 525 distinct values in 1,167 observations, **78.1% inside a tie group**, 5.8% exactly zero. **Any future size-derived book feature on this instrument family must argue against that census first** — the constraint is how little book there is to observe, not the estimator. [MNQ.md](MNQ.md)

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| MNQ | DEAD | 2026-08-05 | ../../lab/archive/mnq_orderflow_probe_2026-08-04/RESULTS.md |


## overnight-gap-magnitude-range-conditioning

**NEW 2026-08-29.** Does the overnight gap's **magnitude** (today's RTH open − yesterday's RTH close, sign discarded) predict the same day's RTH-session range? Cross-series, same-session — the same S2-shaped shared-regime confound as `overnight-range-day-session-transfer`, scored identically (a $0 increment test vs. the day-session-history comparator, not a full battery). Distinct from any fill/fade **direction** claim (e.g. Mesfin 2026, MNQ-only, external corroboration that does not exist for MYM on either magnitude or direction).

- **Class finding:** (corrected — stratified design, 2026-08-29, AUTHORITATIVE): same design correction as `overnight-range-day-session-transfer` (marginal comparison → stratify on `bias_hist`, measure lift within stratum). Within `bprime=0` (n=1,010): lift **+0.1404** (0.5526 vs 0.4122). Within `bprime=1` (n=297): lift **+0.0672** (0.7766 vs 0.7094) — **the sign itself flips positive** in both strata. Block-bootstrap on the minimum stratified lift: mean **+0.0594**, 95% CI **[−0.0419, +0.1477]**, p(lift≤0)=0.1247 / null-calibrated p(null≥obs)=0.0086 (within-stratum circular-shift of the gap predictor, distinct rotations enumerated, identity included; n_null=1304 from the sibling joint-gate cache vs original n=1307; 3-day difference disclosed; per-stratum null p=0.00099 / 0.152). **First operator ruling, 2026-08-30** ("go with INCREMENT, ... the null-calibrated test is the more reliable one") read this as a blanket INCREMENT off the blended p=0.0086 figure. **That figure was itself defective (Codex review, PR #211):** `circular_shift_null_min_lift` computes p=0.0086 as the *product* of the two per-stratum tail probabilities, which tests the sharp joint null that both strata are simultaneously zero — not the disjunctive composite null a "both strata" claim needs to reject. The correct test is an intersection-union test (the **max** of the per-stratum p's): max(0.00099, 0.152) = 0.152, not significant. **Corrected disposition — split by stratum:** `bprime=0` (day-history NOT elevated): **INCREMENT** — the within-stratum p=0.00099 is properly scoped and decisive, the same operator principle (null-calibrated over bootstrap CI) correctly applied. `bprime=1` (day-history elevated): **not established** — p=0.152 does not reject. A meaningfully weaker signal than the sibling overnight-range candidate's +0.2186 even in its decisive stratum. The `bprime=0` result is nested under `Q-RANGEXFER-1` as the new (2026-08-30) hypothesis clause `H-RANGEXFER-1.b-MYM`, distinct from `H-RANGEXFER-1.a-MYM`'s overnight-calm-restricted claim (a different estimand). First instrument scored under this id. [MYM.md](MYM.md) · [`N-2026-08-29-mym-gap-magnitude-rth-range.md`](../../docs/notes/notice/N-2026-08-29-mym-gap-magnitude-rth-range.md)

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| MYM | AMBIGUOUS-PARKED | 2026-08-30 | ../../docs/briefs/closures/Q-RANGEXFER-1-closure-ambiguous-design.md |


## overnight-gap-magnitude-range-conditioning-overnight-calm

**Split off from `overnight-gap-magnitude-range-conditioning` above, 2026-08-30 (Q-RANGEXFER-1 closure) — same cross-series shared-regime confound, distinct restriction.** Does unsigned RTH-open gap magnitude predict same-day RTH range specifically *within the overnight-range-calm stratum* (today's own overnight range below its own trailing P80) — the ⚠ note above's own `gap_lifts_within_overnight_strata` two-way statistic, not the `bprime`(day-history)-restricted statistic the sibling heading owns. This is `H-RANGEXFER-1.a-MYM`.

- **Class finding:** (`FALSIFIED`, MYM, 2026-08-30): stage-1 lift +8.5pp (bootstrap p=0.037, null-calibrated p=0.0495 — barely clears 0.05, already the weakest, least-decisive cell in the whole batch) failed the presence battery's own L2 limb: block-bootstrap CI (frozen `block=20, draws=4000, seed=42`) on the restricted lift is `[-0.008, +0.180]` — the lower bound crosses zero. L1 and L3 both pass; the failure is L2 alone. Adversarially verified before being trusted (4-lens workflow, `TRUSTWORTHY_AS_IS`): the decisive CI independently reproduced by five separate methods (bit-exact from-scratch bootstrap, 12 alternate seed/RNG-engine trials, naive i.i.d. bootstrap, normal-approximation SE). Genuinely borderline, disclosed not hidden: 1 of 5 tested seeds under a different-but-defensible non-circular bootstrap variant flips the sign barely positive. Full record: [`rangexfer_presence_battery_2026-08-30/RESULTS.md`](../../lab/analysis/_inbox/rangexfer_presence_battery_2026-08-30/RESULTS.md). [MYM.md](MYM.md) · [`Q-RANGEXFER-1-closure-ambiguous-design.md`](../../docs/briefs/closures/Q-RANGEXFER-1-closure-ambiguous-design.md)

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| MYM | DEAD | 2026-08-30 | ../../docs/briefs/closures/Q-RANGEXFER-1-closure-ambiguous-design.md |


## overnight-range-day-session-transfer

**NEW 2026-08-29.** The frozen magnitude-persistence spec's own "S2" role (`docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md` §4 D5): does the Globex **overnight** (pre-RTH) session's realized range predict the **same trading day's** RTH-session range? Cross-series (overnight range, RTH range are different series), same-session — the spec explicitly marks this role PAUSED pending a joint-surrogate null design (independent-series IAAFT, `daily-range-state-persistence`'s legitimate S1 tool, does NOT delete the shared-regime confound here) plus an owed $0 stage-1 cheap falsifier and an operator GO. Conditioner-role, not entry-role — makes no directional claim.

- **Class finding:** (corrected — stratified design, 2026-08-29, AUTHORITATIVE): MYM $0 cheap falsifier for spec un-pause precondition 2 ("does overnight-state conditioning beat matched day-session-history conditioning?"), run properly as a **stratify-on-`bias_hist`, measure-lift- within-stratum** design after adversarial review caught that a marginal-rate comparison does not test "matched conditioning" — two correlated predictors can show near-identical marginal rates while one still carries large incremental information. Within `bprime=0` (n=1,010): lift **+0.3178** (0.6963 vs 0.3785). Within `bprime=1` (n=297): lift **+0.2207** (0.8607 vs 0.6400). Block-bootstrap on the minimum stratified lift: mean **+0.2186**, 95% CI **[+0.1042, +0.3216]**, p(lift≤0)=0.00025 / null-calibrated p(null≥obs)=3.4×10⁻⁶ (within-stratum circular-shift of the overnight predictor, distinct rotations enumerated, identity included; n_null=1304 from the sibling joint-gate cache vs original n=1307). Per-stratum null p=0.00099 / 0.00338. **INCREMENT — decisive; verdict unchanged under the corrected null.** Un-pause precondition 2 is now CLEARED; conditions 3 (joint-surrogate null design, adversarial-reviewed) and 4 (operator GO) remain outstanding before any full battery. First instrument scored under this role; ledger cell `AMBIGUOUS-PARKED` (GRADUATE-eligible, Pre-Q deferred — no frozen forward test executing). [MYM.md](MYM.md) · [`N-2026-08-29-mym-overnight-rth-range-transfer.md`](../../docs/notes/notice/N-2026-08-29-mym-overnight-rth-range-transfer.md)

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| MYM | AMBIGUOUS-PARKED | 2026-08-30 | ../../docs/briefs/closures/Q-RANGEXFER-1-closure-ambiguous-design.md |


## overnight-range-failed-extension-fade

**NEW 2026-08-13 (MSL-C3 K2 revive).** Fade a **failed** extension of the Globex **overnight** high/low into the RTH probe window: reclaim after a break that does not follow through; structural stop beyond the swept overnight extreme; truncated-loss exit; session-flat by 16:00 ET; k=1 first valid signal per session. Mean-reversion-at-a-level (route ①) — **not** PDH/PDL RTH prior-day, **not** London/COMEX (C2), **not** WSTRUCT weekly.

- **Class finding:** M2K explore **FALSIFIED 2026-08-13** (Axis B both-arms IS 95% CI entirely &lt; 0; long n=359 CI [−0.220, −0.021]; short n=378 CI [−0.204, −0.014]; pooled −0.114R). CONFIRM unread. [closure](../../docs/briefs/closures/MSL-C3-K2-closure-falsified.md) · [RESULTS](../../lab/archive/msl_c3_m2k_2026-08/RESULTS_g2.md).

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| M2K | DEAD | 2026-08-13 | ../../docs/briefs/closures/MSL-C3-K2-closure-falsified.md |


## overnight-range-transmission

**NEW 2026-08-29 (Q-RANGEXFER-1); scope broadened to cover MYM 2026-08-30 (Q-RANGEXFER-1 amendment).** Conditioner-role, not entry-role: does the Globex overnight (pre-RTH) session's own realized range, and/or the unsigned RTH-open gap magnitude, predict the *same trading day's* RTH-session realized range being elevated (vs its own trailing median, causal `.shift(1)`)? Cross-series claim — bias and outcome are two *different* magnitude series on the *same* day, not one series lagged against itself. Distinct from `daily-range-state-persistence` (single-series, next-*day* self-lag) and from `overnight-range-failed-extension-fade` (entry-role fade-the-level construct keyed to a broken overnight extreme, not a conditioner on realized range magnitude). Grounding: same ARCH/GARCH-canon volatility-clustering evidence-robustness as `daily-range-state-persistence`, extended to the cross-series/same-day case — the frozen corrected-null-battery spec's own §4 (D5) names this shape **"S2"** and holds its S1 (single- series) null does NOT port to it (independent surrogation of the two series deletes the shared same-day-regime confound the test needs to preserve; O1: `UNRESOLVED-NEEDS-DESIGN`).

- **Class finding:** (D5 stage-1 $0 cheap falsifier, MNQ, OFFICIAL): overnight range clears D5's un-pause condition (2) decisively — incremental lift over matched day-history conditioning +57.7pp / +38.7pp across both day-history strata (block-bootstrap p<0.00025, n=1487 scored days). Gap magnitude also clears it on its own (+17.0pp / +15.5pp vs day-history, p≈0.00225) but a same-session joint check (holding overnight-range state fixed) found gap's own increment is **conditional and sign-unstable**: +10.5pp when overnight range is itself NOT elevated (bootstrap p=0.0078 / null-calibrated p=0.00871) but −8.1pp (not significant, bootstrap p=0.998 / null-calibrated p=0.997 for the positive direction) when overnight range is already elevated — gap does not add information once overnight range is known to be hot. Recalibration does not overturn the nested-gap finding. Parent-Q convention: overnight range is the primary falsifiable claim; gap magnitude is a forked, nested sub-question scoped to the overnight-calm regime only, not a co-equal claim. Stage 2 (joint-surrogation null design solving D5's O1 item, adversarial review, operator GO) is **owed, not yet run, on either instrument** — this class finding is a stage-1 result only, not a certified verdict under the corrected battery. [MNQ.md](MNQ.md) · [`Q-RANGEXFER-1`](../../docs/briefs/Q-RANGEXFER-1-overnight-range-gap-magnitude-transfer.md) · [`joint gate script`](../../lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate24_joint_gate.py)

- **Class finding:** (D5 stage-1 $0 cheap falsifier, MYM, amended in 2026-08-30 under this same Q-brief — see below): overnight range's own min-stratified lift +21.9pp (block-bootstrap p=0.00025, n=1,307 scored days across two day-history strata), gap magnitude's own +5.9pp pooled (AMBIGUOUS, p=0.1247) — same qualitative relationship to its own sibling as MNQ's pair. Joint gate (`c24_joint_gate.py`, direct port of MNQ's script) replicates the nested structure: gap lift +8.5pp (calm, null-calibrated p=0.020) / −7.2pp (hot, p=0.888) vs. this heading's own MNQ +10.5pp/−8.1pp — same sign, same relative ordering, 10.6%-44.8% smaller in magnitude (not a uniform ratio). Scored independently of MNQ's own verdict (Q-RANGEXFER-1 §6); stage 2 equally owed and not yet run. [MYM.md](MYM.md) · [`N-2026-08-29-mym-overnight-gap-joint-gate.md`](../../docs/notes/notice/N-2026-08-29-mym-overnight-gap-joint-gate.md)

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| MNQ | AMBIGUOUS-PARKED | 2026-08-30 | ../../docs/briefs/closures/Q-RANGEXFER-1-closure-ambiguous-design.md |


## pdh-pdl-breakout-rth

**NEW 2026-08-10.** First RTH close beyond prior-RTH high (long) or low (short) → enter next 1m open; structural stop at the opposite prior extreme; first valid signal per session; session-flat; Tradeify RT. Through-break continuation — distinct from compression-break (CON-2/3), ORB, MNQPROX OF-approach contrast, and N9/C10 level-touch attraction/fade.

- **Class finding:** MNQ PDH/PDL with-break (`Q-TNEC-CON-4`) explore → `AMBIGUOUS-HOLD` — long −0.007R / short +0.005R; CIs straddle; stop ≈257 pt; gross/(4×RT) ≈0.27×; not FALSIFIED; not live-pass; CONFIRM unread. [MNQ.md](MNQ.md) · [`RESULTS`](../../lab/analysis/c1/mnq_tnec_con4_pdh_pdl_break_2026-08/RESULTS.md)

_No instrument has a recorded verdict on this mechanism._


## pdh-pdl-failed-break-reclaim

**NEW 2026-08-13 (MSL-C3).** Fade a **failed** break of prior-day RTH high/low (PDH/PDL): reclaim after a sweep that does not follow through; structural stop beyond the swept extreme; truncated-loss exit; session-flat by 16:00 ET; k=1 first valid signal per session. Mean-reversion-at-a-level (route ①) — **not** through-break continuation.

- **Class finding:** MYM explore **FALSIFIED** (both-arms CI &lt; 0) — [C1 RESULTS](../../lab/archive/msl_c1_mym_2026-08/RESULTS_g2.md) · [closure](../../docs/briefs/closures/MSL-C1-closure-falsified.md). M2K unpaid path [OPERATOR-KILL](../../docs/briefs/closures/MSL-C3-closure-operator-kill.md) (B4 declined; class not killed at C3). **M2K dual-axis explore FALSIFIED 2026-08-13** (Axis A both-arms IS 95% CI entirely &lt; 0; long n=293 CI [−0.256, −0.038]; short n=295 CI [−0.307, −0.089]; pooled −0.171R) — [closure](../../docs/briefs/closures/MSL-C3-K2-closure-falsified.md) · [RESULTS](../../lab/archive/msl_c3_m2k_2026-08/RESULTS_g2.md). Does not clear or reopen the MYM explore kill.

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| M2K | DEAD | 2026-08-13 | ../../docs/briefs/closures/MSL-C3-K2-closure-falsified.md |
| MYM | DEAD | 2026-08-13 | ../../docs/briefs/closures/MSL-C1-closure-falsified.md |


## prior-session-breakout-continuation

**NEW 2026-08-22 (deep-lane DL-2).** A break of the immediately-prior *full trading session's* high or low, confirmed by a subsequent session close beyond the level before entry; structural stop at the opposite prior extreme; target at a fixed multiple of that risk; first valid signal per session (k=1); session-flat. The full-session generalization of `pdh-pdl-breakout-rth`: that id's one prior use (MNQ) implicitly took an equity-cash "RTH" window as both the reference and entry window; this id's reference/entry window is the instrument's own full native trading session (e.g. the complete CME Globex day for a currency future), not an RTH-scoped sub-window. The distinction is deliberate, not cosmetic — swapping which hours count as "the session" changes the volatility regime and event population the level is drawn from, the same load-bearing reason `overnight-range-failed-extension-fade` was split from `pdh-pdl-failed-break-reclaim` rather than folded into it. First campaign under this id: [DL-2 prereg](../../docs/briefs/pre-registration/2026-08-22-deep-lane-dl2-m6a-pdhpdl-prereg.md) (M6A) — no class finding yet, this id is untested on every instrument at authoring time.

- **Class finding:** (M6A, 2026-08-22 — same day as minting): DL-2's TRAIN scoring closed AMBIGUOUS/ABANDONMENT the same day this id was minted — nominee V9 fails 3 of 4 nomination gates; a same-day geometric-feasibility diagnostic found the construction structurally infeasible on M6A and retired it for that instrument, with a stop-rule/re-proposal bar binding any successor. [`RESULTS.md`](../../lab/archive/dl2_m6a_pdhpdl_2026-08-22/RESULTS.md).

_No instrument has a recorded verdict on this mechanism._


## pullback-failure-resumption

**NEW 2026-08-13 (MSL-S2A).** Join an established **intraday** directional move after a pullback fails to reverse it — continuation entry on the resumption bar; hard stop beyond the pullback extreme; target at `rr` ∈ [2, 3] of that stop; session-flat; k=1 first valid signal per session. One trigger class: *pullback-failure resumption*. Not breakout-from-range, not compression-expansion, not MR-at-level.

- **Class finding:** MCL explore **FALSIFIED** (N-ACT 0.511 trades/week; long FLIP FAIL) — [S2A RESULTS](../../lab/archive/msl_s2a_mcl_2026-08/RESULTS_g2.md) · [closure](../../docs/briefs/closures/MSL-S2A-closure-falsified.md). CONFIRM unread.

| Instrument | Verdict | Date | Source |
|---|---|---|---|
| MCL | DEAD | 2026-08-13 | ../../docs/briefs/closures/MSL-S2A-closure-falsified.md |


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

**NEW 2026-08-20 (`Q-TODVOL-1`).** Within-instrument temporal selectivity under [`ADR 2026-08-10`](../../docs/adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md) §2-B — first RTH bar, outside the opening-range window, whose range exceeds a frozen multiple of the **same time-of-day slot's own trailing median range** (causal, `.shift(1)`); enter in that bar's own close-vs-open direction; stop/target sized off the triggering bar's own range (not an independent point count); session-flat; first valid signal per session (k=1). Causal story: volatility clustering (ARCH/GARCH-class serial dependence in absolute returns) as a real-time, per-moment information-arrival signal — distinct from a fixed clock window (ORB) or a reference price level (PDH/PDL, VWAP). Runs on **native 15m RTH bars** — explicitly outside the paused dense-1m/G=10 lane ([`DENSE1M-UNPAUSE closure`](../../docs/briefs/closures/DENSE1M-UNPAUSE-closure-resolved-u0-keep.md), U0 KEEP stands) — so gated by the [`2026-08-16 CON-5-scope ADR`](../../docs/adr/2026-08-16-con5-timeframe-scope-cheap-falsifier-gate.md) §2 D2 pre-G0 cheap falsifier before route ① counts as open for it.

- **Class finding:** MNQ D2 pre-G0 falsifier `FAIL` — mean signed gross **+0.2546 pt** vs the generous **2.82 pt** pass bar (0.5× the 4×RT hurdle), n=975 signals, 54.26% session coverage. Not a close call — 9% of the required bar. Route ① stays open in principle ([`ADR 2026-08-10`](../../docs/adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md)); this specific causal story (volatility-threshold entry, stop/target sized off the trigger bar's own range) does not supply a candidate through it. Re-proposal bar: a structurally different criterion, not a re-tuned θ/lookback/stop-target on this shape. [`FREEZE`](../../lab/archive/todvol_1_2026-08-20/FREEZE.md) · [`RESULTS`](../../lab/archive/todvol_1_2026-08-20/RESULTS.md).

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
