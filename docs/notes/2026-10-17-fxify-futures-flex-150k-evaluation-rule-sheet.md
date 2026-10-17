# FXIFY Futures Flex 150K — evaluation-stage rule sheet (2026-10-17)

**Scope:** Flex plan, $150,000, **evaluation stage** (the tier in [four-firm addendum 2026-10-16 §3](../adr/2026-07-12-prop-portfolio-four-friendly-firms.md#addendum-2026-10-16--operator-rulings-50-ceiling-fresh-4-candidate-orb-mnq-v7-fxify-futures-flex-registration-accepted)). This is the dated primary-source re-read for condition (c). It changes no strategy. Its row is `FIRM_RULES["FXIFY_Futures_Flex_150K"]` (provisional; reconciled with this revision 2026-10-17).

**Sources, read 2026-10-17:**
- fxifyfutures.com FAQ pages, every one stamped "Updated on September 28, 2026". They were read through a rendering fetch that returns quoted extracts, because Cloudflare blocks scripted reads; they are not checked byte-for-byte. Cited as `faq:<slug>`.
- FXIFY Futures General Terms and Conditions (GTC), PDF at `fxifyfutures.com/terms-and-conditions/`, footer date December 6, 2024, sha256 `c25d2fa8…abfc72f`. Text extracted locally with `pdftotext`.
- GTC 6.2 makes "the parameters as stipulated on the Website" the pass conditions, so the FAQ figures below are the binding parameters.

The sheet has four parts: **A** sourced rules (what the sources say); **B** interpretations (readings where the text is silent or ambiguous, each with its basis); **C** optional stress assumptions (not part of the primary model); **D** open conflicts.

## A. Sourced rules

### A1. Risk limits

| Rule | Source text or value | Source |
|---|---|---|
| Fee | $449 one-time | faq:flex-plan-overview |
| Profit target | $9,000 (6%); "you must achieve and maintain a Profit Target of 6%" | faq:how-does-the-fxify-futures-evaluation-process-work |
| Maximum Loss Limit (MLL) | $4,500 (3.0%), end-of-day trailing (§A2) | faq:what-is-the-maximum-loss-limit-mll |
| Daily Loss Limit (DLL) | $3,000 (2%), applied to "the starting balance" of the day. "Considered a soft breach … read-only mode … for the remainder of the trading day … not a hard breach and will not cause you to fail your evaluation" | faq:what-is-the-daily-loss-limit |
| Max position | 10 minis / 100 micros, as "the number of open contracts a trader can hold". Micros count 1:10 against minis (MBT/MET 1:1, SIL 1:5) | faq:what-is-the-max-position-limit |
| Time limit | "The Flex Evaluation has a 30-day duration"; it can be extended for a fee | faq:what-is-the-time-limit-to-complete-the-evaluation |
| Minimum trading days | "No minimum trading-day requirement"; the 50% rule "naturally requires trading across at least 2 separate trading days". A trading day is "any day on which at least one trade is executed and closed" | faq:what-is-the-minimum-trading-days-requirement |
| Inactivity | "At least 1 trade every 2 weeks" (14 calendar days), then a 7-day grace period, then the account is "permanently closed" (evaluation and funded) | faq:what-is-fxify-futures-inactivity-policy |
| Price limits | "Prohibits trading when a product is within 2% of a CME price limit" | faq:what-is-fxify-futures-price-limit-trading-policy |
| Add-ons | Checkout only; each costs 15% of the fee, or 35% for the bundle: remove the DLL; MLL +$250; split raised to 100% | faq:how-do-fxify-futures-add-ons-work |
| Reset | $209; "can be reset at any time for a reset fee if a breach occurs" | faq:flex-plan-overview, evaluation-process FAQ |

### A2. Drawdown mechanics (faq:what-is-the-maximum-loss-limit-mll)

- The page's value table is headed **"Flex Accounts (Evaluation)"**: $150,000 = $4,500.
- **Trailing:** an "End-of-Day (EOD) trailing drawdown … based on the highest account balance recorded at market close". The threshold "will not move down".
- **Locking the Drawdown**, in the page's shared "How Max Loss Limit is Calculated" section: "Once your account profit equals your initial drawdown cushion (reaching $51,750 on a $50k account), or whenever a payout request is processed, the trailing threshold locks permanently at your starting account balance ($50,000) for the remainder of the account's life."
- **Breach:** "If your account balance falls to or below your Maximum Loss Limit threshold, all open positions will be closed, and the account will be deactivated."
- **The funded-parameters page** (faq:funded-account-parameters-overview) gives the Flex funded MLL as $4,500 EOD trailing and **does not mention a lock**.

### A3. Consistency (faq:what-are-fxify-futures-consistency-rules)

- "Trading returns from any single trading day cannot exceed 50% of the total returns made during the evaluation phase."
- Exceeding this does not fail the account: "You do not fail your account. Instead, you must continue trading and earning returns on subsequent days."
- Flex funded is 40%; Direct is 25%.

### A4. Session boundaries (faq:what-are-the-trading-hours-at-fxify-futures)

- "Trading hours run from 6 PM EST to 5 PM EST the following day."
- "Markets are closed from Friday 5 PM EST until Sunday 6 PM EST."
- "All trades must be closed by 4:59 PM EST each day. If you forget to close your trades, our system will automatically do it for you." The evaluation-process FAQ writes the same time as "4:59 PM ET".

### A5. Automation

- **Permission** (faq:can-i-use-eas-expert-advisors-to-trade): "the use of Expert Advisors (EAs) and automated trading scripts is permitted on both Flex and Direct accounts … enabled by default across all account types … across supported platforms, including NinjaTrader, Tradovate, and TradingView".
- **EA prohibitions** (same page): EAs engaging in latency arbitrage, micro-scalping, platform-glitch exploitation or news trading "will result in an immediate account breach and deactivation".
- **Supported platforms** (faq:trading-platforms-overview): Tradovate, TradingView via Tradovate, and NinjaTrader.
- **Copy trading** (faq:does-fxify-futures-allow-copy-trading): permitted between accounts owned by the "exact same user", including from a personal account or another prop firm's account. Copying from "third-party traders, signal providers, or automated signal services" is an immediate breach.
- **Prohibited strategies** (faq:what-trading-strategies-are-prohibited):
  - "Tick or Micro Scalping: taking trades with minimal movement, such as fewer than 10 ticks, without a clear plan."
  - "All or Nothing" approach: "relying on loss limits as a stop-loss strategy".
  - Reverse trading: opposite positions on separate accounts.
  - Group trading.
  - Latency arbitrage.
  - "High Leverage News Trading".
  - Statistical arbitrage.
- **Micro-scalping definition** (faq:what-is-micro-scalping-and-why-is-it-prohibited): "trades are executed within seconds to under a minute", with profits "typically less than 3 points".
- **GTC clauses:**
  - 5.4.1.4: no trades manipulating trading "including between connected accounts, or accounts held with different FXIFY entities … simultaneously entering into opposite positions".
  - 5.4.1.5(e): no "software, artificial intelligence, ultra-high speed, or mass data entry which might manipulate, abuse, or give you an unfair advantage".
  - 5.4.2: personal use only; no third party trades the account.
  - 9.6.6: no "automated means to view, display or collect information available through the Website or Services".
  - 5.4.1.8: the prohibited list may be amended "at any time with a notice of 7 days".
- **Not addressed by any page read:** API access, bridges, webhooks, VPS or cloud hosting.

### A6. Feed rights

- **Platform data** (faq:what-is-the-difference-between-level-1-and-level-2-data): Level 1 free; Level 2 "$39 monthly fee". No provider, no professional or non-professional status, no permitted-use terms.
- **Exchanges** (faq:what-products-can-i-trade): CME, CBOT, NYMEX, COMEX; no product list.
- **GTC clauses:**
  - 5.4.1.2: prohibited to "perform trades using an external or slow data feed" ("external" is undefined).
  - 9.6.5: no use of the Services or Content "otherwise than as permitted".
  - 5.9: disclaims liability for real trading that uses platform data.

## B. Interpretations

| # | Question | Reading | Basis |
|---|---|---|---|
| B1 | Does the MLL lock apply in the Flex **evaluation**? | **Yes.** At 150K the floor locks at **$150,000** once end-of-day profit reaches $4,500 (EOD balance ≥ $154,500). Row encoding: `dd_type: "trailing_locking"`, `dd_lock_offset_usd: 0` | The MLL page's only Flex label is "Flex Accounts (Evaluation)". The lock sits in that page's shared calculation section with no stage carve-out. The trigger is disjunctive ("or whenever a payout request is processed"), so the funded-only payout limb doesn't restrict the profit limb. The funded-parameters page carries no lock text that would place it at funded only. This differs from the Tradeify and MFFU cases behind the [2026-08-04 fix](../adr/2026-08-04-firm-rules-eval-lock-fix-applied.md), where the source put the lock under funded-only headings |
| B2 | Breach clock | Breach is tested on intraday balance against the floor set at end of day | The source gives no breach time. This follows the house intraday-honest convention (2026-10-02); it is a modelling convention, not an FXIFY statement |
| B3 | DLL basis | Day-start balance; whether it counts realized or unrealized P&L is unknown; the day resets at 18:00 ET | The FAQ says "starting balance" and gives no reset time; the trading day runs 6 PM–5 PM |
| B4 | "EST" | US/Eastern local time (EDT in October), matching the CME session | One page says "ET"; CME session times are ET |
| B5 | Scalping definitions | They describe prohibited **behaviour** (minimal-movement trades "without a clear plan"; holds of seconds to under a minute). They are **not** minimum stop, target or holding-period rules, and they impose no change on a strategy | Neither page states a minimum; the 10-tick text is qualified by "without a clear plan" |
| B6 | Off-platform logic and bridges | Not covered by the written permission; unresolved | The permission names supported platforms only. GTC 5.4.1.5(e) and 9.6.6 are broad. Covered by the venue note's [FXIFY Q1–Q3](2026-10-14-funded-venue-alternatives-assessment.md#12-questions-to-send); sent status unverified (§E4) |
| B7 | "External … data feed" | Undefined; unresolved whether it reaches signals computed from a separately licensed feed | GTC 5.4.1.2 alone. Covered by the venue note's FXIFY Q4 (sent status unverified, §E4); the CME side is in [CME non-display research](2026-10-10-cme-non-display-licensing-research.md). A new execution feed still needs the [feed-equivalence pre-flight](../spec/feed_equivalence_discovery_test_LOCKED.md) |
| B8 | Encodable fields | `profit_target_pct: 6.0`, `consistency_rule_pct: 50.0` (soft pass gate), `weekend_holds: False`, `daily_loss_pct` per the add-on choice. Inactivity is not modelled as an absorbing barrier (house convention: barrier OFF) | §A1, §A3, §A4 |

## C. Optional stress assumptions

These are not part of the primary model. A pre-registration may adopt one; none is required by this sheet.

- **S1, no evaluation lock.** `dd_lock_offset_usd: 1_000_000.0` (unreachable), bounding a B1 misreading. This is the pessimistic direction, since the $9,000 target lies past the lock point.
- **S2, DLL on unrealized P&L.** Treat the $3,000 limit as tested intraday on open equity (B3 unknown). This applies only if the DLL add-on is not bought.
- **S3, MLL +$250 add-on.** $4,750 cushion, if the pre-registration assumes the add-on.

No news exclusion is offered as a stress assumption. The sources define no window, and picking one would invent a rule (§D1).

## D. Open conflicts

- **D1, news trading (genuine conflict, unresolved).**
  - faq:news-trading-policy: "news trading is allowed".
  - faq:can-i-use-eas-expert-advisors-to-trade: EA "news trading" → "immediate account breach and deactivation".
  - faq:what-trading-strategies-are-prohibited bans only "High Leverage News Trading".
  - GTC 5.4.1.6 prohibits "gap trading by opening trade(s): (I) when major global news, macroeconomic event or corporate reports or earnings … are scheduled; and (II) 2 hours or less before a relevant financial market is closed for 2 hours or longer; or". The "and … or" joining makes it unclear whether (I) and (II) must both hold.
  - No source defines a news window, the qualifying events, or whether holding a position through a release counts.
  - For an automated strategy, the EA page is the most specific text, and it conflicts with the general page.
  - This sheet changes neither the strategy nor the model's news handling. The venue note's FXIFY Q6 is the resolution path; its sent status is unverified (§E4).
- **D2, GTC versus website.** The GTC (Dec 2024) describes a two-step "FXIFY Challenge and Verification" that does not match the one-step Flex evaluation. GTC 6.2 adopts the website parameters, and 5.4.1.8 allows 7-day amendments. Every figure here is valid only while the FAQ pages are stamped 2026-09-28; re-read them at the pre-registration freeze (2026-10-23).

## E. Decision readiness (second read, 2026-10-17)

A second, independent rendering-fetch read on 2026-10-17 found the same "Updated on September 28, 2026" stamp and the same values on the MLL, DLL, account-parameters, Flex-overview, time-limit, trading-hours, EA, news-policy and prohibited-strategies pages. The GTC PDF fetched again hashes to the same `c25d2fa8…abfc72f`.

**E1. MNQ costs: unpublished.**
- No FXIFY Futures source names a per-contract commission, an exchange or NFA pass-through, or whether a figure is per side or round trip. No article title in the FAQ index (48 articles by its category counts, every title listed on the category pages read) concerns fees or commissions. The payment-structure, account-parameters, Flex-overview and products pages list only the one-time fee and the reset fee. The GTC mentions "fee" only for the challenge purchase price (2.5–3.3) and has no "commission".
- Third-party reviews give unsourced estimates. They are not evidence.
- `cost_per_side_usd` stays `None`. The §4 harness's per-tier G2 (`cost_law_kill`) raises on `None` ([executor card](../briefs/handoffs/2026-10-06-four-firm-remc-executor-card.md) §0.5 item 4), so an FXIFY tier cannot be scored as frozen until one of two things happens: FXIFY gives a written figure, or the pre-registration adopts and discloses its own cost assumption (an operator choice, not a venue fact).

**E2. Source capture.**
- Condition (c) of the [2026-10-16 addendum §3](../adr/2026-07-12-prop-portfolio-four-friendly-firms.md#addendum-2026-10-16--operator-rulings-50-ceiling-fresh-4-candidate-orb-mnq-v7-fxify-futures-flex-registration-accepted) requires the modelled facts to be "re-verified at a primary source and dated". It does not require a byte-for-byte capture, and a repo search for byte-level capture requirements ("byte-for-byte", "byte-verified") found none that applies to firm rules. Tradeify, MFFU and BluSky rows rest on dated help-centre reads; Bulenox's byte-exact PDF re-check was an extra step, not a stated requirement.
- This sheet and the second read above are two dated primary-domain reads that agree. On that reading they meet (c). The row's "FAQ capture is not byte-verified" hold is a self-imposed caution, not a gate. Lifting it is the acceptance owner's call.
- Residual risk: a rendering fetch can paraphrase. The load-bearing numbers ($4,500, the lock text, $9,000, 50%, 100 micros, $3,000, 4:59 PM) were returned as quotes in the second read; the first read's extracts are as the sheet records them. If the owner wants more, an operator browser save of the MLL page is enough.

**E3. Facts, modelling assumptions and execution restrictions.**

| Item | Fact (sourced) | Modelling assumption (pre-registration states it) | Execution restriction (before trading only) |
|---|---|---|---|
| News | Conflict D1: general "allowed"; EA "news trading" = immediate breach; "High Leverage News Trading" prohibited; GTC 5.4.1.6 gap clause. No window is defined | None. The MC applies no news exclusion. Inventing a window is barred (§C) | Whether ORB v7's automated entries or holds around scheduled releases are "EA news trading". Answer at FXIFY Q6 |
| DLL $3,000 | Soft, read-only for the rest of the day; "resets based on your new starting balance"; Flex overview: "caps allowable intraday losses" | The engine ignores it (`daily_loss_pct: None`). Material only if a day's loss at `R_deploy` can reach $3,000; otherwise immaterial. The bundle removes it | Realized or open P&L; reset time; whether positions are flattened |
| MLL breach clock | Not stated | B2: intraday, a house convention and the conservative direction | FXIFY Q7 |
| 30-day duration | "30-day duration"; extension for "a small fee"; calendar or trading days not stated; expiry outcome not stated | **Material and not yet encoded.** Prereg v2 uses horizon 1500. The pre-registration must choose and disclose a horizon (for example 30 calendar days ≈ 21 sessions, or paid extensions with the fee counted) | Extension price |
| Session close | 4:59 PM ET auto-close; weekend closed; no holiday rule | `weekend_holds: False`; ORB is intraday | Whether the auto-close counts as a violation (Q7) |
| Prohibited behaviour | The 2026-10-17 page also lists "exploiting the absence of slippage", "isolated fills in illiquid or gapped markets" and account rolling | None | Fill-realism discretion; no strategy change |

**E4. Acceptance map.**
- **Acceptable now (sourced, two dated reads):** `starting_balance` 150,000; `dd_type` trailing_locking; `max_dd_pct` 3.0; `profit_target_pct` 6.0; `micro_contract_cap` 100; `consistency_rule_pct` 50.0 (soft); `soft_daily_loss_pct` 2.0; `weekend_holds` False; `daily_loss_pct` None and `inactivity_max_idle_days` None (deliberate non-encodings).
- **Acceptable as a disclosed interpretation:** `dd_lock_offset_usd` 0.0 (B1, with S1 as stress); `min_trading_days` 2 (derived); the intraday breach clock (B2).
- **Not acceptable as a fact:** `cost_per_side_usd` (E1).
- **Decision owner for cost, horizon and DLL:** the fresh candidate's §4 pre-registration (ORB MNQ v7, freeze 2026-10-23; [addendum §2](../adr/2026-07-12-prop-portfolio-four-friendly-firms.md#addendum-2026-10-16--operator-rulings-50-ceiling-fresh-4-candidate-orb-mnq-v7-fxify-futures-flex-registration-accepted)), held by the existing technical owners under Codex. This sheet supplies the facts and does not choose for it.
- **What stops FXIFY counting in the 2026-10-23 frozen set:**
  - (a) the row is not on `main` until #867 merges;
  - (b) the pre-flight passes only with `allow_provisional_rules=True`, so the owner must lift the provisional hold, which (c) no longer needs;
  - G2 cannot run on a `None` cost (E1);
  - the pre-registration must fix a horizon for the 30-day clock (E3).
- **Before execution only:** news (Q6), the breach clock and auto-close (Q7), the DLL basis, the extension price, and the B6/B7 automation and feed questions (Q1–Q4). None of them changes the MC inputs above.
- **Outreach status: unverified.** The venue note lists Q1–Q8 as to be sent (its §11 step 1, 10-14 → 10-16). Neither the repo nor a search of the connected Gmail account for "fxify" over the prior 14 days (2026-10-17) holds a sent copy or a reply. That makes the sent status unverified, not evidence that nothing was sent; the questions may have gone by support chat, a ticket or another inbox. Until the operator confirms the channel and date, this sheet relies on no answer and on neither sent status (§B6, §B7, §D1).
