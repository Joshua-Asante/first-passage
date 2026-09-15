# Stage 2 runtime integration implementation plan

> **Current continuation, recorded 2026-09-15 UTC:** [attended Packet 0](2026-09-14-tradeify-attended-release.md) freezes [TB-S3 rev9](../../spec/2026-09-14-tb-s3-halt-resume-contract.md). Incident-triggered automated emergency dispatch in the historical slice 2b/2c instructions below is deferred for the first release. Implement durable all-mutation intervention, observation, attendance and qualified separate resume instead. Normal/scheduled execution, evidence/capacity/fingerprint requirements remain. [Packet 0 capability matrix](../../notes/2026-09-14-tradeify-attended-feasibility.md) owns the current READY/BLOCKED disposition and dependency revision inventory; it explicitly distinguishes newer committed recovery/collector work from main. M1/A7/A8 are complete. Historical slice records and tests are provenance, not current completion or renewed pending-approval claims.

> **For agentic workers:** Execute with superpowers:executing-plans. Preserve one integration owner and the behavioral contract. No delegation is required for the first slice.

**Goal:** Connect the accepted TB-I1 components to durable execution, shared calendar/replay and snapshot consumers under TB-S3 rev8.

**Architecture:** The coordinator owns integration. The listener is the authority for permission and serialized broker operations; daemon reports are inputs, never permission. One shared sizing/capacity/fingerprint implementation and schedule serve replay and rail.

**Tech Stack:** Python >=3.11, stdlib SQLite, existing listener/HTTP adapter and pytest. No new external package.

**Spec:** [TB-S3 rev8](../../spec/2026-09-14-tb-s3-halt-resume-contract.md) and its linked retained contracts.

## Global constraints and post-merge record

PR #379 merged at `d53a06e3fa6018c6c36eb63771e5ad6d1ae961cf`; PR #380 merged at `8101ba498aad812e79c3d80c45f963cd67b55de6`. The #380 merge has the same tree as reviewed head `6f0969bb055a0495ea60a9f70edde77d68c578db`. Prior engineering checks remain evidence for unchanged source bytes. No risk constants, registry admission, active allocations or live config change in this packet.

Joshua's explicit E/P/U approval is recorded in the [dated ratification and bounded TB-I1 acceptance record](../../briefs/handoffs/2026-09-14-track-b-ratifications.md), with the existing S2b/P2 addenda published alongside it. Stage 1 is accepted at the engineering/contract level. Earlier pending-authority language describes the pre-ratification checkpoint. The second exact Part A depth/budget approval remains deferred to TB-F1. No merge or engineering acceptance supplies live GO.

