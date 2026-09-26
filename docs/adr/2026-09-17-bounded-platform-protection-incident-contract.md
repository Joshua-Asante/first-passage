# ADR — Bounded platform protection during signal/control incidents

**Status:** `Proposed` — operator-directed contract amendment, pending governing-contract propagation and route qualification. No implementation or live acceptance.
**Decision date:** 2026-09-17
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Authors:** Joshua (direction) + Codex (assessment).
**Proposes to amend:** The incident authority interpretation in the halt/resume contract and Phase 5 plan. Retains the no-same-session strategy-reactivation design restriction; no effective contract changes yet.
**Layer:** execution.

> **Addendum 2026-09-24 (Proposed):** §2's "Unknown entry, add, cancel, close or modification" row is proposed to change for narrowed-shape requests: a permanent worst-case reservation instead of an account block. See [the addendum](#addendum-2026-09-24--bounded-exposure-reservation-for-unknown-requests-proposed) (revised 2026-09-25, §A8). Not effective until accepted and propagated.

## §0 — Rule 0 reads and verification anchors

Read before authoring:

- `ops/c1_rail/book_account_owner.py` at commit `b4aa8efb0ee8f6d40b5aa332d5bb850bfa8b68ac`: `_dispatch_action_locked` refuses `INTERVENTION`; `_halt_db` retains a durable halt and invalidates bootstrap authority; production transport is unavailable outside the explicit synthetic seam. `git diff b4aa8ef 95b37af -- ops/c1_rail/book_account_owner.py ops/c1_rail/book_policy.py` is empty.
- `ops/c1_rail/book_policy.py` at that same commit: fixed-book policy, sizing and protected-rule definitions inspected. This amendment changes none of those constants or allocation rules.
- `docs/spec/2026-09-14-tb-s3-halt-resume-contract.md` at `95b37afaad319cbebf421f8a89fa9e6d1e2bd732`: incident revokes normal and scheduled runtime sends; provider managers are separately inventoried actors. The current code and contract do not implement this amendment.
- [Capability decision](../briefs/phase4-preparation/2026-09-16/capability-decision.md) at commit `95b37afaad319cbebf421f8a89fa9e6d1e2bd732`, inspected 2026-09-17: local R1 qualified; whole-route N1 and R2–R5 unproven; inline triggered trail and cancel/replace have scoped incompatibilities. No new private acquisition was performed here.
- [Feasibility design](../superpowers/specs/2026-09-16-tradeify-settlement-order-feasibility-design.md) and [Phase 5 plan](../superpowers/plans/2026-09-16-phase5-attended-operations.md): published with this ADR at reachable commit `32a71bd6f27dcfc75d11b39c9db7cbaa7727bebb`. Original drafting used local copies; those local checkout identities are not verification anchors. Use the committed sources and checks below for reproduction.

Primary NinjaTrader documentation inspected 2026-09-17:

