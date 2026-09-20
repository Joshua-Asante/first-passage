# S1 — Durable campaign budget and recovery state

> Implement only S1. Use superpowers:executing-plans and its applicable implementation workflows. Read AGENTS.md, the entire common execution contract, the governing specification and S1 before editing. Return to the coordinator at this boundary.

**Selected outcome:** One persisted campaign allowance and operation history survive reopen, duplicate calls, concurrent transitions and uncertain completion. No process is launched and no execution authority is activated.

**Prerequisites:** The accepted predecessor is PR425 merge `1e4928360b95812b04725dc1e8da97709d670ff4` PLUS the recovered Task 1a/1b snapshot below. The bare commit is insufficient. All 13 recovered implementation/test files match accepted hashes. Fresh verification has 182 passing tests, zero skips; check passed with three disclosed evidence-store skips and existing advisories. Real Linux enforcement is outside S1; trusted observations are explicitly simulated in its deterministic tests.

**Ownership:** You are the sole S1 implementation owner. The existing task **Coordinate protected E1 execution** is the coordinator and retains slice acceptance, interface alignment and combined campaign acceptance. Independent review and successor selection remain with the coordinator. Do not independently start S2.

**Verification:** From your checkout, run `./fp.ps1 doctor`, then write behavior tests and observe the missing behavior before implementation. On stable final sources run:

```powershell
./fp.ps1 --workers 2 python -m pytest tests/ops/qualification/execution/test_campaign_budget.py tests/ops/qualification/execution/test_campaign_recovery.py tests/ops/qualification/execution/test_campaign_admission.py tests/ops/qualification/execution/test_store.py tests/ops/qualification/execution/test_lifecycle_model.py -q --tb=short
./fp.ps1 check
git diff --check
```

Use the checkout's operations launcher; no system-Python fallback. Retain actual commands, interpreter, exact source identity, completed recorder paths, counts, skips/advisories and any failures. Test actual SQLite transaction interleavings, rollback and reopen. Reuse unchanged predecessor evidence; do not rerun the entire historical campaign suite. Add proportionate checks if changed interfaces require them.

**Checkpoint:** Return a concrete prerequisite or consequential interface/scope conflict before dependent implementation. Routine implementation choices within S1 are authorized. At completion return the exact accepted interfaces and schemas, revision rules, evidence, migration/rollback limitations and an immutable source snapshot. Update the recovered execution plan's progress ledger after recorder closure, marking S1 delivered for coordinator review, not accepted by yourself.

**Return boundary:** Stop after locally verified persisted semantics and the return packet, or a concrete prerequisite/scope conflict. Exclude process launch, Linux counter enforcement, executable admission activation, N1/N2/Part A execution, G5, results, seals, S2–S8 implementation and full campaign acceptance. No push, PR, merge, deployment, account action or statistical-policy change is assigned. Deliver reviewable local changes and a checksummed snapshot; no commit is required.

## Exact predecessor and setup

Recovery packet directory:

`C:/Users/joshu/multi_firm_operations/recovery/full-e1-20260919`

Read `README.md`, `manifest.json` and `SHA256SUMS` there. The snapshot is `full-e1-task1ab-recovered.zip`.

- ZIP SHA-256: `3bfcf1155fa50fa80a2dd40440645ce356cd3954c6dde3b3086bdd09ba16d56e`.
- Manifest SHA-256: `54c9947e7ba5c56b4f57ae6b92a00cf51dfc25e8b0a88b351ee7a022d44631d2`.
- Accepted 13-file source-set SHA-256: `5cee6b6aad3559ec46c3694f3713959bca51bbd94fe6f3ebd84fc64ce299d91c`, calculated as SHA-256 of the sorted compact JSON path-to-hash mapping.

Create a fresh isolated checkout at the exact base commit using the worktree workflow. Verify the ZIP and manifest hashes, overlay only the ZIP's `source/` files onto the checkout with exact bytes, and verify every file against `snapshot_files` in the manifest. Preserve the immutable recovery packet and any unrelated local work. Do not execute the historical replay script. Do not use the stale shared main checkout or an unmodified PR425 checkout as the accepted predecessor.

