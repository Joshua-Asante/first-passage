# TB-S3 kernel redesign — draft implementation handoff

> For the receiving agent: start with the contract decisions and failing traces below. Do not begin by applying the eight review suggestions independently. Use `superpowers:executing-plans` after the contract is accepted; use bounded delegation only when authorized. One coordinator owns acceptance of the combined result.

**Status:** COMMITTED AND PUSHED — after implementation the operator authorized committing, pushing, babysitting and repeated Codex review until no remaining issues. The implementation is in `C:/Users/joshu/multi_firm_operations/.worktrees/pr365-babysit`, branch `codex/pr365-babysit`, pushed to PR #365 at `2eb6c12b10f4bdee5fbd5decacfdb67298cbcfae`. The collaborator's documentation-only merge `8aef391` was preserved before committing. Independent review accepted the bounded offline code; remote CI and fresh Codex review are being followed. No merge or live action has been performed.

**Production-reference acceptance: WITHHELD.** The operator requires a bounded redesign before another patch round. PR #365 must remain unaccepted as a reference for production implementation until all five requirements below are implemented and verified together at the final revision:

1. Represent outstanding obligations individually and derive account-wide blocks from every unresolved owner.
2. Define shared rules for flatness, working remainders and valid protection transitions.
3. Give evidence explicit ordering semantics.
4. Trigger required actions automatically on completion; status queries only report.
5. Test the rules across event sequences, including restart and reordered evidence, with expected outcomes independent of the implementation.

Sections 3–6 detail the proposed decisions, acceptance traces and verification work for these requirements. This hold does not itself settle D1–D4 or establish that the redesign is complete. Acceptance requires the combined contract and sequence evidence, including independent review, rather than another set of isolated repairs or passing CI alone.

**Goal:** Make the test-only kernel a trustworthy reference for TB-I3 by expressing outstanding obligations, evidence ordering and lifecycle transitions consistently, then testing their composition.

**Architecture proposed:** A deterministic transition function consumes commands, transport outcomes, broker evidence and timer events. It produces durable state and explicit effects. Admission and status queries read that state; they do not silently complete operations or clear safety obligations. The fake broker supplies events independently of the kernel's assertions.

**Stack:** Python, dataclasses and pytest; existing `OrderIntent`, `Bracket`, `CapacityLedger` and `Takeover`. Do not add a service, database or dependency merely to implement the model.

**Integration owner:** The receiving coordinating agent. Contributors may own bounded changes, but separate file reviews or passing suites do not establish acceptance of the whole model.

## 1. Starting point and evidence

### Execution result (supersedes the draft work status below)

Latest follow-up: `23cf0e1ef0ca89ad857b159836293def13395656` is pushed to PR #365. All four distinct findings from Codex's `bafdd97` review were reproduced and repaired: post-restart amendment fencing, atomic first attachment, complete trailing fields and known-order risk-field validation. Original PLACE authority and immutable execution provenance now gate per-order allocation, with persistent quarantine for mismatches and explicit offline L-1 history/location guarantees. Independent review also closed foreign-symbol absence, terminal contradictions, history conflicts and mixed-side recovery cases. Forty-six new regressions bring the kernel to 362 passing tests, independently repeated; full ops 939 passed / 13 skipped, lint 9.73/10, final gates and commit/push hooks passed, and all five semantic mutations were detected. Independent review accepted the bounded offline code. Fresh Codex review requested on `23cf0e1` via comment 5651694520; new CI/review remain pending. Production-reference acceptance remains held. The ignored worktree ledger retains all review dispositions and current monitoring state.

All five redesign requirements are implemented together. The model's `CONTRACT.md` records D1–D4 and the exact offline refinements to spec rev 5.6 at `73a3334`. Durable obligations and effects, request acquisition/fences, component attempts, shared quiescence/protection checks, completion-driven disarm, restart schema handling and independent sequence coverage are present. Production `ops/` and `core/` have no changes.

Verified local results: 232 kernel tests; full ops 809 passed, 13 skipped, with two existing seaborn deprecation warnings; check-tier gates exit 0 with public-worktree/private-artifact warnings. Five isolated semantic mutations were all detected: owner overwrite (77 failed), ignored working remainder (4), timestamp without causality (1), ignored protection fields (3), omitted disarm (9). The independent reviewer separately ran 232 kernel tests and found no remaining blocking code findings. Focused lint passed at 9.86/10 and repository-wide lint passed at 8.49/10; the model's final verification record includes the commands and Windows UTF-8 retry.

