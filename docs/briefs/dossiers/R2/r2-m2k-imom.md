# r2-m2k-imom: M2K × intraday-momentum × Tradeify

Status: R2 dossier (Part A §A2–§A3, tasks T2–T3) · 2026-11-04 · K = 0 (no data read) · decides nothing; generation never blesses (Rule 25)

## Cell
- Instrument: M2K (CME Micro E-mini Russell 2000) · Mechanism: `intraday-momentum` (existing) · Provisional firm: Tradeify (D10 proposed mapping, not decided) · Session: US cash session, final half-hour, signed by the return earlier in the day; flat by the cash close.
- Event frequency: every session if two-sided (cohort); about half the sessions if forced long-only by the hedging rule (see Venue legality; share not measured, K=0). Early-close days lose the window (Tradeify holiday flat-by 12:59 ET).

## Mechanism (harvest Req 1, path 1a)
- WHO pays: short-gamma hedgers who must trade with the day's move before the close: leveraged-ETF rebalancers (daily leverage reset is a mandate) and options market makers (delta-hedging requirement). Baltussen et al. 2021: "market makers of index products such as LETFs have little choice but to hedge at the end of the day." Clause (i) met in the source. Russell-specific LETF/gamma share: not verified this session.
- WHEN: final half-hour of the cash session, signal from the earlier return; declared by the cohort. Met.
- WHY it persists: hedging demand is mandate-inelastic; capacity limited by end-of-day liquidity. Weak: the published decay (below) says arbitrage or regime change has eroded it.
- HOW it dies: Russell LETF AUM and dealer net gamma shrink, or the predictive slope turns ≤ 0. Observable: LETF market cap (Baltussen's "IndexingLETF" measure), dealer gamma estimates.

## Effect priors (Req 2)
| Source (date accessed) | Cohort | Figure | Transplant? |
|---|---|---|---|
| Baltussen, Da, Lammers & Martens 2021, *JFE* 142(1):377–403, https://academicweb.nd.edu/~zda/intramom.pdf (2026-11-04) | **Russell 2000 futures (Tickdata "ER", ICE/CME, regular contract before the mini), 1993-02-08 → 2020-05-01, 6,746 obs** (Table A1) | Table B1 Panel B, row ER: β(rONFH) 8.17, t = 4.62, R² 2.38%; β(rROD) 6.00, t = 5.86, R² 3.35% (Newey-West t) | No — target index futures (parent-scale contract, not M2K micro) |
| Gao, Han, Li & Zhou, working paper Dec 2015 (published *JFE* 129(2) 2018), https://c.mql5.com/forextsd/forum/173/intraday_momentum_-_the_first_half-hour_return_predicts_the_last_half-hour_return.pdf (2026-11-04) | IWM ETF, 2000-05-26 → 2013-12-31 (Table 12) | r1 timing: Avg Ret 11.72% p.a. (t 5.18), Std 7.70%, INS R² 2.51%, OOS R² 2.43% | Same index, ETF vehicle (labelled; not used as screen figure) |
| Repo: end-of-day adversity bar (rejected_candidates.md, 2026-08-02, attempt 1) | MNQ | corr(mid-session return, final-block return) = +0.0127, NW t +0.321 | Yes — MNQ; context only |
| Repo: MECHANISMS.md `intraday-momentum` class finding | MNQ | OOS gross Sharpe +0.88 → −0.13 (post-2021 decay) | Yes — MNQ; sign-reversal warning |
- δ/σ derivation (t-scaled, D5 precedent t/√N): rONFH 4.62/√6746 = **0.0562**; rROD 5.86/√6746 = 0.0713. R²-derived would be 0.154 / 0.183 (rejected as optimistic, §4).
- Decay haircut: **58%**, McLean & Pontiff 2016 (*JF* 71(1)): "Portfolio returns are 26% lower out-of-sample and 58% lower post-publication." Full post-publication figure chosen because the dev window is post-publication for both papers and the repo's MNQ sibling shows the sign reversing. 32% (publication-informed share alone) shown as the optimistic bound.
- Screen figure: δ/σ = 0.0562 × 0.42 = **0.024** (rONFH, lowest defensible). Break-even for power 0.50 at N = 1,492: 0.051.

## Prior consult (advisory, Rule 26)
```text
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
```
- Register hits: M2K DEAD cells `pdh-pdl-failed-break-reclaim` and `overnight-range-failed-extension-fade` (MSL-C3-K2, both-arms IS CI < 0; addback "new mechanism evidence — NOT θ-retune"): different mechanism (continuation into close, not fade at a level); disclosed, not binding. D5 (Baltussen intraday momentum on MNQ) closed: Stage-2 cost-law 2026-07-16, then D5-RECOST OOS decayed negative 2026-07-21. M3 (RTY intraday pull poor prior) is about cross-index selection; adjacent only.
- Domain bars: `index-intraday-ohlcv-directional-timing-2026-07-21` **binds** (single liquid US equity-index future, OHLCV only, flat-by-close; M2K.md M1). Route by route: (1) outside {price, cross-instrument selection, hold-time}: **not met** — D5 is one of the bar's four basis closures and the bar says "a different index is the exhausted move"; a LETF-AUM conditioner would be non-OHLCV and a new axis (K), not this cell; (2) modality/venue: no new modality; the D5 wall (4× cost law) was deleted as a rule on 2026-10-24, which is not a venue change; **not met**; (3) beats ORB-MNQ net: no evidence; **not met**. Prior only (Rule 26), but no route is cleared. Also the **end-of-day adversity raised bar (2026-08-02)** is adjacent: its attempt 1 measured the same continuation question on MNQ and found it insignificant.
- Family K bank (Req 3 disclosure): M2K 0 (no manifest mentions M2K/RTY, grep 2026-11-04; MSL-C3-K2 "K=2" vs ledger "K spent=0" unreconciled). NQ/MNQ bank carries D5 (`d5_nq_intraday_mom.json`).

## Venue legality at Tradeify
- Native route: NinjaScript native strategy logic only for evaluation accounts (route record addendum 2026-10-12, AGENTS.md posture) · Product offered: M2K in the Equity Index group, $1.82 RT (core/firm_rules.py:241, article 10468315, verified 2026-07-13) · Flat-by: "4:45 PM ET"; holiday "12:59 PM ET" (10495876, register §I.2, 2026-11-01) · News: "news trading is allowed on all accounts" (12268167) · Hold: intraday only, flat by deadline · Cross-firm hedging / product group: opposing positions in a product group banned "in a single account or … across several of your accounts", extended to External Accounts (10495868; ESA §6.7(c),(i); register §I.2). ORB-MNQ is in market long into the close (repo records long-only expressions: MNQ.md 2026-08-25 entry, firm_rules.py:258 comment; the current native edition's direction is not verified). **A short M2K trade in the final half-hour while ORB-MNQ is long is a breach wherever M2K trades.** So the cell must be long-only, or gated off whenever ORB is long. Bots must be solely owned and exclusive within Tradeify (ESA §6.6).
- Firm choice: D10 default kept. Moving firms does not escape §6.7 (it reaches external accounts) and only adds a second monitoring surface. Consequence at Tradeify: a second strategy at the firm next to ORB, on its own account, Tradeify-exclusive thereafter; the 10-30 "one strategy per firm" reading needs Joshua's ruling.

## Distinctness
- vs index ORB book: same session family (US cash session), different window (final half-hour vs the open) and mechanism (end-of-day hedging continuation vs opening-range breakout). In-market overlap with ORB in the final half-hour is near-certain on ORB days; with long-only, the two are same-direction-correlated, so diversification is weak by construction (M2K.md M4 structure prior).
- vs other R2 dossiers: Same mechanism as r2-mym-intraday-momentum (and D5 on MNQ): not distinct from it; at most one runs. Late-session hold in the ORB book's product group: short side needs sign coordination. Differs from the non-index dossiers in instrument and product group.

## Reach (T3)
- 5f reach (D7, `gates.reachability(k, n)` run 2026-11-04 through the fp launcher; arithmetic only, no data read). Banked builder K on this instrument: **0** on the public record (R1 is MCL-only and unrun; the builder ledger is private, so `ledger.k()` must confirm it at registration). Development sessions n ≈ **1,492**: window 2019-05-06..2026-11-02 ≈ 1,870 sessions by `ops/calendars/cme_holiday_calendar_2016_2026.json` (sha256 `407d93bb815ee6b2…`; weekdays less non-`NORMAL` dates), less D9's 378-session holdout. The pinned export sets the real n.
  | K (banked + this card) | 5f floor (annual SR) | P(pass \| SR 0.85) | P(pass \| SR 0.89) | Reachable (D7) |
  |---|---|---|---|---|
  | 1 (this card) | 0.676 | 0.664 | 0.698 | yes |
  | 2 (the reserve look) | 0.890 | 0.461 | 0.500 | yes, at the boundary |
  | 3 | 1.027 | 0.334 | 0.370 | no |
  Normal approximation; 5f only, so every other gate lowers P(pass). The instrument's lifetime budget is 2 looks (generation note §11).
- Power at expected event count: power = Φ(√N·|δ|/σ − 1.96).
  - Two-sided, N = 1,492: haircut 58% δ/σ 0.024 → Φ(−1.05) = **0.15**; haircut 32% (0.038) → 0.32; unhaircut 0.056 → 0.58.
  - Long-only, N ≈ 746 (assumed half; unmeasured): 58% → 0.09; unhaircut → 0.34.
  - Using rROD instead (0.0713): 58% → 0.21; 26% → 0.53; unhaircut → 0.79.
  - **Req 4 fails at the conservative central reading** (0.15 < 0.50).
- Cost and entry-slip sensitivity (M-16, printed only): Tradeify RT $1.82 = 3.64 ticks (tick 0.1 pt = $0.50) ≈ 1.92bp at the ledger's 2019–2024 panel median 1,897.20 (recompute at dev-panel median, M-20). No target-cohort per-event mean in price terms (ER rows give slopes, not trade means), so the target-cohort figure is **not computable**. Orientation from the IWM ETF cohort (not a screen figure): 11.72%/252 ≈ 4.65bp/event gross ≈ 8.8 ticks; after the 58% haircut ≈ 1.95bp ≈ 3.7 ticks; commission alone takes 3.64, so **≈0 ticks of entry slip** consume the haircut edge (unhaircut: ≈5.2 ticks round trip). Entry is time-triggered, not a stop, so slip is the spread-crossing cost (builder default 1 tick/side).
- Barrier feasibility: pending atlas (sibling session).
