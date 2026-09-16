# PR 409 Slice B protection ownership and evidence Implementation Plan

> **For agentic workers:** Execute with superpowers:executing-plans; use superpowers:subagent-driven-development when bounded delegation is useful and authorized. Preserve the behavioral contract and integration owner. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Bind protection demands to their source occurrence and immutable protection owners, and change working-protection state only on qualified synthetic broker evidence.

**Architecture:** Retain `BookAccountOwner`, its account serializer, SQLite journal, capacity reducer, adapter protocol and emulator semantics. Add a pure protection contract/reducer, versioned owner-owned state, and an independently stateful offline evidence producer. Runtime/internal callers own occurrence provenance; the account owner owns scope resolution, admission, persistence and sending.

**Tech Stack:** Python 3.11-compatible dataclasses, SQLite and pytest; standard library only for new runtime code.

**Spec:** [Approved bounded correction](../../spec/2026-09-16-pr409-bounded-execution-correction.md), sections 2–4 and Slice B; [rail primitives/K2 contract](../../spec/2026-09-12-c1-multi-leg-rail-extension-spec.md), subject to the [rev9 intervention override](../../spec/2026-09-14-tb-s3-halt-resume-contract.md).

**Status:** IMPLEMENTED locally following the user's 2026-09-16 instruction to complete Slice B. The design below records the approved execution baseline; section 7 records the implementation, verification and remaining slice boundaries. No push, deployment or production activation is included.

## Global Constraints

- Offline synthetic execution only; no production transport, deployment, arming, or trading.
- No strategy parameters, sizing laws, allocation constants, protection-tier constants, or calibration changes.
- No production resume or general-purpose incident recovery in this correction.
- Preserve immutable historical operation/fact identities and retained obligations.
- Preserve the Python 3.11 language floor and existing repository layer boundaries.
- Runtime regression tests must execute without private strategy inputs or optional signing dependencies.
- Preserve Slice A's numeric ingress contract, including rejection of zero trailing offset. No clamping, private-port edit or validator relaxation belongs to B.

## 1. Grounding and scope

Integration owner: the coordinating implementer of PR 409. Contributors may own bounded work; only the coordinator accepts producer → listener → owner → retained binding → command → evidence → feedback behavior.

Draft baseline: local `c8476c8`, following implementation `26636b8`, on `codex/phase2-four-leg-execution` in `.worktrees/phase2-four-leg-execution`. Refresh remote head and inspect intervening changes before execution; preserve these locally accepted Slice A commits and collaborators' work.

Production code read before drafting: `book_account_owner.py` (schema/boot, `_context`, dispatch, observations, schedule/takeover); `book_policy.py`; `book_capacity.py` (reductions and allocation); `book_runtime.py`; listener `handle_book_action`/`handle_book_fact`; `book_protocol.py`; emulator `_amend`, `_rounded`, `_fill_exit`, `_close_scope` and trailing state. No sizing/protection-policy constants change.

| Existing behavior | Required correction |
|---|---|
| Intent ID is `order_id`; control ID hashes serialized content | Occurrence identity independent of content, with one retained resolved scope/result |
| `BracketAmend` uses generic control admission | Validate every original protection owner and its leg/symbol before any child send |
| `protection_state` stores session mode/cancel IDs | Preserve its meaning; add separate order-level protection ownership/evidence |
| `BrokerFact` only carries fills/terminals; synthetic route dequeues results | Supply a real synthetic working-order evidence producer |
| Any facts on an amendment result can mark it observed | Only linked, postdating evidence of effective protection can resolve it |
| Emulator keeps live sibling protection after its original lot is FIFO-exhausted | Separate owner, lot remainder, executable quantity and trailing state |
| Owner close-fill path requires a prepared ordinary close reservation | Add protective-execution evidence carrying triggering owner and actual FIFO allocations |
| Schema 1 has an inferred feed-watch migration | Explicit new-version recognition; missing new structures are corruption |

B owns protection, occurrence provenance and the minimum schema boundary needed for that durability. C still owns takeover sequencing/full quiescence. D owns legacy migration, fresh-only activation and combined acceptance. The existing activation helper is not made safe by B: do not use it to resume an incident/restarted owner in tests or claim full V6 acceptance.

## 2. Interfaces and durable contract

The types and signatures below are implemented by this slice. Public immutable types and pure transition/normalization helpers go in new `ops/c1_rail/book_protection.py`. SQLite access remains in the account owner. Keep adapter action dataclasses unchanged.

### 2.1 Occurrence provenance

```python
@dataclass(frozen=True)
class ActionOccurrence:
    account: str
    account_epoch: str
    session_id: str
    producer: str       # runtime | schedule | takeover | mode | direct
    event_id: str       # stable producer-owned event/boundary
    ordinal: int        # exact nonnegative integer

# Changed owner and listener APIs.
def dispatch(self, action: Action, *, occurrence: ActionOccurrence | None = None,
             now: datetime) -> DispatchResult: ...
def handle_book_action(action, owner, *, occurrence=None, now): ...
```

The key includes all six fields. Account epoch persists across boots; acquisition time/boot ID cannot replace an occurrence. Invalid actions still follow Slice A before serialization. Valid actions without occurrence are refused as `source_occurrence_required`, before operation, reservation, attempt or send. No random/content-hash fallback authorizes executable controls.

