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

Originally a provisional interface-level plan grounded at `567a583`. The user subsequently requested “commit and push, then implement slice d.” C was committed and pushed to PR 409 as `b5fdde8b89aaab6bccc37d2850f9ec14da314819`, and D is implemented against that exact schema 3. Sections 2–6 retain the proposed design/checklist as planning history; section 7 records the concrete implementation, reconciliations and verification. D targets schema 4 and remains local until separately integrated. The coordinating implementer owns combined A–D acceptance.

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

## 7. Implementation and acceptance record — 2026-09-16

The later user instruction authorized implementation. Base is committed C `b5fdde8`; the work remains in `phase2-four-leg-execution`. No live account, deployment or recovery operation is involved. Conversions execute only on disposable synthetic fixture copies during tests.

### Actual schema and interfaces

Schema 4 retains all schema-3 tables and adds the proposed `bootstrap_identity`, `migration_records` and `legacy_obligations`, plus `bootstrap_reads(read_id PRIMARY KEY, body NOT NULL)`. Bootstrap reads use their own purpose-specific table so C's root-bound read/proof contract remains unchanged. Missing current structures or weakened SQL constraints fail recognition; boot does not migrate or repair. Supported legacy source layouts and revisions are frozen in `book_migration_schema.py` and mirrored in the fixture manifest.

`activate_synthetic(now=...)` now consumes a fresh creation entitlement exactly once. Creation existence is checked inside the canonical serializer. Restart invalidates even an unused entitlement; incident invalidation shares the incident transaction. The initial proof is a synchronous `SyntheticProtectionBroker.read_bootstrap_inventory` call under the same serializer/transaction. Equal synthetic timestamps are permitted for this synchronous read because the read is executed after creation and before consumption, with a newly bound read identity; C's asynchronous strictly-postdating rule is unchanged. Complete typed outer and nested protection inventory must cover all four legs and contain no positions, working orders, request history or broker facts. The receipt-only `SyntheticBroker` cannot bootstrap.

Creation/activation identity binds account/epoch/boot/generation/session and the binding digest. The durable read is decoded through the same complete contract used at admission. A RUNNING/NORMAL repeat is a read-only no-op only for the same consumed identity and still-current binding. It does not issue cancellations or renew evidence. Restarts, incidents, rollover and migration cannot reactivate. Existing carried-position and signed-settlement tests preserve their sizing/accounting checks separately while asserting no recovery send. SQLite failures remain latched locally even after storage becomes available again.

The explicit API is `book_migration.migrate_book_owner(path, account, now=..., crash_at=None) -> MigrationResult`; `crash_at` is an offline fault-injection seam. It accepts no broker or activation authority. Recognition validates exact SQL constraints, retained bindings, state/capacity/operation/attempt/fact/feedback relationships and the applicable B/C journals before writing. Attached settlement chains and source BLOBs are validated without booting their store. Canonical audit JSON represents BLOBs as `{"sqlite_blob_hex": "..."}` while live SQLite bytes remain untouched.

Conversion runs transactional DDL, writes a deterministic source-digest-bound migration identity, preserves original rows, rotates boot/generation and leaves HALTED/INTERVENTION with permanently ineligible bootstrap identity. Pre-commit interruption rolls back; post-commit retry validates the target and returns the original migration ID without writes. Subsequent boot validates required original history against the immutable source archive, allowing only documented outcome/checkpoint updates and appended observations.

Only schema-1 fills may lack normal original protection owners; every such fill receives an unresolved source-bound obligation. All original schema-1 operations remain explicitly quarantined, including accepted/unknown legacy controls and unresolved attempts. Only schema-1/2 takeovers may have legacy evidence gaps. The required quarantine set is derived from source records, so deleting an obligation or inventing a schema-3 exemption is corruption. Late schema-1 entry fills extend quarantine instead of creating B protection ownership. Unprovable protective executions are retained as diagnostic facts without changing exposure. Regular `status()` exposes unresolved obligations and their migration provenance.

