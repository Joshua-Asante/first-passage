# Q-PATH-TO-PAYOUT-1: The easiest route to a payout, and what it means for strategy and deployment

**Version:** v1, 2026-10-21. Follows Q-PROP-TRADER-METRICS-1. Public sources only. Model code: [prop_payout_geometry_2026-10](../../../lab/analysis/_inbox/prop_payout_geometry_2026-10/) (`payout_sim.py`, `programs.py`, `run_*.py`).

**Objective (Joshua, 2026-10-21):** make the path to a payout as easy as possible.

**Operational definition used here:** maximise P(first payout of **≥ $1,000 net** within **120 trading days**) and minimise expected fees per such payout. Resets and re-buys are allowed.

The $1,000 floor stops "easy" from meaning a $125 payout.

## 0. Answer

1. **Trade the 50K tier, not 100K.**
   - Almost every firm's 50K evaluation is $3K target on a $2K drawdown, a ratio of 1.5. The 100K and 150K tiers are 2.0.
   - Tradeify Select Flex 50K versus 100K: about 1.7× cheaper per payout at every Sharpe.

   | Sharpe | 50K cost per payout | 100K cost per payout |
   |---|---|---|
   | 1.0 | $980 | $1,789 |
   | 2.0 | $535 | $911 |
   | 2.7 | $376 | $613 |

   - Scale by adding 50K accounts once the edge is confirmed live, not by moving up a size.
2. **Program choice matters less than tier and cost.** Among 50K EOD-trailing programs, P(payout ≤ 120d) is about 0.87–0.88 at Sharpe 2 for all of them. Price, resets and payout gates separate them.
3. **Primary: Tradeify Select Flex 50K.**
   - It is a good choice, it is Joshua's current firm, and its rules are verified on Tradeify's own help centre.
   - Its funded side has no consistency rule, no payout buffer, and a $250 minimum payout.
   - **Benchmark: Topstep 50K** (no-activation-fee path), the best-verified alternative. It has slightly higher P at a similar cost and published outcome statistics.
   - **Lucid Flex 50K** is equivalent, but its price is third-party only.
   - **FundedNext Flex 50K** looks cheapest, but the model gives it positive EV at **zero** edge. That means a funded rule I could not verify is missing from the model. Not recommended until its benchmark-day and payout rules are pinned.
4. **Instant funding (Tradeify Lightning, Alpha Direct) is fastest and most certain:**
   - P ≈ 0.97–0.99, about 30 days at Sharpe 2–2.7.
   - It costs about 1.5–2.5× more per payout.
   - Use it only if calendar time matters more than fees.
5. **Strategy shape:**
   - **Size the eval at daily P&L σ ≈ 0.2–0.4 × drawdown**, i.e. about $400–800/day on a 50K.
     - Toward $400: cheapest per payout.
     - Toward $800: fastest and highest P.
     - Low-variance sizing (≈ 0.1 × drawdown) is the costliest route: it rarely busts but is too slow to finish inside the window.
   - **Add a daily profit cap at about 25–35% of the target** (about $750–1,050 on a 50K). It keeps the 40% consistency rule satisfied automatically and is essentially free in the model.
   - **A daily stop does not raise pass odds** with an i.i.d. edge. Keep one only as a gap and fat-tail guard, at ≥ 0.5 × drawdown.
   - **Run the combined book on each account. Do not give each leg its own account.** Cost per payout falls steeply with Sharpe (legs at 1.0 → about $980; book at 2.7 → about $376 at Select Flex 50K).
   - Copying the same book to more accounts multiplies payouts but does not raise the odds of passing, because the accounts are perfectly correlated.
6. **Gate (unchanged from the earlier memo):** everything above assumes the book's live Sharpe after costs is about 2.
   - At Sharpe 1, the 50K route still reaches a first payout about 65–76% of the time, at about $800–1,000 of fees per payout.
   - At zero edge it costs about $1,650–3,000 per payout. Fees fund the payouts; the firm's margin comes from negative-edge buyers.
   - A forward or paper period with costs is the deciding input.

