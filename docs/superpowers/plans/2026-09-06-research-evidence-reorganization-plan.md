# Research evidence reorganization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make existing campaign evidence reusable and current instructions easy to follow.
**Architecture:** Codex owns the contract and integration. Claude inventories private assets while Cursor builds independent synthetic tooling against that contract.
**Tech Stack:** Markdown, JSON and Python 3.11+ standard library.
**Spec:** ../specs/2026-09-06-research-evidence-reorganization-design.md

## Global constraints

All boundaries in the linked approved design apply verbatim. No strategy/risk changes, private publication, source moves/deletions, baseline regeneration, replay/search/final validation, merges or deployment. User owns merges. Existing monitoring stays paused. This file is a plan, not evidence that execution has occurred.

## Task 1 — Codex: prepare execution and establish current authority

**Files:** Read the linked design, RESUME-2026-09-06.md in the private audit directory, the current campaign-state document and the two lane plans. During execution modify only:
- docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md
- Private audit reorganization/integration-report.md

**Interface:** Contract v1 is the linked design. Claude owns assets.json and locations.local.json; Cursor owns tooling. Codex does not rewrite their outputs during parallel execution.

- [ ] Verify the execution checkout and applicable repository instructions; establish an isolated implementation branch using the worktree skill. Preserve the current private worktree. Reconcile current public branch/main state read-only before choosing a base; do not assume the old local checkout includes later merges.
- [ ] Read the current campaign plan, resume checkpoint and relevant decision authorities. Build a compact table: instruction, current authority, historical conflicting instruction, disposition. Do not reinterpret risk constants.
- [ ] Add one current operational section to the existing campaign-state file: objective, owner, asset references, admitted versus pending evidence, blockers, next milestone and stopping conditions. Mark historical operational sections as historical by pointers; retain their contents. Preserve STATE/CATALOG roles.
- [ ] Dispatch the Claude and Cursor handoffs below using separate tasks. Claude must run locally; cloud Cursor receives only tracked source-neutral design/plan and synthetic fixtures. Do not use a Codex subagent while claiming it is Claude or Cursor. If either target cannot be reached, deliver its exact handoff for the operator to start and continue independent Codex work.
- [ ] Keep a dispatch receipt with actual destination/task identifiers. Do not claim assignment delivery until confirmed.

## Task 2 — Claude: one private inventory pass

Execute 2026-09-06-research-evidence-claude-inventory-plan.md.
Accept the private inventory separately from tool implementation.
No external publication or automatic admission.

## Task 3 — Cursor: one minimal tooling pass

Execute 2026-09-06-research-evidence-cursor-tooling-plan.md.
Can run in parallel with Task 2 after the contract is read.
A PR, if opened during execution, contains only tooling/tests and follows the applicable PR workflow; this plan does not start a monitor.

## Task 4 — Codex: integrated review

**Files:** private reorganization/integration-report.md, INDEX.generated.md; the existing campaign-state current section.
**Consumes:** Claude inventory/report and Cursor validator/tests.
**Produces:** evidence-backed acceptance of inventory and tooling, plus separately stated backup status.

- [ ] Check lane changes against ownership boundaries; inspect public diff for private paths/parameters/fixtures before publication.
- [ ] Run Cursor's focused tests once in the integrated checkout. Record interpreter, exact command, exit status and source revision.
- [ ] Run validate against private assets.json and locations.local.json. Retain errors as findings; do not downgrade them or edit verdicts to get a green result.
- [ ] Generate the private Markdown index. Confirm no absolute paths leak into it.
- [ ] Trace one configuration to its exact export and original capture evidence; verify all active exports have bindings or explicit gaps in Claude's coverage report.
- [ ] Trace the incomplete and complete Aegis datasets, keeping the complete candidate pending intake review and preserving the volume-revision limitation.
- [ ] Trace ORB code/test/review evidence to its actual replay dependency. Synthetic success must not become source parity.
- [ ] Have a fresh reader answer the four retrieval questions in the design using only the current campaign section and index; record missing links.
- [ ] Permit one focused correction pass for acceptance failures. Defer optional enhancements. Stop for an explicit scope decision if success requires a new service, external dependency, source migration or changed campaign rules.

## Task 5 — Codex: preservation and final handoff

**Files:** private reorganization/backup-receipt.json and integration-report.md.
- [ ] Check for an existing approved private backup destination and procedure. If none is established, ask only for the missing destination/authorization while finishing other work.
- [ ] At an authorized destination, retain a manifest of copied members and their hashes. Restore a small representative registry/evidence sample into a separate temporary location and verify hashes; preserve originals.
- [ ] Record backup as verified only after the copy and restore checks. Otherwise record pending with the exact unresolved dependency.
- [ ] Record inventory acceptance, tooling acceptance, current-instructions acceptance and backup status separately. No global COMPLETE if mandatory preservation remains unresolved.
- [ ] Commit only source-neutral plans/tooling/current-state changes after review, preserving private artifacts locally. Operator retains merges.
- [ ] Stop at reorganization handoff. Resuming replay is a distinct action; no automatic campaign run.

## Delegation messages

**Claude task title:** Research evidence — private inventory.
Read the approved design and Claude plan. Work locally against the preserved study files. Own only the three private inventory outputs listed in your plan. Return coverage, inconsistencies and limitations, never campaign admission.

**Cursor task title:** Research evidence — validator and index.
Read the approved design and Cursor plan. Own only the source-neutral tool and synthetic tests. Do not request or ingest private evidence. Return test evidence and exact commit/files for integration.

**Codex task:** Remain in the current conversation as integrator. No extra orchestration task or competing state writer.

## Acceptance matrix

| Requirement | Owner/check |
|---|---|
| Stable identity and paths separated | Claude records; Cursor contract tests |
| Exact hashes and provenance | Claude records; Cursor streaming checks; Codex integration |
| Claims separated from admission | All lanes; Codex reads current instructions |
| Existing catalog respected | Codex; no new root index |
| Originals preserved | Claude before/after hashes; Codex review |
| Private/public boundary | Cursor synthetic tests; Codex diff review |
| Retrieval without chat history | Codex fresh-reader check |
| Durable preservation | Codex destination and restore receipt |
| Bounded work | One pass per lane, integrated review, one correction pass |

