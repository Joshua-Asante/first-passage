# Feed providers: evidence matrix and narrowed questions (DRAFT, for Joshua's review)

**Status:** DRAFT, 2026-10-03. Nothing here has been sent. Joshua sends the final versions himself. The six existing Gmail drafts stay unsent references.
**Authority:** Joshua's request of 2026-10-03 (about 19:31Z), relayed by coordinator (2) to coordinator (3). It supersedes the attended-outreach plan.
**Serves, does not replace (Rule 7):** the [#583 note](2026-10-01-feed-provider-questions-DRAFT.md) (question set Q1–Q12, recording rules §4, rulings D-Q1…D-Q7), which coordinator (3) owns and will integrate. This note does not edit it.
**Evidence:** [companion matrix](2026-10-03-feed-provider-questions-narrowed-matrix.md), one row per (provider variant, question), every source retrieved 2026-10-03.

## Summary

Of 13 questions per variant (Q1, Q2a, Q2b, Q3–Q12), public primary sources fully answer very few. They do narrow most of the rest, often adversely. **D** = dropped (answered by source). **N** = narrowed (a smaller question remains). **F** = asked in full (nothing relevant found from the provider).

| Variant | D | N | F | Residual | Rejection-rule questions (Q1 licensing · Q2a coverage · Q3 order containment · Q5 unattended auth) |
|---|---|---|---|---|---|
| CME-LIC (licensor: Q1, Q2a, Q2b, plus Q1b) | 0 | 3 (+Q1b) | 0 | 3 (+Q1b) | Q1 open |
| P7a CME WebSocket API | 1 (Q11, negative) | 11 | 1 | 12 | all four open |
| P7b CME Smart Stream on Google Cloud | 2 (Q9; Q11, negative) | 10 | 1 | 11 | all four open |
| P1 Massive, Futures Advanced | 2 (Q3, Q11) | 11 | 0 | 11 | Q3 **met** by source; Q1, Q2a, Q5 open |
| P2 tastytrade Open API / DXLink | 0 | 13 | 0 | 13 | all four open |
| P3a IBKR TWS API / IB Gateway | 1 (Q5, negative) | 12 | 0 | 12 | Q5 **failed** by source; Q1, Q2a, Q3 open |
| P3b IBKR Client Portal Web API | 1 (Q5, negative, excerpt only) | 10 | 2 | 12 | Q5 **failed** by source (excerpt); Q1, Q2a, Q3 open |
| P4 Ironbeam API | 0 | 9 | 4 | 13 | all four open |
| P5 Rithmic R\|Protocol (stage 1) | 0 | 9 | 4 | 13 (7 with an FCM part) | all four open; Q3 and Q5 partly deferred to the FCM |
| P6 Tradovate API, personal data-only account | 0 | 11 | 2 | 13 | all four open |

The drafts in §4 are much shorter than #583's messages because each asks only the residual wording, cites the clause it is asking about, and drops the shared context paragraph's internal detail.

**What the sources change (all inferences unless an official source states it):**

1. **CME licensing reaches every provider.** CME's fee lists [excerpt] charge non-display fees **per exchange (DCM)**, so 6J and MNQ (CME), MYM (CBOT) and MGC (COMEX) pay three times. The individual rate (User Non-Display, "A8") is $457 per DCM per month in 2026, rising to $472 in January 2027: about **$1,371/month** for three DCMs. The cheaper managed rate ("A9", $208 per DCM) appears to require the data source to also route the subscriber's automated orders to CME markets. Here the orders go to another broker, so **A9 may be unavailable through any data source that does not route them**, which would push every candidate to A8. Only CME can confirm. That is why the CME message goes first (D-Q3).
2. **CME's 2026 licence updates (effective 2026-09-17)** ban "Synthetic Feeds" and, in a machine-learning/AI clause, list the automated generation of trade signals among prohibited uses [excerpt]. The context suggests the AI clause targets data shown on websites, and that internal, undistributed bars are not a Synthetic Feed. Neither reading is established, and a literal reading of the AI clause would reach this use. The CME draft asks both.
3. **Two providers' own terms point against this use.** Massive's Market Data Terms (§2, §5(d)) limit data to display use unless separately licensed. tastytrade's API Terms tie data use to transactions with tastytrade (Permitted Purpose, §8(3)). Both also apply CME's non-professional test that use must be limited to one's own assets, which a prop-firm evaluation account may fail.
4. **IBKR's unattended login fails by source** (IB Gateway from IBKR's own pages; the Client Portal Gateway from excerpts only). IB Gateway needs a manual two-factor login through a screen each week, and the Client Portal Gateway needs one daily. Individual accounts cannot use IBKR's OAuth. Under the §3 rejection rule that excludes both variants if a reply confirms it. The IBKR draft is therefore a single gate question.
5. **Capital that the #583 tables missed:** Ironbeam requires a live funded account with a $1,000 minimum balance for any API access. Tradovate requires $1,000 to create an API key and charges $35 per 30 days without a live trade on its free plan. An FCM offering Rithmic (Ironbeam) requires $500.
6. **Evidence quality.** `cmegroup.com` timed out on every fetch (12 of 12), so every CME licensing and fee fact is a search excerpt. `interactivebrokers.com` returned HTTP 403, and the Tradovate, NinjaTrader and tastytrade knowledge-base pages rendered empty. Excerpts can be stale or paraphrased, so these facts stay UNVERIFIED until Joshua reads them on the page or in a reply.

