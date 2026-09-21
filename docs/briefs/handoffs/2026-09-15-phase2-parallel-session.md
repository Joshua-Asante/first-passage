# Handoff — Parallel Phase 2: integrated four-leg execution

## Assignment and parallel feasibility

Own Phase 2: complete the offline four-leg path through daemon, listener, durable order ownership, confirmed feedback, protection, scheduled flattening, restart recovery and synchronized replay. One integration owner accepts the whole behavior.

**Yes, engineering can run alongside Phase 1.** Start durable orchestration, dispatch fencing, feedback/checkpoint integration, crash tests and replay integration against the accepted contracts with explicitly synthetic account/broker fixtures. Final Phase 2 acceptance requires integration with Phase 1's accepted calendar, settlement producer and admitted candidate bundle identities. Do not mark a fixture-only result as the completed phase.

This document is a draft for the receiving session. Preparing it does not start a task or authorize external sends, deployment or activation.

## Establish the execution base first

1. Read applicable repository instructions; verify current main, open PRs, working changes and active writers. Create or use an explicitly assigned isolated `codex/` worktree. Preserve the primary checkout and other sessions' work.
2. Inspect existing runtime work before implementing replacements. Discovery anchors observed during this handoff:
   - `C:/Users/joshu/multi_firm_operations/.worktrees/stage2-runtime-owner`, last observed `39f4768` on `codex/stage2-runtime-owner`.
   - `C:/Users/joshu/multi_firm_operations/.worktrees/tradeify-runtime-resume`, last observed `077163b` on `codex/tradeify-runtime-resume`.
   - `C:/Users/joshu/multi_firm_operations/.worktrees/tradeify-attended-release`, last observed `1cdfafe` on `codex/tradeify-packet1-startup-coverage`.
3. Treat those as discovery anchors only. They differ in contents; names do not establish ownership, merge status or currency. For example, the inspected older recovery owner explicitly lacks production transport/resume, while the resume checkout does not contain that same module. Resolve branch lineage and accepted successors rather than copying both designs together.
4. Identify the Phase 1 owner and establish one shared-file ledger with base revision, writer and consumer. Phase 2 should own listener/account-owner integration; Phase 1 owns evidence qualification and producer/verifier work. Agree exceptions before editing shared files.

No remote refresh, live-host inspection or runtime test was performed when drafting this handoff. Recorded implementation claims must be checked against the execution revision.

## Read these authorities

Use the latest verified accepted versions, locating newer documents in the Packet 1 worktree above where necessary:

- `docs/superpowers/plans/2026-09-14-tradeify-attended-release.md`, Packet 2 and its current status. The inspected version records **Packet 0 complete** and the attended design frozen in **TB-S3 rev9**.
- `docs/spec/2026-09-14-tb-s3-halt-resume-contract.md`, rev9 or accepted successor, in full. Its exact provider-side actor and dispatch-fence semantics govern.
- `docs/notes/2026-09-14-tradeify-attended-feasibility.md`.
- `docs/superpowers/plans/2026-09-14-stage2-runtime-integration.md`, reconciled against rev9; older automatic recovery assumptions do not override it.
- `docs/superpowers/specs/2026-09-14-recovery-owner-design.md` and the existing observer design, as implementation history subject to current authority.
- Accepted TB-S1/TB-S2/TB-S3, calendar/session, fingerprint and TB-P2 contracts.
- `docs/spec/2026-09-15-tradeify-attended-settlement-contract.md` and `docs/briefs/handoffs/2026-09-14-seven-bundle-runtime-interface-plan.md`.
- Parallel assignment: `C:/Users/joshu/multi_firm_operations/docs/briefs/handoffs/2026-09-15-phase1-parallel-session.md`.
- Phase roadmap: `C:/Users/joshu/multi_firm_operations/docs/superpowers/plans/2026-09-15-deployment-phase-breakdown.md`.

Read production policy, sizing, capacity and protection code first under Rule 0. Reuse accepted laws; historical `core/dd_protection.py` is not the candidate configuration surface. Preserve completed M1 and bounded TB-I1 work.

