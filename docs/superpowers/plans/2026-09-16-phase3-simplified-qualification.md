# Phase 3 Simplified Qualification Implementation Plan

> **For agentic workers:** Execute with superpowers:executing-plans; use superpowers:subagent-driven-development when bounded delegation is useful and authorized. Preserve the behavioral contract and integration owner. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce one defensible fixed-book E1 qualification result, and on PASS its seal, D0 admission and separate ORB decision, with the agent handling evidence assembly and the operator handling substantive decisions and required signatures.

**Architecture:** Reuse the existing qualification controller, retained-source factory, attempt journal, trust domains and authenticated result/seal interfaces. Present one generated preparation packet over the existing F01–F52 requirements inventory; it is a view of evidence, never a second authorization system. Execute the frozen stages through the existing controller once, with exception-driven reporting.

**Tech Stack:** Existing Python qualification libraries, pytest, Markdown governance artifacts and ignored private evidence storage; no new service, scheduler, dashboard or database.

**Spec:** The design contract in this document, read with `docs/superpowers/plans/2026-09-15-deployment-phase-breakdown.md`, `docs/superpowers/plans/2026-09-15-phase3-completion-handoff.md`, and the accepted successor of `docs/briefs/pre-registration/2026-09-12-track-b-final-validation-prereg.md`. The latter and the preparation evidence currently reside in `.worktrees/phase3-f1-preparation`; resolve their accepted revisions before execution. The approved settlement/order-feasibility design in PR 411 supplies context for later release scope, not qualification evidence.

## Global Constraints

- **Status: PROPOSED, planning only, 2026-09-16.** This document issues no freeze, exact-depth approval, attempt, source acceptance, admission, ORB GO, merge or live authorization.
- Preserve the fixed book, accepted risk controls, preregistered statistical criteria, stage order and distinct approval scopes.
- The preregistration states: “The exact-depth second ratification follows TB-F1 and precedes TB-E1.”
- The preregistration states: “A merge of this draft does not freeze its proposals.”
- Use pristine E1 unless an alternative sealed initial state receives its required approval. Fresh B7 and sole n3 belong to deployment Phase 6.
- Qualification values, curves, source code and account evidence remain private under the governing publication policy. The public packet contains permitted identities, verdicts and counts only.
- No repeated outcome-bearing stage, replacement sample, silent depth reduction, outcome-driven model change or automatic recovery from ambiguous dispatch.
- Keep existing signing authorities and enrolled keys separate by scope; the agent does not manufacture approval or attest its own result as an authorized producer.
- Preserve the paused Phase 3 worktrees and other agents' changes. This plan does not resume the previously paused engineering or qualification run.

---

## Design decision

Simplify coordination rather than replacing the execution machinery. Phase 3 becomes four work packages, delivered by one integration owner:

1. Accept one integrated engineering baseline.
2. Assemble one decision-ready freeze packet.
3. Obtain sequential freeze/depth approvals and execute one E1 attempt.
4. Close the result; on PASS, seal it and prepare D0 and the separate ORB decision.

The coordinating agent owns end-to-end integration, evidence freshness and the handoff. The operator owns remaining material model choices, compute/depth decisions and assigned approval scopes. Authorized result/signing roles retain their existing responsibilities. A contributor's passing tests do not establish combined acceptance.

The packet is ordinary generated Markdown assembled from existing validators, retained evidence and journal inspection. Start with agent-operated assembly and the existing libraries; do not build a generic workflow engine or new packet schema. A new CLI is unnecessary for this phase. If repeated assembly proves costly, a later read-only renderer may be proposed independently.

### Operator contact model

| Occasion | Agent prepares | Operator or authorized signer does | Ordering constraint |
|---|---|---|---|
| Resolve remaining material choices, only if any remain | One consolidated list with evidence, recommended disposition and consequence of withholding | Resolve source/model/schedule choices and any proposed scope amendment | Decisions must precede the freeze; administrative missing files are agent work |
| Freeze and execute | Complete reviewed candidate, measured budget, exact bytes and signing subjects | Approve F1; then review/sign the exact-depth subject derived from that actual frozen contract | Sequential approvals can occur in one sitting, but cannot be pre-signed or combined |
| Review the outcome | Actual adjudicated result, authentication/seal subjects, then D0/ORB evidence as available | Authorized producer attests the actual result; authorized seal signer signs PASS; operator makes the separate ORB decision | Each subject exists only after its prerequisite; D0 review/merge follows its own authority |