## 1. Conflicts

**With the #583 note's published-terms tables:**
- **CME fee unit and amount.** #583 left the unit open and could not reconcile "$670 per exchange". The excerpts give $457 (A8) and $208 (A9) **per licensee, per DCM**. $670 is the **2014** Category A fee [3p]. A January 2027 list (A8 $472, A9 $215) and a June 2026 list (unread) also exist.
- **CME rule cited.** #583 §1 quotes the semi-automated rule. This use is fully automated (Category A), so the A8/A9 routes govern.
- **CME $0.50/GB.** #583 attributes it to Smart Stream. The excerpts tie it to the WebSocket API page and repeat it for Smart Stream, so it is ambiguous.
- **Massive.** The KB line #583 relied on (individual plans cover your own scripts and trading) conflicts with Massive's own Market Data Terms §2/§5(d). The personal, non-professional licence wording #583 quoted comes from Massive's stocks page. History is 7+ years (pricing) or since 2017-04-03 (docs), not 5 years (the Developer tier).
- **tastytrade.** The $4.65/month non-professional CME bundle and the "CME Group bundle" are on no tastytrade source. Current tastytrade excerpts say non-professionals pay no data fees.
- **IBKR.** CME non-pro L1 is $1.25 or $1.55 in different excerpts, and the bundle waiver is $20 or $30 of commissions. #583's "$5 streaming" line was not seen. One line covers CME, CBOT, COMEX and NYMEX.
- **Ironbeam.** #583 omitted the $1,000 minimum balance. $249/month is a floor; the page says pricing varies by use case. The free non-professional data applies to Ironbeam's own platform; "other platforms" pay $3.00 per exchange.
- **Rithmic.** The "$100 monthly minimum per API user" is a 2013 forum post. FCM API fees now range from $20 to $100+, and L1 data from $2.55 to $3.00 per exchange.
- **Tradovate.** #583's $290–$500 CME figure is forum-sourced. The CME excerpts give $457 or $208 per DCM, so about $1,371 or $624 for three DCMs. #583 omitted the $1,000 balance and the $35 inactivity fee.

**Between or within official sources:**
- CME (paraphrased): the FAQ's rule that all non-display use is licensed directly with CME vs Schedule 5's A9 managed route through a provider; and the FAQ's rule that non-professionals license through their data provider vs its rule that semi-automated users license directly with CME. Excerpts give different wording for the AI clause's trade-signal item and different A1 tier amounts.
- CME direct products: WebSocket sequence numbers are per topic and weekly (overview) vs per session (message pages). The trade correction action is "update" (WebSocket) vs "change" (Pub/Sub).
- IBKR: real-time bar time is the bar start (current docs excerpt) vs the bar end (a summary of the deprecated page). Nightly reset is 00:15–01:45 ET vs 23:45–00:45 ET. The tick-by-tick limit is 3 vs 5% of market-data lines.
- Ironbeam: professional data $119.80 vs $135 per exchange. Its llms.txt says the API is free; its KB prices non-traders from $249. Two extractions of its API reference disagree on a REST history endpoint.
- Rithmic: the conformance environment is Rithmic Test (one page) vs paper trading (another).
- Tradovate: access tokens last 80 minutes (partner docs) vs about 90 (NinjaTrader docs).
- tastytrade: a third-party report of empty candle history vs the DXLink specification.

## 2. Licensing and eligibility points still assumptions

None of these is established by an official source. Each is a residual question in §4.