## Contract and ownership

Trace the actual behavior:

**completed bars -> four adapters -> deterministic barrier -> listener account owner -> shared sizing/capacity -> durable reservation and dispatch attempt -> broker facts -> durable accounting -> confirmed adapter feedback/checkpoint.**

Existing interface anchors, to verify at the execution base:

- `BookStrategy.on_bar(bar)`, `set_mode(mode)`, `on_execution(event)`, `checkpoint()`.
- `size_book_request(request, *, context, binding, policy, now)`.
- `entry_quantities`, `add_quantity`, `book_capacity.apply_event`, `project_capacity`.
- Typed `BookSession`, `SettledClose`, account binding/context and execution events.

The listener owns account serialization and dispatch permission. Pure sizing returns a demand; it does not authorize sending. The durable owner supplies verified confirmed-base/exposure state. HTTP acceptance, observations and intended quantities are not confirmed fills.

| Boundary | Phase 1 provides | Phase 2 provides | Joint acceptance |
|---|---|---|---|
| Session/calendar | Reviewed artifact, digest, exact account/product chronology and `BookSession` producer | Runtime/replay consumption, cutoff/flatten scheduling, stale/missing refusal | Same accepted schedule governs both consumers |
| Settlement | Authenticated evidence producer/verifier and accepted-close semantics | Real listener hook, coordinated durable consumption and account context | Producer-to-listener success/refusal/restart cases; no implicit resume |
| Strategy bundles | Reviewed candidate source/runtime identities, shared-law evidence and admission records | Actual four-adapter integration, execution feedback and checkpoints | Final replay/integration binds accepted identities |
| Execution truth | Phase 1 does not fabricate it | Operation/attempt journal, fact reducer, reservations and feedback | Synthetic facts labeled for offline proof; actual capability evidence deferred to Phase 4 |

If a needed producer is absent, keep the real path closed and record its exact dependency. Synthetic injection must stay a test seam, never an HTTP/config shortcut to trusted production state.

## Work package A — Complete the deterministic four-leg pipeline

- Inventory existing implementations and select one canonical path. Bind Aegis 6J, Striker MYM p250, Vanguard MGC and ORB MNQ without changing the fixed book.
- Connect completed bars and adapter intents through the accepted synchronization/barrier rules. Arrival order must not choose capacity winners.
- Consume trusted session/mode/lifecycle and account context; stale/missing evidence follows the accepted refusal/incident distinction.
- Use shared sizing and capacity functions directly. Preserve confirmed-base add sizing, account-wide reservations, priority and all-or-refuse behavior.

**Acceptance:** concrete simultaneous intents reach the real listener/account owner and produce deterministic accepted/refused decisions, including zero-size cases. No alternative sizing implementation or invented default session.

## Work package B — Durable execution and feedback

- Define/preserve account, boot/generation, intent, operation, attempt and broker-fact identities and their persisted owners before adding sends.
- Persist reservation and attempt ownership before dispatch. Serialize competing operations and revalidate capacity at admission; a prior sizing observation is insufficient.
- Process confirmed partial/full fills, rejections, cancellations, reductions and duplicates using the accepted reducer. Preserve unknown outcomes and unresolved reservations until the required terminal evidence arrives.
- Route every automatic mutation through one permission owner, including legacy exit/flat, protective amendments, takeover and scheduled closure.
- Deliver confirmed execution feedback and persist adapter checkpoints coherently so crashes cannot double-apply a fill or lose its remaining obligation.

**Acceptance:** tests cross real daemon/listener/journal/reducer/adapter boundaries with a labeled synthetic broker. Successful transport alone never creates fill credit; duplicate facts never duplicate exposure or release capacity twice.

## Work package C — Protection, schedule and attended fence