| Actual producer | Stable identity source |
|---|---|
| Runtime barrier | Session + completed `bar.ts` + ordinal in the retained sorted complete batch, including `set_mode` outputs |
| Standalone mode transition | Persisted mode-transition event and child ordinal |
| Schedule | Persisted session/phase/root event and child ordinal; each newly justified remainder has a retained new event |
| Takeover | Existing retained takeover request + retained phase/child ordinal; change provenance, not C's phase ordering |
| Direct Python harness | Caller-retained event ID supplied explicitly on every delivery |

Commit runtime actions and occurrence envelopes together before first dispatch. Freeze cancel-all children before expansion. Audit every producer using `rg 'handle_book_action|\.dispatch\(|_dispatch_locked\(' ops tests`; classify each caller rather than patching only runtime.

Under the serializer, look up occurrence **before** resolving current inventory. Equal source/key reuses the original scope/result. Conflicting source under the same key commits an identity incident before reporting refusal. Retain no-op/refused/deferred outcomes too: redelivery cannot acquire a newly eligible scope. A demand deferred behind another operation requires a new occurrence after reconciliation; it is not an automatic queue.

Keep `OrderIntent.order_id` as its operation ID and existing fact linkage. A new occurrence reusing an intent ID never overwrites it or sends again. Derive new control IDs from occurrence, and multi-target child IDs from retained parent/ordinal, never from current scope or source content. Historical IDs remain untouched.

### 2.2 Owners, targets and changed components

```python
@dataclass(frozen=True)
class ProtectionTarget:
    owner_id: str                # stable from originating fill identity
    entry_fill_id: str
    leg_id: str
    order_symbol: str
    side: Side
    quantity: int                # evidenced executable protection coverage
    primitive: str              # attach | amend

@dataclass(frozen=True)
class ProtectionChange:
    target: ProtectionTarget
    desired: Bracket             # original source semantics
    effective: Bracket           # normalized receiver/comparison levels
    changed_components: tuple[str, ...]  # stop | limit | trail
```

Create one immutable owner per **actual entry/add fill**, including partial fills. An accepted unfilled entry has desired intent but no invented fill/owner. Store original fill/operation/quantity, desired revision, observed effective bracket, executable protection quantity, broker IDs, consumed tombstone, trailing-active/anchor, evidence identity/time and pending operation separately from FIFO lot remainder.

`BracketAmend` resolution:

1. Explicit fill IDs name original protection owners. Unknown/foreign leg or symbol refuses the whole demand with a durable semantic incident before any child send. Do not silently discard invalid members.
2. `None` snapshots all live protection owners plus never-protected surviving lots of this leg, in stable creation order. Freeze once; `()` remains explicit no-target.
3. A known consumed owner is never reattached; record `consumed_protection` refusal/no-op. A surviving FIFO lot does not make its consumed bracket “bare.”
4. A live owner with zero original lot remainder remains amendable when fresh evidence proves its executable coverage of residual same-leg position.
5. Attach only to a never-protected surviving lot, with complete fresh evidence proving no executable prior protection and no overlapping unresolved request.
6. An unresolved protection operation or overlapping explicit close defers competing modification. Capture/validate the entire target set before sending any child. Multi-owner sends are not claimed remotely atomic; retain earlier effects if a later child fails.

`None`/empty brackets do not establish working protection. On a never-protected lot an empty definition is a recorded no-op. Removing live components is a state-dependent weakening, not evidence of health. Quantity must match evidenced executable residual coverage; do not substitute adapter-normal entry quantity or original lot remainder, or shrink coverage without proving the corresponding reduction.

Emit only changed components. An unchanged active trail is never resent/reset when the fixed stop changes. Preserve raw desired prices; compare directionally normalized receiver levels. A pure helper may centralize bracket normalization, proved against emulator `_rounded`; do not move entry-trigger normalization before crossing evaluation.

### 2.3 Evidence and producers

```python
@dataclass(frozen=True)
class ObservedProtection:
    owner_id: str
    entry_fill_id: str
    leg_id: str
    order_symbol: str
    broker_order_ids: tuple[str, ...]
    operation_id: str | None     # last applied operation
    revision: int
    quantity: int
    effective: Bracket
    trail_active: bool
    trail_anchor: float | None

@dataclass(frozen=True)
class ProtectionSnapshot:
    fact_id: str
    account: str
    account_epoch: str
    stream_id: str
    sequence: int
    as_of: datetime
    scope_legs: tuple[str, ...]
    complete: bool
    orders: tuple[ObservedProtection, ...]
    positions: tuple[tuple[str, int], ...]  # original fill -> remaining qty
    resolved_operations: tuple[tuple[str, str], ...]  # applied | rejected

@dataclass(frozen=True)
class ProtectionExecution:
    fact_id: str
    account: str
    account_epoch: str
    owner_id: str
    broker_order_id: str
    as_of: datetime
    quantity: int
    price: float
    allocations: tuple[tuple[str, int], ...]
    terminal: bool              # true only when the triggering order is consumed
    snapshot: ProtectionSnapshot  # complete residual protection/position state

@dataclass(frozen=True)
class ProtectionRead:
    occurrence: ActionOccurrence
    scope_legs: tuple[str, ...]
    prepared_at: datetime

# New owner APIs.
def observe_protection(self, snapshot: ProtectionSnapshot, *, now: datetime) -> None: ...
def observe_protection_execution(self, event: ProtectionExecution,
                                 *, now: datetime) -> tuple[ExecutionEvent, ...]: ...
def check_protection_deadlines(self, *, now: datetime) -> None: ...
```

