# ADR — Bounded platform protection during signal/control incidents

**Trade-authority clarification (2026-10-01).** Categorical statements below that agents may not place trades, exit positions or cancel orders are **historical, superseded** by [ADR Addendum 2026-09-30b](2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-09-30b): Agents may place orders, exit positions and cancel orders only at the operator's direction for the specific act; `trade.submit` is an operator act at risk `high`, never grantable in a card. Arming, live-spend and per-session GO requirements are unchanged. This artifact grants no order action; its task-specific exclusions, named performers and separate drill approvals remain in force. It does not supply direction for a specific trade.

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
>
> *Pointer 2026-09-26 (callout above preserved):* by operator ruling, the first release runs today's preserve-and-block rule, not this reservation, for one attended session, then explicit review before extending ([§A11](#a11--operator-ruling-first-release-posture-2026-09-26)). Option B's implementation is deferred and the addendum stays Proposed.
>
> *Pointer 2026-10-01 (callouts above preserved):* a narrow first-release text is drafted as [§A12](#a12--first-release-text-narrow-2026-10-01--proposed) (PROPOSED, not accepted): an unknown request holds its reservation and halts trading; release only on a uniquely correlated outcome; §A2 rule 7 for non-entry requests. Option B's resume machinery is deferred, not deleted.

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
4. **Admission check (new, account-level).** A new risk-add is admitted only if the sum of all held worst cases plus the new request's own worst case stays within the account's room to the venue drawdown floor, less the reserve margin. This is an admission gate in the account owner. It is **not** an input to `dd_protection` and never alters the protection rule's equity, trigger or scale. With no held reservations the check is the existing admission unchanged, so the qualified normal path is unaffected. (To verify at implementation: a replay with no unknowns produces byte-identical admission decisions.) *[Qualified 2026-09-26, Proposed: replaced by §A10 rules 4′ and 4a–4c (exceptional-mode scope, account-wide check); UB-2 reads "worst-case" as a conditional loss allowance.]*
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

*[Qualified 2026-09-26, Proposed: capacity versus loss-allowance scope set by §A10 rule 9′.]* **Rule 9 (proposed): split intents are admitted whole or not at all.** A multi-contract intent (Striker up to its maximum setting, Aegis up to its captured size, Vanguard base plus adds) is admitted only if rule 4 admits the **sum** of its one-contract worst cases on top of every held reservation, checked before the first request is sent. Otherwise the whole intent is refused. Admission never sends a partial intent. After sending, confirmed fills are the leg's position; a refused request is not re-sent; an unknown one holds its own reservation (rule 1). This matches pre-registration STR-4.

**Rule 10 (proposed): one unresolved request per symbol.** The next one-contract request of a split, or any new exposure-creating request on that symbol, is sent only after the previous one on that symbol is acknowledged or refused. One transport failure can therefore create at most **one** held reservation per symbol, not N. *Tradeoff, stated rather than hidden:* a split of N now takes N sequential acknowledgement round trips, so later contracts can fill at worse prices. The pre-registration's §6 replay-modelling choice must price that latency before freeze. Without rule 10, a single failed 30-contract Striker split could hold 30 reservations and reach rule 8 exhaustion in one event.

**Facts recorded.**
- *Exit-side partial fills (T08 residual row):* moot by construction. Under the one-contract rule an exit is for one contract and cannot partially fill. *[Withdrawn pending UB-5, §A9.1, 2026-09-26, Proposed.]*
- *§A1 admission-precondition trace:* the planned source is drill D1 of the [2026-09-25 operator session plan](../notes/2026-09-25-t08-drills-t07-reads-operator-session.md), authorized in principle by the operator on 2026-09-25 and performed by Joshua. Until that trace is retained and recorded in CAP, this addendum still grants nothing (§A1). *[Qualified 2026-09-26 by [§A11.1](#a111--operator-ruling-close-direction-2026-09-26) item 6: D1 is not treated as cleared for execution; it returns as an individual decision.]*
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
| UB-8 | **Is continuity after an unknown needed for the first attended release?** | Without B, one unresolved request that is never found ends automated trading on the account (scope §1; no negative closure, Gate A A1). With B, rule 8 stops risk-adds when held allowances exhaust the room; how many unknowns that takes is not established until the allowance, account state and capacity limits are specified. Neither posture has been sized against how often responses are actually lost. | An **availability assessment**: how many requests stay unresolved after reconciliation, including clustered outages (a vendor or session failure that hits several legs at once), and what each posture does to trading days under those scenarios. Data is sparse, so the result is scenarios with stated uncertainty, not a point failure-rate estimate. The operator then decides whether B's scope is needed for the first release. |

**Order** (*corrected 2026-09-26 by §A9.1; original text: "UB-1, UB-4 and UB-5 are contract wording and can be answered now. UB-2, UB-3 and UB-6 need load-bearing-number and T13 inputs."*). UB-1 and UB-3's policy can be settled now. UB-2 and UB-6 can be defined now; their figures come later. UB-4 freezes with the editions. UB-5 and UB-7 resolve through gate C evidence. UB-8 runs in parallel and may shrink the scope of everything else. The step-4 reviews (§A8) run after the answers are written, not before.

#### A9.1 — Recommended answers (2026-09-26, Proposed)

**Status.** These are recommended answers from the operator-directed executive review of this section at `deb8144`, with coordinator adjustments marked *(adj.)*. The operator directed that they be written here as scoped. They remain **Proposed**, like the rest of this addendum. Nothing below is accepted, effective or propagated, and gates B–D stay pending. Each answer carries one tag:

- **POLICY:** the direction can be settled now; wording is final pending acceptance.
- **DEFINITION:** the concept is fixed now; figures, thresholds and envelopes come later.
- **FREEZE WITH EDITIONS:** the rule is set by the edition pre-registrations and replay, not by this ADR alone.
- **EVIDENCE-PENDING:** the principle is set now; route capability decides the mechanism.

**Operator ruling (2026-09-26, in session):** the four POLICY rows (UB-1, UB-3, UB-8, UB-9) are ruled as written, including their *(adj.)* notes. The DEFINITION, FREEZE WITH EDITIONS and EVIDENCE-PENDING rows remain recommendations pending their inputs. The ruled rows are direction for the contract text: they are not effective until they are written into §A2/§A8 as rules, reviewed (§A8 step 4) and the addendum is accepted.

**Scope of B.** B stays narrowly scoped to operating *with unresolved exposure-creating requests*. Ordinary admission with none outstanding is unchanged. Formal acceptance of B follows the completed account-wide loss model (UB-1), the UB-8 assessment and the §A8 step-4 reviews.

| # | Tag | Recommended answer |
|---|---|---|
| UB-1 | POLICY — **RULED 2026-09-26** | **Choose (a).** The additional loss-room check applies only while at least one exposure-creating request has an unresolved outcome ("exceptional mode"); ordinary capacity reservations alone do not activate it. Whole-intent **capacity** reservation applies to every split in every mode; the whole-split **loss allowance** applies only in exceptional mode. Consequences, stated rather than hidden: (i) the first unknown can arise from a normally admitted request, so B cannot promise room to continue afterward: on entering exceptional mode it evaluates the resulting state and stops further admissions if the room is insufficient; (ii) clearing the final unknown must atomically transfer any discovered exposure into confirmed accounting before normal admission resumes. **Account-wide loss model:** the check must count the remaining loss exposure of existing positions and acknowledged working entries alongside held unknowns and the new request, without double-counting losses already reflected in equity. *(adj.)* This model is new engineering in the account owner, not a formula change, which is why UB-8 runs before its full implementation is committed. |
| UB-2 | DEFINITION | The reservation is a **conservative admission allowance** under explicitly stated execution, market and response assumptions. **It does not guarantee a maximum realized loss.** Three separate quantities: (1) *contract capacity*, the contracts potentially committed by the unknown; (2) *conditional loss allowance*, the amount charged when considering further admissions; (3) *incident state*, the circumstances in which that allowance no longer supports continued admission. Stop activation, slippage, fees, delayed execution and protection failure are each either covered by a stated assumption or trigger the incident state. Because a reservation can survive across sessions, the specification states when its reference price and allowance are recalculated, when their inputs become stale, and that stale inputs stop continued admission. Figures and the demonstrated operating envelope come later (UB-6). |
| UB-3 | POLICY — **RULED 2026-09-26** (thresholds later) | For the first attended release: **required monitoring or broker evidence unavailable or stale:** stop new risk-adds on all legs. **Failed stop activation or unexplained exposure open:** stop new risk-adds on all legs and invoke the attended incident procedure (§2 row). **Monitoring restored:** reconcile first; restoration alone does not resume trading. Resume requires fresh account, order and protection reconciliation, restored monitoring and attendance, and the applicable authorization. Stopping admissions never means blindly cancelling qualified resting protection or automatically flattening through an uncertain route; risk-reducing actions follow their separately accepted procedure. *(adj.)* **No confirmed attendance at session start, so no risk-adds** applies to all trading, not only to B, so it belongs to the attended-operations contract ([checklist T13](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#t13--attended-operations-and-recovery-implemented-750k1m)); B cites it rather than owning it. Detection thresholds and response evidence are bound later. |
| UB-4 | FREEZE WITH EDITIONS | First-release rule: reserve the full intent before its first child. Send the next child only after the previous one meets an explicitly defined acknowledgment condition. On a conclusive refusal, unknown outcome, cutoff, takeover or flatten, **abandon the unsent remainder** of that intent. Never retry an unknown child or top up a short fill under a fresh identity. Release only reservations demonstrably belonging to unsent or conclusively closed children. Keep managing every submitted child and confirmed fill. A base becomes eligible for add logic only after its submission sequence is closed and its resulting state satisfies the approved strategy rule; acknowledgment alone is insufficient. Whether a partly filled base may support adds is frozen in each edition contract and its replay. *(adj.)* Abandoning a remainder changes strategy behavior: the declared strategies send the full quantity. So this rule must enter the Striker and Vanguard (and Aegis, where it splits) pre-registrations and be replayed; stating it here does not qualify it. |
| UB-5 | EVIDENCE-PENDING | One-contract exits are **not** imposed merely because entries are split: the entry rule addresses first-fill protection, not the exit mechanism. Principle: **preserve the intended exit scope, and use the simplest qualified closing primitive that closes that scope and resolves its protection without touching other owned exposure.** Whole-leg or full-symbol exits: assess a qualified full close. Subset exits: require explicit attribution, protection adjustment and race handling. Native one-contract protective exits keep their own order ownership. Exit-side partial completion is **not** moot: sequential one-contract closes can still leave an intent partly closed. §A8's "moot by construction" fact is therefore withdrawn, pending this answer. The primitive choice waits for gate C (D3 / L2(d)). |
| UB-6 | DEFINITION | Freeze the formula, input definitions, stale-data behavior, calibration method and every decision-bearing constant **before production qualification**. T16 binds identities and current observations *through* that frozen rule. A later-binding envelope is acceptable only if qualification covers the envelope, or a justified invariance argument does. Stating a range is not enough, and "more conservative" is not automatically equivalent, because refusing more trades changes performance and interaction. A value outside the qualified envelope refuses binding pending an explicit requalification decision. |
| UB-7 | EVIDENCE-PENDING | Resolve through **uniquely correlated, accepted broker evidence**. Resolution is usually a *transfer*, not a release to zero: a correlated working entry becomes a known working-order reservation; a correlated fill becomes confirmed exposure plus its protection obligations; an accepted terminal outcome releases only the conclusively unfilled remainder; an entry that is identified but whose child effects are unresolved keeps the remaining uncertainty. Q5's "only possible actor" attribution (§A8) is **not** adopted initially: an actor inventory does not exclude delayed repair, prior-session activity or an overlooked operation. The REST reads (Gate A drill map) establish which cases the route supports. |
| UB-8 | POLICY — **RULED 2026-09-26** (assessment first) | Keep B as the development direction, but make it **mandatory for the first release only if this assessment shows useful continuity under credible scenarios**, not merely that B can sometimes admit another order. Scenarios: no unresolved requests; one unknown that stays unresolved; several symbols hit by one outage; an unknown just before session reset; a partial split followed by lost monitoring; repeated unknowns across days. Compare: trading opportunities lost under preserve-and-block; additional opportunities B admits; reservation accumulation and exhaustion; operator interventions and unresolved obligations; implementation and verification work required. |
| UB-9 | POLICY — **RULED 2026-09-26** (new) | **Re-evaluation between admissions.** Passing the exceptional-mode check once does not keep it valid as prices, working orders, equity and evidence freshness change. The specification names the events that revoke permission for further risk-adds (at minimum: any new unknown, a fill or terminal on an owned order, an equity update, and evidence staleness under UB-2/UB-3) and requires the check to be re-run before the next admission. |
| UB-10 | DEFINITION (new) | **One obligation record per child request.** Every child request carries exactly one of: unsent, submitted-unknown, acknowledged-working, filled, protection-unresolved, terminal. UB-4 and UB-7 transitions act on that record only, so a reservation cannot be freed twice. *(adj.)* This extends the account owner's existing attempt journal (`book_account_owner.py:764`, `:791`, `:1674`: `UNKNOWN`, `REJECTED` and accepted terminals), so that one record owns each reservation. It is not a parallel ledger, which would create the double-release risk this row exists to prevent. |

**Withdrawn or qualified by this subsection (Proposed, pending acceptance):** §A2 rule 4's sentence "With no held reservations the check is the existing admission unchanged" (superseded by UB-1's exceptional-mode scope); §A2's "worst-case" wording (read as UB-2's conditional loss allowance); §A8's exit-side partial fills "moot by construction" (UB-5); and §A8 rule 9's application of the loss check to every split (UB-1: loss allowance only in exceptional mode). The original text above is preserved.

### A10 — Contract text for the ruled policy rows (2026-09-26, Proposed)

**Status.** This section turns the four POLICY rows ruled on 2026-09-26 (§A9.1: UB-1, UB-3, UB-8, UB-9) into rule text. It is **Proposed** like the rest of this addendum: nothing here is effective until the §A8 step-4 reviews are done, the operator accepts the addendum and §A5 propagation is applied. Where a rule below conflicts with §A2 or §A8, this section governs, and the original text above stays preserved. Details that depend on the capability allocation map ([handoff](../briefs/handoffs/2026-09-25-tradeify-capability-allocation-deletion-map.md), in progress) or on unruled rows are marked **OPEN** and are not decided here.

*Pointer, 2026-09-26 (status text above preserved):* the allocation map has returned ([PR #516](https://github.com/Joshua-Asante/first-passage/pull/516), `docs/notes/2026-09-25-tradeify-capability-allocation-deletion-map.md`, draft; not gate-D acceptance). Its row C06b, marked provisional on B, proposes local ownership of the rule 4a account-wide loss check (decision and recovery local, no vendor execution) as new engineering. Its item B16 (the option-B machinery) is deferred with B, which §A11 leaves unbuilt for the first release. Nothing is ruled by this pointer; rule 4a's OPEN item stands.

**Rule 4′ (replaces rule 4): exceptional mode.** The account is in *exceptional mode* while at least one narrowed-shape exposure-creating request has an unresolved outcome. That is, an attempt in the account owner's fence (today `_ordinary_unknown_orders_db`, `ops/c1_rail/book_account_owner.py:768`) that no accepted terminal resolves. Ordinary capacity reservations alone do not create exceptional mode. **Outside exceptional mode, admission is today's admission, unchanged**, and §A6's no-unknowns replay falsifier tests exactly that. In exceptional mode, a new risk-add, or a whole split intent under rule 9′, is admitted only if rule 4a passes.

**Rule 4a: account-wide loss check.** The room to the venue drawdown floor, less the reserve margin, must be at least the sum of three amounts:
- the conditional loss allowances of all held unknowns (UB-2);
- the remaining loss exposure of existing positions and acknowledged working entries to their protective stops, not double-counting losses already reflected in equity;
- the allowance of the new request or whole split intent.

The floor definition, allowance formula, inputs, stale-data behavior and calibration are frozen before production qualification (UB-6; **OPEN** until defined). **OPEN:** which component computes this check and from which observations. That is assigned by the allocation map and then ruled; this rule fixes what is checked, not where.

**Rule 4b: entering exceptional mode.** The first unknown can come from a normally admitted request, so B promises no room to continue. On entering exceptional mode, rule 4a is evaluated on the resulting state before any further admission. If it fails, no further risk-add is admitted (rule 8).

**Rule 4c: leaving exceptional mode.** When the last unknown is resolved (under rule 2), any exposure its resolution reveals is transferred into confirmed accounting (position, working order and protection obligations). That transfer happens atomically with the exit from exceptional mode, and before ordinary admission resumes. **OPEN:** which evidence may resolve an unknown and what each resolution transfers (UB-7, evidence-pending).

**Rule 9′ (qualifies rule 9).** Whole-intent **capacity** reservation applies to every split intent in every mode. The whole-intent **loss allowance** under rule 4a applies only in exceptional mode. **OPEN:** partial-split execution: remainder abandonment, acknowledgment condition, base eligibility for adds (UB-4; frozen with the editions).

*Pointer 2026-09-26 (rule text above preserved):* [campaign §59 Ruling 5](../briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#ruling-5--edition-directions-2026-09-26) records the operator's constraint for preparing the editions' splits: whole-intent capacity reservation, sequential submission, and abandonment of the unsent remainder on an exceptional outcome. It is a preparation constraint, not rule text. This OPEN item stays until the editions freeze; the acknowledgment condition and base eligibility for adds are not ruled.

**Rule 11: stopping and resuming risk-adds when B's assumptions fail (account-wide).**
1. If required monitoring or broker evidence is unavailable or stale, no new risk-add is admitted on any leg.
2. If a failed stop activation or unexplained exposure is open, no new risk-add is admitted on any leg, and the §2 protection/state-failure row applies (attended incident procedure).
3. Restoring monitoring or evidence does not by itself resume admission. Resumption requires three things: a fresh reconciliation of account, orders and protection; restored monitoring and attendance; and the applicable authorization.
4. Stopping admissions never cancels qualified resting protection and never flattens automatically through an uncertain route. Risk-reducing actions follow their separately accepted procedure.
5. Attendance at session start is governed by the attended-operations contract (checklist T13), which this rule cites and does not define.

**OPEN:** the list of "required" monitoring and evidence, and the staleness thresholds (bound per UB-6).

**Rule 12: re-evaluation between admissions.** In exceptional mode, permission for further risk-adds lapses on any of: a new unknown; a fill or terminal on an owned order; an equity update; or any rule 4a input becoming stale. Rule 4a is re-run before the next admission. **OPEN:** whether ordering and freshness of these events can come from a vendor stream or must be polled (allocation map; Gate A A7).

**Acceptance condition (UB-8).** This addendum is accepted as a **mandatory first-release** contract only if the UB-8 availability assessment shows useful continuity under credible scenarios. If it does not, the first release runs under today's preserve-and-block rule, and this addendum stays Proposed for a later release.

*Pointer 2026-09-26 ([§A11](#a11--operator-ruling-first-release-posture-2026-09-26), operator ruling; condition text above preserved):* the first release runs preserve-and-block for one attended session, then explicit review before extending; option B's implementation is deferred and this addendum stays Proposed. That takes this condition's non-mandatory branch for the first release. The ruling itself states no finding on the UB-8 assessment; the determination that UB-8 has not shown useful continuity for the first release under credible scenarios is the B–D decision packet's recommendation (PR #518), noted under §A11's basis as drafted.

**Still open elsewhere in §A9.1:** UB-2 (figures), UB-4 (with the editions), UB-5 and UB-7 (gate C evidence), UB-6 (calibration), UB-10 (obligation states in the attempt journal).

### A11 — Operator ruling: first-release posture (2026-09-26)

**Operator ruling 2026-09-26.** Source: operator ruling and coordination, 2026-09-26, relayed in session, together with the operator's structured-question answers the same day (for this item, "Preserve-and-block, accept suspension"). The operator approved the recommended overall ruling in writing; its text governs and supersedes the earlier shorthand recording of those answers. Recorded as operator decisions:

1. **Posture.** The first release adopts preserve-and-block, today's rule, for **one attended session**, followed by **explicit review before extension**. Under that rule an unresolved request halts automated trading on this account ([halt/resume contract](../spec/2026-09-14-tb-s3-halt-resume-contract.md) §2–§4); the owner's risk-add fence (`book_account_owner.py:1608`, `unknown_order`) is the part implemented today.
2. **Consequence accepted.** The operator accepts that one unresolved request may suspend automation on this account indefinitely. **No acknowledgment, reset or elapsed time resolves that obligation.**
3. **Option B deferred.** Option B's implementation is deferred. B is retained as **Proposed** and is not built for the first release; it remains the development direction for a later release (§A9.1, UB-8 row). By adopting preserve-and-block for the first release and deferring B, the ruling takes §A10's non-mandatory branch for the first release (§A10, dated pointer); the ruling itself states no finding on the UB-8 assessment (the packet's recommended determination is under *Basis as drafted* below).
4. **Manual intervention.** Manual intervention remains available, **subject to fencing, outcome evidence and reconciliation**. This replaces the unconditional "manual trading is unaffected" wording ([scope note](../superpowers/specs/2026-09-24-bounded-exposure-unknown-request-amendment-scope.md) §1, dated pointer). Where the recorded contracts already carry these requirements: during intervention, runtime mutations are fenced, and no claim that manual action is race-free is allowed without evidence ([halt/resume contract](../spec/2026-09-14-tb-s3-halt-resume-contract.md) §1); recovery completes only on fresh coherent evidence covering operator actions (§3); resumption needs a new operator resume (§4). How operator-placed preservation trades on the book's own symbols are treated stays **OPEN** (route drill-plan draft §0.1 and open question 9, [PR #518](https://github.com/Joshua-Asante/first-passage/pull/518), `docs/notes/2026-09-26-tradeify-route-drill-plan-draft.md`).

**Basis as drafted (not part of the ruling).** The B–D decision packet §3 and the UB-8 comparison's coordinator correction 2 (both drafts, PR #518) recommend the §A10 determination that the UB-8 assessment has not shown useful continuity for the first release under credible scenarios, because UB-8's conditions C2–C4 are unevidenced. The written ruling does not itself state that determination, and it is not recorded here as an operator decision.

**What this ruling does not do.** It does not make §A10 effective: §A10's rules concern option B, and this addendum as a whole stays Proposed under the §2 effectiveness gate. The §A8 step-4 reviews and formal acceptance remain owed before any later release uses B. Gate A stays accepted. Acceptance of gates B, C and D, qualification S5 release, order-producing drills, production qualification, deployment and arming remain subject to their recorded gates. It accepts no close guarantee or residual risk and grants no T09 dispatch or spend.

#### A11.1 — Operator ruling: close direction (2026-09-26)

**Operator ruling 2026-09-26.** Source as §A11 (for this item the structured answer was "Record as Astra recommends", ruling R-CLOSE in the B–D decision packet, draft, [PR #518](https://github.com/Joshua-Asante/first-passage/pull/518), `docs/notes/2026-09-26-tradeify-bd-decision-packet.md`). The written ruling governs; it covers the close contract, reads and drills. Recorded as operator decisions:

1. **Close direction: investigation only.** C-a, whole-leg broker liquidation, is pursued as the **first candidate to investigate**. This approves investigation only: **neither the close-contract amendment** (the packet's §1.1a outline, elements (a)–(e), whose OPEN items stand) **nor an unspecified residual risk is accepted.**
2. **What the investigation must establish.** Authoritative semantics for protection during liquidation, partial or rejected outcomes, protective-fill races, reversal prevention and completion evidence. Unresolved risks are returned precisely. **A contradicting trace stops C-a.**
3. **C-b.** C-b (exit through each lot's own OCO) requires its own operator expression decision and qualification. It is never automatic.
4. **Reads.** Operator-performed REST reads **R-1** (same-session reconciliation of a known order) and **R-2** (prior-session lifecycle lookup of a known order) **only**, within the route drill-plan draft's exact read-only scope and after the existing CrossTrade REST entitlement is confirmed. **No purchase, new access, route change or order mutation is authorized.** The draft's own preconditions apply, including the operator's confirmation of its known-order definition before the first read; that is the draft's scope, not an addition to the ruling. The drill plan records the read authorization and its scope in its operator-ruling section ([PR #518](https://github.com/Joshua-Asante/first-passage/pull/518), `docs/notes/2026-09-26-tradeify-route-drill-plan-draft.md`).
5. **Drills.** Normal-case drill decisions are prepared individually after their documentary prerequisites are met. Each returns with its exact environment, actions, exposure limits and abort/recovery procedure before execution approval is requested. The deliberate protective-fill race drill is deferred. There is no automatic fallback to the live evaluation environment. No order-producing drill is authorized.
6. **Webhook-form drills D1–D4 of 2026-09-25.** The operator authorized the [session plan](../notes/2026-09-25-t08-drills-t07-reads-operator-session.md)'s webhook-form drills D1–D4 in principle on 2026-09-25 (its §0). This ruling authorizes R-1 and R-2 only, authorizes no order mutation, and requires normal-case drill decisions to be prepared individually and approved for execution. D1–D4 are therefore **not treated as cleared for execution**; each returns as an individual decision. The 2026-09-25 authorization is not recorded as formally revoked: it is superseded in practice by the requirement for individual decisions.
7. **Performer.** R-1 and R-2 are operator-performed. No agent places, amends or cancels an order (AGENTS.md live-execution posture); that is standing posture, not an addition by this ruling.

**Relation to this addendum.** C-a concerns whole-leg exits only. The editions are prepared under the constraint that a subset exit is never widened into whole-leg liquidation ([campaign §59 Ruling 5](../briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#ruling-5--edition-directions-2026-09-26)). UB-5 (§A9.1) stays a recommendation, EVIDENCE-PENDING: this ruling names the candidate to investigate and qualifies no closing primitive.

**What this ruling does not do.** It adopts no close-contract amendment and changes no rail-spec text. It accepts no close guarantee or residual risk, and grants no gate B, C or D acceptance, order-producing drill, T09 dispatch, deployment, arming or spend.

#### A11.2 — Operator ruling: no same-session restart of automation after an incident (2026-09-27)

**Operator ruling 2026-09-27, in session.** The operator adopted this ruling by structured answer ("No same-session restart") to the text relayed the same day; the relayed text governs: "For commissioning and the first attended release, no same-session restart of automation after an incident; recovery and evidence collection continue, followed by review." Its detail, verbatim:
- "during commissioning and the first attended release, an incident ends automated trading for that session. Continue operator recovery and evidence collection; review before another session."
- "This applies to incidents—not ordinary, correctly handled signal or capacity refusals."

**Relation to existing text.** This is a **new** ruling. Halt/resume rev9 §4 permits conditional same-session resumption with operator approval ([contract](../spec/2026-09-14-tb-s3-halt-resume-contract.md) §4). For commissioning and the first attended release, this ruling narrows that permission to none. §A11 items 1, 2 and 4 are unchanged: one attended session, then explicit review before extension; no acknowledgment, reset or elapsed time resolves an unresolved request; manual intervention is subject to fencing, outcome evidence and reconciliation. The Phase 5 plan's "no same-account-session reactivation" was PROPOSED; for these two contexts this ruling now decides the question. Its scope for later releases is not ruled. The halt/resume owner text is amended by [handoff H5](../briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md) step (a).

**Not granted:** any session, drill, arm, deployment or GO. The addendum stays Proposed.

**Operator clarifications, 2026-09-27 (same day, in session, by structured answer to the coordinator's questions on the H5 step (a) return).**
- **A deliberate operator stop (O-6).** A deliberate operator stop with no fault is an incident for this ruling. It ends automated trading for that session, and review follows before another session. The operator chose "Yes, it ends the session".
- **Scope of "commissioning" (O-7).** The ruling covers the first attended release and **any commissioning session in which automation is armed**. None is defined today. The operator chose "Cover any armed commissioning". Operator-run commissioning sessions with automation disarmed follow the commissioning packet's own stop rule.

#### A11.3 — Operator ruling: preservation-trade evidence as the target of authorized reads (2026-09-27)

**Operator ruling 2026-09-27, in session.** The operator adopted this ruling by structured answer ("Preservation-trade reads") to the text relayed the same day; the relayed text governs: "Approve reuse of preservation-trade evidence for the authorized reads where its scope and timing qualify, after entitlement and target confirmation. No additional trade is authorized." Its detail, verbatim:
- "an already completed operator-placed preservation trade may be the R-2 and settlement-read target where it meets the required evidence conditions. R-1 must observe a trade in the same session; use a preservation trade you place anyway."
- "Entitlement and transaction identity still need confirmation. This authorizes no new trade, purchase or account reset."

**Scope.**
- The ruling changes the **target** of reads already authorized: R-1/R-2 (§A11.1 item 4) and T07 R1–R3 (2026-09-25). It adds no read.
- The drill plan's ruling block carries the same record. §A11.1's "single owner OPEN" rule applies, so the two texts must agree.
- It does not settle how preservation trades on the book's own symbols are treated in operation (drill plan open question 9; §A11 item 4).

**Not granted:** a new trade, purchase, new access, account reset or order mutation; no agent account access.

### A12 — First-release text (narrow), 2026-10-01 — PROPOSED

**Status.** `PROPOSED`. Drafted for the operator's 2026-10-01 ruling "go with all six recommended cuts", item 1, recorded in the deployment-checklist addendum "Addendum 2026-10-01 — first-session simplification rulings (six cuts)" ([PR #580](https://github.com/Joshua-Asante/first-passage/pull/580)). **Nothing here is effective until Joshua accepts it** (scope §5 step 5), after the two step-4 reviews of this narrow text (§A12.7). Until then the accepted contracts govern unchanged.

**Scope.** First release only: the first attended release (§A11 item 1), meaning one attended session followed by explicit review. §A11.2's O-7 extends only the no-same-session-restart ruling to armed commissioning; it does not extend this amendment. So in any armed commissioning session, the accepted halt/resume contract (including §4.1) governs unchanged, and §A12 does not apply. Applying §A12 there needs an explicit operator ruling (D8). *(Revised 2026-10-01 on Codex review of #584 at `a77ae73`.)* For that scope, where §A12 differs from §A2, §A8, §A9 or §A10, §A12 governs. §A9 withholds formal acceptance until each UB question has a written answer in this addendum. Several §A12.3 dispositions are not answers. Among them: UB-3 as amendment text is UNRULED, UB-4 freezes with the editions, UB-5 is EVIDENCE-PENDING and UB-7 waits on D2. **§A12 does not count any disposition as an answer.** Acceptance therefore needs one of two things (D7):
- §A9 satisfied on its own terms, meaning a written answer for **every** UB row it lists (UB-1 to UB-10); or
- Joshua's explicit approval of the §A12.3 disposition as the first-release replacement for §A9's gate.

While any UB row lacks a written answer, only the second branch is available. Without one of them, §A9 stands and blocks D1. *(Revised 2026-10-01 on Codex review of #584 at `373a103`: the first branch had listed only UB-3, UB-4 and UB-7 and omitted UB-5.)* For any later release that adopts B, §A9 stands unchanged. *(Revised 2026-10-01 on Codex's second pass of #584 at `e5e1397`.)* *(Revised 2026-10-01 on the refute-first review of #584, P2-3.)* Their text stays preserved and is the starting point for any later release that adopts option B. Each deferred rule is **deferred, not deleted** (§A12.3).

**Relation to the accepted contracts.** On this section's reading, every first-release rule below is already carried by an accepted owner:
- the [halt/resume contract](../spec/2026-09-14-tb-s3-halt-resume-contract.md) rev9 with its 2026-09-27 amendment (§1–§4, §4.1);
- the rail spec's **unamended** E3 row with its §59 Ruling 7(b) marker ([rail spec](../spec/2026-09-12-c1-multi-leg-rail-extension-spec.md) §1 `pending` row and §2e E3);
- the closure plan's Step 2 outcome table ([closure plan](../superpowers/plans/2026-09-16-self-service-capability-closure.md)).

What §A12 adds is the first-release meaning of this ADR's own §2 row "Unknown entry, add, cancel, close or modification", a per-type statement for non-entry requests (scope Q2), and an explicit record of what is deferred. It changes no accepted contract and decides no item an accepted owner leaves OPEN. If that reading is wrong anywhere, the review should report it as a finding; this section does not silently change the owner.

#### A12.1 — Rules

**F1. An unknown request holds its reservation, and trading halts.** A runtime request of any type or shape has an *unknown outcome* once an accepted owner's trigger fires and no accepted outcome covers the request. The triggers are:
- the rail spec §1 `pending` row's one-bar outcome timeout;
- a crash between send and outcome (same row);
- an unknown transport result, or a send exception caught after transport may have started (the CC-3 record, halt/resume §4.1).

A request still inside its outcome window is pending, not unknown. *(Revised 2026-10-01 on the refute-first review of #584, P3-1.)* A request **whose outcome has become unknown** is an incident; a pending request is not (halt/resume §2, row "uncertain transport/order outcome"; "Unknown order identity is an incident"; §4.1). Then:
- (a) **Ownership is retained.** The original attempt, its identity and its contracts stay owned as today. There is no resend and no speculative cancel, amend or repair. Absence, flatness, empty reads, elapsed time, a session reset, a restart and operator acknowledgment release nothing (§A2 rule 1; scope §4). Rail spec S4 says "the cancel is still sent" for a resting entry whose `pending` state is `UNKNOWN`. That is incident-time runtime dispatch, which rev9 supersedes: incidents revoke all runtime mutation authority (the rail spec's "Current attended amendment — rev9" callout; halt/resume §1). So under F1(c) no runtime cancel is sent, and the operator handles the resting entry in attended recovery (§3).
- (b) **The reservation is held.** For an exposure-creating request, its contracts stay in `reserved` for its leg's symbol (§A2 rule 5). For a request on an existing position or order, that position's lots and that order's reservation stay owned exactly as they were before the request was sent. It is the request's **worst-case reservation** (T08 §7.10), and it has two parts. The first is that contract capacity. The second, for an exposure-creating request, is its §A2 rule 3 charge, held as its retained inputs: quantity, intended entry or reference price, attached stop, and point value. The charge's value needs the §A3 gap allowance, which the 2026-10-01 ruling defers. Until that allowance is bound, the charge is **unbound**. No rule may read an unbound charge as zero, as released, or as room (§A12.2).
- (c) **The account halts.** The account enters durable HALTED with account-wide intervention scope. INTERVENTION permits no new runtime broker mutation: no exits, amendments, emergency cancel or close, and no scheduled flatten (halt/resume §1). An alert goes out for attended intervention (§3). In the first attended release, automated trading ends for that session. §A11.2 says the same for armed commissioning, which §A12 does not otherwise govern (Scope). No resume request and no repeated activation is valid in it (§A11.2; halt/resume §4 marker).
- (d) **Every shape.** F1 applies to every request type and shape. The §A1 narrowed shape changes nothing in the first-release response.

**F2. Release only on a uniquely correlated outcome.** A held request is released only by evidence in the first two rows of the closure plan's Step 2 outcome table: a uniquely correlated accepted request, order or execution, or a supported definitive terminal rejection or no-future-effect result for that attempt (§A2 rule 2(a)). Release is a **transfer, not a write-off** (E3: "Completion hands responsibility to observed working orders, gross lots or quarantine before releasing the request owner"; §A9.1 UB-7):
- a correlated working order becomes a known working order that keeps its capacity reservation (rail spec §1 `pending` row marker (1)). For an **unknown** dispatch, marker (3) governs instead: such an order becomes known working only when an evidence class that admits it is accepted (D2). Under the terminal-only class, an unknown dispatch is released only by a covering terminal. *(Revised 2026-10-01 on the refute-first review of #584, P1-1.)*
- a correlated fill becomes confirmed exposure, with its protection obligations;
- an accepted terminal outcome releases only the conclusively unfilled remainder of that request (UB-7; rail spec §1 `pending` row marker (4));
- the request stays unresolved while any child, sibling or coverage-repair effect is unexplained, or while the position does not reconcile with the correlated order, its children and its fills (T08 §7.10; Gate A A3(iii)).

A collision, a duplicate `clOrdId` match or a contradictory identity is quarantined through the existing owner (closure row 4). Absence never releases (closure row 3). Option A's vendor-time release (§A2 rule 2(b)) is unavailable on the supplied support reply (T08 §7.9) and is not part of the first release.

*Evidence classes in the first release.* There are two places where a request can be released, and they differ:
- **Runtime classifier (T09).** Against the unamended E3, T09 implements one release class: the conservative terminal-resolution rule, meaning an accepted postdating terminal that demonstrably covers the request (rail spec §1 `pending` row marker (3)). §59 Ruling 7(b)(3) holds positive-lookup resolution "for this slice", and that hold stays. A runtime release changes bookkeeping only: "later or attached facts settle the order but do not restore authority" (CC-3 record, halt/resume §4.1), and §A11.2 permits no same-session restart.
- **Attended recovery (halt/resume §3).** The accepted owners already release on unique correlation here. Closure row 1 says "transfer to identified order … before releasing", and E3 says "Completion hands responsibility to observed working orders, gross lots or quarantine". The release class is whatever an **accepted E3 producer** can establish, subject to Gate A A3(iii). The binding constraint is halt/resume §4 ¶2: "No production resume implementation is released until a named accepted producer supplies each retained E1/E2/E3 fact". That is already a live-release precondition. A positive `clOrdId` lookup by the REST recipe ([REST §6.4](../briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md#64-correlation-and-recovery-step-3)), which T08 §7.10 names, is a candidate for that producer once UB-7's evidence is accepted. Whether §59 Ruling 7(b)(3) is also meant to reach attended recovery is the one question left for the operator (D2, §A12.5).

*(Revised 2026-10-01 on the refute-first review of #584, P2-1.)*

**F3. Duration.** While a request is held, attended recovery cannot complete: halt/resume §3 ¶2 requires "no unresolved requests". No later session may resume or activate either: §4 ¶1 says "unresolved owner cannot be overridden". F2's evidence ends only the request's ownership block, by transfer. It **never ends the halt by itself**. HALTED persists until three things hold:
- halt/resume §3 recovery completes on fresh coherent evidence: positions, working orders, protection and every remaining request reconciled;
- in the first-release scope, no same-session restart (§A11.2);
- any later session is activated by a new, valid operator action under §4 and its deployment gates.

After this incident halt, refreshed evidence never automatically restores permission (rail spec §1 `pending` row marker (5)). That marker does not reach stale evidence without an incident, which is a refusal (§A12.5, stale-evidence row). Automation can therefore stay suspended indefinitely, at least until F2's evidence arrives. The operator accepted that consequence on 2026-09-26 (§A11 item 2). *(Revised 2026-10-01 on Codex review of #584 (P1). The first draft said suspension lasted "until F2's evidence arrives".)*

*Watching a held request.* T08 §7.9 gives no time after which a request can no longer act, so a held request may still fill, rest or trigger repair after the attended session ends. While any request is held, a check for unexplained effects stays an obligation of attended operations: at each session open, or at another cadence that owner names. Disarm does not satisfy it. The owner is the attended-operations contract (checklist T13), with the channels under D-MON (§A12.5). §A12 does not read halt/resume §3's "Attendance continues until reconciled/disarmed" as ending this watch, and it defines no cadence. *(Revised 2026-10-01 on the refute-first review of #584, P2-2.)* **No accepted owner carries this watch today.** The attended-operations owner must adopt it, with a cadence and a binding owner, before §A12 is accepted or in the same act. It is therefore a precondition of D1, not a follow-up (§A12.5). *(Revised 2026-10-01 on Codex review of #584 at `e5e1397`.)*

*Consequence, stated rather than hidden.* The documented correlation lists are session-scoped and reset at about 17:00 ET (REST §6.4). Cross-session recovery is UNESTABLISHED (R-2 closed with limits, 2026-09-29). So a request that is not correlated within its own session is likely, in practice, to stay held.

**F4. Unknown non-entry requests (§A2 rule 7, carried).** An unknown amend (`change`), cancel, cancel/replace, close (full or partial), attach or flatten, including the scheduled flatten, is governed by the accepted carriers:
- halt/resume §2, row "uncertain transport/order outcome, protection fault", and §3's attended recovery;
- rail I1: an `UNKNOWN` refuses every risk-adding action.

That means immediate attended intervention, with no autonomous protection claimed. This ADR's own §2 row "Protection identity, quantity, ownership, platform state … uncertain/failed" (Proposed) states the same response. F1 already halts the whole account. This rule adds, for each request type, what is presumed and what attended reconciliation must establish. New risk-adds on the affected leg stay refused until attended reconciliation establishes its position and working orders from fresh evidence; F3 and halt/resume §3 already impose that account-wide. An unknown cancel of a resting entry leaves that entry's reservation held under F2 (rail spec S4).

| Unknown request | Presumed while unknown | Reconciliation must establish (fresh, postdating evidence) | Evidence owner (§A12.5) |
|---|---|---|---|
| Amend (`change`, Tradovate modify) | The old stop may or may not be working, at either price. A version can exist for a command that is later rejected (REST §6.4, Q21) | The protective order's state and effective price, from command reports and lifecycle | M2 modify semantics; GC-2b / X-2 |
| Cancel | The order may still be working, or partly filled | The order's terminal status and its fills by `orderId` | GC-4 / X-4 |
| Cancel/replace | Non-atomic: either order, both or neither may be working; the route returns `reconciliation_required` on ambiguity (REST §6.4, Q28) | Both orders' states and fills | — |
| Full close (`liquidateposition`) | The position may be unreduced, partly reduced, flat or reversed. Protection may already be cancelled | Fill-reconciled position; working orders on the contract, and on the account while the scope question S stays `CONFLICTING`; fills by `orderId` | C-a M1–M9 |
| Partial close | An opposing market order; working orders stay in place; reversal is possible (§A4) | Position against protective quantity | Subset-exit path under UB-5 (C-a covers whole-leg exits only, §A11.1) |
| Attach | Protection may or may not exist. L2(f) is unsupported on this route (§A4), and no edition uses it | Whether any protective order exists, and its quantity | — |
| Scheduled flatten | As a full close. SCHEDULED_EXIT authority is revoked; the own-flat deadline stays an obligation for attended handling (halt/resume §2, §5) | As a full close | C-a M1–M9 |

**F5. Unexplained effects.** Any position, working order or fill on any symbol that is explained neither by an owned operation nor by a recorded operator action under §A11 item 4 is an incident. The accepted carriers are halt/resume §2 ("Unknown order identity is an incident"; the protection-fault row) and rail E2 ("Contradictory immutable identities require attended resolution"). This ADR's §2 protection/state-failure row and §A2 rule 6 (both Proposed) state the same. **F5 does not classify operator platform actions**, such as a manual takeover or an operator-placed preservation trade on a book symbol. Halt/resume §4.1 O-5 and §A11 item 4 leave those OPEN, and they stay OPEN. *(Revised 2026-10-01 on the refute-first review of #584, P1-2.)* *Conditional on D3 (§A12.5), and with §A7's correlation clause qualified to match (§A12.3):* an effect that an accepted F2 class uniquely correlates to a held request is that request's outcome, and it transfers under F2. Until D3 is confirmed, that transfer is deferred and the effect is treated as below. An effect that is not uniquely correlated never releases a held request. It becomes an additional identified exposure alongside the reservation, and the double count is deliberate. §A2 rule 6's premise that "no fill can be uniquely correlated to an unknown request (T08 §7.3 blockers 1–2)" is qualified for the first release to that extent: the REST §6.4 recipe postdates T08 §7.3 (D3, §A12.5).

**F6. The normal path is unchanged.** With no unknown request outstanding, admission is today's admission. The first release has no exceptional mode, no loss-room check and no bound worst-case charge figure (F1(b)).

#### A12.2 — Reconciliation with T08 §7.10, "halt versus reservation"

T08 §7.10 ([PR #575](https://github.com/Joshua-Asante/first-passage/pull/575), head `aa20360`) reads the operator's 2026-10-01 route ruling in three parts. §A12 matches each:

1. *"An unresolved request keeps its worst-case reservation, which is never released without such an outcome."* F1(b) and F2. The whole worst-case reservation is kept: its contract capacity (§A2 rule 5; UB-2's quantity (1)), and its loss charge (§A2 rule 3; UB-2's quantity (2)), held as retained inputs. Only the charge's **figure** is deferred, with §A3 and UB-2. Its only consumers are the deferred room check (rules 4′/4a) and B's resume. While F1 halts the account nothing is admitted, so no first-release decision needs the value. An unbound charge is never read as zero or as released. *(Revised 2026-10-01 on Codex review of #584 (P1). The first draft held capacity only, which would have narrowed T08 §7.10.)*
2. *"'Halt' here is the current first-release posture … It is not a permanent account block."* F1(c) and F3. The block is not permanent: F2 names how it ends. In attended recovery, closure row 1 and E3 release on unique correlation once an accepted E3 producer supplies the facts (halt/resume §4 ¶2; Gate A A3(iii)). That producer is already a live-release precondition, and the REST recipe is a candidate for it. The scope note's §1 premise of "permanently" assumed no evidence could ever resolve a request. But the block is **indefinite in practice** whenever no F2 evidence arrives (F3), as §A11 item 2 accepted. That includes every lost-response request until such a producer is accepted. *(Revised 2026-10-01 on the refute-first review of #584, P2-1.)* Under the unamended E3, the unresolved request owns an account block across sessions until F2 releases it. Even then, the halt ends only through F3.
3. *"Whether automation later resumes with reduced room while a reservation-held unknown remains … stays with the amendment owner."* Deferred (§A12.3: rules 4′, 4a–4c, 9′, 12; the §A5 halt/resume §3–§4 and E3 additions). §A12 neither adopts nor narrows that rule.

#### A12.3 — Disposition of the existing rules for the first release

**IN** = first-release text, as the named F rule. **DEFERRED** = out of the first release by the 2026-10-01 ruling, or because it depends on deferred text; preserved for a later release, **not deleted**. **INERT** = cannot bind while F1 halts the account; deferred with B. **UNRULED** = in neither the ruled IN list nor the OUT list; returned as a decision (§A12.5).

| Text | First release | Note |
|---|---|---|
| §A1 narrowed shape | Not decision-bearing for the response (F1(d)) | Editions are still prepared in the shape (§A8; campaign §59). Its trace stays owed (§A12.5) |
| §A2 rule 1 | **IN** as F1(a)–(b) | Its "not an account block" clause is **DEFERRED**: that is B |
| §A2 rule 2(a) | **IN** as F2 | — |
| §A2 rule 2(b), option A | Unavailable | T08 §7.9. Retained, so a later vendor bound could reopen it |
| §A2 rule 3, worst-case charge | **IN** as held retained inputs (F1(b)); the **figure** is **DEFERRED** | The figure waits on §A3 and UB-2. Unbound until then, never read as zero (§A12.2 item 1) |
| §A2 rule 4 / §A10 rule 4′ | **DEFERRED** | By ruling |
| §A2 rule 5, micro-cap accounting | **IN** as F1(b) | — |
| §A2 rule 6 | **IN** as F5 | Premise qualified (D3) |
| §A2 rule 7, non-entry requests | **IN** as F4 | By ruling |
| §A2 rule 8, exhaustion | **INERT** | No admission while halted |
| §A3 figures | **DEFERRED** | By ruling |
| §A5 propagation | Replaced for the first release by a reduced set, owed with the acceptance packet (§A12.7) | §A5 stays the later-release set |
| §A6 falsifiers 1, 2, 4 (atomicity, quantity growth, one contract) | Kept as falsifiers of the §A1 trace | Not first-release gates (D6) |
| §A6 falsifiers 3, 5 (no-unknowns replay; response within room) | **DEFERRED** | They test rule 4′ and the room. Attended response remains T13's to measure |
| §A7 forbidden moves | In force, with one clause conditional | The clause "treating an observed later fill as correlated to an unknown request" stands unchanged **unless D3 is confirmed**. If D3 is confirmed, it yields only to evidence that an accepted F2 class uniquely correlates, and every other use of an observed fill stays forbidden. Until then, F5's correlated-effect transfer is **DEFERRED**, and an observed effect is only an additional exposure. *(Added 2026-10-01 on Codex review of #584 (P1).)* |
| §A8 rule 9 / §A10 rule 9′ | **DEFERRED** | 9′ by ruling; rule 9's loss part goes with it. Whole-intent capacity reservation stays a §59 Ruling 5 edition-preparation constraint |
| §A8 rule 10, one unresolved request per symbol | **UNRULED** | D4 |
| §A8 Q5, correlation by exclusivity | Not adopted | UB-7 recommended answer |
| §A9.1 UB-1 (ruled) | Rule text **DEFERRED** (4′, 4a–4c) | The ruling stands for the later release |
| UB-2, UB-6, UB-9, UB-10 | **DEFERRED** | By ruling |
| UB-3 (ruled) / §A10 rule 11 | **UNRULED** as amendment text | D5. Item 3 (resume) is B machinery and is **DEFERRED**; its stale-evidence consequence is owed at acceptance (§A12.5) |
| UB-4 | With the editions | Unchanged; not amendment text |
| UB-5 | Kept | Close contract; EVIDENCE-PENDING |
| UB-7 | Kept | Decides F2's evidence classes (D2) |
| UB-8 (ruled) | Settled for the first release | §A11 took §A10's non-mandatory branch |
| §A10 rules 4a, 4b, 4c, 12 | **DEFERRED** | By ruling |

#### A12.5 — Evidence still owed

| Item | What it decides for the first release | State at drafting | Owner |
|---|---|---|---|
| **UB-7** | Which evidence classes release a held request under F2, including whether a positive `clOrdId` lookup counts, and anything across sessions | R-1 on X-1's order **DISCHARGED** 2026-10-01, `LOCATED_WITH_CLORDID`: one order, same session, at that time only. It does not establish uniqueness, anything about an absent order, or cross-session behavior. R-2 closed with limits 2026-09-29; cross-session recovery UNESTABLISHED. Gate A A3(iii) constraint: a located entry settles only the facts it establishes | Route/incident coordinator records the evidence; gate C and T09 apply the classifier constraint; lifting §59 Ruling 7(b)(3)'s hold is Joshua's (D2) |
| **§A1 CAP trace** | Not a first-release admission precondition (F1(d); D6). It supports F2 and F4's child correlation (`ocoId`/`parentId`/`linkedId`) and stays B's admission precondition | X-1 executed 2026-09-30: scoped GC-2a PASS, evidence accepted with limits, no release ratification. The drill plan's "X-1 acceptance" addendum ([PR #572](https://github.com/Joshua-Asante/first-passage/pull/572)) is merged, and [CAP-20260916](../briefs/phase4-preparation/2026-09-16/capability-decision.md)'s 2026-09-30 scoped update records the PASS: the observed one-contract identity, fill and protection trace, not qualified wholesale. **Still owed:** binding that trace to a deployed strategy consumer. *(Updated 2026-10-02 on Codex review of #584 at `e57bd98`.)* | Coordinator, through CAP; Joshua performs any further trace (D1–D4 of 2026-09-25 are individual decisions, §A11.1 item 6) |
| **Subset-exit (partial close) evidence** (UB-5; L2(d) partial) | What an unknown partial close leaves (F4 partial-close row): attribution, protection adjustment and race handling. C-a excludes it (§A11.1), and an edition never widens a subset exit into whole-leg liquidation (§59 Ruling 5) | §A4 marks partial close **U** on this route. No trace or documentary step is carded. UB-5 is EVIDENCE-PENDING through gate C. Until a primitive is qualified, T09's partial-close case is an offline consumer case: halt, presume per F4, retain everything. It is not route evidence | Coordinator, under gate C (card a subset-close step, or record the case unsupported). The operator decides any edition consequence |
| **C-a M1–M9** ([close-semantics note](../notes/2026-09-26-close-semantics-c-a.md) §2.1) | What an unknown or failed whole-leg close or flatten leaves (F4 close and flatten rows), and the attended flatten after an uncertain liquidation | All nine `OPEN`; S `CONFLICTING`; the vendor question has not been sent. X-3 runs only inside the operator's residual-risk decision; a contradicting trace stops C-a | Close-semantics investigation under R-CLOSE (coordinator). Sending the vendor question and the residual-risk decision are Joshua's |
| **M2 modify semantics** (GC-2b; X-2's precondition) | What an unknown or rejected amend leaves (F4 amend row) | Returned 2026-09-28 ([PR #541](https://github.com/Joshua-Asante/first-passage/pull/541)): Q1–Q4 `OPEN`. The coordinator's review of the return is owed | Coordinator reviews. The vendor question and the GC-2b decision for Striker and Aegis are Joshua's |
| **Held-request watch and monitoring loss** (F3; D5) | Who checks for late effects of a held request across sessions, and what alert-channel loss without an incident does | Not carried by any accepted owner. Halt/resume §3's attendance sentence is ambiguous for a disarmed account with a live unknown. Rule 11 / UB-3 (unruled as text here, D5) was the only text addressing absent attendance | Attended operations (T13) and D-MON; adoption is a precondition of D1. The channel choice is still the operator's (2026-10-01 rulings item 5, **D-MON bullet**; not its feed-repair bullet) |
| Halt-on-unknown implementation (F1(c)) | That the owner raises the halt this text relies on | CC-3 repair demonstrated synthetically, not accepted (halt/resume §4.1 record, 2026-09-29) | TB-I3 / T09 |
| **Stale order-level evidence** (halt/resume §4.1 O-1) | Whether evidence going stale and then fresh again can restore admission without reconciliation | O-1 is OPEN. Today stale evidence (one bar, `pending` row marker (2)) yields a **refusal, not a halt** (the #519 trace O-1 cites). No incident occurs, so halt/resume §3 and marker (5), which acts only after an incident halt, do not stop fresh evidence lifting the refusal. **Fresh evidence alone must not lift it.** No accepted owner says so today, and §A12 adds no rule. *(Added 2026-10-02 on Codex review of #584 at `e57bd98`, P1.)* | O-1's owners (rail spec fence classification; TB-I3). The choice between an explicit no-auto-resume rule for the refusal path and classifying stale evidence as an incident is owed at acceptance, and is Joshua's |

Kept and not reopened here: the close contract (R-CLOSE; UB-5) and the X-2 and X-4 rows (X-4's reduced build path is in the 2026-10-01 rulings, item 3).

**Acceptance prerequisites (D1: accept, amend or reject §A12).** Preconditions to acceptance, not parallel follow-ups:
- both step-4 reviews of this text are clean (§A12.7);
- each of these decisions has a recorded disposition:
  - D2: F2's evidence classes, meaning the runtime classifier's (T09) class, and whether §59 Ruling 7(b)(3)'s hold also reaches attended recovery;
  - D3: confirm F5's qualification of §A2 rule 6's premise and the matching §A7 clause (§A12.3), or keep both absolute;
  - D4: whether §A8 rule 10 (one unresolved request per symbol) is first-release amendment text;
  - D5: whether §A10 rule 11 (UB-3) is carried as text;
  - D6: whether the §A1 trace gates acceptance of this text;
  - D7: §A9's gate for the first release, either a written answer for every UB row (UB-1 to UB-10) or explicit approval of the §A12.3 disposition as its replacement;
- the attended-operations owner has adopted the held-request watch (F3), or adopts it in the same act;
- the stale-evidence choice above is recorded: an explicit no-auto-resume rule for the refusal path, or stale evidence classified as an incident.

D8, whether §A12 also governs an armed commissioning session (Scope), is not a precondition.

#### A12.7 — Reviews and what this section does not do

**Step-4 reviews of this narrow text** (scope §5 step 4; 2026-10-01 rulings item 1, "Both step-4 reviews stay, applied to the narrow text"): (a) a separate-session refute-first review, under D-codex (a), spawned by the coordinator and not by the author; (b) a cross-vendor Codex review on the pull request. Their findings and dispositions are recorded with the pull request.

**Not done here.** No accepted contract, CAP verdict, owner text or §A2/§A8/§A10 text is changed. No option-B rule is accepted, rejected or made effective. No figure is written. Nothing is granted: no T09 dispatch, gate acceptance, drill, order action, arm, deployment or spend. Live release stays held (T08 §7.8 part 1).

**Carried out (2026-10-02).** §A12.4 (reduced propagation set) and §A12.6 (decisions D1–D8 with recommendations and rationale) were removed under the coordinator's scope narrowing and are carried to the acceptance packet note `docs/notes/2026-10-02-a12-acceptance-packet.md` (commit `7424747`), owed when Joshua takes up acceptance; D1's prerequisites stay in §A12.5.

## Change history

| Date | Change | By |
|---|---|---|
| 2026-09-17 UTC | Record operator-directed incident amendment and conditional ATM/thin-bridge assessment | Joshua + Codex |
| 2026-09-24 UTC | Addendum (Proposed): bounded-exposure reservation for unknown narrowed-shape requests, after T08 R3 = NONE and the operator's Q1 = B ruling | Joshua (rulings) + Claude (text) |
| 2026-09-25 UTC | §A4 dated correction and §A8 revision (Proposed): whole book in the narrowed shape; rules 9–10; exit-side partials moot; open question Q5. Still Proposed; the step-4 reviews are owed | Joshua (rulings) + Claude (text) |
| 2026-09-26 UTC | §A9 (Proposed): eight questions (UB-1..UB-8) that must be answered before acceptance, including an availability assessment. B remains the direction; no rule, figure or mapping added | Joshua (review) + Claude (text) |
| 2026-09-26 UTC | §A9.1 (Proposed): recommended answers to UB-1..UB-8 plus UB-9 (re-evaluation) and UB-10 (one obligation record per child), each tagged; §A9 order and UB-8 wording corrected; qualified sentences of §A2/§A8 listed. Not accepted | Joshua (review, direction) + Claude (text) |
| 2026-09-26 UTC | Operator ruling: §A9.1 POLICY rows UB-1, UB-3, UB-8, UB-9 ruled as written; other rows remain recommendations. Addendum still Proposed; contract text owed | Joshua (ruling) + Claude (text) |
| 2026-09-26 UTC | §A10 (Proposed): contract text for the ruled POLICY rows: rules 4′, 4a–4c, 9′, 11, 12 and the UB-8 acceptance condition; allocation-dependent and unruled details marked OPEN; reader intercepts at rules 4 and 9 | Claude (text) under the operator's ruling |
| 2026-09-26 UTC | §A11: operator ruling on the first-release posture, recorded from the operator's written ruling (which supersedes the shorthand recording of the structured answers): preserve-and-block for one attended session, then explicit review before extending; possible indefinite suspension accepted, and no acknowledgment, reset or elapsed time resolves the obligation; B's implementation deferred, B retained as Proposed; §A10 first-release branch recorded (no UB-8 finding by the ruling; the packet's recommended determination noted as basis, not ruling); manual intervention subject to fencing, outcome evidence and reconciliation; preservation trades OPEN. Dated pointers at the top-of-file callout, under §A10's status (allocation map returned) and under its acceptance condition. Addendum still Proposed; §A10 not made effective | Joshua (ruling) + Claude (text) |
| 2026-09-26 UTC | §A11.1: operator ruling on close, reads and drills (written ruling governs): C-a is the first candidate to investigate, investigation only; neither the close-contract amendment nor an unspecified residual risk accepted; a contradicting trace stops C-a; C-b needs its own expression decision and qualification; R-1/R-2 only, operator-performed, after the existing REST entitlement is confirmed; no purchase, new access, route change or order mutation; normal-case drill decisions prepared individually, race drill deferred, no automatic fallback to the live evaluation environment; webhook-form D1–D4 of 2026-09-25 not treated as cleared, each an individual decision. Dated pointers at rule 9′ (§59 Ruling 5 split constraint) and at §A8's D1 fact | Joshua (ruling) + Claude (text) |
| 2026-09-27 UTC | §A11.2: operator ruling: for commissioning and the first attended release, an incident ends automated trading for that session; no same-session restart; recovery and evidence collection continue; review before another session; incidents only, not correctly handled refusals. New ruling narrowing rev9 §4 for those contexts; halt/resume owner text via handoff H5 | Joshua (ruling) + Claude (text) |
| 2026-09-27 UTC | §A11.3: operator ruling: a completed operator-placed preservation trade may be the R-2 and settlement-read target where it qualifies; R-1 observes a same-session trade placed anyway; entitlement and transaction identity to be confirmed; no additional trade, purchase or reset. Mirrored in the drill plan's ruling block | Joshua (ruling) + Claude (text) |
| 2026-09-27 UTC | §A11.2 clarifications (operator, same day): a deliberate operator stop with no fault is an incident for §A11.2 (O-6); the ruling covers the first attended release and any commissioning session in which automation is armed, none defined today (O-7). Applied to the halt/resume amendment by handoff H5 step (a) | Joshua (ruling) + Claude (text) |
| 2026-10-01 UTC | §A12 (PROPOSED): narrow first-release text under the operator's 2026-10-01 ruling (six cuts, item 1; PR #580). Rules F1–F6 (unknown request: reservation held and halt; release only on a uniquely correlated outcome; §A2 rule 7 by request type; unexplained effects; normal path unchanged); reconciliation with T08 §7.10; disposition of every §A2/§A8/§A10 rule (deferred, not deleted); reduced propagation set; evidence owed with owners; decisions D1–D6. Revised the same day on Codex review of #584: the worst-case reservation is kept with its figure unbound; HALTED persists past an F2 transfer; §A7's correlation clause is made conditional on D3; a subset-exit evidence owner is named. Revised again on the refute-first review (NOT_REFUTED_WITH_FINDINGS): the unknown-dispatch working-order bullet now waits on D2 (`pending` markers re-cited); F5 no longer classifies operator platform actions (O-5 stays OPEN); §A9's withhold is answered by §A12.3 for the first release; D2 is split into the runtime classifier and attended recovery; a held-request watch and monitoring loss are routed to T13/D-MON; the T09 cases add the split outcome-known gate; F1 gets an in-flight boundary; the rev9 supersession, carriers, the scope-note and VAN-5 pointers, and D5's citation are fixed. A further Codex pass at `e5e1397`: only an unknown (not a pending) request is an incident; the held-request watch and D2–D6 become preconditions of D1; the split propagation covers every affected pre-registration row, with UB-5 kept OWED. A second Codex pass: §A9's gate is not treated as answered (new D7); the monitoring-owner citation names item 5's D-MON bullet; the edition production handoffs are added to propagation. A further Codex pass at `373a103`: D7's first branch requires an answer for every UB row, including UB-5. Another Codex pass at `a77ae73`: scope narrowed to the first attended release (armed commissioning stays with the accepted contract; new D8, not a D1 precondition); the T08 and session-plan "exit-side partials moot" lines are added to propagation. Not accepted; no owner text changed | Joshua (ruling) + Claude (text) |
| 2026-10-02 UTC | §A12 narrowed by the coordinator under the operator's review-round limit (#584 issuecomment-5945118501, corrected by 5945120347): §A12.4 and §A12.6 removed and carried to the acceptance packet note (§A12.7); D1's prerequisites kept in §A12.5 as a plain list; a stale-evidence row added to §A12.5 (O-1 OPEN: a refusal, not a halt; fresh evidence alone must not lift it; the no-auto-resume-or-incident choice owed at acceptance), with F3's marker (5) citation limited to the incident halt; the CAP row updated for #572 (scoped X-1 PASS recorded; binding to a deployed consumer still owed). Still PROPOSED; no owner text changed | Coordinator (scope) + Claude (text) |
