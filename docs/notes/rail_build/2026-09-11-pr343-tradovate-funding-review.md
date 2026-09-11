# PR 343 review — whether to fund a personal Tradovate account

**Reviewed:** 2026-09-11  
**Object:** PR #343 (`claude/o4-production-feed-a-prime`) and its proposed
option A′ production-feed ruling  
**Decision status:** advisory review only; no account-opening, spend, feed,
deployment, emission, or arm authority

## Bottom line

**PR #343 has not established that a personal live Tradovate account is the
best production-feed candidate, and funding it now is not the best next action
for making the accepted configuration deployable.** The two propositions are
different:

1. **Provider choice:** A′ is preferable to the narrow alternatives scored in
   PR #343, but that menu omitted at least three plausible brokerage APIs and
   CME Group's direct API. Tastytrade and Interactive Brokers have credible
   lower-capital or lower-recurring-cost shapes and must be checked before A′
   can be called best.
2. **Sequence choice:** funding does not make the book deployable. It only
   satisfies one external prerequisite for building and validating the source
   adapter. The accepted configuration still has a deliberately unperformed
   qualification, four private strategy adapters and parity work, rail/runtime
   extensions, source-equivalence testing, M1 resolution, an execution
   fingerprint, the sole n3 run, and a separate deployment GO.

The recommended present ruling is therefore **NO-GO on funding today; demote
A′ from selected to SHORTLISTED and run the bounded vendor verification below.**
This is not a rejection of A′. It is a correction to an incomplete comparison.

## What the original comparison got right

Against the alternatives scored in the S2b ADR, A′ has the strongest
cost/capability fit:

- the eval sub-account cannot be relied on for direct API access;
- a plain licensed third-party real-time feed restores approximately the same
  recurring spend that was just retired;
- delayed feeds violate the existing bar-age and staleness locks;
- the TradingView-webhook option has the recorded non-display-use terms
  conflict; and
- free sources are delayed, unlicensed for this use, or both.

A′ also keeps execution and data-account identity separate: the personal
account supplies bars while CrossTrade continues to target the Tradeify
sub-account. That separation is desirable only if the adapter is demonstrably
read-only and the personal account is never linked into the execution path.

## Expanded production-feed scan

This scan used vendor documentation available on 2026-09-11. Prices and account
eligibility remain operator-verified facts at purchase time. A row is not
viable merely because it exposes an API: the source must deliver current,
licensed 1-minute bars for 6J, MGC, MYM and MNQ to a headless Linux service,
survive reconnects, and avoid an unattended-login ceremony.

| Candidate | Verified capability | Cost/capital visible today | Material issue | Disposition |
|---|---|---|---|---|
| **Tastytrade Open API / dxFeed** | Official guide exposes a DXLink WebSocket, futures symbols, 15-minute OAuth access tokens and a 24-hour quote token; fully onboarded customers only. | API/data charge and minimum balance were not established by the readable primary pages. | The marketed API has full read/write trading access; scope restriction, all-four contracts, real-time entitlement, OHLC/bar events, unattended refresh and account-funding requirement need written confirmation. | **Best challenger; verify first.** |
| **Interactive Brokers** | Official pricing covers CBOT/CME/COMEX/NYMEX top-of-book; Web/TWS APIs support futures data. | $500 minimum equity to keep data active; $10 US snapshot/futures base plus $5 streaming add-on on the displayed non-professional schedule. | Client Portal/TWS Gateway and brokerage-session authentication are a much heavier always-on deployment; permissions are order-capable. Prove unattended renewal and native/derived 1-minute bars before considering it. | **Economic challenger; operationally conditional.** |
| **Ironbeam REST/WebSocket API** | Official docs expose WebSocket quotes, trades and trade bars, bearer auth, exchange-entitlement discovery, and a documented reconnect rule requiring a new `streamId`. | Public API pages did not establish account minimum, API charge or complete data charge. | Username/password/API key authenticate an API that also places orders; exact bar-close semantics, entitlements, pricing and read-only restriction remain unknown. | **Request a quote; do not fund yet.** |
| **CME Group direct real-time API / Smart Stream** | CME advertises direct real-time futures/options API and cloud WebSocket products. | Retail/self-service price and entitlement terms were not readable; Smart Stream is presented as an enterprise/cloud data product. | May require commercial licensing/onboarding and may not be economical for one daemon. | **RFI only.** |
| **TradeStation API** | Official site documents REST/JSON, real-time streaming and futures from a brokerage API. | No API subscription charge, but the current official page states a **$10,000 funded-account minimum** for an API key. | Ten times A′'s parked capital and order-capable credentials. | **Dominated for this use.** |
| **Massive Advanced** | Official page covers CME, CBOT, NYMEX and COMEX with real-time WebSockets and minute aggregates. | $199/month. | Clean data-only secret, but restores the retired recurring run-rate. | **Safe fallback, not cost leader.** |
| **Databento paid plan** | Existing adapter experience; official site supplies CME Globex real-time data and OHLCV through client libraries. | Paid-plan live access; the repo records the relevant plan at approximately $199/month and retired. | Reverses an explicit cost decision; reauthorization required. | **Fallback only.** |
| **IQFeed / CQG / Barchart / dxFeed direct** | Each markets futures data or an API. | A complete, current, self-service price for a headless cloud entitlement was not established. | IQFeed's official developer page requires a Windows executable/socket client; CQG is broker/commercially sponsored; Barchart and direct dxFeed require sales confirmation. | **No evidence they beat the shortlist.** |

