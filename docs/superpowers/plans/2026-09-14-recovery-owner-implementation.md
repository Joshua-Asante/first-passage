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

## Publication and Stage 2 continuation audit — 2026-09-14

Joshua requested commit/push and continuation through Stage 2. The reviewed 2b
packet was committed as `014144158831256b32c0091c7fcd30c03d9c9001` and pushed to
`origin/codex/stage2-runtime-owner`. Commit hooks and push collision checks passed.
The earlier local/uncommitted description above is its pre-publication record.

The next dependency was investigated against production source, current governing
records, and official provider documentation; no live account API, host mutation,
broker send or qualification was performed. Joshua did not know of a newer
accepted producer packet. Read-only coordination with **Complete Tradeify
deployment** confirmed that main through #391 supplies none. The last prerequisite
owner is **Resume Track B prerequisites**, task
`01a09e17-faa1-7d00-abd4-f8f8b5019745`; that task is archived and was not reopened.
Its retained #382 ledger remains the evidence baseline. No competing governing
document or private manifest was changed.

### Named candidate inputs and the unresolved contract

| Required guarantee | Actual source inspected | Result for the next consumer |
|---|---|---|
| S3 E1 coherent acquisition and restart-stable causal domain | CrossTrade Tradovate REST positions/orders; WebSocket `Tv_ListPositions`/`Tv_ListOrders` and pushed events | Candidate read interfaces exist; accepted coherent acquisition and durable shared boundary do not. A new local counter cannot manufacture broker causal order. |
| S3 E2 complete immutable execution/history and protection/FIFO identities | CrossTrade fill routes and Tradovate per-order lifecycle; local `BrokerEvidence`/`ExecutionStateStore` | No accepted complete-history/gross-lot/protection producer. Existing local stores are insufficient. |
| S3 E3 every earlier accepted request, including external requests | Existing local operation/attempt journal and provider order reads | Local ownership is implemented; no accepted global request fence accounts for requests outside it. Order existence or missing orders cannot prove absence of unresolved requests. |
| Native L2 cancel/close/protection | CrossTrade REST close-position documentation and legacy `crosstrade_payload.py` | Documented routes are candidates; route/version-specific acceptance and protection-transition evidence remain absent. No fallback adapter is admitted. |
| Authenticated source-health reports | `EvaluateLoop`, `ListenerClient`, daemon `build_loop`, listener handler | Production currently builds the bounded M1 operator-input loop and posts B1 only. No four-source authenticated fault producer/endpoint or required-session consumer exists. |
| Qualified completion and acknowledged disarm | `c1_rail_arm.py` config writer | The CLI writes configuration and explicitly requires restart to take effect; it does not supply a recovery-owner activation/readback acknowledgment. |
| Shared calendar and settlement/host inputs | D19 calendar, TB-T1 seal contract, `BookSession`/`SettledClose`, M1 deployment records | Date membership and prior deployment evidence do not supply source-backed deadline coverage, settled-account-close producer or reusable boot/request-bound host verifier. |

Current official sources, read 2026-09-14:

- [CrossTrade WebSocket API](https://crosstrade.io/docs/api/websocket-api) documents
  connection-lifetime sequence numbers, possible dropped frames, and a stream that
  is not a durable log. Re-pulling and per-order lifecycle reads are advised after
  gaps/reconnects. This does not establish S3's durable all-account causal fence.
- [Tradovate order lifecycle](https://crosstrade.io/docs/api/orders/get-order-lifecycle)
  is assembled from order, orderVersion, command and commandReport dependency
  reads for an identified order. The documented response exposes the current order,
  highest-ID version, commands and reports; it is not a documented all-request fence.
- [All orders](https://crosstrade.io/docs/api/orders/get-all-orders),
  [all positions](https://crosstrade.io/docs/api/positions/get-all-positions), and
  [executions/fills](https://crosstrade.io/docs/api/executions) name real read
  surfaces. Combining separate reads is not, by itself, proof of coherent E1–E3.
- [Close position](https://crosstrade.io/docs/api/positions/post-close-position)
  documents a Tradovate REST route through the shared dispatcher, including Account
  Manager/Trade Copier behavior. A route description supplies neither this
  account's accepted controls nor the retained S3 protection/quantity guarantees.

These are findings about the inspected interfaces and absent acceptance evidence,
not proof that the provider can never supply an adequate contract. In particular,
TB-T1's evidence-file labels E1/E2/E3 must not be confused with S3's E1–E3 producer
guarantees: a sealed dashboard/positions/statement packet does not supply a global
broker request fence.

### Exact continuation prerequisite

Before decision-bearing 2c integration, identify and accept the account/route/version
producer that supplies a fresh coherent gross/order/protection/history acquisition,
immutable complete-history cursor and global unresolved-request fence in the same
durable causal domain as preparation/dispatch. Include recovery after producer and
listener restarts and requests submitted outside the listener. Runtime owns the
adapter and consumer implementation; prerequisites owns collection/verification.
If the route cannot provide those facts, that is a capability problem requiring an
explicit contract/route decision, not a permissive mock or inferred approval.

The 2c implementation then needs durable cursors/conflicts and execution credit,
atomic request-to-order/lot/quarantine transfer, fresh global gross quiescence, and
config-owner write/readback acknowledgment. Slices 3–5 retain their calendar,
replay/feedback, snapshot/resume and combined acceptance dependencies. The handoff
requires these actual interfaces; another synthetic-only owner extension cannot
close them. Stage 2 therefore remains **INCOMPLETE, blocked on the named producer
contract/evidence**, rather than accepted from 2b's green module suites.
