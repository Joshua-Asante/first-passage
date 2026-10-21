# Published-rule candidates for a Tradeify-only native strategy: sourcing pass (2026-10-21)

**Status:** sourcing note.
- **Cost:** zero K, $0, no data read.
- **What it doesn't do:** it opens no manifest and admits nothing.
- **What it serves:** decision D2 of the [native strategy plan](../../superpowers/plans/2026-10-21-tradeify-native-ninjascript-strategy-plan-DRAFT.md#6-decisions-for-joshua), and the bracketed rule in the [follow-up draft](../2026-10-21-tradeify-native-followup-questions-DRAFT.md).

**Question:** is there a published intraday rule, with published parameters and flat by the close, that is native-implementable on a Tradeify Select account and clears this repo's harvest admission?

**Answer:** not on index or gold micros. Every candidate found fails at sourcing-time sniff level, or is barred by an existing domain bar or closure. The repo's own findings already predicted this:
- [Q-INVENTORY-1](../../rejected_candidates.md) (0 of 8 staged rows admissible);
- the 2026-07-21 index-intraday raised bar (rejected register, "Single-instrument index-futures intraday OHLCV directional timing");
- MNQ N3 ([`ops/instruments/NQ.md`](../../../ops/instruments/NQ.md)).

**Labels:**

| Label | Meaning |
|---|---|
| [FT] | Read from the paper's full text |
| [ABS] | Read from the abstract only |
| [3P] | Independent but non-peer-reviewed replication |
| [SEC] | Secondary source, unverified |
| [INF] | This note's arithmetic |

## 1. Gates applied (all existing; none new)

| Gate | Source | What it requires |
|---|---|---|
| Tradeify fit | Native plan §1 | Intraday and flat by 16:45 ET; holds over 10 s; at least one trade a week; native NinjaScript; not the same bot as any other firm's strategy |
| Req-5 cost law, sourcing time | [`strategy_harvest.md`](../../methodology/strategy_harvest.md) §1, §2.2 | Per-event δ ≥ 4 × round-trip cost |
| Req-4 power | Same | Confirm-power ≥ 0.50; event frequency daily or intraday |
| Domain bar | Rejected register, 2026-07-21 raised bar | Admits a new single-index intraday OHLCV directional rule only if: (1) its mechanism lies outside the mapped price, cross-instrument and hold-time levers; (2) it uses a different modality; or (3) it beats incumbent ORB-MNQ net of costs |
| Dedup | Rejected register; MNQ N3 | A dead class stays dead under a new citation |
| Cross-firm | Tradeify FTA §6.6 | ORB MNQ v7 is the four-firm §4 candidate ([#864](https://github.com/Joshua-Asante/first-passage/pull/864)) |

**4× cost floor at the Tradeify basis** [INF]: `lab/discovery/cost_model.bp_hurdle`, firm `Tradeify_Select_50K` ($0.91/side), 1 tick/side slippage, per-side convention. MGC was computed by hand at $1.06/side, because the firm row is index-micro only.

| Micro | Price range | 4× floor |
|---|---|---|
| MNQ | 11,000–16,000 | 5.1 → 3.5 bp |
| MES | 3,800–5,000 | 9.1 → 6.9 bp |
| MYM | 31,000–38,000 | 7.3 → 5.9 bp |
| MGC | 1,700–2,300 | ≈ 9.7 → 7.2 bp |

## 2. Candidates

| # | Published rule | Tradeify fit | Cost law (sniff) | Bars / dedup | Verdict |
|---|---|---|---|---|---|
| 1 | **Noise-area breakout + VWAP trail** (Zarattini, Aziz, Barbon 2024, SSRN 4824172; working paper). Details below | Fits: intraday, about 1.8 trades a day | **FAIL on MNQ.** About 2.1 bp gross per trade vs 4.2 bp at 13,500. ES is negative after publication. Details below | Domain bar applies: same gamma-hedging mechanism as D5, so it needs route 3 (beat ORB-MNQ net). MNQ N3 says the class is "statistically absent on modern MNQ" | **Not admissible.** Closest candidate; fails cost by about 2× |
| 2 | **5-min opening-range breakout** (Zarattini & Aziz 2023, SSRN 4416622). Direction of the first 5-min candle; stop at its extreme; 10R target or exit at the close [FT]. QQQ 2016–2023: Sharpe 1.12, +0.13R per trade, no slippage [FT] | Fits | Third-party CFD replication (2015–2026, paper parameters): net NQ +0.002R; SPX, Dow and FTSE −0.08R [3P] | ORB family: a different ORB window is the "exhausted move" under the bar. Same class as ORB-MNQ, the four-firm §4 candidate, so the "same bot" risk applies | **Excluded** |
| 3 | **Last-half-hour momentum** (Gao, Han, Li, Zhou 2018, *JFE*). Sign of r(prior close → 10:00) sets the 15:30–16:00 trade [FT]. SPY Sharpe 1.08; about 2.6 bp gross per trade [FT/INF] | Fits | FAIL: about 2.6 bp vs 3.5–9 bp | D5 class: dead on cost (2026-07-16) and decayed OOS (D5-RECOST, 2026-07-21) | **Dead class** |
| 4 | **Hedging-demand intraday momentum** (Baltussen et al. 2021, *JFE*) [ABS] | Fits | Was D5's δ: 1.46 bp vs 11.06 bp | Is D5 | **Dead** |
| 5 | **Leveraged-ETF rebalance front-run** (Rodier/Shum et al. 2012; *RoF* 2016). At 14:45, if the market is ±2%, trade with it to the close; +0.60% per trade gross, 128 trades 2006–2011, clustered in 2007–08 [SEC] | **Fails** the weekly-activity rule alone (about 25 trades a year, bunched in crises) | Clears per event | Req-4 power: few events, mostly in crises. End-of-day raised bar 2026-08-02, row 4: equity-close-flow subgroups underpowered 2–5×. LETF effect decaying [SEC] | **Dead (power)** |
| 6 | **Pre-FOMC drift** (Lucca & Moench 2015, *JF*) [FT] | **Fails**: the published rule holds overnight | n/a | Q-INVENTORY-1: power-dead after 2016; decayed after 2015 [ABS] | **Dead** |
| 7 | **London PM gold fix leakage** (Caminschi & Heaney 2014, *JFM*) [FT] | Not a tradable rule: the benchmark is an informed trader with foresight | n/a | The fix it studied was replaced by an electronic auction in 2015 (unverified this pass). Gold benchmark-fix family R8 already dead | **Dead** |
| 8 | Gap fade, VWAP/Bollinger reversion, 8:30 macro drift | — | — | No peer-reviewed or working-paper rule with parameters found; theses and blogs only | **None found** |

**Row 1 detail: the rule** [FT]
- **Bands:** max(open, prior close) × (1 ± σ14). σ14 is the 14-day mean absolute move from the open to each half-hour.
- **Entry:** checked only on the half-hour.
- **Exit:** stop at the band or the regular-hours VWAP, whichever is tighter; flat at 16:00.
- **Sizing:** volatility-targeted to 2% a day, capped at 4×.
- **Reported:** SPY 2007–2024, Sharpe 1.33, 19.6% a year, max drawdown 25%, about 1.8 trades per traded day.

**Row 1 detail: the cost sniff.** The third-party MNQ replication used 1 micro, $1.75 round trip plus 1 tick a fill [3P]:

| Market | Daily result | t | Post-publication |
|---|---|---|---|
| NQ 2010–2026 | +$5.35 | 2.74 | t = 1.37 |
| ES | −$0.25 | — | −$5.56 a day |

Converting the NQ figure:
- per trade gross ≈ $5.35/1.8 + $2.75 ≈ $5.7;
- at MNQ notional 13,500 × $2, that is ≈ **2.1 bp** [INF];
- the 4× floor at the same price is **4.2 bp**.

## 3. What this means for D2

1. **The published-rule route is effectively closed on index micros** for a Tradeify-only strategy.
   - The one rule that fits Tradeify's mechanics (row 1) fails the cost law by about 2× on the best index, MNQ.
   - It also sits under the same mechanism finding that killed D5.
   - The ORB family is the incumbent and is already allocated elsewhere.
2. **Options still open** (none is recommended here):
   - **D2(b):** reassign ORB MNQ v7 to Tradeify-only. It is the domain's only survivor, and it trades the four-firm candidate.
   - **Domain-bar route 2:** a different modality, for example order flow computed natively in NinjaScript from Tradeify's data. No published, parameterised order-flow rule with δ above the cost floor was found in this pass, and it would need its own sourcing pass. Native order-flow features may also depend on a NinjaTrader entitlement, which is a P1 check.
   - **Non-index micros:** CL/MCL, FX and gold intraday literature is already largely closed in the register: EIA, TAS, FX fixing, gold fix. A new pass would need new mechanism evidence.
   - **Park Tradeify:** 11-08 branch (d).
3. **Follow-up draft:** the bracketed rule cannot be filled from this pass. Sending the ownership question is premature until D2 picks a candidate; if D2(b) is chosen, the question changes, because ORB v7 is an in-house strategy, not a published rule.

## 4. Sources

Papers:
- Zarattini, Aziz, Barbon, SSRN 4824172 / SFI RP 24-97: https://www.alexandria.unisg.ch/entities/publication/71ef0a23-34e3-4b37-a8d7-d98285579662
- Zarattini & Aziz, SSRN 4416622: https://wealth-lab.com/api/discussion/download/pdf/6590-ORB-Strategy-pdf
- Gao, Han, Li, Zhou, SSRN 2440866: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2440866
- Baltussen et al., SSRN 3760365: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3760365
- Shum et al., *RoF* 2016: https://ideas.repec.org/a/oup/revfin/v20y2016i6p2379-2409..html
- Lucca & Moench, SR 512: https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr512.pdf
- Kurov, Wolfe, Gilbert 2021: https://ideas.repec.org/a/eee/finlet/v40y2021ics1544612320315956.html
- Caminschi & Heaney 2014: https://api.research-repository.uwa.edu.au/ws/files/4725264/A0205_use_this.pdf

Third-party replications:
- [3P] VigorTas replication: https://github.com/VigorTas/beat-the-market-replication
- [3P] MQL5 ORB replication: https://www.mql5.com/en/blogs/post/776235

In-repo:
- Rejected register entries cited above.
- `ops/instruments/NQ.md` N3.
- [MNQBASE-1 closure](../../briefs/closures/MNQBASE-1-closure-intake-dry.md), which cites arXiv 2605.04004 (MNQ 14-family OHLCV falsification).
