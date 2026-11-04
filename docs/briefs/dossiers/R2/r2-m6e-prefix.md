# r2-m6e-prefix: M6E × fx-fix-dealer-prehedge-drift × MFFU

Status: R2 dossier (Part A §A2–§A3, tasks T2–T3) · 2026-11-04 · K = 0 (no data read) · decides nothing; generation never blesses (Rule 25)

## Cell
- Instrument: M6E (CME E-micro EUR/USD; no repo ledger yet, landing owed; EURUSD.md is the nearest prior, labelled) · Mechanism: `fx-fix-dealer-prehedge-drift` (NEW; nearest existing `event-window-reversal`) · Provisional firm: MFFU Rapid (D10 proposed mapping, not decided) · Session: European open through the Frankfurt/ECB-concertation fix (London morning, before the US cash open). Direction is fixed a priori: short EUR (long USD) into the fix, flat at the fix.
- Event frequency: every session (one event per trading day). Source: Krohn–Mueller–Whelan document the pre-fix USD appreciation as an unconditional daily pattern, "consistently positive in all days of the week, weeks of the month as well as months of the year".
- Primary declared expression is the pre-ECB leg only. The London-WMR post-fix leg and the Tokyo-fix legs were considered and set aside (sources/NOTES-M6E.md §3).

## Mechanism (harvest Req 1, path 1a)
- WHO pays: benchmark-execution customers. Asset managers value and hedge at fixes; euro-area corporates reference the ECB rate for forward hedges. They pay because their mandate or hedge-accounting benchmark is the fix rate, which spares them tracking error against it. Dealers fill these orders at the fix and pre-hedge the expected net USD demand. That pre-hedging is the price pressure. Dealers accept it because of their inventory and risk-bearing limits. KMW name the payer channel as "constrained intermediation by foreign exchange dealers" absorbing "unconditional demand for U.S. dollars at currency fixings". Constraint, not preference: clause (i) is met on the paper's own account.
- WHEN: a scheduled daily trigger. The window opens at the European open and ends at the fix. The schedule is published, not read from data. **Disclosed anchor change:** the ECB moved publication of its reference rate to later in the CET afternoon in July 2016 "while keeping the methodology unchanged", and an earlier-afternoon Reuters fix was introduced for corporates (KMW SWP, §II). The dev window (2016–2026) therefore straddles an anchor change, and the pre-registration must name which fix the window ends at.
- WHY it persists: KMW find that harvesting it needs better than average spreads. At 100% quoted spread, returns "turn negative, reflecting the huge turnover", so it pays only for "traders that are able to get reasonably good conditions to trade". The rent sits under the spread for most capital. Dealers are the ones paying it, and their capacity is the binding constraint, since "reversal returns are lower during low volatility periods". Clause (iii) is met as a cost-capacity argument. It is weak at micro size, because our own spread plus commission is the same wall (see Reach).
- HOW it dies: three observables. (a) The share of FX volume executed at benchmark fixes, from Euromoney or FX-survey fix shares and WMR fix volumes. (b) Dealer pre-fix hedging disclosures and FSB benchmark reforms. (c) In-sample, KMW's own year-by-year reversal returns, a series that was already falling: "dropped to below 5% during the last two years in our sample". The decay monitor watches (a) beside the edge CUSUM.

## Effect priors (Req 2)
| Source (date accessed) | Cohort | Figure | Transplant? |
|---|---|---|---|
| Krohn, Mueller, Whelan, Bank of Canada SWP 2021-48 (working-paper version of *J. Finance* 79(1) 2024, 541–578), https://www.bankofcanada.ca/wp-content/uploads/2021/10/swp2021-48.pdf (2026-11-04) | EUR/USD spot (Refinitiv RTH), Jan 1999–Dec 2019 | Table I, EUR "pre-E": −8.87% annualised, t = −7.24 | No (parent spot pair of M6E, labelled) |
| same, Table III | CME futures dollar portfolio (EUR, GBP, JPY), Jan 2006–Dec 2019 | pre-E −5.06% ann., t = −5.81 | Portfolio incl. EUR; futures-market confirmation only, not the screen figure |
| same, Table II | dollar portfolio, 9 currencies, subsamples | pre-E full −4.21 (t −4.50); 2014–19 −3.14 (t −2.28) | Portfolio; used only as a decay ratio, disclosed |
| McLean & Pontiff, *J. Finance* 71(1) 2016, 5–32, https://Www.Gwern.net/doc/economics/2016-mclean.pdf (2026-11-04) | 97 US cross-sectional predictors | "26% lower out-of-sample and 58% lower post-publication … 32% (58%–26%) lower return from publication-informed trading" | Haircut source (equities), not a δ |

