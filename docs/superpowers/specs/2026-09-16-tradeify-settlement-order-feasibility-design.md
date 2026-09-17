# Tradeify settlement and ambiguous-order feasibility

> **Design amendment, 2026-09-17 UTC:** The [bounded platform-protection incident contract](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md) records the operator-directed revision: fence new strategy commands, allow only qualified pre-existing protection through isolated signal/control failures, retain uncertain-order blocks and prohibit same-session strategy reactivation. Reassess ordinary ATM plus a thin bridge under that boundary. Full governing-contract propagation is pending; no capability verdict or deployment approval changes here.

Date: 2026-09-16. Status: **OPERATOR-APPROVED BASE DESIGN; EVENING EXTENSION FOR REVIEW**.

Approval: Joshua instructed, “I approve this design. commit it and open a pr”.
This approves the design and its publication. Implementation, reconciliation of
the affected governing contracts, actual capability qualification and live
authorization remain separate; this document changes no runtime behavior.

Extension authority: Joshua subsequently instructed, "Close the
production-feasibility gaps described in #411, add the evening approval
requirement to the operating design". Section 6.1 records that requirement and
its proposed detailed contract. Earlier approval does not ratify these new
mechanics or amend production authority implicitly. Investigation results are in
the [capability decision record](../../notes/2026-09-16-tradeify-production-feasibility-decision.md).

Purpose: determine whether the incumbent account and execution route can support
the accepted portfolio, then select the smallest feasible attended release.
The optimization priority is lower architecture complexity and shorter time to
deployment. This is a bounded evidence and design slice, not implementation or a
claim that production capabilities have been qualified.

## 1. Decision and scope

Preserve PR 409's durable account owner and offline integration. Before building
more production recovery machinery, resolve three questions:

1. Can the account provide an admissible initial anchor and each required close?
2. Can every possibly effective order request be resolved, including requests
   whose response was lost and actions by the operator or provider services?
3. Can the route execute the accepted book's normal protection and close semantics?

The recommended first release, conditional on all three, is one incumbent
account, the fixed four-leg book, one execution owner, attended sessions, manual
incident intervention, and **no same-session reactivation after an incident**.
That last restriction is approved here as a design amendment; propagation to the
governing halt/resume contract and implementation remain owed.
It reduces restart transitions; it does not reduce reconciliation obligations.

Deliver one capability decision record with evidence references and a selected
release profile. Do not create another service, general workflow engine, evidence
database or parallel source of trading permission for this slice.

Specification approval does not authorize trades, provider spending, account
migration, support messages, deployment, arming or changes to accepted portfolio
behavior. Actual capability tests that transmit orders remain separately scoped
and operator-executed. Existing approvals are reused within their actual scope.

## 2. Ground truth and authority

**Execution update:** PR #409 merged as
`845fb13ed2141482649627f5b78a51f4cadbd61d`, final branch head
`3cf42e43f4f41f0b1e66d7510d2c55cda57c21b9`. Section 6.1 and the decision record
use an isolated worktree at that merge. Base design: PR #411 at
`d7709adb7d3816b3beaf44506d56138f3ae6f067`. Historical drafting references below
retain their provenance; the extension reads the merged source/contracts.
No earlier validation count is represented as a fresh test run.