- **CME (all routes):** which route applies when the data source does not route the orders (A8 or A9); whether CME will sign an ILA, or Smart Stream's cloud agreement, with an individual; whether one ILA covers CME, CBOT and COMEX; the fee cadence, base ILA fee, setup, minimum term, audits and deposits; whether trading a prop firm's evaluation account removes non-professional status under the own-assets test; whether non-pro status changes the Category A fee; the scope of the 2026 AI/ML clause and the Synthetic Feed ban; whether raw messages and derived bars may be stored for audit without a derived-data licence; whether the funded-trader consent clause reaches a data subscriber.
- **P1 Massive:** that Futures Advanced licenses automated non-display decisions at all; that no separate CME licence is due from the individual; that the subscriber stays non-professional with a prop-firm destination; that the CME condition of an active futures trading account is met; cloud hosting; retention after the subscription ends (§8 requires deletion); that $199 is all-in.
- **P2 tastytrade:** that DXLink data may drive orders at another broker; that a prop evaluation account counts as the subscriber's own assets; that tastytrade's licence covers automated non-display use; that a read-only server meets the subscriber agreement's order-terminal condition; that a cloud server is an acceptable designated location; real-time API delivery for a funded non-pro account; private storage and retention.
- **P3 IBKR (both variants):** that the "Non-Display (API trading applications)" subscription covers this use without the subscriber's own CME licence; that orders at another broker are permitted; that a prop destination keeps non-pro status under the personal-investment-purposes test; the non-display fee; cloud hosting and storage; that a no-trading username can hold real-time data.
- **P4 Ironbeam:** whether its CME licence covers the use; that a prop destination changes nothing; real-time data on the read-only tier; the API data fee class; that the $1,000 is withdrawable; server-side order blocking; cloud and storage; no conformance for a data-only client.
- **P5 Rithmic:** the unpublished Market Data Subscription Agreement's treatment of headless automated use; who reports CME non-display (subscriber, Rithmic or FCM); non-pro status for a data-only or no-trading account and with a prop destination; a server-enforced data-only user id; conformance for a data-only app; cloud and storage under the agreement and the FCM's terms.
- **P6 Tradovate:** that the ILA requirement (excerpt) is current and complete; which CME category and unit apply; that an ILA-licensed subscriber may drive orders in a separate prop-evaluation Tradovate account; non-pro status; the 2026 CME updates; cloud and storage; that a key with reduced order permission blocks every order action and still gets data; that $1,000 applies only at key generation.

## 3. What the drafts drop and keep

**Dropped from every draft:** the bar-stamping convention, the fee-classification mechanics ((a1)/(a2)/(b)/(c)) and the deposit-versus-minimum arithmetic, the equivalence-test and rejection-rule wording, and any name of the firm, the rail or a program. Questions that a source already answers are not asked. One sentence keeps what §4 recording needs: "for each fee, say whether it is for the market data or the account, how often it is billed, and what is due at signup".

**Kept, where a source shows it matters:** individual non-professional status; automated non-display use; orders at a prop-firm evaluation account at another broker (D-Q2: disclose, in one plain sentence); the four symbols; and a cloud host only for P2 and P5 (and inside P1/P4/P6 Q6, which asks the cloud question itself). Each draft ends with a one-line reason for each kept sentence. Order follows D-Q3: CME first, then P1–P6. P6 keeps the same-broker wording.

## 4. Drafts

### 4.0 CME Group, market data licensing (send first)

