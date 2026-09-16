# PR 409 Slice D Bootstrap and Migration Implementation Plan

> **For agentic workers:** Execute with superpowers:executing-plans when implementation is authorized; use superpowers:subagent-driven-development only when bounded delegation is authorized. Preserve the behavioral contract and integration owner. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bootstrap only a proven fresh empty synthetic account once, and preserve revoked authority and historical obligations through restart and explicit migration.

**Architecture:** Keep boot, activation, migration and observation under the existing account serializer. Introduce durable creation/consumption identity and a versioned quarantine representation for legacy records that cannot satisfy B/C evidence invariants. Migration never obtains a broker or send capability.

**Tech Stack:** Python 3.11 language floor, SQLite transactional DDL, pytest.

**Spec:** [Approved correction, sections 6–8](../../spec/2026-09-16-pr409-bounded-execution-correction.md), [rev9](../../spec/2026-09-14-tb-s3-halt-resume-contract.md), [C/D handoff](2026-09-16-pr409-slices-c-d-handoff.md), [proposed C interfaces](2026-09-16-pr409-slice-c-takeover.md).

## Global Constraints

- Offline synthetic execution only; no production transport, deployment, arming, or trading.
- No strategy parameters, sizing laws, allocation constants, protection-tier constants, or calibration changes.
- No production resume or general-purpose incident recovery in this correction.
- Preserve immutable historical operation/fact identities and retained obligations.
- Preserve the Python 3.11 language floor and existing repository layer boundaries.
- Runtime regression tests must execute without private strategy inputs or optional signing dependencies.
- Preserve A/B validation, consumed owners, FIFO, pending amendment deadlines, and delivered-feedback checkpoints. Empty current exposure is not fresh history.

## 1. Dependency and current findings

This is a **provisional interface-level plan**, grounded at `567a583`. C is not implemented or committed. Its proposed schema 3 must be reconciled against the actual C commit before D's detailed conversion code/fixtures can be finalized. Version 4 below is a proposed D target, conditional on C shipping schema 3. This document authorizes no implementation, migration execution, commits, push or production activity. The coordinating implementer owns combined A–D acceptance.

Joshua confirmed during this session that A and B are pushed to PR 409, superseding the original handoff's unpushed status. Current remote SHA and CI were not independently verified; see C's grounding record.

Current `activate_synthetic` can restore RUNNING after an incident/restart and can dispatch mode-transition cancels. Current boot rotates boot ID/generation and starts HALTED/INTERVENTION but retains no immutable fresh-creation entitlement. Current schema 2 requires exactly one original protection owner per capacity fill. Historical schema 1 at `fc7cdc7` lacks those owners and evidence tables; it also has a historical implicit `feed_watch` repair path. D must not copy that repair behavior into current-schema recognition.

The governing correction intentionally supersedes next-session activation fixtures, including `test_protected_session_cancels_resting_orb_add_without_resizing_carried_fill`. Preserve its quantity/policy assertions in policy/reducer tests and add an authority test asserting restart/rollover remains fenced, with no activation cancel. Do not use raw SQL permission patches, success-mocked predicates or deleted coverage to make tests pass.

## 2. Proposed schema 4 creation and bootstrap contract

Add centrally defined tables, preserving every existing table/column:

```sql
CREATE TABLE bootstrap_identity (
  singleton INTEGER PRIMARY KEY CHECK(singleton=1),
  body TEXT NOT NULL
);
CREATE TABLE migration_records (
  migration_id TEXT PRIMARY KEY, source_version INTEGER NOT NULL,
  source_digest TEXT NOT NULL, target_version INTEGER NOT NULL,
  body TEXT NOT NULL
);
CREATE TABLE legacy_obligations (
  obligation_id TEXT PRIMARY KEY, source_table TEXT NOT NULL,
  source_id TEXT NOT NULL, kind TEXT NOT NULL, body TEXT NOT NULL,
  UNIQUE(source_table, source_id, kind)
);
```

Bootstrap body version 1 contains `origin` (`fresh` or `migrated`), account/epoch, creation boot/generation/session, creation binding digest, `state` (`eligible`, `consumed`, `ineligible`), activation time/generation, and first invalidation reason. Fresh creation writes `eligible` only in the same transaction that creates the previously nonexistent owner database. An existing empty file is not fresh. Determine existence inside the serializer, avoiding a two-creator pre-lock race. An interrupted creation either rolls back to an unusable existing file or produces a complete valid owner; neither is silently recreated.

