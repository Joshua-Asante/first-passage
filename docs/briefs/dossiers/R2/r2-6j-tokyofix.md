# r2-6j-tokyofix: 6J × tokyo-fix-usd-demand × Bulenox

Status: R2 dossier (Part A §A2–§A3, tasks T2–T3) · 2026-11-04 · K = 0 (no data read) · decides nothing; generation never blesses (Rule 25)

## Cell
- Instrument: 6J (full-size; no M6J at any firm) · Mechanism: `tokyo-fix-usd-demand` (NEW; nearest existing `event-window-reversal`, then `turn-of-month`) · Provisional firm: Bulenox (D10 proposed mapping, not decided) · Session: CME Globex evening ET = Tokyo morning, from the Globex reopen into the Tokyo fix and from the fix into the European open
- Event frequency: every session (the Tokyo fix is daily). Declared hypothesis band K_intrinsic ≤ 3, proposed: (H1) unconditional pre-fix yen weakness; (H2) unconditional post-fix reversal; (H3) the pre-fix leg on gotobi days only (5th/10th/15th/20th/25th/30th and month-end). Calendar estimate for H3: about 72 dates a year, about 29% of sessions (6 dates × 12 months ÷ ~250; shift rule for weekend dates not verified).

## Mechanism (harvest Req 1, path 1a)
- WHO pays: Japanese importers and other real-side bank customers who buy USD at their bank's Tokyo fixing rate. They pay because of a constraint, not a preference: orders placed before the fix fill at the bank's posted fix, and payables settle on gotobi dates by business custom. Banks pre-hedge that predictable one-sided demand (Ito & Yamada 2016/2017: "the buying orders of foreign currency (US dollar and Euro) by importers regularly exceed the selling orders by exporters"). Their compensation lies elsewhere: settlement convenience and a fixed accounting rate.
- WHEN: the Tokyo fix every Tokyo business day, which falls in the CME Globex evening ET (KMW note 14; Japan has no DST, so its ET clock time shifts with US DST). The gotobi and month-end calendar is published ex ante.
- WHY it persists: each event is small, a few bp (KMW Table I JPY), and the counterparty is mandate-inelastic. Harvesting it means attended or automated trading in the US evening, and at full indicative bid-ask the spot version loses money (KMW Table IX, JPY pre+post −6.54%/yr at 100% bid-ask), which keeps arbitrage capital away. Below institutional capacity.
- HOW it dies: observable signs are (a) the USD share of Japanese import invoicing (Akiyama et al. 2021 relate the gotobi effect to it; abstract not opened); (b) bank fix-order volume and the fix-minute spike frequency (Ito & Yamada Table 2); (c) the published decay of the reversal ("returns around the Tokyo fix have been around 5% or below since 2013, and the first year with a negative reversal return was recorded in 2018", KMW).

## Effect priors (Req 2)
| Source (date accessed) | Cohort | Figure | Transplant? |
|---|---|---|---|
| Krohn, Mueller & Whelan, *Foreign Exchange Fixings and Returns Around the Clock*, Bank of Canada SWP 2021-48 (J. Finance 2024 version not opened); https://www.bankofcanada.ca/wp-content/uploads/2021/10/swp2021-48.pdf (2026-11-04) | spot USDJPY, Refinitiv RTH mid quotes, 1999-01..2019-12, 5,264 daily obs | Table I JPY: pre-T −4.06%/yr (t −5.87); post-T +7.94%/yr (t +8.22). Table VII JPY Tokyo reversal (pre+post): mean 12.00%/yr (t 10.12), 57% of days positive | Parent spot pair (USDJPY; 6J is its reciprocal), not a transplant across instruments. The sign flips for 6J. |
| same, Table III | CME futures dollar portfolio (EUR, GBP, JPY), 2006-01..2019-12 | pre-T −4.06 (t −8.93), post-T 5.61 (t 10.00) | Futures support at **portfolio** level only. The JPY futures leg is not reported alone. |
| same, Table II | dollar portfolio, 2014–2019 subsample | pre-T −1.59 (t −2.64), post-T 2.08 (t 2.25) | used only as an in-sample decay ratio |
| Ito & Yamada, *Puzzles in the Forex Tokyo "Fixing"*, CJEB WP 352 (2016), J. Int. Econ. 109 (2017) 214–234; https://business.columbia.edu/sites/default/files-efs/imce-uploads/Research/Research_Papers/WP_352.Ito-Yamada.Tokyo_Fixing_Puzzles.pdf (2026-11-04) | USDJPY, EBS, 1999–2013 (sample varies by test) | a short long/short window either side of the fix: "the average return becomes 1.8bp"; "particularly high at 5th and 10th days" (Figure 6, graphical, no number). Table 5's 5th/10th-day dummy is significant, but on the gap between the **bank fix and the market price**, which is not a tradable return | target pair; gotobi limb has no number |
| Bessho, Sugimoto & Suzuki, arXiv 2301.13204 (2023); https://arxiv.org/html/2301.13204v1 (2026-11-04) | USDJPY, EBS per-minute, 2018–2020 | gotobi pre-fix strategy N=185, PF 1.46, W 0.60 (with filter N=65, PF 2.62); non-gotobi PF 0.51. No mean, σ or t-stat | target pair; PF and win rate only, so no δ/σ is derivable |