> **Subject:** Non-display licence for an individual's automated trading program
>
> Hello,
>
> I am an individual (a natural person) and a non-professional trader. A program I run would receive real-time data for the front contracts of 6J and MNQ (CME), MYM (CBOT) and MGC (COMEX), and use it, with no display, to generate and send orders automatically. The data would come from a data vendor or broker, or directly from CME. The orders would go to a proprietary-trading-firm evaluation account held at a different broker from the data source. Nothing would be redistributed.
>
> Could you answer in writing, with links to the governing terms? Please write "none" for any fee or requirement that does not apply.
>
> 1. **Licence route.** Which licence applies: User Non-Display (A8) under my own ILA, Managed User Non-Display (A9) through the data source, or another category? Schedule 5 appears to require an A9 licensee to provide the subscriber's automated order routing to CME markets. Is A9 available when the data source does not route my orders?
> 2. **Status.** Does placing the orders in a third-party prop firm's evaluation account count as managing third-party assets, so that I am not non-professional? Does non-professional status change the Category A fee?
> 3. **Fees.** Please confirm that A8 is $457 per month per DCM in 2026 and $472 from January 2027 (A9: $208 and $215), so three times for CME, CBOT and COMEX. Is one ILA enough for all three? Is there a base ILA fee, setup fee, minimum term, deposit or audit obligation for an individual?
> 4. **2026 licence updates.** Does the ML/AI/LLM prohibition in the 2026 updates, including its item on automated generation of trade signals, apply to real-time data licensed for Category A non-display use, or only to data displayed on websites? Are 15-minute bars that my program computes internally, and never distributes, a Synthetic Feed? May I store the raw messages and those bars privately for audit without a derived-data licence?
> 5. **Direct products.** Please answer separately for (a) the real-time futures and options WebSocket API and (b) Smart Stream on Google Cloud:
>    1. May an individual sign the agreements each one requires?
>    2. Which entitlements or topics give real-time data for these four products?
>    3. What is the per-GB tier schedule, what exactly is metered, and is there a minimum or setup fee? Which product does the $0.50/GB starting price belong to? Please give a bounded monthly estimate, in GB and dollars, for trades only (and for top of book) on these four front months.
>    4. Does the credential (API ID or Google Cloud access grant) carry any order or account capability?
>    5. What connection or subscription limits apply? Does an open WebSocket survive token expiry? Is certification required for a data-only client?
>    6. Is each trade message one match event, not conflated? What do the update/change and delete actions mean for volume? What is the timestamp precision?
>    7. WebSocket: is anything replayed after a reconnect, and is the sequence number per topic per week or per session? Smart Stream: do trade messages carry a gap-detectable sequence number, and how are replayed messages told apart from live ones?
>    8. How is a trading halt signalled? On Smart Stream, is there a heartbeat or sequenced status message?
>    9. What is the typical and worst-case delay from match to delivery? I need every trade of a 15-minute interval within 30 seconds of its close. Are there maintenance windows inside the Sunday–Friday 18:00–17:00 ET session?
>    10. WebSocket: does subscribing to an expired or unknown contract month return an error? Smart Stream: does each product-group topic carry every contract month?
>    11. How are holiday early closes and DST changes shown: in messages, or only in your calendars?
>
> Thank you.

*Why each disclosure stays (for Joshua):*
- *Individual (natural person):* A8 and A9 are rates for a single natural person (CME fee list, Schedule 5 [excerpt]).
- *Non-professional:* CME's definition limits non-professional use to one's own assets (Information Policies [excerpt]); question 2 depends on it.
- *No display, automated orders:* this places the use in Category A non-display (non-display FAQ [excerpt]), which decides the licence.
- *Data from a vendor, broker or CME:* A8 and A9 differ by how the data is received (fee list, 2014 policies update [excerpt]).
- *Orders at a prop-firm evaluation account at a different broker:* D-Q2 ruled to disclose. A9 appears to require the data source to route the orders (Schedule 5 §11 [excerpt]), so this sentence decides the route and price.
- *Four symbols, three exchanges:* fees are per DCM (fee list [excerpt]), so it sets the multiplier.
- *Nothing redistributed:* keeps the Synthetic Feed question to internal use (ILA v5.02 [excerpt]).
- *Cloud host: omitted.* No CME source shows it changes the category; Smart Stream runs on Google Cloud by design.

### 4.1 P1 Massive, Futures Advanced

> **Subject:** Futures Advanced: licensing for automated (non-display) use
>
> Hello,
>
> I am an individual, non-professional trader considering Futures Advanced for real-time data on the front contracts of 6J and MNQ (CME), MYM (CBOT) and MGC (COMEX). A program would use the data, with no display, to make automated trading decisions. Its orders would go to a proprietary-trading-firm evaluation account at another broker. I have not opened an account. Could you answer in writing, with links to the governing terms?
>
> 1. Your Market Data Terms (§2 and §5(d)) limit use to display unless I am licensed for non-display use. Does Futures Advanced, or another agreement you offer individuals, license automated non-display trading decisions? If not, must I hold a CME licence myself?
> 2. With my orders going to a prop-firm evaluation account, am I still non-professional under your criteria and CME's? Are all four products in the real-time Futures Advanced stream?
> 3. Is $199/month the all-in cost, or are exchange or CME licence fees charged on top? Is there a setup fee? Please write "none" if not.
> 4. May I run the client unattended on a cloud server, and keep raw messages and derived bars privately for audit, including after the subscription ends (your Terms §8 asks for deletion on termination)?
> 5. On the futures WebSocket: is a per-minute bar sent once, or re-sent or revised later? Is trade `t` the exchange timestamp? Is bar `v` contract volume? How are busted or corrected trades signalled? After a reconnect, is anything replayed, or is REST the only backfill?
> 6. When is a futures per-minute bar sent after its minute closes, typically and at worst? I need every bar of a 15-minute interval within 30 seconds of its close. Is there a heartbeat, status or halt message, or a scheduled reset, on the futures WebSocket?
> 7. Do API keys expire? What does subscribing to an expired or unknown futures ticker return? Do the schedules entries include holiday early closes?
>
> Thank you.

