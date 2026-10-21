# Q-PROP-TRADER-METRICS-1: What successful prop-firm futures traders look like, and whether "≥95% single-attempt pass" is the right objective

**Version:** v1, 2026-10-21. Desk research only: public sources, no outreach, no spend. Successor: [Q-PATH-TO-PAYOUT-1](2026-10-21-q-path-to-payout-1-memo.md).

**Labels.** Every figure carries one of these:
- **[FP]** firm-published, verified on the firm's own page;
- **[FP-r]** firm-attributed but relayed by a third party;
- **[3P]** third-party data, journalism or academic work;
- **[A/M]** anecdotal or marketing;
- **[INF]** my inference or model output.

---

## 0. Top findings

1. **Account-level pass rates are about what a zero-edge trader gets. They measure the rule geometry, not skill.**
   - Tradeify [FP]: 17.2% of evaluation accounts completed (Growth, Advanced and Select, Aug 2025 to Jul 2026).
   - Topstep [FP]: 16.8% of Combines completed (2025).
   - My Monte Carlo of Tradeify Select 100K [INF]: a zero-edge trader at aggressive size passes about 16–17% of single attempts. That matches the observed figures.
   - The academic work supports the same reading.
     - Lim (SSRN 2026) [3P]: a zero-edge trader passes about 30% of standard 2-step attempts.
     - Youngblood (SSRN) [3P]: a no-edge NQ strategy has positive mean P&L per Topstep account.
   - So the population passes at roughly a coin-flip rate. "Pass rate" is not a metric that separates successful traders.
2. **About 1 buyer in 6 to 9 ever gets a first payout. Roughly 0.4–1.2% of individuals reach live capital.**
   - Per individual [FP × FP → INF]:
     - Tradeify: about 40.3% × 28.5% ≈ 11.5% reach a first payout. About 1.2% are called to live.
     - Topstep: about 51.8% × 33.3% ≈ 17% reach a first payout. About 0.4% are called to live.
   - Per account, it is much lower.
     - FPFX dataset, 10 firms, about 300k accounts [3P]: about 6–7% of accounts reached a payout. The average payout was about 4% of plan size.
     - The Funded Trader [3P, CEO statement]: 1–2% of clients reached a payout.
   - No firm publishes repeated-payout survival.
   - "Live" is a firm-policy gate with a skill floor underneath it. It is not a skill measure.
3. **No population-level metric profile of successful prop traders exists in public.**
   - What exists is selected case studies (FTMO [A/M]: win rates of 34–52%, average R of about 2.5–4) and unsourced "risk 0.5–1% per trade" advice.
   - The only rigorous base rates are academic, on retail day traders.
     - Brazil futures (Chague et al.) [3P]: 97% of persistent day traders lose money.
     - Taiwan (Barber et al.) [3P]: fewer than 3% are predictably profitable.
   - These match the 0.4–1.2% "live" shares.
   - Successful prop traders are a survivor-selected tail. Their published metrics are both survivor-biased and marketing-filtered.
4. **No firm targets "≥95% single-attempt pass", and no surviving trader shows it. The objective is unusually strict.**
   - The evidence implies successful traders get funded through repeated attempts. Tradeify's median buyer bought 3 evaluations [FP].
   - Their pass-within-a-window probability is high because of resets, not because each attempt is near-certain.
   - Under the same model [INF], the existing book (Sharpe about 2.7) gives:
     - ~79–80% pass per single attempt (bust about 10–17%), which is consistent with the hold;
     - **~96% pass within 200 trading days with resets allowed**;
     - expected fees of about $330 at Tradeify's $265 price and $169 reset; 95th-percentile spend about $600.
5. **On an expected-value-per-fee basis, the model clears break-even well below the current Sharpe floor.**
   - The objective that matters to the firm, and to every trader who gets paid, is net cash: payouts minus fees.
   - Model EV per $265 attempt [INF, payout rules simplified, haircut discussed in §3]:
     - Sharpe 0: about $0;
     - Sharpe 1.0: about +$300 to +$850;
     - Sharpe 2.7: about +$3k to +$5.7k.
   - The binding question is whether live Sharpe survives costs and regime change. It is not whether the single-attempt pass rate reaches 95%.

