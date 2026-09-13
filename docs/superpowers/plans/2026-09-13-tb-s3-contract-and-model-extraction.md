# TB-S3 contract and model extraction implementation plan

> **For agentic workers:** Execute with superpowers:executing-plans; use superpowers:subagent-driven-development when bounded delegation is useful and authorized. Preserve the behavioral contract and integration owner. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Reconcile PR 360 and replace the unaccepted PR 365 candidate with three dependency-ordered review units.

**Architecture:** The producer owns external facts; the primitive kernel owns durable obligations and recovery; account orchestration composes those primitives. The coordinating agent owns integrated acceptance. Split by observable guarantees, not historical review rounds.

**Tech Stack:** Python, pytest, GitHub PRs, Markdown contracts.

**Spec:** `docs/spec/2026-09-12-c1-multi-leg-rail-extension-spec.md` rev 6, §2e.

## Global constraints

- Test-only extraction: no production control or policy constant changes.
- No merge, deploy, arm, emit or feed authorization.
- Preserve PR 365 at 23cf0e1 and its uncommitted round-7 candidate.
- Start replacement branches from actual origin/main, not stale local main.
- Missing live producer guarantees remain acceptance dependencies.

## Task 1: dependency map and governing contract

- [x] Refresh PR 358/360–363/365 heads, bodies, checks and discussion.
- [x] Correct stale #358-open dependency wording, preserving other PR body content.
- [x] Reconcile spec §1/§2e and publish the dependency map below.
- [x] Review concrete E1–E3/K1–K3/A1 traces against production inputs; obtain independent review and commit to PR 360.

## Task 2: broker/evidence candidate

**Files:** `tests/ops/tb_s3_kernel/{__init__,broker}.py`, `tests/ops/test_tb_s3_evidence_contract.py`, adjacent `EVIDENCE_CONTRACT.md`.
**Interface:** existing `Clock`, `FakeBroker`, `Evidence`, `Execution`, `Outcome`; `snapshot(sym)` captures facts independently of listener delivery.

- [x] Extract producer from preserved candidate without kernel/daemon imports.
- [x] Exercise snapshot isolation, strict causal order, pending/completed request fences, terminal history, lot identity, bounded close and native protection transitions using literal expected broker facts.
- [x] Run `python -m pytest tests/ops/test_tb_s3_evidence_contract.py -q`; review and publish first candidate from origin/main.

## Task 3: complete primitive candidate

**Files:** `tests/ops/tb_s3_kernel/{kernel,state,rules,provenance,effects,harness}.py`, semantic primitive tests and `KERNEL_CONTRACT.md`.
**Interface:** `Kernel.admit_entry`, `apply_evidence`, `cancel`, `close`, `amend`, `restart`, `reconcile_restart`; persisted effects remain in the same transaction as owners. Completion extension runs during event transitions, never status queries.

- [x] Extract ownership, allocation and all recovery together on the producer branch.
- [x] Separate account orchestration while keeping primitive tests executable without importing the account/daemon layer.
- [x] Map every inherited test to a semantic guarantee; preserve source test names in the extraction inventory.
- [x] Run primitive cases including all restart/crash/reorder regressions. Record inherited unresolved review findings explicitly; do not call a passing suite acceptance.
- [x] Review and publish second candidate based on the producer branch.

## Task 4: account integration candidate

**Files:** `tests/ops/tb_s3_kernel/{account,daemon,account_harness,mutation_check}.py`, semantic account tests and `ACCOUNT_CONTRACT.md`.
**Interface:** `AccountKernel` composes primitive transitions with takeover, kill, EOD, feed and daemon loss; persisted account fields extend the same snapshot. Shared bracket classification remains in the primitive kernel.

- [x] Add orchestration and route only account tests through the account harness.
- [x] Run all extracted tests and compare collection inventory with all 385 inherited cases; no regression disappears silently.
- [x] Run full ops tests, lint and required gates; review integrated boundaries and publish third candidate based on primitive branch.
- [x] Link replacement PRs from #360 and #365; keep #365 unaccepted and preserve historical evidence. The user deleted the babysit task; no recurring automation is created or resumed. CI/review status is reported separately from extraction completion.

## Dependency and acceptance map (2026-09-13)

| Item | Current disposition | Dependency / acceptance gate |
|---|---|---|
| #358 | Merged 2026-09-12 | Historical prerequisite satisfied; not an open merge blocker. |
| #360 | PROPOSED governing execution contract, rev 6 candidate | Operator ratification and independent contract review; no accepted #365 reference. |
| #361 | PROPOSED policy ADR; separate review track | Operator ratification before TB-F1; exact Part A depth ratification before TB-E1; registry admission only under its lifecycle. |
| #362 | Prepared operating procedure | Actual implemented/qualified capabilities and operational gates before authorization. |
| #363 | DRAFT—NOT FROZEN preregistration plus calculator | Existing freeze dependencies remain; calculator extraction is recommended but outside this execution request. |
| #365 | Unaccepted preserved development candidate | Replaced for review by evidence → primitive kernel → account orchestration; no acceptance transferred. |

The last published #365 review found five additional P1 issues after earlier local acceptance. Its 23cf0e1 results and the uncommitted 385-test repair candidate are historical evidence, not proof of completeness. Request-owner/gross-lot compositions and the incomplete retained-close regression remain explicit review questions during extraction.

## Extraction closeout

Published review stack: [#368 evidence producer](https://github.com/Joshua-Asante/first-passage/pull/368)
→ [#369 durable primitives](https://github.com/Joshua-Asante/first-passage/pull/369)
→ [#370 account orchestration](https://github.com/Joshua-Asante/first-passage/pull/370).
All remain drafts. Stage1 starts from actual origin/main `2e8cf9e`; later PRs target
their immediate predecessor. PR365's original head and uncommitted work remain intact.

Independent review accepted this contract reconciliation and bounded extraction
correctness, not the underlying model. It independently repeated producer6,
primitive237 and integrated393 passing cases, and confirmed exact preservation of
all385 inherited parametrized cases. Fullops970passed/13skipped; model pylint9.66;
all five selected mutations detected with a393-case control. See stage3's
`tests/ops/tb_s3_kernel/EXTRACTION_VERIFICATION.md` for evidence and limits.

Model acceptance remains blocked on the consumer compositions explicitly listed in
stage2's `KERNEL_CONTRACT.md`. Contract ratification, hosting checks, integrated
semantic review and live qualification are separate gates. No changes to #361's
policy, #362's operational authority or #363's freeze were made; only dependency
status notes were refreshed. No calculator extraction was authorized in this step.
