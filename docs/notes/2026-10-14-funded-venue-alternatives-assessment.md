# Funded-account venues for the book after Tradeify (research, 2026-10-14)

**Status:** research input for Joshua. It ranks venues and drafts questions; it changes no status and grants no spend, account, arming or venue change. Track B stays suspended ([checklist addendum 2026-10-13](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-10-13--track-b-suspended-11-08-decision-rules-draft)).
**Question:** which prop venue could run the current system on a funded account with the fewest changes, now that Tradeify bars external engines on evaluation and sim-funded accounts ([route record, 10-12 addenda](../briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md#addendum-2026-10-12-later--tradeify-support-strategy-logic-must-be-native-for-evaluation-accounts))?
**Decision it informs:** whether to open a successor-venue question at or before the 11-08 sitting. A move needs an operator GO overriding [S1](../adr/2026-08-07-loop-s1-environment-ratification.md) ("no successor migration"). Venues outside `AUTOMATION_FRIENDLY_PROP_FIRMS` cannot discharge the [four-firm §4](../adr/2026-07-12-prop-portfolio-four-friendly-firms.md) falsifier without an expansion ADR. Within-Tradeify routes are covered separately in [2026-10-13-tradeify-compliant-automation-routes.md](2026-10-13-tradeify-compliant-automation-routes.md).
**Evidence limit:** no MC, replay or screen was run. Firm facts come from official help centres, terms and pricing pages fetched 2026-10-13/14 by research agents, with each candidate re-checked independently. Apex, Lucid's main site and FXIFY blocked direct reads; their quotes come from search excerpts, PDF copies or rendered summaries (labelled). No funded or live account agreement was readable. All bust directions for 150K-class tiers are **INFERENCE** from the 100K size grid.

Labels: **DOCUMENTED** (official firm page or repo file), **INFERENCE** (reasoning or arithmetic from documented inputs), **UNVERIFIED** (third-party or blocked source).

## 1. Answer

No prop venue can take the system as it runs today. Of 54 futures prop firms screened, none permits in writing a privately owned external engine, cloud-hosted, sending orders through an API or bridge at every paid stage. Three venues could, if each gives one clause-cited written yes:

| Pick | Venue | Why | Main open item |
|---|---|---|---|
| Fewest changes | **LucidPro 150K**, daily loss limit off | Tradovate family (same transport as the rail and the personal lane). Full 6J listed; short 6J with long micros in one account explicitly allowed; 100-micro cap at evaluation and funded; non-fatal 16:45 ET flat; no evaluation consistency | Funded agreement §1(c) requires prior written approval for automated software and bans third-party-developed automated software (CrossTrade?) |
| Best terms (Rithmic adapter) | **FundYourEdge Prime 150K** | Strongest permission clause found, in the governing ToS; end-of-day-only breach per help article; no evaluation consistency; 100-micro cap from day one; 16:59 ET; lowest costs | 6J unconfirmed; "unapproved platform" undefined; new firm; 30-day evaluation |
| Cheapest on Tradovate | **FXIFY Flex 150K** | 16:59 ET; 100-micro cap; drawdown locks at the starting balance; $449 one-time | Platform-scoped generic permission; 6J never named; EA "news trading" ban with immediate breach; "external or slow data feed" clause |

Topstep is the only firm whose rules name API bots, but it needs the most change: orders from a personal device only, 16:10 ET flat, funded (XFA) accounts start at 30 micros, no API on Live. Bulenox (Rithmic, 120-micro cap, $5,500 rope) is a second-wave candidate behind a 2021 ToS approval clause.

On a consistent rubric the leaders score within 0.6 of each other (§4), so the written answers decide. Ask Lucid (as a formal §1(c) approval request), FundYourEdge, FXIFY and Bulenox at once and buy nothing until they answer. If more than one passes, choose the venue on the personal lane's broker rail so one adapter serves both lanes.

## 2. What a venue must accept for the book to run unchanged

| Requirement | Source (DOCUMENTED) |
|---|---|
| External, privately owned engine trading automatically at evaluation and sim-funded, not only live | rail architecture; [route record](../briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md) |
| Cloud hosting of the order path (Fly.io listener) | [feed-cost note](2026-10-11-feed-cost-sanity-check.md) addendum 2026-10-12 |
| Full-size 6J (Aegis, sell-only) with long MGC, MYM, MNQ in one account; 1 full = 10 micros | [`book_policy.py`](../../ops/c1_rail/book_policy.py) |
| Cap ≥ 80 micro-equivalents at evaluation and funded (Aegis alone is 8 × 6J); half size needs about 40 | [`book_policy.py`](../../ops/c1_rail/book_policy.py); [`firm_rules.py`](../../core/firm_rules.py) |
| Flat deadline ≥ 16:15 ET: the scored series fills its flatten at 16:15 and is open past 16:10 on 403 of 1,020 weekdays; an earlier deadline forces re-expression and requalification | [four-firm RESULTS](../../lab/analysis/c1/four_firm_remc_2026-10/RESULTS.md); [prereg I-24](../briefs/pre-registration/2026-10-02-four-firm-dated-remc-prereg-DRAFT.md); [halt contract](../spec/2026-09-14-tb-s3-halt-resume-contract.md) |
| Bracket entry, per-bar stop modify, close, cancel, fill and position reads | [route record §6](../briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md) |

Owed at every venue: a production four-leg broker adapter (the book owner returns `production_route_unavailable`, [`book_account_owner.py`](../../ops/c1_rail/book_account_owner.py); the legacy CrossTrade path is long-only, [`c1_rail_listener.py`](../../ops/c1_rail/c1_rail_listener.py)); a firm ADR, tier rows, pre-flight and a pre-registered intraday-honest re-MC (fresh authorization; four-firm early-fail branch armed); venue editions, protection rebinding, own M1 acceptance; stopping all Tradeify use of the bot first (FTA §6.6, [exclusive-use replies](2026-10-10-tradeify-exclusive-use-replies.md)); and the CME non-display answer ($0–$1,408/month, ticket #04738415, [feed-cost note](2026-10-11-feed-cost-sanity-check.md)).

## 3. Market screen (54 prop firms)

| Class | Count | Firms |
|---|---|---|
| Ban automation, native-only, or block the route | 29 | Apex, Take Profit Trader, Alpha Futures, TradeDay, Elite Trader Funding, Phidias, Aqua Futures, E8, Top One, Funded Futures Family, Blue Guardian, Purdia, Hola Prime, The5ers Futures, Nexgen, Winbance, FundedSeat, Savius, Halcyon, PropEd, 10FOUR, UProfit (VPS), TickTickTrader, Phoenix, Emerge, BestProp4U, Tradeify (since 10-12), FundingTicks and The Futures Desk (not selling) |
| Silent or unconfirmable | 9 | Earn2Trade, Leeloo, OneUp, Ment Funding, Legends, Traders Launch, YRM, Ylos, Swiss Firmup |
| Generic or conditional permission | 15 | FXIFY, FundYourEdge, Lucid, Bulenox, Goat, DojoTraders, BluSky, DayTraders.com, FLI Capital, 18th Street, FTMO Futures, MFFU, FFN, The Trading Pit, FundedNext |
| Names API bots in writing | 1 | Topstep (personal device only; no API on Live) |
| Permits the exact setup | 0 | — |

**DOCUMENTED, industry:** Tradovate states prop and evaluation accounts are not eligible for its API (repo read 2026-10-10; page unreadable 10-13/14, **UNVERIFIED** since), so Tradovate-hosted prop routes need a bridge, the class Tradeify barred. ProjectX wound down third-party service (Feb 2026, third-party report), leaving Topstep its only API firm. Platform scan: CQG, Volumetrica, Quantower, Tradesea and in-house platforms expose no trader-usable order API; Rithmic R|Protocol/R|API+ do, subject to conformance and firm entitlement.

## 4. Scorecard

Rubric (0–10): permission evidence 35%, change needed 30%, drawdown fit 20%, economics 15%. Same deductions for every firm: unconfirmed 6J −2 change; "external or slow data feed" clause −1 change; approval clauses scored 3.5 on permission. **INFERENCE** throughout.

| Venue (best account) | Permission | Change | Drawdown | Economics | Overall | If permission confirmed |
|---|---|---|---|---|---|---|
| FundYourEdge Prime 150K | 4.5 | 4.5 | 7 | 5.5 | 5.2 | 6.8 |
| Bulenox Fast Track 150K Opt 2 | 3.5 | 6.5 | 5 | 4 | 4.8 | 6.2 |
| FXIFY Flex 150K | 4 | 4.5 | 5 | 6 | 4.7 | 6.5 |
| Goat EOD 150K | 4 | 5 | 5 | 5 | 4.7 | 5.9 |
| LucidPro 150K (DLL off) | 3.5 | 5 | 5.5 | 5 | 4.6 | 6.0 |
| BluSky Orbit 150K | 3 | 4 | 5 | 5 | 4.0 | 6.2 |
| Topstep 150K → XFA | 5 | 1 | 4 | 5 | 3.6 | 4.5 |
| Personal Tradovate (self-funded comparator) | 6.5 | 7.5 | 7 | 4 | 6.5 | — |

"If permission confirmed" sets permission to 7.5 and removes the 6J deduction where the same reply would confirm 6J. Lucid's change score carries −1.5 for documented live caps below 80; other firms' live caps are unknown. The research panel's as-fitted ranking put FXIFY first (5.6) only because 6J was docked unevenly. Lucid is preferred for fewest changes despite its score because, once it says yes, its remaining unknowns are fewest (6J, mixed long/short, cap and flat already documented) and §1(c) yields a signed, stage-specific approval.

## 5. Requirement check (DOCUMENTED ✓ · unconfirmed ? · fails ✗)

| Venue | External engine | Cloud host | Full 6J short + micros | Cap ≥ 80 eval and funded | Flat ≥ 16:15 ET | Tradovate transport | EOD-only breach | No eval consistency |
|---|---|---|---|---|---|---|---|---|
| LucidPro 150K | ? approval | ? | ✓ | ✓ | ✓ 16:45 | ✓ | ? | ✓ |
| FXIFY Flex 150K | ? generic | ? | ? | ✓ (funded inferred) | ✓ 16:59 | ✓ | ? | ✗ 50% |
| FundYourEdge Prime 150K | ? ToS §7.2 | ? | ? | ✓ | ✓ 16:59 | ✗ Rithmic | ✓ help article | ✓ |
| Bulenox Fast Track 150K | ? FAQ vs ToS | ? | ✓ | ✓ 120 | ✓ 16:59 | ✗ Rithmic | ✗ probably intraday | ✓ (20–30% at payout) |
| Goat EOD 150K | ? | ✗ VPS banned | ✓ | ✓ 120 | ✓ 16:55 | ✗ local NT8 | ? conflicting | ✗ 50% |
| Topstep 150K | ✓ API bots | ✗ personal device | ✓ | ✗ XFA starts 30 | ✗ 16:10 | ✗ ProjectX | ✗ | ? soft 55% |

## 6. Drawdown geometry

Under a fixed-dollar trail the full book on rope R behaves like the book at size $3,000 ÷ R on a $3,000 rope ([size-feasibility RESULTS](../../lab/analysis/c1/size_feasibility_2026-10/RESULTS.md): 0.5 cleared 5% bust, 0.75 failed; full size busts 25–36% on $3,000, [four-firm RESULTS](../../lab/analysis/c1/four_firm_remc_2026-10/RESULTS.md)). **INFERENCE:**

| Tier | Rope | Equivalent size | Reading |
|---|---|---|---|
| Tradeify Select 100K | $3,000 | 1.00 | measured: 36.08% bust (Run-2) |
| Topstep / Lucid / FundYourEdge / Goat 150K | $4,500 | 0.67 | untested zone (0.5–0.75) |
| FXIFY Flex 150K + bundle | $4,750 | 0.63 | untested zone |
| Bulenox Fast Track 150K Opt 2 | $5,500 | 0.55 | untested zone, nearest the cleared point |

Plan on FLOOR-HALF (ORB off) or about 0.75 size until a dated intraday-honest re-MC on the chosen tier clears full size.

## 7. Routes and adapter reuse

| Rail | Chain | Venues | Notes |
|---|---|---|---|
| Tradovate | daemon → Fly.io listener → new 4-leg adapter → CrossTrade → Tradovate | Lucid, FXIFY, BluSky; personal Tradovate | Repo already models Tradovate semantics. Shared risk: bridge-only on prop accounts. CrossTrade REST has no trailing stop (Vanguard uses its fixed-stop edition). CrossTrade "Link Demo" OAuth to prop logins is a vendor claim (**UNVERIFIED**) |
| Rithmic | daemon → Fly.io listener → new R\|Protocol or R\|API+ adapter → Rithmic | FundYourEdge, Bulenox, DayTraders.com; AMP self-funded | New protocol plus Rithmic conformance; server-side brackets and trailing stops. R\|Protocol is "Not available for paper trading demos with live market data" (rithmic.com); whether that covers paid prop paper IDs is unconfirmed; R\|API+ (C++) carries no such caveat. NinjaTrader is no longer onboarding new Rithmic connections |
| ProjectX | daemon and new ProjectX adapter on a home machine → api.topstepx.com | Topstep only | Cloud may only log, monitor and receive copies of fills; signals from ProjectX data (ToU bans "an external or slow Data feed") |

## 8. Shortlist evidence

**LucidPro 150K (DLL off).** $4,500 EOD trail, locks at $150,100; $9,000 target; 100-micro cap at evaluation and funded ("No scaling plan, access to max contract size immediately"); 16:45 ET, auto-flatten "does not result in a failed account"; 6J $2.40/side, micros $0.50, MGC $0.80; hedging FAQ: "You can go long / short different contracts in the same account". Live 150K starts at 40 CME / 40 CBOT / 20 COMEX micros. Price about $259 (**UNVERIFIED**, third-party). Governing text, LucidPro/LucidFlex Account Agreement §1(c), Last Modified 2025-11-28 (dash.lucidtrading.com/assets/pdfs/lucid-agreement.pdf): "obtain written approval from us prior to using any Automated Trading Software … we prohibit the use of any Automated Trading Software owned or developed by any third party other than you." Prohibited conduct also lists "Performing trades using an external or slow data feed". Evaluation terms unread (403).

**FXIFY Futures Flex 150K.** $449 one-time (+35% bundle removes the soft DLL, adds $250 rope, 100% split); $4,500 EOD trail locking at the starting balance; $9,000 target; 50% evaluation consistency; 10 minis / 100 micros; 16:59 ET ("our system will automatically do it for you", fxifyfutures.com trading-hours FAQ, 2026-09-28). EA FAQ, updated 2026-09-28 (fxifyfutures.com/faqs/general-rules/can-i-use-eas-expert-advisors-to-trade/, rendered summary, **UNVERIFIED** byte-for-byte): "the use of Expert Advisors (EAs) and automated trading scripts is permitted on both Flex and Direct accounts … enabled by default across all account types … across supported platforms, including NinjaTrader, Tradovate, and TradingView." The same page lists EA "news trading" as prohibited with immediate breach. GTC v1.21 (Dec 2024) 5.4.1.2 bars trades "using an external or slow data feed". No page names 6J. 30-day evaluation clock.

**FundYourEdge Prime 150K.** $429 list ($257 coupon seen 2026-10-14); $4,500 EOD rope, funded lock at $150,100; $9,000 target; no evaluation consistency; soft DLL; "10 mini / 100 micro" from the first funded trade; flat by 16:59 ET; $2.50/side full-size, $0.25 micros. ToS §7.2, last updated 2026-09-02 (fundyouredge.com/terms-of-service, verbatim): "Automated and algorithmic trading with your own proprietary strategy is permitted, and you may copy trades between your own accounts. … or trade through an unapproved platform." Help article 75: breach "measured on your end-of-day balance, never an intraday swing". §7.3 allows screen-share audits of "your tools". Rithmic only; 6J not named; five Prime payouts, then a discretionary live program.

**Bulenox Fast Track 150K, Option 2.** $788 one-time (Momentum 150K Opt 2: $358, 30-day window); $5,500 EOD drawdown locking at +$100; 12 minis = 120 micros; permanent $3,300 DLL; first payout goal $9,000; payout consistency 20%/25%/30%; flat 3:59 PM CT; 6J $2.36, MGC $0.76, MYM/MNQ $0.61 per side. FAQ (bulenox.com/faq, 2026-09-17): "Bots, algorithms and trade copiers are permitted. If you connect to Rithmic through a third-party API or composite software, an additional $100 per month applies. Only user-built tools intended solely for the account owner's personal use are permitted." Terms of Use (body "Updated July 2021"): "any third party algorithms must be approved from the Bulenox management team"; "DTC Protocol Bridge API or automated discretional trading" listed as abuse. Forced live transition ("If you do not consent to the transition, the applicable Master Account will be closed").

**Topstep 150K Combine → XFA.** $199/month + $149 activation, API $29/month; $4,500 EOD trail with real-time breach; $9,000 target; Combine cap 150, XFA scaling starts at 3 lots; flat 3:10 PM CT (flattening from 3:08); 6J listed. Help article 11187768, modified 2026-09-17 (help.topstep.com, verified): "Custom automated strategies and bots are allowed via the TopstepX / ProjectX API … All trading activity must originate from your personal device. The use of VPS, VPNs, and remote servers is prohibited … Live funded accounts are not allowed to trade through the ProjectX API." Call-up cannot be declined.

## 9. Economics (DOCUMENTED terms; values INFERENCE)

| Venue | Entry | Payout per request | Split | After the sim stage |
|---|---|---|---|---|
| LucidPro 150K | ~$259 (third-party) | $3,000 first, then $3,500 | 90/10 | Live after payout 5, reduced caps |
| FXIFY Flex 150K | $449 (+$157) | ≤ $3,000 per cycle | 90/10 (100% with bundle) | Discretionary "FXIFY Trader" contract |
| FundYourEdge Prime 150K | $429 ($257 coupon) | $3,000 first, then $3,500 | 90/10 | 5 payouts, then discretionary live |
| Bulenox Fast Track 150K | $788 | $3,000 (1–3), then $3,500 | 90/10 (pages conflict) | Forced transition |
| Topstep 150K | $199/mo + $149 + $29/mo API | ≤ $5,000 (50% of balance) | 90/10 | Forced call-up; no API on Live |

Three payouts at these tiers total at most about $9,000–$10,000 gross and need $18,000+ of profit. A user non-display feed at $1,408/month is about $16.9K a year, the same order as one account's simulated payout ceiling. CME's answer on ticket #04738415 decides whether any funded venue pays for its data.

## 10. Excluded firms (selected official wording)

| Firm | Wording | Source |
|---|---|---|
| Apex | "the use of automation is strictly prohibited on all account types" | support.apextraderfunding.com art. 31519788944411 (search excerpt, **UNVERIFIED**) |
| Take Profit Trader | "No Trading Bots or Algos. Automated trading systems, bots, or algorithmic execution tools are not permitted." | TPT help art. 34431153546397, 2026-10-09 |
| Alpha Futures | "The use of AI, bots, and other automated trading mechanisms is strictly prohibited across all account types." | help.alpha-futures.com art. 9508585 |
| TradeDay | "We do not make platform APIs available to traders." VPS not allowed | tradeday.freshdesk.com art. 103000085101 |
| Elite Trader Funding | "The only automated trading tools currently authorized are the approved trade copiers listed above." | elitetraderfunding.app trade-copier disclaimer, 2026-10-08 |
| Blue Guardian Futures | "AI, bots, and other fully automated trading mechanisms are strictly prohibited across all account types." | helpfutures.blueguardian.com art. 14110289, 2026-10-12 |
| E8 Futures | Prohibited: "Semi-Automated or Fully-Automated Trading, such as trading bots, AI tools…" | E8 help art. 10209270 |
| Phidias | "The use of robots, fully automated trading algorithms, or any other form of automated trading is not permitted." | phidiaspropfirm.com/rules, 2026-09-22 |
| MyFundedFutures | 16:10 ET auto-liquidation makes the scored series I-24 inadmissible; generic "own settings" automation wording | [prop envelope §4](../../ops/prop_envelope_default.md) |
| Goat Funded Futures | own EAs allowed, but VPS/remote server banned "with no exceptions"; "EA that follows an external source" prohibited | Goat trading rules 2026-09-08; VPS article 2026-08-11 |

## 11. Verification-first plan (fits inside the suspension; no spend)

1. **10-14 → 10-16:** send §12's questions (Lucid as a formal §1(c) approval request; FundYourEdge; FXIFY; Bulenox; platform questions to CrossTrade/Tradovate and Rithmic; optionally Topstep). Chase CME #04738415 and Tradeify compliance.
2. **10-21:** triage; convert any chat or phone yes into an emailed, clause-cited answer; drop any firm that answers native-only.
3. **10-28:** hard gate. A firm passes only with a clause-cited yes at evaluation and sim-funded covering the external engine, the exact route, cloud hosting, and full 6J short with micros under a cap ≥ 80. Silence counts as no.
4. **11-08 sitting:** if a venue passes, it is an input to the operator's decision under S1; any move then needs a firm ADR, tier rows, pre-flight, a pre-registered re-MC (full and FLOOR-HALF, at the venue's costs and evaluation clock), the adapter and drills, a separate live-spend GO, and an exit from Tradeify use first.

## 12. Questions to send

**Lucid (§1(c) approval request).** (1) Approval, separately for the LucidPro evaluation, LucidPro funded and LucidLive, of our own Python program on a US cloud server computing signals on completed 15-minute bars and sending market orders with attached stop and target to our Lucid Tradovate account via CrossTrade; about 2 round trips a day, intraday, not HFT. (2) Does the third-party-software ban cover an order-routing bridge when all strategy logic is ours? (3) Do the Terms of Use and LucidTest terms carry the same requirement (please send copies)? (4) Does "external or slow data feed" bar signals from a separately licensed CME feed, and may the account's data drive automated orders? (5) Any IP or region rule for the cloud host? (6) What advance testing is required, and does approval carry to LucidLive? (7) Breach on intraday net liquidation value or closing balance? (8) Does one 6J count as 10 micros against the 100-micro limit; LucidLive limits for 6J and MGC? (9) Current price of LucidPro 150K with DLL off.

**FundYourEdge.** (1) Is our own R|Protocol or R|API+ client, after Rithmic conformance, an "approved platform" under ToS §7.2 at evaluation and funded? (2) May it run fully automated on a US cloud server; any IP or device rule? (3) Will FYE enable API access on our Rithmic user ID; system, gateway, FCM ID, fees? (4) Is full 6J tradable and shortable on Prime 150K alongside micros under the 100-micro cap? (5) Please send the Funded Account Agreement. (6) Is the MLL tested only on the end-of-day balance; does the soft DLL liquidate? (7) May the included non-professional data via Rithmic drive our program? (8) Does the §7.3 audit require disclosing source code?

**FXIFY Futures.** (1) Per stage (Flex evaluation, Flex funded, Direct, live) with the clause: may our own program on a US cloud server place, modify and cancel orders on the FXIFY Tradovate account through CrossTrade, flagged as automated? (2) Does the EA FAQ's "across supported platforms" cover logic running outside those platforms via API or bridge? (3) If not, is the CrossTrade NT8 add-on on our own Windows VPS allowed? (4) Does GTC 5.4.1.2 "external or slow data feed" cover our separately licensed feed; is GTC v1.21 current? (5) Is full 6J tradable short, up to 8 alongside micros under 100 micros? (6) May an automated strategy hold positions with resting stops through scheduled releases, and enter on bars closing at release times? (7) Intraday or end-of-day MLL breach; is the 4:59 PM auto-close a violation? (8) Please send the funded agreement; any restriction on reusing the strategy in a personal account?

**Bulenox.** (1) Per stage (Qualification, Momentum, Master, Fast Track, live Funded) with the clause: may our own Python program on a rented cloud server trade via the Rithmic API? (2) Does "any third party algorithms must be approved" apply to our own program; what is the process, and will approved use avoid the "refuse to claim any profit" remedy? (3) What do "DTC Protocol Bridge API" and "automated discretional trading" mean? (4) Is API access enabled on Rithmic Paper Trading IDs; is the $100 fee per user ID or per account? (5) Fast Track Option 2: intraday breach on open P&L, and is the DLL a pause or a breach? (6) Is automation allowed on live Funded, and is declining a transition account-closing?

**Platforms.** CrossTrade: does "Link Demo" OAuth work with prop-issued Tradovate logins (Lucid, FXIFY), and does Tradovate permit it on evaluation accounts? Tradovate: does the prop-account API exclusion cover partner integrations? Rithmic: does the R|Protocol paper-demo exclusion cover paid prop paper IDs; can R|API+ log in to them after conformance; what does conformance check and cost?

**Topstep (only if a home-device route is acceptable).** Does an unattended home machine on a home ISP count as "your personal device"? May a cloud server with no order access compute signals that a home client executes? May ProjectX data drive the bot? Is API trading permitted on the XFA? Do protective stops fill during Tier-1 news windows?

**CME (#04738415).** Which licence row applies to a non-professional's own program using CME/CBOT/COMEX data from Rithmic, Tradovate or a prop platform to generate orders for (a) their own account and (b) a prop firm's simulated evaluation; how do Schedule 5 §3.3 and Subscriber Addendum §4.2 reconcile; does Information Policies §7.3 apply?
