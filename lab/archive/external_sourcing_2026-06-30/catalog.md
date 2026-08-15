# External-strategy sourcing — Harvest catalog (§2.2)

**Generated:** 2026-06-30 from Workflow `wf_6a7fc6ff-c94` (13 mechanism-family deep searches -> adversarial source-verify -> synthesize).
**Counts:** raw=69 deduped(exact-name)=69 verified=69 source-CONFIRMED=65.

**Provenance caveat (load-bearing):** all `claimed_performance` is source-stated, NOT primary-table-verified (SSRN PDFs 403, QuantifiedStrategies CAPTCHA-walled, TradingView backtest tabs JS-gated). Performance numbers carry ZERO evidential weight under Edit-1; the OOS gate runs on OUR panels.

## Synthesis headline

> Source-verification yield is moderate, not thin: of ~50 rows, 46 carry a CONFIRMED verdict and 4 are excluded as MISREPRESENTED. After merging heavy semantic duplication (the Connors RSI(2) / cumulative-RSI / IBS oscillator cluster, the overnight-intraday reversal cluster, the gap-fade cluster, the carry cluster, and the band-fade cluster each had 3-6 near-identical rows), roughly 30 distinct CONFIRMED chop/MR/range candidates survive. The catalog is dominated by short-horizon oscillator/close-location mean-reversion (Connors family + IBS), overnight/intraday session reversal (Tug-of-War / Della Corte-Kosowski / Liu et al. cluster), gap-fade-to-prior-close, band/z-score fades, carry/term-structure, calendar seasonality, and stat-arb spread reversion — but the strongly-grounded tail (peer-reviewed, returns-independent side-prediction, regime-conditioned) is much smaller than the raw count, and almost every row is documented on US equity ETFs/indices or broad multi-asset baskets, so transfer to the in-scope FXIFY/futures instruments and 15m timeframe is an untested extrapolation in nearly every case.

## Verified rows (CONFIRMED), grouped by reported mechanism family

### z-score / standard-deviation mean reversion

- **Z-Score SMA-deviation reversion on SP500 futures (StatOasis)** — instr: SPX500, MNQ, MYM | d=2025-03-21
  - mechanism: Z = (Close - SMA) / rolling stdev of price. Enter long when Z < -1; exit when Z returns toward neutral (~0.1-0.5) or after a 5-bar fixed exit. Adds an ATR filter (ATR10 < ATR10[1], i.e. contracting volatility) to refine entries.
  - chop-fit: Buys mean-reverting stretches and exits on reversion to mean, profiting precisely when index price oscillates around its average rather than trending; the ATR-contraction filter further concentrates entries in range/chop regimes.
  - side-prediction (candidate): The ATR10<ATR10[1] (contracting-volatility) entry filter implies the edge concentrates on low-and-falling realized-vol days; a returns-independent check is whether the proportion of signal bars with falling ATR is materially above base rate, i.e. signals cluster in vol-contraction windows. | independence=no-reduces-to-pnl
  - claimed perf (UNVERIFIED): SP500 futures daily, ~18yr: win rate 74%, net profit $148,187, avg profit/trade $516, max DD $30,237 (author-stated, no out-of-sample split disclosed).
  - source: StatOasis, 'Understanding Z-Score and Its Application in Mean Reversion Strategies', published 2025-03-21. Backtest stated on SP500 futures daily bars, 18-year history: 74% win rate, net $148,187, avg $516/trade, max DD $30,237. <https://statoasis.com/post/understanding-z-score-and-its-application-in-mean-reversion-strategies>

### standard-deviation band mean reversion

- **QuantConnect 1-stdev 30-day mean-reversion (research docs example)** — instr: SPX500 | d=undatable
  - mechanism: Compute 30-day rolling mean and standard deviation; an asset trading more than 1 standard deviation below its 30-day mean is flagged 'due to revert'. Enter the most-stretched names, hold ~1 trading day, rebalance. Documented on an 18-ticker fixed-income ETF basket (SHY, TLT, EDV, etc.).
  - chop-fit: The whole premise is buying a >1 SD downside deviation from a rolling mean and exiting on snap-back, which earns when price ranges around its mean and loses when a deviation extends into a trend - the opposite payoff profile to the book's breakout legs.
  - side-prediction (candidate): Mechanism implies the buy-side deviation reverts only if the underlying return series is stationary; a returns-independent test is a variance-ratio / ADF stationarity check on the candidate instrument's 30-day-detrended price - reversion edge should track low variance-ratio (mean-reverting) windows. | independence=yes
  - claimed perf (UNVERIFIED): 2021 backtest equity curve shown as positive on a fixed-income ETF basket; no Sharpe / return / win-rate figures published, no instrument-universe scoping to the search universe.
  - source: QuantConnect Documentation, 'Mean Reversion' (Research Environment / Applying Research). 30-day mean, 1 SD threshold, 1-day hold; 2021 backtest equity curve shown (positive) on an 18 fixed-income ETF basket. <https://www.quantconnect.com/docs/v2/research-environment/applying-research/mean-reversion>

### regime-conditioned z-score mean reversion

- **Regime-conditioned statistical z-score mean reversion for intraday FX (Bhatti)** — instr: USDJPY, EURUSD, USDCAD, GBPUSD | d=2026-01-17
  - mechanism: Volatility-normalized price deviations (z-scores) generate entry signals; higher-timeframe momentum state classifies regime and gates execution (suppress MR when higher-TF is trending), with volatility-adjusted position sizing. MQL5 prototype provided.
  - chop-fit: Explicitly built to pay in liquidity-imbalance/dealer-inventory reversion (chop) and to SWITCH OFF during trends via a higher-TF momentum gate - the exact regime-decorrelation property the book needs against its trend legs.
  - side-prediction (candidate): Mechanism attributes reversion to dealer inventory / liquidity imbalances, predicting the MR edge should correlate with bid-ask-spread widening and order-flow imbalance signatures at entry - a returns-independent microstructure check. | independence=yes
  - claimed perf (UNVERIFIED): Abstract describes framework + MQL5 prototype; no out-of-sample performance numbers extracted (full text not retrievable, SSRN 403). Treat as mechanism source, not performance source.
  - source: Amaanullah Bhatti, 'A Regime-Conditioned Statistical Mean Reversion Framework for Intraday FX Markets', SSRN working paper 6087107, posted 2026 (Jan). Abstract verified via search snippet; full PDF behind SSRN 403, metadata checkable on SSRN. <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6087107>

### oscillator-reversal mean reversion

- **Connors RSI(2) short-term mean reversion (with 200MA trend filter)** — instr: SPX500, DJ30, NAS100 | d=2008
  - mechanism: On an index/ETF: if Close > 200-day MA and 2-period RSI < 5 (Connors also uses <10), buy; exit when Close > 5-day MA. Symmetric short when Close < 200MA and RSI2 > 95. No hard stops (Connors found stops hurt on indices).
  - chop-fit: Fades short-term oscillator extremes back to a 5-day mean, harvesting the pullback-and-revert behavior of an index inside a range; it is flat ~72% of the time and trades the counter-swing the book's momentum legs ignore.
  - side-prediction (candidate): Mechanism predicts the reversion is a short-horizon pullback inside an up-trend, implying entries cluster on down-days that do NOT breach the 200MA; returns-independent check: conditional autocorrelation of 1-3 day returns should be negative at RSI2 extremes. | independence=yes
  - claimed perf (UNVERIFIED): SPY 1993-present (QuantifiedStrategies restatement): ~9% annual return while only ~28% invested. Original Connors testing across indices/ETFs; widely-replicated, but a 2008-vintage published edge (decay risk).
  - source: Larry Connors & Cesar Alvarez, 'Short Term Trading Strategies That Work' (TradingMarkets, 2008) - original source. Rules + SPY backtest (1993-present: ~9% annual, ~28% time in market) restated at QuantifiedStrategies.com and StockCharts ChartSchool 'RSI(2)'. <https://www.quantifiedstrategies.com/rsi-2-strategy/>
- **Cumulative RSI(2) mean reversion (Quantitativo)** — instr: SPX500, NAS100 | d=2024-06-22
  - mechanism: Sum the 2-period RSI over 2 consecutive days (cumulative RSI). Enter long when cumulative RSI2 < 10 and price > 200-day MA; exit when cumulative RSI2 > 65. Max 3 concurrent positions, liquidity-screened universe.
  - chop-fit: Buys sustained short-term oversold dips and exits on reversion, profiting from index pullback-and-revert oscillation rather than trend continuation; selective (3 positions) and counter-swing to the momentum book.
  - side-prediction (candidate): Cumulative-vs-single RSI2 implies the marginal edge comes from requiring multi-day persistence; returns-independent check: signal frequency should drop sharply and entry days should show higher 2-day downside persistence than single-bar RSI2 triggers. | independence=yes
  - claimed perf (UNVERIFIED): S&P 500 large/mega-cap, 1999-2023: 26.6% annual return, Sharpe 1.18, max DD 37%, win ~65%. Author notes only 'marginally better' than vanilla RSI2 - modest incremental edge.
  - source: Quantitativo (Quant Trading Rules, Substack), 'Squeezing more profits with cumulative RSI', published 2024-06-22. Backtest 1999-2023 on large/mega-cap S&P 500 names: 26.6% annual, Sharpe 1.18, max DD 37%, ~65% win. <https://www.quantitativo.com/p/squeezing-more-profits-with-cumulative>

### Bollinger-band mean reversion

- **Bollinger Bands Mean Reversion 'by Kevin Davey' (TradingView, EdgeTools)** — instr: XAUUSD, DJ30, NAS100, SPX500 | d=2024-10-24
  - mechanism: 20-period SMA Bollinger Bands at 2.0 standard deviations. Enter long when price closes BELOW the lower band (anticipating reversion to the SMA midline); exit when price closes ABOVE the upper band.
  - chop-fit: Fades 2-SD band breaches back to the mean, which earns when price ranges inside/around the bands and loses when price 'walks the band' in a trend - structurally anti-correlated with the book's breakout/pyramid legs.
  - side-prediction (candidate): none-apparent (rules-only script; the only implication is the generic band-width one - reversion works when Bollinger bandwidth is low/contracting, which is a checkable volatility-regime signature but not specific to this script). | independence=none-apparent
  - claimed perf (UNVERIFIED): None published on the script page - rules-only. Instrument-agnostic open-source script; would need own backtest. Kevin-Davey attribution unverified beyond title.
  - source: TradingView open-source strategy 'Bollinger Bands Mean Reversion by Kevin Davey', published by EdgeTools, 2024-10-24. Rules verified on script page; no performance metrics published on the page; Kevin-Davey attribution is in-title only. <https://www.tradingview.com/script/umOCSa0t/>

### z-score mean reversion (multi-filter)

- **Z-Score Mean Reversion Pro (TradingView, ayusattv)** — instr: XAUUSD, DJ30, NAS100, EURUSD, GBPUSD | d=undatable
  - mechanism: Combines statistical Z-score extremes with RSI momentum confirmation, Bollinger-band volatility filtering, and EMA trend alignment to time mean-reversion entries; specific threshold values not published on the page. Open-source.
  - chop-fit: Explicitly a z-score reversion entry with a Bollinger volatility filter and EMA gate intended to catch reversion to mean on indices/gold/FX intraday - thesis-aligned chop payoff, but underspecified.
  - side-prediction (candidate): none-apparent (exact thresholds undisclosed; cannot derive a checkable returns-independent implication beyond the generic z-extreme = stretched-from-mean claim). | independence=none-apparent
  - claimed perf (UNVERIFIED): None published - rules described qualitatively, exact z-score lookback/thresholds not disclosed on the page. Author self-describes intended markets/timeframes only.
  - source: TradingView open-source strategy 'Z-Score Mean Reversion Pro' by ayusattv, published May 3 (year unspecified on fetched page). Stated as best on 5m/15m/1H/4H across Forex, Crypto, Indices, liquid Stocks. No performance metrics published. <https://www.tradingview.com/script/92rilzXd-Z-Score-Mean-Reversion-Pro/>

### standard-deviation / mean reversion (academic survey-build)

- **QuantConnect mean-reversion suite (Vu & Bhattacharyya)** — instr: SPX500, NAS100 | d=2024-06-27
  - mechanism: Paper designs and backtests mean-reversion strategies (Bollinger-band / standard-deviation style and pairs/statistical reversion) on the QuantConnect platform for intraday NYSE equities, deployable to live brokers; uses standard-deviation bands around a moving average as the core reversion signal.
  - chop-fit: SD-band reversion that buys below-mean stretches and sells reversion is a chop-paying mechanism; the paper is most useful as a mechanism + cost-realism reference (its own result flags that intraday equity reversion can be eaten by costs).
  - side-prediction (candidate): The paper's own finding implies the edge is gross-positive but cost-fragile; returns-independent check: per-trade gross excursion vs round-trip cost - reversion edge survives only where mean-distance at entry exceeds the cost hurdle, a checkable spread/cost ratio. | independence=yes
  - claimed perf (UNVERIFIED): Paper reports the realistic-cost problem directly: an intraday SD-band reversion produced very low net results once commissions were applied (a noted ~2% win-rate / 26-cent-gross-eaten-by-fees failure mode) - a cautionary, cost-sensitive result rather than a strong edge.
  - source: Duc Long Vu & Ritabrata Bhattacharyya, 'Design and Development of Mean Reversion Strategies on QuantConnect Platform', SSRN 4878676 (2024); mirrored on ResearchGate publication 381942833. Metadata verified via search; PDF behind SSRN 403. <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4878676>

### oscillator mean-reversion / short-period RSI fade

