# Tradeify production feasibility and evening-approval decision record

Date: 2026-09-16. Integration owner: coordinating agent. Verdict:
**BLOCKED FOR LIVE RELEASE; bounded source/code investigation completed,
account-source qualification remains open.** No account fact is accepted merely
because the operator approved the design. No trades, host changes, source
submissions, new seals, support messages, or activation occurred in this pass.

Scope: execute the available read-only portion of
[PR #411](https://github.com/Joshua-Asante/first-passage/pull/411), and add the
requested evening workflow to its [operating design, section 6.1](../superpowers/specs/2026-09-16-tradeify-settlement-order-feasibility-design.md#61-evening-approval-and-automatic-scheduled-activation).
This record identifies disposition and the exact next evidence per gap; it does
not represent unresolved capabilities as closed or implementation-ready.

## 1. Baseline and evidence classes

### Operator checkpoint: working assumptions and outstanding decisions

Joshua requested that this state be recorded after reviewing Tradovate's AI reply
and the working-assumption summary. This checkpoint preserves planning context;
it does not qualify a capability, ratify detailed activation mechanics, amend a
governing contract or authorize live operation.

| Working assumption | Boundary |
|---|---|
| Review updates and approve around 18:00 America/New_York; no routine morning interaction | Later activation requires fresh automatic checks; evening evidence is not reused as fresh morning evidence. |
| Joshua is reachable by phone and available for incidents | Actual delivery, acknowledgment and escalation still require a phone drill. |
| An incident ends automated trading for that account session | Repair prepares a later eligible session; rollover never clears outstanding requests or reconciliation obligations. |
| Reuse #409's durable owner and offline integration | Offline acceptance does not qualify broker behavior or production evidence. |
| Observed account reports are candidate evidence sources | Completeness, timezone/filter semantics, correction handling and historical close valuation remain unqualified. |
| Unknown or unsupported conditions prevent activation | Never automatically retry a mutation whose original outcome remains unknown. |

Do not infer request closure from flat positions, atomic scoped protection from
ordinary OCO support, or required delayed trailing behavior from generic trailing
support. These remain distinct requirements.

Conditional decisions:

- **Settlement origin:** no accepted production chain was verified in the inspected
  locations. Whether one exists elsewhere remains unanswered. If none exists,
  qualify a prospective initial launch using the existing B7 procedure; September
  14's rehearsal close is not automatically mandatory. If one exists, preserve its
  predecessor and resolve its specific gap. No reset or origin selection occurred.
- **Execution route:** CrossTrade/Tradovate remains the incumbent candidate. No
  migration, direct-API entitlement or overall route suitability is established.
  The specifically incompatible mappings already documented remain unsupported.
- **Work boundary:** evening-workflow design, diagnostics design and offline
  verification may progress under their applicable approvals. Production adapters
  and live approval depend on supported provider semantics and actual qualification.
  Recording this checkpoint is not blanket implementation approval.

Provider state at checkpoint:

- CrossTrade inquiry submitted; receipt confirmed; substantive reply not yet read.
- Tradeify inquiry submitted; human escalation confirmed after an inadequate AI
  answer; human response not yet read.
- Tradovate case submitted by Joshua; success page verified. Its September 16
  19:38 Eastern AI email explicitly could not confirm the missing capabilities.
  No capability verdict changed. Human escalation by replying "Agent" was offered
  by the email but has not been sent in this task.

Resume from the [inquiry and response log](2026-09-16-production-capability-inquiries.md):
review substantive provider replies against the existing acceptance criteria,
resolve production-chain existence, and select supported source/route procedures
before implementation that depends on them. No new outreach, monitoring job,
runtime change or deployment is initiated by this checkpoint. Live release remains
blocked. This checkpoint was originally local on `codex/tradeify-evening-feasibility`.
Joshua subsequently requested publication to PR #411 and resolution of its review
findings; integration uses `codex/tradeify-feasibility-design` at fetched head
`083766668e56d7362c36ce66f1e32847f3efcebf`, preserving its intervening base updates.

### Pinned investigation baseline

- Integration: merged PR #409, `845fb13ed2141482649627f5b78a51f4cadbd61d`;
  final branch head `3cf42e43f4f41f0b1e66d7510d2c55cda57c21b9`.
- Approved feasibility design: PR #411 head
  `d7709adb7d3816b3beaf44506d56138f3ae6f067`; open when inspected.
- Working branch: `codex/tradeify-evening-feasibility`, based on the #409 merge.
  Other worktrees and primary-checkout untracked documents were preserved.
- Direct source reads: `book_account_owner.py`, `book_bootstrap.py`,
  `book_settlement.py`, `book_sizing_context.py`, `book_policy.py`,
  `crosstrade_payload.py`; accepted settlement, halt/resume rev9, rail extension
  and arming procedure. The source reads precede this decision record.
- Historical evidence: September 14 broker probe and September 15 account
  producer/collection records. Those are dated observations, not fresh account
  attestations. Their reported limitations remain explicit below.
- New actual evidence: host status/data-filename inventory, one disarmed-host
  CrossTrade GET cash-balance probe, and signed-in Tradeify, Tradovate and
  CrossTrade inspection after operator login. Historical Orders and Position
  History CSV originals were downloaded and retained privately; findings below.
- Documentary evidence: current official pages linked below. Published capabilities
  are not demonstrated entitlements or account-specific qualification.

## 2. Chain-specific settlement disposition

The retained private collection is under the primary checkout's ignored root:
`lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/inputs/private_overrides/op1/2026-09-14-seven/producer-qualification-2026-09-15/`.
It contains an issuance email, dashboard and current account captures, six bounded
cash-query exports/observations and balance history. Reuse these originals for
provenance and comparison; do not discard them. Every current or record-only
acceptance still needs newly captured required reports and a fresh complete
inception-to-capture cash-history query, including revision comparisons.

The existing `qualification-output/qualification-report.json` explicitly labels
its attestations as placeholders, its predecessor as manually seated rather than
from B7, capture times as local download-file times, a simulated qualification
clock, and a placeholder policy digest. Read-only SQLite inspection returned
`quick_check=ok`, two chain rows, two receipts and origins labelled `B7` and
`ACCOUNT_CLOSE`. Those labels do not override the report's rehearsal provenance.
There is no `b7_history` table in that inspected rehearsal database. It is not
an accepted production chain and must not be promoted, migrated or copied to live.

The running legacy `c1-rail` host's top-level `/data` inventory contained legacy
JSON/JSONL/configuration files, not an identified four-leg settlement database.
This bounded inventory plus the rehearsal inspection establishes **no verified
production chain in the inspected locations**. It does not prove that no accepted
chain exists elsewhere. Obtain the authoritative deployment-state inventory before
selecting an origin. No chain was booted, reset, accepted or invalidated here.

Consequences:

- September 14, 2026 21:00 UTC remains unsupported as a historical close in the
  examined account evidence. Current flatness cannot fill that missing fact.
- It is not automatically a mandatory production predecessor merely because the
  rehearsal used it. If the authoritative inventory confirms no accepted chain,
  qualify prospective sources and use the existing initial-B7 procedure when the
  release is ready. This is not a new-origin shortcut or authority to collect an
  expiring launch seal now.
- If an accepted chain is located and requires that predecessor, preserve it and
  obtain the missing historical evidence or an explicitly reviewed disposition.
  A later date, new database or operator signature cannot skip the gap.

## 3. Capability matrix

`UNPROVEN` denotes missing required evidence. `UNSUPPORTED` below applies only
to the specifically named documented mapping, not every possible vendor route.
`AMENDMENT_REQUIRED` denotes a proposed semantic change, never a PASS.

| ID | Producer/evidence examined | Verdict and exact next disposition |
|---|---|---|
| settlement-S1 | Retained issuance notice, six bounded cash windows and account captures | UNPROVEN as a complete qualified producer. Original collection exists; establish report filter date basis, endpoint inclusion and timestamp semantics, then re-query fresh full history when acceptance is scheduled. Do not substitute purchase charge for nominal funding. |
| settlement-S2 | Accepted account calendar; operator/UI timezone labels; [Tradeify account day](https://help.tradeify.co/en/articles/10468225-what-is-a-trading-day) | UNPROVEN for report-to-session mapping. The venue day is 18:00–17:00 Eastern; that does not certify the CSV timezone or query predicate. Establish report-specific mapping, including the exact September 14 boundary if that close is consumed. |
| settlement-S3 | Balance-history CSV; historical dashboard inspection; new cash-balance endpoint | UNPROVEN historical close equity/flatness. Locate an account-entitled close valuation, or balance plus evidence of boundary flatness. Current cash snapshot and later empty positions fail this requirement. |
| settlement-S4 | Operator-attested close contract and retained reports | UNPROVEN. Source must identify the finished close and support costs/adjustments and no known pending conflict. A machine finality flag is not newly required; a signature cannot create missing close identity. |
| settlement-S5 | #409 durable owner plus old placeholder rehearsal | Local engineering exists; real producer acceptance UNPROVEN. Demonstrate authentic anchor/next close in an isolated non-authorizing rehearsal and measure source availability through accepted receipt near 18:00. Production acceptance remains separately gated. |
| recovery-R1 | Merged durable account owner, attempt/operation and restart interfaces | Reuse #409's bounded offline acceptance; not independently rerun here. This does not establish remote delivery, execution or production adapter capability. |
| recovery-R2 | Historical fill identities; current documented client labels/lifecycle | UNPROVEN end-to-end correlation. Trace one existing actual request through broker ID, commands, executions and protection ownership. Label reuse must not be treated as deduplication. |
| recovery-R3 | Published ordinary-placement correlation protocol and order reads | Positive-match route identified; negative-result closure UNPROVEN. Locate a supported disposition for a request with no returned ID and no matching order, covering delayed acceptance. Do not retry an ambiguous mutation based only on absence. |
| recovery-R4 | Snapshot/lifecycle reads and durable fill history | UNPROVEN coherent, complete account history. Require entitled source coverage/ordering and revisions across every relevant action; exhausted stored pagination is insufficient. |
| recovery-R5 | Runtime journal plus manual/provider actors | UNPROVEN all-account request closure. Inspect actual enabled managers, copiers, triggers, queues and manual access; name each control and terminal/quiescence producer. A local halt does not stop those actors. |
| normal-N1 | Rail L2/S3/S5 requirements against documented routing below | UNPROVEN as a complete route; two convenient mappings are UNSUPPORTED against the retained semantics. Resolve those mappings before any real mutation tests or production adapter implementation. |

### Signed-in account inspection

The operator supplied login access on September 16. The incumbent account was
visible in Tradeify and Tradovate DEMO; CrossTrade showed Tradovate connected and
NinjaTrader disconnected. No orders or provider configurations were changed.

- Tradeify account details exposed current balances, last-traded date September
  10 and an approximate EOD graph, with guidance to use the broker for accurate
  liquidation information. This view supplied no exact historical close valuation.
- Tradovate's report selector offered Performance, Orders, Position History,
  Cash History, Order Details, Fills and Account Balance History. No separately
  named close-equity or client-statement report appeared in that selector. This
  is a bounded menu observation, not proof that support cannot supply one.
- For the displayed September 10 through September 15 date range, with blank
  time fields and no additional filters, Orders returned two filled market orders
  and Position History returned one completed position with net quantity zero.
  Both CSVs name the same account. Buy/sell times agree across the files, and the
  position record contains both fill IDs. This verifies access to existing real
  trade records, not complete account coverage or flatness at September 14 close.
- Order Details queried using the actual exit order ID returned column headings
  but no detail rows. No error cause or retention guarantee was established.
  Therefore request labels, accepted amendments and protective relationships
  remain unqualified; the empty result is not proof that no command existed.
- The report times are unzoned. The workspace clock displayed CDT while the
  retained earlier CrossTrade probe reports UTC fill extrema that suggest a
  possible different report offset. No ID-matched cross-source timezone proof
  was completed. Neither CDT nor Eastern is accepted as the report timezone.
- CrossTrade Account Manager showed no monitors; Trade Copier showed zero active
  and total copiers, leaders and followers. Management Log had no rows. Alert
  History also had no rows; its filter panel showed All for status/show,
  destination, command, origin and sender, with blank account/instrument fields.
  Its auto-hide control exists but its exclusions were not independently qualified.
  These observations narrow the enabled-actor inventory. They do not certify
  absence of delayed requests, broker-side protection, retained triggers or all
  manual actors, and do not discharge R3/R5.

Original CSVs are under the ignored `production-feasibility-2026-09-16/` directory
beside the earlier private collection. SHA-256 values:

| Original | Rows | SHA-256 |
|---|---:|---|
| `Orders.csv` | 2 | `be279eda258534fdbeaf5012c93784f1a069c37280272c110cb32e4a9d2078a9` |
| `Position History.csv` | 1 | `cabddc04e1c72a315472115b2835b0697f3cc80c5e057aa727cdc7246c60d6c3` |

Browser observations are investigator notes, not retained signed source exports.
CSV file/download times must not be substituted for source capture/finality times.
This closes the login/access dependency and confirms these two report exports;
it does not close settlement-S1 through S5 or recovery-R2 through R5.

### Current cash-balance probe

At `2026-09-16T22:33:47.688887+00:00`, the existing host configuration passed
`dry_run=true`, empty `armed_until`, `destination=tradovate` assertions. The probe
used its in-place credential for one `GET /v1/api/tv/cashbalances`, refusing
redirects and limiting response size to 2 MB with a 20-second timeout.

Result: HTTP 200, one linked-identity envelope and one row. Row fields included
`accountId`, `amount`, `amountSOD`, `archived`, `currencyId`, `id`, `realizedPnL`,
`timestamp`, `tradeDate`, `weekRealizedPnL`. No values or credentials were printed.
Response SHA-256:
`18db5b5ee96e0eb36a1300d5bc651e45351fbfb7e3e553bb65f28c15e22e3f64`.
Only schema metadata/digest was retained, not original private response bytes;
this is diagnostic capability evidence, not an admissible settlement package.
The probe did not independently bind that row's numeric account ID to the configured
account name. Do not infer the binding from the single-row result.

The [cash-balance documentation](https://crosstrade.io/docs/api/tradovate/get-cash-balances)
describes current raw balance rows. The observed timestamp/trade-date fields do
not establish historical equity at a requested close. Stop this route as a proposed
replacement for S3; another current-balance poll cannot resolve the missing fact.

Fly reported `Error: The handle is invalid.` and wrapper exit 1 after the remote
completion marker. Remote JSON reported `remote_complete=true`; report both
facts. `fly status` itself exited 0 and reported the existing machine started with
one passing check. Host liveness is not four-leg readiness or a broker-state check.

### Ambiguous requests: useful protocol, remaining hard edge

The [Tradovate API overview](https://crosstrade.io/docs/api/tradovate/overview)
documents ordinary-placement correlation via working/session orders and the
lifecycle command's client label. It explicitly distinguishes labels from
idempotency and excludes inline ATM placement from that label protocol.

Use that procedure to find a **positive** matching order and retain its actual
terminal/fill evidence. The published recommendation to place again when no order
matches does not establish the retained contract's causal fence against a delayed
request. Thus this is a candidate R2 producer, not acceptance of R3/R5. Do not
import a vendor retry recommendation as a waiver of the approved contract.

[Order status](https://crosstrade.io/docs/api/orders/get-order-status) takes a broker
order ID; its slim status does not establish accepted modification parameters.
[Lifecycle](https://crosstrade.io/docs/api/orders/get-order-lifecycle) is a candidate
positive-order audit producer, but partial/unavailable components and bounded
command/report acquisition must be checked. Prior historical-item/lifecycle GETs
returned errors; their cause was not established. Login/report access or a new
supported source must change before repeating identical failed samples.

[Fill history](https://crosstrade.io/docs/api/tradovate/get-fill-history) retains
captured fills but does not certify capture completeness, promise capture
deadlines, or backfill earlier sessions. It is useful for observed-fill identity
and overlapping revision checks. It cannot alone discharge complete history.

### Normal execution: reject these unqualified substitutions

1. **Partial close -> ordinary Tradovate CLOSEPOSITION is UNSUPPORTED for the
   required automatic scoped-protection reduction.** The [command reference](https://crosstrade.io/docs/webhooks/commands/close-position)
   says a partial close is an opposing market order and leaves working orders in
   place. Rail S5/L2(d)/(e) requires residual protection at the intended quantity
   after each partial fill and no reverse orphan. A later cancel/replace is not
   the specified atomic behavior. An alternative broker-native scoped primitive
   needs its own evidence; a full-symbol liquidation is not a scoped-close substitute.
2. **Triggered trail -> CrossTrade-managed trigger is UNSUPPORTED as a claim of
   fully native L2(g) behavior.** The [execution reference](https://crosstrade.io/docs/webhooks/tradovate-advanced)
   distinguishes native continuous trailing from managed trigger activation and
   describes provider-side protection management. Rail S3(e)/AC-3 requires the
   accepted activation, anchor and sibling semantics, including native realization.
   Merely renaming a managed field cannot establish that. Qualify a matching native
   route or present an explicit execution/replay amendment before changing it.

No unsupported claim is made about every Tradovate/NT8 capability. An NT8 lifecycle
can resolve an original ID in its documented surface, but this does not prove
that an absent ID can never arrive later, nor this account's entitlement, history,
protection semantics or suitability. Direct/partner Tradovate documentation likewise
does not establish access for this account. No alternate route, subscription,
weaker contract or different portfolio is selected by this record.

## 4. Bounded collection procedures and stop conditions

### A. Source and entitlement pass after login (read-only)

Account/environment: the incumbent Tradeify account already identified in retained
private artifacts, Tradovate DEMO. Verify identity against those originals before
capturing; do not select another account merely because it has richer reports.

1. Inspect the available Reports menu and relevant report help. Locate account
   close/equity, cash, orders/order details and activity records; distinguish retail
   availability from [partner report documentation](https://partner.tradovate.com/resources/admin-dashboards/reports).
2. For the historical blocker, request the exact September 14, 2026 21:00 UTC
   close valuation or a source-bound balance and boundary-flatness record. Retain
   timezone, effective date, account scope, query bounds/result status and originals.
   A later balance or blank daily P&L tile is not success. Do not broaden to repeated
   identical current screenshots when the view cannot expose historical facts.
3. Inspect one retained nonempty cash transaction with source query help or a
   bounded boundary query to distinguish timestamp-date versus business-date
   filtering. Preserve the original timestamp zone and both endpoint semantics.
   An interior transaction alone cannot prove inclusivity or DST behavior.
4. Inspect available order-detail/activity records for an already existing order
   and its client label, fills, cancels and protective relationships. Use no
   fabricated IDs, new trades, deliberately dropped responses or duplicate sends.
5. In CrossTrade, inspect enabled account managers/copiers/managed triggers and
   Alert History. Capture identities and states privately without changing them.
   Provider success/pending/failed labels are not automatically terminal broker facts.

Save new originals under the same ignored parent in
`production-feasibility-2026-09-16/`, with UTC capture time, query context and hashes.
Secrets remain in their existing secure locations. If a required report is absent,
record that account-specific absence once and stop the row. Operator login is now
complete; the bounded pass above found records but no qualifying historical close
or complete order audit. No support contact or purchase is authorized.

### B. Prospective close, if historical retrieval cannot work

First resolve whether an accepted production chain exists. With none, rehearse
future collection against a non-authorizing fixture and defer real B7 until launch;
with an existing chain, preserve it and obtain the exact disposition for its gap.
At a named covered close, collect source-backed effective equity or a complete
balance/flatness interval, finished-session identity, original reports and costs/
correction evidence. Capture the dashboard after its relevant update and re-query
bounded full history. No manufactured activity is required.

Measure when all required facts become available and whether the full package can
be reviewed/submitted around 18:00 under the existing 30-minute receipt-age and
five-minute challenge bounds. This is a measurement, not a new deadline or finality
rule. The partner page's EOD guidance is not proof of this account's report timing.
Bracketing flat snapshots alone fail the interval requirement. Scheduling a future
collector and choosing a new production origin are separate actions, not performed.

### C. Real order tests are gated on semantic feasibility

Do not place orders to test a mapping already shown to violate the contract.
For a supported candidate, first prepare a separate operator-run packet naming
the actual authorized account/environment, exact symbol and bounded quantity,
permitted window, action, existing protection, required records and teardown.
Until those source/account facts exist, that packet is not ready for authorization.
The agent performs no broker mutations. Use retained real traces wherever sufficient.
Synthetic lost-response/race cases check consumers; they do not prove remote guarantees.

The required real trace set remains entry/partial fill, terminal cancellation,
protected scoped close, attach/amend, trail/anchor, takeover, scheduled closure,
provider effects and reconciliation. Any mismatch/unknown result stops the test,
retains the original obligation and transfers exposure management to Joshua. Finish
only with qualified reconciliation and confirmed ordinary disarm.

## 5. Evening operating-design result and release disposition

The design now requires evening settlement/review followed by one conditional
session approval, fresh automatic activation checks, no routine morning click,
phone incident delivery, automatic diagnostics and next-eligible-session approval
after verified recovery. An incident still ends automated trading for its account
session. Unexpected restart invalidates consent. Routine updates happen disarmed
before approval; changed strategy semantics require affected qualification.

Two direct conflicts are identified for a coordinated contract amendment:
rev9 forbids future-session preapproval and permits same-session incident resume.
The proposed extension addresses the former; #411's approved base restriction
addresses the latter. The detailed extension is reviewable, not implemented or
silently promoted to a new governing rev10. Initial B7/n3/GO remains separate.

**Selected disposition:** retain the incident-attended, evening-approved target,
but keep live release blocked. Signed-in source/order inspection is complete for
the bounded views above. Next resolve the explicit R3/R5 and normal-primitive gaps through supported
evidence, a concrete route alternative, or a separately reviewed contract amendment.
Do not build provider-specific recovery/activation adapters around missing facts.
Neither #409's merge nor no-same-session-resume removes these prerequisites.

## 6. Verification and limits

Follow-up: [provider inquiries and resolution criteria](2026-09-16-production-capability-inquiries.md)
now supplies exact questions, acceptance evidence and stop conditions for the three
remaining capability groups. Joshua authorized sending; the companion submission
log records all three provider submissions, including independently observed
Tradovate success after Joshua submitted its form. Substantive confirmation
remains pending. The Tradeify AI response is not accepted as a
qualified source; human confirmation was requested.
Tradovate's September 16 19:38 Eastern AI email was subsequently read: it
explicitly cannot confirm exact historical close evidence, source semantics or
the two required protection primitives. No matrix verdict changes; the inquiry
record retains the response disposition. Human platform/API confirmation remains
outstanding.
Current official
API documentation exposes potential order-strategy surfaces but does not establish
the required scoped-close/trailing guarantees or this account's direct entitlement.
The operator has been asked whether any production settlement chain exists outside
the inspected rehearsal/deployment locations; until answered, origin selection
remains unresolved.

- Primary checkout `.\fp.ps1 doctor`: exit 0; operations interpreter
  `tmp/ops-env/Scripts/python.exe`, Python 3.13.2; 62 locked packages matched,
  optional signing dependency available. The #409 worktree predates the launcher;
  the read-only SQLite audit ran through the primary launcher with no project
  imports or database writes. It inspected existing bytes, not a replay acceptance run.
- SQLite audit via `.\fp.ps1 python -c <read-only audit>`: exit 0, results above.
- Remote probe: actual HTTP 200 and completion JSON; Fly wrapper exit 1 disclosed.
  No raw account response retained and no fresh production account attestation.
- Documentation checks through the primary launcher's scripts:
  `check_governance_prose_control_chars.py <two edited documents>` passed;
  `check_md_relative_links.py --repo-root .worktrees/tradeify-evening-feasibility
  --glob docs/notes/2026-09-16-tradeify-production-feasibility-decision.md
  --glob docs/superpowers/specs/2026-09-16-tradeify-settlement-order-feasibility-design.md
  --strict` passed: two documents, two relative targets, zero unresolved.
- No runtime source was changed, no new runtime test result claimed, and no
  all-capabilities-PASS asserted. The initial investigation was local; the later
  operator instruction authorizes committing and pushing these records to PR #411.
  Exact new activation mechanics remain a review draft.

### PR #411 review disposition

| Finding / related case | Repair and verification |
|---|---|
| Amendment-required recovery or normal execution had no release-table outcome | Added explicit blocking dispositions and ordered evaluation. Qualified settlement with recovery amendment, normal amendment, both amendments, or mixed unproven/amended recovery cannot select the live candidate. All-qualified remains the sole candidate row; settlement gaps still block. |
| Historical Route A could reuse stale ledger evidence | Reuse is now provenance/comparison only. Current and record-only submissions explicitly require fresh reports and full inception-to-capture history. Matched the settlement contract's freshness and catch-up rules; aligned this record's reuse instruction. Prospective collection already requires full-history rereads. |

These are specification repairs, not new production guarantees. Provider responses
and evidence qualification remain open independently of review completion.