Complete scope means all executable protection and position allocations for each declared leg, including explicit empty legs. Position omission proves zero only under this completeness contract. Unknown owners/orders, duplicate bindings, wrong epoch, foreign-leg linkage or impossible coverage cause incidents. A live row has positive quantity and an executable component; consumed tombstones remain in owner history, not fictitious working rows.

Persist validated evidence separately from `BrokerFact`, with raw body, original time, stream cursor and disposition. Same fact/content is idempotent and cannot renew currency; conflicting content is an incident. An older/new equal sequence cannot supersede newer evidence. Stream replacement requires explicit binding/reconciliation, not an implicit restart reset.

Completion and no-op credit require `as_of > prepared_at`, causal operation/revision linkage and coherent order-level evidence. Use the retained rail protection-read freshness bound of one book bar; do not replace it with `MAX_FACT_AGE`, the existing fill-fact bound. Neither constant changes. Equal-time/future/stale/position-only/incomplete reads cannot resolve requests or prove absence. Earlier fresh evidence can classify admission; only a post-prepare read completes it.

**Actual producer:** create offline-only `ops/c1_rail/book_synthetic_protection.py` with `SyntheticProtectionBroker(SyntheticBroker)`. It owns independent positions, working components, pending command application, operation outcomes and a monotonic synthetic clock/stream. Proposed methods:

```python
def send(self, command: BrokerCommand) -> BrokerResult: ...
def apply(self, operation_id: str, *, outcome: str, at: datetime) -> None: ...
def execute_entry(self, operation_id: str, *, fill_id: str, quantity: int,
                  price: float, at: datetime) -> BrokerFact: ...
def read_protection(self, request: ProtectionRead) -> ProtectionSnapshot | None: ...
def execute_protection(self, owner_id: str, *, quantity: int, price: float,
                       terminal: bool, at: datetime) -> ProtectionExecution: ...
```

`send` records transport receipt only. `apply(applied|rejected)` changes/preserves independent broker state atomically. `execute_entry` validates against the admitted pending command and produces actual fill/attached-protection state; partial fills get distinct original owners. Reads enumerate that state; they never copy owner desire into “observed” state. A producer clock not strictly after preparation returns insufficient evidence, never an invented later timestamp. Fault modes delay/drop reads/application rather than hand-author a successful working snapshot.

The producer must implement bare attachment, atomic component modification, explicit scoped close and triggered-protection FIFO transitions, retaining IDs/anchors. Restarting the owner does not reset the producer. A protocol plus a fixture returning `working=True` is not delivery of this task.

Use unchanged `TVBrokerEmulator` as an independent oracle for matched traces; do not import the emulator/producer from runtime owner code. If inspection needs a read-only emulator projection, add it without altering execution, `_amend`, `_fill_exit`, `_close_scope`, crossing or rounding.

### 2.4 Prepare, read, send and authority

Prepare the occurrence, frozen scope and `prepared_at` durably before asking the producer for `read_protection(ProtectionRead(...))`. Do not hold a SQLite transaction across a producer call. The account serializer owns the send critical section; use locked helpers, not recursive OS-lock acquisition.

If the read is insufficient, return retained `awaiting_evidence` with no attempt. The harness may advance its producer clock, deliver the snapshot and redeliver that **unattempted** occurrence. This is the sole same-occurrence continuation; terminal/deferred/attempted outcomes never resend. Add runtime `redeliver_prepared_boundary(bar_time: datetime, *, now: datetime)` for explicit same-boot continuation of retained unattempted `awaiting_evidence` members only. It loads the original batch/envelopes and rechecks time/authority; no adapter reevaluation, new ordinal/scope, restart continuation or attempted-member resend. `recover` never calls it. Do not mark a barrier dispatched/completed while any member remains unattempted `awaiting_evidence`; retain its batch and slot for explicit continuation. Complete the marker only after all members have durable dispatch/no-op/refusal dispositions. Do not rely on `on_completed_bar`'s existing duplicate-boundary early return to supply this missing path.

Immediately before attempt/send recheck boot, generation, intervention/local suppression, evidence/time and relevant current admission prerequisites. Arrival of evidence is not send authority. Observers never dispatch deferred desires automatically. SCHEDULED_EXIT admits only its retained authorized operations, never loosening/risk-add; INTERVENTION allows observation/bookkeeping only.

Classify component changes against confirmed effective old parameters:

| Change | Classification |
|---|---|
| Identical effective components/quantity | No send; post-prepare evidence completes no-op |
| Long stop raised / short stop lowered, with no weakening elsewhere | Tightening |
| Stop moved oppositely or existing stop removed | Loosening |
| Trail activation distance/offset increased or existing trail removed | Loosening |
| Trail distances decreased, old state known and anchor preservation supported | Tightening |
| First defined protection on proven never-protected residual lot | Attach |
| Unknown old parameters or uncertain coverage | Defer; never infer tightening |
| Limit-only/mixed change without established non-weakening classification | Conservatively require risk-add authority |

Any weakening component makes the whole demand risk-adding. Require current RUNNING/NORMAL, generation, binding/policy/lifecycle/session/expiry/source-health and existing uncertainty checks; reuse actual owner predicates, never entry sizing to manufacture protection quantity. A missing prerequisite refuses. Conservative limit classification is a proposed design choice for review, not a new strategy rule or permission to omit components.

### 2.5 Outcomes, executions and deadlines

