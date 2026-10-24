# Next affordable uncertainty: can the rebalancing signal become a native Tradeify component?

**Date:** 2026-10-22 · **For:** Portfolio Research Manager · **Spend:** $0, public sources and repo records. No market data, backtests or parameter searches.
**Follows:** [next-mechanism scan](2026-10-22-next-mechanism-scan-memo.md) (its findings stand).
**Not readable from this cloud clone:** the HMM replication's local records; E1; ORB v7's direction and sizing; Tradeify support correspondence beyond what is committed. None of their contents is inferred here.

## 0. Recommendation

**Recommended action:** a native-deployability check on the Harvey–Mazzoleni–Melone (HMM) rebalancing signal.
- **Cost:** $0; about 2 h of desk work, one 5-minute operator platform check, and one Tradeify support question.
- **Why it ranks first.** HMM is the only live non-ORB candidate with a published effect clearly above the house cost hurdle.
  - The paper reports that a one-standard-deviation signal predicts about −16 bp (Threshold signal) or −17 bp (Calendar signal) in next-day equity returns, and +4 bp / +2 bp in bonds (NBER w33554).
  - The MES 4× hurdle is about 3.46 points (MOC-wake record, MES panel basis).
  - The coefficient is not a profit-per-trade figure. The replication owns that.
- **The uncertainty this resolves.** Whether a positive replication could be deployed natively at Tradeify at all. Three Tradeify rules bear on it directly (§1).
- **No duplication.** The check does not test the effect; that stays with the replication. It turns venue rules into acceptance criteria the replication can report against. Resolving them now prevents a positive result from landing on an expression Tradeify cannot run.

**Alternative (another vehicle).** HMM's own published trade — long S&P 500 futures / short 10-year Treasury note futures, or the reverse — reports a Sharpe ratio above 1 net of costs over 1997–2023. That expression fits the [self-funded lane](../../adr/2026-10-09-self-funded-tradovate-lane-reopen.md), which allows overnight holds and Treasuries, as published. It needs no new research beyond the replication, but it is gated by that lane's seven ADR items. Use it if §1 fails.

**Permission versus qualification.** Running this check grants nothing: it only says whether a positive replication *could* deploy. Deployment still needs the replication's own result, the harvest gates and the operator's arming and spend controls.

## 1. The check: four questions, the data each needs, and the decision each answer changes

| # | Question | Evidence needed | If NO | If YES |
|---|---|---|---|---|
| 1 | Does the Tradeify NinjaTrader/Tradovate feed stream real-time **ZN** quotes? The signal needs 10-year Treasury futures returns. Tradeify's help centre says CME Group Level 1 for "all major futures contracts" is included, but names no CBOT products. | Operator adds ZN to a chart on the Tradeify connection (5 min), or asks Tradeify support | The signal cannot be computed natively. HMM is not a Tradeify component; plan it for the self-funded lane. | Go to question 2 |
| 2 | Is reading a non-traded instrument's platform data inside NinjaScript "native strategy logic" under Tradeify's 2026-10-12 statement? (The statement bans external engines, bridges and the API; platform data is not obviously external.) | One support question, added to the [pending follow-up draft](../2026-10-21-tradeify-native-followup-questions-DRAFT.md) | Same as question 1, NO | Go to question 3 |
| 3 | Does the equity-only leg survive Tradeify's holding geometry? Tradeify has no Treasuries, so only an MES/ES leg is possible. The signal forms at day t's close; the hold runs from the 18:00 ET reopen to 16:44 ET, at one round trip a day. | The replication reports **equity-only** next-day returns over 18:00→16:44 ET, net of Tradeify MES/ES costs | HMM stays a two-asset, other-vehicle trade | Go to question 4 |
| 4 | Is the short-equity half compatible with any concurrent long index leg? Tradeify's hedging rule breaches on opposing positions in the same product group across **all accounts under control**, held over 10 s with hedge profit over $150 ([envelope](../../../ops/prop_envelope_default.md)). | The replication reports the long and short halves separately; the PRM states which index legs would run concurrently | Restrict to the long half (only if that half carries the effect), keep windows time-disjoint, or use another vehicle | A positive replication converts directly into a native build candidate |

**Inconclusive answers.** An unanswered support question or an ambiguous feed check means "treat as non-native": build nothing at Tradeify. The self-funded-lane alternative is unaffected.

**Market data and spending:** none proposed. The operator's chart check reads one quote to confirm a data entitlement; it is not research data.

## 2. The London-fix passive-execution lead (requested calculation): no procurement

