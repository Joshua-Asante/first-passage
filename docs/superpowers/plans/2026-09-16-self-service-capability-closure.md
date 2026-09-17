# Self-Service Capability Closure Implementation Plan

> **Design amendment, 2026-09-17 UTC:** The [bounded platform-protection incident contract](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md) directs the next design assessment. Reassess ordinary ATM before custom protection infrastructure; retain uncertain-request blocks and no same-session strategy reactivation. Existing capability evidence remains valid within its scope, but this plan's incident assumptions need reconciliation before implementation. The amendment does not qualify any route.

> **For agentic workers:** Execute with superpowers:executing-plans; use superpowers:subagent-driven-development when bounded delegation is useful and authorized. Preserve the behavioral contract and integration owner. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Resolve the incumbent account's settlement, request-recovery and normal-execution gaps using existing access, retained records and bounded consumer rehearsals, without making support replies the critical path.

**Architecture:** Establish the actual chain and actors, test the decisive no-ID request-resolution source, collect settlement evidence, characterize normal primitives, then specify the missing production integration. Extend CAP-20260916 as the sole capability decision record. Sources provide facts; the existing account owner retains permission and obligations.

**Tech Stack:** Existing account/report UIs and documented read interfaces, immutable private captures, pinned Git artifacts, existing settlement/account-owner consumers and the post-413 operations launcher. No new production service or alternate evidence database.

**Spec:** [PR 411 assessment plan](2026-09-16-pr411-capability-assessment-handoff.md), [capability decision CAP-20260916](../../briefs/phase4-preparation/2026-09-16/capability-decision.md), [feasibility design](../specs/2026-09-16-tradeify-settlement-order-feasibility-design.md); scope: capability assessment and the conditional integration handoff.

## Global constraints

- Status: **EXECUTED bounded assessment, September 17, 2026 UTC.** The operator subsequently authorized implementation of this sequence, commit and PR publication. See the execution ledger below; unfinished source qualification remains explicit. New order tests, production implementation and activation remain separate scopes.
- Use the final accepted PR 411 successor for qualification and dependent rehearsals. Execution baseline: PR 411 MERGED at `7c317703869d252e35560e994d9bd11576152827`; accepted design unchanged from inspected head `72050e4a7d5248fb895bd736e4f446283e6d94b6`.
- Runtime reference inspected for this specification: `b4aa8efb0ee8f6d40b5aa332d5bb850bfa8b68ac`, containing merged PR 409 and PR 413. Select a clean accepted successor at execution. Do not run against the older primary checkout or another task's dirty tree.
- Preserve the fixed book, policy, account-anchor derivation, calendar, normal protection/close semantics and evidence laws. No timeout-based failure inference, new peak, missing-session bypass or synthetic source guarantee.
- No spending, account migration, subscription, credential staging, new support contact, order mutation, emitted signal, deployment or arming. Do not disable actors as an inspection shortcut.
- Raw account identities, financial values, signatures, reports and recordings remain in established ignored primary-checkout roots. Confirm ignore status before writing; retain original bytes and revisions without overwriting. Worktrees contain only public-safe code/docs and synthetic fixtures.
- Inspect a live owner only through an existing qualified read-only interface or a consistent isolated copy. Never call `boot`, migration, bootstrap, restore/reconciliation or observation methods against production merely to inspect it.
- Actual order tests require a concrete separately approved operator procedure. Do not manufacture live lost responses, delayed fills or unmanaged exposure.
- A support reply is optional source evidence to evaluate if it arrives. It is neither a prerequisite for the initial pass nor sufficient by itself to qualify the account/route.

## Ownership, output and acceptance vocabulary

The coordinating agent owns integration and updates only
`docs/briefs/phase4-preparation/2026-09-16/capability-decision.md` for outcomes.
The existing private CAP-20260916 index receives append-only capture batches and
references. Do not create competing S/R/N matrices in new decision records.
Joshua supplies account-only facts, authentication and separately approved actions.
The accepted settlement verifier/account owner owns acceptance, persistence and
permission; a capture tool cannot assume any of those roles.