- **Connors RSI(2) mean-reversion (long pullbacks above 200-SMA)** — instr: SPX500/US500, DJ30, NAS100, MGC, MYM, MNQ | d=2008
  - mechanism: Larry Connors' 2-period RSI system: trade only in the direction of the 200-day SMA (long when price > 200-SMA). Enter long when RSI(2) closes below 5 (more aggressive) or below 10; exit on a close above the 5-day SMA (some implementations exit when RSI(2) rises above 65-70). No stop-loss in the original system; the 200-SMA acts as the structural filter. Connors found returns are higher the deeper RSI(2) dips (below 5 > below 10). Symmetric short side: short when price < 200-SMA and RSI(2) > 95/90.
  - chop-fit: It is an explicit counter-trend fade that buys brief oversold spikes and sells the snap-back, so it earns in choppy/range/follow-through-deficit conditions where a deep 1-4 day dip reverts rather than continuing — exactly when the book's trend/breakout legs go flat.
  - side-prediction (candidate): Returns-independent implication: the conditional probability that a daily close N days after an RSI(2)<5 reading lies above the entry close should exceed the unconditional base rate (a short-horizon reversion signature measurable from price alone, no P&L needed). Also: average forward 3-day realized return after RSI(2)<5 should be positive and larger than after RSI(2)<10, monotone in dip depth. | independence=yes
  - claimed perf (UNVERIFIED): QuantifiedStrategies cites ~9% annualized on SPY since 1993 while invested only ~28% of the time, ~34% max drawdown; equity win rate >75%, most trades exit in 3-7 days. Connors' own testing across hundreds of thousands of trades reported >70-85% win rates on broad indices. Note: documented to underperform from ~2014 onward.
  - source: StockCharts ChartSchool, 'RSI(2)' (Trading Strategies and Models); strategy attributed to Larry Connors & Cesar Alvarez, 'Short Term Trading Strategies That Work' (2008). Corroborated by QuantifiedStrategies.com 'RSI 2 Strategy' page. <https://chartschool.stockcharts.com/table-of-contents/trading-strategies-and-models/trading-strategies/rsi-2>

### oscillator mean-reversion / cumulative short-period RSI fade

- **Cumulative RSI(2) (sum-of-RSI(2) sustained-oversold variant)** — instr: SPX500/US500, DJ30, NAS100, MGC, MYM, MNQ | d=2008
  - mechanism: Connors-Alvarez cumulative variant: instead of a single RSI(2) reading, sum RSI(2) over the last 2-3 days. Buy when the cumulative (e.g. 2-day or 3-day) sum of RSI(2) is below a threshold (~10 for 2-day sum, or 3-day sum below 20), with price above the 200-day MA; exit when the cumulative RSI(2) rises above ~65. quantitativo.com adds operational filters (max 3 concurrent positions, liquidity/size caps, prefer lower-cap names within a large/mega-cap universe).
  - chop-fit: Same chop-paying fade mechanism as RSI(2) but tuned to require multi-day sustained oversold pressure, so it concentrates entries in range/pullback conditions and avoids one-bar noise — pays when trend continuation stalls.
  - side-prediction (candidate): Returns-independent: forward 2-3 day reversion probability conditioned on cumulative-RSI(2)<threshold should be HIGHER and more stable than conditioned on a single RSI(2)<5 reading (a measurable property of the price series), i.e. signal persistence/clustering of oversold days predicts a stronger snap-back. | independence=yes
  - claimed perf (UNVERIFIED): quantitativo backtest (large/mega-cap US stocks, 1999-2024): ~26.6% annual return, Sharpe 1.18, ~37% max drawdown (vs vanilla RSI ~26.8%, Sharpe 1.05). Original Connors book: cumulative RSI(2)<20 (3-day) reported ~88% accurate on SPY; the cumulative filter raised win rate vs single-reading with fewer signals. Author declined to trade it live due to drawdown and post-2014 underperformance.
  - source: quantitativo.com, 'Squeezing more profits with cumulative RSI', published 2024-06-22; method attributed to Connors & Alvarez, 'Short Term Trading Strategies That Work' (2008). Original book reports the cumulative RSI(2) variant was ~88% accurate on SPY 1993-publication. <https://www.quantitativo.com/p/squeezing-more-profits-with-cumulative>

### oscillator mean-reversion / composite short-period RSI fade

- **ConnorsRSI (CRSI) composite oscillator fade** — instr: SPX500/US500, DJ30, NAS100, XAUUSD, MGC, MYM, MNQ | d=2012
  - mechanism: ConnorsRSI(3,2,100) = [RSI(3) of price + RSI(2) of the up/down streak length + PercentRank(100) of the 1-day return] / 3. Mean-reversion use: buy when CRSI falls below an oversold extreme (Connors recommends 10, or 5 for volatile instruments) and exit when it rebounds above a level (e.g. above 50, or the 5-day SMA cross); symmetric short above 90/95. The streak-RSI component punishes long consecutive down-runs and the PercentRank component flags an unusually large single-day move, so all three legs spike to extremes together at a genuine short-term washout.
  - chop-fit: Pure counter-trend washout fade — fires only on triple-confirmed short-term oversold extremes and exits on the bounce, so it monetizes range/MR snap-backs and follow-through-deficit days rather than trend continuation.
  - side-prediction (candidate): Returns-independent: the three sub-components (RSI3, streak-RSI2, PercentRank of return) should be POSITIVELY correlated at the moment of an extreme CRSI reading (they co-spike), and forward short-horizon reversion probability should be measurably higher when all three are extreme than when only RSI3 is — a structure checkable from the indicator series alone, no P&L. | independence=yes
  - claimed perf (UNVERIFIED): No single canonical backtest on the ChartSchool reference; QuantifiedStrategies' ConnorsRSI page reports broad-index win rates around 75% for CRSI-based oversold entries. Performance figures are less standardized than RSI(2); treat as needing independent re-test.
  - source: StockCharts ChartSchool, 'ConnorsRSI'; indicator developed by Larry Connors / Connors Research (introduced 2014). Formula and 10/90 (or 5/95) oversold/overbought thresholds corroborated by TradingView CRSI docs and backtrader CRSI recipe. <https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/connorsrsi>

### oscillator mean-reversion / %R range-fade

- **Williams %R short-period oversold fade** — instr: SPX500/US500, NAS100, DJ30, MYM, MNQ | d=1973
  - mechanism: Williams %R (typically 5-day lookback) oscillates 0 to -100; below -80 is oversold. Two-rule MR system: buy when %R is deeply oversold (e.g. crosses up through -80 from below, or simply %R < -80/-90), exit on price strength (%R moving back above an upper level such as -20, or a short-MA cross). Connors-style usage applies a longer-trend filter (trade longs above the 200-SMA). %R is essentially a fast stochastic %K, so this is the stochastic-fade family.
  - chop-fit: By construction it buys closes near the bottom of the recent range and sells the rebound to the range middle/top, so it is profitable precisely in range-bound/chop where %R extremes mark reversions rather than trend starts — and the cited backtest flags it fails in strong trends, confirming it is decorrelated from trend/momentum legs.
  - side-prediction (candidate): Returns-independent: in range/low-ADX regimes the unconditional reversion rate of %R from <-80 back above -50 within K bars should exceed that in high-ADX/trending regimes — a regime-conditional reversion signature measurable from the %R and price series alone (and the basis for predicting the strategy earns in chop, loses in trends). | independence=yes
  - claimed perf (UNVERIFIED): QuantifiedStrategies reports ~72% win rate on Nasdaq 100 (QQQ) with the market exposed only ~21% of the time; simple two-rule oversold-buy / exit-on-strength systems reported >70-80% win rate on S&P 500 and Nasdaq 100. Explicitly noted to work in range-bound markets and fail in strong trends.
  - source: QuantifiedStrategies.com, 'Williams Percent Range (Williams %R) Indicator — Backtest Strategy and Trading Rules' (and Substack mirror, updated 2026-03-01). Indicator originally by Larry Williams (1973). Exact entry/exit thresholds partly paywalled; lookback=5, oversold=-80 confirmed. <https://www.quantifiedstrategies.com/williams-r-trading-strategy/>

### opening-range fade / intraday reversal

- **SPY mid-sized opening-range mean reversion (Option Alpha)** — instr: SPX500/US500, NAS100 | d=2022-10-31
  - mechanism: Define the opening range as the move from the 9:30 open to 10:30 ET price. Bucket days by first-hour range size. Mid-sized moves (Groups 2-3) showed 67% and 62% probability of mean-reverting over the rest of the day (down moves close higher); small moves trend (85% of small up-moves close higher) and the very largest moves continue (76% of Group 4 days close below the 10:30 price). The fade trade is: on a MID-SIZED first-hour move, take the counter-direction position into the close.
  - chop-fit: It explicitly fades mid-sized opening displacements that fail to follow through, which is precisely the trend-deficit / range behavior the book lacks a leg for.
  - side-prediction (candidate): The mean-reversion edge should be strongest on average-volatility days and absent/inverted on the largest opening-range days (size-conditioned reversal), and the conditioning is checkable from open-to-10:30 range magnitude alone without the strategy P&L. | independence=yes
  - claimed perf (UNVERIFIED): Groups 2/3: 67% and 62% mean-reversion probability; small up-moves 85% close higher (+0.65% avg 10:30-close); Group 4: 76% close below 10:30 price. Sample Apr-Oct 2022, SPY.
  - source: Steve Henry & Kirk Du Plessis, 'Trading the Opening Range: Mean Reversion vs Trend Following,' Option Alpha, Oct 31 2022 (updated Apr 2026). <https://optionalpha.com/blog/opening-range-breakout>

### failed opening-breakout fade

- **Failed-ORB fade counter-strategy (re-entry into range)** — instr: SPX500/US500, NAS100, DJ30, XAUUSD | d=2026-04-01
  - mechanism: Price breaks the opening-range high (or low), fails, and re-enters the range. Instead of chasing the break, fade it: short when price falls back inside after a false break above (and the mirror for a false break below). Trapped breakout traders create the reversal pressure; positions are intraday-only. Reported as a ~52% win rate counter-strategy on SPY using the 15-minute opening range.
  - chop-fit: It only fires when breakouts FAIL, i.e. exactly on non-trend / range days when the book's breakout legs (DJ30/NAS) get chopped; it is structurally the inverse of the legs it would hedge.
  - side-prediction (candidate): Failed breakouts should cluster on low-volume / wrong-side-of-VWAP pokes (the cited 'low volume or wrong side of VWAP = trap' filter) and on mid-sized rather than large opening ranges — both observable from volume/VWAP and range magnitude, independent of the fade's own returns. | independence=no-reduces-to-pnl
  - claimed perf (UNVERIFIED): ~52% win rate on SPY for the failed-breakout reversal counter-strategy (15-min ORB); breakout-failure rates cited 40-80% depending on source.
  - source: HighStrike, 'Opening Range Breakout Strategy: Explained for Day Traders' and TradeAlgo ORB guide — failed-breakout fade rule, SPY ~52% WR (educational, undated). <https://highstrike.com/opening-range/>

### intraday short-horizon reversal (academic)

- **Intraday Residual Reversal (Brogaard, Han & Kim 2024)** — instr: SPX500/US500, NAS100 | d=2024-02-19
  - mechanism: Documents an intraday residual reversal in U.S. equities: half-hourly returns orthogonalized to common factors reverse over short intraday horizons (buy intraday losers / sell intraday winners on the residual). Stronger than raw short-term reversal; tied to overreaction to non-fundamental information and liquidity provision rather than continuation.
  - chop-fit: It is a contrarian/reversal mechanism that profits from transient overreaction within the day — the chop-paying side of the book; horizon is intraday, matching the operational layer.
  - side-prediction (candidate): The reversal should concentrate in the residual (factor-orthogonalized) component and in higher-overreaction / lower-liquidity conditions — checkable via factor decomposition and bid-ask/liquidity proxies, independent of the trading P&L. | independence=yes
  - claimed perf (UNVERIFIED): Paper reports residual reversal economically and statistically significant, exceeding standard short-term reversal; (cross-sectional single-stock evidence — not an index-level backtest).
  - source: Jonathan Brogaard, Jaehee Han, Hanjun Kim, 'Intraday Residual Reversal in the U.S. Stock Market,' SSRN Working Paper No. 4731947, posted Feb 19 2024. <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4731947>

### overnight/intraday return reversal (clientele-driven mean reversion)

- **Tug of War: Overnight vs Intraday Reversal (Lou-Polk-Skouras)** — instr: SPX500, NAS100, DJ30, MYM, MNQ | d=2014-08-01
  - mechanism: Strategy profits from 14 trading strategies are earned ENTIRELY in either the overnight or intraday window, with opposite signs across the two components; a 'tug of war' exists because institutions trade intraday (near the close) while individuals trade overnight (at the open). Past one-month INTRADAY returns negatively predict future intraday returns: sorting on past intraday returns yields ~2.19%/mo intraday excess return (t=6.72), i.e. an intraday reversal that reverses what built up overnight.
  - chop-fit: It is an explicit reversal/mean-reversion mechanism (intraday fades the overnight build-up) that is orthogonal to trend follow-through, so it should pay precisely when trend legs go flat in range/chop regimes.
  - side-prediction (candidate): Order-flow/clientele signature: small/retail trades cluster at the open while large/institutional trades cluster near the close; open order-imbalance is positive. This timing-of-volume composition is observable from intraday volume/trade-size data without using the strategy's own P&L. | independence=yes
  - claimed perf (UNVERIFIED): n/a
  - source: Lou, Polk, Skouras, 'A Tug of War: Overnight Versus Intraday Expected Returns', Journal of Financial Economics 134(1), 2019 (working-paper version circulated 2015, NBER APf15). <https://personal.lse.ac.uk/polk/research/TugOfWar.pdf>

