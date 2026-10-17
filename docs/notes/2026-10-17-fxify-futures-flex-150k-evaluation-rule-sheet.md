# FXIFY Futures Flex 150K — evaluation-stage rule sheet (2026-10-17)

**Scope:** Flex plan, $150,000 size, **evaluation stage** only (the tier named in the [four-firm addendum 2026-10-16 §3](../adr/2026-07-12-prop-portfolio-four-friendly-firms.md#addendum-2026-10-16--operator-rulings-50-ceiling-fresh-4-candidate-orb-mnq-v7-fxify-futures-flex-registration-accepted)). Funded-stage and Direct rules appear only where they explain a contradiction.
**Purpose:** the dated primary-source re-read that the addendum's condition (c) asks for, ahead of the 2026-10-23 pre-registration freeze. It changes no firm_rules row. Conditions (a) row and (b) pre-flight stay with their owners.
**Sources, read 2026-10-17:**
- fxifyfutures.com FAQ pages, every one stamped "Updated on September 28, 2026". The site blocks scripted fetches (Cloudflare), so these were read through a rendering fetch that returns quoted extracts. They are a primary source, but not checked byte-for-byte.
- FXIFY Futures General Terms and Conditions (GTC), PDF served at `fxifyfutures.com/terms-and-conditions/`, footer date December 6, 2024, sha256 `c25d2fa8…abfc72f`. Text was extracted locally with `pdftotext` and quoted from that extract.
- FAQ slugs are cited as `faq:<slug>`.

Labels: **V** = verified at the source today. **V-scope?** = verified, but the source does not say which stage it applies to. **U** = not stated anywhere read.

## 1. Risk limits

| Rule | Value | Status | Source |
|---|---|---|---|
| Fee | $449 one-time | V | faq:flex-plan-overview |
| Profit target | $9,000 (6%), "achieve and maintain" | V | faq:how-does-the-fxify-futures-evaluation-process-work |
| Maximum Loss Limit (MLL) | $4,500 (3.0%), EOD trailing; see §2 | V | faq:what-is-the-maximum-loss-limit-mll |
| Daily Loss Limit (DLL) | $3,000 (2%) from the day's starting balance; **soft**: read-only for the rest of the trading day, "not a hard breach" | V | faq:what-is-the-daily-loss-limit |
| DLL realized or unrealized | — | U | |
| Max position | 10 minis / 100 micros, counted on open contracts. Micros count 1:10 (MBT/MET 1:1, SIL 1:5). Working orders, stage scaling and the over-cap consequence are not stated | V / U | faq:what-is-the-max-position-limit |
| Time limit | 30 days, extendable for a fee; the consequence of expiry is not stated | V / U | faq:what-is-the-time-limit-to-complete-the-evaluation |
| Minimum trading days | "No minimum", but consistency "naturally requires" at least 2 days. A trading day is any day with at least one trade opened and closed | V | faq:what-is-the-minimum-trading-days-requirement |
| Inactivity | At least 1 trade every 14 calendar days, then a 7-day grace period; after that the account is "permanently closed" (evaluation and funded) | V | faq:what-is-fxify-futures-inactivity-policy |
| Price-limit rule | No trading when a product is within 2% of a CME price limit | V | faq:what-is-fxify-futures-price-limit-trading-policy |
| Add-ons (checkout only, each 15% of the fee; all three as a bundle for 35%) | Remove the DLL; MLL +$250; split raised to 100% | V | faq:how-do-fxify-futures-add-ons-work |
| Reset | $209, allowed any time after a breach | V | faq:flex-plan-overview, evaluation-process FAQ |
| Commissions and fees | — | U | |

## 2. Drawdown mechanics

- **Threshold:** the MLL trails the **highest end-of-day balance**: floor = EOD peak − $4,500. It never moves down. Initial floor $145,500. (V, faq:what-is-the-maximum-loss-limit-mll)
- **Lock:** "Once your account profit equals your initial drawdown cushion … the trailing threshold locks permanently at your starting account balance". The page adds that it also locks "whenever a payout request is processed". At 150K: EOD balance ≥ $154,500 locks the floor at **$150,000**, which in `firm_rules` terms is `trailing_locking` with `dd_lock_offset_usd = 0`. (**V-scope?**)
- **Breach:** "If your account balance falls to or below your Maximum Loss Limit threshold, all open positions will be closed, and the account will be deactivated." The source does not say whether the check runs intraday or at end of day, or whether it uses balance or equity. (U)

## 3. Consistency

- Evaluation: "Trading returns from any single trading day cannot exceed 50% of the total returns made during the evaluation phase." Exceeding this is **not a failure**: you keep trading until the best day is at or below 50% of total profit. Funded is 40%; Direct is 25%. (V, faq:what-are-fxify-futures-consistency-rules)
- Model it as a soft pass gate (`consistency_rule_pct: 50.0`), the same class as the MFFU Rapid evaluation.

## 4. Session boundaries

- The trading day runs 6 PM to 5 PM "EST". Markets are closed from Friday 5 PM to Sunday 6 PM. (V, faq:what-are-the-trading-hours-at-fxify-futures)
- "All trades must be closed by 4:59 PM" each day; otherwise "our system will automatically do it for you". The source does not say whether the auto-close counts as a violation. (V / U)
- No overnight or weekend holds (`weekend_holds: False`). No holiday-session rule is stated. (U)

## 5. Automation restrictions

- **Permission:** "the use of Expert Advisors (EAs) and automated trading scripts is permitted on both Flex and Direct accounts … enabled by default across all account types … across supported platforms, including NinjaTrader, Tradovate, and TradingView". (V, faq:can-i-use-eas-expert-advisors-to-trade)
- **Supported platforms:** Tradovate, TradingView via Tradovate, and NinjaTrader. No page addresses API access, bridges (CrossTrade and similar), webhooks, or VPS/cloud hosting. (V / U, faq:trading-platforms-overview, faq:what-are-fxify-futures-ip-rules)
- **EA-specific prohibitions, with "immediate account breach and deactivation":** latency arbitrage, micro-scalping, exploiting glitches, **news trading**. (V)
- **Copy trading** is permitted between accounts owned by the same person, including from a personal account or another prop firm's account. Copying from "third-party traders, signal providers, or automated signal services" is a breach. (V, faq:does-fxify-futures-allow-copy-trading)
- **GTC 5.4.1.5(e)** prohibits using "any software, artificial intelligence, ultra-high speed, or mass data entry which might manipulate, abuse, or give you an unfair advantage". **GTC 5.4.2** requires personal use only, with no third party trading the account. (V)
- **Scalping:** the prohibited-strategies FAQ defines tick or micro scalping as "fewer than 10 ticks". The micro-scalping FAQ defines it as holds of "seconds to under 1 minute" with profits "typically less than 3 points". (V)
- **Also prohibited:** an "all or nothing" approach ("relying on loss limits as a stop-loss strategy"); opposite positions across accounts (FAQ, and GTC 5.4.1.4, which covers connected accounts and other FXIFY entities); high-leverage news trading. (V, faq:what-trading-strategies-are-prohibited)

## 6. Feed rights

- **Platform data:** Level 1 is free on the platform. Level 2 costs $39 a month. No page names the data provider, sets professional or non-professional status, or states permitted uses. Exchanges offered: CME, CBOT, NYMEX, COMEX; no product list. (V / U, faq:what-is-the-difference-between-level-1-and-level-2-data, faq:what-products-can-i-trade)
- **GTC 5.4.1.2:** prohibited to "perform trades using an external or slow data feed". "External" is undefined. (V)
- **GTC 9.6.5 / 9.6.6:** no use of the Services or Content "otherwise than as permitted", and no "automated means to view, display or collect information available through the Website or Services". (V)
- **GTC 5.9** disclaims liability when platform data is used for real trading elsewhere, so it contemplates that use rather than banning it. (V)
- The CME licence position for an agent consuming the data stays with [CME non-display research](2026-10-10-cme-non-display-licensing-research.md). Repo feed status: Databento retired, no replacement approved (AGENTS.md). A new execution feed needs the [feed-equivalence pre-flight](../spec/feed_equivalence_discovery_test_LOCKED.md).

## 7. Contradictions that affect modelling or execution

| # | Conflict | Affects | Conservative reading until FXIFY answers in writing |
|---|---|---|---|
| C1 | The MLL lock text has no stage scope, and its payout-request trigger is a funded-only event. This repo has twice encoded a funded lock into evaluation rows (Tradeify, MFFU; [2026-08-04 fix](../adr/2026-08-04-firm-rules-eval-lock-fix-applied.md)). The $9,000 target sits above the $4,500 cushion, so the lock is reachable before a pass and the choice changes bust rates | Modelling | Primary row: **no evaluation lock** (`dd_lock_offset_usd: 1_000_000.0`, the house idiom). Run the $0 lock as a sensitivity. Add the stage-scope question to the venue note's FXIFY Q7 |
| C2 | News trading: the news FAQ says "news trading is allowed"; the EA FAQ lists "news trading" as an immediate breach for EAs; the prohibited-strategies FAQ bars only *high-leverage* news trading; GTC 5.4.1.6 bars "gap trading by opening trade(s)" when major events "are scheduled", and/or 2 h or less before a market closes for 2 h or more. The clause joins its limbs with "AND … OR", so it reads either way. No window length is given anywhere | Execution (automated entries); modelling (event-day exclusion) | For an automated strategy, treat **no new entries around scheduled high-impact releases** as binding; the window is undefined. Under the disjunctive GTC reading, there are no new entries after 15:00 ET before a weekend or holiday close. The model sets `news_trading: False`. A deterministic event filter is needed before any run that claims compliance. The venue note's Q6 covers this |
| C3 | Breach clock: the threshold updates on the EOD peak, but the breach is tested on "account balance" with no time stated | Modelling | Intraday-honest clock (house convention since 2026-10-02): breach on intraday equity against the EOD-set floor |
| C4 | The FAQ grants automation on "supported platforms" without mentioning off-platform logic. GTC 5.4.1.5(e) bars software that "might … give you an unfair advantage", and 9.6.6 bars "automated means to … collect information" from the Services | Execution route | Only strategy logic running natively on Tradovate, NinjaTrader or TradingView is covered by text. The external-engine and bridge route remains unpermitted (the venue note's Q1–Q3, already sent; not re-asked here) |
| C5 | GTC 5.4.1.2 bars an "external … data feed" without defining it, and nothing grants data rights | Execution (signal source); feed equivalence | Compute signals from the venue's own platform feed. An externally fed engine is unpermitted until the venue note's Q4 is answered |
| C6 | Two scalping definitions: "fewer than 10 ticks" (MNQ: 2.5 points) against "under 1 minute" and "typically less than 3 points" | Execution (targets, exits); modelling (trade filter) | Satisfy both: no planned target or stop under 12 MNQ ticks, and no designed hold under 60 s. Count any shorter trade as a rule risk |
| C7 | The GTC (Dec 2024) describes a two-step "FXIFY Challenge and Verification" that does not match the Flex one-step evaluation. GTC 6.2/6.5 adopt "the parameters as stipulated on the Website". GTC 5.4.1.8 lets FXIFY amend the prohibited list on 7 days' notice | Provenance of every figure above | The FAQ figures are the binding parameters through 6.2. Re-read them at freeze (2026-10-23) and at any purchase; a later "Updated on" date invalidates this sheet |
| C8 | Session times are given as "EST" (one page says "ET") while the clock is on EDT | Execution (cut-off) | Read them as US/Eastern local time, matching the CME session. Flatten well before 16:59 ET; the auto-close is a backstop, not the plan |

These do not conflict, but they must be encoded: the 2-day minimum (implied by consistency); the 14-day inactivity rule (not modelled as an absorbing barrier, per house convention, inactivity barrier OFF); the 2% price-limit guard; the open-contract cap; the DLL, which is soft and removed by the bundle.
