# Recovery owner implementation plan

> **For agentic workers:** Execute with superpowers:executing-plans. Preserve the behavioral contract and coordinator-owned integration.

**Goal:** Persist and fence slice 2b operations/attempts without enabling production dispatch.
**Architecture:** One account serializer spans boot, halt, preparation, and synchronous synthetic dispatch. One SQLite database owns halt and recovery state. Production inputs cannot select synthetic transport.
**Tech Stack:** Python 3.11+, stdlib SQLite/file locks, pytest.
**Spec:** [approved design](../specs/2026-09-14-recovery-owner-design.md), approved by Joshua in this task after review.

## Constraints

Base `089f0a0765d1dd011f05c6a1ae0253ab2e44297a`; isolated branch `codex/stage2-runtime-owner`. No live sends, qualification, host/config/allocation changes. HALTED persists. Real E1–E3, route authority and qualified adapters are absent. Synthetic response observations confer no reduction credit, retry or completion.

## 1. Establish storage and caller refusal regressions

- [x] Add tests rebuilding report schema without its key, dropping configured coverage, and configured exit/flat reaching a forbidden sender.
- [x] Run these tests and observe failures against existing implementation.
- [x] Add a shared account serializer, schema validation and independently pinned coverage to `book_halt.py`; route configured exits into retained recovery refusal. Verify existing halt/scope tests.

```python
with pytest.raises(HaltStoreError):
    corrupted.snapshot()
assert action.sent is False
```

## 2. Persist the complete recovery graph

- [x] Add `test_book_recovery_owner.py` failures for batch preparation, duplicate/conflict, corruption, unknown external order, bounded refusal and no production transport.
- [x] Implement `book_recovery.py` and supporting schema/serializer modules. `RecoveryOwner.boot`, `report_fault`, `prepare`, `prepare_recovery`, `dispatch`, `snapshot` consume the approved typed demand/evidence boundary.
- [x] Persist exact demand, child order/protection/allocation/effect records, independent obligations and events atomically; validate the full graph on reads. Test v1/v2 migration and stale handles.

```python
owner.prepare_recovery((first, second), evidence=evidence)
assert len(owner.snapshot()['operations']) == 2
assert owner.dispatch(first.operation_id)['status'] == 'blocked'
```

## 3. Fence attempts across real process death

- [x] Add `test_book_recovery_process.py` with explicit synthetic broker/causal producer, subprocess barriers and durable broker call records.
- [x] Persist UNKNOWN before synchronous transport under the account serializer; record observations separately and prohibit every reattempt in 2b.
- [x] Kill processes before/after graph and attempt commits and after broker receipt; restart and assert no sends. Race new boot against paused dispatch and reject stale handle afterward. Concurrent same-symbol work cannot dispatch competing closes; two-symbol partial progress preserves siblings.

```python
assert restarted.snapshot()['attempts'][0]['state'] == 'UNKNOWN'
assert broker_call_count == 1
```

## 4. Handler/image integration and acceptance

- [x] Handler boots one production RecoveryOwner. Direct BookHaltStore calls share its fence. Configured book signals cannot enter legacy transport; unconfigured M1 regression behavior stays available.
- [x] Update Dockerfile/context and CI inventories for required modules; test actual handler and listener interfaces.
- [x] Run focused tests, full affected ops suite, error-level lint and `scripts/gate_manifest.py --tier check`; inspect final diff.
- [x] Obtain independent combined 2a/2b review, fix substantiated findings and recheck affected tests. Record exact results and producer limitations in the design execution record.

The coordinator owns acceptance across the store, listener and synthetic process fixtures. No model or persistence test accepts E1–E3, actual broker semantics, 2c completion/disarm or combined Stage 2.

## Execution record — 2026-09-14

Implemented on `codex/stage2-runtime-owner` from
`089f0a0765d1dd011f05c6a1ae0253ab2e44297a`; local reviewable packet, no push,
merge or host action. The original shared checkout and unrelated work remain intact.