### opening gap fade to prior RTH close

- **NQ Gap-Fill / Gap-Fade (tradingstats.net 2015-2025 study)** — instr: NAS100, MNQ | d=2026-02-01
  - mechanism: On the RTH open, fade the overnight gap: gap up -> sell, gap down -> buy, target = prior session RTH close (100% fill). Across 2,791 NQ days (Jan 2015-Dec 2025), 60.3% of gaps fill completely by the close. Fill probability is strongly conditioned on gap size (tiny <0.3xATR: 77.8% fill; large >1.2xATR: 8.2%) and open location (inside prior range: 70.4%; outside: ~44-47%). Best setup: tiny gap + first-15min confirmation toward fill = 93.1%.
  - chop-fit: A pure fade-to-prior-close mechanic that pays when overnight moves do not follow through into the RTH session — the follow-through-deficit/range condition the trend legs lose money in.
  - side-prediction (candidate): Fill probability should be monotonically decreasing in gap-size/ATR and higher when the open is inside the prior day's range — a returns-independent conditional-probability structure checkable directly from OHLC + ATR, with no P&L needed. | independence=yes
  - claimed perf (UNVERIFIED): n/a
  - source: tradingstats.net, 'Gap Fill Strategy: 2,791 Days of NQ Data (2015-2025)', published 2026-02-01. <https://tradingstats.net/gap-fill-strategy/>

### intraday-short / overnight-long session seasonality

- **Overnight-vs-Daytime Return Decomposition (Cooper-Cliff-Gulen 'Night and Day')** — instr: SPX500, DJ30, NAS100, MYM, MNQ | d=2008-09-26
  - mechanism: Decomposing returns into Night (16:00-09:30), AM, Mid-day, PM intervals over 1993-2006: overnight returns are strongly positive (S&P500 stocks 0.028%-0.048%/interval) while daytime returns are ~0 and sometimes negative (-0.028% to 0.002%). Holds for individual stocks, equity indexes AND index futures. The tradeable side is buy-at-close / sell-at-open (long overnight) and/or short the flat-to-negative daytime leg.
  - chop-fit: Documents that the daytime (RTH) session carries ~zero net trend; a daytime fade/MR leg therefore is not penalized by trend drift and is structurally decorrelated from the overnight-trend legs.
  - side-prediction (candidate): The effect should partition cleanly into a positive overnight and a flat/negative intraday component across days-of-week, days-of-month and months — a calendar-invariant decomposition checkable from open/close vs prior-close series alone, independent of any trading P&L. | independence=yes
  - claimed perf (UNVERIFIED): n/a
  - source: Cooper, Cliff, Gulen, 'Return Differences between Trading and Non-Trading Hours: Like Night and Day', SSRN abstract 1004081, posted 2008-09-26. <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1004081>

### large-gap fade conditioned on overnight move size + weekday

- **Fade the Large Overnight Gap in SPY/QQQ (SharePlanner study)** — instr: SPX500, NAS100, MYM, MNQ | d=2025-04-26
  - mechanism: On sessions opening with a >=1% overnight gap (~15-20% of days): gap-ups drift mildly negative open-to-close (SPY ~ -0.2%, QQQ ~ -0.5% avg), gap-downs partially recover (SPY ~ +0.21% open-to-close). ~50% of 1%+ gaps fill intraday (1-1.99%: ~45%; 2%+: 30-33%). Monday gap-ups have higher fade/fill propensity (~61%, 'sell the rip'); Monday gap-downs keep declining (~ -0.20% extra).
  - chop-fit: An explicit fade of over-extended overnight moves that pays when the gap does not continue — i.e., when overnight momentum fails to follow through intraday, the chop condition.
  - side-prediction (candidate): A weekday-conditional asymmetry: Monday gap-ups fill/fade more often than other weekdays while Monday gap-downs underperform — a day-of-week structure in fill rates testable from calendar-tagged OHLC, independent of strategy returns. | independence=yes
  - claimed perf (UNVERIFIED): n/a
  - source: SharePlanner, 'Fading the Gap: How Large Overnight Moves in SPY and QQQ Play Out During the Trading Day', published 2025-04-26. <https://www.shareplanner.com/blog/strategies-for-trading/fading-the-gap-how-large-overnight-moves-in-spy-and-qqq-play-out-during-the-trading-day.html>

### regime-conditioned overnight-session anomaly

- **Sentiment-Filtered Overnight Hold (Quantpedia, SPY)** — instr: SPX500, MYM | d=2021-04-19
  - mechanism: Hold SPY overnight (close-to-open) only when sentiment/regime filters are favorable: SPY > 20-day MA, VIX < 20-day MA, and a news-based Brain Market Sentiment > 20-day MA. An equal-weight combination of the three signals optimizes the overnight-anomaly capture (analysis window Jan 2018-Jan 2021).
  - chop-fit: Captures the overnight (non-trend) return component while RTH-trend legs are dormant; a session-timed leg decorrelated from intraday trend, with regime gating to survive chop-driven volatility spikes.
  - side-prediction (candidate): Conditioning observables (VIX vs its 20d MA, news-sentiment index level) are exogenous regime variables; the claim that overnight outperformance concentrates in low-VIX / positive-sentiment states is checkable from VIX and sentiment series without the strategy's P&L. | independence=yes
  - claimed perf (UNVERIFIED): n/a
  - source: Quantpedia, 'Market Sentiment and an Overnight Anomaly', published 2021-04-19 (builds on Cooper-Cliff-Gulen 2008 and Branch-Ma). <https://quantpedia.com/market-sentiment-and-an-overnight-anomaly/>

### volatility-contraction range / mean-reversion hold

- **NR7 narrow-range time-exit reversion (Oxford Capital Strategies build)** — instr: DJ30, NAS100, SPX500, USOIL, MGC, MYM, MNQ | d=2016
  - mechanism: Identify an NR7 day (today's range is the narrowest of the last 7 days = volatility contraction). Oxford's build enters via an opening-range-breakout stretch the next day, but the PRIMARY exit is a TIME exit at the close of the Nth day (N swept 1-40), plus an opposite-stretch exit and a 6x20-ATR stop. Tested on 42 US futures (commodities, currencies, rates, equity indexes) over 1980-2016 in MATLAB. Without costs it is profitable across the parameter range; with $50 round-turn cost it is rated 'C' and 'not currently tradeable without additional rules'.
  - chop-fit: It is anchored on a volatility-contraction filter (NR7) and exits on a fixed time horizon rather than riding a trend, so it harvests the post-squeeze range/normalization that pays precisely when compression does NOT resolve into a sustained directional move.
  - side-prediction (candidate): Returns-independent observable: NR7 days should be measurably followed by a rise in realized range/ATR on the subsequent 1-3 days (volatility expansion after contraction) regardless of direction; this volatility-expansion signature is checkable on bar data without running the strategy P&L. | independence=yes
  - claimed perf (UNVERIFIED): Profitable across N=1-40 without costs; with $50/round-turn cost downgraded to 'C / not tradeable without extra rules'. No clean CAGR/DD published per-instrument.
  - source: Oxford Capital Strategies, 'NR7 Pattern | Trading Strategy (Setup & Exit)', published March 2016. Tested 42 US futures markets incl. equity indexes, 1980-2016. <https://oxfordstrat.com/trading-strategies/nr7/>

### close-location range fade / 1-day mean reversion

- **Internal Bar Strength (IBS) one-day mean reversion** — instr: SPX500, NAS100, DJ30 | d=2014
  - mechanism: IBS = (Close - Low) / (High - Low), bounded [0,1], measuring where the close sits inside the day's range. Long when IBS is low (e.g. < 0.2, oversold within the bar's own range); exit/short when IBS is high (> 0.8). Documented to work strongly on equity-index ETFs (SPY, QQQ) over ~2000-2020. Cesar Alvarez's bucket study on S&P 500 names shows win rate declining monotonically from ~71% (low IBS) to ~57% (high IBS) and ~58% higher average P&L for the IBS<10 bucket.
  - chop-fit: IBS fades the close's position within the bar's own range on a 1-day horizon, so it earns its return from intraday/overnight reversion rather than follow-through, paying in range/chop where closes near the extremes snap back.
  - side-prediction (candidate): Returns-independent observable (verified in source): the next-day mean return / win rate sorts MONOTONICALLY by IBS bucket (low-IBS days followed by higher positive next-day returns than high-IBS days). This bucket-monotonicity is a conditional-distribution signature checkable on OHLC data without simulating the strategy's equity curve. | independence=yes
  - claimed perf (UNVERIFIED): QQQ ~14.5%/yr in ETF tests (2000-2020); Alvarez S&P-names study ~+58% avg P&L for IBS<10 bucket, win rate 71%->57% low->high IBS.
  - source: Cesar Alvarez, 'Internal Bar Strength for Mean Reversion', Alvarez Quant Trading, 2022-02-16. Corroborated by A. Soffronow Pagonidis, 'The IBS Effect: Mean Reversion in Equity ETFs' (NAAIM, ~2014) and Pandey & Joshi, 'Using Internal Bar Strength as a Key Indicator for Trading Country ETFs', arXiv:2306.12434 (2023-06-14). <https://alvarezquanttrading.com/blog/internal-bar-strength-for-mean-reversion/>

### oscillator-reversal mean reversion (dip-buy in trend filter)

- **Connors RSI(2) short-term mean reversion** — instr: SPX500, NAS100, DJ30 | d=2008
  - mechanism: Trend filter: price above 200-day SMA. Entry: 2-period RSI drops below 5 (some variants <10 or cumulative-RSI), buy at close. Exit: RSI(2) rises above 65 (or above the 5-day SMA), sell at close. Symmetric short version below the 200-SMA with RSI(2) > 95. Published by Larry Connors in 'Short Term Trading Strategies That Work' (2008) and earlier 'Street Smarts' (1996). Documented equity win rate >75% historically, with explicit acknowledgement that the vanilla edge has decayed since 2008 publication.
  - chop-fit: It buys 2-3-day oversold extremes for a fast reversion to the mean, profiting when selloffs fail to follow through (chop/whipsaw) rather than when trends extend.
  - side-prediction (candidate): Returns-independent observable: days with RSI(2)<5 should exhibit elevated short-horizon return-reversal (negative serial correlation at the 1-3 day lag) in the conditioned subsample; this autocorrelation-sign signature is measurable on price series alone, separate from the strategy's tradeable P&L. | independence=yes
  - claimed perf (UNVERIFIED): Historical equity win rate >75%; explicitly noted to have lost most of its vanilla edge since the 2008 publication (decay disclosed).
  - source: Larry Connors & Cesar Alvarez, 'Short Term Trading Strategies That Work' (TradingMarkets, 2008); earlier RSI(2)/narrow-range work in Connors & Raschke, 'Street Smarts' (1996). Replication: QuantifiedStrategies, 'RSI 2 Strategy: Complete Guide'. <https://www.quantifiedstrategies.com/rsi-2-strategy/>

### volatility-squeeze (range-during-compression) - documented failure of naive entry

- **Bollinger-in-Keltner squeeze, traded as a NEGATIVE/calibration result** — instr: SPX500, NAS100, DJ30, EURUSD | d=2021-12-27
  - mechanism: Squeeze = Bollinger Bands contract entirely inside the Keltner Channels (low-volatility compression; price ranges during this window). Huault's Superalgos quantitative study takes naive squeeze-triggered entries: 55 trades, 55% hit ratio, but TOTAL LOSS of initial capital without stop/target money management; adding Supertrend + SL/TP was required to make it viable. Published Medium, Dec 2021, with KNIME analysis + Superalgos backtest.
  - chop-fit: Directly about the squeeze/range-during-compression window the focus targets; its value is showing that the range exists but a naive fade/entry inside it loses without explicit reversion targets and stops.
  - side-prediction (candidate): Returns-independent observable: BB-inside-KC squeeze periods should show statistically lower realized range / ADX than non-squeeze periods by construction, and an elevated probability of a subsequent volatility expansion; both are directly measurable on bar data, no P&L needed. | independence=yes
  - claimed perf (UNVERIFIED): 55 trades, 55% hit ratio, total loss of capital under naive entry; only viable after adding Supertrend filter + SL/TP (negative result disclosed).
  - source: Thomas Huault, 'A Quantitative Study of the Bollinger Bands Squeeze Strategy', Superalgos (Medium), December 2021. <https://medium.com/superalgos/a-quantitative-study-of-the-bollinger-bands-squeeze-strategy-9f47143f33fb>

### oscillator-reversal mean-reversion (overbought/oversold fade)

- **Connors RSI(2) mean-reversion (index/ETF oscillator fade)** — instr: SPX500/US500, NAS100, DJ30 | d=2008
  - mechanism: On a daily bar with price above the 200-day SMA, buy when the 2-period RSI drops below 10 (better below 5); exit when price closes above the 5-day SMA. Symmetric short side below the 200-SMA: short when RSI(2) > 90 (better >95), cover below 5-day SMA. Connors does not advocate hard stops in the original rules.
  - chop-fit: It explicitly buys oversold dips and sells overbought spikes expecting reversion to a short SMA, so it earns exactly when price oscillates without follow-through — the chop regime where trend legs go flat.
  - side-prediction (candidate): Returns-independent implication: conditional next-day mean of the index is predictable from today's RSI(2) bucket (very-low RSI(2) days should show positive average forward 1-3 day returns, very-high RSI(2) days negative) — checkable on price series alone without trading the system. | independence=yes
  - claimed perf (UNVERIFIED): n/a
  - source: StockCharts ChartSchool, 'RSI(2)'; rules originate with Larry Connors, 'Short Term Trading Strategies That Work' (Connors & Alvarez, 2008) and earlier 'Street Smarts' (Connors & Raschke, 1996). <https://chartschool.stockcharts.com/table-of-contents/trading-strategies-and-models/trading-strategies/rsi-2>

