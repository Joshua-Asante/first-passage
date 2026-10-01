# Feed: provider shortlist and written questions Q1–Q12 (DRAFT, for the operator to send)

**Status:** DRAFT, returned to the coordinator on 2026-10-01. This is a candidate list for **written questions only**. It does not select, rank for funding, contact or price a provider. Nothing here has been sent. **Sending any message is Joshua's act alone.**
**Authority:** Joshua's ruling of 2026-10-01, item 2 ("Feed: no-spend steps move earlier"), recorded in the deployment-checklist addendum "first-session simplification rulings" in [PR #580](https://github.com/Joshua-Asante/first-passage/pull/580) (branch `claude/first-session-cuts`, head `628a520`; not merged when this was written). Under that ruling, written provider questions Q1–Q12 and reads of published terms are **allowed now**, with no account, signup, credential or spend. Signup and spend stay behind D-feed (a)+(b) and CP-7.
**Serves (Rule 7), does not replace:**
- the question set, which is [H8 note §5](2026-09-27-feed-provider-neutral-preparation.md#5-provider-specific-facts-that-become-funding-decision-questions) (Q1–Q12, with Q2 split into Q2a and Q2b);
- the candidate record and decision rule in [Track A plan §3.2](../superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md#32-a9--production-feed-verification-record-and-funding-checkpoint-added-2026-09-11), which this note re-reads on 2026-10-01 and does not overrule;
- the funding decision, which is **CP-7** ([checklist §4](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#4-operator-checkpoints--where-approval-is-taken)).

**Not granted:** contact, account, signup, trial, credential, subscription or spend; a provider selection; TradingView in any feed role (`reference_tradingview_tos_display_only`: webhooks-as-feed are forbidden); any change to `emit_enabled`, `dry_run`, arming or orders. Databento stays retired (AGENTS.md data-source disposition).

---

## 0. Evidence standard: read this first

**No vendor page was opened in this session.** The cloud session's network policy blocked direct reads of `cmegroup.com`, `massive.com` and `developer.tastytrade.com` (`EGRESS_BLOCKED`). Every published-terms entry below therefore comes from one of two places:

- **[repo]**: the Track A plan's record of vendor pages that the Codex review read on 2026-09-11 (§3.2). That record is three weeks old.
- **[excerpt]**: a search-engine result excerpt for the cited URL, read on 2026-10-01. The page itself was not opened. An excerpt can be stale, paraphrased, or quoted from a third party, and it is marked that way where the URL is not the vendor's.

Treat every price, threshold and licence statement as **UNVERIFIED** until Joshua reads it on the vendor's own page or in a written reply. That is the existing "primary signup verification" rule (Track A plan readiness checkpoint 3). Where a cell says *not found*, it means not found in these excerpts. It does not mean the vendor does not publish it.

## 1. The cross-provider fact: CME's own non-display licence

Q1 is not only a vendor question. The symbols are CME Group products, and CME licenses **non-display use** (data consumed by software, not a screen) separately from display use. Our use is a headless service that turns real-time bars into automated trading decisions, which is non-display use.

| Published fact (all **[excerpt]**, UNVERIFIED) | Source |
|---|---|
| CME's non-display licences come in three categories. **Category A, Automated Trading,** has three sub-categories covering automated and semi-automated trading | [CME data licensing policy guidelines and non-display FAQ (PDF)](https://www.cmegroup.com/market-data/distributor/files/cme-group-data-licensing-policy-guidelines-and-non-display-licensing-faq.pdf) |
| An automated trading system is "any system or computer software … that generates and/or routes orders electronically with no, or only de minimis, human action" | same |
| "Any entity that utilizes a Semi-Automated Trading System (direct from CME or indirect via a Data Provider) requires an ILA for Non-Display Use" | same |
| The January 2026 fee list shows **User Non-Display Category A $457** and **Managed User Non-Display Category A $208**. The billing unit (per month? per licensee? per exchange?) is not in the excerpt. A second excerpt says "$670 per exchange" for Category A; the two do not reconcile | [CME fee list, January 2026 (PDF)](https://www.cmegroup.com/market-data/files/january-2026-market-data-fee-list.pdf) |
| Third-party and forum excerpts say real-time data through the Tradovate API requires the subscriber to sign the CME Information License Agreement (ILA), at a reported $290–$500 per month | [NinjaTrader vendor support: Tradovate API Access](https://vendor-support.ninjatrader.com/s/article/Tradovate-API-Access); [Tradovate forum](https://community.tradovate.com/t/is-cme-sub-vendor-requirement-for-api-access-is-290-per-month/6215) (forum, not terms) |
| Interactive Brokers describes API use as "off-platform", which "typically" has a cost, and offers non-display options for API trading applications | [IBKR market data pricing](https://www.interactivebrokers.com/en/pricing/market-data-pricing.php) |

**Consequence.** For any candidate, the all-in monthly cost may be the vendor's price **plus** a CME non-display licence that the subscriber holds directly. One CME licence could cover all of the vendor's routes, or each vendor could require its own. Only CME can say. So the shortlist adds one **licensor** message (§3.0) to the vendor messages. That message is the cheapest single question, because its answer changes the cost of every candidate.

The non-display question also interacts with where the orders go. The orders would be placed in a third-party prop-firm evaluation account at a different broker, through the rail. Whether that changes non-professional status or the licence category is a fact only CME and each vendor can answer. Whether to disclose it is the operator's choice (decision D-Q2, §5). If it is omitted, Q1 stays unresolved until CME and the provider confirm the actual use (§5, D-Q2).

## 2. Shortlist

**Fit criteria (from the owners):** real-time data for all four symbols on three exchanges (6J and MNQ on CME, MYM on CBOT, MGC on COMEX; [Track A plan §3.2](../superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md#32-a9--production-feed-verification-record-and-funding-checkpoint-added-2026-09-11) entitlement table); a programmatic stream a headless Linux service can hold for weeks without a UI; licensing for automated, non-display decisions; delivery that can be built into 15-minute bars stamped at bar open in UTC ([draft spec §4](../spec/2026-09-27-cme-execution-feed-equivalence-test-DRAFT.md#4--bar-construction-frozen-with-the-spec)); and preferably a credential that cannot place orders (the Track A credential-boundary correction).

| # | Candidate | Credential boundary | Why it is on the list | Main open fact | Disposition for questions |
|---|---|---|---|---|---|
| P1 | **Massive** (formerly Polygon.io), Futures **Advanced** (individual) | Data-only API key (vendor is not a broker) | Real-time CME/CBOT/NYMEX/COMEX over WebSocket, with per-second and per-minute aggregates (**[excerpt]**) | Whether an individual plan covers automated non-display trading decisions under CME's licence; whether CME licence fees are extra | **Send.** Safest secret boundary |
| P2 | **tastytrade** Open API / DXLink | Brokerage; full read/write API **[repo]** | Track A's "best challenger": WebSocket candle events for CME futures **[repo]** | Data-only scope; unattended token renewal; whether data may drive orders at another broker | **Send** |
| P3 | **Interactive Brokers**, screened as two variants: **P3a** TWS API through IB Gateway, and **P3b** Client Portal Web API. Each is a separate row in §4 (Codex review on #583) | Brokerage; order-capable **[repo]** | Low non-professional exchange fees; explicit non-display options for API use (**[excerpt]**) | The always-on gateway, and the non-display cost for API use | **Send** |
| P4 | **Ironbeam** API (REST/WebSocket) | Brokerage; order-capable **[repo]** | WebSocket trade, tick, time and volume bars; documented reconnect rule (**[excerpt]**, **[repo]**) | API fee without trading activity; bar-close semantics; read-only restriction | **Send** |
| P5 | **Rithmic** R\|Protocol API, through a clearing broker (FCM) | Brokerage-routed; order-capable | Server-side time bars over WebSocket; widely used for futures automation (**[excerpt]**) | Conformance testing before production access; the FCM's own terms | **Send**, as a two-stage screen (§3.5): first Rithmic at protocol level, then one named FCM. The rejection rule applies to the combined answers |
| P6 | **Tradovate** API, on a personal live data-only account (option A′) | Brokerage; order-capable **[repo]** | Already the operator's shortlisted option A′ **[repo]** | Real-time API data reportedly needs the subscriber's own CME ILA (**[excerpt]**, third-party) | **Send** |
| P7 | **CME Group direct**, screened as two variants: **P7a** Market Data over WebSocket API, and **P7b** Smart Stream on GCP. Each is a separate row in §4, with the full Q1–Q12 screen applied to each (Codex review on #583) | Data-only | The licensor's own feed. Usage-priced from $0.50/GB "plus applicable ILA fees" (**[excerpt]**) | Whether an individual can subscribe at all; minimum commitments | **RFI only**, inside the §3.0 licensing message |

**Excluded, with the owner of each exclusion:**
- **Databento:** retired by the operator on 2026-09-10 ([retirement record](../adr/2026-07-10-databento-research-stack.md#addendum-2026-09-10---operator-retirement-of-databento)). Only the operator can reverse that.
- **TradingView, in any feed role:** forbidden (`reference_tradingview_tos_display_only`; AGENTS.md: TV is research/export only).
- **TradeStation:** "dominated", because of a $10,000 funded minimum for an API key **[repo]**.
- **IQFeed, CQG, Barchart, dxFeed direct:** "no evidence they beat the shortlist" **[repo]**. They were not re-researched here. They are the next set to question if **no** shortlisted candidate meets the complete funding requirements: Q1/Q2a/Q3/Q5 unambiguous, plus a usable bar or trade stream, permitted storage and cloud use, and the **ceiling-bearing total** (§4: every non-exempt field summed with existing commitments) within the ceiling. Failing only the four mandatory checks is not required for this (Codex review on #583).

The order of P1–P7 is not a ranking. Track A's decision rule, which prefers no greater secret authority at lower capital or run-rate, applies at CP-7 to the **answers**. It does not apply to this list.

## 3. Messages, ready to send

**How to use these.** Each block is a complete message. Square brackets mark the operator's choices. Every block asks Q1–Q12 in the same order, so the answers line up across providers. Where published terms already appear to answer a question, the question asks the vendor to **confirm** that reading in writing, and the URL is given. Do not include account identifiers or P&L. **The rejection rule is unchanged:** reject an answer that leaves licensing (Q1), all-four-symbol coverage (Q2a), the ability to disable order actions (Q3) or unattended authentication (Q5) ambiguous ([Track A plan](../superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md#32-a9--production-feed-verification-record-and-funding-checkpoint-added-2026-09-11), "Reject any answer …"). An ambiguous Q2b is an input to the funding decision, not a disqualification ([H8 note §5](2026-09-27-feed-provider-neutral-preparation.md#5-provider-specific-facts-that-become-funding-decision-questions)).

**Common context paragraph** (paste at the top of every message):

> I am an individual, non-professional trader. I am evaluating real-time CME Group futures data for a headless, automated system, before opening any account. The instruments are the front dated contracts of **6J** (CME Japanese yen), **MNQ** (CME Micro E-mini Nasdaq-100), **MYM** (CBOT Micro E-mini Dow) and **MGC** (COMEX Micro Gold). A Linux service on a cloud server would build 15-minute bars from the data, without any screen, and make automated trading decisions from them. The data would not be displayed to anyone or redistributed. [Optional, see D-Q2: The resulting orders are placed in a proprietary-trading-firm evaluation account held at a different broker.] I would be grateful for written answers to the questions below, with links to the governing terms where possible.

### 3.0 CME Group: market-data licensing (licensor; covers P7)

Send to CME Group's market data licensing contact (the Data Services portal, or the contact named on the non-display FAQ).

> [Common context paragraph]
>
> 1. **(Q1)** Does this use require a **Non-Display (Category A, automated trading)** licence held by me directly, or can it be covered by a data vendor's or broker's licence? Is there a non-professional or individual route for Category A, and which sub-category applies? [If D-Q2 is "disclose": Does placing the orders in a third-party firm's evaluation account, rather than my own funded account, change the category or my non-professional status?]
> 2. **(Q2a)** Does one licence cover CME, CBOT and COMEX, or is each exchange licensed separately? **For the direct feed:** do your Market Data over WebSocket API and Smart Stream on GCP each deliver **real-time** data for all four of 6J, MNQ (CME), MYM (CBOT) and MGC (COMEX), and which entitlement does each need?
> 3. **(Q2b)** What are the current monthly fees, including the billing unit (per licensee, per exchange, per device)? Your January 2026 fee list appears to show User Non-Display Category A at $457 and Managed User Non-Display Category A at $208 ([fee list](https://www.cmegroup.com/market-data/files/january-2026-market-data-fee-list.pdf)). Please confirm which applies, and whether a "$670 per exchange" figure I have seen is current. Are there minimum terms, setup fees or annual audits?
> **Questions 4 to 13 below (Q3–Q12): please answer separately for (a) Market Data over WebSocket API and (b) Smart Stream on GCP.** The two products may differ in authentication, storage rights, replay, symbology, latency and session handling.
>
> 4. **(Q3, for the direct feed)** Your Market Data over WebSocket API and Smart Stream on GCP are data-only. Can an individual subscribe to either, and what are the minimum commitments? **For each product separately**, what is the all-in monthly cost for these four products: delivery or usage charges, licence fees, and any one-time setup charge? Smart Stream appears to be priced "as low as $0.50/GB plus applicable ILA fees" ([page](https://www.cmegroup.com/market-data/real-time-futures-and-options-data-api.html)).
> 5. **(Q4)** Please answer this question **separately for each direct product**, the Market Data over WebSocket API and Smart Stream on GCP. Are 1-minute bars or only trades published? Are exchange timestamps included, and are bars stamped at the open or the close? **Volume:** does each bar carry exchange-reported **trade volume** (contracts traded in the bar)? Is that volume ever synthetic, estimated or quote-derived, and is it final when the bar is delivered, or revised later? **If only trades are published:** does each trade message carry the exchange-reported **contract quantity**? How are corrected, busted or cancelled trades signalled, and how should they change a bar's volume?
> 6. **(Q5)** Can authentication run unattended for weeks without interactive login or MFA? What session, connection and concurrent-subscription limits apply, and can one connection receive all four products at once?
> 7. **(Q6)** May derived bars and the original messages be stored privately for audit, on a cloud server?
> 8. **(Q7)** How are corrections and replays after a reconnect delivered? Are sequence numbers provided?
> 9. **(Q8)** Are bars (if any) published for intervals with no trades? If so, how is such a bar marked, so that a client can tell it apart from a trade-evidenced bar? **Exchange halts:** how is an exchange trading halt inside a session represented: as an omission, as a flagged bar, or as a status message?
> 10. **(Q9)** How are dated contracts identified, and is a continuous or front-month symbol offered? What is its roll rule?
> 11. **(Q10)** What is the typical delivery latency, and what maintenance windows fall inside the Sunday–Friday 18:00–17:00 ET session?
> 12. **(Q11)** What historical depth is available for these products, and at what cost?
> 13. **(Q12)** How are DST changes and holiday early closes reflected in the session data?

### 3.1 P1: Massive, Futures Advanced (individual plan)

**What published terms already appear to answer** (all **[excerpt]**, UNVERIFIED):

| Q | Reading | Source |
|---|---|---|
| Q1 | Individual plans are "licensed for personal and non-professional use", covering "your own research, your own scripts, your own trading". CME non-display coverage: not found | [Massive KB: which plan do I need](https://massive.com/knowledge-base/article/which-plan-do-i-need-to-show-massive-data-in-my-app); [understanding professional status](https://massive.com/blog/understanding-professional-status) |
| Q2a | Real-time and historical data for CME, CBOT, NYMEX and COMEX | [massive.com/futures](https://massive.com/futures) |
| Q2b | Starter $29/month and Developer $79/month (10-minute delayed); **Advanced $199/month, real-time**; business plans from $999/month. Whether exchange or CME licence fees are extra: not found | [massive.com/futures](https://massive.com/futures) |
| Q3 | Data-only API key **[repo]** (Track A: "data-only secret") | Track A plan §3.2 |
| Q4 | WebSocket per-second and per-minute aggregates; trades and quotes streams. Bar stamp (open or close) and exchange timestamps: not found | [per-minute aggregates](https://massive.com/docs/websocket/futures/aggregates-per-minute); [per-second](https://massive.com/docs/websocket/futures/aggregates-per-second) |
| Q11 | Advanced: 5 years of history; minute-aggregate flat files per exchange | [massive.com/futures](https://massive.com/futures); [flat files, CME](https://massive.com/docs/flat-files/futures/minute-aggregates/cme) |
| Q5–Q10, Q12 | Not found | — |

> [Common context paragraph]
>
> 1. **(Q1)** Your knowledge base says individual plans cover "your own scripts, your own trading". Does the individual **Futures Advanced** plan permit a headless program to use real-time data for **automated trading decisions** (non-display use)? Does your CME licence cover that use, or must I hold a CME Non-Display (Category A) licence myself? [If D-Q2 is "disclose": Does placing the orders in a third-party firm's evaluation account at another broker change the plan or my status?]
> 2. **(Q2a)** Does Futures Advanced include **real-time** data for all four of 6J and MNQ (CME), MYM (CBOT) and MGC (COMEX), with no further exchange entitlement?
> 3. **(Q2b)** Is $199/month the all-in monthly cost for this use, including exchange and CME licence fees? Are there setup fees, minimum terms or cancellation terms?
> 4. **(Q3)** Please confirm that the API key gives data access only, with no order or account capability.
> 5. **(Q4)** For the per-minute aggregate WebSocket stream: is the timestamp the bar's **start or end**, in what zone or epoch unit, and is it exchange time or your aggregation time? Is a minute bar ever revised after it is published? **Volume:** does each bar carry exchange-reported **trade volume** (contracts traded in the bar)? Is that volume ever synthetic, estimated or quote-derived, and is it final when the bar is delivered, or revised later?
> 6. **(Q5)** Can one API key hold a WebSocket connection for weeks unattended, with no interactive login? How many concurrent connections and subscribed symbols does the plan allow? Can all four products (6J, MNQ, MYM, MGC) stream at the same time on one session?
> 7. **(Q6)** May I run the client on a cloud server, and store the raw messages and derived bars privately for audit?
> 8. **(Q7)** After a disconnect and reconnect, are missed minute bars replayed? Are corrections flagged? Do messages carry sequence numbers?
> 9. **(Q8)** Is a minute aggregate published for a minute with **no trades**? If so, how is it marked? **Exchange halts:** how is an exchange trading halt inside a session represented: as an omission, as a flagged bar, or as a status message?
> 10. **(Q9)** How are dated contracts named (for example, the March MNQ contract)? Do you offer a continuous or front-month symbol, and what is its roll rule?
> 11. **(Q10)** How long after the minute closes is the aggregate typically delivered? Are there maintenance windows inside the Sunday–Friday 18:00–17:00 ET session?
> 12. **(Q11)** Please confirm the historical depth on Futures Advanced for these four products.
> 13. **(Q12)** How do the aggregates and session data handle DST changes and holiday early closes?

### 3.2 P2: tastytrade Open API / DXLink

**What published terms already appear to answer:**

| Q | Reading | Source |
|---|---|---|
| Q1 | Non-professional status is self-certified under a CME subscriber agreement **[excerpt]**. Headless or automated non-display use: not found | [tastytrade CME subscriber agreement (PDF)](https://assets.tastyworks.com/production/documents/cme_market_data_subscriber_agreement.pdf) |
| Q2a | DXLink streams CME futures **[repo]**. A non-professional "CME Group bundle" covering CME, CBOT, NYMEX and COMEX **[excerpt; the excerpt did not identify its source page]** | [streaming guide](https://developer.tastytrade.com/docs/guides/stream-market-data/) |
| Q2b | API access included with the account; live data "once an account is funded with any amount"; professional futures data $480/month; non-professional CME bundle $4.65/month L1 **[excerpt; partly third-party]** | [professional data fees](https://support.tastytrade.com/support/s/solutions/articles/43000435398); [tastytrade.com/api](https://tastytrade.com/api/) |
| Q3 | Full read/write API **[repo]**. Data-only scope: not found | [tastytrade.com/api](https://tastytrade.com/api/) |
| Q4 | Candle events over DXLink **[repo]** | [streaming guide](https://developer.tastytrade.com/docs/guides/stream-market-data/) |
| Q5 | 15-minute OAuth access tokens; 24-hour quote token; "fully onboarded tastytrade customer" required **[repo]** | same |
| Q6–Q12 | Not found | — |

> [Common context paragraph]
>
> 1. **(Q1)** May a non-professional customer use real-time 6J, MNQ, MYM and MGC data from the Open API (DXLink) in a headless program that makes automated trading decisions? **May those decisions drive orders at a different broker?** Does your CME licence cover this non-display use, or must I hold a CME Non-Display (Category A) licence myself? [If D-Q2 is "disclose": the other broker account is a proprietary-trading-firm evaluation account.]
> 2. **(Q2a)** Does the non-professional futures data entitlement include **real-time** CME, CBOT and COMEX data for all four products through the API, not only in your platforms?
> 3. **(Q2b)** What is the all-in monthly cost of API access plus that data for a non-professional? What minimum balance, deposit, inactivity fee and withdrawal terms apply, and is any activity requirement attached to API or data access? Are there any **one-time, non-refundable** charges (setup, activation, onboarding)?
> 4. **(Q3)** Is there an OAuth scope or API credential that **cannot place, modify or cancel orders**? If not, can order permission be disabled at the account or API-user level?
> 5. **(Q4)** For DXLink candle events on futures: are 1-minute candles supported live? Is the candle time the **start** of the period, in UTC milliseconds? Are exchange timestamps carried? Can a live candle be updated after its period ends? **Volume:** does each bar carry exchange-reported **trade volume** (contracts traded in the bar)? Is that volume ever synthetic, estimated or quote-derived, and is it final when the bar is delivered, or revised later?
> 6. **(Q5)** Access tokens appear to last 15 minutes and the quote token 24 hours. Can both be renewed **unattended for weeks** (no UI, MFA prompt or daily login)? What session or connection limits apply? Can all four products (6J, MNQ, MYM, MGC) stream at the same time on one session?
> 7. **(Q6)** Are cloud or VPS use, and private storage of raw messages and derived bars for audit, permitted under the subscriber agreement?
> 8. **(Q7)** After a reconnect, can missed candles be backfilled? Are revised candles flagged? Are there sequence identifiers?
> 9. **(Q8)** Is a candle published for an interval with **no trades**? If so, how is it marked? **Exchange halts:** how is an exchange trading halt inside a session represented: as an omission, as a flagged bar, or as a status message?
> 10. **(Q9)** What symbol format identifies dated futures contracts (for example the March MNQ)? Is a continuous symbol offered, and with what roll rule?
> 11. **(Q10)** What is the typical delay from period end to candle delivery? Are there maintenance windows inside the Sunday–Friday 18:00–17:00 ET session?
> 12. **(Q11)** How much historical candle data is available through the API for these products, and at what cost?
> 13. **(Q12)** How are DST changes and holiday early closes reflected in candle and session data?

### 3.3 P3: Interactive Brokers (TWS / Client Portal API)

**What published terms already appear to answer:**

| Q | Reading | Source |
|---|---|---|
| Q1 | API use is "off-platform", and exchanges "typically" charge for it; non-display options exist for API trading applications **[excerpt]** | [market data pricing](https://www.interactivebrokers.com/en/pricing/market-data-pricing.php) |
| Q2a | CME, CBOT, COMEX and NYMEX top-of-book **[repo]** | same |
| Q2b | $500 minimum equity for data; $10 base + $5 streaming, non-professional, as displayed on 2026-09-11 **[repo]**. A 2026-10-01 excerpt shows "CME Real-Time (L1)" for non-professionals at USD 1.55/month; whether CBOT and COMEX are separate lines is not in the excerpt **[excerpt]** | same |
| Q3 | Order-capable **[repo]**. Read-only setting: not found | — |
| Q5 | Requires an always-on Client Portal or TWS gateway **[repo]** | — |
| Q4, Q6–Q12 | Not found | — |

> [Common context paragraph]
>
> **Please answer every question below separately for (a) the TWS API through IB Gateway and (b) the Client Portal Web API.** The two paths may differ in authentication, bar delivery, limits and permissions.
>
> 1. **(Q1)** I would use real-time 6J, MNQ, MYM and MGC data through your API in a headless program that makes automated trading decisions. **May those decisions drive orders at a different broker?** Which non-display subscription applies to this "off-platform" use, and does it replace or add to a CME Non-Display (Category A) licence held by me? [If D-Q2 is "disclose": the other account is a proprietary-trading-firm evaluation account.]
> 2. **(Q2a)** Which exact subscriptions give real-time API data for CME (6J, MNQ), CBOT (MYM) and COMEX (MGC)?
> 3. **(Q2b)** What is the all-in monthly cost of those subscriptions plus any non-display or API fee, for a non-professional? Is the minimum equity for market data still $500? What inactivity, deposit and withdrawal terms apply? Are there any **one-time, non-refundable** charges (setup, activation, onboarding)?
> 4. **(Q3)** Can order permission be disabled at the account or API-user level, or is there a read-only API setting that the server enforces?
> 5. **(Q4)** Do you stream completed 1-minute bars (for example, real-time bars or keep-up-to-date historical bars) with exchange timestamps? Is the bar time the start of the bar, and in which time zone or UTC offset is it expressed (for example UTC epoch, exchange-local or account-local time)? Can a bar be revised after delivery? **Volume:** does each bar carry exchange-reported **trade volume** (contracts traded in the bar)? Is that volume ever synthetic, estimated or quote-derived, and is it final when the bar is delivered, or revised later?
> 6. **(Q5)** Can the gateway authenticate and stay connected **unattended for weeks** without a daily login, MFA prompt or desktop session? What session, connection, market-data-line and concurrent-subscription limits apply? Can all four products (6J, MNQ, MYM, MGC) stream at the same time on one session?
> 7. **(Q6)** Is running the gateway on a cloud server permitted, and may raw messages and derived bars be stored privately for audit?
> 8. **(Q7)** After a reconnect, are missed bars replayed? Are corrections flagged? Are sequence identifiers provided?
> 9. **(Q8)** Is a bar published for an interval with no trades? If so, how is it marked? **Exchange halts:** how is an exchange trading halt inside a session represented: as an omission, as a flagged bar, or as a status message?
> 10. **(Q9)** How are dated futures contracts identified in the API, and is a continuous contract offered, with what roll rule?
> 11. **(Q10)** What is the typical delay from bar end to delivery? What maintenance or reset windows fall inside the Sunday–Friday 18:00–17:00 ET session?
> 12. **(Q11)** What historical bar depth is available through the API for these products, and with what pacing limits?
> 13. **(Q12)** How are DST changes and holiday early closes reflected in trading-hours and bar data?

### 3.4 P4: Ironbeam API

**What published terms already appear to answer** (**[excerpt]** unless marked):

| Q | Reading | Source |
|---|---|---|
| Q2b | API access is free with at least 5 contracts traded per month; otherwise "starting at $249/month". Level 1 and Level 2 real-time are "free for non-professional traders" (whether through the API or platforms only: not stated in the excerpt) | [API access](https://www.ironbeam.com/knowledge-base/ironbeam-api-access/); [platform market data fees](https://www.ironbeam.com/knowledge-base/ironbeam-platform-market-data-fees/) |
| Q3 | Order-capable; read-only restriction unknown **[repo]** | [ironbeam.com/api](https://www.ironbeam.com/api/) |
| Q4 | Trade bars, tick bars, time bars and volume bars over one WebSocket. Bar-close semantics unknown **[repo]** | [subscribing over WebSockets](https://www.ironbeam.com/how-to-subscribe-real-time-market-data-ironbeam-websockets/) |
| Q5 | Bearer authentication; documented reconnect rule **[repo]** | [API reference](https://docs.ironbeamapi.com/) |
| Q1, Q2a, Q6–Q12 | Not found | — |

> [Common context paragraph]
>
> 1. **(Q1)** May a non-professional customer use real-time data from your API in a headless program that makes automated trading decisions? **May those decisions drive orders at a different broker?** Does your licence cover CME non-display use, or must I hold a CME Non-Display (Category A) licence myself? [If D-Q2 is "disclose": the other account is a proprietary-trading-firm evaluation account.]
> 2. **(Q2a)** Does API data include **real-time** CME (6J, MNQ), CBOT (MYM) and COMEX (MGC) for a non-professional?
> 3. **(Q2b)** Your page says API access is free with 5 or more contracts traded per month and otherwise starts at $249/month. For a data-only use with no trading at Ironbeam, what is the all-in monthly cost? Are non-professional real-time data fees free through the API too? What **required opening deposit**, minimum balance, inactivity and withdrawal terms apply? Are there any **one-time, non-refundable** charges (setup, activation, onboarding)?
> 4. **(Q3)** Is there an API credential that cannot place, modify or cancel orders, or can order permission be disabled at the account level?
> 5. **(Q4)** For WebSocket time bars at 1 or 15 minutes: is the bar timestamp the start or the end, in what zone? Is the bar emitted once at close, or updated in place while it forms? Are exchange timestamps included? **Volume:** does each bar carry exchange-reported **trade volume** (contracts traded in the bar)? Is that volume ever synthetic, estimated or quote-derived, and is it final when the bar is delivered, or revised later?
> 6. **(Q5)** Can bearer-token authentication be renewed unattended for weeks, with no UI or MFA? What session and subscription limits apply? Can all four products (6J, MNQ, MYM, MGC) stream at the same time on one session?
> 7. **(Q6)** Are cloud or VPS use, and private storage of raw messages and derived bars for audit, permitted?
> 8. **(Q7)** After a reconnect, are missed bars replayed? Are corrections flagged? Are sequence identifiers provided?
> 9. **(Q8)** Is a time bar emitted for an interval with no trades? If so, how is it marked? **Exchange halts:** how is an exchange trading halt inside a session represented: as an omission, as a flagged bar, or as a status message?
> 10. **(Q9)** How are dated contracts identified, and is a continuous symbol offered, with what roll rule?
> 11. **(Q10)** What is the typical delay from bar end to delivery? Are there maintenance windows inside the Sunday–Friday 18:00–17:00 ET session?
> 12. **(Q11)** What historical bar depth is available through the API, and at what cost?
> 13. **(Q12)** How are DST changes and holiday early closes reflected in session and bar data?

### 3.5 P5: Rithmic (R|Protocol API)

**Two-stage screen** (Codex review on #583). Rithmic data comes through a clearing broker (FCM), so Rithmic may properly defer licensing, entitlement, order-restriction, authentication or storage questions to the FCM.
- **Stage 1 (this message).** Rithmic answers what it controls. Any answer that defers to the FCM is recorded as **DEFERRED-TO-FCM**, not as ambiguous, and the rejection rule is not applied to those items at stage 1.
- **Stage 2.** The same common context and Q1–Q12 go to **one named FCM**, chosen by the operator from Rithmic's stage-1 answer about which FCMs offer data-only users. For the FCM, Q2b also asks for its **capital and liquidity terms**: required deposit, minimum account balance, inactivity fees, and withdrawal constraints. Those answers fill the held-capital field (§4) (Codex review on #583).
- **The rejection rule (§3)** is applied to the stage-1 and stage-2 answers combined, before CP-7.

**What published terms already appear to answer** (all **[excerpt]**, several from brokers rather than Rithmic):

| Q | Reading | Source |
|---|---|---|
| Q2b | Reported API access around $20/month plus $0.10 per contract; some brokers charge a $100 monthly minimum per API user ID. Non-professional L1 data from $3.00 per exchange per month; CME Globex L2 bundle $41/month (broker pages, not Rithmic terms) | [Ironbeam: Rithmic market data fees](https://www.ironbeam.com/knowledge-base/rithmic-market-data-fees/); [EdgeClear: market data costs](https://support.edgeclear.com/portal/en/kb/articles/market-data-costs) |
| Q4 | R\|Protocol (WebSocket plus protocol buffers) provides server-side "custom time, tick, volume, and price range bars" | [rithmic.com/apis](https://www.rithmic.com/apis) |
| Q5 | **Conformance testing is required before production access.** Development runs against the Rithmic Test system | [rithmic.com/apis](https://www.rithmic.com/apis); [exchange simulator](https://www.rithmic.com/products/exchange-simulator) |
| Q1, Q2a, Q3, Q6–Q12 | Not found | — |

> [Common context paragraph]
>
> 1. **(Q1)** May a non-professional user consume real-time data through R|Protocol in a headless program that makes automated trading decisions, with **no orders sent through Rithmic**? Does that use need a CME Non-Display (Category A) licence held by me? [If D-Q2 is "disclose": the orders go to a proprietary-trading-firm evaluation account at another broker.]
> 2. **(Q2a)** Can one user ID receive real-time CME, CBOT and COMEX data for all four products? Which clearing firms offer a **data-only** R|Protocol user?
> 3. **(Q2b)** What is the all-in monthly cost for a data-only user: API or connection fee, per-exchange data fees and any minimum, and what does the clearing firm add? Are there any **one-time, non-refundable** charges (setup, activation, onboarding)?
> 4. **(Q3)** Can a user ID be configured, on the server side, so that it cannot place, modify or cancel orders?
> 5. **(Q4)** For server-side time bars at 1 or 15 minutes: is the bar stamped at the start or the end, in what time base? Is a bar sent once at close, or updated while it forms? Are exchange timestamps included? **Volume:** does each bar carry exchange-reported **trade volume** (contracts traded in the bar)? Is that volume ever synthetic, estimated or quote-derived, and is it final when the bar is delivered, or revised later?
> 6. **(Q5)** Is conformance testing required for a **market-data-only** application? Can login and session renewal run unattended for weeks? What connection and symbol limits apply? Can all four products (6J, MNQ, MYM, MGC) stream at the same time on one session?
> 7. **(Q6)** Are cloud or VPS use, and private storage of raw messages and derived bars for audit, permitted?
> 8. **(Q7)** After a reconnect, are missed bars replayed? Are corrections flagged? Are sequence numbers provided?
> 9. **(Q8)** Is a time bar emitted for an interval with no trades? If so, how is it marked? **Exchange halts:** how is an exchange trading halt inside a session represented: as an omission, as a flagged bar, or as a status message?
> 10. **(Q9)** How are dated contracts identified, and is a continuous or front-month symbol offered, with what roll rule?
> 11. **(Q10)** What is the typical delay from bar end to delivery? What maintenance windows fall inside the Sunday–Friday 18:00–17:00 ET session?
> 12. **(Q11)** What historical bar depth is available through R|Protocol, and at what cost?
> 13. **(Q12)** How are DST changes and holiday early closes reflected in session and bar data?

### 3.6 P6: Tradovate API, personal live data-only account (option A′)

**Keep this separate from the eval.** The feed account would be a personal account that is never linked to the broker bridge (Track A readiness checkpoint 5). It is not the incumbent evaluation account.

**What published terms already appear to answer** (**[excerpt]** unless marked):

| Q | Reading | Source |
|---|---|---|
| Q1 | Real-time data through the API reportedly requires the subscriber to become a CME sub-vendor by signing the CME ILA. The ILA is not needed for order-only API use | [NinjaTrader vendor support: Tradovate API Access](https://vendor-support.ninjatrader.com/s/article/Tradovate-API-Access); [forum thread](https://community.tradovate.com/t/how-to-do-the-cme-vendor-registration-for-market-data-access-via-websocket/11320) |
| Q2b | API add-on $25/month, "does not provide access to real-time market data"; a CME licence reported at $290–$500/month on top (forum and third-party). Non-professional data rates are on a support page | same; [non-professional monthly data rates](https://support.tradovate.com/s/article/Non-Professional-Monthly-Data-Rates-Tradovate?language=en_US) |
| Q3 | Order-capable **[repo]** | Track A plan §3.2 |
| Q2a, Q4–Q12 | Not found | — |

> [Common context paragraph]
>
> 1. **(Q1)** On a personal live account, may I stream real-time 6J, MNQ, MYM and MGC data through your API into a headless program that makes automated trading decisions? Your support material appears to say this requires me to sign the CME Information License Agreement as a sub-vendor ([article](https://vendor-support.ninjatrader.com/s/article/Tradovate-API-Access)). Please confirm that, and which CME licence category applies. [If D-Q2 is "disclose": the orders go to a proprietary-trading-firm evaluation account, which is a separate account.]
> 2. **(Q2a)** Does API data cover real-time CME, CBOT and COMEX for all four products, once the CME licence is in place?
> 3. **(Q2b)** What is the all-in monthly cost: the API add-on, data subscriptions and the CME licence? What **required opening deposit**, minimum balance, inactivity and withdrawal terms apply to a live account used only for data? Are there any **one-time, non-refundable** charges (setup, activation, onboarding)?
> 4. **(Q3)** Can an API key or the account itself be restricted so that it cannot place, modify or cancel orders?
> 5. **(Q4)** Does the API publish completed 1-minute bars (chart subscription) with exchange timestamps? Is the bar time the start of the bar, and in UTC? Can a bar be revised after the period ends? **Volume:** does each bar carry exchange-reported **trade volume** (contracts traded in the bar)? Is that volume ever synthetic, estimated or quote-derived, and is it final when the bar is delivered, or revised later?
> 6. **(Q5)** Can token renewal run unattended for weeks, with no UI, MFA prompt or daily login? What session and connection limits apply? Can all four products (6J, MNQ, MYM, MGC) stream at the same time on one session?
> 7. **(Q6)** Are cloud or VPS use, and private storage of raw messages and derived bars for audit, permitted?
> 8. **(Q7)** After a reconnect, are missed bars replayed? Are corrections flagged? Are sequence identifiers provided?
> 9. **(Q8)** Is a bar published for an interval with no trades? If so, how is it marked? **Exchange halts:** how is an exchange trading halt inside a session represented: as an omission, as a flagged bar, or as a status message?
> 10. **(Q9)** How are dated contracts named, and is a continuous symbol offered, with what roll rule?
> 11. **(Q10)** What is the typical delay from bar end to delivery? What maintenance windows fall inside the Sunday–Friday 18:00–17:00 ET session?
> 12. **(Q11)** What historical bar depth is available through the API, and at what cost?
> 13. **(Q12)** How are DST changes and holiday early closes reflected in session and bar data?

## 4. Recording the answers

- Keep each reply's original privately, and record its SHA-256 beside the answer, as the drill plan does for venue replies.
- Fill one row per provider and question with **answer · source (reply or page, with date) · verified by the operator (yes/no)**.
- Apply the rejection rule (§3) before comparing costs.
- Costs are compared in **three separate fields**, never summed: (a) **recurring monthly cost**, split into **(a1)** data-feed subscription fees and CME market-data licence fees, which are exempt under D-Q1, and **(a2)** every other recurring charge, such as account, platform, inactivity or API-access fees not billed as a data subscription (Codex review on #583); (b) **held capital**, meaning refundable deposits and minimum balances required for data access; and (c) **one-time non-refundable charges**, such as setup, activation or onboarding fees (Codex review on #583). This follows Track A's decision rule, which weighs "lower capital **or** run-rate" separately (Codex review on #583). **Subscription and CME licence fees are outside** the $700 ceiling (D-Q1, ruled). **Refundable deposits and minimum balances stay under the cap** until Joshua rules otherwise (D-Q5). One-time charges also stay under the cap until ruled (D-Q6): the D-Q1 exemption covers only subscription and licence fees. **Ceiling check:** the three fields stay separate for ranking, but the $700 check **sums every non-exempt field** with the ceiling's existing commitments. Today that means (a2) over the ceiling's 3-month run-rate horizon, plus (b), plus (c), until D-Q5, D-Q6 and D-Q7 are ruled. Two items that each pass alone can therefore still fail together, for example a $500 deposit plus a $300 onboarding fee (Codex review on #583). Feed costs are recorded outside the ceiling tally, and every purchase stays an operator act at CP-7.
- The answers feed **CP-7**. They select nothing, and they open no account.

## 5. Decisions needed from Joshua

| # | Decision | Why it matters now | Options |
|---|---|---|---|
| **D-Q1** | **RULED 2026-10-01, narrowed the same day:** feed **subscription fees and CME market-data licence fees** do **not** count toward the $700 ceiling | Joshua, 2026-10-01: "feed costs don't count toward the $700 ceiling". It is recorded as the rail GO ADR addendum "production data-feed costs are outside the $700 ceiling" in [PR #580](https://github.com/Joshua-Asante/first-passage/pull/580) (`473533c`). Joshua's same-day clarification (`3474ab2`) limits the exemption to **feed costs only**: subscription and licence fees, which are also outside the projected spend that revert trigger (b) measures. **Refundable deposits and minimum balances stay under the cap**; the A′ parked deposit is the addendum's own example. That part is open as D-Q5. *Superseded question (kept for the record):* whether feed costs counted, given the ceiling "$700 all-in to first live fill (eval + 3 months run-rate)" and F-4's drill-only ruling. Feed signup and spend still need D-feed (a)+(b) and CP-7 | Ruled: fees and licences do not count; deposits and minimum balances do, pending D-Q5 |
| **D-Q2** | Disclose, in the questions, that the orders go to a prop-firm evaluation account at another broker? | Licence category and non-professional status may depend on it (§1). An answer obtained without that fact may not hold. **If the destination is omitted, Q1 stays unresolved** for every candidate, however clear the reply reads. It cannot satisfy the rejection rule's licensing condition (§3) or reach CP-7 until CME and the provider confirm the actual use (Codex review on #583) | Disclose (recommended: an answer that holds) · omit · ask CME first, then decide |
| **D-Q3** | Which messages to send, and in what order? | Every vendor's cost depends on the CME licensing answer (§1) | Recommended: §3.0 (CME) first, then P1–P6 together. Or all at once |
| **D-Q4** | The Track A plan says to send the questions "near the actual feed gate so answers and prices are current" | The 2026-10-01 ruling moves the questions earlier. Answers may be stale by CP-7 | Recommended: send now, then **re-confirm every decision-bearing answer at CP-7**. That means the mandatory facts (Q1 licensing, Q2a coverage, Q3 order containment, Q5 unattended authentication) as well as prices and capital terms, as Track A readiness checkpoint 3 already requires. Or hold sending (Codex review on #583) |
| **D-Q5** | Are refundable deposits or minimum balances needed for data access exempt from the $700 ceiling? | Open per the rail GO ADR addendum (#580, `3474ab2`): until ruled, they **count**. Several candidates attach capital to data access. Examples, all unverified: IBKR's $500 minimum equity for data **[repo]**; tastytrade's "funded with any amount" **[excerpt]**; the A′ parked deposit. With the ceiling's existing commitments, that capital may decide which candidates are feasible | Exempt · count (the standing position until ruled) · exempt only up to a stated amount |
| **D-Q6** | Do one-time non-refundable feed charges (setup, activation, onboarding) count toward the $700 ceiling? | The D-Q1 exemption names only subscription and CME licence fees, so until ruled these **count**. CME's Q2b/Q3, Massive's Q2b and every brokerage Q2b now ask for them (§4, field (c)) | Exempt as feed costs · count (the standing position until ruled) |
| **D-Q7** | Does a recurring **API-access or platform fee** that a provider requires for data access count as a data-feed subscription fee (exempt under D-Q1), or as a non-feed recurring charge (field (a2), which counts)? Examples, all unverified: Tradovate's $25 API add-on; Ironbeam's "from $249/month" API fee without trading activity | The D-Q1 addendum names only "production data-feed subscription fees" and CME licence fees, so until ruled these count as (a2) (Codex review on #583) | Exempt as feed costs · count (the standing position until ruled) |

## 6. A9-PREP: not discharged, because the owner text does not allow it

**The task asked** whether Track A's A9-PREP can be discharged by reference to H8, to remove duplicate ownership. **It cannot, for three reasons in the owner text:**

1. **Scope.** A9-PREP is: "freeze the provider-neutral `BarSource` contract, four-symbol mapping requirements and mocked auth/renewal/reconnect/staleness/fail-closed test contract" ([Track A plan](../superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md#4-task-list-checkbox--parent-session-acceptance-after-the-two-pass-review), A9-PREP line). H8 delivered the mapping requirements ([spec §5](../spec/2026-09-27-cme-execution-feed-equivalence-test-DRAFT.md#5--per-symbol-mapping-requirements), [note §2](2026-09-27-feed-provider-neutral-preparation.md#2-four-leg-symbol-roll-and-session-mapping)) and handling rules (spec §7). It **proposes** freezing the consumer contract at F1 ([note §3](2026-09-27-feed-provider-neutral-preparation.md#3-later-binding-rule--proposed-text-for-the-f1-packet), A.2, accepted only at CP-6). No mocked auth/renewal/reconnect test contract exists: `grep -rln BarSource tests` returns nothing.
2. **Who ticks it.** The Track A task list's checkboxes are "parent-session acceptance after the two-pass review" (plan §4 heading). A worker cannot tick one.
3. **H8's own record.** H8 says that note §2 and spec §5 "are **inputs offered to A9-PREP**. A9-PREP (Track A) remains the owner that freezes the mapping requirements, and this preparation discharges no A9-PREP checkbox" ([note header](2026-09-27-feed-provider-neutral-preparation.md)).

**The real duplication is narrower than the task assumed:**
- **Mapping requirements.** Two owners: A9-PREP freezes them, and the equivalence spec §5 states them. Once the spec is frozen, the coordinator could record that A9-PREP's mapping clause is satisfied by reference to frozen spec §5. That would be a coordinator act on the Track A plan, which this worker does not take.
- **Candidates and questions.** The Track A plan's six questions and candidate table predate H8's Q1–Q12, and its timing line ("send … near the actual feed gate") predates the 2026-10-01 ruling. This note reads them, and it does not edit them. It is a mirror skew for the coordinator's blast-radius pass.
- **Not duplicated, still owed by A9-PREP:** the `BarSource` contract freeze and the mocked auth/renewal/reconnect/staleness/fail-closed tests.

## 7. Verification of this note

Commands and reads in this session, at `origin/main` `2b98d22`:
- Owner reads by `sed -n`/`grep -n`: H8 note (all), draft spec (all), locked template (all), H8 card and status row (handoff set `:52`, `:481–:527`), checklist §3 Feed row and §4 CP-6/CP-7, Track A plan §3.2 and §4–§5, CP-2 F-4 ruling and X-13, rail GO ADR ceiling lines. #580's diff: `git diff origin/main...origin/claude/first-session-cuts`.
- Web: `WebSearch` result excerpts only. `WebFetch` to `cmegroup.com`, `massive.com` and `developer.tastytrade.com` returned `EGRESS_BLOCKED`. No vendor page was opened, and no message, form or account was touched.
- `grep -rln BarSource tests ops` → `ops/c1_signal_daemon/evaluate_loop.py`, `ops/c1_signal_daemon/feed.py` only.
- Link check and gates: see the PR body.