For every finding record: S/R/N row; source and entitlement; private account/
environment/route binding; query/filter bounds and timezone; effective,
published-if-supplied and captured times; coverage, ordering, corrections and
retention; original-byte digest; code/config identity; consumer result; verdict;
exactly one next disposition and owner. Signed/received times are separate when
submission is applicable. Unavailable fields are explicitly unknown.

Retain the four verdicts: QUALIFIED, UNPROVEN, UNSUPPORTED and AMENDMENT_REQUIRED.
**Source feasibility is a work checkpoint, not a fifth verdict.** A source may
have documented semantics and adequate original observations while its row stays
UNPROVEN pending consumer acceptance. This permits a bounded adapter proposal
without either assuming its inputs or requiring an already-built adapter first.

## Dependency order

| Step | Required input | Concrete output | What can continue if blocked |
|---|---|---|---|
| 0. Revision/authority | Existing record and current PR metadata | Accepted design/runtime pins or precise unresolved gate | Public documentation and preparation; no dependent qualification/rehearsal |
| 1. Chain and actors | Existing deployment/artifact locations and authorized read access | Bound chain disposition and actor/request inventory, with explicit unknowns | Source discovery and local test preparation |
| 2. No-ID resolution | Route/environment identity and actor scope | Supported request-resolution protocol or exact missing guarantee | Settlement collection and source-independent engineering |
| 3. Settlement | Exact chain predecessor, or evidenced no-chain finding | Historical package or admissible prospective collection procedure | Unrelated documentary primitive checks |
| 4. Normal primitives | Actual port requirements and supported route records | L2/normal-operation source and trace packet | Local consumer testing; no route-specific build around missing semantics |
| 5. Consumers/integration handoff | Accepted baseline, usable evidence and identified interfaces | Revision-bound test results and bounded production integration specification | Return precise blockers; no production release |

Steps 2 and 3 may share captures. Investigate R3 first because a missing request
guarantee can defeat the route regardless of successful settlement. A failed R3
inquiry does not cancel useful settlement work. Source-independent Phase 3 work
retains its separate authority.

## Step 0 — Establish the execution baseline

**Files:** existing assessment plan, CAP-20260916, accepted governing contracts.

- [x] Read current PR 411/409/413 metadata and remote main. Record exact head/merge identities and whether PR 411 has an accepted successor; an open draft is not that successor.
- [x] Compare the accepted design with the inspected draft and propagate material changes to this sequence and CAP-20260916 before dependent work.
- [x] Select isolated clean code containing the accepted account owner and launcher; record revision and working-tree state. Keep private evidence in the primary checkout.
- [x] Read accepted successors of attended settlement, initial B7, rail E1/E2/E3/K1/K2/L2 and halt/resume contracts. Read relevant production code before any risk-control claim.

**Exit:** exact baseline and governing authority recorded. If the accepted design
is still unavailable, retain G0 unresolved and prepare independent evidence work;
do not relabel the proposed incident-session restriction as accepted behavior.

## Step 1 — Establish chain and actor inventory

**Outcome:** identify the real predecessor and every actor that can still affect
the account, without assuming the absence of an export interface means absence
of production state. Joshua's prior “none exists” answer establishes only that
no existing export/status interface or actor inventory was identified.

**Existing interfaces:** `BookAccountOwner.status()` and
`SettlementStore.status()` exist in the inspected code; their availability in an
actual deployed read endpoint is unverified. `BookAccountOwner.boot()` and
`SettlementStore.boot()` mutate state. `SettlementStore.status()` returns chain
head/row count and invalidation/restore state, but does not alone supply every
receipt or original supporting artifact.