These are interaction windows, not a promise of three signatures or one uninterrupted session. A rejected choice, failed test or missing fact does not create more routine check-ins: the agent reports the specific blocker once, with the next required action. An unavailable signer may split the final window.

### What is simplified now

- Reuse prior approvals within their actual scope; ask again only for changed, expired or uncovered subjects.
- Reuse F01–F52 as the requirement identifiers; retire duplicate checklists as operative views after this plan is approved.
- Present changed or unresolved items first. Keep complete evidence links available without making the operator reconcile documents.
- Run legality, n1, n2/Part B and Part A through `run_production_e1`; do not ask the operator to start each stage.
- Keep progress and durable status readable without reopening, reserving or dispatching an attempt.
- Freeze the monitoring battery's definitions in Phase 3. The preregistration calls these post-deployment diagnostics/monitoring, not additional n3 acceptance tests. Preserve any separately named execution obligation at its actual owning gate; do not confuse the original campaign's phase numbering with deployment Phases 1–6.
- Retain the existing monitoring scope by default. Removing descriptive studies is an optional preregistration amendment requiring its own decision before F1, not a prerequisite for this simplification.

## Current evidence and dependencies

This is a dated snapshot, not a readiness declaration:

| Item | Observed state | Required disposition |
|---|---|---|
| PR 409 task, “Document PR 409 Slices C and D” | Slice C pushed; Slice D undergoing fixes/review, including preservation of unresolved protection obligations and bootstrap/halt behavior | Consume the final accepted successor and its applicable combined evidence; do not duplicate, alter or declare its work accepted |
| Phase 3 preparation | Preserved at `35fae36169f056600286081c44edcc53bf618880`; last engineering checkpoint `8f09a6266be671890cf4e0693664612eeded7a8a` | Inspect and integrate selectively onto the accepted baseline; historical component passes are insufficient |
| Preflight/G5 recovery | `f9ff974` in `.worktrees/phase3-qualification-control`, explicitly unreviewed/incomplete | Review exact diff and complete the domain-aware composition; do not broadly cherry-pick the worktree |
| Signed full TEST_ONLY route | Not accepted at the paused checkpoint | Demonstrate the combined retained-source → preflight → replay → adjudication → authentication/commit → seal route |
| Private successor source/settings/schedule evidence | Bounded historical admission exists; does not automatically establish successor parity | Rebind the actual accepted port/settings/calendar/runtime bytes; resolve chronology and warmup evidence before freeze |
| Depth and compute | Historical numerical proposals and component timings are drafts | Derive proposals from declared assumptions; measure the representative full workload and obtain actual approvals |

PR 409 is an upstream implementation dependency where the governing readiness predicate requires it. Its operational recovery tests do not replace E1 source parity or signed qualification composition. Conversely, pristine E1 does not need a fabricated fresh B7 or facts required only by later live gates. Track each missing fact against its named consuming gate.

## Behavioral contract and evidence flow

| Boundary | Producer and input | Consumer and confirmed output | State authority |
|---|---|---|---|
| Preparation | Accepted implementation/source owners supply revision-bound reports, retained bytes and approvals | Coordinator assembles the F01–F52 packet; unresolved evidence remains explicit | Original evidence and governing contracts; packet has no authority |
| F1 | Operator's valid freeze approval plus complete candidate and observed inventory | Existing G1 validator produces `ValidatedFrozenContract` in the enrolled trust domain | Authenticated contract bytes and identities |
| Exact depth | `exact_depth_subject(contract, attempt_id=...)` derives subject from actual F1; operator signs that subject | `validate_e1_preflight(...)` validates approval and reserves a previously unused root, returning `PreflightReceipt` | Authenticated approval, receipt and subsequently bound attempt journal |
| Execution | Accepted retained `ProductionSource`, frozen contract, preflight and matching store | `run_production_e1(...)` dispatches frozen stages and returns the execution/result evidence | `AttemptStore` owns durable dispatch/checkpoints; controller owns ordering |
| Result | Existing adjudicator validates actual evidence; authorized producer supplies result authentication | `authenticate_result(...)` then `commit_authenticated_result(...)` authenticate and bind the actual result to the journal | Domain-enrolled result authority and committed digest |
| Seal | Committed authenticated PASS plus authorized seal record over exact payload | `seal_e1_pass(...)` produces the E1 seal for that same attempt/result | Separate seal authority; seal grants no admission or activation |
| Admission/ORB | E1 seal, ratifications, exact policy provenance and ORB-specific evidence | D0 admission through its owning process; separate D1 ORB GO or explicit withholding | Registry/governance owners and operator |