- [Using ATM strategies](https://ninjatrader.com/support/helpguides/nt8/using_atm_strategies.htm): signal generation can hand execution to ATM; host strategy position/PnL and session-close settings do not govern that execution; ATM is real-time only.
- [Auto Trail](https://ninjatrader.com/support/helpguides/nt8/auto_trail.htm): profit trigger, offset and adjustment frequency, with multiple steps. Feature availability does not prove portfolio equivalence.
- [Server-side versus local ATM](https://ninjatrader.com/support/helpguides/nt8/server-side-vs-local-atms.htm): different scaling, cancellation and attachment behavior; documented server-side mode is connection-specific and cannot be used with NinjaScript. Opposite positions can net flat while protective orders remain. These are documentary bounds, not this account's entitlement or tested behavior.

## §1 — Context

Requiring every platform modification to stop on every incident made programmatic ATM pause appear essential and pushed the design toward custom trailing infrastructure. The operator now selects a narrower objective: stop new strategy activity while qualified, already established platform protection continues on known exposure until attended intervention. The existing local runtime fence remains useful; its existence never proved that remote managers had stopped. The actual change is to authorize a bounded class of surviving platform behavior explicitly, rather than treat it only as residual work awaiting shutdown.

**Decision driver:** select the smallest platform-supported execution behavior and assess its economic differences before specifying another custom subsystem.

## §2 — Proposed decision and replacement incident language

**Effectiveness gate:** The following is candidate contract text for investigation, not an effective exception. Operator direction to reconsider the design and permission to publish do not establish acceptance of these detailed semantics. The accepted halt/resume and rail contracts continue to govern implementation and capability verdicts. Only after explicit acceptance and propagation to the governing owners may this text authorize dependent behavior; until then, record such dependencies as AMENDMENT_REQUIRED rather than QUALIFIED under the proposed exception.

On an incident, durably stop new strategy commands for the account session. Do not re-enable strategy activity in that same account session, including after flatness, reconciliation, restart, restore, feed recovery or civil-date rollover. Fresh later-session authorization retains the existing settlement, identity, reconciliation and readiness gates.

For a narrowly qualified signal/control failure, an already established platform protection mechanism may continue only within its previously authorized envelope on identified existing exposure. This is continuing authority, not a new command permission. The bridge may observe and alert but may not create, repair, retune, replace or expand protection after the incident. All new runtime broker commands remain fenced, including strategy closes and scheduled flatten commands. Already accepted platform orders and their qualified internal protective actions are distinct from new bridge dispatch.

| Incident class | Continuing authority | Required response |
|---|---|---|
| Signal daemon/bar/control-channel failure isolated from protection dependencies | Only the specifically qualified pre-existing stop/target/OCO/trailing mechanism | Latch strategy halt, fence every strategy sender, retain observations and alert for attended intervention |
| Unknown entry, add, cancel, close or modification | No new command; no assumed outcome or speculative repair | Retain original attempt, reservation and account block. Affected protection is not presumed safe. An independently qualified unaffected mechanism may continue only if non-interference is proved; otherwise use the next row |
| Protection identity, quantity, ownership, platform state, required market data or manager health uncertain/failed | No assertion of safe autonomous protection | Immediate attended intervention/escalation using the qualified platform procedure; retain all possible effects and uncertainty |
| Mixed, unclassified or unavailable safety state | No signal-only exception by default | Apply the protection/state-failure response |

Losing authorization to rely on a manager is not proof that it has stopped. Do not blindly cancel a working protective stop or claim a remote pause. The operator needs the supported intervention procedure, including races with orders/managers still running. A platform that cannot be brought under attended control is unsuitable; this does not impose automatic programmatic pause for every signal failure.

### Qualification of continuing protection

Before admission, bind the exact account/environment, instrument, exposure/fill ownership, platform/version/connection mode, manager instance, child orders/OCO relationships, template/settings and authorized quantity. Record establishment evidence; an entry acknowledgment or locally generated ATM ID is insufficient.

The envelope permits only the original exit/stop/target/trailing lifecycle and proved quantity reduction for residual exposure. It permits no entry, add, reversal, auto-reentry, unrelated position management or post-incident parameter expansion. Qualify partial entry fills, partial exits, sibling cancellation, overlapping protection, rejected amendments and manual-intervention races. Protective quantity must remain correctly tied to actual residual exposure; labels such as “reduce risk” and net-flat snapshots prove neither that property nor absence of reverse exposure.

The failure class must be isolated from dependencies used by the manager. A missing strategy signal feed can qualify only if it is not the manager's required price source. Shared host failure, platform restart, connection loss or stale execution observations are not automatically signal-only failures. Specify the maximum observation gap and failure-detection bound for the selected route before qualification; this record invents neither a timing guarantee nor a loss bound.

Previously sent entries/remainders may fill after the fence. They remain outstanding exposure obligations, not an exception authorizing new risk. Do not cancel/resend them speculatively or count an unfilled entry's prospective bracket as established protection. Late fills, insufficient protection or unknown remaining quantity demand attended handling. Any future desire to authorize automatic post-incident remainder cancellation or first attachment requires its own explicit amendment.

Attended intervention begins on the alert; it does not mean waiting indefinitely for a target. Existing session cutoff/own-flat deadlines remain obligations. Since a signal incident can remove the ordinary scheduled-close sender, qualification must prove the attended cutoff procedure under that failure. An independently pre-authorized platform scheduled exit would need explicit qualification of its own envelope; it is not granted by calling it protective.

## §3 — Alternatives and ATM reassessment

| Alternative | Disposition |
|---|---|
| Stop every platform mutation after any incident | Proposed replacement for qualified signal/control faults; current governing requirements remain effective pending acceptance and propagation |
| Continue anything called protective | Rejected: uncertain identity/quantity and duplicate exits can create exposure |
| Custom trailing manager now | Defer the design choice while assessing the proposed exception; pause requirements are not waived in current qualification |
| Ordinary ATM plus thin command-and-observation bridge | Preferred candidate for qualification, not yet a sufficient or selected production route |

The bridge retains one durable owner for admission, session restrictions, command attempts and uncertainty. It translates already authorized commands, binds platform identities, collects order/execution/manager observations with coverage limits, and alerts. It does not reproduce native trailing logic or claim exactly-once execution from local deduplication. Fence at the last strategy-command dispatch boundary, including downstream queues/reconnect replay; a dead daemon alone is not a fence. Already transmitted requests retain their possible effects.

The platform owns only the qualified protection envelope. Compare an ordinary local NinjaTrader ATM with the actual incumbent route; do not conflate NinjaTrader ATM, Tradovate ATM and CrossTrade-managed trailing. The current CAP record's inline-ATM correlation limitation is not cured by this incident amendment. Its ordinary-placement positive lookup recipe cannot be transplanted to ATM without proof. Absence from a query never permits resend.

| Required assessment | Minimum evidence / consequence |
|---|---|
| Exact platform, mode, entitlement and failure domain | Name the real supported route. Daemon shutdown must leave the qualified manager functioning; platform/connection failures receive a separate verdict |
| Initial stop/target and first attachment | Fill-to-child identity and establishment timing, including bare-lot attachment if used. Unknown or rejected attachment fails qualification |
| Trailing economics | Compare each used leg's activation basis, price source, tick rounding, step frequency, anchor preservation, tightening and fixed-stop interaction with its pinned production port. Tick-driven and bar-driven behavior are not interchangeable by assertion |
| Partial fills, adds and multiple managers | Prove ownership, per-fill versus average-entry basis, quantity adjustment, OCO behavior and absence of duplicate/reverse exits through races |
| Strategy amendments and scoped exits | Prove supported modification and close behavior, sibling cleanup, takeover and schedule. Removing incident pause does not make non-atomic cancel/replace equivalent to native amendment |
| Observation and unknown requests | Retain durable intent before transport, request/ATM/order/fill linkage, restart uncertainty and supported terminal evidence. Remain blocked when resolution is unavailable |
| Portfolio economics | Explicitly list changed normal-path and incident-path behavior. Preserve current allocations/policy; any economic deviation needs separate acceptance based on named evidence, not an invented tolerance or outage frequency |

**Assessment:** ATM may remove custom protective-order management and all automatic pause plumbing. It does not remove admission/sizing, uncertain-attempt accounting, actual observation, settlement or attendance. Whether the whole portfolio fits ordinary ATM remains UNPROVEN. No sufficient-route claim follows from vendor feature documentation alone.

## §4 — Falsifier and binary gate

If any qualified signal/control fault interrupts the manager's required dependencies, allows a new strategy send/replay, loses protection identity or produces duplicate/reverse exposure, then reject that route's continuation qualification and retain attended intervention; do not broaden the exception. If ATM cannot reproduce a required normal-path behavior, then ordinary ATM is insufficient for the unchanged portfolio: either approve a specifically measured economic difference, add only the missing mechanism, or reject the route.

**Gate:** QUALIFIED only when every applicable §3 row has route-bound source evidence and a passing concrete trace with no unresolved ownership/quantity/unknown-request defect. Otherwise UNPROVEN or UNSUPPORTED as the evidence warrants; live release remains blocked. Check at first qualification and after platform/template/route or relevant portfolio changes. No completed traces are claimed here.

Required trace assertions: daemon loss after established bracket leaves only authorized ATM activity; queued signal after halt sends nothing; lost entry response stays unknown without resend; partial fill plus halt retains remainder obligation; partial target fill adjusts/cancels siblings without reverse exposure; uncertain modification never causes repair; stale manager state escalates; restart and restored old state refuse same-session activation; manual close racing ATM action retains every effect; cutoff during outage reaches the unchanged attended closure requirement.

## §5 — Forbidden moves

- Do not replace automatic pause with an unrestricted “risk-reducing” send bypass.
- Do not interpret flatness, timeout, restart or successful ATM callback as closure of an unknown attempt.
- Do not adopt server-side ATM capabilities for a local/NinjaScript route, or assume local ATM survives a host failure.
- Do not silently replace portfolio bar/anchor/rounding/exit semantics with convenient template behavior.

## §6 — Consequences and propagation

If accepted and propagated, the benefit would be a smaller candidate execution bridge and removal of programmatic ATM pause as a universal requirement. The cost would be explicit dependence on the selected platform manager and an attended intervention procedure while its state may continue changing. The proposal does not promise prevention of every late fill or bound incident losses.

Before implementation, propagate the authority split and no-same-session restriction together into the accepted halt/resume contract, rail E1/E2/E3 and L2 mappings, feasibility design, Phase 4/5/6 acceptance lists, arming/operating procedure and CAP-20260916. Preserve historical evidence and keep CAP as the capability-verdict owner. This amendment does not upgrade any CAP verdict.

The four planning/design documents carry investigatory notices, not precedence overrides. The governing contracts are present in this branch but have not been amended. This ADR remains Proposed and changes no current permission or acceptance criterion. Continued design reconciliation is within the operator's request; making the resulting exception effective requires explicit acceptance and propagation.

## §7 — Next bounded work

Design/evidence only: select the exact ordinary ATM candidate, map the existing portfolio actions to its supported behavior, and return the §3 table with precise gaps and economic differences. Keep current-contract qualification separate from prospective qualification under this proposal. First test the decisive separation of signal failure from ATM operation in an isolated authorized rehearsal, then the partial-fill/unknown-order cases. Defer the custom-trailing design choice until this assessment; no current pause requirement is waived. No new order drill, host change or deployment was performed in this task.

## §10 — Audit hooks

From a checkout containing this ADR:

```powershell
git diff b4aa8ef 95b37af -- ops/c1_rail/book_account_owner.py ops/c1_rail/book_policy.py
# Expected: empty; pins the production reads across these revisions.
git show 95b37af:docs/spec/2026-09-14-tb-s3-halt-resume-contract.md | Select-String 'INTERVENTION permits no new runtime broker mutations'
# Expected: old contract present; full propagation is explicitly pending.
rg -l '2026-09-17-bounded-platform-protection-incident-contract' docs/superpowers/plans/2026-09-16-phase5-attended-operations.md docs/superpowers/plans/2026-09-16-phase4-real-capability-qualification.md docs/superpowers/plans/2026-09-16-self-service-capability-closure.md docs/superpowers/specs/2026-09-16-tradeify-settlement-order-feasibility-design.md
# Expected: all four planning documents contain the investigatory notice.
```

## Verification

The earlier local-working-copy 5/5 result is withdrawn as evidence for the published artifact: its checkout and external checker were not portable verification anchors. Review repairs are based on reachable commit `32a71bd6f27dcfc75d11b39c9db7cbaa7727bebb` (original ADR blob `cf7503f2b627416ab78a3e5f67b8c49c17bf3ba2`). Final verification is posted to PR 416 after the repair commit, with the exact committed revision and ADR blob, avoiding a self-referential hash in this file.

Reproduce on that committed revision using repository-owned tooling:

```powershell
.\fp.ps1 doctor
.\fp.ps1 python .claude/skills/brief-authoring/scripts/check_brief.py docs/adr/2026-09-17-bounded-platform-protection-incident-contract.md --type adr
.\fp.ps1 python scripts/check_adr_graph.py
git rev-parse HEAD
git rev-parse HEAD:docs/adr/2026-09-17-bounded-platform-protection-incident-contract.md
git rev-parse HEAD:.claude/skills/brief-authoring/scripts/check_brief.py
```

These checks validate document structure and source references, not ATM capability or runtime behavior. No runtime or complete gate-suite pass is claimed.

## Addendum 2026-09-24 — bounded-exposure reservation for unknown requests (Proposed)

**Status:** `Proposed`, like the ADR it amends, and under the same §2 effectiveness gate. Nothing below is effective until the operator accepts it and it is propagated to the owners in §A5. Until then every dependent behavior is AMENDMENT_REQUIRED, and the current rule governs: an unresolved entry or add refuses every new risk-add (`book_account_owner.py:1608`, `unknown_order`).
**Origin:** T08 R3 = NONE ([T08 §7](../briefs/handoffs/2026-09-21-tradeify-t08-broker-protection-feasibility.md#7-executor-return)): no documented fence exists for an unknown request on the CrossTrade → Tradovate route. Operator rulings 2026-09-24: "approve item 1" (hold live release; vendor question; scope this amendment) and "I accept B. You can proceed as scoped" ([scope](../superpowers/specs/2026-09-24-bounded-exposure-unknown-request-amendment-scope.md), Q1 = B).
**Rewrites:** §2's row "Unknown entry, add, cancel, close or modification", for the narrowed shape only (§A1). Every other §2 row, §4 and §5 stay as written.

### A0 — Rule 0 reads

| Source | Anchor | What it establishes |
|---|---|---|
| `ops/c1_rail/book_account_owner.py` | `_ordinary_unknown_orders_db` :768–798; admission :1606–1622 | Today's account fence: any entry/add attempt that is `UNKNOWN`, or not resolved by an accepted terminal, refuses every risk-add. Capacity is reserved before dispatch (`Reserve`). |
| `ops/c1_rail/book_policy.py` | `CapacityLedger` :570–; `BOOK_LEGS` :179–196 | Reservations count against the account micro cap until released; four legs; this addendum changes no constant, allocation or sizing law. |
| `core/dd_protection.py` | `DD_TRIGGER`/`DD_SCALE` (frozen, import-guarded) | This addendum does **not** feed held reservations into the protection rule's equity input (§A2 rule 4). |
| [Halt/resume contract](../spec/2026-09-14-tb-s3-halt-resume-contract.md) | §3 ¶2, §4 ¶1–2 | "no unresolved requests"; "unresolved owner cannot be overridden"; a different protocol needs "a concrete separately reviewed amendment" (this one). |
| [Rail extension spec](../spec/2026-09-12-c1-multi-leg-rail-extension-spec.md) | E3 row; §2 S1–S5; R-B3 L2(a)–(g) | "Each unresolved request owns an account block"; the order-shape contract. |
| [CAP-20260916](../briefs/phase4-preparation/2026-09-16/capability-decision.md) | R3 row; N1 table; Addendum 2026-09-24 | R3 NONE; N1 rows UNPROVEN. |
| [Closure plan](../superpowers/plans/2026-09-16-self-service-capability-closure.md) | Step 2 outcome table | Row "Not found, timeout…": preserve and block. |

### A1 — Scope: the narrowed shape

The reservation replaces the account block only for an **exposure-creating request of the narrowed shape**: a single market or stop entry (or add) for **exactly one contract**, carrying its own native stop in the same request (CrossTrade `place` with `stop_loss` → one Tradovate `placeoso`), sent without `delay=`, ATM fields, trailing fields, `cancel_after` or copier/multi-account fan-out, from the runtime's own client. Every other request shape keeps today's rule unchanged.

**Why one contract.** The N1 map (§A4) found the bracket created with the entry in one broker call, but Tradovate activates the stop on the entry's **first fill** and sizes it to that fill. Quantity filled later is covered only by CrossTrade's after-the-fact repair. A one-contract request fills in one print, so its stop covers the whole fill. For more than one contract, quantity × stop distance is not a bound the broker enforces. A multi-contract intent can still be sent as that many one-contract requests; each one is its own narrowed-shape request with its own reservation.

**Admission precondition (hard):** the narrowed shape is admissible only while CAP records (i) the entry-and-bracket single-call creation and (ii) first-fill activation for a one-contract request, each with a retained source. Without both, an unknown entry's worst case is unbounded and this addendum grants nothing.

**Residual inside the bound (accepted by this rule, not hidden):** there is always a broker-side interval between a fill and its stop reaching Working, and a stop leg can reach a rejected or ended state while the position stays open. Rule 3's gap allowance must cover the activation interval. A stop that fails to activate is an unexplained, unprotected position, which rule 6 routes to attended intervention. In that state the exposure is bounded by the attended response, not by the reservation. §A6 makes that a falsifier to measure, not an assumption.

### A2 — The rule

1. **An unknown narrowed-shape request holds a reservation, not an account block.** Its original attempt, identity and contracts stay owned exactly as today (no resend, no speculative cancel or repair, no release on absence, flatness, elapsed time, empty reads, restart or operator acknowledgment).
2. **The reservation is permanent until evidence.** It is released only by (a) a uniquely correlated outcome under the closure plan's first two rows, or (b) option A: a written, retained vendor bound on all deferred work for this shape, plus a margin, elapsed with no effect observed in the window. Nothing else releases it, across sessions, restarts and account days.
3. **Worst-case charge.** Each held reservation carries a worst-case loss: its quantity × (distance from the intended entry to its attached stop + the gap allowance) × point value, computed from the request's own retained fields. For a stop entry, the entry level is the stop-entry price; for a market entry, the reference price in the intent plus the gap allowance.
4. **Admission check (new, account-level).** A new risk-add is admitted only if the sum of all held worst cases plus the new request's own worst case stays within the account's room to the venue drawdown floor, less the reserve margin. This is an admission gate in the account owner. It is **not** an input to `dd_protection` and never alters the protection rule's equity, trigger or scale. With no held reservations the check is the existing admission unchanged, so the qualified normal path is unaffected. (To verify at implementation: a replay with no unknowns produces byte-identical admission decisions.)
5. **Micro-cap accounting.** A held reservation keeps its contracts in `reserved` for its leg's symbol, as today.
6. **Unexplained later effects are incidents.** Any position, working order or fill that no owned operation explains, on any symbol, triggers the §2 protection/state-failure row (immediate attended intervention). An observed effect never releases a held reservation, because no fill can be uniquely correlated to an unknown request (T08 §7.3 blockers 1–2). It becomes an additional identified exposure alongside the reservation, which may double-count. Double-counting is deliberate.
7. **Unknown non-entry requests** (amend, cancel, close, attach, flatten): the §2 row "Protection identity, quantity, ownership … uncertain/failed" applies. That means immediate attended intervention, with no autonomous protection claimed. New risk-adds on the affected leg stay refused until attended reconciliation establishes its position and working orders from fresh evidence. An unknown cancel of a resting entry leaves that entry's reservation held under rule 2, as S4 already requires.
8. **Exhaustion.** When the held worst cases leave no room for any leg's minimum request, automated risk-adds stop by arithmetic. No waiver, reset or operator acknowledgment restores room; only rule 2's evidence does.

### A3 — Figures

The gap allowance, the reserve margin and the definition of "room to the venue drawdown floor" (intraday-enforced trailing, per `lesson_tradeify_trail_enforced_intraday`) are load-bearing numbers. They are bound from [load_bearing_numbers.md](../load_bearing_numbers.md) at candidate binding (checklist T16), not written here. Until bound, rule 4 is AMENDMENT_REQUIRED.

### A4 — Fit with the book (scope Q3)

**Source.** A documentary N1(a)–(g) map, 2026-09-24. Read-only; no login or order action. Retained privately at `local_artifacts/t08-r3-2026-09-24/n1-map-2026-09-24/` (`N1_MAP.md` SHA-256 `359e98f5466e5fac…`, directory index `9eca5f343b7310e5…`; 11 content files incl. 7 new public Tradovate help-centre captures with URL, time and hash). 43 of 45 quotes re-verify byte-for-byte against the retained pages; the 2 misses are JSON `–` escape artifacts on a status-definition page, not load-bearing. The decisive facts (single-call OSO creation, first-fill activation and sizing, the activation interval, the plain-Stop bracket) sit on the CrossTrade internals page CAP already cites (`adaa513e8eb096a8`) and on `1142e6b7f340adac`. No vendor text is reproduced here. The map is documentation only: it qualifies nothing, and every row stays UNPROVEN in CAP until traced.

**Per-primitive result on this route** (S = documented supported, K = unknown until a drill, U = documented unsupported):

| Primitive | Result | Note |
|---|---|---|
| Market entry; resting stop entry, L2(a); bracket at entry, L2(b) | S (creation only) | Acceptance is not rest or fill. |
| Atomic native modify, L2(c) | K | Whether the old stop survives a rejected modify is unread. |
| Full close, L2(d) | K | A liquidate is documented as a request, not a guarantee. |
| Partial/scoped close, L2(d) partial | U | Leaves working orders in place; a reversed position is possible (inference). |
| Residual cover on partial entry fills, L2(e) | U | First-fill sizing; later quantity covered only by CrossTrade repair. |
| First attach to an open fill, L2(f) | U | Only a cancel-then-place composite exists. |
| Native activated trailing, OCO-linked, L2(g) | U | The bracket stop is a plain Stop; the only activated trail is CrossTrade-managed (CAP 09-17 finding re-confirmed). |
| Close-time crossed-level exit preserving FIFO ownership | U/K | — |
| Cancel's effect on suspended bracket legs; exit-side partial fills | K | Unread. |

**Per-leg fit (facts for the operator; the addendum makes no strategy change):**

| Leg | Fits with every exposure-creating request in the narrowed shape? | What falls outside |
|---|---|---|
| ORB MNQ | **No**, on L2(g) alone | Its bracket carries trailing parameters. Otherwise it fits: entries and adds are one contract. |
| Striker MYM | **No** | It enters bare and attaches later (L2(f) U). Multi-contract entries. Close-time exits U/K. |
| Vanguard MGC | **Undetermined** | Protection cases aren't public (private port). Quantities up to 2 need per-contract requests. |
| Aegis 6J | **Undetermined; no for full cover as one request** | Protection cases aren't public. 3–8 contracts need per-contract requests. The breakeven move is an L2(c) modify (K). The takeover is a non-entry composite. |

**Consequence (stated, not decided).** The largest blockers are **not caused by this addendum**. L2(e), L2(f) and L2(g) are unsupported on this route for normal-path trading whatever posture governs unknowns, and CAP recorded L2(g) as unsupported on 2026-09-17. What this addendum adds is the one-contract request rule. As publicly declared, no leg is shown to trade on this route with every exposure-creating request in the narrowed shape. The rail spec (S2, D-B4) forbids a substitute expression without requalification. Whether to requalify changed expressions (for example a fixed-stop ORB bracket, or a Striker entry carrying its stop), or to reject the route, is an **operator decision outside this addendum**. It is recorded as the scope's Q3 outcome.

*Correction, 2026-09-25 (operator rulings; prior text preserved above):* the per-leg table is superseded as follows. **Vanguard MGC** and **Aegis 6J**: fit — operator-attested ("yes and yes" to a fixed stop in the same order and one-contract expressibility); private ports unread by any agent; L2(c) and the takeover composite stay K. **ORB MNQ** and **Striker MYM**: the operator adopted route-native editions (ORB fixed-stop OSO bracket without trailing; Striker entry carrying its stop, one-contract requests) for pre-registered K=1 requalification. Owner: [campaign record §59](../briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#59--route-native-expressions-for-the-accepted-book-three-operator-rulings-2026-09-25). This corrects §A4's fit facts only; §A1–§A3 and the addendum's Proposed status are unchanged, and the §A1 admission precondition still needs a retained trace.

### A5 — Propagation on acceptance (not applied)

On acceptance, each owner receives a dated addendum carrying the text below. No owner text is edited before acceptance.

| Owner | Place | Replacement or addition |
|---|---|---|
| Halt/resume contract | §3 ¶2 | Add: "An unknown narrowed-shape request held under the bounded-exposure reservation (incident ADR Addendum 2026-09-24, §A2) does not prevent recovery completion; it remains held and charged. Every other exclusion in this paragraph stands." |
| same | §4 ¶1–2 | Add: "A reservation-held unknown is not an 'unresolved owner' for resume, provided §A2 rule 4 admits. This addendum is the separately reviewed amendment §4 names." |
| Rail extension spec | E3 row | Add: "For a narrowed-shape exposure-creating request (incident ADR Addendum 2026-09-24 §A1), the unresolved request owns a permanent worst-case reservation instead of an account block. All other shapes keep the block." Acceptance case: two narrowed-shape unknowns; a third request is admitted iff §A2 rule 4 holds; an unknown non-entry request still blocks its leg. |
| CAP-20260916 | R3 row | Dated addendum: "R3 remains NONE as a fence finding. Under incident ADR Addendum 2026-09-24 the consumer outcome for narrowed-shape unknowns is a held reservation; admissibility depends on the OSO-atomicity row." |
| Closure plan | Step 2 outcome table | New row beside "Not found, timeout…": "Narrowed-shape exposure-creating request, outcome unknown → hold a permanent worst-case reservation (incident ADR Addendum 2026-09-24 §A2); no resend, no release without evidence." |
| Account owner code (T09/TB-I3 scope, after acceptance) | `_ordinary_unknown_orders_db` / admission | Split narrowed-shape unknowns out of the refusal into the §A2 rule 4 check; keep every other unknown refusing. |

### A6 — Falsifiers

- If CAP cannot record the attached stop as atomic with the entry, the narrowed shape is inadmissible and this addendum grants nothing (§A1).
- If any documented vendor mechanism can turn a narrowed-shape request into a larger or unprotected exposure (quantity growth, stop removal, reversal), the worst-case charge is not a bound. Reject the addendum for that shape.
- If the no-unknowns replay's admission decisions differ from today's (§A2 rule 4), the check is not inert on the normal path. Fix it before acceptance; never accept it as an economic change.
- If a one-contract request can fill in more than one print, or its stop can activate for less than the filled quantity, the one-contract premise fails. Reject the addendum.
- If attended detection plus response to a failed stop activation (§A1 residual) cannot be demonstrated within the room rule 4 leaves, the reservation is not a bound in that state. Measure it at T13 (attended operations) before any live use; never assume it.

### A7 — Forbidden under this addendum

Releasing a reservation on flatness, elapsed time (except option A's retained vendor bound), empty reads, restart or acknowledgment; feeding held reservations into `dd_protection`; resending; admitting a non-narrowed shape under the reservation; treating an observed later fill as correlated to an unknown request; writing the §A3 figures anywhere but their owner.

### A8 — Revision 2026-09-25 (Proposed): the whole book in the narrowed shape

**Why.** On 2026-09-25 the operator attested that Vanguard and Aegis fit §A1 and adopted route-native editions for ORB and Striker ([campaign record §59](../briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#59--route-native-expressions-for-the-accepted-book-three-operator-rulings-2026-09-25); [pre-registration draft](../briefs/pre-registration/2026-09-25-tradeify-route-native-editions-prereg.md)). Once the editions are frozen and requalified, **every** exposure-creating request of the book is in the narrowed shape. The reservation then governs the normal path of all four legs, not an edge case, and multi-contract intents become several one-contract requests. §A1–§A7 stand. This section adds two rules and records facts; it stays Proposed under the same gate.

**Rule 9 (proposed): split intents are admitted whole or not at all.** A multi-contract intent (Striker up to its maximum setting, Aegis up to its captured size, Vanguard base plus adds) is admitted only if rule 4 admits the **sum** of its one-contract worst cases on top of every held reservation, checked before the first request is sent. Otherwise the whole intent is refused. Admission never sends a partial intent. After sending, confirmed fills are the leg's position; a refused request is not re-sent; an unknown one holds its own reservation (rule 1). This matches pre-registration STR-4.

**Rule 10 (proposed): one unresolved request per symbol.** The next one-contract request of a split, or any new exposure-creating request on that symbol, is sent only after the previous one on that symbol is acknowledged or refused. One transport failure can therefore create at most **one** held reservation per symbol, not N. *Tradeoff, stated rather than hidden:* a split of N now takes N sequential acknowledgement round trips, so later contracts can fill at worse prices. The pre-registration's §6 replay-modelling choice must price that latency before freeze. Without rule 10, a single failed 30-contract Striker split could hold 30 reservations and reach rule 8 exhaustion in one event.

**Facts recorded.**
- *Exit-side partial fills (T08 residual row):* moot by construction. Under the one-contract rule an exit is for one contract and cannot partially fill.
- *§A1 admission-precondition trace:* the planned source is drill D1 of the [2026-09-25 operator session plan](../notes/2026-09-25-t08-drills-t07-reads-operator-session.md), authorized in principle by the operator on 2026-09-25 and performed by Joshua. Until that trace is retained and recorded in CAP, this addendum still grants nothing (§A1).
- *Scope-note §5 progress:* step 2 (N1 map) and step 3 (text and §A5 propagation diffs) were done on 2026-09-24 and are revised here. **Step 4 is owed:** a separate-session refute-first review under D-codex (a), then a cross-vendor review before acceptance. Step 5 (acceptance) is the operator's.

**Open question for the operator (not adopted).** *Q5, correlation by exclusivity.* If the R5 inventory shows the account exclusive to this runtime (no copiers, managers, other platforms or manual sessions) and rule 10 holds, then an effect observed on a symbol could be attributed to the single unknown request on it. That would let such an effect **release** the reservation, amending rule 6 and §A7. It would recover room lost to transport failures. The risk is that one unrecorded actor makes the attribution wrong. Recommendation: decide only after the D1–D4 traces and the R5 inventory exist.

### A9 — Questions to resolve before acceptance (2026-09-26, Proposed)

**Status.** Option B stays the direction under development: the Q1 = B scoping ruling of 2026-09-24 still stands, and formal acceptance (scope §5 step 5) is withheld until each question below has a written answer in this addendum. This section adds no rule, figure or mapping. It is the operator's gate-B checklist for this amendment ([T09 gate row B](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#t09-gate-acceptance-record)). **Sources:** the operator's 2026-09-26 executive review of the Chief of Staff's gate analysis, and the code reads cited per question. Each question names what a sufficient answer looks like.

| # | Question | Why it is open | A sufficient answer |
|---|---|---|---|
| UB-1 | **Does rule 4 change normal-path admission?** | Rule 4 compares the new request's own worst case with the remaining room **even when nothing is held**. Today's admission has no room-to-floor check (`book_account_owner.py:1590-1622`; `book_policy.py` sizes by tier, not by room). So "with no held reservations the check is the existing admission unchanged" is true only if the check can never bind. Rule 9 widens this to the sum across a whole split intent. | Either (a) scope rules 4 and 9 to apply **only while at least one reservation is held**, keeping the normal path byte-identical, or (b) accept them as a new normal-path admission rule, which then enters the pre-registration and replay as an economic change. §A6's replay falsifier then tests whichever was chosen. |
| UB-2 | **What does the reservation actually bound?** | §A1 admits a residual: during the activation interval, or after a failed stop, exposure is bounded by the attended response, not by quantity × stop distance. So "worst case" is a conditional estimate, not an unconditional maximum. | A restated name and definition: the market and service-failure assumptions the figure covers, and which states it excludes. |
| UB-3 | **What happens while monitoring or operator response is unavailable?** | Rules 6 and 7 route failed or unexplained protection to attended intervention, but no rule covers attendance itself being absent. | For each state (unattended session, lost monitoring, failed-stop incident open): whether new risk-adds on any leg continue, pause or stop, and what evidence resumes them. |
| UB-4 | **What happens to a split intent that executes only partly?** | Rule 9 admits the whole intent; rule 10 sends its children one at a time. A refusal, timeout, takeover, flatten or session cutoff can stop a split midway. | Rules for: whether an unsent remainder is abandoned or continued; whether a conclusively refused child permits the next; when a base counts as established enough to permit an add (confirmed fills only, per VAN-6 and STR-4); and how takeover and flatten interrupt a split. These apply to normal replay, not only recovery. |
| UB-5 | **Are exits split too?** | §A1 scopes the one-contract rule to exposure-creating requests. §A8 then treats exit-side partial fills as moot, which assumes exits are also one contract each. A multi-order close can finish partly, race a protective fill, or leave sibling protection working. | A separate decision, with its own reason and evidence (D3 / L2(d)): either exits are one contract per request, with close ordering and orphan handling stated, or exits stay whole and exit-side partial fills are handled explicitly. |
| UB-6 | **When are the figures bound?** | §A3 binds the gap allowance, reserve margin and room definition at T16. Rules 4, 8 and 9 change admission, so a replay or E1 run made before T16 would qualify a different policy. | Before qualification: freeze the formula, its inputs, and a permitted envelope for the later-bound values. State the consequence of a value outside that envelope (requalify, or refuse to bind). |
| UB-7 | **What may resolve a correlated effect?** | Rule 6 and §A7 forbid releasing a reservation on an observed effect; Q5 (§A8) proposes correlation by exclusivity; REST gives a same-session positive recipe (REST assessment §6.4, accepted at Gate A as A1). | Which evidence releases a held reservation: a positive `clOrdId` lookup (and which facts it settles — Gate A A3(iii)), exclusivity under Q5, or neither. Cross-session behavior waits on the prior-session lookup read (REST D5). |
| UB-8 | **Is continuity after an unknown needed for the first attended release?** | Without B, one unresolved request that is never found ends automated trading on the account (scope §1; no negative closure, Gate A A1). With B, trading still stops after a few unknowns (rule 8). Neither posture has been sized against how often responses are actually lost. | An **availability assessment**: how many requests stay unresolved after reconciliation, including clustered outages (a vendor or session failure that hits several legs at once), and what each posture does to trading days under those scenarios. Data is sparse, so the result is scenarios with stated uncertainty, not a point failure-rate estimate. The operator then decides whether B's scope is needed for the first release. |

**Order.** UB-1, UB-4 and UB-5 are contract wording and can be answered now. UB-2, UB-3 and UB-6 need load-bearing-number and T13 inputs. UB-7 waits on the REST reads. UB-8 can run in parallel and may shrink the scope of everything else. The step-4 reviews (§A8) run after the answers are written, not before.

## Change history

| Date | Change | By |
|---|---|---|
| 2026-09-17 UTC | Record operator-directed incident amendment and conditional ATM/thin-bridge assessment | Joshua + Codex |
| 2026-09-24 UTC | Addendum (Proposed): bounded-exposure reservation for unknown narrowed-shape requests, after T08 R3 = NONE and the operator's Q1 = B ruling | Joshua (rulings) + Claude (text) |
| 2026-09-25 UTC | §A4 dated correction and §A8 revision (Proposed): whole book in the narrowed shape; rules 9–10; exit-side partials moot; open question Q5. Still Proposed; the step-4 reviews are owed | Joshua (rulings) + Claude (text) |
| 2026-09-26 UTC | §A9 (Proposed): eight questions (UB-1..UB-8) that must be answered before acceptance, including an availability assessment. B remains the direction; no rule, figure or mapping added | Joshua (review) + Claude (text) |