**Contract:** full-size 6E at Tradeify.
- **Fact:** one tick is $6.25.
- **Assumptions:** $6.20 round-trip commission (6E is absent from the pinned [Tradeify schedule](../../../lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/tradeify_commission_schedule.json); the full-size 6J rate is used); EUR/USD at 1.16, so about $145k notional. On that basis the commission is 0.43 bp and one tick is 0.43 bp.

| Execution | Round trip (bp) | 4× hurdle (bp) |
|---|---|---|
| Repo convention (1 tick a side) | 1.29 | 5.2 |
| Taker (crosses one tick in total) | 0.86 | 3.4 |
| Passive, realistic (see below) | 0.65–0.86 | 2.6–3.4 |
| Passive, no adverse selection, every order filled | 0.43 | 1.7 |

**How the passive row is derived.** Cost per side is p·a + (1−p)·c:
- p is the fill rate; a is the post-fill adverse markout; c is the cost of chasing a missed fill (cross the spread plus the move away), all in ticks. A taker pays about 0.5 tick a side.
- At p = 0.7, a = 0.25, c = 1.0, the passive cost is 0.475 tick a side: almost no saving.
- At p = 0.9, a = 0.1, c = 1.0, it is 0.19 tick a side, saving about 0.27 bp per round trip.
- Missed fills cost little through lost drift, because the published drift accrues at roughly 0.01 bp a minute. They cost through chasing.

**Effect per leg.**
- Krohn–Mueller–Whelan, 1999–2019: about 3.1 bp gross (EUR Europe window, 15.6% a year across two legs).
- Recent evidence is about 2 bp: KMW's 2014–2019 pre-ECB dollar portfolio runs about 5% a year, and the repo's 2020–2026 EUR/USD post-fix mean move was about 2 bp ([register](../../rejected_candidates.md), FX fixing-reversal).

**Result.**
- At about 2 bp, the leg fails even the realistic passive hurdle. Only the zero-adverse-selection case passes, and that is not a plausible assumption for a retail queue position.
- What decides the question is the size of the *recent* effect, not execution. Measuring that ourselves would be the re-run Q-INVENTORY-1 bars.
- Do not procure L1 or fill data.
- The same arithmetic holds generally: on Tradeify micros, commission is most of the round trip (MNQ, $1.82 against a $0.50 tick). Passive execution cannot move a micro hurdle by more than about a third.

## 3. Other opportunities ranked below, and what failed in each

| Opportunity | Lens | What fails | Type of failure |
|---|---|---|---|
| Prop-firm flatten-deadline flow (e.g. a 16:10 ET firm deadline after the cash close) | Forced trader, new since the prop boom | No cohort effect exists (UNSCREENABLE). A post-close window must move about 3.46 MES points to clear cost, and fails the 2026-09-01 Vet-intake bar for a high-expectancy prior | Evidence |
| Short VSTOXX mini (FVS) volatility carry | Payoff pattern | The daily flatten makes each day a round trip, roughly equal to the daily roll-down (assumption). EUREX data is a paid add-on. It adds long-equity crash exposure | Vehicle / cost |
| Daily-reset trend or carry on FX, metals or energy | Payoff pattern | One round trip per day held; trend's win rate of 50% or less sits in the shape map's infeasible zone | Vehicle / shape |
| Session-open breakouts on MCL, MGC or 6E | Complement to ORB | No robust primary source found in this pass; ZB's opening range was sign-reversed (`ZB.md` B1) | Evidence |
| Native depth-imbalance signals | Execution / modality | Level 2 is a paid Tradovate add-on at Tradeify; the aggressor-flow variants are already falsified on MNQ | Cost (data) / mechanism |
| Treasury auction cycle; Gotobi | Forced trader | See the [scan memo](2026-10-22-next-mechanism-scan-memo.md) | Vehicle and decay; barred and below the cost hurdle |

## Sources

- Harvey, Mazzoleni and Melone, *The Unintended Consequences of Rebalancing*, [NBER w33554](https://www.nber.org/system/files/working_papers/w33554/w33554.pdf) (rev. January 2026); [SSRN 5122748](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5122748)
- Krohn, Mueller and Whelan, *Foreign Exchange Fixings and Returns Around the Clock*, [Bank of Canada SWP 2021-48](https://www.bankofcanada.ca/wp-content/uploads/2021/10/swp2021-48.pdf); J. Finance 2024
- Tradeify, [supported platforms](https://intercom.help/tradeify/en/articles/10468221-supported-platforms) and [data feed troubleshooting](https://help.tradeify.co/en/articles/12270225-data-feed-issues-and-market-data-troubleshooting)
- Repo records: [register](../../rejected_candidates.md) (MOC wake on MES; FX fixing-reversal; Q-INVENTORY-1), [prop envelope](../../../ops/prop_envelope_default.md), [`firm_rules.py`](../../../core/firm_rules.py)
