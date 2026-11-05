# r2-mym-overnight-drift: MYM × `overnight-drift-european-open` × Bulenox

Status: R2 dossier (Part A §A2–§A3, tasks T2–T3) · 2026-11-04 · K = 0 (no data read) · decides nothing; generation never blesses (Rule 25)

## Cell
- Instrument: MYM (CBOT Micro E-mini Dow) · Mechanism: `overnight-drift-european-open` (NEW; nearest existing `event-window-reversal`) · Provisional firm: **Bulenox** (deviates from D10's index→Tradeify; reason under Venue legality) · Session: Globex overnight session, the European-open window (London morning); long only, entered after the daily Globex reopen, flat well before the US cash open.
- Event frequency: every session (unconditional expression, as published: BLW 2023 average the window over all days). A K-charged conditioned variant (only after a US-close selloff, BLW's asymmetry) has no cited event fraction, so its frequency is unstated.

## Mechanism (harvest Req 1, path 1a)
- WHO pays: traders whose order imbalance hits the US close (the paper reads the futures as "traded as a hedging instrument for the underlying"); liquidity providers absorb it at a discount and are repaid when overseas participants arrive (SR917 §"Returns around the clock"; Liberty Street 2026-07-01). Constraint, not preference, only in part: closing-benchmark execution is a 1a(i) constraint class, but BLW name the imbalance, not the payer's mandate. **Partly met.**
- WHEN: the European-open hour, fixed ex ante by the published schedule. **Met.**
- WHY it persists: LP inventory-risk capacity. **Contradicted:** the authors report the drift "averaged close to zero since 2021", which they link to smaller closing imbalances and LPs slicing flow more finely, i.e. the rent shrank. **Not met.**
- HOW it dies: dispersion of end-of-day signed-volume imbalance (RSV). The authors' std fell from 6.5% to 2.9% (2021–2025 vs. full sample) as the drift faded. Observable, but signed volume is order flow and is not in the admitted OHLCV feed. **Met in principle; not monitorable on the admitted feed.**

## Effect priors (Req 2)
| Source (date accessed) | Cohort | Figure | Transplant? |
|---|---|---|---|
| Boyarchenko, Larsen, Whelan, "The Overnight Drift", FRBNY SR917 (rev. Aug 2022); RFS 36(9) 2023, 3502–3547 (2026-11-04) | ES E-mini, 1998-01-05→2020-12-31 | Table I: European-open hour 1.5 bp/day, HAC t = 7.1; positive in 20 of 23 years | **Yes, ES→MYM** |
| Same authors, "The Disappearing Overnight Drift", Liberty Street Economics, 2026-07-01 (2026-11-04) | ES, 2021-01→2025-12 (1,245 days); 1998–2020 = 5,691 days | "averaged close to zero since 2021"; "The same pattern holds in the … (NQ) and E-mini Dow Jones (YM) contracts" (no YM figure given) | ES figure; YM named without a number |
| In-house H-OD-1 (`discovery_manifests/h_od_1_es_overnight_drift.json`, ADR 2026-07-16 attestation §1) | ES, 2010-06→2018-12 | +1.444 bp vs 1.5 bp, t≈5.0, 9/9 IS years | ES; MYM was FORBIDDEN in that manifest |
- Decay haircut: the authors' own post-publication sample gives **≈100%** (2021–2025 ≈ 0). Literature fallback: McLean–Pontiff (2016, JF 71(1)) "58% lower post-publication". The MYM development window (from 2019-05) is mostly post-2021.
- Screen figure: **UNSCREENABLE.** The only δ is ES (transplant, refused by Req 2); YM is named without a number. For illustration only (not a screen): ES δ/σ = 7.1/√5,691 = 0.094; ×0.42 = 0.040. To supply it: a δ-extraction probe on MYM's own European-open window (K = 1, spends one of MYM's two builder looks, §11), split pre/post 2021, or a published YM figure from the authors' online appendix if one exists.

## Prior consult (advisory, Rule 26)
```text
$ python3 -I scripts/fp.py python scripts/instrument_profiles.py cell MYM overnight-drift-european-open; echo "exit=$?"
FATAL: unknown mechanism 'overnight-drift-european-open'. Declare it NEW in MECHANISMS.md.
exit=2
$ python3 -I scripts/fp.py python scripts/instrument_profiles.py cell MYM event-window-reversal; echo "exit=$?"   # nearest existing id
=== MYM x event-window-reversal ===
ledger: ops/instruments/MYM.md
venue: NOT TRADABLE at the live firm — AUTHORIZED-but-venue-less incumbent (Striker DJ30 MYM edition); no live book to correlate new work against — check venue_note before book-correlation gate.
verdict: DEAD (2026-07-21)
  source: ../../docs/briefs/closures/MYM-3FPS-1-closure-falsified.md
  BLOCKING — the re-proposal bar below must be met and addressed in the pre-registration.
class finding (mechanism-wide, not specific to MYM): The settlement limb does not reproduce at useful magnitude — MYM's third-Friday derivative-settlement reversal cleared exact-coverage sourcing (84/87, 96.6% PASS) but both power legs sit below the 0.2139 floor and the tradable limb is negative in 2024–2026. [MYM.md M5](MYM.md)
class finding (mechanism-wide, not specific to MYM): *Auction limb (2026-07-27) — dies at the PROCUREMENT GATE, not on edge, on ANY instrument.* Closing-auction/MOC-imbalance is reject-at-bar for an instrument-independent reason, hence recorded as a class finding rather than a cell. It is **not** killed by the free-data classification (the signal is exchange-licensed, unlike LETF EOD rebalance whose signal is public-AUM-derivable) nor by the a4 category prior (a published **signed** imbalance is not participant-category splitting) — those non-kills are stated so a future session does not borrow the wrong one. What binds: free-data route 1 requires **demonstrating** a vol-orthogonal, within-era-robust edge (F1 had no δ at all — unclaimed, not cleared); the order-flow modality is parenthesised to the standing *"don't buy explanatory data before a survivor justifies it"* rule (Avenue-A qualifying triple unmet; *scoped-not-procured*); and harvest Req 2 independently renders it UNSCREENABLE with the δ-extraction probe route **circular** (it needs the gated data). Cheapest re-open is free: a published cohort δ for imbalance → index-futures response, citable without procurement. [F1 ruling](../../docs/briefs/programs/2026-07-27-f1-moc-imbalance-mym-ruling.md)
BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21 -> ../../docs/rejected_candidates.md
BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21 -> ../../docs/rejected_candidates.md
cost hurdle: 6.57 bp/event (4x Tradeify hurdle) — VERIFY at #M6
K bank: read ../../discovery_manifests/ — never trust a snapshot.
prior: Not a barren instrument — the incumbent locked leg is profitable here; one narrow continuation expression failed. [#M1]
exit=1
```
- Register hits: the nearest id is DEAD on MYM (`MYM-3FPS-1`, third-Friday settlement reversal, 2026-07-21; its re-proposal bar asks for "new target-instrument mechanism evidence", and the bar names no overnight limb as a rescue). This is a different event, but it is the same `event-window-reversal` class. H-OD-1 (ES overnight drift) has no register entry; it closed 2026-07-16 at the Stage-2 cost law, now deleted (harvest Req 5, 2026-10-24), with the mechanism CONFIRMED-IS. The deleted law no longer binds, but the authors' post-2021 null is the operative prior. Its HOW-dies observable is signed flow. The MOC-imbalance register entry (2026-07-27, paid-data procurement gate) reaches order-flow work on MYM.
- Domain bars: the tool binds `index-intraday-ohlcv-directional-timing-2026-07-21`, but the bar's own scope excludes "overnight mechanisms (H-OD-1 — venue-walled)". Route by route, in case a reviewer holds it in scope: **route 1 claimed.** The European-open window is a within-instrument moment named a priori by BLW's mechanism (ADR 2026-08-10 §2-A/§2-B), frozen before data, one window, K = 1. **Route 2 not claimed** (OHLCV only). **Route 3 not claimed** (no evidence). Sibling bar: end-of-day adversity (2026-08-02) is out of scope (not a late-session claim).
- Family K bank (Req 3 disclosure): closed manifests touching MYM are `st_eh_supertrend_grid` (1 MYM), `mymdd_1_2026_08_29` (5) and `q_txg1_striker_nas100_mym_20260812` (1), giving **7** by this read. The ledger says 6 (it omits the Q-TXG-1 cell); unreconciled. `t00_tradeify_book_lineage_2026_10_10` is open (K = 13, includes `dj30_mym_p250`) and not banked. The banks are disclosure only (ADR 2026-08-04). The builder budget is MYM 2 lifetime looks (generation note §11).

## Venue legality at Bulenox
- Native route: algos and bots via the Rithmic third-party API, "$100 monthly fee" (envelope §4 Bulenox row, re-verified 2026-10-02). Whether NinjaScript on NT8 over Rithmic counts as that route is **unverified**.
- Product offered: MYM at 0.61/side (Rates PDF "Updated Aug/11/2026", venue register §F, 2026-11-01).
- Flat-by: "All positions must be closed by 3:59 PM (CT)" (bulenox.com help-center/qualification, envelope §4, 2026-10-02). `firm_rules.py:139`: "force-flattens EOD; no overnight/weekend carry". **Unverified:** whether a position opened after the Globex evening reopen and closed before the US open counts as intraday for Bulenox. It needs a Rule-17 quote.
- News: "News trading allowed" (pricing page, envelope §4, 2026-10-02).
- Hold: minutes to about an hour, inside one Globex session.
- Cross-firm hedging / product group: Tradeify ESA §6.7(c),(i) bans opposing positions between a Tradeify account and any "External Account" incl. "any proprietary trading firm", and Equity Index is one group (MNQ, MYM, …; Tradeify 10495868, envelope §4a, re-read 2026-10-02; deep-dive item 5, 2026-11-01). This cell is **long-only** and **time-disjoint** from ORB-MNQ: ORB enters at the US cash open and is flat by 16:45 ET, and this cell is flat before the cash open. It therefore cannot oppose a Tradeify index position, whichever side ORB-MNQ trades. Bulenox's own hedging rule was not read (gap).
- Why not Tradeify: the 10-30 ruling is "one strategy per firm; Tradeify scales by accounts" of ORB-MNQ (generation note §10.2). A second Tradeify strategy contradicts it while that ruling stands. Tradeify would otherwise be legal: the trading day is "6:00 P.M. ET to 5:00 P.M. ET" (10468225), flat-by 16:45, and the micro RT is $1.82. Why not BluSky or MFFU: D10 assigns them metals and FX. Bulenox's D10 slot is "6J … or held", the weakest. The harshest barrier, an intraday trail on Option 1, matters least for a sub-hour, low-volatility hold. Option 2 is EOD.

## Distinctness
- vs index ORB book: a different session (Globex overnight vs. US cash open), a different mechanism (inventory-resolution drift vs. opening-range break), and a different side structure (unconditional long, no breakout trigger). No holding-time overlap.
- vs withdrawn Striker DJ30 MYM editions: Striker is a long-only pyramided trend-follower on the locked book (register `Q-PYRPARITY-1`). This cell has no trend signal, no pyramid and a fixed clock window. The locked entry windows are private and were not read, so non-overlap of their sessions is **asserted from mechanism, not verified**.
- vs other R2 dossiers: Same mechanism and source as r2-mnq-ovndrift and r2-m2k-ondrift (Equity Index group): not distinct from them, so at most one of the three runs in R2. The authors name YM explicitly ("The same pattern holds in the E-mini Nasdaq-100 (NQ) and E-mini Dow Jones (YM) contracts", Liberty Street Economics 2026-07-01), and MYM is not the ORB instrument. Differs from every non-index dossier in instrument, product group and mechanism.

## Reach (T3)
- 5f reach (D7, `gates.reachability(k, n)` run 2026-11-04 through the fp launcher; arithmetic only, no data read). Banked builder K on this instrument: **0** on the public record (R1 is MCL-only and unrun; the builder ledger is private, so `ledger.k()` must confirm it at registration). Development sessions n ≈ **1,492**: window 2019-05-06..2026-11-02 ≈ 1,870 sessions by `ops/calendars/cme_holiday_calendar_2016_2026.json` (sha256 `407d93bb815ee6b2…`; weekdays less non-`NORMAL` dates), less D9's 378-session holdout. The pinned export sets the real n.
  | K (banked + this card) | 5f floor (annual SR) | P(pass \| SR 0.85) | P(pass \| SR 0.89) | Reachable (D7) |
  |---|---|---|---|---|
  | 1 (this card) | 0.676 | 0.664 | 0.698 | yes |
  | 2 (the reserve look) | 0.890 | 0.461 | 0.500 | yes, at the boundary |
  | 3 | 1.027 | 0.334 | 0.370 | no |
  Normal approximation; 5f only, so every other gate lowers P(pass). The instrument's lifetime budget is 2 looks (generation note §11).
- Power at expected event count: N = 1,492 dev sessions × 1/session = 1,492. Screen power is **not computable (UNSCREENABLE)**. Illustrative transplant only: power = Φ(√1,492 × 0.094 − 1.96) = Φ(1.68) = 0.95 unhaircut; at δ/σ 0.040 (58%) Φ(−0.43) = 0.33; at the authors' post-2021 ≈ 0, power ≈ Φ(−1.96) = 0.025. Break-even δ/σ for 0.50 = 1.96/√1,492 = 0.051.
- Cost and entry-slip sensitivity (M-16, printed only): Bulenox RT $1.22 = **2.44 ticks** (tick = 1 pt = $0.50, MYM.md 2026-09-02). Alternatives: Tradeify $1.82 = 3.64, MFFU $1.90 = 3.80, BluSky $0.50/side Rithmic = 2.00. Ticks per bp = L/10⁴ points at index level L; illustratively at L = 40,003.59 (DJIA first close above 40,000, 2024-05-17), 1 bp ≈ 4.0 ticks. The ES transplant figure of 1.5 bp ≈ 6.0 ticks gross leaves 3.6 ticks for total slip at Bulenox. Haircut 0.63 bp ≈ 2.5 ticks leaves ≈0.1 tick. At post-2021 ≈ 0 any slip is a loss. BLW returns are mid-quote, so the spread is not in the published figure. This is a market-order entry with no stop-entry, so M-16's stop-slip case applies only as a spread or market-impact charge.
- Barrier feasibility: pending atlas (sibling session).
