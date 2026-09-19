# Task 1b: Durable protected synthetic E1 admission

> Execute with superpowers:executing-plans and test-driven-development. Coordinator owns acceptance.

**Selected outcome:** A verified FULL_E1 TEST_ONLY bundle admits one dormant durable campaign and immutable plan; exact retries recover the original receipt, status/authorized VOID survive restart, and bounded authenticated plan retrieval works without dispatch.

**Prerequisites:** PR425 merge 1e4928360b95812b04725dc1e8da97709d670ff4 plus accepted uncommitted Task1a in this isolated checkout. Existing N1 authority remains unchanged. Operations doctor passed (Python 3.13.2). Transport decision: retain plan service-side; at most 1MiB raw chunks, total at most the canonical 64MiB plan cap and installed profile input limit.

**Ownership:** Executor /root/task1b_admission; coordinator /root accepts this outcome and combined full-E1 acceptance. Executor owns source/tests and this handoff; coordinator owns roadmap/spec.

**Verification:** Signed-fixture service admission, exact retry/restart/conflict/VOID ordering, invalid/expired admission, authenticated artifact membership, reference-depth chunk roundtrip, strict field/range rejection, transaction failure, N1 behavior/closure and schema-v4 migration. Run checkout doctor, selected launcher pytest with two workers, and check; retain interpreter/base/source-stability/capture evidence. Local tests do not establish Linux isolation or E1 execution.

**Checkpoint:** Report interface conflicts and meaningful progress to coordinator. Record final interfaces and verification here. Coordinate recorder runs so all agents freeze source/docs during capture.

**Return boundary:** Return after implemented locally verified admission or a concrete unresolved dependency. No Task2 lifetime budget, worker/G5/seal launch, statistical engine edits, result authority, live activity, commit/push/PR, or full-E1 acceptance.

## Behavioral contract and traced decisions

Installed authority follows release.install_release -> admission.verify_release -> release_schema.parse_release/profile.parse_profile; stage_bundle and service admission both call verify_bundle. Service/client select a closed campaign protocol only for versioned campaign messages. FULL_E1 release/v2 and profile/v2 bind TEST_ONLY, production=false, dispatch_enabled=false and admission-only phase. Original v1 remains N1_ONLY. No existing N1 attempt can promote, and FULL_E1 cannot call SUBMIT_N1.

ExecutionStore is the sole journal/transaction owner. Migrate only the exact accepted schema-v4 layout to v5 by adding dormant full-campaign tables; N1 tables and receipts remain unchanged. Cross-family attempt uniqueness is checked under the same BEGIN IMMEDIATE lock. Retain request, canonical plan, index and original source bytes atomically as SQLite blobs. Retained context validation shares the same canonical admission logic, so historical status/retry needs no mutable staging directory. New admissions verify current signatures; exact retries recover saved receipt before requiring fresh admission and separately report current policy eligibility. VOID uses original signed enrollment and current key authorization under the admission lock; duplicate exact VOID recovers saved receipt.

The service derives plans from its verified context. Wire requests carry schema, operation and attempt_id only plus SUBMIT_E1 bundle_sha256/request_id, FETCH_PLAN_CHUNK object_sha256/offset/length, or VOID reason/operator_approval_bytes. STATUS has no extras. Clients may fetch only their admitted plan membership; g5/operator may inspect status, operator alone may VOID. No candidate/output/commit/dispatch operations are enabled. Chunks return schema, attempt, digest, offset, total length and canonical base64 bytes; retry is deterministic. Integers reject bool, negative offset, zero/oversized length, offsets at/after EOF; the final chunk clips EOF and reports its actual length. The production client reassembles bounded ordered chunks and verifies the complete digest.

The 21.6MB reference plan stays inside the input/64MiB caps. N1 output/RPC limits are unchanged. Frozen budget bytes/identity are retained, but no lifetime charge is claimed: Task2 must account for admission/planning before execution activation.

## Work sequence

- [x] Add signed campaign fixture, protocol/service regression tests and observe expected missing-capability failures.
- [x] Add closed release/profile/protocol and production consumer selection, preserve N1 closure.
- [x] Add v5 atomic dormant admission/storage/retry/status/VOID and bounded plan fetch.
- [x] Verify failure/concurrency/restart/reference-depth cases and N1 regressions, then check.
- [x] Report exact evidence and return to coordinator.


## Executor return — 2026-09-18

**Disposition:** IMPLEMENTED AND LOCALLY VERIFIED; returned to coordinator for acceptance. Detached base remains `1e4928360b95812b04725dc1e8da97709d670ff4`. Accepted Task1a edits preserved; all changes uncommitted. No roadmap/spec edits by this executor, no activation or live activity.