Actual interfaces: `RecoveryOwner.boot`, `report_fault`, `prepare`,
`prepare_recovery`, `dispatch`, `snapshot` return validated dictionaries backed
by the real SQLite store. `RecoveryDemand` and `RecoveryEvidence` are frozen
dataclasses; nested inputs are copied and structurally validated before persistence.
Evidence includes explicit product/dated-symbol bindings and their evidence digests;
this structural binding does not authenticate or qualify a producer.

Schema 3 migration occurs atomically with boot through `BookHaltStore`, so direct
halt-store callers and the handler-owned recovery instance share one OS/thread
serializer. Schema keys/constraints, configured coverage, complete child graphs,
events, and operation/attempt relationships are checked before work. Configured
exit/flat signals retain a halt incident and alert instead of using legacy
`closeposition`; unconfigured legacy M1 behavior remains regression-covered.
All new modules are included in Docker/context and the CI image inventory.

Production preparation retains capability refusals. Production dispatch has no
adapter or network fallback. `RecoveryOwner.synthetic` is an explicit Python test
seam, never selected by handler configuration. It uses the same persistent owner
and lock across attempt commit, synchronous transport and observation recording.
Every sent attempt stays UNKNOWN with its separate observation; there is no
retry, credit, completion, disarm or resume method in this packet. Unknown orders
and their observed request identities receive separate durable obligations even
when outside the selected demand. This is not a covering E3 request fence.

### Verification

New corruption/caller tests initially failed in all four intended places; missing
owner API tests then failed collection before implementation. Subsequent planted
regressions caught uncovered observed locations, lost CHECK constraints, invalid
generation/causal relationships and missing independent external owners; each was
fixed and verified. Packaging regression caught the initially omitted CI inventory
entries; they are now present.

Repository CPython 3.11.9, primary installed venv, isolated checkout:

- Full `python -m pytest tests/ops -q`: **1,657 passed, 12 skipped**, two existing
  seaborn deprecation warnings, 60.48 seconds. Production files were unchanged
  afterward. One additional post-response two-symbol crash test was added during
  that run and passed separately (**1 passed**, 0.82 seconds).
- Independent reviewer ran owner/validation/process suites: **41 passed**,
  10.63 seconds, including the additional crash test.
- Error-level pylint passed for all six changed/new production modules.
- Required `python scripts/gate_manifest.py --tier check` passed (exit 0) with
  the complete packet staged, including 72 evidence-store tests (3 skipped),
  source-boundary checks and image/M1 gate checks. Existing absent-private-tree
  skips and advisory notes remain. Packet links and `git diff --cached --check`
  passed. No core risk, allocation or live-config file changed.
- Real subprocess tests cover death inside migration, mid-batch publication,
  before/after preparation and attempt commits, after broker recording, before
  response commit, and after partial-response commit. A pipe-barrier boot race
  proves boot cannot cross a committed attempt's pre-transport lock boundary;
  stale handles refuse afterward. Fixtures and broker recorders are SYNTHETIC.

Independent `review_2b` reviewed the entire 2a/2b uncommitted integration against
the approved contract. Four findings were reproduced and fixed: product scopes
bound to unrelated symbols, empty/incomplete owned brackets, missing relational
attempt validation, and unselected unknown orders lacking independent owners.
Re-review found **no remaining blocking findings for the bounded packet**. It
also independently rehashed six corrupted attempt variants (account, route,
version, command digest, boot and generation); all refused. This accepts the code
boundary, not broker capability, hosting, merge or deployment readiness.

### Remaining producer and acceptance work

Slice 2c remains required: actual named E1–E3 producers, coherent acquisitions and
immutable complete history, durable execution credit/cursors/conflicts, global
request fencing and atomic transfer, fresh gross quiescence, and config-owner
disarm write/readback. The internal fault-report method still needs an authenticated
source/session/sequence producer and endpoint. Neither current legacy telemetry
nor the synthetic route supplies those capabilities. Native route/version-qualified
cancel/close/protection and scoped recovery authority remain absent.

Only combined 2a–2c acceptance closes recovery slice 2. Shared calendar/replay,
snapshot/resume and combined Stage 2 acceptance remain subsequent packets. No
seven-bundle admission, parity, qualification, allocation, live configuration or
M1 rework was performed or authorized by these tests.