- [ ] Trace configured state/artifact locations from deployment manifests and existing retained release records. Inspect only the relevant account scope; do not search or print credential values.
- [ ] Prefer an already-running read-only export. Otherwise identify a supported consistent snapshot/backup mechanism whose source-side behavior is read-only. Capture the database's committed state, including relevant WAL content; copying an active SQLite main file alone is insufficient. Do not stop production, force a checkpoint or rotate boot state to obtain a copy.
- [ ] Keep the untouched original snapshot privately with digests and capture context. Inspect schema/state read-only on an isolated copy. Any later rehearsal uses a separate derivative copy; its outputs never replace production state. If no safe capture mechanism is available, return that bounded engineering/access gap.
- [ ] Locate B7 identity, accepted chain head and receipts, calendar/policy bindings, invalidation state and outstanding operations/attempts. Distinguish production identity from synthetic fixtures and unaccepted bootstrap proposals. Cross-check the configured owner location, not just files found locally.
- [ ] Inspect current runtime senders, manual sessions, broker working orders/gross positions, CrossTrade managers/triggers/copiers and scheduled/queued actions. For each retain identity, enabled state, control owner, request-history source and possible delayed effects. Missing visibility becomes an explicit unknown actor obligation.

**Chain branching:**

| Evidence | Required disposition |
|---|---|
| Accepted production chain with valid receipts and bindings | Name its exact required next predecessor/session; preserve all intervening obligations |
| Evidence from authoritative deployment/state inventory establishes no accepted chain | Use the existing permitted initial-B7 procedure; do not infer a September 14 origin |
| Missing, contradictory, invalidated or inaccessible state | Keep chain and predecessor unknown or specifically invalidated; no new origin/database/reset |

**Acceptance cases:** a synthetic B7 does not establish production acceptance;
missing receipts are not “no chain”; an old empty snapshot does not close a
current actor obligation; apparent net flatness does not discharge gross lots,
orders or unknown requests. No actor is disabled during assessment.

**One next action if blocked:** coordinator prepares the exact read-only snapshot
or inventory acquisition needed, naming its owner and absent access. Consolidate
operator questions into one packet; never request raw credentials in chat.

## Step 2 — Resolve the no-returned-ID source question early

**Outcome:** establish a supported route protocol for original-request lookup
and delayed-effect closure, or stop with the exact missing guarantee.

**Candidate sources:** existing accessible provider request/submission history,
platform Orders/Order Details/Activity Log exports and documented route request
status/fencing interfaces. These are candidates, not asserted entitlements.
Use the actual Tradovate surface; NT8 behavior is not portable evidence.

- [ ] Inspect the available report/API surfaces once and record which support the current account and environment. Prefer existing nonempty history. Preserve original response/export bytes; the old probe's digest-only summaries cannot be replayed.
- [ ] For an existing known request, identify the key available **before transport** and whether the source can search by that key without an order ID. Matching symbol/time/quantity alone is ambiguous when multiple attempts can match.
- [ ] Obtain the source's supported coverage, ordering, retention, revision and terminal/delayed-effect semantics. Enumerating stored rows, an HTTP success or an empty result cannot establish completeness or terminal failure.
- [ ] Assemble one exact protocol: source identity; account/environment and all-actor scope; query key/bounds; coverage/fence boundary; matching/conflict rules; pending, terminal and ownership-transfer outcomes; consumer interface; stop condition. Require a source-backed common causal ordering with relevant preparation/dispatch, not a locally invented sequence number.
- [ ] Map actual positive observations into the existing request/obligation consumers in an isolated rehearsal after Step 0. If no existing ingestion path accepts the evidence, record its exact interface gap; do not fabricate broker causal/fence fields to fit a fixture.

**Required protocol outcomes:**

