# Stage 2 runtime integration implementation plan

> **For agentic workers:** Execute with superpowers:executing-plans. Preserve one integration owner and the behavioral contract. No delegation is required for the first slice.

**Goal:** Connect the accepted TB-I1 components to durable execution, shared calendar/replay and snapshot consumers under TB-S3 rev8.

**Architecture:** The coordinator owns integration. The listener is the authority for permission and serialized broker operations; daemon reports are inputs, never permission. One shared sizing/capacity/fingerprint implementation and schedule serve replay and rail.

**Tech Stack:** Python >=3.11, stdlib SQLite, existing listener/HTTP adapter and pytest. No new external package.

**Spec:** [TB-S3 rev8](../../spec/2026-09-14-tb-s3-halt-resume-contract.md) and its linked retained contracts.

## Global constraints and post-merge record

PR #379 merged at `d53a06e3fa6018c6c36eb63771e5ad6d1ae961cf`; PR #380 merged at `8101ba498aad812e79c3d80c45f963cd67b55de6`. The #380 merge has the same tree as reviewed head `6f0969bb055a0495ea60a9f70edde77d68c578db`. Prior engineering checks remain evidence for unchanged source bytes. No risk constants, registry admission, active allocations or live config change in this packet.

The operator explicitly requested post-merge work and Stage 2 commencement. This supplies scope for the offline implementation below; it is not a dated TB-P2 ratification, live GO or completed Stage 1 governance acceptance. Record those separately rather than inferring them from merge. The revised S2b addendum and first policy ratification still require their explicit records. Stage 1 engineering/mainline integration is complete; formal acceptance remains pending those records.

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