Review findings were reproduced before repair, including takeover admission bypass, lost broader exit identity, interrupted multi-leg work, never-dispatched entry reservation release/replay, missing restart state, unallocated bare exposure, inactive-trail activation races, incomplete disarm reporting, weak bounded residual checks and late deferred outcomes after scope consumption. Original acceptance tests remain; timestamp-backdating and direct derived-state test fixtures were replaced with actual event traces.

The design/trace checklist below is retained as the original implementation plan. Current implementation and evidence are in:

- `tests/ops/tb_s3_kernel/CONTRACT.md` and `VERIFICATION.md` in the isolated checkout.
- `tests/ops/test_tb_s3_kernel_redesign.py` (regressions and crash boundaries).
- `tests/ops/test_tb_s3_kernel_sequences.py` (96 delivery/restart permutations and cancellation/owner sequences).
- `tests/ops/tb_s3_kernel/mutation_check.py` (reproducible isolated mutation checks).

Production-reference acceptance remains held pending the operator's disposition. Live L-1 equivalent request/evidence ordering, L-2 verification, production disarm acknowledgment and feed-loss ratification remain owed. PR metadata now describes the redesign, and comment 5650804216 requested fresh Codex review at `2eb6c12`. The running follow-up is recorded in the isolated checkout's ignored `tmp/pr365-babysit-ledger.md`; heartbeat `babysit-pr-365-redesign` continues CI and review monitoring.