| Source result | Consumer obligation |
|---|---|
| Uniquely correlated accepted request/order/execution | Transfer to identified order, gross-lot, protection or quarantine ownership before releasing original request ownership |
| Supported definitive terminal rejection/no-future-effect | Resolve only that attempt; preserve all sibling requests |
| Not found, timeout, partial history or unsupported retention | Preserve original uncertain attempt and block; no resend or reservation release |
| Collision, contradictory identity or reuse of completed request identity | Retain evidence and quarantine through the existing owner |
| Manual close or local halt while older request remains possible | Keep older request owned; local fence is not remote quiescence |

**Bound:** one source/entitlement pass and one retained nonempty trace per relevant
distinct interface. Retry transport reads only within the source's documented
bounds; if none are documented, record the failure and stop that acquisition.
Repeat a capability inquiry only with a new source, changed entitlement or new
relevant observation. Never repeatedly poll absence hoping to prove a guarantee.

**Stop decision:** if no entitled source supports the protocol, retain R3
UNPROVEN; mark only a demonstrated incompatible interface UNSUPPORTED in its
examined scope. Return one concrete next disposition: inspect a named alternate
entitled source, or prepare an explicit route/contract decision. Do not buy,
migrate, contact support or weaken the contract implicitly. Route-dependent
production implementation waits; settlement work may continue.

## Step 3 — Establish a repeatable settlement evidence path

**Outcome:** S1–S5 have an admissible source package and isolated acceptance, or
one exact historical/prospective gap with its owner.

**Existing consumers:** `account_close_evidence.py`,
`account_close_calculation.py`, `book_settlement.py`, account-owner settlement
integration and listener sizing. Initial B7 remains a separate procedure.

- [ ] Bind the precise predecessor from Step 1 before requesting its historical close. With chain unknown, inventory reports and inception history without asserting which close is mandatory.
- [ ] Establish account inception from lifecycle evidence. Newly retrieve account-wide cash history from inception through capture in demonstrated bounded ranges, with overlaps and retained result/coverage evidence for empty ranges. Compare additions, removals and changed contents against prior captures; preserve all revisions.
- [ ] Seek one source-backed historical close equity/valuation record, or balance plus evidence of flatness at that same boundary. Verify report-specific timezone/offset/date semantics against the accepted account calendar. Current balance, later flatness and absent trade rows do not qualify.
- [ ] Reconcile costs and adjustments under the accepted rules; preserve effective, source publication-if-supplied and capture times. Unknown funding/classification, unresolved corrections or missing coverage refuse acceptance.
- [ ] If historical evidence is unavailable, select the following prospective branch only after determining its chain consequence. Prepare the protocol before booking an attended capture.

**Prospective protocol:** bind account, exact source-backed session/close and
all actors; name sources covering gross positions, orders, unresolved requests,
balance/equity and the finished close. Establish supported coverage across the
boundary. Two snapshots or a screen recording of a periodically refreshed UI
cannot establish unseen intervening state. If boundary flatness is not supported,
require source-backed close equity with valuation basis. Preserve the finished
report and reread full cash history for subsequent submission.

- With evidenced no accepted chain, assess this package under existing initial
  B7 C1–C10 and its separate consumption requirements. Assessment does not issue
  a production seal or authorize n3/arming.
- With an accepted chain, future capture does not repair an unavailable mandatory
  predecessor. Keep that historical gap blocked and return the exact source or
  separately reviewed amendment decision.

- [ ] For admissible actual evidence, obtain any required exact-subject operator signing action through the existing mechanism and exercise anchor plus subsequent close in an isolated non-authorizing rehearsal. No self-issued operator authority; synthetic keys establish only synthetic tests.
- [ ] Exercise correction, missing predecessor, lost receipt, stale challenge and restore behavior with synthetic cases. Verify the accepted close reaches the intended account-owner/listener consumer; collection alone is insufficient.
- [ ] Measure operator effort and evidence-to-usable-submission latency. Preserve ongoing 30-minute freshness and 300-second challenge bounds plus all other current contract conditions; B7 has separate capture/expiry rules. If the schedule cannot be met, record the measured incompatibility instead of relaxing it.