## 0.1 Objective options for Joshua

| # | Objective | Hard requirement | Status of the current book (model) [INF] |
|---|---|---|---|
| A | **Keep:** P(pass in 1 attempt ≤200d) ≥ 95% and bust < 5% | Sharpe ≈ 3.5+ (trailing barrier, 40% consistency rule, intraday enforcement) | Not met. About 79% pass and 10% bust at S=2.7. Hold remains correct under A. |
| B | **Pass within the window, resets allowed:** P(funded within 200d) ≥ 95%, with a spend cap (e.g. E[fees] ≤ $500 and P95 ≤ 4 attempts) | Sharpe ≈ 2.5–2.7 at about $300–400 daily σ. Zero edge can also hit 95% by gambling, so B **must** be paired with C or D. | Met at S=2.7 (σ $400/day): 95.7%, E[fees] about $331. Not met at S=2.0: about 87%. |
| C | **EV per fee:** E[net payouts over 12 months] − E[fees] > 0, with a margin (e.g. ≥ 3× fees) | Live Sharpe ≳ 1 after costs; a margin of ≥ 3× fees needs about 1.5–2 | Met with a wide margin if the live Sharpe is ≥ 1.5. The risk is live degradation, not the threshold. |
| D | **Pass × payout survival:** P(≥ k payouts within N months per funded account), e.g. P(≥ 5 payouts in 12 months) ≥ 50% | Sharpe ≈ 1–2 with small funded sizing (σ ≈ $250/day), under the simplified Select Flex rules | Model about 86% at S=2.7. Payout rules need primary-source pinning before this is trusted. |
| E | **Easier geometry** (target/drawdown < 2, static or locking drawdown, no consistency rule) | The Sharpe floor falls roughly in proportion to the target/drawdown ratio | Not evaluated here. Needs a firm-rule survey (Q-follow-up). |

**My recommendation [INF].** Replace A with **B + C as joint gates, with D as the funded-phase health metric.**
- B on its own is gameable: zero edge reaches 95% with resets.
- C on its own ignores the time to first cash.
- A is stricter than anything firms or survivors are measured on. It also forbids resets, which is the main thing successful traders use.
- Before un-holding, the open item is a **live/forward Sharpe estimate with costs**. If the book delivers ≥ 2 live, B+C+D are comfortably met.

---

## 1. Firm-published and other outcome statistics

### 1.1 Primary firm disclosures (verified on firm pages)

**Tradeify** [FP]. Source: tradeify.co/forge, "Trader Performance Statistics (August 2025 – July 2026, calculated as of 9 August 2026)", covering the Growth, Advanced and Select evaluation products.
- (a) **17.2% of evaluation *accounts* initiated** were completed and "afforded the opportunity to advance to the Funded Level".
  - Denominator: evaluation accounts.
  - Resets are counted as purchases per (b), so it is effectively per attempt.
- (b) **40.3% of *individual participants* who initiated one or more evaluations** advanced to the Funded Level in at least one evaluation.
  - Participants "initiated a median of 3 [evaluations and resets] each over the period".
- (c) **28.5% of *individual participants at the Funded Level*** received a payout.
  - The Funded Level includes Funded (sim) and Live Funded accounts.
- (d) **3.0% of *individual participants trading in a Funded Account*** were called up to a Live Funded Account.
- Not stated:
  - whether (c) counts people funded before August 2025;
  - payout counts or sizes;
  - survival time;
  - a definition of "Live Funded" on that page.

**Topstep** [FP]. Source: topstep.com/our-program, "2025 Trader Performance Statistics", January–December 2025.
- (a) **16.8% of all Trading Combines initiated** were completed. Denominator: Combines.
- (b) **51.8% of individual participants** who entered ≥ 1 Combine reached the Funded Level in at least one.
- (c) **33.3% of all individual participants at the Funded Level** received a payout. The Funded Level is Express plus Live.
- (d) **0.71% of individual participants trading in an Express Funded Account** were called up to a Live Funded Account.
- The disclosure notes that the statistics "reflect both simulated and live trading".
- The PM's leads match on all four. The 0.71% denominator is **XFA individuals**, not "all traders who started". Several third-party sites misstate this, e.g. tradecovex.