### intrabar-position oscillator mean-reversion (range-close fade)

- **IBS effect (Internal Bar Strength daily mean-reversion)** — instr: SPX500/US500, NAS100, DJ30 | d=2013
  - mechanism: IBS = (Close - Low) / (High - Low) on a daily bar (0 = close at low, 1 = close at high). Buy index/ETF when IBS < 0.2 (closed in bottom of day's range), expecting a higher next-day close; avoid/short when IBS > 0.8. Author reports avg next-day return ~+0.35% after IBS<0.2 vs ~-0.13% after IBS>0.8; adding the IBS filter raised total return ~10pp while cutting time-in-market ~45%.
  - chop-fit: A close at the bottom of the range (panic/overshoot) systematically reverts up next day — it harvests intraday-overreaction corrections, which cluster in non-trending/choppy tape exactly when momentum legs stall.
  - side-prediction (candidate): Returns-independent: the conditional mean of next-day close-to-close return as a monotone decreasing function of today's IBS bucket is a property of the price series itself; computable on OHLC without trading the rule. Also predicts low-IBS days cluster after high-range/high-volume sessions (checkable on volume/range data). | independence=yes
  - claimed perf (UNVERIFIED): n/a
  - source: Alexander Soffronow Pagonidis, 'The IBS Effect: Mean Reversion in Equity ETFs', NAAIM-hosted paper (c. 2013-2014). Independently reproduced by Jonathan Kinlay (2019) and in arXiv:2306.12434 for country ETFs. <https://www.naaim.org/wp-content/uploads/2014/04/00V_Alexander_Pagonidis_The-IBS-Effect-Mean-Reversion-in-Equity-ETFs-1.pdf>

### channel/extreme fade mean-reversion

- **Donchian channel FADE (sell upper / buy lower channel in range)** — instr: EURUSD, USDCAD, XAUUSD, USOIL | d=undatable
  - mechanism: Compute the N-period Donchian channel (highest-high / lowest-low). Counter to the classic breakout use, the fade variant buys when price reaches/pierces the LOWER band and sells when it reaches/pierces the UPPER band, targeting the channel midline (or opposite band), used only in range-bound (non-trending) conditions and confirmed with a momentum/volume filter.
  - chop-fit: By construction it sells the top and buys the bottom of a horizontal range and exits at the midline, so every completed oscillation between support/resistance is a winning trade — precisely the chop payoff the book lacks.
  - side-prediction (candidate): none-apparent (the educational source offers no returns-independent observable; any side prediction — e.g. that band-touch reversals cluster when realized vol / ADX is low — would have to be hypothesized and tested, not taken from the source). | independence=none-apparent
  - claimed perf (UNVERIFIED): n/a
  - source: TrendSpider Learning Center, 'Donchian Channel Trading Strategies: Breakouts, Reversals & Setup'. Indicator originates with Richard Donchian (mid-20th-century futures trend trader); the fade/reversal use is the documented range-bound variant. <https://trendspider.com/learning-center/donchian-channel-trading-strategies/>

### volatility-band fade mean-reversion

- **Bollinger Band %b lower-band buy (volatility-band fade to mean)** — instr: SPX500/US500, NAS100, EURUSD | d=2001
  - mechanism: 20-period Bollinger Bands; the fade variant buys when price/%b tags the LOWER band (e.g. close below the lower band at 1.5-2.0 SD) in a non-trending market and exits back at the middle band (20-SMA). One cited backtest of a lower-band-at-1.5SD S&P 500 buy produced 561 trades, avg +0.52% per trade, ~8.8% CAGR with capital invested ~25% of the time; ~60% win rate, ~1:1 R. Bollinger himself stresses band touches are NOT automatic signals and require regime filtering.
  - chop-fit: Buying 1.5-2SD below the 20-bar mean and exiting at the mean monetizes reversion within a range; it earns when price overshoots and snaps back rather than trends, complementing trend legs that need follow-through.
  - side-prediction (candidate): Returns-independent: the strategy implies forward returns are conditionally higher when %b is below 0 (price below lower band) than when above 1 — a property of the price/vol series testable without P&L. Also predicts band-touch reversals concentrate when band-width (realized vol) is contracting, checkable on the vol series. | independence=yes
  - claimed perf (UNVERIFIED): n/a
  - source: Rational Growth, 'Bollinger Bands on S&P 500: Why Mean Reversion Fails' (documents failure of generic variants); positive lower-band-buy variant figures from QuantifiedStrategies '12 Bollinger Bands Trading Strategies'. Indicator: John Bollinger, 'Bollinger on Bollinger Bands' (2001). <https://rational-growth.com/bollinger-band-mean-reversion-sp500/>

### gap-fade / overnight-to-intraday reversal mean-reversion

- **Gap fade (open-gap reversion to prior close, index)** — instr: SPX500/US500, NAS100, DJ30 | d=undatable
  - mechanism: On a moderate overnight gap, fade it: buy at the open when the index gaps DOWN within a bounded range (e.g. SPY opens between -0.15% and -0.6%), sell/short a bounded gap UP; target the prior close / intraday fill. The -0.6% cap is because larger down-gaps show much weaker mean reversion. Cited as ~60-70% win probability with roughly symmetric P&L and little optimization.
  - chop-fit: It buys panic down-gaps and sells euphoric up-gaps expecting reversion to prior close — it monetizes overnight overreactions that revert intraday, a non-trend payoff that fires in unsettled/range tape.
  - side-prediction (candidate): Returns-independent: the rule predicts the conditional intraday (open-to-close) return is negatively related to the overnight gap within the bounded band — i.e. an overnight/intraday return autocorrelation sign, measurable from OHLC alone (the CO-OC reversal signature) without trading the system. | independence=yes
  - claimed perf (UNVERIFIED): n/a
  - source: SharePlanner, 'Fading the Gap: How SPY and QQQ Overnight Moves Play Out During the Trading Day'; rule-specific gap-band example (-0.15% to -0.6% long) per QuantifiedStrategies gap-trading writeups. Mechanism corroborated by overnight-to-intraday (CO-OC) reversal literature. <https://www.shareplanner.com/blog/strategies-for-trading/fading-the-gap-how-large-overnight-moves-in-spy-and-qqq-play-out-during-the-trading-day.html>

### carry / term-structure / roll-yield

- **Commodity term-structure (roll-yield) carry: long backwardation / short contango** — instr: USOIL, XAUUSD, MGC | d=2010-04-22
  - mechanism: Cross-sectional commodity strategy: each month rank a futures universe by roll-return (term-structure slope), go long the top ~20% (most backwardated, positive roll yield) and short the bottom ~20% (most contangoed, negative roll yield), equal-weighted, hold one month. Captured roll yield is independent of spot direction.
  - chop-fit: Roll yield is harvested from curve shape (backwardation vs contango) rather than spot follow-through, so it can pay during flat/range regimes where directional trend legs go to zero.
  - side-prediction (candidate): Inventory / theory-of-storage signature: backwardation (positive roll, the long signal) should coincide with low/falling reportable inventories and high convenience yield; this inventory-slope link is checkable from EIA stocks data independent of the strategy's own P&L. | independence=yes
  - claimed perf (UNVERIFIED): Quantpedia/Fuertes-Miffre-Rallis: ~11.73% annualized, vol 23.84%, Sharpe 0.49, max DD -78.06% (1979-2004, full multi-commodity long-short).
  - source: Quantpedia, 'Term Structure Effect in Commodities'; primary academic ref: Fuertes, Miffre & Rallis (2010), 'Tactical Allocation in Commodity Futures Markets: Combining Momentum and Term Structure Signals', Journal of Banking & Finance / SSRN. Quantpedia-reported backtest 1979-2004: ~11.73% p.a., vol 23.84%, Sharpe 0.49, max DD -78%. <https://quantpedia.com/strategies/term-structure-effect-in-commodities>
- **Theory-of-storage inventory-conditioned commodity roll carry (Gorton-Hayashi-Rouwenhorst)** — instr: USOIL, XAUUSD | d=2007-07
  - mechanism: Futures basis (term-structure slope) and the level of inventories jointly predict the cross-section of commodity futures risk premia. Low inventories => high convenience yield => backwardation => high subsequent futures returns; the paper shows the futures basis is a sufficient statistic largely subsuming raw inventory, supporting a basis/roll-sorted carry portfolio.
  - chop-fit: Returns are driven by the inventory/scarcity state (convenience yield) rather than spot trending, providing a premium that persists through non-trending, range-bound commodity regimes.
  - side-prediction (candidate): Directly returns-independent: the sign of the front-to-next-month basis should track reportable inventory levels (EIA crude stocks for WTI) — backwardation when inventories are below normal, contango when above. Verifiable from inventory + curve data alone. | independence=yes
  - claimed perf (UNVERIFIED): Reports significant predictive power of the futures basis and inventory for the cross-section of commodity returns; no single packaged Sharpe headline (factor-regression paper) — claimed performance not stated as a turnkey strategy.
  - source: Gorton, Hayashi & Rouwenhorst, 'The Fundamentals of Commodity Futures Returns', NBER Working Paper No. 13249 (2007); later Review of Finance (2013). Establishes inventory-basis-roll predictability for a broad commodity panel. <https://www.nber.org/system/files/working_papers/w13249/w13249.pdf>
- **FX carry trade (high-rate long / low-rate short; forward-premium harvest)** — instr: USDJPY, USDCAD, EURUSD, GBPUSD | d=1984
  - mechanism: Go long the basket of currencies with the highest short-term (central-bank/money-market) rates and short the basket with the lowest, monthly rebalanced; the position earns the interest-rate differential (the FX analogue of carry/roll) as long as spot does not move adversely by more than the differential.
  - chop-fit: Carry accrues continuously from rate differentials regardless of FX trend; in quiet, range-bound FX (low realized vol) it is precisely when carry is harvested cleanly, decorrelated from index/gold trend legs.
  - side-prediction (candidate): Negative-skew / crash signature: carry-basket returns should show conditional left-tail risk that loads on global risk aversion (VIX/funding spreads) and on FX order-flow forward bias — observable from option-implied skew and positioning, independent of the strategy P&L. | independence=yes
  - claimed perf (UNVERIFIED): Deutsche Bank Currency Carry USD Index (via Quantpedia): ~7.27% annualized, vol 9.6%, Sharpe 0.29, max DD -32.05%; academic long-short HML-FX Sharpe ~0.5-0.7 post-Bretton Woods.
  - source: Quantpedia, 'FX Carry Trade'; academic refs Lustig, Roussanov & Verdelhan (2011) 'Common Risk Factors in Currency Markets' (Review of Financial Studies); Brunnermeier, Nagel & Pedersen 'Carry Trades and Currency Crashes' (NBER Macro Annual 2008). Quantpedia cites DB Currency Carry USD Index ~7.27% p.a., vol 9.6%, Sharpe 0.29, max DD -32%. <https://quantpedia.com/strategies/fx-carry-trade>
- **Global cross-asset 'Carry' factor (Koijen-Moskowitz-Pedersen-Vrugt) — rates/bond carry sleeve** — instr: micro-rates, USDJPY, USOIL | d=2013-08
  - mechanism: Define carry model-free as the return to a security if prices stay unchanged (futures-spot or yield-roll). Within each asset class go long high-carry, short low-carry instruments. For fixed income/rates this is the yield-curve slope + roll-down (long steep-curve/high-roll bond futures, short flat-curve ones).
  - chop-fit: Rates/bond carry is earned from curve slope and roll-down, not from yields trending; in non-trending macro chop the slope persists and the carry continues to accrue, decorrelated from gold/index trend.
  - side-prediction (candidate): Carry's own term-structure signature: high-carry assets should have steeper own futures/forward curves; in bonds the predicted return maps to the published yield-curve slope (e.g. 10y-3m) and roll-down, both observable from rate data independent of realized strategy returns. | independence=yes
  - claimed perf (UNVERIFIED): Diversified global carry factor reports high risk-adjusted returns (paper-reported Sharpe well above 1 for the diversified-across-asset-classes carry portfolio); per-asset-class sleeves lower. Exact headline Sharpe in paper tables, not restated here to avoid misquote.
  - source: Koijen, Moskowitz, Pedersen & Vrugt, 'Carry', Journal of Financial Economics 127(2) (2018), pp. 197-225; NBER WP 19325 (2013). DOI 10.1016/j.jfineco.2017.11.002. <https://www.nber.org/system/files/working_papers/w19325/w19325.pdf>

### intraday/overnight short-term reversal (mean-reversion)

- **Overnight-Intraday Reversal (multi-asset, index/commodity/FX futures)** — instr: SPX500/US500, NAS100, DJ30, USOIL, XAUUSD, EURUSD, USDJPY, MNQ, MYM, MGC | d=2016-12-31
  - mechanism: Decompose close-to-close into overnight (close->open) and intraday (open->close). Assets/sessions with high past overnight returns tend to reverse during the next intraday session and vice versa; trade the open->close leg against the prior overnight move. Driven by asset-class-specific liquidity provision; cross-sectional return dispersion positively predicts the strategy's return and conditional Sharpe.
  - chop-fit: It is an explicit mean-reversion of the overnight gap harvested intraday, so it pays when moves fail to follow through (chop/range) and is structurally orthogonal to the book's trend/breakout legs.
  - side-prediction (candidate): Strategy expected return and conditional Sharpe should rise with cross-sectional return dispersion and with realized volatility (liquidity-provision premium widens in stress), both observable from price data without the strategy's own P&L; effect should also strengthen in high-VIX regimes per the related Della Corte-Kosowski result. | independence=yes
  - claimed perf (UNVERIFIED): Avg excess return and Sharpe ~2-5x a conventional short-term reversal strategy; robust across asset classes and OOS (no single headline CAGR given for the futures basket).
  - source: Liu, Liu, Wang, Zhou & Zhu, 'Overnight-Intraday Reversal Everywhere', SSRN 2730304 <https://papers.ssrn.com/sol3/Delivery.cfm/2730304.pdf?abstractid=2730304>

### short-term reversal (mean-reversion), volatility-conditioned

- **Market Closure and Short-Term Reversal (overnight-conditioned intraday reversal, VIX-amplified)** — instr: SPX500/US500, NAS100, DJ30, USOIL, XAUUSD, EURUSD, GBPUSD, USDJPY | d=2015-12
  - mechanism: Building on Hong's periodic-market-closure model: overnight (closure) returns are followed by intraday reversal. A reversal strategy formed on the close-to-open move and held over the subsequent open-to-close session earns a liquidity premium; predictability is strongest when VIX/uncertainty is high.
  - chop-fit: Reversal amplitude rises with VIX/uncertainty, so it monetizes exactly the high-volatility non-follow-through tape where the trend/breakout legs stall.
  - side-prediction (candidate): Conditional reversal magnitude should increase monotonically with VIX / realized volatility and with overnight-gap size: a returns-independent, directly testable volatility/order-flow signature. | independence=yes
  - claimed perf (UNVERIFIED): Reported intraday reversal Sharpe materially above conventional daily reversal; exact figure not legibly extractable from the conference PDF (corroborated qualitatively by the companion 'Everywhere' paper).
  - source: Della Corte & Kosowski, 'Market Closure and Short-Term Reversal', CICF conference paper (paper_357), ~2015 <https://www.cicfconf.org/sites/default/files/paper_357.pdf>

### calendar / turn-of-month seasonality

- **Turn-of-the-Month effect in equity indexes** — instr: SPX500/US500, DJ30, NAS100, MYM, MNQ | d=1988
  - mechanism: Buy the index ~1 (some variants ~4) trading day before month-end and exit at the close of the 3rd trading day of the new month. Lakonishok & Smidt (1988) and McConnell & Xu (2006/2008) show essentially all of the index's positive return historically accrues in this ~4-day window; effect present in 31 of 35 countries and not driven by quarter/year-ends.
  - chop-fit: It is a calendar-window flow effect with no dependence on a prevailing trend, so it can deliver return in flat/choppy months when the trend legs are idle; decorrelation via timing rather than via a reversal mechanism per se.
  - side-prediction (candidate): Independent observable: a concentration of net institutional inflows / above-average volume in the ~4-day turn-of-month window (flow and volume data, not the strategy's P&L); effect should be stronger in months following payday/settlement cycles. | independence=yes
  - claimed perf (UNVERIFIED): Quantpedia SPY implementation: ~7.2% p.a., Sharpe ~1.04, vol ~6.9%, max DD -20.79%.
  - source: McConnell & Xu, 'Equity Returns at the Turn of the Month', SSRN 917884 (orig. Lakonishok & Smidt 1988) <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=917884>

### calendar / monetary-policy-cycle seasonality

- **FOMC-cycle even-week equity premium** — instr: SPX500/US500, DJ30, NAS100, MYM, MNQ | d=2014-04-23
  - mechanism: Since 1994 the entire equity premium has accrued in even weeks (0,2,4,6) of the FOMC cycle measured from the last FOMC meeting; odd weeks earn ~zero/negative. A long-only strategy holding only in even weeks beat buy-and-hold (11.8% vs 8.3% excess, 1994-2015). Authors tie it to systematic informal Fed communication / monetary-policy news flow.
  - chop-fit: Return is harvested on a fixed monetary-policy calendar regardless of trend state, so it can be positive in choppy stretches; decorrelation from the trend legs comes from the calendar gating rather than from a directional edge.
  - side-prediction (candidate): Independent observable: the even/odd-week return asymmetry should co-move with the FOMC-meeting calendar and with measurable Fed-communication intensity (Fed funds futures moves, inter-meeting target changes, Board-of-Governors meeting dates), all checkable without the strategy's P&L. | independence=yes
  - claimed perf (UNVERIFIED): Even-week long-only ~11.8% vs 8.3% buy-and-hold excess return, 1994-2015; even/odd difference statistically significant.
  - source: Cieslak, Morse & Vissing-Jorgensen, 'Stock Returns over the FOMC Cycle', SSRN 2687614 / J. Finance 2019 <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2687614>

### calendar / scheduled-announcement drift

- **Pre-FOMC Announcement Drift** — instr: SPX500/US500, DJ30, NAS100, MYM, MNQ | d=2011-09
  - mechanism: Since 1994, US equities earn large excess returns in the ~24 hours before scheduled FOMC announcements: ~49 bps on average over Sep1994-Mar2011, ~80% of annual realized equity returns. No analogous effect in Treasuries or money-market futures; other macro announcements show no pre-drift. Returns higher when the yield curve is flat and implied vol is high.
  - chop-fit: Effect is larger when implied volatility is high (uncertain, non-trending tape), so the calendar-gated long captures premium precisely in regimes where the book's trend legs struggle; some recent work reports the drift has weakened post-2011.
  - side-prediction (candidate): Independent observables: the pre-FOMC return should be increasing in implied equity volatility (VIX) and decreasing in the slope of the Treasury yield curve, both measurable ex-ante from market data, not from the strategy's own returns. | independence=yes
  - claimed perf (UNVERIFIED): ~49 bps average over the 24h pre-FOMC window, Sep1994-Mar2011 (~80% of annual equity return); JF 2015, vol-conditional.
  - source: Lucca & Moench, 'The Pre-FOMC Announcement Drift', NY Fed Staff Report 512 (2011) / J. Finance 2015 <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1923197>

### calendar / monthly commodity seasonality

- **Gold monthly seasonality (September & November / winter effect)** — instr: XAUUSD, MGC | d=2013
  - mechanism: Hold gold in September and November (and broadly the turn-of-year 'winter' window), cash otherwise. Baur (2013) documents positive, statistically significant gold returns concentrated in Sep and Nov, attributed to seasonal physical/jewelry demand (e.g., Indian wedding season). Corroborated by Qi & Wang (2013) and Naylor, Wongchoti & Ith (2015).
  - chop-fit: A calendar-gated seasonal long can add return in flat/choppy gold months when Guardian's trend leg is idle; weak thesis fit because the source (Bartsch, Baur, Dichtl, Drobetz 2018) finds the pure seasonal effect does NOT survive Hansen SPA data-snooping controls, so include only as a low-confidence calendar overlay.
  - side-prediction (candidate): Independent observable: a seasonal rise in physical gold demand / import volumes (e.g., Indian jewelry-import and wedding-season data) concentrated in the Sep-Nov window, a demand signature checkable without the strategy's P&L. | independence=yes
  - claimed perf (UNVERIFIED): Sep/Nov returns positive and statistically significant in-sample (Baur 2013); but seasonal strategies fail SPA data-snooping test in Bartsch et al. (2018), so no robust net-of-snooping outperformance claimed.
  - source: Baur (2013) 'The Autumn Effect of Gold'; Bartsch, Baur, Dichtl & Drobetz (2018) market-timing test (via Quantpedia) <https://quantpedia.com/an-extensive-test-of-market-timing-strategies-in-the-gold-market/>

### stat-arb pairs / distance-method mean-reversion

- **GGR distance-method pairs trading (foundational relative-value arbitrage rule)** — instr: SPX500, DJ30, NAS100 | d=1999-03
  - mechanism: Gatev-Goetzmann-Rouwenhorst (2006): form pairs by minimum sum-of-squared-deviations between normalized price series over a 12-month formation window; trade in the next 6-month period by opening the spread (long the relative loser, short the relative winner) when normalized prices diverge by >2 historical standard deviations, closing when they re-converge (cross). Reported ~11% annualized excess return on US equities 1962-2002, profits exceeding conservative cost estimates.
  - chop-fit: Convergence-of-divergence pays precisely when prices oscillate around a relationship rather than trend — i.e. when trend legs go flat and follow-through fails, the spread mean-reverts and the leg earns.
  - side-prediction (candidate): Returns-independent: the paper attributes profits to a common factor in pair returns; an independent check is that selected pairs exhibit statistically significant cointegration / low spread half-life over the formation window measured on prices alone (no P&L), and pair profitability should rise in higher cross-sectional-volatility / bear regimes (Fil 2020 corroboration) — both observable without the strategy's own returns. | independence=yes
  - claimed perf (UNVERIFIED): n/a
  - source: Gatev, E., Goetzmann, W.N., Rouwenhorst, K.G. (2006). 'Pairs Trading: Performance of a Relative-Value Arbitrage Rule.' The Review of Financial Studies 19(3): 797-827. (NBER w7032, 1998; SSRN 141615.) <https://academic.oup.com/rfs/article-abstract/19/3/797/1646694>

### stat-arb pairs / distance + cointegration mean-reversion

- **Gold Standard Pairs Trading Rules validity re-test (Fil 2020)** — instr: SPX500, DJ30, NAS100 | d=2020-10-02
  - mechanism: Fil (2020) re-runs the canonical distance method and cointegration method on US equities 1990-2020 (incl. COVID), with hyperparameter tuning of the z-score entry threshold. Finds the classic rule overall fails to beat the market benchmark in recent samples but is substantially stronger in bear markets / high-volatility regimes; optimal parameters are regime-dependent.
  - chop-fit: Explicitly documents that pairs-trading profitability is concentrated in bear/high-volatility regimes and weak in trending markets — a direct empirical match to 'pays when trends fail to follow through.'
  - side-prediction (candidate): Returns-independent: the conditional-edge claim implies a measurable correlation between realized pair-spread dispersion (cross-sectional return dispersion of constituents) and a bear/high-vol regime flag (e.g. VIX level, drawdown state) — checkable on price/vol data without running the strategy P&L. | independence=yes
  - claimed perf (UNVERIFIED): n/a
  - source: Fil, M. (2020). 'Gold Standard Pairs Trading Rules: Are They Valid?' arXiv:2010.01157. <https://arxiv.org/abs/2010.01157>

### cointegration spread reversion (two-leg commodity spread)

- **WTI/Brent crude spread mean-reversion (SMA fair-value reversion)** — instr: USOIL | d=2009
  - mechanism: Trade the WTI-minus-Brent spread against a 20-day SMA fair value: short the spread when it is above the SMA20, long when below; exit when the spread crosses back through fair value; daily rebalance. (Quantpedia codification of Evans, Dunis, Laws.) Quantpedia-reported Sharpe ~0.88, ~9.92% annualized, but large drawdown and OOS decay; an ARMA variant did better in-sample.
  - chop-fit: A stationary spread mean-reverts continuously regardless of whether outright oil trends; it earns from range-bound spread oscillation, decorrelated from outright trend direction.
  - side-prediction (candidate): Returns-independent: spread reversion is driven by the physical WTI-Brent quality/logistics differential — an observable term-structure/inventory signature (e.g. Cushing inventory builds widen the spread) predicts spread direction without the strategy's own P&L. Note Quantpedia's own OOS-decay caveat flags data-mining risk. | independence=yes
  - claimed perf (UNVERIFIED): n/a
  - source: Evans, Dunis, Laws, 'Trading Futures Spread Portfolios: An Application of Correlation...' Journal of Derivatives & Hedge Funds 15(4); backtest 1995-2004. Codified at Quantpedia 'Trading WTI/Brent Spread.' <https://quantpedia.com/strategies/trading-wti-brent-spread>

### cointegration spread reversion with regime-switching MR

- **Hidden-Markov regime-switching crude oil stat-arb (Brent/WTI/Shanghai)** — instr: USOIL | d=2023-09-02
  - mechanism: Fanelli, Fontana, Rotondi (2023): cointegrate international crude benchmarks (Brent, WTI, Dubai, Shanghai INE), model the cointegration residual as a mean-reverting Ornstein-Uhlenbeck process whose parameters are modulated by a hidden Markov chain (online filter estimation); take spread positions when the residual deviates from its regime-conditional equilibrium. Shanghai-inclusive spreads profitable after conservative costs; Brent/WTI/Dubai-only spreads not consistently profitable.
  - chop-fit: Earns from OU reversion of a stationary cointegration residual; the regime filter explicitly gates trading to mean-reverting (non-trending) states, the chop-paying regime.
  - side-prediction (candidate): Returns-independent: the inferred hidden-Markov regime state is itself an observable derived from spread/volatility dynamics (not P&L); the claim 'reversion only in certain regimes' predicts that spread half-life estimated on price residuals differs significantly across the filtered states — checkable on price data alone. CAVEAT: in-scope universe lacks Shanghai INE access, and the paper found Western-benchmark-only spreads NOT consistently profitable, weakening codifiability for a USOIL-only book. | independence=yes
  - claimed perf (UNVERIFIED): n/a
  - source: Fanelli, V., Fontana, C., Rotondi, F. (2023). 'A hidden Markov model for statistical arbitrage in international crude oil futures markets.' arXiv:2309.00875. <https://arxiv.org/abs/2309.00875>

### ratio mean-reversion (two-leg precious-metals spread)

- **Gold/Silver ratio extreme-level mean reversion (long-short metals spread)** — instr: XAUUSD | d=undatable
  - mechanism: Classic GSR contrarian rule: when gold/silver price ratio is at a historic extreme high (gold rich vs silver), short gold / long silver; when extreme low, long gold / short silver; ratio reverts toward its long-run mean (~65-70:1). CME Group education page documents the ratio-spread construction; ratio is unreliable for short-term timing (can stay extreme for months) and needs additional confirmation.
  - chop-fit: Pays from reversion of a range-bound ratio when neither metal trends decisively — earns in the sideways/oscillating metals regime where the gold-trend leg goes flat.
  - side-prediction (candidate): Returns-independent: GSR mean-reversion is driven by the relative supply/industrial-demand profile of silver vs gold; an observable signature is that the ratio's distance from its long-run mean predicts subsequent ratio change (a price-only, P&L-independent regression). The CME/practitioner sources themselves warn the ratio can stay extreme for months — flag as weak short-term timing. | independence=yes
  - claimed perf (UNVERIFIED): n/a
  - source: CME Group, 'Gold and Silver Ratio Spread Trade' (Introduction to Precious Metals course). Mechanism also in UC Denver J.P. Morgan Center, 'The Gold to Silver Ratio' (2020). <https://www.cmegroup.com/education/courses/introduction-to-precious-metals/gold-and-silver-ratio-spread-trade>

### cointegration spread reversion + Kalman dynamic hedge + ML regime gate

- **Cointegration/Kalman gold-silver spread with ML regime filter (Mittal & Mittal 2025)** — instr: XAUUSD | d=2025-10-01
  - mechanism: Mittal & Mittal: cointegrate gold-silver (COMEX GC/SI futures and GLD/SLV ETFs, 2015-2025), estimate a dynamic hedge ratio via Kalman filtering, standardize the spread to a z-score for mean-reversion entries, and gate trades with ML classifiers (Gradient Boosting, SVM) trained on volatility/macro/sentiment features to distinguish stable vs unstable spread regimes. Claims higher Sharpe and lower drawdown than static stat-arb, especially in 2020/2022/2024 high-vol episodes.
  - chop-fit: Mean-reversion of a cointegrated metals spread, with an ML gate that is claimed to add most value in high-volatility/unstable regimes — the chop window where trend legs fail.
  - side-prediction (candidate): Returns-independent: the ML 'stable vs unstable regime' label is built from volatility/macro/sentiment inputs (not P&L), so its predictive content can be audited by checking whether the regime label forecasts realized spread half-life on price data alone. CAVEAT: unverified preprint, possible overfit (ML + Kalman + feature search on a single 10-yr window) — treat performance claims as unconfirmed. | independence=yes
  - claimed perf (UNVERIFIED): n/a
  - source: Mittal, V.K. & Mittal, R. 'Gold Silver Pair Trading - Mean Reversion Strategy Using Machine Learning.' SSRN abstract 5710242 / Authorea preprint (2025). Title+authors+instruments verified via SSRN/ResearchGate listings; SSRN/Authorea PDF returned 403 so internal performance numbers NOT independently fetched. <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5710242>

### anchor-reversion (previous-close / overnight)

- **Overnight/intraday cross-period reversal (Tug-of-War)** — instr: SPX500, NAS100, DJ30 | d=2015-04-11
  - mechanism: Firm/index returns show within-period continuation but a robust CROSS-period reversal: a high overnight (prev-close-to-open) return is offset by a relatively low/negative intraday (open-to-close) return, and vice versa. Trade fades the overnight move during the day session, anchoring to the previous close.
  - chop-fit: Pays when an overnight/prev-close anchor overshoots and the day session reverts rather than follows through — i.e. exactly the follow-through-deficit/chop regime where the book's trend legs go flat.
  - side-prediction (candidate): Sign asymmetry in the return decomposition: overnight component and intraday component of the SAME name carry systematically OPPOSITE signs (negative overnight-vs-intraday correlation), a positioning/flow signature checkable from open/close/prev-close prices alone, independent of any strategy P&L. | independence=yes
  - claimed perf (UNVERIFIED): n/a
  - source: Lou, Polk & Skouras, 'A Tug of War: Overnight Versus Intraday Expected Returns', Journal of Financial Economics 134(1) 2019, pp.192-213 (WP circulated ~2015) <https://www.sciencedirect.com/science/article/abs/pii/S0304405X19300650>

### anchor-reversion (intraday VWAP)

- **Session-VWAP standard-deviation band reversion** — instr: SPX500, NAS100, DJ30, XAUUSD, MNQ, MYM, MGC | d=undatable
  - mechanism: Compute session VWAP and bands at vwap +/- k*sigma (default k=2.0). Fade: short when price extends above the upper band, long when below the lower band, requiring a rejection candle (pin/engulfing/volume spike). Exit at VWAP (optionally half at VWAP, trail through to opposite band).
  - chop-fit: Explicitly conditioned on low-ADX, lunchtime/early-afternoon chop on ES/NQ — the strategy is designed to harvest range oscillation and is gated OFF during trends, so its P&L concentrates in the regime the trend book misses.
  - side-prediction (candidate): Conditional reversion intensity: realized k-sigma VWAP excursions should mean-revert to VWAP at materially higher rate on low-ADX days than high-ADX days; the ADX-conditioned reversion-frequency gap is observable from price/VWAP series without trading. | independence=yes
  - claimed perf (UNVERIFIED): n/a
  - source: crosstrade.io 'VWAP reversion strategy' (rule set: vwap +/- 2*sd, fade to VWAP, ADX<25 filter); corroborated by metrotrade.com and chartswatcher VWAP guides <https://crosstrade.io/learn/trading-strategies/vwap-reversion>

### anchor-reversion (previous-close gap-fill)

- **Opening-gap fade to previous close (gap-fill)** — instr: SPX500, DJ30, NAS100, MYM, MNQ | d=2024-07-17
  - mechanism: Define gap = open vs prior-session close. Fade the gap toward prior close (short up-gaps, long down-gaps), target = prior close (full fill); rules scale by gap size: for gaps <~0.5% target full fill with stop ~= gap size; for larger gaps take 50% of gap with 50% stop. Filter to small / low-volume gaps.
  - chop-fit: Gap-fill is a same-session reversion to a prior-close anchor; it profits from overnight overshoot being reabsorbed (no follow-through), decorrelated from trend continuation.
  - side-prediction (candidate): Fill-rate monotonicity: same-day fill probability should decline monotonically with gap size and with overnight volume, and be higher for down-gaps than up-gaps — a calendar/price-only seasonality signature checkable from OHLC history without running the strategy. | independence=yes
  - claimed perf (UNVERIFIED): n/a
  - source: EquitySet 'A Literal Gap Analysis of the S&P 500'; ainvest 'Filter Small, Low-Volume Gaps for High-Fill Setup' (E-mini ES, 2,646 days 2014-2024); QuantifiedStrategies 'Gap Fill Trading Strategies' <https://equityset.com/insights-analysis/gaps-gaps-everywhere-a-comprehensive-gap-analysis-of-the-s-and-p-500>

### short-horizon time-series/cross-sectional reversal (contrarian), volume-conditioned

- **Trading-activity / volume-conditioned weekly contrarian reversal in futures (Wang & Yu)** — instr: USDJPY, USDCAD, EURUSD, GBPUSD, USOIL, XAUUSD, DJ30, NAS100, SPX500, micro-rates | d=2004-06
  - mechanism: In 24 US futures markets, weekly returns reverse: a contrarian strategy that sells past best performers and buys past worst performers earns positive profits. Reversal profits are POSITIVELY associated with lagged increases in trading volume and NEGATIVELY associated with lagged changes in open interest — i.e. high-volume/low-OI contracts overreact and then revert. Mechanism framed as overreaction + liquidity/inventory effects, not risk.
  - chop-fit: It is a pure reversal/overreaction mechanism — it explicitly fades prior-period winners and buys prior-period losers, so it earns most when moves do NOT follow through (chop/range), exactly the regime where the trend book goes flat.
  - side-prediction (candidate): Trading volume and open interest, both observable independently of the strategy's P&L: the paper predicts reversal magnitude rises with a contemporaneous spike in trading volume and falls with rising open interest — a checkable order-flow/positioning signature. | independence=yes
  - claimed perf (UNVERIFIED): Reported in a QuantPedia replication (1983-2000): ~29.6% ann. return, 31.4% vol, Sharpe ~0.82, MaxDD -58.65% (replication numbers, not the journal's).
  - source: Wang, Changyun & Yu, Min (2004). 'Trading activity and price reversals in futures markets.' Journal of Banking & Finance 28(6): 1337-1361. <https://ideas.repec.org/a/eee/jbfina/v28y2004i6p1337-1361.html>

### short-horizon reversal driven by periodic market-closure liquidity provision

- **Overnight-Intraday (close-to-open / open-to-close) reversal in futures (Della Corte, Kosowski & Wang)** — instr: DJ30, NAS100, SPX500, USOIL, XAUUSD, USDJPY, EURUSD, GBPUSD, USDCAD, micro-rates | d=2015-01
  - mechanism: Assets with low (high) past OVERNIGHT (close-to-open) returns earn high (low) subsequent INTRADAY (open-to-close) returns. A daily long-low/short-high overnight-return strategy delivers excess return and Sharpe 2-5x larger than the conventional close-to-close reversal across equity-index, interest-rate, commodity and currency futures. Consistent with the Hong & Wang (2000) continuous-time model of periodic market closures: closures force liquidity providers to demand a premium, creating a temporary overnight push that reverses intraday.
  - chop-fit: It systematically fades the overnight move (a gap-fade / reversal), so it pays when overnight directional pushes do not continue into the session — i.e. non-trending, mean-reverting follow-through-deficit conditions that starve the breakout/trend legs.
  - side-prediction (candidate): The intraday-reversal premium should concentrate immediately after the market open and decay within minutes (a microstructure/liquidity-provision timing signature) and be larger in less-liquid contracts — both observable from the intraday return path and spreads, independent of the strategy P&L. | independence=yes
  - claimed perf (UNVERIFIED): For US stocks the close-to-open/open-to-close (CO-OC) version reports ~1.68% avg daily gross return vs 0.33% for conventional close-to-close; gross annualized Sharpe ~24 vs ~5.5 (gross, pre-cost, equities). Futures Sharpes reported 2-5x conventional reversal. Treat as gross, capacity-limited.
  - source: Della Corte, P., Kosowski, R. & Wang, T. (2015/2017). 'Market Closure and Short-Term Reversal' (a.k.a. 'Overnight-Intraday Reversal Everywhere'). Working paper, Imperial College / CICF. <https://www.cicfconf.org/sites/default/files/paper_357.pdf>

### event-conditioned short-horizon contrarian (mean reversion) on abnormal-return days

- **Gold contrarian effect after abnormal-return days (Caporale & Plastun)** — instr: XAUUSD | d=2020-07
  - mechanism: Using daily Gold and Oil prices (2009-2020), on days with abnormal (outlier) returns the next-day pattern differs by asset: OIL shows a momentum (continuation) effect, but GOLD shows a CONTRARIAN effect — abnormal gold moves tend to reverse the following day. Trading simulations on the gold contrarian pattern generate abnormal profits net of the authors' filters.
  - chop-fit: It is an explicit one-day mean-reversion / spike-fade on gold: it profits when an outsized gold move reverses rather than extends, complementing (and decorrelating from) the long-gold-TREND leg that wants follow-through.
  - side-prediction (candidate): The sign asymmetry itself is a returns-independent, checkable prediction: gold reverses but oil continues after abnormal days. One can verify the next-day conditional-return sign separately for gold vs oil (and across thresholds) without trading the strategy. | independence=yes
  - claimed perf (UNVERIFIED): Authors report the gold contrarian and oil momentum effects 'can be exploited to generate abnormal profits' in trading simulations; no clean Sharpe quoted in the abstract (daily gold/oil, 2009-2020).
  - source: Caporale, G.M. & Plastun, A. (2021). 'Gold and oil prices: abnormal returns, momentum and contrarian effects.' Financial Markets and Portfolio Management 35: 353-368 (also CESifo WP 8445 / SSRN 3662052). <https://link.springer.com/article/10.1007/s11408-021-00380-w>

### cross-sectional currency mean reversion (deviation-from-average reversal)

- **Cross-sectional mean reversion across G6 currency futures (Beluska & Vojtko / QuantPedia)** — instr: USDJPY, USDCAD, EURUSD, GBPUSD | d=2024-10-25
  - mechanism: Across six FX futures (AUD, GBP, CAD, EUR, CHF, JPY), each currency's cumulative return is compared to the average of all six. Currencies above the average are treated as overvalued (short) and those below as undervalued (long), betting the cross-section reverts toward its mean. Position size scales with the deviation (linear or exponential weighting), rebalanced monthly.
  - chop-fit: Cross-sectional FX mean reversion: it buys laggards and sells leaders on the bet they converge, paying when currency trends stall and revert — a chop/range mechanism orthogonal to single-leg trend following.
  - side-prediction (candidate): none-apparent (the article reports only P&L-based results; it offers no order-flow/positioning/term-structure observable that can be checked independently of the strategy's own returns). | independence=none-apparent
  - claimed perf (UNVERIFIED): Linear weighting Sharpe ~0.12; exponential weighting Sharpe ~0.35 (Feb 2007-Sep 2024, monthly, 6 FX futures). Modest; weak standalone but cited as the documented FX-MR construction.
  - source: Beluska, S. & Vojtko, R. (2024). 'How to Build Mean Reversion Strategies in Currencies.' QuantPedia (research note; also SSRN abstract_id=5002058). <https://quantpedia.com/how-to-build-mean-reversion-strategies-in-currencies/>

### short-horizon return reversal / overreaction (canonical)

- **Foundational short-term return reversal — Jegadeesh (1990) / Lehmann (1990)** — instr: SPX500, DJ30, NAS100 | d=1990-02
  - mechanism: Lehmann (1990) documents weekly stock-return reversal (a zero-cost portfolio buying losers/selling winners earns reliable profits); Jegadeesh (1990) documents monthly reversal (~2%/month buying prior-month losers, selling winners, 1934-1987). Interpreted as overreaction / 'fads' / temporary liquidity imbalance + bid-ask bounce rather than risk premia.
  - chop-fit: The canonical mean-reversion/overreaction anomaly: it earns precisely when recent moves over-extend and snap back, the chop/follow-through-deficit regime the trend book cannot monetize.
  - side-prediction (candidate): Later work attributes much of the weekly reversal to liquidity-provision compensation and bid-ask bounce — predicting reversal profits should be larger in low-liquidity/high-spread names and shrink after costs; a spread/liquidity observable checkable independent of the strategy return. | independence=yes
  - claimed perf (UNVERIFIED): Jegadeesh (1990): equal-weight loser-minus-winner ~2%/month (monthly, US single-name equities, 1934-1987, gross). Lehmann (1990): reliable weekly reversal profits. Single-name equity — included as mechanism provenance, not a directly tradeable index leg.
  - source: Jegadeesh, N. (1990) 'Evidence of Predictable Behavior of Security Returns,' Journal of Finance 45(3):881-898; Lehmann, B. (1990) 'Fads, Martingales, and Market Efficiency,' Quarterly Journal of Economics 105(1):1-28. <https://www.bauer.uh.edu/rsusmel/phd/jegadeesh-titman93.pdf>

### intraday FX statistical mean reversion with explicit trend/regime gating

- **Regime-conditioned intraday FX statistical mean reversion (Bhatti)** — instr: EURUSD, GBPUSD, USDJPY, USDCAD | d=2026-01-17
  - mechanism: Short-horizon intraday FX prices frequently mean-revert, driven by liquidity imbalances and dealer inventory adjustments, but this behavior deteriorates sharply in persistent trending regimes. The paper proposes a regime-conditioned statistical mean-reversion framework that gates the MR signal on a detected regime so trades are taken in mean-reverting states and suppressed in trends.
  - chop-fit: It is explicitly engineered to earn in mean-reverting/range regimes and to switch OFF in trends — the exact complement to the trend legs, addressing the book's 2020-2023-style chop weakness by construction.
  - side-prediction (candidate): The stated driver (dealer inventory / liquidity imbalance) implies an order-flow / bid-ask-spread / quote-imbalance signature that should precede the reversion — checkable from microstructure data independent of strategy P&L. (Caveat: must verify the paper supplies an explicit, testable form rather than asserting the channel.) | independence=none-apparent
  - claimed perf (UNVERIFIED): Not verified — SSRN abstract page returned 403 on fetch; performance numbers could not be confirmed and are therefore omitted. Citation/existence confirmed via SSRN search index only.
  - source: Bhatti, A. (2026). 'A Regime-Conditioned Statistical Mean Reversion Framework for Intraday FX Markets.' SSRN working paper, abstract_id=6087107. <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6087107>

### calendar/seasonality (auction/flow)

- **Turn-of-the-Month (ToM) in equity indexes** — instr: SPX500, DJ30, NAS100 | d=1987
  - mechanism: Buy the equity index ~1 day before month-end and sell at the close of the 3rd trading day of the new month; the index earns abnormal positive returns in the last ~4 and first ~3 trading days of each month, driven by month-end pension/payroll cash inflows and model rebalancing.
  - chop-fit: It is a fixed-calendar flow impulse independent of trend follow-through, so it earns in 2020-2023-style chop where the book's momentum legs go flat.
  - side-prediction (candidate): Returns-independent: trading volume / institutional net buy imbalance should spike on the last trading day and first 3 trading days of the month; verifiable from volume and fund-flow data without the strategy's P&L. | independence=yes
  - claimed perf (UNVERIFIED): Quantpedia: 7.2%/yr, vol 6.9%, Sharpe 1.04, maxDD -20.8% (1926-2005, SPY proxy).
  - source: Aggregator: Quantpedia 'Turn of the Month in Equity Indexes'. Primary sources cited: McConnell & Xu, 'Equity Returns at the Turn of the Month', Financial Analysts Journal (SSRN 917884); orig. Lakonishok & Smidt (1988). Futures-specific: Carcano & Tornero, 'Calendar Anomalies in Stock Index Futures'. <https://quantpedia.com/strategies/turn-of-the-month-in-equity-indexes>

### calendar/seasonality

- **Sell-in-May / Halloween seasonal in equity index futures** — instr: SPX500, DJ30, NAS100 | d=2016-01-22
  - mechanism: Hold long equity index futures from ~6 trading days before end-October through the first trading day of May, hold cash May-October; the Nov-Apr half-year historically delivers most of the annual equity return while May-Oct is weak/crash-prone.
  - chop-fit: Mechanism is a seasonal de-risking window, not trend continuation; it pays/protects exactly when the weak May-Oct period chops and trend legs stall.
  - side-prediction (candidate): Returns-independent: realized-volatility and crash frequency should be measurably higher in the May-Oct window than Nov-Apr across decades; checkable from price-vol history alone. | independence=yes
  - claimed perf (UNVERIFIED): Quantpedia: ~2x B&H final wealth on S&P500, ~3x on Russell 2000 (1993-2015).
  - source: Aggregator: Quantpedia. Primary: Dzahabarov & Ziemba, 'Sell in May and Go Away in the Equity Index Futures Markets', SSRN 2721068 (2016). <https://quantpedia.com/sell-in-may-and-go-away-in-the-equity-index-futures-markets/>
- **Gold seasonal market-timing (Sep/Nov demand window)** — instr: XAUUSD, MGC | d=2018-08-06
  - mechanism: Hold gold only in September and November (cash otherwise); these months show positive and significant gold returns historically, attributed to Indian wedding-season jewelry demand.
  - chop-fit: A date-driven seasonal demand pulse in gold, decoupled from trend follow-through, so it can earn in flat gold regimes — BUT see caveat: the paper finds the seasonal rule is NOT robust to data-snooping (only trend rules survive).
  - side-prediction (candidate): Returns-independent: physical gold import/jewelry-demand volume into India should peak around the Sep/Nov window (festival/wedding season) — checkable from trade/import statistics, not strategy P&L. | independence=yes
  - claimed perf (UNVERIFIED): Quantpedia/paper: large raw gains vs buy-and-hold, but explicitly NOT robust to data-snooping bias for the seasonal rule (only technical trend rules survive) — treat as weak.
  - source: Aggregator: Quantpedia. Primary: Bartsch, Baur, Dichtl, Drobetz, 'Investing in the Gold Market: Market Timing or Buy-and-Hold?', SSRN 3202658 (2018-08-06). <https://quantpedia.com/an-extensive-test-of-market-timing-strategies-in-the-gold-market/>

### mean-reversion / overreaction reversal

- **Short-term reversal in futures (volume/open-interest sorted)** — instr: USOIL, USDJPY, USDCAD, EURUSD, GBPUSD | d=2004-06
  - mechanism: Weekly (Wed-Wed) rebalance: within high-volume, low-open-interest contracts, go long the prior-week worst performers and short the prior-week best performers, position-sized by deviation from the group mean; price reversals follow short-horizon overreaction.
  - chop-fit: It is a direct contrarian bet against the prior week's move, conditioned on high-volume/low-OI overreaction — i.e. it monetizes exactly the trend-failure/follow-through-deficit the book is weak in.
  - side-prediction (candidate): Returns-independent: the reversal magnitude should increase with weekly volume change and decrease with open-interest (hedging) — a cross-sectional order-flow signature checkable from volume/OI data without the strategy's P&L. | independence=yes
  - claimed perf (UNVERIFIED): Quantpedia: 29.6%/yr, vol 31.4%, Sharpe 0.82, maxDD -58.7% (1983-2000, 24 US futures) — high vol/DD, sizing-sensitive.
  - source: Aggregator: Quantpedia 'Short Term Reversal with Futures'. Primary: Wang (Yu), 'Trading activity and price reversals in futures markets', J. Banking & Finance (study period 1983-2000). <https://quantpedia.com/strategies/short-term-reversal-with-futures>

### carry

- **FX carry trade (rate-differential cross-section)** — instr: USDJPY, USDCAD, EURUSD, GBPUSD | d=1984
  - mechanism: Go long the highest-policy-rate currencies and short the lowest-rate currencies (monthly rebalance over a 10-20 currency set), earning the interest-rate differential plus the forward-premium bias; uncovered interest parity fails so high-yielders do not depreciate enough to offset carry.
  - chop-fit: Carry income is a yield, not a directional bet, so it accrues in flat/range FX regimes where the book's trend legs make nothing; payoff is decorrelated from momentum (though it carries crash-tail risk).
  - side-prediction (candidate): Returns-independent: carry-basket returns should covary with the cross-currency interest-rate differential and exhibit negative skew / crash risk that spikes with FX-vol (VIX-like) — checkable from rate-differential and realized-skew data, not the strategy P&L. | independence=yes
  - claimed perf (UNVERIFIED): Quantpedia/DB: 7.27%/yr, vol 9.6%, Sharpe 0.29, maxDD -32.1% (since 1989).
  - source: Aggregator: Quantpedia 'FX Carry Trade'. Primary source cited: Deutsche Bank, 'Currency Carry Returns' (March 2009); forward-premium-puzzle literature. <https://quantpedia.com/strategies/fx-carry-trade>

### mean-reversion / stress-reversal

- **Correlated cross-asset stress reversal (intraday liquidity provision)** — instr: SPX500, NAS100, DJ30, USOIL, XAUUSD | d=2025-04-25
  - mechanism: Detect a stress day when risky assets (SPY, USO, GLD) fall together — or fall while Treasuries (IEF) rally — then buy the equity index at that day's close and exit the next day's close, providing liquidity into a correlated de-risking overshoot.
  - chop-fit: It buys overshoot reversals after correlated de-risking days — the snap-back behavior characteristic of range/chop regimes rather than trend continuation.
  - side-prediction (candidate): Returns-independent: the gold/treasury (GLD/IEF) co-movement with falling equities is the entry trigger — a cross-asset correlation signature observable directly from those assets' returns, independent of the equity P&L. | independence=yes
  - claimed perf (UNVERIFIED): Quantpedia shows positive cumulative equity curves for the diversified 3-signal version; no single headline Sharpe/return stated numerically.
  - source: Quantpedia original research (Cyril Dujava), 'Short-Term Correlated Stress Reversal Trading', 2025-04-25. No external academic primary; aggregator is the source. <https://quantpedia.com/short-term-correlated-stress-reversal-trading/>

### trend-fade / mean-reversion

- **Kaufman Fade-The-Trend (QuantConnect port by Pardhu Nani)** — instr: SPX500, NAS100, DJ30, MGC, MYM, MNQ | d=undatable
  - mechanism: Fade short-term moves while a long-term trend filter is up: e.g. SPY long when 50-day trend up, exit when 4-day short trend turns up; QQQ uses 90-day/4-day; IWM 100-day/10-day. Profit target = entry + 3.5x 10-day ATR. Trade only when 20-day annualized vol is between 0.10 and 0.50 (skips dead-low and extreme-high vol).
  - chop-fit: It explicitly fades short-term overshoot and only acts inside a vol band, harvesting the bounce when moves fail to follow through - the chop/follow-through-deficit regime the trend book bleeds in.
  - side-prediction (candidate): The vol-band gate (0.10-0.50 annualized) is a returns-independent observable: the mechanism predicts edge concentrates in mid-vol regimes and disappears outside the band, checkable directly against realized-vol buckets without the strategy's P&L. | independence=yes
  - claimed perf (UNVERIFIED): None disclosed in post (backtest 2000-present referenced, no metrics).
  - source: 'Fade The Trend Strategy - Mean Reversion Algorithm by Perry J Kaufman', author Pardhu Nani, QuantConnect community forum (port of Kaufman, Trading Systems and Methods). <https://www.quantconnect.com/forum/discussion/15226/fade-the-trend-strategy-mean-reversion-algorithm-by-perry-j-kaufman/>

### gap-fade / intraday mean-reversion

- **Mind-the-Gap intraday gap-down reversal (Robert Wiener)** — instr: SPX500, NAS100, DJ30 | d=undatable
  - mechanism: On names above their 100-day SMA, if price gaps DOWN more than 1.2x the 14-day ATR vs prior close at the open, go long; liquidate all positions 15 minutes after the open.
  - chop-fit: Pure gap-fade: it profits from opening overreactions reverting, a mechanism uncorrelated with intraday trend continuation and active precisely when moves fail to extend.
  - side-prediction (candidate): The mechanism predicts a measurable post-open mean-reversion signature on large (>1.2x ATR) gap-down opens in up-trend names - testable from the gap-conditioned 15-minute return distribution independent of the strategy's own P&L. | independence=yes
  - claimed perf (UNVERIFIED): None disclosed; author states it is a learning project and 'isn't optimal'; staff flagged 10 implementation bugs.
  - source: 'Mind the Gap: An Intraday Reversal Strategy Using Gap Downs and ATR', author Robert Wiener, QuantConnect community forum. <https://www.quantconnect.com/forum/discussion/19075/mind-the-gap-an-intraday-reversal-strategy-using-gap-downs-and-atr/>

### band mean-reversion

- **Bollinger Bands Mean Reversion by Kevin Davey (TradingView, EdgeTools)** — instr: XAUUSD, NAS100, DJ30, EURUSD, USDJPY, SPX500 | d=2024-10-24
  - mechanism: Bollinger Bands = 20-period SMA +/- 2.0 stdev. Buy when price falls below the lower band (oversold); exit the long when price closes above the upper band (overbought).
  - chop-fit: Band-edge fade pays when price oscillates around the mean and reverts off extremes - the defining behavior of range/chop regimes; it stalls only in strong trends, the inverse of the existing book.
  - side-prediction (candidate): none-apparent (mechanism is defined off the strategy's own price/band signals; no independent order-flow/seasonality/term-structure implication stated). | independence=no-reduces-to-pnl
  - claimed perf (UNVERIFIED): None disclosed in script description.
  - source: 'Bollinger Bands Mean Reversion by Kevin Davey', published by user EdgeTools, TradingView open-source script, 2024-10-24 (method attributed to Kevin Davey, multi-time World Cup Trading Championship participant). <https://www.tradingview.com/script/umOCSa0t/>

### oscillator-reversal / mean-reversion

- **Dynamic RSI Mean Reversion Strategy (nathanfarmer, TradingView)** — instr: XAUUSD, NAS100, DJ30, USDJPY, EURUSD, USDCAD | d=2024-11-04
  - mechanism: RSI overbought/oversold thresholds are widened/tightened by ATR (expand bands in high vol, tighten in low vol). Enter when RSI crosses back through the dynamic threshold AND the move is not countertrend (MA-crossover trend filter blocks longs in downtrends / shorts in uptrends). Stop loss set at an ATR distance from entry.
  - chop-fit: Oscillator-reversal entries on RSI extremes are a reversion mechanism that earns when price swings back from overbought/oversold inside a range - active when trends stall.
  - side-prediction (candidate): The ATR-scaled threshold makes a returns-independent prediction: reversion-entry density should rise as realized vol rises (bands widen), checkable from the vol-vs-signal-count relationship without the strategy's P&L. | independence=yes
  - claimed perf (UNVERIFIED): None disclosed; author states results were deliberately not cherry-picked.
  - source: 'Dynamic RSI Mean Reversion Strategy', author nathanfarmer, TradingView open-source script, published 2024-11-04. <https://www.tradingview.com/script/K9FLcueo-Dynamic-RSI-Mean-Reversion-Strategy/>

### band + oscillator mean-reversion

- **Bollinger Bands Mean Reversion using RSI [Krishna Peri] (thechadyogi, TradingView)** — instr: XAUUSD, NAS100, DJ30, EURUSD, USDJPY, SPX500 | d=2025-12-06
  - mechanism: Long when RSI reaches oversold AND at least one bullish candle closes back inside the lower Bollinger Band; short when RSI reaches overbought AND at least one bearish candle closes back inside the upper band. Targets exhaustion moves that snap back toward the middle band. Author notes it is optimized for sideways/ranging markets and degrades in strong trends.
  - chop-fit: Explicitly built for sideways/ranging markets, fading exhaustion back to the mean - the chop regime where the trend book goes flat; author flags it weakens in strong trends, confirming the decorrelation direction.
  - side-prediction (candidate): none-apparent (entry is defined purely by the strategy's own BB/RSI/candle signals; no independent positioning, spread, or seasonality implication is offered). | independence=none-apparent
  - claimed perf (UNVERIFIED): None disclosed in script description.
  - source: 'Bollinger Bands Mean Reversion using RSI [Krishna Peri]', author thechadyogi, TradingView open-source script, published 2025-12-06. <https://www.tradingview.com/script/XRPeqEdA-Bollinger-Bands-Mean-Reversion-using-RSI-Krishna-Peri/>

## EXCLUDED — source MISREPRESENTED (not catalog-worthy)

- **Overnight gap fade with day-of-week conditioning (SPY/QQQ)** — Source is REAL and reachable: Ryan Mallory, "Fading the Gap: How Large Overnight Moves in SPY and QQQ Play Out During the Trading Day," SharePlanner, Apr 26 2025 (also syndicated on TalkMarkets). Author, title, venue, date, and the core mechanism (1%+ gap fade in SPY/QQQ with a Monday/day-of-week ef
- **Bollinger-Band %b / outer-band tag fade-to-mean** — Source URL is live and real (LuxAlgo, "Mean Reversion Trading: Fading Extremes with Precision", published 2025-08-19) and DOES describe the generic mechanism: fade outer Bollinger-band tags (close beyond +/-2 to +/-3 sigma) back toward the moving average, gated by RSI<30 / RSI>70 and volume, exiting
- **WTI crude calendar-spread (front-vs-deferred) directional contango/backwardation trade** — Both cited sources are real and reachable. The headline source — CME Group Economic Research, Erik Norland, "Implications of WTI Oil Futures In Backwardation Amid the Supply Crunch," published 2026-04-16 (verified via cmegroup.com URL + Yahoo Finance/AlphaMaven/MarketScreener mirrors) — exists and d
- **Pivot-point (Camarilla) reversion fade** — All three cited sources are real and reachable, but the row stitches them into a mechanism none of them actually states, and two are cited against their own conclusions. (1) source_url (edgeful 'trading pivot points', reachable, published 2025-09-25) describes STANDARD pivots (PP, R1-R3, S1-S3) via 

## Coverage gaps (no silent caps — §5)

- SSRN full-text PDFs return HTTP 403 to WebFetch across the board (Bhatti 6087107, Vu-Bhattacharyya 4878676, Fuertes-Miffre-Rallis, Cieslak-Morse-Vissing-Jorgensen, Lucca-Moench, Mittal-Mittal 5710242, Della Corte-Kosowski). Title/author/date/abstract confirmed via search snippets and mirrors, but exact in-paper rules, parameters, out-of-sample splits, and Sharpe/DD tables were NOT read firsthand — treat all academic performance figures as abstract/aggregator-level, not primary-table-verified.
- QuantifiedStrategies.com (the single richest source of rule-specific dated backtests for RSI(2), Williams %R, ConnorsRSI, Bollinger, gap-fill, pivot, ORB) is Cloudflare/CAPTCHA bot-walled — all its CAGR/WR/PF figures are snippet-level, not page-verified. StockCharts ChartSchool and quantitativo.com were the accessible cross-checks for rules/dates.
- TradingView script backtest tabs (embedded PF/Sharpe/DD report) and raw Pine source do not render through WebFetch (auth/JS-gated) — every TV script (Davey/EdgeTools, ayusattv, nathanfarmer, thechadyogi/Krishna Peri) is rules/description-only with no verifiable performance and unverified exact thresholds/session windows/exit logic; two TV scripts are undatable to a year (page shows month/day only).
- INSTRUMENT-TRANSFER GAP (pervasive): essentially all verified evidence is on US equity ETFs/indices (SPY/QQQ/IWM), single-name US equities, or broad multi-asset/multi-futures cross-sectional baskets. No rule-complete, independently-backtested chop/MR/range study was found natively on the in-scope FX pairs (USDJPY/USDCAD/EURUSD/GBPUSD), USOIL, XAUUSD, or CME micro futures (MGC/MYM/MNQ/micro-rates). Cross-sectional basket Sharpes (carry, futures-reversal) do NOT transfer to 3-5 single-instrument ports.
- TIMEFRAME-TRANSFER GAP: the locked book trades 15m; nearly all verified MR/range/gap evidence is daily-bar (oscillator family, IBS, gap-fill, seasonality) or session-level. No verified intraday-15m squeeze/range/oscillator-fade backtest was found — 15m transfer is unvalidated for the whole oscillator and band family.
- GOLD (XAUUSD) is a specific coverage hole and a contrary signal: no datable rule-complete XAUUSD-specific opening-range or band/oscillator FADE backtest exists in open sources, AND one source reported naive RSI MR FAILS on gold (23% WR, trending). The only XAUUSD-native CONFIRMED reversal evidence is Caporale-Plastun's abnormal-day contrarian (daily granularity, not 15m). The gold-trend leg (Guardian) is likely unsuited to naive fade overlays.
- SINGLE-ACCOUNT / LANE-B CONSTRAINT on the entire stat-arb/spread/carry tier: GGR, Fil, WTI/Brent, HMM-crude, gold/silver-ratio, Kalman-ML, FX-carry, and cross-sectional futures-reversal are intrinsically multi-leg (long one instrument, short another). On a single prop account that cannot cleanly hold simultaneous opposing legs, these are likely NON-CODIFIABLE as-is; only the decorrelating mechanism is harvestable, and a single-leg residual/ratio-overlay proxy needs separate design.
- Returns-independent side-predictions are mechanism-IMPLIED for most rows — only the IBS bucket-monotonicity is explicitly demonstrated in-source. The Bhatti FX-MR microstructure side-prediction collapsed on second read (the paper's actual signal is price-z-score; 'dealer inventory' is narrative-only). Treat side-predictions as untested falsifiers to run on our own panels, not as established facts.
- STRENGTH/DECAY (not source) risk on the most-cited rows: Connors RSI(2) family (post-2014 decay disclosed), turn-of-month, Sell-in-May, pre-FOMC drift, FX carry, and overnight-long are all heavily-mined, decades-OOS-exposed anomalies with documented post-publication decay or crowding. A publication-date OOS gate weighting the post-sample window is mandatory before any GO. Gold Sep/Nov seasonal explicitly fails Hansen SPA data-snooping in its own source.
- Primary book texts unread: Connors & Alvarez 'Short Term Trading Strategies That Work' (2008), Connors & Raschke 'Street Smarts' (1996), Bollinger 'Bollinger on Bollinger Bands' (2001), Crabel 'Day Trading With Short-Term Price Patterns' (1990, NR7 origin, out-of-print). Book-sourced rules/win-rates (e.g. 88% cumulative-RSI SPY figure) are second-hand via practitioner references.
- Under-searched mechanism/source channels: auction-market / Market-Profile value-area-edge fade; stochastic %K-%D crossover fades (distinct from Williams %R); FX-microstructure-journal intraday/day-of-week fades (USDJPY/USDCAD time-of-day, Monday/weekend FX effects); option-expiration-week and Treasury-auction-cycle index calendar effects; DJ30-vs-NAS100 specific cointegration backtest (the most book-relevant index pair, not found as a discrete dated source); peer-reviewed gold/oil SD-band reversion (academic MR literature is overwhelmingly equities/FX); reproducible open-source code repos (GitHub) for any gap-fade/overnight/MR system; QuantConnect 'Quant League' equity curves (JS/auth-gated); invite-only/paid TradingView scripts (EdgeLabTrading XAUUSD MR, TomTrades86 — proprietary band rules omitted rather than guessed).

## Semantic duplicates merged (audit)

- Connors RSI(2)+200-SMA mean reversion: 6 rows collapsed to 1 ('Connors RSI(2) short-term mean reversion') — StockCharts/QuantifiedStrategies/practitioner restatements of the same 2008 Connors-Alvarez book mechanism (rows titled 'Connors RSI(2) short-term mean reversion (with 200MA trend filter)', 'Connors RSI(2) mean-reversion (long pullbacks above 200-SMA)', 'Connors RSI(2) short-term mean reversion', 'Connors RSI(2) mean-reversion (index/ETF oscillator fade)', plus two duplicate-titled entries).
- Cumulative RSI(2): 2 rows (both Quantitativo 2024-06-22, 'Squeezing more profits with cumulative RSI') merged to 1.
- Internal Bar Strength (IBS): 2 rows ('IBS one-day mean reversion' Alvarez/Pagonidis/arXiv + 'IBS effect daily mean-reversion') merged to 1.
- Tug-of-War overnight/intraday reversal: 2 rows (Lou-Polk-Skouras JFE 2019, 'A Tug of War') merged to 1.
- Della Corte-Kosowski / Liu et al. market-closure reversal: CICF paper_357 cited under 3 framings ('Market Closure and Short-Term Reversal' x2 + 'Overnight-Intraday Reversal Everywhere' Liu et al. SSRN 2730304) — same working-paper lineage; consolidated to 2 named distinct citations within one mechanism family.
- Bhatti regime-conditioned FX z-score MR (SSRN 6087107): 2 rows merged to 1.
- Kevin Davey / EdgeTools Bollinger Bands Mean Reversion (TradingView umOCSa0t): 2 identical rows merged to 1.
- FX carry trade (rate-differential cross-section, Quantpedia 'FX Carry Trade'): 2 rows merged to 1.
- Wang & Yu futures volume/OI weekly reversal (JBF 2004): 2 rows (direct journal + Quantpedia 'Short Term Reversal with Futures' codification) consolidated to 1 mechanism, both names retained.
- Global cross-asset Carry rates/bond sleeve (KMPV 2013/2018): 2 rows merged to 1.
- Index opening-gap-fade / gap-fill to prior close (QuantifiedStrategies-sourced): 2 index-gap-fade rows consolidated to 1.
- Turn-of-the-Month: 2 rows (McConnell-Xu SSRN 917884 / Quantpedia) merged to 1.
- Gold Sep/Nov seasonal: 2 rows (Baur 2013 + Bartsch et al. 2018 / Quantpedia) merged to 1.
- EXCLUDED as MISREPRESENTED (noted, not cataloged): 'Overnight gap fade with day-of-week conditioning (SPY/QQQ)' (Mallory SharePlanner — fabricated 61% Monday-revert and gap-up-drift figures not in source); 'Bollinger-Band %b / outer-band tag fade-to-mean' (LuxAlgo — ~60%/1:1R, %b thresholds, non-trending-crux, ES/NQ/CL/GC all analyst embellishment absent from source); 'Pivot-point (Camarilla) reversion fade' (sources cited against their own conclusions — QS says pivots untradeable, TradingView row is a breakout not a fade); 'WTI crude calendar-spread directional contango/backwardation trade' (CME source is market commentary that cautions against being long and does not describe the stated bull/bear spread rules).