| Outcome/evidence | Durable behavior |
|---|---|
| Accepted without working-order evidence | Pending confirmation; desired retained, old observation retained, deadline unchanged |
| Complete linked read at intended effective components/quantity | Apply observed revision; resolve only matching child/obligation |
| First attach definitively rejected | Immediate protection-gap intervention, no recovery mutation |
| Amend rejected and complete postdating evidence proves old protection intact | Retain refusal and old protection; later authorized new occurrence may retry |
| Amend rejected without proof old protection intact | Remain unresolved; read/reconcile, do not retry; proved absence or timeout intervenes |
| Unknown transport | Immediate intervention; retain attempt, ownership and obligations |
| Complete read proves expected protection absent/wrong after applied outcome | Protection-gap intervention; no automatic close |
| Incomplete/position-only read | No absence/completion credit; original deadline remains |
| Protective execution | Apply evidenced FIFO allocation once; consume trigger owner only on terminal evidence; preserve evidenced residual/sibling coverage |
| Confirmation deadline expired | Intervention; keep unresolved operation/owner; old or duplicate facts cannot extend deadline |

Initial attached protection is due one bar after each actual fill. Subsequent attach/amend is due one bar after preparation. A qualified bare lot has no expected-protection deadline until the strategy defines executable components. Pending accepted is distinct from transport unknown. Check deadlines before dispatch and in `FourLegEvaluateLoop.step` even when every poll returns `None`; late evidence never clears authority.

Validate a `ProtectionExecution` against original owner/broker order, executable quantity, same-leg FIFO allocation and coherent residual snapshot. Terminal execution tombstones the triggering owner; a nonterminal partial execution retains the evidenced working remainder and anchor. The terminal flag must agree with order-level outcome/residual snapshot; quantity alone does not prove consumption. Emulator comparison covers its fully consumed trigger path; additional synthetic partial cases must prove safe residual coverage rather than claim that full-fill parity qualifies every live partial-fill route. Append `Reduction` with a distinct stable protective-execution `close_request_id`, never an entry reservation ID or invented ordinary close. Atomically journal execution, owner consumption, capacity reduction, residual protection and adapter feedback. Emit per-allocation `ExecutionEvent` only after commit, preserving trigger linkage separately from allocated `entry_fill_id`. Ordinary historical `BrokerFact` IDs/reductions remain unchanged.

### 2.6 Versioned durable state

Propose schema **2** for fresh synthetic owners. Keep `protection_state`'s existing session-mode meaning.

| New table | Required durable content |
|---|---|
| `action_occurrences` | key PK; canonical envelope/source; frozen scope; parent/child operation IDs; prepared time/generation; disposition/result |
| `protection_owners` | owner PK; unique original fill; leg/symbol/side/original qty; consumed; desired/observed revisions; effective bracket/qty/order IDs/trail state; evidence identity/time; pending child |
| `protection_operations` | child PK; parent occurrence; owner; primitive; old revision; desired/effective changed components; prepared time/deadline; outcome/attempt |
| `protection_facts` | immutable fact PK; snapshot/execution kind; canonical body; disposition; stream/sequence/time |
| `protection_streams` | account/epoch/stream binding; last accepted sequence/original time; scope |

Define tables/record encoding in `book_protection.py`; owner controls transactions. Extend `BrokerCommand` with optional occurrence and `ProtectionChange` for each protection child, and persist exactly that executable payload in attempts. The original parent action and frozen target set stay in the occurrence row. Parent aggregation retains each child result; a later failure does not erase an earlier applied child.

Fresh path creates version 2 and all required structures atomically. Recognized version 2 validates tables/content/replay invariants; absent required tables are corruption, not migration. Recognized version 1 is refused **without writes** as `legacy_owner_requires_slice_d`. Inspect the version before the current inferred feed-watch migration. Unknown versions refuse without mutation. Never delete/recreate a database to make a test pass. D must supply explicit legacy conversion; this bounded read-only refusal is a design proposal requiring approval here.

## 3. Implementation tasks

Each task includes its real failing-before/passing-after tests. Proposed types may be introduced during implementation; initial reproductions must demonstrate unsafe existing behavior rather than fail only because a helper is absent. Commit only tested deliverables. No subtask completion establishes integrated Slice B acceptance.

### Task 1: Occurrence-bound dispatch cannot expand on redelivery

**Outcome:** Every executable producer supplies provenance; identical content at another occurrence is not permanently deduplicated, and redelivery cannot acquire newly arrived fills.

**Files:** create `ops/c1_rail/book_protection.py`; modify `ops/c1_rail/book_account_owner.py`, `ops/c1_rail/c1_rail_listener.py`, `ops/c1_signal_daemon/book_runtime.py`; create `tests/ops/test_book_occurrence_identity.py`; update concrete existing caller fixtures/tests found by the call-site inventory.

**Interfaces:** `ActionOccurrence`; changed `dispatch`/`handle_book_action`; occurrence records and schema-2 recognition. Protection types are declared here, but working-protection capability is not claimed until Task 2.

- [x] Write a failing current-interface probe that sends a bracket, records rejection, then delivers identical content at a later boundary and observes the existing permanent `duplicate_operation` behavior. Add tests that require stable redelivery scope, identity conflict fencing and caller-provided provenance.
- [x] Implement canonical occurrence serialization and transactional lookup/binding/result persistence. Keep intent IDs; derive new control IDs from occurrence. Record explicit no-target/refused results. Validate an entire cancel-all snapshot before expanding children.
- [x] Commit runtime envelopes with its sorted batch; use the same envelope on the existing takeover-pending retry. Update mode/schedule/takeover/direct producers using section 2.1, without changing C's phases. Add explicit prepared-boundary continuation and replay envelope checks.
- [x] Implement version-2 creation/validation, untouched version-1 refusal and new-schema corruption refusal. Test file-byte equality before/after rejected legacy boot, including a legacy database with retained attempts.
- [x] Run the occurrence file plus `test_four_leg_runtime.py`, `test_book_account_owner.py`, and affected caller tests. Independently inspect every producer assignment before commit.