- Decay haircut: keep 0.42× (a 58% decline). Source: McLean & Pontiff (2016, J. Finance 71(1)): "Portfolio returns are 26% lower out-of-sample and 58% lower post-publication" (https://Www.Gwern.net/doc/economics/2016-mclean.pdf, 2026-11-04). KMW's own decay agrees: δ/σ for the dollar portfolio in 2014–19 against the full sample is 0.45× (pre-T) and 0.49× (post-T), from Table II/I t-stats with N≈1,316 a subsample. That is a portfolio-level ratio, applied to JPY. The dev window (2016–2026) lies mostly after the KMW sample, so this is a conservative central reading, not a bound.
- Screen figure: δ/σ = t/√N with N = 5,264:
  - H1 pre-T: 5.87/72.55 = 0.0809 → ×0.42 = **0.034**
  - H2 post-T: 8.22/72.55 = 0.1133 → ×0.42 = **0.048**
  - H1+H2 reversal (Table VII): 10.12/72.55 = 0.1395 → ×0.42 = 0.059 (disclosed, not a separate limb)
  - H3 gotobi-conditional: **UNSCREENABLE.** No target-cohort mean/σ was found. Supplying it needs a δ-extraction probe (the 6J panel with a gotobi dummy on the pre-fix window, which charges K) or opening Akiyama et al. 2021 (JAFEE 19, in Japanese; not opened).

## Prior consult (advisory, Rule 26)
```text
$ python3 -I scripts/fp.py python scripts/instrument_profiles.py cell 6J tokyo-fix-usd-demand
FATAL: unknown mechanism 'tokyo-fix-usd-demand'. Declare it NEW in MECHANISMS.md.
exit=2
```
(The earlier placeholder `tokyo-fix-gotobi-flow` gave the same FATAL, exit=2.)
Nearest existing id:
```text
=== 6J x event-window-reversal ===
ledger: ops/instruments/6J.md
verdict: untested — no prior on this cell.
class finding (mechanism-wide, not specific to 6J): The settlement limb does not reproduce at useful magnitude — MYM's third-Friday derivative-settlement reversal cleared exact-coverage sourcing (84/87, 96.6% PASS) but both power legs sit below the 0.2139 floor and the tradable limb is negative in 2024–2026. [MYM.md M5](MYM.md)
class finding (mechanism-wide, not specific to 6J): *Auction limb (2026-07-27) — dies at the PROCUREMENT GATE, not on edge, on ANY instrument.* Closing-auction/MOC-imbalance is reject-at-bar for an instrument-independent reason, hence recorded as a class finding rather than a cell. It is **not** killed by the free-data classification (the signal is exchange-licensed, unlike LETF EOD rebalance whose signal is public-AUM-derivable) nor by the a4 category prior (a published **signed** imbalance is not participant-category splitting) — those non-kills are stated so a future session does not borrow the wrong one. What binds: free-data route 1 requires **demonstrating** a vol-orthogonal, within-era-robust edge (F1 had no δ at all — unclaimed, not cleared); the order-flow modality is parenthesised to the standing *"don't buy explanatory data before a survivor justifies it"* rule (Avenue-A qualifying triple unmet; *scoped-not-procured*); and harvest Req 2 independently renders it UNSCREENABLE with the δ-extraction probe route **circular** (it needs the gated data). Cheapest re-open is free: a published cohort δ for imbalance → index-futures response, citable without procurement. [F1 ruling](../../docs/briefs/programs/2026-07-27-f1-moc-imbalance-mym-ruling.md)
K bank: read ../../discovery_manifests/ — never trust a snapshot.
prior: Aegis-to-6J venue-transfer retains measured panel evidence (n=129, PF 2.318, ~50% venue haircut vs canonical) - parked as a scale-path decision, not falsified by the evidence. [#J1]
prior: The venue structurally throttles Aegis sizing: the 12-contract cap binds on 76% of trades, realizing effective risk ~0.5-1.0% against the locked 1.5% target. [#J5]
exit=0
```
The second-nearest id, `turn-of-month` (gotobi/month-end calendar), also returned exit 0, untested on 6J, with the SPX500 F5 class finding and the same two Aegis priors (full paste in [NOTES-6J.md](sources/NOTES-6J.md)).
- Register hits, each disclosed and none blocking:
  - **Q-INVENTORY-1** (docs/rejected_candidates.md, 2026-07-17) staged "FX fixing-window 6E/6J drift (Krohn-Mueller-Whelan)", the same source family, and killed it on the **4× cost-law** (Req 5). Req 5 was deleted on 2026-10-24, so the kill basis no longer stands as a gate. Its re-proposal bar still reads "not a re-citation of any of the eight dead classes under a different paper". This cell's added elements are the named-payer gotobi limb (H3), the JPY-specific post-fix leg, and the 6J futures cost basis.
  - **fx-fixing-reversal-session-mr on EURUSD** (2026-06-22): a London-fix fade failed its cost pre-screen at the FXIFY ~0.8 pip retail CFD cost. Its add-back bar names "NOT … a different fix (Tokyo/Frankfurt)" and "materially better-than-retail execution". This cell is that named move. What differs is the venue (CME futures at Bulenox's all-in rate, not CFD spread), not the parameters.
  - **Custodian-family month-end flow on EURUSD** (shelved 2026-06-10): a different flow (month-end equity hedging); adjacent only.
  - **D7 6J month-end** (strategy_harvest Req 4 table): died on power 0.30. H3 is a daily-frequency calendar subset, not the monthly event.
- Domain bars: the index-intraday OHLCV raised bar does not apply (non-index instrument). No FX domain bar exists.
- Family K bank (Req 3 disclosure): `fc_carry_6e6j6cl` K=1, closed (combined 6E/6J/CL). `t00_tradeify_book_lineage_2026_10_10` K=13, open (includes the Aegis 6J A-0 replay). Undisclosed-manifest informal 6J 15m 43-cell IS battery on 2026-08-25 (6J.md session log; contents not in repo). 6J `orb-ny-breakout` OOS-falsified (J16).

## Venue legality at Bulenox
- Native route: algos via Rithmic third-party API, "$100 monthly fee" (ops/prop_envelope_default.md §4, re-verified 2026-10-02). Strategy logic native to NinjaScript works through NT8 on Rithmic. The Tradeify-native rule does not bind Bulenox.
- Product offered: full-size 6J only, $2.36/side all-in; "NO M6J row in Rates.pdf" (core/firm_rules.py; Rates PDF "Updated Aug/11/2026", envelope §4 2026-10-02). Bulenox_100K cap 120 micro-equivalents = 12 full-size 6J ("1 mini = 10 micros", accounts-pricing, envelope 2026-10-02).
- Flat-by: "All positions must be closed by 3:59 PM (CT)" = 16:59 ET year-round (envelope §4, 2026-10-02). Both windows open and close within one CME trading day (Globex reopen to before the European open), so no position crosses the flat-by.
- News: "News trading allowed" (Bulenox pricing page, envelope §4, 2026-10-02).
- Hold: no overnight or weekend carry (`weekend_holds: False`, firm_rules.py). The cell is intra-session.
- Inactivity: ≥1 trade per 5 trading days (firm_rules.py). H1/H2 trade daily. H3 alone leaves gaps of up to about 6–7 trading days (the 25th/30th to the 5th), which **may trip the rule** and would need a token trade.
- Drawdown: Option 1 trails the high "including both realized and unrealized (open) profits" (envelope §4). This is the harshest barrier (register A1.1; the engine does not model it faithfully).
- Cross-firm hedging / product group: Tradeify's Currencies group includes 6J and M6E (Tradeify 10495868, envelope §4a, re-read 2026-10-02). ESA §6.7(c),(i) bars opposing positions between a Tradeify account and an "External Account", including "any proprietary trading firm" (deep-dive DRAFT item 5). The cell is **two-sided**: short 6J pre-fix, long post-fix. While Aegis 6J or any Currencies-group book runs at Tradeify, a simultaneous opposite position is a compliance breach. The two books would need sign coordination or time separation.

## Distinctness
- vs index ORB book: different instrument, product group (Currencies), session window (Tokyo morning, the Globex evening ET) and mechanism (scheduled fix flow, entered by clock, not by price break).
- vs Aegis 6J (accepted book; its Pine and ports were not read): Aegis is a mean-reversion strategy. This cell is clock-scheduled flow with no price-extension trigger. Time overlap with Aegis cannot be judged without reading Aegis (forbidden). Raise it as an open coordination item (hedging rule above).
- vs 6J ORB (J16, OOS-falsified): a different window and a different entry type.
- vs other R2 dossiers: Shares its source family (Krohn–Mueller–Whelan dealer fix intermediation) with r2-m6e-prefix, but differs in instrument, fix (Tokyo vs Frankfurt/ECB) and session window (Globex evening vs London morning). Distinct under the working three-limb test; the shared counterparty class is disclosed. Both sit in Tradeify's Currencies group, so their directions need coordination if either runs alongside a Currencies book at Tradeify.

## Reach (T3)
- 5f reach (D7, `gates.reachability(k, n)` run 2026-11-04 through the fp launcher; arithmetic only, no data read). Banked builder K on this instrument: **0** on the public record (R1 is MCL-only and unrun; the builder ledger is private, so `ledger.k()` must confirm it at registration). Development sessions n ≈ **2,325**: window 2016-01-04..2026-11-02 (the calendar's 2016 start binds, not the export) ≈ 2,703 sessions by `ops/calendars/cme_holiday_calendar_2016_2026.json` (sha256 `407d93bb815ee6b2…`; weekdays less non-`NORMAL` dates), less D9's 378-session holdout. The pinned export sets the real n; FX holidays differ from the equity columns, so the calendar estimate is coarser for FX.
  | K (banked + this card) | 5f floor (annual SR) | P(pass \| SR 0.85) | P(pass \| SR 0.89) | Reachable (D7) |
  |---|---|---|---|---|
  | 1 (this card) | 0.542 | 0.825 | 0.855 | yes |
  | 2 | 0.713 | 0.662 | 0.705 | yes |
  | 3 | 0.822 | 0.533 | 0.581 | yes |
  | 4 | 0.888 | 0.454 | 0.502 | yes, at the boundary |
  Normal approximation; 5f only, so every other gate lowers P(pass). The instrument's lifetime budget is 4 looks (generation note §11).
- Power at expected event count, using power = Φ(√N·|δ|/σ − 1.96) with N = 2,325 dev sessions (√N = 48.22):
  - H1 pre-T: Φ(48.22×0.034 − 1.96) = Φ(−0.32) = **0.37** (fails 0.50)
  - H2 post-T: Φ(48.22×0.048 − 1.96) = Φ(0.33) = **0.63** (passes)
  - reversal H1+H2: Φ(0.87) = 0.81
  - break-even δ/σ for power 0.50 is 0.0406
  - H3: not computable (UNSCREENABLE). At N ≈ 670 gotobi sessions (calendar estimate) the break-even is δ/σ = 1.96/√670 = 0.076, which is 0.18 before the 0.42 haircut.
- Cost and entry-slip sensitivity (M-16, printed only):
  - Bulenox round-trip commission is 2 × $2.36 = $4.72 = **0.76 ticks** (tick $6.25).
  - One tick in bp = 0.005 × USDJPY level L (from ¥12.5M contract, $6.25 tick). L = 100 gives 0.50 bp; L = 150 gives 0.75 bp. These are illustrative levels, not cited figures.
  - Haircut per-event δ (annualized ÷ 252, an assumption) is pre-T 0.68 bp and post-T 1.32 bp:
    - At L = 100: 1.35 and 2.65 ticks gross, leaving **0.60 / 1.89 ticks** of total round-trip slip before the effect is consumed.
    - At L = 150: 0.90 and 1.76 ticks, leaving **0.15 / 1.01 ticks**.
  - At the repo's 1 tick/side modelled slip (2 ticks RT), every leg is net ≤ 0 at L = 150, and only post-T survives at L = 100. Entry is time-triggered (market or limit), not a stop entry, so M-16's stop-slip mechanism applies only weakly. The binding question is the limit-vs-market fill.
- Barrier feasibility: pending atlas (sibling session).