Restart permanently invalidates an eligible entitlement, even when activation never happened. Incident and session change invalidate it as part of their transaction; migrated accounts always begin `ineligible`. Consumption is monotonic: no replay or data reconciliation can make it eligible. Missing bootstrap identity in version 4 is corruption, not an upgrade opportunity.

Retain the public `activate_synthetic(*, now)` signature. Under the existing serializer:

1. Validate actor boot and complete current schema, binding/session/time/settlement, source-independent account evidence freshness, policy and capacity. Reject local storage-failure send suppression.
2. If RUNNING/NORMAL, return unchanged state only when consumed activation boot/generation/session/binding identity still matches and current authorization remains valid. This path does not write, renew time, clear incidents or issue commands; ordinary history accumulated after valid bootstrap is compatible with this no-op. A scheduled cutoff or incident fails the identity/authority conditions.
3. Otherwise require eligible fresh origin and exact creation boot/generation/session/binding. Require no incidents, operations, attempts, capacity events/positions/reservations, close reservations, original protection owners or operations, pending takeover, legacy obligations, prior feedback or dispatchable/prepared actions. Require no earlier protection-mode activation. Runtime registration and inert input setup are allowed only if they contain no attempted/dispatched work or fault. Explicitly validate retained tables, not just aggregate zero exposure.
4. Require complete current synthetic account inventory covering all four legs from C's independent producer: zero positions, risk/close/protection orders and unresolved requests. Bind to account/epoch and a post-creation read with existing evidence age limits. A database that is fresh while the producer owns an external order is not empty. Inventory acquisition can occur outside the transaction; consume only a matching fresh read and recheck all local preconditions under the serializer. Extend C's read persistence to permit a bootstrap read purpose in schema 4; do not fabricate a takeover root to request it.
5. Atomically write session mode, consume bootstrap identity and set RUNNING/NORMAL. No cancellation or other command belongs to bootstrap. Failure leaves authority revoked; incident publication must not be rolled back by raising inside a transaction after `_halt_db`. Return/raise after the durable incident commit where appropriate.

The base `SyntheticBroker` is a receipt queue, not an independent inventory producer. Tests using activation must adopt the stateful broker or a supported empty-inventory capability with actual independent state; a hand-authored empty proof is insufficient. Before changing fixtures, retain baseline activation failures using the current helper, then migrate fixtures through public setup APIs.

## 3. Explicit migration interface and recognition

Create `ops/c1_rail/book_migration.py` with no transport imports or activation calls:

```python
@dataclass(frozen=True)
class MigrationResult:
    source_version: int
    target_version: int
    migration_id: str
    disposition: str           # converted, already_converted
    unresolved_ids: tuple[str, ...]

def migrate_book_owner(path: Path, account: str, *, now: datetime
                       ) -> MigrationResult:
    """Explicit offline conversion; transaction contract specified below."""
```

This callable is an explicit offline operation, not a boot side effect or HTTP route. It accepts no broker, current fabricated binding or recovery authorization. Acquire the same canonical path serializer used by `BookAccountOwner`, open the existing database without create, and validate source before any mutation. `boot` continues to refuse recognized legacy versions with a migration-required error.

Recognized inputs must have one well-formed owner_state row, matching account, valid exact table/column shapes and valid historical records:

| Source | Recognition and conversion disposition |
|---|---|
| 1, full layout at `fc7cdc7` | Freeze exact schema/record validators from that revision; preserve legacy rows, add quarantine records for unprovable B/C ownership/evidence |
| 2, full layout at `567a583` | Require B invariant validation; preserve owners/occurrences/facts/obligations byte-for-byte; quarantine historical takeover lacking C proof |
| 3, exact committed C layout | Validate C phases/streams/proofs; retain them unchanged, add permanently ineligible bootstrap record |
| 4 | Validate full current schema and migration record; repeated conversion is a read-only no-op only for an already converted database |
| Unknown, malformed, missing required source/current structures | Refuse without mutation; do not create tables, normalize records or downgrade version |