**Apex Trader Funding** [FP-r]: "The customer pass rate of the evaluation program was 43.13% between January 1, 2023 – Sept 1, 2023".
- This is the disclaimer in an Apex press release syndicated via NewsDirect, Feb 2024.
- It is a per-customer rate, comparable to Tradeify (b) and Topstep (b). It is three years old and comes from a different rule era.
- Apex also reports cumulative payouts: >$100M by Feb 2024 [FP-r], and >$660M per a third-party 2026 review [3P]. These totals cannot be turned into rates.

**FTMO.**
- No aggregate pass or payout statistics were found. Confirmed: only "Successful Traders Stories" case studies, which are [A/M].
- Financials [3P]:
  - 2023 revenue $203.9M (TradeInformer, citing the financial statements);
  - the FTMO awards page says >$75M was paid to traders in 2023, about 35% of turnover [INF arithmetic];
  - cumulative payouts >$450M by Sep 2025, and about $200M in a trailing 12 months, per Finance Magnates.
- These are useful for the firm's economics, not for trader metrics.

**Lucid.**
- No firm-published statistics were found.
- The PM's lead "18% of funded traders paid" could not be traced to a primary source. Treat it as **unverified, do not use**.
- Only aggregator payout anecdotes exist [A/M]: e.g. an average payout of about $1,025 on a $25–100K account.

**FundedNext, FXIFY, The5%ers, E8.**
- No current firm pass or payout disclosures were found.
- E8: a pass rate of 17.7% (Jan 2023–Mar 2024) is cited by TradeInformer [FP-r/3P, original not located].
- Fintokei: 23% (2024) [3P].
- FundedNext and The5%ers appear only in on-chain payout-volume rankings from Finance Magnates DataLab [3P]. Those rankings cannot separate trader payouts from other outflows.

### 1.2 Cross-firm datasets and journalism

