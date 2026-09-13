# PR 365 redesign contract

Execution authorized by the operator after the production-reference acceptance hold.
Starting PR head: `dfa185c974b8b2def1591831bbeb0f314bb9b42d`.
Inspected owning spec: rev 5.6 at `73a3334` on `claude/tb-s3-rail-extension-spec`.
Read production `book_protocol.py`, `book_policy.py` and telemetry `BrokerEvidence`
directly at the PR head. These remain read-only dependencies.

| Decision | Chosen offline semantics | Producer, consumer and discharge evidence |
|---|---|---|
| D1 | Preserve rev 5.6 strict timestamp postdating; additionally require monotonic acquisition after the exact prepare/latest dispatch boundary. Reject duplicates, older acquisitions, future or stale reads. Never assemble a full read from unrelated position and working snapshots. | The harness clock sequences commands, dispatches and broker read acquisition. Broker snapshots capture independent immutable facts at acquisition. The listener persists accepted cursors and attempt boundaries; reconciliation requires a covering full read. Production L-1 equivalence is still owed. |
| D2 | Distinguish zero position from quiescent scope. Broad flats own cancellation of every working remainder, including partial orders and unknown sends. The block and work record precede dispatch. A racing fill remains owned and is closed after reconciliation. Session latch expiry never discards unfinished work. | Commands/timers own flat operations; order-level terminal evidence resolves cancellation and releases only unfilled reserve. Quiescence requires zero position, empty working orders and no unknown exposure-creating request. Feed semantics remain subject to the spec's live ratification boundary. |
| D3 | Observed protection must match the confirmed component or a value actually dispatched by an unresolved attempt for that component. Quantity, side, type and linkage must match. Unsent siblings are not transitions. Mixed outcomes retain individual attempts. | Strategy supplies desired fields; transport supplies individual outcomes; full broker evidence confirms each component. Static parameters exclude the native moving anchor. Classify against fresh observed fields; wider/later trails are risk-adds and unknown anchor semantics defer. First-attach rejection creates immediate gap recovery. |
| D4 | Completion drives durable effects, including disarm; status is pure. Persist planned effects and ownership before dispatch, and dispatch boundaries before invoking the broker. | Event handlers reconcile facts for all operations before advancing queued work. A missing response after dispatch survives restart as unknown and requires evidence before retry. Local effect IDs do not establish exactly-once broker execution. The model disarm is local; production configuration acknowledgment remains owed. |

The coordinator owns integration. Modules remain one listener state machine: durable
records in `state.py`, shared predicates in `rules.py`, the facade/event transitions
in `kernel.py`, independent broker execution in `broker.py`, event scheduling and crash
injection in `harness.py`. No alternate listener state is maintained during migration.

The following refinements govern the test model wherever rev 5.6 described only a
single owner or timestamp. They are explicit integration requirements for the owning
spec and TB-I3; they do not amend a live adapter or authorize live activity.

- An obligation is keyed by `(reason, owner)`. Retrying an operation does not erase
  its rejection obligation. A completed bounded reduction discharges that owner's
  rejection when the entire residual satisfies the shared protection predicate; it
  does not require an unrequested full liquidation. Gap obligations remain until
  confirmed flatness. Session latch expiry removes only the session latch.
- The harness clock is an external monotonic sequencing domain that survives listener
  restart. Read acquisition, command creation and actual dispatch each have distinct
  identities. A full read has a request fence: every earlier accepted request is
  either still pending or accounted for. `pending_requests` and `request_outcomes`
  are captured at acquisition. Delayed execution rejection/unknown outcomes feed
  the same transition handler as immediate outcomes. A live producer must supply
  equivalent guarantees; a model sequence number is not a broker API claim.
- A known-old value after a fenced, nonpending unknown amendment resolves that
  component as unapplied, allowing the port's next reissue. An unsent sibling cannot
  explain a new value. Trails on a route that resets anchors defer parameter changes
  even while observed inactive: activation can race dispatch. No atomic conditional
  modification capability is invented. Fresh absence after first protection is
  defined still creates a gap, including when evidence precedes an unsent ATTACH;
  that ordering observes different facts from dispatch-before-acquisition. A late
  rejection after gap recovery does not recreate retired protection or crash.
- Whole-account flatten and multi-leg takeover persist every scope and planned effect
  before the first dispatch. Status cannot report kill complete before disarm applies.
  A bounded attempt whose requested quantity already executed cannot send that
  quantity again; if residual protection is invalid, a queued full recovery may
  consume the scope and complete both obligations on subsequent evidence.
- Takeover settlement runs the same admission checks as normal admission, verifies
  the requester and sized quantity, and requires fresh quiescence on displaced
  scopes. The in-progress ledger takeover survives restart. Repeated unchanged
  position evidence does not manufacture a position-change event.

Schema 2 rejects incompatible or missing restart snapshots explicitly. It never boots
empty/armed because records are absent, and restart halts on unallocated bare exposure.
Never-dispatched entries and loosening amendments are cancelled on restart and require
new admission; reservations for those entries are released because dispatch did not
occur. Dispatched attempts remain unknown until evidence resolves them. A production
migration is outside this test model.

## Verification

Baseline: 58 existing tests passed. Initial redesign regressions: 12 failed, one
passed at the starting head. The final kernel suite has 232 passing tests, including
96 permutations of two owners' old/new evidence deliveries with four restart cuts,
partial cancellation outcomes, all four dispatch crash boundaries, mixed component
outcomes, active/inactive trails, deferred execution and late outcomes. Expected
allocations and owner sets are literal or independently computed from named external
events, never kernel decision helpers. Status purity is checked after each delivery.

Independent review accepted the bounded offline code after reproducing and closing
the ownership, takeover admission, missing-state, trail-race and late-outcome findings.
The reviewer independently ran all seven kernel suites: 232 passed. This is code
acceptance, separate from PR/CI acceptance and live qualification.

`python tests/ops/tb_s3_kernel/mutation_check.py` copies the model and tests into a
temporary directory, verifies a passing control, and requires assertion failures for
five mutations. Results: owner overwrite 77 failures; ignored working remainder 4;
timestamp without causality 1; ignored protection parameters 3; omitted disarm 9.
No mutation is applied to this checkout or production files.

Final full-ops, check-tier and lint results are recorded in the execution handoff.

The production-reference acceptance hold remains pending final operator disposition.
Live L-1 request/evidence equivalence, L-2 validation, production disarm acknowledgment
and the spec's feed-loss ratification remain explicit dependencies.