Do not recognize missing `feed_watch` merely because old boot repaired it. Earlier schema-1 variants need a separately enumerated historical manifest and evidence before support; the initial bounded converter supports the full known `fc7cdc7` layout. An integer version alone is not recognition. Optional settlement tables require their existing attachment/chain validation and are retained intact. Preserve source bytes/IDs and original permission/generation in the migration audit record even while current authority is revoked.

Transaction sequence: validate source and cross-record integrity → compute a canonical logical digest of original schema and sorted original rows → create required new structures → insert deterministic migration/quarantine records → set current HALTED/INTERVENTION, rotate boot/generation to fence old actors, write ineligible bootstrap identity → validate target including obligations → update version → COMMIT. Use transactional SQLite DDL without implicit-commit `executescript`; test the actual driver behavior. The digest excludes migration-created tables and later boot metadata, and is audit provenance, not a broker evidence seal. Migration ID is derived from account/epoch/source version/source digest/target version.

Failure before commit rolls back all conversion writes; failure after commit leaves a fully recognized target whose repeated conversion returns the same migration identity. No database deletion/recreation or history compaction is allowed. Corrupt inputs are preserved and reported by exact table/record identity. If validation cannot safely open/replay them, there is no runtime owner and no send capability.

## 4. Legacy representation without invented protection

Do not synthesize normal B protection owners from a legacy fill. A legacy fill establishes execution identity, not confirmed bracket parameters, live owner status or consumption. Add a durable `legacy_obligations` entry for each unprovable original fill, old accepted/unknown attachment/amendment, pending takeover and unresolved request. Body version 1 contains source version/digest, original row references and retained content, known leg/operation/fill IDs, reason, original deadline if recorded, and disposition `unresolved`. If a deadline was never recorded, retain that absence as unresolved; never create a fresh future deadline. No automatic resolver or rearm API is part of D.

Modify B/C validation narrowly for a migrated/quarantined account:

```text
capacity fill IDs == normal original-owner fill IDs UNION legacy-fill obligation IDs
normal original-owner fill IDs INTERSECT legacy-fill obligation IDs == empty
```

This exception requires a valid migration record naming the exact legacy source fill and digest. It is forbidden for fresh accounts and cannot hide a missing schema-2/3/4 owner: validate those sources under their original invariants before conversion. Normal B owners retain their consumed/pending state and deadlines unchanged. Keep legacy accepted protection in quarantine, never in `observed` working protection. Status exposes unresolved legacy ownership and blocks all mutation paths.

Legacy pending takeover remains in capacity accounting with its original operation/action/reservations. Store an explicit legacy takeover obligation; do not fabricate a C PLAN, child scope, terminal or quiescence proof for already attempted historical work. Historical completed takeover events remain historical accounting, with a legacy evidence-gap record if they lack a C proof. C replay validation accepts this only through the source-bound migration exception and never resumes it.

Read-only ordinary facts may update known legacy accounting through existing identity/cumulative checks, but must not create a normal B owner or erase quarantine merely because the account appears flat. Legacy new fill observations extend the explicit unresolved representation. Protective evidence requiring an unprovable owner is retained as unresolved diagnostic evidence and cannot reduce capacity via invented FIFO. Valid schema-2/3 protection observation and feedback recovery continue through their existing contracts while authority remains revoked. Missing immutable feedback/checkpoint data fails replay; migration cannot manufacture it.

## 5. Work packages and acceptance traces

### D0 — reconcile against committed C

**Files:** this plan, C plan and exact C schema/contracts/validators; immutable legacy fixtures under `tests/fixtures/book_migration/` with provenance manifests.

- [ ] Read C's committed schema and tests; reconcile all proposed version/table/record names here before implementation.
- [ ] Export representative schema-1/2 databases using their original public APIs and revision-bound tooling, without booting them under new code. Include empty, attempted, filled, accepted/unknown amend and pending/completed takeover histories. Capture logical rows/digests and expected feedback before conversion.
- [ ] Export committed-C phase-boundary fixtures and record exact schema/record manifests. Reject historical variants absent from these recognized manifests.
- [ ] Finalize conversion mappings and concrete executable fixtures against those bytes. This is a sequential prerequisite; a provisional schema description is not an executable migration plan or acceptance evidence.

### D1 — one-use bootstrap and serializer races