*Why each disclosure stays:*
- *Individual, non-professional:* Futures Advanced is for non-professionals only, and the Terms condition the licence on personal, non-professional use (futures pricing page; Market Data Terms §1, §4.3).
- *No display, automated decisions:* Terms §2 and §5(d) make non-display use the licensing question.
- *Orders at a prop-firm evaluation account at another broker:* D-Q2. Massive's professional triggers include trading someone else's capital or sharing profits (KB, professional status).
- *Four symbols:* entitlement scope; per-product inclusion is unconfirmed.
- *Cloud host:* only in question 4, which the §2 screen (Q6) needs; no source shows it changes the plan.

### 4.2 P2 tastytrade Open API / DXLink

> **Subject:** Open API: using DXLink futures data for orders at another broker
>
> Hello,
>
> I am an individual, non-professional trader considering the Open API with DXLink for real-time data on the front contracts of 6J and MNQ (CME), MYM (CBOT) and MGC (COMEX). A program on a cloud server would use the data, with no display, to make automated trading decisions. Its orders would go to a proprietary-trading-firm evaluation account at another broker, not to a tastytrade account. I have not opened an account. Could you answer in writing, with links to the governing terms?
>
> 1. Your API Terms tie data use to transactions with tastytrade (Permitted Purpose; §8(3)). May DXLink data drive automated orders in a prop-firm evaluation account at another broker? Does that destination affect my non-professional status under the CME subscriber agreement's own-assets test (§1)? Does your CME licence cover this automated non-display use, or must I hold a CME licence myself?
> 2. For a funded non-professional account, does DXLink deliver real-time 6J, MNQ, MYM and MGC through the API? Which account permission is needed, and what are the streamer symbols for MYM and MGC?
> 3. Please confirm $0/month for non-professional real-time futures data and API access, with no inactivity or exchange-licence fee. What minimum balance keeps live data, and must it be maintained? For any fee, please say what it is for and how often it is billed.
> 4. If my OAuth grant has only the `read` scope, will the server reject placing, modifying and cancelling orders while still issuing quote tokens?
> 5. Can a personal grant's refresh token keep renewing access and quote tokens unattended indefinitely, with no inactivity expiry, re-consent or 2FA prompt? Is any review needed for a personal data-only app?
> 6. May the client run unattended on a cloud server, and how do I designate that location under the CME subscriber agreement (§3.2(i))? May raw messages and derived 15-minute bars be stored privately for audit, and for how long?
> 7. For futures 1-minute and 15-minute candles: is `time` the period start in UTC milliseconds? Can a candle change after its period ends? Is a candle sent for a no-trade interval? How is an exchange halt signalled? Are time-and-sale events, with trade size and correction and cancel flags, available?
> 8. After a reconnect, does re-subscribing with a start time backfill missed candles? Are snapshot rows and revised candles always flagged?
> 9. What is the typical and worst-case delay from candle close to delivery? I need every bar within 30 seconds of its interval closing. Which maintenance windows fall inside Sunday–Friday 18:00–17:00 ET, and what tells a client that an interval had no more trades?
> 10. Which time zone defines candle midnight alignment, and how are DST changes and holiday early closes shown? How far back do 1-minute and 15-minute candle requests reach? Is a continuous symbol offered, and what does DXLink return for an expired or unknown symbol?
>
> Thank you.

*Why each disclosure stays:*
- *Individual, non-professional:* the CME subscriber agreement tastytrade uses sets the non-professional tests (§1); professional futures data costs $480/month [excerpt].
- *No display, automated decisions:* the API Terms allow algorithmic trading only for transactions with tastytrade, so the use must be stated.
- *Orders at another broker, not tastytrade:* D-Q2. The Permitted Purpose and §8(3) tie data use to tastytrade transactions; the own-assets test may fail for a prop account.
- *Four symbols:* entitlement scope and MYM/MGC streamer symbols.
- *Cloud server:* the subscriber agreement limits use to designated locations and devices (§3.2(i)).

