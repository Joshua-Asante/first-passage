# Gold versus WTI relative outlook — 2026-11-04

## Question, decision and scope

Will MGC outperform MCL in percentage price return over the next 5–10 trading
sessions? Ten sessions is the primary endpoint; five is an interim observation.
The operator requires confidence above 70% before endorsing a direction.

**Verdict: the evidence does not clear 70%; withhold a directional forecast.**
Gold-outperforming-oil is a plausible consequence of sustained de-escalation,
weaker dollar pricing and falling real yields. Current evidence does not establish
that combination, its persistence or a calibrated probability. This is also not
an endorsement of the opposite direction.

The same three-pass approach as the [equity investigation](2026-11-04-market-regime-and-equity-outlook.md)
was used: current conditions, historical-data suitability, and counterevidence plus
prospective falsification. No threshold search or optimized historical screen was
run. The historical stage stopped at input validation; missing evidence is not a
negative statistical result.

## Current evidence

TradingView was inspected through the Codex in-app browser. Late-evening quotations
already referred to the next Globex session; their near-zero daily changes must not
be substituted for the large moves in the completed November 4 session.

| Evidence | Reading | Interpretation |
|---|---|---|
| Completed November 4 session | December gold settled at $4,073, approximately +3.4%; December WTI reference settlement $88.12, approximately −8.3% | Roughly 11.7 percentage points of gold outperformance already occurred that day; it is not a forecast return |
| Continuous-chart recent performance, around 18:45–18:50 ET | MGC approximately +1.0% over the displayed five-day window versus MCL −14.1%; calendar month approximately −2.3% versus −1.1%; three months approximately −5.2% versus +12.9% | A recent relative reversal, not established medium-term gold leadership; continuous-contract returns have roll caveats |
| December gold daily technicals | Price approximately $4,076; 20-day SMA approximately $4,086; 50-day SMA approximately $4,242; RSI approximately 47 | Recovery toward its 20-day average, still below the longer trend |
| December WTI daily technicals | Price approximately $88.3; 20-day SMA approximately $97.1; 50-day SMA approximately $92.0; RSI approximately 38 | Sharp deterioration, with scope for a rebound; indicators are correlated price summaries, not independent probability votes |
| WTI named-contract curve | December approximately $88.3, January $87.2, February $86.0 | Near-term backwardation remains; consistent with near-term supply value, not proof of falling future spot prices |