**Exit:** actual consumer acceptance for the exact evidence scope or precise
UNPROVEN/UNSUPPORTED/AMENDMENT_REQUIRED disposition. Rehearsal receipts cannot
become production receipts. No-activity sessions still require source evidence.

## Step 4 — Characterize every normal primitive

**Outcome:** the actual accepted port declarations map to source semantics and
retained traces for every required L2/normal transition. CAP-20260916's existing
N1 subrows own the matrix; do not qualify the whole book from one market order.

- [ ] Read the exact candidate port/config manifest and declared requirements. Reconcile them with rail R-B3 and the existing N1-entry/a–g/cancel/close-time/takeover/schedule rows. Missing declaration/binding remains a separate gap.
- [ ] Pair each used primitive with entitled documented semantics and existing nonempty original traces. Include entry/partial fill; resting stop; entry bracket; first attach; atomic modify; residual protection; explicit scoped close; triggered-owner/FIFO close; native trailing/OCO and preserved sibling anchor; cancellation; takeover; scheduled closure.
- [ ] Test observed identity/transition sequences through existing isolated consumers where an admissible input path exists. Identify missing parser/binding work without claiming source feasibility is completed qualification.
- [ ] For remaining observable gaps, prepare one minimal operator-run action packet sharing compatible captures. Do not execute it under this specification.

Each action packet must contain the privately bound account/environment and
route; exact starting gross positions/orders/requests; exact symbol/quantity and
primitive scope; pre-existing source-supported expected behavior; request/order/
execution/protection identities; original-byte capture sources; stop/intervention
conditions; evidence-backed teardown; authority/operator; and the owner of any
unresolved effect after the test window. No placeholder action is ready for
approval. If source semantics themselves are absent, a test packet is not the
next step: stop for the source/route decision.

**Acceptance cases:** rejection retains old protection for atomic amend; partial
fills preserve correct residual quantities; a scoped close removes only its
qualified scope; triggered protection preserves the specified FIFO and surviving
sibling lifecycle; fixed-component modification preserves trailing anchor;
cancel/fill races retain both obligations until resolved. No executable reverse
orphans, non-atomic substitutes or locally simulated native trailing.

**Exit:** source/trace feasibility sufficient for a bounded integration proposal,
or precise row blockers. Actual transmitted tests remain separately approved;
simulation of an order environment cannot qualify a different production route.

## Step 5 — Verify consumers and specify production integration

**Outcome:** distinguish proven local behavior from actual source capability,
then deliver a buildable integration packet only for interfaces whose producers
are established. This specification does not authorize the production build.

Inspected code has a synthetic-only broker seam and returns
`production_route_unavailable` without it. Preserve that refusal until the later
implementation is reviewed. Do not wire a real transport into `SyntheticBroker`.

- [x] Run doctor from the selected clean accepted checkout before project Python. Diagnose any failure; never fall back silently to system Python.
- [x] Run the following existing consumer suites, inspecting current paths first. Preserve actual commands, interpreter, revision/dirty state, pass/fail/skip counts and automatic verification-record locations. Required signing cases must run.

```powershell
.\fp.ps1 doctor
.\fp.ps1 python -m pytest tests/ops/test_book_account_owner.py tests/ops/test_book_owner_settlement_integration.py tests/ops/test_account_close_evidence.py tests/ops/test_account_close_calculation.py tests/ops/test_book_settlement.py
.\fp.ps1 python -m pytest tests/ops/test_book_protection_identity.py tests/ops/test_book_protection_allocations.py tests/ops/test_book_protection_evidence.py tests/ops/test_book_protection_lifecycle.py tests/ops/test_book_takeover_phases.py
```

Without PowerShell 7.3+, use the documented `python -I scripts/fp.py doctor`
and `python -I scripts/fp.py python -m pytest ...` bootstrap from that checkout.
Project child processes use `sys.executable`; operations and research environments
remain separate. No production database path or credential goes to pytest.

