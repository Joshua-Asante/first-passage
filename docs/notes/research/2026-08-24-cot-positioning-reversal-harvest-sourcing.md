# COT/TFF positioning-extreme reversal — harvest sourcing pass (literature-only, $0/K=0)

**Date:** 2026-08-24
**Type:** Harvest sourcing note (`strategy_harvest.md` §2.3 rank-1/2/3 literature channels) — not a Pre-Q,
not a pre-registration, not a `register_search open`.
**Context:** one of three literature-sourced candidates scanned this session from a public-strategy
source list (futures.io/Reddit/GitHub/books/papers/TradingView-class sources), reweighted against this
repo's own ranked channel portfolio. Siblings: closing-auction/MOC-imbalance (superseded same day by
live Phase-B Lane B1 work on `claude/phase-b-mechanism-supply-b1-b2`) and cross-sectional futures carry
ranking (staged separately, `needs-delta-extraction-probe`).
**Disposition:** **DROP — unscreenable-drop.** No manifest opened, no `register_search`, no K spent, no
data pulled.

---

## Mechanism

Hedging-pressure theory (Bessembinder 1992; De Roon, Nijman & Veld 2000; Kang, Rouwenhorst & Tang 2020)
frames non-commercial/speculator net positioning as the liquidity-providing counterpart to hedgers'
risk-transfer demand: when speculator positioning reaches a historical extreme, theory predicts a
subsequent price move against the crowded side as the position normalizes. This is a real, multi-decade,
top-journal literature (1992–2020) — but not a clean, unanimous result. Wang (2003, *Journal of Futures
Markets*) finds noncommercial/speculator sentiment extremes behave as a **continuation** (momentum)
indicator, not a reversal one — it is **commercial/hedger** sentiment extremes that behave contrarian in
that paper, directly complicating the "speculator extremes revert" framing this candidate assumed.

## Why it fails, in order

1. **Shape (decisive; venue-native, not literature-derived).** Predicted payoff: symmetric, ~40–50% win
   rate, possibly sub-coin-flip, with no a-priori reason for mean-win > mean-loss — a contrarian entry
   into a persistent positioning extreme risks being stopped out just before the eventual reversal (the
   mirror-image risk of the low-win-rate trend shapes this venue's own shape-feasibility map already
   excludes). The map's 630-cell sweep
   ([`shape_feasibility_map_2026-08/RESULTS.md`](../../../lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md))
   found **no cell at win_rate ≤50% is FEASIBLE** (bust ≤3.0% AND P(pass) ≥50%) for any shape, cadence, or
   per-trade risk level tested — this candidate's predicted shape sits 15–30 points inside that dead
   zone. Because the shape is a structural property of the mechanism (fighting a persistent extreme, not
   a measurement artifact), a real-panel pull would very likely confirm rather than rescue it.
2. **Power (independently sufficient).** Realistic independent event count, once multi-week
   autocorrelation/persistence of positioning extremes is accounted for (not the raw 52 weekly
   releases/yr), estimated at roughly 20–160 events per instrument over the ~20yr TFF-disaggregated era
   (2006–2026) — the same low-N regime that killed H-TSMOM-1 (N≈86, power 0.34). The one usable
   literature figure (Dreesmann, Herberger & Charifzadeh 2023, best-of-6-of-many-markets Sharpe
   1.24–2.09, portfolio-level aggregation **fails**) implies a weekly δ/σ of roughly 0.17–0.29 —
   below this program's own applied floor (0.35–0.65 at N<150) across nearly the entire plausible N
   range.
3. **Cost-law.** Never reached (moot) — no paper supplies a citable per-event $/bp delta at
   daily-or-better resolution; every effect size found is a gross, strategy-level, continuously-rebalanced
   figure, not a discrete extreme-only entry.

## Citations

Primary-source hosts (SSRN, JSTOR, several publisher pages) were egress-blocked this session; findings
below are WebSearch-synthesized secondary summaries, not independently verified full-text quotations —
re-verify before any load-bearing use.

