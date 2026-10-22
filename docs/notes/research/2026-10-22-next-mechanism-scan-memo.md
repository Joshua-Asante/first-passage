# Next-mechanism scan: is there a new driver beyond ORB and rebalancing worth testing?

**Date:** 2026-10-22 · **For:** Portfolio Research Manager · **Spend:** $0, about 2 h. Public sources and existing records only. No market data, backtests or parameter searches.
**Excluded by brief:** the ORB MNQ v7 build (local Codex) and the Harvey–Mazzoleni–Melone rebalancing replication (separate researcher).
**Vehicle assumed:** the current objective's vehicle is the Tradeify-native evaluation and funded account ([Q-PATH-TO-PAYOUT-1](2026-10-21-q-path-to-payout-1-memo.md)). The account must be flat by 16:45 ET, has no Treasuries, offers micro FX in M6E and M6A only, and full 6J ([`core/firm_rules.py`](../../../core/firm_rules.py) Tradeify block). Candidates that need overnight holds are listed separately.
**Not readable from this cloud clone:** the E1 record, the HMM work, and the private bodies in `first-passage-archive` (the closure RESULTS files linked from the register). Their contents are not inferred here; only the public register summaries are used.

## 0. Answer

**No mechanism sourced in this scan earns a funded test on the current vehicle.** This is a finding about the candidates examined here, not a proof that none exists. The two strongest fail for these reasons:

| Candidate | Who pays and why | Status | Decisive reason |
|---|---|---|---|
| A. Tokyo-fix "Gotobi" settlement-day USD demand (6J) | Japanese importers settle USD at the bank-set TTM rate on days divisible by 5 | **Barred, and below the cost hurdle** | The register bars "a different fix (Tokyo/Frankfurt)" as a re-tune of the FX-fixing family. Inside the Tradeify window, the published drift is about 1.2–1.8× round-trip cost, against a 4× requirement. |
| B. Treasury auction supply cycle (ZN/ZF) | Primary dealers with limited risk capacity absorb scheduled supply | **Intraday: below the cost hurdle. Multi-day: needs a different vehicle and has decayed** | Intraday, the effect is real but small (FLN six-hour window; H-ZNAUC-1 on ZN). The multi-day expression needs Treasuries (not available at Tradeify) and would pay a round trip at every daily 16:45–18:00 ET flatten, and FLN's 10-day estimates are mostly insignificant after 2015. Treasuries are not tradable at Tradeify at any horizon. |

**The specific evidence gap in this scan.** Every scheduled-flow mechanism with a named constrained payer that this scan sourced and that fits the vehicle's intraday window has a published intraday effect of about 1–3 bp per event. The house cost law ([Req-5](../../methodology/strategy_harvest.md)) requires the per-event effect to be at least 4× the round-trip cost; the recorded hurdles run from about 4.4 bp (6E) to 14.9 bp (MCL), each on its own contract and price basis (§3). The register already holds seven or more "real mechanism, below the cost hurdle" kills of this shape (D5, H-OD-1, H-ZNAUC-1, the FX London fix, TAS MCL, third-Friday MYM, H-FBEIA-1).

Flow premia are large enough to clear cost only over horizons of days, as with the auction cycle's 10-day V-shape. Tradeify allows a hold from the 18:00 ET reopen to 16:45 ET (about 22.75 hours), so a one-day horizon is legal. Each additional day held costs one more round trip at the daily flatten. Slow risk premia (carry, trend) clear cost but fail 90-day power and the venue's payout-shape test (H-TSMOM-1, the Koijen axis). Within this scan's search lens (scheduled flows with a named forced trader), a seed for this vehicle must show a cohort effect of at least 4× round-trip cost **inside one Globex session**. None of the sources below does. Other lenses, such as payoff shape, execution or validation design, are outside this scan.

