# X-4 decision packet — resting entry cancellation and child teardown

**Status: PREPARED FOR REVIEW; NOT CLEARED TO EXECUTE.** Joshua's “proceed as
scoped” authorizes this documentary packet only. No account/host read, order,
cancel, arming, tool build or deployment is authorized or performed by it.
Joshua subsequently requested concrete recommendations and a draft offline
build/review handoff. The recommendations below remain **PROPOSED**, not ratified;
the [bounded handoff](../briefs/handoffs/2026-09-30-x4-offline-tools-build-review.md)
is a draft, not a dispatch. The deployment coordinator retains combined acceptance; Joshua retains the
actor ruling, numerical limits, environment decision and separate written CP-3.

## 1. Outcome, owners and boundary

Prepare one attended REST observation of cancelling a **resting buy-stop entry
for one MNQ contract**, with both native stop-loss and take-profit children.
The intended observation is parent `Working`, both children `Suspended`, then
one parent cancel, followed by terminal parent/children, no fills, flat exposure
and no working orders. This validates GC-4 for the observed route/environment/
symbol/date only. It does not choose or change ORB's ruled L1 lifecycle.

The [deployment checklist](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md)
is the roadmap. The [drill plan §2.4](2026-09-26-tradeify-route-drill-plan-draft.md#24-x-4--cancel-of-a-resting-stop-entry-ends-its-suspended-children-gc-4)
owns row semantics and §2.0 owns recovery. The [commissioning packet §4.2](2026-09-27-route-commissioning-session-packet.md#42-x-4-cancel-of-a-resting-stop-entry-ends-its-suspended-children-drill-plan-24-lines-265278)
owns the row's CP-3 fields; §3.7 C.2–C.4 supplies retained request shapes.
The [B–D packet](2026-09-26-tradeify-bd-decision-packet.md) owns GC-7 and GC-4's
consequence. Those owners govern wherever this preparation differs.

X-1's [scoped acceptance](2026-09-26-tradeify-route-drill-plan-draft.md#x-1-acceptance--2026-09-30)
is recorded. Its omitted intermediate P0b provides no interval coverage.
**Update 2026-10-01:** its separate post-teardown R-1 was discharged for X-1's
order, at that time only: Joshua's attended read 08:22–08:59Z returned
`LOCATED_WITH_CLORDID` ([dated owner result](2026-09-26-tradeify-route-drill-plan-draft.md#r-1-result-on-x-1s-order--2026-10-01)).
No extra trade follows from that result. The X-1 placement attempt is consumed.
X-1 does not prove MNQ behavior or cancellation of two Suspended children.

**Preparation return:** this packet, the actor decision text, private-binding
field inventory, request/read/recovery sequence and explicit remaining gates.
Stop here. A tool build needs its own bounded assignment and offline verification;
actual execution needs all readiness gates and X-4's CP-3. No X-2/X-3/X-5 is added.

## 2. Actor decision — proposed X-4-only exception

X-1's accepted exception for mandatory firm controls is X-1-only. It does not
amend X-4's session-start rule. **X-4 remains held** if an actor cannot meet the
drill plan's required state and no row-specific ruling has been accepted.

**Recommendation for Joshua's decision:** accept this narrow extension, to be
recorded in the B–D GC-7 owner and labelled mirrors only after acceptance:

> For X-4 only, identified non-disableable firm risk controls may remain enabled.
> Record their timed and threshold behavior privately, select a window avoiding
> known scheduled liquidation, and expressly accept that threshold intervention
> may still occur, including if the resting entry unexpectedly fills. Every
> operator-configurable competing sender remains disabled. Any firm intervention
> ends X-4 without a clean GC-4 PASS: retain the actor and outcome, invoke existing
> attended recovery, and reconcile every possibly effective request and order.
> Unknown outcomes remain held; flatness alone never clears them. This exception
> changes only X-4's session-start rule and grants no execution, runtime release,
> exclusive close ownership, C-a/X-3 exception or race guarantee.

Alternative: retain the hold until a compatible, expressly approved environment
exists. Do not disable mandatory firm controls. Neither recommendation nor this
preparation is a ruling. Configurable copier/Account Manager/ATM/replay/timed
exit/scheduled work/other senders must meet the full inventory rules. Inventory
vendor coverage repair separately; unexpected effects end testing. Expected
creation of the row's two children is not itself unexpected coverage repair.

**Recommended additional condition:** permit the exception only with the fresh
MNQ headroom gate in §3.1 passing and all applicable mandatory controls positively
identified. No observed/attested firm intervention yields a clean GC-4 PASS.
Retain the C-a/X-3 hold and every runtime-release gate. The rationale is that the
drill is short, attended, initially unfilled and subject to immediate recovery;
those facts reduce intended exposure but do not remove threshold-liquidation or
fill/cancel races. If the headroom gate fails, retain the hold; do not weaken it
or relabel the same evaluation account as an equivalent sandbox.

## 3. Private binding and explicit decisions still owed

Keep account identifiers, figures, request bytes, order ids and originals in a
new gitignored X-4 evidence folder. No live payload is created by this packet.

| Field | Proposal / completion requirement |
|---|---|
| Environment and exact account | Operator names the environment at CP-3. Incumbent eval is a candidate only; no automatic fallback and no equivalence inferred from a Demo label |
| Contract, route and quantity | Exact dated MNQ contract, away from roll; one contract per placement and in total; existing CrossTrade REST route, no account migration. Fresh private identity/tick binding required |
| Direction / entry / children | Buy; resting stop entry; both absolute `stopLoss` and `takeProfit` in the same request. No expiry drill |
| Quote source / side | Propose attended Tradovate web ask for the exact contract. Source identity, honest observation/procedure time and tick grid recorded |
| Placement freshness / movement / SEND | Preserve the ten-second freshness limit, both five-point bounds against a frozen approved reference and generation ask, exact human SEND confirmation and unchanged validated bytes. These are proposed for X-4 and require its approval; no numerical relaxation or unattended authority |
| Entry distance and cancel buffer | Recommend **100 points above generation ask**, **25-point buffer**. Entry must remain strictly more than the buffer above the current ask. Numerical judgment for this drill, not calibrated no-fill assurance; approval owed |
| Protective stop / target distances | Recommend **10-point stop**, **20-point target**, each from **entry E**; maximum actual fill-to-stop distance **20 points**. No anchoring on R; approval owed |
| Entry time in force | Propose explicit `day`, never an omitted default; bracket exits GTC per retained documentation. No GTD/scheduled-expiry or `cancelAfter` mechanism |
| Timing | Recommend initial unfilled-state evidence within **15 s of placement T0**, normal parent-cancel handoff before **30 s from T0**, terminal cancel evidence within **10 s of cancel T0**, stop validation within **10 s of first observed unexpected fill**; invalid protection triggers immediate recovery when detected, and absent valid protection at that deadline triggers recovery immediately then. The separate **60 s** read window is for final recovery confirmation, measured from recovery entry. §3.1 defines independent clocks; approval owed |
| Cost / headroom / calendar | Recommend **$50 planning allowance**, and the fresh MNQ stress/headroom gate in §3.1; private margin and remaining spend checks still required. Fresh 15-minute scheduled high-impact-release exclusion. X-1's MYM result does not transfer; no loss guarantee |
| Attempts and evidence budget | Recommend one placement and one designed parent-cancel attempt, each separately tracked, no retry/resend. **60 total read attempts**, including pre-send; at most **40** before final confirmation, reserving **20**; no more than **60 reads per rolling 60 s**, **10 s** request timeout, **one HTTP request in flight**, mutations included in serialization. All are new X-4 proposals, not broker safety guarantees |
| Cross-account no-hedge attestation | Fresh operator attestation after actor inventory and before written CP-3: no opposite or correlated-product position on any of the operator's accounts. Retain privately; account-local flatness and inventory do not establish it (X-1 packet §5 / §8) |
| Recovery actor / owner | Joshua attended throughout, rehearsed platform exit/cancel and evidence collection; Joshua owns unresolved effects. No automation restart that session |

No CP-3 is ready while any field or execution gate remains unresolved. If an
entry fills before the planned cancel, the row cannot receive its normal GC-4
PASS even if later recovery succeeds. The resting distance and buffer reduce
trigger likelihood; they cannot guarantee an unfilled entry.

### 3.1 Recommended profile and its limits — proposed, not executable defaults

**Instrument arithmetic, checked against primary sources:** MNQ is $2 per
index point, tick 0.25 points ($0.50). [CME contract specifications](https://www.cmegroup.com/markets/equities/nasdaq/micro-e-mini-nasdaq-100.contractSpecs.html).
Tradeify publishes $1.82 per contract round trip under its free-membership
assumptions. [Commission schedule](https://help.tradeify.co/en/articles/10468315-trading-commission-fees).
Both pages were read for this recommendation on September 30; account applicability
must still be confirmed. Production `core/firm_rules.py`'s `_TRADEIFY_EVAL`
records $0.91 per side, consistent with that schedule. `core/dd_protection.py`
and `ops/c1_rail/book_policy.py` were read under Rule 0; their sizing/protection
controls are not changed or used as authorization for this commissioning profile.

**Rationale:** 100 points keeps the intended resting entry away from a brief
attended quote/read/confirmation sequence; the 25-point buffer is an earlier
abort point. Neither is a volatility estimate or guarantee. A ten-point stop
represents $20 before fees; the 20-point realized-distance abort represents $40
before fees. At the published fee, $41.82 leaves $8.18 within the proposed $50
allowance. That allowance is for planning/spend accounting, not a cap on gaps,
failed protection or recovery loss. No profitability objective or ORB parameter
is optimized by these distances. Avoid extending the resting interval to obtain
more samples or to make a failed confirmation succeed.

**Deterministic price rule:** refuse an off-grid observed ask; for tick-valid
R, E = R + 100, SL = E − 10, TP = E + 20, all exactly on the 0.25-point grid.
Use Decimal arithmetic. No rounding is needed under this profile; reject altered
tick/distance inputs rather than silently rounding them. For a fill F, F − SL > 20
is immediate recovery. At placement, both five-point quote bounds, honest
ten-second prompt-age check and unchanged-byte check hold. Never regenerate
after a possible placement; pre-send regeneration retains the frozen reference
and a new independent request/validation hash pair. A new reference selection
requires its own explicit amendment; no automatic reselection.

**Headroom recommendation:** retain the X-1 decision's two-times stress-loss
factor and propose, for MNQ, L = 0.04 × R × $2 + applicable round-trip fee;
require current net-liquidation-to-firm-floor headroom H ≥ 2 × L. This is a
conservative new MNQ judgment screen, not evidence that X-1's historical MYM
component calibrates MNQ or bounds loss. It requires Joshua's explicit acceptance.
Compute from fresh private account/quote evidence before CP-3 and recheck at
session start. Margin and remaining $50 spend headroom are separate checks.
This gate can fail on the incumbent eval even with a tight planned stop; shrinking
the stop cannot cure it. No account figure or present gate result is asserted.

**Clock contract:** initial observation ends at placement T0 + 15 s unless all
required unfilled facts already hold. Once they hold, request normal cancellation
immediately. The 30-second placement-to-cancel-handoff limit includes human
confirmation time; it is not a promise that the remote order ends then. Buffer
≤25, stale/missing quote, an unexpected fill or expiration of either clock exits
the normal REST-cancel path and prompts immediate attended platform recovery.
Do not wait for a delayed confirmation. Disable pending normal mutation work;
if a mutation already crossed its handoff, retain it as possibly effective.
Cancel T0 + 10 s without terminal evidence is uncertainty/recovery, never success.
Final recovery confirmation gets a **60-second read window from recovery entry**,
bounded also by session end and remaining read capacity; unresolved effects stay
owned after it. Physical recovery continues even when evidence collection stops.

**Window and observation:** recommend one 30-minute attended evening window,
date/time chosen later; no placement within its final **180 seconds**. Avoid the
15-minute bands around scheduled high-impact releases and identified timed firm
actions. That reserve is operational slack, not a closure guarantee. During a
resting interval Joshua watches the exact Tradovate contract and reports any
buffer breach immediately. Retain adapter quote samples before placement and
before normal cancellation under the unchanged **ten-second** freshness rule;
record any intervening samples actually taken. Human watching is an attestation,
not a continuous machine quote stream or proof that no transient breach occurred.
No scraped quote feed is approved. Loss of quote visibility or stale required
input prompts platform recovery, not automatic timestamp renewal. Keep REST positions/working-order samples at a
proposed **5-second cadence**, with serialized requests and stated gaps. Do not
delay cancellation solely to reach another sample. This cadence is subject to the
exact-tool attended rehearsal: if infeasible, return a workflow finding; do not
enlarge freshness, lengthen exposure or invent unattended input.

**Cancel-specific safeguard:** after exact `CANCEL <context-hash-prefix>` human
confirmation, refresh the parent's identity-bound status; it must be unfilled
`Working`, response receipt age ≤5 seconds, with no invalidating event, expired
resting deadline or buffer trigger. Hash method, account-bound path, empty body,
parent id and binding together; hashing `{}` alone is insufficient. Do not apply
the placement's five-point movement test to this risk-reducing request: price can
move enough to require cancellation. On failed readiness, use the attended
platform branch immediately. This new cancellation contract still needs review
and approval; no claim of atomic read/cancel coherence is made.

**Offline build use:** the recommended numbers may be installed as a named
`PROPOSED` synthetic profile for tests. A missing approval or unresolved private
binding must refuse a production execution path before credential/network use.
Synthetic approvals exercise mechanics only. Builder and reviewer cannot ratify
the profile, actor exception or a live binding by marking a fixture accepted.

## 4. Request and observation contract for the next preparation slice

These shapes come from retained commissioning §3.7, not newly verified live
vendor semantics. Before CP-3, recheck documentary drift and pin the actual
generator, sender, observer, adapter and binding. Round-7's X-1 generator permits
only `market` and bars `stopPrice` / `takeProfit` (`x1_generate.py` request keys
and `validate_binding`); its observer assumes one stop child. **Those tools are
not cleared for X-4.** Preserve them and their sealed evidence unchanged.

Required X-4 request specification, not an executable request:

- Placement: `POST /v1/api/tv/accounts/{account}/orders/place`; fields
  `instrument`, `action=buy`, `qty=1`, `orderType=stop`, explicit `tif`, fresh
  `orderId`, `stopPrice=E`, `stopLoss`, `takeProfit`. No separate `clOrdId`;
  the retained forwarding semantics provide the correlation id.
- Prices: first E = R + approved resting distance; then stopLoss = E − approved
  stop distance; takeProfit = E + approved target distance. The reviewed generator
  must define deterministic tick rounding, verify stop < E < target, entry beyond
  the buffer and entry-to-stop distance within the approved maximum. Rounding
  and reference-reselection rules must be accepted before generation.
- Parent cancel: `POST /v1/api/tv/accounts/{account}/orders/{entry_id}/cancel`,
  body `{}`, bound to the positively identified parent. It is the row's designed
  second mutation, separately logged; placement approval alone does not approve it.
- Retain and independently compare actual placement/validation bytes, sidecars,
  binding, tool/adapter hashes before handoff. Freeze bytes; no silent repricing.
  The read-only observer must never issue a mutation. A future cancel controller
  needs its own reviewed freshness/state checks and exact human confirmation.
  Bind its confirmation to the exact account/parent/empty-body attempt, and
  define how the buffer-triggered cancel remains prompt. Do not blindly reuse
  placement movement checks to suppress a required cancellation after price moves;
  that cancellation contract is a separate reviewed requirement, not approved here.
- Both-child ids: retain `orderId`, `oso1Id`, `oso2Id` and `osoChildIds`; retained
  documentation orders legs target then stop. Validate each child's actual type,
  side, price, quantity, parent linkage and supported relationship fields rather
  than relying only on array order. Missing/ambiguous identity means no PASS.

Required offline tool/rehearsal coverage includes clean cancel, child remaining
live after parent terminal, fill before/during cancel, unknown placement/cancel,
late response, pending/malformed reads, timeout/rate limit, exhausted read budget,
firm intervention, quote-buffer breach and recovery while keeping one request
in flight. Terminal vocabulary must use reviewed vendor schemas (retained
v3.3 uses `Canceled`; the older drill table says `Cancelled`); do not invent an
alias or accept a raw unsupported state. Offline tests qualify tools only.

## 5. Later execution sequence — conditional on X-4 CP-3

1. Fresh session: confirm entitlement/venue conditions, accepted actor ruling,
   inventory, host rail `dry_run=true` / `armed_until=None`, daemon emission off,
   calendar, margin/headroom/spend and recovery readiness. Obtain original
   account-scoped fill-reconciled positions, working/session orders and OR:
   flat, nothing working, nothing outstanding. Historical snapshots do not clear it.
   After inventory, Joshua gives and privately retains the fresh **cross-account
   no-hedge attestation**: no opposite or correlated-product position on any of
   the operator's accounts, including other Equity Index products. Account-local
   flatness and actor checks cannot establish this. Missing, stale or conflicting
   attestation holds the row. Obtain written **X-4 CP-3 only after** this
   attestation and all other fresh readiness gates pass, before step 2.
2. Under X-4's accepted binding/rule, capture a fresh quote; derive, validate and
   record the exact entry and both child levels. Compare the independent hash
   record before observer and sender; human confirms the placement. Record time
   immediately before the single placement attempt. Unknown response: no resend.
3. Retain response; lifecycle must correlate the recorded id to one `New` and
   the parent and both children. Read lifecycle/status for all three, fills and
   positions: parent `Working`, children `Suspended`, no fill/exposure. Missing
   or uncertain required evidence ends normal observation, never assumed absent.
   Record account-wide competing-order/position samples at the accepted cadence
   and explicitly disclose any unobserved interval; X-1's omitted-sample ruling
   does not grant arbitrary omissions for a resting-entry interval.
4. Cancel promptly once that evidence is obtained; do not hold the entry for an
   expiry or extra observation. Recheck buffer while resting within the reviewed
   cadence. Buffer reached or resting deadline: invoke authorized cancellation /
   recovery; the result is not presumed a clean GC-4 observation. Record exactly
   one designed parent-cancel attempt and its immutable empty body and timestamp.
5. Read parent/child lifecycle/status, per-parent fills, and account positions/
   orders after the cancellation. Acknowledgment alone does not complete it.
   Reconcile any execution revealed while cancellation was in flight.
6. Fresh final account-wide positions/working/session orders, terminal evidence
   for every parent, child and recovery id, complete OR and host disarm checks.
   Seal all originals, including failed/late reads, and return. No further row.

**Unknown placement or cancel:** stop mutation sends, read actual exposure,
working orders and positively identified lifecycle/status first. No resend,
regeneration, speculative replacement or automatic flatten. An exposed position
gets the existing attended platform intervention only after those fresh reads
show it needs one; record the second close-owner race where a prior unknown
request could still act. If flat, do not flatten; cancel every positively
identified live order, including any live parent or orphan child, through the
attended platform. Record that additional actor and its race with the possibly
effective unknown request. Confirm terminal state for every involved id from
fresh reads after the last intervention. An unconfirmed effect or missing
terminal evidence remains outstanding even if the display is flat.

**Unexpected fill:** end the intended unfilled-cancel test; inspect actual
exposure and native stop `Working` at correct quantity and relationship under
the ten-second deadline from first observed fill. Missing valid protection at
that deadline triggers attended recovery immediately; detected invalid/rejected
protection, excess realized distance or unexpected quantity triggers it sooner,
without waiting for the deadline. The separate 60-second read window begins at
recovery entry and bounds final confirmation only; it never delays intervention. Manage
remaining entry/children under the existing recovery procedure, then confirm
flat/no-working/all-terminal. Never blindly remove the only effective protection
while exposure remains. Do not claim fill/cancel or OCO races cannot reverse.

**Other stops:** SC-1–SC-7, firm intervention, identity conflict, unclassified
coverage repair, deadline/window expiry or loss of host confirmation end testing.
If REST is unavailable or its budget is exhausted, attended platform recovery
continues; missing terminal REST evidence stays outstanding. No same-session
restart follows successful recovery, a reset or elapsed time.

## 6. Acceptance and remaining gate ledger

| Outcome | Required finding / consequence |
|---|---|
| Scoped GC-4 PASS | Supported terminal cancellation of parent; both children terminal after that cancel; retained no-fill evidence; nothing live or unresolved; final flat/no-working and complete terminal reconciliation. Scope is the actual MNQ/REST/environment/date only |
| GC-4 fail | Child remains `Suspended` or `Working` after parent terminal: **operator decision for ORB**, not automatic route-wide failure. Preserve trace, recover and return alternatives from the drill owner; no edition change adopted |
| Fill, firm intervention, identity/capture/shape gap, or unknown outcome | Record the actual branch, recovery and remaining obligations; no clean unfilled-cancel PASS. Protection failure retains its governing GC-2a consequence; cancellation failure alone is not relabelled as it |

Not established: expiry behavior, other symbols, absence of a race, repeated
cancel/idempotency, a cancellation-time distribution/bound, account-wide causal
coherence, C-a close, unknown-request resolution/fence, production consumer
qualification or deployment. R-1, R-2 and other route/settlement gates retain
their separately recorded dispositions.

| Gate | Current preparation disposition |
|---|---|
| Prior-row review | X-1 scoped decision recorded; sealed evidence untouched |
| X-4 actor exception | Proposed in §2; **operator ruling owed** |
| Exact limits / environment / private binding | Field inventory in §3; **operator selections and fresh evidence owed** |
| X-4 tool and read contract | Requirements identified in §4; **build, review and offline verification owed** |
| Bounded offline build/review handoff | [Draft card](../briefs/handoffs/2026-09-30-x4-offline-tools-build-review.md) prepared; synthetic transports only; **not dispatched or implemented** |
| Attended rehearsal | **Owed on the exact accepted X-4 tools**, including unexpected fill and unknown cancel; X-1 rehearsal is supporting context only |
| Fresh session gates and separate written CP-3 | **Owed; no execution authorized**. Fresh cross-account no-hedge attestation follows inventory and precedes CP-3; account-local checks are insufficient |

**Document verification:** compared the packet to the retained drill §2.0/§2.4,
commissioning §3.2–§3.7/§4.2, X-1 acceptance and round-7 source restrictions on
primary HEAD `028c5ce88a473942e0e792bb607fe9e85133948b` plus prior documentary
edits. The later recommendations used direct production reads and primary CME /
Tradeify web pages; subsequent document validators are reported in the handoff.
No host/broker call, implementation or live-readiness PASS is claimed.