Primary pages: [tastytrade streaming guide](https://developer.tastytrade.com/docs/guides/stream-market-data/),
[tastytrade Open API](https://tastytrade.com/api/),
[IBKR market-data pricing](https://www.interactivebrokers.com/en/pricing/market-data-pricing.php),
[Ironbeam API](https://www.ironbeam.com/api/),
[Ironbeam WebSocket guide](https://www.ironbeam.com/how-to-subscribe-real-time-market-data-ironbeam-websockets/),
[Ironbeam API reference](https://docs.ironbeamapi.com/),
[CME market-data APIs](https://www.cmegroup.com/market-data/market-data-api.html),
[TradeStation API](https://www.tradestation.com/platforms-and-tools/trading-api/),
[Massive futures](https://www.massive.com/futures),
[Databento futures](https://databento.com/futures), and
[IQFeed developer interface](https://www.iqfeed.net/dev/).

### Important comparison correction

The security distinction in the original A′ versus third-party comparison was
too coarse. Tradovate, tastytrade, IBKR, Ironbeam and TradeStation are all
brokerage-backed APIs unless the vendor can issue a technically enforced
market-data-only credential. Merely promising not to call order endpoints does
not turn a full-write credential into a data-only secret. Massive, Databento
and a direct licensed feed have the safer credential boundary; that benefit
must be priced explicitly rather than omitted.

### Bounded verification before selecting a provider

Send the same written questions to **tastytrade, Ironbeam and Tradovate**, and
check the corresponding IBKR documentation, without opening or funding an
account:

1. Can a non-professional customer consume real-time 6J, MGC, MYM and MNQ data
   from a headless Linux service for internal algorithmic decision-making?
2. What are the all-in monthly API and CME/CBOT/COMEX entitlement fees, minimum
   funded balance, inactivity fees, and withdrawal constraints?
3. Is there a market-data-only OAuth scope/API key that cannot place, modify or
   cancel orders? If not, can order permission be disabled at the account or
   API-user level?
4. Does the stream publish completed 1-minute OHLCV bars with exchange/event
   timestamps, or must the client aggregate trades? Are historical backfill and
   correction events available after reconnect?
5. Can authentication and token renewal run unattended for weeks without a UI,
   MFA prompt, daily brokerage login or desktop gateway? What session caps
   apply?
6. Are cloud/VPS use, local persistence of derived 1-minute bars, and use as an
   input to automated signals permitted under the subscriber agreement?

Reject any response that leaves licensing, all-four-symbol coverage,
unattended authentication, or the effective ability to disable order actions
ambiguous. Then run a paper/demo spike only for candidates that survive.

## Why funding is not yet the deployability bottleneck

The accepted configuration record explicitly says that operator acceptance did
not establish technical qualification or deployment authority. Track B's own
inventory says the rail cannot yet express the four-leg book and lists the
strategy adapters, policy/runtime controls, replay, parity, calendar, symbol,
snapshot, and execution-feedback work that remains. Its dependency graph also
places the feed behind a separate Track A delivery and requires a frozen
feed-equivalence successor test before the live integration test.

PR #343 itself makes A9 off the M1 critical path. Consequently, opening the
account early does not accelerate the current Track A ceremony and cannot turn
the accepted research configuration into a deployable configuration by itself.
It starts recurring fees and exposes order-capable brokerage credentials before
the campaign has demonstrated that the fixed book survives its earlier
qualification gates.

## Blocking defect in the proposed signup instruction

PR #343 tells the operator to subscribe to **CME and COMEX** data for all four
adapters. That list is incomplete for the fixed book as named in Track B:

| Leg | Contract family | Exchange entitlement to verify |
|---|---|---|
| Aegis | 6J | CME |
| Vanguard | MGC | COMEX |
| Striker | MYM | **CBOT** |
| ORB | MNQ | CME |

The operator instruction therefore cannot safely be executed as written. The
signup checkpoint must enumerate CME, COMEX **and CBOT**, or select and verify a
bundle that explicitly covers all three. Account funding without the MYM/CBOT
entitlement would still leave one of the four production adapters without its
required source and could make a quoted low-cost estimate misleading.

## Required readiness checkpoint before funding

Fund only after one short, explicit checkpoint records all of the following:

1. **Campaign viability:** the fixed K=1 book has passed every qualification
   gate that does not require a live source, so feed spend is the actual next
   blocker rather than speculative inventory.
2. **Build readiness:** the source-adapter spec (A9 or its superseding packet)
   is frozen far enough to name the exact selected-provider endpoints,
   token-renewal behavior, reconnect/staleness behavior,
   route-label-to-dated-contract mapping, secret fields, and test plan. Mocked
   protocol tests need not wait for funded credentials.
3. **Primary signup verification:** the operator confirms in the actual account
   UI or written vendor terms the API eligibility, current fee, minimum equity,
   token lifetime, concurrent-session behavior, and whether market-data access
   is permitted when the account is used for data only. The bounded comparison
   above must be complete; PR #343 acknowledges that several A′ facts are
   currently second-hand.
4. **Complete entitlements:** the selected subscriptions cover CME, COMEX and
   CBOT for 6J, MGC, MNQ and MYM respectively, with the actual total monthly
   cost recorded before purchase.
5. **Credential containment:** credentials are operator-staged, volume-only,
   excluded from logs and images, and exercised only by an allowlisted
   market-data client. No order endpoint is implemented; no separate feed
   account is linked to CrossTrade; withdrawal/closure is the brokerage-account
   rollback where applicable.
6. **Immediate-use window:** an owner and time window are booked for live auth,
   subscription, all-four-symbol receipt, reconnect, staleness, and TB-I5
   equivalence checks. Do not start fees merely to leave the account idle.

## Decision rule

- **If tastytrade proves real-time, all-four-symbol, headless use with no greater
  secret authority and lower capital/run-rate than A′:** select it, amend the
  S2b source row, and build its adapter before spending on Tradovate.
- **If no challenger clears every mandatory fact and the A′ checkpoint passes:**
  fund Tradovate. A′ remains the best fully costed brokerage route in the
  current record, but not yet the best demonstrated route.
- **If the book fails an earlier qualification gate:** do not fund; the feed no
  longer unlocks a deployable book.
- **If API/data eligibility, all-three-exchange coverage, or read-only
  containment cannot be confirmed:** do not fund and re-price a data-only
  licensed provider. The extra recurring cost buys a materially safer secret
  boundary and may then be rational.

This staged rule preserves A′ as a credible fallback without mistaking the
first priced option for the best option, account funding for deployment
readiness, or an application-level promise not to trade for a read-only
credential boundary.

## Condensed checklist while funding is deferred

- [ ] **Record the deferral:** PR #343 must not leave A′ presented as funded,
  connected or finally selected; no account, subscription, credentials or A9
  provider implementation yet.
- [ ] **Finish Track A without a live feed:** implement and Linux-validate the
  option-D controlled input, deploy the daemon inert, run the attended M1
  ceremony, obtain operator signoff and reach M1 `RESOLVED`; never arm.
- [ ] **Run Track B's source-independent work:** regenerate the missing private
  inputs, accept the locked specs, intake every reachable size/mode, build the
  four private adapters, prove parity, implement the offline rail/runtime
  controls, and complete the fixed-book legality/n1/n2 qualification. Stop if
  the K=1 book fails; a feed would no longer unlock this deployment.
- [ ] **Close pre-feed operational gaps:** freeze the forward calendar and
  closure overlay; resolve lifecycle/protection state; verify all four
  CrossTrade ticket symbols; implement dedupe, capacity, execution feedback,
  EOD flattening, restart recovery and fail-closed interlocks in dry-run/inert
  form.
- [ ] **Prepare provider-neutral feed gates:** freeze the adapter contract and
  the four-symbol TB-I5 feed-equivalence test, including bar-close timing,
  session/timezone, roll mapping, corrections/backfill, reconnect and staleness.
- [ ] **Near the actual feed gate, compare vendors:** obtain written answers
  from tastytrade, Ironbeam and Tradovate; verify IBKR's unattended-auth shape;
  compare all-in cost, capital, CME/COMEX/CBOT coverage, licensing and a
  technically enforced read-only boundary.
- [ ] **Return for one funding decision only when needed:** the fixed book has
  survived every source-independent gate, one provider clears every mandatory
  fact, its adapter is ready for immediate live validation, and an owner/time
  window is booked for subscription, all-four-symbol receipt, reconnect,
  staleness and TB-I5. Funding authorizes data validation only—not deployment,
  emission, arming or trading.