| Citation | Venue / year | Finding |
|---|---|---|
| Bessembinder (1992) | Rev. Financial Studies | Hedging-pressure predicts returns for currency/agricultural/mineral futures; "relatively trivial" for interest-rate futures. |
| De Roon, Nijman & Veld (2000) | Journal of Finance | Own- and cross-market hedging pressure significant across 20 futures markets, 4 groups; survives price-pressure controls. |
| Wang (2003) | Journal of Futures Markets | Sign-direction complication: noncommercial/speculator extremes are a *continuation* indicator; commercial/hedger extremes are the contrarian one. |
| Sanders, Irwin & Merrin (2009) | J. Agricultural & Resource Economics | Null result — Granger-causality finds "very little evidence" positions forecast returns, 10 agricultural futures markets. |
| Chen & Maher (2013) | J. Int'l Financial Markets, Institutions & Money | Null result — position-based sentiment signals "do not produce significant average returns," S&P 500 futures (this program's MES/M2K family). |
| Kang, Rouwenhorst & Tang (2020) | Journal of Finance | Strongest modern support: short-term (liquidity-driven, mean-reverting) vs. long-term (hedging-demand-driven) position-change components carry opposite-signed return implications — specific to commodities. |
| Dreesmann, Herberger & Charifzadeh (2023) | Int'l J. Financial Markets and Derivatives | Weekly-COT-index long-only reversal rule significant (Sharpe 1.24–2.09) in 6 of many US futures markets tested; fails to survive portfolio-level (multi-market) aggregation — a multiplicity flag this program's own doctrine treats as disqualifying. |
| Cheng, Kirilenko & Xiong (2015) | Review of Finance | Positioning-driven reversal is crisis-conditional (VIX-shock-state-dependent), not an always-on weekly rule. |

## Dedup — corrected after adversarial review

The first-pass dedup check (run against a summary of this program's dead-class ledger) reported
"clear." An adversarial cross-check caught what it missed; re-verified directly against the repo this
session:

- **`H-COTREV-6A`** — CFTC-COT positioning-extreme reversal on AUD, dispositioned **UNSCREENABLE
  (Requirement 2)** 2026-08-16
  ([`lab/analysis/harvest/radar_tier_a_burst_2026-07/CANDIDATE_ROWS.md`](../../../lab/analysis/harvest/radar_tier_a_burst_2026-07/CANDIDATE_ROWS.md)).
  Same mechanism family, the identical Wang-2003 sign-direction caution, the identical missing-citable-δ
  defect (sourced from Wang 2003/2004 and Klitgaard & Weir 2004). Not a strict duplicate — different
  instrument (AUD/M6A, absent from this candidate's 9-instrument menu) and a broader citation set — but
  this candidate does **not** take H-COTREV-6A's own prescribed recovery path (switch to a hedger-
  sentiment, not speculator-extreme, specification) despite citing the same Wang caution that motivated
  it.
- **`Q-ORBPOS-1`** — closed `FALSIFIED` 2026-08-23
  ([closure](../../briefs/closures/Q-ORBPOS-1-closure-falsified.md)) — a diagnostic question about one
  dated MNQ regime break (2021-09-28), not a strategy-candidate proposal, correctly carrying no
  registry row per its own §8 convention. Third independent trailing-classifier null against that break:
  CFTC TFF Leveraged-Funds positioning-extremity failed to date-correlate at 0-of-3 pre-registered
  windows and its gate-clearance direction sign-flipped between windows. Reinforcing, not colliding — a
  third, MNQ-specific data point that CFTC positioning classifiers don't correlate cleanly with real
  price patterns in this program's own panels.
- **`MNQBASE-1-closure-intake-dry.md`** §2.1 — the CFTC COT/TFF channel (rank 4 of `strategy_harvest.md`
  §2.3's ranked channel portfolio) was already scored dead via inheritance from the forced-flow census
  (P4-2): *"weekly density, cross-sectional δ — dead."*

## Verdict

`unscreenable-drop`, K_intrinsic = 0. Logged as a sourced-but-not-viable Tier-A mechanism class per its
own genuine, citable literature — not a fabricated mechanism, just wrong-shaped and power-starved for
this venue at weekly cadence, and now the third occurrence of the class in this program's own ledger
(H-COTREV-6A, Q-ORBPOS-1, this pass). If a future session wants to keep chasing this mechanism family,
the only route that isn't a rehash: a higher-frequency (intraday/daily) crowding proxy, the
hedger-sentiment (not speculator-extreme) specification, and a demonstrably right-skewed rather than
symmetric predicted payoff — none of which this pass, H-COTREV-6A, or Q-ORBPOS-1 evaluated.

**Registry:** [`docs/rejected_candidates.md`](../../rejected_candidates.md), entry
*"COT/TFF positioning-extreme reversal (hedging-pressure contrarian signal)."*