**Files:** owner boot/activation/halt, C inventory read-purpose codec, synthetic broker fixtures; create `tests/ops/test_book_bootstrap_migration.py`; update `test_book_account_owner.py`, `test_book_owner_settlement_integration.py` and shared occurrence/protection fixtures as required.

- [ ] Reproduce current unsafe empty-incident activation and restarted clean-looking activation. Record failing assertions that permission remains HALTED and broker commands do not increase.
- [ ] Implement schema-4 creation identity and inventory-proven bootstrap. Test fresh complete empty inventory succeeds once; occupied/partial/stale/foreign inventory and any historical operation/attempt/obligation refuse.
- [ ] Verify repeated RUNNING activation is a no-op with unchanged database rows and authority expiry, including after ordinary activity. It must not replace the session mode or rerun cancellation.
- [ ] Use actual serializer/thread coordination to race halt against bootstrap and dispatch. A halt linearized first prevents activation/send; if a send entered transport first, retain it and fence every subsequent send. Race two boots and prove the old actor cannot activate.
- [ ] Replace next-session activation expectations with restart/rollover refusal. Move carried-size arithmetic to policy/reducer tests; keep settlement attachment and record-only revision coverage through public APIs.
- [ ] Run affected owner/settlement/occurrence/protection/runtime suites and review before an authorized commit.

### D2 — explicit transactional conversion and quarantined recovery

**Files:** `book_migration.py`, owner boot/schema/status, protection/takeover validators and ordinary observation, runtime recovery; `test_book_bootstrap_migration.py`, `tests/fixtures/book_migration/`.

- [ ] Write fixture tests asserting original operation/fact/attempt/occurrence/feedback IDs and raw bodies survive conversion. Assert FIFO/reservations and delivered checkpoints replay identically, while permission is HALTED/INTERVENTION and bootstrap is ineligible.
- [ ] Implement source recognition and conversion transaction, migration audit and explicit unresolved rows. Compare source-table logical dumps before/after, permitting only documented owner authority/version changes.
- [ ] Test accepted/unknown legacy amendments never become confirmed protection; legacy fills get quarantine coverage exactly once; schema-2 consumed owners retain pending amendment and original deadline; legacy pending takeover never sends.
- [ ] Inject interruption after each DDL/copy/validation step and immediately before/after COMMIT. Reopen under SQLite recovery and prove either valid original or complete target, repeat conversion idempotence and no partial target accepted by boot.
- [ ] Delete each current required table/owner/proof/bootstrap/migration record in isolated test copies; corrupt versions, timestamps, links and duplicate singleton identity. Assert refusal with no repair or content mutation. Unsupported variants are preserved.
- [ ] Exercise ordinary observation, B protection observation and runtime feedback replay on migrated fixtures without rearm or hidden transport. Compare adapter checkpoints, not just row counts.
- [ ] Run migration and all affected replay/settlement tests; obtain review of recognition and preservation before an authorized commit.

### D3 — combined A–D acceptance

**Files:** A/B/C/D suites, runtime/listener integration tests, image manifests and the correction acceptance record.

- [ ] Run complete C traces with fresh-only bootstrap, including halt/storage failure and every durable phase/attempt boundary. Record baseline and final evidence separately.
- [ ] Run the handoff's targeted, image, full `tests/ops` and check-tier commands, adding both new C/D test files. Recheck edits affecting prior results. Execute synthetic coverage without private inputs or optional signing imports.
- [ ] Independently review the entire corrected path: ingress → occurrence → protection → cancellation/close evidence → admission → bootstrap/migration/replay. Individual file or slice review does not establish combined acceptance.
- [ ] Record actual interpreter, skips, fixture/source revisions, tested diff/commit and review dispositions. Preserve prior evidence logs. Refresh remote and actual-head CI only when integration authorization allows it; no local result establishes remote readiness or deployment authority.

## 6. Documentation review and limitations

Reviewed against current creation/activation and B original-owner validation, plus historical schema 1 at `fc7cdc7`. The important design corrections are explicit creation entitlement, inventory-proven emptiness, no-op versus recovery separation, and a migration-bound quarantine exception that cannot repair missing current records. Failure and restart retain obligations and no send authority.

No implementation tests or migrations were run. C's committed schema, exact legacy fixture exports and executable converter validation remain dependencies for finalizing D; they are intentionally not represented as available. The handoff's documentation-only authorization is the reason this work stops at plans.
