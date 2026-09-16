# PR 409 Slices C and D Implementation Handoff

> **For agentic workers:** Read the governing spec and current production code before designing changes. Draft separate interface-level implementation plans for C and D. When implementation is authorized, execute with `superpowers:executing-plans`. One coordinating implementer owns integrated acceptance; bounded contributors do not independently establish completion.

**Goal:** Complete evidence-gated Aegis takeover, fresh-account-only synthetic activation, explicit legacy migration and combined correction acceptance without reopening Slice A/B safety decisions.

**Architecture:** Retain the account owner, serializer, SQLite journal, capacity reducer, runtime and listener. Extend the independent synthetic producer to supply the evidence takeover actually needs. Keep observation, capacity accounting and authority separate.

**Tech stack:** Python, SQLite, pytest; preserve the Python 3.11 floor and existing module boundaries.

**Spec:** [Approved bounded correction](../../spec/2026-09-16-pr409-bounded-execution-correction.md), especially sections 5–8; [rev9 halt/resume contract](../../spec/2026-09-14-tb-s3-halt-resume-contract.md); [Slice B implementation and acceptance record](2026-09-16-pr409-protection-correction.md#7-implementation-and-acceptance-record-2026-09-16).

**Status:** Draft handoff, grounded at `567a583`. This document does not implement C/D or settle their new evidence/schema interfaces. The current request is documentation only. No push, deployment, production activation or recovery is authorized by this handoff.

## 1. Repository and accepted baseline

Work in the existing isolated checkout:

```text
C:\Users\joshu\multi_firm_operations\.worktrees\phase2-four-leg-execution
branch: codex/phase2-four-leg-execution
HEAD:   567a583 fix(book): bind protection to owned occurrences and broker evidence
prior:  c8476c8 test(book): retain zero-offset rejection and close Slice A evidence
prior:  26636b8 fix(book): fence malformed ingress before downstream effects
```

The main checkout is separate; do not transplant edits into it or reset it. At handoff drafting, the worktree has no tracked implementation changes. Untracked `tmp-slice-a-*` and `tmp-slice-b-*` files are retained evidence; preserve them. This handoff itself is an uncommitted documentation addition.

Slice B was committed locally and not pushed. Last recorded remote head was `fc7cdc7`; remote state was not refreshed while writing this handoff. Inspect current branch/worktree/remote divergence before future integration; do not infer actual-head CI readiness from local tests.

Verified Slice B evidence, with overlapping counts kept separate:

| Check | Result |
|---|---|
| Full `tests/ops` | 2,479 passed, 15 skipped; skips require absent private ports/effective inputs |
| Synthetic + ingress + emulator, optional signing imports blocked | 174 passed, no skips |
| Image manifests and image-validation tests | 23 passed |
| Repository check-tier and commit hooks | Passed |

Runtime tests used Python 3.13.2. Installed interpreters were 3.13/3.14; syntax-floor checks do not establish execution under 3.11. Image tests establish packaging inventories, not a Docker build or live route.

## 2. Decisions to preserve

- Offline synthetic work only. No live transport, deployment, arming, production trading or general incident-recovery protocol.
- Keep Slice A numeric validation, including exact integer trailing parameters and rejection of zero trailing offset. Joshua explicitly directed retaining rejection until intended strategy behavior is established. Do not normalize, clamp, relax validation or edit private strategy ports to make compatibility tests pass.
- Do not change sizing laws, accepted book priorities, allocation, protection-tier or calibration constants. Read actual policy/sizing code before touching admission.
- INTERVENTION permits observation/bookkeeping only. No automatic cancellation, close, amendment, attachment or Aegis send after the fence; a late fact never restores authority.
- Preserve immutable historical action, operation, attempt and fact identities, pending obligations, FIFO allocations and delivered-feedback checkpoints.
- Every executable action has explicit source occurrence provenance. Equal-content controls at different occurrences are distinct; redelivery cannot expand its frozen scope or resend an attempted child.
- A consumed protection owner never becomes bare again. An owner can remain live after FIFO exhausted its original lot. Preserve active trailing anchors and unchanged components.
- A terminal protective execution does not resolve a separate pending amendment: B deliberately retains that obligation/deadline, including on a consumed owner. Do not silently discard it for takeover quiescence or migration.
- Never repair a recognized current schema by silently creating a missing required table/record. Never recreate a database to obtain a clean fixture.

## 3. Existing code and capabilities

Read these symbols, not just previous plans:

| Files | Current responsibility / important boundary |
|---|---|
| `ops/c1_rail/book_account_owner.py` | `boot`, `_SCHEMA`, `activate_synthetic`, `_dispatch_locked`, ready-takeover admission, `_advance_takeover_locked`, `resume_takeover`, `_retire_takeover_db`, `_halt_db`, ordinary observations |
| `ops/c1_rail/book_capacity.py` | `Takeover`, `Quiescence`, `CompleteTakeover`, `RetireTakeover`, reservation/terminal/reduction replay; accounting is not broker evidence |
| `ops/c1_rail/book_protection.py` | `ActionOccurrence`, `ProtectionRead`, `ProtectionSnapshot`, `ProtectionExecution`, typed owner targets/component changes |
| `ops/c1_rail/book_protection_owner.py` | Complete scoped evidence validation, original-owner journal, deadlines, atomic protective reductions/feedback and retained obligations |
| `ops/c1_rail/book_synthetic_protection.py` | Independent receipt/application/fill/read state, explicit clock and market prices; offline producer only |
| `ops/c1_signal_daemon/book_runtime.py` | Retained sorted batches/envelopes, ordinary fact handling, takeover continuation, same-runtime unattempted protection continuation, read-only recovery |
| `ops/c1_rail/c1_rail_listener.py` | Typed action/fact/protection boundaries; protective execution does not resume takeover |
| `ops/c1_signal_daemon/book_evaluate_loop.py` | Idle protection deadlines, feed silence, schedule and barrier processing |
| `ops/c1_rail/book_policy.py`, `book_sizing_context.py`, `book_schedule.py` | Actual current policy, admission evidence and schedule predicates |

Existing public interfaces include:

```python
owner.dispatch(action, occurrence=occurrence, now=now)
owner.make_occurrence(producer, event_id, ordinal=0)
owner.advance_takeover(now=now)
owner.resume_takeover(now=now)
owner.observe_protection(snapshot, now=now)
owner.observe_protection_execution(event, now=now)
owner.check_protection_deadlines(now=now)
runtime.redeliver_prepared_boundary(bar_time, now=now)
```

B creates schema 2 for fresh owners and refuses schema 1 without migration. Required new tables are `action_occurrences`, `protection_owners`, `protection_operations`, `protection_facts` and `protection_streams`. `protection_state` still means session-mode state; it is not the working-order inventory.

**Missing capability for C:** `ProtectionSnapshot` enumerates protection and original-fill positions, not all resting/partially filled entry/add orders. The synthetic producer's cancellation application currently records an outcome without implementing independently evidenced cancellation of a pending entry. A transport receipt, `_pending` command map, capacity reservation or empty protection snapshot is not a complete working-order inventory. C must supply and test the missing producer before claiming quiescence.

## 4. Slice C: evidence-gated takeover

**Acceptance outcome:** A retained Aegis request displaces lower-priority exposure only through the persisted sequence below, then sends at most once after complete evidence and current admission permit it.

```text
PLAN -> CANCEL -> CONFIRM CANCELLATIONS -> CLOSE DISPLACED LEGS
     -> CONFIRM QUIESCENCE -> REVALIDATE ADMISSION -> admitted send or refusal
```

### Concrete defects to reproduce first

1. `_advance_takeover_locked` collects cancel and flat actions in the same pass, allowing a close before qualifying terminal evidence for displaced entry/add orders.
2. It constructs `Quiescence(next_sequence, displaced, 0, 0, 0, 0)` from local accounting checks. This does not prove absence of broker working orders, protection or pending requests.
3. The ready-takeover dispatch branch rechecks permission, authority, generation, session and account-evidence times, but does not rerun the complete current admission contract. Audit policy/lifecycle, source/bar validity, settlement, uncertainty and capacity before dispatch without inventing a fresh reservation or resizing from fabricated inputs.
4. `test_async_takeover_completes_and_sends_retained_aegis_once` in `tests/ops/test_pr409_owner_lifecycle.py` currently obtains a flat command before delivering the entry terminal. Replace this forbidden intermediate expectation; preserving the old green assertion is not compatibility.

### Plan and implement in this order

- [ ] Draft C's exact durable phase records, version boundary and evidence interfaces. Name every producer and consumer, account/epoch/scope binding, observation sequence/time, completeness claim, unresolved-operation linkage and replay rule. Publish the full displaced scope before any send.
- [ ] Extend the real synthetic producer with independently tracked entry/add working remainders, cancellation application/terminal evidence, late-fill races and a complete inventory suitable for quiescence. Do not derive its observation from the owner's desired state.
- [ ] Persist cancellation child identities and wait for qualifying terminal evidence for every displaced resting/partially filled risk-add order. Include fills arriving during cancellation in confirmed exposure.
- [ ] Close whole displaced legs in the required lowest-priority-first order only after cancellation is confirmed. Observe real fill allocations, partial/rejected/unknown close outcomes and residual protection. Do not call a leg flat from command acceptance.
- [ ] Build quiescence from complete postdating position and working-order evidence, including protection, plus the retained unresolved-request journal. Zero values must be derived from qualified evidence covering the frozen scope.
- [ ] Revalidate current admission immediately before the retained Aegis attempt. Cutoff may retire an unattempted Aegis request; it may not erase displaced effects, cancellation/close attempts or protection obligations.
- [ ] Exercise the complete producer -> listener/runtime -> owner -> phase journal -> command -> evidence -> accounting/feedback sequence, then independently review C and commit tested work only when integration is authorized.

Likely modified files are the owner, capacity/protection contracts, synthetic producer, runtime/listener and packaging inventories if new runtime modules are introduced. Proposed new test file: `tests/ops/test_book_takeover_phases.py`. Keep one integration owner for the entire trace.

Required C traces: accepted cancellation with no terminal (no close); late partial fill during cancel; duplicate terminal; mixed displaced legs and close ordering; partial/rejected/unknown close; orphan protection; partial/stale/foreign/position-only inventory; unknown in-flight mutation; cutoff before and after displacement; source/evidence invalidation before Aegis; halt between phases; crash at every durable phase/attempt boundary. Replays preserve identities and never manufacture send authority. Missing or failed incident storage must suppress further sends.

**C/D interface:** C must explicitly name the persisted phase/evidence records D will recognize. If C adds required schema structures, version them in C; do not alter schema 2 silently and defer recognition to D. Full legacy conversion remains D's responsibility.

## 5. Slice D: bootstrap restrictions, migration and combined acceptance

**Acceptance outcome:** Only a proven fresh empty account can bootstrap. Restarts, incidents, day rollover, migration and replay preserve HALTED/INTERVENTION and all obligations without sending.

### Concrete defects and fixture conflicts

`activate_synthetic` can write RUNNING/NORMAL after existing mode/time/capacity checks. It does not yet establish a fresh empty account with no historical attempts, incidents or pending work. Existing tests call activation again after activity or restart; for example, `test_book_account_owner.py` contains a restarted next-session activation expecting RUNNING with carried ORB exposure. This expectation conflicts with the approved correction.

Fresh boot also starts HALTED/INTERVENTION. Permission strings alone therefore cannot distinguish a fresh bootstrap candidate from restart/incident recovery. D must specify and durably retain the creation/bootstrap identity and consumption rule. Do not equate empty current exposure with a never-used account.

### Plan and implement in this order

- [ ] Draft D against the committed C schema/interfaces. Specify fresh-account recognition, same-generation idempotence, recognized legacy versions, conversion transactions and failure behavior before editing `boot` or activation.
- [ ] Atomically prove fresh identity, no incidents/attempts/positions/protection obligations/pending work and current binding/time admission under the account serializer. Bootstrap once. An already RUNNING call in the same generation may return unchanged state; it cannot clear or renew authority.
- [ ] Refuse activation after restart, incident, day change or migration, including when subsequent evidence looks flat. Race halt against bootstrap/dispatch through the real serializer. No control-file write, acknowledgment or cache refresh grants recovery.
- [ ] Design explicit migration for recognized historical schemas, preserving old identities, facts, reservations, attempts, occurrences, feedback and unresolved protection/takeover obligations. Historical accepted amendments do not become confirmed protection. Unprovable ownership remains halted and explicitly unresolved.
- [ ] Make conversion atomic and restart-safe. Test interruption before/after commit, repeated conversion, malformed versions, missing structures and corrupted retained records. Preserve unsupported inputs without mutation; unknown/current-schema corruption is not a migration opportunity.
- [ ] Resolve the structural difference between legacy fills and B's required one-original-owner-per-fill invariant explicitly. Define a durable unresolved legacy representation or a recognized quarantined state; do not invent protection parameters, complete observations or clean bootstrap history to satisfy validation.
- [ ] Replace unsafe activation fixtures with fresh single-bootstrap scenarios. Keep carried-position policy arithmetic tests isolated from authority tests; do not patch permission with SQL, replace real predicates with success mocks, or discard coverage merely to make the new guard pass.
- [ ] Run combined A–D acceptance, independently review the whole correction, and record revision-bound local/remote evidence separately. Push/current-head CI only with applicable authorization; no deployment follows from test success.

Likely files: owner boot/schema/activation, any C schema modules, protection journal validation, runtime recovery, and tests for owner lifecycle, settlement integration, occurrence identity and retained protection. Proposed new test file: `tests/ops/test_book_bootstrap_migration.py`. Preserve settlement attachment/record-only behavior while correcting fixtures that previously depended on unsafe activation.

Required D traces: fresh empty bootstrap; repeat RUNNING same-generation no-op; incident while empty; ordinary and protection attempts retained; consumed owner with pending amendment; restarted clean-looking account; session rollover with carried exposure; migrated legacy accepted/unknown amendments; migrated pending takeover; failed/interrupted migration; missing current-version table/owner record; observation and feedback recovery without rearm; halt racing bootstrap and dispatch. Every forbidden path keeps authority revoked and sends nothing.

## 6. Verification and handoff discipline

Start with these existing suites and add C/D tests to the targeted command once created:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'
$env:PYTHONUTF8='1'
& 'C:/Program Files/Python313/python.exe' -m pytest tests/ops/test_book_occurrence_identity.py tests/ops/test_book_protection_producer.py tests/ops/test_book_protection_ownership.py tests/ops/test_book_protection_evidence.py tests/ops/test_book_protection_lifecycle.py tests/ops/test_book_protection_review.py tests/ops/test_book_runtime_occurrences.py tests/ops/test_book_account_owner.py tests/ops/test_pr409_owner_lifecycle.py tests/ops/test_pr409_review2.py tests/ops/test_pr409_review3.py -q -p no:cacheprovider
# Record $LASTEXITCODE immediately; stop and investigate any failure.
& 'C:/Program Files/Python313/python.exe' -m pytest tests/ops/test_c1_signal_daemon_image_manifest.py tests/ops/test_c1_rail_image_manifest.py tests/scripts/test_c1_image_validation.py -q -p no:cacheprovider
& 'C:/Program Files/Python313/python.exe' -m pytest tests/ops -q -p no:cacheprovider -ra
& 'C:/Program Files/Python313/python.exe' scripts/gate_manifest.py --tier check
```

On this host, pytest required access to installed dependencies outside the sandbox; request the appropriate command escalation if that recurs rather than treating missing sandbox-visible packages as implementation defects. Run new synthetic scenarios without private inputs and with optional signing imports blocked. Report skips and actual interpreter availability honestly.

Keep both failing-before and passing-after evidence. Test intermediate commands and retained obligations, not just eventual flat exposure. Exercise stateful producer observations, not hand-authored zero proofs. Refresh tests affected by subsequent edits and inspect final diffs. Do not add counts from overlapping suites or use synthetic evidence to claim live capability.

The next implementer should first deliver C's concrete interface-level plan; D's detailed migration plan follows C's committed schema. Independent D audit and bootstrap reproductions can be prepared earlier, but final migration/integration acceptance depends on C. This handoff fixes required outcomes and identifies design work still owed; it does not label absent producers or migration APIs as implemented.

## 7. Draft review record

Grounded against `567a583`: owner takeover/activation/boot paths, capacity proof types,
synthetic producer cancellation behavior, policy definitions, listener/runtime boundaries,
existing takeover/activation tests and the approved correction/rev9 contracts. The main
inherited conflicts are explicitly called out rather than copied into new acceptance.
No implementation or runtime test was run for this documentation-only handoff. Confirm
the current tree and any intervening changes before execution.