### Revision-bound fixture evidence

`tests/fixtures/book_migration/` contains logical exports made using original public APIs from `fc7cdc7`, `567a583` and `b5fdde8`, never by downgrading a current database. Each export includes the full source revision, exact SQL, column order, raw rows and canonical logical digest. Cases cover empty/filled state, pending/completed takeover, legacy accepted/unknown amendments, prepared B amendments, consumed B owners with separately pending accepted/unknown amendments, and a populated attached settlement chain. The test loader reconstructs exact SQLite values without invoking owner boot before conversion.

### Review and verification

Independent review drove additional regressions for contradictory nested bootstrap exposure, deleted/forged quarantine, wrapped storage errors, cross-record source corruption, settlement BLOBs, missing original migrated history and incomplete retained proof identities. Failing-before logs are retained in `tmp-slice-d-bootstrap-red.txt`, `tmp-slice-d-migration-red.txt`, `tmp-slice-d-review-red.txt` and `tmp-slice-d-review2-red.txt`. Final review disposition and verification results are recorded below after the final tree passes.

Final independent code review accepted the integrated D contracts with no remaining blockers. The final pass independently ran 83 D tests and additionally verified that an accepted historical resolution survives later unrelated snapshots, while a rejected snapshot cannot justify clearing a pending obligation. Migration preserves original attempts and frozen occurrence scopes in full, preserves protection operation provenance except observed status, and prevents unresolved deadlines from being renewed. Qualifying resolution evidence is found among retained accepted snapshots rather than relying on the latest evidence pointer.

The final focused D suite passed 83 tests. Synthetic integrated C/D/protection/ingress/emulator coverage with `cryptography` and `nacl` imports deliberately blocked passed 303 tests. Both image manifests and image-validation script tests passed 23 tests. Check-tier repository gates returned 0; documented absent private Pine/data trees remained skips/warnings. UTF-8 decoding and Python 3.11 grammar parsing passed for all 15 changed/new Python files; local runtime tests used Python 3.13.2, not Python 3.11.

Task-created historical source archives were preserved outside the repository at `C:/Temp/pr409-slice-d-source-evidence/` after the import-boundary gate correctly discovered their duplicate source trees. No project gate was weakened. Source exports, failing-before logs and final verification logs remain separate evidence.

Slice C was pushed as `b5fdde8`, followed by encoding-only repair `83f06ac`: an invalid byte in an existing regression comment caused Astroid's fatal parse failure. The repair changes only that comment to ASCII and was independently parsed before push. Slice D remains an uncommitted local implementation above that head; remote CI does not validate D. No merge, deployment, live conversion or recovery rearm has been performed.

Final complete operations run: `python -m pytest tests/ops -q -p no:cacheprovider --tb=short` passed **2,630 tests, 15 skipped**, with two existing seaborn deprecation warnings, in 153.19 seconds (`tmp-slice-d-ops-final.txt`). This run includes the final retained-resolution helper and the positive historical replay regression. `git diff --check` also passed. The 303-test signing-disabled result and independent 83-test D review apply to the same final implementation.

Remote Slice C final check snapshot: head `83f06acb9554df65b5fdbb86990d913465a42a4a`, all actual CI checks passed (Pylint, Python 3.11 pytest, both images, skills and Semgrep). CodeRabbit reports its manual-review-required skip as successful; this is not an additional code-review acceptance. PR remains open and mergeable. These remote results apply to committed C only.

### Integration authorization

The subsequent user request authorized committing and pushing Slice D and posting a Codex review request on PR #409. The local verification and independent review above apply to the implementation being committed. Historical statements that D was uncommitted describe the preceding acceptance checkpoint.

### Post-D Codex review repairs — 2026-09-16

Review of `0e2f654` reported four defects; integration starts from `847b6b0`, the owner's subsequent documentation-only merge from main. Each defect was reproduced against the original implementation before repair.

