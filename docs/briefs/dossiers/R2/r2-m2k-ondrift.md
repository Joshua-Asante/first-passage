# r2-m2k-ondrift: M2K × overnight-drift-intermediary-inventory × Bulenox

Status: R2 dossier (Part A §A2–§A3, tasks T2–T3) · 2026-11-04 · K = 0 (no data read) · decides nothing; generation never blesses (Rule 25)

## Cell
- Instrument: M2K (CME Micro E-mini Russell 2000) · Mechanism: `overnight-drift-intermediary-inventory` (NEW; nearest existing ids consulted: `ict-liquidity`, where the register files H-OD-1's overnight-inventory finding, and `overnight-range-transmission`) · Provisional firm: **Bulenox** (deviates from D10's Tradeify→index; reasons under Venue legality) · Session: Globex overnight, around the European cash open; flat long before the US cash open. Long-only, unconditional.
- Event frequency: every session (cohort construct is unconditional daily; SR917).

## Mechanism (harvest Req 1, path 1a)
- WHO pays: liquidity demanders who leave end-of-day order imbalances at the US close (sell-offs in particular); intermediaries with limited risk-bearing capacity carry that inventory overnight and are paid to do so. Source: SR917 abstract: "Consistent with models of inventory risk, we demonstrate a strong relationship with order imbalances at the close of the preceding U.S. trading day." Clause (i) **partly met**: the friction is a constraint (dealer inventory/risk capacity), but the payer's own constraint (e.g. benchmark-at-close execution) is not shown in the source.
- WHEN: cohort-declared clock window at the European open (SR917), fixed before any data read. Met.
- WHY it persists: small rent in a thin overnight hour, below institutional ticket interest after costs; compensation for inventory risk, not mispricing. Argued, not evidenced for Russell.
- HOW it dies: prior-day end-of-day signed order imbalance stops predicting the drift; overnight depth growth erodes dealer inventory premium. Observable: EOD signed volume (SR917 measure), overnight volume/depth.

## Effect priors (Req 2)
| Source (date accessed) | Cohort | Figure | Transplant? |
|---|---|---|---|
| Boyarchenko, Larsen & Whelan, *The Overnight Drift*, FRBNY SR917 (rev. Aug 2022; RFS 36(9) 2023), https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr917.pdf (2026-11-04) | S&P 500 e-mini futures, Jan 1998–Dec 2020 | "averaging 3.7% on an annualized basis (1.48 basis points per day)"; "positive in 20 out of 23 years since 1998 and statistically significant in 17" | **Yes — S&P only.** No Russell cohort in the text (grep of full text: no Russell/small-cap rows) |
| Repo: H-OD-1 prereg (`docs/briefs/pre-registration/H-OD-1-ES-overnight-drift-preregistration.md:26`) | ES, SR917 Table I | δ/σ = 0.093 (t-scaled; +1.5bp/day, t = 7.1); in-house ES IS mean gross +1.444bp (rejected_candidates.md :1064) | **Yes — ES.** Repo already ruled MNQ/NQ/MYM expressions UNSCREENABLE on this transplant (prereg :27) |
- Decay haircut: McLean & Pontiff (2016, JF 71(1)) 58% post-publication would apply; moot because no target cohort exists.
- Screen figure: **UNSCREENABLE**. Supplier: a K=1 δ-extraction probe on M2K's own panel (or RTY parent, proxy discipline) for the cohort-declared window, IS-only, placebo clock hour pre-committed (H-OD-1's design), costs one K on M2K.

