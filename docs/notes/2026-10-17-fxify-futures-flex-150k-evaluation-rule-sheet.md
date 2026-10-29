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
- **The funded-parameters page** (faq:funded-account-parameters-overview) gives the Flex funded MLL as $4,500 EOD trailing and **does not mention a lock**. The payout trigger can fire only at a stage that has payouts; the funded lock therefore remains unverified, not disproved.

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
- **Copy trading** (faq:does-fxify-futures-allow-copy-trading): permitted between accounts owned by the "exact same user", including from a personal account or another prop firm's account. Copying from "third-party traders, signal providers, or automated signal services" is an immediate breach. The page gives no account limit. It does not address running the same strategy independently, and permission to copy into FXIFY does not establish permission to copy out.
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
| B6 | Off-platform logic and bridges | Not covered by the written permission; unresolved | The permission names supported platforms only. GTC 5.4.1.5(e) and 9.6.6 are broad. Superseded outreach mapping: FX-N1; sent status remains unverified (§E4) |
| B7 | "External … data feed" | Undefined; unresolved whether it reaches signals computed from a separately licensed feed | GTC 5.4.1.2 alone. Superseded outreach mapping: FX-5b (deferred; sent status unverified, §E4); the CME side is in [CME non-display research](2026-10-10-cme-non-display-licensing-research.md). A new execution feed still needs the [feed-equivalence pre-flight](../spec/feed_equivalence_discovery_test_LOCKED.md) |
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
  - This sheet changes neither the strategy nor the model's news handling. FX-2 is the resolution path; its sent status is unverified (§E4).
- **D2, GTC versus website.** The GTC (Dec 2024) describes a two-step "FXIFY Challenge and Verification" that does not match the one-step Flex evaluation. GTC 6.2 adopts the website parameters, and 5.4.1.8 allows 7-day amendments. Every figure here is valid only while the FAQ pages are stamped 2026-09-28; re-read them when any pre-registration that uses this tier freezes. A 2026-10-19 re-read found the MLL, EA, news, copy-trading and funded-parameters pages still stamped 2026-09-28 and the GTC hash unchanged; the fee, DLL, time-limit and hours pages were not re-read.

## E. Decision readiness (second read, 2026-10-17)

A second, independent rendering-fetch read on 2026-10-17 found the same "Updated on September 28, 2026" stamp and the same values on the MLL, DLL, account-parameters, Flex-overview, time-limit, trading-hours, EA, news-policy and prohibited-strategies pages. The GTC PDF fetched again hashes to the same `c25d2fa8…abfc72f`.

A narrower 2026-10-19 re-read found the MLL, EA, news, copy-trading and funded-parameters pages unchanged and still stamped 2026-09-28; the GTC PDF hash was unchanged. It did not re-read the fee, DLL, time-limit or trading-hours pages. A fresh read remains owed when any pre-registration using this tier freezes.

**E1. MNQ costs: unpublished.**
- No FXIFY Futures source names a per-contract commission, an exchange or NFA pass-through, or whether a figure is per side or round trip. No article title in the FAQ index (48 articles by its category counts, every title listed on the category pages read) concerns fees or commissions. The payment-structure, account-parameters, Flex-overview and products pages list only the one-time fee and the reset fee. The GTC mentions "fee" only for the challenge purchase price (2.5–3.3) and has no "commission".
- Third-party reviews give unsourced estimates. They are not evidence.
- `cost_per_side_usd` stays `None`. The §4 harness's per-tier G2 (`cost_law_kill`) raises on `None` ([executor card](../briefs/handoffs/2026-10-06-four-firm-remc-executor-card.md) §0.5 item 4). Two ways forward:
  - **A written FXIFY figure.** That is verified venue pricing and can enter the row.
  - **A cost assumption that the pre-registration discloses** (an operator choice). It supports conditional research only. It is not verified venue pricing, it does not enter the row as a fact, and any G2 or clearance result that rests on it is conditional on it.