**FPFX Tech** [3P]. Source: Finance Magnates, D. Chmiel, 18 Sep 2024, "Exclusive: Only 7% of 300,000 prop trading accounts achieved payouts". Justin Hertzberg (CEO) is quoted.
- Sample: >300,000 accounts, 100,000 traders and 10 unnamed firms (mostly CFD/FX, on FPFX's back office).
- "14% of traders passed the challenge and obtained a funded account".
- About 45% of those achieved a payout, "7% of all traders". The arithmetic gives 6.3%.
- Average payout: **4% of plan size**. It is ambiguous whether that is per payout or per trader in total.
- About 3 challenges per account, about $800 spend per trader, and 2.2 firms per trader.
- **Caveats:**
  - The article mixes "traders" and "accounts" as denominators.
  - It is unaudited vendor data with unnamed firms.
  - It is FX/CFD-heavy, not futures.

**The Funded Trader** [3P relaying CEO]. Source: Finance Magnates, 18 Mar 2025.
- A 5–10% challenge pass rate.
- About 20% of funded traders received a payout.
- A 1–2% overall chance of a payout.
- **Caveat:** The source is a distressed firm (payout backlog, settlements) speaking to clients. Its incentives cut both ways.

**PipFarm survey** [3P/A-M]: 450 respondents; 41% reached the payout stage. It is self-selected and from one firm, so it is not comparable.

### 1.3 Regulator material

**CFTC v. Traders Global Group (My Forex Funds), filed Aug 2023.**
- The complaint alleged that the firm was mainly a simulated-trading platform and that its rules were designed to stop traders qualifying.
- The case was **dismissed with prejudice on 13 May 2025**. The CFTC was sanctioned (Rule 11, >$3M in fees) over evidence misconduct [3P: Finance Magnates, TradeInformer].
- **No ruling on the merits.**
- The legal status of "evaluation fee for a sim profit-share" (is it a commodity-pool interest?) remains open [3P commentary].
- No CFTC or NFA rulemaking or statistics on prop-firm outcomes were found.

**Relevance:** Payouts at most futures firms come from **simulated** accounts and are funded largely by evaluation fees. Topstep's disclosure says its statistics mix sim and live, and "Live" is a small, firm-curated tier. That makes "live" a firm-capacity and policy outcome (§1.5).

### 1.4 Academic work

**Lim, "The Price of a Funded Account: An Actuarial Analysis of Proprietary Trading Firm Challenges"** (SSRN 7178078, July 2026) [3P, from the abstract only; full text was 403].
- It prices a 2-step challenge as a contingent claim.
- A zero-edge trader's pass rate falls from 0.50 to **0.30** once the time limit is added.
- It implies about a 56% gross margin for the firm under an illustrative population.
- It proposes standard disclosure: a cohort funnel and a payout ratio.

**Youngblood, "The Inherent Value of Retail Prop Firms for Fixed-Size Trading Strategies"** (SSRN 7514219) [3P, abstract only].
- A no-edge fixed-size NQ strategy has **positive mean net P&L per account** under the Topstep framework.
- But 39.7% of simulations lost money, and the result was unstable across subperiods.
- The finding: the contract's convexity (capped loss = fee, uncapped payout) gives zero-edge traders option value.

**Chague, De-Losso & Giovannetti, "Day Trading for a Living?"** (FGV EESP WP 525, 2020) [3P].
- The sample is Brazilian mini-index futures day traders who persisted ≥ 300 days.
- 97% lost money. About 0.4–0.5% earned more than a bank teller's wage.
- There was no evidence of learning.

**Barber, Lee, Liu, Odean & Zhang** (2018 version, Taiwan) [3P].
- **Fewer than 3% of day traders** are predictably profitable after costs.
- 97% can expect to lose.

### 1.5 PM's explicit question: what share of eval buyers reach each stage?

The denominators do not nest perfectly, so all products below are [INF]. The Funded-Level population can include people funded before the window opened.

| Stage | Individuals: Tradeify (Aug 25–Jul 26) | Individuals: Topstep (2025) | Accounts: Tradeify / Topstep | Accounts: cross-firm |
|---|---|---|---|---|
| Funded at least once | 40.3% [FP] | 51.8% [FP] | 17.2% / 16.8% [FP] | 14% (FPFX) [3P]; 5–10% (TFT) [3P] |
| (i) First payout | ≈ 11.5% (40.3% × 28.5%) | ≈ 17.2% (51.8% × 33.3%) | Not published. ≈ 3–4% per account if buyers average about 3–4 accounts [INF, weak] | ≈ 6–7% (FPFX) [3P]; 1–2% (TFT) [3P] |
| (ii) Repeated payouts over months | **Not published.** Proxy: Elite live requires 5 approved payouts [3P on the rule] and 3.0% of funded individuals were promoted. So ≥ 5 payouts ≥ about 1.2% of buyers; the true share is plausibly about 2–5% [INF]. | **Not published.** Live is "usually" after about 5 XFA payouts and discretionary [3P], so a ≥ 0.4% floor; plausibly about 1–4% [INF]. | Not published | Not published |
| (iii) Live | ≈ 1.2% (40.3% × 3.0%) | ≈ 0.37% (51.8% × 0.71%) | n/a | n/a |

**What "promoted to live" means.**
- **Topstep Live Funded Account.** Real capital, called up at the Risk Team's discretion.
  - Third-party sources say "usually" after about 5 XFA payouts, with a scaled balance up to $150K.
  - Third-party sources also cite a reserve/tradeable split (e.g. 20% tradeable, 80% reserve). I could not confirm this on primary pages.
- **Tradeify Elite / Live Funded.**
  - Per third parties: it requires 5 approved payouts across any accounts, then **manual selection**.
  - The transition is mandatory and terminates all sim accounts.
  - The drawdown is locked.
  - The Forge page does not define the term.

**Skill or policy?** **Mostly policy, with a skill floor.**
- Eligibility (about 5 payouts) needs sustained positive performance. That part is skill-correlated.
- The call-up itself is discretionary. It depends on the firm's real-capital appetite, hedging, jurisdiction and capacity.
  - Example: one Trustpilot reviewer reports funded accounts closed because they could not go live from Canada [A/M].
  - Promotion also removes the trader's sim accounts and payout optionality, which a firm can use to manage payout liability.
- Low live rates therefore understate the skilled share. A better skill proxy would be "≥ k payouts within N months", which no firm publishes.

---

## 2. Metric profile of successful traders: what is actually known

**Bottom line:** no firm, regulator or academic source publishes a population-level profile of funded traders who keep getting paid (win rate, profit factor, daily P&L distribution, Sharpe, and so on). Everything below is weak evidence.

| Metric | Best available evidence | Label | Bias |
|---|---|---|---|
| Win rate / average R | FTMO case studies: WR 51.5% at R 2.63; 34.0% at R 2.45; 34.8% at R 4.05; a gold scalper at 40% WR and R 2.59. Third-party claim of a "22.7–80%" range across FTMO traders. | [A/M]; [3P, unverified] | Hand-picked winners. Survivorship and marketing bias. CFD/FX, not futures. |
| Profit factor | Not published anywhere. Implied by the case studies: WR 35–50% × R 2.5–4 → PF about 1.3–2.6. | [INF from A/M] | As above |
| Daily P&L distribution / best-day share | Not published. Firms impose consistency caps instead (Tradeify Select eval 40%; Topstep 40–55% variants), which tells you firms see payouts concentrated in a few days. | [FP rule] / [INF] | — |
| Drawdown use / risk per trade | Repeated advice: 0.5–1% of balance per trade for those who stay funded, versus 2–3% for failures. A "177k-trader study" (R 2–2.5, winners held twice as long) **could not be traced and is likely apocryphal**. | [A/M] | No dataset or methodology |
| Trade frequency / holding time | A "3.2 vs 6.8 trades/day passers vs failers" claim with no source. Tradeify funded rule: >50% of trades and profit must come from holds >10s (anti-microscalping). No overnight holds at Tradeify. | [A/M]; [FP rule] | — |
| Instruments | FTMO case studies: gold, NAS100, BTC. Futures firms: NQ/ES/MNQ dominant (common knowledge, not a published share). | [A/M] | — |
| Attempts before funding | Tradeify median 3 evaluations plus resets per participant. FPFX: about 3 challenges, about $800 spend. Topstep: 51.8% per person versus 16.8% per Combine, which implies about 3 Combines per person. | [FP]; [3P]; [INF] | Includes non-passers |
| Sharpe or proxy | Not published anywhere. | — | — |

**Implied profile [INF].** Use with care.
- About 1–3% of eval buyers become repeat earners.
- The academic base rate of persistent retail profitability is about 1–3%.
- These coincide, which suggests that prop "successes" are mostly the same small skilled tail plus a lucky fringe. The lucky fringe is large at the first-payout stage and shrinks with each payout.
- Under my model (§3), traders who reach ≥ 5 payouts at small sizing are consistent with **annualised Sharpe of about 1–2**, not 3+.
  - Repeated attempts and the sim-payout convexity do the rest.
  - This holds under the simplified payout rules.
- Nobody in the observed population is doing what objective A asks.

---

## 3. Implications for Tradeify Select 100K

### 3.1 Model

Rules and assumptions [INF; code in [the camp](../../../lab/analysis/_inbox/prop_payout_geometry_2026-10/): `eval_barrier_sim.py`, `run_funded_sweep.py`, `run_resets.py`]:
- daily P&L i.i.d. Gaussian, with 13 intraday sub-steps for net-liquidation enforcement;
- end-of-day trailing $3K drawdown, no lock in the eval, breach checked intraday;
- $6K target, 40% best-day consistency, 3-day minimum, 200-day horizon;
- price $265 and reset $169, no activation fee [FP, Tradeify pricing reference];
- no costs beyond those in the Sharpe; no regime change; no fat tails.

**Single attempt, best daily σ per Sharpe:**

| Annualised Sharpe | Best σ/day | P(pass) | P(bust) | Median days to pass |
|---|---|---|---|---|
| 0 | ~$1,000 | 0.16–0.17 | 0.83 | 16 |
| 0.7 | $400 | 0.28 | 0.71 | 77 |
| 1.0 | $300–400 | 0.34–0.35 | 0.55–0.66 | 76–118 |
| 2.0 | $300 | 0.63 | 0.30 | 106 |
| 2.7 (current book) | $250–300 | 0.79–0.80 | 0.10–0.17 | 93–116 |
| 3.5 | $250 | 0.93 | 0.04 | 99 |

**Checks against the outside numbers:**
- The zero-edge row reproduces the observed account-level pass rates (Tradeify 17.2%, Topstep 16.8%).
- The S=3.5 row lands just under 95%. That is consistent with the earlier closed-form bound of 2.8–3.5: this sim adds the consistency rule and intraday enforcement, so it should be slightly stricter.

**Resets allowed within 200 trading days:**

| Sharpe | σ/day | P(funded ≤ 200d) | Mean attempts | P95 attempts | E[fees] |
|---|---|---|---|---|---|
| 0 | $1,000 | 0.95 | 5.9 | 16 | ~$1,090 |
| 1.0 | $600 | 0.87 | 3.2 | 8 | ~$640 |
| 2.0 | $400 | 0.88 | 1.7 | 4 | ~$380 |
| 2.7 | $400 | **0.96** | 1.4 | 3 | **~$330** |
| 2.7 | $600 | 0.99 | 1.8 | 4 | ~$400 |

**Funded phase, Select Flex as simplified.** These assumptions are **unverified on primary pages** [3P rules]:
- the floor locks at start + $100;
- a payout every 5 positive days;
- each payout is 50% of profit, capped at $4K, with a $500 minimum;
- 90% split;
- 250-day horizon.

At σ ≈ $250/day:

| Sharpe | P(≥ 1 payout) | P(≥ 5 payouts) | Mean net paid |
|---|---|---|---|
| 0 | 0.69 | 0.24 | ~$1.6K |
| 1.0 | 0.86 | 0.51 | ~$3.2K |
| 2.0 | 0.95 | 0.76 | ~$5.5K |
| 2.7 | 0.98 | 0.86 | ~$7.5K |

**Calibration warning.** The zero-edge P(≥ 1 payout) of 0.69 is far above Tradeify's observed 28.5% of funded individuals.
- So either the real payout gates are stricter (winning-day minimums, buffers, the micro-scalp rule, the Daily option's $2.6K buffer), or the population is negative-edge and oversized. Most likely both.
- Treat the funded payouts as **upper bounds**. Apply a haircut of about 50% for planning.

**EV per $265 attempt** [INF] = P(pass) × E[funded net] − fee:

| Sharpe | Unhaircut | Haircut |
|---|---|---|
| 0 | ≈ $0 | — |
| 1.0 | ≈ +$850 | ≈ +$300 |
| 2.7 | ≈ +$5.7K | ≈ +$2.7K |

The zero-edge break-even is consistent with firm economics: fees fund the sim payouts, and the firm's margin comes from negative-edge and oversized buyers.

### 3.2 How the reference book compares
- **Individual legs (Sharpe 0.7–2.0).**
  - Each leg alone beats the typical eval buyer by a wide margin. The buyer population is about zero edge; the legs pass about 28–63% of single attempts versus about 17%.
  - Each leg plausibly meets objective C if its live Sharpe holds.
- **Combined book (2.7).**
  - It sits above the implied Sharpe of successful traders as far as that can be inferred (about 1–2).
  - It fails only objective A.
- **The 2.8–3.5 bound** is correct for what it measures: single attempt, no resets, bust < 5%. What it measures is the objective, not the market: no successful population is held to it.

### 3.3 What each objective would require
- **A (keep).** A Sharpe ≈ 3.5 live book, or easier geometry (E). Under A, the hold stays.
- **B + C (recommended).**
  - A pre-registered forward or paper period showing live Sharpe ≥ about 2 after commissions and slippage. At about 2.0, use σ ≈ $400/day; at about 2.7, σ ≈ $250–400/day.
  - A fee budget: e.g. ≤ 4 attempts, about $770 at $265 + 3 × $169.
  - A kill rule: stop if live Sharpe after N attempts is inconsistent with ≥ 1.
- **D.**
  - Pin the actual Select Flex/Daily payout rules from Tradeify's help centre first: winning-day threshold, buffer, lock level, cap.
  - Then re-run the funded model.
  - Funded-phase sizing should be smaller than eval sizing.
- **E.** A separate rule-survey task across firms: target/drawdown ratio, static versus trailing drawdown, consistency rules.

---

## 4. Biases and limits
- **Survivorship and marketing.**
  - All "successful trader" metrics are hand-picked case studies (FTMO) or affiliate-site content.
  - Payout totals are firm marketing.
  - On-chain trackers cannot separate payouts from other outflows.
- **Firm disclosures** are self-reported and unaudited. Topstep's and Tradeify's appear modelled on the same template, possibly for regulatory-defensive reasons. Their denominators differ in each line, so products across lines are approximate.
- **FPFX and TFT** are FX/CFD-heavy and unaudited. TFT spoke while in distress.
- **The model** assumes Gaussian i.i.d. returns and simplified payout rules. Fat tails and regime change would lower the high-Sharpe rows. The live-versus-backtest Sharpe haircut is the dominant real-world uncertainty and is not modelled.
- **Not verified:**
  - the Lucid "18%" figure (no primary source found);
  - the "177k-trader study";
  - Topstep's reserve split;
  - Tradeify Elite mechanics (third-party only).
- **Not found:** any CFTC/NFA statistics, or any audited cross-firm dataset.

## 5. Sources
- Tradeify, Forge page, "Trader Performance Statistics": https://tradeify.co/forge [FP]
- Tradeify, pricing reference: https://intercom.help/tradeify/en/articles/14369021-tradeify-pricing-reference [FP]
- Tradeify, essential trading rules: https://intercom.help/tradeify/en/articles/12268167-essential-trading-rules-overview [FP]
- Topstep, 2025 Trader Performance Statistics: https://www.topstep.com/our-program [FP]
- Apex, 43.13% disclaimer, via the Feb 2024 press release: https://markets.financialcontent.com/wral/article/newsdirect-2024-2-15-apex-trader-funding-crosses-100-million-paid-to-its-traders [FP-r]
- Finance Magnates, FPFX 300k accounts (18 Sep 2024): https://www.financemagnates.com/forex/exclusive-only-7-of-300000-prop-trading-accounts-achieved-payouts/ [3P]
- Finance Magnates, The Funded Trader (18 Mar 2025): https://www.financemagnates.com/forex/only-1-in-20-traders-pass-prop-firm-challenges-reports-the-funded-trader/ [3P]
- TradeInformer, FTMO finances: https://www.tradeinformer.com/prop-weekly/what-ftmo-tells-us-about-prop-firm-finances [3P]
- Finance Magnates, FTMO $450M: https://www.financemagnates.com/forex/ftmo-announces-over-450-million-paid-out-as-prop-trading-firm-turns-10/ [3P]
- Finance Magnates, MFF case: https://financemagnates.com/forex/mff-case-misconduct-embarrassment-for-the-cftc-but-not-yet-a-win-for-prop-trading [3P]
- Lim (SSRN 7178078): https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7178078 [3P]
- Youngblood (SSRN 7514219): https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7514219 [3P]
- Chague, De-Losso & Giovannetti (2020): https://repositorio.fgv.br/items/e87d04fc-4b4c-4a56-ab5a-1c84c1afde1b/full [3P]
- Barber et al. (2018): https://faculty.haas.berkeley.edu/odean/papers/day%20traders/Day%20Trading%20Skill%20110523.pdf [3P]
- FTMO case studies, e.g. https://ftmo.com/en/a-high-win-rate-is-the-foundation-of-success/ [A/M]