- Settlement submission rejects noncanonical signing key IDs before a mapping lookup; arrays/objects return `unknown_key_or_scope` without an exception, state change or owner storage-failure latch.
- Protection snapshots bound the sum of executable owner quantities per leg to evidenced remaining exposure. Original owner identity and FIFO semantics remain separate; no protection is automatically cancelled or reassigned.
- Scheduled flattening waits for every same-leg entry/add to become terminal. Late fills are included before the flat is sized, and unresolved cancellation at the own-flat deadline retains exposure under INTERVENTION without an unsafe flat.
- New risk is refused account-wide for UNKNOWN ordinary attempts or accepted attempts unresolved for one 15-minute bar. The fence is derived from retained attempt/fact history, holds reservations, covers takeover revalidation and protection loosening, and clears only when every owning attempt has accepted terminal evidence strictly after preparation. Restart still retains HALTED/INTERVENTION authority. Before/equal-time terminal evidence cannot clear an aged attempt; unsupported general inventory recovery is not inferred from a receipt.

Independent review accepted the changes after reproducing and correcting a temporal shortcut for accepted attempts. Review regressions cover multiple pending owners, clearing only one, terminal timing, restart, scheduled cutoff/flatten/deadline, aggregate protection, and malformed keys through standalone and unified settlement APIs. The original lifecycle tests now explicitly supply accepted receipts when their scenario needs two concurrent pending orders; their prior empty queues returned UNKNOWN. The old scheduled-flat-before-terminal expectation was replaced with terminal-first reconciliation.

Focused integration: 208 passed across review4, owner lifecycle, review3, bootstrap/migration and takeover phases. Unified malformed-key regressions: 2 passed. Check-tier repository gates returned 0, with the existing absent private Pine/data warnings. Final full-suite evidence follows below.

Final reviewed tree: full operations **2,651 passed, 15 skipped**, two existing seaborn warnings, 181.88s; signing-disabled integrated execution **313 passed**, 73.96s. Local interpreter Python 3.13.2; check-tier gates and diff whitespace check passed. No live transport or deployment was used.

### Related-case follow-up on `17aa7ec` — 2026-09-16

Integration owner: the coordinating implementer. The latest three review findings
share two bounded failure families. A close must not allocate exposure while a
same-leg entry/add has an executable remainder: cancellation transport status is
not terminal evidence. Configuration and package boundaries must establish the
types their consumers rely on before retaining authority or performing lookups;
validated mutable caller maps must not remain aliased after boot.

| Related path or input | Shared rule | Disposition and evidence |
| --- | --- | --- |
| Adapter/direct exit and flat, explicit fill scope | Live entry/add remainder can recreate exposure after close | Common `_reserve_close` checks retained same-leg reserved capacity before allocating; accepted, unknown and rejected cancellation tests retain exposure until terminal evidence. |
| Unfilled/partially filled add; no cancellation yet | Another same-leg risk order can still fill | Same common guard, including scoped closes of the earlier base. |
| Fully filled entry without a separate terminal; unrelated-leg live order | No executable remainder for the closing leg | Valid nearby cases remain admissible; no account-wide close prohibition. |
| Scheduled and takeover closes | Same allocation owner, with additional evidence prerequisites | Existing scheduler terminal gate and takeover complete-inventory phases retained; shared allocator adds defense at final allocation. |
| Duplicate occurrence, new evaluation, restart | Refusal identity and reservations survive reconstruction | Same occurrence retains refusal; new occurrence after terminal can size from reconciled late fills. Runtime batch regression replays the refusal and retained exposure after boot. |
| Settlement and nested flatness bases | Set lookup requires a scalar string | Existing settlement-basis guard retained; flatness-basis guard added at package shape boundary. Missing equity keys already return `equity_keys`. |
| Venue equity valuation basis | Evidence description must be text, not a coerced collection | Reject list/object filename representations; legitimate daily-flat `None` remains supported. |
| Standalone calculation, signed store and unified owner | Malformed package must return a refusal without accepting a close or raising a storage error | Pure and signed entry-point regressions; signed imports are local to signing tests. |
| Lifecycle, allocation and risk maps | Consumers index/get per-leg mappings, not iterables of keys | Validate all three as mappings and copy them before retention; lifecycle and allocation still require all legs, risk remains sparse. Validate values with existing policy laws; Decimal/Fraction risks preserved. |
| Caller mutation after boot | Runtime sizing must use the retained validated binding | Detached map copies keep later mutation from changing quantity or retained digest; plain dict and Mapping implementations tested. |
| Source rows, coverage windows and transaction identities | Adjacent nested strings used as mapping keys | Existing validators type-check strings before membership/indexing in `account_close_evidence` and `_v10_transactions`; no change required. |

