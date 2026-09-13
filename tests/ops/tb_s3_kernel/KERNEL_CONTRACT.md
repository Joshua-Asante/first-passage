# Durable primitive kernel

Stage 2 consumes the merged #368 producer and implements the offline consumer
rules E1–E3/K1–K3 in TB-S3 rev7 §2e. It owns reservations, verified allocation,
quarantine, individual obligations, CANCEL/CLOSE/AMEND/ATTACH, protection recovery
and persisted effects. No daemon or account orchestration module is required.
Production L1 equivalence, L2 qualification and operator authorization remain owed.

## Supported boundary

- Entry executions have immutable, account-wide IDs and generation-specific lot
  IDs. Every generation is allocated separately; a full fill close owns late fills
  of its original entry until its remainders and gross exposure are quiescent.
- Accounting lots and protection owners are distinct. Triggered FIFO reductions
  may consume another accounting lot while preserving an owner's original anchor.
  Consumption is established in event order, including flat-then-new-entry traces.
- Commands expose explicit market closes. Bounded reductions support only
  `CLOSE(fill, qty)`; bounded leg/symbol exits are refused before dispatch.
  The producer refuses divergent scoped closes; the consumer retains a block
  until attended recovery (including a supported full-symbol close) resolves it.
- Native `triggered_protection` evidence is consumed, but listener-origin
  close-time triggered-protection dispatch is not exposed by this command API.
  #370 must re-review its caller against this limitation; it must not substitute
  an explicit fill close. That integration or a separate primitive extension is owed.
- Bounded-close progress is the sum of immutable reductions attributed to its
  dispatched request IDs, not a position delta. A late fill cannot erase progress
  and permit duplicate execution. Residual protection is checked before completion.
- `completion_actions(now)` permits account composition to plan journaled effects
  in the same transaction. Completion drives effects; status queries only report.

## Evidence and ownership

Full acquisitions must contain coherent W, status, facts and a global registry.
Previously observed registry keys cannot disappear from newer acquisitions.
Immutable entry/reduction histories must remain complete and unchanged; allocations
must conserve gross lots and net position. Reused global IDs and backdated or
rewritten histories retain identity-conflict blocks across restart. Incomplete
structural proof cannot settle work; later complete proof can restore coherence.

Each pending or covering external request expands its possible symbol set on
newer global fences even when its completion record is omitted. Renewed pending
state after completion retains a conflict owner. Completion transfers exposure
atomically to order/gross-lot owners, including offsetting lots with zero net.
Clearing one owner never clears another. Quiescence includes gross lots, active
protection and working entry remainders.

The producer extension in this stage adds optional `Reduction.request_id` for
explicit request attribution; direct external reductions retain `None`. It does
not add a live route. Schema **6** persists generation membership, acquired proof,
completed request identities and history conflicts. Missing/incompatible snapshots
are refused; no production or #370 schema migration is supplied.

## Verification and acceptance

`EXTRACTION_INVENTORY.md` preserves inherited test mapping. New rev7 regressions
use literal quantities and event-derived identities, and malformed evidence uses
explicit adversarial injection rather than invalid normal producer calls.
`PRIMITIVE_VERIFICATION.md` records final evidence. The former candidate blockers
(request-to-gross ownership, scope expansion, renewed IDs and the retained-close
race) now have focused sequence regressions and independent review. This boundary
accepts neither the superseded #365 implementation nor the #370 account stage.

## Stage 3 integration extension (#370)

#370 extends the command API with durable `triggered_protection` close-time exits
and an offline atomic producer transition. It preserves explicit-close limits and
request-attributed reduction accounting. The explicit-only restriction above
records the accepted #369 boundary; the extension is separately verified in
`ACCOUNT_VERIFICATION.md` and scoped in `ACCOUNT_CONTRACT.md`.