Sources: [MGC overview](https://www.tradingview.com/symbols/COMEX_MINI-MGC1!/),
[MCL overview](https://www.tradingview.com/symbols/NYMEX-MCL1!/),
[December gold daily technicals](https://www.tradingview.com/symbols/COMEX_MINI-MGC1!/technicals/?contract=MGCZ2026),
[December WTI daily technicals](https://www.tradingview.com/symbols/NYMEX-MCL1!/technicals/?contract=MCLZ2026),
[WTI contracts](https://www.tradingview.com/symbols/NYMEX-MCL1!/contracts/).
The curve observations are delayed last prices, not a synchronized executable spread.

[Reuters' gold report](https://www.tradingview.com/news/reuters.com,2026:newsml_L2N46L182:0-gold-heads-for-biggest-daily-gain-since-august-as-dollar-weakens/)
confirmed the $4,073 December settlement and the weaker-dollar backdrop.
[Reuters' market column](https://www.tradingview.com/news/reuters.com,2026:newsml_L6N46L1DT:0-oil-tanks-stocks-leap-on-us-midterms/)
described the oil selloff as markets anticipating an end to the Iran war, including
Qatari mediation efforts. This is evidence of expectations; it does not verify a
peace agreement or restored shipping and production.

## Counterevidence that prevents a high-confidence call

**The oil market is not showing a simple physical surplus.** The
[November 4 EIA release](https://www.eia.gov/petroleum/supply/weekly/archive/2026/2026_11_04/download/summary.txt),
covering the week ending October 30, reported commercial crude stocks of 409.8 million
barrels, down 0.9 million and 4% below the five-year average. Distillate stocks fell
3.6 million barrels and were 13% below their five-year average. Total commercial
petroleum inventories fell 8.2 million barrels; four-week product supplied was
4.2% above the prior year. These US observations do not establish the global balance,
but they contradict an uncomplicated demand-collapse explanation for the selloff.

[OPEC's November 1 announcement](https://www.opec.org/pr-detail/620-1-november-2026.html)
kept the seven participating countries' September required production levels in
place for December. Unchanged targets do not prevent actual production or exports
from recovering after disruption, but the announcement itself was not a fresh quota
increase. Failed diplomacy or renewed disruption could restore the oil risk premium
quickly, especially after the large price decline already observed.

**Nominal-yield relief is not broad real-yield relief.** The current
[Treasury real-yield table](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_real_yield_curve&field_tdr_date_value=2026)
resolved the lag in the map/FRED observation: on November 4 the ten-year real yield
was **2.64%, down only 1 bp** from November 3; the five-year real yield was **2.39%,
up 4 bp**, and the seven-year was **2.51%, up 2 bp**. A decline in nominal yields
driven mainly by lower inflation compensation does not automatically make gold
materially cheaper to hold. The interpretation here is an inference from those
observations, not a causal estimate.

**Structural gold buying is supportive but too slow to calibrate this horizon.**
The [World Gold Council's September ETF report](https://www.gold.org/goldhub/data/global-gold-backed-etf-holdings-and-flows)
reported $10 billion of September inflows, $31 billion for Q3, and record holdings of
4,256 tonnes. The report was published October 7 and describes September, not the
November 4 shock. It supports a background demand case, not a ten-session hit rate.

Several favorable observations share one underlying political/de-escalation shock.
Counting weaker oil, weaker dollar, lower nominal yields and higher gold as four
independent confirmations would overstate the evidence. De-escalation can also
reduce gold's safe-haven demand; the relative response is not mechanically fixed.

## Historical-data audit

The FRED cash-series approach used for equities does not transfer directly:
[FRED removed the daily LBMA gold series in January 2022](https://fred.stlouisfed.org/news/2022/01/ice-benchmark-administration-ltd-iba-data-to-be-removed-from-fred).
No current matched gold/WTI cash panel was established through that route.

Existing private TradingView BAR_EXPORT files dated November 3 were inspected in
place. No vendor data was copied into this note or staged. A temporary read-only
audit used the repository's canonical signal/metadata decoders, selecting Entry rows
and checking the encoded close against the entry price, OHLC ordering, 15-minute
bar duration, symbol/timeframe metadata and conflicting duplicate timestamps.

| Audit item | MGC | MCL |
|---|---:|---:|
| Files inspected | 17 | 6 |
| Unique 15-minute bars | 358,488 | 125,685 |
| Earliest bar-open UTC | 2010-10-04 10:00 | 2021-07-11 22:00 |
| Latest bar-open UTC | 2026-11-02 21:45 | 2026-11-02 21:45 |
| Decode / price / shape errors | 0 | 0 |
| Conflicting duplicate timestamps | 0 | 0 |
| Nonpositive closes | 0 | 0 |
| File hashes found in current CME manifest | 0/17 | 0/6 |

These checks establish transport consistency, not research readiness. The suffix
identifies continuous tickers `MGC1!` / `MCL1!`, without per-bar expiry identities,
switch dates or adjustment settings. The shared possible span starts in July 2021;
the micro oil history does not include April 2020. File naming as November 3 does
not mean the final completed observation is November 3.

**No historical forward win rate is claimed.** MCL's monthly rolls can fall inside
a ten-session holding window. Without verified expiry histories or a documented
return construction that removes artificial roll jumps, a continuous-price win
fraction is not a validated test of the requested fixed-contract return. Computing
new hashes today also does not establish the missing export provenance.

For a subsequent historical test, freeze the condition before reading outcomes:
gold daily settlement return at least +2%, WTI at most −5%, USD quotes, matched
session dates, five-/ten-session endpoints. This describes the present shock rather
than importing the Dow's twenty-day leadership condition. Use named contracts with
enough remaining life for the full horizon (or a declared, tested roll-return rule),
no forward filling, no nonpositive-denominator percentage returns, and earliest-first
ten-session non-overlapping episodes. Report every eligible episode, mean relative
return, win fraction, uncertainty and regime concentration. This proposed screen
was not run and is not an untouched out-of-sample probability model.

Audit execution: `fp.ps1 doctor` passed; `fp.ps1 python
tmp/commodity_outlook_20261104/audit_inputs.py` exited zero using the checkout's
`tmp/ops-env/Scripts/python.exe` (Python 3.13.2), after equity-note commit `c479fd1`
with existing unrelated working-tree changes. It was a read-only data audit, not
a project test-suite run or a recorded strategy-validation result.

## Prospective falsification

Use **MGCZ2026 and MCLZ2026**, retaining those identities throughout the observation.
November 4 settlement benchmarks are **4,073.0** and **88.12**. Settlement conventions
differ across gold and oil; this is a same-session daily-settlement comparison,
not a synchronized executable entry. CME documents that
[micro gold settlements derive from full-sized gold](https://www.cmegroup.com/education/lessons/micro-gold-and-micro-silver-futures-product-overview)
and [micro WTI uses the corresponding CL settlement](https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/457218849/NYMEX%2BCrude%2BOil).

At session `h`, score relative return in percentage points:

`D(h) = 100 * (MGCZ2026[h] / 4073.0 - MCLZ2026[h] / 88.12)`

- `D(5)` is the interim observation; `D(10)` is the primary endpoint.
- A positive value means gold outperformed; zero or negative fails the hypothesis
  at that endpoint. Do not reset the baseline after an adverse move.
- Track daily settlement ratios and mechanism evidence, keeping the original
  forecast test separate from any later revised thesis. An endpoint win would not
  retroactively justify a 70% probability claim today.
- TradingView lists MCLZ2026 expiry as November 19. A ten-weekday-session observation
  from November 4 reaches November 18 if both contracts have settlements on each
  intervening weekday. Count actual exchange settlement sessions; do not replace
  the December contract with the continuous front month as it rolls.

Early evidence against the mechanism would be renewed oil supply disruption,
continuing inventory draws with stronger near-month backwardation, a rebound in
the dollar or real yields, and gold surrendering its recovery above $4,000. Gold
holding $4,000 alone is not sufficient: it must beat oil's percentage return.
Conversely, verified supply restoration plus weakening oil scarcity and lower real
yields would strengthen the hypothesis, without automatically assigning it 70%.

Scheduled checks: [BLS](https://www.bls.gov/schedule/2026/home.htm) employment November 6,
CPI November 10 and PPI November 13, all 08:30 ET;
[EIA](https://www.eia.gov/petroleum/supply/weekly/schedule.php) November 12 at 12:00 ET
(holiday exception), then the standard November 18 Wednesday release at 10:30 ET.
Geopolitical developments are unscheduled and can dominate this short horizon.