Execution checklist:

- [x] Trace governing implementation and consumers before patching; no sizing constants or strategy parameters changed.
- [x] Reproduce direct-close, nested-equity and binding failures against the original code; initial corrected boundary run: 49 failed, 11 passed (two integration fixtures subsequently corrected).
- [x] Fix the common close allocator and the two input boundaries; initial focused integration: 149 passed.
- [x] Run final related cases, full operations, required repository gates and independent review; results below.

Commands: `python -m pytest tests/ops -q -p no:cacheprovider --tb=short` and
`python scripts/gate_manifest.py --tier check`. Tests are offline synthetic; no
production capability, merge or deployment claim follows from this evidence.

Final local evidence (working-tree changes above `17aa7ecb94f27fd9690391977af7c7f8f8fa7206`,
Python 3.14; remote head rechecked unchanged):

- Final operations run: **2,718 passed, 15 skipped**, two existing seaborn
  deprecation warnings, exit 0, 151.18 seconds (`tmp-related-ops-final.txt`).
- Final related-case file: **67 passed**, including all six signing cases.
  Signing-disabled run: **61 passed, 6 skipped**, so runtime cases do not depend
  on the optional cryptography package.
- Check-tier gates: exit 0 (`tmp-related-gates.txt`); existing absent-private-data,
  absent Pine and historical documentation advisories remain.
- Python 3.11 grammar parsing passed for all five changed/new Python files;
  `git diff --check` passed. This is grammar compatibility, not a Python 3.11
  runtime result.
- Targeted Pylint with repository import roots reports only the unchanged
  `_boot_locked(owner)` E0213 naming diagnostic already present in the base.
  It returned exit 2; a clean lint run is not claimed.
- Independent read-only review accepted the complete changes and subsequently
  checked the three updated legacy test expectations. The two invalid-binding
  tests now assert rejection before database creation; the valid partial-close
  fixture supplies terminal cancellation evidence first. The reviewer did not
  independently execute the full suite.

All discovered in-scope paths have a disposition. At the local acceptance
checkpoint, these changes were uncommitted and remote CI had not validated them.
The subsequent operator request authorizes committing and pushing this patch to
PR 409 and requesting a Codex review. The local evidence above applies to the
code being committed; post-push CI and review are separate checks.

### Runtime and close reconciliation follow-up on `5b948ca` — 2026-09-16

Integration owner: coordinating implementer. A completed bar must extend the
bound session's contiguous history and every resulting order must name that
exact boundary and producing leg. An ordinary close is not reconciled while
its residual attached orders remain unproven; another close on that symbol
must wait. Fully filled terminal evidence does not mean cancellation.