Initial defect reproduction using existing fixtures (time difference is within the bound evidence window):

```python
def test_control_content_is_not_a_permanent_occurrence_id(tmp_path):
    account, route = owner(tmp_path, [BrokerResult("rejected"),
                                      BrokerResult("accepted")])
    action = BracketAmend("dj30_mym_p250", Bracket(stop=99))
    first = account.dispatch(action, now=NOW)
    later = account.dispatch(action, now=NOW + timedelta(seconds=1))
    # Baseline diagnostic probe only: demonstrates content-key reuse.
    assert later.operation_id != first.operation_id
```

This initial probe deliberately exposes the old identity defect; it is not the final safe-retry acceptance test. Once interfaces exist, replace it with a real-owned-fill, explicit-occurrence, intact-old-evidence sequence from Tasks 2–4. Do not legitimize unowned amendments just to keep this probe executable.

### Task 2: Independent synthetic broker state supplies complete evidence

**Outcome:** Transport acceptance is distinct from working protection; reads have a real named producer and cannot be manufactured from owner desire.

**Files:** `book_protection.py`; create `ops/c1_rail/book_synthetic_protection.py`, `tests/ops/book_protection_fixtures.py`, `tests/ops/test_book_protection_evidence.py`; owner observation and Python-only listener `handle_book_protection(snapshot, owner, *, now)` forwarding boundary.

**Interfaces:** section 2.3 types and producer methods, owner `observe_protection`, and read-only `owner.protection_owners` projection exposing original fill, observed bracket/quantity, consumed, pending operation and trailing state. Existing `BrokerResult.facts` remains its fill/terminal tuple; protection reads are separate.

- [x] Reproduce that transport/irrelevant result facts are not working-order evidence. Add failing tests for wrong account/epoch/leg, unrelated operation, partial/position-only/equal-time/future/stale reads, changed content under a fact ID, and sequence rollback.
- [x] Implement the producer's independent command/application/fill/read state machine. A scenario controls application and its clock separately from receipt. Evidence must enumerate the actual producer state, with full scope and operation/revision linkage.
- [x] Implement owner evidence validation/application. Commit incidents before reporting errors; storage failure latches local suppression and never claims durability. Remove the generic “any result facts marks amendment observed” path only when its replacement is tested.
- [x] Add fixtures using real owner, serializer, SQLite, listener and producer. Fresh fixtures bootstrap once before any activity through the existing synthetic helper; no fixture writes protection rows directly, mutates authority after that bootstrap or supplies mock success predicates. The fixture may choose broker outcomes/clock as explicit synthetic stimuli.
- [x] Run the new evidence/occurrence files; inspect actual commands, broker state and retained snapshots together before commit.

Define the following fixture helpers alongside their first use:

| Helper | Actual implementation contract |
|---|---|
| `fill_bare(fill_id, quantity, leg_id="orb_mnq_v7")` | Submit a valid entry via listener, producer `execute_entry`, then owner `observe`; honor real per-leg admission; create no SQL fixture rows |
| `occurrence(event_id, ordinal=0)` | Use actual account/epoch/session and explicit retained event ID |
| `dispatch(action, occurrence)` | Call the real listener with the fixture's current clock |
| `prepare_read_and_dispatch(action, occurrence)` | Prepare without a qualified read; advance producer clock; submit its read to owner; redeliver the same unattempted occurrence |
| `apply_and_observe(operation_id)` | Producer apply; later complete read; real owner observation |
| `dispatch_and_confirm(action, occurrence)` | Compose the previous two helpers; return original dispatch result |
| `protection(fill_id)` | Read persisted projection, exposing `observed`, `consumed`, `pending_operation`, `quantity`, `trail_anchor` |
| `establish_working(fill_id, quantity, bracket)` | Compose real fill/attach/apply/read steps; establish a test command-count baseline afterward |
| `protection_commands` | Read protection commands since that baseline; never clear broker/owner state |

```python
def test_transport_acceptance_does_not_prove_working(scenario):
    scenario.fill_bare("base", quantity=1)
    action = BracketAmend("orb_mnq_v7", Bracket(stop=98), ("base",))
    result = scenario.prepare_read_and_dispatch(
        action, scenario.occurrence("attach"))
    assert result.transport_state == "accepted"
    assert scenario.protection("base").observed is None
    assert scenario.protection("base").pending_operation is not None
    scenario.apply_and_observe(result.operation_id)
    assert scenario.protection("base").observed.stop == 98
```

If an occurrence has multiple children, `apply_and_observe(parent_id)` explicitly applies each persisted child, then emits the complete read; it must not pretend the parent was one atomic remote mutation.

### Task 3: Owner binding prevents foreign mutation and consumed-owner resurrection

**Outcome:** Captured scope consists only of eligible bare lots or live original owners, and commands contain only authorized changed components.

**Files:** `book_protection.py`, owner scope/admission; create `tests/ops/test_book_protection_ownership.py`; inspect/extend `tests/ops/test_tv_broker_emulator.py` for missing literal vectors. Any necessary emulator projection is read-only.