Existing API anchors, to be reverified on the final accepted revision:

```python
exact_depth_subject(contract, *, attempt_id) -> bytes
validate_e1_preflight(contract, *, attempt_id, output_root,
                     exact_depth_approval_bytes, trusted_keys, now,
                     trust_domain) -> PreflightReceipt
run_production_e1(contract, *, source, store, preflight,
                  exact_depth_approval_bytes, trusted_keys, now)
authenticate_result(result, authentication_bytes, *, trusted_keys,
                    now, trust_domain) -> AuthenticatedResult
commit_authenticated_result(attempt_store, result, *, trusted_keys,
                            now, trust_domain) -> bytes
seal_e1_pass(result, seal_record_bytes, *, sealed_utc, trusted_keys,
             now, result_trusted_keys, attempt_store, trust_domain) -> bytes
```

These are library interfaces, not runnable CLI recipes. `qualification_cli.py` currently provides read-only `status`; it is not a freeze/run/seal command. In particular, `validate_e1_preflight` creates the output root: never call it to preview the packet. Use `AttemptStore.inspect` for read-only journal inspection; opening a store can claim a boot. The accepted execution recipe must retain these distinctions and the existing source/store construction rules.

## Work package 1: Accept one integrated baseline

**Outcome:** A revision-bound engineering acceptance record establishes that the existing machinery can carry an authenticated synthetic attempt through the complete route without weakening production trust or restart behavior.

**Files:** Existing `ops/c1_rail/qualification/{preflight,seal,orchestration,production_source,production,attempt,trust_domain}.py`; existing `tests/ops/qualification/{test_composition_route,test_controller_seal_integration,test_orchestration,test_production_source,test_attempt,test_trust_domain}.py`; preparation `paused-checkpoint.md`, `tooling-review.md` and `execution.md`.

**Dependencies:** Accepted upstream revision including applicable PR 409 successor evidence; preserved preparation and recovery diffs. This package consumes those contributions rather than assigning work to the ongoing PR 409 task.

- [ ] Record the selected base and accepted dependency revisions; inspect dirty state and preserve all existing work before integration in an isolated worktree.
- [ ] Reconcile the preserved qualification changes against the accepted upstream implementation. Document each retained/rejected recovery change and the requirement it serves.
- [ ] Use the existing signed composition fixtures to expose missing cross-boundary behavior before repairing production code. Record failures against the cases below; do not accept mocked caller-supplied PASS as proof.
- [ ] Complete only the identified integration/security repairs, with a failing test followed by its minimal fix for each defect.
- [ ] Run the focused suite below, followed by the accepted repository's required checks. Obtain independent combined review before calling the baseline accepted.
- [ ] Update the existing engineering evidence record with revision, environment, commands and results. Commit reviewed engineering changes separately from any later freeze or private qualification output under the execution authorization in force.

