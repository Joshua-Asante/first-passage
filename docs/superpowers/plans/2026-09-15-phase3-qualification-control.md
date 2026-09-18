# Phase 3 G1/G2/G5 qualification-control implementation plan

> **For Codex:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Deliver synthetic-tested, fail-closed F1 contract validation, an exactly-once qualification attempt journal, and authenticated E1 result/seal tooling without freezing F1, running qualification, admitting evidence, or granting deployment authority.

**Architecture:** Keep production qualification authority outside the runner. Canonical immutable inputs are validated from one byte snapshot; detached Ed25519 approvals bind exact digests and scopes. A standalone SQLite journal owns one campaign attempt and two outcome-bearing stages (`TB_E1`, `TB_E2_N3`) with atomic receipts. Result authentication and E1 sealing are distinct external-authority boundaries. Runtime prerequisites share one pure schedule classifier and durably deliver local owner refusals to adapters. Historical Phase 1 admission remains immutable and bounded.

**Tech Stack:** Python 3.12, dataclasses, `cryptography` Ed25519, SQLite (`BEGIN IMMEDIATE`, `synchronous=FULL`), pytest.

**Constraints:** Synthetic evidence only. Do not execute F1/E1/n1/n2/Part A/n3, freeze a contract, create a production signature, admit a registry record, send live orders, deploy, activate, merge, or reset a predecessor chain. Preserve all accepted Phase 1 identities, including corrected Striker runtime `efd479b6b4c7eeaa7d8df3f40f36593f87d96b9d5f512dc79c4dd9b0520211f4`. The historical ORB effective setting `qty=2` is not silently transformed into the fixed-book base of one; decision-bearing preflight refuses until a newly reviewed settings binding exists.

## Behavioral contract

- Parse canonical JSON from bytes with duplicate-key, BOM, whitespace, NaN, missing-field, and extra-field rejection.
- Validate a closed-world artifact inventory, dependency closure, unique role ownership, runtime load equality, separate source/path/deployment clocks, exact FULL/H1/H2 relation, complete four-leg/state coverage, and exact accepted historical pins.
- `FREEZE_F1` and exact-depth approval are detached, scope-specific signatures from an externally supplied trusted-key registry. Test keys are explicitly `TEST_ONLY` and cannot pass a production CLI boundary.
- Freeze validation is pure; this implementation never issues a production freeze.
- The journal maintains independent `verdict` (`PENDING|FALSIFIED|RESOLVED|AMBIGUOUS`) and `validity` (`VALID|VOID`) axes. Failure remains terminal after invalidation; void never becomes a verdict.
- Stage transitions are `RESERVED -> STARTED -> COMPLETED`. Exact repeated calls are idempotent; changed bindings conflict. A started stage is never automatically redrawn after restart.
- Result envelopes retain partial/corrupt outcomes and exact output identities. Only a complete, authenticated PASS can be sealed. The E1 seal explicitly grants no admission, activation, n3, D0, D1, or deployment authority.
- Runtime loader hashes before execution, executes the verified bytes without timestamp bytecode reuse, and parses effective settings from the verified snapshot.
- A shared pure schedule classifier distinguishes risk-add, cutoff, flatten, deadline, and closed phases. Qualification requires explicit source-instant price evidence at flatten instants.
- Final local owner refusals become durable, replayable adapter `reject` feedback. Transient takeover and duplicate-operation states do not fabricate rejection feedback.

### Task 1: Runtime identity snapshot prerequisites

**Files:**
- Modify: `ops/c1_signal_daemon/book_adapters.py`
- Test: `tests/ops/test_book_adapter_identity_atomicity.py`

1. Write failing tests proving unaccepted code cannot execute, stale timestamp `.pyc` cannot replace verified source, and effective inputs are parsed from the hashed byte snapshot.
2. Read once, hash before execution, compile/execute those bytes directly, and decode the retained settings bytes.
3. Run the focused adapter/runtime tests.

### Task 2: Shared schedule and durable local-refusal feedback