**Interfaces:** `ProtectionTarget`, `ProtectionChange`; command occurrence/change fields; owner projection and qualified observations from Task 2.

- [x] Reproduce an ORB amendment targeting a real MYM fill through the current owner. Add a mixed scope with a valid first/foreign final target, proving complete preflight before the first child send.
- [x] Implement all section 2.2 resolution rules. Add consumed-owner no-op/refusal, unknown/cross-leg incident, empty scope, unscoped capture, unresolved-owner/close deferral and bare-first-attach cases.
- [x] Implement pure normalized component diff and authority predicates in section 2.4. Tests independently pin long/short literal prices and verify that changing a stop does not resend an unchanged active trail.
- [x] Pair producer and unchanged emulator traces for live sibling owner with zero original FIFO remainder, consumed owner with residual lot, bare first attachment, active-anchor preservation and explicit scoped close versus protective FIFO execution. Compare original owners, allocations, quantities, components and anchor, not only classifier return values.
- [x] Run ownership, emulator, ingress and occurrence suites; review target and authority boundaries before commit.

```python
def test_foreign_member_prevents_every_child_send(scenario):
    scenario.fill_bare("orb-fill", quantity=1)
    scenario.fill_bare("mym-fill", quantity=1, leg_id="dj30_mym_p250")
    action = BracketAmend("orb_mnq_v7", Bracket(stop=98),
                          ("orb-fill", "mym-fill"))
    scenario.dispatch(action, scenario.occurrence("foreign-scope"))
    assert scenario.protection_commands == ()
    assert scenario.owner.authority == "INTERVENTION"

def test_redelivery_cannot_capture_new_fill(scenario):
    scenario.fill_bare("base", quantity=1)
    occurrence = scenario.occurrence("bar-1")
    action = BracketAmend("orb_mnq_v7", Bracket(stop=98), None)
    first = scenario.dispatch_and_confirm(action, occurrence)
    scenario.fill_bare("add", quantity=1)
    again = scenario.dispatch(action, occurrence)
    assert again.operation_id == first.operation_id
    assert len(scenario.protection_commands) == 1
    assert scenario.protection_commands[0].protection_change.target.entry_fill_id == "base"
```

Use `BrokerCommand.protection_change: ProtectionChange | None` and `occurrence: ActionOccurrence | None` as the proposed exact new fields. Fixture fill setup must use valid adapter-normal quantities that yield the requested admitted fill, or explicitly assert the admitted/partial quantity; it cannot alter sizing laws to obtain a convenient fixture.

### Task 4: Outcomes, deadlines and protective execution retain real obligations

**Outcome:** Evidence resolves only its request; rejected/unknown/expired operations cannot create retry permission, and protective fills reach capacity/feedback exactly once.

**Files:** owner `_observe_locked` plus new observers, `book_protection.py`, synthetic producer, `ops/c1_signal_daemon/book_evaluate_loop.py`; create `tests/ops/test_book_protection_lifecycle.py`; extend runtime replay tests.

**Interfaces:** `ProtectionExecution`, `observe_protection_execution`, `check_protection_deadlines`. Add Python-only listener `handle_book_protection_execution(event, owner, runtime, *, now)`: commit first, then use the runtime's serialized feedback-delivery path. No HTTP route or production source is added.

- [x] Write a rejected-amendment trace with real original working protection. A later new occurrence may send identical desired content only after complete intact-old evidence and current authority. The original rejected occurrence always returns its retained result.
- [x] Encode every section 2.5 outcome with real producer application and SQLite: first attach reject; amend reject with/without intact-old proof; pending accepted; unknown transport; proved absence/wrong parameters; expiry; late observation after intervention.
- [x] Implement atomic protective-execution/Reduction/feedback journaling. Add a nonterminal partial protective fill followed by its terminal remainder: no early tombstone, no released obligation from acceptance, no double reduction. Test trigger owner differs from allocated oldest lot, owner remains consumed across restart, and surviving sibling retains its anchor despite zero original remainder. Duplicate execution neither reduces twice nor delivers feedback twice.
- [x] Add crash cuts after preparation, attempt-before-send, producer apply-before-observation and execution commit-before-feedback. Restart remains HALTED and read-only; never invoke activation as recovery.
- [x] Inject real SQLite failure during incident persistence; verify sticky local suppression after storage restoration and no false durable-incident claim. Race evidence/dispatch with halt under the actual serializer; no second send after a confirmed fence.
- [x] Exercise the loop with all sources returning `None` across a deadline, plus repeated stale/duplicate evidence. Preserve the original deadline and distinguish accepted-pending from unknown transport.
- [x] Run lifecycle/occurrence/runtime plus `test_pr409_owner_lifecycle.py`, `test_pr409_review2.py`, `test_pr409_review3.py`; investigate changed expectations against the contract before committing.

```python
def test_unknown_amend_does_not_authorize_another_occurrence(scenario):
    scenario.establish_working("base", quantity=1, bracket=Bracket(stop=98))
    scenario.broker.queue(BrokerResult("unknown"))
    action = BracketAmend("orb_mnq_v7", Bracket(stop=99), ("base",))
    scenario.prepare_read_and_dispatch(action, scenario.occurrence("change-1"))
    assert scenario.owner.authority == "INTERVENTION"
    assert scenario.protection("base").observed.stop == 98
    scenario.dispatch(action, scenario.occurrence("change-2"))
    assert len(scenario.protection_commands) == 1
```

`queue` retains the existing `SyntheticBroker` transport-response seam. It does not mutate working protection; only producer application/execution methods do so.

