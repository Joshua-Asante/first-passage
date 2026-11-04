# NOTES-M2K — R2 worker notes (2026-11-04, K = 0, no market data read)

Checkout: consults first run at main `9509cf1f`; the raw capture below re-ran at `8745b402` (branch `claude/r2-cell-dossiers`, moved by another session mid-task). `git diff --stat` of `ops/instruments`, `docs/rejected_candidates.md`, `scripts/instrument_profiles.py`, `core/firm_rules.py`, `ops/prop_envelope_default.md` between the two: empty.

## Ranking
1. **r2-m2k-ondrift** (overnight drift, Globex, long-only, Bulenox). Path 1a story partly met (inventory constraint named; payer's own constraint not shown). Outside the domain bar's scope by its own text. Long-only and session-disjoint from ORB-MNQ, so no ESA §6.7 conflict and true session distinctness. Blockers can be answered: δ needs a K=1 extraction probe on M2K's own panel (UNSCREENABLE until then). Severe cost risk: the ES transplant gross (1.48bp) barely exceeds Bulenox commission and is below Tradeify's; Req 5 is deleted, so cost is report-only, but it is the likely killer (H-OD-1's own "micro cliff" forecast).
2. **r2-m2k-imom** (final-half-hour intraday momentum, Tradeify). Screenable on a true Russell-futures cohort (Baltussen ER), but fails Req 4 at the conservative haircut (power 0.15; 0.32 even at the 32% haircut). The domain bar binds and no route clears (D5 is a basis closure; "a different index is the exhausted move"). The repo's MNQ sibling sign-reversed OOS. Forced long-only by §6.7 because ORB-MNQ is long into the close, which halves N. Weak diversification against ORB.

## Sources opened, with verbatim support
- SR917 — Boyarchenko, Larsen, Whelan, *The Overnight Drift*, FRBNY Staff Report 917 (Feb 2020, rev. Aug 2022), https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr917.pdf, accessed 2026-11-04 (pdftotext of the PDF):
  - "the largest positive returns are between [time elided] and [time elided] - the opening of European markets in U.S. Eastern Time terms (ET) - averaging 3.7% on an annualized basis (1.48 basis points per day)." (literature fact; not a card setting)
  - "they are positive in 20 out of 23 years since 1998 and statistically significant in 17 of these."
  - Abstract: "Consistent with models of inventory risk, we demonstrate a strong relationship with order imbalances at the close of the preceding U.S. trading day."
  - Sample: "Our sample period spans January 5, 1998" … (to Dec 2020). Full-text grep for Russell/small-cap/RTY: no hits → no Russell cohort. Published version: RFS 36(9) 2023, 3502–3547 (econpapers listing, search result only).
- Baltussen, Da, Lammers, Martens, "Hedging demand and market intraday momentum", *JFE* 142 (2021) 377–403, https://academicweb.nd.edu/~zda/intramom.pdf (redirect from www3.nd.edu), accessed 2026-11-04:
  - Table A1: "Russell 2000 ICE/CME∗ ER 1993-02-08 2020-05-01 6746 09:30–16:00 USA"; asterisk = "sample period is extended by considering the regular future before the mini contract was introduced."
  - Table B1 Panel B row: "ER 8.17∗∗∗ 2.38 2.21∗∗∗ 7.79∗∗∗ 3.61∗∗∗ 12.27∗∗ 3.91 3.33∗∗∗ 6.00∗∗∗ 3.35 3.15∗∗∗" with t-stats "(4.62) (4.54) (3.15) (2.17) (5.86)"; columns βONFH, R², R²OOS, βrONFH, βM, βSLH, R², R²OOS, βROD, R², R²OOS; "Newey and West (1986) robust t-statistics"; "Adjusted R2, R2OOS, and slope coefficients are multiplied by 100."
  - Mechanism: "market makers of index products such as LETFs have little choice but to hedge at the end of the day."
  - Arithmetic: 4.62/√6746 = 0.0562; 5.86/√6746 = 0.0713; √0.0238 = 0.154; √0.0335 = 0.183.
- Gao, Han, Li, Zhou, "Intraday Momentum: The First Half-Hour Return Predicts the Last Half-Hour Return", working paper, "Current Version: December, 2015" (JFE 129(2) 2018, 394–414), https://c.mql5.com/forextsd/forum/173/intraday_momentum_-_the_first_half-hour_return_predicts_the_last_half-hour_return.pdf, accessed 2026-11-04:
  - Table 11: "IWM iShares Russell 2000 ETF 05/26/2000"; Table 12: "The sample period for each ETF is from its inception date to December 31, 2013".
  - Table 12 Panel A row: "IWM 11.72∗∗∗ 7.70 2.51 2.43 11.72" with "(5.18)" (Avg Ret %, Std Dev %, INS R², OOS R², CER; annualized).
  - Arithmetic: 11.72/252 = 0.0465% ≈ 4.65bp/day; Sharpe/day 11.72/7.70/√252 = 0.096.
- McLean & Pontiff, "Does Academic Research Destroy Stock Return Predictability?", *JF* 71(1) 2016, 5–32, https://Www.Gwern.net/doc/economics/2016-mclean.pdf, accessed 2026-11-04: "Portfolio returns are 26% lower out-of-sample and 58% lower post-publication. … We estimate a 32% (58%–26%) lower return from publication-informed trading."
- LSEG / FTSE Russell press release 2026-05-22, https://www.lseg.com/en/media-centre/press-releases/ftse-russell/2026/ftse-russell-begins-june-2026-semi-annual-russell-us-indexes-reconstitution, accessed 2026-11-04: "the reconstitution of the Russell US Indexes will again be held semi-annually in June and December"; "Changes from the June 2026 reconstitution will take effect after US equity markets close on Friday, June 26."
- MFFU article 9735811, https://help.myfundedfutures.com/en/articles/9735811, accessed 2026-11-04 (WebFetch summary, dated "August 24, 2026"): M2K "Total Cost Round Trip" "$1.90"; RTY "$4.68".
- BluSky 17115915, https://help.blusky.pro/en/articles/17115915-markets-symbols-commissions, accessed 2026-11-04 (dated "September 23, 2026"): M2K row "M2K | Micro E-mini Russell 2000 | CME | $0.36 | $0.19 | $0.64 | $0.84 | $0.94"; "Micros: $0.50/side" (Rithmic & Volumetrica / Tradesea evaluation); "Availability on a specific BluSky account may differ". Column headings not returned by the fetch: I read the last three as the NT lifetime/monthly/free per-side tiers by analogy with the envelope §4 MNQ row; unverified.
- Opened, no relevant figure: Glasserman et al. arXiv 2507.04481 (S&P 500 firms only); Terstegge 2025 "Intermediary Option Pricing" (option risk premium; no Russell futures).

## Repo-held facts used (not re-verified on the web)
- Tradeify M2K $1.82 RT: `core/firm_rules.py:241` (article 10468315, 2026-07-13). Equity Index group includes RTY/M2K: firm_rules.py:258; envelope §4a.
- Bulenox M2K 0.61/side: `core/firm_rules.py:102` (Sept-2024 PDF). The Aug-2026 PDF re-check (envelope §4, register §F) restates MNQ/MYM/MES 0.61 only.
- Tradeify flat-by, news, hedging, bots, native route: venue-fact register §I.2 (2026-11-01); deep-dive item 5 (ESA §6.7(c),(i)).
- ORB-MNQ long-only: MNQ.md 2026-08-25 entry ("Confirmed baseline … long-only, 15m"; informal lane) and the c1 editions per firm_rules.py:258. Current native edition's direction: not verified.
- Cost conversion at 1,897.20: M2K.md M2 (2019–2024 panel median). The dev panel's median is unknown at K=0.

## Alternatives considered and rejected
- **Russell reconstitution flow** (named payer: index trackers, a true 1a constraint). Events: annual until 2025, semi-annual from 2026 (LSEG above). About 7–8 events over the 2019-05 → 2026-11 window; power is hopeless at any plausible δ/σ (Req 4: monthly is "presumptively dead"; this is rarer). Rejected.
- **Turn-of-month on Russell:** monthly; Req 4 precedent (D3, D7); SPX500 TOM class finding hard-absent. Rejected.
- **Compression-gated / PDH-PDL breakout (RTH):** no named payer, no Russell cohort, 1b not shown; domain bar binds with no route; MNQ siblings AMBIGUOUS-HOLD. UNSCREENABLE with no cheaper probe than mining. Rejected.
- **ES→RTY lead-lag (small caps lag large caps):** futures arbitrage compresses it to seconds; not closed-bar expressible. Rejected.
- **Order-flow → Russell response** (M2K.md ACTIVE: "cheapest re-open is free: a published cohort δ for aggressor-signed flow"): I found no such cohort in this pass and did not search deeply. Left open.

## Could not verify
- Bulenox: native NinjaScript automation on Rithmic (beyond "Rithmic third-party API $100/month"); whether a position may be opened after the Globex reopen and closed before 15:59 CT; current M2K rate; Bulenox's own hedging rule.
- Russell LETF AUM / gamma share (Baltussen's Russell-specific LETF regression row not read).
- arXiv 2605.04004 (repo-cited MNQ falsification): not opened.
- McLean-Pontiff is a cross-sectional-anomaly haircut applied to a time-series timing effect; a convention borrowed from strategy_harvest §4, not a measured decay for this effect.
- Discrepancy: rejected_candidates.md :132 "MSL-C3-K2 … K=2" vs M2K.md session log "K spent=0", and no M2K manifest exists.

## Raw consult output (verbatim, with exit codes)
```text
$ python3 -I scripts/fp.py python scripts/instrument_profiles.py cell M2K intraday-momentum
=== M2K x intraday-momentum ===
ledger: ops/instruments/M2K.md
verdict: untested — no prior on this cell.
class finding (mechanism-wide, not specific to M2K): Baltussen-class intraday momentum is statistically ABSENT on modern MNQ — the cost-geometry thesis was real (hurdle fell 11.06→3.01 bp) but the OOS edge decayed negative (gross Sharpe +0.88→−0.13), corroborating the published post-2021 decay and an external 14-signal-family falsification (arXiv 2605.04004). [NQ.md N3](NQ.md)
BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21 -> ../../docs/rejected_candidates.md
cost hurdle: 11.89 bp/round-trip (panel-era median 1,897.20 => 11.89 bp/RT (recomputed 2026-07-28; supersedes illustrative index-2300 figure and withdrawn 10-30x margin claim). WARN Multiplier basis PENDING — 4x hurdle was Tradeify; venue de-scoped 2026-08-04; F3 ruled 2026-08-07 (no successor venue; Tradeify_Select_100K remains the environment for new strategies — docs/adr/2026-08-07-loop-s1-environment-ratification.md); friendly-firm per-side $0.50-$0.95; re-price against elected venue before this row gates anything if a future deployment lands outside Tradeify.) — VERIFY at #M2
K bank: read ../../discovery_manifests/ — never trust a snapshot.
prior: Cross-index RV selection over ES/NQ/YM/RTY is strictly dominated by single-instrument ORB-MNQ - index aggregation compresses the idiosyncratic dispersion that makes Stocks-in-Play work. An RTY intraday pull is a DEFER-procurement trigger with an explicitly poor prior. [#M3]
prior: Opening-range momentum is an equity-index property (it fades on Treasuries) - so equity-index instruments are where directional structure plausibly lives, but that same tie means cost-viability and decorrelation-from-the-book are in tension by construction. [#M4]
exit=1

$ python3 -I scripts/fp.py python scripts/instrument_profiles.py cell M2K overnight-drift-intermediary-inventory
FATAL: unknown mechanism 'overnight-drift-intermediary-inventory'. Declare it NEW in MECHANISMS.md.
exit=2

$ python3 -I scripts/fp.py python scripts/instrument_profiles.py cell M2K ict-liquidity
=== M2K x ict-liquidity ===
ledger: ops/instruments/M2K.md
verdict: untested — no prior on this cell.
class finding (mechanism-wide, not specific to M2K): Sweep→same-direction-FVG→opposing-pool-draw direction is real on SPX500 (block-permutation p=0.0144) but fails robustness (drop-top-3 = −0.152R, 95% block-CI straddles 0). [SPX500.md D2](SPX500.md)
class finding (mechanism-wide, not specific to M2K): — CORRECTED 2026-08-04; supersedes the former "the 1M 0%-fill wall is feed-general" clause, which is REFUTED. The archived closure attributed US500's **0 fills in 247 attempts** to an instrument-general *price law* — "displacement FVGs continue rather than retrace within 6 bars" — and predicted recurrence on "NAS100 or any fast 1m index". **That law is false on native micro data.** MNQ retraces to FVG mid within the frozen `retraceK=6` **59.06%** of the time (n=128,089; 58–60% in *every* year 2019–2026, including the 2020 crash and 2022 bear), and ES **59.88%** (n=124,748). Every escape route is refuted at 45×+ the ≤1.2% rate that 0-of-247 requires: raid-conditioning leaves it at **59.01%**, the arm-delay curve is nearly flat (**55.91%** even armed 8 bars late — mid-touches recur, they are not one-shot), and ES retraced **62.33%** in the *exact* 2026-06-24→26 window that produced the 0/247. **0/247 was platform-side by elimination** — the deployed (now lost) script, TV's strategy-tester fill handling, or the retired Pepperstone US500 CFD feed; not further separable, and recorded as a residual, never as "bug X". **Consequence for this class:** do **not** cite "1m FVGs don't retrace" against an execution layer on any instrument; **do** require any such design to demonstrate fills on native data rather than trusting TV-tester fill behavior. [MNQ.md W3](MNQ.md) · [`RESULTS_1M_DIAG.md`](../../lab/analysis/_inbox/ict_mnq_2026-08/RESULTS_1M_DIAG.md)
class finding (mechanism-wide, not specific to M2K): **Liquidity pools are anti-attractors**, replicated on three independent instruments — old highs/lows are swept far *less* often than a radius-matched MC null, on every side measured (US500 0.55/0.34 vs base 0.76/0.61; NQ 0.5401/0.3128 vs 0.7756/0.6014; MNQ 0.5303/0.3397 vs 0.8020/0.6502). Any construct keying on "price is drawn to old highs/lows" argues against three panels. The companion **bear-FVG draw** is the real positive of this class (NQ 0.8630 vs base 0.7494, RESOLVED). [MNQ.md N9](MNQ.md) · [`RESULTS.md`](../../lab/analysis/_inbox/ict_mnq_2026-08/RESULTS.md) §3
BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21 -> ../../docs/rejected_candidates.md
cost hurdle: 11.89 bp/round-trip (panel-era median 1,897.20 => 11.89 bp/RT (recomputed 2026-07-28; supersedes illustrative index-2300 figure and withdrawn 10-30x margin claim). WARN Multiplier basis PENDING — 4x hurdle was Tradeify; venue de-scoped 2026-08-04; F3 ruled 2026-08-07 (no successor venue; Tradeify_Select_100K remains the environment for new strategies — docs/adr/2026-08-07-loop-s1-environment-ratification.md); friendly-firm per-side $0.50-$0.95; re-price against elected venue before this row gates anything if a future deployment lands outside Tradeify.) — VERIFY at #M2
K bank: read ../../discovery_manifests/ — never trust a snapshot.
prior: Cross-index RV selection over ES/NQ/YM/RTY is strictly dominated by single-instrument ORB-MNQ - index aggregation compresses the idiosyncratic dispersion that makes Stocks-in-Play work. An RTY intraday pull is a DEFER-procurement trigger with an explicitly poor prior. [#M3]
prior: Opening-range momentum is an equity-index property (it fades on Treasuries) - so equity-index instruments are where directional structure plausibly lives, but that same tie means cost-viability and decorrelation-from-the-book are in tension by construction. [#M4]
exit=1

$ python3 -I scripts/fp.py python scripts/instrument_profiles.py cell M2K overnight-range-transmission
=== M2K x overnight-range-transmission ===
ledger: ops/instruments/M2K.md
verdict: untested — no prior on this cell.
class finding (mechanism-wide, not specific to M2K): (D5 stage-1 $0 cheap falsifier, MNQ, OFFICIAL): overnight range clears D5's un-pause condition (2) decisively — incremental lift over matched day-history conditioning +57.7pp / +38.7pp across both day-history strata (block-bootstrap p<0.00025, n=1487 scored days). Gap magnitude also clears it on its own (+17.0pp / +15.5pp vs day-history, p≈0.00225) but a same-session joint check (holding overnight-range state fixed) found gap's own increment is **conditional and sign-unstable**: +10.5pp when overnight range is itself NOT elevated (bootstrap p=0.0078 / null-calibrated p=0.00871) but −8.1pp (not significant, bootstrap p=0.998 / null-calibrated p=0.997 for the positive direction) when overnight range is already elevated — gap does not add information once overnight range is known to be hot. Recalibration does not overturn the nested-gap finding. Parent-Q convention: overnight range is the primary falsifiable claim; gap magnitude is a forked, nested sub-question scoped to the overnight-calm regime only, not a co-equal claim. Stage 2 (joint-surrogation null design solving D5's O1 item, adversarial review, operator GO) is **owed, not yet run, on either instrument** — this class finding is a stage-1 result only, not a certified verdict under the corrected battery. [MNQ.md](MNQ.md) · [`Q-RANGEXFER-1`](../../docs/briefs/Q-RANGEXFER-1-overnight-range-gap-magnitude-transfer.md) · [`joint gate script`](../../lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate24_joint_gate.py)
class finding (mechanism-wide, not specific to M2K): (D5 stage-1 $0 cheap falsifier, MYM, amended in 2026-08-30 under this same Q-brief — see below): overnight range's own min-stratified lift +21.9pp (block-bootstrap p=0.00025, n=1,307 scored days across two day-history strata), gap magnitude's own +5.9pp pooled (AMBIGUOUS, p=0.1247) — same qualitative relationship to its own sibling as MNQ's pair. Joint gate (`c24_joint_gate.py`, direct port of MNQ's script) replicates the nested structure: gap lift +8.5pp (calm, null-calibrated p=0.020) / −7.2pp (hot, p=0.888) vs. this heading's own MNQ +10.5pp/−8.1pp — same sign, same relative ordering, 10.6%-44.8% smaller in magnitude (not a uniform ratio). Scored independently of MNQ's own verdict (Q-RANGEXFER-1 §6); stage 2 equally owed and not yet run. [MYM.md](MYM.md) · [`N-2026-08-29-mym-overnight-gap-joint-gate.md`](../../docs/notes/notice/N-2026-08-29-mym-overnight-gap-joint-gate.md)
BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21 -> ../../docs/rejected_candidates.md
cost hurdle: 11.89 bp/round-trip (panel-era median 1,897.20 => 11.89 bp/RT (recomputed 2026-07-28; supersedes illustrative index-2300 figure and withdrawn 10-30x margin claim). WARN Multiplier basis PENDING — 4x hurdle was Tradeify; venue de-scoped 2026-08-04; F3 ruled 2026-08-07 (no successor venue; Tradeify_Select_100K remains the environment for new strategies — docs/adr/2026-08-07-loop-s1-environment-ratification.md); friendly-firm per-side $0.50-$0.95; re-price against elected venue before this row gates anything if a future deployment lands outside Tradeify.) — VERIFY at #M2
K bank: read ../../discovery_manifests/ — never trust a snapshot.
prior: Cross-index RV selection over ES/NQ/YM/RTY is strictly dominated by single-instrument ORB-MNQ - index aggregation compresses the idiosyncratic dispersion that makes Stocks-in-Play work. An RTY intraday pull is a DEFER-procurement trigger with an explicitly poor prior. [#M3]
prior: Opening-range momentum is an equity-index property (it fades on Treasuries) - so equity-index instruments are where directional structure plausibly lives, but that same tie means cost-viability and decorrelation-from-the-book are in tension by construction. [#M4]
exit=1

$ python3 -I scripts/fp.py python scripts/instrument_profiles.py cell M2K overnight-range-failed-extension-fade
=== M2K x overnight-range-failed-extension-fade ===
ledger: ops/instruments/M2K.md
verdict: DEAD (2026-08-13)
  source: ../../docs/briefs/closures/MSL-C3-K2-closure-falsified.md
  BLOCKING — the re-proposal bar below must be met and addressed in the pre-registration.
class finding (mechanism-wide, not specific to M2K): M2K explore **FALSIFIED 2026-08-13** (Axis B both-arms IS 95% CI entirely &lt; 0; long n=359 CI [−0.220, −0.021]; short n=378 CI [−0.204, −0.014]; pooled −0.114R). CONFIRM unread. [closure](../../docs/briefs/closures/MSL-C3-K2-closure-falsified.md) · [RESULTS](../../lab/archive/msl_c3_m2k_2026-08/RESULTS_g2.md).
BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21 -> ../../docs/rejected_candidates.md
cost hurdle: 11.89 bp/round-trip (panel-era median 1,897.20 => 11.89 bp/RT (recomputed 2026-07-28; supersedes illustrative index-2300 figure and withdrawn 10-30x margin claim). WARN Multiplier basis PENDING — 4x hurdle was Tradeify; venue de-scoped 2026-08-04; F3 ruled 2026-08-07 (no successor venue; Tradeify_Select_100K remains the environment for new strategies — docs/adr/2026-08-07-loop-s1-environment-ratification.md); friendly-firm per-side $0.50-$0.95; re-price against elected venue before this row gates anything if a future deployment lands outside Tradeify.) — VERIFY at #M2
K bank: read ../../discovery_manifests/ — never trust a snapshot.
prior: Cross-index RV selection over ES/NQ/YM/RTY is strictly dominated by single-instrument ORB-MNQ - index aggregation compresses the idiosyncratic dispersion that makes Stocks-in-Play work. An RTY intraday pull is a DEFER-procurement trigger with an explicitly poor prior. [#M3]
prior: Opening-range momentum is an equity-index property (it fades on Treasuries) - so equity-index instruments are where directional structure plausibly lives, but that same tie means cost-viability and decorrelation-from-the-book are in tension by construction. [#M4]
exit=1

$ python3 -I scripts/fp.py python scripts/instrument_profiles.py cell M2K pdh-pdl-failed-break-reclaim
=== M2K x pdh-pdl-failed-break-reclaim ===
ledger: ops/instruments/M2K.md
verdict: DEAD (2026-08-13)
  source: ../../docs/briefs/closures/MSL-C3-K2-closure-falsified.md
  BLOCKING — the re-proposal bar below must be met and addressed in the pre-registration.
class finding (mechanism-wide, not specific to M2K): MYM explore **FALSIFIED** (both-arms CI &lt; 0) — [C1 RESULTS](../../lab/archive/msl_c1_mym_2026-08/RESULTS_g2.md) · [closure](../../docs/briefs/closures/MSL-C1-closure-falsified.md). M2K unpaid path [OPERATOR-KILL](../../docs/briefs/closures/MSL-C3-closure-operator-kill.md) (B4 declined; class not killed at C3). **M2K dual-axis explore FALSIFIED 2026-08-13** (Axis A both-arms IS 95% CI entirely &lt; 0; long n=293 CI [−0.256, −0.038]; short n=295 CI [−0.307, −0.089]; pooled −0.171R) — [closure](../../docs/briefs/closures/MSL-C3-K2-closure-falsified.md) · [RESULTS](../../lab/archive/msl_c3_m2k_2026-08/RESULTS_g2.md). Does not clear or reopen the MYM explore kill.
BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21 -> ../../docs/rejected_candidates.md
cost hurdle: 11.89 bp/round-trip (panel-era median 1,897.20 => 11.89 bp/RT (recomputed 2026-07-28; supersedes illustrative index-2300 figure and withdrawn 10-30x margin claim). WARN Multiplier basis PENDING — 4x hurdle was Tradeify; venue de-scoped 2026-08-04; F3 ruled 2026-08-07 (no successor venue; Tradeify_Select_100K remains the environment for new strategies — docs/adr/2026-08-07-loop-s1-environment-ratification.md); friendly-firm per-side $0.50-$0.95; re-price against elected venue before this row gates anything if a future deployment lands outside Tradeify.) — VERIFY at #M2
K bank: read ../../discovery_manifests/ — never trust a snapshot.
prior: Cross-index RV selection over ES/NQ/YM/RTY is strictly dominated by single-instrument ORB-MNQ - index aggregation compresses the idiosyncratic dispersion that makes Stocks-in-Play work. An RTY intraday pull is a DEFER-procurement trigger with an explicitly poor prior. [#M3]
prior: Opening-range momentum is an equity-index property (it fades on Treasuries) - so equity-index instruments are where directional structure plausibly lives, but that same tie means cost-viability and decorrelation-from-the-book are in tension by construction. [#M4]
exit=1

```
