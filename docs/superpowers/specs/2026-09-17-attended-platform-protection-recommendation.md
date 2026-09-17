# Attended platform protection: simplify the incident contract first

Status: **PROPOSED RECOMMENDATION — publication authorized, not a runtime amendment.**

Joshua requested investigation of a local trading-platform bridge on an attended
VPS, expressed openness to platform-managed trailing, and instructed publication
of these recommendations on an isolated branch. This records the proposed
direction; it does not approve its unresolved exception semantics, purchase a
VPS, qualify a platform, change governing controls or authorize trading.

Baseline inspected: `63ea70143c67b31c07d3e90704d22621ce044710`, containing the
PR 411 feasibility design and PR 414 capability assessment. Production
`ops/c1_rail/book_policy.py` was read directly before this recommendation.
No sizing, capacity, allocation, strategy or calendar constant changes here.

## 1. Root problem and recommendation

The current attended incident contract stops every new runtime broker mutation.
Applying that rule to independently running platform protection creates a
requirement to pause trailing precisely, without cancelling working stops or
closing positions. That requirement is pushing the design toward a custom
trailing engine before the actual platform has been qualified.

Reconsider that contract before building the engine:

> On narrowly defined signal/control failures, stop new strategy activity while
> already established, qualified platform protection may continue under its
> original bounded authority until attended intervention.

This is a proposed exception to the all-mutation fence, not a claim that trailing
is inherently safe or that every incident permits continued management. It must
be reconciled into the governing contracts before implementation. Keep the
no-same-session strategy-reactivation restriction and complete reconciliation
before any future activation.

The broader simplification is to qualify a small set of platform-supported
behaviors, explicitly assess their economic and failure differences, and avoid
recreating unavailable broker primitives through additional services.

## 2. Candidate architecture

```text
Existing Python strategies
          |
Existing account owner, permission, reservations and durable journal
          |
Narrow local command-and-observation bridge
          |
NinjaTrader on an attended Windows VPS
          |
The account's qualified broker connection
```

The candidate replaces CrossTrade's order-routing role rather than stacking a
second execution route beneath it. The existing account owner remains the risk
and strategy-command authority. The platform is an explicitly inventoried actor
executing previously authorized protection; its actions must remain observable
and reconcilable. Do not reimplement strategies in NinjaScript or create another
independent sizing/permission owner.

Prefer built-in platform management if its actual behavior is acceptable. A
direct AddOn managing stops is a fallback, not the starting implementation.
Neither choice is qualified yet. VPS availability helps hosting; it does not
establish request closure, complete history, broker atomicity or stop survival.

## 3. Proposed incident distinctions

| Fault | Proposed response | Required boundary |
|---|---|---|
| Signal producer/control failure, with protection and execution state independently known healthy | Stop entries, adds and new strategy instructions; established protection may continue | Qualified protection retains its independent data, connection, ownership and original parameters; a general account-health failure is not misclassified here |
| Unknown entry or modification | Retain original operation, reservation and uncertainty; no resend or speculative repair | Do not assume an unknown change is protective or authorize new manager actions against an uncertain scope; classify continued effects explicitly |
| Protection identity/quantity, platform state, history or route failure | Attended intervention; continued-manager safety is not presumed | Report possible autonomous effects and fence confirmation/uncertainty separately; define a supported intervention procedure before release |
| Platform/VPS disconnect or death | No claim that trailing continues; alert through an independent channel | Qualify exactly which already accepted orders/OCO functions survive on the selected connection; reconnect cannot silently resume strategy authority |

An allowed protection scope must identify the account, instrument, protected
fills/quantity, orders/OCO relationships, manager/template version, price source,
activation/offset, permissible tightening and termination conditions. It must
exclude new risk, widening protection, entry retries, reversal, discretionary
repair and exposure beyond its qualified scope.

These are requirements for the next design, not a completed authorization
schema. If an ATM's scaling, rejection, partial-fill or repair behavior cannot
stay inside that scope, this exception does not qualify it. In particular, a
protective label does not prevent duplicate exits or reverse exposure.

The owner must retain manager-originated order changes and their effects. Manual
intervention can race them; a manual close is not complete until residual orders,
manager effects and unknown requests are accounted for. A paused Python process
does not prove a remote or platform actor has stopped.

## 4. Documentary findings and limits

The following findings motivated the recommendation; reverify against the
installed version and actual connection during qualification.