| Related path or input | Shared rule | Disposition and evidence |
| --- | --- | --- |
| First live bar, resumed session, retained complete/partial history | No missing opening or intervening boundaries | Runtime checks from persisted session open; watchdog anchors session open, not process start. Chronology regressions include restart and invalid retained history. |
| `on_bar` and `set_mode` actions | Order timestamps and leg identity belong to the producing barrier | Exact timestamp/leg validation; missing, prior, future and cross-leg variants rejected before dispatch. |
| Equivalent timezone spellings and retained payload timestamps | One instant names one bar occurrence | UTC live normalization, instant-based duplicate comparison, retained payload checks and duplicate-history refusal. |
| Protected partial/full close, cancellation after partial execution | Accounting changes on observed fill; adapter feedback waits for complete residual evidence | Durable held feedback and `awaiting_protection`; complete fresh reads release ordered events, missing evidence expires to intervention. |
| Duplicate old snapshot, delayed fill, pending attachment | An earlier receipt is not proof of the new residual state | Duplicate reads cannot release new obligations; pending protection queues closes until confirmed. |
| Protective execution and takeover inventory | All complete inventory consumers share close reconciliation | Reconcile held ordinary fills before protective feedback; takeover inventories include held feedback only after successful fresh protection validation. |
| Same-symbol close overlap, new arrivals ahead of queued demand | Only one in-flight close; preserve queue order | Durable `close_pending` occurrences reserve nothing; common allocator enforces FIFO and runtime fact/protection/schedule callbacks resume eligible demands. |
| Repeated scheduled flatten, restart, authority generation | Replay must not resend or invent a different action for the same occurrence | Reuse queued scheduled source; restart retains halted authority and evidence obligations; cutoff retires superseded queued demands explicitly. |
| Filled entry/close terminal and strict adapter consumer | Terminal fill evidence is not a cancellation instruction | Retain valid terminal in broker journal without adapter event; real strict execution reducer and unknown-attempt clearing regressions. |

Initial close regressions: 8 failed. Runtime chronology failures reproduced
before repair, including timezone duplicate behavior. Independent close review
reproduced the stale-snapshot variant and accepted its repair with edge tests.
Final verification and publication evidence will be recorded below.

The branch predates the operations launcher present in the parent checkout.
For final verification, its launcher files were copied here as untracked tooling
and excluded from this patch. `./fp.ps1 doctor` selected the shared isolated
operations environment, Python 3.13.2, and matched all 62 locked distributions
(optional cryptography 50.0.1). Earlier diagnostic runs used Python 3.14; final
results below use the validated environment and this checkout's sources.

Verification above `5b948ca4419d5367862bc4e5d37c8ea222f6105c`:

- `./fp.ps1 test-ops -q -p no:cacheprovider --tb=short`: **2,758 passed,
  15 skipped**, four dependency deprecation warnings, exit 0 (215.59s).
- After the final protective-execution queue callback and its additional
  regression, all four new regression files passed: **41 passed**, exit 0
  (9.94s). This refresh covers the final code; the full run began before that
  final two-line callback change and additional test.
- `./fp.ps1 check`: exit 0; existing absent private-data/Pine and historical
  documentation advisories remain. Python 3.11 grammar parsing passed for
  all 15 changed/new Python files; this is not a Python 3.11 runtime claim.
- Targeted Pylint with repository import roots: only unchanged E0213 on
  `_boot_locked(owner)`, exit 2. No clean lint claim. `git diff --check` passed.
- Independent close review accepted the bounded changes after reproducing
  the duplicate-snapshot and cutoff-generation variants. Takeover final
  revalidation already checks unresolved attempts account-wide and invalidates
  proof after operation changes; no extra admission rule was required there.
- Remote PR head was rechecked at `5b948ca` before publication. Tests are
  offline synthetic; no production activation, deployment or merge occurred.

### Review follow-up on `d14d74f` — 2026-09-16

The three new findings share journal-consumer and identity assumptions missed
by the preceding case map. Accepted broker facts, held adapter events, and
emitted events are distinct states. Protection quantity follows explicit close
allocations while protective fills retain the separate FIFO rule. Completed and
partial bar identities must remain distinct before any in-memory consolidation.

