# Feed: provider shortlist and written questions Q1–Q12 (DRAFT, for the operator to send)

**Status:** DRAFT, returned to the coordinator on 2026-10-01. This is a candidate list for **written questions only**. It does not select, rank for funding, contact or price a provider. Nothing here has been sent. **Sending any message is Joshua's act alone.**
**Authority:** Joshua's ruling of 2026-10-01, item 2 ("Feed: no-spend steps move earlier"), recorded in the deployment-checklist addendum "first-session simplification rulings" in [PR #580](https://github.com/Joshua-Asante/first-passage/pull/580) (branch `claude/first-session-cuts`, head `628a520`; merged as `dd94b41`). Under that ruling, written provider questions Q1–Q12 and reads of published terms are **allowed now**, with no account, signup, credential or spend. Signup and spend stay behind D-feed (a)+(b) and CP-7.
**Serves (Rule 7), does not replace:**
- the question set, which is [H8 note §5](2026-09-27-feed-provider-neutral-preparation.md#5-provider-specific-facts-that-become-funding-decision-questions) (Q1–Q12, with Q2 split into Q2a and Q2b);
- the candidate record and decision rule in [Track A plan §3.2](../superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md#32-a9--production-feed-verification-record-and-funding-checkpoint-added-2026-09-11), which this note re-reads on 2026-10-01 and does not overrule;
- the funding decision, which is **CP-7** ([checklist §4](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#4-operator-checkpoints--where-approval-is-taken)).

**Not granted:** contact, account, signup, trial, credential, subscription or spend; a provider selection; TradingView in any feed role (its Terms of Use §3 license alerts and webhooks for display-only use, so webhooks-as-feed are forbidden: [S2b daemon build, option C](../adr/2026-08-08-s2b-signal-daemon-build.md#option-c--tradingview-alert-webhook-as-bar-transport); a TV webhook as bar transport is not licensed: [M1 addendum of 2026-09-11](../adr/2026-07-22-c1-venue-native-monitoring-maturity.md#addendum-2026-09-11--item-5-input-for-stage-1-operator-attended-controlled-input-express)); any change to `emit_enabled`, `dry_run`, arming or orders. Databento stays retired (AGENTS.md data-source disposition).

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
- **TradingView, in any feed role:** forbidden (TradingView Terms of Use §3, display-only: [S2b daemon build, option C](../adr/2026-08-08-s2b-signal-daemon-build.md#option-c--tradingview-alert-webhook-as-bar-transport); [PIPELINES.md P2](../../PIPELINES.md#p2--codification-bridge-python--pine--retired-2026-08-02): Pine/TV stays research/export).
- **TradeStation:** "dominated", because of a $10,000 funded minimum for an API key **[repo]**.
- **IQFeed, CQG, Barchart, dxFeed direct:** "no evidence they beat the shortlist" **[repo]**. They were not re-researched here. They are the next set to question if **no** shortlisted candidate meets **every requirement CP-7 needs** from its answers. A candidate fails if **any** of the following is not met:
  - Q1, Q2a, Q3 and Q5 answered unambiguously **and affirmatively**. That means the use is licensed or licensable (Q1), all four products are covered (Q2a), order actions can be disabled or the product is data-only (Q3), and authentication can run unattended, with session and subscription limits that let all four products stream at the same time (Q5; spec four-leg boundary). A clear "no" fails just as an ambiguous answer does;
  - a usable bar or trade stream (Q4);
  - cloud or VPS operation and private storage, both permitted (Q6);
  - every other Q7–Q12 answer compatible with the [equivalence spec](../spec/2026-09-27-cme-execution-feed-equivalence-test-DRAFT.md) (frozen at `721be61`, PR #585) and the H8 requirements. Examples of failure: revisions or backfill that cannot be distinguished from live delivery, so they can be neither held back from the consumer (M7) nor labelled in the capture (Q7). Missing replay is **not** a failure: the spec halts while disconnected and, after a reconnect, delivers only bars still within the M5 bound, so replay availability is recorded, not required. Other examples: no-trade intervals or halts that cannot be identified (Q8), contracts that cannot be mapped (Q9), 15-minute bars that routinely cannot be completed by the 30-second hard deadline after their interval closes (Q10; spec M5), and session, DST or early-close handling that cannot be reconciled (Q12);
  - a **complete Q2b cost and capital record** (§4), independent of the ceiling. Every amount in fields (a), (b) and (c) must be known, including the exempt (a1) charges, and any usage-priced charge must carry a bounded monthly estimate. Track A needs the actual total monthly cost before any purchase;
  - the **ceiling-bearing total** (§4: every non-exempt field summed with existing commitments) within the ceiling.

  A candidate does not need to fail the four mandatory checks to trigger this (Codex reviews on #583).

The order of P1–P7 is not a ranking. Track A's decision rule, which prefers no greater secret authority at lower capital or run-rate, applies at CP-7 to the **answers**. It does not apply to this list.

## 3. Messages, ready to send

**How to use these.** Each message has three parts, pasted in this order:
1. the **common context paragraph** (below);
2. the **canonical questions Q1–Q12** (below), with "[the product]" replaced by the product that the provider block names;
3. the provider block's **additions** (§3.0–§3.6). Paste each addition directly after the canonical question whose label it carries.

The canonical set is written once, so every provider is asked the same questions and the answers line up. A provider block holds only what is specific to that provider: the product name, published terms to confirm, and provider-specific follow-ups (restructure requested by the coordinator on #583). Square brackets mark the operator's choices. Where published terms already appear to answer a question, the addition asks the vendor to **confirm** that reading in writing, and the URL is given. Do not include account identifiers or P&L.

**The rejection rule is unchanged:** reject an answer that leaves licensing (Q1), all-four-symbol coverage (Q2a), the ability to disable order actions (Q3) or unattended authentication (Q5) ambiguous ([Track A plan](../superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md#32-a9--production-feed-verification-record-and-funding-checkpoint-added-2026-09-11), "Reject any answer …"). An ambiguous Q2b is an input to the funding decision, not a disqualification ([H8 note §5](2026-09-27-feed-provider-neutral-preparation.md#5-provider-specific-facts-that-become-funding-decision-questions)). The full eligibility screen in §2 applies before any cost comparison (§4).

**Common context paragraph** (paste at the top of every message):

> I am an individual, non-professional trader. I am evaluating real-time CME Group futures data for a headless, automated system, before opening any account. The instruments are the front dated contracts of **6J** (CME Japanese yen), **MNQ** (CME Micro E-mini Nasdaq-100), **MYM** (CBOT Micro E-mini Dow) and **MGC** (COMEX Micro Gold). A Linux service on a cloud server would build 15-minute bars from the data, without any screen, and make automated trading decisions from them. The data would not be displayed to anyone or redistributed. [Optional, see D-Q2: The resulting orders are placed in a proprietary-trading-firm evaluation account held at a different broker.] I would be grateful for written answers to the questions below, with links to the governing terms where possible. **For every fee or charge you mention, recurring or one-time, please say what it is for: receiving the market data, or opening or maintaining an account. Please also give its billing cadence (monthly, annual, or a prepaid minimum term) and the amount due at signup. If both a deposit and a minimum balance apply, does the deposit count toward the minimum balance? For every deposit, minimum balance, inactivity charge or withdrawal restriction, please state "none" explicitly if it does not apply.**

**Canonical questions Q1–Q12** (paste into every message after the common context):

> **(Q1) Licensing.** May a non-professional customer use real-time 6J, MNQ, MYM and MGC data from [the product] in a headless program that makes automated trading decisions (non-display use)? **May those decisions drive orders at a different broker?** Does your CME licence cover this non-display use, or must I hold a CME Non-Display (Category A) licence myself? [If D-Q2 is "disclose": the other broker account is a proprietary-trading-firm evaluation account. Does that change the licence category, the plan or my non-professional status?]
>
> **(Q2a) Coverage.** Does [the product] give a non-professional **real-time** data for all four products, CME (6J, MNQ), CBOT (MYM) and COMEX (MGC), through the API and not only in your platforms? Which exact subscriptions or entitlements are needed, and is any further exchange entitlement required?
>
> **(Q2b) Cost and capital.** What is the all-in monthly cost for this use, including any API or connection fee, data subscriptions, exchange and CME licence fees, and any monthly minimum? Are there setup fees or other **one-time, non-refundable** charges (setup, activation, onboarding), minimum terms or cancellation terms? What **required opening deposit, prepayment, minimum balance or equity, inactivity charge and withdrawal terms** apply, and is any trading-activity requirement attached to API or data access? Please state "none" for each that does not apply. **For every deposit, prepayment or minimum balance:** is it refundable, and under what conditions and timing is it returned? **If any charge is usage-priced** (per GB, per message or similar): what exactly is metered (for example bytes delivered, egress, or per channel or symbol), are there monthly minimums, and what is a bounded monthly estimate, in both metered units and dollars, for continuous real-time delivery of only these four products through their full trading sessions? Please give the estimate for **every delivery granularity you offer**: trades, 1-minute bars, finer bars and native completed 15-minute bars.
>
> **(Q3) Order containment.** Is there an API credential, key or user that the server prevents from placing, modifying or cancelling orders? If not, can order permission be disabled at the account or API-user level? If [the product] is data-only, please confirm that its credentials give no order or account capability.
>
> **(Q4) Bars and trades.** Do you stream completed 1-minute bars, or native completed 15-minute bars? Do you also deliver finer bars (for example 1-second or 5-second bars) or individual trades? For each stream you offer, please give:
> - whether the timestamp marks the **start or the end** of the bar or interval, and the interval;
> - the time zone, UTC offset or epoch unit (for example UTC epoch milliseconds or nanoseconds, or exchange-local or account-local wall-clock time), for bars and for trades separately;
> - whether exchange timestamps are included, and whether the time is exchange time or your own aggregation time;
> - whether a bar is emitted once at close or updated in place while it forms, and whether a bar or trade can be revised after delivery or after its period ends;
> - **prices:** whether each bar's open, high, low and close are built from **executed trade prices**, or from bid/ask, midpoint, settlement or another indicative price;
> - **volume:** whether each bar carries exchange-reported **trade volume** (contracts traded in the bar), whether that volume is ever synthetic, estimated or quote-derived, and whether it is final when the bar is delivered or revised later;
> - **for trades:** whether each trade message carries the exchange-reported **contract quantity**, how corrected, busted or cancelled trades are signalled, and how they should change a bar's volume;
> - how the stream is delivered.
>
> **(Q5) Unattended operation.** Can login, token and session renewal run **unattended for weeks**, with no UI, interactive login, MFA prompt, daily login or desktop session? Is conformance testing required for a **market-data-only** application? What session, connection, concurrent-subscription, symbol and market-data-line limits apply? Can all four products (6J, MNQ, MYM, MGC) stream at the same time on one session?
>
> **(Q6) Cloud use and storage.** May the client or gateway **connect and run unattended from a cloud or VPS host**? May the raw messages and derived bars be stored privately for audit on a cloud server?
>
> **(Q7) Reconnects, replays and corrections.** After a disconnect and reconnect, are missed bars replayed or backfilled, and how are replays and corrections delivered? Are corrections and revised bars flagged? Do messages carry sequence numbers or identifiers? **If replayed or backfilled messages are delivered,** how are they distinguished from live delivery: a flag, a field, a separate channel or a separate message type?
>
> **(Q8) No-trade intervals and halts.** Is a bar published for an interval with **no trades**? If so, how is it marked, so that a client can tell it apart from a trade-evidenced bar? **Exchange halts:** how is an exchange trading halt inside a session represented: as an omission, as a flagged bar, or as a status message?
>
> **(Q9) Contracts.** How are dated futures contracts identified (for example, the March MNQ contract)? Is a continuous or front-month symbol offered, and what is its roll rule? **If I request an expired, ambiguous or unrecognised dated-contract code,** do you return an error, or silently substitute the current or continuous contract? Does every delivered message identify the **actual dated contract** it belongs to?
>
> **(Q10) Delivery timing.** What is the typical delay from bar end to delivery? What maintenance or reset windows fall inside the Sunday–Friday 18:00–17:00 ET session? **Hard deadline:** I build 15-minute bars, and each one must be complete **within 30 seconds after its 15-minute interval closes**. For native 15-minute bars: does every completed bar reach the client within 30 seconds after it closes? For 1-minute or finer bars, or trades: does **all** the data belonging to a 15-minute interval (its last constituent bar, or its last trade) reach the client within 30 seconds after that **15-minute interval** closes? What share of 15-minute intervals miss that, and what is the worst case you document? "Typical" latency alone is not enough for this use. **Quiet intervals:** when a 15-minute interval has no trades, what tells the client within those same 30 seconds that the interval is over and nothing is missing: a heartbeat, a sequenced status message, a no-trade marker, or nothing?
>
> **(Q11) History.** What historical bar depth is available through the API for these products, and with what pacing limits? Is historical access included in the subscription, and if not, what does it cost?
>
> **(Q12) Sessions.** How are DST changes and holiday early closes reflected in session, trading-hours and bar data?

### 3.0 CME Group: market-data licensing (licensor; covers P7)

Send to CME Group's market data licensing contact (the Data Services portal, or the contact named on the non-display FAQ).

**Message layout.** CME is the licensor, so its message differs from the others:
- the common context paragraph;
- CME's own licensing questions Q1, Q2a and Q2b below, **in place of** canonical Q1–Q2b;
- canonical Q3–Q12, with "[the product]" read as each direct product, **answered separately for (a) Market Data over WebSocket API and (b) Smart Stream on GCP**;
- the additions below.

> **(Q1, licensing)** Does this use require a **Non-Display (Category A, automated trading)** licence held by me directly, or can it be covered by a data vendor's or broker's licence? Is there a non-professional or individual route for Category A, and which sub-category applies? [If D-Q2 is "disclose": Does placing the orders in a third-party firm's evaluation account, rather than my own funded account, change the category or my non-professional status?]
>
> **(Q2a, licensing)** Does one licence cover CME, CBOT and COMEX, or is each exchange licensed separately? **For the direct feed:** do your Market Data over WebSocket API and Smart Stream on GCP each deliver **real-time** data for all four of 6J, MNQ (CME), MYM (CBOT) and MGC (COMEX), and which entitlement does each need?
>
> **(Q2b, licensing)** What are the current monthly fees, including the billing unit (per licensee, per exchange, per device)? Your January 2026 fee list appears to show User Non-Display Category A at $457 and Managed User Non-Display Category A at $208 ([fee list](https://www.cmegroup.com/market-data/files/january-2026-market-data-fee-list.pdf)). Please confirm which applies, and whether a "$670 per exchange" figure I have seen is current. Are there minimum terms, setup fees or annual audits? Is any **deposit, prepayment or minimum commitment** required for either direct product? Please state "none" if not. **For each one:** is it refundable, and under what conditions and timing is it returned?
>
> **Please answer Q3–Q12 separately for (a) Market Data over WebSocket API and (b) Smart Stream on GCP.** The two products may differ in authentication, storage rights, replay, symbology, latency and session handling.

**Additions:**

> **(Q3, addition)** Your Market Data over WebSocket API and Smart Stream on GCP are data-only. Can an individual subscribe to either, and what are the minimum commitments? **For each product separately**, what is the all-in monthly cost for these four products: delivery or usage charges, licence fees, and any one-time setup charge? Smart Stream appears to be priced "as low as $0.50/GB plus applicable ILA fees" ([page](https://www.cmegroup.com/market-data/real-time-futures-and-options-data-api.html)). **If either product is usage-priced** (per GB, per message or similar): what exactly is metered (for example bytes delivered, egress, or per channel or symbol), are there monthly minimums, and what is a bounded monthly estimate, in both metered units and dollars, for continuous real-time delivery of only these four products through their full trading sessions? Please give the estimate for **every delivery granularity you offer**: trades, 1-minute bars, finer bars and native completed 15-minute bars.
>
> **(Q6, addition)** The client for each product means the WebSocket API client and the Smart Stream consumer respectively.

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

**[The product]:** the individual **Futures Advanced** plan.

**Additions:**

> **(Q1, addition)** Your knowledge base says individual plans cover "your own scripts, your own trading". Does that include this non-display use by a headless program?
>
> **(Q2b, addition)** Is $199/month the all-in monthly cost for this use, including exchange and CME licence fees?
>
> **(Q3, addition)** Please confirm that the API key gives data access only, with no order or account capability.
>
> **(Q4, addition)** Please answer for the per-minute aggregate WebSocket stream, and also for the per-second aggregates and the trades stream.
>
> **(Q5, addition)** Can one API key hold a WebSocket connection for weeks unattended, with no interactive login?
>
> **(Q11, addition)** Please confirm the historical depth on Futures Advanced for these four products.

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

**[The product]:** the Open API (DXLink).

**Additions:**

> **(Q2a, addition)** Does the non-professional futures data entitlement cover all four products through the API?
>
> **(Q3, addition)** Is there an OAuth scope that cannot place, modify or cancel orders?
>
> **(Q4, addition)** For DXLink candle events on futures: are 1-minute candles supported live? Is the candle time the **start** of the period, in UTC milliseconds? Can a live candle be updated after its period ends?
>
> **(Q5, addition)** Access tokens appear to last 15 minutes and the quote token 24 hours. Can both be renewed **unattended for weeks**?
>
> **(Q6, addition)** Are cloud or VPS use and private storage permitted **under the subscriber agreement**?

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

**[The product]:** your API. **Please answer every question separately for (a) the TWS API through IB Gateway and (b) the Client Portal Web API.** The two paths may differ in authentication, bar delivery, limits and permissions. Put this sentence at the top of the questions.

**Additions:**

> **(Q1, addition)** Which non-display subscription applies to this "off-platform" use, and does it replace or add to a CME Non-Display (Category A) licence held by me?
>
> **(Q2b, addition)** Is the minimum equity for market data still $500?
>
> **(Q4, addition)** For 1-minute bars, please cover real-time bars and keep-up-to-date historical bars. For finer data, please cover 5-second real-time bars and tick-by-tick last-sale data.
>
> **(Q5, addition)** Can the gateway authenticate and stay connected unattended for weeks without a desktop session?

### 3.4 P4: Ironbeam API

**What published terms already appear to answer** (**[excerpt]** unless marked):

| Q | Reading | Source |
|---|---|---|
| Q2b | API access is free with at least 5 contracts traded per month; otherwise "starting at $249/month". Level 1 and Level 2 real-time are "free for non-professional traders" (whether through the API or platforms only: not stated in the excerpt) | [API access](https://www.ironbeam.com/knowledge-base/ironbeam-api-access/); [platform market data fees](https://www.ironbeam.com/knowledge-base/ironbeam-platform-market-data-fees/) |
| Q3 | Order-capable; read-only restriction unknown **[repo]** | [ironbeam.com/api](https://www.ironbeam.com/api/) |
| Q4 | Trade bars, tick bars, time bars and volume bars over one WebSocket. Bar-close semantics unknown **[repo]** | [subscribing over WebSockets](https://www.ironbeam.com/how-to-subscribe-real-time-market-data-ironbeam-websockets/) |
| Q5 | Bearer authentication; documented reconnect rule **[repo]** | [API reference](https://docs.ironbeamapi.com/) |
| Q1, Q2a, Q6–Q12 | Not found | — |

**[The product]:** your API.

**Additions:**

> **(Q2b, addition)** Your page says API access is free with 5 or more contracts traded per month and otherwise starts at $249/month. For a data-only use with no trading at Ironbeam, what is the all-in monthly cost? Are non-professional real-time data fees free through the API too?
>
> **(Q4, addition)** Please answer for WebSocket time bars at 1 or 15 minutes, and for trade and tick bars.
>
> **(Q5, addition)** Can bearer-token authentication be renewed unattended for weeks?

### 3.5 P5: Rithmic (R|Protocol API)

**Two-stage screen** (Codex review on #583). Rithmic data comes through a clearing broker (FCM), so Rithmic may properly defer licensing, entitlement, order-restriction, authentication or storage questions to the FCM.
- **Stage 1 (this message).** Rithmic answers what it controls. Any answer that defers to the FCM is recorded as **DEFERRED-TO-FCM**, not as ambiguous, and the rejection rule is not applied to those items at stage 1.
- **Stage 2.** The same common context and canonical Q1–Q12 go to **one named FCM**, chosen by the operator from Rithmic's stage-1 answer about which FCMs offer either a **data-only** user or an otherwise order-capable user whose order actions are **disabled and enforced on the server side**. Either form of containment is accepted, as in §2 and canonical Q3 (Codex review on #583). **If Rithmic's stage-1 answer names no such FCM**, for example because it defers containment to the FCM (DEFERRED-TO-FCM), the operator instead chooses an FCM that publicly offers R|Protocol access, and that FCM's own canonical Q3 answer decides containment (Codex review on #583). Canonical Q2b already asks the FCM for its **capital and liquidity terms**: required deposit, minimum account balance, inactivity fees and withdrawal constraints. Those answers fill the held-capital field (§4) (Codex review on #583).
- **The rejection rule (§3)** is applied to the stage-1 and stage-2 answers combined, before CP-7.

**What published terms already appear to answer** (all **[excerpt]**, several from brokers rather than Rithmic):

| Q | Reading | Source |
|---|---|---|
| Q2b | Reported API access around $20/month plus $0.10 per contract; some brokers charge a $100 monthly minimum per API user ID. Non-professional L1 data from $3.00 per exchange per month; CME Globex L2 bundle $41/month (broker pages, not Rithmic terms) | [Ironbeam: Rithmic market data fees](https://www.ironbeam.com/knowledge-base/rithmic-market-data-fees/); [EdgeClear: market data costs](https://support.edgeclear.com/portal/en/kb/articles/market-data-costs) |
| Q4 | R\|Protocol (WebSocket plus protocol buffers) provides server-side "custom time, tick, volume, and price range bars" | [rithmic.com/apis](https://www.rithmic.com/apis) |
| Q5 | **Conformance testing is required before production access.** Development runs against the Rithmic Test system | [rithmic.com/apis](https://www.rithmic.com/apis); [exchange simulator](https://www.rithmic.com/products/exchange-simulator) |
| Q1, Q2a, Q3, Q6–Q12 | Not found | — |

**[The product]:** R|Protocol.

**Additions:**

> **(Q1, addition)** No orders would be sent through Rithmic.
>
> **(Q2a, addition)** Can one user ID receive real-time CME, CBOT and COMEX data for all four products? Which clearing firms offer a **data-only** R|Protocol user, or a user whose order actions can be disabled and enforced on the server side?
>
> **(Q2b, addition)** What does the clearing firm add to the cost?
>
> **(Q3, addition)** Can a user ID be configured, on the server side, so that it cannot place, modify or cancel orders?
>
> **(Q4, addition)** Please answer for server-side time bars at 1 or 15 minutes, and for tick bars or trades.

### 3.6 P6: Tradovate API, personal live data-only account (option A′)

**Keep this separate from the eval.** The feed account would be a personal account that is never linked to the broker bridge (Track A readiness checkpoint 5). It is not the incumbent evaluation account.

**What published terms already appear to answer** (**[excerpt]** unless marked):

| Q | Reading | Source |
|---|---|---|
| Q1 | Real-time data through the API reportedly requires the subscriber to become a CME sub-vendor by signing the CME ILA. The ILA is not needed for order-only API use | [NinjaTrader vendor support: Tradovate API Access](https://vendor-support.ninjatrader.com/s/article/Tradovate-API-Access); [forum thread](https://community.tradovate.com/t/how-to-do-the-cme-vendor-registration-for-market-data-access-via-websocket/11320) |
| Q2b | API add-on $25/month, "does not provide access to real-time market data"; a CME licence reported at $290–$500/month on top (forum and third-party). Non-professional data rates are on a support page | same; [non-professional monthly data rates](https://support.tradovate.com/s/article/Non-Professional-Monthly-Data-Rates-Tradovate?language=en_US) |
| Q3 | Order-capable **[repo]** | Track A plan §3.2 |
| Q2a, Q4–Q12 | Not found | — |

**[The product]:** your API on a personal live account. [If D-Q2 is "disclose": the evaluation account is a separate account.]

**Additions:**

> **(Q1, addition)** Your support material appears to say that streaming real-time data through the API requires me to sign the CME Information License Agreement as a sub-vendor ([article](https://vendor-support.ninjatrader.com/s/article/Tradovate-API-Access)). Please confirm that, and which CME licence category applies.
>
> **(Q2a, addition)** Does API data cover all four products once the CME licence is in place?
>
> **(Q2b, addition)** Please break the all-in monthly cost into the API add-on, data subscriptions and the CME licence. The deposit and balance terms asked about are those for a live account used only for data.
>
> **(Q4, addition)** Please answer for the chart subscription's completed 1-minute bars. Is the bar time the start of the bar, in UTC?

## 4. Recording the answers

- Keep each reply's original privately, and record its SHA-256 beside the answer, as the drill plan does for venue replies.
- Fill one row per **provider variant** and question, with P3a, P3b, P7a and P7b as separate rows, never merged into one provider row (Codex review on #583). Each row records **answer · source (reply or page, with date) · verified by the operator (yes/no)**.
- Before any candidate enters the cost comparison, apply the **full eligibility screen in §2**, not only §3's ambiguity rule. Q1, Q2a, Q3 and Q5 must be answered affirmatively, Q4 and Q6–Q12 must be compatible with the spec, and the Q2b record must be complete. A clear "no" excludes the candidate just as an ambiguous answer does (Codex review on #583).
- Costs are compared in **three separate fields**, never summed:
  - **(a) recurring monthly cost**, split into two parts. **(a1)** covers every recurring non-refundable charge whose purpose is receiving the market data: data-feed subscriptions, CME licence fees, and **required API or data-access fees** such as a broker API add-on or a monthly API fee. **(a2)** covers every other recurring charge, such as account maintenance or inactivity fees that are not for receiving the data.
  - **Usage-priced charges** (per GB, per message) enter (a1) or (a2) as the provider's **bounded monthly estimate for the exact four-symbol stream**, recorded with its metering rules and any monthly minimum. A bare tariff such as "$0.50/GB" leaves field (a) incomplete for that row, and the row can be neither compared nor ceiling-checked until an estimate is obtained (Codex review on #583).
  - **(b) held capital**, meaning refundable deposits, **refundable prepayments** and minimum balances required for data access. Any upfront amount the provider says is refundable belongs here, whatever it is called. A non-refundable upfront amount belongs in (c) only if it is a one-time charge; a non-refundable advance payment of a recurring charge stays in (a) (Codex review on #583). Record each requirement as the provider states it, and also record the **capital that must actually be committed**. Where an opening deposit also satisfies the minimum balance, that is the larger of the two, not their sum. For example, a $500 opening deposit that leaves the account at its $500 minimum commits $500. If the answer does not say whether one satisfies the other, the two are counted separately until clarified. Field (b) enters the ceiling check at the committed amount (Codex review on #583).
  - **(c) one-time non-refundable charges**, such as setup, activation or onboarding fees, each marked as either for the feed or not. Field (c) holds only charges that do not recur. A recurring charge billed in advance, such as an annual bill or a prepaid minimum term, is **not** a (c) entry: it is recorded once in (a), with its monthly equivalent, its billing cadence and the amount due up front (Codex review on #583).

  The split between (a1) and (a2), and the feed marking in (c), come from each provider's own statement of what every charge is for. The common context paragraph (§3) asks every provider for that statement. If a charge's purpose is unstated or ambiguous, it counts toward the ceiling until clarified (Codex review on #583).

  This follows Track A's decision rule, which weighs "lower capital **or** run-rate" separately (Codex review on #583).
- **What the ceiling covers** (D-Q1, D-Q6 and D-Q7 ruled; rail GO ADR [addendum of 2026-10-01](../adr/2026-07-17-c1-rail-build-account-registration-go.md#addendum--2026-10-01-production-data-feed-costs-are-outside-the-700-ceiling), in force on `main` since [PR #587](https://github.com/Joshua-Asante/first-passage/pull/587) merged as `abab003`). A feed cost is any non-refundable charge whose purpose is receiving the market data, and it is **exempt**. That covers field (a1) and the feed charges in field (c). **Refundable deposits and minimum balances stay under the cap** until Joshua rules otherwise (D-Q5). Any charge whose purpose is not receiving the market data also stays under the cap, as the addendum states.
- **Ceiling check.** The three fields stay separate for ranking. The $700 check **sums every non-exempt amount** with the ceiling's existing commitments:
  - **Recurring charges and upfront billing.** Each recurring charge enters the check at the **larger** of two amounts: its 3-month accrual, or any amount required up front, such as an annual bill, a prepaid minimum term or another payment due at signup. The rail GO halts on **actual** spend over $700 as well as projected spend, so a checkout charge that breaches the ceiling fails the check even when the 3-month accrual fits (Codex review on #583).
  - **The sum:** each (a2) charge at that larger amount, plus (b), plus any charge in (c) that is not for the feed. A prepaid recurring charge is counted **once**, inside its recurring term, never again as a one-time charge. For example, a non-feed account fee of $10 a month billed annually at $120 up front enters at max(3 × $10, $120) = $120, not $120 + $120 = $240 (Codex review on #583).

  Two items that each pass alone can therefore still fail together, for example a $500 deposit plus a $300 non-feed account fee (Codex review on #583).
- Only exempt charges, field (a1) and the feed charges in (c), are recorded outside the ceiling tally. Every purchase stays an operator act at CP-7.
- The answers feed **CP-7**. They select nothing, and they open no account.

## 5. Decisions needed from Joshua

| # | Decision | Why it matters now | Options |
|---|---|---|---|
| **D-Q1** | **RULED 2026-10-01, narrowed the same day:** feed **subscription fees and CME market-data licence fees** do **not** count toward the $700 ceiling | Joshua, 2026-10-01: "feed costs don't count toward the $700 ceiling". It is recorded as the rail GO ADR addendum "production data-feed costs are outside the $700 ceiling" in [PR #580](https://github.com/Joshua-Asante/first-passage/pull/580) (`473533c`). Joshua's same-day clarification (`3474ab2`) limits the exemption to **feed costs only**: subscription and licence fees, which are also outside the projected spend that revert trigger (b) measures. **Refundable deposits and minimum balances stay under the cap**; the A′ parked deposit is the addendum's own example. That part is open as D-Q5. *Superseded question (kept for the record):* whether feed costs counted, given the ceiling "$700 all-in to first live fill (eval + 3 months run-rate)" and F-4's drill-only ruling. Feed signup and spend still need D-feed (a)+(b) and CP-7 | Ruled: fees and licences do not count; deposits and minimum balances do, pending D-Q5 |
| **D-Q2** | Disclose, in the questions, that the orders go to a prop-firm evaluation account at another broker? | Licence category and non-professional status may depend on it (§1). An answer obtained without that fact may not hold. **If the destination is omitted, Q1 stays unresolved** for every candidate, however clear the reply reads. It cannot satisfy the rejection rule's licensing condition (§3) or reach CP-7 until CME and the provider confirm the actual use (Codex review on #583) | Disclose (recommended: an answer that holds) · omit · ask CME first, then decide |
| **D-Q3** | Which messages to send, and in what order? | Every vendor's cost depends on the CME licensing answer (§1) | Recommended: §3.0 (CME) first, then P1–P6 together. Or all at once |
| **D-Q4** | The Track A plan says to send the questions "near the actual feed gate so answers and prices are current" | The 2026-10-01 ruling moves the questions earlier. Answers may be stale by CP-7 | Recommended: send now, then **re-confirm every decision-bearing answer at CP-7**. That means the **complete Q1–Q12 set** that the fallback test (§2) treats as CP-7-required, not just the mandatory facts (Q1 licensing, Q2a coverage, Q3 order containment, Q5 unattended authentication). It includes, for example, the cloud-use right (Q6), replay behaviour (Q7), timestamp mapping (Q4) and the delivery deadline (Q10), as well as prices and capital terms, as Track A readiness checkpoint 3 already requires. Or hold sending (Codex review on #583) |
| **D-Q5** | Are refundable deposits or minimum balances needed for data access exempt from the $700 ceiling? | Open per the rail GO ADR addendum (#580, `3474ab2`): until ruled, they **count**. Several candidates attach capital to data access. Examples, all unverified: IBKR's $500 minimum equity for data **[repo]**; tastytrade's "funded with any amount" **[excerpt]**; the A′ parked deposit. With the ceiling's existing commitments, that capital may decide which candidates are feasible | Exempt · count (the standing position until ruled) · exempt only up to a stated amount |
| **D-Q6** | **RULED 2026-10-01:** one-time non-refundable charges for the feed (setup, activation, onboarding) are feed costs and are **exempt** | Joshua, 2026-10-01: "a feed cost is any non-refundable charge whose purpose is receiving the market data". Recorded as a rail GO ADR addendum in [PR #587](https://github.com/Joshua-Asante/first-passage/pull/587), merged as `abab003`. One-time charges that are not for the feed still count (§4, field (c)) | Ruled: exempt when for the feed |
| **D-Q7** | **RULED 2026-10-01:** recurring API or data-access fees required to receive the data are feed costs and are **exempt**. Examples: a broker API add-on, a monthly API fee | The same ruling and record as D-Q6 ([PR #587](https://github.com/Joshua-Asante/first-passage/pull/587), merged as `abab003`). These fees move into field (a1). Recurring charges that are not for receiving the data stay in field (a2) and count | Ruled: exempt when required for the data |

## 6. A9-PREP: not discharged, because the owner text does not allow it

**The task asked** whether Track A's A9-PREP can be discharged by reference to H8, to remove duplicate ownership. **It cannot, for three reasons in the owner text:**

1. **Scope.** A9-PREP is: "freeze the provider-neutral `BarSource` contract, four-symbol mapping requirements and mocked auth/renewal/reconnect/staleness/fail-closed test contract" ([Track A plan](../superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md#4-task-list-checkbox--parent-session-acceptance-after-the-two-pass-review), A9-PREP line). H8 delivered the mapping requirements ([spec §5](../spec/2026-09-27-cme-execution-feed-equivalence-test-DRAFT.md#5--per-symbol-mapping-requirements), [note §2](2026-09-27-feed-provider-neutral-preparation.md#2-four-leg-symbol-roll-and-session-mapping)) and handling rules (spec §7). It **proposes** freezing the consumer contract at F1 ([note §3](2026-09-27-feed-provider-neutral-preparation.md#3-later-binding-rule--proposed-text-for-the-f1-packet), A.2, accepted only at CP-6). No mocked auth/renewal/reconnect test contract exists: `grep -rln BarSource tests` returns nothing.
2. **Who ticks it.** The Track A task list's checkboxes are "parent-session acceptance after the two-pass review" (plan §4 heading). A worker cannot tick one.
3. **H8's own record.** H8 says that note §2 and spec §5 "are **inputs offered to A9-PREP**. A9-PREP (Track A) remains the owner that freezes the mapping requirements, and this preparation discharges no A9-PREP checkbox" ([note header](2026-09-27-feed-provider-neutral-preparation.md)).

**The real duplication is narrower than the task assumed:**
- **Mapping requirements.** Two owners: A9-PREP freezes them, and the equivalence spec §5 states them. The spec froze at `721be61` (PR #585), so the coordinator could now record that A9-PREP's mapping clause is satisfied by reference to frozen spec §5. That would be a coordinator act on the Track A plan, which this worker does not take.
- **Candidates and questions.** The Track A plan's six questions and candidate table predate H8's Q1–Q12, and its timing line ("send … near the actual feed gate") predates the 2026-10-01 ruling. This note reads them, and it does not edit them. It is a mirror skew for the coordinator's blast-radius pass.
- **Not duplicated, still owed by A9-PREP:** the `BarSource` contract freeze and the mocked auth/renewal/reconnect/staleness/fail-closed tests.

## 7. Verification of this note

Commands and reads in this session, at `origin/main` `2b98d22`:
- Owner reads by `sed -n`/`grep -n`: H8 note (all), draft spec (all), locked template (all), H8 card and status row (handoff set `:52`, `:481–:527`), checklist §3 Feed row and §4 CP-6/CP-7, Track A plan §3.2 and §4–§5, CP-2 F-4 ruling and X-13, rail GO ADR ceiling lines. #580's diff: `git diff origin/main...origin/claude/first-session-cuts`.
- Web: `WebSearch` result excerpts only. `WebFetch` to `cmegroup.com`, `massive.com` and `developer.tastytrade.com` returned `EGRESS_BLOCKED`. No vendor page was opened, and no message, form or account was touched.
- `grep -rln BarSource tests ops` → `ops/c1_signal_daemon/evaluate_loop.py`, `ops/c1_signal_daemon/feed.py` only.
- Link check and gates: see the PR body.