- Local ATM Auto Trail supports manual enable/disable on a working stop. That
  demonstrates a UI operation, not a supported programmatic pause-and-confirm
  fence. [Auto Trail](https://ninjatrader.com/support/helpguides/nt8/auto_trail.htm).
- `AtmStrategyClose` cancels working orders and closes positions; its return value
  does not confirm completion. It is not a pause primitive.
  [API reference](https://docs.ninjatrader.com/ninjascript/atmstrategyclose).
- The ATM FAQ describes cancellation of ATM stops/targets when a stop or target
  is rejected. This is a material qualification issue, not an acceptable default
  assumption about protection preservation.
  [ATM FAQ](https://ninjatrader.com/support/helpguides/nt8/faq.htm).
- Platform settings include choices affecting scale-in/bracket quantities and
  last-price versus bid/ask trailing triggers. These belong in the exact qualified
  configuration; a template name is insufficient identity.
  [Strategy settings](https://ninjatrader.com/support/helpguides/nt8/options_strategies.htm).
- Account-level order/execution observations and `Account.Change` provide
  candidate bridge interfaces. They do not establish durable complete history,
  broker-atomic changes or request deduplication.
  [AddOn account events](https://ninjatrader.com/support/helpguides/nt8/other_uses_for_an_addon.htm),
  [Change](https://ninjatrader.com/support/helpguides/nt8/change.htm).
- Broker order IDs may change during an order lifetime. Preserve internal
  operation identity and the observed mapping history rather than use a mutable
  broker ID as the sole durable key.
  [Order reference](https://ninjatrader.com/support/helpGuides/nt8/order.htm).

No supported programmatic ATM pause interface was established in the examined
documentation. This is an UNPROVEN capability, not proof that no such interface
exists. Local and server-side ATMs must not be conflated; their availability and
behavior require separate account/version qualification.

## 5. Requirements to reconsider, and those retained

| Requirement | Recommended treatment |
|---|---|
| All trailing logic broker-native | Permit qualified platform management with explicit disconnect and restart behavior; review normal trigger/fill parity |
| Every incident stops every protective modification | Investigate the narrow pre-existing-protection exception above; no blanket exemption |
| Amendment implementation | Prefer an outcome requirement: existing protection stays effective until the qualified modification takes effect; no assumption that cancel-first replacement satisfies it |
| Unknown-request resolution | Retain no blind resend and no release on absence/timeout. Automatic resolution may be limited, but attended closure still requires supported evidence |
| Scoped close, partial fills and residual protection | Retain existing safety/economic requirements initially; do not relax several primitive guarantees at once |
| Same-session reactivation | Remains prohibited after incident; continuing previously authorized protection is not resumed strategy trading |
| Settlement and initial account evidence | Unchanged; NinjaTrader or a VPS does not supply missing historical close facts by itself |

The initial scope is not an account migration, direct API entitlement assumption
or recommendation to buy a particular VPS. Account access, licensing, data and
platform interfaces must be established before proposing such actions.

## 6. Smallest next feasibility slice

1. Verify the incumbent account's supported NinjaTrader connection and AddOn/ATM
   access. Pin exact platform version, account/environment and candidate settings.
2. Map each used primitive to its actual platform behavior, including trigger
   price basis, increments, partial fills, OCO ownership, rejection, modification,
   scoped close and connection loss. Record incompatible behavior explicitly.
3. Design the signal/control-failure exception with exact eligibility, observation,
   original authority and operator intervention rules. A failed protection or
   uncertain account state must not enter that category by default.
4. In an authorized local simulator, compare trailing with accepted semantics;
   stop strategy input while protection continues; exercise manager rejection,
   partial fill, manual-close race, disconnect/reconnect and restart. Preserve
   identities and all unresolved effects. No VPS purchase is needed for this
   local characterization; simulation does not qualify broker guarantees.
5. Separately qualify the actual connection's persistent protection, modification
   and request-history behavior with retained evidence or a bounded operator-run
   procedure. Do not deliberately create live transport faults.
6. Choose built-in ATM plus a narrow bridge only if those results support it.
   Otherwise return the exact failure and compare a small explicit protection
   controller or another route before committing to implementation.

Unknown-request closure remains a decisive gate even if the ATM-pause requirement
is removed. A request accepted just before a lost response cannot be declared
unsent because the platform later shows no matching order. No exactly-once broker
claim follows from a durable local journal.

## 7. Contract and qualification impact

Before implementation, reconcile the accepted halt/resume and rail-extension
contracts, PR 411 minimal-release profile, operations procedure, manager actor
inventory, observation/reconciliation interfaces and affected tests. Record which
guarantees change; do not edit old acceptance records into new claims.

Phase 3 input/tooling preparation may continue within its authority. Keep affected
execution/fill definitions open before F1 until this design establishes whether
normal fills or only outage behavior changes. If already frozen, use the owning
change/invalidation process. No speculative outage probabilities or automatic
qualification rerun is authorized.

Completion of this recommendation means a reviewable alternative is recorded.
It does not mean that built-in ATM, the AddOn bridge, the VPS or the protective
exception has passed feasibility. No platform test, purchase, support message,
account action or runtime change was performed for this publication.