| Related case | Shared rule | Disposition |
| --- | --- | --- |
| Filled terminal after versions 1/2/3 conversion | No event is SQL NULL, not an emitted JSON value | Store SQL NULL; repeat conversion remains read-only and idempotent. Previous v4 JSON-null records remain readable only with valid filled-terminal proof and no emitted-event timeline. |
| UNKNOWN and aged ACCEPTED entry/add attempts | Feedback absence cannot determine fact acceptance | Resolve from matching broker/capacity terminal identity, time and payload plus reducer-accepted terminal state. Stale, incomplete and non-postdating facts retain the fence. |
| Held partial/full close and cancellation after partial fill | Deliberately deferred feedback is not missing emitted feedback | Migration accepts only an awaiting-protection close with accepted reduction evidence; a preexisting feedback timeline prevents masking deleted emitted events. |
| Scoped partial/full explicit close with sibling protection | The close must resize its allocated owner | Validate scoped residual quantities at the relevant reduction sequence; synthetic producer now actually resizes partial scoped orders. |
| Protective FIFO before or after explicit close, delayed observation, restart | Origin-lot remainder alone does not describe surviving FIFO protection | Preserve FIFO coverage, distinguish newly reconciled explicit closes with a capacity sequence cursor, and use held fact identities for older rows without the cursor. No timestamp-only inference. |
| Completed/partial overlap, duplicate same-leg partials, timezone aliases | Raw durable identity must be checked before dictionary/set collapse | Reject duplicate identities during construction. Canonical distinct-leg partials recover and complete; historical noncanonical partial keys fail closed because text-key promotion/expiry cannot safely resume them. No history rewrite. |

Initial journal regression run: 6 failed, 4 passed. Initial runtime run: 6 failed,
19 passed. Scoped-close producer and consumer failures were reproduced separately.
Independent journal review accepted the changes with 24 focused tests passing.
Final combined verification is recorded below once complete.

Independent protection review additionally reproduced a same-owner partial
protective execution after an unobserved scoped close: the pre-execution
remainder check still used the pre-close quantity. The common residual rule
must govern both snapshot reconciliation and the protective execution's initial
quantity check. The separate regression covers partial and terminal execution
plus overstated quantity. Earlier full runs were superseded while this repair
was in progress and are not acceptance evidence.

The inverse ordering (FIFO, then an explicit scoped close) also reproduced
overlapping protection in the synthetic producer. The pinned emulator's
`_close_scope` removes zero-lot owners after an explicit close, including a
sibling whose origin was exhausted by an earlier FIFO fill; `_fill_exit` alone
does not. The repair records this removal eligibility at the explicit close's
sequence and applies the same rule to the producer. A later FIFO exhaustion
cannot retrospectively authorize removal, and unrelated legs are excluded.

If FIFO leaves a nonzero origin with different working protection quantity,
certain partial explicit closes cannot preserve both the pinned cleanup rule
and I7. Before reserving or sending, the common close allocator models the
qualified residual transition: remaining working protection cannot exceed
residual exposure or lose more defined coverage than the quantity closed.
Otherwise it returns `close_capability_problem`, following K2's required
capability block rather than transferring/cancelling an owner under invented
semantics. Full flatten remains a supported nearby transition; bare lots do not
acquire new protection requirements.

Final review-6 acceptance on `d14d74f` plus the final working-tree changes:

- Validated launcher environment: Python 3.13.2, 62 matched locked packages.
- `./fp.ps1 test-ops -q -p no:cacheprovider --tb=short`: **2,803 passed,
  15 skipped**, four dependency deprecation warnings, exit 0 (181.10s).
  This run includes all final production changes and all 44 new regressions.
- `./fp.ps1 check`: exit 0. Existing absent private-data/Pine and historical
  documentation advisories remain.
- Independent bounded journal and protection reviews accepted the repaired
  cases. Final protection edge suite: **6 passed** (2.61s), including both
  pre-dispatch capability refusals and the subsequent valid full flatten.
- Python 3.11 grammar parsing passed for all nine changed/new Python files;
  this is not a Python 3.11 runtime claim.
- Targeted Pylint with `ops` and `core` import roots reports only unchanged
  E0213 on `_boot_locked(owner)`, exit 2. No clean lint claim.
- `git diff --check` passed. PR head remained `d14d74f` before publication.
  Tests are offline synthetic; no deployment, live activation or merge.
