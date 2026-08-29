# RESULTS — MNQ Notice-phase 5-candidate bars-only geometry screen (2026-08-29)

**Manifest:** [`discovery_manifests/mnq_dailygeom_notice_20260829.json`](../../../../discovery_manifests/mnq_dailygeom_notice_20260829.json) — `--lane blind`, K=5, registered (Rule 1: K declared before any result examined), closed same session.
**Panel:** `core/data/bar_data/MNQ_M15.csv` (BAR EXPORT v0.2, `CME_MINI:MNQ1!`), n=141,541 bars post-dedup, 2020-07-01→2026-07-03Z. RTH = [09:30,16:00) ET (this repo's own standing convention, `mnq_tnec_con4_pdh_pdl_break_2026-08/construct_lib.py`). Trading-day cutover = 18:00 ET (CME Globex-day convention) — see `data_lib.py` docstring for why this needs no explicit weekend filter, unlike the databento `ohlcv-1d` daily panels (MNQ.md W2).
**Scripts:** `data_lib.py` (shared), `candidate{1..5}_*.py`, raw output in `candidate{1..5}_results.json` + `diagnostics_MNQ_*.json`.

## Candidate 1 — daily-range-state-persistence (full trading-day TR)

Real observation (uncorrected): gateHit `P(TR_{d+1} elevated | TR_d top quintile)` = **0.6867** (n_cond=332/n_scored=1497), CI [0.608, 0.753] (circular block-bootstrap, block=60, seed=42), halves 0.663/0.711 — both comfortably above GC's 0.5299 and CL's 0.6282 under the same frozen pipeline shape.

Corrected battery (`docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md`), MNQ run as a new leaf (X_code=3, disjoint from every burned GC/CL seed block):
- L1 (n-floor) **PASS**, L2 (CI lb>0.50) **PASS**, L3 (halves) **PASS**.
- L4 (by-year floor, N_valid≥7 else AMBIGUOUS): only 6 calendar years clear n_cond≥20 (2020 is a partial year, n_cond=6) → **AMBIGUOUS**. This panel's span is structurally short of what L4 needs to resolve, independent of anything about MNQ's edge.
- L5 (IAAFT attribution): diagnostic gate **FAILED** at iter=100 (Spearman-ACF mismatch med=0.0511 > 0.04 limit, p95=0.0707 = the limit) and again, byte-identically, at the ladder's iter=500 step (confirms this is a real structural ACF mismatch, not an IAAFT convergence issue — the reference implementation's own note that "100 vs 1000 iterations are bit-identical" reproduces here too). The final ladder step (Schreiber end-matching trim, ≤2% of record) found no offset improving the wraparound discontinuity (best_k=0). **Escalation ladder exhausted → VOID per spec §3 CASE V.** No p_upper/p_lower may be quoted.

**Net: HOLD, not GRADUATE and not DROP.** A real, striking raw effect that the frozen battery cannot currently certify on this panel — not because it's null, but because (a) the panel is too short for L4 to resolve and (b) MNQ's own TR series doesn't fit the IAAFT tolerance band calibrated on GC/CL. Forward work is explicit in the spec itself: a longer panel (discharges L4) or a fresh surrogate class, e.g. ARFIMA/FGN or GARCH-fitted (spec's own pre-named O5 remedy for L5) — neither is in scope for a Notice-phase session.

## Candidate 2 — overnight-range → RTH-range, SAME trading day

**Re-framing found during grounding (not assumed from the handoff):** this is cross-series (overnight range, RTH range are two different series on the same day), not single-series lag-1 persistence like candidate 1. The frozen battery's own §4 D5 names this exact shape "S2" and says the S1 (candidate-1-style) null does **not** port — independent surrogation of two series sharing a slow common vol state deletes the very confound under test. D5's un-pause path requires a stage-1 **$0 cheap falsifier** first: does overnight-state conditioning beat matched day-session-history conditioning on the same days? Ran that, not the IAAFT battery.

