# PR 409 Slice C Evidence-Gated Takeover Implementation Plan

> **For agentic workers:** Execute with superpowers:executing-plans when implementation is authorized; use superpowers:subagent-driven-development only when bounded delegation is authorized. Preserve the behavioral contract and integration owner. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Send a retained Aegis request at most once, only after evidenced cancellation, ordered whole-leg displacement, complete quiescence and current admission.

**Architecture:** Keep the account serializer, owner, SQLite journal, capacity reducer and runtime. Add pure takeover evidence contracts and a takeover owner mixin; extend the independent synthetic broker. Accounting consumes qualified evidence and never produces broker inventory.

**Tech Stack:** Python 3.11 language floor, SQLite, pytest, offline synthetic broker.

**Spec:** [Approved correction, sections 5–8](../../spec/2026-09-16-pr409-bounded-execution-correction.md), [rev9](../../spec/2026-09-14-tb-s3-halt-resume-contract.md), [C/D handoff](2026-09-16-pr409-slices-c-d-handoff.md), [B acceptance](2026-09-16-pr409-protection-correction.md#7-implementation-and-acceptance-record-2026-09-16).

## Global Constraints

- Offline synthetic execution only; no production transport, deployment, arming, or trading.
- No strategy parameters, sizing laws, allocation constants, protection-tier constants, or calibration changes.
- No production resume or general-purpose incident recovery in this correction.
- Preserve immutable historical operation/fact identities and retained obligations.
- Preserve the Python 3.11 language floor and existing repository layer boundaries.
- Runtime regression tests must execute without private strategy inputs or optional signing dependencies.
- Preserve A's exact integer trailing validation and zero-offset rejection, B's original protection ownership, consumed tombstones, FIFO allocations, unchanged anchors and pending-amendment deadlines.

## 1. Status, grounding and integration ownership

Originally a documentation-only proposal grounded at `567a583` on `codex/phase2-four-leg-execution` in the existing `phase2-four-leg-execution` worktree. The user subsequently authorized “implement slice C.” Implementation is now present as local uncommitted changes; section 8 records the as-built interface and acceptance evidence. Sections 2–7 retain the original design and task checklist as planning history. The coordinating implementer owns acceptance of the entire producer → listener/runtime → owner → journal → command → evidence → accounting/feedback trace. No push, deployment or recovery is authorized by this record.

Read on 2026-09-16: owner boot/schema/activation/dispatch/context/observation/takeover; capacity reservation, completion and projection; protection contracts and validation; synthetic receipt/application/execution/read paths; runtime ordinary/protective observation, source validation, continuation and recovery; listener boundaries; policy, sizing and schedule code; current takeover and activation tests; governing specs and B acceptance. No applicable AGENTS.md was found in the worktree or checked parent locations.

Joshua confirmed during this planning session that **Slices A and B are pushed to PR 409**. This supersedes the handoff's unpushed status. Before that update, the local branch was three commits ahead and zero behind the cached tracking ref `fc7cdc7`; `git ls-remote origin refs/heads/codex/phase2-four-leg-execution` failed to connect. That cached comparison does not describe the current remote. The push is operator-reported; current remote SHA and actual-head CI were not independently verified. Existing `tmp-slice-a-*`, `tmp-slice-b-*`, the push ledger and the untracked handoff must remain intact.

| Current boundary | Required correction |
|---|---|
| `_advance_takeover_locked` builds cancel and flat actions in one pass | Publish PLAN, finish cancellation evidence for all displaced entries/adds, then prepare closes |
| Local `Quiescence(..., 0, 0, 0, 0)` | Derive all four counts from complete postdating inventory and retained unresolved work |
| `ProtectionSnapshot` has protection orders and fill positions only | New complete inventory includes entry/add and close remainders and unapplied requests |
| Synthetic `apply(cancel)` records an outcome without removing an entry remainder | Independent working-entry state, cancellation application and terminal evidence |
| Ready takeover skips `size_book_request` | Current admission against a narrowly defined own-reservation view, quantity equality and final total-cap check |
| Runtime protection execution does not resume takeover | Preserve observation-only callback; use explicit qualified inventory continuation |
| Capacity completion removes the takeover pointer | Durable owner phase journal survives completion, retirement and halt |

## 2. Proposed wire contracts and producers

Create `ops/c1_rail/book_takeover.py` containing immutable dataclasses only. Existing `ActionOccurrence`, `ObservedProtection`, `ProtectionSnapshot`, `BrokerFact`, `DispatchResult` and `ExecutionEvent` remain owned by their current modules. Use postponed annotations and TYPE_CHECKING-only imports for owner/runtime types, notably BrokerFact, to avoid an owner → takeover contracts → owner import cycle; runtime validation belongs to the consumer. Use the following exact proposed fields (all IDs are nonempty canonical strings; quantities and sequences are exact integers, excluding bool):

```python
@dataclass(frozen=True)
class WorkingOrder:
    broker_order_id: str
    operation_id: str
    leg_id: str
    order_symbol: str
    kind: str                 # entry, add, exit, flat
    remaining: int            # strictly positive working remainder

@dataclass(frozen=True)
class InventoryPosition:
    fill_id: str
    operation_id: str
    leg_id: str
    order_symbol: str
    side: str
    remaining: int            # strictly positive; gross, never netted

@dataclass(frozen=True)
class RequestOutcome:
    operation_id: str
    attempt_id: str
    target_operation_id: str | None
    status: str               # pending, applied, rejected, unknown
    terminal_fact_id: str | None

@dataclass(frozen=True)
class InventoryRead:
    read_id: str
    occurrence: ActionOccurrence
    scope_legs: tuple[str, ...]
    prepared_at: datetime
    after_sequence: int       # last accepted sequence for this stream

@dataclass(frozen=True)
class AccountInventory:
    fact_id: str
    account: str
    account_epoch: str
    stream_id: str
    sequence: int
    read_id: str
    as_of: datetime
    scope_legs: tuple[str, ...]
    complete: bool
    positions: tuple[InventoryPosition, ...]
    working_orders: tuple[WorkingOrder, ...]
    protection: ProtectionSnapshot
    requests: tuple[RequestOutcome, ...]
    facts: tuple[BrokerFact, ...]
```

`facts` contains immutable fill/terminal events needed to bring accounting to the inventory's watermark, including causal fills preceding a terminal. It is not a replacement for existing protective `ProtectionExecution` events: those travel through their existing atomic FIFO path before a dependent inventory can qualify. Missing executions cause a wait/refusal, never synthetic allocation. `protection` must be a coherent snapshot of the same broker state, account/epoch/scope/time; its separate existing stream cursor is validated by B. Broker inventory stream sequence and owner capacity event sequence are separate namespaces.

Proposed producer APIs on `SyntheticProtectionBroker`:

```python
read_inventory(request: InventoryRead) -> AccountInventory | None
apply_cancel(operation_id: str, *, at: datetime) -> tuple[BrokerFact, ...]
execute_close(operation_id: str, *, execution_id: str, quantity: int,
              price: float, terminal: bool, at: datetime) -> tuple[BrokerFact, ...]
```

Extend existing `apply` so applied entry/add creates a working remainder and applied cancellation delegates to `apply_cancel`. Retain `execute_entry` compatibility: a fill itself establishes application and subtracts from independently tracked intended quantity. Receipt alone creates an unresolved provider request, not a working order or fill. Cancellation application removes the unfilled remainder, forbids subsequent new fills, and emits the target's terminal with exact cumulative fills. A fill applied before cancellation but delivered later remains deliverable with its original identity. Cancelling an already fully filled target returns its retained filled terminal; it does not invent a cancelled result. Cancellation rejection leaves the order working. Unknown transport remains an unresolved local attempt and revokes authority even if the producer later reports an effect.

`execute_close` uses existing explicit prices/FIFO lots and reduces only the requested quantity. A nonterminal partial fill leaves the remainder working; terminal partial/rejected completion retains residual position. Full close application may use this API internally. Never delete a separate pending protection amendment merely because close/protective execution consumed its owner. Residual/orphan protection remains visible until producer evidence actually removes it; no automatic orphan cleanup command is introduced.

`read_inventory` snapshots `_lots`, working entry/close orders, protection and request outcomes at one synthetic instant. It must not query the owner, desired scopes, capacity or reservations to construct state. Scope filtering is allowed; manufacturing omitted state is not. Request outcomes include retained applied/rejected resolutions and pending received requests, even those with no working order. Inventory tests must also model an unexpected external working order and a pending provider request. Unknown identities fence admission rather than being silently filtered out.

Proposed consumers:

```python
# BookAccountOwner / new TakeoverOwnerMixin
prepare_takeover_inventory(*, now: datetime) -> InventoryRead | None
observe_takeover_inventory(snapshot: AccountInventory, *, now: datetime
                           ) -> tuple[ExecutionEvent, ...]
# BookRuntime
observe_takeover_inventory(snapshot: AccountInventory, *, now: datetime
                           ) -> tuple[ExecutionEvent, ...]
# c1_rail_listener.py
handle_book_takeover_inventory(snapshot: AccountInventory, runtime: BookRuntime,
                              *, now: datetime) -> tuple[ExecutionEvent, ...]
```

The owner observation API validates and commits evidence/feedback only. The runtime serializes adapter feedback, then invokes existing `resume_takeover(now=now)`, which rechecks send authority. A read may finish after halt; accounting can still update, but continuation sends nothing. A protection-only read or execution callback never independently establishes takeover quiescence. Recovery replays feedback without invoking continuation.

## 3. Schema 3 and immutable scope

C creates fresh schema **3**, recognizes current 3 strictly, and refuses 1/2 with an explicit migration-required error. It does not run D conversion implicitly. Keep all schema-2 tables/columns unchanged. Add these tables centrally in `book_account_owner._SCHEMA`:

```sql
CREATE TABLE takeover_plans (
  operation_id TEXT PRIMARY KEY, occurrence_key TEXT NOT NULL UNIQUE,
  body TEXT NOT NULL
);
CREATE TABLE takeover_events (
  event_id TEXT PRIMARY KEY, operation_id TEXT NOT NULL,
  ordinal INTEGER NOT NULL, kind TEXT NOT NULL, body TEXT NOT NULL,
  UNIQUE(operation_id, ordinal)
);
CREATE TABLE takeover_children (
  operation_id TEXT PRIMARY KEY, takeover_id TEXT NOT NULL,
  occurrence_key TEXT NOT NULL UNIQUE, kind TEXT NOT NULL,
  target TEXT NOT NULL, body TEXT NOT NULL
);
CREATE TABLE takeover_reads (
  read_id TEXT PRIMARY KEY, operation_id TEXT NOT NULL, body TEXT NOT NULL
);
CREATE TABLE takeover_inventory (
  fact_id TEXT PRIMARY KEY, stream_id TEXT NOT NULL, sequence INTEGER NOT NULL,
  body TEXT NOT NULL, disposition TEXT NOT NULL,
  UNIQUE(stream_id, sequence)
);
CREATE TABLE takeover_streams (
  stream_id TEXT PRIMARY KEY, body TEXT NOT NULL
);
```

Every JSON body has `record_version: 1` and canonical serialization. Required keys are validated on boot and before replay. Plan body contains account/epoch/session/boot/generation; root action and occurrence; original quantity and sizing request/binding witness; ordered displaced legs from `capacity.takeover.displaced`; every known displaced entry/add operation ID, fill ID and protection owner ID; unresolved request IDs; capacity sequence at publication; creation time; source boundary/action digest and expiry. This is the full leg-wide scope, not just the initial fills. Later fills of frozen entry IDs belong to that scope. A newly discovered unrelated order is an incident, not permission to expand children.

Events contain previous phase, next phase, time, generation, evidence IDs, capacity sequence and reason. Phases: `PLAN`, `CANCEL`, `CONFIRM_CANCELLATIONS`, `CLOSE_DISPLACED`, `CONFIRM_QUIESCENCE`, `REVALIDATE`, `ATTEMPTED`, `RETIRED`. HALT is an append-only fence event preserving the unfinished phase; it does not erase obligations. Child body binds action, scope, original occurrence, preparation time and generation. Use `make_occurrence('takeover', root_id + ':cancel:' + target_id)` or `root_id + ':close:' + leg_id` as stable event IDs; store the resolved operation ID before dispatch. No second child for a target on redelivery.

The transaction that records the capacity takeover and root operation must also publish PLAN; a crash cannot leave an actionable capacity takeover without a plan. Before first cancellation, require a post-PLAN complete inventory agreeing with the frozen scope and local journal. Publish all cancellation children before any send. After all cancellations qualify, freeze the actual close FIFO scope (including late fills) and close child identities before sending the first close. Child attempts use existing `attempts` uniqueness and occurrence machinery.

Stream body records account/epoch, accepted sequence, fact identity and acquisition time. Duplicate identical evidence does not advance freshness. Same identity/sequence with different content is an incident. Missing tables, plans, child references, original occurrence, proof evidence or stream records in schema 3 are corruption: fail closed, never backfill them on boot. Schema validation must cross-check capacity completions against takeover proof events. D's recognized schema-3 contract is this entire section, subject to reconciliation with C's eventual committed implementation.

## 4. Phase gates and replay

| Phase and trigger | Transaction and gate | Observable next command |
|---|---|---|
| PLAN after capacity displacement decision | Save full scope; request complete initial inventory; reconcile accounting and unknown state | None until inventory qualifies |
| CANCEL | Persist all cancellation child bindings for nonterminal displaced entry/add targets; recheck authority before each attempt | Each cancel at most once |
| CONFIRM_CANCELLATIONS | Every target has qualified filled/cancelled/rejected terminal and cumulative fills agree; associated cancel request outcome is resolved | No flat while any target/request remains unresolved |
| CLOSE_DISPLACED | Scope includes all confirmed late fills; follow retained priority order, one leg at a time | Whole-leg close; next leg only after prior close terminal and zero evidenced gross |
| CONFIRM_QUIESCENCE | Complete postdating inventory, local reconciled zero exposure, no working/protection/pending requests in frozen legs | None while any count or obligation remains |
| REVALIDATE | Save proof and capacity completion atomically, then revalidate retained request immediately before attempt under serializer | Exactly one Aegis attempt or durable refusal |
| RETIRED / HALT | Preserve children, evidence, allocations, pending obligations and feedback | No takeover sends; separately authorized schedule may own ordinary scheduled work |

For cancellation, a receipt or `applied` string alone is insufficient. Require target terminal linked to the known operation and matching attempt/request outcome. Apply causal fills before terminal. An out-of-order envelope lacking those fills is retained as unqualified and produces no phase advance; a later complete envelope can supply the missing facts. Conflicting cumulative quantities or impossible identity is an incident. Do not feed a known incomplete envelope into `_observe_locked` and then treat its induced capacity block as resolved.

Inventory qualifies only when complete, exact declared scope, unique IDs, valid symbols/sides/quantities, registered synthetic stream/account/epoch, and current read ID match. Require `snapshot.as_of > read.prepared_at`, `sequence > read.after_sequence`, nonfuture time, age within existing `MAX_FACT_AGE` and binding `max_evidence_age`, and valid binding expiry. The read is prepared after the latest scope mutation preparation and all events it must settle. Use a new read if another mutation intervenes. Require gross positions/FIFO remainder agreement with accounting and no unconsumed causal event gaps. Validate the nested B snapshot and journal requests in the same transaction; invalid later members must not leave earlier applied accounting behind. Refactor observation internals to accept the existing transaction where necessary; do not open nested independent commits.

Persist quiescence evidence IDs, read ID, inventory sequence/time, local journal sequence and explicit lists used for each count. `gross` sums position quantities; `working` counts risk/close working orders; `protection` counts nested protection orders; `pending` is the union of provider pending/unknown requests and local unresolved operations/attempts/protection obligations for the scope. Local accepted ordinary entry/cancel/close attempts resolve only through their established terminal linkage. Never count all historical attempts as pending, and never drop an unresolved amendment on a consumed owner. Construct existing `Quiescence` with the next capacity event sequence only after these derived counts are zero; its sequence is a reducer ordering field, not broker evidence. Store `CompleteTakeover` and the referencing proof event in one transaction.

Partial/rejected terminal close with remaining exposure cannot advance the leg or authorize another child. Record a takeover execution incident and retain residual scope for intervention. Unknown outcomes immediately revoke authority. Nonterminal partial close may wait with its working remainder and reservation intact. Orphan protection or unknown request prevents quiescence; a qualified inconsistency/protection deadline follows existing incident rules, never a cleanup send.

Cutoff retires only unattempted Aegis. Call existing schedule classification before takeover progression, preserve effects already made and all unresolved requests, and let scheduled operations use their existing occurrence/authority and close reservations. Takeover must neither race a new scheduled close nor clear its obligations. Before any displacement, retirement sends no takeover controls. After displacement it does not undo fills or cancel history. Incident/early expiry leaves INTERVENTION and permits observation only.

Replay validates durable phase/event order, reconstructs accounting/obligations and feedback, and never calls transport. Crash after PLAN/child preparation/attempt/pre-send/send/application/evidence/proof/retirement requires a new boot that is HALTED/INTERVENTION. An existing UNKNOWN attempt is never retried. Same-process redelivery can continue only unattempted children in the retained boot/generation with current prerequisites. Failed incident storage sets the existing process send-suppression latch; do not claim a durable fence that failed to commit.

## 5. Final admission without a new reservation

Propose `_revalidate_takeover_db(db, operation_id: str, *, now: datetime) -> str | None` on the takeover mixin: `None` permits the retained attempt; a reason becomes a durable local refusal, or an incident where rev9 requires one. This helper performs no transport and no new reservation.

1. Validate current actor boot, generation, RUNNING/NORMAL, input-send latch, schedule, deadlines, settlement attachment/seal, policy identity, lifecycle, session/calendar/binding and expiry. Recheck occurrence content, original source and retained action through shared validators.
2. For runtime sources require the complete retained four-leg boundary and ordinal/action digest to agree, current runtime identity, and `bar_time <= now <= bar_time + BAR_PERIOD + BAR_SLACK`. Direct synthetic sources must have an explicit valid action `bar_time` and the same bounded expiry, captured in PLAN; missing source timing refuses takeover. Do not invent a bar or refresh the original time. Source invalidation/stale individual signal refuses the root; unhealthy feed, expired barrier or invalid identity invokes the existing account incident rule. Run the existing source-silence/deadline checks before continuation; evidence receipt is not a heartbeat. These are offline checks, not a claim of authenticated live source-health support.
3. Rebuild current `_context` from actual policy, settlement, lifecycle, binding and capacity. After evidenced `CompleteTakeover`, the exact root reservation is active and appears in its own pending list/exposure. Create a pure validation view subtracting **only its retained unfilled quantity** from its leg's reserved exposure and removing **only its own operation ID** from pending IDs. Require its unique reservation, unchanged identity/quantity, zero fills and no attempt. Do not clear any blocks, foreign reservations or protection obligations. Before capacity completion this view is forbidden.
4. Call existing `size_book_request` with the original request, current view/binding/policy. Require no halt, positive quantity and `decision.qty_out == retained quantity`; changed sizing means refusal, never resize. Independently check actual used micro including the root reservation against the unchanged account cap and leg allocation. Require no other uncertain mutation or unqualified inventory update since proof.
5. Under the same serializer, persist the decision witness and existing attempt record before invoking transport. Recheck prerequisites at the actual attempt boundary if the implementation releases a transaction between admission and attempt. No clock/evidence renewal from replay. Preserve refusal feedback once using existing feedback machinery.

The own-reservation view is derived exclusively from verified journal rows. It is not a fabricated flat account and cannot be reused to obtain a second reservation. Unit tests must leave a second reservation and an unrelated block in place to prove this boundary.

## 6. Implementation tasks and acceptance

Each task is a reviewable behavior; the coordinator remains the integration owner. Every code task starts with a failing test, records the failure, implements only its contract, reruns affected tests, and receives review before an authorized commit. Implementation authorization is separate from this documentation request.

### C1 — independent producer and schema boundary

**Files:** create `ops/c1_rail/book_takeover.py`, `tests/ops/test_book_takeover_phases.py`; modify `book_synthetic_protection.py`, owner schema/boot; extend `tests/ops/test_book_protection_producer.py` and schema tests. If adding runtime imports, update both image copy inventories identified by `tests/ops/test_c1_signal_daemon_image_manifest.py` and `test_c1_rail_image_manifest.py`.

**Interfaces:** produce the exact contracts and producer methods in section 2 and schema 3 in section 3. Consume existing command/occurrence and FIFO/protection primitives.

- [ ] Write producer tests that send an entry of quantity 3, execute 1, receive a cancel, and read: receipt leaves 2 working; applying one late fill leaves 1; applying cancel yields cumulative terminal 2 and no entry remainder. Redelivering the terminal changes nothing; a new fill after cancel is rejected by the producer.
- [ ] Run those tests and record baseline missing-capability failures. Separately change the existing async takeover expectation locally to assert no flat before terminal; record its behavioral failure before implementing owner changes.
- [ ] Implement independent working/request state and exact inventory snapshots; preserve current B API behavior. Add partial-close and orphan-protection stimuli; prove account state is not an input to reads.
- [ ] Implement fresh schema 3, strict current validation and nonmutating legacy refusal. Test each missing required table, conflicting stream row and missing plan/child reference.
- [ ] Run producer, evidence, lifecycle and new schema tests; retain exit codes and review the diff. Commit only under implementation/integration authorization.

Illustrative assertion in the existing lifecycle regression (retain its real fixture/action setup):

```python
controls, completed = account.advance_takeover(now=NOW)
assert not completed
assert all(command.kind != 'flat' for command in broker.commands)
```

The decisive baseline falsifier is absence of flat while the displaced entry lacks terminal evidence; retain the existing fixture's real action and operation identities.

### C2 — durable cancellation and ordered close progression

**Files:** create `ops/c1_rail/book_takeover_owner.py`; modify owner dispatch/takeover/observation internals and synthetic producer; extend `test_book_takeover_phases.py` and `test_pr409_owner_lifecycle.py`.

**Interfaces:** mixin provides existing `advance_takeover`/`resume_takeover` behavior plus section-2 owner inventory methods. Consume schema-3 evidence, existing capacity reducer and occurrence/attempt uniqueness.

- [ ] Write the receipt-without-terminal, late partial fill and duplicate terminal traces using the stateful producer; assert phase rows, exact command prefix and reserved quantities at each step.
- [ ] Run and retain failing evidence. Implement atomic PLAN/children and cancellation qualification before any close preparation.
- [ ] Write mixed ORB/Vanguard/Striker displacement tests deriving required whole legs from actual capacity, and assert close order matches retained lowest-priority-first scope. Deliver previous-leg terminal and fresh zero-position inventory before allowing the next leg.
- [ ] Implement close progression; test nonterminal partial wait, terminal partial/rejected intervention, unknown transport, late evidence after halt, FIFO feedback once and no duplicate child after redelivery.
- [ ] Test fault injection before/after each phase and attempt transaction plus halt between children. Run existing ordinary close, occurrence, protection and schedule suites to detect scope/obligation regressions; review before authorized commit.

### C3 — quiescence, final admission and runtime integration

**Files:** takeover owner/contracts, owner context/dispatch, `book_runtime.py`, `c1_rail_listener.py`, `book_evaluate_loop.py` if continuation/deadline wiring requires it; `test_book_takeover_phases.py`, `test_book_runtime_occurrences.py`, `test_pr409_owner_lifecycle.py`, `test_pr409_review2.py`, `test_pr409_review3.py`.

**Interfaces:** listener/runtime use the section-2 inventory path and existing feedback checkpointing; owner uses section-5 helper. Idle processing requests/consumes inventory through the explicit synthetic test seam and checks current deadlines; no automatic production polling/transport is added.

- [ ] Write a trace where all local exposure is zero but a producer orphan order or a consumed owner's pending amendment remains: no completion or Aegis attempt.
- [ ] Parameterize incomplete, stale, future, equal-time, foreign account/epoch/scope, position-only, mismatched FIFO and unknown in-flight request inventory. Assert no manufactured proof and retained obligations.
- [ ] Implement atomic evidence qualification, proof references and `CompleteTakeover`. Test reordered causal facts, duplicate snapshot without freshness renewal and rollback on an invalid final member.
- [ ] Write final-admission cases invalidating each of generation, authority, policy, lifecycle, source/bar, settlement, binding currency, uncertainty and capacity after displacement. Assert root refusal/incident as appropriate and no second reservation. Implement section 5.
- [ ] Exercise the real listener/runtime path: qualify cancellation → close/fill/feedback → postdating inventory → one Aegis send → duplicate delivery → no second send. Include cutoff before and after displacement and halt between proof and attempt.
- [ ] Verify every durable crash boundary yields read-only restart, preserving IDs, FIFO and feedback checkpoints. Inject real SQLite incident-write failure and prove sends remain suppressed after storage access returns.
- [ ] Run the acceptance commands in section 7 and obtain independent integrated review when implementation is authorized. Record C's committed schema contract for D, without calling combined A–D complete.

## 7. Verification and D handoff

Use the targeted/full commands from [handoff section 6](2026-09-16-pr409-slices-c-d-handoff.md#6-verification-and-handoff-discipline), adding `tests/ops/test_book_takeover_phases.py`. Set `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, `PYTHONUTF8=1`, use the installed Python 3.13 path and `-p no:cacheprovider`; record each exit code immediately. Run new synthetic tests with optional signing imports blocked and without private inputs. Run both image manifest suites/image validation and `scripts/gate_manifest.py --tier check`. Do not combine overlapping test counts. Python 3.11 syntax validation is not a Python 3.11 execution result.

Acceptance requires evidence of every intermediate gate in sections 4–6, passing affected/full suites and independent review. C's final commit must supply D with exact schema definitions, record codecs/validators, phase/child/stream semantics, new and inherited crash cuts, immutable fixture exports, unresolved obligation examples and any change from this proposed interface. D must reconcile its separate provisional plan before implementation.

Documentation self-review checked the critical compositions: pending receipt cannot yield cancellation proof; late fill enters frozen leg scope before close; terminal close cannot erase a pending amendment; own-reservation revalidation cannot reserve again; retirement retains displacement; restart cannot restore authority. This is a design trace, not executed acceptance. No runtime tests were run for this documentation-only change.

## 8. Slice C implementation record — 2026-09-16

The later user instruction authorized Slice C implementation. C1–C3 are implemented locally against `567a583`; no Slice D bootstrap or migration implementation is included. The original checklists above describe the planned work, while this section records the delivered contract. No commit or push has been made for C.

### Delivered behavior

`book_takeover.py` defines immutable inventory/read/position/working-order/request contracts. `SyntheticProtectionBroker` independently retains working remainders, terminal outcomes, fills, close allocations and protection state. Receipts do not apply cancellation. Duplicate close executions are rejected before producer mutation. The listener and `FourLegRuntime.observe_takeover_inventory` deliver complete evidence through the existing serializer and feedback checkpoints.

`book_takeover_owner.py` freezes the retained request and displaced scope, journals cancellation children before sends, waits for target terminal evidence, and closes whole legs in lowest-priority-first order. Each subsequent close requires the previous leg's terminal and zero-position evidence. Partial terminal, rejected and unknown controls preserve effects and revoke authority. Quiescence includes independent positions, all working order kinds, protection orders and the union of provider/local unresolved requests, including consumed protection owners with pending amendments.

Inventory validation binds producer stream, read identity, scope, sequence, freshness, postdating and the account mutation marker. Contained facts and already-delivered facts must predate the inventory. Causal incompleteness is retained as immutable unqualified evidence; contradictory terminal quantities and conflicting retained fact identities are incidents. Fact application, FIFO/protection reconciliation and inventory qualification share one SQLite transaction with rollback on an invalid member. Late evidence after halt may update accounting; independent boot/generation/permission checks prohibit renewed sends.

Final admission checks the retained proof and unchanged binding, current lifecycle/settlement/sizing/capacity, original source timing, complete runtime source boundary and actor identity. Its sizing view removes only the existing root reservation. It creates no second reservation and journals at most one root attempt. Cutoff retirement keeps displaced effects and obligations. Storage failures latch local send suppression.

### Schema 3 contract for D

The authoritative SQL is `_SCHEMA` in `book_account_owner.py`; body encoding is the existing canonical `_body` through the mixin's `_dump`. Current boot invokes `_validate_takeover_state_db`. Versions 1 and 2 are refused without mutation; missing/corrupt current structures are not repaired or migrated.

| Table | Identity and retained meaning |
| --- | --- |
| `takeover_plans` | Root operation primary key and unique occurrence key; record version 1 freezes account/epoch/boot/generation/session, action/occurrence/quantity, ordered displaced legs, active target operations, all historical scoped operations, fills/owners/unresolved identities, request and admission binding, runtime actor and creation/capacity witnesses. |
| `takeover_events` | Event primary key and unique root/ordinal pair; previous-kind chain, time/generation/capacity witness, published children and proof references. |
| `takeover_children` | Operation primary key and unique occurrence key; root, kind, target and immutable action/occurrence/preparation witness. Cancel target is an operation; flat target is a leg. |
| `takeover_reads` | Read primary key and root; versioned request plus expected producer stream and prepared mutation marker. |
| `takeover_inventory` | Fact primary key and unique stream/sequence; immutable snapshot, root and qualification disposition. Qualified records retain mutation witnesses. |
| `takeover_streams` | Stream primary key; latest qualified fact and sequence cursor. Duplicate delivery does not renew freshness. |

The legal phase chain is `PLAN → CANCEL → CONFIRM_CANCELLATIONS → CLOSE_DISPLACED → CONFIRM_QUIESCENCE → REVALIDATE → ATTEMPTED`. `HALT` is a retained incident event without permission to advance; `RETIRED` terminates an unattempted root. Cancellation preparation and its confirmation phase commit together; quiescence and revalidation proof commit together. Proof events link exact inventory/read IDs, zero derived counts and mutation marker. Capacity completion and proof publication are atomic.

Synthetic durable cuts are `takeover:PLAN`, `takeover:CONFIRM_CANCELLATIONS`, `takeover:CLOSE_DISPLACED`, `takeover:REVALIDATE`, `takeover:ATTEMPTED`, `takeover:RETIRED`, plus inherited `after_reservation`, `before_send`, `after_send`. Tests exercise phase and child/root attempt boundaries; restart remains HALTED/INTERVENTION and does not replay sends. The stateful `TakeoverScenario` and consumed-owner/mixed-leg/cutoff tests are reproducible offline fixtures for D. They retain actual operation, occurrence, fill, attempt and proof identities rather than manufactured flat snapshots.

D must reconcile its provisional plan against this actual schema and the eventual committed C revision. Conversion, fresh-bootstrap recognition and combined A–D acceptance remain D work. This local record is not a committed migration contract or remote CI result.

### Review and verification

Independent integrated review accepted C after fixes for duplicate producer mutation, retained unqualified identity, ordinary cancellation history, causal postdating, required plan fields, complete runtime source validation, contradictory terminal facts and late accounting after halt. The reviewer independently ran 65 cases and `git diff --check`; three later storage/schema cases brought the local C suite to 68 passing cases. Production code did not change after that review.

Failing-before logs are retained in `tmp-slice-c-red.txt`, `tmp-slice-c-phases-red.txt` and `tmp-slice-c-journal-red.txt`. Final acceptance results follow below. These are local Python 3.13.2 executions with plugin autoload disabled, UTF-8 enabled and no pytest cache provider. Python 3.11 syntax checking does not establish execution on Python 3.11.

| Final check | Result | Evidence file |
| --- | --- | --- |
| Slice C regression suite | 68 passed; exit 0 | `tmp-slice-c-phases-final.txt` |
| Full `tests/ops` suite | 2547 passed, 15 skipped, 2 warnings; exit 0 | `tmp-slice-c-ops-final.txt` |
| C/protection/ingress/emulator with `cryptography` and `nacl` imports blocked | 220 passed; exit 0 | `tmp-slice-c-no-signing-final.txt` |
| Both image manifests and image-validation script tests | 23 passed; exit 0 | `tmp-slice-c-packaging-final.txt` |
| `scripts/gate_manifest.py --tier check` | exit 0 | `tmp-slice-c-gates-final.txt` |

Counts overlap and must not be added. Gates report absent private Pine/heavy/data inputs; those inputs were not verified. Boundary checking parsed 570 first-party modules under Python 3.13.2 with the 3.11 syntax floor. Packaging checks validate import closure and the harness; no deployment or live execution was performed.

The full-suite skips are unavailable private adapter ports/effective inputs; its two warnings are existing seaborn pending deprecations. Final tracked diff whitespace check passed. A/B push status remains operator-reported; this execution did not verify remote PR-head CI. Slice C is ready for local review/integration, while Slice D and combined correction acceptance remain outstanding.