- [ ] Map decisive traces to exact tests: crash before/after send; two unknown attempts with one resolved; cancel/partial-fill race; manual close followed by a delayed older request; provider work after local halt; restart/rollover; residual protection; correction and restored settlement binding. A listed suite name is not proof of coverage. Missing cases become a bounded engineering task with a reproducer.
- [ ] Assemble the production integration packet only after the relevant source-feasibility checks succeed. Specify the real producer → parsing/identity binding → owner consumer for each fact, supported transport result states, attempt persistence before send, uncertain-outcome ownership, causal/history cursor persistence and restore behavior. Include exact files/APIs and acceptance cases discovered on that baseline; do not invent an unavailable provider API now.
- [ ] Require code review of that packet before subsequent implementation authority. Later implementation must preserve single-writer ownership, generation/boot fencing, partial outcomes, no blind resend and existing normal primitives. Qualification still requires actual evidence through the integrated consumer; a parser or adapter test alone is insufficient.
- [ ] Obtain independent review of the complete path and update CAP-20260916. Keep each row UNPROVEN until its source evidence and applicable consumer acceptance both exist.

**Combined acceptance trace:** admissible B7/close → verified owner/listener
binding → durable admitted attempt → actual route outcome → normal closure or
attended intervention → complete account-wide reconciliation → ordinary disarm.
At any missing transition preserve the block and existing obligations. Full live
acceptance additionally depends on the later Phase 3–6 gates; this path grants
neither trading permission nor a feed/symbol qualification by implication.

## Completion and stopping rules

This sequence completes its assessment/handoff when every row has qualified
evidence or a precise stopped disposition, the chain consequence is explicit,
the no-ID protocol is supported or explicitly missing, every used primitive is
covered, and the implementation packet is either concrete or blocked by named
inputs. It may validly conclude BLOCKED FOR LIVE RELEASE. Record unfinished
steps honestly; no source-feasibility checkpoint becomes a QUALIFIED verdict.

Stop investigating an unchanged endpoint once its relevant limitation is
established. Continue independent work. Reopen only for new evidence, entitlement
or source/contract change, retaining previous versions and verdicts. A later
support response is handled through that same rule, without restarting the
entire assessment.

Draft verification: source/consumer boundaries were checked against the pinned
code and existing decision record. Self-review covered chain-unknown/no-chain
branching, no-ID absence versus terminal evidence, prospective-capture limits,
source-feasibility versus integration qualification, and separate order-test/
implementation authority. No Python, private acquisition or capability test ran
while drafting this specification.

## Execution ledger — September 17 UTC

CAP-20260916 is the authoritative outcome record. Unchecked items above are
unfulfilled evidence/qualification requirements, not permission to infer them.

| Step | Executed result | Stopped dependency |
|---|---|---|
| 0 | Accepted merge pinned; unchanged design; isolated code containing PRs 409/413 | None for bounded assessment |
| 1 | Approved metadata from both known deployments; disarm/emission config observed | No chain located in inspected paths; other acceptance locations and external actors unknown |
| 2 | Documented positive client-ID lookup identified; authenticated nonempty Orders observed | No original export retained, terminal negative evidence or all-actor remote fence |
| 3 | Report entitlement and account-summary/position-history views inspected; synthetic consumers exercised | Inception, fresh complete cash history, exact predecessor and admissible close package absent |
| 4 | Candidate semantics reviewed; two incompatible realizations scoped in N1 | Actual port binding and complete primitive traces absent |
| 5 | Doctor and selected suites: 316 + 119 passed, zero skips; precise trace gaps recorded | Actual-evidence rehearsal and production packet require established producers |

No production implementation or release acceptance results from this execution.
The stopping rule returns precise source and engineering tasks in CAP-20260916;
four missing exact consumer sequences remain explicitly unclaimed. Original
private captures and verification records stay outside the publication. Final
independent review is recorded in the capability decision before publication.