- Arithmetic: δ/σ per event = |t|/√N_days. N_days = 5,264, the paper's own count ("5,264 daily observations", KMW table notes; coordinator re-read 2026-11-04). EUR pre-E: 7.24/√5264 = **0.0998**.
- Post-2014 check, which covers the post-Feb-2015 WMR window change: the dollar-portfolio pre-E δ/σ is 2.28/√1315 = 0.0629 for 2014–19 against 4.50/√5264 = 0.0620 for the full sample. The ratio is 1.01, so no in-sample decay appears on this leg. (N for 2014–19 ≈ 1,315 is my estimate: 5.25 years × ~251.)
- Decay haircut: McLean–Pontiff **58%**, the conservative central choice. It covers both data-mining and publication decay, and the paper was circulating from about 2019–2020, inside our dev window. The 32% publication-only figure is a sensitivity.
- Screen figure: **δ/σ = 0.0998 × 0.42 = 0.042** (sensitivity: 32% haircut gives 0.068). The figure is gross and from the spot parent. Net tradeability on M6E is the campaign's question, not the screen's.

## Prior consult (advisory, Rule 26)
```text
$ python3 -I scripts/fp.py python scripts/instrument_profiles.py cell M6E event-window-reversal; echo "exit=$?"
FATAL: no ledger for 'M6E'. Known: 6J, BTCUSD, ES, EURGBP, EURUSD, GER40, M2K, M6A, M6B, MCL, MES, MGC, MJY, MNQ, MYM, NAS100, NG, NQ, SPX500, USDCAD, USOIL, XAGUSD, XAUUSD, YM, ZB, ZF, ZN
exit=2
$ python3 -I scripts/fp.py python scripts/instrument_profiles.py cell M6E fx-fix-dealer-prehedge-drift; echo "exit=$?"
FATAL: no ledger for 'M6E'. Known: 6J, BTCUSD, ES, EURGBP, EURUSD, GER40, M2K, M6A, M6B, MCL, MES, MGC, MJY, MNQ, MYM, NAS100, NG, NQ, SPX500, USDCAD, USOIL, XAGUSD, XAUUSD, YM, ZB, ZF, ZN
exit=2
$ python3 -I scripts/fp.py python scripts/instrument_profiles.py cell EURUSD fx-fix-dealer-prehedge-drift; echo "exit=$?"
FATAL: unknown mechanism 'fx-fix-dealer-prehedge-drift'. Declare it NEW in MECHANISMS.md.
exit=2
--- nearest proxy (EURUSD spot ledger x nearest existing id; PROXY, not M6E) ---
$ python3 -I scripts/fp.py python scripts/instrument_profiles.py cell EURUSD event-window-reversal; echo "exit=$?"
=== EURUSD x event-window-reversal ===
ledger: ops/instruments/EURUSD.md
venue: NOT TRADABLE at the live firm — FXIFY/DXTrade CFD venue closed 2026-07-10; no live venue for this instrument at present.
verdict: DEAD (2026-06-22)
  source: ../../docs/rejected_candidates.md
  BLOCKING — the re-proposal bar below must be met and addressed in the pre-registration.
class finding (mechanism-wide, not specific to EURUSD): The settlement limb does not reproduce at useful magnitude — MYM's third-Friday derivative-settlement reversal cleared exact-coverage sourcing (84/87, 96.6% PASS) but both power legs sit below the 0.2139 floor and the tradable limb is negative in 2024–2026. [MYM.md M5](MYM.md)
class finding (mechanism-wide, not specific to EURUSD): *Auction limb (2026-07-27) — dies at the PROCUREMENT GATE, not on edge, on ANY instrument.* Closing-auction/MOC-imbalance is reject-at-bar for an instrument-independent reason, hence recorded as a class finding rather than a cell. It is **not** killed by the free-data classification (the signal is exchange-licensed, unlike LETF EOD rebalance whose signal is public-AUM-derivable) nor by the a4 category prior (a published **signed** imbalance is not participant-category splitting) — those non-kills are stated so a future session does not borrow the wrong one. What binds: free-data route 1 requires **demonstrating** a vol-orthogonal, within-era-robust edge (F1 had no δ at all — unclaimed, not cleared); the order-flow modality is parenthesised to the standing *"don't buy explanatory data before a survivor justifies it"* rule (Avenue-A qualifying triple unmet; *scoped-not-procured*); and harvest Req 2 independently renders it UNSCREENABLE with the δ-extraction probe route **circular** (it needs the gated data). Cheapest re-open is free: a published cohort δ for imbalance → index-futures response, citable without procurement. [F1 ruling](../../docs/briefs/programs/2026-07-27-f1-moc-imbalance-mym-ruling.md)
K bank: read ../../discovery_manifests/ — never trust a snapshot.
prior: The London 16:00 WM/Reuters fix carries a genuine ~2bp gross post-fix reversal (reproducing the source paper's magnitude) but FXIFY retail all-in cost (~0.8 pip) exceeds the 0.277-pip best-of-grid break-even — the edge is real but not retail-tradeable. [#F1]
exit=1
```
- Register hits (all advisory):
  1. **FX intraday fixing-reversal on EURUSD**, DEAD, cost, 2026-06-22. Its bar: "materially better-than-retail execution … OR a genuinely different mechanism. NOT … a different fix (Tokyo/Frankfurt)". **This cell probably trips the letter of that bar.** It is a Frankfurt-anchored window on the same fix-intermediation family. Its claim to distinctness is that it is the pre-fix drift over a multi-hour window, not the fix-print reversal. The cost wall that killed D2 has not obviously gone away on M6E (see Reach). The pre-registration must address it head-on.
  2. **London-fix wake on 6E/6B**, FALSIFIED edge-failure, 2026-08-24. It is a different window (after the London fix) and a different sign logic (fading the impulse). Shared lesson: orthogonality to generic reversal was the test that killed it, so this cell's null should include a same-session time placebo (M-17).
  3. **Custodian month-end on EURUSD**, SHELVED soft. KMW report their pattern is "not driven by an end-of-month equity hedging channel", so there is no dedup collision.
  4. **Informed-flow signature** (MCL TAS entry; R8 gold fix, metals-scoped, DEAD). Benchmark-flow public residue is small by construction. That is an adverse prior, and R8 does not bind FX.