### Task 5: Package and accept the integrated synthetic slice

**Files:** both `deploy/c1_rail/Dockerfile` and `deploy/c1_signal_daemon/Dockerfile`, `.dockerignore`, `scripts/c1_image_validation.sh`; corresponding manifest tests; this plan/spec evidence links.

- [x] Add the shared runtime `book_protection.py` import closure to both explicit COPY sets and exact validation inventories. Keep the offline producer/emulator out of runtime imports. Do not weaken inventories to pass.
- [x] Verify fresh schema 2, untouched legacy refusal, missing-table/new-schema corruption, unchanged historical identities and no sends at restart cuts. D owns migration, not this task.
- [x] Run the four new suites with ingress/emulator/runtime/owner/lifecycle/review regressions. Run all three image-manifest/validation suites, the full operations suite and check-tier repository gates using the commands below.
- [x] Run new synthetic suites with private inputs absent and optional signing imports blocked. Record actual exits, skips, dependencies and Python 3.11 execution availability separately from syntax-floor checks.
- [x] Independently review the complete current diff against the acceptance traces below. Commit the tested slice and revision-bound evidence. Push/check actual-head CI only if separately authorized; no deployment/activation.

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'
& 'C:/Program Files/Python313/python.exe' -m pytest tests/ops/test_book_occurrence_identity.py tests/ops/test_book_protection_evidence.py tests/ops/test_book_protection_ownership.py tests/ops/test_book_protection_lifecycle.py tests/ops/test_book_ingress_validation.py tests/ops/test_tv_broker_emulator.py tests/ops/test_four_leg_runtime.py tests/ops/test_book_account_owner.py tests/ops/test_pr409_owner_lifecycle.py tests/ops/test_pr409_review2.py tests/ops/test_pr409_review3.py -q -p no:cacheprovider --tb=short
& 'C:/Program Files/Python313/python.exe' -m pytest tests/ops/test_c1_signal_daemon_image_manifest.py tests/ops/test_c1_rail_image_manifest.py tests/scripts/test_c1_image_validation.py -q -p no:cacheprovider --tb=short
& 'C:/Program Files/Python313/python.exe' -m pytest tests/ops -q -p no:cacheprovider --tb=short -ra
& 'C:/Program Files/Python313/python.exe' scripts/gate_manifest.py --tier check
```

Capture `$LASTEXITCODE` immediately after each command; stop on failures before claiming acceptance. A subsequent successful log-read command is not the test process's exit status.

## 4. Combined acceptance and falsifiers

| Trace | Required intermediate and final evidence |
|---|---|
| Foreign/mixed scope | No child send; durable semantic incident; prior obligations retained |
| Same occurrence after another fill | Original operation/target scope reused, no new child/send |
| New occurrence after definitive amend rejection | Same desired content eligible only with postdating intact-old proof and present authorization |
| Rejected first attachment | Immediate gap/intervention; position retained; no incident-triggered close |
| Accepted versus unknown amendment | Accepted remains pending with original deadline; unknown intervenes; neither allows competing mutation |
| FIFO trigger consumes another owner's lot | Trigger tombstoned, actual lot reduced once, live sibling owner/anchor retained |
| Desire targeting consumed owner | No resurrection despite residual lot or replay |
| Deadline/late evidence/storage failure | Honest durable-or-failed incident, no refreshed deadline, sticky suppression, no clearing authority |
| Crash/restart at every durable boundary | Same IDs/scopes/attempts/obligations, no send, schema ambiguity/corruption blocked |
| Read-after-prepare continuation | Equal-time read sends nothing; qualified later read can advance only a same-boot unattempted request under current authority; no completed/attempted redelivery sends |

Every successful amendment must also prove unchanged components were not resent. Compare full producer/emulator outputs for long/short, off-tick, partial/FIFO, consumed/bare and close-time cases. Tests of helper return values alone are insufficient.

Falsifiers: desired-state-derived observation; a “complete” snapshot omitting an executable order; equal-time/position-only completion; redelivery expanding scope; content equality blocking a genuinely new authorized demand; original-lot exhaustion killing a live owner; consumed-owner reattachment; post-incident send; silently converting legacy uncertainty into apparent protection health.

## 5. Design review decisions and next-slice handoff

The user authorized execution of these concrete design choices on 2026-09-16:

1. Required source occurrence on every executable caller, with explicit same-boot continuation only for unattempted read-waiting preparations. This is an offline API compatibility change; silent provenance inference is rejected.
2. Independently stateful synthetic producer, complete scope reads and a protective-execution path. This adds real offline capability without claiming a live provider.
3. Schema 2 for fresh owners and non-mutating schema-1 refusal. This supplies B's durability boundary while reserving legacy migration for D.
4. Conservative risk-add treatment of limit/mixed changes not proved non-weakening. Unknown old state always defers; no permission is inferred from a “protection” label.

Slice B establishes scoped V2/V3/V4/V5/V7 protection behavior and observer-side V6 fencing. It does not establish C's cancellation/close/quiescence ordering, D's activation/migration, whole-account recovery, live route capability or PR 409 merge readiness. Before C, map these evidence types into takeover phase transitions/current admission. Before D, specify legacy conversion and fresh-account bootstrap identity. Missing capabilities remain explicit blockers, never test-only substitutes.


## 6. Draft self-review record

This draft was checked against the approved correction's B responsibilities and the actual
caller/observation paths at `c8476c8`. The review identified and incorporated three otherwise
missing dependencies: protective executions need their own owner-to-FIFO accounting path;
read-after-prepare needs explicit unattempted runtime continuation rather than the existing
duplicate-bar early return; and new required tables need a version boundary even though D
owns migration. Nonterminal protective fills retain working remainder instead of prematurely
consuming their owner. Example ORB fixtures use one admitted base contract, preserving sizing.

At the original draft boundary no implementation tests had run. The execution record below supersedes that draft-only status.


## 7. Implementation and acceptance record (2026-09-16)

Implemented from `c8476c8` in the existing isolated worktree, after confirming remote
`fc7cdc7` had not advanced. The executing instruction approved this plan, including a
local tested commit. No push or actual-head CI claim is included.

### As-built structure

- `book_protection.py`: immutable occurrence/read/execution contracts and pure component,
  directional normalization and weakening helpers.
- `book_protection_owner.py`: owner mixin using the same serializer, connection and
  transactions. SQL definitions remain centralized in `book_account_owner.py` rather
  than split between pure contracts and persistence code.
- `book_synthetic_protection.py`: independent offline working orders, application clock,
  execution allocations and trailing state; never imported into production runtime.
- Schema 2 stores occurrences, original owners, mutation obligations, immutable evidence
  and stream cursors. Explicit schema 1/unknown versions refuse without migration;
  recognized-schema missing structures, missing original owner records or invalid retained records refuse without writes.
- Runtime retains provenance with each sorted batch. Explicit continuation is restricted
  to the original runtime instance and unattempted evidence waits; reconstruction does
  not restore continuation authority. All executable direct callers now supply provenance.
- Both runtime images include the pure contracts and owner mixin, with exact manifests.

The implemented tests are split across occurrence, producer, ownership, evidence,
lifecycle, review and runtime-occurrence files. Initial existing-interface foreign/unknown
scope probes failed because the baseline sent unauthorized controls; producer tests first
failed because the new capability was absent. During review, concrete failing regressions
proved and corrected premature equal-time observation, residual-snapshot atomicity,
rejected-old quantity qualification, attempted-child continuation, removal resurrection,
and loss of successful sibling observations on a later coherent rejection. Existing
unowned-amendment tests now establish real fill/read evidence rather than bypassing the
new ingress contract. These are the as-built equivalents of the illustrative draft probes.

### Acceptance traces

| Contract | Executable evidence |
|---|---|
| Entire target set checked before sending | `test_invalid_final_target_prevents_every_child_send` |
| New occurrence retry; frozen old occurrence | ownership rejection/retry and unscoped-later-fill tests; occurrence identity suite |
| Independent evidence and literal semantics | producer suite paired with unchanged emulator for both sides, directional rounding, FIFO/anchors and explicit closes |
| Accepted/pending versus rejected/unknown | ownership/lifecycle suites, including producer receipt followed by connection failure |
| Atomic protective FIFO reduction and feedback | ownership partial/terminal/replay and review invalid-residual rollback tests |
| No consumed/removal resurrection | ownership original-owner/tombstone and removal-operation regression |
| Multi-owner partial outcome | first applied child retained despite second rejected attachment; intervention remains |
| Postdating complete evidence only | evidence/review suites: incomplete, equal-time, stale/future, wrong binding, mismatched revision, replay/sequence conflict |
| Idle and executable-dispatch deadlines | runtime idle, occurrence ordinary-dispatch and lifecycle late-observation tests |
| Real persistence failure | SQLite trigger abort prevents incident commit and latches local send suppression after storage restoration |
| Restart cuts | occurrence/lifecycle cuts at preparation, attempt, send, broker application and execution commit before feedback |
| Version boundary/corruption | non-mutating schema-1 refusal, missing schema-2 structures and malformed retained owner/time tests |

If working protection executes while a separate amendment is pending, the consumed owner
retains that operation and its original deadline. Consumption is not invented amendment
resolution; timeout still intervenes. A consumed-order recovery protocol is not introduced.

Verification (exit 0 for every listed command):

- Full `tests/ops`: **2,479 passed, 15 skipped**, two existing seaborn deprecation warnings.
  All skips identify absent private adapters/effective inputs. This run includes the final
  runtime implementation and all final lifecycle/corruption regressions.
- Final lifecycle suite: **10 passed**, including actual serializer concurrency with a
  committed halt, application-before-observation and execution-before-feedback restart cuts.
- The combined synthetic/ingress/emulator run with optional signing imports blocked:
  **174 passed**, no skips; includes all final new tests. Counts overlap; do not add them.
- Both image manifest suites plus image-validation tests: **23 passed**. These check the
  packaged import closure and exact inventories, not a Docker image build or deployment.
- `scripts/gate_manifest.py --tier check`: passed. Warnings identify absent private/heavy
  data and existing documentation metadata, without weakening any gate.
- Final diff whitespace and repository boundary checks: passed.

Evidence logs are retained locally as `tmp-slice-b-ops-final.txt`,
`tmp-slice-b-no-signing-final.txt` and `tmp-slice-b-gates.txt`; they are not product files.
The committed record and executable tests carry the durable acceptance summary. Tests run under Python 3.13.2;
only 3.13 and 3.14 are installed. The repository boundary gate parses the 3.11 syntax floor;
this is not a claim of a Python 3.11 runtime test. Private Pine/data trees are absent in this
worktree; optional `cryptography`/`nacl` imports are deliberately blocked in the dedicated
synthetic run. No strategy numeric ingress exception was introduced: zero trailing offsets
remain rejected pending the separate strategy decision.