**E2. Source capture.**
- Condition (c) of the [2026-10-16 addendum §3](../adr/2026-07-12-prop-portfolio-four-friendly-firms.md#addendum-2026-10-16--operator-rulings-50-ceiling-fresh-4-candidate-orb-mnq-v7-fxify-futures-flex-registration-accepted) requires the modelled facts to be "re-verified at a primary source and dated". It does not require a byte-for-byte capture, and a repo search for byte-level capture requirements ("byte-for-byte", "byte-verified") found none that applies to firm rules. Tradeify, MFFU and BluSky rows rest on dated help-centre reads; Bulenox's byte-exact PDF re-check was an extra step, not a stated requirement.
- This sheet and the second read above are two dated primary-domain reads that agree. On that reading they meet (c). The row's "FAQ capture is not byte-verified" hold is a self-imposed caution, not a gate. Lifting it is the acceptance owner's call.
- Residual risk: a rendering fetch can paraphrase. The load-bearing numbers ($4,500, the lock text, $9,000, 50%, 100 micros, $3,000, 4:59 PM) were returned as quotes in the second read; the first read's extracts are as the sheet records them. If the owner wants more, an operator browser save of the MLL page is enough.

**E3. Facts, modelling treatment and qualification conditions.**

None of the open questions below blocks infrastructure work or research that is labelled conditional. **Qualification of a nominated strategy and configuration on this tier** needs one of two things for each row: evidence that the item does not affect that strategy and configuration, or a model of its effect. "Before execution" is not a category that waives this.

| Item | Fact (sourced) | Modelling treatment now | Qualification condition |
|---|---|---|---|
| News | Conflict D1: general "allowed"; EA "news trading" = immediate breach; "High Leverage News Trading" prohibited; GTC 5.4.1.6 gap clause. No window is defined | None. The MC applies no news exclusion. Inventing a window is barred (§C) | Either evidence that the nominated configuration's entries and holds are not "EA news trading" (an FXIFY answer at Q6, or a schedule showing no overlap with releases under a reading FXIFY accepts), or a model of the exposure. An immediate breach would be an account failure, so this cannot be left unmodelled for qualification |
| DLL $3,000 | Soft, not a hard account failure; read-only "for the remainder of the trading day"; "resets based on your new starting balance"; Flex overview: "caps allowable intraday losses". Realized or open P&L, reset time and flattening not stated | The engine has no soft-DLL model (`daily_loss_pct: None` is correct, because a hard bust would be wrong). The rest-of-day lockout can still change pass probability, by ending a day's trading or flattening a position the strategy would have held | One of three. (i) Assume the no-DLL add-on as an **explicit product assumption** with its cost (35% bundle or 15% single), and model that product. (ii) Show from the nominated configuration's trades that no day's loss, open or realized under S2, reaches $3,000 at `R_deploy`. (iii) Model the lockout. Which one applies is a pre-registration choice |
| MLL breach clock | Not stated | B2: intraday, a house convention and the conservative direction | Holds as disclosed. If FXIFY says end-of-day, B2 stays the conservative bound (Q7) |
| 30-day duration | "30-day duration"; extension for "a small fee"; calendar or trading days not stated; expiry outcome not stated | **Not encoded.** Prereg v2 uses horizon 1500 | The pre-registration specifies the horizon and reports **evaluation timeout** (target not reached by the horizon, with the floor never breached) **separately from drawdown bust**. A timeout is not a bust; it is a non-pass whose cost is a reset, an extension or a new fee. State the day basis (calendar or sessions), whether paid extensions are assumed and at what fee, and how an unknown expiry outcome is treated |
| Session close | 4:59 PM ET auto-close; weekend closed; no holiday rule | `weekend_holds: False` | Evidence that the nominated configuration is flat before 16:59 ET, or a model of the forced close. Whether the auto-close counts as a violation is Q7 |
| Prohibited behaviour | The 2026-10-17 page also lists "exploiting the absence of slippage", "isolated fills in illiquid or gapped markets" and account rolling | None | Evidence that the configuration's fill assumptions do not depend on these, or a model of them. No strategy change |
| Automation and feed (B6, B7) | Generic platform-scoped permission; "external or slow data feed" undefined | Not an MC input | Venue admission and the feed-equivalence pre-flight; S1 still applies. This is separate from MC qualification, and required before any execution |

**E4. Acceptance map.**
- **Acceptable now (sourced, two dated reads):** `starting_balance` 150,000; `dd_type` trailing_locking; `max_dd_pct` 3.0; `profit_target_pct` 6.0; `micro_contract_cap` 100; `consistency_rule_pct` 50.0 (soft); `soft_daily_loss_pct` 2.0 (base product; the no-DLL add-on removes it); `weekend_holds` False; `daily_loss_pct` None and `inactivity_max_idle_days` None (deliberate non-encodings).
- **Acceptable as a disclosed interpretation:** `dd_lock_offset_usd` 0.0 (B1, with S1 as stress); `min_trading_days` 2 (derived); the intraday breach clock (B2).
- **Not acceptable as a fact:** `cost_per_side_usd` (E1). A disclosed assumption supports conditional research only, not verified venue pricing.
- **Decision owner for cost, horizon and DLL:** the nominated candidate's §4 pre-registration ( [addendum §2](../adr/2026-07-12-prop-portfolio-four-friendly-firms.md#addendum-2026-10-16--operator-rulings-50-ceiling-fresh-4-candidate-orb-mnq-v7-fxify-futures-flex-registration-accepted)), held by the applicable pre-registration owner. This sheet supplies the facts and does not choose for it.
- **What stops FXIFY counting in a frozen tier set:**
  - (a) the row is not on `main` until #867 merges;
  - (b) the pre-flight passes only with `allow_provisional_rules=True`, so the owner must lift the provisional hold, which (c) no longer needs;
  - G2 cannot run on a `None` cost. With a disclosed assumption it runs, but the result is conditional (E1);
  - the pre-registration must specify a horizon for the 30-day clock and report timeout separately from bust (E3);
  - the pre-registration must state its DLL treatment: the no-DLL product assumption, evidence that the DLL is never reached, or a lockout model (E3).
- **Conditional, not execution-only:** news (FX-2), the auto-close (FX-N2), the DLL basis, the extension price and the prohibited-behaviour items need not block infrastructure or conditional research. Each must be shown not to affect the nominated configuration, or modelled, before that configuration qualifies (E3). The B6/B7 automation and feed questions (FX-N1 and deferred FX-5b) are venue-admission matters and must be settled before any execution.
- **Outreach status: unverified.** The 2026-10-19 question draft supersedes the venue note's Q1–Q8 and maps them as follows: Q1 → FX-N1, Q2 → FX-N1, Q3 → FX-N1, Q4 → FX-5b (deferred), Q5 → FX-3, Q6 → FX-2, Q7 → FX-7 and FX-N2 (both deferred), and Q8 → FX-N8. Nothing has been recorded as sent; Joshua must confirm whether any earlier question went out by email, chat or ticket before sending the replacement draft. This sheet relies on no answer or sent status (§B6, §B7, §D1).