- Domain bars: the index-intraday OHLCV raised bar does not apply (FX, not an index). There is no FX domain bar in "Domain-level tail-exhaustion raised bars".
- Family K bank (Req 3 disclosure): `discovery_manifests/fc_carry_6e6j6cl.json` K = 1, closed, combined 6E/6J/CL carry. Outside the manifest ledger: the EURUSD pattern-enum harness K = 450 (spot, closed DONE_WITH_CONCERNS), the D2 cost pre-screen and the B2.2 6E wake battery. Declared K_intrinsic for this cell: 1.

## Venue legality at MFFU
- Native route: own-settings automation allowed: "Traders may make use of automated trading strategies tailored to their own specific settings". HFT is banned. 8444599, read 2026-11-04 via a summarising fetch [W-x]. Envelope E6 assumes attended automation. **This window is US pre-dawn, so attended operation is an operational burden; flag it to the operator.**
- Product offered: M6E is on the instrument list, "Total Cost Round Trip" $1.44, which is $0.72/side. Source: `core/firm_rules.py` comment citing 9735811, verified 2026-07-13; envelope re-verified 9735811 on 2026-10-02.
- Flat-by: auto-liquidation at 16:10 ET, "4:10 PM EST" (9558251, envelope re-verified 2026-10-02). The session opens at 18:00 ET. The cell ends hours before that.
- News: Tier 1 is "FOMC Meetings, FOMC Minutes, Employment Report, CPI". It is prohibited on Rapid and Pro Sim Funded and permitted on "All evaluations". The rule is "No positions or orders … 2 minutes before and after the release". No non-US or ECB event is listed (8230009, "Last updated August 31, 2026", read 2026-11-04 [W-x]). Collision: the window normally ends before the 08:30 ET US release slot. In the US/EU DST-mismatch weeks the fix lands later in ET and the window can span 08:30 ET. Sim-funded must then skip NFP and CPI days, so list the collision frequency (envelope E7).
- Hold: intraday only. No overnight or weekend hold is needed (`weekend_holds: False`, firm_rules).
- Fills: "Exploiting the absence of slippage and utilizing tight brackets to gain from favorable fills are not permitted" (8444599 [W-x]; register D9, 2026-10-30). The cell enters and exits on the clock with no tight brackets. Live fills on a thin European-morning M6E book may be worse than sim, so the backtest must charge live-realistic fills.
- Cross-firm hedging / product group: MFFU says "MyFunded Futures prohibits hedging of any kind", meaning "both buy and sell positions on the same underlying asset, at the same time". A single-direction cell is compliant. The MFFU page states no rule on running the same strategy elsewhere [W-x]. Tradeify §4a: Currencies group = 6E, M6E, 6B, 6J, 6A, M6A, 6C, 6S, and opposing positions across "any accounts under your control" are banned. If any Tradeify account holds a long Currencies position (e.g. 6J) while this cell is short M6E, that is an opposing-direction breach on Tradeify's reading. Sign-coordinate it, or keep Currencies out of Tradeify.