PR [409](https://github.com/Joshua-Asante/first-passage/pull/409), published head
`567a583a3da4e752d9cadb979c3a0aee74eb6925`, is the integration reference observed
while drafting. Its acceptance boundary is offline synthetic engineering; actual
account-close and broker qualification remain open. Its description names an
older validation revision, so this specification does not certify current tests.
The local PR worktree contains ongoing edits; none were changed by this task.
Execution must pin the final accepted successor revision and assess affected
interfaces rather than assuming the observed head remains current.

Sources read directly include `book_policy.py`, `book_sizing_context.py`,
`book_settlement.py`, and the account-owner interfaces. The candidate four-leg
policy in `book_policy.py` is distinct from historical `core/dd_protection.py`.
No sizing constant, allocation, strategy, protection law or schedule changes here.

Governing contracts at the inspected PR revision:

- [Attended settlement](https://github.com/Joshua-Asante/first-passage/blob/567a583a3da4e752d9cadb979c3a0aee74eb6925/docs/spec/2026-09-15-tradeify-attended-settlement-contract.md): evidence-backed operator acceptance, authenticated chain, corrections and restore.
- [Attended halt/resume rev9](https://github.com/Joshua-Asante/first-passage/blob/567a583a3da4e752d9cadb979c3a0aee74eb6925/docs/spec/2026-09-14-tb-s3-halt-resume-contract.md): intervention fences every runtime mutation; attendance and reconciliation remain required.
- [Rail extension, section 2e](https://github.com/Joshua-Asante/first-passage/blob/567a583a3da4e752d9cadb979c3a0aee74eb6925/docs/spec/2026-09-12-c1-multi-leg-rail-extension-spec.md): recovery E1 coherent acquisition, E2 complete history/identity, E3 unresolved requests, K1 quiescence and normal L2 primitives.
- [Initial account snapshot](https://github.com/Joshua-Asante/first-passage/blob/567a583a3da4e752d9cadb979c3a0aee74eb6925/docs/spec/2026-09-12-tradeify-account-snapshot-seal-contract.md): B7 and initial peak authority.

Use `settlement-S*`, `recovery-R*` and `normal-N*` labels below. B7's E1/E2/E3
attachments are not the recovery contract's E1/E2/E3 guarantees.

Known findings are bounded evidence, not timeless provider judgments:

- The [September 14 broker probe](https://github.com/Joshua-Asante/first-passage/blob/39f47682208b21c28dd7abda9baac73e99e6be6b/docs/notes/2026-09-14-crosstrade-evidence-capability-probe.md), retained at its separate runtime-owner revision, demonstrated reads and stored fill pagination, not complete history or global request resolution. Historical order lookups failed.
- The [account producer probe](https://github.com/Joshua-Asante/first-passage/blob/567a583a3da4e752d9cadb979c3a0aee74eb6925/docs/notes/2026-09-15-packet1-producer-feasibility.md) demonstrated balance/cash exports, not historical closing equity or boundary flatness.
- Subsequent account inspection did not resolve the September 14 close. Its supporting note, `docs/notes/2026-09-15-account-timezone-operator-clarification.md`, was local and uncommitted at drafting and is not published by this PR. This is a reported observation, not independently retrievable acceptance evidence. Operator-provided report labels/endpoints remain distinct from verified source semantics.
- Current [CrossTrade fill-history documentation](https://crosstrade.io/docs/api/tradovate/get-fill-history), inspected September 16, describes periodic capture without guaranteed deadlines, no prior-session backfill through that endpoint, and no completeness implication from exhausted pagination.
- [Tradovate report documentation](https://partner.tradovate.com/resources/admin-dashboards/reports) is a source-discovery aid; partner capabilities do not prove entitlement on this account. [Tradeify's account-day definition](https://help.tradeify.co/en/articles/10468225-what-is-a-trading-day) does not establish an individual report's timezone or close valuation.

## 3. Work boundary and evidence interface

The coordinator owns the combined decision. The existing settlement verifier
owns close acceptance; the account owner owns execution obligations and permission.
The observation collector retains source observations without certifying absent
guarantees. Joshua owns account-only facts, signing and any approved platform
actions. A signature authenticates an assertion; it does not create its evidence.

Each capability row in the single decision record contains:

| Field | Required content |
|---|---|
| Requirement | ID below, exact consuming contract and allowed use |
| Producer | Named report/endpoint/procedure, account/environment and entitlement |
| Source semantics | Effective time, query bounds, timezone, coverage, ordering, corrections and retention |
| Evidence | Private original-byte locations/digests, capture times, query context, relevant code/route revision |
| Verification | Source statement plus observed trace and expected result; gaps explicitly identified |
| Outcome | `QUALIFIED`, `UNPROVEN`, `UNSUPPORTED`, or `AMENDMENT_REQUIRED` |
| Next disposition | One precise missing fact/test, or stop/change-route/change-contract recommendation |

`QUALIFIED` requires actual evidence for the stated account, route and use plus
the applicable verifier/consumer acceptance. Documentation, mock success and
observation-only access are separate evidence classes, never interchangeable.
`UNSUPPORTED` means a demonstrated incompatibility within the examined scope;
absence of evidence alone is `UNPROVEN`. An unapproved alternative is never PASS.

Public output contains contracts, digests, verdicts and limitations. Raw reports,
account identifiers, financial values, signatures and recordings remain in the
existing approved private evidence root. Retain raw bytes and revisions; do not
publish credentials or private source in the specification/decision record.

## 4. Settlement feasibility

### 4.1 Establish what chain actually exists

Read the accepted B7 identity, durable chain status and acceptance receipts under
authorized read-only access. Distinguish a production accepted chain from a
synthetic fixture or an unaccepted proposed bootstrap. Name the precise session
whose missing evidence blocks the next acceptance. Do not treat September 14 as
a permanent production anchor solely because it appears in a development test.
Conversely, do not reset an accepted chain to escape its missing predecessor.

Initial peak remains derived under B7 from its dashboard threshold and kernel
width. Subsequent peaks follow accepted settled closes. Statements, current
equity and a newly chosen date do not replace either authority.

### 4.2 Required facts and candidate producers

| ID | Required fact | Candidate source and pass condition |
|---|---|---|
| settlement-S1 | Correct account, inception and complete adjustment history | Account lifecycle evidence plus account-wide bounded cash queries from inception through capture; retain filters, successful query coverage, endpoint semantics, original rows and revisions. Identify initial funding and classify costs/adjustments under the existing contract. |
| settlement-S2 | Exact session and close boundary | Accepted calendar mapping plus report-specific timezone/date semantics. Resolve DST offsets and account-day versus business-date differences; preserve effective, published-if-supplied, captured, signed and received times separately. |
| settlement-S3 | Equity at that close | Venue-backed closing equity with valuation basis; alternatively source-backed balance and evidence of flatness at that same boundary. A later flat view, absent trade row or sum of observed fills fails. |
| settlement-S4 | Evidence-backed close acceptance | Source identifies the finished session; costs/adjustments reconcile; operator can attest no known pending correction/conflict from the presented evidence. No machine finality flag is newly required. Missing source facts or unresolved contradictions still fail. |
| settlement-S5 | Continuous state and repeatable operation | Exact predecessor, history comparisons, authenticated challenge/receipt, correction invalidation and restored listener binding pass through the accepted owner. Measure operator time and latest usable submission against the real schedule. |

Keep existing challenge/freshness bounds, full-history rereads, adjustment policy
and record-only catch-up semantics. Do not silently replace them with incremental
queries, an arbitrary waiting period, weekday carry-forward or a generic signed
checkbox. If an existing bound makes the route impractical, report its measured
effect and an exact proposed amendment rather than weakening the verifier.

### 4.3 Source routes, in order

**A — Existing historical evidence (preferred).** Locate an account-accessible
close/equity report or balance plus contemporaneous flatness evidence. Reuse
retained reports for provenance and comparison only. Before qualification or any
current or record-only submission, newly capture the required reports and query
the complete cash history from inception through capture, comparing prior history
for added, removed or revised transactions. Missing close facts require their own
source evidence. A historical report must identify the relevant close rather
than merely displaying the latest balance.

**B — Prospective attended capture.** If historical retrieval fails, determine
whether a supported account-bound capture protocol at a future close can meet
S1–S5. Record positions, orders, request uncertainty, balance/equity and source
close identity at the relevant boundary, then obtain the finished-close package.
Two observations bracketing the boundary cannot prove the intervening state
without supported coverage. This route can qualify future collection; it cannot
retroactively prove September 14 flatness or fix an existing chain gap.

If there is no accepted production chain, map prospective qualification to the
existing permitted initial-B7 procedure. If a predecessor is mandatory or an
accepted chain exists, a new origin requires a separate reviewed disposition
covering history, initial peak, seals, qualification and downstream invalidation.
Do not bootstrap a replacement database under the label of collection testing.

**C — Alternate source or contract disposition.** If neither route provides the
facts, stop settlement producer implementation. Present the specific missing
fact, available alternate source and entitlement, or the exact contract change
and affected qualification. No fresh account, spend, peak reset or economic
assumption is selected by this specification.

### 4.4 Qualification trace

Demonstrate an admissible anchor and a subsequent close through the real verifier
in an isolated, non-authorizing evidence rehearsal, then through the separately
authorized production acceptance procedure when due. Preserve original account
facts; rehearsal receipts cannot become live receipts or activate trading.
Reuse accepted traces; additional account activity is not required merely to
produce test data. Synthetic tests cover correction, missing session and restore
branches; they do not establish real report capability.

A no-activity session still needs evidence for S1–S4. A delayed report can delay
activation; it never authorizes stale-mode trading or replay of missed signals.
Historical catch-up accepts each supported predecessor in order while HALTED.

## 5. Ambiguous-order and normal-route feasibility

### 5.1 Inventory every actor before evaluating a fence

Enumerate runtime senders, manual platform access, working broker orders,
CrossTrade managers/managed triggers, copiers, queued/scheduled actions and any
other enabled account actor. For each, identify its control, request identity,
acknowledgment, delayed-effect behavior and retained history. Disable optional
actors only under a reviewed procedure that preserves required protection.
Exclusive local dispatch is useful but does not fence already accepted remote
work. Credential revocation, process termination and logout are not assumed to
cancel queued work or broker orders.

### 5.2 Required capability matrix

| ID | Required result | Acceptance boundary |
|---|---|---|
| recovery-R1 | Persist operation and attempt before transport; retain uncertainty after crash/lost response | Reuse PR 409 owner tests. Distinguish never attempted, possibly sent, acknowledged, working and terminal; never infer fill from HTTP success. |
| recovery-R2 | Map attempts to actual requests/orders/executions | Account/environment, symbol, side, quantity, action and protection relationships match; reject collisions and contradictory identity. Client tags alone are not proven broker deduplication. |
| recovery-R3 | Resolve a request with no returned broker ID | A supported request-status/correlation or remote fencing protocol identifies whether it can still take effect. An absent order in a snapshot or elapsed timeout is insufficient. This is a decisive feasibility test. |
| recovery-R4 | Complete and causally ordered reconciliation | Meet retained E1/E2: account scope, history coverage, revisions, gross lots, protection ownership/allocation and acquisition after the last relevant action. Local receive time and an exhausted cursor are not coverage watermarks. |
| recovery-R5 | Account-wide request closure | Meet retained E3/K1 across runtime, manual and provider-side work. Every earlier possibly effective request transfers to a known obligation or has terminal evidence; zero net exposure alone is insufficient. |
| normal-N1 | Execute the fixed book without semantic substitution | Qualify every used L2 entry, partial-fill, bracket/attach/amend/trail, cancel, scoped close, takeover and scheduled-close transition, including protection/FIFO ownership and no executable reverse orphan. |

R1 is a local engineering property. R2–R5 and N1 require the actual route.
Qualifying R1 does not imply any of the others. Report each independently.
Ordinary definitive rejection can release only its own reservation; an unknown
send retains its obligation. Retrying a read can be safe; retrying an uncertain
mutation is not authorized by read failure or HTTP timeout.

### 5.3 Candidate protocols

1. **Retained strict protocol:** qualify the existing route against E1/E2/E3/K1
   and L2 with actual supported producers. Prefer this if available: it preserves
   both the model and consumer contracts.
2. **Supported attended reconciliation protocol:** if the API alone is
   insufficient, examine whether platform request/order records and a supported
   intervention/quiescence procedure jointly prove the same facts. Each manual
   action is evidence-backed and linked to its outcome. If the composite cannot
   meet the current causal/history contract, label it `AMENDMENT_REQUIRED` and
   provide the exact replacement semantics and residual risk. Attendance is not
   an implicit waiver. No such weaker protocol is selected here.
3. **Alternate execution route:** if required facts or normal primitives are
   unavailable, compare a concrete entitled route against precisely those gaps.
   Require evidence that the alternative solves them before migration work.
   A shorter transport chain is not by itself evidence of better semantics.

Never introduce a timeout-based “assume failed” path or claim exactly-once broker
execution from a local journal. Polling and streaming can supply observations;
neither inherently establishes complete history or a remote request fence.

### 5.4 Decisive traces

| Trace | Required outcome |
|---|---|
| Response lost after request accepted, including no returned order ID | Same retained attempt; no resend; actual supported evidence eventually identifies its outcome or remains explicitly unresolved. |
| Two unknown attempts, one later resolved | Only that owner clears; account remains blocked for the other. |
| Partial fill races cancellation | Credit each execution once; retain remainder and protection obligations until their own terminal evidence. |
| Operator closes while an old request is unknown; delayed fill follows | Original request remains owned; observed flatness never clears it; late exposure remains an intervention obligation. |
| Provider manager acts after local halt | Inventory/control protocol accounts for the action; local fence is not presented as remote quiescence. |
| Restart or session rollover with missing/revised history | Original uncertainty survives; neither a fresh empty snapshot nor the date change allows activation. |
| Scoped close with residual protective orders | Confirm the accepted allocation/protection transition; no cancel-plus-market fallback that changes atomicity or strategy semantics. |

Use independent synthetic traces to check consumers without placing orders.
Real route characterization uses retained nonempty evidence where sufficient.
Where actual order actions are necessary, prepare a bounded operator-run test
with account/environment, action, expected evidence, intervention and teardown
specified before authorization. Do not deliberately lose live responses or create
unmanaged exposure merely to manufacture a failure test. A successful sample
cannot prove an undocumented universal guarantee; pair tests with supported
source semantics. Missing actual evidence remains UNPROVEN.

## 6. Smallest release selected by the evidence

| Settlement | Recovery R2–R5 | Normal N1 | Supported outcome |
|---|---|---|---|
| Qualified | Qualified | Qualified | Candidate for the minimal attended release below; all other existing qualification/live gates still apply. |
| Qualified only through proposed amendment | Any | Any | Review exact amendment and revalidate affected consumers first; no live readiness claim. |
| Qualified | Amendment required | Any | No live release; approve the exact recovery amendment and revalidate affected producers/consumers before reevaluating this table. |
| Qualified | Qualified | Amendment required | No fixed-book release; approve the exact normal-execution amendment and requalify affected execution/replay behavior before reevaluating this table. |
| Qualified | Unproven or unsupported | Any | Observation/offline engineering only; no live first session justified by promising never to resume. |
| Unproven or unsupported | Any | Any | No live release on the current settlement protocol. |
| Qualified | Qualified | Unproven or unsupported | No fixed-book release; resolve route or explicitly revise/requalify the affected execution contract. |

Read rows from top to bottom; the first matching row selects the disposition.
"Amendment required" includes `AMENDMENT_REQUIRED` for any member of the grouped
capability column. A recovery group with both unproven and amendment-required rows
therefore takes the amendment disposition, but all remaining gaps still block live
release. Approval alone does not change a row to qualified: collect the amended
contract's evidence, revalidate affected consumers and reevaluate every capability.

**Minimal attended profile:**

- One incumbent account, fixed four legs, existing signal daemon and listener;
  one durable account owner serializes all mutations and capacity decisions.
- One qualified production feed and execution route, with explicit supported
  symbol bindings and accepted calendar coverage. No active-active failover,
  automatic route switching or additional execution service.
- Preserve normal strategy operations, required protection, takeover and the
  approved scheduled cutoff/flatten sequence. These are not optional extras.
- Incident or unexpected process restart ends automated trading for that account
  session. Fence all subsequent runtime mutations, retain obligations, alert and
  require attended platform intervention. Existing remote orders may still act.
- No same-account-session reactivation following that incident, even if later
  reconciled. Persist the incident session across restart. A future session still
  requires complete reconciliation, accepted settlement, current source/identity
  checks and new bounded authorization; waiting for it supplies none of those facts.
- Reconciliation, disarm and urgent platform intervention remain available during
  the incident session. Do not defer risk management until the next session.
  Attendance continues under rev9 until reconciled/disarmed.
- A minimal authenticated incident view and acknowledgment control; show local
  fence status, observed exposure, outstanding requests, evidence age and exact
  blockers. Reuse existing signing/authority boundaries. No trading terminal or
  same-session resume button. Retain alternate-channel escalation and external
  missed-heartbeat monitoring; one local alert process cannot detect its own death.
- Initial activation retains B7/n3/GO/reseal and effective activation checks.
  Later-session activation is not a new B7 or automatic n3 rerun. Preserve expiry,
  correction and stop/adjudicate rules from their existing owners.

Normal refusals (capacity, recognized duplicate or valid stale individual signal)
remain request-level refusals, not new session-ending incidents. Normal scheduled
cutoff remains its existing bounded exit authority; an incident revokes it.
Account evidence failure, source failure and authorization faults retain their
existing incident definitions and thresholds.

This profile reduces recovery transitions, interface scope and deployment modes.
It does not remove the producer work needed for normal operation or safe incident
closure. It makes no availability or response-time guarantee beyond the qualified
services and existing attended contract.

### 6.1 Evening approval and automatic scheduled activation

**Requirement:** Joshua reviews the completed session and updates around 18:00
`America/New_York`, approves one identified upcoming trading session, and needs
no routine morning interaction. Joshua is reachable by phone and available for
incident platform intervention. At evening review, confirm platform/alert access
and availability for the authorized window. Retain acknowledgment/escalation
targets and prove actual phone delivery. Continuous screen presence is not required.

18:00 follows daylight saving time, not fixed UTC-05:00. Use the approved calendar
to show the target account-session ID, local/UTC boundaries, execution window and
expiry. Tradeify's ordinary account day starts at 18:00, so approval then can
cover the just-opened session containing the next morning. Do not add another
session at midnight or infer weekday/holiday mappings. Activation follows the
existing qualified strategy/calendar schedule; this adds no morning-only window.

**Recommended mechanism:** keep the existing services running. Complete updates
and intended disarmed deployment/restart before approval. The existing account
owner retains one-use conditional consent bound to the current boot and halt
generation, then evaluates it at the permitted start without another click.
Do not schedule a daily restart or keep a generally armed configuration. Unexpected
restart invalidates pending consent; surviving that restart is not selected for
the first release. First-ever launch retains its separate B7/n3/GO sequence.

The evening screen groups these steps but preserves their distinct authority:

1. Assemble the finished-close evidence and accept it using the existing signed
   settlement challenge/receipt. Retain source facts, freshness and attestation
   requirements. A report missing at 18:00 prevents completed evening approval;
   do not pre-sign unknown future facts or silently postpone signing to morning.
2. Validate any update and complete its applicable qualification/release admission.
   Show exact image/config, portfolio/policy, calendar, feed/route and predecessor
   settlement identities. Strategy changes do not inherit the old release GO.
3. Sign conditional authorization naming account/epoch, boot, generation, those
   identities, accepted settlement digest, target session, not-before time,
   activation deadline and expiry at or before the existing entry cutoff. Include
   nonce, signing identity and incident availability. Reject invalid/missing bounds.

Consent authorizes **later verification**, not reuse of evening observations as
fresh morning evidence. At activation, qualified read-only producers supply current
account scope, zero gross positions, no working/protective orphan orders, resolution
of previous requests and coverage of intervening activity/corrections. The listener
also checks settlement continuity, exact identities/GO, calendar, feed/warm-up/
barrier/control health, notification health and incident-session restrictions.
If any required fact needs manual morning collection, the no-morning requirement
is not qualified. Expected feed arrival is not an account change; unexplained
manual/provider activity or corrected history invalidates approval.

Only the serialized account owner consumes consent and records the fresh evidence
digest and durable effective-activation acknowledgment before risk admission. The
service records fulfillment of conditions; it cannot create an operator signature.
The UI/scheduler requests evaluation but cannot grant permission. Duplicate requests
return the retained outcome. Concurrent halt/revocation wins; uncertain activation
commit or restart remains HALTED rather than retrying into trading.

| Event | Required result |
|---|---|
| Evening approval; feed not expected open yet | HALTED/pending until the named eligibility boundary; off-session silence is not an invented fault. |
| Fresh checks pass inside the authorized start window | Consume once, record acknowledgment, start at the next complete eligible bar without replaying missed signals. |
| Missing/stale evidence or failed preflight by activation deadline | No trading; send exact blockers to the phone. Expiry does not permit a late start. |
| Unexpected restart, incident, revocation, changed bound identities/settlement, unexplained account activity | Invalidate pending consent, retain obligations, require new eligible approval. |
| Incident after activation | Fence runtime mutations, notify Joshua and end automated trading for that account session. |
| Repair, reconciliation and ordinary disarm finish | Prepare the next eligible session's approval; never resume the incident session or clear uncertainty on rollover. |

Diagnostics assemble one incident record automatically: outstanding requests,
observed exposure, evidence age, identity, fault and exact recovery blockers.
Bounded read-only retries may be automatic. Repair must not replay ambiguous
mutations, weaken evidence or silently change the approved image. Joshua performs
required platform actions. Once recovery is verified, present the next eligible
session's approval with the evidence already assembled; do not ask the operator
to gather logs or repeat completed diagnostics. Acknowledge remains separate from
approval. Single-screen recovery is not a promise of one-click platform repair.

**Timing gate:** measure source availability, collection, review/signing and receipt
around 18:00. Retain receipt-age bounds. If complete evidence is routinely unavailable
then, report the measured conflict and a concrete source/timing alternative. A
provider update window is not proof of readiness. No collection job or notification
service is configured by this document.

**Integration owed:** replace rev9 section 4's no-future-preapproval clause with
this narrow mechanism and its same-session resume permission with #411's restriction.
Reconcile sections 3/7, rail-extension S8/S9 and R-N/R-M, the arming procedure's
subsequent-session dependency, replay incident tests and Phase 5/6 plans together.
Keep planned disarmed initial boot distinct from unexpected restart through verified
state, not a caller's `planned` label. Later-session GO validity/current-state rules
remain an explicit owner dependency. No new B7 or n3 is implied by routine approval.
This extension does not silently supersede the governing contracts.

**Acceptance traces:** evening approval to healthy morning without interaction;
approval at/after 18:00; weekend/holiday/DST; late report; correction/manual order
after approval; stale/replayed consent; halt race; lost activation reply; restart
before/after consumption; phone failure/escalation; incident repair with same-session
refusal; later-session approval only after reconciliation/disarm; initial-launch
separation. Exercise actual listener/config/evidence boundaries and an attended
phone drill. Synthetic success proves only consumer behavior, not real capabilities.

## 7. Contract delta and integration boundary

| Owner/component | Proposed treatment |
|---|---|
| PR 409 account owner, runtime and settlement integration | Reuse merged `845fb13` and retained acceptance. Later-session authorization is follow-up work; synthetic bootstrap is not a production activation API. |
| Settlement contract, `account_close_evidence.py`, `account_close_calculation.py`, `book_settlement.py` | Preserve interface and acceptance law. Add only qualified source adapters/procedures in later implementation. Any new anchor/evidence law is a separate exact amendment. |
| Rail extension E1/E2/E3/K1 and L2 | Retain. Capability gaps are decision outputs; do not disguise them as serializer fields or provider guarantees. |
| Halt/resume rev9 sections 3, 4 and 7 | Approved base restriction: incident-session reactivation refused. Section 6.1 proposes narrow evening consent and later automatic verification; reconcile the no-future-preapproval clause and attendance wording before implementation. |
| Runtime owner and activation/config owner | Later implementation persists incident-session restriction through restore and verifies actual activation. No new permission owner. |
| Replay/qualification | Preserve portfolio and normal schedule. Document impact of changed incident-resume availability; retain existing separation of outage integration scenarios from economic sampling. Do not invent outage frequencies or rerun outcome-bearing samples without their authority. |
| Release checklist/operating procedure | Reference the accepted capability record and changed session behavior; reuse unaffected evidence and approvals. |

The feasibility slice completes before provider-specific production adapters or
resume UI work. Source-independent qualification work remains governed by its
own approvals; this draft neither pauses it nor authorizes a paused run.

## 8. Bounded execution and completion

1. Pin the final accepted integration revision and governing contracts; inventory
   the actual accepted chain and existing private evidence. Reuse valid work.
2. Perform one documented source/entitlement pass for S1–S5, R2–R5 and N1. For
   each unresolved row, specify one bounded collection/test that can change its
   verdict. Repeated identical flat-account polls are not a test plan.
3. Prepare the settlement collection procedure and broker trace procedures.
   Record real account/environment, inputs, capture boundaries, expected outputs,
   freshness/retention, operator actions and stop/teardown conditions before use.
4. Execute available authorized read-only collection and isolated verifier
   rehearsals under the subsequent execution instruction. Present any needed
   operator-only action as a concrete procedure. No support contact is assumed.
5. Stop a row when the examined route lacks a necessary guarantee. Retry only on
   a named new source, changed access or relevant new observation. Return a
   capability/contract choice instead of building around an imaginary producer.
6. Publish one decision record and select the supported profile using section 6.
   If any required capability is missing, the completed design slice may conclude
   BLOCKED FOR LIVE RELEASE. That is a valid result, not a passed capability.

Exit evidence: every required row has a producer or a precise unresolved gap;
settlement has a chain-specific disposition; request ambiguity without a returned
ID has an explicit disposition; normal primitives have their own verdict; actual,
synthetic and documentary evidence are distinguished; operational effort/timing
has been measured where demonstrated and marked unknown otherwise. Record code,
route and evidence identities plus conditions requiring requalification.

Before accepting a live candidate, verify the combined trace: qualified anchor
and close -> shared sizing -> admitted action -> durable attempt -> real outcome
-> scheduled closure or attended incident -> qualified reconciliation -> ordinary
disarm. An incident never returns to running in the same account session under
the proposed profile. Restart, correction, lost receipt and stale authorization
must retain those outcomes through the real consumer boundaries.

Do not claim the feasibility tests have run from this specification. Drafting
used code/contract reads, existing probe records and current public documentation;
no new private account acquisition, service configuration or order action occurred.
The recorded design approval permits a subsequent bounded execution plan; it does
not select a weaker evidence standard or authorize production activation.