### 4.3 P3 Interactive Brokers (TWS API / IB Gateway and Client Portal Web API)

**Send the gate question alone.** Public sources answer Q5 negatively for both variants (§1 above; matrix P3a/P3b Q5). Whether to send at all is Joshua's call. If the reply confirms, the §3 rejection rule excludes both variants and nothing more needs asking.

> **Subject:** Unattended API login for an individual account
>
> Hello,
>
> I am an individual, non-professional trader considering your API for real-time CME Group futures data used, with no display, by an automated program on a server. Your documentation appears to say that IB Gateway needs a manual two-factor login each week, the Client Portal Gateway needs one each day, and OAuth is not available to individual accounts. Is there any supported way for an individual account to keep either the TWS API (through IB Gateway) or the Client Portal Web API authenticated unattended for weeks, with no manual login or 2FA prompt?
>
> Thank you.

**Follow-up, only if the answer is yes** (ask for answers separately for the TWS API and the Client Portal Web API):
1. My orders would go to a proprietary-trading-firm evaluation account at another broker. Does your "Non-Display (API trading applications)" CME subscription license that use, or must I hold a CME Category A licence myself? Does that destination affect my non-professional status?
2. Which subscription gives real-time 6J, MNQ, MYM and MGC through each API under the non-display selection? What is the all-in monthly cost, including any CME non-display fee? Is minimum equity still $500? Does an IB Gateway login reset the 60-day subscription-termination clock?
3. Can a second username with order permission removed on your servers still receive real-time futures data through each API?
4. May the gateway run on a cloud server, and may I store raw messages and derived bars privately for audit?
5. TWS API 5-second trade bars: is the time the bar start; is volume unfiltered exchange volume; is a bar sent for a no-trade interval; how are halts and busted trades shown? Web API: does it stream completed 1-minute bars or trades for CME futures, and is the history time the bar start?
6. After a reconnect that reports data lost, is missed data re-delivered, and are revised bars flagged?
7. Does an expired or unknown contract always return an error rather than a substitute?
8. What is the delivery delay, and what are the exact nightly reset and outage windows in ET?
9. What 1-minute history is available for the live contracts, and how are early closes and DST shown?

*Why each disclosure stays:* *individual, non-professional* — IBKR prices and classifies data by status (pricing, professional definition [excerpt]); *no display, automated* — IBKR lists "Non-Display (API trading applications)" as a separate subscription (user guide [page]); *orders at another broker* (follow-up only) — D-Q2; *on a server* — the gate question is about unattended running, which IBKR says needs a screen (initial setup [page]).

### 4.4 P4 Ironbeam API

> **Subject:** API for data only, no trading at Ironbeam
>
> Hello,
>
> I am an individual, non-professional trader considering your API for real-time data on the front contracts of 6J and MNQ (CME), MYM (CBOT) and MGC (COMEX). A program would use the data, with no display, to make automated trading decisions. Its orders would go to a proprietary-trading-firm evaluation account at another broker, so I would not trade at Ironbeam. I have not opened an account. Could you answer in writing, with links to the governing terms? Please write "none" for any fee or requirement that does not apply.
>
> 1. Does your CME licence cover this automated non-display use, with orders at another broker, or must I hold a CME Category A licence myself?
> 2. On the read-only/development tier, does the API stream real-time data for all four products? Which entitlements are needed, and what are the CBOT and COMEX symbol prefixes?
> 3. For data-only use with no trading at Ironbeam: what is the exact monthly API price, and the non-professional real-time data fee per exchange through the API? Any setup fee or minimum term? Is the $1,000 minimum balance fully withdrawable when I leave? For each fee, please say what it is for and how often it is billed.
> 4. Is a read-only/development API key rejected by your servers on every place, modify and cancel order request?
> 5. What is the bearer-token lifetime, and can authentication be repeated unattended indefinitely with no MFA? Is conformance testing required for a data-only client?
> 6. May the client run unattended on a cloud server, and may raw messages and derived bars be stored privately for audit?
> 7. For 1-minute and 15-minute time bars: is the timestamp the bar start or end? Is a bar re-sent while it forms? Are OHLC and volume built from trades only? How are busted trades applied? Is a bar sent for a no-trade interval, and how is a halt signalled? Does each bar message name its dated contract?
> 8. After a reconnect, can missed bars be backfilled, and how are backfilled bars and corrected trades flagged?
> 9. What is the worst-case delay from bar close to delivery? I need every bar within 30 seconds of its interval closing. Are there maintenance windows inside the session, and what marks a no-trade interval as complete?
> 10. Does an expired contract code return an error? What historical bar depth is available, and at what cost? How do time bars and trading-hours data reflect DST and holiday early closes?
>
> Thank you.