**Files:**
- Create: `ops/c1_rail/book_schedule.py`
- Modify: `ops/c1_rail/book_account_owner.py`
- Modify: `ops/c1_signal_daemon/book_runtime.py`
- Test: `tests/ops/test_book_schedule.py`
- Test: `tests/ops/test_four_leg_runtime.py`

1. Add failing boundary tests for each schedule phase, aware datetimes, invalid ordering, and a flatten instant between bars that requires an explicit price-evidence callback in qualification.
2. Implement the pure classifier and refactor account scheduling to consume it without changing production fill authority.
3. Add failing runtime tests showing a final local sizing/capacity refusal is durably delivered once, checkpointed, and replayed after restart; prove takeover-pending and exact duplicates do not emit false rejection.
4. Add the owner operation that atomically retains deterministic local-refusal feedback and timeline identity, then have the runtime deliver it through the existing checkpoint boundary.
5. Run owner/runtime/schedule tests.

### Task 3: G1 frozen-contract validator

**Files:**
- Create: `ops/c1_rail/qualification/contract.py`
- Test: `tests/ops/qualification/test_contract.py`

1. Write failing tests for canonical bytes, closed schemas, exact historical pins, artifact inventory/load trace, coverage, population split, clock separation, synthetic-authority exclusion, and ORB settings mismatch.
2. Define immutable `EvaluationState`, `ReplayConfiguration`, artifact/approval/key records, and `ValidatedFrozenContract` interfaces compatible with the Phase 3 runner.
3. Implement strict canonical parsing and semantic validation from retained bytes.
4. Implement detached Ed25519 approval verification with explicit scope, subject, contract, time, revocation, and authority-class checks.
5. Run focused contract tests and Phase 1 provenance vectors.

### Task 4: G2 durable attempt/stage journal

**Files:**
- Create: `ops/c1_rail/qualification/attempt.py`
- Test: `tests/ops/qualification/test_attempt.py`

1. Write failing transition/idempotency/crash tests for reserve, start, result commit, terminal failure, ambiguity, void, restart, and singleton campaign identity.
2. Implement a standalone SQLite store with strict schema validation, boot fencing, append-only hash-chained events, and atomic canonical result/receipt commits.
3. Enforce E1-before-n3, exact manifest equality, no retry/reset/reopen API, and no automatic execution on recovery.
4. Run focused journal tests including concurrent reservation and lost-receipt cases.

### Task 5: G5 result authentication and E1 sealing

**Files:**
- Create: `ops/c1_rail/qualification/seal.py`
- Test: `tests/ops/qualification/test_seal.py`

1. Write failing tests for partial result, missing/extra/drifted outputs, runtime-load drift, invalid `PathOutcome`, failed/unresolved paths, wrong producer scope, self-signing, and every non-PASS seal refusal.
2. Validate canonical envelopes against the frozen contract, Phase 3 `PathOutcome` values, exact counts, output roles, journal bytes, and runtime trace.
3. Verify a detached external result attestation, then construct a canonical E1 PASS seal only with a distinct authorized seal approval.
4. Assert every seal authority-grant flag is false and no n3 identity is consumed.

### Task 6: Qualification CLI and combined integration

**Files:**
- Create: `ops/c1_rail/qualification_cli.py`
- Test: `tests/ops/qualification/test_qualification_cli.py`

1. Add failing CLI tests for validate/status/preflight and explicit refusal of test-only keys in production mode.
2. Implement byte-oriented validation and journal inspection commands. Commands may prepare or inspect synthetic records but cannot sign, freeze, run qualification, seal with a repository-held key, or grant authority.
3. Integrate Phase 3-owned package files without editing its shared initializer except through the integrator.
4. Run all qualification, runtime, provenance, boundary, and full ops tests.
5. Request independent review; fix findings; rerun exact focused and full verification before reporting completion.

## Handoff and invalidation reporting

Report reused Phase 1 components by exact digest, remaining interface conflicts, and any change that would require new accepted runtime bindings. The loader implementation change, shared scheduling bytes, local-refusal serialization, any effective-settings successor, and the qualification package/CLI are new identities; none inherit Phase 1 admission merely because old sources or signatures are referenced. Actual close acceptance remains blocked by CSV/query timezone semantics, September 14 boundary equity/flatness, and correction-status evidence.