## 1. Rule geometry that drives payout difficulty

All drawdowns below are enforced intraday on net liquidation unless noted.

| Lever | Easiest | Hardest | Notes |
|---|---|---|---|
| Target / drawdown ratio | 1.5 (50K: $3K/$2K, nearly every firm) | 2.0–2.3 (100K/150K; Alpha Advanced $4K/$1.75K) | The biggest single lever |
| Drawdown type | Static, or EOD trailing that locks at start | Intraday trailing (MFFU Rapid funded, TradeDay Quick Pay, Apex intraday) | Intraday trailing taxes winning days |
| Eval consistency | None (Tradeify Growth, MFFU Builder, Alpha Zero) | 20% (instant-funded products); 30% (TradeDay Quick Pay, Earn2Trade) | The 40–55% caps are cheap to satisfy with a daily profit cap |
| Funded payout gate | No buffer, $250 minimum, 5 winning days (Tradeify Select Flex) | Buffer of drawdown + $100 (MFFU, Lucid Pro, Tradeify Daily); profit goal = target (Lightning, Direct) | A buffer roughly doubles the profit needed before the first payout |
| Split | 90–95% | 50% below $4K (TradeDay Quick Pay); 50% below $2.25K (Earn2Trade); 80% (MFFU Pro/Builder, TradeDay Fast Pass) | |
| Pricing | One-time, cheap reset (Tradeify $165/$109; Topstep $95/mo; FundedNext $75/$83) | No reset or rebuy only (MFFU, Apex) | |

**Tradeify specifics** [Tradeify help centre, verified 21 Oct 2026]:
- **Select 50K eval:** $165, reset $109. $3K target, $2K EOD trailing drawdown, 40% consistency, 3-day minimum, max 4 minis.
- **Open conflict:** Tradeify's own pages disagree on whether the eval floor locks at start + $100. The model assumes no lock, the conservative case.
- **Select Flex funded:**
  - $2K EOD trailing drawdown, which locks at start + $100 on reaching +$2,100 or on the first payout request;
  - no daily loss limit and no consistency rule;
  - a payout every 5 winning days of ≥ $150;
  - each payout is 50% of profit, capped at $2,500, minimum $250, split 90/10.
- **Contract scaling:** 2 minis at start, 3 at +$1.5K, 4 at +$2K.
- **Other rules:**
  - >50% of trades and of profit must come from holds of >10 seconds;
  - flat by 4:45pm ET;
  - hedging across own accounts is banned.
- **Elite (live):** eligible after 3 payouts on one account; selection is at Tradeify's discretion.

## 2. Program ranking: 50K, first payout ≥ $1,000 net within 120 trading days

The model takes each program's own rules, a Gaussian i.i.d. edge with intraday Brownian paths, and the best sizing and profit-cap choice per row. **Sharpe 2.0 is the planning case.**

| Program | Max P (fees, median days) | Cheapest $/payout (P) | $/payout at Sharpe 1.0 | $/payout at Sharpe 2.7 | Rule source |
|---|---|---|---|---|---|
| FundedNext Flex 50K | 0.92 ($472, 38d) | $231 (0.63) | $475 | $155 | [F] rules, but model fails the zero-edge check |
| Tradeify Select Flex 50K | 0.88 ($638, 41d) | $535 (0.65) | $980 | $376 | [F] |
| Lucid Flex 50K | 0.88 ($678, 41d) | $531 (0.65) | $1,038 | $342 | [F] rules, [3P] price |
| Topstep 50K (no-activation path) | 0.88 ($566, 40d) | $625 (0.81) | $1,043 | $441 | [F] |
| TradeDay Fast Pass 50K | 0.88 ($590, 43d) | $649 (0.79) | $1,040 | $470 | [F]; 80/20 split |
| Tradeify Growth 50K | 0.82 ($602, 47d) | $573 (0.55) | $1,124 | $375 | [F] + [3P] for funded drawdown |
| Tradeify Select Daily 50K | 0.84 ($696, 47d) | $662 (0.55) | $1,303 | $436 | [F] |
| Alpha Standard 50K | 0.87 ($730, 43d) | $840 (0.87) | $1,355 | $603 | [F] |
| MFFU Pro 50K | 0.87 ($1,343, 43d) | $978 (0.66) | $1,963 | $618 | [F]; no resets |
| MFFU Rapid 50K | 0.81 ($1,164, 48d) | $1,060 (0.52) | $2,317 | $675 | [F]; no resets |
| Tradeify Lightning 50K (instant) | 0.97 ($1,446, 32d) | $884 (0.75) | $1,557 | $693 | [F] |
| Alpha Direct 50K (instant) | 0.98 ($1,498, 33d) | $919 (0.76) | $1,649 | $728 | [F] |
| *Tradeify Select Flex 100K (reference)* | 0.82 ($1,107, 47d) | $911 (0.60) | $1,789 | $613 | [F] |