*Why each disclosure stays:*
- *Individual, non-professional:* data is free for non-professionals and $119.80–$135 per exchange for professionals (market data fees, fee schedule).
- *No display, automated decisions:* CME treats automated trading as Category A non-display [excerpt]; Ironbeam publishes nothing, so it must be asked.
- *Orders at another broker, no trading at Ironbeam:* D-Q2. The free API tier needs 5 contracts a month traded at Ironbeam; otherwise a priced read-only tier applies (API access KB).
- *Four symbols:* entitlement scope and per-exchange data fees.
- *Cloud host:* only in question 6 (Q6); no source shows it changes the plan.

### 4.5 P5 Rithmic R|Protocol (stage 1; FCM questions follow)

> **Subject:** R|Protocol for market data only
>
> Hello,
>
> I am an individual, non-professional trader considering R|Protocol for real-time data on the front contracts of 6J and MNQ (CME), MYM (CBOT) and MGC (COMEX). A program on a cloud server would use the data, with no display, to make automated trading decisions. Its orders would go to a proprietary-trading-firm evaluation account at another broker; no orders would go through Rithmic. Could you answer in writing? If an answer depends on the clearing firm, please say so.
>
> 1. Does your Market Data Subscription Agreement permit this headless, automated (non-display) use? Do you or the clearing firm report CME managed-user non-display, or must I hold a CME licence myself? Could you send the agreement text? It appears to be viewable only inside R|Trader.
> 2. Can one user ID receive real-time data for all four products at the same time, and with which entitlements? Please confirm their symbol and exchange codes, your front-month roll rule, and whether an expired code returns an error.
> 3. Does Rithmic bill an API user anything directly (API, conformance or history), or does the clearing firm set and bill every charge?
> 4. Can a user ID be set up so your servers refuse order-plant login and every order action? Which clearing firms offer that?
> 5. Is conformance testing required for an app that logs in only to the ticker and history plants? Can password login run unattended for weeks, with no MFA, forced logout or interactive re-signing of agreements? Can all four products stream on one session?
> 6. Does the agreement permit an unattended client on a cloud server, and private storage of raw messages and derived bars for audit?
> 7. For 1-minute and 15-minute time bars: is the bar marker the bar start or end, in UTC seconds? Is a bar sent once after close or updated in place, and can it be revised? How are busted or corrected trades signalled? Is a bar sent for a no-trade interval, and how is a halt shown?
> 8. Are live bar and trade messages sequenced? After a reconnect, is missed live data re-sent, or only available by replay? Are corrections flagged?
> 9. What is the delay from interval end to bar delivery, typically and at worst? I need every bar within 30 seconds of its interval closing. What maintenance windows fall inside Sunday–Friday 18:00–17:00 ET, and what signals that a quiet interval is over?
> 10. What minute-bar history can be replayed, and how are DST changes and holiday early closes reflected in bar timestamps?
>
> Thank you.

*Why each disclosure stays:*
- *Individual, non-professional:* users self-certify under Rithmic's agreement, and non-professional status needs an active futures account (Rithmic support and FAQ [excerpt]).
- *No display, automated decisions:* CME treats this as Category A non-display [excerpt]; Rithmic's agreement is not public.
- *Orders at another broker, none through Rithmic:* D-Q2; also no order routing fee applies.
- *Four symbols:* CME fees are per exchange and per session (Rithmic support [excerpt]).
- *Cloud server:* Rithmic's plug-in fee relief applies only on the same machine as R|Trader Pro (Rithmic support [excerpt]), so a cloud client needs its own billed session.

