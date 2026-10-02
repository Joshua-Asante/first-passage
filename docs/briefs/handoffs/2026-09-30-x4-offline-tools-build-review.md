# X-4 offline tools build and review — bounded handoff

**Status:** DRAFT / NOT DISPATCHED. Joshua requested recommendations and this
handoff, not implementation or a live action. Before dispatch, the coordinator
commits and freezes the governing packet/card, identifies the executor, and
records the exact starting commit. An uncommitted card is not a worker dispatch.
The recommended actor exception and limits remain PROPOSED; a synthetic build
can exercise them without their live ratification. No actor ruling is delegated.

> **Superseded in part, 2026-10-01 (operator ruling, merged in #580).** The
> [deployment checklist's first-session simplification rulings, item 3](../../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-10-01--first-session-simplification-rulings-six-cuts)
> now **owns the X-4 build scope** and supersedes this draft where they differ.
> The build is **small reviewed extensions to X-1's accepted round-7 generator
> and sender**: a stop entry type, two children, and a parent cancel bound to the
> parent's account path. Terminal reads use **R-1 v3.2**, with a **bounded
> GET-only pre-cancel status reader** that seals the parent `Working` and both
> children `Suspended` before the cancel; the coordinator classifies from sealed
> bytes. **Kept:** one-use placement and cancel claims that survive restart,
> including an unknown placement (MUST-PASS); raw response bytes sealed before
> parsing; validation of both child identities; attended cancel of every live
> order if the account is flat. **Cut:** `x4_profile`, the observer's read
> budget and rate machinery, the asynchronous late-response channel,
> `x4_attended_input`, `x4_adjudicate` and the multi-pass reviews; one focused
> review replaces those reviews. The component list, interfaces, tests and
> sequence below are the **superseded full-suite design**, retained as a record
> of what was drafted. Do not dispatch from them. A coordinator freezing the
> next X-4 card builds it from the checklist's kept set, reusing only the parts
> of this draft that bind a kept item. Its return uses the four-state taxonomy
> (`DONE` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT` / `BLOCKED`), and any
> `BLOCKED` return names its sub-case: `BLOCKED — context-problem |
> capability-problem | scope-problem | plan-itself-wrong` (brief-authoring
> discipline 8; `cc_handoff` §6). GC-4's required observation and the X-1
> acceptance record are unchanged.

**Selected outcome:** one independently reviewable, offline-verified X-4 tool
package: deterministic two-child resting-entry generation, separately confirmed
single parent cancel, read-only observation, sealed evidence and a separate
network-free evidence classifier. Deliver synthetic end-to-end traces and an
independent review return. No live-capability or deployment acceptance.

**Prerequisites:** read the frozen [X-4 decision packet](../../notes/2026-09-30-x4-decision-packet.md),
especially §2 / §3.1 / §4–§6; the [drill plan](../../notes/2026-09-26-tradeify-route-drill-plan-draft.md)
§2.0/§2.4; commissioning §3.2–§3.7/§4.2; STATE and applicable AGENTS.md.
The packet defines the exact proposed profile and production/private decisions
still owed. The accepted X-1 sources and pins must be present and match before
reuse. Live ratifications are not prerequisites to synthetic implementation;
they are mandatory prerequisites to any later production path.

**Ownership:** one named worker proposes the design and builds the package;
a different reviewer first refutes the frozen interfaces/state machine before
implementation, then inspects the final frozen bytes and independent adversarial
cases under a separate review dispatch. The dispatching
deployment coordinator assigns both roles, accepts the combined offline return,
and retains integration authority. Joshua retains live profile/actor ratification,
private account decisions, attendance and CP-3. The builder never accepts its own
combined result. The reviewer needs its own bounded read/test dispatch, with no
authority to edit the builder's bytes or campaign owners.

**Verification:** all acceptance cases in §4 and named authority-block tests,
plus end-to-end synthetic traces; launcher-retained completed, zero-exit,
stable-source, complete-capture records and before/after source/package hashes.
The independent reviewer rechecks actual source files and sealed fixtures,
not summaries. No remote HTTP, host/broker commands or real credential use.

**Checkpoint:** return premise findings and the proposed interface/state-machine
design before implementation. The coordinator freezes that design and dispatches
an independent **refute-first interface review (C1)** under brief-authoring
discipline 13. No implementation or acceptance-trace production starts until the
coordinator accepts the design review. Report contradictions immediately and stop
dependent work. After implementation, return the candidate package and evidence;
the coordinator freezes its hashes and issues the separate final byte review.
After any repair, re-review affected traces before acceptance. A change to the
accepted interfaces, clocks, ownership or terminal rules reopens C1 and invalidates
affected evidence; retained final review does not replace the early checkpoint.

**Return boundary:** successful delivery ends with the independently reviewed
offline package and four-state return. A scope/authority/source-contract conflict
returns `NEEDS_CONTEXT` before dependent implementation; no consequential choice
is invented. Stop before primary-checkout installation, real-binding generation,
attended human rehearsal, account/host reads, CP-3, orders, arming or deployment.
The roadmap is context, not authorization to take the next slice.

```yaml authority
seat: worker
parent: docs/notes/2026-09-30-x4-decision-packet.md
max_risk: low
capabilities: [repository.read, tests.run, worktree.write]
constraints:
  - offline_synthetic_only
  - no_account_host_vendor_or_credential_access
  - no_real_network_calls
  - no_existing_x1_or_sealed_evidence_edits
  - no_governance_owner_edits
  - no_commit_push_pr_or_primary_install
  - proposed_profile_not_live_authority
acceptance:
  - local_artifacts/route-drills-2026-09/tools/x4-v1/test_x4_contract.py::test_mutations_need_human_confirmations
  - local_artifacts/route-drills-2026-09/tools/x4-v1/test_x4_contract.py::test_tampering_and_refusal_leave_no_handoff
  - local_artifacts/route-drills-2026-09/tools/x4-v1/test_x4_contract.py::test_two_children_cancel_trace_classified_from_sealed_bytes
  - local_artifacts/route-drills-2026-09/tools/x4-v1/test_x4_contract.py::test_unknown_cancel_blocks_retry_across_restart
  - local_artifacts/route-drills-2026-09/tools/x4-v1/test_x4_contract.py::test_deadlines_preempt_prompts_and_late_responses
  - local_artifacts/route-drills-2026-09/tools/x4-v1/test_x4_contract.py::test_offline_tripwire_blocks_real_network
  - local_artifacts/route-drills-2026-09/tools/x4-v1/test_x4_contract.py::test_raw_response_is_sealed_before_parsing
```

## Open items, binding on the C1 interface review

Under the operator's stopping rule after the finding count rose from five to
seven, these six findings are **recorded, not folded** into this draft. A seventh
binding item was added by operator ruling on 2026-10-01 (item 7 below). The C1
interface review must resolve **each one before implementation starts**, with
the coordinator accepting the resulting disposition. The interface snippets,
test ownership and execution sequence below remain provisional on these points;
their presence does not discharge this gate or authorize dispatch.

**Applicability after the 2026-10-01 reduced build path.** The checklist ruling
says these items apply only where they bind the kept items:

| Item | Status against the kept set |
| --- | --- |
| P1 read kind and GET binding fields | **Applies.** It binds the kept GET-only pre-cancel reader and the R-1 v3.2 terminal reads. |
| P1 unknown placement in the durable-claim/restart test | **Applies, MUST-PASS.** The kept one-use placement claim must survive restart, including an unknown placement. |
| P2 async late-response channel | **Applies, cancel operations only, merged into item 7.** The general channel stays cut. Item 7 requires C1 to settle an owned completion/polling primitive for cancel operations and the sealing of a late cancel response. |
| P2 pre-mortem (brief-authoring discipline 11) | **Applies** to the reduced X-4 card, scoped to the kept extensions. |
| P2 separate spec-compliance and quality passes (discipline 9) | **Moot.** The ruling cuts the multi-pass reviews; one focused review replaces them. |
| P2 acceptance tests frozen by the coordinator or reviewer, not the builder | **Applies** to the tests for the kept items. |
| Item 7 post-cancel status read (added 2026-10-01 by operator ruling) | **Applies, MUST-RESOLVE before dispatch.** It closes the gap between the kept pre-cancel reader and R-1 v3.2's all-terminal precondition, after any cancel attempt, including an unknown outcome. |

- **P1 — PRRT_kwDOT46Eac6n2QJB:** Operation needs an explicit read kind and GET binding fields. [Thread](https://github.com/Joshua-Asante/first-passage/pull/572#discussion_r4152959541).
- **P1 — PRRT_kwDOT46Eac6n2QIw:** The durable-claim/restart test must cover unknown **PLACEMENT** as well as cancel; this is **MUST-PASS before any live X-4**, because `order_id` idempotency is disproven. [Thread](https://github.com/Joshua-Asante/first-passage/pull/572#discussion_r4152959517).
- **P2 — PRRT_kwDOT46Eac6n2QIc:** Provide a late-response channel by modelling a request as an owned async operation. [Thread](https://github.com/Joshua-Asante/first-passage/pull/572#discussion_r4152959492).
- **P2 — PRRT_kwDOT46Eac6n2QIn:** Add a pre-mortem per brief-authoring discipline 11. [Thread](https://github.com/Joshua-Asante/first-passage/pull/572#discussion_r4152959506).
- **P2 — PRRT_kwDOT46Eac6n2QI3:** Separate spec-compliance and quality review passes per brief-authoring discipline 9. [Thread](https://github.com/Joshua-Asante/first-passage/pull/572#discussion_r4152959524).
- **P2 — PRRT_kwDOT46Eac6n2QJN:** Acceptance tests are frozen by the coordinator or C1 reviewer, not by the builder, per `cc_handoff` §6.0. [Thread](https://github.com/Joshua-Asante/first-passage/pull/572#discussion_r4152959551).
- **Item 7 — post-cancel status read (operator ruling 2026-10-01, option c; MUST-RESOLVE before dispatch).** After any parent cancel attempt, acknowledged or with an unknown outcome (a timed-out or lost response gives no acknowledgment), the parent or a child may still be `Suspended` or `Working`, and no reviewed tool reads it. The kept pre-cancel reader runs only before the cancel. R-1 v3.2's accepted contract runs only once every involved id is terminal ([X-1 packet](../../notes/2026-09-29-x1-decision-packet.md), observer procedure). Neither a cancel acknowledgment nor an unknown cancel outcome establishes terminal state. Before any build or live X-4, C1 decides between a reviewed GET-only post-cancel reader that permits and reports live parent/child states, and an extended, reviewed R-1 contract. C1 must also settle an owned completion/polling primitive for cancel operations, which tells when a cancel request has actually completed so that no post-cancel GET overlaps an in-flight cancel, and the sealing of a late cancel response. Both are settled before the post-cancel reader is dispatched. This is scoped to cancel operations only and does not reinstate the cut general late-response channel; if C1 finds that it needs more than that, the question returns to the operator. [Thread](https://github.com/Joshua-Asante/first-passage/pull/572#discussion_r4161616775) · [completion thread](https://github.com/Joshua-Asante/first-passage/pull/572#discussion_r4161777694).

## 0. Read and premise report before coding

Identify HEAD and dirty state, frozen card/packet hashes, read-only source roots,
planned footprint, and actual approved Python environment. The starting source
identity inspected by the drafter was primary `028c5ce88a473942e0e792bb607fe9e85133948b`
with documentary edits; that is **not** the later dispatch commit. No dispatch
has occurred. The coordinator supplies the committed card/packet identity at
dispatch, rather than pretending this draft's starting revision contains them.

Read in the primary checkout, verify pins, then report:

- `local_artifacts/route-drills-2026-09/tools/x1-r7/`: generator, sender, observer,
  common validators/recorder/seal and adjudicator; pins from adjacent
  `x1-r7-codex-review/RULING.json`. Round-7 is market-entry/single-child only.
- `local_artifacts/route-drills-2026-09/tools/x1-attended-input-v1/attended_input.py`:
  hash `6dcee76cf35184aa5cb215c3168f37f71594d033cee892b473b78d5699c39421`.
- `local_artifacts/route-drills-2026-09/x1-prep-2026-09-29/X1_OBSERVER_PROCEDURE_V3_3.md`:
  hash `5da9618623e96cf38c6bb494557131c95e0731fc387356bcd39a6b8a63e81b2e`;
  use supported status/report/version shapes, not its one-child sufficiency list.
- Public commissioning §3.7's retained-source contract and packet §3.1's primary
  instrument/fee sources. No new browsing/vendor contact by this worker. If
  a required field's semantics are unavailable, record it as unobserved, not
  invented from a successful fixture. No private strategy source is needed.

No read of the real X-1 session binding, request, account data, credentials or
`.env` is permitted by this card. Do not copy live session fixtures. Source-tool
read access does not imply access to adjacent private account evidence.

## 0.5 Routing and allowed environment

Build in an isolated local worktree of this repository, selected/created at
dispatch under `superpowers:using-git-worktrees`, using that checkout's launcher.
Run `fp.ps1 doctor` first. If it fails, diagnose the launcher environment;
do not bypass it or use a research/system interpreter.

All implementation and synthetic artifacts live in that worktree's gitignored
`local_artifacts/route-drills-2026-09/tools/x4-v1/` and
`local_artifacts/route-drills-2026-09/x4-offline-build-review/`.
Verify ignore disposition before writing. The primary accepted X-1 tools are
read-only references; do not import mutable helpers from a sibling live directory.
If reusing code, place reviewed isolated copies in the new X-4 package, document
provenance and changes, and hash them. Never edit or overwrite accepted X-1 files.

## 1. Scope, roadmap and integration contract

The [deployment checklist](../../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md)
and X-4 packet own the overall roadmap: proposed limits/actor decision → this
bounded offline package → coordinator acceptance → exact-tool attended rehearsal
and fresh private binding/readiness → separate CP-3 → one row → trace review.
Only the offline package is selected here. Later phases remain separate.

Proposed components and responsibility boundaries:

| File in `tools/x4-v1/` | Responsibility |
|---|---|
| `x4_profile.py` | Canonical proposed profile from packet §3.1; resolved binding validation; explicit approval state and profile digest. All consumers reference the same object; no copied numerical defaults |
| `x4_generate.py` | Exact nine-field placement bytes, two child levels, write-once validation/sidecars and independent hash-record export; no network |
| `x4_mutate.py` | Placement and parent-cancel operations with separate human confirmation, final checks, one-use durable claims, method/path/body context digest and injected transport |
| `x4_common.py` | Supported raw-byte validators, identity/status/pending/report checks, recorder, seal and terminal/OR logic; no network |
| `x4_observe.py` | Sole serialized read scheduler, independent deadline/event owner, quote/actor/recovery input and read-only capture. Never performs mutations |
| `x4_adjudicate.py` | Independent offline derivation from sealed originals; never invokes a sender or trusts an outcome summary as source evidence |
| `x4_attended_input.py` | Prompt-time UTC before ask input; never restamps after typing. Separate place/cancel confirmations, event interruption and recovery walkthrough |
| `test_x4_contract.py` | Named acceptance tests, parametrized boundary/failure cases and a deterministic injected transport/clock harness |
| `X4_TOOL_RETURN.md` | Private package manifest, fixture provenance, commands/records, limits and instructions for later coordinator transfer |

Public worker return allowed only at
`docs/notes/2026-09-30-x4-offline-tools-return.md`. It reports scoped synthetic
results and hashes, never raw captures, account details or full vendor text.
No files outside these output paths may be modified; necessary expansion is a
scope finding for the coordinator.

**Producer/state chain:** approved-or-proposed resolved profile/binding →
generator's immutable request+validation pair → independent hash comparison →
observer preflight ticket → human placement confirmation → durable placement
claim → placement handoff → raw response and three-id ownership → unfilled-state
evidence ticket → human cancel confirmation → fresh parent check → durable cancel
claim → cancel handoff → raw order/fill/account evidence → platform recovery
records, if needed → all-terminal OR reconciliation → seal → independent class.
The coordinator accepts the composed behavior; individual helper tests do not.

Persist placement and cancel obligations independently, keyed to one immutable
session identity and canonical attempt root outside run folders. Opening a new
run folder, restarting, regenerating bytes or changing binding cannot grant a
second mutation in that session. A claim/crash before response consumes its
attempt. Never reset the claimed session to obtain a success. Account blocks and
unresolved ownership outlive the read window. Local state is not remote idempotency.

**Defined interfaces:** use these boundaries; internal organization can vary
within the named footprint if the return maps it explicitly:

```python
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from typing import Callable, Literal, Mapping, Protocol

@dataclass(frozen=True)
class QuoteSample:
    ask: Decimal
    captured_utc: str       # captured BEFORE prompt; not a broker tick timestamp
    source: str

@dataclass(frozen=True)
class Operation:
    kind: Literal['place', 'cancel']
    method: str
    path: str              # account and positively identified parent bound here
    body: bytes
    context_sha256: str    # kind + method + path + body hash + binding + session

@dataclass(frozen=True)
class TransportResponse:
    outcome: Literal['HTTP', 'TIMEOUT', 'ERROR']
    status: int | None
    headers: tuple[tuple[str, str], ...]  # original values/order, duplicate fields kept
    body: bytes                         # original body, including malformed bytes
    started_utc: datetime
    received_utc: datetime
    received_monotonic: float
    error: str | None                   # transport error, never a parsed JSON body

class Transport(Protocol):
    def request(self, operation: Operation, timeout_s: float) -> TransportResponse: ...

class Clock(Protocol):
    def utc_now(self) -> datetime: ...  # timezone-aware UTC
    def monotonic(self) -> float: ...

class Operator(Protocol):
    def quote(self, purpose: str) -> QuoteSample: ...
    def confirm(self, exact_text: str, interrupted: Callable[[], bool]) -> bool: ...
    def events(self) -> tuple[Mapping, ...]: ...  # recover, fill, firm, visibility

def generate(binding: Mapping, quote: QuoteSample, out_dir: str) -> Mapping: ...
def handoff_once(operation: Operation, attempt_root: str,
                 confirm: Callable[[str], bool], final_check: Callable[[], None],
                 transport: Transport) -> Mapping: ...
def observe(binding: Mapping, run_dir: str, transport: Transport,
            operator: Operator, clock: Clock) -> Mapping: ...
def adjudicate(run_dir: str) -> Mapping: ...
```

Clock supplies aware UTC plus monotonic elapsed time, and operator supplies
honest quote samples, exact confirmation and independent recover/firm events.
Transport never parses JSON or reconstructs response bytes. For every response,
including malformed, failed and late ones, the recorder first writes the original
body and status/ordered headers/times/outcome to write-once evidence, hashes them
and seals that response record. Only then may validators parse those retained
bytes; the final run seal incorporates the response seals. Duplicate JSON keys
or malformed encoding remain observable and cannot be normalized into success.
Dummy-credential withholding preserves the existing explicit evidence-gap rule;
withheld originals cannot qualify as complete raw evidence. A timeout records the
absence of a response; any later actual response is separately sealed and remains
inert. Capture/seal failure stops dependent processing and cannot manufacture a
terminal classification or permit another mutation. The offline classifier reads
sealed originals and metadata, independently of observer summaries.
No fixture supplies a vendor capability not specified in packet §4. All actual
remote response schemas remain supported-or-unobserved. Transport fixtures
describe synthetic mechanics and cannot prove broker behavior.

## 2. Profile, cancellation and authority requirements

Implement packet §3.1 literally as the named `PROPOSED` profile: quantity one;
entry +100, buffer 25, SL −10, TP +20, realized maximum 20; tick 0.25, point value
$2; placement freshness 10 s and two movement bounds 5; initial evidence 15 s,
normal cancel handoff 30 s, cancel terminal evidence 10 s, unexpected-fill stop
validation 10 s from first observed fill; missing valid protection at that
deadline enters recovery immediately, with detected invalid/rejected protection,
excess realized distance or unexpected quantity entering recovery sooner.
Final recovery-confirmation read window 60 s from recovery entry, window-end precedence, no placement in final 180 s; total 60
read attempts with at most 40 before confirmation and 20 reserved, rolling 60/60,
request timeout 10 s and one actual HTTP request in flight, mutations included.
No read-budget/rate/deadline reset on restart or phase transition. Read counts
include pre-send, retries and abandoned attempts; mutation claims have separate
one-use counts but participate in serialization. The proposed $50 allowance and
H ≥ 2 × (0.04 × R × $2 + applicable fee) are profile data, not automatic safety
evidence. Fee/applicability, headroom, margin, date/window and exact account/
contract remain operator-produced private inputs for later live readiness.

The build has **no operational production transport**: injected in-memory
fixtures only, real HTTP/socket admission refuses. Keep an interface for a
separately reviewed live transport, but do not add an HTTPS send implementation
or an escape flag here. Synthetic approved fixtures exercise control mechanics;
the default PROPOSED profile and missing private approvals refuse operational
admission. Builder/reviewer ratification is impossible by design and by scope.
Tool readiness for a later live transport remains a disclosed later dependency.

Separate exact confirmations: `SEND <validated-request-hash-prefix>` and
`CANCEL <cancel-context-prefix>`. Cancel digest includes the account-bound path
and parent; `{}` hash alone cannot distinguish orders. Preserve the approved
attended SEND request-byte confirmation; validate placement context separately.
Confirm then refresh
positive identity-bound unfilled `Working` parent status, receipt age ≤5 s,
and recheck interruption/deadline/quote-buffer state immediately before claim
and handoff. Changes/invalidation refuse before claiming when demonstrably not
handed off; any crossed handoff retains an unknown obligation until reconciled.
Quote data cannot be silently refreshed by changing its timestamp.

No placement-movement test blocks a necessary risk-reducing cancel. A buffer
breach, stale required quote or deadline exits the normal REST-cancel path,
invalidates pending normal sends and promptly asks Joshua to use the existing
attended platform procedure. No tool automatically flattens, cancels children,
resends or repairs protection. An already in-flight request stays possibly
effective; late responses are retained inert and no new request overlaps it.
Cancellation snapshot freshness is not an atomic read/cancel guarantee.

After an unknown placement or cancel, fresh account-scoped position and order
reads govern recovery. Even when the account is flat, require Joshua to cancel
**every positively identified live order** (including the parent and orphan
children) through the attended platform. Record this additional actor and its
race with any possibly effective in-flight request. Then confirm from fresh
reads after the last intervention: flat positions, no live orders and terminal
state for every involved id. Retain each unresolved request or missing terminal
state as an OR obligation; a flat snapshot alone cannot discharge it.

Read/record both children by actual supported fields and retained placement
mapping; target `Limit`, stop `Stop`, each `Sell`, quantity one, level and parent
identity bound. Record relationship fields without inventing OCO semantics.
`Canceled` is supported by retained vendor schema; raw `Cancelled`, `Completed`,
`Unknown` or an unrecognized/ill-typed status does not discharge an OR id without
a separately reviewed mapping. Pending*, Suspended and Working remain live.

## 3. Implementation sequence and dependency checkpoint

Execute with `superpowers:executing-plans`; use TDD for implementation. This is
one composed outcome with a review boundary, not separate assignments per file.

- [ ] Premise report and source-pin verification; report missing input or conflict.
- [ ] Return the proposed interface/state-machine design for C1 before coding:
  producer/consumer contracts, mutation ownership, clocks/event precedence,
  raw-response capture/sealing and terminal/OR transitions. Coordinator freezes
  its identity and dispatches refute-first review by someone other than builder.
  Reviewer traces clean cancel, unexpected fill/failed stop, unknown/late response
  and restart through concrete input/state/outcome cases; returns contradictions
  and required invariants. Stop until coordinator accepts the reviewed design.
- [ ] Encode every reviewed transition rule as a local invariant: mutation/restart
  ownership in `test_unknown_cancel_blocks_retry_across_restart`, deadline and
  recovery precedence in `test_deadlines_preempt_prompts_and_late_responses`,
  terminal classification in `test_two_children_cancel_trace_classified_from_sealed_bytes`,
  and capture-before-parse in `test_raw_response_is_sealed_before_parsing`.
- [ ] Write the named failing contract tests with synthetic binding/clock/transport;
  retain meaningful red evidence for absent behavior, not merely collection errors.
- [ ] Implement canonical profile, Decimal level rules and independent request/
  validation integrity. Demonstrate tamper refusal before prompt/claim/handoff.
- [ ] Implement separate one-use placement/cancel obligations and exact context
  confirmations; prove restart/new-folder/changed-binding cannot bypass them.
- [ ] Implement read-only scheduler, state tickets, independent clocks/events and
  inert late-response recording; replay clean cancel and fill/unknown branches.
- [ ] Implement sealing and separate raw-byte adjudication; compare derived
  classes to preserved observer claims and refuse altered/incomplete evidence.
- [ ] Exercise the complete attended-input CLI using injected no-network transport.
  This is scripted tool verification, **not Joshua's attended rehearsal**.
- [ ] Run focused and related-case suites, inspect recorded results and unchanged
  original X-1 pins; return package/hashes to coordinator, stop coding.
- [ ] Coordinator issues the independent review of frozen returned bytes. Reviewer
  reports cases in §4, reproductions and exact evidence; builder repairs only
  returned in-scope findings, then affected evidence is re-reviewed.
- [ ] Return final offline status, limitations and all records. Do not install,
  dispatch a live transport, create real bindings, request CP-3 or advance a row.

## 4. Required tests and concrete acceptance cases

**Hypothesis:** the composed offline tools enforce separate attended mutations,
durable attempt consumption and honest three-order evidence classification.
**Falsifier:** accept only if all required cases pass on the frozen returned
bytes; any unauthorized handoff, retry after an unknown outcome, live-network
attempt or manufactured complete classification rejects offline acceptance.

Synthetic reference R=25000 on a 0.25 grid produces E=25100, SL=25090, TP=25120;
synthetic H=10000 passes the proposed stress gate; H=3000 fails at fee $1.82.
These are invented test inputs, never copied account figures or price observations.
No-fill clean trace uses one parent, one target and one stop with fake distinct
ids, one correlated New, correct child versions and parent links. Record parent
Working / children Suspended before cancel and all Canceled afterward, empty
per-id fills plus final flat/account-wide empty working lists, terminal OR and
sampled host assertions. The classifier emits `OBSERVED_CANCEL_COMPLETE`, an
evidence class with explicit no-PASS/no-authority wording.

| Case / named test | Required observable result |
|---|---|
| `test_mutations_need_human_confirmations` | No handoff without exact SEND/CANCEL for the respective context; wrong-parent `{}` confirmation refuses. Clean injected flow has exactly one place and one parent cancel, no child mutation; observer issues GET only |
| `test_tampering_and_refusal_leave_no_handoff` | Mutate bytes, sidecars, metadata, quote source/time, account/parent/path or profile/binding; either integrity/semantics or final checks refuse before handoff. Operational use with PROPOSED/missing approvals and every real-network attempt refuses; frozen request bytes remain unchanged |
| `test_two_children_cancel_trace_classified_from_sealed_bytes` | Recompute all three identities/versions/statuses, fills/positions, final terminal OR from raw sealed bytes. Child Working/Suspended after terminal parent yields `CHILD_REMAINS_LIVE`, not complete; missing/pending/unknown/unsupported state or incomplete capture yields `EVIDENCE_INCOMPLETE`; changing outcome.json alone cannot manufacture success |
| `test_unknown_cancel_blocks_retry_across_restart` | Timeout/unclassified cancel result creates `CANCEL_UNKNOWN`; no automatic retry, new-folder retry, changed-binding retry or resend after restart; original attempt remains owned despite flat snapshots. Terminal evidence can reconcile it but never reopens the consumed attempt |
| `test_deadlines_preempt_prompts_and_late_responses` | Missing valid protection at first observed fill +10 s enters recovery immediately, even during blocked input/read; invalid/rejected protection enters recovery when detected. Final confirmation stops at recovery entry +60 s without delaying intervention. Buffer breach, deadline, firm/recover event or new fill interrupts a blocked human prompt and invalidates pending normal cancel. Monotonic clocks continue during I/O/Retry-After; late bytes are inert; first observed fill starts immutable fill clocks; no second HTTP request while the abandoned one is in flight |
| `test_raw_response_is_sealed_before_parsing` | Exact malformed/non-UTF8/duplicate-key body bytes and status/ordered duplicate headers are write-once captured and response-sealed before any parse. Failed and late responses retain originals; late processing is inert. Capture/seal failure refuses dependent processing; changed raw bytes/metadata or a credential-withholding gap cannot yield a complete class |
| `test_offline_tripwire_blocks_real_network` | In-memory transport handles every scenario; attempts to use sockets, urllib/HTTP or a host/broker subprocess fail and are counted. No bearer token is read; dummy-token echoes are withheld without erasing evidence-gap records |

Also parametrize: quote ages 10 / over 10; each movement 5 / over 5; buffer 25
/ greater than 25; status receipt age 5 / over 5; realized distance 20 / over 20;
initial deadline 15, handoff deadline 30, cancel deadline 10, unexpected-fill
stop-validation deadline 10, recovery-confirmation window 60 from recovery entry,
window final-180 boundary; off-grid/nonfinite values; duplicate New/child ids;
one child missing; target versus stop swapped; parent fills before confirmation,
during the final GET and after cancel handoff; one child fills; flat with orphan;
terminal parent with pending child; more-than-one position or competing order;
firm cancel/liquidation; rate_limited / snapshot_refresh_pending retry only if
allowed and within budget/deadline; broker_rate_limited / egress_limited means
no further REST reads; failed/late first per-order read; attempt 40 and total 60;
crash before claim, after claim before handoff and after handoff before response;
thread completion is never inferred from a timed join. Recovery prompts are
conditional: actual open exposure → attended intervention; already flat → no
flatten, but cancel every positively identified live order through the attended
platform; unknown → read first; missing terminal evidence → retain OR.
The **flat with orphan** case must assert attended cancellation of every
identified live orphan (and any live parent). The **terminal parent with pending
child** case must assert attended cancellation of every identified pending/live
child even when positions are flat. Both cases must assert the additional
actor/race record, fresh post-intervention terminal confirmation for all involved
ids, and retained OR obligations wherever that confirmation is missing.

No clean GC-4 class after any unexpected fill, buffer/deadline abort, firm
intervention, malformed data or missing mandatory evidence. Sampled reads and
operator-attested watching are not continuous competing-order/buffer coverage.
Budget success never proves safety of vendor-side dependency requests.

Verification commands from the checkout tested:

```powershell
.\fp.ps1 doctor
.\fp.ps1 --workers 2 python -m pytest local_artifacts/route-drills-2026-09/tools/x4-v1/test_x4_contract.py -q -p no:cacheprovider
```

Run a serial synthetic CLI/restart replay as well to exercise shared durable
session state; concurrent independent tests must have distinct attempt roots.
Related-case regression: select the accepted X-1 generator/sender integrity,
clock, rate-limit, late-response and pending-terminal suites covering reused
helpers, copied byte-identically into the private test-reference area if required
for imports. Compare their source pins before/after. Do not modify accepted X-1
tests to obtain a green result or claim the entire repository suite passed.
Read actual record.json/JUnit, including failed attempts. Completion requires
completed/exit-zero/stable-source/complete-capture and valid reports, not record
existence. Retain interpreter, tested commit/dirty state, explicit hashes,
command, fixture provenance, no-network count and results.

## 5. Forbidden moves

- No real account/host/vendor calls, browser control, credentials, .env or private
  account/capture files; no locked Pine/runtime port reads or external model service.
- No operational HTTP implementation or calls, websocket/feed adapter, GUI quote
  scraping, automatic reference renewal, timestamp refresh or synthetic live attestation.
- No changes to frozen controls, strategy parameters, accepted X-1 tools/seals,
  campaign/STATE/owner verdicts, standing hooks/instructions or acceptance criteria.
- No real payload generation, primary installation, human-rehearsal claim,
  orders/cancels, arm/deploy, spend, commit/push/PR or acceptance of proposed rulings.
- No remote exactly-once, race-free, continuous-observation, latency-bound,
  economic-equivalence or unattended-operation claim from the synthetic build.

## 6. Output, independent review and four-state return

Deliver the accepted C1 design identity, independent refute-first findings and
coordinator disposition, with each reviewed transition mapped to its local
invariant test. Deliver private source/test hashes, write-once package seal, resolved synthetic
profile digest, original fixture runs including failures, launcher records,
red/green evidence and CLI/restart traces. Public return references hashes and
scoped outcomes only. Coordinator must retain the complete private package in
the primary private root and verify actual file hashes **before** the build
worktree is removed; that transfer/installation is excluded from this worker card.
The independent reviewer checks the copied candidate bytes and supplies its own
reproducers/records. Independent review is a required later dispatch within the
overall outcome, not authority conferred by the builder's report.

Use exactly one of `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, `BLOCKED`.
The offline acceptance verdict is `RESOLVED` only after the accepted C1 review
and separate final frozen-byte review close all required cases; it is `AMBIGUOUS` while evidence or review is missing,
and `FALSIFIED` when a required control fails. These are offline verdicts only.
`DONE` requires all selected offline acceptance evidence and no unresolved
in-scope findings; a builder return pending independent review is
`DONE_WITH_CONCERNS` with review outstanding. `NEEDS_CONTEXT` identifies the
specific governing/source/authority contradiction. `BLOCKED` states the external
dependency that prevents this slice, not a general difficulty. Each return names
selected outcome, evidence, remaining dependencies, changed files and the stop
boundary. None establishes live route acceptance or permission to advance.

## 7. Stop conditions

Stop dependent work on a source-pin mismatch, absent committed handoff, private
account-data requirement, missing vendor semantics needed for an asserted
validation, required out-of-footprint change, attempted real transport, accidental
credential exposure or consequential profile/authority conflict. Preserve evidence,
report to the coordinator and continue only independent work still inside scope.
After two failed corrections of the same mechanism, follow AGENTS.md's escalation
rule rather than a third repair loop or criterion relaxation.

## 9. Dispatch and premise record

Current disposition: uncommitted draft; executor/reviewer not appointed, no build
started and no source transfer. At actual dispatch the coordinator records the
committed SHA containing this card and the packet, successor dirty state if any,
named seats, private reference-package pin verification and environment result.
The executor's Phase 0 return compares the actual frozen text to those sources.
Any changed intended behavior returns before coding. Do not fill this record
with a historical revision that lacks the selected requirements.

## 10. After return — coordinator retains the next decision

Coordinator evaluates the independently reviewed **offline** result and missing
production transport/admission work. It may prepare a separate bounded live-
transport readiness assignment after recommendations are ratified, then exact-
tool attended rehearsal, fresh private binding/session gates and X-4 CP-3.
No next slice is selected by the worker. Operator actor/profile decisions and
session-specific GO remain separate from the successful build. No automatic
unattended use, X-1 resend or broader deployment is inferred.

Coordinator audit of this card's structure, separate from tool acceptance:

```powershell
.\fp.ps1 python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-09-30-x4-offline-tools-build-review.md
.\fp.ps1 python scripts/check_brief.py docs/briefs/handoffs/2026-09-30-x4-offline-tools-build-review.md --type handoff
```