Resume baseline: current main `420ce3af88ede04ff5503aa1c3f14cd2a16eea10` (#382), fetched 2026-09-14. #381 merged the bounded HALTED-only slice at `c1dcb31730157c2895c258c9921b8d8164557335`; its local/uncommitted wording below is historical. #382 is the authoritative collection/intake baseline: collection 7/7, acceptance 0/7, admitted normalization/parity not run. The [seven-bundle interface proposal](../../briefs/handoffs/2026-09-14-seven-bundle-runtime-interface-plan.md) is retained as a proposal, not an implemented or approved API. This task owns combined runtime acceptance; the prerequisites owner retains collection/intake verification. Claude owns A7 and its hosts; A8 waits for accepted genuine evidence and Joshua's dated signoff.

## Integration sequence and capability owners

| Slice | Observable outcome | Actual inputs and remaining dependencies |
|---|---|---|
| 1 — durable halt rejection | HTTP-handler boot creates a durable account/boot-bound halt; listener refuses four-leg risk-adds before sizing or send, including missing/corrupt store and stale process handles | Existing config loader/handler and listener. SQLite stores boot, halt generation and incident records. No RUNNING transition or broker-recovery dispatch exists in this slice. |
| 2 — recovery ownership and qualified evidence | Fault report publishes all scopes before dispatch; real listener operation owner serializes cancel/close/reconciliation and retains uncertain work across restart | TB-I3 must implement the retained operation store and E1–E3 producer interfaces. Current ExecutionStateStore/net positions are insufficient. L1/L2 actual route evidence remains a separate live gate. |
| 3 — shared schedule and synchronized replay | Both consumers refuse at cutoff, begin flatten at the same instant and account for deadline failures | TB-C1 produces source-backed calendar/deadline rows, closure overlay and provenance. TB-I2 produces continuous replay and confirmation feedback. Seven exports/parity gate decision-bearing use. |
| 4 — snapshot and operator resume | Authenticated one-use request matches boot/generation/evidence/identity, and acknowledged activation precedes serialized risk-add dispatch | TB-T1 produces authenticated evidence manifest; host verifier supplies actual image/config identity; operator-only authentication is distinct from webhook authentication. P2 and initial activation gates apply. No fixture can stand in for a missing producer. |
| 5 — combined acceptance | Crash, partial/unknown outcomes, schedule, halt/resume races and replay/rail agreement pass across actual interfaces | All prior slices, required gates and independent review. Synthetic route tests remain labeled synthetic. |

Each later slice receives its concrete API/test plan after the preceding owner interfaces exist. This table is the integration sequence, not permission to invent unavailable evidence or claim those slices implemented.

## Slice 1: durable halt through the listener

**Files:** create `ops/c1_rail/book_halt.py` and `tests/ops/test_book_halt.py`; modify `c1_rail_listener.py`, `c1_rail_http_server.py`, listener tests, and Docker image inventory. Shared risk functions remain unchanged.

**Interface:** `BookHaltStore.boot(path, account) -> BookHaltStore` generates a new boot id and atomically records HALTED plus a boot incident; `halt(incident_id, reason) -> dict` deduplicates identical reports, refuses conflicting IDs and keeps all prior incidents; `snapshot() -> dict` reads without mutations and validates account/boot/schema; `rejection_reason() -> str` always refuses risk-add in this bounded slice. SQLite transactions use FULL synchronization and serialize concurrent writers. Initialization and reads never silently replace a corrupt store. A stale boot handle cannot mutate a newer owner's state. Repeated boot never clears incident history.

The handler owns boot, not per-request routing. Optional `book_halt_path` enables the store in the configured process; invalid configuration prevents handler creation. Four-leg identities are always rejected by the legacy listener when no store is supplied, so omitting configuration cannot route unqualified book orders. Configured stores also block legacy entry/add routing; legacy exit/flat behavior is preserved as regression coverage, not claimed as qualified TB-I3 recovery. A future RUNNING state requires a separately reviewed schema/API migration; this slice rejects such a state.

- [x] Write failing store tests for reboot/history, duplicate/conflicting incidents, two stale/current handles, account mismatch, corruption and concurrent distinct reports.
- [x] Write listener tests that call the real `handle_signal` with a store, asserting no sizing/sender call on entry/add. Test absent store for every four-leg ID; retain legacy exit and dry-run tests. Test handler factory boot and failure before serving.
- [x] Run `python -m pytest tests/ops/test_book_halt.py -q`; observe missing module/API failures.
- [x] Implement the store and boot-to-listener wiring. Include the new module in the listener image.
- [x] Run the focused store/listener/HTTP/image suites, then the repository check tier. Inspect unchanged core risk bytes and inert config/registry.
- [x] Record exact outcomes and remaining producer work. Do not claim recovery/resume, Stage 2 acceptance or live qualification from rejection tests.

Minimal acceptance shape:

```python
store = BookHaltStore.boot(tmp_path / "halt.sqlite", "test-account")
store.halt("fault-1", "feed")
next_boot = BookHaltStore.boot(tmp_path / "halt.sqlite", "test-account")
assert next_boot.snapshot()["permission"] == "HALTED"
assert "fault-1" in {item["incident_id"] for item in next_boot.snapshot()["incidents"]}
# handle_signal(..., book_halt=next_boot) must refuse entry/add without invoking sender.
```


## Slice 1 execution record — 2026-09-14 UTC

Implemented locally on `codex/tb-stage2-durable-halt` from `8101ba4`; not committed. The initial new suite failed on the missing module, then passed after implementation. Packaging regression tests caught missing Docker context/CI inventory entries; both are now included. A close-path fixture initially omitted required existing B1 fields; correcting that fixture established legacy closure/dry-run behavior without weakening the host.

Final new store/handler tests: **21 passed**. Full `tests/ops`: **1,577 passed, 12 skipped**, two existing seaborn deprecation warnings, 32.60 seconds under repository CPython 3.11.9. The actual HTTP handler was exercised with in-memory HTTP transport, real equity-file/peak handling and the real listener; no network send was used. Error-level pylint passed for the three changed production modules with repository import paths. Repository check tier passed with existing private-tree/advisory skips using the already-installed documentation dependencies. Core risk files, registry, active allocations and live config are unchanged.

New database state is HALTED-only, with a persistent recovery-required marker rather than a claim of full recovery-scope publication. No external incident endpoint, automatic broker recovery, schedule implementation, resume authority, complete image build, actual feed/broker evidence or deployment acceptance is supplied by this slice. Those are the next integration work, not capabilities mocked into completion here. The startup/store option is not enabled in any deployed configuration.

Independent read-only review accepted the bounded halt-only slice with no blocking findings and independently passed 46 store/listener tests under repository Python 3.11. It retained all capability and governance limits above. This is code review acceptance, not Stage 2 or live acceptance.

## Slice 2: listener-owned recovery API and test plan

Grounded at #382 in `book_halt.py`, `c1_rail_telemetry.ExecutionStateStore` and
`BrokerEvidence`, handler boot/dispatch, the retained S3 §1/§2e contracts, and the
offline `tb_s3_kernel` producer/consumer contracts. Integration owner: this task.
No production route currently implements E1–E3 or qualified L2 cancel/close.
The offline `FakeBroker.snapshot` and external `Clock` are the actual existing
synthetic producers; neither is deployed or imported into production.

### 2a — atomic scope publication and retained uncertainty

Extend the existing listener-owned SQLite transaction, rather than writing a
second JSON journal after halt publication. This updates the storage mechanism
proposed in retained S3 §1, preserving its single-owner/K3 atomicity requirement.
Schema 1 incident history is migrated transactionally; malformed or incompatible
state is refused. No database is replaced. All boot and incident scopes include
the configured controlled symbols plus observed external locations. Account-wide
coverage remains outstanding until a qualified global acquisition proves it.

`BookHaltStore.halt(incident_id, reason, *, observed_symbols=())` publishes the
halt, deduplicated report body and scope obligations in one transaction. Unknown
locations become reconciliation obligations, not cancel authority. Handler boot
supplies no guessed dated contracts: the fixed product identities are coverage
requirements, while actual broker/order symbols are separately observed facts.
Duplicate identical reports are read-only; conflicting reuse refuses and retains
the original report. Scope publication is not proof of complete broker inventory.

`snapshot()` includes recovery scopes and reports without advancing recovery.
Missing scope/history rows fail closed. Restart retains original scope/report
identities and increments the halt generation. No completion or send API is added
by 2a; it establishes the persistent input consumed by the subsequent owner.

- [x] Write failures for all four product scopes on real handler boot; atomic
  fault publication with external symbols; duplicate/conflicting reports;
  concurrent reports; crash rollback; schema-1 migration; corrupt/missing scope
  refusal; restart and stale owner. Exercise `handle_signal` against that store.
- [x] Implement the durable scope extension and run the halt/listener/HTTP suites.
- [x] Perform focused self-review of migration and listener boundaries; independent review remains owed before broader slice acceptance.

### 2b — serialized operation/attempt owner

Proposed `RecoveryOwner` consumes the scope journal and a qualified acquisition
port, derives only supported CANCEL(resting risk-add remainder) and full-symbol
CLOSE operations, and records their exact demand/transition, order refs, request
IDs, protection owners and FIFO allocations. Publish every operation/effect before
any dispatch. Each dispatch records its causal boundary and timestamp durably
before transport; response loss, crash or ambiguous acceptance is UNKNOWN, with
no automatic resend. Partial/rejected responses retain scope and original IDs.
An account-level operation lock serializes preparation, evidence consumption,
dispatch and boot fencing; a SQLite transaction alone must not be released before
an unfenced sender can race a new boot. Close/protection semantics are selected
from qualified L2(d/e); no concurrent cancel/close substitute is admissible.

Actual route dependencies: the current `crosstrade_payload` supports a legacy
market PLACE/closeposition transport only; HTTP acceptance is not execution.
It has no qualified native cancel/close/protection adapter. L2(a/b) entry/brackets,
L2(c) atomic modify, L2(d/e) scoped/full close with residual protection, L2(f)
first attach and L2(g) trail/anchor behavior all require route/version evidence.
Until the actual port and authorization are accepted, dispatch stays unavailable.

Tests must use the real persistent store and owner interfaces with the labeled
synthetic producer: crash before/after scope publication, each dispatch boundary
and response; two-symbol partial progress; concurrent same-symbol commands;
uncertain response/restart without resend; bounded partial quantity without
overclose; stale owner after reboot; unknown order never blindly cancelled.

### 2c — qualified evidence, completion and disarm acknowledgment

Proposed `consume_acquisition(acquisition)` requires account/route/domain identity,
one fresh coherent E1 acquisition after preparation/latest dispatch in timestamp
and durable causal order, immutable complete E2 execution/history identities,
and the E3 global request fence. Persist accepted cursors, all previous execution
identities/locations and conflicts. New backdated history, changed immutable
fields, missing history, renewed completed requests or a newer position-only fact
must prevent completion. Transfer external request ownership to discovered orders,
gross lots or quarantine atomically, before releasing the request owner.

Named production producer work: TB-I3/R-M must implement and qualify route-backed
account position/gross-lot/order/history acquisition and a restart-stable ordering
domain shared with preparation/dispatch. `BrokerEvidence` and `ExecutionStateStore`
cannot supply these facts. The prerequisites owner collects actual L1/L2 evidence;
this runtime owner implements its consumer. An attended acquisition requires the
same proved facts and causal guarantees; an attestation label alone is insufficient.

Completion requires zero gross lots, no working/protective orders, no unresolved
requests and accounted-for global history across every scope. It automatically
queues ordinary disarm through the existing configuration owner and records its
write/readback acknowledgment. Failed writes remain outstanding. HALTED survives
completion, feed recovery, rollover and restart. Tests cover net-zero offsetting
lots, cancellation racing a fill, orphan/surviving FIFO protection, stale/reordered
full acquisition, duplicate/conflicting history, external request transfer,
missing acquisition fields, failed disarm and crash/restart at each transition.

Only the combined 2a–2c result can close slice 2. Next are slice 3 shared source-backed
calendar/continuous replay and actual fill/fee/PnL feedback, then slice 4 authenticated
snapshot/resume and slice 5 combined acceptance. Missing actual producers remain
explicit dependencies; passing synthetic scenarios does not close live capability.

### Slice 2a engineering record — 2026-09-14 UTC

Implemented on `codex/tradeify-runtime-resume`, base #382 `420ce3a`. Publication
commit/PR supplies the exact resulting revision. Modified `book_halt.py` and real
handler boot; added `test_book_recovery_scopes.py`. Schema 2 retains schema-1
incidents and persists product coverage, report bodies and observed locations.
Products come from the shared `BOOK_LEGS`; they are not dated broker bindings.
No producer can mark these scopes complete in this increment. The internal report
API is not yet exposed through an authenticated daemon fault endpoint.

Evidence on repository CPython 3.11.9: initial 11 new cases failed on the absent
API; 32 combined halt/scope cases then passed. Full `tests/ops`: **1,588 passed,
12 skipped**, two existing seaborn warnings, 54.63 seconds. Two additional actual
process-death cases were then added: final scope suite **13 passed**. These cover
death inside scope insertion (no partial report/incident survives) and immediately
after commit (the complete report/scopes survive). A surviving test crash trigger
initially prevented restart; removing only that injected trigger corrected the
test harness, without changing recovery rows or production code. Error-level
pylint passed for both changed modules. Relative links and `git diff --check`
passed. The repository check tier passed with its existing private-tree/advisory
skips after exposing the installed venv packages to Windows child Python processes.

Focused self-review verified atomic rollback, report identity, boot fencing,
conservative migration and coverage preservation. No independent review is claimed.
Scope publication is the bounded implemented result; **slice 2 is not complete**.
Operation/attempt identities, qualified partial/unknown outcomes, E1–E3 consumer
enforcement and acknowledged disarm are still the 2b/2c work described above.
There is no recovery dispatch, activation, resume, calendar/replay acceptance,
seven-bundle admission or qualification in this packet. Existing risk-code bytes,
registry, allocations and deployed configuration are unchanged.

Prerequisite disposition: A7 remains Claude-owned; no hosts were read or changed
by this task. A8 waits for genuine accepted A7 evidence and dated M1 signoff.
The #382 intake ledger is byte-preserved. Its actual L1/L2, source/funding,
four-symbol, calendar/settled-close and TB-I4 gates remain open. The retained
seven-bundle proposal supplies the shared interface starting point; amendments
require the pinned private-body and producer reads before any binding changes.
