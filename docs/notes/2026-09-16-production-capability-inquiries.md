# Production capability inquiries and resolution criteria

Status: Tradeify, CrossTrade and Tradovate inquiries submitted; substantive
provider confirmation pending.
September 16, 2026.
Companion: [feasibility decision record](2026-09-16-tradeify-production-feasibility-decision.md).
These inquiries request facts about the incumbent Tradeify Tradovate DEMO route.
They authorize no trades, purchases, migrations or changes to governing contracts.
Insert account identifiers only in the provider's authenticated support channel.

## Submission log

- Tradeify: settlement inquiry sent through the recognized-user Intercom support
  conversation at `https://help.tradeify.co/en`. Message visible in the conversation.
  AI responder claimed no formal close statement/API exists, citing only the
  trading-day article. This is not accepted capability evidence. A follow-up was
  sent requesting human account-specific confirmation of the unanswered questions.
  The AI then confirmed it would connect the conversation to the support team.
- CrossTrade: contact form at `https://crosstrade.io/contact` prepared with the
  uncertain-request and protection inquiries combined. Submitted using the reply
  email Joshua supplied. The form cleared and displayed a success acknowledgment
  saying the team would be in touch shortly. No ticket number was displayed.
- Tradovate: official legacy request URL redirected to
  `https://support.tradovate.com/s/contactsupport?language=en_US`. Form prepared
  with settlement and native-protection inquiries, category Web Trading Platform.
  Joshua completed submission. The confirmation page was independently inspected
  and states that the inquiry was successfully submitted to Customer Support.
  No case number was displayed. No duplicate submission was made.
- No attachments, credentials,
  account changes or trades were sent. No ticket number has yet been exposed.

## 1. Tradeify / Tradovate: settlement evidence

### Tradovate response received

Read the open email dated September 16, 2026 at 19:38 Eastern, subject
"Re: Tradeify DEMO: close-report evidence and native protection capabilities".
The sender identifies the response as AI-generated (Tradovate Assistant).

- It identifies Account Balance History as session-ending balance/PNL and Cash
  History as balance changes, consistent with candidate sources already examined.
- It explicitly cannot confirm exact 17:00 close equity with open-position
  valuation, report timezone/filter/DST semantics, retention, revision tracking,
  automatic availability or retrieval of the September 14 close.
- It cannot confirm the required per-fill atomic protection reduction or native
  delayed trailing semantics. Generic bracket, OCO and trailing support does not
  establish those guarantees.
- It directs provider-specific account entitlements/records to the prop firm.
- It offers human escalation by replying "Agent". No reply was sent during this
  read-only email inspection.

Disposition: no capability upgraded to QUALIFIED or newly declared UNSUPPORTED.
This is an explicit limit of the assistant's documentation-based answer, not a
human engineering determination that the capabilities do not exist. Human
platform/API confirmation and Tradeify account-source confirmation remain needed.

Suggested message:

> I am qualifying automated operation of my existing Tradeify account using
> Tradovate. My report menu has Orders, Position History, Cash History, Order
> Details, Fills and Account Balance History, but no Client Statements report.
> Please identify the account-entitled report or supported API that establishes
> equity at the 17:00 America/New_York account close, including open-position
> valuation, commissions and adjustments. If the account is flat, what historical
> source proves its positions at that boundary rather than its current positions?
>
> Please confirm the timezone of exported timestamps separately from the platform
> clock, whether date filters select event timestamps or business/trade dates,
> whether both bounds are inclusive, and how DST is represented. Which source
> supplies complete cash adjustments from inception, including later corrections?
>
> Can the September 14, 2026 21:00 UTC close be retrieved for this account? For
> future sessions, when is the finished-close report normally available, how are
> later revisions identified, and can it be obtained automatically before my
> approximately 18:00 Eastern review? Please provide report names, access steps,
> retention limits and documentation. A sample can be provided through this
> authenticated channel. Please do not change the account or enable paid access.

Acceptance: account entitlement + source semantics + original actual close record
and adjustment history + verifier rehearsal. An estimate of availability is not
an observed timing qualification. A current equity snapshot, purchase receipt or
later empty position list does not substitute for the historical fact.

If no accepted production chain exists, failure to retrieve September 14 does not
make that rehearsal date mandatory. Qualify prospective collection and the existing
initial-B7 procedure. If a production chain exists, preserve its predecessor and
resolve its specific gap. Neither answer authorizes a new chain in this task.

## 2. CrossTrade: uncertain requests and account-wide closure

Suggested message:

> I need a supported reconciliation procedure for the Tradovate destination when
> an order request times out after transmission and no broker order ID is returned.
> I understand that a client label is not an idempotency key. Please identify a
> durable request lookup/receipt, processing-state record, or supported fence that
> establishes either the resulting broker obligation or that the original request
> can never be accepted later. Absence from current orders is insufficient for my
> use case. Does any request expiry apply before broker acceptance, and what record
> proves its completion? Order TIF/expiry alone would not answer this question.
>
> Does a documented administrative procedure terminate queued/in-flight webhook
> work and managed triggers, and provide evidence that termination is effective?
> Please distinguish disabling future submissions from draining already accepted
> requests, reconnect/replay work and broker orders. Do not perform these actions.
>
> Which supported records cover placements, cancels, amendments, partial fills,
> protection changes and provider-managed actions across session rollover and
> disconnects? Please state retention, completeness boundaries, revisions and
> how to recover missed records. My UI currently shows no monitors or copiers;
> that does not establish absence of per-order managers or delayed work.
>
> Please supply exact endpoint/procedure names and applicable limits. I do not
> want duplicate order retries or a timeout-based assumption that a request failed.

Acceptance: supported semantics for the original request plus actual retained
trace, account scope and consumer reconciliation. A successful sample alone cannot
establish a guarantee about late delivery. A provider-assisted terminal incident
procedure can be evaluated; phone attendance alone is not such a procedure.

If unavailable: keep unresolved obligations and activation blocked. Compare a
specific entitled alternate route against the same requirements, or explicitly
review a narrower replacement contract and its residual risk. Waiting overnight,
disconnecting a client, revoking a key or seeing flat positions is not presumed to
terminate work already accepted elsewhere.

## 3. CrossTrade / Tradovate: protection semantics

Suggested message:

> Before implementing a four-strategy adapter, I need to establish two capabilities
> on the existing Tradovate DEMO route:
>
> 1. Can a close target specific entry-fill quantities while ensuring their linked
> protective orders are reduced/retired with every partial execution, with no
> executable excess or reverse orphan during the transition? Other strategy lots
> and their protection must remain intact. Please name the native primitive and
> explain races with a protective fill and partial/rejected close. An opposite
> market order followed by cancel/replace does not meet this requirement.
> 2. Is there a broker-native delayed trailing activation with per-fill activation
> threshold, favorable-price anchor, fixed-stop floor and OCO sibling handling?
> Amendments must preserve already earned trailing protection. Please distinguish
> continuous native trailing, broker multibracket strategies, and CrossTrade/NT8
> managed triggers, and explain additional-fill and restart behavior.
>
> Please give exact supported fields/endpoints and limitations. If either is not
> available, an explicit unsupported answer is useful. Do not enable features,
> alter existing orders or place test trades.

Acceptance: each capability must map to the retained rail contract and be supported
on this account, followed by separately scoped operator-run traces. Ordinary OCO
availability is not proof of atomic reduction for an independent scoped close.

Current source findings:

- [CrossTrade execution internals](https://crosstrade.io/docs/webhooks/tradovate-advanced)
  distinguish provider-managed activation from continuous native trailing. This
  is a real execution difference; changing field names cannot close it.
- [Tradovate API reference](https://api.tradovate.com/) exposes order strategies,
  OCO/OSO and trailing types. Their existence does not demonstrate either requested
  guarantee or direct API entitlement for the incumbent account.
- [Tradovate report help](https://tradovate.zendesk.com/hc/en-us/articles/16653178768275-How-Can-I-Run-a-Report-Within-Tradovate-s-Platform)
  lists client statements generally; the observed account menu does not. Resolve
  entitlement before designing an automated statement collector.

## 4. Work order and stop rules

1. Confirm whether the deployment has any accepted production settlement chain.
   This determines whether historical repair or prospective initial qualification
   is the applicable path. Preserve the rehearsal as a rehearsal.
2. Obtain the three capability responses. The normal-protection response is the
   first execution-route decision: do not build a recovery adapter for a route
   already known not to execute the book's required behavior.
3. Where supported, retain actual account evidence and run a non-authorizing
   settlement rehearsal. Measure close publication, collection and review timing
   against the evening requirement. Do not pre-approve unknown close facts.
4. Prepare real execution characterization only for supported candidate primitives,
   naming account, environment, symbol, bounded quantity, intervention and teardown.
   No real order test is authorized or executed by these inquiries.
5. If unsupported, present the exact route or contract choice. Do not silently
   replace native activation, atomic protection or causal closure with weaker
   behavior. No migration is selected merely because it uses fewer intermediaries.

The evening workflow remains a separate contract integration: approval binds one
session and exact release, activation uses fresh automatic checks, and incidents
end automation for that session. The source must support unattended acquisition;
a manual report required each morning would fail the user's operating requirement.