## Prior consult (advisory, Rule 26)
```text
=== overnight-drift-intermediary-inventory
FATAL: unknown mechanism 'overnight-drift-intermediary-inventory'. Declare it NEW in MECHANISMS.md.
exit=2
=== ict-liquidity  (nearest: register files H-OD-1's overnight-inventory finding under this class)
=== M2K x ict-liquidity ===
ledger: ops/instruments/M2K.md
verdict: untested — no prior on this cell.
class finding (mechanism-wide, not specific to M2K): Sweep→same-direction-FVG→opposing-pool-draw direction is real on SPX500 (block-permutation p=0.0144) but fails robustness (drop-top-3 = −0.152R, 95% block-CI straddles 0). [SPX500.md D2](../../../../ops/instruments/SPX500.md)
class finding (mechanism-wide, not specific to M2K): — CORRECTED 2026-08-04; [... 1m FVG retrace finding, full text in [NOTES-M2K.md](sources/NOTES-M2K.md) consult log ...] [MNQ.md W3](../../../../ops/instruments/MNQ.md) · [`RESULTS_1M_DIAG.md`](../../../../lab/analysis/_inbox/ict_mnq_2026-08/RESULTS_1M_DIAG.md)
class finding (mechanism-wide, not specific to M2K): **Liquidity pools are anti-attractors**, replicated on three independent instruments [...] [MNQ.md N9](../../../../ops/instruments/MNQ.md) · [`RESULTS.md`](../../../../lab/analysis/_inbox/ict_mnq_2026-08/RESULTS.md) §3
BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21 -> ../../docs/rejected_candidates.md
cost hurdle: 11.89 bp/round-trip (panel-era median 1,897.20 => 11.89 bp/RT [...]) — VERIFY at #M2
K bank: read ../../discovery_manifests/ — never trust a snapshot.
prior: Cross-index RV selection over ES/NQ/YM/RTY is strictly dominated by single-instrument ORB-MNQ [...] [#M3]
prior: Opening-range momentum is an equity-index property (it fades on Treasuries) [...] [#M4]
exit=1
=== overnight-range-transmission  (nearest by session)
=== M2K x overnight-range-transmission ===
ledger: ops/instruments/M2K.md
verdict: untested — no prior on this cell.
class finding: (D5 stage-1 $0 cheap falsifier, MNQ, OFFICIAL): overnight range clears D5's un-pause condition (2) decisively [...] Stage 2 [...] owed, not yet run [...]
class finding: (D5 stage-1 $0 cheap falsifier, MYM, amended 2026-08-30 [...]) [...] stage 2 equally owed and not yet run.
BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21 -> ../../docs/rejected_candidates.md
cost hurdle / K bank / priors #M3 #M4: as above
exit=1
=== overnight-range-failed-extension-fade  (DEAD cell, disclosed)
verdict: DEAD (2026-08-13)
  source: ../../docs/briefs/closures/MSL-C3-K2-closure-falsified.md
  BLOCKING — the re-proposal bar below must be met and addressed in the pre-registration.
class finding: M2K explore **FALSIFIED 2026-08-13** (Axis B both-arms IS 95% CI entirely &lt; 0; long n=359 CI [−0.220, −0.021]; short n=378 CI [−0.204, −0.014]; pooled −0.114R). CONFIRM unread.
BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21
exit=1
```
(Bracketed `[...]` elisions only; verbatim full output is in [NOTES-M2K.md](sources/NOTES-M2K.md).)
- Register hits: M2K DEAD `overnight-range-failed-extension-fade` (MSL-C3-K2, addback "new mechanism evidence — NOT θ-retune"): different mechanism (unconditional long in a dealer-inventory clock window vs fading failed extensions of the overnight range); does not bind, disclosed. H-OD-1 (ES overnight drift) closed 2026-07-16 on the Stage-2 cost-law, since deleted (harvest Req 5, 2026-10-24); its mechanism confirmed IS on ES (+1.444bp, t≈5.0, 9/9 IS years; rejected_candidates.md :1064). M3 (RTY intraday pull = DEFER, poor prior) is scoped to cross-index selection; not this mechanism.
- Domain bars: `index-intraday-ohlcv-directional-timing-2026-07-21` binds M2K (US equity-index future; M2K.md M1 declares it directly). Its scope text **excludes "overnight mechanisms (H-OD-1 — venue-walled)"**, so this cell sits outside scope by the bar's own wording. Route by route anyway: (1) mechanism outside {price, cross-instrument selection, hold-time}: a within-instrument clock window from dealer inventory, outside the mapped set per ADR 2026-08-10 §2-A; **claimed, not adjudicated**; (2) modality/venue: no new modality; "venue-walled" label is stale for a flat-by-firm-deadline Globex expression; not claimed; (3) beats ORB-MNQ net: no evidence. End-of-day adversity bar (2026-08-02): out of scope (no RTH final-block claim).
- Family K bank (Req 3 disclosure): M2K 0 (no file in `discovery_manifests/` mentions M2K or RTY, grep 2026-11-04). Note: rejected_candidates.md :132 labels MSL-C3-K2 "K=2" while M2K.md's session log says "K spent=0" and no manifest exists; unreconciled. ES family 2 includes H-OD-1.

