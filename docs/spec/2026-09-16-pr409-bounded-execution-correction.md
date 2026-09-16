# PR 409 bounded execution correction

Status: DESIGN APPROVED by the operator in the 2026-09-16 Codex conversation. Slice A implementation and local verification are recorded in the [Slice A execution evidence](../superpowers/plans/2026-09-16-pr409-ingress-correction.md#final-slice-a-acceptance--2026-09-16). Slices B-D implementation and whole-PR acceptance remain outstanding.

Integration owner: the coordinating implementer of PR 409. Individual slice completion does not establish whole-PR acceptance.

## 0. Grounding and authority

Reviewed PR revision: `fc7cdc781c892207abdbfe0b7d9a4c7f046aa816`. The local executable probes ran on `a9175a101ac4e822125498a311a5d65b2f65ae35`; `git diff a9175a1..fc7cdc7 -- ops tests` was empty. The intervening merge changed skill guidance, not the probed runtime.

Sources inspected before design:

- [Account owner](../../ops/c1_rail/book_account_owner.py): dispatch, activation, takeover, capacity replay, attempt journal, feedback.
- [Runtime](../../ops/c1_signal_daemon/book_runtime.py), [loop](../../ops/c1_signal_daemon/book_evaluate_loop.py), [protocol](../../ops/c1_signal_daemon/book_protocol.py), and [feed](../../ops/c1_signal_daemon/feed.py).
- [Capacity reducer](../../ops/c1_rail/book_capacity.py) and [policy](../../ops/c1_rail/book_policy.py): executable accounting and risk-control boundaries; no constants change under this correction.
- [Rail contract](2026-09-12-c1-multi-leg-rail-extension-spec.md): S10, expected protection, ATTACH/AMEND, FIFO and protection-owner semantics.
- [Rev9 halt/resume contract](2026-09-14-tb-s3-halt-resume-contract.md): supersedes older incident-triggered automatic CLOSE/AMEND/ATTACH/CANCEL instructions. Ordinary and scheduled operations retain their prerequisites.
- [Capacity contract](2026-09-12-tradeify-book-protection-capacity-spec.md): cancellation evidence, whole-leg displacement, reservation ownership.
- [Emulator](../../ops/c1_signal_daemon/tv_broker_emulator.py) and [its tests](../../tests/ops/test_tv_broker_emulator.py): directional rounding, crossing evaluation, FIFO reductions, consumed protection.

Observed before correction: a partially filled displaced order produced entry/cancel/flat commands while seven contracts remained reserved; a bracket for ORB targeted a MYM fill; a rejected identical amendment became a permanent duplicate; inverted OHLC was retained; NaN raised with authority still NORMAL and no incident; a negative stop was sent; synthetic activation changed INTERVENTION to RUNNING with an incident and unknown attempt retained. The earlier async takeover regression expected a flat before cancellation evidence and therefore encoded the wrong intermediate ordering.

ROOT CAUSE: validation, identity, and evidence prerequisites are not enforced consistently across independently advanced operation, attempt, capacity, protection, and authority state.

FIX: preserve the architecture, but establish shared ingress validation, explicit ownership and occurrence identity, evidence-gated transitions, and a narrow synthetic bootstrap boundary.

VERIFICATION: reproduce each defect before repair; assert intermediate invariants and final outcomes after repair, including duplicate delivery, reordered evidence, restart, cutoff, and halt races. Existing green tests are not acceptance evidence for missing invariants.

## 1. Scope and invariant set

Keep the account owner, serializer, journal, capacity reducer, adapter protocol, and existing strategy semantics. Do not build a second account coordinator or rewrite the execution stack.

Global constraints:

- Offline synthetic execution only; no production transport, deployment, arming, or trading.
- No strategy parameters, sizing laws, allocation constants, protection-tier constants, or calibration changes.
- No production resume or general-purpose incident recovery in this correction.
- Preserve immutable historical operation/fact identities and retained obligations.
- Preserve the Python 3.11 language floor and existing repository layer boundaries.
- Runtime regression tests must execute without private strategy inputs or optional signing dependencies.

| ID | Invariant |
|---|---|
| V1 | Invalid bars never reach adapters; invalid actions never create reservations or attempts. |
| V2 | Intent and transport acceptance are not broker outcome evidence. |
| V3 | Every command has an authorized leg/symbol and persisted, unambiguous target scope. |
| V4 | Uncertainty preserves its reservations and obligations across restart. |
| V5 | One source occurrence binds one operation and one resolved scope across redelivery. |
| V6 | Incident authority cannot be overwritten by activation, callbacks, or replay. |
| V7 | Qualified timing, rounding, FIFO, and protection-owner behavior remain unchanged. |

## 2. Responsibilities and interfaces

Runtime owns source validation, complete-bar sequencing, and stable action occurrence provenance. Validate bars before recording a partial or calling adapters. Validate the entire emitted batch before journaling it as dispatchable or sending its first member. A valid recorded input boundary may precede discovery of invalid adapter output; that failure must remain explicit and recovery must not invent a valid action batch.

Account owner owns action admission, state-dependent scope resolution, authorization, and the durable transition. Validate direct callers as well as runtime-produced actions. Resolve and bind targets under the serializer before send. The command and attempt journal must preserve the full admitted action.

Capacity reducer owns reservations and confirmed execution accounting. It does not infer broker positions, working orders, protection, or cancellation from transport state.

Protection state separates desired protection, original protection owner, observed broker protection, and execution allocation. A protection owner can remain live after FIFO consumed its originating lot. A surviving lot whose protection was consumed does not authorize resurrecting that order. First attachment is eligible only for a never-protected surviving lot; amendments address live authorized protection owners.

Proposed interfaces are introduced within these owners, not through new external endpoints. Slice A's exact proposed interfaces are specified in the [implementation plan](../superpowers/plans/2026-09-16-pr409-ingress-correction.md). Later slices must finalize their type/schema definitions against this contract before implementation.

## 3. Occurrence and attempt identity

Use separate identities for source occurrence, admitted operation, and potentially effective transport attempt.

The runtime occurrence key is account/session/completed-boundary/action-ordinal. It must be reproducible from the retained deterministic batch. Internal scheduler/takeover producers retain their own stable event identities. Scope is a binding beneath the occurrence key, not a changing ingredient that can manufacture another occurrence.

On redelivery, look up the occurrence before resolving current inventory. Identical source content reuses the original binding and result; conflicting content under the same key is an identity incident. One unresolved protection operation defers another modification of that owner. Retaining a superseding desire does not authorize dispatching it later automatically. Reconciliation must be followed by a newly evaluated, currently authorized occurrence.

Unchanged observed protection is not re-sent. In particular, do not reset an active trailing anchor. A definitively rejected amendment may be proposed again at a later boundary only when evidence confirms the old protection intact and current authorization permits the change. Content equality alone is neither a permanent dedupe key nor retry authority.

## 4. Protection evidence and outcome classification

The synthetic producer must supply explicitly scoped evidence with account/epoch, immutable fact identity, operation/broker-order linkage, original protection owner, observed parameters and quantity, observation time, and completeness. Absence requires a complete declared scope; incremental order observations cannot prove an empty account or scope. Evidence must causally postdate the operation it resolves and satisfy the existing applicable freshness requirement. Conflicting/replayed facts cannot renew currency.

No accepted production evidence producer is claimed by this design. Synthetic tests exercise the stated interface; missing live capabilities remain a qualification blocker.

| Outcome | Required behavior |
|---|---|
| Accepted and awaiting evidence | Pending, not working. Retain the confirmation deadline. |
| Qualified working-order evidence | Update observed protection and resolve the matching obligation. |
| Rejected first attachment | Protection gap; durable intervention, no automatic recovery mutation. |
| Rejected amendment with old protection confirmed intact | Preserve old observed protection and retain refusal. Later authorized occurrence may modify. |
| Unknown outcome, missing expected protection, expired confirmation deadline | Intervention with unresolved ownership retained. |
| Consumed protective order | Remain consumed, including across repeated demands and replay. |

Initial entry-attached protection is due within one bar after the fill. Subsequent attachment/amendment confirmation is due within one bar after preparation. Earlier incident, authority, and evidence fences still apply. An accepted operation awaiting this evidence is distinct from a transport-unknown result; late evidence can update accounting but cannot restore trading permission.

Classify tightening/loosening from confirmed old parameters. Loosening requires risk-add authorization. Unknown old parameters cannot establish that a modification tightens protection. Preserve first-attachment semantics for a lot deliberately entered bare; absence before the strategy defines protection is not itself a gap.

## 5. Takeover transitions

Persist the sequence PLAN -> CANCEL -> CONFIRM CANCELLATIONS -> CLOSE DISPLACED LEGS -> CONFIRM QUIESCENCE -> REVALIDATE ADMISSION.

Publish the entire displaced scope before dispatch. Every displaced resting or partially filled entry/add must have qualifying terminal evidence before takeover closes start. Count fills arriving during cancellation and close whole displaced legs in the required lowest-priority-first order.

Quiescence requires consistent postdating position evidence, complete working-order evidence including protection, and no unresolved scope requests. Never construct zero proof fields because a code path finished. Before admitting Aegis, recheck generation, authority, policy, lifecycle, source/bar validity, evidence freshness, and capacity.

Rejected/unknown/partial outcomes retain real effects and the obligations required by the governing contract; they do not roll back displaced exposure or authorize a duplicate close. Current rev9 incidents revoke runtime mutation authority. Cutoff can retire only the unattempted Aegis request; it cannot clear displaced obligations or erase evidence.

## 6. Approved activation boundary

Synthetic activation is limited to a fresh-account bootstrap. Restart and incident recovery remain blocked until a separately designed recovery protocol exists. This narrows previous unsafe synthetic behavior deliberately; tests must distinguish bootstrap from recovery.

Bootstrap atomically proves a fresh empty owner with no incidents, attempts, positions, protection obligations, or pending work, alongside existing binding/time checks. An already RUNNING call in the same generation may be an idempotent no-op, never a clearing operation. A restart, day change, acknowledgment, or reconciled-looking cache cannot turn INTERVENTION into RUNNING.

Tests of carried-position policy calculations can remain isolated policy/replay tests. They cannot establish authorization to restart trading by invoking the bootstrap helper.

## 7. Migration and recovery

Version new persisted structures explicitly. Preserve old IDs, facts, reservations, and replay history. Do not reinterpret accepted historical amendments as confirmed working protection. Ambiguous legacy protection or operation state remains halted and visible. Migration/replay must never send or silently discard an obligation.

After a new schema is present, deletion or corruption of a required structure is not an old-version migration opportunity. Legacy recognition must be explicit. Replay either reconstructs the recorded state without external effects or fails closed with the missing/corrupt obligation identified.

## 8. Delivery and acceptance

| Slice | Outcome | Gate |
|---|---|---|
| A | Validated ingress and durable failure reporting | Invalid inputs have no downstream effects; valid timing/rounding remain unchanged. |
| B | Protection ownership, evidence, and occurrence identity | No cross-leg mutation, dynamic-scope duplicate, unsafe reissue, or consumed-owner resurrection. |
| C | Evidence-gated takeover | All intermediate cancellation/close/quiescence ordering constraints hold. |
| D | Activation restrictions, migration, integration | Restart/incident/concurrent halt cannot regain authority or resend. |

Detailed implementation begins with independently deliverable Slice A. Slices B-D require interface-level plans before coding; this document fixes their behavior and acceptance conditions rather than pretending their evidence producers already exist.

Acceptance matrix: malformed OHLCV/actions; invalid and stale targets; duplicate source occurrence before/after intervening fill; rejected attach versus intact-old amend; pending versus unknown; consumed owner versus live owner with zero originating inventory; delayed cancellation; late fill; partial/rejected close; cutoff before/after displacement; restart at each durable boundary; halt concurrent with authorization; old-schema migration and new-schema corruption; storage failure while publishing an incident.

Every slice needs failing-before/passing-after evidence and independent review. Correct the prior takeover test's forbidden intermediate expectation with the contract cited. Full acceptance additionally requires operations tests, repository gates, and current CI. Do not add counts from overlapping suites or equate passing synthetic tests with live capability.

Falsifier: if any trace sends before its evidence/authority prerequisites, changes qualified strategy semantics, loses an obligation, or creates fresh-send authority from replay/activation, the correction is not accepted even when its regression suite passes.