Not modelled:
- **Apex:** all rules are third-party and it is costly ($249–590 one-time, no resets).
- **Take Profit Trader:** mostly third-party, with an intraday-trailing PRO account.
- **Bulenox:** prices and DLL unknown.
- **Earn2Trade:** 50% split below $2.25K, and the lowest published pass rate (8.89%).

**Published outcome statistics found this round** [F]:

| Firm | Pass | Funded traders paid | Promoted to live | Period |
|---|---|---|---|---|
| MFFU | 19.97% | 39.2% | 4.2% | not stated |
| TradeDay | 36% ("trader pass rate") | — | — | Jan–Jun 2026 |
| Earn2Trade | 8.89% | about 18% had a withdrawal | — | 2025 |

**Calibration check:**
- At zero edge, the model's per-attempt eval pass rate is 20–25%, near the observed 17–20% per account.
- At zero edge, the expected net (first payout minus fees) is negative for every program except FundedNext Flex. That is why FundedNext is flagged.

## 3. Deployment spec (proposed)

1. **Account:** Tradeify Select Flex 50K ($165, reset $109). Before buying, confirm NinjaTrader-native connectivity for the chosen program.
2. **Strategy:** the combined book on one account.
   - Eval sizing: daily P&L σ about $400–600. Go up to about $800 if speed matters more than fees.
   - Hard daily profit cap of $750–1,050, flat for the day after it.
   - Catastrophe stop of ≥ $1,000/day.
   - Flat by 4:45pm ET; no sub-10-second scalps as the majority of trades.
3. **Funded:** same sizing until the drawdown locks at +$2,100, which coincides with roughly the first payout. Request at the first eligible cycle with ≥ $2,222 profit, which gives a $1,000 net payout.
4. **Reset policy:** reset immediately after a bust. Fee budget: 4 attempts (about $490) before a forced review.
5. **Kill and review rule:** judge the edge on trade-level live statistics, not on pass/fail. The number of attempts barely separates Sharpe 0 from Sharpe 2:
   - zero edge passes about 22% of attempts;
   - Sharpe 2 passes about 40%.
6. **Scale-up:** after the first ≥ $1K payout and a live Sharpe estimate of ≥ 1.5, add more 50K accounts running the same book. First verify Tradeify's rules on copy-trading across own accounts.
7. **Benchmark in parallel (optional):** one Topstep 50K. It has the best-verified rules and published statistics, and it diversifies firm risk.

## 4. Caveats
- The model is i.i.d. Gaussian, so it favours high variance more than fat-tailed reality would. Treat the $800/day "max P" sizing as an upper bound.
- First-payout sizes only; long-run funded EV is not modelled here (see the earlier memo).
- **Open items to verify before deployment:**
  - the Tradeify Select eval lock conflict;
  - Tradeify copy-trading and multi-account limits;
  - FundedNext Flex funded rules (benchmark-day threshold, payout fraction);
  - Lucid prices;
  - Topstep's XFA DLL amounts and NinjaTrader availability.