- PR: [#365](https://github.com/Joshua-Asante/first-passage/pull/365).
- Metadata refresh when recording the operator's acceptance hold: PR open and unmerged, head `dfa185c974b8b2def1591831bbeb0f314bb9b42d`, base `17292651f494d22aa4418c4aae20b132e8cf5619`. This refresh inspected metadata only; the findings and test results below remain tied to their historical reviewed snapshot and must be revalidated against the newer head. The acceptance hold is recorded locally in this handoff; no GitHub review or PR metadata was changed.
- Reviewed snapshot: `f8e39afae6796cbea43b277fc6bd5d808c7a51e9`, including repairs in `21b916fa7a3c3683b901969669b844787c0ae24b` and a merge of main. Refresh the remote before using this snapshot; do not reset over another actor's changes.
- Current task-owned checkout: `C:/Users/joshu/multi_firm_operations/.worktrees/pr365-babysit`, branch `codex/pr365-babysit`. It was clean when the diagnosis was made. Verify again before editing.
- Governing spec inspected: [TB-S3 rev 5.4 at ed70fd8](https://github.com/Joshua-Asante/first-passage/blob/ed70fd8/docs/spec/2026-09-12-c1-multi-leg-rail-extension-spec.md), PR #360. At execution start inspect the latest owning spec and record whether its later revisions already settle the decisions in section 3.
- [Posted prior repair evidence](https://github.com/Joshua-Asante/first-passage/pull/365#issuecomment-5650102958). Nine regressions were added in that repair round. At the reviewed tree: 49 kernel tests and 626 ops tests passed, with 13 ops skips; check-tier gates and lint passed. CI also passed at `f8e39af`. These results do **not** close the new findings.
- All eight behaviors in section 5 were reproduced with the real test model at `f8e39af`. No additional implementation changes for those eight findings were made before drafting this handoff.

Required source reads, at the refreshed PR revision:

| Source | What must be understood |
|---|---|
| `tests/ops/tb_s3_kernel/{kernel,broker,daemon,harness}.py` | Current state, event ordering, synchronous broker effects, operation queues and test conveniences. |
| `tests/ops/test_tb_s3_kernel_{model,findings,review,review_followups}.py` | Existing AC coverage and regressions; preserve behavior, not implementation-shaped assertions. |
| `ops/c1_signal_daemon/book_protocol.py` | Existing sided intents; positive or all-in-scope exit quantities; bracket parameters; execution events. |
| `ops/c1_rail/book_policy.py` | Real reservation accounting and takeover prerequisites. `ack_cancel()` and `confirm_close()` trust their caller's evidence; they do not read the broker. `confirm_fill()` consumes an existing reservation. |
| `ops/c1_rail/c1_rail_telemetry.py` | Existing operator-attested `BrokerEvidence` and ledger persistence. This is not the proposed richer evidence protocol. |
| TB-S3 sections 1, 2/S1–S10, 2d, R-B3, R-M, R-N and section 5 | Authorities, route capabilities, recovery, evidence and the feed-loss ratification boundary. |

Rule 0: these production protocol/accounting sources were read directly for this handoff. Re-read them before changing allocation integration. Do not copy a historical document's description over the current code's contract.

## 2. Diagnosis to preserve

The model encodes named scenarios, but shared safety rules are repeated in different forms. Four defects in the design explain the review pattern:

1. **Lost obligations:** a reason maps to one detail string even when many operations own the block; zero position hides working future exposure; a partial order's executed and working portions are not treated together everywhere.
2. **Incomplete protection transitions:** desired, dispatched and confirmed states are conflated. A multi-component amend has one overall outcome even though its component sends can differ.
3. **Missing causal ordering:** timestamps and receipt order stand in for proof that evidence observed an operation. Cached and newly acquired reads can have equal timestamps.
4. **Scattered completion effects:** polling a status method performs disarm; a later snapshot is needed to react to an already-known attachment rejection; one operation's reconciliation can change shared data before another consumes the same read.

The test process reinforces this: selected arrange/send/advance/snapshot stories miss simultaneous failures, same-time events, partial cancellation, restart between durable boundaries and status-free completion. More examples alone are not the redesign; the state representation must make those cases expressible.

## 3. Contract decisions — resolve before dependent implementation

Produce one decision table in this handoff or the owning spec, with the chosen semantics, concrete trace, source authority and coordinator acceptance. Do not silently make these decisions in helper functions.

### D1. Evidence ordering

The inspected spec expressly allows `as_of >= prepared_at`. The review's global replacement with strict `>` is not automatically the right contract. The real defect is allowing a cached flat read to skip a close after a later fill at the same clock time.

Proposed resolution: retain timestamp freshness, but require evidence coverage/causality in addition to it. Name the read request or broker event and the operation attempt it can cover. A cached equal-time read without that proof cannot complete or skip the operation. A genuinely post-operation read may have the same timestamp. A delayed response is not made current by its delivery time. AC-5's stricter absence-based inference for a never-executed order remains a separate rule.

**Producer:** the test broker/event harness can assign acquisition sequence and broker generation independently of the kernel. **Consumer:** reconciliation and no-op decisions. **Persistence:** accepted evidence identity, operation/attempt boundary and deduplication cursor must survive restart. **Live dependency:** the production L-1 adapter must later document how its actual read/event semantics provide equivalent proof. A synthetic model sequence is not proof that CrossTrade/Tradovate supplies such a field. If that proof is unavailable, leave completion unknown and recovery attended.

### D2. Feed loss with resting exposure

S6 in the inspected spec excludes `CONFIRMED(0)` without addressing a working entry. That is a specification gap as well as a model failure.

Proposed resolution: distinguish **position flat** from **quiescent scope**. Quiescence for a feed-loss or account flatten request requires confirmed zero position, confirmed absence of exposure-creating working remainders and reconciliation of sent/unknown exposure-creating requests. On feed loss, establish the episode's block before dispatching cancellations; include partial remainders. Reconcile a fill racing cancellation and close the resulting exposure through the supported primitive. A cancel rejection or unknown outcome must never be relabeled cancellation success. Retain the session-scoped feed block according to its owner; do not clear it merely because cancellation completed or the source recovered.

**Authority:** route the amendment through the TB-S3 coordinator/spec owner and the existing S6/section 5 ratification boundary. The offline proposal does not authorize a new live action or supersede the live fail-closed rule.

### D3. Protection during mutation

Define valid observed protection per component: the last confirmed parameters, or parameters actually dispatched by a still-unresolved attempt for that component. Never whitelist an unsent component because a sibling amend was sent. Missing protection or an unexplained third value is a gap. Preserve the distinction between accepting a transitional value and confirming the whole operation.

Record dispatch/outcome by component. Compare static stop/limit/trail parameters and quantity/linkage; a native trail anchor may move legitimately and is not a static target. Classify amendments against fresh observed protection. Specify active/inactive trail behavior and combinations of activation/offset changes; if direction cannot be established under the recorded route semantics, defer rather than call it tightening. An attachment rejection after first protection was defined immediately creates an obligation and block; actual flatness still requires broker evidence.

### D4. Completion versus observation

Completion is a state transition with required durable effects. Kill completes only after its cancellation/close obligations are satisfied **and** disarm has been applied. A status query must not be required to make that happen. A model-local disarm state change is not proof of a production configuration write; the future production effect requires its own acknowledgment/read-back contract.

## 4. Proposed state and transition boundaries

Keep one coherent state machine; splitting the current large file is useful only if ownership remains explicit.

| State | Sole authority / producer | Required durable content and consumer |
|---|---|---|
| Broker facts | Broker evidence | Positions, working remainders, cumulative fills, lot allocation, component fields, evidence coverage and acquisition identity; consumed by reconciliation. Intent never writes broker facts. |
| Orders | Transition function from admission, transport and evidence | Requested quantity, cumulative executed quantity, remaining reservation, cancellation attempt and outcome. A partial order has both exposure and an outstanding remainder. |
| Operations and attempts | Transition function | Kind, exact scope, reason/episode, requested reduction, per-attempt dispatch boundary, per-component progress, evidence coverage and terminal disposition. Preserve every independent request identity. |
| Blocking obligations | Transition function and authorized lifecycle events | Key by reason **and owner identity**, with explicit discharge criteria. Derive the account-wide blocked view from every unresolved obligation. Scheduler/operator latches remain until their authorized clear event. |
| Protection | Strategy defines target; broker evidence confirms | Confirmed component set, requested mutations, component attempts, linkage and quantities. Bare-before-first-definition is distinct from failed first protection. |
| Capacity/takeover | Existing ledger through evidence-validated integration | Reservations and confirmed quantities plus the in-progress takeover/cancel obligations needed after restart. Never call `ack_cancel()` for an unconfirmed remainder. |
| Lifecycle | Transition function | Feed episode/session latch, kill phase, disarm effect/acknowledgment and restart reconciliation phase. Timer origins survive restart. |

Proposed transition shape: `(durable_state, input_event) -> (next_state, effects)`. This is a design interface, not an existing API. Inputs have named producers: strategy commands from the harness/daemon; transport outcomes from fake route requests; broker evidence from the independent broker; timer ticks from the clock; operator/session events from explicit harness actions.

Persist next state and planned effect identities **before** dispatch. Feed transport responses and broker reads back as separate inputs. Recovery after a crash between dispatch and acknowledgment must reconcile before reissuing; do not claim exactly-once broker execution from local effect IDs. Model unknown outcomes both when the action executed and when it did not. Do not synthesize a CLOSE to retry an AMEND.

Process one evidence event consistently for all affected operations. An operation must not consume another operation's progress by updating shared lots first. Recompute derived blocks and eligible follow-up effects after applying facts, then persist. Status views are pure. Admission must use the same derived state as recovery and restart.

Proposed file boundaries, all under `tests/ops/tb_s3_kernel/`:

- `state.py`: explicit durable records and obligation identities.
- `transitions.py`: event application, lifecycle completion and effect planning.
- `kernel.py`: existing public facade and compatibility adapters, not a second policy implementation.
- `broker.py`: independent fake broker and evidence acquisition/event control.
- `daemon.py`: source/control observation and command production, without duplicating listener safety decisions.
- `harness.py`: deterministic event scheduling and crash/restart injection.

The coordinator may keep fewer modules if that is clearer. Do not create two independently mutating versions of state during migration.

## 5. Required acceptance traces

Each row needs a regression that fails at the reviewed baseline for the named behavior, then passes after redesign. Link the final test and evidence to its review comment. A test ending at HTTP acceptance is incomplete.

| ID / review comment | Concrete trigger | Required observable outcome |
|---|---|---|
| R1 / `3998394097` | Source becomes stale while an entry is working and position evidence is zero. | Episode block precedes cancellation. No completion while the remainder may fill. A racing fill is accounted for and closed; canceled remainder releases reservation only on confirming evidence. |
| R2 / `3998394099` | Close on symbol A rejected; close on B rejected; B subsequently succeeds. | A's obligation still blocks account-wide admission. The final unresolved owner alone determines whether the reason can clear. Repeat with both failures on one symbol and across restart. |
| R3 / `3998394101` | Flat snapshot acquired; entry fills; close prepared, all at one timestamp. | Cached snapshot cannot produce a no-op. Later causally covering evidence can complete, including at equal timestamp if D1 permits it. Delayed/replayed reads cannot regress or discharge newer obligations. |
| R4 / `3998394102` | Existing protection has the wrong parameter or linkage/quantity, including after restart. | Unexplained mismatch creates a gap obligation. Old/new values justified by actual pending component attempts do not cause a false gap. Mixed component success/rejection retains exact outstanding state. |
| R5 / `3998394106` | First ATTACH to a bare lot is definitively rejected. | Immediate gap obligation and blocked admission without waiting for a new snapshot. Recovery is durably owned and uses supported CLOSE; its outcome is confirmed independently. |
| R6 / `3998394108` | Takeover displaces a partially filled entry with a working remainder. | Remainder is canceled and confirmed, fill/cancel race is reconciled, and requester stays refused until all prerequisites hold. No erased reservation while a remainder can still fill. |
| R7 / `3998394112` | Activation/offset change weakens trail protection while a block exists. | Risk-add classification refuses it. Include inactive and active trails, allowed tightening, mixed-direction changes and anchor-preservation capability limits. |
| R8 / `3998394114` | Kill receives all confirming broker evidence; nobody polls status. | Disarm transition occurs and persists. Reading status zero, one or many times changes neither state nor effects. Clearing the kill latch cannot re-arm the model. |

Preserve all prior acceptance obligations: AC-1–AC-10, bare-lot qualification, close-time crossed-level exit, native trailing behavior, post-operation evidence, accepted versus confirmed outcomes, unsupported-capability refusal, scoped/bounded close quantities, queued broader closes, partial/rejected/unknown recovery, protective-fill consumption, reservation conservation and account-wide blocking.

## 6. Work sequence and deliverables

### A. Freeze evidence and settle the contract

- [ ] Refresh PR, base and spec; record exact revisions and concurrent changes.
- [ ] Turn R1–R8 into minimal failing traces using the current public model facade. Keep the historical behavior visible; do not rewrite assertions to bless it.
- [ ] Resolve D1–D4 with transition tables, input producers and discharge evidence. Identify any spec amendment and its owner. Acceptance of offline behavior is separate from live ratification.
- [ ] Have the coordinator review the proposed state/effect schema against every trace before restructuring the kernel.

**Deliverable:** accepted contract plus failing baseline cases. Do not move to dependent implementation while a required input or semantics is unspecified.

### B. Implement durable obligations and causal evidence

- [ ] Introduce the chosen records and one transition boundary while preserving the public test facade.
- [ ] Route block ownership, partial remainders and attempt progress through those records.
- [ ] Implement D1 evidence admission; test duplicate, delayed and equal-time events and reconstruction after restart.
- [ ] Define the Store schema behavior: either migrate prior test snapshots faithfully or reject them and block pending reconciliation. Never silently boot empty/armed because a record is absent.

**Deliverable:** R2/R3 plus reservation and restart invariants pass; existing behavior outside the changed contract remains covered.

### C. Integrate lifecycle and protection behavior

- [ ] Route feed loss, takeover and kill through shared obligations/effects; include partial remainders and cancellation races.
- [ ] Implement per-component protection mutation evidence, rejection recovery and amendment classification.
- [ ] Make status APIs read-only and drive disarm from the completion transition.
- [ ] Run every acceptance trace across its real producer, transition, persistence, effect and confirming-evidence boundary.

**Deliverable:** R1–R8 and all preserved acceptance obligations pass together. Per-file completion does not satisfy this gate.

### D. Prove composition, not only examples

- [ ] Add a deterministic sequence harness that can separate request acceptance from broker execution and evidence delivery. Snapshots capture immutable broker facts when acquired, not when delivered.
- [ ] Enumerate relevant short sequences: accepted/rejected/unknown request, partial fill, cancel acknowledgment, protective fill, source loss, repeated evidence, restart and status read. Constrain generation to legal broker events.
- [ ] Assert invariants after each transition, not just at the end: no lost block owner; no reservation released without resolving evidence; no risk-add under an obligation; no completion from uncovered evidence; no unowned protection gap; status-query purity.
- [ ] Include two simultaneous owners and overlapping scopes. Insert restart before dispatch, after dispatch/before acknowledgment, after acknowledgment/before evidence and after completion persistence.
- [ ] Compare restarted and uninterrupted traces for broker effects and safety state. Compare permissible independent-event reorderings; do not assume all events commute.
- [ ] Prove tests fail for representative mutations: omit partial remainder, overwrite an obligation owner, trust an equal-time cached read, ignore a parameter, or remove completion-driven disarm. Expected outcomes must not call the kernel's own decision helpers.

**Deliverable:** executable invariant/sequence coverage with reproducible failure traces. Property-based tooling is optional; deterministic parametrization is sufficient when it exercises these cases.

### E. Review and integrate

- [ ] Independently review the complete redesign against the accepted contract, including unchanged callers and accounting dependencies. Re-review affected contracts after repairs.
- [ ] Run the model suite, full ops suite, check-tier gates and configured lint. Capture exact revision, commands, pass/skip results and limitations.
- [ ] Refresh remote/base before commit or push. Preserve other actors' work. Follow the existing PR's integration strategy and use an explicit lease for any authorized rewrite.
- [ ] Report disposition of each review finding and every D1–D4 decision. Refresh CI and conversations after the final push. Do not resolve another reviewer's thread merely to make the queue empty.

## 7. Validation commands and environment

From the selected implementation checkout:

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
& C:/Users/joshu/multi_firm_operations/.venv/Scripts/python.exe -m pytest tests/ops -q -p no:cacheprovider
$env:PATH = 'C:/Users/joshu/multi_firm_operations/.venv/Scripts;' + $env:PATH
$env:PYTHONPATH = 'C:/Users/joshu/multi_firm_operations/.venv/Lib/site-packages'
python scripts/gate_manifest.py --tier check
git diff --check
```

For focused model runs, select all existing `test_tb_s3_kernel_*.py` files and the newly added redesign tests explicitly or with a shell-expanded file list; do not accidentally run only the old four files. CI's lint contract is in `.github/workflows/pylint.yml`.

In this task the sandbox cannot launch the Python 3.11 base interpreter behind the venv; tool escalation succeeds. Windows gate subprocesses can select base Python despite PATH, hence the explicit package path above. These are environment constraints, not reasons to suppress checks or edit production packaging. Public worktrees omit private data; keep legitimate skips visible.

## 8. Footprint and stopping conditions

Monitoring update (2026-09-13T06:38Z): all applicable CI passed on `23cf0e1`.
Codex remains running since06:35:08 via trigger5651694520. The existing heartbeat
continues the authorized fix/push/re-review loop; final clean-review acceptance is
still pending and the production-reference hold remains.

Implementation footprint proposed: `tests/ops/tb_s3_kernel/**`, the associated `tests/ops/test_tb_s3_kernel_*.py` tests and the accepted owning-spec amendments. Update the package's scope description if its modeled contract changes. Preserve useful prior regressions; replacing internals does not justify deleting their guarantees.

Production `ops/` and `core/` are read-only dependencies for this redesign. Do not change sizing laws, protection-policy constants, strategy logic, live daemon/listener configuration, deployment, arm state or external broker behavior. A required production interface change is a dependency to route through TB-I1/TB-I3, not an implicit expansion of this PR. New L-1/L-2 capabilities remain owed rather than being invented by a fake.

Do not claim completion if any review trace lacks a confirmed outcome or explicit durable attended-recovery state; any block owner can disappear unresolved; any effect depends on polling; restart changes safety outcomes; or a required evidence capability has no producer. A reviewer must be able to follow each trace to its outcome using the accepted contract, not just a passing test name.

**Final handoff back:** refreshed revision and diff scope; D1–D4 dispositions and authority; R1–R8 test links; invariant/sequence evidence; independent review result; local/CI validation; unresolved live dependencies; PR merge status. Drafting, implementation acceptance, merge readiness and live qualification are separate outcomes.