Planned focused verification, from the integrated worktree:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
python -m pytest tests/ops/qualification/test_composition_route.py tests/ops/qualification/test_controller_seal_integration.py tests/ops/qualification/test_orchestration.py tests/ops/qualification/test_production_source.py tests/ops/qualification/test_attempt.py tests/ops/qualification/test_trust_domain.py -q -p no:cacheprovider
```

Required cases: signed TEST_ONLY full-route PASS; production rejection of TEST_ONLY authority; same key ID with replacement key bytes; cross-domain contract/receipt/result; source bytes changed after retention; path aliases; journal persistence and reopen; loss of receipt after dispatch; mismatched result commit/seal; halt/recovery behavior at the actual integrated boundary. A synthetic PASS establishes engineering behavior only, never private-data acceptance or F1 permission.

## Work package 2: Produce one decision-ready packet

**Outcome:** The operator can review material choices and exact evidence without assembling the qualification package manually.

**Files:** Existing `docs/briefs/phase3-preparation/2026-09-15/{requirements,production-readiness,compute-depth,representative-workloads,freeze-candidate,execution}.md`; existing preregistration and ORB decision document. Create a public-safe `decision-packet.md` in that preparation directory, with sensitive attachments under the existing ignored private evidence root.

**Interface:** The packet consumes original evidence references and F01–F52 identifiers. For every requirement it reports disposition (`SATISFIED`, `BLOCKED` or `LATER-GATE`), consuming gate, producer/owner, exact revision/digest, evidence location and unresolved decision. `LATER-GATE` requires a cited owning gate; it cannot waive a freeze prerequisite. Packet labels never substitute for validator output or approval.

- [ ] Resolve F01–F52 against the accepted baseline once; refresh existing documents by reference rather than copying conflicting requirement lists.
- [ ] Bind the real seven-strategy successor inputs/settings, retained source factory output, continuous initialization/warmup behavior, typed calendars, schedule and full runtime inventory. Preserve explicit coverage limitations.
- [ ] Resolve the between-bar cutoff evidence/model choice and successor ORB settings parity. Missing finer chronology is not supplied by an operator signature; present either actual admissible evidence or an explicit permitted model amendment for review.
- [ ] Prepare sizes from declared assumptions and the existing calculator. Measure representative end-to-end cost including source verification, warmup, replay, Part A, persistence and adjudication; do not call the synthetic component benchmark a full-run budget. Any measurement using outcome-bearing private data requires its governing permission first.
- [ ] Freeze-ready monitoring definitions must include every preregistered partition, replica budget, RNG namespace, perturbation scope, missing-output rule, statistic, cutoff/severity and action/descriptive disposition. Record execution ownership separately from definition readiness.
- [ ] Assemble the candidate bytes and signing instructions. Keep draft exact-depth estimates visibly non-authorizing until actual F1 exists.
- [ ] Perform a consistency review: no unresolved freeze field, no invented source fact, no stale approval reuse, no private result in the public packet, no extra diagnostic acceptance gate. Put any genuinely unresolved operator decisions together at the front.

Acceptance: a reviewer can follow each freeze prerequisite to its original producer; deleting a required evidence reference makes that item BLOCKED; revising a bound input invalidates affected readiness/signing subjects; regenerating the packet cannot reserve a root, claim a boot, allocate a sample or change authority. If source or model choices remain unresolved, deliver the consolidated decisions instead of repeatedly requesting approval for administrative steps.

## Work package 3: Freeze, ratify exact depth, execute once

**Outcome:** After separately authorized execution, one frozen attempt reaches its prescribed terminal or blocked disposition with durable evidence and no stage-by-stage operator dispatch.

**Files/interfaces:** Existing contract/preflight/source/attempt/controller APIs above; update the existing `execution.md` with the tested invocation recipe for the accepted revision. Store original approvals, receipt, dispatch/checkpoints and results in the permitted private roots.

- [ ] Confirm implementation acceptance, source acceptance, full candidate completeness and valid signing authorities. Obtain actual F1 approval and validate the immutable contract.
- [ ] Derive the exact-depth subject from that validated contract and intended attempt identity. Present its depth, budget and identities; obtain the distinct post-F1 approval.
- [ ] Verify the private result location is ignored and unused. Invoke the accepted preflight/source/store setup once, preserving the receipt and matching identities; an existing root is a collision, not permission to overwrite or mint a replacement attempt.
- [ ] Dispatch `run_production_e1` once with its bound retained source, store, receipt, approval bytes and callable clock. Let the controller enforce legality → n1 → n2/Part B and Part A according to the frozen contract.
- [ ] Report only a meaningful blocker, terminal result or required decision. Use read-only status for visibility; do not introduce a monitoring service or require operator presence throughout compute.
- [ ] Preserve all evidence on failure, interrupted execution or uncertain dispatch. Follow the disposition table below; a restart never implies permission to redraw.

Acceptance cases: missing/expired depth approval dispatches nothing; changed contract/domain/source identities fail closed; failed screen prevents later stages; joint n2/Part B cannot become separate draws; budget exhaustion cannot reduce depth; uncertain dispatch/reopen preserves the attempt; concurrent workers cannot acquire independent authority for the same stage. Results are judged only by the frozen criteria.

## Work package 4: Close the result and prepare admission

**Outcome:** The actual result is retained with its proper disposition. PASS yields the exact authenticated seal and an evidence-complete D0/ORB handoff; non-PASS closes or blocks the chain as prescribed.

**Files/interfaces:** Existing result adjudicator and G5 authentication/commit/seal APIs; existing D0 registry/governance files selected by the accepted contract; existing ORB decision document. Resolve those owning paths from the accepted execution inventory, rather than inventing an admission CLI or writing a second registry.

- [ ] Adjudicate the retained output against the frozen contract. Request authorized producer authentication over the actual result bytes, not a predicted PASS.
- [ ] Authenticate and durably commit the result using the enrolled result authority. On PASS only, derive the actual seal payload and obtain the separate valid seal record before sealing.
- [ ] Prepare the exact D0 row and provenance evidence through its existing governance process. Apply/merge only within the execution and merge authorization actually in force; E1 seal alone does not authorize admission.
- [ ] Present the separate ORB decision with its specific supersession evidence. Withheld ORB GO blocks V1/downstream deployment; it does not alter the E1 verdict or remove ORB from the fixed book.
- [ ] Produce a compact handoff identifying F1, both ratifications, attempt/result/seal, D0 state and ORB state, plus the remaining Phase 4–6 dependencies. Stop before V1, B7, n3 or activation.

Acceptance cases: failed or incomplete result cannot seal; result substitution or trust-domain drift cannot commit/seal; missing producer authentication remains blocked; missing ORB GO leaves the sealed result intact but blocks downstream use; no outcome silently creates registry/admission/live authority.

## Exception and restart policy

| Event | Required behavior | Operator involvement |
|---|---|---|
| Missing implementation, evidence or approval | BLOCKED at the owning gate; preserve preparation and identify its producer | Only when the missing item is an operator decision/fact |
| Required field genuinely unfreezable | AMBIGUOUS and closure under the governing contract | New decision required for a successor; do not mistake pending work for unfreezability |
| Statistical/legality criterion fails | Terminal disposition prescribed by preregistration; preserve complete result | Report closure; no request to retry for a better result |
| Corrupt/incomplete artifact or uncertain dispatch | Stop, retain bytes/journal and adjudicate integrity/continuation authority | Escalate once with concrete evidence and allowed choices |
| Implementation or bound input changes after freeze | Invalidate affected chain under its governing change rules | Obtain required replacement authority; no silent rehash |
| Approval expires before a durable dispatch | Refuse that dispatch; retain earlier evidence | Renew only the required subject under the governing process |
| Compute exceeds approved envelope | Stop under the budget/context rule; preserve state | Decide only the permitted next action; no automatic extra paths or fan-out |

## Completion and scope of approval

Approving this design accepts the preparation/execution organization and preserves the named substantive gates. It does not approve draft sizes, unresolved model choices, removal of diagnostics, production source facts, a freeze, a run, a merge or ORB GO. Engineering execution should be explicitly resumed from the existing paused checkpoint before work packages are carried out.

Successful Phase 3 exit requires the authenticated E1 seal, completed D0 admission and separate affirmative ORB GO. A terminal failure closes the qualification attempt without achieving that successful exit; withheld ORB GO leaves the deployment chain blocked. A draft packet, passing component suite or open D0 PR is progress, not completion. The reduced burden comes from agent-owned assembly, reuse of accepted evidence and controller-owned stage sequencing; the evidence and decision boundaries remain intact.
