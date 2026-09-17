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

## Change history

| Date | Change | By |
|---|---|---|
| 2026-09-17 UTC | Record operator-directed incident amendment and conditional ATM/thin-bridge assessment | Joshua + Codex |
