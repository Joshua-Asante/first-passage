# Offline broker and evidence producer contract

Stage 1 of the PR #365 extraction. Governing source: merged TB-S3 rev7,
`docs/spec/2026-09-12-c1-multi-leg-rail-extension-spec.md` §1 and §2e E1–E3.
The starting extraction was `b0103dc`; user revision `0dcc183` merged main
`e9fcebb`. #365 is closed and supplies historical regression provenance only.

## Acceptance boundary

This stage implements the offline producer portions of E1–E3. It does not accept
listener allocation credit, quarantine, request-owner discharge, durable recovery,
or account orchestration. Those remain #369/#370 obligations. Production telemetry
does not supply this full protocol; TB-I3 must qualify the real producer and causal
domain, and live L-2 support remains unproven. No ratification, registry admission,
deployment, arm or emission follows from merging this test-only stage.

## Observable protocol

- `snapshot(sym)` captures position, gross quantities and identities, working and
  terminal order facts, complete immutable entry executions, protection owners,
  immutable reduction allocations, global order locations and request fences in
  one synchronous acquisition. Nested maps are detached from broker state and
  other captures; they remain editable for deliberately malformed delivery tests.
- `Clock.sequence` is the external causal domain used by executions, reductions,
  acquisitions and consumer preparation/dispatch. Consumer restart never replaces
  this clock. Consumers persist their cursors and reject reordered evidence; this
  stage only produces it. Wall time advances explicitly. An `as_of` override is
  fault injection, not a historical query. Broker-process durability is not modeled.
- `executions` retains every entry execution and its original fields. `lot_facts`
  identifies gross accounting lots; net zero never hides opposite-side lots.
  Multiple partial executions can share one open accounting lot. A fill after its
  protection was consumed or its accounting quantity exhausted gets a fresh identity.
- `protection_owners` retains each originating owner's quantity, consumed flag and
  component refs independently of its accounting lot quantity. Component parameters,
  linkage and trailing anchors are captured in `order_facts`, including terminal refs.
- `reductions` records the transition (`explicit_scope` or `triggered_protection`),
  triggering order/owner when present, allocated lot quantities, and exact immutable
  entry-execution tranches. FIFO iterates execution order, including interleaved
  partial fills, subtracting previously consumed tranches; dictionary order is not
  the allocation rule. Old history never changes on an order edit or later reduction.
- Request IDs are unique for the route lifetime. Reuse while pending or completed
  is refused before side effects and never overwrites the original record. Pending
  IDs and retained outcomes are global even on an unrelated symbol read. An unknown
  outcome remains unknown; a consumer must reconcile actual facts. Unexpected
  execution exceptions retain the accepted request as pending rather than omit it.
- Normal request boundaries validate before mutation: no duplicate order refs,
  malformed/empty ATTACH, duplicate defined component, consumed-owner reattachment,
  invalid quantities, foreign scoped lot, or identity-changing MODIFY. Generated
  refs cannot overwrite terminal or explicit refs. Direct broker-state edits remain
  deliberate adversarial injection, not a route capability.

## Native transition limits

The production emulator's `_fill_exit`, `_close_scope` and `_amend` were read before
extending the producer. The pinned trace is base2 + add2; add protection triggers,
base2 is consumed FIFO, add protection is consumed, and base protection survives
with its unchanged anchor to cover add2. A later fill of a partially filled entry
gets a new owner if the former owner was consumed; an AMEND cannot revive the old one.

Explicit scoped close is a separate transition, requires modeled L2(d) and L2(e),
and adjusts the selected lot's protection atomically while owner and allocation
quantities remain aligned. After FIFO makes those quantities diverge, bounded or
fill-scoped close is **unsupported and refused without mutation**: no reassignment
rule is invented. Full-symbol close can consume all gross lots and remove every
remaining owner atomically. Mixed-side exposure likewise requires full-symbol close.
#369 must retain a durable capability block/attended recovery for unsupported scopes.

Price triggers are explicit events, not a bar-fill emulator. Fixed levels are prices;
trailing parameters are ticks, converted through fixture-supplied `tick_sizes`.
The default unit tick is an abstract coordinate system, not MGC/MYM/MNQ geometry.
Capabilities marked supported characterize only the implemented offline surface.

## Independent sequence expectations

| Sequence | Required observation |
|---|---|
| Capture, fill, capture; deliver newest then oldest | Captures stay detached, execution lies between acquisition IDs. |
| Two deferred requests on different symbols; complete one | One pending owner remains globally; completion history and new locations persist. |
| Invalid deferred attachment or unexpected execution failure | Rejection is recorded, or accepted request remains pending; never a covering fence that forgot it. |
| Partial fill, mutate order, fill | Earlier immutable identity stays unchanged; opposite-side lots stay gross-visible. |
| Base2/add2, add trigger, base amend/trigger | FIFO consumes base, surviving owner keeps anchor, later exit consumes add; no owner recreation. |
| A1, B1, A1, C2; C trigger | Allocate A's first execution and B, not both A executions. |
| Scoped add reduction vs triggered add exit | Explicit scope reduces add; trigger allocates FIFO. Histories distinguish them. |
| Divergent ownership then scoped/full close | Scoped transition refuses; full close clears lots and every owner. |
| Duplicate request/ref/attachment, malformed modify/fill | Rejected before any fabricated execution, overwritten identity or orphan protection. |

Producer tests import no listener or daemon and use literal/event-derived expectations.
Their success does not accept the consumers: the previous stack assumes one stable
lot ID per entry and allows malformed route calls as implicit fault injection.
#369 must migrate to the owner/tranche protocol, explicitly inject adversarial facts,
and re-review all retained-close, orphan and late-fill sequences before acceptance.

## Stage 2 extension (#369)

The primitive migration adds optional `Reduction.request_id`: explicit reductions
executed inside a broker request retain that request ID; direct external closes
retain `None`. This enables exact bounded-operation attribution despite concurrent
entry fills. The historical #368 verification below/above remains evidence for
its recorded revision; #369's updated producer and consumers are verified together
in `PRIMITIVE_VERIFICATION.md`.

## Stage 3 producer extension (#370)

The account integration adds an atomic close-time protection issue/trigger command.
Its reductions retain `request_id`, identify the triggering owner and allocate
FIFO. It can create a bare owner's first fixed component and consume it in the
same event. Partial execution is refused before mutation. No producer-only #368
acceptance or live qualification is inferred for this extension; see
`ACCOUNT_VERIFICATION.md` for combined sequence evidence.