**Stage 2 (one named FCM, chosen by Joshua from Rithmic's answer; same opening paragraph).** Ask only the DEFERRED-TO-FCM items: (1) does a data-only account count as an active futures trading account for non-professional status, and do you bill CME non-display fees; (2) which exchange entitlements and API access you enable on the user ID, and the session count; (3) the all-in monthly cost with no trading at your firm, and every deposit, minimum balance, inactivity and withdrawal term, with refundability; (4) will you issue a data-only user ID, or disable order authorization on the server, and confirm it in writing; (5) cloud hosting and private storage under your customer agreement; (6) any history charge.

### 4.6 P6 Tradovate API, personal data-only account

> **Subject:** API market data on a personal account used only for data
>
> Hello,
>
> I am an individual, non-professional trader considering a personal live Tradovate account used only for API market data on the front contracts of 6J and MNQ (CME), MYM (CBOT) and MGC (COMEX). A program would use the data, with no display, to make automated trading decisions. The resulting orders go to a separate Tradovate account that belongs to a proprietary-trading firm's evaluation and is never linked to the personal Tradovate account I would open for this data. Could you answer in writing, with links to the governing terms? Please write "none" for any fee or requirement that does not apply.
>
> 1. Your API access article says real-time API data requires me to sign the CME Information License Agreement. Once I sign it, may I use the data for automated non-display decisions whose orders go to that separate evaluation account? Which CME category and fee apply (User or Managed User Non-Display, Category A), and is the fee per exchange? Does the evaluation-account destination change the ILA or sub-vendor answer?
> 2. With the CME licence in place, does API data cover all four products in real time? Is a Tradovate data subscription, or the free Level 1, also required?
> 3. For a live account used only for API data: must the $1,000 balance be kept, or only reached when the key is created? Does the $35 inactivity fee apply when no trades are placed? Are there any one-time fees? For each fee, please say what it is for and how often it is billed.
> 4. Can I create an API key whose order permission makes your servers reject placing, modifying and cancelling orders, while it still receives market data?
> 5. Can token renewal keep one session alive for weeks with no re-login? Do API users' passwords expire? Is conformance testing required for a data-only app?
> 6. May the client run unattended on a cloud server, and may raw messages and derived bars be stored privately for audit, under your terms and the CME ILA?
> 7. For chart minute bars (size 1 and 15): is the timestamp the bar start, in UTC? Is the forming bar updated in place, and is a closed bar ever revised? Are OHLC and volume from exchange trades? How are busted trades signalled? Is a bar published for a minute with no trades, and how is a halt shown? Does an expired or unknown symbol return an error or a substitute, and does every chart message identify the dated contract?
> 8. Are bars or trades ever revised after delivery, and how are revisions flagged?
> 9. What are the typical and worst-case delays from bar close to delivery? I need every bar within 30 seconds of its interval closing. What maintenance windows fall inside Sunday–Friday 18:00–17:00 ET, and what signals that a quiet interval is over?
> 10. What historical minute-bar depth does the API give for these contracts, and how are DST changes and holiday early closes reflected in bar timestamps?
>
> Thank you.

*Why each disclosure stays:*
- *Individual, non-professional:* Tradovate's data rates depend on status, and CME's non-display rates are for a natural person (non-pro data rates KB; CME fee list [excerpt]).
- *No display, automated decisions:* decides the CME category the ILA must carry (non-display FAQ [excerpt]).
- *Same-broker destination, never linked:* D-Q2 with #583's P6 same-broker wording. Tradovate says prop and evaluation accounts cannot get API access [excerpt], so the separate personal account must be explicit.
- *Four symbols:* entitlement scope; CME fees appear to be per exchange.
- *Cloud host:* only in question 6 (Q6); Tradovate's IP and device limits imply servers are expected, and no source shows it changes the plan.

## 5. Recording

Replies are recorded under the [#583 note §4](2026-10-01-feed-provider-questions-DRAFT.md#4-recording-the-answers) rules, one row per variant and question, with the matrix row's source kept beside the reply. A row answered here by a public source still needs Joshua's verification on the page (the "verified by the operator" field).

## 6. Verification of this note

- Base: `origin/main` at `e9fade0`; branch `claude/feed-questions-narrowed`; worktree under `.claude/worktrees/`.
- Research: seven parallel WebSearch/WebFetch passes, one per provider, on 2026-10-03. No vendor contact, form, login, account, trial, cookie acceptance or mailbox access. Fetch failures are listed per provider in the matrix.
- Owner reads: the #583 note (all), the H8 note §5, Track A plan §3.2, and the frozen equivalence spec §3, §4.3, §6 and §7. The locked feed-equivalence spec was read and not edited; its technical content concerns an earlier MT5/TV comparison.
- Link check and gates: see the PR body.