**Delivered interfaces:** `campaign_protocol.parse_campaign_request(raw: bytes) -> dict` closes `qualification_campaign_request/v1` to SUBMIT_E1, STATUS, FETCH_PLAN_CHUNK and VOID. `release_schema.parse_release` accepts admission-only `qualification_execution_release/v2` with FULL_E1, TEST_ONLY, production false and dispatch false; `profile.parse_profile` requires matching v2 profile, protocol 2, empty executable checkpoints, dispatch false and adequate bounded frame capacity. Existing installation/staging consumers call these same parsers; no fixture-only alternate activation path was added. Runtime source measurement follows the new imports automatically.

`ExecutionStore` is schema v5 with exact-layout v4 migration under its existing transaction authority. `CampaignStore(store)` supplies `admit(request_bytes, context, plan, *, now) -> dict`, `retry(request_bytes) -> dict | None`, `status(attempt) -> dict`, `context(attempt, installed_release, keys, *, now) -> ExecutionContext`, `chunk(request) -> bytes`, `void_retry(request_bytes) -> bytes | None`, and `void(request_bytes, *, now) -> bytes`. These are service-private methods, not authority-bearing caller APIs. All original bytes and the immutable receipt are retained atomically; cross-capability attempt collisions reject in both directions. New admissions revalidate retained originals after planning, near commit. Exact admission and VOID retries recover saved receipts. Status reports current policy eligibility separately from historical receipt and durable validity.

`admission.verify_retained_bundle(index_raw, retained, installed_release, trusted_keys, now)` shares the canonical bundle validator for retained custody. `client.fetch_campaign_plan(socket_path: Path, *, attempt_id: str) -> bytes` obtains authenticated status and bounded chunks, verifies receipt/profile/attempt identity, strict offset/length/total fields and whole SHA256. Each chunk uses bounded SQLite `substr`, maximum 1MiB raw, clips EOF, and cannot overflow SQLite indexing because the parser uses the canonical plan cap. Whole-plan limits reuse the original canonical 64MiB cap and installed input limit. N1 RPC/output limits remain unchanged.

**Verification:** operations interpreter `C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`, Python 3.13.2; doctor passed before Python work. The first red run rejected the missing FULL_E1 profile (`20260919T002032Z-b9af1cc9197c`). Later red cases demonstrated absent client reassembly/type rejection (`20260919T002759Z-062271db85d4`) and the exact `2**63-1` offset gap (`20260919T003221Z-76321bfa78eb`). The intermediate expanded run had 33 passes and a controlled-corruption case rejecting NULL VOID receipt through the wrong exception; final code explicitly rejects it with ValueError. These intermediate records are not acceptance evidence.

Final command:

```powershell
./fp.ps1 --workers 2 python -m pytest tests/ops/qualification/execution/test_campaign_admission.py tests/ops/qualification/execution/test_campaign_plan.py tests/ops/qualification/execution/test_bundle.py tests/ops/qualification/execution/test_profile.py tests/ops/qualification/execution/test_release.py tests/ops/qualification/execution/test_protocol.py tests/ops/qualification/execution/test_store.py tests/ops/qualification/execution/test_client.py tests/ops/qualification/execution/test_service.py tests/ops/qualification/execution/test_service_assessment.py -q --tb=short
./fp.ps1 check
```

- Selected tests: **182 passed, zero skips**, including 35 new campaign-admission cases, in 205.15 seconds. Record: `.cache/fp-verification/20260919T003248Z-100e170d5b7e/record.json`.
- `check`: exit 0; 72 evidence-store tests with 3 skips. Existing absent Pine/data/heavy-artifact warnings and documentation/source-date/session-label advisories remain disclosed. Record: `.cache/fp-verification/20260919T003321Z-44e0f6cac19f/record.json`.
- Both records inspected: completed, exit/verification exit 0, source_stable true, capture_complete true, no report errors. All ten Task1b source/test file SHA256 values match both records. Final `git diff --check` passed. This evidence appendix was added after the records closed; source/tests remain unchanged.

The reference-depth functional roundtrip proves a plan exceeding the N1 RPC limit can be retrieved exactly, including final partial chunk; transport envelopes fit the existing RPC limit. Signed tests cover expired admission, expiry during planning, exact retries after expiry/VOID, retained history after staging removal, duplicate concurrency, concurrent invalidation, injected precommit rollback, exact v4 migration rollback/reopen, corruption rejection, membership/role isolation and both no-promotion directions. No performance characterization is claimed.

**Remaining obligations:** Task2 must introduce and charge the one lifetime budget, including admission/planning costs, before any execution activation. Task3 genuine workers, Task4 independent G5 continuation, Task5 result/commit/seal and Task6 Linux combined acceptance remain outstanding. Current release/profile versions deliberately cannot dispatch; enabling execution requires a subsequent explicit versioned contract. Local signed-fixture tests do not establish Linux isolation or an end-to-end E1 PASS. Coordinator owns independent review and acceptance; executor returns here.