The ZIP's `evidence/` directory contains fresh complete recorder artifacts. Original verification directories were not recovered; the recovery report distinguishes their archived history from fresh verification. Record your own checkout path and starting hash verification before edits.

After overlay, read these documents in your checkout:

- `docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md` — the complete common contract, S1, cross-slice obligations and E01–E12 mapping.
- `docs/superpowers/specs/2026-09-17-protected-full-e1-campaign.md` — governing specification.
- `docs/briefs/handoffs/2026-09-18-full-e1-task1b-durable-admission.md` — accepted predecessor interfaces and persistence semantics.

For reference, the recovered predecessor checkout is `C:/Users/joshu/.codex/worktrees/full-e1-recovery/multi_firm_operations`. Implement in your own isolated checkout, leaving that predecessor intact.

## S1 behavioral and interface contract

Extend the existing ExecutionStore transaction/database authority through CampaignStore; do not introduce a second database or replace the accepted validity owner. Existing dormant v2 receipts retain their meaning and cannot be activated or assigned fabricated historical usage. Preserve exact v4/v5 readability with additive, exactly validated transactional migration.

Own one durable allowance across admission and later phases: immutable request/profile/budget bindings, original boot/start/deadline, UTC audit value, reservations, settled charges, revision/head, attributed memory/OOM observations, work identities and terminal states. Account for provisional admission before the contract is trusted. Canonical installed phase configuration supplies bounded reservations; do not copy statistical constants or accept worker-asserted CPU as authoritative.

Closed private observation schemas require exact integer and identity checks. Exact settlement is idempotent, conflicting observations reject, and unknown usage consumes its reservation. Boot changes or regressing trusted clocks cause BUDGET_UNCERTAIN. Overrun permanently bars authority. Persist IN_DOUBT before cleanup. RESERVED without START_INTENT can reuse its reservation; START_INTENT/RUNNING without finalized capture cannot reexecute; CAPTURED can only validate saved bytes. VOID serializes with these transitions in the existing transaction.

The proposed CampaignStore interfaces are owned by S1: `begin_admission`, `bind_budget`, `reserve_work`, `settle_work`, `record_work_transition`, `recover_work` and `budget_snapshot`. Use the complete signatures in the execution plan; report the actual accepted signatures on return. Snapshot encoding belongs to `qualification/journal_snapshot.py`. Define authority revision versus accounting observation/settlement precisely, serialize authority-changing work, reserve before obtaining a signing snapshot, and test settlement/publication consistency without implementing actual signing or publication. Preserve N1 snapshot semantics and avoid cyclic digests.

The planned file scope is `ops/c1_rail/qualification/execution/{campaign_store,store,profile,campaign_budget}.py`, `ops/c1_rail/qualification/journal_snapshot.py`, `tests/ops/qualification/execution/lifecycle_model.py`, and the new budget/recovery tests. Necessary consequential changes outside the slice return as a concrete scope finding.

Required cases include one cap across stages, outstanding reservations, duplicate/conflicting settlement, lost counters, wall expiry through downtime, changed boot, concurrent reservation, rollback, both VOID orderings and SQLite reopen/model parity. Preserve the arithmetic vector:

```python
assert remaining_cpu(100, (20,), (60,)) == 20
assert remaining_cpu(100, (20, 60), ()) == 20
```

## Return packet and preservation

Return changed behavior, exact starting/final identities, interface and snapshot schemas, authority/accounting revision rules, test records, remaining dependencies and migration/rollback limitations. State what is implemented versus awaiting coordinator review; do not describe local evidence as Linux or full-campaign acceptance.

Before returning, preserve changed/new source, the updated ledger and verification artifacts in a checksummed packet under a new directory within `C:/Users/joshu/multi_firm_operations/recovery/`, outside the disposable managed worktree. Include an explicit file inventory and the accepted predecessor reference. Do not overwrite the Task 1a/1b recovery packet. The coordinator will inspect the implementation and evidence before accepting S1 and selecting S2.