## Distinctness
- vs index ORB book: it differs on every axis. Instrument (M6E vs MNQ), product group (Currencies vs Equity Index), session (European morning vs US cash open), mechanism (clock-anchored benchmark-flow drift vs range breakout) and order type (time entry vs stop entry).
- vs other R2 dossiers: Shares its source family (Krohn–Mueller–Whelan) with r2-6j-tokyofix but differs in instrument, fix (Frankfurt/ECB vs Tokyo) and window (London morning vs Globex evening): distinct under the working test, shared counterparty class disclosed. Same Currencies group as both 6J dossiers: direction coordination needed if a Currencies book runs at Tradeify.

## Reach (T3)
- 5f reach (D7, `gates.reachability(k, n)` run 2026-11-04 through the fp launcher; arithmetic only, no data read). Banked builder K on this instrument: **0** on the public record (R1 is MCL-only and unrun; the builder ledger is private, so `ledger.k()` must confirm it at registration). Development sessions n ≈ **2,325**: window 2016-01-04..2026-11-02 (the calendar's 2016 start binds, not the export) ≈ 2,703 sessions by `ops/calendars/cme_holiday_calendar_2016_2026.json` (sha256 `407d93bb815ee6b2…`; weekdays less non-`NORMAL` dates), less D9's 378-session holdout. The pinned export sets the real n; FX holidays differ from the equity columns, so the calendar estimate is coarser for FX. M6E's export landed locally 2026-11-03; its repo landing (ledger, specs, SHA256SUMS) is owed before any card.
  | K (banked + this card) | 5f floor (annual SR) | P(pass \| SR 0.85) | P(pass \| SR 0.89) | Reachable (D7) |
  |---|---|---|---|---|
  | 1 (this card) | 0.542 | 0.825 | 0.855 | yes |
  | 2 | 0.713 | 0.662 | 0.705 | yes |
  | 3 | 0.822 | 0.533 | 0.581 | yes |
  | 4 | 0.888 | 0.454 | 0.502 | yes, at the boundary |
  Normal approximation; 5f only, so every other gate lowers P(pass). The instrument's lifetime budget is 4 looks (generation note §11).
- Power at expected event count: N = 2,325 dev sessions × 1 event/session = 2,325. power = Φ(√2325 × 0.042 − 1.96) = Φ(48.22 × 0.0419 − 1.96) = Φ(0.060) = **0.52**. That is marginal. The break-even δ/σ for 0.50 is 1.96/48.22 = 0.0406. With the 32% haircut: Φ(3.274 − 1.96) = **0.91**. Unhaircut: 0.998.
- Cost and entry-slip sensitivity (M-16, printed only): M6E tick 0.0001 = $1.25 (CME spec, quoted in the generation DRAFT §9.1; Rule 17 re-read owed at landing). The MFFU commission of $1.44 RT = **1.15 ticks RT**. The per-event gross mean takes −8.87%/252 = 3.52 bp; the 252-day annualisation is my assumption, not stated in the table note. At an assumed EUR/USD level of 1.0–1.2 that is 3.5–4.2 ticks unhaircut, **1.48–1.77 ticks after the 58% haircut**, and 2.39–2.87 ticks after 32%. Net of commission: **0.33–0.62 ticks** (58%) or 1.24–1.72 ticks (32%). So **0.3–0.6 tick of total entry-plus-exit slip consumes the screen effect.** That is less than crossing a one-tick spread once each way at half-spread per side. On M-16's terms the cell is cost-bound at the conservative haircut and survives only at the 32% reading. It is the same cost wall D2 hit.
- Barrier feasibility: pending atlas (sibling session).