Naive: P(y=1|overnight-bias=1) = **0.9263** (n=339) vs P(y=1|dayhist-bias=1) = 0.6796 (n=334); unconditional base rate 0.5087. Stratified on yesterday's own RTH-range state (bias′): overnight range still lifts the conditional rate by **+57.7pp** (bias′=0 stratum, n=213/940) and **+38.7pp** (bias′=1 stratum, n=126/208) — i.e. overnight range is not a proxy for yesterday's regime; it carries large same-day incremental information. Block-bootstrap (day-blocks, block=20, 4000 draws) on the minimum stratified lift: mean 0.386, CI [0.300, 0.473], p(lift≤0) < 0.00025.

**D5 stage-1 falsifier CLEARS decisively.** Per D5, this licenses proceeding to stage 2 (a joint-surrogation null design + adversarial review + operator GO) — not a naive independent-IAAFT battery, and not a deploy-ready finding on its own.

## Candidate 3 — bar-volume regime → next-bar conditioning (M15)

Two outcomes tested, both ToD-matched (causal per-time-of-day-slot trailing reference, mirroring `tod-baseline-range-trigger`'s design to remove the deterministic intraday volume-seasonality confound — the fresh null-validity citation this candidate needed) alongside a naive pooled version disclosed for comparison:

- **Directional continuation: clean NULL.** Naive lift +0.5pp, ToD-matched lift +0.01pp (n≈134k). No effect either way.
- **Next-bar range elevation: real.** Naive pooled lift +28.9pp (obs 0.803 vs base 0.514) — as predicted, heavily ToD-confounded. ToD-matched: obs **0.684** vs base 0.503, lift **+18.1pp**, CI [0.673, 0.695] (n_cond=70,545/n_scored=136,020).
- **Incremental check (not in the original framing, run to test whether "volume" is just a range-autocorrelation proxy):** own-range→own-range persistence (ToD-matched) gives an almost identical point estimate (0.686) to volume→range — same-bar Spearman(volume, range) = 0.88. But stratifying on the trigger bar's own range state, volume still adds **+20.6pp** (low-range stratum) and **+25.6pp** (high-range stratum) of incremental lift. Volume is not redundant with range; it is a distinct, incrementally informative signal, though very plausibly the same underlying activity/volatility-clustering phenomenon as candidate 1, observed at a finer grain and via a different proxy — not a demonstrated distinct WHO.

## Candidate 4 — unsigned gap magnitude → RTH-range conditioning

Same cross-series (S2-shaped) re-framing as candidate 2 — gap magnitude and RTH range are different series on the same day. Ran the identical D5 stage-1 $0 falsifier design.

Naive: P(y=1|gap-bias=1) = 0.6636 (n=327) vs P(y=1|dayhist-bias=1) = 0.6796 (n=334) — naive marginals look similar, no lift over day-history in the pooled comparison. But stratified: gap magnitude adds **+17.0pp** (bias′=0, n=209/944) and **+15.5pp** (bias′=1, n=118/216) of incremental lift within day-history strata. Block-bootstrap on min stratified lift: mean 0.137, CI [0.054, 0.212], p(lift≤0) ≈ 0.00225.

**D5 stage-1 falsifier clears**, smaller effect size than candidate 2 (a single jump vs a whole session's realized range is a noisier signal, as expected) but real and well above the noise floor.

## Candidate 5 — bar closing-location (CLV) lag-1 autocorrelation

Fresh null (block-shuffle, block=96≈1 trading day, 2000 perms) — deliberately not the IAAFT battery, since CLV is a bounded ratio, not a heavy-tailed magnitude series (disclosed null-validity argument, not a battery reuse). Full continuous bar sequence, n=141,540 consecutive pairs.

Spearman rho(CLV_t, CLV_{t+1}) = **−0.0301**. Block-shuffle null band [−0.0052, +0.0051] (mean −0.0001, sd 0.0026) — real value sits far outside it, p_lower = 0.0005 (0/2000 permutations at or below observed). Both halves same sign (H1 −0.0385, H2 −0.0219; some attenuation, not a sign flip).

**Real, precisely-measured, but small.** A strong-close bar is followed by a weaker-close bar more often than chance — mean-reverting, not persistent, closing location. Magnitude (rho≈−0.03) is modest; plausibly a microstructure artifact (bid-ask-bounce-adjacent) rather than a directional edge of practical size. Admission-route status under the raised bar is explicitly unresolved (see notice §4) — this is a routing call for the next session, not this one.