- Apply the accepted settlement-driven protection clock and lifecycle rules without resizing carried positions by inference. Preserve ORB adds-off transition requirements and unresolved cancellation ownership.
- Implement normal entry/add/exit/protection/takeover behavior and the exact approved cutoff/flatten/deadline schedule, including denied-session boundaries.
- Apply rev9 incident authority across every sender. Distinguish normal cutoff's narrow scheduled-exit authority from incident/manual intervention that revokes automatic mutation authority.
- Retain already-sent or ambiguous requests and broker-resident obligations after the local fence. A locally confirmed fence cannot promise remote flatness or cancellation.
- Preserve pure status reads, durable halt state and failure-to-persist behavior. Do not add an independent emergency sender based on older recovery designs.

**Acceptance:** incident during entry, normal exit, takeover and scheduled flatten prevents subsequent unauthorized local mutations while retaining outstanding obligations. Ordinary sizing/capacity refusals are not mislabeled as incidents.

## Work package D — Restart recovery

- Exercise crashes before reservation, after durable reservation, around transmission, after remote execution before local confirmation, and after journal commit before feedback/checkpoint completion.
- Restore account ownership, unresolved attempts, fills/reservations, protection transitions and adapter state from durable records. Reconcile facts without blindly retrying ambiguous requests.
- Boot into the required halted state with fresh epoch/generation. Do not inherit stale activation authority, replay halted-period intents or treat accepted settlement as permission to resume.
- Reuse existing resume/fence primitives where accepted. This phase proves the offline state and authorization boundary; actual alert delivery, operator UI and attended resume acceptance belong to Phase 5.

**Acceptance:** every crash boundary preserves obligations and prevents unauthorized risk. Corrupt/incomplete recovery evidence produces the prescribed halt rather than reconstructed certainty.

## Work package E — Replay equivalence and combined acceptance

- Integrate continuous synchronized replay with the same shared quantity, capacity, protection, priority and calendar rules as runtime. Keep simulated account closes explicitly distinct from real evidence.
- Compare observable decisions and final state using identical input/event sequences: quantities, refusals, reservations, confirmed exposure, transitions, scheduled closure and adapter feedback.
- Cover same-bar contention, partial base/add, cancel/fill races, refused takeover, pending ORB cancellations, stale input, denied/early-close sessions and restart. Retain costs and fill assumptions under the accepted replay contract.
- Once Phase 1 delivers accepted inputs, integrate exact artifact and candidate identities and rerun the affected combined cases. Synthetic calendar/settlement fixtures do not close this dependency.
- Run focused cross-boundary tests, appropriate regressions and current repository-required gates on the exact integrated revision. Obtain independent combined review and resolve its findings.

**Acceptance:** complete offline four-leg behavior and replay/runtime agreement, bound to Phase 1's accepted interfaces and candidate identities. External route guarantees remain explicitly unqualified until Phase 4.

## Parallel sequence and limits

Start **baseline/interface agreement -> A/B -> C/D -> E**, advancing independent pieces where dependencies allow. Phase 1 can finish evidence qualification concurrently. Coordinate settlement hooks early rather than deferring a conflicting interface until final integration.

Write bounded code-level implementation packets against the verified base. Existing accepted components should be integrated, not recreated. One writer owns each shared file; send the Phase 1 owner concrete signatures, fixtures and revision changes through the established coordination channel.

No Phase 2 outcome-bearing qualification run, F1 approval, E1/n3, provider purchase, actual broker send, policy-registry admission, live allocation activation, deployment or arming is authorized by this assignment. Offline dispatch uses a synthetic route. Unsupported real broker behavior is a Phase 4 blocker, not permission to weaken the accepted contract.

Keep private ports/evidence in approved ignored roots and publish permitted identities/digests/verdicts. Confirm private-input availability instead of counting skipped tests as evidence.

## Return packet

Return exact base/head, branch/commits/PRs, integrated prior work and changed-file ownership; actual test commands/results; independent review disposition; and a compact evidence table for pipeline, durable execution, protection/schedule, incident fence, recovery and replay equivalence.

List each Phase 1 dependency as integrated or blocked with its owner/revision. Separately list real-route and attended-operation evidence still owed by Phases 4/5.

Use **Phase 2 accepted** only after the full offline path, Phase 1 integration and combined review pass. Otherwise state the bounded deliverables completed and exact acceptance blockers. Do not stop independent engineering merely because final input acceptance is pending.