## Venue legality at Bulenox
- Native route: algos/bots "via Rithmic third-party API ($100/mo)" (ops/prop_envelope_default.md §4, re-verified 2026-10-02); native NinjaScript-on-Rithmic not verified · Product offered: M2K 0.61/side (core/firm_rules.py:102, Rates PDF Sept-2024 vintage; the Aug-2026 PDF re-check at :121 restates MNQ/MYM/MES only — M2K current rate unverified) · Flat-by: "All positions must be closed by 3:59 PM (CT)" (envelope §4, 2026-10-02) · News: "News trading allowed" (envelope §4, 2026-10-02) · Hold: no overnight carry past flat-by; **whether opening a position after the Globex reopen and closing before flat-by is permitted is not stated in any repo source** (verify) · Cross-firm hedging / product group: Tradeify ESA §6.7(c),(i) bars opposing positions between a Tradeify account and any External Account (venue-fact register §I.2, 2026-11-01). This cell is long-only, so it cannot oppose a long-only ORB-MNQ; long+long is allowed (firm_rules.py:258 comment). Bulenox's own hedging rule not in repo.
- Why not D10's Tradeify: (a) Joshua 2026-11-03: "For now we are not letting index stay Tradeify only"; (b) D10's Bulenox slot is "6J … or held", the weakest slot; (c) Bulenox M2K commission is the lowest repo-held (cost decides this cell, see Reach); (d) Tradeify makes any bot exclusive within Tradeify (ESA §6.6, register §I.2). Consequence if kept at Tradeify: second strategy beside ORB on one firm, Tradeify-exclusive, RT $1.82 exceeds even the ES-transplant gross. Consequence at Bulenox: Option 1 intraday trail is the harshest barrier (D10 watch); native route and overnight-session entry unverified; Tradeify §6.7 still watches it.

## Distinctness
- vs index ORB book: different session (Globex overnight vs US cash open), different mechanism (inventory clock drift vs opening-range breakout), no in-market overlap (ORB flat by close; this flat before the cash open). Same product group (Equity Index), long-only both: no hedge conflict.
- vs other R2 dossiers: Same mechanism and source as r2-mnq-ovndrift and r2-mym-overnight-drift (Equity Index group): not distinct from them, so at most one of the three runs in R2. No published Russell figure exists, unlike YM (named by the authors). Differs from every non-index dossier in instrument, product group and mechanism.

## Reach (T3)
- 5f reach (D7, `gates.reachability(k, n)` run 2026-11-04 through the fp launcher; arithmetic only, no data read). Banked builder K on this instrument: **0** on the public record (R1 is MCL-only and unrun; the builder ledger is private, so `ledger.k()` must confirm it at registration). Development sessions n ≈ **1,492**: window 2019-05-06..2026-11-02 ≈ 1,870 sessions by `ops/calendars/cme_holiday_calendar_2016_2026.json` (sha256 `407d93bb815ee6b2…`; weekdays less non-`NORMAL` dates), less D9's 378-session holdout. The pinned export sets the real n.
  | K (banked + this card) | 5f floor (annual SR) | P(pass \| SR 0.85) | P(pass \| SR 0.89) | Reachable (D7) |
  |---|---|---|---|---|
  | 1 (this card) | 0.676 | 0.664 | 0.698 | yes |
  | 2 (the reserve look) | 0.890 | 0.461 | 0.500 | yes, at the boundary |
  | 3 | 1.027 | 0.334 | 0.370 | no |
  Normal approximation; 5f only, so every other gate lowers P(pass). The instrument's lifetime budget is 2 looks (generation note §11).
- Power at expected event count: N ≈ 1,492 dev sessions × 1/session = 1,492. Power **not computable (UNSCREENABLE)**. Break-even δ/σ for power 0.50: 1.96/√1492 = 0.051 (ES transplant 0.093 shown for context only; not a screen figure).
- Cost and entry-slip sensitivity (M-16, printed only): M2K tick 0.1 pt = $0.50. RT commission in ticks: Bulenox $1.22 → 2.44 · BluSky Rithmic eval $1.00 → 2.00 · Tradeify $1.82 → 3.64 · MFFU $1.90 → 3.80 (sources in Venue legality / NOTES). At the ledger's 2019–2024 panel median 1,897.20 (M2K.md M2; recompute at the dev-panel median, M-20) 1 tick ≈ 0.53bp. Target-cohort per-event effect: none, so slip-to-consume is **not computable**. For orientation only (ES transplant 1.48bp/day): after Bulenox commission 0.19bp ≈ 0.37 ticks remain, so half a tick of entry slip consumes it; at Tradeify the transplant gross is below commission alone. Passive limit entries (H-OD-1's frozen model) would be the only plausible fill model; fill risk then binds.
- Barrier feasibility: pending atlas (sibling session).