**Most useful next step ($0, about 1 h, no new data).** Before sourcing any further mechanism for this vehicle, apply the §3 one-division screen at intake: the seed's cohort effect divided by the instrument's hurdle. The other admissible lever is the Req-5 redesign route on the *cost* side. Two re-proposal bars ([H-ZNAUC-1](../../rejected_candidates.md), [FX fixing-reversal](../../rejected_candidates.md)) already name "materially better-than-taker execution" as new evidence. The FX benchmark fix ([Krohn, Mueller and Whelan 2024](#sources)) is the closest killed mechanism: about 3.3 bp gross against a 4.4 bp hurdle (6E, at Q-INVENTORY-1's modeled 1.1 bp round trip), a shortfall of about 1.3×. Whether passive execution could close that gap after missed fills and adverse selection is a calculation to do from existing evidence before any data procurement. The 2026-10-22 follow-up does that calculation.

If the PRM opens an overnight-capable vehicle (the [self-funded lane](../../adr/2026-10-09-self-funded-tradovate-lane-reopen.md) permits holds), §2 says what remains of the best multi-day candidate. It is still not enough to fund.

## 1. Candidate A: Gotobi / Tokyo-fix settlement-day flow on 6J (compatible vehicle; barred)

**Mechanism.** Japanese import firms pay USD invoices on *gotobi* days (the 5th, 10th, 15th, 20th, 25th and month-end) at the TTM rate, which banks set at 9:55 JST. Banks know the demand in advance, buy USD ahead of the fix, and USD/JPY drifts up into 9:55 JST, then falls just after. Exporters follow no matching custom, so the flow is one-sided. The rule clause, "settlement custom, priced off a bank-set benchmark," passes Req-1a's constraint test.

**Primary sources and independence.**
- Bessho, Sugimoto and Suzuki (2023): EBS data for 2018–2020, 185 gotobi days.
- Akiyama, Sugimoto, Sakemoto and Suzuki (2021): same research group, so not independent of Bessho et al.
- Ito and Yamada (2017, JIE): Tokyo-fix order imbalance and bank pricing, independent. Its gotobi-specific magnitudes were not verified here (paywalled).
- Krohn, Mueller and Whelan (2024, JF): pre-fix USD appreciation and post-fix reversal across all fixes, including Tokyo, over 21 years. Independent, but it is the parent family the register already closed.

**Rule sketch.**
- On a Japanese business day that is a gotobi date, sell 6J at 18:00:30 ET, the Globex reopen.
- Cover at 9:54 JST: 19:54 ET under US standard time, 20:54 ET under daylight time.
- All inputs (calendar date and Japanese holidays) are known days ahead. It is native and fixed-parameter: a date list plus two clock times.

**Costs, full-size 6J at Tradeify.** Facts: $3.10 per side ($6.20 round trip); one tick is $6.25. Assumptions: a ¥12.5m contract at about 150 JPY/USD (about $83k notional), and a round trip costing one tick plus commission. On that basis the round trip is about **1.5 bp** and the 4× hurdle about **6 bp**.

**Effect inside the window.** The paper's Figure 1 (2018–2020) shows the gotobi path about 0.02–0.03 yen below its 9:55 level at 7:00–8:00 JST, which is the earliest Tradeify-legal entry. That is about **1.8–2.7 bp gross**. The paper's best leg (3:00→9:55 JST) is not available, because it crosses the 16:45 ET flat deadline and the 17:00–18:00 ET halt.
- Ratio to round trip: about 1.2–1.8×. Req-5 fails by roughly 2–3×.
- This is a magnitude read from a chart, not a cohort δ (per the brief: no coefficient-to-profit transfer).

**Portfolio contribution, if it had cleared.**
- Up to about 6 events a month (about 18 in 90 days), in Asian hours.
- Plausibly uncorrelated with US-morning equity legs.
- Same order symbol as Aegis 6J, if both ran in one account (single-position netting; see MYM F1). It is short-only, so it is exposed to the FX product-group opposing-direction rule if Aegis is long at the same time.

**Strongest reason it fails.** It is a calendar subset of the closed FX-fixing family, and inside the Tradeify window it is below the cost hurdle. The custom may also be eroding: the paper itself frames the anomaly as a leak that rational traders exploit.

**What would justify reconsideration.** A published, post-2020 gotobi cohort δ, measured inside the 18:00 ET–9:55 JST window on 6J, of at least 6 bp per event. A re-measurement of the same window on our own data would be the barred re-tune.

## 2. Candidate B: Treasury auction supply cycle (intraday below the cost hurdle; multi-day needs another vehicle and has decayed)

**Mechanism.** Auction timing and size are announced in advance. Dealers with limited balance sheet sell or short ahead of supply and buy back after. Yields rise into the auction and fall after: the price falls then recovers.

**Primary sources and independence.**
- Lou, Yan and Zhang (2013, RFS), 1980–2008. The 5-day pre-versus-post return gap was **22.54 bp (t=3.67)** for 5-year notes and **23.84 bp (t=1.78)** for 10-year notes. A hedged 2-year strategy had Sharpe 1.08 (1.44 in 1998–2008).
- Fleming, Liu and Nguyen (2026, NY Fed SR 1188, rev. July 2026), 1991–2024, BrokerTec. This is the independent extension and the decisive one. The intraday six-hour yield pressure is real and is shown by order flow. But the **post-2015 effect is "less than half" the earlier magnitudes**, at both intraday and daily horizons.
  - The 10-day on-the-run yield pressure for 2015–2024 is 1.53, −0.06, **2.62\*\***, 1.47, 1.17 and 1.61 bp for the 2Y, 3Y, 5Y, 7Y, 10Y and 30Y (Table A2). Only the 5-year is significant at 5%.
- Euro-area replications cited there: Beetsma et al. 2016 and 2018; Sigaux, ECB WP 2208, published in JBF 2023.

**Intraday evidence (separate from the multi-day trade below).**
- FLN six-hour window, 2015–2024, cash on-the-run: 10-year yield pressure 0.59 bp (p<0.1); 10-year price pressure 5.2 bp (p<0.1) (Tables 2–3).
- H-ZNAUC-1, ZN futures, 2010–2018: post-auction long only, held 15–60 minutes, measured 1.01 bp, killed by the cost hurdle (6–10 bp; see §3). The pre-auction leg was never tested, but the register bars window retunes of that construct.

**Register context.** [`ZN.md` R1](../../../ops/instruments/ZN.md) records tail exhaustion across the directional Treasury complex.

**Multi-day rule sketch (needs another vehicle).**
- Short ZF/ZN at the close five days before each 5-, 7- or 10-year auction, cover at the auction, then go long for five days.
- Inputs: TreasuryDirect quarterly tentative calendar; sizes announced about one week ahead. Holdings are overnight.

**Costs, full-size ZN (H-ZNAUC-1 basis: median price 126.4, 2010–2018).** About 1.25 bp per tick and about 1.5 bp per round trip including commission. The multi-day trade needs two round trips per cycle.

**Effect versus hurdle.**
- **Assumption:** about 6 bp of price per bp of yield for ZN.
- The post-2015 pooled cycle is about 1.2–1.5 bp of yield, about 7–9 bp of price. That is about 2.5–3.5× round-trip cost, under the 4× requirement.
- The 5-year alone (about 2.6 bp of yield) would clear. But choosing it from a six-maturity table is selection.
- An out-of-sample check (about 27 five-year auctions since August 2024) has δ/σ around 0.1 and cannot reach significance.

**Strongest reason it fails.** Documented decay, plausibly because non-dealers now absorb more supply (FLN's own explanation). It is also venue-dead at Tradeify: no Treasuries, and a round trip at every daily flatten.

**Decision value of a test.** Low. FLN already ran the experiment I would have proposed, the post-2008 out-of-sample check. An inconclusive futures re-run would only repeat that.

**Worth recording:** LYZ also report CRSP equities 49 bp (t=3.11) lower in the five days before 2-year auctions than after. They call the mechanism unclear. Those auctions fall in the last week of the month, so the window overlaps the HMM month-end window. Do not open it without HMM's results in hand.

## 3. Intake screen for this vehicle: minimum per-event cohort δ (from existing records)

| Contract | 4× round-trip hurdle (bp/event) | Basis as recorded by the source | Source |
|---|---|---|---|
| ES | 5.05 | IS-panel price, the record's execution model | H-OD-1, via [Req-5 precedent](../../methodology/strategy_harvest.md) |
| MNQ | 11.06, then 3.01 after re-costing | D5 cost geometry, then D5-RECOST-1's | D5 / D5-RECOST-1 ([`MNQ.md`](../../../ops/instruments/MNQ.md)) |
| MYM | 6.57 | the closure's native-micro cost model | third-Friday closure ([register](../../rejected_candidates.md)) |
| 6E (size as modeled) | 4.4 | 1.1 bp modeled round trip | Q-INVENTORY-1 FX-fix row |
| 6J (full, Tradeify) | about 6 | §1 assumptions (one tick plus $6.20, about 150 JPY/USD) | this memo |
| MCL | 14.87 | 11.60 ticks per event, 2023 panel price | Q-MCLTAS-1 |
| ZN (not Tradeify-legal) | 6 single round trip / 10 two round trips | 1.5 / 2.5 bp round trip, median price 126.4 | H-ZNAUC-1 |

A seed whose cohort δ is below its row dies at intake, at the cost of one division. Recompute at the campaign's panel-basis price before relying on any row (Req-5).

## 4. Mechanisms checked and already owned by the register (not reopened)

- **Barred:** pre-FOMC drift, announcement-day returns, macro pre-release drift, FX fixing-window drift (Q-INVENTORY-1); London fix and fix wake; leveraged-ETF end-of-day rebalancing; MOC imbalance; intraday momentum (Baltussen); the overnight/European-open drift (H-OD-1, NOCT-SPX); third-Friday settlement; TAS on MCL; EIA post-release; turn-of-month; dealer-gamma sign; COT positioning extremes; own-sign carry timing; time-series momentum (H-TSMOM-1).
- **Not barred, but already dead by vehicle or prior evidence:**
  - Commodity-index (GSCI) roll on MCL: SFX-1 is dead.
  - Bank of Japan ETF-purchase afternoon support on NKD: the regime ended in 2024 when the BoJ stopped purchases.
  - Mortgage-convexity hedging flows (Hanson 2014; Malkhozov et al. 2016): multi-day, Treasuries-only, and dormant while mortgages sit far out of the money.
  - Vol-targeting and risk-control close flows: no primary futures-level δ found. It sits inside the end-of-day raised bar and is a rebalancing cousin of HMM.

## Sources

- Bessho, Sugimoto and Suzuki (2023), *Forex Trading Strategy That Might Be Executed Due to the Popularity of Gotobi Anomaly*, [arXiv 2301.13204](https://arxiv.org/abs/2301.13204)
- Ito and Yamada (2017), *Puzzles in the Tokyo fixing in the forex market: order imbalances and bank pricing*, J. International Economics, [doi:10.1016/j.jinteco.2017.09.005](https://doi.org/10.1016/j.jinteco.2017.09.005)
- Krohn, Mueller and Whelan (2024), *Foreign Exchange Fixings and Returns Around the Clock*, J. Finance 79, [doi:10.1111/jofi.13306](https://doi.org/10.1111/jofi.13306)
- Lou, Yan and Zhang (2013), *Anticipated and Repeated Shocks in Liquid Markets*, RFS 26(8). Working paper: [FMG DP 684](https://www.fmg.ac.uk/sites/default/files/publications/DP684.pdf)
- Fleming, Liu and Nguyen (2026), *Intraday Price Pressure and Order Flow Around U.S. Treasury Auctions*, [NY Fed Staff Report 1188](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr1188.pdf)
- Sigaux, *Trading ahead of Treasury auctions*, [ECB WP 2208](https://www.ecb.europa.eu/pub/pdf/scpwps/ecb.wp2208.en.pdf); JBF 2023
- *The treasury auction risk premium*, JBF 170 (2025), [RePEc](https://ideas.repec.org/a/eee/jbfina/v170y2025ics0378426624002309.html), abstract only
