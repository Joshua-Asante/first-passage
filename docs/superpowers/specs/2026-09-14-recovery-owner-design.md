# Slice 2b: durable recovery operation owner

Status: APPROVED by Joshua in this task; bounded 2b implementation completed
locally. See the [execution record](../plans/2026-09-14-recovery-owner-implementation.md).
Production dispatch and route qualification remain unavailable.

Base: `089f0a0765d1dd011f05c6a1ae0253ab2e44297a` (PR #391), freshly
fetched 2026-09-14. Worktree: `.worktrees/stage2-runtime-owner`, branch
`codex/stage2-runtime-owner`. The coordinator owns combined integration.

This is the concrete next packet under the [Stage 2 plan](../plans/2026-09-14-stage2-runtime-integration.md)
and [ratified halt/resume contract](../../spec/2026-09-14-tb-s3-halt-resume-contract.md).
It preserves retained S3 E1–E3/K1–K3, quantity and protection laws. Approval of
this engineering design would not qualify a producer, authorize a send, or close
slice 2. M1 is complete; the historical A7/A8 pending text in earlier plans is
not a new obligation. Seven bundles remain collected 7/7, accepted 0/7.

## Ground truth and choice

Read production `book_halt.py`, handler/listener, `ExecutionStateStore`,
`BrokerEvidence`, `crosstrade_payload.py`, `core/lib/file_lock.py`, `book_policy.py`
and emulator `_fill_exit`/`_close_scope`. Read the retained offline producer,
primitive and account contracts as test provenance, not production capabilities.

`BookHaltStore` schema 2 owns atomic halt/scopes but no operations or attempts.
`ExecutionStateStore` holds confirmed leg bases, not immutable order histories.
`BrokerEvidence` is an optional-field per-event overlay, not E1–E3. The handler
boots the halt store once, but the listener only consults it for risk-adds:
legacy exit/flat still reaches `closeposition` without boot fencing.

Use the existing SQLite journal plus a process-shared account lock held across
commits and transport. SQLite-only transactions cannot both commit a boundary
before transport and fence the intervening boot race. A separate durable worker
could also serialize commands, but would introduce a second lifecycle/service
for this bounded packet. The listener remains the single owner.

## Serializer and boot boundary

Add `AccountSerializer` in `ops/c1_rail/book_recovery.py`: an in-process lock
shared by canonical database path plus the existing portable OS file lock.
Lock order is always account lock, then SQLite transaction. Do not acquire the
account lock recursively through public methods; internal transaction helpers
accept the already-held guard. Resolve paths once; require one configured journal
per account on one supported local filesystem. Multiple journals, hosts, aliases
through hard links, or old unfenced binaries are not a supported shared owner.
Actual deployment qualification must prove exclusive account routing.

Every boot, halt report, preparation, evidence mutation and dispatch uses this
serializer. Boot waits for an active send critical section; it cannot acquire a
new boot ID while an old synchronous sender is still permitted to invoke transport.
Lock failure refuses startup/work and raises an attended alert; it never steals
ownership. Process death releases the OS lock. The new boot commits HALTED and
retains all operations, original identities and unresolved attempts. A stale
handle fails its boot check after obtaining the lock, before any mutation/send.

Dispatch holds the lock across: boot/authority validation, durable attempt commit,
synchronous transport invocation, and durable response recording. No background
sender or callback may outlive that section. A transport timeout records UNKNOWN;
it does not prove the broker did nothing. A request already emitted before boot
may still execute remotely and remains reconciliation-owned. A hung process
prevents takeover until termination; safety does not depend on a timed lease.

## Schema 3, one atomic migration

Validate schema 1/2 history and coverage before migration; preserve their bytes
semantically and all identities. Add tables in the same FULL-synchronous database,
with foreign keys, uniqueness, CHECK constraints and read-time cross-row validation.
HALTED is still the only permission. No reset/replacement on migration failure.

| Table | Required identity and facts |
|---|---|
| `recovery_operations` | `operation_id` PK; immutable canonical demand and digest; kind CANCEL/CLOSE; transition; account; route/version/domain; dated symbol; source incident; preparation boot/generation/time/causal boundary; status |
| `operation_scopes` | operation/scope composite key; every controlled/observed coverage obligation linked before dispatch; products alone are never dated order bindings |
| `operation_orders` | operation/original order key; original authority digest, request IDs, side, type, accepted quantity and known remainder; retain terminal identities |
| `operation_protection` | operation/protection-owner/component key; originating execution, intended full bracket, linkage, quantity and anchor facts; distinct from current lot allocations |
| `operation_allocations` | operation/entry-execution tranche key; accounting lot, execution causal order, available quantity and intended reduction bound; distinguish explicit close from triggered FIFO reduction |
| `recovery_effects` | effect ID PK; operation; exact immutable adapter command/digest; dependency; status; no transport secrets |
| `recovery_attempts` | attempt ID PK; unique route-lifetime request ID; effect; boot/generation; account/route/domain; durable causal boundary and UTC; command digest; transport observation; never overwrite prior attempt |
| `recovery_obligations` | independent reason/owner key; scope; retained conflict or reconciliation fact; unknown external orders/requests own obligations, never cancel permission |
| `recovery_events` | monotonic local audit sequence, entity ID, transition and body digest; appended atomically with state, not a second best-effort safety journal |

Persist the complete canonical demand alongside its digest so exact duplicates
are checkable and changed reuse refuses. An operation's status is derived from
its effects/attempts and obligations, not a caller-supplied completion flag.
Read validation refuses missing child records, impossible quantities, unsupported
versions, changed account/route identities and broken references. Acquisition
history/cursors and completion/disarm tables belong to 2c's concrete migration;
do not claim these proposed operation facts are verified broker inventory.

Before migration or any read, compare actual table columns, primary/unique keys
and foreign keys against the versioned schema manifest. Validate report row
cardinality and unique incident IDs before constructing maps. Pin the configured
controlled-product tuple on the boot handle and check it against stored coverage
on every access; do not accept a simultaneously edited config and scope set.
Validate statuses against enums, quantities as non-boolean positive integers
(nonnegative only for remaining/consumed values), and allocations against their
declared total. These checks detect malformed state, not authenticated protection
against an attacker rewriting an entire valid database.

## Public API and production wiring

This API was approved before implementation; the execution record identifies
the implemented signatures and the remaining qualification boundaries.

```python
RecoveryOwner.boot(path, account, *, controlled_products) -> RecoveryOwner
owner.report_fault(incident_id, reason, *, observed_symbols=()) -> RecoverySnapshot
owner.prepare(demand: RecoveryDemand, *, evidence: RecoveryEvidence) -> OperationView
owner.prepare_recovery(demands: tuple[RecoveryDemand, ...], *, evidence: RecoveryEvidence) -> RecoverySnapshot
owner.dispatch(operation_id: str) -> OperationView
owner.snapshot() -> RecoverySnapshot
```

`boot` owns the store migration and boot fence; handler construction calls it once.
The existing halt-only API remains compatible and shares the same serializer,
so direct `BookHaltStore.boot/halt` cannot bypass recovery fencing. `report_fault`
atomically invokes scope publication and retains independent reconciliation work.
Its public HTTP producer is a separate missing integration, not an unauthenticated
new way to submit recovery demands.

`prepare` takes immutable explicit CANCEL(order) or CLOSE(full dated symbol)
demands. A duplicate identical operation returns the original record; changed
reuse refuses. Overlapping same-symbol work joins/queues under the existing owner
and cannot dispatch a competing close. Full account recovery publishes all symbol
operations/effects together via `prepare_recovery`: validate the complete batch,
then commit every operation and child row in one transaction. `prepare` is the
single-operation wrapper and cannot certify whole-account preparation. A batch
with conflicting reuse or missing controlled coverage refuses atomically. Unsupported bounded,
mixed protection or ambiguous ownership demands create capability obligations.
There is no arbitrary SQL/state-edit API, direct `mark_complete`, or caller-selected
transport callback on the production owner.

`RecoveryEvidence` names account, route/version, restart-stable causal domain,
acquisition identity/time/sequence, orders, gross lots, entry executions,
protection owners and immutable reduction allocations. 2b can persist and validate
the structural boundary using explicitly synthetic fixtures. Only 2c's accepted
E1–E3 consumer may produce decision-bearing production evidence; a dict, boolean,
HTTP response or legacy overlay cannot confer that authority.

Production `dispatch` is unavailable in this packet: it returns a durable
capability/authority refusal without creating a send attempt or calling legacy
transport. A separate explicitly synthetic construction path exercises the same
store/owner/attempt code with a recording broker fixture; the handler cannot
select it via config, webhook body, or an `enabled` boolean. The future production
adapter must bind accepted route/version semantics, E1–E3 evidence and recovery
authority before being wired. No default `send_to_crosstrade` fallback exists.

When the book journal is configured, all listener exits/flats are routed to this
owner or refused with retained reconciliation/alert; they never reach the legacy
payload builder. This intentionally closes the configured-book bypass. Existing
unconfigured legacy M1 operation remains a regression surface, not a recovery
adapter. Four-leg signals without the owner remain refused. No deployed config,
host, risk constant, registry or allocation is changed.

## Attempt and quantity laws

Preparation commits exact effects and original identities before a send is eligible.
For a synthetic dispatch, persist the unique request/attempt and causal boundary
with state UNKNOWN **before** calling transport. This means a crash immediately
after commit but before sending is conservatively ambiguous. A prepared effect
with no committed attempt is distinguishable as never dispatched, but reboot
does not automatically send it; fresh evidence and authority are required.

Record transport acceptance, rejection, partial or unknown observations without
turning them into completion. Exceptions or failure to persist the response leave
the committed UNKNOWN attempt. Restart never resends any previous request.
A later attempt needs fresh qualified evidence proving the previous request's
terminal outcome and exact remaining demand, plus current authorization; it gets
a new request ID and retains all original identities. This decision remains
disabled in production until 2c. HTTP rejection alone is insufficient proof of
no side effect unless the accepted adapter contract establishes that fact.

Bounded quantity acceptance includes refusal of unsupported bounded scopes and
synthetic partial execution of a full-symbol demand. Reduction credit comes only
from immutable executions allocated to the operation's actual request IDs, never
from a net-position delta. Already consumed tranches cannot be spent twice.
In 2b all sent/partial/rejected/unknown attempts remain unresolved and ineligible
for reattempt: this is the bounded no-overclose mechanism. Synthetic observations
do not grant reduction credit. 2c must introduce a unique immutable execution-credit
ledger atomically with acquisition consumption before any residual retry or
completion is enabled; tests of that algorithm are owed to 2c, not claimed here.
Late fills and cancellation races retain their original entry/remainder owner.
If protection-owner quantity diverges from FIFO lot allocation, do not invent
a bounded-close reassignment; require a qualified full-symbol transition or
attended recovery. Unknown orders are retained and never blindly cancelled.

## Executable acceptance plan

Add production-owner tests in `tests/ops/test_book_recovery_owner.py` and real
subprocess crash/fencing tests in `tests/ops/test_book_recovery_process.py`.
Synthetic brokers and causal producers must be labeled SYNTHETIC in fixtures
and reported results. Use fresh child processes, disk SQLite, event/pipe barriers
and forced termination, not object reconstruction alone or timing sleeps.

| Trace | Required independent observation |
|---|---|
| Death inside/beyond migration and operation/effect publication | rollback or complete committed graph; no partial child set; schema-2 scopes/history preserved |
| Death after first symbol insertion inside `prepare_recovery` | neither symbol's partial graph committed; after batch commit both graphs survive |
| Death before attempt commit | no transport; all prepared effects retained |
| Death after attempt commit before transport | UNKNOWN survives; restart makes zero sends |
| Death after broker recording before response/response commit | broker records at most one send; request ID remains owned and unreplayed |
| Concurrent identical/different same-symbol demands | exact duplicate identity stable; conflicts refuse; no overlapping dispatched closes |
| Two symbols, first partial/rejected/unknown, crash before second | both scopes persist; no sibling completion; no restart sends |
| Old owner paused at pre-send boundary, new boot attempted | boot cannot commit while send lock held; after boot commits old owner cannot send/mutate |
| Partial close plus late fill and duplicate outcome | no credit from position delta; no overclose or duplicate reduction credit; residual protection owned |
| Unknown external order/location | scope and independent obligation survive; zero cancel commands for unknown owner |
| Configured listener exit/flat and malformed/missing owner | legacy sender never invoked; no risk-add; no inferred flatness |
| Dry run, missing route evidence, forged synthetic mode | zero production transport calls and retained capability refusal |
| Missing/corrupt operation, child row or stale boot | fail closed without replacing database or losing original identities |
| Duplicate report ID in altered schema; stored product/scope pair deleted | reject before map construction/migration and against the boot handle's pinned coverage |

2c additionally must exercise fill/cancel races, opposite gross lots at net zero,
protective orphans, latest-position versus full-acquisition ordering, backdated or
changed immutable histories, global request renewal, atomic request-to-order/lot/
quarantine transfer, and crashes during disarm write/readback. Those tests cannot
be reported passed by 2b persistence fixtures.

Run affected halt/scope/listener/HTTP/image tests and required check tier through
`scripts/gate_manifest.py` (composition owner), then obtain independent review
of the combined 2a/2b diff. Add the production module to Docker context/image
inventories with their regression checks. Return exact revision, test results,
review findings and implemented-versus-qualified limits for the bounded packet.

## Actual producer dependencies and following sequence

TB-I3/R-M still owes route-backed E1 coherent account acquisition, E2 complete
immutable execution/reduction history and E3 global request fencing, with a durable
causal boundary API shared by acquisition/preparation/dispatch. There is no actual
named qualified service behind those requirements today. The offline `FakeBroker`
and `Clock` implement synthetic semantics only. Runtime must implement the real
adapter after prerequisite evidence identifies the accepted provider and version.

L2 native CANCEL and CLOSE/protection semantics remain unqualified; legacy market
PLACE/closeposition is insufficient. Prerequisites owns evidence collection;
runtime owns adapters and admission. The daemon fault producer still needs a
durable outbox, authenticated source/session/sequence binding and listener endpoint
integrated through `report_fault`; sizing-path authentication is not source-health
or operator-resume authentication. No endpoint qualification is supplied here.

Next design 2c against the actual producer interfaces, including cursor/conflict
persistence, atomic request ownership transfer, global gross quiescence and
ordinary disarm write/readback through the real config owner. HALTED persists.
Only combined 2a–2c acceptance closes recovery slice 2. Shared calendar/replay,
settled-account/host producers, authenticated resume and combined Stage 2 acceptance
follow the existing plan. Seven-bundle/private-input amendments remain with their
coordinated owners; this draft does not amend those shared contracts.

## Pre-implementation independent review and evidence

Independent read-only reviewer `review_2a` inspected the base implementation and
this draft. Existing tests ran at the base revision, in this isolated checkout:

```text
C:/Users/joshu/multi_firm_operations/.venv/Scripts/python.exe -m pytest tests/ops/test_book_halt.py tests/ops/test_book_recovery_scopes.py -q
..................................                                       [100%]
34 passed in 1.55s
```

Exit 0, repository CPython 3.11 environment. These are existing 2a tests, not 2b
acceptance. Independent temporary-database reproductions found:

- Rebuilding `recovery_reports` without its primary key permits contradictory
  duplicate incident rows; conversion to a dict in `book_halt.py` silently hides
  one. Both snapshot and boot accepted malformed state, with boot advancing
  generation. The subsequent implementation fixes this with schema validation.
- Coordinated removal of a product from stored config and its scope passes a
  current handle's self-consistency check; reboot with the original configured
  product tuple rejects it. This is a coordinated-corruption hardening gap,
  not proof of an accidental single-row deletion or an existing send bypass.

The design requires explicit schema/report uniqueness and pinned coverage
checks plus regressions. Reviewer also requested explicit account-batch preparation
and a clear reduction-credit boundary. Those changes are incorporated above.
On re-review, no blocking findings remained for this bounded design. This verdict
does not accept the existing validation defects or any unimplemented 2b behavior.
The execution record records the subsequent independent complete 2a/2b review.

Repository verification: `scripts/gate_manifest.py --tier check` exited 0 using
the installed Python environment, with existing private-tree skips and advisory
notes (including 72 evidence-store tests, 3 skipped). This draft is untracked,
so tracked-file gate discovery does not establish coverage of its new prose;
its relative links and whitespace are checked directly. No production code,
configuration, governing contract, intake ledger or private evidence was edited.
